# Generates the Cybele Design Console app icon (cybele_icon.ico):
# the brand butterfly in WHITE, optically centered (by centre of mass), on a rounded square with a
# 20/60/20 gradient (accent violet -> brand blue -> accent mint) plus a glass sheen — Adobe CC style.
#
# Pipeline: extract the 4 butterfly paths from the logo -> recolour white -> render butterfly alone to
# find its centroid -> render the final icon (gradient + glass + optically-centred butterfly) with
# headless Chrome -> round the corners + build the multi-size .ico with Pillow.
import os, re, subprocess, tempfile
from PIL import Image, ImageDraw

BASE = os.path.dirname(os.path.abspath(__file__))  # portable: this script's folder
LOGO = os.path.join(BASE, "data", "brand-assets", "cybele-logo.svg")
ICO  = os.path.join(BASE, "cybele_icon.ico")
PNG  = os.path.join(BASE, "cybele_icon.png")
# Headless Chrome (Windows default install path); override if Chrome lives elsewhere
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# Colours that identify the butterfly paths in the logo (NOT the icon background)
WING_COLORS = ["#0A74D6", "#FFA91F", "#66C44F", "#F34620"]
# Icon background gradient (diagonal TL->BR): 20/60/20 — accent violet corner, brand blue centre,
# accent mint corner. Violet sits at the opposite end from the green.
BG_STOPS = [(0.0, "#8878ED"), (0.20, "#0A74D6"), (0.80, "#0A74D6"), (1.0, "#3DCCA1")]
S = 512                      # render size
RADIUS = int(S * 0.225)      # rounded-square corner radius
GLYPH_FRAC = 0.72            # butterfly size as a fraction of the canvas
NUDGE_X, NUDGE_Y = 0.012, -0.028  # optical fine-tune: slight up (butterfly reads bottom-heavy)
tmp = tempfile.mkdtemp()

def render_svg(svg, out_png):
    html = ("<!doctype html><html><head><meta charset='utf-8'><style>"
            "html,body{margin:0;padding:0;background:transparent}svg{display:block}</style></head><body>"
            + svg + "</body></html>")
    hp = os.path.join(tmp, "r.html")
    open(hp, "w", encoding="utf-8").write(html)
    subprocess.run([
        CHROME, "--headless=new", "--disable-gpu", "--no-first-run", "--hide-scrollbars",
        "--user-data-dir=" + os.path.join(tmp, "profile"),
        "--force-device-scale-factor=1", f"--window-size={S},{S}",
        f"--screenshot={out_png}", "file:///" + hp.replace("\\", "/"),
    ], check=True, timeout=90)

# ── 1. Extract the four coloured butterfly paths ──
svg_src = open(LOGO, encoding="utf-8").read()
paths = []
for m in re.finditer(r"<path\b[^>]*?\bd=\"([^\"]*)\"[^>]*?>", svg_src):
    tag, d = m.group(0), m.group(1)
    fm = re.search(r'fill="([^"]*)"', tag)
    if fm and any(c.lower() in fm.group(1).lower() for c in WING_COLORS):
        paths.append(d)

# ── 2. Butterfly bounding box (parse commands so single-param H/V map to the right axis) ──
def path_xy(d):
    xs, ys = [], []
    for cmd, params in re.findall(r"([A-Za-z])([^A-Za-z]*)", d):
        nums = [float(n) for n in re.findall(r"-?\d*\.?\d+(?:e-?\d+)?", params)]
        c = cmd.upper()
        if c in ("M", "L", "T", "C", "S", "Q"):
            for i in range(0, len(nums) - 1, 2):
                xs.append(nums[i]); ys.append(nums[i + 1])
        elif c == "H": xs.extend(nums)
        elif c == "V": ys.extend(nums)
        elif c == "A":
            for i in range(0, len(nums) - 6, 7):
                xs.append(nums[i + 5]); ys.append(nums[i + 6])
    return xs, ys

xs, ys = [], []
for d in paths:
    px, py = path_xy(d); xs += px; ys += py
bx0, bx1, by0, by1 = min(xs), max(xs), min(ys), max(ys)
bw, bh = bx1 - bx0, by1 - by0
cx, cy = (bx0 + bx1) / 2, (by0 + by1) / 2
scale = (S * GLYPH_FRAC) / max(bw, bh)
white_paths = "".join(f'<path d="{d}" fill="#ffffff"/>' for d in paths)

def butterfly_group(tx, ty):
    return f'<g transform="translate({tx} {ty}) scale({scale:.5f}) translate({-cx} {-cy})">{white_paths}</g>'

# ── 3. Render butterfly alone (bbox-centred) and find its centre of mass ──
fly_png = os.path.join(tmp, "fly.png")
render_svg(f'<svg width="{S}" height="{S}" viewBox="0 0 {S} {S}" xmlns="http://www.w3.org/2000/svg">'
           f'{butterfly_group(S/2, S/2)}</svg>', fly_png)
alpha = Image.open(fly_png).convert("RGBA").split()[3]
data = alpha.load()
sx = sy = sw = 0
for y in range(S):
    for x in range(S):
        v = data[x, y]
        if v > 10:
            sx += x * v; sy += y * v; sw += v
mass_x, mass_y = sx / sw, sy / sw
# Shift so the centre of mass lands at the canvas centre (+ optional manual nudge)
tx = S / 2 + (S / 2 - mass_x) + NUDGE_X * S
ty = S / 2 + (S / 2 - mass_y) + NUDGE_Y * S

# ── 4. Final icon: gradient background + glass effect + optically-centred white butterfly ──
grad = "".join(f'<stop offset="{o:.3f}" stop-color="{c}"/>' for o, c in BG_STOPS)
final = (
    f'<svg width="{S}" height="{S}" viewBox="0 0 {S} {S}" xmlns="http://www.w3.org/2000/svg">'
    f'<defs>'
    f'<linearGradient id="bg" x1="0" y1="0" x2="{S}" y2="{S}" gradientUnits="userSpaceOnUse">{grad}</linearGradient>'
    # glossy top light, soft top-left glow, faint bottom shade — the "glass" sheen
    f'<linearGradient id="sheen" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="#ffffff" stop-opacity="0.32"/>'
    f'<stop offset="0.46" stop-color="#ffffff" stop-opacity="0.05"/>'
    f'<stop offset="1" stop-color="#ffffff" stop-opacity="0"/></linearGradient>'
    f'<radialGradient id="glow" cx="0.26" cy="0.16" r="0.85">'
    f'<stop offset="0" stop-color="#ffffff" stop-opacity="0.38"/>'
    f'<stop offset="0.55" stop-color="#ffffff" stop-opacity="0"/></radialGradient>'
    f'<linearGradient id="shade" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0.62" stop-color="#000000" stop-opacity="0"/>'
    f'<stop offset="1" stop-color="#000000" stop-opacity="0.13"/></linearGradient>'
    f'</defs>'
    f'<rect x="0" y="0" width="{S}" height="{S}" fill="url(#bg)"/>'
    f'<rect x="0" y="0" width="{S}" height="{S}" fill="url(#shade)"/>'
    f'<rect x="0" y="0" width="{S}" height="{S}" fill="url(#glow)"/>'
    f'<rect x="0" y="0" width="{S}" height="{S}" fill="url(#sheen)"/>'
    f'{butterfly_group(tx, ty)}'
    # glass rim catch-light (rounded to match the corner mask, inset so it isn't clipped)
    f'<rect x="2.5" y="2.5" width="{S - 5}" height="{S - 5}" rx="{RADIUS - 2}" ry="{RADIUS - 2}" '
    f'fill="none" stroke="#ffffff" stroke-opacity="0.22" stroke-width="2.5"/>'
    f'</svg>')
final_png = os.path.join(tmp, "final.png")
render_svg(final, final_png)

# ── 5. Round the corners + build the .ico ──
im = Image.open(final_png).convert("RGBA")
if im.size != (S, S):
    im = im.resize((S, S), Image.LANCZOS)
mask = Image.new("L", (S, S), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, S - 1, S - 1], radius=RADIUS, fill=255)
im.putalpha(mask)
im.save(PNG)
im.save(ICO, format="ICO", sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
print(f"Wrote {ICO}  | bbox-centre ({cx:.1f},{cy:.1f}) -> mass-centre px ({mass_x:.1f},{mass_y:.1f}) | shift px ({S/2-mass_x:+.1f},{S/2-mass_y:+.1f})")
