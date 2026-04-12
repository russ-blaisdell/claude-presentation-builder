#!/usr/bin/env python3
"""
Stress Test Generator — Creates YAML decks that exercise every layout
at multiple content levels for golden reference regression testing.

For each layout, tests the cross-product of:
  - Item count (min → mid → max → over-max)
  - Text length per item (short → medium → long)
  - Optional fields (with/without icons, subtitles, notes)

Target: 8-10 variants per layout, ~450 total slides.

Output: One YAML file per layout batch, organized in stress-tests/ directory.
"""

import os
import yaml

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stress-tests")
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Text generators at different lengths
# ---------------------------------------------------------------------------

def short(n=1):
    words = ["Plan", "Build", "Test", "Ship", "Scale", "Fix", "Launch", "Grow",
             "Lead", "Track", "Review", "Audit", "Report", "Alert", "Deploy",
             "Analyze", "Migrate", "Secure", "Monitor", "Optimize"]
    return words[n % len(words)]

def medium(n=1):
    phrases = [
        "Cloud migration Phase 1", "Security posture review", "Platform modernization",
        "Developer experience team", "Infrastructure automation", "Cost optimization sprint",
        "Kubernetes adoption plan", "Monitoring and alerting", "Database consolidation",
        "Identity management overhaul", "Fleet census pipeline", "Design system rollout",
        "On-call transition program", "Compliance certification", "Partner evaluation process",
        "API gateway replacement", "Service mesh deployment", "Capacity planning review",
        "Disaster recovery exercise", "Release automation pipeline",
    ]
    return phrases[n % len(phrases)]

def long(n=1):
    sentences = [
        "Migrate 1,300 VMs from on-premises data centers to multi-cloud GCP and AWS infrastructure by EOY 2026",
        "Implement unified identity management across consumer, corporate, machine-to-machine, and IoT domains",
        "Establish automated security scanning pipeline with SAST, DAST, SCA, and container image scanning",
        "Deploy multi-region active-active database cluster for disaster recovery across AWS and GCP",
        "Transition operational ownership from centralized SRE team to individual engineering teams with full on-call",
        "Build self-service developer platform with golden paths for CI/CD, observability, secrets, and compute",
        "Execute comprehensive cloud cost optimization through reserved instances, right-sizing, and spot usage",
        "Standardize fleet-wide technology adoption across 12 teams spanning compute, storage, CI/CD, and observability",
        "Complete partner evaluation across cloud providers, managed services, and security tooling vendors by Q3 2026",
        "Consolidate monitoring stacks from three vendor solutions to a unified observability platform with full-stack traces",
    ]
    return sentences[n % len(sentences)]

def bullet_items(count, length="medium"):
    fn = {"short": short, "medium": medium, "long": long}[length]
    return [fn(i) for i in range(count)]

ICONS = ["server-stack", "cloud-network", "padlock", "coin-stacks", "checklist",
         "dashboard-gauge", "lightbulb", "three-stars", "team-network", "circle-check",
         "chart-bars", "clipboard", "telescope", "globe", "speedometer"]

def icon(n=0):
    return ICONS[n % len(ICONS)]

# ---------------------------------------------------------------------------
# Layout test definitions — each targets 8-10 variants
# ---------------------------------------------------------------------------

def gen_structural():
    """title_cover, agenda, section_divider, closing — ~28 slides"""
    slides = []

    # title_cover: 6 variants (short/med/long × with/without subheader × backgrounds)
    for label, hl in [
        ("min", "Q1 Update"),
        ("med", "Cloud Infrastructure — Modernization Program"),
        ("max", "Quarterly Business Review — Engineering Platform and Developer Experience Organization — April 2026"),
    ]:
        slides.append({"layout": "title_cover", "headline": hl, "subheader": f"Stress test: {label}", "background": "p12"})
    slides.append({"layout": "title_cover", "headline": "Annual Review", "background": "p13"})  # no subheader
    slides.append({"layout": "title_cover", "headline": "Platform Strategy — Next Steps", "subheader": "Engineering Leadership", "background": "p17"})
    slides.append({"layout": "title_cover", "headline": "Security and Compliance — Annual Certification Review", "subheader": "Prepared for VP Engineering and CTO", "background": "p12"})

    # agenda: 8 variants (3/5/7 items × short/long, plus edge cases)
    for count in [3, 5, 7]:
        for length, fn in [("short", short), ("long", medium)]:
            slides.append({"layout": "agenda", "headline": f"Agenda ({count} items, {length})",
                           "items": [fn(i) for i in range(count)]})
    slides.append({"layout": "agenda", "headline": "Workshop Topics", "background": "p21",
                   "items": [long(i) for i in range(4)]})
    slides.append({"layout": "agenda", "headline": "All Hands", "background": "p23",
                   "items": [medium(i) for i in range(6)]})

    # section_divider: 8 variants (backgrounds × with/without subheader/icon × section numbers)
    for bg in ["purple", "light", "image"]:
        slides.append({"layout": "section_divider", "section_number": "01",
                       "headline": f"Section ({bg} bg)", "background": bg})
    slides.append({"layout": "section_divider", "section_number": "02", "headline": "Strategic Context",
                   "subheader": "Scale, timeline, and dependencies", "background": "purple", "icon": "telescope"})
    slides.append({"layout": "section_divider", "section_number": "03", "headline": "Technical Architecture and Migration Plan",
                   "subheader": "Multi-cloud infrastructure, networking, and disaster recovery design across all regions",
                   "background": "light"})
    slides.append({"layout": "section_divider", "section_number": "04", "headline": "Appendix",
                   "background": "purple", "icon": "clipboard"})
    slides.append({"layout": "section_divider", "headline": "Discussion", "background": "light"})  # no section_number
    slides.append({"layout": "section_divider", "section_number": "05",
                   "headline": "Financial Impact and Cost Optimization", "background": "image"})

    # closing: 4 variants
    for hl, bg in [("Questions?", "p12"), ("Thank You", "p13"),
                   ("Next Steps and Follow-Up Actions", "p12"),
                   ("End of Presentation — Cloud Infrastructure Program Review", "p17")]:
        slides.append({"layout": "closing", "headline": hl, "background": bg})

    return slides

def gen_single_message():
    """big_stat_manual, callout, quote — ~26 slides"""
    slides = []

    # big_stat_manual: 8 variants (different numbers, labels, with/without icon/context)
    for num, lbl, ic in [
        ("1,300+", "VMs migrated", "server-stack"),
        ("$2.1M", "Annual savings", "coin-stacks"),
        ("99.99%", "Uptime SLA", "speedometer"),
        ("47", "Active services", "cloud-network"),
    ]:
        slides.append({"layout": "big_stat_manual", "headline": "Key Metric",
                       "number": num, "label": lbl, "icon": ic})
    slides.append({"layout": "big_stat_manual", "headline": "Program Scale",
                   "number": "12", "label": "Teams participating in the migration program across three continents"})
    slides.append({"layout": "big_stat_manual", "headline": "Milestone",
                   "number": "Q3", "label": "Target completion", "icon": "checklist",
                   "context": "On track with 60% of workloads migrated"})
    # alias test: big_stat → big_stat_manual
    slides.append({"layout": "big_stat", "headline": "Alias Test",
                   "number": "100%", "label": "Coverage", "icon": "circle-check"})
    slides.append({"layout": "big_stat_manual", "headline": "Long Label Test",
                   "number": "3.2x", "label": "Performance improvement after migrating from legacy on-premises infrastructure to cloud-native containerized architecture with auto-scaling"})

    # callout: 8 variants (boxed/open × short/medium/long × with/without supporting text)
    for style in ["boxed", "open"]:
        for ct, sup in [
            ("Invest $2M in cloud migration.", None),
            (medium(1), "This approach provides simpler governance and unified billing."),
            (long(1), "Key recommendation from the architecture review board."),
            (medium(5), None),
        ]:
            s = {"layout": "callout", "callout_text": ct, "icon": "lightbulb", "style": style}
            if sup:
                s["supporting_text"] = sup
            slides.append(s)

    # quote: 8 variants (short/medium/long × with/without headline/attribution_title)
    for qt, attr, title, hl in [
        ("Cloud-first is our future.", "CTO", "Leadership Summit Q1 2026", "Vision"),
        (medium(0), "VP Engineering", "Architecture Review", "Strategy"),
        (long(0), "Head of Platform", "All-Hands Q1 2026", None),
        ("Simple. Fast. Secure.", "CEO", None, "Core Values"),
        (long(3), "Director of Security", "Annual Security Review", "Security Posture"),
        ("We ship features, not excuses.", "Engineering Lead", None, None),
    ]:
        s = {"layout": "quote", "quote_text": qt, "attribution": attr}
        if title:
            s["attribution_title"] = title
        if hl:
            s["headline"] = hl
        slides.append(s)

    return slides

def gen_content_layouts():
    """side_by_side, three_column, four_card, numbered_list, before_after — ~46 slides"""
    slides = []

    # side_by_side: 8 variants (text lengths × with/without icons)
    for length, fn in [("short", short), ("medium", medium), ("long", long)]:
        slides.append({"layout": "side_by_side", "headline": f"Side by Side ({length})",
                       "left_icon": "checklist", "left_title": "Option A",
                       "left_body": "\n".join(fn(i) for i in range(4)),
                       "right_icon": "three-stars", "right_title": "Option B",
                       "right_body": "\n".join(fn(i+4) for i in range(4))})
    # without icons
    slides.append({"layout": "side_by_side", "headline": "Comparison (no icons)",
                   "left_title": "Before", "left_body": "\n".join(medium(i) for i in range(5)),
                   "right_title": "After", "right_body": "\n".join(medium(i+5) for i in range(5))})
    # long body text
    slides.append({"layout": "side_by_side", "headline": "Deep Dive",
                   "left_icon": "padlock", "left_title": "Current Architecture",
                   "left_body": "\n".join(long(i) for i in range(3)),
                   "right_icon": "cloud-network", "right_title": "Target Architecture",
                   "right_body": "\n".join(long(i+3) for i in range(3))})
    # asymmetric content
    slides.append({"layout": "side_by_side", "headline": "Asymmetric Content",
                   "left_icon": "chart-bars", "left_title": "Summary",
                   "left_body": short(0),
                   "right_icon": "clipboard", "right_title": "Details",
                   "right_body": "\n".join(long(i) for i in range(4))})
    # alias test: content_three_section → three_column
    slides.append({"layout": "side_by_side", "headline": "Dense Comparison",
                   "left_icon": "server-stack", "left_title": "On-Premises",
                   "left_body": "\n".join(medium(i) for i in range(6)),
                   "right_icon": "cloud-network", "right_title": "Cloud-Native",
                   "right_body": "\n".join(medium(i+6) for i in range(6))})
    slides.append({"layout": "side_by_side", "headline": "Minimal Content",
                   "left_title": "Pro", "left_body": "Fast",
                   "right_title": "Con", "right_body": "Expensive"})

    # three_column: 8 variants
    for length, fn in [("short", short), ("medium", medium), ("long", long)]:
        slides.append({"layout": "three_column", "headline": f"Three Column ({length})",
                       "col1_icon": "padlock", "col1_title": "Security", "col1_body": "\n".join(fn(i) for i in range(3)),
                       "col2_icon": "coin-stacks", "col2_title": "Finance", "col2_body": "\n".join(fn(i+3) for i in range(3)),
                       "col3_icon": "dashboard-gauge", "col3_title": "Ops", "col3_body": "\n".join(fn(i+6) for i in range(3))})
    slides.append({"layout": "three_column", "headline": "Dense (no icons)",
                   "col1_title": "Phase 1", "col1_body": "\n".join(medium(i) for i in range(5)),
                   "col2_title": "Phase 2", "col2_body": "\n".join(medium(i+5) for i in range(5)),
                   "col3_title": "Phase 3", "col3_body": "\n".join(medium(i+10) for i in range(5))})
    slides.append({"layout": "three_column", "headline": "Minimal",
                   "col1_icon": "checklist", "col1_title": "Do", "col1_body": short(0),
                   "col2_icon": "lightbulb", "col2_title": "Think", "col2_body": short(1),
                   "col3_icon": "three-stars", "col3_title": "Review", "col3_body": short(2)})
    # alias test
    slides.append({"layout": "content_three_section", "headline": "Alias: content_three_section",
                   "col1_icon": "padlock", "col1_title": "A", "col1_body": medium(0),
                   "col2_icon": "coin-stacks", "col2_title": "B", "col2_body": medium(1),
                   "col3_icon": "dashboard-gauge", "col3_title": "C", "col3_body": medium(2)})
    slides.append({"layout": "three_column", "headline": "Long Bodies",
                   "col1_icon": "server-stack", "col1_title": "Infrastructure",
                   "col1_body": "\n".join(long(i) for i in range(2)),
                   "col2_icon": "padlock", "col2_title": "Security",
                   "col2_body": "\n".join(long(i+2) for i in range(2)),
                   "col3_icon": "cloud-network", "col3_title": "Networking",
                   "col3_body": "\n".join(long(i+4) for i in range(2))})
    slides.append({"layout": "three_column", "headline": "Asymmetric",
                   "col1_icon": "checklist", "col1_title": "Short", "col1_body": short(0),
                   "col2_icon": "clipboard", "col2_title": "Medium", "col2_body": "\n".join(medium(i) for i in range(3)),
                   "col3_icon": "telescope", "col3_title": "Long", "col3_body": "\n".join(long(i) for i in range(2))})

    # four_card: 10 variants (2/3/4/5/6/8 cards × short/long, with/without icons)
    for count in [2, 3, 4, 5, 6, 8]:
        for length, fn in [("short", short), ("long", medium)]:
            s = {"layout": "four_card", "headline": f"Cards ({count}, {length})"}
            for c in range(count):
                s[f"card{c+1}_title"] = fn(c)
                s[f"card{c+1}_body"] = fn(c + 10) if length == "short" else "\n".join(fn(c*3+j) for j in range(3))
                if length == "long":
                    s[f"card{c+1}_icon"] = icon(c)
            slides.append(s)
    # alias test
    s = {"layout": "content_four_cards", "headline": "Alias: content_four_cards"}
    for c in range(4):
        s[f"card{c+1}_title"] = medium(c)
        s[f"card{c+1}_body"] = medium(c + 10)
    slides.append(s)

    # numbered_list: 8 variants (3/5/7 items × short/medium/long)
    for count in [3, 5, 7]:
        for length, fn in [("short", short), ("medium", medium), ("long", long)]:
            slides.append({"layout": "numbered_list", "headline": f"Numbered ({count}, {length})",
                           "items": [{"title": fn(i), "body": fn(i+10)} for i in range(count)]})

    # before_after: 8 variants (3/5/7 items × short/medium/long × with/without arrow label)
    for count in [3, 5, 7]:
        for length in ["short", "medium", "long"]:
            s = {"layout": "before_after", "headline": f"Before/After ({count}, {length})",
                 "before": {"label": "Current", "icon": "server-stack",
                            "items": bullet_items(count, length)},
                 "after": {"label": "Target", "icon": "cloud-network",
                           "items": bullet_items(count, length)}}
            if count > 3:
                s["arrow_label"] = "Transformation"
            slides.append(s)

    return slides

def gen_data_layouts():
    """content_table, content_table_bullets, kpi_dashboard, status_board, matrix, comparison_matrix — ~54 slides"""
    slides = []

    # content_table: 12 variants (cols × rows × text length)
    for cols in [3, 5]:
        for rows in [4, 8, 12]:
            for length in ["short", "long"]:
                fn = short if length == "short" else medium
                columns = [f"Col {c+1}" for c in range(cols)]
                data_rows = [[fn(r * cols + c) for c in range(cols)] for r in range(rows)]
                slides.append({"layout": "content_table",
                               "headline": f"Table ({cols}x{rows}, {length})",
                               "columns": columns, "rows": data_rows})

    # content_table_bullets: 8 variants (cols × rows × with/without bullets)
    for cols in [3, 4]:
        for rows in [3, 5]:
            columns = [f"Category {c+1}" for c in range(cols)]
            data_rows = []
            for r in range(rows):
                row = []
                for c in range(cols):
                    if c == 0:
                        row.append(medium(r))
                    else:
                        row.append(f"- {short(r*cols+c)}\n- {short(r*cols+c+1)}")
                data_rows.append(row)
            slides.append({"layout": "content_table",
                           "headline": f"Table+Bullets ({cols}x{rows})",
                           "columns": columns, "rows": data_rows})
    # wide table
    columns = [f"C{c+1}" for c in range(7)]
    data_rows = [[short(r * 7 + c) for c in range(7)] for r in range(5)]
    slides.append({"layout": "content_table", "headline": "Wide Table (7 cols)",
                   "columns": columns, "rows": data_rows})
    # narrow deep table
    columns = ["Item", "Status", "Owner"]
    data_rows = [[medium(r), ["Active", "Blocked", "Complete"][r % 3], f"Person {r+1}"] for r in range(15)]
    slides.append({"layout": "content_table", "headline": "Deep Table (15 rows)",
                   "columns": columns, "rows": data_rows})

    # kpi_dashboard: 8 variants (2/3/4/6/8 metrics × with/without trends/targets)
    for count in [2, 3, 4, 6, 8]:
        metrics = []
        for i in range(count):
            m = {"number": str(100 + i * 37), "label": medium(i), "icon": icon(i)}
            if i % 2 == 0:
                m["trend"] = "up"
            if i % 3 == 0:
                m["target"] = str(200 + i * 20)
            metrics.append(m)
        slides.append({"layout": "kpi_dashboard", "headline": f"KPIs ({count})", "metrics": metrics})
    # minimal (no icons, no trends)
    slides.append({"layout": "kpi_dashboard", "headline": "KPIs (minimal)",
                   "metrics": [{"number": "42", "label": "Active"}, {"number": "7", "label": "Blocked"},
                               {"number": "99%", "label": "Uptime"}]})
    # with all optional fields
    slides.append({"layout": "kpi_dashboard", "headline": "KPIs (full detail)",
                   "metrics": [{"number": "$1.2M", "label": "Monthly spend", "icon": "coin-stacks", "trend": "down", "target": "$1.0M"},
                               {"number": "47", "label": "Services deployed", "icon": "cloud-network", "trend": "up", "target": "60"},
                               {"number": "99.9%", "label": "Availability", "icon": "speedometer", "trend": "up", "target": "99.95%"},
                               {"number": "12", "label": "Teams onboarded", "icon": "team-network", "trend": "up", "target": "15"}]})

    # status_board: 8 variants (3/5/7/10 items × with/without summary)
    for count in [3, 5, 7, 10]:
        statuses = ["green", "amber", "red"]
        items = [{"name": medium(i), "status": statuses[i % 3],
                  "summary": medium(i + 10)} for i in range(count)]
        slides.append({"layout": "status_board", "headline": f"Status ({count})", "items": items, "as_of": "April 2026"})
    # with short names
    slides.append({"layout": "status_board", "headline": "Status (short names)",
                   "items": [{"name": short(i), "status": ["green", "amber", "red", "green"][i % 4],
                              "summary": short(i + 5)} for i in range(6)], "as_of": "Q1 2026"})
    # with long summaries
    slides.append({"layout": "status_board", "headline": "Status (long summaries)",
                   "items": [{"name": medium(i), "status": ["green", "red"][i % 2],
                              "summary": long(i)} for i in range(4)], "as_of": "April 10, 2026"})

    # matrix (RACI): 8 variants
    for opts in [3, 4, 5]:
        for rows_count in [4, 6]:
            columns = [f"Team {c+1}" for c in range(opts)]
            vals = ["R", "A", "C", "I", ""]
            rows = [{"label": medium(r), "values": [vals[(r + c) % len(vals)] for c in range(opts)]} for r in range(rows_count)]
            slides.append({"layout": "matrix", "headline": f"RACI ({opts}x{rows_count})",
                           "row_header": "Activity", "columns": columns, "rows": rows,
                           "legend": "R=Responsible  A=Accountable  C=Consulted  I=Informed"})
    # small matrix
    slides.append({"layout": "matrix", "headline": "Simple Matrix",
                   "row_header": "Task", "columns": ["Dev", "Ops"],
                   "rows": [{"label": short(i), "values": [["R", "C"], ["A", "R"], ["C", "I"]][i % 3]} for i in range(3)]})
    # large matrix
    slides.append({"layout": "matrix", "headline": "Large Matrix (6x8)",
                   "row_header": "Workstream", "columns": [f"Team {c+1}" for c in range(6)],
                   "rows": [{"label": medium(r), "values": [["R", "A", "C", "I", "", "C"][(r+c) % 6] for c in range(6)]} for r in range(8)],
                   "legend": "R=Responsible  A=Accountable  C=Consulted  I=Informed"})

    # comparison_matrix: 8 variants (2-5 options × 3-8 criteria)
    for opts in [2, 3, 4, 5]:
        for criteria in [4, 7]:
            cols = [f"Option {c+1}" for c in range(opts)]
            vals = ["full", "three-quarter", "half", "quarter", "none", "check", "cross"]
            rows = [{"label": medium(r), "values": [vals[(r + c) % len(vals)] for c in range(opts)]} for r in range(criteria)]
            slides.append({"layout": "comparison_matrix",
                           "headline": f"Comparison ({opts} options x {criteria} criteria)",
                           "row_header": "Criteria", "columns": cols, "rows": rows})

    return slides

def gen_process_flow():
    """process_flow, staircase, cycle_diagram, hub_spoke, funnel, roadmap — ~56 slides"""
    slides = []

    # process_flow: 10 variants (3/4/5/6 steps × short/long × chevron/arrow)
    for count in [3, 4, 5, 6]:
        for length, fn in [("short", short), ("long", medium)]:
            steps = [{"label": fn(i), "body": fn(i + 10),
                      "status": ["complete", "active", ""][min(i, 2)]} for i in range(count)]
            slides.append({"layout": "process_flow", "headline": f"Flow ({count} steps, {length})",
                           "style": "chevron", "steps": steps})
    # arrow style
    slides.append({"layout": "process_flow", "headline": "Flow (arrow style)",
                   "style": "arrow", "steps": [{"label": medium(i), "body": short(i)} for i in range(5)]})
    # no body text
    slides.append({"layout": "process_flow", "headline": "Flow (labels only)",
                   "style": "chevron", "steps": [{"label": medium(i)} for i in range(4)]})

    # staircase: 8 variants (3/4/5 levels × different current_level)
    for count in [3, 4, 5]:
        for cur in [1, count]:
            levels = [{"label": medium(i), "body": short(i)} for i in range(count)]
            slides.append({"layout": "staircase", "headline": f"Maturity ({count} levels, at {cur})",
                           "current_level": cur, "levels": levels})
    # without body text
    slides.append({"layout": "staircase", "headline": "Staircase (labels only)",
                   "current_level": 2, "levels": [{"label": medium(i)} for i in range(4)]})
    # long labels
    slides.append({"layout": "staircase", "headline": "Staircase (long labels)",
                   "current_level": 3, "levels": [{"label": long(i), "body": medium(i)} for i in range(4)]})

    # cycle_diagram: 8 variants (3/4/5/6 nodes × with/without center label)
    for count in [3, 4, 5, 6]:
        nodes = [{"label": short(i)} for i in range(count)]
        slides.append({"layout": "cycle_diagram", "headline": f"Cycle ({count} nodes)",
                       "center_label": "Core", "nodes": nodes})
    for count in [4, 6]:
        nodes = [{"label": medium(i)} for i in range(count)]
        slides.append({"layout": "cycle_diagram", "headline": f"Cycle ({count}, long labels)",
                       "center_label": medium(0), "nodes": nodes})
    slides.append({"layout": "cycle_diagram", "headline": "Cycle (no center)",
                   "nodes": [{"label": short(i)} for i in range(5)]})
    slides.append({"layout": "cycle_diagram", "headline": "Cycle (3, minimal)",
                   "center_label": "Loop", "nodes": [{"label": short(i)} for i in range(3)]})

    # hub_spoke: 8 variants (3/4/5/6/8 spokes × with/without spoke descriptions)
    for count in [3, 4, 5, 6, 8]:
        spokes = [{"label": short(i)} for i in range(count)]
        slides.append({"layout": "hub_spoke", "headline": f"Hub ({count} spokes)",
                       "hub": "Platform", "spokes": spokes})
    for count in [4, 6]:
        spokes = [{"label": medium(i)} for i in range(count)]
        slides.append({"layout": "hub_spoke", "headline": f"Hub ({count}, long labels)",
                       "hub": medium(0), "spokes": spokes})
    slides.append({"layout": "hub_spoke", "headline": "Hub (minimal)",
                   "hub": "Core", "spokes": [{"label": short(i)} for i in range(3)]})

    # funnel: 8 variants (3/4/5/6 stages × with/without values)
    for count in [3, 4, 5, 6]:
        stages = [{"label": medium(i), "value": f"{1000 - i * 200} items", "width": 100 - i * 15} for i in range(count)]
        slides.append({"layout": "funnel", "headline": f"Funnel ({count} stages)", "stages": stages})
    # without values
    slides.append({"layout": "funnel", "headline": "Funnel (no values)",
                   "stages": [{"label": medium(i), "width": 100 - i * 20} for i in range(4)]})
    # long labels
    slides.append({"layout": "funnel", "headline": "Funnel (long labels)",
                   "stages": [{"label": long(i), "value": f"{500 - i * 100}", "width": 100 - i * 20} for i in range(4)]})
    # minimal
    slides.append({"layout": "funnel", "headline": "Funnel (3 minimal)",
                   "stages": [{"label": short(i), "width": 100 - i * 25} for i in range(3)]})
    slides.append({"layout": "funnel", "headline": "Funnel (6 tight)",
                   "stages": [{"label": short(i), "value": str(100 - i * 15) + "%", "width": 100 - i * 12} for i in range(6)]})

    # roadmap: 8 variants (different swimlanes × milestones × durations)
    slides.append({"layout": "roadmap", "headline": "Roadmap (3 swimlanes)",
                   "start": "Q1 2026", "end": "Q4 2026",
                   "swimlanes": [
                       {"name": "Infrastructure", "items": [
                           {"label": "VM Migration", "start": 0, "end": 40, "status": "active"},
                           {"label": "Network Setup", "start": 30, "end": 60, "status": "planned"}]},
                       {"name": "Security", "items": [
                           {"label": "IAM Rollout", "start": 10, "end": 50, "status": "complete"},
                           {"label": "Pen Test", "start": 60, "end": 80, "status": "planned"}]},
                       {"name": "Platform", "items": [
                           {"label": "K8s Deploy", "start": 20, "end": 70, "status": "active"}]},
                   ],
                   "milestones": [{"label": "Go/No-Go", "position": 50}, {"label": "Launch", "position": 90}]})
    slides.append({"layout": "roadmap", "headline": "Roadmap (2 swimlanes, dense)",
                   "start": "Jan 2026", "end": "Dec 2026",
                   "swimlanes": [
                       {"name": "Workstream A", "items": [
                           {"label": medium(i), "start": i * 15, "end": i * 15 + 25,
                            "status": ["complete", "active", "planned"][min(i, 2)]} for i in range(4)]},
                       {"name": "Workstream B", "items": [
                           {"label": medium(i + 4), "start": i * 20 + 10, "end": i * 20 + 35,
                            "status": "planned"} for i in range(3)]},
                   ]})
    slides.append({"layout": "roadmap", "headline": "Roadmap (4 swimlanes)",
                   "start": "2026", "end": "2027",
                   "swimlanes": [
                       {"name": f"Track {t+1}", "items": [
                           {"label": short(t * 2 + i), "start": t * 10 + i * 20, "end": t * 10 + i * 20 + 30,
                            "status": ["complete", "active", "planned"][min(t, 2)]} for i in range(2)]}
                       for t in range(4)],
                   "milestones": [{"label": "M1", "position": 25}, {"label": "M2", "position": 50}, {"label": "M3", "position": 75}]})
    slides.append({"layout": "roadmap", "headline": "Roadmap (minimal)",
                   "start": "Now", "end": "EOY",
                   "swimlanes": [
                       {"name": "Project", "items": [
                           {"label": "Phase 1", "start": 0, "end": 40, "status": "complete"},
                           {"label": "Phase 2", "start": 40, "end": 70, "status": "active"},
                           {"label": "Phase 3", "start": 70, "end": 100, "status": "planned"}]}]})
    slides.append({"layout": "roadmap", "headline": "Roadmap (long labels)",
                   "start": "Q1", "end": "Q4",
                   "swimlanes": [
                       {"name": "Infrastructure Migration", "items": [
                           {"label": long(0), "start": 0, "end": 50, "status": "active"}]},
                       {"name": "Security and Compliance", "items": [
                           {"label": long(1), "start": 20, "end": 80, "status": "planned"}]},
                   ]})
    slides.append({"layout": "roadmap", "headline": "Roadmap (many milestones)",
                   "start": "Sprint 1", "end": "Sprint 12",
                   "swimlanes": [
                       {"name": "Dev", "items": [{"label": f"Feature {i+1}", "start": i*8, "end": i*8+15, "status": "planned"} for i in range(6)]}],
                   "milestones": [{"label": f"Release {i+1}", "position": i * 20 + 10} for i in range(5)]})
    slides.append({"layout": "roadmap", "headline": "Roadmap (5 swimlanes, crowded)",
                   "start": "H1 2026", "end": "H2 2026",
                   "swimlanes": [
                       {"name": short(t), "items": [
                           {"label": short(t * 3 + i), "start": i * 25, "end": i * 25 + 20, "status": "planned"}
                           for i in range(3)]}
                       for t in range(5)]})
    slides.append({"layout": "roadmap", "headline": "Roadmap (overlapping items)",
                   "start": "Q1", "end": "Q4",
                   "swimlanes": [
                       {"name": "Stream 1", "items": [
                           {"label": "Alpha", "start": 0, "end": 60, "status": "active"},
                           {"label": "Beta", "start": 30, "end": 90, "status": "planned"},
                           {"label": "GA", "start": 70, "end": 100, "status": "planned"}]}],
                   "milestones": [{"label": "Review", "position": 50}]})

    return slides

def gen_chart_layouts():
    """waterfall, donut_rings, gauge, tornado, radar, combo, bubble, risk_heat_map — ~56 slides"""
    slides = []

    # waterfall: 8 variants (3/5/7 items × with/without start/end labels)
    for count in [3, 5, 7]:
        items = [{"label": short(i), "value": (-1)**i * (100 + i * 50) * 1000,
                  "type": "negative" if i % 2 == 0 else "positive"} for i in range(count)]
        slides.append({"layout": "waterfall", "headline": f"Waterfall ({count} items)",
                       "start": {"label": "Baseline", "value": 2000000},
                       "items": items, "end": {"label": "Result", "value": 1500000}})
    # large values
    slides.append({"layout": "waterfall", "headline": "Waterfall (large values)",
                   "start": {"label": "Revenue", "value": 50000000},
                   "items": [{"label": "Growth", "value": 12000000, "type": "positive"},
                             {"label": "Churn", "value": -8000000, "type": "negative"},
                             {"label": "Expansion", "value": 5000000, "type": "positive"},
                             {"label": "Costs", "value": -15000000, "type": "negative"}],
                   "end": {"label": "Net", "value": 44000000}})
    # small values
    slides.append({"layout": "waterfall", "headline": "Waterfall (small values)",
                   "start": {"label": "Start", "value": 100},
                   "items": [{"label": short(i), "value": (-1)**i * (10 + i * 5), "type": "positive" if i % 2 else "negative"} for i in range(6)],
                   "end": {"label": "End", "value": 85}})
    # all positive
    slides.append({"layout": "waterfall", "headline": "Waterfall (all positive)",
                   "start": {"label": "Base", "value": 0},
                   "items": [{"label": medium(i), "value": 100000 + i * 50000, "type": "positive"} for i in range(5)],
                   "end": {"label": "Total", "value": 600000}})
    # long labels
    slides.append({"layout": "waterfall", "headline": "Waterfall (long labels)",
                   "start": {"label": "Beginning of fiscal year", "value": 1000000},
                   "items": [{"label": medium(i), "value": (-1)**i * 200000, "type": "positive" if i % 2 else "negative"} for i in range(4)],
                   "end": {"label": "End of fiscal year", "value": 1000000}})

    # donut_rings: 8 variants (2/3/4/5/6 rings × different colors)
    for count in [2, 3, 4, 5, 6]:
        colors = ["green", "amber", "red", "purple", "pink"]
        rings = [{"value": 20 + i * 15, "label": medium(i), "color": colors[i % len(colors)]} for i in range(count)]
        slides.append({"layout": "donut_rings", "headline": f"Donuts ({count})", "rings": rings})
    # high values
    slides.append({"layout": "donut_rings", "headline": "Donuts (high values)",
                   "rings": [{"value": 95, "label": "Uptime", "color": "green"},
                             {"value": 88, "label": "Coverage", "color": "green"},
                             {"value": 72, "label": "Adoption", "color": "amber"}]})
    # low values
    slides.append({"layout": "donut_rings", "headline": "Donuts (low values)",
                   "rings": [{"value": 12, "label": "Migration", "color": "red"},
                             {"value": 25, "label": "Testing", "color": "amber"},
                             {"value": 8, "label": "Docs", "color": "red"},
                             {"value": 40, "label": "Training", "color": "amber"}]})
    # long labels
    slides.append({"layout": "donut_rings", "headline": "Donuts (long labels)",
                   "rings": [{"value": 60 + i * 10, "label": long(i), "color": ["green", "amber", "purple"][i % 3]} for i in range(3)]})

    # gauge_dashboard: 8 variants (2/3/4 gauges × different value ranges)
    for count in [2, 3, 4]:
        gauges = [{"value": 30 + i * 25, "label": medium(i)} for i in range(count)]
        slides.append({"layout": "gauge_dashboard", "headline": f"Gauges ({count})", "gauges": gauges})
    # all high
    slides.append({"layout": "gauge_dashboard", "headline": "Gauges (all high)",
                   "gauges": [{"value": 92, "label": "Availability"}, {"value": 88, "label": "Performance"},
                              {"value": 95, "label": "Security"}]})
    # all low
    slides.append({"layout": "gauge_dashboard", "headline": "Gauges (all low)",
                   "gauges": [{"value": 15, "label": "Migration"}, {"value": 22, "label": "Testing"}]})
    # mixed with long labels
    slides.append({"layout": "gauge_dashboard", "headline": "Gauges (long labels)",
                   "gauges": [{"value": 45, "label": long(i)} for i in range(3)]})
    # single gauge
    slides.append({"layout": "gauge_dashboard", "headline": "Single Gauge",
                   "gauges": [{"value": 73, "label": "Overall Health Score"}]})
    slides.append({"layout": "gauge_dashboard", "headline": "Gauges (4, varied)",
                   "gauges": [{"value": v, "label": l} for v, l in
                              [(10, "Critical"), (45, "Warning"), (78, "Good"), (99, "Excellent")]]})

    # tornado_chart: 8 variants (3/5/7 items × different scales)
    for count in [3, 5, 7]:
        items = [{"label": medium(i), "low": -(100 + i * 50), "high": 150 + i * 40} for i in range(count)]
        slides.append({"layout": "tornado_chart", "headline": f"Tornado ({count})", "items": items})
    # symmetric
    slides.append({"layout": "tornado_chart", "headline": "Tornado (symmetric)",
                   "items": [{"label": medium(i), "low": -(200 + i * 30), "high": 200 + i * 30} for i in range(5)]})
    # asymmetric
    slides.append({"layout": "tornado_chart", "headline": "Tornado (asymmetric)",
                   "items": [{"label": medium(i), "low": -(50 + i * 10), "high": 300 + i * 100} for i in range(4)]})
    # long labels
    slides.append({"layout": "tornado_chart", "headline": "Tornado (long labels)",
                   "items": [{"label": long(i), "low": -(150 + i * 50), "high": 200 + i * 50} for i in range(4)]})
    # small values
    slides.append({"layout": "tornado_chart", "headline": "Tornado (small range)",
                   "items": [{"label": short(i), "low": -(5 + i), "high": 5 + i * 2} for i in range(6)]})
    slides.append({"layout": "tornado_chart", "headline": "Tornado (minimal)",
                   "items": [{"label": short(i), "low": -100, "high": 100} for i in range(3)]})

    # radar_chart: 8 variants (4/6/8 axes × 1/2/3 series)
    for axes_count in [4, 6, 8]:
        for series_count in [1, 2]:
            axes = [short(i) for i in range(axes_count)]
            series = [{"name": f"Series {s+1}", "values": [30 + (i * 15 + s * 20) % 70 for i in range(axes_count)]} for s in range(series_count)]
            slides.append({"layout": "radar_chart", "headline": f"Radar ({axes_count} axes, {series_count} series)",
                           "axes": axes, "series": series})
    # 3 series
    slides.append({"layout": "radar_chart", "headline": "Radar (3 series)",
                   "axes": [short(i) for i in range(6)],
                   "series": [{"name": f"Team {s+1}", "values": [20 + (i * 10 + s * 25) % 80 for i in range(6)]} for s in range(3)]})
    # long axis labels
    slides.append({"layout": "radar_chart", "headline": "Radar (long labels)",
                   "axes": [medium(i) for i in range(5)],
                   "series": [{"name": "Current", "values": [40, 60, 30, 80, 50]},
                              {"name": "Target", "values": [70, 80, 60, 90, 75]}]})

    # combo_chart: 8 variants (4/6/8/12 categories)
    for count in [4, 6, 8, 12]:
        cats = [f"M{i+1}" for i in range(count)]
        slides.append({"layout": "combo_chart", "headline": f"Combo ({count} categories)",
                       "categories": cats,
                       "bars": {"name": "Revenue", "values": [100 + i * 15 for i in range(count)]},
                       "line": {"name": "Growth %", "values": [40 + i * 8 for i in range(count)]}})
    # with long category labels
    slides.append({"layout": "combo_chart", "headline": "Combo (long categories)",
                   "categories": [medium(i) for i in range(5)],
                   "bars": {"name": "Spend", "values": [200, 180, 220, 195, 240]},
                   "line": {"name": "Savings %", "values": [10, 15, 12, 18, 22]}})
    # large values
    slides.append({"layout": "combo_chart", "headline": "Combo (large values)",
                   "categories": ["Q1", "Q2", "Q3", "Q4"],
                   "bars": {"name": "Revenue ($M)", "values": [12000000, 14500000, 13200000, 16800000]},
                   "line": {"name": "Margin %", "values": [22, 25, 23, 28]}})
    # minimal
    slides.append({"layout": "combo_chart", "headline": "Combo (3 points)",
                   "categories": ["Jan", "Feb", "Mar"],
                   "bars": {"name": "Count", "values": [50, 75, 60]},
                   "line": {"name": "Rate", "values": [80, 85, 82]}})
    slides.append({"layout": "combo_chart", "headline": "Combo (declining trend)",
                   "categories": [f"W{i+1}" for i in range(8)],
                   "bars": {"name": "Incidents", "values": [50 - i * 5 for i in range(8)]},
                   "line": {"name": "MTTR (hrs)", "values": [24 - i * 2 for i in range(8)]}})

    # bubble_chart: 8 variants (3/5/7 bubbles × different distributions)
    for count in [3, 5, 7]:
        bubbles = [{"label": medium(i), "x": 20 + i * 15, "y": 30 + (i * 20) % 70, "size": 30 + i * 15} for i in range(count)]
        slides.append({"layout": "bubble_chart", "headline": f"Bubbles ({count})",
                       "x_axis": "Strategic Value", "y_axis": "Effort", "bubbles": bubbles})
    # clustered
    slides.append({"layout": "bubble_chart", "headline": "Bubbles (clustered)",
                   "x_axis": "Risk", "y_axis": "Impact",
                   "bubbles": [{"label": short(i), "x": 20 + (i % 3) * 10, "y": 60 + (i % 2) * 15, "size": 40 + i * 5} for i in range(6)]})
    # corner cases
    slides.append({"layout": "bubble_chart", "headline": "Bubbles (extremes)",
                   "x_axis": "Cost", "y_axis": "Benefit",
                   "bubbles": [{"label": "Low/Low", "x": 5, "y": 5, "size": 20},
                               {"label": "High/High", "x": 95, "y": 95, "size": 80},
                               {"label": "Mid", "x": 50, "y": 50, "size": 50}]})
    # long labels
    slides.append({"layout": "bubble_chart", "headline": "Bubbles (long labels)",
                   "x_axis": "Implementation Complexity", "y_axis": "Business Value",
                   "bubbles": [{"label": long(i), "x": 15 + i * 20, "y": 20 + i * 15, "size": 25 + i * 10} for i in range(4)]})
    # many small
    slides.append({"layout": "bubble_chart", "headline": "Bubbles (9 items)",
                   "x_axis": "Priority", "y_axis": "Urgency",
                   "bubbles": [{"label": short(i), "x": 10 + (i % 3) * 30, "y": 10 + (i // 3) * 30, "size": 15 + i * 3} for i in range(9)]})
    slides.append({"layout": "bubble_chart", "headline": "Bubbles (minimal)",
                   "x_axis": "X", "y_axis": "Y",
                   "bubbles": [{"label": short(i), "x": 30 + i * 20, "y": 50, "size": 40} for i in range(3)]})

    # risk_heat_map: 8 variants (2/4/6/8 items × different distributions)
    for count in [2, 4, 6, 8]:
        items = [{"label": short(i), "x": 1 + i % 5, "y": 1 + (i * 2) % 5,
                  "description": medium(i)} for i in range(count)]
        slides.append({"layout": "risk_heat_map", "headline": f"Risk Map ({count})",
                       "x_axis": "Impact", "y_axis": "Likelihood", "items": items})
    # high risk cluster
    slides.append({"layout": "risk_heat_map", "headline": "Risk Map (high cluster)",
                   "x_axis": "Severity", "y_axis": "Probability",
                   "items": [{"label": short(i), "x": 4 + (i % 2), "y": 4 + (i % 2), "description": medium(i)} for i in range(5)]})
    # long descriptions
    slides.append({"layout": "risk_heat_map", "headline": "Risk Map (detailed)",
                   "x_axis": "Business Impact", "y_axis": "Likelihood of Occurrence",
                   "items": [{"label": medium(i), "x": 1 + i, "y": 5 - i, "description": long(i)} for i in range(4)]})
    # minimal
    slides.append({"layout": "risk_heat_map", "headline": "Risk Map (minimal)",
                   "x_axis": "Impact", "y_axis": "Likelihood",
                   "items": [{"label": "Risk A", "x": 2, "y": 4}, {"label": "Risk B", "x": 4, "y": 2}]})
    slides.append({"layout": "risk_heat_map", "headline": "Risk Map (10 items)",
                   "x_axis": "Impact", "y_axis": "Likelihood",
                   "items": [{"label": short(i), "x": 1 + i % 5, "y": 1 + (i * 3) % 5, "description": short(i + 5)} for i in range(10)]})

    return slides

def gen_comparison_layouts():
    """quadrant, pros_cons, pricing_table, bold_bullet, team_profiles — ~52 slides"""
    slides = []

    # quadrant: 8 variants (different item counts × short/long × color variations)
    for length, fn in [("short", short), ("medium", medium), ("long", long)]:
        items_per = 3 if length != "long" else 2
        slides.append({"layout": "quadrant", "headline": f"Quadrant ({length})",
                       "x_axis": "Implementation Effort", "y_axis": "Business Impact",
                       "quadrants": [
                           {"position": "top-left", "title": "Quick Wins", "color": "#4CAF50",
                            "items": [fn(i) for i in range(items_per)]},
                           {"position": "top-right", "title": "Major Projects", "color": "#2196F3",
                            "items": [fn(i+3) for i in range(items_per)]},
                           {"position": "bottom-left", "title": "Fill-Ins", "color": "#FFC107",
                            "items": [fn(i+6) for i in range(items_per)]},
                           {"position": "bottom-right", "title": "Avoid", "color": "#F44336",
                            "items": [fn(i+9) for i in range(items_per)]},
                       ]})
    # sparse
    slides.append({"layout": "quadrant", "headline": "Quadrant (sparse)",
                   "x_axis": "Risk", "y_axis": "Reward",
                   "quadrants": [
                       {"position": "top-left", "title": "Low Risk / High Reward", "color": "#4CAF50", "items": [medium(0)]},
                       {"position": "top-right", "title": "High Risk / High Reward", "color": "#2196F3", "items": [medium(1)]},
                       {"position": "bottom-left", "title": "Low Risk / Low Reward", "color": "#FFC107", "items": []},
                       {"position": "bottom-right", "title": "High Risk / Low Reward", "color": "#F44336", "items": [medium(2)]},
                   ]})
    # dense
    slides.append({"layout": "quadrant", "headline": "Quadrant (dense)",
                   "x_axis": "Cost", "y_axis": "Value",
                   "quadrants": [
                       {"position": "top-left", "title": "High Value / Low Cost", "color": "#4CAF50",
                        "items": [medium(i) for i in range(5)]},
                       {"position": "top-right", "title": "High Value / High Cost", "color": "#2196F3",
                        "items": [medium(i+5) for i in range(4)]},
                       {"position": "bottom-left", "title": "Low Value / Low Cost", "color": "#FFC107",
                        "items": [medium(i+9) for i in range(3)]},
                       {"position": "bottom-right", "title": "Low Value / High Cost", "color": "#F44336",
                        "items": [medium(i+12) for i in range(2)]},
                   ]})
    # long axis labels
    slides.append({"layout": "quadrant", "headline": "Quadrant (long labels)",
                   "x_axis": "Technical Implementation Complexity", "y_axis": "Strategic Business Value",
                   "quadrants": [
                       {"position": p, "title": t, "color": c, "items": [long(i)]}
                       for i, (p, t, c) in enumerate([
                           ("top-left", "Quick Wins", "#4CAF50"), ("top-right", "Strategic", "#2196F3"),
                           ("bottom-left", "Tactical", "#FFC107"), ("bottom-right", "Deprioritize", "#F44336")])
                   ]})
    # asymmetric quadrant items
    slides.append({"layout": "quadrant", "headline": "Quadrant (asymmetric)",
                   "x_axis": "Effort", "y_axis": "Impact",
                   "quadrants": [
                       {"position": "top-left", "title": "Do First", "color": "#4CAF50", "items": [medium(i) for i in range(6)]},
                       {"position": "top-right", "title": "Plan", "color": "#2196F3", "items": [medium(6)]},
                       {"position": "bottom-left", "title": "Delegate", "color": "#FFC107", "items": [medium(7), medium(8)]},
                       {"position": "bottom-right", "title": "Drop", "color": "#F44336", "items": []},
                   ]})
    slides.append({"layout": "quadrant", "headline": "Quadrant (minimal)",
                   "x_axis": "X", "y_axis": "Y",
                   "quadrants": [
                       {"position": p, "title": t, "color": c, "items": [short(i)]}
                       for i, (p, t, c) in enumerate([
                           ("top-left", "A", "#4CAF50"), ("top-right", "B", "#2196F3"),
                           ("bottom-left", "C", "#FFC107"), ("bottom-right", "D", "#F44336")])
                   ]})

    # pros_cons: 8 variants (2/4/6 items × with/without recommendation)
    for count in [2, 4, 6]:
        s = {"layout": "pros_cons", "headline": f"Pros/Cons ({count} each)",
             "pros": bullet_items(count, "medium"), "cons": bullet_items(count, "medium")}
        if count > 2:
            s["recommendation"] = "Proceed with Option A based on overall assessment."
        slides.append(s)
    # long items
    slides.append({"layout": "pros_cons", "headline": "Pros/Cons (long items)",
                   "pros": bullet_items(3, "long"), "cons": bullet_items(3, "long"),
                   "recommendation": long(7)})
    # short items
    slides.append({"layout": "pros_cons", "headline": "Pros/Cons (short items)",
                   "pros": bullet_items(5, "short"), "cons": bullet_items(5, "short")})
    # asymmetric
    slides.append({"layout": "pros_cons", "headline": "Pros/Cons (asymmetric)",
                   "pros": bullet_items(6, "medium"), "cons": bullet_items(2, "medium"),
                   "recommendation": "Strong recommendation to proceed."})
    # minimal
    slides.append({"layout": "pros_cons", "headline": "Pros/Cons (minimal)",
                   "pros": ["Fast"], "cons": ["Expensive"]})
    slides.append({"layout": "pros_cons", "headline": "Pros/Cons (8 each)",
                   "pros": bullet_items(8, "short"), "cons": bullet_items(8, "short"),
                   "recommendation": "Mixed results — requires further analysis."})

    # pricing_table: 8 variants (2/3/4 tiers × 3/6 features)
    for tiers in [2, 3, 4]:
        for feat_count in [3, 6]:
            tier_list = []
            for t in range(tiers):
                tier_list.append({"name": ["Basic", "Pro", "Enterprise", "Ultimate"][t],
                                  "price": ["Free", "$49/mo", "$199/mo", "Custom"][t],
                                  "highlight": t == 1,
                                  "features": [medium(t * feat_count + f) for f in range(feat_count)]})
            slides.append({"layout": "pricing_table", "headline": f"Pricing ({tiers} tiers, {feat_count} features)",
                           "tiers": tier_list})
    # long feature names
    slides.append({"layout": "pricing_table", "headline": "Pricing (long features)",
                   "tiers": [{"name": "Standard", "price": "$99/mo", "highlight": False,
                              "features": [long(i) for i in range(4)]},
                             {"name": "Premium", "price": "$299/mo", "highlight": True,
                              "features": [long(i+4) for i in range(4)]}]})
    # minimal
    slides.append({"layout": "pricing_table", "headline": "Pricing (minimal)",
                   "tiers": [{"name": "Free", "price": "$0", "highlight": False, "features": ["Basic access"]},
                             {"name": "Pro", "price": "$10/mo", "highlight": True, "features": ["Everything", "Priority support"]}]})

    # bold_bullet: 8 variants (2/3/4 points × 1/2/3 evidence)
    for points in [2, 3, 4]:
        for ev_count in [1, 2, 3]:
            pts = [{"assertion": medium(i), "evidence": bullet_items(ev_count, "medium")} for i in range(points)]
            slides.append({"layout": "bold_bullet", "headline": f"Summary ({points} points, {ev_count} evidence)",
                           "points": pts})
    # long assertions
    slides.append({"layout": "bold_bullet", "headline": "Bold Bullet (long assertions)",
                   "points": [{"assertion": long(i), "evidence": [medium(i*2), medium(i*2+1)]} for i in range(3)]})
    # minimal
    slides.append({"layout": "bold_bullet", "headline": "Bold Bullet (minimal)",
                   "points": [{"assertion": medium(0), "evidence": [short(0)]}]})

    # team_profiles: 8 variants (2/3/4/5/6/8 profiles × with/without context/icon)
    for count in [2, 3, 4, 5, 6, 8]:
        profiles = [{"name": f"Person {i+1}", "role": medium(i), "icon": icon(i),
                     "context": short(i + 10)} for i in range(count)]
        slides.append({"layout": "team_profiles", "headline": f"Team ({count} profiles)", "profiles": profiles})
    # without icons
    slides.append({"layout": "team_profiles", "headline": "Team (no icons)",
                   "profiles": [{"name": f"Person {i+1}", "role": medium(i)} for i in range(4)]})
    # long roles
    slides.append({"layout": "team_profiles", "headline": "Team (long roles)",
                   "profiles": [{"name": f"Person {i+1}", "role": long(i), "icon": icon(i)} for i in range(3)]})

    return slides

def gen_composite_layouts():
    """bento_grid, dashboard_panel, left_nav_sidebar, image_text_hero, venn, concentric_circles, pyramid — ~58 slides"""
    slides = []

    # bento_grid: 8 variants (2/3/4/5/6 tiles × large/small mix)
    for count in [2, 3, 4, 5, 6]:
        tiles = [{"title": short(0), "body": medium(0), "size": "large"}]
        for i in range(1, count):
            tiles.append({"title": short(i), "body": medium(i), "size": "small"})
        slides.append({"layout": "bento_grid", "headline": f"Bento ({count} tiles)", "tiles": tiles})
    # all small
    slides.append({"layout": "bento_grid", "headline": "Bento (all small)",
                   "tiles": [{"title": short(i), "body": short(i + 5), "size": "small"} for i in range(6)]})
    # with long text
    slides.append({"layout": "bento_grid", "headline": "Bento (long text)",
                   "tiles": [{"title": medium(0), "body": long(0), "size": "large"},
                             {"title": medium(1), "body": long(1), "size": "small"},
                             {"title": medium(2), "body": medium(2), "size": "small"}]})
    # mixed sizes
    mixed_tiles = [{"title": short(0), "body": medium(0), "size": "large"},
                   {"title": short(1), "body": medium(1), "size": "large"}]
    mixed_tiles += [{"title": short(i+2), "body": short(i+7), "size": "small"} for i in range(4)]
    slides.append({"layout": "bento_grid", "headline": "Bento (2 large + 4 small)", "tiles": mixed_tiles})

    # dashboard_panel: 8 variants (2/3/4 KPIs × 3/6 bars × with/without summary)
    for kpi_count in [2, 3, 4]:
        for bar_count in [3, 6]:
            kpis = [{"number": str(100 + i * 25), "label": short(i)} for i in range(kpi_count)]
            chart_data = [{"label": f"M{i+1}", "value": 50 + i * 20} for i in range(bar_count)]
            slides.append({"layout": "dashboard_panel",
                           "headline": f"Dashboard ({kpi_count} KPIs, {bar_count} bars)",
                           "kpis": kpis, "chart_title": "Trend", "chart_data": chart_data,
                           "summary": medium(0) + "\n" + medium(1)})
    # without summary
    slides.append({"layout": "dashboard_panel", "headline": "Dashboard (no summary)",
                   "kpis": [{"number": "42", "label": "Active"}, {"number": "7", "label": "Blocked"}],
                   "chart_title": "Monthly", "chart_data": [{"label": f"M{i+1}", "value": 30 + i * 10} for i in range(4)]})
    # long labels
    slides.append({"layout": "dashboard_panel", "headline": "Dashboard (long labels)",
                   "kpis": [{"number": "$1.2M", "label": medium(0)}, {"number": "99.9%", "label": medium(1)},
                            {"number": "47", "label": medium(2)}],
                   "chart_title": "Quarterly Trend", "chart_data": [{"label": medium(i+3), "value": 100 + i * 50} for i in range(4)],
                   "summary": long(0)})

    # left_nav_sidebar: 8 variants (3/5/7 items × different active items × short/long content)
    for count in [3, 5, 7]:
        nav = [{"label": short(i), "active": i == count // 2} for i in range(count)]
        slides.append({"layout": "left_nav_sidebar", "headline": f"Nav ({count} items)",
                       "nav_items": nav, "content_title": "Active Section",
                       "content_body": "- " + "\n- ".join(medium(i) for i in range(4))})
    # first item active
    slides.append({"layout": "left_nav_sidebar", "headline": "Nav (first active)",
                   "nav_items": [{"label": medium(i), "active": i == 0} for i in range(5)],
                   "content_title": medium(0), "content_body": "\n".join(long(i) for i in range(2))})
    # last item active
    slides.append({"layout": "left_nav_sidebar", "headline": "Nav (last active)",
                   "nav_items": [{"label": short(i), "active": i == 4} for i in range(5)],
                   "content_title": "Final Section", "content_body": "- " + "\n- ".join(medium(i) for i in range(6))})
    # long nav labels
    slides.append({"layout": "left_nav_sidebar", "headline": "Nav (long labels)",
                   "nav_items": [{"label": medium(i), "active": i == 2} for i in range(4)],
                   "content_title": "Details", "content_body": long(0)})
    # minimal content
    slides.append({"layout": "left_nav_sidebar", "headline": "Nav (minimal)",
                   "nav_items": [{"label": short(i), "active": i == 0} for i in range(3)],
                   "content_title": short(0), "content_body": medium(0)})
    # dense content
    slides.append({"layout": "left_nav_sidebar", "headline": "Nav (dense content)",
                   "nav_items": [{"label": short(i), "active": i == 1} for i in range(6)],
                   "content_title": "Comprehensive Overview",
                   "content_body": "\n".join(f"- {long(i)}" for i in range(4))})

    # venn: 8 variants (2/3 circles × different labels × with/without intersections)
    for count in [2, 3]:
        circles = [{"label": medium(i), "color": ["purple", "pink", "light_purple"][i]} for i in range(count)]
        intersections = [{"regions": list(range(count)), "label": "Overlap"}]
        slides.append({"layout": "venn", "headline": f"Venn ({count} circles)",
                       "circles": circles, "intersections": intersections})
    # short labels
    slides.append({"layout": "venn", "headline": "Venn (short labels)",
                   "circles": [{"label": short(i), "color": ["purple", "pink"][i]} for i in range(2)],
                   "intersections": [{"regions": [0, 1], "label": short(5)}]})
    # long labels
    slides.append({"layout": "venn", "headline": "Venn (long labels)",
                   "circles": [{"label": long(i), "color": ["purple", "pink", "light_purple"][i]} for i in range(3)],
                   "intersections": [{"regions": [0, 1, 2], "label": long(3)}]})
    # no intersection label
    slides.append({"layout": "venn", "headline": "Venn (no intersection label)",
                   "circles": [{"label": medium(i), "color": ["purple", "pink"][i]} for i in range(2)]})
    # multiple intersections
    slides.append({"layout": "venn", "headline": "Venn (multiple intersections)",
                   "circles": [{"label": medium(i), "color": ["purple", "pink", "light_purple"][i]} for i in range(3)],
                   "intersections": [{"regions": [0, 1], "label": "A∩B"}, {"regions": [1, 2], "label": "B∩C"},
                                     {"regions": [0, 1, 2], "label": "All"}]})

    # concentric_circles: 8 variants (2/3/4/5 rings × with/without values)
    for count in [2, 3, 4, 5]:
        rings = [{"label": short(i), "value": f"${(count - i) * 10}B"} for i in range(count)]
        slides.append({"layout": "concentric_circles", "headline": f"Concentric ({count} rings)", "rings": rings})
    # without values
    slides.append({"layout": "concentric_circles", "headline": "Concentric (no values)",
                   "rings": [{"label": medium(i)} for i in range(3)]})
    # long labels
    slides.append({"layout": "concentric_circles", "headline": "Concentric (long labels)",
                   "rings": [{"label": long(i)} for i in range(3)]})
    # with values only
    slides.append({"layout": "concentric_circles", "headline": "Concentric (values only)",
                   "rings": [{"label": short(i), "value": f"{(4-i)*25}%"} for i in range(4)]})
    # minimal
    slides.append({"layout": "concentric_circles", "headline": "Concentric (minimal)",
                   "rings": [{"label": "Core"}, {"label": "Extended"}]})

    # pyramid: 8 variants (3/4/5/6 tiers × with/without body)
    for count in [3, 4, 5, 6]:
        tiers = [{"label": medium(i), "body": short(i)} for i in range(count)]
        slides.append({"layout": "pyramid", "headline": f"Pyramid ({count} tiers)", "tiers": tiers})
    # without body
    slides.append({"layout": "pyramid", "headline": "Pyramid (labels only)",
                   "tiers": [{"label": medium(i)} for i in range(4)]})
    # long labels
    slides.append({"layout": "pyramid", "headline": "Pyramid (long labels)",
                   "tiers": [{"label": long(i), "body": medium(i)} for i in range(3)]})
    # with long body
    slides.append({"layout": "pyramid", "headline": "Pyramid (long body)",
                   "tiers": [{"label": short(i), "body": long(i)} for i in range(3)]})
    # minimal
    slides.append({"layout": "pyramid", "headline": "Pyramid (minimal)",
                   "tiers": [{"label": "Top"}, {"label": "Middle"}, {"label": "Base"}]})

    # image_text_hero: 8 variants (left/right/bottom × short/long text)
    for pos in ["left", "right", "bottom"]:
        slides.append({"layout": "image_text_hero", "headline": f"Hero ({pos})",
                       "body": medium(0) + "\n\n" + medium(1), "text_position": pos})
    for pos in ["left", "right"]:
        slides.append({"layout": "image_text_hero", "headline": f"Hero ({pos}, long text)",
                       "body": "\n\n".join(long(i) for i in range(3)), "text_position": pos})
    slides.append({"layout": "image_text_hero", "headline": "Hero (minimal)",
                   "body": short(0), "text_position": "left"})
    slides.append({"layout": "image_text_hero", "headline": "Hero (bullet list)",
                   "body": "- " + "\n- ".join(medium(i) for i in range(5)), "text_position": "right"})
    slides.append({"layout": "image_text_hero", "headline": "Hero (bottom, dense)",
                   "body": "\n".join(medium(i) for i in range(6)), "text_position": "bottom"})

    return slides

# ---------------------------------------------------------------------------
# Main — generate all stress test YAMLs
# ---------------------------------------------------------------------------

def main():
    batches = [
        ("01-structural", gen_structural()),
        ("02-single-message", gen_single_message()),
        ("03-content", gen_content_layouts()),
        ("04-data", gen_data_layouts()),
        ("05-process-flow", gen_process_flow()),
        ("06-charts", gen_chart_layouts()),
        ("07-comparison", gen_comparison_layouts()),
        ("08-composite", gen_composite_layouts()),
    ]

    total_slides = 0
    for batch_name, slides in batches:
        deck = {
            "title": f"Stress Test — {batch_name}",
            "date": "2026-04-10",
            "slides": slides,
        }
        path = os.path.join(OUT_DIR, f"{batch_name}.yaml")
        with open(path, "w") as f:
            yaml.dump(deck, f, default_flow_style=False, allow_unicode=True, width=120)
        print(f"  {batch_name}: {len(slides)} slides -> {path}")
        total_slides += len(slides)

    print(f"\nTotal: {total_slides} stress test slides across {len(batches)} batches")

if __name__ == "__main__":
    main()
