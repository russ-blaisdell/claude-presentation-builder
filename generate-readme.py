#!/usr/bin/env python3
"""
Generate README.md from showcase deck YAML and proof images.

Reads the showcase YAML, matches proof PNGs to slides by index,
and produces a README with screenshots and collapsible YAML blocks.

Usage:
    python3 generate-readme.py [--yaml showcase-deck.yaml] [--proof-dir showcase-deck-proof]
"""

import argparse
import os
import re
from pathlib import Path

import yaml


# Layout metadata for the README — descriptions and categories
LAYOUT_META = {
    "title_cover": {
        "display": "Title Cover",
        "category": "structural",
        "description": "Full-bleed background image with two-line text overlay. Auto-splits headline at dash separators (line 1 white, line 2 pink).",
    },
    "agenda": {
        "display": "Agenda",
        "category": "structural",
        "description": "Left background image with numbered items and purple divider lines. Supports up to 7 items with dynamic row spacing.",
    },
    "section_divider": {
        "display": "Section Divider",
        "category": "structural",
        "description": "Visual break between deck sections. Purple, light, or image background with large section number, headline, and optional icon.",
    },
    "closing": {
        "display": "Closing",
        "category": "structural",
        "description": "Large centered headline with optional subheader and background image. Text color adapts to background.",
    },
    "content_two_col": {
        "display": "Two-Column",
        "category": "content",
        "description": "Left stats graphic (3 style variants) with right-side stacked sections. Icons, titles, body text, and divider.",
    },
    "content_diagram_text": {
        "display": "Diagram + Text",
        "category": "content",
        "description": "Split layout combining a diagram (native, draw.io, or AI-generated) with text sections. Vertical and horizontal splits with auto-ratio bumping.",
    },
    "side_by_side": {
        "display": "Side-by-Side",
        "category": "content",
        "description": "Two equal columns with icons beside titles and body text below. Vertically centered. Great for comparisons and two-topic overviews.",
    },
    "three_column": {
        "display": "Three-Column",
        "category": "content",
        "description": "Three titled columns with icons and body text. Vertically centered in available space.",
    },
    "four_card": {
        "display": "Card Grid",
        "category": "content",
        "description": "Dynamic card layout with light purple backgrounds. Renders 1-8 cards with auto-adjusting width and font size.",
    },
    "numbered_list": {
        "display": "Numbered List",
        "category": "content",
        "description": "Large numbers with title and body per item, separated by light dividers. For step-by-step processes and decision frameworks.",
    },
    "before_after": {
        "display": "Before / After",
        "category": "content",
        "description": "Transformation slide with two columns (neutral left, branded right) and a center arrow. Current state vs. target state.",
    },
    "content_table": {
        "display": "Table",
        "category": "data",
        "description": "Styled table with purple header, optional row striping, and auto-sized columns. First column bolded in purple as row labels.",
    },
    "content_table_bullets": {
        "display": "Table + Bullets",
        "category": "data",
        "description": "Table in top portion with bullet points below. Supports color-coded cells and legends.",
    },
    "matrix": {
        "display": "Matrix",
        "category": "data",
        "description": "Color-coded matrix for RACI charts, responsibility grids, or capability assessments. Cell backgrounds mapped by value.",
    },
    "kpi_dashboard": {
        "display": "KPI Dashboard",
        "category": "data",
        "description": "Grid of 2-8 metric cards with numbers, labels, trend arrows, targets, and icons. Highlight cards use purple background.",
    },
    "status_board": {
        "display": "Status Board",
        "category": "data",
        "description": "Red/Amber/Green status tracking with colored circles, workstream names, and summaries.",
    },
    "big_stat_manual": {
        "display": "Big Stat",
        "category": "feature",
        "description": "Large centered number (72pt) with label and optional icon. For hero metrics and key statistics.",
    },
    "quote": {
        "display": "Quote",
        "category": "feature",
        "description": "Decorative quotation mark with centered quote text, pink rule, and attribution.",
    },
    "callout": {
        "display": "Callout",
        "category": "feature",
        "description": "Key takeaway with large text. Boxed (purple card, white text) or open (purple text, pink rule) styles.",
    },
    "roadmap": {
        "display": "Roadmap",
        "category": "feature",
        "description": "Gantt-style timeline with time axis, swimlane rows, colored status bars, and milestone diamonds.",
    },
    "funnel": {
        "display": "Funnel",
        "category": "feature",
        "description": "Progressively narrowing bars showing pipeline stages. Purple-to-pink color gradient.",
    },
    "image_showcase": {
        "display": "Image Showcase",
        "category": "feature",
        "description": "Full-slide image with optional caption and border. Maintains aspect ratio, centered in available space.",
    },
}

CATEGORY_ORDER = ["structural", "content", "data", "feature"]
CATEGORY_LABELS = {
    "structural": "Structural",
    "content": "Content",
    "data": "Data & Metrics",
    "feature": "Feature & Visualization",
}
CATEGORY_DESCRIPTIONS = {
    "structural": "Opening, navigation, and closing slides that frame the deck.",
    "content": "Multi-column layouts for presenting ideas, comparisons, and processes.",
    "data": "Tables, dashboards, and status tracking for data-heavy slides.",
    "feature": "Single-focus slides for metrics, quotes, timelines, and key takeaways.",
}

# Slides to feature in the hero grid (diverse visual mix)
HERO_SLIDES = [
    ("title_cover", "Title Cover"),
    ("kpi_dashboard", "KPI Dashboard"),
    ("roadmap", "Roadmap"),
    ("before_after", "Before / After"),
    ("callout", "Callout"),
    ("content_table", "Table"),
]


def extract_slide_yaml(yaml_path):
    """Extract individual slide YAML blocks from the showcase deck."""
    with open(yaml_path) as f:
        deck = yaml.safe_load(f)

    slides = []
    for slide_def in deck.get("slides", []):
        layout = slide_def.get("layout", "unknown")
        clean = yaml.dump([slide_def], default_flow_style=False, allow_unicode=True, sort_keys=False)
        slides.append({
            "layout": layout,
            "headline": slide_def.get("headline", slide_def.get("callout_text", "")[:50]),
            "yaml": clean.strip(),
            "def": slide_def,
        })

    return slides


def generate_readme(yaml_path, proof_dir, output_path):
    """Generate the README.md from showcase data."""
    slides = extract_slide_yaml(yaml_path)
    proof_dir_rel = os.path.basename(proof_dir)

    # Map layout names to slide numbers
    layout_to_slide = {}
    for i, slide in enumerate(slides):
        layout = slide["layout"]
        if layout not in layout_to_slide:
            layout_to_slide[layout] = i + 1

    lines = []

    # ─── HERO ───────────────────────────────────────────────────────────
    lines.append("<div align=\"center\">")
    lines.append("")
    lines.append("# Deck Builder")
    lines.append("")
    lines.append("**YAML-driven presentation pipeline that generates branded PowerPoint decks**")
    lines.append("")
    lines.append("Define slides in YAML. Get a pixel-perfect, brand-compliant PPTX with automated quality checks.")
    lines.append("")
    lines.append("</div>")
    lines.append("")

    # Hero visual grid — 6 diverse slides in a 3x2 table
    lines.append("<table>")
    for row_idx in range(0, len(HERO_SLIDES), 3):
        row_items = HERO_SLIDES[row_idx:row_idx + 3]
        lines.append("<tr>")
        for layout_name, label in row_items:
            slide_num = layout_to_slide.get(layout_name)
            if slide_num is not None:
                png = f"{proof_dir_rel}/slide-{slide_num:02d}.png"
                lines.append(f'<td width="33%"><img src="{png}" alt="{label}"><br><sub><b>{label}</b></sub></td>')
        lines.append("</tr>")
    lines.append("</table>")
    lines.append("")

    # ─── FEATURE HIGHLIGHTS ─────────────────────────────────────────────
    lines.append("---")
    lines.append("")
    lines.append("### Highlights")
    lines.append("")
    lines.append("| | |")
    lines.append("|---|---|")
    lines.append("| **22 Slide Layouts** | Structural, content, data, and feature slides covering every presentation need |")
    lines.append("| **148 Branded Icons** | Semantic icon library in pink and light-pink variants with 1-second recognition rule |")
    lines.append("| **Automated QA** | 12 checks across structural, visual, and AI-powered categories run on every build |")
    lines.append("| **Audience Calibration** | 5 audience profiles (C-suite to IC) with density limits, headline rules, and layout guidance |")
    lines.append("| **Storytelling Frameworks** | Minto Pyramid, SCR, and Duarte patterns built into the design system |")
    lines.append("| **Diagram Pipeline** | Native PPTX shapes, draw.io export, and AI-generated visuals (Imagen 4 + Gemini) |")
    lines.append("| **Markdown in Slides** | `**bold**`, `- bullets`, and `[links](url)` rendered as real PPTX formatting |")
    lines.append("| **Corpus-Validated** | Rules validated against 52 real brand presentations (921 slides) |")
    lines.append("")

    # ─── QUICK START ────────────────────────────────────────────────────
    lines.append("## Quick Start")
    lines.append("")
    lines.append("```bash")
    lines.append("# Set up Python environment")
    lines.append("python3 -m venv /tmp/xlsx-venv")
    lines.append("/tmp/xlsx-venv/bin/pip install python-pptx pyyaml Pillow openpyxl python-docx")
    lines.append("")
    lines.append("# Build a deck from YAML")
    lines.append("/tmp/xlsx-venv/bin/python3 test_deck.py my-deck.yaml --proof-images")
    lines.append("")
    lines.append("# Build + upload to Google Drive")
    lines.append("/tmp/xlsx-venv/bin/python3 test_deck.py my-deck.yaml --proof-images --upload")
    lines.append("")
    lines.append("# Build + Claude vision review (requires ANTHROPIC_API_KEY)")
    lines.append("/tmp/xlsx-venv/bin/python3 test_deck.py my-deck.yaml --proof-images --ai-review")
    lines.append("```")
    lines.append("")
    lines.append("A minimal deck definition:")
    lines.append("")
    lines.append("```yaml")
    lines.append("meta:")
    lines.append("  title: Quarterly Update")
    lines.append("  date: 2026-03-30")
    lines.append("  purpose: mixed")
    lines.append("")
    lines.append("slides:")
    lines.append("  - layout: title_cover")
    lines.append("    headline: Quarterly Update -- Engineering")
    lines.append("    subheader: brand | Q1 2026")
    lines.append("    background: p12")
    lines.append("")
    lines.append("  - layout: big_stat_manual")
    lines.append("    headline: Team Growth")
    lines.append("    number: \"42\"")
    lines.append("    label: Engineers shipped code this quarter")
    lines.append("    icon: team-network")
    lines.append("")
    lines.append("  - layout: closing")
    lines.append("    headline: Questions?")
    lines.append("    background: p12")
    lines.append("```")
    lines.append("")

    # ─── HOW IT WORKS ───────────────────────────────────────────────────
    lines.append("## How It Works")
    lines.append("")
    lines.append("```")
    lines.append("                    ┌─────────────────┐")
    lines.append("                    │   YAML Deck      │")
    lines.append("                    │   Definition      │")
    lines.append("                    └────────┬──────────┘")
    lines.append("                             │")
    lines.append("              ┌──────────────┼──────────────┐")
    lines.append("              ▼              ▼              ▼")
    lines.append("     ┌────────────┐  ┌────────────┐  ┌────────────┐")
    lines.append("     │ 22 Layout  │  │  148 Icon  │  │  Diagram   │")
    lines.append("     │ Renderers  │  │  Library   │  │  Engine    │")
    lines.append("     └──────┬─────┘  └──────┬─────┘  └──────┬─────┘")
    lines.append("            └───────────┬────┘───────────────┘")
    lines.append("                        ▼")
    lines.append("              ┌─────────────────┐")
    lines.append("              │  Branded PPTX   │")
    lines.append("              │  (10\" x 5.62\")  │")
    lines.append("              └────────┬────────┘")
    lines.append("                       │")
    lines.append("            ┌──────────┼──────────┐")
    lines.append("            ▼          ▼          ▼")
    lines.append("     ┌───────────┐ ┌────────┐ ┌──────────┐")
    lines.append("     │ 12 QA     │ │ Proof  │ │ Claude   │")
    lines.append("     │ Checks    │ │ PNGs   │ │ Vision   │")
    lines.append("     └───────────┘ └────────┘ └──────────┘")
    lines.append("```")
    lines.append("")
    lines.append("**1. Design** -- Read [presentation-principles.md](presentation-principles.md) to choose an audience profile, storytelling framework, and headline style.")
    lines.append("")
    lines.append("**2. Author** -- Write YAML per [presentation-guide.md](presentation-guide.md). Select from 22 layouts, respect [content limits](layout-limits.json), use assertion headlines for strategic decks.")
    lines.append("")
    lines.append("**3. Build** -- Run `test_deck.py --proof-images`. The pipeline builds the PPTX, runs 12 QA checks, generates proof PNGs, and optionally uploads to Google Drive.")
    lines.append("")

    # ─── LAYOUT GALLERY ─────────────────────────────────────────────────
    lines.append("## Layout Gallery")
    lines.append("")
    lines.append("All 22 layouts rendered with real brand data from the cloud infrastructure modernization program.")
    lines.append("Each layout is manually rendered on a clean canvas for pixel-perfect control.")
    lines.append("")
    lines.append("Full YAML field reference: [presentation-guide.md](presentation-guide.md) -- Content limits: [layout-limits.json](layout-limits.json)")
    lines.append("")

    for category in CATEGORY_ORDER:
        cat_label = CATEGORY_LABELS[category]
        cat_desc = CATEGORY_DESCRIPTIONS[category]
        lines.append(f"### {cat_label}")
        lines.append("")
        lines.append(f"*{cat_desc}*")
        lines.append("")

        for layout_name, meta in LAYOUT_META.items():
            if meta["category"] != category:
                continue

            slide_num = layout_to_slide.get(layout_name)
            if slide_num is None:
                continue

            display_name = meta["display"]
            description = meta["description"]
            png_name = f"slide-{slide_num:02d}.png"

            lines.append(f"#### `{layout_name}` -- {display_name}")
            lines.append("")
            lines.append(description)
            lines.append("")
            lines.append(f"![{display_name}]({proof_dir_rel}/{png_name})")
            lines.append("")

            # Collapsible YAML
            for slide in slides:
                if slide["layout"] == layout_name:
                    lines.append("<details>")
                    lines.append("<summary>YAML</summary>")
                    lines.append("")
                    lines.append("```yaml")
                    lines.append(slide["yaml"])
                    lines.append("```")
                    lines.append("")
                    lines.append("</details>")
                    lines.append("")
                    break

    # ─── AUDIENCE-CALIBRATED DESIGN ─────────────────────────────────────
    lines.append("---")
    lines.append("")
    lines.append("## Audience-Calibrated Design")
    lines.append("")
    lines.append("The same topic adapts to the room. A cloud migration slide for four audiences:")
    lines.append("")
    lines.append("| Audience | Layout | Headline | Density |")
    lines.append("|----------|--------|----------|---------|")
    lines.append("| **C-Suite** | `callout` | \"We should invest $2M to exit all data centers by EOY 2026\" | 30 words |")
    lines.append("| **Customer** | `before_after` | \"Your parking infrastructure moves to cloud with zero downtime\" | 50 words |")
    lines.append("| **Manager** | `roadmap` | \"Migration executes in 3 waves -- partner onboards April 15\" | 80 words |")
    lines.append("| **IC / Engineer** | `content_table` | \"VM migration path by hypervisor type and target compute service\" | 120 words |")
    lines.append("")
    lines.append("The pattern: **C-Suite** gets the decision. **Customer** gets their benefit. **Manager** gets who-does-what-by-when. **IC** gets the technical truth.")
    lines.append("")
    lines.append("Three complete decks demonstrate this in practice:")
    lines.append("")
    lines.append("| Deck | Slides | Style |")
    lines.append("|------|--------|-------|")
    lines.append("| [Showcase](showcase-deck.yaml) | 19 | Topic labels (demo of all layouts) |")
    lines.append("| [C-Suite](cloud-migration-csuite-deck.yaml) | 10 | Assertion headlines, Minto Pyramid |")
    lines.append("| [Management](cloud-migration-mgmt-deck.yaml) | 18 | Action headlines with dates |")
    lines.append("")
    lines.append("Full side-by-side analysis: [audience-comparison.md](audience-comparison.md)")
    lines.append("")

    # ─── DESIGN PRINCIPLES ──────────────────────────────────────────────
    lines.append("## Design Principles")
    lines.append("")
    lines.append("Distilled from [2,380 lines of research](research/) and a [52-deck corpus analysis](research/corpus-analysis.md):")
    lines.append("")
    lines.append("| Principle | Rule |")
    lines.append("|-----------|------|")
    lines.append("| **One idea per slide** | The headline IS the takeaway -- an assertion, not a topic label |")
    lines.append("| **Deck purpose drives headlines** | Strategic decks: assertions. Operational: labels. Set `purpose:` in YAML |")
    lines.append("| **Icon 1-second test** | Can the audience identify the icon in 1 second without text? If no, remove it |")
    lines.append("| **Bold budget: 3-5 per slide** | Bold key numbers, decisions, names. If everything is bold, nothing stands out |")
    lines.append("| **Split, don't shrink** | Two clear slides beat one crammed slide |")
    lines.append("| **Lead with the answer** | Minto Pyramid: recommendation on slide 2, evidence after |")
    lines.append("")
    lines.append("Full principles with examples: [presentation-principles.md](presentation-principles.md)")
    lines.append("")

    # ─── DESIGN SYSTEM ──────────────────────────────────────────────────
    lines.append("## Design System")
    lines.append("")
    lines.append("| Token | Value |")
    lines.append("|-------|-------|")
    lines.append("| Heading font | Urbanist ExtraBold |")
    lines.append("| Body font | DM Sans |")
    lines.append("| Primary purple | `#5F016F` |")
    lines.append("| Primary pink | `#FF80D4` |")
    lines.append("| Light pink | `#FFADE4` |")
    lines.append("| Light background | `#F0E8F5` |")
    lines.append("| Canvas | 10\" x 5.625\" (16:9) |")
    lines.append("| Icons | 148 semantic icons (pink + light-pink variants) |")
    lines.append("")

    # ─── QA PIPELINE ────────────────────────────────────────────────────
    lines.append("## QA Pipeline")
    lines.append("")
    lines.append("Every build runs 12 automated checks before delivery:")
    lines.append("")
    lines.append("| Category | Checks |")
    lines.append("|----------|--------|")
    lines.append("| **Structural** | Word count limits, font size floor (7pt), text overflow detection, cross-slide consistency, containment, empty text boxes, table font sizing, table centering, unhyperlinked URLs |")
    lines.append("| **YAML** | Content field limits per layout, icon name resolution against catalog |")
    lines.append("| **Visual** | Element overlap detection (0.02\" threshold), margin violations (0.5\"), group containment |")
    lines.append("| **AI** | Claude vision review for spacing, alignment, and brand consistency *(optional)* |")
    lines.append("")
    lines.append("```bash")
    lines.append("# Standard build with all structural + visual checks")
    lines.append("/tmp/xlsx-venv/bin/python3 test_deck.py deck.yaml --proof-images")
    lines.append("")
    lines.append("# Add Claude vision review")
    lines.append("/tmp/xlsx-venv/bin/python3 test_deck.py deck.yaml --proof-images --ai-review")
    lines.append("")
    lines.append("# Strict mode -- block upload on critical issues")
    lines.append("/tmp/xlsx-venv/bin/python3 test_deck.py deck.yaml --proof-images --strict --upload")
    lines.append("```")
    lines.append("")

    # ─── DIAGRAM PIPELINE ───────────────────────────────────────────────
    lines.append("## Diagram Pipeline")
    lines.append("")
    lines.append("Three rendering approaches for inline diagrams, selected per slide:")
    lines.append("")
    lines.append("| Approach | Engine | Best For |")
    lines.append("|----------|--------|----------|")
    lines.append("| **Native** | PPTX shapes | Org charts, flows, comparisons, timelines (7 types, 10 style palettes) |")
    lines.append("| **draw.io** | XML + CLI export | Complex architecture diagrams, network topologies |")
    lines.append("| **AI** | Imagen 4 + Gemini review | Conceptual illustrations, custom visuals (auto-retry with refinement) |")
    lines.append("")

    # ─── DOCUMENTATION ──────────────────────────────────────────────────
    lines.append("---")
    lines.append("")
    lines.append("## Documentation")
    lines.append("")
    lines.append("### For deck authors")
    lines.append("")
    lines.append("| Document | Description |")
    lines.append("|----------|-------------|")
    lines.append("| [presentation-principles.md](presentation-principles.md) | **Start here** -- audience profiles, storytelling frameworks, density rules |")
    lines.append("| [presentation-guide.md](presentation-guide.md) | YAML field reference for all 22 layouts, icon catalog, design tokens, build commands |")
    lines.append("| [deck-templates.md](deck-templates.md) | Starter YAML skeletons for executive, technical, and status decks |")
    lines.append("| [audience-comparison.md](audience-comparison.md) | Same topic adapted for C-suite vs management -- principles in action |")
    lines.append("")
    lines.append("### Research")
    lines.append("")
    lines.append("| Document | Content |")
    lines.append("|----------|---------|")
    lines.append("| [research/visual-design.md](research/visual-design.md) | 53 rules on icons, images, whitespace, and cognitive load |")
    lines.append("| [research/typography-emphasis.md](research/typography-emphasis.md) | 80 rules on bold, italics, color emphasis, and font hierarchy |")
    lines.append("| [research/audience-profiles.md](research/audience-profiles.md) | 5 audience profiles with layout matrices and density tables |")
    lines.append("| [research/storytelling-frameworks.md](research/storytelling-frameworks.md) | Minto Pyramid, SCR, Duarte, McKinsey patterns |")
    lines.append("| [research/corpus-analysis.md](research/corpus-analysis.md) | Analysis of 52 real brand presentations (921 slides) |")
    lines.append("")
    lines.append("### For developers")
    lines.append("")
    lines.append("| Document | Content |")
    lines.append("|----------|---------|")
    lines.append("| [CLAUDE.md](CLAUDE.md) | Codebase architecture, rendering pipeline, how to add layouts |")
    lines.append("| [SYSTEM-PLAN.md](SYSTEM-PLAN.md) | Build plan, layer architecture, progress tracking |")
    lines.append("")

    # ─── BUILD PIPELINE ─────────────────────────────────────────────────
    lines.append("## Project Structure")
    lines.append("")
    lines.append("```")
    lines.append("deck-builder/")
    lines.append("├── build_deck.py            # Core YAML-to-PPTX builder (22 layout renderers)")
    lines.append("├── test_deck.py             # Build harness + proof report + QA + upload")
    lines.append("├── qa_pipeline.py           # 12-check QA orchestrator")
    lines.append("├── proof_renderer.py        # PIL-based proof PNG generator")
    lines.append("├── curated-layouts.json     # Layout definitions and placeholder mappings")
    lines.append("├── layout-limits.json       # Per-layout content limits (machine-readable)")
    lines.append("├── icons/                   # 148 branded icons (pink + lightpink PNGs)")
    lines.append("│   └── icon-catalog.json    # Semantic icon names and categories")
    lines.append("├── title-assets/            # Background images for title/agenda/closing")
    lines.append("├── diagrams/                # Diagram engine (native, draw.io, AI)")
    lines.append("├── research/                # 2,380 lines of design research")
    lines.append("├── analysis/                # 52-deck corpus analysis and metrics")
    lines.append("└── showcase-deck.yaml       # All 22 layouts with real brand data")
    lines.append("```")
    lines.append("")

    with open(output_path, "w") as f:
        f.write("\n".join(lines))

    print(f"Generated: {output_path}")
    print(f"  Layouts documented: {len(layout_to_slide)}")


def ensure_showcase_current(script_dir, yaml_path, proof_dir):
    """Rebuild showcase PPTX and proof images if sources are newer."""
    import subprocess

    pptx_path = yaml_path.replace(".yaml", ".pptx")
    yaml_mtime = os.path.getmtime(yaml_path)

    # Check if PPTX needs rebuilding (YAML newer than PPTX)
    needs_build = not os.path.exists(pptx_path)
    if not needs_build:
        needs_build = yaml_mtime > os.path.getmtime(pptx_path)

    # Check if proof images need regenerating
    needs_proof = needs_build or not os.path.exists(proof_dir)
    if not needs_proof and os.path.exists(pptx_path):
        pptx_mtime = os.path.getmtime(pptx_path)
        proof_files = [f for f in os.listdir(proof_dir) if f.endswith(".png")] if os.path.exists(proof_dir) else []
        if proof_files:
            oldest_proof = min(os.path.getmtime(os.path.join(proof_dir, f)) for f in proof_files)
            needs_proof = pptx_mtime > oldest_proof
        else:
            needs_proof = True

    # Also check if source scripts are newer than outputs
    for src in ["build_deck.py", "proof_renderer.py"]:
        src_path = os.path.join(script_dir, src)
        if os.path.exists(src_path):
            src_mtime = os.path.getmtime(src_path)
            if os.path.exists(pptx_path) and src_mtime > os.path.getmtime(pptx_path):
                needs_build = True
                needs_proof = True
            if not needs_proof and os.path.exists(proof_dir):
                proof_files = [f for f in os.listdir(proof_dir) if f.endswith(".png")]
                if proof_files:
                    oldest_proof = min(os.path.getmtime(os.path.join(proof_dir, f)) for f in proof_files)
                    if src_mtime > oldest_proof:
                        needs_proof = True

    if needs_build:
        print("  Rebuilding showcase PPTX (source files changed)...")
        result = subprocess.run(
            [sys.executable, os.path.join(script_dir, "build_deck.py"),
             yaml_path, "--output", pptx_path],
            capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  WARNING: Build failed: {result.stderr[-200:]}")
            return False
        print("  PPTX rebuilt.")

    if needs_proof:
        print("  Regenerating proof images...")
        result = subprocess.run(
            [sys.executable, os.path.join(script_dir, "proof_renderer.py"),
             pptx_path, "--output-dir", proof_dir],
            capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  WARNING: Proof rendering failed: {result.stderr[-200:]}")
            return False
        print("  Proof images regenerated.")

    if not needs_build and not needs_proof:
        print("  Showcase is current (no rebuild needed).")

    return True


def main():
    parser = argparse.ArgumentParser(description="Generate README from showcase deck")
    parser.add_argument("--yaml", default="showcase-deck.yaml",
                        help="Showcase deck YAML file")
    parser.add_argument("--proof-dir", default="showcase-deck-proof",
                        help="Directory with proof PNG images")
    parser.add_argument("--output", default="README.md",
                        help="Output README path")
    parser.add_argument("--no-rebuild", action="store_true",
                        help="Skip auto-rebuild of showcase deck")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_path = os.path.join(script_dir, args.yaml)
    proof_dir = os.path.join(script_dir, args.proof_dir)
    output_path = os.path.join(script_dir, args.output)

    if not os.path.exists(yaml_path):
        print(f"ERROR: YAML not found: {yaml_path}")
        sys.exit(1)

    # Auto-rebuild showcase if sources changed
    if not args.no_rebuild:
        ensure_showcase_current(script_dir, yaml_path, proof_dir)

    if not os.path.exists(proof_dir):
        print(f"ERROR: Proof directory not found: {proof_dir}")
        print("Run: python3 test_deck.py showcase-deck.yaml --proof-images")
        sys.exit(1)

    generate_readme(yaml_path, proof_dir, output_path)


if __name__ == "__main__":
    import sys
    main()
