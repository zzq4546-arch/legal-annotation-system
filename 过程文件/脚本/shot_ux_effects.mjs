#!/usr/bin/env node
/** 拍效果图：悬停上浮、点击涟漪、提示条、模块切场。 */
import { writeFileSync } from 'node:fs';

const PORT = Number(process.env.CDP_PORT || 9222);
const BASE = process.argv[2];
const OUT = process.argv[3] || '.';

const list = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
const page = list.find(t => t.type === 'page');
const ws = new WebSocket(page.webSocketDebuggerUrl);
let id = 0; const pending = new Map();
ws.addEventListener('message', ev => {
  const m = JSON.parse(ev.data);
  if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
});
await new Promise(r => ws.addEventListener('open', r));
const sleep = ms => new Promise(r => setTimeout(r, ms));
const send = (method, params) => { const i = ++id; return new Promise(res => { pending.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); }); };
async function ev(expression) {
  const r = await send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
  return r.result && r.result.result ? r.result.result.value : undefined;
}
async function shot(name) {
  const s = await send('Page.captureScreenshot', { format: 'png' });
  if (s.result && s.result.data) {
    writeFileSync(name, Buffer.from(s.result.data, 'base64'));
    console.log('saved', name);
  }
}

await send('Emulation.setDeviceMetricsOverride', { width: 1500, height: 950, deviceScaleFactor: 1, mobile: false });
await send('Page.navigate', { url: BASE + '#overview' });
await sleep(900);
await send('Runtime.evaluate', { expression: 'try{localStorage.clear()}catch(e){}' });
await send('Page.navigate', { url: BASE + '#overview' });
await sleep(1400);

// 找到首屏主按钮坐标
const b = await ev(`(() => {
  const el = [...document.querySelectorAll('#view button')].find(x => (x.textContent||'').includes('继续标注'));
  if (!el) return null;
  const r = el.getBoundingClientRect();
  return { x: r.left + r.width/2, y: r.top + r.height/2 };
})()`);

// 1) 悬停 + 提示条
if (b) await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: b.x, y: b.y });
await ev('notice("✓ 已保存到此浏览器")');
await sleep(500);
await shot(OUT + '/ux-hover-toast.png');

// 2) 按下涟漪（截图在动画中段）
if (b) {
  await send('Input.dispatchMouseEvent', { type: 'mousePressed', x: b.x, y: b.y, button: 'left', clickCount: 1 });
  await sleep(130);
  await shot(OUT + '/ux-ripple.png');
  await send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: b.x, y: b.y, button: 'left', clickCount: 1 });
}

// 3) 模块切换的入场动画（截在动画过程中）
await ev(`(() => { const x=[...document.querySelectorAll('.rail button')].find(n=>(n.textContent||'').includes('任务')); if(x) x.click(); })()`);
await sleep(170);
await shot(OUT + '/ux-view-enter.png');
await sleep(900);

ws.close();
