// Table styling (strokes, fills, header row)

#import "colors.typ": accent, text-gray
#import "tokens.typ": border-medium, border-thin, sp-sm

#let apply-tables(doc) = {
  set table(
    stroke: (x, y) => if y == 0 {
      (bottom: border-medium + accent)
    } else {
      border-thin + text-gray.lighten(70%)
    },
    inset: sp-sm,
  )

  show table.cell.where(y: 0): set text(weight: "bold", fill: accent)

  doc
}
