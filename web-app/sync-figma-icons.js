// Downloads the icon set from the Cybele Design System file in Figma (the "Cyb Font" frame) into
// data/icons-figma/, one SVG per icon. build-icon-lib.js then turns that folder into brand-icon-lib.js.
//
// One variant per icon: "light", or — when an icon has no light variant — the closest one that
// exists (see VARIANT_ORDER). Nick's choice, 2026-09-28.
//
// Needs a Figma personal access token (read access to file content), taken from, in order:
// the FIGMA_TOKEN environment variable, or data/figma-token.txt (gitignored, one line).
// Which file/frame to read lives in data/icon-source.json, so it can move without touching code.
const fs = require('fs');
const path = require('path');

const DATA = path.join(__dirname, 'data');
const OUT = path.join(DATA, 'icons-figma');
const SOURCE = Object.assign(
  { fileKey: 'x0HMD1pXkcYdFM7NSaBvb4', nodeId: '8120:7263' },
  readJson(path.join(DATA, 'icon-source.json')) || {}
);
const VARIANT_ORDER = ['light', 'bold', 'filled-light', 'filled-bold', 'extra-bold'];
const SKIP_GROUPS = new Set(['Frame 26']);   // the page title block, not an icon category

function readJson(p) { try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch (e) { return null; } }

function token() {
  if (process.env.FIGMA_TOKEN) return process.env.FIGMA_TOKEN.trim();
  try { const t = fs.readFileSync(path.join(DATA, 'figma-token.txt'), 'utf8').trim(); if (t) return t; } catch (e) {}
  fail('No Figma token. Save your Figma personal access token in web-app/data/figma-token.txt');
}

function fail(msg) { console.error(msg); process.exit(1); }

async function api(url, tok) {
  for (let attempt = 0; attempt < 4; attempt++) {
    const r = await fetch(url, { headers: { 'X-Figma-Token': tok } });
    if (r.status === 429) { await new Promise(res => setTimeout(res, 2000 * (attempt + 1))); continue; }
    if (r.status === 403) fail('Figma rejected the token (403). Check that it is valid and can read file content.');
    if (!r.ok) fail(`Figma API ${r.status}: ${(await r.text()).slice(0, 150)}`);
    return r.json();
  }
  fail('Figma API is rate-limiting; try again in a minute.');
}

// "Property 1=light" -> "light"; anything else -> null
const variantOf = name => { const m = /^Property 1=(.+)$/.exec(name.trim()); return m ? m[1].trim() : null; };
const safeName = n => n.trim().replace(/[\\/:*?"<>|\s]+/g, '-');

// Walk the frame: every node whose children are variant components is one icon.
function collectIcons(root) {
  const icons = [];
  const walk = (node, group) => {
    const kids = node.children || [];
    const variants = kids.filter(k => (k.type === 'COMPONENT' || k.type === 'INSTANCE') && variantOf(k.name));
    if (variants.length) {
      const pick = VARIANT_ORDER.map(v => variants.find(k => variantOf(k.name) === v)).find(Boolean) || variants[0];
      icons.push({ name: safeName(node.name), group, variant: variantOf(pick.name), id: pick.id });
      return;
    }
    // A standalone component named after the icon itself.
    if (node.type === 'COMPONENT' && !variantOf(node.name)) {
      icons.push({ name: safeName(node.name), group, variant: null, id: node.id });
      return;
    }
    kids.forEach(k => walk(k, group));
  };
  (root.children || []).forEach(g => { if (!SKIP_GROUPS.has(g.name)) walk(g, g.name); });
  return icons;
}

async function pool(items, n, fn) {
  let i = 0;
  await Promise.all(Array.from({ length: n }, async () => { while (i < items.length) { const it = items[i++]; await fn(it); } }));
}

(async () => {
  const tok = token();
  const { fileKey, nodeId } = SOURCE;
  const file = await api(`https://api.figma.com/v1/files/${fileKey}/nodes?ids=${encodeURIComponent(nodeId)}`, tok);
  const root = file.nodes && file.nodes[nodeId] && file.nodes[nodeId].document;
  if (!root) fail(`Frame ${nodeId} not found in Figma file ${fileKey}.`);

  const all = collectIcons(root);
  const seen = new Set(), icons = [], dupes = [];
  for (const ic of all) { if (seen.has(ic.name)) { dupes.push(ic.name); continue; } seen.add(ic.name); icons.push(ic); }
  if (!icons.length) fail('No icons found in the Figma frame.');

  // Ask Figma to render SVGs in batches, then download each one.
  const urls = {};
  for (let i = 0; i < icons.length; i += 100) {
    const ids = icons.slice(i, i + 100).map(ic => ic.id).join(',');
    const r = await api(`https://api.figma.com/v1/images/${fileKey}?ids=${encodeURIComponent(ids)}&format=svg&svg_include_id=false`, tok);
    Object.assign(urls, r.images || {});
  }
  const svgs = {}, failed = [];
  await pool(icons, 12, async ic => {
    const u = urls[ic.id];
    if (!u) { failed.push(ic.name); return; }
    try { const r = await fetch(u); if (!r.ok) throw 0; svgs[ic.name] = await r.text(); } catch (e) { failed.push(ic.name); }
  });
  if (Object.keys(svgs).length < icons.length * 0.9) fail(`Only ${Object.keys(svgs).length} of ${icons.length} icons downloaded; kept the previous set.`);

  // Replace the folder only once everything is in hand, so a failed sync never leaves it half-empty.
  fs.rmSync(OUT, { recursive: true, force: true });
  fs.mkdirSync(OUT, { recursive: true });
  for (const [name, svg] of Object.entries(svgs)) fs.writeFileSync(path.join(OUT, name + '.svg'), svg);
  const manifest = {
    source: `https://www.figma.com/design/${fileKey}/?node-id=${nodeId.replace(':', '-')}`,
    syncedAt: new Date().toISOString(),
    icons: icons.filter(ic => svgs[ic.name]).map(({ name, group, variant }) => ({ name, group, variant })),
  };
  fs.writeFileSync(path.join(OUT, '_manifest.json'), JSON.stringify(manifest, null, 2));
  const notLight = manifest.icons.filter(ic => ic.variant && ic.variant !== 'light').length;
  console.log(JSON.stringify({ figma: manifest.icons.length, notLight, duplicates: dupes, failed }));
})().catch(e => fail(e.message));
