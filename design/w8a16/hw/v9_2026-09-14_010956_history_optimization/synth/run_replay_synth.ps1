[CmdletBinding()]
param(
  [string]$Vivado = 'D:\software\Vivado\2021.2\bin\vivado.bat',
  [string]$RunRoot = ''
)
$ErrorActionPreference = 'Stop'
$synthDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$tcl = Join-Path $synthDir 'syn_replay.tcl'
if (-not (Test-Path -LiteralPath $Vivado)) { throw "Vivado executable not found: $Vivado" }
if ([string]::IsNullOrWhiteSpace($RunRoot)) { $RunRoot = Join-Path $synthDir (Join-Path 'runs' (Get-Date -Format 'yyyy-MM-dd_HHmmss')) }
New-Item -ItemType Directory -Force -Path $RunRoot | Out-Null
$records = @()
foreach ($cfg in @(@{Name='array_off_trace_off';Array=0;Trace=0},@{Name='array_on_trace_off';Array=1;Trace=0},@{Name='array_on_trace_on';Array=1;Trace=1})) {
  $out = Join-Path $RunRoot $cfg.Name
  New-Item -ItemType Directory -Force -Path $out | Out-Null
  $start = Get-Date
  & $Vivado -mode batch -source $tcl -tclargs $out $cfg.Array $cfg.Trace 2>&1 | Tee-Object -FilePath (Join-Path $out 'vivado.log')
  $exitCode = $LASTEXITCODE
  $finish = Get-Date
  $statusPath = Join-Path $out 'status.json'
  $status = if (Test-Path -LiteralPath $statusPath) { try { Get-Content -Raw $statusPath | ConvertFrom-Json } catch { $null } } else { $null }
  $records += [ordered]@{name=$cfg.Name;enable_array=$cfg.Array;trace_enable=$cfg.Trace;exit_code=$exitCode;started=$start.ToString('o');finished=$finish.ToString('o');elapsed_s=[math]::Round(($finish-$start).TotalSeconds,3);status=if($status){$status.status}elseif($exitCode -eq 0){'passed'}else{'failed'};output_dir=$out}
}
$summary = [ordered]@{generated=(Get-Date).ToString('o');vivado=(Resolve-Path $Vivado).Path;part='xczu7ev-ffvc1156-2-e';target_period_ns=4.0;run_root=(Resolve-Path $RunRoot).Path;records=$records}
$summary | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $RunRoot 'run_summary.json') -Encoding UTF8
$summary | ConvertTo-Json -Depth 6
