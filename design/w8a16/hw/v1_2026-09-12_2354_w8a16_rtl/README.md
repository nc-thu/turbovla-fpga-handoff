# W8A16 RTL v1

主 RTL 是 16×48 单时钟阵列。每个 PE 使用一颗 DSP 计算一路 signed INT16×INT8 乘法；中间结果保留 INT16，累加器和快照为 40 bit。阵列之外还提供向量激活单元、DMA 读写、64-bit ISA 控制器和一个可独立仿真的 runtime seam。

```text
sim/run_verilator.sh       # 长回归首选
sim/run_iverilog_smoke.sh  # 仅秒级语法/行为冒烟
synth/run_top_synth.ps1    # 系统顶层 + 1×1、4×4、16×48 Vivado 逻辑综合
```

`synth/top_w8a16_system.sv` 是把 runtime、两路 DMA、向量算子和重新量化接在一起的综合壳，不是最终板级 AXI/DDR 顶层。当前目录不包含完整系统互连和布线。综合报告中的 Fmax 是 3.298 ns 约束下的综合估算，不能当成 post-route 结果。

Verilator 回归包含 PE、4×4、16×48、requant、GEMM、激活、vector_ops、DMA、ISA 控制器和 runtime 十个测试。Icarus 只跑 PE、4×4、激活和 ISA 四个短测试。runtime 的动作输出来自确定性小矩阵和已有 LIBERO 初始状态元数据；它只验证编译器字、地址顺序和七维动作打包，不表示完整 TurboVLA 已经驱动 LIBERO。
