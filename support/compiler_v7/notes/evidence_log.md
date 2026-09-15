# F4 修复轮证据账（compiler v7，2026-09-10）

每个数字都由主会话亲自从 JSON/原始输出核对（核数纪律）。服务器地址以
`<SERVER>` 占位（实际见 shell 历史）；服务器目录 /tmp/compiler_v7、/tmp/hw_v7。

## §1 前提的结构性证明（f4_pong_proof.py）

- 证明对象："两块暂存区覆盖写回存活期" ⇔ 对每个 y 链读者 r_j，它与下一个
  同奇偶写者 w 之间存在一条 op∈{4,5} 的发射 s（S3）。s 的发射门（S1a：
  ae_sched.sv:246-254 op=5 要 !wr_busy；S1b：T_EXEC op=4 要 !dma_busy，
  dma_busy=rd_busy|wr_busy，ae_dma.sv:310）保证 s 发射时写引擎已排空；
  调度器严格按流序（S2）保证 w 晚于 s 执行。
- v6 基线 build（96 列 build_s000_v6_96）：3,400 段全扫，**0 违反**；
  strict5（仅靠 LOAD 排空就安全、op=5-only 判据会误报的段）= 361 段
  6,884 对。108 列 build_s000_v6_full_fix1：3,442 段全扫，**0 违反**；
  strict5 = 368 段 6,872 对。
  - 门控谓词必须是 op∈{4,5}：只算 op=5 会把 361 段 LOAD 排空类误报成
    违反（它们本来就安全，f4_scan2 的危险对判据不含它们）。
- 168=168 同一性：f4_scan2 的危险段（STORE 悬置未被 op=4 清除、被同 y
  GEMM 命中）恰好就是 swin 相位一多迭代段，两个方向差集都是 0。
  - swin 相位一形态（is_swin_phase1）：LOAD* 头 + 严格 (COPY GEMM
    STORE)×nb + DONE，GEMM/STORE 共用唯一 y。v6 96 档 168 段形态分布：
    k=32×76 段(nb=96)、k=32 nb=48×8、k=4×60、k=8×22(nb=96)、k=8
    nb=64×2。
- 产物：results/f4_pong_96.json、f4_pong_108.json（修复前基线），
  f4_pong_v7_96.json、f4_pong_v7_full.json（修复后）。

## §2 VCD 实测锚点（f4_anchor.py，seg_0003，修复前单缓冲）

- 修复前 seg_0003（单缓冲）：n_iter=96、n_loads=3、y_base=24576、
  y_words=196、VCD 3,579MB。
  - **A_min=90,000ps=9 拍**（A_k = STORE k 末次 CTX 读 → STORE k+1 发射，
    全部 >0）：写引擎排空到下一条发射只有 9 拍——余量薄到只有结构性
    证明（门控顺序）吃得下，这是放弃余量口径、改用结构证明的实测依据。
    （时间戳单位 ps，clk 周期 10ns=10,000ps。）
  - **B_min=6,190,000ps=619 拍**（B_k = STORE k+1 发射 → GEMM k+2 首写
    回，全部 >0）。A∧B 链起来：乒乓下缓冲 k%2 的重写比它的末读晚
    ≥628 拍。
  - **race_true=95/95=100%**：单缓冲下每一对相邻迭代都咬上（GEMM k+1
    首写早于 STORE k 末读）——F4 竞态在电路上直接量到，与失配字节
    100%=golden 下一迭代值的静态证据互证。
- 工具坑（都已修进脚本注释）：
  - VCD 每拍两个时间戳（半拍），快照式逐时间戳求值把持续一拍的高电平
    记两次（首版 n_iter=192 假数）→ 只在本时间戳变更集含 clk→1 时求值。
  - seq 逐字解码必须跳过 GEMM 头后的 NCW 系数字（首版 y_base=410465
    假数）。
  - Verilator 别名信号共用 id 码，须按 码→[名字们] 多映射收集。
  - 空真防护：verdict 要求 B/R 非空。
- 修复后复跑（§6）见 results/f4_anchor_v7_seg0003.json。

## §3 修复实施（compiler.py _attn_swin 相位一）

- 改动点：`sreg = ctx_alloc('ss', T16*T)` → `sreg0/sreg1 = ctx_alloc
  ('ss0'), ctx_alloc('ss1')`；T%16 时两块都 _prezero；循环内
  `sreg = sreg0 if (pw0+pw)%2==0 else sreg1` 同时喂 _emit_gemm 与
  _emit_store；批尾 free 两块。相位二（preg/oreg/yreg/vreg）零改动。
- 本地权威副本：compiler/v7_2026-09-10_1258_f4_ybase_pong/sw/（v6 副本
  sha256 154bbf8f…起步，改后服务器侧 sha a3176ec7…）；
  服务器 /tmp/compiler_v7/sw/compiler.py。
- 编译（不带 --attn-calib，与 v6 轮同口径）：
  - 96 档：3,388 段 / 1,023,008 描述符 / 最大 SEQ 1,981 / 预估
    3,083.44ms@198.5MHz（v6：3,400 段 / 3,083.58ms，**−12 段、预估
    −0.005%**）。
  - 108 档：3,442 段 / 1,173,499 描述符 / 最大 SEQ 1,975 / 预估
    3,170.11ms（v6：3,442 段 / 3,169.77ms，段数不变）。
- −12 段的来源（diff_builds.py / diff_align.py 全量对齐定位）：仅 96
  档两个 swin 单元的**相位二**批重排（26 段→20 段 ×2）。相位一每段的
  差异恰为 op4 3→4（多一个预热零 LOAD）+ y 集合 {24576}→{24576,24772}
  （乒乓间隔恰 196 字）；strict5 段 361/6,884 逐数不变（非 swin 段零
  扰动）。108 档段数与 v6 完全一致，重排是 96 档批预算边缘效应，数值
  影响由 §4 的字节全等门兜底。
- 旧工具 verify_outputs.py 对 v6/v7 两代 build 都 FAIL（NCW 时代之前的
  逐字解码器，系数字被当假 STORE）——非本轮问题，不作为门。

## §4 全量图级对拍（g_v7_compare.py = v6 轮 g2_fix_compare 换 build 对）

- 口径：v6 build_s000_v6_full_fix1 vs v7 build_s000_v7_full，同解释器，
  图级对齐（输入按 crc32(name) 全局流 + 批S+C 切绝对单元；输出按
  (name, 窗/头后缀) 配对；同名段链式跑在共享 DDR 像上）。
- **31,991/31,991 输出条目字节全等，0 失配**（30,840/30,840 图哈希全等）。
- 裁判：18/18 golden==fast、18/18 交叉。
- verify 直查 2,811 键中 2,767 全等、44 非全等、0 错误——与 v6 轮同位置
  现象（v6：2,953 键中 2,400 全等、553 非全等），是链式重跑按名过滤的
  已知计数伪影（如 n_old=1 vs n_new=3 的 FFN 名），总账以全链哈希多集
  对比为准则 0 失配。本轮比 v6 轮干净一个量级（44 vs 553）。
- 权重 blob sha256 两侧相等（plan.json 记录）。
- 产物：results/g_v7_result.json。

## §5 危险对扫描（f4_scan2 判据，96 档 v7 build）

- **危险段 168→0，危险 GEMM-after-STORE 同址对 15,512→0**。
- 判据不变：STORE(y) 悬置未被 op=4 清除、被同 y GEMM 命中。

## §6 RTL 电路门（Verilator，hw v7 二进制 obj_f4/gate_v7，RTL 零改动）

- 本轮 RTL 一行未动（F4 是编译器侧修复）；电路门验证的是新指令流过
  同一套已验证电路。
- F4 批（乒乓相位一 + 重打包相位二 + nb=1 类）：
  seg_0003/0353/0354（k=32 乒乓，cycles 327,725，0 坏字节）、
  seg_0357/0372（重打包相位二，243,037，0）、seg_1218（4,722，0）。
  seg_0403（k=4，197,721，0）、seg_0597（k=8，216,437，0）。
- G3 回归批（v7 内容）：seg_1163/1200/1417/0713/1211/0607/1230 全
  PASS 0 坏字节（cycles 180,173 / 333,815 / 304,029 / 956,305 /
  166,811 / 118,741 / 231,541）。
- 合计 **15/15 段 0 失配字节**，覆盖 swin 相位一全部三种形态
  （k=32/4/8）+ 相位二重打包段 + G3 七段。
- 拍数代价：seg_0003 326,849→327,725（**+876 拍，+0.27%/段**，多一个
  预热零 LOAD 的 DMA 时长；段为 DMA 主导）。帧级预估 3,083.58→
  3,083.44ms（**−0.005%**，−12 段的段头开销盖过 168×2 个预热零）。

## §7 修复后锚点复跑（f4_anchor.py，v7 build seg_0003）

- n_iter=96、n_loads=4（3 数据 LOAD + 1 预热零 ✓）、y_base=24576
  （sreg0）、VCD 3,378MB、仿真 97.5s + 解析 289.5s。
- **A_min=9 拍、B_min=619 拍不变**——前提在修复后的电路上依然全链成立。
- race_true=47/94：94 对中偶数 k（同缓冲对，47 对）全部不咬；奇数 k
  （47 对）全部"重叠"——但奇数对是跨缓冲重叠（GEMM k+1 写 sreg0 vs
  STORE k 读 sreg1），正是乒乓要允许的并发。47=47 与奇偶分组严丝合缝，
  锚点的 y 区间过滤只能盯 sreg0，跨缓冲流量本就无害；同缓冲安全性由
  A∧B 全链 >0 直接给出（末读 < 下一发射 < 隔代首写）。
- 修复前对照（§2）：race_true=95/95=100% 全咬。**95/95 → 0/47（同缓冲
  口径）**。
- VCD 已删（3.4GB，服务器盘回 91%）。

## §8 复现命令

```bash
# 证明脚本（两个档，v6/v7 build 各跑一遍）
ssh <SERVER> "python3 /tmp/compiler_v6/f4_pong_proof.py /tmp/compiler_v7/build_s000_v7_96 96"
ssh <SERVER> "python3 /tmp/compiler_v6/f4_pong_proof.py /tmp/compiler_v7/build_s000_v7_full 108"

# 危险对扫描（判据=f4_scan2，路径已换成 v7）
ssh <SERVER> "python3 /tmp/hw_v7/f4_scan2_v7.py"

# 编译（不带 --attn-calib）
ssh <SERVER> "cd /tmp/compiler_v7 && python3 sw/compiler.py --trace /tmp/ae_hostdrv/trace_s000.json --manifest /tmp/pcw_rtn/manifest.json --w8 /tmp/pcw_rtn/w8_full --calib /tmp/pcw_rtn/hw_calib_table_pcw_v3.json --pcw-w8 /tmp/pcw_rtn/pcw_export --profile full96 --out build_s000_v7_96"
# （108 档把 full96 换成 full、out 换成 build_s000_v7_full）

# 全量对拍（plan→48 分片并行→merge1→verify 16 分片→merge2）
ssh <SERVER> "cd /tmp/compiler_v7 && python3 g_v7_compare.py plan && cd gtasks && split -n l/48 -d tasks.jsonl shard_ && cd .. && for f in gtasks/shard_*; do python3 g_v7_compare.py worker \$f >/dev/null 2>&1 & done; wait; python3 g_v7_compare.py merge1"

# RTL 电路门（Verilator，两批）
ssh <SERVER> "cd /tmp/hw_v7 && python gate_v7.py /tmp/compiler_v7/build_s000_v7_96 -t 300 seg_0003 seg_0353 seg_0354 seg_0357 seg_0372 seg_1218 seg_0403 seg_0597"
ssh <SERVER> "cd /tmp/hw_v7 && python gate_v7.py /tmp/compiler_v7/build_s000_v7_96 -t 500 seg_1163 seg_1200 seg_1417 seg_0713 seg_1211 seg_0607 seg_1230"

# VCD 锚点（修复前后各一次；跑完删 VCD）
ssh <SERVER> "cd /tmp/hw_v7 && python3 f4_anchor.py /tmp/compiler_v7/build_s000_v7_96 seg_0003 && rm -f run/seg_0003_f4/vcd_f4.vcd"
```
