# Convert a PPTX to PDF for the in-app preview.
# Usage: python render_pdf.py <input.pptx> <output.pdf>
#
# Microsoft PowerPoint (COM) is used when it is installed — it is the reference renderer. Otherwise it
# falls back to LibreOffice in headless mode (free; slightly different fonts/effects, fine for review).
# Set CYBELE_SOFFICE to a soffice.exe path to force a LibreOffice location.
import os, shutil, subprocess, sys, tempfile
from pathlib import Path

src = Path(sys.argv[1]).resolve()
dst = Path(sys.argv[2]).resolve()
dst.parent.mkdir(parents=True, exist_ok=True)


def via_powerpoint():
    import pythoncom
    import win32com.client
    pythoncom.CoInitialize()
    try:
        ppt = win32com.client.Dispatch("PowerPoint.Application")
        ppt.Visible = 1          # some installs reject 0
        ppt.WindowState = 2      # minimized
        deck = ppt.Presentations.Open(str(src), WithWindow=False, ReadOnly=True)
        deck.SaveAs(str(dst), 32)     # 32 = ppFixedFormatTypePDF
        deck.Close()
        ppt.Quit()
    finally:
        pythoncom.CoUninitialize()


def find_soffice():
    cands = [os.environ.get('CYBELE_SOFFICE'),
             shutil.which('soffice'),
             r"C:\Program Files\LibreOffice\program\soffice.exe",
             r"C:\Program Files (x86)\LibreOffice\program\soffice.exe"]
    return next((c for c in cands if c and os.path.exists(c)), None)


def via_libreoffice(soffice):
    with tempfile.TemporaryDirectory() as tmp:
        profile = Path(tmp, 'profile').as_uri()      # private profile: no lock clash with an open LibreOffice
        out = Path(tmp, 'out')
        r = subprocess.run([soffice, f'-env:UserInstallation={profile}', '--headless',
                            '--convert-to', 'pdf', '--outdir', str(out), str(src)],
                           capture_output=True, text=True, timeout=600)
        made = out / (src.stem + '.pdf')
        if r.returncode != 0 or not made.exists():
            raise RuntimeError('LibreOffice conversion failed: ' + (r.stderr or r.stdout).strip()[-300:])
        shutil.move(str(made), str(dst))


engine = None
try:
    via_powerpoint()
    engine = 'PowerPoint'
except Exception as e:                      # not installed (invalid class string), no pywin32, etc.
    soffice = find_soffice()
    if not soffice:
        sys.exit(f'No PowerPoint ({type(e).__name__}) and no LibreOffice found. '
                 'Install one of them (see deckgen/README.md).')
    via_libreoffice(soffice)
    engine = 'LibreOffice'

print("OK", engine, dst, dst.stat().st_size // 1024, "KB")
