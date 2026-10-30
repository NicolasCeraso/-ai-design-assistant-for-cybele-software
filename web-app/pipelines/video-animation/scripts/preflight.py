#!/usr/bin/env python3
"""Chequeo previo del pipeline de video (todo lo que se puede comprobar fuera de Figma).

Uso:  py -3.13 preflight.py [video.json]

Comprueba: Python >= 3.13 con numpy, ffmpeg (CYBELE_FFMPEG, PATH o WinGet), el códec libx264 y,
si se pasa video.json, que existan la locución, la música, la carpeta de SFX y los MP4 de escena.
Sale con código 1 si falta algo imprescindible. El chequeo del MOTION de Figma NO se puede hacer
desde acá: se hace con `use_figma` (ver SKILL.md, paso 0).
"""
import glob, json, os, shutil, subprocess, sys

bad = []
def check(ok, msg):
    print(("OK    " if ok else "FALTA ") + msg)
    if not ok:
        bad.append(msg)

check(sys.version_info >= (3, 13), f"Python {sys.version.split()[0]} (se pide 3.13+)")
try:
    import numpy
    check(True, f"numpy {numpy.__version__}")
except ImportError:
    check(False, "numpy (pip install numpy)")

cands = [os.environ.get("CYBELE_FFMPEG"), shutil.which("ffmpeg")]
cands += glob.glob(os.path.join(os.path.expanduser("~"), "AppData", "Local", "Microsoft", "WinGet", "Packages",
                                "Gyan.FFmpeg*", "ffmpeg-*", "bin", "ffmpeg.exe"))
ff = next((c for c in cands if c and os.path.exists(c)), None)
check(bool(ff), f"ffmpeg: {ff}" if ff else "ffmpeg (winget install Gyan.FFmpeg, o CYBELE_FFMPEG)")
if ff:
    enc = subprocess.run([ff, "-hide_banner", "-encoders"], capture_output=True, text=True).stdout
    check("libx264" in enc, "códec libx264")
    check("libvpx-vp9" in enc, "códec libvpx-vp9 (sólo para exportar WebM)")

if len(sys.argv) > 1:
    base = os.path.dirname(os.path.abspath(sys.argv[1]))
    cfg = json.load(open(sys.argv[1], encoding="utf-8-sig"))
    rel = lambda p: p if os.path.isabs(p) else os.path.join(base, p)
    if cfg.get("voice"):
        check(os.path.exists(rel(cfg["voice"])), "locución: " + cfg["voice"])
    else:
        print("AVISO sin locución: el video saldrá SIN audio (se completa \"voice\" y \"cuts\" cuando llegue el audio)")
    m = (cfg.get("music") or {}).get("file")
    if m:
        check(os.path.exists(rel(m)), "música: " + m)
    sfx = rel(cfg.get("sfx_dir", "sfx"))
    used = {e["f"] for v in cfg.get("sfx", {}).values() for e in v} | {v[0] for v in cfg.get("transition_sfx", {}).values()}
    check(all(os.path.exists(os.path.join(sfx, f)) for f in used), f"{len(used)} efectos de sonido en {sfx}")
    d = rel(cfg.get("scenes_dir", "escenas"))
    n = len(cfg["cuts"]) - 1 if "cuts" in cfg else len(cfg["scene_durations"])
    miss = [i for i in range(1, n + 1) if not os.path.exists(os.path.join(d, cfg.get("scene_pattern", "Escena_{:02d}.mp4").format(i)))]
    check(not miss, f"{n} MP4 de escena en {d}" + (f" (faltan: {miss})" if miss else ""))

print("\nPreflight " + ("OK" if not bad else "con faltantes: " + "; ".join(bad)))
sys.exit(1 if bad else 0)
