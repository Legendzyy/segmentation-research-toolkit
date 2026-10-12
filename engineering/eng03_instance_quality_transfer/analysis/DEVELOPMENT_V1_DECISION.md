> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../../docs/PROVENANCE.md)。

# D0/Q0 seed42 development readout (2026-09-25)

Both frozen 60-epoch jobs completed normally. The independent full254/1803-GT
input640 evaluator used the scheduled last checkpoint for each. The comparison
table is `DEVELOPMENT_V1_COMPARISON.json`; instance identities and candidate
alignment are in `development_v1_instance_evidence.csv`. No test data were read.

| Variant | AP | ΔAP vs A0 (pp) | AP75 | AP90 | small AP | same-class box coverage, score≥.25 |
|---|---:|---:|---:|---:|---:|---:|
| A0 historical native n | .840904 | — | .887850 | .741207 | .610283 | 1722/1803 |
| K1 historical feature KD | .842336 | +.1433 | .889433 | see ENG02 | .613395 | 1720/1803 |
| D0 direct GT-corresponded output KD | .842408 | +.1504 | .894527 | .740528 | .611968 | 1729/1803 |
| Q0 selective class/box/mask KD | .841307 | +.0404 | .889263 | .750389 | .617076 | 1735/1803 |

D0 exceeds K1 by only **.0072 pp**, not evidence that output correspondence
beats mature feature imitation. Q0 loses **.1101 pp** AP to D0 while gaining
**.9860 pp** AP90, **.5108 pp** small AP and six fixed-operating-point GT.
This is a mixed development result, not a confirmed improvement or proof of
complementary components. Both variants recover 11 of the 21 teacher-only
GT from the historical A0/A2 fixed-operating-point comparison. D0/Q0 produce
more full-queue detections than A0 (7594/7373 versus 6401); this deserves a
ranking and false-positive audit before a claim about complete predictions.

On the *same* 1708 A0/D0 GT whose score-.25 same-class assignment coincides
with the class-agnostic mask-metric candidate, D0 changes mean mask IoU by
only +.000285 and boundary F by +.000113; small-GT IoU changes +.007568
among 110. Q0's corresponding 1705-GT mean IoU change is −.000023, with
small-GT +.006122 among 109. Thin-pixel recall is a 640-grid skeleton proxy,
not a semantic thin-structure result. Candidate and subgroup selection make
these **descriptive conditional differences**, never an AP decomposition.

The contrast cannot identify which gate causes the Q0 trade-off: Q0 gates
class, box and mask together. Next bounded development package freezes a
two-factor completion: `M0` keeps direct class/box KD and selects mask KD;
`C0` selects class/box KD and keeps direct mask KD. D0 and Q0 are the other
two cells. Both new jobs retain the D0/Q0 teacher, student initialization,
native loss, three KD weights, data, seed42, 60-epoch schedule, batch8,
last-epoch selection and evaluator. They test whether selective mask targets
can preserve Q0's high-IoU/small trade-off without losing D0's overall AP,
or whether detector gating causes the drop. No weight, threshold or checkpoint
rule is chosen from the validation results. This is mechanism diagnosis, not
confirmation; a promising cell must still face strong budget-matched baselines,
nearest mature KD, paired seeds and external development data.

Resource accounting: D0/Q0 consume 2/24 60-epoch-equivalent formal units and
24713.8 s = 6.865 h of the 96 h training-process cap, plus the documented
non-scientific smokes. GPU was shared; evaluation wall times 189/161 s are
**non-isolated**, not deployment latency. E: free was 24.164 GiB after the
pair; retain the 8 GiB floor and recheck before each new job.
