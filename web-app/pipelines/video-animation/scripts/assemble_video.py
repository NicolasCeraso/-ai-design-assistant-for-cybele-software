#!/usr/bin/env python3
"""Arma el video final desde los MP4 por escena + la locución, guiado por un JSON.

Uso:  py -3.13 assemble_video.py video.json [salida.mp4] [--4k]

Hace, en este orden:
  1. calcula el inicio/fin de cada escena en el video final (los cortes de la locución más las
     pausas insertadas),
  2. arma el grafo de ffmpeg con las transiciones entre escenas (xfade, expresiones propias),
  3. mezcla el audio: locución (con pausas y silencios), efectos de sonido (nivel relativo a la
     voz), whooshes de transición y música de fondo en loop con ducking,
  4. codifica H.264 (yuv420p, AAC).

Dependencias: ffmpeg en el PATH (o "ffmpeg" en el JSON), Python 3.13 con numpy. Ver
video.example.json para todos los campos.
"""
import json, os, subprocess, sys, wave
import numpy as np

SR = 48000
args = [a for a in sys.argv[1:] if not a.startswith("--")]
if not args:
    sys.exit(__doc__)
CFG_PATH = args[0]
cfg = json.load(open(CFG_PATH, encoding="utf-8-sig"))
BASE = os.path.dirname(os.path.abspath(CFG_PATH))
P4K = "--4k" in sys.argv
FF = cfg.get("ffmpeg", "ffmpeg")
W_OUT, H_OUT = (3840, 2160) if P4K else (cfg.get("width", 1920), cfg.get("height", 1080))


def rel(p):
    return p if os.path.isabs(p) else os.path.join(BASE, p)


OUTV = rel(args[1] if len(args) > 1 else cfg.get("out", "video_final.mp4"))
SCENES_DIR = rel(cfg.get("scenes_dir", "escenas"))
PATTERN = cfg.get("scene_pattern", "Escena_{:02d}.mp4")
# Sin locución NI música NI efectos el video sale SIN audio (sin pista). Con música o efectos pero sin locución sale con esa pista: las escenas duran
# lo que dice "scene_durations" (segundos por escena). Cuando llegue el audio, se completan "voice"
# y "cuts" y se vuelve a armar.
SILENT = not (cfg.get("voice") or (cfg.get("music") or {}).get("file") or cfg.get("sfx") or cfg.get("transition_sfx"))
if SILENT:
    cfg["sfx"], cfg["transition_sfx"], cfg["music"], cfg["pauses"], cfg["voice_mute"] = {}, {}, None, [], []
if "cuts" in cfg:
    CUTS = cfg["cuts"]                  # cortes absolutos en la locución: escena i = CUTS[i-1]..CUTS[i]
else:
    CUTS = [0.0]
    for d_ in cfg["scene_durations"]:
        CUTS.append(CUTS[-1] + d_)
N = len(CUTS) - 1
T0 = CUTS[0]
PAUSES = [(p["at"], p["seconds"]) for p in cfg.get("pauses", [])]
HOLD = {p["hold_scene"]: p["seconds"] for p in cfg.get("pauses", []) if p.get("hold_scene")}


def f(t):                               # tiempo absoluto de la locución -> tiempo del video final
    return t - T0 + sum(d for c, d in PAUSES if t >= c - 1e-6)


B = [f(c) for c in CUTS[1:]]            # B[j] = fin de la escena j+1
S = [0.0] + B[:-1]                      # S[j] = inicio de la escena j+1
TOTAL = B[-1]
vids = [os.path.join(SCENES_DIR, PATTERN.format(i)) for i in range(1, N + 1)]
TR = {int(k): (v[0], v[1]) for k, v in cfg.get("transitions", {}).items()}
for k in range(1, N):
    TR.setdefault(k, ("fade", 0.2))

# ---------- transiciones ----------
EASE = "st(0,1-P);st(1,if(lt(ld(0),0.5),4*pow(ld(0),3),1-pow(-2*ld(0)+2,3)/2));"


def bz(p, n=4000):
    x1, y1, x2, y2 = p
    u = np.linspace(0, 1, n)
    return 3*(1-u)**2*u*x1 + 3*(1-u)*u**2*x2 + u**3, 3*(1-u)**2*u*y1 + 3*(1-u)*u**2*y2 + u**3


# curva de la "parábola" de Nick: cubic-bezier(0.438, 0.145, 0.01, 1)
X_, Y_ = bz(tuple(cfg.get("easing", [0.438, 0.145, 0.01, 1.0])))
tab = np.interp(np.linspace(0, 1, 21), X_, Y_)


def lerp_chain(i=0):
    a, b = i/20, (i+1)/20
    seg = f"{tab[i]:.5f}+(ld(0)-{a:.2f})*{(tab[i+1]-tab[i])*20:.5f}"
    return seg if i == 19 else f"if(lt(ld(0),{b:.2f}),{seg},{lerp_chain(i+1)})"


EASEP = "st(0,1-P);st(1," + lerp_chain() + ");"
PL = "if(eq(PLANE,0),a0(%s,%s),if(eq(PLANE,1),a1(%s,%s),a2(%s,%s)))"
PB = "if(eq(PLANE,0),b0(%s,%s),if(eq(PLANE,1),b1(%s,%s),b2(%s,%s)))"
ax, bx = "(X+ld(1)*W)", "(X-W*(1-ld(1)))"
ay, by = "(Y+ld(1)*H)", "(Y-H*(1-ld(1)))"
EXPR = {
    # panel diagonal que barre de derecha a izquierda
    "diag":    EASE + "if(gt(X-0.6*(H-Y),W-ld(1)*(W+0.6*H)),B,A)",
    # círculo que crece desde el borde derecho
    "circle":  EASE + "if(lt(hypot(X-W,Y-H/2),ld(1)*(hypot(W,H/2)+4)),B,A)",
    # barrido curvo desde la esquina inferior izquierda
    "sweep":   EASE + "if(lt(hypot(X,H-Y),(1-ld(1))*(hypot(W,H)+4)),A,B)",
    # círculo que se cierra hacia el centro (parábola)
    "ccenter": EASEP + "if(lt(hypot(X-W/2,Y-H/2),(1-ld(1))*(hypot(W/2,H/2)+4)),A,B)",
    # empuje lateral (parábola)
    "slide":   EASEP + "if(lt(X,W*(1-ld(1))),"+PL % (ax, "Y", ax, "Y", ax, "Y")+","+PB % (bx, "Y", bx, "Y", bx, "Y")+")",
    # empuje vertical, la nueva escena entra desde abajo (parábola)
    "slidev":  EASEP + "if(lt(Y,H*(1-ld(1))),"+PL % ("X", ay, "X", ay, "X", ay)+","+PB % ("X", by, "X", by, "X", by)+")",
    # el color sólido se expande desde el centro hacia los costados (parábola)
    "band":    EASEP + "if(lt(abs(X-W/2),ld(1)*W/2),B,A)",
}


def xf(kind, d, off):
    if kind == "fade":
        return f"xfade=transition=fade:duration={d}:offset={off:.4f}"
    return f"xfade=transition=custom:duration={d}:offset={off:.4f}:expr='{EXPR[kind]}'"


g = ""
for j in range(N):
    L = B[j] - S[j]
    p = TR[j][1] / 2 if j > 0 else 0
    q = TR[j+1][1] / 2 if j < N - 1 else 0
    ext = HOLD.get(j + 1, 0)            # último cuadro congelado durante la pausa
    g += (f"[{j}:v]trim=duration={L-ext:.4f},setpts=PTS-STARTPTS,fps=30,scale={W_OUT}:{H_OUT}:flags=lanczos,"
          f"format=yuv420p,tpad=start_mode=clone:start_duration={p:.4f}:stop_mode=clone:stop_duration={q+ext:.4f},"
          f"setpts=PTS-STARTPTS[v{j}];\n")
prev = "v0"
for j in range(N - 1):
    kind, d = TR[j + 1]
    off = B[j] - d / 2
    lab = "v" if j == N - 2 else f"x{j}"
    g += f"[{prev}][v{j+1}]{xf(kind, d, off)}[{lab}];\n"
    prev = lab
GRAPH = os.path.join(BASE, "_graph.txt")
open(GRAPH, "w", encoding="utf-8").write(g.rstrip(";\n") + "\n")


# ---------- audio ----------
def load(p):
    raw = subprocess.run([FF, "-loglevel", "error", "-i", p, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


vf = np.zeros(int(CUTS[-1]*SR) + SR, dtype=np.float32) if not cfg.get("voice") else load(rel(cfg["voice"]))
pieces, last = [], T0
for c, d in sorted(PAUSES):
    pieces += [vf[int(last*SR):int(c*SR)], np.zeros(int(d*SR), dtype=np.float32)]
    last = c
pieces.append(vf[int(last*SR):int(CUTS[-1]*SR)])
voice = np.concatenate(pieces)
n = int(TOTAL * SR)
voice = np.pad(voice, (0, max(0, n - len(voice))))[:n]
for a, b in cfg.get("voice_mute", []):  # chasquidos sueltos de la locución
    voice[int(f(a)*SR):int(f(b)*SR)] = 0
master = voice.copy()


def vrms(t):
    seg = voice[int(max(0, t-0.3)*SR):int((t+0.3)*SR)]
    return 20*np.log10(np.sqrt((seg**2).mean())+1e-9) if len(seg) else -90


SFX = rel(cfg.get("sfx_dir", "sfx"))
cache = {}


def eff(fn):
    if fn not in cache:
        x = load(os.path.join(SFX, fn))
        e = np.convolve(np.abs(x), np.ones(480)/480, "same")
        cache[fn] = (x, 20*np.log10(np.abs(x).max()+1e-9), e.argmax()/SR)
    return cache[fn]


def place(fn, t_peak, db):              # alinea el PICO del efecto con t_peak
    x, pk, pt = eff(fn)
    y = x * 10**((db-pk)/20)
    s = int((t_peak-pt)*SR)
    if s < 0:
        y = y[-s:]
        s = 0
    e = min(n, s+len(y))
    master[s:e] += y[:e-s]


for k, L in cfg.get("sfx", {}).items():
    i = int(k)
    for e in L:
        if e.get("seg"):                # tramo del efecto (con loop si hace falta), corta seco al final
            x, pk, _ = eff(e["f"])
            y = np.resize(x[int(e.get("off", 0)*SR):], int(e["dur"]*SR)) * 10**((e["db"]-pk)/20)
            fi, fo = int(0.01*SR), int(0.06*SR)
            y[:fi] *= np.linspace(0, 1, fi)
            y[-fo:] *= np.linspace(1, 0, fo)
            s0 = int((S[i-1]+e["start"])*SR)
            master[s0:s0+len(y)] += y[:max(0, min(len(y), n-s0))]
            continue
        t = S[i-1] + e["at"]
        if e.get("fix"):
            db = e["db"]
        else:                           # nivel automático: la voz local + 4 dB, entre -16 y -8
            r = vrms(t)
            db = -14 if r < -35 else max(-16, min(-8, r+4))
        place(e["f"], t, db)
for k, v in cfg.get("transition_sfx", {}).items():   # whoosh en el corte k -> k+1
    place(v[0], B[int(k)-1], v[1] if len(v) > 1 else -11)

mus_cfg = cfg.get("music")
if mus_cfg and mus_cfg.get("file"):
    mus = load(rel(mus_cfg["file"]))
    XF = int(mus_cfg.get("crossfade", 2.0)*SR)

    def loop(x, total):
        out = x.copy()
        while len(out) < total:
            w = np.linspace(0, 1, XF)
            cross = out[-XF:]*np.cos(w*np.pi/2) + x[:XF]*np.sin(w*np.pi/2)
            out = np.concatenate([out[:-XF], cross, x[XF:]])
        return out[:total]

    mus = loop(mus, n)
    mus *= 10**((-20 - 20*np.log10(np.sqrt((mus**2).mean())+1e-9))/20)
    w = int(0.05*SR)
    env = np.sqrt(np.convolve(voice**2, np.ones(w)/w, "same"))
    act = (20*np.log10(env+1e-9) > -42).astype(float)

    def smooth(x, att, rel_):
        y = np.zeros_like(x)
        c = 0.0
        ka, kr = np.exp(-1/(att*SR)), np.exp(-1/(rel_*SR))
        for i in range(0, len(x), 48):
            t = x[i]
            c = (ka*c+(1-ka)*t) if t > c else (kr*c+(1-kr)*t)
            y[i:i+48] = c
        return y

    act = smooth(act, 0.12, 0.7)
    idle, talk = mus_cfg.get("idle_db", -7.0), mus_cfg.get("voice_db", -16.0)
    gain_db = idle + (talk - idle) * act
    t = np.arange(n) / SR
    master += (mus * 10**(gain_db/20) * np.minimum(1, t/mus_cfg.get("fade_in", 2.0))
               * np.minimum(1, (TOTAL-t)/mus_cfg.get("fade_out", 3.0))).astype(np.float32)

m = np.abs(master).max()
if m > 0.97:
    master *= 0.97/m
AUDIO = os.path.join(BASE, "_master_audio.wav")
with wave.open(AUDIO, "wb") as wv:
    wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR)
    wv.writeframes((np.clip(master, -1, 1)*32767).astype(np.int16).tobytes())

# ---------- codificación ----------
ins = []
for v in vids:
    ins += ["-i", v]
if not SILENT:
    ins += ["-i", AUDIO]
amap = ["-an"] if SILENT else ["-map", f"{N}:a", "-c:a", "aac", "-b:a", "192k"]
cmd = [FF, "-y", "-loglevel", "error"] + ins + [
    "-/filter_complex", GRAPH, "-map", "[v]"] + amap + [
    "-c:v", "libx264", "-crf", str(cfg.get("crf", 17)), "-preset", "medium", "-pix_fmt", "yuv420p",
    "-movflags", "+faststart", "-t", f"{TOTAL:.3f}", OUTV]
r = subprocess.run(cmd, capture_output=True, text=True)
print(f"OK  {TOTAL:.2f} s -> {OUTV}" if r.returncode == 0 else "ERROR " + r.stderr[-1500:])
if r.returncode == 0 and cfg.get("preview_low", True) and not P4K:
    # rendición BAJA (720p) para la preview por defecto: <nombre>_low.mp4 junto al maestro
    LOW = os.path.splitext(OUTV)[0] + "_low.mp4"
    rl = subprocess.run([FF, "-y", "-loglevel", "error", "-i", OUTV, "-vf", "scale=-2:'min(720,ih)'", "-c:v", "libx264",
                         "-crf", "29", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "96k",
                         "-movflags", "+faststart", LOW], capture_output=True, text=True)
    print(f"preview baja -> {LOW}" if rl.returncode == 0 else "ERROR preview " + rl.stderr[-500:])
print("inicios de escena:", [round(x, 2) for x in S])
