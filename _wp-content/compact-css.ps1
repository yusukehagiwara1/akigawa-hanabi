# compact-css.ps1
# Conservative styles.css compaction:
#  - strips /* ... */ comments (block)
#  - collapses 3+ blank lines to a single blank line
#  - trims trailing whitespace on each line
# Does NOT touch selectors, properties, or values. Idempotent.

[CmdletBinding()]
param(
  [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path,
  [switch]$DryRun
)

$cssPath = Join-Path $Root "styles.css"
if (-not (Test-Path $cssPath)) { throw "styles.css not found" }

$css = [System.IO.File]::ReadAllText($cssPath, [System.Text.Encoding]::UTF8)
$origBytes = $css.Length
$origLines = ($css -split "`n").Count

# 1) Strip block comments. License/header comments survive because the
#    file opens with a single block at the very top; we preserve THAT
#    one by detecting and re-prepending it.
$headerMatch = [regex]::Match($css, '^/\*[\s\S]*?\*/\s*')
$header = if ($headerMatch.Success) { $headerMatch.Value } else { "" }
$body = if ($header) { $css.Substring($header.Length) } else { $css }

# Keep all comments — they document round-by-round rationale and help
# future maintainers (and AI sessions) understand each block.
# Comments are well-compressed by gzip, so removing them yields only a
# small wire-size win not worth the readability loss.

# 2) Trim trailing whitespace per line
$body = [regex]::Replace($body, '[ \t]+(\r?\n)', '$1')

# 3) Collapse 3+ blank lines to one
$body = [regex]::Replace($body, '(\r?\n){3,}', "`r`n`r`n")

$result = $header + $body
$newBytes = $result.Length
$newLines = ($result -split "`n").Count

$savedBytes = $origBytes - $newBytes
$savedPct = if ($origBytes -gt 0) { [Math]::Round(100 * $savedBytes / $origBytes, 1) } else { 0 }

Write-Host ("Original: {0,8} bytes ({1} KB, {2} lines)" -f $origBytes, [Math]::Round($origBytes/1024), $origLines)
Write-Host ("Compact:  {0,8} bytes ({1} KB, {2} lines)" -f $newBytes, [Math]::Round($newBytes/1024), $newLines)
Write-Host ("Saved:    {0,8} bytes ({1}%)" -f $savedBytes, $savedPct)

if ($DryRun) {
  Write-Host "DRY RUN — not writing."
} else {
  $utf8 = New-Object System.Text.UTF8Encoding $false
  [System.IO.File]::WriteAllText($cssPath, $result, $utf8)
  Write-Host "Wrote $cssPath"
}
