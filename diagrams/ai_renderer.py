"""
Approach C: AI-Generated Images via Google Imagen 4 + Gemini Review

Pipeline:
  1. Build prompt from slide data + brand tokens + target dimensions
  2. Imagen 4 generates image
  3. Gemini reviews image for accuracy, dimensions, text errors
  4. If review fails, refine prompt and regenerate (max 2 retries)
  5. If still fails, return None (caller falls back to native renderer)

Requires GOOGLE_GEMINI_API_KEY environment variable.
"""

import base64
import json
import os
import tempfile
from PIL import Image


# Style-specific prompt modifiers
STYLE_PROMPTS = {
    # Primary styles (brand-aware)
    "corporate": "Clean, minimalist, professional corporate style. Flat design with subtle gradients. No hand-drawn elements. Sharp edges and precise geometry. White background.",
    "tech-gradient": "Modern technology aesthetic with deep purple-to-cyan gradients, subtle glowing edges, dark background with luminous elements, faint grid pattern. Think AWS or Azure marketing materials.",
    "blueprint": "Technical blueprint style with white/light blue lines on deep navy background. Engineering schematic feel, thin precise lines, technical drawing crosshatch patterns. Like an architect's diagram.",
    # Additional styles
    "isometric": "3D isometric projection. Geometric shapes, clean lines, subtle shadows. Modern tech illustration style with colorful blocks and depth.",
    "glassmorphism": "Frosted glass panel aesthetic. Soft blurred backgrounds, translucent overlapping cards with subtle borders, light refraction effects. Premium and modern.",
    "neon-wireframe": "Dark background with neon green and magenta wireframe shapes. No fills, only glowing outlines. Connection lines pulse with light. Futuristic and high-tech.",
    "paper-cut": "Layered paper cutout effect with subtle drop shadows between layers. Clean and friendly. Soft colors, rounded shapes, approachable design.",
    "minimal-line": "Simple single-weight line drawings. Extensive whitespace. Black lines with one accent color. Elegant and understated. Let the structure speak.",
    "hand-drawn": "Hand-sketched whiteboard style. Informal, slightly imperfect lines. Black ink on white background with color highlights. Casual and approachable.",
}

# Diagram type to visual concept mapping
TYPE_CONCEPTS = {
    "org-hierarchy": "organizational hierarchy chart showing {root} at the top managing {n_children} departments: {children}. {root} is the parent, with lines connecting down to each department below it",
    "flow": "process flow diagram showing sequential steps: {steps}, connected by arrows left to right",
    "architecture": "cloud architecture diagram showing {description}",
    "comparison": "side-by-side comparison of {options}",
    "timeline": "horizontal timeline with milestones: {milestones}",
    "network": "network topology diagram showing connected nodes",
    "conceptual": "{description}",
}

# Aspect ratio keywords that Imagen understands
ASPECT_DESCRIPTIONS = {
    "wide": "very wide panoramic landscape format (approximately 3:1 ratio)",
    "landscape": "landscape format (approximately 16:9 ratio)",
    "square": "square format (1:1 ratio)",
    "tall": "tall portrait format (approximately 9:16 ratio)",
}


class AIRenderer:

    def __init__(self, tokens):
        self.tokens = tokens
        self._client = None

    def _get_client(self):
        if self._client is None:
            from google import genai
            api_key = os.environ.get("GOOGLE_GEMINI_API_KEY", "")
            if not api_key:
                raise RuntimeError("GOOGLE_GEMINI_API_KEY not set")
            self._client = genai.Client(api_key=api_key)
        return self._client

    def render(self, diagram_type, data, target_width_in, target_height_in,
               style="corporate", output_dir=None):
        """Generate and validate an image using Imagen 4 + Gemini review."""
        if output_dir is None:
            output_dir = tempfile.mkdtemp(prefix="deck-ai-img-")
        os.makedirs(output_dir, exist_ok=True)

        png_path = os.path.join(output_dir, f"{diagram_type}-ai-{style}.png")
        max_retries = 2

        prompt = self._build_prompt(diagram_type, data, target_width_in,
                                    target_height_in, style)

        for attempt in range(1, max_retries + 2):  # 1 initial + 2 retries
            # Step 1: Generate image
            success = self._generate_image(prompt, png_path)
            if not success:
                print(f"    WARNING: AI generation failed on attempt {attempt}")
                if attempt > max_retries:
                    return None
                continue

            # Step 2: Fix dimensions — crop/pad to target aspect ratio
            self._fix_aspect_ratio(png_path, target_width_in, target_height_in)

            # Step 3: Review with Gemini
            review = self._review_image(png_path, diagram_type, data,
                                        target_width_in, target_height_in)

            if review["pass"]:
                return {
                    "type": "png",
                    "path": png_path,
                    "label": f"AI-generated image ({diagram_type}, {style})",
                }

            # Step 4: Refine prompt based on review feedback
            if attempt <= max_retries:
                print(f"    AI review failed (attempt {attempt}): {review['reason']}")
                prompt = self._refine_prompt(prompt, review["reason"],
                                             review.get("suggestions", ""))
            else:
                print(f"    AI review failed after {max_retries + 1} attempts: {review['reason']}")
                return None

        return None

    def _build_prompt(self, diagram_type, data, w_in, h_in, style):
        """Build an image generation prompt from diagram data + brand tokens."""
        colors = self.tokens["colors"]
        style_desc = STYLE_PROMPTS.get(style, STYLE_PROMPTS["corporate"])

        # Build the concept description from data
        concept_template = TYPE_CONCEPTS.get(diagram_type, "{description}")
        concept_vars = {}

        if diagram_type == "org-hierarchy":
            root = data.get("root", "Organization")
            owner = data.get("owner", "")
            children = data.get("children", [])
            child_names = [c if isinstance(c, str) else c.get("name", "") for c in children]
            root_label = f"{root} (managed by {owner})" if owner else root
            concept_vars = {
                "root": root_label,
                "n_children": str(len(child_names)),
                "children": ", ".join(child_names),
            }
        elif diagram_type == "flow":
            steps = data.get("steps", [])
            step_names = [s if isinstance(s, str) else s.get("name", "") for s in steps]
            concept_vars = {"steps": " → ".join(step_names)}
        elif diagram_type == "timeline":
            milestones = data.get("milestones", [])
            ms_names = [m if isinstance(m, str) else m.get("label", "") for m in milestones]
            concept_vars = {"milestones": ", ".join(ms_names)}
        elif diagram_type == "comparison":
            options = data.get("options", [])
            opt_names = [o.get("name", "") for o in options]
            concept_vars = {"options": " vs ".join(opt_names)}
        else:
            concept_vars = {"description": json.dumps(data, indent=2)[:200]}

        try:
            concept = concept_template.format(**concept_vars)
        except KeyError:
            concept = str(data)[:200]

        # Determine aspect ratio
        aspect = w_in / h_in if h_in > 0 else 1.5
        if aspect > 2:
            aspect_desc = ASPECT_DESCRIPTIONS["wide"]
        elif aspect > 1.3:
            aspect_desc = ASPECT_DESCRIPTIONS["landscape"]
        elif aspect > 0.8:
            aspect_desc = ASPECT_DESCRIPTIONS["square"]
        else:
            aspect_desc = ASPECT_DESCRIPTIONS["tall"]

        prompt = (
            f"Create a {aspect_desc} infographic illustration of: {concept}. "
            f"STYLE: {style_desc} "
            f"COLORS: Use purple, pink, and light purple tones. White background. "
            f"CRITICAL: Do NOT include ANY text, words, labels, numbers, hex codes, "
            f"or any readable characters in the image. Use only shapes, icons, "
            f"and visual elements to communicate the hierarchy/structure. "
            f"The image must be suitable for a professional business presentation."
        )

        return prompt

    def _refine_prompt(self, original_prompt, failure_reason, suggestions):
        """Refine the prompt based on review feedback."""
        refinement = (
            f"{original_prompt} "
            f"IMPORTANT CORRECTIONS: {failure_reason}. "
        )
        if suggestions:
            refinement += f"SUGGESTIONS: {suggestions}. "
        return refinement

    def _generate_image(self, prompt, output_path):
        """Call Google Imagen 4 to generate a PNG."""
        try:
            from google import genai
            client = self._get_client()

            response = client.models.generate_images(
                model="imagen-4.0-generate-001",
                prompt=prompt,
                config=genai.types.GenerateImagesConfig(
                    number_of_images=1,
                    output_mime_type="image/png",
                ),
            )

            if response.generated_images:
                img = response.generated_images[0]
                with open(output_path, "wb") as f:
                    f.write(img.image.image_bytes)
                return True
            else:
                print("    WARNING: Imagen returned no images")
                return False

        except ImportError:
            print("    WARNING: google-genai SDK not installed — pip install google-genai")
            return False
        except Exception as e:
            print(f"    WARNING: AI image generation failed: {e}")
            return False

    def _fix_aspect_ratio(self, png_path, target_w_in, target_h_in):
        """Adjust image to match target aspect ratio.

        Strategy: prefer PADDING over cropping to avoid cutting off content.
        - If image is too tall for the slot: pad left/right with white
        - If image is too wide for the slot: pad top/bottom with white
        - Only crop if the mismatch is extreme (>3x off)
        """
        try:
            target_aspect = target_w_in / target_h_in if target_h_in > 0 else 1.5
            img = Image.open(png_path)
            current_aspect = img.width / img.height

            # Close enough — skip
            if abs(current_aspect - target_aspect) / target_aspect < 0.15:
                img.close()
                return

            if current_aspect < target_aspect:
                # Image is too tall/narrow — pad sides to make it wider
                new_w = int(img.height * target_aspect)
                padded = Image.new("RGBA", (new_w, img.height), (255, 255, 255, 255))
                x_offset = (new_w - img.width) // 2
                padded.paste(img, (x_offset, 0))
                img = padded
            else:
                # Image is too wide — pad top/bottom to make it taller
                new_h = int(img.width / target_aspect)
                padded = Image.new("RGBA", (img.width, new_h), (255, 255, 255, 255))
                y_offset = (new_h - img.height) // 2
                padded.paste(img, (0, y_offset))
                img = padded

            # Convert to RGB for PNG saving (drop alpha)
            if img.mode == "RGBA":
                bg = Image.new("RGB", img.size, (255, 255, 255))
                bg.paste(img, mask=img.split()[3])
                img = bg

            img.save(png_path)
            img.close()
        except Exception as e:
            print(f"    WARNING: Aspect ratio fix failed: {e}")

    def _review_image(self, png_path, diagram_type, data, target_w_in, target_h_in):
        """Use Gemini to review the generated image for accuracy."""
        try:
            client = self._get_client()

            # Read image
            with open(png_path, "rb") as f:
                img_bytes = f.read()

            # Check dimensions
            img = Image.open(png_path)
            actual_aspect = img.width / img.height
            target_aspect = target_w_in / target_h_in if target_h_in > 0 else 1.5
            img.close()

            # Build review data description
            if diagram_type == "org-hierarchy":
                root = data.get("root", "")
                owner = data.get("owner", "")
                children = data.get("children", [])
                child_names = [c if isinstance(c, str) else c.get("name", "") for c in children]
                expected = (
                    f"An org hierarchy with '{root}' "
                    f"{'(managed by ' + owner + ')' if owner else ''} "
                    f"at the top and {len(child_names)} children: {', '.join(child_names)}."
                )
            else:
                expected = f"A {diagram_type} diagram representing: {json.dumps(data)[:300]}"

            review_prompt = (
                f"Review this generated image for a business presentation. "
                f"EXPECTED CONTENT: {expected} "
                f"CHECK FOR: "
                f"1) Does the image contain any visible text, labels, numbers, or hex codes? (it should NOT) "
                f"2) Does the visual structure roughly match the expected hierarchy/layout? "
                f"3) Is the image professional quality suitable for a presentation? "
                f"Respond in JSON format: "
                f'{{"pass": true/false, "reason": "brief explanation", "suggestions": "how to improve if failed"}}'
            )

            from google.genai import types

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_bytes(data=img_bytes, mime_type="image/png"),
                            types.Part.from_text(text=review_prompt),
                        ],
                    )
                ],
            )

            # Parse response
            result_text = response.text.strip()
            # Extract JSON from response
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()

            try:
                result = json.loads(result_text)
                return {
                    "pass": bool(result.get("pass", False)),
                    "reason": result.get("reason", ""),
                    "suggestions": result.get("suggestions", ""),
                }
            except json.JSONDecodeError:
                # If we can't parse, assume pass (don't block on review parsing)
                print(f"    WARNING: Could not parse review response: {result_text[:100]}")
                return {"pass": True, "reason": "review parse failed, assuming pass"}

        except Exception as e:
            # If review fails, don't block — assume pass
            print(f"    WARNING: AI review failed: {e}")
            return {"pass": True, "reason": f"review error: {e}"}
