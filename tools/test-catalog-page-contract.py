#!/usr/bin/env python3
"""Offline browser/CI pagination-contract regressions; synthetic entries never published."""
import copy
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_MANIFEST = json.loads((ROOT / "catalog/manifest.json").read_text(encoding="utf-8"))
BASE_SHARD = json.loads((ROOT / "catalog/part-00000.json").read_text(encoding="utf-8"))
PATH0 = "catalog/part-00000.json"
PATH1 = "catalog/part-00001.json"
RELEASES = "https://github.com/retrocraft0-hub/Q-Downloads/releases/"


def check(manifest, shards):
    with tempfile.TemporaryDirectory(prefix="q-public-shard-test-") as tmp:
        root = Path(tmp)
        (root / "tools").mkdir()
        (root / "catalog").mkdir()
        shutil.copy2(ROOT / "tools/check-release-catalog.py", root / "tools/check-release-catalog.py")
        (root / "catalog/manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        for path, shard in shards.items():
            (root / path).write_text(json.dumps(shard), encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(root / "tools/check-release-catalog.py")],
            capture_output=True, text=True, timeout=10, check=False,
        )


def expect_rejected(label, manifest, shards, message):
    result = check(manifest, shards)
    assert result.returncode != 0 and message in result.stderr, (
        label, result.returncode, result.stdout, result.stderr
    )
    print("PASS rejected:", label)


assert check(BASE_MANIFEST, {PATH0: BASE_SHARD}).returncode == 0
print("PASS original 16-entry public catalog")

# The old Python checker accepted two 8-entry shards, while the browser
# rejects pages.length != ceil(count / 250), hiding every download.
split = copy.deepcopy(BASE_MANIFEST)
split["pages"] = [{"path": PATH0, "count": 8}, {"path": PATH1, "count": 8}]
expect_rejected(
    "extra shard for 16 entries", split,
    {PATH0: {"schema": 1, "entries": BASE_SHARD["entries"][:8]},
     PATH1: {"schema": 1, "entries": BASE_SHARD["entries"][8:]}},
    "catalog page count",
)

# Python bool compares equal to 1; the browser's Number.isSafeInteger rejects it.
one = {"schema": 1, "entries": BASE_SHARD["entries"][:1]}
bad_count = copy.deepcopy(BASE_MANIFEST)
bad_count["count"] = True
bad_count["pages"] = [{"path": PATH0, "count": 1}]
expect_rejected("boolean manifest count", bad_count, {PATH0: one}, "invalid catalog count")

bad_page = copy.deepcopy(BASE_MANIFEST)
bad_page["count"] = 1
bad_page["pages"] = [{"path": PATH0, "count": True}]
expect_rejected("boolean page count", bad_page, {PATH0: one}, "invalid catalog shard size")

# A 251-entry single shard used to pass Python's unique-identity checks,
# but the browser caps each page at 250. These are TEMPORARY test-only rows.
seed = BASE_SHARD["entries"][0]
synthetic = []
for i in range(251):
    row = copy.deepcopy(seed)
    version = f"0.1.{i}"
    row["version"] = version
    row["filename"] = f"Q-Player_Paper_V{version}_MC1.18.2_Java17-dev.jar"
    row["tag"] = f"dev/q-player/paper/mc1.18.2/java17/v{version}-c2a8f48142"
    row["href"] = RELEASES + "download/" + row["tag"] + "/" + row["filename"]
    row["releaseUrl"] = RELEASES + "tag/" + row["tag"]
    synthetic.append(row)
too_large = copy.deepcopy(BASE_MANIFEST)
too_large["count"] = 251
too_large["pages"] = [{"path": PATH0, "count": 251}]
expect_rejected(
    "oversized 251-entry shard", too_large,
    {PATH0: {"schema": 1, "entries": synthetic}},
    "catalog page count",
)

# The exact 250+1 split is accepted offline, with no release publication.
valid = copy.deepcopy(BASE_MANIFEST)
valid["count"] = 251
valid["pages"] = [{"path": PATH0, "count": 250}, {"path": PATH1, "count": 1}]
result = check(valid, {
    PATH0: {"schema": 1, "entries": synthetic[:250]},
    PATH1: {"schema": 1, "entries": synthetic[250:]},
})
assert result.returncode == 0, (result.stdout, result.stderr)
print("PASS synthetic 250+1 pagination (offline test data only)")
print("PASS browser-compatible catalog pagination regression suite")
