#!/usr/bin/env python3
"""
Redesign whitepaper HTML pages to match Figma reference:
  - Clean bullet points (blue dot) for list items
  - Labeled items styled with bold blue title + description
  - Callout boxes for key takeaways/summaries
  - Pro/con styling for checkmark/cross items
  - Blue bar flush at bottom
  - NO icon images
"""

import os, re, glob, tempfile

DASHBOARD = os.environ.get('WP_DASHBOARD', os.path.join(tempfile.gettempdir(), 'wp_pages'))

# ── NEW CSS ─────────────────────────────────────────────────────────────────────
NEW_CSS = r"""* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    width: 795px;
    height: 1125px;
    font-family: 'Inter', sans-serif;
    color: #373737;
    line-height: 1.6;
    background: white;
    overflow: hidden;
}
.page {
    width: 795px;
    height: 1125px;
    padding: 50px 55px 55px 55px;
    position: relative;
}
.page-number {
    position: absolute;
    top: 28px;
    right: 55px;
    font-size: 9px;
    color: #999;
}
.blue-bar {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 6px;
    background: #0A74D6;
    z-index: 10;
}

/* ── Typography ── */
h1.chapter-title {
    font-weight: 600;
    font-size: 22px;
    color: #0A74D6;
    margin-bottom: 14px;
    line-height: 1.2;
}
h2.section-title {
    font-weight: 600;
    font-size: 13px;
    color: #373737;
    margin-top: 16px;
    margin-bottom: 6px;
}
h3.subsection-title {
    font-weight: 600;
    font-size: 11px;
    color: #373737;
    margin-top: 10px;
    margin-bottom: 4px;
}
p {
    font-size: 12px;
    color: #515151;
    line-height: 1.6;
    margin-bottom: 8px;
    text-align: justify;
}
strong { font-weight: 600; color: #2a2a2a; }

/* ── Pictures (screenshots from the source) ── */
figure.wp-figure {
    margin: 18px 0 26px 0;
    text-align: center;
}
figure.wp-figure img {
    display: block;
    margin: 0 auto;
    border: 1px solid #D4E5F7;
    border-radius: 6px;
}

/* ── Tables ── */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 8px 0 12px 0;
    font-size: 10px;
}
table th {
    background: #0A74D6;
    color: white;
    font-weight: 600;
    text-align: left;
    padding: 5px 7px;
}
table td {
    padding: 4px 7px;
    border: 1px solid #dce3ea;
    vertical-align: top;
}
table tr:nth-child(even) td { background: #F5F8FB; }

/* ── Labeled Item (bold title + description) ── */
.labeled-item {
    padding: 7px 0;
    padding-left: 14px;
    position: relative;
}
.labeled-item + .labeled-item {
    border-top: 1px solid #EDF1F5;
}
.labeled-item::before {
    content: "\25CF";
    color: #0A74D6;
    font-size: 7px;
    position: absolute;
    left: 0;
    top: 9px;
}
.labeled-title {
    font-weight: 600;
    font-size: 13px;
    color: #0A74D6;
    margin-bottom: 2px;
    line-height: 1.3;
}
.labeled-desc {
    font-size: 12px;
    color: #515151;
    line-height: 1.6;
    margin: 0;
    text-align: justify;
}
.labeled-desc strong { color: #2a2a2a; }

/* ── Bullet List Item (short items with blue dot) ── */
.bullet-item {
    font-size: 12px;
    color: #515151;
    line-height: 1.6;
    padding: 5px 0 5px 14px;
    position: relative;
}
.bullet-item + .bullet-item {
    border-top: 1px solid #EDF1F5;
}
.bullet-item::before {
    content: "\25CF";
    color: #0A74D6;
    font-size: 6px;
    position: absolute;
    left: 0;
    top: 7px;
}
.bullet-item strong { color: #2a2a2a; }

/* ── Callout Box ── */
.callout-box {
    background: #F0F7FF;
    border: 1px solid #D4E5F7;
    border-radius: 8px;
    padding: 10px 14px;
    margin: 10px 0;
    display: flex;
    gap: 10px;
    align-items: flex-start;
}
.callout-dot {
    width: 20px;
    height: 20px;
    min-width: 20px;
    background: #0A74D6;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 700;
    font-size: 11px;
    margin-top: 1px;
}
.callout-body { flex: 1; min-width: 0; }
.callout-title {
    font-weight: 600;
    font-size: 13px;
    color: #0A74D6;
    margin-bottom: 2px;
}
.callout-text {
    font-size: 12px;
    color: #515151;
    line-height: 1.6;
    margin: 0;
    text-align: justify;
}
.callout-text strong { color: #2a2a2a; }

/* ── Pro/Con Items ── */
.check-item {
    font-size: 12px;
    line-height: 1.6;
    padding: 4px 0;
    display: flex;
    align-items: flex-start;
    gap: 8px;
}
.check-item .check-icon {
    width: 16px;
    height: 16px;
    min-width: 16px;
    flex-shrink: 0;
    margin-top: 1px;
}
.check-item.pro { color: #1a7a4a; }
.check-item.con { color: #b83030; }"""

# ── CALLOUT DETECTION ───────────────────────────────────────────────────────────
CALLOUT_LABELS = [
    'key takeaway', 'summary', 'business implication', 'implication',
    'bottom line', 'important', 'note',
]

def strip_tags(s):
    return re.sub(r'<[^>]+>', '', s).strip()

def extract_label(inner):
    """Extract (label, description) from labeled paragraph, or None."""
    m = re.match(r'\s*<strong>(.*?):\s*</strong>\s*(.*)', inner, re.DOTALL)
    if m:
        return (m.group(1).strip(), m.group(2).strip())
    m = re.match(r'\s*<strong>(.*?)</strong>\s*:\s*(.*)', inner, re.DOTALL)
    if m:
        return (m.group(1).strip(), m.group(2).strip())
    m = re.match(r'\s*<strong>(.*?)</strong>\s*[\u2192\u2013\u2014]\s*(.*)', inner, re.DOTALL)
    if m:
        return (m.group(1).strip(), m.group(2).strip())
    return None

def is_callout_label(label):
    ll = label.lower().replace('&amp;', '&')
    return any(cl in ll for cl in CALLOUT_LABELS)

def classify_paragraph(inner, plain, all_plains, idx):
    """Returns: 'callout', 'labeled', 'bullet', 'pro', 'con', 'regular'"""
    if plain.startswith('\u2705'):
        return 'pro'
    if plain.startswith('\u274c'):
        return 'con'

    lr = extract_label(inner)
    if lr:
        label, desc = lr
        if is_callout_label(label):
            return 'callout'
        return 'labeled'

    if len(plain) < 12:
        return 'regular'
    if len(plain) > 350:
        return 'regular'

    # Short paragraph group
    if len(plain) < 180:
        prev_ok = (idx > 0 and 12 < len(all_plains[idx-1]) < 180
                   and '\u2705' not in all_plains[idx-1]
                   and '\u274c' not in all_plains[idx-1])
        next_ok = (idx < len(all_plains)-1 and 12 < len(all_plains[idx+1]) < 180
                   and '\u2705' not in all_plains[idx+1]
                   and '\u274c' not in all_plains[idx+1])
        if prev_ok or next_ok:
            return 'bullet'

    return 'regular'

# ── HTML GENERATORS ─────────────────────────────────────────────────────────────

def make_labeled(label, desc):
    return (
        f'<div class="labeled-item">'
        f'<div class="labeled-title">{label}</div>'
        f'<p class="labeled-desc">{desc}</p>'
        f'</div>'
    )

def make_bullet(inner):
    return f'<div class="bullet-item">{inner}</div>'

def make_callout(label, desc):
    return (
        f'<div class="callout-box">'
        f'<div class="callout-dot">!</div>'
        f'<div class="callout-body">'
        f'<div class="callout-title">{label}</div>'
        f'<p class="callout-text">{desc}</p>'
        f'</div></div>'
    )

CHECK_SVG = '<svg class="check-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><circle cx="8" cy="8" r="7" fill="none" stroke="#3DCCA1" stroke-width="1.2"/><path d="M4.8 8.2L6.8 10.2L11.2 5.8" stroke="#3DCCA1" stroke-width="1.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CROSS_SVG = '<svg class="check-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><circle cx="8" cy="8" r="7" fill="none" stroke="#E04040" stroke-width="1.2"/><path d="M5.5 5.5L10.5 10.5M10.5 5.5L5.5 10.5" stroke="#E04040" stroke-width="1.4" stroke-linecap="round"/></svg>'

def make_check(text, kind):
    css = 'pro' if kind == 'pro' else 'con'
    icon = CHECK_SVG if kind == 'pro' else CROSS_SVG
    # Strip the emoji prefix from the text
    clean = text.lstrip('\u2705\u274c').strip()
    return f'<div class="check-item {css}">{icon}<span>{clean}</span></div>'

# ── FILE PROCESSING ─────────────────────────────────────────────────────────────

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace entire <style> block (use lambda to avoid backreference issues with \25CF)
    new_style = f'<style>\n{NEW_CSS}\n</style>'
    content = re.sub(
        r'<style>.*?</style>',
        lambda m: new_style,
        content, count=1, flags=re.DOTALL
    )

    # Extract body
    body_match = re.search(
        r'(<div class="page">)(.*?)(\s*<div class="blue-bar">)',
        content, re.DOTALL
    )
    if not body_match:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return {}

    body = body_match.group(2)
    body_offset = body_match.start(2)

    # Parse elements
    elem_re = re.compile(
        r'<(h[123][^>]*|p|table|div class="page-number")>(.*?)</(h[123]|p|table|div)>',
        re.DOTALL
    )
    elements = []
    for m in elem_re.finditer(body):
        open_tag = m.group(1)
        inner = m.group(2)
        if open_tag.startswith('table'):
            tag = 'table'
        elif open_tag.startswith('div'):
            tag = 'page-number'
        elif open_tag.startswith('h'):
            tag = open_tag[:2]
        else:
            tag = 'p'
        elements.append({
            'tag': tag, 'inner': inner,
            'plain': strip_tags(inner),
            'start': m.start(), 'end': m.end(),
        })

    # Get paragraph plains for group detection
    para_indices = [i for i, e in enumerate(elements) if e['tag'] == 'p']
    para_plains = [elements[i]['plain'] for i in para_indices]

    # Classify
    counts = {'labeled': 0, 'bullet': 0, 'callout': 0, 'check': 0}
    for seq_idx, elem_idx in enumerate(para_indices):
        el = elements[elem_idx]
        el['cls'] = classify_paragraph(el['inner'], el['plain'], para_plains, seq_idx)

    # Build replacements
    replacements = []
    for el in elements:
        if el['tag'] != 'p':
            continue
        cls = el.get('cls', 'regular')
        if cls == 'regular':
            continue

        inner = el['inner']
        plain = el['plain']

        if cls == 'labeled':
            lr = extract_label(inner)
            if lr:
                label, desc = lr
                replacements.append((el['start'], el['end'], make_labeled(label, desc)))
                counts['labeled'] += 1

        elif cls == 'callout':
            lr = extract_label(inner)
            if lr:
                label, desc = lr
                replacements.append((el['start'], el['end'], make_callout(label, desc)))
                counts['callout'] += 1

        elif cls == 'bullet':
            replacements.append((el['start'], el['end'], make_bullet(inner)))
            counts['bullet'] += 1

        elif cls in ('pro', 'con'):
            replacements.append((el['start'], el['end'], make_check(plain, cls)))
            counts['check'] += 1

    # Apply backwards
    new_body = body
    for start, end, repl in reversed(replacements):
        new_body = new_body[:start] + repl + new_body[end:]

    content = content[:body_offset] + new_body + content[body_offset + len(body):]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return counts


def main():
    files = sorted(glob.glob(os.path.join(DASHBOARD, 'wp-page-*.html')))
    totals = {'labeled': 0, 'bullet': 0, 'callout': 0, 'check': 0}

    for f in files:
        c = process_file(f)
        n = sum(c.values())
        print(f"  {os.path.basename(f)}: {n} ({c.get('labeled',0)}L {c.get('bullet',0)}B {c.get('callout',0)}C {c.get('check',0)}P)")
        for k in totals:
            totals[k] += c.get(k, 0)

    total = sum(totals.values())
    print(f"\nDone! {len(files)} files — {totals['labeled']} labeled, {totals['bullet']} bullets, "
          f"{totals['callout']} callouts, {totals['check']} pro/con = {total} total")


if __name__ == '__main__':
    main()
