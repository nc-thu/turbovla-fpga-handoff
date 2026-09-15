[CmdletBinding()]
param(
  [string]$Vivado = 'D:\software\Vivado\2021.2\bin\vivado.bat',
  [string]$RunRoot = ''
)

$ErrorActionPreference = 'Stop'
$hwDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$tcl = Join-Path $hwDir 'impl/impl_top.tcl'
if (-not (Test-Path -LiteralPath $Vivado)) { throw "Vivado executable not found: $Vivado" }
if (-not (Test-Path -LiteralPath $tcl)) { throw "Implementation Tcl not found: $tcl" }
if ([string]::IsNullOrWhiteSpace($RunRoot)) {
  $RunRoot = Join-Path $hwDir (Join-Path 'impl/runs' (Get-Date -Format 'yyyy-MM-dd_HHmmss'))
}
New-Item -ItemType Directory -Force -Path $RunRoot | Out-Null

$out = Join-Path $RunRoot 'system_top'
New-Item -ItemType Directory -Force -Path $out | Out-Null
$command = "`"$Vivado`" -mode batch -source `"$tcl`" -tclargs w8a16_system_top `"$out`" 16 48"
Set-Content -LiteralPath (Join-Path $out 'command.txt') -Value $command -Encoding UTF8
$start = Get-Date
& $Vivado -mode batch -source $tcl -tclargs w8a16_system_top $out 16 48 2>&1 |
  Tee-Object -FilePath (Join-Path $out 'vivado.log')
$exitCode = $LASTEXITCODE
$finish = Get-Date
$statusPath = Join-Path $out 'status.json'
$status = $null
if (Test-Path -LiteralPath $statusPath) {
  try { $status = Get-Content -Raw -LiteralPath $statusPath | ConvertFrom-Json } catch {}
}
$summary = [ordered]@{
  generated = (Get-Date).ToString('o')
  vivado = (Resolve-Path -LiteralPath $Vivado).Path
  part = 'xczu7ev-ffvc1156-2-e'
  target_period_ns = 3.298
  run_root = (Resolve-Path -LiteralPath $RunRoot).Path
  exit_code = $exitCode
  started = $start.ToString('o')
  finished = $finish.ToString('o')
  elapsed_s = [math]::Round(($finish - $start).TotalSeconds, 3)
  status = if ($status) { $status.status } elseif ($exitCode -eq 0) { 'passed' } else { 'failed' }
  output_dir = $out
}
$summary | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $RunRoot 'run_summary.json') -Encoding UTF8
$summary | ConvertTo-Json -Depth 6
if ($exitCode -ne 0) { exit $exitCode }
