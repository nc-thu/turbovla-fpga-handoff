# RTL 快速验证

`run_verilator.sh` 按顺序运行 PE、4×4、16×48、requant、GEMM、激活、向量、DMA、ISA 控制器和 runtime，共十项。真实 DSP48E2 冒烟需要在有 UNISIM 的 Vivado 环境中去掉 `VERILATOR` 宏；长测试只使用 Verilator，避免 Icarus 慢仿真。

`tb_w8a16_runtime.sv` 发送编译器 smoke 程序同构的 LOAD_CTX、LOAD_WEIGHT、GEMM、BIAS_ADD、TANH、STORE_ACTION、END 命令。它使用固定的 1×7×8 整数数据，检查一个可解码、可打包的动作输出。它不加载完整 TurboVLA 权重，也不替代 LIBERO 回合。
