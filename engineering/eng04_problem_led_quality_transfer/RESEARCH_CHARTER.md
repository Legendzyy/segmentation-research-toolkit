> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# ENG04 研究契约与当前执行边界

阶段：EXP-SIS-20260927-ENG04。2026-09-27。状态更新（18:36 Asia/Shanghai）：权限已恢复，首批X0→I0正式队列已启动；下文开工读数及环境故障是历史记录。

中心问题固定为：轻量果实实例分割中，强模型的实例监督能否改善完整预测 mask AP，并使局部识别、定位和几何改善在部署预测中保留。不能以仅 coverage、oracle 或 small AP 上涨替代主问题。历史 STOP/PAUSE 不作为本轮科学门槛，但保留其原文。

当前选定的研究切入点是**有效实例监督与实际预测之间的对应及监督量混杂**。先完成三项检查，再冻结一个完整方法，最多两个核心组成。现阶段没有证据把所有历史负结果归因于 anchor 错配，也未给新方案起成功式名称。

## 首批工作及资源

1. 已执行：阅读 ENG01–03 报告、ENG03 实际损失与 evaluator、修正配对 reference；核读 CrossKD 论文和官方 GFL 实现。
2. 部分完成：监督分母静态审计及已有 24 张训练图审计复核。还需固定真实 batch，分别提取 student/teacher TAL 分配及逐任务有效权重质量。
3. 部分完成：保存完整预测的 CPU replay 脚本已实现；环境依赖受阻，尚未得到新 TP/FP/排序重算结果。旧的分阈值结果仅作为回顾性线索。
4. 待前述证据完成：冻结完整设计及 faithful-core CrossKD YOLO 适配，先审计梯度路径、空集合、坐标解码、BN 状态、质量分母，再开始 seed42 正式开发。

预算：总上限 18 个 60epoch 等价单位、72 训练进程小时；开发最多8单位，至少10单位留给确认、核心消融和外部配对。初始拟分配：成熟近邻1，完整设计1，关键分量/等质量对照2，必要新baseline/桥接与一次有依据修订合计最多4；不强行用满。最终验证两粒配对种子整组冻结；不能根据其中第一粒结果中断后声称完成确认。外部teacher、smoke、失败尝试均计费。若75epoch桥接，每个run计1.25单位。

新资产≤12GiB，E盘始终至少8GiB空闲。16:43–16:44 本机时间元数据读数：E free=23,557,881,856 bytes（约21.94GiB），C free=9,754,255,360 bytes（约9.08GiB）。E当前理论可用 min(12GiB, free−8GiB)=12GiB；该值不是未来预授权，启动前重读。C仅存小型准备文本/表，不放训练和数据副本。

2026-09-28 更新：首批X0/I0、原生N0与去除分类teacher项的I1均完成单seed正式训练及独立full254。I1恢复了I0相对N0的损失，但整体AP相对N0仅+.0170pp且不及D0；未兑现论文主张。基于D0较好的整体AP/AP75与I1较好的AP90/small有限信号，在同一中心问题内事前冻结J0任务分工修订，见 `analysis/I1_S42_DECISION.md` 与 `configs/DEVELOPMENT_V3.json`。这是开发种子假设；最终两粒配对确认及外部证据仍未实施，不以单seed宣称稳定或创新成立。

## 环境边界

目标为 ${RESEARCH_ROOT}/engineering/eng04_problem_led_quality_transfer/。
本会话仅 ${HISTORICAL_WRITABLE_ROOT} 及指定可视化目录可写，审批模式 never；因此正式E盘产出受阻。没有尝试绕过、建立计划任务、借其他窗口代写或修改旧实验。

Win32 CIM盘/进程枚举返回拒绝访问；Get-PSDrive成功；Get-Process未显示python，但nvidia-smi存在不可见进程，故**不能确认GPU隔离或全系统无训练**。没有停止任何进程。

历史实验解释器可以运行numpy，但pycocotools不可导入，历史vendor/pycocotools目录枚举被拒绝。完整预测replay依赖受阻；未安装包、未修改旧环境。ENG03 common模块导入会创建旧目录，故不导入它。

不创建周期聊天监控，不恢复ENG03监控；不访问test，不改P1A–F/ENG01–03/NewResearchProject。正式执行需在目标E目录可写的会话中接续，先检查本准备包避免重复。

## 2026-09-27 18:36 更新

完整访问恢复后，E盘目标目录建立，合法train/val图像硬链接复用，label复制到ENG04；旧资产只读。pycocotools现可正常导入，7模型49项保存预测AP重算PASS；共同GT类别编码修复后coverage与旧凭据一致。真实batch检查见results/TRAIN_CORRESPONDENCE.json；源码实现、两项train-only smoke通过，正式配置见configs/DEVELOPMENT_V1.json。当前训练X0，之后独立评价、I0训练、独立评价；无后续模型自动扩张。不存在周期监控。

## 2026-09-30 最终证据边界

上文准备阶段的权限/环境状态及“PENDING”描述为历史快照，后续事实以 `FINAL_REPORT.md` 和六项正式收据为准。当前中心问题保持原样，J0/D0/N0 两新seed锁定配对全部完成，J0主AP及AP90效应换号、均值近零，故当前方案不支持正向论文claim；阶段状态 `CENTER_PROBLEM_UNSUPPORTED`，四选一建议 `NO_SUPPORTED_METHOD_AFTER_FINAL_ATTEMPT`。用户允许少量冻结后新消融，但没有充足训练时间完成新机制的公平两粒对照，也无唯一实例级机制指向，因此本轮停止新增训练、整理论文资产。历史资料、失败尝试、test边界及共享GPU非隔离标签保持不变。
