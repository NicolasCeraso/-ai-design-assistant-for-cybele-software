// Build 6 native, Figma-safe SVG placas (1080x1080) — "The Idle-Hour Line" (v2).
const fs = require('fs');
const path = require('path');

// Usage: node build_svgs_v2.js [output-dir]   (default: ./output)
const BASE = path.join(__dirname, '..');            // deckgen/ — brand_assets/, icons/
const OUT  = process.argv[2] || path.join(__dirname, 'output');
fs.mkdirSync(OUT, { recursive: true });

const C = {
  pale:'#eef4fd', ink:'#0f2233', muted:'#5b7089', mutedN:'#9fb0c6',
  blue:'#1a7fe0', brand:'#007DC1', ltblue:'#7fc0ff', iconBlue:'#0A74D6',
  navy0:'#14335c', navy1:'#0a1f3a',
  teal:'#1aa778', red:'#e8452a',
  idleL:'#fbe1da', idleN:'#40252f', track:'#12335a',
  cardN:'#10294d', cardStroke:'#2b4a6f', white:'#ffffff',
};
const FONT = 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif';

function loadAsset(file){
  let s = fs.readFileSync(path.join(BASE, file), 'utf8');
  const vb = s.match(/viewBox="([-\d.\s]+)"/)[1].trim().split(/\s+/).map(Number);
  let inner = s.replace(/^[\s\S]*?<svg[^>]*>/, '').replace(/<\/svg>\s*$/, '');
  inner = inner.replace(/var\(--[^,]*,\s*([^)]+)\)/g, (_, v) => v.trim());
  inner = inner.replace(/\sid="[^"]*"/g, '').replace(/\sstyle="[^"]*"/g, '');
  return { inner, w: vb[2], h: vb[3] };
}
const A = {
  tf:   loadAsset('brand_assets/thinfinity_logo.svg'),
  tfW:  loadAsset('brand_assets/thinfinity_logo_white.svg'),
  cyb:  loadAsset('brand_assets/cybele_logo.svg'),
  cybW: loadAsset('brand_assets/cybele_logo_white.svg'),
};
function place(a, tx, ty, targetW){ const s = targetW / a.w; return `<g transform="translate(${tx} ${ty}) scale(${s.toFixed(5)})">${a.inner}</g>`; }

function T(x,y,s,{size=32,weight=400,fill=C.ink,anchor='start',spacing=0,deco=''}={}){
  return `<text x="${x}" y="${y}" font-family='${FONT}' font-size="${size}" font-weight="${weight}" fill="${fill}" text-anchor="${anchor}"${spacing?` letter-spacing="${spacing}"`:''}${deco?` text-decoration="${deco}"`:''}>${s}</text>`;
}
const userIcon = (f) => `<g fill="${f}" fill-rule="evenodd"><path d="M80.924 85.5842C104.558 85.5842 123.716 66.4261 123.716 42.7926C123.716 19.1591 104.558 0 80.924 0C57.2905 0 38.132 19.1591 38.132 42.7926C38.132 66.4261 57.2905 85.5842 80.924 85.5842ZM80.924 9.17988C99.458 9.17988 114.536 24.258 114.536 42.7925C114.536 61.3269 99.458 76.404 80.924 76.404C62.3901 76.404 47.312 61.3259 47.312 42.7925C47.312 24.259 62.3901 9.17988 80.924 9.17988Z"/><path d="M161.841 171.634C159.407 129.058 124.11 95.2825 80.9241 95.2825C37.7384 95.2825 2.44093 129.058 0.00728412 171.634L0 189.101C0 191.807 2.19338 194 4.89893 194H156.949C159.655 194 161.848 191.807 161.848 189.101L161.841 171.634ZM9.18001 184.82L9.1868 171.906C11.4806 134.065 42.9427 104.463 80.924 104.463C118.905 104.463 150.367 134.065 152.661 171.906L152.668 184.82H9.18001Z"/></g>`;
function gridI(x,y,sz,col){const s=sz/24;return `<g transform="translate(${x} ${y}) scale(${s})" fill="${col}"><rect x="2" y="2" width="8.5" height="8.5" rx="2"/><rect x="13.5" y="2" width="8.5" height="8.5" rx="2"/><rect x="2" y="13.5" width="8.5" height="8.5" rx="2"/><rect x="13.5" y="13.5" width="8.5" height="8.5" rx="2"/></g>`;}
function clockI(x,y,sz,col){const s=sz/24;return `<g transform="translate(${x} ${y}) scale(${s})" fill="none" stroke="${col}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.2 2"/></g>`;}
function chipI(x,y,sz,col){const s=sz/24;return `<g transform="translate(${x} ${y}) scale(${s})" fill="none" stroke="${col}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 9h6v6H9z"/><path d="M9 3v3M15 3v3M9 18v3M15 18v3M3 9h3M3 15h3M18 9h3M18 15h3"/></g>`;}
function checkMark(cx,cy,r,col){return `<path d="M${cx-r*0.5} ${cy} l${r*0.32} ${r*0.4} l${r*0.66} -${r*0.72}" fill="none" stroke="${col}" stroke-width="${r*0.34}" stroke-linecap="round" stroke-linejoin="round"/>`;}

// week timeline: days = fractions 0..1
function weekBar(x,y,w,h,days,mode,labels){
  const n=days.length, gap=10, cw=(w-gap*(n-1))/n;
  const idle = mode==='light'?C.idleL:C.idleN;
  let out='';
  for(let i=0;i<n;i++){
    const cx=x+i*(cw+gap);
    out+=`<rect x="${cx.toFixed(1)}" y="${y}" width="${cw.toFixed(1)}" height="${h}" rx="6" fill="${idle}"/>`;
    const lh=h*days[i];
    if(lh>0.5) out+=`<rect x="${cx.toFixed(1)}" y="${(y+h-lh).toFixed(1)}" width="${cw.toFixed(1)}" height="${lh.toFixed(1)}" rx="6" fill="${C.blue}"/>`;
    if(labels) out+=T(cx+cw/2, y+h+30, labels[i], {size:22,weight:700,fill:mode==='light'?C.muted:'#8fa3bd',anchor:'middle'});
  }
  return out;
}
function costTrack(x,y,w,h,frac,fill){
  return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="8" fill="${C.track}"/><rect x="${x}" y="${y}" width="${(w*frac).toFixed(1)}" height="${h}" rx="8" fill="${fill}"/>`;
}
function svg(body, defs=''){
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">
<defs>${defs}</defs>
${body}
</svg>`;
}
const navyGrad = (id) => `<linearGradient id="${id}" x1="920" y1="-100" x2="216" y2="1080" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="${C.navy0}"/><stop offset="0.58" stop-color="${C.navy1}"/></linearGradient>`;
const days=[0.58,0.60,0.57,0.60,0.55,0.18,0], dayLabels=['M','T','W','T','F','S','S'];
const P=96;
const out={};

// lockups
const lockLight = (y)=>`${place(A.tf,P,y,250)}${T(360,y+42,'by',{size:22,weight:600,fill:C.muted})}${place(A.cyb,404,y+12,120)}`;
const lockDark  = (y)=>`${place(A.tfW,P,y,250)}${T(370,y+42,'by',{size:22,weight:600,fill:C.mutedN})}${place(A.cybW,414,y+12,120)}`;

// ===== PLACA 1 — Portada (navy) =====
out.placa1 = svg(`
<rect width="1080" height="1080" fill="url(#p1-bg)"/>
${T(P,175,'Microsoft cut cloud',{size:60,weight:800,fill:'#fff'})}
${T(P,242,'desktop prices',{size:60,weight:800,fill:'#fff'})}
<text x="${P}" y="420" font-family='${FONT}' font-size="150" font-weight="800" fill="#fff" letter-spacing="-4">20%</text>
${T(430,412,'↓',{size:96,weight:800,fill:C.teal})}
${T(P,485,'Time to redo the branch math.',{size:34,weight:500,fill:C.mutedN})}
${weekBar(P,600,500,90,days,'navy')}
${lockDark(920)}
`, navyGrad('p1-bg'));

// ===== PLACA 2 — Disparador + pregunta (light) =====
const p2 = [
  'In <tspan font-weight="800">May 2026</tspan>, Windows 365 Business',
  'pricing dropped roughly <tspan font-weight="800">20%</tspan> — the first',
  'real move in the DaaS market in two',
  'years — landing right as banks enter',
  'mid-year budget reviews.'
];
out.placa2 = svg(`
<rect width="1080" height="1080" fill="${C.pale}"/>
${p2.map((l,i)=>`<text x="${P}" y="${185+i*56}" font-family='${FONT}' font-size="40" font-weight="600" fill="${C.ink}">${l}</text>`).join('\n')}
${T(P,545,'list price',{size:44,weight:800,fill:'#b9c6d8',deco:'line-through'})}
${T(360,545,'→',{size:44,weight:800,fill:C.teal})}
${T(430,548,'−20%',{size:52,weight:800,fill:C.teal})}
${T(P,700,'So what does a teller seat',{size:46,weight:800,fill:C.blue})}
${T(P,762,'actually cost now?',{size:46,weight:800,fill:C.blue})}
${lockLight(930)}
`);

// ===== PLACA 3 — La pregunta equivocada (navy) =====
function trait(x, icon, label){
  const w=280;
  return `<rect x="${x}" y="360" width="${w}" height="196" rx="18" fill="${C.cardN}" stroke="${C.cardStroke}" stroke-width="2"/>
${icon(x+w/2-24,410,48)}
${T(x+w/2,510,label,{size:28,weight:700,fill:'#eaf1fb',anchor:'middle'})}`;
}
out.placa3 = svg(`
<rect width="1080" height="1080" fill="url(#p3-bg)"/>
${T(P,178,'Vendor list prices answer',{size:52,weight:800,fill:'#fff'})}
<text x="${P}" y="242" font-family='${FONT}' font-size="52" font-weight="800" fill="#fff">the <tspan fill="${C.red}">wrong question.</tspan></text>
<g transform="translate(${P} 285) scale(0.19)">${userIcon(C.ltblue)}</g>
${T(P+52,320,'A teller is the textbook task worker:',{size:30,weight:500,fill:C.mutedN})}
${trait(P, (x,y,s)=>gridI(x,y,s,C.ltblue), '6–10 apps')}
${trait(P+304, (x,y,s)=>clockI(x,y,s,C.ltblue), 'Fixed hours')}
${trait(P+608, (x,y,s)=>chipI(x,y,s,C.ltblue), 'No GPU')}
<rect x="${P}" y="640" width="6" height="200" rx="3" fill="${C.red}"/>
${T(P+34,690,'Per-user fixed pricing',{size:36,weight:700,fill:'#eaf1fb'})}
${T(P+34,742,'= the most expensive way',{size:36,weight:700,fill:C.red})}
${T(P+34,794,'to buy the seat.',{size:36,weight:700,fill:'#eaf1fb'})}
`, navyGrad('p3-bg'));

// ===== PLACA 4 — La hora ociosa (light · hero) =====
out.placa4 = svg(`
<rect width="1080" height="1080" fill="${C.pale}"/>
${T(P,178,'The line vendors leave off',{size:52,weight:800,fill:C.ink})}
<text x="${P}" y="242" font-family='${FONT}' font-size="52" font-weight="800" fill="${C.ink}">the page is <tspan fill="${C.red}">idle hours.</tspan></text>
${T(P,380,'36%',{size:56,weight:800,fill:C.blue})}
${T(P,420,'needed',{size:26,weight:500,fill:C.muted})}
${T(1080-P,380,'64%',{size:56,weight:800,fill:C.red,anchor:'end'})}
${T(1080-P,420,'idle — paid, not used',{size:26,weight:500,fill:C.muted,anchor:'end'})}
${weekBar(P,470,888,170,days,'light',dayLabels)}
${[['Pooled hosts scale to','zero on Sundays',P],['Thin-client energy','savings',P+300],['DR posture you','didn’t have before',P+600]].map(([a,b,x])=>`<circle cx="${x+14}" cy="${800}" r="15" fill="none" stroke="${C.teal}" stroke-width="3"/>${checkMark(x+14,801,15,C.teal)}${T(x+42,795,a,{size:25,weight:600,fill:C.ink})}${T(x+42,826,b,{size:25,weight:600,fill:C.ink})}`).join('\n')}
`);

// ===== PLACA 5 — El delta (navy) =====
out.placa5 = svg(`
<rect width="1080" height="1080" fill="url(#p5-bg)"/>
${T(P,170,'For a 50-branch, 300-teller bank,',{size:46,weight:800,fill:'#fff'})}
<text x="${P}" y="228" font-family='${FONT}' font-size="46" font-weight="800" fill="#fff">the delta is the <tspan fill="${C.blue}">idle-hour line</tspan> —</text>
${T(P,286,'not the license line.',{size:46,weight:800,fill:'#fff'})}
${T(P,395,'Windows 365 · fixed per-user',{size:28,weight:600,fill:'#cddaeb'})}
${T(1080-P,395,'≈$30 / seat',{size:28,weight:800,fill:C.red,anchor:'end'})}
${costTrack(P,415,888,44,1.0,C.red)}
${T(P,545,'Thinfinity on OCI · pooled',{size:28,weight:600,fill:'#cddaeb'})}
${T(1080-P,545,'≈$16–19 / seat',{size:28,weight:800,fill:C.teal,anchor:'end'})}
${costTrack(P,565,888,44,0.57,C.teal)}
${T(P,660,'the idle-hour line',{size:24,weight:600,fill:C.ltblue})}
<line x1="${P+220}" y1="653" x2="800" y2="653" stroke="${C.ltblue}" stroke-width="2"/>
${T(1080-P,660,'that is the delta',{size:24,weight:600,fill:C.ltblue,anchor:'end'})}
${lockDark(930)}
`, navyGrad('p5-bg'));

// ===== PLACA 6 — CTA de cierre (navy) =====
out.placa6 = svg(`
<rect width="1080" height="1080" fill="url(#p6-bg)"/>
${T(P,200,'The list price isn’t',{size:56,weight:800,fill:'#fff'})}
${T(P,268,'the whole story.',{size:56,weight:800,fill:'#fff'})}
<text x="${P}" y="345" font-family='${FONT}' font-size="32" font-weight="500" fill="#cddaeb">Read the full cost breakdown at <tspan font-weight="800" fill="#fff">blog.cybelesoft.com</tspan></text>
${weekBar(P,405,888,50,days,'navy')}
<rect x="${P}" y="520" width="888" height="200" rx="18" fill="#fff"/>
${T(P+40,585,'REMOTE DESKTOP · VDI &amp; DaaS',{size:19,weight:700,fill:C.blue,spacing:1})}
${T(P+40,635,'The $26 Teller Desktop:',{size:31,weight:800,fill:C.ink})}
${T(P+40,677,'Branch VDI Cost Math for Banks',{size:31,weight:800,fill:C.ink})}
<rect x="668" y="558" width="290" height="124" rx="12" fill="url(#p6-thumb)"/>
<g transform="rotate(-4 813 620)"><rect x="712" y="592" width="202" height="56" rx="6" fill="${C.teal}"/>${T(813,630,'cutting branch vdi costs',{size:24,weight:800,fill:'#fff',anchor:'middle'})}</g>
${place(A.cybW,P,935,150)}
<rect x="272" y="941" width="2" height="46" fill="rgba(255,255,255,0.4)"/>
${T(302,977,'Blogs',{size:34,weight:800,fill:C.ltblue})}
`, navyGrad('p6-bg') + `<linearGradient id="p6-thumb" x1="668" y1="558" x2="958" y2="682" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#0d2340"/><stop offset="1" stop-color="${C.blue}"/></linearGradient>`);

for (const [name, content] of Object.entries(out)){
  const f = path.join(OUT, `branch_math_v2_${name}.svg`);
  fs.writeFileSync(f, content, 'utf8');
  console.log('[ok]', f, content.length, 'bytes');
}
