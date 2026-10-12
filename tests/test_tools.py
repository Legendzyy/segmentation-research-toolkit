import csv
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from tools.manifest import create, verify
from tools.paired_summary import summarize


def row(seed=1, ap=0.6, ref=0.5, **changes):
    result = dict(candidate="A", reference="B", seed=str(seed), AP=str(ap), reference_AP=str(ref),
                  dataset="synthetic", schedule="fixed", checkpoint_rule="last",
                  evaluator="test_only", evidence_role="synthetic_fixture")
    result.update(changes)
    return result


class PairedSummaryTests(unittest.TestCase):
    def test_percentage_points_and_all_signs(self):
        result = summarize([row(), row(2, 0.4), row(3, 0.5)])["comparisons"][0]
        self.assertAlmostEqual(result["mean_delta_pp"], 0)
        self.assertAlmostEqual(result["max_delta_pp"], 10)
        self.assertEqual((result["positive_seeds"], result["negative_seeds"], result["zero_seeds"]), (1, 1, 1))

    def test_references_are_not_pooled(self):
        self.assertEqual(len(summarize([row(), row(reference="C", reference_AP="0.4")])["comparisons"]), 2)

    def test_duplicate_and_conflicting_values(self):
        for rows in ([row(), row()], [row(), row(reference="C", AP="0.7")]):
            with self.assertRaises(ValueError):
                summarize(rows)

    def test_missing_and_invalid_values(self):
        for value in ("", "nan", "inf", "-0.1", "60"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                summarize([row(AP=value)])
        with self.assertRaises(ValueError):
            summarize([])

    def test_mixed_roles_and_budgets_rejected(self):
        for field in ("dataset", "schedule", "checkpoint_rule", "evaluator", "evidence_role"):
            with self.subTest(field=field), self.assertRaises(ValueError):
                summarize([row(), row(2, **{field: "different"})])

    def test_published_aggregate_arithmetic(self):
        source = Path(__file__).resolve().parents[1] / "evidence/paired_confirmation.csv"
        with source.open(encoding="utf-8", newline="") as handle:
            results = summarize(csv.DictReader(handle))["comparisons"]
        by_ref = {r["reference"]: r for r in results}
        self.assertAlmostEqual(by_ref["D0"]["mean_delta_pp"], -0.067324732026619, places=10)
        self.assertAlmostEqual(by_ref["N0"]["mean_delta_pp"], -0.047377339979354, places=10)
        for result in results:
            self.assertEqual((result["positive_seeds"], result["negative_seeds"]), (1, 1))

    def test_published_table_matches_provenance(self):
        root = Path(__file__).resolve().parents[1]
        receipt = json.loads((root / "evidence/paired_confirmation.provenance.json").read_text(encoding="utf-8"))
        raw = (root / "evidence/paired_confirmation.csv").read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), receipt["published_sha256"])
        self.assertEqual(len(list(csv.DictReader(raw.decode("utf-8").splitlines()))), receipt["rows"])
        sources = json.loads((root / "evidence/source_index.json").read_text(encoding="utf-8"))["sources"]
        source = next(r for r in sources if r["source_relative_path"] == receipt["source_relative_path"])
        self.assertEqual(source["sha256"], receipt["source_sha256"])


class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "README.md").write_text("fixture\n", encoding="utf-8")
        self.manifest = self.root / "work/index.json"

    def tearDown(self):
        self.temp.cleanup()

    def test_roundtrip_and_no_overwrite(self):
        create(self.root, self.manifest)
        self.assertEqual(verify(self.root, self.manifest)["status"], "PASS")
        with self.assertRaises(ValueError):
            create(self.root, self.manifest)

    def test_added_changed_missing_are_distinguished(self):
        (self.root / "removed.md").write_text("remove", encoding="utf-8")
        create(self.root, self.manifest)
        (self.root / "README.md").write_text("changed", encoding="utf-8")
        (self.root / "removed.md").unlink()
        (self.root / "added.py").write_text("pass\n", encoding="utf-8")
        result = verify(self.root, self.manifest)
        self.assertEqual(result["changed"], ["README.md"])
        self.assertEqual(result["missing"], ["removed.md"])
        self.assertEqual(result["added"], ["added.py"])

    def test_excluded_assets_are_out_of_scope(self):
        (self.root / "data").mkdir()
        (self.root / "data/private.json").write_text("{}", encoding="utf-8")
        (self.root / ".env.json").write_text("{}", encoding="utf-8")
        (self.root / "model.pt").write_bytes(b"binary")
        self.assertEqual(list(create(self.root, self.manifest)["files"]), ["README.md"])

    def test_traversal_manifest_is_rejected(self):
        result = create(self.root, self.manifest)
        result["files"]["../outside.md"] = result["files"].pop("README.md")
        self.manifest.write_text(json.dumps(result), encoding="utf-8")
        with self.assertRaises(ValueError):
            verify(self.root, self.manifest)

    def test_invalid_utf8_rejected(self):
        (self.root / "bad.txt").write_bytes(b"\xff")
        with self.assertRaises(UnicodeError):
            create(self.root, self.manifest)


if __name__ == "__main__":
    unittest.main()
