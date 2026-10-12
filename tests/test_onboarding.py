import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.manifest import create, refresh, verify
from tools.new_stage import create_stage
from tools.paired_summary import read_rows


ROOT = Path(__file__).resolve().parents[1]


class OnboardingTests(unittest.TestCase):
    def test_tutorial_command_and_expected_output(self):
        process = subprocess.run([sys.executable, "tools/paired_summary.py",
                                  "examples/synthetic_study/paired_metrics.csv"],
                                 cwd=ROOT, capture_output=True, text=True, check=True)
        result = json.loads(process.stdout)["comparisons"][0]
        self.assertEqual((result["n_seeds"], result["positive_seeds"], result["negative_seeds"]), (3, 2, 1))
        self.assertAlmostEqual(result["mean_delta_pp"], 0.5)
        self.assertEqual([v["seed"] for v in result["pairs"]], [11, 22, 33])

    def test_csv_duplicate_header_and_extra_column(self):
        raw = (ROOT / "examples/synthetic_study/paired_metrics.csv").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "input.csv"
            for text in (raw.replace("reference_AP", "AP", 1), raw.rstrip() + ",unexpected\n"):
                path.write_text(text, encoding="utf-8")
                with self.assertRaises(ValueError):
                    read_rows(path)

    def test_relative_document_links_exist(self):
        paths = [*ROOT.glob("*.md")]
        for folder in ("docs", "templates", "examples", "tools", "diagnostics", "engineering", "src"):
            paths.extend((ROOT / folder).rglob("*.md"))
        for path in paths:
            for dest in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
                if dest.startswith(("https://", "http://", "#")):
                    continue
                resolved = (path.parent / dest.split("#")[0]).resolve()
                self.assertTrue(resolved.is_relative_to(ROOT) and resolved.exists(), f"{path.name}: {dest}")


class StageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        for folder in ("templates", "configs"):
            shutil.copytree(ROOT / folder, self.root / folder)
        for folder in ("diagnostics", "engineering"):
            (self.root / folder).mkdir()

    def tearDown(self):
        self.temp.cleanup()

    def test_new_stage_is_draft_and_does_not_overwrite(self):
        result = create_stage(self.root, "diagnostics", "pilot01")
        stage = self.root / result["stage"]
        config = json.loads((stage / "config.json").read_text(encoding="utf-8"))
        self.assertEqual(config["experiment_id"], "pilot01")
        self.assertEqual(config["status"], "DRAFT")
        self.assertFalse(config["execution_authorized"])
        self.assertFalse(config["data"]["final_content_access_authorized"])
        self.assertTrue((stage / "DECISIONS.md").exists())
        (stage / "README.md").write_text("user changes", encoding="utf-8")
        with self.assertRaises(ValueError):
            create_stage(self.root, "diagnostics", "pilot01")
        self.assertEqual((stage / "README.md").read_text(encoding="utf-8"), "user changes")

    def test_invalid_paths_and_reserved_names(self):
        for name in ("../escape", "absolute/name", "con", "lpt1", "Upper", "a", "x" * 65):
            with self.subTest(name=name), self.assertRaises(ValueError):
                create_stage(self.root, "engineering", name)
        with self.assertRaises(ValueError):
            create_stage(self.root, "../other", "pilot01")
        self.assertEqual(list((self.root / "engineering").iterdir()), [])

    def test_missing_template_leaves_no_partial_stage(self):
        (self.root / "templates/PROTOCOL.md").unlink()
        with self.assertRaises(OSError):
            create_stage(self.root, "diagnostics", "pilot01")
        self.assertFalse((self.root / "diagnostics/pilot01").exists())


class RefreshTests(unittest.TestCase):
    def test_refresh_retains_old_bytes_and_passes_new_inventory(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            source, manifest = root / "README.md", root / "RELEASE_MANIFEST.json"
            source.write_text("before", encoding="utf-8")
            create(root, manifest)
            old = manifest.read_bytes()
            source.write_text("after", encoding="utf-8")
            self.assertEqual(verify(root, manifest)["status"], "FAIL")
            result = refresh(root, manifest)
            self.assertEqual(result["status"], "REFRESHED")
            self.assertEqual((root / result["backup"]).read_bytes(), old)
            self.assertEqual(result["previous_sha256"], hashlib.sha256(old).hexdigest())
            self.assertEqual(verify(root, manifest)["status"], "PASS")
            self.assertEqual(refresh(root, manifest)["status"], "UNCHANGED")

    def test_failed_replace_preserves_current_manifest(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            source, manifest = root / "README.md", root / "RELEASE_MANIFEST.json"
            source.write_text("before", encoding="utf-8")
            create(root, manifest)
            original = manifest.read_bytes()
            source.write_text("after", encoding="utf-8")
            with patch("tools.manifest.os.replace", side_effect=OSError("simulated failure")):
                with self.assertRaises(OSError):
                    refresh(root, manifest)
            self.assertEqual(manifest.read_bytes(), original)
            self.assertEqual(list(root.glob(".manifest-*.tmp")), [])


if __name__ == "__main__":
    unittest.main()
