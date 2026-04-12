# Layout Selection Guide

**For Claude and deck authors.** This guide tells you which layout to use for a given piece of content. It supplements `presentation-guide.md` (YAML field reference) and `presentation-principles.md` (audience/storytelling rules).

The goal: **every slide uses the optimal layout for its content type, not the default or easiest one.**

---

## Quick Decision Tree

Start here. Ask these questions about the content for each slide:

```
What is this slide's job?
│
├─ Frame the deck (open/close/navigate)
│  ├─ First slide?                    → title_cover
│  ├─ List of topics?                 → agenda
│  ├─ Transition between sections?    → section_divider
│  └─ Final slide?                    → closing
│
├─ Deliver a single key message
│  ├─ One number/metric?              → big_stat_manual
│  ├─ One recommendation/decision?    → callout
│  └─ One quote from a person?        → quote
│
├─ Show data or status
│  ├─ Multiple KPIs (2-8 metrics)?    → kpi_dashboard
│  ├─ RAG status of workstreams?      → status_board
│  ├─ Tabular data (rows × columns)?  → (see Table Decision below)
│  └─ A single visual + explanation?  → content_diagram_text
│
├─ Compare or evaluate options
│  ├─ Before vs after state?          → before_after
│  ├─ Strengths vs risks?            → pros_cons
│  ├─ Feature checklist with scores?  → comparison_matrix
│  ├─ 2x2 priority/SWOT?            → quadrant
│  ├─ Tier/pricing comparison?        → pricing_table
│  ├─ Exactly 2 topics?              → side_by_side
│  ├─ Exactly 3 topics?              → three_column
│  └─ 4-8 discrete items?            → four_card
│
├─ Show a process or timeline
│  ├─ Time-based with durations?      → roadmap
│  ├─ Pipeline/funnel stages?         → funnel
│  ├─ Sequential steps (3-6)?         → process_flow
│  ├─ Repeating cycle?                → cycle_diagram
│  ├─ Central hub + satellites?       → hub_spoke
│  └─ Maturity/progression levels?    → staircase
│
├─ Show data or charts
│  ├─ Multiple KPIs (2-8 metrics)?    → kpi_dashboard
│  ├─ Progress percentages?           → donut_rings
│  ├─ Performance vs thresholds?      → gauge_dashboard
│  ├─ "How we got from A to B"?       → waterfall
│  ├─ Sensitivity/impact ranking?     → tornado_chart
│  ├─ Multi-dimension comparison?     → radar_chart
│  ├─ Trend + volume together?        → combo_chart
│  ├─ Portfolio/3-variable scatter?   → bubble_chart
│  └─ Risk likelihood x impact?       → risk_heat_map
│
├─ Show structure or hierarchy
│  ├─ Strategy layers?                → pyramid
│  ├─ Nested scope (TAM/SAM/SOM)?    → concentric_circles
│  ├─ Overlapping concepts?           → venn
│  ├─ Mixed-size overview?            → bento_grid
│  ├─ KPIs + chart + summary?         → dashboard_panel
│  └─ Step-by-step with navigation?   → left_nav_sidebar
│
└─ Show people or relationships
   ├─ Team introductions?             → team_profiles
   ├─ Responsibility assignments?     → matrix
   └─ Org/team structure?             → content_diagram_text (org-hierarchy)
```

---

## Table Decision Sub-Tree

Tables are overused. Ask yourself: **does this data genuinely need rows and columns, or is there a better layout?**

```
How many items are you showing?
│
├─ 2 items with descriptions         → side_by_side (NOT a 2-row table)
├─ 3 items with descriptions         → three_column (NOT a 3-row table)
├─ 4-6 items with short descriptions → four_card (NOT a table)
│
├─ Items have 3+ comparable attributes across columns
│  ├─ RACI or coded values?           → matrix
│  ├─ With bullet takeaways below?    → content_table_bullets
│  └─ Pure data grid?                 → content_table
│
└─ Items are a flat list with one attribute
   └─ Use numbered_list or status_board, NOT a table
```

**Rule of thumb:** If a table has only 2 columns and fewer than 6 rows, it's probably a card or side-by-side layout in disguise. Tables shine when you have 3+ columns of comparable data.

---

## Layout-by-Layout Selection Rules

### Structural Layouts

| Layout | Use When | Don't Use When |
|--------|----------|----------------|
| `title_cover` | Opening slide. Always use `background: p12` for photo. | Never skip this — every deck needs a cover. |
| `agenda` | Deck has 3-7 distinct sections. | Deck is <5 slides (agenda adds no value). |
| `section_divider` | Transitioning between major themes in a 10+ slide deck. | Deck is short or has no thematic breaks. |
| `closing` | Final slide. Always use `background: p12`. | Never skip this. |

### Single-Message Layouts

| Layout | Use When | Don't Use When |
|--------|----------|----------------|
| `big_stat_manual` | One hero number that tells the story. C-suite loves these. | You have 2+ metrics (use `kpi_dashboard`). |
| `callout` | One recommendation, decision, or key insight. The "so what" slide. | The message needs supporting data on the same slide. |
| `quote` | Exact words from a named person that carry weight. | Paraphrasing or generic motivational text. |

### Content Layouts

| Layout | Content Shape | Use When | Don't Use When |
|--------|-------------|----------|----------------|
| `side_by_side` | 2 parallel topics | Comparing two options, current/future, team A/team B. | Items aren't truly parallel (use bullets instead). |
| `three_column` | 3 parallel topics | Three pillars, three teams, three phases. | Items have very different amounts of content (columns will look unbalanced). |
| `four_card` | 4-8 discrete items | Cards for partners, teams, capabilities, options. Each item is self-contained. | Items are sequential (use `numbered_list`). Items need cross-comparison (use `content_table`). |
| `numbered_list` | 3-6 ordered steps | Processes, decision frameworks, prioritized actions. Order matters. | Items aren't sequential. More than 6 items (split to 2 slides). |
| `before_after` | Transformation narrative | Current state → target state. Change story. | The "before" and "after" aren't clearly different states. |
| `content_diagram_text` | Visual + narrative | Architecture diagrams, org charts, flow diagrams with explanatory text. | The diagram is decorative, not informational. |

### Data Layouts

| Layout | Content Shape | Use When | Don't Use When |
|--------|-------------|----------|----------------|
| `content_table` | Rows × columns | 3+ columns of comparable data. Scoring rubrics, feature matrices, daily trackers. | <3 columns or <4 rows (use cards or side-by-side). |
| `content_table_bullets` | Table + insights | Table data that needs key takeaways called out below. | Bullets would just repeat what's in the table. |
| `matrix` | Coded grid | RACI charts, responsibility assignments, color-coded assessments. | Cells have long text (use `content_table`). |
| `kpi_dashboard` | 2-8 metrics | Quarterly reviews, program health, portfolio status. Mix of numbers with trends. | Only 1 metric (use `big_stat_manual`). |
| `status_board` | RAG status list | Project/workstream health with red/amber/green + summary text. | Status is binary (just use a table with checkmarks). |
| `roadmap` | Time-based plan | Gantt-style timelines with durations, milestones, swimlanes. | Simple sequential steps without time dimension (use `numbered_list`). |
| `funnel` | Pipeline stages | Decreasing quantities through stages. Sales funnels, adoption pipelines. | Stages don't decrease (it's just a list). |

---

## Audience-Adaptive Layout Selection

The same content should use different layouts depending on who's in the room:

| Content | C-Suite (5 slides) | Manager (12 slides) | IC/Engineer (18 slides) |
|---------|--------------------|--------------------|------------------------|
| Budget | `big_stat_manual` — one number | `content_table` — line items | `content_table` — full breakdown with notes |
| Status | `callout` — "on track" or "blocked" | `status_board` — RAG per workstream | `kpi_dashboard` — detailed metrics |
| Plan | `roadmap` — 4 milestones | `roadmap` — full swimlanes | `numbered_list` + `content_table` — detailed steps |
| Comparison | `callout` — "we recommend X" | `side_by_side` — pros/cons | `content_table` — full scoring matrix |
| Team | Skip | `four_card` — leads only | `four_card` + org chart diagram |

**Density rules by audience:**
- **C-Suite:** Max 30 words per slide. Headlines are assertions ("We should invest $2M"). Prefer `callout`, `big_stat_manual`, `before_after`.
- **Manager:** Max 80 words per slide. Headlines are action-oriented ("Migration partner onboards April 15"). Prefer `roadmap`, `status_board`, `side_by_side`.
- **IC/Engineer:** Max 120 words per slide. Headlines are descriptive ("VM migration path by hypervisor type"). Prefer `content_table`, `numbered_list`, `content_diagram_text`.

---

## Slide Sequencing Patterns

Layouts should follow narrative patterns, not appear randomly:

### Minto Pyramid (C-Suite decks)
```
title_cover → agenda → callout (recommendation) → big_stat_manual (key metric)
→ before_after (why change) → roadmap (how) → kpi_dashboard (proof) → closing
```

### SCR Framework (Problem-solving decks)
```
title_cover → callout (situation) → content_table or status_board (complication)
→ side_by_side or numbered_list (resolution) → roadmap (plan) → closing
```

### Status Update (Operational decks)
```
title_cover → agenda → kpi_dashboard (health) → status_board (workstreams)
→ [section_divider → detail slides per workstream] → roadmap (upcoming) → closing
```

### Evaluation/Decision (Partner/vendor decks)
```
title_cover → agenda → callout (criteria) → content_table (scoring)
→ four_card (shortlist) → side_by_side (top 2 deep-dive)
→ callout (recommendation) → numbered_list (next steps) → closing
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `content_table` for 2-column, 3-row data | Use `side_by_side` or `three_column` |
| Using `four_card` for sequential steps | Use `numbered_list` — order matters |
| Putting 10 bullet points on a `side_by_side` | Split into 2 slides, or use `content_table` |
| Using `content_diagram_text` without a real diagram | Use `side_by_side` or `callout` |
| Every slide is `four_card` | Vary layouts — monotony kills attention |
| Opening with a table | Open with `callout` or `big_stat_manual` — lead with the insight |
| No `section_divider` in a 15-slide deck | Add dividers every 3-4 content slides |
| Status board for non-RAG content | Use `content_table` if items aren't red/amber/green |

---

## Extended Layouts (25 new layouts added)

All layouts from the research are now implemented. 47 total layout types covering all 53 identified patterns.

### Process & Flow
| Layout | Use When |
|--------|----------|
| `process_flow` | 3-6 sequential steps (chevron or circle style, with status coloring) |
| `cycle_diagram` | Repeating process (3-6 nodes in a ring with arrows) |
| `hub_spoke` | Central concept with radiating related items |
| `staircase` | Maturity levels, progression stages, ascending capability |

### Data Visualization
| Layout | Use When |
|--------|----------|
| `waterfall` | How you got from A to B — positive/negative contributions |
| `donut_rings` | Percentage progress toward goals (OKRs, completion) |
| `gauge_dashboard` | Performance against thresholds (SLAs, health scores) |
| `tornado_chart` | Sensitivity analysis — which variables have biggest impact |
| `radar_chart` | Multi-dimension capability comparison |
| `combo_chart` | Two metrics on one slide — bars + line with dual axes |
| `bubble_chart` | Three-variable scatter (x, y, size) for portfolio analysis |
| `risk_heat_map` | 5x5 likelihood x impact grid with plotted risks |

### Comparison & Analysis
| Layout | Use When |
|--------|----------|
| `comparison_matrix` | Feature evaluation with Harvey balls/checkmarks |
| `quadrant` | 2x2 SWOT, effort/impact, priority matrix |
| `pros_cons` | Strengths vs risks with recommendation |
| `pricing_table` | Tier comparison cards with highlighted recommended plan |
| `bold_bullet` | Executive summary — assertions with indented evidence |

### Structural & Visual
| Layout | Use When |
|--------|----------|
| `team_profiles` | People cards with icons, names, roles |
| `pyramid` | Hierarchical layers (strategy, tech stack) |
| `venn` | Overlapping concepts, strategic intersection |
| `concentric_circles` | Nested scope (TAM/SAM/SOM, layered strategy) |
| `bento_grid` | Mixed-size tiles with hero + supporting cards |
| `dashboard_panel` | KPI tiles + chart + summary combined |
| `left_nav_sidebar` | Step-by-step walkthrough with navigation panel |
| `image_text_hero` | Full-bleed image with text overlay |

---

## Measured Capacity Per Layout

Verified from 162-slide stress test (April 2026). The builder validates against these limits at build time and returns clear error messages when content exceeds them. See `layout-limits.json` for machine-readable values.

### When to Split vs Shrink vs Change Layout

| Situation | Action |
|-----------|--------|
| Item count exceeds max | Split across 2 slides with "(continued)" headline |
| Text too long for shape | Shorten text or use a layout with more text capacity |
| Too many columns in table | Remove non-essential columns or transpose the data |
| Too many items for visual layout | Switch to `content_table` (tables scale better than shapes) |

### Content Layouts

| Layout | Comfortable Max | Hard Max | When to Switch |
|--------|----------------|----------|----------------|
| `four_card` | 6 cards | 8 (short text only) | 6+ with descriptions: use `content_table` |
| `numbered_list` | 5 items | 7 | 6+ items: split across slides |
| `before_after` | 5 per side | 7 per side | 6+ per side: use `content_table` |
| `side_by_side` | 8 lines/side | — | Dense comparison: use `content_table` |

### Data Layouts

| Layout | Comfortable Max | Hard Max | When to Switch |
|--------|----------------|----------|----------------|
| `content_table` | 5 cols x 8 rows | 6 cols x 12 rows (auto-splits) | 7+ cols: reduce columns |
| `kpi_dashboard` | 6 metrics | 8 | 9+: split into themed dashboards |
| `status_board` | 5 items | 7 | 8+: group by theme |
| `comparison_matrix` | 4 options x 6 criteria | 5 options x 8 criteria | 6+ options: use `content_table` |

### Process & Flow Layouts

| Layout | Comfortable Max | Hard Max | When to Switch |
|--------|----------------|----------|----------------|
| `process_flow` | 5 steps | 6 (short labels) | 7+: use `roadmap` or `numbered_list` |
| `staircase` | 4 levels | 5 | 6+: use `numbered_list` |
| `cycle_diagram` | 5 nodes | 6 | Labels must be single short words |
| `hub_spoke` | 6 spokes | 8 (short labels) | 9+: use `content_table` or split |
| `funnel` | 4 stages | 5 | Labels auto-shrink; use abbreviations for narrow stages |

### Chart Layouts

| Layout | Comfortable Max | Hard Max | Notes |
|--------|----------------|----------|-------|
| `donut_rings` | 4 rings | 6 | Labels below, max 25 chars |
| `gauge_dashboard` | 3 gauges | 4 | Labels below gauges |
| `waterfall` | 5 items | 7 | Bar labels max 12 chars |
| `tornado_chart` | 5 items | 7 | Label column max 25 chars |
| `radar_chart` | 6 axes, 2 series | 8 axes, 3 series | Axis labels max 15 chars |
| `combo_chart` | 6 categories | 8 | Category labels max 8 chars |
| `bubble_chart` | 4 bubbles | 5 | Labels inside bubbles, max 20 chars |
| `risk_heat_map` | 4 items | 8 | Fixed 5x5 grid + risk register panel |

### Comparison & Composite Layouts

| Layout | Comfortable Max | Hard Max | Notes |
|--------|----------------|----------|-------|
| `quadrant` | 3 items/quadrant | 5 | Fixed 4 quadrants; items max 30 chars |
| `pros_cons` | 4 per side | 6 | Recommendation bar max 80 chars |
| `pricing_table` | 3 tiers | 4 | Features max 6 per tier |
| `bold_bullet` | 3 points | 4 | Max 3 evidence items per point |
| `team_profiles` | 4 profiles | 8 | 5-8 renders as 2-row grid |
| `bento_grid` | 4 tiles | 5 | 1 hero + 3-4 small |
| `dashboard_panel` | 4 KPIs, 6 bars | — | Summary max 150 chars |
| `pyramid` | 4 tiers | 5 | Label max 25 chars, body max 30 |
| `venn` | 2-3 circles | 3 | Labels max 15 chars |
| `concentric_circles` | 3 rings | 4 | Labels max 10 chars |
