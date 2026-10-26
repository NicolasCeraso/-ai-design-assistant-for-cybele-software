"""
Stage C1 — render PPTX → PDF → JPGs → slides_preview.html
For consumption by /impeccable critique downstream.

Pipeline:
  1. PPTX → PDF via render_pdf.py (PowerPoint COM, or LibreOffice when PowerPoint is absent)
  2. PyMuPDF: PDF pages → JPGs at usable resolution (~1500 px width)
  3. Build single HTML page with all slides stacked vertically, labeled

Run: python render_for_critique.py
"""

import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent.resolve()
PPTX = HERE / "output" / "Enterprise_VDI_OCI_Discovery_Demo_ESP.pptx"
PDF = HERE / "output" / "Enterprise_VDI_OCI_Discovery_Demo_ESP.pdf"
JPG_DIR = HERE / "output" / "slides"
HTML = HERE / "output" / "slides_preview.html"


def export_pptx_to_pdf():
    """PPTX → PDF through ../../render_pdf.py (PowerPoint COM if installed, else LibreOffice)."""
    import subprocess
    script = HERE.parent.parent / "render_pdf.py"
    print("[1/3] Converting PPTX → PDF…")
    r = subprocess.run([sys.executable, str(script), str(PPTX), str(PDF)], capture_output=True, text=True)
    print("     ", (r.stdout or r.stderr).strip().splitlines()[-1] if (r.stdout or r.stderr).strip() else "")
    if r.returncode != 0:
        sys.exit(r.stderr.strip()[-400:] or "PDF conversion failed")


def render_pdf_to_jpgs(width_px=1500):
    """Use PyMuPDF to render each PDF page to a JPG."""
    import fitz

    JPG_DIR.mkdir(exist_ok=True)
    # Clear stale jpgs
    for f in JPG_DIR.glob("slide-*.jpg"):
        f.unlink()

    print(f"[2/3] Rendering PDF pages to JPGs at ~{width_px}px wide…")
    doc = fitz.open(PDF)
    # Calculate zoom from desired width (PDF default is 72 dpi, page width in points)
    sample = doc[0]
    zoom = width_px / sample.rect.width
    mat = fitz.Matrix(zoom, zoom)

    for i, page in enumerate(doc):
        pix = page.get_pixmap(matrix=mat, alpha=False)
        out = JPG_DIR / f"slide-{i+1:02d}.jpg"
        pix.save(out, jpg_quality=85)

    print(f"      {doc.page_count} JPGs written to {JPG_DIR.name}/")
    doc.close()
    return list(sorted(JPG_DIR.glob("slide-*.jpg")))


def build_preview_html(jpgs):
    """Generate single HTML with all slides labeled, stacked vertically."""
    print("[3/3] Building slides_preview.html…")
    body_parts = []
    body_parts.append('<!DOCTYPE html><html lang="en"><head>')
    body_parts.append('<meta charset="utf-8"><title>Enterprise VDI on OCI ESP · preview</title>')
    body_parts.append('<style>')
    body_parts.append('body{font-family:Inter,system-ui,sans-serif;background:#f5f5f5;margin:0;padding:32px;color:#373737}')
    body_parts.append('h1{font-weight:500;font-size:16px;margin:0 0 8px;color:#0A74D6;letter-spacing:0.03em;text-transform:uppercase}')
    body_parts.append('.meta{font-size:13px;color:#6B7280;margin:0 0 32px}')
    body_parts.append('.slide{margin-bottom:48px;border-radius:8px;overflow:hidden;background:#fff;box-shadow:0 2px 16px rgba(10,26,47,0.08)}')
    body_parts.append('.slide-header{padding:14px 20px;background:#0A1A2F;color:#fff;display:flex;justify-content:space-between;align-items:center}')
    body_parts.append('.slide-num{font-weight:600;font-size:14px;letter-spacing:0.05em}')
    body_parts.append('.slide-mode{font-size:11px;color:#5BAFFF;text-transform:uppercase;letter-spacing:0.1em}')
    body_parts.append('.slide img{display:block;width:100%;height:auto}')
    body_parts.append('</style></head><body>')
    body_parts.append('<h1>Enterprise VDI on OCI · Discovery Demo (ESP) · Stage C1 preview</h1>')
    body_parts.append(f'<p class="meta">{len(jpgs)} slides · rendered via PowerPoint COM → PyMuPDF · for /impeccable critique consumption</p>')

    # Dark slides per shape.md
    dark_slides = {1, 25, 30, 33, 34}
    for jpg in jpgs:
        n = int(jpg.stem.split('-')[1])
        mode = 'dark' if n in dark_slides else 'light'
        body_parts.append(f'<div class="slide"><div class="slide-header"><span class="slide-num">Slide {n} / {len(jpgs)}</span><span class="slide-mode">{mode}</span></div>')
        body_parts.append(f'<img src="slides/{jpg.name}" alt="Slide {n}"></div>')

    body_parts.append('</body></html>')
    HTML.write_text('\n'.join(body_parts), encoding='utf-8')
    print(f"      Wrote {HTML.name}")


if __name__ == '__main__':
    t0 = time.time()
    if not PPTX.exists():
        print(f"ERROR: PPTX not found at {PPTX}")
        sys.exit(1)
    try:
        export_pptx_to_pdf()
        jpgs = render_pdf_to_jpgs()
        build_preview_html(jpgs)
        print(f"\nOK · {time.time()-t0:.1f}s · open output/slides_preview.html")
    except Exception as e:
        print(f"\nERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
