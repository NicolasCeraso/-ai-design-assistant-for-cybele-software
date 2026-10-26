// Builds a browsable icon library from the icons synced from Figma plus the official Cybele/Thinfinity SVG set.
// Output: brand-icon-lib.js  ->  window.BRAND_ICON_LIB = { name: '<svg…>' }
const fs = require('fs');
const path = require('path');

const os = require('os');

// The official Cybele/Thinfinity SVG set. Resolved in order so this runs on any machine: the copy
// vendored in this repo, an explicit override, then the installed skill folder.
function iconsDir() {
  const tried = [
    path.join(__dirname, '..', 'skills', 'thinfinity-architecture', 'icons'),
    globalThis.process.env.CYBELE_ICONS_DIR,   // `process` is a local helper here
    path.join(os.homedir(), '.claude', 'skills', 'thinfinity-architecture', 'icons'),
  ].filter(Boolean);
  for (const d of tried) { if (fs.existsSync(d)) return d; }
  console.error('Icon set not found. Tried:');
  tried.forEach(d => console.error('  ' + d));
  console.error('Set CYBELE_ICONS_DIR to the folder holding the Thinfinity icon SVGs.');
  globalThis.process.exit(1);
}

const SRC = iconsDir();

function process(svg) {
  return svg
    .replace(/^﻿/, '').trim()
    .replace(/preserveAspectRatio="none"/g, 'preserveAspectRatio="xMidYMid meet"')
    .replace(/var\(--fill-\d+,\s*#[0-9A-Fa-f]{3,8}\)/g, 'currentColor')
    .replace(/fill="#[0-9A-Fa-f]{3,8}"/g, 'fill="currentColor"')
    .replace(/fill="black"/g, 'fill="currentColor"')
    .replace(/stroke="#[0-9A-Fa-f]{3,8}"/g, 'stroke="currentColor"');
}

// Figma exports: size to the container like the source set, and give every id a per-icon prefix —
// all icons are inlined on one page, so two icons' "clip0_1_2" would clip each other.
function fromFigma(svg, name) {
  const pre = 'i-' + name.replace(/[^\w-]/g, '_') + '-';
  return process(svg)
    .replace(/^<svg([^>]*?)\swidth="[^"]*"/, '<svg$1 width="100%"')
    .replace(/^<svg([^>]*?)\sheight="[^"]*"/, '<svg$1 height="100%"')
    .replace(/\bid="([^"]+)"/g, (m, id) => `id="${pre}${id}"`)
    .replace(/url\(#([^)]+)\)/g, (m, id) => `url(#${pre}${id})`)
    .replace(/(xlink:)?href="#([^"]+)"/g, (m, x, id) => `${x || ''}href="#${pre}${id}"`);
}

// Figma (data/icons-figma/, filled by sync-figma-icons.js) is the source of truth. Icons that exist
// only in the older source set are kept on top of it and listed in BRAND_ICON_LEGACY.
const FIGMA = path.join(__dirname, 'data', 'icons-figma');
// Icons marked in Figma as retired ("absolute-touch ⚠️ no se usa") stay in the synced folder, so
// fingerprints keep matching Figma, but never reach the library (Nick, 2026-09-28).
const RETIRED = /no[-\s_]*se[-\s_]*usa/i;
const out = {};
const legacy = [];
const retired = [];
let skipped = 0;
if (fs.existsSync(FIGMA)) {
  for (const file of fs.readdirSync(FIGMA)) {
    if (!file.endsWith('.svg')) continue;
    const raw = fs.readFileSync(path.join(FIGMA, file), 'utf8');
    if (!raw.trim()) { skipped++; continue; }
    const name = file.replace(/\.svg$/, '');
    if (RETIRED.test(name)) { retired.push(name); continue; }
    out[name] = fromFigma(raw.replace(/^﻿/, '').trim(), name);
  }
}
const fromFigmaCount = Object.keys(out).length;
// Icons drawn for the console in the brand's light style where the Figma set has none
// (data/icons-custom/, e.g. "attach", 2026-09-28). A Figma icon with the same name always wins.
const CUSTOM = path.join(__dirname, 'data', 'icons-custom');
const custom = [];
if (fs.existsSync(CUSTOM)) {
  for (const file of fs.readdirSync(CUSTOM)) {
    if (!file.endsWith('.svg')) continue;
    const name = file.replace(/\.svg$/, '');
    if (out[name]) continue;
    out[name] = fromFigma(fs.readFileSync(path.join(CUSTOM, file), 'utf8').replace(/^﻿/, '').trim(), name);
    custom.push(name);
  }
}
for (const file of fs.readdirSync(SRC)) {
  if (!file.endsWith('.svg')) continue;
  if (file === '_arrow.svg') continue;
  const name = file.replace(/\.svg$/, '');
  if (out[name]) continue;
  const raw = fs.readFileSync(path.join(SRC, file), 'utf8');
  if (!raw.trim()) { skipped++; continue; }
  out[name] = process(raw);
  if (fromFigmaCount) legacy.push(name);
}

// When the Figma set was last brought up to date (by a download, or a check that found nothing new).
let manifest = {};
try { manifest = JSON.parse(fs.readFileSync(path.join(FIGMA, '_manifest.json'), 'utf8')); } catch (e) {}
const syncedAt = manifest.syncedAt || null;

// Categories: the console's own (data/icon-categories.json — Figma is not changed), falling back to
// the Figma categories when that file is absent. Each A–Z; the legacy icons close the list as their
// own group, keyed null (the page labels it "not in Figma").
let cats = null;
try { cats = JSON.parse(fs.readFileSync(path.join(__dirname, 'data', 'icon-categories.json'), 'utf8')).categories; } catch (e) {}
const byIcon = new Map(), byFigma = new Map();
for (const c of cats || []) {
  (c.icons || []).forEach(n => byIcon.set(n, c.name));
  (c.figmaGroups || []).forEach(g => byFigma.set(g, c.name));
}
const groups = new Map((cats || []).map(c => [c.name, []]));
const uncategorized = [];
for (const ic of manifest.icons || []) {
  if (!out[ic.name]) continue;
  let g = ic.group || 'other';
  if (cats) {
    g = byIcon.get(ic.name) || byFigma.get(ic.group);
    if (!g) { g = 'Otros'; uncategorized.push(ic.name); }
  }
  if (!groups.has(g)) groups.set(g, []);
  groups.get(g).push(ic.name);
}
// custom icons go to the category that lists them by name in icon-categories.json
for (const name of custom) {
  const g = byIcon.get(name) || 'Otros';
  if (g === 'Otros') uncategorized.push(name);
  if (!groups.has(g)) groups.set(g, []);
  groups.get(g).push(name);
}
for (const [g, names] of groups) if (!names.length) groups.delete(g);
const sortAZ = a => a.sort((x, y) => x.localeCompare(y, 'en', { sensitivity: 'base' }));
const grouped = [...groups].map(([g, names]) => [g, sortAZ(names)]);
if (legacy.length) grouped.push([null, sortAZ(legacy.slice())]);

// Search keywords (Spanish + English) from data/icon-keywords.json, for the icons in the library.
let kwFile = {};
try { kwFile = JSON.parse(fs.readFileSync(path.join(__dirname, 'data', 'icon-keywords.json'), 'utf8')); } catch (e) {}
const keywords = {};
for (const n of Object.keys(out)) if (typeof kwFile[n] === 'string') keywords[n] = kwFile[n];
const noKeywords = Object.keys(out).filter(n => !keywords[n]);

const js = '// Auto-generated by build-icon-lib.js — do not edit by hand\nwindow.BRAND_ICON_LIB = ' + JSON.stringify(out) + ';\n'
  + 'window.BRAND_ICON_LEGACY = ' + JSON.stringify(legacy) + ';\n'
  + 'window.BRAND_ICON_CUSTOM = ' + JSON.stringify(custom) + ';\n'
  + 'window.BRAND_ICON_SYNCED_AT = ' + JSON.stringify(syncedAt) + ';\n'
  + 'window.BRAND_ICON_GROUPS = ' + JSON.stringify(grouped) + ';\n'
  + 'window.BRAND_ICON_KEYWORDS = ' + JSON.stringify(keywords) + ';\n';
fs.writeFileSync(path.join(__dirname, 'brand-icon-lib.js'), js);
console.log(JSON.stringify({ count: Object.keys(out).length, figma: fromFigmaCount, legacy: legacy.length, skipped, bytes: js.length, uncategorized, retired, noKeywords }));
