// Design tokens: spacing, type scale, borders, radii

// Spacing scale (4pt geometric base)
// Print uses tighter spacing than CSS (screen): sp-md=12pt vs CSS 16px, sp-lg=16pt vs CSS 24px.
// This is intentional, print density requires tighter vertical rhythm.
#let sp-0 = 0pt
#let sp-1 = 2pt
#let sp-2 = 4pt
#let sp-3 = 8pt
#let sp-4 = 12pt
#let sp-5 = 16pt
#let sp-6 = 24pt
#let sp-7 = 32pt

// Semantic spacing aliases
#let sp-xs = sp-2    // 4pt
#let sp-sm = sp-3    // 8pt
#let sp-md = sp-4    // 12pt
#let sp-lg = sp-5    // 16pt
#let sp-xl = sp-6    // 24pt
#let sp-2xl = sp-7   // 32pt
#let sp-3xl = 48pt

// Type scale
#let ts-tiny = 7pt
#let ts-small = 8pt
#let ts-caption = 9pt
#let ts-body = 10pt
#let ts-h4 = 11pt
#let ts-h3 = 13pt
#let ts-h2 = 16pt
#let ts-h1 = 22pt
#let ts-display = 28pt

// Border weights
#let border-thin = 0.5pt
#let border-medium = 1pt
#let border-thick = 2pt

// Border radii
#let radius-sm = 2pt
#let radius-md = 4pt
#let radius-lg = 8pt

// Leading (Typst par leading ≈ CSS line-height - 1)
#let ld-tight = 0.2em      // CSS line-height: 1.2 (headings)
#let ld-snug = 0.375em     // CSS line-height: 1.375 (sub-headings)
#let ld-normal = 0.5em     // CSS line-height: 1.5
#let ld-relaxed = 0.65em   // CSS line-height: 1.65 (body text)

// Tracking (letter-spacing)
#let trk-tight = -0.025em
#let trk-normal = 0em
#let trk-wide = 0.025em
