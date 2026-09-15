# TurboVLA W8A16 编译器适配

本目录定义 `tvla_w8a16.v1` 描述符。它只描述 W8A16 线性／矩阵乘法和明确的 fallback，不修改共享编译器的公共接口。

每个可映射任务包含 `M/N/K`、A16/W8/O16 位宽、40-bit 累加、布局、地址、scale 标识和 bias 处理方式。动态 BMM 只有在两个操作数都满足相同布局和数值配置时才会拆成 GEMM。

`compile_program.py` 另外生成一个 64-bit `word_hex`：高 8 bit 是 opcode，随后是 flags、dst、src0、src1、16-bit length，最低 8 bit 保留。矩阵尺寸、scale ID、stride 和 fallback 原因留在 JSON 描述符侧带里。当前完整示例程序有 83 条指令，短动作程序有 7 条，并额外生成 18 条 opcode 编码目录项；`scripts/isa_sim.py` 会逐条检查它们能被 `data/isa_spec.json` 解码，并验证 END 在两个可执行程序末尾。
