# 第一次使用：从阅读到建立自己的阶段

这个仓库首先服务于学习科研。可以直接阅读案例和复用模板；两个分析/审计工具及阶段创建工具可以直接运行。这里没有完整分割训练器，创建目录不等于训练模型。

## 1. 下载并检查环境

安装 Python 3.10+ 和 Git 后，在 PowerShell、macOS Terminal 或 Linux shell 依次执行：

```bash
git clone https://github.com/Legendzyy/segmentation-research-toolkit.git
cd segmentation-research-toolkit
python --version
python -m unittest discover -s tests -v
python tools/manifest.py verify . RELEASE_MANIFEST.json
```

预期测试最后显示 `OK`，清单显示 `"status": "PASS"`。如果系统只提供 `python3`，把下文所有 `python` 替换成 `python3`。无需安装 PyTorch、下载数据或配置 GPU。若用 GitHub 的 **Use this template**，克隆你新建仓库的地址；下载 ZIP 则解压后进入含 README 的根目录，Git 命令可跳过。

## 2. 先跑完全虚构的教学示例

```bash
python tools/paired_summary.py examples/synthetic_study/paired_metrics.csv
```

预期只有 `B` 对 `A` 一组比较：3 个 seed，差值约为 `+1.0 / -0.5 / +1.0` 百分点，均值 `+0.5`，2 正 1 负。浮点末尾的小数误差正常。CSV 是手工设定的教学数，不是模型评价；脚本读取已有 AP，不会从 mask 计算 AP。

然后读 [填写完整的示例](../examples/synthetic_study/README.md)，沿“协议 → 表格 → 汇总 → 决策 → claim”走一遍。再看 [失败案例练习](FAILURE_CASES.md)，比较真实历史裁决与这个算术示例的区别。

## 3. 为自己的问题创建空阶段

```bash
python tools/new_stage.py diagnostics pilot01
```

生成 `diagnostics/pilot01/`，含 README、PROTOCOL、config、EXPERIMENT_LOG、DECISIONS、CLAIM_EVIDENCE 及 `src/`、`results/` 说明。目标存在时拒绝覆盖。需要训练的阶段使用 `engineering`：

```bash
python tools/new_stage.py engineering study01
```

这是两个可选例子，不要求都创建。阶段名用小写字母开头，后接小写字母、数字或下划线；长度 2–64。新配置始终为 `DRAFT`，不会运行实验或自动冻结。

按以下顺序填写，比一次填完全部空栏更容易：

| 顺序 | 先做什么 | 做完时应留下什么 |
|---|---|---|
| 1 | 具体问题与竞争解释 | 协议里的问题句、主假设和至少一个替代解释 |
| 2 | 明确比较与 endpoint | 谁与谁比较、同 seed 如何配对、主指标单位 |
| 3 | 固定身份与公平性 | 数据角色、初始化、预算、checkpoint 与评价器定义 |
| 4 | 明确预定决策 | 什么支持/反驳假设，什么只允许判为不确定 |
| 5 | 接入现有工程 | 在 `src/` 实现或引用训练、数据、评价接口及版本 |
| 6 | 检查并冻结 | 验证关键计算，记录配置哈希、执行范围与时间 |

暂不适用的字段写 `not_applicable` 并说明理由；未决定的字段保留 `null`，不得将未完成协议称为冻结。`config.json` 是记录结构，没有内置科学审查或运行权限控制，工具也不会自动检测全部未填项。

## 4. 从模板变成自己的研究仓库

更新根目录 `CURRENT_PROGRESS.md` 和 `DECISIONS.md`，使它们描述你的工作。`docs/`、`examples/` 和 `evidence/` 可保留作参考，但不要把维护者的历史证据当作你的结果。将自己选定的聚合表放入对应阶段的 `results/`；样本身份、预测和运行日志放本地 `artifacts/`。

历史示例是测试夹具的一部分。若要删除 `evidence/` 或示例，需要同时调整引用文档和相关测试；保留它们并不妨碍新阶段运行。MIT 允许复用与修改，请保留原版权及许可，并为你自己的新增内容按需署名。

## 5. 修改文件后，如何更新清单并通过 CI

修改 README 或新增阶段后，旧发布清单显示 FAIL 是预期行为。先看变更，再显式更新：

```bash
git status --short
git diff
python tools/manifest.py verify . RELEASE_MANIFEST.json
```

上面的 `verify` 若发现变更会以退出码 1 结束，并列出 changed/added/missing；这一步不会阻止你人工继续下列命令。确认所有待发布文本可公开后：

```bash
python tools/manifest.py refresh . RELEASE_MANIFEST.json
python -m unittest discover -s tests -v
python tools/manifest.py verify . RELEASE_MANIFEST.json
```

`refresh` 将旧清单按其 SHA256 备份到本地 `work/manifest_history/`，再原子替换当前清单。它只确认新字节成为基线，不判断科研结论正确或文件适合公开。CI 只做 verify，不会替你接受修改；发布时把更新的清单与审核后的源文件一起提交。

## 常见卡点

| 现象 | 含义与处理 |
|---|---|
| 提示找不到 tools 文件 | 当前目录应是含 README 的仓库根目录 |
| `Refusing to overwrite` | 已有清单用 verify；确实接受新版本时用 refresh。已有阶段换新名字，勿覆盖历史 |
| AP 输入 65 被拒绝 | 输入采用 fraction，例如 0.65；输出才是百分点 |
| 混合协议被拒绝 | 开发/确认、不同数据或预算分文件汇总，不删字段绕过检查 |
| 所有测试通过却没有训练结果 | 测试只证明工具契约通过；训练和科学验证需要你自己的实现 |
| 清单 PASS 但有未列文件 | 清单只覆盖允许文本。用 Git 文件列表另查二进制、日志和不应发布的文件 |
