# Segmentation Research Toolkit

实例分割研究代码与阶段档案。提供原生方法的训练、COCO mask 评价、预测重放和配对消融入口；保留 P1A–P1F、ENG01–ENG04 的历史设计与结果。

| 入口 | 内容 |
|---|---|
| [安装与首次运行](docs/START_HERE.md) | 在公开 COCO8-seg 上完成训练 → 评价 → 消融汇总 |
| [数据集获取与接入](docs/DATASETS.md) | Mega_Blueberry、MinneApple、COCO8-seg 的官方来源及数据角色 |
| [方法与运行契约](docs/RUNTIME.md) | 25 个入口、配置字段、评价定义、输出与限制 |
| [Agent 状态](PROJECT_STATE.json) / [协作规则](AGENTS.md) | 当前能力、检查命令、续接顺序 |
| [工程研究主线](docs/PAPER_DESIGN_WORKFLOW.md) | 场景、强基线、机制、消融、trade-off 与证据 |
| [工程阶段](engineering/README.md) / [诊断阶段](diagnostics/README.md) | 原始协议、方法、日志、图表与结论 |

## 可运行方法

| 家族 | 变体 | 实现 |
|---|---|---|
| Native | YOLO11 n/s | 固定版本的上游网络；n 为学生，s 可训练为教师 |
| ENG01 | E0–E5 | detail、MLCA、gate、训练期 boundary head 及其组合 |
| ENG02 | K1/K2 | 普通/前景加权 feature KD |
| ENG03 | D0/Q0/M0/C0/R0/F0 | 输出 KD、任务门控、代表 anchor 与 feature 组合 |
| ENG04 | X0/I0/I1/J0 | CrossKD 适配、GT-linked 迁移及检测/mask 分工 |
| P1F | F00/F10/F01/F11/CUP/CCOMP | source × lattice、插值和算力控制 |

方法类来自已结束阶段，保留原计算；运行层使用显式路径和数据 manifest。历史配方与移植后的新运行分开记录，不宣称恢复原数据划分或复现旧表数值。

## 最短运行路径

完成[安装](docs/START_HERE.md)后，在仓库根目录执行：

```bash
python -m research_toolkit fetch-smoke --output work/coco8
python -m research_toolkit matrix --config configs/runnable/smoke_matrix.json --data work/coco8/prepared/data.yaml --output work/smoke_matrix
python -m research_toolkit replay --evaluation work/smoke_matrix/native_s42_eval
```

输出包括两次真实小规模训练的 checkpoint、评价预测、指标和 `work/smoke_matrix/summary/paired.csv`。COCO8-seg 仅用于工程验证；一轮随机初始化结果不能作为方法有效性证据。

正式数据接入后，可使用 `configs/runnable/eng01_matrix.json` 执行 6 变体 × 3 seeds 的新实验。先核对预算与数据定义，再启动该配置。KD 变体需要同任务、同类别映射的教师 checkpoint。

## 目录职责

```text
src/research_toolkit/     # 移植方法类、训练、数据、评价、消融
configs/runnable/        # 可执行配置；不覆盖历史冻结配置
tests/                   # 数值、数据和比较契约检查
diagnostics/             # P1A–P1F 历史档案
engineering/             # ENG01–ENG04 历史档案
evidence/                # 文档与代码来源映射、运行验证记录
work/                    # 本地数据与新运行输出，Git 忽略
```

原始数据、标注、权重和预测不随仓库发布；未发表项目的代码、方法与数据不进入发布范围。历史 Blueberry development 结果不等于官方公开 benchmark 排名。

文档及独立档案维护工具保留 MIT；训练运行代码和第三方依赖适用相应许可，详见 [THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES.md)。
