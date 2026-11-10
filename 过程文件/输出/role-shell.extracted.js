
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
