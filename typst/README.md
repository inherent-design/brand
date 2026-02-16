# @local/brand

Design tokens, components, and layout primitives for inherent.design Typst documents.

## Quick Reference

| Export | Module | Kind |
|---|---|---|
| `base-template` | `inherent.typ` | Show rule chain (typography, layout, tables, code) |
| `deep-merge`, `get`, `get-nested` | `lib/utils.typ` | Dictionary utilities |
| `text-dark`, `text-gray`, `accent`, `accent-light`, `accent-dark` | `lib/colors.typ` | Core color tokens |
| `success`, `warning`, `error`, `info` | `lib/colors.typ` | Semantic color tokens |
| `bg-subtle`, `bg-card`, `border` | `lib/colors.typ` | Surface and border tokens |
| `sp-0` .. `sp-7`, `sp-xs` .. `sp-3xl` | `lib/tokens.typ` | Spacing scale |
| `ts-tiny` .. `ts-display` | `lib/tokens.typ` | Type scale |
| `border-thin`, `border-medium`, `border-thick` | `lib/tokens.typ` | Border weights |
| `radius-sm`, `radius-md`, `radius-lg` | `lib/tokens.typ` | Border radii |
| `ld-tight`, `ld-snug`, `ld-normal`, `ld-relaxed` | `lib/tokens.typ` | Leading (line spacing) |
| `trk-tight`, `trk-normal`, `trk-wide` | `lib/tokens.typ` | Tracking (letter spacing) |
| `font-body`, `font-code`, `font-display`, `font-serif` | `lib/typography.typ` | Font stacks |
| `title-block`, `info-table`, `signature-block`, `separator` | `lib/components.typ` | Base components |
| `hero-section`, `two-column`, `sidebar-layout`, `card`, `card-grid` | `lib/components-layout.typ` | Layout components |
| `metric-card`, `service-card`, `competency-block`, `callout-box`, `pull-quote` | `lib/components-content.typ` | Content components |
| `info-box`, `warning-box`, `success-box`, `error-box`, `note-box`, `tip-box`, `important-box` | `lib/components-content.typ` | Callout presets |
| `cover-page`, `contact-strip`, `registration-block`, `invoice-header`, `line-items-table` | `lib/components-document.typ` | Document components |

## Package Manifest

From `typst.toml`:

```toml
[package]
name = "brand"
version = "0.4.1"
entrypoint = "prelude.typ"
authors = ["inherent.design"]
license = "Apache-2.0"
```

The entrypoint is `prelude.typ`, which re-exports everything consumers need.

## Architecture

### Module Structure

```
typst/
  typst.toml           Package manifest
  prelude.typ          Public entrypoint; re-exports all modules
  inherent.typ         Base template with show rule chain
  lib/
    colors.typ         Color tokens
    tokens.typ         Spacing, type scale, border, radius, leading, tracking
    typography.typ     Font stacks, heading styles, text rules
    layout.typ         Page setup, margins, header/footer
    tables.typ         Table stroke and fill rules
    code.typ           Code block and inline code styling
    utils.typ          Dictionary utilities (deep-merge, get, get-nested)
    components.typ     Barrel file; re-exports all component modules
    components-layout.typ    Layout primitives (hero, columns, cards)
    components-content.typ   Content blocks (metrics, callouts, quotes)
    components-document.typ  Document sections (cover, invoice, registration)
```

### Prelude Re-exports

`prelude.typ` is the single public surface. It re-exports:

```typst
#import "inherent.typ": base-template
#import "lib/utils.typ": deep-merge, get, get-nested
#import "lib/colors.typ": *
#import "lib/tokens.typ": *
#import "lib/typography.typ": *
#import "lib/components.typ": *
```

Consumers import everything through this one file. The `components.typ` barrel re-exports `components-layout.typ`, `components-content.typ`, and `components-document.typ` via glob imports.

### Show Rule Chain

`inherent.typ` defines `base-template`, which applies four show rules in sequence:

1. `apply-typography` (font stacks, heading styles, text defaults, list/link formatting)
2. `apply-layout` (page size, margins, header, footer)
3. `apply-tables` (stroke patterns, header row styling)
4. `apply-code` (code block background, inline code color)

Templates consume this via:

```typst
#show: base-template.with(title: "My Document", date: "2025-01-15")
```

## Base Template

```typst
#let base-template(
  title: "",
  date: none,
  body,
)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `title` | `string` | `""` | Document title, passed to layout header |
| `date` | `string` or `none` | `none` | Document date, shown in header when set |
| `body` | `content` | (required) | Document body content |

The template applies all four show rules. Individual templates can override specific rules after calling `base-template` by applying additional show rules.

## Color Tokens

### Core Colors

| Token | Hex | Purpose |
|---|---|---|
| `text-dark` | `#1a1a1a` | Primary text color |
| `text-gray` | `#6b7280` | Secondary text, captions, metadata |
| `accent` | `#2563eb` | Brand accent; headings, links, interactive elements |
| `accent-light` | (computed) | `accent.lighten(80%)`; subtle accent backgrounds |
| `accent-dark` | (computed) | `accent.darken(20%)`; hover states, emphasis |

### Semantic Colors

| Token | Hex | Purpose |
|---|---|---|
| `success` | `#2E7D32` | Positive states, confirmation |
| `warning` | `#F57F17` | Caution, attention required |
| `error` | `#C62828` | Error states, destructive actions |
| `info` | `#1565C0` | Informational highlights |

### Surface and Border

| Token | Hex | Purpose |
|---|---|---|
| `bg-subtle` | `#F8F9FA` | Subtle background fill (code blocks, cards) |
| `bg-card` | `#FFFFFF` | Card background |
| `border` | `#DEE2E6` | Default border color |

## Design Tokens

### Spacing Scale

4pt geometric base. Print uses tighter spacing than CSS (screen): `sp-md` = 12pt vs CSS 16px, `sp-lg` = 16pt vs CSS 24px. This is intentional for print density.

| Token | Value | Alias |
|---|---|---|
| `sp-0` | 0pt | |
| `sp-1` | 2pt | |
| `sp-2` | 4pt | `sp-xs` |
| `sp-3` | 8pt | `sp-sm` |
| `sp-4` | 12pt | `sp-md` |
| `sp-5` | 16pt | `sp-lg` |
| `sp-6` | 24pt | `sp-xl` |
| `sp-7` | 32pt | `sp-2xl` |
| (none) | 48pt | `sp-3xl` |

### Type Scale

| Token | Value | Use |
|---|---|---|
| `ts-tiny` | 7pt | Fine print |
| `ts-small` | 8pt | Header/footer text |
| `ts-caption` | 9pt | Captions, metadata |
| `ts-body` | 10pt | Body text default |
| `ts-h4` | 11pt | Level 4 headings |
| `ts-h3` | 13pt | Level 3 headings |
| `ts-h2` | 16pt | Level 2 headings |
| `ts-h1` | 22pt | Level 1 headings |
| `ts-display` | 28pt | Hero titles, cover pages |

### Border Weights

| Token | Value |
|---|---|
| `border-thin` | 0.5pt |
| `border-medium` | 1pt |
| `border-thick` | 2pt |

### Border Radii

| Token | Value |
|---|---|
| `radius-sm` | 2pt |
| `radius-md` | 4pt |
| `radius-lg` | 8pt |

### Leading

Typst `par.leading` corresponds to CSS `line-height - 1`.

| Token | Value | CSS Equivalent | Use |
|---|---|---|---|
| `ld-tight` | 0.2em | line-height: 1.2 | Headings |
| `ld-snug` | 0.375em | line-height: 1.375 | Sub-headings |
| `ld-normal` | 0.5em | line-height: 1.5 | General |
| `ld-relaxed` | 0.65em | line-height: 1.65 | Body text |

### Tracking

| Token | Value | Use |
|---|---|---|
| `trk-tight` | -0.025em | Headings |
| `trk-normal` | 0em | Body text |
| `trk-wide` | 0.025em | Labels, small caps |

## Typography

### Font Stacks

| Stack | Fonts | Use |
|---|---|---|
| `font-body` | Inter, Noto Sans SC, Noto Sans Devanagari | UI text, sans-serif body |
| `font-code` | Commit Mono, Noto Sans Mono | Code blocks, inline code |
| `font-display` | Cormorant Garamond | Hero titles, cover pages |
| `font-serif` | Bitstream Charter, Noto Sans SC, Noto Sans Devanagari | Default body text |

The base template sets `font-serif` as the default body font.

### Text Defaults

`apply-typography` sets:

- Font: `font-serif`
- Fill: `text-dark`
- Size: `ts-body` (10pt)
- Hyphenation: enabled
- Language: English
- Paragraph: justified, leading `ld-relaxed` (0.65em)

### Heading Styles

| Level | Size | Weight | Fill | Leading | Spacing Above | Spacing Below |
|---|---|---|---|---|---|---|
| H1 | `ts-h1` (22pt) | bold | `accent` | `ld-tight` | `sp-xl` (24pt) | `sp-lg` (16pt) |
| H2 | `ts-h2` (16pt) | semibold | `accent` | `ld-tight` | 20pt | `sp-md` (12pt) |
| H3 | `ts-h3` (13pt) | semibold | `text-dark` | `ld-snug` | `sp-lg` (16pt) | 10pt |
| H4 | `ts-h4` (11pt) | semibold | `text-dark` | `ld-snug` | `sp-md` (12pt) | `sp-sm` (8pt) |

H1 also applies `trk-tight` (-0.025em) tracking.

### List and Link Formatting

- Lists (ordered and unordered): indent 1em, body-indent 0.5em
- Links: colored `accent`, underlined

## Layout

`apply-layout` configures the page:

| Property | Value |
|---|---|
| Paper | US Letter |
| Margins | 1in on all sides |
| Header | Shows on page 2+; left: "inherent.design", right: date (if set); thin gray rule below |
| Footer | All pages; left: "inherent.design", right: "Page N of M"; thin gray rule above |

Header and footer text uses `ts-small` (8pt) in `text-gray`.

## Table Styling

`apply-tables` applies these rules:

- Header row (y = 0): bottom stroke `border-medium` in `accent`, bold text colored `accent`
- Data rows: bottom stroke `border-thin` in lightened `text-gray`
- Cell inset: `sp-sm` (8pt)

## Code Styling

`apply-code` applies these rules:

- All raw text: `font-code` at 0.9em relative size
- Block code: full width, `bg-subtle` fill, `border-thin` + `text-gray` stroke, 10pt inset, `radius-md` corners
- Inline code: text colored `accent`

## Utility Functions

### deep-merge

```typst
#let deep-merge(a, b)
```

Recursively merges dictionary `b` into dictionary `a`. When both values for a key are dictionaries, they merge recursively. Otherwise, `b` overwrites `a`.

```typst
#let defaults = (spacing: (top: 10pt, bottom: 5pt), color: blue)
#let overrides = (spacing: (bottom: 12pt), size: 14pt)
#let result = deep-merge(defaults, overrides)
```

### get

```typst
#let get(dict, key, default: "")
```

Safe dictionary access with a default. Returns `dict.at(key)` if the key exists, otherwise returns `default`.

```typst
#let name = get(config, "name", default: "Untitled")
```

### get-nested

```typst
#let get-nested(dict, keys, default: "")
```

Traverses nested dictionaries using an array of keys. Returns the value at the path if every key exists, otherwise returns `default`.

```typst
#let city = get-nested(data, ("address", "city"), default: "N/A")
```

## Components Overview

The barrel file `lib/components.typ` defines four base components (`title-block`, `info-table`, `signature-block`, `separator`) and re-exports three component modules:

- `components-layout.typ` for structural primitives
- `components-content.typ` for display blocks
- `components-document.typ` for full document sections

All components are available through the prelude.

## Base Components

### title-block

```typst
#let title-block(title: [], date: none)
```

Renders a document title in `font-display` at `ts-h1` size with the `accent` color. Optionally shows a date below in `text-gray`. Ends with a horizontal separator rule.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `title` | `content` | `[]` | Title text |
| `date` | `string` or `none` | `none` | Date shown below title when set |

### info-table

```typst
#let info-table(..pairs)
```

Renders label/value pairs in a two-column grid. Accepts positional arguments where each argument is a two-element array `(label, value)`. Labels are rendered bold.

```typst
#info-table(
  ("Client:", "Acme Corp"),
  ("Project:", "Website Redesign"),
  ("Status:", "In Progress"),
)
```

### signature-block

```typst
#let signature-block(party-name, include-title: true)
```

Renders a signature area with name and date fields (underlined blanks). Optionally includes a title field.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `party-name` | `content` | (required) | Bold heading for the signing party |
| `include-title` | `bool` | `true` | Whether to include a "Title:" field |

### separator

```typst
#let separator()
```

Renders a full-width horizontal rule in lightened `text-gray`, wrapped as a PDF artifact (excluded from accessibility tree).

## Layout Components

### hero-section

```typst
#let hero-section(
  title: [],
  subtitle: none,
  accent-line: true,
  fill: accent.lighten(92%),
  text-fill: text-dark,
)
```

Full-width banner with display-sized title. Suitable for document openers and section headers.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `title` | `content` | `[]` | Main title in `font-display` at `ts-display` |
| `subtitle` | `content` or `none` | `none` | Smaller text below title in `text-gray` |
| `accent-line` | `bool` | `true` | Show an 80pt accent-colored rule below content |
| `fill` | `color` | `accent.lighten(92%)` | Background fill |
| `text-fill` | `color` | `text-dark` | Title text color |

### two-column

```typst
#let two-column(
  left,
  right,
  ratio: (2fr, 1fr),
  gutter: sp-xl,
)
```

Simple two-column grid layout.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `left` | `content` | (required) | Left column content |
| `right` | `content` | (required) | Right column content |
| `ratio` | `array` | `(2fr, 1fr)` | Column width ratio |
| `gutter` | `length` | `sp-xl` (24pt) | Gap between columns |

### sidebar-layout

```typst
#let sidebar-layout(
  main,
  sidebar,
  sidebar-width: 2.2in,
  gutter: sp-xl,
  sidebar-position: "right",
)
```

Main content area with a fixed-width sidebar.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `main` | `content` | (required) | Main content area (fills remaining width) |
| `sidebar` | `content` | (required) | Sidebar content |
| `sidebar-width` | `length` | `2.2in` | Fixed sidebar width |
| `gutter` | `length` | `sp-xl` (24pt) | Gap between main and sidebar |
| `sidebar-position` | `string` | `"right"` | `"left"` or `"right"` |

### card

```typst
#let card(body, title: none, fill: bg-card, stroke: border-thin + border)
```

Rounded bordered container with optional title.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `body` | `content` | (required) | Card content |
| `title` | `content` or `none` | `none` | Bold 11pt title above body |
| `fill` | `color` | `bg-card` (#FFFFFF) | Background color |
| `stroke` | `stroke` | `border-thin + border` | Border stroke |

### card-grid

```typst
#let card-grid(
  cards,
  columns: 3,
  gutter: sp-md,
)
```

Arranges content in an equal-width grid. Typically used with `card` or `metric-card` elements.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `cards` | `array` | (required) | Array of content elements |
| `columns` | `int` | `3` | Number of columns |
| `gutter` | `length` | `sp-md` (12pt) | Row and column gap |

## Content Components

### metric-card

```typst
#let metric-card(
  value,
  label,
  description: none,
  fill: accent.lighten(92%),
  value-color: accent,
)
```

Displays a large numeric value with a label and optional description. Useful for KPIs and statistics.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `value` | `content` | (required) | Large display value (e.g., "98%") |
| `label` | `content` | (required) | Label below the value |
| `description` | `content` or `none` | `none` | Small caption text in `text-gray` |
| `fill` | `color` | `accent.lighten(92%)` | Card background |
| `value-color` | `color` | `accent` | Color of the value text |

### service-card

```typst
#let service-card(
  name,
  description,
  deliverables: (),
  accent-color: accent,
)
```

Left-bordered card for service or offering descriptions. Shows a name, description text, and optional deliverables list.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `name` | `content` | (required) | Service name in bold at `ts-h3` |
| `description` | `content` | (required) | Description text |
| `deliverables` | `array` | `()` | List of deliverable strings |
| `accent-color` | `color` | `accent` | Left border and name color |

### competency-block

```typst
#let competency-block(
  title,
  items,
  accent-color: accent,
  columns: 2,
)
```

Multi-column list with colored dot markers. Suitable for skill lists, features, or capabilities.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `title` | `content` | (required) | Section heading in bold at `ts-h3` |
| `items` | `array` | (required) | Array of text items |
| `accent-color` | `color` | `accent` | Dot and title color |
| `columns` | `int` | `2` | Number of columns |

### callout-box

```typst
#let callout-box(
  body,
  title: none,
  variant: "info",
  icon: none,
)
```

Left-bordered callout with semantic color variants.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `body` | `content` | (required) | Callout content |
| `title` | `content` or `none` | `none` | Bold title above body |
| `variant` | `string` | `"info"` | One of: `"info"`, `"warning"`, `"success"`, `"error"`, `"note"` |
| `icon` | `content` or `none` | `none` | Icon content shown before the title |

**Variant colors:**

| Variant | Fill | Border | Title Color |
|---|---|---|---|
| `"info"` | `info.lighten(90%)` | `info` | `info` |
| `"warning"` | `warning.lighten(88%)` | `warning` | `warning` |
| `"success"` | `success.lighten(90%)` | `success` | `success` |
| `"error"` | `error.lighten(90%)` | `error` | `error` |
| `"note"` (or other) | `bg-subtle` | `text-gray` | `text-dark` |

### Callout Presets

Pre-configured `callout-box` variants for convenience:

| Preset | Variant | Default Title |
|---|---|---|
| `info-box` | `"info"` | (none) |
| `warning-box` | `"warning"` | (none) |
| `success-box` | `"success"` | (none) |
| `error-box` | `"error"` | (none) |
| `note-box` | `"note"` | "Note" |
| `tip-box` | `"info"` | "Tip" |
| `important-box` | `"warning"` | "Important" |

```typst
#note-box[This is a note with a default title.]
#warning-box(title: "Caution")[Check your inputs before proceeding.]
```

### pull-quote

```typst
#let pull-quote(
  body,
  attribution: none,
  accent-color: accent,
)
```

Indented quote block with left accent border and optional attribution.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `body` | `content` | (required) | Quote text, rendered italic at `ts-h2` |
| `attribution` | `content` or `none` | `none` | Right-aligned attribution line |
| `accent-color` | `color` | `accent` | Left border color |

## Document Components

### cover-page

```typst
#let cover-page(
  title: [],
  subtitle: none,
  date: none,
  company: none,
  fill: white,
  accent-color: accent,
)
```

Full standalone cover page with accent bar, large title, and optional company name at the bottom. Renders on its own page with custom margins (1.5in horizontal, 2.5in top, 1.5in bottom) and no header/footer.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `title` | `content` | `[]` | Cover title in `font-display` at `ts-display + 8pt` |
| `subtitle` | `content` or `none` | `none` | Subtitle in `text-gray` at `ts-h2` |
| `date` | `string` or `none` | `none` | Date text |
| `company` | `string` or `none` | `none` | Company name anchored to bottom-left |
| `fill` | `color` | `white` | Page background |
| `accent-color` | `color` | `accent` | Top bar and rule color |

### contact-strip

```typst
#let contact-strip(
  name: none,
  title: none,
  email: none,
  phone: none,
  address: none,
  separator: [ | ],
)
```

Single-line contact information strip. Fields are joined with the separator. Email values are automatically wrapped in `mailto:` links.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `name` | `content` or `none` | `none` | Bold name |
| `title` | `content` or `none` | `none` | Job title |
| `email` | `string` or `none` | `none` | Email address (auto-linked) |
| `phone` | `content` or `none` | `none` | Phone number |
| `address` | `content` or `none` | `none` | Mailing address |
| `separator` | `content` | `[ \| ]` | Delimiter between fields |

### registration-block

```typst
#let registration-block(
  uei: none,
  cage: none,
  sam: none,
  naics-primary: none,
  naics-secondary: none,
  certifications: none,
  ein-last4: none,
)
```

Federal registration information panel with `bg-subtle` background. Renders a labeled grid of registration identifiers.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `uei` | `content` or `none` | `none` | Unique Entity Identifier |
| `cage` | `content` or `none` | `none` | CAGE Code |
| `sam` | `content` or `none` | `none` | SAM.gov registration status |
| `naics-primary` | `content` or `none` | `none` | Primary NAICS code |
| `naics-secondary` | `content` or `none` | `none` | Secondary NAICS codes |
| `certifications` | `content` or `none` | `none` | Certifications list |
| `ein-last4` | `content` or `none` | `none` | Last 4 digits of EIN |

Only fields with non-`none` values are rendered.

### invoice-header

```typst
#let invoice-header(
  company: none,
  client: none,
  number: none,
  date: none,
  due: none,
  po-number: none,
)
```

Two-column invoice header. Left side shows company identity (name, address, email, phone). Right side shows "INVOICE" label with metadata fields. Below both, a "BILL TO" section shows client details.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `company` | `dictionary` or `none` | `none` | Keys: `name`, `address`, `email`, `phone` |
| `client` | `dictionary` or `none` | `none` | Keys: `name`, `address` |
| `number` | `content` or `none` | `none` | Invoice number |
| `date` | `content` or `none` | `none` | Invoice date |
| `due` | `content` or `none` | `none` | Due date |
| `po-number` | `content` or `none` | `none` | Purchase order number (shown only when set) |

### line-items-table

```typst
#let line-items-table(
  items,
  tax-rate: none,
  tax-label: "Tax",
  currency: "$",
  show-quantity: true,
)
```

Invoice line items table with automatic subtotal, tax, and total calculations.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `items` | `array` | (required) | Array of dictionaries; each needs `description` and `amount`; optional `quantity` and `rate` |
| `tax-rate` | `float` or `none` | `none` | Tax rate as decimal (e.g., 0.0875 for 8.75%); omitted when `none` |
| `tax-label` | `string` | `"Tax"` | Label for the tax row |
| `currency` | `string` | `"$"` | Currency symbol prefix |
| `show-quantity` | `bool` | `true` | Show Qty and Rate columns; set `false` for flat-fee invoices |

When `show-quantity` is `true`, the table renders four columns: Description, Qty, Rate, Amount. When `false`, it renders two columns: Description, Amount.

```typst
#line-items-table(
  (
    (description: "Web Design", quantity: 1, rate: 5000, amount: 5000),
    (description: "Hosting (annual)", quantity: 1, rate: 600, amount: 600),
  ),
  tax-rate: 0.0875,
)
```

## Integration

### How the docs repo consumes this package

The brand package is installed as an npm dependency (`@inherent.design/brand`) and symlinked into the Typst `@local` namespace at install time. Templates access it via `@local/brand:0.4.1` through the docs prelude.

The import chain in a typical document:

```
@local/brand:0.4.1 (prelude.typ)
  <- docs/lib/prelude.typ (adds load-defaults)
    <- docs/templates/*.typ (individual documents)
```

### Docs prelude

The docs repo defines its own `lib/prelude.typ` that wraps the brand prelude:

```typst
#import "@local/brand:0.4.1": *
```

This gives every template access to `base-template`, all tokens, all components, and the utility functions.

### Font path requirement

Builds require `--font-path` pointing to the brand fonts directory. The build script uses `--ignore-system-fonts` for reproducibility, loading only bundled fonts from `node_modules/@inherent.design/brand/fonts/src/typst`.

### Symlink setup

The `scripts/link-brand.sh` script creates the `@local` symlink so Typst resolves `@local/brand:0.4.1` to the brand package directory.
