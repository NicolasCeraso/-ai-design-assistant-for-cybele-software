#!/usr/bin/env node
// verbatim_check.js — enforces the LinkedIn-carousel verbatim contract (SPEC §1b / §3.7).
//
//   node verbatim_check.js <script.txt> <output-dir> [--json]
//
// Extracts every <text>/<tspan> string from <output-dir>/*_placa*.svg and reports:
//   1. words rendered on a placa that do not appear in the script's PLACA blocks
//   2. figures (numbers/percentages) printed more than once on the same placa
// Exit 0 = clean, 1 = violations, 2 = usage/IO error.
//
// The CAPTION block is deliberately EXCLUDED from the allowed vocabulary: mining it is a
// violation, so words that live only there must be reported.

const fs = require('fs'), path = require('path');

const [, , scriptPath, outDir, ...rest] = process.argv;
const asJson = rest.includes('--json');
if (!scriptPath || !outDir) {
  console.error('usage: node verbatim_check.js <script.txt> <output-dir> [--json]');
  process.exit(2);
}

// ---------- brand chrome that is exempt (§3.7) ----------
const EXEMPT = new Set(['cybele', 'blogs', 'thinfinity', 'by', 'software']);

// ---------- normalisation ----------
// Fold typographic punctuation, strip anything that is not a letter/digit/%/. , lowercase.
const fold = s => s
  .replace(/[‘’ʼ]/g, "'")
  .replace(/[“”]/g, '"')
  .replace(/[–—]/g, '-')
  .replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
  .replace(/&#(\d+);/g, (_, d) => String.fromCharCode(+d))
  .replace(/&[a-zA-Z]+;/g, ' ')
  .toLowerCase();

// A "word" keeps internal ' - . % so that 7x, 22%, 3389, can't, remote-access, 7.6.3 survive intact.
const tokenize = s => (fold(s).match(/[a-z0-9][a-z0-9'’.\-%#$]*/g) || [])
  .map(w => w.replace(/^[.'-]+|[.'-]+$/g, ''))
  .filter(Boolean);

// ---------- read the script ----------
let raw;
try { raw = fs.readFileSync(scriptPath, 'utf8'); }
catch (e) { console.error('cannot read script: ' + e.message); process.exit(2); }

// Allowed vocabulary = the PLACA blocks only (everything from the first PLACA marker,
// minus a trailing CAPTION if the file is ordered oddly).
const placaBlocks = [];
{
  const re = /^\s*PLACA\s+(\d+)\b[ \t:.\-]*([\s\S]*?)(?=^\s*PLACA\s+\d+\b|^\s*LOGO\b|^\s*CAPTION\b|\s*$(?![\s\S]))/gim;
  let m;
  while ((m = re.exec(raw)) !== null) placaBlocks.push({ n: +m[1], text: m[2] });
}
if (!placaBlocks.length) {
  console.error('no "PLACA n" blocks found in ' + scriptPath + ' — cannot audit. '
    + 'If the input was raw article text, the verbatim contract cannot be checked automatically.');
  process.exit(2);
}
// Trailing lines after the last PLACA that belong to the CTA (e.g. "Read the breakdown at ...")
const tail = raw.split(/^\s*PLACA\s+\d+\b/im).pop().split(/^\s*LOGO\b/im).slice(1).join(' ');
const allowed = new Set([...tokenize(placaBlocks.map(b => b.text).join(' ')), ...tokenize(tail), ...EXEMPT]);

// The URL, when present, is exempt in whole.
for (const u of raw.match(/https?:\/\/\S+|[a-z0-9.-]+\.(?:com|net|org)(?:\/\S*)?/gi) || [])
  tokenize(u).forEach(t => allowed.add(t));

// ---------- read the placas ----------
let files;
try {
  files = fs.readdirSync(outDir).filter(f => /_placa\d+\.svg$/i.test(f)).sort();
} catch (e) { console.error('cannot read output dir: ' + e.message); process.exit(2); }
if (!files.length) { console.error('no *_placa<NN>.svg found in ' + outDir); process.exit(2); }

const strip = s => s.replace(/<defs[\s\S]*?<\/defs>/gi, '');
function placaStrings(svg) {
  const out = [];
  for (const m of strip(svg).matchAll(/<text\b[^>]*>([\s\S]*?)<\/text>/gi)) {
    const inner = m[1];
    if (/<tspan/i.test(inner)) {
      for (const t of inner.matchAll(/<tspan\b[^>]*>([\s\S]*?)<\/tspan>/gi)) {
        const v = t[1].replace(/<[^>]*>/g, '').trim(); if (v) out.push(v);
      }
    } else {
      const v = inner.replace(/<[^>]*>/g, '').trim(); if (v) out.push(v);
    }
  }
  return out;
}

const FIG = /^[$]?\d[\d.,]*[%x]?$/;   // 22%, 7x, 3.65, $349, 3389

// Both tiers are failures under the strict contract (§1b), but they need different fixes:
//   INVENTED — the word exists nowhere in the script. Delete it or redesign.
//   ALTERED  — a script word exists but in another form ("devices" -> "device",
//              "Verizon's" -> "Verizon"). Restore the script's exact form.
// A single stem is not enough: stripping "es" turns "devices" into "devic", which never
// matches "device". Index every plausible reduction of each word and match on intersection.
const variants = w => {
  const v = new Set([w]);
  v.add(w.replace(/'s$/, ''));
  if (/s$/.test(w)) v.add(w.replace(/s$/, ''));
  if (/es$/.test(w)) v.add(w.replace(/es$/, ''));
  if (/ies$/.test(w)) v.add(w.replace(/ies$/, 'y'));
  v.delete('');
  return v;
};
const stems = new Map();                       // reduction -> the script word that produced it
for (const a of allowed) for (const k of variants(a)) if (!stems.has(k)) stems.set(k, a);
const nearMatch = w => { for (const k of variants(w)) { const hit = stems.get(k); if (hit && hit !== w) return hit; } return null; };

const report = [];
for (const f of files) {
  const strings = placaStrings(fs.readFileSync(path.join(outDir, f), 'utf8'));
  const invented = new Map(), altered = new Map(), figs = new Map();

  for (const s of strings) {
    for (const w of tokenize(s)) {
      if (!allowed.has(w)) {
        const near = nearMatch(w);
        const bucket = near ? altered : invented;
        if (!bucket.has(w)) bucket.set(w, { seenIn: new Set(), near });
        bucket.get(w).seenIn.add(s);
      }
      if (FIG.test(w)) figs.set(w, (figs.get(w) || 0) + 1);
    }
  }
  const dupes = [...figs.entries()].filter(([, c]) => c > 1);
  const pack = m => [...m].map(([w, v]) => ({ word: w, near: v.near, seenIn: [...v.seenIn] }));
  report.push({ file: f, strings: strings.length, invented: pack(invented), altered: pack(altered), dupes });
}

const sum = k => report.reduce((a, r) => a + r[k].length, 0);
const totalInvented = sum('invented'), totalAltered = sum('altered');
const totalUnmatched = totalInvented + totalAltered;
const totalDupes = sum('dupes');

if (asJson) {
  console.log(JSON.stringify({ ok: !totalUnmatched && !totalDupes, totalInvented, totalAltered, totalDupes, report }, null, 2));
} else {
  console.log('VERBATIM AUDIT — ' + path.basename(outDir));
  console.log('script: ' + scriptPath + '  (' + placaBlocks.length + ' bloques PLACA, '
    + allowed.size + ' tokens permitidos)\n');
  for (const r of report) {
    const bad = r.invented.length + r.altered.length + r.dupes.length;
    console.log((bad ? 'x ' : 'v ') + r.file.padEnd(52) + String(r.strings).padStart(3) + ' strings'
      + (bad ? '  -> ' + r.invented.length + ' inventada(s), ' + r.altered.length + ' alterada(s), ' + r.dupes.length + ' cifra(s) repetida(s)' : '  ok'));
    for (const u of r.invented)
      console.log('      INVENTADA  "' + u.word + '"   en: ' + u.seenIn.slice(0, 2).map(s => JSON.stringify(s)).join(', '));
    for (const u of r.altered)
      console.log('      ALTERADA   "' + u.word + '"  <- el script dice "' + u.near + '"   en: ' + u.seenIn.slice(0, 2).map(s => JSON.stringify(s)).join(', '));
    for (const [w, c] of r.dupes)
      console.log('      REPETIDA   "' + w + '" x' + c + ' en la misma placa');
  }
  console.log();
  if (totalUnmatched || totalDupes) {
    console.log('FALLA — no entregar.');
    console.log('  ' + totalInvented + ' palabra(s) inventada(s)  -> borrarlas o rediseñar el elemento que las pide');
    console.log('  ' + totalAltered + ' palabra(s) alterada(s)   -> restaurar la forma exacta del script');
    console.log('  ' + totalDupes + ' cifra(s) repetida(s)     -> una cifra, una vez por placa');
  } else {
    console.log('OK: todo el texto renderizado proviene del script.');
  }
}
process.exit(totalUnmatched || totalDupes ? 1 : 0);
