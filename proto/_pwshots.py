"""새 화면 캡처: 10지역 지도, 기술 교사, 게임코너, 육성가, 동시형 협동 전투(벤치)."""
import sys; sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1100,'height':1000}); errs=[]
    pg.on('pageerror',lambda e:errs.append('PAGEERROR '+str(e))); pg.on('console',lambda m: errs.append(m.type+': '+m.text) if m.type in('error','warning') else None)
    pg.goto('http://localhost:8765/'); pg.wait_for_timeout(400); pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_timeout(400)
    pg.click('button[data-act=mode][data-arg=field]'); pg.click('button[data-act=mpn][data-arg="3"]'); pg.wait_for_timeout(100); pg.click('button[data-act=mpmode][data-arg=split]'); pg.wait_for_timeout(100)
    pg.click('button[data-act=newrun]'); pg.wait_for_timeout(150); pg.click('div[data-act=starter][data-arg="0"]'); pg.wait_for_timeout(400)
    pg.screenshot(path='_v4_map.png'); print('map types', pg.evaluate("S.run.map.map(row=>row.map(n=>n.t).join('/')).join(' | ')"))
    for scr,setup in [('tutor',"S.run.tutor=genTutor()"),('casino',"S.run.casino=genCasino()"),('daycare',"S.run.daycare={raised:false}")]:
        pg.evaluate(setup+"; S.screen='%s'; render();"%scr); pg.wait_for_timeout(250); pg.screenshot(path='_v4_%s.png'%scr)
    # 기술 교사 조작: 카드 구매, 강화, 교환, 잊기
    pg.evaluate("S.run.tutor=genTutor(); S.run.money=400; S.screen='tutor'; render();"); pg.wait_for_timeout(200)
    pg.click('[data-act=tbuy]'); pg.click('[data-act=tup]'); pg.wait_for_timeout(150); pg.click('[data-act=tuppick]'); pg.wait_for_timeout(150)
    pg.click('[data-act=tswap]'); pg.wait_for_timeout(150); pg.click('[data-act=tswappick]'); pg.wait_for_timeout(150); pg.click('[data-act=tswapchoose]'); pg.wait_for_timeout(150)
    print('after tutor: money', pg.evaluate("S.run.money"), 'deck', pg.evaluate("S.run.deck.length"), 'ups', pg.evaluate("S.run.deck.filter(c=>c.up).length"))
    pg.evaluate("S.run.casino=genCasino(); S.run.money=300; S.screen='casino'; render();"); pg.wait_for_timeout(150)
    for i in range(3): pg.click('[data-act=spin]'); pg.wait_for_timeout(120)
    pg.click('[data-act=prize]'); pg.wait_for_timeout(150); pg.screenshot(path='_v4_casino2.png'); print('casino msgs', pg.evaluate("S.run.casino.msgs"), 'party', pg.evaluate("S.run.party.map(m=>m.ko)"))
    pg.evaluate("S.run.daycare={raised:false}; S.screen='daycare'; render();"); pg.wait_for_timeout(150); pg.click('[data-act=dcraise]'); pg.click('[data-act=dcegg]'); pg.wait_for_timeout(150); print('daycare', pg.evaluate("S.run.daycare.msg"), pg.evaluate("S.run.egg"))
    # 협동 동시형 전투: 파티 3마리로 만든 뒤 셋이 함께 야생전
    pg.evaluate("S.run.party.push(joinMon('pidgey')); S.screen='map'; render();"); pg.wait_for_timeout(150)
    pg.evaluate("(async()=>{ const me=H(); const n=reachableOf(me)[0]; for(const p of S.multi.players) S.multi.intents[p.id]=n.f+','+n.l; await chooseNode(n); })()"); pg.wait_for_timeout(800)
    print('battle parts', pg.evaluate("S.run.battle&&S.run.battle.parts"), 'fieldIdx', pg.evaluate("S.multi.players.map(p=>p.fieldIdx)"), 'field mons', pg.evaluate("allField(S.run.battle).map(m=>m.ko)"))
    pg.screenshot(path='_v4_coop_field.png')
    pg.click('[data-act=bench]'); pg.wait_for_timeout(300); print('after bench swap fieldIdx', pg.evaluate("H().fieldIdx"), 'free', pg.evaluate("H().battle.freeSwitch"), 'log', pg.evaluate("H().battle.log.slice(-2)"))
    pg.click('button[data-act=end]'); pg.wait_for_timeout(3500); print('turn', pg.evaluate("H().battle.turn"), 'log', pg.evaluate("H().battle.log.slice(-5)"))
    pg.screenshot(path='_v4_coop_field2.png')
    print('errors', len(errs)); print('\n'.join(errs[:10])); b.close()
