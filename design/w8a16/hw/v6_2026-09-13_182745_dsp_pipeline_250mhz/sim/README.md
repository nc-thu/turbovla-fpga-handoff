# RTL 验证（v2 camera-ready）

更新时间：2026-09-13 13:08:00

`run_verilator.sh` 按顺序运行 PE、4×4、16×48、requant、GEMM、激活、向量、DMA、ISA 控制器、runtime 和 system top，共 11 项。最新服务器回归在 144 秒内全部通过，记录在 `logs/verilator_run.json`。Verilator 使用行为级 DSP48E2 模型；16×48 阵列仍是 768 颗 DSP。

`run_iverilog_smoke.sh` 只做秒级语法／行为冒烟，覆盖 PE、阵列、激活、ISA 和 runtime。LayerNorm/Softmax 的逐位除法会增加延迟，所以激活 smoke 的等待窗口按最大 N=4 延迟设置。`run_unisim_smoke.sh` 只有在安装 Vivado 的服务器上才会调用 `xvlog`；当前服务器没有该命令，结果记录为 `unavailable`，不能冒充硬原语回归。

`tb_w8a16_system.sv` 检查 runtime、两条 DMA 和 16×48 阵列接口能同时 elaboration；`tb_w8a16_runtime.sv` 进一步检查动作路径、向量单元、REQUANT、DMA 完成等待和控制指令。两者都是 tile-level smoke，不等于完整 TurboVLA 权重、DINO/T5 或 LIBERO 回合已经在 RTL 中执行。
