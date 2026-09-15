# Project-mode vendor FP16 synthesis.  The IP project is opened instead of
# re-importing XCI files, so Vivado reuses the generated IP output products and
# does not place all cores in one shared in-memory output directory.
set script_dir [file normalize [file dirname [info script]]]
set root [file normalize [file join $script_dir ..]]
set fp16_proj [file join $root fp16_ip_project tvla_fp16_ip.xpr]
set out_dir [file join $script_dir fp16_vendor_project_synth_20260916_070720]
file mkdir $out_dir
set part xczu7ev-ffvc1156-2-e
set top tvla_complete_model_package_top
set_param general.maxThreads 4
open_project $fp16_proj
set_property verilog_define {TVLA_USE_VENDOR_FP16} [get_filesets sources_1]
set xci_root [file join $root fp16_ip_project tvla_fp16_ip.srcs sources_1 ip]
foreach ip_name {tvla_fp16_add tvla_fp16_mul tvla_fp16_div tvla_fp16_exp tvla_fp16_sqrt} {
  set xci_file [file join $xci_root $ip_name ${ip_name}.xci]
  if {[file exists $xci_file]} {
    add_files -norecurse $xci_file
    set ip_obj [get_ips -quiet $ip_name]
    if {[llength $ip_obj] > 0} {
      # Force Vivado to use the generated HDL wrapper in synthesis.  The
      # copied project otherwise prefers an OOC checkpoint and the top-level
      # elaborator cannot see the IP module name.
      set xci_obj [get_files -quiet $xci_file]
      if {[llength $xci_obj] > 0} {
        set_property generate_synth_checkpoint 0 $xci_obj
      }
      generate_target all $ip_obj
    }
  } else {
    puts "WARNING: missing XCI $xci_file"
  }
}
set rtl_dir [file join $root rtl]
cd $rtl_dir
foreach f [glob -nocomplain *.sv] {
  add_files -norecurse $f
}
cd $script_dir
read_xdc complete_model_4ns.xdc
set_property top $top [get_filesets sources_1]
update_compile_order -fileset sources_1
puts "IP objects: [get_ips -quiet]"
puts "IP source files: [get_files -quiet -of_objects [get_filesets sources_1]]"
synth_design -top $top -part $part -flatten_hierarchy rebuilt -directive PerformanceOptimized
cd $out_dir
report_utilization -file synth_utilization.rpt
report_timing_summary -file synth_timing.rpt
write_checkpoint -force fp16_vendor_project_synth.dcp
close_project
exit
