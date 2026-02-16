// brand/typst/inherent.typ: Base template for inherent.design documents
//
// Pure Typst entry point. Templates use: #show: base-template.with(title: ..., date: ...)

#import "lib/colors.typ": *
#import "lib/tokens.typ": *
#import "lib/typography.typ": apply-typography
#import "lib/layout.typ": apply-layout
#import "lib/tables.typ": apply-tables
#import "lib/code.typ": apply-code

#let base-template(
  title: "",
  date: none,
  body,
) = {
  show: apply-typography
  show: apply-layout.with(title: title, date: date)
  show: apply-tables
  show: apply-code
  body
}
