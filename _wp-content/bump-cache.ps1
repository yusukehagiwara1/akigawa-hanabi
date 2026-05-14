# bump-cache.ps1
# Auto-bumps the cache-buster (`?v=YYYYMMDD<letter>`) across all HTML files
# and bumps the Service Worker CACHE_VERSION integer to match. Run once
# per deploy that ships CSS/JS/SW changes.
#
# Usage:
#   .\bump-cache.ps1           # picks the next letter automatically
#   .\bump-cache.ps1 -DryRun   # preview without writing

[CmdletBinding()]
param(
  [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path,
  [switch]$DryRun
)

$today = (Get-Date).ToString("yyyyMMdd")

# Find the latest version suffix across HTML files.
$swPath = Join-Path $Root "sw.js"
$sw = [System.IO.File]::ReadAllText($swPath, [System.Text.Encoding]::UTF8)
$swMatch = [regex]::Match($sw, 'CACHE_VERSION\s*=\s*"akigawa-hanabi-v(\d+)"')
if (-not $swMatch.Success) {
  throw "Could not find CACHE_VERSION in sw.js"
}
$swInt = [int]$swMatch.Groups[1].Value

# Scan one HTML file to find current version suffix
$indexHtml = [System.IO.File]::ReadAllText((Join-Path $Root "index.html"), [System.Text.Encoding]::UTF8)
$vMatch = [regex]::Match($indexHtml, '\?v=(\d{8})([a-z]+)')
if (-not $vMatch.Success) {
  throw "Could not find current ?v= cache buster in index.html"
}
$curDate = $vMatch.Groups[1].Value
$curLetter = $vMatch.Groups[2].Value

# Compute next version. Strategy:
#  - today > curDate  → use today + "a" (new day)
#  - today == curDate → increment letter (a→b, z→aa, az→ba)
#  - today < curDate  → keep curDate + increment letter (manual override
#                       earlier may have advanced the date; never roll
#                       backward).
function Step-Letter([string]$letter) {
  $chars = $letter.ToCharArray()
  $i = $chars.Length - 1
  $carry = $true
  while ($i -ge 0 -and $carry) {
    if ($chars[$i] -eq 'z') {
      $chars[$i] = 'a'
      $carry = $true
    } else {
      $chars[$i] = [char]([int]$chars[$i] + 1)
      $carry = $false
    }
    $i--
  }
  $result = -join $chars
  if ($carry) { $result = "a" + $result }
  return $result
}

if ($today -gt $curDate) {
  $newDate = $today
  $newLetter = "a"
} else {
  # today == curDate OR today < curDate (don't roll backward)
  $newDate = $curDate
  $newLetter = Step-Letter $curLetter
}

$oldVer = "$curDate$curLetter"
$newVer = "$newDate$newLetter"
$newSwInt = $swInt + 1

Write-Host "  Current: ?v=$oldVer  /  CACHE_VERSION v$swInt"
Write-Host "  Next:    ?v=$newVer  /  CACHE_VERSION v$newSwInt"
Write-Host ""

if ($DryRun) {
  Write-Host "DRY RUN — not writing."
  return
}

# Update all HTML files
$htmlChanged = 0
Get-ChildItem -Path $Root -Filter "*.html" -File | ForEach-Object {
  $content = [System.IO.File]::ReadAllText($_.FullName, [System.Text.Encoding]::UTF8)
  $original = $content
  $content = [regex]::Replace($content, "\?v=$([regex]::Escape($oldVer))\b", "?v=$newVer")
  if ($content -ne $original) {
    $utf8Bom = New-Object System.Text.UTF8Encoding $true
    [System.IO.File]::WriteAllText($_.FullName, $content, $utf8Bom)
    $htmlChanged++
  }
}
Write-Host "  Updated $htmlChanged HTML files."

# Update SW
$swNew = [regex]::Replace($sw, 'CACHE_VERSION\s*=\s*"akigawa-hanabi-v\d+"', "CACHE_VERSION = `"akigawa-hanabi-v$newSwInt`"")
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText($swPath, $swNew, $utf8NoBom)
Write-Host "  Updated sw.js."

Write-Host ""
Write-Host "Done. New cache identity: ?v=$newVer / CACHE_VERSION v$newSwInt"
