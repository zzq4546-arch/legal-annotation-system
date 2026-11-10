# -*- coding: utf-8 -*-
"""让原型真正按身份区分：教师 / 学生 / 裁定者 看到不同模块与首页。

依据（需求梳理文档 §2.1 与 F2.9）：
- 任务创建者（教师）：上传、配标签、分配任务、指定裁定者 → 需要全部模块
- 学生：独立入口做练习，结果与标准样例比对，不污染主数据
- 裁定者：查看版本差异、人工比对、裁定最终版本

改动：
1) 新增角色→模块表、首页表、身份标签；
2) 侧栏只渲染该身份可见的模块（图标索引保持原样）；
3) 切换身份进入对应首页；越权访问回首页；
4) 学生只能在自己的「独立练习」版本里改标注；
5) 首页顶部加身份专属入口卡。
"""
import io
import sys

P = r'C:\Users\32354\Documents\deepseek-harness\default-workspace\法律论证标注系统\过程文件\输出\legal-annotation-prototype.html'
MARK = 'role-shell-js'

s = io.open(P, encoding='utf-8').read()
if MARK in s:
    print('已应用过角色分层，未重复写入')
    sys.exit(0)

# ---------- 1) 角色策略表 ----------
ANCHOR_NAV = "['ledger','台账与记录']];"
POLICY = ANCHOR_NAV + r"""

/* ===== 身份 → 可见模块（依据需求文档 §2.1 / F2.9） ===== */
var ROLE_NAV = {
  '教师': ['overview','guide','task','work','adj','quality','teach','exp','ledger'],
  '学生': ['overview','guide','work','teach','ledger'],
  '裁定者': ['overview','work','adj','quality','ledger']
};
var ROLE_HOME = { '教师':'overview', '学生':'teach', '裁定者':'adj' };
var ROLE_TAG  = { '教师':'任务创建 · 教学', '学生':'独立练习', '裁定者':'分歧裁定' };
function roleAllow(){ return ROLE_NAV[state.role] || ROLE_NAV['教师']; }
function canSee(m){ return roleAllow().indexOf(m) >= 0; }
function roleHome(){ return ROLE_HOME[state.role] || 'overview'; }
/* 返回 [模块键, 标题, 原始图标序号]，过滤后图标不错位 */
function visibleNav(){
  var allow = roleAllow(), out = [];
  NAV.forEach(function(n, i){ if (allow.indexOf(n[0]) >= 0) out.push([n[0], n[1], i]); });
  return out;
}"""
if ANCHOR_NAV not in s:
    print('未找到 NAV 结尾，未改动')
    sys.exit(1)
s = s.replace(ANCHOR_NAV, POLICY, 1)

# ---------- 2) 侧栏只渲染可见模块 ----------
OLD_MAP = "'+NAV.map((n,i)=>"
NEW_MAP = "'+visibleNav().map((n,i)=>"
if OLD_MAP not in s:
    print('未找到侧栏渲染语句，未改动')
    sys.exit(1)
s = s.replace(OLD_MAP, NEW_MAP, 1)

OLD_ICO = "+ico(i)+'<span class=\"nav-label\">"
NEW_ICO = "+ico(n[2])+'<span class=\"nav-label\">"
if OLD_ICO not in s:
    print('未找到图标索引，未改动')
    sys.exit(1)
s = s.replace(OLD_ICO, NEW_ICO, 1)

# ---------- 3) 角色行为脚本 ----------
SCRIPT = r"""
<script id="role-shell-js">
(function(){
  "use strict";
  function say(msg){ try { notice(msg); } catch (e) {} }

  /* 切换身份 → 进入该身份首页；学生自动落到练习版本 */
  window.switchRole = function(r){
    state.role = r;
    state.user = (r === '学生') ? '学生甲' : (r === '裁定者') ? '王五'
               : (r === '标注员') ? '张三' : (r === '领域专家') ? '赵博士' : '王老师';
    if (r === '学生') state.currentVersion = state.versions.practice ? 'practice' : 'A';
    state.mod = roleHome();
    if (location.hash !== '#' + state.mod) location.hash = '#' + state.mod;
    else render();
    say('已切换为「' + r + '」身份，进入对应首页');
  };

  /* 越权模块拦截：直接回首页并说明 */
  var baseSetMod = window.setMod;
  window.setMod = function(m){
    var hit = NAV.filter(function(n){ return n[0] === m; })[0];
    var label = hit ? hit[1] : '该模块';
    if (!canSee(m)) {
      say('「' + label + '」不对' + state.role + '开放，已返回首页。');
      m = roleHome();
    }
    /* 学生进工作台：有练习版本就进练习；还没有就先回学习页，避免进到不能改的页面 */
    if (m === 'work' && state.role === '学生') {
      if (state.versions.practice) state.currentVersion = 'practice';
      else { say('请先在「学习与反馈」开始独立练习。'); m = 'teach'; }
    }
    return baseSetMod(m);
  };

  /* 该身份用不了的操作：直接隐藏，而不是留在页面上点了报错 */
  var GATED = {
    '教师': [],
    '学生': ['teacherAnswer','newTaskDialog','doImportGuide','importBack','doExport','simulateUpload','saveText','finalizeAll'],
    '裁定者': ['teacherAnswer','newTaskDialog','doImportGuide','importBack','doExport','simulateUpload','saveText']
  };
  function sweepGated(){
    var hide = GATED[state.role] || [];
    if (!hide.length) return;
    var btns = document.querySelectorAll('#view button[onclick]');
    for (var i = 0; i < btns.length; i++) {
      var oc = btns[i].getAttribute('onclick') || '';
      for (var j = 0; j < hide.length; j++) {
        if (oc.indexOf(hide[j]) >= 0) { btns[i].style.display = 'none'; break; }
      }
    }
  }
  if (typeof window.render === 'function') {
    var baseRender = window.render;
    window.render = function(){
      var out = baseRender.apply(this, arguments);
      try { sweepGated(); } catch (e) {}
      return out;
    };
  }

  /* 学生只能在独立练习版本里改标注 */
  var baseWritable = window.writable;
  window.writable = function(){
    if (state.role === '学生' && state.currentVersion !== 'practice') {
      say('学生身份只能在「独立练习」里标注：请到「学习与反馈」开始练习。');
      return false;
    }
    return baseWritable.apply(this, arguments);
  };

  /* 首页顶部：身份专属入口卡 */
  function roleBanner(){
    var pending = 0;
    try { pending = diffSet().length; } catch (e) {}
    var hasAnswer = !!(state.teaching && state.teaching.answer);
    var h = '<div class="card role-banner" style="border-left:4px solid #526f37">' +
      '<div class="row" style="align-items:center;gap:16px">' +
      '<div style="flex:1;min-width:260px">' +
      '<div class="eyebrow">CURRENT ROLE</div>' +
      '<h3 style="margin:2px 0 6px">' + esc(state.role) +
      '　<span class="pill">' + esc(ROLE_TAG[state.role] || '') + '</span></h3>';
    if (state.role === '学生') {
      h += '<p class="tiny" style="margin:0">你看到的模块只与学习有关。正式标注对你只读，' +
           '练习结果单独保存，不会写进主数据。</p>';
      if (!hasAnswer) h += '<p class="tiny warn" style="margin:6px 0 0">教师尚未发布标准样例，练习将在发布后开放。</p>';
    } else if (state.role === '裁定者') {
      h += '<p class="tiny" style="margin:0">待裁定分歧 <b>' + pending + '</b> 处。你看到的模块只与比对和裁定有关；' +
           '可以直接重标，也可以认可某一方的版本。</p>';
    } else {
      h += '<p class="tiny" style="margin:0">你是任务创建者：可管理指南、创建任务、分配标注员、指定裁定者，' +
           '并查看全部模块。</p>';
    }
    h += '</div><div class="row" style="margin-left:auto">';
    if (state.role === '学生') {
      h += '<button class="primary" onclick="studentDo()">' + (hasAnswer ? '开始/继续独立练习 →' : '独立练习 →') + '</button>' +
           '<button class="ghost" onclick="setMod(\'teach\')">学习与反馈</button>';
    } else if (state.role === '裁定者') {
      h += '<button class="primary" onclick="setMod(\'adj\')">处理待裁定 →</button>' +
           '<button class="ghost" onclick="setMod(\'quality\')">质量看板</button>';
    } else {
      h += '<button class="primary" onclick="setMod(\'task\')">任务管理 →</button>' +
           '<button class="ghost" onclick="setMod(\'guide\')">指南管理</button>';
    }
    return h + '</div></div></div>';
  }

  /* VIEWS 是对象字面量快照，改完函数必须回写，否则不生效 */
  if (typeof viewOverview === 'function' && window.VIEWS) {
    var baseOverview = viewOverview;
    viewOverview = function(){ return roleBanner() + baseOverview(); };
    VIEWS.overview = viewOverview;
  }

  /* 刷新后若当前模块不属于该身份，回首页 */
  try {
    if (!canSee(state.mod)) {
      state.mod = roleHome();
      if (location.hash !== '#' + state.mod) location.hash = '#' + state.mod;
      else render();
    }
  } catch (e) {}
})();
</script>
"""

if '</body>' not in s:
    print('未找到 </body>，未改动')
    sys.exit(1)
s = s.replace('</body>', SCRIPT + '</body>', 1)

io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('角色分层已写入：策略表 + 侧栏过滤 + 身份脚本(%d 字节)' % len(SCRIPT.encode('utf-8')))
