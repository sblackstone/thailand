# Thailand — November 2026

Itinerary for a 14-day trip, 1–14 November 2026. Published with GitHub Pages.

**Live site:** `https://<username>.github.io/<repo>/`

## Quick start

```bash
pip install weasyprint          # needs npm on PATH for the font fetch
python3 scripts/build_itinerary_pdf.py
python3 scripts/build_calendar.py
```

Fonts download once into `scripts/fonts/` (gitignored) and are cached after that.

## What's here

| File | |
|---|---|
| `site/index.html` | The itinerary. Source of truth — edit this. |
| `site/*.pdf` | Generated. Don't hand-edit. |
| `scripts/build_itinerary_pdf.py` | Renders `index.html` for print. |
| `scripts/build_calendar.py` | One-page landscape calendar (own trip data). |
| `DESIGN.md` | Design system + renderer quirks. **Read before visual edits.** |
| `CLAUDE.md` | Standing instructions for Claude Code / Cowork sessions. |

## Publishing

Settings → Pages → Deploy from a branch → `main` / `/site`.
(If Pages is set to repo root instead, move the contents of `site/` up a level.)

## Printing the calendar

Landscape, **background graphics enabled**. Without it the region colours and
the diagonal split cells vanish — which is most of the information design.
