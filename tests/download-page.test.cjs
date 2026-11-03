"use strict";
const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");

// Evaluate the real production script without firing DOMContentLoaded or fetching a catalog.
const context = vm.createContext({
  window: { Q_I18N: { names: { de: "Deutsch", "en-US": "English" }, texts: {} } },
  navigator: { languages: ["de"], language: "de" },
  localStorage: { getItem: () => null },
  document: { addEventListener: () => {} },
  URL,
});
vm.runInContext(fs.readFileSync("site.js", "utf8"), context, { filename: "site.js" });
const safeUrl = (url, kind) => vm.runInContext(
  "safeUrl(" + JSON.stringify(url) + "," + JSON.stringify(kind) + ")", context
);

test("accepts only HTTPS GitHub release paths in the exact public repository", () => {
  const base = "https://github.com/retrocraft0-hub/Q-Downloads/releases/";
  const download = base + "download/Q-System-test/Q-System-dev.jar";
  const tag = base + "tag/Q-System-test";
  assert.equal(safeUrl(download, "download"), download);
  assert.equal(safeUrl(tag, "tag"), tag);
  for (const url of [
    "http://github.com/retrocraft0-hub/Q-Downloads/releases/download/tag/a.jar",
    "https://github.com.evil.example/retrocraft0-hub/Q-Downloads/releases/download/tag/a.jar",
    "https://evil.example/retrocraft0-hub/Q-Downloads/releases/download/tag/a.jar",
    "https://github.com/other/Q-Downloads/releases/download/tag/a.jar",
    "https://github.com/retrocraft0-hub/Q-Downloads/issues",
    "https://github.com:444/retrocraft0-hub/Q-Downloads/releases/download/tag/a.jar",
    "https://user:pass@github.com/retrocraft0-hub/Q-Downloads/releases/download/tag/a.jar",
    "https://github.com/retrocraft0-hub/Q-Downloads/releases/download/tag/a.jar?download=1",
    "https://github.com/retrocraft0-hub/Q-Downloads/releases/download/tag/a.jar#fragment",
    "javascript:alert(1)",
    "not a URL",
  ]) assert.equal(safeUrl(url, "download"), "", url);
  assert.equal(safeUrl(tag + "?view=1", "tag"), "");
  assert.equal(safeUrl(tag + "#fragment", "tag"), "");
  assert.equal(safeUrl(tag, "download"), "");
  assert.equal(safeUrl(download, "tag"), "");
});

test("rejects invalid public catalog entries before rendering", () => {
  const base = "https://github.com/retrocraft0-hub/Q-Downloads/releases/";
  const valid = {
    product: "Q-System", version: "0.1", filename: "Q-System-dev.jar",
    platform: "Paper", mc: "1.21.11",
    href: base + "download/Q-System-test/Q-System-dev.jar",
    releaseUrl: base + "tag/Q-System-test",
  };
  const clean = (row) => vm.runInContext("clean(" + JSON.stringify(row) + ")", context);
  assert.equal(clean(valid).platform, "Paper");
  assert.equal(clean({ ...valid, platform: "NotALoader" }), null);
  assert.equal(clean({ ...valid, product: "Q-Unknown" }), null);
  assert.equal(clean({ ...valid, filename: "source.zip" }), null);
  assert.equal(clean({ ...valid, href: "https://evil.example/a.jar" }), null);
  assert.equal(clean({ ...valid, releaseUrl: "https://evil.example/tag" }), null);
  assert.equal(clean({ ...valid, filename: "Different-dev.jar" }), null);
  assert.equal(clean({ ...valid, href: base + "download/Q-System-test/other.jar" }), null);
  assert.equal(clean({ ...valid, releaseUrl: base + "tag/other-tag" }), null);
});
