import asyncio, os, sys, json
from playwright.async_api import async_playwright

HTML = "file://" + os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "index.html")
OUT = os.path.abspath("shots"); os.makedirs(OUT, exist_ok=True)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={"width": 1000, "height": 560}, device_scale_factor=2,
                                  is_mobile=True, has_touch=True, locale="ja-JP")
        page = await ctx.new_page()
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: errors.append("console." + m.type + ": " + m.text) if m.type == "error" else None)
        await page.goto(HTML)
        await page.wait_for_timeout(500)
        await page.screenshot(path=f"{OUT}/m00_intro.png")
        await page.fill("#name", "灰の旅人")
        await page.tap("#start")
        await page.wait_for_timeout(600)
        await page.screenshot(path=f"{OUT}/m01_village.png")
        # HUD 要素の表示・レイアウト確認
        boxes = {}
        for sel in ["#top", "#right", "#joyZone", "#actions", "#versionBadge", "#mini"]:
            bb = await page.locator(sel).bounding_box()
            boxes[sel] = bb
        print("boxes", json.dumps(boxes))
        # ジョイスティック操作: 右上方向へドラッグして移動
        jb = boxes["#joyZone"]; cx, cy = jb["x"] + jb["width"] / 2, jb["y"] + jb["height"] / 2
        pos0 = await page.evaluate("[player.x,player.y]")
        cdp = await ctx.new_cdp_session(page)
        async def touch(kind, x, y):
            await cdp.send("Input.dispatchTouchEvent", {"type": kind, "touchPoints": ([] if kind == "touchEnd" else [{"x": x, "y": y}])})
        await touch("touchStart", cx, cy)
        for i in range(1, 11):
            await touch("touchMove", cx + 5 * i, cy - 3 * i)
            await page.wait_for_timeout(30)
        await page.wait_for_timeout(700)
        joy = await page.evaluate("JSON.stringify(joy)")
        await page.screenshot(path=f"{OUT}/m02_joystick.png")
        await touch("touchEnd", 0, 0)
        await page.wait_for_timeout(100)
        pos1 = await page.evaluate("[player.x,player.y]")
        joy2 = await page.evaluate("JSON.stringify(joy)")
        print("joy during:", joy, "after:", joy2, "moved:", pos0, "->", pos1)
        assert pos1 != pos0, "joystick did not move player"
        assert json.loads(joy2)["active"] is False
        # 走る: 外周まで倒す
        await touch("touchStart", cx, cy)
        await touch("touchMove", cx + 80, cy)
        await page.wait_for_timeout(500)
        st = await page.evaluate("[joy.run, sprintMultiplier(), player.stamina]")
        print("run:", st)
        await touch("touchEnd", 0, 0)
        # 街道へ移動して戦場へ (直接テレポートで検証)
        await page.evaluate("(()=>{const r=area.roads[0];player.x=r.x;player.y=r.y;})()")
        await page.wait_for_timeout(300)
        info = await page.evaluate("[area.type, area.name, area.enemies.length]")
        print("after road:", info)
        await page.wait_for_timeout(300)
        await page.screenshot(path=f"{OUT}/m03_field.png")
        # 攻撃ボタン長押し
        ab = await page.locator("#btnAttack").bounding_box()
        await touch("touchStart", ab["x"] + ab["width"] / 2, ab["y"] + ab["height"] / 2)
        await page.wait_for_timeout(400)
        held = await page.evaluate("[mouse.held, cd.attack]")
        await page.screenshot(path=f"{OUT}/m04_attack.png")
        await touch("touchEnd", 0, 0)
        await page.wait_for_timeout(100)
        held2 = await page.evaluate("mouse.held")
        print("attack held:", held, "released:", held2)
        assert held[0] is True and held2 is False
        # スキルボタン
        for sel, key in [("#btnSpin", "spin"), ("#btnDash", "dash")]:
            bb = await page.locator(sel).bounding_box()
            await touch("touchStart", bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2)
            await touch("touchEnd", 0, 0)
            await page.wait_for_timeout(50)
            print(key, "cd:", await page.evaluate(f"cd.{key}"))
        # 地面タップで移動先指定
        await touch("touchStart", 500, 200); await touch("touchEnd", 0, 0)
        await page.wait_for_timeout(50)
        print("target:", await page.evaluate("target"))
        # メニュー類
        for btn, name in [("#inventoryBtn", "inventory"), ("#mapBtn", "map"), ("#settingsBtn", "settings")]:
            await page.tap(btn); await page.wait_for_timeout(300)
            await page.screenshot(path=f"{OUT}/m05_{name}.png")
            opened = await page.evaluate("$('modal').open")
            print(name, "modal open:", opened, "joy active:", await page.evaluate("joy.active"))
            await page.keyboard.press("Escape"); await page.wait_for_timeout(200)
        # 小さい画面 (6インチ級 横)
        await page.set_viewport_size({"width": 800, "height": 380})
        await page.wait_for_timeout(300)
        await page.screenshot(path=f"{OUT}/m06_small.png")
        # 版表示
        print("version badge:", await page.evaluate("$('versionBadge').textContent"), await page.evaluate("typeof VERSION===\"undefined\"?null:VERSION"))
        # 30秒分の進行で例外が無いか
        for i in range(60):
            await page.evaluate("tick(0.04)")
        print("errors:", errors)
        await b.close()

asyncio.run(main())
