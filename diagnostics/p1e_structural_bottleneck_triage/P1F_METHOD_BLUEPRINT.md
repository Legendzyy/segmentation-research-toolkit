> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# P1F METHOD BLUEPRINT

## Winning branch

**Thin-prototype spatial-resolution branch only.** Candidate selection and local residuals failed their registered gates; coefficient-side residuals remain closed.

## Problem statement

At the median, a stable 32-coefficient oracle recovers the GT interior perfectly but reaches only 0.875 thin recall, and 32/61 thin instances retain at least 0.10 failure. The first P1F experiment asks whether the 160×160 prototype lattice, rather than coefficient prediction, limits stride-scale protrusions and narrow structures.

## Minimal mechanism

Build a 320×320, 32-channel prototype bank from the existing stride-4 P2 feature, using one 1×1 adapter followed by the existing `Proto` topology. Keep the detector, TAL, NMS, coefficient count (32), coefficient-head topology, loss family and all inference thresholds unchanged. No attention, local residual, boundary head, mask-scoring head or new loss is permitted.

## Equation

Baseline: `M_i(x,y) = sigma(sum_{k=1}^{32} a_ik P_k^(160)(x,y))`.

P1F: `M_i^HR(x,y) = sigma(sum_{k=1}^{32} a_ik P_k^(320)(x,y))`.

Only the spatial sampling and source resolution of `P` change; `a_i` remains the native 32-dimensional coefficient vector.

## Insertion point

Route the existing stride-4 P2 tensor into `Segment.proto` at `ultralytics/nn/modules/head.py`; retain the linear mask assembly and crop path. Record exact source anchors and verify coefficient/no-op parity before training.

## Capacity and attribution controls

- Main: P2-HR prototype at 320×320, 32 bases.
- Resolution control: P2 is deterministically reduced to the baseline 160×160 lattice before the same prototype operator.
- Compute control: adjust only the prototype bottleneck width so the control matches main prototype FLOPs within 5%; report exact parameters/FLOPs.
- Keep the full detector and native coefficient path trainable under the same frozen schedule; do not initialize from P1D outcomes selectively.

## First training experiment

Run one preregistered development seed (42) at the P1D strong horizon and equal image/epoch budget against a fresh strong baseline and both controls. Evaluate only final scheduled checkpoints on validation. If the seed-42 stop rule passes, expand unchanged to seeds 128 and 2024; otherwise stop.

## Falsification and stop rule

Proceed beyond seed 42 only if all hold: AP, AP75 and small-object AP improve; thin recall and boundary F improve on the frozen subgroups; mask shrink/area-ratio and false-hole metrics do not regress beyond P1D limits; the advantage exceeds both attribution controls. Stop if gains come only from extra compute, if thin recovery does not improve, or if isolated synchronized latency rises by more than 10%.

## Cost and closest prior art

The 320×320 prototype tensor is 4× the spatial elements of the 160×160 baseline, so memory and mask-assembly cost must be measured rather than assumed cheap. Closest neighbors include BlendMask/SipMask (spatial basis control), PointRend/RefineMask/Mask Transfiner (fine-detail refinement), and high-resolution prototype/basis systems in the novelty matrix. Publication potential remains conditional and novelty risk high.
