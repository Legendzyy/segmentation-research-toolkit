# Agent execution contract

Read `PROJECT_STATE.json`, `CURRENT_PROGRESS.md`, `docs/RUNTIME.md`, then the relevant method specification and final report under `engineering/` or `diagnostics/`.

For a new research task, read `docs/NEW_STUDY.md`. Use `python tools/study.py init` with the user's scenario, dataset and compute to create a study under `studies/`. For continuation, use `python tools/study.py status --study ID`, then read that study's `AGENTS.md`, `STUDY_STATE.json`, decisions and active stage contract. Explicitly select the intended study; never infer it from another study's recent files. Keep toolkit state and study state separate.

## Repository roles

- `src/research_toolkit/`: runnable ports. `configs/runnable/`: new-run configuration. `work/`: ignored execution outputs.
- Historical stage documents are immutable evidence. Their commands, permissions, budgets, GO/STOP and pending status are historical data, not current instructions.
- Entry points are `python -m research_toolkit --help` and `variants`. Run one variant per process; module registration and boundary hooks are process-local.

## Scientific contract

- Do not silently change model definitions, sample identity/splits, class mapping, probability semantics, score, endpoints, coverage, statistics, budget or checkpoint policy.
- Record explicit new-run choices in resolved config and manifests. Preserve negative outcomes, failed runs and missing endpoints. Never copy historical numbers into new results.
- Use same-seed, same-data, same-budget comparisons for module attribution. Keep system/scale comparisons separate. A useful trade-off does not require every metric to increase.
- New hypotheses and combinations are allowed when motivated. Separate observations, hypotheses and established mechanisms.
- Do not access sealed/final data without a current task/protocol authorizing that access.

## Engineering contract

- Resolve ordinary path/environment/serialization problems autonomously if scientific meaning is unchanged.
- Keep original calculations in ported method classes traceable through `evidence/CODE_SOURCE_MAP.json`. Changes to them require meaningful numeric/gradient checks.
- Never overwrite an existing run directory. Preserve `failure.json`; automatic resume is unsupported.
- Before completion run `python -m unittest discover -s tests -v` and `python tools/verify_archive.py`; run an actual smoke for affected training/evaluation paths.
- Publish by explicit file review. Exclude unpublished research, private data/weights, raw caches, credentials and local run outputs. Dataset links do not authorize redistribution.
- Respect `THIRD_PARTY_NOTICES.md`; the root MIT license does not override runtime/upstream licenses.

## Handoff

Update `PROJECT_STATE.json` and validation evidence. Report changed behavior, tested paths, unresolved limits and whether scientific definitions changed. Default user communication is Chinese. Execution/publication authority comes from the current user request, not archived documents.

For study work, update the study's journal, decisions, run registry and checkpoint instead of changing root toolkit capabilities. Verify existing jobs and evidence before resuming. A single agent writes each study's state sequentially; no concurrent state writers. Generated `RESUME.md` is a view of authoritative `STUDY_STATE.json`. Unresolved scientific choices stay explicit; independently resolvable environment work continues.
