# -*- coding: utf-8 -*-
"""
Cybele brand iconography -> transparent PNGs for PPTX  (portable variant).

Same cache format and rasterising method as `_brand_icons.py` (one Edge headless
launch, a 256 px sprite sheet, alpha-trimmed cells keyed `name_rrggbb` in
`_icon_cache/`), with two differences:

  * `brand-icon-lib.js` is *discovered* among the known console locations instead
    of being hardcoded to one machine's Desktop copy, so a clone of the repo works.
  * adds `pic_px()` for builders that lay out in 1280x720 canvas pixels.

Source of truth is the brandbook icon set exported by the console
(`brand-icon-lib.js`, 131 icons, every path fill="currentColor") — the real brand
shapes, not look-alikes.
"""
import json, os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
# The cache is keyed by name+colour only, so a new icon library needs its own
# folder or stale shapes come back: CYBELE_ICON_CACHE points at a fresh one.
CACHE = os.environ.get('CYBELE_ICON_CACHE') or os.path.join(HERE, '_icon_cache')
def _find_edge():
    for p in (os.environ.get('CYBELE_EDGE'),
              r"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
              r"C:/Program Files/Microsoft/Edge/Application/msedge.exe"):
        if p and os.path.exists(p):
            return p
    return r"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"


EDGE = _find_edge()
CELL = 256          # px per sprite cell
COLS = 8
PXE = 9525          # EMU per canvas pixel (1280x720 canvas on a 13.333x7.5in slide)

LIB_CANDIDATES = [
    os.environ.get('CYBELE_ICON_LIB'),
    # this file sits in <repo>/presentations/reference_builder/; the lib in <repo>/web-app/
    os.path.join(HERE, '..', '..', 'web-app', 'brand-icon-lib.js'),
    os.path.join(HERE, 'brand-icon-lib.js'),
]

_lib = None


def lib_path():
    for p in LIB_CANDIDATES:
        if p and os.path.exists(p):
            return p
    raise FileNotFoundError(
        'brand-icon-lib.js not found. Looked in: '
        + ', '.join(repr(p) for p in LIB_CANDIDATES if p))


def lib():
    global _lib
    if _lib is None:
        src = open(lib_path(), encoding='utf-8').read()
        # The library now carries several `window.X = {...};` statements (icons,
        # legacy, groups, keywords); the icons are the first object.
        _lib, _ = json.JSONDecoder().raw_decode(src[src.index('{'):])
    return _lib


def names():
    return sorted(lib().keys())


def _key(name, hexcolor):
    return '%s_%s' % (name, hexcolor.lstrip('#').lower())


def _meta_path():
    return os.path.join(CACHE, 'index.json')


def build(pairs):
    """pairs: iterable of (icon_name, '#RRGGBB'). Warms the cache in one launch."""
    from PIL import Image
    os.makedirs(CACHE, exist_ok=True)
    meta = {}
    if os.path.exists(_meta_path()):
        meta = json.load(open(_meta_path(), encoding='utf-8'))

    pairs = sorted(set(pairs))
    todo = [p for p in pairs if _key(*p) not in meta
            or not os.path.exists(os.path.join(CACHE, _key(*p) + '.png'))]
    if todo:
        L = lib()
        cells = []
        for name, col in todo:
            if name not in L:
                raise KeyError('no brand icon named %r' % name)
            svg = (L[name].replace('width="100%"', 'width="%d"' % (CELL - 24))
                          .replace('height="100%"', 'height="%d"' % (CELL - 24)))
            cells.append('<div class="c" style="color:%s">%s</div>' % (col, svg))
        rows = (len(cells) + COLS - 1) // COLS
        html = ('<!doctype html><meta charset="utf-8"><style>'
                'html,body{margin:0;padding:0;background:transparent}'
                '.g{display:grid;grid-template-columns:repeat(%d,%dpx);'
                'grid-auto-rows:%dpx;width:%dpx}'
                '.c{width:%dpx;height:%dpx;display:flex;align-items:center;'
                'justify-content:center}'
                '.c svg{max-width:%dpx;max-height:%dpx}'
                '</style><div class="g">%s</div>'
                % (COLS, CELL, CELL, COLS * CELL, CELL, CELL,
                   CELL - 24, CELL - 24, ''.join(cells)))
        hp = os.path.join(CACHE, '_sheet.html')
        sp = os.path.join(CACHE, '_sheet.png')
        open(hp, 'w', encoding='utf-8').write(html)
        if os.path.exists(sp):
            os.remove(sp)
        subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--hide-scrollbars',
                        '--default-background-color=00000000',
                        '--window-size=%d,%d' % (COLS * CELL, rows * CELL),
                        '--screenshot=' + sp, 'file:///' + hp.replace(chr(92), '/')],
                       check=True, capture_output=True, timeout=240)
        sheet = Image.open(sp).convert('RGBA')
        for i, (name, col) in enumerate(todo):
            x, y = (i % COLS) * CELL, (i // COLS) * CELL
            cell = sheet.crop((x, y, x + CELL, y + CELL))
            bbox = cell.getchannel('A').getbbox()
            if not bbox:
                raise RuntimeError('icon %r rendered empty' % name)
            trimmed = cell.crop(bbox)
            k = _key(name, col)
            trimmed.save(os.path.join(CACHE, k + '.png'))
            meta[k] = {'w': trimmed.width, 'h': trimmed.height}
        json.dump(meta, open(_meta_path(), 'w', encoding='utf-8'), indent=1)
        os.remove(sp)
    return meta


def path_and_size(name, hexcolor, box):
    """PNG path + (w,h) in the same unit as `box`, aspect kept, fitted in a square."""
    meta = json.load(open(_meta_path(), encoding='utf-8'))
    m = meta[_key(name, hexcolor)]
    sc = box / max(m['w'], m['h'])
    return os.path.join(CACHE, _key(name, hexcolor) + '.png'), m['w'] * sc, m['h'] * sc


def pic_px(slide, name, x, y, box, hexcolor):
    """Place a brand icon centred in a `box`-pixel square at canvas px (x, y).

    Every icon reads at the same optical size whatever its own proportion, which
    is what keeps a set of them on one slide looking like one system.
    """
    from pptx.util import Emu
    path, w, h = path_and_size(name, hexcolor, box)
    def E(v): return Emu(int(round(v * PXE)))
    return slide.shapes.add_picture(path, E(x + (box - w) / 2.0),
                                    E(y + (box - h) / 2.0), E(w), E(h))
