// Content components: metric-card, service-card, competency-block, callout-box, pull-quote

#import "tokens.typ": sp-xs, sp-sm, sp-md, sp-lg, sp-xl, ts-h1, ts-h2, ts-h3, ts-h4, ts-body, ts-caption, border-thin, radius-md
#import "colors.typ": accent, text-dark, text-gray, bg-subtle, success, warning, error, info

#let metric-card(
  value,
  label,
  description: none,
  fill: accent.lighten(92%),
  value-color: accent,
) = {
  block(
    width: 100%,
    fill: fill,
    radius: radius-md,
    inset: sp-md,
  )[
    #text(size: ts-h1, weight: "bold", fill: value-color)[#value]
    #v(sp-xs)
    #text(size: ts-h4, weight: "semibold", fill: text-dark)[#label]
    #if description != none {
      v(sp-xs)
      text(size: ts-caption, fill: text-gray)[#description]
    }
  ]
}

#let service-card(
  name,
  description,
  deliverables: (),
  accent-color: accent,
) = {
  block(
    width: 100%,
    stroke: (left: 3pt + accent-color, rest: border-thin + text-gray.lighten(70%)),
    radius: (right: radius-md),
    inset: sp-md,
    below: sp-md,
  )[
    #text(size: ts-h3, weight: "bold", fill: accent-color)[#name]
    #v(sp-sm)
    #text(fill: text-dark)[#description]
    #if deliverables.len() > 0 {
      v(sp-sm)
      text(size: ts-caption, weight: "bold", fill: text-gray)[Deliverables:]
      for item in deliverables {
        v(sp-xs)
        grid(
          columns: (12pt, 1fr),
          column-gutter: sp-xs,
          text(fill: accent-color)[--],
          text(size: ts-caption)[#item],
        )
      }
    }
  ]
}

#let competency-block(
  title,
  items,
  accent-color: accent,
  columns: 2,
) = {
  block(below: sp-lg)[
    #text(size: ts-h3, weight: "bold", fill: accent-color)[#title]
    #v(sp-sm)
    #grid(
      columns: (1fr,) * columns,
      column-gutter: sp-lg,
      row-gutter: sp-sm,
      ..items.map(item => {
        grid(
          columns: (8pt, 1fr),
          column-gutter: sp-xs,
          align(horizon, circle(radius: 3pt, fill: accent-color)),
          text(size: ts-body, fill: text-dark)[#item],
        )
      }),
    )
  ]
}

#let callout-box(
  body,
  title: none,
  variant: "info",
  icon: none,
) = {
  let (fill, stroke-color, title-color) = if variant == "info" {
    (info.lighten(90%), info, info)
  } else if variant == "warning" {
    (warning.lighten(88%), warning, warning)
  } else if variant == "success" {
    (success.lighten(90%), success, success)
  } else if variant == "error" {
    (error.lighten(90%), error, error)
  } else {
    (bg-subtle, text-gray, text-dark)
  }

  block(
    width: 100%,
    fill: fill,
    stroke: (left: 3pt + stroke-color, rest: none),
    radius: (right: radius-md),
    inset: sp-md,
    above: sp-md,
    below: sp-md,
  )[
    #if title != none {
      text(weight: "bold", fill: title-color, size: ts-body)[
        #if icon != none [#icon ] #title
      ]
      v(sp-xs)
    }
    #body
  ]
}

// Preset variants via .with()
#let info-box = callout-box.with(variant: "info")
#let warning-box = callout-box.with(variant: "warning")
#let success-box = callout-box.with(variant: "success")
#let error-box = callout-box.with(variant: "error")
#let note-box = callout-box.with(variant: "note", title: "Note")
#let tip-box = callout-box.with(variant: "info", title: "Tip")
#let important-box = callout-box.with(variant: "warning", title: "Important")

#let pull-quote(
  body,
  attribution: none,
  accent-color: accent,
) = {
  block(
    width: 100%,
    inset: (left: sp-xl, right: sp-lg, y: sp-lg),
    above: sp-lg,
    below: sp-lg,
  )[
    #block(
      stroke: (left: 3pt + accent-color),
      inset: (left: sp-md),
    )[
      #text(
        size: ts-h2,
        style: "italic",
        fill: text-dark,
        weight: "regular",
      )[#body]
    ]
    #if attribution != none {
      v(sp-sm)
      align(right)[
        #text(size: ts-body, fill: text-gray)[--- #attribution]
      ]
    }
  ]
}
