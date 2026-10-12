> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# ENG03 最终研究报告（PAUSE-B 阶段交付）

**结论：`NO-SUPPORTED-METHOD-AFTER-BOUNDED-DEVELOPMENT`。** 在 Blueberry development val 的固定 full254/1803-GT、input640、预定最后 checkpoint 口径下，本轮实现并检验了实例 GT 对应的输出蒸馏、按任务选择、代表 anchor 修订及与普通 feature KD 的加法组合。目前没有得到可复验、优于同预算原生训练的完整预测方法。研究问题仍有价值，但现有设计不能写成已成立的论文主方法。按用户授权的研究节点 **PAUSE-B** 停止本分支新增训练；这不是磁盘、算力或权限障碍，也不代表所有实例级蒸馏无效。

## 问题、实际实现与前史使用

研究问题是如何把较强 teacher 的实例质量优势转化成轻量 YOLO11n-seg 的完整实例预测收益，而不只提升已共同匹配实例的局部 mask。ENG02 只读历史表中 YOLO11s teacher A2 比 native n A0 高 .6854 pp mask AP、3.5842 pp small AP；ENG03 的 score-.25 同类 box 诊断发现 21 个 A2-only GT 中 20 个在 A0 有低于阈值的同类候选。这提示候选分数/集合与局部 mask 的连接值得检验，但不是 AP 的因果分解。P1C 的低置信度、面积资格与排序分析，以及 P1D M1 在其不同协议下的正向 AP，均被保留为设计/比较边界，没有跨表直接相减。

我们在同一增强图像上用学生 TAL positive anchor 的 GT 身份对应 teacher 的同格响应；比较 true-class sigmoid、解码 box 和公共栅格上渲染的实例 mask，保留学生原生 GT loss。D0 对所有合格 GT 直接蒸馏；Q0 以 detached 的 task-specific teacher 优势开关监督；M0/C0 补齐四格；R0 改变 mask 代表 anchor 的预定选择；F0 直接叠加普通三层 neck feature-MSE。teacher、蒸馏逻辑与 F0 适配器仅在训练中使用，部署为原生学生图。数值审计验证了 native no-op、梯度路径、teacher 冻结、空 GT 和部署输出一致性；烟测自动 val 没有用于科学选择。公式和路径见 [METHOD_SPEC.md](METHOD_SPEC.md)，冻结配置在 `configs/`。

## 主要结果及反证

以下 AP 均为 0–1 原值；差异写为百分点，来源是独立 full254 评估而非训练自动 val。每个正式模型固定训练 60 epoch、使用预定最后 checkpoint。`RESULTS_MASTER.csv` 给出 AP50/AP75/AP90/尺度指标、来源和可比性。

| 对照 | 结果与解释 |
|---|---|
| D0 vs 原生 N0，seed128 | .839156 vs .840163，D0−N0 **−.1007 pp**；AP75 +.6494、AP90 −1.1638、small AP +.2090 pp。 |
| D0 vs 原生 N0，seed2024 | .844379 vs .842095，D0−N0 **+.2284 pp**；small AP −.6098 pp。两种子的 overall 方向相反，描述性平均仅 +.0639 pp。 |
| D0 vs K1 feature-MSE，seed2024 | .844379 vs .842411，D0 +.1968 pp；只有一个本轮完全同预算 seed，不能称稳定优于普通 KD。 |
| Q0/C0 vs D0，开发 seed42 | Q0 .841307、C0 .838899、D0 .842408；按任务选择未带来 overall AP 优势。 |
| M0 vs D0 | seed42 small AP +1.8292 pp、overall −.0126 pp；seed128 small AP **−.2780 pp**、overall +.0638 pp，核心小目标现象反转。M0_s2024 按预登记屏障零 epoch 跳过。 |
| R0 vs D0，seed2024 | .840318 vs .844379，overall −.4062 pp、small −1.0731 pp；停止扩种。 |
| F0 简单相加 vs D0，seed2024 | .840628 vs .844379，overall −.3751 pp、AP75 −.4381 pp；停止扩种。 |

seed128 D0 相比 N0 的 score-.25 同类 box coverage 为 1727 vs 1715 GT，1700 个对齐共同 GT 上平均 mask IoU +.000695、boundary F +.000675，但完整 AP 更低。这直接说明固定 operating point 与条件质量不足以代表完整 AP；候选排序、置信度和高 IoU 结局都可能参与，当前证据不识别唯一成因。[配对图](analysis/PAIRED_NATIVE_D0.png) 和 逐实例数据（原资产，本次未收录：`analysis/n0_s128_instance_evidence.csv`）保留了这种不一致。Q0/M0/R0/F0 的负向证据意味着继续原样调权重或补第三种子的信息价值低；不把某个 seed 或某个阈值当作普遍定理。

## 决策、预算与证据边界

预先记录的后续 K1_s128 调度门槛要求 D0−N0 overall AP ≥+.10 pp、AP75/AP90 至少一个为正、small AP 不低于 −1.0 pp。seed128 的 overall AP 为 −.1007 pp，故门槛失败，**K1_s128 不启动**。两种子符号相反也使 D0 不能作为论文 finalist。R0 和 K1 的第一次工程中断均完整保留，后续成功运行从冻结初始权重全新开始，没有声称严格 checkpoint 连续。累计 12 个完成的 60-epoch 正式任务，37.601 小时完成任务的共享 GPU 训练进程时间，另有约 29+2 epoch 的失败部分计入预算；均低于 24 单位/96 小时上限。当前 E: 可用约 22 GiB，高于 8 GiB 保留线；`runs` 逻辑约 1.68 GiB，数据视图中的图像是 NTFS 硬链接，不重复当作新增占用。无 test 读取，也未修改历史阶段或 ICASSP。

最接近的公开方法已有 instance/response/feature、cross-head 等监督思路（见 [NEAREST_PRIOR_AND_CLAIM_DIFF.md](NEAREST_PRIOR_AND_CLAIM_DIFF.md)）。本轮没有完成忠实成熟近邻适配、MinneApple development、P1D M1 同预算再训练或 isolated latency。因此**不能声称**优于最近邻、跨数据泛化、稳定小目标收益、训练成本公平优势或投稿级新方法。这些是未完成的比较，不是它们的失败结果。seed42 A0/K1 与本轮 seed128/2024 控制的训练来源也不得混为配对复验。

当前可以肯定地写：GT-linked dense-output supervision 的训练路径可实现；teacher 优势与完整预测收益不等价；本轮多个合理监督组织在同一开发协议下没有形成稳健主指标优势。不能写“实例协调迁移已经成功”或“普遍 KD 无效”。要重新寻求投稿方法，最有信息量的下一步是先提出**明确针对最终候选分数/高 IoU 失配的单一可证伪训练机制**，并在同预算原生 N0 与简单 D0 上做一个预注册单 seed 完整 AP 对照；只有主指标及机制证据同时有实质信号，再按 adaptive policy 补第二 seed、忠实成熟近邻和外部开发。该设计尚未实施，不能当作本轮结果，也不能保证一次实验就足以投稿。

阶段状态：`RESEARCH_DIRECTION=OPEN`；`METHOD_IMPLEMENTED=YES`；`DISTINCTION_FROM_NEAREST_PRIOR=DESCRIPTIVE_ONLY`；`MAIN_AP_EVIDENCE=NOT_SUPPORTED`；`IMPORTANT_TRADEOFFS=DOCUMENTED`；`PAIRED_REPLICATION=NATIVE_2_SEEDS_MIXED / M0_2_SEEDS_REVERSED`；`EXTERNAL_DEVELOPMENT_EVIDENCE=NOT_RUN`；`EFFICIENCY_CERTIFICATION=NOT_RUN`；`CLAIMS_READY_FOR_WRITING=LIMITED_OBSERVATIONS_ONLY`；`MISSING_SUBMISSION_EVIDENCE=POSITIVE_METHOD,FAITHFUL_NEIGHBOR,EXTERNAL,ISOLATED_COST`；`NEXT_HUMAN_DECISION=ACCEPT_PAUSE_B_OR_AUTHORIZE_A_NEW_MECHANISM_FOCUSED_STAGE`。
