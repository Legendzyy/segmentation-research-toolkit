> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../../docs/PROVENANCE.md)。

# 现有模块组合与成熟方法适配的独立复盘

2026-09-30。此复盘依据 P1D、ENG02、ENG03、ENG04 的正式报告及 ENG04 同 seed 配对表；百分点均指 mask AP 的绝对差值×100。不同训练时长、模型大小、seed 或阶段来源不能合并为同一因果比较。没有访问 test。

## 我们是否真正试过“成熟方法组合后在社区 benchmark 上公平赢强基线”？

**没有完整试过。** 已做的是自有 Blueberry development 上的有限工程适配：ENG02 以原生 YOLO11n 与较大 YOLO11s 做容量/尺度对照，并试普通 feature-MSE KD；ENG03 试直接输出 KD、任务门控与简单 output+feature 相加；ENG04 做简化的 CrossKD 核心路径适配、GT-linked quality 监督和任务分工组合。这些并非一个公开成熟方法的忠实复现＋几个有归因设计的模块组合，也没有在第二个公开 development 数据集及完整成熟近邻对照上取得结果。P1D 有较系统的头部重训/系数残差阶乘实验，但其问题与60epoch KD 主线不同。

## 是否有组合超过其原始 A？有，但不能偷换“有效论文方法”

| 阶段/组合 | 合理的同协议 A | 主 AP 结果 | 解释边界 |
|---|---|---|---|
| P1D M1：已有 coefficient head 重训＋mask ratio1 | 配对 M0 | 三 seed 均值 **+0.5253 pp**；三 seed 在 AP/AP75/small 对 M0 同向 | 这是最清楚的简单工程信号；但比同总训练预算 fresh75 的均值 AP75 **−0.3101 pp**，创新性也弱。不能称全面胜出强基线。 |
| P1D M3：head 重训＋系数残差＋mask ratio1 | 配对 M0；fresh75 强对照 | 均值对 M0 **+0.5162 pp**，对 fresh75 **+0.4525 pp** | **A+B+C 的总 AP 确实大于原始 A**；但 M3 的 AP 均值没有超过更简单的 M1（约 −0.0091 pp），不证明残差有互补贡献；对 fresh75 AP75 −0.1961 pp，seed42 small 负向、seed2024 thin 触及失败门槛。 |
| ENG02 A2：YOLO11s@640 | YOLO11n A0@640 | 单 seed AP **+0.6854 pp**、small +3.5842 pp | 证明容量空间，不是同部署成本的方法组合。A1@896 是分辨率改变，不能作为等成本模块增益。 |
| ENG02 K1：普通 feature-MSE KD | A0 | 单 seed AP **+0.1433 pp** | 探索性正数，未过事前门槛；后续 ENG03 同 seed2024 K1 对 native 仅约 +0.0316 pp。 |
| ENG03 F0：输出 KD＋feature-MSE 简单相加 | 同 seed D0 | seed2024 **−0.3751 pp** | 已经试过“直接 A+B”，结果未超过 A；不能说所有更有依据的组合都被否定。 |
| ENG04 I1：移除 I0 的 teacher 类别 BCE，保留 GT-linked box/mask | 同 seed I0；原生 N0 | seed42 对 I0 **+0.4038 pp**；对 N0 仅 **+0.0170 pp**，低于 D0 | 消融证明 I0 的教师分类项在该开发 seed 有副作用，不证明 I1 是强方法。 |
| ENG04 J0：D0 检测监督＋I1 mask 监督 | 同 seed D0/N0 | 两个新确认 seed 对 D0 **−0.6491 / +0.5145 pp**，对 N0 **−0.5327 / +0.4379 pp** | 完整组合两粒确认换号；AP90 也换号，无法宣称稳定优于 A。开发 seed42/128 另列，不混成独立确认。 |

所以“所有组合都没涨过”不准确；“已经找到一个公平、稳健、可归因且有区别度的 A+B+C 新方法”也不准确。P1D M3 对弱/中等 A 有主 AP 增益，但未证明 B+C 的独立价值和强对照的全面优势；ENG04 J0 在一半已见 seed 里有正数，但冻结后两粒确认不稳定。

## 对下一种研究组织方式的判断

可以从成熟方法出发，不必先挖出完美诊断信号再允许组合。可行的完整路线是：先选社区可复核的数据/评价及真正强的开源 baseline；忠实复现成熟方法 A 和简单的 B，再基于果实密集小实例的具体局限设计**有署名、有计算差异**的适配 C；同模型、数据、输入、训练预算比较 `baseline`、`baseline+A`、`baseline+B`、`baseline+A+B`、`baseline+A+B+C`。如果完整组合赢而组件无法解释，仍只能主张系统经验效果，不能伪称每个模块都有独立贡献。作者应引用原模块，明确新意落在适配、交互、约束或评估发现，而不是把他人的设计改名为原创。

在当前项目上，不建议直接用已看过的 Blueberry val 数值拼一个“最优包”：已经看过的候选和 seed 是开发资料，不能充当新的独立验证。若重开，应先做一轮最新文献/代码许可与 benchmark 审查、冻结一个组合和预算，再用未参与设计的新 seed/外部 development 公平验证。P1D M1 是值得保留的**简单强工程参照**；其历史75epoch 结果不能直接拿来和 ENG04 60epoch 排名。P1D M3 可作为“组合有正主 AP 但互补性未证实”的反例教材，不应因曾涨点就直接包装论文。

## 数值出处

- [P1D 最终报告](../../../diagnostics/p1d_engineering_qualification/FINAL_REPORT.md)与[三种子资格表](../../../diagnostics/p1d_engineering_qualification/QUALIFICATION_RESULTS.md)：M0/M1/M2/M3、fresh75 的不同对照。
- [ENG02 裁决](../../eng02_scale_capacity_small_object/ENG02_VERDICT.md)：A0/A1/A2/K1/K2 的 seed42 full254。
- [ENG03 最终报告](../../eng03_instance_quality_transfer/FINAL_RESEARCH_REPORT.md)：同 seed2024 的 F0/D0/K1/N0，及 seed128/2024 配对。
- [ENG04 原始配对表](../results/PAIRED_COMPARISONS.csv)及[确认裁决](CONFIRM_J0_V1_DECISION.md)：J0/D0/N0 开发与新 seed 确认；本复盘未重算任何历史大文件哈希。
