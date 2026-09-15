param([string]$OutputRoot = "")

$ErrorActionPreference = "Continue"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $scriptDir
if ([string]::IsNullOrWhiteSpace($OutputRoot)) { $OutputRoot = Join-Path $root "reports" }
New-Item -ItemType Directory -Force -Path (Join-Path $OutputRoot "250MHz") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $OutputRoot "303MHz") | Out-Null

function Run-One([string]$Label, [double]$Period) {
  $out = Join-Path $OutputRoot $Label
  $start = Get-Date
  $status = "not_run"
  $reason = "vivado command not found on this host"
  $rc = 127
  $vivado = Get-Command vivado -ErrorAction SilentlyContinue
  if ($null -ne $vivado) {
    $status = "running"; $reason = ""
    $log = Join-Path $out "launcher.log"
    & $vivado.Source -mode batch -source (Join-Path $scriptDir "run_vivado_impl.tcl") `
      -tclargs ("{0:F3}" -f $Period) $out *> $log
    $rc = $LASTEXITCODE
    if ($rc -eq 0) { $status = "passed"; $reason = "" }
    else { $status = "failed"; $reason = "Vivado returned exit code $rc" }
  }
  $end = Get-Date
  [pscustomobject]@{
    status=$status; reason=$reason
    start=$start.ToString("yyyy-MM-dd HH:mm:ss")
    end=$end.ToString("yyyy-MM-dd HH:mm:ss")
    elapsed_seconds=[math]::Round(($end-$start).TotalSeconds,3)
    period_ns=$Period; frequency_mhz=[math]::Round(1000/$Period,6)
  } | ConvertTo-Json | Set-Content -Encoding UTF8 (Join-Path $out "run_metadata.json")
  Write-Host "$Label $status ($rc)"
  return $rc
}

$result = 0
$rc250 = Run-One "250MHz" 4.000
if ($rc250 -ne 0) { $result = $rc250 }
$rc303 = Run-One "303MHz" 3.298
if ($rc303 -ne 0) { $result = $rc303 }
exit $result
