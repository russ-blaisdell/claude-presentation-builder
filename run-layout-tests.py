#!/usr/bin/env python3
"""
Layout Test Runner — End-to-end test suite for the deck builder.

Generates test variations, builds the deck, runs QA, checks proof images,
and produces a per-layout pass/fail report.

Usage:
    python3 run-layout-tests.py [--ai-review] [--keep-artifacts]

Outputs:
    test-layouts.yaml           — generated test YAML
    test-layouts.pptx           — built deck
    test-layouts-proof/         — proof PNGs
    test-layouts-qa-report.json — QA report
    test-results.md             — per-layout summary
"""

import json
import os
import sys
import subprocess
from pathlib import Path
from collections import defaultdict


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON = sys.executable
BLANK_THRESHOLD_KB = 5  # PNGs smaller than this are truly blank (renderer gap)


def run_step(description, cmd, timeout=300):
    """Run a command, print status, return success."""
    print(f"\n{'='*60}")
    print(f"  {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if result.returncode != 0:
            print(f"  FAILED (exit code {result.returncode})")
            if result.stderr:
                print(result.stderr[-500:])
            return False
        return True
    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT after {timeout}s")
        return False


def check_blank_slides(proof_dir):
    """Check proof PNGs for blank slides (file size < threshold)."""
    blank_slides = []
    proof_path = Path(proof_dir)
    for png in sorted(proof_path.glob("slide-*.png")):
        size_kb = png.stat().st_size / 1024
        if size_kb < BLANK_THRESHOLD_KB:
            slide_num = int(png.stem.split("-")[1])
            blank_slides.append({"slide": slide_num, "file": png.name, "size_kb": round(size_kb, 1)})
    return blank_slides


def parse_qa_report(qa_json_path):
    """Parse the QA report JSON and return per-slide issues."""
    if not os.path.exists(qa_json_path):
        return {}
    with open(qa_json_path) as f:
        report = json.load(f)
    return report


def parse_test_yaml(yaml_path):
    """Parse the test YAML to map slide numbers to layout names."""
    import yaml
    with open(yaml_path) as f:
        deck = yaml.safe_load(f)
    slide_map = {}
    for i, slide_def in enumerate(deck.get("slides", [])):
        slide_map[i + 1] = {
            "layout": slide_def.get("layout", "unknown"),
            "notes": slide_def.get("notes", ""),
        }
    return slide_map


def generate_results(slide_map, qa_report, blank_slides, output_path):
    """Generate the per-layout test results markdown."""
    # Organize issues by layout
    layout_issues = defaultdict(lambda: {"total": 0, "critical": 0, "warnings": 0, "info": 0, "blank": 0, "slides": 0, "issues": []})

    # Count slides per layout
    for num, info in slide_map.items():
        layout_issues[info["layout"]]["slides"] += 1

    # Blank slides
    blank_nums = {b["slide"] for b in blank_slides}
    for b in blank_slides:
        layout = slide_map.get(b["slide"], {}).get("layout", "unknown")
        layout_issues[layout]["blank"] += 1
        layout_issues[layout]["issues"].append(f"Slide {b['slide']}: BLANK ({b['size_kb']}KB) — {slide_map.get(b['slide'], {}).get('notes', '')}")

    # QA issues
    qa_slides = qa_report.get("slides", {})
    for num_str, slide_data in qa_slides.items():
        num = int(num_str)
        layout = slide_map.get(num, {}).get("layout", "unknown")
        for issue in slide_data.get("issues", []):
            sev = issue.get("severity", "info")
            layout_issues[layout]["total"] += 1
            if sev == "critical":
                layout_issues[layout]["critical"] += 1
            elif sev == "warning":
                layout_issues[layout]["warnings"] += 1
            else:
                layout_issues[layout]["info"] += 1
            # Only record non-margin issues (margin warnings are expected for edge-positioned elements)
            if "margin" not in issue.get("category", ""):
                layout_issues[layout]["issues"].append(
                    f"Slide {num} [{sev.upper()}] {issue.get('category', '')}: {issue.get('description', '')[:100]}")

    # Generate report
    lines = []
    lines.append("# Layout Test Results")
    lines.append("")
    lines.append(f"**Total slides:** {len(slide_map)}")
    lines.append(f"**Blank slides:** {len(blank_slides)}")
    lines.append(f"**Layouts tested:** {len(layout_issues)}")
    lines.append("")

    # Summary table
    lines.append("## Summary")
    lines.append("")
    lines.append("| Layout | Slides | Blank | Critical | Warnings | Status |")
    lines.append("|--------|--------|-------|----------|----------|--------|")

    total_pass = 0
    total_fail = 0
    for layout in sorted(layout_issues.keys()):
        data = layout_issues[layout]
        has_blank = data["blank"] > 0
        has_critical = data["critical"] > 0
        # Filter warnings — only count non-margin warnings
        non_margin_warnings = len([i for i in data["issues"] if "[WARNING]" in i and "margin" not in i.lower()])

        if has_blank or has_critical:
            status = "FAIL"
            total_fail += 1
        elif non_margin_warnings > 0:
            status = "WARN"
            total_pass += 1  # warnings don't fail
        else:
            status = "PASS"
            total_pass += 1

        lines.append(f"| `{layout}` | {data['slides']} | {data['blank']} | {data['critical']} | {data['warnings']} | **{status}** |")

    lines.append("")
    lines.append(f"**Result: {total_pass} passed, {total_fail} failed**")
    lines.append("")

    # Detailed issues per layout
    lines.append("## Details")
    lines.append("")
    for layout in sorted(layout_issues.keys()):
        data = layout_issues[layout]
        non_margin = [i for i in data["issues"] if "margin" not in i.lower()]
        if non_margin:
            lines.append(f"### `{layout}`")
            lines.append("")
            for issue in non_margin[:20]:  # cap at 20 per layout
                lines.append(f"- {issue}")
            if len(non_margin) > 20:
                lines.append(f"- ... and {len(non_margin) - 20} more")
            lines.append("")

    # Blank slide details
    if blank_slides:
        lines.append("## Blank Slides")
        lines.append("")
        lines.append("These slides rendered as blank in the proof images (likely a proof_renderer.py gap):")
        lines.append("")
        for b in blank_slides:
            info = slide_map.get(b["slide"], {})
            lines.append(f"- **Slide {b['slide']}** (`{info.get('layout', '?')}`) — {b['size_kb']}KB — {info.get('notes', '')}")
        lines.append("")

    with open(output_path, "w") as f:
        f.write("\n".join(lines))

    return total_fail


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Run layout test suite")
    parser.add_argument("--ai-review", action="store_true", help="Enable Claude vision review on sample")
    parser.add_argument("--keep-artifacts", action="store_true", help="Keep test PPTX and proof images")
    args = parser.parse_args()

    os.chdir(SCRIPT_DIR)

    # Step 1: Generate test YAML
    print("\n" + "=" * 60)
    print("  Step 1: Generating test YAML")
    print("=" * 60)
    from importlib import import_module
    # Import and run directly to avoid subprocess overhead
    sys.path.insert(0, SCRIPT_DIR)
    test_gen = __import__("test-layouts")
    yaml_path = test_gen.generate_test_yaml("test-layouts.yaml")

    # Step 2: Build the deck
    ok = run_step("Step 2: Building deck",
                  [PYTHON, os.path.join(SCRIPT_DIR, "build_deck.py"),
                   "test-layouts.yaml", "--output", "test-layouts.pptx"],
                  timeout=120)
    if not ok:
        print("\nBUILD FAILED — cannot continue")
        sys.exit(1)

    # Step 3: Generate proof images
    ok = run_step("Step 3: Generating proof images",
                  [PYTHON, os.path.join(SCRIPT_DIR, "proof_renderer.py"),
                   "test-layouts.pptx", "--output-dir", "test-layouts-proof"],
                  timeout=300)
    if not ok:
        print("\nPROOF RENDERING FAILED — continuing with partial results")

    # Step 4: Run QA pipeline
    ok = run_step("Step 4: Running QA pipeline",
                  [PYTHON, os.path.join(SCRIPT_DIR, "qa_pipeline.py"),
                   "test-layouts.pptx", "--output-dir", "."],
                  timeout=120)

    # Step 5: Check for blank slides
    print("\n" + "=" * 60)
    print("  Step 5: Checking for blank slides")
    print("=" * 60)
    blank_slides = check_blank_slides("test-layouts-proof")
    if blank_slides:
        print(f"  Found {len(blank_slides)} blank slide(s):")
        for b in blank_slides:
            print(f"    Slide {b['slide']}: {b['size_kb']}KB")
    else:
        print("  No blank slides detected")

    # Step 6: Parse results and generate report
    print("\n" + "=" * 60)
    print("  Step 6: Generating test report")
    print("=" * 60)
    slide_map = parse_test_yaml("test-layouts.yaml")
    qa_report = parse_qa_report("test-layouts-qa-report.json")
    failures = generate_results(slide_map, qa_report, blank_slides, "test-results.md")

    print(f"\n  Report: test-results.md")
    print(f"  Total slides: {len(slide_map)}")
    print(f"  Blank slides: {len(blank_slides)}")
    print(f"  Failed layouts: {failures}")

    # Cleanup
    if not args.keep_artifacts:
        import shutil
        for f in ["test-layouts.yaml", "test-layouts.pptx", "test-layouts-qa-report.json", "test-layouts-qa-report.md"]:
            if os.path.exists(f):
                os.remove(f)
        if os.path.exists("test-layouts-proof"):
            shutil.rmtree("test-layouts-proof")
        print("\n  Cleaned up test artifacts (use --keep-artifacts to preserve)")

    if failures > 0:
        print(f"\n  RESULT: {failures} layout(s) FAILED")
        sys.exit(1)
    else:
        print(f"\n  RESULT: ALL LAYOUTS PASSED")
        sys.exit(0)


if __name__ == "__main__":
    main()
