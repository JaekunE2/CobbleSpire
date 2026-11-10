from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1100,'height':760}); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://localhost:8765/'); pg.wait_for_timeout(400); pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_timeout(400)
    pg.click('button[data-act=mode][data-arg=switch]'); pg.click('button[data-act=newrun]'); pg.click('div[data-act=starter][data-arg="0"]'); pg.click('button[data-act=node]'); pg.wait_for_timeout(300)
    # 공격 카드 하나 내고 120ms 뒤 캡처 (버스트·숫자)
    pg.evaluate("(()=>{const b=S.run.battle; const i=b.hand.findIndex(c=>def(c).dmg>0); if(i>=0) playCard(i);})()")
    pg.wait_for_timeout(140); pg.screenshot(path='_fx_attack.png')
    pg.click('button[data-act=end]'); pg.wait_for_timeout(600); pg.screenshot(path='_fx_enemy.png')
    pg.wait_for_timeout(1500)
    pg.emulate_media(color_scheme='dark'); pg.wait_for_timeout(200); pg.screenshot(path='_fx_dark.png')
    print('errs',errs); b.close()
