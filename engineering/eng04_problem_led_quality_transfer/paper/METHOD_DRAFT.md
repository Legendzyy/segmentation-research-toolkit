> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../../docs/PROVENANCE.md)。

# 方法与实验设置草稿（负/混合结果版本）

本文草稿记录一个**被检验但未获支持**的训练期监督设计，不把它写成已成功的新方法。研究问题是，在密集、外观相似果实的轻量实例分割中，更强教师的实例目标能否令完整预测 mask AP 高于同预算原生学生及简单输出蒸馏。学生为原生 YOLO11n-seg，输入640；教师为既有 YOLO11s-seg。训练 recipe、学生初值、60epoch、batch8、AdamW/nbs32 和预定最后 checkpoint 在锁定确认块内保持一致；Blueberry development full254 用统一 evaluator。所有方法只使用训练集 GT，推理时不读取 GT 或教师。

**N0** 使用原生 GT 分割损失。**D0** 在学生 TAL 正例同位置迁移教师 true-class 概率、decoded box 与 mask，作为更简单的输出 KD。**X0** 为冻结教师 head 的 CrossKD 核心 head-input 路径在 YOLO 检测分支的简化适配；不声称完整复现原论文。**I0** 从教师自己对同一 GT 的正例中取合格代表，以实例相关的检测/mask 质量给予连续权重。**I1** 仅去除 I0 教师分类 BCE。**J0** 在检测端沿用 D0 同位置监督，在 mask 端采用 I1 的 teacher-own same-GT 代表与质量权重；native GT loss 始终保留，KD 在前三 epoch 线性 warmup。J0 对 D0 的变动同时包含 mask 目标来源与权重，故不把两者分别宣称为被隔离的因果组件。详细数值定义、空集合处理和工程检查见 `../METHOD_SPEC.md`、冻结配置和 preflight receipt。

seed42 与在看过 seed42 后追加的 seed128 是开发资料。最终评价前，事前锁定 seed31415/27182 × J0/D0/N0 六项完整配对：每项独立训练60epoch并以最后预定 checkpoint 在相同 254 图、1803 GT、输入640、maxDet300 下计算 class-aware mask COCO AP@[.50:.95]，AP75/AP90/尺度为辅助。六项均完成，且未根据第一粒结果删减后续任务。保存预测 replay 仅用于与同一 pycocotools evaluator 结果核对，不构成独立评价算法。

实例级分析分别报告全 GT 固定 score 点 coverage、完整预测队列的各 IoU 阈值 TP/FP/ignore 与高分 FP 排序，以及同 GT 且预测可对齐时的条件 mask IoU/boundary。三者的分母不同，不用 coverage 或条件均值替代完整 AP；不从 TP/FP 总量反推 AP 因果。训练耗时为共享 GPU 的非隔离进程时间；teacher 初训成本和隔离推理 latency 分开列为未完整评估项目。

本设计最后未在两粒新确认 seed 上取得同方向的主 AP 或 AP90 变化。本文若保留这段方法，应作为有控制的失败案例及监督目标/排序不确定性的研究记录，而不是以 J0 为正向方法名称或成功式摘要。
