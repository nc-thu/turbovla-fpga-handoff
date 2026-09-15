param(
  [string]$OutDir = ""
)

# Icarus emits benign "constant selects" diagnostics on stderr for this RTL.
# Treat native-tool exit codes as authoritative instead of promoting those
# diagnostics to terminating PowerShell errors.
$ErrorActionPreference = "Continue"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $here
if ([string]::IsNullOrWhiteSpace($OutDir)) { $OutDir = Join-Path $root "data" }
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$iverilog = "C:\iverilog\bin\iverilog.exe"
$vvp = "C:\iverilog\bin\vvp.exe"
$rtl = Join-Path $root "rtl"
$results = New-Object System.Collections.Generic.List[object]

function Run-Check([string]$Name, [string[]]$CompileArgs, [string]$VvpFile) {
  $start = Get-Date
  $log = Join-Path $OutDir "$Name.log"
  $status = "passed"
  $message = ""
  try {
    & $iverilog @CompileArgs *> $log
    if ($LASTEXITCODE -ne 0) { throw "iverilog exited with $LASTEXITCODE" }
    & $vvp $VvpFile *>> $log
    if ($LASTEXITCODE -ne 0) { throw "vvp exited with $LASTEXITCODE" }
  } catch {
    $status = "failed"
    $message = $_.Exception.Message
  }
  $end = Get-Date
  $results.Add([pscustomobject]@{
    name = $Name
    status = $status
    start = $start.ToString("yyyy-MM-dd HH:mm:ss")
    end = $end.ToString("yyyy-MM-dd HH:mm:ss")
    elapsed_seconds = [math]::Round(($end-$start).TotalSeconds, 3)
    log = $log
    message = $message
  })
  if ($status -eq "failed") { Write-Warning "$Name failed: $message" }
  else { Write-Output "$Name PASS" }
}

if (!(Test-Path $iverilog) -or !(Test-Path $vvp)) {
  $results.Add([pscustomobject]@{name="toolchain";status="not_run";reason="Icarus executable not found"})
} else {
  $multVvp = Join-Path $OutDir "tb_pack2_mult_padd.vvp"
  Run-Check "pack2_mult_padd" @(
    "-g2012", "-DVERILATOR", "-s", "tb_pack2_mult_padd", "-o", $multVvp,
    (Join-Path $rtl "pack2_mult_padd.sv"),
    (Join-Path $here "tb_pack2_mult_padd.sv")
  ) $multVvp

  $arrayVvp = Join-Path $OutDir "tb_timing_array_smoke.vvp"
  Run-Check "timing_array" @(
    "-g2012", "-DVERILATOR", "-s", "tb_timing_array_smoke", "-o", $arrayVvp,
    (Join-Path $rtl "pack2_mult_padd.sv"),
    (Join-Path $rtl "ae_pe_p2_pa_timing.sv"),
    (Join-Path $rtl "ae_sysarr_p2.sv"),
    (Join-Path $rtl "tvla_w8a8_pack2_sysarr.sv"),
    (Join-Path $rtl "tvla_w8a8_pack2_timing_array_top.sv"),
    (Join-Path $here "tb_timing_array_smoke.sv")
  ) $arrayVvp

  $replayVvp = Join-Path $OutDir "tb_timing_replay_top.vvp"
  Run-Check "timing_replay" @(
    "-g2012", "-DVERILATOR", "-s", "tb_replay_top", "-o", $replayVvp,
    (Join-Path $rtl "pack2_mult_padd.sv"),
    (Join-Path $rtl "ae_pe_p2_pa_timing.sv"),
    (Join-Path $rtl "ae_sysarr_p2.sv"),
    (Join-Path $rtl "tvla_w8a8_pack2_sysarr.sv"),
    (Join-Path $rtl "tvla_w8a8_pack2_timing_array_top.sv"),
    (Join-Path $rtl "tvla_w8a8_pack2_replay_top_timing.sv"),
    (Join-Path $here "tb_timing_replay_top.sv")
  ) $replayVvp

  $elabVvp = Join-Path $OutDir "system_top_elab.vvp"
  $elabLog = Join-Path $OutDir "system_top_elaboration.log"
  $elabStart = Get-Date
  $elabStatus = "passed"; $elabMessage = ""
  try {
    & $iverilog -g2012 -DVERILATOR -s tvla_w8a8_pack2_system_top -o $elabVvp `
      (Join-Path $rtl "pack2_mult_padd.sv") `
      (Join-Path $rtl "ae_pe_p2_pa_timing.sv") `
      (Join-Path $rtl "ae_sysarr_p2.sv") `
      (Join-Path $rtl "tvla_w8a8_pack2_sysarr.sv") `
      (Join-Path $rtl "tvla_w8a8_pack2_timing_array_top.sv") `
      (Join-Path $rtl "tvla_w8a8_pack2_replay_top_timing.sv") `
      (Join-Path $rtl "tvla_w8a8_pack2_system_top.sv") *> $elabLog
    if ($LASTEXITCODE -ne 0) { throw "iverilog exited with $LASTEXITCODE" }
  } catch { $elabStatus = "failed"; $elabMessage = $_.Exception.Message }
  $elabEnd = Get-Date
  $results.Add([pscustomobject]@{
    name="system_top_elaboration"; status=$elabStatus
    start=$elabStart.ToString("yyyy-MM-dd HH:mm:ss")
    end=$elabEnd.ToString("yyyy-MM-dd HH:mm:ss")
    elapsed_seconds=[math]::Round(($elabEnd-$elabStart).TotalSeconds, 3)
    log=$elabLog; message=$elabMessage
  })
}

$json = Join-Path $OutDir "functional_checks.json"
$results | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 $json
if ($results | Where-Object {$_.status -eq "failed"}) { exit 1 }
