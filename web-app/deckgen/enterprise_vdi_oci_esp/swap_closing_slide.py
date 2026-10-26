"""Replace the last slide of the built deck with slide 1 from cierre.pptx, exactly.
This produces an editable PowerPoint slide (clickable in PPT/Google Slides UI).
Additionally: swap the 9.8 MB image7.gif decoration for a static thinfinity_icon_white.png
to reduce file size and ensure rendering in static viewers.
"""

import zipfile
import shutil
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
DECK = HERE / "output" / "Enterprise_VDI_OCI_Discovery_Demo_ESP.pptx"
CIERRE = HERE.parents[2] / "presentations" / "assets" / "cierre.pptx"   # repo root
THINFINITY_PNG = HERE.parent / "brand_assets" / "thinfinity_icon_white.png"
TMP = HERE / "output" / "_swap_tmp"
OUT = HERE / "output" / "_swap_out.pptx"


def main():
    if TMP.exists():
        shutil.rmtree(TMP)
    TMP.mkdir(parents=True)

    # 1. Unzip both
    deck_dir = TMP / "deck"; cierre_dir = TMP / "cierre"
    deck_dir.mkdir(); cierre_dir.mkdir()
    with zipfile.ZipFile(DECK) as zf: zf.extractall(deck_dir)
    with zipfile.ZipFile(CIERRE) as zf: zf.extractall(cierre_dir)

    # 2. Target = last slide
    slides = sorted((deck_dir / "ppt" / "slides").glob("slide*.xml"),
                    key=lambda p: int(re.search(r'\d+', p.stem).group()))
    target_path = slides[-1]
    target_idx = int(re.search(r'\d+', target_path.stem).group())
    target_rels = deck_dir / "ppt" / "slides" / "_rels" / f"slide{target_idx}.xml.rels"
    print(f"Target: slide{target_idx}.xml")

    # 3. Determine fresh image numbering
    deck_media = deck_dir / "ppt" / "media"; deck_media.mkdir(exist_ok=True)
    existing = list(deck_media.glob("image*"))
    max_num = max([int(m.group(1)) for f in existing
                   if (m := re.search(r'^image(\d+)$', f.stem))] + [0])

    # 4. Get cierre media refs (in rels)
    cierre_rels_text = (cierre_dir / "ppt" / "slides" / "_rels" / "slide1.xml.rels").read_text(encoding="utf-8")
    refs = list(dict.fromkeys(re.findall(
        r'Target="\.\./media/(image\d+\.(?:png|gif|jpe?g))"', cierre_rels_text)))

    # 5. Copy each cierre image to deck media with fresh names — INCLUDING the
    #    animated image7.gif (Thinfinity rotation) so the closing keeps its motion.
    name_map = {}
    for i, old in enumerate(refs):
        ext_old = old.rsplit('.', 1)[1]
        new_num = max_num + 1 + i
        new = f"image{new_num}.{ext_old}"
        src = cierre_dir / "ppt" / "media" / old
        shutil.copy2(src, deck_media / new)
        name_map[old] = new
        print(f"  {old:>15}  ->  {new}")

    # 6. Rewrite rels: map old image names to new via two-pass (temp names first to avoid
    #    sequential rename collisions when both old and new sets overlap, e.g. image2→image1
    #    followed by image3→image2 would corrupt the first step).
    new_rels = cierre_rels_text
    for i, old in enumerate(name_map):
        new_rels = new_rels.replace(f"media/{old}", f"media/__TMP_{i}__")
    for i, (old, new) in enumerate(name_map.items()):
        new_rels = new_rels.replace(f"media/__TMP_{i}__", f"media/{new}")
    new_rels = new_rels.replace("notesSlides/notesSlide1.xml",
                                f"notesSlides/notesSlide{target_idx}.xml")

    # 7. Slide XML itself: keep as-is (rels file owns the file mapping)
    slide_xml = (cierre_dir / "ppt" / "slides" / "slide1.xml").read_text(encoding="utf-8")

    target_path.write_text(slide_xml, encoding="utf-8")
    target_rels.write_text(new_rels, encoding="utf-8")
    print(f"Replaced slide{target_idx}.xml + rels")

    # 8. Repackage
    if OUT.exists(): OUT.unlink()
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in deck_dir.rglob("*"):
            if path.is_file():
                zf.write(path, path.relative_to(deck_dir).as_posix())

    shutil.move(OUT, DECK)
    shutil.rmtree(TMP)
    print(f"\nOK -> {DECK}")


if __name__ == "__main__":
    main()
