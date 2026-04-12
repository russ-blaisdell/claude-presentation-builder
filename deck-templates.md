# Deck Templates — Starter YAML Skeletons

Pre-built YAML structures for common presentation types. Copy one as a starting point, fill in your content, and build with `test_deck.py`.

**Related docs:** [README](README.md) | [Principles](presentation-principles.md) (audience rules) | [Guide](presentation-guide.md) (YAML reference) | [Content Limits](layout-limits.json)

## Executive Presentation (10-15 slides)

For C-suite, VP-level audiences. Strategy decisions, program kickoffs, quarterly reviews.

```yaml
title: "Presentation Title"
date: "2026-03-28"
style: "corporate"
diagram_variants: 1

slides:
  - layout: title_cover
    headline: "Title — Subtitle"
    subheader: "Platform Engineering | Context Line"
    background: "p12"

  - layout: agenda
    items:
      - "Strategic Context"
      - "Key Findings"
      - "Recommendation"
      - "Path Forward"
      - "Next Steps"

  - layout: section_divider
    section_number: "01"
    headline: "Strategic Context"
    background: "purple"

  - layout: kpi_dashboard
    headline: "Current State"
    metrics:
      - number: "XX"
        label: "Metric 1"
        trend: "up"
      - number: "XX"
        label: "Metric 2"
        trend: "flat"
      - number: "XX"
        label: "Metric 3"
        trend: "down"
      - number: "XX"
        label: "Metric 4"
        highlight: true

  - layout: before_after
    headline: "The Transformation"
    before:
      label: "Current State"
      items:
        - "Pain point 1"
        - "Pain point 2"
        - "Pain point 3"
    after:
      label: "Target State"
      items:
        - "Outcome 1"
        - "Outcome 2"
        - "Outcome 3"
    arrow_label: "Program Name"

  - layout: section_divider
    section_number: "02"
    headline: "Key Findings"
    background: "purple"

  - layout: three_column
    headline: "Three Pillars"
    col1_icon: "gear"
    col1_title: "Pillar 1"
    col1_body: "Description..."
    col2_icon: "padlock"
    col2_title: "Pillar 2"
    col2_body: "Description..."
    col3_icon: "dashboard-gauge"
    col3_title: "Pillar 3"
    col3_body: "Description..."

  - layout: callout
    callout_text: "The key recommendation in one clear sentence."
    supporting_text: "Brief supporting rationale — why this approach, what it enables."
    icon: "lightbulb"
    style: "boxed"

  - layout: roadmap
    headline: "Path Forward"
    time_axis: ["Q1", "Q2", "Q3", "Q4"]
    swimlanes:
      - name: "Workstream 1"
        items:
          - label: "Phase 1"
            start: "Q1"
            end: "Q2"
            status: "active"
          - label: "Phase 2"
            start: "Q3"
            end: "Q4"
            status: "planned"

  - layout: numbered_list
    headline: "Next Steps"
    items:
      - title: "Immediate Action"
        body: "What happens this week"
      - title: "Short-term Milestone"
        body: "What happens this month"
      - title: "Decision Point"
        body: "What needs to be decided and by when"

  - layout: closing
    headline: "Questions?"
    subheader: "Title — Platform Engineering"
    background: "p12"
```

## Technical / Architecture Deck (15-20 slides)

For engineering leadership, architecture reviews, technical deep-dives.

```yaml
title: "Technical Topic — Architecture Review"
date: "2026-03-28"
style: "corporate"
diagram_variants: 3

slides:
  - layout: title_cover
    headline: "Technical Topic — Architecture Review"
    subheader: "Platform Engineering"
    background: "p12"

  - layout: agenda
    items:
      - "Current Architecture"
      - "Problem Statement"
      - "Proposed Solution"
      - "Migration Plan"
      - "Risk Assessment"
      - "Next Steps"

  - layout: content_two_col
    headline: "System Overview"
    left_stats:
      - number: "XX"
        label: "Metric"
        icon: "server-stack"
      - number: "XX"
        label: "Metric"
        icon: "database-new"
    left_icon: "gear"
    left_title: "Architecture"
    left_body: "Current system description..."
    right_icon: "checklist"
    right_title: "Constraints"
    right_body: "Key constraints and requirements..."

  - layout: content_diagram_text
    headline: "Architecture — Current State"
    visual:
      type: "org-hierarchy"
      style: "corporate"
      approaches: ["native"]
      data:
        root: "System"
        children:
          - "Component A"
          - "Component B"
          - "Component C"
    left_icon: "gear"
    left_title: "Structure"
    left_body: "How it works today..."
    right_icon: "sliders"
    right_title: "Tradeoffs"
    right_body: "Pros and cons..."

  - layout: side_by_side
    headline: "Requirements"
    left_icon: "checklist"
    left_title: "Must Have"
    left_body: |
      Requirement 1
      Requirement 2
      Requirement 3
    right_icon: "three-stars"
    right_title: "Nice to Have"
    right_body: |
      Preference 1
      Preference 2
      Preference 3

  - layout: content_table
    headline: "Option Comparison"
    columns: ["Criteria", "Option A", "Option B", "Weight"]
    rows:
      - ["Criterion 1", "Value", "Value", "25%"]
      - ["Criterion 2", "Value", "Value", "20%"]
      - ["Criterion 3", "Value", "Value", "15%"]

  - layout: matrix
    headline: "RACI"
    row_header: "Component"
    rows:
      - label: "Component A"
        values: ["R", "A", "C"]
      - label: "Component B"
        values: ["C", "R", "A"]
    columns: ["Team 1", "Team 2", "Team 3"]
    cell_colors:
      R: "5F016F"
      A: "FF80D4"
      C: "F0E8F5"
    legend: "R = Responsible | A = Accountable | C = Consulted"

  - layout: status_board
    headline: "Risk Assessment"
    items:
      - name: "Risk 1"
        status: "green"
        summary: "Mitigated. Description of mitigation."
      - name: "Risk 2"
        status: "amber"
        summary: "Monitoring. Description of concern."
      - name: "Risk 3"
        status: "red"
        summary: "Blocked. What needs to happen."

  - layout: closing
    headline: "Questions?"
    background: "p12"
```

## Status / Update Deck (8-12 slides)

For program reviews, monthly updates, governance check-ins.

```yaml
title: "Program Status Update"
date: "2026-03-28"
style: "corporate"

slides:
  - layout: title_cover
    headline: "Program Status Update"
    subheader: "Engineering | Monthly Review"
    background: "p12"

  - layout: kpi_dashboard
    headline: "Key Metrics"
    metrics:
      - number: "XX"
        label: "On Track"
        trend: "up"
      - number: "XX"
        label: "At Risk"
        trend: "flat"
      - number: "XX"
        label: "Blocked"
        trend: "down"
        highlight: true

  - layout: status_board
    headline: "Workstream Status"
    items:
      - name: "Workstream 1"
        status: "green"
        summary: "On track. Milestone achieved."
      - name: "Workstream 2"
        status: "amber"
        summary: "Minor delay. Mitigation in progress."
      - name: "Workstream 3"
        status: "red"
        summary: "Blocked. Requires escalation."
    as_of: "2026-03-28"

  - layout: roadmap
    headline: "Timeline"
    time_axis: ["Q1", "Q2", "Q3", "Q4"]
    swimlanes:
      - name: "Delivery"
        items:
          - label: "Phase 1"
            start: "Q1"
            end: "Q2"
            status: "complete"
          - label: "Phase 2"
            start: "Q2"
            end: "Q3"
            status: "active"

  - layout: numbered_list
    headline: "Actions & Decisions Needed"
    items:
      - title: "Decision 1"
        body: "What needs to be decided and by whom"
      - title: "Action 1"
        body: "What needs to happen next"
      - title: "Escalation"
        body: "What needs leadership attention"

  - layout: closing
    headline: "Questions?"
    background: "p12"
```
