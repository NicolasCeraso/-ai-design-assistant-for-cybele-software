# Convert a PPTX to PDF via PowerPoint COM (for in-app preview).
# Usage: py -3 render_pdf.py <input.pptx> <output.pdf>
import sys
from pathlib import Path
import pythoncom
import win32com.client

src = str(Path(sys.argv[1]).resolve())
dst = str(Path(sys.argv[2]).resolve())

pythoncom.CoInitialize()
try:
    ppt = win32com.client.Dispatch("PowerPoint.Application")
    ppt.Visible = 1          # some installs reject 0
    ppt.WindowState = 2      # minimized
    deck = ppt.Presentations.Open(src, WithWindow=False, ReadOnly=True)
    deck.SaveAs(dst, 32)     # 32 = ppFixedFormatTypePDF
    deck.Close()
    ppt.Quit()
    print("OK", dst, Path(dst).stat().st_size // 1024, "KB")
finally:
    pythoncom.CoUninitialize()
