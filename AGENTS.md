# AGENTS.md — 灰の街道 モバイルUI版 / Android APK : 必須更新手順

## 構成
- `index.html` … ゲーム本体 (単一HTML)。**このファイルが正**。
- `app/src/main/assets/index.html` … APK に同梱されるコピー。手で編集しない (update-version.cjs / ワークフローが同期)。
- `app/`, `build.gradle`, `settings.gradle`, `gradlew*`, `gradle/` … Android WebView アプリ (Java)。
- `.github/workflows/build-apk.yml` … GitHub Actions。push で APK を作り Artifacts へ。
- `version.json` … 表示バージョン `version`、保存形式 `save_format`、納品内容の `content_hash`。
- `update-version.cjs` … バージョン更新スクリプト。
- `tools/` … 再生成パイプラインと Playwright テスト (納品物ではない開発用)。
  `build_mobile_from_v112.py` (1.1.2版 → モバイルUI) → `build_sticker_from_mobile.py` (→ ステッカー風ビジュアル) の順で index.html を生成。
  `gallery_shots.py` で全敵種・ボスの見た目確認、`perf_check.py` で描画時間を計測。

## バージョン規則
1. `index.html`、`README.txt`、`app/` 以下、ワークフローのどれかを修正して納品するときは必ず番号を上げる。
2. 通常は `node update-version.cjs` で末尾 (patch) を +1。UI 刷新など大きな変更は `node update-version.cjs --release X.Y.0`。
3. 番号は戻さない。`version.json` を手で編集・削除しない。
4. 次の5か所が常に同じ番号: `index.html` の `VERSION='x.y.z'`、同ファイル内 `data-game-version` の表示2か所、`app/src/main/assets/index.html`(コピー)、`README.txt` の「バージョン:」、`version.json`。
   APK の versionName/versionCode は index.html の VERSION から自動算出 (X*10000+Y*100+Z)。
5. 保存形式番号 (`save_format`, ゲーム内 localStorage キー `ashen-roads-v1`) は別管理。互換が壊れる変更のときだけ上げ、移行処理を書く。バージョン更新だけでセーブを消さない。

## 納品手順
```
# 1. index.html / README.txt / app を修正
# 2. 検証
python tools/test_mobile.py index.html      # Playwright (chromium) が必要。横画面タッチ操作の自動テスト
# 3. 番号更新と assets 同期
node update-version.cjs                     # 変更があれば +1。同じ内容では増えない
node update-version.cjs --check             # 判定のみ
# 4. GitHub に push → Actions の Artifacts から APK を取得
```

## ステッカー描画の実装メモ
- `sprite(key,w,h,fn)` が種類×位相(6コマ)ごとにビットマップを生成しキャッシュ (上限96枚、LRU)。白縁は白シルエットを12方向に、黒縁を8方向にずらして重ね描き。
- 敵は `drawMonster` (通常9形状) / `drawBossSticker` (12ボス) を `sprite` 経由で描く。色は `vivid()` で高彩度化し `t.color`/`t.accent` に格納。
- プレイヤー・ペットは毎フレーム `sticker()` で直接描画 (武器・向きが連続的に変わるため)。
- 新しい敵形状を足すときは `drawMonster` に分岐を追加し、位相 `a` だけでアニメーションさせる (time を直接使うとキャッシュで止まる)。

## モバイルUI の実装メモ
- 入力は `joy` (画面基準の移動ベクトル, run フラグ) をキーボードと同じ経路 (`tick` 内の vx/vy, `sprintMultiplier`) に合流させている。
- タッチの地面タップは `target` (移動先) を設定し、マウスは従来どおり照準+攻撃。
- 攻撃ボタン長押しは `mouse.held` を使い、照準は `aim()` の近敵自動選択に任せる。
- モーダルを開くと `joyReset()` で入力を解放する。
- PC (hover:hover and pointer:fine) ではスティック/ボタンを CSS で非表示。
