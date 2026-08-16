# Working in this repo

A travel itinerary for Thailand, 1–14 November 2026, published to GitHub Pages.
Two travellers: Stephen and Doug.

## Read first

**`DESIGN.md` before touching anything visual.** The design system is
deliberate and documented. Match it; don't restyle. It also lists the
renderer quirks that cause silent, invisible failures — worth reading even
for a small change.

## Structure

```
site/
  index.html                      the itinerary — SINGLE SOURCE OF TRUTH
  Thailand-Itinerary-Nov2026.pdf  generated
  Thailand-Calendar-Nov2026.pdf   generated
  Thailand-Dossier-Nov2026.pdf    generated
scripts/
  fonts.py                        shared font fetch + @font-face
  build_itinerary_pdf.py          index.html -> PDF
  build_calendar.py               standalone one-page print calendar
  build_dossier.py                standalone long-form agent-style dossier
```

`site/` is what GitHub Pages serves.

## The rule that matters most

**`site/index.html` is the source of truth. The PDFs are build artefacts.**

Never hand-edit a PDF or regenerate the itinerary from scratch. Edit the HTML,
then:

```bash
python3 scripts/build_itinerary_pdf.py
python3 scripts/build_calendar.py
python3 scripts/build_dossier.py
```

**Two documents carry their own copy of the trip data.** The calendar has a
`trip` dict near the top of `build_calendar.py`; the dossier has `DAYS` and
`VOUCHERS` in `build_dossier.py`. Change a date, a hotel or a confirmation
reference and you must update the HTML *and* both of those, or the three
documents disagree with each other.

## Verify before committing

PDF rendering fails silently here. Always look at the output:

```bash
pdftoppm -png -r 110 site/Thailand-Calendar-Nov2026.pdf /tmp/cal
```

Check specifically: fonts embedded (not fallback serif), dark background
reaching every page edge on the itinerary, split cells showing two colours
on the calendar, no text overflowing its container.

## Publishing

Pages serves `site/` on push to `main`. Commit the regenerated PDFs — they're
tracked deliberately so the download links work.

## Conventions

- British-ish plain prose. No marketing voice, no exclamation marks.
- All times 24-hour. Flight numbers, confirmation refs and station codes in mono.
- Confirmed bookings state the reference; unbooked items say so plainly.
- Uncertainty is stated, not smoothed over. If a detail needs confirming with
  a supplier, say which and why.

## Privacy

The published site contains booking references and flight numbers. It's a
public URL. Don't add passport numbers, card details, or addresses.
