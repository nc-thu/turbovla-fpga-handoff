param(
  [string]$Vivado = 'D:\software\Vivado\2021.2\bin\vivado.bat'
)
$round = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$stage = "E:\tvla_w8a8_repro_$stamp"
$rtl = Join-Path $round 'rtl'
$synth = Join-Path $round 'synth'
New-Item -ItemType Directory -Force -Path $stage,(Join-Path $stage 'rtl'),(Join-Path $stage 'synth') | Out-Null
Get-ChildItem -LiteralPath $rtl | Copy-Item -Destination (Join-Path $stage 'rtl') -Force
Get-ChildItem -LiteralPath $synth -File | Copy-Item -Destination (Join-Path $stage 'synth') -Force
$tcl = Join-Path $stage 'synth\run_scale_subunits.tcl'
& $Vivado -mode batch -source $tcl -tclargs $stage -log (Join-Path $stage 'synth\vivado.log') -journal (Join-Path $stage 'synth\vivado.jou')
if ($LASTEXITCODE -ne 0) { throw "Vivado returned $LASTEXITCODE" }
New-Item -ItemType Directory -Force -Path (Join-Path $synth 'runs') | Out-Null
Get-ChildItem -LiteralPath (Join-Path $stage 'synth\runs') | Copy-Item -Destination (Join-Path $synth 'runs') -Recurse -Force
Copy-Item -LiteralPath (Join-Path $stage 'synth\vivado.log') -Destination $synth -Force
Write-Output "Vivado results copied from $stage"
