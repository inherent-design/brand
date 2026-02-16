// Layout components: hero-section, two-column, sidebar-layout, card, card-grid

#import "tokens.typ": sp-xs, sp-sm, sp-md, sp-lg, sp-xl, sp-2xl, sp-3xl, ts-display, ts-body, border-thin, border-thick, radius-md
#import "colors.typ": accent, text-dark, text-gray, bg-card, border
#import "typography.typ": font-display

#let hero-section(
  title: [],
  subtitle: none,
  accent-line: true,
  fill: accent.lighten(92%),
  text-fill: text-dark,
) = {
  block(
    width: 100%,
    fill: fill,
    inset: (x: sp-2xl, top: sp-3xl, bottom: sp-2xl),
    below: sp-xl,
  )[
    #text(
      font: font-display,
      size: ts-display,
      fill: text-fill,
      weight: "bold",
    )[#title]
    #if subtitle != none {
      v(sp-sm)
      text(size: ts-body + 2pt, fill: text-gray)[#subtitle]
    }
    #if accent-line {
      v(sp-md)
      line(length: 80pt, stroke: border-thick + accent)
    }
  ]
}

#let two-column(
  left,
  right,
  ratio: (2fr, 1fr),
  gutter: sp-xl,
) = {
  grid(
    columns: ratio,
    column-gutter: gutter,
    left,
    right,
  )
}

#let sidebar-layout(
  main,
  sidebar,
  sidebar-width: 2.2in,
  gutter: sp-xl,
  sidebar-position: "right",
) = {
  let cols = if sidebar-position == "left" {
    (sidebar-width, 1fr)
  } else {
    (1fr, sidebar-width)
  }
  let cells = if sidebar-position == "left" {
    (sidebar, main)
  } else {
    (main, sidebar)
  }
  grid(
    columns: cols,
    column-gutter: gutter,
    ..cells,
  )
}

#let card(body, title: none, fill: bg-card, stroke: border-thin + border) = {
  block(
    width: 100%,
    fill: fill,
    stroke: stroke,
    radius: radius-md,
    inset: sp-md,
    above: sp-sm,
    below: sp-sm,
  )[
    #if title != none {
      text(weight: "bold", size: 11pt)[#title]
      v(sp-xs)
    }
    #body
  ]
}

#let card-grid(
  cards,
  columns: 3,
  gutter: sp-md,
) = {
  grid(
    columns: (1fr,) * columns,
    column-gutter: gutter,
    row-gutter: gutter,
    ..cards,
  )
}
