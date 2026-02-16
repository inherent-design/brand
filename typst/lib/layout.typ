// Page setup, margins, header/footer

#import "colors.typ": text-gray
#import "tokens.typ": ts-small, border-thin, sp-xs

#let apply-layout(title: [], date: none, doc) = {
  set page(
    paper: "us-letter",
    margin: (top: 1in, bottom: 1in, left: 1in, right: 1in),
    header: context {
      if counter(page).get().first() > 1 {
        set text(size: ts-small, fill: text-gray)
        grid(
          columns: (1fr, auto),
          [inherent.design],
          if date != none [#date],
        )
        v(-8pt)
        line(length: 100%, stroke: border-thin + text-gray.lighten(60%))
      }
    },
    footer: context {
      set text(size: ts-small, fill: text-gray)
      line(length: 100%, stroke: border-thin + text-gray.lighten(60%))
      v(sp-xs)
      grid(
        columns: (1fr, auto),
        [inherent.design],
        [Page #counter(page).display("1 of 1", both: true)],
      )
    },
  )

  doc
}
