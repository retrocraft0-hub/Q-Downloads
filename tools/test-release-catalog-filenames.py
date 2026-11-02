#!/usr/bin/env python3
"""Offline negative tests: public JAR filenames must bind to catalog identity."""
import copy
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "catalog/manifest.json").read_text(encoding="utf-8"))
SHARDS = {
    page["path"]: json.loads((ROOT / page["path"]).read_text(encoding="utf-8"))
    for page in MANIFEST["pages"]
}
TARGET = next(
    (path, index, entry)
    for path, shard in SHARDS.items()
    for index, entry in enumerate(shard["entries"])
    if entry["product"] == "Q-Player"
    and entry["platform"] == "paper"
    and entry["mc"] == "1.18.2"
    and entry["javaTarget"] == "17"
    and entry["dev"] is True
)


SHORT_TARGET = next(
    (path, index, entry)
    for path, shard in SHARDS.items()
    for index, entry in enumerate(shard["entries"])
    if entry["product"] == "Q-Player"
    and entry["platform"] == "fabric"
    and entry["mc"] == "1.21.11"
    and entry["javaTarget"] == "21"
    and "_MC" not in entry["filename"]
)


def audit(replacement=None, short_mutation=None, tag_mutation=None, short_tag_mutation=None):
    with tempfile.TemporaryDirectory(prefix="q-public-catalog-test-") as tmp:
        root = Path(tmp)
        (root / "tools").mkdir()
        (root / "catalog").mkdir()
        shutil.copy2(ROOT / "tools/check-release-catalog.py", root / "tools/check-release-catalog.py")
        (root / "catalog/manifest.json").write_text(json.dumps(MANIFEST), encoding="utf-8")
        for path, original in SHARDS.items():
            shard = copy.deepcopy(original)
            if path == TARGET[0] and replacement is not None:
                item = shard["entries"][TARGET[1]]
                old = item["filename"]
                item["filename"] = replacement
                item["href"] = item["href"][:-len(old)] + replacement
            if short_mutation is not None and path == SHORT_TARGET[0]:
                shard["entries"][SHORT_TARGET[1]].update(short_mutation)
            for target, new_tag in ((TARGET, tag_mutation), (SHORT_TARGET, short_tag_mutation)):
                if new_tag is not None and path == target[0]:
                    item = shard["entries"][target[1]]
                    item["tag"] = new_tag
                    base = "https://github.com/retrocraft0-hub/Q-Downloads/releases/"
                    item["href"] = base + "download/" + new_tag + "/" + item["filename"]
                    item["releaseUrl"] = base + "tag/" + new_tag
            (root / path).write_text(json.dumps(shard), encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(root / "tools/check-release-catalog.py")],
            capture_output=True, text=True, check=False, timeout=10,
        )


assert audit().returncode == 0, "The original 16-entry public catalog must remain valid"
CASES = {
    "wrong product": "Q-System_Paper_V0.1.0_MC1.18.2_Java17-dev.jar",
    "wrong loader": "Q-Player_Fabric_V0.1.0_MC1.18.2_Java17-dev.jar",
    "wrong Q version": "Q-Player_Paper_V9.9.9_MC1.18.2_Java17-dev.jar",
    "wrong Minecraft": "Q-Player_Paper_V0.1.0_MC1.20.1_Java17-dev.jar",
    "wrong Java target": "Q-Player_Paper_V0.1.0_MC1.18.2_Java21-dev.jar",
    "wrong short filename": "Q-Player_Paper_V9.9.9-dev.jar",
}
for name, filename in CASES.items():
    result = audit(filename)
    assert result.returncode != 0 and "filename does not match" in result.stderr, (
        name, result.returncode, result.stdout, result.stderr
    )
    print("PASS rejected:", name)
print("PASS 1 original catalog + 6 negative filename-identity regressions")

# A short historical filename contains no MC/Java axis. It must not be
# relabelled as another MC/Java target while keeping the original binary URL.
for name, mutation in {
    "short name wrong Minecraft metadata": {"mc": "1.20.1"},
    "short name wrong Java metadata": {"javaTarget": "17"},
}.items():
    result = audit(short_mutation=mutation)
    assert result.returncode != 0 and "filename does not match" in result.stderr, (
        name, result.returncode, result.stdout, result.stderr
    )
    print("PASS rejected:", name)
print("PASS 2 short-filename MC/Java metadata drift regressions")

# Even when the href and releaseUrl agree, the release tag must be bound to
# the five-axis catalog identity. The previous checker accepted these attacks.
TAG_CASES = {
    "wrong release product": "dev/q-system/paper/mc1.18.2/java17/v0.1.0-c2a8f48142",
    "wrong release loader": "dev/q-player/fabric/mc1.18.2/java17/v0.1.0-c2a8f48142",
    "wrong release Minecraft": "dev/q-player/paper/mc1.20.1/java17/v0.1.0-c2a8f48142",
    "wrong release Java": "dev/q-player/paper/mc1.18.2/java21/v0.1.0-c2a8f48142",
    "wrong release Q version": "dev/q-player/paper/mc1.18.2/java17/v9.9.9-c2a8f48142",
    "encoded release segment": "dev/q-player/paper/mc1.18.2/java17/v0.1.0-%2e%2e",
}
for name, tag in TAG_CASES.items():
    result = audit(tag_mutation=tag)
    assert result.returncode != 0 and "release tag does not match" in result.stderr, (
        name, result.returncode, result.stdout, result.stderr
    )
    print("PASS rejected:", name)
for name, tag in {
    "wrong historical release product": "dev/q-core/v0.1.0-d5ef99a6c0",
    "wrong historical release Q version": "dev/q-player/v9.9.9-d5ef99a6c0",
}.items():
    result = audit(short_tag_mutation=tag)
    assert result.returncode != 0 and "release tag does not match" in result.stderr, (
        name, result.returncode, result.stdout, result.stderr
    )
    print("PASS rejected:", name)
# A future release may use the explicit full target tag, including on MC 1.21.11.
valid_full = "dev/q-player/fabric/mc1.21.11/java21/v0.1.0-d5ef99a6c0"
result = audit(short_tag_mutation=valid_full)
assert result.returncode == 0, (result.stdout, result.stderr)
print("PASS accepted: synthetic explicit target tag (offline structural test only)")
print("PASS 8 release-tag identity rejections + 1 positive full-target tag")
