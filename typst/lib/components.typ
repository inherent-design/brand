#import "colors.typ": accent, text-gray
#import "typography.typ": font-display
#import "tokens.typ": ts-h1, ts-body, sp-xs, sp-sm, sp-md, border-thin

#let title-block(title: [], date: none) = {
  align(left)[
    #text(font: font-display, size: ts-h1, fill: accent, weight: "bold")[#title]
    #v(sp-sm)
    #if date != none [
      #text(size: ts-body, fill: text-gray)[#date]
      #v(sp-xs)
    ]
  ]
  v(sp-sm)
  pdf.artifact(line(length: 100%, stroke: border-thin + text-gray.lighten(40%)))
  v(sp-md)
}

#let info-table(..pairs) = {
  grid(
    columns: (auto, 1fr),
    row-gutter: sp-sm,
    column-gutter: sp-md,
    ..pairs.pos().map(((label, value)) => {
      (strong(label), value)
    }).flatten()
  )
}

#let signature-block(party-name, include-title: true) = {
  v(1em)
  strong(party-name)
  v(2em)
  grid(
    columns: (1fr, auto),
    column-gutter: 2em,
    [Name: #box(width: 12em, stroke: (bottom: border-thin))],
    [Date: #box(width: 6em, stroke: (bottom: border-thin))],
  )
  if include-title {
    v(1em)
    [Title: #box(width: 12em, stroke: (bottom: border-thin))]
  }
}

#let separator() = {
  pdf.artifact(line(length: 100%, stroke: border-thin + text-gray.lighten(40%)))
}

#import "components-layout.typ": *
#import "components-content.typ": *
#import "components-document.typ": *
