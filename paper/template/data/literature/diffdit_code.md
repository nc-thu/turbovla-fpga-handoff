# Diff-DiT: Temporal Differential Accelerator for Low-bit Diffusion Transformers on FPGA

Diff-DiT is an algorithm-hardware co-design accelerator for diffusion transformers using temporal differential computation.

## Chanllenges and contributions

![Alt text](assets/challenges_contributions.jpg) Chanllenges and contributions


## Speedups and energy efficiency improvement

![Alt text](assets/speedup.jpg) Speedups and energy efficiency improvement

## Code Structure

```
./src
├── TOP.h ---> Top-level header file
├── TOP.cpp ---> Top-level implementation
│ ├── HalfCondition/condition_dataflow ---> Class condition calculation unit
│ │ ├── silu ---> SiLU
│ │ └── PE_wrapper_no_dsp_packing ---> Systolic array for class condition
│ └── matmul/matmul_kernel ---> Core functional unit
│   ├── load_sfu_mask ---> Load SFU mask for the diff-sfu calculations
│   ├── load_quant_factor ---> Load scale factor and zero point
│   ├── input_from_axi ---> Load activation and weight via AXI
│   ├── PE_input ---> Reorganize input data for systolic arrays
│   ├── PE_tile ---> Main code of systolic array
│   ├── PE_output ---> Reorganize output data from systolic arrays
│   ├── sfu ---> Special function unit
│   ├── store_sfu_mask ---> Store SFU mask for the diff-sfu calculations of next time-step
│   └── output_to_axi ---> Store activation output via AXI
├── Adder_rtl.cpp ---> C description of accumulator
├── AMA_rtl.cpp ---> C description of Add-Multiply-Add
├── common.h ---> Common definitions
├── config.h ---> Configuration parameters
├── test.cpp ---> Test implementation
└── test.h ---> Test header file
```

## Mode Introduction

| Mode | Description |
|------|-------------|
| 0 | HC1 + LN + Proj0 |
| 1 | Proj1 |
| 2 | HC0 + LN + Proj2 + GELU |
| 3 | Proj3 + Res |
| 4 | QK + SoftMax |
| 5 | SV |
| 6 | HC0 |
| 7 | HC1 + LN + Diff-Proj0 |
| 8 | Diff-Proj1 |
| 9 | HC0 + LN + Diff-Proj2 + Diff-GELU |
| 10 | Diff-Proj3 + Res |
| 11 | Diff-QK + Diff-SoftMax |
| 12 | Diff-SV |

## Citation

```bibtex
@inproceedings{tang2025diff,
  title={Diff-DiT: Temporal Differential Accelerator for Low-bit Diffusion Transformers on FPGA},
  author={Tang, Shidi and Zheng, Pengwei and Chen, Ruiqi and Lv, Yuxuan and Da Silva, Bruno and Ling, Ming},
  booktitle={2025 IEEE/ACM International Conference On Computer Aided Design (ICCAD)},
  pages={1--9},
  year={2025},
  organization={IEEE}
}
```