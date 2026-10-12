> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# Frozen-prototype diagnostic pilot

Experiment: `EXP-SIS-20260918-P1A`. Read `PROTOCOL.md`, `config.json` and the original `task_prompt.md` before running. No test outcomes are used. No network training or structural interventions are implemented.

The isolated environment inherits the read-only PyTorch 2.1.2/cu121 runtime from `${RUNTIME_ROOT}/.venvs/lednet-p0`. Additional packages live only in this project's `.venv`. Exact versions are saved in `artifacts/pip_freeze.txt`. The clean upstream is cloned into `upstream/` and pinned in `config.json`; imports explicitly resolve there. The legacy source is not imported.

From this directory in PowerShell:

```powershell
& ./.venv/Scripts/python.exe -u prepare.py
& ./.venv/Scripts/python.exe -u run_stage.py extract
# Inspect artifacts/mask_path_closure.json: PASS is mandatory.
& ./.venv/Scripts/python.exe -u run_stage.py refit
& ./.venv/Scripts/python.exe -u run_stage.py audit_precision
# Inspect BOTH oracle_optimization_closure.json and precision_closure.json before interpretation.
& ./.venv/Scripts/python.exe -u run_stage.py analyze
& ./.venv/Scripts/python.exe -u run_stage.py precision_failure_visual
& ./.venv/Scripts/python.exe -u run_stage.py validate_artifacts
& ./.venv/Scripts/python.exe -u package_provenance.py
```

Do not overwrite an archived run. Each supervised stage writes a timestamped `artifacts/runs/<run_id>/` with an exact command, configuration, hashes, git commit/diff, stdout and stderr. Large per-image tensors are in `artifacts/extracted/`; all coefficient solutions and loss curves are in `artifacts/fits/`. The first extracted image additionally saves native and manually reconstructed continuous logits. All images save P, anchor coefficients, original post-NMS coefficients, GT masks, boxes, native binary masks and the model-input RGB image.

`per_instance_results.csv` has one row for every selected legal GT. `matched_prediction=false` means no unused predicted bbox passed the fixed matching gate. Its original-coefficient and predicted-support fields are empty (not zero), because those quantities do not exist. NN fields are empty for a singleton image; local neighbor count remains zero. No unmatched row is discarded from SET-A. SET-B uses matched rows only. Classification agreement is tracked separately from class-agnostic localization matching.

Primary IoUs use identical GT support for both original and refitted coefficients. `_native` uses identical predicted support for both. Neither may be substituted for an aggregate combining missed GT and matched predictions. Prototype refit is a privileged per-GT reconstruction and a feasible BCE solution, not a deployable predictor or an exact IoU upper bound.

`IoU_GT_box_only` controls for the benefit of a privileged tight GT box. `native_support_GT_recall_ceiling` is the exact maximum possible IoU for a perfect mask restricted to the predicted crop. Boundary distance is measured between raster contours on the input grid; singleton distance is missing. GT centroid distances and object pixel areas are also retained in original image coordinates.

No dataset caches, model files, source edits or result files are written into `${DATA_WORKSPACE_ROOT}` or the revision project.

Final outcome: **VERDICT E**, because the supplementary native-oracle precision gate remains unclosed. Read `FINAL_REPORT.md`. The final validator intentionally returns nonzero for this scientific-readiness failure while saving artifact-integrity PASS. Do not reinterpret that as missing data or as a model-representation failure.

The canonical oracle revision is v2: float64 prototype interpolation, 1800/3600 iteration budgets, unchanged BCE objective and native float32 reporting. `config_v1.json` and `artifacts/numeric_attempt_v1/` preserve the earlier numerical attempt. `probe_double.py` and `check_separation.py` are engineering probes; neither replaces the primary diagnostic or changes the selected data.
