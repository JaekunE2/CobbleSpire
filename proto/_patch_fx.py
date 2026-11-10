p='src.html'; s=open(p,encoding='utf-8').read()
def rep(a,b,cnt=1):
    global s
    assert s.count(a)==cnt, ('NOT FOUND/UNIQUE', a[:80], s.count(a))
    s=s.replace(a,b)

# ---------- CSS ----------
rep("</style>", r"""
/* 스프라이트·이펙트 */
.spr{image-rendering:pixelated;image-rendering:crisp-edges;width:64px;height:64px;object-fit:contain;flex:none;filter:drop-shadow(0 3px 2px rgba(0,0,0,.35))}
.spr.big{width:96px;height:96px}
.spr.sm{width:40px;height:40px}
.ico{image-rendering:pixelated;width:22px;height:22px;vertical-align:middle;margin-right:2px}
.mon{position:relative;overflow:visible}
.mon.hit{animation:shake .35s}
@keyframes shake{20%{transform:translateX(-6px)}40%{transform:translateX(6px)}60%{transform:translateX(-4px)}80%{transform:translateX(3px)}}
.mon.fainting .spr{animation:faint .6s forwards}
@keyframes faint{to{transform:translateY(24px);opacity:0}}
.burst{position:absolute;left:50%;top:40%;width:18px;height:18px;margin:-9px;border-radius:50%;pointer-events:none;animation:burst .5s forwards;z-index:3}
@keyframes burst{0%{transform:scale(.3);opacity:.9}60%{transform:scale(4);opacity:.5}100%{transform:scale(5.5);opacity:0}}
.fnum{position:absolute;left:55%;top:10px;font-family:var(--display);font-size:22px;pointer-events:none;animation:fnum 1s forwards;z-index:4;text-shadow:0 1px 0 #fff,0 -1px 0 #fff,1px 0 0 #fff,-1px 0 0 #fff;white-space:nowrap}
.fnum.dmg{color:#d42}.fnum.heal{color:#2a4}.fnum.txt{font-size:13px;color:var(--fg);background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:1px 6px;text-shadow:none}
.fnum.super{color:#e0a000;font-size:24px}
@keyframes fnum{0%{transform:translateY(0);opacity:1}100%{transform:translateY(-34px);opacity:0}}
.arena{border-radius:12px;padding:12px;background:linear-gradient(180deg,#8fd0ff 0%,#cfe9c4 55%,#9bc46b 100%);position:relative;overflow:hidden}
:root[data-theme="dark"] .arena{background:linear-gradient(180deg,#223a55 0%,#2f4a33 55%,#3e5a2a 100%)}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) .arena{background:linear-gradient(180deg,#223a55 0%,#2f4a33 55%,#3e5a2a 100%)}}
.arena.rain::after,.arena.sand::after,.arena.sun::after{content:"";position:absolute;inset:0;pointer-events:none}
.arena.rain::after{background:repeating-linear-gradient(115deg,transparent 0 14px,rgba(120,170,255,.35) 14px 16px);animation:rain .5s linear infinite}
@keyframes rain{to{background-position:40px 60px}}
.arena.sand::after{background:repeating-linear-gradient(100deg,transparent 0 9px,rgba(200,170,90,.35) 9px 11px);animation:sand .4s linear infinite}
@keyframes sand{to{background-position:60px 10px}}
.arena.sun::after{background:radial-gradient(circle at 85% 10%,rgba(255,230,120,.7),transparent 45%)}
.arena .mon{background:color-mix(in srgb,var(--panel) 90%,transparent)}
.busyb{font-size:12px;color:var(--muted)}
.ball{display:inline-block;width:40px;height:40px;image-rendering:pixelated;animation:wobble 1.6s ease-in-out 1}
@keyframes wobble{0%,100%{transform:rotate(0)}15%{transform:rotate(-25deg)}30%{transform:rotate(25deg)}45%{transform:rotate(-20deg)}60%{transform:rotate(20deg)}75%{transform:rotate(-10deg)}}
.capres{opacity:0;animation:appear .3s 1.6s forwards}
@keyframes appear{to{opacity:1}}
.cat{display:inline-block;font-size:10px;border-radius:3px;padding:0 4px;color:#fff;font-weight:700}
.cat.p{background:#c0392b}.cat.s{background:#5b4bd6}.cat.x{background:#777}.cat.t{background:#2e8b57}
.hand .card{animation:deal .25s}
@keyframes deal{from{transform:translateY(14px);opacity:0}}
@media (prefers-reduced-motion:reduce){.hand .card,.mon.hit,.burst,.fnum,.ball,.arena::after,.mon.fainting .spr{animation:none!important}}
</style>""")

# ---------- 데이터 ----------
rep("const KO = /*__MOVES_KO__*/{};", "const KO = /*__MOVES_KO__*/{};\nconst SPR = /*__SPRITES__*/{};\nconst DEX={charmander:4,charmeleon:5,charizard:6,squirtle:7,wartortle:8,blastoise:9,bulbasaur:1,ivysaur:2,venusaur:3,pidgey:16,pidgeotto:17,rattata:19,caterpie:10,weedle:13,pikachu:25,sandshrew:27,nidoranm:32,paras:46,zubat:41,diglett:50,meowth:52,geodude:74,slowpoke:79,magnemite:81,mankey:56,oddish:43,ekans:23,spearow:21,gastly:92,machop:66,psyduck:54,magikarp:129,gyarados:130,onix:95};\nconst ICON={leftovers:'leftovers',focussash:'focus-sash',lifeorb:'life-orb',shellbell:'shell-bell',quickclaw:'quick-claw',expshare:'exp-share',oran:'oran-berry',sitrus:'sitrus-berry',lum:'lum-berry',lansat:'lansat-berry',ball:'poke-ball'};")

rep("function orb(types,ko){", "function pic(types,ko,spid,back,size){ const k=(back?'b':'f')+DEX[spid]; const src=SPR[k]; if(src) return '<img class=\"spr '+(size||'')+'\" src=\"'+src+'\" alt=\"'+esc(ko)+'\">'; return orb(types,ko); }\nfunction ico(k){ const src=SPR['i_'+ICON[k]]; return src?'<img class=\"ico\" src=\"'+src+'\" alt=\"\">':''; }\nfunction orb(types,ko){")
rep("<div class=\"row\" style=\"align-items:center\">'+orb(p.types,p.ko)+'<div><div class=\"nm\"", "<div class=\"row\" style=\"align-items:center\">'+pic(p.types,p.ko,p.sp,false,'big')+'<div><div class=\"nm\"")
rep("return '<div class=\"mon '+(m.hp<=0?'fainted':'')+(o.active?' active':'')+(o.target?' target':'')+(o.bench?' bench':'')+'\" '+(o.attr||'')+'><div class=\"row\" style=\"align-items:center;gap:8px;flex-wrap:nowrap\">'+orb(s.types,m.ko)+",
    "return '<div class=\"mon '+(m.hp<=0?'fainted':'')+(o.active?' active':'')+(o.target?' target':'')+(o.bench?' bench':'')+'\" data-uid=\"'+m.uid+'\" '+(o.attr||'')+'><div class=\"row\" style=\"align-items:center;gap:8px;flex-wrap:nowrap\">'+pic(s.types,m.ko,m.sp,o.back,o.small?'sm':o.big?'big':'')+")
rep("return '<div class=\"mon '+(e.hp<=0?'fainted':'')+(targetable?' target':'')+'\" '+(targetable?'data-act=\"target\" data-arg=\"'+e.uid+'\"':'')+'><div class=\"row\" style=\"align-items:center;gap:8px;flex-wrap:nowrap\">'+orb(s.types,e.ko)+",
    "return '<div class=\"mon '+(e.hp<=0?'fainted':'')+(targetable?' target':'')+'\" data-uid=\"'+e.uid+'\" '+(targetable?'data-act=\"target\" data-arg=\"'+e.uid+'\"':'')+'><div class=\"row\" style=\"align-items:center;gap:8px;flex-wrap:nowrap\">'+pic(s.types,e.ko,e.sp,false,'big')+")
rep("h+='<h3 style=\"margin-top:10px\">포획 기회</h3><div class=\"row\" style=\"align-items:center\">'+orb(s.types,s.ko)+'<div>쓰러진",
    "h+='<h3 style=\"margin-top:10px\">포획 기회</h3><div class=\"row\" style=\"align-items:center\">'+pic(s.types,s.ko,rw.capture.sp,false,'big')+'<div>쓰러진")
rep("<div class=\"tiny\">'+typeTag(d.type)+' <span class=\"muted\">'+catName(d)+'</span></div>", "<div class=\"tiny\">'+typeTag(d.type)+' <span class=\"cat '+d.cat+'\">'+catName(d)+'</span></div>")
rep("<span><span class=\"k\">몬스터볼</span>'+r.balls+'</span><span><span class=\"k\">열매</span>'+(r.berries.map(b=>BERRIES[b][0]).join(', ')||'없음')+'</span><span><span class=\"k\">도구</span>'+(r.items.map(i=>ITEMS[i][0]).join(', ')||'없음')+'</span>'",
    "<span><span class=\"k\">몬스터볼</span>'+ico('ball')+r.balls+'</span><span><span class=\"k\">열매</span>'+(r.berries.map(b=>ico(b)+BERRIES[b][0]).join(', ')||'없음')+'</span><span><span class=\"k\">도구</span>'+(r.items.map(i=>ico(i)+ITEMS[i][0]).join(', ')||'없음')+'</span>'")
rep("<button data-act=\"help\" class=\"tiny\">규칙</button>", "<button data-act=\"help\" class=\"tiny\">규칙</button><button data-act=\"auto\" class=\"tiny '+(S.auto?'primary':'')+'\">자동 '+(S.auto?'ON':'OFF')+'</button><button data-act=\"mute\" class=\"tiny\">'+(S.mute?'소리 꺼짐':'소리 켜짐')+'</button>")
rep("'<div class=\"item\"><div class=\"nm\">'+ITEMS[i][0]+'</div><div class=\"tiny\">'+ITEMS[i][1]+'</div><button class=\"tiny\" data-act=\"pickitem\"", "'<div class=\"item\"><div class=\"nm\">'+ico(i)+ITEMS[i][0]+'</div><div class=\"tiny\">'+ITEMS[i][1]+'</div><button class=\"tiny\" data-act=\"pickitem\"")
rep("'<div class=\"item\"><div class=\"nm\">'+ITEMS[i][0]+'</div><div class=\"tiny\">'+ITEMS[i][1]+'</div><button class=\"tiny\" data-act=\"buyitem\"", "'<div class=\"item\"><div class=\"nm\">'+ico(i)+ITEMS[i][0]+'</div><div class=\"tiny\">'+ITEMS[i][1]+'</div><button class=\"tiny\" data-act=\"buyitem\"")
rep("'<div class=\"item\"><div class=\"nm\">'+BERRIES[bk][0]+'</div>", "'<div class=\"item\"><div class=\"nm\">'+ico(bk)+BERRIES[bk][0]+'</div>")
rep("<div class=\"item\"><div class=\"nm\">몬스터볼</div>", "<div class=\"item\"><div class=\"nm\">'+ico('ball')+'몬스터볼</div>")
rep("<button data-act=\"take\" data-arg=\"berry\" '+(r.berries.length>=3?'disabled':'')+'>'+BERRIES[rw.berry][0]+' 받기</button>", "<button data-act=\"take\" data-arg=\"berry\" '+(r.berries.length>=3?'disabled':'')+'>'+ico(rw.berry)+BERRIES[rw.berry][0]+' 받기</button>")
rep("<button data-act=\"take\" data-arg=\"item\">'+ITEMS[rw.item][0]+' 받기</button>", "<button data-act=\"take\" data-arg=\"item\">'+ico(rw.item)+ITEMS[rw.item][0]+' 받기</button>")

# ---------- 전투 화면 ----------
rep("h+='<div class=\"field '+(b.enemies.length>1?'three':'')+'\" style=\"margin-top:8px\">'+b.enemies.map(e=>enemyCard(e,b,targetable&&e.hp>0)).join('')+'</div></div>';",
    "h+='<div class=\"arena '+(b.weather?b.weather.w:'')+'\" style=\"margin-top:8px\"><div class=\"field '+(b.enemies.length>1?'three':'')+'\">'+b.enemies.map(e=>enemyCard(e,b,targetable&&e.hp>0)).join('')+'</div>';")
rep("if(modeB){ h+='<div class=\"field three\">'+r.party.map((m,i)=>monCard(m,{target:allyPick&&m.hp>0,attr:allyPick&&m.hp>0?'data-act=\"ally\" data-arg=\"'+i+'\"':''})).join('')+'</div>'; }",
    "if(modeB){ h+='<div class=\"field three\" style=\"margin-top:10px\">'+r.party.map((m,i)=>monCard(m,{back:true,big:true,target:allyPick&&m.hp>0,attr:allyPick&&m.hp>0?'data-act=\"ally\" data-arg=\"'+i+'\"':''})).join('')+'</div></div></div>'; }")
rep("else { const a=r.party[r.active]; h+='<div class=\"row\"><div class=\"grow\">'+monCard(a,{active:true})+'</div>",
    "else { const a=r.party[r.active]; h+='<div class=\"row\" style=\"margin-top:10px\"><div class=\"grow\">'+monCard(a,{active:true,back:true,big:true})+'</div>")
rep("'</div></div>'; }\n // 손패", "'</div></div></div></div>'; }\n // 손패")
rep("<div class=\"energy\"><b>'+b.energy+'</b>/3 <span class=\"tiny muted\">에너지</span></div>", "<div class=\"energy\"><b>'+b.energy+'</b>/3 <span class=\"tiny muted\">에너지</span>'+(b.busy?' <span class=\"busyb\">상대 턴...</span>':'')+'</div>")
rep("<button class=\"primary\" data-act=\"end\">턴 종료</button>", "<button class=\"primary\" data-act=\"end\" '+(b.busy?'disabled':'')+'>턴 종료</button>")

# ---------- FX 큐 ----------
rep("function log(s){ const b=S.run.battle; b.log.push(s); if(b.log.length>60) b.log.shift(); }",
    "function log(s){ const b=S.run.battle; b.log.push(s); if(b.log.length>60) b.log.shift(); }\nfunction fx(o){ const b=S.run&&S.run.battle; if(b){ (b.fx||(b.fx=[])).push(o); } }")
rep("log(m.ko+'이(가) '+(src?src+'로 ':'')+left+' 피해'+(v-left>0?' (방어 '+(v-left)+')':'')); if(m.hp<=0){ log(m.ko+'은(는) 쓰러졌다!'); m.st={}; } return left; }",
    "log(m.ko+'이(가) '+(src?src+'로 ':'')+left+' 피해'+(v-left>0?' (방어 '+(v-left)+')':'')); fx({k:'dmg',uid:m.uid,v:left,blocked:v-left}); if(m.hp<=0){ log(m.ko+'은(는) 쓰러졌다!'); m.st={}; fx({k:'faint',uid:m.uid}); } return left; }")
rep("function heal(m,v){ const before=m.hp; m.hp=Math.min(m.maxHp,m.hp+v); return m.hp-before; }",
    "function heal(m,v){ const before=m.hp; m.hp=Math.min(m.maxHp,m.hp+v); if(m.hp-before>0) fx({k:'heal',uid:m.uid,v:m.hp-before}); return m.hp-before; }")
rep("const m=eff(d.type,e.types); log(cname(c)+' → '+e.ko+'에게 '+total+' 피해'+(m>1.01?' (효과가 굉장했다!)':m<.99?' (효과가 별로다)':''));",
    "const m=eff(d.type,e.types); log(cname(c)+' → '+e.ko+'에게 '+total+' 피해'+(m>1.01?' (효과가 굉장했다!)':m<.99?' (효과가 별로다)':'')); fx({k:'atk',uid:e.uid,type:d.type,v:total,eff:m});")
rep("if(e.hp<=0){ log(e.ko+'은(는) 쓰러졌다!'); }\n}", "if(e.hp<=0){ log(e.ko+'은(는) 쓰러졌다!'); fx({k:'faint',uid:e.uid}); }\n}")
rep("log(e.ko+'은(는) '+{poison:'독',toxic:'맹독',burn:'화상',para:'마비',sleep:'잠듦'}[f.s]+' 상태가 되었다'); } break;\n      case 'R': { const t=f.who==='s'?owner:e; if(t&&t.hp>0){ t.rk[f.st]=clamp(t.rk[f.st]+f.v,-3,3); log(t.ko+'의 '+{atk:'공격',def:'방어',spd:'스피드'}[f.st]+'이(가) '+(f.v>0?'올랐다':'떨어졌다')); } } break;",
    "log(e.ko+'은(는) '+{poison:'독',toxic:'맹독',burn:'화상',para:'마비',sleep:'잠듦'}[f.s]+' 상태가 되었다'); fx({k:'txt',uid:e.uid,t:{poison:'독',toxic:'맹독',burn:'화상',para:'마비',sleep:'잠듦'}[f.s]}); } break;\n      case 'R': { const t=f.who==='s'?owner:e; if(t&&t.hp>0){ t.rk[f.st]=clamp(t.rk[f.st]+f.v,-3,3); log(t.ko+'의 '+{atk:'공격',def:'방어',spd:'스피드'}[f.st]+'이(가) '+(f.v>0?'올랐다':'떨어졌다')); fx({k:'txt',uid:t.uid,t:{atk:'공격',def:'방어',spd:'스피드'}[f.st]+(f.v>0?' ↑':' ↓')}); } } break;")
rep("case 'B': if(owner){ owner.block+=fxv(c,'B'); } break;", "case 'B': if(owner){ owner.block+=fxv(c,'B'); fx({k:'txt',uid:owner.uid,t:'방어 +'+fxv(c,'B')}); } break;")
rep("else if(isAtk){ const targets=d.all?fm:[m]; for(const t of targets){ const v=enemyDmg(e,id,t); for(let h=0;h<d.hits;h++) dmgMon(t,v,e.ko+'의 '+nm);",
    "else if(isAtk){ const targets=d.all?fm:[m]; for(const t of targets){ const v=enemyDmg(e,id,t); fx({k:'atk',uid:t.uid,type:d.type,v:v*d.hits,eff:eff(d.type,SP[t.sp].types),enemy:true}); for(let h=0;h<d.hits;h++) dmgMon(t,v,e.ko+'의 '+nm);")
rep("switch(f.k){ case 'S': if(m.hp>0){ if(f.s==='poison'||f.s==='toxic') m.st.poison=(m.st.poison||0)+f.v; else if(f.s==='burn') m.st.burn=3; else if(f.s==='para'){ m.st.para=2; b.paraNext=1; } else if(f.s==='sleep') m.st.sleep=2; log(m.ko+'은(는) '+{poison:'독',toxic:'맹독',burn:'화상',para:'마비',sleep:'잠듦'}[f.s]+' 상태가 되었다'); } break;",
    "switch(f.k){ case 'S': if(m.hp>0){ if(f.s==='poison'||f.s==='toxic') m.st.poison=(m.st.poison||0)+f.v; else if(f.s==='burn') m.st.burn=3; else if(f.s==='para'){ m.st.para=2; b.paraNext=1; } else if(f.s==='sleep') m.st.sleep=2; log(m.ko+'은(는) '+{poison:'독',toxic:'맹독',burn:'화상',para:'마비',sleep:'잠듦'}[f.s]+' 상태가 되었다'); fx({k:'txt',uid:m.uid,t:{poison:'독',toxic:'맹독',burn:'화상',para:'마비',sleep:'잠듦'}[f.s]}); } break;")
rep("case 'R': { const t=f.who==='s'?e:m; t.rk[f.st]=clamp(t.rk[f.st]+f.v,-3,3); log(t.ko+'의 '+{atk:'공격',def:'방어',spd:'스피드'}[f.st]+'이(가) '+(f.v>0?'올랐다':'떨어졌다')); } break;\n    case 'B': e.block+=f.v; break;",
    "case 'R': { const t=f.who==='s'?e:m; t.rk[f.st]=clamp(t.rk[f.st]+f.v,-3,3); log(t.ko+'의 '+{atk:'공격',def:'방어',spd:'스피드'}[f.st]+'이(가) '+(f.v>0?'올랐다':'떨어졌다')); fx({k:'txt',uid:t.uid,t:{atk:'공격',def:'방어',spd:'스피드'}[f.st]+(f.v>0?' ↑':' ↓')}); } break;\n    case 'B': e.block+=f.v; fx({k:'txt',uid:e.uid,t:'방어 +'+f.v}); break;")

# ---------- 적 턴 순차 연출 ----------
rep("""function endTurn(){
  const r=S.run, b=r.battle; if(b.over) return; b.sel=null;
  b.hand=b.hand.filter(c=>{ if(def(c).fx.some(f=>f.k==='RET')) return true; b.discard.push(c); return false; });
  b.dmgTaken=0;
  for(const e of b.enemies){ e.block=0; enemyAct(e); if(checkEnd()) { render(); return; } }
  for(const e of b.enemies){ if(e.hp>0) setIntent(e); }""",
"""const sleep=(ms)=>new Promise(res=>setTimeout(res,ms));
async function endTurn(){
  const r=S.run, b=r.battle; if(b.over||b.busy) return; b.sel=null; b.busy=true;
  b.hand=b.hand.filter(c=>{ if(def(c).fx.some(f=>f.k==='RET')) return true; b.discard.push(c); return false; });
  b.dmgTaken=0; SFX.play('end'); render(); await sleep(S.auto?300:450);
  for(const e of b.enemies){ e.block=0; enemyAct(e); render(); if(checkEnd()) { b.busy=false; render(); return; } await sleep(S.auto?450:700); }
  b.busy=false;
  for(const e of b.enemies){ if(e.hp>0) setIntent(e); }""")
rep("function playCard(idx,target){\n  const b=S.run.battle, r=S.run; const c=b.hand[idx]; if(!c) return; const why=canPlay(c); if(why){ toast(why); return; }",
    "function playCard(idx,target){\n  const b=S.run.battle, r=S.run; const c=b.hand[idx]; if(!c||b.busy) return; const why=canPlay(c); if(why){ toast(why); return; } SFX.play('card');")
rep("function canPlay(c){ const b=S.run.battle, r=S.run; const d=def(c); if(ccost(c)>b.energy) return '에너지 부족';",
    "function canPlay(c){ const b=S.run.battle, r=S.run; const d=def(c); if(b.busy) return '상대 턴'; if(ccost(c)>b.energy) return '에너지 부족';")
rep("if(!r.party.some(m=>m.hp>0)){ b.over='lose'; log('눈앞이 캄캄해졌다...'); S.screen='gameover'; return true; }",
    "if(!r.party.some(m=>m.hp>0)){ b.over='lose'; log('눈앞이 캄캄해졌다...'); S.screen='gameover'; SFX.play('lose'); return true; }")
rep("b.over='win'; finishBattle(); return true; }", "b.over='win'; SFX.play('win'); finishBattle(); return true; }")
rep("if(chance(p)){ log('야호! '+e.ko+'을(를) 잡았다!'); b.captured=e; e.hp=0; e.capturedFlag=true; } else log('아깝다! '+e.ko+'이(가) 볼에서 빠져나왔다 ('+Math.round(p*100)+'%)'); }",
    "if(chance(p)){ log('야호! '+e.ko+'을(를) 잡았다!'); b.captured=e; e.hp=0; e.capturedFlag=true; SFX.play('capok'); fx({k:'txt',uid:e.uid,t:'잡았다!'}); } else { log('아깝다! '+e.ko+'이(가) 볼에서 빠져나왔다 ('+Math.round(p*100)+'%)'); SFX.play('capfail'); fx({k:'txt',uid:e.uid,t:'빠져나왔다'}); } }")

# ---------- 포획 연출 ----------
rep("case 'capture': { const rw=r.reward; r.balls--; if(chance(rw.capture.p)){",
    "case 'capture': { const rw=r.reward; if(rw.capAnim) return; r.balls--; rw.capAnim=true; SFX.play('throw'); setTimeout(()=>{ rw.capAnim=false; if(S.screen==='reward') render(); },1900); if(chance(rw.capture.p)){ SFX.play('capok');")
rep("} else rw.capMsg='아깝다! '+SP[rw.capture.sp].ko+'이(가) 볼에서 빠져나와 도망쳤다.'+(r.balls>0?' 다시 던질 수 있다.':'');",
    "} else { SFX.play('capfail'); rw.capMsg='아깝다! '+SP[rw.capture.sp].ko+'이(가) 볼에서 빠져나와 도망쳤다.'+(r.balls>0?' 다시 던질 수 있다.':''); }")
rep("<button data-act=\"capture\" '+(r.balls<=0?'disabled':'')+'>몬스터볼 던지기</button></div>'; if(rw.capMsg) h+='<p class=\"tiny\">'+esc(rw.capMsg)+'</p>'; }",
    "<button data-act=\"capture\" '+(r.balls<=0||rw.capAnim?'disabled':'')+'>'+ico('ball')+'몬스터볼 던지기</button></div>'; if(rw.capAnim) h+='<div class=\"row\" style=\"align-items:center;margin-top:6px\"><img class=\"ball\" src=\"'+(SPR['i_poke-ball']||'')+'\" alt=\"\"><span class=\"capres\">'+esc(rw.capMsg||'')+'</span></div>'; else if(rw.capMsg) h+='<p class=\"tiny\">'+esc(rw.capMsg)+'</p>'; }")

# ---------- render 후 FX, 자동 진행 ----------
rep("app.innerHTML=h; }", "app.innerHTML=h; playFx(); scheduleAuto(); }")
rep("/* ---------- 도움말 ---------- */", r"""function playFx(){ const b=S.run&&S.run.battle; if(!b||!b.fx||!b.fx.length) return; const list=b.fx; b.fx=[]; let i=0;
  for(const f of list){ const el=app.querySelector('[data-uid="'+f.uid+'"]'); if(!el) continue; const delay=i*110; i++;
    setTimeout(()=>{ if(!el.isConnected) return;
      if(f.k==='atk'){ const col=f.type==='trainer'?'#999':TYPES[f.type][1]; const bu=document.createElement('div'); bu.className='burst'; bu.style.background='radial-gradient(circle,'+col+',transparent 70%)'; el.appendChild(bu); setTimeout(()=>bu.remove(),600); if(f.eff>1.01) SFX.play('super'); else if(f.eff<.99) SFX.play('weak'); else SFX.play('hit'); if(f.eff>1.01) num(el,'효과가 굉장했다!','super',0); else if(f.eff<.99) num(el,'효과가 별로다','txt',0); }
      else if(f.k==='dmg'){ el.classList.remove('hit'); void el.offsetWidth; el.classList.add('hit'); num(el,'-'+f.v,'dmg',8); if(f.blocked) num(el,'방어 '+f.blocked,'txt',44); }
      else if(f.k==='heal'){ num(el,'+'+f.v,'heal',8); SFX.play('heal'); }
      else if(f.k==='txt'){ num(el,f.t,'txt',22); SFX.play('status'); }
      else if(f.k==='faint'){ el.classList.add('fainting'); SFX.play('faint'); }
    },delay); } }
function num(el,text,cls,top){ const n=document.createElement('div'); n.className='fnum '+cls; n.textContent=text; n.style.top=top+'px'; el.appendChild(n); setTimeout(()=>n.remove(),1100); }
/* ---------- 효과음 (WebAudio 합성, 외부 파일 없음) ---------- */
const SFX={ctx:null,on(){ if(S.mute) return null; try{ if(!this.ctx) this.ctx=new (window.AudioContext||window.webkitAudioContext)(); if(this.ctx.state==='suspended') this.ctx.resume(); return this.ctx; }catch(e){ return null; } },
  tone(f,t,type,g,slide){ const c=this.on(); if(!c) return; const o=c.createOscillator(), v=c.createGain(); o.type=type||'square'; o.frequency.setValueAtTime(f,c.currentTime); if(slide) o.frequency.exponentialRampToValueAtTime(slide,c.currentTime+t); v.gain.setValueAtTime(g||.05,c.currentTime); v.gain.exponentialRampToValueAtTime(.0005,c.currentTime+t); o.connect(v); v.connect(c.destination); o.start(); o.stop(c.currentTime+t); },
  noise(t,g){ const c=this.on(); if(!c) return; const n=Math.floor(c.sampleRate*t), buf=c.createBuffer(1,n,c.sampleRate), d=buf.getChannelData(0); for(let i=0;i<n;i++) d[i]=(Math.random()*2-1)*(1-i/n); const s=c.createBufferSource(); s.buffer=buf; const v=c.createGain(); v.gain.value=g||.08; const f=c.createBiquadFilter(); f.type='lowpass'; f.frequency.value=1800; s.connect(f); f.connect(v); v.connect(c.destination); s.start(); },
  play(k){ try{ switch(k){ case 'hit': this.noise(.12,.1); this.tone(180,.12,'square',.04,90); break; case 'super': this.noise(.18,.14); this.tone(320,.2,'sawtooth',.05,80); break; case 'weak': this.tone(200,.1,'triangle',.03,150); break;
    case 'heal': [523,659,784].forEach((f,i)=>setTimeout(()=>this.tone(f,.15,'sine',.05),i*70)); break; case 'status': this.tone(440,.08,'square',.03,330); break; case 'card': this.tone(900,.05,'square',.02,1200); break; case 'end': this.tone(300,.08,'triangle',.03); break;
    case 'faint': this.tone(400,.5,'sawtooth',.05,60); break; case 'win': [392,523,659,784].forEach((f,i)=>setTimeout(()=>this.tone(f,.18,'square',.05),i*110)); break; case 'lose': [330,262,196].forEach((f,i)=>setTimeout(()=>this.tone(f,.3,'triangle',.05),i*220)); break;
    case 'throw': this.tone(700,.15,'sine',.04,300); [0,500,1000].forEach(d=>setTimeout(()=>this.tone(250,.06,'square',.04),400+d)); break; case 'capok': setTimeout(()=>[523,659,784,1046].forEach((f,i)=>setTimeout(()=>this.tone(f,.15,'square',.05),i*90)),1500); break; case 'capfail': setTimeout(()=>this.tone(300,.3,'sawtooth',.05,120),1500); break; case 'evolve': [440,554,659,880].forEach((f,i)=>setTimeout(()=>this.tone(f,.25,'sine',.05),i*120)); break; case 'buy': this.tone(1200,.08,'square',.03); break; } }catch(e){} } };
/* ---------- 자동 진행 (봇 시뮬레이션) ---------- */
let autoTimer=null;
function scheduleAuto(){ clearTimeout(autoTimer); if(!S.auto||!S.run) return; autoTimer=setTimeout(autoTick,S.screen==='battle'?650:900); }
function autoTick(){ if(!S.auto||!S.run) return; const r=S.run, scr=S.screen; try{
  if(scr==='map'){ const re=reachable(); if(re.length) enterNode(pick(re)); return; }
  if(scr==='battle'){ const b=r.battle; if(b.busy||b.over) return; if(b.sel&&b.sel.kind==='switch'){ const i=r.party.findIndex((m,k)=>k!==r.active&&m.hp>0); if(i>=0) doSwitch(i); b.sel=null; render(); return; }
    if(S.mode==='switch'&&b.freeSwitch&&r.party[r.active].hp<r.party[r.active].maxHp*.3){ const i=r.party.findIndex((m,k)=>k!==r.active&&m.hp>r.party[r.active].hp); if(i>=0){ doSwitch(i); b.freeSwitch=false; for(const e of b.enemies) if(e.hp>0) e.target=r.party[r.active].uid; render(); return; } }
    const order=b.hand.map((c,i)=>i).sort((x,y)=>(def(b.hand[y]).dmg||0)-(def(b.hand[x]).dmg||0));
    for(const i of order){ const c=b.hand[i]; if(canPlay(c)) continue; const nt=needsTarget(c); if(nt==='enemy'){ const e=b.enemies.filter(x=>x.hp>0).sort((p,q)=>p.hp-q.hp)[0]; playCard(i,{kind:'enemy',e}); } else if(nt==='ally'){ const fm=fieldMons().slice().sort((p,q)=>p.hp/p.maxHp-q.hp/q.maxHp); playCard(i,{kind:'ally',m:fm[0]}); } else playCard(i); return; }
    endTurn(); return; }
  if(scr==='reward'){ const rw=r.reward; if(rw.capAnim) return; if(rw.money&&!rw.took.money){ takeReward('money'); return; } if(rw.badge&&!rw.took.badge){ takeReward('badge'); return; } if(rw.berry&&!rw.took.berry){ takeReward('berry'); return; } if(rw.item&&!rw.took.item){ takeReward('item'); return; }
    if(rw.items3&&!rw.took.items3){ r.items.push(rw.items3[0]); rw.took.items3=true; render(); return; } if(rw.cards&&rw.cards.length&&!rw.took.cards){ const best=rw.cards.slice().sort((x,y)=>(def(y).dmg||0)-(def(x).dmg||0))[0]; r.deck.push(best); rw.took.cards=true; render(); return; }
    if(rw.capture&&!rw.took.capture&&r.balls>0&&r.party.length<3){ const bt=app.querySelector('[data-act=capture]'); if(bt&&!bt.disabled){ bt.click(); return; } } if(rw.capture&&!rw.took.capture){ rw.took.capture=true; }
    if(rw.partyFull){ takeReward('fullcard'); return; } if(rw.evo&&!rw.took.evo){ const bt=app.querySelector('[data-act=evolve]'); if(bt){ bt.click(); return; } rw.took.evo=true; render(); return; }
    const go=app.querySelector('[data-act='+(rw.kind==='boss'?'win':'tomap')+']'); if(go) go.click(); return; }
  if(scr==='event'){ const ev=r.event; if(!ev.done){ doEvent({forget:'rm1',fisher:'fish',camper:'camp',thief:'fight',mossrock:'rock',dojo:'train'}[ev.id]); return; } if(ev.pickCard){ const cs=ev.pickCard.cards; const i=Math.max(0,cs.findIndex(x=>['guard','growl','tailwhip','splashc'].includes(x.id))); const bt=app.querySelectorAll('[data-act=evpick]')[i]; if(bt) bt.click(); return; } if(ev.upCard){ const bt=app.querySelector('[data-act=evup]'); if(bt) bt.click(); return; } const go=app.querySelector('[data-act=tomap]'); if(go) go.click(); return; }
  if(scr==='rest'){ if(S.ui.upCards){ const bt=app.querySelector('[data-act=restup]'); if(bt) bt.click(); return; } if(S.ui.restDone){ const go=app.querySelector('[data-act=tomap]'); if(go) go.click(); return; } const m=r.party.find(canEvolve); doRest(m?'evo:'+m.uid:(r.party.some(x=>x.hp<x.maxHp*.6)?'heal':'train')); return; }
  if(scr==='shop'){ const sh=r.shop; if(!sh.sold.c0&&sh.cards[0]&&r.money>=(def(sh.cards[0]).rare?100:50)){ const bt=app.querySelector('[data-act=buycard]'); if(bt){ bt.click(); return; } } if(r.money>=50&&r.balls<3){ const bt=app.querySelector('[data-act=buyball]'); if(bt){ bt.click(); return; } } const go=app.querySelector('[data-act=tomap]'); if(go) go.click(); return; }
  if(scr==='gameover'||scr==='win'){ S.auto=false; render(); return; }
  }catch(e){ console.error('auto',e); S.auto=false; render(); } }
/* ---------- 도움말 ---------- */""")
rep("case 'mode': S.mode=arg; render(); break;", "case 'mode': S.mode=arg; render(); break; case 'auto': S.auto=!S.auto; render(); break; case 'mute': S.mute=!S.mute; try{localStorage.setItem('cobblespire-mute',S.mute?'1':'');}catch(e){} render(); break;")
rep("let S={screen:'title',mode:'switch',chart:'soft',run:null,ui:{}};", "let S={screen:'title',mode:'switch',chart:'soft',run:null,ui:{},auto:false,mute:false};")
rep("function boot(data){ if(data&&data.S){ S=data.S; UID=data.UID||UID; } else { try{ const j=JSON.parse(localStorage.getItem('cobblespire-proto')); if(j){ S.mode=j.mode||S.mode; S.chart=j.chart||S.chart; } }catch(e){} } render(); }",
    "function boot(data){ if(data&&data.S){ S=data.S; UID=data.UID||UID; } else { try{ const j=JSON.parse(localStorage.getItem('cobblespire-proto')); if(j){ S.mode=j.mode||S.mode; S.chart=j.chart||S.chart; } S.mute=!!localStorage.getItem('cobblespire-mute'); }catch(e){} } S.auto=false; render(); }")
rep("const id=evolve(m); r.reward.took.evo=true;", "const id=evolve(m); SFX.play('evolve'); r.reward.took.evo=true;")
rep("else if(k.startsWith('evo:')){ const m=r.party.find(x=>x.uid===+k.slice(4)); const id=evolve(m);", "else if(k.startsWith('evo:')){ const m=r.party.find(x=>x.uid===+k.slice(4)); const id=evolve(m); SFX.play('evolve');")
rep("r.money-=price; r.deck.push(c); sh.sold['c'+arg]=true; render(); } break;", "r.money-=price; r.deck.push(c); sh.sold['c'+arg]=true; SFX.play('buy'); render(); } break;")
rep("<button class=\"primary\" data-act=\"newrun\" style=\"font-size:16px;padding:10px 22px\">새 모험 시작</button>", "<button class=\"primary\" data-act=\"newrun\" style=\"font-size:16px;padding:10px 22px\">새 모험 시작</button><button data-act=\"demo\" style=\"font-size:16px;padding:10px 22px\">자동 시연 보기</button>")
rep("case 'newrun': S.screen='starter'; render(); break;", "case 'newrun': S.auto=false; S.screen='starter'; render(); break; case 'demo': S.auto=true; startRun(R(3)); break;")
rep("<p class=\"muted\">코블버스 위의 슬레이 더 스파이어식 로그라이크. 스타터를 고르고, 루트 지도를 따라 1막(회색시티)까지 가 봅니다.<br>이 페이지는 기획서 v0.1의 규칙을 그대로 옮긴 웹 프로토타입입니다. 포켓몬 그림 대신 타입 색 구슬로 표시합니다.</p>",
    "<p class=\"muted\">코블버스 위의 슬레이 더 스파이어식 로그라이크. 스타터를 고르고, 루트 지도를 따라 1막(회색시티)까지 가 봅니다.<br>기획서 v0.1의 규칙을 그대로 옮긴 웹 프로토타입입니다. 포켓몬 그림은 임시로 5세대 스프라이트(실제 모드에서는 Cobblemon 3D 모델), 효과음은 합성음입니다. <b>자동 시연</b>을 누르면 봇이 플레이하는 모습을 볼 수 있고, 상단의 자동 버튼으로 언제든 끌 수 있습니다.</p>")
open(p,'w',encoding='utf-8').write(s); print('patched ok')
