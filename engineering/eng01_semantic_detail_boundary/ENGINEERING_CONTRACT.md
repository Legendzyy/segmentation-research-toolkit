> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# ENG01 engineering contract

Frozen before the first formal training result. See `USER_REQUEST_ENG01.md` and `configs/frozen.json` for the full authorization and numerical gates.

- Primary data are the existing audited Blueberry 1,778-train/254-val split, YOLO11n-seg, input 640, native K32/160-grid mask head. The official initialization and historical source hashes are pinned in `configs/frozen.json`. Historical assets and raw data are read-only. Test is sealed.
- E0 uses the unmodified native graph. E1/E2/E3/E5 preserve the semantic feature from neck layer 16, route backbone layer 2 into the same zero-initialized residual output projection after native Proto `cv2`, and leave the detector branches unchanged. Detail width is 32. E2 uses official MLCA defaults from commit `afbeb47a` under GPL-3.0 attribution; E3/E5 use a single spatial gate. E4/E5 add a training-only boundary head on the post-fusion Proto feature.
- The boundary target is constructed after the same augmentation transforms from each separate instance polygon at input resolution. A radius-2 morphological gradient is unioned after per-instance computation, then downsampled to 160-grid with max occupancy. A transformed valid-pixel map excludes padding. The native mask target and native loss stay unchanged. The boundary loss is balanced positive/negative BCE with weight 0.1, inserted after official batch scaling without a second batch multiplier.
- All six formal runs use separate seed42 initialization, 60 epochs, final planned checkpoint, AdamW/augmentations copied from P1F F00. The E5 real-batch smoke and shared-GPU batch probe passed, so common microbatch is frozen at 8. No best-epoch selection. The six GPU runs are a single queue. Shared-GPU timing is descriptive only.
- Development revisions are limited to registered R-A (fixed smaller detail injection) and R-B (boundary weight 0.03), each permitted only on its stated outcome trigger and each charged to the 20-task/72-hour budget. Blueberry repeat and MinneApple opening follow Section 12 of the request exactly.
- E0 final evaluation and all method evaluation use identical full254 image/GT identities, confidence 0.001, NMS IoU 0.7, max_det 300, input640 COCO mask AP. No historical P1F/P1D verdict is rewritten.

This stage is housed in its own Git repository because the parent project directory has no Git root. `runs/`, `checkpoints/`, and bulk predictions are excluded from Git but remain on disk with manifests and hashes.
