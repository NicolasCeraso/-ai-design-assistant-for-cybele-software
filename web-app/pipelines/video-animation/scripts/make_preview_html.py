#!/usr/bin/env python3
"""Escribe preview.html para el entregable de video: reproductor con calidad BAJA por defecto.

Uso:  py -3.13 make_preview_html.py carpeta_de_salida [titulo]

Busca en la carpeta:  video_low.mp4 (720p, la preview por defecto), video.mp4 (maestro, "Alta"),
y opcionalmente video_medium.mp4 y contact_sheet.png. Arranca con la calidad más baja que exista
(baja → media → alta), deja cambiar de calidad sin perder el punto de reproducción y no precarga
más que los metadatos. Los videos se referencian por ruta relativa: funciona dentro del iframe de
la consola (el servidor entrega mp4 con soporte de Range) y abriendo el archivo directamente.
"""
import html, os, sys

folder = sys.argv[1]
title = sys.argv[2] if len(sys.argv) > 2 else "Animated Video"
opts = [("low", "Baja · 720p", "video_low.mp4"), ("medium", "Media · 1080p", "video_medium.mp4"),
        ("high", "Alta · original", "video.mp4")]
have = [(k, lb, f) for k, lb, f in opts if os.path.exists(os.path.join(folder, f))]
if not have:
    sys.exit("No hay video en " + folder)
first = have[0]
sheet = os.path.exists(os.path.join(folder, "contact_sheet.png"))
options = "".join(f'<option value="{f}"{" selected" if f == first[2] else ""}>{html.escape(lb)}</option>' for k, lb, f in have)
page = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<style>
:root{{--bg:#fff;--fg:#0a1530;--mut:#5b6785;--line:#d6dcea}}
@media (prefers-color-scheme:dark){{:root{{--bg:#050b1a;--fg:#e8edf8;--mut:#8f9bb8;--line:#1f2a45}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font:14px/1.5 Inter,system-ui,sans-serif}}
main{{max-width:1100px;margin:0 auto;padding:16px}}
video{{width:100%;background:#000;border-radius:8px;display:block}}
.bar{{display:flex;gap:12px;align-items:center;margin:10px 0;color:var(--mut)}}
select{{background:var(--bg);color:var(--fg);border:1px solid var(--line);border-radius:6px;padding:4px 8px}}
img{{width:100%;border:1px solid var(--line);border-radius:8px;margin-top:12px}}
</style></head><body><main>
<video id="v" controls preload="metadata" src="{first[2]}"></video>
<div class="bar"><label for="q">Calidad</label><select id="q">{options}</select>
<span>La preview arranca en baja calidad; la descarga permite elegir formato y calidad.</span></div>
{'<img src="contact_sheet.png" alt="Contact sheet">' if sheet else ''}
</main>
<script>
const v=document.getElementById('v'),q=document.getElementById('q');
q.addEventListener('change',()=>{{const t=v.currentTime,p=!v.paused;v.src=q.value;
  v.addEventListener('loadedmetadata',()=>{{v.currentTime=t;if(p)v.play();}},{{once:true}});}});
</script></body></html>
"""
open(os.path.join(folder, "preview.html"), "w", encoding="utf-8").write(page)
print("OK", os.path.join(folder, "preview.html"), "calidad inicial:", first[1])
