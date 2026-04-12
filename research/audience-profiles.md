# Audience Profiles for Presentation Building

> Part of the [Deck Builder](../README.md) research library. Synthesized into [Presentation Principles](../presentation-principles.md).
> Other research: [Visual Design](visual-design.md) | [Typography](typography-emphasis.md) | [Storytelling Frameworks](storytelling-frameworks.md)

Reference guide for the deck-builder AI. Use these profiles to select layouts, calibrate density, choose headline style, and set icon/color usage based on who will be in the room.

---

## Available Layouts (22)

For quick reference, every layout mentioned below maps to one of these builder functions:

| Layout key | Description |
|---|---|
| `title_cover` | Background image + two-line text overlay |
| `agenda` | Left image + numbered items + divider lines |
| `section_divider` | Purple/light/image bg, section number, headline, icon |
| `content_two_col` | Left stats graphic + right sections with icons + divider |
| `content_diagram_text` | Split layout with diagram and text columns |
| `side_by_side` | Two columns with icons, vertically centered |
| `three_column` | Headline + 3 titled columns with icons |
| `four_card` | Headline + 4 card blocks with light purple backgrounds |
| `big_stat_manual` | Large centered number with label and optional icon |
| `kpi_dashboard` | Grid of 2-8 metric cards with trends, targets, icons |
| `roadmap` | Gantt timeline with swimlanes, status bars, milestones |
| `before_after` | Two columns with center arrow, transformation layout |
| `numbered_list` | Large numbers + title/body with dividers |
| `status_board` | RAG colored circles + name + summary |
| `content_table` | Column/row data table |
| `matrix` | Color-coded cells with legend (RACI, etc.) |
| `funnel` | Progressively narrowing bars |
| `callout` | Boxed or open style key takeaway |
| `quote` | Decorative quotation mark, centered text, attribution |
| `image_showcase` | Full-slide image with caption and border |
| `closing` | "Questions?" with background image |
| `content_table_bullets` | Table with bullet-point cells |

---

## Profile 1: C-Suite / Board (CEO, CTO, CFO, Board Directors)

### How they process presentations

Executives scan, they do not read. They look at the headline, the biggest number on the slide, and the color of any status indicator. If those three things do not immediately tell them something useful, the slide has failed. They will interrupt with questions at any point, so every slide must stand on its own with zero context from the preceding slide.

Their core questions are always: What should we decide? What does it cost? What is the risk? What happens if we do nothing?

### What they need

- A strategic narrative with a clear recommendation
- Decisions framed as options with tradeoffs, not open-ended explorations
- Financial impact quantified in dollars, percentages, or time-to-value
- Risk stated plainly: what can go wrong, how likely, what is the mitigation
- Progress shown as RAG status, not detailed task lists

### What they do NOT want

- Technical architecture details (they trust you to get that right)
- Process steps or methodology explanations
- Team-level org charts or individual contributor names
- Slide after slide of "context setting" before getting to the point
- Jargon without definition (Nutanix AHV, K8s, IaC mean nothing to a CFO)

### Density and structure rules

| Parameter | Rule |
|---|---|
| Words per slide | 30-50 max. Fewer is better. |
| Words per text field | Headline: 8-12 words. Body fields: 15-25 words each. |
| Slide count | 8-12 slides for a 30-minute meeting. |
| Sections | No section dividers needed. The deck is short enough to flow. |
| Agenda slide | Optional. If included, 4-5 items maximum. |
| Bold text | Numbers and decisions only. Never bold entire sentences. |
| Color usage | Semantic only: green/amber/red for status. No decorative color. |
| Icons per slide | 0-2 max. Only for key concepts (money, time, risk). |
| Footnotes/sources | Move to appendix or omit entirely. |

### Preferred layouts

| Priority | Layout | When to use |
|---|---|---|
| Primary | `big_stat_manual` | Hero number that tells the story (cost, timeline, scale) |
| Primary | `callout` | The recommendation or key decision, boxed style |
| Primary | `kpi_dashboard` | 4-6 metrics showing program health at a glance |
| Primary | `status_board` | RAG dashboard for multi-workstream programs |
| Secondary | `before_after` | Transformation story: where we are vs. where we are going |
| Secondary | `roadmap` | Timeline with 3-5 milestones max, no granular tasks |
| Secondary | `numbered_list` | 3-5 recommended next steps (not 8-10) |
| Avoid | `content_table` | Too dense. Summarize the table into a callout or stat. |
| Avoid | `matrix` | RACI is a management tool, not a board tool. |
| Avoid | `content_diagram_text` | Architecture diagrams lose this audience. |
| Avoid | `content_two_col` | Stats + body text is too much to scan. Pick one. |

### Headline style

**Assertion headlines only.** Every headline must be a complete thought that a CEO can read without looking at the body text.

| Good headline | Bad headline | Why it fails |
|---|---|---|
| "Invest $2M now to exit 10 data centers by EOY" | "Cloud Migration Overview" | No point of view. No number. No action. |
| "Partner decision needed by April 10" | "Partner Evaluation Status" | Does not tell the CEO what to do. |
| "3 of 8 partners fail compliance check" | "Partner Compliance Review" | Buries the finding in the body text. |
| "Migration on track --- FinOps is the blocker" | "Program Health Dashboard" | Dashboard without a verdict. |

### Icon usage

- Use only for the single most important concept on a slide
- Acceptable icons: `coin-stacks` (cost), `clock` (time), `warning` (risk), `trophy` (win), `lightbulb` (recommendation)
- Never use icons as bullet decorators for executives
- On `big_stat_manual`, one icon reinforcing the stat is ideal
- On `kpi_dashboard`, icons per metric card are fine (they are small and functional)

### Good slide example

```yaml
- layout: callout
  callout_text: "Recommend Option A: single GCP organization under Engineering, saving $400K/year in governance overhead."
  supporting_text: "Simpler billing. Single security surface. IT concerns mitigated by cross-functional Security Platform Team."
  icon: "lightbulb"
  style: "boxed"
```

Why it works: One clear recommendation. Dollar figure. Three-word rationale bullets. The CEO can approve or challenge in 10 seconds.

### Bad slide example

```yaml
- layout: content_two_col
  headline: "GCP Organization Options"
  left_stats:
    - number: "Option A"
      label: "Single Org"
      icon: "gear"
    - number: "Option B"
      label: "Dual Org"
      icon: "gear"
  left_icon: "gear"
  left_title: "Architecture Comparison"
  left_body: |
    Option A uses a single GCP Organization managed by Engineering.
    Org-level changes are coordinated with IT. Folders include IT,
    Engineering Quarantine, Dev/Test, Staging, and Production.

    Option B uses two separate GCP Organizations: one for IT and
    one for Engineering. Each org manages its own policies, billing,
    and IAM independently.
  right_icon: "sliders"
  right_title: "Tradeoffs Analysis"
  right_body: |
    Option A Pros: Simpler billing, single security pane, easier sharing
    Option A Cons: Requires IT/Eng coordination for org changes

    Option B Pros: Complete isolation, independent governance
    Option B Cons: Duplicated security tooling, complex cross-org access
```

Why it fails: 120+ words. No recommendation. No cost difference. No clear action. The CEO has to read two full columns and synthesize the answer themselves. This is a middle-management slide shown to the wrong audience.

### The "elevator pitch" test

Cover the body text with your hand. Read only the headline. Does it tell the CEO something actionable? If not, rewrite the headline. Every slide must pass this test.

---

## Profile 2: Customers / External Partners

### How they process presentations

External audiences are evaluating you. They want to know: Can this company solve my problem? Are they credible? What specifically will I get? They will forward the deck to colleagues who were not in the room, so every slide must be self-explanatory without a presenter.

They are also comparing you to competitors. Differentiation must be obvious, not buried in fine print.

### What they need

- Value proposition framed around their pain, not your capabilities
- Credibility signals: numbers, references, certifications, scale
- Specifics about what affects them: timeline, deliverables, pricing model
- A clear "why us" differentiator
- Obvious next steps with dates and contact information

### What they do NOT want

- Internal jargon (team names, internal project codenames, org structure)
- Your internal metrics unless they demonstrate capability
- Org charts or reporting structures
- Vague promises without specifics ("world-class," "cutting-edge," "best-in-class")
- Slides that only make sense with a presenter talking over them

### Density and structure rules

| Parameter | Rule |
|---|---|
| Words per slide | 40-70. Clean but substantive enough to build trust. |
| Words per text field | Headline: 6-10 words. Body fields: 20-40 words each. |
| Slide count | 12-18 slides. Enough to share internally and stand alone. |
| Sections | Use section dividers for 3-4 major sections. |
| Agenda slide | Required. Sets expectations and shows professionalism. |
| Bold text | Key numbers, differentiators, and partner-specific benefits. |
| Color usage | Brand-consistent. Use brand primary/secondary palette throughout. Sparing accent color for emphasis. |
| Icons per slide | 2-4. Brand consistency matters. Icons should feel polished and intentional. |
| Footnotes/sources | Include sparingly for credibility ("Source: Gartner, 2026"). |

### Preferred layouts

| Priority | Layout | When to use |
|---|---|---|
| Primary | `title_cover` | Strong branded opening with clear value statement |
| Primary | `three_column` | Capabilities, service tiers, or option packages |
| Primary | `four_card` | Feature categories, solution components, or partner options |
| Primary | `roadmap` | Engagement timeline showing what happens when |
| Primary | `numbered_list` | Clear engagement process or next steps |
| Secondary | `quote` | Testimonial from a reference customer or executive sponsor |
| Secondary | `before_after` | Transformation story with quantified improvement |
| Secondary | `big_stat_manual` | Hero credential number (customers served, uptime, scale) |
| Secondary | `side_by_side` | "What you get" vs. "What we handle" |
| Secondary | `kpi_dashboard` | Track record metrics (uptime, customers, scale) |
| Avoid | `matrix` | Internal governance tool. Not for customers. |
| Avoid | `status_board` | Internal RAG status is not customer-facing. |
| Avoid | `content_two_col` | Stats-heavy layout feels internal. |
| Avoid | `funnel` | Internal pipeline visualization. Rarely customer-relevant. |

### Headline style

**Benefit-oriented headlines.** Frame everything in terms of what the customer gets, not what you do.

| Good headline | Bad headline | Why it fails |
|---|---|---|
| "Reduce parking search time by 40%" | "Parking Discovery Technology" | Feature label, not a benefit. |
| "Live in production within 90 days" | "Implementation Timeline" | Generic. Does not promise anything. |
| "12M monthly transactions with 99.97% uptime" | "Platform Performance" | Vague label hides the impressive numbers. |
| "Three engagement options from $50K" | "Pricing and Packages" | Misses the chance to lead with accessibility. |

### Icon usage

- Use consistently across capability/feature slides for visual rhythm
- Icons should reinforce the category, not decorate randomly
- On `three_column` and `four_card`, one icon per column/card is expected
- On `side_by_side`, one icon per side reinforces the contrast
- Avoid technical icons (database, server-stack) for non-technical audiences
- Preferred icons for customers: `circle-check`, `three-stars`, `trophy`, `clock`, `coin-stacks`, `team-celebrate`

### Good slide example

```yaml
- layout: three_column
  headline: "Three Ways We Accelerate Your Migration"
  col1_icon: "clock"
  col1_title: "90-Day Fast Track"
  col1_body: |
    Assessment to production in one quarter

    Proven wave methodology from 500+ migrations
    Pre-built runbooks for Nutanix AHV environments
  col2_icon: "padlock"
  col2_title: "Zero Compliance Gaps"
  col2_body: |
    ISO 27001, SOC 2 Type II, PCI-DSS certified

    Security controls deployed before first VM moves
    Your auditors get documentation on day one
  col3_icon: "coin-stacks"
  col3_title: "Fixed-Price Confidence"
  col3_body: |
    No surprise costs or open-ended timelines

    Milestone-based billing tied to VM counts
    RaMP program alignment maximizes your credits
```

Why it works: Benefit-first headline. Three clear differentiators. Each column leads with what the customer gets. Credibility numbers are woven in naturally. No internal jargon.

### Bad slide example

```yaml
- layout: content_two_col
  headline: "Our Migration Methodology"
  left_stats:
    - number: "6"
      label: "Internal Teams"
      icon: "team-network"
    - number: "147"
      label: "Runbook Templates"
      icon: "bullet-list"
  left_icon: "gear"
  left_title: "Internal Process"
  left_body: |
    Phase 1: Discovery sprint (Byron's security team reviews)
    Phase 2: Wave planning (Rafael's FinOps team models costs)
    Phase 3: Migration execution (Allan's SRE team monitors)
    Phase 4: Validation (Thomas's IAM team provisions access)
  right_icon: "checklist"
  right_title: "Quality Gates"
  right_body: |
    Gate 1: Architecture review board approval
    Gate 2: Security baseline deployment
    Gate 3: Cost model sign-off
    Gate 4: Production readiness review
```

Why it fails: Internal team names (Byron, Rafael, Allan, Thomas) mean nothing to a customer. "Internal Process" is literally labeled as internal. The customer does not care about your quality gates --- they care about whether they will get a working migration on time. This deck would embarrass you if forwarded to the customer's CTO.

### The "forward-to-my-boss" test

Print the deck. Remove the presenter. Hand it to someone who was not in the meeting. Can they understand the value proposition, timeline, and next steps? If any slide requires verbal explanation to make sense, rewrite it.

---

## Profile 3: Middle Management (Directors, Senior Managers)

### How they process presentations

Middle managers are operators. They need to leave the meeting knowing what to do, who is responsible, when it is due, and what resources they need. They can handle density and actually prefer it to vagueness --- but the density must be structured, scannable, and action-oriented.

They will use the deck as a reference document after the meeting. Slides will be screenshot and pasted into Slack, referenced in 1:1s, and used to delegate work to their teams.

### What they need

- Actionable plans with owners, dates, and dependencies
- Resource implications: headcount, budget, tooling, access
- Timelines with milestones they can put on their calendar
- RACI or ownership clarity for cross-functional work
- Risk registers with probability and mitigation plans
- Status dashboards they can use in their own staff meetings

### What they do NOT want

- Strategic narrative without execution specifics ("cloud-first vision" with no dates)
- Technical deep-dives into implementation details they will delegate
- Slides that look great but contain no actionable information
- Presentations that make a case for something already decided

### Density and structure rules

| Parameter | Rule |
|---|---|
| Words per slide | 50-90. Structured density is fine. |
| Words per text field | Headline: 8-15 words. Body fields: 25-50 words each. |
| Slide count | 15-25 slides. They need reference material. |
| Sections | Use section dividers for every major workstream or phase. |
| Agenda slide | Required. Include timing per section if the meeting is long. |
| Bold text | Owners, dates, decisions, and blockers. |
| Color usage | Semantic RAG for status. Purple accent for section differentiation. Light backgrounds for information density. |
| Icons per slide | 2-4. Functional icons that aid scanning (status, category). |
| Footnotes/sources | Include for dates, data sources, and caveats. |

### Preferred layouts

| Priority | Layout | When to use |
|---|---|---|
| Primary | `roadmap` | Detailed timeline with swimlanes, dependencies, milestones |
| Primary | `status_board` | RAG dashboard for program health reviews |
| Primary | `matrix` | RACI, responsibility mapping, evaluation scoring |
| Primary | `numbered_list` | Action items, decision frameworks, prioritized next steps |
| Primary | `content_table` | Comparison data, resource plans, schedule details |
| Secondary | `side_by_side` | Option comparison, current vs. proposed, gap analysis |
| Secondary | `three_column` | Workstream breakdowns, team responsibilities |
| Secondary | `before_after` | Process improvement with quantified delta |
| Secondary | `kpi_dashboard` | KPIs they track weekly |
| Secondary | `callout` | Key decision or blocker that needs escalation |
| Tertiary | `four_card` | Workstream summaries, initiative overview cards |
| Tertiary | `funnel` | Pipeline or conversion metrics |
| Avoid | `big_stat_manual` | Too sparse. Managers want the stat plus the breakdown. |
| Avoid | `quote` | Testimonials do not help operators plan. |

### Headline style

**Action-oriented headlines.** Tell the manager what needs to happen and when.

| Good headline | Bad headline | Why it fails |
|---|---|---|
| "Partner decision needed by April 10" | "Partner Evaluation Status" | No urgency. No date. No action verb. |
| "3 workstreams blocked on FinOps cost model" | "Program Dependencies" | Does not name the blocker or the count. |
| "RACI: Engineering owns infra, Security owns controls" | "Responsibility Matrix" | Generic label when the headline could deliver the key insight. |
| "Wave 1 starts May 1 --- 200 VMs in dev/test" | "Migration Wave Planning" | Vague topic label instead of specific commitment. |

### Icon usage

- Functional icons to aid scanning: `circle-check` (done), `warning` (risk), `clock` (deadline), `calendar-day` (date)
- Use status-indicating icons on `status_board` and `kpi_dashboard`
- On `three_column` and `side_by_side`, category icons help managers quickly identify which workstream they are looking at
- Avoid purely decorative icons --- every icon should encode information

### Good slide example

```yaml
- layout: roadmap
  headline: "Wave 1 kicks off May 1 --- 200 dev/test VMs to GCP"
  time_axis: ["Apr 2026", "May 2026", "Jun 2026", "Jul 2026", "Aug 2026"]
  swimlanes:
    - name: "Infrastructure"
      items:
        - label: "Landing zone ready"
          start: "Apr 2026"
          end: "Apr 2026"
          status: "active"
        - label: "Wave 1 migration"
          start: "May 2026"
          end: "Jul 2026"
          status: "planned"
    - name: "Security"
      items:
        - label: "Baseline controls"
          start: "Apr 2026"
          end: "May 2026"
          status: "active"
        - label: "Compliance validation"
          start: "Jun 2026"
          end: "Jul 2026"
          status: "planned"
    - name: "FinOps"
      items:
        - label: "Cost model + labels"
          start: "Apr 2026"
          end: "May 2026"
          status: "active"
  milestones:
    - date: "May 2026"
      label: "Wave 1 start"
    - date: "Aug 2026"
      label: "Wave 1 complete"
```

Why it works: Headline states the specific action, date, and scope. Three swimlanes show cross-functional dependencies. Milestones are calendar events a manager can plan around. Every bar has an owner (swimlane name) and a status.

### Bad slide example

```yaml
- layout: big_stat_manual
  headline: "Migration Scale"
  number: "1,300+"
  label: "Virtual machines will be migrated to the cloud as part of our multi-year transformation program"
  icon: "server-stack"
```

Why it fails: A manager already knows the scale. They need to know which 200 VMs are in Wave 1, who owns the migration, and when the landing zone will be ready. This slide delivers zero actionable information. It belongs in an executive deck where the number is news, not a planning deck where the number is table stakes.

### The "Monday morning" test

Read each slide on a Monday at 9 AM. Can you identify at least one specific thing to do this week based on this slide? If every slide passes, the deck is ready for middle management.

---

## Profile 4: Individual Contributors (Engineers, Analysts, Specialists)

### How they process presentations

ICs are the most demanding audience for accuracy and specificity. They will notice if a version number is wrong, if an architecture diagram omits a component, or if a comparison table leaves out a relevant dimension. They actually read every line. They process presentations as technical documents, not narratives.

They are not impressed by polish --- they are impressed by precision. A slide with correct technical details in plain text earns more respect than a beautifully designed slide with vague generalities.

### What they need

- Technical accuracy: correct version numbers, service names, API details
- Specific details: configuration parameters, migration paths, compatibility matrices
- Data to validate: benchmarks, test results, comparison tables with real numbers
- Architectural context: how components connect, what talks to what, data flow
- Enough detail to take action without asking follow-up questions

### What they do NOT want

- Vague strategy without implementation specifics
- Marketing language ("world-class," "next-generation," "best-in-class")
- Slides that restate what they already know to "set context"
- Oversimplified diagrams that hide important details
- Decisions presented without the supporting analysis

### Density and structure rules

| Parameter | Rule |
|---|---|
| Words per slide | 70-120. High density is expected and respected. |
| Words per text field | Headline: 10-18 words. Body fields: 40-70 words each. |
| Slide count | 20-30+ slides. Depth matters more than brevity. |
| Sections | Use section dividers for architectural domains or phases. |
| Agenda slide | Required. Include the full scope so ICs know what is covered. |
| Bold text | Technical terms, service names, version numbers, key parameters. |
| Color usage | Minimal. Use color to encode data (RAG, comparison winner) not to decorate. |
| Icons per slide | 0-1. Data and diagrams are more useful than icons. |
| Footnotes/sources | Expected. Link to docs, RFCs, benchmark sources, Jira tickets. |

### Preferred layouts

| Priority | Layout | When to use |
|---|---|---|
| Primary | `content_table` | Comparison matrices, compatibility tables, feature grids |
| Primary | `content_diagram_text` | Architecture diagrams with explanatory text |
| Primary | `content_table_bullets` | Detailed technical specifications with notes per row |
| Primary | `side_by_side` | Technology comparison (Option A vs. Option B with specifics) |
| Primary | `numbered_list` | Implementation steps, migration runbook, decision criteria |
| Secondary | `matrix` | Compatibility matrix, evaluation scoring, feature coverage |
| Secondary | `three_column` | Technology stack breakdown, component comparison |
| Secondary | `content_two_col` | Stats + detailed breakdown (engineers appreciate the data) |
| Secondary | `roadmap` | Detailed implementation timeline with dependencies |
| Tertiary | `status_board` | Component-level health (API latency, service status) |
| Tertiary | `kpi_dashboard` | Performance metrics with targets and trends |
| Avoid | `big_stat_manual` | Too sparse for an audience that wants the breakdown. |
| Avoid | `callout` | ICs want the analysis, not just the conclusion. |
| Avoid | `quote` | Testimonials are irrelevant to technical audiences. |
| Avoid | `funnel` | Business metric visualization, not technical content. |

### Headline style

**Descriptive and precise headlines.** Include the specific technology, version, or scope. ICs use headlines to decide if a slide is relevant to them.

| Good headline | Bad headline | Why it fails |
|---|---|---|
| "Nutanix AHV to GCP Compute Engine migration path" | "Migration Approach" | Does not name the source or target platform. |
| "AlloyDB vs. Cloud SQL: latency, cost, and HA comparison" | "Database Options" | Vague. ICs need to know which databases are compared. |
| "Landing zone Terraform modules: network, IAM, logging" | "Infrastructure as Code" | Does not specify the tool or the modules. |
| "K8s 1.28 compatibility matrix across all 10 DC environments" | "Kubernetes Compatibility" | Misses the version and scope that make it useful. |

### Icon usage

- Minimal or none. Icons are visual noise for technical audiences.
- If used, only for category differentiation on multi-column slides
- Never use icons as substitutes for data or diagrams
- On `content_diagram_text`, the diagram itself is the visual --- no additional icons needed
- Acceptable: `server-stack` or `cloud-network` on infrastructure slides for quick category identification

### Good slide example

```yaml
- layout: content_table
  headline: "Nutanix AHV to GCP Compute Engine --- VM type mapping"
  columns: ["AHV Config", "GCP Machine Type", "vCPUs", "RAM (GB)", "Monthly Cost", "Notes"]
  rows:
    - ["Small (2c/4GB)", "e2-medium", "2", "4", "$48", "Dev/test workloads"]
    - ["Medium (4c/8GB)", "e2-standard-4", "4", "16", "$97", "Most app servers"]
    - ["Large (8c/32GB)", "e2-standard-8", "8", "32", "$194", "Database servers"]
    - ["XL (16c/64GB)", "n2-standard-16", "16", "64", "$466", "Analytics, batch"]
    - ["GPU (4c/16GB+T4)", "g2-standard-4", "4", "16+T4", "$587", "ML inference"]
  notes: "Prices are us-central1 on-demand. CUD pricing reduces by 37-55%. Sole-tenant nodes available for PCI-DSS workloads at ~30% premium."
```

Why it works: Specific VM type mappings an engineer can use to plan. Cost per type. Notes column for edge cases. Footnote with pricing context and compliance callout. An engineer can start sizing VMs from this slide alone.

### Bad slide example

```yaml
- layout: before_after
  headline: "Infrastructure Transformation"
  before:
    label: "Current State"
    icon: "server-stack"
    items:
      - "On-premises data centers"
      - "Legacy virtual machines"
      - "Manual provisioning"
      - "Limited security baseline"
  after:
    label: "Target State"
    icon: "cloud-network"
    items:
      - "Multi-cloud platform"
      - "Container-first architecture"
      - "Automated provisioning"
      - "Unified security"
  arrow_label: "Migration"
```

Why it fails: Every bullet is a vague platitude. "Legacy virtual machines" tells an engineer nothing --- what hypervisor, what OS, what version? "Container-first architecture" --- which orchestrator, what runtime, what registry? "Automated provisioning" --- Terraform? Pulumi? Crossplane? This slide could describe any company's migration. ICs need specifics that are unique to this migration.

### The "can I implement from this?" test

After reading a slide, an IC should be able to take at least one concrete action: write a config, file a ticket, size a resource, or validate an assumption. If the slide only provides "awareness" with no actionable detail, it belongs in an executive deck, not a technical one.

---

## Profile 5: Mixed Audiences (All-hands, Town halls, Cross-functional reviews)

### How they process presentations

Mixed audiences are the hardest to serve because you have executives, managers, and ICs in the same room with fundamentally different needs. Executives will check out if you start with technical details. ICs will check out if you stay at the strategic level too long. Managers want the operational middle ground.

The solution is a layered structure that satisfies each audience in sequence.

### The layer cake approach

Structure the deck in three acts, with density increasing through each act. Executives get what they need in Act 1 and can leave (or stay and listen). Managers engage in Act 2. ICs take notes in Act 3.

| Act | Slides | Audience served | Density | Content |
|---|---|---|---|---|
| Act 1: Why | 3-5 slides | Executives | Sparse (30-50 words) | Strategic context, business case, key decision, headline metrics |
| Act 2: What | 6-10 slides | Managers | Medium (50-80 words) | Plan, timeline, ownership, resources, dependencies, status |
| Act 3: How | 5-15 slides | ICs | Dense (70-120 words) | Architecture, implementation, data, comparison tables, technical specs |
| Appendix | Variable | Reference | Maximum | Backup slides, detailed data, full tables, raw analysis |

### Structure rules

| Parameter | Rule |
|---|---|
| Total slide count | 20-35 slides across all acts, plus appendix. |
| Section dividers | Required between each act. Use `section_divider` with section numbers. |
| Agenda slide | Required. Show all three acts so every audience knows when their section comes. |
| Navigation | Number sections clearly ("01 Strategic Context", "02 Execution Plan", "03 Technical Detail") |
| Transition slides | Use `callout` between acts to signal the shift in depth. |

### Density by section

| Section | Words per slide | Preferred layouts |
|---|---|---|
| Act 1 (Why) | 30-50 | `big_stat_manual`, `callout`, `kpi_dashboard`, `before_after` |
| Act 2 (What) | 50-80 | `roadmap`, `status_board`, `numbered_list`, `three_column`, `side_by_side` |
| Act 3 (How) | 70-120 | `content_table`, `content_diagram_text`, `matrix`, `content_table_bullets` |
| Appendix | 80-150 | `content_table`, `matrix`, `content_diagram_text` |

### Preferred layouts by act

**Act 1 layouts:**

| Layout | Usage |
|---|---|
| `title_cover` | Opening with clear program name and date |
| `agenda` | Full agenda showing all three acts |
| `big_stat_manual` | Hero number that frames the scale or urgency |
| `callout` | The key recommendation or decision |
| `kpi_dashboard` | 4-6 headline metrics |
| `before_after` | Transformation narrative |

**Act 2 layouts:**

| Layout | Usage |
|---|---|
| `section_divider` | Transition into operational detail |
| `roadmap` | Timeline with swimlanes and milestones |
| `status_board` | RAG health for workstreams |
| `numbered_list` | Prioritized actions or decisions |
| `three_column` | Workstream or team breakdowns |
| `side_by_side` | Option comparison or gap analysis |
| `four_card` | Initiative summaries |

**Act 3 layouts:**

| Layout | Usage |
|---|---|
| `section_divider` | Transition into technical depth |
| `content_table` | Comparison matrices and data tables |
| `content_diagram_text` | Architecture with explanatory text |
| `matrix` | RACI, compatibility, scoring |
| `content_table_bullets` | Detailed specs with notes |
| `side_by_side` | Technical option comparison |

### Headline style by act

| Act | Style | Example |
|---|---|---|
| Act 1 | Assertion | "We should invest $2M to exit all data centers by December" |
| Act 2 | Action | "Three workstreams launch in parallel on May 1" |
| Act 3 | Descriptive | "VM type mapping: Nutanix AHV to GCP Compute Engine" |

### Icon usage by act

| Act | Icons per slide | Rule |
|---|---|---|
| Act 1 | 0-1 | Strategic emphasis only |
| Act 2 | 2-3 | Functional category indicators |
| Act 3 | 0-1 | Data over decoration |

### Good structure example

```yaml
slides:
  # --- ACT 1: WHY (Executives) ---
  - layout: title_cover
    headline: "Cloud Migration Program\nQ2 2026 Review"
    subheader: "Acme Corp | Engineering Leadership"
    background: "p12"

  - layout: agenda
    items:
      - "Strategic Context (5 min)"
      - "Program Health (5 min)"
      - "Execution Plan (10 min)"
      - "Architecture Deep Dive (10 min)"
      - "Next Steps & Discussion"

  - layout: big_stat_manual
    headline: "On track to exit 10 data centers by December"
    number: "67%"
    label: "of target VMs assessed and wave-planned"
    icon: "circle-check"

  - layout: callout
    callout_text: "Decision needed: add Wipro to GCP partner shortlist before April 10 deadline."
    supporting_text: "Wipro scored 4.74 --- highest of all 17 partners evaluated. None of the current GCP shortlist scored above 3.83."
    icon: "warning"
    style: "boxed"

  # --- ACT 2: WHAT (Managers) ---
  - layout: section_divider
    section_number: "02"
    headline: "Execution Plan"
    subheader: "Timelines, ownership, and dependencies"
    background: "purple"

  - layout: roadmap
    headline: "Wave 1 kicks off May 1 --- 200 dev/test VMs to GCP"
    # ... (detailed swimlanes and milestones)

  - layout: status_board
    headline: "5 workstreams: 3 green, 1 amber, 1 red"
    # ... (RAG items)

  - layout: matrix
    headline: "RACI --- Migration workstreams"
    # ... (responsibility matrix)

  # --- ACT 3: HOW (ICs) ---
  - layout: section_divider
    section_number: "03"
    headline: "Technical Detail"
    subheader: "Architecture, VM mapping, and configuration"
    background: "purple"

  - layout: content_diagram_text
    headline: "GCP landing zone architecture with folder hierarchy"
    # ... (architecture diagram + explanation)

  - layout: content_table
    headline: "Nutanix AHV to GCP Compute Engine --- VM type mapping"
    # ... (detailed mapping table)
```

Why it works: Clear three-act structure. Executives get the verdict in slides 3-4. Managers get the plan in slides 6-8. ICs get the specs in slides 10-11. Section dividers signal the depth transition. Anyone can leave after their section without missing what they need.

### Bad structure example

A deck that alternates randomly between strategic and technical slides:

```
Slide 1: Title
Slide 2: Architecture diagram (ICs)
Slide 3: Business case (Executives)
Slide 4: VM sizing table (ICs)
Slide 5: Roadmap (Managers)
Slide 6: Key recommendation (Executives)
Slide 7: RACI matrix (Managers)
Slide 8: Database comparison (ICs)
```

Why it fails: No audience can follow a coherent thread. The CEO is confused by slide 2. The IC is bored by slide 3. The manager cannot find the plan because it is sandwiched between a VM table and a recommendation. Everyone leaves dissatisfied.

### The "three audiences, one deck" test

For each section, ask: which audience is this for? If you cannot answer clearly, the section tries to serve everyone and serves no one. Every slide should have a primary audience. If a slide tries to be strategic and technical simultaneously, split it into two slides in different acts.

---

## Quick Reference: Layout Selection by Audience

| Layout | C-Suite | Customer | Manager | IC | Mixed |
|---|---|---|---|---|---|
| `title_cover` | Open | Open | Open | Open | Act 1 |
| `agenda` | Optional | Required | Required | Required | Required |
| `section_divider` | Skip | 3-4 max | Per workstream | Per domain | Per act |
| `content_two_col` | Avoid | Avoid | OK | Good | Act 2-3 |
| `content_diagram_text` | Avoid | Avoid | OK | Primary | Act 3 |
| `side_by_side` | OK | Good | Primary | Primary | Act 2-3 |
| `three_column` | OK | Primary | Primary | Good | Act 2 |
| `four_card` | OK | Primary | Good | OK | Act 2 |
| `big_stat_manual` | Primary | Good | Avoid | Avoid | Act 1 |
| `kpi_dashboard` | Primary | Good | Good | OK | Act 1-2 |
| `roadmap` | OK (simple) | Good | Primary | Good | Act 2 |
| `before_after` | Good | Good | OK | Avoid | Act 1 |
| `numbered_list` | Good (3-5) | Good | Primary | Primary | Act 2 |
| `status_board` | Primary | Avoid | Primary | OK | Act 2 |
| `content_table` | Avoid | Avoid | Good | Primary | Act 3 |
| `content_table_bullets` | Avoid | Avoid | OK | Primary | Act 3 |
| `matrix` | Avoid | Avoid | Primary | Primary | Act 2-3 |
| `funnel` | OK | Avoid | OK | Avoid | Act 1-2 |
| `callout` | Primary | OK | Good | Avoid | Act 1 |
| `quote` | OK | Primary | Avoid | Avoid | Act 1 |
| `image_showcase` | OK | Good | OK | Good | Any |
| `closing` | Close | Close | Close | Close | Close |

**Key:** Primary = ideal for this audience. Good = works well. OK = acceptable. Avoid = wrong audience.

---

## Quick Reference: Density Limits by Audience

| Parameter | C-Suite | Customer | Manager | IC |
|---|---|---|---|---|
| Max words per slide | 50 | 70 | 90 | 120 |
| Max words per headline | 12 | 10 | 15 | 18 |
| Max words per body field | 25 | 40 | 50 | 70 |
| Ideal slide count | 8-12 | 12-18 | 15-25 | 20-30+ |
| Max icons per slide | 2 | 4 | 4 | 1 |
| Section dividers | None | 3-4 | Per workstream | Per domain |
| Headline style | Assertion | Benefit | Action | Descriptive |
| Bold usage | Numbers + decisions | Numbers + differentiators | Owners + dates + blockers | Terms + names + parameters |
| Footnotes | Appendix only | Sparing | Expected | Expected |
| Agenda | Optional | Required | Required | Required |

---

## Quick Reference: Headline Patterns by Audience

### C-Suite patterns
- "We should [action] by [date] to [outcome]"
- "[Number] [noun] at risk if we [don't act / delay]"
- "Recommend [Option X]: [one-line rationale]"
- "[Metric] is [status] --- [implication]"

### Customer patterns
- "[Verb] your [pain point] by [quantified improvement]"
- "[Number] [customers/transactions/uptime] and growing"
- "From [current state] to [better state] in [timeframe]"
- "Three ways we [solve your problem]"

### Manager patterns
- "[Action] needed by [date]"
- "[N] workstreams: [summary status]"
- "Wave [N] starts [date] --- [scope]"
- "[Owner] owns [workstream], reports [cadence]"

### IC patterns
- "[Source technology] to [target technology] [specific topic]"
- "[Tool/Service] v[version]: [what it does in this context]"
- "[N] [things] compared across [N] dimensions"
- "[Architecture component]: [role in system]"

---

## Applying Profiles: Decision Flowchart

When building a deck, follow this sequence:

1. **Identify the primary audience.** Who has the most decision-making power in the room? That is your primary audience.
2. **Check for mixed audience.** If the audience spans more than one profile (e.g., CTO + engineering directors + senior engineers), use the Mixed Audience profile with the layer cake structure.
3. **Select slide count range** from the density table for the primary audience.
4. **Select layouts** from the layout selection matrix, prioritizing "Primary" layouts for the identified audience.
5. **Write headlines** using the headline pattern for the identified audience.
6. **Apply density limits** --- check every text field against the word count maximums.
7. **Set icon budget** --- count icons per slide and remove any that exceed the limit.
8. **Run the audience test** --- apply the specific test for the audience (elevator pitch, forward-to-boss, Monday morning, can-I-implement, three-audiences).
9. **Review for anti-patterns** --- check that no slide matches the "bad example" pattern for the audience.
