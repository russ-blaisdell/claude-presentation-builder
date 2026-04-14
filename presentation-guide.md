# Presentation Guide

Complete reference for building branded PowerPoint decks using the brand YAML deck builder. Read this before writing any deck YAML.

**Read first:** [Presentation Principles](presentation-principles.md) (audience profiles, storytelling frameworks, design rules)

**Related docs:** [README](README.md) | [Deck Templates](deck-templates.md) | [Content Limits](layout-limits.json) | [Codebase Guide](CLAUDE.md)

## Quick Start

```bash
# Ensure Python venv exists
python3 -m venv /tmp/xlsx-venv && /tmp/xlsx-venv/bin/pip install python-pptx pyyaml Pillow openpyxl python-docx

# Build a deck from YAML with proof images
/tmp/xlsx-venv/bin/python3 test_deck.py <definition.yaml> --proof-images

# Build with upload to Google Drive
/tmp/xlsx-venv/bin/python3 test_deck.py <definition.yaml> --proof-images --upload

# Build with Claude vision review
/tmp/xlsx-venv/bin/python3 test_deck.py <definition.yaml> --proof-images --ai-review

# Strict mode — blocks upload on critical QA issues
/tmp/xlsx-venv/bin/python3 test_deck.py <definition.yaml> --proof-images --strict --upload
```

The `--proof-images` flag generates PNG previews per slide with overlap/margin annotations. The `--upload` flag uploads to Google Drive and converts to Google Slides.

## YAML Deck Structure

```yaml
title: "Presentation Title"
date: "2026-03-28"
style: "corporate"           # visual style for diagrams (see Style System)
diagram_variants: 1           # variants per diagram slide: 1, 3, 6, 9, 12+

slides:
  - layout: title_cover
    headline: "Title — Subtitle"
    subheader: "Platform Engineering | Context Line"
    background: "p12"
    notes: "Speaker notes go here"

  - layout: agenda
    items:
      - "First Topic"
      - "Second Topic"

  # ... one entry per slide
```

**Global fields:**
- `title` — deck title (appears in footers)
- `date` — date string (appears in footers)
- `style` — default diagram style (see Style System section)
- `diagram_variants` — how many diagram variants to generate per `content_diagram_text` slide

**Per-slide fields:**
- `layout` — layout type name (see tables below)
- `headline` — slide headline (most layouts)
- `notes` — speaker notes (any layout)

---

## Text Formatting in Body Fields

Body text fields (`left_body`, `right_body`, `col1_body`, etc.) support markdown-style formatting:

### Bullets
Lines starting with `- ` render as bulleted list items with a `•` prefix:
```yaml
right_body: |
  - First item
  - Second item
  - Third item
```

### Named hyperlinks
Use `[Display Text](url)` to render clean link text with a clickable hyperlink behind it:
```yaml
right_body: |
  - [Cloud Services](wipro.com/cloud)
  - [AWS Partner Page](aws.amazon.com/partners/wipro)
  - [Case Study (PDF)](example.com/case-study.pdf)
```

Renders as purple underlined text like "Cloud Services" that links to the URL when clicked.

### Inline bold
Wrap text in `**double asterisks**` to render bold. Use for labels, key metrics, and emphasis:
```yaml
left_body: |
  **HQ:** Bezons (Paris), France
  **Employees:** 63,000. **Revenue:** EUR 8B

  **AWS Premier** (19 competencies)
  Line with **inline bold** in the middle
```

Bold can be combined with bullets:
```yaml
right_body: |
  - **Key reference:** Philips 4,200 apps
  - **Compliance:** ISO 27001 confirmed
```

### Bare URL auto-linking
URLs written as plain text (e.g. `example.com/path` or `https://example.com`) are automatically detected and converted to clickable hyperlinks. Named links are preferred for readability.

### Combining formats
All inline formats (bold, links, bullets, bare URLs) can be mixed freely in any body field:
```yaml
left_body: |
  **55,000+ servers** migrated for 60+ clients
  **First-ever Google Cloud RaMP partner**

  - [Cloud Services](wipro.com/cloud)
  - [Case study](example.com/case-study)
```

**Supported in:**
- **Bullets + bold + links:** `side_by_side`, `three_column`, `four_card`, `numbered_list` (item body), `status_board` (summary), `content_diagram_text`, `content_stacked`
- **Links only (no bullets):** `callout` (callout_text, supporting_text), `closing` (contact_info)

---

## Slide Layouts (22 total)

### Structural Slides

| Layout | YAML `layout:` | Description |
|--------|----------------|-------------|
| Title cover | `title_cover` | Background image + two-line text overlay (auto-splits at dash separators) |
| Agenda | `agenda` | Left image + numbered items + divider lines (up to 7 items) |
| Section divider | `section_divider` | Visual break — purple/light/image bg, section number, headline, icon |
| Closing | `closing` | "Questions?" with background image |

**title_cover fields:** `headline`, `subheader`, `background` (p12, p13, p17, or image path)

**agenda fields:** `headline`, `items` (list of strings), `agenda_image` (p21, p22, p23, or path)

**section_divider fields:** `section_number`, `headline`, `subheader`, `background` (purple, light, or image key), `icon`

**closing fields:** `headline` (default "Questions?"), `subheader`, `contact_info`, `background`

### Content Slides

| Layout | YAML `layout:` | Description |
|--------|----------------|-------------|
| Stacked two-section | `content_two_col` | Left stats graphic + right sections with icons + divider |
| Diagram + text | `content_diagram_text` | Split layout (v- or h- ratios) with diagram and text columns |
| Side-by-side | `side_by_side` | Two columns with icons, vertically centered |
| Three-column | `three_column` | Headline + 3 titled columns with icons |
| Four-card | `four_card` | Headline + 1-8 card blocks with light purple backgrounds |
| Numbered list | `numbered_list` | Large numbers + title/body per item with dividers |
| Before / After | `before_after` | Two columns with center arrow showing transformation |

**side_by_side fields:** `headline`, `left_icon`, `left_title`, `left_body`, `right_icon`, `right_title`, `right_body`

**three_column fields:** `headline`, `col1_icon`, `col1_title`, `col1_body`, `col2_icon`, `col2_title`, `col2_body`, `col3_icon`, `col3_title`, `col3_body`

**four_card fields:** `headline`, `card1_title`, `card1_body`, ... up to `card8_title`, `card8_body` (renders only cards with titles)

**numbered_list fields:** `headline`, `items` (list of `{title, body}` or plain strings)

**before_after fields:** `headline`, `before` (`{label, icon, items}`), `after` (`{label, icon, items}`), `arrow_label`

**content_two_col fields:** same as side_by_side + `left_stats` (list of `{number, label, icon}`), `variants` (1 or 3)

**content_diagram_text fields:** `headline`, `split` (v-50/50, h-60/40, etc.), `diagram` (path), `visual` (`{type, style, approaches, data}`), `left_icon`, `left_title`, `left_body`, `right_icon`, `right_title`, `right_body`

### Data Slides

| Layout | YAML `layout:` | Description |
|--------|----------------|-------------|
| Table | `content_table` | Styled table with purple header and optional row striping |
| Table + Bullets | `content_table_bullets` | Table + bullet points below with color-coded cells |
| Matrix (RACI) | `matrix` | Color-coded matrix with cell coloring and legend |
| KPI Dashboard | `kpi_dashboard` | Grid of 2-8 metric cards with numbers, trends, icons |
| Status Board | `status_board` | RAG (red/amber/green) status tracking with circles |

**content_table fields:** `headline`, `columns` (list), `rows` (list of lists), `col_widths` (proportional weights, e.g., `[30, 70]`), `col_align` (single string or per-column list: `left`/`center`/`right`), `header_bg` (hex), `header_style` (`bold` or `allcaps`), `stripe` (bool)
- Cell text supports `**bold**` and `- ` bullet prefixes
- Tables auto-split across slides when content overflows (with "(continued)" headers)
- `col_widths` are proportional weights, not inches — `[30, 70]` = 30%/70% split

**kpi_dashboard fields:** `headline`, `metrics` (list of `{number, label, trend, target, icon, highlight}`), `columns` (auto-detected)

**status_board fields:** `headline`, `items` (list of `{name, status, summary}`), `as_of`
- `status` values: `green`, `amber`, `red`

**matrix fields:** `headline`, `row_header`, `rows` (list of `{label, values}`), `columns` (list), `cell_colors` (dict mapping value to hex color), `legend`

### Feature Slides

| Layout | YAML `layout:` | Description |
|--------|----------------|-------------|
| Big stat | `big_stat_manual` | Large centered number with label and optional icon |
| Quote | `quote` | Decorative quotation mark + centered text + attribution |
| Callout | `callout` | Key takeaway — boxed (purple card) or open style |
| Roadmap | `roadmap` | Gantt-style timeline with swimlanes and milestone diamonds |
| Funnel | `funnel` | Progressively narrowing bars for pipeline visualization |
| Image showcase | `image_showcase` | Full-slide image with optional caption and border |

**big_stat_manual fields:** `headline`, `number`, `label`, `icon`

**quote fields:** `headline`, `quote_text`, `attribution`, `attribution_title`, `icon`, `style` (centered or left-aligned)

**callout fields:** `callout_text`, `supporting_text`, `icon`, `style` (boxed or open)

**roadmap fields:** `headline`, `time_axis` (list of date/period labels), `swimlanes` (list of `{name, items: [{label, start, end, status}]}`), `milestones` (list of `{date, label}`)
- `start` / `end`: string matching a `time_axis` label (e.g., `"Apr 3"`) or integer index (0-based)
- `date` (milestones): string matching a `time_axis` label
- `status` values: `complete`, `active`, `planned`
- **Proportional spacing:** If `time_axis` labels are parseable dates (e.g., `"Mar 31"`, `"Apr 14"`), columns scale proportionally to actual days between dates. Falls back to equal-width columns for non-date labels.

**funnel fields:** `headline`, `stages` (list of `{label, value, width}`) — width is 0-100 percentage

**image_showcase fields:** `headline`, `image` (path), `caption`, `border` (bool)

### Process & Flow Slides

| Layout | YAML `layout:` | Description |
|--------|----------------|-------------|
| Process flow | `process_flow` | 3-6 connected chevron or circle steps with status coloring |
| Staircase | `staircase` | Ascending maturity levels with current-level highlight |
| Cycle diagram | `cycle_diagram` | 3-6 nodes in a circle with directional arrows |
| Hub and spoke | `hub_spoke` | Central hub with radiating spoke nodes |
| Pyramid | `pyramid` | 3-5 horizontal tiers, narrow top to wide bottom |

**process_flow fields:** `headline`, `steps` (list of `{label, body, status}`), `style` (chevron or circles)
- `status` values: `complete` (filled purple), `active` (filled pink), default (outlined)
- Max 5 steps comfortable, 6 with short labels

**staircase fields:** `headline`, `levels` (list of `{label, body}`), `current_level` (1-based index)
- Max 5 levels. Current level highlighted in pink.

**cycle_diagram fields:** `headline`, `nodes` (list of `{label}` or strings), `center_label`
- Max 6 nodes. Labels must be single short words (Plan, Build, Test).

**hub_spoke fields:** `headline`, `hub` (center label string), `spokes` (list of `{label, body}`)
- Max 6 comfortable, 8 with short labels. Hub label max 15 chars.

**pyramid fields:** `headline`, `tiers` (list of `{label, body}` from top/narrowest to bottom/widest)
- Max 5 tiers. Color gradient darkest at top, lightest at bottom.

### Comparison & Analysis Slides

| Layout | YAML `layout:` | Description |
|--------|----------------|-------------|
| Comparison matrix | `comparison_matrix` | Feature evaluation with Harvey balls and checkmarks |
| Quadrant | `quadrant` | 2x2 SWOT/priority matrix with axis labels |
| Pros / Cons | `pros_cons` | Green strengths vs red risks with recommendation |
| Pricing table | `pricing_table` | 3-4 tier cards with features and highlighted plan |
| Bold bullet | `bold_bullet` | Executive summary — bold assertions + indented evidence |
| Team profiles | `team_profiles` | People cards with icon, name, role, context |

**comparison_matrix fields:** `headline`, `row_header` (label for first column), `columns` (list of option names), `highlight_column` (optional — name to accent), `rows` (list of `{label, values}`), `legend` (optional)
- `values`: `full`, `three-quarter`, `half`, `quarter`, `none`, `check`, `cross`, or short text
- Max 5 options x 8 criteria

**quadrant fields:** `headline`, `x_axis` (label), `y_axis` (label), `quadrants` (list of 4 `{position, title, color, items}`)
- `position`: `top-left`, `top-right`, `bottom-left`, `bottom-right`
- `color`: hex with # prefix (e.g., `"#4CAF50"`)
- Max 5 items per quadrant

**pros_cons fields:** `headline`, `pros_label` (default "Strengths"), `cons_label` (default "Risks"), `pros` (list of strings), `cons` (list of strings), `recommendation` (optional)
- Max 6 items per side. Recommendation renders as purple bar at bottom.

**pricing_table fields:** `headline`, `tiers` (list of `{name, price, features, highlight}`)
- `highlight`: `true` on one tier for purple accent. Max 4 tiers, 6 features each.

**bold_bullet fields:** `headline`, `points` (list of `{assertion, evidence}`)
- `assertion`: bold purple text. `evidence`: list of strings rendered as indented bullets.
- Max 4 points, 3 evidence items each.

**team_profiles fields:** `headline`, `profiles` (list of `{name, role, icon, context}`)
- `icon`: resolves from icon catalog. Falls back to initials if not found.
- 2-4 profiles: single row. 5-8: 2-row grid. Max 8.

### Chart & Data Visualization Slides

| Layout | YAML `layout:` | Description |
|--------|----------------|-------------|
| Waterfall | `waterfall` | Bridge chart — floating bars showing A→B contributions |
| Donut rings | `donut_rings` | Progress ring dashboard with percentage arcs |
| Gauge dashboard | `gauge_dashboard` | 2-4 semicircular speedometer dials |
| Tornado chart | `tornado_chart` | Horizontal sensitivity bars left/right from center |
| Radar chart | `radar_chart` | Polygon on radial axes for multi-dimension comparison |
| Combo chart | `combo_chart` | Overlaid bar chart + line with dual Y-axes |
| Bubble chart | `bubble_chart` | Scatter with variable-size circles |
| Risk heat map | `risk_heat_map` | 5x5 color grid with risk register panel |

**waterfall fields:** `headline`, `start` (`{label, value}`), `items` (list of `{label, value, type}`), `end` (`{label, value}`), `source` (optional)
- `type`: `positive` (green) or `negative` (red). Start/end bars are purple.
- Max 7 items. Labels max 12 chars.

**donut_rings fields:** `headline`, `rings` (list of `{value, label, color}`)
- `value`: 0-100 (percentage). `color`: `green`, `amber`, `red`, `purple`, `pink`, or `auto`
- `auto` color: green ≥80, amber ≥50, red <50. Max 6 rings, 4 comfortable.

**gauge_dashboard fields:** `headline`, `gauges` (list of `{value, label}`)
- `value`: 0-100. Auto-colored: green ≥75, amber ≥40, red <40. Max 4 gauges.

**tornado_chart fields:** `headline`, `items` (list of `{label, low, high}`), `center_label` (optional)
- `low`/`high`: numeric magnitude (negative values extend left). Max 7 items.

**radar_chart fields:** `headline`, `axes` (list of label strings), `series` (list of `{name, values, color}`)
- `values`: list of 0-100 per axis. Max 8 axes, 3 series.

**combo_chart fields:** `headline`, `categories` (list of x-axis labels), `bars` (`{name, values, color}`), `line` (`{name, values, color}`), `y_axis_left`, `y_axis_right`
- `values`: list of numbers matching categories length. Max 8 categories.

**bubble_chart fields:** `headline`, `x_axis` (label), `y_axis` (label), `bubbles` (list of `{label, x, y, size}`)
- `size`: relative 1-100. Labels render inside bubbles as white text. Max 5 bubbles.

**risk_heat_map fields:** `headline`, `x_axis` (default "Impact"), `y_axis` (default "Likelihood"), `items` (list of `{label, x, y, description}`)
- `x`/`y`: 1-5 grid coordinates. Risk register panel shows items with severity color-coding.

### Composite & Structural Slides

| Layout | YAML `layout:` | Description |
|--------|----------------|-------------|
| Bento grid | `bento_grid` | Mixed-size tiles with hero + supporting cards |
| Dashboard panel | `dashboard_panel` | KPI tiles + chart + summary text combined |
| Left nav sidebar | `left_nav_sidebar` | Purple nav panel with main content area |
| Image + text hero | `image_text_hero` | Image with text in configurable position |
| Venn diagram | `venn` | 2-3 overlapping translucent circles |
| Concentric circles | `concentric_circles` | TAM/SAM/SOM nested rings |

**bento_grid fields:** `headline`, `tiles` (list of `{title, body, size}`)
- `size`: `large` (hero, left 50%) or `small` (stacked right). First `large` tile gets hero treatment.

**dashboard_panel fields:** `headline`, `kpis` (list of `{number, label}`), `chart_title`, `chart_data` (list of `{label, value}`), `summary`
- KPI tiles across top, bar chart left, summary panel right. Max 4 KPIs, 6 chart bars.

**left_nav_sidebar fields:** `headline`, `nav_items` (list of `{label, active}` or strings), `content_title`, `content_body`
- `active: true` on one item shows pink indicator. Body supports markdown bullets.

**image_text_hero fields:** `headline`, `image` (path), `body`, `text_position` (`left`, `right`, or `bottom`)
- Image placeholder renders as light purple if path not found.

**venn fields:** `headline`, `circles` (list of `{label, color}`), `intersections` (list of `{regions, label}`)
- `color`: `purple`, `pink`, `light_purple`, `blue`, `green`, `amber`, `red`, `teal`
- `regions`: list of circle indices (0-based) defining the intersection area. Max 3 circles.

**concentric_circles fields:** `headline`, `rings` (list of `{label, value}` from outermost to innermost)
- Color gradient: lightest outer, darkest inner. Max 4 rings. Labels max 10 chars.

---

## Icon Library (147 icons)

Reference icons by semantic name in any `*_icon` field. The builder resolves to the correct PNG.

| Category | Icons |
|----------|-------|
| **analytics** (4) | dashboard-gauge, parking-analytics, presentation-chart, search-analytics |
| **business** (3) | briefcase, briefcase-check, briefcase-star |
| **commerce** (10) | contactless-pay, discount-sign, free-parking, mobile-payment, parking-receipt, parking-ticket, price-tag, shopping-cart, storefront, ticket |
| **communication** (4) | bell, chat-bubble, customer-support, waving-hand |
| **content** (5) | bullet-list, checklist, folder-add, parking-document, pencil |
| **energy** (4) | battery-charging, ev-charger, lightning-bolt, search-energy |
| **facilities** (7) | barriers, buildings, garage-parking, restroom, restroom-2, valet-key, wheelchair |
| **feedback** (5) | heart, sad-face, smiley-face, three-stars, thumbs-up |
| **finance** (5) | coin-stacks, coins, contactless-payment, payment-calendar, wallet |
| **ideas** (1) | lightbulb |
| **location** (6) | map-pin, navigation-arrow, push-pin, route-map, route-pin, touch-map |
| **people** (11) | add-user, add-user-2, add-user-screen, contact-card, couple, crowd-cheering, parent-child, parking-attendant, person-search, team-celebrate, team-network |
| **security** (3) | car-key, padlock, security-camera |
| **technology** (18) | barcode-scan, cloud-network, database-new, desktop-mobile, globe-orbit, led-sensor, mobile-list, mobile-notification, network-hub, no-connection, no-database, phone-refresh, qr-code, remote-control, satellite, server-stack, smartphone, touch-screen |
| **time** (7) | 24-hours, calendar-day, clock, hourglass, hourglass-2, time-rewind, time-settings |
| **tools** (3) | gear, sliders, wrench |
| **transport** (22) | bicycle-parking, bike-lane, bus, bus-2, car, car-add, car-clock, car-download, car-download-2, car-garage, car-number, connected-car, connected-car-2, no-parking, parked-car, parking-gate, parking-meter, parking-search, parking-signs, parking-verified, ship, tow-truck |
| **ui** (16) | circle-check, cursor-disabled, cursor-question, dice, download, filter-funnel, finger-snap, home, loop-arrows, merge-arrows, move-directions, question-mark, refresh-target, return-arrow, tap-touch, warning |

---

## Design Tokens

All colors and fonts come from your brand's `brand.yaml`. The table below shows the **generic** brand defaults. Your brand will have different values — check `brands/<your-brand>/brand.yaml`.

| Token | Generic Default | Brand YAML Key |
|-------|----------------|----------------|
| **Heading font** | Arial | `fonts.heading` |
| **Body font** | Arial | `fonts.body` |
| **Primary** | `#1A365D` (navy) | `colors.primary` |
| **Secondary** | `#3182CE` (blue) | `colors.secondary` |
| **Accent** | `#63B3ED` (light blue) | `colors.accent` |
| **Light Background** | `#EBF4FF` | `colors.background_light` |
| **White** | `#FFFFFF` | `colors.white` |
| **Dark text** | `#2D3748` | `colors.text_dark` |
| **Canvas** | 10" x 5.625" (16:9) | — |
| **Content safe area** | 0.35"-9.65" horizontal, 0.85"-5.0" vertical | — |

---

## Typography Rules

The builder applies these rules automatically. Understanding them helps when tuning content density.

### Paragraph Spacing

When body text doesn't fill its available vertical space, `space_after` is distributed across content paragraphs to prevent text from bunching at the top. The spacing follows established typography standards:

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| **Target space_after** | 75% of font size | Butterick's Practical Typography: 50-100% range. Nancy Duarte recommends the upper end for presentation scannability |
| **Maximum space_after** | 100% of font size | Items feel disconnected beyond this (Bringhurst, Elements of Typographic Style) |
| **Minimum space_after** | 25% of font size | Below this, paragraphs lose visual separation |

For common body text sizes:

| Font Size | Target Spacing | Maximum Spacing |
|:---------:|:--------------:|:---------------:|
| 10pt | 7.5pt | 10pt |
| 9pt | 6.75pt | 9pt |
| 8pt | 6pt | 8pt |

The builder picks the **lesser** of the calculated even distribution and the 75% target. Any remaining vertical space becomes bottom whitespace rather than stretching beyond the typographic maximum.

**Currently applied in:** `side_by_side` body text fields. Future: all layouts with body text.

### Font Size Hierarchy

| Level | Font | Size | Weight | Use |
|-------|------|:----:|--------|-----|
| Headline | Heading font | 24pt | Extra Bold | Slide headline |
| Section title | Heading font | 12-14pt | Extra Bold | Column/card titles |
| Body | Body font | 9-10pt | Regular | Main content |
| Body bold | Body font | 9-10pt | Bold | Labels, emphasis (via `**text**`) |
| Tertiary | Body font | 7-8pt | Regular | Footnotes, sources, bar labels |

Heading and body fonts are set in your brand's `brand.yaml` (`fonts.heading` and `fonts.body`).

### Line Height

The builder uses 1.3x the font size as default line height (single spacing with slight breathing room). This is not configurable per-slide — it's a global constant for consistency.

### References

- Butterick, M. *Practical Typography* — paragraph spacing: 50-100% of body text size
- Bringhurst, R. *Elements of Typographic Style* — spacing should distinguish paragraphs without losing connection
- Duarte, N. *slide:ology* — presentations need more whitespace than documents; 75-100% for scannability
- Reynolds, G. *Presentation Zen* — minimize text, maximize breathing room
- Microsoft/Google Slides defaults — ~50% of font size for bullet list spacing

---

## Deck Templates

Starter YAML skeletons for common deck types in `deck-templates.md`:
- **Executive Presentation** (10-15 slides) — strategy decisions, program kickoffs
- **Technical / Architecture** (15-20 slides) — architecture reviews, deep-dives
- **Status / Update** (8-12 slides) — program reviews, governance check-ins

Copy a skeleton, fill in your content, and build.

---

## Style System

10 visual styles for diagrams and AI-generated graphics. Set at deck level (`style: "corporate"`) or per-slide (`visual.style: "blueprint"`).

| Style | Description | Best for |
|-------|-------------|----------|
| `corporate` | Clean flat design, brand primary/pink, white background | Default — works for any audience |
| `tech-gradient` | Purple-to-cyan gradients, glowing edges, dark background | Tech workshops, partner pitches |
| `blueprint` | White lines on navy, engineering schematic style | Architecture slides, deep-dives |
| `isometric` | 3D isometric blocks, colorful depth | Tech infographics |
| `glassmorphism` | Frosted glass panels, translucent cards | Premium/modern feel |
| `neon-wireframe` | Dark background, neon wireframe outlines | Innovation presentations |
| `paper-cut` | Layered paper cutout, soft shadows | Non-technical audiences |
| `minimal-line` | Single-weight lines, extensive whitespace | Elegant executive decks |
| `hand-drawn` | Sketchy whiteboard style, imperfect lines | Brainstorming, workshops |

---

## Diagram Pipeline

Embed diagrams in `content_diagram_text` slides using the `visual:` block:

```yaml
- layout: content_diagram_text
  headline: "Architecture"
  split: "v-50/50"
  visual:
    type: "org-hierarchy"
    style: "corporate"
    approaches: ["native", "drawio"]
    data:
      root: "System"
      children:
        - "Component A"
        - "Component B"
  left_icon: "gear"
  left_title: "Structure"
  left_body: "Description..."
  right_icon: "sliders"
  right_title: "Tradeoffs"
  right_body: "Description..."
```

**Diagram types:** org-hierarchy, flow, comparison, timeline, key-stats, labeled-boxes, process-steps

**Rendering approaches:**
- `native` — PPTX shapes (fastest, editable, always available)
- `drawio` — draw.io XML export as PNG
- `ai` — Google Imagen 4 + Gemini review (requires API key)

**Split ratios:** `v-70/30`, `v-50/50`, `v-30/70`, `h-60/40`, `h-50/50`, `h-40/60`

---

## Content Limits

Each layout has maximum content capacity. Exceeding these limits causes text overflow, cramped layouts, or unreadable slides. The QA pipeline checks against these limits automatically and suggests fixes.

### Quick Reference — Max Content Per Layout

| Layout | Max Items | Body Text Limit | When Exceeded |
|--------|-----------|-----------------|---------------|
| `agenda` | 7 items | 2 lines per item | Split into two agenda slides |
| `side_by_side` | 2 columns | ~18 lines / 130 words per body | Split into Part 1/2 or use `numbered_list` |
| `three_column` | 3 columns | ~20 lines / 110 words per body | Use `side_by_side` for 2 dense topics |
| `four_card` | 8 cards | 4 cards: ~11 lines; 8 cards: ~14 lines at 7pt | Split across two slides (4 cards each) |
| `numbered_list` | ~5 items | ~7 lines per body | Split: "Steps 1-3" and "Steps 4-6" |
| `status_board` | ~7 items | ~2 lines per summary | Split into themed boards |
| `kpi_dashboard` | 8 metrics | 2-3 words per label | Split into themed dashboards |
| `content_table` | ~13 rows | 1-2 lines per cell | Split with header repeated: "(continued)" |
| `matrix` | ~9 rows | Single letter/word per cell | Split with header repeated |
| `roadmap` | 4 swimlanes | 4 bars per lane, 25 chars per bar | Split: "Phase 1" and "Phase 2" roadmaps |
| `funnel` | ~6 stages | 30 chars per label | Reduce to key stages |
| `quote` | 1 quote | ~5 lines / 40 words | Edit down or use `callout` |
| `callout` | 1 message | ~4 lines callout + ~5 lines supporting | Follow with `numbered_list` for detail |
| `before_after` | ~14 items/side | 10pt bullet items | Use two `side_by_side` slides |

### Splitting Content Over Multiple Slides

**Tables:** Repeat the header row and column headers on the continuation slide. Add "(continued)" to the headline. Use the same `col_widths`.

**Lists (numbered_list, status_board):** Continue numbering. "Migration Steps (1-5)" on slide 1, "Migration Steps (6-10)" on slide 2.

**Cards:** Split into groups of 4. "Partner Shortlist (1/2)" and "Partner Shortlist (2/2)".

**Roadmaps:** Split by phase. "Phase 1 Roadmap (2025-2026)" and "Phase 2 Roadmap (2027-2028)".

Full machine-readable limits: `layout-limits.json`

---

## QA Pipeline

Every build runs automated quality checks:

| Check | Description |
|-------|-------------|
| **Content limits** | Checks YAML against per-layout content limits with split suggestions |
| **Overlap detection** | Flags text elements that vertically overlap |
| **Margin violations** | Elements within 0.5" of slide edge |
| **Word count** | Warns at 30 words per text box, flags at 50 |
| **Font size floor** | Flags text below 7pt, warns below 9pt |
| **Text overflow** | Estimates if text exceeds its container |
| **Containment** | Verifies text stays inside parent shapes |
| **Cross-slide consistency** | Font families, headline sizes, footer presence |
| **Claude vision review** | AI-powered visual QA (with `--ai-review`) |

**Flags:**
- `--proof-images` — generate PNG previews with issue annotations
- `--ai-review` — send each slide to Claude Sonnet for visual review
- `--strict` — block upload if critical issues found

---

## Layout Selection Guide

When building a presentation, use this guide to pick layouts:

| Content type | Recommended layout |
|--------------|--------------------|
| Opening slide | `title_cover` |
| Agenda / table of contents | `agenda` |
| Section break | `section_divider` |
| Two-topic comparison | `side_by_side` |
| Three pillars / options | `three_column` |
| 4+ cards / teams / items | `four_card` |
| Program overview with stats | `content_two_col` |
| Architecture diagram | `content_diagram_text` |
| Step-by-step process | `numbered_list` |
| Current vs target state | `before_after` |
| Data grid / comparison table | `content_table` or `matrix` |
| Multi-metric dashboard | `kpi_dashboard` |
| Project health / RAG | `status_board` |
| Hero number / impact stat | `big_stat_manual` |
| Timeline / phases | `roadmap` |
| Key recommendation | `callout` (boxed) |
| Stakeholder quote | `quote` |
| Pipeline / adoption stages | `funnel` |
| Full-slide image | `image_showcase` |
| Closing / Q&A | `closing` |

---

## Visual Showcase

See `README.md` for a screenshot of every layout type with the YAML that produced it, built from real example data.
