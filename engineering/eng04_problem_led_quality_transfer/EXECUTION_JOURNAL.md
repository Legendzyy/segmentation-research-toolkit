> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# ENG04 执行日志

2026-09-27 16:43：只读/准备阶段，C盘保存标量重算与源码审查。完整预测重算受权限限制，未训练。
2026-09-27 18:18：用户打开完全访问。重读prompt；无可见Python训练，E free23,554,146,304 bytes；GPU非隔离。建立E盘独立ENG04目录。
18:19–18:24：1778 train/254 val图像硬链接、labels自有副本；未读test。7模型49项AP replay与存量误差<1e-10；无历史哈希。固定24图真实batch独立TAL诊断PASS，原标签去重后ID与letterbox/overlap顺序映射验证。
18:25–18:34：实现X0/I0，数值/梯度/保存加载parity；X0训练梯度校准.25，I0沿用1/5/1；冻结首批60epoch配置。I0 AMP零项工程错误修复，失败保留；smoke fresh重试PASS。共同GT分析类别映射assert失败修复，全部coverage与既有记录一致。
18:36：有限顺序队列通过无周期trigger隐藏Windows任务启动，X0→eval→I0→eval。两项正式实验未完成，不得宣称科学结果或全任务完成。下批任务需依据结果形成科研判断。

2026-09-27 18:54:22 +08:00：用户明确要求保持低频监控直至ENG04全部任务完成；创建ACTIVE每小时ENG04 heartbeat，id eng04。现场 X0_s42 epoch6/60，队列driver28280与训练35332均活跃，E free23,178,670,080 bytes。未重启训练。


2026-09-28 03:09 Asia/Shanghai：首批X0/I0各60epoch和独立full254 PASS，队列以PENDING_RESEARCH_DECISION正常结束；累计2.000075单位/8.4603训练进程小时。CPU保存预测重放和same-class common-GT分析完成，分析见analysis/FIRST_BATCH_DECISION.md。原生N0_s42对照在科学配置NATIVE_S42_V1.json冻结；4张train图1epoch工程smoke PASS，其自动train-val不作科学结果。无test访问，E盘保留线充足。


2026-09-28 04:23:59 +08:00：首批X0/I0均train/eval PASS。CPU保存预测pycocotools replay及同类sparse GT分析PASS；I0 AP比D0_s42低.5373pp，small低2.4688pp，全队列.75/.90 TP各多7但FP各多640，不能因果归因。冻结原生N0_s42，4张train图smoke PASS；通过无trigger隐藏计划任务ENG04_NATIVE_S42_20260928启动有限N0 train→full254 eval，stderr初始空，epoch1正在运行。更新每小时ENG04 heartbeat，未重跑旧实验。

2026-09-28 07:14 +08:00：N0_s42 full254 PASS，AP .840904；四模型和完整队列/common-GT配对分析见 analysis/NATIVE_S42_DECISION.md。冻结I1分类teacher BCE去除式消融，保持I0其余科学定义、初值与训练预算。train-only审计PASS：I0−I1 loss等于分类项4.344323，I1分类头KD梯度0、box/mask非零、teacher梯度0、原生loss/部署逐位一致、空GT有限；4张train图1epoch smoke PASS，自动val不作科学证据。E free 21,855,424,512 bytes，正式启动前再核查。完整prompt仍需继续。

2026-09-28 07:16 +08:00：Git提交622b4ef冻结I1配置/实现及N0配对分析。正式前预算3.000150单位、10.800188训练进程小时、ENG04非图像元数据计579,886,833 bytes，E free21,855,309,824 bytes，无活跃ENG04 Python及I1完成/锁文件。无trigger隐藏Windows任务ENG04_I1_S42_20260928手动启动有限I1_s42 train60→独立full254 eval；初始driver PID36300、训练子进程36156/34972，以实时为准。logs/I1_s42_state.json为RUNNING，stderr初始空。每小时原ENG04 heartbeat已改为此队列检查，正常训练安静，不重复启动。

2026-09-28 13:17 +08:00：I1_s42正式60epoch和独立full254 PASS，AP .841073；已见seed42 I1−I0 +.4038pp、I1−N0 +.0170pp、I1−D0 −.1335pp。保存预测完整队列/common-GT和7项AP replay PASS，见 analysis/I1_S42_DECISION.md。按同一中心问题提出J0 D0同位置检测+I1 GT-linked quality mask的任务分工，配置DEVELOPMENT_V3事前冻结。train-only数值审计J0检测项与旧D0同batch等价、mask项与I1同batch等价，梯度/空GT/部署检查PASS；4张train图1epoch工程smoke PASS，自动val不作科学证据。正式任务尚未启动，预算约4.000187单位/16.5365进程小时，E free21,624,115,200 bytes；启动前复测。

2026-09-28 13:18 +08:00：正式前复测4.000187单位、16.536477训练进程小时、ENG04非图像新增计758,882,370 bytes、E free21,623,627,776 bytes。无活跃ENG04 Python/J0完成/锁文件，提交c407454冻结J0实现/配置/科研解释。Windows无trigger隐藏任务ENG04_J0_S42_20260928手动启动有限J0 train60→独立full254 eval；初始driver PID29052、训练进程36044/36096，logs/J0_s42_state.json=RUNNING，stderr初始空。原每小时heartbeat更新；正常时一次检查即结束。

2026-09-28 19:24 +08:00：J0_s42训练60epoch与独立full254 PASS，有限队列正常结束。总体AP/AP75低于D0，AP90/small正向，不称方法成功；正式结果及完整队列/common-GT见analysis/J0_S42_DECISION.md和analysis/first_batch。冻结J0_s128一次适应性第二开发seed；新旧科学变体、epoch/batch/input逐项比对一致，只有seed变化，runner语法审计PASS。现场无ENG04 Python，E free21,162,278,912 bytes，预算5.000187单位/22.156192训练进程小时、非图像新增868,390,571 bytes。下一步提交冻结资产后手动启动无trigger有限train→full254队列。

2026-09-28 19:25 +08:00：Git提交14176f6冻结J0结果与J0_s128协议/runner。正式前实时预算5.000187单位、22.156192训练进程小时、ENG04非图像新增868,457,287 bytes、E free21,162,188,800 bytes；无活跃ENG04 Python或J0_s128既有run/锁。无trigger隐藏Windows任务ENG04_J0_S128_20260928手动启动有限60epoch训练→独立full254 last评价；队列logs/J0_s128_state.json=RUNNING/train，driver PID39976、训练子进程39636，stderr初始空。历史D0/N0_s128只读参照。正常推进只低频检查，不重复启动。

2026-09-28 22:40 +08:00：收到用户 ENG04 候选收敛补充；以 `EXECUTION_ADDENDUM_20260928.md` 记录生效边界。现场J0_s128 epoch26/60、driver39976/child39636活跃、恢复文件更新、无train/eval completion，E free19,844,722,688 bytes。保留在跑任务及原评价计划，不更改科学定义；完成后先集中配对审核，再决定最关键验证或收敛裁决。没有启动新实验。

2026-09-29 03:29 +08:00：J0_s128正式60epoch/预定last独立full254 PASS，AP=.843956981846、AP75=.888920429、AP90=.751375048、small=.609145567。seed128 J0−D0 AP+.480079pp、AP75−.430338pp、AP90+1.651560pp、small−.151856pp；J0−N0 AP+.379422pp、AP90+.487787pp。与seed42总AP差值换号，AP90对两参照同向。三模型254图/1803GT保存预测pycocotools replay一致；覆盖/完整队列/共同GT见analysis/j0_s128。历史参照只读，配方科学字段与train/val文件名/长度核验，未重哈希大资产。裁决保留J0为待确认单一候选，不称已成立方法。

2026-09-29 03:29 +08:00：事前冻结`configs/CONFIRM_J0_V1.json`两粒新seed31415/27182×J0/D0/N0六任务完整块，安全/资源异常外不看首任务结果删减；D0代码与ENG03小源码SHA一致，N0/D0/J0各4训练图1epoch smoke PASS（自动val不作科学证据），preflight见results/CONFIRM_J0_V1_PREFLIGHT.json。提交1d402e9。启动前无ENG04 Python，E free19,557,568,512 bytes，预算6.000300单位/29.445231进程小时/非图像新增1,153,093,907 bytes。无trigger Windows任务ENG04_CONFIRM_J0_V1_20260929手动启动，03:29状态RUNNING J0_s31415 train，driver PID39252、child PID37648；六项train→full254单GPU顺序，日志、registry及状态在logs/confirm_j0_v1*。当前队列不是完整ENG04交付；低频检查后续科研结论。


2026-09-29 09:36 Asia/Shanghai: CONFIRM_J0_V1 first J0_s31415 train60 PASS. Eval failed before creating output because evaluate_full254.py seed allowlist covered only 42/128/2024; original stderr preserved as logs/J0_s31415.eval.stderr.attempt1_assert_seed.log. Engineering-only change added frozen confirmation seeds 31415/27182 to evaluator allowlist. No scientific configuration, checkpoint, endpoint, or evaluation calculation changed. Queue stopped with INCOMPLETE_CONFIRMATION; next action is evaluate the existing scheduled-last checkpoint, then resume finite queue reusing completion receipts.

2026-09-29 09:37 Asia/Shanghai: 原无trigger任务 ENG04_CONFIRM_J0_V1_20260929 经实时进程/锁/完成凭据/空间检查后手动重启。registry 明确记录 REUSED_COMPLETED J0_s31415 train，随后进入 eval；新driver PID25228、eval PID43084，以实时为准。原60epoch训练未重跑；eval attempt1 失败日志已保留。未改变 frozen 配置或科学评估。

2026-09-29 19:11 Asia/Shanghai：用户新增条件调度见 USER_DECISION_20260929_STOP_IF_NO_SIGNAL.md。原冻结 CONFIRM_J0_V1 六项不删减，完整确认后先不启动新训练；若两粒新seed仍无可复现且可辩护的主AP收益/事前应用质量取舍，则停训转独立分析、图表、证据索引和论文草稿，不包装正向方法。若有明确信号，也先做独立裁决与预算审计。此为资源与交付策略调整，不改变已完成科学结果、冻结配置或当前活跃任务。eng04低频监控已更新，保持原2小时频率。
2026-09-29 用户澄清：确认块完整结束并独立裁决后，若仍无有效结果，允许在仓库/论文资产整理及问题分析之后，事前冻结少量可区分竞争解释的新训练消融。此为后续调度授权，不改变 CONFIRM_J0_V1 六项、历史结果、主指标或预算。新增分析计划见 analysis/POST_CONFIRMATION_ASSET_AND_STORY_PLAN.md；活跃确认任务不动，未清理任何证据资产。原绝对停训表述以 USER_DECISION_20260929_STOP_IF_NO_SIGNAL.md 末尾澄清为准。

2026-09-29 23:46–23:53 +08:00：应用户要求做 E 盘空间/科研目录元数据盘点，见 analysis/DISK_AUDIT_20260929.md、DISK_METADATA_20260929.json。E free 16.503→16.502 GiB，ENG04 J0_s27182 仍正常运行；项目范围扫描逻辑156.36 GiB，其中多链接逻辑50.35 GiB，阶段间重复硬链接41.96 GiB。约95.3 GiB集中在P1B/P1C/P1D/P1F历史图像物化和科研缓存，不能把硬链接或已索引证据当可直接删除的垃圾。C/D可用6.30/13.65 GiB，不适合大项归档。仅有ENG04六个 `.pyc` 临时文件约40 KiB可直接重建，精确删除请求被自动策略拦截，未绕过；实际删除0 B、回收0 B。未改历史项目、模型、原始数据、外审包或活跃队列。

2026-09-30 04:50–05:03 +08:00：冻结六任务全部train/eval PASS，队列正常结束为 `CONFIRMATION_BLOCK_EVALUATED_PENDING_DECISION`，无ENG04训练进程，E free约16.37GiB。复用保存的val预测运行src/analyze_confirm_j0.py，六项同一COCO evaluator AP replay PASS，并输出锁定两seed配对/完整队列/共同GT条件形状及收据；新增结果总表42条绝对指标、配对表28条指标。J0−D0确认主AP−.6491/+ .5145pp，J0−N0−.5327/+ .4379pp，AP90亦换号，见analysis/CONFIRM_J0_V1_DECISION.md及图。资源账12.000300单位/53.2308进程小时/ENG04新非图像约1.696GB，未越18/72/12GiB和E free≥8GiB。按用户条件调度停止J0扩种与结果驱动补救；分析现有消融、最小论文组合和剩余公平预算后决定不追加孤立新训练，写作负/混合结果及最终裁决NO_SUPPORTED_METHOD_AFTER_FINAL_ATTEMPT。未读test，未修改旧阶段或外部项目。

2026-09-30 05:10 +08:00：完成 `FINAL_REPORT.md`、paper方法/结果/claim草稿、analysis最小论文资产审查、确认图及结果总表；`completion/FINAL_RESEARCH_DECISION.json` 记录阶段与四选一裁决。建立约224KiB的精简最终外审包 `delivery/ENG04_final_evidence_20260930.zip`，仅文本、表、图、小收据与关键源码，不含大数据/权重/完整预测/test；2026-09-28旧外审包原样保留为历史快照。更新README与元数据级ARTIFACT_INDEX，不重算大型历史资产哈希。准备最终一致性检查并暂停ENG04低频监控。

2026-09-30 12:58:21 +08:00：按用户要求释放E盘空间。元数据确认P1D artifacts/specialization_cache 4个checkpoint-specific train派生缓存各1,781文件；在ENG04归档 analysis/asset_archive/P1D_specialization_cache_20260930/ 保存旧P1D artifact index中对应的5,343条原路径/长度/SHA条目、源index SHA-256及3类小manifest副本。删除P1D BASE45_s20260919、BASE60_s128、BASE60_s2024 三个目录（29,778,931,000 B逻辑文件），保留 BASE60_s42 作为一套可重放代表缓存。E盘free从29,328,388,096 B升至最终59,188,928,512 B（净增29,860,540,416 B /27.81 GiB，当前55.12 GiB）。仅清理P1D train-derived specialization cache；原始图像/标签/checkpoint/源码/日志/报告和P1D旧索引均保留；未读test、未发现Python训练进程。旧P1D artifact_index.json 是清理前的历史快照，当前删除路径见上述归档映射。ENG04 ARTIFACT_INDEX.json 仅补入这两项新归档记录。

2026-09-30 13:11:46 +08:00：为及时释放空间，清理P1D四个checkpoint-specific train-derived specialization_cache目录：7,124个文件、39,706,628,882逻辑字节；保留各目录小型input/completion/normalization副本和旧P1D artifact_index中的全部旧路径/长度/SHA条目。随后清理P1B已压缩、可由原PNG重建的BGR .npy 输入缓存2,032个文件、40,591,627,340逻辑字节；保留原PNG硬链接、dataset manifest、artifacts/decoded_disk_cache.json（含逐图decoded-pixel SHA和像素相等记录）、代码、报告、checkpoint、logs。P1D特征缓存已纳入历史负结果，不是独有原始证据；删除会增加后续重放计算成本。无Python训练进程时执行，未碰其他进程。新归档位于ENG04 analysis/asset_archive；ENG04 ARTIFACT_INDEX仅登记五项小型归档记录，P1D旧索引保留为清理前快照。E盘初始29,328,388,096 B，清理过程中因并发写盘显著波动；当前读取 72583192576 B（67.598 GiB）。原始数据、标签、权重、报告、日志、checkpoint均未删除；未读test。

