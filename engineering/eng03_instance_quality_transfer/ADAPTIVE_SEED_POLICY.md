> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# ENG03 adaptive seed scheduling amendment (2026-09-26)

User-directed resource scheduling change. The scientific problem, D0/M0
recipes, seed42/128 training, checkpoint policy and evaluation definition are
unchanged. The active D0_s2024 job is allowed to finish. M0_s2024 must not
perform GPU work or create a formal training checkpoint until the completed
D0_s128/M0_s128 pair is independently evaluated on the fixed full254 val set.

The paired seed128 evaluation must report overall mask AP, AP75, AP90,
small AP, same-class score-.25 coverage and aligned common-GT shape/boundary
diagnostics alongside seed42. Seed42 was used for development selection and
is not an unseen confirmation seed. AP is primary; fixed-threshold coverage
and conditional common-GT quality are descriptive, not AP decomposition.

Operationalization recorded **before looking at seed128 validation AP**:
M0_s2024 is released only if its seed128 comparison to D0_s128 retains
overall AP within 0.20 percentage points and improves small AP by at least
0.50 percentage points, with valid full254 PASS receipts. These tolerances
make the user's qualitative “near no overall AP loss, clearly positive
small AP” instruction concrete for this scheduling decision; they are not a
claim of statistical equivalence or a publication significance threshold.
If either criterion fails, stop the unstarted M0_s2024 job and prioritize
failure analysis. AP75/AP90, coverage and common-GT shape must still be
reported, including adverse effects, regardless of the release decision.

Future development: new designs normally receive one seed; a substantive
signal permits a second; a third is reserved for a direction retained on
the second seed and approaching paper finalist. Single ablations normally
use one seed. External development begins with one paired seed. Final paper
evidence requirements are unchanged. No test access, historical deletion,
retroactive experiment rewriting or result-driven checkpoint choice.
