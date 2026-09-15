# 全模型 smoke

`tb_full_model.sv` 是一个最小的宽接口检查：提交一个 descriptor、执行一个向量 ADD 和 END，确认 command/descriptor 握手、done 和 activity observation 能走通。它不是完整 TurboVLA trace 仿真。

本地 Vivado 2021.2 可按以下方式编译（把 `rtl/*.sv` 展开为实际文件列表，并加入 Vivado 自带的 `glbl.v`）：

```text
xvlog -sv rtl/*.sv sim/tb_full_model.sv <Vivado>/data/verilog/src/glbl.v
xelab -debug typical tb_full_model glbl -s tb_full_model_sim -timescale 1ns/1ps
xsim tb_full_model_sim -runall
```

预期输出为 `FULL_MODEL_SMOKE PASS`。完整 trace 的周期和 fallback 统计由 `data/` 中的 Python 编译器结果提供。
