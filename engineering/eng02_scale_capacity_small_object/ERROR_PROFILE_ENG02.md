> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# ENG02 preliminary three-seed error profile

Diagnostic matching uses confidence ≥0.25 and greedy same-class mask IoU ≥0.5. It is not the COCO AP matching algorithm. Small/medium/large use input640 GT area. Seed42 box IoU uses detector boxes from an ENG02 rerun; seeds128/2024 use mask-derived bounding boxes from the pinned historical predictions. These sources are not pooled for a detector-box claim.

| Seed | Small GT | Small coverage | Medium coverage | Large coverage | Small missing | Small classification | Small localization/mask | AP50-AP75 | Background FP | Duplicate/class FP |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 42 | 132 | 0.833 | 0.953 | 0.998 | 16 | 0 | 6 | 0.0431 | 195 | 38 |
| 128 | 132 | 0.818 | 0.950 | 0.990 | 17 | 0 | 7 | 0.0403 | 185 | 46 |
| 2024 | 132 | 0.833 | 0.951 | 0.993 | 18 | 0 | 4 | 0.0379 | 190 | 53 |

Matched distributions (median [10th, 90th percentile]):

- seed42 small: box IoU 0.902 [0.753, 0.951]; mask IoU 0.893 [0.752, 0.934]; score 0.792 [0.423, 0.908].
- seed42 medium: box IoU 0.959 [0.870, 0.980]; mask IoU 0.953 [0.866, 0.975]; score 0.939 [0.801, 0.964].
- seed42 large: box IoU 0.978 [0.926, 0.989]; mask IoU 0.977 [0.931, 0.986]; score 0.964 [0.935, 0.974].
- seed128 small: box IoU 0.891 [0.731, 0.945]; mask IoU 0.899 [0.800, 0.935]; score 0.816 [0.477, 0.911].
- seed128 medium: box IoU 0.953 [0.868, 0.980]; mask IoU 0.953 [0.868, 0.975]; score 0.940 [0.822, 0.965].
- seed128 large: box IoU 0.975 [0.936, 0.990]; mask IoU 0.978 [0.934, 0.986]; score 0.961 [0.933, 0.972].
- seed2024 small: box IoU 0.888 [0.762, 0.948]; mask IoU 0.899 [0.796, 0.937]; score 0.777 [0.466, 0.911].
- seed2024 medium: box IoU 0.953 [0.872, 0.980]; mask IoU 0.954 [0.868, 0.975]; score 0.939 [0.801, 0.964].
- seed2024 large: box IoU 0.974 [0.933, 0.989]; mask IoU 0.978 [0.937, 0.986]; score 0.961 [0.932, 0.974].

A GT without a ≥0.5 same-class match is assigned wrong-class overlap, partial localization/mask overlap, or missing in that priority. Unmatched predictions are described separately. The categories are diagnostic approximations and cannot distinguish all annotation ambiguity. Stage A proceeds regardless of these patterns.
