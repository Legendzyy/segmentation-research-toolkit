# 原生工程阶段

四个阶段保留了从结构改进到蒸馏，再到针对具体监督问题调整设计的连续过程。

| 阶段 | 设计主线 | 先读方法 | 再读实验与判断 |
|---|---|---|---|
| ENG01 | semantic/detail 融合、MLCA、spatial gate、训练期 boundary head | [ENGINEERING_CONTRACT](eng01_semantic_detail_boundary/ENGINEERING_CONTRACT.md) | [六变体矩阵](eng01_semantic_detail_boundary/results/SEED42_MATRIX.csv)、[最终报告](eng01_semantic_detail_boundary/FINAL_ENGINEERING_REPORT.md) |
| ENG02 | n/s 容量、640/896 分辨率与 feature KD | [错误剖面](eng02_scale_capacity_small_object/ERROR_PROFILE_ENG02.md)、[筛选契约](eng02_scale_capacity_small_object/contracts/SCREENING_CONTRACT.md) | [KD 决策](eng02_scale_capacity_small_object/analysis/KD_SEED42_DECISION.md)、[裁决](eng02_scale_capacity_small_object/ENG02_VERDICT.md) |
| ENG03 | plain output KD、任务质量门控、rank 及 output+feature 控制 | [METHOD_SPEC](eng03_instance_quality_transfer/METHOD_SPEC.md) | [结果主表](eng03_instance_quality_transfer/RESULTS_MASTER.csv)、[最终报告](eng03_instance_quality_transfer/FINAL_RESEARCH_REPORT.md) |
| ENG04 | teacher-own 对应、质量权重、去除分类项、检测/mask 分工组合 | [设计日志](eng04_problem_led_quality_transfer/EVIDENCE_AND_METHOD_LOG.md)、[METHOD_SPEC](eng04_problem_led_quality_transfer/METHOD_SPEC.md) | [模块组合复盘](eng04_problem_led_quality_transfer/analysis/METHOD_COMBINATION_REASSESSMENT_20260930.md)、[最终报告](eng04_problem_led_quality_transfer/FINAL_REPORT.md) |

方法说明里的张量关系、目标、归一化和变体矩阵是具体研究资产。阶段的原始训练源码没有随本版公开，不能把这些目录视作可直接启动的训练包。局部正向结果与最终混合/负向结果均保留，不把它们压缩成“加模块都没用”或“组合已经成功”。
