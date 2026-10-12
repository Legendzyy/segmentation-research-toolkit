# 标准库工具

运行目录为仓库根目录，Python ≥3.10，不依赖 PyTorch、NumPy 或 GPU。

## 创建空阶段

`python tools/new_stage.py diagnostics pilot01` 或 `python tools/new_stage.py engineering study01`。

生成协议、配置、日志、决策、claim 模板与源码/结果目录说明。目标存在时拒绝覆盖；名称只允许小写字母开头和后续字母、数字、下划线，2–64 字符，排除 Windows 保留名。配置保持 DRAFT，不校验科学定义、不运行实验。完整首次使用步骤见 [从零开始指南](../docs/START_HERE.md)。

## 配对 AP 描述性汇总

`python tools/paired_summary.py evidence/paired_confirmation.csv`

CSV 必须含 candidate、reference、seed、AP、reference_AP、dataset、schedule、checkpoint_rule、evaluator、evidence_role。AP 输入是 `[0,1]` 的 fraction，输出差值是 `(AP-reference_AP)*100` 百分点。

工具拒绝缺失、非有限数、重复 seed 配对、混合协议/角色，以及同模型同 seed 的冲突数值。不同 reference 分开汇总，列出所有正、负、零差值。它不能验证 CSV 所声明的数据与训练身份是否真实，也不提供 bootstrap、显著性检验或完整 AP 评价。

| 列 | 内容与例子 |
|---|---|
| candidate / reference | 稳定的模型/方案名称，如 B / A，不把 seed 拼进名称 |
| seed | 非负整数；每行已对齐同一 seed 的两个模型 |
| AP / reference_AP | 已由你自己的评价器计算的 AP fraction，如 0.65 / 0.64 |
| dataset | 同一数据版本和 split 的身份标签；本工具不读取原数据 |
| schedule | 训练配方/预算的固定标识，不只写模糊的 default |
| checkpoint_rule | 如 last_epoch20；不要混入不同 best 选择规则 |
| evaluator | 评价定义与版本标识，应能关联到你的协议 |
| evidence_role | 如 development 或 locked_seed_confirmation，不混合 |

多个参照各自列出实际存在的 seed，不自动取交集或补齐缺失；比较组的 seed 集合不同时不能将其均值直接当同一配对比较。`zero_seeds` 使用精确零，不包含任意近零容差。CLI 不输出科学 PASS/STOP，退出码 0 只表示合法输入完成了算术汇总。

## 文本 SHA256 清单

```bash
python tools/manifest.py create . work/local_manifest.json
python tools/manifest.py verify . work/local_manifest.json
```

只包含 `.md/.json/.csv/.py/.yml/.yaml/.toml/.txt` 及 LICENSE、.gitignore、.gitattributes；UTF-8 文本每文件上限 2 MiB。排除 `.git`、运行缓存、数据、权重、输出等目录和 `.env*` 文件。符号链接不受支持；清单本身不包含在自己的 hash 中。

`create` 拒绝覆盖已有清单；`verify` 检查所允许文本的新增、缺失及变化，变更退出码 1，输入错误退出码 2。排除的文件不受完整性保护，包含的文本也不因此安全公开。使用前检查 `tools/manifest.py` 的范围定义，避免误认为这是全部研究资产索引或凭据扫描器。

生成的新清单会改变源码树的文本集合；临时清单优先放 `work/`。首版发布清单 `RELEASE_MANIFEST.json` 验证命令为 `python tools/manifest.py verify . RELEASE_MANIFEST.json`。修改被索引文件后，该清单预期失效；正式再发布前审核变化并显式更新它。

审核后执行 `python tools/manifest.py refresh . RELEASE_MANIFEST.json`：旧清单按 SHA256 备份在 `work/manifest_history/`，新清单原子替换；没有变化则输出 UNCHANGED。必须再运行 verify，并将清单和已审核文件一起提交。不要用自动 refresh 掩盖意外文件或写进 CI；清单更新不代表科学协议可以覆写。
