# Non-project Vivado synthesis entry point for the TurboVLA W8A16 RTL.
# Usage from Vivado batch mode:
#   vivado -mode batch -source syn_top.tcl -tclargs TOP OUT ROWS PCOLS
#
# The flow deliberately keeps synthesis separate from implementation.  The
# reported timing is an estimate at the requested 3.298 ns clock and is not a
# post-place-and-route result.

set TOP   [lindex $argv 0]
set OUT   [lindex $argv 1]
set ROWS  [lindex $argv 2]
set PCOLS [lindex $argv 3]

if {$TOP eq ""}   { set TOP "w8a16_system_top" }
if {$OUT eq ""}   { set OUT [file join [file dirname [info script]] runs default] }
if {$ROWS eq ""}  { set ROWS 16 }
if {$PCOLS eq ""} { set PCOLS 48 }

set SCRIPT_DIR [file normalize [file dirname [info script]]]
set RTL_DIR    [file normalize [file join $SCRIPT_DIR .. rtl]]
set PART       "xczu7ev-ffvc1156-2-e"
set PERIOD_NS  3.298
file mkdir $OUT

proc iso_now {} {
  return [clock format [clock seconds] -format {%Y-%m-%dT%H:%M:%S%z}]
}

proc json_quote {s} {
  return [string map [list \\ \\\\ \" \\\" \n \\n \r \\r] $s]
}

proc write_status {path top rows pcols part period status start_iso end_iso elapsed message} {
  set fh [open $path w]
  puts $fh [format {{"top":"%s","rows":%s,"pcols":%s,"part":"%s","target_period_ns":%s,"status":"%s","started":"%s","finished":"%s","elapsed_s":%.3f,"message":"%s"}} \
    [json_quote $top] $rows $pcols [json_quote $part] $period [json_quote $status] \
    [json_quote $start_iso] [json_quote $end_iso] $elapsed [json_quote $message]]
  close $fh
}

set start_epoch [clock seconds]
set start_iso [iso_now]
set status "failed"
set message ""
set synth_ok 0

set sources [glob -nocomplain -types f [file join $RTL_DIR *.sv]]
if {$TOP eq "w8a16_array_top"} {
  lappend sources [file normalize [file join $SCRIPT_DIR top_w8a16.sv]]
} elseif {$TOP eq "w8a16_system_top"} {
  lappend sources [file normalize [file join $SCRIPT_DIR top_w8a16_system.sv]]
} else {
  set message "unsupported top requested"
}

if {$message eq ""} {
  if {[catch {
    # Non-project flow: read RTL directly, then synthesize the selected top.
    read_verilog -sv $sources
    if {$TOP eq "w8a16_array_top"} {
      synth_design -top $TOP -part $PART -mode out_of_context \
        -flatten_hierarchy none -directive RuntimeOptimized \
        -generic ROWS=$ROWS -generic PCOLS=$PCOLS -generic ACC_W=40
    } else {
      synth_design -top $TOP -part $PART -mode out_of_context \
        -flatten_hierarchy none -directive RuntimeOptimized
    }
    set synth_ok 1

    # Apply the target clock after elaboration so report_timing_summary can
    # use it.  A missing clock port is recorded as a warning, not a false
    # synthesis failure.
    set clk_ports [get_ports -quiet clk]
    if {[llength $clk_ports] > 0} {
      create_clock -name clk -period $PERIOD_NS $clk_ports
    }

    write_checkpoint -force [file join $OUT post_synth.dcp]
    report_utilization -hierarchical -file [file join $OUT utilization.rpt]
    report_timing_summary -delay_type max -file [file join $OUT timing.rpt]
    catch { report_drc -file [file join $OUT drc.rpt] }
    catch { report_dsp_utilization -file [file join $OUT dsp.rpt] }
  } err]} {
    set message $err
  }
}

set end_epoch [clock seconds]
set end_iso [iso_now]
set elapsed [expr {$end_epoch - $start_epoch}]
if {$synth_ok} {
  set status "passed"
  if {$message eq ""} { set message "synth_design completed; reports may contain tool warnings" }
} elseif {$message eq ""} {
  set message "synth_design did not complete"
}
write_status [file join $OUT status.json] $TOP $ROWS $PCOLS $PART $PERIOD_NS \
  $status $start_iso $end_iso $elapsed $message

if {$status ne "passed"} { exit 1 }
exit 0
