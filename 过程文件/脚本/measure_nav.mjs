#!/usr/bin/env node
/** 测量切换导航的耗时与长任务（用于优化前后对比）。 */
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
await sleep(1400);

// 埋点：记录 render 耗时 + 长任务
await ev(`(() => {
  window.__renderMs = [];
  window.__long = [];
  try {
    new PerformanceObserver(list => {
      for (const e of list.getEntries()) window.__long.push(Math.round(e.duration));
    }).observe({ entryTypes: ['longtask'] });
  } catch (err) {}
  if (!window.__wrappedRender) {
    const base = window.render;
    window.__wrappedRender = true;
    window.render = function(){
      const t0 = performance.now();
      const out = base.apply(this, arguments);
      window.__renderMs.push(performance.now() - t0);
      return out;
    };
  }
  return true;
})()`);

const mods = ['overview', 'guide', 'task', 'work', 'adj', 'quality', 'teach', 'exp', 'ledger'];
const per = {};
for (const m of mods) {
  await ev(`window.__renderMs = []; window.__long = [];`);
  for (let i = 0; i < 3; i++) {
    await ev(`setMod('${m}')`);
    await sleep(320);
  }
  per[m] = await ev(`({
    renderAvg: +(window.__renderMs.reduce((a,b)=>a+b,0) / Math.max(1, window.__renderMs.length)).toFixed(1),
    renderMax: +Math.max(0, ...window.__renderMs).toFixed(1),
    longTasks: window.__long.length,
    longMax: window.__long.length ? Math.max(...window.__long) : 0
  })`);
}

const all = await ev(`(() => {
  const html = document.documentElement.outerHTML.length;
  return { domNodes: document.querySelectorAll('*').length, htmlBytes: html };
})()`);

console.log(JSON.stringify({ per, all }, null, 2));
ws.close();
