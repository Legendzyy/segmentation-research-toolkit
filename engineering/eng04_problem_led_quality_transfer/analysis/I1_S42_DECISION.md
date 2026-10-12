> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../../docs/PROVENANCE.md)。

# I1_s42 去除分类teacher项后的配对决定

2026-09-28。I1从与I0相同的冻结学生初值、teacher、seed42、Blueberry train、640/b8、AdamW/60epoch重新训练；唯一科学改动为GT-linked teacher true-class BCE系数1→0。训练及预定最后checkpoint的独立full254均PASS，见 `runs/I1_s42/completion.json`、`analysis/evaluation/I1_s42/completion.json`。训练图数值审计证实I1 KD对分类头梯度为0、box/mask仍非0。以下差异单位为百分点，均属已见seed42开发证据。

| 候选−参照 | AP | AP50 | AP75 | AP90 | small AP |
|---|---:|---:|---:|---:|---:|
| I1−I0 | +0.4038 | +0.4951 | +0.0530 | +0.6660 | +2.6854 |
| I1−N0 | +0.0170 | +0.0411 | +0.1608 | +0.2599 | +0.3851 |
| I1−D0 | −0.1335 | −0.1155 | −0.5069 | +0.3277 | +0.2166 |

保存预测由同一pycocotools算法重放，全部7项AP与独立evaluator输出误差<1e−10；这只是算法重放一致性，不是另一个评估算法。完整score≥.001队列中，IoU.75/.90的I1 TP分别1712/1459、FP4700/4953；I0为1722/1464、FP6519/6777，N0为1707/1461、FP4694/4940。I1候选数6412，I0为8241、N0为6401。低分FP计数不能独立解释AP，但与分类项移除后的候选规模变化一致。score≥.25同类boxIoU≥.5覆盖I1为1720/1803，I0为1725、N0为1722、D0为1729，因此不能声称覆盖改善。

I1−I0共同GT1706，其中1698个旧legacy匹配索引与同类索引一致；条件mask IoU +.000494、boundary F +.001828，8个明确排除。I1−N0共同GT1707/可对齐1700，条件mask IoU −.000081、boundary F +.000042；这是接近持平而非形状普遍获益。I1的两个类别small AP分别.631763与.596505；相比I0的.611742/.562819均提高，但类别2仍低于N0的.600016。完整AP的正负变化和局部shape不是可互相替代的endpoint。

**解释边界：** 单因素干预支持“在I0这套配方、seed42下，teacher分类项对最终结果有不利净效应”；尚不能证明它通过特定FP机制、校准或所有种子起作用。I1相对同配方N0仅+.0170pp整体AP，无法称为稳定完整预测改善；相对历史D0仍−.1335pp，AP75明显落后。I1在AP90和small上有有限正向，提示mask/实例几何监督可能保留价值，但同种子AP90小于因果证明的证据需求。

**下一次有限开发设计J0，正式前需单独冻结及审计：** 同一学生、teacher和native recipe，检测分支使用D0的同格student-TAL GT-positive true-class BCE及decoded box SmoothL1（保持D0系数1/5和每GT分母），mask分支使用I1的teacher-own same-GT合格候选、独立mask质量权重及全GT分母（系数1）。三epoch warmup与现有一致。这个任务分工针对D0较好的完整AP/AP75与I1较好的AP90/small取舍：检测仍用student位置teacher输出以维护原D0排序路径，mask才跨anchor取GT-linked高质量teacher目标。它不是D0和I1所有项相加，也不同于ENG03 F0的feature-MSE叠加。最直接比较为同seed N0/D0/I1及I0；若J0仅局部改善或完整AP不超过强参照，应收缩为负结果。先做同batch D0检测loss数值等价、J0任务梯度/空GT/部署parity及train-only smoke，成功才占用一个正式开发单位。当前已用4.00015/18单位、16.532/72训练进程小时；开发还可用约4单位，但验证保留至少10。共享GPU为非隔离；不读test。
