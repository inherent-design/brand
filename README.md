# @inherent.design/brand

[![npm](https://img.shields.io/npm/v/@inherent.design/brand?style=flat&logo=npm&logoColor=white&color=CB3837)](https://www.npmjs.com/package/@inherent.design/brand) [![License](https://img.shields.io/github/license/inherent-design/brand?style=flat)](LICENSE)

Single source of truth for the inherent.design design language across print (Typst) and web (CSS/Astro).

## Quick Start

```sh
pnpm add @inherent.design/brand
```

On install, the `prepare` hook automatically downloads source fonts and builds optimized web font subsets. No additional setup is required for web consumption.

For Typst document consumption, run the symlink script in your docs project to register the package under the `@local` namespace:

```sh
./scripts/link-brand.sh
```

## Module Overview

| Module | Purpose | Key Exports | README |
|---|---|---|---|
| `typst/` | Typst design system for print (PDF) output | `base-template`, color/spacing/type tokens, layout and content components | [typst/README.md](typst/README.md) |
| `fonts/` | Multi-locale font pipeline (download, subset, instance) | CSS font stacks, woff2 subsets, static Typst instances | [fonts/README.md](fonts/README.md) |
| `components/` | Branded Astro components on Starwind UI | Button, Prose, Image, Separator | [components/README.md](components/README.md) |
| `styles/` | CSS design tokens and Starwind theme bridge | Brand token custom properties, Tailwind v4 theme mapping | [styles/README.md](styles/README.md) |

## Package Exports

The complete exports map from `package.json`:

### Fonts

| Export Path | File | Description |
|---|---|---|
| `./fonts/vars` | `fonts/vars.css` | CSS custom properties defining locale-aware font stacks |
| `./fonts/en` | `fonts/dist/en/index.css` | English locale: `@font-face` rules and woff2 subsets |
| `./fonts/zh` | `fonts/dist/zh/index.css` | Chinese locale: `@font-face` rules and woff2 subsets |
| `./fonts/hi` | `fonts/dist/hi/index.css` | Hindi locale: `@font-face` rules and woff2 subsets |

### Styles

| Export Path | File | Description |
|---|---|---|
| `./styles` | `styles/styles.css` | Brand design tokens as `--brand-*` CSS custom properties |
| `./styles/starwind` | `styles/starwind.css` | Starwind UI / Tailwind CSS v4 theme bridge with light and dark mode |

### Components

| Export Path | File | Description |
|---|---|---|
| `./components/button` | `components/button/index.ts` | Polymorphic button (renders as `<a>` or `<button>`) with 8 variants and 6 sizes |
| `./components/image` | `components/image/index.ts` | Wrapper around Astro's `<Image>` with responsive defaults |
| `./components/prose` | `components/prose/index.ts` | Typography container for rendered markdown and HTML content |
| `./components/separator` | `components/separator/index.ts` | Accessible horizontal or vertical divider |

### Typst

| Export Path | File | Description |
|---|---|---|
| `./typst` | `typst/inherent.typ` | Base template with show rule chain (typography, layout, tables, code) |
| `./typst/prelude` | `typst/prelude.typ` | Public entrypoint re-exporting all tokens, components, and utilities |

## Sub-Module Index

### typst/

Design tokens, components, and layout primitives for Typst documents. Provides `base-template` (a show rule chain applying typography, page layout, table styling, and code formatting), a full token set (colors, spacing, type scale, borders, radii, leading, tracking), four font stacks, and three tiers of components: layout primitives (hero, columns, cards), content blocks (metrics, callouts, quotes), and document sections (cover page, invoice, registration).

See [typst/README.md](typst/README.md) for the full API reference.

### fonts/

Multi-locale font system serving four typographic stacks (Serif, Display, Sans, Mono) across English, Chinese, and Hindi. Includes automated pipelines for downloading source fonts from GitHub, building per-locale woff2 subsets via cn-font-split, and generating static TTF instances for Typst compatibility. The web font output totals 1,019 woff2 files across three locales.

See [fonts/README.md](fonts/README.md) for font stacks, scripts, and the instancing pipeline.

### components/

Branded Astro components built on Starwind UI and Tailwind Variants. Each component follows a consistent pattern: a `.astro` file with a `tv()` variant schema, a barrel `index.ts` exporting both the component and its raw variant function, and a `data-slot` attribute for styling hooks. All components require the Starwind CSS foundation from `styles/starwind.css`.

See [components/README.md](components/README.md) for props, variants, and usage examples.

### styles/

Two-layer CSS system. The first layer (`styles.css`) declares canonical brand values as `--brand-*` custom properties covering colors (oklch), typography scale, spacing, layout constraints, and borders. The second layer (`starwind.css`) bridges brand tokens to Starwind semantic variables that Tailwind CSS v4 exposes as utility classes, with full light and dark mode support.

See [styles/README.md](styles/README.md) for the complete token reference and theme mapping.

## Integration Patterns

### Document Pipeline (docs repo)

The docs repo consumes the brand package for Typst document generation through three mechanisms:

**1. Symlink registration.** The `link-brand.sh` script reads the version from `typst.toml` and creates a symlink in the local Typst package directory so that `@local/brand:0.4.1` resolves to the brand package inside `node_modules`.

**2. Prelude import chain.** Templates access the brand system through a layered import:

```
@local/brand:0.4.1 (prelude.typ)
  <- docs/lib/prelude.typ (wraps brand prelude, adds project utilities)
    <- docs/templates/*.typ (individual documents)
```

**3. Font path.** Typst builds require `--font-path` pointing to `node_modules/@inherent.design/brand/fonts/src/typst`. The build script uses `--ignore-system-fonts` for reproducibility, loading only the bundled static instances.

### Web Application (site repo)

The site repo (future) will consume the brand package through standard npm imports:

```astro
---
import "@inherent.design/brand/fonts/en";
import "@inherent.design/brand/fonts/vars";
import "@inherent.design/brand/styles";
import "@inherent.design/brand/styles/starwind";
import { Button } from "@inherent.design/brand/components/button";
import { Prose } from "@inherent.design/brand/components/prose";
---
```

Load order matters: font face declarations first, then font variable assignments, then brand tokens, then the Starwind theme that references everything above.

### Design Token Flow

The brand package maintains parallel token systems for two output media:

```
Brand Design Language
  |
  +-- Web (CSS): styles.css -> starwind.css -> Tailwind utilities
  |     Colors in oklch, spacing for screen density
  |
  +-- Print (Typst): lib/colors.typ + lib/tokens.typ -> base-template
        Colors in sRGB hex, spacing tuned for print density
```

Both systems share the same conceptual values (accent color, type scale, spacing rhythm) but adapt them for their medium. The spacing scale intentionally diverges because print requires tighter vertical rhythm than screen rendering. When updating the design language, changes should propagate to both layers.

## Development

### Prerequisites

- Node.js 18+
- pnpm
- Python 3.11+ with fonttools 4.61+ (for Typst static instancing only)
- `7z` CLI (for Sarasa Mono SC archive extraction only)

### Working on the Brand Package

```sh
git clone <repo>
cd brand
pnpm install
```

The `pnpm install` step triggers the `prepare` hook, which downloads source fonts and builds web font subsets automatically.

### Available Scripts

| Script | Command | Description |
|---|---|---|
| `fonts:download` | `node fonts/scripts/download.js` | Fetch source fonts from GitHub into `fonts/src/` |
| `fonts:build` | `node fonts/scripts/build.js` | Run cn-font-split to produce per-locale woff2 subsets |
| `prepare` | (runs on install) | Chains `fonts:download` and `fonts:build` |

To generate Typst static instances (separate from the npm lifecycle):

```sh
uv run brand/fonts/scripts/instance.py
```

## Version History

**0.4.1** (current)

Published to npm as `@inherent.design/brand`. Includes the complete Typst design system with base template and three component tiers (layout, content, document), multi-locale font pipeline with automated download and subsetting, four branded Astro components, and the two-layer CSS token system with Starwind theme bridge and dark mode support.

## License

Apache-2.0. See [LICENSE](LICENSE) for the full text.

Individual font families are distributed under their own licenses (SIL OFL 1.1, MIT, Bitstream Charter License). See [fonts/licenses/](fonts/licenses/) for details.
