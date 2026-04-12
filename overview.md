# Deck Builder — Overview

**Owner:** Russ Blaisdell
**Status:** Active
**Source:** `deck-builder/`

## What It Does

YAML-driven PPTX presentation pipeline with 22 slide layouts, automated QA, and Claude vision review. All slides render on a clean canvas using the brand tokens (purple/pink, Urbanist/DM Sans fonts, 147 icons).

## Pipeline

1. **Author** — Write presentation content in YAML (one file per deck)
2. **Build** — `test_deck.py` renders YAML to branded PPTX (10"x5.62")
3. **QA** — `--proof-images` generates per-slide PNGs for visual review
4. **Upload** — `--upload` pushes to Google Drive
5. **Review** — Claude vision reviews each slide for layout, content, and brand compliance

## Key Files

- **Builder:** `test_deck.py`
- **Reference:** `presentation-guide.md` — complete layout reference, icon catalog, build commands
- **Templates:** `deck-templates.md` — starter YAML skeletons (executive, technical, status)
- **Plan:** `SYSTEM-PLAN.md` — architecture and progress
- **Python env:** `/tmp/xlsx-venv` (python-pptx, pyyaml, Pillow)

## Build Command

```bash
/tmp/xlsx-venv/bin/python3 deck-builder/test_deck.py <yaml> --proof-images --upload
```

## Goals

1. Produce leadership-ready decks from YAML in under 5 minutes
2. Consistent the branding across all presentations
3. Reduce deck creation time by >80% vs. manual PowerPoint
4. Support all common presentation formats (executive, technical, status review)

## Effectiveness Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Decks produced | Track monthly count | Count uploaded Drive files |
| Time-to-deck | <5 min from YAML to uploaded PPTX | Build log timestamps |
| Layout coverage | 22 layouts cover >95% of needs | Track when manual slides are needed outside the system |
| QA pass rate | >90% of slides pass visual QA on first build | Count proof-image review corrections |
| Brand compliance | 100% the brand tokens | Claude vision review results |
