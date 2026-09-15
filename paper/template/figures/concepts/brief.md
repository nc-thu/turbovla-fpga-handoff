# 网页 GPT 论文图像草案

生成时间：2026-09-12 12:29:20（Asia/Shanghai）  
网页 GPT 交付标签页：<https://chatgpt.com/c/6aa4d1f2-d1f4-83e9-8452-8515560351dc>

后续重绘的真实视觉参考为：`E:/GPU ARCH/vector_core_sim/paper/2026-09-12_vla_fpga/figures/references/ditpa_fig11_12_13.png`（Fig. 11–13 拼图）和 `ditpa_page2.png`（Fig. 2 整页）。当前 Chrome 扩展通道尝试通过网页“从电脑上传”提交这两张 PNG 时，文件选择器返回 `Not allowed`，因此本轮没有伪称已上传，也没有用纯文字提示替代真实参考图。旧 PNG 草图均标记为 superseded，等待真实参考上传后重绘。

三张图均由网页版 GPT 根据本项目提供的架构事实原创生成。整体只借鉴 DiTPA 第 2 页的白底、黑色轮廓、淡色填充、多面板和简短英文标签风格，没有复制原图。PNG 是论文重绘草案，正式投稿前应在 Visio 或矢量绘图工具中重画并校对公式、箭头和字体。

## 图 1：overview

文件：`fig_overview_concept_2026-09-12_121742.png`  
生成完成：2026-09-12 12:17:42

建议重绘标签和数据流：

- 三列标题为 `Observation`、`Response`、`Primitives`。
- 第 1 行：`Deep-K supply limit` → `Dual-slice supply + 2× core clock` → `Dual-read banks`。
- 第 2 行：`Shallow-K readout floor` → `Overlap compute / drain` → `Snapshot banks`。
- 第 2 行的时序重绘要明确标成两组：compute 属于组 `g`，drain 属于上一组 `g−1`，不要只画成无编号的重叠条。
- 第 3 行建议改成 `Short contiguous transfers`；已经连续的小段传输可以合并，乱地址 scattered writes 不能画成可直接合并。
- 底部成本条写明：`preadder PE: 121 → 103 LUT/PE; 1 DSP; 5 cycles`。

重绘时保留每行从瓶颈到对应解决办法再到硬件原语的单向箭头。面积数字只表示 LUT/PE 从 121 降到 103；DSP 数量和 5-cycle 延迟保持不变。`2× core clock` 只属于供数方案，不能挪到 PE 预加器图中。

## 图 2：system path

文件：`fig_system_concept_v2_hostops_2026-09-12_122811.png`（替换旧系统图）  
生成完成：2026-09-12 12:28:11

建议重绘标签和数据流：

- 离线链路：`Offline model trace` → `Compiler / descriptors + quant params` → `Functional / cycle sim`。
- 存储块：`DDR: instructions / weights / activations`。
- FPGA 运行链路标为 `GEMM segments`：`FPGA controller + DMA` → `Buffers` → `GEMM Pack2 array` → `Requant + activation` → `Segment outputs`。
- DDR 与 `Host boundary operations` 之间画实线双向数据通路，HostOp 包含 `norm / activation`、`selected softmax`、`rotary / rearrange`、`deformable`。
- 单独用虚线表示 `Host setup / configuration + load`，它只代表初始化和装载。
- 图例保留 `solid arrow = runtime data`、`dashed arrow = host setup`。

重绘时把 model compilation、FPGA segments 和 host boundary operations 分开。不要把图画成所有算子已经在 PL 上验证；建议保留 `path schematic; coverage spans FPGA segments and host boundary operations`，并在正文说明 compiler v7 仍有 norm/actv、部分 softmax、rotary、deformable 等 HostOp。整模型动作来自跨段执行后的输出，不要画成单一 token model。

## 图 3：PE 前后对比

文件：`fig_pe_preadder_concept_2026-09-12_122434.png`  
生成完成：2026-09-12 12:24:34

建议重绘标签和数据流：

- 输入为 signed8 `a, w0, w1`，打包式为 `Q=(w1+128)*65536+(w0+128)`。
- Before：`a × Q` 后，低 16 位走 `low16 − 128a`，高 16 位走 `high16 + P15 − 128a`，两路都进入已有累加器。
- After：DSP 内使用 27-bit preadder，`D=Q`、`A=−8388736`、`B=a`，形成 `P=a(Q−8388736)`；低 16 位直接提取，高 16 位经过 `P15` 校正。`P15` 的高位校正保留在 DSP 外部的 LUT 逻辑中，两路均删除外部 `−128a`。
- 底部说明：`one physical DSP multiplier, two logical products per core cycle; no dual-clock claim`。

重绘时必须保留两路 existing accumulator，不能把累加器误删。重点检查 `−8388736`、`P15`、`low16/high16` 和两个 `−128a` 的位置；After 图中外部 `−128a` 应删除，但高位 `P15` 校正仍保留在 DSP 内部逻辑中。`121 → 103 LUT/PE; 1 DSP; 5 cycles` 只表示 LUT 成本下降，不能画成 DSP 数量或周期数下降。
