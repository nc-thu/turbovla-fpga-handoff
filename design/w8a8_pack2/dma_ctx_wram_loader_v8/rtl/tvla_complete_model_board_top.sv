// Board-facing wrapper for the complete-model top.
//
// The simulation top deliberately exposes wide internal buses so that a test
// bench can inject a complete descriptor and tile in one cycle.  Those buses
// are not a useful FPGA pinout: they exceed the package I/O budget.  This
// wrapper keeps the same internal protocol but presents a narrow command
// stream, a tagged 64-bit payload stream, and 64-bit AXI data channels.
`ifndef TVLA_COMPLETE_MODEL_BOARD_TOP_SV
`define TVLA_COMPLETE_MODEL_BOARD_TOP_SV
module tvla_complete_model_board_top #(
  parameter int ROWS = 16,
  parameter int PCOLS = 48,
  parameter int DESC_W = 512,
  parameter int DESC_ID_W = 16
) (
  input  logic clk,
  input  logic rst_n,

  // One command beat carries the 64-bit opcode word and a descriptor index.
  input  logic [63:0] host_cmd_word,
  input  logic [15:0] host_desc_id,
  input  logic [15:0] host_desc_data,
  input  logic host_cmd_valid,
  output logic host_cmd_ready,

  // payload_kind: 0 = activation beat, 1 = weight beat,
  // 2 = action low 64 bits, 3 = action high 48 bits.
  input  logic [63:0] host_payload,
  input  logic [1:0] host_payload_kind,
  input  logic host_payload_valid,
  output logic host_payload_ready,
  input  logic host_feed_pulse,
  input  logic [3:0] host_drain_row,

  output logic [63:0] host_action_out,
  output logic [1:0] host_action_word_index,
  output logic host_action_gripper,
  output logic [7:0] host_action_step,
  output logic host_action_valid,
  input  logic host_action_ready,
  output logic host_done,
  output logic [31:0] host_observe,

  // Narrow AXI4 read channel.
  output logic m_axi_arvalid,
  input  logic m_axi_arready,
  output logic [63:0] m_axi_araddr,
  input  logic m_axi_rvalid,
  input  logic [63:0] m_axi_rdata,
  input  logic m_axi_rlast,
  output logic m_axi_rready,
  // Narrow AXI4 write channel.
  output logic m_axi_awvalid,
  input  logic m_axi_awready,
  output logic [63:0] m_axi_awaddr,
  output logic m_axi_wvalid,
  input  logic m_axi_wready,
  output logic [63:0] m_axi_wdata,
  output logic m_axi_wlast,
  input  logic m_axi_bvalid,
  output logic m_axi_bready
);
  logic [63:0] cmd_word;
  logic cmd_valid, cmd_ready;
  logic desc_valid, desc_ready;
  logic [DESC_ID_W-1:0] desc_id;
  logic [15:0] desc_data;
  logic [63:0] activation_data, weight_data;
  logic activation_valid, activation_ready;
  logic weight_valid, weight_ready;
  logic [111:0] action_data;
  logic action_valid, action_ready;
  logic action_out_valid, action_out_ready;
  logic [111:0] action_target;
  logic action_gripper;
  logic [7:0] action_step;
  logic replay_done;
  logic [31:0] architecture_observe;
  logic [127:0] core_wdata;
  logic [15:0] core_wstrb;
  logic [7:0] core_arlen, core_awlen;

  // The command and descriptor sideband are accepted together.  Keeping
  // desc_valid tied to cmd_valid matches the compiler's one-descriptor-per-
  // command stream and avoids an external 512-bit descriptor pin bus.
  assign cmd_word = host_cmd_word;
  assign desc_id = host_desc_id;
  assign desc_data = host_desc_data;
  assign cmd_valid = host_cmd_valid;
  assign desc_valid = host_cmd_valid;
  assign host_cmd_ready = cmd_ready && desc_ready;

  // Directly forward one 64-bit payload beat to the matching internal port.
  // The internal memory/array interfaces consume the same beat repeatedly for
  // wider tiles; the compiler controls the beat count in the descriptor.
  assign activation_data = host_payload;
  assign weight_data = host_payload;
  assign activation_valid = host_payload_valid && (host_payload_kind == 2'd0);
  assign weight_valid = host_payload_valid && (host_payload_kind == 2'd1);
  always_comb begin
    case (host_payload_kind)
      2'd0: host_payload_ready = activation_ready;
      2'd1: host_payload_ready = weight_ready;
      2'd2, 2'd3: host_payload_ready = !action_valid;
      default: host_payload_ready = 1'b0;
    endcase
  end

  // Action output is widened internally for the robot adapter but exposed as
  // one 128-bit response beat on the board side.
  // The action target is 112 bits internally.  Serialize it as two 64-bit
  // response beats so that the board pinout stays within the package budget.
  logic [1:0] action_word_index;
  assign action_out_ready = host_action_ready && (action_word_index == 2'd1);
  assign host_action_valid = action_out_valid;
  assign host_action_word_index = action_word_index;
  assign host_action_out = (action_word_index == 2'd0) ? action_target[63:0] :
                           {16'd0, action_target[111:64]};
  assign host_action_gripper = action_gripper;
  assign host_action_step = action_step;
  assign host_done = replay_done;
  assign host_observe = architecture_observe;

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) action_word_index <= 2'd0;
    else if (action_out_valid && host_action_ready) begin
      if (action_word_index == 2'd0) action_word_index <= 2'd1;
      else action_word_index <= 2'd0;
    end
  end

  // Assemble a 112-bit action input from two tagged payload beats.  The low
  // beat arrives first; the upper 48 bits are taken from the low portion of
  // the second beat.  A new low beat replaces an already consumed action.
  logic action_half;
  logic [63:0] action_low;
  logic [47:0] action_high;
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      action_half <= 1'b0;
      action_low <= '0;
      action_high <= '0;
      action_valid <= 1'b0;
    end else begin
      if (host_payload_valid && host_payload_kind == 2'd2 && host_payload_ready) begin
        action_low <= host_payload;
        action_half <= 1'b1;
        action_valid <= 1'b0;
      end
      if (host_payload_valid && host_payload_kind == 2'd3 && host_payload_ready && action_half) begin
        action_high <= host_payload[47:0];
        action_half <= 1'b0;
        action_valid <= 1'b1;
      end
      if (action_valid && action_ready) action_valid <= 1'b0;
    end
  end
  assign action_data = {action_high, action_low};

  tvla_complete_model_top #(
    .ROWS(ROWS), .PCOLS(PCOLS), .DESC_W(DESC_W), .DESC_ID_W(DESC_ID_W)
  ) u_core (
    .clk(clk), .rst_n(rst_n), .cmd_word(cmd_word), .cmd_valid(cmd_valid),
    .cmd_ready(cmd_ready), .desc_valid(desc_valid), .desc_ready(desc_ready),
    .desc_id(desc_id), .desc_data(desc_data),
    .activation_data(activation_data), .activation_valid(activation_valid),
    .activation_ready(activation_ready), .weight_data(weight_data),
    .weight_valid(weight_valid), .weight_ready(weight_ready),
    .feed_pulse(host_feed_pulse), .drain_row(host_drain_row),
    .action_data(action_data), .action_valid(action_valid),
    .action_ready(action_ready), .action_out_valid(action_out_valid),
    .action_out_ready(action_out_ready), .action_target(action_target),
    .action_gripper(action_gripper), .action_step(action_step),
    .replay_done(replay_done), .architecture_observe(architecture_observe),
    .m_axi_arvalid(m_axi_arvalid), .m_axi_arready(m_axi_arready),
    .m_axi_araddr(m_axi_araddr), .m_axi_arlen(core_arlen), .m_axi_rvalid(m_axi_rvalid),
    .m_axi_rdata({64'd0, m_axi_rdata}), .m_axi_rlast(m_axi_rlast),
    .m_axi_rready(m_axi_rready), .m_axi_awvalid(m_axi_awvalid),
    .m_axi_awready(m_axi_awready), .m_axi_awaddr(m_axi_awaddr), .m_axi_awlen(core_awlen),
    .m_axi_wvalid(m_axi_wvalid), .m_axi_wready(m_axi_wready),
    .m_axi_wdata(core_wdata), .m_axi_wstrb(core_wstrb), .m_axi_wlast(m_axi_wlast),
    .m_axi_bvalid(m_axi_bvalid), .m_axi_bready(m_axi_bready)
  );

  // The core's AXI data path is 128 bits.  In this first board wrapper the
  // lower 64 bits are the external data lane; the upper half is intentionally
  // ignored and is reported as a single-beat narrow-AXI integration mode.
  assign m_axi_wdata = core_wdata[63:0];
endmodule
`endif
