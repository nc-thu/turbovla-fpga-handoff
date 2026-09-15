`timescale 1ns/1ps
module tb_complete_model;
  logic clk = 1'b0;
  logic rst_n = 1'b0;
  always #2 clk = ~clk;

  logic [63:0] cmd_word; logic cmd_valid; wire cmd_ready;
  logic desc_valid; wire desc_ready; logic [15:0] desc_id; logic [15:0] desc_data;
  logic [63:0] activation_data; logic activation_valid; wire activation_ready;
  logic [63:0] weight_data; logic weight_valid; wire weight_ready;
  logic feed_pulse; logic [3:0] drain_row;
  logic [111:0] action_data; logic action_valid; wire action_ready;
  wire action_out_valid; logic action_out_ready; wire [111:0] action_target;
  wire action_gripper; wire [7:0] action_step; wire replay_done;
  wire [31:0] architecture_observe;
  wire m_axi_arvalid; logic m_axi_arready; wire [63:0] m_axi_araddr; wire [7:0] m_axi_arlen;
  logic m_axi_rvalid; logic [127:0] m_axi_rdata; logic m_axi_rlast; wire m_axi_rready;
  wire m_axi_awvalid; logic m_axi_awready; wire [63:0] m_axi_awaddr; wire [7:0] m_axi_awlen;
  wire m_axi_wvalid; logic m_axi_wready; wire [127:0] m_axi_wdata; wire [15:0] m_axi_wstrb;
  wire m_axi_wlast; logic m_axi_bvalid; wire m_axi_bready;

  tvla_complete_model_top dut (
    .clk(clk), .rst_n(rst_n), .cmd_word(cmd_word), .cmd_valid(cmd_valid), .cmd_ready(cmd_ready),
    .desc_valid(desc_valid), .desc_ready(desc_ready), .desc_id(desc_id), .desc_data(desc_data),
    .activation_data(activation_data), .activation_valid(activation_valid), .activation_ready(activation_ready),
    .weight_data(weight_data), .weight_valid(weight_valid), .weight_ready(weight_ready),
    .feed_pulse(feed_pulse), .drain_row(drain_row), .action_data(action_data), .action_valid(action_valid),
    .action_ready(action_ready), .action_out_valid(action_out_valid), .action_out_ready(action_out_ready),
    .action_target(action_target), .action_gripper(action_gripper), .action_step(action_step),
    .replay_done(replay_done), .architecture_observe(architecture_observe),
    .m_axi_arvalid(m_axi_arvalid), .m_axi_arready(m_axi_arready), .m_axi_araddr(m_axi_araddr), .m_axi_arlen(m_axi_arlen),
    .m_axi_rvalid(m_axi_rvalid), .m_axi_rdata(m_axi_rdata), .m_axi_rlast(m_axi_rlast), .m_axi_rready(m_axi_rready),
    .m_axi_awvalid(m_axi_awvalid), .m_axi_awready(m_axi_awready), .m_axi_awaddr(m_axi_awaddr), .m_axi_awlen(m_axi_awlen),
    .m_axi_wvalid(m_axi_wvalid), .m_axi_wready(m_axi_wready), .m_axi_wdata(m_axi_wdata), .m_axi_wstrb(m_axi_wstrb),
    .m_axi_wlast(m_axi_wlast), .m_axi_bvalid(m_axi_bvalid), .m_axi_bready(m_axi_bready)
  );

  task automatic push_desc(input [15:0] id, input [15:0] payload);
    begin
      @(negedge clk);
      desc_id = id; desc_data = payload; desc_valid = 1'b1;
      @(posedge clk);
      while (!desc_ready) @(posedge clk);
      @(negedge clk); desc_valid = 1'b0;
    end
  endtask

  task automatic issue(input [7:0] op, input [15:0] id);
    begin
      push_desc(id, 16'h0001);
      @(negedge clk);
      cmd_word = {op, 8'h00, id, 32'h0}; cmd_valid = 1'b1;
      action_valid = (op == 8'h60);
      @(posedge clk);
      while (!cmd_ready) @(posedge clk);
      @(negedge clk); cmd_valid = 1'b0; action_valid = 1'b0;
      repeat (2) @(posedge clk);
    end
  endtask

  initial begin
    cmd_word = '0; cmd_valid = 1'b0; desc_valid = 1'b0; desc_id = '0; desc_data = '0;
    activation_data = 64'h0102_0304_0506_0708; activation_valid = 1'b0;
    weight_data = 64'h0102_0304_0506_0708; weight_valid = 1'b0;
    feed_pulse = 1'b0; drain_row = '0; action_data = '0; action_valid = 1'b0;
    action_out_ready = 1'b1; m_axi_arready = 1'b1; m_axi_awready = 1'b1;
    m_axi_rvalid = 1'b0; m_axi_rdata = '0; m_axi_rlast = 1'b1;
    m_axi_wready = 1'b1; m_axi_bvalid = 1'b0;
    repeat (4) @(posedge clk); rst_n = 1'b1;

    // Exercise a pointwise operator and its FP16-compatible slot.
    issue(8'h21, 16'd0); // ADD
    // Embedding, layout, BMM, convolution and metadata all have a real sink.
    issue(8'h39, 16'd1); // EMBED
    issue(8'h40, 16'd2); // LAYOUT
    issue(8'h19, 16'd3); // BMM
    issue(8'h42, 16'd4); // CONV/IM2COL
    issue(8'h3d, 16'd5); // MASK
    issue(8'h60, 16'd6); // action post
    issue(8'h01, 16'd7); // DMA read (zero length in compact descriptor)
    @(negedge clk); cmd_word = 64'hff00000000000000; cmd_valid = 1'b1;
    @(posedge clk); while (!cmd_ready) @(posedge clk);
    @(negedge clk); cmd_valid = 1'b0;
    repeat (6) @(posedge clk);
    if (!replay_done) $fatal(1, "complete model did not finish");
    $display("COMPLETE_MODEL_SMOKE PASS done=%0d observe=%h action=%h", replay_done,
             architecture_observe, action_target);
    $finish;
  end
endmodule
