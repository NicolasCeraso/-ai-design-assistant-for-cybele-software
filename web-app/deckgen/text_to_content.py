#!/usr/bin/env python3
"""
Text/DOCX to Content JSON converter.

Reads plain text or .docx file and generates a content JSON structure
that can be fed to generate_deck.py.

Usage:
  python text_to_content.py input.txt -o content.json
  python text_to_content.py input.docx -o content.json

Format conventions for .txt input:
  Lines starting with # are slide titles
  Lines starting with ## are section headers
  Lines starting with - or * are bullet points
  Lines starting with + are pros
  Lines starting with ! are cons
  Lines starting with | are table rows (pipe-separated)
  Blank lines separate sections
  First line (or first # line) becomes the cover slide title
"""

import argparse, json, os, re, sys


def extract_text_from_docx(path):
    """Extract text from a .docx file."""
    from docx import Document
    doc = Document(path)
    lines = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            lines.append(text)
    # Also grab table data
    for table in doc.tables:
        for row in table.rows:
            cells = [cell.text.strip() for cell in row.cells]
            lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def parse_text_to_sections(text):
    """Parse structured text into sections."""
    lines = text.strip().split("\n")
    sections = []
    current = {"title": "", "content": []}

    for line in lines:
        line = line.rstrip()
        if not line:
            if current["content"] or current["title"]:
                sections.append(current)
                current = {"title": "", "content": []}
            continue

        if line.startswith("# "):
            if current["content"] or current["title"]:
                sections.append(current)
            current = {"title": line[2:].strip(), "content": []}
        elif line.startswith("## "):
            current["subtitle"] = line[3:].strip()
        else:
            current["content"].append(line)

    if current["content"] or current["title"]:
        sections.append(current)

    return sections


def classify_content(lines):
    """Determine what type of slide content we have."""
    has_pros = any(l.startswith("+") for l in lines)
    has_cons = any(l.startswith("!") for l in lines)
    has_table = any(l.startswith("|") for l in lines)
    has_bullets = any(l.startswith(("-", "*")) for l in lines)

    if has_pros or has_cons:
        return "pros_cons"
    if has_table:
        return "table"
    if has_bullets:
        return "bullets"
    return "text"


# Icon auto-assignment based on keywords
ICON_KEYWORDS = {
    "security": "shield", "secure": "shield", "protection": "shield",
    "cost": "dollar-sign", "price": "dollar-sign", "pricing": "dollar-sign",
    "savings": "dollar-sign", "budget": "dollar-sign", "money": "dollar-sign",
    "cloud": "cloud", "web": "cloud", "browser": "cloud", "saas": "cloud",
    "computer": "pc", "desktop": "pc", "platform": "pc", "device": "pc",
    "analytics": "stats", "data": "stats", "metrics": "stats", "report": "stats",
    "scale": "scale", "scalab": "scale", "growth": "scale", "performance": "scale",
    "education": "education", "university": "education", "academic": "education",
    "remote": "remote-work", "work from home": "remote-work", "access": "remote-work",
    "login": "login", "authentication": "lock-check", "mfa": "lock-check",
    "vpn": "no-vpn", "zero trust": "enterprise-ZTNA", "ztna": "enterprise-ZTNA",
    "health": "healthcare", "medical": "healthcare",
    "vdi": "vdi", "virtual": "vdi", "virtualization": "vdi",
    "gpu": "gpu-fast", "fast": "gpu-fast", "speed": "gpu-fast",
    "compliance": "audit-log", "audit": "audit-log",
    "user": "user", "team": "user", "employee": "user",
    "book": "book", "documentation": "book", "guide": "book",
    "config": "system-config", "settings": "system-config", "setup": "system-config",
    "gateway": "gateway", "network": "gateway",
    "broker": "broker", "connection": "broker",
    "storage": "daas", "infrastructure": "daas",
    "premises": "premises", "building": "premises", "office": "premises",
}


def guess_icon(text):
    """Guess the best icon based on text content."""
    lower = text.lower()
    for keyword, icon in ICON_KEYWORDS.items():
        if keyword in lower:
            return icon
    return "stats"  # default fallback


def sections_to_content(sections, doc_title=""):
    """Convert parsed sections to content JSON structure."""
    slides = []
    slide_num = 1

    # First section → cover slide
    if sections:
        first = sections[0]
        title = first.get("title", doc_title) or "Presentation"
        subtitle = first.get("subtitle", "")
        if not subtitle and first["content"]:
            subtitle = first["content"][0]
        slides.append({
            "type": "cover",
            "title": title,
            "subtitle": subtitle
        })
        sections = sections[1:]
        slide_num += 1

    # Process remaining sections
    for sec in sections:
        title = sec.get("title", f"Section {slide_num}")
        lines = sec["content"]

        if not lines:
            continue

        content_type = classify_content(lines)

        if content_type == "pros_cons":
            pros = [l[1:].strip() for l in lines if l.startswith("+")]
            cons = [l[1:].strip() for l in lines if l.startswith("!")]
            other = [l for l in lines if not l.startswith(("+", "!"))]
            slides.append({
                "type": "pros_cons",
                "section_label": "Analysis",
                "section_title": title,
                "slide_num": slide_num,
                "title": title,
                "pros": pros,
                "cons": cons
            })

        elif content_type == "table":
            table_lines = [l for l in lines if l.startswith("|")]
            non_table = [l for l in lines if not l.startswith("|")]

            rows = []
            for tl in table_lines:
                cells = [c.strip() for c in tl.strip("|").split("|")]
                rows.append(cells)

            if rows:
                headers = rows[0]
                data_rows = rows[1:]
                slides.append({
                    "type": "table",
                    "section_label": "Data",
                    "section_title": title,
                    "slide_num": slide_num,
                    "title": title,
                    "headers": headers,
                    "rows": data_rows,
                    "highlight_col": 1 if len(headers) > 1 else None
                })

        elif content_type == "bullets":
            bullets = []
            intro_lines = []
            for l in lines:
                if l.startswith(("-", "*")):
                    bullets.append(l[1:].strip())
                else:
                    intro_lines.append(l)

            # If we have many bullets (6+), try cards_grid instead
            if len(bullets) >= 6:
                cards = []
                for b in bullets:
                    cards.append({
                        "icon": guess_icon(b),
                        "title": b[:50] + ("..." if len(b) > 50 else ""),
                        "text": b
                    })
                slides.append({
                    "type": "cards_grid",
                    "section_label": "Overview",
                    "section_title": title,
                    "slide_num": slide_num,
                    "title": title,
                    "cols": 3,
                    "cards": cards[:6]  # max 6 per grid
                })
                # If more than 6, overflow to a second slide
                if len(cards) > 6:
                    slide_num += 1
                    slides.append({
                        "type": "cards_grid",
                        "section_label": "Overview",
                        "section_title": title + " (continued)",
                        "slide_num": slide_num,
                        "title": title + " (continued)",
                        "cols": 3,
                        "cards": cards[6:12]
                    })
            else:
                slides.append({
                    "type": "bullets",
                    "section_label": "Details",
                    "section_title": title,
                    "slide_num": slide_num,
                    "title": title,
                    "intro": " ".join(intro_lines) if intro_lines else "",
                    "bullets": bullets
                })

        else:
            # Plain text → section slide with body
            text = " ".join(lines)
            # If short enough, use bullet slide with single "bullet"
            slides.append({
                "type": "bullets",
                "section_label": "Content",
                "section_title": title,
                "slide_num": slide_num,
                "title": title,
                "intro": text,
                "bullets": []
            })

        slide_num += 1

    # Add closing slide
    slides.append({
        "type": "closing",
        "tagline": "Thank You",
        "subtitle": "Contact us for more information"
    })

    return {
        "title": doc_title or (sections[0]["title"] if sections else "Presentation"),
        "slides": slides
    }


def main():
    parser = argparse.ArgumentParser(description="Convert text/docx to content JSON")
    parser.add_argument("input", help="Path to .txt or .docx file")
    parser.add_argument("-o", "--output", default=None, help="Output JSON path")
    parser.add_argument("--title", default="", help="Override presentation title")
    args = parser.parse_args()

    ext = os.path.splitext(args.input)[1].lower()
    if ext == ".docx":
        text = extract_text_from_docx(args.input)
    else:
        with open(args.input, 'r', encoding='utf-8') as f:
            text = f.read()

    sections = parse_text_to_sections(text)
    content = sections_to_content(sections, args.title)

    out = args.output or os.path.splitext(args.input)[0] + "_content.json"
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=2, ensure_ascii=False)

    print(f"Content JSON saved to {out}")
    print(f"  {len(content['slides'])} slides defined")
    print(f"\nNext step: python generate_deck.py {out}")


if __name__ == "__main__":
    main()
