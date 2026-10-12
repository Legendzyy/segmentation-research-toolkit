# 仓库结构与状态分层

| 路径 | 角色 | 修改规则 |
|---|---|---|
| `src/research_toolkit/` | 可执行方法与运行入口 | 修改后跑契约测试和受影响方法 smoke |
| `configs/runnable/` | 新运行配置 | 显式记录科学选择；不继承历史 FROZEN 状态 |
| `diagnostics/`, `engineering/` 阶段目录 | 127 份历史原件 | 冻结，只追加具日期的更正或新阶段 |
| `evidence/NATIVE_SOURCE_MAP.json` | 历史原件映射 | 对应原件变更需说明原因 |
| `evidence/CODE_SOURCE_MAP.json` | 移植代码来源 | 修改移植文件时更新 hash 与适配说明 |
| `PROJECT_STATE.json` | 当前能力、验证与接续入口 | 与实现同步更新 |
| `studies/<id>/` | 独立课题输入、决策与原生阶段结构 | 通过 `tools/study.py` 创建与接续；课题间状态隔离 |
| `studies/<id>/STUDY_STATE.json` | 该课题当前阶段、证据、任务与事件历史 | 单写者顺序 checkpoint；`RESUME.md` 为生成视图 |
| `work/` | 本地数据、checkpoint、预测与临时输出 | Git 忽略；不作为公开资产自动收录 |

原阶段的内部结构保留：问题/协议 → 方法定义 → 冻结配置 → analysis/results → 阶段报告/paper → 执行日志。运行代码通过来源映射与这些原件连接，避免把历史环境路径重新引入公共入口。

新研究创建独立阶段，先定义场景、benchmark、baseline、候选机制与比较矩阵。运行输出必须能定位到配置、数据 manifest 和 checkpoint。历史报告中的结论、预算和授权仅描述原阶段，不驱动当前任务执行。

新课题不写入根目录冻结档案。其 `engineering/` 与 `diagnostics/` 位于各自 study 内，沿用原阶段的契约、方法、配置、分析、结果、论文主线、日志与登记结构。操作入口见[新课题工作区](NEW_STUDY.md)。
