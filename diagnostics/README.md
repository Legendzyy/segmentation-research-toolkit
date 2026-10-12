# 原生诊断阶段

这些目录保留当时的问题定义、实现/数值契约、结果与裁决。可以按遇到的问题选读，无须把诊断全套当作开始工程创新的先决条件。

| 阶段 | 实际问题 | 原生入口 | 阶段结果 |
|---|---|---|---|
| P1A | 固定 prototype 的系数重拟合是否说明表达空间不足 | [协议](p1a_coef_refit/PROTOCOL.md)、[mask 路径](p1a_coef_refit/MASK_PATH.md)、[报告](p1a_coef_refit/FINAL_REPORT.md) | 数值路径未闭合，不能直接做结构归因 |
| P1B | 稳定 oracle 的差距是否可学习、可形成完整 AP 收益 | [数值契约](p1b_publishability_triage/NUMERIC_CONTRACT.md)、[结果表](p1b_publishability_triage/RESULT_TABLES.md)、[报告](p1b_publishability_triage/FINAL_REPORT.md) | 有局部小增益，特异性与联合 AP gate 未通过 |
| P1C | 训练目标与部署路径错配，还是分辨率/容量造成现象 | [loss 路径](p1c_objective_alignment/LOSS_PATH_AUDIT.md)、[AP 诊断](p1c_objective_alignment/P1B_AP_DIAGNOSIS.md)、[报告](p1c_objective_alignment/FINAL_REPORT.md) | 一些工程信号，不支持独立 decode-alignment 方法 claim |
| P1D | 特化 head/系数残差是否超过简单方案及同预算强基线 | [特化契约](p1d_engineering_qualification/SPECIALIZATION_CONTRACT.md)、[报告](p1d_engineering_qualification/FINAL_REPORT.md) | M1 保留工程价值；复杂设计未通过完整资格检查 |
| P1E | thin 结构是否存在稳定 prototype 容量缺口 | [协议](p1e_structural_bottleneck_triage/PROTOCOL_P1E.md)、[报告](p1e_structural_bottleneck_triage/FINAL_REPORT_P1E.md)、[下一阶段蓝图](p1e_structural_bottleneck_triage/P1F_METHOD_BLUEPRINT.md) | 有限范围的 GO，进入验证和归因 |
| P1F | 更细 source / 更密 lattice 的增益能否独立归因并部署 | [factorial 契约](p1f_thin_prototype_attribution/FACTORIAL_IMPLEMENTATION_CONTRACT.md)、[报告](p1f_thin_prototype_attribution/FINAL_REPORT_P1F.md) | 局部信号可复验，候选未转成稳定部署收益 |

P1E/P1F 文件名中的后缀是原项目命名；继承自前阶段的重复主件没有再次拷贝。每个目录的日志、方法和原始表述保留，索引只负责定位。
