# -*- coding: utf-8 -*-
"""モバイルUI版 index.html に「ステッカー風モンスター」ビジュアルとUIテーマを適用する (v1.3.0)"""
import re, sys

SRC = sys.argv[1] if len(sys.argv) > 1 else "index.html"
DST = sys.argv[2] if len(sys.argv) > 2 else "index_sticker.html"
NEW_VERSION = "1.3.0"
html = open(SRC, encoding="utf-8").read()

def patch(s, old, new, count=1):
    n = s.count(old)
    assert n == count, ("patch target count %d != %d: %s" % (n, count, old[:90]))
    return s.replace(old, new)

html = re.sub(r"VERSION='\d+\.\d+\.\d+'", "VERSION='%s'" % NEW_VERSION, html)
html = re.sub(r"(data-game-version[^>]*>)v\d+\.\d+\.\d+", r"\g<1>v" + NEW_VERSION, html)

# ---- ctx を差し替え可能にする ----
html = patch(html, "canvas=$('game'),ctx=canvas.getContext('2d'),mini=$('mini'),mc=mini.getContext('2d');",
             "canvas=$('game'),ctx0=canvas.getContext('2d'),mini=$('mini'),mc=mini.getContext('2d');let ctx=ctx0;")
# ---- 背景色をステッカー台紙の黒へ ----
html = patch(html, "ctx.fillStyle=area?.type==='village'?'#5c5843':'#0d1717';ctx.fillRect(0,0,screenW,screenH);",
             "ctx.fillStyle=area?.type==='village'?'#3a3328':'#050508';ctx.fillRect(0,0,screenW,screenH);")
html = patch(html, "shade.addColorStop(1,village?'#8c632422':'#020c0bbf');", "shade.addColorStop(1,village?'#2a1a0a55':'#000000cc');")
# ---- 戦利品・弾・ダメージ文字をくっきり ----
html = patch(html, "ctx.font='bold '+(f.text.startsWith('!')?28:20)+'px Georgia';ctx.textAlign='center';ctx.fillStyle=f.color;ctx.fillText(f.text,p.x,p.y-50-(1-f.t/f.max)*30);",
             "ctx.font='900 '+(f.text.startsWith('!')?30:22)+'px sans-serif';ctx.textAlign='center';ctx.lineWidth=5;ctx.strokeStyle='#000';ctx.lineJoin='round';ctx.strokeText(f.text,p.x,p.y-50-(1-f.t/f.max)*30);ctx.fillStyle=f.color;ctx.fillText(f.text,p.x,p.y-50-(1-f.t/f.max)*30);")

# ---- CSS テーマ ----
css_start = html.index("<style>") + len("<style>")
css_end = html.index("</style>")
css = html[css_start:css_end]
rep = [
 (":root{--gold:#d6b579;--ink:#101515;--muted:#99a7a4;--line:#ffffff20;",
  ":root{--gold:#ffd43a;--pink:#ff4fa3;--lime:#9bff3d;--cyan:#45e0ff;--violet:#b36bff;--ink:#07070c;--muted:#b9b4cf;--line:#ffffff;"),
 ("body{margin:0;background:#101515;color:#e9e7dc;font:14px/1.5 'Yu Gothic UI','Meiryo','Noto Sans JP',sans-serif;",
  "body{margin:0;background:#07070c;color:#f4f1ff;font:700 14px/1.5 'Yu Gothic UI','Meiryo','Noto Sans JP',sans-serif;"),
 ("button{font:inherit;color:inherit;border:1px solid #ba9a5860;background:#202b2b;padding:9px 15px;cursor:pointer;border-radius:4px;touch-action:manipulation}",
  "button{font:inherit;font-weight:800;color:#fff;border:2px solid #fff;background:#1c1830;padding:9px 15px;cursor:pointer;border-radius:12px;touch-action:manipulation;box-shadow:0 0 0 2px #000,0 3px 0 2px #000}"),
 ("button:hover{border-color:var(--gold);background:#34413d}", "button:hover{background:var(--pink);color:#140a12}"),
 ("button.primary{background:#b28b4e;color:#141b1a;font-weight:bold}", "button.primary{background:linear-gradient(180deg,#ff7cc0,#ff2e8f);color:#17060f;font-weight:900}"),
 (".panel{background:linear-gradient(120deg,#111b1bea,#111717eb);border:1px solid var(--line);box-shadow:0 6px 30px #0005}",
  ".panel{background:linear-gradient(160deg,#1b1830f0,#0d0b16f2);border:2px solid #fff;border-radius:12px;box-shadow:0 0 0 2px #000,0 6px 22px #000a}"),
 ("#top .eyebrow{font-size:9px;letter-spacing:3px;color:var(--gold);margin:0 0 2px 4px}", "#top .eyebrow{font-size:9px;letter-spacing:3px;color:var(--pink);margin:0 0 2px 6px;font-weight:900}"),
 ("#location{padding:7px 12px;border-left:2px solid var(--gold)}", "#location{padding:7px 12px;border-left:6px solid var(--pink)}"),
 ("#gold{color:#ffd98a;white-space:nowrap}", "#gold{color:var(--gold);white-space:nowrap;text-shadow:1px 1px 0 #000}"),
 (".bar{height:8px;background:#060b0b;overflow:hidden;border-radius:2px}", ".bar{height:10px;background:#120f1c;overflow:hidden;border-radius:6px;border:2px solid #fff;box-shadow:0 0 0 1px #000}"),
 ("#health{background:linear-gradient(90deg,#8d3037,#e07c6c)}", "#health{background:linear-gradient(90deg,#ff2e5f,#ff7cc0)}"),
 ("#staminaFill{background:linear-gradient(90deg,#2d6b5a,#79d7b8)}", "#staminaFill{background:linear-gradient(90deg,#1fb7d8,#7df1ff)}"),
 ("#xpbar{height:4px;margin-top:5px}", "#xpbar{height:7px;margin-top:5px}"),
 ("#staminaText{color:#aed7c8}", "#staminaText{color:#9ff0ff}"),
 ("#joyBase{position:absolute;left:50%;top:50%;width:140px;height:140px;margin:-70px 0 0 -70px;border-radius:50%;border:2px solid #d6b57966;background:radial-gradient(circle,#1a2626cc 0%,#0e1717aa 70%,#0e171744 100%);box-shadow:0 0 0 6px #0b121233,inset 0 0 24px #000a}",
  "#joyBase{position:absolute;left:50%;top:50%;width:140px;height:140px;margin:-70px 0 0 -70px;border-radius:50%;border:3px solid #fff;background:radial-gradient(circle,#1d1a30dd 0%,#0d0b16cc 70%,#0d0b1655 100%);box-shadow:0 0 0 3px #000,inset 0 0 24px #000a}"),
 ("#joyBase::after{content:'';position:absolute;inset:38px;border-radius:50%;border:1px dashed #d6b57940}", "#joyBase::after{content:'';position:absolute;inset:38px;border-radius:50%;border:2px dashed #ffffff33}"),
 ("#joyBase.run{border-color:#79d7b8;box-shadow:0 0 18px #79d7b866,inset 0 0 24px #000a}", "#joyBase.run{border-color:var(--cyan);box-shadow:0 0 0 3px #000,0 0 22px var(--cyan),inset 0 0 24px #000a}"),
 ("#joyKnob{position:absolute;left:50%;top:50%;width:62px;height:62px;margin:-31px 0 0 -31px;border-radius:50%;background:radial-gradient(circle at 40% 35%,#e9d6a8,#b28b4e 60%,#7a5c2f);box-shadow:0 4px 14px #000b;border:2px solid #f3e4bf88;transition:transform .05s}",
  "#joyKnob{position:absolute;left:50%;top:50%;width:62px;height:62px;margin:-31px 0 0 -31px;border-radius:50%;background:radial-gradient(circle at 38% 32%,#ffd1e8,#ff4fa3 55%,#8f1557);box-shadow:0 0 0 2px #000,0 5px 14px #000b;border:3px solid #fff;transition:transform .05s}"),
 ("#joyKnob::before{content:'';position:absolute;inset:14px;border-radius:50%;border:2px solid #0006}", "#joyKnob::before{content:'';position:absolute;left:12px;top:9px;width:16px;height:9px;border-radius:50%;background:#ffffff99}"),
 ("#runBtn{position:absolute;right:-8px;top:-4px;width:52px;height:52px;border-radius:50%;padding:0;font-size:11px;line-height:1.1;background:#15201f;border-color:#79d7b866;color:#aed7c8}",
  "#runBtn{position:absolute;right:-8px;top:-4px;width:52px;height:52px;border-radius:50%;padding:0;font-size:11px;line-height:1.1;background:#15122a;border-color:#fff;color:#9ff0ff}"),
 ("#runBtn.on{background:#2d6b5a;color:#fff;border-color:#79d7b8}", "#runBtn.on{background:var(--cyan);color:#06202a;border-color:#fff}"),
 ("#actions button{position:absolute;border-radius:50%;padding:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0;background:radial-gradient(circle at 40% 30%,#2a3a38,#141f1e 70%);border:2px solid #ba9a5870;box-shadow:0 4px 14px #000a;overflow:hidden;touch-action:none}",
  "#actions button{position:absolute;border-radius:50%;padding:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0;background:radial-gradient(circle at 40% 30%,#3a3560,#17142a 70%);border:3px solid #fff;box-shadow:0 0 0 2px #000,0 5px 0 2px #000;overflow:hidden;touch-action:none;color:#fff}"),
 ("#actions button:active,#actions button.held{background:radial-gradient(circle at 40% 30%,#5a4a2a,#2b2316 70%);border-color:var(--gold)}",
  "#actions button:active,#actions button.held{transform:translateY(3px);box-shadow:0 0 0 2px #000,0 2px 0 2px #000;filter:brightness(1.25)}"),
 ("#actions button .icon{font-size:24px;line-height:1.1;color:var(--gold)}", "#actions button .icon{font-size:24px;line-height:1.1;color:#fff;text-shadow:2px 2px 0 #000}"),
 ("#actions button small{font-size:10px;display:block;color:#d9d3c2;line-height:1.1}", "#actions button small{font-size:10px;display:block;color:#fff;line-height:1.1;font-weight:900;text-shadow:1px 1px 0 #000}"),
 ("#actions button .cd{position:absolute;inset:0;background:#0c1515db;display:none;place-content:center;font-size:20px;color:#ffe2a3;border-radius:50%}",
  "#actions button .cd{position:absolute;inset:0;background:#07070cdd;display:none;place-content:center;font-size:20px;color:#fff;border-radius:50%;font-weight:900}"),
 ("#btnAttack .icon{font-size:34px}", "#btnAttack .icon{font-size:34px}#actions #btnAttack{background:radial-gradient(circle at 40% 30%,#ff8ccb,#ff2e8f 55%,#8f1557)}#actions #btnSpin{background:radial-gradient(circle at 40% 30%,#9df0ff,#1fb7d8 55%,#0d5c70)}#actions #btnDash{background:radial-gradient(circle at 40% 30%,#ffe98a,#ffb81f 55%,#9a5f05)}#actions #btnPotion{background:radial-gradient(circle at 40% 30%,#d1ff9a,#7ee82f 55%,#2e7a0d)}"),
 ("#btnPotion .icon{color:#8fe3b0}", "#btnPotion .icon{color:#fff}"),
 ("#interact{position:fixed;right:calc(14px + var(--sar));bottom:calc(230px + var(--sab));display:none;border-color:#d6b579;background:#152420ed;",
  "#interact{position:fixed;right:calc(14px + var(--sar));bottom:calc(230px + var(--sab));display:none;border-color:#fff;background:var(--lime);color:#0b1a04;"),
 ("#toast{position:fixed;top:18%;left:50%;transform:translateX(-50%);background:#141f1fe8;border:1px solid #bb9b6160;", "#toast{position:fixed;top:18%;left:50%;transform:translateX(-50%);background:#14112aee;border:2px solid #fff;border-radius:12px;box-shadow:0 0 0 2px #000;"),
 (".versionMark{position:fixed;right:calc(6px + var(--sar));bottom:calc(2px + var(--sab));z-index:30;background:#111c1ccc;border:1px solid #d6b57944;border-radius:3px;padding:1px 6px;font:10px Georgia,serif;letter-spacing:1px;color:#ead3a2;pointer-events:none}",
  ".versionMark{position:fixed;right:calc(6px + var(--sar));bottom:calc(2px + var(--sab));z-index:30;background:#14112acc;border:1px solid #fff8;border-radius:6px;padding:1px 6px;font:800 10px sans-serif;letter-spacing:1px;color:#fff;pointer-events:none}"),
 (".loot-card{background:#101d1bf5;border:1px solid currentColor;border-left:5px solid currentColor;", ".loot-card{background:#14112af5;border:2px solid #fff;border-left:8px solid currentColor;border-radius:10px;box-shadow:0 0 0 2px #000;"),
 (".loot-card b{display:block;font-size:13px}", ".loot-card b{display:block;font-size:13px;color:#fff}"),
 ("dialog{background:#111c1c;color:#eceadf;border:1px solid #806d49;", "dialog{background:#14112a;color:#f4f1ff;border:3px solid #fff;box-shadow:0 0 0 4px #000,0 30px 140px #000!important;"),
 ("dialog h2{font:20px 'Yu Mincho',serif;margin:0 0 8px;color:#e1c693}", "dialog h2{font:900 20px sans-serif;margin:0 0 8px;color:var(--gold);text-shadow:2px 2px 0 #000}"),
 ("dialog p{color:#a9b8b1;margin:6px 0}", "dialog p{color:#cfc8e8;margin:6px 0}"),
 ("#modalContent .row{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:8px 0;border-bottom:1px solid var(--line);flex-wrap:wrap}",
  "#modalContent .row{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:8px 0;border-bottom:1px solid #ffffff22;flex-wrap:wrap}"),
 (".tag{font-size:11px;color:#9daba4}", ".tag{font-size:11px;color:#b9b4cf}"),
 (".rarity0{color:#c3cbc1}.rarity1{color:#70c9a5}.rarity2{color:#7fbcf1}.rarity3{color:#dba5f6}.rarity4{color:#efb767}",
  ".rarity0{color:#e2e2ea}.rarity1{color:#9bff3d}.rarity2{color:#45e0ff}.rarity3{color:#d58cff}.rarity4{color:#ffd43a}"),
 (".note{padding:10px;border:1px solid var(--line);font-size:12px;color:#aabbaf}", ".note{padding:10px;border:2px solid #ffffff44;border-radius:10px;font-size:12px;color:#cfc8e8}"),
 ("#world{width:100%;height:min(330px,55vh);background:#0b1313;border:1px solid var(--line)}", "#world{width:100%;height:min(330px,55vh);background:#07070c;border:2px solid #fff;border-radius:10px}"),
 ("dialog input,#intro input{background:#0f1d1b;border:1px solid #9b855660;color:#eee;", "dialog input,#intro input{background:#07070c;border:2px solid #fff;border-radius:10px;color:#fff;"),
 ("#intro{position:fixed;inset:0;background:radial-gradient(ellipse at 65% 40%,#37574a20,#070f0fe8);", "#intro{position:fixed;inset:0;background:radial-gradient(ellipse at 65% 40%,#ff4fa322,#07070cf0 60%);"),
 ("#intro .eyebrow{font-size:10px;letter-spacing:4px;color:var(--gold)}", "#intro .eyebrow{font-size:10px;letter-spacing:4px;color:var(--cyan);font-weight:900}"),
 ("#intro h2{font:clamp(34px,8vh,72px) 'Yu Mincho',serif;letter-spacing:8px;line-height:1.3;margin:8px 0}",
  "#intro h2{font:900 clamp(34px,9vh,76px) sans-serif;letter-spacing:6px;line-height:1.3;margin:8px 0;color:#fff;-webkit-text-stroke:2px #000;paint-order:stroke fill;text-shadow:5px 5px 0 var(--pink),-3px -3px 0 var(--cyan)}"),
 ("#intro p{color:#bcc7bf;line-height:1.8;margin:6px 0}", "#intro p{color:#cfc8e8;line-height:1.8;margin:6px 0}"),
 ("#intro .meta{display:flex;gap:22px;margin:14px 0;color:#b7bea9;font-size:11px}", "#intro .meta{display:flex;gap:22px;margin:14px 0;color:#b9b4cf;font-size:11px}"),
 ("#intro .meta b{display:block;font:20px Georgia;color:#ddc28d}", "#intro .meta b{display:block;font:900 22px sans-serif;color:var(--lime);text-shadow:2px 2px 0 #000}"),
 ("#bossHud{display:none;position:fixed;top:calc(8px + var(--sat));left:50%;transform:translateX(-50%);width:min(320px,34vw);padding:6px 12px;font-size:12px;text-align:center;color:#ead9ad;z-index:9}",
  "#bossHud{display:none;position:fixed;top:calc(8px + var(--sat));left:50%;transform:translateX(-50%);width:min(320px,34vw);padding:6px 12px;font-size:12px;text-align:center;color:#fff;z-index:9;font-weight:900}#bossHealth{background:linear-gradient(90deg,#b36bff,#ff4fa3)}"),
 ("#hptext,#staminaText{font-size:10.5px;color:#bcc6c1;margin-top:3px;line-height:1.3}", "#hptext,#staminaText{font-size:10.5px;color:#e6e1ff;margin-top:3px;line-height:1.3}"),
 ("a{color:var(--gold)}", "a{color:var(--cyan)}"),
]
for old, new in rep:
    assert css.count(old) == 1, ("css target: " + old[:70])
    css = css.replace(old, new)
html = html[:css_start] + css + html[css_end:]

# ---- ステッカー描画 JS (末尾に追加: 同名関数は後勝ちで上書き) ----
JS = r'''
/* ===================== ステッカー風ビジュアル (v1.3.0) ===================== */
const STK={off:document.createElement('canvas'),mask:document.createElement('canvas')};
STK.o=STK.off.getContext('2d');STK.m=STK.mask.getContext('2d');
function hexToHsl(hex){let r=parseInt(hex.slice(1,3),16)/255,g=parseInt(hex.slice(3,5),16)/255,b=parseInt(hex.slice(5,7),16)/255;const mx=Math.max(r,g,b),mn=Math.min(r,g,b);let h=0,s=0,l=(mx+mn)/2;if(mx!==mn){const d=mx-mn;s=l>.5?d/(2-mx-mn):d/(mx+mn);switch(mx){case r:h=(g-b)/d+(g<b?6:0);break;case g:h=(b-r)/d+2;break;default:h=(r-g)/d+4;}h/=6;}return[h*360,s,l];}
function hsl(h,s,l){return 'hsl('+((h%360+360)%360).toFixed(0)+','+(s*100).toFixed(0)+'%,'+(l*100).toFixed(0)+'%)';}
function vivid(hex,dh=0,ds=0,dl=0){if(!/^#[0-9a-f]{6}$/i.test(hex))return hex;const[h,s,l]=hexToHsl(hex);return hsl(h+dh,Math.min(1,Math.max(.72,s*1.5)+ds),Math.min(.72,Math.max(.42,l))+dl);}
// 敵種ごとに鮮やかで個別の色を割り当てる (同バイオーム内で色相をずらす)
(function(){const seen={};enemyTypes.forEach((t,i)=>{t.base=t.color;if(t.ai==='boss'){t.color=vivid(t.base,0,.1,0);t.accent=vivid(t.base,180,0,-.05);return;}const b=(t.biomes||['grass'])[0];seen[b]=(seen[b]||0)+1;const k=seen[b];const dh=i<20?0:k*33+(i%2)*160;t.color=vivid(t.base,dh,.15,(k%3)*.04);t.accent=vivid(t.base,dh+150,.1,0);});})();

/** 図形を白縁+黒縁のステッカーとして描く (キャッシュ無し・プレイヤー等の単体用)。fn は ctx を使って通常どおり描画する */
function sticker(px,py,w,h,fn,opts={}){
  const T=ctx0.getTransform();const dpr=T.a;const W=Math.ceil(w*dpr),H=Math.ceil(h*dpr);
  if(STK.off.width!==W||STK.off.height!==H){STK.off.width=STK.mask.width=W;STK.off.height=STK.mask.height=H;}
  const o=STK.o,m=STK.m;o.setTransform(1,0,0,1,0,0);o.clearRect(0,0,W,H);
  const dx=W/2-(T.a*px+T.c*py+T.e),dy=H*(opts.anchor??.8)-(T.b*px+T.d*py+T.f);
  o.setTransform(T.a,T.b,T.c,T.d,T.e+dx,T.f+dy);
  ctx=o;try{fn();}finally{ctx=ctx0;}
  ctx0.save();ctx0.setTransform(1,0,0,1,0,0);stampOutline(ctx0,STK.off,m,W,H,-dx,-dy,dpr,opts);ctx0.drawImage(STK.off,-dx,-dy);ctx0.restore();
}
function stampOutline(dst,src,m,W,H,x,y,scale,opts){
  m.setTransform(1,0,0,1,0,0);m.clearRect(0,0,W,H);m.globalCompositeOperation='source-over';m.drawImage(src,0,0);m.globalCompositeOperation='source-in';m.fillStyle='#fff';m.fillRect(0,0,W,H);
  const r=(opts.outline??4.5)*scale,n=opts.cached?12:8;for(let i=0;i<n;i++){const a=i/n*Math.PI*2;dst.drawImage(m.canvas,x+Math.cos(a)*r,y+Math.sin(a)*r);}
  m.globalCompositeOperation='source-in';m.fillStyle='#120b16';m.fillRect(0,0,W,H);
  const r2=(opts.edge??1.6)*scale,n2=opts.cached?8:4;for(let i=0;i<n2;i++){const a=i/n2*Math.PI*2+.4;dst.drawImage(m.canvas,x+Math.cos(a)*r2,y+Math.sin(a)*r2);}
}
/** キャッシュ付きステッカー: key ごとに1枚のビットマップを作り、以後は drawImage 1回で描く */
const SPR=new Map(),SPR_MAX=96,SPR_FRAMES=6;
function spriteScale(){return Math.min(devicePixelRatio||1,1.5);}
function sprite(key,w,h,fn,opts={}){
  let c=SPR.get(key);if(c)return c;
  if(SPR.size>=SPR_MAX){SPR.delete(SPR.keys().next().value);}
  const s=spriteScale(),W=Math.ceil(w*s),H=Math.ceil(h*s);
  const off=document.createElement('canvas');off.width=W;off.height=H;const o=off.getContext('2d');
  o.setTransform(s,0,0,s,W/2,H*(opts.anchor??.8));ctx=o;try{fn();}finally{ctx=ctx0;}
  const res=document.createElement('canvas');res.width=W;res.height=H;const rc=res.getContext('2d');
  if(STK.mask.width!==W||STK.mask.height!==H){STK.mask.width=W;STK.mask.height=H;}
  stampOutline(rc,off,STK.m,W,H,0,0,s,{...opts,cached:true});rc.drawImage(off,0,0);
  c={img:res,w,h,anchor:opts.anchor??.8};SPR.set(key,c);return c;
}
function drawSprite(c,px,py,scale=1,bright=false){if(bright)ctx0.filter='brightness(1.9) saturate(.3)';ctx0.drawImage(c.img,px-c.w*scale/2,py-c.h*scale*c.anchor,c.w*scale,c.h*scale);if(bright)ctx0.filter='none';}
function phaseOf(v){return Math.floor(((v%(Math.PI*2))+Math.PI*2)%(Math.PI*2)/(Math.PI*2)*SPR_FRAMES);}
// ---- パーツ ----
function ink(){return '#120b16';}
function gloss(x,y,rx,ry,a=.45){ellipse(x,y,rx,ry,'rgba(255,255,255,'+a+')');}
function eyeBall(x,y,r,iris='#2bd4ff',look=0){ellipse(x,y,r,r,'#fff');ellipse(x+look*r*.25,y,r*.58,r*.58,iris);ellipse(x+look*r*.3,y+r*.05,r*.3,r*.32,ink());ellipse(x-r*.3,y-r*.32,r*.22,r*.18,'#fff');}
function angryEye(x,y,r,side,iris='#ffd43a'){ellipse(x,y,r,r*.8,'#fff');ellipse(x,y+r*.1,r*.45,r*.45,iris);ellipse(x,y+r*.12,r*.2,r*.22,ink());poly([[x-r*1.1,y-r*1.1-(side>0?r*.4:0)],[x+r*1.1,y-r*1.1-(side>0?0:r*.4)],[x+r*1.1,y-r*.5],[x-r*1.1,y-r*.5]],ink());}
function teethRow(x,y,w,n,h,down=true,color='#fff'){const step=w/n;for(let i=0;i<n;i++){const x0=x-w/2+i*step,x1=x0+step;poly([[x0,y],[x1,y],[(x0+x1)/2,y+(down?h:-h)]],color);}}
function grin(x,y,w,h,n=7,open=1){ellipse(x,y,w/2,h/2*open,'#2a0c22');ellipse(x,y+h*.18*open,w*.3,h*.22*open,'#b8265e');teethRow(x,y-h/2*open+1,w*.9,n,h*.42*open,true);teethRow(x,y+h/2*open-1,w*.8,n-1,h*.3*open,false);}
function jaw(x,y,w,h,n=6){/* 下向きに開いた大口 (楕円の下半分) */ctx.save();ctx.beginPath();ctx.ellipse(x,y,w/2,h,0,0,Math.PI);ctx.closePath();ctx.fillStyle='#2a0c22';ctx.fill();ctx.restore();teethRow(x,y+1,w*.9,n,h*.5,true);teethRow(x,y+h-1,w*.7,n-1,h*.35,false);ellipse(x,y+h*.55,w*.22,h*.2,'#c92a63');}
function drips(x,y,w,c,n=4,t=0){for(let i=0;i<n;i++){const dx=x-w/2+w*(i+.5)/n,len=6+((i*7)%9)+Math.sin(t*3+i)*2;ellipse(dx,y+len*.6,4,len*.6,c);}}
function legsStub(x,y,c,spread=12,n=2,anim=0){for(let i=0;i<n;i++){const dx=x-spread+ (2*spread)*(n===1?.5:i/(n-1));ellipse(dx,y-3+Math.sin(anim+i*2)*1.5,7,5,c);}}
function hornPair(x,y,c,size=1,curve=1){for(const s of[-1,1]){poly([[x+s*10*size,y],[x+s*26*size,y-26*size*curve],[x+s*4*size,y-6*size]],c);}}

// ---- 通常敵 ----
function drawMonster(t,e,c,bob,a){
  const shape=t.shape,acc=t.accent||'#ff4fa3',dark=vivid(t.base||t.color,0,0,-.18);
  const walk=Math.sin(a)*3;
  if(shape==='slime'){const sq=1+Math.sin(a)*.06;ellipse(0,-22+bob,30*sq,24/sq,c);drips(0,-6,44,c,5,a);gloss(-12,-36+bob,9,5);grin(2,-14+bob,34,16,7,1);eyeBall(4,-34+bob,9,acc,.3);}
  else if(shape==='beast'){const horn=t.ai==='charger';poly([[-30,-14],[-22,-30],[0,-36],[22,-32],[30,-14],[14,-4],[-14,-4]],c);for(const s of[-1,1]){line(s*16,-12,s*18+(s>0?walk:-walk),2,dark,6);line(s*6,-10,s*8-(s>0?walk:-walk),2,dark,6);}line(-28,-24,-44,-40+Math.sin(a)*4,c,5);ellipse(18,-36,19,16,c);jaw(22,-33,34,16,7);angryEye(12,-46,5,1,acc);angryEye(26,-47,4,-1,acc);if(horn)poly([[24,-50],[42,-74],[32,-46]],'#f6f1d8');gloss(6,-30,8,4,.3);}
  else if(shape==='spider'){for(let i=0;i<4;i++)for(const s of[-1,1]){const y=-22+i*5,k=Math.sin(a+i)*3;line(s*8,y,s*(26+k),y-12,dark,4);line(s*(26+k),y-12,s*(34+k),y+8,dark,3);}ellipse(0,-22,22,17,c);ellipse(-6,-30,7,5,acc);grin(0,-14,30,12,8,1);for(let i=0;i<5;i++){const q=-2.2+i*.55;eyeBall(Math.cos(q)*14,-30+Math.sin(q)*6,i===2?5:3.2,ink(),0);}gloss(-9,-33,6,3);}
  else if(shape==='bat'){const flap=Math.sin(a)*10;for(const s of[-1,1]){poly([[s*8,-36],[s*44,-56-flap],[s*52,-32-flap*.5],[s*34,-30],[s*40,-14],[s*14,-24]],dark);poly([[s*10,-34],[s*42,-54-flap],[s*48,-34-flap*.5],[s*32,-30],[s*36,-16],[s*14,-26]],c);}ellipse(0,-34+bob,18,17,c);jaw(0,-30+bob,30,15,6);eyeBall(0,-44+bob,8,acc,0);for(const s of[-1,1])poly([[s*6,-50+bob],[s*12,-64+bob],[s*14,-48+bob]],c);legsStub(0,0,dark,8);}
  else if(shape==='crystal'){const f=-6+bob;poly([[0,-66+f],[22,-52+f],[26,-20+f],[12,-4],[-12,-4],[-26,-20+f],[-22,-52+f]],c);poly([[0,-66+f],[22,-52+f],[6,-36+f]],vivid(t.base||t.color,0,0,.14));poly([[-22,-52+f],[0,-66+f],[-6,-38+f]],'rgba(255,255,255,.28)');poly([[12,-4],[26,-20+f],[16,-24+f]],dark);grin(0,-22+f,30,13,6,1);eyeBall(0,-44+f,10,acc,0);for(let i=0;i<3;i++){const q=a+i*2.1;ellipse(Math.cos(q)*34,-34+Math.sin(q)*14+bob,4,6,c);}}
  else if(shape==='golem'){ctx.save();ctx.scale(1.25,1.25);for(const s of[-1,1])ellipse(s*12,-4,9,6,dark);ctx.beginPath();ctx.roundRect(-26,-54,52,50,12);ctx.fillStyle=c;ctx.fill();for(const s of[-1,1]){ellipse(s*30,-34,10,13,c);ellipse(s*30,-34,5,6,dark);}poly([[-20,-52],[-10,-62],[2,-52]],dark);line(-14,-48,-6,-40,dark,2);line(10,-44,18,-36,dark,2);grin(0,-22,40,16,6,1);for(const s of[-1,1])angryEye(s*10,-40,5,s,acc);gloss(-14,-50,7,3);ctx.restore();}
  else if(shape==='mage'){poly([[-20,0],[-10,-40],[0,-70+bob],[10,-40],[20,0]],c);poly([[-18,0],[-6,-32],[6,-32],[18,0]],dark);ellipse(0,-32,13,10,'#1a0a22');for(const s of[-1,1]){ellipse(s*5,-34,4,3,acc);ellipse(s*5,-34,1.5,1.5,'#fff');}teethRow(0,-27,18,5,4,true);line(22,-2,20,-56,'#8a5a2b',4);ellipse(20,-60,7,7,acc);glow({x:20,y:-60},16,acc.replace('hsl','hsla').replace(')',',.5)'));gloss(-6,-56+bob,4,8,.25);}
  else if(shape==='warrior'||shape==='skeleton'){poly([[-16,0],[-12,-26],[12,-26],[16,0]],dark);ellipse(0,-36,19,19,c);ellipse(0,-34,14,13,'#f3ecde');for(const s of[-1,1])ellipse(s*6,-38,4.5,5,ink());ellipse(0,-30,3,2,ink());teethRow(0,-25,20,6,-4,true,'#f3ecde');line(-2,-29,2,-29,ink(),1);line(16,-10,30,-44,'#d8dde6',4);line(13,-22,26,-16,'#b06a2a',4);legsStub(0,0,dark,8,2,a);}
  else if(shape==='archer'){const sway=Math.sin(a)*2;poly([[-18,0],[-20,-30],[-10,-62+bob],[10,-62+bob],[20,-30],[18,0]],c);ctx.beginPath();ctx.ellipse(0,-50+bob,16,14,0,Math.PI,0);ctx.fillStyle=c;ctx.fill();for(let i=0;i<4;i++)ellipse(-13+i*9,0,5,4+(i%2)*2,c);grin(0,-24+sway,26,13,6,1);for(const s of[-1,1])ellipse(s*6,-42+bob,3,3,ink());ctx.strokeStyle='#e9d28a';ctx.lineWidth=3;ctx.beginPath();ctx.arc(20,-30,16,-1.5,1.5);ctx.stroke();line(21,-46,21,-14,'#fff',1);gloss(-8,-54+bob,4,6,.3);}
  else{ellipse(0,-24,22,20,c);grin(0,-18,30,14,6,1);eyeBall(0,-36,8,acc,0);}
}
// ---- 旧ボス形状にステッカー要素を足す ----
function drawBossSticker(t,c,bob,e,a){
  const acc=t.accent||'#ff4fa3';
  if(t.shape==='earth'){ellipse(0,-28,42,32,c);for(let i=-1;i<=1;i++)poly([[i*23-12,-44],[i*23,-78],[i*23+17,-42]],i%2?'#74694b':'#a28c64');for(const s of[-1,1]){line(s*26,-22,s*38,-2,vivid(c,0,0,-.15),14);poly([[s*22,-50],[s*48,-70],[s*36,-40]],'#f6f1d8');}jaw(0,-34,56,22,9);for(const s of[-1,1])angryEye(s*12,-46,7,s,acc);gloss(-14,-50,10,5);}
  else if(t.shape==='water'){for(let i=0;i<8;i++){const a=i*Math.PI/4;ctx.strokeStyle=c;ctx.lineWidth=9;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(Math.cos(a)*10,-22);ctx.quadraticCurveTo(Math.cos(a)*50,-30+Math.sin(a+i)*12,Math.cos(a)*62,Math.sin(a)*18);ctx.stroke();}ellipse(0,-40+bob,28,34,c);grin(0,-30+bob,34,16,7,1);for(const s of[-1,1])eyeBall(s*10,-52+bob,8,acc,s*.3);gloss(-10,-62+bob,8,5);}
  else if(t.shape==='fire'){poly([[-20,-16],[-72,-8],[-46,-30],[-21,-30]],vivid(c,0,0,-.1));ellipse(0,-26,38,20,c);for(const s of[-1,1])line(s*20,-18,s*30,2,vivid(c,0,0,-.15),10);ellipse(40,-32,22,16,c);jaw(44,-30,34,14,7);angryEye(36,-42,6,1,acc);for(let i=0;i<6;i++)poly([[-30+i*12,-36],[-26+i*12,-62-Math.sin(a+i)*8],[-16+i*12,-34]],i%2?'#ffd43a':'#ff6a2a');}
  else if(t.shape==='wind'){const flap=Math.sin(a)*8;for(const s of[-1,1])poly([[s*6,-33],[s*68,-68-flap],[s*52,-20],[s*28,-24],[s*10,-7]],vivid(c,0,0,-.08));ellipse(0,-26,22,28,c);for(let i=-1;i<=1;i++){line(i*12,-30,i*24,-58+bob,c,11);ellipse(i*24,-64+bob,12,9,c);jaw(i*24,-62+bob,16,7,4);eyeBall(i*24+2,-70+bob,4,acc,0);}}
  else{drawNewBoss(t,c,bob);const shape=t.shape;if(shape==='ogre'||shape==='cyclops'){jaw(0,-58,30,12,6);}else if(shape==='dragon'){jaw(10,-56,22,10,5);eyeBall(6,-66,5,acc,0);}else if(shape==='vampire'||shape==='lich'){teethRow(0,-52+bob,16,5,4,true);}}
}
function drawEnemy(e){const p=project(e.x,e.y),t=enemyTypes[e.type],boss=isBoss(e.type),bob0=time*5+e.x;
 if(p.x<-160||p.x>screenW+160||p.y<-140||p.y>screenH+200)return;
 ellipse(p.x,p.y,boss?44:20,boss?18:9,'#0009');if(e.wind>0){ctx.strokeStyle='#fff';ctx.lineWidth=3;ctx.setLineDash([6,5]);ctx.beginPath();ctx.ellipse(p.x,p.y,boss?65:t.ai==='heavy'?58:27,boss?32:t.ai==='heavy'?29:14,0,0,7);ctx.stroke();ctx.setLineDash([]);if(t.ai==='charger'||e.type===23){const q=project(e.x+Math.cos(e.angle)*5,e.y+Math.sin(e.angle)*5);line(p.x,p.y,q.x,q.y,'#ff4fa3aa',5);}}
 const w=boss?320:200,h=boss?300:220,ph=phaseOf(bob0),a=ph/SPR_FRAMES*Math.PI*2,bob=Math.sin(a)*2;
 const spr=sprite('e:'+e.type+':'+ph,w,h,()=>{if(e.type>=104||t.ai==='boss')drawBossSticker(t,t.color,bob,e,a);else drawMonster(t,e,t.color,bob,a);},{outline:boss?5.5:4.5});
 drawSprite(spr,p.x,p.y,e.elite?1.1:1,e.hit>0);
 const nearby=active&&dist(e,player)<5;if(boss||nearby){ctx.font=(boss?'900 15px':'800 11px')+' sans-serif';ctx.textAlign='center';ctx.lineWidth=4;ctx.strokeStyle='#000';ctx.lineJoin='round';const label=(e.elite?'強・':'')+t.name+(e.elite?' ×'+e.elite:''),ly=p.y-(boss?100:82);ctx.strokeText(label,p.x,ly);ctx.fillStyle=boss?'#ffd43a':'#fff';ctx.fillText(label,p.x,ly);}
 if(e.hp<e.max||boss){const width=boss?80:40,y=p.y-(boss?90:72);ctx.fillStyle='#000';ctx.fillRect(p.x-width/2-1,y-1,width+2,7);ctx.fillStyle='#fff';ctx.fillRect(p.x-width/2,y,width,5);ctx.fillStyle=e.elite?'#ff4fa3':'#ff2e5f';ctx.fillRect(p.x-width/2,y,width*Math.max(0,e.hp/e.max),5);}}

// ---- プレイヤー (ステッカー騎士) ----
function character(e,isPlayer=false){if(!isPlayer){drawEnemy(e);return;}const p=project(e.x,e.y);const hit=player.hit>0;const bob=Math.sin(time*9+e.x)*1.2,walk=keys.w||keys.a||keys.s||keys.d||joy.active||target?Math.sin(time*14)*3:0;
 ellipse(p.x,p.y,16,8,'#0009');ctx.strokeStyle='#ffffff55';ctx.lineWidth=2;ctx.beginPath();ctx.ellipse(p.x,p.y+2,19,9,0,0,Math.PI*2);ctx.stroke();
 const facing=e.facing??-Math.PI/2,side=Math.cos(facing)-Math.sin(facing)>=0?1:-1;
 sticker(p.x,p.y,200,220,()=>{ctx.save();ctx.translate(p.x,p.y);
  const armor=hit?'#fff':'#9fb6cc',armorD=hit?'#fff':'#5f7a94',cape=hit?'#fff':'#ff2e5f';
  // マント
  poly([[-10*side,-40+bob],[-26*side,-6+Math.sin(time*6)*3],[-8*side,-2],[2*side,-34+bob]],cape);
  // 脚
  line(-6,-14,-7-walk,1,armorD,7);line(6,-14,7+walk,1,armorD,7);ellipse(-7-walk,2,6,4,'#2d2a3a');ellipse(7+walk,2,6,4,'#2d2a3a');
  // 胴
  ctx.beginPath();ctx.roundRect(-15,-40+bob,30,30,9);ctx.fillStyle=armor;ctx.fill();poly([[-15,-30+bob],[15,-30+bob],[12,-12],[-12,-12]],armorD);ellipse(0,-24+bob,4,4,'#ffd43a');
  // 肩
  ellipse(-16,-36+bob,9,7,armorD);ellipse(16,-36+bob,9,7,armorD);
  // 兜
  ellipse(0,-52+bob,15,15,armor);ellipse(0,-49+bob,13,8,'#1b1530');for(const s of[-1,1]){ellipse(s*5+side*2,-49+bob,3.2,3.2,'#45e0ff');ellipse(s*5+side*2,-49+bob,1.3,1.3,'#fff');}
  poly([[-4,-66+bob],[0,-80+bob],[4,-66+bob]],'#ff2e5f');line(-14,-56+bob,14,-56+bob,armorD,3);gloss(-6,-60+bob,5,3,.5);
  ctx.restore();
  if(e.shield&&!twoHanded(e.weapon)){poly([[p.x-14*side,p.y-30],[p.x-27*side,p.y-32],[p.x-27*side,p.y-14],[p.x-19*side,p.y-6],[p.x-11*side,p.y-16]],'#45e0ff');poly([[p.x-19*side,p.y-28],[p.x-24*side,p.y-24],[p.x-19*side,p.y-12],[p.x-14*side,p.y-24]],'#fff');}
  drawHeldWeapon(e);
 },{outline:4.5});
}
// ---- 村人 ----
function drawNpc(npc){const p=project(npc.x,npc.y),v=villagers[npc.id],walking=npc.pause<=0,ph=walking?phaseOf(time*7+npc.id):0,a=ph/SPR_FRAMES*Math.PI*2,bob=walking?Math.sin(a)*1.4:0,step=walking?Math.sin(a)*3:0;ellipse(p.x,p.y,13,6,'#0008');
 const spr=sprite('n:'+npc.id+':'+ph,160,180,()=>{const c=vivid(v.color,0,.2,.05);line(-5,-12,-6+step,1,'#2d2a3a',5);line(5,-12,6-step,1,'#2d2a3a',5);ctx.beginPath();ctx.roundRect(-12,-32+bob,24,24,8);ctx.fillStyle=c;ctx.fill();ellipse(0,-42+bob,13,13,'#ffd9b3');ellipse(0,-50+bob,13,6,vivid(v.color,120,0,-.1));for(const s of[-1,1])ellipse(s*5,-42+bob,2.5,3,ink());ellipse(0,-35+bob,4,2,'#c0506a');line(-11,-27+bob,-15,-14-step,'#ffd9b3',4);line(11,-27+bob,15,-14+step,'#ffd9b3',4);gloss(-5,-47+bob,4,2.5,.5);},{outline:3.5});
 drawSprite(spr,p.x,p.y);
 const near=active&&dist(npc,player)<2.5;ctx.textAlign='center';ctx.font=near?'800 12px sans-serif':'900 14px sans-serif';const label=near?npc.name:'···';ctx.lineWidth=4;ctx.strokeStyle='#000';ctx.strokeText(label,p.x,p.y-66);ctx.fillStyle='#ffd43a';ctx.fillText(label,p.x,p.y-66);}
// ---- ペット: 元の描画をステッカー化 ----
function drawPet(){const a=petActor;if(!a)return;const q=project(a.x,a.y);sticker(q.x,q.y,160,160,()=>drawPetPlain(),{outline:3.5});}
'''
html = patch(html, "function drawPet(){const a=petActor;", "function drawPetPlain(){const a=petActor;")
html = patch(html, "}load();requestAnimationFrame(frame);", "}" + JS + "\nload();requestAnimationFrame(frame);")
open(DST, "w", encoding="utf-8").write(html)
print("ok", DST, len(html), "chars; version", NEW_VERSION)
