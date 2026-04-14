# Presentation Principles

Actionable rules for building effective presentations with the deck builder. The `/create-presentation` skill reads this file to make layout, density, emphasis, and structural decisions.

**Related docs:** [README](README.md) | [Presentation Guide](presentation-guide.md) (YAML reference) | [Deck Templates](deck-templates.md) | [Content Limits](layout-limits.json)

**Research backing these principles:** [Visual Design](research/visual-design.md) (53 rules) | [Typography](research/typography-emphasis.md) (80 rules) | [Audience Profiles](research/audience-profiles.md) (5 profiles) | [Storytelling Frameworks](research/storytelling-frameworks.md) (4 frameworks, 6 sequences) | [Corpus Analysis](analysis/corpus-analysis-report.md) (52 decks, 921 slides from a real company)

---

## Deck Purpose

Every deck has a **purpose** that modifies how the rules below apply. Set this in the YAML `meta` block:

```yaml
meta:
  purpose: strategic    # strategic | mixed | operational
  audience: c-suite
```

| Purpose | When to use | Headline style | Density tolerance | Examples |
|---------|-------------|----------------|-------------------|----------|
| **Strategic** | Persuading, recommending, pitching, requesting decisions | Assertions required | Standard (65% rule, word limits) | Partner selection, AI strategy, cloud migration pitch, customer pitch |
| **Mixed** | Combining strategy with reference data | Assertions preferred, labels OK for data slides | Standard for strategy slides, relaxed for data slides | Quarterly planning kickoffs, architecture reviews, QBRs |
| **Operational** | Reporting status, tracking work, sharing data | Labels expected | Relaxed (data tables OK, higher word counts) | Status updates, MBRs, issue trackers, OKR grids, migration status |

Purpose is orthogonal to audience — you can have an operational deck for the CTO or a strategic deck for ICs. Purpose determines *how* you communicate; audience determines *how much detail*.

*Validated by corpus analysis: 75% of slides in the corpus use label headlines, clustering in operational decks. The 17% that use assertions cluster in strategic decks and are the most visually effective slides in the corpus.*

---

## 1. One Idea Per Slide

Every slide should have exactly one takeaway. The headline IS the takeaway. If you need two ideas, you need two slides.

### Headline rules by purpose

**Strategic decks — assertions required.** Every headline is a full-sentence claim. The audience should be able to read just the headlines and get the complete argument.

- **GOOD:** "All dev/test workloads migrate to cloud by December 2026"
- **BAD:** "Migration Timeline"
- **Test:** Read just the headlines in order — they tell the complete story without body content (McKinsey "horizontal logic")

**Mixed decks — assertions preferred, labels acceptable.** Use assertions for strategy/recommendation slides. Labels are fine for data reference slides within the same deck.

- **Assertion slide:** "Three teams need additional headcount to hit Q2 targets"
- **Label slide (OK):** "Q2 OKR Tracker" (followed by a data table)

**Operational decks — labels expected.** Headlines identify what's on the slide. The audience reads the data, not the headlines.

- **GOOD:** "March Status Update", "Consolidated Top 10 Issues", "Migration Progress by Workstream"
- **Still bad:** No headline at all, or misleading/vague headlines

---

## 2. Audience Profiles

Select layouts, density, and headline style based on who is in the room.

### C-Suite / Board
- **Density:** 30-50 words per slide. Whitespace is your friend.
- **Slide count:** 8-12 for a 30-minute meeting
- **Headline style:** Assertion ("We should invest $2M in cloud migration")
- **Preferred layouts:** `big_stat_manual`, `callout`, `kpi_dashboard`, `before_after`, `roadmap`
- **Icons:** 0-2 per slide, only for key concepts
- **Bold:** Numbers and decisions only
- **Test:** Every slide works if the CEO flips to it with no context

### Customers / Partners
- **Density:** Medium. Clean but with substance to build trust.
- **Slide count:** 12-18 (must work standalone without a presenter)
- **Headline style:** Benefit-oriented ("Reduce parking search time by 40%")
- **Preferred layouts:** `title_cover`, `three_column`, `four_card`, `roadmap`, `quote`
- **Icons:** Moderate. Brand consistency matters.
- **Test:** Would someone forward this to their boss and it still makes sense?

### Middle Management
- **Density:** Medium-high. They can handle more text.
- **Slide count:** 15-25 (reference material)
- **Headline style:** Action-oriented ("Partner decision needed by April 10")
- **Preferred layouts:** `roadmap`, `status_board`, `matrix`, `numbered_list`, `content_table`
- **Icons:** Functional (status circles, category indicators)
- **Test:** Can this slide tell someone what to do this week?

### Individual Contributors
- **Density:** High is fine. They'll read every line.
- **Slide count:** 20-30+ (depth > brevity)
- **Headline style:** Descriptive technical ("Nutanix AHV to GCP Compute Engine Migration Path")
- **Preferred layouts:** `content_table`, `content_diagram_text`, `numbered_list`, `side_by_side`, `matrix`
- **Icons:** Minimal or none. Data > decoration.
- **Test:** Can I implement from this?

### Mixed Audiences
- Use the **layer cake**: start strategic (executives stay), add detail (managers engage), appendix for depth (ICs reference)
- Use `section_divider` slides to signal transitions between layers

---

## 3. Storytelling Frameworks

### Default: Minto Pyramid (lead with the answer)
Best for: executive briefings, decision requests, status updates.

```
1. title_cover
2. agenda
3. callout (THE RECOMMENDATION — slide 2 is the punchline)
4. section_divider "Evidence"
5-8. Evidence slides (kpi_dashboard, before_after, content_table, etc.)
9. roadmap (path forward)
10. numbered_list (next steps)
11. closing
```

### For Transformation Stories: SCR
Situation → Complication → Resolution. Best for persuasion and change management.

```
1-2. Situation (kpi_dashboard — "here's where we are")
3-4. Complication (status_board, big_stat — "here's what's wrong")
5-6. Resolution (callout, before_after — "here's what we do")
7-9. Detail (roadmap, numbered_list, matrix)
10. closing
```

### For Vision Presentations: Duarte Sparkline
Alternate "what is" and "what could be." Best for inspiring action.

### Assertion-Evidence (Strategic and Mixed decks)
For strategic and mixed-purpose decks, apply assertion-evidence: every content headline is a full-sentence claim, body is visual evidence. For operational decks, storytelling frameworks are less relevant — structure by topic or status category instead.

---

## 4. Icons — Optional Enhancement, Not Required

Icons are an enhancement, not an expectation. Most slides use zero icons and work fine. When you do use icons, apply the one-second recognition test: can the audience identify what the icon represents within one second, without reading text? If no, remove it.

### Use icons to:
- **Categorize** section titles (padlock = Security, coin-stacks = Finance)
- **Identify** what a metric measures in KPI cards (server-stack + "1,300")
- **Enable scanning** in status boards (green circle = on track)

### Skip icons when:
- They don't map to a concrete noun ("merge-arrows" beside "Next Steps")
- Text is already short and scannable (a 3-item list needs no icons)
- The slide is data-heavy or operational (icons add clutter to dense content)
- You're unsure — no icon is always better than a wrong icon

### Max icons per slide by layout:

| Layout | Max Icons |
|--------|-----------|
| `title_cover`, `closing` | 0 |
| `big_stat_manual`, `callout`, `quote` | 1 |
| `side_by_side`, `before_after` | 2 |
| `three_column` | 3 |
| `four_card` (4 cards) | 4 |
| `kpi_dashboard` | 1 per metric card |
| `section_divider` | 1 (optional) |
| `content_table`, `matrix`, `numbered_list` | 0 |

---

## 5. Typography and Emphasis

### Bold
- Bold for: **key numbers**, **decision points**, **names**, **action items**, the single most important phrase per slide
- Bold NOT for: entire paragraphs, headers that are already visually distinct
- **Bold budget:** Max 3-5 bold items per slide

### Italics
- Italics for: quotes within body text, titles of documents/reports, terms on first use
- Italics NOT for: long passages, anything scanned quickly
- Rule: bold = "important", italics = "different"

### Color as emphasis
- **Primary color:** structural elements — headers, labels, dividers, names (set in `brand.yaml` `colors.primary`)
- **Secondary/accent color:** accent — hero numbers in `big_stat`, key stats, decorative marks (set in `brand.yaml` `colors.secondary`)
- **Green/Amber/Red:** status meaning only, never decorative
- **Dark text color:** body text (set in `brand.yaml` `colors.text_dark`)
- **Gray:** supporting/secondary text (set in `brand.yaml` `colors.text_gray`)
- Max **4 color families** per slide

### Font size by context
- **Projected presentations** (spoken): nothing below 18pt body
- **Read-along decks** (sent as PDF/Slides): 10-14pt body is acceptable
- Current builder range (8-14pt) is designed for read-along. For projected, use `big_stat`, `callout`, and `quote` layouts which use 18-72pt.

### Font floor (hard rule)
- **7pt absolute minimum** — nothing below this, ever. QA flags as error.
- **9pt warning threshold** — body text below 9pt is flagged as warning (except table cells and footnotes).
- If content requires smaller text, split into two slides instead.

*Corpus finding: some decks hit 5pt in budget tables and org charts. This is unreadable and should be caught by QA.*

### Non-brand font tolerance
- **Brand fonts** (defined in `brand.yaml` `fonts.heading` and `fonts.body`) should be used for all new content.
- **Non-brand fonts** may appear in imported slides from Google Slides exports and shared templates. QA warns but does not error on non-brand fonts in imported slides.

---

## 6. Content Density Rules

### The 65% rule
Content should never fill more than 65% of the slide area. The remaining 35% is whitespace that gives the content breathing room and perceived importance.

*Corpus validation: average content density across 921 slides is 60.8% — the company naturally stays near this guideline.*

### Words per slide by audience

| Audience | Max words/slide | Max bullets | Headline max |
|----------|----------------|-------------|--------------|
| C-Suite | 50 | 4 | 12 words |
| Customer/Partner | 75 | 5 | 15 words |
| Middle Management | 100 | 6 | 15 words |
| Individual Contributor | 150 | 8 | 20 words |

### Data table exception (operational decks)
Operational slides that are fundamentally tabular (budget tables, OKR grids, issue trackers, status matrices) may exceed the 65% density rule and word limits. These slides must still enforce:
- **7pt font floor** (no exceptions)
- **Alternating row shading** or clear row separators for readability
- **Bold column headers** with brand primary color background
- **Max 200 words** — beyond 200, split into multiple slides or link to a spreadsheet

*Corpus finding: 25% of slides in the corpus are fundamentally tabular. Denying this reality doesn't improve them — enforcing readability does.*

### The split decision
**Two clear slides beat one crammed slide.** When content approaches the limit, split rather than shrink font or reduce whitespace.

- **200+ words on a single slide** → mandatory split recommendation
- **Font forced below 9pt** → split instead of shrink
- **More than 6 rows in a table** → consider splitting or using appendix

See `layout-limits.json` for per-layout maximums.

---

## 7. Structural Elements

- **Section dividers** between every 3-5 content slides to chunk information
- **Agenda** slide near the start so the audience knows the journey
- **Recap slides** after every 5-7 slides for long decks (use `callout` with key takeaway so far)
- **Bookend technique:** opening question in `callout` → content → closing answer in `callout`
- **Number sections** (01, 02, 03) for orientation

---

## 8. Company Patterns

Patterns observed across 52 presentations (921 slides). These reflect how the company actually communicates and should be supported by the builder.

### Status card format
A repeating convention in status/update decks. Structured fields on a single slide:

| Field | Content |
|-------|---------|
| **Owner** | Name and team |
| **Lifecycle Phase** | Discovery / Build / Deploy / Maintain |
| **Status** | On Track / At Risk / Blocked (with RAG color) |
| **Key Actions** | 2-4 bullet points of completed/in-progress work |
| **Blockers** | Active blockers with owners |
| **Next Steps** | 2-3 items with dates |
| **Decision Required** | Yes/No — if yes, state the decision clearly |

Use `content_table` or a custom status layout. This pattern appears in parking quality, migration status, and project status decks.

### Photo headshots in team/org slides
Many decks heavily feature employee headshot photos in org charts, team slides, and quarterly planning intros. When building team or org slides:
- Use circular or rounded-rectangle photo frames
- Size photos consistently (1-1.5" for team grids, 0.8-1" for org charts)
- Always pair with name and role text
- Use the `side_by_side` or custom grid layouts for team presentations

### Product screenshots
When present, app screenshots and UI mockups are the most effective visual elements in the corpus. For product/feature slides:
- Use `side_by_side` with text on the left, screenshot on the right
- Screenshots add credibility and visual interest — prefer real UI over diagrams
- Size screenshots to fill 40-50% of the slide

### Interactive/placeholder slides
Some slides are intentionally empty or minimal — Q&A tables, discussion prompts, status report covers. These are valid slide types meant to be filled during live meetings. The builder should support:
- Q&A tables (empty table with Slide/Member/Question/Answer headers)
- Discussion prompt slides (single question or topic as headline, blank body)

---

## 9. Slide Sequence Templates

### Strategy Recommendation (C-Suite, 10 slides)
```yaml
1. title_cover: "Cloud Migration — Strategic Recommendation"
2. callout: "We recommend dual-cloud with GCP as primary and AWS for existing workloads"
3. section_divider: "01 — Why Now"
4. kpi_dashboard: "Infrastructure costs grow 23% annually without migration"
5. before_after: "On-premise vs cloud-native infrastructure"
6. section_divider: "02 — The Plan"
7. roadmap: "Migration completes EOY 2026 with partner execution"
8. numbered_list: "Three decisions required this quarter"
9. status_board: "Current program health across all workstreams"
10. closing: "Questions?"
```

### Quarterly Business Review (Middle Management, 15 slides)
```yaml
1. title_cover
2. agenda
3. kpi_dashboard: "Q1 metrics — 3 on track, 1 at risk, 1 blocked"
4. status_board: "Workstream health dashboard"
5. section_divider: "01 — Accomplishments"
6. three_column: "Three key deliverables completed this quarter"
7. section_divider: "02 — Risks & Blockers"
8. status_board: "Two items require escalation"
9. content_table: "Risk register with owners and mitigations"
10. section_divider: "03 — Next Quarter"
11. roadmap: "Q2 delivery plan"
12. numbered_list: "Five priorities for the next 90 days"
13. matrix: "RACI for Q2 workstreams"
14. callout: "The one thing we need to get right: partner onboarding by April 15"
15. closing
```

### Customer/Partner Pitch (12 slides)
```yaml
1. title_cover: "Platform Engineering — Technology Partnership"
2. big_stat_manual: "300M+ parking transactions processed annually"
3. three_column: "Three platform capabilities"
4. section_divider: "01 — The Opportunity"
5. before_after: "Current parking experience vs connected experience"
6. kpi_dashboard: "Market metrics — size, growth, penetration"
7. section_divider: "02 — Our Approach"
8. roadmap: "Integration timeline and milestones"
9. four_card: "Four deployment options"
10. quote: "Testimonial from existing partner"
11. numbered_list: "Next steps to get started"
12. closing: "Let's Connect"
```

### Operational Status Update (Operational, 8-12 slides)
```yaml
meta:
  purpose: operational
  audience: middle-management

1. title_cover: "Parking Quality — March 2026 Status Report"
2. status_board: "Program Health Dashboard"
3. content_table: "Consolidated Top 10 Issues" (owner, ETA, progress, next steps)
4. content_table: "Blockers Requiring Escalation"
5. kpi_dashboard: "Key Metrics This Period"
6. roadmap: "Next 30/60/90 Day Plan"
7. numbered_list: "Decisions Required"
8. closing: "Q&A"
```

### Monthly Business Update (Operational, 15-25 slides)
```yaml
meta:
  purpose: operational
  audience: middle-management

1. title_cover: "Monthly Business Update — [Business Unit] — [Month]"
2. kpi_dashboard: "Executive KPIs"
3. content_table: "Financial Summary" (revenue, costs, margin)
4. section_divider: "Operations"
5. status_board: "Service Health"
6. content_table: "Incidents & Resolutions"
7. section_divider: "Product"
8. roadmap: "Feature Delivery Progress"
9. content_table: "Customer Feedback / Issues"
10. section_divider: "Team"
11. content_table: "Hiring & Capacity"
12. numbered_list: "Priorities Next Month"
13. callout: "Key Risk or Decision"
14. closing: "Q&A"
```
