"""멀티(투표형/분산형)·포켓몬풍 지도·지역명·이벤트 확장·배경 패치. src.html에 1회 적용."""
import pathlib, re, urllib.parse
root = pathlib.Path(__file__).parent
p = root / 'src.html'
s = p.read_text(encoding='utf-8')
if 'function chooseNode(' in s:
    raise SystemExit('already patched')

def rep(old, new, count=1):
    global s
    c = s.count(old)
    assert c == count, ('needle count %d != %d: %s' % (c, count, old[:90]))
    s = s.replace(old, new)

def svg(body, w, h):
    raw = "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' preserveAspectRatio='none'>%s</svg>" % (w, h, body)
    return "url(\"data:image/svg+xml," + urllib.parse.quote(raw, safe="' =/:;,.()-") + "\")"

# ---------- 배경 SVG ----------
SKY = "<defs><linearGradient id='s' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#6fbcff'/><stop offset='1' stop-color='#dff2ff'/></linearGradient></defs><rect width='800' height='300' fill='url(#s)'/>"
CLOUDS = "<g fill='#fff' opacity='.85'><ellipse cx='130' cy='62' rx='58' ry='20'/><ellipse cx='160' cy='50' rx='34' ry='16'/><ellipse cx='560' cy='48' rx='74' ry='22'/><ellipse cx='600' cy='38' rx='36' ry='16'/></g>"
BG_ROUTE = svg(SKY + CLOUDS + "<path d='M0 200 Q200 130 400 190 T800 180 V300 H0Z' fill='#a6dd7e'/><path d='M0 236 Q250 196 500 240 T800 226 V300 H0Z' fill='#78c05f'/><g stroke='#4f9a3a' stroke-width='3' fill='none' stroke-linecap='round'><path d='M90 262 l5 -16 l5 16 M100 262 l3 -18 l3 18'/><path d='M300 272 l5 -16 l5 16 M310 272 l3 -18 l3 18'/><path d='M620 258 l5 -16 l5 16 M630 258 l3 -18 l3 18'/></g><path d='M0 300 Q400 262 800 300Z' fill='#5aa347'/>", 800, 300)
BG_FOREST = svg("<defs><linearGradient id='s' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#1f4a2a'/><stop offset='1' stop-color='#3f7a3a'/></linearGradient></defs><rect width='800' height='300' fill='url(#s)'/><g fill='#163d22'><path d='M40 240 L90 110 L140 240Z'/><path d='M150 250 L210 90 L270 250Z'/><path d='M560 250 L620 100 L680 250Z'/><path d='M690 240 L740 120 L790 240Z'/></g><g fill='#215a30'><path d='M0 250 L60 130 L120 250Z'/><path d='M230 260 L300 120 L370 260Z'/><path d='M420 255 L480 115 L540 255Z'/><path d='M640 260 L700 130 L760 260Z'/></g><g fill='#4a2d16'><rect x='84' y='250' width='12' height='30'/><rect x='294' y='258' width='12' height='28'/><rect x='474' y='254' width='12' height='30'/><rect x='694' y='258' width='12' height='28'/></g><path d='M0 300 Q400 250 800 300Z' fill='#2e6b2e'/><circle cx='720' cy='60' r='26' fill='#fff8c0' opacity='.35'/>", 800, 300)
BG_MOUNT = svg(SKY + "<g fill='#9c8a62'><path d='M0 230 L120 90 L240 230Z'/><path d='M180 240 L330 60 L480 240Z'/><path d='M420 236 L560 110 L700 236Z'/><path d='M620 240 L740 120 L860 240Z'/></g><g fill='#f4f1e8'><path d='M300 96 L330 60 L360 96Z'/><path d='M538 128 L560 110 L582 128Z'/></g><path d='M0 232 Q400 200 800 236 V300 H0Z' fill='#cdb98a'/><path d='M0 300 Q400 262 800 300Z' fill='#b39c6d'/>", 800, 300)
BG_CAVE = svg("<rect width='800' height='300' fill='#3a3f4c'/><g fill='#2a2e38'><path d='M0 0 H800 V40 L760 90 L720 40 L660 110 L620 40 L560 80 L520 40 L450 130 L400 40 L340 100 L300 40 L240 120 L190 40 L130 90 L90 40 L40 100 L0 40Z'/></g><g fill='#4c5262'><ellipse cx='120' cy='262' rx='70' ry='26'/><ellipse cx='520' cy='270' rx='90' ry='30'/><ellipse cx='720' cy='258' rx='60' ry='24'/></g><path d='M0 300 Q400 268 800 300Z' fill='#2a2e38'/><g fill='#8fd0ff' opacity='.25'><circle cx='230' cy='210' r='5'/><circle cx='640' cy='190' r='4'/><circle cx='400' cy='228' r='3'/></g>", 800, 300)
BG_CITY = svg(SKY + "<g fill='#9a9892'><rect x='30' y='120' width='70' height='120'/><rect x='120' y='90' width='50' height='150'/><rect x='200' y='140' width='90' height='100'/><rect x='520' y='110' width='60' height='130'/><rect x='600' y='70' width='80' height='170'/><rect x='710' y='130' width='60' height='110'/></g><g fill='#fff2c0'><rect x='40' y='135' width='10' height='10'/><rect x='60' y='135' width='10' height='10'/><rect x='130' y='105' width='8' height='10'/><rect x='150' y='125' width='8' height='10'/><rect x='615' y='90' width='10' height='12'/><rect x='640' y='120' width='10' height='12'/></g><rect x='330' y='150' width='150' height='90' fill='#f3efe3'/><path d='M320 152 L405 100 L490 152Z' fill='#7a1c1c'/><rect x='392' y='200' width='26' height='40' fill='#7a1c1c'/><rect x='0' y='240' width='800' height='60' fill='#b9b2a3'/><g stroke='#d9d4c7' stroke-width='2'><path d='M0 262 H800 M0 284 H800'/></g>", 800, 300)
BG_GYM = svg("<rect width='800' height='300' fill='#4e433a'/><g fill='#6b5c4e'><rect x='60' y='40' width='40' height='200'/><rect x='700' y='40' width='40' height='200'/><rect x='40' y='30' width='80' height='14'/><rect x='680' y='30' width='80' height='14'/></g><g fill='#7d6a52'><ellipse cx='200' cy='250' rx='80' ry='22'/><ellipse cx='600' cy='252' rx='90' ry='24'/><ellipse cx='400' cy='262' rx='120' ry='20'/></g><rect x='0' y='262' width='800' height='38' fill='#8c7756'/><g stroke='#a38d66' stroke-width='3' fill='none'><circle cx='400' cy='275' r='60'/><circle cx='400' cy='275' r='120'/></g><g fill='#d4a017' opacity='.7'><rect x='380' y='70' width='40' height='40' transform='rotate(45 400 90)'/></g>", 800, 300)
BG_TITLE = svg("<defs><linearGradient id='s' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#3f8fe0'/><stop offset='1' stop-color='#cfe9ff'/></linearGradient></defs><rect width='1200' height='360' fill='url(#s)'/><circle cx='1020' cy='80' r='46' fill='#fff2a8'/><g fill='#8aa7c4' opacity='.8'><path d='M0 250 L140 120 L260 250Z'/><path d='M200 260 L380 90 L560 260Z'/><path d='M520 250 L660 140 L800 250Z'/><path d='M760 260 L920 110 L1080 260Z'/><path d='M1000 250 L1120 150 L1240 250Z'/></g><g fill='#f4f1e8' opacity='.9'><path d='M352 118 L380 90 L408 118Z'/><path d='M892 138 L920 110 L948 138Z'/></g><path d='M0 258 Q300 200 600 250 T1200 240 V360 H0Z' fill='#7cc06a'/><g fill='#3f7a3a'><path d='M80 300 L110 240 L140 300Z'/><path d='M150 306 L180 236 L210 306Z'/><path d='M900 300 L930 236 L960 300Z'/><path d='M970 306 L1005 230 L1040 306Z'/><path d='M1050 300 L1080 246 L1110 300Z'/></g><path d='M0 330 Q300 290 600 322 T1200 316 V360 H0Z' fill='#5aa347'/><path d='M520 360 Q560 300 600 300 Q640 300 680 360Z' fill='#d8c48e'/><rect x='560' y='300' width='80' height='48' fill='#f3efe3'/><path d='M552 302 L600 272 L648 302Z' fill='#d9302b'/><rect x='592' y='326' width='16' height='22' fill='#d9302b'/>", 1200, 360)
CLOUD_LAYER = svg("<g fill='#fff' opacity='.9'><ellipse cx='80' cy='40' rx='60' ry='18'/><ellipse cx='110' cy='30' rx='34' ry='14'/><ellipse cx='330' cy='60' rx='70' ry='20'/><ellipse cx='360' cy='48' rx='36' ry='16'/><ellipse cx='560' cy='34' rx='50' ry='16'/></g>", 700, 100)

# ---------- CSS ----------
rep("@media (prefers-reduced-motion:reduce){.hand .card,.mon.hit,.burst,.fnum,.ball,.arena::after,.mon.fainting .spr{animation:none!important}}\n</style>",
"""@media (prefers-reduced-motion:reduce){.hand .card,.mon.hit,.burst,.fnum,.ball,.arena::after,.mon.fainting .spr{animation:none!important}}
/* 장면 배경 (직접 그린 SVG, 외부 리소스 없음) */
.arena{background-size:cover;background-position:center bottom}
.arena.bg-route{background-image:%s}
.arena.bg-forest{background-image:%s}
.arena.bg-mount{background-image:%s}
.arena.bg-cave{background-image:%s}
.arena.bg-city{background-image:%s}
.arena.bg-gym{background-image:%s}
.arena.bg-forest .mon,.arena.bg-cave .mon,.arena.bg-gym .mon{background:color-mix(in srgb,var(--panel) 92%%,transparent)}
.scene{position:relative;border:2px solid var(--line);border-radius:14px;overflow:hidden;min-height:230px;background:%s center bottom/cover no-repeat;color:#1a2a3a}
.scene::before{content:"";position:absolute;inset:0;background:%s repeat-x;background-size:700px 100px;opacity:.9;animation:drift 60s linear infinite;pointer-events:none}
@keyframes drift{to{background-position-x:700px}}
.scene .inner{position:relative;padding:28px 16px 18px;text-align:center}
.scene h1{font-size:44px;color:#fff;text-shadow:0 2px 0 #7a1c1c,0 4px 10px rgba(0,0,0,.35);letter-spacing:.02em}
.scene .sub{display:inline-block;background:rgba(255,253,246,.88);border:2px solid var(--line);border-radius:10px;padding:8px 14px;margin-top:10px;max-width:720px;font-size:13px;color:#2b2418}
.map{background:linear-gradient(180deg,#bfe3ff 0%%,#dff2c8 18%%,#cfe8b0 100%%)}
:root[data-theme="dark"] .map{background:linear-gradient(180deg,#223a55 0%%,#2f4a33 18%%,#2a3f2a 100%%)}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) .map{background:linear-gradient(180deg,#223a55 0%%,#2f4a33 18%%,#2a3f2a 100%%)}}
.map svg{min-width:760px}
.node.open .ring{stroke:var(--accent);stroke-width:3;animation:pulse 1.2s infinite}
.node.open{cursor:pointer}
.pdot{display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%%;color:#fff;font-size:11px;font-weight:700;border:2px solid #fff;box-shadow:0 0 0 1px var(--line);vertical-align:middle}
.ally{border:1px dashed var(--line);border-radius:10px;padding:6px 8px;margin-top:6px;background:color-mix(in srgb,var(--panel2) 60%%,transparent)}
.allies{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:8px}
.lobby .seg button{padding:6px 10px}
.lobby .choices button.primary small{color:#ffe9e7}
.vote{font-size:11px;background:var(--panel2);border:1px solid var(--line);border-radius:999px;padding:0 7px;margin-left:4px}
.news{font-size:12px;background:var(--panel2);border-radius:8px;padding:6px 10px;margin-top:6px}
.news li+li{margin-top:2px}
</style>""" % (BG_ROUTE, BG_FOREST, BG_MOUNT, BG_CAVE, BG_CITY, BG_GYM, BG_TITLE, CLOUD_LAYER))

# ---------- 데이터: 지형·이벤트 ----------
rep("const NODE_ICON={wild:'草',trainer:'!',event:'?',rest:'+',shop:'$',treasure:'★',boss:'◆'};",
"""const NODE_ICON={wild:'草',trainer:'!',event:'?',rest:'+',shop:'$',treasure:'★',boss:'◆'};
const TERRAIN=['route','forest','forest','route','mount','cave','city','gym'];
const TCOL={route:['#a8d978','#8cc45e'],forest:['#5f9a4a','#3f7a35'],mount:['#d8c9a0','#bca779'],cave:['#5a5f6e','#434857'],city:['#d9d4c7','#c3bdae'],gym:['#cfc9bb','#b9b2a3']};
const placeOf=(floor)=>PLACES[clamp(floor-1,0,7)];
/* 이벤트: [제목, 본문, 선택지[[라벨,키]], 봇 선택, 출현 층(선택)] */
const EVENTS={
 forget:{t:'기술 잊기 할아버지',d:'"기술을 잊고 싶은 포켓몬이 있느냐? 잊는 것도 강해지는 길이란다."',c:(r)=>[['카드 1장 제거 (무료)','rm1'],['카드 2장 제거 (앞 포켓몬 HP -7)','rm2'],['지나간다','leave']],bot:'rm1'},
 fisher:{t:'낚시꾼 아저씨',d:'"낡은 낚싯대를 빌려주지. 뭐가 낚일지는 나도 몰라!"',c:(r)=>[['낚시한다 (60% 물 포켓몬 동료, 40% 잉어킹...)','fish'],['거절한다','leave']],bot:'fish'},
 camper:{t:'쉬는 트레이너',d:'모닥불을 쬐던 트레이너가 손짓한다. "같이 쉴래? 아니면... 한판 할래?"',c:(r)=>[['같이 쉰다 (파티 HP 15% 회복)','camp'],['대전을 신청한다 (엘리트: 도구+희귀 카드, 위험)','elite']],bot:'camp'},
 thief:{t:'로켓단 똘마니',d:'"가진 도구를 내놓으면 곱게 보내 주지!"',c:(r)=>[[r.items.length?'도구 1개를 넘긴다':'돈 30원을 넘긴다','give'],['싸운다 (앞 포켓몬 HP -12, 40원 획득)','fight']],bot:'fight'},
 mossrock:{t:'이끼 낀 바위',d:'이끼로 덮인 커다란 바위. 이상한 기운이 느껴진다.',c:(r)=>[[r.party.some(canEvolve)?'바위에 손을 댄다 (진화 가능한 포켓몬 1마리 진화)':'바위를 살펴본다 (원 20)','rock'],['지나간다','leave']],bot:'rock',where:[1,2,3]},
 dojo:{t:'체육관 수련생',d:'"관장님의 제자다! 수련하고 갈래? 좀 아플 텐데."',c:(r)=>[['수련한다 (카드 1장 강화, 앞 포켓몬 HP -8)','train'],['거절한다','leave']],bot:'train'},
 nurse:{t:'출장 간호순이',d:'"포켓몬센터가 멀어서 순회 진료 중이에요. 어떤 치료를 할까요?"',c:(r)=>[['한 마리 완전 회복 (가장 지친 포켓몬)','healone'],['전원 20% 회복','healall']],bot:'healall'},
 berrytree:{t:'열매 나무',d:'가지가 휘도록 열매가 열렸다. 흔들면 더 떨어질 것 같지만, 벌레 포켓몬이 숨어 있을지도.',c:(r)=>[['열매 1개를 딴다','berry1'],['세게 흔든다 (열매 2개, 40%로 야생 벌레 포켓몬과 전투)','shake'],['지나간다','leave']],bot:'berry1',where:[1,2,3,4]},
 moonstone:{t:'달의돌',d:'동굴 바닥에서 희미하게 빛나는 돌. 포켓몬이 이 빛에 반응한다.',c:(r)=>[[r.party.some(m=>SP[m.sp].evo)?'돌을 쓴다 (진화 조건 무시하고 1마리 진화)':'돌을 줍는다 (80원에 팔린다)','moon'],['지나간다','leave']],bot:'moon',where:[5,6]},
 eggman:{t:'알 배달원',d:'"이 알, 대신 좀 맡아 주겠어? 두 번만 더 전투하면 부화할 거야."',c:(r)=>[['알을 맡는다 (전투 2회 후 부화)','egg'],['거절한다','leave']],bot:'egg'},
 karpman:{t:'잉어킹 장수',d:'"이 잉어킹, 단돈 50원! 나중에 분명 크게 될 녀석이라니까!"',c:(r)=>[[r.money>=50?'산다 (50원, 잉어킹 동료)':'돈이 없다...','buykarp'],['거절한다','leave']],bot:'buykarp'},
 gift:{t:'이상한 소포',d:'길가에 떨어진 소포. 수신인이 없다.',c:(r)=>[['열어 본다 (도구 / 돈 / 꽝)','open'],['우체통에 넣는다 (원 10)','post']],bot:'open'},
 stray:{t:'버려진 포켓몬',d:'풀숲에서 지친 포켓몬이 바라본다. 트레이너에게 버려진 듯하다.',c:(r)=>[[r.party.length<3?'데려간다 (HP 30%로 동료)':'기술 카드만 배운다','adopt'],['지나간다','leave']],bot:'adopt',where:[2,3,4]},
 rival:{t:'라이벌 그린',d:'"어이, 아직도 그런 파티냐? 내 포켓몬과 한번 붙어 볼래?"',c:(r)=>[['승부한다 (엘리트 전투, 희귀 카드+도구)','elite'],['무시한다 (그린이 비웃는다)','leave']],bot:'leave',where:[4,5,6]},
 trade:{t:'교환 트레이너',d:'"네 기술 카드 한 장이랑 내 희귀 카드를 바꾸자."',c:(r)=>[['교환한다 (카드 1장 제거 → 같은 포켓몬 희귀 카드)','trade'],['거절한다','leave']],bot:'trade'},
 hotspring:{t:'숨겨진 온천',d:'바위 틈에서 김이 오른다. 포켓몬들이 좋아할 것 같다.',c:(r)=>[['몸을 담근다 (전원 40% 회복, 상태이상 해제)','bath'],['지나간다','leave']],bot:'bath',where:[5,6]}
};""")

rep("const BERRIES={oran:['오랭열매','HP 10 회복',40],sitrus:['자뭉열매','최대 HP의 25% 회복',70],lum:['모과열매','상태이상 모두 해제',50],lansat:['캄라열매','이번 턴 에너지 +1',60]};",
"const BERRIES={oran:['오랭열매','HP 10 회복',40],sitrus:['자뭉열매','최대 HP의 25% 회복',70],lum:['모과열매','상태이상 모두 해제',50],lansat:['캄라열매','이번 턴 에너지 +1',60]};\nconst PCOL=['#d9302b','#2f6fd6','#2e8b57','#b8860b'];\nconst BOT_NAMES=['민수','유리','철수'];")

# ---------- 상태·저장 ----------
rep("let S={screen:'title',mode:'switch',chart:'soft',run:null,ui:{},auto:false,mute:false};",
    "let S={screen:'title',mode:'switch',chart:'soft',run:null,ui:{},auto:false,mute:false,mp:{n:1,mode:'vote',scale:'auto'},multi:null,headless:false,resolving:false};")
rep("function save(){ try{ localStorage.setItem('cobblespire-proto',JSON.stringify({mode:S.mode,chart:S.chart,run:S.run,screen:S.screen})); }catch(e){} }",
"""function save(){ try{ if(S.headless) return; if(S.multi&&S.screen!=='map'&&S.screen!=='title'&&S.screen!=='deck') return;
  const multi=S.multi?Object.assign({},S.multi,{players:S.multi.players.map(p=>Object.assign({},p,{map:null,battle:null,reward:null,event:null,shop:null}))}):null;
  localStorage.setItem('cobblespire-proto',JSON.stringify({mode:S.mode,chart:S.chart,mp:S.mp,run:S.multi?null:S.run,multi,map:S.multi?S.multi.players[0].map:null,screen:S.screen,uid:UID})); }catch(e){} }""")
rep("function load(){ try{ const j=JSON.parse(localStorage.getItem('cobblespire-proto')); if(j&&j.run){ S.mode=j.mode; S.chart=j.chart; S.run=j.run; S.screen=j.screen==='title'?'map':j.screen; UID=(j.run.uidc||1000); return true; } }catch(e){} return false; }",
"""function load(){ try{ const j=JSON.parse(localStorage.getItem('cobblespire-proto')); if(j&&(j.run||j.multi)){ S.mode=j.mode; S.chart=j.chart; if(j.mp) S.mp=j.mp; UID=j.uid||5000;
  if(j.multi){ S.multi=j.multi; for(const p of S.multi.players) p.map=j.map; S.run=S.multi.players[0]; S.screen='map'; }
  else { S.multi=null; S.run=j.run; if(S.run.id==null){ S.run.id=0; S.run.name='나'; S.run.bot=false; } const b=S.run.battle; if(b&&!b.parts){ b.parts=[0]; b.leader=0; b.pl={}; b.curPid=0; } S.screen=j.screen==='title'?'map':j.screen; }
  return true; } }catch(e){} return false; }""")

# ---------- 런 생성 ----------
rep("""function startRun(starterIdx){
  const st=STARTERS[starterIdx]; const mon=newMon(st.sp);
  const deck=st.deck.map(id=>mkCard(id,M[id]?mon.uid:null));
  S.run={party:[mon],active:0,deck,money:120,balls:3,berries:[st.berry],items:[],floor:0,map:genMap(),pos:null,badges:[],won:0,seen:[st.sp],ability:true,hist:[],battle:null,reward:null,event:null,shop:null,uidc:0};
  S.screen='map'; render();
}""",
"""function mkRun(starterIdx,o){ const st=STARTERS[starterIdx]; const mon=newMon(st.sp); const deck=st.deck.map(id=>mkCard(id,M[id]?mon.uid:null));
  return Object.assign({id:0,name:'나',bot:false,dead:false,party:[mon],active:0,deck,money:120,balls:3,berries:[st.berry],items:[],floor:0,map:null,pos:null,badges:[],won:0,seen:[st.sp],ability:true,hist:[],battle:null,reward:null,event:null,shop:null,egg:null,uidc:0},o||{}); }
function startRun(starterIdx){
  const map=genMap(); const me=mkRun(starterIdx,{map}); S.run=me; S.multi=null; S.resolving=false;
  if(S.mp.n>1){ const others=shuffle([0,1,2].filter(i=>i!==starterIdx)); const players=[me];
    for(let i=1;i<S.mp.n;i++) players.push(mkRun(others[(i-1)%others.length],{id:i,name:BOT_NAMES[i-1],bot:true,map}));
    S.multi={mode:S.mp.mode,scale:S.mp.scale==='auto'?S.mp.mode==='vote':S.mp.scale==='on',players,intents:{},news:[],floorNews:[],lastVote:''}; planBots(); }
  S.screen='map'; render();
}""")
rep("function reachable(){ const r=S.run; if(!r.pos) return r.map[0]; const cur=r.map[r.pos.f][r.pos.l]; if(r.pos.f>=7) return []; return r.map[r.pos.f+1].filter(n=>cur.next.includes(n.l)); }",
    "function reachableOf(r){ if(!r.pos) return r.map[0]; const cur=r.map[r.pos.f][r.pos.l]; if(r.pos.f>=7) return []; return r.map[r.pos.f+1].filter(n=>cur.next.includes(n.l)); }\nfunction reachable(){ return reachableOf(S.run); }")

# ---------- 전투 시작 ----------
i0 = s.index("function startBattle(kind,opts){")
i1 = s.index("function log(s){", i0)
s = s[:i0] + """function startBattle(kind,opts){
  opts=opts||{}; const parts=(opts.parts||[S.run]).filter(p=>!p.dead); const n=parts.length; const lead=opts.lead||parts.find(p=>!p.bot)||parts[0]; S.run=lead;
  const r=lead; const fl=r.floor; const modeB=S.mode==='field'; const multiF=modeB||n>=2;
  const bal=BAL[S.mode][kind]; const coop=n>=2&&(kind==='boss'||(S.multi&&S.multi.scale));
  const scale=bal[0]*(coop?(kind==='wild'?1+0.2*(n-1):1+0.45*(n-1)):1), ds=bal[1]*(coop?1+0.1*(n-1):1);
  let enemies=[], queue=[], title='', line='';
  if(kind==='wild'){ const table=opts.table||(fl<=2?WILD_EARLY:fl<=4?WILD_EARLY.concat(WILD_MID):WILD_MID.concat(WILD_LATE)); const big=modeB&&r.party.length>=2; const a=pick(table); enemies=[enemyMon(a,scale*(big?1.15:1),ds)];
    const pairP=modeB?(r.party.length>=3?.6:r.party.length===2?.4:.1):(fl>=4?.3:0); const cnt=n>=2?Math.min(3,n):(chance(pairP)?2:1); while(enemies.length<cnt) enemies.push(enemyMon(pick(table),scale*(big?1.15:1),ds)); title='야생 '+enemies.map(e=>e.ko).join('와 ')+'이(가) 튀어나왔다!'; }
  else if(kind==='trainer'||kind==='elite'){ const t=opts.trainer||pick(TRAINERS); title=t.name+'이(가) 승부를 걸어왔다!'; line=t.line; const ms=t.mons.map(m=>enemyMon(m,scale,ds)); if(multiF) enemies=ms; else { enemies=[ms[0]]; queue=ms.slice(1);} }
  else { title=BOSS.name; line=BOSS.line; const ms=BOSS.mons.map(m=>enemyMon(m,scale,ds)); if(multiF) enemies=ms; else { enemies=[ms[0]]; queue=ms.slice(1);} }
  for(const p of parts){ for(const m of p.party){ m.block=0; m.rk={atk:0,def:0,spd:0}; m.st={}; m.sashUsed=false; } if(!modeB){ if(p.party[p.active].hp<=0) p.active=Math.max(0,p.party.findIndex(m=>m.hp>0)); } }
  const b={kind,title,line,enemies,queue,turn:0,weather:kind==='boss'?{w:'sand',turns:99}:null,log:[],over:false,captured:null,capturedBy:null,parts:parts.map(p=>p.id),pl:{},curPid:null,leader:lead.id,n,fx:[],busy:false,botAct:false,
    hand:[],draw:[],discard:[],exhaust:[],energy:3,pending:[],nextAtk:1,paraNext:0,rechargeNext:0,freeSwitch:true,dmgTaken:0,sel:null};
  for(const p of parts){ const deckCards=p.deck.filter(c=>!(T[c.id]&&T[c.id].modeA&&modeB)); b.pl[p.id]={hand:[],draw:shuffle(deckCards.map(c=>({...c}))),discard:[],exhaust:[],energy:3,pending:[],nextAtk:1,paraNext:0,rechargeNext:0,freeSwitch:true,dmgTaken:0,sel:null}; p.battle=b; }
  swapIn(b,lead.id); log(title); if(line) log('"'+line+'"'); if(kind==='boss') log('모래바람이 몰아친다! (관장의 기믹)');
  if(n>=2) log(parts.map(p=>p.name).join(', ')+'이(가) 함께 싸운다!'+(S.multi&&S.multi.mode==='split'&&kind!=='boss'?' (보상은 '+n+'명이 나눈다)':''));
  for(const e of enemies) setIntent(e);
  for(const p of parts){ swapIn(b,p.id); startTurn(); } swapIn(b,lead.id);
  S.screen='battle'; render();
}
""" + s[i1:]

rep("function fieldMons(){ const r=S.run; return S.mode==='field'?r.party.filter(m=>m.hp>0):(r.party[r.active]&&r.party[r.active].hp>0?[r.party[r.active]]:[]); }",
"""function fieldMonsOf(r){ return S.mode==='field'?r.party.filter(m=>m.hp>0):(r.party[r.active]&&r.party[r.active].hp>0?[r.party[r.active]]:[]); }
function fieldMons(){ return fieldMonsOf(S.run); }
function H(){ return S.multi?S.multi.players[0]:S.run; }
function playerById(id){ return S.multi?(S.multi.players.find(p=>p.id===id)||S.run):S.run; }
function partRuns(b){ return (b&&b.parts?b.parts:[S.run.id]).map(playerById); }
function allField(b){ const out=[]; for(const r of partRuns(b)) out.push(...fieldMonsOf(r)); return out; }
function runOf(m){ const b=S.run&&S.run.battle; if(b&&b.parts&&b.parts.length>1){ for(const r of partRuns(b)) if(r.party.some(x=>x.uid===m.uid)) return r; } return S.run; }
function monByUid(uid){ const b=S.run.battle; for(const r of partRuns(b)){ const m=r.party.find(x=>x.uid===uid); if(m) return m; } return null; }
function ownerName(m){ const r=runOf(m); return r?r.name:''; }
const PFIELDS=['hand','draw','discard','exhaust','energy','pending','nextAtk','paraNext','rechargeNext','freeSwitch','dmgTaken','sel'];
function swapIn(b,pid){ if(b.curPid===pid){ S.run=playerById(pid); return; } if(b.curPid!=null){ const o={}; for(const k of PFIELDS) o[k]=b[k]; b.pl[b.curPid]=o; } const src=b.pl[pid]; if(src) for(const k of PFIELDS) b[k]=src[k]; b.curPid=pid; S.run=playerById(pid); }
function plOf(b,pid){ return b.curPid===pid?b:(b.pl[pid]||b); }""")

rep("const b=S.run.battle, r=S.run; b.turn++; b.energy=3-(b.paraNext?1:0)-(b.rechargeNext?1:0);",
    "const b=S.run.battle, r=S.run; if(S.run.id===b.leader) b.turn++; b.energy=3-(b.paraNext?1:0)-(b.rechargeNext?1:0);")
rep("for(const e of b.enemies){ if(e.st.leech&&e.hp>0){ e.hp=Math.max(0,e.hp-3); const o=r.party.find(m=>m.uid===e.st.leech);",
    "if(S.run.id===b.leader) for(const e of b.enemies){ if(e.st.leech&&e.hp>0){ e.hp=Math.max(0,e.hp-3); const o=monByUid(e.st.leech);")
rep("function dmgMon(m,v,src){ const r=S.run;", "function dmgMon(m,v,src){ const r=runOf(m);")
rep("const d=def(c); if(b.busy) return '상대 턴'; if(ccost(c)>b.energy) return '에너지 부족';",
    "const d=def(c); if(b.busy&&!b.botAct) return '상대 턴'; if(!fieldMons().length) return '싸울 포켓몬이 없다'; if(ccost(c)>b.energy) return '에너지 부족';")
rep("if(d.fx.some(f=>f.k==='CAP')&&(b.kind!=='wild'||r.balls<=0)) return b.kind!=='wild'?'야생 전투에서만':'몬스터볼 없음';",
    "if(d.fx.some(f=>f.k==='CAP')&&(b.kind!=='wild'||r.balls<=0||r.party.length>=3)) return b.kind!=='wild'?'야생 전투에서만':r.balls<=0?'몬스터볼 없음':'파티가 가득 참';")
rep("const c=b.hand[idx]; if(!c||b.busy) return;", "const c=b.hand[idx]; if(!c||(b.busy&&!b.botAct)) return;")
rep("b.captured=e; e.hp=0; e.capturedFlag=true;", "b.captured=e; b.capturedBy=r.id; e.hp=0; e.capturedFlag=true;")
rep("const fm=fieldMons(); e.target=fm.length?", "const fm=allField(S.run.battle); e.target=fm.length?")
rep("let fm=fieldMons(); if(!fm.length) return; let m=fm.find(x=>x.uid===e.target)||pick(fm);",
    "let fm=allField(b); if(!fm.length) return; let m=fm.find(x=>x.uid===e.target)||pick(fm);")
rep("else if(f.s==='para'){ m.st.para=2; b.paraNext=1; }", "else if(f.s==='para'){ m.st.para=2; plOf(b,runOf(m).id).paraNext=1; }")

# ---------- 턴 종료 / 종료 판정 / 보상 ----------
i0 = s.index("const sleep=(ms)=>new Promise(res=>setTimeout(res,ms));")
i1 = s.index("function joinMon(spid){", i0)
s = s[:i0] + """const sleep=(ms)=>S.headless?Promise.resolve():new Promise(res=>setTimeout(res,ms));
function discardHand(b){ b.hand=b.hand.filter(c=>{ if(def(c).fx.some(f=>f.k==='RET')) return true; b.discard.push(c); return false; }); b.dmgTaken=0; }
async function endTurn(){
  const b=S.run.battle; if(b.over||b.busy) return; const leadId=b.curPid; b.sel=null; b.busy=true;
  discardHand(b); SFX.play('end'); render(); await sleep(S.auto?300:450);
  // 동료(봇) 턴: 리더가 아닌 참가자
  for(const pid of b.parts){ if(pid===leadId) continue; const p=playerById(pid); if(!p.bot||p.dead) continue; swapIn(b,pid);
    if(fieldMons().length){ log('— '+p.name+'의 턴 —'); await botTurn(b); if(b.over){ b.busy=false; render(); return; } } discardHand(b); }
  swapIn(b,leadId);
  for(const e of b.enemies){ e.block=0; enemyAct(e); render(); if(checkEnd()) { b.busy=false; render(); return; } await sleep(S.auto?450:700); }
  b.busy=false;
  for(const e of b.enemies){ if(e.hp>0) setIntent(e); }
  if(b.weather&&b.weather.turns<90){ b.weather.turns--; if(b.weather.turns<=0){ b.weather=null; log('날씨가 원래대로 돌아왔다'); } }
  for(const pid of b.parts){ swapIn(b,pid); const r=S.run;
    if(S.mode==='switch'&&r.party[r.active].hp<=0){ const i=r.party.findIndex(m=>m.hp>0); if(i>=0){ r.active=i; log('가라, '+r.party[i].ko+'!'); } }
    startTurn(); if(b.over){ b.busy=false; render(); return; } }
  swapIn(b,leadId); render();
}
function checkEnd(){
  const b=S.run.battle; if(b.over) return true;
  if(!partRuns(b).some(r=>r.party.some(m=>m.hp>0))){ b.over='lose'; log('눈앞이 캄캄해졌다...'); S.run=playerById(b.leader); S.screen='gameover'; SFX.play('lose'); return true; }
  if(b.enemies.every(e=>e.hp<=0)){ if(b.queue.length&&!b.captured){ const n=b.queue.shift(); b.enemies=[n]; setIntent(n); log('상대가 '+n.ko+'을(를) 내보냈다!'); return false; } b.over='win'; SFX.play('win'); finishBattle(); return true; }
  return false;
}
function finishBattle(){
  const b=S.run.battle; const parts=partRuns(b); const n=parts.length; const together=n>=2; const split=together&&S.multi&&S.multi.mode==='split'&&b.kind!=='boss'; const share=split?n:1;
  const capCands=parts.filter(p=>p.balls>0&&p.party.length<3); const capTo=together?(capCands.length?pick(capCands):null):parts[0];
  const itemTo=together?pick(parts):parts[0]; const berryTo=together?pick(parts):parts[0];
  const capturedBy=b.captured?playerById(b.capturedBy!=null?b.capturedBy:b.leader):null;
  for(const r of parts){ S.run=r; r.won++;
    for(const m of r.party){ m.block=0; m.rk={atk:0,def:0,spd:0}; m.st={}; if(m.hp<=0) m.hp=Math.max(1,Math.round(m.maxHp*0.2)); }
    const extra=r.items.includes('expshare')?10:0;
    const rw={kind:b.kind,money:0,cards:[],berry:null,item:null,capture:null,badge:null,evo:false,captured:(capturedBy===r&&b.captured)?b.captured.sp:null,took:{},share,mates:together?parts.filter(p=>p!==r).map(p=>p.name):[]};
    if(b.kind==='wild'){ rw.money=Math.round((15+R(11))/share)+extra; if(berryTo===r&&chance(.25)) rw.berry=pick(Object.keys(BERRIES)); if(!b.captured&&capTo===r){ const last=b.enemies[b.enemies.length-1]; rw.capture={sp:last.sp,p:clamp(0.15+0.75*(SP[last.sp].catchR/255),0.05,0.95)}; } }
    else if(b.kind==='trainer'){ rw.money=Math.round((30+R(16))/share)+extra; if(itemTo===r) rw.item=pick(Object.keys(ITEMS).filter(i=>!r.items.includes(i))); }
    else if(b.kind==='elite'){ rw.money=Math.round((45+R(16))/share)+extra; if(itemTo===r) rw.item=pick(Object.keys(ITEMS).filter(i=>!r.items.includes(i))); }
    else { rw.money=80+extra; rw.badge=BOSS.badge; rw.items3=shuffle(Object.keys(ITEMS).filter(i=>!r.items.includes(i))).slice(0,3); rw.evo=true; }
    if(capturedBy===r){ if(r.party.length<3) r.party.push(joinMon(b.captured.sp)); else { r.deck.push(mkCard(pick(SP[b.captured.sp].moves.filter(id=>M[id])),null)); rw.captured=null; rw.capMsg=SP[b.captured.sp].ko+'을(를) 잡았지만 파티가 가득 차 기술 카드 1장만 받았다.'; } }
    else rw.cards=rewardCards(split?2:3);
    if(r.egg&&b.kind!=='boss'){ r.egg.left--; if(r.egg.left<=0){ const sp=pick(WILD_EARLY.concat(['pikachu'])); r.egg=null; if(r.party.length<3){ r.party.push(joinMon(sp)); rw.hatch=sp+' 부화! '+SP[sp].ko+'이(가) 파티에 들어왔다.'; } else { r.deck.push(mkCard(pick(SP[sp].moves.filter(id=>M[id])),null)); rw.hatch='알에서 '+SP[sp].ko+'이(가) 태어났지만 파티가 가득 차 기술 카드만 받았다.'; } } }
    if(r.bot) botTakeReward(r,rw); else r.reward=rw;
  }
  const lead=playerById(b.leader); S.run=lead; S.screen=lead.bot?'map':'reward';
}
""" + s[i1:]

# ---------- 노드 진입 ----------
rep("""function enterNode(n){ const r=S.run; r.pos={f:n.f,l:n.l}; r.floor=n.f+1; n.done=true; r.hist.push(n.t);
  if(n.t==='wild') startBattle('wild');""",
"""function visit(r,n){ r.pos={f:n.f,l:n.l}; r.floor=n.f+1; n.done=true; r.hist.push(n.t); }
function enterNode(n){ visit(S.run,n); openNode(n); }
function openNode(n){ const r=S.run;
  if(n.t==='wild') startBattle('wild');""")
rep("function genEvent(){ const r=S.run; const list=['forget','fisher','camper','thief','mossrock','dojo']; const used=r.hist.filter(h=>h.startsWith('ev:')).map(h=>h.slice(3)); const c=list.filter(e=>!used.includes(e)); const id=pick(c.length?c:list); r.hist.push('ev:'+id); return {id,done:false,text:''}; }",
    "function genEvent(){ const r=S.run; const list=Object.keys(EVENTS).filter(k=>!EVENTS[k].where||EVENTS[k].where.includes(r.floor)); const used=r.hist.filter(h=>h.startsWith('ev:')).map(h=>h.slice(3)); const c=list.filter(e=>!used.includes(e)); const id=pick(c.length?c:list); r.hist.push('ev:'+id); return {id,done:false,text:''}; }")

# ---------- 렌더 ----------
rep("function render(){ save(); let h=''; if(S.run&&S.screen!=='title') h+=topBar();",
    "function render(){ if(S.headless) return; save(); const keepRun=S.run; if(S.multi&&S.run!==H()&&S.screen!=='title') S.run=H(); let h=''; if(S.run&&S.screen!=='title') h+=topBar();")
rep("app.innerHTML=h; playFx(); scheduleAuto(); }", "app.innerHTML=h; S.run=keepRun; playFx(); scheduleAuto(); }")
rep("function topBar(){ const r=S.run; return '<div class=\"bar\"><span class=\"brand\">CobbleSpire</span><span class=\"pill mode\">'+(S.mode==='switch'?'교체형 (3마리·교체)':'동시형 (3마리 동시)')+'</span>'+",
    "function topBar(){ const r=H(); return '<div class=\"bar\"><span class=\"brand\">CobbleSpire</span><span class=\"pill mode\">'+(S.mode==='switch'?'교체형 (3마리·교체)':'동시형 (3마리 동시)')+'</span>'+(S.multi?'<span class=\"pill mode\" style=\"background:var(--good)\">'+(S.multi.mode==='vote'?'투표형':'분산형')+' '+S.multi.players.length+'인</span>':'')+")
rep("'<span><span class=\"k\">층</span>'+r.floor+'/8</span>", "'<span><span class=\"k\">위치</span>'+(r.pos?PLACES[r.pos.f]:'관동 입구')+' <span class=\"muted tiny\">('+r.floor+'/8)</span></span>")

# 제목 화면
rep("function scrTitle(){ const has=(()=>{try{return !!JSON.parse(localStorage.getItem('cobblespire-proto')||'null')?.run}catch(e){return false}})();\n return '<div class=\"panel center\" style=\"padding:28px 16px\"><h1>CobbleSpire 체험판</h1><p class=\"muted\">",
    "function scrTitle(){ const has=(()=>{try{const j=JSON.parse(localStorage.getItem('cobblespire-proto')||'null'); return !!(j&&(j.run||j.multi));}catch(e){return false}})();\n return '<div class=\"scene\"><div class=\"inner\"><h1>CobbleSpire</h1><div class=\"sub\">코블버스 위의 슬레이 더 스파이어식 로그라이크 덱빌딩 · 웹 체험판 v0.3</div></div></div><div class=\"panel center\" style=\"padding:20px 16px\"><p class=\"muted\">")
rep("<li>야생 승리 후 몬스터볼로 포획 → 파티 최대 3마리.</li></ul></div></div>'+\n '<div class=\"row\" style=\"justify-content:center\"><button class=\"primary\" data-act=\"newrun\"",
    """<li>야생 승리 후 몬스터볼로 포획 → 파티 최대 3마리.</li></ul></div></div>'+
 '<div class="panel lobby" style="text-align:left;max-width:740px;margin:0 auto 14px"><h3>함께 하기 (멀티플레이 상정)</h3><p class="tiny muted">실제 모드에서는 서버의 다른 플레이어가 들어오는 자리입니다. 체험판에서는 봇 동료가 각자 파티·덱·돈을 가지고 같은 지도를 진행합니다.</p>'+
 '<div class="row" style="align-items:center"><span class="tiny">인원</span><div class="seg">'+[1,2,3,4].map(n=>'<button data-act="mpn" data-arg="'+n+'" class="'+(S.mp.n===n?'on':'')+'">'+(n===1?'혼자':n+'명')+'</button>').join('')+'</div>'+(S.mp.n>1?'<span class="tiny">적 강도</span><div class="seg"><button data-act="mpscale" data-arg="auto" class="'+(S.mp.scale==='auto'?'on':'')+'">자동</button><button data-act="mpscale" data-arg="on" class="'+(S.mp.scale==='on'?'on':'')+'">인원 비례</button><button data-act="mpscale" data-arg="off" class="'+(S.mp.scale==='off'?'on':'')+'">고정</button></div>':'')+'</div>'+
 (S.mp.n>1?'<div class="choices" style="margin-top:10px"><button data-act="mpmode" data-arg="vote" class="'+(S.mp.mode==='vote'?'primary':'')+'">투표형 — 한 팀으로 이동<small>슬레이 더 스파이어 2 협동처럼 모두 같은 길을 간다. 노드마다 투표해 다수결로 이동하고 전투는 항상 함께. 적은 인원에 맞춰 강해지고(자동) 보상은 각자 전부 받는다.</small></button>'+
 '<button data-act="mpmode" data-arg="split" class="'+(S.mp.mode==='split'?'primary':'')+'">분산형 — 따로 또 같이<small>각자 길을 고른다. 같은 노드를 고르면 함께 싸워 쉽지만 돈·카드 선택지를 나눠 갖고, 혼자 가면 보상을 독차지하되 위험하다. 적 강도는 고정(자동). 체육관은 전원이 합류해 관장을 함께 상대한다.</small></button></div>':'')+'</div>'+
 '<div class="row" style="justify-content:center"><button class="primary" data-act="newrun\"""")

# 지도
i0 = s.index("function scrMap(){")
i1 = s.index("function stTags(m){", i0)
s = s[:i0] + r"""function hsh(a,b){ let x=(a*374761393+b*668265263)|0; x=(x^(x>>>13))*1274126177|0; return ((x^(x>>>16))>>>0)/4294967296; }
function mapDeco(f,colW,H){ const t=TERRAIN[f]; let o=''; const x0=colW*f; for(let i=0;i<10;i++){ const x=(x0+8+hsh(f+1,i)*(colW-16)).toFixed(1), y=(14+hsh(i+3,f+7)*(H-60)).toFixed(1); const X=+x,Y=+y;
  if(t==='route') o+='<path d="M'+(X-4)+' '+(Y+6)+' l3 -9 l3 9 M'+(X+2)+' '+(Y+6)+' l2 -11 l2 11" stroke="#4f9a3a" stroke-width="1.8" fill="none" stroke-linecap="round"/>';
  else if(t==='forest') o+='<path d="M'+(X-8)+' '+(Y+7)+' L'+X+' '+(Y-9)+' L'+(X+8)+' '+(Y+7)+'Z" fill="#2f6b2a"/><rect x="'+(X-1.5)+'" y="'+(Y+6)+'" width="3" height="5" fill="#5a3a1a"/>';
  else if(t==='mount') o+='<path d="M'+(X-10)+' '+(Y+8)+' L'+X+' '+(Y-9)+' L'+(X+10)+' '+(Y+8)+'Z" fill="#9c8a62"/><path d="M'+(X-3.5)+' '+(Y-3)+' L'+X+' '+(Y-9)+' L'+(X+3.5)+' '+(Y-3)+'Z" fill="#f4f1e8"/>';
  else if(t==='cave') o+='<ellipse cx="'+X+'" cy="'+Y+'" rx="7" ry="4.5" fill="#2f333d"/><ellipse cx="'+(X-2)+'" cy="'+(Y-1)+'" rx="2.5" ry="1.5" fill="#6b7180"/>';
  else o+='<rect x="'+(X-6)+'" y="'+(Y-3)+'" width="12" height="10" fill="#8f8a7f"/><rect x="'+(X-7)+'" y="'+(Y-6)+'" width="14" height="4" fill="'+(t==='gym'?'#7a1c1c':'#6d6860')+'"/><rect x="'+(X-2)+'" y="'+(Y)+'" width="3" height="3" fill="#fff2c0"/>'; }
  return o; }
const MAP_DEFS='<defs>'+
 '<symbol id="n-wild" viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="#dff3c4"/><path d="M12 30 l4 -14 l4 14 M18 30 l2 -16 l2 16 M24 30 l4 -12 l-2 12" stroke="#3f8f2a" stroke-width="3" fill="none" stroke-linecap="round"/></symbol>'+
 '<symbol id="n-trainer" viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="#ffe3b3"/><circle cx="18" cy="15" r="6" fill="#f3d2b0"/><path d="M12 15 a6 6 0 0 1 12 0z" fill="#e07b00"/><path d="M8 33 q10 -16 20 0z" fill="#e07b00"/><text x="29" y="15" font-size="14" font-family="Jua,sans-serif" fill="#c0392b" font-weight="700">!</text></symbol>'+
 '<symbol id="n-event" viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="#e9dcff"/><rect x="18" y="19" width="4" height="13" fill="#7a5230"/><rect x="9" y="9" width="22" height="12" rx="2" fill="#a97b4f"/><text x="20" y="19" text-anchor="middle" font-size="11" font-family="Jua,sans-serif" fill="#fff">?</text></symbol>'+
 '<symbol id="n-rest" viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="#ffd6dc"/><rect x="10" y="18" width="20" height="14" fill="#fff"/><path d="M8 19 L20 8 L32 19Z" fill="#e05a6d"/><rect x="17" y="24" width="6" height="8" fill="#e05a6d"/><path d="M12 21 h4 M14 19 v4" stroke="#e05a6d" stroke-width="1.5"/></symbol>'+
 '<symbol id="n-shop" viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="#cfe6ff"/><rect x="10" y="18" width="20" height="14" fill="#fff"/><path d="M8 19 L20 8 L32 19Z" fill="#2f8fc9"/><text x="20" y="30" text-anchor="middle" font-size="11" font-family="Jua,sans-serif" fill="#2f8fc9">$</text></symbol>'+
 '<symbol id="n-treasure" viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="#fff0bf"/><rect x="9" y="17" width="22" height="13" rx="2" fill="#8b5a2b"/><rect x="9" y="12" width="22" height="7" rx="3" fill="#a9713a"/><rect x="18" y="17" width="4" height="6" fill="#d4a017"/></symbol>'+
 '<symbol id="n-boss" viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="#f1d3d3"/><rect x="8" y="16" width="24" height="16" fill="#e8e4dc"/><path d="M6 17 L20 7 L34 17Z" fill="#7a1c1c"/><rect x="11" y="20" width="3" height="12" fill="#b9b2a3"/><rect x="26" y="20" width="3" height="12" fill="#b9b2a3"/><rect x="17" y="24" width="6" height="8" fill="#7a1c1c"/></symbol>'+
 '</defs>';
function marker(x,y,p,ghost){ const c=p.dead?'#777':PCOL[p.id%4]; return '<g opacity="'+(ghost?.6:1)+'"><circle cx="'+x+'" cy="'+(y-6)+'" r="5" fill="#f3d2b0"/><path d="M'+(x-5)+' '+(y-6)+' a5 5 0 0 1 10 0z" fill="'+c+'"/><path d="M'+(x-7)+' '+(y+9)+' q7 -14 14 0z" fill="'+c+'"'+(ghost?' stroke="#fff" stroke-dasharray="2 1.5"':'')+'/>'+(p.dead?'<text x="'+(x+4)+'" y="'+(y-8)+'" font-size="11" fill="#c0392b">×</text>':'')+'</g>'; }
function scrMap(){ const r=H(); const mu=S.multi; const reach=reachableOf(r); const W=760, HH=340, colW=W/8;
 let svg='<svg viewBox="0 0 '+W+' '+HH+'" width="'+W+'" height="'+HH+'" role="img" aria-label="관동지방 루트 지도">'+MAP_DEFS;
 for(let f=0;f<8;f++){ const t=TERRAIN[f]; const c=TCOL[t]; svg+='<rect x="'+(colW*f)+'" y="0" width="'+colW+'" height="'+HH+'" fill="'+c[0]+'"/><rect x="'+(colW*f)+'" y="0" width="'+colW+'" height="'+HH+'" fill="url(#none)" opacity="0"/>'+mapDeco(f,colW,HH-26); }
 svg+='<rect x="0" y="'+(HH-26)+'" width="'+W+'" height="26" fill="rgba(43,36,24,.75)"/>';
 const pos=(n)=>({x:colW*n.f+colW/2,y:r.map[n.f].length===1?(HH-26)/2:62+n.l*98});
 for(const row of r.map) for(const n of row) for(const l of n.next){ const a=pos(n), b=pos(r.map[n.f+1][l]); const d='M'+a.x+' '+a.y+' C'+(a.x+40)+' '+a.y+' '+(b.x-40)+' '+b.y+' '+b.x+' '+b.y; svg+='<path d="'+d+'" stroke="#b58f55" stroke-width="7" fill="none" stroke-linecap="round"/><path d="'+d+'" stroke="#e8d7a8" stroke-width="2" fill="none" stroke-dasharray="6 7" stroke-linecap="round"/>'; }
 for(const row of r.map) for(const n of row){ const p=pos(n); const open=reach.includes(n); const cls='node '+(n.done?'done':open?'open':'off');
   svg+='<g class="'+cls+'" '+(open?'data-act="node" data-arg="'+n.f+','+n.l+'"':'')+'><circle class="ring" cx="'+p.x+'" cy="'+p.y+'" r="22" fill="rgba(255,255,255,.45)" stroke="var(--line)" stroke-width="2"/><use href="#n-'+n.t+'" x="'+(p.x-19)+'" y="'+(p.y-19)+'" width="38" height="38"/>'+(r.pos&&r.pos.f===n.f&&r.pos.l===n.l&&!mu?'<circle cx="'+p.x+'" cy="'+p.y+'" r="27" fill="none" stroke="var(--fg)" stroke-width="2" stroke-dasharray="4 3"/>':'')+'</g>'; }
 if(mu){ const off=[[-18,-26],[18,-26],[-18,28],[18,28]]; for(const p of mu.players){ const o=off[p.id%4]; const q=p.pos?pos(r.map[p.pos.f][p.pos.l]):{x:colW/2-30,y:(HH-26)/2}; svg+=marker(q.x+o[0],q.y+o[1],p,false);
     const it=mu.intents[p.id]; if(it&&!p.dead&&p.bot){ const [f,l]=it.split(',').map(Number); const q2=pos(r.map[f][l]); svg+=marker(q2.x+o[0],q2.y+o[1],p,true); } } }
 else if(!r.pos){ svg+=marker(colW/2-30,(HH-26)/2,r,false); }
 for(let f=0;f<8;f++) svg+='<text x="'+(colW*f+colW/2)+'" y="'+(HH-8)+'" text-anchor="middle" font-size="12" font-family="Jua,sans-serif" fill="'+(r.pos&&r.pos.f===f?'#ffd36b':'#fff')+'">'+PLACES[f]+'</text>';
 svg+='</svg>';
 const alive=mu?mu.players.filter(p=>!p.dead):[]; const key=(n)=>n.f+','+n.l;
 const goingTo=(n)=>alive.filter(p=>p.bot&&mu.intents[p.id]===key(n));
 let h='<div class="map">'+svg+'</div><div class="row"><div class="panel grow"><h3>'+(r.pos?PLACES[r.pos.f]+'에서 다음 길을 고른다':'관동지방 모험의 시작. 어느 길로 갈까?')+'</h3>';
 if(mu) h+='<p class="tiny muted" style="margin:4px 0">'+(mu.mode==='vote'?'투표형: 내 표와 동료의 표를 합쳐 다수결로 이동한다 (동률은 무작위).':'분산형: 같은 길을 고른 동료와 함께 싸운다. 혼자 가면 보상을 독차지하지만 위험하다.')+'</p>';
 h+='<div class="choices" style="margin-top:8px">'+reach.map(n=>{ const g=goingTo(n); let tag=''; if(mu){ if(mu.mode==='vote') tag=g.length?'<span class="vote">'+g.map(p=>p.name).join('·')+' '+g.length+'표</span>':''; else tag=g.length?'<span class="vote">'+g.map(p=>p.name).join('·')+'와 함께 · 보상 1/'+(g.length+1)+'</span>':'<span class="vote">혼자 · 보상 전부</span>'; }
   return '<button data-act="node" data-arg="'+n.f+','+n.l+'">'+NODE_TXT[n.t][0]+' <span class="pill">'+PLACES[n.f]+'</span>'+tag+'<small>'+NODE_TXT[n.t][1]+'</small></button>'; }).join('')+'</div></div>';
 h+='<div class="panel" style="flex:1 1 260px"><h3>파티</h3>'+r.party.map((m,i)=>monCard(m,{small:true,active:S.mode==='switch'&&i===r.active})).join('')+(r.egg?'<div class="tiny">🥚 알: 전투 '+r.egg.left+'회 후 부화</div>':'')+'<div class="tiny muted" style="margin-top:6px">풀숲 야생 · 트레이너 · 표지판 이벤트 · 빨간 지붕 포켓몬센터 · 파란 지붕 상점 · 상자 보물 · 체육관</div>'+(r.berries.length?'<div style="margin-top:8px">'+r.berries.map((b,i)=>'<button class="tiny" data-act="berry" data-arg="'+i+'">'+BERRIES[b][0]+' 사용</button>').join(' ')+'</div>':'')+'</div>';
 if(mu){ h+='<div class="panel" style="flex:1 1 260px"><h3>동료</h3>'+mu.players.filter(p=>p.bot).map(p=>'<div class="ally"><div class="row" style="align-items:center;gap:6px"><span class="pdot" style="background:'+PCOL[p.id%4]+'">'+p.name[0]+'</span><b>'+p.name+'</b>'+(p.dead?'<span class="st bad">쓰러짐</span>':'')+'<span class="tiny muted">'+p.money+'원 · 덱 '+p.deck.length+'장 · 볼 '+p.balls+(p.items.length?' · '+p.items.map(i=>ITEMS[i][0]).join(', '):'')+'</span></div>'+(p.dead?'':'<div class="row" style="gap:4px">'+p.party.map(m=>monCard(m,{small:true})).join('')+'</div>')+(!p.dead&&mu.intents[p.id]?'<div class="tiny muted">다음: '+(()=>{const [f,l]=mu.intents[p.id].split(',').map(Number); const n=r.map[f][l]; return NODE_TXT[n.t][0]+' ('+PLACES[f]+')';})()+'</div>':'')+'</div>').join('')+
   (mu.news.length?'<div class="news"><b>동료 소식</b><ul style="padding-left:16px;margin:2px 0">'+mu.news.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul></div>':'')+(mu.lastVote?'<div class="tiny muted" style="margin-top:4px">지난 투표: '+esc(mu.lastVote)+'</div>':'')+'</div>'; }
 return h+'</div>'; }
""" + s[i1:]

rep("const fm=fieldMons(); const tg=fm.find(x=>x.uid===e.target)||fm[0];", "const fm=allField(b); const tg=fm.find(x=>x.uid===e.target)||fm[0];")
rep("(tg&&fm.length>1?' → '+tg.ko:'')", "(tg&&fm.length>1?' → '+(S.multi?ownerName(tg)+'의 ':'')+tg.ko:'')")

# 전투 화면
i0 = s.index("function scrBattle(){")
i1 = s.index("function scrReward(){", i0)
s = s[:i0] + """function scrBattle(){ const r=H(), b=r.battle; const modeB=S.mode==='field'; const pl=plOf(b,r.id); const sel=b.curPid===r.id?b.sel:null; const mine=b.curPid===r.id;
 const targetable=sel&&sel.kind==='enemy'; const allyPick=sel&&sel.kind==='ally'; const swPick=sel&&sel.kind==='switch'; const others=partRuns(b).filter(p=>p!==r);
 let h='<div class="panel"><div class="row" style="justify-content:space-between;align-items:center"><h2>'+(b.kind==='boss'?'관장전: '+BOSS.name:b.kind==='wild'?'야생 포켓몬':b.kind==='elite'?'엘리트 트레이너':'트레이너 대전')+' <span class="pill">'+b.turn+'턴</span>'+(b.weather?' <span class="pill">'+{sun:'쾌청',rain:'비',sand:'모래바람'}[b.weather.w]+(b.weather.turns<90?' '+b.weather.turns:'')+'</span>':'')+(others.length?' <span class="pill" style="background:var(--good);color:#fff;border-color:transparent">'+(others.length+1)+'인 협동'+(S.multi&&S.multi.mode==='split'&&b.kind!=='boss'?' · 보상 1/'+(others.length+1):'')+'</span>':'')+'</h2>'+(b.queue.length?'<span class="tiny muted">대기 중: '+b.queue.map(q=>q.ko).join(', ')+'</span>':'')+'</div>';
 h+='<div class="arena bg-'+TERRAIN[r.pos?r.pos.f:0]+' '+(b.weather?b.weather.w:'')+'" style="margin-top:8px"><div class="field '+(b.enemies.length>1?'three':'')+'">'+b.enemies.map(e=>enemyCard(e,b,targetable&&e.hp>0)).join('')+'</div>';
 if(sel) h+='<div class="panel center" style="border-color:var(--accent)">'+(targetable?'<b>'+esc(cname(sel.card))+'</b>: 공격할 상대를 고르세요':allyPick?'<b>'+esc(cname(sel.card))+'</b>: 적용할 포켓몬을 고르세요':'교체할 포켓몬을 고르세요')+' <button data-act="cancel" class="tiny">취소</button></div>';
 if(modeB){ h+='<div class="field three" style="margin-top:10px">'+r.party.map((m,i)=>monCard(m,{back:true,big:true,target:allyPick&&m.hp>0,attr:allyPick&&m.hp>0?'data-act="ally" data-arg="'+i+'"':''})).join('')+'</div>'; }
 else { const a=r.party[r.active]; h+='<div class="row" style="margin-top:10px"><div class="grow">'+monCard(a,{active:true,back:true,big:true})+'</div><div style="flex:1 1 200px;min-width:0"><div class="tiny muted" style="margin-bottom:4px">벤치 '+(pl.freeSwitch&&!swPick?'(무료 교체 1회 남음: 클릭)':swPick?'(교체 카드: 클릭)':'(이번 턴 무료 교체 사용함)')+'</div>'+r.party.map((m,i)=>i===r.active?'':monCard(m,{small:true,bench:m.hp>0&&(pl.freeSwitch||swPick),attr:m.hp>0&&(pl.freeSwitch||swPick)?'data-act="bench" data-arg="'+i+'"':''})).join('')+(r.party.length<2?'<div class="tiny muted">벤치가 비어 있다. 야생 포켓몬을 잡아 보자.</div>':'')+'</div></div>'; }
 if(others.length) h+='<div class="allies" style="margin-top:8px">'+others.map(p=>'<div class="ally"><div class="tiny"><span class="pdot" style="background:'+PCOL[p.id%4]+'">'+p.name[0]+'</span> <b>'+p.name+'</b>'+(b.busy&&b.curPid===p.id?' <span class="busyb">행동 중...</span>':'')+' <span class="muted">에너지 '+plOf(b,p.id).energy+' · 손패 '+plOf(b,p.id).hand.length+'</span></div><div class="row" style="gap:4px">'+p.party.map((m,i)=>monCard(m,{small:true,back:true,active:S.mode==='switch'&&i===p.active})).join('')+'</div></div>').join('')+'</div>';
 h+='</div></div>';
 h+='<div class="panel"><div class="row" style="align-items:center;justify-content:space-between"><div class="energy"><b>'+pl.energy+'</b>/3 <span class="tiny muted">에너지</span>'+(b.busy?' <span class="busyb">'+(b.curPid!==r.id&&b.botAct?playerById(b.curPid).name+'의 턴...':'상대 턴...')+'</span>':'')+'</div><div class="tiny muted">덱 '+pl.draw.length+' · 버림 '+pl.discard.length+' · 소멸 '+pl.exhaust.length+'</div><div>'+r.berries.map((x,i)=>'<button class="tiny" data-act="berry" data-arg="'+i+'">'+BERRIES[x][0]+'</button>').join(' ')+' <button class="primary" data-act="end" '+(b.busy||!mine?'disabled':'')+'>턴 종료</button></div></div>';
 h+='<div class="hand">'+pl.hand.map((c,i)=>cardHtml(c,i,{sel:sel&&sel.idx===i})).join('')+(pl.hand.length?'':'<div class="muted tiny" style="padding:20px">손패가 없다</div>')+'</div>';
 h+='<div class="log">'+b.log.slice(-10).map(esc).map(x=>'<div>'+x+'</div>').join('')+'</div></div>';
 return h; }
""" + s[i1:]

rep("if(rw.captured) h+='<p><b>'+SP[rw.captured].ko+'</b>을(를) 잡아서 파티에 들어왔다. 그 포켓몬의 기술 카드 3장이 덱에 추가되었다.</p>';",
    "if(rw.captured) h+='<p><b>'+SP[rw.captured].ko+'</b>을(를) 잡아서 파티에 들어왔다. 그 포켓몬의 기술 카드 3장이 덱에 추가되었다.</p>'; if(rw.mates&&rw.mates.length) h+='<p class=\"tiny muted\">'+rw.mates.join(', ')+'와(과) 함께 싸웠다'+(rw.share>1?' — 돈은 1/'+rw.share+', 카드 선택지는 2장':'')+'.</p>'; if(rw.hatch) h+='<p>🥚 '+esc(rw.hatch)+'</p>';")
rep("if(rw.cards.length&&!rw.took.cards) h+='<h3 style=\"margin-top:10px\">기술 카드 3택1</h3>", "if(rw.cards.length&&!rw.took.cards) h+='<h3 style=\"margin-top:10px\">기술 카드 '+rw.cards.length+'택1</h3>")

# 이벤트 화면: EVENTS 데이터 사용
i0 = s.index("function scrEvent(){")
i1 = s.index("function cardPickList(", i0)
s = s[:i0] + """function scrEvent(){ const r=S.run, ev=r.event; let h='<div class="panel">'; const e=EVENTS[ev.id];
 h+='<h2>'+e.t+'</h2><p>'+e.d+'</p>'; if(ev.done){ h+='<p class="tiny">'+esc(ev.text)+'</p>'; if(ev.pickCard) h+=cardPickList(ev.pickCard.cards,'evpick',ev.pickCard.title); if(ev.upCard) h+=cardPickList(ev.upCard.cards,'evup','강화할 카드를 고르세요'); if(!ev.pickCard&&!ev.upCard) h+='<button class="primary" data-act="tomap">지도로</button>'; }
 else h+='<div class="choices" style="max-width:520px">'+e.c(r).map(c=>'<button data-act="ev" data-arg="'+c[1]+'">'+c[0]+'</button>').join('')+'</div>';
 return h+'</div>'; }
""" + s[i1:]

rep("function scrOver(){ const r=S.run; return '<div class=\"panel center\"><h1>눈앞이 캄캄해졌다...</h1><p>'+r.floor+'층 '+PLACES[Math.max(0,r.floor-1)]+'에서 쓰러졌다.",
    "function scrOver(){ const r=H(); return '<div class=\"panel center\"><h1>눈앞이 캄캄해졌다...</h1>'+(S.multi?'<p class=\"tiny muted\">'+S.multi.players.filter(p=>p.bot).map(p=>p.name+(p.dead?' (쓰러짐)':' ('+placeOf(p.floor)+', 파티 '+p.party.map(m=>m.ko).join('·')+')')).join(' · ')+'</p>':'')+'<p>'+PLACES[Math.max(0,r.floor-1)]+'에서 쓰러졌다.")
rep("function scrWin(){ const r=S.run; return '<div class=\"panel center\"><h1>회색배지 획득!</h1><p>1막 클리어. 파티: '+r.party.map(m=>m.ko).join(', ')+' · 덱 '+r.deck.length+'장 · 도구 '+(r.items.map(i=>ITEMS[i][0]).join(', ')||'없음')+'</p>",
    "function scrWin(){ const r=H(); return '<div class=\"panel center\"><h1>회색배지 획득!</h1><p>1막 클리어. 파티: '+r.party.map(m=>m.ko).join(', ')+' · 덱 '+r.deck.length+'장 · 도구 '+(r.items.map(i=>ITEMS[i][0]).join(', ')||'없음')+'</p>'+(S.multi?'<p class=\"tiny\">함께한 동료: '+S.multi.players.filter(p=>p.bot).map(p=>p.name+(p.dead?' (도중 쓰러짐)':' — '+p.party.map(m=>m.ko).join('·'))).join(' · ')+'</p>':'')+'")

rep("  play(k){ try{ switch(k){", "  play(k){ if(S.headless) return; try{ switch(k){")
rep("function autoTick(){ if(!S.auto||!S.run) return; const r=S.run, scr=S.screen; try{\n  if(scr==='map'){ const re=reachable(); if(re.length) enterNode(pick(re)); return; }",
    "function autoTick(){ if(!S.auto||!S.run||S.headless||S.resolving) return; const r=S.run, scr=S.screen; try{\n  if(scr==='map'){ const re=reachable(); if(re.length) chooseNode(pick(re)); return; }")
rep("if(scr==='event'){ const ev=r.event; if(!ev.done){ doEvent({forget:'rm1',fisher:'fish',camper:'camp',thief:'fight',mossrock:'rock',dojo:'train'}[ev.id]); return; }",
    "if(scr==='event'){ const ev=r.event; if(!ev.done){ doEvent(EVENTS[ev.id].bot); return; }")

# 입력
rep("app.addEventListener('click',(ev)=>{ const el=ev.target.closest('[data-act]'); if(!el||el.disabled) return; const act=el.dataset.act, arg=el.dataset.arg; const r=S.run; const b=r&&r.battle;\n  switch(act){",
    """app.addEventListener('click',(ev)=>{ const el=ev.target.closest('[data-act]'); if(!el||el.disabled) return; const act=el.dataset.act, arg=el.dataset.arg; const r=S.run; const b=r&&r.battle;
  if(b&&S.screen==='battle'&&(b.busy||(S.multi&&b.curPid!==H().id))&&['card','target','ally','bench','end','berry','cancel'].includes(act)) return;
  if(S.resolving&&act==='node') return;
  switch(act){
    case 'mpn': S.mp.n=+arg; render(); break; case 'mpmode': S.mp.mode=arg; render(); break; case 'mpscale': S.mp.scale=arg; render(); break;""")
rep("case 'node': { const [f,l]=arg.split(',').map(Number); const n=r.map[f][l]; if(reachable().includes(n)) enterNode(n); } break;",
    "case 'node': { const [f,l]=arg.split(',').map(Number); const n=r.map[f][l]; chooseNode(n); } break;")
rep("case 'tomap': r.reward=null; r.event=null; r.shop=null; S.ui={}; S.screen='map'; render(); break;", "case 'tomap': toMap(); break;")
rep("S.run=null; S.screen='title';", "S.run=null; S.multi=null; S.screen='title';", 3)
rep("if(j){ S.mode=j.mode||S.mode; S.chart=j.chart||S.chart; }", "if(j){ S.mode=j.mode||S.mode; S.chart=j.chart||S.chart; if(j.mp) S.mp=j.mp; }")

# 이벤트 처리 확장
i0 = s.index("function doEvent(k){")
i1 = s.index("function doRest(k){", i0)
s = s[:i0] + """function doEvent(k){ const r=S.run, ev=r.event; const lead=r.party[S.mode==='switch'?r.active:0]; ev.done=true;
  switch(k){ case 'leave': ev.text='조용히 지나갔다.'; break;
    case 'rm1': ev.text='할아버지가 고개를 끄덕인다.'; ev.pickCard={mode:'remove',cards:r.deck.slice(),left:1,title:'잊을 기술 카드를 고르세요'}; break;
    case 'rm2': lead.hp=Math.max(1,lead.hp-7); ev.text=lead.ko+'이(가) 7 피해를 입었다.'; ev.pickCard={mode:'remove',cards:r.deck.slice(),left:2,title:'잊을 기술 카드를 고르세요 (2장)'}; break;
    case 'fish': if(chance(.6)){ const sp=pick(['psyduck','slowpoke']); if(r.party.length<3){ r.party.push(joinMon(sp)); ev.text='찌가 움직였다! '+SP[sp].ko+'이(가) 낚였다. 파티에 들어왔다.'; } else { r.deck.push(mkCard(pick(SP[sp].moves.filter(id=>M[id])),null)); ev.text=SP[sp].ko+'이(가) 낚였지만 파티가 가득 차서 기술 카드만 배웠다.'; } } else { if(r.party.length<3){ r.party.push(joinMon('magikarp')); ev.text='잉어킹이다... 잉어킹이 파티에 들어왔고 덱에 튀어오르기 카드가 들어왔다. '+placeOf(6)+'부터 포켓몬센터에서 진화할 수 있다.'; } else { ev.text='잉어킹이다... 덱에 튀어오르기 카드 2장이 들어왔다.'; r.deck.push(mkCard('splashc',null)); } r.deck.push(mkCard('splashc',null)); } break;
    case 'camp': for(const m of r.party) heal(m,Math.round(m.maxHp*.15)); ev.text='모닥불 앞에서 함께 쉬었다. 파티 HP 15% 회복.'; break;
    case 'elite': r.event=null; startBattle('elite',{trainer:ev.id==='rival'?{name:'라이벌 그린',mons:['pidgeotto','wartortle'],line:'내 포켓몬의 냄새를 맡아 보라고!'}:pick(TRAINERS.slice(2))}); return;
    case 'give': if(r.items.length){ const it=r.items.pop(); ev.text=ITEMS[it][0]+'을(를) 빼앗겼다.'; } else { r.money=Math.max(0,r.money-30); ev.text='30원을 빼앗겼다.'; } break;
    case 'fight': lead.hp=Math.max(1,lead.hp-12); r.money+=40; ev.text=lead.ko+'이(가) 12 피해를 입으며 똘마니를 쫓아냈다. 떨어뜨린 40원을 주웠다.'; break;
    case 'rock': { const m=r.party.find(canEvolve); if(m){ const id=evolve(m); ev.text='바위가 빛났다! '+m.ko+'(으)로 진화했다. 새 기술 카드: '+KO[id].n; } else { r.money+=20; ev.text='바위 밑에서 20원을 찾았다.'; } } break;
    case 'train': lead.hp=Math.max(1,lead.hp-8); ev.text=lead.ko+'이(가) 8 피해를 입으며 수련했다.'; ev.upCard={cards:r.deck.filter(c=>!c.up)}; break;
    case 'healone': { const m=r.party.reduce((a,x)=>a.hp/a.maxHp<x.hp/x.maxHp?a:x); heal(m,m.maxHp); m.st={}; ev.text=m.ko+'이(가) 완전히 회복했다.'; } break;
    case 'healall': for(const m of r.party) heal(m,Math.round(m.maxHp*.2)); ev.text='파티 전원이 20% 회복했다.'; break;
    case 'berry1': { const bk=pick(Object.keys(BERRIES)); if(r.berries.length<3){ r.berries.push(bk); ev.text=BERRIES[bk][0]+'을(를) 땄다.'; } else ev.text='열매 가방이 가득 차서 '+BERRIES[bk][0]+'을(를) 두고 왔다.'; } break;
    case 'shake': { const got=[]; for(let i=0;i<2;i++){ const bk=pick(Object.keys(BERRIES)); if(r.berries.length<3){ r.berries.push(bk); got.push(BERRIES[bk][0]); } } ev.text=(got.length?got.join(', ')+'이(가) 떨어졌다.':'가방이 가득 차 열매를 주울 수 없었다.'); if(chance(.4)){ r.event=null; startBattle('wild',{table:['caterpie','weedle','paras']}); return; } } break;
    case 'moon': { const m=r.party.find(x=>SP[x.sp].evo); if(m){ const id=evolve(m); SFX.play('evolve'); ev.text='달의돌이 빛났다! '+m.ko+'(으)로 진화했다. 새 기술 카드: '+KO[id].n; } else { r.money+=80; ev.text='돌을 주워 80원에 팔았다.'; } } break;
    case 'egg': r.egg={left:2}; ev.text='알을 받았다. 전투를 2번 하면 부화한다.'; break;
    case 'buykarp': if(r.money>=50){ r.money-=50; if(r.party.length<3){ r.party.push(joinMon('magikarp')); ev.text='잉어킹을 샀다! '+placeOf(6)+'부터 포켓몬센터에서 갸라도스로 진화할 수 있다.'; } else { r.deck.push(mkCard('splashc',null)); ev.text='잉어킹을 샀지만 파티가 가득 차 튀어오르기 카드만 받았다...'; } } else ev.text='돈이 부족해 장수가 코웃음을 쳤다.'; break;
    case 'open': { const roll=Math.random(); if(roll<.4){ const it=pick(Object.keys(ITEMS).filter(i=>!r.items.includes(i))); r.items.push(it); ev.text='소포 안에 '+ITEMS[it][0]+'이(가) 들어 있었다!'; } else if(roll<.8){ r.money+=40; ev.text='40원이 들어 있었다.'; } else ev.text='소포는 비어 있었다...'; } break;
    case 'post': r.money+=10; ev.text='우체통에 넣었다. 착한 일을 해서 10원을 받았다.'; break;
    case 'adopt': { const sp=pick(['pikachu','sandshrew','meowth','psyduck','oddish']); if(r.party.length<3){ const m=joinMon(sp); m.hp=Math.round(m.maxHp*.3); r.party.push(m); ev.text=SP[sp].ko+'이(가) 파티에 들어왔다. 많이 지쳐 있다 (HP 30%).'; } else { r.deck.push(mkCard(pick(SP[sp].moves.filter(id=>M[id])),null)); ev.text=SP[sp].ko+'이(가) 기술을 가르쳐 주고 떠났다.'; } } break;
    case 'trade': ev.text='"좋아, 어떤 카드를 줄래?"'; ev.pickCard={mode:'trade',cards:r.deck.filter(c=>c.owner),left:1,title:'넘길 기술 카드를 고르세요 (같은 포켓몬의 희귀 카드를 받는다)'}; break;
    case 'bath': for(const m of r.party){ heal(m,Math.round(m.maxHp*.4)); m.st={}; } ev.text='온천에 몸을 담갔다. 전원 40% 회복, 상태이상 해제.'; break; }
  render(); }
""" + s[i1:]
rep("case 'evpick': { const ev=r.event; const c=ev.pickCard.cards[+arg]; if(ev.pickCard.mode==='remove'){",
    "case 'evpick': { const ev=r.event; const c=ev.pickCard.cards[+arg]; if(ev.pickCard.mode==='trade'){ r.deck=r.deck.filter(x=>x.uid!==c.uid); const o=r.party.find(m=>m.uid===c.owner); const pool=o?SP[o.sp].pool.filter(id=>M[id]&&M[id].rare):[]; const nid=pool.length?pick(pool):pick(SP[o?o.sp:r.party[0].sp].pool.filter(id=>M[id])); const nc=mkCard(nid,o?o.uid:null); r.deck.push(nc); ev.text+=' '+cname(c)+' → '+cname(nc)+'.'; ev.pickCard=null; } else if(ev.pickCard.mode==='remove'){")

# ---------- 멀티 흐름·봇 ----------
rep("/* ---------- 도움말 ---------- */", r"""/* ---------- 멀티(협동) 흐름 · 봇 ---------- */
function botPickNode(p,re){ const hpf=p.party.reduce((a,m)=>a+m.hp,0)/Math.max(1,p.party.reduce((a,m)=>a+m.maxHp,0));
  const scored=re.map(n=>{ let sc=Math.random()*2; if(n.t==='rest') sc+=hpf<.5?5:1; if(n.t==='shop') sc+=p.money>=100?3:0; if(n.t==='treasure') sc+=4; if(n.t==='wild') sc+=p.party.length<3&&p.balls>0?2.5:1.5; if(n.t==='trainer') sc+=hpf>.6?2:0; if(n.t==='event') sc+=1.5; if(n.t==='boss') sc+=10; return [sc,n]; });
  return scored.reduce((a,b)=>b[0]>a[0]?b:a)[1]; }
function planBots(){ const mu=S.multi; if(!mu) return; for(const p of mu.players){ if(!p.bot||p.dead){ delete mu.intents[p.id]; continue; } const re=reachableOf(p); if(!re.length){ delete mu.intents[p.id]; continue; } const n=botPickNode(p,re); mu.intents[p.id]=n.f+','+n.l; } }
async function chooseNode(n){ const r=H(); S.run=r; if(S.resolving||!reachableOf(r).includes(n)) return;
  if(!S.multi){ enterNode(n); return; }
  const mu=S.multi; const key=n.f+','+n.l; const alive=mu.players.filter(p=>!p.dead); let node=n, group;
  if(mu.mode==='vote'){ const votes={}; votes[key]=1; for(const p of alive) if(p.bot&&mu.intents[p.id]) votes[mu.intents[p.id]]=(votes[mu.intents[p.id]]||0)+1;
    const top=Math.max(...Object.values(votes)); const wk=pick(Object.keys(votes).filter(k=>votes[k]===top)); const [f,l]=wk.split(',').map(Number); node=r.map[f][l]; group=alive;
    mu.lastVote=Object.entries(votes).map(([k,v])=>{ const [f2,l2]=k.split(',').map(Number); return NODE_TXT[r.map[f2][l2].t][0]+' '+v+'표'; }).join(' · ')+' → '+NODE_TXT[node.t][0]; }
  else group=[r].concat(alive.filter(p=>p.bot&&mu.intents[p.id]===key));
  mu.floorNews=[]; await enterGroup(node,group); }
async function enterGroup(n,group){ const me=H(); for(const p of group) visit(p,n);
  if(n.t==='wild'||n.t==='trainer'||n.t==='boss'){ S.run=me; startBattle(n.t,{parts:group}); if(S.multi&&S.multi.lastVote&&S.multi.mode==='vote') log('투표: '+S.multi.lastVote); return; }
  const bots=group.filter(p=>p.bot); if(bots.length) await headlessGroup(bots,n);
  S.run=me; S.ui={}; openNode(n); }
async function toMap(){ const r=H(); S.run=r; r.reward=null; r.event=null; r.shop=null; S.ui={}; S.screen='map'; if(S.multi){ S.resolving=true; render(); try{ await resolveFloor(); } finally{ S.resolving=false; } } render(); }
async function resolveFloor(){ const mu=S.multi; if(!mu) return; const me=H(); const pend=mu.players.filter(p=>p.bot&&!p.dead&&p.floor<me.floor);
  const groups={}; for(const p of pend){ const re=reachableOf(p); if(!re.length) continue; let k=mu.intents[p.id]; if(!k||!re.some(n=>n.f+','+n.l===k)){ const n=botPickNode(p,re); k=n.f+','+n.l; } (groups[k]||(groups[k]=[])).push(p); }
  for(const k in groups){ const [f,l]=k.split(',').map(Number); const n=me.map[f][l]; const g=groups[k]; for(const p of g) visit(p,n); await headlessGroup(g,n); }
  mu.news=mu.floorNews.slice(); mu.floorNews=[]; planBots(); }
async function headlessGroup(bots,n){ const keep={run:S.run,screen:S.screen,ui:S.ui}; S.headless=true; clearTimeout(autoTimer); const mu=S.multi; const names=bots.map(p=>p.name).join(', ');
  try{ if(n.t==='wild'||n.t==='trainer'||n.t==='boss'){ S.run=bots[0]; startBattle(n.t,{parts:bots,lead:bots[0]}); const b=S.run.battle; let g=0; while(S.screen==='battle'&&g++<150){ await botTurn(b); if(S.screen!=='battle') break; await endTurn(); }
      if(S.screen==='gameover'){ for(const p of bots) p.dead=true; mu.floorNews.push(names+': '+PLACES[n.f]+'의 '+NODE_TXT[n.t][0]+'에서 쓰러졌다...'); }
      else if(S.screen==='battle'){ b.over='draw'; mu.floorNews.push(names+': 전투가 길어져 도망쳤다.'); }
      else mu.floorNews.push(names+': '+PLACES[n.f]+' '+(b.kind==='boss'?'관장전':b.kind==='wild'?'야생 '+b.enemies.map(e=>e.ko).join('·'):'트레이너')+' 승리 ('+bots.map(p=>p.name+' HP '+p.party.map(m=>m.hp).join('/')+(p.lastNews?' '+p.lastNews:'')).join(', ')+')'); }
    else { for(const p of bots){ S.run=p; S.ui={}; p.lastNews=''; openNode(n); let g=0; while(g++<40){ if(S.screen==='battle'){ const b=p.battle; await botTurn(b); if(S.screen==='battle') await endTurn(); } else if(['reward','event','rest','shop'].includes(S.screen)) botStep(p); else break; }
        if(S.screen==='gameover'){ p.dead=true; mu.floorNews.push(p.name+': '+PLACES[n.f]+'에서 쓰러졌다...'); } else mu.floorNews.push(p.name+': '+PLACES[n.f]+' '+(p.lastNews||NODE_TXT[n.t][0])); } }
  } finally { for(const p of bots){ p.battle=null; p.reward=null; p.event=null; p.shop=null; p.lastNews=''; } S.headless=false; S.run=keep.run; S.screen=keep.screen; S.ui=keep.ui; } }
async function botTurn(b){ const r=S.run; let g=0; b.botAct=true;
  try{ while(g++<15&&!b.over&&S.screen==='battle'){
    if(b.sel&&b.sel.kind==='switch'){ const i=r.party.findIndex((m,k)=>k!==r.active&&m.hp>0); if(i>=0) doSwitch(i); b.sel=null; }
    if(S.mode==='switch'&&b.freeSwitch&&r.party[r.active].hp<r.party[r.active].maxHp*.3){ const i=r.party.findIndex((m,k)=>k!==r.active&&m.hp>r.party[r.active].hp); if(i>=0){ doSwitch(i); b.freeSwitch=false; } }
    const order=b.hand.map((c,i)=>i).sort((x,y)=>(def(b.hand[y]).dmg||0)-(def(b.hand[x]).dmg||0)); let played=false;
    for(const i of order){ const c=b.hand[i]; if(canPlay(c)) continue; const nt=needsTarget(c); if(nt==='enemy'){ const e=b.enemies.filter(x=>x.hp>0).sort((p,q)=>p.hp-q.hp)[0]; playCard(i,{kind:'enemy',e}); } else if(nt==='ally'){ const fm=fieldMons().slice().sort((p,q)=>p.hp/p.maxHp-q.hp/q.maxHp); playCard(i,{kind:'ally',m:fm[0]}); } else playCard(i); played=true; break; }
    if(!played) break; await sleep(S.auto?250:380); } }
  finally{ b.botAct=false; } }
function botTakeReward(r,rw){ const keep=S.run; S.run=r; const notes=[];
  r.money+=rw.money; if(rw.berry&&r.berries.length<3) r.berries.push(rw.berry); if(rw.item) r.items.push(rw.item); if(rw.items3&&rw.items3.length) r.items.push(rw.items3[0]);
  if(rw.cards&&rw.cards.length){ const best=rw.cards.slice().sort((x,y)=>(def(y).dmg||0)-(def(x).dmg||0))[0]; r.deck.push(best); notes.push('카드 '+cname(best)); }
  if(rw.capture&&r.balls>0&&r.party.length<3){ r.balls--; if(chance(rw.capture.p)){ r.party.push(joinMon(rw.capture.sp)); notes.push(SP[rw.capture.sp].ko+' 포획!'); } else notes.push('포획 실패'); }
  if(rw.captured) notes.push(SP[rw.captured].ko+' 포획!'); if(rw.hatch) notes.push('알 부화');
  if(rw.evo){ const m=r.party.find(canEvolve); if(m){ const was=m.ko; evolve(m); notes.push(was+' → '+m.ko+' 진화'); } } if(rw.badge) r.badges.push(rw.badge);
  r.lastNews=notes.join(', '); S.run=keep; }
function botStep(r){ const scr=S.screen; S.run=r;
  if(scr==='reward'){ const rw=r.reward; botTakeReward(r,rw); r.reward=null; if(rw.kind==='boss'){ S.screen='win'; } else S.screen='map'; return; }
  if(scr==='event'){ const ev=r.event; if(!ev.done){ doEvent(EVENTS[ev.id].bot); if(S.screen!=='event') return; }
    if(ev.pickCard){ const cs=ev.pickCard.cards; const c=cs.find(x=>['guard','growl','tailwhip','splashc'].includes(x.id))||cs[0]; if(c){ if(ev.pickCard.mode==='remove') r.deck=r.deck.filter(x=>x.uid!==c.uid); else if(ev.pickCard.mode==='trade'){ r.deck=r.deck.filter(x=>x.uid!==c.uid); const o=r.party.find(m=>m.uid===c.owner); const pool=o?SP[o.sp].pool.filter(id=>M[id]&&M[id].rare):[]; if(pool.length) r.deck.push(mkCard(pick(pool),o.uid)); } else r.deck.push(c); } ev.pickCard=null; }
    if(ev.upCard){ const c=ev.upCard.cards[0]; if(c) c.up=true; ev.upCard=null; }
    r.lastNews=EVENTS[ev.id].t+': '+ev.text; r.event=null; S.screen='map'; return; }
  if(scr==='rest'){ const m=r.party.find(canEvolve); const k=m?'evo:'+m.uid:(r.party.some(x=>x.hp<x.maxHp*.6)?'heal':'train'); doRest(k); if(S.ui.upCards&&S.ui.upCards[0]) S.ui.upCards[0].up=true; r.lastNews='포켓몬센터: '+(k==='heal'?'회복':k==='train'?'훈련':'진화'); S.ui={}; S.screen='map'; return; }
  if(scr==='shop'){ const sh=r.shop; const bought=[]; if(sh.cards[0]&&r.money>=(def(sh.cards[0]).rare?100:50)){ r.money-=def(sh.cards[0]).rare?100:50; r.deck.push(sh.cards[0]); bought.push(cname(sh.cards[0])); } if(r.money>=50&&r.balls<3){ r.money-=50; r.balls++; bought.push('몬스터볼'); } for(const bk of sh.berries){ if(r.money>=BERRIES[bk][2]&&r.berries.length<3){ r.money-=BERRIES[bk][2]; r.berries.push(bk); bought.push(BERRIES[bk][0]); break; } }
    r.lastNews='상점: '+(bought.join(', ')||'구경만 함'); r.shop=null; S.screen='map'; return; }
}
/* ---------- 도움말 ---------- */""")

rep("'<h3>이 체험판에서 빠진 것</h3>",
    "'<h3>멀티플레이 (상정)</h3><table><tr><th></th><th>투표형</th><th>분산형</th></tr><tr><td>이동</td><td>모두 같은 길. 노드마다 투표, 다수결(동률은 무작위)</td><td>각자 길 선택. 같은 노드면 합류</td></tr><tr><td>전투</td><td>항상 전원 협동. 각자 에너지 3·손패, 적은 모든 참가자의 포켓몬을 노린다</td><td>같은 노드끼리 협동, 혼자면 단독. 체육관은 전원 합류</td></tr><tr><td>적 강도</td><td>인원 비례(야생 HP +20%/명, 트레이너 +45%/명, 피해 +10%/명)</td><td>고정 (관장만 인원 비례)</td></tr><tr><td>보상</td><td>각자 전부</td><td>함께면 돈 1/n, 카드 선택지 2장, 도구·열매·포획은 1명에게. 혼자면 전부</td></tr><tr><td>진행</td><td colspan=2>지역 단위로 동시 진행. 내가 없는 그룹은 봇이 같은 엔진으로 자동 처리하고 결과가 \"동료 소식\"에 뜬다</td></tr></table>'+\n'<h3>이 체험판에서 빠진 것</h3>")
rep("진화(포켓몬센터·이끼 낀 바위·관장전 후, 1진화는 5층부터)", "진화(포켓몬센터·이끼 낀 바위·달의돌·관장전 후, 1진화는 월견산 기슭부터)")

p.write_text(s, encoding='utf-8')
print('patched', len(s))
