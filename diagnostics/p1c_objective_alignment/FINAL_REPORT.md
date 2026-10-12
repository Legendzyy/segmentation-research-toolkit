> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

P1C VERDICT: F — MIXED MECHANISM

EXP-SIS-20260919-P1C · 2026-09-19

状态：正式实验与补充诊断完成；结果与证据如下。

已有表示可以通过继续训练、提高监督分辨率和通用 coefficient 重参数化得到小幅收益；本轮没有发现值得作为独立新方法推进的 native-decode alignment 机制。不能给出“coefficient 侧没有任何工程机会”的结论：B2r1、B4 的 AP75 与 small AP 在三个种子上都高于原模型。也不能把这些小幅收益升级为论文主线：B3 失败，通用训练与容量基线已解释主要可学习改善，创新风险高，且只有一个模型、一个验证环境。

P1A 永久保持 **E**；P1B 永久保持 **A + STOP**。本轮不恢复 H/P、conditioning 或 dual-source 故事。

| 必报状态 | 结论 |
|---|---|
| LOSS_PATH_AUDIT | PASS；明确分辨率、GT/predicted support、overlap target、TAL/面积加权及 score-ranked AP 的差别 |
| MASK_RATIO_EFFECT | PARTIAL POSITIVE；ratio1 稳定改善 AP90、boundary、matched IoU，但相对 B1 的 AP75/small 优势不稳定，不能称为解释大部分 oracle gap |
| HEAD_FINETUNE_EFFECT | PARTIAL POSITIVE；B1 三种子 AP/small/boundary 均提升，AP75 有一个种子下降 |
| DECODE_ALIGNMENT_EFFECT | NOT SUPPORTED；B3 开发种子 AP75/small 同时下降，按预注册规则停止扩展 |
| CAPACITY_CONTROL | GENERIC REMAPPING SUPPORTED；纯 coefficient B4 已产生同量级 matched gain，并有三种子 full-quality 收益；并非新增视觉信息证据 |
| COEFFICIENT_ONLY_CONTROL | PASS；COEF 不读取 geometry，CONST 为全局 residual，名义参数量均为10,912；有效函数类并不相等 |
| AP75_TRANSLATION | B2r1/B4 三种子正向；B1/B5 不稳定；B3 负向 |
| SMALL_AP_TRANSLATION | B1/B2r1/B4 三种子正向；B5 不稳定；B3 负向 |
| THRESHOLD_CROSSING_PATTERN | 匹配子集与完整 AP 队列不一致；REGRESSION-TO-THE-MEAN PATTERN = FALSE（预注册群体定义） |
| MASK_AREA_BIAS | SHRINK；native-support 组更明显；不能统一解释成 SMOOTH |
| NOVELTY_RISK | HIGH；25项 primary works/官方实现审计，predicted-box crop 和训练期改进有直接近邻 |
| PUBLICATION_MAINLINE | 当前 coefficient/decode-alignment 新方法主线 STOP；保留工程基线，最终行动 PIVOT |

## 正式结果与门槛

18个正式训练成员均使用固定15轮的最后 checkpoint：10个 seed42 配置，B1/B2r1/B4/B5 再各做128、2024。连同 B0 共19个成员全部完成254-val、1803 GT 的评估。B2r1 是预先指定的 ratio 候选；B2r2、G4/G5、C4/C5 为单种子辅助组。B3 的停扩展由事前“AP75 与 small AP 同时低于 B0”规则触发，不能据此宣称它已获得三种子否证。

下表为相对 B0 的变化。AP 列单位为**百分点**；IoU、boundary F 为0–1原尺度差值。三种子正向表示三个观测值同号，不代表统计显著性或跨数据集复现。

| 方案 | 种子数 | ΔAP | ΔAP75 均值 [范围] | Δsmall AP 均值 [范围] | ΔAP90 | Δmatched IoU | Δboundary F |
|---|---:|---:|---|---|---:|---:|---:|
| B1 原 head/原 objective = B6 | 3 | +0.3664 | +0.1115 [-0.1361,+0.3958] | +0.7820 [+0.4395,+0.9992] | +0.8757 | +0.002048 | +0.001575 |
| B2 ratio1 | 3 | +0.5565 | +0.0965 [+0.0300,+0.2245] | +0.5555 [+0.3834,+0.7195] | +1.4550 | +0.003683 | +0.003838 |
| B3 native decode | 1 | +0.5247 | -0.1918 | -0.5072 | +1.4383 | +0.003319 | +0.003747 |
| B4 COEF/原 objective | 3 | +0.4271 | +0.2700 [+0.0967,+0.4122] | +0.6001 [+0.3916,+0.9706] | +0.9226 | +0.002225 | +0.002592 |
| B5 COEF/native objective | 3 | +0.5630 | -0.0117 [-0.0588,+0.0244] | +0.2612 [-0.0169,+0.6579] | +1.5427 | +0.003634 | +0.004181 |

B0 的 AP/AP75/AP90/small AP 分别为83.96855/89.16347/73.38649/59.81913。全部逐成员 AP50/medium/large、边界、轮廓、FP/FN、面积和效率见 [RESULT_TABLES.md](RESULT_TABLES.md)，机器精度数值见 `artifacts/analysis/full_results.json`。

最关键的同结构比较是 B3−B2r1：seed42 的 AP75 **-0.4163**、small AP **-1.0709** 个百分点，matched IoU -0.000293。B3−B1 对应 -0.5876/-0.9468 个百分点。整体 AP 的微增不能覆盖这两个主判据的下降。B5−B4 在三个种子上 AP75 都下降（-0.1555/-0.4130/-0.2766点），尽管 AP90、boundary 和 matched IoU 都提升。

**PART II = NOT STARTED。** 第12节门槛未通过；不加入 Dice、boundary loss、quality weighting 或 residual gate。P1B及P1C均未出现预注册的“低质量均值改善、高质量均值下降”模式，也不满足以此启动 identity gate 的前提。无P1D大规模实验或跨模型扩展。

## 具体机制与阈值证据

固定 source commit `b454f423600f99d41730bd75a7a26b491187de36` 的 loss.py 实际把 prototype 上采样到监督 target 网格；注释中的 GT 下采样分支未执行。因此 ratio4/2/1 分别对应160/320/640监督，ratio1不是重复160分辨率的伪对照。

训练原路径是 `a·U(P) → BCE → GT-box support → GT-area normalization`；native 路径是 `U(a·P) → strict logit>0 → predicted-box crop`。B3 将 BCE 作用于 native 连续 logits 的 predicted-box support，保留相同 overlap GT、TAL assignment、GT面积权重和优化器。线性组合与双线性插值在实数算术下可交换；B2r1/B3 的主要干预是 support，不能把算子顺序本身包装为新机制。二值阈值不可导，“exact”不表示训练目标已等价于完整 AP。详见 [LOSS_PATH_AUDIT.md](LOSS_PATH_AUDIT.md)。

seed42 的固定匹配全集 crossing 如下，单元格为 up/down/net；全部种子、small 子集和十个阈值保留在 `artifacts/analysis/p1c/threshold_crossings.csv`。

| 方案 | t=.75 | t=.80 | t=.85 | t=.90 | t=.95 |
|---|---|---|---|---|---|
| B1 | 12/2/+10 | 9/3/+6 | 9/3/+6 | 33/15/+18 | 58/21/+37 |
| B2r1 | 12/1/+11 | 10/6/+4 | 14/6/+8 | 45/16/+29 | 79/31/+48 |
| B3 | 10/5/+5 | 13/11/+2 | 21/15/+6 | 51/22/+29 | 97/36/+61 |
| B4 | 8/1/+7 | 6/0/+6 | 8/5/+3 | 25/10/+15 | 56/15/+41 |
| B5 | 13/5/+8 | 14/8/+6 | 16/14/+2 | 50/19/+31 | 97/33/+64 |

B3 的固定匹配 NetCross75=+5，但完整 class-aware COCO TP 净变化为 -4：diagnostic组+5、其他高置信度组-1、confidence<.25组-8。small AP75 的 diagnostic组净0、低置信度组净-3；低置信度组 active small FP 增加339。TP计数本身仍不能重构AP，因为还有分数排序和precision插值。

P1B P0/42 同样是固定匹配 +7、完整 TP -8；低置信度组贡献 -14。其三种子官方 small AP 平均下降1.4404点；只冻结原检测面积参与 unmatched ignore-rule 的**非标准诊断**下，下降变为0.0821点，差1.3583点。标准COCO从预测mask计算面积，shrink 会把部分 unmatched predictions 移入small范围，改变FP资格。这是可观测的评价机制，不是改写正式AP的理由。置信度分组的反事实也不等于选择了可部署gate，见 [P1B_AP_DIAGNOSIS.md](P1B_AP_DIAGNOSIS.md)。

P1B所有21成员的 native IoU≥.9 均值变化均正，19/21 AP90提高。P1C所有18成员的高质量组均值与中位数也均正，AP90全部提高；其中约24%–33%的高质量实例仍受损。个别严重损伤需要披露，但不能据此称为系统性高质量均值回归。B3高质量均值+0.002578、中位数+0.002731，27.63%实例受损。散点图和完整分位分布均已保留。

面积偏置为 SHRINK：B1约79%–83%、B2r1约90%–91%、B4约80%–86%、B5约95%–96%的匹配mask缩小；B3为95.37%。B3平均 FP -56.01、FN +37.38像素，B2r1/42为 FP -41.86、FN +23.73。precision提高而recall下降；原模型平均面积比1.01995，B3变为0.99916。面积向1靠拢并不保证每个mask改善，也不能保证small AP改善。

补充topology覆盖全部19成员和32,832条匹配实例记录。GT细结构定义为Zhang skeleton中距背景≤2 input像素的点：全体有2,000点（510实例），small有197点（44实例）。native分别漏755/53点。下面三种子组按42/128/2024顺序列出；这是真实栅格窄结构的覆盖诊断，不等于所有语义细枝，skeleton量化毛刺是已知限制。

| 方案 | 全体漏细结构像素 | small漏细结构像素 | Δ归一化周长（全体） |
|---|---|---|---|
| B1 | 815 / 807 / 806 | 53 / 54 / 52 | +0.00434 / +0.00309 / +0.00878 |
| B2r1 | 840 / 835 / 853 | 54 / 55 / 55 | +0.03523 / +0.03392 / +0.04040 |
| B3 | 911（单种子） | 59 | +0.03902 |
| B4 | 812 / 807 / 813 | 54 / 55 / 53 | +0.00500 / +0.00543 / +0.00645 |
| B5 | 900 / 888 / 888 | 62 / 60 / 61 | +0.03651 / +0.03652 / +0.03727 |

所有18个修正成员在全体窄结构上都比native漏得更多；small方面B1/B4并非一致受损，B5则三种子一致增加遗漏。所有成员的全体归一化周长都增加，且B3/B5连通分量增加，不支持统一“边界变平滑”解释。GT真实hole仅269像素、small仅2像素，不能支撑广泛hole-filling故事。B3真实hole被填像素减少8，却新增301个GT前景中的false-hole像素；B5三个种子false-hole增量为284/179/6，B4则减少1,028/1,393/321。总hole面积与错误hole面积方向可以不同，完整定义和逐实例值见 `artifacts/analysis/p1c/topology`。

39个固定代表实例的梯度诊断：original160/ratio1平均 cosine 0.81683，original160/native为0.74967，ratio1/native为0.91680。前两组各1/39出现反向，后一组无反向；native IoU≥.9的9个代表中没有负cosine。仅改变组合/插值顺序时 cosine≈0.999999985，说明顺序不是主要机制。归一化单步并未普遍损伤高质量组。空缺分层如 small [0.5,0.6) 已披露，39例不是全体估计，cosine也不是论文贡献。

## 对十个问题的回答

1. **P1B P0 gain主要来自什么？** 证据更支持已有 coefficient 的通用可学习重映射和训练目标/权重带来的小幅纠偏。B4无新增信息，三种子matched改善0.002065–0.002333，已接近P0的0.002–0.003量级；全局CONST也能改善均值。但P0含P5且训练样本、target和权重不同，不能给出P0收益的严格因果百分比分解，也不能声称本轮已直接做了同协议P5消融。
2. **是否需要新增 inference information？** 获得本轮小幅收益不需要。B1/B2保留原head，B4只读a；geometry辅助对照没有一致优于COEF的证据。不能推广为任何任务都不需要新信息。
3. **单纯继续训练head是否足够？** 足以改善平均质量、overall AP和small AP；不足以保证AP75三种子均提高，B1/2024下降0.1361点。它也没有消除约0.03的oracle gap；15轮结果不证明任意训练预算下已收敛。
4. **监督分辨率是否解释gap？** 解释一部分可学习改善。B2r1相比B1三种子都提高AP、AP90、boundary、matched IoU，但AP75在两种子下降，small AP也在两种子下降。不能说“resolution解释大部分gap”，更不能把ratio1作为新方法。约0.03是此前受约束oracle诊断量，不是本轮可严格相除的认证上界。
5. **exact native-decode监督有独立价值吗？** 当前固定recipe下没有满足部署主判据的独立价值。B3的AP75/small同时低于B0而触发停扩展，也低于B2r1；B5相对B4的AP75在三种子均下降。这里报告观测差值，不声称统计显著，也不排除其他未测试recipe。
6. **为什么matched IoU涨而AP75/small掉？** matched集合只覆盖高置信度固定pair；AP覆盖所有GT/低置信度候选、class-aware重新匹配及排序。其外的低置信度行为、不同阈值crossing和mask面积导致的small FP资格变化能够抵消matched收益。P1B和B3的完整cohort表及固定反事实提供直接证据。
7. **高质量mask是否regression-to-the-mean？** 按事前定义FALSE。P1B与P1C高质量组均值正，P1C中位数也正；存在部分损伤但不是普遍高质量尾部退化。不能用负相关或IoU上限效应代替检验。
8. **是否有shrink/expand/smoothing偏置？** 稳定SHRINK，native-support更强；全体不支持统一SMOOTH标签。需结合FP/FN、归一化perimeter、连通分量、thin skeleton和真假holes，而非只看面积或boundary F。
9. **不同objective的coefficient方向冲突吗？** 有少数实例和明显角度差异，尤其低分辨率与640监督之间；没有证据支持高质量组普遍反向。ratio1/native平均方向较接近，纯operator-order几乎一致。
10. **是否继续coefficient方向？** 不继续以新coefficient模块、H/P或decode-alignment为论文主线。保留B2r1、B4作为已有信息可优化的工程对照，将问题转向训练样本/目标权重与完整评价队列的一致性。该转向仅为诊断结论与后续建议，不在本轮启动新的模型、loss或数据集实验。

## 推理成本、局限与复现

B1/B2/B3更新160,224个既有head参数；部署总参数2,842,998不变，网络估计9.786675 GFLOPs不变。残差组增加10,912个名义参数，总数2,853,910，每个保留candidate增加21,504次dense乘加计数；其有效函数容量随输入约束不同。COEF不使用box/class/confidence，训练后metadata置乱仍bitwise不变；head全部18个BN buffer保持初值。B1=B6，避免重复命名预算控制。

19个成员×12图的在线原模型推理与缓存评估binary masks逐像素一致。用户要求ICASSP并行，所有计时成员均观察到另一个Python GPU任务。B0平均78.54ms，其余约80.51–121.56ms仅为共享负载下观测值，**不能据此估计独占GPU的额外延迟或宣称零实测延迟**。零额外参数/相同算子图与实测零延迟是不同主张。VRAM为本进程tensor peak，并包含在线一致性核验暂存及checkpoint，不等同于纯网络激活内存或整卡占用。详细协议、P95和原始samples见结果表及 `artifacts/resources`。

重要范围限制：一个固定clean YOLO11、一个254-val集合，其中完整small GT仅132个；辅助geometry/CONST/ratio2仅单种子；B3按规则只做一个种子。head/residual学习率不同，跨结构比较不是纯参数量因果实验。重采样CI仅覆盖固定成员的验证image-cluster变化，不是训练种子或外部数据不确定度。overlap训练target与独立评估GT仍有19,870像素差异，B2r1/B3保持相同target而不宣称完全对齐AP。所有正式结果只使用最后epoch，未使用test outcome。

novelty审计覆盖25项primary works/官方实现，证据深度在矩阵中逐项标明，并非全部论文均完整方法复现。官方YOLACT早已有 `mask_proto_crop_with_pred_box`，高分辨率mask监督、训练期辅助目标和quality-aware ranking亦有近邻。具体证据与链接见 [OBJECTIVE_NOVELTY_MATRIX.md](OBJECTIVE_NOVELTY_MATRIX.md)。本轮没有“未找到完全相同代码就算新方法”的推断。

复现入口：[PROTOCOL.md](PROTOCOL.md)、[MEASUREMENT_NOTES.md](MEASUREMENT_NOTES.md)、[EXECUTION_JOURNAL.md](EXECUTION_JOURNAL.md)。科学配置SHA256为 `3abbf9205676a585160e3972cd4d7da65bda4fcdccbb11e6421def1d4ae07203`；baseline SHA256为 `fe653f3463bddc072bb84730b7a1294720af73076686c000b826e15dd9a9399c`。每个stage的exact CLI、git commit/diff、source snapshot、stdout/stderr和退出码在 `artifacts/runs`；checkpoint hashes/freeze map、完整预测/系数、AP tensors/matching、crossing、梯度和文献检索日志均保留。数值合同、原资产完整性、最终交付核验与全量索引分别见 `artifacts/audit`、`artifacts/delivery_closure.json`、`artifacts/artifact_index.json`。

最终原资产重哈希PASS：P1B 6,818文件、P1A 512文件、2,032条原数据记录及2,032个decoded pixel cache均保持原值；历史git树和固定上游source保持clean。初始loss/gradient/native-forward合同、训练后BN/COEF/CONST合同和deterministic interpolation补充合同均PASS。后者最大loss差3.5763e-7、coefficient gradient差2.9803e-8，低于预先固定的2e-5容差；这是数值等价，不是声称与baseline AMP训练轨迹bitwise一致。

最终delivery检查PASS：18个checkpoint均为固定15轮、权重有限、config与baseline哈希一致；每成员254张系数输出齐全；228次在线binary-mask一致性检查通过，完整COCO cohort映射无丢行，全部要求的诊断与报告资产存在。

选择PIVOT而非GO：没有满足独立decode机制与novelty门槛；选择PIVOT而非“所有coefficient操作均无部署收益”的STOP总判词：B2r1/B4确有三个种子一致的AP75/small收益。当前coefficient新方法论文主线停止，工程事实如实保留，后续干预位置应重新审视训练与完整评价的对应关系。

PIVOT
