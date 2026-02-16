// Code/raw block styling

#import "colors.typ": accent, text-gray, bg-subtle
#import "typography.typ": font-code
#import "tokens.typ": border-thin, radius-md

#let apply-code(doc) = {
  show raw: set text(font: font-code, size: 0.9em)

  show raw.where(block: true): it => {
    block(
      width: 100%,
      fill: bg-subtle,
      stroke: border-thin + text-gray,
      inset: 10pt,
      radius: radius-md,
      it,
    )
  }

  show raw.where(block: false): set text(fill: accent)

  doc
}
