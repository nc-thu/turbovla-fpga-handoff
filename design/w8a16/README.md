# TurboVLA W8A16 专用 768-DSP 工作区

本目录只保存 TurboVLA 的 W8A16 算法、编译器、周期模型和 RTL 验证。旧实验目录作为只读参考，不在这里改写。

当前 camera-ready 候选是 16 行 × 48 物理列的单时钟阵列。每个 PE 使用一颗 DSP，计算一路 INT16 激活乘 INT8 权重，因此阵列保持 768 DSP，但逻辑列数为 48。激活读写口为 256 bit，权重逻辑输入为 384 bit，累加器为 40 bit。runtime、DMA、向量／激活单元和阵列都由同一个 `w8a16_system_top` 接出。

## 目录

- `algo/`：量化语义、scale 和算子清单。
- `arch/`：16×48 阵列周期和流量模型。
- `compiler/`：TurboVLA 专用 W8A16 描述符和映射结果。
- `hw/`：W8A16 PE、阵列、GEMM、激活、DMA、ISA 控制器和 runtime RTL。
- `scripts/`：生成清单、周期数据、检查和报告。
- `reports/`：带秒级时间戳的中文 HTML 工作记录。
- `data/`：机器可读输入、结果和散列。

## 快速检查

```powershell
cd 'E:\GPU ARCH\vector_core_sim\turbovla_w8a16'
python scripts\run_python_checks.py --data-dir data
python scripts\build_inventory.py
python scripts\build_cycles.py
python compiler\v2_2026-09-13_1113_w8a16_camera_ready_compiler\compile_program.py --output-dir compiler\v2_2026-09-13_1113_w8a16_camera_ready_compiler\data
python compiler\v2_2026-09-13_1113_w8a16_camera_ready_compiler\emit_descriptors.py --output-dir compiler\v2_2026-09-13_1113_w8a16_camera_ready_compiler\data
python scripts\build_instruction_costs.py --data-dir compiler\v2_2026-09-13_1113_w8a16_camera_ready_compiler\data
python scripts\isa_sim.py --data-dir compiler\v2_2026-09-13_1113_w8a16_camera_ready_compiler\data --isa-spec data\isa_spec.json
python scripts\collect_rtl_results.py
python scripts\generate_report.py
```

Python 检查不依赖 GPU。服务器上的 Verilator/Icarus 快速回归结果写入 v2 RTL 日志，归档脚本再写入 `data/rtl_results.json`。`isa_sim.py` 检查编译器输出、指令解码和一个带 LIBERO 观测来源的七维动作路径。它不代替真实 TurboVLA 推理，也不代替 LIBERO 成功率。超过 16 bit 的长度由编译器分片，不截断 transport word；当前完整示例是 83 条逻辑指令、172 条可传输 word。
