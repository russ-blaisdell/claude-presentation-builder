# Competitive Edge — Claude Pres Builder

## What This Is

This document defines what makes Claude Pres Builder a contest-winning AI presentation solution. It serves as a **quality rubric** — every feature, layout, and design decision should be measured against these differentiators. If we're not clearly ahead of the field on each dimension, we have work to do.

---

## The Competitive Landscape

Most AI presentation tools fall into one of two buckets:

1. **Template stuffers** — Take user text, drop it into a pre-made template, apply brand colors. No intelligence about layout selection, content density, or visual hierarchy. (Gamma, Beautiful.ai, Tome, SlidesAI)

2. **Image generators** — Create slide-sized images with AI. Visually interesting but not editable, not data-driven, not brand-compliant. (Midjourney-based workflows, Canva AI)

Neither category delivers what engineering leaders need: **a system that thinks like a presentation designer, executes like a production team, and operates within enterprise brand constraints.**

### Specific Competitor Weaknesses

| Tool | Category | Key Limitation |
|------|----------|----------------|
| **Gamma** | Template stuffer | No adaptive font sizing. Fixed layouts. Can't handle data-heavy content. No QA. |
| **Beautiful.ai** | Template stuffer | "Smart" templates are rigid. Can't split overflowing tables. No research phase. No brand-native rendering. |
| **Tome** | Image generator | Generates images, not editable PPTX objects. No data tables. No version control. |
| **SlidesAI** | Template stuffer | Google Slides only. No diagram engine. No vision QA. Generic templates. |
| **Canva AI** | Hybrid | Strong templates but no intelligence pipeline. No content-aware sizing. No YAML source-of-truth. |
| **Copilot (PowerPoint)** | In-app assistant | Helps write text, doesn't design slides. No layout selection intelligence. No end-to-end pipeline. |

**Our moat:** The combination of research → narrative → adaptive rendering → QA is a pipeline, not a feature. Competitors would need to build 5+ systems to match it.

---

## Our Differentiators

### 1. End-to-End Intelligence Pipeline

**What it is:** Research agents gather context → Claude synthesizes strategy → YAML structure is generated → branded PPTX is built → QA pipeline validates → vision review catches visual issues → human reviews final output.

**Why it wins:** No other tool connects research to narrative to visual execution in a single pipeline. Most tools start at "here's my text, make slides." We start at "here's my topic, build me a presentation."

**Evidence:** The `/create-presentation` skill launches parallel research agents, produces a living strategy document, conducts a synthesis interview, and only then generates the deck. The content is researched, not just formatted.

**Gap to close:** Research modes need refinement (web-only, project+web, project-only). Claude needs better heuristics for when to use which.

---

### 2. Intelligent Layout Selection

**What it is:** Claude chooses layouts based on content characteristics — data density, comparison structure, narrative flow, audience profile — not random template assignment.

**Why it wins:** A table with 3 items should be a card layout. A timeline with 8 milestones needs a roadmap. A single key metric deserves a big-stat slide. The right layout for the content is a design decision, and we automate it.

**Evidence:** 22 layout types each with a distinct structural purpose, tested with 500 generated slides (25 variations per layout via `test-layouts.py`). Layout aliases handle 10+ common naming variations. Content-aware column widths and row heights adapt to actual data. 14+ production YAML decks in daily use across security, cloud migration, partner evaluation, and organizational strategy.

**Gap to close:** Need a formal layout selection rubric (decision tree mapping content → layout). Need audience-adaptive selection (executives get fewer, denser slides; technical audiences get more detail). Need Claude to explain its layout choices in slide notes.

---

### 3. Adaptive Typography & Content Fitting

**What it is:** Font sizes step down automatically when content is dense. Row heights adapt to text wrapping. Column widths auto-size by content length. Tables that overflow split across continuation slides with repeated headers.

**Why it wins:** Every other tool either overflows (text runs off the slide) or uses a fixed small font regardless of content. We find the optimal font size for the actual content, and when nothing fits, we split intelligently rather than truncating.

**Evidence:** `select_font_size()` tries 10pt → 9pt → 8pt → 7pt, picking the largest that fits. `normalize_col_widths()` uses square-root dampening to allocate column space proportionally. `split_table_rows()` creates continuation slides automatically. `compute_row_heights()` uses uniform heights when content is similar, variable heights when content varies.

**Gap to close:** Need the same adaptive intelligence for bullet lists, diagram text, and card layouts — not just tables.

---

### 4. Visual QA with Self-Correction

**What it is:** After building the PPTX, a QA pipeline runs structural checks (overflow, containment, font sizes, word counts), generates proof images, checks for visual issues (overlap, margin violations), and optionally sends each slide to Claude vision for subjective review.

**Why it wins:** No other AI presentation tool validates its own output. We catch text overflow, unhyperlinked URLs, off-center tables, font inconsistencies, and empty text boxes before the human ever sees the deck.

**Evidence:** `qa_pipeline.py` runs 10+ structural checks. `proof_renderer.py` generates full-size PNGs with alignment annotations. Vision review returns categorized issues with severity ratings.

**Gap to close:** QA should auto-fix common issues (re-center a table, increase font size when space allows) rather than just reporting them. Should generate a before/after comparison.

---

### 5. Brand-Native Rendering

**What it is:** Every slide is rendered manually on a clean canvas using precise brand tokens — your company's colors, fonts, and icon set. 10" x 5.625" widescreen canvas with full OOXML theme support (12 color slots + 2 font slots).

**Why it wins:** We don't "theme" a generic template — we build from brand primitives. The output is indistinguishable from slides made by the design team. Icons are curated from the brand's icon set, not generic clip art.

**Evidence:** `curated-layouts.json` maps every layout to template positions. Design tokens are constants used across all builders. 6 built-in brands ship out of the box, and the onboarding wizard extracts new brands from any PPTX template.

**Gap to close:** Need brand compliance checking in QA. Need automated brand drift detection.

---

### 6. YAML-as-Source-of-Truth

**What it is:** Presentations are defined in human-readable YAML files. Every slide is a structured definition — layout, headline, content, icons, data. The YAML is version-controlled, diffable, reviewable, and reproducible.

**Why it wins:** Presentations become code. You can review a deck in a PR. You can template a quarterly review and update just the data. You can generate 10 variants by changing the YAML programmatically. No other tool treats presentations as structured data.

**Evidence:** Production YAML decks in daily use across strategy, migration, partner evaluation, and organizational presentations.

**Gap to close:** Need a YAML linter/validator. Need schema documentation. Need YAML-to-slides round-tripping (edit in Slides, export back to YAML).

---

### 7. Multi-Approach Diagram Engine

**What it is:** Three rendering backends — native PPTX shapes, draw.io XML export, and AI-generated images (Google Imagen 4 with Gemini 2.5 Flash review loop). 7 diagram types (org hierarchy, flow, comparison, timeline, key-stats, labeled-boxes, process-steps). 10 style palettes (corporate, tech-gradient, blueprint, etc.) with role-based color mapping.

**Why it wins:** No other AI presentation tool generates editable, on-brand diagrams as native PowerPoint shapes. The AI renderer has a built-in quality loop — Imagen generates, Gemini reviews for text accuracy and structural correctness, auto-retries with refined prompts up to 3 times, and falls back to native rendering if AI fails.

**Evidence:** `diagrams/native_renderer.py` builds PPTX-native shapes. `diagrams/ai_renderer.py` runs the Imagen → Gemini review loop with max 3 attempts. `diagrams/engine.py` dispatches across all three backends. 10 named palettes map role-based colors (root, child, connector, accent, background) consistently across renderers.

**Gap to close:** Native renderer covers 7 types but real decks need architecture diagrams, Venn diagrams, and Sankey flows. AI renderer quality varies — need to expand the Gemini review criteria and add more structural checks.

---

### 8. Research-Backed Design System

**What it is:** The entire design system was derived from empirical analysis of 50+ real corporate presentations (900+ slides) — all-hands decks, steering committees, product reviews, tech board presentations. Typography rules, density limits, layout proportions, and color usage all come from measured patterns in actual corporate decks, not design intuition.

**Why it wins:** Most presentation tools apply generic "best practices." We measured what actually works in real enterprise decks — word counts per slide, font distributions, color frequency, heading patterns — and built rules from data. The `analyze-corpus.py` tool lets any user run the same analysis on their own company's decks.

**Evidence:** Five deep research documents in `research/` cover visual design (53 rules), typography (80 rules), audience profiles (5 profiles), storytelling frameworks (6 frameworks), and corpus analysis findings.

**Gap to close:** Need to expand analysis with public best-in-class decks from consulting firms and tech companies. Need to periodically re-analyze as design languages evolve.

---

### 9. Storytelling Architecture

**What it is:** Decks follow proven narrative frameworks — Minto pyramid, Situation-Complication-Resolution, McKinsey SCQA. The slide sequence is intentional: context → problem → evidence → recommendation → next steps.

**Why it wins:** Most AI tools generate slides in isolation. We generate a narrative arc. The research phase identifies the story, the synthesis shapes the argument, and the layout sequence delivers it.

**Evidence:** `presentation-principles.md` codifies 5 storytelling frameworks with slide-sequence patterns. Research corpus analysis of 50+ real corporate decks informed the design system.

**Gap to close:** Claude doesn't actively enforce narrative structure yet. Need a "story validator" that checks the slide sequence against framework patterns and flags weak transitions.

---

**Total: 9 differentiators.** No competitor covers more than 2. Our moat is the integration — each system reinforces the others.

---

## Scoring Rubric

Use this to evaluate any deck we produce:

| Dimension | 1 (Weak) | 3 (Good) | 5 (Exceptional) |
|-----------|----------|----------|------------------|
| **Layout fit** | Wrong layout for content type | Reasonable layout choices | Every slide uses the optimal layout for its content |
| **Visual hierarchy** | Wall of text, no emphasis | Clear headings, some structure | Eye flows naturally: headline → key insight → supporting detail |
| **Data presentation** | Raw numbers in paragraphs | Basic tables and lists | Tables with adaptive sizing, KPI dashboards, visual scoring |
| **Narrative flow** | Random slide order | Logical grouping | Clear story arc: setup → tension → resolution → action |
| **Brand compliance** | Off-brand colors/fonts | Correct colors, adequate spacing | Indistinguishable from design-team output |
| **Information density** | Too sparse or too cramped | Reasonable balance | Tufte-level: maximum insight per pixel, zero chartjunk |
| **Adaptiveness** | Fixed layout regardless of content | Some content-aware sizing | Font, spacing, layout all adapt to actual content volume |
| **Diagrams** | No diagrams, or static images | Basic shapes, one style | Native editable diagrams, multiple styles, AI-reviewed for accuracy |
| **Polish** | Visible issues (overflow, misalignment) | Clean but basic | Borders, alignment, whitespace, typography all publication-grade |

**Target: Average 4+ across all dimensions for every deck we produce.**

---

## Roadmap to First Prize

### Now (Table Overhaul) — DONE
- [x] Content-aware column widths
- [x] Adaptive row heights
- [x] Font step-down algorithm
- [x] Multi-slide table splitting
- [x] Cell bullets and bold
- [x] Column alignment
- [x] Clean border system
- [x] Header emphasis

### Next (Layout Expansion) — Research Complete
Research analyzed 30+ sources (McKinsey, BCG, Bain, Stripe, think-cell, Visme, SlideModel, etc.) and cataloged 53 distinct layout patterns. 20+ are gaps. See `research/layout-patterns-research.md` for full report.

**Top 10 new layouts to add (ranked by frequency x impact x feasibility):**

| Rank | Layout | What It Is | Complexity |
|------|--------|-----------|------------|
| 1 | `process_flow` | Chevron/step flow — 3-6 connected steps, horizontal | Medium |
| 2 | `comparison_matrix` | Feature comparison with Harvey balls/checkmarks | Medium |
| 3 | `quadrant` | 2x2 matrix (SWOT, priority, effort/impact) | Low-Medium |
| 4 | `team_profiles` | People cards with photo/icon, name, role, context | Low |
| 5 | `pros_cons` | Green pros / red cons columns with recommendation | Low |
| 6 | `staircase` | Maturity model — ascending levels with current highlight | Medium |
| 7 | `donut_rings` | Progress ring dashboard — percentage arcs with labels | Medium |
| 8 | `pyramid` | Hierarchical tiers (strategy layers, tech stack) | Medium |
| 9 | `venn` | 2-3 overlapping circles with intersection labels | Medium |
| 10 | `waterfall` | Bridge chart — floating bars showing A→B contributions | High |

**Priority batch:** Top 5 (#1-5) bring us from 22→27 layouts and close the biggest consulting-deck gaps. All feasible with current `add_shape()`/`add_textbox()` rendering.

- [x] Implement batch 1: process_flow, comparison_matrix, quadrant, team_profiles, pros_cons (22→27)
- [x] Build layout selection rubric for Claude
- [x] Implement batches 2-5: staircase, donut_rings, pyramid, venn, waterfall, pricing_table, concentric_circles, bold_bullet, cycle_diagram, hub_spoke, gauge_dashboard, risk_heat_map, tornado_chart, radar_chart, combo_chart, bubble_chart, bento_grid, dashboard_panel, left_nav_sidebar, image_text_hero (27→47)
- [x] 47 layouts covering all 53 identified patterns

### Then (Intelligence Layer) — DONE
- [x] Story validator — checks slide sequence against narrative frameworks
- [x] Auto-fix in QA — re-centers tables, upsizes fonts, adds hyperlinks
- [x] Audience-adaptive density — c-suite/manager/ic presets with layout + headline guidance
- [x] Layout recommendation engine — [Layout choice] notes in every slide explaining selection

### Later (Generalization) — PARTIALLY DONE
- [x] Multi-brand support — configurable color palette via brand YAML files
- [ ] YAML schema validation and linting
- [ ] Round-trip editing (Slides → YAML export)
- [ ] Interactive preview during authoring

---

## Contest Demo Strategy

A contest judge needs to see the **full pipeline in action** in under 5 minutes. The demo should be a single compelling scenario that touches every differentiator.

### The Demo Scenario

**Prompt:** "Build me a presentation on our cloud migration strategy for the CTO."

**What the judge sees:**

1. **Research phase** (30s) — Parallel agents gather context via web research and project data. Not template-filling — actual research.
2. **Strategy synthesis** (30s) — Claude produces a living strategy doc: narrative arc, key findings, recommendation structure. The human reviews and approves.
3. **YAML generation** (30s) — Structured slide definitions: title cover → agenda → executive summary (big_stat) → partner comparison (content_table) → per-partner scoring (four_card) → risk matrix (content_table with col_align) → timeline (roadmap) → recommendation → next steps → closing. Each layout chosen for the content type.
4. **Build + QA** (60s) — PPTX renders with brand tokens. QA catches a table overflow, auto-splits to continuation slide. Font step-down finds optimal size. Proof images generated. Vision review passes.
5. **Final output** (60s) — Walk through the deck: brand-perfect, data-driven, narratively coherent. Show the YAML source. Show the QA report. Show the proof images.

### Key Moments to Highlight

- "Watch it choose a table layout for the scoring data, not cards — because there are 8 partners with 6 criteria each"
- "See how the font stepped down from 10pt to 8pt because the evidence text is dense"
- "This table had 14 rows — it automatically split to two slides with repeated headers"
- "The diagram was generated as native PPTX shapes — you can edit every box and arrow"
- "The QA pipeline caught that this URL wasn't hyperlinked and flagged it"

### Demo Deck to Build

We should create a showcase deck specifically designed to demonstrate every differentiator. It should use a real business scenario (cloud migration strategy is ideal because it has tables, comparisons, timelines, diagrams, and recommendations).

---

## How to Use This Document

1. **Before building a deck:** Read the scoring rubric. Aim for 4+ on every dimension.
2. **After building a deck:** Score it honestly. Identify the weakest dimension. Fix it.
3. **When adding features:** Check if it advances a differentiator. If not, deprioritize.
4. **When comparing to competitors:** Map their capabilities to our 7 differentiators. Find where we're behind.

This is a living document. Update it as we ship features and close gaps.
