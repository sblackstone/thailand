# Design system

This document exists so the look survives future edits. **The design is
deliberate, not a default.** If you're changing content, match what's here
rather than restyling.

---

## Type

| Role | Face | Notes |
|---|---|---|
| Display / headings | **Fraunces** | 400 and 500 only. Italic used for the accent half of headings (`<em>`, `.dash`). Never bold it — the weight comes from size. |
| Body | **Instrument Sans** | 400 / 500 / 600. |
| Data, labels, chips | **IBM Plex Mono** | Uppercase with wide tracking (`.1em`–`.26em`) for eyebrows and labels. All times, prices, refs and codes are mono. |

The mono-for-data rule is load-bearing: it's what makes times and confirmation
numbers scannable against the prose. Don't set a departure time in Instrument Sans.

Fonts come from `@fontsource` npm packages, not Google Fonts — see
[Environment quirks](#environment-quirks).

---

## Colour

### Web itinerary (`site/index.html`) — dark

```
--bg        #0E332E   deep jungle green, page field
--bg2       #0A2622   darker, card gradient base
--surface   #143F38   card fill
--rice      #F0EBDC   primary text (warm off-white, never pure #fff)
--rice-dim  #D3CFBF   secondary text
--muted     #8FA69F   labels, de-emphasised
--line      rgba(240,235,220,0.13)   hairlines
```

### Region accents — used in BOTH documents

Each region owns a colour. This is the backbone of the whole system: the
calendar, the route ribbon, the section headers and the day cards all key off it.

| Region | Var | Dark (web) | Light (print) |
|---|---|---|---|
| Bangkok | `--bangkok` | `#E6AC43` gold | `#F6CE85` |
| Chiang Mai | `--chiangmai` | `#DE8A4C` amber | `#F0A876` |
| Krabi | `--krabi` | `#46BFB0` teal | `#7ED8CB` |
| Khao Sok | `--khaosok` | `#69AB60` green | `#9BCE91` |

Sections set `--accent` to their region's colour and everything inside
(spine, bullets, chips, rules) inherits it. To add a region, add a colour —
don't reuse an existing one.

### Print calendar (`scripts/build_calendar.py`) — light

Inverted deliberately. Ink text `#15332C` on white, with the *light* region
tints above as cell fills. **Never make the printable calendar dark.**

---

## Layout patterns

**Day cards on a spine.** Each region renders as a vertical rule with dotted
nodes; cards attach to it. The date column is a fixed 96px gutter, mono
day-of-week over a large Fraunces numeral.

**Chips.** Small mono pills for logistics (`STAY`, `FLY`, `TRAIN`, refs). The
key word is in `--accent`, the value in `--rice-dim`. Below a dashed divider,
separated from the prose.

**The ticket stub.** The sleeper-train block is the signature element: a
two-panel card with a dashed perforation, notch cutouts, and a barcode.
It's intentionally the most designed thing in the document. Keep it.

**Transfer bars.** Dashed-border rows between regions, mode icon at left,
timing right-aligned. Deliberately lighter than day cards — they're connective
tissue, not destinations.

**Diagonal split cells (calendar).** A day where you wake in one region and
sleep in another is cut corner-to-corner at 135°: origin upper-left,
destination lower-right. Apply to every region change, not a subset — the
consistency is what makes it read as a system.

---

## Environment quirks

Hard-won. Ignoring these costs an hour each.

**1. Google Fonts is unreachable from the sandbox.** `fonts.googleapis.com`
isn't on the allowlist; `npmjs.org` is. Hence `@fontsource`. If a PDF renders
in a generic serif, the fonts didn't embed.

**2. WeasyPrint rejects modern multi-position gradient syntax.**

```css
/* SILENTLY FAILS -> renders white */
background: linear-gradient(135deg, #A 0 49%, #B 49% 100%);

/* WORKS */
background: linear-gradient(135deg, #A 0%, #A 49%, #B 49%, #B 100%);
```

This one is nasty because there's no error — the cell just goes blank.

**3. Put the page background on `<html>`, not `<body>`.** On `<body>` it
paints only page one and the rest come out white.

**4. WeasyPrint runs no JavaScript.** `index.html` uses an IntersectionObserver
for scroll reveals; elements start at `opacity:0`. The PDF build strips the
script AND forces `.reveal{opacity:1}` — drop either and the PDF is blank.

**5. CSS grid support is partial.** The PDF build converts cards and the
ticket to flex. Grid is fine for the 7-column calendar.

**6. Unicode glyphs not in these fonts render as tofu.** ★ (U+2605), ✈
(U+2708), 🚆 fall back badly. Use inline SVG icons, or a background tint to
signal state.

**7. The calendar must print landscape with background graphics enabled.**
Browsers strip background fills by default, which kills the region colours
and the split cells — the entire information design.

---

## Editing checklist

- Content changes go in `site/index.html`, then rerun both build scripts —
  the PDFs are generated, never hand-edited.
- Weekday labels appear in four places (day cards, region date ranges, the
  embedded calendar, the ticket). Change one, change all. **Nov 1 2026 is a
  Sunday** — an early draft had this wrong and it propagated everywhere.
- After any PDF change, rasterise and actually look at it:
  `pdftoppm -png -r 110 file.pdf out` — silent layout failures are the norm here.
