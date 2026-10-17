import asyncio, os
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); ctx=await b.new_context(viewport={"width":1000,"height":560},device_scale_factor=2,is_mobile=True,has_touch=True)
        page=await ctx.new_page(); await page.goto("file://"+os.path.abspath(__import__("sys").argv[1])); await page.wait_for_timeout(300)
        await page.tap("#start"); await page.wait_for_timeout(300)
        await page.evaluate("(()=>{const r=area.roads[0];player.x=r.x;player.y=r.y;})()"); await page.wait_for_timeout(300)
        n=await page.evaluate('''(()=>{for(let k=0;k<30;k++){const idx=24+k*3;const t=enemyTypes[idx];const ang=k/30*Math.PI*2;area.enemies.push({id:'p'+k,type:idx,x:player.x+Math.cos(ang)*(2+k%5),y:player.y+Math.sin(ang)*(2+k%5),hp:t.hp,max:t.hp,damage:t.damage,cd:2,wind:0,angle:0,facing:0,hit:0});}return area.enemies.length})()''')
        ms=await page.evaluate("(()=>{const t0=performance.now();for(let i=0;i<30;i++)render();return (performance.now()-t0)/30})()")
        print("enemies",n,"render avg ms (headless CPU, dpr2):",round(ms,1))
        await b.close()
asyncio.run(main())
