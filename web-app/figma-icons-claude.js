// Plan B for the icon sync: no Figma token. Claude reads the Figma file through its own Figma
// connection (use_figma) and uses this helper to compare and write, so only what changed travels.
// The recipe (and the use_figma snippets that go with it) is in RUNBOOK.md, "Icon library from Figma".
//
//   node figma-icons-claude.js digest               per-category fingerprints of data/icons-figma/
//   node figma-icons-claude.js diff <group> <list>  <list> = "name:hash,name:hash" from Figma for
//                                                   one category -> new / changed / removed names
//   node figma-icons-claude.js write <file.json>    { icons: [{name, group, variant, svg}], remove: [names] }
//                                                   writes the SVGs and updates _manifest.json
//   node figma-icons-claude.js checked              a check found nothing new: stamp the date anyway,
//                                                   so the library's "last updated" stays truthful
//
// Fingerprint = FNV-1a over the SVG text exactly as Figma's exportAsync('SVG_STRING') returns it.
// It is stored per icon in _manifest.json ("fp") rather than recomputed from the files: the REST
// export (sync-figma-icons.js) rounds some coordinates differently, so its files would never match.
// An icon without "fp" (e.g. after a REST sync) always shows as changed.
const fs = require('fs');
const path = require('path');

const DIR = path.join(__dirname, 'data', 'icons-figma');
const MANIFEST = path.join(DIR, '_manifest.json');

const fnv = s => { let h = 0x811c9dc5; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return (h >>> 0).toString(36); };
const digestOf = pairs => fnv(pairs.slice().sort().join(','));

function manifest() {
  try { return JSON.parse(fs.readFileSync(MANIFEST, 'utf8')); } catch (e) { return { icons: [] }; }
}
function localPairs(group) {
  return manifest().icons.filter(ic => ic.group === group).map(ic => ic.name + ':' + (ic.fp || '?'));
}

const [cmd, a, b] = process.argv.slice(2);
if (cmd === 'digest') {
  const groups = [...new Set(manifest().icons.map(ic => ic.group))];
  console.log(groups.map(g => `${g}=${digestOf(localPairs(g))}`).join('\n'));
} else if (cmd === 'diff') {
  const local = new Map(localPairs(a).map(p => p.split(/:(?=[^:]*$)/)));
  const remote = new Map((b || '').split(',').filter(Boolean).map(p => p.split(/:(?=[^:]*$)/)));
  const added = [...remote.keys()].filter(n => !local.has(n));
  const changed = [...remote.keys()].filter(n => local.has(n) && local.get(n) !== remote.get(n));
  const removed = [...local.keys()].filter(n => !remote.has(n));
  console.log(JSON.stringify({ group: a, added, changed, removed }));
} else if (cmd === 'write') {
  const batch = JSON.parse(fs.readFileSync(a, 'utf8'));
  const m = manifest();
  const byName = new Map(m.icons.map(ic => [ic.name, ic]));
  fs.mkdirSync(DIR, { recursive: true });
  for (const ic of batch.icons || []) {
    fs.writeFileSync(path.join(DIR, ic.name + '.svg'), ic.svg);
    byName.set(ic.name, { name: ic.name, group: ic.group, variant: ic.variant || null, fp: fnv(ic.svg) });
  }
  for (const name of batch.remove || []) {
    fs.rmSync(path.join(DIR, name + '.svg'), { force: true });
    byName.delete(name);
  }
  m.icons = [...byName.values()];
  m.syncedAt = new Date().toISOString();
  m.syncedBy = 'claude (use_figma)';
  fs.writeFileSync(MANIFEST, JSON.stringify(m, null, 2));
  console.log(JSON.stringify({ written: (batch.icons || []).length, removed: (batch.remove || []).length, total: m.icons.length }));
} else if (cmd === 'checked') {
  const m = manifest();
  m.syncedAt = new Date().toISOString();
  m.syncedBy = 'claude (use_figma)';
  fs.writeFileSync(MANIFEST, JSON.stringify(m, null, 2));
  console.log(JSON.stringify({ syncedAt: m.syncedAt }));
} else {
  console.error('usage: digest | diff <group> <name:hash,...> | write <file.json> | checked');
  process.exit(1);
}
