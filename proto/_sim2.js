const vm=require('vm'),fs=require('fs');
const code=fs.readFileSync('_check.js','utf8');
function mk(){ const el={innerHTML:'',hidden:true,textContent:'',addEventListener(){},close(){},showModal(){},querySelectorAll(){return[]},querySelector(){return null},isConnected:false};
const sb={document:{getElementById:()=>el,addEventListener(){}},window:{},console,Math,JSON,setTimeout,clearTimeout,Set,Object,Array,Number,String,Boolean,Error,Promise};
vm.createContext(sb); vm.runInContext(code,sb); return sb; }
async function run(sb,mode,chart,seed){
  sb.S.mode=mode; sb.S.chart=chart; sb.startRun(seed%3); let steps=0, lastKind='';
  while(steps++<3000){ const S=sb.S, r=S.run;
    if(S.screen==='map'){ const re=sb.reachable(); if(!re.length) break; sb.enterNode(re[Math.floor(Math.random()*re.length)]); }
    else if(S.screen==='battle'){ const b=r.battle; lastKind=b.kind; if(b.over) break; let played=false;
      // 봇: 가장 비싼 카드부터 낼 수 있으면 낸다 (공격 우선)
      const order=b.hand.map((c,i)=>i).sort((x,y)=>{ const dx=sb.def(b.hand[x]), dy=sb.def(b.hand[y]); return (dy.dmg||0)-(dx.dmg||0); });
      for(const i of order){ const c=b.hand[i]; if(!sb.canPlay(c)){ const nt=sb.needsTarget(c); if(nt==='enemy'){ const e=b.enemies.filter(x=>x.hp>0).sort((p,q)=>p.hp-q.hp)[0]; sb.playCard(i,{kind:'enemy',e}); } else if(nt==='ally'){ const fm=sb.fieldMons(); sb.playCard(i,{kind:'ally',m:fm.sort((p,q)=>p.hp/p.maxHp-q.hp/q.maxHp)[0]}); } else sb.playCard(i); played=true; break; } }
      if(S.screen!=='battle') continue;
      if(b.sel&&b.sel.kind==='switch'){ const i=r.party.findIndex((m,k)=>k!==r.active&&m.hp>0); if(i>=0) sb.doSwitch(i); b.sel=null; }
      if(mode==='switch'&&b.freeSwitch&&r.party[r.active].hp<r.party[r.active].maxHp*.3){ const i=r.party.findIndex((m,k)=>k!==r.active&&m.hp>r.party[r.active].hp); if(i>=0){ sb.doSwitch(i); b.freeSwitch=false; } }
      if(!played) await sb.endTurn(); }
    else if(S.screen==='reward'){ const rw=r.reward; if(rw.money&&!rw.took.money) sb.takeReward('money'); if(rw.cards&&rw.cards.length&&!rw.took.cards){ const best=rw.cards.slice().sort((x,y)=>(sb.def(y).dmg||0)-(sb.def(x).dmg||0))[0]; r.deck.push(best); rw.took.cards=true; } if(rw.items3&&!rw.took.items3){ r.items.push(rw.items3[0]); rw.took.items3=true; } if(rw.item&&!rw.took.item) sb.takeReward('item');
      if(rw.capture&&!rw.took.capture&&r.balls>0&&r.party.length<3){ r.balls--; if(Math.random()<rw.capture.p){ rw.took.capture=true; r.party.push(sb.joinMon(rw.capture.sp)); } }
      if(rw.evo&&!rw.took.evo){ const m=r.party.find(sb.canEvolve); if(m) sb.evolve(m); rw.took.evo=true; }
      if(rw.kind==='boss'){ S.screen='win'; break; } r.reward=null; S.screen='map'; }
    else if(S.screen==='event'){ const ev=r.event; if(!ev.done){ const opts={forget:'rm1',fisher:'fish',camper:'camp',thief:'fight',mossrock:'rock',dojo:'train'}; sb.doEvent(opts[ev.id]); if(S.screen!=='event') continue; }
      if(ev.pickCard){ const c=ev.pickCard.cards.find(x=>x.id==='guard'||x.id==='growl'||x.id==='tailwhip')||ev.pickCard.cards[0]; if(ev.pickCard.mode==='remove'){ r.deck=r.deck.filter(x=>x.uid!==c.uid); } ev.pickCard=null; } if(ev.upCard){ if(ev.upCard.cards[0]) ev.upCard.cards[0].up=true; ev.upCard=null; } r.event=null; S.screen='map'; }
    else if(S.screen==='rest'){ const m=r.party.find(sb.canEvolve); if(m) sb.doRest('evo:'+m.uid); else sb.doRest(r.party.some(x=>x.hp<x.maxHp*.6)?'heal':'train'); if(sb.S.ui.upCards){ if(sb.S.ui.upCards[0]) sb.S.ui.upCards[0].up=true; } sb.S.ui={}; S.screen='map'; }
    else if(S.screen==='shop'){ const sh=r.shop; if(r.money>=50&&sh.cards[0]){ r.money-=50; r.deck.push(sh.cards[0]); } if(r.money>=50){ r.money-=50; r.balls++; } r.shop=null; S.screen='map'; }
    else if(['tutor','casino','daycare'].includes(S.screen)){ sb.botStep(r); }
    else if(S.screen==='gameover'||S.screen==='win') break; else throw new Error('unknown '+S.screen); }
  return {screen:sb.S.screen,floor:sb.S.run.floor,kind:lastKind,party:sb.S.run.party.length}; }
const bal=process.argv[2]?JSON.parse(process.argv[2]):null;
(async()=>{ for(const mode of ['switch','field']){ const sb=mk(); if(bal) Object.assign(sb.BAL[mode],bal[mode]||{}); const res=[]; for(let i=0;i<150;i++){ try{ res.push(await run(sb,mode,i%2?'orig':'soft',i)); }catch(e){ console.log('ERR',mode,e.stack.split('\n').slice(0,3).join('|')); break; } }
  const wins=res.filter(r=>r.screen==='win').length; const deaths={}; for(const r of res) if(r.screen!=='win'){ const k=r.kind+'@'+r.floor; deaths[k]=(deaths[k]||0)+1; }
  console.log(mode,'win',wins+'/'+res.length,'avg floor',(res.reduce((a,r)=>a+r.floor,0)/res.length).toFixed(1),'party',(res.reduce((a,r)=>a+r.party,0)/res.length).toFixed(2),'deaths',JSON.stringify(deaths)); }
})();
