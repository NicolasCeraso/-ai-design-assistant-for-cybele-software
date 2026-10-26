# One-command setup of the document pipelines (PPTX, whitepaper, carousel).
# The console itself (node server.js) needs none of this.
#
# Usage (from web-app/, in PowerShell):  .\setup.ps1
# Safe to re-run. Needs: Python 3.13 (py launcher) and Node 18+ already installed.

$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

function Step($n, $text) { Write-Host ""; Write-Host "[$n] $text" -ForegroundColor Cyan }
function Fail($text)     { Write-Host "ERROR: $text" -ForegroundColor Red; exit 1 }

Step 1 'Checking Python 3.13 and Node'
$null = & py -3.13 --version 2>$null
if ($LASTEXITCODE -ne 0) { Fail 'Python 3.13 not found (py -3.13). Install it from python.org and re-run.' }
$null = & node --version 2>$null
if ($LASTEXITCODE -ne 0) { Fail 'Node.js not found. Install Node 18+ and re-run.' }

Step 2 'Python virtual environment (.venv) + libraries'
if (-not (Test-Path '.venv\Scripts\python.exe')) { & py -3.13 -m venv .venv; if ($LASTEXITCODE) { Fail 'venv creation failed' } }
$py = (Resolve-Path '.venv\Scripts\python.exe').Path
& $py -m pip install --quiet --upgrade pip
& $py -m pip install --quiet -r requirements.txt
if ($LASTEXITCODE) { Fail 'pip install failed' }

Step 3 'Chromium for Playwright (renders the whitepaper PDF and the icons)'
& $py -m playwright install chromium
if ($LASTEXITCODE) { Fail 'playwright install failed' }

Step 4 'pptxgenjs (Node decks)'
Push-Location 'deckgen\enterprise_vdi_oci_esp'
& npm install --no-audit --no-fund --silent
$npmExit = $LASTEXITCODE
Pop-Location
if ($npmExit) { Fail 'npm install failed' }

Step 5 'Brand icons: rendering the whole library to PNG (about 1-2 minutes)'
& $py 'deckgen\enterprise_vdi_oci_esp\render_icons.py' | Select-Object -Last 1
& $py 'deckgen\enterprise_vdi_oci_esp\render_diagram_icons.py' | Select-Object -Last 1

Step 6 'Brand font: Inter (static weights, current user)'
try { & "$PSScriptRoot\install-fonts.ps1" } catch { Fail "font install failed: $_" }

Step 7 'Optional tools (warnings only)'
$edge = @('C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe', 'C:\Program Files\Microsoft\Edge\Application\msedge.exe') | Where-Object { Test-Path $_ }
if (-not $edge) { Write-Host 'WARNING: Microsoft Edge not found - the PPTX icon builder (presentations/reference_builder) needs it.' -ForegroundColor Yellow }
$ppt = Get-ItemProperty 'Registry::HKEY_CLASSES_ROOT\PowerPoint.Application' -ErrorAction SilentlyContinue
$lo  = @('C:\Program Files\LibreOffice\program\soffice.exe', 'C:\Program Files (x86)\LibreOffice\program\soffice.exe') | Where-Object { Test-Path $_ }
if (-not $ppt -and -not $lo) {
    # PPTX -> PDF previews need PowerPoint (reference) or LibreOffice (free fallback used by render_pdf.py)
    Write-Host 'No PowerPoint or LibreOffice found - installing LibreOffice for PPTX previews (Windows may ask for permission)...'
    try { & winget install --id TheDocumentFoundation.LibreOffice --source winget --accept-package-agreements --accept-source-agreements } catch {}
    $lo = @('C:\Program Files\LibreOffice\program\soffice.exe', 'C:\Program Files (x86)\LibreOffice\program\soffice.exe') | Where-Object { Test-Path $_ }
    if (-not $lo) { Write-Host 'WARNING: could not install LibreOffice. Decks still build, but PPTX -> PDF previews will fail. Install PowerPoint or LibreOffice by hand.' -ForegroundColor Yellow }
}

Write-Host ""
Write-Host "Setup finished. Python for the pipelines: $py" -ForegroundColor Green
