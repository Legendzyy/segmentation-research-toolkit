# 新课题工作区与 Agent 接续

研究者提供场景、数据集和算力，Agent 创建独立课题后核对环境和官方协议，建立 baseline，分析实际错误，再开展机制与消融。结构沿用原生 ENG 阶段的协议、`RESUME.md`、执行日志、运行登记与论文主线；不继承旧阶段的数据身份、预算或结论。

## 研究者入口

将下面的任务交给 Agent，并替换三个输入即可：

> 在本仓库开展新课题。场景：【目标对象、实际困难或应用需求】；数据集：【名称、官方链接或已有本地路径】；算力：【GPU 型号/数量/显存、可用时长；不清楚的请检查】。先读 AGENTS.md 和 docs/NEW_STUDY.md，创建独立 study，复用已验证能力。核对 benchmark 与强 baseline，跑通工程检查，再建立本课题的 baseline 实验、错误分析和机制验证。保留失败及未排除解释，每轮更新阶段接续状态。能够自行核实的工程问题直接解决；尚未明确的科学选择集中说明，不借用旧实验结论。

课题标识由 Agent 选择简短英文 slug。以下为命令格式，尖括号内容必须替换为研究者输入；不是已存在的数据或实验：

```bash
python tools/study.py init --study surface_instances --scenario "<场景>" --dataset "<数据集>" --compute "<算力>"
python tools/study.py status --study surface_instances
```

创建工具只依赖 Python 标准库，尚未安装 PyTorch 也能使用。不下载数据、不训练、不填写假结果。已有同名课题会报错，使用 `status` 接续，不重新初始化覆盖。

## 工作区

```text
studies/<id>/
  AGENTS.md                 # 当前课题的执行与交接约定
  USER_REQUEST.md            # 原始三个输入
  STUDY_STATE.json           # 权威状态、当前阶段、历史接续事件
  DECISIONS.md               # 科学与工程决策及依据
  engineering/eng00_baseline/
    README.md
    ENGINEERING_CONTRACT.md  # draft 协议；不自动冻结
    METHOD_SPEC.md
    configs/protocol.json    # 未确定的科学定义为 null
    src/                    # 当前阶段适配或候选实现
    analysis/
    results/                # 可审查的小型证据
    paper/PAPER_BLUEPRINT.md
    EXECUTION_JOURNAL.md
    run_registry.jsonl
    artifact_index.json
    RESUME.md               # 根据权威状态生成的接续视图
    FINAL_REPORT.md          # 初始明确“尚未结束，无结果”
work/<id>/<stage>/<run>/     # Git 忽略的实际运行输出
```

`configs/protocol.json` 定义研究问题、数据角色、baseline、评价、预算、对照与 checkpoint 策略，**不是训练配置**。Agent 核实后，另存兼容[运行契约](RUNTIME.md)的 `train.json` / `matrix.json`。当前工具不会解析 GPU 自述自动选 batch，也不会把默认配方当成新课题的既定科学选择。

## 第一轮工作与阶段推进

1. 读取根目录 Agent 规则、工具能力，再读取当前课题输入、状态与协议。多课题并存时始终显式使用 `--study`，没有全局活动课题。
2. 核查实际 GPU/显存、Python/依赖、存储与当前在跑任务；查明数据获取方式、许可、标签格式、官方划分与评价。无法核实的项目保留未知，并继续独立工作。
3. 按[首次运行](START_HERE.md)执行 COCO8-seg 工程检查，将输出放 `work/<id>/`。仅说明运行能力，不把工程 smoke 当成新课题 baseline。
4. 根据场景、benchmark、资源和公开实现确定强 baseline 候选；确认当前评价与官方口径的差异。将明确选择填入协议；探索配置注明探索，正式比较前固定必要定义和预算。真正影响科学含义且仍有歧义时才询问研究者。
5. 准备数据 manifest，在独立输出目录运行 baseline，登记配置、代码版本、hash 和实际状态。分析具体失败类型与简单替代解释，再提出机制及最小充分的对照。方法阶段与诊断阶段由实际问题决定，不强制跑满固定流程。
6. 每次交接更新执行日志、决策与 checkpoint；阶段完成后写报告并建立下一阶段，保留前阶段原件和证据。

例如，baseline 后可创建一个诊断阶段；这条命令只创建目录并切换当前阶段，不代表旧阶段已完成，也不启动实验：

```bash
python tools/study.py stage --study surface_instances --kind diagnostics --id p01_error_analysis --question "baseline 的哪些错误在固定评价下可重复，简单因素是否足以解释？"
```

工程阶段使用 `--kind engineering --id eng01_<name>`。后续阶段应在协议中引用前阶段证据，不能复制结论作为本阶段新结果。

## 状态交接

Agent 将以下结构写入本地 JSON 文件，例如 `work/<id>/handoff.json`，再调用 checkpoint。示例描述的是初始化状态，不是执行记录；实际交接须替换为真实情况。

```json
{
  "status": "planning",
  "summary": "工作区已创建，尚未执行实验。",
  "next_action": "检查运行环境并核对数据集官方划分与评价。",
  "evidence": [],
  "blockers": [],
  "running_jobs": []
}
```

```bash
python tools/study.py checkpoint --study surface_instances --input work/surface_instances/handoff.json
python tools/study.py status --study surface_instances
```

- `status`：`planning`、`exploring`、`running`、`analyzing`、`blocked`、`complete`。它描述工作状态，不是科学有效性判定。
- `summary`：已完成事实与未完成项；`next_action`：下一项可执行动作、条件及应读取的文件。状态为 complete 仍需写清关闭原因或下一阶段。
- `evidence`：仓库根目录相对文件路径数组；工具记录 SHA256。恢复时 `status` 列出缺失或变化证据，Agent 先处理差异再引用结论。hash 证明文件身份，不证明内容正确。外部文献写入本地引用记录后登记该文件。
- `blockers`：具体未解决问题数组；blocked 必须有阻塞原因。不会把普通工程报错自动视为需要研究者介入。
- `running_jobs`：每项含 `host`、`id`（PID 或调度任务 ID）、`command`、`output` 字符串。running 必须登记任务；恢复时核查真实进程和输出，记录可能已过期，不能据此重复启动。
- `status` 输出中的 `registered_jobs` 汇总本课题所有阶段登记的任务；切换阶段不会隐藏旧阶段的在跑任务。它仍是待核实的记录，不是实时进程查询。
- 可选 `stage`：课题内已存在的阶段相对路径；用于返回旧阶段，同时切换 `active_stage`。不提供则更新当前阶段。

checkpoint 以原子替换写入 `STUDY_STATE.json`，同时保留 events 历史，再生成阶段 `RESUME.md`。complete 要求存在证据且无在跑任务或阻塞，但工具不判断是否足以支持论文 claim。若生成视图中断，以 JSON 为准，下一次 checkpoint 会重建视图。同一课题状态由一个 Agent 顺序写入；此工具不提供并发任务调度或多写者合并。

实际运行按行记录到 `run_registry.jsonl`，包含运行 ID、命令、工作目录、seed、代码 commit、配置/manifest/checkpoint hash、输出路径和实际状态；未生成的 checkpoint 不填假 hash。`artifact_index.json` 登记小型证据与大文件本地位置。日志和登记由执行 Agent 更新，工作区工具不监控进程，也不自动推断训练完成。

## 版本控制与发布

根目录 `PROJECT_STATE.json` 只描述工具包能力；课题状态只写自己的 `STUDY_STATE.json`。原始 `engineering/`、`diagnostics/` 档案不作为新课题输出目录。新目录默认只是本地未跟踪文件，纳入 Git 前显式审查；不要用整仓 `git add .` 自动收录研究材料。数据、权重、逐样本预测和日志留在 `work/`。课题创建或实验授权不等于公开其方法、设计或数据的授权。
