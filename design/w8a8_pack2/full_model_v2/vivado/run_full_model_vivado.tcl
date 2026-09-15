# TurboVLA full-model Pack2 synthesis/implementation (2026-09-16 01:00:24).
set root {E:/GPU ARCH/vector_core_sim/turbovla_w8a8_pack2/hw/v4_2026-09-16_0100_full_model_rtl}
set rtl_dir {E:/GPU ARCH/vector_core_sim/turbovla_w8a8_pack2/hw/v4_2026-09-16_0100_full_model_rtl/rtl}
set work_dir {E:/GPU ARCH/vector_core_sim/turbovla_w8a8_pack2/hw/v4_2026-09-16_0100_full_model_rtl/vivado}
cd $work_dir
set run_tag 20260916_0244
if {[info exists ::env(TVLA_VIVADO_RUN_TAG)] && $::env(TVLA_VIVADO_RUN_TAG) ne ""} {
  set run_tag $::env(TVLA_VIVADO_RUN_TAG)
}
set out_dir "vivado_runs_$run_tag"
file mkdir $out_dir
set part xczu7ev-ffvc1156-2-e
set top tvla_full_model_board_top
set_param general.maxThreads 4
set saved_pwd [pwd]
cd $rtl_dir
foreach f [glob -nocomplain *.sv] { read_verilog -sv $f }
cd $saved_pwd
read_xdc full_model_4ns.xdc
set_property top $top [current_fileset]
update_compile_order -fileset sources_1
synth_design -top $top -part $part -flatten_hierarchy rebuilt -directive PerformanceOptimized
report_utilization -file [file join $out_dir synth_utilization.rpt]
report_timing_summary -file [file join $out_dir synth_timing.rpt]
write_checkpoint -force [file join $out_dir full_model_synth.dcp]
opt_design -directive Explore
place_design -directive Explore
phys_opt_design -directive Explore
route_design -directive Explore
report_utilization -file [file join $out_dir impl_utilization.rpt]
report_timing_summary -file [file join $out_dir impl_timing.rpt]
report_drc -file [file join $out_dir impl_drc.rpt]
report_power -file [file join $out_dir impl_power.rpt]
write_checkpoint -force [file join $out_dir full_model_impl.dcp]
exit
