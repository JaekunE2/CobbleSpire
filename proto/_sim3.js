// 멀티(투표형/분산형) 헤드리스 시뮬레이션: 사람 자리도 봇 로직으로 채워 런 전체를 돌린다.
// 사용: node _sim3.js [런 수=60]
const vm=require('vm'),fs=require('fs');
const code=fs.readFileSync('_check.js','utf8');
function mk(){ const el={innerHTML:'',hidden:true,textContent:'',addEventListener(){},close(){},showModal(){},querySelectorAll(){return[]},querySelector(){return null},isConnected:false};
const sb={document:{getElementById:()=>el,addEventListener(){}},window:{},console,Math,JSON,setTimeout,clearTimeout,Set,Object,Array,Number,String,Boolean,Error,Promise};
vm.createContext(sb); vm.runInContext(code,sb); return sb; }
async function run(sb,mode,n,mpmode,seed){
  const S=sb.S; S.mode=mode; S.chart=seed%2?'orig':'soft'; S.mp={n,mode:mpmode,scale:'auto'}; sb.startRun(seed%3);
  let steps=0, lastKind='', coop=0, solo=0;
  while(steps++<4000){ const r=S.run; if(S.screen==='title') break;
    if(S.screen==='map'){ const me=sb.H(); const re=sb.reachableOf(me); if(!re.length) break; await sb.chooseNode(sb.botPickNode(me,re)); }
    else if(S.screen==='battle'){ const b=sb.H().battle; lastKind=b.kind; if(b.over) break; if(b.turn===1&&b.curPid===sb.H().id&&!b.counted){ b.counted=true; if(b.parts.length>1) coop++; else solo++; } await sb.botTurn(b); if(S.screen!=='battle') continue; await sb.endTurn(); }
    else if(['reward','event','rest','shop'].includes(S.screen)){ sb.botStep(sb.H()); if(S.screen==='map') await sb.toMap(); }
    else if(S.screen==='gameover'||S.screen==='win') break; else throw new Error('unknown '+S.screen); }
  const me=sb.H(); const mu=S.multi;
  return {screen:S.screen,floor:me.floor,kind:lastKind,coop,solo,botsDead:mu.players.filter(p=>p.bot&&p.dead).length,botsAlive:mu.players.filter(p=>p.bot&&!p.dead).length,money:me.money,news:mu.news.length,steps};
}
const N=+(process.argv[2]||60); const OV=process.argv[3]?JSON.parse(process.argv[3]):null;
(async()=>{ for(const mpmode of ['vote','split']) for(const n of [2,3]) for(const mode of ['switch','field']){ const sb=mk(); if(OV) for(const k in OV) Object.assign(sb.COOP[k],OV[k]); const res=[]; let err=null;
    for(let i=0;i<N;i++){ try{ res.push(await run(sb,mode,n,mpmode,i)); }catch(e){ err=e.stack.split('\n').slice(0,4).join(' | '); break; } }
    const wins=res.filter(r=>r.screen==='win').length; const deaths={}; for(const r of res) if(r.screen!=='win'){ const k=r.kind+'@'+r.floor; deaths[k]=(deaths[k]||0)+1; }
    const avg=(k)=>(res.reduce((a,r)=>a+r[k],0)/Math.max(1,res.length)).toFixed(2);
    console.log(mpmode,n+'p',mode,'win',wins+'/'+res.length,'floor',avg('floor'),'coop',avg('coop'),'solo',avg('solo'),'botsDead',avg('botsDead'),'money',avg('money'),'deaths',JSON.stringify(deaths),err?('ERR '+err):'');
  } })();
