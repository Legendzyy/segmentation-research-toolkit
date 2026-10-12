> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# EXP-SIS-20260921-P1E execution journal

- Protocol freeze: commit `fb529c9`; primary checkpoint and deterministic 64-image validation sample fixed before outcomes.
- Candidate extraction: PASS, run `20260921T222738_436180_candidate_bank`; one earlier TAL-state engineering failure is preserved and did not alter scientific settings.
- Candidate summary: PASS, run `20260921T223431_865257_summarize_candidates`; `CANDIDATE_MASK_ALIGNMENT=MODERATE`.
- Global/local oracle: PASS, run `20260921T223514_293456_oracle_diagnosis`; 453 GT, 446 selected, 61 thin.
- Verdict synthesis: PASS, run `20260921T224645_982978_summarize_p1e` (the preceding malformed CLI is retained as failed evidence).
- Oracle convergence sensitivity: PASS, run `20260921T224952_247577_oracle_stability_audit`; thresholded thin metrics unchanged.
- Visual cases: PASS, run `20260921T225312_967018_visual_cases`.
- Interaction/bootstrap audit: PASS, run `20260921T225428_669164_interaction_analysis`.
- Final outcome: `C. THIN-PROTOTYPE CAPACITY BOTTLENECK`, decision `GO`; one P1F thin-prototype blueprint, no P1E training.
- Generated: 2026-09-21T23:05:39.523469 Asia/Shanghai workstation context.
