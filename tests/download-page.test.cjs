"use strict";
// Dependency-free regression test: node --test tests/download-page.test.cjs
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const html = fs.readFileSync(path.join(__dirname, "..", "index.html"), "utf8");
const match = html.match(/<script>\s*([\s\S]*?)<\/script>/);
assert.ok(match, "The inline download UI script exists");
const source = match[1];

class FakeElement {
  constructor(id = "") {
    this.id = id; this.children = []; this.handlers = {}; this.dataset = {};
    this.attributes = {}; this.value = ""; this.checked = false; this.hidden = false;
    this.disabled = false; this.textContent = ""; this.className = "";
    this.classList = {toggle: () => {}};
  }
  append(...items) {
    for (const item of items) {
      if (item && item.isFragment) this.children.push(...item.children);
      else this.children.push(item);
    }
  }
  appendChild(item) { this.append(item); return item; }
  replaceChildren(...items) { this.children = []; this.append(...items); }
  setAttribute(name, value) { this.attributes[name] = value; }
  addEventListener(name, handler) { this.handlers[name] = handler; }
  dispatch(name) { assert.ok(this.handlers[name], this.id + " handles " + name); this.handlers[name](); }
  querySelectorAll(selector) {
    return this.id === "productTiles" && selector === "button[data-product]" ? this.buttons : [];
  }
}

function fixture(count = 30) {
  return Array.from({length: count}, (_, i) => {
    const product = i % 2 ? "Q-Player" : "Q-System";
    return {
      product, platform: "paper", version: "0.1." + i, mc: "1.18.2",
      javaTarget: "17", date: "2026-10-02T10:00:00Z", dev: true,
      filename: product + "_" + i + ".jar",
      href: "https://github.com/retrocraft0-hub/Q-Downloads/releases/download/dev/" + product + "_" + i + ".jar",
      releaseUrl: "https://github.com/retrocraft0-hub/Q-Downloads/releases/tag/dev/example-" + i,
      description: "Fixture " + i
    };
  });
}

async function boot(entries = fixture()) {
  const ids = new Map();
  const el = id => {
    if (!ids.has(id)) ids.set(id, new FakeElement(id));
    return ids.get(id);
  };
  const projects = ["Q-System","Q-Core","Q-Chunky","Q-Entity","Q-Player"];
  el("productTiles").buttons = projects.map(product => {
    const button = new FakeElement(product); button.dataset.product = product; return button;
  });
  el("sort").value = "published-desc";
  const timers = [];
  let intersectionCallback;
  class FakeObserver {
    constructor(callback) {intersectionCallback = callback;}
    observe() {}
  }
  const document = {
    documentElement: {},
    getElementById: el,
    querySelectorAll: () => [],
    createElement: tag => new FakeElement(tag),
    createDocumentFragment: () => Object.assign(new FakeElement(), {isFragment: true}),
    createTextNode: text => text
  };
  const manifest = {
    schema: 1, repo: "retrocraft0-hub/Q-Downloads", count: entries.length,
    pages: [{path: "catalog/part-00000.json", count: entries.length}]
  };
  const fetch = async url => {
    if (url === "catalog/manifest.json") return {ok: true, json: async () => manifest};
    if (url === "catalog/part-00000.json")
      return {ok: true, json: async () => ({schema: 1, entries})};
    throw Error("Unexpected network request " + url);
  };
  const context = {
    document, navigator: {languages: ["de"], language: "de"},
    window: {IntersectionObserver: FakeObserver}, IntersectionObserver: FakeObserver,
    localStorage: {getItem: () => null, setItem: () => {}},
    Option: (label, value) => ({label, value}),
    fetch, console,
    setTimeout: callback => { timers.push(callback); return timers.length; },
    clearTimeout: id => { if (id) timers[id - 1] = null; }
  };
  vm.runInNewContext(source, context, {timeout: 2000});
  // load() has only two Promise-based fake requests.
  await new Promise(resolve => setImmediate(resolve));
  await new Promise(resolve => setImmediate(resolve));
  return {
    el,
    clickProduct: name => el("productTiles").buttons.find(b => b.dataset.product === name).dispatch("click"),
    scroll: () => intersectionCallback([{isIntersecting: true}]),
    flushTimers: () => { for (const callback of timers.splice(0)) if (callback) callback(); }
  };
}

test("no date range, no stray editor text, and inline JS parses", () => {
  assert.doesNotMatch(html, /id="date(?:From|To)"/);
  assert.doesNotMatch(html, /delete all/);
  assert.match(html, /<fieldset id="filterFields"[^>]*disabled/);
  assert.match(html, /id="lockedOverlay"/);
  new vm.Script(source, {filename: "index.html inline script"});
});

test("all real downloads browseable before choosing a Q project, 24 at a time", async () => {
  const ui = await boot();
  assert.equal(ui.el("filterFields").disabled, true);
  assert.equal(ui.el("downloads").hidden, false);
  assert.equal(ui.el("cards").children.length, 24);
  assert.match(ui.el("count").textContent, /^30 /);
  assert.equal(ui.el("moreWrap").hidden, false);
  ui.scroll();
  assert.equal(ui.el("cards").children.length, 30);
  assert.equal(ui.el("moreWrap").hidden, true);
});

test("locked search warns, product unlocks, keyword filters, reset works", async () => {
  const ui = await boot();
  ui.el("lockedOverlay").dispatch("click");
  assert.equal(ui.el("chooseWarning").hidden, false);
  assert.match(ui.el("chooseWarning").textContent, /System.*Core.*Chunky.*Entity.*Player/);
  ui.clickProduct("Q-Player");
  assert.equal(ui.el("filterFields").disabled, false);
  assert.equal(ui.el("lockedOverlay").hidden, true);
  assert.equal(ui.el("cards").children.length, 15);
  ui.el("query").value = "Q-Player_11.jar";
  ui.el("query").dispatch("input");
  ui.flushTimers();
  assert.equal(ui.el("cards").children.length, 1);
  ui.el("latestOnly").checked = true;
  ui.el("latestOnly").dispatch("change");
  assert.equal(ui.el("cards").children.length, 1);
  ui.el("reset").dispatch("click");
  assert.equal(ui.el("cards").children.length, 15);
  ui.clickProduct("Q-Player");
  assert.equal(ui.el("filterFields").disabled, true);
  assert.equal(ui.el("cards").children.length, 24);
});
