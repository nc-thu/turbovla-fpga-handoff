`timescale 1ns/1ps
module tb_descriptor_sideband;
  logic clk = 0;
  always #1 clk = ~clk;
  logic rst_n = 0;
  logic in_valid, in_last;
  logic [63:0] in_data;
  wire in_ready, out_valid;
  wire [511:0] out_data;
  logic out_ready;
  wire [3:0] out_beats;
  tvla_descriptor_sideband_fifo dut (
    .clk(clk), .rst_n(rst_n), .in_valid(in_valid), .in_ready(in_ready),
    .in_data(in_data), .in_last(in_last), .out_valid(out_valid),
    .out_ready(out_ready), .out_data(out_data), .out_beats(out_beats)
  );
  integer i;
  initial begin
    in_valid = 0; in_last = 0; in_data = 0; out_ready = 0;
    repeat (2) @(posedge clk); rst_n = 1;
    for (i = 0; i < 8; i = i + 1) begin
      @(negedge clk);
      in_data = 64'h1000 + i;
      in_last = (i == 7);
      in_valid = 1;
      @(posedge clk);
      while (!in_ready) @(posedge clk);
      @(negedge clk); in_valid = 0; in_last = 0;
    end
    repeat (1) @(posedge clk);
    if (!out_valid || out_beats != 8 || out_data[63:0] !== 64'h1000 ||
        out_data[511:448] !== 64'h1007) $fatal(1, "sideband assembly failed");
    out_ready = 1;
    @(posedge clk);
    $display("DESCRIPTOR_SIDEBAND PASS beats=%0d first=%h last=%h", out_beats,
             out_data[63:0], out_data[511:448]);
    $finish;
  end
endmodule
