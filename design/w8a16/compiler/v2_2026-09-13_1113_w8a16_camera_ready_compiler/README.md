# TurboVLA W8A16 camera-ready compiler

生成时刻：2026-09-13 13:08:00（v2 camera-ready 修订）

这版编译器把 64-bit 指令字和 descriptor sideband 分开保存。指令字只携带操作码、地址和长度；矩阵尺寸、scale、布局、转置和依赖留在同一个 JSON 描述符里。这样硬件接口不变，编译器也不会丢掉 W8A16 的数值信息。

运行：

```powershell
python compile_program.py --output-dir .\data
python emit_descriptors.py --output-dir .\data
```

编译器内部先维护 83 条逻辑操作。向量长度超过 64-bit 指令中的 16-bit transport 字段时，`compile_program.py` 自动切成不超过 65535 个元素／beat 的连续片段，并在 JSON 中写入 `logical_length`、`chunk_index` 和 `chunk_count`。本版示例因此输出 172 条可传输 word，而不是把超长长度截断。

`length_unit` 对 DMA 指令是 beat 数，对向量指令是 element 数，对 GEMM/BMM 由 shape sideband 定义。每条非 END 指令都必须等选中的单元应答；runtime 不再对未完成的 DMA 或激活单元提前应答。

矩阵指令的 `flags[7]` 是阵列选择位。小型 `1x7x8` 动作 smoke 清零该位，走本地动作投影路径；其它 GEMM/BMM 描述符置位后，从系统 top 发出一次 `gemm_start_cmd`，等待 16×48 阵列的 `done`。阵列的激活／权重 feed 和快照 drain 仍由上层 tile scheduler 驱动，不能把 64-bit 指令字误当成完整张量数据。

编译器会检查 PC 连续、字编码、长度范围、矩阵尺寸和 BMM 阵列选择位。LayerNorm/Softmax 的 gamma、beta、mask 作为依赖字段保留；如果运行时没有这些 sideband，记录为 `mapped_candidate`，不会把不完整的参数路径伪装成逐位一致。

本目录输出的 `compile_manifest.json` 和 `descriptor_manifest.json` 包含时间戳、散列和校验结果。文件只写入本版本目录，不覆盖上一版编译器的数据。
