#!/usr/bin/env node
// Guard for the console's icons: every icon in the UI must come from the brandbook icon library
// (brand-icon-lib.js) — never an emoji, never a hand-drawn SVG. Run it after any change to index.html:
//
//   node check-ui-icons.js          (or: npm run check:icons)
//
// It fails (exit 1) when index.html has:
//   * an emoji used as an icon (paperclip, wastebasket),
//   * a hand-drawn <svg> (one with its own <path>/<circle>/<rect>/...) that is not marked as an exception,
//   * an icon constant that is not built from BRAND_ICON_LIB, or an icon name the library does not have.
// A drawing may stay only when the brandbook has no such icon: put `brandbook-exception: <why>` on the
// same line or the line above, and tell Nick.
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const html = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf8').replace(/\r\n/g, '\n');
const lines = html.split('\n');
const sandbox = { window: {} };
vm.runInNewContext(fs.readFileSync(path.join(__dirname, 'brand-icon-lib.js'), 'utf8'), sandbox);
const LIB = sandbox.window.BRAND_ICON_LIB;
const isComment = l => /^\s*(\/\/|\/\*|\*|<!--)/.test(l);
const code = lines.map(l => (isComment(l) ? '' : l)).join('\n');   // comments may mention <svg> and the old drawings
const lineOf = idx => code.slice(0, idx).split('\n').length;
const fails = [];

// 1) emoji icons
const EMOJI = [[/\u{1F4CE}|\u{1F587}/u, 'paperclip emoji — use the library icon "attach"'],
               [/\u{1F5D1}/u, 'wastebasket emoji — use the library icon "trash"']];
lines.forEach((l, i) => { if (!isComment(l)) for (const [re, why] of EMOJI) if (re.test(l)) fails.push(`index.html:${i + 1}  ${why}`); });

// 2) hand-drawn <svg>
const DRAWING = /<(path|circle|rect|line|polyline|polygon|ellipse)\b/;
for (const m of code.matchAll(/<svg(?=[\s>])[^<>]*>(?:(?!<svg)[\s\S])*?<\/svg>/g)) {   // real tags only, not the '<svg' text in strings
  if (!DRAWING.test(m[0])) continue;
  const n = lineOf(m.index);
  if (/brandbook-exception/.test(lines[n - 1] + (lines[n - 2] || ''))) continue;
  fails.push(`index.html:${n}  hand-drawn <svg> — use a brandbook icon: <svg data-icon="name"></svg> in HTML, brandSvg('name') or BRAND_ICON_LIB.name in JS`);
}

// 3) icon constants and names
const CONST = { ICO_CLIP: 'attach', ICO_TRASH: 'trash', TRASH_ICON: 'trash', ICO_DOWNLOAD: 'download', ICO_PENCIL: 'edit',
  EDIT_ICON: 'edit', ICO_EYE: 'eye', ICO_FILE: 'file', ICO_REFRESH: 'refresh', ICO_COMMENT: 'chat', ICO_CHECK: 'check',
  ICO_LINK: 'link', ICO_ALERT: 'alert-s', ICO_CHEV_DOWN: 'a-down', ALL_ICON: 'grid', ICO_PLAY: 'play',
  PIN_SVG: 'pin', STAR_SVG: 'star', GRID_SVG: 'grid', LIST_SVG: 'list' };
for (const [name, icon] of Object.entries(CONST)) {
  const def = lines.find(l => l.startsWith('const ' + name + ' ='));
  if (!def) fails.push(`${name} is not defined in index.html`);
  else if (!new RegExp("BRAND_ICON_LIB(\\." + icon.replace('-', '\\-') + "\\b|\\['" + icon + "'\\])").test(def)) fails.push(`${name} must be built from the library icon "${icon}"`);
}
const wanted = new Set([...Object.values(CONST),
  ...[...code.matchAll(/data-icon="([^"]+)"/g)].map(m => m[1]),
  ...[...code.matchAll(/brandSvg\('([^']+)'/g)].map(m => m[1])]);
for (const icon of wanted) if (!LIB[icon]) fails.push(`the library has no icon "${icon}"`);

if (fails.length) {
  console.error('ICON CHECK FAILED:');
  fails.forEach(f => console.error('  ' + f));
  process.exit(1);
}
const exceptions = lines.map((l, i) => [l, i + 1]).filter(([l]) => /brandbook-exception/.test(l)).map(([l, n]) => `  index.html:${n}  ${l.split('brandbook-exception:')[1].trim()}`);
console.log(`Icon check OK — ${wanted.size} brandbook icons in use, none hand-drawn.`);
if (exceptions.length) console.log('Declared exceptions (not in the brandbook):\n' + exceptions.join('\n'));
