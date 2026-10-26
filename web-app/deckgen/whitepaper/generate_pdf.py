#!/usr/bin/env python3
"""
Generate a single PDF from all 34 whitepaper HTML pages using Playwright.
Each page is rendered at 795x1125px and captured as a PDF page.
Output: WP_OUTPUT_PDF (build_whitepaper.py sets WP_DASHBOARD and WP_OUTPUT_PDF)
"""

import os
import glob
import tempfile
from playwright.sync_api import sync_playwright

DASHBOARD = os.environ.get('WP_DASHBOARD', os.path.join(tempfile.gettempdir(), 'wp_pages'))
OUTPUT_PDF = os.environ.get('WP_OUTPUT_PDF', os.path.abspath('whitepaper.pdf'))

# Page dimensions in px (match the HTML)
PAGE_W = 795
PAGE_H = 1125

# Convert px to inches (96 dpi) then to mm
PX_TO_MM = 25.4 / 96
PAGE_W_MM = PAGE_W * PX_TO_MM
PAGE_H_MM = PAGE_H * PX_TO_MM


def main():
    files = sorted(glob.glob(os.path.join(DASHBOARD, 'wp-page-*.html')))
    print(f"Found {len(files)} HTML pages")

    pdf_pages = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)

        for i, html_file in enumerate(files):
            page = browser.new_page(viewport={'width': PAGE_W, 'height': PAGE_H})
            file_url = 'file:///' + html_file.replace('\\', '/')
            page.goto(file_url, wait_until='networkidle', timeout=30000)
            page.wait_for_timeout(1000)  # let fonts + icons load

            # Generate single-page PDF
            pdf_bytes = page.pdf(
                width=f'{PAGE_W_MM}mm',
                height=f'{PAGE_H_MM}mm',
                margin={'top': '0mm', 'bottom': '0mm', 'left': '0mm', 'right': '0mm'},
                print_background=True,
                prefer_css_page_size=False,
            )
            pdf_pages.append(pdf_bytes)
            page.close()

            name = os.path.basename(html_file)
            print(f"  [{i+1}/{len(files)}] {name} ({len(pdf_bytes):,} bytes)")

        browser.close()

    # Merge all single-page PDFs into one
    print("\nMerging pages...")
    try:
        import fitz  # PyMuPDF
        merged = fitz.open()
        for pdf_bytes in pdf_pages:
            doc = fitz.open(stream=pdf_bytes, filetype='pdf')
            merged.insert_pdf(doc)
            doc.close()
        merged.save(OUTPUT_PDF)
        merged.close()
    except ImportError:
        # Fallback: use pypdf
        from pypdf import PdfMerger
        import tempfile
        merger = PdfMerger()
        tmp_files = []
        for j, pdf_bytes in enumerate(pdf_pages):
            tmp = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
            tmp.write(pdf_bytes)
            tmp.close()
            tmp_files.append(tmp.name)
            merger.append(tmp.name)
        merger.write(OUTPUT_PDF)
        merger.close()
        for tf in tmp_files:
            os.unlink(tf)

    size_mb = os.path.getsize(OUTPUT_PDF) / (1024 * 1024)
    print(f"\nDone! PDF saved: {OUTPUT_PDF}")
    print(f"Size: {size_mb:.2f} MB ({len(pdf_pages)} pages)")


if __name__ == '__main__':
    main()
