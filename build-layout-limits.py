#!/usr/bin/env python3
"""
Compute content limits for every layout field.

Uses the same estimate_text_height() math as build_deck.py to calculate
maximum lines and characters that fit in each text field at each font size.

Outputs layout-limits.json — the machine-readable content limits reference.
"""

import json
import math


def estimate_lines(avail_height_in, font_size_pt):
    """How many lines of text fit in avail_height_in at font_size_pt."""
    line_height = font_size_pt * 1.4 / 72
    return max(1, int(avail_height_in / line_height))


def chars_per_line(width_in, font_size_pt):
    """How many characters fit on one line at font_size_pt in width_in."""
    chars_per_inch = 13 * (10 / font_size_pt)
    return max(1, int(width_in * chars_per_inch))


def max_chars(width_in, avail_height_in, font_size_pt):
    """Total characters that fit in a text area."""
    lines = estimate_lines(avail_height_in, font_size_pt)
    cpl = chars_per_line(width_in, font_size_pt)
    return lines * cpl


def field_limits(width_in, avail_height_in, font_size_pt, field_name="body"):
    """Build a limits dict for a single text field."""
    lines = estimate_lines(avail_height_in, font_size_pt)
    cpl = chars_per_line(width_in, font_size_pt)
    return {
        "field": field_name,
        "width_in": round(width_in, 2),
        "avail_height_in": round(avail_height_in, 2),
        "font_size_pt": font_size_pt,
        "max_lines": lines,
        "chars_per_line": cpl,
        "max_chars": lines * cpl,
        "max_words": max(1, (lines * cpl) // 6),  # ~6 chars per word average
    }


# ---------------------------------------------------------------------------
# Content area constants (from build_deck.py)
# ---------------------------------------------------------------------------

AVAIL_TOP = 0.85
AVAIL_BOTTOM = 5.0
AVAIL_H = AVAIL_BOTTOM - AVAIL_TOP  # 4.15"

ICON_SIZE = 0.4
TITLE_H = 0.30
PAD = 0.12

# Body available height (after icon row + padding)
BODY_AVAIL = AVAIL_H - ICON_SIZE - PAD  # 3.63" in the common pattern


def build_limits():
    limits = {}

    # -----------------------------------------------------------------------
    # title_cover
    # -----------------------------------------------------------------------
    limits["title_cover"] = {
        "description": "Background image with text overlay",
        "max_items": 1,
        "fields": [
            field_limits(8.0, 1.0, 40, "headline"),
            field_limits(8.0, 0.5, 14, "subheader"),
        ],
        "split_guidance": "Title slides should not be split. Shorten the title or move detail to the subheader.",
    }

    # -----------------------------------------------------------------------
    # agenda
    # -----------------------------------------------------------------------
    limits["agenda"] = {
        "description": "Numbered agenda items with left image",
        "max_items": 7,
        "fields": [
            field_limits(3.87, 0.57, 14, "item (<=5 items)"),
            field_limits(3.87, 0.47, 12, "item (6-7 items)"),
        ],
        "split_guidance": "If more than 7 agenda items, split into two agenda slides or group items into fewer high-level topics.",
    }

    # -----------------------------------------------------------------------
    # section_divider
    # -----------------------------------------------------------------------
    limits["section_divider"] = {
        "description": "Visual break between sections",
        "max_items": 1,
        "fields": [
            field_limits(8.0, 1.0, 36, "headline"),
            field_limits(7.0, 0.5, 16, "subheader"),
        ],
        "split_guidance": "Section dividers should not be split. Keep headline to 1-2 lines.",
    }

    # -----------------------------------------------------------------------
    # side_by_side
    # -----------------------------------------------------------------------
    col_w_sbs = 3.45  # 4.0 - 0.55 text_indent
    limits["side_by_side"] = {
        "description": "Two columns with icons",
        "max_items": 2,
        "fields": [
            field_limits(col_w_sbs, TITLE_H, 14, "left_title / right_title"),
            field_limits(col_w_sbs, BODY_AVAIL, 10, "left_body / right_body"),
        ],
        "split_guidance": "If either body exceeds {max_lines} lines, split into two side_by_side slides (Part 1 / Part 2) or move dense content to a content_table.",
    }

    # -----------------------------------------------------------------------
    # three_column
    # -----------------------------------------------------------------------
    col_w_3c = 2.35  # 2.9 - 0.55
    limits["three_column"] = {
        "description": "Three titled columns with icons",
        "max_items": 3,
        "fields": [
            field_limits(col_w_3c, TITLE_H, 12, "col_title"),
            field_limits(col_w_3c, BODY_AVAIL, 9, "col_body"),
        ],
        "split_guidance": "If any column body exceeds {max_lines} lines, consider side_by_side (for 2 dense topics) or numbered_list (for sequential items).",
    }

    # -----------------------------------------------------------------------
    # four_card
    # -----------------------------------------------------------------------
    for n_cards in [2, 3, 4, 5, 6, 7, 8]:
        gap = 0.1
        card_w = min(3.0, (9.3 - (n_cards - 1) * gap) / n_cards)
        text_w = card_w - 0.24
        if n_cards <= 4:
            title_pt, body_pt = 11, 9
        elif n_cards <= 6:
            title_pt, body_pt = 10, 8
        else:
            title_pt, body_pt = 9, 7

        card_key = f"four_card ({n_cards} cards)"
        # Body height: total_avail - card_pad_top - title_h - gap - card_pad_bottom
        # Approximate: card_h ~ AVAIL_H, body gets about 60% of that
        body_avail = min(AVAIL_H * 0.6, 2.0)

        limits[card_key] = {
            "description": f"Card layout with {n_cards} cards",
            "max_items": n_cards,
            "fields": [
                field_limits(text_w, 0.28, title_pt, "card_title"),
                field_limits(text_w, body_avail, body_pt, "card_body"),
            ],
            "split_guidance": f"With {n_cards} cards, each body is limited to {{max_lines}} lines. If cards need more text, reduce card count or split across slides.",
        }

    # -----------------------------------------------------------------------
    # big_stat_manual
    # -----------------------------------------------------------------------
    limits["big_stat_manual"] = {
        "description": "Large centered number with label",
        "max_items": 1,
        "fields": [
            field_limits(9.0, 1.5, 72, "number"),
            field_limits(6.0, 1.0, 16, "label"),
        ],
        "split_guidance": "Big stat should be a single number + short label. If you need multiple stats, use kpi_dashboard.",
    }

    # -----------------------------------------------------------------------
    # kpi_dashboard
    # -----------------------------------------------------------------------
    for n_metrics in [2, 3, 4, 5, 6, 7, 8]:
        cols = min(n_metrics, 4) if n_metrics > 4 else n_metrics
        rows = math.ceil(n_metrics / cols)
        gap = 0.12
        card_w = (9.3 - (cols - 1) * gap) / cols
        card_h = min(1.8, (3.8 - (rows - 1) * gap) / rows)
        inner_w = card_w - 0.24
        if n_metrics <= 4:
            num_pt, label_pt = 32, 10
        elif n_metrics <= 6:
            num_pt, label_pt = 28, 9
        else:
            num_pt, label_pt = 24, 8

        label_avail = card_h * 0.3  # roughly bottom third of card

        limits[f"kpi_dashboard ({n_metrics} metrics)"] = {
            "description": f"KPI grid with {n_metrics} metrics ({cols}x{rows})",
            "max_items": n_metrics,
            "fields": [
                field_limits(inner_w, card_h * 0.4, num_pt, "number"),
                field_limits(inner_w, label_avail, label_pt, "label"),
            ],
            "split_guidance": f"Labels limited to {{max_lines}} lines. Keep labels to 3-5 words. For detailed metrics, use content_table.",
        }

    # -----------------------------------------------------------------------
    # content_table
    # -----------------------------------------------------------------------
    for n_cols in [2, 3, 4, 5, 6, 7]:
        col_w = 9.3 / n_cols
        if n_cols <= 4:
            hdr_pt, body_pt = 10, 9
        elif n_cols <= 6:
            hdr_pt, body_pt = 9, 8
        else:
            hdr_pt, body_pt = 8, 7
        # Max rows: (5.05 - 0.85 - 0.35 header) / 0.45 max row height
        max_rows = int((5.05 - 0.85 - 0.35) / 0.28)

        limits[f"content_table ({n_cols} cols)"] = {
            "description": f"Table with {n_cols} columns",
            "max_items": max_rows,
            "fields": [
                field_limits(col_w, 0.35, hdr_pt, "header_cell"),
                field_limits(col_w, 0.45, body_pt, "data_cell"),
            ],
            "split_guidance": f"Max ~{max_rows} rows. For tables with more rows, split across two slides — repeat the header row on the second slide. Use notes to indicate 'continued'.",
            "split_at_rows": max_rows,
        }

    # -----------------------------------------------------------------------
    # matrix
    # -----------------------------------------------------------------------
    for n_cols in [2, 3, 4, 5, 6]:
        data_col_w = (9.3 - 2.0) / n_cols
        max_rows = int((4.0 - 0.35) / 0.4)
        limits[f"matrix ({n_cols} cols)"] = {
            "description": f"RACI/color-coded matrix with {n_cols} columns",
            "max_items": max_rows,
            "fields": [
                field_limits(2.0, 0.4, 9, "row_label"),
                field_limits(data_col_w, 0.4, 11, "data_cell"),
            ],
            "split_guidance": f"Max ~{max_rows} rows. For larger matrices, split rows across two slides with header repeated.",
            "split_at_rows": max_rows,
        }

    # -----------------------------------------------------------------------
    # numbered_list
    # -----------------------------------------------------------------------
    text_w_nl = 8.55  # 9.3 - 0.6 num_w - 0.15 gap
    # Each item: title_h + body_h + divider_gap (~0.15)
    # At 12pt title + 10pt body with 2 body lines: ~0.23 + 0.39 + 0.15 = 0.77" per item
    item_h_est = 0.77
    max_items_nl = int(AVAIL_H / item_h_est)

    limits["numbered_list"] = {
        "description": "Large numbers with title and body per item",
        "max_items": max_items_nl,
        "fields": [
            field_limits(text_w_nl, 0.25, 12, "title"),
            field_limits(text_w_nl, 1.5, 10, "body"),
        ],
        "split_guidance": f"Max ~{max_items_nl} items with 2-line bodies. For more items, split across slides: 'Steps 1-3' and 'Steps 4-6'. Or use shorter body text.",
    }

    # -----------------------------------------------------------------------
    # status_board
    # -----------------------------------------------------------------------
    # Each item: circle + name + summary, ~0.5" per row
    max_items_sb = int(AVAIL_H / 0.55)
    limits["status_board"] = {
        "description": "RAG status tracking with circles",
        "max_items": max_items_sb,
        "fields": [
            field_limits(2.5, 0.35, 12, "name"),
            field_limits(5.8, 0.5, 10, "summary"),
        ],
        "split_guidance": f"Max ~{max_items_sb} items. For more workstreams, split across slides or group into categories.",
    }

    # -----------------------------------------------------------------------
    # roadmap
    # -----------------------------------------------------------------------
    limits["roadmap"] = {
        "description": "Gantt-style timeline with swimlanes",
        "max_items": 4,  # practical max swimlanes
        "max_time_periods": 8,
        "fields": [
            field_limits(1.2, 0.3, 10, "lane_name"),
            {"field": "bar_label", "max_chars": 25, "max_words": 4, "note": "Bars are 0.28\" tall, 8pt font — keep labels very short"},
        ],
        "split_guidance": "Max 4 swimlanes with 3-4 bars each. For longer timelines, split into 'Phase 1 Roadmap' and 'Phase 2 Roadmap' slides.",
        "max_bars_per_lane": 4,
    }

    # -----------------------------------------------------------------------
    # before_after
    # -----------------------------------------------------------------------
    col_w_ba = 3.4  # 3.8 - 0.4 padding
    # Icon (0.5) + label (0.35) + gap (0.1) = 0.95" overhead per column
    items_avail_h = AVAIL_H - 0.95 - 0.4  # padding
    max_items_ba = int(items_avail_h / (10 * 1.4 / 72))  # lines at 10pt

    limits["before_after"] = {
        "description": "Current vs target state transformation",
        "max_items": max_items_ba,
        "fields": [
            field_limits(col_w_ba, 0.35, 14, "label"),
            field_limits(col_w_ba, items_avail_h, 10, "items (per side)"),
        ],
        "split_guidance": f"Max ~{max_items_ba} bullet items per side. If both sides are dense, consider two side_by_side slides instead.",
    }

    # -----------------------------------------------------------------------
    # quote
    # -----------------------------------------------------------------------
    limits["quote"] = {
        "description": "Decorative quotation with attribution",
        "max_items": 1,
        "fields": [
            field_limits(7.0, 2.0, 18, "quote_text"),
            field_limits(7.0, 0.3, 12, "attribution"),
        ],
        "split_guidance": "Quotes should be 1-3 sentences max. If the quote is longer, edit it down or use callout instead.",
    }

    # -----------------------------------------------------------------------
    # callout
    # -----------------------------------------------------------------------
    limits["callout"] = {
        "description": "Key takeaway in boxed or open style",
        "max_items": 1,
        "fields": [
            field_limits(6.4, 1.8, 20, "callout_text"),
            field_limits(6.4, 1.2, 12, "supporting_text"),
        ],
        "split_guidance": "Callout text should be 1-2 sentences. Supporting text 2-3 sentences. If more detail needed, follow with a numbered_list slide.",
    }

    # -----------------------------------------------------------------------
    # funnel
    # -----------------------------------------------------------------------
    max_stages = int(AVAIL_H / (0.55 + 0.08))
    limits["funnel"] = {
        "description": "Pipeline stages with narrowing bars",
        "max_items": max_stages,
        "fields": [
            {"field": "label", "max_chars": 30, "max_words": 5, "note": "Inside 0.55\" bar at 12pt"},
            {"field": "value", "max_chars": 25, "max_words": 4, "note": "Right side of bar at 11pt"},
        ],
        "split_guidance": f"Max ~{max_stages} stages. Funnel labels must be very concise — use short phrases.",
    }

    # -----------------------------------------------------------------------
    # closing
    # -----------------------------------------------------------------------
    limits["closing"] = {
        "description": "Closing/CTA slide",
        "max_items": 1,
        "fields": [
            field_limits(8.0, 1.5, 48, "headline"),
            field_limits(7.0, 1.0, 16, "subheader"),
            field_limits(6.0, 1.0, 12, "contact_info"),
        ],
        "split_guidance": "Closing slides should not be split. Keep to headline + optional subheader.",
    }

    # -----------------------------------------------------------------------
    # image_showcase
    # -----------------------------------------------------------------------
    limits["image_showcase"] = {
        "description": "Full-slide image with optional caption",
        "max_items": 1,
        "fields": [
            field_limits(9.3, 0.25, 8, "caption"),
        ],
        "split_guidance": "One image per slide. Caption should be a single line.",
    }

    # -----------------------------------------------------------------------
    # content_two_col (stacked)
    # -----------------------------------------------------------------------
    text_w_stacked = 4.55  # 5.1 - 0.55
    limits["content_two_col"] = {
        "description": "Stats graphic + two stacked sections",
        "max_items": 5,  # max stats
        "fields": [
            field_limits(text_w_stacked, TITLE_H, 14, "left_title / right_title"),
            field_limits(text_w_stacked, BODY_AVAIL * 0.45, 10, "left_body / right_body"),
            {"field": "left_stats", "max_items": 4, "note": "More than 4 stats crowds the graphic area"},
        ],
        "split_guidance": "If body text exceeds {max_lines} lines per section, move detail to a follow-up slide. Max 4 stats.",
    }

    # -----------------------------------------------------------------------
    # content_diagram_text
    # -----------------------------------------------------------------------
    limits["content_diagram_text"] = {
        "description": "Diagram + two text sections with split ratios",
        "max_items": 1,
        "fields": [
            field_limits(4.0, TITLE_H, 14, "left_title / right_title (vertical split)"),
            field_limits(4.0, 1.5, 10, "left_body / right_body (v-50/50)"),
            field_limits(3.5, 1.5, 10, "left_body / right_body (h-50/50)"),
        ],
        "split_guidance": "For dense text, use h-40/60 (more text space). If text still overflows, move one section to a follow-up slide.",
    }

    # -----------------------------------------------------------------------
    # General multi-slide split rules
    # -----------------------------------------------------------------------
    split_rules = {
        "table_continuation": {
            "description": "When a table has too many rows, split across slides",
            "rule": "Repeat the header row and column headers on the continuation slide. Add '(continued)' to the headline. Use the same col_widths.",
            "layouts": ["content_table", "content_table_bullets", "matrix"],
            "example": {
                "slide_1": {"headline": "Cloud Provider Comparison", "rows": "rows 1-8"},
                "slide_2": {"headline": "Cloud Provider Comparison (continued)", "rows": "rows 9-16"},
            },
        },
        "list_continuation": {
            "description": "When a numbered list or status board has too many items",
            "rule": "Split items across slides. Continue numbering (e.g., slide 1 has items 1-5, slide 2 has items 6-10). Add 'Part 1/2' or number range to headline.",
            "layouts": ["numbered_list", "status_board", "agenda"],
            "example": {
                "slide_1": {"headline": "Migration Steps (1-5)", "items": "items 1-5"},
                "slide_2": {"headline": "Migration Steps (6-10)", "items": "items 6-10"},
            },
        },
        "card_overflow": {
            "description": "When cards need more text than the layout allows",
            "rule": "Reduce card count per slide and split across multiple slides. 4 cards per slide is the sweet spot for readability. Use same headline with '(1/2)'.",
            "layouts": ["four_card"],
            "example": {
                "slide_1": {"headline": "Partner Shortlist (1/2)", "cards": "cards 1-4"},
                "slide_2": {"headline": "Partner Shortlist (2/2)", "cards": "cards 5-8"},
            },
        },
        "body_overflow": {
            "description": "When body text in any layout exceeds the available space",
            "rule": "Either: (1) trim text to key points only, (2) split topic across two slides of same layout, or (3) switch to a layout with more text space (e.g., three_column → side_by_side → numbered_list).",
            "layouts": ["side_by_side", "three_column", "before_after", "callout", "quote"],
            "layout_upgrade_path": {
                "three_column": "side_by_side (2 topics with more space) or numbered_list (sequential)",
                "side_by_side": "numbered_list (more vertical space) or two content_table slides",
                "four_card": "numbered_list or two four_card slides with fewer cards each",
                "before_after": "two side_by_side slides (current state, target state)",
                "callout": "numbered_list for detailed recommendations",
                "quote": "callout for longer text with supporting detail",
            },
        },
        "kpi_overflow": {
            "description": "When too many metrics for one dashboard",
            "rule": "Max 8 metrics per slide. For more, split into themed dashboards: 'Infrastructure Metrics' and 'Cost Metrics'.",
            "layouts": ["kpi_dashboard"],
        },
    }

    return {"layouts": limits, "split_rules": split_rules}


def main():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "layout-limits.json")

    data = build_limits()

    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Generated: {output_path}")
    print(f"  Layouts: {len(data['layouts'])}")
    print(f"  Split rules: {len(data['split_rules'])}")

    # Print summary
    for name, layout in sorted(data["layouts"].items()):
        fields_summary = []
        for field in layout.get("fields", []):
            if isinstance(field, dict) and "max_lines" in field:
                fields_summary.append(f"{field['field']}: {field['max_lines']} lines / {field['max_words']} words")
            elif isinstance(field, dict) and "max_chars" in field:
                fields_summary.append(f"{field['field']}: {field['max_chars']} chars")
        max_items = layout.get("max_items", "unlimited")
        print(f"  {name}: max_items={max_items}, {', '.join(fields_summary[:2])}")


if __name__ == "__main__":
    main()
