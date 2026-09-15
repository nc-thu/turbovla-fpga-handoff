// Timing-boundary wrapper for Pack2 array OOC and full-top synthesis.
//
// INPUT_PIPE isolates the external CTX/WRAM fan-in from the systolic edge.
// OUTPUT_PIPE registers the row readout mux output.  The internal PE also has
// a DSP-P boundary register (ae_pe_p2_pa_timing).  All three changes add
// latency, but do not change the 16x48 geometry or the two-product Pack2 math.
`ifndef TVLA_W8A8_PACK2_TIMING_ARRAY_TOP_SV
`define TVLA_W8A8_PACK2_TIMING_ARRAY_TOP_SV
module tvla_w8a8_pack2_timing_array_top #(
  parameter int ROWS = 16,
  parameter int PCOLS = 48,
  parameter bit INPUT_PIPE = 1'b1,
  parameter bit OUTPUT_PIPE = 1'b1
)(
  input  logic clk,
  input  logic rst_n,
  input  logic clr,
  input  logic feed_vld,
  input  logic feed_pulse,
  input  logic [ROWS*8-1:0] a_feed,
  input  logic [PCOLS*16-1:0] b_feed,
  input  logic [((PCOLS+3)/4)*4-1:0] drain_row_rep,
  output logic [PCOLS*2*32-1:0] acc_row
);
  logic [ROWS*8-1:0] a_feed_r;
  logic [PCOLS*16-1:0] b_feed_r;
  logic feed_vld_r, feed_pulse_r;
  logic [((PCOLS+3)/4)*4-1:0] drain_row_rep_r;
  logic [PCOLS*2*32-1:0] acc_row_i;

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      a_feed_r <= '0;
      b_feed_r <= '0;
      feed_vld_r <= 1'b0;
      feed_pulse_r <= 1'b0;
      drain_row_rep_r <= '0;
    end else begin
      a_feed_r <= a_feed;
      b_feed_r <= b_feed;
      feed_vld_r <= feed_vld;
      feed_pulse_r <= feed_pulse;
      drain_row_rep_r <= drain_row_rep;
    end
  end

  tvla_w8a8_pack2_sysarr #(.ROWS(ROWS), .PCOLS(PCOLS)) u_array (
    .clk(clk), .rst_n(rst_n), .clr(clr),
    .feed_vld(INPUT_PIPE ? feed_vld_r : feed_vld),
    .feed_pulse(INPUT_PIPE ? feed_pulse_r : feed_pulse),
    .a_feed(INPUT_PIPE ? a_feed_r : a_feed),
    .b_feed(INPUT_PIPE ? b_feed_r : b_feed),
    .drain_row_rep(INPUT_PIPE ? drain_row_rep_r : drain_row_rep),
    .acc_row(acc_row_i)
  );

  generate
    if (OUTPUT_PIPE) begin : g_output_pipe
      always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) acc_row <= '0;
        else        acc_row <= acc_row_i;
      end
    end else begin : g_no_output_pipe
      always_comb acc_row = acc_row_i;
    end
  endgenerate
endmodule
`endif
