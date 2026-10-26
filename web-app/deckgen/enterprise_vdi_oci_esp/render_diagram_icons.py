"""Render the architecture-diagram icon set from the thinfinity-architecture skill SVGs
to PNG in three colorways (brand blue, dark, white) for use in pptxgenjs diagrams.
Output: ./diagram_icons/{name}.png (blue), {name}_dark.png, {name}_white.png
"""
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

SRC = Path(__file__).resolve().parents[3] / "skills" / "thinfinity-architecture" / "icons"   # repo root
DST = Path(__file__).parent / "diagram_icons"
DST.mkdir(exist_ok=True)
SIZE = 256

BLUE = "#0A74D6"  # Brandbook-official primary (was #0F7FE0; reconciled 2026-06-11)
DARK = "#2E2E2E"
WHITE = "#FFFFFF"

# concept -> skill svg stem
NEEDED = [
    "load-balancer", "gateway", "broker", "broker-monitor", "database",
    "windows", "server", "linux", "user", "user-group", "firewall",
    "fslogix", "thinfinity", "network", "app-group", "pc", "cloud",
    "oracle", "vdi", "html5", "remote", "refresh", "app-server", "app-virtualization",
]


def colorize(svg_text, target):
    svg_text = re.sub(r'(<svg[^>]*?)fill="none"', rf'\1fill="{target}"', svg_text, count=1)
    svg_text = re.sub(r'fill="#[0-9A-Fa-f]{3,6}"', f'fill="{target}"', svg_text)
    svg_text = re.sub(r'stroke="#[0-9A-Fa-f]{3,6}"', f'stroke="{target}"', svg_text)
    return svg_text


def render(page, svg_text, out_path):
    html = f"""<!DOCTYPE html><html><head><style>
    *{{margin:0;padding:0}} body{{background:transparent}}
    #wrap{{width:{SIZE}px;height:{SIZE}px;display:flex;align-items:center;justify-content:center}}
    #wrap svg{{width:90%;height:90%}}
    </style></head><body><div id="wrap">{svg_text}</div></body></html>"""
    page.set_content(html)
    page.set_viewport_size({"width": SIZE, "height": SIZE})
    page.locator("#wrap").screenshot(path=str(out_path), omit_background=True)


with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    n = 0
    for name in NEEDED:
        svg = SRC / f"{name}.svg"
        if not svg.exists():
            print(f"  MISSING {name}")
            continue
        text = svg.read_text(encoding="utf-8")
        render(page, colorize(text, BLUE), DST / f"{name}.png")
        render(page, colorize(text, DARK), DST / f"{name}_dark.png")
        render(page, colorize(text, WHITE), DST / f"{name}_white.png")
        n += 1
        print(f"  {name}")
    browser.close()
    print(f"\nOK · {n} icons × 3 = {n*3} PNGs at {SIZE}px in {DST}")
