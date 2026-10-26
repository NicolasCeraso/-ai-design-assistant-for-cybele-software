#!/usr/bin/env python3
"""
Build a branded Cybele/Thinfinity whitepaper PDF from a DOCX source.

Usage:
    python build_whitepaper.py <input.docx> [output.pdf]

Pipeline:
    1. Parse DOCX → paginated HTML pages (generate_wp_pages)
    2. Apply Figma-style redesign: bullets, labeled items, callouts, pro/con (redesign_wp)
    3. Generate cover + closing pages (generate_cover_closing)
    4. Render all pages to merged PDF (generate_pdf)

Output characteristics:
    - 795x1125px pages (whitepaper format)
    - Inter font, 12px body text, line-height 16px
    - Margins: 50px top, 60px sides, 55px bottom
    - Blue bar (6px) at bottom of each content page
    - Cover: dark navy gradient, "Whitepaper" badge, white title, logos
    - Closing: contact info with SVG icons, CTA box, footer
    - Labeled items: blue title + bullet + description with separator lines
    - Bullet items: blue dot + text with separator lines
    - Callout boxes: light blue bg, blue border, rounded, "!" icon
    - Pro/con: circle-light SVG icons (green check / red cross, no fill)
    - Tables: blue header, alternating rows

Requires:
    pip install beautifulsoup4 playwright
    python -m playwright install chromium
    pip install PyMuPDF Pillow
"""

import sys
import os
import subprocess
import shutil
import tempfile
import glob
import zipfile
import xml.etree.ElementTree as ET

# Resolve paths relative to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)


def extract_title_from_docx(docx_path):
    """Extract the document title (first Heading1 or Title-styled paragraph) from a DOCX."""
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    try:
        z = zipfile.ZipFile(docx_path)
        root = ET.fromstring(z.read('word/document.xml'))
        body = root.find('.//w:body', ns)
        for child in list(body)[:10]:
            tag = child.tag.split('}')[-1]
            if tag != 'p':
                continue
            ppr = child.find('w:pPr', ns)
            style = ''
            if ppr is not None:
                ps = ppr.find('w:pStyle', ns)
                if ps is not None:
                    style = ps.get(f'{{{ns["w"]}}}val', '')
            if style in ('Title', 'Heading1'):
                text = ''.join(t.text or '' for t in child.findall('.//w:t', ns)).strip()
                if text:
                    return text
        # Fallback: first non-empty paragraph
        for child in list(body)[:5]:
            tag = child.tag.split('}')[-1]
            if tag == 'p':
                text = ''.join(t.text or '' for t in child.findall('.//w:t', ns)).strip()
                if text and len(text) > 5:
                    return text
    except Exception:
        pass
    # Last resort: use filename
    return os.path.splitext(os.path.basename(docx_path))[0]


def main():
    # ── Parse args ──
    if len(sys.argv) < 2:
        print("Usage: python build_whitepaper.py <input.docx> [output.pdf]")
        print("\nBuilds a branded Cybele/Thinfinity whitepaper PDF from a DOCX source.")
        sys.exit(1)

    docx_path = os.path.abspath(sys.argv[1])
    if not os.path.exists(docx_path):
        print(f"Error: file not found: {docx_path}")
        sys.exit(1)

    if len(sys.argv) >= 3:
        output_pdf = os.path.abspath(sys.argv[2])
    else:
        base = os.path.splitext(os.path.basename(docx_path))[0]
        output_pdf = os.path.join(os.path.dirname(docx_path), f"{base}_branded.pdf")

    # ── Create temp working directory ──
    work_dir = tempfile.mkdtemp(prefix="wp_build_")
    print(f"Working dir: {work_dir}")

    try:
        # ── Step 1: Generate HTML pages from DOCX ──
        print("\n[1/4] Generating HTML pages from DOCX...")
        gen_script = os.path.join(SCRIPT_DIR, "generate_wp_pages.py")
        env = os.environ.copy()
        env["WP_DOCX_PATH"] = docx_path
        env["WP_OUTPUT_DIR"] = work_dir
        result = subprocess.run(
            [sys.executable, gen_script],
            env=env, capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"Error in generate_wp_pages:\n{result.stderr}")
            sys.exit(1)
        pages = sorted(glob.glob(os.path.join(work_dir, "wp-page-*.html")))
        print(f"       {len(pages)} content pages generated")

        # ── Step 2: Apply redesign ──
        print("[2/4] Applying Figma-style redesign...")
        redesign_script = os.path.join(SCRIPT_DIR, "redesign_wp.py")
        env["WP_DASHBOARD"] = work_dir
        result = subprocess.run(
            [sys.executable, redesign_script],
            env=env, capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"Error in redesign_wp:\n{result.stderr}")
            sys.exit(1)
        # Print summary line
        for line in result.stdout.strip().split("\n"):
            if line.startswith("Done!"):
                print(f"       {line}")

        # ── Step 3: Generate cover + closing ──
        print("[3/4] Generating cover + closing pages...")
        cover_script = os.path.join(SCRIPT_DIR, "generate_cover_closing.py")
        env["WP_DASHBOARD"] = work_dir
        # Extract title from DOCX for the cover page
        doc_title = extract_title_from_docx(docx_path)
        env["WP_COVER_TITLE"] = doc_title
        env["WP_COVER_SUBTITLE"] = ""
        print(f"       Title: {doc_title}")
        result = subprocess.run(
            [sys.executable, cover_script],
            env=env, capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"Error in generate_cover_closing:\n{result.stderr}")
            sys.exit(1)
        print("       Cover + closing OK")

        # ── Step 4: Generate PDF ──
        print("[4/4] Rendering PDF...")
        pdf_script = os.path.join(SCRIPT_DIR, "generate_pdf.py")
        env["WP_DASHBOARD"] = work_dir
        env["WP_OUTPUT_PDF"] = output_pdf
        result = subprocess.run(
            [sys.executable, pdf_script],
            env=env, capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"Error in generate_pdf:\n{result.stderr}")
            sys.exit(1)

        size_mb = os.path.getsize(output_pdf) / (1024 * 1024)
        total_pages = len(glob.glob(os.path.join(work_dir, "wp-page-*.html")))
        print(f"\nDone! {output_pdf}")
        print(f"{total_pages} pages, {size_mb:.2f} MB")

    finally:
        # Cleanup temp dir
        shutil.rmtree(work_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
