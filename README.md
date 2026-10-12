# Segmentation Research Toolkit

这里公开的是一个实例分割研究项目的**原生研究记录**：从具体问题出发，在 YOLO 分割基线上做结构与训练机制改进，记录每次设计、实验、消融、结果与下一步判断。供学弟学妹参考真实科研怎么推进。

主体来自原项目的 **P1A–P1F、ENG01–ENG04 十个阶段**，沿用原目录名。包含 95 份原始文档、17 份冻结配置、10 张真实汇总表和 5 张原始结果图。既保留有价值的正向信号，也保留错误假设、失败尝试和没有完成的验证。正文数值没有重编，没有虚构教学实验。

## 先看工程研究怎么做

研究主线是：**具体问题场景 → 合适的强 benchmark 与新近强基线 → 定位实际失效模式 → 有针对性的架构/训练机制 → 对比与消融 → 解释模块贡献和质量、成本取舍 → 组织论文。**

先读 [按原项目推进研究](docs/START_HERE.md)，再读 [工程论文设计思路](docs/PAPER_DESIGN_WORKFLOW.md)。后者是依据本项目整理的编辑说明；下面的阶段文件才是当时的原始记录。

| 研究问题 | 实际设计与原始入口 | 结果怎么看 |
|---|---|---|
| 增加细节信息和边界监督，能否改善实例 mask？ | [ENG01 六变体结构/监督契约](engineering/eng01_semantic_detail_boundary/ENGINEERING_CONTRACT.md) | [单 seed 矩阵](engineering/eng01_semantic_detail_boundary/results/SEED42_MATRIX.csv)、[多 seed 复验](engineering/eng01_semantic_detail_boundary/results/REPLICATION_TABLE.csv)、[完整报告](engineering/eng01_semantic_detail_boundary/FINAL_ENGINEERING_REPORT.md) |
| 小目标还有多少提升空间？先加分辨率、容量还是蒸馏？ | [ENG02 问题剖面](engineering/eng02_scale_capacity_small_object/ERROR_PROFILE_ENG02.md)、[筛选契约](engineering/eng02_scale_capacity_small_object/contracts/SCREENING_CONTRACT.md) | [容量/尺度与 KD 裁决](engineering/eng02_scale_capacity_small_object/ENG02_VERDICT.md) |
| 强教师的分类、框和 mask 信息怎样传给轻量学生？ | [ENG03 实例质量迁移方法定义](engineering/eng03_instance_quality_transfer/METHOD_SPEC.md) | [18 行结果主表](engineering/eng03_instance_quality_transfer/RESULTS_MASTER.csv)、[强对照决策](engineering/eng03_instance_quality_transfer/analysis/STRONG_CONTROL_V1_DECISION.md)、[报告](engineering/eng03_instance_quality_transfer/FINAL_RESEARCH_REPORT.md) |
| 目标对应关系、质量权重与任务分工，哪一项真有用？ | [ENG04 问题与设计迭代](engineering/eng04_problem_led_quality_transfer/EVIDENCE_AND_METHOD_LOG.md)、[方法定义](engineering/eng04_problem_led_quality_transfer/METHOD_SPEC.md) | [模块组合复盘](engineering/eng04_problem_led_quality_transfer/analysis/METHOD_COMBINATION_REASSESSMENT_20260930.md)、[最终确认](engineering/eng04_problem_led_quality_transfer/analysis/CONFIRM_J0_V1_DECISION.md) |
| 更细的特征来源、更密的 prototype 输出，贡献如何分开？ | [P1F 六变体 factorial 实现契约](diagnostics/p1f_thin_prototype_attribution/FACTORIAL_IMPLEMENTATION_CONTRACT.md) | [source × lattice、插值与算力控制](diagnostics/p1f_thin_prototype_attribution/FINAL_REPORT_P1F.md) |
| 简单机制是否已经解释了复杂模块的收益？ | [P1D 头部特化契约](diagnostics/p1d_engineering_qualification/SPECIALIZATION_CONTRACT.md) | [M0/M1/M2/M3 与 fresh75 对照](diagnostics/p1d_engineering_qualification/FINAL_REPORT.md) |

不必先读完所有诊断。做架构改进可从 ENG01 开始；做蒸馏可从 ENG02–04 开始；遇到“局部指标很好、完整 AP 不涨”时，再读 P1B/P1C/P1F。全部阶段见 [诊断索引](diagnostics/README.md)和[工程索引](engineering/README.md)。

## 原仓库的组织方式

```text
diagnostics/
  p1a_coef_refit/                     # 系数拟合与数值实现
  p1b_publishability_triage/          # 可学习性、对照与完整 AP
  p1c_objective_alignment/            # 训练目标与部署评价
  p1d_engineering_qualification/      # 头部特化与同预算强对照
  p1e_structural_bottleneck_triage/    # thin 结构瓶颈与下一阶段蓝图
  p1f_thin_prototype_attribution/     # source × lattice 归因
engineering/
  eng01_semantic_detail_boundary/     # 细节分支、注意力、边界监督
  eng02_scale_capacity_small_object/  # 容量、分辨率与 feature KD
  eng03_instance_quality_transfer/    # 输出 KD 与质量选择
  eng04_problem_led_quality_transfer/ # 对应关系、权重与任务分工
docs/                                # 本次整理的阅读入口与论文思路
evidence/NATIVE_SOURCE_MAP.json       # 每份原件与公开文件的 hash/改动记录
```

阶段内部保留自己的 `PROTOCOL` / `RESEARCH_CHARTER`、方法定义、`configs/`、`analysis/`、`results/`、`paper/`、`EXECUTION_JOURNAL`。文件名没有强行统一，旧阶段也没有被改成新模板。怎样借用这套组织方式，见 [原生架构与复用](docs/REPOSITORY_ARCHITECTURE.md)。

## 使用范围

可以直接阅读、复用研究组织方式、方法表述和消融设计；这是研究档案的精选公开版，**尚不具备独立训练复现条件**。未附训练器、数据/标注、权重、预测缓存、样本清单及上游第三方源码。原记录中的运行命令和路径保留为历史背景；缺失依赖不会靠执行这些命令自动补齐。

历史 Blueberry full254 数值属于项目 development 协议，不是社区官方 benchmark 排名。本项目没有完成“强公开 benchmark 上稳定胜出”的完整证据链；这项缺口在原报告里保留。旧报告中的 GO/STOP、预算和授权都属于当时阶段，不是要求读者照搬的通用规定。

发布前只做资料核对，没有重跑科研实验。检查公开文件完整性可运行 `python tools/verify_archive.py`（Python 3.10+，标准库）。详细来源、改动及未收录内容见 [发布说明](docs/PROVENANCE.md)。已明确排除的在研论文材料不在本仓库发布与许可范围内。

本仓库公开的自有文档与维护脚本采用 [MIT](LICENSE)。保留原作者与上游方法的署名；引用既有模块不改变它们的来源和许可。
