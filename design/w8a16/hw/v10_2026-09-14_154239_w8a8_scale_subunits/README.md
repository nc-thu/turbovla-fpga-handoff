# W8A8 scale 子单元

生成时间：2026-09-14 16:01:00。

这里不是完整 16×48 阵列，而是 4 组 × 32 个 INT8 乘法的代表性子单元。A、B、C 对应软件实验的三个边界。A 的 FP32 scale 合并没有进入 RTL，所以硬件表里的 A 只是共同的 INT32 部分和。

在安装了 Vivado 2021.2 的 Windows 主机上运行：

```powershell
cd 'E:\GPU ARCH\vector_core_sim\turbovla_w8a16\hw\v10_2026-09-14_154239_w8a8_scale_subunits\synth'
.\run_scale_subunits.ps1
```

脚本会把工程临时复制到没有空格的路径，再运行 `run_scale_subunits.tcl`。结果回收到 `synth/runs/`。当前结果是 OOC `synth_design + opt_design`，不是布局布线和功耗结果。
