from pathlib import Path
import datetime,json,csv,hashlib,html,shutil
P=Path(__file__).resolve().parents[1];now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
def doc(name,title,body):
 (P/name).write_text(f'# {title}\n\n生成时间：{now}。\n\n'+body,encoding='utf8')
doc('README.md','VLA-FPGA 论文修订二版', '''本版保留上一版，并新增五组对应 DiTPA 的图表。打开 `main.pdf` 阅读论文，打开 `2026-09-12_五组图表预览.html` 看图与中文说明。

已经完成：英文正文接入五组图表；前两组的真实参考图生成草案及矢量说明版；9 项架构能力对照；等工作量 RTL 微实验；新单时钟预加器引擎布线报告接收；统计脚本、原始日志、证据位置和实验任务书。

仍未完成：HoloBrain-0 GPU/FPGA 的同输入完整调用测量、固定轨迹重放、版本匹配的调用能效、突发写回与预加器累计集成。Cambricon-D 的全文未取得，表中 NR* 不能读成“不支持”。图 4、5 因而有明确缺项，当前稿件不是最终实验完成稿。

新收到的单时钟引擎：104066 LUT、169969 FF、768 DSP、0 BRAM；3.298 ns 时钟，WNS/WHS 为 +0.034/+0.014 ns。向量无注记功耗估计为 7.043 W。相对旧版路由结果，LUT 减少 12.1%，估计功耗减少 15.4%。这是历史版本比较，不是完整系统板级能耗实验。

复现论文：在本目录运行 `./build.ps1`。它只重建文稿和图表，不启动硬件实验，不干预 Vivado。新实验脚本在 `experiment_inputs/matched/`；服务器 g++-10 的重建脚本解决已知 conda C++ 头文件问题。运行范围及验收见新的 Claude 任务书。

`data/manifest.json` 保留原版冻结证据；`data/route_intake/manifest.json` 记录新报告；`data/figure_records.json` 统一结果字段，缺失值为 null；`data/capabilities.json` 保存逐项文献判断。第三方论文和用户参考图不作为项目开源资产再发布。''')
doc('2026-09-12_中文逐节说明.md','论文每节需要证明什么', '''1. Introduction：说明 VLA 的矩阵形状和输出节奏为何使阵列等待。三项贡献分别是编译执行流程、供数/读出/写回优化、精确低面积 PE。当前还有 HostOp，因此不写“所有算子已经在 FPGA 上运行”。
2. Background：图 1 分清模型输入、动作头迭代与控制器动作；图 2 用 C1–C3 把观察和机制对应起来。短 K 只占约 5.9% MAC，却占约 29.1% 模型周期；这意味着只统计乘加量会低估它的成本。
3. Compilation：说明模型如何变成权重、指令和宿主执行计划。列合并是有合法条件的候选变换，不能因为增加 N 的测试更快就宣布编译器已经实现。
4. Hardware：说明计算与读出怎样重叠、双切片怎样供数、突发怎样减少事务，以及预加器为什么减少 LUT。保留高位乘积借位校正，不能把两个乘积或两路累加器画丢。
5. Evaluation：先区分预测、RTL 仿真、布线估计和板级测量，再给性能比较与消融。新的相同行组微实验消除了旧结果启动开销口径不一的问题，但没有自动补齐完整系统测试。单时钟预加器的新路由结果已经加入。
6. Related Work：按具身/扩散与通用 FPGA 分组。支持、部分支持、未报告、不适用分开。Quasar-ViT 把部分算子放在 ARM；FINN 当前公开仓库和 2017 论文原型也需要分开描述。
7. Discussion：列出哪些结论现在能成立，哪些仍要实验。单时钟面积/估计功耗下降已可报告；双倍时钟预加器当前时序不闭合；成功率表继续空白。

这版图 4 的空项意味着“尚无可比测量”，不是零性能。图 5 的下半部分也没有伪造能效柱。全文目前 14 页，属于便于检查证据的工作稿；压缩到目标会议页数应在数据与图形定稿后完成。''')
doc('2026-09-12_图表任务书.md','五组图表的标签与 Visio 重绘要求', '''所有硬件原图按个人绘图规则：模块、连线和实心箭头 2.25 pt；英文 Arial Bold。白底、少量淡色、直角布线。按照最终双栏宽度检查，主要文字至少 7 pt。这是个人偏好，不是会议强制标准。

## 第一组：模型与执行层次

文件：`figures/core1_model.svg/pdf`；视觉草案：`figures/concepts/model_draft.png`。
标签：RGB observation、Depth、Instruction、RGB Swin、Depth Swin、BERT、Spatial / multimodal features、Robot state、Action decoder、Predicted sequence、Controller。
上面是数据流，下面是一次调用内的 10 步去噪与 6 个 decoder block。执行 chunk 最多 32 个动作，不等于输出序列一定只有 32 个动作，也不等于调用频率可乘以 32。
模型与运行设置来源：`data/model.config.json`、`algo/w8a8_success/2026-09-09_140354/runtime_check.json` 和同目录实验入口。模型结构本身不证明所有模块已在 FPGA 上。
草案的修正要求：生成工具把上图控制器和动作序列顺序画反，并把深度画成灰度 RGB；不得把这些当真实深度数据。以矢量版的数据流为准，Visio 中画实际输入框，不合成深度照片。下图要明确 Block 6 → Upsample → Scheduler，调度更新返回下一迭代，只有最终预测交给控制器。循环反馈线不是模型特征重新编码。

## 第二组：C1–C3 对应图

文件：`figures/core2_codesign.svg/pdf`；视觉草案：`figures/concepts/codesign_draft.png`。
三行：Observation、Compilation / scheduling、Hardware。三列：矩阵形状、写事务、PE 校正。
第一行的 5.9%/29.1%、99.5%、121/103 都由脚本和冻结数据生成。不要用图片生成工具重画数值柱。第二行要给尚未实现的列合并标 pending。第三行依次画双切片与快照读出、FIFO 与 AXI 三通道、DSP48E2 预加器与两路累加器。
草案仅供布局参考：C1 的 slice0/1 时间轴不能误画成两个彼此独立的阵列；C3 的 +P[15] 只接高位乘积，低位乘积直接进自己的累加器；权重打包不是近似算法。统计版保留正确文字和真实数据，视觉草案保留更丰富的阵列/事务小图，Visio 定稿应合并两者。

## 第三组：能力对照

`tables/capabilities.tex` 及 `data/capabilities.json`。不是性能排名。每项结论的原文页码或官方代码位置见 `2026-09-12_相关工作逐项证据.md`。NR* 与 NR 不能合并；前者是全文访问未完成。

## 第四组：性能与功耗

`figures/core4_performance.pdf` 预留同模型比较；底部历史模型只画 GEMM 周期。`core4_power_boundary.pdf` 画两个版本的引擎功耗估计，不能拿这两个 W 数字直接得出完整调用 calls/J。阶段时长模板在 `tables/stage_times_template.csv`。

## 第五组：累计消融

`figures/core5_ablation.pdf`。目前可比的是相同描述符的 RTL 周期。带斜线的 2× 核心系列不代表当前时序失败的预加器版本已经可实现。突发写回、预加器和列合并需完成对应集成才能加柱。能效缺项保持空白。

## 图像工具记录

本轮先尝试网页版 GPT 上传用户给的真实图 1、2。点击上传后没有可用 file chooser，并出现超时；此前同通道曾返回 Not allowed。没有绕过限制。按照用户批准的备用方案，内置图像工具直接读取本地 DiTPA 参考图，生成了两个草案。草案没有冒充实测统计图，也没有冒充已核对完成的电路图。''')
doc('2026-09-12_Claude_experiments_r2.md','交给 Claude 的补实验任务', '''请在 `E:/GPU ARCH/vector_core_sim` 继续本轮论文实验。保留 `paper/2026-09-12_vla_fpga` 和 r2 冻结数据；新结果放有年月日时分秒的新目录。不要改动或重启正在运行的 Vivado 实现。每一轮编译加运行控制在 10 分钟内，RTL 优先 Verilator。不要使用 Evo-1 的 V100 数据，不把软件 fake-quant 延迟写成 GPU INT8 性能，不填成功率。

### P0-1：补齐同模型 GPU 延迟与功率

目的：为第 4 组完整策略调用提供真正同模型、同输入基线。服务器 `ssh nc23@101.6.64.77`；四卡目前有其他用户常驻进程，不要停止它们或把混合功耗归到本模型。需要空闲独占卡才能收功率。
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

最终请输出：可直接作图的 JSON/CSV、原始结果路径、命令和环境、每项完成/未完成原因。成功率继续为空。不要修改仓库可见性，不对外发布。''')
doc('2026-09-12_证据索引_r2.md','新增图表与证据', '''|组|主张/用途|原始证据与状态|
|---|---|---|
|1|模型层次、迭代与动作执行分开|model.config.json；runtime_check.json；run_pairs.py；scene_head.png|
|2 C1|短 K 的计算量小但周期占比高|冻结 data/arch.json k_dist；预测|
|2 C2|绝大多数输出字节在长连续区间|data/arch.json write_channel；静态 trace|
|2 C3|外部校正重复占 LUT|data/pe.json 及 v9 原始综合报告|
|3|能力差异而非跨模型速度排名|data/capabilities.json；逐项定位 Markdown；Crossref 元数据|
|4 性能|同模型完整调用比较|缺失，HoloBrain GPU 未测；旧模型 GEMM 预测单独画|
|4 功耗|单时钟预加器引擎的新估计功耗|data/route_intake/；7.043 W 路由估计；非板级|
|5|同描述符累计周期变化|data/matched/*/run.log，16 项通过；两组、4 物理列|
|5 能效|各配置自己的功耗和调用时间|缺失；未使用旧功耗或面积比例补数|

新微实验第二次编译及运行完成：2026-09-12 13:32:59。首次编译记录保留，它因服务器 conda 头文件问题失败；系统 g++-10 重建后通过。新路由功耗报告完成：2026-09-12 13:38:06，时序摘要完成：13:37:16。文件路径均保留源信息和冻结副本，论文图表只读副本。

新微实验的 input_definition_sha256 是输入生成程序及 seed 的定义哈希，不冒充导出张量哈希；tensor input_sha256 仍为 null。GPU 与完整策略调用的 checkpoint 哈希也待实际导出。''')
stage=[{'platform':p,'vision_s':None,'language_interaction_s':None,'action_s':None,'full_call_s':None,'overlap_note':None} for p in ['HoloBrain-0 GPU','FPGA baseline','FPGA optimized']]
with (P/'tables/stage_times_template.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.DictWriter(f,fieldnames=stage[0].keys());w.writeheader();w.writerows(stage)
items=[('第一组：模型与执行层次','core1_model.png','从左向右看模型输入到动作预测，再看下面的一次调用。32 个动作是执行 chunk，不是调用频率倍数。'),('第二组：观察、编译与硬件','core2_codesign.png','每列自上而下读：观察对应哪种编译/调度动作，又需要哪块硬件。小统计图来自真实记录。'),('第四组：完整性能比较的缺项','core4_performance.png','前两行尚未测量。第三行只比较旧模型的 GEMM 周期，不能解释成整模型延迟。'),('第四组：当前可用引擎功耗','core4_power_boundary.png','每条长度是一个版本的引擎估计功耗。新版比旧版少约 15.4%，不等于整板能耗下降同样比例。'),('第五组：相同工作量的 RTL 消融','core5_ablation.png','高柱表示同一描述符需要的周期更少。斜线柱的双倍时钟尚未形成可实现性能结论；能效缺数。')]
content=f'<!doctype html><html lang="zh"><meta charset="utf-8"><title>VLA-FPGA 五组图表修订</title><style>body{{font:16px/1.7 system-ui;max-width:1160px;margin:35px auto;padding:0 24px;color:#18212b}}h1{{font-size:28px}}h2{{margin-top:45px}}img{{max-width:100%;border:1px solid #ddd}}.status{{padding:15px;background:#fff3dc}}table{{border-collapse:collapse;font-size:12px}}td,th{{border:1px solid #bbb;padding:7px;vertical-align:top}}a{{color:#12649b}}</style><h1>VLA-FPGA 五组核心图表修订</h1><p>生成时间：{now}</p><p class="status">图表结构、文献对照和同组数 RTL 微实验已加入。完整 GPU/FPGA 调用比较、轨迹重放和累计能效仍缺数据。</p><p><a href="main.pdf">英文论文 PDF</a> · <a href="2026-09-12_Claude_experiments_r2.md">Claude 实验任务书</a> · <a href="2026-09-12_图表任务书.md">Visio 标签与重绘说明</a></p>'
for title,file,desc in items[:2]:content+=f'<h2>{title}</h2><p>{desc}</p><img src="figures/{file}">'
content+='<h2>前两组：按真实 DiTPA 图片生成的视觉草案</h2><p>草案供 Visio 布局参考，不代替已核对的数据和连线。已发现的箭头、深度画面和借位分支问题详见重绘说明。</p><img src="figures/concepts/model_draft.png"><img src="figures/concepts/codesign_draft.png">'
caps=json.loads((P/'data/capabilities.json').read_text())
content+='<h2>第三组：相关架构能力对照</h2><p>S 支持；P 部分支持；NR 所查来源未报告；N/A 不适用；NR* 全文未取得。<a href="2026-09-12_相关工作逐项证据.md">逐项证据位置</a></p><table><tr><th>架构</th>'+''.join('<th>'+html.escape(s)+'</th>' for s in ['目标范围','器件','全模型/主机','跨迭代复用','形状/重叠','低精度/打包','公开材料'])+'</tr>'
for r in caps['rows']:content+='<tr><td>'+r['name']+'</td>'+''.join('<td>'+html.escape(c['judgment'])+'</td>' for c in r['cells'].values())+'</tr>'
content+='</table>'
for title,file,desc in items[2:]:content+=f'<h2>{title}</h2><p>{desc}</p><img src="figures/{file}">'
(P/'2026-09-12_五组图表预览.html').write_text(content+'</html>',encoding='utf8')
g=json.loads((P/'data/gpu_rough.json').read_text());gd=json.loads((P/'data/gpu_derived.json').read_text())
update=f'''\n\n## 本轮最后补充（{now}）\n\n全宽原 PE 和预加器 PE 各 16 项对拍通过；加上前期 4 列 16 项，共 48 项。主消融图改用 48 物理列、768 DSP、M=32。短 K 宽输出为 399→228 拍，减少 42.9%；深 K 为 4329→2205 拍，减少 49.1%。单独替换预加器时，这 16 项周期完全不变。全宽结果位于 data/matched48 与 data/matched48_pa，验证汇总在 data/matched_audit.json。突发写回仍未集成到这份累计测试。\n\n用户随后明确允许共享 GPU 粗测。GPU1 保留他人进程，运行 HoloBrain-0 FP32 的 s000 真实观测，共 12 次前向，均值 {g['mean_latency_s']*1000:.1f} ms，范围 {g['min_latency_s']*1000:.1f}–{g['max_latency_s']*1000:.1f} ms。测试期 GPU 总功率均值 {g['mean_shared_gpu_power_w']:.1f} W，含其他进程；不归为本模型独占功耗。该前向包含 10 步去噪和内部预处理，不含外部观测处理与动作后处理。s000 是已有 episode_0000000.hdf5 t=40，并非 place_empty_cup 场景。\n\n模型配置 SHA-256 与论文快照一致，输入/权重哈希保存在 data/gpu_rough.json。当前输出 shape 为 [1,64,14,8]，因此 64 步预测序列与控制器执行 chunk=32 必须分开。阶段计时是独立的 3 次带同步测量：视觉 {gd['stage_ms']['Visual']:.1f} ms、语言/交互 {gd['stage_ms']['Language / interaction']:.1f} ms、动作 {gd['stage_ms']['Action']:.1f} ms，动作阶段约占 {gd['action_stage_fraction']*100:.1f}%。不是三个任务。\n\n本轮粗测已完成，不必因没有独占卡停止继续分析。若后续要形成严格的跨平台能效结论，再补齐匹配输入、完整执行范围和可归因功耗。现在仍不计算 GPU/FPGA 速度比或 calls/J。\n'''
for name in ['README.md','2026-09-12_中文逐节说明.md','2026-09-12_图表任务书.md','2026-09-12_证据索引_r2.md','2026-09-12_Claude_experiments_r2.md']:
 path=P/name;body=path.read_text(encoding='utf8')
 body=body.replace('需要空闲独占卡才能收功率。','用户已允许共享 GPU 粗测；记录占用和功率范围，不阻塞粗测。严格归因功率另需独占条件。')
 body=body.replace('缺失，HoloBrain GPU 未测；旧模型 GEMM 预测单独画','已有共享 GPU s000 前向粗测；完整同输入调用仍缺失，旧模型 GEMM 预测单独画')
 body=body.replace('data/matched/*/run.log，16 项通过；两组、4 物理列','data/matched48/*/run.log 与 data/matched48_pa/*/run.log，全宽原/新 PE 各 16 项通过')
 path.write_text(body+update,encoding='utf8')
for old,new in [('2026-09-12_Claude_experiments.md','2026-09-12_Claude_experiments_r2.md'),('2026-09-12_证据索引.md','2026-09-12_证据索引_r2.md')]:doc(old,'本轮文档入口',f'本轮请阅读 [{new}]({new})。上一版完整材料保留在相邻的 2026-09-12_vla_fpga 目录。')
path=P/'2026-09-12_五组图表预览.html';h=path.read_text(encoding='utf8').replace('前两行尚未测量。第三行只比较旧模型的 GEMM 周期，不能解释成整模型延迟。','前两行是共享 GPU 的前向粗测与独立阶段计时。第三行是旧 FPGA 模型的 GEMM 周期；范围不同，不计算跨平台加速倍数。')
h=h.replace('完整 GPU/FPGA 调用比较、轨迹重放和累计能效仍缺数据。',f'GPU 共享卡前向粗测已补充（{g["mean_latency_s"]*1000:.1f} ms）；完整同输入调用比较、轨迹重放和累计能效仍缺数据。')
h=h.replace('</html>','<h2>共享 GPU 原始功率记录</h2><p>这是总板卡传感器功率，含其他进程。不能直接作为本模型的独占能耗。</p><img src="figures/gpu_shared_power.png"></html>');path.write_text(h,encoding='utf8')
print('Delivery documents written',now)
