# Non-project synthesis for the TurboVLA activity replay top.
# Usage: vivado -mode batch -source syn_replay.tcl -tclargs OUT ENABLE_ARRAY TRACE_ENABLE
# Timing is an OOC estimate at 4.000 ns (250 MHz), not post-route timing.
set OUT [lindex $argv 0]
set ENABLE_ARRAY [lindex $argv 1]
set TRACE_ENABLE [lindex $argv 2]
if {$OUT eq ""} { set OUT [file join [file dirname [info script]] runs default] }
if {$ENABLE_ARRAY eq ""} { set ENABLE_ARRAY 1 }
if {$TRACE_ENABLE eq ""} { set TRACE_ENABLE 0 }
set SCRIPT_DIR [file normalize [file dirname [info script]]]
set RTL_DIR [file normalize [file join $SCRIPT_DIR .. rtl]]
set PART "xczu7ev-ffvc1156-2-e"
set PERIOD_NS 4.000
file mkdir $OUT

proc iso_now {} { return [clock format [clock seconds] -format {%Y-%m-%dT%H:%M:%S%z}] }
proc json_quote {s} { return [string map [list {\\} {\\\\} {\"} {\\\"} {\n} {\\n} {\r} {\\r}] $s] }
proc status_json {path status start finish elapsed msg out ena trace period part} {
  set fh [open $path w]
  puts $fh [format {{"top":"tvla_replay_top","output_dir":"%s","enable_array":%s,"trace_enable":%s,"part":"%s","target_period_ns":%s,"status":"%s","started":"%s","finished":"%s","elapsed_s":%.3f,"message":"%s"}} [json_quote $out] $ena $trace [json_quote $part] $period [json_quote $status] [json_quote $start] [json_quote $finish] $elapsed [json_quote $msg]]
  close $fh
}

set start_epoch [clock milliseconds]
set start_iso [iso_now]
set ok 0
set message ""
set sources [glob -nocomplain -types f [file join $RTL_DIR *.sv]]
if {[catch {
  set_param general.maxThreads 8
  read_verilog -sv $sources
  synth_design -top tvla_replay_top -part $PART -mode out_of_context -flatten_hierarchy none -directive RuntimeOptimized -generic ENABLE_ARRAY=$ENABLE_ARRAY -generic TRACE_ENABLE=$TRACE_ENABLE
  set clk_ports [get_ports -quiet clk]
  if {[llength $clk_ports] > 0} { create_clock -name clk -period $PERIOD_NS $clk_ports }
  write_checkpoint -force [file join $OUT post_synth.dcp]
  report_utilization -hierarchical -file [file join $OUT utilization.rpt]
  report_timing_summary -delay_type max -file [file join $OUT timing.rpt]
  catch { report_drc -file [file join $OUT drc.rpt] }
  catch { report_power -file [file join $OUT power.rpt] }
  catch { report_dsp_utilization -file [file join $OUT dsp.rpt] }
  set ok 1
} err]} { set message $err }
set finish_iso [iso_now]
set elapsed [expr {([clock milliseconds] - $start_epoch) / 1000.0}]
if {$ok} {
  set status "passed"
  if {$message eq ""} { set message "synth_design completed; timing is synthesis-estimated" }
} else {
  set status "failed"
  if {$message eq ""} { set message "synth_design failed" }
}
status_json [file join $OUT status.json] $status $start_iso $finish_iso $elapsed $message $OUT $ENABLE_ARRAY $TRACE_ENABLE $PERIOD_NS $PART
if {$ok} { exit 0 } else { exit 1 }
