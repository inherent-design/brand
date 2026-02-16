# Styles

Design tokens and theme integration for inherent.design web surfaces.

## Quick Reference

| File | Role |
|---|---|
| `styles.css` | Brand tokens as CSS custom properties (`--brand-*`), `@layer base` element and semantic role styles |
| `starwind.css` | Starwind UI / Tailwind CSS v4 theme bridge; maps brand tokens to framework semantics, defines light and dark mode |
| `../fonts/vars.css` | Font stack custom properties (`--brand-font-*`), consumed by both layers |

**Token namespace:** All brand tokens use the `--brand-*` prefix to avoid collision with framework theme variables.

**Color space:** oklch throughout, chosen for perceptual uniformity and wide gamut support.

**Package exports:**

```
@inherent.design/brand/styles       -> styles.css  (brand tokens only)
@inherent.design/brand/styles/starwind -> starwind.css (full Tailwind + Starwind theme)
```

## Architecture

The styles system is a two-layer pipeline:

```
fonts/vars.css          styles.css              starwind.css
(font stacks)  --->  (brand tokens +     --->  (Tailwind v4 theme bridge +
                      @layer base rules)        light/dark mode values)
                                                      |
                                                      v
                                              Tailwind utility classes
                                              (bg-primary, text-foreground, etc.)
```

1. **`styles.css`** declares the canonical brand values: colors, typography scale, spacing, layout constraints, and borders. It also defines `@layer base` rules that apply brand typography to HTML elements and semantic role classes.

2. **`starwind.css`** imports Tailwind CSS v4, tw-animate-css, and `@tailwindcss/forms`. It reads the `--brand-*` custom properties and maps them to Starwind semantic tokens (`--primary`, `--foreground`, `--muted`, etc.) that Tailwind utilities consume. It also defines all dark mode overrides.

Consumers import one or both layers depending on need. A static page that only needs brand typography can import `styles.css` alone. An interactive Astro/Starwind page imports `starwind.css`, which pulls in Tailwind and the full component theme.

## Brand Tokens (styles.css)

All tokens are declared on `:root` and namespaced with `--brand-*`.

### Colors

| Token | Value | Purpose |
|---|---|---|
| `--brand-text-dark` | `oklch(21.78% 0 0)` | Primary body text, near-black |
| `--brand-text-gray` | `oklch(55.10% 0.0234 264.4)` | Secondary text, muted labels |
| `--brand-accent` | `oklch(54.61% 0.2152 262.9)` | Primary accent (links, buttons, focus) |
| `--brand-accent-hover` | `oklch(47.73% 0.1944 264.6)` | Accent hover state, slightly darker |
| `--brand-code-bg` | `oklch(97.02% 0 0)` | Inline code background tint |

### Typography: Size

| Token | Value |
|---|---|
| `--brand-text-xs` | `0.75rem` |
| `--brand-text-sm` | `0.875rem` |
| `--brand-text-base` | `1.0625rem` |
| `--brand-text-lg` | `1.125rem` |
| `--brand-text-xl` | `1.25rem` |
| `--brand-text-2xl` | `1.5rem` |
| `--brand-text-3xl` | `1.875rem` |
| `--brand-text-4xl` | `2.25rem` |
| `--brand-text-5xl` | `3rem` |

The base size is `1.0625rem` (17px), slightly larger than the browser default for improved body text readability.

### Typography: Weight

| Token | Value |
|---|---|
| `--brand-weight-light` | `300` |
| `--brand-weight-normal` | `400` |
| `--brand-weight-medium` | `500` |
| `--brand-weight-semibold` | `600` |
| `--brand-weight-bold` | `700` |
| `--brand-weight-black` | `900` |

### Typography: Tracking (Letter Spacing)

| Token | Value | Use |
|---|---|---|
| `--brand-tracking-tight` | `-0.025em` | Headings, display type |
| `--brand-tracking-normal` | `0em` | Body text |
| `--brand-tracking-wide` | `0.025em` | Overlines, CTAs, uppercase text |

### Typography: Leading (Line Height)

| Token | Value | Use |
|---|---|---|
| `--brand-leading-tight` | `1.2` | Headings (h1, h2) |
| `--brand-leading-snug` | `1.375` | Sub-headings (h3, h4, h5, h6) |
| `--brand-leading-normal` | `1.5` | Captions, subtitles |
| `--brand-leading-relaxed` | `1.65` | Body text (p, li) |

### Spacing

| Token | Value |
|---|---|
| `--brand-spacing-xs` | `0.25rem` (4px) |
| `--brand-spacing-sm` | `0.5rem` (8px) |
| `--brand-spacing-md` | `1rem` (16px) |
| `--brand-spacing-lg` | `1.5rem` (24px) |
| `--brand-spacing-xl` | `2rem` (32px) |
| `--brand-spacing-2xl` | `3rem` (48px) |

### Layout

| Token | Value | Purpose |
|---|---|---|
| `--brand-max-width-content` | `42rem` | Prose column (optimal reading width) |
| `--brand-max-width-page` | `64rem` | Outer page container |

### Borders

| Token | Value |
|---|---|
| `--brand-border-rule` | `0.5px solid color-mix(in oklch, var(--brand-text-gray) 40%, transparent)` |
| `--brand-border-code` | `0.5px solid var(--brand-text-gray)` |
| `--brand-radius-code` | `4px` |

`--brand-border-rule` uses `color-mix` to create a 40% opacity rule line without introducing a separate color token.

## Base Layer Rules (styles.css)

The `@layer base` block in styles.css applies brand typography to HTML elements and defines semantic role classes.

### HTML Elements

| Element | Size | Weight | Tracking | Leading |
|---|---|---|---|---|
| `h1` | `--brand-text-3xl` | bold (700) | tight | tight (1.2) |
| `h2` | `--brand-text-xl` | semibold (600) | (default) | tight (1.2) |
| `h3` | `--brand-text-lg` | semibold (600) | (default) | snug (1.375) |
| `h4` | `--brand-text-base` | semibold (600) | (default) | snug (1.375) |
| `h5`, `h6` | `--brand-text-sm` | medium (500) | (default) | snug (1.375) |
| `body` | `--brand-text-base` | normal (400) | (default) | (default) |
| `p`, `li` | (inherited) | (inherited) | (default) | relaxed (1.65) |
| `small` | `--brand-text-sm` | (inherited) | (default) | (inherited) |
| `code` | `--brand-text-sm` | (inherited) | (default) | (inherited) |

### Semantic Roles

| Class | Font | Size | Weight | Tracking | Leading | Extra |
|---|---|---|---|---|---|---|
| `.site-title` | display | `5xl` | black (900) | tight | tight | |
| `.site-subtitle` | (inherited) | base | (inherited) | (default) | normal | |
| `.nav-text` | (inherited) | sm | medium (500) | (default) | (default) | |
| `.cta` | (inherited) | (inherited) | black (900) | wide | (default) | |
| `.caption` | (inherited) | xs | (inherited) | (default) | normal | |
| `.overline` | (inherited) | xs | semibold (600) | wide | (default) | `text-transform: uppercase` |
| `.label` | (inherited) | sm | medium (500) | (default) | (default) | |

## Starwind Theme Bridge (starwind.css)

starwind.css maps brand tokens to Starwind semantic variables, which Tailwind CSS v4 then exposes as utility classes.

### Imports

```css
@import "tailwindcss";
@import "tw-animate-css";
@plugin "@tailwindcss/forms";
```

The dark mode variant is configured as a class strategy:

```css
@custom-variant dark (&:where(.dark, .dark *));
```

### Color Mapping (Light Mode)

| Brand Token | Starwind Variable | Tailwind Utility | Light Value |
|---|---|---|---|
| `--brand-text-dark` | `--foreground` | `text-foreground` | `oklch(21.78% 0 0)` |
| `--brand-text-dark` | `--card-foreground` | `text-card-foreground` | `oklch(21.78% 0 0)` |
| `--brand-text-dark` | `--popover-foreground` | `text-popover-foreground` | `oklch(21.78% 0 0)` |
| `--brand-text-dark` | `--accent-foreground` | `text-accent-foreground` | `oklch(21.78% 0 0)` |
| `--brand-accent` | `--primary` | `bg-primary` | `oklch(54.61% 0.2152 262.9)` |
| `--brand-accent-hover` | `--primary-accent` | `bg-primary-accent` | `oklch(47.73% 0.1944 264.6)` |
| `--brand-text-gray` | `--secondary` | `bg-secondary` | `oklch(55.10% 0.0234 264.4)` |
| `--brand-text-gray` | `--secondary-accent` | `bg-secondary-accent` | `oklch(55.10% 0.0234 264.4)` |
| `--brand-text-gray` | `--muted-foreground` | `text-muted-foreground` | `oklch(55.10% 0.0234 264.4)` |
| `--brand-text-gray` | `--outline` | `outline-outline` | `oklch(55.10% 0.0234 264.4)` |
| (literal) | `--background` | `bg-background` | `oklch(100% 0 0)` |
| (literal) | `--card` | `bg-card` | `oklch(100% 0 0)` |
| (literal) | `--popover` | `bg-popover` | `oklch(100% 0 0)` |
| (literal) | `--primary-foreground` | `text-primary-foreground` | `oklch(100% 0 0)` |
| (literal) | `--secondary-foreground` | `text-secondary-foreground` | `oklch(100% 0 0)` |
| (literal) | `--muted` | `bg-muted` | `oklch(97% 0 0)` |
| (literal) | `--accent` | `bg-accent` | `oklch(97% 0 0)` |
| (computed) | `--border` | `border-border` | `color-mix(in oklch, --brand-text-gray 30%, transparent)` |
| (computed) | `--input` | `border-input` | `color-mix(in oklch, --brand-text-gray 30%, transparent)` |
| (literal) | `--radius` | `rounded-*` | `0.5rem` |

### Semantic Status Colors

These are defined with literal oklch values in both light and dark modes.

| Variable | Tailwind Utility | Light Value | Dark Value |
|---|---|---|---|
| `--info` | `bg-info` | `oklch(78% 0.12 222)` | `oklch(78% 0.12 222)` |
| `--info-foreground` | `text-info-foreground` | `oklch(17% 0.04 251)` | `oklch(17% 0.04 251)` |
| `--success` | `bg-success` | `oklch(80% 0.16 153)` | `oklch(80% 0.16 153)` |
| `--success-foreground` | `text-success-foreground` | `oklch(19% 0.04 161)` | `oklch(19% 0.04 161)` |
| `--warning` | `bg-warning` | `oklch(83% 0.15 86)` | `oklch(83% 0.15 86)` |
| `--warning-foreground` | `text-warning-foreground` | `oklch(22% 0.05 71)` | `oklch(22% 0.05 71)` |
| `--error` | `bg-error` | `oklch(50% 0.20 27)` | `oklch(45% 0.20 27)` |
| `--error-foreground` | `text-error-foreground` | `oklch(98.51% 0 0)` | `oklch(98.51% 0 0)` |

Note: The semantic status colors (info, success, warning) share values between light and dark modes. Only `--error` shifts slightly darker in dark mode (`50%` to `45%` lightness).

### Radius Scale

The `@theme inline` block exposes a radius scale derived from the base `--radius` (0.5rem):

| Theme Variable | Computation | Resolved Value |
|---|---|---|
| `--radius-xs` | `--radius - 0.375rem` | `0.125rem` |
| `--radius-sm` | `--radius - 0.25rem` | `0.25rem` |
| `--radius-md` | `--radius - 0.125rem` | `0.375rem` |
| `--radius-lg` | `--radius` | `0.5rem` |
| `--radius-xl` | `--radius + 0.25rem` | `0.75rem` |
| `--radius-2xl` | `--radius + 0.5rem` | `1rem` |
| `--radius-3xl` | `--radius + 1rem` | `1.5rem` |

### Font Integration

starwind.css maps `--brand-font-*` properties (defined in `fonts/vars.css`) to Tailwind font theme variables:

| Brand Property | Tailwind Variable | Tailwind Utility | Stacks (English) |
|---|---|---|---|
| `--brand-font-serif` | `--font-body` | `font-body` | Charter, Georgia, serif |
| `--brand-font-display` | `--font-display` | `font-display` | Cormorant Garamond, Charter, Georgia, serif |
| `--brand-font-sans` | `--font-sans` | `font-sans` | Inter, system-ui, sans-serif |
| `--brand-font-mono` | `--font-mono` | `font-mono` | Commit Mono, monospace |

`fonts/vars.css` provides locale-aware stacks: `:root` (universal fallback), `:root:lang(en)`, `:root:lang(zh)`, and `:root:lang(hi)` each declare appropriate typefaces for their script.

### Sidebar Variables

Starwind sidebar components read dedicated variables. These parallel the core theme but allow independent sidebar styling.

| Variable | Light Value | Dark Value |
|---|---|---|
| `--sidebar-background` | `oklch(98.51% 0 0)` | `oklch(19% 0 0)` |
| `--sidebar-foreground` | `var(--brand-text-dark)` | `oklch(98.51% 0 0)` |
| `--sidebar-primary` | `var(--brand-accent)` | `var(--brand-accent)` |
| `--sidebar-primary-foreground` | `oklch(100% 0 0)` | `oklch(98.51% 0 0)` |
| `--sidebar-accent` | `oklch(97% 0 0)` | `oklch(25% 0 0)` |
| `--sidebar-accent-foreground` | `var(--brand-text-dark)` | `oklch(95% 0 0)` |
| `--sidebar-border` | `color-mix(...)` | `oklch(25% 0 0)` |
| `--sidebar-outline` | `var(--brand-text-gray)` | `oklch(45% 0 0)` |

## Dark Mode

Dark mode is activated by adding the `.dark` class to an ancestor element. The `@custom-variant dark` directive in starwind.css scopes all dark overrides to `.dark` and its descendants.

### All Dark Mode Overrides

| Variable | Light | Dark |
|---|---|---|
| `--background` | `oklch(100% 0 0)` | `oklch(15% 0 0)` |
| `--foreground` | `var(--brand-text-dark)` | `oklch(98.51% 0 0)` |
| `--card` | `oklch(100% 0 0)` | `oklch(19% 0 0)` |
| `--card-foreground` | `var(--brand-text-dark)` | `oklch(98.51% 0 0)` |
| `--popover` | `oklch(100% 0 0)` | `oklch(22% 0 0)` |
| `--popover-foreground` | `var(--brand-text-dark)` | `oklch(98.51% 0 0)` |
| `--primary` | `var(--brand-accent)` | `var(--brand-accent)` |
| `--primary-foreground` | `oklch(100% 0 0)` | `oklch(98.51% 0 0)` |
| `--primary-accent` | `var(--brand-accent-hover)` | `oklch(62% 0.22 263)` |
| `--secondary` | `var(--brand-text-gray)` | `var(--brand-text-gray)` |
| `--secondary-foreground` | `oklch(100% 0 0)` | `oklch(98.51% 0 0)` |
| `--secondary-accent` | `var(--brand-text-gray)` | `oklch(65% 0.02 264)` |
| `--muted` | `oklch(97% 0 0)` | `oklch(25% 0 0)` |
| `--muted-foreground` | `var(--brand-text-gray)` | `oklch(55% 0 0)` |
| `--accent` | `oklch(97% 0 0)` | `oklch(30% 0 0)` |
| `--accent-foreground` | `var(--brand-text-dark)` | `oklch(95% 0 0)` |
| `--error` | `oklch(50% 0.20 27)` | `oklch(45% 0.20 27)` |
| `--border` | `color-mix(...)` | `oklch(30% 0 0)` |
| `--input` | `color-mix(...)` | `oklch(32% 0 0)` |
| `--outline` | `var(--brand-text-gray)` | `oklch(50% 0 0)` |

The `@layer base` in starwind.css applies `scheme-light` and `dark:scheme-dark` to `<body>`, ensuring native form controls and scrollbars follow the active mode.

### Design Decisions

Several tokens are intentionally shared between modes:

- `--primary` stays `var(--brand-accent)` in both modes, preserving brand identity.
- `--secondary` stays `var(--brand-text-gray)` in both modes.
- Semantic status colors (info, success, warning) are mode-invariant; only `--error` adjusts lightness slightly.
- Dark mode foreground values use `oklch(98.51% 0 0)` (not pure white) to reduce eye strain.

## Animations

starwind.css defines two accordion animations via `@theme`:

| Animation | Variable | Duration | Easing |
|---|---|---|---|
| `accordion-down` | `--animate-accordion-down` | 0.2s | ease-out |
| `accordion-up` | `--animate-accordion-up` | 0.2s | ease-out |

Both animations interpolate height between `0` and `var(--starwind-accordion-content-height)`, which Starwind accordion components set at runtime.

### Global Base Rules

The starwind.css `@layer base` applies three global defaults:

- All elements: `border-border outline-outline/50` (consistent border and 50% opacity outline)
- `body`: `bg-background text-foreground scheme-light dark:scheme-dark`
- `button`: `cursor-pointer`

## Integration

### Package Exports

Import via the `@inherent.design/brand` package:

```css
@import "@inherent.design/brand/styles";
```

For Starwind UI / Tailwind projects:

```css
@import "@inherent.design/brand/styles/starwind";
```

### Load Order in Astro

When using both layers, import styles.css before starwind.css. The brand tokens must be defined before the theme bridge reads them:

```astro
---
import "@inherent.design/brand/fonts/en";
import "@inherent.design/brand/fonts/vars";
import "@inherent.design/brand/styles";
import "@inherent.design/brand/styles/starwind";
---
```

Fonts load first (face declarations), then font variable assignments, then brand tokens, then the Starwind theme that references everything above.

### Standalone Usage

For pages that do not need Tailwind or Starwind components, import only the brand tokens and font variables:

```css
@import "@inherent.design/brand/fonts/vars";
@import "@inherent.design/brand/styles";
```

This gives you `--brand-*` custom properties and the `@layer base` typography rules without any framework overhead.

## Adding New Tokens

To introduce a new design token:

1. **Define in styles.css:** Add the custom property under `:root` with the `--brand-*` prefix.

2. **Bridge in starwind.css (if needed):** If the token should be available as a Tailwind utility, add a mapping in the `@theme inline` block (e.g., `--color-my-token: var(--my-token)`) and define values in both `:root` and `.dark`.

3. **Consume via Tailwind:** The new token becomes available as a utility class (e.g., `bg-my-token`, `text-my-token`).

4. **Update Typst tokens (if applicable):** If the token affects the shared design language, add the corresponding value to the Typst layer (see below).

## Relationship to Typst Tokens

`styles.css` and the Typst files `typst/lib/colors.typ` and `typst/lib/tokens.typ` define the same design language for different output media. CSS targets screens; Typst targets print (PDF).

Key correspondences:

| CSS Token | Typst Variable | Notes |
|---|---|---|
| `--brand-text-dark` | `text-dark` | CSS uses oklch; Typst uses sRGB hex approximation |
| `--brand-text-gray` | `text-gray` | Same conceptual value, different color space |
| `--brand-accent` | `accent` | Same conceptual value, different color space |
| `--brand-tracking-tight` | `trk-tight` | Identical value (`-0.025em`) |
| `--brand-tracking-wide` | `trk-wide` | Identical value (`0.025em`) |
| `--brand-leading-tight` | `ld-tight` | CSS `1.2` corresponds to Typst `0.2em` paragraph leading |
| `--brand-spacing-*` | `sp-*` | Print uses tighter spacing; values differ intentionally |

When CSS tokens change, Typst tokens should be reviewed and updated to maintain visual consistency across web and print. The spacing scale diverges intentionally because print density requires tighter vertical rhythm than screen rendering.
