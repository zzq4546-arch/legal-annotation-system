#!/usr/bin/env node
/** 真实浏览器里验证交互动效层：涟漪、按压、模块切换、提示条、控制台异常。 */
import { writeFileSync } from 'node:fs';

const PORT = Number(process.env.CDP_PORT || 9222);
const URL = process.argv[2];
if (!URL) { console.error('用法: node verify_ux.mjs <file-url>'); process.exit(1); }

const list = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
const page = list.find(t => t.type === 'page');
if (!page) { console.error('没有页面目标'); process.exit(1); }

const ws = new WebSocket(page.webSocketDebuggerUrl);
let id = 0;
const pending = new Map();
const errors = [];
const logs = [];
ws.addEventListener('message', ev => {
  const m = JSON.parse(ev.data);
  if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); return; }
  if (m.method === 'Runtime.exceptionThrown') {
    const d = m.params.exceptionDetails;
    errors.push((d.exception && d.exception.description) || d.text || 'unknown');
  }
  if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') {
    logs.push(m.params.args.map(a => a.value ?? a.description ?? '').join(' '));
  }
});
await new Promise(r => ws.addEventListener('open', r));
const sleep = ms => new Promise(r => setTimeout(r, ms));
function send(method, params) {
  const i = ++id;
  return new Promise(resolve => { pending.set(i, resolve); ws.send(JSON.stringify({ id: i, method, params })); });
}
async function evaluate(expression) {
  const r = await send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
  if (r.result && r.result.exceptionDetails) throw new Error(r.result.exceptionDetails.text);
  if (r.result && r.result.result) return r.result.result.value;
  return undefined;
}

await send('Runtime.enable');
await send('Emulation.setDeviceMetricsOverride', { width: 1500, height: 950, deviceScaleFactor: 1, mobile: false });

// 干净的初始状态
await send('Page.navigate', { url: URL });
await sleep(900);
await send('Runtime.evaluate', { expression: 'try{localStorage.clear()}catch(e){}' });
await send('Page.navigate', { url: URL });
await sleep(1400);

const out = {};

out.motionScriptPresent = await evaluate('!!document.getElementById("ux-motion-js")');
out.motionStylePresent = await evaluate('!!document.getElementById("ux-motion-v1")');
out.renderWrapped = await evaluate('typeof window.render === "function"');
out.buttonCount = await evaluate('document.querySelectorAll("button").length');

// 1) 提示条：补全的样式是否生效
out.snackbarBefore = await evaluate('!!document.getElementById("snackbar")');
await evaluate('notice("交互测试：状态已保存")');
await sleep(420);
out.snackbar = await evaluate(`(() => {
  const el = document.getElementById('snackbar');
  if (!el) return null;
  const cs = getComputedStyle(el);
  return { position: cs.position, opacity: Number(cs.opacity), bottom: cs.bottom,
           hasShow: el.classList.contains('show'), text: el.textContent };
})()`);

// 2) 真实点击一个可见按钮，检查涟漪与按压类
const btn = await evaluate(`(() => {
  const b = [...document.querySelectorAll('#view button, .topbar button')]
    .find(x => { const r = x.getBoundingClientRect(); return r.width > 40 && r.height > 20 && r.top > 0 && r.top < 900; });
  if (!b) return null;
  const r = b.getBoundingClientRect();
  return { x: r.left + r.width / 2, y: r.top + r.height / 2, tag: b.tagName, text: (b.textContent || '').trim().slice(0, 18) };
})()`);
if (btn) {
  await send('Input.dispatchMouseEvent', { type: 'mousePressed', x: btn.x, y: btn.y, button: 'left', clickCount: 1 });
  await sleep(90);
  out.rippleAfterPointerDown = await evaluate('document.querySelectorAll(".ux-ripple").length');
  await send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: btn.x, y: btn.y, button: 'left', clickCount: 1 });
  await sleep(60);
  out.pressClassAfterClick = await evaluate(`(() => {
    const b = [...document.querySelectorAll('#view button, .topbar button')].find(x => x.classList.contains('ux-press'));
    return b ? (b.textContent || '').trim().slice(0, 18) : null;
  })()`);
  out.clickedButton = btn.text;
  await sleep(400);
  out.rippleCleanedUp = await evaluate('document.querySelectorAll(".ux-ripple").length === 0');
}

// 3) 切换模块：淡入 + 错峰
await evaluate(`(() => {
  const b = [...document.querySelectorAll('.rail button')].find(x => (x.textContent || '').includes('任务'));
  if (b) b.click();
  return !!b;
})()`);
await sleep(180);
out.viewIn = await evaluate('document.getElementById("view").classList.contains("ux-view-in")');
out.riseCount = await evaluate('document.querySelectorAll("#view .ux-rise").length');
out.moduleNow = await evaluate('location.hash');
await sleep(1200);

// 4) 断言：动效结束后类已清理
out.riseCleanedUp = await evaluate('document.querySelectorAll("#view .ux-rise").length === 0');
out.viewInCleanedUp = await evaluate('!document.getElementById("view").classList.contains("ux-view-in")');

// 5) 对话框：打开时是否应用了动画
await evaluate('toast("动效测试","<p class=\\"muted\\">对话框打开动效</p>")');
await sleep(320);
out.dialog = await evaluate(`(() => {
  const d = document.getElementById('dlg');
  if (!d) return null;
  const cs = getComputedStyle(d);
  return { open: d.open, animationName: cs.animationName, animationDuration: cs.animationDuration };
})()`);
await evaluate('closeDlg()');

// 6) 结构没有被动过：关键容器数量
out.structure = await evaluate(`({
  nav: document.querySelectorAll('.rail button').length,
  cards: document.querySelectorAll('.card').length,
  panes: document.querySelectorAll('.pane-body').length,
  reducedMotionRule: [...document.styleSheets].some(s => { try { return [...s.cssRules].some(r => r.conditionText && /prefers-reduced-motion/.test(r.conditionText)); } catch { return false; } })
})`);

out.consoleErrors = logs;
out.exceptions = errors;
out.verdict = (!errors.length && !logs.length && out.motionScriptPresent && out.renderWrapped
  && out.rippleAfterPointerDown > 0 && out.pressClassAfterClick
  && out.viewIn && out.riseCount > 0 && out.snackbar && out.snackbar.hasShow
  && out.dialog && out.dialog.animationName !== 'none') ? 'PASS' : 'CHECK';

console.log(JSON.stringify(out, null, 2));

// 截图留档
for (const [hash, file] of [['#overview', 'ux-overview.png'], ['#work', 'ux-work.png']]) {
  await send('Page.navigate', { url: URL.split('#')[0] + hash });
  await sleep(1100);
  const shot = await send('Page.captureScreenshot', { format: 'png' });
  if (shot.result && shot.result.data) {
    writeFileSync(file, Buffer.from(shot.result.data, 'base64'));
    console.log('saved', file);
  }
}
ws.close();
