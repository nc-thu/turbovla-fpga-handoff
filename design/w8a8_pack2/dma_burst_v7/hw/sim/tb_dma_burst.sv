`timescale 1ns/1ps
module tb_dma_burst;
  logic clk = 1'b0;
  always #1 clk = ~clk;
  logic rst_n = 1'b0;
  logic start_read = 0, start_write = 0;
  logic [63:0] base_addr = 0;
  logic [31:0] length_bytes = 0;
  wire busy, done;
  wire [31:0] read_cycles, write_cycles;
  wire arvalid; logic arready = 1;
  wire [63:0] araddr; wire [7:0] arlen;
  wire rready; logic rvalid = 0; logic [127:0] rdata = 0; logic rlast = 0;
  wire awvalid; logic awready = 1;
  wire [63:0] awaddr; wire [7:0] awlen;
  wire wvalid; logic wready = 1;
  wire [127:0] wdata; wire [15:0] wstrb; wire wlast;
  logic bvalid = 0; wire bready;
  wire stream_out_valid; logic stream_out_ready = 1; wire [127:0] stream_out_data;
  logic stream_in_valid = 0; wire stream_in_ready; logic [127:0] stream_in_data = 0;

  tvla_dma_axi #(.DW(128), .MAX_BURST_BEATS(4)) dut (
    .clk(clk), .rst_n(rst_n), .start_read(start_read), .start_write(start_write),
    .base_addr(base_addr), .length_bytes(length_bytes), .busy(busy), .done(done),
    .read_cycles(read_cycles), .write_cycles(write_cycles),
    .m_axi_arvalid(arvalid), .m_axi_arready(arready), .m_axi_araddr(araddr), .m_axi_arlen(arlen),
    .m_axi_rready(rready), .m_axi_rvalid(rvalid), .m_axi_rdata(rdata), .m_axi_rlast(rlast),
    .m_axi_awvalid(awvalid), .m_axi_awready(awready), .m_axi_awaddr(awaddr), .m_axi_awlen(awlen),
    .m_axi_wvalid(wvalid), .m_axi_wready(wready), .m_axi_wdata(wdata), .m_axi_wstrb(wstrb), .m_axi_wlast(wlast),
    .m_axi_bvalid(bvalid), .m_axi_bready(bready),
    .stream_out_valid(stream_out_valid), .stream_out_ready(stream_out_ready), .stream_out_data(stream_out_data),
    .stream_in_valid(stream_in_valid), .stream_in_ready(stream_in_ready), .stream_in_data(stream_in_data)
  );
  integer r_left = 0, w_left = 0, r_beats = 0, w_beats = 0;
  integer read_words = 0, write_words = 0, errors = 0;
  logic read_phase = 1'b1;
  always_ff @(posedge clk) begin
    if (!rst_n) begin
      rvalid <= 0; rlast <= 0; bvalid <= 0;
      r_left <= 0; w_left <= 0; r_beats <= 0; w_beats <= 0;
      stream_in_valid <= 0; stream_in_data <= 0;
    end else begin
      if (arvalid && arready) begin
        r_left <= arlen + 1;
        r_beats <= r_beats + 1;
        rvalid <= 1;
        rlast <= ((arlen + 1) == 1);
        rdata <= {64'hd00d_0000_0000_0000, r_beats[31:0]};
      end else if (rvalid && rready) begin
        read_words <= read_words + 1;
        if (r_left <= 1) begin
          rvalid <= 0;
          rlast <= 0;
        end else begin
          r_left <= r_left - 1;
          rlast <= (r_left == 2);
          rdata <= rdata + 1;
        end
      end
      if (awvalid && awready) begin
        w_left <= awlen + 1;
        w_beats <= w_beats + 1;
        stream_in_valid <= 1;
        stream_in_data <= {64'hfeed_0000_0000_0000, w_beats[31:0]};
      end else if (wvalid && wready) begin
        write_words <= write_words + 1;
        if (wlast) begin
          w_left <= 0;
          stream_in_valid <= 0;
          bvalid <= 1;
        end else begin
          w_left <= w_left - 1;
          stream_in_data <= stream_in_data + 1;
        end
      end
      if (bvalid && bready) bvalid <= 0;
    end
  end

  initial begin
    repeat (4) @(posedge clk); rst_n <= 1;
    @(posedge clk); base_addr <= 64'h1000; length_bytes <= 80; start_read <= 1;
    @(posedge clk); start_read <= 0;
    wait (done); read_phase = 0;
    @(posedge clk); base_addr <= 64'h2000; length_bytes <= 80; start_write <= 1;
    @(posedge clk); start_write <= 0;
    wait (done);
    repeat (2) @(posedge clk);
    if (read_words != 5) begin $display("DMA_BURST FAIL read_words=%0d", read_words); errors=errors+1; end
    if (write_words != 5) begin $display("DMA_BURST FAIL write_words=%0d", write_words); errors=errors+1; end
    if (errors == 0) $display("DMA_BURST PASS reads=%0d writes=%0d read_cycles=%0d write_cycles=%0d", read_words, write_words, read_cycles, write_cycles);
    $finish;
  end
endmodule
