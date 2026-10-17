#!/usr/bin/env node
/*
  update-version.cjs — 灰の街道 (Android/モバイルUI版) バージョン更新スクリプト

  使い方:
    node update-version.cjs                 内容が変わっていれば末尾 (patch) を +1
    node update-version.cjs --check         書き換えずに判定だけ表示
    node update-version.cjs --release 1.3.0 明示した版へ更新 (現在より大きい番号のみ)

  動作:
   1. 納品対象 (index.html, README.txt, app/ 以下のソース, ワークフロー) の内容ハッシュを
      バージョン文字列を除いて計算し、version.json の content_hash と比較する
   2. 変化があれば番号を更新し、次の4か所を同じ番号に揃える
        index.html の VERSION='x.y.z' と <... data-game-version>vX.Y.Z</...> (2か所)
        README.txt の「バージョン: x.y.z」
        version.json の version
        app/src/main/assets/index.html (index.html のコピー) ← APK の versionName/versionCode になる
   3. 同じ内容で再実行しても番号は増えない。番号は決して戻さない。
*/
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const DIR = __dirname;
const VERSION_JSON = path.join(DIR, "version.json");
const INDEX = path.join(DIR, "index.html");
const ASSET = path.join(DIR, "app", "src", "main", "assets", "index.html");
const README = path.join(DIR, "README.txt");

function walk(dir, out) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (["build", ".gradle", "node_modules", ".git"].includes(e.name)) continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, out);
    else out.push(p);
  }
  return out;
}

function targets() {
  const list = [INDEX, README, path.join(DIR, "build.gradle"), path.join(DIR, "settings.gradle"), path.join(DIR, "gradle.properties")];
  for (const d of ["app/src", "app/build.gradle", ".github"]) {
    const p = path.join(DIR, d);
    if (!fs.existsSync(p)) continue;
    if (fs.statSync(p).isDirectory()) walk(p, list); else list.push(p);
  }
  return list.filter(p => fs.existsSync(p) && p !== ASSET).sort();
}

function stripVersion(text) {
  return text
    .replace(/VERSION\s*=\s*['"]\d+\.\d+\.\d+['"]/g, "VERSION='<ver>'")
    .replace(/v\d+\.\d+\.\d+/g, "v<ver>")
    .replace(/バージョン[:：]\s*\d+\.\d+\.\d+/g, "バージョン: <ver>");
}

function hashAll() {
  const h = crypto.createHash("sha256");
  for (const f of targets()) {
    h.update(path.relative(DIR, f) + "\n");
    const buf = fs.readFileSync(f);
    const isText = /\.(html|txt|md|cjs|js|gradle|properties|xml|java|yml|yaml|json|pro)$/i.test(f);
    h.update(isText ? stripVersion(buf.toString("utf8")) : buf);
    h.update("\n");
  }
  return h.digest("hex");
}

function cmp(a, b) {
  const pa = a.split(".").map(Number), pb = b.split(".").map(Number);
  for (let i = 0; i < 3; i++) if (pa[i] !== pb[i]) return pa[i] - pb[i];
  return 0;
}
function bump(v) {
  const m = v.match(/^(\d+)\.(\d+)\.(\d+)$/);
  if (!m) throw new Error("不正なバージョン: " + v);
  return `${m[1]}.${m[2]}.${Number(m[3]) + 1}`;
}

function applyVersion(next) {
  let html = fs.readFileSync(INDEX, "utf8");
  html = html.replace(/VERSION\s*=\s*['"]\d+\.\d+\.\d+['"]/, `VERSION='${next}'`)
             .replace(/(data-game-version[^>]*>)v\d+\.\d+\.\d+/g, `$1v${next}`);
  fs.writeFileSync(INDEX, html, "utf8");
  fs.mkdirSync(path.dirname(ASSET), { recursive: true });
  fs.writeFileSync(ASSET, html, "utf8");
  if (fs.existsSync(README)) {
    let rd = fs.readFileSync(README, "utf8");
    rd = rd.replace(/バージョン[:：]\s*\d+\.\d+\.\d+/, `バージョン: ${next}`).replace(/v\d+\.\d+\.\d+/g, `v${next}`);
    fs.writeFileSync(README, rd, "utf8");
  }
}

function main() {
  const args = process.argv.slice(2);
  const check = args.includes("--check");
  const relIdx = args.indexOf("--release");
  const release = relIdx >= 0 ? args[relIdx + 1] : null;

  let vj = { version: "1.2.0", save_format: 1, content_hash: "" };
  if (fs.existsSync(VERSION_JSON)) vj = Object.assign(vj, JSON.parse(fs.readFileSync(VERSION_JSON, "utf8")));
  const html = fs.readFileSync(INDEX, "utf8");
  const pm = html.match(/VERSION\s*=\s*['"](\d+\.\d+\.\d+)['"]/);
  let current = vj.version;
  if (pm && cmp(pm[1], current) > 0) current = pm[1];

  const hash = hashAll();
  let next;
  if (release) {
    if (!/^\d+\.\d+\.\d+$/.test(release)) throw new Error("--release は X.Y.Z 形式で指定");
    if (cmp(release, current) <= 0) throw new Error(`--release ${release} は現在の v${current} より大きくなければなりません`);
    next = release;
  } else if (hash === vj.content_hash && pm && pm[1] === current && fs.existsSync(ASSET) &&
             fs.readFileSync(ASSET, "utf8") === html) {
    console.log(`変更なし: v${current} (番号は据え置き)`);
    return;
  } else {
    next = vj.content_hash ? bump(current) : current; // 初回登録は現番号のまま
  }
  if (check) { console.log(`変更あり: v${current} -> v${next} (--check のため書き換えなし)`); return; }
  applyVersion(next);
  const out = { version: next, save_format: vj.save_format, content_hash: hashAll(), updated_at: new Date().toISOString() };
  fs.writeFileSync(VERSION_JSON, JSON.stringify(out, null, 2) + "\n", "utf8");
  console.log(`更新: v${current} -> v${next}  (index.html / assets / README / version.json を同期)`);
}

main();
