# Exports a deliverable. SVG is treated as the editable BASE:
#   - fmt=svg  → the original vector SVG, with external <image href="*.svg"> icons inlined as nested
#                <svg> (self-contained, still fully editable — text stays text, shapes stay shapes).
#   - fmt=png/jpg → the SVG rendered by headless Chrome (faithful: icons, fonts, gradients kept).
#   - fmt=pdf  → the SVG printed to a vector PDF at its exact size by headless Chrome.
# When there is no vector SVG (PPTX/Whitepaper deliverables), the PDF preview is the source and
# PyMuPDF handles it: fmt=svg via get_svg_image, png/jpg via pixmap, pdf via page slicing.
# Multi-page controls (single canvas vs per page, all vs selection) apply to the PDF source; an SVG
# is a single canvas. Emits JSON {ok, file, name, zip} on stdout.
import sys, os, json, argparse, zipfile, io, re, base64, subprocess, tempfile, glob, uuid, threading
from concurrent.futures import ThreadPoolExecutor

def parse_pages(sel, n):
    if not sel or sel == 'all':
        return list(range(n))
    out = set()
    for part in str(sel).split(','):
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            try:
                a, b = part.split('-', 1); a = int(a); b = int(b)
            except Exception:
                continue
            for p in range(min(a, b), max(a, b) + 1):
                if 1 <= p <= n: out.add(p - 1)
        else:
            try:
                p = int(part)
            except Exception:
                continue
            if 1 <= p <= n: out.add(p - 1)
    return sorted(out) if out else list(range(n))

def find_chrome():
    for p in [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
              r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"]:
        if os.path.exists(p):
            return p
    raise RuntimeError('no Chrome/Edge found for SVG rendering')

def svg_dims(svg_text):
    m = re.search(r'viewBox\s*=\s*"[\s]*([\d.\-]+)[\s,]+([\d.\-]+)[\s,]+([\d.\-]+)[\s,]+([\d.\-]+)', svg_text)
    if m:
        w = float(m.group(3)); h = float(m.group(4))
        if w > 0 and h > 0:
            return w, h
    def dim(name):
        mm = re.search(name + r'\s*=\s*"([\d.]+)', svg_text)
        return float(mm.group(1)) if mm else 0
    return (dim('width') or 800), (dim('height') or 600)

def inline_svg(svg_path):
    """Return the SVG with external <image href='*.svg'> inlined as nested <svg> (keeps it vector
    and editable), and raster refs embedded as data URIs — so the file is fully self-contained."""
    d = os.path.dirname(svg_path)
    txt = open(svg_path, encoding='utf-8').read()
    def attr(tag, name):
        mm = re.search(r'\b' + name + r'\s*=\s*"([^"]*)"', tag)
        return mm.group(1) if mm else None
    def repl(m):
        tag = m.group(0)
        href = attr(tag, 'href') or attr(tag, 'xlink:href')
        if not href:
            return tag
        ref = os.path.normpath(os.path.join(d, href))
        ext = os.path.splitext(ref)[1].lower()
        x, y, w, h = attr(tag, 'x'), attr(tag, 'y'), attr(tag, 'width'), attr(tag, 'height')
        if ext == '.svg' and os.path.exists(ref):
            inner = open(ref, encoding='utf-8').read()
            vb = re.search(r'viewBox\s*=\s*"([^"]+)"', inner)
            body = re.sub(r'^.*?<svg[^>]*>', '', inner, count=1, flags=re.S)
            body = re.sub(r'</svg>\s*$', '', body, flags=re.S)
            pos = ''.join(' %s="%s"' % (k, v) for k, v in [('x', x), ('y', y), ('width', w), ('height', h)] if v)
            vbattr = ' viewBox="%s"' % vb.group(1) if vb else ''
            return '<svg%s%s overflow="visible" preserveAspectRatio="xMidYMid meet">%s</svg>' % (pos, vbattr, body)
        if os.path.exists(ref):
            mime = {'png': 'image/png', 'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'gif': 'image/gif', 'webp': 'image/webp'}.get(ext.lstrip('.'), 'application/octet-stream')
            data = base64.b64encode(open(ref, 'rb').read()).decode()
            return re.sub(r'(?:xlink:)?href\s*=\s*"[^"]*"', 'href="data:%s;base64,%s"' % (mime, data), tag, count=1)
        return tag
    txt = re.sub(r'<image\b[^>]*/>', repl, txt)
    txt = re.sub(r'<image\b[^>]*>.*?</image>', repl, txt, flags=re.S)
    return txt

_LOCAL = threading.local()
def _chrome_profile(outdir):
    """A throwaway Chrome profile per worker thread, reused for every design that thread renders.
    Building a fresh profile is most of the cost of a headless launch, so reuse matters — but Chrome
    locks a profile while it runs, so concurrent renders cannot share one. Per thread gives both."""
    prof = getattr(_LOCAL, 'profile', None)
    if prof is None or not os.path.isdir(prof):
        prof = _LOCAL.profile = tempfile.mkdtemp(dir=outdir)
    return prof

# Flags that only skip first-run chrome (profile setup, default-browser prompt, extensions) — they
# never touch how the page is painted.
CHROME_COLD = ['--no-first-run', '--no-default-browser-check', '--disable-extensions']

def chrome_png(svg_path, scale, transparent, outdir):
    W, H = svg_dims(open(svg_path, encoding='utf-8').read())
    prof = _chrome_profile(outdir)
    outp = os.path.join(outdir, '_shot_%s.png' % uuid.uuid4().hex[:8])
    bg = '00000000' if transparent else 'FFFFFFFF'
    args = [find_chrome(), '--headless=new', '--disable-gpu', '--hide-scrollbars',
            '--force-device-scale-factor=%s' % scale, '--window-size=%d,%d' % (round(W), round(H)),
            '--default-background-color=%s' % bg, '--user-data-dir=' + prof,
            *CHROME_COLD, '--screenshot=' + outp, 'file:///' + svg_path.replace('\\', '/')]
    r = subprocess.run(args, timeout=90, capture_output=True)
    if not os.path.exists(outp):
        raise RuntimeError('chrome screenshot failed for %s: %s' % (
            os.path.basename(svg_path), (r.stderr or b'').decode('utf-8', 'replace').strip()[-300:]))
    return open(outp, 'rb').read()

def chrome_pdf(svg_path, outdir):
    inlined = inline_svg(svg_path)
    W, H = svg_dims(inlined)
    html = ('<!doctype html><html><head><meta charset="utf-8"><style>'
            '@page{size:%dpx %dpx;margin:0}html,body{margin:0;padding:0}svg{display:block}'
            '</style></head><body>%s</body></html>') % (round(W), round(H), inlined)
    prof = _chrome_profile(outdir)
    # Unique per call: renders run in parallel, and a shared scratch name meant two threads
    # overwrote each other's wrapper — every page came out as whichever design wrote last, or
    # half-written and rendered as raw text.
    tag = uuid.uuid4().hex[:8]
    htmlp = os.path.join(outdir, '_wrap_%s.html' % tag); open(htmlp, 'w', encoding='utf-8').write(html)
    outp = os.path.join(outdir, '_doc_%s.pdf' % tag)
    args = [find_chrome(), '--headless=new', '--disable-gpu', '--no-pdf-header-footer',
            '--user-data-dir=' + prof, *CHROME_COLD, '--print-to-pdf=' + outp, 'file:///' + htmlp.replace('\\', '/')]
    r = subprocess.run(args, timeout=90, capture_output=True)
    if not os.path.exists(outp):
        raise RuntimeError('chrome print-to-pdf failed for %s: %s' % (
            os.path.basename(svg_path), (r.stderr or b'').decode('utf-8', 'replace').strip()[-300:]))
    return open(outp, 'rb').read()

def encode_fit(im, fmt, transparent, maxbytes):
    """Encode a PIL image to png/jpg. If maxbytes is set, progressively reduce scale (and JPEG
    quality / PNG palette) until the output fits under the byte budget; return the smallest tried."""
    from PIL import Image
    def enc(work, q=None):
        buf = io.BytesIO()
        if fmt == 'jpg':
            (work if work.mode == 'RGB' else flatten_to_rgb(work)).save(buf, 'JPEG', quality=q or 92)
        else:
            work.save(buf, 'PNG', optimize=True)
        return buf.getvalue()
    if not maxbytes:
        return enc(im)
    best = None
    for s in [1.0, 0.85, 0.7, 0.55, 0.45, 0.35, 0.25, 0.18]:
        work = im if s == 1.0 else im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)
        if fmt == 'jpg':
            for q in [88, 78, 68, 58, 48, 38, 30]:
                d = enc(work, q)
                if best is None or len(d) < len(best): best = d
                if len(d) <= maxbytes: return d
        else:
            cands = [enc(work)]
            try:
                pal = (work.convert('RGBA') if transparent else work.convert('RGB')).quantize(colors=256, method=Image.FASTOCTREE if transparent else Image.MEDIANCUT)
                b = io.BytesIO(); pal.save(b, 'PNG', optimize=True); cands.append(b.getvalue())
            except Exception:
                pass
            d = min(cands, key=len)
            if best is None or len(d) < len(best): best = d
            if len(d) <= maxbytes: return d
    return best

def _outbase(a, paths):
    """Base name for a combined download. The console sends a generic, document-type name
    ("blog-visuals"); without one, fall back to the files' common prefix."""
    return (getattr(a, 'name', '') or '').strip() or _setname(paths)

def _setname(paths):
    """A shared, tidy name for a combined output built from several files."""
    bases = [os.path.splitext(os.path.basename(p))[0] for p in paths]
    pre = re.sub(r'[_\-\s]*\d.*$', '', os.path.commonprefix(bases)).strip('_- ')
    return pre or 'designs'

def export_pptx_from_svgs(svg_paths, out, base=None):
    """Build an EDITABLE .pptx with one slide per SVG. Each SVG is embedded as a native Scalable
    Vector Graphic — the same package PowerPoint writes: a picture whose PNG fallback (rendered by
    headless Chrome) is paired with the SVG through the `svgBlip` extension. In PowerPoint, right-click
    -> Convert to Shape makes it fully editable. Needs neither PowerPoint nor Windows."""
    from pptx import Presentation
    from pptx.opc.constants import RELATIONSHIP_TYPE as RT
    from pptx.opc.package import Part
    from pptx.opc.packuri import PackURI
    from pptx.util import Emu
    from lxml import etree
    w, h = svg_dims(open(svg_paths[0], encoding='utf-8').read())
    SW = 12192000                                   # 13.333 in, in EMU
    SH = round(SW * (h / w if w else 0.5625))
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(SW), Emu(SH)
    blank = prs.slide_layouts[6]
    A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
    R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
    ASVG = 'http://schemas.microsoft.com/office/drawing/2016/SVG/main'
    for s in svg_paths:
        slide = prs.slides.add_slide(blank)
        fallback = chrome_png(s, 2, True, out)      # PNG for viewers that cannot draw SVG
        pic = slide.shapes.add_picture(io.BytesIO(fallback), 0, 0, Emu(SW), Emu(SH))
        pic.name = os.path.splitext(os.path.basename(s))[0]
        svg_part = Part(prs.part.package.next_partname('/ppt/media/svg%d.svg'), 'image/svg+xml',
                        prs.part.package, inline_svg(s).encode('utf-8'))
        rid = slide.part.relate_to(svg_part, RT.IMAGE)
        blip = pic._element.xpath('.//a:blip')[0]
        ext_lst = etree.SubElement(blip, '{%s}extLst' % A)
        ext = etree.SubElement(ext_lst, '{%s}ext' % A, uri='{96DAC541-7B7A-43D3-8B79-37D633B846F1}')
        etree.SubElement(ext, '{%s}svgBlip' % ASVG, nsmap={'asvg': ASVG}).set('{%s}embed' % R, rid)
    buf = io.BytesIO()
    prs.save(buf)
    return ((base or _setname(svg_paths)) + '.pptx', buf.getvalue())

WORKERS = 4   # concurrent headless Chrome renders; keeps a 16-design set under a few seconds

def _parallel(fn, items):
    """Map fn over items, in order, a few at a time. One worker for a single item (no thread at all
    for the common case of one design)."""
    if len(items) <= 1:
        return [fn(x) for x in items]
    with ThreadPoolExecutor(max_workers=min(WORKERS, len(items))) as ex:
        return list(ex.map(fn, items))

def export_from_svg(a, svg_paths, out):
    # svg_paths may be a single path or several (a multi-SVG deliverable, e.g. one file per design).
    # Everything is derived from the real vectors, so outputs stay editable / true-vector.
    if isinstance(svg_paths, str):
        svg_paths = [svg_paths]
    # Honour the page/selection choice: export only the selected files (sorted in page order).
    if len(svg_paths) > 1:
        svg_paths = [svg_paths[i] for i in parse_pages(a.pages, len(svg_paths))]
    if a.fmt == 'pptx':
        return [export_pptx_from_svgs(svg_paths, out, _outbase(a, svg_paths))]
    if a.fmt == 'pdf' and len(svg_paths) > 1:
        # Combine into ONE multi-page vector PDF (selectable text/paths, not image pages).
        import pymupdf as fitz
        merged = fitz.open()
        for data in _parallel(lambda sp: chrome_pdf(sp, out), svg_paths):
            page = fitz.open('pdf', data); merged.insert_pdf(page); page.close()
        data = merged.tobytes(); merged.close()
        return [(_outbase(a, svg_paths) + '.pdf', data)]
    def one(svg_path):
        base = os.path.splitext(os.path.basename(svg_path))[0]
        if a.fmt == 'svg':
            return (base + '.svg', inline_svg(svg_path).encode('utf-8'))
        if a.fmt == 'pdf':
            return (base + '.pdf', chrome_pdf(svg_path, out))
        # png / jpg — render the SVG with Chrome, then encode (optionally fit to a byte budget)
        from PIL import Image
        transparent = a.fmt == 'png' and a.bg == 'transparent'
        im = Image.open(io.BytesIO(chrome_png(svg_path, a.scale, transparent, out)))
        return (base + ('.jpg' if a.fmt == 'jpg' else '.png'), encode_fit(im, a.fmt, transparent, a.maxbytes))
    return _parallel(one, svg_paths)

def flatten_to_rgb(im):
    from PIL import Image
    if im.mode == 'RGBA':
        bg = Image.new('RGB', im.size, (255, 255, 255)); bg.paste(im, mask=im.split()[3]); return bg
    return im.convert('RGB')

def export_from_raster(a, src, out):
    import pymupdf as fitz
    from PIL import Image
    base = os.path.splitext(os.path.basename(src))[0]
    ext = os.path.splitext(src)[1].lower().lstrip('.')
    results = []
    is_pdf = ext == 'pdf'
    doc = fitz.open(src)
    n = doc.page_count or 1
    sel = parse_pages(a.pages, n)
    if a.fmt == 'pdf':
        pdfdoc = doc if is_pdf else fitz.open('pdf', doc.convert_to_pdf())
        selp = parse_pages(a.pages, pdfdoc.page_count or 1)
        if a.layout == 'pages' and len(selp) > 1:
            for i in selp:
                nd = fitz.open(); nd.insert_pdf(pdfdoc, from_page=i, to_page=i); results.append((f"{base}_p{i+1}.pdf", nd.tobytes())); nd.close()
        else:
            nd = fitz.open()
            for i in selp: nd.insert_pdf(pdfdoc, from_page=i, to_page=i)
            results.append((f"{base}.pdf", nd.tobytes())); nd.close()
    elif a.fmt == 'svg':
        for i in sel:
            results.append((f"{base}.svg" if len(sel) == 1 else f"{base}_p{i+1}.svg", doc[i].get_svg_image().encode('utf-8')))
    else:
        alpha = (a.fmt == 'png' and a.bg == 'transparent')
        imgs = [(i, Image.frombytes('RGBA' if (px := doc[i].get_pixmap(matrix=fitz.Matrix(a.scale, a.scale), alpha=alpha)).alpha else 'RGB', (px.width, px.height), px.samples)) for i in sel]
        eo = 'jpg' if a.fmt == 'jpg' else 'png'
        transparent = (a.fmt == 'png' and alpha)
        if a.layout == 'canvas':
            W = max(im.width for _, im in imgs); H = sum(im.height for _, im in imgs)
            mode = 'RGBA' if transparent else 'RGB'
            canvas = Image.new(mode, (W, H), (255, 255, 255, 0) if transparent else (255, 255, 255)); y = 0
            for _, im in imgs:
                paste = im if im.mode == mode else (flatten_to_rgb(im) if mode == 'RGB' else im.convert('RGBA'))
                canvas.paste(paste, ((W - paste.width) // 2, y)); y += paste.height
            results.append((f"{base}.{eo}", encode_fit(canvas, a.fmt, transparent, a.maxbytes)))
        else:
            for i, im in imgs:
                results.append((f"{base}.{eo}" if len(sel) == 1 else f"{base}_p{i+1}.{eo}", encode_fit(im, a.fmt, transparent, a.maxbytes)))
    return results

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--svg', default='')      # vector source (preferred base)
    ap.add_argument('--raster', default='')   # pdf/image source (for PPTX/Whitepaper)
    ap.add_argument('--fmt', default='png')   # png | jpg | svg | pdf
    ap.add_argument('--bg', default='opaque')
    ap.add_argument('--layout', default='canvas')
    ap.add_argument('--pages', default='all')
    ap.add_argument('--scale', type=float, default=2.0)
    ap.add_argument('--maxbytes', type=int, default=0)  # >0: fit raster output under this size
    ap.add_argument('--name', default='')      # generic base name for a whole-run download
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    # SVG is the base whenever we have one; otherwise fall back to the raster/PDF source.
    # --svg may carry several newline-separated vector files (a multi-SVG deliverable).
    svglist = [p for p in a.svg.split('\n') if p.strip() and os.path.exists(p.strip())]
    if svglist:
        results = export_from_svg(a, [p.strip() for p in svglist], a.out)
    elif a.raster and os.path.exists(a.raster):
        results = export_from_raster(a, a.raster, a.out)
    else:
        raise RuntimeError('no source available')
    # write single file or zip
    for f in glob.glob(os.path.join(a.out, '_shot.png')) + glob.glob(os.path.join(a.out, '_wrap.html')) + glob.glob(os.path.join(a.out, '_doc.pdf')):
        pass  # keep temp render outputs out of the final result set (handled by naming)
    finals = [r for r in results if r]
    if len(finals) == 1:
        fn, data = finals[0]
        # A whole-run download carries the generic name too, so a one-design task lands as
        # "blog-visuals.png". A hand-picked selection keeps the design's own filename (the console
        # only sends --name when the export is the complete set).
        if (a.name or '').strip():
            fn = a.name.strip() + os.path.splitext(fn)[1]
        outp = os.path.join(a.out, fn)
        open(outp, 'wb').write(data)
        print(json.dumps({"ok": True, "file": outp, "name": fn, "zip": False}))
    else:
        base = (a.name or '').strip() or (os.path.splitext(finals[0][0])[0].rsplit('_p', 1)[0] if finals else 'export')
        zipname = base + '.zip'; outp = os.path.join(a.out, zipname)
        with zipfile.ZipFile(outp, 'w', zipfile.ZIP_DEFLATED) as z:
            for fn, data in finals: z.writestr(fn, data)
        print(json.dumps({"ok": True, "file": outp, "name": zipname, "zip": True}))

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)})); sys.exit(1)
