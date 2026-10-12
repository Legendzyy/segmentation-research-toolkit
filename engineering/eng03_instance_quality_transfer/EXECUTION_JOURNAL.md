> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# Execution journal

- 2026-09-25 12:50 Asia/Shanghai — Started ENG03; read user prompt and
  required historical reports. ENG02 K2 STOP is retained as historical
  protocol outcome, not a ban on distinct output-level experiments.
- 2026-09-25 12:53 — Built full254 cross-model instance/candidate table
  from A0/A2/K1/K2 saved ENG02 predictions and GT cache, without modifying
  historical assets. The historical ENG02 box match was class-agnostic;
  ENG03 additionally computed same-class greedy IoU≥.5/score≥.25.
- 2026-09-25 12:56 — Same-class A0/A2 common 1698, A2-only 21, A0-only
  24; 20/21 A2-only have a low-score same-class A0 box at IoU≥.5. Wrote
  `RESEARCH_CHARTER.md`. No AP mechanism or causal claim inferred.
- 2026-09-25 12:57–13:03 — Prioritized E: live-space audit at user request.
  Free space 21.129 GiB, then 21.126 GiB over ~88 seconds. No ENG03 writer
  at audit; an unrelated NewResearchProject materialization had increasing
  cumulative write counters and was untouched. No safe temporary deletion.
  Local train/val view uses image hardlinks and copied labels, not duplicate
  8.6 GiB image blocks. Details in `DISK_AUDIT.md`.
- 2026-09-25 13:06–13:20 — D0 and Q0 **non-scientific** two-batch/one-epoch
  train-path smokes exited normally. On one train-only numeric batch, native
  loss with zero KD differed by 0; empty-GT KD was 0; teacher gradient was
  0; student KD gradient nonzero; selective class/box/mask fractions were
  0.478/0.789/7-of-9. Rendered and visually inspected one actual augmented
  training GT/student/teacher target overlay on the common 160² grid. The
  GT mask region and teacher/student regions coincide spatially; this does
  not prove general alignment. Fused deployment graph was numerically close
  under atol .003/rtol .001; max absolute output difference .0044 on a large
  raw output and maximum leaf mean absolute difference 6.5e-6. Evidence:
  `analysis/NUMERIC_AUDIT.json`, `analysis/TARGET_OVERLAY_TRAIN_BATCH.png`.
  The short-run val numbers are intentionally excluded from model selection.
- 2026-09-25 13:22 — Froze `configs/DEVELOPMENT_V1.json` for formal D0/Q0
  pair, seed42, 60 epochs, batch8, last-epoch selection, fixed A2 teacher
  and native n initialization. E: free 20.918 GiB; no files deleted.
- 2026-09-25 13:23:58 — Started only the frozen formal D0→Q0 sequence
  using `src/queue_development_v1.py` in a hidden local process. Windows
  launcher PID 69072, real Python driver PID 73996; first D0 child launchers
  PID 70688/83912. Live E: free before D0 22,452,097,024 bytes (20.910 GiB).
  Formal D0 directory was absent before launch. Driver and per-job stdout/
  stderr are in `logs/`; completion will be explicit. An hourly low-noise
  thread heartbeat `eng03` will inspect state and continue scientific work
  after the queue finishes.
- 2026-09-25 13:36 — D0 finished epoch 1/60, emitted `recovery_full.pt`
  (86,917,257 B) and best/last student weights (23,344,238 B each), then
  entered epoch 2. E: free 20.767 GiB. No completion receipt yet. Prepared
  ENG03-only full254 evaluator, results master, claim matrix, method spec and
  paper drafts while the training process continued; those drafts explicitly
  mark ENG03 AP and stronger/paired/external evidence pending.
- 2026-09-25 20:16 — Frozen D0 and Q0 seed42 each completed all 60 scheduled
  epochs with exit code 0, last-epoch weight and explicit PASS receipt. D0/Q0
  process times were 13,868.7/10,845.1 s on a shared GPU (not isolated GPU
  hours). Independent full254/1803-GT input640 mask evaluation then passed:
  D0 AP .842408; Q0 AP .841307; historical A0 .840904 and K1 .842336.
  The single-seed output-KD increment over K1 is negligible. Q0 loses .1101
  pp AP to D0, gains .9860 pp AP90, .5108 pp small AP and six score-.25
  same-class box matches. Detailed conditional comparisons and limitations:
  `analysis/DEVELOPMENT_V1_DECISION.md`. Evaluation wall times 189/161 s
  were on the shared GPU and are not isolated latency. No test access.
- 2026-09-25 20:47 — Froze `DEVELOPMENT_V2.json` for the two missing gate
  factorial cells M0 (direct detector/selective mask) and C0 (selective
  detector/direct mask), retaining v1 teacher, initialization, native loss,
  weights, 60-epoch schedule, batch and last-epoch checkpoint. A first
  train-only audit script failed because Ultralytics lazily initializes its
  criterion; the audit script was fixed, with no formal run involved. Its
  rerun passed exact component-algebra equalities and nonzero student/zero
  teacher gradients (`analysis/NUMERIC_AUDIT_V2.json`). The sampled mask gate
  happened to select all nine GT; the earlier v1 numeric audit and formal Q0
  first-batch audit documented nontrivial mask selection. The next formal
  package remains a development mechanism check, not paired confirmation.
- 2026-09-25 20:48 — Started only the frozen M0→C0 seed42 sequential queue
  after confirming D0/Q0 PASS receipts, no ENG03 training process, no V2
  lock or run directory, and E: free 24.162 GiB. Hidden Windows launcher
  PID 51316; actual Python driver PID 91576; M0 child launchers 91216/92012.
  `development_v2_state.json` and registry show M0 START; stderr empty at
  launch. Do not start a second queue. The same 10/9 GiB disk launch/epoch
  guards and explicit completion receipts apply. C0 starts only after M0
  exits with PASS; no formal M0/C0 result exists yet.
- 2026-09-26 04:07 — M0 and C0 finished their frozen 60-epoch seed42 jobs
  sequentially, exit 0 with PASS receipts and last/recovery checkpoints.
  Training-process times were 12,609.4 and 13,702.7 s; total ENG03 four-job
  usage is 51,025.9 s (14.174 h), four of 24 formal units. No queue/training
  process remained at 04:55; E: free 23.779 GiB.
- 2026-09-26 05:03 — Independently evaluated both last checkpoints on the
  full254/1803-GT input640 val set, PASS receipts. M0 AP .842282, AP90
  .746360, small AP .630261; C0 AP .838899, AP90 .745435, small AP
  .610730. Updated `RESULTS_MASTER.csv` and generated four-cell common-GT,
  coverage, boundary/thin and arithmetic interaction outputs in
  `analysis/DEVELOPMENT_V2_COMPARISON.json`. See
  `analysis/DEVELOPMENT_V2_DECISION.md`: M0 has a single-seed small-object
  signal at essentially equal overall AP to D0; C0 overall AP decreases.
  These are development results, no paired or external confirmation. No test
  access or isolated latency claim; no cleanup of evidence.
- 2026-09-26 05:07 — Froze `configs/REPLICATION_V1.json` before any new-seed
  training: D0/M0 with seeds128/2024, 60 epochs, identical variant recipes
  except seed, same last checkpoint and independent full254 evaluator. Syntax
  and contract preflight PASS. No ENG03 GPU/queue process or prospective run
  directory existed; E: free 23.729 GiB. Launched one hidden sequential queue
  `src/queue_replication_v1.py`, launcher PID 71980, Python driver PID 49200;
  initial D0_s128 children 95740/56576. Registry shows D0_s128 START and
  stderr empty. No K1/mature-neighbor run launched. Next checks must inspect
  live state and completion before action, not duplicate jobs.
- 2026-09-26 13:56–14:02 — User changed only ENG03 seed scheduling. D0_s128
  and M0_s128 already had 60-epoch PASS receipts; D0_s2024 was still actively
  training (~29/60), M0_s2024 had no run directory. Added a waiting
  evaluation barrier to the next M0_s2024 child (the active D0 process had
  loaded its previous source and was not touched). Wrote the adaptive policy
  before inspecting seed128 validation AP: release third seed only if M0-D0
  overall AP ≥−0.20 pp and small AP ≥+0.50 pp; report AP75/AP90, coverage
  and common-GT shape regardless. These numbers operationalize the user's
  qualitative scheduling rule, not a significance or equivalence claim.
  Queued post-D0 independent full254 seed128 evaluations in an idle helper
  PID 91640/85288, and a separate analysis/decision helper PID 59720/82716.
  Both helpers were observed waiting with empty stderr, barrier PENDING.
  GPU 4060 Laptop 8,188 MiB had 3,972 MiB in use while D0 trained, so
  evaluation was deferred until D0's normal completion. E: free 23.239 GiB;
  no deletion, historical edit, test access or other-project intervention.
- 2026-09-26 16:04 — D0_s2024 completed 60 epochs PASS with unchanged
  scientific recipe and 13,829.3 s training-process time. The post-D0 helper
  independently evaluated D0_s128/M0_s128 on full254/1803 GT, both PASS;
  decision helper compared them with seed42. Seed128 M0-D0: AP +0.0638 pp,
  AP75 -0.4430 pp, AP90 +0.8535 pp, small AP -0.2780 pp. Seed42 small
  delta had been +1.8292 pp. Registered adaptive rule failed on small AP,
  barrier STOP. M0_s2024 exited with an explicit zero-epoch
  `SKIPPED_BY_ADAPTIVE_SEED_POLICY` receipt. Queue terminal state says
  `TRAINING_PAIR_REPLICATION_COMPLETE` but only D0_s128, M0_s128 and
  D0_s2024 trained in that queue. All associated helpers exited; no ENG03
  training process remained. E: free 24,970,248,192 bytes (~23.26 GiB).
  No cleanup or test access. See `analysis/SEED128_ADAPTIVE_DECISION.md`.
- 2026-09-26 16:10 — Independently evaluated D0_s2024 scheduled last
  checkpoint, full254/1803 GT PASS: AP .844379, AP75 .895112, AP90 .745004,
  small AP .622610. Evaluation elapsed 149.3 s on a shared GPU (not isolated
  latency). CPU-only saved-prediction replay localized the seed-dependent
  small-AP reversal to high mask-IoU thresholds among 132 small GT; see
  `analysis/SMALL_AP_THRESHOLD_DIAGNOSTIC.json`. Refreshed `RESULTS_MASTER.csv`
  with evaluated seed128 and D0_s2024 rows plus an explicit zero-epoch
  M0_s2024 skip row. Seven trained formal units total; 89,970.9 s (~24.992 h)
  cumulative training-process time. E: free 24,968,511,488 bytes (~23.26 GiB).
- 2026-09-26 17:07 — Read-only heartbeat found no active ENG03 Python process,
  all prior PASS/SKIPPED receipts unchanged and E: free 24,961,404,928 bytes
  (~23.25 GiB). CPU-only replay of the four saved seed42/128 D0/M0 full254
  predictions at mask IoU .90 found small GT transitions 42: both39,
  D0-only10, M0-only15, neither68; 128: both46, D0-only12, M0-only4,
  neither70. It also saved per-GT identities and matched scores. Updated
  paired interpretation and wrote a read-only strong-baseline/P1D M1 bridge
  audit; no new training, external data, test access or cleanup.

- 2026-09-26 17:55 — Fixed-input train-only gate/anchor replay and numeric R0
  audit passed. The preliminary unpaired smoke was retained and explicitly
  marked invalid for cross-seed comparison. On 24 identical augmented train
  images enriched for small GT, the geometric-center positive matched a
  deployed score-.25 NMS anchor for 4/21 and 4/24 small matched GT (seeds
  42/128), versus 10/21 and 12/24 for the top detached class-score positive.
  These are exploratory train-image alignment proxies, not validation AP or
  a causal result. R0 changes only M0's mask-KD representative TAL-positive
  anchor to this top-score positive. Numeric audit on two train images:
  native no-op diff 0, detector-KD components exact M0/R0, finite changed
  mask loss, nonzero student gradient and zero teacher gradient. One-epoch,
  four-image R0_s2024 engineering smoke exited 0; its automatic val output
  was not used for scientific selection. `configs/DEVELOPMENT_V3.json` was
  frozen before the formal run for one seed2024/60-epoch last checkpoint;
  D0_s2024 is the existing same-seed comparator. E: live free
  24,887,783,424 bytes (~23.18 GiB), no ENG03 training process, seven formal
  units/~24.992 process hours consumed. No test access, cleanup or changes
  outside ENG03.

- 2026-09-26 19:41 — Formal R0_s2024 attempt 1 was found abruptly stopped in
  epoch 29/60, with completed epoch-28 `results.csv` row and 86,917,321-byte
  `recovery_full.pt`, but no completion receipt or live Python process.
  Standard stderr is empty and stdout ends mid-progress; exact termination
  cause/exit code is unavailable. The full run and stdout/stderr were moved
  intact within ENG03 to `runs/R0_s2024_attempt1_interrupted` and matching
  `logs/*attempt1_interrupted*` names. This failed partial attempt consumed
  about 100 minutes/~0.48 formal 60-epoch unit. No strict checkpoint resume
  is claimed: loader state is not proven replayable. Attempt 2 will restart
  from the same frozen seed2024 initialization/configuration, preserving all
  first-attempt evidence. E: free 25,275,592,704 bytes (~23.54 GiB) at
  audit; no other project was altered.

- 2026-09-26 19:43 — Registered and manually started one Windows Task
  Scheduler job `ENG03_R0_s2024_attempt2_20260926` to avoid coupling a
  multi-hour Python process to the current tool session. The one-time
  trigger was disabled immediately after the manual start to prevent a
  duplicate scheduled launch; the current task instance remained Running.
  Driver state `logs/R0_s2024_attempt2_driver.json` recorded STARTED,
  PID 28548, fresh initialization and no prior-attempt resume. Trainer
  Python descendants were observed; `runs/R0_s2024` was newly created.
  E: free at launch 25,275,539,456 bytes (~23.54 GiB), leaving >15 GiB
  above the hard reserve. Formal budget before attempt 2: seven completed
  units/~24.992 process hours plus attempt 1's ~0.48 unit/~1.67 hours.
  `eng03` hourly heartbeat prompt was updated to monitor this specific
  attempt and independent full254 evaluation, without repeat launch.

- 2026-09-26 22:53 — R0_s2024 fresh attempt 2 completed 60/60 epochs PASS;
  driver exited 0, scheduled last.pt and recovery_full.pt present, stderr
  empty. Independent full254/1803-GT input640 evaluation PASS using last.pt:
  mask AP .840318, AP75 .888962, AP90 .742619, small AP .611878. Versus
  existing same-seed D0_s2024: −.4062/−.6150/−.2385/−1.0731 pp,
  respectively. Same-class score-.25 coverage 1720 vs 1731 GT; aligned
  common-GT mean IoU −.000877. Among 132 COCO-small GT at mask IoU .90,
  D0-only12/R0-only8. Adaptive development decision STOP R0 seed expansion;
  see `analysis/R0_S2024_DECISION.md`. R0 attempt 2 consumed 9851.3 s;
  total prior complete jobs 24.992 h plus interrupted attempt1 ~1.67 h
  plus R0 attempt2 ~2.736 h = ~29.40 training-process hours, eight full
  60-epoch jobs plus a partial ~.48 unit. Shared GPU timing is non-isolated.
  E: free 24,875,012,096 bytes (~23.17 GiB) before evaluation; no test
  access, cleanup or other-project intervention.

- 2026-09-26 23:03 — Entered the R0 independent full254 result and STOP
  decision into `RESULTS_MASTER.csv`, preserving both R0 attempts and all
  prior evidence. Built ENG03-owned same-budget native N0 and feature-KD K1
  control trainer, importing the frozen ENG02 K1 model read-only. Both
  one-epoch/four-image engineering smoke runs exited 0; their automatic
  validation scores were excluded. `configs/STRONG_CONTROL_V1.json` was
  frozen for N0_s2024 then K1_s2024, 60 epochs each, fixed last checkpoint.
  See `analysis/STRONG_CONTROL_V1_RATIONALE.md`. E: free ~23.07 GiB; no
  active ENG03 process, no existing formal N0/K1 run. This is a new matched
  strong-control package, not a rerun of historical A0/K1 or R0.

- 2026-09-26 23:04 — Registered and manually started Windows Task Scheduler
  job `ENG03_STRONG_CONTROLS_V1_20260926`, then disabled its one-time trigger
  to prevent a second scheduled launch. The task remained Running. Driver
  PID 23344 wrote `logs/strong_controls_v1_state.json` with TRAINING
  N0_s2024; N0 child PID 22544/20392 was observed, empty stderr and new
  ENG03-owned stdout. The queue is frozen N0_s2024→K1_s2024, one GPU job at
  a time, each 60 epochs and last checkpoint. E: free before first job
  24,763,056,128 bytes (~23.06 GiB), with 8 GiB hard reserve and 10/9 GiB
  start/epoch guards. Neither historical assets nor ICASSP were touched.

- 2026-09-27 01:51 — N0_s2024 completed 60/60 epochs PASS, last/recovery
  checkpoint and receipt present, 7998.4 s training-process time. Queue
  automatically started K1_s2024 at 01:17, but its process vanished during
  epoch 2 with no completion and no Python stderr; the Windows task returned
  0xC000013A (control-console termination). Task Scheduler had interactive
  logon and default stop-if-going-on-battery=true; a session/power transition
  or another external termination is possible, not proven. Preserved K1's
  complete files under `runs/K1_s2024_attempt1_interrupted` and matching
  `logs/K1_s2024_attempt1_interrupted.*`; last completed epoch is 1. No
  strict loader-state replay is proven, so the frozen K1 recipe will restart
  from initial seed2024 state, counting partial time/epochs separately.
  Attempted a tiny S4U scheduler-token GPU probe, but Windows denied task
  registration; no probe ran and no CUDA claim was made. Independent N0
  full254/1803-GT evaluation PASS using last.pt: mask AP .842095, AP75
  .893193, AP90 .743623, small AP .628707. Same-seed D0 AP .844379
  (+.2284 pp) but small AP .622610 (−.6098 pp); no comparative decision
  until K1 evaluation. E: free about 22.85 GiB after evaluation.

- 2026-09-27 01:57 — Registered and manually started independent scheduled
  task `ENG03_K1_s2024_attempt2_20260927` for a fresh K1 seed2024 run from
  the frozen initial weights. Disabled its one-time trigger after starting
  to prevent duplicate execution. The task has battery-start and
  battery-continuation enabled. At 01:59 it remained Running with live driver
  PID 31068 and trainer PID 27048/7960, stdout advancing in epoch 1, no
  stderr, and no completion yet. `logs/K1_s2024_attempt2_driver.json`
  records `fresh_from_initialization=true`, `prior_attempt_resumed=false`.
  E: free at launch was 24,523,735,040 bytes and at 01:59 was
  24,523,665,408 bytes (~22.84 GiB). The old interrupted attempt remains
  intact and counted separately. Do not infer why it terminated; do not
  restart the old queue. Shared GPU time is non-isolated.

- 2026-09-27 05:03 — K1_s2024 fresh attempt2 trained 60/60 epochs PASS
  (7900.9 s process time), last/recovery checkpoints and receipt present;
  independent full254/1803-GT evaluation PASS. The same-seed N0/K1/D0
  mask AP is .842095/.842411/.844379. D0−N0 +.2284 pp AP but −.6098 pp
  small AP; D0−K1 +.1968 pp AP and +2.5962 pp small AP. Fixed score-.25
  same-class coverage 1717/1709/1731 GT. Aligned common-GT mean IoU
  differences are small and conditional. See
  `analysis/STRONG_CONTROL_V1_DECISION.md` and paired JSON/CSV. No
  multi-seed superiority, isolated latency, or mature-neighbor claim.
  Updated `RESULTS_MASTER.csv` to include all three controls and R0.

- 2026-09-27 05:03 — Froze one F0_s2024 simple additive control (D0
  GT-corresponded direct output KD + K1 three-neck feature-MSE). The code
  was committed before formal launch. Two fixed training images/9 GT gave
  native noop and output-parity differences 0, positive student/adapter
  feature gradients, zero teacher gradient, finite loss, empty-GT output KD
  zero, and deployment allclose. One-epoch/four-train-image smoke exited 0;
  its automatic val scores were ignored. Registered/manual-started Windows
  task `ENG03_F0_s2024_20260927`, then disabled its one-time trigger.
  Driver `logs/F0_s2024_driver.json` STARTED PID22760, trainer
  PID26100/26628 observed, stdout training-data scan active, stderr empty.
  E: free at launch 23,988,703,232 bytes (~22.34 GiB), above 8 GiB
  reserve; ten completed 60-epoch units plus two interrupted partials
  precede F0. Shared GPU process time is non-isolated. No test access.
- 2026-09-27 09:02 — F0_s2024 completed 60 epochs PASS from fresh initialization and independent full254 last-checkpoint evaluation PASS. AP .840628; F0−D0 −.3751 pp overall, −.4381 pp AP75, −.1021 pp AP90, +.3976 pp small. Fixed score-.25 same-class coverage −6 GT and aligned conditional IoU −.000446. See `analysis/F0_S2024_DECISION.md` and paired JSON/CSV. F0 expansion STOP under adaptive policy. No scientifically supported simple additive benefit, external result, mature-neighbor comparison or novelty claim.
- 2026-09-27 09:02 — Froze `configs/STRONG_CONTROL_V2.json` for exactly one N0_s128 60-epoch matched native run against already completed/evaluated D0_s128. Pre-recorded K1_s128 consideration gate in `analysis/F0_S2024_DECISION.md`; it is a resource filter, not a significance test. `train_controls.py` dispatches V1 seed2024 unchanged or V2 seed128; frozen science fields were compared and syntax passed. No ENG03 Python process or prior N0_s128 run existed. E: free 23,765,151,744 bytes; estimated run output <0.3 GiB, above 8 GiB reserve. No test or other-project write.

- 2026-09-27 09:03 — Registered and manually started one-shot Windows task `ENG03_N0_s128_20260927`, then disabled its future trigger. Driver STARTED PID23140, trainer PID9640/29200 observed at model load/AMP checks, stdout active, stderr empty. E: free before launch 23,762,280,448 bytes, above reserve; formal run fresh from frozen initialization/seed128. No existing N0_s128 run or active ENG03 Python was present at launch. Full254 evaluation and the predeclared K1_s128 resource gate await completion. No other project or test access.
- 2026-09-27 12:08 — N0_s128 frozen native training 60/60 PASS and independent full254 last-checkpoint evaluation PASS. D0_s128−N0_s128 overall AP −.1006568 pp, AP75 +.6494032 pp, AP90 −1.1637735 pp, small AP +.2089789 pp. Fixed-threshold same-class coverage +12 GT and 1700 aligned common-GT mean mask IoU +.000695 do not offset the complete AP loss. The pre-recorded +.10 pp overall resource gate failed, so K1_s128 was not started. Against seed2024's +.2284 pp D0−N0, overall direction reversed. Created `analysis/N0_S128_PAIRED_EVALUATION.json`, per-GT CSV, `analysis/N0_S128_DECISION.md`, and visually checked `analysis/PAIRED_NATIVE_D0.png`. Formal completed jobs 12/24 (37.601 completed-job process hours) plus preserved R0/K1 interrupted portions; E: free 23,682,613,248 bytes. Delivered PAUSE-B final report, method/claim/paper drafts, reproducibility guide and compact artifact index. No active ENG03 Python, no test or historical/ICASSP changes.
