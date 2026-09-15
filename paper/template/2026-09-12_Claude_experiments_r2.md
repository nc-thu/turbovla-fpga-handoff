# 交给 Claude 的补实验任务

生成时间：2026-09-12 14:04:19。

请在 `E:/GPU ARCH/vector_core_sim` 继续本轮论文实验。保留 `paper/2026-09-12_vla_fpga` 和 r2 冻结数据；新结果放有年月日时分秒的新目录。不要改动或重启正在运行的 Vivado 实现。每一轮编译加运行控制在 10 分钟内，RTL 优先 Verilator。不要使用 Evo-1 的 V100 数据，不把软件 fake-quant 延迟写成 GPU INT8 性能，不填成功率。

### P0-1：补齐同模型 GPU 延迟与功率

目的：为第 4 组完整策略调用提供真正同模型、同输入基线。服务器 `ssh nc23@101.6.64.77`；四卡目前有其他用户常驻进程，不要停止它们或把混合功耗归到本模型。用户已允许共享 GPU 粗测；记录占用和功率范围，不阻塞粗测。严格归因功率另需独占条件。
模型入口：`/home/nc23/workspace/holobrain/ckpt/HoloBrain_v0.0_GD/post_training_robotwin`。复用 `algo/w8a8_success/2026-09-09_140354/run_pairs.py` 的 pipeline 构造、观测预处理和推理调用，任务为 `place_empty_cup`、10 denoising steps、action_chunk=32。实际 checkpoint、模型配置、输入张量都计算 SHA-256。
提供了通用采样器 `scripts/measure_gpu_callable.py`。先编写 `hb_measure_adapter.py` 的 `make_call()`，返回 `(callable, metadata)`。callable 执行一次真实策略调用；metadata 必须包含模型和输入哈希、量化语义及计时边界。不能用空函数替代模型。
运行命令：`CUDA_VISIBLE_DEVICES=<独占卡> <已有环境python> measure_gpu_callable.py --factory hb_measure_adapter:make_call --nvml-index <物理卡号> --warmup 5 --repeat 20 --out gpu_calls.json`。不要为运行脚本擅自更换模型环境。
输出：原始 NVML 时间戳/功率、每次调用耗时和 GPU device joule、GPU/驱动/框架版本、输入和 checkpoint 哈希。抽查 CUDA 同步和功率采样覆盖。此脚本只有 GPU 设备功率；完整平台能效另需主机/内存数据。验收：20 次真实调用，采样覆盖完整，不存在其他进程；超过十分钟则减少重复数并注明。

### P0-2：固定轨迹重放和阶段时长

目的：区别一次调用、轨迹推理、闭环任务时间。将已有参考轨迹的观测按原顺序导出为不可变 manifest，逐观测记录输入哈希；严禁把一个观测复制成十个不同任务。复用 P0-1 adapter，按 manifest 逐次调用；记录 vision、language/interaction、action 三段，说明它们是否相互重叠。输出 `trajectory_manifest.json`、`trajectory_calls.jsonl`、`stage_times.csv`。验收：轨迹推理时间等于各次调用实测时间之和；不包括仿真器或机械运动耗时；阶段不重叠时才求和。

### P0-3：架构模型与当前输入版本匹配

输入：`hb_fpga_impl/12_actv/a3/build_a3/segments`、`arch/v8_2026-09-11_2315_gemm_util_design/util_decomp.py`、当前 compiler v7 HostOp 计划。先审计现有 trace 对应 checkpoint/输入；不能直接给旧 trace 补上新配置哈希。复制脚本到新目录，输出每段原始 cycles 与阶段归属，分别列 GEMM、搬运、HostOp。频率来自对应已闭合报告；2× 时序失败版本仅作独立理想上界。验收：模型调用范围明确，MAC 数可回查；没有用 GEMM 时间冒充完整策略调用。

### P0-4：完整累计消融

输入：r2 `experiment_inputs/matched/`，已有 4 列、M=32 的 16 项通过结果在 `data/matched/`。每轮使用相同 M、N、K、seed、量化、内存延迟、行组数及开始/结束事件。该测试避开旧基线多组事件丢失，不能用它宣布多组问题已修复。
运行：`bash run.sh`；如遇 conda timespec_get 错误，用 `bash rebuild_system_cxx.sh`，只在该轮 build 目录使用 g++-10。先检查全部输出与黄金数组逐字节一致，再取周期。当前有效 MAC 应用 M×N_loc×K，不能盲用硬件计数器对窄输出多计的 lane。
按顺序增加：原 Pack2 → overlap+dual readout → 双切片/可实现核心时钟 → burst writeback → preadder PE。将已有突发写回段级实现接进同一 harness，加入反压、4KB/突发边界和连续地址场景。预加器保持相同语义；先完成全宽正确性与时序，不预设加速。每个开关保存 RTL hash、描述符、结果 hash、interface/core cycles 和运行日志。
输出 `matched_ablation.json`、全部原始日志、功耗报告对应表。验收：相同工作量、输出一致、时间边界一致；未过时序的配置不进入可实现性能柱。合法列合并等价验证完成后才增加系列。

### P0-5：接收匹配版本的实现与功耗

新收到的单时钟预加器已冻结在 `data/route_intake/`，7.043 W、104066 LUT，3.298 ns，WNS +0.034、WHS +0.014。不要重复启动它。继续读取现有实现的完成结果；每组接收 util、timing、power、XDC、RTL revision、活动注记和哈希。2× preadder 当前综合 WNS −0.216 ns，不把该时钟当作已达到的频率。
验收：每个配置有自己的报告，标明 vectorless/SAIF、OOC/完整系统、综合/路由/板级。仅靠 LUT 降幅、GPU TDP 或旧版 8.321 W 不允许补全能效。调用能耗需要和同版本有效活动时间匹配；可以只完成引擎估计，不强行出跨平台 calls/J。

### P1：边界/敏感性

对短 K、深 K、窄 N、写敏感负载，改变 1–2 个真实可实现参数，分别记录服务等待与总周期。先缩小代表测试确保十分钟内，避免启动大批长实验。保持旧结果不变，把新表格合并进 `data/figure_records.json` 前先检查哈希、版本与功耗边界。

最终请输出：可直接作图的 JSON/CSV、原始结果路径、命令和环境、每项完成/未完成原因。成功率继续为空。不要修改仓库可见性，不对外发布。

## 本轮最后补充（2026-09-12 14:04:19）

全宽原 PE 和预加器 PE 各 16 项对拍通过；加上前期 4 列 16 项，共 48 项。主消融图改用 48 物理列、768 DSP、M=32。短 K 宽输出为 399→228 拍，减少 42.9%；深 K 为 4329→2205 拍，减少 49.1%。单独替换预加器时，这 16 项周期完全不变。全宽结果位于 data/matched48 与 data/matched48_pa，验证汇总在 data/matched_audit.json。突发写回仍未集成到这份累计测试。

用户随后明确允许共享 GPU 粗测。GPU1 保留他人进程，运行 HoloBrain-0 FP32 的 s000 真实观测，共 12 次前向，均值 404.9 ms，范围 402.1–419.0 ms。测试期 GPU 总功率均值 99.7 W，含其他进程；不归为本模型独占功耗。该前向包含 10 步去噪和内部预处理，不含外部观测处理与动作后处理。s000 是已有 episode_0000000.hdf5 t=40，并非 place_empty_cup 场景。

模型配置 SHA-256 与论文快照一致，输入/权重哈希保存在 data/gpu_rough.json。当前输出 shape 为 [1,64,14,8]，因此 64 步预测序列与控制器执行 chunk=32 必须分开。阶段计时是独立的 3 次带同步测量：视觉 33.0 ms、语言/交互 60.4 ms、动作 312.8 ms，动作阶段约占 76.5%。不是三个任务。

本轮粗测已完成，不必因没有独占卡停止继续分析。若后续要形成严格的跨平台能效结论，再补齐匹配输入、完整执行范围和可归因功耗。现在仍不计算 GPU/FPGA 速度比或 calls/J。
