[CmdletBinding()]
param(
  [string]$Vivado = 'D:\software\Vivado\2021.2\bin\vivado.bat',
  [string]$RunRoot = ''
)

$ErrorActionPreference = 'Stop'
$synthDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$tcl = Join-Path $synthDir 'syn_top.tcl'
if (-not (Test-Path -LiteralPath $Vivado)) {
  throw "Vivado executable not found: $Vivado"
}
if (-not (Test-Path -LiteralPath $tcl)) {
  throw "Synthesis Tcl not found: $tcl"
}
if ([string]::IsNullOrWhiteSpace($RunRoot)) {
  $RunRoot = Join-Path $synthDir (Join-Path 'runs' (Get-Date -Format 'yyyy-MM-dd_HHmmss'))
}
New-Item -ItemType Directory -Force -Path $RunRoot | Out-Null

$jobs = @(
  @{ Name = 'system_top'; Top = 'w8a16_system_top'; Rows = 16; Pcols = 48 },
  @{ Name = 'array_1x1';  Top = 'w8a16_array_top';   Rows = 1;  Pcols = 1  },
  @{ Name = 'array_4x4';  Top = 'w8a16_array_top';   Rows = 4;  Pcols = 4  },
  @{ Name = 'array_16x48';Top = 'w8a16_array_top';   Rows = 16; Pcols = 48 }
)

$records = @()
foreach ($job in $jobs) {
  $out = Join-Path $RunRoot $job.Name
  New-Item -ItemType Directory -Force -Path $out | Out-Null
  $command = "`"$Vivado`" -mode batch -source `"$tcl`" -tclargs $($job.Top) `"$out`" $($job.Rows) $($job.Pcols)"
  Set-Content -LiteralPath (Join-Path $out 'command.txt') -Value $command -Encoding UTF8
  $start = Get-Date
  & $Vivado -mode batch -source $tcl -tclargs $job.Top $out $job.Rows $job.Pcols 2>&1 |
    Tee-Object -FilePath (Join-Path $out 'vivado.log')
  $exitCode = $LASTEXITCODE
  $finish = Get-Date
  $statusPath = Join-Path $out 'status.json'
  $status = $null
  if (Test-Path -LiteralPath $statusPath) {
    try { $status = Get-Content -Raw -LiteralPath $statusPath | ConvertFrom-Json } catch {}
  }
  $records += [ordered]@{
    name = $job.Name; top = $job.Top; rows = $job.Rows; pcols = $job.Pcols
    exit_code = $exitCode; started = $start.ToString('o'); finished = $finish.ToString('o')
    elapsed_s = [math]::Round(($finish - $start).TotalSeconds, 3)
    status = if ($status) { $status.status } else { if ($exitCode -eq 0) { 'passed' } else { 'failed' } }
    output_dir = $out
  }
  if ($exitCode -ne 0) {
    Write-Warning "$($job.Name) synthesis failed; continuing with the remaining tops."
  }
}

$summary = [ordered]@{
  generated = (Get-Date).ToString('o')
  vivado = (Resolve-Path -LiteralPath $Vivado).Path
  part = 'xczu7ev-ffvc1156-2-e'
  target_period_ns = 3.298
  run_root = (Resolve-Path -LiteralPath $RunRoot).Path
  records = $records
}
$summary | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $RunRoot 'run_summary.json') -Encoding UTF8
Write-Output ($summary | ConvertTo-Json -Depth 6)
