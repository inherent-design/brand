// Document components: cover-page, contact-strip, registration-block, invoice-header, line-items-table

#import "tokens.typ": sp-xs, sp-sm, sp-md, sp-lg, sp-xl, sp-2xl, sp-3xl, ts-display, ts-h1, ts-h2, ts-body, ts-small, ts-caption, border-thin, border-medium, border-thick, radius-md
#import "colors.typ": accent, text-dark, text-gray, bg-subtle
#import "typography.typ": font-display

#let cover-page(
  title: [],
  subtitle: none,
  date: none,
  company: none,
  fill: white,
  accent-color: accent,
) = {
  page(
    margin: (x: 1.5in, top: 2.5in, bottom: 1.5in),
    header: none,
    footer: none,
    fill: fill,
  )[
    // Accent bar at top
    #place(top + left, dx: -1.5in, dy: -2.5in)[
      #rect(width: 100% + 3in, height: 6pt, fill: accent-color)
    ]

    // Title block
    #text(
      font: font-display,
      size: ts-display + 8pt,
      weight: "bold",
      fill: text-dark,
    )[#title]

    #if subtitle != none {
      v(sp-md)
      text(size: ts-h2, fill: text-gray)[#subtitle]
    }

    #v(sp-xl)
    #line(length: 100pt, stroke: border-thick + accent-color)

    #if date != none {
      v(sp-xl)
      text(size: ts-body, fill: text-gray)[#date]
    }

    // Company name at bottom
    #if company != none {
      align(bottom + left)[
        #text(size: 12pt, fill: text-gray)[#company]
      ]
    }
  ]
}

#let contact-strip(
  name: none,
  title: none,
  email: none,
  phone: none,
  address: none,
  separator: [ | ],
) = {
  block(
    width: 100%,
    inset: (y: sp-sm),
  )[
    #set text(size: ts-small, fill: text-gray)
    #{
      let parts = ()
      if name != none { parts.push(text(weight: "bold", fill: text-dark)[#name]) }
      if title != none { parts.push(title) }
      if email != none { parts.push(link("mailto:" + email)[#email]) }
      if phone != none { parts.push(phone) }
      if address != none { parts.push(address) }
      parts.join(separator)
    }
  ]
}

#let registration-block(
  uei: none,
  cage: none,
  sam: none,
  naics-primary: none,
  naics-secondary: none,
  certifications: none,
  ein-last4: none,
) = {
  block(
    width: 100%,
    fill: bg-subtle,
    radius: radius-md,
    inset: sp-md,
    below: sp-md,
  )[
    #text(size: 11pt, weight: "bold", fill: accent)[Federal Registration]
    #v(sp-sm)
    #grid(
      columns: (auto, 1fr),
      row-gutter: sp-sm,
      column-gutter: sp-md,
      ..{
        let pairs = ()
        if uei != none { pairs.push((strong[UEI:], uei)) }
        if cage != none { pairs.push((strong[CAGE Code:], cage)) }
        if sam != none { pairs.push((strong[SAM.gov:], sam)) }
        if naics-primary != none { pairs.push((strong[NAICS (Primary):], naics-primary)) }
        if naics-secondary != none { pairs.push((strong[NAICS (Secondary):], naics-secondary)) }
        if certifications != none { pairs.push((strong[Certifications:], certifications)) }
        if ein-last4 != none { pairs.push((strong[EIN (last 4):], ein-last4)) }
        pairs.flatten()
      },
    )
  ]
}

#let invoice-header(
  company: none,
  client: none,
  number: none,
  date: none,
  due: none,
  po-number: none,
) = {
  grid(
    columns: (1fr, auto),
    column-gutter: sp-xl,

    // Left: company identity
    {
      if company != none {
        text(size: 14pt, weight: "bold", fill: accent)[#company.at("name", default: "")]
        v(sp-xs)
        if "address" in company {
          text(size: ts-small, fill: text-gray)[#company.address]
        }
        if "email" in company {
          v(sp-xs)
          text(size: ts-small, fill: text-gray)[#company.email]
        }
        if "phone" in company {
          v(sp-xs)
          text(size: ts-small, fill: text-gray)[#company.phone]
        }
      }
    },

    // Right: invoice metadata
    {
      text(size: ts-h1, weight: "bold", fill: accent)[INVOICE]
      v(sp-sm)
      grid(
        columns: (auto, auto),
        row-gutter: sp-xs,
        column-gutter: sp-md,
        text(size: ts-small, weight: "bold")[Invoice \#:], text(size: ts-small)[#number],
        text(size: ts-small, weight: "bold")[Date:], text(size: ts-small)[#date],
        text(size: ts-small, weight: "bold")[Due:], text(size: ts-small)[#due],
        ..if po-number != none {
          (text(size: ts-small, weight: "bold")[PO \#:], text(size: ts-small)[#po-number])
        } else { () },
      )
    },
  )

  v(sp-lg)

  // Client: "Bill To" section
  if client != none {
    text(size: ts-small, weight: "bold", fill: text-gray)[BILL TO]
    v(sp-xs)
    text(size: ts-body)[#client.at("name", default: "")]
    if "address" in client {
      v(sp-xs)
      text(size: ts-small, fill: text-gray)[#client.address]
    }
  }

  v(sp-lg)
  line(length: 100%, stroke: border-thin + text-gray.lighten(40%))
  v(sp-md)
}

#let line-items-table(
  items,
  tax-rate: none,
  tax-label: "Tax",
  currency: "$",
  show-quantity: true,
) = {
  // Calculate totals
  let subtotal = items.fold(0, (acc, item) => acc + item.at("amount", default: 0))
  let tax-amount = if tax-rate != none { subtotal * tax-rate } else { 0 }
  let total = subtotal + tax-amount

  // Format currency
  let fmt(n) = {
    currency + str(calc.round(n, digits: 2))
  }

  // Header + items
  table(
    columns: if show-quantity {
      (1fr, auto, auto, auto)
    } else {
      (1fr, auto)
    },
    inset: sp-sm,
    stroke: (x, y) => if y == 0 {
      (bottom: border-medium + accent)
    } else {
      (bottom: border-thin + text-gray.lighten(70%))
    },

    // Header row
    ..if show-quantity {
      (
        table.cell(text(weight: "bold", size: ts-small)[Description]),
        table.cell(text(weight: "bold", size: ts-small)[Qty]),
        table.cell(text(weight: "bold", size: ts-small)[Rate]),
        table.cell(text(weight: "bold", size: ts-small, fill: text-dark)[Amount]),
      )
    } else {
      (
        table.cell(text(weight: "bold", size: ts-small)[Description]),
        table.cell(text(weight: "bold", size: ts-small, fill: text-dark)[Amount]),
      )
    },

    // Item rows
    ..items.map(item => {
      if show-quantity {
        (
          text(size: ts-body)[#item.description],
          align(right, text(size: ts-small)[#item.at("quantity", default: 1)]),
          align(right, text(size: ts-small)[#fmt(item.at("rate", default: 0))]),
          align(right, text(size: ts-body, weight: "medium")[#fmt(item.amount)]),
        )
      } else {
        (
          text(size: ts-body)[#item.description],
          align(right, text(size: ts-body, weight: "medium")[#fmt(item.amount)]),
        )
      }
    }).flatten(),
  )

  // Totals section
  v(sp-sm)
  align(right)[
    #grid(
      columns: (auto, 6em),
      row-gutter: sp-xs,
      column-gutter: sp-lg,
      text(size: ts-small, fill: text-gray)[Subtotal:],
      align(right, text(size: ts-body)[#fmt(subtotal)]),
      ..if tax-rate != none {
        (
          text(size: ts-small, fill: text-gray)[#tax-label (#str(calc.round(tax-rate * 100, digits: 2))%):],
          align(right, text(size: ts-body)[#fmt(tax-amount)]),
        )
      } else { () },
    )
    #v(sp-xs)
    #line(length: 10em, stroke: border-thin + text-gray.lighten(40%))
    #v(sp-xs)
    #grid(
      columns: (auto, 6em),
      column-gutter: sp-lg,
      text(size: 12pt, weight: "bold")[Total:],
      align(right, text(size: 12pt, weight: "bold", fill: accent)[#fmt(total)]),
    )
  ]
}
