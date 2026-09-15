# TurboVLA complete-model board top: synthesis and implementation (2026-09-16 04:20:30).
set script_dir [file normalize [file dirname [info script]]]
set root [file normalize [file join $script_dir ..]]
set rtl_dir [file join $root rtl]
set run_tag 20260916_0500_package
if {[info exists ::env(TVLA_VIVADO_RUN_TAG)] && $::env(TVLA_VIVADO_RUN_TAG) ne ""} {
  set run_tag $::env(TVLA_VIVADO_RUN_TAG)
}
set out_dir [file join $script_dir "vivado_runs_$run_tag"]
file mkdir $out_dir
set part xczu7ev-ffvc1156-2-e
set top tvla_complete_model_package_top
set_param general.maxThreads 4
cd $rtl_dir
foreach f [glob -nocomplain *.sv] { read_verilog -sv $f }
cd $script_dir
read_xdc {complete_model_4ns.xdc}
set_property top $top [current_fileset]
update_compile_order -fileset sources_1
synth_design -top $top -part $part -flatten_hierarchy rebuilt -directive PerformanceOptimized
report_utilization -file [file join $out_dir synth_utilization.rpt]
report_timing_summary -file [file join $out_dir synth_timing.rpt]
write_checkpoint -force [file join $out_dir complete_model_synth.dcp]
opt_design -directive Explore
place_design -directive Explore
phys_opt_design -directive Explore
route_design -directive Explore
report_utilization -file [file join $out_dir impl_utilization.rpt]
report_timing_summary -file [file join $out_dir impl_timing.rpt]
report_drc -file [file join $out_dir impl_drc.rpt]
report_power -file [file join $out_dir impl_power.rpt]
write_checkpoint -force [file join $out_dir complete_model_impl.dcp]
exit
