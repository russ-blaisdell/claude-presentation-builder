#!/usr/bin/env python3
"""
Layout Test Generator — Creates 25 content variations per layout type.

Generates test-layouts.yaml with ~550 slides organized by layout, testing:
- Minimal content (fewest items, shortest text)
- Typical content (realistic length)
- Dense content (maximum items, long text)
- Overflow stress (very long text, no natural breaks)
- Edge cases (1 item, max items, special characters, missing optional fields)
- Icon combinations (all, none, mixed)
- Real-world examples (Acme Corp content from actual projects)

Usage:
    python3 test-layouts.py [--output test-layouts.yaml]
"""

import json
import os
import sys

import yaml


# ---------------------------------------------------------------------------
# Test content library — realistic Acme Corp-themed text at varying lengths
# ---------------------------------------------------------------------------

SHORT_TITLES = [
    "Overview", "Status", "Next Steps", "Timeline", "Budget",
    "Architecture", "Security", "Migration", "Platform", "FinOps",
]

MEDIUM_TITLES = [
    "Cloud Migration Program Overview",
    "Infrastructure Modernization Status",
    "Platform Engineering Roadmap",
    "Security Compliance Assessment",
    "Data Center Exit Strategy",
]

LONG_TITLES = [
    "Comprehensive Cloud Infrastructure Modernization and Data Center Exit Program — Strategic Assessment and Recommendation",
    "Enterprise Platform Engineering Transformation: From On-Premise Legacy Systems to Multi-Cloud Native Architecture",
    "Cross-Functional Security, Compliance, and Identity Access Management Platform Integration Strategy",
]

SHORT_BODY = "Migrate 1,300 VMs to cloud."

MEDIUM_BODY = """Migrate ~1,300 Flowbird on-prem VMs to GCP and AWS
Hard deadline: EOY 2026 (dev/test/IT)
Production: 2026-2027
Approach: Lift-and-shift with minimum modernization"""

LONG_BODY = """Migrate approximately 1,300 Flowbird on-premise virtual machines currently running on Nutanix AHV hypervisors across 10 global data center locations spanning EMEA, Americas, and APAC regions to a multi-cloud destination architecture leveraging both Google Cloud Platform (GCP) and Amazon Web Services (AWS).

The migration follows a phased approach:
Phase 1: K8s-based workloads (lowest complexity, highest cloud-readiness)
Phase 2: K8s-capable workloads requiring containerization assessment
Phase 3: Outdated software requiring version updates before migration

Hard deadline for dev/test/IT environments: End of Year 2026
Production environment migration: Q1-Q4 2027
Post-migration modernization and optimization: 2027-2028

Key constraints: PCI-DSS compliance required, ISO 27001 controls mandatory, GDPR data residency for EU workloads.

Migration partner evaluation criteria: Speed/delivery confidence (25%), Technical depth (20%), Reference cases (20%), Cost/fixed price (15%), Geographic presence EMEA (10%), Tooling/methodology (10%)."""

OVERFLOW_TEXT = "Supercalifragilisticexpialidocious_extremely_long_word_without_any_natural_break_points_that_should_definitely_cause_text_overflow_in_narrow_containers " * 3

# Icon subsets for testing
ALL_ICONS = ["gear", "padlock", "dashboard-gauge", "coin-stacks", "checklist",
             "clock", "server-stack", "buildings", "calendar-day", "lightbulb",
             "three-stars", "briefcase-check", "cloud-network", "team-network"]
NO_ICONS = ["", "", "", ""]

SPECIAL_CHARS = "Acme Corp's \"cloud-first\" strategy: <100ms latency & 99.99% uptime — $1.2M/mo"


def _icon(idx=0):
    """Get an icon name by index, cycling through available icons."""
    return ALL_ICONS[idx % len(ALL_ICONS)]


# ---------------------------------------------------------------------------
# Per-layout test generators
# ---------------------------------------------------------------------------

def gen_title_cover():
    """25 title_cover variations."""
    slides = []
    # Minimal
    slides.append({"layout": "title_cover", "headline": "Title", "notes": "TEST: minimal — shortest title"})
    slides.append({"layout": "title_cover", "headline": "Title", "subheader": "Sub", "background": "p12", "notes": "TEST: minimal with subheader"})
    # Typical
    slides.append({"layout": "title_cover", "headline": "Cloud Infrastructure — Modernization Program", "subheader": "Acme Corp | Engineering Leadership Briefing", "background": "p12", "notes": "TEST: typical — dash-split title"})
    slides.append({"layout": "title_cover", "headline": "Platform Engineering Strategy", "subheader": "Acme Corp | Q1 2026 Review", "background": "p13", "notes": "TEST: typical — no dash, different bg"})
    slides.append({"layout": "title_cover", "headline": "Security Program — Annual Review", "subheader": "Acme Corp | Confidential", "background": "p17", "notes": "TEST: typical — p17 background"})
    # Dense
    slides.append({"layout": "title_cover", "headline": "Comprehensive Cloud Infrastructure Modernization — Data Center Exit Program", "subheader": "Acme Corp | Engineering Leadership | Developers XP Organization | Q1 2026 Strategic Review", "background": "p12", "notes": "TEST: dense — long title and subheader"})
    # Overflow
    slides.append({"layout": "title_cover", "headline": LONG_TITLES[0], "subheader": "This is an extremely long subtitle that tests how the system handles overflow in the subheader text field which should wrap properly", "background": "p12", "notes": "TEST: overflow — very long title and subtitle"})
    slides.append({"layout": "title_cover", "headline": "NoSpacesInThisTitleAtAllToTestWrappingBehaviorWithoutNaturalBreakPoints", "background": "p12", "notes": "TEST: overflow — no spaces in title"})
    # Edge cases
    slides.append({"layout": "title_cover", "headline": SPECIAL_CHARS, "background": "p12", "notes": "TEST: edge — special characters"})
    slides.append({"layout": "title_cover", "headline": "A", "notes": "TEST: edge — single character title"})
    slides.append({"layout": "title_cover", "headline": "Title – Subtitle", "background": "p12", "notes": "TEST: edge — en-dash separator"})
    slides.append({"layout": "title_cover", "headline": "Title - Subtitle", "background": "p12", "notes": "TEST: edge — hyphen separator"})
    # No optional fields
    slides.append({"layout": "title_cover", "headline": "Title Only — No Background", "notes": "TEST: edge — no background specified"})
    # Width stress
    slides.append({"layout": "title_cover", "headline": "W" * 100, "background": "p12", "notes": "TEST: width — 100 character single word"})
    # Real world
    slides.append({"layout": "title_cover", "headline": "GCP — Cloud Migration Program", "subheader": "Acme Corp | Data Center to Cloud Migration", "background": "p12", "notes": "TEST: real — actual GCP deck title"})
    slides.append({"layout": "title_cover", "headline": "AWS — Migration Acceleration Program", "subheader": "Acme Corp | MAP 2.0 Engagement", "background": "p13", "notes": "TEST: real — actual AWS deck title"})
    # Padding to 25
    for i in range(25 - len(slides)):
        slides.append({"layout": "title_cover", "headline": f"Variant {len(slides)+1} — Test {i+1}", "subheader": f"Test variant {i+1}", "background": "p12", "notes": f"TEST: variant {i+1}"})
    return slides[:25]


def gen_agenda():
    """25 agenda variations."""
    slides = []
    # Minimal
    slides.append({"layout": "agenda", "items": ["Single Item"], "notes": "TEST: minimal — 1 item"})
    slides.append({"layout": "agenda", "items": ["Item 1", "Item 2"], "notes": "TEST: minimal — 2 items"})
    # Typical
    slides.append({"layout": "agenda", "items": ["Program Overview", "Architecture", "Migration Plan", "Cost Model", "Next Steps"], "notes": "TEST: typical — 5 items"})
    slides.append({"layout": "agenda", "headline": "Custom Headline", "items": ["Topic A", "Topic B", "Topic C", "Topic D"], "notes": "TEST: typical — custom headline"})
    # Dense
    slides.append({"layout": "agenda", "items": ["Program Overview & Timeline", "Architecture & Governance", "Migration Execution Plan", "Cost Model & FinOps", "Partner Evaluation", "Risk Assessment", "Next Steps"], "notes": "TEST: dense — 7 items (max)"})
    slides.append({"layout": "agenda", "items": [f"Very Long Agenda Item Number {i+1} That Tests How Well the Layout Handles Wrapping Text" for i in range(7)], "notes": "TEST: dense — 7 long items"})
    # Overflow
    slides.append({"layout": "agenda", "items": [f"Item {i+1}" for i in range(10)], "notes": "TEST: overflow — 10 items (exceeds max 7)"})
    slides.append({"layout": "agenda", "items": [OVERFLOW_TEXT[:80] for _ in range(5)], "notes": "TEST: overflow — long text per item"})
    # Edge cases
    slides.append({"layout": "agenda", "items": [SPECIAL_CHARS], "notes": "TEST: edge — special characters"})
    slides.append({"layout": "agenda", "agenda_image": "p21", "items": ["Item 1", "Item 2", "Item 3"], "notes": "TEST: edge — p21 image"})
    slides.append({"layout": "agenda", "agenda_image": "p23", "items": ["Item 1", "Item 2", "Item 3"], "notes": "TEST: edge — p23 image"})
    # Real world
    slides.append({"layout": "agenda", "items": ["Program Overview & Timeline", "Architecture Options", "Folder Structure & Governance", "Cross-Cutting Services & FinOps", "Migration Partner Requirements", "Next Steps"], "notes": "TEST: real — GCP deck agenda"})
    # Padding
    for i in range(25 - len(slides)):
        slides.append({"layout": "agenda", "items": [f"Item {j+1}" for j in range(3 + i % 5)], "notes": f"TEST: variant {i+1}"})
    return slides[:25]


def gen_section_divider():
    """25 section_divider variations."""
    slides = []
    # Minimal
    slides.append({"layout": "section_divider", "headline": "Title", "background": "purple", "notes": "TEST: minimal — no number, no sub"})
    slides.append({"layout": "section_divider", "section_number": "1", "headline": "Title", "background": "purple", "notes": "TEST: minimal — number only"})
    # Typical
    slides.append({"layout": "section_divider", "section_number": "01", "headline": "Program Overview", "subheader": "Scale, timeline, and strategic context", "background": "purple", "icon": "presentation-chart", "notes": "TEST: typical — all fields"})
    slides.append({"layout": "section_divider", "section_number": "02", "headline": "Architecture", "background": "light", "notes": "TEST: typical — light background"})
    # Dense
    slides.append({"layout": "section_divider", "section_number": "03", "headline": "Comprehensive Cross-Cutting Platform Services and Security Controls", "subheader": "Including FinOps, monitoring, identity, and compliance enforcement across all cloud providers", "background": "purple", "icon": "padlock", "notes": "TEST: dense — long headline and subheader"})
    # Overflow
    slides.append({"layout": "section_divider", "headline": LONG_TITLES[1], "background": "purple", "notes": "TEST: overflow — very long headline"})
    # Edge cases
    slides.append({"layout": "section_divider", "section_number": "99", "headline": "Section", "background": "purple", "notes": "TEST: edge — large section number"})
    slides.append({"layout": "section_divider", "headline": "Section", "background": "purple", "icon": "gear", "notes": "TEST: edge — icon no number"})
    slides.append({"layout": "section_divider", "headline": "A", "background": "purple", "notes": "TEST: edge — single char"})
    # Backgrounds
    slides.append({"layout": "section_divider", "headline": "Image Background", "background": "p12", "notes": "TEST: edge — image background"})
    # Real world
    slides.append({"layout": "section_divider", "section_number": "01", "headline": "Migration Strategy", "subheader": "Assessment, planning, and execution approach", "background": "purple", "icon": "checklist", "notes": "TEST: real — migration section"})
    # Padding
    for i in range(25 - len(slides)):
        slides.append({"layout": "section_divider", "section_number": str(i+1), "headline": f"Section {i+1}", "background": ["purple", "light"][i % 2], "notes": f"TEST: variant {i+1}"})
    return slides[:25]


def gen_side_by_side():
    """25 side_by_side variations."""
    slides = []
    # Minimal
    slides.append({"layout": "side_by_side", "headline": "Comparison", "left_title": "Left", "left_body": "A", "right_title": "Right", "right_body": "B", "notes": "TEST: minimal — shortest content"})
    # Typical
    slides.append({"layout": "side_by_side", "headline": "Migration Partner Requirements", "left_icon": "checklist", "left_title": "Must Have", "left_body": MEDIUM_BODY, "right_icon": "three-stars", "right_title": "Evaluation Criteria", "right_body": "Speed: 25%\nTechnical depth: 20%\nReference cases: 20%\nCost: 15%\nGeographic: 10%", "notes": "TEST: typical — icons + medium text"})
    # Dense
    slides.append({"layout": "side_by_side", "headline": "Dense Comparison", "left_icon": "gear", "left_title": "Left Column", "left_body": LONG_BODY, "right_icon": "padlock", "right_title": "Right Column", "right_body": LONG_BODY, "notes": "TEST: dense — long body both sides"})
    # No icons
    slides.append({"layout": "side_by_side", "headline": "No Icons", "left_title": "Left", "left_body": MEDIUM_BODY, "right_title": "Right", "right_body": MEDIUM_BODY, "notes": "TEST: edge — no icons"})
    # Overflow
    slides.append({"layout": "side_by_side", "headline": LONG_TITLES[0], "left_title": "Overflow Left", "left_body": OVERFLOW_TEXT, "right_title": "Overflow Right", "right_body": OVERFLOW_TEXT, "notes": "TEST: overflow — all fields overflow"})
    # Unbalanced
    slides.append({"layout": "side_by_side", "headline": "Unbalanced", "left_icon": "gear", "left_title": "Short", "left_body": SHORT_BODY, "right_icon": "padlock", "right_title": "Long Column", "right_body": LONG_BODY, "notes": "TEST: edge — very unbalanced columns"})
    # Special chars
    slides.append({"layout": "side_by_side", "headline": SPECIAL_CHARS, "left_title": SPECIAL_CHARS, "left_body": SPECIAL_CHARS, "right_title": "Normal", "right_body": "Normal text", "notes": "TEST: edge — special characters"})
    # Real world
    slides.append({"layout": "side_by_side", "headline": "GCP Program — RaMP Alignment", "left_icon": "coin-stacks", "left_title": "RaMP Program", "left_body": "Rapid Migration & Modernization Program\nService funds: 20% of projected ARR\nCapped at $2M per workload", "right_icon": "gear", "right_title": "Migration Tools", "right_body": "Migrate to Virtual Machines\nSupports Nutanix AHV\nTargets: Compute Engine, GKE", "notes": "TEST: real — GCP RaMP slide"})
    # Padding
    for i in range(25 - len(slides)):
        slides.append({"layout": "side_by_side", "headline": f"Test {i+1}", "left_icon": _icon(i), "left_title": f"Left {i+1}", "left_body": MEDIUM_BODY[:50*(i%3+1)], "right_icon": _icon(i+1), "right_title": f"Right {i+1}", "right_body": MEDIUM_BODY[:50*((i+1)%3+1)], "notes": f"TEST: variant {i+1}"})
    return slides[:25]


def gen_three_column():
    """25 three_column variations."""
    slides = []
    # Minimal
    slides.append({"layout": "three_column", "headline": "Three Things", "col1_title": "One", "col1_body": "A", "col2_title": "Two", "col2_body": "B", "col3_title": "Three", "col3_body": "C", "notes": "TEST: minimal"})
    # Typical
    slides.append({"layout": "three_column", "headline": "Cross-Cutting Platform Teams", "col1_icon": "padlock", "col1_title": "Security Platform", "col1_body": "Lead: Byron Gehman\nSecurity controls across ALL cloud accounts\nIAM, network security, encryption", "col2_icon": "coin-stacks", "col2_title": "Compute Platform", "col2_body": "Lead: Rafael Ramirez\nFinOps services to IT and Engineering\nCost monitoring and optimization", "col3_icon": "dashboard-gauge", "col3_title": "Monitoring Platform", "col3_body": "Lead: Allan Cieli\nObservability across AWS and GCP\nUnified alerting and on-call", "notes": "TEST: typical — real teams"})
    # Dense
    slides.append({"layout": "three_column", "headline": "Dense Content", "col1_icon": "gear", "col1_title": "Column One", "col1_body": LONG_BODY[:300], "col2_icon": "padlock", "col2_title": "Column Two", "col2_body": LONG_BODY[:300], "col3_icon": "clock", "col3_title": "Column Three", "col3_body": LONG_BODY[:300], "notes": "TEST: dense — long body text"})
    # No icons
    slides.append({"layout": "three_column", "headline": "No Icons", "col1_title": "One", "col1_body": MEDIUM_BODY, "col2_title": "Two", "col2_body": MEDIUM_BODY, "col3_title": "Three", "col3_body": MEDIUM_BODY, "notes": "TEST: edge — no icons"})
    # Overflow
    slides.append({"layout": "three_column", "headline": LONG_TITLES[2], "col1_title": "Overflow", "col1_body": OVERFLOW_TEXT, "col2_title": "Overflow", "col2_body": OVERFLOW_TEXT, "col3_title": "Overflow", "col3_body": OVERFLOW_TEXT, "notes": "TEST: overflow — all columns overflow"})
    # Unbalanced
    slides.append({"layout": "three_column", "headline": "Unbalanced", "col1_icon": "gear", "col1_title": "Short", "col1_body": "Brief.", "col2_icon": "padlock", "col2_title": "Medium", "col2_body": MEDIUM_BODY, "col3_icon": "clock", "col3_title": "Long", "col3_body": LONG_BODY[:400], "notes": "TEST: edge — very unbalanced columns"})
    # Padding
    for i in range(25 - len(slides)):
        slides.append({"layout": "three_column", "headline": f"Test {i+1}", "col1_icon": _icon(i), "col1_title": f"Col A", "col1_body": SHORT_BODY * (i%3+1), "col2_icon": _icon(i+3), "col2_title": f"Col B", "col2_body": SHORT_BODY * ((i+1)%3+1), "col3_icon": _icon(i+6), "col3_title": f"Col C", "col3_body": SHORT_BODY * ((i+2)%3+1), "notes": f"TEST: variant {i+1}"})
    return slides[:25]


def gen_four_card():
    """25 four_card variations."""
    slides = []
    # Minimal
    slides.append({"layout": "four_card", "headline": "One Card", "card1_title": "Card", "card1_body": "Content", "notes": "TEST: minimal — 1 card"})
    slides.append({"layout": "four_card", "headline": "Two Cards", "card1_title": "A", "card1_body": "Content", "card2_title": "B", "card2_body": "Content", "notes": "TEST: minimal — 2 cards"})
    # Typical
    slides.append({"layout": "four_card", "headline": "Partner Shortlist", "card1_title": "Devotam", "card1_body": "Google Cloud Premier\nFrance, Nordics & UK", "card2_title": "Capgemini", "card2_body": "Google's strongest\nProven at scale", "card3_title": "Persistent", "card3_body": "Added by Acme Corp\nStrong presence", "card4_title": "EPAM", "card4_body": "Existing relationship\nData expertise", "notes": "TEST: typical — 4 cards"})
    # Dense — 8 cards
    slides.append({"layout": "four_card", "headline": "Eight Cards", **{f"card{i+1}_title": f"Card {i+1}" for i in range(8)}, **{f"card{i+1}_body": f"Content for card {i+1}\nLine 2\nLine 3" for i in range(8)}, "notes": "TEST: dense — 8 cards (max)"})
    # 5, 6, 7 cards
    for n in [5, 6, 7]:
        slides.append({"layout": "four_card", "headline": f"{n} Cards", **{f"card{i+1}_title": f"Card {i+1}" for i in range(n)}, **{f"card{i+1}_body": f"Content {i+1}" for i in range(n)}, "notes": f"TEST: edge — {n} cards"})
    # Overflow
    slides.append({"layout": "four_card", "headline": "Overflow Cards", "card1_title": "Card 1", "card1_body": LONG_BODY[:200], "card2_title": "Card 2", "card2_body": LONG_BODY[:200], "card3_title": "Card 3", "card3_body": LONG_BODY[:200], "card4_title": "Card 4", "card4_body": LONG_BODY[:200], "notes": "TEST: overflow — long body per card"})
    # 3 cards
    slides.append({"layout": "four_card", "headline": "Three Cards", "card1_title": "A", "card1_body": "Content A", "card2_title": "B", "card2_body": "Content B", "card3_title": "C", "card3_body": "Content C", "notes": "TEST: edge — 3 cards"})
    # Padding
    for i in range(25 - len(slides)):
        n = (i % 4) + 2
        slides.append({"layout": "four_card", "headline": f"Test {i+1}", **{f"card{j+1}_title": f"Card {j+1}" for j in range(n)}, **{f"card{j+1}_body": f"Body text for card {j+1}" for j in range(n)}, "notes": f"TEST: variant {i+1} — {n} cards"})
    return slides[:25]


def gen_big_stat():
    """25 big_stat_manual variations."""
    slides = []
    # Minimal
    slides.append({"layout": "big_stat_manual", "headline": "Stat", "number": "42", "notes": "TEST: minimal — number only"})
    slides.append({"layout": "big_stat_manual", "headline": "Stat", "number": "42", "label": "Answer", "notes": "TEST: minimal — number + label"})
    # Typical
    slides.append({"layout": "big_stat_manual", "headline": "Global Scale", "number": "1,300+", "label": "Virtual machines across 10 data centers migrating to multi-cloud", "icon": "server-stack", "notes": "TEST: typical — all fields"})
    slides.append({"layout": "big_stat_manual", "headline": "Cost Savings", "number": "$2.4M", "label": "Annual infrastructure cost reduction target", "icon": "coin-stacks", "notes": "TEST: typical — dollar amount"})
    slides.append({"layout": "big_stat_manual", "headline": "Uptime", "number": "99.99%", "label": "Production SLA target across multi-cloud", "icon": "circle-check", "notes": "TEST: typical — percentage"})
    # Dense
    slides.append({"layout": "big_stat_manual", "headline": "Very Detailed Metric", "number": "1,300+", "label": "Virtual machines spanning 10 data centers across EMEA, Americas, and APAC regions currently running on Nutanix AHV hypervisors being migrated to GCP and AWS multi-cloud architecture", "icon": "server-stack", "notes": "TEST: dense — very long label"})
    # Overflow
    slides.append({"layout": "big_stat_manual", "headline": LONG_TITLES[0], "number": "999,999,999", "label": OVERFLOW_TEXT[:200], "notes": "TEST: overflow — long number and label"})
    # Edge cases
    slides.append({"layout": "big_stat_manual", "headline": "", "number": "0", "label": "Zero", "notes": "TEST: edge — zero value, no headline"})
    slides.append({"layout": "big_stat_manual", "headline": "Big", "number": "1", "notes": "TEST: edge — single digit, no label, no icon"})
    # Padding
    for i in range(25 - len(slides)):
        slides.append({"layout": "big_stat_manual", "headline": f"Metric {i+1}", "number": str((i+1) * 100), "label": f"Description of metric {i+1}", "icon": _icon(i), "notes": f"TEST: variant {i+1}"})
    return slides[:25]


def gen_kpi_dashboard():
    """25 kpi_dashboard variations."""
    slides = []
    # Minimal
    slides.append({"layout": "kpi_dashboard", "headline": "Metrics", "metrics": [{"number": "42", "label": "Answer"}], "notes": "TEST: minimal — 1 metric"})
    slides.append({"layout": "kpi_dashboard", "headline": "Metrics", "metrics": [{"number": "A", "label": "X"}, {"number": "B", "label": "Y"}], "notes": "TEST: minimal — 2 metrics"})
    # Typical
    slides.append({"layout": "kpi_dashboard", "headline": "Migration Progress", "metrics": [
        {"number": "847", "label": "VMs Discovered", "trend": "up", "target": "1,300", "icon": "server-stack"},
        {"number": "94%", "label": "Assessment Coverage", "trend": "up", "icon": "circle-check"},
        {"number": "$1.2M", "label": "Monthly Spend", "trend": "down", "icon": "coin-stacks"},
        {"number": "3", "label": "Partners", "trend": "flat", "icon": "team-network"},
    ], "notes": "TEST: typical — 4 metrics with all fields"})
    # Dense — 8 metrics
    slides.append({"layout": "kpi_dashboard", "headline": "Full Dashboard", "metrics": [
        {"number": str(i*100), "label": f"Metric {i+1}", "trend": ["up", "down", "flat"][i%3], "icon": _icon(i)}
        for i in range(8)
    ], "notes": "TEST: dense — 8 metrics (max density)"})
    # 6 metrics
    slides.append({"layout": "kpi_dashboard", "headline": "Six Metrics", "metrics": [
        {"number": str(i*50), "label": f"KPI {i+1}", "icon": _icon(i)} for i in range(6)
    ], "notes": "TEST: typical — 6 metrics"})
    # Highlight
    slides.append({"layout": "kpi_dashboard", "headline": "Highlights", "metrics": [
        {"number": "100", "label": "Normal", "icon": "gear"},
        {"number": "URGENT", "label": "Highlighted", "highlight": True, "icon": "clock"},
        {"number": "50%", "label": "Normal", "icon": "checklist"},
        {"number": "BLOCKED", "label": "Highlighted", "highlight": True, "icon": "padlock"},
    ], "notes": "TEST: edge — mixed highlight"})
    # No icons
    slides.append({"layout": "kpi_dashboard", "headline": "No Icons", "metrics": [
        {"number": str(i*10), "label": f"Metric {i+1}", "trend": "up"} for i in range(4)
    ], "notes": "TEST: edge — no icons"})
    # Overflow labels
    slides.append({"layout": "kpi_dashboard", "headline": "Overflow", "metrics": [
        {"number": "999,999", "label": "A very long label that should test wrapping behavior in the small card container", "icon": _icon(i)}
        for i in range(4)
    ], "notes": "TEST: overflow — long labels"})
    # Padding
    for i in range(25 - len(slides)):
        n = (i % 6) + 2
        slides.append({"layout": "kpi_dashboard", "headline": f"Test {i+1}", "metrics": [
            {"number": str(j*10+i), "label": f"M{j+1}", "icon": _icon(j)} for j in range(n)
        ], "notes": f"TEST: variant {i+1} — {n} metrics"})
    return slides[:25]


def gen_roadmap():
    """25 roadmap variations."""
    slides = []
    q4 = ["Q1 2026", "Q2 2026", "Q3 2026", "Q4 2026"]
    q8 = ["Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025", "Q1 2026", "Q2 2026", "Q3 2026", "Q4 2026"]
    # Minimal
    slides.append({"layout": "roadmap", "headline": "Timeline", "time_axis": ["Q1", "Q2"], "swimlanes": [{"name": "Work", "items": [{"label": "Do", "start": "Q1", "end": "Q2", "status": "active"}]}], "notes": "TEST: minimal — 2 periods, 1 lane, 1 bar"})
    # Typical
    slides.append({"layout": "roadmap", "headline": "Cloud Migration Roadmap", "time_axis": q4, "swimlanes": [
        {"name": "GCP", "items": [{"label": "Assess", "start": "Q1 2026", "end": "Q1 2026", "status": "complete"}, {"label": "Wave 1", "start": "Q2 2026", "end": "Q3 2026", "status": "active"}]},
        {"name": "AWS", "items": [{"label": "MAP 2.0", "start": "Q1 2026", "end": "Q2 2026", "status": "active"}]},
    ], "milestones": [{"date": "Q4 2026", "label": "DC Exit"}], "notes": "TEST: typical — 2 lanes, milestone"})
    # Dense — many lanes and items
    slides.append({"layout": "roadmap", "headline": "Dense Roadmap", "time_axis": q4, "swimlanes": [
        {"name": f"Lane {i+1}", "items": [
            {"label": f"Phase {j+1}", "start": q4[j % len(q4)], "end": q4[min(j+1, len(q4)-1)], "status": ["complete", "active", "planned"][j % 3]}
            for j in range(3)
        ]} for i in range(4)
    ], "notes": "TEST: dense — 4 lanes, 3 items each"})
    # Long time axis
    slides.append({"layout": "roadmap", "headline": "8-Quarter Roadmap", "time_axis": q8, "swimlanes": [
        {"name": "Migration", "items": [{"label": "Full Program", "start": "Q1 2025", "end": "Q4 2026", "status": "active"}]},
    ], "notes": "TEST: edge — 8 periods"})
    # Milestones only
    slides.append({"layout": "roadmap", "headline": "Milestones", "time_axis": q4, "swimlanes": [], "milestones": [
        {"date": "Q1 2026", "label": "Kickoff"}, {"date": "Q3 2026", "label": "Wave 1"}, {"date": "Q4 2026", "label": "Exit"},
    ], "notes": "TEST: edge — milestones only, no swimlanes"})
    # Overflow
    slides.append({"layout": "roadmap", "headline": LONG_TITLES[0], "time_axis": q4, "swimlanes": [
        {"name": "Very Long Swimlane Name That Tests Wrapping", "items": [{"label": "Very Long Bar Label That Should Fit", "start": "Q1 2026", "end": "Q4 2026", "status": "active"}]},
    ], "notes": "TEST: overflow — long names"})
    # Padding
    for i in range(25 - len(slides)):
        n_lanes = (i % 3) + 1
        slides.append({"layout": "roadmap", "headline": f"Test {i+1}", "time_axis": q4[:3+i%2], "swimlanes": [
            {"name": f"Lane {j+1}", "items": [{"label": f"Work {j+1}", "start": q4[0], "end": q4[1], "status": "active"}]}
            for j in range(n_lanes)
        ], "notes": f"TEST: variant {i+1}"})
    return slides[:25]


def gen_before_after():
    """25 before_after variations."""
    slides = []
    # Minimal
    slides.append({"layout": "before_after", "headline": "Change", "before": {"label": "Before", "items": ["Old"]}, "after": {"label": "After", "items": ["New"]}, "notes": "TEST: minimal — 1 item each"})
    # Typical
    slides.append({"layout": "before_after", "headline": "Infrastructure Transformation", "before": {"label": "Current State", "icon": "server-stack", "items": ["10 on-prem data centers", "1,300 VMs", "Manual provisioning"]}, "after": {"label": "Target State", "icon": "cloud-network", "items": ["Multi-cloud GCP + AWS", "K8s platform", "IaC provisioning"]}, "arrow_label": "Migration", "notes": "TEST: typical — all fields"})
    # Dense
    slides.append({"layout": "before_after", "headline": "Dense Transform", "before": {"label": "Before", "icon": "server-stack", "items": [f"Before item {i+1} with description" for i in range(8)]}, "after": {"label": "After", "icon": "cloud-network", "items": [f"After item {i+1} with description" for i in range(8)]}, "arrow_label": "Transform", "notes": "TEST: dense — 8 items each side"})
    # No icons
    slides.append({"layout": "before_after", "headline": "No Icons", "before": {"label": "Old", "items": ["A", "B", "C"]}, "after": {"label": "New", "items": ["X", "Y", "Z"]}, "notes": "TEST: edge — no icons"})
    # Unbalanced
    slides.append({"layout": "before_after", "headline": "Unbalanced", "before": {"label": "Before", "items": ["One item"]}, "after": {"label": "After", "items": [f"Item {i+1}" for i in range(6)]}, "notes": "TEST: edge — unbalanced sides"})
    # Overflow
    slides.append({"layout": "before_after", "headline": LONG_TITLES[0], "before": {"label": "Before", "items": [OVERFLOW_TEXT[:60]]}, "after": {"label": "After", "items": [OVERFLOW_TEXT[:60]]}, "notes": "TEST: overflow — long text"})
    # Padding
    for i in range(25 - len(slides)):
        slides.append({"layout": "before_after", "headline": f"Test {i+1}", "before": {"label": "Before", "icon": _icon(i), "items": [f"Item {j+1}" for j in range(2+i%3)]}, "after": {"label": "After", "icon": _icon(i+5), "items": [f"Item {j+1}" for j in range(2+i%3)]}, "notes": f"TEST: variant {i+1}"})
    return slides[:25]


def gen_numbered_list():
    """25 numbered_list variations."""
    slides = []
    # Minimal
    slides.append({"layout": "numbered_list", "headline": "Steps", "items": [{"title": "Step One", "body": "Do this."}], "notes": "TEST: minimal — 1 item"})
    slides.append({"layout": "numbered_list", "headline": "Steps", "items": ["Plain string item"], "notes": "TEST: minimal — plain string"})
    # Typical
    slides.append({"layout": "numbered_list", "headline": "Decision Framework", "items": [
        {"title": "Select Organization Model", "body": "Choose single-org vs. dual-org based on governance requirements"},
        {"title": "Engage Migration Partner", "body": "Complete RFP with 3 shortlisted vendors"},
        {"title": "Execute Assessment Phase", "body": "2-day workshop, app discovery, dependency mapping"},
    ], "notes": "TEST: typical — 3 items with title+body"})
    # Dense
    slides.append({"layout": "numbered_list", "headline": "Many Steps", "items": [
        {"title": f"Step {i+1}", "body": f"Description for step {i+1} with enough text to test wrapping behavior"}
        for i in range(7)
    ], "notes": "TEST: dense — 7 items"})
    # Overflow
    slides.append({"layout": "numbered_list", "headline": "Overflow", "items": [
        {"title": LONG_TITLES[0], "body": LONG_BODY[:200]},
        {"title": "Normal", "body": "Short"},
    ], "notes": "TEST: overflow — very long first item"})
    # Title only (no body)
    slides.append({"layout": "numbered_list", "headline": "Titles Only", "items": [
        {"title": f"Priority {i+1}"} for i in range(5)
    ], "notes": "TEST: edge — titles only, no body text"})
    # Padding
    for i in range(25 - len(slides)):
        n = (i % 5) + 1
        slides.append({"layout": "numbered_list", "headline": f"Test {i+1}", "items": [
            {"title": f"Item {j+1}", "body": f"Body for item {j+1}"} for j in range(n)
        ], "notes": f"TEST: variant {i+1} — {n} items"})
    return slides[:25]


def gen_status_board():
    """25 status_board variations."""
    slides = []
    # Minimal
    slides.append({"layout": "status_board", "headline": "Status", "items": [{"name": "Project", "status": "green", "summary": "OK"}], "notes": "TEST: minimal — 1 item"})
    # Typical
    slides.append({"layout": "status_board", "headline": "Program Health", "items": [
        {"name": "GCP Migration", "status": "green", "summary": "On track. Assessment complete."},
        {"name": "AWS Migration", "status": "amber", "summary": "Partner selection delayed."},
        {"name": "Security", "status": "green", "summary": "Controls deployed."},
        {"name": "FinOps", "status": "red", "summary": "Cost model not finalized."},
    ], "as_of": "March 28, 2026", "notes": "TEST: typical — 4 items with as_of"})
    # Dense
    slides.append({"layout": "status_board", "headline": "Dense Status", "items": [
        {"name": f"Workstream {i+1}", "status": ["green", "amber", "red"][i%3], "summary": f"Status description for workstream {i+1} with enough text to test wrapping"}
        for i in range(8)
    ], "notes": "TEST: dense — 8 items"})
    # Long summaries
    slides.append({"layout": "status_board", "headline": "Long Summaries", "items": [
        {"name": "Project", "status": "amber", "summary": LONG_BODY[:200]},
        {"name": "Other", "status": "red", "summary": LONG_BODY[:200]},
    ], "notes": "TEST: overflow — long summaries"})
    # All same status
    slides.append({"layout": "status_board", "headline": "All Green", "items": [
        {"name": f"Item {i+1}", "status": "green", "summary": "On track"} for i in range(5)
    ], "notes": "TEST: edge — all green"})
    slides.append({"layout": "status_board", "headline": "All Red", "items": [
        {"name": f"Item {i+1}", "status": "red", "summary": "Blocked"} for i in range(5)
    ], "notes": "TEST: edge — all red"})
    # Padding
    for i in range(25 - len(slides)):
        n = (i % 4) + 2
        slides.append({"layout": "status_board", "headline": f"Test {i+1}", "items": [
            {"name": f"Item {j+1}", "status": ["green", "amber", "red"][j%3], "summary": f"Summary {j+1}"}
            for j in range(n)
        ], "notes": f"TEST: variant {i+1}"})
    return slides[:25]


def gen_content_table():
    """25 content_table variations."""
    slides = []
    # Minimal
    slides.append({"layout": "content_table", "headline": "Table", "columns": ["A", "B"], "rows": [["1", "2"]], "notes": "TEST: minimal — 2x1"})
    # Typical
    slides.append({"layout": "content_table", "headline": "Cloud Comparison", "columns": ["Capability", "AWS", "GCP", "Weight"], "rows": [
        ["VM Migration", "SMS + MGN", "Migrate to VMs", "25%"],
        ["K8s Platform", "EKS", "GKE", "20%"],
        ["Database", "Aurora", "Cloud SQL", "20%"],
    ], "notes": "TEST: typical — 4 cols, 3 rows"})
    # Dense
    slides.append({"layout": "content_table", "headline": "Dense Table", "columns": [f"Col {i+1}" for i in range(7)], "rows": [
        [f"R{r}C{c}" for c in range(7)] for r in range(8)
    ], "notes": "TEST: dense — 7 cols, 8 rows"})
    # Striped off
    slides.append({"layout": "content_table", "headline": "No Stripe", "columns": ["A", "B", "C"], "rows": [["1", "2", "3"], ["4", "5", "6"]], "stripe": False, "notes": "TEST: edge — stripe off"})
    # Padding
    for i in range(25 - len(slides)):
        cols = (i % 4) + 2
        rows = (i % 5) + 1
        slides.append({"layout": "content_table", "headline": f"Test {i+1}", "columns": [f"C{c+1}" for c in range(cols)], "rows": [[f"R{r}C{c}" for c in range(cols)] for r in range(rows)], "notes": f"TEST: variant {i+1} — {cols}x{rows}"})
    return slides[:25]


def gen_matrix():
    """25 matrix variations."""
    slides = []
    cc = {"R": "5F016F", "A": "FF80D4", "C": "F0E8F5", "I": "FFFFFF"}
    legend = "R = Responsible | A = Accountable | C = Consulted | I = Informed"
    # Minimal
    slides.append({"layout": "matrix", "headline": "Matrix", "row_header": "Item", "columns": ["A", "B"], "rows": [{"label": "Row 1", "values": ["R", "A"]}], "cell_colors": cc, "notes": "TEST: minimal — 2x1"})
    # Typical
    slides.append({"layout": "matrix", "headline": "RACI", "row_header": "Workstream", "columns": ["Engineering", "Security", "IT", "Business"], "rows": [
        {"label": "Infrastructure", "values": ["R", "A", "C", "I"]},
        {"label": "Security", "values": ["C", "R", "A", "I"]},
        {"label": "Application", "values": ["R", "C", "I", "A"]},
    ], "cell_colors": cc, "legend": legend, "notes": "TEST: typical — 4x3 RACI"})
    # Dense
    slides.append({"layout": "matrix", "headline": "Dense Matrix", "row_header": "Component", "columns": [f"Team {i+1}" for i in range(6)], "rows": [
        {"label": f"Component {r+1}", "values": ["R", "A", "C", "I", "R", "C"][:6]} for r in range(8)
    ], "cell_colors": cc, "legend": legend, "notes": "TEST: dense — 6x8"})
    # No legend
    slides.append({"layout": "matrix", "headline": "No Legend", "row_header": "Row", "columns": ["X", "Y"], "rows": [{"label": "A", "values": ["R", "A"]}], "cell_colors": cc, "notes": "TEST: edge — no legend"})
    # Padding
    for i in range(25 - len(slides)):
        cols = (i % 4) + 2
        rows = (i % 4) + 1
        slides.append({"layout": "matrix", "headline": f"Test {i+1}", "row_header": "Row", "columns": [f"C{c+1}" for c in range(cols)], "rows": [
            {"label": f"R{r+1}", "values": ["R", "A", "C", "I"][:cols]} for r in range(rows)
        ], "cell_colors": cc, "notes": f"TEST: variant {i+1} — {cols}x{rows}"})
    return slides[:25]


def gen_quote():
    """25 quote variations."""
    slides = []
    # Minimal
    slides.append({"layout": "quote", "quote_text": "Simple quote.", "notes": "TEST: minimal — quote only"})
    slides.append({"layout": "quote", "quote_text": "Quote.", "attribution": "Person", "notes": "TEST: minimal — quote + attribution"})
    # Typical
    slides.append({"layout": "quote", "headline": "Strategic Vision", "quote_text": "Cloud-first is not just a technology decision — it is a business imperative for Acme Corp's next chapter.", "attribution": "Sarah Chen, CTO", "attribution_title": "Acme Corp Technology Leadership Summit, Q1 2026", "notes": "TEST: typical — all fields"})
    # Dense
    slides.append({"layout": "quote", "headline": "Long Quote", "quote_text": LONG_BODY[:300], "attribution": "Very Long Attribution Name Title Goes Here", "attribution_title": "At a Very Important Event with a Very Long Name", "notes": "TEST: dense — long quote"})
    # Left aligned
    slides.append({"layout": "quote", "quote_text": "Left-aligned quote text for a different visual style.", "attribution": "Author", "style": "left-aligned", "notes": "TEST: edge — left aligned"})
    # With icon
    slides.append({"layout": "quote", "quote_text": "Quote with icon.", "attribution": "Author", "icon": "lightbulb", "notes": "TEST: edge — with icon"})
    # Overflow
    slides.append({"layout": "quote", "quote_text": OVERFLOW_TEXT[:200], "attribution": OVERFLOW_TEXT[:60], "notes": "TEST: overflow — long text"})
    # Padding
    for i in range(25 - len(slides)):
        slides.append({"layout": "quote", "headline": f"Quote {i+1}", "quote_text": f"This is test quote number {i+1} with varying length text to test the layout.", "attribution": f"Author {i+1}", "notes": f"TEST: variant {i+1}"})
    return slides[:25]


def gen_funnel():
    """25 funnel variations."""
    slides = []
    # Minimal
    slides.append({"layout": "funnel", "headline": "Funnel", "stages": [{"label": "All", "value": "100", "width": 100}, {"label": "Some", "value": "50", "width": 50}], "notes": "TEST: minimal — 2 stages"})
    # Typical
    slides.append({"layout": "funnel", "headline": "Technology Pipeline", "stages": [
        {"label": "Evaluated", "value": "2,667 repos", "width": 100},
        {"label": "Cataloged", "value": "1,200 services", "width": 60},
        {"label": "Owned", "value": "850 services", "width": 40},
        {"label": "Standardized", "value": "340 services", "width": 20},
    ], "notes": "TEST: typical — 4 stages"})
    # Dense
    slides.append({"layout": "funnel", "headline": "Deep Funnel", "stages": [
        {"label": f"Stage {i+1}", "value": f"{1000-i*100} items", "width": 100-i*12}
        for i in range(8)
    ], "notes": "TEST: dense — 8 stages"})
    # No values
    slides.append({"layout": "funnel", "headline": "No Values", "stages": [
        {"label": f"Stage {i+1}", "width": 100-i*20} for i in range(5)
    ], "notes": "TEST: edge — no value text"})
    # Overflow
    slides.append({"layout": "funnel", "headline": "Overflow", "stages": [
        {"label": "Very Long Stage Label That Tests Wrapping", "value": "Very Long Value Text", "width": 100},
        {"label": "Short", "value": "5", "width": 30},
    ], "notes": "TEST: overflow — long labels"})
    # Padding
    for i in range(25 - len(slides)):
        n = (i % 5) + 2
        slides.append({"layout": "funnel", "headline": f"Test {i+1}", "stages": [
            {"label": f"Level {j+1}", "value": str(100-j*15), "width": 100-j*(80//n)}
            for j in range(n)
        ], "notes": f"TEST: variant {i+1} — {n} stages"})
    return slides[:25]


def gen_callout():
    """25 callout variations."""
    slides = []
    # Minimal
    slides.append({"layout": "callout", "callout_text": "Key point.", "notes": "TEST: minimal — callout only"})
    # Typical boxed
    slides.append({"layout": "callout", "callout_text": "We recommend Option A — Single GCP Organization.", "supporting_text": "Simpler governance, unified billing, single security surface.", "icon": "lightbulb", "style": "boxed", "notes": "TEST: typical — boxed with icon"})
    # Typical open
    slides.append({"layout": "callout", "callout_text": "Key takeaway for the audience.", "supporting_text": "Supporting rationale and context.", "style": "open", "notes": "TEST: typical — open style"})
    # Dense
    slides.append({"layout": "callout", "callout_text": LONG_TITLES[0], "supporting_text": LONG_BODY[:300], "icon": "lightbulb", "style": "boxed", "notes": "TEST: dense — long text boxed"})
    # No supporting text
    slides.append({"layout": "callout", "callout_text": "Single statement with no supporting text.", "style": "boxed", "notes": "TEST: edge — no supporting text"})
    # No icon
    slides.append({"layout": "callout", "callout_text": "No icon callout.", "supporting_text": "Context.", "style": "boxed", "notes": "TEST: edge — no icon"})
    # Overflow
    slides.append({"layout": "callout", "callout_text": OVERFLOW_TEXT[:150], "supporting_text": OVERFLOW_TEXT[:200], "style": "open", "notes": "TEST: overflow — long text open"})
    # Padding
    for i in range(25 - len(slides)):
        slides.append({"layout": "callout", "callout_text": f"Test callout {i+1} with varying content.", "supporting_text": f"Supporting text for variant {i+1}.", "icon": _icon(i) if i % 2 == 0 else "", "style": ["boxed", "open"][i%2], "notes": f"TEST: variant {i+1}"})
    return slides[:25]


def gen_closing():
    """25 closing variations."""
    slides = []
    # Minimal
    slides.append({"layout": "closing", "notes": "TEST: minimal — defaults only"})
    slides.append({"layout": "closing", "headline": "Questions?", "notes": "TEST: minimal — explicit headline"})
    # Typical
    slides.append({"layout": "closing", "headline": "Questions?", "subheader": "Cloud Migration — Acme Corp", "background": "p12", "notes": "TEST: typical — all fields"})
    # Different text
    slides.append({"layout": "closing", "headline": "Thank You", "subheader": "Jane Smith\nHead of Platform Engineering\njane.smith@example.com", "background": "p13", "notes": "TEST: typical — thank you with contact"})
    # Contact info
    slides.append({"layout": "closing", "headline": "Let's Connect", "contact_info": "Jane Smith\nVP of Engineering\njane.smith@example.com\n+1 (555) 123-4567", "background": "p12", "notes": "TEST: edge — contact info"})
    # No background
    slides.append({"layout": "closing", "headline": "Questions?", "subheader": "No background", "notes": "TEST: edge — no background"})
    # Overflow
    slides.append({"layout": "closing", "headline": LONG_TITLES[0], "subheader": LONG_BODY[:200], "background": "p12", "notes": "TEST: overflow — long headline and sub"})
    # Padding
    for i in range(25 - len(slides)):
        slides.append({"layout": "closing", "headline": ["Questions?", "Thank You", "Discussion"][i%3], "subheader": f"Test {i+1}", "background": ["p12", "p13", "p17"][i%3], "notes": f"TEST: variant {i+1}"})
    return slides[:25]


def gen_image_showcase():
    """25 image_showcase variations — uses title-assets as test images."""
    slides = []
    imgs = ["title-assets/title-bg-p12.jpg", "title-assets/title-bg-p13.jpg", "title-assets/agenda-left-p22.jpg"]
    # Minimal
    slides.append({"layout": "image_showcase", "headline": "Image", "image": imgs[0], "notes": "TEST: minimal — image only"})
    # Typical
    slides.append({"layout": "image_showcase", "headline": "Architecture Diagram", "image": imgs[0], "caption": "Source: GCP Cloud Architecture Center", "notes": "TEST: typical — with caption"})
    # Border
    slides.append({"layout": "image_showcase", "headline": "With Border", "image": imgs[1], "caption": "Bordered image", "border": True, "notes": "TEST: edge — with border"})
    # No caption
    slides.append({"layout": "image_showcase", "headline": "No Caption", "image": imgs[2], "notes": "TEST: edge — no caption"})
    # Different images
    for i, img in enumerate(imgs):
        slides.append({"layout": "image_showcase", "headline": f"Image {i+1}", "image": img, "caption": f"Test image {i+1}", "notes": f"TEST: variant — image {i+1}"})
    # Padding
    for i in range(25 - len(slides)):
        slides.append({"layout": "image_showcase", "headline": f"Test {i+1}", "image": imgs[i%len(imgs)], "caption": f"Caption {i+1}", "notes": f"TEST: variant {i+1}"})
    return slides[:25]


def gen_content_two_col():
    """25 content_two_col (stacked) variations."""
    slides = []
    # Minimal
    slides.append({"layout": "content_two_col", "headline": "Overview", "variants": 1, "left_stats": [{"number": "42", "label": "Stat"}], "left_title": "Left", "left_body": "Content", "right_title": "Right", "right_body": "Content", "notes": "TEST: minimal — 1 stat"})
    # Typical
    slides.append({"layout": "content_two_col", "headline": "Program Overview", "variants": 1, "left_stats": [
        {"number": "1,300", "label": "VMs", "icon": "server-stack"},
        {"number": "10", "label": "Data Centers", "icon": "buildings"},
        {"number": "EOY 2026", "label": "Deadline", "icon": "calendar-day"},
    ], "left_icon": "clock", "left_title": "Timeline", "left_body": MEDIUM_BODY, "right_icon": "checklist", "right_title": "Phases", "right_body": "Phase 1: K8s-based\nPhase 2: K8s-capable\nPhase 3: Updates", "notes": "TEST: typical — 3 stats, icons"})
    # Dense
    slides.append({"layout": "content_two_col", "headline": "Dense", "variants": 1, "left_stats": [
        {"number": str(i*100), "label": f"Metric {i+1}", "icon": _icon(i)} for i in range(5)
    ], "left_icon": "gear", "left_title": "Long Title", "left_body": LONG_BODY[:300], "right_icon": "padlock", "right_title": "Long Title", "right_body": LONG_BODY[:300], "notes": "TEST: dense — 5 stats, long body"})
    # No icons
    slides.append({"layout": "content_two_col", "headline": "No Icons", "variants": 1, "left_stats": [{"number": "100", "label": "Count"}], "left_title": "Left", "left_body": "Content", "right_title": "Right", "right_body": "Content", "notes": "TEST: edge — no icons"})
    # Padding
    for i in range(25 - len(slides)):
        slides.append({"layout": "content_two_col", "headline": f"Test {i+1}", "variants": 1, "left_stats": [
            {"number": str(i*10+j), "label": f"Stat {j+1}", "icon": _icon(j)} for j in range(2+i%2)
        ], "left_icon": _icon(i), "left_title": f"Left {i+1}", "left_body": MEDIUM_BODY[:80*(i%3+1)], "right_icon": _icon(i+3), "right_title": f"Right {i+1}", "right_body": MEDIUM_BODY[:80*((i+1)%3+1)], "notes": f"TEST: variant {i+1}"})
    return slides[:25]


# ---------------------------------------------------------------------------
# Main generator
# ---------------------------------------------------------------------------

LAYOUT_GENERATORS = {
    "title_cover": gen_title_cover,
    "agenda": gen_agenda,
    "section_divider": gen_section_divider,
    "closing": gen_closing,
    "content_two_col": gen_content_two_col,
    "side_by_side": gen_side_by_side,
    "three_column": gen_three_column,
    "four_card": gen_four_card,
    "numbered_list": gen_numbered_list,
    "before_after": gen_before_after,
    "content_table": gen_content_table,
    "matrix": gen_matrix,
    "kpi_dashboard": gen_kpi_dashboard,
    "status_board": gen_status_board,
    "big_stat_manual": gen_big_stat,
    "quote": gen_quote,
    "callout": gen_callout,
    "roadmap": gen_roadmap,
    "funnel": gen_funnel,
    "image_showcase": gen_image_showcase,
}


def generate_test_yaml(output_path="test-layouts.yaml"):
    """Generate the full test YAML with 25 variations per layout."""
    all_slides = []
    layout_counts = {}

    for layout_name, gen_fn in LAYOUT_GENERATORS.items():
        slides = gen_fn()
        layout_counts[layout_name] = len(slides)
        all_slides.extend(slides)

    deck = {
        "title": "Layout Test Suite",
        "date": "2026-03-28",
        "style": "corporate",
        "diagram_variants": 1,
        "slides": all_slides,
    }

    with open(output_path, "w") as f:
        yaml.dump(deck, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    total = len(all_slides)
    print(f"Generated: {output_path}")
    print(f"  Layouts: {len(layout_counts)}")
    print(f"  Total slides: {total}")
    for name, count in layout_counts.items():
        print(f"    {name}: {count}")

    return output_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate layout test YAML")
    parser.add_argument("--output", default="test-layouts.yaml")
    args = parser.parse_args()
    generate_test_yaml(args.output)
