---
name: create-presentation
description: >
  Build a research-backed presentation end-to-end: parallel research agents,
  living markdown strategy document, synthesis interview, and a branded PowerPoint deck
  built from the Claude Pres Builder YAML pipeline. Use when the user wants to create
  a presentation, deck, or strategy document on any topic.
argument-hint: "[topic] [audience] [number-of-research-areas]"
---

# create-presentation

Build a complete, research-backed presentation using the Claude Pres Builder.
Follow this exact workflow in order. Do not skip phases.

## Locating the builder

The builder lives in a separate repository. Its location is recorded in:
```
~/.claude/skills/create-presentation-config
```

**Step 1 of every invocation: read this config file.** It exports `REPO_PATH`
(the absolute path to the builder repo) and `PYTHON` (the absolute path to the
builder's Python interpreter). Use these for ALL file references and shell
commands below. If the file is missing or `REPO_PATH` is invalid, tell the user
to run `setup.sh` in their cloned builder repo.

For all references below, treat `$REPO` as shorthand for the value of
`REPO_PATH` from that config.

## Deck Builder Reference

**All presentations are built using the YAML-driven deck builder.**

Before writing any YAML or building any deck, read these two files:

**Presentation principles** (read FIRST -- governs all design decisions):
```
$REPO/presentation-principles.md
```
Contains: audience profiles, storytelling frameworks, icon rules, typography/emphasis
rules, density limits, slide sequence templates. Use these to decide structure, layout
selection, content density, and headline style BEFORE writing YAML.

**Presentation guide** (technical reference for YAML authoring):
```
$REPO/presentation-guide.md
```
Contains: all 47 layout types with YAML field references, icon names by category,
design tokens, build commands, QA flags, content limits per layout.

**Starter YAML skeletons:**
```
$REPO/deck-templates.md
```

**Visual showcase -- screenshot of every layout with YAML:**
```
$REPO/README.md
```

---

## Invocation

```
/create-presentation "Developer Platform Strategy" "C-suite, VP Engineering" 4
/create-presentation "Cloud FinOps Strategy" "CFO, VP Engineering"
/create-presentation "API Platform Modernization"
```

Arguments:
- `$ARGUMENTS[0]` -- Topic / title (required)
- `$ARGUMENTS[1]` -- Target audience (optional; default: "Executive leadership")
- `$ARGUMENTS[2]` -- Number of research areas (optional; default: inferred from topic)

If the topic is ambiguous, ask one clarifying question first:
> "Who is the primary decision-maker this presentation must influence, and what decision do you want them to make?"

---

## PHASE 0 -- Setup

1. **Confirm working directory** with the user. All output files go here.

2. **Read both reference files** (using `$REPO` from the config):
   ```
   $REPO/presentation-principles.md
   $REPO/presentation-guide.md
   ```

3. **Identify the audience profile** from `$ARGUMENTS[1]` and map to one of:
   - **C-Suite** -> 8-12 slides, 30-50 words/slide, assertion headlines, minimal icons
   - **Customer/Partner** -> 12-18 slides, benefit headlines, must work standalone
   - **Middle Management** -> 15-25 slides, action headlines, include RACI/timelines
   - **Individual Contributor** -> 20-30 slides, technical headlines, include data/diagrams
   - **Mixed** -> layer cake (strategic -> tactical -> technical appendix)

   This profile governs ALL downstream decisions: layout selection, content density,
   headline style, icon usage, and slide count.

4. **Select storytelling framework** based on purpose:
   - Decision request -> **Minto Pyramid** (lead with recommendation)
   - Change/transformation -> **SCR** (situation -> complication -> resolution)
   - Vision/inspiration -> **Duarte Sparkline** (alternate what-is / what-could-be)
   - Default -> **Minto Pyramid**

5. **Infer 4-6 research areas** from the topic. Each must be:
   - Self-contained and independently researchable
   - Clearly relevant to the stated audience
   - Distinct enough that two agents won't duplicate content

6. **Create tasks** with `TaskCreate`:
   - Task 1 through N: one per research area
   - Task N+1: Strategy Synthesis Interview
   - Task N+2: Build PowerPoint from YAML

7. **Create the master living document** `[topic-slug]-strategy.md`:
   - Header: topic, audience, status, date
   - TODO table: one row per task, all `pending`
   - One placeholder section per research area
   - `## Strategy Brief` (placeholder)
   - `## Presentation Outline` (placeholder)
   - `## Appendix`

8. **Confirm** research areas and task list with the user before launching agents.

---

## PHASE 1 -- Parallel Research

Launch all research agents simultaneously with `Agent` tool, `run_in_background: true`.

Each agent prompt must include:
- The research area and its relationship to the overall topic
- 6-10 explicit sub-topics to cover (not open-ended)
- Write findings to `[area-slug].md` in the working directory
- Also update the corresponding section in the master strategy doc
- Tone: "professional, executive-ready -- concrete and specific, no vague generalities"
- Format: "headers, bullet points, tables, before/after comparisons where applicable"

**Agent prompt template:**
```
You are a [domain expert]. Research and write a comprehensive executive-ready document
on [research area] as it relates to [overall topic].

Cover ALL of the following:
1. [sub-topic 1]
...N. [sub-topic N]

Save to `[area-slug].md` in the current directory.
Update the corresponding section in `[master-doc].md`.

Requirements: professional tone, specific numbers, role names, metrics. No vague
generalities. Headers/tables/bullets. Before-and-after contrasts. Written for [audience].
```

As each agent completes: mark task `completed`, update the TODO table status.

---

## PHASE 2 -- Strategy Synthesis Interview

Start only after ALL research tasks are complete.

Launch one background agent to produce `strategy-synthesis.md` containing:

**Part 1 -- The Interview (8-10 Q&A pairs)**
Each answer: 3-5 paragraphs of strategic narrative. Draw on specific research findings.

Required questions (adapt to topic):
- Q1: 30-second answer to "why does [topic] matter right now"?
- Q2: The single most important thing to get right in the first 90 days?
- Q3: The most dangerous misconception leaders have about [topic]?
- Q4: What is most underestimated -- and why does it catch orgs off guard?
- Q5: Where do most organizations stall, and what is the real reason?
- Q6: What do the three decisions look like that determine success or failure?
- Q7: What does success look like 3 years from now?
- Q8: The one thing the research doesn't fully capture but is critical?
- [Add 2 topic-specific questions from the research]

**Part 2 -- Strategy Brief (2-3 pages)**
- Strategic Imperative: why now, cost of waiting
- Core Thesis: 3-5 sentence north star
- Key Transformation Domains: what fundamentally changes
- Path Forward: 3-horizon view (90 days / 12 months / 3 years)
- Risks of Inaction and Misaction: specific and concrete

**Part 3 -- Presentation Outline (15-25 slides, 5 acts)**
For each slide, specify:
- Slide number, **layout type** (from the 47 available layouts), and title
- Core message (one sentence -- the "so what")
- 3-5 bullet points or key visual concept
- Speaker notes with audience-specific guidance

Act structure:
- Act 1 (slides 1-5): The Burning Platform -- why this matters, why now
- Act 2 (slides 6-14): What Changes -- key domains, before/after contrast
- Act 3 (slides 15-18): The Strategic Recommendation
- Act 4 (slides 19-23): Path Forward -- phases, 90-day plan, metrics, governance
- Act 5 (slides 24-25): Call to Action -- decisions required, first step

**Layout selection guide for each act:**
- Act 1: `title_cover`, `agenda`, `section_divider`, `kpi_dashboard` or `big_stat`, `before_after`
- Act 2: `section_divider`, `three_column`, `side_by_side`, `content_diagram_text`, `four_card`, `content_table`
- Act 3: `callout`, `quote`, `numbered_list`
- Act 4: `roadmap`, `status_board`, `matrix`, `kpi_dashboard`
- Act 5: `callout` or `numbered_list`, `closing`

After writing `strategy-synthesis.md`, update the master doc and mark synthesis task completed.

---

## PHASE 3 -- Build the YAML Deck Definition

Start only after synthesis is complete.

### Step 1: Read the deck builder reference

Read `$REPO/presentation-guide.md` (using the `Read` tool with the absolute path).

### Step 2: Verify Python environment

Use the `PYTHON` value from `~/.claude/skills/create-presentation-config`. This is
the builder's venv with all dependencies pre-installed by `setup.sh`.

```bash
ls "$PYTHON"  # should print the path; if missing, ask the user to run setup.sh in the builder repo
```

### Step 3: Write the YAML deck definition

Create `[topic-slug]-deck.yaml` in the working directory. Use the presentation outline
from Phase 2, mapping each slide to a layout from the deck builder.

**YAML structure:**
```yaml
title: "Presentation Title"
date: "2026-Q2"
brand: generic

slides:
  # Act 1: The Burning Platform
  - layout: title_cover
    headline: "Title -- Subtitle"
    subheader: "Team | Context"

  - layout: agenda
    items:
      - "Topic 1"
      - "Topic 2"

  # ... one entry per slide, using the 47 available layouts
```

**Layout selection rules:**
- Use `section_divider` between acts (with section numbers)
- Use `kpi_dashboard` for any slide with 3+ metrics
- Use `before_after` for transformation/change slides
- Use `roadmap` for timeline/phased delivery slides
- Use `callout` (boxed) for the key recommendation
- Use `quote` for stakeholder endorsements or vision statements
- Use `status_board` for RAG/health tracking
- Use `three_column` or `four_card` for pillars/options
- Use `numbered_list` for decision frameworks or next steps
- Use `side_by_side` for two-topic comparisons
- Use `content_diagram_text` with `visual:` block for architecture diagrams
- Use `content_table` or `matrix` for data grids

**Content limits -- respect these to avoid overflow:**
- `agenda`: max 7 items
- `three_column`: max ~20 lines per column at 9pt
- `four_card`: max 4 cards for readable text (5-8 work but text shrinks)
- `numbered_list`: max ~5 items with body text
- `content_table`: max ~13 rows (split with header repeated + "(continued)")
- `matrix`: max ~9 rows
- `status_board`: max ~7 items
- `kpi_dashboard`: max 8 metrics
- `roadmap`: max 4 swimlanes, 4 bars per lane
- `funnel`: max ~6 stages
- `quote`: max ~40 words
- `callout`: max ~4 lines callout + ~5 lines supporting

When content exceeds limits, **split across slides** rather than cramming. Use
"(continued)", "(1/2)", or "Part 1" / "Part 2" in headlines.

Full limits reference: `$REPO/layout-limits.json`

**General content rules:**
- Keep body text concise -- the slide is a visual aid, not a document
- Use icons from the icon library (see `$REPO/presentation-guide.md` for full list by category)
- Add `notes:` field with speaker notes for important slides

### Step 4: Build and QA

```bash
# Build with proof images and QA pipeline (run from working directory)
"$PYTHON" "$REPO/test_deck.py" [topic-slug]-deck.yaml --proof-images
```

### Step 5: Review proof images

Check the generated `[topic-slug]-deck-proof/` directory for PNG previews of each slide.
Fix any flagged issues (overlaps, overflow, margin violations) by adjusting the YAML
and rebuilding.

---

## PHASE 4 -- Documentation

Write two files in the working directory:

**README.md**
- What this project produces (file map table)
- How it was built (step-by-step: research -> synthesis -> deck)
- Research scope (one paragraph per area with key findings)
- Presentation structure (acts and slides)
- Key strategic principles (5 governing principles that emerged)
- How to rebuild: `"$PYTHON" "$REPO/test_deck.py" [yaml] --proof-images` (substitute actual REPO_PATH and PYTHON values)

**CLAUDE.md**
- Project summary
- File map (all files and purpose)
- How to work on this in future sessions
- Key content reference (thesis, principles, path forward)
- Presentation notes (audience-specific guidance, anticipated tough questions)
- Style and tone guidelines

---

## PHASE 5 -- Final Status Report

Provide the user:
1. **File inventory** -- table of all files with sizes
2. **Presentation summary** -- title, slide count, act structure
3. **Key strategic outputs** -- core thesis, 3 governing principles, 3-horizon path
4. **Next steps** -- how to open the deck, rebuild from YAML, customize it

---

## Quality standards

- **Specificity:** Every claim needs a number, a role name, or a concrete mechanism.
- **Before/after contrast:** Every change description includes a concrete before and after state.
- **No filler:** Lead with findings. No introductory paragraphs that restate the task.
- **Audience calibration:** C-suite gets strategic narrative and outcomes. Engineering leaders get specific patterns and role definitions. Both get concrete metrics.
- **Governing principle:** Identify the one sentence that, if understood, makes everything else coherent.
- **Brand fidelity:** All decks use the brand system. Never hardcode colors or fonts -- use `brand:` in the YAML and let the builder handle theming.
- **QA before delivery:** Always run with `--proof-images` to verify layout quality before presenting to the user.
