#!/usr/bin/env python3
"""Brand Onboarding CLI — Extract, label, then launch wizard for review.

Default flow:
  1. Extract theme, images, icons from template and/or corpus (Python)
  2. Label icons with Claude Code (parallel `claude -p` instances)
  3. Launch browser wizard with everything pre-loaded for visual review
  4. User selects images, reviews icons, clicks Finalize

Flags:
  --auto     Skip wizard, auto-select everything (for scripting/CI)
  --skip-ai  Skip Claude Code icon labeling, use generic names
  --port     Wizard port (default: 5002)

Usage:
    python3 onboard_cli.py --name "acme" --template path/to/template.pptx
    python3 onboard_cli.py --name "acme" --template t.pptx --corpus ./decks/
    python3 onboard_cli.py --name "acme" --corpus ./decks/
    python3 onboard_cli.py --name "acme" --template t.pptx --auto  # no wizard
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import webbrowser
from pathlib import Path

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pptx import Presentation
from patch_template_theme import extract_theme, derive_theme, inject_theme, save_theme
from extract_brand_images import extract_all_images
from extract_icons import (
    extract_icons_from_pptx, extract_icons_from_corpus, deduplicate_icons,
    label_icons_with_claude_code, _generic_labels, save_icon_catalog
)
from onboard_brand import (
    theme_to_brand_yaml, generate_backgrounds, save_brand_images,
    extract_canvas_size, extract_corpus_colors
)


def extract_all(name, template_path=None, corpus_dir=None, skip_ai=False):
    """Run all extraction steps. Returns a state dict for the wizard.

    This is the heavy lifting — theme, images, icons, labels.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    state = {
        'brand_name': name,
        'template_path': template_path,
        'corpus_dir': corpus_dir,
        'theme': None,
        'canvas': None,
        'images': [],      # non-icon images (backgrounds, panels, logos)
        'extracted': None,  # raw extraction results
        'icon_groups': [],
        'icon_labels': [],
    }

    # ── Theme ─────────────────────────────────────────────────
    print("\nSTEP 1: Theme extraction")
    if template_path:
        state['theme'] = extract_theme(template_path)
        prs = Presentation(template_path)
        state['canvas'] = extract_canvas_size(prs)
        print(f"  Heading: {state['theme']['fonts']['heading']}")
        print(f"  Body: {state['theme']['fonts']['body']}")
        print(f"  Primary (dk1): {state['theme']['colors'].get('dk1')}")

        if corpus_dir:
            corpus_colors = extract_corpus_colors(corpus_dir)
            if corpus_colors:
                print(f"  Corpus enrichment: {len(corpus_colors)} dominant colors")
    elif corpus_dir:
        corpus_colors = extract_corpus_colors(corpus_dir)
        top = list(corpus_colors.keys())
        colors = {
            "primary": top[0] if len(top) >= 1 else "#1A365D",
            "secondary": top[1] if len(top) >= 2 else "#3182CE",
        }
        state['theme'] = derive_theme(colors, {"heading": "Arial", "body": "Arial"})
        print(f"  Synthesized from corpus: dk1={state['theme']['colors']['dk1']}")
    else:
        existing_yaml = os.path.join(script_dir, 'brands', name, 'brand.yaml')
        if os.path.isfile(existing_yaml):
            with open(existing_yaml) as f:
                data = yaml.safe_load(f)
            state['theme'] = derive_theme(data.get('colors', {}), data.get('fonts', {}))
            print(f"  Derived from existing brand.yaml")
        else:
            print("  ERROR: No template, corpus, or existing brand.yaml")
            return None

    # ── Images ────────────────────────────────────────────────
    print("\nSTEP 2: Image extraction")
    sources = []

    if template_path:
        extracted = extract_all_images(template_path)
        state['extracted'] = extracted
        non_icon = [img for img in extracted['images']
                    if img['category'] not in ('icon', 'small')]
        state['images'] = non_icon
        sources.append(f"template ({len(non_icon)} images)")

    if corpus_dir:
        for pptx_file in sorted(Path(corpus_dir).glob("*.pptx")):
            try:
                corpus_extracted = extract_all_images(str(pptx_file))
                seen_hashes = {img['hash'] for img in state['images']}
                for img in corpus_extracted['images']:
                    if img['category'] not in ('icon', 'small') and img['hash'] not in seen_hashes:
                        img['source'] = pptx_file.name
                        state['images'].append(img)
                        seen_hashes.add(img['hash'])
                # Merge into extracted for icon purposes
                if not state['extracted']:
                    state['extracted'] = corpus_extracted
            except Exception:
                continue
        sources.append(f"corpus ({len(state['images'])} total after dedup)")

    if sources:
        full_bleed = sum(1 for img in state['images'] if img['category'] == 'full-bleed')
        panels = sum(1 for img in state['images'] if img['category'] == 'panel')
        logos = sum(1 for img in state['images'] if img['category'] == 'logo')
        print(f"  Sources: {', '.join(sources)}")
        print(f"  {full_bleed} backgrounds, {panels} panels, {logos} logos")
    else:
        print("  No images found — will generate gradients")

    # ── Icons ─────────────────────────────────────────────────
    print("\nSTEP 3: Icon extraction + labeling")
    all_icons = []

    if template_path:
        template_icons = extract_icons_from_pptx(template_path)
        all_icons.extend(template_icons)
        print(f"  Template: {len(template_icons)} raw icons")

    if corpus_dir:
        corpus_icons = extract_icons_from_corpus(corpus_dir)
        seen = {ic['hash'] for ic in all_icons}
        new = [ic for ic in corpus_icons if ic['hash'] not in seen]
        all_icons.extend(new)
        if new:
            print(f"  Corpus: {len(new)} additional icons")

    if all_icons:
        groups = deduplicate_icons(all_icons)
        state['icon_groups'] = groups
        print(f"  Deduplicated: {len(groups)} unique designs")

        if not skip_ai:
            print(f"  Labeling with Claude Code...")
            state['icon_labels'] = label_icons_with_claude_code(groups)
        else:
            state['icon_labels'] = _generic_labels(groups)
            print(f"  Using generic labels (AI skipped)")
    else:
        print("  No icons found")

    return state


def auto_finalize(state):
    """Auto-select images and build brand package without wizard."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    name = state['brand_name']
    output_dir = os.path.join(script_dir, 'brands', name)
    os.makedirs(output_dir, exist_ok=True)

    theme = state['theme']
    canvas = state['canvas']

    # Save theme
    save_theme(theme, os.path.join(output_dir, 'theme.json'))

    # Copy/build template
    if state['template_path']:
        shutil.copy2(state['template_path'], os.path.join(output_dir, 'template.pptx'))
    else:
        generic = os.path.join(script_dir, 'brands', 'generic', 'template.pptx')
        shutil.copy2(generic, os.path.join(output_dir, 'template.pptx'))
        inject_theme(os.path.join(output_dir, 'template.pptx'), theme)

    # Extract and save layout mapping
    from extract_layout_mapping import extract_layout_mapping
    template_pptx = os.path.join(output_dir, 'template.pptx')
    mapping = extract_layout_mapping(template_pptx)
    clean_mapping = {k: v for k, v in mapping.items() if k != 'all_placeholders'}
    with open(os.path.join(output_dir, 'layout_mapping.json'), 'w') as f:
        json.dump(clean_mapping, f, indent=2)
    print(f"  Layout mapping: canvas={clean_mapping['blank_canvas_idx']} footers={len(clean_mapping['footers'])}")

    # Auto-select images
    image_paths = None
    if state['images']:
        full_bleed = [img for img in state['images'] if img['category'] == 'full-bleed']
        panels = [img for img in state['images'] if img['category'] == 'panel']
        logos = [img for img in state['images'] if img['category'] == 'logo']

        selections = {
            'title': sorted(full_bleed, key=lambda x: -x['size_kb'])[:3],
            'agenda': sorted(panels, key=lambda x: -x['size_kb'])[:3],
            'section': sorted(full_bleed, key=lambda x: -x['size_kb'])[:1],
            'closing': sorted(full_bleed, key=lambda x: -x['size_kb'])[:1],
            'logo': logos[0] if logos else None,
        }
        image_paths = save_brand_images(selections, output_dir)
        print(f"\n  Auto-selected: {len(selections['title'])} title, "
              f"{len(selections['agenda'])} agenda"
              f"{', 1 logo' if selections['logo'] else ''}")
    else:
        primary = theme['colors'].get('dk1', '#1A365D')
        secondary = theme['colors'].get('dk2', '#3182CE')
        generate_backgrounds(output_dir, primary, secondary)
        image_paths = {
            'title_backgrounds': {"default": "title-assets/title-bg.jpg"},
            'agenda_backgrounds': {"default": "title-assets/agenda-left.jpg"},
        }
        print(f"\n  Generated gradient backgrounds")

    # Save icons
    if state['icon_groups'] and state['icon_labels']:
        save_icon_catalog(state['icon_groups'], state['icon_labels'], output_dir)
        print(f"  Saved {len(state['icon_labels'])} icons")

    # Generate brand.yaml
    brand_yaml_path = os.path.join(output_dir, 'brand.yaml')
    if not os.path.isfile(brand_yaml_path):
        brand_data = theme_to_brand_yaml(name, theme, canvas, image_paths=image_paths)
        with open(brand_yaml_path, 'w') as f:
            yaml.dump(brand_data, f, default_flow_style=False, sort_keys=False)
        print(f"  Generated brand.yaml")

    # Validation
    test_yaml = os.path.join(script_dir, 'examples', 'showcase-generic.yaml')
    if os.path.isfile(test_yaml):
        result = subprocess.run(
            [sys.executable, os.path.join(script_dir, 'build_deck.py'),
             test_yaml, '--output', os.path.join(output_dir, 'validation.pptx')],
            capture_output=True, text=True,
        )
        print(f"  Validation: {'SUCCESS' if result.returncode == 0 else 'FAILED'}")

    print(f"\n  Brand package: brands/{name}/")
    print(f"  Usage: brand: {name}")
    return output_dir


def launch_wizard(state, port=5002):
    """Launch the browser wizard pre-loaded with extraction results."""
    # The wizard needs the state passed via a temp file
    import tempfile
    state_file = tempfile.mktemp(suffix='.json', prefix='onboard-state-')

    # Serialize state (without blobs — wizard will re-extract from template)
    wizard_state = {
        'brand_name': state['brand_name'],
        'template_path': state['template_path'],
        'corpus_dir': state['corpus_dir'],
        'theme': state['theme'],
        'canvas': state['canvas'],
        'icon_labels': state['icon_labels'],
    }
    with open(state_file, 'w') as f:
        json.dump(wizard_state, f)

    print(f"\nLaunching wizard at http://localhost:{port}")
    print(f"  Review images, icons, and theme in the browser.")
    print(f"  Click 'Create Brand Package' when ready.")
    print(f"  Press Ctrl+C to cancel.\n")

    # Set env var so wizard picks up pre-extracted state
    env = os.environ.copy()
    env['ONBOARD_STATE_FILE'] = state_file
    env['ONBOARD_BRAND_NAME'] = state['brand_name']

    # Open browser
    webbrowser.open(f'http://localhost:{port}')

    # Run wizard (blocking)
    try:
        subprocess.run(
            [sys.executable, os.path.join(os.path.dirname(__file__), 'onboard_wizard.py'),
             '--port', str(port)],
            env=env,
        )
    except KeyboardInterrupt:
        print("\nWizard stopped.")
    finally:
        if os.path.isfile(state_file):
            os.unlink(state_file)


def main():
    parser = argparse.ArgumentParser(
        description="Brand Onboarding — extract from template/corpus, review in browser")
    parser.add_argument("--name", required=True, help="Brand name")
    parser.add_argument("--template", help="PPTX template file")
    parser.add_argument("--corpus", help="Directory of example PPTX files")
    parser.add_argument("--auto", action="store_true",
                        help="Auto-select everything, skip wizard (for scripting)")
    parser.add_argument("--skip-ai", action="store_true",
                        help="Skip Claude Code icon labeling")
    parser.add_argument("--port", type=int, default=5002,
                        help="Wizard port (default: 5002)")
    args = parser.parse_args()

    if not args.template and not args.corpus:
        # Check for existing brand.yaml
        script_dir = os.path.dirname(os.path.abspath(__file__))
        existing = os.path.join(script_dir, 'brands', args.name, 'brand.yaml')
        if not os.path.isfile(existing):
            parser.error("Provide --template, --corpus, or have an existing brand.yaml")

    print(f"\n{'='*60}")
    print(f"  Brand Onboarding: {args.name}")
    print(f"{'='*60}")

    # Step 1-3: Extract everything
    state = extract_all(
        name=args.name,
        template_path=args.template,
        corpus_dir=args.corpus,
        skip_ai=args.skip_ai,
    )

    if not state:
        sys.exit(1)

    if args.auto:
        # Auto mode: skip wizard, finalize immediately
        print("\nSTEP 4: Auto-finalize (no wizard)")
        auto_finalize(state)
    else:
        # Default: launch wizard for visual review
        print("\nSTEP 4: Launching wizard for review...")
        launch_wizard(state, port=args.port)


if __name__ == "__main__":
    main()
