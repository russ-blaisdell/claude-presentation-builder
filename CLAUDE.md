# deck-builder — Codebase Guide

YAML-driven presentation pipeline that generates branded PowerPoint decks. All slides are rendered manually on a clean canvas for full layout control.

**To build a presentation**, start with `presentation-principles.md` (audience, framework, rules), then use `presentation-guide.md` (layouts, YAML syntax, icons, build commands).

**This file** covers the codebase internals for working on the builder itself.

## Documentation Map

| Document | Audience | Content |
|----------|----------|---------|
| [README.md](README.md) | Everyone | Visual overview, audience examples, screenshots of all 47 layouts |
| [presentation-principles.md](presentation-principles.md) | Deck authors / skill | Audience profiles, storytelling frameworks, icon/typography rules, density limits |
| [presentation-guide.md](presentation-guide.md) | Deck authors / skill | YAML field reference, 148 icons, design tokens, content limits, build commands |
| [layout-selection-guide.md](layout-selection-guide.md) | Deck authors / skill | Decision tree for choosing layouts, audience rules, sequencing patterns, measured capacity |
| [audience-presets.json](audience-presets.json) | Deck authors / skill | c-suite/manager/ic density presets with preferred layouts and headline guidance |
| [deck-templates.md](deck-templates.md) | Deck authors | Starter YAML skeletons (executive, technical, status) |
| [layout-limits.json](layout-limits.json) | QA pipeline / skill | Machine-readable max content per field per layout |
| [CLAUDE.md](CLAUDE.md) (this file) | Developers | Codebase architecture, rendering pipeline, how to add layouts |
| [SYSTEM-PLAN.md](SYSTEM-PLAN.md) | Developers | Build plan, layer architecture, progress tracking |
| [research/visual-design.md](research/visual-design.md) | Reference | 53 rules: icons, images, whitespace, cognitive load |
| [research/typography-emphasis.md](research/typography-emphasis.md) | Reference | 80 rules: bold, italics, color, font hierarchy |
| [research/audience-profiles.md](research/audience-profiles.md) | Reference | 5 audience profiles with layout matrices and examples |
| [research/storytelling-frameworks.md](research/storytelling-frameworks.md) | Reference | Minto, SCR, Duarte, McKinsey, 6 slide sequences |
| [research/corpus-analysis.md](research/corpus-analysis.md) | Reference | 52-deck analysis: density, typography, headlines, brand patterns |
| [research/layout-patterns-research.md](research/layout-patterns-research.md) | Reference | 53 layout patterns from 30+ sources, gap analysis, top 10 new layouts to add |
| [analysis/corpus-analysis-report.md](analysis/corpus-analysis-report.md) | Reference | Full findings with principles alignment and recommendations |
| [competitive-edge.md](competitive-edge.md) | Strategy | 9 differentiators, scoring rubric, contest demo strategy, roadmap to first prize |

## Architecture

### Build Pipeline

| File | Purpose |
|------|---------|
| `build_deck.py` | Core builder — parses YAML, renders 47 layout types on `content_generic` canvas |
| `test_deck.py` | Build harness — runs builder, proof report, QA pipeline, upload |
| `qa_pipeline.py` | Unified QA orchestrator — content limits, structural checks, visual proof, Claude vision |
| `proof_renderer.py` | PIL-based proof renderer — full-size PNGs with alignment/text rendering |
| `curated-layouts.json` | Layout definitions and placeholder mappings |

### Testing

| File | Purpose |
|------|---------|
| `test-layouts.py` | Generates 500 test slides (25 variations per layout) |
| `run-layout-tests.py` | End-to-end test runner with blank detection and pass/fail reporting |
| `build-layout-limits.py` | Computes layout-limits.json from estimate_text_height() math |

### Diagram Engine

| File | Purpose |
|------|---------|
| `diagrams/engine.py` | Diagram dispatcher — routes to native, draw.io, or AI renderers |
| `diagrams/native_renderer.py` | PPTX-native diagrams (7 types, 10 style palettes) |
| `diagrams/drawio_renderer.py` | draw.io XML generation + CLI export |
| `diagrams/ai_renderer.py` | Google Imagen 4 + Gemini review loop |

### Corpus Analysis

| File | Purpose |
|------|---------|
| `analyze-corpus.py` | PPTX corpus scanner — `--manifest` mode for inventory, `--analyze` for metric extraction |
| `analysis/corpus-manifest.json` | 56 company PPTX files cataloged with generation, canvas size, brand font detection |
| `analysis/corpus-metrics.json` | Per-slide metrics (word count, fonts, colors, density) for all 921 slides |
| `analysis/corpus-analysis-report.md` | Findings report with principles alignment ratings and recommendations |
| `analysis/corpus/` | 25 PPTX files downloaded from Google Drive (all-hands, steering, product reviews, etc.) |

### Showcase & README

| File | Purpose |
|------|---------|
| `examples/showcase-*.yaml` | 10-slide showcase per brand — "Project Horizon" developer platform story |
| `generate-readme.py` | Builds README.md from showcase YAML + proof images |
| `showcase-deck-proof/` | 19 proof PNGs used as README screenshots |

## How the Builder Works

### Slide rendering pipeline

1. `build_deck()` in `build_deck.py` loads the YAML definition and the brand's PPTX template
2. For each slide, `build_slide()` resolves the layout name (checking `LAYOUT_ALIASES`), looks it up in `curated-layouts.json`, and adds a slide from the matching template layout
3. For manually-rendered layouts (all 47 custom layouts), the placeholder-based slide is immediately swapped for a clean `content_generic` canvas (layout index 2)
4. The corresponding `_build_*()` function renders all content as manual shapes using `slide.shapes.add_textbox()`, `add_picture()`, `add_shape()`, etc.
5. Footers are set via `_set_footers()` — title centered on left half, date centered on right half

### Adding a new layout

1. Add the layout name to the routing `elif` block in `build_slide()` (~line 412)
2. Write a `_build_<name>(slide, slide_def, deck_meta)` function following existing patterns
3. Add the layout to `curated-layouts.json` with `layout_idx: 2` (content_generic) and the standard footer placeholders
4. All positioning uses `Inches()` coordinates on the 10" x 5.625" canvas
5. Use `estimate_text_height()` for all text box sizing — never hardcode heights
6. Vertically center content between `avail_top=0.85` and `avail_bottom=5.0`

### Key constants and helpers

| Function/Constant | Location | Purpose |
|-------------------|----------|---------|
| `estimate_text_height()` | line ~191 | Calculates rendered text height from text + width + font size |
| `_resolve_icon()` | line ~1131 | Resolves icon name to file path via `icon-catalog.json` |
| `_set_footers()` | line ~515 | Repositions footer placeholders to proper centering |
| `_split_title()` | line ~553 | Splits title at dash separators, drops the separator |
| `_calc_split()` | line ~834 | Auto-bumps split ratios toward text if content doesn't fit |
| `_render_text_hierarchical()` | line ~766 | Renders primary/secondary/tertiary text levels |
| `add_text_box()` | line ~210 | Convenience wrapper for manual text box creation |
| `LAYOUT_ALIASES` | line ~59 | Maps old layout names to current names |
| `FIELD_ALIASES` | line ~46 | Maps YAML field names to catalog names |
| `SPLIT_RATIOS` | line ~71 | Predefined split fractions for diagram+text layouts |
| `TYPO_HIERARCHY` | line ~83 | Font sizes by typography level (primary/secondary/tertiary) |
| `_render_body_text()` | line ~300 | Renders multi-line body text with bullet, bold, and link support |
| `_add_run_with_hyperlinks()` | line ~239 | Adds text with auto-detected URLs and `[text](url)` markdown links |
| `_set_hyperlink_on_run()` | line ~225 | Sets OOXML hyperlink on a text run |

### Design tokens (used in all builders)

| Token | Python | Value |
|-------|--------|-------|
| Primary | `brand.primary` | Brand-dependent (generic: `#1A365D`) |
| Secondary | `brand.secondary` | Brand-dependent (generic: `#3182CE`) |
| Accent | `brand.accent` | Brand-dependent (generic: `#63B3ED`) |
| Light bg | `brand.bg_light` | Brand-dependent (generic: `#EBF4FF`) |
| Dark text | `brand.text_dark` | Brand-dependent (generic: `#2D3748`) |
| Heading font | `brand.heading_font` | Brand-dependent (generic: `Arial`) |
| Body font | `brand.body_font` | Brand-dependent (generic: `Arial`) |
| Canvas | `content_generic` layout index 2 | 10" x 5.625" |

## Key Rules for Development

- **All slides render manually** on `content_generic` — never rely on template placeholder positions for content layout
- **Use `estimate_text_height()`** for all manual text boxes — never hardcode heights
- **Generate 2-3 variants** per content slide that includes graphics
- **Title text splitting:** Auto-split at ` — `, ` – `, ` - ` separators; drop the separator; max 2 lines; white line 1, pink line 2
- **Footers:** Title left-half centered, date right-half centered, single-line, no-wrap
- **Typography hierarchy:** Primary (12pt bold), Secondary (10pt), Tertiary (8pt) — adaptive sizing reduces in steps if content overflows
- **Split ratios:** `v-70/30`, `v-50/50`, `v-30/70`, `h-60/40`, `h-50/50`, `h-40/60` — auto-bumps toward text if content doesn't fit
- **QA before delivery:** Always run with `--proof-images` to check overlaps, margins, and containment
- **Use `fit_font_size()`** for text inside constrained shapes (circles, chevrons, narrow bars) — prevents word wrapping
- **Brand colors:** Extract `brand = deck_meta.get("brand", BrandConfig())` at the start of each builder. Use `brand.primary`, `brand.secondary`, etc. — never hardcode `RGBColor` values
- **Layout notes:** Each builder gets a `[Layout choice]` note via `_generate_layout_note()` explaining why it was selected
- **Audience presets:** Deck YAML `audience: c-suite|manager|ic` controls density limits validated by `check_audience_density()`
- **Hifi proofs:** Use `--hifi` for LibreOffice pixel-perfect screenshots (README, demos). Use `--proof-images` for fast QA iteration.

## QA Pipeline Internals

`qa_pipeline.py` orchestrates all checks via the `QAPipeline` class:

**Structural checks** (operate on PPTX object model, no rendering):
- `check_word_count()` — per-textbox word counting, exempt tables and footers
- `check_font_sizes()` — walks all runs, checks against 7pt floor / 9pt warn threshold
- `check_text_overflow()` — compares `estimate_text_height()` output to actual shape height
- `check_consistency()` — cross-slide font families, headline sizes, footer presence
- `check_story_structure()` — validates slide sequence (title_cover first, closing last, context before data)
- `check_audience_density()` — validates against audience presets (slide count, layout choices, headline style)
- `auto_fix_pptx()` — re-centers tables, upsizes fonts when space allows, adds hyperlinks to bare URLs
- `check_containment()` — filled rectangles as containers, text boxes inside them
- `check_empty_text_boxes()` — detects visible empty text boxes/placeholders (skips filled shapes and small cards)
- `check_table_font_opportunity()` — flags tables where row height could support a larger font than currently used
- `check_table_centering()` — flags tables not vertically centered when space allows
- `check_unhyperlinked_urls()` — detects URL text that isn't wrapped in a clickable hyperlink

**YAML checks** (require yaml_path):
- `check_yaml_content_limits()` — validates YAML field content against per-layout limits
- `check_yaml_icon_resolution()` — verifies every icon name in YAML exists in the catalog with a valid PNG file

**Visual checks** (generate proof PNGs via `proof_renderer.py`):
- Overlap detection between text elements (0.02" threshold)
- Margin violations (0.5" from slide edge)
- Group containment (child shapes inside parent groups)
- Red outline annotations on flagged elements

**Vision review** (optional, calls Anthropic API):
- Sends each slide PNG to Claude Sonnet with a structured evaluation prompt
- Returns JSON issues with category, severity, description
- Falls back gracefully if API is unavailable

**Output:** `<deck>-qa-report.json` + `<deck>-qa-report.md` with per-slide pass/warn/fail

## Diagram Pipeline Internals

`diagrams/engine.py` dispatches to three renderers:

| Renderer | Output | Diagram types |
|----------|--------|---------------|
| `native_renderer.py` | PPTX shapes (callable) | org-hierarchy, flow, comparison, timeline, key-stats, labeled-boxes, process-steps |
| `drawio_renderer.py` | PNG (via draw.io CLI) | org-hierarchy, flow, architecture, timeline, labeled-boxes, process-steps |
| `ai_renderer.py` | PNG (Imagen 4 + Gemini) | All types + conceptual, data-visual |

**Style system:** 10 palettes (corporate, tech-gradient, blueprint, etc.) map role-based colors (root_fill, child_fill, connector, accent, bg) applied across all renderers.

**AI pipeline:** Imagen 4 generates → Gemini 2.5 Flash reviews (text presence, structure accuracy) → auto-retry with refined prompt (max 3 attempts) → fallback to native if all fail.

## Refreshing the README

```bash
# Rebuild showcase and regenerate
/tmp/xlsx-venv/bin/python3 test_deck.py showcase-deck.yaml --proof-images
/tmp/xlsx-venv/bin/python3 generate-readme.py
```

## Related Files

- **Presentation principles:** `presentation-principles.md` — audience profiles, storytelling frameworks, icon/typography rules
- **Presentation guide:** `presentation-guide.md` — the reference for building decks (layouts, icons, YAML syntax)
- **Research:** `research/` — deep research backing the principles (visual design, typography, audiences, frameworks)
- **Build plan:** `SYSTEM-PLAN.md` — architecture, progress tracking, and build order
- **Deck templates:** `deck-templates.md` — starter YAML skeletons
- **Brand templates:** `brands/*/template.pptx` — each brand's PPTX template with baked theme
- **Skill:** `~/.claude/skills/create-presentation/SKILL.md` — end-to-end research + deck creation workflow
