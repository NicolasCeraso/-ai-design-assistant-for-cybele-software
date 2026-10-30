#!/usr/bin/env python3
"""Arma el audio de UNA escena con micro-pausas insertadas entre palabras.

Uso:  py -3.13 insert_pauses.py locucion.wav inicio fin salida.wav pausa1_abs:seg [pausa2_abs:seg ...] [--ffmpeg ruta]

Corta la locución [inicio, fin] (segundos absolutos) en cada punto `pausa_abs` e inserta `seg`
segundos de silencio. Sirve cuando la animación necesita aire entre dos acciones (p. ej. "copy,
download and print"), pero ojo: Nick rechazó pausas largas por antinaturales. Probado: 1.2 s tras
el final de una escena funciona (se congela el último cuadro); DENTRO de una frase, 0.03-0.08 s
como máximo. Después hay que alargar la escena en Figma esa misma cantidad y desplazar lo que
viene tras cada pausa.
"""
import subprocess, sys, wave
import numpy as np

a = sys.argv[1:]
FF = "ffmpeg"
if "--ffmpeg" in a:
    i = a.index("--ffmpeg"); FF = a[i+1]; del a[i:i+2]
src, t0, t1, out, *ps = a
t0, t1 = float(t0), float(t1)
pauses = sorted((float(p.split(":")[0]), float(p.split(":")[1])) for p in ps)
SR = 48000
raw = subprocess.run([FF, "-loglevel", "error", "-i", src, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                     capture_output=True, check=True).stdout
v = np.frombuffer(raw, dtype=np.float32)
pieces, last = [], t0
for c, d in pauses:
    pieces += [v[int(last*SR):int(c*SR)], np.zeros(int(d*SR), dtype=np.float32)]
    last = c
pieces.append(v[int(last*SR):int(t1*SR)])
y = np.concatenate(pieces)
with wave.open(out, "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(y, -1, 1)*32767).astype(np.int16).tobytes())
print(f"OK {len(y)/SR:.2f} s -> {out}")
