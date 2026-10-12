> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# ENG04：实例质量迁移的最终证据入口

状态（2026-09-30）：X0/I0/N0/I1/J0 开发和事前锁定的 J0/D0/N0 两粒新 seed 完整配对确认已完成。六项确认训练与独立 Blueberry full254 评价均 PASS；队列已结束，无活跃 ENG04 训练。**J0 未得到可复现的完整 mask AP 收益，不能写成已成立的新方法。** [最终研究报告](FINAL_REPORT.md)、[确认结果与独立判断](analysis/CONFIRM_J0_V1_DECISION.md)及写作资产已交付，低频监控已暂停。报告如实标注缺少外部配对、同预算 P1D 桥接和隔离 latency。

先看这些文件：

- 原研究问题与约束（原资产，本次未收录：`USER_REQUEST_ENG04.md`）、[研究契约](RESEARCH_CHARTER.md)、[方法定义](METHOD_SPEC.md)、[开发/资源日志](EXECUTION_JOURNAL.md)。
- [冻结的确认设计](configs/CONFIRM_J0_V1.json)、[六项配对原始表](analysis/confirm_j0_v1/PAIR_TABLE.csv)、[确认图](analysis/confirm_j0_v1/J0_PAIRED_EFFECTS.png)、完整队列与共同 GT（原资产，本次未收录：`analysis/confirm_j0_v1/RECEIPT.json`）。
- [现有消融与最小论文贡献审查](analysis/MINIMAL_PAPER_ASSET_REVIEW.md)、[claim 边界](paper/CLAIM_EVIDENCE.md)、[方法草稿](paper/METHOD_DRAFT.md)、[结果草稿](paper/RESULTS_DRAFT.md)。
- 磁盘与硬链接盘点（原资产，本次未收录：`analysis/DISK_AUDIT_20260929.md`）、历史缓存价值与空间整理（原资产，本次未收录：`analysis/CACHE_VALUE_AND_SPACE_RECLAMATION_20260930.md`）、[现有模块组合复盘](analysis/METHOD_COMBINATION_REASSESSMENT_20260930.md)、近邻顶会方法与复用审查（原资产，本次未收录：`analysis/RECENT_ADJACENT_LITERATURE_AND_REUSE_20260930.md`）、[结果总表](results/RESULTS_MASTER.csv)、[配对总表](results/PAIRED_COMPARISONS.csv)。

用户要求的 外审压缩包（原资产，本次未收录：`delivery/external_audit_20260928/EXP-SIS_external_audit_20260928.zip`） 是 **2026-09-28 历史快照**，形成时 J0_s128 仍在运行；它不包含本次完整确认。当前结论须以本目录新报告、正式收据与结果表为准，不能把旧 ZIP 当最终复验包。

ENG04 最终精简证据包（原资产，本次未收录：`delivery/ENG04_final_evidence_20260930.zip`） 含本轮裁决、配对表、图、冻结配置、关键源码和六项小型完成/AP收据（约224 KiB）；不含原图、标签、checkpoint、完整预测或 test，不是可独立重训的复制仓库。包内 `HANDOFF_MANIFEST.json` 列出精确成员。

关键数值：两粒新确认 seed31415/27182 的 J0−D0 主 AP 为 −0.6491/+0.5145 百分点，J0−N0 为 −0.5327/+0.4379；AP90也换号。开发 seed42/128 单列，不能并入锁定确认。Blueberry full254 是项目 development 评价，不能称社区官方 leaderboard 或 final test。所有历史 P1A–P1F、ENG01–03 和外审交付包保留原样；ENG04 仅引用，不回写。

经用户补充，若后续确有实例级证据指向唯一最小修订，允许先冻结少量新训练消融。但当前剩余训练进程时间不足以在新机制上完成新的两粒×必要对照完整配对，且没有已辨识的单因果瓶颈，因此没有启动结果驱动的新训练。具体判断与未来最小实验蓝图在上述资产审查文件。test 仍封存；共享 GPU 计时非隔离。

