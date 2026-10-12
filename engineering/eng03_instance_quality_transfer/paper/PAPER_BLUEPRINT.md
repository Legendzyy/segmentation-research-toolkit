> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../../docs/PROVENANCE.md)。

# Paper blueprint — PAUSE-B evidence package

**Working topic:** When GT-corresponded instance supervision fails to improve a light segmenter's complete prediction queue. This is a development-stage negative-evidence and methods-analysis outline, not an affirmative new-method submission or a finalized title.

## Question and contribution boundary

Blueberry full254 native YOLO11n versus YOLO11s teacher leaves a measurable mask AP gap. Our fixed-score same-class diagnostic finds 20/21 teacher-only GT have a low-score student candidate. We asked whether GT-linked class, box and rendered mask supervision, task-dependent selection, or combining feature and response transfer closes the *complete-prediction* AP gap. The implemented training paths and independent evaluator make this question auditable. Two matched native seeds show an overall AP sign reversal; Q0/M0/R0/F0 do not establish a robust new mechanism. Thus an affirmative utility/novelty narrative is unsupported.

## Potential manuscript structure if the research later advances

1. Define the difference between conditional GT/mask quality, fixed operating-point coverage and ranking-based mask AP, retaining P1C failure modes.
2. Specify native TAL-positive GT identity, teacher/student common-grid mask target and the exact gradient/deployment paths (`METHOD_SPEC.md`).
3. Present direct D0, task-selective Q0/M0/C0, ranked-anchor R0, feature K1 and additive F0 without hiding failures.
4. Use two-seed matched native N0/D0 chart (`analysis/PAIRED_NATIVE_D0.png`) to show that even +12 fixed-score GT and +.000695 common-GT IoU in seed128 coexist with −.1007 pp complete AP.
5. Only after a revised mechanism gives a robust positive effect, add a faithful mature KD adaptation, paired seeds, MinneApple development, isolated efficiency and sealed test under separate authorization.

Main available table: `RESULTS_MASTER.csv` with 18 rows, including one explicit zero-epoch skip and five historical ENG02 rows whose training provenance differs. Figure 1: `analysis/PROBLEM_EVIDENCE.png`; Figure 2: `analysis/PAIRED_NATIVE_D0.png`. A method-flow diagram is textually specified in `METHOD_SPEC.md` but no validated final method graphic is claimed. External and mature-neighbor rows must remain “not run,” not zero or negative. Shared-GPU process times are not isolated latency.

**Claim for a current report:** the attempted GT-linked supervision is implementable, but its local quality/coverage diagnostics did not reliably become full AP gain under this development protocol. **Not claimable:** first instance KD, superior full AP, small-object robustness, generalization, isolated speed, superiority to CrossKD/GID, or submission readiness. The next stage needs a single concrete, preregistered mechanism tied to final candidate ranking/high-IoU failure; this package does not pretend to have implemented it.
