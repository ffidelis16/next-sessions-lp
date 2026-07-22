/* ===== 0. TRACKING — camada de eventos para GTM / GA4 / Meta Pixel.
   A página só EMPURRA eventos no dataLayer; quem escuta e dispara as tags é o container (GTM).
   Eventos: cta_click, form_open, form_submit, generate_lead, scroll_depth, scarcity_state. ===== */
window.dataLayer=window.dataLayer||[];
function track(ev,params){try{window.dataLayer.push(Object.assign({event:ev},params||{}));}catch(e){}}

/* ===== 1. OCUPAÇÃO — agenda de disponibilidade aprovada pelo cliente.
   Cada marco entra na virada do respectivo dia D-N (00h, BRT).
   Antes de D-45 a página permanece em 60; de D-1 até o início do evento, em 2.
   • TOTAL          → nº total de lugares
   • SCHEDULE       → pares [dias antes, lugares disponíveis]
   • LAST_THRESHOLD → abaixo ou igual vira "Últimos lugares"
   • FORCE_STATE    → 'open' | 'last' | 'waitlist' para teste visual
   Contagem real do HubSpot: trocar somente o corpo de getSeatsRemaining(). ===== */
const SEAT={
  TOTAL:60,
  EVENT:new Date('2026-08-26T18:30:00-03:00'),
  EVENT_DAY:new Date('2026-08-26T00:00:00-03:00'),
  SCHEDULE:[[45,60],[40,54],[35,53],[30,49],[25,42],[20,36],[15,29],[12,21],[10,16],[7,12],[5,8],[3,4],[1,2]],
  FORCE_STATE:null,
  LAST_THRESHOLD:10
};
function getSeatsRemaining(now=new Date()){
  const dayMs=86400000;
  let remaining=SEAT.TOTAL;
  for(const [daysBefore,seats] of SEAT.SCHEDULE){
    const milestone=new Date(SEAT.EVENT_DAY.getTime()-daysBefore*dayMs);
    if(now>=milestone)remaining=seats;
    else break;
  }
  return remaining;
}
function getSeatState(rem,now=new Date()){if(SEAT.FORCE_STATE)return SEAT.FORCE_STATE;if(now>=SEAT.EVENT)return'waitlist';if(rem<=SEAT.LAST_THRESHOLD)return'last';return'open';}

/* ===== 2. TEATRO — anfiteatro em leque, enche do centro-frente para trás ===== */
function makeTiers(total){ // 5 fileiras em leque que somam `total` (a última absorve a diferença)
  const a=Math.max(2,Math.round((total-20)/5)), t=[a,a+2,a+4,a+6,a+8];
  t[4]+=total-t.reduce((s,x)=>s+x,0); return t;
}
const TIERS=makeTiers(SEAT.TOTAL), SPAN=86, R0=90, GAP=19;
let theaterSeats=[];
function buildTheater(el){
  el.innerHTML='';const seats=[];
  TIERS.forEach((n,t)=>{
    const R=R0+t*GAP, step=n>1?SPAN/(n-1):0, mid=(n-1)/2;
    const order=[...Array(n).keys()].sort((a,b)=>Math.abs(a-mid)-Math.abs(b-mid));
    order.forEach(i=>{
      const angle=(i-mid)*step;
      const arm=document.createElement('span');arm.className='seat-arm';
      arm.style.height=R+'px';arm.style.transform=`translateX(-50%) rotate(${angle}deg)`;
      const s=document.createElement('span');s.className='seat';
      arm.appendChild(s);el.appendChild(arm);seats.push(s);
    });
  });
  return seats;
}
function paintTheater(animate){
  if(!theaterSeats.length)return;
  const occ=SEAT.TOTAL-getSeatsRemaining();
  theaterSeats.forEach((s,i)=>{
    const take=i<occ;
    if(animate&&take&&!s.classList.contains('taken')){setTimeout(()=>s.classList.add('taken'),i*20);}
    else{s.classList.toggle('taken',take);}
  });
}

/* ===== 3. Mini-arco do readout ===== */
function drawBar(el){
  const rem=getSeatsRemaining(),frac=Math.max(0,Math.min(1,1-rem/SEAT.TOTAL));
  const fill=el.querySelector('i');if(fill)fill.style.width=(frac*100).toFixed(1)+'%';
}

function renderSeats(animateTheater){
  const rem=getSeatsRemaining(),state=getSeatState(rem);
  const stateText={open:'Sala reservada',last:'Últimos lugares',waitlist:'Sala lotada'};
  document.querySelectorAll('[data-seats-state]').forEach(el=>{el.textContent=stateText[state];el.classList.toggle('is-last',state==='last');el.classList.toggle('is-wait',state==='waitlist');});
  const countHTML=state==='waitlist'?'A sala está cheia. Entre na <b>lista de espera</b>.':`<b>${rem}</b> de ${SEAT.TOTAL} lugares disponíveis`;
  document.querySelectorAll('[data-seats-count]').forEach(el=>el.innerHTML=countHTML);
  document.querySelectorAll('[data-seats-total]').forEach(el=>el.textContent=SEAT.TOTAL);
  const shortText=state==='waitlist'?'Lista de espera aberta':`${rem} lugares disponíveis`;
  document.querySelectorAll('[data-seats-text]').forEach(el=>el.textContent=shortText);
  document.querySelectorAll('[data-bar]').forEach(drawBar);
  paintTheater(animateTheater);
  if(state!==window.__seatState){window.__seatState=state;track('scarcity_state',{state:state});}
  if(state==='waitlist')document.querySelectorAll('[data-open-form]').forEach(b=>{if(!b.dataset.o)b.dataset.o=b.textContent;b.textContent='Entrar na lista de espera';});
}
const theaterEl=document.querySelector('[data-theater]');
if(theaterEl)theaterSeats=buildTheater(theaterEl);
renderSeats(false);
setInterval(()=>renderSeats(false),60000);

const salaSec=document.getElementById('sala');
if(salaSec){const io=new IntersectionObserver(([e])=>{if(e.isIntersecting){renderSeats(true);io.disconnect();}},{threshold:.35});io.observe(salaSec);}

/* ===== 4. Sticky + mobile CTA ===== */
const hero=document.querySelector('.hero'),stickybar=document.getElementById('stickybar'),mobilecta=document.getElementById('mobilecta');
new IntersectionObserver(([e])=>{const gone=!e.isIntersecting;stickybar.classList.toggle('show',gone);mobilecta.classList.toggle('show',gone);stickybar.setAttribute('aria-hidden',!gone);mobilecta.setAttribute('aria-hidden',!gone);},{rootMargin:'-80px 0px 0px 0px',threshold:0}).observe(hero);

/* ===== 5. Reveal ===== */
const ro=new IntersectionObserver((ents)=>{ents.forEach(en=>{if(en.isIntersecting){en.target.classList.add('in');ro.unobserve(en.target);}});},{threshold:.12,rootMargin:'0px 0px -8% 0px'});
document.querySelectorAll('.reveal').forEach((el,i)=>{el.style.transitionDelay=(i%6)*40+'ms';ro.observe(el);});

/* ===== 6. Modal HubSpot (lazy) ===== */
const modal=document.getElementById('formModal');let formRendered=false,lastFocus=null,lastCta='cta';
function openForm(src){lastCta=src||'cta';lastFocus=document.activeElement;modal.classList.add('open');document.body.style.overflow='hidden';track('form_open',{cta:lastCta});if(!formRendered&&window.hbspt){hbspt.forms.create({portalId:"8180620",formId:"bdb0ccad-d2b3-471a-adf1-9187057e1ab3",target:"#hubspotForm",onFormSubmitted:function(){track('form_submit',{cta:lastCta});track('generate_lead',{value:1});}});formRendered=true;}const x=modal.querySelector('.modal__x');if(x)x.focus();}
function closeForm(){modal.classList.remove('open');document.body.style.overflow='';if(lastFocus)lastFocus.focus();}
document.querySelectorAll('[data-open-form]').forEach(b=>b.addEventListener('click',()=>{track('cta_click',{cta:b.dataset.cta||'cta'});openForm(b.dataset.cta);}));
document.querySelectorAll('[data-close-form]').forEach(b=>b.addEventListener('click',closeForm));
document.addEventListener('keydown',e=>{
  if(!modal.classList.contains('open'))return;
  if(e.key==='Escape'){closeForm();return;}
  if(e.key==='Tab'){
    const f=modal.querySelectorAll('button,[href],input,select,textarea,[tabindex]:not([tabindex="-1"])');
    if(!f.length)return;
    const first=f[0],last=f[f.length-1];
    if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}
    else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}
  }
});

/* ===== 7. Slider de depoimentos — dots sincronizados ===== */
(function(){
  const track=document.querySelector('[data-depo-track]'),dotsWrap=document.querySelector('[data-depo-dots]');
  if(!track||!dotsWrap)return;
  const cards=[...track.children].filter(c=>c.classList&&c.classList.contains('tcard'));
  if(cards.length<=1){track.classList.add('is-single');dotsWrap.style.display='none';return;}
  function centerCard(i){const c=cards[i],tr=track.getBoundingClientRect(),cr=c.getBoundingClientRect();track.scrollBy({left:(cr.left+cr.width/2)-(tr.left+tr.width/2),behavior:'smooth'});}
  cards.forEach((c,i)=>{const b=document.createElement('button');b.className='depo__dot'+(i===0?' is-active':'');b.setAttribute('aria-label','Ver depoimento '+(i+1));b.addEventListener('click',()=>centerCard(i));dotsWrap.appendChild(b);});
  const dots=[...dotsWrap.children];let raf;
  track.addEventListener('scroll',()=>{cancelAnimationFrame(raf);raf=requestAnimationFrame(()=>{
    const tr=track.getBoundingClientRect(),center=tr.left+tr.width/2;let best=0,bestD=Infinity;
    cards.forEach((c,i)=>{const r=c.getBoundingClientRect(),cc=r.left+r.width/2,d=Math.abs(cc-center);if(d<bestD){bestD=d;best=i;}});
    dots.forEach((d,i)=>d.classList.toggle('is-active',i===best));
  });},{passive:true});
})();

/* ===== 8. TRACKING — rotula cada CTA pela origem e mede profundidade de scroll ===== */
(function(){
  const label=b=>b.closest('.stickybar')?'sticky':b.closest('.mobilecta')?'mobile_bar':b.closest('.hero__topbar')?'hero_topbar':b.closest('.hero')?'hero':b.closest('.playbook')?'playbook':b.closest('.local__card')?'local':b.closest('.close')?'final':'cta';
  document.querySelectorAll('[data-open-form]').forEach(b=>{if(!b.dataset.cta)b.dataset.cta=label(b);});
  const seen={};
  addEventListener('scroll',()=>{const h=document.body.scrollHeight-innerHeight;if(h<=0)return;const pct=Math.round((scrollY/h)*100);[25,50,75,100].forEach(m=>{if(!seen[m]&&pct>=m){seen[m]=1;track('scroll_depth',{percent:m});}});},{passive:true});
})();
