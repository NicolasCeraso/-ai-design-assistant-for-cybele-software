#!/usr/bin/env python3
"""Contact sheet de un video en los instantes que le pidas.

Uso:  py -3.13 contact_sheet.py video.mp4 salida.png t1 t2 t3 ... [--cols 6] [--w 480] [--ffmpeg ruta]

Extrae un cuadro por instante (segundos), los numera y los une en una sola imagen para mirarla con
Read. Usalo alrededor de cada transición y de cada cambio pedido: es la forma de "ver" un video
sin reproducirlo.
"""
import os, subprocess, sys, tempfile

a = sys.argv[1:]
def opt(name, default):
    if name in a:
        i = a.index(name); v = a[i+1]; del a[i:i+2]; return v
    return default
cols = int(opt("--cols", 6)); w = int(opt("--w", 480)); FF = opt("--ffmpeg", "ffmpeg")
video, out, times = a[0], a[1], a[2:]
tmp = tempfile.mkdtemp()
for i, t in enumerate(times, 1):
    subprocess.run([FF, "-y", "-loglevel", "error", "-ss", t, "-i", video, "-frames:v", "1",
                    "-vf", f"scale={w}:-1", os.path.join(tmp, f"s_{i:03d}.png")], check=True)
rows = -(-len(times) // cols)
subprocess.run([FF, "-y", "-loglevel", "error", "-framerate", "1", "-i", os.path.join(tmp, "s_%03d.png"),
                "-vf", f"tile={cols}x{rows}", "-frames:v", "1", out], check=True)
print("OK", out, "orden:", " ".join(times))
