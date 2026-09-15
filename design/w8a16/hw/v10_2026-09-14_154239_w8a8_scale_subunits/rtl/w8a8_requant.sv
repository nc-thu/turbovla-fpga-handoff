`timescale 1ns/1ps
// Optional INT8 output requantizer used only by path C.
// Rounding is ties-to-even before the signed INT8 clamp.
module w8a8_requant (
    input  logic                         clk,
    input  logic                         rst,
    input  logic                         in_valid,
    input  logic signed [63:0]            value,
    input  logic        [5:0]            shift,
    output logic                         out_valid,
    output logic signed [7:0]             qvalue
);
    logic signed [63:0] rounded;
    logic signed [63:0] shifted;
    logic signed [63:0] base;
    logic signed [63:0] rem;
    logic signed [63:0] half;

    always_comb begin
        if (shift == 0) begin
            rounded = value;
        end else begin
            half = 64'sd1 <<< (shift - 1);
            base = value >>> shift;
            rem  = value - (base <<< shift);
            rounded = base;
            if ((rem > half) || ((rem == half) && base[0]))
                rounded = base + 64'sd1;
        end
        if (rounded > 64'sd127)
            shifted = 64'sd127;
        else if (rounded < -64'sd127)
            shifted = -64'sd127;
        else
            shifted = rounded;
    end

    always_ff @(posedge clk) begin
        if (rst) begin
            qvalue    <= 8'sd0;
            out_valid <= 1'b0;
        end else begin
            out_valid <= in_valid;
            if (in_valid)
                qvalue <= shifted[7:0];
        end
    end
endmodule
