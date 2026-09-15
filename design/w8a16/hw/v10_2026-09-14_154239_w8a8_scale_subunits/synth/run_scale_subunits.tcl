# Non-project Vivado OOC synthesis for the W8A8 A/B/C subunits.
# MODE=0 is the integer partial-sum core shared by A/B/C.  The FP32 scale
# merge in software path A is deliberately not represented as an FPGA result.
# Vivado 2021.2 on this Windows host mishandles some paths containing spaces.
# The companion PowerShell wrapper stages this directory under a no-space path
# and passes that path as the first Tcl argument.
set BASE [lindex $argv 0]
if {$BASE eq ""} { error "run_scale_subunits.tcl requires a no-space BASE path" }
set SCRIPT_DIR "$BASE/synth"
set ROOT "$BASE"
set RTL_DIR "$BASE/rtl"
set RUN_ROOT "$BASE/synth/runs"
set XDC_FILE "$BASE/synth/w8a8_scale_path.xdc"
set PART "xczu7ev-ffvc1156-2-e"
set PERIOD_NS 4.000
file mkdir $RUN_ROOT
set modes {0 1 2}
set names {A_partial_int32 B_fixed_merge_fpout C_fixed_merge_int8out}
for {set idx 0} {$idx < [llength $modes]} {incr idx} {
    set mode [lindex $modes $idx]
    set name [lindex $names $idx]
    set OUT "$RUN_ROOT/$name"
    file mkdir $OUT
    set start [clock seconds]
    set status "passed"
    set message ""
    if {[catch {
        catch {close_project -quiet}
        catch {close_design}
        read_verilog -sv [glob -nocomplain "$RTL_DIR/*.sv"]
        read_xdc $XDC_FILE
        synth_design -top w8a8_scale_path_top -part $PART -mode out_of_context \
            -generic MODE=$mode -generic GROUPS=4 -generic LANES=32 \
            -flatten_hierarchy rebuilt -directive RuntimeOptimized
        opt_design
        report_utilization -file "$OUT/utilization.rpt"
        report_timing_summary -file "$OUT/timing.rpt"
        report_drc -file "$OUT/drc.rpt"
        write_checkpoint -force "$OUT/post_synth.dcp"
        close_design
    } result]} {
        set status "failed"
        set message $result
        catch {close_design}
    }
    set finish [clock seconds]
    set fh [open "$OUT/status.txt" w]
    puts $fh "mode=$mode"
    puts $fh "name=$name"
    puts $fh "part=$PART"
    puts $fh "period_ns=$PERIOD_NS"
    puts $fh "status=$status"
    puts $fh "started=[clock format $start -format {%Y-%m-%dT%H:%M:%S%z}]"
    puts $fh "finished=[clock format $finish -format {%Y-%m-%dT%H:%M:%S%z}]"
    puts $fh "elapsed_s=[expr {$finish-$start}]"
    puts $fh "message=$message"
    close $fh
}
