#!/usr/bin/env python3
"""
Quick Deck — One-step branded PPTX from text or docx.
Generates native editable PowerPoint elements by default.

Usage:
  python quick_deck.py input.txt
  python quick_deck.py input.docx
  python quick_deck.py input.docx --output MyDeck.pptx
  python quick_deck.py input.txt --title "My Presentation"

Outputs to ~/Downloads/<title>.pptx by default.
"""

import argparse, json, os, sys

sys.path.insert(0, os.path.dirname(__file__))

from text_to_content import extract_text_from_docx, parse_text_to_sections, sections_to_content
from generate_deck import build_native_pptx


def main():
    parser = argparse.ArgumentParser(description="One-step branded PPTX generator")
    parser.add_argument("input", help="Path to .txt or .docx file")
    parser.add_argument("-o", "--output", default=None, help="Output PPTX path")
    parser.add_argument("--title", default="", help="Override presentation title")
    args = parser.parse_args()

    # 1. Read input
    ext = os.path.splitext(args.input)[1].lower()
    if ext == ".docx":
        text = extract_text_from_docx(args.input)
    else:
        with open(args.input, 'r', encoding='utf-8') as f:
            text = f.read()
    print(f"Read input: {len(text):,} chars from {args.input}")

    # 2. Parse to content structure
    sections = parse_text_to_sections(text)
    title = args.title or os.path.splitext(os.path.basename(args.input))[0]
    content = sections_to_content(sections, title)
    print(f"Generated {len(content['slides'])} slides")

    # 3. Determine output
    output = args.output
    if not output:
        safe = title.replace(" ", "_").replace("/", "_")
        output = os.path.join(os.path.expanduser("~"), "Downloads", f"{safe}.pptx")

    # 4. Build
    build_native_pptx(content, output)

    print(f"\nDone! Open: {output}")


if __name__ == "__main__":
    main()
