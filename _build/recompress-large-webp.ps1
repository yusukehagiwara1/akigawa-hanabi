# recompress-large-webp.ps1
# Re-encodes WebP images in assets/wp/ at quality 72 (visually equivalent
# to 80 for photographs) using cwebp's slowest / highest-effort method.
# Only replaces the original when the new file is ≥20% smaller, to avoid
# noisy churn. Originals stay in git history.

[CmdletBinding()]
param(
  [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path,
  [int]$Quality = 72,
  [int]$MinSizeBytes = 100000,    # only process files larger than 100 KB
  [double]$MinReduction = 0.20    # require ≥20% smaller to keep new version
)

# Don't stop on native-command stderr output (dwebp / cwebp emit progress
# to stderr which PowerShell would otherwise treat as error).
$ErrorActionPreference = "Continue"

$bin = "C:\Users\hagiy\AppData\Local\Microsoft\WinGet\Packages\Google.Libwebp_Microsoft.Winget.Source_8wekyb3d8bbwe\libwebp-1.6.0-windows-x64\bin"
$dwebp = Join-Path $bin "dwebp.exe"
$cwebp = Join-Path $bin "cwebp.exe"
if (-not (Test-Path $dwebp)) { throw "dwebp.exe not found at $dwebp" }
if (-not (Test-Path $cwebp)) { throw "cwebp.exe not found at $cwebp" }

$wpDir = Join-Path $Root "assets\wp"
if (-not (Test-Path $wpDir)) { throw "assets\wp not found" }

$candidates = Get-ChildItem -Path $wpDir -Filter "*.webp" -File | Where-Object { $_.Length -ge $MinSizeBytes }
Write-Host "Found $($candidates.Count) WebP files >= $([Math]::Round($MinSizeBytes/1024)) KB"

$savedTotal = 0
$replacedCount = 0
$skippedCount = 0
$tmpPng = Join-Path $env:TEMP "recompress-$(Get-Random).png"
$tmpOut = Join-Path $env:TEMP "recompress-$(Get-Random).webp"

foreach ($f in $candidates) {
  # Decode original to PNG (lossless). Redirect stderr to a discard stream
  # because dwebp emits informational lines there.
  Remove-Item $tmpPng -ErrorAction SilentlyContinue
  Remove-Item $tmpOut -ErrorAction SilentlyContinue
  $null = & $dwebp $f.FullName -o $tmpPng -quiet 2>&1
  if (-not (Test-Path $tmpPng) -or (Get-Item $tmpPng).Length -eq 0) {
    Write-Host "  SKIP $($f.Name): dwebp failed"
    $skippedCount++
    continue
  }
  # Re-encode at target quality with max effort
  $null = & $cwebp -q $Quality -m 6 -mt -quiet $tmpPng -o $tmpOut 2>&1
  if (-not (Test-Path $tmpOut) -or (Get-Item $tmpOut).Length -eq 0) {
    Write-Host "  SKIP $($f.Name): cwebp failed"
    $skippedCount++
    continue
  }
  $orig = $f.Length
  $new = (Get-Item $tmpOut).Length
  $reduction = ($orig - $new) / $orig
  if ($reduction -ge $MinReduction) {
    Copy-Item $tmpOut $f.FullName -Force
    $savedTotal += ($orig - $new)
    $replacedCount++
    Write-Host ("  OK   {0,-50} {1,6} -> {2,6} KB ({3:P0} reduction)" -f $f.Name, [Math]::Round($orig/1024), [Math]::Round($new/1024), $reduction)
  } else {
    $skippedCount++
    Write-Host ("  KEEP {0,-50} only {1:P0} reduction" -f $f.Name, $reduction)
  }
}

Remove-Item $tmpPng -ErrorAction SilentlyContinue
Remove-Item $tmpOut -ErrorAction SilentlyContinue

Write-Host ""
Write-Host ("=== TOTAL: {0} replaced, {1} kept, {2} KB saved ({3} MB) ===" -f $replacedCount, $skippedCount, [Math]::Round($savedTotal/1024), [Math]::Round($savedTotal/1048576, 2))
