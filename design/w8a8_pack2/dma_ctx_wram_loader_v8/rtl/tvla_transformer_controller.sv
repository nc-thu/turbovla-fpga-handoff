// Lightweight layer controller for DINO, language and action-head command
// streams.  It does not contain model weights; descriptors identify those
// weights in CTX/WRAM.  The controller makes layer boundaries and barriers
// explicit so the compiler and the RTL replay have the same ordering.
`ifndef TVLA_TRANSFORMER_CONTROLLER_SV
`define TVLA_TRANSFORMER_CONTROLLER_SV
module tvla_transformer_controller #(
  parameter int LAYER_W = 8,
  parameter int MAX_LAYERS = 64
) (
  input logic clk,
  input logic rst_n,
  input logic start,
  input logic [LAYER_W-1:0] layer_count,
  input logic [15:0] descriptor_count,
  input logic dispatch_ready,
  output logic dispatch_valid,
  output logic [LAYER_W-1:0] layer_index,
  output logic [15:0] descriptor_index,
  output logic barrier,
  output logic busy,
  output logic done
);
  logic [15:0] emitted;
  logic [LAYER_W-1:0] layers;
  logic active;
  localparam logic [LAYER_W-1:0] MAX_LAYERS_VALUE = MAX_LAYERS;
  // Keep the running state registered.  The previous version derived busy
  // from dispatch_valid and dispatch_valid from busy, which created a
  // combinational loop in synthesis and made the controller unsafe for an
  // integrated top-level implementation.
  assign busy = active;
  assign dispatch_valid = active && !done && (emitted < descriptor_count);
  assign barrier = dispatch_valid && (emitted[3:0] == 4'hf);
  assign layer_index = (descriptor_count == 0) ? '0 :
                       (emitted * layer_count) / descriptor_count;
  assign descriptor_index = emitted;
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      emitted <= '0; layers <= '0; active <= 1'b0; done <= 1'b0;
    end else begin
      if (start && !active) begin
        emitted <= '0;
        layers <= (layer_count > MAX_LAYERS) ? MAX_LAYERS_VALUE : layer_count;
        done <= (descriptor_count == 0);
        active <= (descriptor_count != 0);
      end else if (dispatch_valid && dispatch_ready) begin
        if (emitted + 1'b1 >= descriptor_count) begin
          emitted <= emitted + 1'b1;
          done <= 1'b1;
          active <= 1'b0;
        end else emitted <= emitted + 1'b1;
      end
    end
  end
endmodule
`endif
