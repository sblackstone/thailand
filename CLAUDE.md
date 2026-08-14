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
scripts/
  fonts.py                        shared font fetch + @font-face
  build_itinerary_pdf.py          index.html -> PDF
  build_calendar.py               standalone one-page print calendar
```

`site/` is what GitHub Pages serves.

## The rule that matters most

**`site/index.html` is the source of truth. The PDFs are build artefacts.**

Never hand-edit a PDF or regenerate the itinerary from scratch. Edit the HTML,
then:

```bash
python3 scripts/build_itinerary_pdf.py
python3 scripts/build_calendar.py
```

The calendar is separate — it has its own trip data near the top of
`build_calendar.py` (the `trip` dict). Change a date or a hotel and you must
update **both** the HTML and that dict, or the two documents disagree.

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
