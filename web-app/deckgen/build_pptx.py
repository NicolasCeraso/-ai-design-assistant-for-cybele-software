"""
Native PPTX builder — creates editable PowerPoint slides using python-pptx.
Each slide type produces real text boxes, shapes, and tables (not images).
"""

import json, os, base64, io, re
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

# ─── Config ───

_config = None

def _load_config():
    global _config
    if _config is None:
        cfg_path = os.path.join(os.path.dirname(__file__), 'brand_config.json')
        with open(cfg_path, 'r', encoding='utf-8') as f:
            _config = json.load(f)
    return _config

def _rgb(hex_color):
    """Convert '#RRGGBB' to RGBColor."""
    h = hex_color.lstrip('#')
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

def _c(key):
    return _load_config()['colors'][key]

def _company(key):
    return _load_config()['company'][key]

# Slide dimensions in EMU (1 inch = 914400 EMU)
SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

# Common measurements
MARGIN_L = Inches(0.55)
MARGIN_R = Inches(0.55)
CONTENT_W = SLIDE_W - MARGIN_L - MARGIN_R
TOP_BAR_H = Inches(0.97)
FOOTER_H = Inches(0.55)
CONTENT_TOP = Inches(1.18)
CONTENT_BOTTOM = SLIDE_H - FOOTER_H
CONTENT_H = CONTENT_BOTTOM - CONTENT_TOP


# ─── Helpers ───

def _set_font(run, size=14, bold=False, color=None, font_name='Inter'):
    """Configure a text run's font properties."""
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.name = font_name
    if color:
        run.font.color.rgb = _rgb(color) if isinstance(color, str) else color


def _add_textbox(slide, left, top, width, height, text, size=14, bold=False,
                 color=None, alignment=PP_ALIGN.LEFT, font_name='Inter',
                 anchor=MSO_ANCHOR.TOP, word_wrap=True):
    """Add a simple text box and return (shape, text_frame)."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = word_wrap
    tf.auto_size = None

    # Set vertical anchor
    bodyPr = tf._txBody.find(qn('a:bodyPr'))
    if bodyPr is not None:
        anchor_map = {MSO_ANCHOR.TOP: 't', MSO_ANCHOR.MIDDLE: 'ctr', MSO_ANCHOR.BOTTOM: 'b'}
        bodyPr.set('anchor', anchor_map.get(anchor, 't'))

    p = tf.paragraphs[0]
    p.alignment = alignment
    run = p.add_run()
    run.text = text
    _set_font(run, size, bold, color, font_name)
    return txBox, tf


def _add_paragraph(tf, text, size=14, bold=False, color=None,
                   alignment=PP_ALIGN.LEFT, space_before=0, space_after=0,
                   font_name='Inter'):
    """Add a paragraph to an existing text frame."""
    p = tf.add_paragraph()
    p.alignment = alignment
    p.space_before = Pt(space_before)
    p.space_after = Pt(space_after)
    run = p.add_run()
    run.text = text
    _set_font(run, size, bold, color, font_name)
    return p


def _add_rect(slide, left, top, width, height, fill_color, corner_radius=None):
    """Add a filled rectangle shape."""
    if corner_radius:
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        # Set corner radius (in EMU)
        shape.adjustments[0] = corner_radius
    else:
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = _rgb(fill_color) if isinstance(fill_color, str) else fill_color
    shape.line.fill.background()  # No border
    return shape


def _add_icon_image(slide, icon_name, left, top, size_inches=0.38):
    """Add a brand-library icon as a PNG picture. Any icon of ../brand-icon-lib.js works by name;
    the PNGs come from enterprise_vdi_oci_esp/render_icons.py (run once). None if not rendered."""
    cfg = _load_config()
    icon_path = os.path.join(os.path.dirname(__file__), cfg['icons_dir'], f'{icon_name}.png')
    if not os.path.exists(icon_path):
        global _warned_icons
        if not _warned_icons:
            _warned_icons = True
            print(f"WARNING: icon PNG not found ({icon_path}) — run "
                  "`python enterprise_vdi_oci_esp/render_icons.py` once; cards are drawn without icons.")
        return None
    sz = Inches(size_inches)
    return slide.shapes.add_picture(icon_path, left, top, sz, sz)


_warned_icons = False


def _add_icon_circle(slide, icon_name, left, top, size=Inches(0.7)):
    """Add an icon in a light blue circle. Uses image if possible, or text fallback."""
    # Draw the circle background
    circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, size, size)
    circle.fill.solid()
    circle.fill.fore_color.rgb = _rgb(_c('bg_card_blue'))
    circle.line.fill.background()

    # Try to add the actual icon image on top
    margin = Inches(0.15)
    icon_img = _add_icon_image(slide, icon_name, left + margin, top + margin,
                                size_inches=0.4)
    if not icon_img:
        # Fallback: add text initial in the circle
        tf = circle.text_frame
        tf.word_wrap = False
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        # Use first letter of icon name
        run.text = icon_name[0].upper()
        _set_font(run, size=16, bold=True, color=_c('primary'))

        bodyPr = tf._txBody.find(qn('a:bodyPr'))
        if bodyPr is not None:
            bodyPr.set('anchor', 'ctr')

    return circle


# ─── Footer & Top Bar ───

def _add_footer(slide):
    """Add the blue footer bar with copyright and website."""
    bar = _add_rect(slide, 0, SLIDE_H - FOOTER_H, SLIDE_W, FOOTER_H, _c('primary'))

    # Copyright text (left)
    _add_textbox(slide, Inches(0.4), SLIDE_H - FOOTER_H, Inches(5), FOOTER_H,
                 f"\u00a9 {_company('year')} {_company('name')}",
                 size=9, color='#FFFFFF', anchor=MSO_ANCHOR.MIDDLE)

    # Website (right)
    _add_textbox(slide, SLIDE_W - Inches(4), SLIDE_H - FOOTER_H, Inches(3.6), FOOTER_H,
                 _company('website'),
                 size=9, color='#FFFFFF', alignment=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)


def _add_top_bar(slide, section_label, section_title, slide_num):
    """Add the blue top header bar."""
    _add_rect(slide, 0, 0, SLIDE_W, TOP_BAR_H, _c('primary'))

    # Section label (smaller, semi-transparent effect via lighter color)
    _add_textbox(slide, Inches(0.55), Inches(0.12), Inches(8), Inches(0.3),
                 section_label, size=10, color='#B8D9F2')

    # Section title
    _add_textbox(slide, Inches(0.55), Inches(0.38), Inches(8), Inches(0.4),
                 section_title, size=14, bold=True, color='#FFFFFF')

    # Slide number (right)
    _add_textbox(slide, SLIDE_W - Inches(1.2), Inches(0.25), Inches(0.8), Inches(0.4),
                 str(slide_num), size=12, color='#B8D9F2', alignment=PP_ALIGN.RIGHT)


# ─── Slide Builders ───

def build_cover(prs, data):
    """Cover slide with logo, title, subtitle, wave background."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank

    # Top gradient area (light blue rectangle)
    _add_rect(slide, 0, 0, SLIDE_W, Inches(5.2), _c('bg_gradient_top'))

    # Wave/bottom area (primary blue)
    # Use a rounded rectangle to simulate the wave
    wave = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                   Inches(-0.5), Inches(3.4), Inches(14.333), Inches(4.6))
    wave.adjustments[0] = 0.08
    wave.fill.solid()
    wave.fill.fore_color.rgb = _rgb(_c('primary'))
    wave.line.fill.background()

    # Logo
    _add_textbox(slide, 0, Inches(2.2), SLIDE_W, Inches(0.55),
                 _company('logo_text') + " \u2726", size=26, bold=True,
                 color=_c('text_dark'), alignment=PP_ALIGN.CENTER)
    _add_textbox(slide, 0, Inches(2.7), SLIDE_W, Inches(0.35),
                 _company('logo_sub'), size=12, color='#666666', alignment=PP_ALIGN.CENTER)

    # Title
    _add_textbox(slide, Inches(1), Inches(3.6), SLIDE_W - Inches(2), Inches(0.8),
                 data.get('title', ''), size=32, bold=True,
                 color='#FFFFFF', alignment=PP_ALIGN.CENTER)

    # Subtitle
    if data.get('subtitle'):
        _add_textbox(slide, Inches(1), Inches(4.35), SLIDE_W - Inches(2), Inches(0.5),
                     data['subtitle'], size=16, color='#FFFFFFDD', alignment=PP_ALIGN.CENTER)

    # Sub2
    if data.get('sub2'):
        _add_textbox(slide, Inches(1), Inches(4.8), SLIDE_W - Inches(2), Inches(0.4),
                     data['sub2'], size=11, color='#FFFFFF99', alignment=PP_ALIGN.CENTER)

    # Bottom copyright
    _add_textbox(slide, Inches(0.4), SLIDE_H - Inches(0.4), Inches(5), Inches(0.3),
                 f"Property of {_company('name')} {_company('year')}",
                 size=8, color='#FFFFFF60')

    return slide


def build_section(prs, data):
    """Standard content slide — top bar, title, and raw body text."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _add_top_bar(slide, data['section_label'], data['section_title'], data['slide_num'])
    _add_footer(slide)

    # Title
    _add_textbox(slide, MARGIN_L, CONTENT_TOP, CONTENT_W, Inches(0.55),
                 data['title'], size=26, bold=True, color=_c('primary'))

    # Body text (strip HTML tags for plain text)
    body = data.get('body_html', '')
    clean = re.sub(r'<[^>]+>', ' ', body).strip()
    clean = re.sub(r'\s+', ' ', clean)
    if clean:
        _add_textbox(slide, MARGIN_L, CONTENT_TOP + Inches(0.7), CONTENT_W, CONTENT_H - Inches(0.7),
                     clean, size=13, color=_c('text_body'))

    return slide


def build_cards_grid(prs, data):
    """Grid of cards with icons and text."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _add_top_bar(slide, data['section_label'], data['section_title'], data['slide_num'])
    _add_footer(slide)

    # Title
    _add_textbox(slide, MARGIN_L, CONTENT_TOP, CONTENT_W, Inches(0.55),
                 data['title'], size=26, bold=True, color=_c('primary'))

    cards = data.get('cards', [])
    cols = data.get('cols', 3)
    rows_count = (len(cards) + cols - 1) // cols

    card_gap = Inches(0.25)
    card_w = (CONTENT_W - card_gap * (cols - 1)) // cols
    card_h = Inches(2.2) if rows_count <= 2 else Inches(1.6)
    start_y = CONTENT_TOP + Inches(0.7)

    for idx, card in enumerate(cards):
        row = idx // cols
        col = idx % cols
        x = MARGIN_L + col * (card_w + card_gap)
        y = start_y + row * (card_h + card_gap)

        # Card background
        bg = _add_rect(slide, x, y, card_w, card_h, _c('bg_light'), corner_radius=0.05)

        # Icon circle
        icon_name = card.get('icon', '')
        if icon_name:
            icon_x = x + (card_w - Inches(0.65)) // 2
            _add_icon_circle(slide, icon_name, icon_x, y + Inches(0.18))

        # Card title
        title_y = y + Inches(0.95) if icon_name else y + Inches(0.25)
        _add_textbox(slide, x + Inches(0.15), title_y, card_w - Inches(0.3), Inches(0.45),
                     card['title'], size=13, bold=True, color=_c('text_dark'),
                     alignment=PP_ALIGN.CENTER)

        # Card text
        text_y = title_y + Inches(0.4)
        _add_textbox(slide, x + Inches(0.15), text_y, card_w - Inches(0.3),
                     card_h - (text_y - y) - Inches(0.15),
                     card['text'], size=10, color=_c('text_body'),
                     alignment=PP_ALIGN.CENTER)

    return slide


def build_pros_cons(prs, data):
    """Two-column pros and cons slide."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _add_top_bar(slide, data['section_label'], data['section_title'], data['slide_num'])
    _add_footer(slide)

    _add_textbox(slide, MARGIN_L, CONTENT_TOP, CONTENT_W, Inches(0.55),
                 data['title'], size=26, bold=True, color=_c('primary'))

    col_w = (CONTENT_W - Inches(0.4)) // 2
    start_y = CONTENT_TOP + Inches(0.7)

    # Pros column
    pros_badge = _add_rect(slide, MARGIN_L, start_y, Inches(0.9), Inches(0.35),
                           _c('accent_teal'), corner_radius=0.15)
    tf = pros_badge.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = "Pros"
    _set_font(run, 11, True, '#FFFFFF')
    bodyPr = tf._txBody.find(qn('a:bodyPr'))
    if bodyPr is not None:
        bodyPr.set('anchor', 'ctr')

    # Pros card
    pros_y = start_y + Inches(0.5)
    pros_items = data.get('pros', [])
    pros_h = max(Inches(0.4) * len(pros_items) + Inches(0.3), Inches(1))
    _add_rect(slide, MARGIN_L, pros_y, col_w, pros_h, _c('bg_light'), corner_radius=0.04)

    for i, pro in enumerate(pros_items):
        item_y = pros_y + Inches(0.15) + Inches(0.38) * i
        # Checkmark circle
        ck = slide.shapes.add_shape(MSO_SHAPE.OVAL,
                                     MARGIN_L + Inches(0.2), item_y + Inches(0.03),
                                     Inches(0.26), Inches(0.26))
        ck.fill.solid()
        ck.fill.fore_color.rgb = _rgb(_c('accent_teal'))
        ck.line.fill.background()
        tf_ck = ck.text_frame
        p_ck = tf_ck.paragraphs[0]
        p_ck.alignment = PP_ALIGN.CENTER
        r = p_ck.add_run()
        r.text = "\u2713"
        _set_font(r, 9, True, '#FFFFFF')
        bodyPr = tf_ck._txBody.find(qn('a:bodyPr'))
        if bodyPr is not None:
            bodyPr.set('anchor', 'ctr')

        _add_textbox(slide, MARGIN_L + Inches(0.55), item_y, col_w - Inches(0.75), Inches(0.35),
                     pro, size=11, color=_c('text_body'))

    # Cons column
    cons_x = MARGIN_L + col_w + Inches(0.4)
    cons_badge = _add_rect(slide, cons_x, start_y, Inches(0.9), Inches(0.35),
                           _c('accent_red'), corner_radius=0.15)
    tf = cons_badge.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = "Cons"
    _set_font(run, 11, True, '#FFFFFF')
    bodyPr = tf._txBody.find(qn('a:bodyPr'))
    if bodyPr is not None:
        bodyPr.set('anchor', 'ctr')

    cons_items = data.get('cons', [])
    cons_h = max(Inches(0.4) * len(cons_items) + Inches(0.3), Inches(1))
    _add_rect(slide, cons_x, pros_y, col_w, cons_h, _c('bg_light'), corner_radius=0.04)

    for i, con in enumerate(cons_items):
        item_y = pros_y + Inches(0.15) + Inches(0.38) * i
        xk = slide.shapes.add_shape(MSO_SHAPE.OVAL,
                                     cons_x + Inches(0.2), item_y + Inches(0.03),
                                     Inches(0.26), Inches(0.26))
        xk.fill.solid()
        xk.fill.fore_color.rgb = _rgb(_c('accent_red'))
        xk.line.fill.background()
        tf_xk = xk.text_frame
        p_xk = tf_xk.paragraphs[0]
        p_xk.alignment = PP_ALIGN.CENTER
        r = p_xk.add_run()
        r.text = "\u2717"
        _set_font(r, 9, True, '#FFFFFF')
        bodyPr = tf_xk._txBody.find(qn('a:bodyPr'))
        if bodyPr is not None:
            bodyPr.set('anchor', 'ctr')

        _add_textbox(slide, cons_x + Inches(0.55), item_y, col_w - Inches(0.75), Inches(0.35),
                     con, size=11, color=_c('text_body'))

    return slide


def build_table(prs, data):
    """Native PowerPoint table with styled header."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _add_top_bar(slide, data['section_label'], data['section_title'], data['slide_num'])
    _add_footer(slide)

    _add_textbox(slide, MARGIN_L, CONTENT_TOP, CONTENT_W, Inches(0.55),
                 data['title'], size=26, bold=True, color=_c('primary'))

    headers = data.get('headers', [])
    rows = data.get('rows', [])
    highlight_col = data.get('highlight_col')
    n_cols = len(headers)
    n_rows = len(rows) + 1  # +1 for header

    table_top = CONTENT_TOP + Inches(0.75)
    row_h = Inches(0.5)
    table_h = row_h * n_rows

    table_shape = slide.shapes.add_table(n_rows, n_cols,
                                          MARGIN_L, table_top, CONTENT_W, table_h)
    table = table_shape.table

    # Disable built-in banding
    tbl = table._tbl
    tblPr = tbl.find(qn('a:tblPr'))
    if tblPr is None:
        tblPr = tbl.makeelement(qn('a:tblPr'), {})
        tbl.insert(0, tblPr)
    tblPr.set('bandRow', '0')
    tblPr.set('firstRow', '0')
    tblPr.set('lastRow', '0')

    # Header row
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.text = h
        for paragraph in cell.text_frame.paragraphs:
            for run in paragraph.runs:
                _set_font(run, 11, True, '#FFFFFF')

        # Header bg
        if highlight_col is not None and j == highlight_col:
            cell.fill.solid()
            cell.fill.fore_color.rgb = _rgb(_c('primary'))
        else:
            cell.fill.solid()
            cell.fill.fore_color.rgb = _rgb(_c('primary'))

    # Data rows
    for i, row in enumerate(rows):
        bg = '#F9F9F9' if i % 2 == 0 else _c('bg_light')
        for j, val in enumerate(row):
            cell = table.cell(i + 1, j)
            cell.text = str(val)
            cell.fill.solid()
            cell.fill.fore_color.rgb = _rgb(bg)

            for paragraph in cell.text_frame.paragraphs:
                for run in paragraph.runs:
                    if highlight_col is not None and j == highlight_col:
                        _set_font(run, 11, True, _c('primary'))
                    else:
                        _set_font(run, 11, False, _c('text_body'))

    # Set column widths evenly
    col_w = CONTENT_W // n_cols
    for j in range(n_cols):
        table.columns[j].width = col_w

    return slide


def build_bullets(prs, data):
    """Bullet list slide with arrow items."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _add_top_bar(slide, data['section_label'], data['section_title'], data['slide_num'])
    _add_footer(slide)

    _add_textbox(slide, MARGIN_L, CONTENT_TOP, CONTENT_W, Inches(0.55),
                 data['title'], size=26, bold=True, color=_c('primary'))

    start_y = CONTENT_TOP + Inches(0.7)

    # Intro text
    intro = data.get('intro', '')
    if intro:
        _add_textbox(slide, MARGIN_L, start_y, CONTENT_W, Inches(0.5),
                     intro, size=13, color=_c('text_body'))
        start_y += Inches(0.6)

    # Card background
    bullets = data.get('bullets', [])
    if bullets:
        card_h = Inches(0.42) * len(bullets) + Inches(0.3)
        _add_rect(slide, MARGIN_L, start_y, CONTENT_W, card_h,
                  _c('bg_light'), corner_radius=0.04)

        for i, bullet in enumerate(bullets):
            by = start_y + Inches(0.15) + Inches(0.42) * i
            # Arrow
            _add_textbox(slide, MARGIN_L + Inches(0.25), by, Inches(0.3), Inches(0.35),
                         "\u2192", size=13, bold=True, color=_c('primary'))
            # Text
            _add_textbox(slide, MARGIN_L + Inches(0.6), by, CONTENT_W - Inches(0.85), Inches(0.35),
                         bullet, size=13, color=_c('text_body'))

    return slide


def build_split(prs, data):
    """Blue left panel with stat + right side pill items."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _add_footer(slide)

    left_w = Inches(5.0)

    # Blue left panel
    _add_rect(slide, 0, 0, left_w, SLIDE_H - FOOTER_H, _c('primary'))

    # Left content
    _add_textbox(slide, Inches(0.5), Inches(1.5), left_w - Inches(1), Inches(0.6),
                 data['left_title'], size=24, bold=True, color='#FFFFFF')
    _add_textbox(slide, Inches(0.5), Inches(2.2), left_w - Inches(1), Inches(1.2),
                 data['left_text'], size=12, color='#FFFFFFE6')

    # Big stat
    _add_textbox(slide, Inches(0.5), Inches(3.8), left_w - Inches(1), Inches(0.8),
                 data['left_stat'], size=40, bold=True, color='#FFFFFF')
    _add_textbox(slide, Inches(0.5), Inches(4.5), left_w - Inches(1), Inches(0.4),
                 data['left_stat_label'], size=12, color='#FFFFFFCC')

    # Right side pills
    pills = data.get('pills', [])
    right_x = left_w + Inches(0.5)
    right_w = SLIDE_W - right_x - Inches(0.5)
    pill_y = Inches(1.2)

    for pill in pills:
        pill_h = Inches(1.0)
        _add_rect(slide, right_x, pill_y, right_w, pill_h,
                  _c('bg_card_blue'), corner_radius=0.04)

        _add_textbox(slide, right_x + Inches(0.2), pill_y + Inches(0.1),
                     right_w - Inches(0.4), Inches(0.3),
                     pill['title'], size=12, bold=True, color=_c('primary'))

        _add_textbox(slide, right_x + Inches(0.2), pill_y + Inches(0.42),
                     right_w - Inches(0.4), Inches(0.5),
                     pill['text'], size=10, color=_c('text_body'))

        pill_y += pill_h + Inches(0.18)

    return slide


def build_stats_columns(prs, data):
    """Colored stat columns with big numbers."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _add_top_bar(slide, data['section_label'], data['section_title'], data['slide_num'])
    _add_footer(slide)

    _add_textbox(slide, MARGIN_L, CONTENT_TOP, CONTENT_W, Inches(0.55),
                 data['title'], size=26, bold=True, color=_c('primary'))

    stats = data.get('stats', [])
    n = len(stats)
    if n == 0:
        return slide

    color_map = {
        "primary": _c('primary'),
        "teal": _c('accent_teal'),
        "green": _c('accent_green'),
    }

    gap = Inches(0.2)
    col_w = (CONTENT_W - gap * (n - 1)) // n
    col_h = Inches(4.4)
    col_y = CONTENT_TOP + Inches(0.7)

    for i, stat in enumerate(stats):
        x = MARGIN_L + i * (col_w + gap)
        fill = color_map.get(stat.get('color', 'primary'), _c('primary'))
        _add_rect(slide, x, col_y, col_w, col_h, fill, corner_radius=0.08)

        # Value (bottom-aligned content)
        val_y = col_y + col_h - Inches(1.8)
        _add_textbox(slide, x + Inches(0.25), val_y, col_w - Inches(0.5), Inches(0.7),
                     stat['value'], size=30, bold=True, color='#FFFFFF')

        _add_textbox(slide, x + Inches(0.25), val_y + Inches(0.65),
                     col_w - Inches(0.5), Inches(0.35),
                     stat['label'], size=13, bold=True, color='#FFFFFF')

        if stat.get('text'):
            _add_textbox(slide, x + Inches(0.25), val_y + Inches(1.0),
                         col_w - Inches(0.5), Inches(0.5),
                         stat['text'], size=9, color='#FFFFFFDD')

    return slide


def build_two_column(prs, data):
    """Two-column layout with plain text."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _add_top_bar(slide, data['section_label'], data['section_title'], data['slide_num'])
    _add_footer(slide)

    _add_textbox(slide, MARGIN_L, CONTENT_TOP, CONTENT_W, Inches(0.55),
                 data['title'], size=26, bold=True, color=_c('primary'))

    col_w = (CONTENT_W - Inches(0.4)) // 2
    y = CONTENT_TOP + Inches(0.7)

    # Strip HTML for plain text
    left = re.sub(r'<[^>]+>', ' ', data.get('left_html', '')).strip()
    right = re.sub(r'<[^>]+>', ' ', data.get('right_html', '')).strip()

    _add_textbox(slide, MARGIN_L, y, col_w, CONTENT_H - Inches(0.7),
                 left, size=12, color=_c('text_body'))
    _add_textbox(slide, MARGIN_L + col_w + Inches(0.4), y, col_w, CONTENT_H - Inches(0.7),
                 right, size=12, color=_c('text_body'))

    return slide


def build_closing(prs, data):
    """Closing slide with logo, tagline, and contact info."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Background
    _add_rect(slide, 0, 0, SLIDE_W, Inches(5.2), _c('bg_gradient_top'))
    wave = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                   Inches(-0.5), Inches(3.4), Inches(14.333), Inches(4.6))
    wave.adjustments[0] = 0.08
    wave.fill.solid()
    wave.fill.fore_color.rgb = _rgb(_c('primary'))
    wave.line.fill.background()

    # Logo
    _add_textbox(slide, 0, Inches(2.2), SLIDE_W, Inches(0.5),
                 _company('logo_text') + " \u2726", size=24, bold=True,
                 color=_c('text_dark'), alignment=PP_ALIGN.CENTER)
    _add_textbox(slide, 0, Inches(2.65), SLIDE_W, Inches(0.3),
                 _company('logo_sub'), size=10, color='#666666', alignment=PP_ALIGN.CENTER)

    # Tagline
    _add_textbox(slide, Inches(1), Inches(3.6), SLIDE_W - Inches(2), Inches(0.6),
                 data.get('tagline', 'Thank You'), size=30, bold=True,
                 color='#FFFFFF', alignment=PP_ALIGN.CENTER)

    if data.get('subtitle'):
        _add_textbox(slide, Inches(1), Inches(4.2), SLIDE_W - Inches(2), Inches(0.4),
                     data['subtitle'], size=15, color='#FFFFFFDD', alignment=PP_ALIGN.CENTER)

    # Contact info row
    contact_y = Inches(5.0)
    center = SLIDE_W // 2

    contacts = [
        ("Web", _company('website')),
        ("Email", _company('email')),
        ("Phone", _company('phone')),
    ]
    spacing = Inches(3.5)
    start_x = center - spacing * 1  # Center the 3 items

    for i, (label, value) in enumerate(contacts):
        x = start_x + spacing * i - Inches(1.2)
        _add_textbox(slide, x, contact_y, Inches(2.4), Inches(0.25),
                     label, size=11, bold=True, color='#FFFFFF', alignment=PP_ALIGN.CENTER)
        _add_textbox(slide, x, contact_y + Inches(0.25), Inches(2.4), Inches(0.25),
                     value, size=11, color='#FFFFFFDD', alignment=PP_ALIGN.CENTER)

    # Copyright
    _add_textbox(slide, Inches(0.4), SLIDE_H - Inches(0.4), Inches(5), Inches(0.3),
                 f"Property of {_company('name')} {_company('year')}",
                 size=8, color='#FFFFFF60')

    return slide


# ─── Main builder ───

def build_presentation(content):
    """Build a full PPTX from content dict. Returns a Presentation object."""
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    builders = {
        'cover': build_cover,
        'section': build_section,
        'cards_grid': build_cards_grid,
        'pros_cons': build_pros_cons,
        'table': build_table,
        'bullets': build_bullets,
        'split': build_split,
        'stats_columns': build_stats_columns,
        'two_column': build_two_column,
        'closing': build_closing,
    }

    for s in content.get('slides', []):
        stype = s.get('type', '')
        builder = builders.get(stype)
        if builder:
            builder(prs, s)
        else:
            print(f"WARNING: Unknown slide type '{stype}', skipping.")

    return prs
