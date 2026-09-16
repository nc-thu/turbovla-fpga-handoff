`timescale 1ns/1ps
module tb_dma_ctx_wram_loader;
  logic clk=0, rst_n=0;
  always #5 clk = ~clk;
  logic start; logic [1:0] target; logic [9:0] base_addr; logic [31:0] length_bytes;
  logic busy, done, stream_valid; logic stream_ready; logic [127:0] stream_data;
  logic ctx_wr_en, wram_wr_en; logic [9:0] ctx_wr_addr, wram_wr_addr;
  logic [127:0] ctx_wr_data; logic [767:0] wram_wr_data; logic [31:0] words_written;
  logic [127:0] ctx_mem [0:31]; logic [767:0] wram_mem [0:31];
  integer i;

  tvla_dma_ctx_wram_loader dut (
    .clk(clk), .rst_n(rst_n), .start(start), .target(target), .base_addr(base_addr),
    .length_bytes(length_bytes), .busy(busy), .done(done),
    .stream_valid(stream_valid), .stream_ready(stream_ready), .stream_data(stream_data),
    .ctx_wr_en(ctx_wr_en), .ctx_wr_addr(ctx_wr_addr), .ctx_wr_data(ctx_wr_data),
    .wram_wr_en(wram_wr_en), .wram_wr_addr(wram_wr_addr), .wram_wr_data(wram_wr_data),
    .words_written(words_written)
  );

  always_ff @(posedge clk) begin
    if (ctx_wr_en) ctx_mem[ctx_wr_addr] <= ctx_wr_data;
    if (wram_wr_en) wram_mem[wram_wr_addr] <= wram_wr_data;
  end

  task automatic send_beat(input logic [127:0] value);
    begin
      @(negedge clk); stream_data = value; stream_valid = 1'b1;
      while (!stream_ready) @(negedge clk);
      @(negedge clk); stream_valid = 1'b0; stream_data = '0;
    end
  endtask

  initial begin
    start=0; target=0; base_addr=0; length_bytes=0; stream_valid=0; stream_data=0;
    for (i=0;i<32;i=i+1) begin ctx_mem[i]='0; wram_mem[i]='0; end
    repeat (3) @(negedge clk); rst_n=1;
    @(negedge clk); target=0; base_addr=10'd3; length_bytes=32; start=1;
    @(negedge clk); start=0;
    send_beat(128'h1111); send_beat(128'h2222);
    wait(done); #1;
    if (ctx_mem[3] !== 128'h1111 || ctx_mem[4] !== 128'h2222 || words_written != 2)
      $fatal(1, "CTX route mismatch data=%h/%h words=%0d", ctx_mem[3], ctx_mem[4], words_written);

    @(negedge clk); target=1; base_addr=10'd5; length_bytes=96; start=1;
    @(negedge clk); start=0;
    send_beat(128'h1); send_beat(128'h2); send_beat(128'h3);
    send_beat(128'h4); send_beat(128'h5); send_beat(128'h6);
    wait(done); #1;
    if (wram_mem[5][127:0] !== 128'h1 || wram_mem[5][255:128] !== 128'h2 ||
        wram_mem[5][383:256] !== 128'h3 || wram_mem[5][511:384] !== 128'h4 ||
        wram_mem[5][639:512] !== 128'h5 || wram_mem[5][767:640] !== 128'h6)
      $fatal(1, "WRAM route mismatch data=%h", wram_mem[5]);
    $display("DMA_CTX_WRAM_LOADER PASS ctx_words=2 wram_words=6");
    $finish;
  end
endmodule
