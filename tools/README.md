# 标准库工具

运行目录为仓库根目录，Python ≥3.10，不依赖 PyTorch、NumPy 或 GPU。

## 配对 AP 描述性汇总

`python tools/paired_summary.py evidence/paired_confirmation.csv`

CSV 必须含 candidate、reference、seed、AP、reference_AP、dataset、schedule、checkpoint_rule、evaluator、evidence_role。AP 输入是 `[0,1]` 的 fraction，输出差值是 `(AP-reference_AP)*100` 百分点。

工具拒绝缺失、非有限数、重复 seed 配对、混合协议/角色，以及同模型同 seed 的冲突数值。不同 reference 分开汇总，列出所有正、负、零差值。它不能验证 CSV 所声明的数据与训练身份是否真实，也不提供 bootstrap、显著性检验或完整 AP 评价。

## 文本 SHA256 清单

```bash
python tools/manifest.py create . work/local_manifest.json
python tools/manifest.py verify . work/local_manifest.json
```

只包含 `.md/.json/.csv/.py/.yml/.yaml/.toml/.txt` 及 LICENSE、.gitignore、.gitattributes；UTF-8 文本每文件上限 2 MiB。排除 `.git`、运行缓存、数据、权重、输出等目录和 `.env*` 文件。符号链接不受支持；清单本身不包含在自己的 hash 中。

已有清单不覆盖。验证检查所允许文本的新增、缺失及变化；变更退出码 1，输入错误退出码 2。排除的文件不受完整性保护，包含的文本也不因此安全公开。使用前检查 `tools/manifest.py` 的范围定义，避免误认为这是全部研究资产索引或凭据扫描器。

生成的新清单会改变源码树的文本集合；临时清单优先放 `work/`。首版发布清单 `RELEASE_MANIFEST.json` 验证命令为 `python tools/manifest.py verify . RELEASE_MANIFEST.json`。修改被索引文件后，该清单预期失效；正式再发布前审核变化并显式更新它。
