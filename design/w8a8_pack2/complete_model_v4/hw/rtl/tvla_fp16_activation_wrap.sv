// Optional FP16 precision hook.  The default implementation is a registered
// INT16 fallback so the design remains synthesizable without a vendor IP.
// USE_VENDOR_FP16 is reserved for a later Vivado floating-point instance.
`ifndef TVLA_FP16_ACTIVATION_WRAP_SV
`define TVLA_FP16_ACTIVATION_WRAP_SV
module tvla_fp16_activation_wrap #(
  parameter int LANES = 16,
  parameter bit USE_VENDOR_FP16 = 1'b0
) (
  input logic clk,
  input logic rst_n,
  input logic in_valid,
  output logic in_ready,
  input logic [LANES*16-1:0] in_data,
  output logic out_valid,
  input logic out_ready,
  output logic [LANES*16-1:0] out_data
);
  logic holding;
  assign in_ready = !holding || (out_valid && out_ready);
  assign out_valid = holding;
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin holding <= 1'b0; out_data <= '0; end
    else begin
      if (holding && out_ready) holding <= 1'b0;
      if (in_valid && in_ready) begin
        out_data <= in_data;
        holding <= 1'b1;
      end
    end
  end
endmodule
`endif
