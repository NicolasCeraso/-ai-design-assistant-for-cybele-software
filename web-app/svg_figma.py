# Makes an exported SVG safe to open in Figma, and refuses to hand over a fake one.
#
#  * inline_markers(): Figma ignores <marker>, so a connector's arrowhead (marker-end / marker-start)
#    disappears on import and the line loses its direction. Each marker is drawn as an ordinary
#    <g> of paths at the end of the line instead — same look in a browser, real layers in Figma.
#  * check_vector(): an SVG that holds only <image> elements (a raster wrapped in an <svg>) is not
#    editable. The export must fail loudly rather than deliver it.
import math
import re
import xml.etree.ElementTree as ET

_NUM = r'-?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?'
_TOKEN = re.compile(r'([MmLlHhVvCcSsQqTtAaZz])|(' + _NUM + ')')
_ARGS = {'M': 2, 'L': 2, 'H': 1, 'V': 1, 'C': 6, 'S': 4, 'Q': 4, 'T': 2, 'A': 7, 'Z': 0}


def _arc_tangent_end(x1, y1, rx, ry, phi, fa, fs, x2, y2):
    """Direction (radians) of an SVG elliptical arc at its end point (W3C implementation notes F.6)."""
    if rx == 0 or ry == 0:
        return math.atan2(y2 - y1, x2 - x1)
    rx, ry = abs(rx), abs(ry)
    p = math.radians(phi)
    cp, sp = math.cos(p), math.sin(p)
    dx, dy = (x1 - x2) / 2, (y1 - y2) / 2
    x1p, y1p = cp * dx + sp * dy, -sp * dx + cp * dy
    lam = x1p ** 2 / rx ** 2 + y1p ** 2 / ry ** 2
    if lam > 1:
        s = math.sqrt(lam); rx, ry = rx * s, ry * s
    num = rx ** 2 * ry ** 2 - rx ** 2 * y1p ** 2 - ry ** 2 * x1p ** 2
    den = rx ** 2 * y1p ** 2 + ry ** 2 * x1p ** 2
    co = math.sqrt(max(0, num / den)) if den else 0
    if fa == fs:
        co = -co
    cxp, cyp = co * rx * y1p / ry, -co * ry * x1p / rx
    # tangent at the end point (x2, y2) in the rotated frame, then rotate back
    ux, uy = (-x1p - cxp) / rx, (-y1p - cyp) / ry               # end point on the unit circle
    tx, ty = -uy * rx, ux * ry                                  # derivative direction (counter-clockwise)
    if not fs:
        tx, ty = -tx, -ty
    return math.atan2(sp * tx + cp * ty, cp * tx - sp * ty)


def path_ends(d):
    """((x, y, angle) at the start, (x, y, angle) at the end) of a path, angle in radians; None if unparsable."""
    toks = _TOKEN.findall(d or '')
    i, cmd = 0, None
    cx = cy = sx = sy = 0.0
    start = end = None
    first_seg = True
    while i < len(toks):
        if toks[i][0]:
            cmd = toks[i][0]; i += 1
            if cmd in 'Zz':
                if end is not None:
                    ang = math.atan2(sy - cy, sx - cx) if (sx, sy) != (cx, cy) else end[2]
                    end = (sx, sy, ang); cx, cy = sx, sy
                continue
        if cmd is None:
            return None
        n = _ARGS[cmd.upper()]
        if i + n > len(toks) or any(toks[j][0] for j in range(i, i + n)):
            return None
        a = [float(toks[j][1]) for j in range(i, i + n)]
        i += n
        rel = cmd.islower()
        c = cmd.upper()
        px, py = cx, cy
        ang = None
        if c == 'M':
            cx, cy = (cx + a[0], cy + a[1]) if rel else (a[0], a[1])
            sx, sy = cx, cy
            cmd = 'l' if rel else 'L'          # further pairs are implicit lineto
            continue
        if c == 'L':
            cx, cy = (cx + a[0], cy + a[1]) if rel else (a[0], a[1])
            ang = math.atan2(cy - py, cx - px)
        elif c == 'H':
            cx = cx + a[0] if rel else a[0]
            ang = math.atan2(0, cx - px)
        elif c == 'V':
            cy = cy + a[0] if rel else a[0]
            ang = math.atan2(cy - py, 0)
        elif c in 'CSQT':
            pts = [(a[k], a[k + 1]) for k in range(0, n, 2)]
            if rel:
                pts = [(cx + x, cy + y) for x, y in pts]
            ctrl = pts[-2] if len(pts) > 1 else (px, py)
            cx, cy = pts[-1]
            if (ctrl[0], ctrl[1]) == (cx, cy) and len(pts) > 2:
                ctrl = pts[0]
            ang = math.atan2(cy - ctrl[1], cx - ctrl[0]) if ctrl != (cx, cy) else math.atan2(cy - py, cx - px)
            if first_seg:
                s0 = pts[0]
                start = (px, py, math.atan2(s0[1] - py, s0[0] - px) if s0 != (px, py) else ang)
                first_seg = False
        elif c == 'A':
            x2, y2 = (cx + a[5], cy + a[6]) if rel else (a[5], a[6])
            ang = _arc_tangent_end(px, py, a[0], a[1], a[2], int(a[3]), int(a[4]), x2, y2)
            cx, cy = x2, y2
        if first_seg and start is None:
            start = (px, py, ang)
            first_seg = False
        end = (cx, cy, ang)
    if start is None or end is None:
        return None
    return start, end


def _attr(tag, name):
    m = re.search(r'(?<![\w:-])' + re.escape(name) + r'\s*=\s*"([^"]*)"', tag)
    return m.group(1) if m else None


def _fmt(v):
    return ('%.3f' % v).rstrip('0').rstrip('.') or '0'


def inline_markers(svg_text):
    """Replace marker-start/marker-end arrowheads with plain <g> paths; drop the now-unused <marker>s."""
    markers = {}
    for m in re.finditer(r'<marker\b([^>]*)>(.*?)</marker>', svg_text, flags=re.S):
        tag, body = m.group(1), m.group(2)
        mid = _attr(tag, 'id')
        if mid:
            markers[mid] = (tag, body)
    if not markers:
        return svg_text

    def chevron(mid, x, y, ang, rev, sw):
        tag, body = markers[mid]
        vb = [float(v) for v in re.split(r'[\s,]+', (_attr(tag, 'viewBox') or '0 0 3 3').strip())]
        mw = float(_attr(tag, 'markerWidth') or 3)
        mh = float(_attr(tag, 'markerHeight') or 3)
        rx = float(_attr(tag, 'refX') or 0)
        ry = float(_attr(tag, 'refY') or 0)
        unit = (_attr(tag, 'markerUnits') or 'strokeWidth')
        s = (sw if unit == 'strokeWidth' else 1.0) * min(mw / vb[2], mh / vb[3])
        orient = _attr(tag, 'orient') or '0'
        deg = math.degrees(ang) if orient.startswith('auto') else float(orient.replace('deg', '') or 0)
        if rev and orient == 'auto-start-reverse':
            deg += 180
        return ('<g transform="translate(%s,%s) rotate(%s) scale(%s) translate(%s,%s)">%s</g>'
                % (_fmt(x), _fmt(y), _fmt(deg), _fmt(s), _fmt(-(rx - vb[0])), _fmt(-(ry - vb[1])), body.strip()))

    def repl(m):
        tag = m.group(0)
        refs = {k: re.search(r'url\(#([^)]+)\)', _attr(tag, k) or '') for k in ('marker-start', 'marker-end')}
        refs = {k: v.group(1) for k, v in refs.items() if v and v.group(1) in markers}
        if not refs:
            return tag
        name = re.match(r'<(\w+)', tag).group(1)
        if name == 'line':
            try:
                x1, y1, x2, y2 = (float(_attr(tag, k) or 0) for k in ('x1', 'y1', 'x2', 'y2'))
            except ValueError:
                return tag
            ang = math.atan2(y2 - y1, x2 - x1)
            ends = ((x1, y1, ang), (x2, y2, ang))
        elif name == 'path':
            ends = path_ends(_attr(tag, 'd'))
            if not ends:
                return tag
        else:
            return tag
        sw = float(_attr(tag, 'stroke-width') or 1)
        extra = ''
        if 'marker-end' in refs:
            extra += chevron(refs['marker-end'], ends[1][0], ends[1][1], ends[1][2], False, sw)
        if 'marker-start' in refs:
            extra += chevron(refs['marker-start'], ends[0][0], ends[0][1], ends[0][2], True, sw)
        clean = re.sub(r'\s+marker-(?:start|mid|end)="[^"]*"', '', tag)
        return clean + extra

    out = re.sub(r'<(?:path|line)\b[^>]*?/>', repl, svg_text)
    # drop the marker definitions only when nothing refers to them any more
    if not re.search(r'url\(#(?:%s)\)' % '|'.join(re.escape(k) for k in markers), out):
        out = re.sub(r'<marker\b.*?</marker>', '', out, flags=re.S)
        out = re.sub(r'<defs>\s*</defs>\s*', '', out)
    return out


def check_vector(svg_text, name='SVG'):
    """Raise ValueError if the SVG is not well-formed XML or is only a raster wrapped in <svg>."""
    try:
        root = ET.fromstring(svg_text.encode('utf-8'))
    except ET.ParseError as e:
        raise ValueError('%s is not well-formed XML (%s) — it would not open in Figma or a browser' % (name, e))
    tags = [el.tag.split('}')[-1] for el in root.iter()]
    shapes = sum(tags.count(t) for t in ('path', 'rect', 'circle', 'ellipse', 'line', 'polygon', 'polyline', 'text'))
    if tags.count('image') and not shapes:
        raise ValueError('%s holds only an embedded image, not vector shapes or text — refusing to export it as an editable SVG' % name)
    return True
