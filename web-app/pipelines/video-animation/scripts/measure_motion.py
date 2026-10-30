#!/usr/bin/env python3
"""Mide en el MP4 (no en los keyframes) cuándo se mueve una zona del cuadro.

Uso:  py -3.13 measure_motion.py escena.mp4 x0 y0 x1 y1 [--seg 5] [--thr 0.02] [--ffmpeg ruta]
      (x0..y1 en fracciones 0-1 del cuadro; --seg = segundos a analizar desde el inicio)

Imprime los intervalos [inicio, fin] en segundos en que la zona cambia más que el umbral
(diferencia media entre cuadros consecutivos, escala 0-255). Sirve para:
  * sincronizar un sonido con el movimiento de un elemento (agujas de un reloj, un check),
  * confirmar el instante real en que aparece algo, antes de ponerle un efecto de sonido.
Ojo: un cambio de fondo en la zona también cuenta como movimiento. Mirá fotogramas para distinguir.
"""
import subprocess, sys
import numpy as np

a = [x for x in sys.argv[1:]]
def opt(name, default):
    if name in a:
        i = a.index(name); v = a[i+1]; del a[i:i+2]; return v
    return default
seg = float(opt("--seg", 5)); thr = float(opt("--thr", 0.02)); FF = opt("--ffmpeg", "ffmpeg")
video, x0, y0, x1, y1 = a[0], *map(float, a[1:5])
W, H = 480, 270
raw = subprocess.run([FF, "-loglevel", "error", "-i", video, "-t", str(seg), "-vf",
                      f"fps=30,scale={W}:{H},format=gray", "-f", "rawvideo", "-"],
                     capture_output=True, check=True).stdout
fr = np.frombuffer(raw, dtype=np.uint8).reshape(-1, H, W).astype(float)
c = fr[:, int(H*y0):int(H*y1), int(W*x0):int(W*x1)]
d = np.abs(np.diff(c, axis=0)).mean(axis=(1, 2))
moving, start = False, 0
for i, v in enumerate(d):
    t = (i + 1) / 30
    if v > thr and not moving:
        moving, start = True, t
    elif v <= thr and moving:
        moving = False; print(f"mueve {start:.2f} - {t:.2f} s")
if moving:
    print(f"mueve {start:.2f} - {seg:.2f} s")
