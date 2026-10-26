const http = require('http');
const fs = require('fs');
const path = require('path');
const { exec, spawn, spawnSync } = require('child_process');

const MIME_TYPES = {
  '.html': 'text/html',
  '.css': 'text/css',
  '.js': 'application/javascript',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.json': 'application/json',
  '.pdf': 'application/pdf',
};

const BASE = __dirname; // portable: serve from wherever this folder lives
const IMG_EXTS = ['png', 'jpg', 'jpeg', 'svg', 'gif', 'webp'];
// Tolerant JSON read: strip a UTF-8 BOM so a stray BOM never makes a task silently vanish from the list.
const readJSON = f => JSON.parse(fs.readFileSync(f, 'utf8').replace(/^﻿/, ''));
const DATA_DIR = path.join(BASE, 'data');
const CUSTOM_PIPELINES_FILE = path.join(DATA_DIR, 'custom-pipelines.json');
const PROGRESS_FILE = path.join(DATA_DIR, 'progress.md');
const JOBS_DIR = path.join(BASE, 'jobs');
const BRAND_FILE = path.join(DATA_DIR, 'brand.json');
const STYLE_NOTES = path.join(DATA_DIR, 'style-notes.json');       // plain-language notes for the style editor
const STYLE_ELEMENTS = path.join(DATA_DIR, 'style-elements.json'); // element names the editor groups by
const BRAND_ASSETS_DIR = path.join(DATA_DIR, 'brand-assets');
// Shared content source: progress.md + brand are mirrored FROM the GitHub repo into this local
// data/ cache, so every teammate's console starts from the same source. Config is machine-specific
// (gitignored). Reads still come from local data/, so the app works offline; /sync refreshes it.
const SOURCE_FILE = path.join(DATA_DIR, 'source.json');
// Headless Claude CLI — used to attend a queued request on demand (semi-auto, one click)
// Resolve the Claude CLI per machine (was hardcoded to one user's path).
// Prefer an explicit CLAUDE_BIN env var, then the current user's native install,
// then a plain 'claude' on PATH. Works for anyone who clones the repo.
const CLAUDE_BIN = (function () {
  const os = require('os');
  const candidates = [
    process.env.CLAUDE_BIN,
    path.join(os.homedir(), '.local', 'bin', 'claude.exe'),
    path.join(os.homedir(), '.local', 'bin', 'claude'),
  ].filter(Boolean);
  for (const c of candidates) { try { if (fs.existsSync(c)) return c; } catch (_) {} }
  return 'claude'; // fall back to PATH lookup
})();

// Canonical Cybele palette 06/26 — seeded the first time only
const SEED_COLORS = [
  { name: 'Brand blue', hex: '#0F7FE0' },
  { name: 'Brand strong', hex: '#0A74D6' },
  { name: 'Blue light', hex: '#5BAFFF' },
  { name: 'Mint', hex: '#3DCCA1' },
  { name: 'Oracle red', hex: '#C74634' },
  { name: 'Navy', hex: '#0A1A2F' },
  { name: 'Canvas', hex: '#EEF4FB' },
];

function loadBrandColors() {
  try {
    if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
    if (!fs.existsSync(BRAND_FILE)) { fs.writeFileSync(BRAND_FILE, JSON.stringify({ colors: SEED_COLORS }, null, 2)); return SEED_COLORS; }
    const parsed = readJSON(BRAND_FILE);
    return Array.isArray(parsed.colors) ? parsed.colors : SEED_COLORS;
  } catch (e) { return SEED_COLORS; }
}

function listBrandFiles() {
  if (!fs.existsSync(BRAND_ASSETS_DIR)) return [];
  return fs.readdirSync(BRAND_ASSETS_DIR).filter(n => !n.startsWith('.')).map(n => ({
    name: n,
    url: '/data/brand-assets/' + encodeURIComponent(n),
    ext: path.extname(n).slice(1).toLowerCase(),
  }));
}

// ── Shared content source (GitHub) ───────────────────────────────────────────
// GitHub is the source of truth; local data/ is a cache. We pull via git (reusing git's own
// credentials — no token to manage) so it works for a private repo. Falls back to local files
// when the app isn't running inside a clone or the network is down.
let lastSync = { at: null, ok: false, error: 'not synced yet', files: [], mode: 'local' };

function loadSource() {
  // branch:null means "follow the branch this clone is on" (auto-detected at sync time), so each
  // teammate syncs from their own checked-out branch (you: Nick, the team: main, a tester: theirs).
  const def = { enabled: true, remote: 'origin', branch: null, repoDir: null, prefix: null };
  try { if (fs.existsSync(SOURCE_FILE)) return Object.assign(def, readJSON(SOURCE_FILE)); } catch (e) {}
  return def;
}

// The branch to sync from: the configured one, else the clone's currently checked-out branch.
function resolveBranch(s, gitDir) {
  if (s.branch) return s.branch;
  try {
    const b = git(['rev-parse', '--abbrev-ref', 'HEAD'], gitDir).toString().trim();
    if (b && b !== 'HEAD') return b;
  } catch (e) {}
  return 'main';
}

// Run a git command in gitDir. Returns stdout (string, or Buffer when asBuffer for binary files).
function git(args, gitDir, asBuffer) {
  const r = spawnSync('git', ['-C', gitDir, ...args], {
    encoding: asBuffer ? 'buffer' : 'utf8', maxBuffer: 64 * 1024 * 1024, windowsHide: true, timeout: 25000,
  });
  if (r.error) throw r.error;
  if (r.status !== 0) {
    const err = ((asBuffer && r.stderr ? r.stderr.toString() : r.stderr) || '').trim();
    throw new Error(err.split('\n').filter(Boolean).pop() || ('git exited ' + r.status));
  }
  return r.stdout;
}

function sourceInfo() {
  const s = loadSource();
  const gitDir = s.repoDir || BASE;
  let remoteUrl = null;
  try { remoteUrl = git(['remote', 'get-url', s.remote], gitDir).toString().trim(); } catch (e) {}
  // Where the shell document pipelines (pptx, whitepaper) live: <this folder>/deckgen, versioned
  // with the console. Set CYBELE_DECKGEN_DIR only to point the console at a different copy.
  const deckgenDir = process.env.CYBELE_DECKGEN_DIR || path.join(BASE, 'deckgen').replace(/\\/g, '/');
  return Object.assign({}, s, { branch: resolveBranch(s, gitDir), remoteUrl, lastSync, deckgenDir });
}

// Mirror progress.md + brand.json + brand-assets/ from the repo ref into local data/, except where this
// clone has work of its own on a file (see "Never overwrite local work" below).
// jobs/ is per-instance and intentionally NOT synced.
function syncFromGitHub() {
  const s = loadSource();
  if (!s.enabled) { lastSync = { at: new Date().toISOString(), ok: true, error: null, files: [], mode: 'local-disabled' }; return lastSync; }
  const gitDir = s.repoDir || BASE;
  try { git(['rev-parse', '--is-inside-work-tree'], gitDir); }
  catch (e) {
    lastSync = { at: new Date().toISOString(), ok: false, error: 'Not a git clone (' + gitDir + ') — serving local files', files: [], mode: 'local' };
    return lastSync;
  }
  try {
    const branch = resolveBranch(s, gitDir);
    git(['fetch', s.remote, branch], gitDir);
    let prefix = s.prefix;
    if (prefix === null || prefix === undefined) prefix = git(['rev-parse', '--show-prefix'], gitDir).toString().trim();
    prefix = String(prefix).replace(/\/$/, '');
    const ref = s.remote + '/' + branch;
    const dataPath = (prefix ? prefix + '/' : '') + 'data';
    if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
    const written = [], kept = [];
    // Never overwrite local work (2026-09-28). The remote copy is written only when this clone has
    // nothing of its own for that file:
    //   - unpushed: a local commit touches it that the remote doesn't have yet (incl. a deletion);
    //   - uncommitted: the file on disk differs from HEAD (text compared without CRs, as autocrlf
    //     makes CRLF-only differences meaningless);
    //   - local-only: it exists here but not in HEAD (e.g. a fresh upload from Brand assets).
    // Before this, every start reverted progress.md to the remote until a push, undoing committed work.
    // `:(top)` roots the pathspec at the repo: gitDir is the web-app/ subfolder, and a plain relative
    // pathspec resolved to web-app/web-app/..., which is why brand-assets never synced at all.
    const TEXT = /\.(md|json|svg|txt|css|js|html)$/i;
    const same = (a, b, repoPath) => TEXT.test(repoPath)
      ? a.toString('utf8').replace(/\r/g, '') === b.toString('utf8').replace(/\r/g, '')
      : Buffer.compare(a, b) === 0;
    const localReason = (repoPath, localFile) => {
      if (git(['log', '--format=%H', ref + '..HEAD', '--', ':(top)' + repoPath], gitDir).toString().trim()) return 'unpushed';
      if (!fs.existsSync(localFile)) return null;
      let head = null;
      try { head = git(['show', 'HEAD:' + repoPath], gitDir, true); } catch (e) {}
      if (!head) return 'local-only';
      return same(fs.readFileSync(localFile), head, repoPath) ? null : 'uncommitted';
    };
    const mirror = (repoPath, localFile, label) => {
      let remote;
      try { remote = git(['show', ref + ':' + repoPath], gitDir, true); } catch (e) { return; } // absent on the ref
      const why = localReason(repoPath, localFile);
      if (why) { kept.push({ file: label, why }); return; }
      if (!fs.existsSync(localFile) || !same(fs.readFileSync(localFile), remote, repoPath)) {
        fs.mkdirSync(path.dirname(localFile), { recursive: true });
        fs.writeFileSync(localFile, remote);
      }
      written.push(label);
    };
    for (const f of ['progress.md', 'brand.json']) mirror(dataPath + '/' + f, path.join(DATA_DIR, f), f);
    const list = git(['ls-tree', '-r', '--name-only', '--full-tree', ref, '--', ':(top)' + dataPath + '/brand-assets'], gitDir)
      .toString().split(/\r?\n/).filter(Boolean);
    for (const full of list) {
      const name = path.basename(full);
      mirror(full, path.join(BRAND_ASSETS_DIR, name), 'brand-assets/' + name);
    }
    lastSync = { at: new Date().toISOString(), ok: true, error: null, files: written, kept, mode: 'github', ref };
  } catch (e) {
    lastSync = { at: new Date().toISOString(), ok: false, error: String((e && e.message) || e), files: [], mode: 'github-error' };
  }
  return lastSync;
}

// ── Style rules ─────────────────────────────────────────────────────────────────────────────────
// Each document type draws from its own specification files. Those specs are markdown, and a
// designer should not have to read markdown to change a colour, a type size or a weight. These
// endpoints expose every style value in them and write one back **in place**: same file, same line,
// same position, nothing else touched.
//
// Brand assets stays what it is — the catalogue of everything the brand has. This is the opposite:
// what each document type actually uses, and the only thing that changes a generated visual.
const STYLE_SPECS = [
  // Covers used to appear here with 141 values, every one of them from the retired generative
  // system. A cover is now a text brief designed by a person: there is no value to configure, so
  // the row is gone rather than sitting empty and looking broken.
  { key: 'blog', label: 'Blog Images', files: [
    { rel: '../skills/cybele-blog-visuals/SECTION_RULES.md',      label: 'Section illustrations' },
  ]},
  { key: 'arch', label: 'Arch Diagrams', files: [
    { rel: '../skills/thinfinity-architecture/SKILL.md',          label: 'Diagram system' },
  ]},
  { key: 'pptx', label: 'PPTX Generation', files: [
    { rel: 'data/progress.md', label: 'Pipeline rules', section: 'PPTX Generation Pipeline', mirrored: true },
    { rel: '../skills/cybele-blog-visuals/BRAND_DESIGN_RULES.md', label: 'Slide layout', section: 'Slide Layout' },
  ]},
  { key: 'wp', label: 'Whitepaper PDF', files: [
    { rel: 'data/progress.md', label: 'Pipeline rules', section: 'PDF Whitepaper Pipeline', mirrored: true },
  ]},
  { key: 'shared', label: 'Shared brand tokens', files: [
    { rel: '../skills/cybele-blog-visuals/BRAND_DESIGN_RULES.md', label: 'Colour, typography, logos' },
  ]},
  // Both specs used to live only on the original author's machine, so these two rows said so and
  // offered nothing to edit. They now sit in web-app/pipelines/ — the console is what reads them —
  // and are parsed like every other spec. Neither pipeline is a packaged skill; it follows its spec
  // directly, which is why the files are filed with the app rather than under skills/.
  //
  // Scoped by section on purpose. Unlike the specs written for this editor, these two are long
  // prose documents: provenance notes, verbatim contracts, changelogs and verify checklists all
  // quote numbers, and parsing the whole file turned a changelog percentage and a stray "2 px" into
  // editable style rules. The sections named here are the ones that actually define how the visual
  // is drawn — the same tables a person would edit. Several entries may share one file: an edit is
  // applied by absolute line number, so only the path is taken from the entry.
  { key: 'storyboard', label: 'Video Storyboard', files: [
    { rel: 'pipelines/STORYBOARD_SPEC.md',        label: 'Design system',    section: '4. The design system' },
  ]},
  { key: 'linkedin-carousel', label: 'LinkedIn Carousel', files: [
    { rel: 'pipelines/LINKEDIN_CAROUSEL_SPEC.md', label: 'Themes',           section: '4. Themes' },
    { rel: 'pipelines/LINKEDIN_CAROUSEL_SPEC.md', label: 'Colour semantics', section: '5. Colour semantics' },
    { rel: 'pipelines/LINKEDIN_CAROUSEL_SPEC.md', label: 'Typography',       section: '6. Typography' },
    { rel: 'pipelines/LINKEDIN_CAROUSEL_SPEC.md', label: 'Composition',      section: '7. Composition' },
  ]},
];

// The nine weights Inter ships, with the numeric form of each. A spec may write either "SemiBold"
// or "SemiBold 600"; both are the same weight, so the editor keeps whichever shape the line uses.
const FONT_WEIGHTS = ['Thin', 'ExtraLight', 'Light', 'Regular', 'Medium', 'SemiBold', 'Bold', 'ExtraBold', 'Black'];

// What counts as an editable style value, and what a new value has to look like. Family and weight
// are separate variables: "Inter" is the typeface, "SemiBold" is the weight, and mixing them into
// one field made the weight impossible to pick from a list.
const STYLE_KINDS = [
  { kind: 'color',  re: /#[0-9a-fA-F]{6}\b/g,                     ok: v => /^#[0-9a-fA-F]{6}$/.test(v) },
  { kind: 'size',   re: /\b\d{1,4}(?:\.\d+)?\s?(?:px|pt)\b/g,     ok: v => /^\d{1,4}(?:\.\d+)?\s?(?:px|pt)$/.test(v) },
  // A ratio, not a length: an icon at 62% of its badge, a margin at 3% of the canvas. Percentages
  // are what let one rule hold at any size, so they are editable like every other value.
  { kind: 'percent', re: /\b\d{1,3}(?:\.\d+)?%/g,                 ok: v => /^\d{1,3}(?:\.\d+)?%$/.test(v) },
  { kind: 'radius', re: /\brx="\d{1,3}"/g,                        ok: v => /^rx="\d{1,3}"$/.test(v) },
  // A budget, not a length: how much text a card may carry, and how many cards an illustration may
  // hold. They are rules for the same reason a colour is — a run has to obey them and the designer
  // has to be able to change them — and they are the two the geometry is derived from now that a
  // card has no fixed size.
  { kind: 'chars',  re: /\b\d{1,4}\s?chars\b/g,                    ok: v => /^\d{1,4}\s?chars$/.test(v) },
  { kind: 'count',  re: /\b\d{1,3}\s?cards\b/g,                    ok: v => /^\d{1,3}\s?cards$/.test(v) },
  { kind: 'rgba',   re: /rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*[\d.]+\s*\)/g,
                    ok: v => /^rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*[\d.]+\s*\)$/.test(v) },
  // Family and weight are matched separately, and only where the two sit together, so the word
  // "Inter" in prose is never offered as an editable value.
  { kind: 'family', re: /\bInter\b(?=\s+(?:Thin|ExtraLight|Light|Regular|Medium|SemiBold|Bold|ExtraBold|Black)\b)/g,
                    ok: v => /^[A-Za-z][A-Za-z0-9 .-]{0,30}$/.test(v) },
  // Two shapes of weight: right after the family ("Inter SemiBold"), or as its own cell with the
  // number ("SemiBold 600"). The second needs the number, so prose like "**Bold labels**" is left alone.
  { kind: 'weight', re: /(?<=\bInter\s)(?:Thin|ExtraLight|Light|Regular|Medium|SemiBold|Bold|ExtraBold|Black)(?:\s+\d{3})?|\b(?:Thin|ExtraLight|Light|Regular|Medium|SemiBold|Bold|ExtraBold|Black)\s+\d{3}\b/g,
                    ok: v => /^(?:Thin|ExtraLight|Light|Regular|Medium|SemiBold|Bold|ExtraBold|Black)(?: \d{3})?$/.test(v) },
];

// ── Modes ──────────────────────────────────────────────────────────────────────────────────────
// A mode is a named variant an illustration is built in (light, dark, and whatever the designer
// adds). Modes are declared in a spec's `## Modes` table, and every value that varies by mode names
// its mode in the column header ("Light", or "Light · bg fill" when an element colours two things).
// Reading them from the spec keeps one source of truth: adding a mode is an edit to that table.
function parseStyleModes(abs) {
  let all = [];
  try { all = fs.readFileSync(abs, 'utf8').split(/\r?\n/); } catch (e) { return []; }
  const out = [];
  let inSection = false, sepSeen = false;
  for (let i = 0; i < all.length; i++) {
    const line = all[i], h = line.match(/^(#{2,4})\s+(.*)/);
    if (h) {
      const isModes = /^modes$/i.test(h[2].replace(/[*`]/g, '').trim());
      if (inSection && !isModes) break;
      inSection = isModes; sepSeen = false;
      continue;
    }
    if (!inSection) continue;
    const t = line.trim();
    if (!(t.startsWith('|') && t.endsWith('|'))) continue;
    if (/^\|[\s:\-|]+\|$/.test(t)) { sepSeen = true; continue; }
    if (!sepSeen) continue;                       // the header row
    const cells = t.split('|').slice(1, -1).map(c => c.replace(/[*`]/g, '').trim());
    if (!cells[0]) continue;
    out.push({ name: cells[0], description: cells[1] || '', line: i });
  }
  return out;
}
// Which mode a column belongs to, and what it names within that mode. "Light" -> [Light, ''];
// "Light · icon fill" -> [Light, 'icon fill']; "Size" -> [null, 'Size'].
function splitModeColumn(column, modes) {
  const col = String(column || '').trim();
  for (const m of modes) {
    const re = new RegExp('^' + m.name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
      + '(?:\\s+mode)?(?:\\s*[·:-]\\s*(.*))?$', 'i');
    const hit = col.match(re);
    if (hit) return { mode: m.name, prop: (hit[1] || '').trim() };
  }
  return { mode: null, prop: col };
}

function styleSpecFile(specKey, rel) {
  const spec = STYLE_SPECS.find(s => s.key === specKey);
  const f = spec && spec.files.find(x => x.rel === rel);
  return f ? { file: f, abs: path.normalize(path.join(BASE, f.rel)) } : null;
}

// The line range a file entry covers: a named section, or the whole file.
function styleRange(lines, section) {
  if (!section) return [0, lines.length];
  let start = -1, level = 0;
  for (let i = 0; i < lines.length; i++) {
    const m = lines[i].match(/^(#{2,4})\s+(.*)/);
    if (m && m[2].toLowerCase().includes(section.toLowerCase())) { start = i; level = m[1].length; break; }
  }
  if (start < 0) return null;
  for (let i = start + 1; i < lines.length; i++) {
    const m = lines[i].match(/^(#{2,4})\s+/);
    if (m && m[1].length <= level) return [start, i];
  }
  return [start, lines.length];
}

// A rule's values are scattered through a spec by markdown structure: the title's colour sits in a
// surfaces table, its size and weight in a typography bullet. People think in elements, not in
// tables, so every value carries an `element` key — a normalised form of its label — and the UI can
// group by that instead. `data/style-elements.json` overrides the name and adds a description, which
// is also how two different labels get merged into one element.
function styleElementKey(label) {
  return String(label)
    .toLowerCase()
    .replace(/\([^)]*\)/g, ' ')            // "Icon badge (circular)" -> "icon badge"
    .replace(/[^a-z0-9/ ]+/g, ' ')
    .split(/\s+/).filter(Boolean)
    .map(w => (w.length > 3 && !/(us|ss|is|os|as)$/.test(w) ? w.replace(/s$/, '') : w))   // Titles -> title; radius, canvas stay whole
    .join(' ')
    .trim();
}

// Every style value in a spec, plus the shape of the tables that hold them (so a row can be added
// or removed from the UI). Code fences are skipped: those are illustrative snippets, not rules.
// Inside a table the column header names the value ("Page surface · Dark mode"), because one label
// usually spans several modes.
function parseStyleTokens(abs, section) {
  const all = fs.readFileSync(abs, 'utf8').split(/\r?\n/);
  const range = styleRange(all, section);
  if (!range) return null;
  const tokens = [], tables = [];
  let heading = '', fence = false, header = null, table = null, prev = '', histBlock = false;
  let histSection = false;   // a "> reference only" note governs everything under its ## heading
  // The parent `##` a value sits under. The spec files group their rules by purpose at that level
  // (margins and spacing / text / elements / colors), and the editor shows that grouping, so a
  // value has to carry the section it belongs to and not only its nearest heading.
  let group = '';
  const cellsOf = l => l.split('|').slice(1, -1).map(c => c.trim());
  const clean = t => (t || '').replace(/[*`]/g, '').replace(/\s+/g, ' ').trim();
  const closeTable = () => { if (table && table.rows.length) tables.push(table); table = null; header = null; };
  for (let i = range[0]; i < range[1]; i++) {
    const line = all[i];
    if (/^\s*```/.test(line)) { fence = !fence; prev = line; continue; }
    if (fence) { prev = line; continue; }
    const h = line.match(/^#{2,4}\s+(.*)/);
    if (h) {
      closeTable(); heading = clean(h[1]); histBlock = false;
      if (/^##\s/.test(line)) { histSection = false; group = heading; }   // a new top-level section
      prev = line; continue;
    }
    const trimmed = line.trim();
    const isRow = trimmed.startsWith('|') && trimmed.endsWith('|');
    const isHeaderRow = isRow && /^\|[\s:\-|]+\|$/.test((all[i + 1] || '').trim());
    if (isRow && /^\|[\s:\-|]+\|$/.test(trimmed)) {
      header = cellsOf(prev.trim()).map(clean);
      table = { heading, header, headerLine: i - 1, sepLine: i, lastRow: i, rows: [] };
      prev = line; continue;
    }
    if (!isRow) { closeTable(); if (trimmed === '') histBlock = false; }
    else if (table) { table.rows.push(i); table.lastRow = i; }
    // Values kept only as history must not be editable — changing them would rewrite the record.
    // A "superseded"/"retired" note governs its whole paragraph, not just the line it sits on; the
    // same note in a blockquote right under a `##` governs that whole section, subheadings included
    // (which is how "### Figma sources" stopped offering a stray 70% from a historical bullet).
    const marker = /retired|superseded|legacy|deprecat|previous canonical|open questions|never use|reference only/i;
    if (marker.test(line)) { histBlock = true; if (/^\s*>/.test(line)) histSection = true; }
    const historic = histBlock || histSection || marker.test(heading);
    const tokensBefore = tokens.length;
    for (const k of STYLE_KINDS) {
      const hits = line.match(k.re);
      if (!hits) continue;
      hits.forEach((raw, occ) => {
        let label, column = '', context = '', cell = 0, isList = false, isFill = false;
        if (isRow) {
          const cells = cellsOf(trimmed);
          label = clean(cells[0]) || heading;
          // Which cell holds THIS occurrence. Counting matches cell by cell matters when the same
          // value appears in two columns (a colour used in both light and dark mode).
          let ci = 0, seen = 0;
          for (let n = 0; n < cells.length; n++) {
            const inCell = (cells[n].match(new RegExp(k.re.source, 'g')) || []).length;
            if (occ < seen + inCell) { ci = n; break; }
            seen += inCell;
            ci = n;
          }
          cell = ci;
          column = header && header[ci] && ci > 0 ? header[ci] : '';
          // "(list)" in the header says the cell holds a set, not a structure: the console may then
          // add or drop one value in it. A gradient pair is two values in one cell too, and pulling
          // one out of that would break the recipe — hence a marker rather than a guess.
          if (/\(list\)\s*$/i.test(column)) { isList = true; column = column.replace(/\s*\(list\)\s*$/i, ''); }
          // "(fill)" says the value may be a colour OR the word none — a background a mode chooses
          // not to draw. Only marked columns accept it: elsewhere `none` is a value nothing can draw.
          if (/\(fill\)\s*$/i.test(column)) { isFill = true; column = column.replace(/\s*\(fill\)\s*$/i, ''); }
          context = cells.filter((c, n) => n !== 0 && n !== ci).map(clean)
                         .filter(c => c && !new RegExp(k.re.source).test(c)).join(' · ');
        } else {
          // A bullet names its own rule: "- **Titles:** Inter SemiBold, ~52px" -> "Titles".
          const bullet = line.match(/^\s*[-*]\s+\**([^:*]{2,40})\**\s*:/);
          const before = line.slice(0, line.indexOf(raw));
          const m = [...before.matchAll(/`([^`]+)`|\*\*([^*]+)\*\*/g)].pop();
          label = clean((bullet && bullet[1]) || (m && (m[1] || m[2])) || heading) || 'in text';
          // Several values of the same kind on one line are ambiguous on their own ("7 · 14 · 20"),
          // so each is named after the words that introduce it: pills/chips, cards, highlighted card.
          if (hits.length > 1) {
            let cursor = 0;
            const lead = [];
            hits.forEach(h => {
              const at = line.indexOf(h, cursor);
              lead.push(line.slice(cursor, at));
              cursor = at + h.length;
            });
            let seg = lead[occ] || '';
            if (occ === 0 && bullet) seg = seg.slice(seg.indexOf(':') + 1);
            seg = clean(seg).replace(/^[\s·,;:—–-]+/, '').replace(/[\s·,;:—–-]+$/, '');
            const words = seg.split(' ').filter(Boolean);
            column = words.slice(-6).join(' ') || ('#' + (occ + 1));
            // Drop a lead-in that only repeats the rule's own name, and keep it short enough to read.
            if (column.toLowerCase().endsWith(label.toLowerCase())) column = label;
            if (column.toLowerCase() === label.toLowerCase()) column = '';
            if (column.length > 42) column = column.split(' ').slice(-4).join(' ');
          }
        }
        tokens.push({ line: i, occ, cell, kind: k.kind, value: raw, label, column, context, heading,
                      group, historic, list: isList, fill: isFill, row: isRow, raw: line,
                      element: styleElementKey(label) });
      });
    }
    // A table cell can hold a rule the parser cannot turn into a control — "white @ 10%", "—", a
    // sentence saying when to use it. Those are shown read-only so a light/dark pair never looks
    // half-defined. They only ever COMPLETE a rule that already has an editable value: a row with
    // no value at all is not a rule (it is a header, or a prose table), and must not become one.
    if (isRow && tokens.length > tokensBefore && !isHeaderRow) {
      const cells = cellsOf(trimmed);
      const parsed = new Set();
      cells.forEach((c, ci) => {
        if (STYLE_KINDS.some(k => new RegExp(k.re.source).test(c))) parsed.add(ci);
      });
      cells.forEach((c, ci) => {
        if (ci === 0 || parsed.has(ci)) return;
        const text = clean(c);
        if (!text || text.length > 70) return;
        // In a (fill) column the word `none` is the value, and it has to stay changeable — a
        // background a mode turned off is not prose.
        const hdr = (header && header[ci]) || '';
        const fillCol = /\(fill\)\s*$/i.test(hdr);
        if (fillCol && /^none$/i.test(text)) {
          tokens.push({ line: i, occ: ci, cell: ci, kind: 'text', value: 'none', editable: false,
                        fill: true, nobg: true,
                        label: clean(cells[0]) || heading,
                        column: hdr.replace(/\s*\(fill\)\s*$/i, ''), context: '', heading, group,
                        historic, row: true, raw: line,
                        element: styleElementKey(clean(cells[0]) || heading) });
          return;
        }
        tokens.push({ line: i, occ: ci, cell: ci, kind: 'text', value: text, editable: false,
                      label: clean(cells[0]) || heading,
                      column: (header && header[ci]) || '', context: '', heading, group, historic,
                      row: true, raw: line, element: styleElementKey(clean(cells[0]) || heading) });
      });
    }
    prev = line;   // the row above a |---| separator is the header, so every line must be remembered
  }
  closeTable();
  // Tag values with the mode their column names, so the editor can show a mode's values together:
  // in a finished illustration the background fill and the icon on it are one decision, not two.
  const modes = parseStyleModes(abs);
  if (modes.length) {
    tokens.forEach(t => {
      const sp = splitModeColumn(t.column, modes);
      t.mode = sp.mode; t.prop = sp.prop;
    });
  }
  // Show a row's values in the order its COLUMNS are written, not in the order the kind regexes
  // happened to match. Scanning runs kind by kind, so every colour came out first and every
  // percentage last — which turned a colour and the opacity written beside it into two unrelated
  // lists at opposite ends of the element. They are one decision and they belong side by side.
  tokens.sort((a, b) => a.line - b.line || (a.cell || 0) - (b.cell || 0));
  return { tokens, tables, modes };
}

// Which progress.md heading provides the working context for each pipeline
const SECTION_KEYWORDS = {
  pptx:   'PPTX Generation Pipeline',
  wp:     'PDF Whitepaper Pipeline',
  blog:   'SVG Blog Illustration Pipeline',
  arch:   'Thinfinity Architecture Diagram Skill',
  // pointer sections to their specs in pipelines/ (added 2026-09-28; RUNBOOK §2 already listed them)
  storyboard: 'Video Storyboard Pipeline',
  'linkedin-carousel': 'LinkedIn Carousel (Placas)',
  webapp: 'Project Vision',
  shared: 'Next Steps',
};

// Extract a markdown section (a heading and everything until the next same-or-higher heading)
function extractSection(md, keyword) {
  const lines = md.split(/\r?\n/);
  let start = -1, startLevel = 0;
  for (let i = 0; i < lines.length; i++) {
    const m = lines[i].match(/^(#{2,4})\s+(.*)/);
    if (m && m[2].toLowerCase().includes(keyword.toLowerCase())) { start = i; startLevel = m[1].length; break; }
  }
  if (start === -1) return null;
  let end = lines.length;
  for (let i = start + 1; i < lines.length; i++) {
    const m = lines[i].match(/^(#{1,4})\s+/);
    if (m && m[1].length <= startLevel) { end = i; break; }
  }
  return lines.slice(start, end).join('\n').trim();
}

// ── Live task channel (SSE) ────────────────────────────────────────────────────────────────────
// The console used to ask "did anything change?" every few seconds and redraw regardless, which
// meant ~900 pointless requests an hour and a list that rebuilt itself under the user's hands.
// The server knows when something changed — it is the one writing job.json — so it says so instead.
const sseClients = new Set();
let sseWatcher = null, sseDebounce = null;
function sseBroadcast(event, payload) {
  const msg = `event: ${event}\ndata: ${JSON.stringify(payload || {})}\n\n`;
  for (const res of sseClients) { try { res.write(msg); } catch (e) { sseClients.delete(res); } }
}
function watchJobs() {
  if (sseWatcher || !fs.existsSync(JOBS_DIR)) return;
  try {
    // Coalesced: writing one run's output touches many files, and the client only needs one nudge.
    sseWatcher = fs.watch(JOBS_DIR, { recursive: true }, () => {
      clearTimeout(sseDebounce);
      sseDebounce = setTimeout(() => sseBroadcast('jobs', { at: Date.now() }), 350);
    });
  } catch (e) { sseWatcher = null; }   // no watcher on this platform → the client falls back
}

function listJobs() {
  if (!fs.existsSync(JOBS_DIR)) return [];
  const out = [];
  for (const id of fs.readdirSync(JOBS_DIR)) {
    const jf = path.join(JOBS_DIR, id, 'job.json');
    try {
      if (!fs.existsSync(jf)) continue;
      const job = readJSON(jf);
      // The cover brief is the deliverable a blog run writes for the cover — text, read on the task
      // itself. Carried here so the card can show it in place of the prompt, which stops being
      // useful the moment the run is over.
      const brief = jobBrief(job);
      if (brief) job.brief = brief;
      out.push(job);
    } catch (e) {}
  }
  return out.sort((a, b) => String(b.createdAt).localeCompare(String(a.createdAt)));
}
// COVER_BRIEF.md from the run folder of a job's latest output, if it wrote one.
const BRIEF_MAX = 8000;
function jobBrief(job) {
  try {
    const rel = job.resultPath || job.previewPath;
    if (!rel) return null;
    const abs = path.normalize(path.join(BASE, String(rel).replace(/^\/+/, '')));
    if (!abs.startsWith(path.normalize(BASE))) return null;
    const f = path.join(deliverableFolder(abs), 'COVER_BRIEF.md');
    if (!fs.existsSync(f)) return null;
    return fs.readFileSync(f, 'utf8').slice(0, BRIEF_MAX);
  } catch (e) { return null; }
}

// A design is a full canvas (1920×1080, 1200×1500…). Vectors bundled beside it — an icon set under
// icons/, a logo — are ingredients, not separate downloads, so they never count as designs.
const MIN_DESIGN_SIDE = 400;
function svgCanvasSide(text) {
  const vb = text.match(/viewBox\s*=\s*["']\s*[-\d.]+[,\s]+[-\d.]+[,\s]+([\d.]+)[,\s]+([\d.]+)/i);
  if (vb) return Math.min(parseFloat(vb[1]), parseFloat(vb[2]));
  const w = text.match(/<svg[^>]*\bwidth\s*=\s*["']([\d.]+)/i);
  const h = text.match(/<svg[^>]*\bheight\s*=\s*["']([\d.]+)/i);
  if (w && h) return Math.min(parseFloat(w[1]), parseFloat(h[1]));
  return Infinity;   // no size declared → treat it as a design
}
// Clean vector SVGs in a deliverable folder (skips raster-wrapped SVGs). Shared by /export & /formats
// so downloads are always driven by the real, editable vectors when they exist.
function cleanSvgsIn(folder) {
  try {
    return fs.readdirSync(folder, { recursive: true })
      .filter(f => f.toLowerCase().endsWith('.svg'))
      .map(f => path.join(folder, f))
      .filter(p => {
        try {
          const t = fs.readFileSync(p, 'utf8');
          return !/<image\b[^>]*base64/i.test(t) && svgCanvasSide(t) >= MIN_DESIGN_SIDE;
        } catch (e) { return false; }
      })
      .sort();
  } catch (e) { return []; }
}
// Working folders whose SVGs are ingredients of the deliverable, never the deliverable itself —
// plus board/contact-sheet folders, which hold ONE huge SVG containing all the other designs laid
// out in a grid (a blog task's figma-board is 6360×6900 and weighs the same as its 15 designs put
// together). Shipping it would duplicate the whole set inside the zip and take slot 7, pushing the
// numbers the Selection field refers to out of step with what the user sees. It stays on disk in
// the task folder; it just does not count as a design. If a future task names such a folder
// something else, add the name here.
const NON_DELIVERABLE_DIRS = new Set(['icons', 'assets', 'fonts', 'src', 'raw', 'tmp', 'temp', 'build',
  'node_modules', 'annotations', 'attachments', 'thumbs', 'logs', 'diff', 'renders', '__pycache__',
  'figma-board', 'figma_board', 'board', 'boards']);
// Some pipelines file their designs one level down (blog visuals: covers/ + sections/) and leave only
// preview.html/.pdf at the top, which used to read as "no vectors here" and greyed out SVG and PPTX.
// So when the folder itself holds no vectors, look one level into its deliverable-looking subfolders.
// Fallback only: a folder that HAS its own vectors is taken as the complete set, so an arch diagram
// still exports as one SVG instead of dragging in the icons/ it was drawn from.
function listVectorSvgs(folder) {
  const own = cleanSvgsIn(folder);
  if (own.length) return own;
  let subs = [];
  try {
    subs = fs.readdirSync(folder, { withFileTypes: true })
      .filter(d => d.isDirectory() && !d.name.startsWith('_') && !d.name.startsWith('.')
        && !NON_DELIVERABLE_DIRS.has(d.name.toLowerCase()))
      .map(d => d.name).sort();
  } catch (e) { return []; }
  return subs.flatMap(n => cleanSvgsIn(path.join(folder, n)));
}
// The deliverable is the whole run folder — jobs/<id>/output/v<N>/ — not the subfolder one file
// happens to sit in. A blog run keeps its designs in covers/ and sections/, so resolving the folder
// as the dirname of resultPath would find one cover and miss every other design.
function runRoot(folder) {
  let p = folder;
  for (let i = 0; i < 8 && p; i++) {
    if (/^v\d+$/i.test(path.basename(p)) && path.basename(path.dirname(p)).toLowerCase() === 'output') return p;
    const up = path.dirname(p);
    if (up === p) break;
    p = up;
  }
  return folder;   // legacy layout with no v<N> folder — leave it where it was
}
function deliverableFolder(...paths) {
  for (const p of paths) {
    if (p) {
      let f;
      try { f = fs.statSync(p).isDirectory() ? p : path.dirname(p); } catch (e) { f = path.dirname(p); }
      return runRoot(f);
    }
  }
  return '';
}

// ── Which Python ─────────────────────────────────────────────────────────────
// Python is spawned for PDF work (thumbnails, page counts) and to run export_doc.py. WHICH
// interpreter answers to `py` is per-machine, and a launcher default can point at a broken install:
// on this machine `py -3` resolves to a 3.14 whose stdlib will not load ("Failed to import encodings
// module"), while 3.13 has every module the console needs. Hardcoding either version breaks somebody
// — `-3` broke PPTX/PDF export here, `-3.13` would break a teammate without that exact minor — so
// the interpreter is discovered once by asking each candidate to import what is actually required.
// Set CYBELE_PYTHON to force one (same escape hatch as CYBELE_ICONS_DIR in build-icons.js).
const PY_REQUIRED = 'pymupdf';           // every call site needs this
const PY_PREFERRED = 'pymupdf, pptx';    // export_doc.py also builds editable decks
function pyCandidates() {
  const list = [];
  if (process.env.CYBELE_PYTHON) list.push({ cmd: process.env.CYBELE_PYTHON, prefix: [] });
  // the virtual environment that setup.ps1 builds next to this file, when it exists
  for (const rel of [['.venv', 'Scripts', 'python.exe'], ['.venv', 'bin', 'python']]) {
    const venvPy = path.join(BASE, ...rel);
    if (fs.existsSync(venvPy)) list.push({ cmd: venvPy, prefix: [] });
  }
  for (const v of ['-3.13', '-3.12', '-3.11', '-3']) list.push({ cmd: 'py', prefix: [v] });
  list.push({ cmd: 'python3', prefix: [] }, { cmd: 'python', prefix: [] });
  return list;
}
let PY;   // undefined = not probed yet; null = probed and nothing works
function python() {
  if (PY !== undefined) return PY;
  const works = (c, mods) => {
    try {
      return spawnSync(c.cmd, c.prefix.concat(['-c', 'import ' + mods]), { windowsHide: true, timeout: 20000 }).status === 0;
    } catch (e) { return false; }
  };
  // Prefer an interpreter that can also build decks; fall back to one that at least reads PDFs, so
  // thumbnails keep working on a machine where only python-pptx is missing.
  const cands = pyCandidates();
  PY = cands.find(c => works(c, PY_PREFERRED)) || cands.find(c => works(c, PY_REQUIRED)) || null;
  return PY;
}
// Python writes its real complaint on the last line of stderr; that is the useful half of a failure.
function lastLine(txt) { return (txt || '').trim().split(/\r?\n/).filter(Boolean).pop() || ''; }
function pyLabel() {
  const p = python();
  return p ? [p.cmd].concat(p.prefix).join(' ') : 'NOT FOUND (needs ' + PY_REQUIRED + '; set CYBELE_PYTHON)';
}
// Python is spawned to rasterise PDFs (thumbnails) and to count their pages. Those used to be
// spawnSync, which blocks this single-threaded server for as long as the interpreter runs: opening
// Task history asks for a thumbnail and a page count per task, so ~34 blocking spawns froze every
// other request. Measured before the change: steady 2–3 ms replies became 857 / 1900 / 1809 /
// 1532 ms for about six seconds, and a Download dialog opened in 8.5 s instead of 0.06 s.
// They run asynchronously now, through a small semaphore so the machine is never asked for 34
// interpreters at once — the queue is what keeps this from trading a freeze for a thrash.
const PY_MAX = 3;
let pyRunning = 0;
const pyQueue = [];
function pyPump() {
  while (pyRunning < PY_MAX && pyQueue.length) {
    const start = pyQueue.shift();
    pyRunning++;
    start().then(() => { pyRunning--; pyPump(); }, () => { pyRunning--; pyPump(); });
  }
}
// Resolves { status, stdout, stderr } and never rejects — every caller already treats a non-zero
// status as "could not do it", which is also the right answer for a spawn error or a timeout.
// args is what follows the interpreter (e.g. ['-c', code] or [script, ...]) — the interpreter
// itself comes from python(), so no call site names a version.
function runPy(args, opts = {}) {
  return new Promise(resolve => {
    const py = python();
    if (!py) return resolve({ status: 1, stdout: '', stderr: 'no usable Python: ' + pyLabel() });
    pyQueue.push(() => new Promise(release => {
      let out = '', err = '', settled = false;
      const finish = status => { if (settled) return; settled = true; resolve({ status, stdout: out, stderr: err }); release(); };
      let child;
      try { child = spawn(py.cmd, py.prefix.concat(args), { windowsHide: true }); }
      catch (e) { return finish(1); }
      const timer = setTimeout(() => { try { child.kill(); } catch (e) {} finish(1); }, opts.timeout || 30000);
      child.stdout.on('data', d => { out += d; });
      child.stderr.on('data', d => { err += d; });
      child.on('error', () => { clearTimeout(timer); finish(1); });
      child.on('close', code => { clearTimeout(timer); finish(code === null ? 1 : code); });
    }));
    pyPump();
  });
}

// Render page 1 of a PDF to a cached <file>.thumb.png (PyMuPDF). Returns the thumb path, or null.
async function renderPdfThumb(absPdf, scale, page) {
  try {
    if (!fs.existsSync(absPdf)) return null;
    const s = scale || 0.7;
    const pg = Math.max(0, parseInt(page) || 0);
    // 0.7/page0 keeps the legacy thumbnail filename; other scales/pages (annotate view) cache separately.
    const suffix = (s === 0.7 && pg === 0) ? '.thumb.png' : '.thumb.' + s + (pg ? '.p' + pg : '') + '.png';
    const thumb = absPdf + suffix;
    if (!fs.existsSync(thumb) || fs.statSync(thumb).mtimeMs < fs.statSync(absPdf).mtimeMs) {
      const py = `import pymupdf as fitz\nd=fitz.open(r'''${absPdf}''')\np=${pg} if ${pg}<d.page_count else 0\nd[p].get_pixmap(matrix=fitz.Matrix(${s},${s})).save(r'''${thumb}''')`;
      const r = await runPy(['-c', py], { timeout: 30000 });
      if (r.status !== 0 || !fs.existsSync(thumb)) return null;
    }
    return thumb;
  } catch (e) { return null; }
}

// Pre-warm thumbnail caches for a job's outputs so History/Overview open instantly. Best-effort.
// Mirrors the client's choice: an image result needs no render; otherwise pre-render the PDF.
async function prewarmThumbs(job) {
  try {
    for (const it of [job, ...(job.revisions || [])]) {
      const cands = [it.resultPath, it.previewPath].filter(Boolean);
      if (cands.some(p => IMG_EXTS.includes(path.extname(p).slice(1).toLowerCase()))) continue;
      const pdf = cands.find(p => path.extname(p).slice(1).toLowerCase() === 'pdf');
      if (!pdf) continue;
      const abs = path.normalize(path.join(BASE, pdf.replace(/^\/+/, '')));
      if (abs.startsWith(path.normalize(BASE))) await renderPdfThumb(abs);
    }
  } catch (e) {}
}

// On startup, no Claude run survives a restart — flip any orphaned 'running' back to 'queued'
// so a crash never leaves a request stuck mid-flight (it just needs the Run button again).
function resetStaleRunning() {
  if (!fs.existsSync(JOBS_DIR)) return;
  for (const id of fs.readdirSync(JOBS_DIR)) {
    const jf = path.join(JOBS_DIR, id, 'job.json');
    try {
      if (!fs.existsSync(jf)) continue;
      const job = readJSON(jf);
      let changed = false;
      if (job.status === 'running' || job.status === 'needs-input') { job.status = 'queued'; if (job.pending) job.pending = null; changed = true; }
      (job.revisions || []).forEach(r => { if (r.status === 'running' || r.status === 'needs-input') { r.status = 'queued'; changed = true; } });
      if (changed) { job.updatedAt = new Date().toISOString(); fs.writeFileSync(jf, JSON.stringify(job, null, 2)); }
    } catch (e) {}
  }
}

// ── Headless-Claude run control (start / stop / re-run) ───────────────────────
const RUNNING = {}; // job id -> { child, target, stopped }

// Spawn Claude for the queued item of a job (base, else the highest queued revision).
function startQueuedRun(id) {
  const jf = path.join(JOBS_DIR, id, 'job.json');
  if (!fs.existsSync(jf)) return { ok: false, error: 'job not found' };
  const job = readJSON(jf);
  let target = null;
  if (job.status === 'queued') target = { kind: 'base', text: job.prompt };
  else {
    const qr = (job.revisions || []).filter(r => r.status === 'queued').sort((a, b) => b.n - a.n)[0];
    if (qr) target = { kind: 'rev', n: qr.n, text: qr.prompt };
  }
  if (!target) return { ok: false, error: 'nothing queued' };
  if (target.kind === 'base') job.status = 'running';
  else job.revisions.find(r => r.n === target.n).status = 'running';
  job.updatedAt = new Date().toISOString();
  fs.writeFileSync(jf, JSON.stringify(job, null, 2));

  const which = target.kind === 'base' ? 'the base job' : ('revision ' + target.n);
  const version = target.kind === 'base' ? 1 : target.n + 1;   // base = v1, revision N = v(N+1)
  const outDir = `jobs/${id}/output/v${version}`;
  // Files the user attached to this change request. Saying so in the prompt is what makes them
  // count: a file sitting in the folder that the run is never told to open is decoration.
  const att = target.kind === 'rev'
    ? ((job.revisions.find(r => r.n === target.n) || {}).attachments || []) : [];
  const prompt = [
    'A request from the Cybele Project Console dashboard is queued — attend it now, fully autonomously, no questions.',
    `Job id: ${id}. Item: ${which} (version v${version}). Request: "${target.text}".`,
    ...(att.length ? [`The user attached ${att.length} file(s) to this change request: ${att.map(a => `jobs/${id}/${a}`).join(', ')}. READ or VIEW every one of them before doing the work — they are part of the request, not background material.`] : []),
    `Follow CLAUDE.md and RUNBOOK.md: read jobs/${id}/job.json and any source file under jobs/${id}/, do the work, and put ALL output for this run in ${outDir}/ (create it; do NOT touch or overwrite any earlier jobs/${id}/output/v* folder). Render a PDF preview inside ${outDir}/ too. Then mark it done by POSTing to http://localhost:3491/jobs/${id} with resultPath and previewPath pointing inside ${outDir}/ (for the base: status/result/resultPath/previewPath; for a revision: update its entry inside the revisions array with status:"done", result, resultPath, previewPath).`,
    'Make reasonable on-brand decisions (Cybele primary #0A74D6). When done, stop.',
  ].join(' ');

  const bin = fs.existsSync(CLAUDE_BIN) ? CLAUDE_BIN : 'claude';
  const logFd = fs.openSync(path.join(JOBS_DIR, id, 'run.log'), 'a');
  fs.writeSync(logFd, `\n===== ${which} · run ${new Date().toISOString()} =====\n`);
  const child = spawn(bin, ['-p', prompt, '--dangerously-skip-permissions'], { cwd: BASE, windowsHide: true, stdio: ['ignore', logFd, logFd] });
  RUNNING[id] = { child, target, stopped: false };
  child.on('error', () => {});
  child.on('exit', (code) => {
    try { fs.closeSync(logFd); } catch (e) {}
    const stopped = RUNNING[id] && RUNNING[id].stopped;
    delete RUNNING[id];
    // If Claude exited without marking the item done, settle the status so the UI doesn't hang.
    try {
      const j2 = readJSON(jf);
      const st = target.kind === 'base' ? j2.status : (j2.revisions.find(r => r.n === target.n) || {}).status;
      if (st === 'running') {
        const newst = stopped ? 'cancelled' : (code === 0 ? 'done' : 'error');
        if (target.kind === 'base') j2.status = newst;
        else j2.revisions.find(r => r.n === target.n).status = newst;
        j2.updatedAt = new Date().toISOString();
        fs.writeFileSync(jf, JSON.stringify(j2, null, 2));
      }
    } catch (e) {}
  });
  return { ok: true, status: 'running', target };
}

// Stop the in-flight run: kill the process tree and mark the running item 'cancelled'.
// Returns the item identity + its prompt so the UI can offer "edit & re-run".
function stopRun(id) {
  const jf = path.join(JOBS_DIR, id, 'job.json');
  if (!fs.existsSync(jf)) return { ok: false, error: 'job not found' };
  const job = readJSON(jf);
  let kind = null, n = null, prompt = '';
  if (job.status === 'running') { kind = 'base'; prompt = job.prompt || ''; }
  else {
    const rr = (job.revisions || []).find(r => r.status === 'running');
    if (rr) { kind = 'rev'; n = rr.n; prompt = rr.prompt || ''; }
  }
  if (!kind) return { ok: false, error: 'nothing running' };
  const entry = RUNNING[id];
  if (entry && entry.child && entry.child.pid) {
    entry.stopped = true;
    try { spawnSync('taskkill', ['/pid', String(entry.child.pid), '/T', '/F'], { windowsHide: true, timeout: 10000 }); }
    catch (e) { try { entry.child.kill(); } catch (e2) {} }
  }
  if (kind === 'base') job.status = 'cancelled';
  else job.revisions.find(r => r.n === n).status = 'cancelled';
  job.updatedAt = new Date().toISOString();
  fs.writeFileSync(jf, JSON.stringify(job, null, 2));
  return { ok: true, kind, n, prompt };
}

// Update an item's prompt and run it again.
function rerunWithPrompt(id, kind, n, prompt) {
  const jf = path.join(JOBS_DIR, id, 'job.json');
  if (!fs.existsSync(jf)) return { ok: false, error: 'job not found' };
  prompt = (prompt || '').trim();
  if (!prompt) return { ok: false, error: 'empty prompt' };
  const job = readJSON(jf);
  if (kind === 'rev') {
    const r = (job.revisions || []).find(x => x.n === n);
    if (!r) return { ok: false, error: 'revision not found' };
    r.prompt = prompt; r.status = 'queued';
  } else {
    job.prompt = prompt; job.status = 'queued';
  }
  job.updatedAt = new Date().toISOString();
  fs.writeFileSync(jf, JSON.stringify(job, null, 2));
  return startQueuedRun(id);
}

// Team-shared, user-created document types (committed in data/).
function loadCustomPipelines() {
  try {
    if (!fs.existsSync(CUSTOM_PIPELINES_FILE)) return [];
    const parsed = readJSON(CUSTOM_PIPELINES_FILE);
    return Array.isArray(parsed.pipelines) ? parsed.pipelines : [];
  } catch (e) { return []; }
}

// Body as text. Collect the raw bytes and decode once: appending chunks to a string decodes them
// as UTF-8 and silently turns anything else into U+FFFD, which cannot be undone. A run records its
// result with the Windows `curl`, which sends the console code page (cp1252) when the text has an
// accent or a dash, so a body that is not valid UTF-8 is read as cp1252 instead of being mangled.
function readBody(req) {
  return new Promise((resolve) => {
    const chunks = [];
    req.on('data', chunk => chunks.push(chunk));
    req.on('end', () => {
      const raw = Buffer.concat(chunks);
      try { resolve(new TextDecoder('utf-8', { fatal: true }).decode(raw)); }
      catch (e) { resolve(new TextDecoder('windows-1252').decode(raw)); }
    });
  });
}

http.createServer(async (req, res) => {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    return res.end();
  }

  // POST endpoint to save base64 screenshot (kept for the capture workflow)
  if (req.method === 'POST' && req.url === '/save-screenshot') {
    const body = await readBody(req);
    try {
      const { data } = JSON.parse(body);
      const base64Data = data.replace(/^data:image\/png;base64,/, '');
      fs.writeFileSync(path.join(BASE, 'dashboard-capture.png'), base64Data, 'base64');
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: true }));
    } catch (e) {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: false, error: e.message }));
    }
    return;
  }

  // GET /run-stream — execute a command and stream stdout/stderr live (SSE)
  if (req.method === 'GET' && req.url.startsWith('/run-stream')) {
    const u = new URL(req.url, 'http://localhost');
    const cmd = (u.searchParams.get('cmd') || '').trim();
    const cwd = (u.searchParams.get('cwd') || BASE).trim();

    res.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    });
    const send = (event, payload) => res.write(`event: ${event}\ndata: ${JSON.stringify(payload)}\n\n`);

    if (!cmd) { send('done', { code: -1, error: 'Empty command' }); return res.end(); }
    if (!fs.existsSync(cwd)) { send('err', { chunk: `Working directory not found:\n${cwd}\n` }); send('done', { code: -1 }); return res.end(); }

    const started = Date.now();
    const child = spawn(cmd, { cwd, shell: true, windowsHide: true });
    const killTimer = setTimeout(() => { child.kill(); send('err', { chunk: '\nProcess timed out after 180s — killed.\n' }); }, 180000);

    child.stdout.on('data', d => send('out', { chunk: d.toString() }));
    child.stderr.on('data', d => send('err', { chunk: d.toString() }));
    child.on('error', e => send('err', { chunk: 'Spawn error: ' + e.message + '\n' }));
    child.on('close', code => {
      clearTimeout(killTimer);
      send('done', { code, ms: Date.now() - started });
      res.end();
    });
    req.on('close', () => { clearTimeout(killTimer); try { child.kill(); } catch (e) {} });
    return;
  }

  // POST /run — execute a pipeline command in a given working directory
  if (req.method === 'POST' && req.url === '/run') {
    const body = await readBody(req);
    let cmd, cwd;
    try {
      const parsed = JSON.parse(body);
      cmd = (parsed.cmd || '').trim();
      cwd = (parsed.cwd || BASE).trim();
    } catch (e) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      return res.end(JSON.stringify({ ok: false, error: 'Invalid JSON body' }));
    }

    if (!cmd) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      return res.end(JSON.stringify({ ok: false, error: 'Empty command' }));
    }
    if (!fs.existsSync(cwd)) {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      return res.end(JSON.stringify({ ok: false, code: -1, stdout: '', stderr: `Working directory not found:\n${cwd}` }));
    }

    const started = Date.now();
    exec(cmd, { cwd, timeout: 180000, windowsHide: true, maxBuffer: 1024 * 1024 * 16 }, (err, stdout, stderr) => {
      const ms = Date.now() - started;
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({
        ok: !err,
        code: err ? (typeof err.code === 'number' ? err.code : 1) : 0,
        killed: err ? !!err.killed : false,
        ms,
        stdout: stdout || '',
        stderr: stderr || (err && err.killed ? 'Process timed out after 180s' : ''),
      }));
    });
    return;
  }

  // GET /pipelines/custom — team-shared, user-created document types
  if (req.method === 'GET' && req.url === '/pipelines/custom') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify({ pipelines: loadCustomPipelines() }));
  }

  // POST /pipelines/custom — replace the custom document-type list (whole-list replace)
  if (req.method === 'POST' && req.url === '/pipelines/custom') {
    const body = await readBody(req);
    try {
      const parsed = JSON.parse(body);
      if (!Array.isArray(parsed.pipelines)) throw new Error('Body must be { pipelines: [...] }');
      if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
      fs.writeFileSync(CUSTOM_PIPELINES_FILE, JSON.stringify({ pipelines: parsed.pipelines }, null, 2));
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: true, count: parsed.pipelines.length }));
    } catch (e) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: false, error: e.message }));
    }
    return;
  }

  // GET /progress-section?pipeline=key — return the relevant progress.md context
  if (req.method === 'GET' && req.url.startsWith('/progress-section')) {
    const u = new URL(req.url, 'http://localhost');
    const pipeline = u.searchParams.get('pipeline') || '';
    const keyword = SECTION_KEYWORDS[pipeline];
    res.writeHead(200, { 'Content-Type': 'application/json' });
    if (!keyword || !fs.existsSync(PROGRESS_FILE)) {
      return res.end(JSON.stringify({ found: false, section: '', source: 'data/progress.md' }));
    }
    try {
      const md = fs.readFileSync(PROGRESS_FILE, 'utf8');
      const section = extractSection(md, keyword);
      res.end(JSON.stringify({ found: !!section, section: section || '', source: 'data/progress.md' }));
    } catch (e) {
      res.end(JSON.stringify({ found: false, section: '', error: e.message }));
    }
    return;
  }

  // GET /jobs — list prepared jobs
  if (req.method === 'GET' && req.url === '/jobs') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify({ jobs: listJobs() }));
  }

  // POST /jobs — create a prepared job (source doc + prompt + pipeline context)
  if (req.method === 'POST' && req.url === '/jobs') {
    const body = await readBody(req);
    try {
      const parsed = JSON.parse(body);
      const pipeline = (parsed.pipeline || '').trim();
      const prompt = (parsed.prompt || '').trim();
      const title = (parsed.title || '').trim();
      if (!pipeline) throw new Error('Missing pipeline');
      if (!fs.existsSync(JOBS_DIR)) fs.mkdirSync(JOBS_DIR, { recursive: true });

      const id = 'task-' + Date.now();
      const dir = path.join(JOBS_DIR, id);
      fs.mkdirSync(dir, { recursive: true });

      let sourceFile = null;
      if (parsed.filename && parsed.dataBase64) {
        sourceFile = path.basename(parsed.filename);
        const b64 = String(parsed.dataBase64).replace(/^data:[^;]+;base64,/, '');
        fs.writeFileSync(path.join(dir, sourceFile), b64, 'base64');
      }

      // Per-pipeline knobs picked in the launcher (e.g. blog: { coverBrief, sectionImages, outputs }).
      // Stored as-is so the run can read them from job.json; the prompt states them too.
      const opts = parsed.options;
      const options = (opts && typeof opts === 'object' && !Array.isArray(opts)) ? opts : null;

      const job = {
        id, pipeline, title, prompt, sourceFile,
        ...(options ? { options } : {}),
        status: 'queued',
        createdAt: new Date().toISOString(),
      };
      fs.writeFileSync(path.join(dir, 'job.json'), JSON.stringify(job, null, 2));
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: true, id, job }));
    } catch (e) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: false, error: e.message }));
    }
    return;
  }

  // GET /source — content-source config + last sync status
  if (req.method === 'GET' && req.url === '/source') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify(sourceInfo()));
  }

  // POST /sync — mirror progress.md + brand from the repo into the local cache (uses git's own auth)
  if (req.method === 'POST' && req.url === '/sync') {
    const r = syncFromGitHub();
    res.writeHead(r.ok ? 200 : 502, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify(r));
  }

  // GET /thumb?path=<rel> — small preview image: images served directly, PDFs rasterised (page 1,
  // cached as <file>.thumb.png via PyMuPDF). Used by the task cards / mosaic.
  if (req.method === 'GET' && req.url.split('?')[0] === '/thumb') {
    try {
      const u = new URL(req.url, 'http://localhost');
      const rel = decodeURIComponent(u.searchParams.get('path') || '').replace(/^\/+/, '');
      const abs = path.normalize(path.join(BASE, rel));
      if (!abs.startsWith(path.normalize(BASE))) throw new Error('bad path');
      if (!fs.existsSync(abs)) throw new Error('not found');
      const ext = path.extname(abs).slice(1).toLowerCase();
      if (IMG_EXTS.includes(ext)) {
        res.writeHead(200, { 'Content-Type': MIME_TYPES['.' + ext] || 'image/png', 'Cache-Control': 'no-cache' });
        return res.end(fs.readFileSync(abs));
      }
      if (ext === 'pdf') {
        const scale = Math.max(0.4, Math.min(3, parseFloat(u.searchParams.get('scale')) || 0.7));
        const page = Math.max(0, parseInt(u.searchParams.get('page')) || 0);
        const thumb = await renderPdfThumb(abs, scale, page);
        if (!thumb) throw new Error('render failed');
        res.writeHead(200, { 'Content-Type': 'image/png', 'Cache-Control': 'no-cache' });
        return res.end(fs.readFileSync(thumb));
      }
      throw new Error('unsupported');
    } catch (e) {
      res.writeHead(404, { 'Content-Type': 'text/plain' });
      return res.end('');
    }
  }

  // GET /pdfinfo?path=<rel> — page count for a deliverable (PDFs via PyMuPDF; non-PDF → 1).
  // Used by the Annotate view to page through a multi-page document one page at a time.
  if (req.method === 'GET' && req.url.split('?')[0] === '/pdfinfo') {
    try {
      const u = new URL(req.url, 'http://localhost');
      const rel = decodeURIComponent(u.searchParams.get('path') || '').replace(/^\/+/, '');
      const abs = path.normalize(path.join(BASE, rel));
      if (!abs.startsWith(path.normalize(BASE)) || !fs.existsSync(abs)) throw new Error('bad path');
      let pages = 1;
      if (path.extname(abs).slice(1).toLowerCase() === 'pdf') {
        const r = await runPy(['-c', `import pymupdf as fitz;print(fitz.open(r'''${abs}''').page_count)`], { timeout: 30000 });
        const n = parseInt((r.stdout || '').trim()); if (n) pages = n;
      }
      res.writeHead(200, { 'Content-Type': 'application/json' });
      return res.end(JSON.stringify({ pages }));
    } catch (e) {
      res.writeHead(404, { 'Content-Type': 'application/json' });
      return res.end(JSON.stringify({ pages: 1 }));
    }
  }

  // GET /style-tokens — every editable style value, grouped by document type
  if (req.method === 'GET' && req.url === '/style-tokens') {
    const specs = STYLE_SPECS.map(spec => ({
      key: spec.key, label: spec.label, external: spec.external || null,
      files: spec.files.map(f => {
        const abs = path.normalize(path.join(BASE, f.rel));
        if (!fs.existsSync(abs)) return { rel: f.rel, label: f.label, path: f.rel.replace(/^\.\.\//, ''), found: false, tokens: [] };
        const parsed = parseStyleTokens(abs, f.section);
        return { rel: f.rel, label: f.label, path: f.rel.replace(/^\.\.\//, ''),
                 section: f.section || null, mirrored: !!f.mirrored,
                 found: parsed !== null, tokens: (parsed && parsed.tokens) || [],
                 tables: (parsed && parsed.tables) || [],
                 modes: (parsed && parsed.modes) || [] };
      }),
    }));
    // Never cached: the editor re-reads this right after a save, and a stale copy would look
    // like the save was lost.
    res.writeHead(200, { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' });
    return res.end(JSON.stringify({ specs }));
  }

  // POST /style-tokens — apply edits in place ({ edits: [{spec, rel, line, occ, kind, from, to}] })
  if (req.method === 'POST' && req.url === '/style-tokens') {
    const body = await readBody(req);
    try {
      const all = JSON.parse(body).edits || [];
      const applied = [], skipped = [];
      const edits = all.filter(e => {
        const k = STYLE_KINDS.find(x => x.kind === e.kind);
        if (k && k.ok(String(e.to || '').trim())) return true;
        skipped.push('not a valid ' + (e.kind || 'value') + ': ' + JSON.stringify(e.to));
        return false;
      });
      const byFile = new Map();
      for (const e of edits) {
        const hit = styleSpecFile(e.spec, e.rel);
        if (!hit || !fs.existsSync(hit.abs)) { skipped.push(e.rel + ': file not found'); continue; }
        if (!byFile.has(hit.abs)) byFile.set(hit.abs, []);
        byFile.get(hit.abs).push(e);
      }
      for (const [abs, list] of byFile) {
        const lines = fs.readFileSync(abs, 'utf8').split(/\r?\n/);
        let touched = false;
        for (const e of list) {
          const line = lines[e.line];
          const k = STYLE_KINDS.find(x => x.kind === e.kind);
          if (line === undefined || !k) { skipped.push(path.basename(abs) + ' line ' + e.line + ': gone'); continue; }
          let n = -1, ok = false;
          const next = line.replace(new RegExp(k.re.source, 'g'), m => {
            n++;
            if (n !== e.occ) return m;
            // The file must still hold what the client was shown, or the edit is stale.
            if (m.toLowerCase() !== String(e.from).toLowerCase()) return m;
            ok = true; return String(e.to).trim();
          });
          if (!ok) { skipped.push(path.basename(abs) + ' line ' + (e.line + 1) + ': expected ' + e.from + ', file changed'); continue; }
          lines[e.line] = next; touched = true;
          applied.push(path.basename(abs) + ':' + (e.line + 1) + ' ' + e.from + ' -> ' + e.to);
        }
        if (touched) fs.writeFileSync(abs, lines.join('\n'));
      }
      res.writeHead(200, { 'Content-Type': 'application/json' });
      return res.end(JSON.stringify({ ok: skipped.length === 0, applied: applied.length, skipped }));
    } catch (e) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      return res.end(JSON.stringify({ ok: false, error: e.message }));
    }
  }

  // POST /style-modes — add or remove a mode in a spec file ({ spec, rel, op, name, description,
  // copyFrom }). A mode is not just a row in the Modes table: every element that varies by mode has
  // a column per mode, so adding one has to add that column everywhere. A new column is seeded from
  // an existing mode rather than left blank — an empty cell is not a value the editor can offer,
  // and "copy then adjust" is how a designer actually builds a variant.
  if (req.method === 'POST' && req.url === '/style-modes') {
    const body = await readBody(req);
    try {
      const p = JSON.parse(body);
      const hit = styleSpecFile(p.spec, p.rel);
      if (!hit || !fs.existsSync(hit.abs)) throw new Error('spec file not found');
      const name = String(p.name || '').trim();
      if (!/^[A-Za-z][A-Za-z0-9 _-]{0,23}$/.test(name)) throw new Error('a mode name is 1-24 letters, digits, spaces, - or _');
      const op = ['delete', 'describe'].includes(p.op) ? p.op : 'add';
      const modes = parseStyleModes(hit.abs);
      const exists = modes.find(m => m.name.toLowerCase() === name.toLowerCase());
      if (op === 'add' && exists) throw new Error('there is already a mode called ' + exists.name);
      if (op !== 'add' && !exists) throw new Error('no mode called ' + name);

      // Describing a mode touches one cell: the registry row is the only place it is written.
      if (op === 'describe') {
        const lines = fs.readFileSync(hit.abs, 'utf8').split(/\r?\n/);
        const cs = lines[exists.line].trim().split('|').slice(1, -1).map(c => c.trim());
        cs[1] = String(p.description || '').trim() || 'No description yet.';
        lines[exists.line] = '| ' + cs.join(' | ') + ' |';
        fs.writeFileSync(hit.abs, lines.join('\n'));
        res.writeHead(200, { 'Content-Type': 'application/json' });
        return res.end(JSON.stringify({ ok: true, op, name }));
      }
      if (op === 'delete' && modes.length <= 1) throw new Error('a spec needs at least one mode');

      const src = op === 'add'
        ? (modes.find(m => m.name.toLowerCase() === String(p.copyFrom || '').toLowerCase()) || modes[0])
        : null;
      if (op === 'add' && !src) throw new Error('nothing to copy the new mode from');

      const lines = fs.readFileSync(hit.abs, 'utf8').split(/\r?\n/);
      const cells = l => l.trim().split('|').slice(1, -1).map(c => c.trim());
      const build = cs => '| ' + cs.join(' | ') + ' |';
      // The separator row has its own compact style in these files; rebuilding it like a data row
      // would rewrite every table cosmetically and bury the real change in a diff.
      const buildSep = n => '|' + Array(n).fill('---').join('|') + '|';
      const parsed = parseStyleTokens(hit.abs, null) || { tables: [] };
      let touchedTables = 0;

      // Bottom-up, so a rewrite never moves a line another edit still points at.
      const tables = (parsed.tables || []).slice().sort((a, b) => b.headerLine - a.headerLine);
      for (const tb of tables) {
        const header = cells(lines[tb.headerLine]);
        const idx = header.map((h, i) => ({ h, i }))
          .filter(({ h }) => splitModeColumn(h, modes).mode);
        if (!idx.length) continue;
        const forMode = m => idx.filter(({ h }) => (splitModeColumn(h, modes).mode || '').toLowerCase() === m.toLowerCase());
        if (op === 'delete') {
          const drop = new Set(forMode(name).map(x => x.i));
          if (!drop.size) continue;
          const keep = cs => cs.filter((c, i) => !drop.has(i));
          lines[tb.headerLine] = build(keep(header));
          lines[tb.sepLine] = buildSep(keep(cells(lines[tb.sepLine])).length);
          tb.rows.forEach(r => { lines[r] = build(keep(cells(lines[r]))); });
          touchedTables++;
        } else {
          const from = forMode(src.name);
          if (!from.length) continue;
          const at = Math.max(...from.map(x => x.i)) + 1;      // the new mode sits after the copied one
          const newHead = from.map(({ h }) => {
            const prop = splitModeColumn(h, modes).prop;
            return prop ? name + ' · ' + prop : name;
          });
          const insert = (cs, vals) => cs.slice(0, at).concat(vals, cs.slice(at));
          lines[tb.headerLine] = build(insert(header, newHead));
          lines[tb.sepLine] = buildSep(cells(lines[tb.sepLine]).length + from.length);
          tb.rows.forEach(r => {
            const cs = cells(lines[r]);
            lines[r] = build(insert(cs, from.map(({ i }) => cs[i] !== undefined ? cs[i] : '')));
          });
          touchedTables++;
        }
      }

      // Some tables carry the modes as rows instead of columns — a list of accents per mode, say.
      // A mode that gained a column everywhere but no row here would exist with no accents allowed.
      for (const tb of tables) {
        if (/^modes$/i.test(tb.heading || '')) continue;      // the registry itself, handled below
        const rowMode = r => {
          const cs = cells(lines[r]);
          return cs.length ? splitModeColumn(cs[0], modes).mode : null;
        };
        const rows = (tb.rows || []).filter(r => rowMode(r));
        if (!rows.length) continue;
        if (op === 'delete') {
          const gone = rows.filter(r => (rowMode(r) || '').toLowerCase() === name.toLowerCase());
          if (!gone.length) continue;
          gone.sort((a, b) => b - a).forEach(r => lines.splice(r, 1));
          touchedTables++;
        } else {
          const from = rows.find(r => (rowMode(r) || '').toLowerCase() === src.name.toLowerCase());
          if (from === undefined) continue;
          const cs = cells(lines[from]);
          // Keep the label's shape: "Light mode" copies to "Sepia mode", "Light" to "Sepia".
          cs[0] = cs[0].replace(new RegExp(src.name, 'i'), name);
          lines.splice(from + 1, 0, build(cs));
          touchedTables++;
        }
      }

      // The registry row itself, last: the table rewrites above were computed against it.
      // Re-find them: inserting or dropping rows above may have moved the registry.
      const isRegRow = (l, who) => {
        const t = String(l || '').trim();
        if (!(t.startsWith('|') && t.endsWith('|'))) return false;
        return cells(t)[0].toLowerCase() === who.toLowerCase();
      };
      if (op === 'delete') {
        const at = lines.findIndex((l, i) => i >= 0 && isRegRow(l, name));
        if (at < 0) throw new Error('the Modes table changed while writing');
        lines.splice(at, 1);
      } else {
        const last = modes[modes.length - 1].name;
        let at = -1;
        for (let i = 0; i < lines.length; i++) if (isRegRow(lines[i], last)) { at = i; break; }
        if (at < 0) throw new Error('the Modes table changed while writing');
        // The registry row carries the mode's own values too — the accents it allows. Copy the
        // source mode's row and change the name and the description, so a new mode is never born
        // with an empty cell the editor cannot offer anything for.
        let from = -1;
        for (let i = 0; i < lines.length; i++) if (isRegRow(lines[i], src.name)) { from = i; break; }
        const base = from >= 0 ? cells(lines[from]) : [src.name, ''];
        base[0] = name;
        base[1] = String(p.description || '').trim() || 'No description yet.';
        lines.splice(at + 1, 0, build(base));
      }
      fs.writeFileSync(hit.abs, lines.join('\n'));
      res.writeHead(200, { 'Content-Type': 'application/json' });
      return res.end(JSON.stringify({ ok: true, op, name, tables: touchedTables }));
    } catch (e) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      return res.end(JSON.stringify({ ok: false, error: e.message }));
    }
  }

  // GET/POST /style-elements — the element names and descriptions the editor groups by
  // ({ "<spec>|<element key>": { name, description } }). Renaming two keys to the same name merges
  // them, which is how "Titles" and "Title" become one element.
  if (req.method === 'GET' && req.url === '/style-elements') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify(fs.existsSync(STYLE_ELEMENTS) ? readJSON(STYLE_ELEMENTS) : {}));
  }
  if (req.method === 'POST' && req.url === '/style-elements') {
    const body = await readBody(req);
    try {
      const p = JSON.parse(body);
      const map = fs.existsSync(STYLE_ELEMENTS) ? readJSON(STYLE_ELEMENTS) : {};
      const key = String(p.key || '').slice(0, 300);
      if (!key) throw new Error('missing key');
      const entry = Object.assign({}, map[key]);
      if (p.name !== undefined) entry.name = String(p.name).slice(0, 80);
      if (p.description !== undefined) entry.description = String(p.description).slice(0, 400);
      if (!entry.name && !entry.description) delete map[key]; else map[key] = entry;
      if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
      fs.writeFileSync(STYLE_ELEMENTS, JSON.stringify(map, null, 2));
      res.writeHead(200, { 'Content-Type': 'application/json' });
      return res.end(JSON.stringify({ ok: true }));
    } catch (e) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      return res.end(JSON.stringify({ ok: false, error: e.message }));
    }
  }

  // GET/POST /style-notes — plain-language descriptions for the style rules, so someone opening the
  // editor for the first time knows what "Category label" is. Kept beside the console (they explain
  // the rules to people; the specs themselves stay the rules).
  if (req.method === 'GET' && req.url === '/style-notes') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify(fs.existsSync(STYLE_NOTES) ? readJSON(STYLE_NOTES) : {}));
  }
  if (req.method === 'POST' && req.url === '/style-notes') {
    const body = await readBody(req);
    try {
      const p = JSON.parse(body);
      const notes = fs.existsSync(STYLE_NOTES) ? readJSON(STYLE_NOTES) : {};
      const key = String(p.key || '').slice(0, 300);
      if (!key) throw new Error('missing key');
      if (p.text) notes[key] = String(p.text).slice(0, 400); else delete notes[key];
      if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
      fs.writeFileSync(STYLE_NOTES, JSON.stringify(notes, null, 2));
      res.writeHead(200, { 'Content-Type': 'application/json' });
      return res.end(JSON.stringify({ ok: true }));
    } catch (e) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      return res.end(JSON.stringify({ ok: false, error: e.message }));
    }
  }

  // POST /style-row — add or remove a whole rule row in a spec ({ op, spec, rel, ... }).
  // Deleting drops a rule from the system, so the client must send the exact line it saw.
  if (req.method === 'POST' && req.url === '/style-row') {
    const body = await readBody(req);
    try {
      const p = JSON.parse(body);
      const hit = styleSpecFile(p.spec, p.rel);
      if (!hit || !fs.existsSync(hit.abs)) throw new Error('file not found');
      const lines = fs.readFileSync(hit.abs, 'utf8').split(/\r?\n/);
      if (p.op === 'delete') {
        // One rule, or every rule of an element. Several lines are removed bottom-up in one pass so
        // the earlier indexes stay valid, and each is checked against what the client was shown.
        const targets = Array.isArray(p.lines) && p.lines.length ? p.lines : [{ line: p.line, expect: p.expect }];
        for (const tgt of targets) {
          if (lines[tgt.line] === undefined) throw new Error('line is gone');
          if (lines[tgt.line].trim() !== String(tgt.expect || '').trim()) throw new Error('the file changed since you opened it');
        }
        [...targets].sort((a, b) => b.line - a.line).forEach(tgt => lines.splice(tgt.line, 1));
      } else if (p.op === 'relabel') {
        // Rename the rule in the specification itself, on every line where it appears — a table row
        // is named by its first cell, a bullet by the words before its colon. Renaming only the
        // console label would leave the file saying one thing and the editor another.
        const to = String(p.to || '').trim();
        if (!to) throw new Error('a rule needs a name');
        if (/[|`*\r\n]/.test(to)) throw new Error('a name cannot contain | ` or *');
        const targets = p.lines || [];
        if (!targets.length) throw new Error('nothing to rename');
        for (const tgt of targets) {
          if (lines[tgt.line] === undefined) throw new Error('line is gone');
          if (lines[tgt.line].trim() !== String(tgt.expect || '').trim()) throw new Error('the file changed since you opened it');
        }
        for (const tgt of targets) {
          const line = lines[tgt.line], t = line.trim();
          if (t.startsWith('|') && t.endsWith('|')) {
            const parts = line.split('|');
            parts[1] = ' ' + to + ' ';
            lines[tgt.line] = parts.join('|');
          } else {
            const from = String(tgt.from || '');
            const at = line.indexOf(from), colon = line.indexOf(':');
            if (!from || at < 0 || (colon >= 0 && at > colon)) continue;   // not the naming part of the line
            lines[tgt.line] = line.slice(0, at) + to + line.slice(at + from.length);
          }
        }
      } else if (p.op === 'add') {
        const cells = (p.cells || []).map(c => String(c).replace(/\|/g, '/').trim());
        if (!cells.length || !cells[0]) throw new Error('a row needs at least a name');
        const at = Math.min(Math.max(0, (p.afterLine | 0) + 1), lines.length);
        lines.splice(at, 0, '| ' + cells.join(' | ') + ' |');
      } else if (p.op === 'setcell') {
        // Replace one cell wholesale. Switching a background between a colour and `none` changes
        // what kind of value the cell holds, which a value-level edit cannot express.
        const li = p.line | 0, ci = p.cell | 0;
        if (lines[li] === undefined) throw new Error('line is gone');
        if (String(p.expect || '').trim() && lines[li].trim() !== String(p.expect).trim())
          throw new Error('the file changed since you opened it');
        const text = String(p.text == null ? '' : p.text).replace(/[|\r\n]/g, '').trim();
        if (!text) throw new Error('a cell needs a value');
        const cs = lines[li].trim().split('|').slice(1, -1).map(c => c.trim());
        if (cs[ci] === undefined || ci === 0) throw new Error('no such column');
        cs[ci] = text;
        lines[li] = '| ' + cs.join(' | ') + ' |';
      } else if (p.op === 'valdel' || p.op === 'valadd') {
        // A cell can hold a list — the accents a mode allows. Removing a rule row would drop the
        // whole list, so these two ops work on one value inside the cell.
        const li = p.line | 0;
        if (lines[li] === undefined) throw new Error('line is gone');
        if (String(p.expect || '').trim() && lines[li].trim() !== String(p.expect).trim())
          throw new Error('the file changed since you opened it');
        const k = STYLE_KINDS.find(x => x.kind === p.kind);
        if (!k) throw new Error('unknown kind');
        if (p.op === 'valdel') {
          let n = -1, ok = false;
          // Take the backticks around it too, or the cell keeps an empty pair of them.
          const re = new RegExp('`?\\s*(?:' + k.re.source + ')\\s*`?', 'g');
          let next = lines[li].replace(re, m => {
            n++;
            if (n !== (p.occ | 0)) return m;
            if (!m.includes(String(p.value))) return m;
            ok = true; return '';
          });
          if (!ok) throw new Error('expected ' + p.value + ', file changed');
          next = next.replace(/[ \t]{2,}/g, ' ').replace(/\|\s+\|/g, '| |');
          const cs = next.trim().split('|').slice(1, -1).map(c => c.trim());
          if (!cs.some(c => new RegExp(k.re.source).test(c))) throw new Error('a rule cannot be left with no value');
          lines[li] = '| ' + cs.join(' | ') + ' |';
        } else {
          const val = String(p.value || '').trim();
          if (!k.ok(val)) throw new Error('not a valid ' + p.kind + ': ' + val);
          const ci = p.cell | 0;
          const cs = lines[li].trim().split('|').slice(1, -1).map(c => c.trim());
          if (cs[ci] === undefined) throw new Error('no such column');
          const ticked = /`/.test(cs[ci]);
          cs[ci] = (cs[ci] + ' ' + (ticked ? '`' + val + '`' : val)).trim();
          lines[li] = '| ' + cs.join(' | ') + ' |';
        }
      } else throw new Error('unknown op');
      fs.writeFileSync(hit.abs, lines.join('\n'));
      res.writeHead(200, { 'Content-Type': 'application/json' });
      return res.end(JSON.stringify({ ok: true }));
    } catch (e) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      return res.end(JSON.stringify({ ok: false, error: e.message }));
    }
  }

  // GET /events — a channel the console keeps open. The server pushes `jobs` when anything under
  // jobs/ changes: a run starting, finishing, or asking for a decision. No polling on either side.
  if (req.method === 'GET' && req.url.split('?')[0] === '/events') {
    res.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
      'X-Accel-Buffering': 'no',
    });
    res.write('retry: 3000\n\n');
    res.write('event: hello\ndata: {}\n\n');
    sseClients.add(res);
    watchJobs();
    // A comment every 25s so an idle connection is not dropped as dead.
    const beat = setInterval(() => { try { res.write(': beat\n\n'); } catch (e) {} }, 25000);
    req.on('close', () => { clearInterval(beat); sseClients.delete(res); });
    return;
  }

  // GET /run-visuals?path=<rel> — every design in the run, in order, each with the article section
  // it illustrates. The preview shows these instead of handing one raw file to an iframe: a
  // 1920×1080 SVG in an iframe renders at native size, so the user scrolls a giant first image and
  // never learns the other visuals exist.
  //
  // Titles come from `visuals.json` in the run folder when the run wrote one (exact section titles);
  // otherwise they are read back out of the filename, which the skill builds from the section title.
  if (req.method === 'GET' && req.url.split('?')[0] === '/run-visuals') {
    const out = { folder: '', visuals: [] };
    try {
      const u = new URL(req.url, 'http://localhost');
      const rel = decodeURIComponent(u.searchParams.get('path') || '').replace(/^\/+/, '');
      const abs = path.normalize(path.join(BASE, rel));
      if (!abs.startsWith(path.normalize(BASE))) throw new Error('bad path');
      const folder = deliverableFolder(abs);
      out.folder = path.relative(BASE, folder).replace(/\\/g, '/');

      // A manifest is authoritative: it carries the real section titles, and a Figma-only run has
      // no image files to find at all.
      let manifest = null;
      try {
        const mf = path.join(folder, 'visuals.json');
        if (fs.existsSync(mf)) {
          const m = readJSON(mf);
          manifest = Array.isArray(m) ? m : (Array.isArray(m && m.visuals) ? m.visuals : null);
        }
      } catch (e) {}

      const relUrl = p => '/' + path.relative(BASE, p).replace(/\\/g, '/').split('/').map(encodeURIComponent).join('/');
      // section_02_four-steps-to-tap-and-go.svg → { kind: section, n: 2, title: "Four steps to tap and go" }
      const fromName = file => {
        const base = path.basename(file).replace(/\.[^.]+$/, '');
        const m = base.match(/^(cover|section)[_-](\d+)[_-](.+)$/i);
        const words = s => s.replace(/[_-]+/g, ' ').trim().replace(/\s+/g, ' ')
          .replace(/^./, c => c.toUpperCase());
        if (!m) return { kind: '', n: 0, title: words(base) };
        return { kind: m[1].toLowerCase(), n: parseInt(m[2], 10), title: words(m[3]) };
      };

      if (manifest) {
        for (const v of manifest) {
          const file = String(v.file || v.path || '');
          let url = '', p = '';
          if (file) {
            p = path.normalize(path.join(folder, file));
            if (p.startsWith(path.normalize(folder)) && fs.existsSync(p)) url = relUrl(p);
          }
          const guess = file ? fromName(file) : { kind: '', n: 0, title: '' };
          // Placement: where in the article this image goes. Accepted as { placement: {where,text} }
          // or as a flat `after` / `before` string. This is the thing the person laying out the post
          // needs — not the layout pattern the generator happened to use.
          const pl = v.placement || {};
          let place = String(pl.where || (v.after ? 'after' : v.before ? 'before' : '')).toLowerCase();
          let anchor = String(pl.text || v.after || v.before || '');
          if (!place && String(v.kind || guess.kind) === 'cover') place = 'top';
          if (!['after', 'before', 'top'].includes(place)) place = anchor ? 'after' : '';
          out.visuals.push({
            url, file: file ? file.replace(/\\/g, '/') : '',
            kind: String(v.kind || guess.kind || ''),
            n: Number(v.n || guess.n || 0),
            title: String(v.title || v.section || guess.title || ''),
            place, anchor,
            meta: String(v.meta || v.note || ''),
            figma: String(v.figma || v.figmaUrl || ''),
          });
        }
      } else {
        // No manifest: the designs are the full-canvas vectors, plus rasters that a visual run
        // named as a visual. A raster is only claimed when it is named `cover_NN` / `section_NN` —
        // a chart dropped beside a whitepaper PDF is an ingredient, and must not take over the
        // preview of a run whose deliverable is the document.
        const svgs = listVectorSvgs(folder);
        const stem = p => path.basename(p).replace(/\.[^.]+$/, '').toLowerCase();
        const seen = new Set(svgs.map(stem));
        let rasters = [];
        try {
          rasters = fs.readdirSync(folder, { recursive: true })
            .filter(f => /\.(png|jpe?g)$/i.test(f) && !/\.thumb\./i.test(f)
                      && /^(cover|section)[_-]\d+/i.test(path.basename(f)))
            .map(f => path.join(folder, f))
            .filter(p => !seen.has(stem(p)))
            .sort();
        } catch (e) {}
        const files = svgs.concat(rasters);
        for (const p of files) {
          const g = fromName(p);
          out.visuals.push({
            url: relUrl(p), file: path.relative(folder, p).replace(/\\/g, '/'),
            kind: g.kind, n: g.n, title: g.title,
            place: g.kind === 'cover' ? 'top' : '', anchor: '',   // no manifest → no placement to show
            meta: '', figma: '',
          });
        }
      }
      // Covers first, then sections in article order, then anything unnamed — the order they are used in.
      const rank = k => k === 'cover' ? 0 : k === 'section' ? 1 : 2;
      out.visuals.sort((a, b) => rank(a.kind) - rank(b.kind) || a.n - b.n || a.file.localeCompare(b.file));
    } catch (e) { out.error = e.message; }
    res.writeHead(200, { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' });
    res.end(JSON.stringify(out));
    return;
  }

  // GET /formats?path=<rel> — which download formats a deliverable truly supports. Vector formats
  // (svg/editable-pdf/pptx) require real vector SVGs in the folder (else they'd be camouflaged
  // rasters). png/jpg also work from any raster; pptx also from an existing deck.
  if (req.method === 'GET' && req.url.split('?')[0] === '/formats') {
    try {
      const u = new URL(req.url, 'http://localhost');
      const rel = decodeURIComponent(u.searchParams.get('path') || '').replace(/^\/+/, '');
      const abs = path.normalize(path.join(BASE, rel));
      if (!abs.startsWith(path.normalize(BASE))) throw new Error('bad path');
      const folder = deliverableFolder(abs);
      let files = []; try { files = fs.readdirSync(folder, { recursive: true }); } catch (e) {}
      const has = ext => abs.toLowerCase().endsWith('.' + ext) || files.some(f => f.toLowerCase().endsWith('.' + ext) && !/\.thumb\./i.test(f));
      const vecCount = listVectorSvgs(folder).length;
      const vector = vecCount > 0, hasPdf = has('pdf'), hasImg = has('png') || has('jpg') || has('jpeg');
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ svg: vector, pdf: vector || hasPdf, png: vector || hasPdf || hasImg,
        jpg: vector || hasPdf || hasImg, pptx: vector || has('pptx'), vectorCount: vecCount }));
    } catch (e) {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ svg: false, pdf: false, png: false, jpg: false, pptx: false, vectorCount: 0 }));
    }
    return;
  }

  // GET /export?svg=&raster=&path=&fmt=&bg=&layout=&pages=&scale= — export a deliverable. SVG is the
  // editable base (fmt=svg → inlined vector; png/jpg/pdf → rendered from the SVG by headless
  // Chrome). PPTX/Whitepaper have no SVG → the PDF preview (raster) is used via PyMuPDF. Returns
  // the file (or a .zip for multiple pages) as an attachment. Conversion done by export_doc.py.
  if (req.method === 'GET' && req.url.split('?')[0] === '/export') {
    let tmp = null;
    try {
      const u = new URL(req.url, 'http://localhost');
      const resolve = key => {
        const rel = decodeURIComponent(u.searchParams.get(key) || '').replace(/^\/+/, '');
        if (!rel) return '';
        const abs = path.normalize(path.join(BASE, rel));
        if (!abs.startsWith(path.normalize(BASE)) || !fs.existsSync(abs)) return '';
        return abs;
      };
      let svg = resolve('svg'); const raster = resolve('raster'); const pathArg = resolve('path');
      if (!svg && !raster && !pathArg) throw new Error('bad path');
      const fmt = ['png', 'jpg', 'svg', 'pdf', 'pptx'].includes(u.searchParams.get('fmt')) ? u.searchParams.get('fmt') : 'png';
      // Vector formats (svg/pdf/png/jpg/pptx) must be built from the deliverable's REAL vector SVGs
      // when they exist — one file per design. This keeps SVG editable (Figma layers), PDF a true
      // multi-page vector doc, and PPTX slides real editable SVG graphics. Never rasterise a PDF into
      // an <image>-wrapped SVG / image-page PDF / image-per-slide PPTX. Raster-only deliverables fall
      // back to the PDF/image source (PyMuPDF) for png/jpg/pdf as before.
      // The whole design set wins over the single file named in resultPath: that file is just the
      // task's thumbnail, so honouring it alone is what made "All pages" download one image.
      // The pages/selection choice is applied over this same set, in the same order.
      const folder = deliverableFolder(svg, raster, pathArg);
      if (['svg', 'pdf', 'png', 'jpg', 'pptx'].includes(fmt) && folder) {
        const vecs = listVectorSvgs(folder);
        if (vecs.length > 1 || (!svg && vecs.length)) svg = vecs.join('\n');
      }
      if (fmt === 'pptx' && !svg) throw new Error('No vector designs available to build an editable PPTX');
      const bg = u.searchParams.get('bg') === 'transparent' ? 'transparent' : 'opaque';
      const layout = u.searchParams.get('layout') === 'pages' ? 'pages' : 'canvas';
      const pages = (u.searchParams.get('pages') || 'all').replace(/[^0-9,\-all\s]/gi, '').slice(0, 200) || 'all';
      const scale = Math.max(0.5, Math.min(4, parseFloat(u.searchParams.get('scale')) || 2));
      const maxbytes = Math.max(0, Math.min(50e6, parseInt(u.searchParams.get('maxbytes')) || 0));
      // Generic name for a whole-run download ("blog-visuals.zip"), from the document type.
      const setName = (u.searchParams.get('name') || '').toLowerCase().replace(/[^a-z0-9-]/g, '').slice(0, 60);
      tmp = path.join(BASE, 'data', 'export-tmp', String(Date.now()) + '-' + Math.floor(Math.random() * 1e6));
      fs.mkdirSync(tmp, { recursive: true });
      const r = await runPy([path.join(BASE, 'export_doc.py'), '--svg', svg, '--raster', raster, '--fmt', fmt, '--bg', bg, '--layout', layout, '--pages', pages, '--scale', String(scale), '--maxbytes', String(maxbytes), '--name', setName, '--out', tmp], { timeout: fmt === 'pptx' ? 240000 : 120000 });
      const line = (r.stdout || '').trim().split('\n').filter(Boolean).pop() || '{}';
      const out = JSON.parse(line);
      // Surface what Python actually said: an unusable interpreter used to read as 'conversion failed'.
      if (!out.ok || !out.file || !fs.existsSync(out.file)) throw new Error(out.error || lastLine(r.stderr) || 'conversion failed');
      const MT = { png: 'image/png', jpg: 'image/jpeg', jpeg: 'image/jpeg', svg: 'image/svg+xml', pdf: 'application/pdf', zip: 'application/zip', pptx: 'application/vnd.openxmlformats-officedocument.presentationml.presentation' };
      const oext = path.extname(out.file).slice(1).toLowerCase();
      const data = fs.readFileSync(out.file);
      res.writeHead(200, { 'Content-Type': MT[oext] || 'application/octet-stream', 'Content-Disposition': 'attachment; filename="' + out.name.replace(/"/g, '') + '"', 'Content-Length': data.length });
      res.end(data);
    } catch (e) {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: false, error: e.message }));
    } finally {
      if (tmp) { try { fs.rmSync(tmp, { recursive: true, force: true }); } catch (e) {} }
    }
    return;
  }

  // POST /icons/rebuild — download the icon set from the Cybele Design System in Figma
  // (sync-figma-icons.js -> data/icons-figma/), then regenerate brand-icon-lib.js from it plus the
  // icons that exist only in the older Cybfont source set. Runs async: a Figma sync takes a while.
  if (req.method === 'POST' && req.url.split('?')[0] === '/icons/rebuild') {
    const runNode = (script, timeout) => new Promise(resolve => {
      const p = spawn(process.execPath, [path.join(BASE, script)], { cwd: BASE, windowsHide: true });
      let out = '', err = '';
      const timer = setTimeout(() => { err += 'timed out'; p.kill(); }, timeout);
      p.stdout.on('data', d => out += d); p.stderr.on('data', d => err += d);
      p.on('close', code => { clearTimeout(timer); resolve({ code, out, err }); });
      p.on('error', e => { clearTimeout(timer); resolve({ code: -1, out, err: e.message }); });
    });
    const lastJson = s => { try { return JSON.parse(s.trim().split('\n').pop()); } catch (e) { return {}; } };
    // Without a token (the usual case: Nick chose "plan B", 2026-09-28) there is no download here —
    // Claude brings Figma changes into data/icons-figma/ with figma-icons-claude.js (RUNBOOK.md), and
    // this just rebuilds the library from that folder and says when it was last synced.
    const hasToken = !!process.env.FIGMA_TOKEN || (() => {
      try { return !!fs.readFileSync(path.join(BASE, 'data', 'figma-token.txt'), 'utf8').trim(); } catch (e) { return false; }
    })();
    (async () => {
      let s = {};
      if (hasToken) {
        const sync = await runNode('sync-figma-icons.js', 300000);
        if (sync.code !== 0) throw new Error((sync.err || sync.out || 'Figma sync failed').trim().slice(0, 240));
        s = lastJson(sync.out);
      }
      const build = await runNode('build-icon-lib.js', 60000);
      if (build.code !== 0) throw new Error((build.err || build.out || 'build failed').trim().slice(0, 240));
      const b = lastJson(build.out);
      let syncedAt = null;
      try { syncedAt = JSON.parse(fs.readFileSync(path.join(BASE, 'data', 'icons-figma', '_manifest.json'), 'utf8')).syncedAt || null; } catch (e) {}
      return { ok: true, count: b.count || 0, figma: b.figma || 0, legacy: b.legacy || 0, notLight: s.notLight || 0, fromFigma: hasToken, syncedAt };
    })().then(body => {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(body));
    }, e => {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: false, error: e.message }));
    });
    return;
  }

  // GET /brand — brand colors + uploaded files
  if (req.method === 'GET' && req.url === '/brand') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify({ colors: loadBrandColors(), files: listBrandFiles() }));
  }

  // POST /brand/colors — replace the brand color list ({ colors: [{name, hex}] })
  if (req.method === 'POST' && req.url === '/brand/colors') {
    const body = await readBody(req);
    try {
      const parsed = JSON.parse(body);
      if (!Array.isArray(parsed.colors)) throw new Error('Body must be { colors: [...] }');
      if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
      fs.writeFileSync(BRAND_FILE, JSON.stringify({ colors: parsed.colors }, null, 2));
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: true, count: parsed.colors.length }));
    } catch (e) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: false, error: e.message }));
    }
    return;
  }

  // POST /brand/upload — upload a brand asset file ({ filename, dataBase64 })
  if (req.method === 'POST' && req.url === '/brand/upload') {
    const body = await readBody(req);
    try {
      const parsed = JSON.parse(body);
      if (!parsed.filename || !parsed.dataBase64) throw new Error('Missing filename or data');
      if (!fs.existsSync(BRAND_ASSETS_DIR)) fs.mkdirSync(BRAND_ASSETS_DIR, { recursive: true });
      const name = path.basename(parsed.filename);
      const b64 = String(parsed.dataBase64).replace(/^data:[^;]+;base64,/, '');
      fs.writeFileSync(path.join(BRAND_ASSETS_DIR, name), b64, 'base64');
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: true, name }));
    } catch (e) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: false, error: e.message }));
    }
    return;
  }

  // POST /brand/delete — delete a brand asset file ({ filename })
  if (req.method === 'POST' && req.url === '/brand/delete') {
    const body = await readBody(req);
    try {
      const name = path.basename(JSON.parse(body).filename || '');
      const f = path.join(BRAND_ASSETS_DIR, name);
      if (name && fs.existsSync(f)) fs.unlinkSync(f);
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: true }));
    } catch (e) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: false, error: e.message }));
    }
    return;
  }

  // /jobs/<id> — GET single job, or POST to update it ({status, result, resultPath}).
  // Only matches the bare /jobs/<id> form; deeper paths (e.g. /jobs/<id>/output/deck.pptx)
  // fall through to static file serving below so results are downloadable.
  const jobSeg = req.url.startsWith('/jobs/') ? req.url.split('?')[0].slice(6) : null;
  if (jobSeg && !jobSeg.includes('/')) {
    const id = path.basename(decodeURIComponent(jobSeg));
    const jf = path.join(JOBS_DIR, id, 'job.json');
    if (!id || !fs.existsSync(jf)) {
      res.writeHead(404, { 'Content-Type': 'application/json' });
      return res.end(JSON.stringify({ ok: false, error: 'job not found' }));
    }
    if (req.method === 'GET') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      return res.end(fs.readFileSync(jf, 'utf8'));
    }
    if (req.method === 'POST') {
      const body = await readBody(req);
      try {
        const patch = JSON.parse(body);
        const job = readJSON(jf);
        ['status', 'result', 'resultPath', 'previewPath', 'revisions', 'title', 'prompt', 'pinned', 'marked', 'favorite'].forEach(k => { if (patch[k] !== undefined) job[k] = patch[k]; });
        job.updatedAt = new Date().toISOString();
        fs.writeFileSync(jf, JSON.stringify(job, null, 2));
        // Pre-warm preview thumbnails when output paths land, so History opens instantly later.
        if (patch.status === 'done' || patch.resultPath || patch.previewPath || patch.revisions) {
          setImmediate(() => prewarmThumbs(job));
        }
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: true, job }));
      } catch (e) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: false, error: e.message }));
      }
      return;
    }
  }

  // POST /jobs/<id>/revise — append a change request to a job ({ prompt })
  const reviseMatch = req.method === 'POST' && req.url.split('?')[0].match(/^\/jobs\/([^/]+)\/revise$/);
  if (reviseMatch) {
    const id = path.basename(decodeURIComponent(reviseMatch[1]));
    const jf = path.join(JOBS_DIR, id, 'job.json');
    const body = await readBody(req);
    try {
      if (!fs.existsSync(jf)) throw new Error('job not found');
      const parsed = JSON.parse(body);
      const prompt = (parsed.prompt || '').trim();
      if (!prompt) throw new Error('Empty change request');
      const job = readJSON(jf);
      job.revisions = Array.isArray(job.revisions) ? job.revisions : [];
      const n = job.revisions.length + 1;
      const rev = { n, prompt, status: 'queued', createdAt: new Date().toISOString() };
      // Optional visual annotation: one flattened PNG per annotated page (numbered pins drawn on the
      // rendered page) + the pin metadata (page, location, comment). Saved into jobs/<id>/annotations/
      // so the run can read both. rev.annotationImages is an array (one entry per page with pins).
      const ann = parsed.annotation;
      if (ann) {
        const annDir = path.join(JOBS_DIR, id, 'annotations');
        const saveImg = (dataUrl, name) => {
          const m = String(dataUrl || '').match(/^data:image\/png;base64,(.+)$/);
          if (!m) return null;
          if (!fs.existsSync(annDir)) fs.mkdirSync(annDir, { recursive: true });
          fs.writeFileSync(path.join(annDir, name), m[1], 'base64');
          return 'annotations/' + name;
        };
        const imgs = [];
        if (Array.isArray(ann.images)) {
          ann.images.forEach(im => { const rel = saveImg(im.image, 'rev' + n + '_p' + ((im.page || 0) + 1) + '.png'); if (rel) imgs.push(rel); });
        } else if (typeof ann.image === 'string') {
          const rel = saveImg(ann.image, 'rev' + n + '.png'); if (rel) imgs.push(rel);
        }
        if (imgs.length) rev.annotationImages = imgs;
        if (Array.isArray(ann.pins)) rev.pins = ann.pins;
      }
      // Optional attachments: files the user added to the change request (a new logo, a corrected
      // brief, a reference screenshot). Stored per revision under jobs/<id>/attachments/rev<N>/ —
      // per revision, so sending the same filename twice never overwrites what an earlier version
      // was built from, and recorded on the revision so the run knows it has to read them.
      const files = Array.isArray(parsed.files) ? parsed.files : [];
      if (files.length) {
        const attDir = path.join(JOBS_DIR, id, 'attachments', 'rev' + n);
        const saved = [];
        for (const f of files) {
          const name = path.basename(String(f.filename || '')).replace(/[\\/:*?"<>|]/g, '_');
          if (!name || !f.dataBase64) continue;
          if (!fs.existsSync(attDir)) fs.mkdirSync(attDir, { recursive: true });
          const b64 = String(f.dataBase64).replace(/^data:[^;]+;base64,/, '');
          fs.writeFileSync(path.join(attDir, name), b64, 'base64');
          saved.push('attachments/rev' + n + '/' + name);
        }
        if (saved.length) rev.attachments = saved;
      }
      job.revisions.push(rev);
      job.updatedAt = new Date().toISOString();
      fs.writeFileSync(jf, JSON.stringify(job, null, 2));
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: true, revision: n, job }));
    } catch (e) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: false, error: e.message }));
    }
    return;
  }

  // POST /jobs/<id>/run — attend the queued item now via headless Claude (semi-auto, one click)
  const runMatch = req.method === 'POST' && req.url.split('?')[0].match(/^\/jobs\/([^/]+)\/run$/);
  if (runMatch) {
    const id = path.basename(decodeURIComponent(runMatch[1]));
    const r = startQueuedRun(id);
    res.writeHead(r.ok ? 200 : (r.error === 'job not found' ? 404 : 200), { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(r));
    return;
  }

  // POST /jobs/<id>/stop — stop the in-flight run; returns the item + prompt so the UI can edit & re-run
  const stopMatch = req.method === 'POST' && req.url.split('?')[0].match(/^\/jobs\/([^/]+)\/stop$/);
  if (stopMatch) {
    const id = path.basename(decodeURIComponent(stopMatch[1]));
    const r = stopRun(id);
    res.writeHead(r.ok ? 200 : 400, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(r));
    return;
  }

  // POST /jobs/<id>/rerun — update the item's prompt and run it again ({ kind, n, prompt })
  const rerunMatch = req.method === 'POST' && req.url.split('?')[0].match(/^\/jobs\/([^/]+)\/rerun$/);
  if (rerunMatch) {
    const id = path.basename(decodeURIComponent(rerunMatch[1]));
    const body = await readBody(req);
    try {
      const p = JSON.parse(body);
      const r = rerunWithPrompt(id, p.kind === 'rev' ? 'rev' : 'base', p.n, p.prompt);
      res.writeHead(r.ok ? 200 : 400, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(r));
    } catch (e) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: false, error: e.message }));
    }
    return;
  }


  // POST /jobs/<id>/delete — remove a task and its folder (history cleanup). Refuses mid-run.
  const delMatch = req.method === 'POST' && req.url.split('?')[0].match(/^\/jobs\/([^/]+)\/delete$/);
  if (delMatch) {
    const id = path.basename(decodeURIComponent(delMatch[1]));
    const dir = path.join(JOBS_DIR, id);
    const jf = path.join(dir, 'job.json');
    try {
      if (!fs.existsSync(jf)) throw new Error('task not found');
      const job = readJSON(jf);
      const busy = job.status === 'running' || job.status === 'needs-input' ||
        (job.revisions || []).some(r => r.status === 'running' || r.status === 'needs-input');
      if (busy) throw new Error('Task is in progress — cancel or let it finish before deleting.');
      fs.rmSync(dir, { recursive: true, force: true });
      // Record the deletion so a later push can drop it from the shared repo too (Option A:
      // only tasks explicitly deleted here are ever removed from the repo — never a blind mirror).
      try {
        const logf = path.join(DATA_DIR, 'deleted-tasks.json');
        let log = [];
        try { if (fs.existsSync(logf)) log = JSON.parse(fs.readFileSync(logf, 'utf8')); } catch (e) {}
        if (!Array.isArray(log)) log = [];
        if (!log.some(e => e && e.id === id)) log.push({ id, pipeline: job.pipeline || '', title: job.title || '', deletedAt: new Date().toISOString() });
        fs.writeFileSync(logf, JSON.stringify(log, null, 2));
      } catch (e) {}
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: true, deleted: id }));
    } catch (e) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: false, error: e.message }));
    }
    return;
  }

  // GET /whoami — who is using this console. Per instance, never shared: a name saved in Settings
  // (data/user.json, gitignored) wins; otherwise the git identity of the clone it runs from, so each
  // teammate sees their own name without anyone editing code. POST sets or clears the saved name.
  if (req.url.split('?')[0] === '/whoami' && (req.method === 'GET' || req.method === 'POST')) {
    const uf = path.join(DATA_DIR, 'user.json');
    const send = (code, obj) => { res.writeHead(code, { 'Content-Type': 'application/json' }); res.end(JSON.stringify(obj)); };
    try {
      if (req.method === 'POST') {
        const parsed = JSON.parse(await readBody(req));
        const name = String(parsed.name || '').replace(/\s+/g, ' ').trim().slice(0, 80);
        if (name) fs.writeFileSync(uf, JSON.stringify({ name }, null, 2));
        else if (fs.existsSync(uf)) fs.unlinkSync(uf);
      }
      let saved = '';
      try { if (fs.existsSync(uf)) saved = String(readJSON(uf).name || '').trim(); } catch (e) {}
      let fromGit = '';
      if (!saved) { try { const s = loadSource(); fromGit = git(['config', 'user.name'], s.repoDir || BASE).toString().trim(); } catch (e) {} }
      return send(200, { ok: true, name: saved || fromGit, saved: !!saved });
    } catch (e) { return send(400, { ok: false, error: e.message }); }
  }

  // GET /deleted-tasks — the pending deletion log (tasks removed via Delete since the last push).
  // A push reads this, confirms with the user, drops those ids from the repo, then clears it.
  if (req.method === 'GET' && req.url.split('?')[0] === '/deleted-tasks') {
    let log = [];
    try { const f = path.join(DATA_DIR, 'deleted-tasks.json'); if (fs.existsSync(f)) log = JSON.parse(fs.readFileSync(f, 'utf8')); } catch (e) {}
    res.writeHead(200, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify({ deleted: Array.isArray(log) ? log : [] }));
  }

  // POST /jobs/<id>/ask — Claude (mid-run) pauses on a doubt/blocker and asks the user.
  // body: { question, options? }  -> task goes to 'needs-input' until a decision is posted.
  const askMatch = req.method === 'POST' && req.url.split('?')[0].match(/^\/jobs\/([^/]+)\/ask$/);
  if (askMatch) {
    const id = path.basename(decodeURIComponent(askMatch[1]));
    const jf = path.join(JOBS_DIR, id, 'job.json');
    const body = await readBody(req);
    try {
      if (!fs.existsSync(jf)) throw new Error('job not found');
      const parsed = JSON.parse(body);
      const job = readJSON(jf);
      job.pending = {
        question: (parsed.question || 'The task needs a decision to continue.').trim(),
        options: Array.isArray(parsed.options) && parsed.options.length ? parsed.options : ['allow', 'continue', 'cancel'],
        askedAt: new Date().toISOString(),
        decision: null,
        // "arch": the window adds the architecture case-data form (any task type, e.g. a deck with a diagram)
        ...(parsed.form === 'arch' ? { form: 'arch' } : {}),
      };
      job.status = 'needs-input';
      job.updatedAt = new Date().toISOString();
      fs.writeFileSync(jf, JSON.stringify(job, null, 2));
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: true }));
    } catch (e) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: false, error: e.message }));
    }
    return;
  }

  // POST /jobs/<id>/decision — the user answers the pending question (allow | continue | cancel).
  const decMatch = req.method === 'POST' && req.url.split('?')[0].match(/^\/jobs\/([^/]+)\/decision$/);
  if (decMatch) {
    const id = path.basename(decodeURIComponent(decMatch[1]));
    const jf = path.join(JOBS_DIR, id, 'job.json');
    const body = await readBody(req);
    try {
      if (!fs.existsSync(jf)) throw new Error('job not found');
      const parsed = JSON.parse(body);
      const choice = (parsed.decision || '').trim();
      const job = readJSON(jf);
      if (!job.pending) throw new Error('no pending question');
      job.pending.decision = { choice, note: (parsed.note || '').trim(), at: new Date().toISOString() };
      // Architecture: the intervention window returns the case-data form (only filled fields). It
      // answers this question and becomes the task's case data from here on.
      const f = parsed.fields;
      if (f && typeof f === 'object' && !Array.isArray(f)) {
        job.pending.decision.fields = f;
        job.options = Object.assign({}, job.options, { arch: f });
      }
      job.status = choice === 'cancel' ? 'cancelled' : 'running';
      job.updatedAt = new Date().toISOString();
      fs.writeFileSync(jf, JSON.stringify(job, null, 2));
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: true, status: job.status }));
    } catch (e) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: false, error: e.message }));
    }
    return;
  }

  // GET /jobs/<id>/log — the captured output of the run(s) for transparency
  const logMatch = req.method === 'GET' && req.url.split('?')[0].match(/^\/jobs\/([^/]+)\/log$/);
  if (logMatch) {
    const id = path.basename(decodeURIComponent(logMatch[1]));
    const lp = path.join(JOBS_DIR, id, 'run.log');
    res.writeHead(200, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end(fs.existsSync(lp) ? fs.readFileSync(lp, 'utf8') : '');
    return;
  }

  // Static file serving
  // Strip the query FIRST, then decide. Checking req.url === '/' before stripping meant any
  // cache-busting root URL such as /?v2 fell through to the else branch, resolved to the directory
  // itself and 404'd, which also removed the simplest way to force a fresh copy.
  const bare = req.url.split('?')[0];
  const urlPath = (bare === '/' || bare === '') ? '/index.html' : bare;
  const filePath = path.join(BASE, decodeURIComponent(urlPath));
  const ext = path.extname(filePath);
  const contentType = MIME_TYPES[ext] || 'application/octet-stream';

  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404);
      res.end('Not found');
    } else {
      // The whole app is index.html plus two generated .js files, and they are edited constantly.
      // Served without any cache header, browsers fall back to heuristic caching and can hold a
      // stale copy for hours: the server has the new build, the tab is still running yesterday's.
      // That is not theoretical, it is how a fixed bug kept looking unfixed. no-cache still allows
      // caching, it just forces a revalidation first, so this costs one conditional request.
      const revalidate = ['.html', '.js', '.json'].includes(ext);
      res.writeHead(200, Object.assign({ 'Content-Type': contentType },
        revalidate ? { 'Cache-Control': 'no-cache' } : {}));
      res.end(data);
    }
  });
// Bind to loopback only. There is no authentication here, POST /run executes an arbitrary shell
// command, and runs spawn the Claude CLI with --dangerously-skip-permissions. Listening on every
// interface would hand anyone on the same network a remote shell on this machine.
}).listen(3491, '127.0.0.1', () => {
  resetStaleRunning();
  console.log('Server running on http://127.0.0.1:3491 (local only)');
  // Resolve the Python interpreter now, not on the first request that needs it: the probe is
  // spawnSync and would otherwise block whichever download or thumbnail asked for it first.
  setTimeout(() => { try { console.log('python:', pyLabel()); } catch (e) {} }, 10);
  // Pull the shared content (progress.md + brand) from the repo at startup, best-effort.
  setTimeout(() => { try { syncFromGitHub(); console.log('content source:', lastSync.mode, lastSync.ok ? 'ok' : ('error: ' + lastSync.error)); } catch (e) {} }, 150);
});
