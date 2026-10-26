"""Render the whole brand icon library to PNG via headless browser (Playwright).

Source of truth: ../../brand-icon-lib.js (the console's library, every path `currentColor`).
Renders each icon at 512px on a transparent background into ../icons_png/ (generated, gitignored):
   - {name}.png        — Cybele brand blue #0A74D6
   - {name}_white.png  — white (for dark cards)

Run once after cloning, and again whenever the library changes:  python render_icons.py
Used by the pptxgenjs decks (build_deck.js) and by ../build_pptx.py.
"""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent   # deckgen/
LIB = ROOT.parent / "brand-icon-lib.js"          # web-app/brand-icon-lib.js
DST = ROOT / "icons_png"
DST.mkdir(exist_ok=True)
SIZE = 512

BRAND_BLUE = "#0A74D6"  # Brandbook-official primary


def load_icons():
    src = LIB.read_text(encoding="utf-8")
    # the file holds several `window.X = {...};` statements; the icons are the first object
    icons, _ = json.JSONDecoder().raw_decode(src[src.index("{"):])
    return icons


def colorize(svg_text, color):
    return svg_text.replace("currentColor", color)


def render_svg_to_png(page, svg_text, out_path):
    html = f"""<!DOCTYPE html><html><head><style>
    *{{margin:0;padding:0}}
    body{{background:transparent}}
    #wrap{{width:{SIZE}px;height:{SIZE}px;display:flex;align-items:center;justify-content:center}}
    #wrap svg{{width:100%;height:100%}}
    </style></head><body><div id="wrap">{svg_text}</div></body></html>"""
    page.set_content(html)
    page.locator("#wrap").screenshot(path=str(out_path), omit_background=True)


icons = load_icons()
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": SIZE, "height": SIZE})
    for i, (name, svg) in enumerate(sorted(icons.items()), 1):
        render_svg_to_png(page, colorize(svg, BRAND_BLUE), DST / f"{name}.png")
        render_svg_to_png(page, colorize(svg, "#FFFFFF"), DST / f"{name}_white.png")
        if i % 50 == 0:
            print(f"  {i}/{len(icons)}")
    browser.close()
print(f"\nOK · {len(icons)} icons × 2 variants = {len(icons) * 2} PNGs at {SIZE}×{SIZE} in {DST}")
