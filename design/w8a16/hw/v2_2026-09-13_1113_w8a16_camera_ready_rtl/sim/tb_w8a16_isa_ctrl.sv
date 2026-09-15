`timescale 1ns/1ps
module tb_w8a16_isa_ctrl;
  logic clk = 0; always #5 clk = ~clk;
  logic rst_n = 0, instr_valid = 0, op_done = 0;
  logic [63:0] instr_word = 0;
  logic instr_ready, op_valid, busy, done;
  logic [7:0] op_code, op_flags, op_dst, op_src0, op_src1;
  logic [15:0] op_length;
  w8a16_isa_ctrl dut(.*);

  function automatic [63:0] word(input [7:0] code, input [7:0] dst,
                                  input [7:0] src0, input [7:0] src1,
                                  input [15:0] length);
    word = {code, 8'h03, dst, src0, src1, length, 8'h00};
  endfunction

  task automatic issue(input [63:0] w, input bit acknowledge);
    begin
      @(negedge clk); instr_word = w; instr_valid = 1'b1;
      while (!instr_ready) @(negedge clk);
      @(negedge clk); instr_valid = 1'b0;
      if (acknowledge) begin
        while (!op_valid) @(negedge clk);
        if (op_code == 8'hff) $fatal(1, "END exposed as normal op");
        @(negedge clk); op_done = 1'b1;
        @(negedge clk); op_done = 1'b0;
        while (busy) @(negedge clk);
      end else begin
        while (!done) @(negedge clk);
      end
    end
  endtask

  initial begin
    repeat (2) @(negedge clk); rst_n = 1'b1;
    issue(word(8'h10, 8'h12, 8'h34, 8'h56, 16'd8), 1'b1);
    if (op_dst !== 8'h12 || op_src0 !== 8'h34 || op_src1 !== 8'h56 || op_length !== 16'd8)
      $fatal(1, "ISA field decode mismatch");
    issue(word(8'hff, 0, 0, 0, 0), 1'b0);
    $display("TB_W8A16_ISA_CTRL PASS");
    $finish(0);
  end
endmodule
