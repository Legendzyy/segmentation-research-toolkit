> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# P1C measurement scope

## Full AP and fixed matched masks

Full AP uses the inherited254-val set,1803 GT annotations and two classes. All masks and area thresholds are evaluated on the640 letterboxed input grid. This is the P1B controlled evaluator; input640 small/medium/large groups must not be confused with original-photo-area groups in other reports. Candidate boxes, class scores, NMS order and the max300 limit are frozen. Confidence threshold is.001, NMS IoU.7. Empty binary masks are omitted exactly as in P1B. Every formal final checkpoint is evaluated on all254 images.

COCO precision tensor dimensions are IoU threshold × recall threshold × class × area group × maxDet. AP averages valid entries over.50:.05:.95; AP50/AP75/AP90 use indices0/5/8. Small, medium and large areas follow COCO's ranges on this input grid. The inherited native AP/AP50/AP75/small-AP replay is asserted equal to P1B within1e-12. All formal predictions, precision tensors and class-aware matching rows are retained.

Fixed diagnostic pairs instead use box-IoU>=.5, confidence>=.25, greedy one-to-one class-agnostic matching inherited from P1B. There are1728 pairs over251 images, including108 small pairs. The full evaluator has132 small GT. Corrections do not change these fixed pair identities. Up/down/net crossing counts are measured against each pair's native mask IoU and do not substitute for score-ranked AP. Full-AP cohort tables verify exact candidate-key coverage with round-trip float parsing; dropping unmatched joins is prohibited.

The retained pycocotools2.0.11 source explains area eligibility: `artifacts/audit/source/pycocotools/coco.py` line349 derives prediction area from its RLE mask, and `cocoeval.py` lines297–299 ignore unmatched detections outside the selected area range. A correction can therefore alter small-AP false-positive eligibility while leaving boxes and scores fixed. The frozen-area counterfactual in P1B_AP_DIAGNOSIS.md is explicitly nonstandard and is never substituted for formal AP.

B2ratio1 and B3 share official float32 overlap targets. The inherited evaluator rasterizes each GT independently with its original float64 parsing. A validation-only target audit finds446 raster-precision XOR pixels across121/1803 GT, and19464 pixels removed by overlap ownership across645 GT; total target/evaluation disagreement is19870/11565141GT pixels. For all132 small GT these counts are15 precision pixels,313 overlap removals and328 total disagreements over90066GT pixels. These remaining target differences are held constant between B2ratio1 and B3; exact native-decode alignment refers to the forward operator and spatial support, not complete evaluator equivalence.

## Pixel, boundary and topology statistics

Per-instance CSVs retain GT area, predicted area, FP, FN, precision, recall, symmetric difference, area ratio, GT perimeter and error/perimeter. IoU is TP/(TP+FP+FN). Boundary F uses inner3×3-eroded boundaries and2input-pixel tolerance. Contour distance averages both directional boundary distances using OpenCV DIST_L2/mask5. An empty prediction receives boundaryF0 and image-diagonal contour distance. Means weight each fixed pair equally; full AP does not use that weighting.

`thin_pixel_recall` in the main evaluation CSV is a GT distance-to-boundary band<=1.5pixels. It is NOT, by itself, a measure of isolated thin appendages. The supplementary topology audit uses Zhang skeleton pixels with GT distance-to-background<=2pixels, reports the number of such pixels and missed coverage, and separates true GT holes from false predicted holes inside GT foreground. Raster skeleton spurs are a limitation. Normalized perimeter is inner-boundary-pixel count/sqrt(mask area); connected components use8-connectivity. Hole filling uses scipy's default binary-fill connectivity. These are descriptive diagnostics, not losses or deployment inputs.

Image-cluster bootstrap intervals use1000 fixed-seed resamples of validation image IDs. They quantify sampling variation conditional on a fitted member and this dataset, not training-seed or cross-dataset uncertainty. Three-seed results are shown individually and with mean/range; one-seed auxiliary controls are labeled explicitly. The21 P1B probes are correlated controls, not21 independent experiments.

## Gradient diagnosis

The hash-selected39 representative instances cover every requested IoU bin and size category, with unavailable strata disclosed: no small instance occurs in the[.5,.6) bin; large instances number only1 and2 in the first two bins. Compare original160, official ratio1/640, exact native640/predicted support, and an order-only640/GT-support control. Boxes, prototype and targets are fixed while differentiating32 coefficients. A normalized coefficient step of.01 is re-rendered through native inference. No representative-instance gradient is used to fit a deployed predictor or select a checkpoint.

Native forward interpolation is the exact pinned CUDA operator. A deterministic gather/reduce adjoint handles4×bilinear resize. Original-loss/gradient contracts and native binary parity are checked before fitting. Order-only interpolation/linear-combination differences are floating-point effects, not new representation capacity. The39-instance gradient means are mechanistic examples, not population estimators.

## Training and efficiency

See PROTOCOL.md for the fixed15-epoch, final-checkpoint-only recipe. Features/prototypes and detector outputs are cached exactly; original backbone, neck, prototype, box/class branches and all BN running statistics stay frozen. Original-head variants train160224 existing parameters; residual controls add10912 nominal parameters. B1 is exactly the B6 extra-training control. Nominal parameter equality of coefficient/geometry/constant residuals does not imply identical effective function classes.

B1/B2/B3 share the same optimizer and recipe; B4/B5/G4/G5/C4/C5 share a separate residual optimizer recipe. Across head and residual structures the learning rates differ, so a cross-structure contrast is not a pure parameter-count experiment. P1B P0 additionally differed in selected training pairs, independent GT masks and weighting; matching its gain would not be a causal P5 ablation.

Resource measurement uses batch1 float32 unfused inference, preletterboxed CPU input through transfer/network/NMS/optional residual/GPU binary masks. It excludes disk, letterbox and RLE encoding and therefore differs from the P1B timing scope. Twelve fixed images, three warmups and36 measured passes are used. Network FLOPs inherit the audited9.7866752GFLOPs estimate; dense residual arithmetic adds21504 multiply/add operations per candidate, while normalization, NMS, interpolation and crop are not claimed to be fully captured by that estimate. Peak allocated VRAM is the process tensor allocation, not total desktop GPU memory. Training time/peak memory are recorded as joint-run quantities, not falsely attributed independently to every variant.

All19 final benchmark members observed another Python GPU workload. Timings are observational under shared load, not isolated overhead estimates. The reported process peak also includes checkpoint tensors and online-parity temporary tensors; it is not a pure inference-activation peak. Online-parity work is outside the timed forward interval. Parameter/FLOP equality for original-head variants does not imply bitwise equal observed latency under contention.

## Decision boundaries

AP75 and small AP take precedence over matched IoU. A development candidate with both below native is stopped under the predeclared rule; otherwise the five key candidates require three seeds. B2ratio1 is fixed in advance. The strict section12 Part-II gate requires an independent B3 advantage over both B1 and B2ratio1 with stable full-quality evidence. No positive diagnostic, counterfactual, overall-AP scalar or novel-looking plot can override that gate. Any final claim is bounded by this frozen clean YOLO11 model, these recipes and this validation set.
