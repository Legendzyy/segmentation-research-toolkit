# DEMO-PAIR 日志格式示例

这里说明应如何记录，不伪造真实实验时间、环境或完成状态。

- 目的：验证已给定表格的配对算术。
- 命令：`python tools/paired_summary.py examples/synthetic_study/paired_metrics.csv`
- 输入：同目录三行虚构表；无训练、真实数据或权重。
- 预期工程结果：退出码 0；均值约 +0.5 pp，2 正 1 负。
- 实际运行时间、Python 版本、退出码与输出：由运行者在自己的 `work/` 中记录。
- 科学解释：仅限教学算术，见 `DECISIONS.md`。
