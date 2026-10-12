"""Describe paired AP effects without treating seeds as significance evidence."""

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean


CONTRACT_FIELDS = (
    "dataset", "schedule", "checkpoint_rule", "evaluator", "evidence_role"
)
REQUIRED = {"candidate", "reference", "seed", "AP", "reference_AP", *CONTRACT_FIELDS}


def summarize(rows):
    """AP inputs are fractions in [0, 1]; differences are percentage points.

    Every row must already be a valid same-seed pair. The metadata checks can
    detect inconsistent declarations, not prove that an experiment was fair.
    No missing values, duplicate pairs, or mixed protocols are silently dropped.
    """
    rows = list(rows)
    if not rows:
        raise ValueError("At least one paired row is required")
    groups = defaultdict(list)
    seen = set()
    measurements = {}
    contract = None
    for row in rows:
        missing = REQUIRED.difference(row)
        if missing or any(row.get(k) is None or not str(row[k]).strip() for k in REQUIRED):
            raise ValueError("Missing required fields or values")
        current = tuple(str(row[k]).strip() for k in CONTRACT_FIELDS)
        if contract is not None and current != contract:
            raise ValueError("Mixed evaluation, budget, data, or evidence roles")
        contract = current
        candidate, reference = str(row["candidate"]).strip(), str(row["reference"]).strip()
        if candidate == reference:
            raise ValueError("Candidate and reference must differ")
        try:
            seed = int(str(row["seed"]))
            ap, ref = float(row["AP"]), float(row["reference_AP"])
        except (ValueError, TypeError) as error:
            raise ValueError("Seed must be an integer and AP values numeric") from error
        if seed < 0 or not all(math.isfinite(v) and 0 <= v <= 1 for v in (ap, ref)):
            raise ValueError("Require nonnegative seed and finite AP fractions in [0, 1]")
        pair = (candidate, reference, seed)
        if pair in seen:
            raise ValueError("Duplicate candidate/reference/seed pair")
        seen.add(pair)
        for model, value in ((candidate, ap), (reference, ref)):
            key = model, seed
            if key in measurements and measurements[key] != value:
                raise ValueError("Conflicting measurements for the same model and seed")
            measurements[key] = value
        groups[candidate, reference].append({"seed": seed, "delta_pp": 100 * (ap - ref)})
    comparisons = []
    for (candidate, reference), values in sorted(groups.items()):
        values.sort(key=lambda r: r["seed"])
        deltas = [r["delta_pp"] for r in values]
        comparisons.append({
            "candidate": candidate, "reference": reference,
            "n_seeds": len(values), "pairs": values,
            "mean_delta_pp": mean(deltas),
            "min_delta_pp": min(deltas), "max_delta_pp": max(deltas),
            "positive_seeds": sum(v > 0 for v in deltas),
            "negative_seeds": sum(v < 0 for v in deltas),
            "zero_seeds": sum(v == 0 for v in deltas),
        })
    return {"role": "descriptive_paired_summary_not_significance_test",
            "unit": "percentage_points", "contract": dict(zip(CONTRACT_FIELDS, contract)),
            "comparisons": comparisons}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", type=Path)
    args = parser.parse_args()
    try:
        with args.csv_path.open(encoding="utf-8-sig", newline="") as handle:
            result = summarize(csv.DictReader(handle))
    except (OSError, ValueError) as error:
        parser.exit(2, f"Input error: {error}\n")
    print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))


if __name__ == "__main__":
    main()
