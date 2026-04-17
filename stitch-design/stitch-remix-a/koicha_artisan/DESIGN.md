# Design System: The Tactile Editorial

## 1. Overview & Creative North Star
**Creative North Star: "The Modern Archivist"**

This design system rejects the frantic, "frictionless" speed of standard SaaS interfaces in favor of a curated, editorial experience. It is designed to feel like a high-end lifestyle magazine or a physical atelier—places where silence has value and every element is placed with intentionality. 

We move beyond the "template" look by embracing **intentional asymmetry** and **expansive negative space**. Rather than boxing content into rigid grids, we treat the screen as a canvas of organic "rice-paper" layers. Key brand moments should utilize overlapping elements—such as a serif headline partially masking a high-fidelity image—to create a sense of tactile depth and artisan craft.

---

## 2. Colors & Surface Philosophy
The palette is rooted in nature and traditional Korean aesthetics: the warmth of fermented ceramics and the vegetal depth of ceremonial matcha.

### The "No-Line" Rule
**Strict Mandate:** Designers are prohibited from using 1px solid borders for sectioning or containment. Traditional dividers make a premium brand feel like a data table. Instead, define boundaries through:
- **Tonal Shifts:** Transitioning from `surface` (#fbf9f4) to `surface-container-low` (#f5f3ee).
- **Whitespace:** Using generous vertical padding to signal the end of a narrative beat.

### Surface Hierarchy & Nesting
Treat the UI as a physical stack of fine papers.
- **Base Layer:** `surface` (#fbf9f4) — Used for the widest expanses of the canvas.
- **Content Blocks:** `surface-container` (#f0eee9) — For secondary content areas.
- **High-Interaction Cards:** `surface-container-lowest` (#ffffff) — Use pure white to make interactive cards appear to "lift" naturally from the warm rice-paper background.

### Signature Accents
- **Primary (`#46533b`):** Use for meaningful brand moments and primary CTAs.
- **Secondary (`#715b37` - Brushed Brass):** Use sparingly for "Gold Thread" moments—small icons, curated labels, or decorative underlines.
- **No Gradients/Glass:** Per the brand vision, avoid all digital-native effects like glassmorphism. Visual soul must come from the interplay of matte textures and flat, sophisticated tonal shifts.

---

## 3. Typography
Typography is the voice of this system. It balances the "Old World" authority of the serif with the "New World" clarity of the sans-serif.

| Level | Token | Font Family | Size | Character |
| :--- | :--- | :--- | :--- | :--- |
| **Display** | `display-lg` | Noto Serif | 3.5rem | Elegant, wide tracking (-2%), editorial. |
| **Headline** | `headline-md` | Noto Serif | 1.75rem | Authoritative, artisan-focused. |
| **Title** | `title-lg` | Manrope | 1.375rem | Modern, clean, approachable. |
| **Body** | `body-lg` | Manrope | 1rem | High legibility, generous line height (1.6). |
| **Label** | `label-md` | Manrope | 0.75rem | All-caps, slightly tracked out (+5%) for secondary info. |

**Editorial Tension:** Always pair a `display-lg` serif headline with a `body-md` sans-serif subline. The contrast in scale creates the "premium" feel.

---

## 4. Elevation & Depth
In this system, depth is felt, not seen. We avoid the "floating in space" look of traditional Material Design.

- **Tonal Layering:** Depth is achieved by "stacking." A `surface-container-lowest` card sitting on a `surface-container` background creates a soft, natural lift.
- **Ambient Shadows:** Shadows are a last resort. When used, they must be "Atmospheric":
    - **Blur:** 40px - 60px.
    - **Opacity:** 4% - 6%.
    - **Color:** Use a tinted neutral (`#1b1c19` at 5% opacity) to mimic natural light on paper.
- **The "Ghost Border" Fallback:** If a container requires definition against a similar background, use the `outline-variant` (#c5c8bd) at **15% opacity**. It should be felt as a whisper of an edge, never a hard line.

---

## 5. Components

### Buttons: The "Quiet Action"
- **Primary:** Filled `primary` (#46533b) with `on-primary` (#ffffff) text. Radius: `md` (0.375rem). No shadows.
- **Secondary:** Outlined with a "Ghost Border" (15% opacity `outline`). 
- **Tertiary:** Text-only in `primary` with a subtle `secondary` (Brass) 1px underline that appears on hover.

### Cards: The "Artisan Tray"
- **Style:** Forbid the use of divider lines. 
- **Separation:** Use a `0.375rem` (md) radius. Background should be `surface-container-lowest` (#ffffff) to stand out against the warmer rice-paper `surface`. 
- **Imagery:** Utilize subtle image masking (e.g., a slight arch or organic rounded corner on one side) to break the "web-standard" rectangular feel.

### Input Fields: "Minimalist Ink"
- **Style:** No box. Only a bottom border using `outline-variant` (#c5c8bd).
- **Focus State:** The bottom border transitions to `secondary` (Brushed Brass) with a 2px weight.

### Chips & Tags
- **Style:** Pill-shaped (`full` radius). 
- **Color:** Background `surface-container-high` (#eae8e3) with `on-surface-variant` text. Avoid high-contrast tags; they should feel integrated into the background.

---

## 6. Do’s and Don’ts

### Do
- **Do** use asymmetrical layouts (e.g., a text block offset to the left with an image bleeding off the right edge).
- **Do** use "Matcha-Cream" (`#F2F4EF`) as a soft background toggle to break up long scrolling pages of "Rice-Paper" (`#F9F7F2`).
- **Do** prioritize large, high-resolution photography of ingredients and textures.

### Don’t
- **Don't** use SaaS-style "Card Grids" with 3-4 columns of identical boxes. Vary the size and rhythm of content.
- **Don't** use pure black (#000000) for text. Always use the Near-Black (`#1A1A1A`) to maintain warmth.
- **Don't** use flashy transitions. Motion should be slow, "weighted" fades or subtle vertical slides (easing: `cubic-bezier(0.2, 0, 0, 1)`).
- **Don't** use icons for everything. Sometimes a well-placed, elegant `label-md` word is more premium than a generic glyph.