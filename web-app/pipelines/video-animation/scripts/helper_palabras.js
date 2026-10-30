// Helper de partida (SIN PROBAR): duplica una capa de texto en N clones, uno por palabra,
// con sólo la palabra k visible. Pegalo dentro de use_figma (top-level await, sin IIFE).
// Uso: const res = await splitWords(textNodeId, parentFrame, groupName)
async function splitWords(textNodeId, parent, groupName) {
  const t = await figma.getNodeByIdAsync(textNodeId);
  // cargar todas las fuentes usadas
  for (const f of t.getRangeAllFontNames(0, t.characters.length)) await figma.loadFontAsync(f);
  const text = t.characters;
  const words = [];
  const re = /\S+/g; let m;
  while ((m = re.exec(text))) words.push({ w: m[0], start: m.index, end: m.index + m[0].length });
  const clones = [];
  for (let k = 0; k < words.length; k++) {
    const c = t.clone();
    parent.appendChild(c);
    c.x = t.x; c.y = t.y;        // si t está dentro de un grupo/autolayout ajustá coordenadas
    c.name = `${t.name} · ${words[k].w}`;
    // vaciar fills de todo salvo la palabra k
    for (let j = 0; j < words.length; j++) {
      if (j === k) continue;
      c.setRangeFills(words[j].start, words[j].end, []);
    }
    clones.push(c);
  }
  t.visible = false;             // el original queda oculto (el copy sigue en él)
  return { words: words.map(w => w.w), cloneIds: clones.map(c => c.id) };
}
// Animación por palabra (tiempos absolutos de la escena en segundos):
// for (i) { c.applyManualKeyframeTrack({type:'PROPERTY', name:'OPACITY'}, {keyframes:[
//   {timelinePosition:0, value:{type:'FLOAT', value:0}, easing:{type:'HOLD'}},
//   {timelinePosition:tIn[i], value:{type:'FLOAT', value:0}, easing:{type:'EASE_OUT'}},
//   {timelinePosition:tIn[i]+0.3, value:{type:'FLOAT', value:1}, easing:{type:'EASE_OUT'}},
//   {timelinePosition:tOut, value:{type:'FLOAT', value:1}},
//   {timelinePosition:tOut+0.25, value:{type:'FLOAT', value:0}, easing:{type:'EASE_OUT'}} ]});
//   c.applyManualKeyframeTrack({type:'PROPERTY', name:'TRANSLATION_Y'}, {keyframes:[
//     {timelinePosition:tIn[i], value:{type:'FLOAT', value:14}},
//     {timelinePosition:tIn[i]+0.3, value:{type:'FLOAT', value:0}, easing:{type:'EASE_OUT'}} ]}) }
// Notas: si un texto tiene opacity keyframes de v2 o TextStagger aplicado en el original, quitalos (removeAnimationStyle / removeManualKeyframeTrack) antes de clonar.
// Si el texto tiene varias líneas con saltos, el regex \S+ sigue sirviendo (las posiciones vienen del layout del clon).
