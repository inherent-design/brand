# Components

Branded Astro components built on Starwind UI and Tailwind Variants, providing a consistent design language across all inherent.design web projects.

## Quick Reference

| Component | Category | Variants | Sizes | Import Path |
|-----------|----------|----------|-------|-------------|
| Button | Interactive | 8 (default, primary, secondary, outline, ghost, info, success, warning, error) | 6 (sm, md, lg, icon-sm, icon, icon-lg) | `@inherent.design/brand/components/button` |
| Prose | Typography | None | Controlled via CSS custom properties | `@inherent.design/brand/components/prose` |
| Image | Media | None | Responsive (full width, auto height) | `@inherent.design/brand/components/image` |
| Separator | Layout | orientation (horizontal, vertical) | Determined by orientation | `@inherent.design/brand/components/separator` |

## Architecture

Every component follows the same structural pattern.

**Astro + Tailwind Variants**: Each `.astro` file defines its variant schema using `tv()` from `tailwind-variants`. The `tv()` call is exported as a named constant so consuming projects can access the raw variant function if needed.

**Slot-based composition**: Components use Astro's `<slot />` for content projection. Button, for example, renders its children inside either an `<a>` or `<button>` tag depending on props.

**Barrel exports**: Each component directory contains an `index.ts` that re-exports the component as both a default and named export, along with a `*Variants` object containing the raw `tv()` function.

```
components/
  button/
    Button.astro
    index.ts
  image/
    Image.astro
    index.ts
  prose/
    Prose.astro
    index.ts
  separator/
    Separator.astro
    index.ts
```

**Data attributes**: All components set a `data-slot` attribute (e.g., `data-slot="button"`) for styling hooks and testing selectors.

## Button

A polymorphic interactive element that renders as `<a>` when an `href` prop is present and `<button>` otherwise.

### Props

```ts
interface Props extends HTMLAttributes<"button">, Omit<HTMLAttributes<"a">, "type">, VariantProps<typeof button> {}
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `variant` | `"default" \| "primary" \| "secondary" \| "outline" \| "ghost" \| "info" \| "success" \| "warning" \| "error"` | `"default"` | Visual style of the button |
| `size` | `"sm" \| "md" \| "lg" \| "icon-sm" \| "icon" \| "icon-lg"` | `"md"` | Size preset |
| `href` | `string` | `undefined` | When provided, renders as `<a>` instead of `<button>` |
| `class` | `string` | `undefined` | Additional CSS classes merged via Tailwind Variants |

All standard HTML button and anchor attributes are forwarded.

### Variants

| Variant | Background | Text | Hover | Use Case |
|---------|-----------|------|-------|----------|
| `default` | foreground | background | foreground/90 | Standard actions |
| `primary` | primary | primary-foreground | primary-accent | Primary CTAs |
| `secondary` | secondary | secondary-foreground | secondary/90 | Secondary actions |
| `outline` | background (with border) | foreground | muted | Form controls, toggles |
| `ghost` | transparent | foreground | muted | Toolbar actions, minimal UI |
| `info` | info | info-foreground | info/90 | Informational actions |
| `success` | success | success-foreground | success/90 | Confirmations, completions |
| `warning` | warning | warning-foreground | warning/90 | Caution-required actions |
| `error` | error | error-foreground | error/90 | Destructive or critical actions |

All variants include a focus-visible ring using the variant's color at 50% opacity. The `aria-invalid` state triggers error styling on any variant.

### Sizes

| Size | Height | Padding | SVG Size | Purpose |
|------|--------|---------|----------|---------|
| `sm` | h-9 | px-4 | 3.5 | Compact UI, dense layouts |
| `md` | h-11 | px-5 | 4.5 | Default, general use |
| `lg` | h-12 | px-8 | 5 | Hero sections, prominent actions |
| `icon-sm` | 9x9 | None | 3.5 | Small icon-only buttons |
| `icon` | 11x11 | None | 4.5 | Standard icon-only buttons |
| `icon-lg` | 12x12 | None | 5 | Large icon-only buttons |

Icon sizes automatically reduce horizontal padding when the button contains an SVG child, using the `has-[>svg]` selector.

### Usage

```astro
---
import { Button } from "@inherent.design/brand/components/button";
---

<Button>Default Action</Button>
<Button variant="primary" size="lg">Get Started</Button>
<Button variant="outline" size="sm">Cancel</Button>
<Button variant="ghost" size="icon"><SearchIcon /></Button>
<Button href="/docs" variant="primary">Read the Docs</Button>
```

## Prose

A typography wrapper that applies consistent styles to rendered markdown and HTML content. Wraps content in a `<div>` with the `.sw-prose` class, which provides global styles for headings, paragraphs, links, lists, tables, code blocks, blockquotes, and more.

All sizing is em-based, so the entire typographic scale adjusts when you change the inherited font size via Tailwind utilities like `text-sm` or `md:text-base`.

### Props

```ts
type Props = HTMLAttributes<"div">;
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `class` | `string` | `undefined` | Additional CSS classes; merged via Tailwind Variants |

The base class constrains content width to `max-w-[65ch]` for optimal reading line length.

### CSS Custom Properties Reference

Override any property inline or on a parent element. All accept standard CSS values.

#### Typography and Spacing

| Custom Property | Internal Variable | Default |
|-----------------|-------------------|---------|
| `--prose-line-height` | `--sw-prose-line-height` | `1.6` |
| `--prose-spacing` | `--sw-prose-spacing` | `1.25em` |
| `--prose-heading-spacing` | `--sw-prose-heading-spacing` | `1.5em` |
| `--prose-code-size` | `--sw-prose-code-size` | `0.875em` |
| `--prose-list-indent` | `--sw-prose-list-indent` | `1.625em` |

#### Colors

| Custom Property | Internal Variable | Default |
|-----------------|-------------------|---------|
| `--prose-color` | `--sw-prose-color` | `foreground / 80%` |
| `--prose-heading-color` | `--sw-prose-heading-color` | `foreground` |
| `--prose-list-marker-color` | `--sw-prose-list-marker-color` | `muted-foreground` |

#### Headings

| Custom Property | Internal Variable | Default |
|-----------------|-------------------|---------|
| `--prose-heading-font` | `--sw-prose-heading-font` | `var(--font-heading, inherit)` |
| `--prose-heading-weight` | `--sw-prose-heading-weight` | `600` |
| `--prose-heading-line-height` | `--sw-prose-heading-line-height` | `1.25` |
| `--prose-h1-size` | `--sw-prose-h1-size` | `2.25em` |
| `--prose-h1-weight` | `--sw-prose-h1-weight` | heading-weight |
| `--prose-h2-size` | `--sw-prose-h2-size` | `1.5em` |
| `--prose-h2-weight` | `--sw-prose-h2-weight` | heading-weight |
| `--prose-h3-size` | `--sw-prose-h3-size` | `1.25em` |
| `--prose-h3-weight` | `--sw-prose-h3-weight` | heading-weight |
| `--prose-h4-size` | `--sw-prose-h4-size` | `1em` |
| `--prose-h4-weight` | `--sw-prose-h4-weight` | heading-weight |

#### Links

| Custom Property | Internal Variable | Default |
|-----------------|-------------------|---------|
| `--prose-link-color` | `--sw-prose-link-color` | `foreground` |
| `--prose-link-decoration-color` | `--sw-prose-link-decoration-color` | `primary-accent` |
| `--prose-link-hover-color` | `--sw-prose-link-hover-color` | `primary-accent` |

#### Strong and Bold

| Custom Property | Internal Variable | Default |
|-----------------|-------------------|---------|
| `--prose-strong-color` | `--sw-prose-strong-color` | `foreground` |
| `--prose-strong-weight` | `--sw-prose-strong-weight` | `600` |

#### Blockquotes

| Custom Property | Internal Variable | Default |
|-----------------|-------------------|---------|
| `--prose-blockquote-color` | `--sw-prose-blockquote-color` | `foreground` |
| `--prose-blockquote-border-color` | `--sw-prose-blockquote-border-color` | `border` |
| `--prose-blockquote-border-width` | `--sw-prose-blockquote-border-width` | `4px` |

#### Inline Code

| Custom Property | Internal Variable | Default |
|-----------------|-------------------|---------|
| `--prose-code-bg` | `--sw-prose-code-bg` | `muted` |
| `--prose-code-color` | `--sw-prose-code-color` | `foreground` |
| `--prose-code-weight` | `--sw-prose-code-weight` | `500` |
| `--prose-code-radius` | `--sw-prose-code-radius` | `radius-sm` |

#### Code Blocks (Pre)

| Custom Property | Internal Variable | Default |
|-----------------|-------------------|---------|
| `--prose-pre-border-color` | `--sw-prose-pre-border-color` | `border` |
| `--prose-pre-border-radius` | `--sw-prose-pre-border-radius` | `radius-md` |

#### Tables

| Custom Property | Internal Variable | Default |
|-----------------|-------------------|---------|
| `--prose-table-heading-color` | `--sw-prose-table-heading-color` | `foreground` |
| `--prose-table-border-color` | `--sw-prose-table-border-color` | `border` |

#### Media (Images, Video)

| Custom Property | Internal Variable | Default |
|-----------------|-------------------|---------|
| `--prose-media-border-width` | `--sw-prose-media-border-width` | `0px` |
| `--prose-media-border-color` | `--sw-prose-media-border-color` | `border` |
| `--prose-media-border-radius` | `--sw-prose-media-border-radius` | `0` |

#### Highlight (Mark)

| Custom Property | Internal Variable | Default |
|-----------------|-------------------|---------|
| `--prose-highlight-color` | `--sw-prose-highlight-color` | `foreground` |
| `--prose-highlight-bg-color` | `--sw-prose-highlight-bg-color` | `warning / 30%` |

### Styled Elements

Prose applies styles to the following elements when they appear inside the `.sw-prose` container:

- **Headings** (h1 through h6): Sized via custom properties, with configurable font family, weight, and line height. Headings that follow non-heading content receive extra top spacing.
- **Paragraphs**: Vertical spacing controlled by `--prose-spacing`.
- **Links**: Underlined with configurable decoration color, smooth color transition on hover.
- **Strong/Bold**: Inherits color from context (links, blockquotes, table headers) or uses `--prose-strong-color`.
- **Lists** (ul, ol, dl): Indented via `--prose-list-indent`. Marker colors are muted. Nested lists receive reduced spacing. Definition lists (`dl/dt/dd`) are supported.
- **Blockquotes**: Italic with a left border. Opening and closing quotation marks are injected via CSS `::before` and `::after` pseudo-elements.
- **Inline code**: Background-highlighted with configurable padding and border radius. Inside headings, code inherits the heading's font size.
- **Code blocks** (pre): Bordered with configurable radius, horizontal overflow scrolling, and `tab-size: 2`. Inner `code` elements have all styles reset.
- **Horizontal rules**: Full-width with `3em` vertical margin.
- **Images and media**: Block-level, responsive (`max-width: 100%`), with optional borders and border radius.
- **Figures and captions**: Captions use muted color and smaller font size.
- **Tables**: Full-width auto layout, bordered rows, styled headers. Font size matches code size.
- **Keyboard input** (kbd): Inline-flex with muted background, sized to match code.
- **Details/Summary**: Left border that highlights on hover, animated chevron marker, Starlight-inspired styling.
- **Abbreviations**: Dotted underline with help cursor.
- **Mark/Highlight**: Warning-tinted background with rounded corners.
- **Subscript/Superscript**: 0.75em font size.

### Opting Out

Add the `not-sw-prose` class to any element within the Prose container to exclude it (and its children) from prose styling.

### Usage

```astro
---
import { Prose } from "@inherent.design/brand/components/prose";
---

<Prose>
  <h1>Article Title</h1>
  <p>Body text with a <a href="#">link</a> and <code>inline code</code>.</p>
</Prose>

<Prose class="text-sm md:text-base [--prose-h1-size:3em]">
  <slot />
</Prose>

<Prose>
  <p>Styled content here.</p>
  <div class="not-sw-prose">
    <CustomWidget />
  </div>
</Prose>
```

### Responsive Overrides

Because all sizing is em-based, use Tailwind's responsive text utilities on the Prose component to scale the entire typographic system. For finer control, override individual custom properties with Tailwind's arbitrary property syntax:

```astro
<Prose class="text-sm md:text-base lg:text-lg [--prose-spacing:1.5em] md:[--prose-spacing:1.25em]">
  <slot />
</Prose>
```

## Image

A thin wrapper around Astro's built-in `<Image>` component from `astro:assets`, adding consistent styling and sensible defaults.

### Props

```ts
type Props = Partial<ComponentProps<typeof AstroImage>> & { inferSize?: boolean };
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `src` | `ImageMetadata \| string` | Required | Image source (local import or remote URL) |
| `alt` | `string` | `""` | Alt text for accessibility |
| `inferSize` | `boolean` | `true` | Automatically infer width and height for remote images |
| `class` | `string` | `undefined` | Additional CSS classes |

The component only renders when `src` is provided. Base styles apply `w-full h-auto` for responsive behavior.

### Usage

```astro
---
import { Image } from "@inherent.design/brand/components/image";
import heroImage from "../assets/hero.png";
---

<Image src={heroImage} alt="Hero banner" />
<Image src="https://example.com/photo.jpg" alt="Remote photo" />
<Image src={heroImage} alt="Styled image" class="rounded-lg shadow-md" />
```

## Separator

An accessible divider element that renders a thin line, either horizontally or vertically.

### Props

```ts
type Props = Omit<HTMLAttributes<"div">, "role" | "aria-orientation"> & {
  orientation?: "horizontal" | "vertical";
};
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `orientation` | `"horizontal" \| "vertical"` | `"horizontal"` | Direction of the separator |
| `class` | `string` | `undefined` | Additional CSS classes |

The component sets `role="separator"` and `aria-orientation` automatically. Horizontal separators are `h-[1px] w-full`; vertical separators are `h-full w-[1px]`.

### Usage

```astro
---
import { Separator } from "@inherent.design/brand/components/separator";
---

<Separator />
<Separator orientation="vertical" class="mx-4" />
```

## Integration

### Importing in Astro Projects

Components are published under `@inherent.design/brand` and imported directly from their subpath exports:

```astro
---
import { Button } from "@inherent.design/brand/components/button";
import { Prose } from "@inherent.design/brand/components/prose";
import { Image } from "@inherent.design/brand/components/image";
import { Separator } from "@inherent.design/brand/components/separator";
---
```

### Starwind CSS Dependency

All components require the Starwind CSS foundation, which provides the design token layer (color semantics, radius, spacing) and Tailwind configuration. Import it in your project's CSS entrypoint or layout:

```css
@import "@inherent.design/brand/styles/starwind";
```

This file configures Tailwind CSS, sets up the theme token mappings, and provides animation utilities that components depend on.

### Accessing Variant Functions

Each component exports its raw `tv()` variant function for programmatic use (conditional class generation, server-side rendering):

```ts
import { ButtonVariants } from "@inherent.design/brand/components/button";

const classes = ButtonVariants.button({ variant: "primary", size: "lg" });
```

## Pattern Library Roadmap

These components form the beginning of a branded pattern library. The vision is to mirror additional Starwind UI components into this library, applying the inherent.design token layer to each one.

Candidates for the next components to add:

| Priority | Component | Rationale |
|----------|-----------|-----------|
| High | Card | Common layout primitive for content grouping |
| High | Input / TextField | Form controls needed for any interactive page |
| High | Badge | Status indicators, tags, labels |
| Medium | Dialog / Modal | Overlays for confirmations and detail views |
| Medium | Tabs | Content organization in documentation and dashboards |
| Medium | Tooltip | Contextual help and label expansion |
| Lower | Accordion | Collapsible content sections |
| Lower | Dropdown Menu | Navigation and action menus |

Each new component should follow the established pattern (see below) and integrate with the same Starwind CSS token layer.

## Adding a New Component

Follow this process to add a component that matches the existing architecture:

1. **Create the directory** under `components/` using the component name in lowercase:

```
components/card/
```

2. **Create the `.astro` file** with a `tv()` variant definition and exported constant:

```astro
---
import type { HTMLAttributes } from "astro/types";
import { tv, type VariantProps } from "tailwind-variants";

export const card = tv({
  base: "rounded-lg border bg-card text-card-foreground shadow-sm",
  variants: {},
  defaultVariants: {},
});

interface Props extends HTMLAttributes<"div">, VariantProps<typeof card> {}

const { class: className, ...rest } = Astro.props;
---

<div class={card({ class: className })} data-slot="card" {...rest}>
  <slot />
</div>
```

3. **Create `index.ts`** as a barrel export:

```ts
import Card, { card } from "./Card.astro";

const CardVariants = { card };

export { Card, CardVariants };

export default Card;
```

4. **Register in `package.json`** under the `exports` field:

```json
"./components/card": "./components/card/index.ts"
```

5. **Verify** that the component renders correctly with `styles/starwind.css` loaded and that all variant props resolve to the expected Tailwind classes.

## Relationship to Typst Components

This `components/` directory contains the **web-facing** component library (Astro, Tailwind, browser rendering). A parallel set of **print-facing** components lives in `typst/lib/`:

| Concern | Web (this directory) | Print (`typst/lib/`) |
|---------|---------------------|----------------------|
| Runtime | Astro + Tailwind CSS | Typst compiler |
| Output | HTML/CSS in browsers | PDF documents |
| Styling | Tailwind Variants, CSS custom properties | Typst functions, show rules |
| Layout | Flexbox, Grid, responsive breakpoints | Typst page layout, measure units |
| Components | `components-*.typ` files: `components-layout.typ`, `components-content.typ`, `components-document.typ` | Same Typst component files |

Both layers share the same design language (colors, typography scale, spacing rhythm) but implement it for their respective medium. The web components reference CSS tokens from `styles/starwind.css`; the Typst components reference tokens from `typst/lib/tokens.typ` and `typst/lib/colors.typ`.

When updating the design language, changes should propagate to both layers to maintain visual consistency across web and print outputs.
