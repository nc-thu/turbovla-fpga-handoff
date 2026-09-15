// One TurboVLA W8A16 PE.  It has one DSP, one INT40 feedback accumulator and
// one INT40 snapshot.  The snapshot is read separately from the live state.
`ifndef TVLA_W8A16_PE_SV
`define TVLA_W8A16_PE_SV
module w8a16_pe #(
  parameter int ACC_W = 40
)(
  input  logic                   clk,
  input  logic                   rst_n,
  input  logic                   clr,
  input  logic                   pulse_in,
  input  logic                   av_in,
  input  logic                   bv_in,
  input  logic signed [15:0]     a_in,
  input  logic signed [7:0]      b_in,
  output logic                   av_out,
  output logic                   bv_out,
  output logic                   pulse_out,
  output logic signed [15:0]     a_out,
  output logic signed [7:0]      b_out,
  output logic signed [ACC_W-1:0] acc,
  output logic signed [ACC_W-1:0] snap
);
  logic signed [15:0] a_r;
  logic signed [7:0]  b_r;
  logic               av_r, bv_r, pulse_r;
  logic signed [47:0] p;
  logic               p_v;
  // Keep the DSP output boundary visible to synthesis.  The register also
  // narrows the product before it reaches the 40-bit feedback adder.
  (* keep = "true" *) logic signed [31:0] product_r;
  (* keep = "true" *) logic               product_v;
  (* use_dsp = "no" *) logic signed [ACC_W-1:0] acc_r;
  logic signed [ACC_W-1:0] snap_r;
  wire signed [ACC_W-1:0] product_ext = {{(ACC_W-32){product_r[31]}}, product_r};

  w8a16_mult #(.A_REG(1), .B_REG(1), .M_REG(1), .P_REG(1)) u_mult (
    .clk(clk), .v_in(av_r & bv_r), .a_in(a_r), .w_in(b_r),
    .p_out(p), .v_out(p_v)
  );

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      a_r <= '0; b_r <= '0; av_r <= 1'b0; bv_r <= 1'b0; pulse_r <= 1'b0;
      product_r <= '0; product_v <= 1'b0; acc_r <= '0; snap_r <= '0;
    end else begin
      a_r <= a_in; b_r <= b_in; av_r <= av_in; bv_r <= bv_in; pulse_r <= pulse_in;
      product_r <= p[31:0];
      product_v <= p_v;
      if (pulse_in) begin
        snap_r <= acc_r;
        acc_r <= '0;
      end else if (clr) begin
        acc_r <= '0;
      end else if (product_v) begin
        acc_r <= acc_r + product_ext;
      end
    end
  end
  assign av_out = av_r;
  assign bv_out = bv_r;
  assign pulse_out = pulse_r;
  assign a_out = a_r;
  assign b_out = b_r;
  assign acc = acc_r;
  assign snap = snap_r;
endmodule
`endif
