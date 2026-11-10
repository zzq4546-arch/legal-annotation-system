#!/usr/bin/env node
/** 验证登录/账号体系：未登录锁屏、登录成功、教师建号、新号可登录、退出。 */
import { writeFileSync } from 'node:fs';

const PORT = Number(process.env.CDP_PORT || 9222);
const URL = process.argv[2];
const OUT = process.argv[3] || '.';
const list = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
const page = list.find(t => t.type === 'page');
const ws = new WebSocket(page.webSocketDebuggerUrl);
let id = 0; const pending = new Map(); const errors = []; const logs = [];
ws.addEventListener('message', ev => {
  const m = JSON.parse(ev.data);
  if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); return; }
  if (m.method === 'Runtime.exceptionThrown') errors.push((m.params.exceptionDetails.exception || {}).description || 'err');
  if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') logs.push(m.params.args.map(a => a.value ?? a.description ?? '').join(' '));
});
await new Promise(r => ws.addEventListener('open', r));
const sleep = ms => new Promise(r => setTimeout(r, ms));
const send = (method, params) => { const i = ++id; return new Promise(res => { pending.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); }); };
async function ev(expression) {
  const r = await send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
  if (r.result && r.result.exceptionDetails) throw new Error(r.result.exceptionDetails.text);
  return r.result && r.result.result ? r.result.result.value : undefined;
}
async function shot(name) {
  const s = await send('Page.captureScreenshot', { format: 'png' });
  if (s.result && s.result.data) { writeFileSync(name, Buffer.from(s.result.data, 'base64')); console.log('saved', name); }
}

await send('Runtime.enable');
await send('Emulation.setDeviceMetricsOverride', { width: 1500, height: 950, deviceScaleFactor: 1, mobile: false });
await send('Page.navigate', { url: 'about:blank' });
await sleep(150);
await send('Page.navigate', { url: URL });
await sleep(900);
await ev('localStorage.clear()');
await send('Page.navigate', { url: 'about:blank' });
await sleep(150);
await send('Page.navigate', { url: URL });
await sleep(1500);

const out = {};
out.loginShownInitially = await ev(`!!document.getElementById('loginLayer') && document.getElementById('loginLayer').classList.contains('on')`);
out.bodyLocked = await ev(`document.body.classList.contains('auth-locked')`);
out.seedAccounts = await ev(`JSON.parse(localStorage.getItem('legal-annotation-accounts-v1')||'[]').map(a=>a.account+':'+a.role)`);
await shot(OUT + '/auth-login.png');

// 登录教师
await ev(`document.getElementById('loginAcc').value='teacher'; document.getElementById('loginPass').value='123456'; doLogin();`);
await sleep(600);
out.afterTeacherLogin = await ev(`({
  loginHidden: !document.getElementById('loginLayer').classList.contains('on'),
  role: state.role, user: state.user,
  navCount: document.querySelectorAll('.rail button:not(.aux)').length,
  hasAccountsNav: [...document.querySelectorAll('.rail button')].some(b => (b.textContent||'').includes('账号管理')),
  chip: (document.getElementById('whoChip')?.textContent||'').trim()
})`);
await shot(OUT + '/auth-teacher.png');

// 教师创建账号
await ev(`setMod('accounts')`);
await sleep(500);
out.accountsView = await ev(`({ cards: document.querySelectorAll('#view .card').length, rows: document.querySelectorAll('#view table tr').length })`);
await ev(`
  document.getElementById('naName').value='学生丙';
  document.getElementById('naAcc').value='stu03';
  document.getElementById('naPass').value='654321';
  document.getElementById('naRole').value='学生';
  createAccount();
`);
await sleep(500);
out.afterCreate = await ev(`JSON.parse(localStorage.getItem('legal-annotation-accounts-v1')||'[]').map(a=>a.account)`);
await shot(OUT + '/auth-accounts.png');

// 退出 + 新账号登录
await ev('logout()');
await sleep(400);
out.afterLogout = await ev(`document.getElementById('loginLayer').classList.contains('on')`);
await ev(`document.getElementById('loginAcc').value='stu03'; document.getElementById('loginPass').value='654321'; doLogin();`);
await sleep(600);
out.studentLogin = await ev(`({ role: state.role, user: state.user, mod: state.mod, navCount: document.querySelectorAll('.rail button:not(.aux)').length })`);
await shot(OUT + '/auth-student.png');

// 错误密码
await ev('logout()');
await sleep(300);
await ev(`document.getElementById('loginAcc').value='teacher'; document.getElementById('loginPass').value='wrong'; doLogin();`);
await sleep(400);
out.badPassword = await ev(`({ stillLocked: document.getElementById('loginLayer').classList.contains('on'), hasError: !!document.querySelector('.login-err') })`);

out.errors = errors; out.consoleErrors = logs;
out.verdict = (out.loginShownInitially && out.bodyLocked && out.afterTeacherLogin.loginHidden
  && out.afterTeacherLogin.role === '教师' && out.afterTeacherLogin.hasAccountsNav
  && out.afterCreate.includes('stu03')
  && out.afterLogout && out.studentLogin.role === '学生' && out.studentLogin.navCount === 5
  && out.badPassword.stillLocked && !errors.length && !logs.length) ? 'PASS' : 'CHECK';
console.log(JSON.stringify(out, null, 2));
ws.close();
