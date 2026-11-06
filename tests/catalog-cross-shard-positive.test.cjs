"use strict";
const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");

// Positive control for the 251-row cross-shard duplicate rejection test.
test("accepts 251 distinct release identities across two catalog shards", async () => {
  const context = vm.createContext({
    window: { Q_I18N: { names: { de: "Deutsch", "en-US": "English" }, texts: {} } },
    navigator: { languages: ["de"], language: "de" },
    localStorage: { getItem: () => null },
    document: { addEventListener: () => {} },
    URL,
  });
  vm.runInContext(fs.readFileSync("site.js", "utf8"), context, { filename: "site.js" });
  const base = "https://github.com/retrocraft0-hub/Q-Downloads/releases/";
  const makeRow = (n) => ({
    product: "Q-System", version: "0." + n, filename: "Q-System-" + n + "-dev.jar",
    platform: "Paper", mc: "1.21.11", javaTarget: 21,
    href: base + "download/Q-System-test-" + n + "/Q-System-" + n + "-dev.jar",
    releaseUrl: base + "tag/Q-System-test-" + n,
  });
  const first = Array.from({ length: 250 }, (_, i) => makeRow(i));
  const second = [makeRow(250)];
  const manifest = {
    schema: 1, repo: "retrocraft0-hub/Q-Downloads", count: 251,
    pages: [
      { path: "catalog/part-00001.json", count: 250 },
      { path: "catalog/part-00002.json", count: 1 },
    ],
  };
  context.fetch = async (path) => ({
    ok: true,
    json: async () => path === "catalog/manifest.json" ? manifest :
      { schema: 1, entries: path.endsWith("00001.json") ? first : second },
  });
  const result = await vm.runInContext("catalog()", context);
  assert.equal(result.length, 251);
  assert.equal(new Set(result.map(row => row.version)).size, 251);
});
