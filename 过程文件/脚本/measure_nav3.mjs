#!/usr/bin/env node
/** 对比：每次切换导航的真实渲染耗时 + 同时存在的动画数量。 */
const PORT = Number(process.env.CDP_PORT || 9222);
const URL = process.argv[2];
const list = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
const page = list.find(t => t.type === 'page');
const ws = new WebSocket(page.webSocketDebuggerUrl);
let id = 0; const pending = new Map();
ws.addEventListener('message', ev => { const m = JSON.parse(ev.data); if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } });
await new Promise(r => ws.addEventListener('open', r));
const sleep = ms => new Promise(r => setTimeout(r, ms));
const send = (method, params) => { const i = ++id; return new Promise(res => { pending.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); }); };
async function ev(expression) {
  const r = await send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
  if (r.result && r.result.exceptionDetails) throw new Error(r.result.exceptionDetails.text);
  return r.result && r.result.result ? r.result.result.value : undefined;
}

await send('Page.navigate', { url: 'about:blank' });
await sleep(150);
await send('Page.navigate', { url: URL });
await sleep(1300);
await ev(`try{ if(document.getElementById('loginLayer')) hideLogin(); }catch(e){}`);

await ev(`(() => {
  window.__s = [];
  if (!window.__wrapped) {
    window.__wrapped = true;
    const base = window.render;
    window.render = function(){
      const t0 = performance.now();
      const out = base.apply(this, arguments);
      const t1 = performance.now();
      document.documentElement.offsetHeight;
      const t2 = performance.now();
      window.__s.push({ js: t1 - t0, layout: t2 - t1 });
      return out;
    };
  }
  return true;
})()`);

const mods = ['guide', 'task', 'adj', 'quality', 'teach', 'exp'];
const anims = [];
for (const m of mods) {
  await ev('window.__s = []');
  await ev(`setMod(${JSON.stringify(m)})`);
  await sleep(40);
  const a = await ev(`(() => {
    const list = document.getAnimations ? document.getAnimations() : [];
    return list.filter(x => x.playState === 'running').length;
  })()`);
  anims.push(a);
  await sleep(260);
}
const stats = await ev(`(() => {
  const s = window.__s;
  const js = s.map(x => x.js), lay = s.map(x => x.layout);
  const avg = a => a.length ? a.reduce((x,y)=>x+y,0)/a.length : 0;
  return {
    samples: s.length,
    jsAvg: +avg(js).toFixed(2), jsMax: +Math.max(0,...js).toFixed(2),
    layoutAvg: +avg(lay).toFixed(2), layoutMax: +Math.max(0,...lay).toFixed(2)
  };
})()`);
console.log(JSON.stringify({ ...stats, animsMax: Math.max(0, ...anims), anims }, null, 2));
ws.close();
