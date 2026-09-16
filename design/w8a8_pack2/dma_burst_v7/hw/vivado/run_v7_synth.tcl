set root "V:/turbovla_w8a8_pack2/hw/v7_2026-09-16_073705_dma_burst_memory_rtl"
set script_dir "$root/vivado"
set out_dir "$script_dir/v7_synth_20260916_0810"
file mkdir $out_dir
set part xczu7ev-ffvc1156-2-e
set_param general.maxThreads 4

read_verilog -sv [glob -nocomplain "$root/rtl/*.sv"]
read_xdc "$script_dir/complete_model_4ns.xdc"
set_property top tvla_complete_model_package_top [current_fileset]
update_compile_order -fileset sources_1
synth_design -top tvla_complete_model_package_top -part $part \
  -flatten_hierarchy rebuilt -directive PerformanceOptimized
report_utilization -file "$out_dir/synth_utilization.rpt"
report_timing_summary -file "$out_dir/synth_timing.rpt"
report_power -file "$out_dir/synth_power.rpt"
write_checkpoint -force "$out_dir/v7_synth.dcp"
close_design
exit
