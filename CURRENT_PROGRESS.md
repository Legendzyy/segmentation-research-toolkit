# 当前状态

- 发布形态：可运行方法移植 + 原生研究档案。
- 可执行范围：native、ENG01、ENG02 KD、ENG03 KD、ENG04 transfer、P1F factorial。
- 数据输入：经过 manifest 验证的 YOLO polygon train/val；COCO8-seg 提供真实数据 smoke 下载。
- 评价：参考网格 COCO mask AP、保存预测重放、严格配对汇总。
- 仍属档案：P1A–P1E 专用诊断、P1D 特化训练、历史数据划分与权重。
- 未支持：MinneApple mask 转换、DDP、自动恢复、官方 benchmark 提交。
- 机器入口：[PROJECT_STATE.json](PROJECT_STATE.json)。

新运行不改变历史研究定义与结论。验证状态见 `evidence/RUNTIME_VALIDATION.json`。
