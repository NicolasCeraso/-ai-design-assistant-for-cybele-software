#!/usr/bin/env python3
"""
Generate individual HTML pages for the whitepaper interior (pages 03+).
Reads the DOCX, parses all content, paginates into 795x1125px pages,
and saves each as wp-page-XX.html in WP_OUTPUT_DIR (build_whitepaper.py sets both env vars).
"""

import zipfile
import xml.etree.ElementTree as ET
import os
import re
import sys
import tempfile
import html as html_mod
from math import ceil

# ── Paths (set via env vars by build_whitepaper.py) ──────────────────────────
DOCX_PATH = os.environ.get("WP_DOCX_PATH")
if not DOCX_PATH:
    sys.exit("WP_DOCX_PATH is not set — run whitepaper/build_whitepaper.py <input.docx> instead.")
OUTPUT_DIR = os.environ.get("WP_OUTPUT_DIR", os.path.join(tempfile.gettempdir(), "wp_pages"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Constants for pagination ───────────────────────────────────────────────────
# Calibrated for 12px Inter, line-height 16px, 60px margins, redesign transforms
PAGE_HEIGHT = 1125
PAD_TOP = 50
PAD_BOT = 55
USABLE_HEIGHT = PAGE_HEIGHT - PAD_TOP - PAD_BOT  # 1020
SAFE_HEIGHT = 840  # conservative: accounts for redesign adding height (borders, padding, callouts)
CONTENT_WIDTH = 675  # 795 - 60 left - 60 right
CHARS_PER_LINE = 75  # approximate for 12px Inter in 675px

# Element height estimates (for 12px body text, line-height 16px)
H1_HEIGHT = 66  # 26px line + 20px margin + 20px page-break padding
H2_HEIGHT = 50  # 21px line + 20px margin-top + 8px margin-bottom
H3_HEIGHT = 34  # 16px line + 14px margin-top + 5px margin-bottom
TABLE_ROW_HEIGHT = 28
TABLE_OVERHEAD = 24  # margins
CALLOUT_OVERHEAD = 50  # callout box padding + margin + title
LI_HEIGHT = 26  # 16px + 10px padding
IMG_FIXED_W = 400  # every screenshot gets exactly this width (px); height follows its aspect ratio


def estimate_para_height(text, font_height=16, margin=10):
    """Estimate rendered height of a paragraph based on character count."""
    if not text:
        return margin
    lines = ceil(len(text) / CHARS_PER_LINE)
    return lines * font_height + margin


def estimate_table_height(rows):
    """Estimate rendered height of a table."""
    return len(rows) * TABLE_ROW_HEIGHT + TABLE_OVERHEAD


# ── Parse DOCX ────────────────────────────────────────────────────────────────
def parse_docx(path):
    """Parse the DOCX and return a list of content elements."""
    z = zipfile.ZipFile(path)
    xml_data = z.read("word/document.xml")
    root = ET.fromstring(xml_data)

    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    body = root.find(".//w:body", ns)

    # Picture relationships (rId -> media file inside the DOCX)
    rels = {}
    try:
        rroot = ET.fromstring(z.read("word/_rels/document.xml.rels"))
        for rel in rroot:
            rels[rel.get("Id")] = rel.get("Target")
    except KeyError:
        pass
    A_BLIP = "{http://schemas.openxmlformats.org/drawingml/2006/main}blip"
    R_EMBED = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed"

    elements = []
    for child in body:
        tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag

        if tag == "p":
            runs = child.findall(".//w:r", ns)
            full_text = ""
            bold_ranges = []
            for run in runs:
                t = run.find("w:t", ns)
                if t is not None and t.text:
                    rpr = run.find("w:rPr", ns)
                    bold = False
                    if rpr is not None:
                        b = rpr.find("w:b", ns)
                        if b is not None:
                            val = b.get(
                                "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val",
                                "1",
                            )
                            bold = val != "0"
                    start = len(full_text)
                    full_text += t.text
                    if bold:
                        bold_ranges.append((start, len(full_text)))

                    # Also check for bCs as fallback
                    if not bold and rpr is not None:
                        bcs = rpr.find("w:bCs", ns)
                        if bcs is not None:
                            val = bcs.get(
                                "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val",
                                "1",
                            )
                            if val != "0":
                                bold_ranges.append((start, len(full_text)))

            # Deduplicate bold ranges
            seen = set()
            unique_bold = []
            for br in bold_ranges:
                if br not in seen:
                    seen.add(br)
                    unique_bold.append(br)
            bold_ranges = unique_bold

            ppr = child.find("w:pPr", ns)
            style = ""
            if ppr is not None:
                pstyle = ppr.find("w:pStyle", ns)
                if pstyle is not None:
                    style = pstyle.get(
                        "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val",
                        "",
                    )

            all_bold = (
                len(bold_ranges) > 0
                and bold_ranges[0][0] == 0
                and bold_ranges[-1][1] >= len(full_text.rstrip())
            )

            if full_text.strip():
                elements.append(
                    {
                        "type": "paragraph",
                        "text": full_text.strip(),
                        "style": style,
                        "bold": all_bold,
                        "bold_ranges": bold_ranges,
                    }
                )

            # Pictures anchored in this paragraph (kept in document order)
            for blip in child.iter(A_BLIP):
                target = rels.get(blip.get(R_EMBED))
                if not target:
                    continue
                media = "word/" + target.lstrip("/").replace("word/", "", 1)
                try:
                    data = z.read(media)
                except KeyError:
                    continue
                elements.append({"type": "image", "name": os.path.basename(media), "data": data})

        elif tag == "tbl":
            rows_data = []
            for row in child.findall(".//w:tr", ns):
                cells = []
                for cell in row.findall(".//w:tc", ns):
                    cell_text = ""
                    for p in cell.findall(".//w:p", ns):
                        for r in p.findall(".//w:r", ns):
                            t = r.find("w:t", ns)
                            if t is not None and t.text:
                                cell_text += t.text
                        cell_text += " "
                    cells.append(cell_text.strip())
                rows_data.append(cells)
            if rows_data:
                elements.append({"type": "table", "rows": rows_data})

    return elements


# ── Classify elements ─────────────────────────────────────────────────────────
def classify_element(elem):
    """
    Classify a parsed element into a rendering type:
    'h1', 'h2', 'h3', 'bullet', 'callout', 'paragraph', 'table'
    Returns (render_type, elem)
    """
    if elem["type"] == "table":
        return "table", elem
    if elem["type"] == "image":
        return "image", elem

    text = elem["text"]
    style = elem["style"]
    bold = elem["bold"]

    # Heading1 style → h1
    if style == "Heading1":
        return "h1", elem

    # Heading3 style → detect if it's really h2 (like "1.1 ...") or h3
    if style == "Heading3":
        # Numbered sections like "1.1", "2.3" etc → h2
        if re.match(r"^\d+\.\d+\s", text):
            return "h2", elem
        return "h2", elem  # All Heading3 styles map to h2 visually

    # Heading4 style → h3
    if style == "Heading4":
        return "h3", elem

    # Bold short lines that look like sub-headings
    if bold and len(text) < 80:
        # Patterns like "AWS Model:", "Thinfinity VDI on OCI Model:", etc.
        if text.endswith(":"):
            return "h3", elem
        # Very short bold lines that are labels
        if len(text) < 40 and text not in ("", " "):
            return "h3", elem

    # Detect bullet-like items (lines starting with bullet chars or short items in a list context)
    bullet_patterns = [
        r"^[\u2022\u25CF\u25CB\u2013\u2014\u00B7]\s",  # bullet chars
        r"^[-\*]\s",  # dash or asterisk bullets
    ]
    for pat in bullet_patterns:
        if re.match(pat, text):
            return "bullet", elem

    return "paragraph", elem


def apply_bold_ranges(text, bold_ranges):
    """Apply <strong> tags based on bold_ranges, with HTML escaping."""
    if not bold_ranges:
        return html_mod.escape(text)

    # Merge overlapping ranges
    merged = []
    for s, e in sorted(bold_ranges):
        if merged and s <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], e))
        else:
            merged.append((s, e))

    result = []
    last = 0
    for s, e in merged:
        if s > last:
            result.append(html_mod.escape(text[last:s]))
        result.append("<strong>" + html_mod.escape(text[s:e]) + "</strong>")
        last = e
    if last < len(text):
        result.append(html_mod.escape(text[last:]))
    return "".join(result)


def render_element(rtype, elem):
    """Render a classified element to HTML string."""
    if rtype == "table":
        rows = elem["rows"]
        lines = ['<table>']
        for i, row in enumerate(rows):
            lines.append("  <tr>")
            tag = "th" if i == 0 else "td"
            for cell in row:
                lines.append(f"    <{tag}>{html_mod.escape(cell)}</{tag}>")
            lines.append("  </tr>")
        lines.append("</table>")
        return "\n".join(lines)

    if rtype == "image":
        return (f'<figure class="wp-figure"><img src="img/{elem["name"]}" '
                f'style="width:{elem["w"]}px;height:{elem["h"]}px" alt=""></figure>')

    text = elem["text"]
    bold_ranges = elem.get("bold_ranges", [])

    if rtype == "h1":
        return f'<h1 class="chapter-title">{html_mod.escape(text)}</h1>'
    elif rtype == "h2":
        return f'<h2 class="section-title">{html_mod.escape(text)}</h2>'
    elif rtype == "h3":
        return f'<h3 class="subsection-title">{html_mod.escape(text)}</h3>'
    elif rtype == "bullet":
        # Strip leading bullet character
        clean = re.sub(r"^[\u2022\u25CF\u25CB\u2013\u2014\u00B7\-\*]\s*", "", text)
        content = apply_bold_ranges(clean, [])  # bullets rarely have mixed bold
        return f"<li>{content}</li>"
    else:
        content = apply_bold_ranges(text, bold_ranges)
        return f"<p>{content}</p>"


def estimate_element_height(rtype, elem):
    """Estimate the pixel height an element will occupy."""
    if rtype == "table":
        return estimate_table_height(elem["rows"])
    if rtype == "image":
        return elem["h"] + 50  # figure margins
    text = elem["text"]
    if rtype == "h1":
        return H1_HEIGHT
    elif rtype == "h2":
        return H2_HEIGHT
    elif rtype == "h3":
        return H3_HEIGHT
    elif rtype == "bullet":
        return LI_HEIGHT
    else:
        return estimate_para_height(text)


# ── Page template ─────────────────────────────────────────────────────────────
PAGE_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<script src="https://mcp.figma.com/mcp/html-to-design/capture.js" async></script>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
    width: 795px;
    height: 1125px;
    font-family: 'Inter', sans-serif;
    color: #373737;
    line-height: 1.6;
    background: white;
    overflow: hidden;
}}
.page {{
    width: 795px;
    height: 1125px;
    padding: 50px 55px 40px 55px;
    position: relative;
}}
.page-number {{
    position: absolute;
    top: 28px;
    right: 55px;
    font-size: 9px;
    color: #999;
}}
.blue-bar {{
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: #0A74D6;
}}
h1.chapter-title {{
    font-weight: 600;
    font-size: 22px;
    color: #0A74D6;
    margin-bottom: 16px;
    line-height: 1.2;
}}
h2.section-title {{
    font-weight: 600;
    font-size: 14px;
    color: #0A74D6;
    margin-top: 16px;
    margin-bottom: 8px;
}}
h3.subsection-title {{
    font-weight: 600;
    font-size: 12px;
    color: #373737;
    margin-top: 12px;
    margin-bottom: 6px;
}}
p {{
    font-size: 9.5px;
    color: #373737;
    line-height: 1.65;
    margin-bottom: 8px;
    text-align: justify;
}}
strong {{ font-weight: 600; color: #2a2a2a; }}
ul {{
    margin: 4px 0 10px 0;
    padding-left: 16px;
    list-style: none;
}}
ul li {{
    font-size: 9.5px;
    color: #373737;
    line-height: 1.65;
    margin-bottom: 4px;
    position: relative;
    padding-left: 12px;
}}
ul li::before {{
    content: "\\25CF";
    color: #0A74D6;
    font-size: 6px;
    position: absolute;
    left: 0;
    top: 2px;
}}
.callout {{
    border-left: 3px solid #0A74D6;
    background: #F0F4F8;
    padding: 10px 14px;
    margin: 10px 0;
    border-radius: 0 4px 4px 0;
    font-size: 9px;
}}
table {{
    width: 100%;
    border-collapse: collapse;
    margin: 8px 0 12px 0;
    font-size: 8.5px;
}}
table th {{
    background: #0A74D6;
    color: white;
    font-weight: 600;
    text-align: left;
    padding: 6px 8px;
}}
table td {{
    padding: 5px 8px;
    border: 1px solid #dce3ea;
    vertical-align: top;
}}
table tr:nth-child(even) td {{ background: #F5F8FB; }}
</style>
</head>
<body>
<div class="page">
    <div class="page-number">{page_number:02d}</div>
{content}
    <div class="blue-bar"></div>
</div>
</body>
</html>"""


# ── Pagination ────────────────────────────────────────────────────────────────
def paginate(classified_elements):
    """
    Split classified elements into pages.
    Returns a list of pages, each page being a list of (rtype, elem) tuples.
    """
    pages = []
    current_page = []
    current_height = 0

    i = 0
    while i < len(classified_elements):
        rtype, elem = classified_elements[i]
        h = estimate_element_height(rtype, elem)

        # Chapter titles always start a new page
        if rtype == "h1" and (current_page or current_height > 0):
            pages.append(current_page)
            current_page = []
            current_height = 0

        # Don't orphan headings: if h2/h3 is near bottom, push to next page
        if rtype in ("h2", "h3") and current_height + h + 40 > SAFE_HEIGHT:
            pages.append(current_page)
            current_page = []
            current_height = 0

        # Check if element fits
        if current_height + h > SAFE_HEIGHT and current_page:
            carry = []
            # A picture illustrates the step just above it: keep them together
            if rtype == "image" and current_page[-1][0] in ("bullet", "paragraph"):
                carry = [current_page.pop()]
            pages.append(current_page)
            current_page = carry
            current_height = sum(estimate_element_height(t, e) for t, e in carry)

        current_page.append((rtype, elem))
        current_height += h
        i += 1

    if current_page:
        pages.append(current_page)

    return pages


def build_page_html(page_elements):
    """Build the inner content HTML for a page."""
    lines = []
    in_ul = False

    for rtype, elem in page_elements:
        if rtype == "bullet":
            if not in_ul:
                lines.append("    <ul>")
                in_ul = True
            lines.append("    " + render_element(rtype, elem))
        else:
            if in_ul:
                lines.append("    </ul>")
                in_ul = False
            lines.append("    " + render_element(rtype, elem))

    if in_ul:
        lines.append("    </ul>")

    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print(f"Reading DOCX: {DOCX_PATH}")
    elements = parse_docx(DOCX_PATH)
    print(f"Parsed {len(elements)} content elements")

    # Skip the document title (element 0 = "Whitepaper: AWS Virtual Desktops...")
    # Start from element 1 (Executive Summary)
    content_elements = elements[1:]

    # Write pictures next to the pages and fit them to the text column
    from PIL import Image
    import io
    img_dir = os.path.join(OUTPUT_DIR, "img")
    os.makedirs(img_dir, exist_ok=True)
    for e in content_elements:
        if e["type"] != "image":
            continue
        with open(os.path.join(img_dir, e["name"]), "wb") as f:
            f.write(e["data"])
        iw, ih = Image.open(io.BytesIO(e["data"])).size
        e["w"], e["h"] = IMG_FIXED_W, round(ih * IMG_FIXED_W / iw)
    print(f"Pictures: {sum(1 for e in content_elements if e['type'] == 'image')}")

    # Classify all elements
    classified = [classify_element(e) for e in content_elements]
    print(f"Classified {len(classified)} elements")

    # Count types
    from collections import Counter
    type_counts = Counter(r for r, _ in classified)
    for t, c in type_counts.most_common():
        print(f"  {t}: {c}")

    # Paginate
    pages = paginate(classified)
    print(f"\nPaginated into {len(pages)} pages")

    # Generate HTML files starting at page 03
    start_page = 3
    generated = []

    for idx, page_elements in enumerate(pages):
        page_num = start_page + idx
        content_html = build_page_html(page_elements)
        full_html = PAGE_TEMPLATE.format(
            page_number=page_num, content=content_html
        )

        filename = f"wp-page-{page_num:02d}.html"
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(full_html)
        generated.append(filename)

        # Show first element of each page for debugging
        first_type, first_elem = page_elements[0]
        first_text = first_elem.get("text", "(table)")[:70] if first_elem.get("text") else ("(picture)" if first_elem.get("type") == "image" else "(table)")
        # Replace non-ASCII for safe console printing
        safe_text = first_text.encode("ascii", "replace").decode("ascii")
        print(f"  {filename} - {len(page_elements)} elements - starts with [{first_type}] {safe_text}")

    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Total pages generated: {len(generated)}")
    print(f"Page range: {start_page:02d} to {start_page + len(generated) - 1:02d}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"\nFiles:")
    for fn in generated:
        print(f"  {fn}")


if __name__ == "__main__":
    main()
