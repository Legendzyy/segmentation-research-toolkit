> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# ENG01 paper/mainline disposition at K2

**Status: no positive paper-mainline blueprint is supported by current evidence.** This file is a bounded closeout record, not authorization to continue experimentation.

The native YOLO11n-seg E0 remains the reference. E4 (native model with a train-only balanced boundary auxiliary) was the seed42 borderline candidate, but its paired three-seed Blueberry AP delta averaged −0.1532 pp (sample SD 0.4978; range −0.7275 to +0.1539), and its modest/precision gates failed. Repeated small-AP deltas were −2.2738 and −2.0124 pp. E1, E2, E3, and E5 do not provide a stronger supported replacement. Therefore no title, abstract claim, or proposed method section should present SPDF, BAPL, or their combination as a validated gain.

If an independent future phase is explicitly authorized, the least-confounded question to reconsider would be whether a train-only boundary auxiliary can improve a clearly specified deployment-relevant boundary metric without small-object AP loss. It would need a newly frozen design, metric, training/evaluation plan, and justification for reopening after the failed replication. This is a research question only; this document does not prescribe a new run or permit access to sealed test data.

Current paper-facing claims supported by ENG01 are limited to: (1) a controlled six-variant engineering comparison was implemented on the pinned native prototype path; (2) full254 paired results and a registered repeat did not validate an AP gain for the candidate; (3) the E4 train-only head can be removed with graph output parity and its deployed static parameter/FLOP count matches E0. These are development findings, not a positive performance claim or evidence of isolated runtime equivalence.

Do not claim statistical significance, external generalization, novelty/priority, CAS Q2, isolated speedup, or test performance. MinneApple was not run. Literature quartiles are unverified. A future manuscript would require a newly authorized phase and stronger positive, repeatable evidence before being framed around this intervention.
