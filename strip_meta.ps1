<#
 Usuń wszystkie metadane z plików:
  • JPG/JPEG/PNG  – ExifTool
  • MP3           – ExifTool (ID3) + weryfikacja FFprobe
  • MP4           – ExifTool + bezstratny remux FFmpeg (-map_metadata -1)
#>

param(
    [string]$TargetDir = "C:\xampp\htdocs\kinga_dramatic"
)

# ─── Funkcja pomocnicza ───────────────────────────────────────────────────────────
function ExecOrThrow ($cmd, $args) {
    $p = Start-Process -FilePath $cmd -ArgumentList $args -NoNewWindow -Wait -PassThru
    if ($p.ExitCode -ne 0) { throw "Błąd [$cmd $args]" }
}

# ─── 1. Przejdź do katalogu docelowego ───────────────────────────────────────────
if (-not (Test-Path $TargetDir)) { throw "Folder nie istnieje: $TargetDir" }
Set-Location $TargetDir

# ─── 2. Zbieramy pliki do obróbki ────────────────────────────────────────────────
$filters = '*.jpg','*.jpeg','*.png','*.mp3','*.mp4'
$files   = Get-ChildItem -File -Include $filters -Recurse

if (-not $files) {
    Write-Host "Brak plików do czyszczenia." -ForegroundColor Yellow
    exit
}

# ─── 3. Przetwarzamy każdy plik ──────────────────────────────────────────────────
foreach ($f in $files) {
    Write-Host "`n→ [$($f.Extension.ToUpper())] $($f.FullName)" -ForegroundColor Cyan

    switch -Regex ($f.Extension) {
        '\.(jpe?g|png)$' {
            ExecOrThrow ".\exiftool.exe" "-all= -overwrite_original `"$($f.FullName)`""
        }

        '\.mp3$' {
            ExecOrThrow ".\exiftool.exe" "-all= -overwrite_original `"$($f.FullName)`""
            # weryfikacja – brak tagów?
            $tags = & ffprobe -v error -show_entries format_tags -of compact=p=0:s=_ "$($f.FullName)"
            if ($tags) { Write-Warning "   Pozostałe tagi: $tags" }
        }

        '\.mp4$' {
            # 1) ExifTool usuwa nietypowe atomy
            ExecOrThrow ".\exiftool.exe" "-all= -overwrite_original `"$($f.FullName)`""
            # 2) FFmpeg remux bez metadanych
            $tmp = "$($f.DirectoryName)\$($f.BaseName)_clean$($f.Extension)"
            ExecOrThrow "ffmpeg" "-y -i `"$($f.FullName)`" -map_metadata -1 -c copy `"$tmp`""
            Move-Item $tmp $f.FullName -Force
        }
    }
}

Write-Host "`n✔  Zakończono. Wszystkie dostępne metadane wyczyszczone." -ForegroundColor Green
