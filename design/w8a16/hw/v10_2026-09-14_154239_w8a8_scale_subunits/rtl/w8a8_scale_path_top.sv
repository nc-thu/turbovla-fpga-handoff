`timescale 1ns/1ps
// Representative hardware comparison for the three software paths:
// MODE=0: INT32 partial sums only (A common integer core; FP32 scale merge
//          is intentionally not synthesized here).
// MODE=1: partial sums + fixed multiplier/shift high-precision output (B).
// MODE=2: MODE=1 + INT8 output requantization (C).
module w8a8_scale_path_top #(
    parameter integer MODE   = 0,
    parameter integer GROUPS = 4,
    parameter integer LANES  = 32
) (
    input  logic                                  clk,
    input  logic                                  rst,
    input  logic                                  in_valid,
    input  logic [GROUPS*LANES*8-1:0]             a_bus,
    input  logic [GROUPS*LANES*8-1:0]             w_bus,
    input  logic signed [GROUPS*24-1:0]           multiplier_bus,
    input  logic [5:0]                            shift,
    output logic                                  out_valid,
    output logic signed [63:0]                   result,
    output logic signed [7:0]                    qresult
);
    wire [GROUPS-1:0] partial_valid;
    wire signed [GROUPS*32-1:0] partial_bus;
    wire merge_valid;
    wire requant_valid;
    wire signed [63:0] merged_bus;
    genvar gi;

    generate
        for (gi = 0; gi < GROUPS; gi = gi + 1) begin : GEN_PARTIAL
            w8a8_partial_accum #(.LANES(LANES)) u_partial (
                .clk(clk), .rst(rst), .in_valid(in_valid),
                .a_bus(a_bus[gi*LANES*8 +: LANES*8]),
                .w_bus(w_bus[gi*LANES*8 +: LANES*8]),
                .out_valid(partial_valid[gi]),
                .sum(partial_bus[gi*32 +: 32])
            );
        end
    endgenerate

    generate
        if (MODE == 0) begin : GEN_MODE_A
            integer ga;
            always_comb begin
                result = 64'sd0;
                for (ga = 0; ga < GROUPS; ga = ga + 1)
                    result = result + $signed(partial_bus[ga*32 +: 32]);
                qresult   = 8'sd0;
                out_valid = partial_valid[0];
            end
        end else begin : GEN_MODE_BC
            w8a8_fixed_merge #(.GROUPS(GROUPS)) u_merge (
                .clk(clk), .rst(rst), .in_valid(partial_valid[0]),
                .partial_bus(partial_bus), .multiplier_bus(multiplier_bus),
                .shift(shift), .out_valid(merge_valid), .merged(merged_bus)
            );
            if (MODE == 1) begin : GEN_MODE_B
                always_comb begin
                    result    = merged_bus;
                    qresult   = 8'sd0;
                    out_valid = merge_valid;
                end
            end else begin : GEN_MODE_C
                w8a8_requant u_requant (
                    .clk(clk), .rst(rst), .in_valid(merge_valid),
                    .value(merged_bus), .shift(shift),
                    .out_valid(requant_valid), .qvalue(qresult)
                );
                always_comb begin
                    result    = merged_bus;
                    out_valid = requant_valid;
                end
            end
        end
    endgenerate
endmodule
