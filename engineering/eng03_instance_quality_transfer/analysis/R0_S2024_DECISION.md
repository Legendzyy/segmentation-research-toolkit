> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../../docs/PROVENANCE.md)。

# R0 ranked-anchor development decision

2026-09-26, Blueberry development full254/1803 GT at input640. R0_s2024
completed a fresh 60-epoch run from the frozen initialization after a
separately preserved interrupted first attempt. The scheduled last checkpoint
passed the independent evaluator; smoke and automatic training validation
scores were not used to select weights. `R0_S2024_PAIRED_EVALUATION.json`,
`r0_s2024_instance_evidence.csv` and `R0_S2024_SMALL_GT_MATCHES.json` are the
machine-readable evidence. The earlier attempt is not merged into the final
checkpoint or treated as a strict continuation.

| Full254 mask endpoint | D0_s2024 | R0_s2024 | R0−D0, pp |
|---|---:|---:|---:|
| AP | .844379 | .840318 | −.4062 |
| AP50 | .931708 | .928048 | −.3660 |
| AP75 | .895112 | .888962 | −.6150 |
| AP90 | .745004 | .742619 | −.2385 |
| Small AP | .622610 | .611878 | −1.0731 |
| Medium AP | .832904 | .826649 | −.6254 |
| Large AP | .929379 | .930423 | +.1043 |

At score≥.25, same-class box coverage is 1731/1803 for D0 versus
1720/1803 for R0; this fixed operating point is descriptive, not an AP
decomposition. Among 1712 common same-class GT, 1705 have quality candidates
aligned with both evaluators' mask records. On that conditional set, R0 mean
mask IoU changes −.000877 and boundary F −.001134; among 106 small aligned
GT, mean IoU changes −.003998. The 132 COCO-small GT at mask IoU .90 have
42 matches in both, 12 D0-only, 8 R0-only and 70 neither. Thus the training
anchor-alignment proxy improved, but the actual deployment AP and small-GT
high-IoU outcomes did not. Candidate ranking, gate feedback, changed mask
targets and training stochasticity remain competing explanations; one seed
does not identify a unique cause or refute all anchor-selection ideas.

**Decision: STOP R0 seed expansion.** The user-directed adaptive policy
requires a substantive coherent development signal before seed 2. R0 has
negative overall, high-IoU and small AP versus its same-seed D0 comparator,
without a compensating coverage or coherent subgroup/cost benefit. Do not
train R0_s42/128 to rescue it or select another checkpoint. This does not
change M0_s2024's prior zero-epoch STOP or historical results. The most
valuable next evidence is an equal-budget same-seed native/K1 strong-control
comparison against D0; seed42-only historical A0/K1 rows cannot establish
multi-seed advantage. Freeze those controls before running them.

R0 attempt 2 training-process time was 9851.3 s on a shared GPU; attempt 1
consumed about 100 minutes and is counted separately. Independent evaluation
took 166.2 s on a shared GPU. These are not isolated deployment latency.
No test or external data were accessed. E: reserve remained above 8 GiB.
