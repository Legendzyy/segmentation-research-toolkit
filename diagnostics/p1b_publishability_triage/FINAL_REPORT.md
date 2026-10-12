> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# P1B VERDICT: A — CROSS-MODEL LEARNABLE COEFFICIENT GAP

**最终决策：STOP 当前 H/P coefficient-calibration 结构及论文主线，不进入完整新网络实验。**

实验 `EXP-SIS-20260919-P1B` 已完成。稳定系数 gap 在三个 clean 模型中重复；仅使用推理时信息的 tiny probe，能够在 clean YOLO11 的留出图像上学习到小幅 matched-mask IoU 改善。但是，同容量基线和打乱控制也取得相近改善，H/P 的独立信息贡献没有成立，收益未通过完整 AP/AP75/small/boundary 联合门槛。**这里的 verdict A 描述实验现象，不等于 publication MAINLINE-A 通过。**“跨模型”修饰 gap 的重复性；learnability 只在 clean YOLO11 上验证，不能外推为三个模型都已验证可学习。

P1A 永久保持 **E — DIAGNOSTIC NOT YET VALID**。本轮建立独立 P1B contract，未改写 P1A。

| 必需状态 | 本轮结论 |
|---|---|
| NUMERIC_CLOSURE | **PASS**：历史参考和三个 clean 模型均闭合 |
| SMALL_OBJECT_GAP_AFTER_GEOMETRIC_CONTROL | **WEAK，作为跨模型通用机制**：逐模型冻结判定为 YOLO11/v8 的 predicted support SUPPORTED，YOLO26 WEAK；三者 GT support 均 WEAK |
| CROSS_MODEL_GAP | **REPEATED**：三个 clean checkpoint 的 own-set 与 common-GT set 均保留 gap |
| LEARNABILITY_PROBE | **SUPPORTED FOR MATCHED IoU ONLY**：P0–P3 及所有控制均通过三种子 matched-IoU 门槛；oracle 恢复比例仍弱且不稳定 |
| PROTOTYPE_SPECIFICITY_CONTROL | **NOT_SUPPORTED**：P2−P0 与 true-P 对 shuffle-P 的联合条件未通过 |
| FULL_AP_TRANSLATION | **NOT_SUPPORTED**：0/7 配置通过三种子联合质量门槛；并非所有 AP 都下降 |
| NOVELTY_RISK | **HIGH**：宽泛动机与组件已有充分先例，本轮缺少新的 source-specific 效果 |
| PUBLICATION_MAINLINE | **STOP**：MAINLINE-A 缺少信息源及完整质量证据；MAINLINE-B 的三环境证据未建立 |

完整数值、全部 21 个成员、非 IoU 指标、回归系数和成本见 [RESULT_TABLES.md](RESULT_TABLES.md)。冻结规则见 [PROTOCOL.md](PROTOCOL.md)，度量边界见 [MEASUREMENT_NOTES.md](MEASUREMENT_NOTES.md)。所有 IoU/AP 采用 0–1 单位；0.002 相当于 0.2 个百分点。

## 最重要的 10 个数值发现

1. **数值闭合：2,008/2,008 个主拟合、10,040/10,040 个正 λ 拟合通过。**主 λ 固定为 `1e-4`；四组主拟合的最大梯度为 `2.0843e-7`，最大 native/design logit 误差为 `1.5485e-5`，主拟合 IoU 差均为 0。正 λ 敏感性路径并非全部二值完全一致：YOLOv8 的最大 IoU 差为 `0.00012801`，仍低于预设 `0.001` 容差。
2. **原 blocker 的收敛与精度问题得到区分。**历史 `val/00260 / GT 8` 的无约束 raw norm 为 `11725.947`，native/ideal IoU 为 `0.996396/0.994595`，相差一个二值像素；梯度已达 `8.66e-9`。固定主 λ 后 raw norm 为 `34.563`、standardized norm 为 `16.252`，两条路径 IoU 均为 `0.989209`。该 GT 未匹配到预测，属于 privileged GT-support 诊断，不能当部署收益。
3. **三个 clean 模型的 own-set gap 都约为 0.031。**YOLO11：`0.941071→0.972279`，Δ=`0.031207`，覆盖 `248/255`；YOLOv8：`0.940435→0.971613`，Δ=`0.031178`，覆盖 `250/255`；YOLO26：`0.940768→0.972313`，Δ=`0.031545`，覆盖 `240/255`。均为 predicted-support pilot 匹配集合。
4. **在相同的 240 个 GT 上，gap 仍重复。**YOLO11/v8/26 的 ΔIoU 分别为 `0.029914 / 0.028809 / 0.031545`。共同集合的面积 min/Q1/median/Q3/max 为 `424 / 2137.75 / 4906.5 / 8804 / 28640` 输入像素，避免混用各模型不同的匹配集合；结论仍条件化于三者均能定位的实例。
5. **几何控制支持有边界：predicted support 为 2/3 clean 模型 SUPPORTED，GT support 为 0/3。**例如 YOLO26 的 log-area→headroom-gain 系数为 `+0.01359`，区间 `[-0.05349,+0.07188]`；log-area→perimeter-error-gain 为 `-0.18330`，区间 `[-0.41840,+0.00612]`。不能把 raw small-object ΔIoU 放大解释为三模型共同的“小目标瓶颈强四倍”。非 IoU 改善确实存在：clean YOLO11 pilot 的平均 FP `154.94→48.31`、FN `100.63→75.21`、boundary F `0.94024→0.99105`、轮廓距离 `0.80308→0.34342` 输入像素。
6. **无需 H/P，P0 已有稳定但很小的留出改善。**在 251 张图像的 1728 个固定匹配实例上，native IoU=`0.931942`；P0 三种子为 `0.934350 / 0.934257 / 0.934480`，增益 `0.002408 / 0.002315 / 0.002538`，图像 bootstrap 区间分别为 `[0.001385,0.003431] / [0.001258,0.003293] / [0.001571,0.003606]`。全部 21 个成员均通过本轮 matched-IoU learnability gate；不能选择 verdict G“不可学习”。
7. **H/P 独立贡献未过控制。**P1−P0 三种子为 `-0.000081 / +0.000813 / -0.000487`；P2−P0 为 `+0.000371 / +0.000653 / +0.000094`，这六个区间均跨零。P3−C1 为 `-0.000142 / +0.000948 / -0.000506`；P3−C2 为 `-0.000041 / +0.000071 / -0.001085`。均未满足所有种子增益≥`0.002`且方向区间为正的规则。P0/C3 参数、训练记录、matched IoU 和完整 AP 完全一致。
8. **matched gain 没有形成所需的完整质量改善。**P3 的 AP 增益为 `+0.002534 / +0.003413 / +0.001757`，但 AP75 全部下降 `-0.001969 / -0.000858 / -0.002372`；small AP 变化为 `-0.006961 / +0.003518 / -0.005039`。全部 21 个成员中，18 个 AP75 下降、20 个 small AP 下降。C2 虽然三个种子的 AP 增益均超过 `0.002`，仍全部损失 AP75 和 small AP；不能只挑 AP 正数签发结论。
9. **恢复比例仅是弱补充。**clean YOLO11 pilot-val 的 129 个匹配实例，native/stable IoU=`0.940223/0.972850`，gap=`0.032627`。排除 gap<`0.01` 的 31 个实例后，仅剩 16 张图像、98 个实例。P0 三种子的平均 recovered fraction 为 `1.879% / 6.902% / 1.082%`，区间均跨零；P3 为 `0.120% / 10.822% / 2.289%`，仅种子 128 区间不跨零。不能把这些比例当整个验证集稳定恢复了多少 oracle gap。
10. **成本小，但不足以挽救质量证据。**每个 probe 增加 `10,912` 个可训练参数，MLP 为 `21,504` FLOPs/候选；P3 固定投影另有 `202,752` FLOPs/候选与 `101,376` 个 float32 buffer 元素。实测 native/P0/P3 平均延迟为 `36.341/37.425/37.444 ms`，FPS 为 `27.52/26.72/26.71`，峰值 allocated VRAM 约 `183.4/183.8/183.9 MiB`。在线路径与评估文件共核对 `3,076` 个掩码，像素差为 0。

## 实验范围与数值含义

三个 clean baseline 在同一 1778-train/254-val 划分上训练 30 轮，使用最后一轮 checkpoint。各代保留官方 mask objective 和 inference 差异：YOLO8/11 为 NMS 路径，YOLO26 为 one-to-one/end-to-end、Proto26 多尺度融合及附加语义监督。它们共享 prototype linear combination，并不具有相同 predictor 或相同失败机制。源代码锁定于 Ultralytics commit `b454f423600f99d41730bd75a7a26b491187de36`，详见 [MODEL_AUDIT.md](MODEL_AUDIT.md)。

三模型完整验证集 native mask AP/AP50/AP75/small AP 分别为：

| 模型 | AP | AP50 | AP75 | small AP |
|---|---:|---:|---:|---:|
| YOLO11n-seg | 0.839685 | 0.932217 | 0.891635 | 0.598191 |
| YOLOv8n-seg | 0.839764 | 0.929954 | 0.893843 | 0.618766 |
| YOLO26n-seg | 0.835143 | 0.926042 | 0.888597 | 0.576662 |

以上是共同 **640 输入栅格、maxDet=300** 的 COCO-style class-aware AP，包含全部 1803 个合法 GT；small GT 共 132 个。不能改称原分辨率官方 benchmark AP。matched 诊断采用 bbox IoU≥0.5、confidence≥0.25、class-agnostic 分配；full AP 使用 confidence≥0.001 的完整输出，二者分母和匹配方式不同。clean YOLO11 的 matched small 子集为 108 个实例、43 张图像。

框、分数、类别和候选顺序冻结；空掩码按 native 规则移除，因此最终非空 mask 数量可以变化。所有未匹配 GT 与 false positives 仍参与 full AP，oracle 掩码从未作为部署预测。

稳定 oracle 优化的是局部列 RMS 标定后的 `b_j=a_j RMS(X_j)`，目标为 mean BCE + `λ||b||²/2`。所有 quality 经 float32 `a@P`、原生双线性上采样、crop/threshold 重新测量，并核对 upstream decode。float64 design 只是求解工具。优化收敛、实数域线性张成空间可表示性、有限精度 native 可实现性是三件事。正则化保留了实质 gap，同时付出了部分无约束 quality；两种诊断方向一致，数值和“可达上界”含义不同。BCE 解不是经证明的最大 IoU 上界。

对 local design 先做列尺度归一化后记录了 singular spectrum、有效秩、condition number 和 coherence；raw norm 不用于跨模型比较。该处理不消除一般通道混合、支持区域和插值造成的参数化依赖。conditioning 分支停止：YOLO11-val、YOLOv8-train、YOLO26-val 的 predicted-support 条件数关联区间均跨零，pooled 关联反而为负，GT-support 更弱，未满足用户要求的跨 split/模型稳定链条。因此没有追加 normalization 干预或把大系数包装成 ill-conditioning mechanism。

## 哪些假设被否定，哪些仍是 provisional

| 假设 | 结论与边界 |
|---|---|
| 历史 gap 全部来自 precision artifact | 被本轮否定：约束后 native gap 保留，且三个 clean 模型重复 |
| gap 只属于历史 checkpoint | 被否定到本轮范围：同一数据/30 轮 recipe 下的三个 clean checkpoint 均有 gap；不是所有模型、数据和收敛阶段的定理 |
| 推理信息无法学到任何系数改善 | 在本轮 frozen family 内被否定：P0 等全部配置有留出 matched-IoU 改善；98 例 oracle 恢复比例不够稳定，不能夸大恢复量 |
| P 描述子是独立瓶颈 | 未获支持：P2−P0 很小且区间跨零，true/shuffled-P 联合控制失败；不等于证明任何更丰富的 P 描述子都无效 |
| H 主导，或 H/P 互补 | 未获支持：P1−P0 不稳定，P3 没有稳定优于两种单源及对应 shuffle controls |
| 所有模型都有相同的强 small-object 机制 | 未成立：predicted/GT support 与 YOLO26 结果限制了该叙事；面积相关性不是因果证据 |
| condition number 高即可推出 normalization 方法 | 未成立，分支不触发；没有 numerical accessibility→learnability→native quality 的干预链 |
| matched IoU 上涨足以支撑最终模块 | 被当前结果否定：联合完整质量门槛全部失败，AP75/small AP 多数下降 |

仍属 provisional 的部分：仅一个 orchard 数据集、每代一个 baseline 训练种子、固定 30 轮训练、36 张 pilot 图像、一个 primary probe backbone、固定随机投影和小 MLP。三种 probe seed 不等于三份独立数据，也不证明 baseline seed robustness。图像聚类 bootstrap 是描述性不确定性，不是 confirmatory p value。

全体 2032 张图像的文件哈希与解码像素哈希均唯一，train/val 无完全相同图像；尚未证明不同场景、序列、果园或感知近重复层面的独立性。局部训练视图排除了已记录的 6 条非法验证 polygon；官方 baseline loader 还对两组同类同 bbox 的训练 polygon 去重，而 probe 诊断保留合法 polygon。原始文件没有修改，差异和原行号映射均留存。

## 真正有增量的是哪种信息

**没有证据把新增 H 或 P 指认为独立贡献源；共同输入已经足以产生小幅改善。**P0 输入包含 original coefficient、预测框/scale/conf/class 和 P5 局部 descriptor，并不是只有一个常数。H 是 P3、stride 8，相对 P5 的 stride 32 更细；prototype P 为 stride 4，不能称 H 比 prototype 更高分辨率。

所有成员采用相同的 136→64→32 residual MLP、两个 32 维 learned-constant 槽与 15 轮 AdamW。GT 仅用于 train assignment/loss，ROI 来自预测框。没有 oracle-vector 回归，没有 val-instance fitting；验证控制从 train-only bank 按 predicted scale 取描述子。训练 shuffle 为每种子/每轮、同尺度、跨图像的双射，全部 45 张映射保存。

名义参数量一致并不意味着有效函数类完全相同；因此判定同时要求 true-source 对 P0 和相应 shuffle 的增量。该条件未满足。P3−C2 在 seed 2024 甚至为 `-0.001085`，区间 `[-0.001897,-0.000213]`。这反驳“只要双源训练 loss 更低，就说明双源机制成立”的推断。未通过 gate 也不是等价性检验。

本结果不属于用户定义的 CASE H/P/HP，也不应塞入“P0–P3 都不可学习”的 CASE NONE；更准确的限定描述是 **共同输入下可学习、新增 H/P 来源未被识别**。P0 的收益可能与额外 ROI/base 信息、容量、重新优化或 baseline 160 网格目标与 probe 640-native BCE 的差异有关。本轮没有分离这些因素，不能直接宣称其中某一个就是原因。

## 最危险的 5 个最近邻与 novelty 边界

核查覆盖 30 个 primary works/official implementations，含用户指定的全部 21 项；主动检索覆盖 2024–2026 的 efficient/real-time、prototype、dynamic kernel、coefficient/basis-aware refinement、small-object 和 representation diagnosis。下面五篇阅读了 method details，完整 14 列矩阵、来源和额外 H 路线核查见 [NOVELTY_MATRIX.md](NOVELTY_MATRIX.md)。非深读条目的未确认字段明确标记，不用“没查到”证明不存在。

| 最近邻 | 已有机制与阻断的主张 | 本轮最多保留的区别 |
|---|---|---|
| [YOLACT](https://arxiv.org/html/1904.02689) | 共享 prototype 与 coefficient assembly，并已讨论系数预测困难 | native 稳定性审计、冻结 decoder 的 utilization 诊断 |
| [BlendMask](https://arxiv.org/html/2001.00309) | ROI bases 与空间 attention blending，覆盖局部 basis 融合动机 | 维持单个 K-vector，不加入空间 coefficient field |
| [SipMask](https://www.ecva.net/papers/eccv_2020/papers_ECCV/papers/123590001.pdf) | 子区域系数与 box-aligned features，已针对空间分离不足 | 不增加子区域向量，原 32 维表示保持冻结 |
| [K-Net](https://papers.nips.cc/paper/2021/file/55a7cf9c71f1c9c495413f934dd1a158-Paper.pdf) | mask-group feature 回读并迭代更新 kernel | 单步 existing-coefficient residual，无 kernel interaction |
| [SparseInst](https://arxiv.org/html/2203.12827) | instance activation pooling 后预测 mask kernel | 复用已训练 detector/basis，做受控小残差诊断 |

这些计算区别没有自动变成 scientific novelty。本轮恰好缺少 source-specific 和完整质量证据，不能以“更小、更简单”代替效果证明。若以后转向 H，必须继续正面对照已深读的 [PointRend](https://arxiv.org/html/1912.08193)、[RefineMask](https://arxiv.org/html/2104.08569) 和 [Mask Transfiner](https://arxiv.org/html/2111.13673)；后者已有 fixed-detector oracle refinement 诊断。

2026 检索也发现同一 YOLO8/11/26 orchard 比较工作，阻断“首次三代 orchard benchmark”的表述。[Cross-generation orchard study](https://arxiv.org/abs/2608.23636)。另对 [D-FINE-seg](https://arxiv.org/pdf/2602.23043) 的全文和官方实现进行了版本区分核查，源码及 hash 留存于 literature/source_audits；它进一步限制轻量 mask embedding/dot-product head 的宽泛 novelty 主张。

**绝对不能声称：**首次 prototype segmentation、首次让 kernel 看 feature、首次系数困难或 mask representation diagnosis、首次 high-res refinement、首次 oracle 引导细节修正、首次三代 YOLO orchard 比较；也不能声称已证明 prototype-context bottleneck、dual-source complementarity、conditioning 因果机制、普遍小目标四倍瓶颈、跨三个模型可学习性、三环境工程收益或可部署 oracle 上界。

**当前允许声称：**在明确的数据、训练配方和匹配条件下，三个 clean checkpoint 保留经过 native 精度验证的稳定系数 gap；一个冻结 YOLO11 的小残差映射可在留出图像上取得小幅平均 matched-mask IoU 改善；加入本轮 H/P descriptors 没有取得受控制支持的独立增量；matched-IoU 改善与完整质量指标之间存在实测断裂。这是一组有价值的诊断及否证结果，尚不是新模块论文的成立证据。

## 最小最终模块、工程 fallback 与投入建议

**当前不推荐最终新模块。**不要把 P2/P3 扩成 attention、Transformer、多级 refinement 或 normalization 系统，也不保留双源模块来维持叙事。MAINLINE-A 的 numeric、cross-model 和有限 learnability 项通过，但 source-specific controls 与完整 AP/quality 项失败，novelty 也不足；因此不进入大规模 final training。

若将来因独立工程需求重新立项，最小可检验对象应是 P0 或现有 coefficient head 的单因素训练/目标对齐对照：冻结相同 detector 和 basis，比较相同 native mask objective 下的 existing head 与 tiny residual，先分离 objective、base ROI 信息和额外容量。此处只是排错方向，不是本轮已发现的新机制，也不是建议现在继续追加训练。未来仍须预先固定匹配、AP75/small/boundary 与成本门槛；失败后停止，不增加 H/P 模块掩盖原因。

工程 fallback 是保留 clean native baseline 与本轮可复用诊断/审计工具链。当前没有充分证据推荐以任何 probe 替换 native 输出。只有未来在 Mega Blueberry、MinneApple 和第三个独立环境中稳定改善 AP75/small quality，并证明部署成本可接受，才有资格重新考虑 engineering paper；本轮没有 MinneApple 或第三环境结果，MAINLINE-B 未成立。

**不值得基于当前 H/P proposed mechanism 继续投入完整结构实验。**STOP 的对象是这条结构/发表主线，已成立的 native-feasible gap 与否证证据保留。若后续研究重新启动，应先提出可证伪的新问题，而不是围绕本轮小幅 AP 正数补模块。

## 资源、实现修复与证据索引

三次成功 baseline 训练的 trainer-call 耗时为 `32.54 / 30.65 / 46.51 min`，峰值 allocated VRAM 为 `2086.4 / 1970.5 / 2309.3 MiB`。21 个 probe 同时堆叠、保持独立参数和 Adam 状态，正式训练耗时 `2911.51 s`（48.53 min），峰值 allocated VRAM 为 `1196236800 bytes`。失败尝试的时间未混入成功训练成本；其日志和检查点均保留。

部署测量使用 RTX 4060 Laptop 8GB、float32、batch 1、未 fuse 模型；native 模型含 `2,842,998` 参数，THOP 估计 `9.7866752 GFLOPs`。每模式 12 张固定图像×3 次同步测量，3 次预热；包括 CPU letterbox、transfer、detector、NMS、必要 ROI/投影、probe 和 GPU mask assembly，不含磁盘读和 CPU RLE 编码。计时期间没有其它研究 GPU 任务，桌面进程仍存在。固定投影、标准化和 ROI 开销另列，不能只报 MLP FLOPs。所有 21 个小权重切片驻留，投影缓存逐模式累积；微小显存差不解释成精确的模块专属差值。

此单次按模式顺序的桌面测量有频率/调度波动，未建立严格配对的延迟置信区间。P2 的均值 `36.224 ms` 略低于 native，不足以声称加速；P1 的 `41.455 ms` 也不构成跨部署后端的固定开销结论。在线/离线一致性核对在计时前完成，8 模式共 3076 个掩码逐像素相同。完整 mean/median/p95/FPS/VRAM 和 GPU 状态在 `artifacts/benchmark/resources.json`。

首个 probe 尝试在第 4 轮主动停止：CUDA interpolation backward 的非确定性使数学上相同的 P0/C3 轨迹偏离。其第 3 轮检查点、部分第 4 轮日志、非零退出及 source snapshot 留存在 `artifacts/failed_probes/nondeterministic-native-backward_20260919T021245/` 和对应 run 目录，未用于 held-out 结果。修复保留原生 CUDA 前向，仅以固定顺序的 separable adjoint 计算相同数学梯度，并启用 deterministic algorithms/cuBLAS workspace。CPU float64 梯度对照最大误差 `3.55e-15`，120 个 train-only 优化步骤逐步 null equality 通过；正式训练从原种子重启，全部 15 轮及 held-out equality 通过。未改变 loss、descriptor、seed、epoch、阈值或 subgroup。

其它启动问题（settings key、缺少 Polars、下载尝试、UTF-8 输出、YOLO26 end-to-end flag）及恢复过程见 [EXECUTION_JOURNAL.md](EXECUTION_JOURNAL.md)。依赖只安装于 P1B runtime；只读使用既有解释器，P1A 环境和资产未改。早期准备阶段尚无可解析 Git HEAD，保留了其文件/config hash，并如实记录这一 provenance 限制；后续训练、诊断和评估均有提交、diff、CLI、日志与 source snapshot。

| 交付内容 | 位置 |
|---|---|
| 冻结实验与输入 | `PROTOCOL.md`, `config.json`, `artifacts/input_freeze.json`, dataset/sample manifests |
| 数值三层区别、原 blocker、三模型闭合 | [NUMERIC_CONTRACT.md](NUMERIC_CONTRACT.md), `artifacts/oracle/` |
| 全量结果与可机读汇总 | [RESULT_TABLES.md](RESULT_TABLES.md), `artifacts/analysis/results_digest.json` |
| 原始预测与 full AP | `artifacts/evaluation/*/*_predictions.json.gz`, `*_ap.json`, `*_matched.csv` |
| 配对控制与判定 | `artifacts/analysis/probe_contrasts.json`, `probe_decision.json`, `ap_translation.json` |
| 30 项文献、检索记录、官方代码核查 | [NOVELTY_MATRIX.md](NOVELTY_MATRIX.md), `artifacts/literature/` |
| 图形 | 三种子 matched IoU/AP（原资产，本次未收录：`artifacts/analysis/probe_vs_AP.png`）, 固定留出实例（原资产，本次未收录：`artifacts/analysis/heldout_examples.png`）, `artifacts/analysis/*_path.png` |
| 环境与完整性 | `artifacts/environment_final.json`, `integrity_closure.json`, `split_integrity.json` |
| 每次运行的 CLI/hash/source/diff/stdout/stderr | `artifacts/runs/`, `artifacts/run_registry.jsonl` |
| 最终判定与文件索引 | `artifacts/analysis/final_verdict.json`, `artifacts/artifact_index.json` |

完整性审计为 **PASS**：核对了 512 个 P1A 资产、P1A Git HEAD/clean 状态、2032 份原始图像/标签及局部标签、冻结协议/config、三个初始与最终权重、30 轮记录和 15 轮 probe。P1A HEAD 仍为 `752c4048f4eea14e18da11f25a9cd960366f1afb`。本轮全部新资产位于当前 P1B 目录，没有读取 test outcome。最终文件索引单独排除自身、追加型 run registry 及正在写入索引的 run；原始输入/runtime/upstream 由各自 provenance 记录覆盖。

**STOP**
