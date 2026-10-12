> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# ENG04 第一批冻结设计：I0 与早期成熟对照 X0

2026-09-27，尚无正式结果。固定问题：teacher的实例监督能否让局部改善保留到完整预测mask AP。

## 决策依据（首版）

24张未增强train图、130 GT，初始化student正anchor与teacher TAL同身份比例44.46%，其余主要是teacher未分为正例，未观测到另一GT身份。D0/M0终点同身份比例95.69%/96.23%。不能据此声称普遍错误对应。初始化同格teacher mask IoU均值.96188，teacher自身同GT最高box-IoU候选的mask IoU .97122；仅为train样本观察，不是可部署oracle收益。初始化与终点不是同一训练轨迹，且采用eval BN。

M0 hard gate在所查终点batch的平均mask监督质量仅.02604；D0终点若应用相同gate为.05155。分母一直是全部eligible GT。这支持研究早期目标供给与任务强度，不支持把selection单独命名为已经有效的贡献。

## I0：两个紧密相关的训练组成

1. **GT-linked teacher target**：独立运行teacher与student TAL。对每个有student positives的GT，从teacher自己分配到同GT的anchors中选decoded box IoU最大的一个（同值按最低索引）；还需类别argmax正确且box IoU>.5。分类迁移该候选的true-class sigmoid；box在输入坐标解码后SmoothL1，不跨anchor KL offset bins；mask用teacher自己的coeff/prototype解码。student mask仍用距GT中心最近的student TAL positive，与D0相同。
2. **连续任务质量权重**：检测权重为q_t*sigmoid((q_t−q_s)/.05)，q为对GT的box IoU；mask使用独立mask IoU，并要求teacher mask IoU>.5。质量及候选全detach。每GT检测项在其student positives中平均，再对所有student-positive GT平均；mask也以所有该GT为分母。未获teacher候选或不合格时跳过transfer、保留native GT。不会把空集合强行归一为单位监督。

总loss为native + warmup*(cls + 5*box + mask)。三个epoch线性warmup：(epoch+1)/3截断到1。当前不加部署模块、不增加feature-MSE或CrossKD到I0。

作用：稳定跨模型实例目标的来源，减少teacher较弱任务对student的约束。副作用：GT质量权重本身改变监督量和难度混合、mask单代表anchor仍可能偏离最终预测、teacher候选为训练GT引导。均需验证，不能称已解决排序。背景/非true类别由native损失负责；不是分类softmax蒸馏。

必要后续对照：普通D0、native、X0；若I0有用，去除质量权重/去除GT-linked来源中的关键消融，并以相同有效权重的简单控制区分来源与强度。若主张依赖GT加权，还须teacher-free同权重GT控制。暂不自动启动这些任务。

## X0：CrossKD head-input YOLO adaptation

依据官方GFL实现，保留冻结teacher head、student cross-path梯度、按通道mean/std对齐、KD-QFL beta1及同位置DFL KL T1（回归系数4）。采用head输入截点0，三个neck 1x1适配器解决YOLO11n/s通道差，送入teacher cv2/cv3。与官方默认idx3/GFL、ATSS和相同head宽度有区别：本适配用YOLO TAL正例数归一分类、无GT整batch跳过KD，mask保持native监督。这是核心机制适配，不是论文全复现，也未实现mask CrossKD。

固定2张train图的学生梯度L2：native216.81，X0未缩放KD866.64，I0 KD12.62。为避免近邻任意过强，X0系数预置.25并同样3epoch warmup；I0沿用D0 1/5/1。不根据验证成绩选系数。X0与I0都获得必要数值/训练短测，若近邻失败会先查实现与优化，不直接声称文献方法无效。

## 公平比较与检查

两者seed42、60epochs、640/b8、AdamW/nbs32，沿用ENG03 native训练recipe与初始化；scheduled last评估，禁用early stopping，自动val/best不用于决策。seed42是已见开发种子。正式训练时不从smoke权重续跑。P1D75epoch桥接、最终两粒配对确认、MinneApple teacher与配对均未实施。

已做native关闭parity、teacher零梯度、student KD梯度、cross adapter梯度、空GT、深拷贝/序列化后部署bitwise parity。I0首个AMP smoke发现连接零项half sum溢出导致NaN，尚未优化；修复为float32 sum，保留原失败目录/日志。该修改只修数值零，不改变损失定义。两种smoke仅4张train图，自动评价同4张train图，不作科学证据。

## 2026-09-28 任务分工修订 J0（开发假设，不是成功结论）

I1 是 I0 移除分类teacher BCE的单因素消融；其seed42 full254整体AP仅比同配方N0高.0170pp，但AP90/small有有限正向，且D0的AP/AP75仍更强，完整配对见 `analysis/I1_S42_DECISION.md`。因此冻结J0：检测使用与ENG03 D0数值等价的student-TAL同位置teacher true-class BCE及decoded-box SmoothL1（系数1/5、每GT平均），mask仅使用I1的teacher-own sameGT合格候选、quality权重及全GT分母（系数1）。保留native GT loss和3epoch warmup，不引入feature MSE或推理模块。目的是使检测排序路径与较强的D0一致，同时检验跨位置高质量mask目标能否保留I1的AP90/small信号；它不是已证明互补，更不能以局部指标替代完整AP。与D0/I1/N0/X0同seed比较，正式评价仍是预定last的full254。train-only数值审计证明J0检测两项与D0实现同batch一致、mask项与I1实现同batch一致，native关闭逐位一致、teacher梯度0、student检测及mask分支梯度非0、空GT与保存部署检查PASS；4张train图1epoch工程smoke PASS且其自动val不是科学结果。
