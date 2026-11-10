"""실제 Chromium으로 멀티(투표형/분산형) 화면 흐름을 사람 시점에서 점검한다.
사용: python _pwmulti.py vote|split [인원=3] [switch|field] [초=70]"""
import sys; sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import sys, time
from playwright.sync_api import sync_playwright
mp = sys.argv[1] if len(sys.argv) > 1 else 'vote'
n = int(sys.argv[2]) if len(sys.argv) > 2 else 3
mode = sys.argv[3] if len(sys.argv) > 3 else 'switch'
secs = int(sys.argv[4]) if len(sys.argv) > 4 else 70
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1100, 'height': 1100})
    errs = []
    pg.on('pageerror', lambda e: errs.append('PAGEERROR ' + str(e)))
    pg.on('console', lambda m: errs.append('console.' + m.type + ': ' + m.text) if m.type in ('error', 'warning') else None)
    pg.goto('http://localhost:8765/'); pg.wait_for_timeout(500)
    pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_timeout(500)
    pg.screenshot(path='_mp_title.png')
    pg.click('button[data-act=mode][data-arg=%s]' % mode)
    pg.click('button[data-act=mpn][data-arg="%d"]' % n); pg.wait_for_timeout(150)
    pg.click('button[data-act=mpmode][data-arg=%s]' % mp); pg.wait_for_timeout(150)
    pg.screenshot(path='_mp_lobby_%s.png' % mp)
    # 사람 경로: 새 모험 → 스타터 → 첫 노드 클릭 → 카드 몇 장 → 턴 종료 → 자동 ON으로 나머지 진행
    pg.click('button[data-act=newrun]'); pg.wait_for_timeout(200)
    pg.click('div[data-act=starter][data-arg="1"]'); pg.wait_for_timeout(300)
    print('players', pg.evaluate("S.multi.players.map(p=>p.name+':'+p.party[0].ko)"), 'intents', pg.evaluate("S.multi.intents"))
    pg.screenshot(path='_mp_map0_%s.png' % mp)
    pg.click('g.node.open'); pg.wait_for_timeout(600)
    print('after node: screen', pg.evaluate("S.screen"), 'parts', pg.evaluate("S.run.battle?S.run.battle.parts:null"), 'lastVote', pg.evaluate("S.multi.lastVote"))
    if pg.evaluate("S.screen") == 'battle':
        pg.screenshot(path='_mp_battle0_%s.png' % mp)
        # 사람 카드 1장 사용 (대상 선택 포함)
        for i in range(3):
            r = pg.evaluate("""(()=>{const b=S.run.battle; if(b.busy) return 'busy'; for(let i=0;i<b.hand.length;i++){ const c=b.hand[i]; if(!canPlay(c)){ const nt=needsTarget(c); if(nt==='enemy'){ playCard(i,{kind:'enemy',e:b.enemies.find(x=>x.hp>0)}); } else if(nt==='ally'){ playCard(i,{kind:'ally',m:fieldMons()[0]}); } else playCard(i); return c.id; } } return null; })()""")
            print('play', r); pg.wait_for_timeout(300)
            if r in (None, 'busy'): break
        pg.click('button[data-act=end]'); pg.wait_for_timeout(1500)
        pg.screenshot(path='_mp_battle1_%s.png' % mp)
        print('after end: turn', pg.evaluate("S.run.battle&&S.run.battle.turn"), 'busy', pg.evaluate("S.run.battle&&S.run.battle.busy"), 'cur', pg.evaluate("S.run.battle&&S.run.battle.curPid"), 'log', pg.evaluate("S.run.battle?S.run.battle.log.slice(-6):null"))
    # 자동 진행
    pg.evaluate("S.auto=true; render();")
    seen = {}; t0 = time.time(); last = ''; shots = 0
    while time.time() - t0 < secs:
        st = pg.evaluate("({scr:S.screen, auto:S.auto, floor:S.run&&S.run.floor, me:S.run&&S.run.name, party:S.run&&S.run.party.map(m=>m.ko+' '+m.hp+'/'+m.maxHp), bots:S.multi?S.multi.players.filter(p=>p.bot).map(p=>p.name+' f'+p.floor+(p.dead?' dead':'')+' '+p.party.map(m=>m.hp).join('/')):null, news:S.multi?S.multi.news:null, resolving:S.resolving})")
        key = st['scr']; seen[key] = seen.get(key, 0) + 1
        line = '%s f%s %s | %s | %s' % (st['scr'], st['floor'], st['party'], st['bots'], st['news'])
        if line != last:
            print('%5.1fs' % (time.time() - t0), line); last = line
        if key in ('map', 'battle', 'reward', 'event', 'rest', 'shop') and shots < 10 and seen[key] in (2, 7):
            pg.screenshot(path='_mp_%s_%d_%s.png' % (mp, shots, key)); shots += 1
        if not st['auto'] and key in ('win', 'gameover'):
            pg.screenshot(path='_mp_%s_end.png' % mp); print('END', key); break
        pg.wait_for_timeout(700)
    print('screens', seen, 'me is human?', pg.evaluate("S.run===H()"))
    print('errors', len(errs)); print('\n'.join(errs[:15]))
    b.close()
