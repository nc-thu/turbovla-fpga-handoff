# Reproduce the v4 compiler -> model -> report checks.
# The server RTL regression and the recorded Vivado run are kept as explicit
# inputs; this script never overwrites v1-v3 directories.
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$compiler = Join-Path $root 'compiler/v4_2026-09-13_150700_w8a16_timing_fixed_compiler'
$data = Join-Path $root 'data/v4_2026-09-13_150700'
$hw = Join-Path $root 'hw/v4_2026-09-13_150700_w8a16_timing_fixed_rtl'
$vivadoRun = Join-Path $hw 'synth/runs/2026-09-13_150700_system_v14'

Push-Location $root
try {
    python (Join-Path $compiler 'compile_program.py') --output-dir (Join-Path $compiler 'data')
    python (Join-Path $compiler 'emit_descriptors.py') --output-dir (Join-Path $compiler 'data')
    foreach ($name in @('turbovla_w8a16_program.json','w8a16_descriptors.json','compile_manifest.json','descriptor_manifest.json','isa_spec.json')) {
        Copy-Item -LiteralPath (Join-Path $compiler ('data/' + $name)) -Destination (Join-Path $data $name) -Force
    }
    python (Join-Path $root 'arch/v4_2026-09-13_150700_w8a16_timing_fixed_model/build_cycle_model.py') --data-dir $data
    python (Join-Path $root 'scripts/build_instruction_costs.py') --data-dir $data
    python (Join-Path $root 'scripts/isa_sim.py') --data-dir $data
    python (Join-Path $root 'scripts/run_python_checks.py') --data-dir $data
    foreach ($name in @('instruction_costs.json','instruction_costs.csv','isa_sim_results.json','libero_action_probe.json','python_checks.json','quant_error.csv','isa_spec.json')) {
        Copy-Item -LiteralPath (Join-Path $data $name) -Destination (Join-Path $compiler ('data/' + $name)) -Force
    }
    python (Join-Path $root 'scripts/collect_v4_rtl_results.py')
    python (Join-Path $root 'scripts/collect_v4_vivado_synth.py') $vivadoRun
    python (Join-Path $root 'scripts/generate_camera_ready_report_v4.py')
} finally {
    Pop-Location
}
