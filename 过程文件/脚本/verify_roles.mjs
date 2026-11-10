#!/usr/bin/env node
/** 验证分角色页面：导航数量、落地首页、越权拦截、学生写入限制、控制台异常。 */
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
await sleep(200);
await send('Page.navigate', { url: URL });
await sleep(900);
await send('Runtime.evaluate', { expression: 'try{localStorage.clear()}catch(e){}' });
await send('Page.navigate', { url: 'about:blank' });
await sleep(200);
await send('Page.navigate', { url: URL });
await sleep(1500);

const result = { roles: {} };

for (const role of ['教师', '学生', '裁定者']) {
  await ev(`switchRole(${JSON.stringify(role)})`);
  await sleep(600);
  result.roles[role] = await ev(`(() => {
    const navs = [...document.querySelectorAll('.rail button')].filter(b => !b.classList.contains('aux')).map(b => (b.textContent||'').trim());
    return {
      hash: location.hash,
      mod: state.mod,
      navCount: navs.length,
      nav: navs,
      bannerTitle: (document.querySelector('.role-banner h3')?.textContent || '').trim(),
      heading: (document.querySelector('#view .page-heading h1, #view h1')?.textContent || '').trim().slice(0, 30),
      cards: document.querySelectorAll('#view .card').length
    };
  })()`);
  await shot(OUT + '/role-' + encodeURIComponent(role) + '.png');
}

// 越权：学生访问任务管理
await ev(`switchRole('学生')`);
await sleep(400);
await ev(`setMod('task')`);
await sleep(400);
result.studentBlocked = await ev(`({ hash: location.hash, mod: state.mod })`);

// 学生写入限制
result.studentWritable = await ev(`(() => {
  state.currentVersion = 'A';
  return { onMain: writable() };
})()`);
result.studentWritablePractice = await ev(`(() => {
  if (!state.versions.practice) state.versions.practice = { by: '我的独立练习', props: [], rels: [], pos: null, submitted: false };
  state.currentVersion = 'practice';
  return { onPractice: writable() };
})()`);

// 教师写入
await ev(`switchRole('教师')`);
await sleep(400);
result.teacherWritable = await ev(`(() => { state.currentVersion='A'; return writable(); })()`);

result.errors = errors;
result.consoleErrors = logs;
result.verdict = (!errors.length && !logs.length
  && result.roles['教师'].navCount === 9
  && result.roles['学生'].navCount === 5
  && result.roles['裁定者'].navCount === 5
  && result.roles['教师'].mod === 'overview'
  && result.roles['学生'].mod === 'teach'
  && result.roles['裁定者'].mod === 'adj'
  && result.studentBlocked.mod === 'teach'
  && result.studentWritable.onMain === false
  && result.studentWritablePractice.onPractice === true
  && result.teacherWritable === true) ? 'PASS' : 'CHECK';

console.log(JSON.stringify(result, null, 2));
ws.close();
