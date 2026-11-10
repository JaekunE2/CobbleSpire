import sys, json, asyncio
from playwright.sync_api import sync_playwright
url=sys.argv[1] if len(sys.argv)>1 else 'http://localhost:8765/'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1100,'height':900})
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m: errs.append('console.'+m.type+': '+m.text) if m.type in('error','warning') else None)
    pg.goto(url); pg.wait_for_timeout(600)
    pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_timeout(500)
    def click(sel,label=''):
        pg.click(sel); pg.wait_for_timeout(250); print('clicked',label or sel,'| screen=',pg.evaluate("S.screen"),'| errs=',len(errs))
    click('button[data-act=chart][data-arg=orig]','원작')
    click('button[data-act=mode][data-arg=field]','동시형')
    click('button[data-act=newrun]','새 모험')
    click('div[data-act=starter][data-arg="0"]','파이리')
    print('reachable',pg.evaluate("reachable().map(n=>n.t+n.f+','+n.l)"))
    click('button[data-act=node]','첫 노드')
    for t in range(12):
        scr=pg.evaluate("S.screen")
        if scr!='battle': break
        # play first playable card
        played=pg.evaluate("""(()=>{const b=S.run.battle; for(let i=0;i<b.hand.length;i++){ const c=b.hand[i]; if(!canPlay(c)){ const nt=needsTarget(c); if(nt==='enemy'){ playCard(i,{kind:'enemy',e:b.enemies.find(x=>x.hp>0)}); } else if(nt==='ally'){ playCard(i,{kind:'ally',m:fieldMons()[0]}); } else playCard(i); return c.id; } } return null; })()""")
        if played is None:
            click('button[data-act=end]','턴 종료')
        else: print('played',played, 'errs', len(errs))
    print('final screen',pg.evaluate("S.screen"))
    pg.screenshot(path='_shot.png'); print('\n'.join(errs[:10]))
    b.close()
