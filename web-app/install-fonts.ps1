# Installs the Inter font (static weights) for the CURRENT USER - no admin rights needed.
#
# Why: the Cybele brand font is Inter. Only the *variable* Inter renders hairline-thin in
# PowerPoint/LibreOffice, so the decks and whitepapers need the static Regular/Medium/SemiBold/Bold.
# Inter is open source (SIL OFL), downloaded from its official release instead of being kept in the repo.
#
# Usage (PowerShell):  .\install-fonts.ps1
# Safe to re-run: weights that are already installed are skipped.

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

$Version = '4.0'
$Url     = "https://github.com/rsms/inter/releases/download/v$Version/Inter-$Version.zip"
$Weights = @('Regular', 'Medium', 'SemiBold', 'Bold')

$FontDir = Join-Path $env:LOCALAPPDATA 'Microsoft\Windows\Fonts'
$RegKey  = 'HKCU:\Software\Microsoft\Windows NT\CurrentVersion\Fonts'
New-Item -ItemType Directory -Force $FontDir | Out-Null
if (-not (Test-Path $RegKey)) { New-Item -Path $RegKey -Force | Out-Null }

function Test-Installed($weight) {
    (Test-Path (Join-Path $FontDir "Inter-$weight.ttf")) -and
    ($null -ne (Get-ItemProperty -Path $RegKey -Name "Inter $weight (TrueType)" -ErrorAction SilentlyContinue))
}

$missing = @($Weights | Where-Object { -not (Test-Installed $_) })
if ($missing.Count -eq 0) {
    Write-Host "Inter ($($Weights -join ', ')) already installed - nothing to do."
    exit 0
}

$tmp = Join-Path ([IO.Path]::GetTempPath()) ("inter_" + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Force $tmp | Out-Null
try {
    Write-Host "Downloading Inter $Version ..."
    $zip = Join-Path $tmp 'inter.zip'
    Invoke-WebRequest -Uri $Url -OutFile $zip -UseBasicParsing

    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $archive = [IO.Compression.ZipFile]::OpenRead($zip)
    try {
        foreach ($w in $missing) {
            $entry = $archive.Entries | Where-Object { $_.FullName -eq "extras/ttf/Inter-$w.ttf" } | Select-Object -First 1
            if (-not $entry) { throw "Inter-$w.ttf not found in the release zip" }
            $dest = Join-Path $FontDir "Inter-$w.ttf"
            [IO.Compression.ZipFileExtensions]::ExtractToFile($entry, $dest, $true)
            New-ItemProperty -Path $RegKey -Name "Inter $w (TrueType)" -Value $dest -PropertyType String -Force | Out-Null
            Write-Host "  installed Inter $w"
        }
    } finally { $archive.Dispose() }
    Write-Host "Done. Restart PowerPoint / the browser if they were open so they pick the font up."
} finally {
    Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
}
