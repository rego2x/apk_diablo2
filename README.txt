灰の街道 — ASHEN ROADS  ステッカー風ビジュアル + モバイル横画面UI版 / Android APK
バージョン: 1.3.0   (保存形式: 1 / ゲーム本体は 1.1.2版 の仕様・数値をそのまま継承)
======================================================================

■ このフォルダの内容
  index.html                       ゲーム本体 (単一HTML・オフライン・PCブラウザでもそのまま遊べる)
  app/, build.gradle, gradlew ...  Android (WebView) アプリのプロジェクト
  .github/workflows/build-apk.yml  GitHub Actions で APK を自動ビルドする定義
  update-version.cjs / version.json / AGENTS.md   バージョン管理
  tools/build_mobile_from_v112.py  1.1.2版 の index.html からモバイルUI版を生成するスクリプト (開発用・工程1)
  tools/build_sticker_from_mobile.py  モバイルUI版にステッカー風ビジュアルを適用する (開発用・工程2)
  tools/gallery_shots.py / perf_check.py  全敵種の表示確認と描画負荷の計測 (開発用)
  tools/test_mobile.py             Playwright による自動操作テスト (開発用)

■ v1.3.0 で刷新した画面 (7インチ級スマホ・横画面を基準に設計)
  左上    地域名・バイオーム/深度/波・祈りの残り時間 (スタート村では「別の地域に旅に出る」)
  右上    名前・Lv・所持金、HPバー、スタミナバー、XPバー、メニュー(装備/地図/帰還/保存)、ミニマップ
  上中央  中ボスのHPバー (出現時のみ)
  左下    バーチャルスティック。〇をスライドした方向へ移動。外周まで倒すとダッシュ(走る)。
          横の「走る」ボタンは押している間ダッシュ、短くタップで走り続けON/OFF。
  右下    行動ボタン。攻撃(大・押し続けで連続攻撃) / 旋風斬 / 突進 / 回復薬。クールダウン表示付き。
          施設・村人・宝箱の近くでは右側に [E] ボタンが出る。
  下中央  自動保存の状態。 右下隅にバージョン。
  ・画面をタップした地点へ歩く (従来の右クリック移動と同じ)。
  ・攻撃の向きは近くの敵を自動で狙う (5単位以内)。敵がいなければ向いている方向。
  ・PC (マウス・キーボード) で開いた場合はスティック/ボタンを隠し、従来の操作 (WASD, Space, Q/R/F/E/I/M/H/Esc) を使う。
  ・ゲーム内容 (敵100種+中ボス12種、7バイオーム、武器8種、盾、スタミナ、複数の旅先、ペット、鍛冶、
    預り所、首飾り、宝箱、死亡処理、保存) は 1.1.2版 と同じ。PC版のセーブJSONもそのまま読み込める。

■ Android 版の動作
  ・横画面固定・全画面・画面スリープなし。通信権限なし (完全オフライン)。
  ・自動保存はアプリ内の localStorage。アンインストールすると消える。
  ・JSONエクスポート: 保存メニューの「エクスポート」→ 端末の Download/AshenRoads/ashen-roads-save.json
  ・JSONインポート: 「インポート」→ ファイル選択画面。PC版からの引き継ぎはこれで行う。
  ・端末の戻るボタン: ゲームへ Esc を送る (メニューを閉じる/保存メニュー)。1.2秒以内に2回で終了確認。
  ・Bluetooth キーボード/マウス接続時は PC 版の操作も使える。

■ GitHub Actions で APK を作る手順
  1) GitHub で新しいリポジトリを作る (例: ashen-roads-apk。Private でも可)
  2) このフォルダ (game_diablo_apk) の中身をリポジトリ直下にアップロードする
       ・Web: 「Add file」→「Upload files」にフォルダ内をドラッグ＆ドロップ
         ※ 隠しフォルダ .github と .gitignore も必ず含める (エクスプローラーで隠しファイル表示)
       ・Git:  git init && git add -A && git commit -m "v1.3.0" && git branch -M main
               git remote add origin https://github.com/<ユーザー名>/ashen-roads-apk.git && git push -u origin main
  3) リポジトリの「Actions」タブ → 初回は「enable」を押す → 「Build Android APK」が自動実行 (3〜6分)
     走らないときは「Run workflow」で手動実行
  4) 完了した実行の「Artifacts」から AshenRoads-debug-apk をダウンロード
     (zip の中に AshenRoads-v1.3.0-debug.apk)
  5) APK をスマホへ送ってタップしインストール (提供元不明アプリの許可が必要)
  ・「v」+番号 (例 v1.3.0) のタグを push すると Releases にも APK が添付される
  ・release APK は署名なし。署名したい場合は Secrets に ASHEN_KEYSTORE_B64 / ASHEN_KEYSTORE_PASSWORD /
    ASHEN_KEY_ALIAS / ASHEN_KEY_PASSWORD を登録する (keytool で作成した keystore を base64 化)

■ ゲームを修正して再ビルドするとき
  1) index.html (リポジトリ直下) を修正する
  2) node update-version.cjs   … 内容が変わっていれば末尾番号を +1 し、
     index.html / app/src/main/assets/index.html / README / version.json を同じ番号に揃える
     (番号を上げないと Android は上書きインストールできない。versionCode = X*10000+Y*100+Z)
  3) GitHub に push → 新しい APK が Artifacts に出る
  ※ ワークフローはリポジトリ直下の index.html を assets にコピーしてからビルドする。

■ Android Studio でビルドする場合
  このフォルダを開いて Build → Build APK(s)。JDK 17 / Android SDK 34 / Gradle 8.9 (自動取得)。

■ 保存について
  ブラウザ/アプリの localStorage 保存と Dropbox のファイル同期は別物です。
  別の端末へ進行を移すには JSON エクスポート/インポートを使ってください。
