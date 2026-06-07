# validate-site.ps1
# Pre-deploy sanity check: validates JSON-LD, internal links, SW precache.
# Returns non-zero exit code if any issue found.
#
# Usage:
#   .\validate-site.ps1

[CmdletBinding()]
param(
  [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
)

$ErrorActionPreference = "Continue"
$failures = 0

function Section($name) {
  Write-Host ""
  Write-Host "== $name ==" -ForegroundColor Cyan
}

# 1) JSON-LD parses cleanly on every HTML
Section "JSON-LD validation"
$blocksOk = 0
$blocksErr = 0
Get-ChildItem -Path $Root -Filter "*.html" -File | ForEach-Object {
  $content = [System.IO.File]::ReadAllText($_.FullName, [System.Text.Encoding]::UTF8)
  $matches = [regex]::Matches($content, '(?s)<script type="application/ld\+json">(.*?)</script>')
  foreach ($m in $matches) {
    try {
      $m.Groups[1].Value | ConvertFrom-Json | Out-Null
      $blocksOk++
    } catch {
      Write-Host "  FAIL: $($_.Name): $($_.Exception.Message)"
      $blocksErr++
    }
  }
}
Write-Host "  $blocksOk blocks OK, $blocksErr errors"
if ($blocksErr -gt 0) { $failures++ }

# 2) Internal HTML links resolve
Section "Internal HTML link resolution"
$existing = @{}
Get-ChildItem -Path $Root -Filter "*.html" -File | ForEach-Object { $existing[$_.Name] = $true }
$broken = @()
Get-ChildItem -Path $Root -Filter "*.html" -File | ForEach-Object {
  $name = $_.Name
  $content = [System.IO.File]::ReadAllText($_.FullName, [System.Text.Encoding]::UTF8)
  foreach ($m in [regex]::Matches($content, 'href="([a-zA-Z0-9_-]+\.html)(?:#[^"]*)?"')) {
    $target = $m.Groups[1].Value
    if (-not $existing.ContainsKey($target)) {
      $broken += "$name -> $target"
    }
  }
}
$brokenUnique = $broken | Sort-Object -Unique
if ($brokenUnique.Count -eq 0) {
  Write-Host "  All internal HTML links resolve"
} else {
  $brokenUnique | ForEach-Object { Write-Host "  FAIL: $_" }
  $failures++
}

# 3) SW PRECACHE_URLS all exist on disk
Section "SW precache integrity"
$sw = [System.IO.File]::ReadAllText((Join-Path $Root "sw.js"), [System.Text.Encoding]::UTF8)
$urls = @()
foreach ($m in [regex]::Matches($sw, '"(/[^"]+)"')) {
  $u = $m.Groups[1].Value
  if ($u -match '^/[^/_]') { $urls += $u }
}
$missingSw = @()
foreach ($u in $urls) {
  $rel = $u.Substring(1).Replace('/', '\')
  $path = Join-Path $Root $rel
  if (-not (Test-Path $path)) { $missingSw += $u }
}
if ($missingSw.Count -eq 0) {
  Write-Host "  All $($urls.Count) SW precache URLs exist on disk"
} else {
  $missingSw | ForEach-Object { Write-Host "  FAIL: $_" }
  $failures++
}

# 4) generate.ps1 parses
Section "generate.ps1 syntax"
$genPath = Join-Path $Root "_build\generate.ps1"
$genContent = [System.IO.File]::ReadAllText($genPath, [System.Text.Encoding]::UTF8)
$tokens = $errors = $null
[System.Management.Automation.Language.Parser]::ParseInput($genContent, [ref]$tokens, [ref]$errors) | Out-Null
if ($errors.Count -eq 0) {
  Write-Host "  generate.ps1 parses cleanly"
} else {
  $errors | Select-Object -First 3 | ForEach-Object { Write-Host "  FAIL: $($_.Message)" }
  $failures++
}

# 5) Cache-buster consistency across HTML files
Section "Cache-buster consistency"
$versions = @{}
Get-ChildItem -Path $Root -Filter "*.html" -File | ForEach-Object {
  $content = [System.IO.File]::ReadAllText($_.FullName, [System.Text.Encoding]::UTF8)
  foreach ($m in [regex]::Matches($content, '\?v=(\d{8}[a-z]+)')) {
    $v = $m.Groups[1].Value
    if (-not $versions.ContainsKey($v)) { $versions[$v] = 0 }
    $versions[$v]++
  }
}
if ($versions.Count -eq 1) {
  $v = $versions.Keys | Select-Object -First 1
  Write-Host "  All HTML uses single cache version: ?v=$v ($($versions[$v]) refs)"
} else {
  Write-Host "  WARN: multiple cache versions in use:"
  $versions.Keys | ForEach-Object { Write-Host "    ?v=$_ ($($versions[$_]) refs)" }
  $failures++
}

Write-Host ""
if ($failures -eq 0) {
  Write-Host "All checks passed." -ForegroundColor Green
  exit 0
} else {
  Write-Host "$failures check(s) failed." -ForegroundColor Yellow
  exit 1
}
