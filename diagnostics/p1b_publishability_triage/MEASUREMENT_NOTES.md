> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# Measurement scope and interpretation

## Matching versus full output

The provided split has 2,032 unique original-file hashes and 2,032 unique decoded-pixel hashes, with no exact train/val overlap (`artifacts/split_integrity.json`). This supports exact-image holdout only; scene, sequence, orchard and perceptual near-duplicate independence have not been established.

Diagnostic matching reuses the P1A rule: greedy descending **bbox IoU >=0.5**, confidence >=0.25, one-to-one, class-agnostic. It describes mask utilization conditional on a localized instance; it is not detection recall or class-aware mask AP. Common-GT cross-model comparisons use the intersection of these independently matched sets, and always show each model's own coverage/scale distribution alongside it.

Full-output evaluation keeps scores, boxes, class IDs and candidate order frozen, includes all candidates at confidence >=0.001 up to 300, and removes only empty masks as native Results does. COCO matching is class-aware. Unmatched GT and false positives participate. AP is averaged over IoU thresholds 0.50:0.05:0.95, with 101 recall samples and maxDet=300. Metrics are computed on the common 640 input raster; `AP_small_input640` uses area <=32² in that raster. These numbers must not be relabeled as original-resolution COCO benchmark AP. Official trainer metrics, if present, are separate measurements.

## Geometry

FP/FN are absolute input-grid pixels. Symmetric difference is (FP+FN)/GT area. Perimeter is the count of inner boundary pixels after a 3×3 erosion; perimeter-normalized error is (FP+FN)/perimeter. Boundary F score tolerates Euclidean distance <=2 input pixels. Symmetric contour distance averages the two nearest-boundary distance means using OpenCV's 5×5 L2 distance-transform approximation. Empty predictions receive boundary F=0 and the image diagonal as a finite contour-error sentinel. These are descriptive digital-mask measurements, not continuous physical lengths.

Oracle headroom gain uses (oracle IoU-native IoU)/(1-native IoU) only when native headroom >=0.01. Learned recovered-gap fraction instead uses (probe IoU-native IoU)/(stable oracle IoU-native IoU), only for fixed pilot val matches with denominator >=0.01. They are different ratios and neither replaces absolute gains or AP. Negative gains and ratios above one are retained: a regularized BCE solution is not an IoU optimum.

Continuous-area regressions include log area, log perimeter, GT count, log(1+normalized nearest-neighbor distance), split and a singleton indicator. Bootstrap resamples whole images, retaining their instances. Area/perimeter correlation and only 36 pilot images limit interpretation; these intervals are descriptive and not confirmatory p values. Split-specific conditioning fits omit no observations, but their constant split column is naturally rank-deficient and is handled by least squares; the numerical design rank is reported.

## Probe controls and limitations

All variants have the same 136→64→32 residual MLP and two learned 32-value constants. Fixed 3×3 ROI projections produce 32-dimensional P5, P3 and prototype descriptors. Learned parameter counts match; input-dependent operations necessarily differ by which information source is present, and fixed projection buffers/FLOPs are reported separately.

Matching nominal parameter counts does not make the effective input-dependent function classes identical: a learned constant carries no instance-specific descriptor. Thus a true-source versus P0 gain alone is insufficient; the corresponding shuffled-source contrast is also required by the frozen decision rule. Neither a failed effect-size gate nor a broad bootstrap interval establishes statistical equivalence.

Probe assignment uses train GT, but spatial extraction uses predicted boxes. Descriptor normalization and shuffle-bank contents use train images only. C1/C2 use a seeded, per-epoch **bijective permutation within predicted-area bins**, excluding the instance's own image. Groups are randomly ordered, rows shuffled within groups, then cyclically displaced by the largest group size; the full maps are saved. Held-out controls draw from that same train-only bank by predicted scale, with no val GT lookup. No oracle coefficient targets are used. P0 and C3 intentionally implement the same capacity-matched null; exact agreement is an implementation check, not an independent statistical replication.

All 21 members train for the same 15 epochs and image order. Seeds change initialization and control draws. A failed gate means no demonstrated benefit in this small frozen-probe family, not a theorem that a richer predictor could never learn the gap. Baseline mask-target resolution and probe objective differ; only P1/P2/P3 contrasts against P0 isolate the added information source.

The first fitting attempt was stopped before held-out evaluation because the CUDA bilinear-interpolation backward separated mathematically identical P0/C3 members. It is retained under `artifacts/failed_probes/`. Scientific probe fitting restarts from the original seeds with deterministic algorithms and `CUBLAS_WORKSPACE_CONFIG=:4096:8`. Forward mask logits still use the exact native CUDA bilinear operator; its backward applies the same linear operator's transpose using fixed-order separable gather/reduction, avoiding atomic scatter accumulation. The independent CPU float64 adjoint check and 120-step train-only null-equality check are retained in `artifacts/contracts/probe_determinism.json`. This is a numerical implementation correction; loss, forward masks, seeds, epochs, inputs, and decision gates remain unchanged. P0/C3 equality is checked after every epoch as well as completion.

## Resources

Latency uses synchronized batch-1 float32 execution without another research GPU job. It includes CPU letterbox, transfer, unfused backbone/head, candidate selection, required ROI/projection work, one standalone probe and native mask assembly; disk I/O is excluded. Fixed random projections are cached on GPU for deployment timing. Desktop GPU usage may remain and is disclosed. GPU allocator peaks describe this process, not all system VRAM. MACs count as two FLOPs; ROI sample operations are stated separately to avoid false precision.
