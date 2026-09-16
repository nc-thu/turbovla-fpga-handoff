`timescale 1ns/1ps
module tb_package_dma_bridge;
  logic clk = 0;
  always #2 clk = ~clk;
  logic rst_n = 0;
  logic [63:0] host_in_data = 0;
  logic [2:0] host_in_kind = 0;
  logic [15:0] host_desc_id = 0;
  logic host_in_valid = 0, host_in_ready;
  logic host_feed_pulse = 0;
  logic [3:0] host_drain_row = 0;
  wire [63:0] host_out_data; wire [2:0] host_out_kind;
  wire host_out_valid; logic host_out_ready = 1;
  wire host_done; wire [31:0] host_observe;
  logic [63:0] ddr_read_data = 0; logic ddr_read_valid = 0; wire ddr_read_ready;
  wire [63:0] ddr_write_data; wire ddr_write_valid; logic ddr_write_ready = 1;
  logic ddr_write_resp_valid = 0;
  integer read_beats = 0, write_beats = 0, responses = 0, dma_out_words = 0, errors = 0;
  integer cycles = 0;
  logic [63:0] write_first = 0, write_second = 0;

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

  task automatic send_host(input logic [2:0] kind, input logic [63:0] data);
    integer accepted;
    begin
      @(negedge clk); host_in_kind = kind; host_in_data = data; host_in_valid = 1'b1;
      $display("SEND kind=%0d t=%0t data=%h ready=%0d sb=%0d fifo_ready=%0d fifo_valid=%0d", kind, $time, data, host_in_ready, dut.sideband_beat, dut.core_sideband_ready, dut.u_core.sideband_complete);
      accepted = 0;
      while (!accepted) begin
        @(posedge clk);
        if (host_in_ready) begin
          $display("ACCEPT kind=%0d t=%0t ready=%0d", kind, $time, host_in_ready);
          @(negedge clk); host_in_valid = 1'b0; host_in_kind = 0; host_in_data = 0;
          accepted = 1;
        end
      end
    end
  endtask

  task automatic send_sideband(input logic [63:0] word0);
    integer i;
    begin
      send_host(3'd5, word0);
      for (i = 1; i < 8; i = i + 1) send_host(3'd5, 64'd0);
    end
  endtask

  // The narrow board stream supplies two 64-bit beats for every internal
  // 128-bit read.  The bridge should expose exactly five AXI R beats.
  task automatic do_read_stream;
    integer i, wait_i;
    begin
      for (i = 0; i < 10; i = i + 1) begin
        @(negedge clk); while (!ddr_read_ready) @(negedge clk);
        ddr_read_data = {32'hcafe0000, i[31:0]};
        ddr_read_valid = 1'b1;
        @(negedge clk); ddr_read_valid = 1'b0;
      end
      for (wait_i = 0; wait_i < 200 && !dut.u_core.dma_done; wait_i = wait_i + 1)
        @(negedge clk);
      if (!dut.u_core.dma_done) begin
        $display("PACKAGE_DMA READ TIMEOUT state=%0d busy=%0d read_beats=%0d", dut.u_core.u_memory.u_dma.state, dut.u_core.dma_busy, read_beats);
        errors = errors + 1;
      end
    end
  endtask

  always @(posedge clk) begin
    cycles <= cycles + 1;
    if (cycles == 300) begin
      $display("PACKAGE_DMA TIMEOUT busy=%0d done=%0d state=%0d wvalid=%0d wready=%0d extvalid=%0d extready=%0d stream_v=%0d stream_r=%0d hold=%0d resp=%0d", dut.u_core.dma_busy, dut.u_core.dma_done, dut.u_core.u_memory.u_dma.state, dut.u_core.m_axi_wvalid, dut.u_core.m_axi_wready, ddr_write_valid, ddr_write_ready, dut.core_dma_stream_in_valid, dut.core_dma_stream_in_ready, dut.wr_hold_valid, dut.wr_resp_hold);
      $finish;
    end
    if (ddr_read_valid && ddr_read_ready) read_beats <= read_beats + 1;
    if (ddr_write_valid && ddr_write_ready) begin
      if (write_beats == 0) write_first <= ddr_write_data;
      if (write_beats == 1) write_second <= ddr_write_data;
      write_beats <= write_beats + 1;
      // One response is returned after the second half of each internal beat.
      if ((write_beats % 2) == 1) begin
        ddr_write_resp_valid <= 1'b1;
        responses <= responses + 1;
      end
    end else if (ddr_write_resp_valid) ddr_write_resp_valid <= 1'b0;
    if (host_out_valid && host_out_ready &&
        (host_out_kind == 3'd2 || host_out_kind == 3'd3))
      dma_out_words <= dma_out_words + 1;
  end

  initial begin
    repeat (4) @(negedge clk); rst_n = 1'b1;
    // Five 128-bit internal beats = ten 64-bit board beats.
    send_sideband(64'h0000_0000_0050_1000);
    send_host(3'd0, 64'h0100_0000_0000_0000);
    do_read_stream();
    for (integer ow = 0; ow < 40 && dma_out_words < 10; ow = ow + 1)
      @(negedge clk);
    if (read_beats != 10) begin
      $display("PACKAGE_DMA FAIL read_beats=%0d", read_beats); errors = errors + 1;
    end
    if (dma_out_words != 10) begin
      $display("PACKAGE_DMA FAIL dma_out_words=%0d", dma_out_words); errors = errors + 1;
    end

    send_sideband(64'h0000_0000_0050_2000);
    send_host(3'd0, 64'h0200_0000_0000_0000);
    // Real payload path: the package top packs these 64-bit beats into
    // internal 128-bit stream beats instead of supplying zero-fill data.
    for (integer p = 0; p < 10; p = p + 1)
      send_host(3'd7, 64'hA000_0000_0000_0000 + p);
    wait (dut.u_core.dma_done);
    if (write_beats != 10) begin
      $display("PACKAGE_DMA FAIL write_beats=%0d", write_beats); errors = errors + 1;
    end
    if (write_first != 64'hA000_0000_0000_0000 ||
        write_second != 64'hA000_0000_0000_0001) begin
      $display("PACKAGE_DMA FAIL payload first=%h second=%h", write_first, write_second);
      errors = errors + 1;
    end
    repeat (4) @(negedge clk);
    if (errors == 0)
      $display("PACKAGE_DMA PASS read64=%0d write64=%0d responses=%0d", read_beats, write_beats, responses);
    $finish;
  end
endmodule
