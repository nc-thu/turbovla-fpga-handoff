# TurboVLA W8A16 v5 post-route implementation.
# Non-project flow: synthesize, optimize, place, physical-optimize and route
# the copied v4 camera-ready system top.  No bitstream is written because the
# wrapper has no board-specific pin/DDR constraints.
# Usage:
#   vivado -mode batch -source impl_top.tcl -tclargs TOP OUT ROWS PCOLS

set TOP   [lindex $argv 0]
set OUT   [lindex $argv 1]
set ROWS  [lindex $argv 2]
set PCOLS [lindex $argv 3]
if {$TOP eq ""}   { set TOP "w8a16_system_top" }
if {$OUT eq ""}   { set OUT [file join [file dirname [info script]] runs default_system] }
if {$ROWS eq ""}  { set ROWS 16 }
if {$PCOLS eq ""} { set PCOLS 48 }

set SCRIPT_DIR [file normalize [file dirname [info script]]]
set HW_DIR     [file normalize [file join $SCRIPT_DIR ..]]
set RTL_DIR    [file normalize [file join $HW_DIR rtl]]
set SYNTH_DIR  [file normalize [file join $HW_DIR synth]]
set PART       "xczu7ev-ffvc1156-2-e"
set PERIOD_NS  3.298
file mkdir $OUT

proc iso_now {} {
  return [clock format [clock seconds] -format {%Y-%m-%dT%H:%M:%S%z}]
}

proc json_quote {s} {
  return [string map [list \\ \\\\ \" \\\" \n \\n \r \\r] $s]
}

proc write_status {path top rows pcols part period status start_iso end_iso elapsed stage message} {
  set fh [open $path w]
  puts $fh [format {{"top":"%s","rows":%s,"pcols":%s,"part":"%s","target_period_ns":%s,"status":"%s","started":"%s","finished":"%s","elapsed_s":%.3f,"stage":"%s","message":"%s"}} \
    [json_quote $top] $rows $pcols [json_quote $part] $period [json_quote $status] \
    [json_quote $start_iso] [json_quote $end_iso] $elapsed [json_quote $stage] [json_quote $message]]
  close $fh
}

set start_epoch [clock seconds]
set start_iso [iso_now]
set status "failed"
set stage "read"
set message ""

set sources [glob -nocomplain -types f [file join $RTL_DIR *.sv]]
lappend sources [file normalize [file join $SYNTH_DIR top_w8a16_system.sv]]
if {[llength $sources] == 0} {
  set message "no SystemVerilog sources found"
} else {
  if {[catch {
    read_verilog -sv $sources

    set stage "synth_design"
    synth_design -top $TOP -part $PART -mode out_of_context \
      -flatten_hierarchy none -directive RuntimeOptimized \
      -generic GEMM_ROWS=$ROWS -generic GEMM_COLS=$PCOLS
    write_checkpoint -force [file join $OUT post_synth.dcp]
    report_utilization -hierarchical -file [file join $OUT post_synth_utilization.rpt]
    report_timing_summary -delay_type max -file [file join $OUT post_synth_timing.rpt]

    # The wrapper exposes clk but has no board-level IO constraints.  The
    # internal clock is still constrained for post-route analysis.
    set clk_ports [get_ports -quiet clk]
    if {[llength $clk_ports] > 0} {
      create_clock -name clk -period $PERIOD_NS $clk_ports
    }

    set stage "opt_design"
    opt_design -directive Default
    report_timing_summary -delay_type max -file [file join $OUT post_opt_timing.rpt]

    set stage "place_design"
    place_design -directive Explore
    report_utilization -hierarchical -file [file join $OUT post_place_utilization.rpt]
    report_timing_summary -delay_type max -file [file join $OUT post_place_timing.rpt]

    set stage "phys_opt_design_post_place"
    phys_opt_design -directive RuntimeOptimized
    report_timing_summary -delay_type max -file [file join $OUT post_physopt_timing.rpt]

    set stage "route_design"
    route_design -directive Explore
    write_checkpoint -force [file join $OUT post_route_pre_physopt.dcp]
    report_timing_summary -delay_type max -report_unconstrained -file [file join $OUT post_route_pre_physopt_timing.rpt]

    # A post-route pass is useful when only a small number of paths are close
    # to the limit.  Final reports are always taken after this pass.
    set stage "phys_opt_design_post_route"
    phys_opt_design -directive Explore

    set stage "final_reports"
    write_checkpoint -force [file join $OUT post_route.dcp]
    report_timing_summary -delay_type max -report_unconstrained -file [file join $OUT post_route_timing.rpt]
    report_timing -max_paths 20 -nworst 10 -file [file join $OUT post_route_critical_paths.rpt]
    report_utilization -hierarchical -file [file join $OUT post_route_utilization.rpt]
    report_route_status -file [file join $OUT post_route_status.rpt]
    catch { report_design_analysis -congestion -file [file join $OUT post_route_congestion.rpt] }
    catch { report_qor_assessment -file [file join $OUT post_route_qor_assessment.rpt] }
    catch { report_methodology -file [file join $OUT post_route_methodology.rpt] }
    catch { report_drc -file [file join $OUT post_route_drc.rpt] }
    catch { report_power -verbose -file [file join $OUT post_route_power.rpt] }
    set status "passed"
    set message "implementation and final reports completed; no bitstream requested"
  } err]} {
    set message $err
  }
}

set end_epoch [clock seconds]
set end_iso [iso_now]
set elapsed [expr {$end_epoch - $start_epoch}]
write_status [file join $OUT status.json] $TOP $ROWS $PCOLS $PART $PERIOD_NS \
  $status $start_iso $end_iso $elapsed $stage $message
if {$status ne "passed"} { exit 1 }
exit 0
