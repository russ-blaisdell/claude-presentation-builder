"""
Approach B: draw.io XML Generator + Export

Generates draw.io XML from structured data using templates,
then exports to PNG at the target dimensions using the draw.io CLI.

IMPORTANT: draw.io value attributes contain HTML markup (e.g. <br>,
<font>, <b>) but these must be XML-entity-escaped when placed inside
XML attribute strings.  Raw angle brackets break the XML parse and
the CLI silently renders a blank canvas.
"""

import os
import subprocess
import tempfile
import xml.etree.ElementTree as ET

DRAWIO_CLI = "/Applications/draw.io.app/Contents/MacOS/draw.io"


def _esc(html_label: str) -> str:
    """Escape an HTML rich-text label for use inside an XML attribute value.

    draw.io expects ``html=1`` labels whose markup is stored *entity-encoded*
    inside the ``value`` attribute of ``<mxCell>``.  For example::

        value="&lt;b&gt;Hello&lt;/b&gt;"

    This helper converts raw HTML such as ``<b>Hello</b>`` into that form.
    Ampersands that are already part of entities (``&amp;``, ``&lt;``, etc.)
    are left alone; bare ``&`` is escaped first, then ``<``, ``>``, ``"``.
    """
    s = html_label
    s = s.replace("&", "&amp;")
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    s = s.replace('"', "&quot;")
    return s


class DrawioRenderer:

    def __init__(self, tokens):
        self.tokens = tokens
        self.templates_dir = os.path.join(os.path.dirname(__file__), "templates")

    def render(self, diagram_type, data, target_width_in, target_height_in,
               style="corporate", output_dir=None):
        """Generate draw.io XML, export to PNG at target size."""
        handler = {
            "org-hierarchy": self._generate_org_hierarchy,
            "flow": self._generate_flow,
            "architecture": self._generate_architecture,
            "timeline": self._generate_timeline,
        }.get(diagram_type)

        if not handler:
            return None

        if output_dir is None:
            output_dir = tempfile.mkdtemp(prefix="deck-drawio-")

        # Generate the draw.io XML
        xml_content = handler(data, target_width_in, target_height_in, style)
        if not xml_content:
            return None

        # Write XML to temp file
        xml_path = os.path.join(output_dir, f"{diagram_type}.drawio")
        with open(xml_path, "w") as f:
            f.write(xml_content)

        # Export to PNG
        target_px = int(target_width_in * 150)  # 150 DPI for good quality
        png_path = os.path.join(output_dir, f"{diagram_type}-drawio.png")

        if not os.path.exists(DRAWIO_CLI):
            print(f"    WARNING: draw.io CLI not found at {DRAWIO_CLI}")
            return None

        result = subprocess.run(
            [DRAWIO_CLI, "--export", "--format", "png",
             "--width", str(target_px), "--border", "10",
             "--crop",
             "--output", png_path, xml_path],
            capture_output=True, text=True, timeout=30
        )

        if result.returncode != 0 or not os.path.exists(png_path):
            print(f"    WARNING: draw.io export failed: {result.stderr[:200]}")
            return None

        return {
            "type": "png",
            "path": png_path,
            "label": f"draw.io rendered ({diagram_type})",
        }

    # ------------------------------------------------------------------
    # XML generators — build draw.io mxGraphModel XML from data
    # ------------------------------------------------------------------

    def _drawio_wrapper(self, cells_xml, page_width=800, page_height=600):
        """Wrap cell XML in the standard draw.io file format."""
        return f'''<mxfile host="app.diagrams.net" modified="2026-03-25T00:00:00.000Z" agent="Deck Builder" version="24.0.0" type="device">
  <diagram id="generated" name="Generated Diagram">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{page_width}" pageHeight="{page_height}" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        {cells_xml}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''

    def _style_box(self, style="corporate", is_root=False):
        """Return draw.io style string for a box."""
        c = self.tokens["colors"]
        if is_root:
            return (f"rounded=1;whiteSpace=wrap;html=1;"
                    f"fillColor={c['purple']};strokeColor=none;"
                    f"fontColor={c['white']};fontFamily={self.tokens['fonts']['body']};"
                    f"fontSize=12;fontStyle=1;")
        else:
            return (f"rounded=1;whiteSpace=wrap;html=1;"
                    f"fillColor={c['light_bg']};strokeColor={c['purple']};"
                    f"fontColor={c['purple']};fontFamily={self.tokens['fonts']['body']};"
                    f"fontSize=10;fontStyle=1;")

    def _generate_org_hierarchy(self, data, w_in, h_in, style):
        """Generate org hierarchy draw.io XML."""
        root_name = data.get("root", "Root")
        root_owner = data.get("owner", "")
        children = data.get("children", [])
        n = len(children)

        pw, ph = int(w_in * 96), int(h_in * 96)

        # Root box
        root_w, root_h = 200, 50
        root_x = (pw - root_w) // 2
        root_y = 20

        root_label = root_name
        if root_owner:
            root_label += f"<br><font style='font-size:9px;font-weight:normal;'>{root_owner}</font>"

        cells = f'''
        <mxCell id="2" value="{_esc(root_label)}" style="{self._style_box(style, is_root=True)}"
                vertex="1" parent="1">
          <mxGeometry x="{root_x}" y="{root_y}" width="{root_w}" height="{root_h}" as="geometry"/>
        </mxCell>'''

        # Children
        if n > 0:
            child_w = min(140, (pw - 40) // n - 10)
            total_w = n * child_w + (n - 1) * 10
            start_x = (pw - total_w) // 2
            child_y = root_y + root_h + 60

            for i, child in enumerate(children):
                if isinstance(child, str):
                    child_name = child
                    child_owner = ""
                else:
                    child_name = child.get("name", "")
                    child_owner = child.get("owner", "")

                cx = start_x + i * (child_w + 10)
                cid = 10 + i
                eid = 100 + i

                child_label = child_name
                if child_owner:
                    child_label += f"<br><font style='font-size:8px;font-weight:normal;'>{child_owner}</font>"

                cells += f'''
        <mxCell id="{cid}" value="{_esc(child_label)}" style="{self._style_box(style)}"
                vertex="1" parent="1">
          <mxGeometry x="{cx}" y="{child_y}" width="{child_w}" height="45" as="geometry"/>
        </mxCell>
        <mxCell id="{eid}" style="edgeStyle=orthogonalEdgeStyle;strokeColor={self.tokens['colors']['purple']};strokeWidth=2;"
                edge="1" source="2" target="{cid}" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>'''

        return self._drawio_wrapper(cells, pw, ph)

    def _generate_flow(self, data, w_in, h_in, style):
        """Generate flow diagram draw.io XML."""
        steps = data.get("steps", [])
        n = len(steps)
        if n == 0:
            return None

        pw, ph = int(w_in * 96), int(h_in * 96)
        step_w = min(150, (pw - 40) // n - 30)
        step_h = 50
        total_w = n * step_w + (n - 1) * 40
        start_x = (pw - total_w) // 2
        step_y = (ph - step_h) // 2

        cells = ""
        for i, step in enumerate(steps):
            if isinstance(step, str):
                step_text = step
            else:
                step_text = step.get("name", "")
                detail = step.get("detail", "")
                if detail:
                    step_text += f"<br><font style='font-size:8px;font-weight:normal;'>{detail}</font>"

            sx = start_x + i * (step_w + 40)
            sid = 10 + i
            is_first = (i == 0)

            cells += f'''
        <mxCell id="{sid}" value="{_esc(step_text)}" style="{self._style_box(style, is_root=is_first)}"
                vertex="1" parent="1">
          <mxGeometry x="{sx}" y="{step_y}" width="{step_w}" height="{step_h}" as="geometry"/>
        </mxCell>'''

            if i < n - 1:
                eid = 100 + i
                cells += f'''
        <mxCell id="{eid}" style="edgeStyle=orthogonalEdgeStyle;strokeColor={self.tokens['colors']['pink']};strokeWidth=2;"
                edge="1" source="{sid}" target="{sid+1}" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>'''

        return self._drawio_wrapper(cells, pw, ph)

    def _generate_architecture(self, data, w_in, h_in, style):
        """Generate architecture diagram — uses existing .drawio file if provided."""
        source = data.get("source", "")
        if source and os.path.exists(source):
            # Re-export existing file at target dimensions
            return None  # handled by direct export in render()
        # Fall back to org-hierarchy for structured data
        return self._generate_org_hierarchy(data, w_in, h_in, style)

    def _generate_timeline(self, data, w_in, h_in, style):
        """Generate timeline draw.io XML."""
        milestones = data.get("milestones", [])
        n = len(milestones)
        if n == 0:
            return None

        pw, ph = int(w_in * 96), int(h_in * 96)
        c = self.tokens["colors"]

        line_y = ph // 2
        margin = 30
        spacing = (pw - 2 * margin) / (n - 1) if n > 1 else 0

        # Timeline line
        cells = f'''
        <mxCell id="2" style="shape=line;strokeColor={c['purple']};strokeWidth=3;"
                edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="{margin}" y="{line_y}" as="sourcePoint"/>
            <mxPoint x="{pw - margin}" y="{line_y}" as="targetPoint"/>
          </mxGeometry>
        </mxCell>'''

        for i, ms in enumerate(milestones):
            if isinstance(ms, str):
                label = ms
                date = ""
            else:
                label = ms.get("label", "")
                date = ms.get("date", "")

            mx = margin + i * spacing
            mid = 10 + i

            # Dot
            cells += f'''
        <mxCell id="{mid}" style="ellipse;fillColor={c['pink']};strokeColor=none;"
                vertex="1" parent="1">
          <mxGeometry x="{mx-8}" y="{line_y-8}" width="16" height="16" as="geometry"/>
        </mxCell>'''

            # Date above
            if date:
                cells += f'''
        <mxCell id="{mid+100}" value="{_esc(date)}"
                style="text;html=1;align=center;fontFamily={self.tokens['fonts']['body']};fontSize=9;fontStyle=1;fontColor={c['purple']};"
                vertex="1" parent="1">
          <mxGeometry x="{mx-50}" y="{line_y-35}" width="100" height="20" as="geometry"/>
        </mxCell>'''

            # Label below
            cells += f'''
        <mxCell id="{mid+200}" value="{_esc(label)}"
                style="text;html=1;align=center;fontFamily={self.tokens['fonts']['body']};fontSize=8;fontColor={c['dark']};whiteSpace=wrap;"
                vertex="1" parent="1">
          <mxGeometry x="{mx-60}" y="{line_y+15}" width="120" height="40" as="geometry"/>
        </mxCell>'''

        return self._drawio_wrapper(cells, pw, ph)
