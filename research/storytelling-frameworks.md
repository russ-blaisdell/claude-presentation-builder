# Storytelling Frameworks for Executive Presentations

> Part of the [Deck Builder](../README.md) research library. Synthesized into [Presentation Principles](../presentation-principles.md).
> Other research: [Visual Design](visual-design.md) | [Typography](typography-emphasis.md) | [Audience Profiles](audience-profiles.md)

Actionable structural patterns for a presentation-building AI. Each framework includes when to use it, a concrete slide sequence using deck builder layout names, headline examples in assertion style, and anti-patterns to avoid.

All layout references map to the 22 layouts in [presentation-guide.md](../presentation-guide.md). All headline examples follow the Assertion-Evidence model (full-sentence claims, not topic labels).

---

## Table of Contents

1. [The Minto Pyramid Principle (McKinsey Style)](#1-the-minto-pyramid-principle-mckinsey-style)
2. [Situation-Complication-Resolution (SCR)](#2-situation-complication-resolution-scr)
3. [Nancy Duarte's Sparkline Structure](#3-nancy-duartes-sparkline-structure)
4. [The Assertion-Evidence Model](#4-the-assertion-evidence-model)
5. [McKinsey/BCG Structural Patterns](#5-mckinseybcg-structural-patterns)
6. [Slide Density Research](#6-slide-density-research--what-actually-works)
7. [Structural Elements That Improve Comprehension](#7-structural-elements-that-improve-comprehension)
8. [Practical Slide Sequences for Common Scenarios](#8-practical-slide-sequences-for-common-scenarios)

---

## 1. The Minto Pyramid Principle (McKinsey Style)

### Core Concept

Barbara Minto's Pyramid Principle, developed at McKinsey in the 1960s and codified in her 1987 book, inverts the natural instinct to build up to a conclusion. Instead, you lead with the answer, then provide grouped supporting evidence. The audience knows the punchline from slide 2 and spends the remaining time being convinced rather than confused.

The SCQA variant structures the opening:
- **Situation:** An uncontroversial statement the audience already agrees with
- **Complication:** The thing that changed, the tension, the problem
- **Question:** The implicit question the audience now has (often unstated)
- **Answer:** Your recommendation, delivered immediately

The supporting evidence beneath the answer is organized into mutually exclusive, collectively exhaustive (MECE) groups -- typically 3, sometimes 2 or 4. Each group is itself a claim supported by data.

### When to Use

- **Audience:** C-suite, VP-level, board members, steering committees
- **Purpose:** Decision requests, investment cases, strategy recommendations, executive briefings
- **Timing:** When the audience has limited time (15-20 min) and needs to decide or approve something
- **Signal phrases from requestor:** "I need a recommendation on...", "What should we do about...", "Brief the leadership team on..."

### 10-Slide Sequence

| # | Layout | Headline Style | Purpose |
|---|--------|---------------|---------|
| 1 | `title_cover` | "Cloud Migration Strategy -- Recommendation to CTO" | Frame the topic |
| 2 | `callout` (boxed) | "We recommend migrating to AWS with GCP standby, saving $2.4M annually" | **The answer -- slide 2** |
| 3 | `section_divider` | "01 -- Why This Matters Now" | Transition to evidence group 1 |
| 4 | `kpi_dashboard` | "Current on-prem costs are growing 18% YoY while cloud pricing drops" | Evidence: the financial case |
| 5 | `before_after` | "Migration eliminates 3 single points of failure in our current architecture" | Evidence: the reliability case |
| 6 | `section_divider` | "02 -- How We Validated This" | Transition to evidence group 2 |
| 7 | `content_table` | "All three partners scored above threshold on security and compliance" | Evidence: vendor evaluation |
| 8 | `three_column` | "Three workstreams run in parallel to complete migration in 9 months" | Evidence: feasibility |
| 9 | `roadmap` | "Phase 1 delivers dev/test in 90 days with zero production risk" | The path forward |
| 10 | `closing` | "Questions?" | Close |

### Headline Examples

- BAD: "Cost Analysis" / GOOD: "Cloud migration saves $2.4M in year one and $3.1M by year three"
- BAD: "Vendor Comparison" / GOOD: "AWS scored highest across all five evaluation criteria"
- BAD: "Timeline" / GOOD: "All production workloads migrate by December 2026 with no downtime"
- BAD: "Risks" / GOOD: "Three identified risks are mitigated by the parallel-run strategy"

### Anti-Patterns

- **Building to the conclusion:** Putting the recommendation on slide 9 instead of slide 2. Executives will interrupt you at slide 4 asking "so what do you recommend?" and you will have lost control of the room.
- **Four or more evidence groups:** If you have more than 3 evidence groups, your argument is either not MECE or not synthesized enough. Combine or cut.
- **Evidence without a claim:** A slide that shows data without stating what the data means. Every evidence slide needs an assertion headline that tells the audience what to conclude.
- **Burying the ask:** If you need a decision or budget approval, it goes on slide 2 or 3, not in the appendix.
- **Topic-label headlines with Pyramid structure:** The whole point of the Pyramid is that headlines carry the argument. Topic labels ("Background", "Analysis", "Options") defeat the framework entirely.

---

## 2. Situation-Complication-Resolution (SCR)

### Core Concept

SCR is the oldest storytelling structure in rhetoric, tracing back to Aristotle's three-act structure. In business presentations, it works because it mirrors how humans naturally process change: here is what we knew, here is what disrupted it, here is what we should do about it.

The key insight is that the Complication section does the persuasive heavy lifting. If the audience does not feel the weight of the problem, they will not accept the cost of the solution. Spend 2-3 slides making the complication vivid and specific before offering the resolution.

**Structural pattern:**
- **Situation (1-2 slides):** Establish shared understanding. Use metrics, timelines, or architecture diagrams the audience already knows. This builds credibility ("they understand our world") and creates a baseline.
- **Complication (2-3 slides):** Introduce the disruption. This can be a market change, a technical debt crisis, a competitive threat, a regulatory shift, or internal dysfunction. Use data to make it concrete, not abstract. The complication should create urgency.
- **Resolution (3-5 slides):** Present the solution. Start with the "what" (the proposal), then the "how" (the plan), then the "proof" (evidence it will work). End with next steps.

### When to Use

- **Audience:** Any audience that needs to be persuaded, not just informed
- **Purpose:** Strategy proposals, change management, new initiative launches, budget requests, transformation programs
- **Timing:** When the audience does not yet agree there is a problem, or when you need buy-in before asking for resources
- **Signal phrases:** "We need to get alignment on...", "The team doesn't see why we need to change...", "I need to justify this investment..."

### 12-Slide Sequence

| # | Layout | Headline Style | Purpose |
|---|--------|---------------|---------|
| 1 | `title_cover` | "Securing Our Platform -- A New Approach to Identity Management" | Frame |
| 2 | `agenda` | 3 sections: Context, The Challenge, Our Path Forward | Roadmap |
| 3 | `section_divider` | "01 -- Where We Are Today" | **Situation begins** |
| 4 | `kpi_dashboard` | "Our IAM system handles 12M authentications daily across 4 identity domains" | Establish baseline |
| 5 | `content_diagram_text` | "Four separate identity systems serve consumer, corporate, M2M, and IoT" | Current architecture |
| 6 | `section_divider` | "02 -- What Changed" | **Complication begins** |
| 7 | `status_board` | "Three security audits in 2025 flagged identity fragmentation as critical risk" | The threat |
| 8 | `big_stat_manual` | "$4.2M" / "estimated annual cost of identity incidents and manual provisioning" | Make it visceral |
| 9 | `section_divider` | "03 -- The Path Forward" | **Resolution begins** |
| 10 | `callout` (boxed) | "A unified identity platform reduces risk exposure by 70% and saves $2.8M annually" | The proposal |
| 11 | `roadmap` | "Three phases deliver unified IAM in 12 months with zero service disruption" | The plan |
| 12 | `numbered_list` | "Three decisions needed this quarter to begin Phase 1" | Next steps |
| 13 | `closing` | "Questions?" | Close |

### Layout Mapping by Section

| SCR Phase | Best Layouts | Why |
|-----------|-------------|-----|
| Situation | `kpi_dashboard`, `content_diagram_text`, `content_two_col` | Metrics and architecture establish credible baseline |
| Complication | `status_board`, `big_stat_manual`, `before_after`, `callout` (open) | RAG status, alarming numbers, and contrast layouts create urgency |
| Resolution | `callout` (boxed), `three_column`, `roadmap`, `numbered_list` | Recommendation, plan pillars, timeline, and actions |

### Headline Examples

- Situation: "Platform engineering supports 47 teams across 6 countries today"
- Complication: "Developer onboarding takes 14 days -- 3x the industry benchmark"
- Complication: "Two production incidents in Q4 traced directly to identity misconfiguration"
- Resolution: "A self-service developer portal cuts onboarding to 2 days"
- Resolution: "Unified IAM eliminates the class of incidents that caused our Q4 outages"

### Anti-Patterns

- **Skipping the Situation:** Jumping straight to the problem. Without shared context, the audience questions whether you understand their world.
- **Weak Complication:** "Things could be better" is not a complication. "We will lose our SOC 2 certification in 6 months if we don't act" is a complication. Use specific data, dates, and consequences.
- **Complication without data:** Assertions of urgency without evidence. "Our security posture is concerning" vs. "Three of five audited systems failed penetration testing in January."
- **Resolution that doesn't match the Complication:** If the complication is about cost, the resolution must address cost. If the complication is about risk, the resolution must quantify risk reduction. Mismatched S-C-R breaks the narrative logic.
- **Too much Situation:** More than 2 slides of "here's what you already know" and the audience checks out. The Situation is table-setting, not the meal.

---

## 3. Nancy Duarte's Sparkline Structure

### Core Concept

Nancy Duarte's research (documented in "Resonate", 2010) analyzed hundreds of transformative presentations -- from Martin Luther King Jr.'s "I Have a Dream" to Steve Jobs's iPhone launch. She discovered a common structure she calls the "Sparkline": the presenter alternates between describing "what is" (current reality) and "what could be" (the envisioned future), creating dramatic tension that pulls the audience forward.

The pattern works because each oscillation between reality and possibility makes the gap feel more urgent and the future more desirable. The presentation ends with a "new bliss" -- a vivid picture of the transformed state that feels both inevitable and exciting.

**Structural rhythm:**
1. **What Is:** Current state (grounding)
2. **What Could Be:** A glimpse of the future (aspiration)
3. **What Is:** But here is why we are stuck (tension)
4. **What Could Be:** And here is how we break through (hope)
5. **What Is:** The cost of inaction (urgency)
6. **New Bliss:** The transformed future -- make it vivid, specific, and desirable

This structure is fundamentally emotional, not just logical. It works because humans are wired to resolve tension. Each "what is" creates dissatisfaction; each "what could be" offers relief. By the end, the audience wants the "new bliss" so badly they will accept the cost of getting there.

### When to Use

- **Audience:** Large groups, all-hands, partner meetings, board vision sessions, conference talks
- **Purpose:** Visionary presentations, transformation stories, culture change, platform launches, annual strategy
- **Timing:** When you need to inspire action, not just inform. When the audience needs to feel the future, not just understand the plan.
- **Signal phrases:** "I want to paint a picture of where we're going...", "We need people excited about this change...", "This is a keynote for..."

### 12-Slide Sequence

| # | Layout | Headline Style | Content Phase |
|---|--------|---------------|---------------|
| 1 | `title_cover` | "The Future of Platform Engineering at Acme Corp" | Frame |
| 2 | `kpi_dashboard` | "Today: 47 teams, 380 services, 14-day developer onboarding" | **What Is** (1) |
| 3 | `callout` (open) | "Imagine: a new engineer ships their first PR to production on day one" | **What Could Be** (1) |
| 4 | `before_after` | "Manual provisioning creates a 14-day bottleneck that blocks every new hire" | **What Is** (2) |
| 5 | `content_diagram_text` | "A self-service platform eliminates 11 of 14 manual onboarding steps" | **What Could Be** (2) |
| 6 | `big_stat_manual` | "2,100 hours" / "engineering hours lost to manual infrastructure requests last year" | **What Is** (3) |
| 7 | `three_column` | "Three platform capabilities that give engineers their time back" | **What Could Be** (3) |
| 8 | `status_board` | "Without change, we lose 3 more senior engineers to companies with modern platforms" | **What Is** (4) -- cost of inaction |
| 9 | `quote` | "I joined Acme Corp because I wanted to build products, not fight infrastructure" / -- Senior Engineer, Exit Interview | Emotional anchor |
| 10 | `roadmap` | "In 12 months, every engineer will have a self-service platform" | **New Bliss** -- the plan |
| 11 | `callout` (boxed) | "Day-one productivity, zero-ticket infrastructure, and engineers who choose to stay" | **New Bliss** -- the vision |
| 12 | `closing` | "Questions?" | Close |

### Layout Mapping by Phase

| Sparkline Phase | Best Layouts | Why |
|----------------|-------------|-----|
| What Is (reality) | `kpi_dashboard`, `before_after` (left side), `big_stat_manual`, `status_board` | Metrics and status communicate current-state friction |
| What Could Be (vision) | `callout` (open), `three_column`, `content_diagram_text`, `before_after` (right side) | Vision statements, capability showcases, and contrast layouts |
| New Bliss (ending) | `callout` (boxed), `roadmap`, `big_stat_manual` | Bold statements, concrete timelines, and impact numbers |

### Headline Examples

- What Is: "Developer satisfaction dropped 12 points in Q4 -- our lowest score in three years"
- What Could Be: "Companies with self-service platforms report 40% higher developer retention"
- What Is: "Every infrastructure change requires a ticket, a review, and a 3-day wait"
- What Could Be: "Policy-as-code lets teams ship infrastructure changes in minutes, not days"
- New Bliss: "By 2027, the company's platform will be the reason engineers join -- not the reason they leave"

### Anti-Patterns

- **All vision, no grounding:** If every slide is "what could be," the presentation feels like fantasy. The "what is" slides provide the gravity that makes the vision credible.
- **All problems, no hope:** If you stack too many "what is" slides without relief, the audience becomes hopeless or defensive. Alternate -- never more than 2 consecutive "what is" slides.
- **Vague "new bliss":** "Things will be better" is not a new bliss. "Every engineer ships to production on day one with zero tickets" is a new bliss. Make it concrete and measurable.
- **Using this framework for a decision request:** Sparkline is for inspiration and alignment, not for getting a yes/no on a budget request. Use Minto Pyramid or SCR for decisions.
- **Flat delivery:** This framework depends on contrast. If your "what is" and "what could be" slides look identical in layout and tone, the oscillation disappears. Use different layout types for each phase.

---

## 4. The Assertion-Evidence Model

### Core Concept

Developed by Michael Alley at Penn State (published in "The Craft of Scientific Presentations", 2003, and validated in multiple controlled studies), the Assertion-Evidence model makes one change that improves every presentation regardless of framework: replace topic-label headlines with full-sentence assertions.

**The rule:** Every slide headline is a complete declarative sentence that states the slide's main claim. The slide body provides visual evidence (charts, diagrams, images) that supports the assertion. If the audience reads only the headlines in order, they should understand the complete argument.

**Research findings:**
- Alley et al. (2006): Engineering students recalled 30% more information from assertion-evidence slides than from topic-label slides after a 24-hour delay.
- Garner & Alley (2013): Audience ratings of presenter credibility and slide effectiveness were significantly higher for assertion-evidence format.
- The effect is strongest when the body is visual (chart, diagram, photo) rather than bullet lists.

This is not a framework for structuring a deck -- it is a rule that applies within every framework. Minto Pyramid, SCR, Sparkline, and all McKinsey patterns become more effective when headlines carry assertions.

### When to Use

- **Always.** Every slide, every audience, every purpose.
- The only exception is structural slides (title covers, agendas, section dividers, closings) where a topic label is the convention.

### How to Implement in the Deck Builder

When generating slide YAML, the AI should:

1. **Write the headline as a full-sentence assertion first**, then choose the layout that best presents evidence for that assertion.
2. **Test with the "headline-only read":** Export all headlines in order. If they tell a coherent story, the deck works. If not, revise.
3. **Avoid noun-phrase headlines** on content slides: "Migration Timeline", "Cost Summary", "Team Structure" are all topic labels. Convert each to: "All workloads migrate by December 2026", "Migration saves $2.4M in year one", "Three new teams own the migration end-to-end."

### Conversion Examples

| Topic Label (BAD) | Assertion (GOOD) |
|-------------------|------------------|
| "Q4 Results" | "Q4 revenue exceeded target by 12% driven by enterprise growth" |
| "Security Posture" | "Three critical vulnerabilities remain unpatched after 90 days" |
| "Architecture Overview" | "The current architecture has a single point of failure in the auth layer" |
| "Team Structure" | "Nine engineering managers across six countries cover all platform domains" |
| "Cloud Costs" | "Cloud spend decreased 15% after rightsizing compute instances in November" |
| "Migration Risks" | "The database migration carries the highest risk due to schema incompatibility" |
| "Developer Experience" | "Developers spend 30% of their time on infrastructure instead of product features" |
| "Partner Evaluation" | "Google Cloud Partner scored highest on both technical depth and company alignment" |
| "Next Steps" | "Three actions this quarter unlock the full migration timeline" |
| "Recommendations" | "We should adopt AWS as primary cloud with GCP for disaster recovery" |

### Anti-Patterns

- **Assertion without evidence:** A headline that claims something the slide body does not support. If the headline says "Migration saves $2.4M," the body must show the math.
- **Assertion that is too vague:** "Things are improving" is technically an assertion but not a useful one. Be specific: "Deployment frequency increased 3x since adopting CI/CD in October."
- **Multiple assertions per slide:** Each slide gets one claim. If you have two assertions, you need two slides.
- **Assertion on structural slides:** Title covers, agendas, section dividers, and closings are exempt. These use conventional topic framing.
- **Forgetting the "so what":** "We have 47 teams" is a fact, not an assertion. "Our 47 teams share no common platform, causing $4M in duplicated tooling" is an assertion with a "so what."

---

## 5. McKinsey/BCG Structural Patterns

### The Ghost Deck

Before writing any slide content, outline the entire deck using only headlines. This is the "ghost deck" -- a skeleton that reveals the narrative logic before any evidence is created.

**How to implement:**
1. Write 10-15 assertion headlines in a list
2. Read them in order -- do they tell a complete, logical story?
3. Rearrange until the flow is airtight
4. Only then choose layouts and fill in body content

**Example ghost deck for a cloud migration recommendation:**
1. "the company's on-prem infrastructure costs are growing 18% annually"
2. "Cloud providers now offer equivalent capabilities at 40% lower TCO"
3. "Three of five competitors completed cloud migration in the last 18 months"
4. "Staying on-prem increases our cost disadvantage by $3M per year"
5. "We recommend migrating to AWS with GCP disaster recovery"
6. "AWS scored highest across all five evaluation criteria"
7. "GCP provides geographic redundancy at minimal incremental cost"
8. "Three parallel workstreams complete migration in 9 months"
9. "Phase 1 delivers dev/test in 90 days with zero production risk"
10. "Three decisions this quarter unlock the full migration"

### Horizontal Logic

**Definition:** Reading only the headlines of every slide tells the complete story from start to finish. No slide body content is needed to follow the argument.

**Test:** Cover up all slide bodies. Read just the headlines. Does the story make sense? Are there gaps? Does the conclusion follow from the evidence?

**Implementation rule for the deck builder:** After generating a deck, extract all headlines into a sequential list. Review this list as a standalone document. If any headline is a topic label, convert it. If any logical gap exists, add a slide.

### Vertical Logic

**Definition:** On each individual slide, the body content directly proves or supports the headline assertion. Nothing in the body is irrelevant to the headline; nothing needed for the proof is missing.

**Test:** For each slide, ask: "Does this body content prove the headline?" If the headline says "AWS scored highest across all five criteria," the body must show a comparison table with scores. A paragraph about AWS's market position fails the vertical logic test.

**Implementation rule for the deck builder:** After choosing a layout for a slide, verify that the body content fields (bullets, stats, diagrams, tables) contain evidence that directly supports the headline assertion.

### The "So What" Test

Every slide must answer: "So what does this mean for us?" If a slide presents data or information without connecting it to the audience's situation, it fails.

**Examples:**
- FAILS: "Cloud market grew 29% in 2025" (so what?)
- PASSES: "Cloud market grew 29% in 2025 -- our on-prem strategy is increasingly out of step with the industry"
- FAILS: "We evaluated three vendors" (so what?)
- PASSES: "Our evaluation of three vendors shows a clear winner on both cost and capability"

### Typical McKinsey/BCG Deck Structure

| Section | Slides | Purpose | Layouts |
|---------|--------|---------|---------|
| Context | 2-3 | Establish the landscape the audience needs to understand | `kpi_dashboard`, `content_diagram_text`, `before_after` |
| Analysis | 5-8 | Present the evidence that supports the recommendation | `content_table`, `three_column`, `side_by_side`, `status_board`, `matrix` |
| Recommendation | 2-3 | State the recommendation and its key pillars | `callout`, `three_column`, `numbered_list` |
| Next steps | 1-2 | Concrete actions, owners, and timelines | `numbered_list`, `roadmap` |

### 12-Slide Sequence (Consulting-Style Strategy Deck)

| # | Layout | Headline | Section |
|---|--------|----------|---------|
| 1 | `title_cover` | "Platform Strategy 2026 -- Recommendation to Technology Board" | Open |
| 2 | `agenda` | 4 items: Context, Analysis, Recommendation, Next Steps | Roadmap |
| 3 | `kpi_dashboard` | "Platform engineering supports 380 services with a 14-day onboarding cycle" | Context |
| 4 | `before_after` | "Developer productivity is constrained by 6 manual processes that could be automated" | Context |
| 5 | `content_table` | "Benchmarking shows the company trails peers on 4 of 5 platform maturity indicators" | Analysis |
| 6 | `three_column` | "Three root causes drive 80% of developer friction: provisioning, CI/CD, and observability" | Analysis |
| 7 | `big_stat_manual` | "2,100 hrs" / "engineering hours lost to manual infrastructure requests annually" | Analysis |
| 8 | `side_by_side` | "Internal platform team costs $1.2M annually but saves $4.1M in recovered productivity" | Analysis |
| 9 | `callout` (boxed) | "Invest in a self-service internal developer platform with three priority capabilities" | Recommendation |
| 10 | `numbered_list` | "Three capabilities deliver 80% of the value: service catalog, CI/CD templates, and environment provisioning" | Recommendation |
| 11 | `roadmap` | "Phase 1 delivers the service catalog in Q2, enabling self-service for 15 teams" | Next steps |
| 12 | `numbered_list` | "Three decisions needed by April 15 to begin Phase 1" | Next steps |
| 13 | `closing` | "Questions?" | Close |

### Anti-Patterns

- **No ghost deck:** Writing slides one-by-one without first outlining the headline story. This produces decks that meander.
- **Broken horizontal logic:** Headlines that require the body to make sense. If a headline says "Key Findings" the horizontal logic is broken because the reader cannot know what the findings are.
- **Broken vertical logic:** Body content that is tangential to the headline. A slide headlined "AWS scored highest" with body content about Azure's market share fails vertical logic.
- **Missing "so what":** Presenting facts without interpretation. Every fact must connect to the audience's decision or situation.
- **Too many analysis slides:** More than 8 analysis slides and the audience loses the thread. Synthesize more aggressively or move detail to an appendix.
- **No recommendation section:** Analysis decks that end with "here are the options" without stating a preference. The audience hired you (or you are presenting) to recommend, not to list.

---

## 6. Slide Density Research -- What Actually Works

### The Fundamental Split: Spoken vs. Read Presentations

The single most important factor in slide density is whether the deck will be presented live (with a speaker) or read asynchronously (emailed, shared as a document). These are fundamentally different media with different optimal densities.

| Dimension | Spoken (presented live) | Read (sent as document) |
|-----------|------------------------|------------------------|
| Words per slide | 15-40 | 75-150 |
| Primary content | Visual + speaker voice | Text on slide |
| Headline style | Short assertion (1 line) | Full assertion (1-2 lines) |
| Body content | Chart, diagram, image, key stats | Paragraphs, detailed bullets, tables |
| Slide count | More slides, less per slide | Fewer slides, more per slide |
| TED Talk equivalent | 1 idea, 1 visual | N/A |
| Amazon equivalent | N/A | 6-page narrative memo |

### Research Findings on Optimal Density

**Mayer's Cognitive Load Theory (2001, 2009):** Working memory processes about 4 chunks of new information at a time. Slides with more than 4 distinct ideas force the audience to choose what to ignore. For spoken presentations, the speaker's voice is one channel and the visual is another -- they must reinforce, not compete.

**Atkinson & Mayer (2004):** The "redundancy principle" -- presenting identical information in both spoken and written form simultaneously actually reduces learning. Slides should show what you cannot say (data, visuals), not a transcript of what you are saying.

**Kosslyn's "Clear and to the Point" (2007):** Stephen Kosslyn, Harvard psychologist, found that audiences process slides best when they contain one clear focal point. Multiple equal-weight elements create "visual competition" that degrades comprehension.

**Practical guidelines by context:**

| Context | Target density | Rationale |
|---------|---------------|-----------|
| C-suite briefing (spoken, 15 min) | 20-30 words/slide, 8-12 slides | Time-constrained, decision-oriented, speaker carries the story |
| All-hands / keynote (spoken, 30-45 min) | 10-20 words/slide, 25-40 slides | Inspirational, rapid pacing, visuals dominate |
| Architecture review (spoken, 45-60 min) | 30-50 words/slide, 15-25 slides | Technical depth, diagrams need annotation |
| Steering committee read-ahead (read) | 75-120 words/slide, 10-15 slides | Must stand alone, replaces a written brief |
| Board package (read) | 100-150 words/slide, 15-25 slides | Reference document, read before meeting |

### The Billboard Test

Can someone understand the main point of the slide in 3 seconds? If not, the slide is too dense for spoken delivery. This test applies to the headline + the primary visual element, not the fine print.

**Implementation for the deck builder:** After generating a slide, check: is the headline under 15 words? Is there one dominant visual element (chart, stat, diagram)? If the answer to both is yes, the slide passes the billboard test for spoken delivery.

### When Dense Narrative Decks Are Appropriate

The Amazon 6-pager model (written narrative, read in silence before discussion) has a presentation equivalent: the "pre-read deck." These decks are designed to be read asynchronously and are not presented slide-by-slide.

**Characteristics of read-optimized decks:**
- Headlines are full assertions (2 lines acceptable)
- Body uses paragraphs or detailed bullets, not single keywords
- Tables and data are annotated with inline interpretation
- Speaker notes are empty (the slide is the complete communication)
- Layout favors text-heavy formats: `side_by_side`, `numbered_list`, `content_table`, `content_two_col`

**Characteristics of spoken-optimized decks:**
- Headlines are short assertions (1 line)
- Body is visual: charts, diagrams, icons, images, stats
- Detailed context lives in speaker notes
- Layout favors visual formats: `big_stat_manual`, `kpi_dashboard`, `before_after`, `content_diagram_text`, `image_showcase`

### Anti-Patterns

- **Death by bullet points:** Slides with 8+ bullet points in small font, read verbatim by the speaker. This violates the redundancy principle and bores the audience.
- **Inconsistent density:** Some slides with 10 words, others with 150. The audience cannot adapt their processing speed. Pick a density range and stay within it.
- **Dense slides presented as spoken:** Emailing a "read-ahead" deck and then reading it aloud in a meeting. Either redesign for spoken delivery or have people read in silence first (the Amazon model).
- **Sparse slides sent as read-ahead:** A deck of single-word slides emailed to stakeholders who were not in the room. Without the speaker's voice, the slides are meaningless. Add full annotations or switch to a narrative format.
- **Ignoring speaker notes:** For spoken decks, the detail belongs in speaker notes, not crammed onto the slide. The deck builder supports `notes:` on every slide for this purpose.

---

## 7. Structural Elements That Improve Comprehension

### Section Dividers with Numbers

**Research basis:** Miller's chunking theory (1956) -- information grouped into labeled chunks is easier to store and retrieve. Section dividers create explicit chunks.

**When to use:** Any deck longer than 7 slides. Place a section divider before each major content group. Use the `section_divider` layout with `section_number` (01, 02, 03) and a headline that previews the section's content.

**Rules:**
- Number sections sequentially (01, 02, 03)
- The section headline should preview what the audience will learn in that section
- 2-5 slides per section (fewer than 2 means the section is not needed; more than 5 means it should be split)
- Total sections: 3-5 for a 12-slide deck, 5-7 for a 20-slide deck

**Implementation in YAML:**
```yaml
- layout: section_divider
  section_number: "02"
  headline: "What We Found"
  subheader: "Analysis of three migration approaches"
  background: "purple"
  icon: "search-analytics"
```

### Progress Indicators

The audience should always know where they are in the presentation. Two approaches:

1. **Agenda with highlights:** Show the agenda slide at the beginning, then repeat it before each section with the current section highlighted (via a modified `agenda` slide or `section_divider`).
2. **Section numbers in dividers:** The numbered section divider approach (above) implicitly communicates progress: "02 of 04" tells the audience they are 50% through.

**Implementation note:** The deck builder's `section_divider` layout with `section_number` provides built-in progress signaling. Use it consistently.

### Recap Slides

**Research basis:** Ebbinghaus's forgetting curve (1885) -- information not reinforced is lost rapidly. A brief recap after every 5-7 content slides reinforces the key points before introducing new material.

**When to use:**
- Decks longer than 12 slides
- Technical presentations where each section builds on the previous one
- Any presentation where the audience must retain earlier points to understand later ones

**Implementation:** Use a `callout` (open style) after each major section:
```yaml
- layout: callout
  callout_text: "Key takeaway: migration to AWS reduces cost by 40% and eliminates three single points of failure"
  supporting_text: "This sets the stage for our recommendation on timeline and phasing."
  icon: "lightbulb"
  style: "open"
```

Alternatively, use a `numbered_list` to recap the top 3 points from the section just completed.

### The Bookend Technique

Open with a provocative question or striking statement. Deliver all content. Close by answering the opening question or completing the opening statement. This creates a satisfying narrative arc.

**Example:**
- Slide 2 (after title): `callout` (open) -- "What if every engineer at Acme Corp could ship to production on their first day?"
- Slides 3-11: All evidence and proposal
- Slide 12 (before closing): `callout` (boxed) -- "With this platform investment, every engineer will ship to production on day one -- starting Q3 2026."

**Implementation pattern:**
1. Open with an open-style callout containing a question or bold claim
2. Deliver the deck content
3. Close with a boxed callout that answers the question or validates the claim, now with evidence behind it

### The "One Slide, One Idea" Rule

Resist the urge to put two ideas on one slide. Splitting content across two slides (even if each feels "light") is always better than cramming two ideas onto one. Slides are free; audience attention is not.

**How to enforce:**
- Each slide's headline contains exactly one assertion
- If you find yourself using "and" or "also" in a headline, split into two slides
- If a slide has two diagrams or two data tables, split into two slides

### Transition Phrases in Speaker Notes

For spoken presentations, the deck builder should generate transition phrases in speaker notes that connect slides:

- "Now that we've seen the problem, let's look at the solution..."
- "This brings us to the critical question..."
- "Building on this analysis, we can now recommend..."
- "The data points to three key themes..."

These belong in the `notes:` field, not on the slide itself.

---

## 8. Practical Slide Sequences for Common Scenarios

### Scenario A: Strategy Recommendation to C-Suite

**Framework:** Minto Pyramid (lead with the answer)
**Audience:** CTO, VP Engineering, CFO
**Duration:** 15-20 minutes spoken
**Density:** 20-30 words per content slide

| # | Layout | Headline | Notes |
|---|--------|----------|-------|
| 1 | `title_cover` | "Cloud Migration Strategy -- Recommendation to Technology Board" | |
| 2 | `callout` (boxed) | "We recommend AWS as primary cloud with GCP standby, delivering $2.4M annual savings" | **The answer, slide 2** |
| 3 | `kpi_dashboard` | "On-prem costs grew 18% YoY while cloud pricing dropped 12% in the same period" | Evidence: financial pressure |
| 4 | `before_after` | "Cloud migration eliminates 3 single points of failure and reduces RTO from 4 hours to 15 minutes" | Evidence: reliability |
| 5 | `content_table` | "AWS scored highest across all five evaluation criteria; GCP was strongest on data analytics" | Evidence: vendor selection |
| 6 | `three_column` | "Three parallel workstreams -- infrastructure, data, and applications -- complete migration in 9 months" | Evidence: feasibility |
| 7 | `roadmap` | "Phase 1 migrates dev/test in 90 days; production follows in Phase 2 with parallel-run" | Timeline |
| 8 | `status_board` | "All three risks are mitigated: data gravity solved by hybrid sync, compliance by pre-certification, skills by partner engagement" | Risk management |
| 9 | `big_stat_manual` | "$2.4M" / "net annual savings after migration, growing to $3.1M by year three" | Impact |
| 10 | `numbered_list` | "Three decisions needed by April 15: approve budget, select partner, assign migration lead" | Call to action |
| 11 | `closing` | "Questions?" | |

### Scenario B: Project Kickoff for Cross-Functional Team

**Framework:** SCR (establish context, explain why now, lay out the plan)
**Audience:** Engineering leads, product managers, architects from multiple teams
**Duration:** 30-45 minutes spoken
**Density:** 25-40 words per content slide

| # | Layout | Headline | Notes |
|---|--------|----------|-------|
| 1 | `title_cover` | "Project Phoenix -- Federated Authentication for B2B/B2G" | |
| 2 | `agenda` | 5 items: Why Now, Scope, Architecture, Team & Roles, Timeline | |
| 3 | `section_divider` | "01 -- Why Now" | |
| 4 | `kpi_dashboard` | "Acme Corp serves 12 enterprise clients today, each requiring custom SSO integration" | Situation: current state |
| 5 | `big_stat_manual` | "6 weeks" / "average time to onboard a new enterprise client due to identity integration" | Complication: the bottleneck |
| 6 | `callout` (boxed) | "Federated auth reduces enterprise onboarding from 6 weeks to 3 days" | Resolution: the promise |
| 7 | `section_divider` | "02 -- What We're Building" | |
| 8 | `content_diagram_text` | "A standards-based identity broker sits between company services and enterprise IdPs" | Architecture |
| 9 | `side_by_side` | "Phase 1 delivers SAML/OIDC federation; Phase 2 adds SCIM provisioning and MFA policies" | Scope |
| 10 | `section_divider` | "03 -- How We'll Work" | |
| 11 | `matrix` | "RACI: IAM team owns delivery, Platform provides infrastructure, Security reviews compliance" | Roles |
| 12 | `roadmap` | "Three milestones: POC in April, pilot client in June, GA in September" | Timeline |
| 13 | `numbered_list` | "Five actions this week: architecture review, dev environment setup, security threat model, pilot client selection, daily standup schedule" | Immediate actions |
| 14 | `closing` | "Questions?" | |

### Scenario C: Quarterly Business Review

**Framework:** McKinsey structure (context, analysis, recommendation, next steps)
**Audience:** CTO, VP Engineering, peer leaders
**Duration:** 30 minutes spoken + 15 min discussion
**Density:** 25-35 words per content slide

| # | Layout | Headline | Notes |
|---|--------|----------|-------|
| 1 | `title_cover` | "DevXP Quarterly Business Review -- Q1 2026" | |
| 2 | `kpi_dashboard` | "Q1 summary: 14 of 16 OKRs on track, cloud spend down 12%, developer satisfaction up 8 points" | Executive summary |
| 3 | `status_board` | "All six programs green except IAM (amber, timeline risk) and SRE transition (red, blocked on hiring)" | Program health |
| 4 | `section_divider` | "01 -- Wins and Progress" | |
| 5 | `three_column` | "Three major deliverables shipped: developer portal v2, CI/CD standard pipeline, and fleet census" | Key wins |
| 6 | `big_stat_manual` | "47%" / "reduction in production incidents attributed to improved CI/CD guardrails" | Impact metric |
| 7 | `section_divider` | "02 -- Risks and Blockers" | |
| 8 | `side_by_side` | "IAM timeline at risk due to vendor delay; SRE transition blocked by 2 unfilled positions" | Two risks in detail |
| 9 | `before_after` | "Proposed mitigation: parallel vendor track for IAM, contractor bridge for SRE positions" | Mitigation plan |
| 10 | `section_divider` | "03 -- Q2 Plan" | |
| 11 | `roadmap` | "Q2 focuses on cloud migration Phase 1, IAM POC, and completing the SRE transition" | Forward-looking plan |
| 12 | `numbered_list` | "Three asks: approve 2 contractor positions, escalate vendor timeline, fund cloud migration Phase 1" | Decisions needed |
| 13 | `closing` | "Questions?" | |

### Scenario D: Technical Architecture Review

**Framework:** SCR + Assertion-Evidence (problem-driven architecture presentation)
**Audience:** Architects, senior engineers, engineering leadership
**Duration:** 45-60 minutes spoken with discussion
**Density:** 30-50 words per content slide

| # | Layout | Headline | Notes |
|---|--------|----------|-------|
| 1 | `title_cover` | "Multi-Cloud Architecture -- Technical Design Review" | |
| 2 | `agenda` | 6 items: Current State, Requirements, Architecture Options, Recommended Design, Migration Path, Open Questions | |
| 3 | `content_diagram_text` | "Today's architecture runs entirely on AWS with a single-region active-passive setup" | Current state diagram |
| 4 | `kpi_dashboard` | "Current setup: 99.95% uptime, 4-hour RTO, $890K monthly compute, 380 services" | Current metrics |
| 5 | `status_board` | "Single-region deployment creates 3 unmitigated failure modes affecting all 380 services" | Problem statement |
| 6 | `side_by_side` | "Requirements: sub-15-minute RTO, geographic redundancy, and no single-cloud vendor lock-in" | Requirements |
| 7 | `section_divider` | "01 -- Architecture Options" | |
| 8 | `content_table` | "Option B (AWS primary + GCP standby) scores highest on cost, resilience, and operational complexity" | Options comparison |
| 9 | `content_diagram_text` | "Recommended architecture: active AWS with warm GCP standby using YugabyteDB for data replication" | Target architecture |
| 10 | `three_column` | "Three key design decisions: database layer (YugabyteDB), networking (Cloud Interconnect), and identity (cross-cloud IAM)" | Design decisions |
| 11 | `section_divider` | "02 -- Migration Path" | |
| 12 | `roadmap` | "Six-month migration: infrastructure in months 1-2, stateless services in 3-4, stateful in 5-6" | Migration timeline |
| 13 | `numbered_list` | "Five open questions for the review board: data residency policy, GCP account structure, failover SLA, budget allocation, team ownership" | Open questions |
| 14 | `closing` | "Questions?" | |

### Scenario E: Customer/Partner Pitch

**Framework:** Sparkline (alternate between their current pain and your solution's future)
**Audience:** Prospective partner, customer executive team
**Duration:** 20-30 minutes spoken
**Density:** 15-25 words per content slide (visual-heavy, speaker carries the narrative)

| # | Layout | Headline | Notes |
|---|--------|----------|-------|
| 1 | `title_cover` | "Acme Corp + Google Cloud -- Parking Intelligence for the AI Era" | |
| 2 | `kpi_dashboard` | "Acme Corp manages 1.2M parking spaces across 4,000 locations in 47 states" | Establish credibility |
| 3 | `callout` (open) | "What if drivers could find, book, and pay for parking with a single voice command?" | **What Could Be** |
| 4 | `before_after` | "Today: drivers search 3 apps and spend 17 minutes finding parking in urban areas" | **What Is** -- the pain |
| 5 | `content_diagram_text` | "the company's MCP server connects real-time parking data to Google's Gemini voice assistant" | **What Could Be** -- the solution |
| 6 | `big_stat_manual` | "17 min" / "average time urban drivers spend searching for parking -- we reduce this to under 2 minutes" | **What Is** -- quantified pain |
| 7 | `three_column` | "Three capabilities: real-time availability, dynamic pricing, and seamless payment -- all via voice" | **What Could Be** -- capabilities |
| 8 | `quote` | "The best parking experience is the one you don't think about" / -- Company Vision Statement | Emotional anchor |
| 9 | `roadmap` | "POC in April, pilot with 50 locations in June, full rollout by September" | **New Bliss** -- the plan |
| 10 | `numbered_list` | "Three partnership elements: API access, co-marketing, and shared analytics" | Partnership terms |
| 11 | `callout` (boxed) | "Together, Acme Corp and Google Cloud make parking invisible -- every driver, every city, every time" | **New Bliss** -- the vision |
| 12 | `closing` | "Questions?" | |

### Scenario F: Status Update for Steering Committee

**Framework:** Minto Pyramid variant (lead with status summary, then exceptions only)
**Audience:** Steering committee (senior leadership overseeing multiple programs)
**Duration:** 10-15 minutes spoken
**Density:** 25-35 words per content slide

| # | Layout | Headline | Notes |
|---|--------|----------|-------|
| 1 | `title_cover` | "Cloud Migration -- Steering Committee Update, March 2026" | |
| 2 | `status_board` | "Overall program status: green -- Phase 1 complete, Phase 2 on track, no budget overruns" | **Lead with the answer** |
| 3 | `kpi_dashboard` | "Phase 1 delivered: 42 dev/test workloads migrated, $180K monthly savings realized, zero incidents" | Key metrics |
| 4 | `roadmap` | "Phase 2 is 30% complete: production migration began March 1 and tracks to June 15 completion" | Timeline status |
| 5 | `side_by_side` | "One risk elevated to amber: database migration delayed 2 weeks due to schema compatibility testing" | Exception reporting |
| 6 | `callout` (boxed) | "Mitigation: parallel schema conversion reduces delay to 1 week; no impact to Phase 2 end date" | Resolution |
| 7 | `numbered_list` | "Two items for steering committee: approve Phase 3 budget ($420K) and confirm GCP disaster recovery scope" | Decisions needed |
| 8 | `closing` | "Questions?" | |

**Key principle for steering committee updates:** Short. Lead with overall status. Only elaborate on exceptions (items that are not green). End with specific asks. Steering committees oversee many programs -- respect their time by focusing on what needs their attention.

---

## Framework Selection Guide

Use this decision tree to choose a framework:

```
Is the audience making a decision today?
  YES --> Minto Pyramid (lead with recommendation)
  NO  --> Continue...

Do you need to persuade the audience that a problem exists?
  YES --> SCR (make the complication vivid)
  NO  --> Continue...

Is this a vision/transformation/inspiration presentation?
  YES --> Sparkline (alternate what-is / what-could-be)
  NO  --> Continue...

Is this a regular status/review cadence?
  YES --> McKinsey structure (context, analysis, recommendation, next steps)
  NO  --> Use any framework, but ALWAYS use Assertion-Evidence headlines
```

**Frameworks can be combined:**
- Minto Pyramid + Assertion-Evidence = the default for any executive briefing
- SCR + Sparkline = powerful for change management (SCR structure with Sparkline emotional beats)
- McKinsey structure + Assertion-Evidence + recap slides = the standard for any deck over 12 slides

---

## Implementation Notes for the Deck Builder

### Headline Generation Rules

1. **Content slides:** Always generate full-sentence assertion headlines. Never use topic labels.
2. **Structural slides:** Use conventional framing (title covers, agendas, section dividers, closings are exempt from assertion rule).
3. **Headline length:** Target 10-15 words for spoken decks, up to 20 words for read-ahead decks.
4. **Headline test:** After generating all slides, extract headlines into a list. Read sequentially. If the story is clear without any body content, the horizontal logic passes.

### Layout Selection by Narrative Role

| Narrative Role | Primary Layouts | Secondary Layouts |
|---------------|----------------|-------------------|
| Establish baseline | `kpi_dashboard`, `content_two_col` | `content_table`, `content_diagram_text` |
| Highlight a problem | `big_stat_manual`, `status_board` | `before_after` (left side emphasized), `callout` (open) |
| Present evidence | `content_table`, `three_column`, `side_by_side` | `matrix`, `content_diagram_text` |
| Make a recommendation | `callout` (boxed) | `numbered_list`, `big_stat_manual` |
| Show transformation | `before_after` | `content_diagram_text`, `callout` |
| Present a plan | `roadmap`, `numbered_list` | `funnel`, `matrix` |
| Inspire / envision | `callout` (open), `quote`, `big_stat_manual` | `image_showcase` |
| Request action | `numbered_list` | `callout` (boxed), `status_board` |
| Show progress/health | `status_board`, `kpi_dashboard` | `roadmap` |
| Create a break | `section_divider` | `quote` |

### Framework-to-Template Mapping

When the deck builder receives a request, it should select a framework and corresponding template:

| Request Type | Framework | Starting Template |
|-------------|-----------|-------------------|
| "Recommend X to leadership" | Minto Pyramid | Executive Presentation |
| "Get buy-in for X" | SCR | Executive Presentation (modified) |
| "Present the vision for X" | Sparkline | Custom (no template -- build from scratch) |
| "Architecture review for X" | SCR + McKinsey | Technical / Architecture |
| "Quarterly review" | McKinsey | Status / Update |
| "Steering committee update" | Minto Pyramid (short) | Status / Update (trimmed) |
| "Partner/customer pitch" | Sparkline | Custom |
| "Project kickoff" | SCR | Executive Presentation (modified) |

### Quality Checklist (Post-Generation)

Before delivering any deck, verify:

- [ ] **Horizontal logic:** Headlines read sequentially tell the complete story
- [ ] **Vertical logic:** Each slide's body proves its headline
- [ ] **So-what test:** Every slide answers "so what does this mean?"
- [ ] **Billboard test:** Each slide's main point is graspable in 3 seconds (spoken decks)
- [ ] **Density match:** Word count matches the delivery context (spoken vs. read)
- [ ] **Section structure:** Dividers chunk content into 3-5 logical groups
- [ ] **Assertion headlines:** No topic labels on content slides
- [ ] **Bookend check:** Opening and closing slides have narrative coherence
- [ ] **Framework consistency:** The chosen framework's structure is followed throughout, not mixed arbitrarily
- [ ] **Call to action:** The deck ends with specific, actionable next steps (not just "Questions?")
