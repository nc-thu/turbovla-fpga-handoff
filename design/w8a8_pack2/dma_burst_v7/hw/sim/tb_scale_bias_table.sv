`timescale 1ns/1ps
module tb_scale_bias_table;
  logic clk = 0;
  always #5 clk = ~clk;
  logic rst_n = 0;
  logic wr_valid;
  logic [11:0] wr_index, rd_index;
  logic [15:0] wr_a_scale, wr_w_scale, wr_out_scale;
  logic signed [31:0] wr_bias;
  logic [15:0] rd_a_scale, rd_w_scale, rd_out_scale;
  logic signed [31:0] rd_bias;
  logic [31:0] version;
  tvla_scale_bias_table dut (
    .clk(clk), .rst_n(rst_n), .wr_valid(wr_valid), .wr_index(wr_index),
    .wr_a_scale(wr_a_scale), .wr_w_scale(wr_w_scale),
    .wr_out_scale(wr_out_scale), .wr_bias(wr_bias), .rd_index(rd_index),
    .rd_a_scale(rd_a_scale), .rd_w_scale(rd_w_scale),
    .rd_out_scale(rd_out_scale), .rd_bias(rd_bias), .version(version)
  );
  initial begin
    wr_valid = 0; wr_index = 12'd7; rd_index = 12'd0;
    wr_a_scale = 16'h3555; wr_w_scale = 16'h3a00;
    wr_out_scale = 16'h3800; wr_bias = -32'sd19;
    #12; rst_n = 1;
    @(negedge clk); wr_valid = 1;
    @(negedge clk); wr_valid = 0; rd_index = 12'd7;
    @(negedge clk);
    if (rd_a_scale !== 16'h3555 || rd_w_scale !== 16'h3a00 ||
        rd_out_scale !== 16'h3800 || rd_bias !== -32'sd19 || version !== 32'd1)
      $fatal(1, "SCALE_TABLE FAIL a=%h w=%h o=%h b=%0d v=%0d",
             rd_a_scale, rd_w_scale, rd_out_scale, rd_bias, version);
    $display("SCALE_TABLE PASS index=7 version=%0d bias=%0d", version, rd_bias);
    $finish;
  end
endmodule
