# TurboVLA complete-model compiler v4

This version reads the captured TurboVLA dispatch stream and emits one
descriptor plus one 64-bit command word for every dispatch event.  It does
not hide unsupported work in a zero-cost bucket.  Each event is assigned to
an explicit execution unit:

* `pack2_gemm` / `pack2_bmm` for W8A8 matrix work;
* `fp16_vector` for LayerNorm, Softmax, GELU, ReLU, tanh, exp, div, add,
  mul, clamp and reductions;
* `conv_im2col`, `embedding_posenc`, `layout_engine`, `mask_engine` and
  `memory_engine` for their corresponding data paths;
* `attention_controller` for attention operations that require both operands;
* `meta_engine` for ordering, identity and control events.

The compiler records conservative cycle and traffic fields in each descriptor.
The v4 descriptor also carries `numeric_format`, `fp16_mode`, and numeric
scale/bias indices in a 512-bit sideband.  The sideband is emitted as
eight little-endian 64-bit words, while the command word remains 64 bits.
The summary is still a cycle-model result; it is not a claim that all
numerical functions have already been proven against the trained policy.
The RTL top now has a sideband FIFO and a project-mode vendor-FP16 path, but
calibration loading and board-level DDR timing remain separate integration
steps.

Run:

```powershell
python compile_complete_model.py `
  --capture ..\..\data\2026-09-14_115230 `
  --output ..\..\data\2026-09-16_060349_fp16_memory_complete\compiled_v4_sideband
```

The output schema is `tvla_w8a8_pack2.complete_model.v4`; `unknown_event_count`
must remain zero and `gemm_compute_cycles` is the denominator for the GEMM
utilization metric.
