# -*- coding: utf-8 -*-
"""orig.html (v1.1.2) からモバイル横画面UI版 index.html を生成する"""
import re, sys

NEW_VERSION = "1.2.0"
src = open("orig.html", encoding="utf-8").read()
lines = src.split("\n")
assert lines[21].startswith("<script>"), lines[21][:40]
script = "\n".join(lines[21:])

HEAD = r'''<!doctype html>
<html lang="ja">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover"><title>灰の街道 — ASHEN ROADS</title>
<style>
:root{--gold:#d6b579;--ink:#101515;--muted:#99a7a4;--line:#ffffff20;--sat:env(safe-area-inset-top,0px);--sab:env(safe-area-inset-bottom,0px);--sal:env(safe-area-inset-left,0px);--sar:env(safe-area-inset-right,0px)}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{height:100%}
body{margin:0;background:#101515;color:#e9e7dc;font:14px/1.5 'Yu Gothic UI','Meiryo','Noto Sans JP',sans-serif;overflow:hidden;user-select:none;-webkit-user-select:none;touch-action:none;overscroll-behavior:none}
canvas#game{display:block;width:100vw;height:100vh;cursor:crosshair;touch-action:none}
button{font:inherit;color:inherit;border:1px solid #ba9a5860;background:#202b2b;padding:9px 15px;cursor:pointer;border-radius:4px;touch-action:manipulation}
button:hover{border-color:var(--gold);background:#34413d}
button:disabled{opacity:.4;cursor:default}
button:focus-visible{outline:2px solid #ffe2a3;outline-offset:3px}
button.primary{background:#b28b4e;color:#141b1a;font-weight:bold}
.panel{background:linear-gradient(120deg,#111b1bea,#111717eb);border:1px solid var(--line);box-shadow:0 6px 30px #0005}
.hud{position:fixed;z-index:10}
/* ---------- 左上: 地域情報 ---------- */
#top{left:calc(10px + var(--sal));top:calc(8px + var(--sat));pointer-events:none;max-width:min(300px,38vw)}
#top .eyebrow{font-size:9px;letter-spacing:3px;color:var(--gold);margin:0 0 2px 4px}
#location{padding:7px 12px;border-left:2px solid var(--gold)}
#location b{display:block;font-size:15px;line-height:1.3;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#location small{display:block;color:var(--muted);font-size:11px;line-height:1.4}
#regionTravelBtn{pointer-events:auto;margin-top:6px;padding:5px 10px;font-size:12px}
/* ---------- 右上: ゲージ ---------- */
#right{right:calc(10px + var(--sar));top:calc(8px + var(--sat));width:min(250px,32vw);display:flex;flex-direction:column;gap:6px;align-items:stretch}
#vitals{padding:8px 12px}
#playerline{display:flex;justify-content:space-between;font-size:12px;margin-bottom:5px;gap:8px}
#playerline b{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#gold{color:#ffd98a;white-space:nowrap}
.bar{height:8px;background:#060b0b;overflow:hidden;border-radius:2px}
.bar>i{height:100%;display:block;transition:width .15s}
#health{background:linear-gradient(90deg,#8d3037,#e07c6c)}
#staminaFill{background:linear-gradient(90deg,#2d6b5a,#79d7b8)}
#xpbar{height:4px;margin-top:5px}
#xp{background:var(--gold)}
#hptext,#staminaText{font-size:10.5px;color:#bcc6c1;margin-top:3px;line-height:1.3}
#staminaText{color:#aed7c8}
#menu{display:flex;gap:4px}
#menu button{flex:1;padding:5px 2px;font-size:11px;white-space:nowrap}
#miniWrap{padding:4px;align-self:flex-end}
#mini{width:132px;height:96px;display:block}
/* ---------- 上中央: ボス ---------- */
#bossHud{display:none;position:fixed;top:calc(8px + var(--sat));left:50%;transform:translateX(-50%);width:min(320px,34vw);padding:6px 12px;font-size:12px;text-align:center;color:#ead9ad;z-index:9}
#bossHud .bar{margin-top:4px}
/* ---------- 左下: ジョイスティック ---------- */
#joyZone{left:calc(18px + var(--sal));bottom:calc(18px + var(--sab));width:170px;height:170px;touch-action:none;z-index:12}
#joyBase{position:absolute;left:50%;top:50%;width:140px;height:140px;margin:-70px 0 0 -70px;border-radius:50%;border:2px solid #d6b57966;background:radial-gradient(circle,#1a2626cc 0%,#0e1717aa 70%,#0e171744 100%);box-shadow:0 0 0 6px #0b121233,inset 0 0 24px #000a}
#joyBase::after{content:'';position:absolute;inset:38px;border-radius:50%;border:1px dashed #d6b57940}
#joyBase.run{border-color:#79d7b8;box-shadow:0 0 18px #79d7b866,inset 0 0 24px #000a}
#joyKnob{position:absolute;left:50%;top:50%;width:62px;height:62px;margin:-31px 0 0 -31px;border-radius:50%;background:radial-gradient(circle at 40% 35%,#e9d6a8,#b28b4e 60%,#7a5c2f);box-shadow:0 4px 14px #000b;border:2px solid #f3e4bf88;transition:transform .05s}
#joyKnob::before{content:'';position:absolute;inset:14px;border-radius:50%;border:2px solid #0006}
#runBtn{position:absolute;right:-8px;top:-4px;width:52px;height:52px;border-radius:50%;padding:0;font-size:11px;line-height:1.1;background:#15201f;border-color:#79d7b866;color:#aed7c8}
#runBtn.on{background:#2d6b5a;color:#fff;border-color:#79d7b8}
/* ---------- 右下: 行動ボタン ---------- */
#actions{right:calc(14px + var(--sar));bottom:calc(14px + var(--sab));width:230px;height:200px;z-index:12;touch-action:none}
#actions button{position:absolute;border-radius:50%;padding:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0;background:radial-gradient(circle at 40% 30%,#2a3a38,#141f1e 70%);border:2px solid #ba9a5870;box-shadow:0 4px 14px #000a;overflow:hidden;touch-action:none}
#actions button:active,#actions button.held{background:radial-gradient(circle at 40% 30%,#5a4a2a,#2b2316 70%);border-color:var(--gold)}
#actions button .icon{font-size:24px;line-height:1.1;color:var(--gold)}
#actions button small{font-size:10px;display:block;color:#d9d3c2;line-height:1.1}
#actions button kbd{display:none}
#actions button .cd{position:absolute;inset:0;background:#0c1515db;display:none;place-content:center;font-size:20px;color:#ffe2a3;border-radius:50%}
#btnAttack{right:0;bottom:0;width:96px;height:96px}
#btnAttack .icon{font-size:34px}
#btnSpin{right:104px;bottom:8px;width:68px;height:68px}
#btnDash{right:84px;bottom:92px;width:68px;height:68px}
#btnPotion{right:2px;bottom:116px;width:62px;height:62px}
#btnPotion .icon{color:#8fe3b0}
#interact{position:fixed;right:calc(14px + var(--sar));bottom:calc(230px + var(--sab));display:none;border-color:#d6b579;background:#152420ed;z-index:13;padding:9px 14px;font-size:13px;max-width:min(300px,40vw);text-align:left;border-radius:6px}
/* ---------- 通知類 ---------- */
#toast{position:fixed;top:18%;left:50%;transform:translateX(-50%);background:#141f1fe8;border:1px solid #bb9b6160;padding:8px 18px;pointer-events:none;opacity:0;transition:opacity .25s;text-align:center;max-width:60vw;font-size:13px;z-index:20}
#saveStatus{position:fixed;bottom:calc(3px + var(--sab));left:50%;transform:translateX(-50%);font-size:10px;color:#9da99c;z-index:11;pointer-events:none}
.versionMark{position:fixed;right:calc(6px + var(--sar));bottom:calc(2px + var(--sab));z-index:30;background:#111c1ccc;border:1px solid #d6b57944;border-radius:3px;padding:1px 6px;font:10px Georgia,serif;letter-spacing:1px;color:#ead3a2;pointer-events:none}
#lootNotices{position:fixed;left:calc(10px + var(--sal));top:calc(110px + var(--sat));z-index:8;width:min(260px,34vw);pointer-events:none;display:grid;gap:6px}
.loot-card{background:#101d1bf5;border:1px solid currentColor;border-left:5px solid currentColor;padding:6px 10px;box-shadow:0 4px 22px #0009;animation:lootIn .22s ease-out;overflow-wrap:anywhere}
.loot-card b{display:block;font-size:13px}
.loot-card small{color:#e5cf9d;font-size:11px}
.loot-card span{display:block;font-size:11px;color:#d3ddd7}
@keyframes lootIn{from{opacity:0;transform:translateX(-24px)}to{opacity:1;transform:translateX(0)}}
#help{display:none}
#objective{display:none}
/* ---------- ダイアログ ---------- */
dialog{background:#111c1c;color:#eceadf;border:1px solid #806d49;padding:16px 18px 18px;width:min(820px,96vw);max-height:92vh;overflow:auto;box-shadow:0 30px 140px #000;border-radius:6px;font-size:13px}
dialog::backdrop{background:#030909bb}
dialog h2{font:20px 'Yu Mincho',serif;margin:0 0 8px;color:#e1c693}
dialog p{color:#a9b8b1;margin:6px 0}
dialog .close{float:right;padding:6px 14px;position:sticky;top:0;z-index:2}
dialog button{padding:8px 12px;min-height:38px}
#modalContent .row{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:8px 0;border-bottom:1px solid var(--line);flex-wrap:wrap}
.tag{font-size:11px;color:#9daba4}
.rarity0{color:#c3cbc1}.rarity1{color:#70c9a5}.rarity2{color:#7fbcf1}.rarity3{color:#dba5f6}.rarity4{color:#efb767}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.note{padding:10px;border:1px solid var(--line);font-size:12px;color:#aabbaf}
#world{width:100%;height:min(330px,55vh);background:#0b1313;border:1px solid var(--line)}
.storage-list{max-height:48vh;overflow:auto}
.storage-actions{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0}
.codex-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:8px}
.codex-grid .note b{font-size:14px}
dialog input,#intro input{background:#0f1d1b;border:1px solid #9b855660;color:#eee;padding:10px;width:230px;font:inherit;margin:8px 8px 12px 0;font-size:16px}
/* ---------- タイトル ---------- */
#intro{position:fixed;inset:0;background:radial-gradient(ellipse at 65% 40%,#37574a20,#070f0fe8);display:flex;align-items:center;padding:4vw 6vw;z-index:40;overflow:auto}
#intro .inner{max-width:560px}
#intro .eyebrow{font-size:10px;letter-spacing:4px;color:var(--gold)}
#intro h2{font:clamp(34px,8vh,72px) 'Yu Mincho',serif;letter-spacing:8px;line-height:1.3;margin:8px 0}
#intro p{color:#bcc7bf;line-height:1.8;margin:6px 0}
#intro .meta{display:flex;gap:22px;margin:14px 0;color:#b7bea9;font-size:11px}
#intro .meta b{display:block;font:20px Georgia;color:#ddc28d}
#intro button.primary{padding:12px 18px;font-size:15px}
a{color:var(--gold)}
/* ---------- 端末差 ---------- */
@media (hover:hover) and (pointer:fine){#joyZone,#actions{display:none}#interact{right:auto;left:50%;transform:translateX(-50%);bottom:30%}#help{display:block;position:fixed;bottom:8px;left:12px;font-size:11px;color:#a5b4ae;line-height:1.8;z-index:5}}
@media (max-height:420px){#top{max-width:min(240px,34vw)}#location b{font-size:13px}#location small{font-size:10px}#right{width:min(210px,30vw)}#mini{width:110px;height:80px}#joyZone{width:140px;height:140px;bottom:calc(10px + var(--sab))}#joyBase{width:118px;height:118px;margin:-59px 0 0 -59px}#joyKnob{width:54px;height:54px;margin:-27px 0 0 -27px}#actions{width:200px;height:170px;bottom:calc(8px + var(--sab))}#btnAttack{width:84px;height:84px}#btnSpin{right:92px;bottom:4px;width:60px;height:60px}#btnDash{right:74px;bottom:78px;width:60px;height:60px}#btnPotion{right:0;bottom:100px;width:54px;height:54px}#interact{bottom:calc(190px + var(--sab))}#lootNotices{top:calc(96px + var(--sat))}#miniWrap{display:none}}
@media (max-width:700px){#right{width:min(200px,38vw)}#top{max-width:38vw}#miniWrap{display:none}#bossHud{width:30vw}}
</style></head>
<body>
<canvas id="game" aria-label="灰の街道 ゲームフィールド"></canvas>
<div id="top" class="hud"><div class="eyebrow">ASHEN ROADS</div><div id="location" class="panel"><b id="areaName"></b><small id="areaInfo"></small><small id="blessing" style="display:none;color:#e6eab3"></small></div><button id="regionTravelBtn" style="display:none">別の地域に旅に出る</button></div>
<div id="right" class="hud"><div id="vitals" class="panel"><div id="playerline"><b id="playerLabel"></b><span id="gold"></span></div><div class="bar"><i id="health"></i></div><div id="hptext"></div><div class="bar" style="height:5px;margin-top:5px"><i id="staminaFill"></i></div><div id="staminaText"></div><div class="bar" id="xpbar"><i id="xp"></i></div></div><div id="menu"><button id="inventoryBtn">装備</button><button id="mapBtn">地図</button><button id="homeBtn">帰還</button><button id="settingsBtn">保存</button></div><div id="miniWrap" class="panel"><canvas id="mini" width="440" height="320"></canvas></div><div id="objective"><span id="objectiveText"></span></div></div>
<div id="help">WASD / 矢印：移動　Shift＋移動：ダッシュ　左クリック / Space：攻撃<br>Q：旋風斬　R：突進　F：回復薬　E：施設・会話　街道は重なると移動<br>地面を右クリック：移動　I：装備　M：世界地図　H：帰還　Esc：保存</div>
<div id="bossHud" class="panel"><div id="bossName"></div><div class="bar"><i id="bossHealth"></i></div></div>
<div id="joyZone" class="hud"><div id="joyBase"><div id="joyKnob"></div></div><button id="runBtn" type="button">走る</button></div>
<div id="actions" class="hud"><button id="btnAttack" data-act="attack" title="通常攻撃"><kbd>SPACE</kbd><span class="icon">⚔</span><small>攻撃</small></button><button id="btnSpin" data-act="spin" title="旋風斬"><kbd>Q</kbd><span class="icon">◉</span><small>旋風斬</small><span class="cd" id="spinCd"></span></button><button id="btnDash" data-act="dash" title="突進"><kbd>R</kbd><span class="icon">➶</span><small>突進</small><span class="cd" id="dashCd"></span></button><button id="btnPotion" data-act="potion" title="回復薬"><kbd>F</kbd><span class="icon">✚</span><small id="potions"></small><span class="cd" id="potionCd"></span></button></div>
<div id="lootNotices" aria-live="polite"></div><button id="interact"></button><div id="toast"></div><div id="saveStatus"></div><div id="versionBadge" class="versionMark" data-game-version>v__VER__</div>
<dialog id="modal"><button class="close" id="closeModal">閉じる ×</button><div id="modalContent"></div><span id="modalVersion" class="versionMark" data-game-version>v__VER__</span></dialog>
<div id="intro"><div class="inner"><div class="eyebrow">A WORLD WITHOUT AN EDGE</div><h2>灰の街道</h2><p>古い街道を辿り、魔物を斬り、失われた村の灯を見つける。<br>その先の世界は、あなたが足を踏み入れた瞬間に生まれる。</p><div class="meta"><div><b>∞</b>つながり続ける世界</div><div><b>100 + 12</b>魔物と元素の中ボス</div><div><b>01</b>戦士の旅</div></div><div id="newCharacter"><label for="name">戦士の名前</label><br><input id="name" maxlength="16" placeholder="名前を入力（16文字まで）" value=""><button class="primary" id="start">旅をはじめる →</button></div><button class="primary" id="continue" style="display:none">旅をつづける →</button><p style="font-size:11px">インストール不要 / オフライン対応 / 自動保存<br>横画面推奨　左の〇をスライドで移動　右のボタンで攻撃</p></div></div>
<input type="file" id="importFile" accept="application/json,.json" hidden>
'''.replace("__VER__", NEW_VERSION)

def patch(s, old, new, count=1):
    n = s.count(old)
    assert n == count, ("patch target count %d != %d: %s" % (n, count, old[:80]))
    return s.replace(old, new)

# ---- スクリプトのパッチ ----
script = patch(script, "VERSION='1.1.2';", "VERSION='%s';" % NEW_VERSION)
# ジョイスティック状態 (var で巻き上げ)
script = patch(script, "<script>\n'use strict';", "<script>\n'use strict';\nvar joy={x:0,y:0,active:false,run:false,runHold:false};")
# 移動入力: ジョイスティックをキーボードと同じ画面基準ベクトルとして扱う
script = patch(script,
    "let vx=(keys.d||keys.ArrowRight?1:0)-(keys.a||keys.ArrowLeft?1:0),vy=(keys.s||keys.ArrowDown?1:0)-(keys.w||keys.ArrowUp?1:0);if(vx||vy){",
    "let vx=(keys.d||keys.ArrowRight?1:0)-(keys.a||keys.ArrowLeft?1:0),vy=(keys.s||keys.ArrowDown?1:0)-(keys.w||keys.ArrowUp?1:0);if(joy.active&&(joy.x||joy.y)){vx=joy.x;vy=joy.y;}if(vx||vy){")
# ダッシュ (Shift) にジョイスティックの外周/走るボタンを追加
script = patch(script,
    "function sprintMultiplier(){return keys.Shift&&",
    "function sprintMultiplier(){return (keys.Shift||joy.run||joy.runHold)&&")
script = patch(script,
    "updateStamina(dt,movedDistance,sprint>1,wasDashing,!!keys.Shift&&!!(vx||vy));",
    "updateStamina(dt,movedDistance,sprint>1,wasDashing,!!(keys.Shift||joy.run||joy.runHold)&&!!(vx||vy));")
# タッチでの地面タップは「移動」、マウスは従来どおり
script = patch(script,
    "canvas.addEventListener('pointermove',e=>{mouse.x=e.clientX;mouse.y=e.clientY;mouse.aim=true;});",
    "canvas.addEventListener('pointermove',e=>{if(e.pointerType==='touch')return;mouse.x=e.clientX;mouse.y=e.clientY;mouse.aim=true;});")
script = patch(script,
    "canvas.addEventListener('pointerdown',e=>{if(!active||$('modal').open)return;mouse.x=e.clientX;mouse.y=e.clientY;mouse.aim=true;",
    "canvas.addEventListener('pointerdown',e=>{if(!active||$('modal').open)return;if(e.pointerType==='touch'){mouse.aim=false;target=unproject(e.clientX,e.clientY);return;}mouse.x=e.clientX;mouse.y=e.clientY;mouse.aim=true;")
# モーダルを開いたらジョイスティックも解放
script = patch(script,
    "function openModal(html){mouse.held=false;keys={};target=null;",
    "function openModal(html){mouse.held=false;keys={};target=null;joyReset();")
# 旧タッチボタンの処理は不要 (要素が無い) — そのまま残しても害はない

MOBILE_JS = r'''
/* ===================== モバイル操作 (v1.2.0) ===================== */
function joyReset(){joy.x=0;joy.y=0;joy.active=false;joy.run=false;const k=$('joyKnob'),b=$('joyBase');if(k)k.style.transform='';if(b)b.classList.remove('run');}
(function(){
  const zone=$('joyZone'),base=$('joyBase'),knob=$('joyKnob'),runBtn=$('runBtn');
  if(!zone)return;
  let pid=null,cx=0,cy=0,R=50;
  const dead=.14;
  function start(e){
    if(pid!==null||!active||$('modal').open)return;
    if(e.target===runBtn)return;
    pid=e.pointerId;
    const r=base.getBoundingClientRect();cx=r.left+r.width/2;cy=r.top+r.height/2;R=r.width/2-8;
    zone.setPointerCapture(pid);
    joy.active=true;mouse.aim=false;target=null;
    move(e);
  }
  function move(e){
    if(e.pointerId!==pid)return;
    let dx=e.clientX-cx,dy=e.clientY-cy;const len=Math.hypot(dx,dy);
    const m=Math.min(len,R);
    if(len>0){dx=dx/len*m;dy=dy/len*m;}
    knob.style.transform='translate('+dx+'px,'+dy+'px)';
    const mag=m/R;
    if(mag<dead){joy.x=0;joy.y=0;}
    else{const s=(mag-dead)/(1-dead);joy.x=dx/len*s;joy.y=dy/len*s;}
    joy.run=mag>=.97;
    base.classList.toggle('run',joy.run||joy.runHold);
  }
  function end(e){
    if(e.pointerId!==pid)return;
    pid=null;joyReset();base.classList.toggle('run',joy.runHold);
  }
  zone.addEventListener('pointerdown',start);
  zone.addEventListener('pointermove',move);
  zone.addEventListener('pointerup',end);
  zone.addEventListener('pointercancel',end);
  zone.addEventListener('lostpointercapture',end);
  // 走るボタン: 押している間ダッシュ (タップで固定ON/OFF切替)
  let runTapT=0;
  runBtn.addEventListener('pointerdown',e=>{e.stopPropagation();runBtn.setPointerCapture(e.pointerId);joy.runHold=true;runBtn.classList.add('on');base.classList.add('run');runTapT=performance.now();});
  const runUp=e=>{const tap=performance.now()-runTapT<220;joy.runHold=false;if(tap){joy.runLock=!joy.runLock;}joy.runHold=!!joy.runLock;runBtn.classList.toggle('on',joy.runHold);base.classList.toggle('run',joy.runHold);};
  runBtn.addEventListener('pointerup',runUp);runBtn.addEventListener('pointercancel',runUp);
  // 攻撃ボタン: 押し続けで連続攻撃 (mouse.held と同じ経路)
  const atk=$('btnAttack');
  atk.addEventListener('pointerdown',e=>{if(!active||$('modal').open)return;atk.setPointerCapture(e.pointerId);mouse.held=true;mouse.aim=false;atk.classList.add('held');action('attack');});
  const atkUp=()=>{mouse.held=false;atk.classList.remove('held');};
  atk.addEventListener('pointerup',atkUp);atk.addEventListener('pointercancel',atkUp);atk.addEventListener('lostpointercapture',atkUp);
  // 旋風斬・突進・回復: pointerdown で即発動 (click は無効化して二重発動を防ぐ)
  for(const [id,kind] of [['btnSpin','spin'],['btnDash','dash'],['btnPotion','potion']]){
    const b=$(id);b.onclick=null;
    b.addEventListener('pointerdown',e=>{e.preventDefault();if(!active||$('modal').open)return;mouse.aim=false;action(kind);});
  }
  atk.onclick=null;
  // 帰還ボタン
  const hb=$('homeBtn');if(hb)hb.onclick=()=>{if(active&&!$('modal').open)returnHome();};
  // 画面サイズ変更や非表示で入力を解放
  addEventListener('blur',joyReset);document.addEventListener('visibilitychange',()=>{if(document.hidden)joyReset();});
  // 長押しメニュー・ダブルタップ拡大を抑止
  document.addEventListener('contextmenu',e=>{if(e.target.closest('dialog,input'))return;e.preventDefault();});
  let lastTouchEnd=0;document.addEventListener('touchend',e=>{const now=Date.now();if(now-lastTouchEnd<300&&!e.target.closest('dialog,input,button'))e.preventDefault();lastTouchEnd=now;},{passive:false});
})();
'''
script = patch(script, "}load();requestAnimationFrame(frame);", "}load();requestAnimationFrame(frame);\n" + MOBILE_JS)

out = HEAD + script
open("index.html", "w", encoding="utf-8").write(out)
print("ok", len(out), "bytes; version", NEW_VERSION)
