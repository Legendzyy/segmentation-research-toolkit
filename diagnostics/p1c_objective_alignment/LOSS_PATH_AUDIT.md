> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# TRAINING-TO-INFERENCE MASK PATH TABLE

Read before any fitting. Official source commit b454f423600f99d41730bd75a7a26b491187de36; source tree clean. Exact source copies/hashes and runtime contracts are retained in artifacts/audit.

| Operation | Official clean11 training | P1B/P1C native inference | Classification |
|---|---|---|---|
| cv4 input | P3 64×80², P4 128×40², P5 256×20² | same inputs | IDENTICAL |
| coefficient head | per scale Conv3×3→Conv3×3→linear1×1, 32 coefficients, 8400 anchors | same, NMS selects anchors | IDENTICAL |
| prototype | Proto on P3, 32×160² at input640 | same | IDENTICAL |
| GT raster | official polygon fill then cv2 resize; ratio4/2/1 →160/320/640 | no GT | OBJECTIVE-ONLY |
| overlap_mask | masks sorted by descending raster area; smaller instance overwrites overlapping pixels, integer IDs | masks independently overlap | OBJECTIVE-ONLY |
| ratio mismatch handling | loss.py 517–521 upsamples P to target grid, commented-out GT downsampling is inactive | logits upsample after combination | RESOLUTION DIFFERENT |
| combination | einsum(a,P_r) on target grid | float32 a@P160 | IDENTICAL mathematically; float32 order differs for ratio<4 |
| interpolation | P160→P320/640 before assembly when needed, align_corners=False | assembled logits160→640, align_corners=False | RESOLUTION DIFFERENT |
| support | continuous GT bbox scaled to target grid, crop BCE | continuous predicted bbox, crop binary mask after resize | SUPPORT DIFFERENT |
| reduction | sum(cropped BCE)/(H_r W_r × normalized GT bbox area), then mean over positive TAL anchors, ×box gain | none | OBJECTIVE-ONLY |
| assignment | official detached box/class TaskAlignedAssigner topk10 | class-aware NMS conf.001 IoU.7 max300 | OBJECTIVE-ONLY / INFERENCE-ONLY |
| sigmoid/threshold | stable BCEWithLogits, no hard threshold | strict logit>0 (equivalent sigmoid>.5), then crop uint8 | INFERENCE-ONLY |

L_original = gain/Npos Σ_i [Σ_xy I_GTbox,r(x,y) BCE(a_i·U_r(P), Y_overlap,r,i) / (H_r W_r A_GTnorm,i)]. The official optional semantic Dice branch is absent in YOLO11; instantiate-only BCEDice is never used here.

L_native = gain/Npos Σ_i [Σ_xy I_predbox,640(x,y) BCE(U_640(a_i·P), Y_overlap,640,i) / (640² A_GTnorm,i)]. Fixed GT weights are retained intentionally to isolate support/order. Pixels outside predicted support have zero coefficient gradient; computing BCE on cropped logits adds constants and is not the useful optimization definition. Binary inference is nondifferentiable, so exact alignment refers to its continuous prethreshold forward and spatial support, not a differentiable hard threshold.

B2r1 already implements full640 supervision. Interpolation and linear combination commute in exact arithmetic, so their order alone is not a new expressive mechanism. B3 is principally a predicted-support intervention after resolution is controlled. Overlap target occlusion and TAL-anchor weighting are additional real differences from deployment AP, held constant here; B3 does not claim to eliminate all train/inference differences. P1B probes used independently rasterized full GT, matched predictions and equal-image weighting; these cannot silently be called the same objective as this controlled factorial.
