// Micro-instruction sequencer for tvla_w8a16.camera_ready.v3.isa.
// The 64-bit transport word carries opcode, flags, three compact selectors and
// a 16-bit transport length. M/N/K, scale IDs and extended tensor offsets live
// in the compiler descriptor sideband; the sequencer waits for the selected
// unit to acknowledge completion.
`ifndef TVLA_W8A16_ISA_CTRL_SV
`define TVLA_W8A16_ISA_CTRL_SV
module w8a16_isa_ctrl #(
  parameter int OPCODE_W = 8
) (
  input  logic             clk,
  input  logic             rst_n,
  input  logic [63:0]      instr_word,
  input  logic             instr_valid,
  output logic             instr_ready,
  output logic [OPCODE_W-1:0] op_code,
  output logic [7:0]       op_flags,
  output logic [7:0]       op_dst,
  output logic [7:0]       op_src0,
  output logic [7:0]       op_src1,
  output logic [15:0]      op_length,
  output logic             op_valid,
  input  logic             op_done,
  output logic             busy,
  output logic             done
);
  localparam logic [7:0] OP_END = 8'hff;
  typedef enum logic [1:0] {S_IDLE, S_ISSUE, S_WAIT} state_t;
  state_t state;
  logic [63:0] word_r;
  logic end_r;

  assign instr_ready = (state == S_IDLE);
  assign busy = (state != S_IDLE);
  assign op_code = word_r[63:56];
  assign op_flags = word_r[55:48];
  assign op_dst = word_r[47:40];
  assign op_src0 = word_r[39:32];
  assign op_src1 = word_r[31:24];
  assign op_length = word_r[23:8];
  assign op_valid = (state == S_ISSUE);

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      state <= S_IDLE;
      word_r <= '0;
      end_r <= 1'b0;
      done <= 1'b0;
    end else begin
      done <= 1'b0;
      case (state)
        S_IDLE: begin
          if (instr_valid && instr_ready) begin
            word_r <= instr_word;
            end_r <= (instr_word[63:56] == OP_END);
            state <= S_ISSUE;
          end
        end
        S_ISSUE: begin
          // The selected unit may acknowledge in the same cycle as issue.
          if (end_r) begin
            state <= S_IDLE;
            done <= 1'b1;
          end else if (op_done) state <= S_IDLE;
          else state <= S_WAIT;
        end
        S_WAIT: begin
          if (op_done) state <= S_IDLE;
        end
        default: state <= S_IDLE;
      endcase
    end
  end
endmodule
`endif
