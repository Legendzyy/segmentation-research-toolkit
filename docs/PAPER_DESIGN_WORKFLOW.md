# 从具体问题到工程论文：本项目的设计思路

本页定义工程研究的组织原则，不增加历史实验结论。相关原件： [ENG01 论文主线蓝图](../engineering/eng01_semantic_detail_boundary/PAPER_MAINLINE_BLUEPRINT.md)、[ENG03 论文蓝图](../engineering/eng03_instance_quality_transfer/paper/PAPER_BLUEPRINT.md)与 [ENG04 模块组合复盘](../engineering/eng04_problem_led_quality_transfer/analysis/METHOD_COMBINATION_REASSESSMENT_20260930.md)。

## 主线：场景、强底座、实际问题、针对性改进

工程型方法研究可以从一个具体应用场景出发，选择有说服力的 benchmark 和先进、成熟的 baseline，在真实错误上做架构或训练机制优化，再解释模块贡献与 trade-off。研究的主体是问题与解决方案，协议、日志和审计负责支撑它。

基线选型优先考察新近且成熟的同任务实现。YOLOv8、YOLO11、YOLO26 等系列属于候选范围，不构成本仓库的性能排名。选定时要核对任务分支、公开实现、权重、训练配方和成本：版本更新值得优先关注，任务内足够强的实际结果才确定主 baseline。当前可运行移植固定 YOLO11n-seg，不能将它的结果改写成更新底座的已验证效果。

benchmark 应能让同行理解并复核任务难度、数据划分、指标和对照。应用数据可以支撑场景价值；是否已完成公开 benchmark 验证要另行说明。本项目的 Blueberry full254 是内部 development 评价，原生 [ENG04 资产审查](../engineering/eng04_problem_led_quality_transfer/analysis/MINIMAL_PAPER_ASSET_REVIEW.md)明确记录了强公开 benchmark、外部配对等缺口。

## 从错误现象提出可实现的机制

先说明 baseline 在什么条件下出错：小目标漏检、相邻实例混淆、轮廓损失、形状破碎、排序失真，或质量与成本的冲突。接着提出为什么一个具体改动可能改善它。允许先做有依据的组合探索；探索结果决定后续机制解释的强度。

本项目有三类实际例子：

| 设计问题 | 原项目怎样落实 | 应追问什么 |
|---|---|---|
| 细节/边界信息是否不足 | ENG01 指定 detail 来源、融合层、门控与训练期边界监督 | 改善来自特征来源、注意力、额外参数还是辅助目标？ |
| 小模型是否有能力空间 | ENG02 比较模型容量与输入尺度，再尝试强教师 KD | 教师优势是否可迁移？额外训练成本换来了什么部署收益？ |
| 输出监督是否传错或传得不合适 | ENG03–04 明确对应关系、任务损失、质量选择和有效监督量 | 真正改变的是教师目标来源、监督强度，还是不同任务的干扰？ |

方法描述要能回答：模块接在哪里，输入/输出是什么，计算怎样发生，训练与推理有什么区别，额外参数/计算来自哪里。原始 [ENG01 契约](../engineering/eng01_semantic_detail_boundary/ENGINEERING_CONTRACT.md)和 [ENG03 METHOD_SPEC](../engineering/eng03_instance_quality_transfer/METHOD_SPEC.md)就是已经填完的参照。

## 用消融讲清贡献，保留有依据的质量取舍

组合设计通常需要原生 baseline、单项模块、完整组合、去掉某模块，以及必要的简单强对照。矩阵由问题决定，不要求每个研究机械跑满所有组合。[P1F factorial](../diagnostics/p1f_thin_prototype_attribution/FACTORIAL_IMPLEMENTATION_CONTRACT.md)适合拆 source/lattice；[P1D](../diagnostics/p1d_engineering_qualification/FINAL_REPORT.md)适合判断复杂残差是否超过简单 head 重训。

“每个模块的贡献讲清楚”不意味着每个单模块必须独立涨点。它可能只在组合中发挥作用，可能专门降低延迟，也可能是在修复一个子群问题。相应地，实验要支持交互、效率或子群主张。若去掉模块没有可辨认损失，就不能仅凭结构图把它列成有效贡献。

质量与成本允许有取舍：例如为更少计算接受小幅精度变化，或为关键错误类型接受一定速度代价。先由应用需求说明取舍有何价值，再用完整指标和实际测量展示。历史阶段里的多项联合门槛属于当时协议，不是所有论文都必须“每个指标全部上涨”的规则；已完成阶段的判定也不能事后换门槛重写。

原生 [ENG04 最小资产审查](../engineering/eng04_problem_led_quality_transfer/analysis/MINIMAL_PAPER_ASSET_REVIEW.md)指出一个很具体的消融缺口：D0→J0 同时改变 mask 目标来源和质量权重，因此现有结果不能独立解释这两部分贡献。值得学习的是怎样发现缺口，以及下一次如何把它拆开。

## 让论文结构对应已有证据

论文可以按“场景中的实际困难 → baseline 的具体局限 → 针对性机制 → 公平对比 → 模块/交互解释 → 成本与适用范围”展开。方法贡献要区分引用的已有组件、自己的适配或组合，以及实验确认的效果。

工程改进不必先证明一个宏大理论，也不能只由若干模块名称组成。即使总 AP 上涨，也要检查强 baseline、预算差异和简单解释；如果创新主要在特定场景的适配，就准确写这项贡献。

失败阶段同样保留方法和过程。ENG01 的辅助边界监督、ENG03 的质量门控、ENG04 的任务组合都是真实尝试；记录它们不是要求以后停止创新，而是让下一次设计能利用已经得到的信息。现有证据支持到哪就写到哪，未完成项作为后续工作。论文分区或录用不能由使用新底座、模块数量或某个固定流程保证。
