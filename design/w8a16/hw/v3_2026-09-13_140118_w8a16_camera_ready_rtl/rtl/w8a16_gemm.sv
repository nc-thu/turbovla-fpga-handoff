// Streaming wrapper for the W8A16 array.  The compiler/DRAM adapter supplies
// one 16-row activation slice and one 48-column weight slice per feed cycle.
// This first RTL target keeps the memory interface explicit and small; the
// full descriptor scheduler is modeled in Python and can wrap this core later.
`ifndef TVLA_W8A16_GEMM_SV
`define TVLA_W8A16_GEMM_SV
module w8a16_gemm #(
  parameter int ROWS = 16,
  parameter int PCOLS = 48,
  parameter int ACC_W = 40
)(
  input  logic                         clk,
  input  logic                         rst_n,
  input  logic                         start,
  input  logic                         clr,
  input  logic                         feed_vld,
  input  logic                         feed_pulse,
  input  logic [ROWS*16-1:0]           a_feed,
  input  logic [PCOLS*8-1:0]            b_feed,
  input  logic [((ROWS <= 1) ? 1 : $clog2(ROWS))-1:0] drain_row,
  output logic [PCOLS*ACC_W-1:0]      snap_row,
  output logic                         busy,
  output logic                         done
  );
  logic running;
  logic draining;
  logic [7:0] drain_count;
  w8a16_sysarr #(.ROWS(ROWS), .PCOLS(PCOLS), .ACC_W(ACC_W)) u_arr (
    .clk(clk), .rst_n(rst_n), .clr(clr | (start & ~running)),
    .feed_vld(feed_vld & running), .feed_pulse(feed_pulse & running),
    .a_feed(a_feed), .b_feed(b_feed), .drain_row(drain_row), .snap_row(snap_row)
  );
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      running <= 1'b0; busy <= 1'b0; done <= 1'b0;
      draining <= 1'b0; drain_count <= '0;
    end else begin
      done <= 1'b0;
      if (start && !running) begin
        running <= 1'b1; busy <= 1'b1; draining <= 1'b0; drain_count <= '0;
      end
      if (running && feed_pulse) begin
        draining <= 1'b1;
        drain_count <= '0;
      end
      if (running && draining) begin
        // The array delays the pulse through the PE wavefront.  Keep the
        // wrapper busy for a conservative fixed drain interval.
        if (drain_count == (ROWS + PCOLS + 8)) begin
          running <= 1'b0; busy <= 1'b0; done <= 1'b1; draining <= 1'b0;
        end else begin
          drain_count <= drain_count + 1'b1;
        end
      end
    end
  end
endmodule
`endif
