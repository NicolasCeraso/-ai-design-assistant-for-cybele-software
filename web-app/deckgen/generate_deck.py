#!/usr/bin/env python3
"""
Cybele Branded Deck Generator
==============================
Reads a content definition (JSON) and generates a branded PPTX presentation
with fully editable native PowerPoint elements (text, shapes, tables).

Usage:
  python generate_deck.py content.json [--output path/to/output.pptx]

The content JSON defines the slides using the available slide types.
See example_content.json for the format.
"""

import argparse, json, os, sys

# Add this directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))


def build_native_pptx(content, output_path):
    """Build PPTX with native editable elements."""
    from build_pptx import build_presentation

    prs = build_presentation(content)
    prs.save(output_path)
    print(f"PPTX saved to {output_path} ({len(content['slides'])} slides, editable)")


def main():
    parser = argparse.ArgumentParser(description="Cybele Branded Deck Generator")
    parser.add_argument("content", help="Path to content JSON file")
    parser.add_argument("--output", "-o", default=None,
                        help="Output PPTX path (default: ~/Downloads/<title>.pptx)")
    args = parser.parse_args()

    with open(args.content, 'r', encoding='utf-8') as f:
        content = json.load(f)

    output = args.output
    if not output:
        safe_title = content.get("title", "Cybele_Presentation").replace(" ", "_")
        output = os.path.join(os.path.expanduser("~"), "Downloads", f"{safe_title}.pptx")

    build_native_pptx(content, output)
    print("Done!")


if __name__ == "__main__":
    main()
