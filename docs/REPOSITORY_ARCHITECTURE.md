# 沿用原生阶段架构

这里整理原项目已经采用的组织方式。公开版没有新增阶段生成器，也不要求把各阶段文件改成同一种模板。

原项目用 `diagnostics/` 放离线诊断与机制归因，用 `engineering/` 放围绕问题开展的训练和方法迭代。两者不是严格流水线：诊断可以为工程设计提供依据，工程结果也会推动下一轮诊断。阶段独立保存自己当时的定义和结论，下一阶段引用历史结果而不回写。

| 要解决的协作问题 | 原生文件/目录 | 可直接参考的原件 |
|---|---|---|
| 现在研究什么、什么已经完成 | README、最终报告 | [ENG04 README](../engineering/eng04_problem_led_quality_transfer/README.md) |
| 问题、预算和比较方式怎样约定 | PROTOCOL、RESEARCH_CHARTER、ENGINEERING_CONTRACT | [ENG01 契约](../engineering/eng01_semantic_detail_boundary/ENGINEERING_CONTRACT.md) |
| 模块的具体计算是什么 | METHOD_SPEC、IMPLEMENTATION_CONTRACT | [ENG03 方法](../engineering/eng03_instance_quality_transfer/METHOD_SPEC.md) |
| 实验用什么数值配置 | configs/ 中的分版 JSON | [ENG04 确认配置](../engineering/eng04_problem_led_quality_transfer/configs/CONFIRM_J0_V1.json) |
| 一轮实验后为什么继续/调整 | analysis/ 下的决策文件 | [ENG03 第二轮决策](../engineering/eng03_instance_quality_transfer/analysis/DEVELOPMENT_V2_DECISION.md) |
| 数值和图怎样集中对照 | results/、RESULTS_MASTER、配对表 | [ENG01 矩阵](../engineering/eng01_semantic_detail_boundary/results/SEED42_MATRIX.csv) |
| 什么实际执行了，遇到什么错误 | EXECUTION_JOURNAL | [P1F 日志](../diagnostics/p1f_thin_prototype_attribution/EXECUTION_JOURNAL_P1F.md) |
| 最后能写什么、证据缺什么 | paper/、FINAL_REPORT | [ENG04 claim 对照](../engineering/eng04_problem_led_quality_transfer/paper/CLAIM_EVIDENCE.md) |

开始自己的研究时，选择最相近的阶段作参照，在自己的新目录里写下场景、baseline、benchmark、候选设计和对照矩阵。沿用这些文件的职责，重新确定自己的配置和协议；把未运行的结果留空，不复制历史数值或 FROZEN 状态充当自己的结果。

原项目还使用 `src/`、运行队列、`runs/`、权重、评价缓存、样本 manifest 和数据接口。它们在本次公开版中**没有迁移**，因此这里只提供研究组织结构与文档资产。要训练，需要另接自己的训练器、数据接口、环境和评价实现，并完成同协议 baseline；原文命令只说明历史执行方式。

阅读历史文件时保留两点上下文：P1E/P1F 原目录曾继承前阶段文件，本次只收录对应阶段主件（带 `_P1E` / `_P1F` 后缀）；阶段报告中的源码 hash、权重 hash 和数据 manifest hash 是历史身份记录，不表示相关资产已附包，或可以从 hash 恢复文件。
