`timescale 1ns/1ps
// Integration check for the v8 descriptor-driven DMA payload route.
// The board-facing stream remains 64 bits, while the internal DMA beat is
// 128 bits.  The test verifies that a DMA_READ selected as CTX or WRAM really
// updates the on-chip memories instead of being returned to the host.
module tb_package_dma_loader;
  logic clk = 1'b0;
  always #2 clk = ~clk;
  logic rst_n = 1'b0;
  logic [63:0] host_in_data = 0;
  logic [2:0] host_in_kind = 0;
  logic [15:0] host_desc_id = 0;
  logic host_in_valid = 0, host_in_ready;
  logic host_feed_pulse = 0;
  logic [3:0] host_drain_row = 0;
  wire [63:0] host_out_data;
  wire [2:0] host_out_kind;
  wire host_out_valid;
  logic host_out_ready = 1'b1;
  wire host_done;
  wire [31:0] host_observe;
  logic [63:0] ddr_read_data = 0;
  logic ddr_read_valid = 0;
  wire ddr_read_ready;
  wire [63:0] ddr_write_data;
  wire ddr_write_valid;
  logic ddr_write_ready = 1'b1;
  logic ddr_write_resp_valid = 1'b0;
  integer errors = 0;

  tvla_complete_model_package_top_v8 dut (
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

  task automatic send_host(input logic [2:0] kind, input logic [63:0] data);
    integer accepted;
    begin
      @(negedge clk);
      host_in_kind = kind;
      host_in_data = data;
      host_in_valid = 1'b1;
      accepted = 0;
      while (!accepted) begin
        @(posedge clk);
        if (host_in_ready) begin
          @(negedge clk);
          host_in_valid = 1'b0;
          host_in_kind = 3'd0;
          host_in_data = 64'd0;
          accepted = 1;
        end
      end
    end
  endtask

  task automatic send_sideband(
      input logic [31:0] base_addr, input logic [31:0] byte_len,
      input logic [1:0] target);
    logic [63:0] words [0:7];
    integer i;
    begin
      for (i = 0; i < 8; i = i + 1) words[i] = 64'd0;
      // Descriptor layout is little-endian 8x64.  The router consumes
      // sideband[95:64], sideband[351:320], and sideband[497:496].
      words[1] = {32'd0, base_addr};
      words[5] = {32'd0, byte_len};
      words[7] = (target == 2'd1) ? 64'h0001_0000_0000_0000 : 64'd0;
      for (i = 0; i < 8; i = i + 1) send_host(3'd5, words[i]);
    end
  endtask

  task automatic send_read_beat(input logic [63:0] value);
    integer accepted;
    begin
      @(negedge clk);
      ddr_read_data = value;
      ddr_read_valid = 1'b1;
      accepted = 0;
      while (!accepted) begin
        @(posedge clk);
        if (ddr_read_ready) begin
          @(negedge clk);
          ddr_read_valid = 1'b0;
          ddr_read_data = 64'd0;
          accepted = 1;
        end
      end
    end
  endtask

  task automatic wait_dma_idle;
    integer i;
    begin
      for (i = 0; i < 300; i = i + 1) begin
        @(negedge clk);
        if (!dut.loader_busy && !dut.u_core.dma_busy) disable wait_dma_idle;
      end
      $display("PACKAGE_DMA_LOADER TIMEOUT loader_busy=%0d dma_busy=%0d", dut.loader_busy,
               dut.u_core.dma_busy);
      errors = errors + 1;
    end
  endtask

  initial begin
    repeat (4) @(negedge clk);
    rst_n = 1'b1;

    // CTX: two 128-bit internal beats -> four 64-bit board beats.
    send_sideband(32'd3, 32'd32, 2'd0);
    send_host(3'd0, 64'h0100_0000_0000_0000);
    send_read_beat(64'h0000_0000_1111_0000);
    send_read_beat(64'h0000_0000_1111_0001);
    send_read_beat(64'h0000_0000_2222_0000);
    send_read_beat(64'h0000_0000_2222_0001);
    wait_dma_idle();
    #1;
    if (dut.u_core.u_memory.u_buffers.ctx_mem[3] !==
        {32'h0000_0000, 32'h1111_0001, 32'h0000_0000, 32'h1111_0000} ||
        dut.u_core.u_memory.u_buffers.ctx_mem[4] !==
        {32'h0000_0000, 32'h2222_0001, 32'h0000_0000, 32'h2222_0000}) begin
      $display("PACKAGE_DMA_LOADER CTX mismatch addr3=%h addr4=%h",
               dut.u_core.u_memory.u_buffers.ctx_mem[3],
               dut.u_core.u_memory.u_buffers.ctx_mem[4]);
      errors = errors + 1;
    end

    // WRAM: six 128-bit beats form one 768-bit weight row.
    send_sideband(32'd5, 32'd96, 2'd1);
    send_host(3'd0, 64'h0100_0000_0000_0000);
    send_read_beat(64'h0000_0000_0000_0001);
    send_read_beat(64'h0000_0000_0000_0002);
    send_read_beat(64'h0000_0000_0000_0003);
    send_read_beat(64'h0000_0000_0000_0004);
    send_read_beat(64'h0000_0000_0000_0005);
    send_read_beat(64'h0000_0000_0000_0006);
    send_read_beat(64'h0000_0000_0000_0007);
    send_read_beat(64'h0000_0000_0000_0008);
    send_read_beat(64'h0000_0000_0000_0009);
    send_read_beat(64'h0000_0000_0000_000a);
    send_read_beat(64'h0000_0000_0000_000b);
    send_read_beat(64'h0000_0000_0000_000c);
    wait_dma_idle();
    #1;
    if (dut.u_core.u_memory.u_buffers.wram_mem[5][127:0] !== 128'h0000_0000_0000_0002_0000_0000_0000_0001 ||
        dut.u_core.u_memory.u_buffers.wram_mem[5][255:128] !== 128'h0000_0000_0000_0004_0000_0000_0000_0003 ||
        dut.u_core.u_memory.u_buffers.wram_mem[5][383:256] !== 128'h0000_0000_0000_0006_0000_0000_0000_0005 ||
        dut.u_core.u_memory.u_buffers.wram_mem[5][511:384] !== 128'h0000_0000_0000_0008_0000_0000_0000_0007 ||
        dut.u_core.u_memory.u_buffers.wram_mem[5][639:512] !== 128'h0000_0000_0000_000a_0000_0000_0000_0009 ||
        dut.u_core.u_memory.u_buffers.wram_mem[5][767:640] !== 128'h0000_0000_0000_000c_0000_0000_0000_000b) begin
      $display("PACKAGE_DMA_LOADER WRAM mismatch row5=%h", dut.u_core.u_memory.u_buffers.wram_mem[5]);
      errors = errors + 1;
    end

    if (errors == 0)
      $display("PACKAGE_DMA_LOADER PASS ctx_addr=3 wram_addr=5 ctx_beats=2 wram_beats=6");
    else
      $display("PACKAGE_DMA_LOADER FAIL errors=%0d", errors);
    $finish;
  end
endmodule
