// Metadata/control unit for identity, fill, mask and reduction events that
// surround the numerical operators.  It preserves command order and gives
// the cycle model a real destination for bookkeeping operations.
`ifndef TVLA_META_UNIT_SV
`define TVLA_META_UNIT_SV
module tvla_meta_unit #(
  parameter int LANES = 16,
  parameter int DW = 16
) (
  input logic clk,
  input logic rst_n,
  input logic in_valid,
  output logic in_ready,
  input logic [3:0] mode,
  input logic [LANES*DW-1:0] in_data,
  input logic [LANES*DW-1:0] aux_data,
  output logic out_valid,
  input logic out_ready,
  output logic [LANES*DW-1:0] out_data
);
  logic holding;
  integer i;
  assign in_ready = !holding || (out_valid && out_ready);
  assign out_valid = holding;
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      holding <= 1'b0;
      out_data <= '0;
    end else begin
      if (holding && out_ready) holding <= 1'b0;
      if (in_valid && in_ready) begin
        case (mode)
          4'd1: out_data <= '0;                 // FILL
          4'd2: out_data <= in_data & aux_data; // MASK
          4'd3: begin                            // REDUCE broadcast sum
            out_data <= '0;
            for (i = 0; i < LANES; i = i + 1)
              out_data[i*DW +: DW] <= in_data[i*DW +: DW];
          end
          default: out_data <= in_data;         // IDENTITY / control
        endcase
        holding <= 1'b1;
      end
    end
  end
endmodule
`endif
