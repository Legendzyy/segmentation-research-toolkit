> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# P1A VERDICT: E

**EXP-SIS-20260918-P1A — DIAGNOSTIC NOT YET VALID**

实验和数值审计已执行到报告阶段。原始 coefficient 的 mask path 已闭环，BCE 优化收敛检查也已通过；但 oracle coefficient 的原生 float32 数值稳定性尚未完全闭环。本轮不采纳 A/B/C/D，不据此提出或实现新模块。

| 要求项 | 最终状态 |
|---|---|
| MASK_PATH_CLOSURE | **PASS** |
| ORACLE_OPTIMIZATION_CLOSURE | **PASS：BCE 收敛层面** |
| CHECKPOINT_COMPATIBILITY | **PASS：YAML、全部 state_dict keys/shapes、strict load** |
| ORACLE_NATIVE_PRECISION_CLOSURE | **FAIL：1/505 个 support fit 超过本轮补充精度门槛** |
| ARTIFACT_INTEGRITY | **PASS** |
| SCIENTIFIC_READINESS | **FAIL** |
| DEVELOPMENT_SAMPLE_MANIFEST | `artifacts/sample_manifest.json` |
| N_IMAGES | **36：train 18 / val 18** |
| N_GT_INSTANCES | **255：train 122 / val 133** |
| N_MATCHED_INSTANCES | **250：train 121 / val 129** |
| Matching coverage | **98.0392%**；5 个 unmatched GT 全部保留在 SET-A |
| NEXT-ROUND RECOMMENDATION | **FIX-DIAGNOSTIC-FIRST** |

## 决定 verdict 的 implementation blocker

`val/00260`、GT instance **8**、GT support：

| 项目 | 数值 |
|---|---:|
| 原生 float32 IoU | 0.9963963964 |
| float64 线性设计矩阵 IoU | 0.9945945946 |
| 绝对 IoU 差 | **0.0018018018** |
| support 内符号不同的像素数 | **1** |
| coefficient norm | 11725.9472 |
| support 内最大连续 logit 误差 | 0.002526691 |

该 GT **未匹配到预测框**，只属于 SET-A；不能将其称为 original coefficient 的失败。补充精度审计使用 `abs(IoU_native - IoU_float64_design) <= 0.001`。这是本轮工程审计门槛，不是论文统计阈值，也不是用户给定的科学效应标准。本轮保留该失败，不事后放宽门槛。一个像素的差异本身并不证明研究结论会改变，更不证明 prototype representation 不足。

此外，505 个 support fit 中共有 5 个符号差异像素；所有 high-norm 独立优化审计均通过，但最大的 coefficient norm 仍为 **5.25345e7**（predicted support），最大连续 logit 误差为 **13.6217**。后者没有造成该实例的二值 mask 差异，仍说明“大范数 + 有限精度”的连续值一致性不能只靠最终 IoU 检查。

未闭合精度案例（原资产，本次未收录：`artifacts/visualizations/precision_failure__val__00260__8.png`）

## 已完成的闭环与修复

原始 coefficient 的 36 图 / 276 个 post-NMS 候选全部完成实际 hook/extract。保存 P、三尺度 coefficient 对应的完整 anchor coefficient、post-NMS 原 coefficient、GT、预测框和 native mask；首图还保存 native/manual 连续 logits。P 为 `[32,160,160]`，raw coefficients 为 `[1,32,8400]`，post-NMS 为 `[N,32]`。

默认 native 路径与手工重建的连续 logits 最大/平均绝对误差均为 **0**，二值差异 **0**。低分辨率路径及每图前 3 个候选的 retina 路径二值差异也为 **0**。原始 coefficient 下，交换线性组合与插值顺序的最大误差为 `2.288818359375e-05`，通过预先设定的 `1e-4` 检查。全部 inference 后网络 state hash 不变。完整顺序、training/inference 差异、坐标缩放与源码锚点见 [MASK_PATH.md](MASK_PATH.md)。

v1 暴露了一个真实的诊断实现问题：在 float32 中预插值 P、随后以 float64 优化 coefficient，会让极大 coefficient 放大预插值的舍入误差。不能凭原始小范数 coefficient 的交换顺序检查就认定所有 oracle coefficient 都稳定。独立 Newton 与 L-BFGS 的 BCE 差异揭示了这一点。

v2 改为 **float64 构建固定双线性设计矩阵**，原生 mask 报告仍使用 float32 原生顺序；主预算由 600 提升到 1800，扩展预算由 1800 提升到 3600。没有修改样本、matching、support、BCE 目标、阈值、模型参数或结构。所有 255 个 GT 与 250 个 matched predicted support 全量重跑，v1 已完整保存在 `artifacts/numeric_attempt_v1/`。

v2 的 primary/secondary 未收敛梯度数均为 **0**。固定 12 个 GT 的 60 次多初始化、扩展预算和独立 Newton 审计均通过：最大 IoU 变化 **0**，最大 BCE 差 `3.62866e-11`。没有 `IoU_refit < 0.8` 的实例需要额外低质量审计。另对大范数解完成 **88 次**补充优化审计，全部通过其收敛门槛。**这些是优化收敛证据，不等于 oracle 到原生有限精度实现的完整数值证书。**

## 数据、sample 与匹配

只读取 `${DATA_WORKSPACE_ROOT}/datasets/mydata/images/{train,val}` 及对应 labels，没有读取 test 图像、标签或 outcome。全 development GT 统计为 **2032 图 / 14694 个合法实例**。6 条明显越界 polygon 已记录；它们不在 pilot 中。另有两条约 `1e-18` 的坐标舍入负值按明确的 `1e-9` 容差裁到 0；原始数据文件未改动。train/val 内容哈希无重复，所有入选原图、标签和 checkpoint 最终哈希未变化。

seed **20260918**。先按 split、GT-count 排序划三层，每层按 `SHA256(seed:split/image_id)` 选 6 图；共 36 图。24 图初稿只有 175 个实例，扩展到 36 图的决定发生在任何 inference/refit 之前，记录见 PROTOCOL 和 git history。最终覆盖 small 73、large 67、close 69、far 65、严格 local-neighbor=0 的孤立实例 9 个。

nearest-neighbor centroid distance 除以目标 `sqrt(area)` 得 normalized distance；local neighbor 是距离不超过 `3*sqrt(area)` 的其他实例数。原图像素面积、面积占比、centroid、bbox 宽高、输入网格面积及 boundary-to-boundary 最近距离全部保存。图像 GT count 不等同于密度。

固定推理 confidence=0.25、class-aware NMS IoU=0.7、max_det=300。matching 为 **class-agnostic bbox IoU descending greedy one-to-one，gate 0.5**，同分按 GT/pred index 排序；matching 在 refit 前保存。分类一致率另记为 99.6%。不存在 mask-IoU 挑选预测。

SET-A 包括所有合法 GT；SET-B 仅包括 matched GT。原 coefficient 与 refit 在每项比较中使用相同 support。主分析是 GT raster bbox，次分析是固定 predicted bbox；框外丢失的 GT 像素计为 FN。缺失 original/predicted-support 字段只表示 unmatched，不是 0，也未删行。

## 暂存数值附录：禁止作为 A/B/C/D 的科学结论

以下保留要求的四项 contrast 以便复核，但全部标记 **PROVISIONAL**。所有报告 IoU 实际通过原生 float32 运算顺序计算；BCE refit 是可行重建，不是严格的 IoU 上界。

| Analysis set / support | N | mean IoU original | mean IoU refit | median paired ΔIoU |
|---|---:|---:|---:|---:|
| SET-A / GT support | 255 | 不适用 | 0.985431 | 不适用 |
| SET-B / GT support | 250 | 0.950548 | 0.985508 | +0.024969 |
| SET-B / predicted support | 250 | 0.942103 | 0.978623 | +0.022102 |
| SET-A / train GT support | 122 | 不适用 | 0.984546 | 不适用 |
| SET-A / val GT support | 133 | 不适用 | 0.986244 | 不适用 |

SET-A 最小 refit IoU=0.907241，255/255 的暂存值均 >=0.9；5 个 unmatched GT 的 mean refit=0.981622。GT-box-only mean IoU=0.693699，避免把 tight GT box 的先验完全归给 prototype。SET-B 的 GT support 与 predicted support refit 差值 median=0.003332，没有实例下降 >=0.15；预定义 spatial gate 计算值为 FALSE，**不在本轮升级为机制结论**。

| 暂存 subgroup | N_GT | mean refit | mean matched ΔIoU |
|---|---:|---:|---:|
| Smallest area quartile | 73 | 0.982806 | 0.061224 |
| Largest area quartile | 67 | 0.989765 | 0.014694 |
| Close neighbor | 69 | 0.986478 | 0.027454 |
| Far neighbor | 65 | 0.987550 | 0.039607 |
| High image GT count | 144 | 0.984506 | 0.039845 |
| Low image GT count | 35 | 0.989472 | 0.026022 |

控制面积分层后的 close-minus-far refit 均值差暂存为 **-0.002989**，按图 bootstrap 描述性区间 `[-0.008080, 0.001518]`；coefficient gap 差为 **-0.000961**，区间 `[-0.010292, 0.006531]`。控制输入像素面积的 sensitivity 分别为 -0.003178 和 +0.000026。另保存 train/val 分开结果、high/low count 对照及 `log(input area) + normalized NN + image count` 描述性回归，无机制 p-value。

这些暂存值不被用于声称 density-specific bottleneck，也不被用于宣布该假设已被反驳。按协议，E 优先于 A–D。

## 对八个问题的本轮回答

1. **shared prototypes 是否已有足够 GT 信息？** 暂不签发科学结论；当前可行重建数值已保存，须先关闭 oracle 原生数值稳定性。
2. **original coefficient 距离 representation 上界多远？** 没有被证明的 IoU 上界；暂存 matched GT-support median gap 为 0.024969，只是本次 BCE 解的差值。
3. **gap 是否主要在 dense/close/small？** 分组表已生成，E 状态下不采纳任何 subgroup 机制叙事。
4. **density effect 能否被 object size 解释？** 已完成面积分层、输入像素面积 sensitivity 和描述性回归，机制判定暂缓。
5. **crop/localization/resize 是否更像真正瓶颈？** 支持框对照已完成，但本轮不选择 C；当前明确 blocker 是 oracle 数值精度，不是已证实的检测定位瓶颈。
6. **哪些观察反驳原假设？** 暂不正式反驳科学假设。被工程审计反驳的是“原始 coefficient 下可交换算子，便足以保证任意大 oracle coefficient 的数值一致性”这一实现假定。
7. **下一轮最小结构干预应在哪里？** 当前无依据选择任何结构干预。先处理近零 logits、coefficient 量化/范数和原生算子顺序的数值闭环。
8. **是否直接停止 prototype/coefficient 研究线？** 不能凭未完全有效的 diagnostic 作该决定；暂停结构推进，先修 diagnostic。

## 复现与交付

环境：Python **3.10.21**，torch **2.1.2+cu121**，torchvision **0.16.2+cu121**，CUDA runtime **12.1**，cuDNN **8.8.1**，RTX 4060 Laptop 8GB。clean upstream 为 [Ultralytics 8.4.155 / b454f423600f99d41730bd75a7a26b491187de36](https://github.com/ultralytics/ultralytics/tree/b454f423600f99d41730bd75a7a26b491187de36)，源码未改动。

Checkpoint 为历史全监督 plain YOLO11n-seg `01_baseline_v11n4/weights/best.pt`，仅根据 args.yaml 和结构选择，未读取历史 outcome。其记录版本为 8.4.14；strict compatibility 不能证明历史训练 recipe 未受历史 source 修改影响。因此本轮范围限定为该 checkpoint 的 clean upstream 推理诊断。

| 资产 | SHA-256 |
|---|---|
| Checkpoint | `eb803e39be7935144816e7eb593e6bc28dec1b9e7499f9b00bbce61a989836c3` |
| Dataset manifest | `f4c69b1e54832e7ad383eced4c6703975fd7d4f187a92dce71fdc003cf98b91b` |
| Sample manifest | `e3fc93e8ab997026d42b42332ef06b097717edc97fb211c50c1f61cdc0008faf` |
| v2 config | `f50aa4f20d40c545a44a61e87edee1d44f983f1a36b5eda963b28e3c51c82c9c` |

关键入口：

- 完整 per-instance CSV（255 行，含 provenance）（原资产，本次未收录：`artifacts/per_instance_results_annotated.csv`）
- sample manifest（原资产，本次未收录：`artifacts/sample_manifest.json`） / dataset manifest（原资产，本次未收录：`artifacts/dataset_manifest.json`）
- mask closure（原资产，本次未收录：`artifacts/mask_path_closure.json`） / BCE optimizer closure（原资产，本次未收录：`artifacts/oracle_optimization_closure.json`） / precision closure（原资产，本次未收录：`artifacts/precision_closure.json`）
- 最终完整性验收（原资产，本次未收录：`artifacts/final_validation.json`）：artifact integrity PASS，scientific readiness FAIL；validator 非零退出是保留的门槛失败。
- 总览图（原资产，本次未收录：`artifacts/plots/diagnostic_overview.png`） / 优化曲线（原资产，本次未收录：`artifacts/plots/optimizer_curves.png`）
- `artifacts/visualizations/`：六类规则各 2 图，加 1 张精度失败图，共 **13 张**；选择清单（原资产，本次未收录：`artifacts/visualization_selection.json`）。已进行视觉检查。
- exact CLI / run registry（原资产，本次未收录：`artifacts/run_registry.csv`），每次 attempt 的 config、git commit/diff、stdout、stderr 在 `artifacts/runs/`。
- 代码 diff（原资产，本次未收录：`artifacts/git_diff_from_empty.patch`） / 最终源码快照（原资产，本次未收录：`artifacts/final_source_snapshot.json`） / 全部 artifact 哈希索引（原资产，本次未收录：`artifacts/artifact_index.json`）。

执行命令见 [README](README.md)。历史源码、原始数据、checkpoint 均未修改。没有新结构、训练、pseudo-label 或新 loss；本轮未实现下一轮 recommendation。

**NEXT-ROUND RECOMMENDATION: FIX-DIAGNOSTIC-FIRST**
