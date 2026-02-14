// =============================================================================
// inherent.design -- Document Template (Pandoc-compatible)
// =============================================================================
// Minimal professional template for client-facing documents.
// Used as Pandoc --template for Markdown -> Typst -> PDF pipeline.

// -----------------------------------------------------------------------------
// COLORS
// -----------------------------------------------------------------------------

#let text-dark = rgb("#1a1a1a")
#let text-gray = rgb("#6b7280")
#let accent = rgb("#2563eb")        // inherent.design blue

// -----------------------------------------------------------------------------
// PANDOC COMPATIBILITY
// -----------------------------------------------------------------------------
// Required for Pandoc's Markdown -> Typst conversion

#let horizontalrule = pdf.artifact(line(length: 100%, stroke: 0.5pt + text-gray.lighten(40%)))

#show terms: it => {
  it
    .children
    .map(child => [
      #strong[#child.term]
      #block(inset: (left: 1.5em, top: -0.4em))[#child.description]
    ])
    .join()
}

#set table(
  inset: (x: 6pt, y: 8pt),
  stroke: none,
)

#show figure.where(kind: table): set figure.caption(position: top)
#show figure: set block(breakable: true)
#show figure.where(kind: image): set figure.caption(position: bottom)

#set smartquote(enabled: true)

// -----------------------------------------------------------------------------
// DOCUMENT TEMPLATE
// -----------------------------------------------------------------------------

#let inherent-doc(
  title: [],
  date: none,
  doc,
) = {
  // Page setup
  set page(
    paper: "us-letter",
    margin: (top: 1in, bottom: 1in, left: 1in, right: 1in),
    header: context {
      if counter(page).get().first() > 1 {
        set text(size: 8pt, fill: text-gray)
        grid(
          columns: (1fr, auto),
          [inherent.design],
          if date != none [#date],
        )
        v(-8pt)
        line(length: 100%, stroke: 0.5pt + text-gray.lighten(60%))
      }
    },
    footer: context {
      set text(size: 8pt, fill: text-gray)
      line(length: 100%, stroke: 0.5pt + text-gray.lighten(60%))
      v(4pt)
      grid(
        columns: (1fr, auto),
        [inherent.design],
        [Page #counter(page).display("1 of 1", both: true)],
      )
    },
  )

  // Typography
  set text(
    font: "Charter",
    fill: text-dark,
    size: 10pt,
    hyphenate: true,
  )

  set par(justify: true, leading: 0.65em)

  // Headings
  show heading.where(level: 1): it => {
    set text(size: 22pt, weight: "bold", fill: accent)
    block(above: 24pt, below: 16pt)[#it.body]
  }

  show heading.where(level: 2): it => {
    set text(size: 16pt, weight: "bold", fill: accent)
    block(above: 20pt, below: 12pt)[#it.body]
  }

  show heading.where(level: 3): it => {
    set text(size: 13pt, weight: "bold", fill: text-dark)
    block(above: 16pt, below: 10pt)[#it.body]
  }

  show heading.where(level: 4): it => {
    set text(size: 11pt, weight: "bold", fill: text-dark)
    block(above: 12pt, below: 8pt)[#it.body]
  }

  // Lists
  set list(indent: 1em, body-indent: 0.5em)
  set enum(indent: 1em, body-indent: 0.5em)

  // Code styling
  show raw: set text(font: "SF Mono", size: 0.9em)

  show raw.where(block: true): it => {
    block(
      width: 100%,
      fill: luma(245),
      stroke: 0.5pt + text-gray,
      inset: 10pt,
      radius: 4pt,
      it,
    )
  }

  show raw.where(block: false): set text(fill: accent)

  // Tables
  set table(
    stroke: (x, y) => if y == 0 {
      (bottom: 1pt + accent)
    } else {
      0.5pt + text-gray.lighten(70%)
    },
    inset: 8pt,
  )
  show table.cell.where(y: 0): set text(weight: "bold", fill: accent)

  // Links
  show link: set text(fill: accent)
  show link: underline

  // Title block
  align(left)[
    #text(size: 22pt, fill: accent, weight: "bold")[#title]
    #v(8pt)
    #if date != none [
      #text(size: 10pt, fill: text-gray)[#date]
      #v(4pt)
    ]
  ]

  v(8pt)
  pdf.artifact(line(length: 100%, stroke: 0.5pt + text-gray.lighten(40%)))
  v(12pt)

  doc
}

// -----------------------------------------------------------------------------
// PANDOC TEMPLATE VARIABLES
// -----------------------------------------------------------------------------

#let title = $if(title)$[$title$]$else$[Document]$endif$
#let date = $if(date)$"$date$"$else$none$endif$

#show: inherent-doc.with(
  title: title,
  date: date,
)

$body$
