"""실제 Chromium으로 자동 시연을 돌려 오류·화면을 확인한다. 사용: python _pwdemo.py [switch|field] [초]"""
import sys, time
from playwright.sync_api import sync_playwright
mode = sys.argv[1] if len(sys.argv) > 1 else 'switch'
secs = int(sys.argv[2]) if len(sys.argv) > 2 else 60
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1100, 'height': 1000})
    errs = []
    pg.on('pageerror', lambda e: errs.append('PAGEERROR ' + str(e)))
    pg.on('console', lambda m: errs.append('console.' + m.type + ': ' + m.text) if m.type in ('error', 'warning') else None)
    pg.goto('http://localhost:8765/'); pg.wait_for_timeout(500)
    pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_timeout(500)
    pg.click('button[data-act=mode][data-arg=%s]' % mode)
    pg.click('button[data-act=demo]'); pg.wait_for_timeout(300)
    seen = {}; shots = 0; t0 = time.time(); last = ''
    while time.time() - t0 < secs:
        st = pg.evaluate("({scr:S.screen, auto:S.auto, floor:S.run&&S.run.floor, party:S.run&&S.run.party.map(m=>m.ko+' '+m.hp+'/'+m.maxHp), turn:S.run&&S.run.battle&&S.run.battle.turn, busy:S.run&&S.run.battle&&S.run.battle.busy})")
        key = st['scr']
        seen[key] = seen.get(key, 0) + 1
        line = '%s f%s t%s %s' % (st['scr'], st['floor'], st['turn'], st['party'])
        if line != last:
            print('%5.1fs' % (time.time() - t0), line); last = line
        if key in ('battle', 'reward', 'map', 'event', 'rest', 'shop') and shots < 8 and seen[key] in (1, 6):
            pg.screenshot(path='_demo_%s_%d_%s.png' % (mode, shots, key)); shots += 1
        if not st['auto'] and key in ('win', 'gameover'):
            print('END', key); break
        pg.wait_for_timeout(700)
    print('screens seen', seen)
    print('errors', len(errs)); print('\n'.join(errs[:15]))
    b.close()
