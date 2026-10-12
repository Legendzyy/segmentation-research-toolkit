> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../../docs/PROVENANCE.md)。

# Same-budget seed2024 strong-control readout

2026-09-27, Blueberry development full254/1803 GT, input640. The scheduled
60-epoch **last** checkpoints for native N0, feature-MSE K1, and direct
GT-corresponded output-KD D0 each passed the independent evaluator. K1's
first attempt ended during epoch2 without a completion receipt; its preserved
evidence was not merged with the successful fresh second attempt. The exact
machine-readable AP, score-.25 coverage, and aligned common-GT calculations
are in `STRONG_CONTROL_V1_PAIRED_EVALUATION.json` and
`strong_control_v1_instance_evidence.csv`.

| Endpoint | N0 native | K1 feature KD | D0 direct output KD |
|---|---:|---:|---:|
| Mask AP | .842095 | .842411 | .844379 |
| AP75 | .893193 | .892507 | .895112 |
| AP90 | .743623 | .743782 | .745004 |
| Small AP | .628707 | .596647 | .622610 |
| Score-.25 same-class box coverage | 1717/1803 | 1709/1803 | 1731/1803 |
| Training process time on shared GPU | 7998 s | 7901 s | 13829 s |

D0−N0 is **+.2284 pp** mask AP, +.1919 pp AP75, +.1380 pp AP90,
**−.6098 pp small AP**, and +14 GT at the fixed score-.25 coverage
diagnostic. D0−K1 is +.1968 pp AP, +.2605 pp AP75, +.1222 pp AP90,
+2.5962 pp small AP, and +22 fixed-threshold GT. K1−N0 is only +.0316 pp
AP while small AP falls 3.2060 pp. D0's overall improvement is therefore
not a uniform scale-group improvement, and the seed2024 control alone does
not establish a stable benefit over either strong baseline. Historical
seed42 D0−A0 was +.1504 pp, while D0−K1 was only +.0072 pp under the same
full254 evaluator; those historical training recipes have not been shown to
be fully paired. D0 has three own seeds, but N0/K1 have only this matched
seed2024 run in ENG03.

On the **1695** N0/D0 common same-class GT with the same candidate in the
mask-quality record, D0 changes mean mask IoU +.000674 and boundary F
+.000736. On 104 small aligned GT mean IoU changes −.001053. On the
**1691** K1/D0 aligned common GT, D0 changes mean IoU +.000807 and boundary
F +.000162; on 104 small aligned GT, mean IoU changes +.004734. These
conditional means and score-.25 coverage describe mechanisms but are not a
decomposition or causal explanation of complete AP. The R0 ranked-anchor
revision was negative against D0, and M0's seed42 small-AP signal reversed
in the second seed. There is currently **no demonstrated stable, distinct
instance-coordination mechanism beyond ordinary direct output KD**.

**Development decision:** retain D0 as the simple output-KD comparator,
not as a paper finalist. Do not spend a second K1/N0 seed just to promote
the +.20 pp single-seed difference. One bounded next development test is
justified: combine the already tested direct GT-corresponded output targets
with the exact K1 neck feature-MSE term, with both original coefficients,
same teacher/init/native schedule/last checkpoint and a training-only
adapter. This tests whether representation imitation supplies a missing
signal to complete predictions, rather than tuning either method against
development validation. It is a **simple additive control**, not a novel
mechanism claim; a negative or weak result will lower the value of continuing
this supervision family. Freeze and audit its implementation before the
single seed2024 formal run. A substantive gain is required before another
seed under the user-directed adaptive policy; a third seed requires retained
direction and near-finalist status. Mature-neighbor adaptation and external
MinneApple remain **unperformed** and cannot be claimed. No test access.

The shared-GPU training times above are non-isolated process times, not
latency or controlled cost comparisons. The first failed K1 partial run and
the first failed R0 partial run count toward resources. At this point ten
60-epoch jobs completed, plus those partial attempts; the 24-unit/96-hour
and E: ≥8 GiB limits still govern any next launch.
