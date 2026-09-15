`timescale 1ns/1ps
// One representative INT8xINT8 partial-sum block.
// The block deliberately exposes the integer accumulation boundary used by
// the software A/B/C experiment.  Scale merging is kept outside this block.
module w8a8_partial_accum #(
    parameter integer LANES = 32
) (
    input  logic                         clk,
    input  logic                         rst,
    input  logic                         in_valid,
    input  logic [LANES*8-1:0]            a_bus,
    input  logic [LANES*8-1:0]            w_bus,
    output logic                         out_valid,
    output logic signed [31:0]            sum
);
    integer i;
    logic signed [31:0] sum_comb;
    wire signed [31:0] products [0:LANES-1];
    genvar gi;

    generate
        for (gi = 0; gi < LANES; gi = gi + 1) begin : GEN_DSP
            w8a8_dsp_mult u_mult (
                .a_in(a_bus[gi*8 +: 8]),
                .w_in(w_bus[gi*8 +: 8]),
                .p_out(products[gi])
            );
        end
    endgenerate

    always_comb begin
        sum_comb = 32'sd0;
        for (i = 0; i < LANES; i = i + 1) begin
            sum_comb = sum_comb + products[i];
        end
    end

    always_ff @(posedge clk) begin
        if (rst) begin
            sum       <= 32'sd0;
            out_valid <= 1'b0;
        end else begin
            out_valid <= in_valid;
            if (in_valid)
                sum <= sum_comb;
        end
    end
endmodule
