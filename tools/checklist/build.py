"""Builds index.html for the posting checklist from eps.json (data embedded)."""
import json, os
S = os.path.dirname(os.path.abspath(__file__))
eps = json.load(open(os.path.join(S, "eps.json")))
BASE = "https://chris61ds-alt.github.io/notjustyou-media/"

HTML = r"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Not just you Posting</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@500;700&family=Roboto:wght@400;500;700;900&family=Roboto+Mono:wght@500&display=swap" rel="stylesheet">
<style>
:root{--bg:#fafaf8;--card:#fff;--ink:#0c0c0c;--mid:#77776f;--rule:#e2e2de;--sig:#ff4000;--sig-ink:#fff;--ok:#0c0c0c;--chip:#efefeb}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0e0e0d;--card:#171716;--ink:#f2f2ee;--mid:#8c8c86;--rule:#2a2a28;--sig:#ff5a1f;--sig-ink:#fff;--ok:#f2f2ee;--chip:#222220}}
:root[data-theme="dark"]{--bg:#0e0e0d;--card:#171716;--ink:#f2f2ee;--mid:#8c8c86;--rule:#2a2a28;--sig:#ff5a1f;--sig-ink:#fff;--ok:#f2f2ee;--chip:#222220}
*{box-sizing:border-box}html,body{margin:0}
body{background:var(--bg);color:var(--ink);font:400 15px/1.45 Roboto,system-ui,sans-serif;-webkit-font-smoothing:antialiased}
.wrap{max-width:860px;margin:0 auto;padding:28px 16px 80px}
h1{font:900 clamp(34px,8vw,56px)/.95 Roboto,sans-serif;letter-spacing:-.02em;margin:0 0 6px;text-transform:uppercase}
h1 span{color:var(--sig)}
.sub{font:500 14px 'Roboto Condensed',sans-serif,sans-serif;color:var(--mid);text-transform:uppercase;letter-spacing:.06em;margin-bottom:22px}
.stats{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:18px}
.stat{border-top:4px solid var(--ink);padding:8px 2px 0;min-width:120px;flex:1}
.stat b{display:block;font:900 30px/1 Roboto,sans-serif;font-variant-numeric:tabular-nums}
.stat.s b{color:var(--sig)}.stat.s{border-color:var(--sig)}
.stat small{font:500 12px 'Roboto Condensed',sans-serif;color:var(--mid);text-transform:uppercase;letter-spacing:.06em}
.bar{position:sticky;top:0;z-index:5;background:var(--bg);padding:10px 0;border-bottom:1px solid var(--rule);display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.f{border:0;background:var(--chip);color:var(--ink);font:700 13px 'Roboto Condensed',sans-serif;text-transform:uppercase;letter-spacing:.05em;padding:8px 12px;border-radius:999px;cursor:pointer}
.f[aria-pressed="true"]{background:var(--ink);color:var(--bg)}
.q{flex:1;min-width:140px;border:1px solid var(--rule);background:var(--card);color:var(--ink);border-radius:999px;padding:8px 14px;font:400 14px Roboto,sans-serif}
.note{font-size:12px;color:var(--mid);margin:10px 0 0}
.day{font:700 13px 'Roboto Mono',monospace,monospace;color:var(--mid);margin:26px 0 8px;text-transform:uppercase;letter-spacing:.04em}
.ep{display:grid;grid-template-columns:72px 1fr;gap:14px;background:var(--card);border:1px solid var(--rule);border-radius:10px;padding:12px;margin-bottom:10px}
.ep.done{opacity:.55}
.ep img{width:72px;height:128px;object-fit:cover;border-radius:6px;background:var(--chip);display:block}
.top{display:flex;justify-content:space-between;gap:10px;align-items:flex-start}
.no{font:500 12px 'Roboto Mono',monospace;color:var(--sig)}
.t{font:900 19px/1.15 Roboto,sans-serif;text-transform:uppercase;margin:2px 0 4px;letter-spacing:-.01em}
.when{font:500 12px 'Roboto Mono',monospace;color:var(--mid)}
.acts{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
.btn{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--ink);color:var(--ink);background:none;font:700 12px 'Roboto Condensed',sans-serif;text-transform:uppercase;letter-spacing:.05em;padding:7px 11px;border-radius:6px;cursor:pointer;text-decoration:none}
.btn.p{background:var(--sig);border-color:var(--sig);color:var(--sig-ink)}
.checks{display:flex;gap:6px;flex-shrink:0}
.ck{display:flex;flex-direction:column;align-items:center;gap:3px;cursor:pointer;user-select:none}
.ck input{position:absolute;opacity:0;pointer-events:none}
.box{width:34px;height:34px;border:2px solid var(--mid);border-radius:8px;display:grid;place-items:center;transition:.12s}
.box svg{width:20px;height:20px;stroke:var(--sig-ink);stroke-width:3;fill:none;opacity:0}
.ck input:checked+.box{background:var(--sig);border-color:var(--sig)}
.ck input:checked+.box svg{opacity:1}
.ck input:focus-visible+.box{outline:2px solid var(--ink);outline-offset:2px}
.ck span{font:700 10px 'Roboto Condensed',sans-serif;text-transform:uppercase;color:var(--mid);letter-spacing:.05em}
details{margin-top:8px}summary{cursor:pointer;font:500 12px 'Roboto Condensed',sans-serif;text-transform:uppercase;color:var(--mid);letter-spacing:.05em}
pre{white-space:pre-wrap;font:400 13px/1.45 Roboto,sans-serif;background:var(--chip);padding:10px;border-radius:6px;margin:8px 0 0;overflow-wrap:anywhere}
.toast{position:fixed;left:50%;bottom:20px;transform:translateX(-50%);background:var(--ink);color:var(--bg);font:700 13px 'Roboto Condensed',sans-serif;text-transform:uppercase;padding:10px 16px;border-radius:999px;opacity:0;transition:.2s;pointer-events:none}
.toast.on{opacity:1}
.empty{color:var(--mid);padding:30px 0;text-align:center}
@media (max-width:480px){.ep{grid-template-columns:56px 1fr}.ep img{width:56px;height:100px}.t{font-size:16px}.box{width:30px;height:30px}}
</style></head><body><div class="wrap">
<h1>Not just you<br><span>Posting-Liste</span></h1>
<div class="sub">@vascoda.soda · alle Reels mit Caption · Häkchen für manuell gepostet</div>
<div class="stats">
 <div class="stat s"><b id="sTT">0</b><small>TikTok gepostet</small></div>
 <div class="stat"><b id="sIG">0</b><small>Instagram manuell</small></div>
 <div class="stat"><b id="sAll">0</b><small>Videos gesamt</small></div>
</div>
<div class="bar" role="toolbar" aria-label="Filter">
 <button class="f" data-f="plan" aria-pressed="true">Im Plan</button>
 <button class="f" data-f="open" aria-pressed="false">TikTok offen</button>
 <button class="f" data-f="all" aria-pressed="false">Alle</button>
 <input class="q" id="q" type="search" placeholder="Suchen: Nr. oder Titel" aria-label="Suchen">
</div>
<p class="note" id="sync">Lädt …</p>
<div id="list"></div>
</div><div class="toast" id="toast" role="status"></div>
<script>
const BASE = __BASE__;
const EPS = __EPS__;
const state = {};            // "nj06" -> {tiktok:bool, ig:bool}
let filter = 'plan', query = '', db = null, col = null, mode = 'local';
const pad = n => String(n).padStart(2,'0');
const id = e => 'nj' + pad(e.no);
const $ = s => document.querySelector(s);
const DOW = ['So','Mo','Di','Mi','Do','Fr','Sa'];
function fmtDay(d){ if(!d) return 'Nicht im Instagram-Plan'; const [y,m,dd]=d.split('-').map(Number); const dt=new Date(y,m-1,dd); return DOW[dt.getDay()]+' '+pad(dd)+'.'+pad(m)+'.'; }
function toast(t){ const el=$('#toast'); el.textContent=t; el.classList.add('on'); clearTimeout(toast._t); toast._t=setTimeout(()=>el.classList.remove('on'),1400); }
function loadLocal(){ try{ const s=JSON.parse(localStorage.getItem('njy-posted')||'{}'); Object.assign(state,s); }catch(e){} }
function saveLocal(){ try{ localStorage.setItem('njy-posted', JSON.stringify(state)); }catch(e){} }
const CHECK = '<svg viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7"/></svg>';

function render(){
  const list = $('#list'); list.innerHTML='';
  let rows = EPS.slice();
  if(filter==='plan') rows = rows.filter(e=>e.date);
  if(filter==='open') rows = rows.filter(e=>!(state[id(e)]||{}).tiktok);
  if(query){ const q=query.toLowerCase(); rows = rows.filter(e=>String(e.no).includes(q)||e.title.toLowerCase().includes(q)||e.caption.toLowerCase().includes(q)); }
  rows.sort((a,b)=> (a.date? (a.date+a.time) : 'z'+pad(b.no)).localeCompare(b.date? (b.date+b.time) : 'z'+pad(a.no)) || a.no-b.no);
  if(!a_or(rows)){ list.innerHTML='<div class="empty">Nichts offen. Stark.</div>'; }
  let lastDay = null;
  for(const e of rows){
    const day = fmtDay(e.date);
    if(day!==lastDay){ const h=document.createElement('div'); h.className='day'; h.textContent=day; list.appendChild(h); lastDay=day; }
    const st = state[id(e)]||{};
    const el = document.createElement('article'); el.className='ep'+(st.tiktok&&(st.ig||e.date)?' done':'');
    el.innerHTML = `<a href="${BASE+id(e)}.mp4" target="_blank" rel="noopener"><img loading="lazy" alt="" src="thumbs/${id(e)}.jpg"></a>
      <div><div class="top"><div><div class="no">No. ${pad(e.no)}</div><div class="t"></div><div class="when">${e.date? 'IG auto · '+e.time : 'nicht eingeplant'}</div></div>
      <div class="checks">
        <label class="ck"><input type="checkbox" data-k="tiktok" ${st.tiktok?'checked':''}><div class="box">${CHECK}</div><span>TikTok</span></label>
        <label class="ck"><input type="checkbox" data-k="ig" ${st.ig?'checked':''}><div class="box">${CHECK}</div><span>IG manuell</span></label>
      </div></div>
      <div class="acts"><a class="btn p" href="${BASE+id(e)}.mp4" target="_blank" rel="noopener">Video öffnen</a>
        <button class="btn" data-copy>Caption kopieren</button>
        <a class="btn" href="${BASE+id(e)}.jpg" target="_blank" rel="noopener">Cover</a></div>
      <details><summary>Caption anzeigen</summary><pre></pre></details></div>`;
    el.querySelector('.t').textContent = e.title;
    el.querySelector('pre').textContent = e.caption;
    el.querySelector('[data-copy]').onclick = ()=>copy(e.caption);
    el.querySelectorAll('input[type=checkbox]').forEach(cb=>cb.onchange=()=>toggle(e, cb.dataset.k, cb.checked));
    list.appendChild(el);
  }
  const all = EPS.length, tt = EPS.filter(e=>(state[id(e)]||{}).tiktok).length, ig = EPS.filter(e=>(state[id(e)]||{}).ig).length;
  $('#sTT').textContent = tt+' / '+all; $('#sIG').textContent = ig; $('#sAll').textContent = all;
}
function a_or(r){ return r.length>0; }
async function copy(t){
  try{ await navigator.clipboard.writeText(t); toast('Caption kopiert'); }
  catch(err){ const ta=document.createElement('textarea'); ta.value=t; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); let ok=false; try{ ok=document.execCommand('copy'); }catch(e){} ta.remove(); toast(ok?'Caption kopiert':'Kopieren blockiert – Caption aufklappen'); }
}
async function toggle(e, k, v){
  const key = id(e); const prev = Object.assign({}, state[key]||{});
  state[key] = Object.assign({}, prev, {[k]: v}); render();
  if(mode==='db'){
    try{ await col.doc(key).set({tiktok: !!state[key].tiktok, ig: !!state[key].ig, no: e.no, updatedAt: new Date().toISOString()}); }
    catch(err){ state[key]=prev; render(); toast('Nicht gespeichert'); }
  } else { saveLocal(); }
}
document.querySelectorAll('.f').forEach(b=>b.onclick=()=>{ filter=b.dataset.f; document.querySelectorAll('.f').forEach(x=>x.setAttribute('aria-pressed', x===b)); render(); });
$('#q').oninput = ev => { query = ev.target.value.trim(); render(); };

loadLocal(); render();
$('#sync').textContent = 'Nur in diesem Browser gespeichert.';
(async()=>{
  try{ db = window.claude && window.claude.use ? await window.claude.use('db') : null; }catch(e){ db=null; }
  if(!db) return;
  col = db.collection('posted'); mode='db';
  $('#sync').textContent = 'Synchronisiert auf allen Geräten.';
  col.onSnapshot(snap=>{
    for(const k of Object.keys(state)) delete state[k];
    snap.docs.forEach(d=>{ const v=d.data()||{}; state[d.id]={tiktok:!!v.tiktok, ig:!!v.ig}; });
    render();
  }, err=>{ $('#sync').textContent='Sync nicht verfügbar – Änderungen werden evtl. nicht gespeichert.'; });
})();
</script></body></html>"""

out = HTML.replace("__BASE__", json.dumps(BASE)).replace("__EPS__", json.dumps(eps, ensure_ascii=False).replace("</", "<\\/"))
open(os.path.join(S, "index.html"), "w").write(out)
print("ok", len(out))
