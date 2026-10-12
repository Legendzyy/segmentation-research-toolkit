# 运行与方法契约

## 方法映射

| CLI variant | 来源 | 固定机制 |
|---|---|---|
| `native` | ENG01 E0 / ENG02 A0、A2 | YOLO11 n/s 原生分割图 |
| `eng01:E0`–`eng01:E5` | ENG01 `eng_model.py`, `eng_boundary.py` | E0 原生；E1 detail；E2 MLCA；E3 gate；E4 boundary；E5 gate+boundary |
| `eng02:K1`, `eng02:K2` | ENG02 `kd_model.py` | neck 16/19/22 feature MSE；K2 前景2、背景1，逐图单位均值权重；lambda=1 |
| `eng03:D0/Q0/M0/C0/R0/F0` | ENG03 output/combined KD | 分类/框/mask 权重1/5/1；D0直接，Q0双任务门控，M0 mask门控，C0检测门控，R0代表anchor改变，F0增加feature MSE |
| `eng04:X0/I0/I1/J0` | ENG04 `transfer_model.py` | 原任务迁移计算；前三epoch ramp；X0 multiplier .25，其余1 |
| `p1f:F00/F10/F01/F11/CUP/CCOMP` | P1F `factorial_model.py` | source/lattice factorial，固定插值与容量控制；命名 CUP/CCOMP 对应报告 C-UP/C-COMP |

方法类的计算保留原件；路径、模型构建、类数、设备和运行输出由移植层显式处理。新数据可以改变类别数；这些运行属于新实验。源文件与公开文件映射见 [CODE_SOURCE_MAP](../evidence/CODE_SOURCE_MAP.json)。

P1A–P1E 中依赖特定候选缓存、oracle 优化和历史样本身份的专用管线仍是档案，未声明为可运行命令。P1D 头部特化训练也未纳入当前 runner。

## 配置字段

单次训练必填 `variant, scale, epochs, batch, imgsz, seed, device, workers, weights, purpose`；KD 另需 `teacher`。`purpose` 为 `engineering_smoke` 或 `new_experiment`。`weights: "none"` 为随机初始化。配置外未知字段拒绝执行，CLI 显式覆盖项写入最终 `run.json`。

方法移植固定 YOLO11 图；结构变体固定 n 学生，`native` 支持 n/s。输入为32倍数且至少64。默认训练配方继承原阶段 AdamW、lr0=.001、lrf=.01、nbs32、overlap mask、mask_ratio4 与相同增强。`smoke.json` 修改了输入、epoch、batch、初始化和设备，因此不属于原实验复现。

矩阵配置包含 `baseline, variants, seeds, reference_size, training`。每个 variant/seed 使用单独进程，防止结构注册和 boundary 数据钩子影响下一任务。失败后停止队列并保留日志；不删除失败、不挑选最佳 seed。

## 评价定义

`evaluate` 沿用 ENG02 的原生 mask 解码与 COCO AP 汇总，替换对私有 GT 缓存的依赖，直接读取准备好的 polygon 标签。

- val 图像全量纳入，包括漏检与空预测。
- 推理 conf=.001、class-aware NMS IoU=.7、maxDet300，模型输入取训练配置 `imgsz`。
- GT 使用 P1B 的 letterbox 比例、padding 与整数截断 fillPoly；参考网格默认640。
- 预测 mask 先在模型输入网格按原生 `process_mask` 生成；输入与参考网格不同时，二值 mask 用最近邻映射到参考网格。
- COCO AP@[.50:.95]、AP50/AP75/AP90 和尺度 AP；尺度面积单位是参考网格像素。不是原始图像尺度的官方 leaderboard 评价。
- 无该尺度 GT 时返回 `null`，空预测但有 GT 时 AP=0。
- `replay` 使用同一 COCO 实现重算存储的 GT/预测，验证一致性；不宣称独立算法验证。

正式配置默认640；工程 smoke matrix 明确使用64参考网格。不同网格、划分或训练预算不得混入同一模块消融表。输入896等系统对照应单独解释，当前 `summarize` 会拒绝不兼容配对。

## Checkpoint 与继续运行

`train/weights/last.pt` 保留最后预定 epoch 的 EMA checkpoint。`deploy.pt` 从该 EMA 导出学生图：移除 KD 教师与 projector；E4/E5 移除 boundary 辅助头。保存前检查非有限/半精度溢出状态，拒绝静默修正权重。

成功产生 `completion.json`；失败产生 `failure.json`。配置、数据 manifest、教师/初值和 checkpoint 具有身份 hash。当前不支持断点恢复、DDP 或声称逐位复现历史 CUDA 运行；CPU smoke 仅验证移植后的执行路径。

`check-deploy --run RUN_DIR` 对比最后 epoch 的 EMA 与 `deploy.pt` 的 CPU 前向张量，要求逐值一致，并检查部署图不含教师或 boundary head。该检查不测隔离时延。
