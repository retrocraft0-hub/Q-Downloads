#!/usr/bin/env python3
"""Offline calendar-date regressions for the public binary catalog; no writes to tracked data."""
import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("q_public_catalog_validator", SOURCE / "tools/check-release-catalog.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def accepts(date=None):
    """Run the real validator on a temporary copy of the real catalog."""
    manifest = json.loads((SOURCE / "catalog/manifest.json").read_text(encoding="utf8"))
    with tempfile.TemporaryDirectory(prefix="q-public-dates-") as directory:
        root = Path(directory)
        (root / "catalog").mkdir()
        (root / "catalog/manifest.json").write_text(json.dumps(manifest), encoding="utf8")
        for page in manifest["pages"]:
            path = page["path"]
            shard = json.loads((SOURCE / path).read_text(encoding="utf8"))
            if date is not None:
                shard["entries"][0]["date"] = date
            (root / path).write_text(json.dumps(shard), encoding="utf8")
        original_root = validator.ROOT
        try:
            validator.ROOT = root
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                try:
                    validator.main()
                    return True
                except SystemExit:
                    return False
        finally:
            validator.ROOT = original_root


class CatalogCalendarTests(unittest.TestCase):
    def test_original_16_entries(self):
        self.assertTrue(accepts())

    def test_valid_leap_day(self):
        self.assertTrue(accepts("2024-02-29T23:59:59Z"))

    def test_valid_end_of_year(self):
        self.assertTrue(accepts("2026-12-31T23:59:59Z"))

    def test_february_30_rejected(self):
        self.assertFalse(accepts("2026-02-30T12:00:00Z"))

    def test_non_leap_february_29_rejected(self):
        self.assertFalse(accepts("2026-02-29T12:00:00Z"))

    def test_month_13_rejected(self):
        self.assertFalse(accepts("2026-13-01T12:00:00Z"))

    def test_hour_24_rejected(self):
        self.assertFalse(accepts("2026-11-02T24:00:00Z"))

    def test_minute_60_rejected(self):
        self.assertFalse(accepts("2026-11-02T12:60:00Z"))

    def test_second_60_rejected(self):
        self.assertFalse(accepts("2026-11-02T12:00:60Z"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
