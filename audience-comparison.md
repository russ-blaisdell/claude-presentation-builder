# Audience Comparison — Same Content, Different Decks

> Back to [README](README.md) | [Presentation Principles](presentation-principles.md) | [Audience Profiles (research)](research/audience-profiles.md)

This document demonstrates how the same cloud migration content adapts to different audiences. Three decks were built from identical source material, each applying the audience-specific rules from [presentation-principles.md](presentation-principles.md).

## The Three Decks

| Deck | Audience | Slides | YAML | PPTX |
|------|----------|--------|------|------|
| **Original Showcase** | (Demo — all layouts) | 19 | [showcase-deck.yaml](showcase-deck.yaml) | [showcase-deck.pptx](showcase-deck.pptx) |
| **C-Suite** | CEO, CTO, VP Engineering | 10 | [cloud-migration-csuite-deck.yaml](cloud-migration-csuite-deck.yaml) | [cloud-migration-csuite-deck.pptx](cloud-migration-csuite-deck.pptx) |
| **Middle Management** | Directors, Sr. Managers, Program Leads | 18 | [cloud-migration-mgmt-deck.yaml](cloud-migration-mgmt-deck.yaml) | [cloud-migration-mgmt-deck.pptx](cloud-migration-mgmt-deck.pptx) |

---

## Side-by-Side Comparison

| Aspect | Original Showcase | C-Suite Deck | Management Deck |
|--------|------------------|--------------|-----------------|
| **Slides** | 19 | 10 | 18 |
| **Framework** | None (demo) | Minto Pyramid | Minto + operational detail |
| **Headline style** | Topic labels | Assertions | Actions + dates |
| **Recommendation** | Slide 18 (buried) | Slide 2 (the punchline) | Implicit via structure |
| **Words per slide** | 50-120 (inconsistent) | 30-50 | 80-100 |
| **Icons** | On everything | Only on KPI cards | Functional (categorize) |
| **RACI matrix** | Yes | No (too detailed) | Yes |
| **Partner comparison** | 6 slides | 0 (condensed to "3 shortlisted") | 3 slides (cards + criteria + timeline) |
| **Cloud provider table** | Yes | No | Yes |
| **Section dividers** | 1 | 2 | 4 |
| **Audience test** | "Does every layout work?" | "CEO flips to random slide?" | "Can someone act Monday morning?" |

---

## What the Principles Changed

### 1. Recommendation moved to slide 2

The original showcase buried the recommendation ("We recommend Option A — Single GCP Organization") on slide 18 of 19. The C-suite deck puts it on **slide 2** — the Minto Pyramid principle says lead with the answer. If the CEO leaves after 2 slides, they got the message.

**Original slide 18 headline:** *(no headline — callout layout)*
**C-Suite slide 2 headline:** "Invest $2M to migrate 1,300 VMs to GCP and AWS by December 2026 with a managed partner."

### 2. Headlines became assertions

Every headline in the principle-driven decks makes a claim the audience can agree or disagree with. The original used topic labels that require reading the body to understand the point.

| Original (topic label) | C-Suite (assertion) | Management (action + date) |
|------------------------|--------------------|-----------------------------|
| "Program Overview" | *(removed — too vague)* | "Migration executes in 3 phases across Nutanix AHV fleet" |
| "Migration Progress — Q1 2026" | "On-prem infrastructure costs $1.2M/month and growing" | "847 of 1,300 VMs discovered — assessment 94% complete" |
| "Cloud Migration Roadmap" | "Dev/test exits data centers by Q4 2026, production follows Q1 2027" | "Partner onboards April 15, Wave 1 starts Q2, DC exit target Q4" |
| "Program Health Dashboard" | "Four of five workstreams are on track — FinOps needs resolution" | "FinOps is blocked — cost model needs CFO sign-off before Q2 budget commits" |
| "Migration Decision Framework" | "Three decisions needed this quarter to stay on track" | "Five actions required in the next 30 days" |
| "Infrastructure Transformation" | "Manual provisioning becomes automated, single-cloud becomes resilient" | "Teams shift from manual DC ops to IaC-driven cloud management" |

Notice the pattern:
- **C-Suite headlines** state the strategic implication (costs, timeline, risk)
- **Management headlines** state the operational action (who does what by when)

### 3. Content density matched the audience

The C-suite deck has roughly **half the slides** and **half the words per slide** as the management deck. Content that was in one dense slide in the showcase got either cut (C-suite) or expanded with operational detail (management).

**What C-Suite lost** (vs. showcase): partner evaluation criteria, cloud provider comparison table, RACI matrix, three-column platform teams, funnel, technology adoption pipeline, quote

**What Management gained** (vs. showcase): 4 section dividers for navigation, action items with dates and owners, explicit "who needs to do what by when" on every operational slide

### 4. Icons followed the 1-second test

The showcase put icons on almost every slide. The C-suite deck uses icons **only** on KPI dashboard cards (where they identify what the metric measures) and the before/after layout (where they distinguish current vs. target). The management deck adds icons to categorize platform team columns but skips them on tables, matrices, and numbered lists.

---

## C-Suite Deck Slides

| # | Layout | Headline |
|---|--------|----------|
| 1 | `title_cover` | We Should Exit All Data Centers by EOY 2026 |
| 2 | `callout` | Invest $2M to migrate 1,300 VMs to GCP and AWS by December 2026 |
| 3 | `section_divider` | 01 — Why Now |
| 4 | `kpi_dashboard` | On-prem infrastructure costs $1.2M/month and growing |
| 5 | `before_after` | Manual provisioning becomes automated, single-cloud becomes resilient |
| 6 | `section_divider` | 02 — The Plan |
| 7 | `roadmap` | Dev/test exits data centers by Q4 2026, production follows Q1 2027 |
| 8 | `numbered_list` | Three decisions needed this quarter to stay on track |
| 9 | `status_board` | Four of five workstreams are on track — FinOps needs resolution |
| 10 | `closing` | Questions? |

## Middle Management Deck Slides

| # | Layout | Headline |
|---|--------|----------|
| 1 | `title_cover` | Cloud Migration — Program Execution Plan |
| 2 | `agenda` | (7 agenda items) |
| 3 | `section_divider` | 01 — Program Scope |
| 4 | `kpi_dashboard` | 847 of 1,300 VMs discovered — assessment 94% complete |
| 5 | `content_two_col` | Migration executes in 3 phases across Nutanix AHV fleet |
| 6 | `section_divider` | 02 — Architecture Decision |
| 7 | `before_after` | Teams shift from manual DC ops to IaC-driven cloud management |
| 8 | `three_column` | Three platform teams provide cross-cutting services |
| 9 | `section_divider` | 03 — Partner Selection |
| 10 | `four_card` | Partner decision needed by April 10 — three GCP, one AWS |
| 11 | `side_by_side` | Partner evaluation weights speed and technical depth highest |
| 12 | `roadmap` | Partner onboards April 15, Wave 1 starts Q2, DC exit target Q4 |
| 13 | `section_divider` | 04 — Status & Risk |
| 14 | `status_board` | FinOps is blocked — cost model needs CFO sign-off |
| 15 | `content_table` | GCP and AWS are complementary — GCP for new workloads, AWS for existing |
| 16 | `matrix` | Engineering owns infrastructure and database — Security owns compliance |
| 17 | `numbered_list` | Five actions required in the next 30 days |
| 18 | `closing` | Questions? |

---

## How to Build These

```bash
# C-Suite version
/tmp/xlsx-venv/bin/python3 test_deck.py cloud-migration-csuite-deck.yaml --proof-images

# Management version
/tmp/xlsx-venv/bin/python3 test_deck.py cloud-migration-mgmt-deck.yaml --proof-images

# Upload either to Google Drive
/tmp/xlsx-venv/bin/python3 test_deck.py cloud-migration-csuite-deck.yaml --proof-images --upload
```

## Principles Applied

These decks were built by applying the rules in [presentation-principles.md](presentation-principles.md):

1. **One idea per slide** — every headline is an assertion, not a topic label
2. **Audience density** — C-suite: 30-50 words, management: 80-100 words
3. **Minto Pyramid** — recommendation on slide 2 (C-suite), not buried at the end
4. **Icon 1-second test** — icons only where they identify a concept instantly
5. **Split > shrink** — management deck has 18 slides instead of cramming into 10
6. **Section dividers** — management deck has 4 sections for navigation; C-suite has 2
