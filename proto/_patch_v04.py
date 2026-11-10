"""v0.4: 10개 지역 지도 + 기술 교사·게임코너·육성가·로켓단 간부 노드 + 협동 전투 필드 칸 제한(동시형). src.html에 1회 적용."""
import pathlib, re
root = pathlib.Path(__file__).parent
p = root / 'src.html'
s = p.read_text(encoding='utf-8')
if 'function scrTutor(' in s:
    raise SystemExit('already patched')
def rep(old, new, count=1):
    global s
    c = s.count(old); assert c == count, ('needle count %d != %d: %s' % (c, count, old[:90])); s = s.replace(old, new)

# ---------- 지역·지형·노드 종류 ----------
rep("const PLACES=['1번도로','상록숲 입구','상록숲','2번도로','월견산 기슭','월견산 동굴','회색시티','회색체육관'];",
    "const PLACES=['1번도로','상록시티','상록숲 입구','상록숲','2번도로','월견산 기슭','월견산 동굴','3번도로','회색시티','회색체육관']; const NF=PLACES.length;")
rep("const TERRAIN=['route','forest','forest','route','mount','cave','city','gym'];", "const TERRAIN=['route','city','forest','forest','route','mount','cave','route','city','gym'];")
s = re.sub(r"const NODE_TXT=\{.*?\};\n", "const NODE_TXT={wild:['풀숲을 헤쳐 간다','야생 포켓몬이 튀어나올 것 같다'],trainer:['트레이너의 시선이 느껴진다','눈이 마주치면 대전!'],elite:['로켓단 간부','강적! 이기면 도구와 희귀 카드'],event:['무언가 반짝인다','무슨 일이 생길지 모른다'],rest:['포켓몬센터','회복 · 훈련 · 진화'],shop:['프렌들리숍','도구 · 열매 · 몬스터볼 · 카드 조금'],tutor:['기술 교사','카드 배우기 · 강화 · 교환 · 잊기 (유료)'],casino:['게임코너','슬롯으로 한몫, 경품으로 포켓몬'],daycare:['포켓몬 육성가','맡기면 최대 HP 상승 · 알 · 진화'],treasure:['보물상자','지닌 도구 3택1'],boss:['체육관','관장에게 도전한다']};\n", s, count=1)
rep("const NODE_ICON={wild:'草',trainer:'!',event:'?',rest:'+',shop:'$',treasure:'★',boss:'◆'};",
    "const NODE_ICON={wild:'草',trainer:'!',elite:'R',event:'?',rest:'+',shop:'$',tutor:'書',casino:'★',daycare:'卵',treasure:'★',boss:'◆'};\nconst BATTLE_NODES=['wild','trainer','elite','boss'];")
rep("const placeOf=(floor)=>PLACES[clamp(floor-1,0,7)];", "const placeOf=(floor)=>PLACES[clamp(floor-1,0,NF-1)];")
rep("bot:'rock',where:[1,2,3]}", "bot:'rock',where:[2,3,4]}")
rep("bot:'berry1',where:[1,2,3,4]}", "bot:'berry1',where:[2,3,4,5]}")
rep("bot:'moon',where:[5,6]}", "bot:'moon',where:[6,7]}")
rep("bot:'adopt',where:[2,3,4]}", "bot:'adopt',where:[3,4,5]}")
rep("bot:'leave',where:[4,5,6]}", "bot:'leave',where:[5,6,7,8]}")
rep("bot:'bath',where:[5,6]}", "bot:'bath',where:[6,7]}")
rep("evo:{to:'gyarados',floor:6}", "evo:{to:'gyarados',floor:7}")
rep("floor:5}", "floor:6}", 4)
rep("floor:8}", "floor:10}", 3)
rep("const BOSS={name:'관장 웅'", "const ELITE={name:'로켓단 간부 아폴로',mons:['zubat','ekans','meowth'],line:'로켓단의 힘을 보여 주지. 네 포켓몬도 곧 우리 것이 된다!'};\nconst BOSS={name:'관장 웅'")

# ---------- 지도 생성 ----------
i0 = s.index("function genMap(){"); i1 = s.index("function reachableOf(r){", i0)
s = s[:i0] + """function genMap(){
  const floors=[]; const TOWN={1:['shop','tutor','casino'],8:['rest','tutor','shop']};
  const roll=(f)=>{ const x=Math.random(); return x<.40?'wild':x<.55&&f>=2?'trainer':x<.75?'event':x<.83?'rest':x<.88?'shop':x<.93?'tutor':x<.97?'casino':'daycare'; };
  for(let f=0;f<NF;f++){ const row=[]; const n=f===NF-1?1:3; const town=TOWN[f]?shuffle(TOWN[f]):null;
    for(let l=0;l<n;l++){ let t='wild'; if(f===NF-1) t='boss'; else if(town) t=town[l]; else if(f===0) t='wild'; else t=roll(f); row.push({f,l,t,name:PLACES[f],next:[],done:false}); }
    floors.push(row); }
  floors[4][R(3)].t='treasure'; floors[7][R(3)].t='elite';
  for(let f=0;f<NF-1;f++){ for(const n of floors[f]){ const cand=floors[f+1].filter(m=>Math.abs(m.l-n.l)<=1||floors[f+1].length===1);
      const k=cand.length>1&&chance(.5)?2:1; n.next=shuffle(cand).slice(0,k).map(m=>m.l); }
    for(const m of floors[f+1]){ if(!floors[f].some(n=>n.next.includes(m.l))){ const near=floors[f].reduce((a,b)=>Math.abs(b.l-m.l)<Math.abs(a.l-m.l)?b:a); near.next.push(m.l);} } }
  return floors;
}
""" + s[i1:]
rep("if(r.pos.f>=7) return []; return r.map[r.pos.f+1].filter(n=>cur.next.includes(n.l)); }", "if(r.pos.f>=NF-1) return []; return r.map[r.pos.f+1].filter(n=>cur.next.includes(n.l)); }")

# ---------- 전투: 야생 표, 엘리트, 필드 칸 ----------
rep("const table=opts.table||(fl<=2?WILD_EARLY:fl<=4?WILD_EARLY.concat(WILD_MID):WILD_MID.concat(WILD_LATE));", "const table=opts.table||(fl<=3?WILD_EARLY:fl<=6?WILD_EARLY.concat(WILD_MID):WILD_MID.concat(WILD_LATE));")
rep("const pairP=modeB?(r.party.length>=3?.6:r.party.length===2?.4:.1):(fl>=4?.3:0);", "const pairP=modeB?(r.party.length>=3?.6:r.party.length===2?.4:.1):(fl>=5?.3:0);")
rep("const t=opts.trainer||pick(TRAINERS); title=t.name+'이(가) 승부를 걸어왔다!';", "const t=opts.trainer||(kind==='elite'?ELITE:pick(TRAINERS)); title=t.name+'이(가) 승부를 걸어왔다!';")
rep("for(const p of parts){ for(const m of p.party){ m.block=0; m.rk={atk:0,def:0,spd:0}; m.st={}; m.sashUsed=false; } if(!modeB){ if(p.party[p.active].hp<=0) p.active=Math.max(0,p.party.findIndex(m=>m.hp>0)); } }",
    "const cap=fieldCap(n); for(const p of parts){ for(const m of p.party){ m.block=0; m.rk={atk:0,def:0,spd:0}; m.st={}; m.sashUsed=false; } if(!modeB){ if(p.party[p.active].hp<=0) p.active=Math.max(0,p.party.findIndex(m=>m.hp>0)); } else { p.fieldIdx=p.party.map((m,i)=>i).filter(i=>p.party[i].hp>0).slice(0,cap); } }")
rep("function fieldMonsOf(r){ return S.mode==='field'?r.party.filter(m=>m.hp>0):(r.party[r.active]&&r.party[r.active].hp>0?[r.party[r.active]]:[]); }",
"""function fieldCap(n){ return Math.max(1,Math.ceil(3/Math.max(1,n))); }
function fieldMonsOf(r){ if(S.mode!=='field') return r.party[r.active]&&r.party[r.active].hp>0?[r.party[r.active]]:[];
  const b=r.battle; if(!b||b.over||!r.fieldIdx) return r.party.filter(m=>m.hp>0); return r.fieldIdx.map(i=>r.party[i]).filter(m=>m&&m.hp>0); }
function benchOf(r){ if(S.mode!=='field'||!r.fieldIdx) return []; return r.party.map((m,i)=>[m,i]).filter(([m,i])=>!r.fieldIdx.includes(i)); }
function fieldSwap(r,bi){ const fi=r.fieldIdx; if(!fi||fi.includes(bi)||!r.party[bi]||r.party[bi].hp<=0) return false; let j=fi.findIndex(i=>r.party[i].hp<=0);
  if(j<0){ j=0; for(let q=1;q<fi.length;q++) if(r.party[fi[q]].hp/r.party[fi[q]].maxHp<r.party[fi[j]].hp/r.party[fi[j]].maxHp) j=q; }
  const out=r.party[fi[j]]; fi[j]=bi; out.block=0; log(out.ko+' 돌아와! 가라, '+r.party[bi].ko+'!'); return true; }
function autoFill(r){ const fi=r.fieldIdx; if(S.mode!=='field'||!fi) return; for(let j=0;j<fi.length;j++){ if(r.party[fi[j]].hp<=0){ const bi=r.party.findIndex((m,i)=>m.hp>0&&!fi.includes(i)); if(bi>=0){ fi[j]=bi; log('가라, '+r.party[bi].ko+'!'); } } } }""")
rep("if(c.owner){ const o=r.party.find(m=>m.uid===c.owner); if(S.mode==='field'){ if(!o||o.hp<=0) return '쓰러진 포켓몬의 기술'; } }",
    "if(c.owner){ const o=r.party.find(m=>m.uid===c.owner); if(S.mode==='field'){ if(!o||o.hp<=0) return '쓰러진 포켓몬의 기술'; if(!fieldMons().includes(o)) return '벤치에 있는 포켓몬의 기술'; } }")
rep("if(c.owner){ const o=r.party.find(m=>m.uid===c.owner); if(o&&o.hp>0) return o; } return null; }", "if(c.owner){ const o=r.party.find(m=>m.uid===c.owner); if(o&&o.hp>0&&fieldMons().includes(o)) return o; } return null; }")
rep("if(S.mode==='switch'&&r.party[r.active].hp<=0){ const i=r.party.findIndex(m=>m.hp>0); if(i>=0){ r.active=i; log('가라, '+r.party[i].ko+'!'); } }\n    startTurn();",
    "if(S.mode==='switch'&&r.party[r.active].hp<=0){ const i=r.party.findIndex(m=>m.hp>0); if(i>=0){ r.active=i; log('가라, '+r.party[i].ko+'!'); } } else autoFill(r);\n    startTurn();")
rep("case 'bench': { const i=+arg; if(b.sel&&b.sel.kind==='switch'){ doSwitch(i); b.sel=null; } else if(b.freeSwitch){ doSwitch(i); b.freeSwitch=false; }",
    "case 'bench': { const i=+arg; if(S.mode==='field'){ if(b.freeSwitch&&fieldSwap(r,i)) b.freeSwitch=false; } else if(b.sel&&b.sel.kind==='switch'){ doSwitch(i); b.sel=null; } else if(b.freeSwitch){ doSwitch(i); b.freeSwitch=false; }")
rep("if(S.mode==='switch'&&b.freeSwitch&&r.party[r.active].hp<r.party[r.active].maxHp*.3){ const i=r.party.findIndex((m,k)=>k!==r.active&&m.hp>r.party[r.active].hp); if(i>=0){ doSwitch(i); b.freeSwitch=false; } }\n    const order=",
    "if(S.mode==='switch'&&b.freeSwitch&&r.party[r.active].hp<r.party[r.active].maxHp*.3){ const i=r.party.findIndex((m,k)=>k!==r.active&&m.hp>r.party[r.active].hp); if(i>=0){ doSwitch(i); b.freeSwitch=false; } }\n    if(S.mode==='field'&&b.freeSwitch&&r.fieldIdx){ const weak=fieldMonsOf(r).find(m=>m.hp<m.maxHp*.3); const bi=r.party.findIndex((m,i)=>m.hp>m.maxHp*.5&&!r.fieldIdx.includes(i)); if(weak&&bi>=0&&fieldSwap(r,bi)) b.freeSwitch=false; }\n    const order=")
# 자동 진행(사람 자리)의 전투는 봇 턴 함수를 그대로 쓴다
i0 = s.index("  if(scr==='battle'){ const b=r.battle; if(b.busy||b.over) return; if(b.sel&&b.sel.kind==='switch')")
i1 = s.index("  if(scr==='reward'){", i0)
s = s[:i0] + "  if(scr==='battle'){ const b=r.battle; if(b.busy||b.over||b.botAct) return; botTurn(b).then(()=>{ if(S.screen==='battle'&&!b.busy&&!b.over&&S.auto) endTurn(); }); return; }\n" + s[i1:]

# 전투 화면: 동시형 필드/벤치
rep("if(modeB){ h+='<div class=\"field three\" style=\"margin-top:10px\">'+r.party.map((m,i)=>monCard(m,{back:true,big:true,target:allyPick&&m.hp>0,attr:allyPick&&m.hp>0?'data-act=\"ally\" data-arg=\"'+i+'\"':''})).join('')+'</div>'; }",
    "if(modeB){ const fset=new Set(r.fieldIdx||r.party.map((m,i)=>i)); const bench=benchOf(r); h+='<div class=\"field three\" style=\"margin-top:10px\">'+r.party.map((m,i)=>fset.has(i)?monCard(m,{back:true,big:true,target:allyPick&&m.hp>0,attr:allyPick&&m.hp>0?'data-act=\"ally\" data-arg=\"'+i+'\"':''}):'').join('')+'</div>'; if(bench.length) h+='<div class=\"tiny muted\" style=\"margin:6px 0 2px\">벤치 (필드 '+fieldCap(b.n||1)+'칸 · '+(pl.freeSwitch?'무료 교체 1회 남음: 클릭하면 HP 비율이 낮은 쪽과 교체':'이번 턴 교체 사용함')+')</div><div class=\"row\" style=\"gap:6px\">'+bench.map(([m,i])=>monCard(m,{small:true,bench:m.hp>0&&pl.freeSwitch,attr:m.hp>0&&pl.freeSwitch?'data-act=\"bench\" data-arg=\"'+i+'\"':''})).join('')+'</div>'; }")
rep("p.party.map((m,i)=>monCard(m,{small:true,back:true,active:S.mode==='switch'&&i===p.active})).join('')", "p.party.map((m,i)=>monCard(m,{small:true,back:true,active:fieldMonsOf(p).includes(m)})).join('')")

# ---------- 노드 열기 ----------
rep("if(n.t==='wild') startBattle('wild'); else if(n.t==='trainer') startBattle('trainer'); else if(n.t==='boss') startBattle('boss');",
    "if(n.t==='wild') startBattle('wild'); else if(n.t==='trainer') startBattle('trainer'); else if(n.t==='elite') startBattle('elite'); else if(n.t==='boss') startBattle('boss');")
rep("else if(n.t==='shop'){ r.shop=genShop(); S.screen='shop'; render(); } else if(n.t==='treasure'){",
    "else if(n.t==='shop'){ r.shop=genShop(); S.screen='shop'; render(); } else if(n.t==='tutor'){ r.tutor=genTutor(); S.screen='tutor'; render(); } else if(n.t==='casino'){ r.casino=genCasino(); S.screen='casino'; render(); } else if(n.t==='daycare'){ r.daycare={raised:false}; S.screen='daycare'; render(); } else if(n.t==='treasure'){")
rep("function genShop(){ const r=S.run; const cards=rewardCards(4);", "function genShop(){ const r=S.run; const cards=rewardCards(2);")
rep("if(n.t==='wild'||n.t==='trainer'||n.t==='boss'){ S.run=me; startBattle(n.t,{parts:group});", "if(BATTLE_NODES.includes(n.t)){ S.run=me; startBattle(n.t,{parts:group});")
rep("try{ if(n.t==='wild'||n.t==='trainer'||n.t==='boss'){ S.run=bots[0]; startBattle(n.t,{parts:bots,lead:bots[0]});", "try{ if(BATTLE_NODES.includes(n.t)){ S.run=bots[0]; startBattle(n.t,{parts:bots,lead:bots[0]});")
rep("else if(['reward','event','rest','shop'].includes(S.screen)) botStep(p); else break; }", "else if(['reward','event','rest','shop','tutor','casino','daycare'].includes(S.screen)) botStep(p); else break; }")
rep("(b.kind==='boss'?'관장전':b.kind==='wild'?'야생 '+b.enemies.map(e=>e.ko).join('·'):'트레이너')", "(b.kind==='boss'?'관장전':b.kind==='wild'?'야생 '+b.enemies.map(e=>e.ko).join('·'):b.kind==='elite'?'로켓단 간부':'트레이너')")
rep("finally { for(const p of bots){ p.battle=null; p.reward=null; p.event=null; p.shop=null; p.lastNews=''; }", "finally { for(const p of bots){ p.battle=null; p.reward=null; p.event=null; p.shop=null; p.tutor=null; p.casino=null; p.daycare=null; p.lastNews=''; }")
rep("async function toMap(){ const r=H(); S.run=r; r.reward=null; r.event=null; r.shop=null; S.ui={};", "async function toMap(){ const r=H(); S.run=r; r.reward=null; r.event=null; r.shop=null; r.tutor=null; r.casino=null; r.daycare=null; S.ui={};")
rep("h+={title:scrTitle,starter:scrStarter,map:scrMap,battle:scrBattle,reward:scrReward,event:scrEvent,rest:scrRest,shop:scrShop,", "h+={title:scrTitle,starter:scrStarter,map:scrMap,battle:scrBattle,reward:scrReward,event:scrEvent,rest:scrRest,shop:scrShop,tutor:scrTutor,casino:scrCasino,daycare:scrDaycare,")
rep("if(scr==='gameover'||scr==='win'){ S.auto=false; render(); return; }", "if(scr==='tutor'||scr==='casino'||scr==='daycare'){ botStep(r); toMap(); return; }\n  if(scr==='gameover'||scr==='win'){ S.auto=false; render(); return; }")

# ---------- 지도 그리기: 열 수·아이콘 ----------
rep("const W=760, HH=340, colW=W/8;", "const W=NF*95, HH=340, colW=W/NF;")
rep("for(let f=0;f<8;f++){ const t=TERRAIN[f];", "for(let f=0;f<NF;f++){ const t=TERRAIN[f];")
rep("for(let f=0;f<8;f++) svg+='<text x=", "for(let f=0;f<NF;f++) svg+='<text x=")
rep(" '</defs>';\nfunction marker(", """ '<symbol id="n-elite" viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="#d9d4e8"/><circle cx="20" cy="15" r="6" fill="#f3d2b0"/><path d="M14 15 a6 6 0 0 1 12 0z" fill="#222"/><path d="M10 33 q10 -16 20 0z" fill="#333"/><text x="20" y="32" text-anchor="middle" font-size="11" font-family="Jua,sans-serif" fill="#e02020" font-weight="700">R</text></symbol>'+
 '<symbol id="n-tutor" viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="#ffe9c4"/><rect x="10" y="11" width="20" height="18" rx="2" fill="#f7efd8" stroke="#a97b4f" stroke-width="2"/><path d="M14 17 h12 M14 21 h12 M14 25 h8" stroke="#a97b4f" stroke-width="1.6"/></symbol>'+
 '<symbol id="n-casino" viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="#f3d6ff"/><rect x="10" y="10" width="20" height="20" rx="4" fill="#8e44ad"/><circle cx="15" cy="15" r="2.2" fill="#fff"/><circle cx="25" cy="15" r="2.2" fill="#fff"/><circle cx="20" cy="20" r="2.2" fill="#fff"/><circle cx="15" cy="25" r="2.2" fill="#fff"/><circle cx="25" cy="25" r="2.2" fill="#fff"/></symbol>'+
 '<symbol id="n-daycare" viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="#e3f5d6"/><ellipse cx="20" cy="21" rx="9" ry="11" fill="#fff8e6" stroke="#b9a66b" stroke-width="1.5"/><circle cx="17" cy="17" r="2" fill="#7cc06a"/><circle cx="23" cy="23" r="2.4" fill="#7cc06a"/><circle cx="22" cy="14" r="1.4" fill="#7cc06a"/></symbol>'+
 '</defs>';
function marker(""")
rep("'<div class=\"tiny muted\" style=\"margin-top:6px\">풀숲 야생 · 트레이너 · 표지판 이벤트 · 빨간 지붕 포켓몬센터 · 파란 지붕 상점 · 상자 보물 · 체육관</div>'", "'<div class=\"tiny muted\" style=\"margin-top:6px\">풀숲 야생 · 트레이너 · R 로켓단 간부 · 표지판 이벤트 · 빨간 지붕 포켓몬센터 · 파란 지붕 상점 · 두루마리 기술 교사 · 주사위 게임코너 · 알 육성가 · 상자 보물 · 체육관</div>'")
rep("' <span class=\"muted tiny\">('+r.floor+'/8)</span></span>", "' <span class=\"muted tiny\">('+r.floor+'/'+NF+')</span></span>")

# ---------- 새 노드 화면·처리 ----------
rep("function scrDeck(){", r"""function genTutor(){ const r=S.run; return {cards:rewardCards(5),sold:{},removeCost:75+25*(r.hist.filter(h=>h==='rm').length),ups:0,swaps:0}; }
function scrTutor(){ const r=S.run, t=r.tutor, ui=S.ui; let h='<div class="panel"><div class="row" style="justify-content:space-between;align-items:center"><h2>기술 교사</h2><span class="pill">'+r.money+'원</span></div><p class="muted">"기술을 가르치고, 다듬고, 바꿔 주지. 물론 공짜는 아니야."</p>';
 h+='<h3 style="margin-top:8px">배우기 <span class="tiny muted">일반 50원 · 희귀 100원</span></h3><div class="hand">'+t.cards.map((c,i)=>t.sold['c'+i]?'':cardHtml(c,i,{noPlay:true,big:true,attr:'data-act="tbuy" data-arg="'+i+'"'})).join('')+'</div>';
 h+='<div class="grid"><div class="item"><div class="nm">강화</div><div class="tiny">카드 1장 강화 (피해 +3 / 방어·회복 +3·+10 / 변화 카드 코스트 −1). 방문당 2회</div><button class="tiny" data-act="tup" '+(r.money<60||t.ups>=2?'disabled':'')+' style="margin-top:6px">60원'+(t.ups>=2?' (끝)':'')+'</button></div>'+
  '<div class="item"><div class="nm">교환</div><div class="tiny">기술 카드 1장을 넘기고 같은 포켓몬의 다른 기술 2택1. 방문당 2회</div><button class="tiny" data-act="tswap" '+(r.money<40||t.swaps>=2?'disabled':'')+' style="margin-top:6px">40원'+(t.swaps>=2?' (끝)':'')+'</button></div>'+
  '<div class="item"><div class="nm">잊기</div><div class="tiny">덱에서 카드 1장 제거. 할수록 비싸진다</div><button class="tiny" data-act="trm" '+(r.money<t.removeCost||t.sold.rm?'disabled':'')+' style="margin-top:6px">'+t.removeCost+'원</button></div></div>';
 if(ui.upCards) h+=cardPickList(ui.upCards,'tuppick','강화할 카드를 고르세요'); if(ui.rmCards) h+=cardPickList(ui.rmCards,'trmpick','잊을 카드를 고르세요'); if(ui.swapCards) h+=cardPickList(ui.swapCards,'tswappick','넘길 카드를 고르세요'); if(ui.swapChoice) h+=cardPickList(ui.swapChoice,'tswapchoose','받을 카드를 고르세요');
 return h+'<div style="margin-top:12px"><button class="primary" data-act="tomap">나간다</button></div></div>'; }
function genCasino(){ return {spins:0,prizes:shuffle(['pikachu','sandshrew','meowth','psyduck','oddish']).slice(0,2),msgs:[],bought:false}; }
function scrCasino(){ const r=S.run, c=r.casino; let h='<div class="panel"><div class="row" style="justify-content:space-between;align-items:center"><h2>게임코너</h2><span class="pill">'+r.money+'원</span></div><p class="muted">"어서 오세요! 슬롯 한 판에 30원. 경품은 150원부터!"</p>';
 h+='<div class="row" style="align-items:center"><button class="primary" data-act="spin" '+(r.money<30||c.spins>=5?'disabled':'')+'>슬롯 돌리기 30원 <small>(남은 '+(5-c.spins)+'회)</small></button><span class="tiny muted">60원 30% · 희귀 카드 20% · 도구 10% · 꽝 40%</span></div>';
 if(c.msgs.length) h+='<div class="news"><ul style="padding-left:16px;margin:2px 0">'+c.msgs.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul></div>';
 h+='<h3 style="margin-top:10px">경품 교환 <span class="tiny muted">150원 · 1회</span></h3><div class="row">'+c.prizes.map(sp=>{ const p=SP[sp]; return '<div class="item"><div class="row" style="align-items:center">'+pic(p.types,p.ko,sp,false,'')+'<div><div class="nm">'+p.ko+'</div>'+p.types.map(typeTag).join(' ')+'</div></div><button class="tiny" data-act="prize" data-arg="'+sp+'" '+(r.money<150||c.bought?'disabled':'')+' style="margin-top:6px">'+(r.party.length<3?'동료로 받기':'기술 카드로 받기')+' 150원</button></div>'; }).join('')+'</div>';
 return h+'<div style="margin-top:12px"><button class="primary" data-act="tomap">나간다</button></div></div>'; }
function scrDaycare(){ const r=S.run, d=r.daycare; let h='<div class="panel"><div class="row" style="justify-content:space-between;align-items:center"><h2>포켓몬 육성가</h2><span class="pill">'+r.money+'원</span></div><p class="muted">"포켓몬을 맡겨 두면 튼튼해진답니다. 알도 하나 가져가렴."</p>';
 h+='<h3 style="margin-top:8px">맡기기 <span class="tiny muted">50원 · 최대 HP +10, HP 20% 회복 · 1마리</span></h3><div class="row">'+r.party.map(m=>'<button data-act="dcraise" data-arg="'+m.uid+'" '+(r.money<50||d.raised?'disabled':'')+'>'+m.ko+' <small>HP '+m.hp+'/'+m.maxHp+'</small></button>').join('')+'</div>';
 const cands=r.party.filter(canEvolve);
 h+='<div class="row" style="margin-top:10px"><button data-act="dcegg" '+(r.egg||d.egg?'disabled':'')+'>알 받기 (무료)<small>'+(r.egg?'이미 알을 갖고 있다':'전투 2회 후 부화')+'</small></button>'+cands.map(m=>'<button data-act="dcevo" data-arg="'+m.uid+'">진화: '+m.ko+' → '+SP[SP[m.sp].evo.to].ko+'<small>무료</small></button>').join('')+'</div>';
 if(d.msg) h+='<p class="tiny">'+esc(d.msg)+'</p>';
 return h+'<div style="margin-top:12px"><button class="primary" data-act="tomap">나간다</button></div></div>'; }
function scrDeck(){""")

rep("    case 'buycard': {", r"""    case 'tbuy': { const t=r.tutor; const c=t.cards[+arg]; const price=def(c).rare?100:50; if(r.money<price){ toast('원이 부족하다'); return; } r.money-=price; r.deck.push(c); t.sold['c'+arg]=true; SFX.play('buy'); render(); } break;
    case 'tup': { if(r.money<60||r.tutor.ups>=2) return; S.ui={upCards:r.deck.filter(c=>!c.up)}; render(); } break;
    case 'tuppick': { const c=S.ui.upCards[+arg]; c.up=true; r.money-=60; r.tutor.ups++; S.ui={}; SFX.play('buy'); toast(cname(c)+' 강화'); render(); } break;
    case 'trm': { if(r.money<r.tutor.removeCost) return; S.ui={rmCards:r.deck.slice()}; render(); } break;
    case 'trmpick': { const c=S.ui.rmCards[+arg]; r.money-=r.tutor.removeCost; r.deck=r.deck.filter(x=>x.uid!==c.uid); r.tutor.sold.rm=true; r.hist.push('rm'); S.ui={}; toast(cname(c)+' 제거'); render(); } break;
    case 'tswap': { if(r.money<40||r.tutor.swaps>=2) return; S.ui={swapCards:r.deck.filter(c=>c.owner&&r.party.some(m=>m.uid===c.owner))}; render(); } break;
    case 'tswappick': { const c=S.ui.swapCards[+arg]; const o=r.party.find(m=>m.uid===c.owner); const pool=shuffle(SP[o.sp].pool.filter(id=>M[id]&&id!==c.id)).slice(0,2); if(!pool.length){ toast('바꿀 기술이 없다'); return; } r.money-=40; r.tutor.swaps++; r.deck=r.deck.filter(x=>x.uid!==c.uid); S.ui={swapChoice:pool.map(id=>mkCard(id,o.uid))}; render(); } break;
    case 'tswapchoose': { const c=S.ui.swapChoice[+arg]; r.deck.push(c); S.ui={}; SFX.play('buy'); toast(cname(c)+' 습득'); render(); } break;
    case 'spin': { const c=r.casino; if(r.money<30||c.spins>=5) return; r.money-=30; c.spins++; const x=Math.random(); let msg; if(x<.3){ r.money+=60; msg='🍒🍒🍒 60원!'; } else if(x<.5){ const o=pick(r.party); const pool=SP[o.sp].pool.filter(id=>M[id]&&M[id].rare); const id=pool.length?pick(pool):pick(SP[o.sp].pool.filter(id=>M[id])); const nc=mkCard(id,o.uid); r.deck.push(nc); msg='7️⃣7️⃣7️⃣ 희귀 카드: '+cname(nc)+'!'; } else if(x<.6){ const its=Object.keys(ITEMS).filter(i=>!r.items.includes(i)); if(its.length){ const it=pick(its); r.items.push(it); msg='⭐ 도구: '+ITEMS[it][0]+'!'; } else { r.money+=30; msg='도구가 다 떨어져서 30원 환불.'; } } else msg='꽝...'; c.msgs.push(msg); SFX.play(x<.6?'buy':'weak'); render(); } break;
    case 'prize': { const c=r.casino; if(r.money<150||c.bought) return; r.money-=150; c.bought=true; const sp=arg; if(r.party.length<3){ r.party.push(joinMon(sp)); c.msgs.push(SP[sp].ko+'이(가) 파티에 들어왔다!'); } else { r.deck.push(mkCard(pick(SP[sp].moves.filter(id=>M[id])),null)); c.msgs.push('파티가 가득 차 '+SP[sp].ko+'의 기술 카드를 받았다.'); } SFX.play('capok'); render(); } break;
    case 'dcraise': { const d=r.daycare; if(r.money<50||d.raised) return; const m=r.party.find(x=>x.uid===+arg); r.money-=50; d.raised=true; m.maxHp+=10; heal(m,Math.round(m.maxHp*.2)+10); d.msg=m.ko+'의 최대 HP가 10 올랐다.'; SFX.play('heal'); render(); } break;
    case 'dcegg': { if(r.egg) return; r.egg={left:2}; r.daycare.egg=true; r.daycare.msg='알을 받았다. 전투 2회 후 부화한다.'; render(); } break;
    case 'dcevo': { const m=r.party.find(x=>x.uid===+arg); const id=evolve(m); SFX.play('evolve'); r.daycare.msg=m.ko+'(으)로 진화했다! 새 기술 카드: '+KO[id].n; render(); } break;
    case 'buycard': {""")

# 봇: 새 노드 처리·선호
rep("  if(scr==='shop'){ const sh=r.shop; const bought=[];", r"""  if(scr==='tutor'){ const t=r.tutor; const did=[]; if(t.cards[0]&&r.money>=(def(t.cards[0]).rare?100:50)+60){ const pr=def(t.cards[0]).rare?100:50; r.money-=pr; r.deck.push(t.cards[0]); did.push('카드 '+cname(t.cards[0])); } if(r.money>=60){ const c=r.deck.find(x=>!x.up&&def(x).dmg); if(c){ c.up=true; r.money-=60; did.push(cname(c)+' 강화'); } } r.lastNews='기술 교사: '+(did.join(', ')||'구경만 함'); r.tutor=null; S.screen='map'; return; }
  if(scr==='casino'){ const c=r.casino; const did=[]; while(r.money>=80&&c.spins<3){ r.money-=30; c.spins++; const x=Math.random(); if(x<.3){ r.money+=60; did.push('60원'); } else if(x<.5){ const o=pick(r.party); const pool=SP[o.sp].pool.filter(id=>M[id]); r.deck.push(mkCard(pick(pool),o.uid)); did.push('카드'); } else if(x<.6){ const its=Object.keys(ITEMS).filter(i=>!r.items.includes(i)); if(its.length){ r.items.push(pick(its)); did.push('도구'); } } else did.push('꽝'); } if(r.money>=200&&r.party.length<3){ r.money-=150; r.party.push(joinMon(c.prizes[0])); did.push(SP[c.prizes[0]].ko+' 경품'); } r.lastNews='게임코너: '+(did.join(', ')||'구경만 함'); r.casino=null; S.screen='map'; return; }
  if(scr==='daycare'){ const did=[]; if(r.money>=50){ const m=r.party.reduce((a,x)=>a.maxHp<x.maxHp?a:x); r.money-=50; m.maxHp+=10; heal(m,Math.round(m.maxHp*.2)+10); did.push(m.ko+' HP+10'); } if(!r.egg){ r.egg={left:2}; did.push('알'); } const ev=r.party.find(canEvolve); if(ev){ evolve(ev); did.push(ev.ko+' 진화'); } r.lastNews='육성가: '+did.join(', '); r.daycare=null; S.screen='map'; return; }
  if(scr==='shop'){ const sh=r.shop; const bought=[];""")
rep("if(n.t==='event') sc+=1.5; if(n.t==='boss') sc+=10; return [sc,n]; });", "if(n.t==='event') sc+=1.5; if(n.t==='boss') sc+=10; if(n.t==='elite') sc+=hpf>.7?2:0; if(n.t==='tutor') sc+=p.money>=110?3:.5; if(n.t==='casino') sc+=p.money>=120?2:.3; if(n.t==='daycare') sc+=(p.egg?.5:2)+(p.party.some(m=>SP[m.sp].evo&&p.floor+1>=SP[m.sp].evo.floor)?3:0); return [sc,n]; });")

# 제목·도움말 문구
rep("<small>최대 3마리가 모두 필드에. 적도 2마리씩 자주 나옴. 카드는 소유 포켓몬이 서 있어야 쓸 수 있고, 적은 HP가 낮은 쪽을 노린다.</small>", "<small>최대 3마리가 모두 필드에. 적도 2마리씩 자주 나옴. 카드는 소유 포켓몬이 서 있어야 쓸 수 있고, 적은 HP가 낮은 쪽을 노린다. 협동 전투에서는 필드가 팀 합산 최대 4칸(1인당 ⌈3/인원⌉)이고 나머지는 벤치.</small>")
rep("<tr><td>진행</td><td colspan=2>지역 단위로 동시 진행.", "<tr><td>동시형 필드</td><td colspan=2>참가자 1인당 ⌈3/인원⌉칸(2인 2칸, 3·4인 1칸). 나머지는 벤치: 턴당 무료 교체 1회(HP 비율 낮은 쪽과 교체), 쓰러지면 벤치가 자동 등판</td></tr><tr><td>진행</td><td colspan=2>지역 단위로 동시 진행.")
rep("'<h3>성장</h3><p>레벨 없음. 카드 보상(야생·트레이너·상점),", "'<h3>지역과 시설</h3><p>1번도로 → 상록시티 → 상록숲 입구 → 상록숲 → 2번도로 → 월견산 기슭 → 월견산 동굴 → 3번도로 → 회색시티 → 회색체육관. 상록시티·회색시티는 시설만 있는 마을(상점·기술 교사·게임코너·포켓몬센터). <b>기술 교사</b>: 카드 5장 판매, 강화 60원, 교환 40원(같은 포켓몬의 다른 기술 2택1), 잊기. <b>게임코너</b>: 슬롯 30원(5회), 경품 150원으로 포켓몬. <b>육성가</b>: 50원에 최대 HP +10, 알 무료, 진화. <b>로켓단 간부</b>(3번도로): 엘리트 전투, 도구+희귀 카드.</p>'+\n'<h3>성장</h3><p>레벨 없음. 카드 보상(야생·트레이너·상점·기술 교사·게임코너),")

p.write_text(s, encoding='utf-8')
q = root / '_sim3.js'; t = q.read_text(encoding='utf-8')
t = t.replace("else if(['reward','event','rest','shop'].includes(S.screen)){", "else if(['reward','event','rest','shop','tutor','casino','daycare'].includes(S.screen)){")
q.write_text(t, encoding='utf-8')
print('patched', len(s))
