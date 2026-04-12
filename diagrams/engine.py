"""
Diagram Engine — dispatches diagram generation to the appropriate renderer.

Takes structured data + target dimensions, returns rendered diagrams as either:
  - PNG file paths (for draw.io and AI approaches)
  - PPTX shape objects (for native approach)

Usage:
    engine = DiagramEngine()
    results = engine.generate(
        diagram_type="org-hierarchy",
        data={...},
        target_width_in=4.5,
        target_height_in=2.5,
        approaches=["native", "drawio", "ai"],
        style="corporate",
    )
    # results = [
    #     {"approach": "native", "type": "shapes", "shapes_fn": callable},
    #     {"approach": "drawio", "type": "png", "path": "/tmp/...png"},
    #     {"approach": "ai", "type": "png", "path": "/tmp/...png"},
    # ]
"""

import os
import tempfile

from .native_renderer import NativeRenderer
from .drawio_renderer import DrawioRenderer
from .ai_renderer import AIRenderer

# Which approaches support which diagram types
APPROACH_CAPABILITIES = {
    "native": [
        "org-hierarchy", "flow", "comparison", "timeline",
        "key-stats", "labeled-boxes", "process-steps",
    ],
    "drawio": [
        "org-hierarchy", "flow", "architecture", "comparison",
        "timeline", "network", "labeled-boxes", "process-steps",
    ],
    "ai": [
        "org-hierarchy", "flow", "architecture", "comparison",
        "timeline", "network", "conceptual", "data-visual",
        "labeled-boxes", "process-steps",
    ],
}

# Default design tokens — used when no brand is passed
DESIGN_TOKENS = {
    "colors": {
        "purple": "#5F016F",
        "pink": "#FF80D4",
        "light_pink": "#FFADE4",
        "light_bg": "#F0E8F5",
        "white": "#FFFFFF",
        "dark": "#333333",
        "gray": "#888888",
        "divider": "#D0C0D8",
    },
    "fonts": {
        "heading": "Urbanist ExtraBold",
        "body": "DM Sans",
    },
    "brand": "Default",
}


def tokens_from_brand(brand):
    """Derive design tokens from a BrandConfig instance."""
    return {
        "colors": {
            "purple": "#" + brand.primary_hex,
            "pink": "#" + brand.secondary_hex,
            "light_pink": "#" + brand.accent_hex,
            "light_bg": "#" + brand.bg_light_hex,
            "white": "#FFFFFF",
            "dark": "#" + brand.text_dark_hex,
            "gray": "#" + brand.color_hex("text_gray"),
            "divider": "#" + brand.divider_hex,
        },
        "fonts": {
            "heading": brand.heading_font,
            "body": brand.body_font,
        },
        "brand": brand.name,
    }


class DiagramEngine:
    """Main diagram generation dispatcher."""

    def __init__(self, brand=None):
        tokens = tokens_from_brand(brand) if brand else DESIGN_TOKENS
        self.native = NativeRenderer(tokens)
        self.drawio = DrawioRenderer(tokens)
        self.ai = AIRenderer(tokens)
        self._renderers = {
            "native": self.native,
            "drawio": self.drawio,
            "ai": self.ai,
        }

    def generate(self, diagram_type, data, target_width_in, target_height_in,
                 approaches=None, style="corporate", output_dir=None):
        """Generate diagram variants using multiple approaches.

        Args:
            diagram_type: Type of diagram (org-hierarchy, flow, architecture, etc.)
            data: Structured data describing the diagram content
            target_width_in: Target width in inches
            target_height_in: Target height in inches
            approaches: List of approaches to try (None = all capable)
            style: Visual style (corporate, tech-gradient, blueprint, isometric, glassmorphism, neon-wireframe, paper-cut, minimal-line, hand-drawn)
            output_dir: Directory for generated PNG files

        Returns:
            List of result dicts, each with:
              approach: which approach generated it
              type: "shapes" (native) or "png" (drawio/ai)
              path: PNG file path (for png type)
              shapes_fn: callable(slide) that adds shapes (for shapes type)
              label: human-readable description
        """
        if output_dir is None:
            output_dir = tempfile.mkdtemp(prefix="deck-diagrams-")

        # Determine which approaches to use
        if approaches is None:
            approaches = [a for a, types in APPROACH_CAPABILITIES.items()
                          if diagram_type in types]
        else:
            approaches = [a for a in approaches
                          if diagram_type in APPROACH_CAPABILITIES.get(a, [])]

        if not approaches:
            print(f"    WARNING: No approach supports diagram type '{diagram_type}'")
            return []

        results = []
        for approach_name in approaches:
            renderer = self._renderers[approach_name]
            try:
                result = renderer.render(
                    diagram_type=diagram_type,
                    data=data,
                    target_width_in=target_width_in,
                    target_height_in=target_height_in,
                    style=style,
                    output_dir=output_dir,
                )
                if result:
                    result["approach"] = approach_name
                    results.append(result)
            except Exception as e:
                print(f"    WARNING: {approach_name} renderer failed: {e}")

        return results

    def get_capable_approaches(self, diagram_type):
        """Return which approaches can handle a given diagram type."""
        return [a for a, types in APPROACH_CAPABILITIES.items()
                if diagram_type in types]
