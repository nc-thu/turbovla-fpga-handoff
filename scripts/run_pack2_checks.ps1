param(
  [ValidateSet('functional','golden','all')]
  [string]$What = 'all'
)

$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot

if ($What -in @('golden','all')) {
  $goldenOut = Join-Path $repo 'data\validation\pack2_golden_check.json'
  New-Item -ItemType Directory -Force -Path (Split-Path $goldenOut) | Out-Null
  python (Join-Path $repo 'design\w8a8_pack2\algo\v1_2026-09-14_115230_w8a8_semantics\test_pack2_golden.py') --output $goldenOut
  if ($LASTEXITCODE -ne 0) { throw "Pack2 golden check failed (exit $LASTEXITCODE)" }
}
if ($What -in @('functional','all')) {
  powershell -ExecutionPolicy Bypass -File (Join-Path $repo 'design\w8a8_pack2\hw\v3_2026-09-15_174639_vivado_impl\sim\run_timing_smoke.ps1')
  if ($LASTEXITCODE -ne 0) { throw "RTL functional smoke failed (exit $LASTEXITCODE)" }
}
