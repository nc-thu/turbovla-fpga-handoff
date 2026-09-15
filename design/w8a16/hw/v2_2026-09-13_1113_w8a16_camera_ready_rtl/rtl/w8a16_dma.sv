// Single-outstanding-burst DMA stream adapter.
// A backend (AXI/DDR or a test memory) answers mem_req/mem_rvalid.  The
// controller keeps address, length and direction explicit so the compiler can
// account for every read and write beat.
`ifndef TVLA_W8A16_DMA_SV
`define TVLA_W8A16_DMA_SV
module w8a16_dma #(
  parameter int DATA_W = 256,
  parameter int ADDR_W = 32
) (
  input  logic                 clk,
  input  logic                 rst_n,
  input  logic                 cmd_valid,
  input  logic                 cmd_write,
  input  logic [ADDR_W-1:0]   cmd_addr,
  input  logic [15:0]         cmd_len,
  output logic                cmd_ready,
  input  logic [DATA_W-1:0]   stream_in_data,
  input  logic                 stream_in_valid,
  output logic                stream_in_ready,
  output logic [DATA_W-1:0]   stream_out_data,
  output logic                stream_out_valid,
  input  logic                stream_out_ready,
  output logic                mem_req,
  output logic                mem_write,
  output logic [ADDR_W-1:0]   mem_addr,
  output logic [DATA_W-1:0]   mem_wdata,
  input  logic [DATA_W-1:0]   mem_rdata,
  input  logic                mem_rvalid,
  output logic                busy,
  output logic                done
);
  typedef enum logic [2:0] {S_IDLE, S_WRITE, S_READ_REQ, S_READ_WAIT, S_READ_OUT} state_t;
  state_t state;
  logic [ADDR_W-1:0] addr_r;
  logic [15:0] remaining_r;
  logic [DATA_W-1:0] out_r;

  assign cmd_ready = (state == S_IDLE);
  assign busy = (state != S_IDLE);
  assign stream_in_ready = (state == S_WRITE);
  assign stream_out_valid = (state == S_READ_OUT);
  assign stream_out_data = out_r;

  always_comb begin
    mem_req = 1'b0;
    mem_write = 1'b0;
    mem_addr = addr_r;
    mem_wdata = stream_in_data;
    if (state == S_WRITE && stream_in_valid) begin
      mem_req = 1'b1;
      mem_write = 1'b1;
    end else if (state == S_READ_REQ) begin
      mem_req = 1'b1;
      mem_write = 1'b0;
    end
  end

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      state <= S_IDLE;
      addr_r <= '0;
      remaining_r <= '0;
      out_r <= '0;
      done <= 1'b0;
    end else begin
      done <= 1'b0;
      case (state)
        S_IDLE: begin
          if (cmd_valid && cmd_ready) begin
            addr_r <= cmd_addr;
            remaining_r <= (cmd_len == 0) ? 16'd1 : cmd_len;
            state <= cmd_write ? S_WRITE : S_READ_REQ;
          end
        end
        S_WRITE: begin
          if (stream_in_valid && stream_in_ready) begin
            addr_r <= addr_r + DATA_W/8;
            if (remaining_r <= 16'd1) begin
              remaining_r <= '0;
              state <= S_IDLE;
              done <= 1'b1;
            end else remaining_r <= remaining_r - 16'd1;
          end
        end
        S_READ_REQ: begin
          state <= S_READ_WAIT;
        end
        S_READ_WAIT: begin
          if (mem_rvalid) begin
            out_r <= mem_rdata;
            state <= S_READ_OUT;
          end
        end
        S_READ_OUT: begin
          if (stream_out_valid && stream_out_ready) begin
            addr_r <= addr_r + DATA_W/8;
            if (remaining_r <= 16'd1) begin
              remaining_r <= '0;
              state <= S_IDLE;
              done <= 1'b1;
            end else begin
              remaining_r <= remaining_r - 16'd1;
              state <= S_READ_REQ;
            end
          end
        end
        default: state <= S_IDLE;
      endcase
    end
  end
endmodule
`endif
