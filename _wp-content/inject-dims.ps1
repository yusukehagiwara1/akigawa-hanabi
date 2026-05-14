# inject-dims.ps1
# Adds width/height attributes to <img> tags in HTML files based on the
# natural dimensions captured in _image-dims.tsv. Idempotent: skips tags
# that already have width= or height= set.

[CmdletBinding()]
param(
  [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
)

$ErrorActionPreference = "Stop"

$tsvPath = Join-Path $Root "_image-dims.tsv"
if (-not (Test-Path $tsvPath)) {
  throw "Missing $tsvPath -- run the inventory step first."
}

# Build lookup: relative path -> "WxH"
$dims = @{}
Get-Content $tsvPath -Encoding utf8 | ForEach-Object {
  $parts = $_ -split "`t"
  if ($parts.Length -ge 2 -and $parts[1] -match '(\d+)\s*x\s*(\d+)') {
    $dims[$parts[0].Trim()] = @{ W = [int]$matches[1]; H = [int]$matches[2] }
  }
}
Write-Host "Loaded $($dims.Count) image dimensions"

# Process all HTML files at root + any in subdirs we manage
$htmlFiles = Get-ChildItem -Path $Root -Filter "*.html" -File
$totalUpdated = 0
$totalSkipped = 0
$totalUnknown = 0

foreach ($file in $htmlFiles) {
  $content = Get-Content -LiteralPath $file.FullName -Raw -Encoding utf8
  $original = $content
  $fileUpdated = 0
  $fileSkipped = 0
  $fileUnknown = @()

  # Match <img ... > tags. Non-greedy, case-insensitive.
  $pattern = '<img\b[^>]*?>'
  $content = [regex]::Replace($content, $pattern, {
    param($m)
    $tag = $m.Value
    # Skip if already has width or height attribute
    if ($tag -match '(?i)\swidth\s*=' -or $tag -match '(?i)\sheight\s*=') {
      $script:fileSkipped++
      return $tag
    }
    # Extract src
    if ($tag -notmatch '(?i)\ssrc\s*=\s*"([^"]+)"') { return $tag }
    $src = $matches[1]
    # Normalize: drop leading slash, drop query/hash
    $norm = $src -replace '^/', '' -replace '[\?#].*$', ''
    if (-not $dims.ContainsKey($norm)) {
      $script:fileUnknown += $norm
      return $tag
    }
    $w = $dims[$norm].W
    $h = $dims[$norm].H
    # Inject right after src="..." attribute
    $updated = [regex]::Replace($tag, '(?i)(\ssrc\s*=\s*"[^"]+")', "`$1 width=`"$w`" height=`"$h`"", 1)
    $script:fileUpdated++
    return $updated
  })

  if ($content -ne $original) {
    # Preserve UTF-8 with BOM for Japanese content
    $utf8Bom = New-Object System.Text.UTF8Encoding $true
    [System.IO.File]::WriteAllText($file.FullName, $content, $utf8Bom)
    Write-Host ("  {0}: +{1} updated, {2} skipped (already had dims), {3} unknown src" -f $file.Name, $fileUpdated, $fileSkipped, $fileUnknown.Count)
    $totalUpdated += $fileUpdated
  } else {
    Write-Host ("  {0}: no change ({1} skipped, {2} unknown)" -f $file.Name, $fileSkipped, $fileUnknown.Count)
  }
  $totalSkipped += $fileSkipped
  $totalUnknown += $fileUnknown.Count
  if ($fileUnknown.Count -gt 0 -and $fileUnknown.Count -le 5) {
    foreach ($u in $fileUnknown) { Write-Host "      unknown: $u" }
  }
}

Write-Host ""
Write-Host ("=== TOTAL: {0} updated, {1} skipped, {2} unknown src ===" -f $totalUpdated, $totalSkipped, $totalUnknown)
