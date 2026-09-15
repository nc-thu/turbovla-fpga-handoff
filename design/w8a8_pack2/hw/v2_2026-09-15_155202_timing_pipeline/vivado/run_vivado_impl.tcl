# TurboVLA W8A8 Pack2 timing-pipeline implementation run.
# Usage:
#   vivado -mode batch -source run_vivado_impl.tcl \
#          -tclargs <period_ns> <output_dir>
#
# One configuration is run per Vivado process.  This makes the 250 MHz and
# 303.215 MHz results independently reproducible and avoids run-state sharing.
set period_ns [lindex $argv 0]
set outdir [file normalize [lindex $argv 1]]
if {$period_ns eq "" || $outdir eq ""} {
  puts "USAGE: vivado -mode batch -source run_vivado_impl.tcl -tclargs <period_ns> <output_dir>"
  exit 2
}
file mkdir $outdir
set root [file normalize [file join [file dirname [info script]] ..]]
set rtl [file join $root rtl]
set part xczu7ev-ffvc1156-2-e
set top tvla_w8a8_pack2_system_top
set log_file [file join $outdir vivado_impl.log]
set start_epoch [clock seconds]
set start_iso [clock format $start_epoch -format {%Y-%m-%d %H:%M:%S}]

proc json_escape {value} {
  set value [string map {\\ \\\\ \" \\\" \n \\n \r \\r \t \\t} $value]
  return $value
}

proc emit_meta {path status start_iso end_iso elapsed period top error_text} {
  set fh [open $path w]
  set status [json_escape $status]
  set start_iso [json_escape $start_iso]
  set end_iso [json_escape $end_iso]
  set top [json_escape $top]
  set error_text [json_escape $error_text]
  puts $fh "{"
  puts $fh "  \"status\": \"$status\","
  puts $fh "  \"start\": \"$start_iso\","
  puts $fh "  \"end\": \"$end_iso\","
  puts $fh "  \"elapsed_seconds\": $elapsed,"
  puts $fh "  \"period_ns\": $period,"
  puts $fh "  \"top\": \"$top\","
  puts $fh "  \"part\": \"xczu7ev-ffvc1156-2-e\","
  puts $fh "  \"error\": \"$error_text\""
  puts $fh "}"
  close $fh
}

set project_dir [file join $outdir project]
set report_dir [file join $outdir reports]
file mkdir $report_dir
set status "failed"
set error_text ""
set rc [catch {
  create_project -force tvla_w8a8_pack2_timing $project_dir -part $part
  set_property target_language Verilog [current_project]
  set_property simulator_language Mixed [current_project]
  set_param general.maxThreads 4

  # The list is intentionally explicit.  It is also the manifest of the
  # complete currently synthesizable replay portion.
  set srcs [list \
    [file join $rtl pack2_mult_padd.sv] \
    [file join $rtl ae_pe_p2_pa_timing.sv] \
    [file join $rtl ae_sysarr_p2.sv] \
    [file join $rtl tvla_w8a8_pack2_sysarr.sv] \
    [file join $rtl tvla_w8a8_pack2_timing_array_top.sv] \
    [file join $rtl tvla_w8a8_pack2_replay_top_timing.sv] \
    [file join $rtl tvla_w8a8_pack2_system_top.sv]]
  read_verilog -sv $srcs
  set_property top $top [current_fileset]
  update_compile_order -fileset sources_1
  create_clock -name clk -period $period_ns [get_ports clk]
  set_clock_uncertainty 0.05 [get_clocks clk]

  synth_design -top $top -part $part -flatten_hierarchy rebuilt -directive PerformanceOptimized
  report_utilization -file [file join $report_dir synth_utilization.rpt]
  report_timing_summary -delay_type max -max_paths 20 -file [file join $report_dir synth_timing_summary.rpt]
  report_methodology -file [file join $report_dir synth_methodology.rpt]
  write_checkpoint -force [file join $outdir post_synth.dcp]

  opt_design -directive Explore
  place_design -directive Explore
  # AggressiveExplore is available in current Vivado releases.  Keep a
  # deterministic Explore fallback for older 2021.x installations.
  if {[catch {phys_opt_design -directive AggressiveExplore} phys_err]} {
    puts "AggressiveExplore unavailable after place; fallback to Explore: $phys_err"
    phys_opt_design -directive Explore
  }
  report_utilization -file [file join $report_dir placed_utilization.rpt]
  report_timing_summary -delay_type max -max_paths 20 -file [file join $report_dir placed_timing_summary.rpt]
  report_design_analysis -congestion -file [file join $report_dir placed_congestion.rpt]

  route_design -directive Explore
  if {[catch {phys_opt_design -directive AggressiveExplore} phys_err2]} {
    puts "AggressiveExplore unavailable after route; fallback to Explore: $phys_err2"
    phys_opt_design -directive Explore
  }
  report_utilization -file [file join $report_dir impl_utilization.rpt]
  report_utilization -hierarchical -file [file join $report_dir impl_utilization_hier.rpt]
  report_timing_summary -delay_type max -max_paths 50 -file [file join $report_dir impl_timing_summary.rpt]
  report_timing -max_paths 20 -sort_by group -file [file join $report_dir impl_timing_paths.rpt]
  report_route_status -file [file join $report_dir route_status.rpt]
  report_drc -file [file join $report_dir impl_drc.rpt]
  report_power -file [file join $report_dir impl_power_vectorless.rpt]
  report_methodology -file [file join $report_dir impl_methodology.rpt]
  write_checkpoint -force [file join $outdir routed.dcp]
  set status "passed"
} error_text]

set end_epoch [clock seconds]
set end_iso [clock format $end_epoch -format {%Y-%m-%d %H:%M:%S}]
set elapsed [expr {$end_epoch - $start_epoch}]
if {$rc != 0} { puts "Vivado run failed: $error_text" }
emit_meta [file join $outdir run_metadata.json] $status $start_iso $end_iso $elapsed $period_ns $top $error_text
catch {close_project -delete}
if {$status ne "passed"} { exit 1 }
exit 0
