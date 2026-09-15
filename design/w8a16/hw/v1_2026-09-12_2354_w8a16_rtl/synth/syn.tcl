set TOP [lindex $argv 0]
set OUT [lindex $argv 1]
set ROWS [lindex $argv 2]
set PCOLS [lindex $argv 3]
if {$TOP eq ""} { set TOP "w8a16_array_top" }
set SCRIPT_DIR [file normalize [file dirname [info script]]]
if {$OUT eq ""} { set OUT [file join $SCRIPT_DIR runs "w8a16_${ROWS}x${PCOLS}"] }
file mkdir $OUT
create_project -in_memory -part xczu7ev-ffvc1156-2-e
read_verilog -sv [list \
  [file join $SCRIPT_DIR .. rtl w8a16_mult.sv] \
  [file join $SCRIPT_DIR .. rtl w8a16_pe.sv] \
  [file join $SCRIPT_DIR .. rtl w8a16_sysarr.sv] \
  [file join $SCRIPT_DIR top_w8a16.sv]]
set_property top $TOP [current_fileset]
update_compile_order -fileset sources_1
synth_design -top $TOP -part xczu7ev-ffvc1156-2-e -mode out_of_context \
  -flatten_hierarchy none -generic ROWS=$ROWS -generic PCOLS=$PCOLS -generic ACC_W=40
create_clock -name clk -period 3.298 [get_ports clk]
report_utilization -hierarchical -file $OUT/utilization.rpt
report_timing_summary -delay_type max -file $OUT/timing.rpt
report_drc -file $OUT/drc.rpt
set fh [open "$OUT/status.json" w]
puts $fh "{\"top\":\"$TOP\",\"rows\":$ROWS,\"pcols\":$PCOLS,\"status\":\"synth_complete\"}"
close $fh
