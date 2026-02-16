# Brand Fonts

Multi-locale font system providing four typographic stacks across English, Chinese, and Hindi, with automated pipelines for web font subsetting and Typst static instancing.

## Quick Reference

### Font Stacks

| Stack | CSS Custom Property | English | Chinese | Hindi |
|---|---|---|---|---|
| Serif | `--brand-font-serif` | Charter | Charter, LXGW WenKai | Charter, Tiro Devanagari Hindi |
| Display | `--brand-font-display` | Cormorant Garamond | Cormorant Garamond, LXGW WenKai | Cormorant Garamond, Tiro Devanagari Hindi |
| Sans | `--brand-font-sans` | Inter | Inter, Noto Sans SC | Inter, Noto Sans Devanagari |
| Mono | `--brand-font-mono` | Commit Mono | Commit Mono, Sarasa Mono SC | Commit Mono, Noto Sans Mono |

### Locale Support

| Locale | Tag | Script Fonts | Subset Count |
|---|---|---|---|
| English | `en` | Charter, Cormorant Garamond, Inter, Commit Mono | 94 woff2 files |
| Chinese | `zh` | LXGW WenKai, Noto Sans SC, Sarasa Mono SC | 871 woff2 files |
| Hindi | `hi` | Tiro Devanagari Hindi, Noto Sans Devanagari, Noto Sans Mono | 54 woff2 files |

## Directory Structure

```
fonts/
  vars.css              CSS custom properties (font stacks per locale)
  src/                  Source font files (gitignored, fetched by download.js)
    *.ttf / *.otf       14 direct downloads + 1 archive extraction
    typst/              Static instances + symlinks for Typst consumption
  dist/                 Built web font subsets (committed)
    en/                 English locale: index.css + 94 woff2 files
    zh/                 Chinese locale: index.css + 871 woff2 files
    hi/                 Hindi locale: index.css + 54 woff2 files
  scripts/
    download.js         Fetches source fonts from GitHub
    build.js            Runs cn-font-split to produce per-locale woff2 subsets
    instance.py         Generates static TTF instances from variable fonts for Typst
  licenses/             One license file per font family (10 files)
```

## Font Stacks

### Serif (Charter)

Primary body text font. Charter is a static font distributed as four separate OTF files (Regular, Bold, Italic, Bold Italic). It serves as the base serif across all locales.

CSS property: `--brand-font-serif`

| Locale | Stack |
|---|---|
| en | `'Charter', Georgia, serif` |
| zh | `'Charter', 'LXGW WenKai', serif` |
| hi | `'Charter', 'Tiro Devanagari Hindi', Georgia, serif` |

### Display (Cormorant Garamond)

Used for headings and display typography. Cormorant Garamond is a variable font with a weight axis spanning 300 to 700.

CSS property: `--brand-font-display`

| Locale | Stack |
|---|---|
| en | `'Cormorant Garamond', 'Charter', Georgia, serif` |
| zh | `'Cormorant Garamond', 'LXGW WenKai', serif` |
| hi | `'Cormorant Garamond', 'Tiro Devanagari Hindi', Georgia, serif` |

### Sans (Inter)

Interface and UI font. Inter is a variable font with optical size (opsz 14 to 32) and weight (wght 100 to 900) axes.

CSS property: `--brand-font-sans`

| Locale | Stack |
|---|---|
| en | `'Inter', system-ui, sans-serif` |
| zh | `'Inter', 'Noto Sans SC', system-ui, sans-serif` |
| hi | `'Inter', 'Noto Sans Devanagari', system-ui, sans-serif` |

### Mono (Commit Mono)

Code and monospaced content. Commit Mono is a variable font with weight (wght 200 to 700) and italic (ital 0 to 1) axes.

CSS property: `--brand-font-mono`

| Locale | Stack |
|---|---|
| en | `'Commit Mono', monospace` |
| zh | `'Commit Mono', 'Sarasa Mono SC', monospace` |
| hi | `'Commit Mono', 'Noto Sans Mono', monospace` |

## Source Fonts

All source fonts live in `src/` and are gitignored. Run `download.js` to fetch them.

### Direct Downloads (14 files)

| File | Format | Family | Weight Range | Source |
|---|---|---|---|---|
| `cormorant-garamond-variable.ttf` | Variable TTF | Cormorant Garamond | 300 to 700 | google/fonts |
| `cormorant-garamond-italic-variable.ttf` | Variable TTF | Cormorant Garamond Italic | 300 to 700 | google/fonts |
| `charter-regular.otf` | Static OTF | Charter | 400 | davidseegert/Bitstream-Charter |
| `charter-bold.otf` | Static OTF | Charter | 700 | davidseegert/Bitstream-Charter |
| `charter-italic.otf` | Static OTF | Charter | 400 italic | davidseegert/Bitstream-Charter |
| `charter-bold-italic.otf` | Static OTF | Charter | 700 italic | davidseegert/Bitstream-Charter |
| `inter-variable.ttf` | Variable TTF | Inter | 100 to 900 | google/fonts |
| `inter-italic-variable.ttf` | Variable TTF | Inter Italic | 100 to 900 | google/fonts |
| `commit-mono-variable.ttf` | Variable TTF | Commit Mono | 200 to 700 | eigilnikolajsen/commit-mono |
| `lxgw-wenkai-regular.ttf` | Static TTF | LXGW WenKai | 400 | lxgw/LxgwWenKai |
| `noto-sans-sc-variable.ttf` | Variable TTF | Noto Sans SC | 100 to 900 | google/fonts |
| `tiro-devanagari-regular.ttf` | Static TTF | Tiro Devanagari Hindi | 400 | google/fonts |
| `noto-sans-devanagari-variable.ttf` | Variable TTF | Noto Sans Devanagari | 100 to 900 | google/fonts |
| `noto-sans-mono-variable.ttf` | Variable TTF | Noto Sans Mono | 100 to 900 | google/fonts |

### Archive Downloads (1 file)

| File | Format | Family | Source |
|---|---|---|---|
| `sarasa-mono-sc-regular.ttf` | Static TTF | Sarasa Mono SC | be5invis/Sarasa-Gothic (7z archive, requires `7z` CLI) |

## Typst Static Instances

### Why Static Instances Are Needed

Typst (as of 0.14.x) does not support variable fonts (see typst/typst#185). The `instance.py` script uses fonttools to pin variable font axes at specific values, producing static TTF files that Typst can consume.

### How instance.py Works

1. Creates the `src/typst/` output directory
2. Symlinks already-static source fonts (Charter OTFs, LXGW WenKai, Sarasa Mono SC, Tiro Devanagari) into `src/typst/`
3. For each variable font, calls `fonttools.varLib.instancer.instantiateVariableFont` with pinned axis values
4. Applies name table fixes so Typst resolves fonts by the correct family and subfamily names

### Name Table Fixes

Variable fonts often have non-standard family names in their name tables (for example, the Commit Mono source uses "CommitMonoV143 ExtLt" as its family). The `fix_name_table` function overwrites six name table entries (IDs 1, 2, 4, 6, 16, 17) to set the canonical family name, subfamily, full name, and PostScript name. It also adjusts `OS/2.usWeightClass`, `OS/2.fsSelection`, and `head.macStyle` to match the target weight and style.

### Output Files (24 total)

**Symlinks to static sources (7 files):**

| File | Links To |
|---|---|
| `charter-regular.otf` | `../charter-regular.otf` |
| `charter-bold.otf` | `../charter-bold.otf` |
| `charter-italic.otf` | `../charter-italic.otf` |
| `charter-bold-italic.otf` | `../charter-bold-italic.otf` |
| `lxgw-wenkai-regular.ttf` | `../lxgw-wenkai-regular.ttf` |
| `sarasa-mono-sc-regular.ttf` | `../sarasa-mono-sc-regular.ttf` |
| `tiro-devanagari-regular.ttf` | `../tiro-devanagari-regular.ttf` |

**Generated instances (17 files):**

| File | Family | Subfamily | Axes Pinned |
|---|---|---|---|
| `inter-regular.ttf` | Inter | Regular | opsz=14, wght=400 |
| `inter-bold.ttf` | Inter | Bold | opsz=14, wght=700 |
| `inter-black.ttf` | Inter | Black | opsz=14, wght=900 |
| `inter-italic.ttf` | Inter | Italic | opsz=14, wght=400 |
| `inter-bold-italic.ttf` | Inter | Bold Italic | opsz=14, wght=700 |
| `commit-mono-regular.ttf` | Commit Mono | Regular | wght=400, ital=0 |
| `commit-mono-bold.ttf` | Commit Mono | Bold | wght=700, ital=0 |
| `cormorant-garamond-regular.ttf` | Cormorant Garamond | Regular | wght=400 |
| `cormorant-garamond-bold.ttf` | Cormorant Garamond | Bold | wght=700 |
| `cormorant-garamond-italic.ttf` | Cormorant Garamond | Italic | wght=400 |
| `cormorant-garamond-bold-italic.ttf` | Cormorant Garamond | Bold Italic | wght=700 |
| `noto-sans-sc-regular.ttf` | Noto Sans SC | Regular | wght=400 |
| `noto-sans-sc-bold.ttf` | Noto Sans SC | Bold | wght=700 |
| `noto-sans-devanagari-regular.ttf` | Noto Sans Devanagari | Regular | wght=400, wdth=100 |
| `noto-sans-devanagari-bold.ttf` | Noto Sans Devanagari | Bold | wght=700, wdth=100 |
| `noto-sans-mono-regular.ttf` | Noto Sans Mono | Regular | wght=400, wdth=100 |
| `noto-sans-mono-bold.ttf` | Noto Sans Mono | Bold | wght=700, wdth=100 |

## Web Font Subsets

### cn-font-split Pipeline

The `build.js` script uses [cn-font-split](https://github.com/nicepkg/cn-font-split) to convert source fonts into optimized woff2 subsets. Each source font is split into small, independently loadable chunks. The browser fetches only the subsets needed for the characters on the page.

### Per-Locale Strategy

Each font is assigned to a locale. All subsets and `@font-face` rules for a locale are merged into a single `index.css` file within that locale's output directory.

| Locale | Fonts Included | Output |
|---|---|---|
| en | Charter (4 styles), Cormorant Garamond (2 variable), Inter (1 variable), Commit Mono (1 variable) | `dist/en/index.css` |
| zh | LXGW WenKai (1 static), Noto Sans SC (1 variable), Sarasa Mono SC (1 static) | `dist/zh/index.css` |
| hi | Tiro Devanagari Hindi (1 static), Noto Sans Devanagari (1 variable), Noto Sans Mono (1 variable) | `dist/hi/index.css` |

### Output Structure

```
dist/
  en/
    index.css          Merged @font-face rules for all English fonts
    *.woff2            94 subset files
  zh/
    index.css          Merged @font-face rules for all Chinese fonts
    *.woff2            871 subset files
  hi/
    index.css          Merged @font-face rules for all Hindi fonts
    *.woff2            54 subset files
```

The Chinese locale produces far more subsets because CJK fonts contain tens of thousands of glyphs. cn-font-split uses Unicode range splitting to keep each subset small enough for efficient HTTP/2 loading.

## Scripts Reference

### download.js

Fetches all source fonts from GitHub into `src/`.

```
node fonts/scripts/download.js
```

Skips fonts that already exist in `src/`. For the Sarasa Mono SC archive, it downloads the 7z file into `.tmp-download/`, extracts the target TTF, copies it to `src/`, and removes the temp directory. Requires the `7z` CLI for archive extraction.

### build.js

Produces per-locale woff2 subsets from source fonts.

```
node fonts/scripts/build.js
```

Cleans `dist/` and `.tmp-build/` before each run. For each font config, it calls `cn-font-split` with the source font, target format (woff2), and CSS metadata (family, weight, style, display). After splitting, it copies woff2 files into the locale directory and merges all `result.css` outputs into a single `index.css` per locale.

### instance.py

Generates static TTF instances from variable fonts for Typst compatibility.

```
uv run brand/fonts/scripts/instance.py
```

Requires Python 3.11+ and fonttools 4.61+. Uses [uv](https://github.com/astral-sh/uv) inline script metadata for dependency resolution. Skips files that already exist in `src/typst/`.

## CSS Integration

### vars.css Structure

The `vars.css` file defines four CSS custom properties under locale-specific `:root` selectors. A base `:root` rule provides generic fallbacks for unsupported locales.

```css
:root {
  --brand-font-serif: serif;
  --brand-font-display: serif;
  --brand-font-sans: system-ui, sans-serif;
  --brand-font-mono: monospace;
}

:root:lang(en) {
  --brand-font-serif: 'Charter', Georgia, serif;
  --brand-font-display: 'Cormorant Garamond', 'Charter', Georgia, serif;
  --brand-font-sans: 'Inter', system-ui, sans-serif;
  --brand-font-mono: 'Commit Mono', monospace;
}
```

Each locale (en, zh, hi) overrides the custom properties with its own font stack, appending locale-specific script fonts after the shared Latin fonts.

### Consuming Fonts in a Site or App

1. Import the font stack variables: `@inherent.design/brand/fonts/vars`
2. Import the locale subset CSS: `@inherent.design/brand/fonts/en` (and/or `zh`, `hi`)
3. Use the custom properties in your stylesheets:

```css
body {
  font-family: var(--brand-font-serif);
}

h1, h2, h3 {
  font-family: var(--brand-font-display);
}

code, pre {
  font-family: var(--brand-font-mono);
}
```

The package exports these paths via the `@inherent.design/brand` package.json `exports` field.

## Licensing

| Font Family | License | File |
|---|---|---|
| Charter | Bitstream Charter License | `LICENSE-Charter.txt` |
| Commit Mono | MIT | `LICENSE-CommitMono.txt` |
| Cormorant Garamond | SIL Open Font License 1.1 | `LICENSE-CormorantGaramond.txt` |
| Inter | SIL Open Font License 1.1 | `LICENSE-Inter.txt` |
| LXGW WenKai | SIL Open Font License 1.1 | `LICENSE-LXGWWenKai.txt` |
| Noto Sans Devanagari | SIL Open Font License 1.1 | `LICENSE-NotoSansDevanagari.txt` |
| Noto Sans Mono | SIL Open Font License 1.1 | `LICENSE-NotoSansMono.txt` |
| Noto Sans SC | SIL Open Font License 1.1 | `LICENSE-NotoSansSC.txt` |
| Sarasa Mono SC | SIL Open Font License 1.1 | `LICENSE-SarasaMonoSC.txt` |
| Tiro Devanagari Hindi | SIL Open Font License 1.1 | `LICENSE-TiroDevanagari.txt` |

All license files are in the `licenses/` directory and are included in the published npm package.

## Build Pipeline

The full pipeline runs three stages. The `prepare` hook in the brand package.json automates the first two stages on `pnpm install`.

### Stage 1: Download Sources

```
pnpm run fonts:download
```

Fetches all 15 source fonts (14 direct, 1 archive) into `src/`. Idempotent; skips existing files.

### Stage 2: Build Web Subsets

```
pnpm run fonts:build
```

Runs cn-font-split on all source fonts, producing per-locale woff2 subsets in `dist/`.

### Stage 3: Generate Typst Instances

```
uv run brand/fonts/scripts/instance.py
```

Produces static TTF instances in `src/typst/`. This step is separate from the npm prepare hook because it requires Python and fonttools.

### npm prepare Hook

The `prepare` script in `package.json` chains download and build:

```
"prepare": "pnpm run fonts:download && pnpm run fonts:build"
```

This runs automatically on `pnpm install`, ensuring web font assets are ready before any consuming project builds.

## Adding a New Font

1. **Add to download.js.** Add an entry to the `FONTS` array (or `ARCHIVES` if the font comes in an archive). Specify `name`, `url`, and `filename`.

2. **Add to build.js configs.** Add an entry to the `configs` array with the source input path, target locale, and CSS metadata (fontFamily, fontWeight, fontStyle, fontDisplay).

3. **Add instance.py entries (if variable).** If the font is a variable font and needs Typst support, add entries to the `INSTANCES` list specifying the source file, output file, pinned axis values, and target family/subfamily names. If the font is already static, add it to the `static_fonts` list for symlinking.

4. **Add a license file.** Place the font's license in `licenses/` with the naming pattern `LICENSE-{FontFamily}.txt`.

5. **Update vars.css.** Add the font family name to the appropriate CSS custom property for each locale where it applies.

6. **Run the pipeline.** Execute download, build, and (if applicable) instance stages to verify everything works.

## Gitignore Strategy

### Tracked (committed to the repository)

- `vars.css` (CSS custom properties)
- `dist/` (built woff2 subsets and merged CSS per locale)
- `src/typst/` (static instances and symlinks for Typst)
- `scripts/` (download, build, and instancing scripts)
- `licenses/` (per-font license files)

### Not Tracked (gitignored)

- `src/*.ttf` and `src/*.otf` (source fonts, fetched by download.js)
- `.tmp-download/` (temporary archive extraction directory)
- `.tmp-build/` (temporary cn-font-split output directory)

Source fonts are excluded because they are large binary files that can be deterministically re-fetched from their upstream repositories.

## Troubleshooting

### Missing Source Fonts

If `build.js` or `instance.py` fails with missing file errors, run the download script first:

```
pnpm run fonts:download
```

Verify that all 15 files exist in `src/` (14 .ttf + 1 .otf set of 4 files, totaling 15 source files).

### Sarasa Mono SC Download Fails

The Sarasa archive download requires the `7z` command-line tool. Install it via your package manager:

```
brew install 7-zip        # macOS
apt install p7zip-full    # Debian/Ubuntu
```

### Typst Font Resolution Issues

If Typst cannot find a font by name, verify the static instance exists in `src/typst/` and that its name table is correct. You can inspect the name table with fonttools:

```
python -c "from fontTools.ttLib import TTFont; t = TTFont('src/typst/inter-regular.ttf'); print([(r.nameID, str(r)) for r in t['name'].names[:10]])"
```

The family name (nameID 1) and typographic family name (nameID 16) must match what your Typst document requests.

### Build Produces No Output

If `build.js` completes but `dist/` is empty, check that `cn-font-split` is installed:

```
pnpm install
```

The `cn-font-split` package is listed as a devDependency in the brand package.json.

### Inter Italic Variable Missing

The Inter Italic variable font (`inter-italic-variable.ttf`) is a separate download from the upright. If italic instance generation fails, confirm the italic source was fetched by checking `src/inter-italic-variable.ttf`.
