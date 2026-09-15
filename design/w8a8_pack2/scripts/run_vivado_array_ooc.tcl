# Vivado 2021.2 OOC resource point for the TurboVLA W8A8 Pack2 array.
# Arguments: rows pcols output_directory
set rows [lindex $argv 0]
set pcols [lindex $argv 1]
set outdir [file normalize [lindex $argv 2]]
file mkdir $outdir
set root [file normalize [file join [file dirname [info script]] ..]]
set rtl [file join $root hw v1_2026-09-14_115230_pack2_rtl rtl]
set files [list \
  [file join $rtl pack2_mult_padd.sv] \
  [file join $rtl ae_pe_p2_pa.sv] \
  [file join $rtl ae_sysarr_p2.sv] \
  [file join $rtl tvla_w8a8_pack2_sysarr.sv] \
  [file join $rtl tvla_w8a8_pack2_array_top.sv]]
read_verilog -sv $files
set generic_args [list ROWS=$rows PCOLS=$pcols]
synth_design -top tvla_w8a8_pack2_array_top -part xczu7ev-ffvc1156-2-e -mode out_of_context -generic $generic_args
create_clock -name clk -period 3.298 [get_ports clk]
set_property SEVERITY Warning [get_drc_checks]
report_utilization -file [file join $outdir utilization.rpt]
report_timing_summary -delay_type max -max_paths 20 -file [file join $outdir timing.rpt]
report_power -file [file join $outdir power.rpt]
report_drc -file [file join $outdir drc.rpt]
set fh [open [file join $outdir run.json] w]
puts $fh "{\"rows\":$rows,\"physical_cols\":$pcols,\"target_period_ns\":3.298,\"top\":\"tvla_w8a8_pack2_array_top\"}"
close $fh
exit
