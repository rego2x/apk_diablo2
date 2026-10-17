import asyncio, os, sys
from playwright.async_api import async_playwright
HTML="file://"+os.path.abspath("index_sticker.html")
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); ctx=await b.new_context(viewport={"width":1000,"height":560},device_scale_factor=2,is_mobile=True,has_touch=True)
        page=await ctx.new_page(); errs=[]; page.on("pageerror",lambda e:errs.append(str(e)))
        await page.goto(HTML); await page.wait_for_timeout(300)
        await page.screenshot(path="shots/g0_intro.png")
        await page.tap("#start"); await page.wait_for_timeout(500)
        await page.screenshot(path="shots/g1_village.png")
        await page.evaluate("(()=>{const r=area.roads[0];player.x=r.x;player.y=r.y;})()"); await page.wait_for_timeout(400)
        # 各形状の敵を周囲に配置
        js='''(()=>{const want=['slime','beast','spider','bat','crystal','golem','mage','warrior','archer','skeleton'];area.enemies=[];let k=0;
        for(const sh of want){const idx=enemyTypes.findIndex((t,i)=>t.shape===sh&&t.ai!=='boss');if(idx<0)continue;const t=enemyTypes[idx];const ang=k/want.length*Math.PI*2;area.enemies.push({id:'g'+k,type:idx,x:player.x+Math.cos(ang)*4.2,y:player.y+Math.sin(ang)*4.2,hp:t.hp,max:t.hp,damage:t.damage,cd:2,wind:0,angle:0,facing:0,hit:0});k++;}
        for(const [j,bt] of [20,21,22,23,104,105,106,107,108,109,110,111].entries()){const t=enemyTypes[bt];const ang=j/12*Math.PI*2;area.enemies.push({id:'b'+j,type:bt,x:player.x+Math.cos(ang)*9.5,y:player.y+Math.sin(ang)*9.5,hp:t.hp,max:t.hp,damage:t.damage,cd:99,wind:0,angle:0,facing:0,hit:0,attacks:0});}
        return area.enemies.length;})()'''
        n=await page.evaluate(js); print("placed",n)
        await page.evaluate("render()"); await page.wait_for_timeout(200)
        await page.screenshot(path="shots/g2_gallery.png")
        # ズーム相当: カメラを少し動かした別ショット
        await page.evaluate("camera.x=player.x+4;camera.y=player.y+4;render()"); await page.wait_for_timeout(100)
        await page.screenshot(path="shots/g3_gallery2.png")
        await page.tap("#inventoryBtn"); await page.wait_for_timeout(300); await page.screenshot(path="shots/g4_inv.png")
        await page.keyboard.press("Escape"); await page.wait_for_timeout(200)
        await page.evaluate("bestiary()"); await page.wait_for_timeout(300); await page.screenshot(path="shots/g5_bestiary.png")
        print("errors",errs); await b.close()
asyncio.run(main())
