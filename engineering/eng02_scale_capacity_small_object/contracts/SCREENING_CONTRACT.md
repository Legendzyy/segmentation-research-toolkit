> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../../docs/PROVENANCE.md)。

# ENG02 native screening contract

Frozen before any formal ENG02 training or validation result is inspected:

- **A0:** native YOLO11n-seg, 640, seed42, 60 epochs. Reuse ENG01 E0 only if checkpoint, source, initialization, data manifest, optimizer/schedule/augmentation, final-epoch policy, and evaluator compatibility all pass. Otherwise train A0 from the same native recipe.
- **A1:** native YOLO11n-seg, one high input size selected in the order 896 → 832 → 768 using only 8 GB VRAM feasibility and runtime stability. Freeze size, microbatch, accumulation, effective batch, and BN caveat before formal training; 60 epochs, seed42.
- **A2:** native YOLO11s-seg, 640, seed42, 60 epochs using the official same-family pretrained source. A2 is a capacity reference; if official weights cannot be obtained and pinned, record a blocker rather than substitute another model.
- All three use the same Blueberry train/val manifest, AdamW family, learning-rate schedule, augmentation family, 32 nominal effective batch target, final scheduled checkpoint, and a common full254 COCO mask evaluator. High-resolution evaluation is mapped to a fixed reference grid, and the exact transform must be audited before scoring.
- Primary: mask AP@[.50:.95]. Also AP50/AP75/AP90, small/medium/large AP, all-GT coverage, common-GT shape/FP/FN, parameters/FLOPs, peak training VRAM and batch-1 timing under stated GPU conditions. Shared-device timing cannot qualify an isolated-latency claim.
- **Scale YES:** A1 ΔAP ≥+0.30 pp, or Δsmall AP ≥+1.50 pp with ΔAP ≥−0.10 pp and AP75 decline no worse than 0.50 pp.
- **Capacity YES:** A2 ΔAP ≥+0.30 pp, or Δsmall AP ≥+1.50 pp with ΔAP ≥−0.10 pp.
- **Strong headroom:** ΔAP ≥+0.70 pp, or Δsmall AP ≥+2.00 pp with nonnegative ΔAP. This is a descriptive engineering allocation signal.
- If neither scale nor capacity passes, stop at K1. If one passes, follow only that branch. If both pass, select one based on AP, small AP, latency, VRAM, parameters, and training cost without launching both methods. Subsequent development, replication, external validation, and budget rules remain exactly as stated in the user prompt.
- Maximum 3 Stage A formal tasks, 4 Stage B, 6 Stage C, 6 Stage D; at most 19 new full training tasks and 72 training process hours. Never read test or modify P1A–P1F/ENG01/ICASSP.
