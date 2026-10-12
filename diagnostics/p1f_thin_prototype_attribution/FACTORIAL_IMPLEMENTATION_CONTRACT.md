> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# P1F source × lattice implementation contract

Frozen after `artifacts/replication/gate.json` set `allow_factorial=true` and before architecture implementation or training. The contract is based on the pinned source at commit `b454f423600f99d41730bd75a7a26b491187de36`.

## Audited clean graph

The native YOLO11n-seg `Segment.proto` source is **layer 16**, the neck P3 tensor, with shape `B×64×80×80` and stride 8 at input 640. Native `Proto` is `Conv3×3(64→64) → ConvTranspose2×2,s2(64→64) → Conv3×3(64→64) → Conv1×1(64→32)`, producing `B×32×160×160`. The clean graph has no neck P2 output. The only reusable stride-4 tensor with the same 64 channels is **backbone layer 2**, shape `B×64×160×160`; it is therefore the frozen S1 source.

Layer 2 has a longest local theoretical receptive field of 23×23 input pixels under the scaled `n` graph. Layer 16 contains a top-down path through layer-10 PSA attention and therefore has global theoretical support, plus local P3 paths. S1 consequently changes semantic depth and receptive field as well as source stride. This residual source confound is explicit and forbids a claim that S1 isolates spatial sampling alone.

## Orthogonalized generator

Every learned generator uses the same native `Proto` topology. A parameter-free bilinear pre-resample maps the selected source to half the requested output lattice:

- R0 maps source to 80×80, then native `Proto` produces 160×160.
- R1 maps source to 160×160, then native `Proto` produces 320×320.

Both sources have 64 channels, so there is no learned adapter. K remains 32. Detection inputs remain exactly layers `[16,19,22]`; the added source input is used only by `proto`, so box/class/coefficient topology, TAL, loss family, NMS, and thresholds stay unchanged.

| Variant | Source | Source shape | Fixed pre-resample | Learned Proto | Output | Internal width | Learned generator params | Learned generator FLOPs |
|---|---|---:|---|---|---:|---:|---:|---:|
| F00 | layer16 neck P3 | 64×80×80, s8 | identity | native 4 operators | 32×160×160 | 64 | 92,544 | 2.6738688 G |
| F10 | layer2 backbone P2 | 64×160×160, s4 | bilinear 160→80 | native 4 operators | 32×160×160 | 64 | 92,544 | 2.6738688 G |
| F01 | layer16 neck P3 | 64×80×80, s8 | bilinear 80→160 | native 4 operators | 32×320×320 | 64 | 92,544 | 10.6954752 G |
| F11 | layer2 backbone P2 | 64×160×160, s4 | identity | native 4 operators | 32×320×320 | 64 | 92,544 | 10.6954752 G |
| C-UP | layer16 neck P3 | 64×80×80, s8 | identity | native generator to 160 | fixed prototype interpolation 160→320 | 64 | 92,544 | 2.6738688 G plus interpolation |
| C-COMP | layer16 neck P3 | 64×80×80, s8 | identity | native topology, widened | 32×160×160 | 136 | 323,880 | 10.6954752 G |

FLOPs count multiply and add separately and cover the learned prototype generator. Fixed bilinear interpolation and coefficient-by-prototype assembly are reported separately by the profiler. Width 136 makes C-COMP's learned generator FLOPs exactly equal to the R1 generator under this convention (0.00% gap), satisfying the registered ±5% requirement. C-COMP matches compute, not parameter count; it adds 231,336 learned generator parameters. All other variants have identical learned parameter count.

## Attribution semantics

- F10 versus F00 measures source content after both are restricted to the same 80×80 generator input. Downsampling prevents the fine source from retaining its full spatial Nyquist range; this is necessary to keep R fixed and is reported as a limitation.
- F01 versus F00 moves the same native source through learned convolutions at the denser lattice. Its input is interpolated, so it introduces no new source information.
- F11 contains both the fine source and dense learned lattice.
- C-UP moves only the final native learned basis to 320×320. If it matches F01/F11, the effect is rasterization/interpolation rather than learned dense representation.
- C-COMP retains the native 160×160 lattice while matching learned generator FLOPs. If it matches the high-resolution branch, the result is generic capacity/compute.

## Initialization and mandatory checks

All six seed42 runs start from the same official `yolo11n-seg.pt` initialization (SHA256 `55ed65c56c91713d23e8402371c6c49a6fd84f257f7dce452e8d70e41dcbe152`) and the frozen P1D 60-epoch schedule. Matching tensors transfer by name and shape. F00 must have exact state/output/loss parity with the clean native graph before training. F10/F01/F11/C-UP reuse native Proto weights. C-COMP's widened Proto cannot shape-transfer and uses the single preregistered seed42 initialization; this initialization difference is retained as a capacity-control limitation.

Before training, an audit must write resolved YAML, full-model params/FLOPs, tensor shapes, transfer counts, F00 output/loss/gradient parity, C-UP interpolation identity, finite gradients for every variant, and a source-code snapshot. Any F00 mismatch or shape/gradient failure blocks all training. Profiling may refine full-model totals in an audit appendix but may not change variants, width 136, gates, or interpretation.

## Pre-training audit appendix

The completed audit at `artifacts/runs/20260922T103802_112527_factorial_audit` passed all registered checks. F00 state tensors, inference outputs, official loss values, and CPU loss gradients were bitwise identical to the native graph (`max_gradient_delta=0`). CPU was used for the strict backward comparison because CUDA convolution backward on the installed GPU uses nondeterministic atomic reductions; separate full-resolution CUDA passes confirmed finite official losses and gradients for every variant. C-UP was bitwise identical to fixed bilinear interpolation of the native learned basis.

Audited full-model totals at input 640 are 2,842,998 parameters and 9.7866752 GFLOPs for F00/F10/C-UP; 2,842,998 parameters and 17.8770944 GFLOPs for F01/F11; and 3,074,334 parameters and 17.8267136 GFLOPs for C-COMP. The profiler does not count parameter-free interpolation, so C-UP's interpolation cost remains reported separately. C-COMP differs from the R1 full-model total by 0.282%, within the frozen ±5% compute-control tolerance.
