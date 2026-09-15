`timescale 1ns/1ps
// Fixed multiplier/shift merge used by path B and path C.
// Each INT32 partial is multiplied by a signed fixed-point ratio M/2^shift.
module w8a8_fixed_merge #(
    parameter integer GROUPS = 4
) (
    input  logic                         clk,
    input  logic                         rst,
    input  logic                         in_valid,
    input  logic signed [GROUPS*32-1:0]  partial_bus,
    input  logic signed [GROUPS*24-1:0]  multiplier_bus,
    input  logic        [5:0]            shift,
    output logic                         out_valid,
    output logic signed [63:0]            merged
);
    integer g;
    logic signed [63:0] merged_comb;

    always_comb begin
        merged_comb = 64'sd0;
        for (g = 0; g < GROUPS; g = g + 1) begin
            merged_comb = merged_comb
                        + ($signed(partial_bus[g*32 +: 32])
                         * $signed(multiplier_bus[g*24 +: 24]));
        end
    end

    always_ff @(posedge clk) begin
        if (rst) begin
            merged    <= 64'sd0;
            out_valid <= 1'b0;
        end else begin
            out_valid <= in_valid;
            if (in_valid)
                merged <= merged_comb >>> shift;
        end
    end
endmodule
