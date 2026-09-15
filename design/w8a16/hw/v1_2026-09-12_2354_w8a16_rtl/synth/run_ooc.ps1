param(
  [string]$Vivado = "vivado.bat",
  [string]$RtlDir = "$(Split-Path -Parent $PSScriptRoot)",
  [string]$RunRoot = "$(Join-Path $PSScriptRoot 'runs')"
)
$ErrorActionPreference = 'Stop'
New-Item -ItemType Directory -Force -Path $RunRoot | Out-Null
$t0 = Get-Date
foreach ($spec in @(@(1,1), @(4,4), @(16,48))) {
  $rows = $spec[0]; $cols = $spec[1]
  $out = Join-Path $RunRoot ("w8a16_{0}x{1}" -f $rows,$cols)
  New-Item -ItemType Directory -Force -Path $out | Out-Null
  & $Vivado -mode batch -source (Join-Path $PSScriptRoot 'syn.tcl') -tclargs w8a16_array_top $out $rows $cols 2>&1 | Tee-Object -FilePath (Join-Path $out 'vivado.log')
  if ($LASTEXITCODE -ne 0) { Write-Warning "OOC failed for ${rows}x${cols}" }
}
@{started=$t0.ToString('o'); ended=(Get-Date).ToString('o'); elapsed_seconds=((Get-Date)-$t0).TotalSeconds} | ConvertTo-Json | Set-Content (Join-Path $RunRoot 'run_summary.json')
