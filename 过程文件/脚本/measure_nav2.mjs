#!/usr/bin/env node
/** 测切换导航的 JS 时间与样式/布局时间（优化前后对比用）。 */
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
// 登录层会挡住点击，但 setMod 是程序调用，不影响测量；先确保在教师身份
await ev(`try{ if(document.getElementById('loginLayer')) hideLogin(); }catch(e){}`);

const mods = ['overview', 'guide', 'task', 'adj', 'quality', 'teach', 'exp', 'ledger'];
const rows = [];
for (const m of mods) {
  const r = await ev(`(() => {
    const t0 = performance.now();
    setMod(${JSON.stringify(m)});
    const t1 = performance.now();
    document.documentElement.offsetHeight;
    const t2 = performance.now();
    return { js: +(t1 - t0).toFixed(2), layout: +(t2 - t1).toFixed(2) };
  })()`);
  await sleep(120);
  rows.push({ mod: m, js: r.js, layout: r.layout });
}
const avg = k => +(rows.reduce((a, b) => a + b[k], 0) / rows.length).toFixed(2);
const max = k => +Math.max(...rows.map(r => r[k])).toFixed(2);
console.log(JSON.stringify({ rows, avgJs: avg('js'), maxJs: max('js'), avgLayout: avg('layout'), maxLayout: max('layout') }, null, 2));
ws.close();
