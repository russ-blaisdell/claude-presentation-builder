# Visual Design Principles for Executive Presentations

> Part of the [Deck Builder](../README.md) research library. Synthesized into [Presentation Principles](../presentation-principles.md).
> Other research: [Typography](typography-emphasis.md) | [Audience Profiles](audience-profiles.md) | [Storytelling Frameworks](storytelling-frameworks.md)

Actionable rules for the deck builder. Every rule is numbered and testable. Where a rule maps to an existing QA check or builder parameter, that is noted.

---

## 1. Icons — When They Help vs. When They Hurt

### The Recognition Test

**Rule 1.1 — The one-second recognition test.** Before placing an icon, ask: "Can the audience identify the concept this icon represents within one second, without reading the adjacent text?" If no, remove the icon.

- GOOD: A padlock icon beside a section titled "Security Posture" — the audience knows the topic before reading a word.
- GOOD: A server-stack icon in a KPI card showing "1,300 VMs" — reinforces what the number measures.
- BAD: A generic "star" icon beside "Migration Timeline" — a star does not map to time or migration. The icon is decoration.
- BAD: A "heart" icon beside "Platform Reliability" — hearts suggest sentiment, not reliability.

**Rule 1.2 — Every icon must map to a concrete noun or universally understood concept.** Icons work for objects (server, building, person, calendar, lock, cloud) and a small set of abstract concepts with strong conventional mappings (checkmark = done, warning triangle = risk, magnifying glass = search). Icons do not work for verbs, adjectives, or complex ideas like "strategic alignment" or "cross-functional coordination."

**Rule 1.3 — If two icons on the same slide could be swapped without the audience noticing, at least one is decorative. Remove it.**

### When to Use Icons

**Rule 1.4 — Use icons to categorize.** Place an icon beside a section title or card header when the icon tells the audience what domain the content belongs to before they read the text. Examples:

| Section Title | Icon | Why It Works |
|---------------|------|--------------|
| Security Assessment | padlock | Universal security symbol |
| Cloud Infrastructure | cloud-server | Maps to cloud computing |
| Cost Management | coin-stacks | Maps to money/finance |
| Team Structure | people | Maps to people/organization |
| Timeline | calendar-day | Maps to dates and scheduling |

**Rule 1.5 — Use icons in KPI cards and stat blocks to identify what the metric measures.** A number alone ("1,300") is ambiguous. A number with an icon (server-stack + "1,300") becomes self-documenting. This is the highest-value use of icons in executive decks.

**Rule 1.6 — Use icons in status boards and RAG displays for visual scanning.** When an audience scans a grid of project statuses, icons (green checkmark, amber warning, red X) are processed faster than colored text.

**Rule 1.7 — Use icons in agenda slides to give each item a visual anchor.** Numbered agenda items benefit from a small icon to the left of each item — it helps the audience locate items when the presenter refers back ("let's jump to the security section").

### When NOT to Use Icons

**Rule 1.8 — Do not use icons when they do not map to a clear, specific concept.** If you cannot describe what the icon represents in two words or fewer, do not use it.

- BAD: A "merge-arrows" icon beside "Next Steps" — merge arrows suggest code merging or convergence, not action items.
- BAD: A "presentation-chart" icon beside "Risk Assessment" — charts do not represent risk.

**Rule 1.9 — Do not use icons purely to fill visual space.** A text block with no icon is better than a text block with an irrelevant icon. Empty space communicates "this is a straightforward point." A random icon communicates "I decorated this slide."

**Rule 1.10 — Do not use icons when text is already short and scannable.** A three-item bulleted list with clear labels ("Phase 1: Discovery," "Phase 2: Migration," "Phase 3: Optimization") does not need icons. The text is already scannable.

### Icon Density Rules

**Rule 1.11 — Maximum icon count by layout type:**

| Layout | Max Icons | Rationale |
|--------|-----------|-----------|
| title_cover | 0 | Full-bleed image, no content icons |
| agenda | 7 | One per agenda item (up to 7 items) |
| content_two_col (stacked) | 5 | 3 stat icons + 2 section icons |
| side_by_side | 2 | One per column |
| three_column | 3 | One per column |
| four_card | 4 | One per card |
| big_stat_manual | 1 | One beside the stat |
| kpi_dashboard | 8 | One per metric card (max 8 cards) |
| status_board | 1 per row | Status indicator per item |
| before_after | 2 | One per panel |
| section_divider | 1 | Topic icon |
| closing | 0 | No content |

**Rule 1.12 — If a slide has more than 6 content icons (excluding status indicators), it is too dense. Split the content across two slides.**

**Rule 1.13 — The squint test.** Blur your eyes or view the slide at 25% zoom. You should still be able to identify the slide's structure — how many sections, where the visual weight sits, what the layout is. If icons create a scattered pattern of pink dots that obscures the structure, reduce icon count or increase spacing.

**Rule 1.14 — Icons should reinforce the visual hierarchy, not compete with it.** Icons should be secondary to headlines and stat numbers. If an icon draws the eye before the headline, it is too large or too prominent. In the the system, icons at 0.35-0.45 inches serve as visual anchors without dominating.

---

## 2. Images — When to Use vs. When to Skip

### Full-Bleed Images

**Rule 2.1 — Full-bleed background images are reserved for title_cover, closing, and image_showcase layouts only.** Never place a photograph or full-slide image behind content text on a working slide. The text becomes unreadable, the image becomes invisible, and both are degraded.

**Rule 2.2 — Background images on title/closing slides must be low-contrast or overlaid with a semi-transparent gradient.** Brand title assets are pre-treated for this. Custom images must be darkened or overlaid so white/pink text passes a 4.5:1 contrast ratio.

### Diagrams

**Rule 2.3 — If you are explaining a relationship, flow, hierarchy, or process, use a diagram. Always.** Text descriptions of system architecture, organizational structures, migration flows, or decision trees are cognitively expensive. A diagram communicates spatial relationships that sentences cannot.

- GOOD: An architecture diagram showing AWS and GCP regions with arrows between services.
- BAD: A bullet list saying "Service A calls Service B, which queries Database C, which replicates to Database D."

**Rule 2.4 — Diagrams must carry structured data, not be abstract art.** Every box, arrow, and label in a diagram must represent a real entity or relationship. Decorative diagrams with vague boxes labeled "Innovation" connected to "Growth" are worse than no diagram.

**Rule 2.5 — Choose the diagram type that matches the data structure:**

| Data Structure | Diagram Type | Native Renderer |
|----------------|-------------|----------------------|
| Reporting chain, org tree | org-hierarchy | Yes |
| Step-by-step process | flow, process-steps | Yes |
| Two options with tradeoffs | comparison | Yes |
| Milestones over time | timeline | Yes |
| Metrics with targets | key-stats | Yes |
| Categories with items | labeled-boxes | Yes |
| Complex architecture | draw.io or AI-generated | Via diagram pipeline |

**Rule 2.6 — Size diagrams to the content they contain.** A 3-box flow diagram should not fill a full slide. A 20-node architecture diagram probably needs a full slide. Use the split ratio system (v-70/30 for diagram-heavy, v-30/70 for text-heavy) to allocate space proportionally.

### Photos

**Rule 2.7 — Photos in executive decks must carry specific, irreplaceable meaning.** Use a photo only when:
- It shows a real thing the audience needs to see (a data center being decommissioned, a product interface, a physical location).
- No diagram, icon, or text could convey the same information.

Do not use photos for "vibes." A stock photo of people shaking hands beside a "Partnership" slide adds zero information.

**Rule 2.8 — The "would a blank space work better?" test.** Before placing any image, ask: "If I removed this image and left the space empty, would the slide communicate less effectively?" If the answer is no, remove the image. Empty space is not a problem to solve — it is a design tool (see Section 3).

**Rule 2.9 — Never use stock photography in executive-level decks presented internally.** Internal audiences recognize stock photos instantly. They signal that the presenter prioritized decoration over substance. External-facing marketing decks have different rules.

### AI-Generated Images

**Rule 2.10 — AI-generated images (Imagen, DALL-E, etc.) follow the same rules as photos.** They must carry meaning. "A futuristic cloud infrastructure" is decoration. A diagram of the actual target architecture is information. The visual quality of AI images does not exempt them from the "does this carry meaning?" test.

**Rule 2.11 — AI-generated images must pass the Gemini multimodal review loop.** Check for: text legibility (AI images often garble text), dimensional accuracy (correct aspect ratio for the slot), and brand alignment (colors match brand tokens).

---

## 3. Whitespace as Communication

### Whitespace and Perceived Importance

**Rule 3.1 — More whitespace around an element increases its perceived importance.** A single stat centered on a slide with generous margins ("1,300+ VMs") communicates "this number matters" more forcefully than the same number crammed into a busy grid. This is the principle behind the big_stat_manual layout.

**Rule 3.2 — Whitespace is not wasted space. It is a signal that says "pause here" or "this is the main point."** A slide with ample margins and breathing room signals confidence and executive-level communication. A slide packed edge-to-edge signals "I could not decide what to cut."

### Content Density by Audience

**Rule 3.3 — Adjust density to audience seniority:**

| Audience | Density | Words per Slide | Items per Slide | Whitespace % |
|----------|---------|----------------|-----------------|-------------|
| C-suite / Board | Sparse | 25-40 | 3-5 | 50-60% |
| VP / Director | Moderate | 40-60 | 5-7 | 40-50% |
| Manager / IC | Dense (acceptable) | 60-80 | 7-10 | 30-40% |
| Workshop / Reference | Very dense | 80-120 | 10+ | 20-30% |

**Rule 3.4 — The default for Acme Corp executive decks is "Moderate" density (VP/Director level).** Russ's primary audiences are CTO-level leadership, VPs, and engineering directors. Err toward less content, not more.

### The Breathing Room Rule

**Rule 3.5 — Content must never fill more than 65% of the slide area.** The remaining 35%+ is margins, gutters, and intentional whitespace. In the company's 10" x 5.625" canvas:

| Zone | Dimensions | Purpose |
|------|-----------|---------|
| Left margin | 0.5" | Breathing room from edge |
| Right margin | 0.5" | Breathing room from edge |
| Top (below headline) | 0.15" | Separation from headline |
| Bottom (above footer) | 0.2" | Separation from footer |
| Inter-column gutter | 0.25-0.4" | Visual separation between columns |
| Inter-section gap | 0.15-0.25" | Vertical separation between sections |

**Rule 3.6 — Gutters between columns must be at least 0.25 inches.** Narrower gutters cause adjacent text blocks to blur together visually. The audience cannot tell where one column ends and another begins.

### Splitting vs. Cramming

**Rule 3.7 — Two clear slides are always better than one crammed slide.** Splitting content costs the presenter 30 seconds of click time. Cramming costs the audience 30 seconds of decoding time multiplied by every person in the room. The math always favors splitting.

**Rule 3.8 — If you must reduce font size below 9pt to fit content, the slide has too much content.** Split it. The QA pipeline already flags fonts below 9pt as warnings and below 7pt as critical. These thresholds exist because text below 9pt is unreadable on a projected slide at typical conference room distances (8-15 feet from screen).

**Rule 3.9 — If adaptive font sizing triggers more than two reduction steps, stop and split the slide.** The adaptive sizing system (FONT_REDUCTION_STEPS) is a safety net, not a layout strategy. It handles marginal cases where content is 10% too long. If the system must shrink fonts twice, the content needs editing or splitting.

**Rule 3.10 — Horizontal scrolling in the audience's mind is forbidden.** If a slide has a wide table, dense matrix, or sprawling diagram that forces the eye to jump back and forth horizontally, split it or simplify. Executive audiences read top-to-bottom, left-to-right in a single visual sweep.

---

## 4. Cognitive Load Theory Applied to Slides

### Miller's Law (7 plus or minus 2)

**Rule 4.1 — No slide should present more than 7 discrete items for the audience to hold in working memory.** "Items" means: bullet points, cards, columns, KPI metrics, status rows, or any other repeated unit. At 5 items, comprehension is comfortable. At 7, it is effortful. At 9+, the audience stops tracking.

**Rule 4.2 — Practical item limits by layout:**

| Layout | Item Limit | Notes |
|--------|-----------|-------|
| agenda | 7 | Built-in limit, scales font for 6-7 items |
| three_column | 3 columns, 5 bullets each | 15 total sub-items is the ceiling |
| four_card | 4 cards, 4 bullets each | 16 total sub-items is the ceiling |
| kpi_dashboard | 8 metrics | 6 is better for readability |
| status_board | 8 rows | Beyond 8, split into two slides |
| numbered_list | 6 items | More than 6 becomes a wall of text |
| side_by_side | 2 columns, 6 bullets each | 12 total sub-items is the ceiling |

**Rule 4.3 — Group items into categories when count exceeds 5.** If you have 12 items, do not present 12 bullets. Group them into 3-4 categories of 3-4 items each. The audience remembers "3 categories" and can drill into each. This is chunking — the primary tool for managing cognitive load.

### The 6x6 Heuristic

**Rule 4.4 — Aim for a maximum of 6 bullet points per section, with a maximum of 10-12 words per bullet.** The classic "6x6 rule" (6 bullets, 6 words each) is too restrictive for technical content. Executive engineering decks need enough precision to be actionable. The adjusted rule: 6 bullets, 10-12 words each, with key terms bolded.

**Rule 4.5 — When to break the 6x6 heuristic:**
- Reference/workshop decks where the slide is a permanent artifact (not presented live)
- Detailed status boards where completeness matters more than scannability
- Appendix slides that serve as backup for Q&A

**Rule 4.6 — The word count guard rails are:**
- 30 words per text box: warning threshold (QA flags this)
- 50 words per text box: critical threshold (QA flags this)
- Entire slide: 80 words maximum for executive content, 120 for workshop/reference

### Dual Coding Theory

**Rule 4.7 — Text paired with a relevant visual is retained better than text alone.** When a slide says "Migration follows three phases," a simple three-stage flow diagram beside the text doubles retention. The text explains what; the diagram shows the structure.

**Rule 4.8 — Text paired with an irrelevant visual is retained worse than text alone.** A decorative stock photo beside a migration timeline actively harms comprehension. The audience spends cognitive cycles trying to connect the image to the content, fails, and loses both the image and the text.

This is the core of dual coding theory, and it is the most important visual design rule: **every visual element must either reinforce the text or be removed.**

**Rule 4.9 — The relevance hierarchy for visuals:**

| Visual Type | Cognitive Value | When to Use |
|-------------|----------------|-------------|
| Diagram showing structure | Highest | Whenever relationships, flows, or hierarchies exist |
| Chart showing data | High | Whenever quantitative comparison matters |
| Icon identifying a concept | Medium | To categorize and aid scanning |
| Photo of a real thing | Medium | Only when the thing itself matters |
| Decorative image | Negative | Never |
| Decorative icon | Negative | Never |

### Extraneous Cognitive Load

**Rule 4.10 — Every visual element the audience must process that does not contribute to understanding is harmful.** This includes: decorative borders, unnecessary gridlines, 3D effects on charts, drop shadows on text, gradient fills on content areas, and background patterns behind text.

**Rule 4.11 — Audit every element on a finished slide with this question: "If I remove this, does the audience lose information?" If not, remove it.** Apply this to:
- Decorative lines that do not separate content
- Icons that do not map to a concept
- Color variations that do not encode data
- Sub-headings that repeat the headline

**Rule 4.12 — Animations and transitions add extraneous load in executive settings.** For live presentations to senior leadership, slides should be static. No fly-ins, no fades, no progressive reveals. The content should be comprehensible the moment the slide appears. Animations imply the presenter does not trust the audience to read.

---

## 5. The "One Idea per Slide" Principle

### The Takeaway Rule

**Rule 5.1 — Every slide must have exactly one takeaway that can be stated in a single sentence.** If a presenter were forced to describe the slide in one sentence to someone who had not seen it, that sentence is the slide's purpose. If the presenter needs two sentences, the slide needs to be split.

**Rule 5.2 — The headline IS the takeaway.** Headlines should be assertions, not labels.

| BAD (label) | GOOD (assertion) |
|-------------|-----------------|
| "Overview" | "We need to migrate 1,300 VMs by EOY 2026" |
| "Architecture" | "Single-org GCP structure reduces operational overhead by 40%" |
| "Partner Evaluation" | "Three partners meet all criteria; recommend Rackspace" |
| "Risk Assessment" | "Datacenter lease expiry in Q3 is the critical-path risk" |
| "Next Steps" | "Three decisions needed by April 15 to stay on schedule" |

**Rule 5.3 — Exception: workshop and reference decks may use topic labels as headlines.** When a deck is a permanent reference artifact (architecture guide, onboarding material), topic labels ("Security Model," "Network Topology") help navigation. For executive presentations that are shown once, assertion headlines are mandatory.

**Rule 5.4 — Supporting content must prove or contextualize the headline.** Every bullet, stat, diagram, and icon on the slide must directly support the headline's claim. If a bullet does not relate to the headline, it belongs on a different slide.

- GOOD: Headline "Three decisions needed by April 15." Bullets list the three decisions with owners and deadlines. Every element supports the headline.
- BAD: Headline "Three decisions needed by April 15." Bullets list the three decisions, plus two FYI items about unrelated topics. The FYI items dilute the takeaway and belong on a separate "Status Updates" slide.

### The Split Decision

**Rule 5.5 — If you need to communicate two ideas, create two slides.** Common violations:

| One Slide (Bad) | Two Slides (Good) |
|-----------------|------------------|
| "Current State and Target Architecture" | Slide 1: "Current architecture has three scaling bottlenecks" / Slide 2: "Target architecture eliminates all three" |
| "Risks and Mitigations" | Slide 1: "Four risks threaten the EOY deadline" / Slide 2: "Each risk has a funded mitigation plan" |
| "Q1 Results and Q2 Plan" | Slide 1: "Q1 delivered 3 of 4 milestones on schedule" / Slide 2: "Q2 focuses on the deferred milestone plus two new ones" |

**Rule 5.6 — The before_after layout is a legitimate exception.** It presents two states (before and after) as a single idea: "transformation." The takeaway is the delta between the two panels, not either panel alone. This layout should be used when the contrast itself is the message.

**Rule 5.7 — Section dividers carry one "meta-idea": we are now entering a new topic.** They do not contain content. Their purpose is to reset the audience's mental context. Section dividers with dense body text defeat this purpose.

---

## 6. Color as Information, Not Decoration

### Brand Colors for Structure

**Rule 6.1 — Use brand colors to encode structural roles, consistently:**

| Color | Hex | Structural Role |
|-------|-----|----------------|
| Purple | #5F016F | Headlines, titles, primary labels, section dividers |
| Pink | #FF80D4 | Accent text, secondary emphasis, stat numbers, icons |
| Light pink | #FFADE4 | Tertiary accent, icon variant |
| Light bg | #F0E8F5 | Card backgrounds, highlighted regions |
| White | #FFFFFF | Slide background, text on dark backgrounds |
| Dark gray | #333333 | Body text, secondary information |
| Medium gray | #888888 | Tertiary text, captions, footnotes |

**Rule 6.2 — Never use brand colors for semantic meaning.** Purple does not mean "good." Pink does not mean "warning." Brand colors are for structure only. This keeps semantic colors unambiguous (see Rule 6.3).

### Semantic Colors for Meaning

**Rule 6.3 — Semantic colors encode exactly one meaning each:**

| Color | Hex | Meaning | Use In |
|-------|-----|---------|--------|
| Green | #4EC98B | Good / On track / Complete | Status boards, KPI trends, RAG indicators |
| Amber/Yellow | #FFD766 | Caution / At risk / Needs attention | Status boards, KPI trends, RAG indicators |
| Red | #E85D5D | Blocked / Off track / Critical | Status boards, KPI trends, RAG indicators |

**Rule 6.4 — Never use green, amber, or red for decoration.** If a card has a green background but the content is not "good/on track," the color misleads. Semantic colors must only appear when they encode a judgment about status.

**Rule 6.5 — The RAG (Red/Amber/Green) system must be consistent across every slide in a deck.** If green means "on track" on slide 5, it cannot mean "environment = production" on slide 8. Pick one semantic system and hold it.

### Color Limits

**Rule 6.6 — Maximum 4 distinct hue families per slide.** A "hue family" is a color and its tints/shades. the company's brand gives you two families (purple and pink). Adding green/amber/red for status gives you five families total, but only three appear on any single slide (brand structure + one or two semantic indicators).

| Slide Type | Typical Colors Used | Count |
|------------|-------------------|-------|
| Content (no status) | Purple, pink, dark gray, light bg | 4 |
| Status board | Purple, green, amber, red | 4 |
| KPI dashboard | Purple, pink, green/amber/red per metric | 4-5 (acceptable; the metrics provide context) |

**Rule 6.7 — If you need more than 4 hue families, you are encoding too many dimensions on one slide.** Simplify or split.

### Contrast for Readability

**Rule 6.8 — Minimum contrast ratios for text legibility (WCAG AA):**

| Text | Background | Minimum Ratio | Status |
|------|-----------|---------------|--------|
| Dark gray (#333) | White (#FFF) | 12.6:1 | Passes |
| Purple (#5F016F) | White (#FFF) | 11.3:1 | Passes |
| White (#FFF) | Purple (#5F016F) | 11.3:1 | Passes |
| Pink (#FF80D4) | White (#FFF) | 2.5:1 | FAILS for body text |
| Pink (#FF80D4) | Purple (#5F016F) | 4.6:1 | Passes for large text only |
| Dark gray (#333) | Light bg (#F0E8F5) | 8.9:1 | Passes |

**Rule 6.9 — Pink (#FF80D4) must never be used for body text on white backgrounds.** The contrast ratio is 2.5:1, far below the 4.5:1 minimum for normal text. Pink is acceptable for: large headlines (18pt+), accent elements (icons, stat numbers, decorative text where the information is also conveyed by position/context), and icon fills.

**Rule 6.10 — On purple backgrounds, use only white text.** Pink-on-purple is acceptable for large accents (24pt+) but not for body text.

**Rule 6.11 — Test all text legibility at projection distances.** A color combination that looks fine on a laptop screen at 18 inches may be unreadable projected at 10 feet. Default to high-contrast combinations (dark on light, white on dark) for any text the audience must read.

---

## Appendix A — Decision Checklist for Slide Authors

Use this checklist when composing each slide's YAML definition:

```
BEFORE adding an icon:
[ ] Does it map to a concrete noun or universally understood concept?
[ ] Would the audience recognize the concept in <1 second?
[ ] Is the slide under the icon density limit for its layout type?
[ ] Does removing it lose information?

BEFORE adding an image or diagram:
[ ] Does it carry meaning that text alone cannot convey?
[ ] Is it a diagram (relationships/flows), not decoration?
[ ] Would blank space work just as well?
[ ] Is it sized proportionally to its information density?

BEFORE finalizing content:
[ ] Can the entire slide's point be stated in one sentence?
[ ] Is the headline an assertion (not a label)?
[ ] Does every element on the slide support the headline?
[ ] Is the word count under 80 (executive) or 120 (workshop)?

BEFORE finalizing layout:
[ ] Are there 7 or fewer discrete items?
[ ] Is content density under 65% of slide area?
[ ] Are all fonts 9pt or above?
[ ] Are semantic colors used only for actual status encoding?
[ ] Does the slide pass the squint test?
```

## Appendix B — Mapping to Deck Builder QA Pipeline

These rules map to existing and proposed automated checks:

| Rule | QA Check | Status |
|------|----------|--------|
| 1.11 — Icon density limits | Count icons per slide by layout type | Proposed |
| 1.13 — Squint test | Visual proof renderer at 25% scale | Proposed |
| 3.5 — 65% content area limit | Calculate content footprint vs canvas | Proposed |
| 3.8 — Font floor at 9pt | `FONT_WARN_PT = 9` in qa_pipeline.py | Implemented |
| 3.8 — Font hard floor at 7pt | `FONT_FLOOR_PT = 7` in qa_pipeline.py | Implemented |
| 4.6 — Word count 30/50 | `WORD_COUNT_WARN = 30, WORD_COUNT_FLAG = 50` | Implemented |
| 6.8-6.9 — Contrast ratios | Check text color vs background color | Proposed |
| 6.5 — Consistent RAG usage | Cross-slide semantic color audit | Proposed |
| 5.2 — Assertion headlines | Detect label-only headlines (single noun/noun phrase) | Proposed |
| 4.1 — Item count limits | Count repeated elements per slide | Proposed |
