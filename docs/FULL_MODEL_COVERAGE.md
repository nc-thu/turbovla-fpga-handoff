# TurboVLA 全模型覆盖边界

> 2026-09-16 更新：下面的历史段落保留作对照；当前全模型版本和最终 Vivado 数字以 `design/w8a8_pack2/full_model_v2/` 及本文件末尾的“当前版本更新” 为准。

更新时间：2026-09-15 23:41:16

## 先说结论

现在已经做成并通过 Vivado 实现的是 **W8A8 Pack2 GEMM 数据通路**，不是一颗可以独立完成 TurboVLA 全模型推理的芯片。编译器能把 Linear 和部分满足布局条件的 BMM 变成 Pack2 描述符；其余算子目前主要被记录成 `aux_behavior` 或被保留在原始 dispatch trace 里。`unknown_event_count=0` 只表示本版本的模块分类没有落入“未分类”分支，不能理解成 6836 个底层 dispatch 都已经有对应硬件指令。

## 目前这份 trace 到底编译了多少

数据来自 `design/w8a8_pack2/data/2026-09-14_115230/`：

| 项目 | 数量 | 该数字说明什么 |
|---|---:|---|
| 模块边界事件 | 408 | 采集器看到的高层模块调用 |
| 底层 dispatch 事件 | 6,836 | 包括 `add`、`mul`、`softmax`、布局变换等细粒度操作 |
| 编译器输出 descriptor | 432 | 280 个 Linear、24 个 BMM 子事件、128 个辅助事件 |
| `rtl_gemm` | 280 | 已映射到 Pack2 GEMM |
| `rtl_bmm` | 24 | 复用同一 Pack2 数据通路的条件映射，不是独立 BMM 引擎 |
| `aux_behavior` | 128 | 有周期占位，但当前 Pack2 RTL 不执行该算子的数学运算 |

因此，当前周期模型的 86,410,126 cycles 只能叫“模块级 trace 的条件投影”。它没有把 6,836 个 dispatch 逐条变成硬件指令，也没有把所有布局和数据搬运逐条计入。

## 算子逐项边界

| 全模型部分 | 当前编译器做了什么 | 当前 Pack2 RTL 做了什么 | 当前状态 |
|---|---|---|---|
| Linear / GEMM | 生成 `GEMM_W8A8` descriptor，记录 M/N/K、scale ID、tile 和周期 | 16×48 Pack2 阵列、每 DSP 两个 INT8×INT8 产品、INT32 累加、snapshot、requant | 已有可综合实现 |
| 动态 BMM | 记录两个输入和形状；满足简单布局条件时生成 `BMM_W8A8` | BMM 命令进入同一 GEMM 阵列；没有独立的转置、重排和地址生成单元 | 条件支持 |
| LayerNorm | 112 个模块事件分类为 `LAYER_NORM`/`aux_behavior` | 没有 LayerNorm 数学电路 | 未做成当前 Pack2 电路 |
| Softmax / attention score | 原始 trace 有 18 次 `softmax`、6 次 `baddbmm`；当前只保留 MHA 容器和 BMM 子事件 | 没有 Softmax、指数、归一化和 mask 电路 | 没有独立编译指令和 RTL |
| GELU | 2 个模块事件分类为 fallback；编译器有 GELU opcode | 没有 GELU 电路 | 只有占位成本 |
| Conv2d / im2col | 2 个 Conv2d 事件标成 `im2col_required` | 没有卷积阵列，也没有 im2col 搬运单元 | fallback |
| Bias / Add / Mul | 编译器定义了 opcode，但当前构建流程没有为每个底层 `add`、`mul`、bias 生成独立 descriptor；bias 只进入 GEMM 成本字段 | 没有独立 bias/add/mul 数据通路 | 未完成 |
| Requant | 编译器记录 requant 周期 | `tvla_w8a8_pack2_requant.sv` 已存在并参与 Pack2 路径 | 已有局部电路，未证明全模型格式闭合 |
| Embedding / positional encoding | 原始 trace 有 embedding、cos/sin、arange 等事件，但没有独立硬件 descriptor | 没有 embedding/位置编码电路 | 未完成 |
| Layout / tensor movement | `permute`、`transpose`、`reshape`、`view`、`slice`、`cat`、`contiguous` 等只存在于 dispatch trace | 没有 gather/scatter、转置 buffer 或通用地址生成器 | 未完成 |
| DMA / CTX / WRAM / DDR | 编译器保留 `LOAD_CTX`、`LOAD_WEIGHT`、`STORE_CTX` opcode 名称，但当前 trace 编译没有形成真实 AXI 事务 | 顶层只有流式 activation/weight/output 端口；没有 DDR 控制器、AXI master 或生产级 CTX/WRAM | 未完成 |
| Scheduler / overlap | 周期模型提供 current、double-buffer、queue、R5 四种计算方式 | replay top 有 descriptor FIFO 和计数器，但没有已验证的读算写双缓冲数据通路 | 模型有，硬件未闭合 |
| DINO / BERT / action head | 其中 Linear 子层可编译，非线性、归一化、布局和注意力外围仍被拆成辅助事件 | 没有完整视觉编码器、语言编码器或动作后处理电路 | 只有 GEMM 子集 |
| Scale / calibration | descriptor 发出 scale ID；当前 `scale_table.json` 的静态硬件系数仍是 `pending_calibration` | 没有动态 scale 采集和全模型校准加载路径 | 未完成 |
| Action post-processing | `clamp`、`tanh`、类型转换等保留在原始 dispatch 中 | 没有动作后处理和机器人接口电路 | 未完成 |

## RTL 实际识别的命令范围

当前 replay top 的真实 RTL 分支主要识别：

- `0x18`：GEMM；
- `0x19`：BMM，仍走 Pack2 阵列；
- `0xff`：结束；
- `0x30/0x31/0x33`：只增加向量/fallback 计数，不执行 LayerNorm、Softmax 或 GELU 数学运算；
- 其他命令：按 fallback 周期累计。

这说明编译器里列出 opcode，不等于 RTL 已经实现该 opcode。完整支持还需要为每个指令定义输入/输出 buffer、数据格式、握手、周期和正确性测试。

## 当前已经做成的硬件

以下部分有 RTL 和实现结果：

1. Pack2 预加器和两个 INT8 乘积抽取；
2. 16 行 × 48 物理列、768 DSP 的阵列；
3. INT32 累加、27-bit snapshot、读出和 requant 局部路径；
4. descriptor FIFO、命令握手和活动计数器；
5. Vivado 2021.2 的 generic top 综合、布局和布线。

250 MHz 约束下 post-route WNS 为 `+0.241 ns`，303.215 MHz 目标下为 `+0.103 ns`。这证明当前 generic Pack2 top 能实现，不证明全模型可以在 FPGA 板上独立运行。

## 要变成“全模型推理芯片”，下一步缺什么

建议按这个顺序补，不要先把当前 GEMM 的 GOPS 当成全模型吞吐：

1. 先让编译器把所有重要 dispatch 变成显式 descriptor，特别是 LayerNorm、Softmax、GELU、bias/add/mul、embedding 和布局搬运；
2. 实现真正的 CTX/WRAM/DMA/AXI 数据路径，让 descriptor 中的地址和 stride 能驱动实际读写；
3. 为 LayerNorm、Softmax/GELU 和 bias/add/mul 做共享向量单元，并定义 INT8/INT32/FP 中间格式；
4. 给 BMM 加转置、mask、缩放和双输入重排，验证动态 attention 的两个操作数都能按依赖进入阵列；
5. 导入静态 scale/bias 表，完成完整 trace 的 payload 回放，再做多 suite 的纯整数 LIBERO 验证。

在这些步骤完成前，报告里应把 Pack2 结果称为“GEMM/BMM 子集的实测实现 + 其余算子的行为级周期占位”，不要称为 TurboVLA 全模型 FPGA 推理结果。

## 当前版本更新（2026-09-16 03:33:14）

本次 `full_model_v2` 使用同一份真实 TurboVLA dispatch trace，把每个 dispatch 都写入 descriptor。统计为 6836 个 dispatch、6836 个 descriptor、301 个 `rtl_gemm`、30 个 `rtl_bmm`、973 个 `layout_rtl`、561 个 `vector_rtl`、3 个 `memory_rtl` 和 4968 个 `aux_behavior`；`unknown=0` 代表分类完整，不代表 6836 个事件都有对应专用电路。

### 已有电路与仅有编译器分类的区别

| 部分 | 当前状态 | 需要继续补的内容 |
|---|---|---|
| Pack2 GEMM/BMM | 16×48、768-DSP、INT8×INT8、INT32 累加、snapshot/readout/requant 有可综合 RTL | 完整 payload 回放、静态 scale/bias 闭合 |
| 向量 primitive | 有 16-lane Add/Mul/Clamp 等接口，LayerNorm/Softmax/Div 使用有界整数近似 | 接入精确数值方案并逐算子对拍 |
| Layout/embedding/im2col/CTX-WRAM | 有对应小模块或存储接口 | 大张量地址生成、容量和冲突验证 |
| AUX/fallback | 有 descriptor、事件顺序、周期和 payload 位置 | DINO/T5/backbone、完整 attention、非线性和采样专用电路 |
| DMA/DDR | 顶层有行为级单拍 AXI 端口 | 真实 DDR 控制器、带宽、背压和板级约束 |

### 最终 generic top 结果

Vivado 2021.2 在 `xczu7ev-ffvc1156-2-e` 上对 `vivado_runs_20260916_0248` 完成 route。资源为 89,795 LUT、193,533 FF、784 DSP、25.5 BRAM；vectorless power 为 5.733 W（Low confidence）。4 ns setup WNS=-0.303 ns，250 MHz 约束未通过；DRC 没有 Error，但有 generic top I/O critical warning。这个结果证明顶层可以被工具实现，不证明整模型已经能在 FPGA 板上运行。

对应周期模型为 565,587,640 cycles、1.794% PE 时间利用率、61.13% GEMM 利用率和 13.78 GOPS@250 MHz。周期模型把 6505 个 AUX/fallback 事件的成本保留在总时间里，因此不能把 13.78 GOPS 当成 Pack2 的物理峰值 768 GOPS。

### 仍然没有做成全模型电路或完整编译支持的项目

1. DINO/视觉 backbone：patch embedding、完整视觉 attention/投影、归一化和 feature 读写。
2. T5/语言 encoder：token embedding、Transformer block、语言 KV/cache 和文本端量化加载。
3. 复杂动态 attention/BMM：mask、转置、双输入重排和不满足布局条件的 BMM。
4. 精确 FP16 激活 IP：当前 `tvla_fp16_activation_wrap.sv` 只是注册接口占位，不是 Xilinx Floating-Point IP。
5. 完整 bias、动态 scale、采样更新和动作后处理链：部分仍是 AUX/fallback，不能按零周期处理。
6. 生产级数据通路：真实 AXI/DDR/NoC、容量管理、跨算子背压、bitstream、板级时序和 LIBERO 端到端执行。

所以，“编译器没有漏掉事件”和“全模型已经有专用硬件”是两件事。当前交接包支持架构师复现分类、Pack2 子集和 generic top 实现；要声称全模型 FPGA 推理，还需要补齐上述六类内容并完成整条 trace 的逐位回放。
