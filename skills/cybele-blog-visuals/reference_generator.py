"""
Build 6 blog cover variants for article:
"Telecom Contact Centers at Scale: A CIO's Strategy for VDI-Powered Customer Experience"

Each of the 6 covers expresses the SAME core concept — "VDI on OCI powering telecom
contact center agents at scale" — using a different visual metaphor, color family,
and composition.

Output: 6 SVG files (1840x1084) + preview.html
"""

import math
from pathlib import Path

OUT = Path(__file__).parent / "output"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1920, 1080

# ============================================================
# SHARED HELPERS
# ============================================================

def wrap(defs, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Inter, 'Segoe UI', Arial, sans-serif">
<defs>
{defs}
<filter id="soft-blur" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="30"/></filter>
<filter id="soft-glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="18"/></filter>
<filter id="ground-shadow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="14"/></filter>
</defs>
{body}
</svg>'''

def linear_grad(id_, stops, x1=0, y1=0, x2=0, y2=1):
    s = "\n".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<linearGradient id="{id_}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{s}</linearGradient>'

def radial_grad(id_, stops, cx=0.5, cy=0.5, r=0.5):
    s = "\n".join(f'<stop offset="{o}" stop-color="{c[0]}" stop-opacity="{c[1]}"/>' for o, c in stops)
    return f'<radialGradient id="{id_}" cx="{cx}" cy="{cy}" r="{r}">{s}</radialGradient>'

def rings(cx, cy, radii, stroke="#FFFFFF"):
    return "\n".join(
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{stroke}" stroke-width="2" stroke-opacity="{op}"/>'
        for r, op in radii
    )

def pill(x, y, w, h, text, bg="#0B1A3B", color="#FFFFFF", fs=22):
    r = h / 2
    return f'''<g>
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{bg}"/>
<text x="{x + w/2}" y="{y + h/2 + fs*0.35}" text-anchor="middle" fill="{color}" font-size="{fs}" font-weight="600">{text}</text>
</g>'''

def circle_badge(cx, cy, r, bg, icon_paths, icon_color="#FFFFFF", icon_scale=0.55):
    s = icon_scale * r / 50
    tx = cx - 50 * s
    ty = cy - 50 * s
    paths = "\n".join(f'<path d="{p}" fill="{icon_color}"/>' for p in icon_paths)
    return f'''<g>
<circle cx="{cx}" cy="{cy}" r="{r}" fill="{bg}"/>
<g transform="translate({tx},{ty}) scale({s})">{paths}</g>
</g>'''

# ============================================================
# ICON / SHAPE LIBRARY (100x100 viewbox)
# ============================================================

ICON = {
    'headset': ['M 20 55 Q 20 18 50 18 Q 80 18 80 55 L 80 65 L 72 65 L 72 52 Q 72 28 50 28 Q 28 28 28 52 L 28 65 L 20 65 Z M 15 60 L 30 60 L 30 85 L 15 85 Q 10 85 10 80 L 10 65 Q 10 60 15 60 Z M 70 60 L 85 60 Q 90 60 90 65 L 90 80 Q 90 85 85 85 L 70 85 Z M 50 85 L 65 85 Q 65 92 58 92 L 54 92 Q 50 92 50 88 Z'],
    'cloud': ['M 18 62 Q 8 62 8 52 Q 8 42 22 40 Q 24 22 44 22 Q 60 22 64 38 Q 84 38 86 54 Q 86 68 72 68 L 22 68 Q 18 68 18 62 Z'],
    'monitor': ['M 10 18 Q 10 14 14 14 L 86 14 Q 90 14 90 18 L 90 68 Q 90 72 86 72 L 14 72 Q 10 72 10 68 Z M 14 18 L 86 18 L 86 68 L 14 68 Z M 40 72 L 60 72 L 62 82 L 38 82 Z M 30 82 L 70 82 L 70 88 L 30 88 Z'],
    'user_simple': ['M 50 32 m -14 0 a 14 14 0 1 1 28 0 a 14 14 0 1 1 -28 0 M 24 85 Q 24 60 50 60 Q 76 60 76 85 Z'],
    'phone': ['M 20 15 Q 20 10 25 10 L 35 10 Q 40 10 40 15 L 40 30 Q 40 35 35 35 Q 28 38 28 50 Q 28 62 35 65 Q 40 65 40 70 L 40 85 Q 40 90 35 90 Q 10 90 10 55 Q 10 15 20 15 Z'],
    'chat': ['M 15 25 Q 15 15 25 15 L 75 15 Q 85 15 85 25 L 85 60 Q 85 70 75 70 L 45 70 L 30 85 L 30 70 L 25 70 Q 15 70 15 60 Z'],
    'email': ['M 10 25 Q 10 20 15 20 L 85 20 Q 90 20 90 25 L 90 75 Q 90 80 85 80 L 15 80 Q 10 80 10 75 Z M 15 28 L 50 55 L 85 28'],
    'share': ['M 75 20 m -15 0 a 15 15 0 1 1 30 0 a 15 15 0 1 1 -30 0 M 25 50 m -15 0 a 15 15 0 1 1 30 0 a 15 15 0 1 1 -30 0 M 75 80 m -15 0 a 15 15 0 1 1 30 0 a 15 15 0 1 1 -30 0 M 38 43 L 62 27 M 38 57 L 62 73'],
    'video': ['M 10 25 Q 10 20 15 20 L 60 20 Q 65 20 65 25 L 65 75 Q 65 80 60 80 L 15 80 Q 10 80 10 75 Z M 70 38 L 90 25 L 90 75 L 70 62 Z'],
    'check': ['M 25 52 L 42 70 L 78 32 L 70 24 L 42 54 L 33 44 Z'],
    'tower': ['M 50 10 L 48 15 L 52 15 Z M 48 15 L 30 90 L 34 90 L 44 60 L 56 60 L 66 90 L 70 90 L 52 15 Z M 45 45 L 55 45 L 54 50 L 46 50 Z M 42 62 L 58 62 L 56 66 L 44 66 Z M 40 78 L 60 78 L 58 82 L 42 82 Z M 50 25 m -5 0 a 5 5 0 1 1 10 0 a 5 5 0 1 1 -10 0', 'M 25 25 Q 22 32 22 40 M 18 20 Q 12 32 12 44 M 75 25 Q 78 32 78 40 M 82 20 Q 88 32 88 44'],
    'thinfinity_ring': [],  # drawn via dedicated function
}

def thinfinity_ring(cx, cy, r, color="#0A74D6", accent="#FFFFFF", stroke=None):
    """Simplified Thinfinity logo: stylized ring with swooshes."""
    sw = r * 0.18
    return f'''<g>
<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="{sw}"/>
<path d="M {cx - r*0.55} {cy - r*0.15} Q {cx} {cy - r*0.75} {cx + r*0.55} {cy - r*0.15}" fill="none" stroke="{color}" stroke-width="{sw*0.85}" stroke-linecap="round"/>
<path d="M {cx - r*0.55} {cy + r*0.15} Q {cx} {cy + r*0.75} {cx + r*0.55} {cy + r*0.15}" fill="none" stroke="{color}" stroke-width="{sw*0.85}" stroke-linecap="round"/>
<circle cx="{cx}" cy="{cy}" r="{r*0.22}" fill="{color}"/>
</g>'''

def agent_with_headset(cx, cy, r, skin="#F5D0B5", body="#0A74D6", headset="#1E293B"):
    """Flat agent icon: head with headset."""
    return f'''<g>
<circle cx="{cx}" cy="{cy-r*0.1}" r="{r*0.55}" fill="{skin}"/>
<path d="M {cx-r*0.62} {cy-r*0.15} Q {cx-r*0.62} {cy-r*0.75} {cx} {cy-r*0.75} Q {cx+r*0.62} {cy-r*0.75} {cx+r*0.62} {cy-r*0.15}" fill="none" stroke="{headset}" stroke-width="{r*0.14}" stroke-linecap="round"/>
<rect x="{cx-r*0.7}" y="{cy-r*0.2}" width="{r*0.2}" height="{r*0.3}" rx="{r*0.08}" fill="{headset}"/>
<rect x="{cx+r*0.5}" y="{cy-r*0.2}" width="{r*0.2}" height="{r*0.3}" rx="{r*0.08}" fill="{headset}"/>
<path d="M {cx+r*0.6} {cy} L {cx+r*0.75} {cy+r*0.15} L {cx+r*0.85} {cy+r*0.18}" stroke="{headset}" stroke-width="{r*0.08}" fill="none" stroke-linecap="round"/>
<circle cx="{cx+r*0.85}" cy="{cy+r*0.18}" r="{r*0.1}" fill="{headset}"/>
<path d="M {cx-r*0.8} {cy+r*0.85} Q {cx-r*0.8} {cy+r*0.25} {cx} {cy+r*0.25} Q {cx+r*0.8} {cy+r*0.25} {cx+r*0.8} {cy+r*0.85} Z" fill="{body}"/>
</g>'''

# ============================================================
# COVER 1 — A Blue, P4 Hub-and-spoke
# Metaphor: Thinfinity ring at center, agents orbiting
# ============================================================

def cover_1():
    defs = "\n".join([
        linear_grad("bg1", [("0%", "#4A96F0"), ("55%", "#1060AB"), ("100%", "#01325E")]),
        radial_grad("halo1", [("0%", ("#FFFFFF", 0.45)), ("100%", ("#FFFFFF", 0))]),
    ])
    body = []
    body.append(f'<rect width="{W}" height="{H}" fill="url(#bg1)"/>')
    cx, cy = W/2, H/2
    # halo
    body.append(f'<circle cx="{cx}" cy="{cy}" r="450" fill="url(#halo1)"/>')
    # rings
    body.append(rings(cx, cy, [(340, 0.22), (450, 0.14), (560, 0.08)]))

    # 8 agents in orbit - 2 rings
    outer_r = 420
    agent_positions = []
    for i, angle in enumerate([-75, -30, 30, 75, 105, 150, 210, 255]):
        rad = math.radians(angle)
        ax = cx + outer_r * math.cos(rad)
        ay = cy + outer_r * math.sin(rad)
        agent_positions.append((ax, ay))

    # connection lines hub -> agents
    for ax, ay in agent_positions:
        body.append(f'<line x1="{cx}" y1="{cy}" x2="{ax}" y2="{ay}" stroke="#FFFFFF" stroke-width="2" stroke-opacity="0.3"/>')

    # agent circles (white with agent icon)
    for ax, ay in agent_positions:
        body.append(f'<circle cx="{ax}" cy="{ay}" r="58" fill="#FFFFFF" opacity="0.95"/>')
        body.append(agent_with_headset(ax, ay, 42, body="#0A74D6"))

    # central hub - Thinfinity ring in white disc
    body.append(f'<g filter="url(#ground-shadow)"><ellipse cx="{cx}" cy="{cy+150}" rx="140" ry="18" fill="#000" opacity="0.4"/></g>')
    body.append(f'<circle cx="{cx}" cy="{cy}" r="140" fill="#FFFFFF"/>')
    body.append(f'<circle cx="{cx-40}" cy="{cy-50}" r="50" fill="#FFFFFF" opacity="0.6"/>')
    body.append(thinfinity_ring(cx, cy, 90, color="#0A74D6"))

    # small label pill on top
    body.append(pill(W/2 - 260, 80, 520, 60, "VDI for Telecom Contact Centers", bg="#0B1A3B", color="#FFFFFF", fs=26))

    # OCI hint at bottom right
    body.append(pill(W - 280, H - 120, 200, 48, "on Oracle Cloud", bg="#0B1A3B", color="#FFFFFF", fs=20))

    return wrap(defs, "\n".join(body))

# ============================================================
# COVER 2 — B Navy, P1 Hero-center
# Metaphor: Big cloud streaming VDI sessions down to a row of agents
# ============================================================

def cover_2():
    defs = "\n".join([
        linear_grad("bg2", [("0%", "#1F3082"), ("55%", "#0D1E5E"), ("100%", "#031035")]),
        radial_grad("halo2", [("0%", ("#5A95D1", 0.55)), ("100%", ("#5A95D1", 0))]),
        linear_grad("cloud2", [("0%", "#FFFFFF"), ("100%", "#E2E8F0")]),
        linear_grad("rayGrad", [("0%", "#5A95D1"), ("100%", "#0A74D6")], x1=0, y1=0, x2=0, y2=1),
    ])
    body = []
    body.append(f'<rect width="{W}" height="{H}" fill="url(#bg2)"/>')

    # halo behind cloud
    body.append(f'<circle cx="{W/2}" cy="370" r="450" fill="url(#halo2)"/>')

    # CLOUD (top hero)
    ccx, ccy = W/2, 330
    body.append(f'<g filter="url(#ground-shadow)"><ellipse cx="{ccx}" cy="{ccy+160}" rx="280" ry="20" fill="#000" opacity="0.45"/></g>')
    cloud_d = f"M {ccx-260} {ccy+100} Q {ccx-340} {ccy+100} {ccx-340} {ccy+20} Q {ccx-340} {ccy-60} {ccx-260} {ccy-70} Q {ccx-240} {ccy-160} {ccx-120} {ccy-160} Q {ccx-40} {ccy-200} {ccx+60} {ccy-180} Q {ccx+180} {ccy-180} {ccx+240} {ccy-100} Q {ccx+340} {ccy-80} {ccx+340} {ccy+20} Q {ccx+340} {ccy+100} {ccx+260} {ccy+100} Z"
    body.append(f'<path d="{cloud_d}" fill="url(#cloud2)"/>')

    # Monitor inside cloud
    mw, mh = 280, 180
    mx, my = ccx - mw/2, ccy - mh/2 - 20
    body.append(f'<rect x="{mx}" y="{my}" width="{mw}" height="{mh}" rx="14" fill="#0B1A3B"/>')
    body.append(f'<rect x="{mx+10}" y="{my+10}" width="{mw-20}" height="{mh-20}" rx="8" fill="#E8F1FB"/>')
    # mock UI bars
    body.append(f'<rect x="{mx+25}" y="{my+28}" width="80" height="10" rx="5" fill="#0A74D6" opacity="0.7"/>')
    body.append(f'<rect x="{mx+25}" y="{my+50}" width="{mw-50}" height="6" rx="3" fill="#0A74D6" opacity="0.25"/>')
    body.append(f'<rect x="{mx+25}" y="{my+64}" width="{mw-80}" height="6" rx="3" fill="#0A74D6" opacity="0.2"/>')
    body.append(f'<rect x="{mx+25}" y="{my+90}" width="90" height="50" rx="6" fill="#0A74D6" opacity="0.35"/>')
    body.append(f'<rect x="{mx+125}" y="{my+90}" width="90" height="50" rx="6" fill="#0A74D6" opacity="0.2"/>')
    # stand
    body.append(f'<rect x="{ccx-30}" y="{my+mh}" width="60" height="12" fill="#0B1A3B"/>')
    body.append(f'<rect x="{ccx-70}" y="{my+mh+12}" width="140" height="8" rx="4" fill="#0B1A3B"/>')

    # Thinfinity ring badge on cloud
    body.append(thinfinity_ring(ccx - 280, ccy - 40, 45, color="#0A74D6"))

    # RAYS: streaming from cloud to agents below
    ray_top_y = ccy + 110
    agents = 6
    spacing = 240
    row_y = H - 280
    first_x = W/2 - (agents - 1) * spacing / 2
    for i in range(agents):
        ax = first_x + i * spacing
        # ray
        body.append(f'<path d="M {ax} {ray_top_y} Q {ax} {(ray_top_y + row_y)/2} {ax} {row_y - 100}" stroke="url(#rayGrad)" stroke-width="4" fill="none" stroke-opacity="0.55" stroke-dasharray="2 8"/>')
        # small monitor above agent
        mx2, my2 = ax - 55, row_y - 130
        body.append(f'<rect x="{mx2}" y="{my2}" width="110" height="72" rx="8" fill="#1E293B"/>')
        body.append(f'<rect x="{mx2+6}" y="{my2+6}" width="98" height="60" rx="4" fill="#E8F1FB"/>')
        body.append(f'<rect x="{mx2+14}" y="{my2+14}" width="40" height="6" rx="3" fill="#0A74D6" opacity="0.7"/>')
        body.append(f'<rect x="{mx2+14}" y="{my2+26}" width="70" height="4" rx="2" fill="#0A74D6" opacity="0.3"/>')
        body.append(f'<rect x="{mx2+14}" y="{my2+36}" width="60" height="4" rx="2" fill="#0A74D6" opacity="0.25"/>')
        body.append(f'<rect x="{mx2+14}" y="{my2+48}" width="50" height="4" rx="2" fill="#0A74D6" opacity="0.2"/>')
        body.append(f'<rect x="{ax-12}" y="{my2+72}" width="24" height="6" fill="#1E293B"/>')
        # agent headset below
        body.append(agent_with_headset(ax, row_y + 20, 52, body="#0A74D6"))

    # ground line
    body.append(f'<line x1="100" y1="{row_y + 120}" x2="{W - 100}" y2="{row_y + 120}" stroke="#5A95D1" stroke-width="2" stroke-opacity="0.4"/>')

    # top label
    body.append(pill(W/2 - 260, 80, 520, 60, "Virtual desktops, any scale", bg="#FFFFFF", color="#0B1A3B", fs=26))

    return wrap(defs, "\n".join(body))

# ============================================================
# COVER 3 — F Pastel, P1 Hero-center
# Metaphor: Single agent with headset + monitor, omnichannel orbiting
# ============================================================

def cover_3():
    defs = "\n".join([
        linear_grad("bg3", [("0%", "#DCE4F9"), ("60%", "#C2D2F9"), ("100%", "#AABCEF")]),
        radial_grad("halo3", [("0%", ("#FFFFFF", 0.7)), ("100%", ("#FFFFFF", 0))]),
        linear_grad("monitor3", [("0%", "#FFFFFF"), ("100%", "#E8F1FB")]),
    ])
    body = []
    body.append(f'<rect width="{W}" height="{H}" fill="url(#bg3)"/>')
    cx, cy = W/2, H/2 + 10
    body.append(f'<circle cx="{cx}" cy="{cy-20}" r="450" fill="url(#halo3)"/>')
    body.append(rings(cx, cy-20, [(330, 0.2), (430, 0.13), (540, 0.08)], stroke="#6366F1"))

    # HERO - monitor + agent in front
    # Monitor behind
    mw, mh = 560, 340
    mx, my = cx - mw/2, cy - 220
    body.append(f'<g filter="url(#ground-shadow)"><rect x="{mx+10}" y="{my+14}" width="{mw}" height="{mh}" rx="18" fill="#000" opacity="0.2"/></g>')
    body.append(f'<rect x="{mx}" y="{my}" width="{mw}" height="{mh}" rx="18" fill="#1E293B"/>')
    body.append(f'<rect x="{mx+14}" y="{my+14}" width="{mw-28}" height="{mh-28}" rx="10" fill="url(#monitor3)"/>')
    # dashboard-ish UI inside
    body.append(f'<rect x="{mx+42}" y="{my+42}" width="180" height="14" rx="7" fill="#0A74D6"/>')
    body.append(f'<rect x="{mx+42}" y="{my+72}" width="{mw-100}" height="8" rx="4" fill="#0A74D6" opacity="0.25"/>')
    body.append(f'<rect x="{mx+42}" y="{my+90}" width="{mw-150}" height="8" rx="4" fill="#0A74D6" opacity="0.2"/>')
    # 3 data cards inside
    for i, (off, color) in enumerate([(0, "#3B82F6"), (1, "#22C55E"), (2, "#A78BFA")]):
        cdx = mx + 42 + off * 165
        body.append(f'<rect x="{cdx}" y="{my+130}" width="150" height="100" rx="8" fill="{color}" opacity="0.18"/>')
        body.append(f'<rect x="{cdx+16}" y="{my+150}" width="50" height="10" rx="5" fill="{color}"/>')
        body.append(f'<rect x="{cdx+16}" y="{my+175}" width="90" height="6" rx="3" fill="{color}" opacity="0.6"/>')
        body.append(f'<rect x="{cdx+16}" y="{my+190}" width="60" height="6" rx="3" fill="{color}" opacity="0.4"/>')
    # stand
    body.append(f'<rect x="{cx-40}" y="{my+mh}" width="80" height="14" fill="#1E293B"/>')
    body.append(f'<rect x="{cx-90}" y="{my+mh+14}" width="180" height="10" rx="5" fill="#1E293B"/>')

    # Agent in front (partial, shoulders + head)
    # position overlap bottom of monitor
    ay = my + mh - 10
    body.append(f'<g filter="url(#ground-shadow)"><ellipse cx="{cx}" cy="{ay+180}" rx="200" ry="18" fill="#1E293B" opacity="0.3"/></g>')
    # body torso
    body.append(f'<path d="M {cx-150} {ay+200} Q {cx-150} {ay+70} {cx} {ay+70} Q {cx+150} {ay+70} {cx+150} {ay+200} Z" fill="#0A74D6"/>')
    # head
    body.append(f'<circle cx="{cx}" cy="{ay+30}" r="62" fill="#F5D0B5"/>')
    # headset
    body.append(f'<path d="M {cx-68} {ay+25} Q {cx-68} {ay-40} {cx} {ay-40} Q {cx+68} {ay-40} {cx+68} {ay+25}" fill="none" stroke="#1E293B" stroke-width="8" stroke-linecap="round"/>')
    body.append(f'<rect x="{cx-78}" y="{ay+15}" width="18" height="26" rx="6" fill="#1E293B"/>')
    body.append(f'<rect x="{cx+60}" y="{ay+15}" width="18" height="26" rx="6" fill="#1E293B"/>')
    # mic
    body.append(f'<path d="M {cx+68} {ay+35} Q {cx+85} {ay+45} {cx+95} {ay+55}" stroke="#1E293B" stroke-width="5" fill="none" stroke-linecap="round"/>')
    body.append(f'<circle cx="{cx+95}" cy="{ay+58}" r="6" fill="#1E293B"/>')

    # Channel badges orbiting
    channels = [
        (-240, -180, "#3B82F6", ICON['phone']),   # top-left: voice
        (240, -180, "#22C55E", ICON['chat']),     # top-right: chat
        (-300, 40, "#F59E0B", ICON['email']),     # left: email
        (300, 40, "#EC4899", ICON['video']),      # right: video
        (-200, 230, "#A78BFA", ICON['share']),    # bottom-left: social
    ]
    for dx, dy, color, icon in channels:
        bx, by = cx + dx, cy + dy
        body.append(circle_badge(bx, by, 48, color, icon, icon_color="#FFFFFF", icon_scale=0.55))

    # connection lines from screen to channels
    for dx, dy, _, _ in channels:
        bx, by = cx + dx, cy + dy
        body.append(f'<path d="M {cx} {my+180} Q {(cx+bx)/2} {(my+180+by)/2} {bx} {by}" stroke="#6366F1" stroke-width="2" stroke-opacity="0.35" fill="none" stroke-dasharray="3 5"/>')

    # Top label
    body.append(pill(W/2 - 270, 80, 540, 60, "One desktop. All channels.", bg="#1E1B4B", color="#FFFFFF", fs=26))

    return wrap(defs, "\n".join(body))

# ============================================================
# COVER 4 — C Purple, P5 Dashboard mockup
# Metaphor: Cloud Manager-style dashboard showing contact center at scale
# ============================================================

def cover_4():
    defs = "\n".join([
        linear_grad("bg4", [("0%", "#C36CE1"), ("55%", "#6B1FA0"), ("100%", "#33188C")]),
        radial_grad("halo4", [("0%", ("#FFFFFF", 0.35)), ("100%", ("#FFFFFF", 0))]),
        linear_grad("panel4", [("0%", "#FFFFFF"), ("100%", "#F3ECF9")]),
        linear_grad("chart4", [("0%", "#A78BFA"), ("100%", "#7C3AED")]),
    ])
    body = []
    body.append(f'<rect width="{W}" height="{H}" fill="url(#bg4)"/>')
    body.append(f'<circle cx="{W/2}" cy="{H/2}" r="500" fill="url(#halo4)"/>')

    # big dashboard panel
    pw, ph = 1400, 780
    px, py = (W - pw)/2, (H - ph)/2 + 10
    body.append(f'<g filter="url(#ground-shadow)"><rect x="{px+12}" y="{py+14}" width="{pw}" height="{ph}" rx="24" fill="#000" opacity="0.3"/></g>')
    body.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="24" fill="url(#panel4)"/>')
    # title bar
    body.append(f'<rect x="{px}" y="{py}" width="{pw}" height="76" rx="24" fill="#1E1B4B"/>')
    body.append(f'<rect x="{px}" y="{py+50}" width="{pw}" height="26" fill="#1E1B4B"/>')
    # logo ring in title bar
    body.append(thinfinity_ring(px + 50, py + 38, 22, color="#FFFFFF"))
    body.append(f'<text x="{px + 90}" y="{py+48}" font-size="26" font-weight="700" fill="#FFFFFF">Thinfinity · Cloud Manager</text>')
    # window dots
    for i, c in enumerate(["#E04040", "#F59E0B", "#22C55E"]):
        body.append(f'<circle cx="{px + pw - 60 - i*26}" cy="{py+38}" r="7" fill="{c}"/>')

    # KPIs row
    kpi_y = py + 110
    kpis = [
        ("Active Agents", "4,782", "#7C3AED"),
        ("Sessions / hr", "12,450", "#EC4899"),
        ("Provision time", "4 min", "#22C55E"),
        ("Uptime", "99.98%", "#06B6D4"),
    ]
    card_w = (pw - 60 - 30) / 4
    for i, (label, val, color) in enumerate(kpis):
        kx = px + 30 + i * (card_w + 10)
        body.append(f'<rect x="{kx}" y="{kpi_y}" width="{card_w}" height="130" rx="14" fill="{color}" opacity="0.1"/>')
        body.append(f'<rect x="{kx}" y="{kpi_y}" width="6" height="130" rx="3" fill="{color}"/>')
        body.append(f'<text x="{kx + 24}" y="{kpi_y + 36}" font-size="16" font-weight="500" fill="#515151">{label}</text>')
        body.append(f'<text x="{kx + 24}" y="{kpi_y + 90}" font-size="44" font-weight="700" fill="#1E1B4B">{val}</text>')

    # Agent grid (left side)
    grid_x, grid_y = px + 30, py + 270
    grid_w = 520
    # label
    body.append(f'<text x="{grid_x}" y="{grid_y - 12}" font-size="18" font-weight="600" fill="#1E1B4B">Agent fleet · North Region</text>')
    cols, rows = 14, 8
    cell = 34
    gap = 4
    for r in range(rows):
        for c in range(cols):
            ax = grid_x + c * (cell + gap)
            ay = grid_y + r * (cell + gap)
            # alternate statuses: online/busy/away
            status = (r * cols + c) % 7
            if status == 6:
                fill = "#CBD5E1"  # away
            elif status % 3 == 0:
                fill = "#22C55E"  # online
            else:
                fill = "#7C3AED"  # busy
            body.append(f'<rect x="{ax}" y="{ay}" width="{cell}" height="{cell}" rx="7" fill="{fill}" opacity="0.9"/>')
            # tiny headset
            body.append(f'<circle cx="{ax+cell/2}" cy="{ay+cell/2}" r="6" fill="#FFFFFF" opacity="0.85"/>')

    # legend
    leg_y = grid_y + rows * (cell+gap) + 20
    for i, (c, txt) in enumerate([("#22C55E","Online"), ("#7C3AED","On-call"), ("#CBD5E1","Away")]):
        lx = grid_x + i * 130
        body.append(f'<rect x="{lx}" y="{leg_y}" width="14" height="14" rx="3" fill="{c}"/>')
        body.append(f'<text x="{lx+22}" y="{leg_y+12}" font-size="14" fill="#515151">{txt}</text>')

    # Right: map + chart
    map_x = px + 600
    body.append(f'<text x="{map_x}" y="{grid_y - 12}" font-size="18" font-weight="600" fill="#1E1B4B">Sessions across regions · last 24h</text>')
    # chart
    chart_x, chart_y = map_x, grid_y
    chart_w, chart_h = pw - (map_x - px) - 30, 220
    body.append(f'<rect x="{chart_x}" y="{chart_y}" width="{chart_w}" height="{chart_h}" rx="10" fill="#F5F3FF"/>')
    # gridlines
    for i in range(1, 4):
        ly = chart_y + i * chart_h / 4
        body.append(f'<line x1="{chart_x+10}" y1="{ly}" x2="{chart_x+chart_w-10}" y2="{ly}" stroke="#A78BFA" stroke-opacity="0.2"/>')
    # area chart
    points_x = 14
    area_pts = []
    vals = [0.3, 0.45, 0.42, 0.55, 0.72, 0.68, 0.85, 0.78, 0.9, 0.82, 0.95, 0.88, 0.75, 0.62]
    step = (chart_w - 20) / (len(vals) - 1)
    for i, v in enumerate(vals):
        x = chart_x + 10 + i * step
        y = chart_y + chart_h - 15 - v * (chart_h - 30)
        area_pts.append(f"{x:.1f},{y:.1f}")
    body.append(f'<polyline points="{chart_x+10},{chart_y+chart_h-15} {" ".join(area_pts)} {chart_x+chart_w-10},{chart_y+chart_h-15}" fill="url(#chart4)" fill-opacity="0.55"/>')
    body.append(f'<polyline points="{" ".join(area_pts)}" fill="none" stroke="#7C3AED" stroke-width="3"/>')

    # region pills below chart
    regions = [("North America", "2,480", "#7C3AED"), ("EMEA", "1,820", "#EC4899"), ("LATAM", "482", "#06B6D4")]
    reg_y = chart_y + chart_h + 26
    for i, (name, num, c) in enumerate(regions):
        rx_ = chart_x + i * ((chart_w - 20) / 3) + 10
        rw_ = (chart_w - 60) / 3
        body.append(f'<rect x="{rx_}" y="{reg_y}" width="{rw_}" height="64" rx="12" fill="{c}" opacity="0.12"/>')
        body.append(f'<circle cx="{rx_ + 26}" cy="{reg_y + 32}" r="10" fill="{c}"/>')
        body.append(f'<text x="{rx_ + 48}" y="{reg_y+28}" font-size="14" fill="#515151">{name}</text>')
        body.append(f'<text x="{rx_ + 48}" y="{reg_y+52}" font-size="22" font-weight="700" fill="#1E1B4B">{num} agents</text>')

    # Top label
    body.append(pill(W/2 - 280, 50, 560, 52, "Contact center at scale, in one pane", bg="#1E1B4B", color="#FFFFFF", fs=24))

    return wrap(defs, "\n".join(body))

# ============================================================
# COVER 5 — D Teal, P2 Split
# Metaphor: Physical call center (left) → Virtual VDI (right)
# ============================================================

def cover_5():
    defs = "\n".join([
        linear_grad("bg5", [("0%", "#47D7C0"), ("55%", "#118982"), ("100%", "#0F222B")]),
        radial_grad("halo5l", [("0%", ("#515151", 0.4)), ("100%", ("#515151", 0))]),
        radial_grad("halo5r", [("0%", ("#3DCCA1", 0.5)), ("100%", ("#3DCCA1", 0))]),
    ])
    body = []
    body.append(f'<rect width="{W}" height="{H}" fill="url(#bg5)"/>')

    lcx, lcy = W * 0.26, H/2 + 20
    rcx, rcy = W * 0.74, H/2 + 20

    body.append(f'<circle cx="{lcx}" cy="{lcy}" r="360" fill="url(#halo5l)"/>')
    body.append(f'<circle cx="{rcx}" cy="{rcy}" r="360" fill="url(#halo5r)"/>')

    # vertical divider
    body.append(f'<line x1="{W/2}" y1="160" x2="{W/2}" y2="{H-160}" stroke="#FFFFFF" stroke-width="2" stroke-opacity="0.25" stroke-dasharray="6 10"/>')

    # ====== LEFT: Physical call center ======
    # 3 rows of cubicles, desaturated/dark
    row_start_y = lcy - 140
    for row in range(3):
        for col in range(3):
            bx = lcx - 180 + col * 150
            by = row_start_y + row * 110
            # cubicle bg
            body.append(f'<rect x="{bx-50}" y="{by-35}" width="100" height="85" rx="6" fill="#1E293B" opacity="{0.85 - row*0.1}"/>')
            # monitor
            body.append(f'<rect x="{bx-35}" y="{by-25}" width="70" height="45" rx="4" fill="#334155"/>')
            body.append(f'<rect x="{bx-30}" y="{by-20}" width="60" height="35" rx="2" fill="#475569"/>')
            # agent dot
            body.append(f'<circle cx="{bx}" cy="{by+32}" r="8" fill="#94A3B8"/>')

    # "Physical" label pill
    body.append(pill(lcx - 130, lcy + 240, 260, 58, "Physical · $12M/yr", bg="#1E0000", color="#FFFFFF", fs=24))
    body.append(f'<text x="{lcx}" y="{lcy - 230}" text-anchor="middle" font-size="30" font-weight="700" fill="#FFFFFF" opacity="0.85">Legacy call center</text>')

    # ====== RIGHT: Virtual VDI ======
    # Cloud above with Thinfinity ring
    body.append(f'<g filter="url(#ground-shadow)"><ellipse cx="{rcx}" cy="{rcy+230}" rx="170" ry="18" fill="#000" opacity="0.45"/></g>')
    # Cloud
    cloud_d = f"M {rcx-160} {rcy-20} Q {rcx-220} {rcy-20} {rcx-220} {rcy-70} Q {rcx-220} {rcy-125} {rcx-160} {rcy-130} Q {rcx-150} {rcy-180} {rcx-80} {rcy-180} Q {rcx-30} {rcy-210} {rcx+30} {rcy-200} Q {rcx+100} {rcy-200} {rcx+140} {rcy-150} Q {rcx+220} {rcy-130} {rcx+220} {rcy-70} Q {rcx+220} {rcy-20} {rcx+160} {rcy-20} Z"
    body.append(f'<path d="{cloud_d}" fill="#FFFFFF" opacity="0.95"/>')
    body.append(thinfinity_ring(rcx, rcy-105, 48, color="#0A74D6"))

    # Grid of clean VDI sessions below cloud
    for row in range(3):
        for col in range(4):
            sx = rcx - 220 + col * 150
            sy = rcy + 30 + row * 80
            body.append(f'<rect x="{sx-55}" y="{sy-25}" width="110" height="68" rx="8" fill="#1E293B"/>')
            body.append(f'<rect x="{sx-48}" y="{sy-18}" width="96" height="54" rx="4" fill="#E8F1FB"/>')
            body.append(f'<rect x="{sx-38}" y="{sy-8}" width="30" height="5" rx="2" fill="#0A74D6" opacity="0.7"/>')
            body.append(f'<rect x="{sx-38}" y="{sy+2}" width="60" height="4" rx="2" fill="#0A74D6" opacity="0.3"/>')
            body.append(f'<rect x="{sx-38}" y="{sy+12}" width="50" height="4" rx="2" fill="#0A74D6" opacity="0.25"/>')
            body.append(f'<circle cx="{sx+40}" cy="{sy-20}" r="4" fill="#22C55E"/>')  # "online" dot
    # ray/connection lines from cloud
    for col in [0, 1, 2, 3]:
        sx = rcx - 220 + col * 150
        body.append(f'<line x1="{rcx}" y1="{rcy-80}" x2="{sx}" y2="{rcy+10}" stroke="#FFFFFF" stroke-width="2" stroke-opacity="0.35" stroke-dasharray="3 6"/>')

    body.append(pill(rcx - 130, rcy + 280, 260, 58, "Virtual · $5M/yr", bg="#053B2C", color="#FFFFFF", fs=24))
    body.append(f'<text x="{rcx}" y="{rcy - 230}" text-anchor="middle" font-size="30" font-weight="700" fill="#FFFFFF">VDI on OCI</text>')

    # Arrow between
    body.append(f'<path d="M {W/2-70} {H/2-20} L {W/2+70} {H/2-20}" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" opacity="0.65"/>')
    body.append(f'<polygon points="{W/2+60},{H/2-40} {W/2+95},{H/2-20} {W/2+60},{H/2}" fill="#FFFFFF" opacity="0.8"/>')

    # Top label
    body.append(pill(W/2 - 280, 60, 560, 58, "Same contact center. Reimagined.", bg="#0F222B", color="#FFFFFF", fs=24))

    return wrap(defs, "\n".join(body))

# ============================================================
# COVER 6 — A Blue alt (brighter), P3 Triad
# Metaphor: 1K / 5K / 10K agent tiers, one platform
# ============================================================

def cover_6():
    defs = "\n".join([
        linear_grad("bg6", [("0%", "#8BEDFF"), ("50%", "#2D8FDF"), ("100%", "#073F69")]),
        radial_grad("halo6", [("0%", ("#FFFFFF", 0.4)), ("100%", ("#FFFFFF", 0))]),
        radial_grad("halo6c", [("0%", ("#FFFFFF", 0.3)), ("100%", ("#FFFFFF", 0))]),
        linear_grad("cloud6", [("0%", "#FFFFFF"), ("100%", "#E8F1FB")]),
    ])
    body = []
    body.append(f'<rect width="{W}" height="{H}" fill="url(#bg6)"/>')

    # Top: central cloud with Thinfinity (platform node)
    ccx, ccy = W/2, 280
    body.append(f'<circle cx="{ccx}" cy="{ccy}" r="280" fill="url(#halo6c)"/>')
    cloud_d = f"M {ccx-180} {ccy+60} Q {ccx-240} {ccy+60} {ccx-240} {ccy+10} Q {ccx-240} {ccy-50} {ccx-180} {ccy-55} Q {ccx-170} {ccy-110} {ccx-100} {ccy-110} Q {ccx-40} {ccy-140} {ccx+40} {ccy-125} Q {ccx+120} {ccy-125} {ccx+170} {ccy-75} Q {ccx+240} {ccy-55} {ccx+240} {ccy+10} Q {ccx+240} {ccy+60} {ccx+180} {ccy+60} Z"
    body.append(f'<g filter="url(#ground-shadow)"><ellipse cx="{ccx}" cy="{ccy+95}" rx="170" ry="14" fill="#000" opacity="0.3"/></g>')
    body.append(f'<path d="{cloud_d}" fill="url(#cloud6)"/>')
    body.append(thinfinity_ring(ccx, ccy - 20, 48, color="#0A74D6"))
    # tag
    body.append(pill(ccx - 110, ccy + 36, 220, 38, "Thinfinity on OCI", bg="#0A74D6", color="#FFFFFF", fs=18))

    # 3 tier circles - show increasing scale
    tiers = [
        (420, H - 290, 120, "1K", "agents", "#60A5FA"),
        (W/2, H - 340, 150, "5K", "agents", "#7C3AED"),
        (W - 420, H - 290, 180, "10K+", "agents", "#06B6D4"),
    ]
    # Connection lines from cloud down to each tier
    for tcx, tcy, tr, _, _, color in tiers:
        body.append(f'<path d="M {ccx} {ccy+90} Q {(ccx+tcx)/2} {(ccy+tcy)/2-40} {tcx} {tcy-tr}" stroke="#FFFFFF" stroke-width="3" fill="none" stroke-opacity="0.5" stroke-dasharray="4 8"/>')

    # Tier circles with agent dots around
    for tcx, tcy, tr, num, lbl, color in tiers:
        # soft halo
        body.append(f'<circle cx="{tcx}" cy="{tcy}" r="{tr + 40}" fill="url(#halo6)"/>')
        # shadow
        body.append(f'<g filter="url(#ground-shadow)"><circle cx="{tcx}" cy="{tcy+6}" r="{tr}" fill="#000" opacity="0.3"/></g>')
        # main circle
        body.append(f'<circle cx="{tcx}" cy="{tcy}" r="{tr}" fill="{color}"/>')
        # inner highlight
        body.append(f'<circle cx="{tcx-tr*0.25}" cy="{tcy-tr*0.3}" r="{tr*0.35}" fill="#FFFFFF" opacity="0.2"/>')
        # agent dots around circle (orbiting)
        n_dots = 8 if tr < 130 else (12 if tr < 170 else 16)
        for i in range(n_dots):
            ang = math.radians(i * 360 / n_dots - 90)
            dx = tcx + (tr + 28) * math.cos(ang)
            dy = tcy + (tr + 28) * math.sin(ang)
            body.append(f'<circle cx="{dx}" cy="{dy}" r="10" fill="#FFFFFF" opacity="0.9"/>')
            body.append(f'<circle cx="{dx}" cy="{dy-1}" r="4.5" fill="{color}"/>')
        # number inside
        body.append(f'<text x="{tcx}" y="{tcy+10}" text-anchor="middle" font-size="{tr*0.55}" font-weight="700" fill="#FFFFFF">{num}</text>')
        body.append(f'<text x="{tcx}" y="{tcy+tr*0.3 + 10}" text-anchor="middle" font-size="{tr*0.18}" font-weight="500" fill="#FFFFFF" opacity="0.9">{lbl}</text>')

    # Top label
    body.append(pill(W/2 - 280, 60, 560, 58, "One platform. Any scale.", bg="#0B1A3B", color="#FFFFFF", fs=26))

    return wrap(defs, "\n".join(body))

# ============================================================
# BUILD ALL
# ============================================================

covers = [
    ("01_hub_orbit", "Hub Thinfinity + agentes orbitando", "A Azul", "P4 Hub-and-spoke", "Anillo Thinfinity central + 8 agentes con auriculares", cover_1),
    ("02_cloud_stream", "Nube entregando VDI a fila de agentes", "B Navy", "P1 Hero-center", "Nube + monitor + 6 agentes recibiendo sesiones", cover_2),
    ("03_unified_agent", "Agente unificado con canales", "F Pastel", "P1 Hero-center", "Agente con headset + monitor + 5 canales orbitando", cover_3),
    ("04_dashboard_scale", "Contact center a escala (panel mgmt)", "C Púrpura", "P5 Dashboard", "Vista Cloud Manager: KPIs, grid de agentes, mapa", cover_4),
    ("05_physical_virtual", "Físico → Virtual", "D Teal", "P2 Split", "Call center físico ↔ grid VDI en nube", cover_5),
    ("06_multi_scale", "VDI a cualquier escala", "A Azul alt", "P3 Triada", "1K / 5K / 10K agentes conectados al mismo cloud", cover_6),
]

for slug, angle, family, comp, hero, fn in covers:
    svg = fn()
    path = OUT / f"telecom_cx_{slug}.svg"
    path.write_text(svg, encoding="utf-8")
    print(f"  [ok] {path.name}  ({len(svg):,} bytes)")

# Preview HTML
html = [
    '<!doctype html>',
    '<html lang="es"><head><meta charset="utf-8">',
    '<title>Telecom CX Cover Variants — Preview</title>',
    '<style>',
    '  * { box-sizing: border-box; }',
    '  body { margin: 0; padding: 40px; background: #F0F4F8; font-family: Inter, "Segoe UI", Arial, sans-serif; color: #1E293B; }',
    '  h1 { font-size: 28px; font-weight: 700; color: #0A74D6; margin: 0 0 8px; }',
    '  p.sub { margin: 0 0 40px; color: #515151; font-size: 16px; max-width: 900px; }',
    '  .card { background: #FFFFFF; border-radius: 16px; box-shadow: 0 4px 24px rgba(0,0,0,0.08); margin-bottom: 32px; overflow: hidden; }',
    '  .card h2 { margin: 0; padding: 20px 28px 8px; font-size: 22px; font-weight: 700; color: #0A74D6; }',
    '  .meta { padding: 0 28px 16px; display: flex; gap: 18px; flex-wrap: wrap; font-size: 14px; color: #515151; }',
    '  .meta .chip { background: #F0F4F8; border-radius: 999px; padding: 4px 14px; font-weight: 500; }',
    '  .meta .chip b { color: #1E293B; }',
    '  .cover-wrap { padding: 0 28px 28px; }',
    '  .cover-wrap img { width: 100%; height: auto; display: block; border-radius: 8px; }',
    '</style></head><body>',
    '<h1>Telecom Contact Center VDI — 6 Variantes del mismo concepto</h1>',
    '<p class="sub">Todas las variantes expresan la <b>misma idea central</b>: VDI en OCI potenciando contact centers de telco a escala. Cada una usa una metáfora visual, familia de color y composición distintas. Indicá cuál querés exportar como SVG nativo para Figma.</p>',
]

for slug, angle, family, comp, hero, _ in covers:
    html.append(f'<div class="card">')
    html.append(f'  <h2>Variante {slug.split("_")[0]} — {angle}</h2>')
    html.append(f'  <div class="meta">')
    html.append(f'    <span class="chip">Familia: <b>{family}</b></span>')
    html.append(f'    <span class="chip">Composición: <b>{comp}</b></span>')
    html.append(f'    <span class="chip">Hero: <b>{hero}</b></span>')
    html.append(f'  </div>')
    html.append(f'  <div class="cover-wrap"><img src="telecom_cx_{slug}.svg" alt="{angle}"/></div>')
    html.append(f'</div>')

html.append('</body></html>')
(OUT / "preview.html").write_text("\n".join(html), encoding="utf-8")
print(f"  [ok] preview.html")
print(f"\nOpen: {OUT / 'preview.html'}")
