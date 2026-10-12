> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../../docs/PROVENANCE.md)。

# Claim 与证据边界（2026-09-30）

## 目前可写为事实

- ENG04 的中心问题未变：教师实例监督能否改善轻量 YOLO11n 的**完整** Blueberry development mask AP。N0 原生、D0 简单输出 KD、J0 任务分工方案在新 seed31415/27182 各 60epoch、预定 last、独立 full254 上完成同种子配对。原始结果在 `../analysis/confirm_j0_v1/PAIR_TABLE.csv`；裁决在 `../analysis/CONFIRM_J0_V1_DECISION.md`。
- J0−D0 主 AP：−0.6491/+0.5145 pp，两粒均值 −0.0673 pp；J0−N0：−0.5327/+0.4379 pp，均值 −0.0474 pp。AP90、AP75、small AP 在新确认种子也未保留同一方向。两粒不能证明零效应，但不支持稳定正收益。
- 固定点 coverage 与共同 GT 条件 IoU 不呈一致形状改善；完整预测排序的具体因果失败来源仍未识别。`../analysis/confirm_j0_v1/COMMON_GT_SHAPE.json` 与 `FULL_QUEUE_COUNTS.csv` 是描述性证据，不能替代 AP 或做因果分解。
- J0 在训练期使用 D0 的同位置学生 TAL 检测监督，加 I1 来源的 teacher-own same-GT 合格 mask 目标及质量权重；部署保留原生学生结构。train-only 数值/梯度/保存加载 parity 通过，但隔离端到端 latency 未测。共享 GPU 的训练耗时高于 D0/N0；现有 teacher 初训成本不能忽略。
- X0 是 CrossKD 核心路径的 YOLO 简化适配，不是官方方法全复现；I0→I1 去掉教师分类 BCE 的开发性正向消融未超越 D0；P1D M1@75 仅作不同预算历史强参照。

## 不能写作成立的主张

- “J0 稳定提高完整 mask AP / AP90 / 小目标 AP / 共同 GT 形状”。
- “实例目标错配或 score 排序瓶颈已被 J0 证实并修复”。
- “J0 优于当前成熟 KD、公开社区强 benchmark baseline 或跨数据集泛化”。CrossKD 完整复现、同预算 P1D M1 桥接、MinneApple 配对与目标域 teacher 均未完成。
- “零部署开销 / 实时性能提升 / 已通过 test”。原生结构 parity 不是隔离速度测试，test 从未访问。

最终建议裁决：`NO_SUPPORTED_METHOD_AFTER_FINAL_ATTEMPT`。可以写诚实的失效分析与未来判别协议，不把负结果包装成新方法成功。详见 `../analysis/MINIMAL_PAPER_ASSET_REVIEW.md`。
