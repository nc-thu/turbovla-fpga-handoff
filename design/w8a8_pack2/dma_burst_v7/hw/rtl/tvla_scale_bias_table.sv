// Static scale and bias table used by the integer deployment path.
//
// Software keeps human-readable scale IDs in JSON.  The compiler also emits
// numeric indices in descriptor bits [432:495].  This table is the hardware
// end of that mapping: a loader writes calibrated values once, and every
// GEMM/vector command reads them synchronously without parsing strings.
`ifndef TVLA_SCALE_BIAS_TABLE_SV
`define TVLA_SCALE_BIAS_TABLE_SV
module tvla_scale_bias_table #(
  parameter int DEPTH = 4096,
  parameter int ADDR_W = (DEPTH <= 2) ? 1 : $clog2(DEPTH)
) (
  input logic clk,
  input logic rst_n,
  input logic wr_valid,
  input logic [ADDR_W-1:0] wr_index,
  input logic [15:0] wr_a_scale,
  input logic [15:0] wr_w_scale,
  input logic [15:0] wr_out_scale,
  input logic signed [31:0] wr_bias,
  input logic [ADDR_W-1:0] rd_index,
  output logic [15:0] rd_a_scale,
  output logic [15:0] rd_w_scale,
  output logic [15:0] rd_out_scale,
  output logic signed [31:0] rd_bias,
  output logic [31:0] version
);
  // Keep reset out of the inferred RAM write process.  Vivado cannot infer a
  // block RAM when the memory array is in an asynchronous-reset always_ff;
  // the old version therefore dissolved the 131,072-bit bias table into
  // registers and failed elaboration.  valid_mem provides the reset state.
  (* ram_style = "block" *) logic [15:0] a_mem [0:DEPTH-1];
  (* ram_style = "block" *) logic [15:0] w_mem [0:DEPTH-1];
  (* ram_style = "block" *) logic [15:0] out_mem [0:DEPTH-1];
  (* ram_style = "block" *) logic signed [31:0] bias_mem [0:DEPTH-1];
  logic [DEPTH-1:0] valid_mem;

  always_ff @(posedge clk) begin
    if (wr_valid) begin
      a_mem[wr_index] <= wr_a_scale;
      w_mem[wr_index] <= wr_w_scale;
      out_mem[wr_index] <= wr_out_scale;
      bias_mem[wr_index] <= wr_bias;
    end
  end

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      rd_a_scale <= 16'h3c00; // FP16 1.0 until calibration is loaded.
      rd_w_scale <= 16'h3c00;
      rd_out_scale <= 16'h3c00;
      rd_bias <= '0;
      version <= '0;
      valid_mem <= '0;
    end else begin
      if (wr_valid) begin
        valid_mem[wr_index] <= 1'b1;
        version <= version + 1'b1;
      end
      if (valid_mem[rd_index]) begin
        rd_a_scale <= a_mem[rd_index];
        rd_w_scale <= w_mem[rd_index];
        rd_out_scale <= out_mem[rd_index];
        rd_bias <= bias_mem[rd_index];
      end else begin
        rd_a_scale <= 16'h3c00;
        rd_w_scale <= 16'h3c00;
        rd_out_scale <= 16'h3c00;
        rd_bias <= '0;
      end
    end
  end
endmodule
`endif
