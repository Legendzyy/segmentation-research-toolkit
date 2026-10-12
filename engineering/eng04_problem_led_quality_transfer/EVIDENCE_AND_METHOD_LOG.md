> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# ENG04 初始证据与设计判断

2026-09-27。全部为源码/历史开发证据，不是新方法的实验成绩。

## 1. 真实对应：静态事实与未验证假设

ENG03 src/output_kd_model.py:73 从student criterion取得TAL GT分配；teacher class/decoded box来自同一anchor，mask teacher coefficient也来自student选择的正anchor。teacher mask与student mask分别用自身prototype渲染，这是正确的跨模型mask比较方向；代码没有直接对齐prototype通道。

源码未计算teacher自己的TAL分配，所以同网格位置不等于已证实同实例身份。强teacher最终AP更高也不能推出该位置teacher target更好。反过来，这个缺口也不证明它确实监督了错误实例。

下一真实batch记录必须包含(image_key, original_gt_id)、student正集合、teacher独立正集合、双方assigned GT、teacher类别/decoded bbox/渲染mask质量、空候选原因。原始标签ID必须经overlap排序映射回去，不能把batch-local gt_index直接当数据集身份。固定合法train样本，禁用写历史cache，teacher推理eval，逐图同变换；不使用val GT定权重。跨anchor box在输入坐标比较，不跨位置KL原始DFL bins。

## 2. 监督预算：已确认混杂

output_kd_model.py:109–119：每个有student positives的GT占1/G总权重，GT内部每anchor为1/(G*n_g)，再乘gate。cls/box筛选不重归一化。:188 mask筛选后sum(selected BCE)/eligible_GT，而非selected_GT。:190 gate.mean是anchor数均值，不能代替上述per-GT加权后的总质量。

因此同lambda的direct/selective不是等监督量对照。必须分清：有效质量sum(weight*gate)、实际loss大小、梯度范数是三种量；不能用一个替代另一个。

已有TRAIN_MASK_GATE_ANCHOR_AUDIT_PAIRED_INPUT_V2.json：相同24张增强train图，154个eligible GT，M0_s42选32、M0_s128选33；all比例20.779%/21.429%，small为14/25、16/25，large均0/33。比例是该样本集合汇总，不是按训练batch平均的全程质量，更不是梯度幅度。小目标面积是160网格前景×16代理，不是正式COCO面积。该审计未覆盖训练阶段曲线，未计算teacher独立assignment。

若新方法保留selection，至少有一个等有效总质量对照区分“选哪些”和“减了多少”；不能将全不可靠集合归一化成非零监督。新方法尚未冻结，不能事后把这个混杂当作已证明的失败原因。

## 3. 质量取舍与reference修正

旧RESULTS_MASTER.delta_AP_pp统一参考历史A0_s42。新results/PAIRED_COMPARISONS.csv直接读各run的ap.json，指定同seed reference并重新相减。

|配对|seeds|平均AP pp|平均AP75 pp|平均AP90 pp|平均small AP pp|
|---|---|---:|---:|---:|---:|
|D0−N0|128/2024|+0.06388|+0.42065|−0.51286|−0.20040|
|M0−D0|42/128|+0.02560|−0.55431|+0.71836|+0.77563|

均为n=2描述性均值，既不证明稳定改善，也不证明方法无效。M0的overall AP90两粒正向不代表small AP90同样：旧SMALL_AP_THRESHOLD_DIAGNOSTIC在small .90下seed42 TP49→54，而seed128 TP58→50（每粒132 small GT）；这是匹配计数不是AP因果分解。应检查全队列排序、FP优先级、面积ignore、bbox/mask误差，而非只比较净TP。

evaluate_full254.py实际保存两种coverage；matched.csv来自legacy class-agnostic bbox匹配。不能把整个matched.csv当same-class common-GT shape。新配对需依(image_key,GT id)稀疏连接并验证预测索引、类别；未检出记coverage缺失，不以IoU=0塞入conditional shape均值。

CPU脚本从保存的完整predictions构造COCO maxDet300、.75/.90、all/small的ignored/TP/FP排序trace，并检验存量AP。依赖导入失败，故目前没有这些新结果；已生成的表仅是存量数值重算。

## 4. 决策

有依据优先检验“监督对应与监督预算是否允许局部收益保留”，不继续堆F0式简单相加，不复跑M0_s2024，也不按旧+0.30门槛自动STOP。CrossKD作为早期成熟对手，完整设计须在真实batch和队列分析后选择，不能先写胜利结论。

P1D M1是15epoch cv4-only、mask_ratio1的specialization；与60epoch全网络ratio4直接比较存在训练机会混杂。桥接需双方75对75或事前同预算适配，预算记实。不会直接引用历史M1−M0上涨作为本轮优势。

## 5. 本次工程记录

- 源码、配置、receipt与小型指标读取；未哈希大文件，未读checkpoint内容。
- 标量表：7个模型×7指标=49行；4组同种子配对×7指标=28行；14行描述性汇总。
- 初次replay在导入pycocotools.coco时失败；无预测加载、训练或旧目录写入。随后显式捕获依赖失败，保存METRICS_RECONCILED_REPLAY_BLOCKED凭据，不冒充replay PASS。
- 未找到复盘包的指定文件于已检查cwd/下载管理路径；未声称读过LITERATURE_20。

## 完全访问恢复后的续记

以上依赖受阻/未实现描述为16时准备快照。18时权限恢复，全部7模型replay PASS；真实batch与同类common-GT完成，见analysis/FIRST_CHECKS.md。X0/I0实现与smoke完成，首批已启动。全队列尚不能支持单一因果解释；方法效果PENDING。完整执行细节以EXECUTION_JOURNAL、METHOD_SPEC和RESUME最新段为准。

## 2026-09-30 锁定确认后的最终证据更新

首批“PENDING”仅为历史快照。X0/I0/N0/I1/J0开发已完成；`CONFIRM_J0_V1` 六项事前锁定 seed31415/27182×J0/D0/N0 各60epoch、预定last独立Blueberry full254全部PASS。保存预测同一COCO evaluator replay逐项一致。J0−D0两确认seed主AP−.6491/+ .5145pp，J0−N0−.5327/+ .4379pp；两确认seed均值分别−.0673/−.0474pp，AP90也换号。开发seed42/128不合并。完整队列、coverage、共同GT条件shape和训练成本见 `analysis/CONFIRM_J0_V1_DECISION.md`。这不证明“所有KD失败”，但不支持本轮J0正向方法主张；没有发现能唯一指向简单修订的因果瓶颈。最终裁决 `NO_SUPPORTED_METHOD_AFTER_FINAL_ATTEMPT`，正文草稿以负/混合结果写法保存于 `paper/`，不写成功式摘要。用户允许少量事前冻结新消融，但剩余18.77训练进程小时不足新设计的两粒×必要对照完整配对且目前缺明确单因素靶点，所以没有追加孤立单seed训练。
