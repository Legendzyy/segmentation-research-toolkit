> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../../docs/PROVENANCE.md)。

# Four-cell output-KD development readout (2026-09-26)

All D0/M0/C0/Q0 seed42 jobs completed their frozen 60 epochs with PASS receipts.
The independent full254/1803-GT input640 evaluator used each scheduled **last**
checkpoint. `DEVELOPMENT_V2_COMPARISON.json` and
`development_v2_instance_evidence.csv` contain the machine-readable AP,
coverage, common-GT and conditional mask evidence. No test data were read.

| Student | Detector KD | Mask KD | AP | ΔAP vs native A0 (pp) | AP75 | AP90 | Small AP | Same-class box coverage at score≥.25 |
|---|---|---|---:|---:|---:|---:|---:|---:|
| A0 native | — | — | .840904 | — | .887850 | .741207 | .610283 | 1722/1803 |
| K1 feature KD | feature imitation | — | .842336 | +.1433 | .889433 | — | .613395 | 1720/1803 |
| D0 | direct | direct | .842408 | +.1504 | .894527 | .740528 | .611968 | 1729/1803 |
| M0 | direct | selective | .842282 | +.1379 | .887871 | .746360 | .630261 | 1728/1803 |
| C0 | selective | direct | .838899 | −.2005 | .888376 | .745435 | .610730 | 1731/1803 |
| Q0 | selective | selective | .841307 | +.0404 | .889263 | .750389 | .617076 | 1735/1803 |

M0 differs from D0 by **−.0126 pp overall AP**, **+.5832 pp AP90**, and
**+1.8292 pp small AP**. Against K1 it is **−.0054 pp overall AP** and
**+1.6866 pp small AP**. These overall AP gaps are too small for a single
seed superiority claim. M0 may be a useful small-object trade-off, but the
effect requires paired-seed and strong-control checks. C0 is **−.3509 pp AP**
from D0, despite two additional score-.25 same-class GT matches. Q0 partly
recovers C0's AP; the factorial AP interaction is +.2534 pp. These are
arithmetic contrasts of four seed42 jobs, not causal component effects.

The fixed-threshold diagnostic does not explain AP on its own. D0/M0 have
1729/1728 same-class matched GT at score≥.25 and 2051/2028 candidates above
that score, while their complete low-threshold queues contain 7594/7742
detections. On 1708 D0/M0 common GT whose class-aware assignment is also the
recorded class-agnostic mask candidate, M0's mean IoU changes −.000413 and
boundary F +.000187; the 109 small aligned GT change mean IoU −.002991.
Thus the +1.8292 pp small AP signal is **not** established as a uniformly
better mask on common small GT. Ranking, recall outside this conditional
set, or mask threshold effects remain competing explanations. The thin-pixel
metric is a raster skeleton proxy, not a semantic branch measure.

**Development decision:** retain M0 as a provisional *small-object
trade-off* candidate, retain D0 as the simpler direct-output comparator, and
do not advance C0 as a standalone candidate. Q0's AP90/coverage trade-off is
reported, not hidden. The next evidence package should test M0 against a
same-budget strong native or feature-KD comparator across paired seeds, and
include one faithfully adapted nearest mature KD method before a paper
novelty/performance claim. Review P1D M1's stronger recipe and bridge its
budget or use it as a shared training base if claiming improvement over native
training. Freeze each package before running; do not choose a checkpoint or
threshold using these validation results. MinneApple remains development
data and needs its own teacher/baseline/candidate training if used.

Resource accounting: four formal 60-epoch units of 24; D0/Q0/M0/C0 process
times total 51,025.9 s = **14.174 h** of the 96 h cap. Shared GPU wall time
is not isolated compute or deployment latency. E: free was about 23.75 GiB
after both new evaluations; the live reading remains the next launch gate.
