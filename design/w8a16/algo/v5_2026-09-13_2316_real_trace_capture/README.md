# TurboVLA 真实输入采集

完成时刻：2026-09-13 23:21:24。

本目录保存一次 `libero_spatial` Spatial task 0 的真实 TurboVLA forward 采集脚本。采集在服务器 GPU 3 上完成，使用 seed=7、两路 256×256 图像、instruction 和 8 维状态，输出 12×7 action chunk。模块 hook 负责边界记账，TorchDispatch 负责发现动态 BMM 和低层事件；大 payload 放在对应 `data/v8_2026-09-13_231621/`，本目录不复制旧权重。

这次采集用于顶层活动回放，不代表完整 LIBERO 成功率或板上推理时延。
