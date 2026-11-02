#!/usr/bin/env python3
"""Offline regressions: duplicate JSON object keys must never enter the public catalog."""
import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("q_catalog_duplicate_audit", SOURCE / "tools/check-release-catalog.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class DuplicateKeyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="q-catalog-duplicate-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "catalog").mkdir()
        self.manifest = (SOURCE / "catalog/manifest.json").read_text(encoding="utf8")
        self.shard = (SOURCE / "catalog/part-00000.json").read_text(encoding="utf8")
        self.old_root = validator.ROOT
        validator.ROOT = self.root
        self.addCleanup(setattr, validator, "ROOT", self.old_root)

    def run_catalog(self, manifest=None, shard=None):
        (self.root / "catalog/manifest.json").write_text(
            self.manifest if manifest is None else manifest, encoding="utf8"
        )
        (self.root / "catalog/part-00000.json").write_text(
            self.shard if shard is None else shard, encoding="utf8"
        )
        with contextlib.redirect_stdout(io.StringIO()):
            validator.main()

    def test_original_16_releases_pass(self):
        self.run_catalog()

    def test_duplicate_manifest_schema_rejected(self):
        mutated = self.manifest.replace('"schema":1', '"schema":1,"schema":1', 1)
        self.assertNotEqual(mutated, self.manifest)
        with self.assertRaisesRegex(SystemExit, "duplicate JSON object key: schema"):
            self.run_catalog(manifest=mutated)

    def test_duplicate_shard_schema_rejected(self):
        mutated = self.shard.replace('"schema":1', '"schema":1,"schema":1', 1)
        self.assertNotEqual(mutated, self.shard)
        with self.assertRaisesRegex(SystemExit, "duplicate JSON object key: schema"):
            self.run_catalog(shard=mutated)

    def test_duplicate_release_product_rejected(self):
        data = json.loads(self.shard)
        serialized = json.dumps(data)
        original = '"product": ' + json.dumps(data["entries"][0]["product"])
        mutated = serialized.replace(original, original + ", " + original, 1)
        self.assertNotEqual(mutated, serialized)
        with self.assertRaisesRegex(SystemExit, "duplicate JSON object key: product"):
            self.run_catalog(shard=mutated)

    def test_duplicate_nested_unknown_key_rejected(self):
        data = json.loads(self.shard)
        data["entries"][0]["unused"] = {"x": 1}
        serialized = json.dumps(data)
        mutated = serialized.replace('"unused": {"x": 1}', '"unused": {"x": 1, "x": 2}', 1)
        self.assertNotEqual(mutated, serialized)
        with self.assertRaisesRegex(SystemExit, "duplicate JSON object key: x"):
            self.run_catalog(shard=mutated)

    def test_nonfinite_manifest_extra_rejected(self):
        # Unknown fields must not bypass strict JSON syntax: browsers reject these.
        for constant in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(constant=constant):
                mutated = self.manifest[:-2] + ',"unused":' + constant + '}\\n'
                with self.assertRaisesRegex(SystemExit, "non-standard JSON constant"):
                    self.run_catalog(manifest=mutated)

    def test_nonfinite_nested_release_extra_rejected(self):
        # A syntactically invalid value deep inside a release hides the whole catalog.
        for constant in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(constant=constant):
                mutated = self.shard.replace(
                    '"product":"Q-Player"',
                    '"unused":{"value":' + constant + '},"product":"Q-Player"',
                    1,
                )
                self.assertNotEqual(mutated, self.shard)
                with self.assertRaisesRegex(SystemExit, "non-standard JSON constant"):
                    self.run_catalog(shard=mutated)


if __name__ == "__main__":
    unittest.main(verbosity=2)
