> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# EXP-SIS-20260920-P1D — final engineering qualification

## P1D VERDICT

**H. NO PUBLISHABLE MAINLINE**

The coefficient-specialization line is closed under the registered P1D rules. The experiments retain a useful engineering signal, especially for retraining the existing coefficient head and for the single-seed BASE45→M2 bridge, but neither M2 nor M3 passed the strong-baseline, equal-budget, three-seed and subgroup gate. MinneApple therefore remained unopened.

## Required statuses

| Status | Result | Evidence |
|---|---|---|
| `BASELINE_CONVERGENCE_STATUS` | **INCONCLUSIVE** | Fresh BASE60 minus BASE45 was AP −0.002260, AP75 −0.001805 and small AP −0.008126. The registered BASE100 trigger did not fire. |
| `SPECIALIZATION_BEYOND_EXTRA_TRAINING` | **NO** | No variant beat fresh75 in three-seed mean on AP, AP75 and small AP simultaneously. M3 deltas were +0.004525, −0.001961 and +0.009819. |
| `B2_INDEPENDENT_VALUE` | **PARTIAL** | M1 improved AP/AP75/small against paired M0 in every seed, with mean deltas +0.005253/+0.000658/+0.002602, but mean AP75 was −0.003101 versus fresh75. |
| `B4_INDEPENDENT_VALUE` | **PARTIAL / NOT QUALIFIED** | M2 mean AP improved +0.003038 versus M0, but small AP declined in seeds42 and128 and AP75 declined in seed2024. |
| `B2_B4_COMPLEMENTARITY` | **NO** | M3 was not above both M1 and M2 on AP/AP75/small across every paired seed. |
| `MEGA_BLUEBERRY_3SEED_STATUS` | **FAIL** | Neither registered candidate M2 nor M3 satisfied all-seed primary positivity plus the fresh75 mean comparison. |
| `MINNEAPPLE_STATUS` | **NOT RUN — GATE CLOSED** | The Mega Blueberry qualification gate failed; no MinneApple assets or outcomes were opened. |
| `SHRINK_BIAS` | **PRESENT** | On common matched GT, mean predicted-area ratio shifted downward in every seed: approximately −0.005 to −0.007 for M2 and −0.014 to −0.016 for M3. |
| `THIN_STRUCTURE_STATUS` | **LIMITING** | M3 seed2024 aggregate raster-thin recall changed −0.050424 versus M0, just beyond the registered −0.05 catastrophic threshold. |
| `EFFICIENCY_STATUS` | **CONDITIONALLY ACCEPTABLE; SHARED-GPU ONLY** | M2 adds10,912parameters. Shared-GPU end-to-end median observations were M0 81.53ms, M2 85.11ms (+4.39%) and M3 83.94ms (+2.96%); these do not certify isolated latency. |
| `NOVELTY_RISK` | **HIGH** | DETR already establishes frozen-detector mask-stage training; SharpContour establishes frozen-base refinement; YOLACT and PatchDCT are close representation/refinement neighbors. |
| `PUBLICATION_STATUS` | **STOP** | The registered equal-budget and stability requirements failed independently of the missing late no-augmentation control. |

## Main quantitative result

All numbers below use final scheduled checkpoints and the fixed full254-image validation evaluator.

| Variant | Mean ΔAP vs M0 / fresh75 | Mean ΔAP75 vs M0 / fresh75 | Mean Δsmall vs M0 / fresh75 | All three paired seeds positive on AP/AP75/small | Registered candidate pass |
|---|---:|---:|---:|---|---|
| B1 | +0.002691 / +0.002055 | −0.000403 / −0.004162 | −0.001930 / +0.003959 | No | No |
| M1 | +0.005253 / +0.004617 | +0.000658 / −0.003101 | +0.002602 / +0.008492 | Yes | No |
| M2 | +0.003038 / +0.002402 | +0.000773 / −0.002986 | −0.000916 / +0.004974 | No | No |
| M3 | +0.005162 / +0.004525 | +0.001797 / −0.001961 | +0.003930 / +0.009819 | No | No |

M3 failed paired all-seed positivity because seed42 small AP changed −0.000773. It also failed the equal-total comparator because mean AP75 remained below fresh75. In seed2024, M3 improved AP/AP75/small by +0.004753/+0.000802/+0.006589 versus M0, but thin recall fell just beyond the registered catastrophic limit.

The bridge diagnostic completed separately. BASE45+15 M2 versus BASE45 changed AP/AP75/small/AP90 by +0.005258/−0.000232/+0.006704/+0.008435. Against fresh BASE60, the changes were +0.007519/+0.001573/+0.014830/+0.007850. This is a positive single-seed bridge observation, not evidence that overrides the independent strong-baseline three-seed failure.

## Twelve required answers

1. **Was the 30-epoch baseline undertrained?** Not established. BASE30 to fresh45 mainly improved small AP, while fresh60 regressed against fresh45. The registered result is `INCONCLUSIVE`, not `UNDERTRAINED`.
2. **What is the final strong-baseline horizon?** 60epochs, retained by the frozen rule. It is a protocol reference, not a claim of proven convergence.
3. **Did specialization exceed equal training budget?** No. Every variant lost mean AP75 to fresh75; none passed all three equal-budget metrics.
4. **Is B4 still stable?** No. The pure residual M2 improved mean AP but had seed-dependent AP75 and small-object regressions.
5. **Does B2 add independent value beyond B1/B4?** Partially. M1 was the only path positive on all primary metrics in all three M0 comparisons, but it failed the fresh75 AP75 comparison and has weak novelty.
6. **Are B2 and B4 genuinely complementary?** No. M3 did not dominate both M1 and M2 across every seed and primary metric.
7. **Is Mega Blueberry stable over three seeds?** The ordinary M1 engineering signal is directionally stable against M0; the registered M2/M3 paper candidates are not qualification-stable.
8. **Was MinneApple replicated?** No. It was intentionally not run because the prerequisite Mega gate failed.
9. **Do shrink/thin effects limit the method?** Yes. All coefficient interventions reduced common-GT predicted area on average; M3 seed2024 exceeded the thin-recall regression limit.
10. **What is the nearest prior art?** DETR for staged frozen detector/mask training; SharpContour and Boundary Patch Refinement for post-hoc/frozen-base spatial refinement; YOLACT for prototype coefficients; PatchDCT for compact-vector refinement.
11. **What is the simplest method now?** As an engineering observation, retraining the existing cv4 head at ratio1 (M1). It needs no new residual module, but it is not a qualified paper mainline.
12. **Is this sufficient for a Q2 engineering paper?** No. The equal-budget AP75 comparison, M2/M3 stability, subgroup gate and external-dataset prerequisite fail.

## Identity and residual interpretation

The residual is not a near-identity numerical correction in magnitude. Across pooled matched instances, M2 median relative residual norms are roughly in the low0.2range; M3 is closer to0.3 and has a heavier tail. Relative residual magnitude generally rises with native mask quality before flattening, so the learned transform cannot be described without qualification as merely repairing poor native masks. The deployed residual remains coefficient-only and exactly10,912parameters, with boxes, scores, classes, prototypes and selected detector candidates fixed.

## Efficiency boundary

The timed path includes the coefficient transformation and official `process_mask` decode; the full-chain measurement additionally includes detector forward and NMS. Each timed sample uses CUDA synchronization after warmup. M2 postprocess-only median overhead was large because the native decode is very short, while the complete chain showed a +4.39% median observation. M3's shared-GPU median happened to be lower than M2 despite more work, demonstrating the noise floor. These measurements support feasibility but not an isolated ≤10% latency claim.

## Protocol limitation

The proposed warm-start, full-network, no-augmentation extra15 control never received a written optimizer/scheduler initialization contract before specialization outcomes were inspected. `SPECIALIZATION_CONTRACT.md` explicitly prohibited choosing that schedule after seeing results. It was therefore not run or relabeled as preregistered evidence. The decisive STOP does not depend on this omission: M2/M3 already fail the mandatory fresh75 comparison and all-seed/subgroup gates. Baseline interruption recovery also restored complete model/EMA/optimizer/scaler/scheduler/RNG state but did not prove bitwise data-loader continuity; this remains disclosed.

## Novelty conclusion

The exact coefficient-only residual was not established in the32-work targeted audit, but absence from the inspected set is not a priority proof. Broad claims about first frozen mask-stage training, first post-training mask refinement, first efficient refinement or first coefficient representation are blocked. Since the exact mechanism does not pass the registered engineering gate, the remaining narrow structural distinction cannot support a main paper claim.

## STOP

**COEFFICIENT-LINE-CLOSED**

Ruled out under this protocol:

- prior gains being sufficient evidence without a strong horizon and equal-budget comparator;
- a stable three-seed pure coefficient-residual advantage;
- reliable B2+B4 package complementarity;
- paper qualification from overall AP while AP75/small/thin behavior remains mixed;
- external replication as a rescue after the primary gate fails.

Reusable assets include checkpoint-specific frozen feature/prototype/TAL caches, official-loss gradient parity checks, NMS source-anchor closure, common-GT boundary/shape/thin analysis, residual-magnitude diagnostics, full-state recovery, and hash-verified run manifests.

The next research line should ask an internal representation question rather than add another coefficient descriptor: whether prototype-basis capacity and assignment/decoder coupling impose the observed shrink/thin ceiling, evaluated end-to-end with a frozen preregistered design. P1D does not execute that P1E work.

## Decision

**STOP**
