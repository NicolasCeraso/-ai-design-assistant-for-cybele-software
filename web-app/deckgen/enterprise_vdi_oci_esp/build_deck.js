// Enterprise VDI on OCI · Discovery Demo (ESP)
// Cybele branded PPTX — palette 06/26. FAITHFUL reproduction of the source PDF:
//   · verbatim source copy (no rewriting/condensing) — preserve-source-language rule
//   · native editable architecture diagrams (pill system from thinfinity-architecture skill)
// Build: node build_deck.js  →  then  python swap_closing_slide.py

const PptxGenJS = require('pptxgenjs');
const pres = new PptxGenJS();
pres.layout = 'LAYOUT_WIDE';            // 13.333 × 7.5
pres.title = 'Enterprise VDI on OCI · Discovery Demo';
pres.company = 'Cybele Software, Inc.';

// ─── Palette 06/26 ───
const C = {
  NAVY: '0A1A2F',
  CANVAS: 'EEF4FB',
  BRAND_BLUE: '0A74D6',       // Brandbook-official primary (was 0F7FE0; reconciled 2026-06-11)
  BLUE_LIGHT: '5BAFFF',
  AZURE: '0AA9FF',            // diagram connectors
  MINT: '3DCCA1',
  ORACLE_RED: 'C74634',
  PERIMETER_RED: 'B3261E',    // network-perimeter dashed border (source uses red)
  TEXT_PRIMARY: '2E2E2E',
  TEXT_BODY: '454B57',        // darker than secondary → legible body/description text
  TEXT_SECONDARY: '5B6672',
  TEXT_ON_NAVY: 'E8EEF7',
  TEXT_ON_NAVY_MUTED: 'A8B4C4',
  TEXT_ON_BLUE: 'EAF2FD',
  DARK_CARD: '122542',
  WHITE: 'FFFFFF',
  FOOTER_TEXT: 'AEB7C2',
  DARK_FOOTER_TEXT: '4A6A90',
  BORDER_LIGHT: 'D5DDE8',
  ROW_ALT: 'F4F8FD',
  ZONE_GRAY: '8A93A0',
  ZONE_FILL: 'F3F6FB',
  CLOUD_LABEL: '0A74D6',
};

// ─── Brand assets ───
const ASSET_DIR = __dirname + '/../brand_assets';
const ICONS_DIR = __dirname + '/../icons_png';
const DIAG_DIR = __dirname + '/diagram_icons';
if (!require('fs').existsSync(DIAG_DIR) || !require('fs').existsSync(ICONS_DIR)) {
  console.error('Missing generated icons. Run once:  python render_icons.py && python render_diagram_icons.py   (see deckgen/README.md)');
  process.exit(1);
}
const ORACLE_LOGO = __dirname + '/assets/Oracle_logo (2) 1.png';
const ASSET = {
  cybeleLogo: `${ASSET_DIR}/cybele_logo.png`,
  cybeleLogoWhite: `${ASSET_DIR}/cybele_logo_white.png`,
  thinfinityLogo: `${ASSET_DIR}/thinfinity_logo.png`,
  thinfinityLogoWhite: `${ASSET_DIR}/thinfinity_logo_white.png`,
  oracleLogo: ORACLE_LOGO,
  oracleCloud: __dirname + '/assets/oracle cloud.png',   // stacked ORACLE/CLOUD, red
};
// Native logo aspect ratios (W/H) — used to size without distortion
const LOGO_AR = {
  thinfinity: 900 / 240,    // 3.75
  oracleCloud: 171 / 52,    // 3.29
  cybele: 700 / 260,        // 2.69
};
const ICON = (name, white = false) => `${ICONS_DIR}/${name}${white ? '_white' : ''}.png`;
// Diagram icon: variant '' (blue) | 'dark' | 'white'
const DICON = (name, variant = '') => `${DIAG_DIR}/${name}${variant ? '_' + variant : ''}.png`;

// ─── Layout constants (inches) ───
const W = 13.333, H = 7.5;
const MAR_L = 0.55, MAR_R = 0.55;
const CONTENT_W = W - MAR_L - MAR_R;
const TITLE_TOP = 0.45;

let SLIDE_INDEX = 0, TOTAL_SLIDES = 0;
const SLIDE_BUILDERS = [];

// ─── Background-mode rule (content slides only) ───
// ~1/3 light (#EEF4FB) · 1/3 white (#FFFFFF) · 1/3 dark (navy). Backgrounds are SOLID (no decoration).
// Hard rules (override the thirds split when in conflict):
//   · architecture-diagram slides are ALWAYS white,
//   · no DARK slide immediately before/after a separator (3, 13, 36, 39) — except the closing (40).
// Cover/dividers/Q&A/closing set their own navy and are excluded from the count.
const SLIDE_MODE = {
  2: 'light', 4: 'light', 5: 'light', 6: 'dark', 7: 'light', 8: 'dark', 9: 'light',
  10: 'dark', 11: 'light', 12: 'light',
  14: 'white', 15: 'white', 16: 'white',
  17: 'dark', 18: 'light', 19: 'dark', 20: 'light', 21: 'dark', 22: 'light', 23: 'dark',
  24: 'light', 25: 'dark', 26: 'dark',
  27: 'white', 28: 'white', 29: 'white', 30: 'white', 31: 'white', 32: 'white', 33: 'white',
  34: 'white', 35: 'white',
  37: 'light', 38: 'light',
};

let MODE = 'light', TH = {};
function setBg(slide, color) { slide.background = { color }; }
function setMode(slide, force) {
  const m = force || SLIDE_MODE[SLIDE_INDEX] || 'light';
  MODE = m;
  if (m === 'dark') {
    slide.background = { color: C.NAVY };
    // Low contrast on navy: cards barely lighter than the bg. accentDark → light text on accent.
    TH = { dark: true, title: C.WHITE, sub: C.TEXT_ON_NAVY_MUTED, body: C.TEXT_ON_NAVY,
      cardBase: C.DARK_CARD, cardBorder: '23364F', cardTitle: C.BLUE_LIGHT, cardBody: C.TEXT_ON_NAVY,
      accentFill: '1C3E63', accentDark: true, rowAlt: '12243F', tableHeader: '1C3E63', footerDark: true };
  } else {
    const white = m === 'white';
    slide.background = { color: white ? C.WHITE : C.CANVAS };
    // Low contrast on light/white: accent = soft blue tint with DARK text (no navy, no strong fill).
    // Vibrant brand blue reserved for details (title text, bullet dots, pill strokes).
    // #0A74D6 used ONLY for the table header row (explicit request).
    TH = { dark: false, title: C.BRAND_BLUE, sub: C.TEXT_SECONDARY, body: C.TEXT_BODY,
      cardBase: C.WHITE, cardBorder: white ? C.BORDER_LIGHT : null, cardTitle: C.BRAND_BLUE, cardBody: C.TEXT_BODY,
      accentFill: 'DCE8F8', accentDark: false, accentBorder: 'C6D8F0', rowAlt: white ? 'F4F8FD' : 'F8FAFD', tableHeader: '0A74D6', footerDark: false, whiteBg: white };
  }
}

// Footer label: alludes to the document title + the Thinfinity + OCI binomial
// (this deck is co-branded; otherwise it would read "Cybele Software").
const FOOTER_LABEL = 'Enterprise VDI on OCI · Discovery Demo  ·  Thinfinity + OCI';
function addFooter(slide, opts = {}) {
  const dark = opts.dark != null ? opts.dark : TH.footerDark;
  const txt = dark ? C.DARK_FOOTER_TEXT : C.FOOTER_TEXT;
  const lineCol = dark ? '24344C' : 'DEE5EE';
  // thin divider rule above the footer (footer element, not background decoration)
  slide.addShape('line', { x: MAR_L, y: H - 0.5, w: CONTENT_W, h: 0, line: { color: lineCol, width: 0.75 } });
  slide.addText(FOOTER_LABEL, {
    x: MAR_L, y: H - 0.4, w: CONTENT_W - 1.6, h: 0.28,
    fontFace: 'Inter', fontSize: 8.5, color: txt, valign: 'middle',
  });
  if (!opts.skipNumber) {
    slide.addText(`${SLIDE_INDEX} / ${TOTAL_SLIDES}`, {
      x: W - MAR_R - 1.5, y: H - 0.4, w: 1.5, h: 0.28,
      fontFace: 'Inter', fontSize: 8.5, color: txt, align: 'right', valign: 'middle',
    });
  }
}

function addTitleBar(slide, title, opts = {}) {
  const h = opts.twoLine ? 1.05 : 0.7;
  slide.addText(title, {
    x: MAR_L, y: TITLE_TOP, w: CONTENT_W, h,
    fontFace: 'Inter SemiBold', fontSize: opts.size || 28, color: opts.color || TH.title, lineSpacingMultiple: 1.05,
  });
}

function addSubtitle(slide, text, y) {
  slide.addText(text, {
    x: MAR_L, y: (y == null ? 1.38 : y), w: CONTENT_W, h: 0.4,
    fontFace: 'Inter', fontSize: 14, color: TH.sub,
  });
}

// Base content card — flat fill, NO border (stroke). Fill auto-adapts to mode.
function card(slide, x, y, w, h, opts = {}) {
  let fill = opts.fill;
  if (fill === undefined || fill === C.WHITE) fill = TH.cardBase || C.WHITE;
  slide.addShape('roundRect', {
    x, y, w, h, fill: { color: fill }, line: { type: 'none' }, rectRadius: opts.radius != null ? opts.radius : 0.06,
  });
}

// Estimate wrapped text height (inches) for a run of given font size and width.
function estLines(text, wIn, fontSize) {
  const cpl = Math.max(8, Math.floor(wIn * 118 / fontSize));   // chars per line (Inter ~)
  return Math.max(1, Math.ceil(text.length / cpl));
}
function estH(text, wIn, fontSize, lh = 1.2) {
  return estLines(text, wIn, fontSize) * (fontSize / 72) * lh;
}

// Heading + bullet list. items: [{t,d}] or ["string"]. Returns next-y.
function bulletList(slide, items, x, y, w, opts = {}) {
  const dot = opts.dot || C.BRAND_BLUE;
  const onDark = opts.onDark != null ? opts.onDark : TH.dark;
  const tColor = onDark ? C.WHITE : C.TEXT_PRIMARY;
  const dColor = onDark ? C.TEXT_ON_NAVY : C.TEXT_BODY;
  const tSize = opts.tSize || 12, dSize = opts.dSize || 10;
  const rowGap = opts.rowGap || 0.1;
  const tw = w - 0.24;
  let cy = y;
  items.forEach(it => {
    const t = typeof it === 'string' ? it : it.t;
    const d = typeof it === 'string' ? null : it.d;
    slide.addShape('ellipse', { x, y: cy + 0.055, w: 0.11, h: 0.11, fill: { color: dot }, line: { type: 'none' } });
    const tH = Math.max(0.24, estH(t, tw, tSize, 1.12) + 0.04);
    slide.addText(t, { x: x + 0.24, y: cy - 0.03, w: tw, h: tH, fontFace: 'Inter SemiBold', fontSize: tSize, color: tColor, lineSpacingMultiple: 1.08, valign: 'top' });
    let used = tH;
    if (d) {
      const dH = estH(d, tw, dSize, 1.2) + 0.04;
      slide.addText(d, { x: x + 0.24, y: cy + tH - 0.05, w: tw, h: dH, fontFace: 'Inter', fontSize: dSize, color: dColor, lineSpacingMultiple: 1.2, valign: 'top' });
      used += dH - 0.02;
    }
    cy += used + rowGap;
  });
  return cy;
}

// Simple feature-card grid. items:[{t,d,icon}]. Alternates brand/white if opts.alt.
function featureGrid(slide, items, opts) {
  const { cols, x0, y0, cardW, cardH, gapX, gapY } = opts;
  items.forEach((it, i) => {
    const col = i % cols, row = Math.floor(i / cols);
    const x = x0 + col * (cardW + gapX);
    const y = y0 + row * (cardH + gapY);
    const isBrand = opts.brandIdx ? opts.brandIdx(i) : false;
    const isNavy = opts.navyIdx ? opts.navyIdx(i) : false;
    // accent = low-contrast tint (light) or muted navy (dark); text adapts to accentDark
    const accent = isBrand || isNavy;
    const accDark = accent && TH.accentDark;
    const fill = accent ? TH.accentFill : TH.cardBase;
    const lightIcon = TH.dark || accDark;
    const titleColor = accDark ? C.WHITE : TH.cardTitle;
    const bodyColor = accDark ? C.TEXT_ON_NAVY : TH.cardBody;
    const accLine = (accent && !TH.dark && TH.accentBorder) ? { color: TH.accentBorder, width: 1 } : undefined;
    card(slide, x, y, cardW, cardH, { fill, line: accLine });
    let ty = y + 0.22;
    if (it.icon) {
      slide.addImage({ path: ICON(it.icon, lightIcon), x: x + 0.22, y: y + 0.24, w: 0.5, h: 0.5, sizing: { type: 'contain', w: 0.5, h: 0.5 } });
      ty = y + 0.9;
    }
    slide.addText(it.t, { x: x + 0.22, y: ty, w: cardW - 0.44, h: opts.titleH || 0.5,
      fontFace: 'Inter SemiBold', fontSize: opts.tSize || 14, color: titleColor, lineSpacingMultiple: 1.1 });
    if (it.d) {
      slide.addText(it.d, { x: x + 0.22, y: ty + (opts.titleH || 0.5) + 0.05, w: cardW - 0.44, h: cardH - (ty - y) - (opts.titleH || 0.5) - 0.2,
        fontFace: 'Inter', fontSize: opts.dSize || 10.5, color: bodyColor, lineSpacingMultiple: 1.3, valign: 'top' });
    }
  });
}

// 2-col table. header:[a,b]. rows:[[a,b]]. colSplit fraction for first column.
function dataTable(slide, header, rows, opts = {}) {
  const y0 = opts.y0, rowH = opts.rowH, c0 = opts.c0w;
  const c1 = CONTENT_W - c0;
  const aColor = TH.dark ? C.WHITE : C.TEXT_PRIMARY, bColor = TH.dark ? C.TEXT_ON_NAVY : C.TEXT_BODY;
  slide.addShape('rect', { x: MAR_L, y: y0, w: CONTENT_W, h: rowH, fill: { color: TH.tableHeader }, line: { type: 'none' } });
  slide.addText(header[0], { x: MAR_L + 0.18, y: y0, w: c0 - 0.3, h: rowH, fontFace: 'Inter SemiBold', fontSize: opts.hSize || 12, color: C.WHITE, valign: 'middle' });
  slide.addText(header[1], { x: MAR_L + c0 + 0.18, y: y0, w: c1 - 0.3, h: rowH, fontFace: 'Inter SemiBold', fontSize: opts.hSize || 12, color: C.WHITE, valign: 'middle' });
  rows.forEach((r, i) => {
    const y = y0 + (i + 1) * rowH;
    if (i % 2 === 0) slide.addShape('rect', { x: MAR_L, y, w: CONTENT_W, h: rowH, fill: { color: TH.rowAlt }, line: { type: 'none' } });
    slide.addText(r[0], { x: MAR_L + 0.18, y, w: c0 - 0.3, h: rowH, fontFace: 'Inter SemiBold', fontSize: opts.aSize || 10.5, color: aColor, valign: 'middle' });
    slide.addText(r[1], { x: MAR_L + c0 + 0.18, y, w: c1 - 0.3, h: rowH, fontFace: 'Inter', fontSize: opts.bSize || 10, color: bColor, valign: 'middle', lineSpacingMultiple: 1.05 });
  });
}

function sectionDivider(slide, eyebrow, title, sub) {
  setBg(slide, C.NAVY);
  slide.addText(eyebrow, { x: MAR_L, y: 2.5, w: CONTENT_W, h: 0.4, fontFace: 'Inter', fontSize: 13, color: C.BLUE_LIGHT, charSpacing: 4 });
  slide.addText(title, { x: MAR_L, y: 3.0, w: CONTENT_W, h: 1.5, fontFace: 'Inter SemiBold', fontSize: 54, color: C.WHITE });
  if (sub) slide.addText(sub, { x: MAR_L, y: 4.55, w: CONTENT_W, h: 0.5, fontFace: 'Inter', fontSize: 18, color: C.TEXT_ON_NAVY });
}

// ═══════════════════════════════════════════════════════════════
//  DIAGRAM ENGINE (pill system · thinfinity-architecture vocabulary)
// ═══════════════════════════════════════════════════════════════
// Category → stroke + label color. Icon keeps its own colorway.
const CAT = {
  thinfinity: { stroke: C.BRAND_BLUE, text: C.BRAND_BLUE, icon: '' },     // gateway/broker/agent
  user:       { stroke: '3A4350',     text: C.TEXT_PRIMARY, icon: 'dark' },
  generic:    { stroke: 'B8C2CE',     text: C.TEXT_PRIMARY, icon: 'dark' },
};

// ── Scale context (skill px-ratios on a 160×43 base pill) ──
// Pick ONE pill width per diagram; every atom derives from it, so each diagram is a
// clean zoom of the identical system (uniform pills + proportional gaps/strides).
function dScale(pillW) {
  const k = pillW / 160;                 // inches per "skill px"
  const PH = 43 * k;
  return {
    k, PW: pillW, PH, R: 7 * k,
    ICON: 23 * k, IOFF: 10 * k, TXTX: 39 * k,
    GAP: 43 * k,                          // min gap between containers = one pill height
    HSTR: 203 * k,                        // horizontal stride (160+43)
    VSTR: Math.max(PH + 0.14, 57 * k),    // vertical stride (≥ pill + gap so rows never touch)
    RUN: Math.max(0.16, 14 * k),          // ≥14px straight run before a chevron
    FS: Math.max(6.5, 12 * k * 72),       // pill label, pt
    FSZ: Math.max(8, 13 * k * 72),        // zone label, pt
    ZTOP: Math.max(0.42, 48 * k),         // top inset (clears the zone label at any scale)
    ZPADX: 20 * k, ZLX: 47 * k, ZLY: 31 * k, ZICON: 22 * k,
  };
}

// A uniform pill. opts: {icon, cat, fs, lines (array→2-line label)}
function pill(slide, x, y, label, sc, opts = {}) {
  const cat = CAT[opts.cat || 'generic'];
  const w = sc.PW, h = sc.PH;
  slide.addShape('roundRect', { x, y, w, h, fill: { color: C.WHITE }, line: { color: cat.stroke, width: 1.25 }, rectRadius: sc.R });
  if (opts.icon) {
    slide.addImage({ path: DICON(opts.icon, cat.icon), x: x + sc.IOFF, y: y + (h - sc.ICON) / 2, w: sc.ICON, h: sc.ICON, sizing: { type: 'contain', w: sc.ICON, h: sc.ICON } });
  }
  const tx = x + (opts.icon ? sc.TXTX : sc.IOFF);
  slide.addText(label, { x: tx, y, w: Math.max(0.15, x + w - tx - sc.IOFF), h, fontFace: 'Inter SemiBold', fontSize: opts.fs || sc.FS, color: cat.text, valign: 'middle', align: opts.align || 'left', lineSpacingMultiple: 0.95 });
  return { x, y, w, h, cx: x + w / 2, cy: y + h / 2, r: x + w, b: y + h };
}

// Edge-center point of a pill for a given side ('l','r','t','b').
function edgePt(p, side) {
  if (side === 'r') return { x: p.r, y: p.cy };
  if (side === 'l') return { x: p.x, y: p.cy };
  if (side === 't') return { x: p.cx, y: p.y };
  return { x: p.cx, y: p.b };
}
// Orthogonal connector between two pill edge-centers, guaranteeing a ≥RUN straight
// run into the target (chevron only on the final segment). opts: {sc, dash, end, color}
function connect(slide, a, aSide, b, bSide, opts = {}) {
  const sc = opts.sc, color = opts.color || C.AZURE, dash = opts.dash || 'solid';
  const end = opts.end === undefined ? 'triangle' : opts.end;
  const p1 = edgePt(a, aSide), p2 = edgePt(b, bSide);
  const seg = (x1, y1, x2, y2, e) => arrow(slide, x1, y1, x2, y2, { color, dash, end: e ? end : 'none' });
  if (Math.abs(p1.y - p2.y) < 0.012 || Math.abs(p1.x - p2.x) < 0.012) { seg(p1.x, p1.y, p2.x, p2.y, true); return; }
  // route with a mid elbow; ensure final straight ≥ RUN into target edge
  if (aSide === 'r' || aSide === 'l') {
    const mx = (sc && bSide === 'l') ? p2.x - sc.RUN : (sc && bSide === 'r' ? p2.x + sc.RUN : (p1.x + p2.x) / 2);
    seg(p1.x, p1.y, mx, p1.y, false); seg(mx, p1.y, mx, p2.y, false); seg(mx, p2.y, p2.x, p2.y, true);
  } else {
    const my = (sc && bSide === 't') ? p2.y - sc.RUN : (sc && bSide === 'b' ? p2.y + sc.RUN : (p1.y + p2.y) / 2);
    seg(p1.x, p1.y, p1.x, my, false); seg(p1.x, my, p2.x, my, false); seg(p2.x, my, p2.x, p2.y, true);
  }
}

// Dashed zone container. opts: {color, fill, labelFill, labelColor, dash}
function zone(slide, x, y, w, h, label, opts = {}) {
  const color = opts.color || C.ZONE_GRAY;
  slide.addShape('roundRect', {
    x, y, w, h,
    fill: opts.fill ? { color: opts.fill } : { type: 'none' },
    line: { color, width: opts.width || 1.25, dashType: opts.dash || 'dash' },
    rectRadius: 0.04,
  });
  if (label) {
    if (opts.labelFill) {
      const lw = 0.28 + label.length * 0.085;
      slide.addShape('roundRect', { x: x + 0.15, y: y - 0.16, w: lw, h: 0.32, fill: { color: opts.labelFill }, line: { type: 'none' }, rectRadius: 0.16 });
      slide.addText(label, { x: x + 0.15, y: y - 0.16, w: lw, h: 0.32, fontFace: 'Inter SemiBold', fontSize: 9.5, color: opts.labelColor || C.WHITE, align: 'center', valign: 'middle' });
    } else {
      slide.addText(label, { x: x + 0.18, y: y + 0.08, w: w - 0.3, h: 0.28, fontFace: 'Inter SemiBold', fontSize: 10, color: opts.labelColor || color });
    }
  }
}

// Arrow / connector between two points. opts: {color,width,dash,begin,end}
function arrow(slide, x1, y1, x2, y2, opts = {}) {
  const color = opts.color || C.AZURE;
  const x = Math.min(x1, x2), y = Math.min(y1, y2);
  const w = Math.abs(x2 - x1), h = Math.abs(y2 - y1);
  slide.addShape('line', {
    x, y, w, h, flipH: x2 < x1, flipV: y2 < y1,
    line: { color, width: opts.width || 1.75, dashType: opts.dash || 'solid',
      beginArrowType: opts.begin || 'none', endArrowType: opts.end === undefined ? 'triangle' : opts.end },
  });
}
// Orthogonal connector: horizontal then vertical (or via midpoint). mode 'h','v','hv','vh'
function elbow(slide, x1, y1, x2, y2, mode, opts = {}) {
  const color = opts.color || C.AZURE, width = opts.width || 1.75, dash = opts.dash || 'solid';
  const seg = (ax, ay, bx, by, end) => arrow(slide, ax, ay, bx, by, { color, width, dash, end: end ? (opts.end === undefined ? 'triangle' : opts.end) : 'none' });
  if (mode === 'h') { arrow(slide, x1, y1, x2, y2, { color, width, dash, end: opts.end === undefined ? 'triangle' : opts.end }); return; }
  if (mode === 'hv') { seg(x1, y1, x2, y1, false); seg(x2, y1, x2, y2, true); }
  else if (mode === 'vh') { seg(x1, y1, x1, y2, false); seg(x1, y2, x2, y2, true); }
}

// Small TLS tag chip (navy pill) used between gateway/broker
function tlsTag(slide, x, y, w, lines) {
  slide.addShape('roundRect', { x, y, w, h: 0.34, fill: { color: C.NAVY }, line: { type: 'none' }, rectRadius: 0.05 });
  slide.addText(lines, { x: x + 0.05, y, w: w - 0.1, h: 0.34, fontFace: 'Inter SemiBold', fontSize: 6.5, color: C.WHITE, align: 'center', valign: 'middle', lineSpacingMultiple: 0.95 });
}

// A small "resource" pill stack: a windows/linux/server pill with a Thinfinity Agent sub-pill.
function resourceTile(slide, x, y, w, topLabel, topIcon, agentLabel) {
  const h = 0.92;
  const narrow = w < 1.0;   // stack icon above label when very narrow
  slide.addShape('roundRect', { x, y, w, h, fill: { color: C.WHITE }, line: { color: 'B8C2CE', width: 1 }, rectRadius: 0.05 });
  if (narrow) {
    slide.addImage({ path: DICON(topIcon, 'dark'), x: x + (w - 0.24) / 2, y: y + 0.07, w: 0.24, h: 0.24, sizing: { type: 'contain', w: 0.24, h: 0.24 } });
    slide.addText(topLabel, { x: x + 0.04, y: y + 0.3, w: Math.max(0.2, w - 0.08), h: 0.22, fontFace: 'Inter SemiBold', fontSize: 7, color: C.TEXT_PRIMARY, align: 'center', valign: 'middle', lineSpacingMultiple: 0.9 });
  } else {
    slide.addImage({ path: DICON(topIcon, 'dark'), x: x + 0.1, y: y + 0.1, w: 0.26, h: 0.26, sizing: { type: 'contain', w: 0.26, h: 0.26 } });
    slide.addText(topLabel, { x: x + 0.4, y: y + 0.08, w: Math.max(0.2, w - 0.48), h: 0.3, fontFace: 'Inter SemiBold', fontSize: 8.5, color: C.TEXT_PRIMARY, valign: 'middle', lineSpacingMultiple: 0.95 });
  }
  if (agentLabel) {
    slide.addShape('roundRect', { x: x + 0.08, y: y + 0.52, w: Math.max(0.2, w - 0.16), h: 0.32, fill: { color: 'F0F6FD' }, line: { color: C.BRAND_BLUE, width: 0.75 }, rectRadius: 0.05 });
    if (narrow) {
      // icon + label centered, full width (no left-offset text box that would squeeze)
      slide.addImage({ path: DICON('thinfinity', ''), x: x + 0.13, y: y + 0.58, w: 0.18, h: 0.18, sizing: { type: 'contain', w: 0.18, h: 0.18 } });
      slide.addText(agentLabel, { x: x + 0.3, y: y + 0.52, w: Math.max(0.2, w - 0.36), h: 0.32, fontFace: 'Inter SemiBold', fontSize: 7.5, color: C.BRAND_BLUE, valign: 'middle' });
    } else {
      slide.addImage({ path: DICON('thinfinity', ''), x: x + 0.14, y: y + 0.57, w: 0.2, h: 0.2, sizing: { type: 'contain', w: 0.2, h: 0.2 } });
      slide.addText(agentLabel, { x: x + 0.36, y: y + 0.52, w: Math.max(0.2, w - 0.42), h: 0.32, fontFace: 'Inter SemiBold', fontSize: 8, color: C.BRAND_BLUE, valign: 'middle' });
    }
  }
  return { x, y, w, h, cx: x + w / 2, cy: y + h / 2, r: x + w, b: y + h };
}

// Centering region for architecture diagrams (below title/desc, above footer).
const DREG = { x: MAR_L, y: 1.75, w: CONTENT_W, h: 6.85 - 1.75 };
// Upper region for the topology on slides that also carry a specs panel at the bottom.
const UREG = { x: MAR_L, y: 1.6, w: CONTENT_W, h: 2.85 };

// Center every shape/image/text added to `slide` from index `fromIdx` onward, within
// `region`. Clamped so it never rides above the region top nor overlaps the footer.
function centerDiagram(slide, fromIdx, region, opts = {}) {
  const objs = (slide._slideObjects || []).slice(fromIdx);
  let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
  for (const o of objs) {
    const op = o && o.options; if (!op) continue;
    if (typeof op.x !== 'number' || typeof op.y !== 'number') continue;
    const w = typeof op.w === 'number' ? op.w : 0, h = typeof op.h === 'number' ? op.h : 0;
    if (op.x < minX) minX = op.x;
    if (op.y < minY) minY = op.y;
    if (op.x + w > maxX) maxX = op.x + w;
    if (op.y + h > maxY) maxY = op.y + h;
  }
  if (!isFinite(minX)) return;
  const bw = maxX - minX, bh = maxY - minY;
  let dx = 0, dy = 0;
  if (opts.axis !== 'y') {
    dx = region.x + (region.w - bw) / 2 - minX;
    if (minX + dx < region.x) dx = region.x - minX;
    if (maxX + dx > region.x + region.w) dx = region.x + region.w - maxX;
  }
  if (opts.axis !== 'x') {
    dy = region.y + (region.h - bh) / 2 - minY;
    if (minY + dy < region.y) dy = region.y - minY;
    if (maxY + dy > region.y + region.h) dy = region.y + region.h - maxY;
  }
  for (const o of objs) {
    const op = o && o.options; if (!op) continue;
    if (typeof op.x === 'number') op.x += dx;
    if (typeof op.y === 'number') op.y += dy;
  }
}

// ═══════════════════════════════════════════════════════════════
//  SLIDE BUILDERS
// ═══════════════════════════════════════════════════════════════

// 1 · Cover (navy) — emulates "Cover sample" (co-branded). Source p1 copy, verbatim.
SLIDE_BUILDERS.push(() => {
  const s = pres.addSlide();
  setBg(s, C.NAVY);   // solid background — no decorative elements
  // Eyebrow badge — outlined pill, transparent fill
  const bw = 2.55, bh = 0.46;
  s.addShape('roundRect', { x: MAR_L, y: 0.72, w: bw, h: bh, fill: { type: 'none' }, line: { color: '5E7BA6', width: 1 }, rectRadius: bh / 2 });
  s.addText('Discovery Demo · 2026', { x: MAR_L, y: 0.72, w: bw, h: bh, fontFace: 'Inter', fontSize: 11.5, color: C.TEXT_ON_NAVY, align: 'center', valign: 'middle' });

  // Hero title (Inter Bold) + subtitle (muted), left-aligned, vertically centered
  s.addText('One platform,\ninfinite solutions', { x: MAR_L, y: 2.35, w: 11.5, h: 2.0, fontFace: 'Inter', bold: true, fontSize: 52, color: C.WHITE, lineSpacingMultiple: 1.04 });
  s.addText('Advanced Zero Trust Remote Access\nand Cloud VDI Solutions', { x: MAR_L + 0.03, y: 4.7, w: 10.5, h: 1.0, fontFace: 'Inter', fontSize: 19, color: '93A1B5', lineSpacingMultiple: 1.25 });

  // Bottom divider with a short colored tint on the left
  const divY = 6.5;
  s.addShape('line', { x: 0, y: divY, w: W, h: 0, line: { color: '24344C', width: 1 } });
  s.addShape('line', { x: 0, y: divY, w: 3.4, h: 0, line: { color: C.ORACLE_RED, width: 1.5, transparency: 30 } });

  // Bottom-left co-brand lockup: Thinfinity + Oracle Cloud (equal height, native AR)
  const lkH = 0.4, lkY = 6.78;
  const tW = lkH * LOGO_AR.thinfinity;
  s.addImage({ path: ASSET.thinfinityLogo, x: MAR_L, y: lkY, w: tW, h: lkH });
  const plusX = MAR_L + tW + 0.16;
  s.addText('+', { x: plusX, y: lkY - 0.02, w: 0.3, h: lkH, fontFace: 'Inter', fontSize: 18, color: '7C8AA0', align: 'center', valign: 'middle' });
  const ocW = lkH * LOGO_AR.oracleCloud;
  s.addImage({ path: ASSET.oracleCloud, x: plusX + 0.34, y: lkY, w: ocW, h: lkH });

  // Bottom-right Cybele (larger), native AR, white
  const cyH = 0.52, cyW = cyH * LOGO_AR.cybele;
  s.addImage({ path: ASSET.cybeleLogoWhite, x: W - MAR_R - cyW, y: 6.72, w: cyW, h: cyH });
});

// 2 · Acerca de nosotros (5 KPI) — source p2 verbatim
SLIDE_BUILDERS.push(() => {
  const s = pres.addSlide();
  setMode(s);
  s.addText('Company / About the company', { x: MAR_L, y: 0.3, w: 6, h: 0.3, fontFace: 'Inter SemiBold', fontSize: 10, color: TH.sub, charSpacing: 1 });
  addTitleBar(s, 'Acerca de nosotros');
  addSubtitle(s, '★  5 datos clave sobre Cybele Software');

  const facts = [
    { kpi: 'A/2002', label: '', detail: 'Más de 20 años en el negocio de la virtualización con enfoque Zero Trust' },
    { kpi: 'Oficinas', label: '', detail: 'Draper, UT\nWilmington, DE\nBuenos Aires, ARG\nSão Paulo, BR' },
    { kpi: '+5000', label: 'Clientes Activos', detail: 'A nivel global' },
    { kpi: '+2000', label: 'Partners', detail: 'MSP, CSP, ISV e integradores de sistemas, socios en todo el mundo' },
    { kpi: 'A/2023', label: '', detail: 'Presencia en más de 78 países' },
  ];
  const cardW = 2.4, cardH = 2.9, startY = 2.0, gap = 0.06;
  facts.forEach((f, i) => {
    const x = MAR_L + i * (cardW + gap);
    const tinted = i % 2 === 0;
    // Light/white slides: NO dark-blue (navy) containers (rev 3). Alternate a soft-blue tint
    // with a clean white card (subtle border so the white reads on the canvas). Dark mode
    // keeps its own muted scheme. Heads use the vibrant brand blue, never navy.
    let fill, headCol, detailCol, borderCol;
    if (TH.dark) {
      fill = tinted ? TH.accentFill : C.DARK_CARD;
      headCol = C.WHITE; detailCol = C.TEXT_ON_NAVY; borderCol = null;
    } else {
      // rev 4: borderless containers. Distinguish cards by fill only (brand's low-contrast look):
      // alternate a soft-blue tint with a slightly cooler neutral so both read on the canvas without strokes.
      fill = tinted ? TH.accentFill : 'F4F8FD';
      headCol = C.BRAND_BLUE; detailCol = C.TEXT_BODY; borderCol = null;
    }
    s.addShape('roundRect', { x, y: startY, w: cardW, h: cardH, fill: { color: fill }, line: { type: 'none' }, rectRadius: 0.06 });
    s.addText(f.kpi, { x: x + 0.18, y: startY + 0.25, w: cardW - 0.36, h: 0.7, fontFace: 'Inter SemiBold', fontSize: 28, color: headCol });
    let dy = startY + 1.05;
    if (f.label) { s.addText(f.label, { x: x + 0.18, y: dy, w: cardW - 0.36, h: 0.35, fontFace: 'Inter SemiBold', fontSize: 14, color: headCol }); dy += 0.4; }
    s.addText(f.detail, { x: x + 0.18, y: dy, w: cardW - 0.36, h: cardH - (dy - startY) - 0.2, fontFace: 'Inter', fontSize: 11, color: detailCol, lineSpacingMultiple: 1.25 });
  });
  addFooter(s);
});

// 3 · Alliance title — treated as a section separator (navy), per internal proposal.
//     Separators self-set navy and carry no footer (same as dividers 13 / 36).
SLIDE_BUILDERS.push(() => {
  sectionDivider(pres.addSlide(), 'THINFINITY + ORACLE', 'Oracle Enterprise VDI & VDA', 'Simplified and Secured by Thinfinity');
});

// 4 · Sobre esta alianza (2 col, verbatim) — source p4
SLIDE_BUILDERS.push(() => {
  const s = pres.addSlide();
  setMode(s);
  addTitleBar(s, 'Sobre esta alianza');
  s.addText('Esta alianza une la plataforma VDI segura de Thinfinity con el rendimiento de Oracle Cloud Infrastructure para ofrecer una alternativa más rápida, sencilla y rentable a Citrix, Horizon y Azure AVD.',
    { x: MAR_L, y: 1.25, w: CONTENT_W, h: 0.7, fontFace: 'Inter', fontSize: 12, color: TH.body, lineSpacingMultiple: 1.25 });

  const colW = (CONTENT_W - 0.5) / 2;
  const colY = 2.1;
  // header chips
  s.addShape('roundRect', { x: MAR_L, y: colY, w: colW, h: 0.42, fill: { color: TH.accentFill }, line: { type: 'none' }, rectRadius: 0.08 });
  s.addText('Beneficios Técnicos', { x: MAR_L + 0.2, y: colY, w: colW - 0.4, h: 0.42, fontFace: 'Inter SemiBold', fontSize: 14, color: TH.accentDark ? C.WHITE : C.BRAND_BLUE, valign: 'middle' });
  const rx = MAR_L + colW + 0.5;
  s.addShape('roundRect', { x: rx, y: colY, w: colW, h: 0.42, fill: { color: TH.accentFill }, line: { type: 'none' }, rectRadius: 0.08 });
  s.addText('Beneficios Comerciales', { x: rx + 0.2, y: colY, w: colW - 0.4, h: 0.42, fontFace: 'Inter SemiBold', fontSize: 14, color: TH.accentDark ? C.WHITE : C.BRAND_BLUE, valign: 'middle' });

  const tech = [
    { t: 'Integración nativa con OCI', d: 'Implemente directamente dentro de Oracle Cloud Infrastructure sin middleware ni pilas de intermediarios complejas.' },
    { t: 'Delivery con Zero Trust', d: 'Sin necesidad de VPNs ni instalaciones en el cliente: acceda a escritorios, aplicaciones, sesiones SSH y servicios web directamente desde el navegador o mediante el cliente Thinfinity.' },
    { t: 'Arquitectura Zero Trust', d: 'Control de acceso basado en identidad con grabación de sesiones, filtrado por IP y políticas basadas en roles.' },
    { t: 'VDI de Alto Rendimiento', d: 'Latencia inferior a 100 ms, compatibilidad con hasta 16 monitores, aceleración por GPU y colaboración en tiempo real (optimizado para Teams y Zoom).' },
    { t: 'Orquestación y Automatización', d: 'Thinfinity Cloud Manager automatiza la provisión de sesiones, el escalado, la aplicación de políticas y la optimización de recursos, sin necesidad de herramientas externas como Nerdio.' },
  ];
  const com = [
    { t: 'Hasta un 50% menos de TCO en comparación con Citrix, AVD y Nerdio', d: 'El modelo de usuario concurrente de Thinfinity y la estructura de precios de infraestructura de OCI ofrecen una eficiencia de costos inigualable.' },
    { t: 'Licenciamiento Predecible', d: 'Precio fijo por usuario/mes basado en concurrencia — no en usuarios nominales o activos.' },
    { t: 'Implementación más ágil con retorno rápido', d: 'Menor fricción en la etapa de preventa y procesos de incorporación simplificados para clientes del mercado medio y empresas.' },
    { t: 'Preparado para Industrias Reguladas', d: 'Diseñado específicamente para cumplir con los requisitos de conformidad en sectores como banca, salud, gobierno y telecomunicaciones.' },
    { t: 'Listo para MSPs y Canales', d: 'Opciones de marca blanca y orquestación centralizada, ideales para proveedores de servicios y socios de Oracle.' },
    { t: 'Alineado con Oracle Co-Sell', d: 'Adquisición simplificada a través de listados en OCI Marketplace.' },
  ];
  bulletList(s, tech, MAR_L, colY + 0.6, colW, { dot: C.BRAND_BLUE, tSize: 11, dSize: 9.5, dH: 0.5, rowGap: 0.12 });
  bulletList(s, com, rx, colY + 0.6, colW, { dot: C.MINT, tSize: 11, dSize: 9.5, dH: 0.42, rowGap: 0.08 });
  addFooter(s);
});

// 5 · Elegido por +5.000 — source p5 (headline verbatim + customer names as text)
SLIDE_BUILDERS.push(() => {
  const s = pres.addSlide();
  setMode(s);
  addTitleBar(s, 'Elegido por más de 5.000 compañías globales de primer nivel', { size: 24 });

  s.addText('+5.000', { x: MAR_L, y: 1.7, w: 5, h: 1.7, fontFace: 'Inter SemiBold', fontSize: 96, color: C.BRAND_BLUE });
  s.addText('compañías globales de primer nivel confían en Cybele Software', { x: 5.6, y: 2.1, w: 7.0, h: 1.3, fontFace: 'Inter', fontSize: 20, color: C.TEXT_PRIMARY, lineSpacingMultiple: 1.3, valign: 'middle' });

  const brands = ['Telefónica', 'Virgin', 'VISA', 'JYSK', 'ABB', 'Shell', 'Dell', 'SD Worx', 'FUJIFILM', 'FIS', 'SHI', 'PAYCHEX', 'HONDA', 'AIG', 'LivaNova', 'NORDSTROM', 'QBS', 'Agilent', 'MITRE', 'Capita', 'IBM', 'EMERSON', 'Rockwell', 'AVERITT', 'NATO / OTAN', 'PayPal', 'TECH Mahindra', 'WEG', 'Insight', 'Schneider Electric'];
  const chipH = 0.42, gapX = 0.14, gapY = 0.16, startY = 3.7;
  let cx = MAR_L, cy = startY;
  brands.forEach(b => {
    const w = 0.28 + b.length * 0.085;
    if (cx + w > MAR_L + CONTENT_W) { cx = MAR_L; cy += chipH + gapY; }
    s.addShape('roundRect', { x: cx, y: cy, w, h: chipH, fill: { color: C.WHITE }, line: { color: C.BORDER_LIGHT, width: 1 }, rectRadius: 0.05 });
    s.addText(b, { x: cx, y: cy, w, h: chipH, fontFace: 'Inter SemiBold', fontSize: 10.5, color: C.TEXT_PRIMARY, align: 'center', valign: 'middle' });
    cx += w + gapX;
  });
  addFooter(s);
});

// 6 · Enterprise VDI on Oracle Cloud — 3 pillars (verbatim) — source p6
SLIDE_BUILDERS.push(() => {
  const s = pres.addSlide();
  setMode(s);
  addTitleBar(s, 'Enterprise VDI on Oracle Cloud');
  addSubtitle(s, 'Tres pilares operativos integrados');

  const pillars = [
    { t: 'Acceso Seguro', icon: 'shield', fill: C.BRAND_BLUE, d: 'Garantiza un acceso Zero Trust a sus recursos corporativos en diversos entornos en la nube y on-premises, mejorando la seguridad y la eficiencia general.' },
    { t: 'Aprovisionamiento y Escalabilidad', icon: 'vdi', fill: C.NAVY, d: 'Impulsa la automatización y escalabilidad al optimizar la implementación y administración de recursos virtuales, tales como VDI, DaaS y otros, a través de diversas plataformas.' },
    { t: 'Gestión', icon: 'broker', fill: C.BRAND_BLUE, d: 'Mejora la agilidad operativa de su organización y optimice la utilización de recursos mediante la centralización de la gestión y la simplificación del control de los recursos de TI. Simplifique las operaciones y reduzca la carga administrativa.' },
  ];
  const cardW = 4.0, cardH = 4.2, startY = 2.0, gap = 0.18;
  pillars.forEach((p, i) => {
    const x = MAR_L + i * (cardW + gap);
    card(s, x, startY, cardW, cardH, { fill: p.fill === C.NAVY ? (TH.dark ? C.DARK_CARD : C.NAVY) : TH.accentFill });
    s.addImage({ path: ICON(p.icon, true), x: x + 0.32, y: startY + 0.35, w: 0.7, h: 0.7, sizing: { type: 'contain', w: 0.7, h: 0.7 } });
    s.addText(p.t, { x: x + 0.32, y: startY + 1.2, w: cardW - 0.64, h: 0.8, fontFace: 'Inter SemiBold', fontSize: 19, color: C.WHITE, lineSpacingMultiple: 1.1 });
    s.addText(p.d, { x: x + 0.32, y: startY + 2.05, w: cardW - 0.64, h: 1.95, fontFace: 'Inter', fontSize: 11.5, color: C.TEXT_ON_BLUE, lineSpacingMultiple: 1.35 });
  });
  addFooter(s);
});

// 7 · Escritorios Virtuales (VDI) — source p7 (verbatim, 7 items)
SLIDE_BUILDERS.push(() => {
  const s = pres.addSlide();
  setMode(s);
  addTitleBar(s, 'Acceso seguro a VDI y VDA desde cualquier dispositivo', { size: 24 });
  addSubtitle(s, 'Escritorios Virtuales (VDI)');

  const items = [
    { t: 'Escritorios Persistentes (1:1)', d: 'Escritorios dedicados con Windows Server /10/11 para usuarios que necesitan un entorno personal consistente.' },
    { t: 'Escritorios No Persistentes', d: 'Escritorios desechables que se reinician después de cada sesión, brindando mayor seguridad y uso compartido.' },
    { t: 'Gestión de Perfiles de Usuario (FSLogix)', d: 'Perfiles centralizados para mantener una experiencia de usuario fluida entre sesiones.' },
    { t: 'Escritorios Basados en Sesión', d: 'Sesiones multiusuario de Windows Server para una publicación de escritorios rentable.' },
    { t: 'Clonación de Imagen Dorada', d: 'Implementación rápida de escritorios a partir de imágenes estandarizadas y preconfiguradas.' },
    { t: 'Autoescalado', d: 'Ajuste dinámico de la capacidad de escritorios según la demanda y los patrones de uso.' },
    { t: 'Soporte Multimonitor', d: 'Hasta 16 monitores simultáneos por sesión, incluyendo resolución 4K.' },
  ];
  const colW = (CONTENT_W - 0.5) / 2;
  const left = items.slice(0, 4), right = items.slice(4);
  bulletList(s, left, MAR_L, 1.95, colW, { dot: C.BRAND_BLUE, tSize: 12, dSize: 10, dH: 0.55, rowGap: 0.18 });
  bulletList(s, right, MAR_L + colW + 0.5, 1.95, colW, { dot: C.BRAND_BLUE, tSize: 12, dSize: 10, dH: 0.55, rowGap: 0.18 });
  addFooter(s);
});

// 8 · Aplicaciones Virtuales (VDA) — source p7 (verbatim, 4 items)
SLIDE_BUILDERS.push(() => {
  const s = pres.addSlide();
  setMode(s);
  addTitleBar(s, 'Acceso seguro a VDI y VDA desde cualquier dispositivo', { size: 24 });
  addSubtitle(s, 'Aplicaciones Virtuales (VDA)');

  const items = [
    { t: 'Publicación Individual de Aplicaciones', d: 'Entrega de aplicaciones específicas sin exponer el entorno completo del escritorio.' },
    { t: 'Gestión Centralizada de Aplicaciones', d: 'Instalación y actualización de todas las aplicaciones desde un único servidor para reducir la complejidad del mantenimiento.' },
    { t: 'Acceso Bajo Demanda a Aplicaciones', d: 'Acceso seguro a las aplicaciones desde cualquier dispositivo a través de un portal web unificado.' },
    { t: 'Aislamiento de Aplicaciones', d: 'Previene conflictos de DLL y dependencias al aislar las aplicaciones durante la ejecución.' },
  ];
  featureGrid(s, items, { cols: 2, x0: MAR_L, y0: 1.95, cardW: (CONTENT_W - 0.3) / 2, cardH: 2.1, gapX: 0.3, gapY: 0.25, brandIdx: () => false, titleH: 0.55, tSize: 15, dSize: 11 });
  addFooter(s);
});

// 9 · Enterprise VDI on Oracle (1/2) — source p8, blocks 1-3 (verbatim bullets)
SLIDE_BUILDERS.push(() => {
  const s = pres.addSlide();
  setMode(s);
  addTitleBar(s, 'Enterprise VDI on Oracle', { size: 26 });
  addSubtitle(s, 'Capacidades empresariales (1 de 2)');

  const blocks = [
    { h: 'Acceso Seguro a VDI y VDA', items: [
      'Acceso unificado a escritorios virtuales (VDI) y aplicaciones publicadas (VDA).',
      'Conexión sin cliente desde cualquier navegador web compatible con HTML5.',
      'Clientes nativos opcionales para Windows, macOS, iOS y Android.',
      'Portal web único para consolidar todos los recursos virtuales.',
      'Compatible con una amplia variedad de thin clients y PCs/laptops reutilizados.' ] },
    { h: 'Integración Nativa con Oracle', items: [
      'Elimine costos y complejidad evitando plataformas de virtualización de terceros como VMware o Hyper-V.',
      'Cree una imagen base (“golden image”) directamente en infraestructura nativa para estandarizar el despliegue de escritorios.',
      'Utilice herramientas nativas de clonación para un aprovisionamiento ultrarrápido de escritorios.',
      'Centralice actualizaciones y parches de seguridad modificando solo la imagen base.',
      'Garantice una experiencia de usuario consistente y un entorno 100% controlado sin capas intermedias.' ] },
    { h: 'Gestión de Acceso a Terceros', items: [
      'Implemente control de acceso basado en roles (RBAC) para permisos granulares y específicos.',
      'Proporcione acceso temporal a proveedores y contratistas mediante el portal unificado.',
      'Habilite sesiones privilegiadas Just-in-Time (JIT) con permisos que expiran automáticamente.',
      'Permita que los equipos de soporte realicen mantenimiento remoto seguro con auditoría y grabación de cada sesión.',
      'Elimine las contraseñas compartidas inyectando credenciales de forma segura en la sesión.' ] },
  ];
  const colW = (CONTENT_W - 0.6) / 3;
  blocks.forEach((b, i) => {
    const x = MAR_L + i * (colW + 0.3);
    s.addText(b.h, { x, y: 1.95, w: colW, h: 0.6, fontFace: 'Inter SemiBold', fontSize: 14, color: TH.dark ? C.BLUE_LIGHT : C.BRAND_BLUE, lineSpacingMultiple: 1.1 });
    bulletList(s, b.items, x, 2.65, colW, { dot: C.MINT, tSize: 10, rowGap: 0.14 });
  });
  addFooter(s);
});

// 10 · Enterprise VDI on Oracle (2/2) — source p8, blocks 4-5 (verbatim bullets)
SLIDE_BUILDERS.push(() => {
  const s = pres.addSlide();
  setMode(s);
  addTitleBar(s, 'Enterprise VDI on Oracle', { size: 26 });
  addSubtitle(s, 'Capacidades empresariales (2 de 2)');

  const blocks = [
    { h: 'Autenticación Segura', items: [
      'Integración nativa y transparente con Microsoft Active Directory para autenticación de usuarios.',
      'Soporte para federación de identidad (SSO) con proveedores como Okta, Azure AD y ADFS vía SAML.',
      'Capacidad para agregar un segundo factor de autenticación (2FA/MFA) a cualquier método de inicio de sesión.',
      'Autenticación moderna sin contraseña usando Passkeys y llaves de seguridad FIDO2.',
      'Soporte para redirección USB, permitiendo lectores de huellas y otros dispositivos biométricos dentro de la sesión virtual.',
      'Creación de un portal de acceso seguro y unificado que centraliza todos los métodos de autenticación.' ] },
    { h: 'Monitoreo y Auditoría', items: [
      'Visualice sesiones activas, usuarios conectados y uso de recursos en tiempo real.',
      'Genere informes y análisis sobre historial de conexiones, duración de sesiones y picos de concurrencia.',
      'Mantenga un registro de auditoría inmutable de todos los eventos de acceso y cambios administrativos.',
      'Grabe las sesiones de usuario en video como evidencia visual para auditorías o resolución de problemas.',
      'Integre con sistemas empresariales de monitoreo (por ejemplo, SIEM, Zabbix) para supervisión centralizada.' ] },
  ];
  const colW = (CONTENT_W - 0.5) / 2;
  blocks.forEach((b, i) => {
    const x = MAR_L + i * (colW + 0.5);
    s.addText(b.h, { x, y: 1.95, w: colW, h: 0.4, fontFace: 'Inter SemiBold', fontSize: 15, color: TH.dark ? C.BLUE_LIGHT : C.BRAND_BLUE });
    bulletList(s, b.items, x, 2.5, colW, { dot: C.MINT, tSize: 11, rowGap: 0.16 });
  });
  addFooter(s);
});

// 11 · Casos de uso table — source p9 (verbatim)
SLIDE_BUILDERS.push(() => {
  const s = pres.addSlide();
  setMode(s);
  addTitleBar(s, 'Todos los casos de uso con Citrix, AVD y Horizon', { size: 24 });
  addSubtitle(s, 'Simplificados con Thinfinity');

  const rows = [
    ['Call Centers y Equipos de Trabajo por Turnos', 'Admite equipos rotativos con licenciamiento por usuario concurrente, escritorios basados en sesiones y optimización de audio/VoIP. Ideal para centros de contacto, mesas de ayuda y BPOs.'],
    ['Habilitación de Fuerza Laboral Remota e Híbrida', 'Proporcione acceso seguro desde el navegador o cliente nativo desde cualquier dispositivo — sin VPNs ni dependencia del endpoint. Perfecto para empleados que trabajan desde casa o en modelos híbridos.'],
    ['Acceso de Terceros y Contratistas', 'Habilite el acceso seguro y controlado por políticas a escritorios internos, aplicaciones o sesiones SSH — con controles Zero Trust y sin exposición de red.'],
    ['Acceso Seguro a Aplicaciones para Usuarios BYOD', 'Entregue aplicaciones internas o SaaS vía navegador con aislamiento de sesión, filtrado por IP y políticas basadas en identidad. Ideal para dispositivos BYOD y no gestionados.'],
    ['Desarrolladores de Software y Equipos de QA', 'Provisión de máquinas virtuales desechables o escritorios basados en Linux con acceso vía SSH y navegador. Automatice su destrucción después de los ciclos de prueba.'],
    ['Entornos con Requisitos de Cumplimiento Normativo', 'Habilite grabación de sesiones, autenticación multifactor y filtrado por IP/ubicación. Cumple con requisitos estrictos de auditoría y control para banca, salud y sector público.'],
    ['Diseñadores, Ingenieros y Usuarios de CAD', 'Ejecute escritorios con aceleración por GPU para diseño, simulación y modelado 3D. Admite flujos de trabajo de alta resolución y múltiples monitores desde el navegador o cliente nativo.'],
    ['Laboratorios de Capacitación y Educación', 'Implemente escritorios virtuales para estudiantes o participantes con acceso temporal y programado. Restablecimiento automático tras cada sesión.'],
    ['Modernización de Aplicaciones Legadas', 'Entregue aplicaciones Win32 legadas desde la nube sin necesidad de modificar el código. Funciona mediante publicación estilo RemoteApp o escritorios completos.'],
  ];
  dataTable(s, ['Escenario', 'Cómo lo soporta Thinfinity'], rows, { y0: 1.95, rowH: 0.47, c0w: 3.9, hSize: 12, aSize: 10, bSize: 8.5 });
  addFooter(s);
});

// 12 · Capacidades Técnicas table — source p10 (verbatim)
SLIDE_BUILDERS.push(() => {
  const s = pres.addSlide();
  setMode(s);
  addTitleBar(s, 'Capacidades Técnicas: Todo lo que IT necesita', { size: 24 });
  addSubtitle(s, 'Sin la complejidad');

  const rows = [
    ['Entrega de escritorios basada en sesiones', 'Entornos multiusuario eficientes con infraestructura RDS escalable para escritorios compartidos.'],
    ['Aprovisionamiento de escritorios dedicados', 'Soporte para escritorios 1:1 persistentes o no persistentes, ideal para empleados remotos y usuarios avanzados.'],
    ['Virtualización acelerada por GPU', 'Gráficos y procesamiento de alto rendimiento para CAD, modelado 3D y cargas de trabajo multimedia.'],
    ['Automatización y orquestación', 'Aprovisionamiento automatizado, control del ciclo de vida de las sesiones y aplicación de políticas mediante Thinfinity Cloud Manager.'],
    ['Infraestructura con escalado automático', 'Escalado dinámico de máquinas virtuales según demanda, programación horaria o métricas de concurrencia.'],
    ['Optimización de audio y video', 'Redirección fluida de audio y video, optimizada para Teams, Zoom, VoIP y aplicaciones WebRTC.'],
    ['Redirección de periféricos', 'Redirección segura de dispositivos USB, impresoras, escáneres, tarjetas inteligentes y tabletas de firma.'],
    ['Acceso flexible', 'Acceso a escritorios desde el navegador o mediante los clientes nativos de Thinfinity para Windows, Linux, iOS y Android.'],
    ['Control de acceso basado en Zero Trust', 'Gestión de sesiones basada en identidad con filtrado por IP, MFA, SSO/SAML y control de políticas por roles.'],
    ['Entrega unificada de aplicaciones', 'Publicación de escritorios completos, aplicaciones individuales de Windows (estilo RemoteApp), SSH, VNC y aplicaciones web internas.'],
    ['Monitoreo y grabación de sesiones', 'Visibilidad en tiempo real de sesiones, registros de auditoría y grabación completa de sesiones para cumplimiento normativo.'],
    ['Acceso a archivos y carpetas', 'Acceso controlado por políticas a carpetas asignadas y sistemas de almacenamiento local o en la nube dentro de la sesión.'],
  ];
  dataTable(s, ['Capacidad', 'Descripción'], rows, { y0: 1.9, rowH: 0.375, c0w: 3.7, hSize: 11, aSize: 9.5, bSize: 8.5 });
  addFooter(s);
});

// 13 · Section divider — Arquitecturas (navy)  [merges source p24 + p25]
SLIDE_BUILDERS.push(() => {
  sectionDivider(pres.addSlide(), 'SECCIÓN', 'Arquitecturas', 'Arquitectura sugerida · del perímetro de red al despliegue multi-sitio');
  // footer
});

// Helper: user-group dashed zone with stacked uniform access pills (scale-driven)
function userGroup(s, x, y, sc, label, pills) {
  const w = sc.ZPADX * 2 + sc.PW;
  const h = sc.ZTOP + pills.length * sc.PH + (pills.length - 1) * (sc.VSTR - sc.PH) + sc.ZPADX;
  zone(s, x, y, w, h, label, { color: C.BRAND_BLUE, labelFill: '0A74D6', labelColor: C.WHITE, width: 1 });
  pills.forEach((p, i) => pill(s, x + sc.ZPADX, y + sc.ZTOP + i * sc.VSTR, p.t, sc, { icon: p.icon, cat: 'user' }));
  return { x, y, w, h, b: y + h, cx: x + w / 2, cy: y + h / 2, r: x + w };
}

// 14 · Arq — Dentro del perímetro de red (source p11)
SLIDE_BUILDERS.push(() => {
  const s = pres.addSlide();
  setMode(s);
  addTitleBar(s, 'Dentro del perímetro de red', { size: 26 });
  const _d = s._slideObjects.length;
  const sc = dScale(1.45);
  const g1 = userGroup(s, MAR_L, 1.5, sc, 'Gpo. de Usuarios 1', [
    { t: 'Acceso Web', icon: 'html5' }, { t: 'Thin Client', icon: 'pc' }, { t: 'Tablets\nAndroid', icon: 'pc' }]);
  const g2 = userGroup(s, MAR_L, g1.b + 0.25, sc, 'Gpo. de Usuarios 2', [
    { t: 'Acceso Web', icon: 'html5' }, { t: 'Acceso por\nCliente', icon: 'remote' }]);
  const midY = 3.35, by = midY - sc.PH / 2;
  const gw = pill(s, g1.r + 0.7, by, 'Gateway', sc, { icon: 'gateway', cat: 'thinfinity' });
  const bk = pill(s, gw.r + sc.GAP + 0.35, by, 'Broker\nPrimario', sc, { icon: 'broker', cat: 'thinfinity' });
  connect(s, g1, 'r', gw, 'l', { sc });
  connect(s, g2, 'r', gw, 'l', { sc });
  connect(s, bk, 'l', gw, 'r', { sc });
  s.addText('Tráfico TLS 1.3 · Puerto 443', { x: g1.r, y: by - 0.32, w: gw.x - g1.r, h: 0.25, fontFace: 'Inter', fontSize: 7.5, color: C.TEXT_SECONDARY, align: 'center' });
  s.addText('TLS 1.3 · Sin puertos abiertos', { x: gw.r, y: by - 0.32, w: bk.x - gw.r, h: 0.25, fontFace: 'Inter', fontSize: 7.5, color: C.TEXT_SECONDARY, align: 'center' });
  // Oracle Cloud red perimeter + 3 solid resource cards (solid sub-cards allowed; no dashed-in-dashed)
  const px = bk.r + 0.6, py = 1.5, pw = W - MAR_R - px, ph = 5.0;
  zone(s, px, py, pw, ph, 'Oracle Cloud (OCI / Datacenter)', { color: C.PERIMETER_RED, labelFill: '0A74D6', labelColor: C.WHITE, width: 2 });
  const ix = px + 0.3, iw = pw - 0.6, rh = 1.32, rgap = 0.14; let ry = py + 0.55;
  [{ l: 'Session Based Servers · Red 1', icon: 'server', n: 'Windows\nServer' },
   { l: 'Recursos Físicos · Red 2', icon: 'pc', n: 'Workstation' },
   { l: 'Servidores VDI · Red 3', icon: 'vdi', n: 'VDI Server' }].forEach(rg => {
    card(s, ix, ry, iw, rh, { fill: 'ECF1F8' });
    s.addText(rg.l, { x: ix + 0.18, y: ry + 0.1, w: iw - 0.36, h: 0.26, fontFace: 'Inter SemiBold', fontSize: 9.5, color: C.TEXT_PRIMARY });
    pill(s, ix + 0.25, ry + 0.5, rg.n, sc, { icon: rg.icon, cat: 'generic' });
    pill(s, ix + 0.25 + sc.HSTR, ry + 0.5, rg.n, sc, { icon: rg.icon, cat: 'generic' });
    ry += rh + rgap;
  });
  arrow(s, px, midY, bk.r, midY);   // resources → broker (into broker right)
  centerDiagram(s, _d, DREG);
  addFooter(s);
});

// 15 · Arq — Gateway en la DMZ (source p12)
SLIDE_BUILDERS.push(() => {
  const s = pres.addSlide();
  setMode(s);
  addTitleBar(s, 'Gateway en la DMZ', { size: 26 });
  const _d = s._slideObjects.length;
  const sc = dScale(1.45);
  const g1 = userGroup(s, MAR_L, 1.45, sc, 'Gpo. de Usuarios 1', [
    { t: 'Acceso Web', icon: 'html5' }, { t: 'Acceso por\nCliente', icon: 'remote' }, { t: 'PWA', icon: 'html5' }]);
  const g2 = userGroup(s, MAR_L, g1.b + 0.22, sc, 'Gpo. de Usuarios 2', [
    { t: 'Acceso Web', icon: 'html5' }, { t: 'Acceso por\nCliente', icon: 'remote' }]);
  const midY = 3.35, by = midY - sc.PH / 2;
  const gwx = g1.r + 0.75;
  zone(s, gwx - 0.2, by - 0.45, sc.PW + 0.4, sc.PH + 0.9, 'DMZ', { color: '8A93A0', fill: 'EDF1F7', width: 1.25 });
  const gw = pill(s, gwx, by, 'Thinfinity\nGateway', sc, { icon: 'gateway', cat: 'thinfinity' });
  const bk = pill(s, gw.r + sc.GAP + 0.4, by, 'Broker\nPrimario', sc, { icon: 'broker', cat: 'thinfinity' });
  connect(s, g1, 'r', gw, 'l', { sc });
  connect(s, g2, 'r', gw, 'l', { sc });
  connect(s, bk, 'l', gw, 'r', { sc });
  s.addText('TLS 1.3 · Puerto 443', { x: g1.r, y: by - 0.32, w: gw.x - g1.r, h: 0.25, fontFace: 'Inter', fontSize: 7, color: C.TEXT_SECONDARY, align: 'center' });
  s.addText('Sin puertos abiertos', { x: gw.r, y: by - 0.32, w: bk.x - gw.r, h: 0.25, fontFace: 'Inter', fontSize: 7, color: C.TEXT_SECONDARY, align: 'center' });
  const px = bk.r + 0.6, py = 1.5, pw = W - MAR_R - px, ph = 5.0;
  zone(s, px, py, pw, ph, 'Oracle Cloud / Datacenter', { color: C.PERIMETER_RED, labelFill: '0A74D6', labelColor: C.WHITE, width: 2 });
  const ix = px + 0.3, iw = pw - 0.6, rh = 1.32, rgap = 0.14; let ry = py + 0.55;
  [{ l: 'Servidor de aplicaciones · Server', icon: 'app-server', n: 'App Server' },
   { l: 'Recursos Físicos · Server 2', icon: 'pc', n: 'Workstation' },
   { l: 'VDI 1 a 1 · Server 3', icon: 'vdi', n: 'VDI 1:1' }].forEach(gr => {
    card(s, ix, ry, iw, rh, { fill: 'ECF1F8' });
    s.addText(gr.l, { x: ix + 0.18, y: ry + 0.1, w: iw - 0.36, h: 0.26, fontFace: 'Inter SemiBold', fontSize: 9.5, color: C.TEXT_PRIMARY });
    pill(s, ix + 0.25, ry + 0.5, gr.n, sc, { icon: gr.icon, cat: 'generic' });
    pill(s, ix + 0.25 + sc.HSTR, ry + 0.5, gr.n, sc, { icon: gr.icon, cat: 'generic' });
    ry += rh + rgap;
  });
  arrow(s, px, midY, bk.r, midY);
  centerDiagram(s, _d, DREG);
  addFooter(s);
});

// 16 · Arq — Híbrido (source p13)
SLIDE_BUILDERS.push(() => {
  const s = pres.addSlide();
  setMode(s);
  addTitleBar(s, 'Híbrido', { size: 26 });
  const _d = s._slideObjects.length;
  const sc = dScale(1.3);
  const g1 = userGroup(s, MAR_L, 1.5, sc, 'Usuarios Locales', [
    { t: 'Azure AD', icon: 'html5' }, { t: 'Okta', icon: 'html5' }, { t: 'Otro\nAzure AD', icon: 'html5' }]);
  const g2 = userGroup(s, MAR_L, g1.b + 0.2, sc, 'Usuarios Remotos', [
    { t: 'Okta', icon: 'html5' }, { t: 'Otro\nAzure AD', icon: 'html5' }]);
  // Gateway (admin zone) over Broker (OCI zone) — chip labels clear the pills
  const cx = g1.r + 0.85;
  const gzY = 2.5, ozY = 4.65, zH = sc.PH + 0.66, zW = sc.PW + 0.4;
  zone(s, cx - 0.2, gzY, zW, zH, 'Administración Ppia.', { color: '8A93A0', fill: 'EDF1F7', labelFill: '8A93A0', labelColor: C.WHITE, width: 1 });
  const gw = pill(s, cx, gzY + 0.42, 'Thinfinity\nGateway', sc, { icon: 'gateway', cat: 'thinfinity' });
  zone(s, cx - 0.2, ozY, zW, zH, 'OCI', { color: C.PERIMETER_RED, fill: 'FBF1F0', labelFill: '7A8694', labelColor: C.WHITE, width: 1.5 });
  const bk = pill(s, cx, ozY + 0.42, 'Thinfinity\nBroker', sc, { icon: 'broker', cat: 'thinfinity' });
  connect(s, g1, 'r', gw, 'l', { sc });
  connect(s, g2, 'r', gw, 'l', { sc });
  arrow(s, bk.cx, bk.y, gw.cx, gw.b);   // broker → gateway (outbound)
  s.addText('Puerto 443', { x: g1.r, y: gw.cy - 0.3, w: cx - g1.r, h: 0.22, fontFace: 'Inter', fontSize: 7, color: C.TEXT_SECONDARY, align: 'center' });
  s.addText('Tráfico\nSaliente\nTLS 1.3', { x: cx - 1.15, y: 3.85, w: 0.95, h: 0.6, fontFace: 'Inter', fontSize: 7, color: C.TEXT_SECONDARY, align: 'center', lineSpacingMultiple: 0.95 });
  // Targets: 2 OCI tenants (red) stacked + firewalls + on-prem (blue)
  function tenant(x, y, label, perimeter, note) {
    const w = sc.ZPADX * 2 + 2 * sc.PW + sc.GAP, h = sc.ZTOP + sc.PH + 0.45;
    zone(s, x, y, w, h, label, { color: perimeter ? C.PERIMETER_RED : C.BRAND_BLUE, labelFill: perimeter ? '7A8694' : '0A74D6', labelColor: C.WHITE, width: perimeter ? 1.75 : 1.25 });
    pill(s, x + sc.ZPADX, y + sc.ZTOP, 'VDI Server', sc, { icon: 'server', cat: 'generic' });
    pill(s, x + sc.ZPADX + sc.HSTR, y + sc.ZTOP, 'VDI Server', sc, { icon: 'server', cat: 'generic' });
    s.addText(note, { x: x + sc.ZPADX, y: y + h - 0.3, w: w - 2 * sc.ZPADX, h: 0.26, fontFace: 'Inter', fontSize: 7.5, color: C.TEXT_SECONDARY });
    return { x, y, w, h, r: x + w, cy: y + h / 2 };
  }
  const tx = cx + sc.PW + 0.7;
  const t1 = tenant(tx, 1.5, 'Tenant Principal de OCI', true, 'VDI · Aplicaciones Virtuales — sin puertos abiertos');
  const t2 = tenant(tx, 3.45, 'Tenant Secundario de OCI', true, 'VDI · Aplicaciones Virtuales — sin puertos abiertos');
  // firewall + on-prem to the right
  const fwx = t1.r + 0.25;
  pill(s, fwx, 2.0, 'Firewall', sc, { icon: 'firewall', cat: 'generic' });
  pill(s, fwx, 3.95, 'Firewall', sc, { icon: 'firewall', cat: 'generic' });
  const opx = fwx + sc.PW + 0.3, opw = W - MAR_R - opx;
  if (opw > sc.PW + 0.4) {
    const oph = sc.ZTOP + 2 * sc.PH + (sc.VSTR - sc.PH) + 0.5;
    zone(s, opx, 2.5, opw, oph, 'On prem', { color: C.BRAND_BLUE, labelFill: '0A74D6', labelColor: C.WHITE, width: 1.25 });
    pill(s, opx + (opw - sc.PW) / 2, 2.5 + sc.ZTOP, 'VDI Server', sc, { icon: 'server', cat: 'generic' });
    pill(s, opx + (opw - sc.PW) / 2, 2.5 + sc.ZTOP + sc.VSTR, 'Virtual Apps', sc, { icon: 'app-server', cat: 'generic' });
    s.addText('sin puertos abiertos', { x: opx + 0.15, y: 2.5 + oph - 0.3, w: opw - 0.3, h: 0.26, fontFace: 'Inter', fontSize: 7, color: C.TEXT_SECONDARY, align: 'center' });
  }
  arrow(s, bk.r, bk.cy, tx, t1.cy, { end: 'none', dash: 'dash' });
  arrow(s, bk.r, bk.cy, tx, t2.cy, { end: 'none', dash: 'dash' });
  centerDiagram(s, _d, DREG);
  addFooter(s);
});

// 17 · Aplicaciones Virtuales · Modo Seamless — source p14 (verbatim, 6 items)
SLIDE_BUILDERS.push(() => {
  const s = pres.addSlide();
  setMode(s);
  addTitleBar(s, 'Aplicaciones Virtuales · Modo Seamless', { size: 26 });
  addSubtitle(s, 'Ejecuta aplicaciones virtuales como si fueran locales');

  const items = [
    { t: 'Experiencia Nativa', d: 'Las aplicaciones virtuales se ejecutan y se comportan como aplicaciones locales en el escritorio del usuario.' },
    { t: 'Identificación Visual', d: 'Un borde azul rodea cada ventana de aplicación virtual y un ícono >< la identifica como una aplicación Thinfinity.' },
    { t: 'Seguridad desde el Diseño', d: 'Las aplicaciones se ejecutan dentro de la sesión VDI, aislándolas del dispositivo local.' },
    { t: 'Protección de la Infraestructura', d: 'Evita que vulnerabilidades del dispositivo local afecten los sistemas del backend.' },
    { t: 'Integración con la Barra de Tareas', d: 'Las aplicaciones aparecen en la barra de tareas de Windows como cualquier aplicación instalada.' },
    { t: 'Identificación en Taskbar', d: 'Un ícono >< las identifica como aplicaciones Thinfinity en la barra de tareas.' },
  ];
  featureGrid(s, items, { cols: 3, x0: MAR_L, y0: 1.95, cardW: (CONTENT_W - 0.5) / 3, cardH: 2.25, gapX: 0.25, gapY: 0.25, brandIdx: () => false, titleH: 0.5, tSize: 13.5, dSize: 10.5 });
  addFooter(s);
});

// 18 · Gestiona, Aprovisiona y Escala (Cloud Manager) — source p15 (verbatim, 5)
SLIDE_BUILDERS.push(() => {
  const s = pres.addSlide();
  setMode(s);
  addTitleBar(s, 'Gestiona, aprovisiona y escala escritorios y aplicaciones virtuales', { size: 22 });
  addSubtitle(s, 'Thinfinity Cloud Manager');

  const items = [
    { t: 'Gestión Centralizada de VDI', icon: 'broker', d: 'Aprovisiona, escala y gestiona entornos VDI en Oracle Cloud desde una única consola.' },
    { t: 'Control Unificado de Infraestructura', icon: 'cloud', d: 'Gestiona máquinas virtuales tanto en OCI como en entornos Oracle privados como PCA o OC3.' },
    { t: 'Automatización del Ciclo de Vida', icon: 'stats', d: 'Automatiza el encendido y apagado de instancias de cómputo OCI para optimizar el uso de recursos y controlar los costos.' },
    { t: 'Planes de Auto Escalado', icon: 'scale', d: 'Escala dinámicamente la capacidad VDI utilizando funciones nativas de autoescalado de OCI basadas en la demanda en tiempo real.' },
    { t: 'Políticas Optimizadas para Oracle', icon: 'shield', d: 'Aplica políticas de orquestación diseñadas específicamente para el ecosistema Oracle, facilitando la administración.' },
  ];
  featureGrid(s, items, { cols: 3, x0: MAR_L, y0: 1.95, cardW: (CONTENT_W - 0.5) / 3, cardH: 2.3, gapX: 0.25, gapY: 0.25, brandIdx: (i) => i === 0 || i === 2 || i === 4, titleH: 0.55, tSize: 13, dSize: 10.5 });
  addFooter(s);
});

// 19 · Experiencia de usuario nativa — source p16 (verbatim, 2 groups)
SLIDE_BUILDERS.push(() => {
  const s = pres.addSlide();
  setMode(s);
  addTitleBar(s, 'Experiencia de usuario nativa');

  const colW = (CONTENT_W - 0.5) / 2;
  const colY = 1.55;
  s.addShape('roundRect', { x: MAR_L, y: colY, w: colW, h: 0.42, fill: { color: TH.accentFill }, line: { type: 'none' }, rectRadius: 0.08 });
  s.addText('Compartir Recursos y Colaboración', { x: MAR_L + 0.2, y: colY, w: colW - 0.4, h: 0.42, fontFace: 'Inter SemiBold', fontSize: 14, color: TH.accentDark ? C.WHITE : C.BRAND_BLUE, valign: 'middle' });
  const left = ['Publicación de archivos y carpetas compartidas.', 'Portapapeles inteligente para texto y texto enriquecido.', 'Funciones avanzadas de transferencia de archivos.', 'Disco virtual personal.', 'Compartición de sesiones para soporte técnico.', 'Soporte integral de periféricos.', 'Impresión para puntos de venta (POS) y etiquetas.'];
  bulletList(s, left, MAR_L, colY + 0.6, colW, { dot: C.BRAND_BLUE, tSize: 12, rowGap: 0.26 });

  const rx = MAR_L + colW + 0.5;
  s.addShape('roundRect', { x: rx, y: colY, w: colW, h: 0.42, fill: { color: TH.accentFill }, line: { type: 'none' }, rectRadius: 0.08 });
  s.addText('Experiencia del Usuario Optimizada y Soporte a Periféricos', { x: rx + 0.2, y: colY, w: colW - 0.4, h: 0.42, fontFace: 'Inter SemiBold', fontSize: 12.5, color: TH.accentDark ? C.WHITE : C.BRAND_BLUE, valign: 'middle' });
  const right = ['Soporte multi-monitor sin cliente.', 'Resolución 4K soportada.', 'Hasta 16 monitores virtuales.', 'RTVA (Audio y Video en Tiempo Real).', 'Soporte para Teams, Google Meets, Zoom y otras herramientas de colaboración.'];
  bulletList(s, right, rx, colY + 0.6, colW, { dot: C.MINT, tSize: 12, rowGap: 0.26 });
  addFooter(s);
});

// 20 · Grabación de sesiones — source p17 (verbatim, 8 items)
SLIDE_BUILDERS.push(() => {
  const s = pres.addSlide();
  setMode(s);
  addTitleBar(s, 'Grabación de sesiones');
  addSubtitle(s, 'Capacidades de grabación de sesiones');

  const items = [
    { t: 'Grabación Completa de Sesiones', d: 'Captura la actividad visual completa de las sesiones de usuario en formato de video.' },
    { t: 'Configuración Granular', d: 'Defina qué usuarios, grupos o perfiles de conexión serán grabados.' },
    { t: 'Invisible para los Usuarios', d: 'Funciona de manera transparente, grabando sesiones sin que los usuarios lo perciban ni se interrumpan.' },
    { t: 'Reproducción en la Consola', d: 'Visualice las grabaciones directamente desde la consola de administración sin necesidad de exportar archivos.' },
    { t: 'Historial con búsqueda', d: 'Filtre los registros de sesión por usuario, fecha o dispositivo para localizar rápidamente grabaciones específicas.' },
    { t: 'Almacenamiento Centralizado y Seguro', d: 'Guarde todos los archivos de video en una ubicación protegida y centralizada para fácil acceso.' },
    { t: 'Evidencia Lista para Auditoría', d: 'Utilice las grabaciones de sesión como prueba visual para auditorías de cumplimiento y seguridad.' },
    { t: 'Soporte para Resolución de Problemas', d: 'Reproduzca sesiones de usuario para reproducir y analizar errores o fallos reportados.' },
  ];
  featureGrid(s, items, { cols: 4, x0: MAR_L, y0: 1.9, cardW: (CONTENT_W - 0.6) / 4, cardH: 2.3, gapX: 0.2, gapY: 0.2, brandIdx: () => false, titleH: 0.75, tSize: 12, dSize: 9.5 });
  addFooter(s);
});

// 21 · Conexiones secundarias — source p18 (verbatim, 5 items)
SLIDE_BUILDERS.push(() => {
  const s = pres.addSlide();
  setMode(s);
  addTitleBar(s, 'Conexiones secundarias');
  addSubtitle(s, 'Tipos de conexiones secundarias');

  const items = [
    { t: 'Acceso SSH basado en navegador', d: 'Acceso seguro a la línea de comandos de servidores remotos directamente desde cualquier navegador web.' },
    { t: 'Acceso remoto a escritorio VNC', d: 'Conéctese a sistemas remotos usando el protocolo estándar VNC para sesiones gráficas.' },
    { t: 'Cliente VNC optimizado', d: 'Aproveche el cliente VNC integrado de alto rendimiento de Thinfinity para una experiencia visual fluida.' },
    { t: 'Integración de archivos WebDAV', d: 'Acceda a carpetas y archivos en red como si fueran unidades locales, a través de WebDAV.' },
    { t: 'Pasarela de aplicaciones web (WAG)', d: 'Publique de forma segura aplicaciones web internas (por ejemplo, intranets) mediante una pasarela accesible por navegador con controles Zero Trust.' },
  ];
  featureGrid(s, items, { cols: 3, x0: MAR_L, y0: 1.95, cardW: (CONTENT_W - 0.5) / 3, cardH: 2.3, gapX: 0.25, gapY: 0.25, brandIdx: (i) => i === 0 || i === 4, titleH: 0.55, tSize: 13, dSize: 10.5 });
  addFooter(s);
});

// 22 · Broker y Monitoreo VDI — source p19 (verbatim, 6 items)
SLIDE_BUILDERS.push(() => {
  const s = pres.addSlide();
  setMode(s);
  addTitleBar(s, 'Broker y Monitoreo VDI');
  addSubtitle(s, 'Monitor de Broker y Monitoreo de VDI');

  const items = [
    { t: 'Monitoreo del Rendimiento de VM', d: 'Monitorea el uso de CPU, disco y memoria de cada máquina virtual en tiempo real.' },
    { t: 'Informes de Estado de Salud', d: 'Genera informes individuales de salud por dispositivo para evaluar la integridad del sistema.' },
    { t: 'Detección de VMs Inactivas', d: 'Identifica máquinas no utilizadas o subutilizadas para desmantelarlas y optimizar costos.' },
    { t: 'Monitoreo de Almacenamiento', d: 'Observa el almacenamiento disponible en los servidores para anticipar necesidades de capacidad y evitar fallas.' },
    { t: 'Alertas Basadas en Umbrales', d: 'Dispara notificaciones automáticas cuando se exceden los umbrales de rendimiento.' },
    { t: 'Alertas a Nivel de Procesos', d: 'Crea alertas basadas en procesos específicos monitoreados para detectar anomalías o fallas.' },
  ];
  featureGrid(s, items, { cols: 3, x0: MAR_L, y0: 1.95, cardW: (CONTENT_W - 0.5) / 3, cardH: 2.25, gapX: 0.25, gapY: 0.25, brandIdx: (i) => i % 2 === 0, titleH: 0.55, tSize: 13, dSize: 10.5 });
  addFooter(s);
});

// 23 · Analíticas y Auditoría — source p20 (verbatim, 12 items)
SLIDE_BUILDERS.push(() => {
  const s = pres.addSlide();
  setMode(s);
  addTitleBar(s, 'Analíticas y Auditoría');
  addSubtitle(s, 'Analíticas y Auditoría de Actividad');

  const items = [
    { t: 'Monitoreo de Sesiones en Tiempo Real', d: 'Visualiza todas las sesiones de usuario activas en tiempo real.' },
    { t: 'Registro de Historial de Sesiones', d: 'Registra cada evento de inicio y cierre de sesión por usuario.' },
    { t: 'Auditoría de Accesos', d: 'Rastrea quién se conectó, a qué recurso, desde dónde y cuándo.' },
    { t: 'Seguimiento de Transferencias de Archivos', d: 'Monitorea las cargas y descargas de archivos durante una sesión.' },
    { t: 'Información del Entorno del Usuario', d: 'Identifica los navegadores y sistemas operativos más usados.' },
    { t: 'Reportes de Uso', d: 'Genera informes sobre la duración de las sesiones y el total de conexiones a lo largo del tiempo.' },
    { t: 'Grabación de Video de Sesiones', d: 'Captura sesiones completas de usuarios para cumplimiento, soporte o revisión de incidentes.' },
    { t: 'Registro de Cambios de Administrador', d: 'Registra cada cambio de configuración realizado por los administradores.' },
    { t: 'Filtrado de Eventos', d: 'Busca en el historial de auditoría por usuario, tipo de evento o rango de fechas.' },
    { t: 'Analíticas de Concurrencia', d: 'Analiza las tendencias de uso máximo para guiar la planificación de capacidad.' },
    { t: 'Verificación de Uso de Periféricos', d: 'Monitorea el uso de dispositivos como impresoras o unidades mapeadas.' },
    { t: 'Exportación de Logs de Auditoría', d: 'Exporta todos los datos de auditoría para análisis externo, cumplimiento o integración con SIEM.' },
  ];
  featureGrid(s, items, { cols: 4, x0: MAR_L, y0: 1.78, cardW: (CONTENT_W - 0.6) / 4, cardH: 1.55, gapX: 0.2, gapY: 0.14, brandIdx: () => false, titleH: 0.6, tSize: 11, dSize: 8.5 });
  addFooter(s);
});

// 24 · Sesiones compartidas — source p21 (verbatim, 9 items)
SLIDE_BUILDERS.push(() => {
  const s = pres.addSlide();
  setMode(s);
  addTitleBar(s, 'Sesiones compartidas');
  addSubtitle(s, 'Sesiones Compartidas y Capacidades de Soporte Remoto');

  const items = [
    { t: 'Soporte para Kioscos y TPV (Punto de Venta)', d: 'Diagnostica y resuelve problemas en sistemas de sucursal como kioscos y terminales de punto de venta, sin necesidad de enviar técnicos al sitio.' },
    { t: 'Soporte en Vivo para Usuarios de VDI', d: 'Proporciona asistencia en tiempo real dentro del escritorio virtual del usuario, como si estuvieras sentado a su lado.' },
    { t: 'Solución de Problemas en Aplicaciones Virtuales', d: 'Investiga y soluciona problemas dentro de aplicaciones virtualizadas de manera eficiente, sin interrumpir la sesión.' },
    { t: 'Toma Activa de Sesión', d: 'Toma el control de la sesión del usuario para una resolución directa y práctica.' },
    { t: 'Configuración Remota de Hardware', d: 'Configura impresoras, escáneres u otros dispositivos conectados a entornos VDI remotos, incluso entre distintas ubicaciones.' },
    { t: 'Demostraciones y Entrenamiento de Software Remotos', d: 'Guía a los usuarios en tiempo real dentro de su propio entorno para onboarding, demostraciones o capacitación.' },
    { t: 'Validación de Dispositivos Biométricos', d: 'Guía a los usuarios en tiempo real dentro de su propio entorno para onboarding, demostraciones o capacitación.' },
    { t: 'Revisiones de Auditoría y Cumplimiento', d: 'Inspecciona configuraciones de sesiones virtuales y actividad de usuarios para validar el cumplimiento de políticas a distancia.' },
    { t: 'Colaboración Multi-Técnicos', d: 'Permite que varios agentes o expertos de soporte vean o interactúen con la misma sesión de usuario para una resolución más rápida.' },
  ];
  featureGrid(s, items, { cols: 3, x0: MAR_L, y0: 1.88, cardW: (CONTENT_W - 0.5) / 3, cardH: 1.55, gapX: 0.25, gapY: 0.14, brandIdx: () => false, titleH: 0.5, tSize: 11.5, dSize: 9 });
  addFooter(s);
});

// 25 · Dashboard GeoIP — source p22 (verbatim, 7 items)
SLIDE_BUILDERS.push(() => {
  const s = pres.addSlide();
  setMode(s);
  addTitleBar(s, 'Dashboard GeoIP');
  addSubtitle(s, 'GeoIP y Restricción de IP');

  const items = [
    { t: 'Bloqueo de Tráfico en Dos Niveles', d: 'Implementa seguridad de doble capa restringiendo el acceso basado en Geo-IP y direcciones IP individuales.' },
    { t: 'Bloqueo por Geo-IP', d: 'Previene conexiones desde regiones geográficas de alto riesgo conocidas por actividad maliciosa.' },
    { t: 'Bloqueo de IP Individual', d: 'Bloquea direcciones IP específicas que muestran comportamiento sospechoso o no autorizado.' },
    { t: 'Panel de Control Geo-IP', d: 'Gestiona y configura reglas de Geo-IP directamente desde un portal centralizado con controles intuitivos.' },
    { t: 'Alertas en Tiempo Real', d: 'Recibe notificaciones instantáneas por intentos de acceso desde regiones bloqueadas o IPs en lista negra.' },
    { t: 'Reportes de Tráfico y Bloqueos', d: 'Genera reportes regulares para evaluar la efectividad del bloqueo y detectar nuevos patrones de amenaza.' },
    { t: 'Actualizaciones de Inteligencia de Amenazas', d: 'Mantén una base de datos continuamente actualizada de direcciones IP y rangos geográficos de alto riesgo.' },
  ];
  featureGrid(s, items, { cols: 4, x0: MAR_L, y0: 1.95, cardW: (CONTENT_W - 0.6) / 4, cardH: 2.1, gapX: 0.2, gapY: 0.2, brandIdx: () => false, titleH: 0.6, tSize: 12, dSize: 9.5 });
  addFooter(s);
});

// 26 · Brokers secundarios y Agentes — source p23 (verbatim, 4 items, navy bg)
SLIDE_BUILDERS.push(() => {
  const s = pres.addSlide();
  setBg(s, C.NAVY);
  s.addText('Brokers secundarios y Agentes', { x: MAR_L, y: TITLE_TOP, w: CONTENT_W, h: 0.7, fontFace: 'Inter SemiBold', fontSize: 28, color: C.WHITE });

  const items = [
    { t: 'Balanceo de Carga Descentralizado', icon: 'scale', d: 'Los Brokers Secundarios descentralizan el proceso de virtualización, permitiendo que Thinfinity gestione conexiones a lo largo de una infraestructura de red dispersa. Esto permite una distribución eficiente de las cargas de trabajo y mejora la capacidad del sistema para escalar.' },
    { t: 'Agrupación de Recursos', icon: 'broker', d: 'El uso de Brokers Secundarios facilita la agrupación de aplicaciones o escritorios, que pueden asignarse dinámicamente según la demanda. Esto contribuye a un uso más eficiente de los recursos y soporta el escalado conforme a las necesidades de los usuarios.' },
    { t: 'Alta Disponibilidad y Tolerancia a Fallos', icon: 'shield', d: 'Con Brokers Secundarios y Agentes de Virtualización en funcionamiento, Thinfinity garantiza alta disponibilidad y tolerancia a fallos, manteniendo la continuidad del servicio y minimizando el tiempo de inactividad.' },
    { t: 'Rendimiento Mejorado en Entornos Multi-Tenant', icon: 'stats', d: 'Al utilizar Brokers Secundarios, Thinfinity puede atender eficazmente a un gran número de usuarios y sesiones simultáneamente, garantizando un rendimiento óptimo incluso en entornos complejos y multi-tenant.' },
  ];
  const cols = 2, gapX = 0.3, gapY = 0.25;
  const cardW = (CONTENT_W - gapX) / 2, cardH = 2.15;
  items.forEach((it, i) => {
    const col = i % cols, row = Math.floor(i / cols);
    const x = MAR_L + col * (cardW + gapX);
    const y = 1.55 + row * (cardH + gapY);
    card(s, x, y, cardW, cardH, { fill: C.DARK_CARD });
    s.addImage({ path: ICON(it.icon, true), x: x + 0.28, y: y + 0.28, w: 0.55, h: 0.55, sizing: { type: 'contain', w: 0.55, h: 0.55 } });
    s.addText(it.t, { x: x + 1.0, y: y + 0.28, w: cardW - 1.25, h: 0.6, fontFace: 'Inter SemiBold', fontSize: 15, color: C.WHITE, lineSpacingMultiple: 1.1, valign: 'middle' });
    s.addText(it.d, { x: x + 0.28, y: y + 0.95, w: cardW - 0.56, h: 1.1, fontFace: 'Inter', fontSize: 10, color: C.TEXT_ON_NAVY, lineSpacingMultiple: 1.28 });
  });
  addFooter(s, { dark: true });
});

// ─── Scaling-diagram building blocks (scale-driven, skill grammar) ───

// HA cluster on a grid: Users → Load Balancer → Gateway×2 ⇄ Broker×2 → DB.
// Columns spaced by HSTR (=PW+GAP → exactly one pill-height gap). opts: {sc, usersLabel,
// clientLabel, db, ha, shortNodes}
function haCore(s, ox, oy, opts = {}) {
  const sc = opts.sc, PH = sc.PH, ha = opts.ha !== false;
  const colx = i => ox + i * sc.HSTR;
  const bandCy = oy + (ha ? PH / 2 + sc.VSTR / 2 : PH / 2);
  const by = bandCy - PH / 2;
  const users = pill(s, colx(0), by, opts.usersLabel || 'Users', sc, { icon: 'user-group', cat: 'user' });
  if (opts.clientLabel) pill(s, colx(0), by + sc.VSTR, opts.clientLabel, sc, { icon: 'pc', cat: 'user' });
  const lb = pill(s, colx(1), by, 'Load\nBalancer', sc, { icon: 'load-balancer' });
  const gwL = opts.shortNodes ? 'Gateway' : 'Thinfinity\nGateway';
  const bkL = opts.shortNodes ? 'Broker' : 'Thinfinity\nBroker';
  const gwT = pill(s, colx(2), oy, gwL, sc, { icon: 'gateway', cat: 'thinfinity' });
  const gwB = ha ? pill(s, colx(2), oy + sc.VSTR, gwL, sc, { icon: 'gateway', cat: 'thinfinity' }) : null;
  const bkT = pill(s, colx(3), oy, bkL, sc, { icon: 'broker', cat: 'thinfinity' });
  const bkB = ha ? pill(s, colx(3), oy + sc.VSTR, bkL, sc, { icon: 'broker', cat: 'thinfinity' }) : null;
  const db = pill(s, colx(4), by, opts.db || 'MySQL\nData Base', sc, { icon: 'database' });
  // connectors (orthogonal, edge-centered; reverse toward gateway)
  connect(s, users, 'r', lb, 'l', { sc });
  connect(s, lb, 'r', gwT, 'l', { sc });
  if (ha) {
    connect(s, lb, 'r', gwB, 'l', { sc });
    connect(s, bkT, 'l', gwT, 'r', { sc });           // same row → straight
    connect(s, bkB, 'l', gwB, 'r', { sc });
    arrow(s, bkT.x, bkT.cy, gwB.r, gwB.cy);           // diagonal cross (matches source)
    arrow(s, bkB.x, bkB.cy, gwT.r, gwT.cy);
    connect(s, bkT, 'r', db, 'l', { sc, end: 'none' });
    connect(s, bkB, 'r', db, 'l', { sc, end: 'none' });
  } else {
    connect(s, bkT, 'l', gwT, 'r', { sc });
    connect(s, bkT, 'r', db, 'l', { sc, end: 'none' });
  }
  return { users, lb, gwT, gwB, bkT, bkB, db, bandCy, rightX: colx(4) + sc.PW, top: oy, bottom: oy + (ha ? sc.VSTR + PH : PH) };
}

// Resource zone: dashed container + uniform pills on the grid (zone_y+48, zone_x+20).
// tiles:[{label,icon}]. Returns geometry. Auto-sizes to the grid.
function resourceZone(s, x, y, sc, tiles, cols, title) {
  const rows = Math.ceil(tiles.length / cols);
  const w = sc.ZPADX * 2 + cols * sc.PW + (cols - 1) * sc.GAP;
  const top = title ? sc.ZTOP : sc.ZPADX + 0.06;
  const h = top + rows * sc.PH + (rows - 1) * (sc.VSTR - sc.PH) + sc.ZPADX;
  zone(s, x, y, w, h, '', { color: '9B86D6', fill: 'F6F3FC', width: 1.25, dash: 'dash' });
  if (title) {
    s.addImage({ path: DICON('network', 'dark'), x: x + sc.ZPADX - 0.02, y: y + sc.ZLY - 0.28, w: sc.ZICON, h: sc.ZICON, sizing: { type: 'contain', w: sc.ZICON, h: sc.ZICON } });
    s.addText(title, { x: x + sc.ZLX, y: y + 0.1, w: w - sc.ZLX - 0.1, h: 0.3, fontFace: 'Inter SemiBold', fontSize: sc.FSZ, color: C.TEXT_PRIMARY, valign: 'middle' });
  }
  tiles.forEach((t, i) => {
    const c = i % cols, r = Math.floor(i / cols);
    pill(s, x + sc.ZPADX + c * sc.HSTR, y + top + r * sc.VSTR, t.label, sc, { icon: t.icon, cat: 'generic', align: 'left' });
  });
  return { x, y, w, h, r: x + w, b: y + h, cx: x + w / 2, top, cols, rows };
}

// Specs panel (light card) with arrow-bullets. specs:[{c,v}]
function specsPanel(s, x, y, w, h, specs) {
  card(s, x, y, w, h, { fill: 'EAF1FB', line: { type: 'none' } });
  let cy = y + 0.22;
  specs.forEach(sp => {
    s.addText('➔', { x: x + 0.22, y: cy, w: 0.3, h: 0.3, fontFace: 'Inter SemiBold', fontSize: 11, color: C.BRAND_BLUE });
    s.addText(sp.c, { x: x + 0.55, y: cy, w: w - 0.75, h: 0.3, fontFace: 'Inter SemiBold', fontSize: 11, color: C.TEXT_PRIMARY });
    s.addText(sp.v, { x: x + 0.55, y: cy + 0.28, w: w - 0.75, h: 0.5, fontFace: 'Inter', fontSize: 9.5, color: C.TEXT_BODY, lineSpacingMultiple: 1.15 });
    cy += 0.28 + estH(sp.v, w - 0.75, 9.5, 1.15) + 0.14;
  });
}

// Vertical dashed firewall/WAF marker with top label
function fwLine(s, x, y0, y1, labels) {
  s.addShape('line', { x, y: y0, w: 0, h: y1 - y0, line: { color: '9AA4B0', width: 1.25, dashType: 'dash' } });
  s.addText(labels, { x: x - 0.7, y: y0 - 0.3, w: 1.4, h: 0.26, fontFace: 'Inter SemiBold', fontSize: 8, color: C.TEXT_SECONDARY, align: 'center' });
}

// Reverse-connection bus from a resource zone back to the gateway (over the top, orthogonal).
// Single arrowhead into the gateway top edge-center; ≥RUN straight before the chevron.
function agentBus(s, gw, zone, sc, topY) {
  const zx = zone.cx;
  arrow(s, zx, zone.y, zx, topY, { end: 'none' });              // up out of zone
  arrow(s, zx, topY, gw.cx, topY, { end: 'none' });             // across
  arrow(s, gw.cx, topY, gw.cx, gw.y, { end: 'triangle' });      // down into gateway top-center
}

const WIN11 = { label: 'Windows 11\n+ Agent', icon: 'windows' };
const WINSRV = { label: 'Windows Server\n+ Agent', icon: 'server' };
const LINUX = { label: 'Linux Server\nUbuntu', icon: 'linux' };

// VDI resource tiles (2-line uniform pills)
const WSVDI = { label: 'Windows\nServer VDI', icon: 'vdi' };
const W10VDI = { label: 'Windows 10\nVDI', icon: 'windows' };
const VAPP = { label: 'Virtual\nApplications', icon: 'app-virtualization' };

// DR mini-row (non-HA) at scale sc: URL Recovery → Gateway → Broker → DB
function drRow(s, ox, cy, sc) {
  const colx = i => ox + i * sc.HSTR, by = cy - sc.PH / 2;
  const ur = pill(s, colx(0), by, 'URL\nRecovery', sc, { icon: 'refresh' });
  const gw = pill(s, colx(1), by, 'Gateway', sc, { icon: 'gateway', cat: 'thinfinity' });
  const bk = pill(s, colx(2), by, 'Broker', sc, { icon: 'broker', cat: 'thinfinity' });
  const db = pill(s, colx(3), by, 'SQL\nData Base', sc, { icon: 'database' });
  connect(s, ur, 'r', gw, 'l', { sc });
  connect(s, bk, 'l', gw, 'r', { sc });
  connect(s, bk, 'r', db, 'l', { sc, end: 'none' });
  return { ur, gw, bk, db };
}

// 27 · Sitio Inicial 50-1000 — Windows 11 + Agent subnet (source p26)
SLIDE_BUILDERS.push(() => {
  const s = pres.addSlide();
  setMode(s);
  addTitleBar(s, 'Sitio Inicial: 50 - 1000 usuarios', { size: 24 });
  s.addText('En este nivel, podemos escalar los componentes existentes. La arquitectura principal se mantiene igual. Diseño para alta disponibilidad.',
    { x: MAR_L, y: 1.18, w: 7.8, h: 0.55, fontFace: 'Inter', fontSize: 11, color: C.TEXT_BODY, lineSpacingMultiple: 1.2 });
  const _d = s._slideObjects.length;
  const sc = dScale(1.35);
  const core = haCore(s, MAR_L, 2.75, { sc, usersLabel: 'User 1 · 2\n3 · n' });
  const pz = resourceZone(s, core.rightX + sc.GAP, 2.05, sc, [WIN11, WIN11, WIN11, WIN11, WIN11, WIN11], 2, 'Subnet');
  agentBus(s, core.gwT, pz, sc, 1.7);
  centerDiagram(s, _d, DREG);
  addFooter(s);
});

// 28 · Sitio Inicial 50-1000 — App Pool Windows Server + specs (source p27)
function siteWithSpecs(title, tiles, poolTitle, db) {
  return () => {
    const s = pres.addSlide();
    setMode(s);
    addTitleBar(s, title, { size: 24 });
    const _d = s._slideObjects.length;
    const sc = dScale(1.18);
    const core = haCore(s, MAR_L, 1.75, { sc, usersLabel: 'Users', clientLabel: 'Windows\nClient', shortNodes: true, db });
    const pz = resourceZone(s, core.rightX + sc.GAP, 1.55, sc, tiles, 3, poolTitle);
    agentBus(s, core.gwT, pz, sc, 1.3);
    fwLine(s, core.lb.x - sc.GAP / 2, 1.45, core.bottom + 0.2, 'WAF · Firewall');
    fwLine(s, core.bkT.r + sc.GAP / 2, 1.45, core.bottom + 0.2, 'Firewall');
    centerDiagram(s, _d, UREG);
    specsPanel(s, MAR_L, 4.55, 5.4, 2.1, [
      { c: 'Gateway', v: '2 × 4 vCPU · 16 GB de RAM' },
      { c: 'Broker', v: '2 × 8 vCPU · 32 GB de RAM' },
      { c: 'Base de Datos ' + (db ? 'SQL' : 'MySQL'), v: '4 vCPU · 8 GB de RAM (considerar un servicio SQL gestionado para facilitar el escalado y la alta disponibilidad)' },
    ]);
    addFooter(s);
  };
}
SLIDE_BUILDERS.push(siteWithSpecs('Sitio Inicial: 50 - 1000 usuarios', [WINSRV, WINSRV, WINSRV, WINSRV, WINSRV, WINSRV], 'Subnet · App Pool'));
// 29 · Sitio Inicial 50-1000 — App Pool Linux/Ubuntu + specs (source p28)
SLIDE_BUILDERS.push(siteWithSpecs('Sitio Inicial: 50 - 1000 usuarios', [LINUX, LINUX, LINUX, LINUX, LINUX, LINUX], 'Subnet · App Pool'));

// 30 · Sitio Inicial 100-1000 con DR (source p29)
SLIDE_BUILDERS.push(() => {
  const s = pres.addSlide();
  setMode(s);
  addTitleBar(s, 'Sitio Inicial: 100 - 1000 usuarios con Recuperación ante Desastres', { size: 18 });
  s.addText('Agregamos un sitio de recuperación ante desastres añadiendo un gateway y un broker adicionales, junto con la sincronización de la base de datos SQL con el entorno principal y una URL de recuperación.',
    { x: MAR_L, y: 1.02, w: CONTENT_W, h: 0.45, fontFace: 'Inter', fontSize: 10, color: C.TEXT_BODY, lineSpacingMultiple: 1.15 });
  const _d = s._slideObjects.length;
  const sc = dScale(1.12);
  const core1 = haCore(s, MAR_L, 1.82, { sc, shortNodes: true });
  const pz1 = resourceZone(s, core1.rightX + sc.GAP, 1.72, sc, [WIN11, WIN11, WIN11, WINSRV, WINSRV, WINSRV], 3, 'Subnet');
  agentBus(s, core1.gwT, pz1, sc, 1.64);
  s.addShape('line', { x: MAR_L, y: 4.1, w: CONTENT_W, h: 0, line: { color: C.BORDER_LIGHT, width: 1, dashType: 'dash' } });
  const dr = drRow(s, MAR_L, 4.95, sc);
  const pz2 = resourceZone(s, core1.rightX + sc.GAP, 4.45, sc, [WIN11, WIN11, WIN11, WINSRV, WINSRV, WINSRV], 3, 'Subnet');
  agentBus(s, dr.gw, pz2, sc, 4.35);
  arrow(s, core1.db.cx, core1.db.b, dr.db.cx, dr.db.y, { dash: 'dash', begin: 'triangle' });  // SQL replication
  centerDiagram(s, _d, DREG);
  addFooter(s);
});

// 31 · 2 Sitios Activo-Activo (source p30) — with FSLogix
SLIDE_BUILDERS.push(() => {
  const s = pres.addSlide();
  setMode(s);
  addTitleBar(s, '2 Sitios Activo-Activo (1000 a 5000 usuarios)', { size: 22 });
  s.addText('Los sitios pueden escalarse vertical y regionalmente añadiendo más gateways, brokers y sitios. FSLogix para perfiles centralizados.',
    { x: MAR_L, y: 1.08, w: CONTENT_W, h: 0.45, fontFace: 'Inter', fontSize: 10, color: C.TEXT_BODY });
  const _d = s._slideObjects.length;
  const sc = dScale(1.12);
  const tiles = [WIN11, WIN11, WIN11, WINSRV, WINSRV, WINSRV];
  const fW = 1.25;
  const c1 = haCore(s, MAR_L, 1.8, { sc, shortNodes: true });
  const pz1 = resourceZone(s, c1.rightX + sc.GAP, 1.68, sc, tiles, 2, 'Subnet');
  agentBus(s, c1.gwT, pz1, sc, 1.62);
  s.addText('Site 1', { x: MAR_L, y: 3.85, w: 1.5, h: 0.22, fontFace: 'Inter SemiBold', fontSize: 10, color: C.TEXT_SECONDARY });
  s.addShape('line', { x: MAR_L, y: 4.08, w: CONTENT_W, h: 0, line: { color: C.BORDER_LIGHT, width: 1, dashType: 'dash' } });
  s.addText('Site 2', { x: MAR_L, y: 4.12, w: 1.5, h: 0.22, fontFace: 'Inter SemiBold', fontSize: 10, color: C.TEXT_SECONDARY });
  const c2 = haCore(s, MAR_L, 4.45, { sc, shortNodes: true });
  const pz2 = resourceZone(s, c2.rightX + sc.GAP, 4.3, sc, tiles, 2, 'Subnet');
  agentBus(s, c2.gwT, pz2, sc, 4.2);
  // FSLogix box far right (spans both sites)
  const fx = Math.max(pz1.r, pz2.r) + sc.GAP;
  if (fx + fW <= W - MAR_R) {
    card(s, fx, 2.5, fW, 2.6, { fill: 'EAF1FB', line: { color: C.BORDER_LIGHT, width: 1 } });
    s.addImage({ path: DICON('fslogix', ''), x: fx + (fW - 0.5) / 2, y: 3.2, w: 0.5, h: 0.5, sizing: { type: 'contain', w: 0.5, h: 0.5 } });
    s.addText('FSLogix', { x: fx, y: 3.8, w: fW, h: 0.4, fontFace: 'Inter SemiBold', fontSize: 13, color: C.BRAND_BLUE, align: 'center' });
  }
  centerDiagram(s, _d, DREG);
  addFooter(s);
});

// 32 · Arquitectura de Pilot to Production (source p31) — single, non-HA
SLIDE_BUILDERS.push(() => {
  const s = pres.addSlide();
  setMode(s);
  addTitleBar(s, 'Arquitectura de Pilot to Production', { size: 24 });
  s.addText('Arquitectura diseñada para desplegar en un tenant existente del cliente, compartment separado, pensada para escalar fácilmente a un ambiente productivo.',
    { x: MAR_L, y: 1.2, w: CONTENT_W, h: 0.5, fontFace: 'Inter', fontSize: 12, color: C.TEXT_BODY, lineSpacingMultiple: 1.2 });
  const _d = s._slideObjects.length;
  const sc = dScale(1.5);
  const cy = 3.8, by = cy - sc.PH / 2;
  const colx = i => MAR_L + i * sc.HSTR;
  const user = pill(s, colx(0), by, 'User', sc, { icon: 'user', cat: 'user' });
  const lb = pill(s, colx(1), by, 'Load\nBalancer', sc, { icon: 'load-balancer' });
  const gw = pill(s, colx(2), by, 'Thinfinity\nGateway', sc, { icon: 'gateway', cat: 'thinfinity' });
  const bk = pill(s, colx(3), by, 'Thinfinity\nBroker', sc, { icon: 'broker', cat: 'thinfinity' });
  fwLine(s, (user.r + lb.x) / 2, 2.5, 5.1, 'Firewall');
  connect(s, user, 'r', lb, 'l', { sc });
  connect(s, lb, 'r', gw, 'l', { sc });
  connect(s, bk, 'l', gw, 'r', { sc });
  const pz = resourceZone(s, bk.r + sc.GAP, 2.55, sc, [
    { label: 'Windows 11', icon: 'windows' }, { label: 'Windows\nServer', icon: 'server' },
    { label: 'Windows 11', icon: 'windows' }, { label: 'Windows\nServer', icon: 'server' },
  ], 2, 'Subnet');
  agentBus(s, gw, pz, sc, 2.25);
  centerDiagram(s, _d, DREG);
  addFooter(s);
});

// 33 · Sitio Inicial 100-1000 — VDI resources + specs (incl FSLogix) (source p32)
SLIDE_BUILDERS.push(() => {
  const s = pres.addSlide();
  setMode(s);
  addTitleBar(s, 'Sitio Inicial: 100 - 1000 usuarios', { size: 24 });
  const _d = s._slideObjects.length;
  const sc = dScale(1.2);
  const core = haCore(s, MAR_L, 1.7, { sc, usersLabel: 'Users', db: 'SQL\nData Base', shortNodes: true });
  const pz = resourceZone(s, core.rightX + sc.GAP, 1.55, sc, [WSVDI, WSVDI, W10VDI, W10VDI, VAPP, VAPP], 2, null);
  agentBus(s, core.gwT, pz, sc, 1.4);
  fwLine(s, core.lb.x - sc.GAP / 2, 1.45, core.bottom + 0.2, 'WAF · Firewall');
  fwLine(s, core.bkT.r + sc.GAP / 2, 1.45, core.bottom + 0.2, 'Firewall');
  centerDiagram(s, _d, UREG);
  const spW = (CONTENT_W - 0.3) / 2;
  specsPanel(s, MAR_L, 4.5, spW, 2.2, [
    { c: 'Gateway', v: '2 × 4 vCPU · 16 GB RAM' },
    { c: 'Broker', v: '2 × 8 vCPU · 32 GB RAM' },
    { c: 'Base de Datos SQL', v: '4 vCPU · 8 GB RAM (considerar servicio SQL gestionado para escalado y alta disponibilidad)' },
  ]);
  specsPanel(s, MAR_L + spW + 0.3, 4.5, spW, 2.2, [
    { c: 'Servidor de Perfiles FSLogix', v: 'Aumentar la capacidad de almacenamiento y asegurar que el servidor de archivos cuente con al menos 4–6 vCPU y 16 GB de RAM para manejar el incremento en el I/O.' },
  ]);
  addFooter(s);
});

// 34 · Sitio Inicial 100-1000 con DR — VDI resources (source p33)
SLIDE_BUILDERS.push(() => {
  const s = pres.addSlide();
  setMode(s);
  addTitleBar(s, 'Sitio Inicial: 100 - 1000 usuarios con Recuperación ante Desastres', { size: 18 });
  s.addText('Agregamos un sitio de recuperación ante desastres añadiendo un gateway y un broker adicionales, junto con la sincronización de la base de datos SQL con el entorno principal y una URL de recuperación.',
    { x: MAR_L, y: 1.02, w: CONTENT_W, h: 0.45, fontFace: 'Inter', fontSize: 10, color: C.TEXT_BODY, lineSpacingMultiple: 1.15 });
  const _d = s._slideObjects.length;
  const sc = dScale(1.12);
  const core1 = haCore(s, MAR_L, 1.82, { sc, db: 'SQL\nData Base', shortNodes: true });
  const pz1 = resourceZone(s, core1.rightX + sc.GAP, 1.72, sc, [WSVDI, WSVDI, W10VDI, W10VDI, VAPP, VAPP], 3, 'Subnet');
  agentBus(s, core1.gwT, pz1, sc, 1.64);
  s.addShape('line', { x: MAR_L, y: 4.1, w: CONTENT_W, h: 0, line: { color: C.BORDER_LIGHT, width: 1, dashType: 'dash' } });
  const dr = drRow(s, MAR_L, 4.95, sc);
  const pz2 = resourceZone(s, core1.rightX + sc.GAP, 4.55, sc, [WSVDI, WSVDI, VAPP, VAPP], 2, 'Subnet');
  agentBus(s, dr.gw, pz2, sc, 4.45);
  arrow(s, core1.db.cx, core1.db.b, dr.db.cx, dr.db.y, { dash: 'dash', begin: 'triangle' });
  centerDiagram(s, _d, DREG);
  addFooter(s);
});

// 35 · 2 Sitios Activo-Activo — VDI resources (source p34)
SLIDE_BUILDERS.push(() => {
  const s = pres.addSlide();
  setMode(s);
  addTitleBar(s, '2 Sitios Activo-Activo (1000 a 5000 usuarios)', { size: 22 });
  s.addText('Los sitios pueden escalarse vertical y regionalmente añadiendo más gateways y brokers, así como más sitios.',
    { x: MAR_L, y: 1.08, w: CONTENT_W, h: 0.45, fontFace: 'Inter', fontSize: 10, color: C.TEXT_BODY });
  const _d = s._slideObjects.length;
  const sc = dScale(1.12);
  const vdi6 = [WSVDI, WSVDI, WSVDI, WSVDI, WSVDI, WSVDI];
  const c1 = haCore(s, MAR_L, 1.8, { sc, db: 'SQL\nData Base', shortNodes: true });
  const pz1 = resourceZone(s, c1.rightX + sc.GAP, 1.7, sc, vdi6, 3, 'Subnet');
  agentBus(s, c1.gwT, pz1, sc, 1.62);
  s.addText('Site 1', { x: MAR_L, y: 3.85, w: 1.5, h: 0.22, fontFace: 'Inter SemiBold', fontSize: 10, color: C.TEXT_SECONDARY });
  s.addShape('line', { x: MAR_L, y: 4.08, w: CONTENT_W, h: 0, line: { color: C.BORDER_LIGHT, width: 1, dashType: 'dash' } });
  s.addText('Site 2', { x: MAR_L, y: 4.12, w: 1.5, h: 0.22, fontFace: 'Inter SemiBold', fontSize: 10, color: C.TEXT_SECONDARY });
  const c2 = haCore(s, MAR_L, 4.55, { sc, db: 'SQL\nData Base', shortNodes: true });
  const pz2 = resourceZone(s, c2.rightX + sc.GAP, 4.45, sc, vdi6, 3, 'Subnet');
  agentBus(s, c2.gwT, pz2, sc, 4.3);
  centerDiagram(s, _d, DREG);
  addFooter(s);
});

// 36 · Section divider — Cronograma (navy)
SLIDE_BUILDERS.push(() => {
  sectionDivider(pres.addSlide(), 'SECCIÓN', 'Cronograma de implementación', '6 fases · de fundamentos a entrega operacional');
});

// Timeline phase card (mode-aware). fill = C.BRAND_BLUE (accent) or C.WHITE (base).
function timelinePhase(s, x, y, w, h, num, title, dur, activities, hito, fill) {
  const accent = fill === C.BRAND_BLUE;          // accent phase card
  const accDark = accent && TH.accentDark;       // accent fill dark → light text
  const lightTxt = TH.dark || accDark;
  const cardFill = accent ? TH.accentFill : TH.cardBase;
  const accentCol = TH.dark ? C.BLUE_LIGHT : C.BRAND_BLUE;
  const accLine = (accent && !TH.dark && TH.accentBorder) ? { color: TH.accentBorder, width: 1 } : undefined;
  card(s, x, y, w, h, { fill: cardFill, line: accLine });
  s.addText(`Fase ${num}`, { x: x + 0.25, y: y + 0.22, w: w - 0.5, h: 0.35, fontFace: 'Inter SemiBold', fontSize: 13, color: accDark ? C.WHITE : accentCol });
  s.addText(title, { x: x + 0.25, y: y + 0.58, w: w - 0.5, h: 0.7, fontFace: 'Inter SemiBold', fontSize: 15, color: lightTxt ? C.WHITE : C.NAVY, lineSpacingMultiple: 1.1 });
  s.addText(dur, { x: x + 0.25, y: y + 1.28, w: w - 0.5, h: 0.3, fontFace: 'Inter SemiBold', fontSize: 11, color: accDark ? C.TEXT_ON_NAVY : accentCol });
  s.addText('Actividades Clave', { x: x + 0.25, y: y + 1.7, w: w - 0.5, h: 0.3, fontFace: 'Inter SemiBold', fontSize: 10.5, color: lightTxt ? C.WHITE : C.TEXT_PRIMARY });
  let ay = y + 2.05;
  activities.forEach(act => {
    s.addText('➔', { x: x + 0.25, y: ay, w: 0.25, h: 0.3, fontFace: 'Inter SemiBold', fontSize: 9, color: accDark ? C.MINT : accentCol });
    s.addText(act, { x: x + 0.5, y: ay, w: w - 0.75, h: 0.5, fontFace: 'Inter', fontSize: 9.5, color: lightTxt ? C.TEXT_ON_NAVY : C.TEXT_BODY, lineSpacingMultiple: 1.15 });
    ay += 0.1 + Math.max(0.28, Math.ceil(act.length / 38) * 0.2);
  });
  const hitoY = y + h - 0.95;
  s.addShape('line', { x: x + 0.25, y: hitoY, w: w - 0.5, h: 0, line: { color: lightTxt ? '2A4060' : C.BORDER_LIGHT, width: 1 } });
  s.addText('Hito', { x: x + 0.25, y: hitoY + 0.06, w: 1, h: 0.25, fontFace: 'Inter SemiBold', fontSize: 10, color: C.MINT, charSpacing: 1 });
  s.addText(hito, { x: x + 0.25, y: hitoY + 0.32, w: w - 0.5, h: 0.55, fontFace: 'Inter', fontSize: 9.5, color: lightTxt ? C.WHITE : C.TEXT_PRIMARY, lineSpacingMultiple: 1.2 });
}

// 37 · Cronograma · Fases 1-3 — source p36 (verbatim)
SLIDE_BUILDERS.push(() => {
  const s = pres.addSlide();
  setMode(s);
  addTitleBar(s, 'Cronograma');
  const cardW = (CONTENT_W - 0.4) / 3, cardH = 5.2, startY = 1.4, gap = 0.2;
  timelinePhase(s, MAR_L, startY, cardW, cardH, 1, 'Fundamentos y Planeación', 'Duración: 1–2 semanas',
    ['Revisión de la propuesta comercial y validación de precios.', 'Inicio del proyecto y descubrimiento técnico.', 'Finalización del diseño de bajo nivel (LLD).', 'Confirmación de casos de uso y alcance.'],
    'Alcance comercial y técnico validado.', C.BRAND_BLUE);
  timelinePhase(s, MAR_L + cardW + gap, startY, cardW, cardH, 2, 'Validación Técnica (POC)', 'Duración: 2 semanas',
    ['Thinfinity desplegado en entorno de pruebas.', 'Validación de casos de uso principales: escritorios basados en sesión, publicación de aplicaciones, integración con identidad, USB / impresión / multimedia.', 'Pruebas de rendimiento, experiencia del usuario y seguridad.'],
    'Aceptación técnica de la POC.', C.WHITE);
  timelinePhase(s, MAR_L + 2 * (cardW + gap), startY, cardW, cardH, 3, 'Adquisición y Licenciamiento', 'Duración: 1 semana',
    ['Confirmación comercial final (SKUs, modelo de licenciamiento, plazo).', 'Selección del modo de licenciamiento: Oracle Cloud Marketplace (créditos OCI u oferta privada) o compra directa a Cybele Software.', 'Activación de licencias de producción.', 'Distribución de claves o asignación en Marketplace.'],
    'Licencias aprovisionadas y listas para activación.', C.BRAND_BLUE);
  addFooter(s);
});

// 38 · Cronograma · Fases 4-6 — source p37 (verbatim)
SLIDE_BUILDERS.push(() => {
  const s = pres.addSlide();
  setMode(s);
  addTitleBar(s, 'Cronograma');
  const cardW = (CONTENT_W - 0.4) / 3, cardH = 5.2, startY = 1.4, gap = 0.2;
  timelinePhase(s, MAR_L, startY, cardW, cardH, 4, 'Despliegue y Configuración', 'Duración: 2 semanas',
    ['Despliegue en producción de Thinfinity Gateway, Broker y VDI Manager.', 'Creación de imágenes base e integración del stack de aplicaciones.', 'Configuración del proveedor de identidad y políticas RBAC.', 'Preparación de dispositivos (thin clients, perfiles BYOD, clientes web).'],
    'Entorno de producción listo para puesta en marcha.', C.WHITE);
  timelinePhase(s, MAR_L + cardW + gap, startY, cardW, cardH, 5, 'Puesta en marcha y despliegue', 'Duración: 1 semana',
    ['Migración de usuarios (por fases o de golpe).', 'Pruebas finales de acceso, verificación de permisos.', 'Capacitación y habilitación de usuarios finales, soporte en el primer inicio de sesión.'],
    'Todos los usuarios operativos en la plataforma Thinfinity.', C.BRAND_BLUE);
  timelinePhase(s, MAR_L + 2 * (cardW + gap), startY, cardW, cardH, 6, 'Soporte intensivo, optimización y entrega', 'Duración: 6 semanas',
    ['Semanas 1–2: Soporte intensivo (SLA prioritarios, manejo de incidencias).', 'Semanas 3–4: Monitoreo de rendimiento, refinamiento de políticas, análisis.', 'Semanas 5–6: Transferencia de conocimiento, runbooks, documentación final.'],
    'Cierre del proyecto y transición de propiedad operacional.', C.WHITE);
  addFooter(s);
});

// 39 · Q&A divider (navy)
SLIDE_BUILDERS.push(() => {
  const s = pres.addSlide();
  setBg(s, C.NAVY);
  s.addText('Q&A', { x: 0, y: 2.6, w: W, h: 2, fontFace: 'Inter SemiBold', fontSize: 120, color: C.WHITE, align: 'center' });
});

// 40 · Closing — placeholder; replaced post-build by swap_closing_slide.py with cierre.pptx
SLIDE_BUILDERS.push(() => {
  const s = pres.addSlide();
  setBg(s, C.NAVY);
});

// ─── Build orchestration ───
TOTAL_SLIDES = SLIDE_BUILDERS.length;
SLIDE_BUILDERS.forEach((builder) => { SLIDE_INDEX++; builder(); });

const outPath = './output/Enterprise_VDI_OCI_Discovery_Demo_ESP.pptx';
const fs = require('fs');
if (!fs.existsSync('./output')) fs.mkdirSync('./output');
pres.writeFile({ fileName: outPath })
  .then(p => console.log(`OK · written ${p} · ${TOTAL_SLIDES} slides`))
  .catch(e => console.error(`ERR ${e}`));
