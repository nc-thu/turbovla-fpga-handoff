`timescale 1ns/1ps
module tb_package_scale_loader;
  logic clk = 0;
  always #5 clk = ~clk;
  logic rst_n = 0;
  logic [63:0] host_in_data;
  logic [2:0] host_in_kind;
  logic [15:0] host_desc_id;
  logic host_in_valid, host_in_ready;
  logic host_feed_pulse;
  logic [3:0] host_drain_row;
  logic [63:0] host_out_data;
  logic [2:0] host_out_kind;
  logic host_out_valid;
  logic host_out_ready = 1'b1;
  logic host_done;
  logic [31:0] host_observe;
  logic [63:0] ddr_read_data = '0;
  logic ddr_read_valid = 1'b0;
  logic ddr_read_ready;
  logic [63:0] ddr_write_data;
  logic ddr_write_valid;
  logic ddr_write_ready = 1'b1;
  logic ddr_write_resp_valid = 1'b0;
  tvla_complete_model_package_top dut (
    .clk(clk), .rst_n(rst_n), .host_in_data(host_in_data),
    .host_in_kind(host_in_kind), .host_desc_id(host_desc_id),
    .host_in_valid(host_in_valid), .host_in_ready(host_in_ready),
    .host_feed_pulse(host_feed_pulse), .host_drain_row(host_drain_row),
    .host_out_data(host_out_data), .host_out_kind(host_out_kind),
    .host_out_valid(host_out_valid), .host_out_ready(host_out_ready),
    .host_done(host_done), .host_observe(host_observe),
    .ddr_read_data(ddr_read_data), .ddr_read_valid(ddr_read_valid),
    .ddr_read_ready(ddr_read_ready), .ddr_write_data(ddr_write_data),
    .ddr_write_valid(ddr_write_valid), .ddr_write_ready(ddr_write_ready),
    .ddr_write_resp_valid(ddr_write_resp_valid)
  );
  initial begin
    host_in_data = '0; host_in_kind = 0; host_desc_id = 0; host_in_valid = 0;
    host_feed_pulse = 0; host_drain_row = 0;
    #12; rst_n = 1;
    // index 0, a=0x3555, w=0x3a00, out=0x3800; second beat bias=-19.
    @(negedge clk); host_in_data = 64'h0380_03a0_0355_5000;
    host_in_kind = 3'd6; host_in_valid = 1'b1;
    @(negedge clk); host_in_data = 64'h0000_0000_ffff_ffed;
    @(negedge clk); host_in_valid = 1'b0; host_in_kind = 3'd0;
    repeat (3) @(negedge clk);
    if (dut.u_core.scale_table_version !== 32'd1 ||
        dut.u_core.u_memory.u_scale_bias_table.a_mem[0] !== 16'h3555 ||
        dut.u_core.u_memory.u_scale_bias_table.w_mem[0] !== 16'h3a00 ||
        dut.u_core.u_memory.u_scale_bias_table.out_mem[0] !== 16'h3800 ||
        dut.u_core.u_memory.u_scale_bias_table.bias_mem[0] !== -32'sd19)
      $fatal(1, "PACKAGE_SCALE FAIL ver=%0d a=%h w=%h o=%h b=%0d",
             dut.u_core.scale_table_version,
             dut.u_core.u_memory.u_scale_bias_table.a_mem[0],
             dut.u_core.u_memory.u_scale_bias_table.w_mem[0],
             dut.u_core.u_memory.u_scale_bias_table.out_mem[0],
             dut.u_core.u_memory.u_scale_bias_table.bias_mem[0]);
    $display("PACKAGE_SCALE PASS version=%0d bias=%0d", dut.u_core.scale_table_version, dut.u_core.bias_value);
    $finish;
  end
endmodule
