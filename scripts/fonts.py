#!/usr/bin/env python3
"""
Font handling shared by both build scripts.

Why this exists: the design uses Fraunces, Instrument Sans and IBM Plex Mono.
Google Fonts is fine for the web page, but a PDF renderer needs the actual
font files on disk or it silently falls back to DejaVu and the design breaks.

We pull them from the @fontsource npm packages (npmjs.org is reachable from
sandboxes where fonts.googleapis.com is not). Files land in scripts/fonts/
and are gitignored -- run once per machine and they're cached.
"""
import pathlib
import subprocess
import sys

FONT_DIR = pathlib.Path(__file__).resolve().parent / "fonts"
PKG_DIR = FONT_DIR / "node_modules" / "@fontsource"

PACKAGES = [
    "@fontsource/fraunces",
    "@fontsource/instrument-sans",
    "@fontsource/ibm-plex-mono",
]

# (family, style, weight, package, filename)
FACES = [
    ("Fraunces", "normal", 400, "fraunces", "fraunces-latin-400-normal.woff2"),
    ("Fraunces", "normal", 500, "fraunces", "fraunces-latin-500-normal.woff2"),
    ("Fraunces", "italic", 400, "fraunces", "fraunces-latin-400-italic.woff2"),
    ("Fraunces", "italic", 500, "fraunces", "fraunces-latin-500-italic.woff2"),
    ("Instrument Sans", "normal", 400, "instrument-sans", "instrument-sans-latin-400-normal.woff2"),
    ("Instrument Sans", "normal", 500, "instrument-sans", "instrument-sans-latin-500-normal.woff2"),
    ("Instrument Sans", "normal", 600, "instrument-sans", "instrument-sans-latin-600-normal.woff2"),
    ("IBM Plex Mono", "normal", 400, "ibm-plex-mono", "ibm-plex-mono-latin-400-normal.woff2"),
    ("IBM Plex Mono", "normal", 500, "ibm-plex-mono", "ibm-plex-mono-latin-500-normal.woff2"),
]


def _path(package: str, filename: str) -> pathlib.Path:
    return PKG_DIR / package / "files" / filename


def ensure_fonts() -> None:
    """Download the font files if they aren't already present."""
    if all(_path(p, f).exists() for *_, p, f in FACES):
        return

    print("Fetching fonts via npm (one-time)...")
    FONT_DIR.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["npm", "init", "-y"], cwd=FONT_DIR, check=True,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    subprocess.run(
        ["npm", "install", *PACKAGES], cwd=FONT_DIR, check=True,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

    missing = [f for *_, p, f in FACES if not _path(p, f).exists()]
    if missing:
        sys.exit(f"Fonts failed to download: {missing}")


def font_face_css() -> str:
    """@font-face rules pointing at the local files, for embedding in a PDF."""
    return "\n".join(
        f"@font-face{{font-family:'{fam}';font-style:{style};font-weight:{wt};"
        f"font-display:swap;src:url('file://{_path(pkg, fn)}') format('woff2')}}"
        for fam, style, wt, pkg, fn in FACES
    )


if __name__ == "__main__":
    ensure_fonts()
    print(f"Fonts ready in {PKG_DIR}")
