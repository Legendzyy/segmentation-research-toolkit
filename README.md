# Segmentation Research Toolkit

面向计算机视觉研究的**问题定义、机制分析、实验组织与证据交付骨架**。

这个仓库整理了已结束的实例分割研究阶段中的可复用经验：如何区分 oracle 空间与可部署收益，如何设计能够区分替代解释的对照，如何保留正负结果，以及如何把研究问题组织成一篇有证据支撑的论文。

它包含研究流程模板、方法设计笔记、失败案例练习、完整填写的教学示例，以及无需深度学习环境的阶段创建、配对汇总与审计工具。没有附带训练器、模型实现、数据集或权重；不构成历史实验的一键复现包。工具在合成夹具和公开的四行汇总表上验证，未重新运行历史训练或评价。

**第一次来，先读 [从零开始指南](docs/START_HERE.md)**：克隆、运行、预期输出、创建阶段及修改后的 CI 更新都有具体步骤。不熟悉术语时查 [术语表](docs/GLOSSARY.md)。

## 从哪里开始

| 你的需要 | 入口 |
|---|---|
| 跑通一次流程，知道模板怎样填 | [完整教学示例](examples/synthetic_study/README.md) |
| 学习失败与错误方向如何判断 | [五个历史案例与练习](docs/FAILURE_CASES.md) |
| 把一个具体问题组织成论文 | [论文设计工作流](docs/PAPER_DESIGN_WORKFLOW.md) |
| 借鉴机制诊断与最小对照 | [方法设计库](docs/METHOD_DESIGNS.md) |
| 看已结束研究留下了什么 | [历史结论与边界](docs/RESEARCH_LESSONS.md) |
| 搭建自己的科研工程 | [仓库架构与迁移指南](docs/REPOSITORY_ARCHITECTURE.md) |
| 统一 endpoint、coverage 与统计角色 | [评价契约](docs/EVALUATION_CONTRACTS.md) |
| 理解公开材料的来源与缺口 | [来源说明](docs/PROVENANCE.md) |

## 快速使用

需要 Python 3.10 或更新版本，仅使用标准库。下载并进入仓库根目录后运行：

```bash
python -m unittest discover -s tests -v
python tools/paired_summary.py examples/synthetic_study/paired_metrics.csv
python tools/manifest.py verify . RELEASE_MANIFEST.json
```

第二条使用完全虚构的教学表，预期均值为 +0.5 pp，2 正 1 负，不构成真实模型结论。第三条验证已发布文本，预期 PASS。真实历史聚合表示例可用 `python tools/paired_summary.py evidence/paired_confirmation.csv` 另行核对。详细字段与限制见 [工具说明](tools/README.md)。

新研究可以使用 GitHub 的 **Use this template** 创建自己的仓库，再运行 `python tools/new_stage.py diagnostics pilot01` 生成空阶段。先填写 `CURRENT_PROGRESS.md` 和实验协议，再向 `src/` 接入自己的模型、数据适配器和评价实现。空阶段配置为 `DRAFT`；不适用项需要解释，未决定项保留 `null`。具体步骤见从零开始指南。

```text
docs/                    # 研究方法、结论与使用说明
templates/               # 协议、决策、实验日志、claim 映射模板
examples/                # 完整填写的虚构教学流程
diagnostics/             # 冻结模型上的离线诊断阶段
engineering/             # 由明确假设驱动的训练/适配阶段
src/                     # 使用者实现模型、数据与评价接口
configs/                 # 可检查的实验定义；示例为 DRAFT
evidence/                # 少量历史聚合证据，不含样本级数据
tools/                   # 阶段创建、配对汇总、文本资产 SHA256 清单
tests/                   # 工具契约测试，不代表科研有效性测试
.github/workflows/       # 工具与文本清单 CI
```

## 核心研究路径

```mermaid
flowchart LR
    A[具体任务与失败现象] --> B[竞争解释]
    B --> C[最小设计与强对照]
    C --> D[开发验证]
    D --> E[冻结预定比较]
    E --> F[独立确认]
    F --> G[有边界的结论]
    D --> H[保留失败与修订记录]
    F --> H
```

允许从成熟方法出发做有依据的组合，也允许提出进取性的假设；关键是把已有组件、设计差异、实验证据和贡献范围分别说清楚。复杂设计必须接受简单强对照，负结果也应保留完整解释空间。

## 发布范围

- 发布：已结束阶段的结论摘要、通用设计与验证思路、可复用目录结构、模板和独立编写的小工具。
- 保留私有：本次明确排除的未发表项目方案、实现与数据，以及原始图像与标注、样本身份清单、checkpoint、预测缓存、设备日志和凭据。已结束研究的方法尝试、失败与错误假设可以作为教学材料讨论。本版也不附带第三方模型源码。
- 历史数值是本地 development 协议下的结果，不是官方 benchmark 排名。本仓库不宣称提出了新的有效分割算法。
- 本仓库代码与文档采用 [MIT 许可证](LICENSE)，允许保留许可与署名后复用、修改和商用；未发布的原研究资产不在授权范围内。第三方依赖和上游方法仍遵循各自许可。

建议先阅读 [贡献说明](CONTRIBUTING.md)，避免把探索结果、缺失证据或尚未执行的方案写成已完成事实。
