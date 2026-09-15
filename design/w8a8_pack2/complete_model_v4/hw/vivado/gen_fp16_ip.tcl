# Generate the optional Xilinx Floating-Point Operator cores used by the
# numerically sensitive activation path.  The RTL has a fixed-point fallback
# for Icarus; Vivado implementation reads the generated XCI files.
set ip_root [file normalize [file join [pwd] fp16_ip_project]]
create_project tvla_fp16_ip $ip_root -part xczu7ev-ffvc1156-2-e -force
set specs {
  {tvla_fp16_add Add_Subtract}
  {tvla_fp16_mul Multiply}
  {tvla_fp16_div Divide}
  {tvla_fp16_sqrt Square_Root}
  {tvla_fp16_exp Exponential}
}
foreach spec $specs {
  lassign $spec name op
  create_ip -name floating_point -vendor xilinx.com -library ip -version 7.1 -module_name $name
  set ip [get_ips $name]
  set_property -dict [list \
    CONFIG.Operation_Type $op \
    CONFIG.A_Precision_Type {Half} \
    CONFIG.Result_Precision_Type {Half} \
    CONFIG.C_Optimization {Speed_Optimized} \
    CONFIG.Flow_Control {Blocking} \
    CONFIG.Has_ARESETn {false} \
    CONFIG.C_Latency {automatic} \
  ] $ip
  generate_target all $ip
  export_ip_user_files -of_objects $ip -no_script -sync -force
}
exit
