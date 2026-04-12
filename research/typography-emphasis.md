# Typography, Emphasis, and Visual Hierarchy in Executive Presentations

> Part of the [Deck Builder](../README.md) research library. Synthesized into [Presentation Principles](../presentation-principles.md).
> Other research: [Visual Design](visual-design.md) | [Audience Profiles](audience-profiles.md) | [Storytelling Frameworks](storytelling-frameworks.md)

Research findings for the deck builder. Covers bold, italic, color emphasis, font sizing, visual hierarchy patterns, inline formatting implementation, and readability at distance. Each section contains numbered rules with concrete values.

---

## 1. Bold -- When and How to Use

Bold is the strongest inline emphasis tool. It creates a high-contrast weight difference that draws the eye during rapid scanning. Used correctly, bold turns a wall of text into a scannable outline. Used carelessly, it turns a slide into visual noise.

### When to bold

1. **Key numbers and statistics.** Any number that justifies a decision or quantifies impact should be bold. "Revenue grew **23%** year over year" -- the reader's eye hits the number first, which is exactly the point.

2. **Decision points and action items.** The single phrase on a slide that answers "what do you want me to do?" must be bold. If the slide says "Recommendation: migrate to GCP by Q3," the word "migrate to GCP by Q3" carries the weight.

3. **Names of people and teams** when assigning ownership. "**Platform team** owns the migration" is scannable; "Platform team owns the migration" in regular weight buries the assignment. In our builder, this maps to the existing "bold part: rest" colon syntax used in bullets.

4. **The single most important phrase per slide.** Every slide has one sentence that, if the audience remembers nothing else, justifies the slide's existence. That phrase gets bold. Everything else is supporting context.

5. **Labels in label-value pairs.** The pattern "**Status:** On track" or "**Owner:** Rachel McCarron" uses bold to create a visual anchor point, letting the reader scan down a list of labels without reading every value.

### When not to bold

6. **Never bold entire paragraphs.** If everything is bold, nothing is bold. A paragraph of bold text creates a dark, undifferentiated block that is harder to read than regular weight. Bold works by contrast -- it needs surrounding regular text to stand out.

7. **Never bold headers that are already visually distinct.** Our Urbanist ExtraBold headings at 14pt purple are already the heaviest element on the slide. Adding `bold=True` to a heading that is already ExtraBold weight and a different color from body text adds nothing. The heading's size, weight, and color already separate it from body text.

8. **Do not bold for emphasis you can achieve with layout.** If a point needs to stand out, consider whether it belongs in a callout box, a bigger font size, or a different slide entirely. Bold within a dense paragraph is the tool of last resort, not the first instinct.

### The bold budget

9. **Maximum 3-5 bold items per slide.** This is the core discipline. Count the distinct bold runs on a finished slide. If there are more than five, the slide has an emphasis problem. The eye cannot prioritize when six things all demand attention simultaneously. If you have seven bold items, at least two of them are not actually the most important thing on the slide.

10. **One bold item per bullet point, maximum.** In a bulleted list, bold exactly one phrase per bullet -- typically the leading label or the key takeaway. Two bold phrases in the same bullet create competing anchors and slow scanning.

### Bold + color combinations

11. **Bold purple (#5F016F) for names and labels.** This is the current builder convention (see `_build_content_table_bullets` line 2183) and it works well. The combination of weight + brand color creates a strong anchor without introducing non-brand colors.

12. **Bold dark (#333333) for key phrases within body text.** When emphasizing a phrase in body copy (not a label), bold in the body text color is sufficient. Adding color emphasis on top of bold is usually overkill for inline phrases.

13. **Bold pink (#FF80D4) only for hero numbers.** Pink bold should be reserved for the single most prominent data point on a slide -- a big stat number, a percentage in a callout, or a KPI value. Using pink bold on more than one or two items per slide dilutes the brand accent.

14. **Never combine bold + italic + color on the same run.** Triple-stacking emphasis signals desperation rather than clarity. Pick two at most: bold + color, or italic + color. Never all three.

---

## 2. Italics -- Proper Usage

Italics tilt letterforms to create a subtle visual distinction. Unlike bold (which says "this is important"), italics say "this is different" -- a quotation, a term, a title, an aside.

### When to use italics

15. **Quotations embedded in body text.** When a slide includes a short quote from a stakeholder or report, italicize the quoted text: *"We need to ship this by March"* -- VP Engineering. This visually sets the quote apart without a separate text box.

16. **Book, report, and document titles.** Reference to the *Cloud Migration Assessment* or the *Q2 Business Review* uses italics per standard typographic convention. This applies to first-mention references within body text.

17. **Technical terms on first use.** When introducing a term the audience may not know, italics signal "this is a defined term": *blue-green deployment*, *chaos engineering*, *service mesh*. After the first use, subsequent uses appear in regular weight.

18. **Gentle emphasis -- the "aside" voice.** Italics work for parenthetical commentary or caveats: "All figures are *preliminary* and subject to revision." The emphasis is softer than bold, appropriate for qualifications rather than calls to action.

### When not to use italics

19. **Never italicize long passages.** Italic letterforms are harder to read than their upright counterparts because the slanted shapes disrupt the horizontal flow the eye expects. A full paragraph in italics is measurably slower to read. Limit italic runs to one sentence maximum, and prefer single words or short phrases.

20. **Never italicize anything the audience needs to scan quickly.** Bullet points, action items, labels, and key numbers should never be italic. Italics slow reading speed by 5-10% compared to regular weight. For anything that needs to be found at a glance, use bold or color instead.

21. **Italics vs bold decision rule.** If the audience should notice the word during a quick scan, use bold. If the audience will notice it only when reading the surrounding sentence carefully, use italics. Bold is for scanning; italics are for reading.

### Italic + other formatting

22. **Italic + gray for source attributions.** The combination of italic + lighter color (gray #888888) at a smaller font size is the standard pattern for footnotes, sources, and attributions. This is already close to what our builder uses for tertiary text.

23. **Never use italic as the default body style.** Some templates use italic DM Sans as a "stylish" body font. This is a readability mistake. Reserve italics for the specific semantic roles listed above.

---

## 3. Color as Emphasis

Color is the most powerful emphasis tool in presentations because it operates at the pre-attentive level -- the brain registers color differences before conscious reading begins. This makes color emphasis both very effective and very dangerous if overused.

### Brand color emphasis

24. **Pink (#FF80D4) for key stats and callout phrases.** Use the brand pink to highlight the single most important data point or phrase on a slide. Pink on a white or light background (#F0E8F5) creates high contrast. Limit to one or two pink-colored text elements per slide.

25. **Purple (#5F016F) for structural elements.** Headers, section titles, labels, and divider accents use purple. This creates a consistent structural skeleton across the deck. Purple should not be used for inline emphasis within body text -- it belongs on the "frame" of the slide, not the content.

26. **Dark (#333333) for body text.** All regular body text uses near-black rather than pure black (#000000). Pure black on white creates excessive contrast that causes eye fatigue in projected settings. Dark gray is the standard choice for extended reading.

27. **Gray (#888888) for supporting and tertiary text.** Footnotes, source attributions, timestamps, and secondary labels use gray. This creates a clear visual hierarchy: purple (structure) > dark (body) > gray (supporting).

### Status and semantic colors

28. **The RAG (Red-Amber-Green) pattern.** Use these sparingly and consistently:
    - Green (#4EC98B or similar) -- on track, complete, success, approved
    - Amber/Yellow (#FFD766 or similar) -- at risk, needs attention, pending
    - Red (#E85D5D or similar) -- blocked, failed, critical, overdue

29. **RAG rules for responsible use:**
    - Use RAG only on dedicated status slides (status boards, KPI dashboards, project trackers). Do not scatter red and green throughout narrative slides.
    - Always pair RAG color with a text label ("On Track," "At Risk," "Blocked"). Color must never be the sole carrier of meaning.
    - Maximum two RAG-colored elements per non-status slide. If a narrative slide has three red items and two green items, it is a status slide pretending to be a narrative slide -- redesign it.
    - Avoid the "Christmas tree" effect: a slide with red, green, amber, purple, and pink text is visually chaotic. If you need RAG colors and brand colors on the same slide, desaturate one set (use muted pastels for RAG backgrounds, keep text in brand colors).

30. **When RAG colors are overused.** If every slide in a deck has red/green indicators, the audience becomes desensitized. Reserve RAG for the 2-4 slides where status is the actual content. On other slides, use words like "on track" or "delayed" in brand colors.

### Accessibility

31. **Never use color as the only way to convey information.** Approximately 8% of men and 0.5% of women have some form of color vision deficiency. Every color-coded element must also have a text label, icon, or pattern. Our status board layout (`_build_status_board`) correctly pairs colored circles with text summaries -- this pattern should be universal.

32. **Ensure 4.5:1 contrast ratio for text.** All text colors must meet WCAG AA contrast against their background:
    - Purple (#5F016F) on white: 11.2:1 -- excellent
    - Pink (#FF80D4) on white: 2.4:1 -- FAILS for body text. Use pink only on dark backgrounds or at large sizes (18pt+)
    - Dark (#333333) on white: 12.6:1 -- excellent
    - Gray (#888888) on white: 3.5:1 -- fails AA for small text; acceptable only at 14pt+ or for decorative elements

33. **Pink text accessibility rule.** Because #FF80D4 fails contrast requirements on white backgrounds at small sizes, pink text should only be used at 18pt or larger, or on purple/dark backgrounds where contrast is sufficient. For inline emphasis within 10pt body text, use bold purple instead of pink.

---

## 4. Font Size Hierarchy in Presentations

Font sizing is context-dependent. A deck projected on a conference room screen at 15 feet has different requirements than a PDF read on a laptop. Our builder must support both modes.

### Projected presentations (conference room, all-hands)

34. **Nothing below 18pt for body text in projected decks.** The person in the last row of a 30-seat conference room is 25-30 feet from the screen. At that distance, 18pt is the practical minimum for comfortable reading on a 1080p projector. Below 18pt, attendees squint, disengage, or pull out their phones to read the shared PDF instead.

35. **Projected size hierarchy (the "3-level rule"):**
    - Level 1 -- Headline: 28-36pt, Urbanist ExtraBold, purple
    - Level 2 -- Key points: 20-24pt, DM Sans Bold, dark
    - Level 3 -- Supporting detail: 18-20pt, DM Sans Regular, dark or gray

36. **If content does not fit at 18pt, the slide has too much content.** For projected presentations, the fix is never "make the font smaller" -- it is "split into two slides" or "move detail to an appendix." A projected slide with 8pt footnotes is a slide that has lost its audience.

### Read-along decks (sent as PDF, read on screen)

37. **10-12pt body text is acceptable for read-along decks.** When the audience reads on a laptop or prints the deck, smaller sizes work because viewing distance is 18-24 inches. Our current body sizes (9-10pt secondary, 12pt primary) are appropriate for this mode.

38. **Read-along size hierarchy:**
    - Level 1 -- Headline: 14-18pt, Urbanist ExtraBold, purple
    - Level 2 -- Key points: 11-14pt, DM Sans Bold, dark
    - Level 3 -- Supporting detail: 9-10pt, DM Sans Regular, dark
    - Level 4 -- Footnotes/sources: 7-8pt, DM Sans Regular, gray

39. **7pt absolute minimum for any text.** Even in read-along mode, text below 7pt becomes unreadable on a 1080p screen at 100% zoom and is nearly invisible when printed. Our tertiary level at 8pt is at the lower boundary. The 7pt legend text (lines 2128-2150 in `build_deck.py`) should not go smaller.

### How our current sizes compare

40. **Current builder sizes are optimized for read-along decks.** The typography hierarchy (primary 12pt bold, secondary 10pt, tertiary 8pt) produces dense, information-rich slides that work well when recipients read them as PDFs. This is the correct choice for Russ's primary use case: executive read-aheads, briefing decks, and strategy documents that are shared via Google Drive.

41. **For any deck that will be projected, add a `presentation_mode` YAML flag.** When set, the builder should multiply all font sizes by 1.5-2x and enforce a minimum of 18pt for body text. This would transform the hierarchy to approximately: primary 20-24pt, secondary 16-18pt, tertiary 14-16pt. Content that overflows at these sizes should trigger a proof-report warning rather than silent shrinking.

42. **Table font sizes are the most aggressive.** Tables currently use 7-9pt (lines 1831-1840, 1975-1976). For read-along decks this works. For projected decks, tables below 14pt are unreadable. The builder should warn when table mode is used with `presentation_mode: true`.

---

## 5. Visual Hierarchy on a Single Slide

The arrangement of elements on a slide creates an implicit reading order. Understanding how the eye moves across a slide is the foundation of visual hierarchy.

### Eye movement patterns

43. **The Z-pattern.** On slides with evenly distributed content (no dominant element), the eye follows a Z: top-left, across to top-right, diagonally to bottom-left, across to bottom-right. This means:
    - The headline (top-left or top-center) is read first. Always.
    - The bottom-right is read last -- put the CTA, next step, or key takeaway there.
    - The diagonal (top-right to bottom-left) is the "dead zone" -- content placed only in this zone may be skipped during quick scanning.

44. **The F-pattern.** On text-heavy slides (bulleted lists, two-column layouts), the eye follows an F: left margin top-to-bottom, then a sweep rightward at the top, and a shorter sweep rightward in the middle. This means:
    - Bold labels at the left margin of each bullet are critical -- they form the vertical scanning rail.
    - Right-aligned content is seen only if the left margin gives the eye a reason to move right.
    - In two-column layouts, the left column is read more thoroughly than the right. Put the more important content on the left.

45. **Place the most important element where eyes land first.** For most layouts, this is the top-left quadrant. For slides with a single hero element (big stat, key quote), center the element -- centering overrides the Z/F patterns by creating a focal point through size and whitespace.

### Combining hierarchy signals

46. **The four levers of emphasis (in order of strength):**
    1. **Size** -- the largest element wins. A 36pt headline dominates a 10pt body block completely.
    2. **Color** -- a single pink or purple element among gray/dark text pulls the eye before reading begins.
    3. **Weight** -- bold text within a regular-weight paragraph creates a local emphasis point.
    4. **Position** -- top-left beats bottom-right; centered beats peripheral; above-the-fold beats below.

47. **Use at most two levers per emphasis point.** A number that is large (24pt) and pink (#FF80D4) is emphatic. Making it also bold and top-left is redundant. Each additional lever adds diminishing returns and risks visual clutter. Two levers create emphasis; four levers create noise.

48. **The "squint test."** Blur the slide (or squint until text is illegible). The visual hierarchy should still be apparent: you should see which element is the headline, which is the key data point, and which is supporting text, even without reading a word. If the slide looks like a uniform gray blob when blurred, the hierarchy is too flat.

### Whitespace as hierarchy

49. **Whitespace is not empty space -- it is a framing device.** The gap between a headline and body text signals "these are different levels." The gap between sections signals "these are different topics." Reducing whitespace to cram more content flattens the hierarchy.

50. **Minimum spacing rules:**
    - After headline: 0.15-0.25 inches
    - Between sections: 0.20-0.35 inches
    - Between bullet items: 0.05-0.10 inches (or 3-6pt space-after)
    - Margin from slide edge: 0.35 inches minimum (our builder uses 0.35, which is correct)
    - Between a divider line and the next element: 0.10-0.15 inches

---

## 6. Inline Formatting -- Bold/Italic Runs Within Body Text

The most impactful near-term improvement to the deck builder is support for inline formatting within body text. Currently, bold/italic can only be applied to entire text boxes or via the colon-split pattern in bullets. Markdown-style inline formatting would enable precise emphasis within any text field.

### How python-pptx supports this

51. **Multiple runs per paragraph.** python-pptx supports adding multiple runs to a single paragraph, each with independent font properties (size, bold, italic, color, name). This is already used in the builder -- see the bullet "bold part: rest" pattern at line 2176-2189 and the legend rendering at line 2125-2151. The infrastructure exists; what is missing is a general-purpose parser.

### Proposed YAML syntax

52. **Markdown-style inline bold and italic.** The YAML author writes natural text with markdown delimiters:
    ```yaml
    body: "Revenue grew **23%** year over year, driven by *organic* expansion"
    ```
    The builder parses this into three runs:
    - "Revenue grew " -- regular
    - "23%" -- bold
    - " year over year, driven by " -- regular
    - "organic" -- italic
    - " expansion" -- regular

53. **Extended syntax for color emphasis.** For cases where color matters, support a bracketed syntax:
    ```yaml
    body: "Status: {green|On Track} -- deployment scheduled for Friday"
    ```
    Parsed into runs:
    - "Status: " -- regular
    - "On Track" -- green colored
    - " -- deployment scheduled for Friday" -- regular

54. **Combined bold + color.** Allow nesting or a compound syntax:
    ```yaml
    body: "The **{pink|23%}** increase exceeded our target"
    ```
    This produces a run that is both bold and pink. This is the most complex case and should be implemented last.

### Implementation approach

55. **A `parse_rich_text()` function** that takes a string and returns a list of run descriptors:
    ```python
    def parse_rich_text(text):
        """Parse markdown-style inline formatting into run descriptors.

        Returns: list of dicts, each with keys:
            text (str), bold (bool), italic (bool), color (tuple or None)
        """
    ```
    This function would use regex to split on `**...**` (bold), `*...*` (italic), and `{color|...}` (color) delimiters. Unparsed segments become regular runs.

56. **An `add_rich_text_box()` function** that replaces `add_text_box()` for any text that may contain inline formatting:
    ```python
    def add_rich_text_box(slide, text, left, top, width, height,
                          font_size=12, font_name="DM Sans",
                          base_color=None, alignment=PP_ALIGN.LEFT):
        """Add a text box with inline bold/italic/color runs."""
    ```
    For plain text (no markdown delimiters detected), this falls through to the existing `add_text_box()` behavior. No performance penalty for the common case.

57. **Update `estimate_text_height()` to ignore formatting markers.** The height estimator counts characters for line-wrapping calculations. It must strip `**`, `*`, and `{color|...}` delimiters before counting, or height estimates will be slightly too tall.

### When inline formatting helps

58. **Label-value pairs.** "**Owner:** Rachel McCarron" is clearer than "Owner: Rachel McCarron" because the label is visually anchored. The existing colon-split pattern handles this for bullets but not for general body text.

59. **Key numbers in narrative text.** "Cloud spend decreased **$1.2M** (**18%**) in Q1" puts the two numbers the audience cares about in bold, letting them skip the surrounding words during a scan.

60. **Action items within body text.** "Next step: **schedule the architecture review** with Platform team by March 15" makes the action scannable even when buried in a paragraph.

### When inline formatting creates visual noise

61. **Do not use inline formatting as a substitute for structure.** If a paragraph has five bold phrases, it should probably be a bulleted list instead. Inline formatting is for 1-2 emphasis points within a flowing sentence, not for restructuring content that belongs in a different layout.

62. **Do not mix bold and italic in the same sentence** unless the semantic roles are distinct (e.g., a bold key phrase containing an italic title: "**Review the *Migration Assessment* by Friday**"). Two different emphasis styles in the same sentence forces the reader to decode what each one means.

63. **Do not use inline formatting in headers or titles.** Headers are already the top of the visual hierarchy. Bolding a word within a header creates a hierarchy-within-a-hierarchy that confuses the eye. If one word in a header matters more than the others, the header is too long.

---

## 7. Readability at Distance

Presentations are often viewed at distances ranging from 3 feet (laptop screen share) to 50 feet (auditorium). Font size, weight, and spacing all interact with distance to determine whether text is legible.

### Minimum readable sizes by distance

64. **Distance-to-size table:**

    | Viewing distance | Minimum body text | Minimum heading | Notes |
    |-----------------|-------------------|-----------------|-------|
    | 3-5 ft (laptop) | 9pt | 14pt | Our current read-along sizes work |
    | 6-10 ft (small meeting) | 14pt | 20pt | Typical 4-person huddle room |
    | 10-20 ft (conference room) | 18pt | 28pt | Standard 10-20 person room |
    | 20-30 ft (large conf room) | 24pt | 36pt | 30+ person room, projector |
    | 30-50 ft (auditorium) | 32pt | 48pt | All-hands, keynote stage |

    The rule of thumb: **divide the farthest viewing distance (in feet) by 1 to get the minimum point size.** At 24 feet, text should be at least 24pt.

65. **The "8H rule" for screen readability.** If the projected image height is H, a viewer should be no farther than 8H from the screen for comfortable reading of body text. For a projector with a 4-foot-tall image, the maximum comfortable distance is 32 feet. At that distance, 24pt is the minimum body text size.

### Font weight at projection

66. **Thin and light font weights fail at projection.** Projectors reduce effective contrast compared to LCD screens. Thin strokes (hairline weight, light weight) lose definition and become hard to distinguish from the background. This is why Urbanist ExtraBold is the correct choice for headings -- it remains readable even on a washed-out projector.

67. **DM Sans Regular at 10pt is readable at laptop distance but not at projection distance.** DM Sans has moderate stroke width at Regular weight. At 10pt projected, the strokes are too thin for back-row readability. For projected use, DM Sans should be at least 18pt at Regular weight, or 14pt at Medium/Bold weight.

68. **If projecting, prefer DM Sans Medium or Bold for body text.** The extra stroke width compensates for projector contrast loss. For read-along decks this is unnecessary -- Regular weight at 10pt is fine on screen.

### Line length

69. **Optimal line length: 45-75 characters.** Research on reading speed and comprehension consistently shows that lines of 45-75 characters (including spaces) produce the best reading outcomes. Shorter lines cause too many line breaks; longer lines cause the eye to lose its place when returning to the left margin.

70. **For our 10-inch slide width with 0.35-inch margins:** The text area is approximately 9.3 inches wide. At 10pt DM Sans, this fits roughly 120 characters per line -- far too wide. For body text blocks, consider:
    - Full-width (9.3"): Good for 1-2 line headlines and short labels
    - Two-third width (6.0"): Appropriate for body paragraphs at 10pt (approximately 78 characters)
    - Half width (4.5"): Good for column layouts at 10pt (approximately 58 characters)
    - One-third width (3.0"): Tight but workable for 10pt (approximately 39 characters -- near minimum)

71. **In two-column and three-column layouts, line length is naturally constrained.** Our side-by-side and three-column layouts produce column widths of 4.0-4.5 inches and 2.8-3.0 inches respectively. At 10pt, these produce 52-58 and 36-39 characters per line. The two-column width is near-ideal; the three-column width is at the low end but acceptable for bulleted content.

### Line spacing

72. **Line spacing (leading) should be 1.2-1.5x the font size.** Our `estimate_text_height()` uses 1.4x leading (line 199: `line_height = font_size_pt * 1.4 / 72`), which is in the optimal range. Specific recommendations:
    - 1.2x -- dense content where vertical space is scarce (tables, cards, footnotes)
    - 1.3-1.4x -- standard body text (our current default is correct)
    - 1.5x -- projected presentations and slides with minimal text where readability at distance matters

73. **Space-after for paragraphs: 3-6pt for body, 8-12pt for sections.** Our builder uses `Pt(3)` space-after for bullet items (line 2174) and `Pt(4)` for agenda items (line 662). These are appropriate for read-along density. For projected decks, increase to 6-8pt.

---

## 8. Summary of Recommendations for the Deck Builder

### Immediate implementation priorities

74. **Add `parse_rich_text()` and `add_rich_text_box()`.** This unlocks markdown-style bold and italic in any text field. The colon-split pattern in bullets is a special case of this; the general parser would subsume it.

75. **Add a `presentation_mode` YAML flag** that scales font sizes for projection:
    ```yaml
    meta:
      presentation_mode: true  # scales all text for projected viewing
    ```
    When enabled: minimum body size 18pt, minimum heading size 28pt, minimum table text 14pt. Content overflow triggers proof-report warnings.

76. **Enforce the bold budget in proof reports.** The proof renderer should count bold runs per slide and flag any slide with more than 5 bold items as "emphasis overload."

### Design token additions

77. **Add semantic color tokens:**
    ```python
    STATUS_GREEN  = RGBColor(0x4E, 0xC9, 0x8B)  # on track / success
    STATUS_AMBER  = RGBColor(0xFF, 0xD7, 0x66)  # at risk / warning
    STATUS_RED    = RGBColor(0xE8, 0x5D, 0x5D)  # blocked / critical
    EMPHASIS_PINK = RGBColor(0xFF, 0x80, 0xD4)  # hero number accent
    ```
    These are already used implicitly in various builders. Making them explicit design tokens ensures consistency.

78. **Add an italic body font variant.** Currently the builder never sets `run.font.italic = True` anywhere. Adding italic support requires no new font installation -- DM Sans includes italic variants. The parser just needs to set the property.

### Rules to embed in the build process

79. **Proof report checks to add:**
    - Bold run count per slide (warn if > 5)
    - Pink text on white background at size < 18pt (accessibility failure)
    - Body text below 7pt (readability failure)
    - Line length exceeding 80 characters at body font size (readability warning)
    - Mixed RAG colors and brand pink on the same slide (visual chaos warning)

80. **Content density guidelines for YAML authors:**
    - Maximum 6 bullet points per slide at secondary size (10pt)
    - Maximum 4 bullet points per slide at primary size (12pt)
    - If a text block exceeds 0.6x the slide height, split into two slides
    - Tables with more than 6 columns should auto-reduce font size (already implemented)
    - Projected mode: maximum 4 bullet points per slide, no tables with more than 4 columns

---

## Appendix A: Current Deck Builder Font Size Inventory

Extracted from `build_deck.py` as of 2026-03-28:

| Context | Size | Weight | Color | Assessment |
|---------|------|--------|-------|------------|
| Typography primary | 12pt | Bold | Purple | Good for read-along |
| Typography secondary | 10pt | Regular | Dark | Good for read-along |
| Typography tertiary | 8pt | Regular | Gray | At lower boundary |
| Column/section titles | 14pt | Regular | Purple | Appropriate |
| Column/section body | 10pt | Regular | Dark | Appropriate |
| Table header (few cols) | 9-10pt | Bold | White on purple | Dense but readable |
| Table header (7+ cols) | 8pt | Bold | White on purple | At lower boundary |
| Table body (few cols) | 8-9pt | Regular | Dark | Dense but readable |
| Table body (7+ cols) | 7pt | Regular | Dark | Absolute minimum |
| Bullet text | 9pt | Mixed | Purple/Dark | Slightly small |
| Legend/footnote | 7pt | Regular | Gray | Absolute minimum |
| Big stat number | varies | Bold | Purple | Context-dependent |
| Agenda items | dynamic | Bold | Dark/Purple | Auto-sized |
| Quote text | 18pt | Regular | Purple | Good for emphasis |
| Section divider headline | 36pt | ExtraBold | White | Good for projection |
| Callout text | 20pt | ExtraBold | Purple | Good for emphasis |

## Appendix B: python-pptx Inline Formatting Reference

The minimal code pattern for multi-run paragraphs:

```python
from pptx.util import Pt
from pptx.dml.color import RGBColor

# Single paragraph with mixed formatting
p = text_frame.paragraphs[0]

run_regular = p.add_run()
run_regular.text = "Revenue grew "
run_regular.font.name = "DM Sans"
run_regular.font.size = Pt(10)

run_bold = p.add_run()
run_bold.text = "23%"
run_bold.font.name = "DM Sans"
run_bold.font.size = Pt(10)
run_bold.font.bold = True

run_regular2 = p.add_run()
run_regular2.text = " year over year"
run_regular2.font.name = "DM Sans"
run_regular2.font.size = Pt(10)
```

Each `add_run()` creates an independent `<a:r>` element in the OOXML with its own `<a:rPr>` (run properties). There is no limit on the number of runs per paragraph. Font properties that are not explicitly set inherit from the paragraph's default run properties (`<a:defRPr>`).
