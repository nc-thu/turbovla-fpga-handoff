`timescale 1ns/1ps
module tb_bmm_layout;
  logic clk = 0; always #1 clk = ~clk;
  logic rst_n = 0, start = 0, a_valid = 0, b_valid = 0;
  logic [31:0] a_row, b_row;
  logic a_index, b_index, transpose_b = 1, mask_enable = 0;
  logic signed [15:0] scale = 16'sd256;
  wire in_ready, out_valid, out_last;
  wire [31:0] out_a, out_b;
  wire out_index;
  logic out_ready = 1;
  tvla_bmm_layout #(.ROWS(2), .COLS(2), .DW(16)) dut (
    .clk(clk), .rst_n(rst_n), .start(start), .a_valid(a_valid), .a_row(a_row),
    .a_index(a_index), .b_valid(b_valid), .b_row(b_row), .b_index(b_index),
    .transpose_b(transpose_b), .mask_enable(mask_enable), .scale(scale),
    .in_ready(in_ready), .out_valid(out_valid), .out_ready(out_ready),
    .out_a(out_a), .out_b(out_b), .out_index(out_index), .out_last(out_last)
  );
  task automatic load_a(input logic idx, input logic [15:0] lo, input logic [15:0] hi);
    begin @(negedge clk); a_index=idx; a_row={hi,lo}; a_valid=1; @(posedge clk);
      @(negedge clk); a_valid=0; end
  endtask
  task automatic load_b(input logic idx, input logic [15:0] lo, input logic [15:0] hi);
    begin @(negedge clk); b_index=idx; b_row={hi,lo}; b_valid=1; @(posedge clk);
      @(negedge clk); b_valid=0; end
  endtask
  initial begin
    a_row=0; b_row=0; a_index=0; b_index=0;
    repeat(2) @(posedge clk); rst_n=1;
    load_a(0,16'sd1,16'sd2); load_a(1,16'sd3,16'sd4);
    load_b(0,16'sd10,16'sd20); load_b(1,16'sd30,16'sd40);
    @(negedge clk); start=1; @(posedge clk); @(negedge clk); start=0;
    wait(out_valid);
    if (out_a !== {16'sd2,16'sd1} || out_b !== {16'sd30,16'sd10} || out_index !== 0)
      $fatal(1,"BMM row0 mismatch a=%h b=%h idx=%d",out_a,out_b,out_index);
    @(posedge clk); @(negedge clk); wait(out_valid);
    if (!out_last || out_b !== {16'sd40,16'sd20} || out_index !== 1)
      $fatal(1,"BMM row1 mismatch a=%h b=%h idx=%d last=%d",out_a,out_b,out_index,out_last);
    $display("BMM_LAYOUT PASS row0=%h row1=%h",out_b,{16'sd40,16'sd20});
    $finish;
  end
endmodule
