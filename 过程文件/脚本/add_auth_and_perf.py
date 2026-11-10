# -*- coding: utf-8 -*-
"""加入登录/账号体系，并顺带修掉切换导航的卡顿。

1) 登录层：账号密码登录，未登录时锁屏；退出登录。
2) 初始化账号组：教师 1、学生 2、裁定者 1（密码 123456）。
3) 教师专属「账号管理」模块：创建新账号。
4) 顶栏去掉"随意切换身份"的下拉，改成当前账号 + 退出。
5) 卡顿：把模块入场动画从"整块 #view transform + 强制回流"改成
   WAAPI 只动 4 个元素、不触发布局；工作台不做入场动画。
"""
import io
import re
import sys

P = r'C:\Users\32354\Documents\deepseek-harness\default-workspace\法律论证标注系统\过程文件\输出\legal-annotation-prototype.html'
s = io.open(P, encoding='utf-8').read()

if 'id="auth-js"' in s:
    print('登录体系已存在，未重复写入')
    sys.exit(0)

# ---------------- 1) 顶栏：身份下拉 → 当前账号 + 退出 ----------------
pat = re.compile(r'<span class="who"><select aria-label="演示身份"[^>]*>.*?</select></span>', re.S)
m = pat.search(s)
if not m:
    print('未找到顶栏身份下拉，未改动')
    sys.exit(1)
print('将替换的顶部栏片段长度:', len(m.group(0)))
CHIP = ("<span class=\"who\" id=\"whoChip\"><span class=\"who-dot\"></span>' + esc(state.user) + "
        "' <span class=\"who-role\">' + esc(state.role) + '</span></span>"
        "<button class=\"ghost\" title=\"退出登录\" onclick=\"logout()\">退出</button>")
s = s[:m.start()] + CHIP + s[m.end():]

# ---------------- 2) NAV 增加「账号管理」 ----------------
NAV_ANCHOR = "['ledger','台账与记录']];"
if NAV_ANCHOR not in s:
    print('未找到 NAV 结尾，未改动')
    sys.exit(1)
s = s.replace(NAV_ANCHOR, "['ledger','台账与记录'],['accounts','账号管理']];", 1)

# 教师角色可见该模块
s = s.replace("'教师': ['overview','guide','task','work','adj','quality','teach','exp','ledger'],",
              "'教师': ['overview','guide','task','work','adj','quality','teach','exp','ledger','accounts'],", 1)

# ---------------- 3) 登录样式 ----------------
CSS = r"""
<style id="auth-css">
body.auth-locked .shell{filter:saturate(.85) blur(2px);pointer-events:none;user-select:none}
#loginLayer{position:fixed;inset:0;z-index:10000;display:none;place-items:center;
  background:radial-gradient(60% 60% at 50% 20%,#eef3e6 0%,#e7ecdf 45%,#dfe5d6 100%)}
#loginLayer.on{display:grid}
.login-card{width:min(430px,92vw);background:#fffefa;border:1px solid #e3e7da;border-radius:18px;
  padding:30px 30px 24px;box-shadow:0 30px 80px -30px rgba(32,54,38,.45);animation:uxDialog .3s cubic-bezier(.22,.9,.3,1.02) both}
.login-brand{display:flex;align-items:center;gap:12px;margin-bottom:18px}
.login-brand b{display:block;font-size:18px;letter-spacing:2px;color:#2e5041}
.login-brand small{display:block;font-size:9px;letter-spacing:2.4px;color:#8a9286;margin-top:2px}
.login-card h2{font-size:20px;margin:0 0 4px;color:#26382c}
.login-form{display:grid;gap:12px;margin:18px 0 8px}
.login-form label{display:grid;gap:6px;font-size:12px;color:#61705f}
.login-form input{padding:10px 12px;border-radius:9px;border:1px solid #d9dfd3;background:#fff;font-size:13px}
.login-form input:focus{outline:none;border-color:#9fb590;box-shadow:0 0 0 4px rgba(126,155,116,.16)}
.login-err{margin:0;color:#a2452c;font-size:12px}
.login-accounts{margin-top:18px;border-top:1px dashed #e3e7da;padding-top:14px;display:grid;gap:7px}
.acc-row{display:flex;gap:10px;align-items:center;font-size:11px;color:#6a7466}
.acc-row b{color:#2f4a3a;font-weight:500;min-width:52px}
.acc-row .pill{font-size:10px;padding:1px 7px}
.who-dot{display:inline-block;width:6px;height:6px;border-radius:50%;background:#7f9a75;margin-right:6px}
.who-role{color:#8a9286;font-size:11px}
</style>
"""

# ---------------- 4) 登录/账号脚本 ----------------
JS = r"""
<script id="auth-js">
(function(){
  "use strict";
  var ACC_KEY = 'legal-annotation-accounts-v1';
  var SESSION_KEY = 'legal-annotation-session-v1';
  var SEED = [
    { id:'u-teacher', name:'王老师', account:'teacher', pass:'123456', role:'教师',   at:'2026-10-20 09:00' },
    { id:'u-stu1',    name:'学生甲', account:'stu01',   pass:'123456', role:'学生',   at:'2026-10-20 09:00' },
    { id:'u-stu2',    name:'学生乙', account:'stu02',   pass:'123456', role:'学生',   at:'2026-10-20 09:00' },
    { id:'u-judge',   name:'赵博士', account:'judge',   pass:'123456', role:'裁定者', at:'2026-10-20 09:00' }
  ];
  function readAccounts(){
    try {
      var a = JSON.parse(localStorage.getItem(ACC_KEY) || 'null');
      if (Array.isArray(a) && a.length) return a;
    } catch (e) {}
    var seed = SEED.map(function(x){ return { id:x.id, name:x.name, account:x.account, pass:x.pass, role:x.role, at:x.at }; });
    try { localStorage.setItem(ACC_KEY, JSON.stringify(seed)); } catch (e) {}
    return seed;
  }
  var accounts = readAccounts();
  function saveAccounts(){ try { localStorage.setItem(ACC_KEY, JSON.stringify(accounts)); } catch (e) {} }
  function findById(id){ return accounts.filter(function(a){ return a.id === id; })[0] || null; }
  function readSession(){
    try {
      var raw = JSON.parse(localStorage.getItem(SESSION_KEY) || 'null');
      if (!raw || !raw.id) return null;
      return findById(raw.id);
    } catch (e) { return null; }
  }
  function saveSession(a){ try { localStorage.setItem(SESSION_KEY, JSON.stringify({ id:a.id, at:Date.now() })); } catch (e) {} }
  function clearSession(){ try { localStorage.removeItem(SESSION_KEY); } catch (e) {} }

  function applySession(a){
    state.role = a.role;
    state.user = a.name;
    if (a.role === '学生') state.currentVersion = state.versions.practice ? 'practice' : 'A';
  }
  window.applySession = applySession;
  window.currentAccount = readSession;

  /* ---------- 登录层 ---------- */
  function loginHTML(err){
    var rows = accounts.map(function(a){
      return '<div class="acc-row"><b>' + esc(a.name) + '</b><span class="mono">' + esc(a.account) +
             '</span><span class="pill">' + esc(a.role) + '</span><span>密码 ' + esc(a.pass) + '</span></div>';
    }).join('');
    return '<div class="login-card">' +
      '<div class="login-brand"><span class="brand-mark">衡</span><div><b>明理</b><small>LEGAL ANNOTATION STUDIO</small></div></div>' +
      '<h2>登录工作空间</h2><p class="tiny" style="margin:0">账号由教师创建；登录后进入与身份对应的工作空间。</p>' +
      '<div class="login-form">' +
      '<label>账号<input id="loginAcc" autocomplete="username" placeholder="例如 teacher"></label>' +
      '<label>密码<input id="loginPass" type="password" autocomplete="current-password" placeholder="演示密码 123456"></label>' +
      (err ? '<p class="login-err">' + esc(err) + '</p>' : '') +
      '<button class="primary" style="width:100%" onclick="doLogin()">登录</button>' +
      '</div>' +
      '<div class="login-accounts"><div class="tiny" style="margin-bottom:2px">初始化账号组</div>' + rows + '</div>' +
      '</div>';
  }
  function layer(){
    var el = document.getElementById('loginLayer');
    if (!el) {
      el = document.createElement('div');
      el.id = 'loginLayer';
      el.setAttribute('role', 'dialog');
      el.setAttribute('aria-modal', 'true');
      el.setAttribute('aria-label', '登录');
      document.body.appendChild(el);
    }
    return el;
  }
  window.showLogin = function(err){
    var el = layer();
    el.innerHTML = loginHTML(err);
    el.classList.add('on');
    document.body.classList.add('auth-locked');
    var i = document.getElementById('loginAcc');
    if (i) window.setTimeout(function(){ try { i.focus(); } catch (e) {} }, 60);
  };
  window.hideLogin = function(){
    var el = document.getElementById('loginLayer');
    if (el) el.classList.remove('on');
    document.body.classList.remove('auth-locked');
  };
  window.doLogin = function(){
    var accEl = document.getElementById('loginAcc'), pwdEl = document.getElementById('loginPass');
    var acc = (accEl ? accEl.value : '').trim();
    var pwd = (pwdEl ? pwdEl.value : '').trim();
    var hit = accounts.filter(function(a){
      return a.account.toLowerCase() === acc.toLowerCase() && a.pass === pwd;
    })[0];
    if (!hit) { showLogin('账号或密码不正确，请重试。'); return; }
    saveSession(hit);
    applySession(hit);
    hideLogin();
    render();
    try { notice('欢迎回来，' + hit.name + '（' + hit.role + '）'); } catch (e) {}
  };
  window.logout = function(){
    clearSession();
    showLogin();
    try { notice('已退出登录'); } catch (e) {}
  };

  /* ---------- 教师：账号管理 ---------- */
  window.viewAccounts = function(){
    var rows = accounts.map(function(a){
      return '<tr><td>' + esc(a.name) + '</td><td><span class="mono">' + esc(a.account) +
             '</span></td><td><span class="pill">' + esc(a.role) + '</span></td><td>' + esc(a.at || '') + '</td></tr>';
    }).join('');
    return '<div class="page-heading"><div class="eyebrow">ACCOUNTS</div><h1>账号管理</h1>' +
      '<p>教师为班级创建账号；学生与裁定者用各自账号登录，进入各自的工作空间。</p></div>' +
      '<div class="card"><h3>新建账号</h3><div class="row">' +
      '<label class="tiny">姓名<input id="naName" placeholder="例如 学生丙" style="display:block;margin-top:6px"></label>' +
      '<label class="tiny">账号<input id="naAcc" placeholder="例如 stu03" style="display:block;margin-top:6px"></label>' +
      '<label class="tiny">初始密码<input id="naPass" value="123456" style="display:block;margin-top:6px"></label>' +
      '<label class="tiny">角色<select id="naRole" style="display:block;margin-top:6px"><option>学生</option><option>裁定者</option><option>教师</option></select></label>' +
      '</div><p><button class="primary" onclick="createAccount()">创建账号</button></p>' +
      '<p class="tiny">原型把账号保存在本浏览器；密码仅用于演示，未做加密。</p></div>' +
      '<div class="card"><h3>已有账号（' + accounts.length + '）</h3><table><tr><th>姓名</th><th>账号</th><th>角色</th><th>创建时间</th></tr>' + rows + '</table></div>';
  };
  window.createAccount = function(){
    if (state.role !== '教师') { notice('只有教师可以创建账号。'); return; }
    var n = document.getElementById('naName'), a = document.getElementById('naAcc');
    var p = document.getElementById('naPass'), r = document.getElementById('naRole');
    var name = (n ? n.value : '').trim(), acc = (a ? a.value : '').trim();
    var pass = (p ? p.value : '').trim(), role = r ? r.value : '学生';
    if (!name || !acc || !pass) { notice('请填写姓名、账号和初始密码。'); return; }
    if (pass.length < 6) { notice('初始密码至少 6 位。'); return; }
    if (accounts.some(function(x){ return x.account.toLowerCase() === acc.toLowerCase(); })) {
      notice('该账号已存在，请换一个。'); return;
    }
    accounts.push({ id:'u-' + Date.now(), name:name, account:acc, pass:pass, role:role, at:nowStr() });
    saveAccounts();
    render();
    notice('已创建账号：' + acc + '（' + role + '）');
  };

  /* ---------- 注册视图（VIEWS 是字面量快照，必须回写） ---------- */
  if (window.VIEWS) VIEWS.accounts = window.viewAccounts;
  if (typeof icons !== 'undefined' && icons) {
    icons[9] = 'M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8Z M4 21c0-4 4-6 8-6s8 2 8 6';
  }

  /* ---------- 重置演示数据后自愈：把登录身份写回来 ---------- */
  var healing = 0;
  var baseRender = window.render;
  window.render = function(){
    var out = baseRender.apply(this, arguments);
    var acc = readSession();
    if (acc && healing === 0 && (state.role !== acc.role || state.user !== acc.name)) {
      healing = 1;
      state.role = acc.role;
      state.user = acc.name;
      window.setTimeout(function(){ healing = 0; if (typeof render === 'function') render(); }, 0);
    }
    return out;
  };

  /* ---------- 启动 ---------- */
  var session = readSession();
  if (session) {
    applySession(session);
    render();
  } else {
    showLogin();
  }
  window.addEventListener('keydown', function(e){
    var el = document.getElementById('loginLayer');
    if (!el || !el.classList.contains('on')) return;
    if (e.key === 'Enter') { e.preventDefault(); doLogin(); }
  });
})();
</script>
"""

# ---------------- 5) 卡顿优化：替换 ux-motion 的入场动画 ----------------
OLD_PLAYIN_START = '  function playIn(){'
i0 = s.find(OLD_PLAYIN_START)
i1 = s.find('  if (typeof window.render === "function") {', i0)
if i0 < 0 or i1 < 0:
    print('未找到入场动画函数，跳过动画优化')
else:
    NEW_PLAYIN = """  function playIn(){
    var view = doc.getElementById("view");
    if (!view || calm() || !view.animate) return;
    if (view.classList.contains("work-view")) return;
    var list = view.querySelectorAll(".page-heading, .card");
    var n = Math.min(list.length, 4), i;
    for (i = 0; i < n; i++) {
      var a = list[i].animate(
        [{ opacity: 0, transform: "translateY(8px)" }, { opacity: 1, transform: "none" }],
        { duration: 220, delay: i * 26, easing: "cubic-bezier(.22,.8,.26,1)", fill: "both" }
      );
      if (a) a.onfinish = (function(anim){ return function(){ try { anim.cancel(); } catch (e) {} }; })(a);
    }
  }
"""
    s = s[:i0] + NEW_PLAYIN + s[i1:]
    print('入场动画已替换为 WAAPI 轻量版')

# 点击回弹不再强制回流
OLD_CLICK = '    b.classList.remove("ux-press");\n    void b.offsetWidth;\n    b.classList.add("ux-press");'
NEW_CLICK = '    b.classList.remove("ux-press");\n    window.requestAnimationFrame(function(){ b.classList.add("ux-press"); });'
if OLD_CLICK in s:
    s = s.replace(OLD_CLICK, NEW_CLICK, 1)
    print('点击回弹已去掉强制回流')

# ---------------- 6) 写入 ----------------
if '</body>' not in s:
    print('未找到 </body>，未改动')
    sys.exit(1)
s = s.replace('</body>', CSS + JS + '</body>', 1)

io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('已写入登录体系与卡顿优化')
