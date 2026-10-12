> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# P1D engineering-mainline qualification

Status: **COMPLETE — STOP / COEFFICIENT-LINE-CLOSED**. Prior and delivery integrity checks passed, and the final artifact index is complete.

The fresh45/60 horizon bridge, all scheduled curve evaluations, three independent BASE60 baselines, three fresh75 equal-budget controls, B1/M1/M2/M3 specializations at seeds42/128/2024, and the BASE45→M2 bridge diagnostic completed with hash-verified final checkpoints and full254-image validation. `BASELINE_CONVERGENCE_STATUS=INCONCLUSIVE`; the registered BASE100 trigger did not fire.

Neither M2 nor M3 passed the all-seed AP/AP75/small plus fresh75-mean gate. M3 also crossed the seed2024 raster-thin regression limit. MinneApple remained unopened. See [FINAL_REPORT.md](FINAL_REPORT.md) for the required verdict,12 statuses,12 answers and STOP decision; [QUALIFICATION_RESULTS.md](QUALIFICATION_RESULTS.md) for the compact three-seed table; and `artifacts/figures/` for the inspected figures.

The warm-start full-network no-augmentation control was not run because its optimizer/scheduler contract was still explicitly unfrozen when specialization outcomes became known. It cannot be selected after results and presented as preregistered evidence. This limitation does not cause the STOP: the mandatory fresh75 and subgroup gates already fail.

Historical P1A/P1B/P1C assets, original data and `${OTHER_PROJECT_ROOT}` remained read-only. Test outcomes were not read. Shared-GPU resource observations are labeled as such and are not isolated latency certification.
