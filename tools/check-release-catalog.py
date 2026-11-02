#!/usr/bin/env python3
"""Pure offline Q-Downloads release index consistency audit (no GitHub API, no writes)."""
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = "retrocraft0-hub/Q-Downloads"
RELEASES = "https://github.com/" + REPO + "/releases/"
PRODUCTS = {"Q-System", "Q-Core", "Q-Chunky", "Q-Entity", "Q-Player"}
PLATFORMS = {"paper", "fabric", "neoforge"}

def fail(message):
    raise SystemExit("Q public catalog: " + message)

def reject_duplicate_keys(pairs):
    """Reject ambiguous JSON objects at every depth, including individual releases."""
    result = {}
    for key, value in pairs:
        if key in result:
            fail("duplicate JSON object key: " + key)
        result[key] = value
    return result


def reject_nonstandard_constant(value):
    """Python accepts NaN/Infinity by default; browser JSON.parse rejects them."""
    fail("non-standard JSON constant: " + value)


def read_catalog_json(path):
    return json.loads(
        path.read_text(encoding="utf8"),
        object_pairs_hook=reject_duplicate_keys,
        parse_constant=reject_nonstandard_constant,
    )


def main():
    catalog = read_catalog_json(ROOT / "catalog/manifest.json")
    if catalog.get("schema") != 1 or catalog.get("repo") != REPO or not isinstance(catalog.get("pages"), list):
        fail("bad catalog manifest contract")
    # Match the browser pagination contract: exact 250-entry shards, integer counts.
    count = catalog.get("count")
    if type(count) is not int or count < 0:
        fail("invalid catalog count")
    if len(catalog["pages"]) != (count + 249) // 250:
        fail("catalog page count does not match 250-entry browser pagination")
    entries = []
    paths = set()
    for page in catalog["pages"]:
        if not isinstance(page, dict) or type(page.get("count")) is not int or not 1 <= page["count"] <= 250:
            fail("invalid catalog shard size")
        path = page.get("path")
        if not isinstance(path, str) or not re.fullmatch(r"catalog/part-[0-9]{5}\.json", path):
            fail("invalid catalog shard path")
        if path in paths:
            fail("duplicate catalog shard")
        paths.add(path)
        shard = read_catalog_json(ROOT / path)
        if shard.get("schema") != 1 or not isinstance(shard.get("entries"), list):
            fail("bad catalog shard")
        if len(shard["entries"]) != page.get("count"):
            fail("catalog shard count mismatch")
        entries.extend(shard["entries"])
    if len(entries) != catalog.get("count"):
        fail("catalog entry count mismatch")
    seen_names = set()
    seen_targets = set()
    for item in entries:
        if item.get("product") not in PRODUCTS or item.get("platform") not in PLATFORMS:
            fail("unknown product/loader")
        if not isinstance(item.get("mc"), str) or not re.fullmatch(r"[0-9]+\.[0-9]+(?:\.[0-9]+)?", item["mc"]):
            fail("invalid Minecraft release")
        if not isinstance(item.get("version"), str) or not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?", item["version"]):
            fail("invalid Q version")
        if not isinstance(item.get("javaTarget"), str) or not re.fullmatch(r"[0-9]{1,2}", item["javaTarget"]):
            fail("invalid Java target")
        filename, tag = item.get("filename"), item.get("tag")
        if not isinstance(filename, str) or not re.fullmatch(r"Q-(?:System|Core|Entity|Chunky|Player)_[A-Za-z0-9_.-]+\.jar", filename):
            fail("unexpected original JAR filename")
        if not isinstance(tag, str) or not tag.startswith("dev/") or ".." in tag or "\\" in tag:
            fail("unexpected release tag")
        if item.get("href") != RELEASES + "download/" + tag + "/" + filename or item.get("releaseUrl") != RELEASES + "tag/" + tag:
            fail("wrong release destination: " + filename)
        if type(item.get("dev")) is not bool or type(item.get("approved")) is not bool:
            fail("missing explicit dev/approval flags")
        # Bind original binary filenames to their public catalog identity.
        loader_name = {"paper": "Paper", "fabric": "Fabric", "neoforge": "NeoForge"}[item["platform"]]
        stem = f"{item['product']}_{loader_name}_V{item['version']}"
        suffix = "-dev.jar" if item["dev"] else ".jar"
        allowed_names = {
            stem + suffix,
            stem + f"_MC{item['mc']}_Java{item['javaTarget']}" + suffix,
        }
        if filename not in allowed_names:
            fail("filename does not match product, loader, Q version or MC/Java identity")
        if item["dev"] and not filename.endswith("-dev.jar"):
            fail("dev version has an official filename")
        if item["dev"] and item["approved"]:
            fail("dev version cannot be CurseForge-approved")
        if not item["dev"] and filename.endswith("-dev.jar"):
            fail("official filename is still a dev JAR")
        if not isinstance(item.get("description"), str) or not item["description"].strip():
            fail("empty public release description")
        if item.get("status") not in ("Testversion (-dev)", "Freigegeben"):
            fail("unexpected public status")
        if (item["status"] == "Freigegeben") != item["approved"]:
            fail("approval label mismatch")
        if not isinstance(item.get("date"), str) or not re.fullmatch(r"20[0-9]{2}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z", item["date"]):
            fail("invalid published timestamp")
        try:
            datetime.strptime(item["date"], "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            fail("invalid published calendar timestamp")
        identity = tuple(item.get(k) for k in ("product", "platform", "mc", "javaTarget", "version"))
        if filename in seen_names or identity in seen_targets:
            fail("duplicate binary filename or five-axis published target")
        seen_names.add(filename)
        seen_targets.add(identity)
    print("PASS: " + str(len(entries)) + " unique, structurally valid public release entries (offline check only)")

if __name__ == "__main__":
    main()
