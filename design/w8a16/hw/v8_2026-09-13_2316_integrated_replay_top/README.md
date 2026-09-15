# TurboVLA 集成 replay top

完成时刻：2026-09-14 00:46:32。

`tvla_replay_top.sv` 是本轮新顶层。它保留 64-bit command，使用 512-bit descriptor FIFO，连接 16×48 W8A16 阵列、行为级 AUX 事件、结果读出和 activity counter。full replay 以一个控制时钟接收一条 descriptor，再把该 descriptor 的事件周期加入计数器；这让完整 forward 不需要执行上亿个空时钟。阵列算术仍由代表性 tile 做逐拍验证。

Vivado 三个 OOC 配置均通过 4.000 ns 目标；没有做 place/route、板级约束或 bitstream。
