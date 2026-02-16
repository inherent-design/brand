// Font stacks, text rules, heading styles

#import "colors.typ": text-dark, text-gray, accent
#import "tokens.typ": ts-body, ts-h1, ts-h2, ts-h3, ts-h4, sp-sm, sp-md, sp-lg, sp-xl, ld-tight, ld-snug, ld-relaxed, trk-tight

// Font stacks
#let font-body = ("Inter", "Noto Sans SC", "Noto Sans Devanagari")
#let font-code = ("Commit Mono", "Noto Sans Mono")
#let font-display = ("Cormorant Garamond",)
#let font-serif = ("Bitstream Charter", "Noto Sans SC", "Noto Sans Devanagari")

#let apply-typography(doc) = {
  // Base text
  set text(
    font: font-serif,
    fill: text-dark,
    size: ts-body,
    hyphenate: true,
    lang: "en",
  )

  set par(justify: true, leading: ld-relaxed)

  // Headings
  show heading.where(level: 1): it => {
    set text(size: ts-h1, weight: "bold", fill: accent, tracking: trk-tight)
    set par(leading: ld-tight)
    block(above: sp-xl, below: sp-lg)[#it.body]
  }

  show heading.where(level: 2): it => {
    set text(size: ts-h2, weight: "semibold", fill: accent)
    set par(leading: ld-tight)
    block(above: 20pt, below: sp-md)[#it.body]
  }

  show heading.where(level: 3): it => {
    set text(size: ts-h3, weight: "semibold", fill: text-dark)
    set par(leading: ld-snug)
    block(above: sp-lg, below: 10pt)[#it.body]
  }

  show heading.where(level: 4): it => {
    set text(size: ts-h4, weight: "semibold", fill: text-dark)
    set par(leading: ld-snug)
    block(above: sp-md, below: sp-sm)[#it.body]
  }

  // Lists
  set list(indent: 1em, body-indent: 0.5em)
  set enum(indent: 1em, body-indent: 0.5em)

  // Links
  show link: set text(fill: accent)
  show link: underline

  doc
}
