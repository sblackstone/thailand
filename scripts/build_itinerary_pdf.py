#!/usr/bin/env python3
"""
Render site/index.html to a print-ready PDF.

The web page and the PDF are the SAME document. index.html is the single
source of truth; this script adapts it for paper:
  - swaps the Google Fonts <link> for locally embedded @font-face rules
  - strips the scroll-reveal <script> (WeasyPrint runs no JS, so without
    this every .reveal element would render invisible)
  - converts CSS grid to flex (WeasyPrint's grid support is partial)
  - adds @page sizing and break-inside rules

Run:  python3 scripts/build_itinerary_pdf.py
Out:  site/Thailand-Itinerary-Nov2026.pdf
"""
import re
import pathlib
import sys

from fonts import ensure_fonts, font_face_css

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "site" / "index.html"
OUT = ROOT / "site" / "Thailand-Itinerary-Nov2026.pdf"

# Adapts the screen layout for paper. Keep the palette and type alone --
# the PDF is meant to look like the web page, not like a document.
PRINT_CSS = r"""
@page { size: letter; margin: 14mm 13mm 16mm; }

/* Background must sit on <html> so the dark field bleeds to every page
   edge. On <body> it only paints the first page. */
html{
  background:
    radial-gradient(1100px 650px at 84% 2%, rgba(230,172,67,0.11), transparent 58%),
    radial-gradient(900px 620px at 4% 96%, rgba(70,191,176,0.10), transparent 55%),
    var(--bg);
}
body{ background:none; overflow:visible }
.wrap{ max-width:none; padding:0 }
.hero{ padding:2px 0 20px }
.region{ padding:24px 0 4px }
.foot{ padding:32px 0 6px; margin-top:24px }

/* No JS on paper, so force the reveal animation's end state. */
.reveal{ opacity:1 !important; transform:none !important }

/* grid -> flex */
.card{ display:flex }
.datecol{ flex:0 0 96px }
.body{ flex:1 1 auto; min-width:0 }
.ticket{ display:flex }
.t-left{ flex:1 1 auto; min-width:0 }
.t-right{ flex:0 0 190px }
.tips{ display:flex; flex-wrap:wrap; gap:16px 30px }
.tip{ flex:0 0 45%; max-width:45% }
.cal{ display:grid; grid-template-columns:repeat(7,1fr); gap:5px }
.cal-day,.cal-pad{ min-height:66px }

/* Keep whole components together across page breaks. */
.card,.ticket,.ticket-zone,.transfer,.tip,.note,.day,.cal{ break-inside:avoid }
.region-head{ break-inside:avoid; break-after:avoid }
.region-desc{ break-after:avoid }
h1,h2,h3{ break-after:avoid }
"""


def build() -> pathlib.Path:
    if not SRC.exists():
        sys.exit(f"Missing {SRC}")

    ensure_fonts()
    html = SRC.read_text()

    # Remote fonts -> embedded. The sandbox can't reach fonts.googleapis.com,
    # and an unembedded PDF would silently fall back to DejaVu.
    html = re.sub(r'<link rel="preconnect"[^>]*>\s*', "", html)
    html = re.sub(r'<link href="https://fonts\.googleapis[^>]*>\s*', "", html)
    html = html.replace("<style>", "<style>\n" + font_face_css() + "\n", 1)

    # WeasyPrint executes no JS; the reveal script would leave content hidden.
    html = re.sub(r"<script>.*?</script>", "", html, flags=re.DOTALL)

    html = html.replace("</style>", PRINT_CSS + "\n</style>", 1)

    if 'name="author"' not in html:
        html = html.replace("<title>", '<meta name="author" content="Trip plan">\n<title>', 1)

    from weasyprint import HTML

    HTML(string=html, base_url=str(SRC.parent)).write_pdf(OUT)
    return OUT


if __name__ == "__main__":
    print(f"Wrote {build()}")
