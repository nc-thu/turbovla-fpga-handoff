# Reproduce the compiler -> integer model -> report part of the W8A16 round.
# RTL compilation itself is run on the server with sim/run_verilator.sh.
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    python 'compiler/v2_2026-09-13_1113_w8a16_camera_ready_compiler/compile_program.py' --output-dir 'compiler/v2_2026-09-13_1113_w8a16_camera_ready_compiler/data'
    python 'compiler/v2_2026-09-13_1113_w8a16_camera_ready_compiler/emit_descriptors.py' --output-dir 'compiler/v2_2026-09-13_1113_w8a16_camera_ready_compiler/data'
    python 'scripts/build_instruction_costs.py' --data-dir 'compiler/v2_2026-09-13_1113_w8a16_camera_ready_compiler/data'
    python 'scripts/isa_sim.py' --data-dir 'compiler/v2_2026-09-13_1113_w8a16_camera_ready_compiler/data' --isa-spec 'data/isa_spec.json'
    python 'scripts/build_inventory.py'
    python 'scripts/run_python_checks.py'
    python 'scripts/collect_rtl_results.py'
    python 'scripts/collect_v2_vivado.py'
    python 'scripts/generate_camera_ready_report.py'
} finally {
    Pop-Location
}
