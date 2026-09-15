`timescale 1ns/1ps
module tb_w8a16_dma;
  localparam int DW = 256;
  logic clk = 0; always #5 clk = ~clk;
  logic rst_n = 0;
  logic cmd_valid = 0, cmd_write = 0;
  logic [15:0] cmd_addr = 0, cmd_len = 0;
  logic cmd_ready;
  logic [DW-1:0] stream_in_data = 0;
  logic stream_in_valid = 0, stream_in_ready;
  logic [DW-1:0] stream_out_data;
  logic stream_out_valid = 0, stream_out_ready = 0;
  logic mem_req, mem_write;
  logic [15:0] mem_addr;
  logic [DW-1:0] mem_wdata, mem_rdata;
  logic mem_rvalid;
  logic busy, done;
  logic [DW-1:0] mem [0:15];
  integer i, seen;

  w8a16_dma #(.DATA_W(DW), .ADDR_W(16)) dut(.*);

  // One-cycle read response models an AXI/DDR return channel.  Writes are
  // accepted on the same cycle as the request.
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      mem_rvalid <= 1'b0;
      mem_rdata <= '0;
      for (i = 0; i < 16; i = i + 1) mem[i] <= '0;
    end else begin
      mem_rvalid <= 1'b0;
      if (mem_req && mem_write) mem[mem_addr[8:5]] <= mem_wdata;
      if (mem_req && !mem_write) begin
        mem_rdata <= mem[mem_addr[8:5]];
        mem_rvalid <= 1'b1;
      end
    end
  end

  task automatic send_cmd(input logic wr, input integer addr, input integer beats);
    begin
      @(negedge clk); cmd_write = wr; cmd_addr = addr; cmd_len = beats; cmd_valid = 1'b1;
      while (!cmd_ready) @(negedge clk);
      @(negedge clk); cmd_valid = 1'b0;
    end
  endtask

  initial begin
    repeat (2) @(negedge clk); rst_n = 1'b1;
    send_cmd(1'b1, 32, 2);
    @(negedge clk); stream_in_data = 256'h1111; stream_in_valid = 1'b1;
    while (!stream_in_ready) @(negedge clk);
    @(negedge clk); stream_in_data = 256'h2222;
    while (!stream_in_ready) @(negedge clk);
    @(negedge clk); stream_in_valid = 1'b0; stream_in_data = '0;
    while (!done) @(negedge clk);
    if (mem[1] !== 256'h1111 || mem[2] !== 256'h2222) $fatal(1, "DMA write mismatch");

    send_cmd(1'b0, 32, 2);
    stream_out_ready = 1'b1; seen = 0;
    while (seen < 2) begin
      @(negedge clk);
      if (stream_out_valid) begin
        if (seen == 0 && stream_out_data !== 256'h1111) $fatal(1, "DMA read beat0");
        if (seen == 1 && stream_out_data !== 256'h2222) $fatal(1, "DMA read beat1");
        seen = seen + 1;
      end
    end
    while (!done) @(negedge clk);
    $display("TB_W8A16_DMA PASS");
    $finish(0);
  end
endmodule
