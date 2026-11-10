#!/usr/bin/env node
/** 用三个账号分别登录，验证角色首页与模块差异；并确认自由切换身份已失效。 */
import { writeFileSync } from 'node:fs';
const PORT = Number(process.env.CDP_PORT || 9222);
const URL = process.argv[2];
const OUT = process.argv[3] || '.';
const list = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
const page = list.find(t => t.type === 'page');
const ws = new WebSocket(page.webSocketDebuggerUrl);
let id = 0; const pending = new Map(); const errs = [];
ws.addEventListener('message', ev => { const m = JSON.parse(ev.data); if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); return; } if (m.method === 'Runtime.exceptionThrown') errs.push('err'); });
await new Promise(r => ws.addEventListener('open', r));
const sleep = ms => new Promise(r => setTimeout(r, ms));
const send = (method, params) => { const i = ++id; return new Promise(res => { pending.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); }); };
async function ev(e) { const r = await send('Runtime.evaluate', { expression: e, awaitPromise: true, returnByValue: true }); if (r.result && r.result.exceptionDetails) throw new Error(r.result.exceptionDetails.text); return r.result && r.result.result ? r.result.result.value : undefined; }
async function shot(n) { const s = await send('Page.captureScreenshot', { format: 'png' }); if (s.result && s.result.data) { writeFileSync(n, Buffer.from(s.result.data, 'base64')); console.log('saved', n); } }

await send('Runtime.enable');
await send('Emulation.setDeviceMetricsOverride', { width: 1500, height: 950, deviceScaleFactor: 1, mobile: false });
await send('Page.navigate', { url: 'about:blank' }); await sleep(150);
await send('Page.navigate', { url: URL }); await sleep(900);
await ev('localStorage.clear()');
await send('Page.navigate', { url: 'about:blank' }); await sleep(150);
await send('Page.navigate', { url: URL }); await sleep(1500);

const out = { roles: {} };
for (const [acc, pass] of [['teacher', '123456'], ['stu01', '123456'], ['judge', '123456']]) {
  await ev(`(function(){ if(document.getElementById('loginLayer').classList.contains('on')) return; logout(); })()`);
  await sleep(200);
  await ev(`document.getElementById('loginAcc').value=${JSON.stringify(acc)}; document.getElementById('loginPass').value=${JSON.stringify(pass)}; doLogin();`);
  await sleep(700);
  out.roles[acc] = await ev(`({
    role: state.role, user: state.user, mod: state.mod,
    navCount: document.querySelectorAll('.rail button:not(.aux)').length,
    nav: [...document.querySelectorAll('.rail button:not(.aux)')].map(b=>(b.textContent||'').trim())
  })`);
  await shot(OUT + '/login-' + acc + '.png');
  await ev('logout()'); await sleep(250);
}

// 自由切换是否已失效：直接调 switchRole 应被会话拉回
await ev(`document.getElementById('loginAcc').value='stu01'; document.getElementById('loginPass').value='123456'; doLogin();`);
await sleep(600);
await ev(`switchRole('教师')`);
await sleep(500);
out.freeSwitchBlocked = await ev(`({ role: state.role, user: state.user })`);

out.verdict = (out.roles.teacher.role === '教师' && out.roles.teacher.navCount === 10
  && out.roles.stu01.role === '学生' && out.roles.stu01.navCount === 5 && out.roles.stu01.mod === 'teach'
  && out.roles.judge.role === '裁定者' && out.roles.judge.navCount === 5 && out.roles.judge.mod === 'adj'
  && out.freeSwitchBlocked.role === '学生' && !errs.length) ? 'PASS' : 'CHECK';
console.log(JSON.stringify(out, null, 2));
ws.close();
