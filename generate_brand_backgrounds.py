#!/usr/bin/env python3
"""Generate brand-colored gradient backgrounds for title and agenda slides.

Creates:
  - title-bg.jpg — full-slide gradient (primary → darker) for title/closing slides
  - agenda-left.jpg — left-side gradient panel for agenda slides

Uses PIL to draw smooth gradients from brand colors.
"""

import os
import sys
import yaml

from PIL import Image, ImageDraw, ImageFilter


def hex_to_rgb(h):
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def darken(rgb, factor=0.4):
    return tuple(int(c * (1 - factor)) for c in rgb)


def lighten(rgb, factor=0.3):
    return tuple(int(c + (255 - c) * factor) for c in rgb)


def generate_title_bg(primary_hex, secondary_hex, output_path, width=1920, height=1080):
    """Generate a diagonal gradient background for title slides."""
    primary = hex_to_rgb(primary_hex)
    dark = darken(primary, 0.5)
    secondary = hex_to_rgb(secondary_hex)

    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)

    for y in range(height):
        t = y / height
        # Vertical gradient: dark primary at top → primary at middle → hint of secondary at bottom
        if t < 0.5:
            t2 = t * 2
            r = int(dark[0] + (primary[0] - dark[0]) * t2)
            g = int(dark[1] + (primary[1] - dark[1]) * t2)
            b = int(dark[2] + (primary[2] - dark[2]) * t2)
        else:
            t2 = (t - 0.5) * 2
            r = int(primary[0] + (secondary[0] - primary[0]) * t2 * 0.3)
            g = int(primary[1] + (secondary[1] - primary[1]) * t2 * 0.3)
            b = int(primary[2] + (secondary[2] - primary[2]) * t2 * 0.3)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Add subtle noise/texture for visual interest
    img = img.filter(ImageFilter.GaussianBlur(radius=2))
    img.save(output_path, quality=90)


def generate_agenda_left(primary_hex, secondary_hex, output_path, width=760, height=760):
    """Generate a vertical gradient panel for the agenda left side."""
    primary = hex_to_rgb(primary_hex)
    secondary = hex_to_rgb(secondary_hex)
    light = lighten(primary, 0.4)

    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)

    for y in range(height):
        t = y / height
        # Top-to-bottom: light primary → primary → secondary hint
        if t < 0.6:
            t2 = t / 0.6
            r = int(light[0] + (primary[0] - light[0]) * t2)
            g = int(light[1] + (primary[1] - light[1]) * t2)
            b = int(light[2] + (primary[2] - light[2]) * t2)
        else:
            t2 = (t - 0.6) / 0.4
            r = int(primary[0] + (secondary[0] - primary[0]) * t2 * 0.4)
            g = int(primary[1] + (secondary[1] - primary[1]) * t2 * 0.4)
            b = int(primary[2] + (secondary[2] - primary[2]) * t2 * 0.4)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    img = img.filter(ImageFilter.GaussianBlur(radius=1))
    img.save(output_path, quality=90)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    brands_dir = os.path.join(script_dir, "brands")

    for brand_name in sorted(os.listdir(brands_dir)):
        brand_dir = os.path.join(brands_dir, brand_name)
        yaml_path = os.path.join(brand_dir, "brand.yaml")
        if not os.path.isfile(yaml_path):
            continue

        with open(yaml_path) as f:
            data = yaml.safe_load(f)

        colors = data.get("colors", {})
        primary = colors.get("primary", "#1A365D")
        secondary = colors.get("secondary", "#3182CE")

        # Create title-assets directory
        assets_dir = os.path.join(brand_dir, "title-assets")
        os.makedirs(assets_dir, exist_ok=True)

        # Generate backgrounds
        title_path = os.path.join(assets_dir, "title-bg.jpg")
        agenda_path = os.path.join(assets_dir, "agenda-left.jpg")

        generate_title_bg(primary, secondary, title_path)
        generate_agenda_left(primary, secondary, agenda_path)

        print(f"  {brand_name}: {primary} → {secondary}")

        # Update brand.yaml to point to local backgrounds
        data["title_backgrounds"] = {"default": "title-assets/title-bg.jpg"}
        data["agenda_backgrounds"] = {"default": "title-assets/agenda-left.jpg"}
        with open(yaml_path, "w") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    print(f"\nDone!")


if __name__ == "__main__":
    main()
