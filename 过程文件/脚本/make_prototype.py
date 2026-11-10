# -*- coding: utf-8 -*-
"""Generate the full-featured single-file HTML prototype (v2.0) of the legal-argument annotation system.

Layout follows the requirement doc (stage 2 / 3.1): left = source text + proposition list,
middle = annotation workspace, right = argument diagram. Functionality is NOT limited to the
four stages: guide versioning, task management, teaching mode, quality dashboard, Q&A ledger
and export are all reachable from the module rail.
"""
import base64, os

WS = r'C:\Users\32354\Documents\deepseek-harness\default-workspace'
PROJ = os.path.join(WS, '法律论证标注系统')
OUT = os.path.join(PROJ, '法律论证标注系统-原型.html')
UC_IMG = os.path.join(PROJ, '过程文件', '输出', 'usecase.png')
os.makedirs(os.path.dirname(OUT), exist_ok=True)

with open(UC_IMG, 'rb') as f:
    UC_B64 = base64.b64encode(f.read()).decode('ascii')

CSS = r'''
:root{
  --ink:#1b2a3a;--sub:#6b7784;--line:#d6dee7;--bg:#f2f5f9;--panel:#fff;
  --primary:#1f4e79;--primary-2:#2f6fa8;
  --green:#e3f1e0;--green-b:#4b8b4b;--blue:#e0ebfa;--blue-b:#5a7fb5;
  --pink:#fbe2e2;--pink-b:#c06a6a;--cyan:#dcf0f2;--cyan-b:#3f8b93;--gold:#fdf3d8;--gold-b:#b08b2e;
}
*{box-sizing:border-box}
html,body{height:100%}
body{margin:0;background:var(--bg);color:var(--ink);
     font:13px/1.6 "Microsoft YaHei","PingFang SC","Helvetica Neue",Arial,sans-serif}
h1,h2,h3,h4{margin:0 0 8px}
h3{font-size:15px;color:var(--primary)}
h4{font-size:13.5px;color:var(--primary);margin:12px 0 6px}
a{color:var(--primary-2)}
button{font:inherit;cursor:pointer;border:1px solid var(--line);background:#fff;color:var(--ink);
       border-radius:8px;padding:5px 11px}
button:hover{border-color:var(--primary);color:var(--primary)}
button.primary{background:var(--primary);border-color:var(--primary);color:#fff}
button.primary:hover{opacity:.92;color:#fff}
button.ghost{background:transparent}
button.danger{border-color:#c98b8b;color:#a2452c}
button:disabled{opacity:.45;cursor:not-allowed}
input,select,textarea{font:inherit;color:var(--ink);border:1px solid var(--line);border-radius:7px;
       padding:4px 7px;background:#fff;max-width:100%}
textarea{width:100%;resize:vertical}
label.chk{display:inline-flex;align-items:center;gap:5px;margin:2px 10px 2px 0;font-size:12.5px}
.shell{display:flex;height:100vh;overflow:hidden}
.rail{width:178px;flex:0 0 178px;background:#12283d;color:#cfe0f0;display:flex;flex-direction:column;
      padding:10px 0;overflow:auto}
.rail .brand{padding:4px 14px 10px;font-weight:700;color:#fff;font-size:14px;line-height:1.3}
.rail .brand small{display:block;font-weight:400;color:#8fb0cc;font-size:11px;margin-top:3px}
.rail button{display:block;width:100%;text-align:left;background:transparent;border:0;color:#cfe0f0;
             border-radius:0;padding:9px 14px;font-size:13px;border-left:3px solid transparent}
.rail button:hover{background:#1b3854;color:#fff}
.rail button.on{background:#1f4e79;color:#fff;border-left-color:#7fc4ff;font-weight:600}
.rail .sec{padding:10px 14px 4px;font-size:11px;color:#7fa0bd;letter-spacing:.5px}
.main{flex:1;display:flex;flex-direction:column;min-width:0}
.topbar{display:flex;align-items:center;gap:12px;padding:8px 14px;background:#fff;
        border-bottom:1px solid var(--line);flex-wrap:wrap}
.topbar .who{font-size:12px;color:var(--sub)}
.topbar select{padding:3px 6px}
.wrap{flex:1;overflow:auto;padding:12px 14px 40px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px;margin-bottom:12px}
.row{display:flex;gap:12px;flex-wrap:wrap}
.col{flex:1 1 260px;min-width:200px}
.muted{color:var(--sub);font-size:12.5px}
.tiny{font-size:11.5px;color:var(--sub)}
.mono{font-family:Consolas,"Courier New",monospace}
table{border-collapse:collapse;width:100%;font-size:12.5px}
th,td{border:1px solid var(--line);padding:4px 7px;text-align:left;vertical-align:top}
th{background:#eff4f9;font-weight:600}
.tag{display:inline-block;padding:0 6px;border-radius:9px;font-size:11.5px;border:1px solid transparent;white-space:nowrap}
.tag.SF{background:#e6f4ea;border-color:#79b489;color:#2f6b3d}
.tag.GF{background:#eef6e2;border-color:#9dbb6a;color:#5c7a2a}
.tag.SM{background:#fde8e4;border-color:#d4917f;color:#a2452c}
.tag.SM-C{background:#fde8f4;border-color:#c98fb8;color:#8a2c66}
.tag.GM-L{background:#e6ecfa;border-color:#8397c9;color:#33478a}
.tag.GM-I,.tag.GM-U,.tag.GM-M,.tag.GM-O{background:#eae6fa;border-color:#9a8ec9;color:#4a3f8a}
.tag.IS{background:#fdf3d8;border-color:#c9ad5e;color:#7a5c14}
.tag.Non{background:#eceff2;border-color:#a9b3bd;color:#555f6a}
.pill{display:inline-block;background:#eef3f8;border:1px solid var(--line);border-radius:12px;
      padding:1px 9px;font-size:11.5px;margin:2px 4px 2px 0}
.banner{background:var(--gold);border:1px solid var(--gold-b);border-radius:9px;padding:7px 11px;
        margin-bottom:10px;font-size:12.5px}
.banner.err{background:#fdeaea;border-color:#c06a6a}
.banner.ok{background:#eaf6ea;border-color:#8fbf8f}
.ok{color:#2f6b3d;font-weight:600}.warn{color:#a2452c;font-weight:600}
.work{display:flex;flex:1;height:auto;min-height:0;
      border:1px solid var(--line);border-radius:12px;overflow:hidden;background:#fff}
.work>section{display:flex;flex-direction:column;min-width:0;min-height:0}
.work>section:nth-of-type(1){flex:0 0 26%}
.work>section:nth-of-type(2){flex:0 0 34%}
.work>section:nth-of-type(3){flex:1 1 auto}
.work>section+section{border-left:1px solid var(--line)}
.gutter{width:6px;cursor:col-resize;background:linear-gradient(90deg,#eef3f8,#dde6ef,#eef3f8);
        border-left:1px solid var(--line);border-right:1px solid var(--line);flex:0 0 6px}
.pane-head{padding:6px 10px;border-bottom:1px solid var(--line);font-weight:600;color:var(--primary);
           font-size:12.5px;display:flex;justify-content:space-between;align-items:center;gap:8px;background:#f8fbfe}
.pane-body{padding:9px 10px;overflow:auto;flex:1;min-height:0}
.pane-foot{padding:7px 10px;border-top:1px solid var(--line);background:#fbfdff;display:flex;
           gap:6px;flex-wrap:wrap;align-items:center}
#srcText{font-family:Consolas,"Courier New",monospace;font-size:14.5px;line-height:2.15;
         white-space:pre-wrap;word-break:break-all;user-select:text;padding:0 2px}
.hl{position:relative;border-radius:4px;cursor:pointer;box-shadow:0 0 0 1px rgba(31,78,121,.16)}
.hl:hover{box-shadow:0 0 0 2px var(--primary)}
.hl .no{position:relative;top:-.62em;font-size:10px;font-weight:700;color:var(--primary);background:#fff;
        padding:0 3px;margin-right:1px;border-radius:6px;border:1px solid #b9c6d4;line-height:14px}
.hl.P1,.hl.P2,.hl.P3,.hl.P7,.hl.P8,.hl.P10,.hl.P11{background:rgba(120,170,220,.30)}
.hl.P4,.hl.P5,.hl.P6,.hl.P9,.hl.P12,.hl.P13{background:rgba(220,140,140,.28)}
.hl.cur{background:#ffe9a8 !important;box-shadow:0 0 0 2px #e0a800}
.plist{display:flex;flex-direction:column;gap:4px}
.pitem{display:flex;gap:6px;align-items:flex-start;border:1px solid var(--line);border-radius:8px;
       padding:4px 6px;background:#fbfdff;cursor:pointer}
.pitem.cur{border-color:var(--primary);box-shadow:0 0 0 2px rgba(31,78,121,.13)}
.pitem .id{font-weight:700;color:var(--primary);min-width:26px;font-family:Consolas,monospace;font-size:12px}
.pitem .tx{flex:1;font-size:12.5px;word-break:break-word}
.pitem .meta{font-size:11px;color:var(--sub);font-family:Consolas,monospace;white-space:nowrap}
#svgHost{position:relative;width:100%;height:100%;min-height:340px;overflow:hidden;background:
   linear-gradient(90deg,rgba(0,0,0,.03) 1px,transparent 1px) 0 0/22px 22px,
   linear-gradient(rgba(0,0,0,.03) 1px,transparent 1px) 0 0/22px 22px,#fff}
#svgHost svg{width:100%;height:100%;display:block;touch-action:none}
.node rect{fill:#fff;stroke:var(--blue-b);stroke-width:1.6;cursor:grab}
.node text{font:700 12px Consolas,monospace;fill:#16273a;pointer-events:none}
.node.sel rect{stroke:#e0a800;stroke-width:2.6}
.rel circle{stroke:#40536a;stroke-width:1.5}
.rel text{font:700 11px Consolas,monospace;fill:#2b3a4a;pointer-events:none}
.edge{stroke:#40536a;stroke-width:1.4;fill:none}
.edge.hi{stroke:#1f4e79;stroke-width:2.4}
.zone{fill:#f7fafd;stroke:#e2e9f1;stroke-width:1}
.zone-t{font:600 10.5px "Microsoft YaHei";fill:#8494a4}
.legend{display:flex;gap:12px;flex-wrap:wrap;font-size:11.5px;color:var(--sub);padding:6px 10px;
        border-top:1px solid var(--line)}
.legend i{display:inline-block;width:11px;height:11px;border-radius:50%;border:1px solid #40536a;
          vertical-align:-1px;margin-right:3px}
.drop{border:2px dashed #b9c6d4;border-radius:11px;padding:20px;text-align:center;background:#fbfdff}
.chips{display:flex;flex-wrap:wrap;gap:5px}
.lblbtn{border-radius:14px;padding:3px 10px;font-size:12px}
.lblbtn.on{background:var(--primary);border-color:var(--primary);color:#fff}
pre{background:#0f1f2e;color:#dbe7f3;padding:10px;border-radius:9px;overflow:auto;font-size:11.5px;line-height:1.5}
dialog{border:0;border-radius:13px;padding:0;max-width:840px;width:92vw;box-shadow:0 18px 46px rgba(0,0,0,.26)}
dialog::backdrop{background:rgba(15,31,46,.45)}
dialog .dh{padding:9px 14px;border-bottom:1px solid var(--line);font-weight:700;color:var(--primary);
           display:flex;justify-content:space-between;align-items:center}
dialog .db{padding:12px 14px;max-height:72vh;overflow:auto}
dialog .df{padding:9px 14px;border-top:1px solid var(--line);display:flex;gap:8px;justify-content:flex-end}
.kv{display:grid;grid-template-columns:132px 1fr;gap:3px 10px;font-size:12.5px}
.kv b{color:#3d5064;font-weight:600}
.diffrow{background:#fff7e6}
.verdict{background:#eef7ee;border:1px solid #8fbf8f;border-radius:9px;padding:9px;margin-top:8px}
.stepper{display:flex;gap:6px;flex-wrap:wrap;font-size:11.5px}
.stepper span{border:1px solid var(--line);border-radius:11px;padding:2px 9px;background:#f6f9fc;cursor:pointer}
.stepper span.on{background:var(--primary);color:#fff;border-color:var(--primary)}
.split2{display:grid;grid-template-columns:1fr 1fr;gap:10px}
'''

JS = r'''
/* ============================================================
   0. 数据层（命题与关系取自指南第 7 章“文书一”）
   ============================================================ */
const SAMPLE = '本院认为，依法成立的合同，自成立时生效。当事人应当按照约定全面履行自己的义务。当事人一方未支付价款、报酬、租金、利息，或者不履行其他金钱债务的，对方可以请求其支付。本案中，原、被告之间系劳务合同关系，原告已依约提供劳务，被告应按照原、被告之间的约定给付劳务报酬。根据原告提交的欠条、微信转账记录可以认定，被告尚欠原告劳务报酬11000元，被告应向原告支付该11000元。原告主张另有劳务报酬600元，但其提供的证据不足以证明其主张，对其主张被告支付该600元劳务报酬的请求，本院不予支持。';
const SAMPLE_LEN = SAMPLE.length;

const CASEINFO = {
  '案号':'(2023)苏0106民初18909号','裁判法院':'江苏省南京市鼓楼区人民法院','法院层级':'基层法院',
  '审级':'一审','裁判日期':'2023年12月28日','案件性质':'民事','案由':'劳务合同纠纷',
  '裁判结果类型':'部分支持','案例类型':'原始判决书'
};

const DEFAULT_SPANS = [
  {id:'P1', s:5,  e:20,  type:'GM-L', arg:'A1'},
  {id:'P2', s:20, e:39,  type:'GM-L', arg:'A1'},
  {id:'P3', s:39, e:82,  type:'GM-L', arg:'A2'},
  {id:'P4', s:82, e:100, type:'SM',   arg:'A1'},
  {id:'P5', s:100,e:110, type:'SF',   arg:'A1'},
  {id:'P6', s:110,e:131, type:'SM',   arg:'A1'},
  {id:'P7', s:131,e:152, type:'SF',   arg:'A2'},
  {id:'P8', s:152,e:169, type:'SF',   arg:'A2'},
  {id:'P9', s:169,e:185, type:'SM',   arg:'A2'},
  {id:'P10',s:185,e:200, type:'SF',   arg:'A3'},
  {id:'P11',s:200,e:216, type:'SF',   arg:'A3'},
  {id:'P12',s:216,e:232, type:'SM',   arg:'A3'},
  {id:'P13',s:232,e:243, type:'SM',   arg:'A3'}
];

const BASE_RELS = [
  {id:'R1', type:'J', args:['P4','P5'], arg:'A1', note:'劳务合同关系 + 已提供劳务，缺一不可'},
  {id:'R2', type:'M', args:['R1','P2'], arg:'A1', note:'组合体与“应按约履行”条文匹配'},
  {id:'R3', type:'S', args:['R2','P6'], arg:'A1', note:'匹配结构支持“应给付报酬”'},
  {id:'R4', type:'S', args:['P7','P8'], arg:'A2', note:'证据可认定 → 欠款事实'},
  {id:'R5', type:'J', args:['P8','P6'], arg:'A2', note:'欠款事实 + 应给付义务'},
  {id:'R6', type:'M', args:['R5','P3'], arg:'A2', note:'与“未付款可请求支付”条文匹配'},
  {id:'R7', type:'S', args:['R6','P9'], arg:'A2', note:'支持“应向原告支付11000元”'},
  {id:'R8', type:'S', args:['P10','P12'], arg:'A3', note:'主张600元 → 请求支付600元'},
  {id:'R9', type:'A', args:['P11','P10'], arg:'A3', note:'证据不足反对“另有600元”的主张'},
  {id:'R10',type:'S', args:['P11','P13'], arg:'A3', note:'证据不足支持“不予支持”'}
];

const L1 = [
  {k:'SF', n:'个别事实判断', d:'关于案件中个别对象的事实判断，是规范适用的前提条件'},
  {k:'GF', n:'一般事实判断', d:'为规范适用提供经验或背景支撑（社会常识、经验法则、行业知识、科学规律）'},
  {k:'SM', n:'个别规范判断', d:'具体主体（含法院）作出的具有法律意义的评价判断；“应/应当”是典型标志'},
  {k:'GM', n:'一般规范判断', d:'构成法律论证的规范基础，连接个案事实与裁判结论的核心要素'},
  {k:'IS', n:'争议焦点', d:'小标题、法院对案件争议的概括语言（非命题要素）'},
  {k:'Non', n:'非论证成分', d:'与论证无关的信息（非命题要素）'}
];
const L2 = {
  GM:[{k:'GM-L',n:'法律条文',d:'依照《××法》第×条规定 / 根据法律规定'},
      {k:'GM-I',n:'法律解释',d:'应当理解为 / 可以解释为 / 该条规定的本意在于'},
      {k:'GM-U',n:'习惯与行业惯例',d:'按照交易习惯 / 行业通常做法是'},
      {k:'GM-M',n:'道德与价值观念',d:'违反公序良俗 / 有悖公平原则'},
      {k:'GM-O',n:'其他规范判断',d:'根据相关政策精神 / 依照××管理规定'}],
  SM:[{k:'SM',n:'个别规范判断',d:'原告请求支付违约金 / 一审法院认定 / 缺乏事实与法律依据'},
      {k:'SM-C',n:'合同及合同解释',d:'双方在合同中约定 / 根据合同约定 / 该条款应理解为'}]
};
const RELTYPES = [
  {k:'S',n:'支持关系',expr:'S(pi,pj)',d:'pi 为 pj 的成立提供理由'},
  {k:'A',n:'反对关系',expr:'A(po,pc)',d:'po 为 pc 的不成立提供理由'},
  {k:'J',n:'组合关系',expr:'J(p1,p2,...,pn)',d:'多个命题“缺一不可”的合取结构（n≥2）'},
  {k:'M',n:'匹配关系',expr:'M(ps,pg)',d:'个别判断与一般判断之间的对应（要件-事实匹配）'},
  {k:'I',n:'同一关系',expr:'I(p1,p2,...,pn)',d:'多个命题语义上表达同一判断内容'}
];

/* ============================================================
   1. 状态
   ============================================================ */
const state = {
  mod:'overview', user:'王老师', role:'管理员',
  step:'granularity',
  doc:{ name:'(2023)苏0106民初18909号 余某诉徐某劳务合同纠纷', text:SAMPLE,
        range:{s:0,e:SAMPLE_LEN}, src:'智能提取', confirmed:false },
  caseInfo:Object.assign({},CASEINFO),
  guides:[{ver:'v1.2', name:'中文裁判文书说理部分法律论证结构标注与图示指南',
           at:'2026-04-14 10:02', by:'王老师', frozen:true, labels:13, rels:5, snap:'guide-v1.2.pdf'}],
  guideVer:'v1.2',
  tasks:[{id:'T-001', name:'劳务合同纠纷论证结构标注（第一批）', caseType:'原始判决书',
          labels:'LS-v1.2', annotators:['张三','李四'], adjudicator:'王五', docs:1, state:'标注中'}],
  currentVersion:'A', versions:{}, cur:null, selection:null,
  selA:null, selB:null,
  closed:false, final:null, ledger:[], exports:[], picked:{}, reasons:{}, noAuto:false,
  teaching:{answer:null,student:null,compare:null}, zoom:1
};

function cloneSpans(){ return DEFAULT_SPANS.map(function(p){ return Object.assign({},p); }); }
function cloneRels(){ return BASE_RELS.map(function(r){ return Object.assign({},r,{args:r.args.slice()}); }); }
function initVersions(){
  state.versions.A={by:'张三', props:cloneSpans(), rels:cloneRels(), submitted:false, pos:null};
  var props=cloneSpans();
  props[9].type='SM';                                   /* 差异①：P10 标签 */
  var rels=cloneRels().filter(function(r){ return r.id!=='R10'; });   /* 差异③：缺 R10 */
  var i=-1; rels.forEach(function(r,k){ if(r.id==='R1') i=k; });
  rels.splice(i,3,
    {id:'R1',type:'S',args:['P4','P6'],arg:'A1',note:'独立支持（错误示范）'},
    {id:'R2',type:'S',args:['P5','P6'],arg:'A1',note:'独立支持（错误示范）'});
  rels.forEach(function(r,k){ r.id='R'+(k+1); });
  state.versions.B={by:'李四', props:props, rels:rels, submitted:false, pos:null};
}
initVersions();

function V(){ return state.versions[state.currentVersion]; }
function props(){ return V().props; }
function rels(){ return V().rels; }
function propById(id){ return props().filter(function(p){return p.id===id;})[0]; }
function relById(id){ return rels().filter(function(r){return r.id===id;})[0]; }
function textFor(p){ return state.doc.text.slice(p.s,p.e); }
function exprOf(r,depth){
  depth=depth||0; if(depth>6) return '…';
  var inside=r.args.map(function(a){ var s=relById(a); return s?exprOf(s,depth+1):a; }).join(',');
  return r.type+'('+inside+')';
}
function relTypeName(k){ var t=RELTYPES.filter(function(x){return x.k===k;})[0]; return t?t.n:k; }

/* ============================================================
   2. 工具
   ============================================================ */
function $(s){ return document.querySelector(s); }
function esc(t){ return String(t==null?'':t).replace(/[&<>"]/g,function(c){
  return ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'})[c]; }); }
function tagHtml(code){
  if(!code) return '<span class="tag Non">待定</span>';
  var isSub = L2.GM.concat(L2.SM).some(function(x){return x.k===code;});
  var cls = isSub ? code : (code.indexOf('GM')===0?'GM-L':code);
  return '<span class="tag '+cls+'">'+esc(code)+'</span>';
}
function l1Of(code){
  if(!code) return '';
  if(code.indexOf('GM')===0) return 'GM';
  if(code.indexOf('SM')===0) return 'SM';
  return code;
}
function toast(title, html, wide){
  $('#dlgTitle').textContent=title;
  $('#dlgBody').innerHTML=html||'';
  $('#dlgFoot').innerHTML='<button class="primary" onclick="closeDlg()">知道了</button>';
  var d=$('#dlg'); d.style.maxWidth=wide?'1020px':'840px';
  if(!d.open) d.showModal();
}
function closeDlg(){ var d=$('#dlg'); if(d.open) d.close(); }
function setMod(m){ state.mod=m; if(location.hash!=='#'+m) location.hash='#'+m; else render(); }
function nowStr(){
  var d=new Date(), p=function(n){ return String(n).padStart(2,'0'); };
  return d.getFullYear()+'-'+p(d.getMonth()+1)+'-'+p(d.getDate())+' '+p(d.getHours())+':'+p(d.getMinutes())+':'+p(d.getSeconds());
}

/* ============================================================
   3. 模块：项目概览
   ============================================================ */
function viewOverview(){
  var A=state.versions.A, B=state.versions.B, g=state.guides[state.guides.length-1];
  return '<div class="card"><h3>项目概览</h3><div class="row">'+
    '<div class="col"><div class="kv">'+
      '<b>项目</b><span>'+esc(state.tasks[0].name)+'</span>'+
      '<b>标注对象</b><span>裁判文书“裁判理由”部分（“本院认为”至“判决如下”之前）</span>'+
      '<b>指南版本</b><span>'+esc(g.ver+' · '+g.name)+'</span>'+
      '<b>标签集</b><span class="mono">LS-'+esc(g.ver)+'（任务期冻结）</span>'+
      '<b>当前文书</b><span>'+esc(state.doc.name)+'</span>'+
      '<b>案例类型</b><span>'+esc(state.caseInfo['案例类型']||'-')+'</span>'+
      '<b>标注员 / 裁定者</b><span>'+state.tasks[0].annotators.join('、')+' / '+esc(state.tasks[0].adjudicator)+'</span>'+
      '<b>当前身份</b><span>'+esc(state.user+'（'+state.role+'）')+'</span>'+
    '</div></div>'+
    '<div class="col"><div class="kv">'+
      '<b>原文长度</b><span class="mono">'+state.doc.text.length+' 字符</span>'+
      '<b>标注范围</b><span class="mono">char '+state.doc.range.s+' – '+state.doc.range.e+'</span>'+
      '<b>张三版</b><span>'+A.props.length+' 个要素 · '+A.rels.length+' 条关系 '+(A.submitted?'<span class="ok">已提交</span>':'<span class="muted">未提交</span>')+'</span>'+
      '<b>李四版</b><span>'+B.props.length+' 个要素 · '+B.rels.length+' 条关系 '+(B.submitted?'<span class="ok">已提交</span>':'<span class="muted">未提交</span>')+'</span>'+
      '<b>任务状态</b><span>'+(state.closed?'<span class="warn">已定稿 / 已导出（只读）</span>':esc(state.tasks[0].state))+'</span>'+
    '</div>'+
    '<p class="muted" style="margin-top:10px">本原型覆盖需求文档的全部功能面：指南版本管理、任务创建与分配、'+
    '颗粒度切割与要素标注、关系标注与图示、冲突裁定、质量看板、教学比对、导出与再导入。'+
    '数据为演示用，命题与关系取自指南第 7 章真实示例。</p>'+
    '</div></div></div>'+

  '<div class="card"><h3>模块与需求对照</h3><table>'+
    '<tr><th style="width:140px">模块</th><th style="width:240px">需求出处</th><th>本原型实现</th></tr>'+
    '<tr><td>指南管理</td><td>2.2 标签体系配置 · Q5 指南版本</td><td>导入预览、标签/关系体系、版本历史与冻结</td></tr>'+
    '<tr><td>任务管理</td><td>2.1–2.3 文本导入 / 智能提取 / 分配</td><td>上传与手动录入、理由边界校正、案例信息、按类型批量分配、人员增减</td></tr>'+
    '<tr><td>标注工作台</td><td>3.1–3.6 三栏布局 / 原文 / 命题列表 / 关系 / 图示</td><td>三栏可调节、字符索引定位、颗粒度切割、要素标注、关系标注、图示拖拽与缩放</td></tr>'+
    '<tr><td>冲突裁定</td><td>4.1–4.2 差异比对与裁定</td><td>差异线索可开关、三列并排、逐条裁定与理由、专家裁决、定稿锁库</td></tr>'+
    '<tr><td>质量看板</td><td>3.7 一致性控制 · 指南 8.3</td><td>颗粒度差异率、标签/关系一致率、高分歧标签、疑难台账、操作留痕</td></tr>'+
    '<tr><td>教学比对</td><td>场景 1 独立入口 · Q7 预览最终结果</td><td>标准样例、学生独立标注、比对与错题集</td></tr>'+
    '<tr><td>导出与归档</td><td>5.1–5.3</td><td>JSON/CSV/SVG/报告、真实下载、进度、只读锁定、下载记录、再导入</td></tr>'+
  '</table></div>'+

  '<div class="card"><h3>演示路线</h3><table>'+
    '<tr><th style="width:52px">步骤</th><th style="width:330px">操作</th><th>观众看到什么</th></tr>'+
    '<tr><td>1</td><td>指南管理 → 导入指南</td><td>解析出标签体系与 5 种关系，新增 v1.3 版本</td></tr>'+
    '<tr><td>2</td><td>任务管理 → 上传 → 确认范围 → 保存案例信息 → 分配</td><td>裁判理由边界可校正；独立标注任务生成</td></tr>'+
    '<tr><td>3</td><td>标注工作台 → ① 颗粒度切割 → 一键自动切分</td><td>按句号/逗号切成子句，形成 13 个要素</td></tr>'+
    '<tr><td>4</td><td>② 要素标注：原文拖选 → 建立命题 → 点标签</td><td>原文出现编号、左侧列表新增、右侧图加节点</td></tr>'+
    '<tr><td>5</td><td>③ 关系标注：图上依次点两个节点 → 选关系</td><td>生成 S(M(J(P4,P5),P2),P6)；切李四版可触发结构校验</td></tr>'+
    '<tr><td>6</td><td>冲突裁定 → 逐条裁定 + 填理由 → 定稿</td><td>差异按标签/关系/边界分类；裁定记录入库</td></tr>'+
    '<tr><td>7</td><td>质量看板 / 教学比对</td><td>一致率指标、高分歧标签；学生错题集</td></tr>'+
    '<tr><td>8</td><td>导出与归档 → 开始导出</td><td>真实下载 4 个文件；之后数据只读</td></tr>'+
  '</table></div>';
}

/* ============================================================
   4. 模块：指南管理
   ============================================================ */
function viewGuide(){
  var rows=state.guides.map(function(g){
    return '<tr><td class="mono">'+esc(g.ver)+'</td><td>'+esc(g.name)+'</td><td class="tiny">'+esc(g.at)+'</td>'+
      '<td>'+esc(g.by)+'</td><td>'+g.labels+' / '+g.rels+'</td>'+
      '<td>'+(g.frozen?'<span class="ok">已冻结</span>':'<span class="muted">草稿</span>')+'</td>'+
      '<td class="tiny mono">'+esc(g.snap)+'</td>'+
      '<td>'+(g.frozen?'<span class="tiny">当前使用</span>':'<button onclick="freezeGuide(\''+g.ver+'\')">冻结</button>')+'</td></tr>';
  }).join('');
  return '<div class="card"><h3>从文件导入标注指南（UC-01）</h3>'+
    '<p class="muted">支持 PDF / Word / 纯文本，批量或单份导入。系统识别章节结构与标签定义，'+
    '形成带版本号的指南版本库记录，并冻结为任务使用的标签集。</p>'+
    '<div class="drop"><p><b>把指南文件拖到这里，或点击下方按钮模拟导入</b></p>'+
      '<p class="tiny">已内置 v1.2；再导入一次可产出 v1.3 并观察版本历史</p>'+
      '<button class="primary" onclick="doImportGuide()">选择文件并导入</button> '+
      '<button onclick="showGuideBody()">查看指南目录与颗粒度规则</button></div></div>'+

  '<div class="card"><h3>指南版本库</h3><table>'+
    '<tr><th>版本</th><th>标题</th><th>导入时间</th><th>导入人</th><th>标签/关系</th><th>状态</th><th>文件快照</th><th>操作</th></tr>'+
    rows+'</table><p class="tiny" style="margin-top:6px">Q5：导出数据需指明使用的指南版本；Q3：任务开始后标签体系不变，改动需新建版本。</p></div>'+

  '<div class="card"><h3>标签体系</h3><table>'+
    '<tr><th style="width:76px">代码</th><th style="width:170px">名称</th><th>定义说明 / 标志性表述</th></tr>'+
    L1.map(function(x){ return '<tr><td>'+tagHtml(x.k)+'</td><td>'+esc(x.n)+'</td><td class="muted">'+esc(x.d)+'</td></tr>'; }).join('')+
    L2.GM.map(function(x){ return '<tr><td>'+tagHtml(x.k)+'</td><td>'+esc(x.n)+'<span class="tiny">（GM 子类型）</span></td><td class="muted">'+esc(x.d)+'</td></tr>'; }).join('')+
    '<tr><td>'+tagHtml('SM-C')+'</td><td>合同及合同解释<span class="tiny">（个别规范判断）</span></td><td class="muted">双方在合同中约定 / 根据合同约定 / 该条款应理解为</td></tr>'+
    '</table><p class="muted" style="margin-top:8px">标注三原则：<b>优先匹配</b>、<b>不重复标注</b>、<b>以文本显性表达为准</b>。</p></div>'+

  '<div class="card"><h3>关系类型</h3><table>'+
    '<tr><th style="width:56px">代码</th><th style="width:110px">名称</th><th>逻辑含义</th><th style="width:150px">形式化表达</th><th style="width:260px">图示特征</th></tr>'+
    RELTYPES.map(function(r){
      var feat=({S:'实心圆● + 有向边（支持者→被支持命题）',A:'空心圆○ + 有向边（反对者→被反对者）',
        J:'带“+”圆 + 无向连线（合取结构）',M:'带“+”圆 + 有向边（匹配者→被匹配者）',
        I:'矩形框内“/”分隔'})[r.k];
      return '<tr><td><b>'+r.k+'</b></td><td>'+esc(r.n)+'</td><td class="muted">'+esc(r.d)+'</td>'+
        '<td class="mono">'+esc(r.expr)+'</td><td class="muted">'+feat+'</td></tr>';
    }).join('')+'</table></div>';
}
function doImportGuide(){
  var n=state.guides.length, ver = n===1?'v1.3':('v1.'+(2+n));
  state.guides.push({ver:ver, name:'中文裁判文书说理部分法律论证结构标注与图示指南（修订）',
    at:nowStr(), by:state.user, frozen:false, labels:13, rels:5, snap:'guide-'+ver+'.pdf'});
  toast('导入成功',
    '<p>已解析指南文件并生成新版本 <b class="mono">'+ver+'</b>：</p><ul>'+
    '<li>识别章节 10 个（含“4.2.2 两组基本区分维度与四种基础判断类型”“5.1 五种关系类型说明”）</li>'+
    '<li>解析标签 13 个：一级 4（SF/GF/SM/GM）+ GM 子类型 5 + SM-C + 非命题 2（IS/Non）</li>'+
    '<li>解析关系类型 5 种：S / A / J / M / I</li>'+
    '<li>写入指南版本库并生成文件快照 guide-'+ver+'.pdf</li></ul>'+
    '<p class="muted">新版本默认是草稿；点击“冻结”后才会替代当前任务使用的标签集（任务期标签不变）。</p>');
  render();
}
function freezeGuide(ver){
  state.guides.forEach(function(g){ g.frozen=(g.ver===ver); });
  state.guideVer=ver;
  toast('已冻结 '+ver,'<p>当前任务使用的标签集切换为 <b class="mono">LS-'+ver+'</b>。</p>'+
    '<p class="muted">Q3：任务开始后标签体系不变；本操作会写入操作日志。</p>');
  render();
}
function showGuideBody(){
  var ch=['1. 动因、目标、意义、适用对象','2. 标注对象、范围与颗粒度','3. 总体标注进路','4. 要素类型体系',
    '　4.1 非命题要素类型','　4.2 命题要素类型体系','5. 命题间关系类型','6. 法律论证结构的图示规则',
    '7. 法律论证标注示例：文书一的标注全流程','8. 标注流程与一致性控制'];
  toast('指南目录与关键规则','<div class="chips">'+ch.map(function(t){return '<span class="pill">'+esc(t)+'</span>';}).join('')+'</div>'+
    '<h4>颗粒度规则（2.3 节）</h4><ul class="muted">'+
    '<li>先按<b>句号</b>切第一刀；句号内按逗号/分号考察子句；</li>'+
    '<li>连续子句<b>同性质</b>且无支持/反对关系 → <b>合并为一个要素</b>，否则各自编号；</li>'+
    '<li>带<b>双引号</b>的内容以双引号为单位；<b>过渡语词</b>与之后的第一个要素切在一起；</li>'+
    '<li>两人切分差异率 <b>&gt;10%</b> 需重新切割。</li></ul>'+
    '<h4>图示规则（第 6 章）</h4><ul class="muted">'+
    '<li>命题＝矩形（框内只写序号，不显示类型）；关系＝圆形节点；</li>'+
    '<li>实心圆＝支持，空心圆＝反对，带“+”圆＝组合或匹配；同一关系＝框内“/”；</li>'+
    '<li>嵌套结构自内而外逐层构造，保持括号层级与逻辑层级一致。</li></ul>');
}

/* ============================================================
   5. 模块：任务管理
   ============================================================ */
function viewTask(){
  var t=state.tasks[0];
  var ck = state.doc.confirmed?'<span class="ok">已确认</span>':'<span class="warn">待确认</span>';
  return '<div class="card"><h3>① 文本导入与智能提取</h3><div class="row">'+
    '<div class="col"><div class="kv">'+
      '<b>文书名</b><span><input value="'+esc(state.doc.name)+'" style="width:100%" onchange="state.doc.name=this.value"></span>'+
      '<b>来源</b><span class="mono">'+esc(state.doc.src)+'</span>'+
      '<b>正文长度</b><span class="mono">'+state.doc.text.length+' 字符</span></div>'+
      '<p class="muted" style="margin-top:8px">支持 PDF / 纯文本 / Word、批量上传与手动录入；'+
      '系统按“本院认为”“判决如下”定位裁判理由，并允许人工校正边界。</p>'+
      '<p><button class="primary" onclick="simulateUpload()">上传文书文件（模拟）</button> '+
      '<button onclick="editText()">手动录入 / 修改正文</button> '+
      '<button onclick="autoExtract()">重新智能提取</button></p></div>'+
    '<div class="col"><h4>标注范围确认 '+ck+'</h4>'+
      '<div class="tiny mono">char '+state.doc.range.s+' – '+state.doc.range.e+'（'+(state.doc.range.e-state.doc.range.s)+' 字符）</div>'+
      '<p class="muted" style="margin:6px 0">起点：“'+esc(state.doc.text.slice(state.doc.range.s,state.doc.range.s+14))+'…”　'+
      '终点：“…'+esc(state.doc.text.slice(Math.max(0,state.doc.range.e-14),state.doc.range.e))+'”</p>'+
      '<p><button class="primary" onclick="confirmRange()">确认标注范围</button> '+
      '<button onclick="openRangeEditor()">手动微调边界</button></p>'+
      '<div class="banner" style="margin-top:8px">指南：裁判理由 ＝ “本院认为”之后、“判决如下”所在句子之前的文本；'+
      '“综上所述，依照……”属引述过渡，应在范围之外。</div></div>'+
  '</div></div>'+

  '<div class="card"><h3>② 案例信息（指南表 1：原始判决书）</h3><table>'+
    Object.keys(state.caseInfo).map(function(k){
      return '<tr><th style="width:150px">'+esc(k)+'</th><td><input value="'+esc(state.caseInfo[k])+
        '" style="width:100%" onchange="state.caseInfo[\''+k+'\']=this.value"></td></tr>';
    }).join('')+
    '</table><p class="tiny" style="margin-top:6px">指导性案例与参考案例的字段不同（指南表 2、表 3）：前者有裁判要点，后者有入库编号与裁判要旨。</p></div>'+

  '<div class="card"><h3>③ 任务分配与人员</h3><div class="row">'+
    '<div class="col"><div class="kv">'+
      '<b>任务名</b><span>'+esc(t.name)+'</span>'+
      '<b>案例类型</b><span>'+esc(t.caseType)+'（可按类型批量分配）</span>'+
      '<b>标签集</b><span class="mono">'+esc(t.labels)+'</span>'+
      '<b>裁定者</b><span>'+esc(t.adjudicator)+'</span>'+
      '<b>文书数</b><span>'+t.docs+'</span></div>'+
      '<h4>标注员（多对多，可追加）</h4><div class="chips">'+
      t.annotators.map(function(a){ return '<span class="pill">'+esc(a)+
        ' <button class="ghost danger" style="padding:0 4px;border:0" onclick="removeAnnotator(\''+esc(a)+'\')">×</button></span>'; }).join('')+
      '</div><p style="margin-top:8px"><button onclick="addAnnotator()">＋ 增加标注员</button> '+
      '<button onclick="assignByType()">按案例类型批量分配</button> '+
      '<button onclick="setAdjudicator()">指定 / 更换裁定者</button></p>'+
      '<p class="tiny">已确认：任务开始后<b>人员可增加</b>、<b>数据可增加</b>、<b>标签体系不变</b>（Q1/Q2/Q3）。</p></div>'+
    '<div class="col"><h4>任务列表</h4><table>'+
      '<tr><th>编号</th><th>任务</th><th>类型</th><th>标注员</th><th>裁定者</th><th>状态</th></tr>'+
      state.tasks.map(function(x){
        return '<tr><td class="mono">'+esc(x.id)+'</td><td>'+esc(x.name)+'</td><td>'+esc(x.caseType)+'</td>'+
          '<td>'+x.annotators.join('、')+'</td><td>'+esc(x.adjudicator)+'</td>'+
          '<td>'+(state.closed?'<span class="warn">已定稿</span>':esc(x.state))+'</td></tr>';
      }).join('')+'</table>'+
      '<p style="margin-top:8px"><button class="primary" onclick="goWork()">进入标注工作台 →</button></p></div>'+
  '</div></div>';
}
function simulateUpload(){
  toast('上传成功','<p>已读取 <b>'+esc(state.doc.name)+'</b>（PDF，3 页）。</p>'+
    '<p>系统定位裁判理由：char '+state.doc.range.s+' – '+state.doc.range.e+'，共 '+
    (state.doc.range.e-state.doc.range.s)+' 字符。</p>'+
    '<p class="muted">这是“智能提取”，仍需人工在右侧确认范围。</p>');
  state.doc.src='文件上传（PDF）'; state.doc.confirmed=false; render();
}
function editText(){
  toast('手动录入 / 修改正文',
    '<p class="muted">需求原文：“希望在原文的文本框中可以修改文本内容”。修改只影响当前演示数据。</p>'+
    '<textarea id="txtEdit" rows="10" class="mono">'+esc(state.doc.text)+'</textarea>', true);
  $('#dlgFoot').innerHTML='<button onclick="closeDlg()">取消</button><button class="primary" onclick="saveText()">保存正文</button>';
}
function saveText(){
  var v=$('#txtEdit').value;
  if(!v.trim()){ toast('不能为空','<p>正文不能为空。</p>'); return; }
  state.doc.text=v; state.doc.range={s:0,e:v.length}; state.doc.src='手动录入'; state.doc.confirmed=false;
  initVersions();
  closeDlg(); render();
}
function autoExtract(){
  var s=state.doc.text.indexOf('本院认为');
  var e=state.doc.text.indexOf('判决如下');
  if(e<0) e=state.doc.text.indexOf('综上所述');
  if(e<0) e=state.doc.text.length;
  state.doc.range={s:(s<0?0:s), e:e};
  toast('智能提取完成','<p>起点：'+(s<0?'未命中“本院认为”，取 0':'<span class="mono">char '+s+'</span>（“本院认为”）')+'</p>'+
    '<p>终点：'+(e>=state.doc.text.length?'未命中锚点，取正文末尾':'<span class="mono">char '+e+'</span>（锚点之前）')+'</p>'+
    '<p class="muted">普通判决书可能没有显式结构，需要人工校正。</p>');
  render();
}
function confirmRange(){
  state.doc.confirmed=true;
  toast('范围已确认','<p>标注范围锁定为 <span class="mono">char '+state.doc.range.s+' – '+state.doc.range.e+'</span>。</p>'+
    '<p class="muted">之后所有命题的字符索引都落在这个区间内。</p>');
  render();
}
function openRangeEditor(){
  toast('手动微调边界',
    '<div class="kv"><b>起点 char</b><span><input id="rs" type="number" value="'+state.doc.range.s+'"></span>'+
    '<b>终点 char</b><span><input id="re" type="number" value="'+state.doc.range.e+'"></span></div>'+
    '<p class="muted" style="margin-top:8px">例如把“综上所述，依照《民法典》……判决如下：”排除在裁判理由之外。</p>');
  $('#dlgFoot').innerHTML='<button onclick="closeDlg()">取消</button><button class="primary" onclick="applyRange()">应用</button>';
}
function applyRange(){
  var s=parseInt($('#rs').value,10), e=parseInt($('#re').value,10);
  if(isNaN(s)||isNaN(e)||s<0||e<=s||e>state.doc.text.length){ toast('范围不合法','<p>终点需大于起点且不超过正文长度。</p>'); return; }
  state.doc.range={s:s,e:e}; state.doc.confirmed=false; closeDlg(); render();
}
function addAnnotator(){
  var n=prompt('新增标注员姓名：','王六');
  if(!n) return;
  if(state.tasks[0].annotators.indexOf(n)>=0){ toast('已存在','<p>'+esc(n)+' 已在该任务中。</p>'); return; }
  state.tasks[0].annotators.push(n);
  toast('已追加标注员','<p>'+esc(n)+' 已加入任务，将从“下一条”开始独立标注。</p>'+
    '<p class="muted">Q1：任务开始后可能出现人员更新 —— 已提交者不受影响。</p>');
  render();
}
function removeAnnotator(n){
  state.tasks[0].annotators=state.tasks[0].annotators.filter(function(x){return x!==n;});
  toast('已移除','<p>'+esc(n)+' 已从任务中移除。</p><p class="muted">原型不做提交状态校验；正式实现应限制为“未提交才可移除”。</p>');
  render();
}
function setAdjudicator(){
  var n=prompt('指定裁定者：',state.tasks[0].adjudicator);
  if(!n) return;
  state.tasks[0].adjudicator=n;
  toast('已指定裁定者','<p>当前裁定者：<b>'+esc(n)+'</b>。</p><p class="muted">Q12：是否需要多人共同裁定待确认。</p>');
  render();
}
function assignByType(){
  toast('按案例类型批量分配',
    '<p>筛选：案例类型 ＝ <b>'+esc(state.tasks[0].caseType)+'</b>，命中 1 份文书。</p>'+
    '<p>已分配给：'+state.tasks[0].annotators.join('、')+'（独立标注）；裁定者：'+esc(state.tasks[0].adjudicator)+'。</p>'+
    '<p class="muted">文书 ↔ 标注员为多对多；同一份数据可再次分配给新增标注员。</p>');
}
function goWork(){ setMod('work'); state.step='granularity'; }

/* ============================================================
   6. 模块：标注工作台（三栏，需求 3.1）
   ============================================================ */
function viewWork(){
  return ''+
  '<div class="banner" style="display:flex;gap:10px;align-items:center;flex-wrap:wrap">'+
    '<span>版本：<b>'+esc(V().by)+'</b></span>'+
    '<button class="'+(state.currentVersion==='A'?'primary':'')+'" onclick="switchVer(\'A\')">张三版</button>'+
    '<button class="'+(state.currentVersion==='B'?'primary':'')+'" onclick="switchVer(\'B\')">李四版</button>'+
    '<span class="stepper">'+
      '<span class="'+(state.step==='granularity'?'on':'')+'" onclick="setStep(\'granularity\')">① 颗粒度切割</span>'+
      '<span class="'+(state.step==='element'?'on':'')+'" onclick="setStep(\'element\')">② 要素标注</span>'+
      '<span class="'+(state.step==='relation'?'on':'')+'" onclick="setStep(\'relation\')">③ 关系标注</span>'+
    '</span>'+
    '<span class="tiny">范围 '+state.doc.range.s+'–'+state.doc.range.e+' · '+props().length+' 要素 · '+rels().length+' 关系</span>'+
    '<span style="margin-left:auto"><button onclick="submitVersion()">提交本版本</button></span>'+
  '</div>'+
  (state.closed?'<div class="banner err">任务已定稿并导出，当前为 <b>只读</b>状态；如需重标请新建任务。</div>':'')+
  '<div class="work" id="work">'+
    '<section><div class="pane-head"><span>原文（裁判理由）</span><span class="tiny">拖动选择文字即可标注</span></div>'+
      '<div class="pane-body"><div id="srcText"></div></div>'+
      '<div class="pane-head"><span>命题列表（显示全文，不省略）</span><span class="tiny" id="plistCount"></span></div>'+
      '<div class="pane-body" style="max-height:36%"><div class="plist" id="plist"></div></div></section>'+
    '<div class="gutter" data-g="1"></div>'+
    '<section><div class="pane-head"><span>标注操作区</span><span class="tiny" id="stepHint"></span></div>'+
      '<div class="pane-body" id="ops"></div>'+
      '<div class="pane-foot" id="opsFoot"></div></section>'+
    '<div class="gutter" data-g="2"></div>'+
    '<section><div class="pane-head"><span>论证图示区</span>'+
      '<span class="tiny"><button onclick="zoom(-1)">－</button> <span id="zoomVal">100%</span> <button onclick="zoom(1)">＋</button> '+
      '<button onclick="autoLayout()">自动排版</button></span></div>'+
      '<div class="pane-body" style="padding:0" id="svgHost"></div>'+
      '<div class="legend">'+
        '<span><i style="background:#333"></i>实心圆＝支持 S</span>'+
        '<span><i style="background:#fff"></i>空心圆＝反对 A</span>'+
        '<span><i style="background:#333;border-radius:2px"></i>“+”圆＝组合 / 匹配</span>'+
        '<span>方框＝命题（仅序号）</span>'+
        '<span class="tiny">拖动方框移动；依次点两个节点建关系</span>'+
      '</div></section>'+
  '</div>';
}
function setStep(s){ state.step=s; state.selection=null; render(); }
function switchVer(v){ state.currentVersion=v; state.cur=null; state.selection=null; state.selA=null; state.selB=null; render(); }
function zoom(d){
  state.zoom=Math.min(2.2,Math.max(.5,state.zoom+d*0.15));
  var z=$('#zoomVal'); if(z) z.textContent=Math.round(state.zoom*100)+'%';
  paintSvg();
}
function textFor2(p){ return state.doc.text.slice(p.s,p.e); }
function paintSource(){
  var el=$('#srcText'); if(!el) return;
  var list=props().slice().sort(function(a,b){return a.s-b.s;}), html='', cur=0;
  list.forEach(function(p){
    if(p.s>cur) html+=esc(state.doc.text.slice(cur,p.s));
    var sel=(state.cur===p.id)?' cur':'';
    html+='<span class="hl '+p.id+sel+'" data-pid="'+p.id+'" title="'+esc(p.id+'  '+textFor2(p))+
          '"><i class="no">'+p.id+'</i>'+esc(textFor2(p))+'</span>';
    cur=Math.max(cur,p.e);
  });
  if(cur<state.doc.text.length) html+=esc(state.doc.text.slice(cur));
  el.innerHTML=html;
  Array.prototype.forEach.call(el.querySelectorAll('span.hl'),function(s){
    s.onclick=function(){ state.cur=s.dataset.pid; render(); };
  });
}
function paintList(){
  var box=$('#plist'); if(!box) return;
  var cnt=$('#plistCount'); if(cnt) cnt.textContent=props().length+' 条';
  box.innerHTML=props().map(function(p){
    var warn=(p.s<state.doc.range.s||p.e>state.doc.range.e)?'<span class="warn tiny">越界</span>':'';
    return '<div class="pitem '+(state.cur===p.id?'cur':'')+'" onclick="pickProp(\''+p.id+'\')">'+
      '<span class="id">'+p.id+'</span><span class="tx">'+esc(textFor2(p))+' '+warn+'</span>'+
      '<span class="meta">'+tagHtml(p.type)+' '+p.s+'-'+p.e+'</span></div>';
  }).join('')||'<p class="muted">暂无要素。在原文中拖动选择文字后建立命题。</p>';
}
function pickProp(id){ state.cur=id; state.selection=null; render(); }
function paintOps(){
  var box=$('#ops'), foot=$('#opsFoot'), hint=$('#stepHint');
  if(!box) return;
  if(state.step==='granularity'){ hint.textContent='步骤一 · 不做标签'; box.innerHTML=opsGranularity(); foot.innerHTML=granFoot(); }
  else if(state.step==='element'){ hint.textContent='步骤二 · 选段 + 标签'; box.innerHTML=opsElement(); foot.innerHTML=elemFoot(); }
  else { hint.textContent='步骤三 · 在图上建关系'; box.innerHTML=opsRelation(); foot.innerHTML=relFoot(); }
}
function opsGranularity(){
  var auto='';
  var re=/[^。！？；]+[。！？；]?/g, m, segs=[];
  while((m=re.exec(state.doc.text))!==null){ if(m[0]) segs.push(m[0]); }
  return '<p class="muted">按句号切第一刀，再按逗号/分号考察子句：<b>性质相同且无支持/反对关系 → 合并为一个要素</b>。</p>'+
  '<p><button class="primary" onclick="autoSegment()">一键自动切分（演示）</button> '+
     '<button onclick="showGranRule()">查看颗粒度规则</button></p>'+
  '<h4>系统建议的切分（'+segs.length+' 句）</h4>'+
  '<table><tr><th style="width:44px">#</th><th>句子</th></tr>'+
  segs.map(function(s,i){ return '<tr><td class="mono">'+(i+1)+'</td><td class="tiny">'+esc(s)+'</td></tr>'; }).join('')+'</table>'+
  '<h4>当前要素（'+props().length+' 个）</h4>'+
  '<table><tr><th style="width:50px">序号</th><th>文本</th><th style="width:92px">字符区间</th><th style="width:104px">操作</th></tr>'+
  props().map(function(p){
    return '<tr><td class="mono">'+p.id+'</td><td>'+esc(textFor2(p))+'</td>'+
      '<td class="mono tiny">'+p.s+'–'+p.e+'</td>'+
      '<td><button class="ghost" onclick="pickProp(\''+p.id+'\')">定位</button> '+
      '<button class="ghost danger" onclick="delProp(\''+p.id+'\')">删</button></td></tr>';
  }).join('')+'</table>'+
  '<p class="tiny" style="margin-top:8px">两人切分差异率 &gt;10% 时系统退回重新切割（指南步骤一）。当前张三版与李四版切分一致，差异率 0%。</p>';
}
function granFoot(){
  return '<button class="primary" onclick="manualCut()">自定义切分（选段 → 分配序号）</button>'+
         '<button onclick="mergeWithPrev()">与上一条合并</button>'+
         '<span style="margin-left:auto"><button onclick="setStep(\'element\')">进入要素标注 →</button></span>';
}
function opsElement(){
  var p=state.cur?propById(state.cur):null, sel=state.selection, h='';
  if(sel) h+='<div class="banner ok">已选段 <span class="mono">char '+sel.s+'–'+sel.e+'</span>：「'+esc(sel.text)+'」</div>';
  else h+='<p class="muted">在左侧原文中<b>拖动选择一段文字</b>，然后选择标签；也可先只分配序号，稍后再补标签。</p>';
  h+='<p><button class="primary" onclick="createProp(false)" '+(sel?'':'disabled')+'>＋ 建立命题（分配序号）</button> '+
     '<button onclick="createProp(true)" '+(sel?'':'disabled')+'>只分配序号（标签待定）</button></p>';
  h+='<h4>一级标签</h4><div class="chips">'+
     L1.map(function(x){
       return '<button class="lblbtn '+((p&&l1Of(p.type)===x.k)?'on':'')+'" onclick="applyL1(\''+x.k+'\')" '+
         (p?'':'disabled')+' title="'+esc(x.d)+'">'+x.k+' · '+esc(x.n)+'</button>';
     }).join('')+'</div>';
  if(p && (l1Of(p.type)==='GM'||l1Of(p.type)==='SM')){
    var subs=(l1Of(p.type)==='GM')?L2.GM:L2.SM;
    h+='<h4>二级标签</h4><div class="chips">'+subs.map(function(x){
      return '<button class="lblbtn '+(p.type===x.k?'on':'')+'" onclick="applyL2(\''+x.k+'\')" title="'+esc(x.d)+'">'+
        x.k+' · '+esc(x.n)+'</button>';
    }).join('')+'</div>';
  }
  if(p){
    h+='<h4>当前命题 <span class="mono">'+p.id+'</span> '+tagHtml(p.type)+'</h4>'+
       '<div class="tiny mono">char '+p.s+'–'+p.e+'　论证单元 '+esc(p.arg||'-')+'</div>'+
       '<p style="margin:6px 0">'+esc(textFor2(p))+'</p>'+
       '<p><button onclick="showPropRule(\''+p.id+'\')">标注规则提示</button> '+
       '<button onclick="splitProp(\''+p.id+'\')">拆分</button> '+
       '<button onclick="mergeWithPrev()">与上一条合并</button> '+
       '<button class="danger" onclick="delProp(\''+p.id+'\')">删除</button></p>'+
       '<p class="tiny">论证单元：<select onchange="setArg(\''+p.id+'\',this.value)">'+
         ['A1','A2','A3','A4'].map(function(a){ return '<option '+(p.arg===a?'selected':'')+'>'+a+'</option>'; }).join('')+
       '</select>（一份文书可含多个独立论证结构，需求 3.6.1）</p>';
  }
  return h;
}
function setArg(id,a){ var p=propById(id); if(p){ p.arg=a; V().pos=null; render(); } }
function elemFoot(){
  return '<span class="tiny">序号按原文顺序动态重排（Q8）；不提供撤销栈，采用“删除—重新创建”（Q10）。</span>'+
    '<span style="margin-left:auto"><button onclick="setStep(\'granularity\')">← 颗粒度</button>'+
    '<button class="primary" onclick="setStep(\'relation\')">下一步：关系标注 →</button></span>';
}
function opsRelation(){
  var a=state.selA,b=state.selB,h='';
  h+='<p class="muted">关系在<b>右侧图示区</b>建立：依次点击两个节点，再选关系类型。节点可以是命题，也可以是已有关系（用于嵌套，如 A(p3,S(p1,p2))）。</p>';
  h+='<div class="banner">已选：<b class="mono">'+(a||'—')+'</b> → <b class="mono">'+(b||'—')+'</b>'+
     ((a&&b)?'':'　<span class="tiny">再点一个节点</span>')+'</div>';
  h+='<h4>关系类型</h4><div class="chips">'+RELTYPES.map(function(t){
    return '<button class="lblbtn" onclick="createRel(\''+t.k+'\')" '+((a&&b)?'':'disabled')+
      ' title="'+esc(t.d)+'">'+t.k+' · '+esc(t.n)+'</button>';
  }).join('')+'</div>';
  h+='<p style="margin-top:8px"><button onclick="clearPick()">清除选择</button> '+
     '<button onclick="validateRels()">校验当前关系结构</button></p>';
  h+='<h4>已有关系（'+rels().length+' 条）</h4><table>'+
     '<tr><th style="width:42px">编号</th><th style="width:34px">类型</th><th>形式化表达</th><th style="width:60px">单元</th><th style="width:60px">操作</th></tr>'+
     rels().map(function(r){
       return '<tr><td class="mono">'+r.id+'</td><td><b>'+r.type+'</b></td>'+
         '<td class="mono tiny">'+esc(exprOf(r))+'</td><td class="mono tiny">'+esc(r.arg||'-')+'</td>'+
         '<td><button class="ghost" onclick="delRel(\''+r.id+'\')">删</button></td></tr>';
     }).join('')+'</table>';
  return h;
}
function clearPick(){ state.selA=null; state.selB=null; render(); }
function relFoot(){
  return '<span class="tiny">关系在图中建立（Q9）；支持嵌套与多对一。</span>'+
    '<span style="margin-left:auto"><button onclick="setStep(\'element\')">← 要素</button>'+
    '<button class="primary" onclick="submitVersion()">提交本版本</button></span>';
}
function autoSegment(){
  var re=/[^。！？；]+[。！？；]?/g, m, out=[];
  while((m=re.exec(state.doc.text))!==null){ if(m[0]) out.push(m[0]); }
  toast('自动切分完成','<p>按句号/分号切出 <b>'+out.length+'</b> 个句子；再按逗号考察子句，合并同性质子句。</p>'+
    '<p class="muted">系统建议的要素数与指南示例一致（13 个）。需要调整时，在原文中拖动选择后手动切分/合并。</p>', true);
}
function showGranRule(){
  toast('颗粒度规则（指南 2.3）','<ul>'+
    '<li>先按<b>句号</b>切分第一刀；</li><li>句号内按<b>逗号/分号</b>考察子句：连续子句同性质且无支持/反对关系 → 合并为一个要素；</li>'+
    '<li>否则各自独立编号；</li><li>带<b>双引号</b>的内容以双引号为单位；</li>'+
    '<li><b>过渡语词</b>与之后第一个要素切在一起；</li><li>两人切分差异率 &gt;10% 需重新切割。</li></ul>');
}
function manualCut(){ toast('自定义切分','<p>在左侧原文中拖动选择文字，然后点“建立命题（分配序号）”。</p>'); }
function delProp(id){
  var v=V();
  v.props=v.props.filter(function(p){return p.id!==id;});
  v.rels=v.rels.filter(function(r){return r.args.indexOf(id)<0;});
  v.props.forEach(function(p,i){ p.id='P'+(i+1); });
  v.rels.forEach(function(r,i){ r.id='R'+(i+1); });
  state.cur=null; v.pos=null;
  toast('已删除','<p>序号已按原文顺序重排。</p><p class="muted">Q10：删除—重新创建。</p>'); render();
}
function mergeWithPrev(){
  var v=V(), i=-1;
  v.props.forEach(function(p,k){ if(p.id===state.cur) i=k; });
  if(i<=0){ toast('无法合并','<p>请先选中一个命题（且不是第一条）。</p>'); return; }
  var a=v.props[i-1], b=v.props[i];
  a.e=b.e; v.props.splice(i,1);
  v.props.forEach(function(p,k){ p.id='P'+(k+1); });
  state.cur=null; v.pos=null;
  toast('已合并','<p>两条合并为一个要素（连续子句同性质）。</p>'); render();
}
function createProp(pendingOnly){
  var sel=state.selection;
  if(!sel){ toast('未选择文本','<p>请在左侧原文中拖动选择一段文字。</p>'); return; }
  var v=V();
  var hit=v.props.filter(function(p){ return !(sel.e<=p.s||sel.s>=p.e); })[0];
  if(hit){ toast('选区与既有命题重叠','<p>与 <b>'+hit.id+'</b> 重叠，请调整范围或直接编辑该命题。</p>'); return; }
  var np={id:'N'+(v.props.length+1), s:sel.s, e:sel.e, type:'', arg:'A1'};
  v.props.push(np); v.props.sort(function(a,b){return a.s-b.s;});
  v.props.forEach(function(p,i){ p.id='P'+(i+1); });
  state.cur=np.id; state.selection=null; v.pos=null;
  toast(pendingOnly?'已分配序号（标签待定）':'已建立命题',
    '<p>已按原文顺序分配序号；'+(pendingOnly?'标签留待后续补充。':'请在中间“一级标签 / 二级标签”里选择。')+'</p>'+'');
  render();
}
function applyL1(k){
  var p=state.cur?propById(state.cur):null;
  if(!p){ toast('未选中命题','<p>请先选中一个命题。</p>'); return; }
  p.type=(k==='GM')?'GM-L':((k==='SM')?'SM':k);
  render();
}
function applyL2(k){
  var p=state.cur?propById(state.cur):null; if(!p) return;
  p.type=k;
  if(k==='GM-O') toast('提示','<p>指南原则：能明确归入 GM-L~GM-M 的，不使用 GM-O（优先匹配原则）。</p>');
  render();
}
function showPropRule(id){
  var p=propById(id); if(!p) return;
  toast('标注规则提示（'+id+'）','<p>当前标签：'+tagHtml(p.type)+'　文本：'+esc(textFor2(p))+'</p><ul>'+
    '<li><b>优先匹配</b>：能归 GM-L~GM-M，就不用 GM-O；</li>'+
    '<li><b>不重复标注</b>：同一规范判断只选一个子类型；</li>'+
    '<li><b>以文本显性表达为准</b>：不依据背景知识补充规范来源；</li>'+
    '<li>含“应 / 应当”等道义表述的，通常为 SM；</li>'+
    '<li>法律关系、程序性判断、证据性判断也属 SM；</li>'+
    '<li>纯标题、争议概括标 IS；与论证无关的信息标 Non。</li></ul>');
}
function splitProp(id){
  var p=propById(id); if(!p) return;
  var t=textFor2(p);
  if(t.length<6){ toast('无法拆分','<p>文本过短。</p>'); return; }
  var cut=Math.max(t.indexOf('，'),t.indexOf('、'));
  if(cut<0) cut=Math.floor(t.length/2);
  toast('拆分命题','<p>把“'+esc(t)+'”拆成两条（以第一个逗号/分号为界）。</p><p class="muted">拆分后序号自动重排。</p>');
  $('#dlgFoot').innerHTML='<button onclick="closeDlg()">取消</button>'+
    '<button class="primary" onclick="doSplit(\''+id+'\','+(cut+1)+')">确认拆分</button>';
}
function doSplit(id,cut){
  var v=V(), p=null;
  v.props.forEach(function(x){ if(x.id===id) p=x; });
  if(!p) return;
  var i=v.props.indexOf(p);
  v.props.splice(i,1,{id:'x1',s:p.s,e:Math.min(p.s+cut,p.e),type:p.type,arg:p.arg},
                     {id:'x2',s:Math.min(p.s+cut,p.e),e:p.e,type:'',arg:p.arg});
  v.props.sort(function(a,b){return a.s-b.s;});
  v.props.forEach(function(q,k){ q.id='P'+(k+1); });
  v.pos=null; closeDlg(); toast('已拆分','<p>拆成两条，序号已重排。</p>'); render();
}
function createRel(k){
  var a=state.selA, b=state.selB;
  if(!a||!b){ toast('未选择节点','<p>请在图示区依次点击两个节点。</p>'); return; }
  if(a===b){ toast('不能自连','<p>请选择两个不同的节点。</p>'); return; }
  var v=V(), id='R'+(v.rels.length+1);
  var host=propById(a)||{arg:'A1'};
  v.rels.push({id:id,type:k,args:[a,b],arg:host.arg||'A1',note:''});
  state.selA=null; state.selB=null;
  toast('已建立关系','<p><b>'+k+'</b>：'+esc(exprOf(v.rels[v.rels.length-1]))+'</p>'+
    '<p class="muted">关系已写入数据并实时反映到图示。</p>');
  render();
}
function delRel(id){
  var v=V(); v.rels=v.rels.filter(function(r){return r.id!==id;});
  v.rels.forEach(function(r,i){ r.id='R'+(i+1); });
  toast('已删除关系','<p>编号已重排。</p>'); render();
}
function validateRels(){
  var msgs=[], v=V();
  v.rels.forEach(function(r){
    if(r.type==='J'&&r.args.length<2) msgs.push([r.id,'组合关系成员少于 2 个']);
    if(r.type==='M'){
      var a=propById(r.args[0]), b=propById(r.args[1]);
      if(a&&b&&l1Of(a.type)===l1Of(b.type)) msgs.push([r.id,'匹配关系双方性质相同（应为个别 ↔ 一般）']);
    }
  });
  var indep=0;
  v.rels.forEach(function(r){
    if(r.type==='S'&&((r.args[0]==='P4'&&r.args[1]==='P6')||(r.args[0]==='P5'&&r.args[1]==='P6'))) indep++;
  });
  if(indep===2) msgs.push(['—','检测到 S(P4,P6) 与 S(P5,P6) 两个独立支持：指南 5.3.3 要求“须共同成立方构成支持”时使用组合关系，不得混同']);
  v.rels.forEach(function(r){
    if(r.type!=='S'&&r.type!=='A') return;
    v.rels.forEach(function(x){
      if((x.type==='S'||x.type==='A')&&x.args[0]===r.args[1]&&x.args[1]===r.args[0]) msgs.push([r.id,'与 '+x.id+' 构成环']);
    });
  });
  if(!msgs.length){ toast('结构校验通过','<p class="ok">未发现违规：组合成员 ≥2、匹配双方性质相异、无环、无“组合/独立支持”混同。</p>'); }
  else{
    toast('结构校验发现 '+msgs.length+' 个问题','<table><tr><th style="width:56px">关系</th><th>问题</th></tr>'+
      msgs.map(function(m){ return '<tr class="diffrow"><td class="mono">'+m[0]+'</td><td>'+esc(m[1])+'</td></tr>'; }).join('')+
      '</table><p class="muted" style="margin-top:8px">这些问题进入裁定流程，由裁定者人工判断，系统不自动改数据。</p>');
  }
}
function submitVersion(){
  V().submitted=true;
  toast('已提交','<p>'+esc(V().by)+' 的版本已提交：'+props().length+' 个要素、'+rels().length+' 条关系。</p>'+
    '<p class="muted">提交后本版本锁定，后续修改在裁定阶段由裁定者进行。</p>');
  render();
}
function layoutNodes(){
  var v=V(), pos={}, seen={};
  var host=$('#svgHost');
  var Wp=Math.max(320,(host&&host.clientWidth)||420);
  var col1=50, col2=Math.max(150,Math.round(Wp*0.34)), col3=Math.max(210,Math.round(Wp*0.60));
  var groups={A1:[[col1,60],[col1,150],[col1,240],[col2,150]],
              A2:[[col1,330],[col1,420],[col2,330],[col3,330]],
              A3:[[col1,520],[col1,600],[col2,520],[col3,600]],
              A4:[[col3,60],[col3,150],[col3,240],[Math.max(col3+40,col2+120),150]]};
  v.props.forEach(function(p){
    var g=groups[p.arg]||groups.A1;
    seen[p.arg]=seen[p.arg]==null?0:seen[p.arg];
    var k=Math.min(seen[p.arg],g.length-1); seen[p.arg]++;
    pos[p.id]={x:g[k][0],y:g[k][1]};
  });
  /* 关系节点：仅当它被其它关系当作参数引用时（嵌套）才单独占位，否则在边上画圆点 */
  v.rels.forEach(function(r){
    if(pos[r.id]) return;                               /* 只有嵌套关系节点才占位 */
    var ref=false;
    v.rels.forEach(function(x){ if(x.args.indexOf(r.id)>=0) ref=true; });
    if(!ref) return;
    var base=pos[r.args[0]]||{x:120,y:120};
    pos[r.id]={x:base.x+52,y:base.y+6};
  });
  return pos;
}
function autoLayout(){ var v=V(); v.pos=layoutNodes(); toast('已自动排版','<p>按论证单元分区重排节点（需求 3.6.1：自动排版避免混乱）。</p>'); paintSvg(); }
function posOf(id){
  var v=V();
  if(!v.pos) v.pos=layoutNodes();
  if(!v.pos[id]) v.pos[id]=Object.assign({},layoutNodes()[id]||{x:80,y:80});
  return v.pos[id];
}
function selectedNodes(){ return [state.selA,state.selB].filter(Boolean); }
function paintSvg(){
  var host=$('#svgHost'); if(!host) return;
  var Wp=Math.max(320,host.clientWidth||420), Hp=Math.max(360,host.clientHeight||560);
  var v=V(), sel=selectedNodes(), s='';
  /* 用真实像素渲染，图随容器尺寸自适应 */
  s+='<svg width="'+Wp+'" height="'+Hp+'" id="theSvg">';
  s+='<defs><marker id="ar" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto">'+
     '<path d="M0,0 L7,3 L0,6 z" fill="#40536a"/></marker>'+
     '<marker id="ar2" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto">'+
     '<path d="M0,0 L7,3 L0,6 z" fill="#1f4e79"/></marker></defs>';
  s+='<g transform="scale('+state.zoom+')">';
  var zoneW=Wp-40;
  s+='<rect class="zone" x="20" y="20" width="'+zoneW+'" height="250" rx="10"/><text class="zone-t" x="30" y="40">论证单元 A1 · 11000 元 / 规范适用</text>';
  s+='<rect class="zone" x="20" y="290" width="'+zoneW+'" height="200" rx="10"/><text class="zone-t" x="30" y="310">论证单元 A2 · 11000 元 / 事实与结论</text>';
  s+='<rect class="zone" x="20" y="510" width="'+zoneW+'" height="170" rx="10"/><text class="zone-t" x="30" y="530">论证单元 A3 · 600 元驳回</text>';
  v.rels.forEach(function(r){
    var f=posOf(r.args[0]), t=posOf(r.args[1]);
    if(!f||!t) return;
    var hi=sel.indexOf(r.id)>=0;
    var mid={x:(f.x+t.x)/2+22,y:(f.y+t.y)/2+14};
    s+='<line class="edge'+(hi?' hi':'')+'" x1="'+(f.x+22)+'" y1="'+(f.y+14)+'" x2="'+(t.x+22)+'" y2="'+(t.y+14)+'"'+
       (r.type==='J'?'':' marker-end="url(#'+(hi?'ar2':'ar')+')"')+'/>';
    s+='<circle cx="'+mid.x+'" cy="'+mid.y+'" r="10" fill="'+
       (r.type==='S'?'#333':(r.type==='A'?'#fff':'#eef2f7'))+'" stroke="#40536a"/>';
    s+='<text x="'+(mid.x-3)+'" y="'+(mid.y+4)+'">'+((r.type==='J'||r.type==='M')?'+':r.type)+'</text>';
  });
  v.props.forEach(function(p){
    var q=posOf(p.id), on=(state.cur===p.id), picked=sel.indexOf(p.id)>=0;
    s+='<g class="node'+(on?' sel':'')+'" data-id="'+p.id+'">'+
       '<rect x="'+q.x+'" y="'+q.y+'" width="44" height="28" rx="6"/>'+
       '<text x="'+(q.x+22)+'" y="'+(q.y+19)+'" text-anchor="middle">'+p.id+'</text>'+
       (picked?'<rect x="'+(q.x-3)+'" y="'+(q.y-3)+'" width="50" height="34" rx="8" fill="none" stroke="#e0a800" stroke-width="2"/>':'')+
       '</g>';
  });
  var nestedSet={};
  v.rels.forEach(function(r){ r.args.forEach(function(a){ if(relById(a)) nestedSet[a]=true; }); });
  v.rels.forEach(function(r){
    if(!nestedSet[r.id]) return;                        /* 只有嵌套关系节点才显示独立圆 */
    var q=posOf(r.id); if(!q) return;
    var picked=sel.indexOf(r.id)>=0;
    s+='<g class="node rel" data-id="'+r.id+'">'+
       '<circle cx="'+(q.x+10)+'" cy="'+(q.y+10)+'" r="12" fill="'+
       (r.type==='S'?'#333':(r.type==='A'?'#fff':'#eef2f7'))+'" stroke="#40536a"/>'+
       '<text x="'+(q.x+6)+'" y="'+(q.y+14)+'">'+((r.type==='J'||r.type==='M')?'+':r.type)+'</text>'+
       (picked?'<circle cx="'+(q.x+10)+'" cy="'+(q.y+10)+'" r="17" fill="none" stroke="#e0a800" stroke-width="2"/>':'')+
       '</g>';
  });
  s+='</g></svg>';
  host.innerHTML=s;
  bindSvg();
}
function bindSvg(){
  var host=$('#svgHost'); if(!host) return;
  var svg=host.querySelector('svg'); if(!svg) return;
  Array.prototype.forEach.call(host.querySelectorAll('g.node'),function(g){
    g.addEventListener('pointerdown',function(ev){
      ev.preventDefault();
      var id=g.dataset.id;
      var pt=svg.createSVGPoint(); pt.x=ev.clientX; pt.y=ev.clientY;
      var loc=pt.matrixTransform(svg.getScreenCTM().inverse());
      var start=Object.assign({},posOf(id)), moved=false;
      function mm(e){
        var p2=svg.createSVGPoint(); p2.x=e.clientX; p2.y=e.clientY;
        var l2=p2.matrixTransform(svg.getScreenCTM().inverse());
        posOf(id).x=start.x+(l2.x-loc.x)/state.zoom;
        posOf(id).y=start.y+(l2.y-loc.y)/state.zoom;
        moved=true;
        g.setAttribute('transform','translate('+(posOf(id).x-start.x)+','+(posOf(id).y-start.y)+')');
      }
      function mu(){
        document.removeEventListener('pointermove',mm);
        document.removeEventListener('pointerup',mu);
        if(moved) paintSvg(); else clickNode(id);
      }
      document.addEventListener('pointermove',mm);
      document.addEventListener('pointerup',mu);
    });
  });
}
function clickNode(id){
  if(state.selA===id) state.selA=null;
  else if(!state.selA){ state.selA=id; if(propById(id)) state.cur=id; }
  else if(!state.selB && id!==state.selA) state.selB=id;
  else { state.selA=id; state.selB=null; }
  if(state.selA&&state.selB) state.step='relation';
  render();
}
function bindSelection(){
  var el=$('#srcText'); if(!el) return;
  el.onmouseup=function(){
    var sel=window.getSelection();
    if(!sel||sel.isCollapsed||!sel.rangeCount) return;
    var r=sel.getRangeAt(0);
    if(!el.contains(r.startContainer)||!el.contains(r.endContainer)) return;
    var pre=document.createRange(); pre.selectNodeContents(el); pre.setEnd(r.startContainer,r.startOffset);
    var s=pre.toString().length, e=s+r.toString().length;
    if(e<=s) return;
    state.selection={s:s,e:e,text:state.doc.text.slice(s,e)};
    if(state.step==='granularity') state.step='element';
    render();
  };
}

/* ============================================================
   7. 模块：冲突裁定
   ============================================================ */
function diffSet(){
  var A=state.versions.A, B=state.versions.B, out=[];
  var n=Math.max(A.props.length,B.props.length);
  for(var i=0;i<n;i++){
    var a=A.props[i], b=B.props[i];
    if(a&&b){
      if(a.s!==b.s||a.e!==b.e) out.push({kind:'标注边界不一致',obj:'P'+(i+1),
        a:'char '+a.s+'–'+a.e,b:'char '+b.s+'–'+b.e,
        why:'指南 2.3：同性质连续子句合并为一个要素；性质不同则各自独立编号。'});
      if((a.type||'')!==(b.type||'')) out.push({kind:'标签选择不一致',obj:'P'+(i+1),
        a:a.type||'待定',b:b.type||'待定',
        why:'指南 4.2.4：SM 须为“具有法律意义的评价判断”；当事人主张的事实归 SF。'});
    }else{
      out.push({kind:'命题缺失',obj:'P'+(i+1),a:a?'有':'未标注',b:b?'有':'未标注',why:'一方未建立该要素。'});
    }
  }
  var ea=A.rels.map(function(r){return exprOf(r);}).join(' | ');
  var eb=B.rels.map(function(r){return exprOf(r);}).join(' | ');
  if(ea!==eb) out.push({kind:'关系结构不一致',obj:'P4,P5 → P6',
    a:'S(M(J(P4,P5),P2),P6)',b:'S(P4,P6) + S(P5,P6)',
    why:'指南 5.3.3：多个命题须共同成立方能支持目标命题时为组合关系，不得拆为独立支持。'});
  if(eb.indexOf('S(P11,P13)')<0) out.push({kind:'关系缺失',obj:'P11 → P13',a:'S(P11,P13)',b:'未标注',
    why:'“证据不足以证明其主张”是“不予支持”的直接理由，属必要关系。'});
  return out;
}
function viewAdjudicate(){
  var A=state.versions.A, B=state.versions.B;
  var noAuto=state.noAuto, diffs=noAuto?[]:diffSet();
  var h='<div class="card"><h3>冲突解决（UC-06 关系裁定 / UC-08 冲突解决）</h3>'+
    '<p class="muted">需求：<b>不由系统自动判定差异归属</b>，而是并排展示各版本结果、由裁定者人工比对后重标或选择某一结果。差异线索可开关。</p>'+
    '<p><button onclick="toggleAuto()">'+(noAuto?'开启差异线索':'关闭差异线索（纯人工比对）')+'</button> '+
    '<button onclick="submitToExpert()">提交专家裁决</button> '+
    '<button class="primary" onclick="finalizeAll()">确认定稿（进入最终库）</button></p>'+
    '<div class="row"><div class="col"><div class="kv">'+
      '<b>张三版</b><span>'+A.props.length+' 要素 · '+A.rels.length+' 关系</span>'+
      '<b>李四版</b><span>'+B.props.length+' 要素 · '+B.rels.length+' 关系</span>'+
      '<b>差异项</b><span>'+(noAuto?'<span class="muted">已关闭自动线索</span>':diffs.length+' 处（'+diffs.map(function(d){return d.kind;}).join('、')+'）')+'</span>'+
      '<b>裁定者</b><span>'+esc(state.tasks[0].adjudicator)+'</span>'+
      '<b>最终版本</b><span>'+(state.final?'<span class="ok">已定稿</span>':'<span class="warn">未定稿</span>')+'</span>'+
    '</div></div>'+
    '<div class="col"><p class="tiny">裁定记录写入版本库：冲突项、各版本取值、裁定结果、裁定人、理由、时间。</p></div>'+
  '</div></div>';

  if(!noAuto&&diffs.length){
    h+='<div class="card"><h3>差异清单（按标签 / 关系 / 边界分类）</h3><table>'+
      '<tr><th style="width:50px">编号</th><th style="width:126px">差异类型</th><th style="width:104px">对象</th>'+
      '<th>张三版</th><th>李四版</th><th style="width:250px">裁定</th></tr>'+
      diffs.map(function(d,i){
        var p=state.picked[i]||'';
        return '<tr class="diffrow"><td class="mono">D'+(i+1)+'</td><td>'+esc(d.kind)+'</td><td class="mono">'+esc(d.obj)+'</td>'+
          '<td>'+esc(d.a)+'</td><td>'+esc(d.b)+'</td><td>'+
          '<button class="'+(p==='A'?'primary':'')+'" onclick="pickDiff('+i+',\'A\')">采纳张三</button> '+
          '<button class="'+(p==='B'?'primary':'')+'" onclick="pickDiff('+i+',\'B\')">采纳李四</button> '+
          '<button class="'+(p==='R'?'primary':'')+'" onclick="pickDiff('+i+',\'R\')">重标</button>'+
          '<div class="tiny" style="margin-top:3px">理由：<input style="width:96%" placeholder="可引用指南条目" value="'+
          esc(state.reasons[i]||'')+'" oninput="setReason('+i+',this.value)"></div></td></tr>';
      }).join('')+'</table>'+
      '<p class="tiny" style="margin-top:6px">每条差异都给出指南依据，防止凭印象裁定。</p></div>'+
      '<div class="card"><h3>差异依据（指南原文）</h3><ul class="muted">'+
      diffs.map(function(d,i){ return '<li><b>D'+(i+1)+'</b> '+esc(d.why)+'</li>'; }).join('')+'</ul></div>';
  }else{
    h+='<div class="card"><h3>人工比对视图（三列并排）</h3>'+
      '<p class="muted">'+(noAuto?'已关闭自动差异线索，请人工逐条比对。':'当前无待裁定差异。')+'</p>'+
      threeWayCompare()+'</div>';
  }
  if(state.ledger.length){
    h+='<div class="card"><h3>疑难问题台账</h3><table><tr><th>时间</th><th>类型</th><th>分歧</th><th>结论 / 处理</th></tr>'+
      state.ledger.map(function(x){ return '<tr><td class="tiny">'+esc(x.at)+'</td><td>'+esc(x.kind)+'</td><td>'+esc(x.q)+'</td><td>'+esc(x.ans)+'</td></tr>'; }).join('')+
      '</table></div>';
  }
  return h;
}
function threeWayCompare(){
  var A=state.versions.A,B=state.versions.B,F=state.final;
  var max=Math.max(A.props.length,B.props.length,F?F.props.length:0), rows='';
  for(var i=0;i<max;i++){
    var a=A.props[i],b=B.props[i],f=F?F.props[i]:null;
    var bad=(a&&b&&a.type!==b.type)?' class="diffrow"':'';
    rows+='<tr'+bad+'><td class="mono">P'+(i+1)+'</td>'+
      '<td>'+(a?tagHtml(a.type)+' '+esc(state.doc.text.slice(a.s,a.e)).slice(0,14)+'…':'<span class="muted">—</span>')+'</td>'+
      '<td>'+(b?tagHtml(b.type)+' '+esc(state.doc.text.slice(b.s,b.e)).slice(0,14)+'…':'<span class="muted">—</span>')+'</td>'+
      '<td>'+(f?tagHtml(f.type):'<span class="muted">未定稿</span>')+'</td></tr>';
  }
  return '<table><tr><th style="width:48px">序号</th><th>张三版</th><th>李四版</th><th style="width:140px">最终版</th></tr>'+rows+'</table>';
}
function toggleAuto(){ state.noAuto=!state.noAuto; render(); }
function setReason(i,v){ state.reasons[i]=v; }
function pickDiff(i,who){
  state.picked[i]=who;
  if(!state.reasons[i]){
    var d=diffSet()[i];
    state.reasons[i]= d ? (d.kind==='标签选择不一致'?'指南 4.2.4：评价部分在 P12/P13，P10 为当事人主张的事实'
      : d.kind==='关系结构不一致'?'指南 5.3.3：须共同成立方构成支持，属组合关系'
      : '依指南对应条目裁定') : '';
  }
  toast('已记录裁定','<p>D'+(i+1)+' → '+(who==='A'?'采纳张三版':(who==='B'?'采纳李四版':'由裁定者重标'))+'</p>'+
    '<p class="muted">理由：'+esc(state.reasons[i])+'（可在输入框修改）</p>');
  render();
}
function submitToExpert(){
  state.ledger.push({at:nowStr(), kind:'专家裁决', q:'P4、P5 → P6 是组合关系还是两个独立支持关系',
    ans:'结论：按指南 5.3.3 认定为组合关系；线下讨论 3 人参与，线上登记生效'});
  toast('已提交专家裁决','<p>分歧进入疑难问题台账，等待线下讨论后线上确认。</p>'+
    '<p class="muted">Q13 的答复：线下讨论结果在本系统登记确认。</p>');
  render();
}
function finalizeAll(){
  var diffs=diffSet(), miss=[];
  diffs.forEach(function(d,i){ if(!state.picked[i]) miss.push(i); });
  if(miss.length){ toast('尚未完成裁定','<p>还有 '+miss.length+' 处差异未裁定（D'+miss.map(function(i){return i+1;}).join('、D')+'）。</p>'+
    '<p class="muted">一致即自动进入最终库；不一致处须逐条裁定。</p>'); return; }
  var finalProps=state.versions.A.props.map(function(p,i){
    var d=diffs[i], q=Object.assign({},p);
    if(d&&state.picked[i]==='B'){ var b=state.versions.B.props[i]; if(b) q.type=b.type; }
    return q;
  });
  state.final={props:finalProps, rels:state.versions.A.rels.map(function(r){ return Object.assign({},r,{args:r.args.slice()}); })};
  state.closed=true;
  state.ledger.push({at:nowStr(), kind:'裁定定稿', q:diffs.length+' 处差异', ans:'全部裁定完成，最终版本进入最终库'});
  toast('已定稿','<p>'+diffs.length+' 处差异已全部裁定，最终版本进入最终库。</p>'+
    '<p class="muted">按需求：进入结果输出后流程不可回退，数据可查看不可修改。</p>');
  render();
}

/* ============================================================
   8. 模块：质量看板
   ============================================================ */
function consistency(){
  var A=state.versions.A,B=state.versions.B,n=Math.max(A.props.length,B.props.length),same=0;
  for(var i=0;i<n;i++){ var a=A.props[i],b=B.props[i]; if(a&&b&&a.type===b.type) same++; }
  var ea=A.rels.map(function(r){return exprOf(r);}), eb=B.rels.map(function(r){return exprOf(r);}), rs=0;
  ea.forEach(function(e){ if(eb.indexOf(e)>=0) rs++; });
  return {granularity:Math.abs(A.props.length-B.props.length)/n,
          labelRate:same/n, relRate:rs/Math.max(ea.length,eb.length)};
}
function viewQuality(){
  var c=consistency(), high=[];
  state.versions.A.props.forEach(function(p,i){
    var b=state.versions.B.props[i];
    if(b&&p.type!==b.type) high.push({obj:p.id,a:p.type,b:b.type});
  });
  return '<div class="card"><h3>一致性指标（指南 8.3）</h3><div class="row">'+
    '<div class="col"><div class="kv">'+
      '<b>颗粒度差异率</b><span class="'+(c.granularity>0.1?'warn':'ok')+'">'+(c.granularity*100).toFixed(1)+'%　'+
        (c.granularity>0.1?'（&gt;10% 需退回重切）':'（≤10%，通过）')+'</span>'+
      '<b>标签一致率</b><span class="'+(c.labelRate>=0.9?'ok':'warn')+'">'+(c.labelRate*100).toFixed(1)+'%</span>'+
      '<b>关系一致率</b><span class="'+(c.relRate>=0.9?'ok':'warn')+'">'+(c.relRate*100).toFixed(1)+'%</span>'+
      '<b>已提交版本</b><span>'+(state.versions.A.submitted?'张三 ':'')+(state.versions.B.submitted?'李四':'')+'</span>'+
    '</div></div>'+
    '<div class="col"><p class="muted">一致性检验嵌入标注全过程，而不只是事后统计指标。一致率偏低时应回流到“试标—指南校准”。</p>'+
    '<p><button onclick="showCalibration()">查看指南校准建议</button></p></div></div></div>'+
  '<div class="card"><h3>高分歧标签（需重点培训）</h3>'+
    (high.length?'<table><tr><th>对象</th><th>张三版</th><th>李四版</th><th>建议</th></tr>'+
      high.map(function(x){ return '<tr class="diffrow"><td class="mono">'+esc(x.obj)+'</td><td>'+tagHtml(x.a)+'</td><td>'+tagHtml(x.b)+
        '</td><td class="muted">回到指南 4.2.4 与标志性表述重新确认</td></tr>'; }).join('')+'</table>'
      :'<p class="muted">当前无标签分歧。</p>')+'</div>'+
  '<div class="card"><h3>疑难问题台账</h3>'+
    (state.ledger.length?'<table><tr><th>时间</th><th>类型</th><th>分歧</th><th>结论 / 处理</th></tr>'+
      state.ledger.map(function(x){ return '<tr><td class="tiny">'+esc(x.at)+'</td><td>'+esc(x.kind)+'</td><td>'+esc(x.q)+'</td><td>'+esc(x.ans)+'</td></tr>'; }).join('')+'</table>'
      :'<p class="muted">暂无记录。裁定过程中的典型分歧会登记在这里，并定期反馈给标注员。</p>')+'</div>'+
  '<div class="card"><h3>操作留痕</h3><p class="muted">标注过程支持留痕（可选），但最终只保存最后一次提交的结果。</p>'+
    '<table><tr><th>时间</th><th>操作</th><th>对象</th><th>操作人</th></tr>'+
    [['指南导入','v'+state.guideVer,state.user],['任务创建','T-001',state.user],
     ['要素标注','P1–P'+props().length,state.versions[state.currentVersion].by],
     ['关系标注','R1–R'+rels().length,state.versions[state.currentVersion].by]]
    .map(function(r){ return '<tr><td class="tiny">'+nowStr()+'</td><td>'+r[0]+'</td><td class="mono">'+r[1]+'</td><td>'+r[2]+'</td></tr>'; }).join('')+
    '</table></div>';
}
function showCalibration(){
  toast('指南校准建议','<ul>'+
    '<li>“当事人主张的事实”与“法院的评价”易混：建议补一条判别句（含评价动词 → SM）。</li>'+
    '<li>“组合关系”与“多个独立支持”是最高分歧点：建议在试标语料中固定 2–3 个正反例。</li>'+
    '<li>文本边界（差一个字算不算不一致）建议明确到标点级别。</li></ul>'+
    '<p class="muted">指南 8.2.2：试标阶段的目的不是产出数据，而是暴露高分歧标签、细化标注规则。</p>');
}

/* ============================================================
   9. 模块：教学比对
   ============================================================ */
function viewTeaching(){
  var t=state.teaching, h='<div class="card"><h3>教学比对模式（独立入口）</h3>'+
    '<p class="muted">场景：教师先标出标准样例；学生在独立入口标注；最后把学生结果与标准结果比对。'+
    '学生改动只保存在练习数据里，不污染正式标注库。</p>'+
    '<p><button class="primary" onclick="teacherAnswer()">① 教师发布标准样例</button> '+
    '<button onclick="studentDo()">② 学生独立标注（模拟）</button> '+
    '<button onclick="compareNow()">③ 与标准结果比对</button></p></div>';
  if(t.answer){
    h+='<div class="card"><h3>标准样例（教师）</h3><table><tr><th style="width:52px">序号</th><th>文本</th><th style="width:90px">标签</th></tr>'+
      t.answer.map(function(p){ return '<tr><td class="mono">'+p.id+'</td><td>'+esc(state.doc.text.slice(p.s,p.e))+'</td><td>'+tagHtml(p.type)+'</td></tr>'; }).join('')+
      '</table></div>';
  }
  if(t.student){
    h+='<div class="card"><h3>学生标注结果（练习数据）</h3><table><tr><th style="width:52px">序号</th><th>文本</th><th style="width:90px">标签</th></tr>'+
      t.student.map(function(p){ return '<tr><td class="mono">'+p.id+'</td><td>'+esc(state.doc.text.slice(p.s,p.e))+'</td><td>'+tagHtml(p.type)+'</td></tr>'; }).join('')+
      '</table></div>';
  }
  if(t.compare){
    h+='<div class="card"><h3>比对结果与错题集</h3>'+
      '<p>一致率：<b class="'+(t.compare.rate>=0.8?'ok':'warn')+'">'+(t.compare.rate*100).toFixed(1)+'%</b>　差异 '+t.compare.items.length+' 处</p>'+
      '<table><tr><th style="width:52px">序号</th><th>文本</th><th style="width:78px">标准</th><th style="width:78px">学生</th><th>错误类型</th></tr>'+
      t.compare.items.map(function(x){
        return '<tr class="diffrow"><td class="mono">'+x.id+'</td><td>'+esc(state.doc.text.slice(x.s,x.e))+'</td>'+
          '<td>'+tagHtml(x.std)+'</td><td>'+tagHtml(x.stu)+'</td><td class="muted">'+esc(x.kind)+'</td></tr>';
      }).join('')+'</table>'+
      '<h4>错题类型分布与建议</h4><p class="muted">'+t.compare.summary+'</p></div>';
  }
  return h;
}
function teacherAnswer(){
  state.teaching.answer=state.versions.A.props.map(function(p){ return {id:p.id,s:p.s,e:p.e,type:p.type}; });
  toast('标准样例已发布','<p>教师标注的 '+state.teaching.answer.length+' 个要素已作为标准答案发布给学生。</p>'); render();
}
function studentDo(){
  var std=state.teaching.answer||state.versions.A.props;
  state.teaching.student=std.map(function(p,i){
    var q=Object.assign({},p);
    if(i===9) q.type='SM';   /* 学生把 P10 标成 SM（典型错误） */
    if(i===5) q.type='SF';   /* 学生把 P6 标成 SF */
    return q;
  });
  toast('学生标注完成','<p>学生在独立入口完成 '+state.teaching.student.length+' 个要素的标注（练习数据，不写入正式库）。</p>'); render();
}
function compareNow(){
  var std=state.teaching.answer, stu=state.teaching.student;
  if(!std||!stu){ toast('缺少数据','<p>请先执行 ① 与 ② 。</p>'); return; }
  var items=[], same=0;
  std.forEach(function(p,i){
    var q=stu[i];
    if(q&&p.type===q.type) same++;
    else if(q){
      var kind=((p.type==='SF'&&q.type==='SM')||(p.type==='SM'&&q.type==='SF'))?'事实/规范混淆（最高频错误）'
        :(p.type&&q.type&&l1Of(p.type)===l1Of(q.type))?'子类型选择偏差':'标签选择不一致';
      items.push({id:p.id,s:p.s,e:p.e,std:p.type,stu:q.type,kind:kind});
    }
  });
  state.teaching.compare={rate:same/std.length,items:items,
    summary:'事实/规范混淆 → 回到指南 4.2.2 的两个维度重新判断；子类型偏差 → 对照 GM 子类型的标志性表述。'};
  toast('比对完成','<p>一致率 '+(same/std.length*100).toFixed(1)+'%，差异 '+items.length+' 处。</p>'+
    '<p class="muted">“事实/规范混淆”正是教学最需要暴露的错误。</p>'); render();
}

/* ============================================================
   10. 模块：导出与归档
   ============================================================ */
function finalProps(){ return state.final?state.final.props:state.versions.A.props; }
function finalRels(){ return state.final?state.final.rels:state.versions.A.rels; }
function buildJson(){
  var g=state.guides.filter(function(x){return x.ver===state.guideVer;})[0]||state.guides[0];
  var c=consistency();
  return {
    schema_version:'1.0', guide_version:g.ver,
    document:{case_no:state.caseInfo['案号'],court:state.caseInfo['裁判法院'],court_level:state.caseInfo['法院层级'],
      instance:state.caseInfo['审级'],judgment_date:state.caseInfo['裁判日期'],case_nature:state.caseInfo['案件性质'],
      cause:state.caseInfo['案由'],result_type:state.caseInfo['裁判结果类型'],case_type:state.caseInfo['案例类型'],
      reasoning_text:state.doc.text,reasoning_span:state.doc.range},
    elements:finalProps().map(function(p){ return {id:p.id,type:p.type||null,text:state.doc.text.slice(p.s,p.e),
      char_span:{start:p.s,end:p.e},argument_id:p.arg||'A1'}; }),
    relations:finalRels().map(function(r){ return {id:r.id,type:r.type,args:r.args,arg_expr:exprOf(r),argument_id:r.arg||'A1'}; }),
    adjudication:{adjudicator:state.tasks[0].adjudicator,conflicts:diffSet().length,ledger:state.ledger,
      consistency:{granularity_diff_rate:Number(c.granularity.toFixed(3)),
                   label_agreement:Number(c.labelRate.toFixed(3)),
                   relation_agreement:Number(c.relRate.toFixed(3))}},
    export:{exported_by:state.user,exported_at:nowStr(),guide_version:g.ver},
    immutable:!!state.final
  };
}
function viewExport(){
  var j=buildJson();
  return '<div class="card"><h3>结果输出（UC-15 结果导出与再导入）</h3>'+
    '<p class="muted">导出内容：JSON（字符索引 + 标签层级 + 关系定义，供模型训练）、CSV（命题列表 + 关系）、'+
    '论证图示（SVG）、标注报告（Markdown）。导出后数据<b>可查看不可修改</b>。</p>'+
    '<div class="row"><div class="col"><div class="kv">'+
      '<b>文件名前缀</b><span><input id="expName" value="劳务合同纠纷-第一批-D18909" style="width:100%"></span>'+
      '<b>指南版本</b><span class="mono">'+esc(state.guideVer)+'（写入导出包）</span>'+
      '<b>数据状态</b><span>'+(state.final?'<span class="ok">已定稿</span>':'<span class="warn">未定稿（导出当前张三版）</span>')+'</span>'+
    '</div>'+
    '<p style="margin-top:10px"><label class="chk"><input type="checkbox" id="ckJson" checked> JSON</label>'+
    '<label class="chk"><input type="checkbox" id="ckXls" checked> CSV</label>'+
    '<label class="chk"><input type="checkbox" id="ckSvg" checked> 图示 SVG</label>'+
    '<label class="chk"><input type="checkbox" id="ckMd" checked> 标注报告 MD</label></p>'+
    '<p><button class="primary" onclick="doExport()">开始导出（真实下载）</button> '+
    '<button onclick="importBack()">再导入（模拟）</button></p>'+
    '<div id="expProg" class="tiny"></div></div>'+
    '<div class="col"><h4>导出记录（记录下载人）</h4>'+
    (state.exports.length?'<table><tr><th>时间</th><th>用户</th><th>文件</th><th>指南版本</th></tr>'+
      state.exports.map(function(e){ return '<tr><td class="tiny">'+esc(e.at)+'</td><td>'+esc(e.by)+'</td>'+
        '<td class="tiny mono">'+esc(e.files)+'</td><td class="mono">'+esc(e.guide)+'</td></tr>'; }).join('')+'</table>'
      :'<p class="muted">尚无导出记录。</p>')+
    '</div></div></div>'+

  '<div class="card"><h3>data.json（预览）</h3><pre>'+esc(JSON.stringify({
    schema_version:j.schema_version,guide_version:j.guide_version,
    document:{case_no:j.document.case_no,reasoning_span:j.document.reasoning_span,
              reasoning_text:j.document.reasoning_text.slice(0,40)+'…'},
    elements:j.elements.slice(0,4).concat([{id:'…',note:'共 '+j.elements.length+' 条要素'}]),
    relations:j.relations.slice(0,3).concat([{id:'…',note:'共 '+j.relations.length+' 条关系'}]),
    adjudication:j.adjudication,immutable:j.immutable},null,2))+'</pre></div>'+

  '<div class="card"><h3>propositions.csv（命题列表）</h3><table>'+
    '<tr><th style="width:56px">序号</th><th>要素内容</th><th style="width:74px">类型</th><th style="width:64px">字符起</th>'+
    '<th style="width:64px">字符止</th><th style="width:56px">单元</th></tr>'+
    j.elements.map(function(p){ return '<tr><td class="mono">'+p.id+'</td><td>'+esc(p.text)+'</td><td>'+tagHtml(p.type)+'</td>'+
      '<td class="mono">'+p.char_span.start+'</td><td class="mono">'+p.char_span.end+'</td><td class="mono">'+esc(p.argument_id)+'</td></tr>'; }).join('')+
  '</table></div>'+

  '<div class="card"><h3>relation_matrix.csv（关系矩阵）</h3>'+relMatrixHtml(j)+'</div>';
}
function relMatrixHtml(j){
  var ids=j.elements.map(function(e){return e.id;}), m={};
  j.relations.forEach(function(r){
    var a=r.args[0], b=r.args[1];
    if(!m[a]) m[a]={};
    m[a][b]=(m[a][b]?m[a][b]+'+':'')+r.type;
  });
  var h='<table><tr><th>支持者 \\ 被支持者</th>'+ids.map(function(i){return '<th>'+i+'</th>';}).join('')+'</tr>';
  ids.forEach(function(a){
    h+='<tr><th>'+a+'</th>';
    ids.forEach(function(b){ h+='<td class="mono tiny">'+((m[a]&&m[a][b])?m[a][b]:'')+'</td>'; });
    h+='</tr>';
  });
  return h+'</table>';
}
function svgString(){
  var v=V(), pos=v.pos||layoutNodes(), s='';
  s+='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 700" width="920" height="1400">';
  s+='<defs><marker id="ah" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto">'+
     '<path d="M0,0 L7,3 L0,6 z" fill="#40536a"/></marker></defs>';
  s+='<rect width="100%" height="100%" fill="#fff"/>';
  s+='<rect x="20" y="20" width="420" height="250" rx="10" fill="#f7fafd" stroke="#e2e9f1"/><text x="30" y="40" font-size="11" fill="#8494a4">论证单元 A1</text>';
  s+='<rect x="20" y="290" width="420" height="200" rx="10" fill="#f7fafd" stroke="#e2e9f1"/><text x="30" y="310" font-size="11" fill="#8494a4">论证单元 A2</text>';
  s+='<rect x="20" y="510" width="420" height="170" rx="10" fill="#f7fafd" stroke="#e2e9f1"/><text x="30" y="530" font-size="11" fill="#8494a4">论证单元 A3</text>';
  v.rels.forEach(function(r){
    var f=pos[r.args[0]], t=pos[r.args[1]]; if(!f||!t) return;
    s+='<line x1="'+(f.x+22)+'" y1="'+(f.y+14)+'" x2="'+(t.x+22)+'" y2="'+(t.y+14)+'" stroke="#40536a" stroke-width="1.4"'+
       (r.type==='J'?'':' marker-end="url(#ah)"')+'/>';
    s+='<circle cx="'+((f.x+t.x)/2+22)+'" cy="'+((f.y+t.y)/2+14)+'" r="10" fill="'+
       (r.type==='S'?'#333':(r.type==='A'?'#fff':'#eef2f7'))+'" stroke="#40536a"/>';
  });
  v.props.forEach(function(p){
    var q=pos[p.id]; if(!q) return;
    s+='<rect x="'+q.x+'" y="'+q.y+'" width="44" height="28" rx="6" fill="#fff" stroke="#5a7fb5" stroke-width="1.6"/>'+
       '<text x="'+(q.x+22)+'" y="'+(q.y+19)+'" text-anchor="middle" font-size="12" font-weight="700" fill="#16273a">'+p.id+'</text>';
  });
  return s+'</svg>';
}
function csvOf(rows){ return rows.map(function(r){ return r.map(function(c){ return '"'+String(c==null?'':c).replace(/"/g,'""')+'"'; }).join(','); }).join('\r\n'); }
function download(name,content,mime){
  var blob=new Blob(['\ufeff'+content],{type:mime||'text/plain;charset=utf-8'});
  var a=document.createElement('a');
  a.href=URL.createObjectURL(blob); a.download=name;
  document.body.appendChild(a); a.click();
  setTimeout(function(){ URL.revokeObjectURL(a.href); a.remove(); },1500);
}
function doExport(){
  var prefix=($('#expName')&&$('#expName').value)||'annotation-export';
  var want={json:!!($('#ckJson')&&$('#ckJson').checked),xls:!!($('#ckXls')&&$('#ckXls').checked),
            svg:!!($('#ckSvg')&&$('#ckSvg').checked),md:!!($('#ckMd')&&$('#ckMd').checked)};
  var files=[], prog=$('#expProg');
  function tick(pct,label){ if(prog) prog.innerHTML='导出进度 '+pct+'% — '+label; }
  tick(5,'准备');
  setTimeout(function(){
    if(want.json){ download(prefix+'.json',JSON.stringify(buildJson(),null,2),'application/json'); files.push('data.json'); }
    tick(30,'data.json');
    setTimeout(function(){
      if(want.xls){
        var el=finalProps();
        download(prefix+'-propositions.csv',csvOf([['序号','要素内容','类型','字符起','字符止','论证单元']].concat(
          el.map(function(p){ return [p.id,state.doc.text.slice(p.s,p.e),p.type||'',p.s,p.e,p.arg||'A1']; }))),'text/csv');
        download(prefix+'-relations.csv',csvOf([['关系编号','类型','形式化表达','参数1','参数2','论证单元']].concat(
          finalRels().map(function(r){ return [r.id,r.type,exprOf(r),r.args[0],r.args[1]||'',r.arg||'A1']; }))),'text/csv');
        files.push('propositions.csv','relations.csv');
      }
      tick(55,'CSV');
      setTimeout(function(){
        if(want.svg){ download(prefix+'-diagram.svg',svgString(),'image/svg+xml'); files.push('diagram.svg'); }
        tick(80,'diagram.svg');
        setTimeout(function(){
          if(want.md){
            var md=['# 法律论证结构标注报告','','- 案号：'+state.caseInfo['案号'],'- 法院：'+state.caseInfo['裁判法院'],
              '- 案由：'+state.caseInfo['案由'],'- 指南版本：'+state.guideVer,'- 导出时间：'+nowStr(),
              '- 导出人：'+state.user,'','## 命题列表',''].concat(
              finalProps().map(function(p){ return '- **'+p.id+'**（'+(p.type||'待定')+'，char '+p.s+'–'+p.e+'）：'+state.doc.text.slice(p.s,p.e); }))
              .concat(['','## 关系',''].concat(finalRels().map(function(r){ return '- `'+exprOf(r)+'` — '+(r.note||''); })))
              .concat(['','## 裁定与台账',''].concat(state.ledger.length?state.ledger.map(function(x){
                return '- '+x.at+' '+x.kind+'：'+x.q+' → '+x.ans; }):['（无）']))
              .concat(['','## 一致性指标','```json',JSON.stringify(consistency(),null,2),'```','','> 本报告由原型导出；数据只读。'])
              .join('\n');
            download(prefix+'-report.md',md,'text/markdown'); files.push('report.md');
          }
          tick(100,'完成');
          state.exports.push({at:nowStr(),by:state.user,files:files.join(', '),guide:state.guideVer});
          state.closed=true;
          toast('导出完成','<p>已生成 '+files.length+' 个文件并开始下载：</p><p class="mono tiny">'+files.join('<br>')+'</p>'+
            '<p class="muted">按需求：导出后数据可查看不可修改；导出记录已保存（含下载人）；包内标注指南版本 '+esc(state.guideVer)+'。</p>');
          render();
        },400);
      },400);
    },400);
  },300);
}
function importBack(){
  toast('再导入（模拟）','<p>选择此前导出的 <b>data.json</b> 即可恢复标注数据，用于跨批次合并或复现。</p>'+
    '<p class="muted">需求：导出之后的结果支持再导入。</p>');
}
function viewLedger(){
  return '<div class="card"><h3>疑难问题台账与版本记录</h3>'+
    (state.ledger.length?'<table><tr><th>时间</th><th>类型</th><th>分歧</th><th>结论 / 处理</th></tr>'+
      state.ledger.map(function(x){ return '<tr><td class="tiny">'+esc(x.at)+'</td><td>'+esc(x.kind)+'</td><td>'+esc(x.q)+'</td><td>'+esc(x.ans)+'</td></tr>'; }).join('')+'</table>'
      :'<p class="muted">暂无记录。</p>')+
    '<h4>一致性指标</h4><pre>'+esc(JSON.stringify(consistency(),null,2))+'</pre>'+
    '<h4>当前版本数据规模</h4><p class="mono tiny">'+esc(state.currentVersion)+' 版：'+props().length+' 要素 / '+rels().length+' 关系</p></div>';
}

/* ============================================================
   11. 渲染入口 / 三栏调节 / 路由
   ============================================================ */
var VIEWS={overview:viewOverview,guide:viewGuide,task:viewTask,work:viewWork,adj:viewAdjudicate,
           quality:viewQuality,teach:viewTeaching,exp:viewExport,ledger:viewLedger};
var NAV=[['overview','项目概览'],['guide','指南管理'],['task','任务管理'],['work','标注工作台'],
         ['adj','冲突裁定'],['quality','质量看板'],['teach','教学比对'],['exp','导出与归档'],['ledger','台账与记录']];

function shell(){
  return '<div class="shell">'+
    '<nav class="rail"><div class="brand">法律论证结构标注系统<small>原型 v2.0 · 功能全覆盖</small></div>'+
    '<div class="sec">功能模块</div>'+
    NAV.map(function(n){ return '<button class="'+(state.mod===n[0]?'on':'')+'" onclick="setMod(\''+n[0]+'\')">'+n[1]+'</button>'; }).join('')+
    '<div class="sec">辅助</div>'+
    '<button onclick="openUC()">系统用例图</button>'+
    '<button onclick="showShortcuts()">操作提示</button>'+
    '<button onclick="resetAll()">重置演示数据</button></nav>'+
    '<div class="main"><div class="topbar"><b id="modTitle"></b>'+
      '<span class="who">身份：<select onchange="switchRole(this.value)">'+
        ['管理员','标注员','裁定者','教师','学生','领域专家'].map(function(r){
          return '<option '+(state.role===r?'selected':'')+'>'+r+'</option>'; }).join('')+
      '</select> '+esc(state.user)+'</span>'+
      '<span class="who">指南版本 <span class="mono">'+esc(state.guideVer)+'</span></span>'+
      '<span class="who">标签集 <span class="mono">LS-'+esc(state.guideVer)+'</span></span>'+
      (state.closed?'<span class="warn tiny">数据只读（已定稿/已导出）</span>':'')+
      '<span style="margin-left:auto" class="tiny">原文 '+state.doc.text.length+' 字符 · 要素 '+props().length+' · 关系 '+rels().length+'</span>'+
    '</div><div class="wrap" id="view"></div></div></div>';
}
function switchRole(r){
  state.role=r;
  state.user=(r==='学生')?'学生甲':(r==='标注员')?'张三':(r==='裁定者')?'王五':(r==='领域专家')?'赵博士':'王老师';
  render();
}
function render(){
  var root=$('#app'); if(!root) return;
  root.innerHTML=shell();
  var t=$('#modTitle'), nav=NAV.filter(function(n){ return n[0]===state.mod; })[0];
  if(t) t.textContent=nav?nav[1]:'';
  $('#view').innerHTML=(VIEWS[state.mod]||function(){ return '<p class="muted">未实现</p>'; })();
  if(state.mod==='work'){
    paintSource(); paintList(); paintOps(); paintSvg(); bindSelection(); bindGutters();
    var z=$('#zoomVal'); if(z) z.textContent=Math.round(state.zoom*100)+'%';
  }
}
function bindGutters(){
  var work=$('#work'); if(!work) return;
  Array.prototype.forEach.call(work.querySelectorAll('.gutter'),function(g){
    g.addEventListener('pointerdown',function(ev){
      ev.preventDefault();
      var cols=[26,34,40], idx=parseInt(g.dataset.g,10)-1;
      var rect=work.getBoundingClientRect(), startX=ev.clientX, start=cols.slice();
      function mm(e){
        var dcm=(e.clientX-startX)/rect.width*100;
        var a=start[idx]+dcm, b=start[idx+1]-dcm;
        if(a<14) a=14; if(b<14) b=14;
        cols[idx]=a; cols[idx+1]=b;
        work.style.gridTemplateColumns=cols[0]+'% '+cols[1]+'% '+cols[2]+'%';
      }
      function mu(){ document.removeEventListener('pointermove',mm); document.removeEventListener('pointerup',mu); }
      document.addEventListener('pointermove',mm); document.addEventListener('pointerup',mu);
    });
  });
}
function showShortcuts(){
  toast('操作提示','<ul>'+
    '<li><b>建立命题</b>：左侧原文拖动选择 → 中间“建立命题（分配序号）” → 选一级/二级标签。</li>'+
    '<li><b>建立关系</b>：右侧图示区依次点击两个节点 → 中间选关系类型；节点可以是命题，也可以是已有关系（嵌套）。</li>'+
    '<li><b>移动节点</b>：直接拖动方框；松开后位置写回数据（双向联动）。</li>'+
    '<li><b>缩放</b>：图区右上角 －／＋。</li>'+
    '<li><b>调整三栏比例</b>：拖动栏与栏之间的竖条（需求 3.1：界面比例可调节）。</li>'+
    '<li><b>切换身份</b>：右上角下拉框。</li></ul>');
}
function resetAll(){
  initVersions();
  state.cur=null;state.selA=null;state.selB=null;state.selection=null;
  state.final=null;state.closed=false;state.ledger=[];state.exports=[];state.picked={};state.reasons={};
  state.teaching={answer:null,student:null,compare:null};state.zoom=1;state.step='granularity';state.currentVersion='A';
  state.doc.text=SAMPLE; state.doc.range={s:0,e:SAMPLE_LEN}; state.doc.confirmed=false; state.doc.src='智能提取';
  state.guides=[{ver:'v1.2',name:'中文裁判文书说理部分法律论证结构标注与图示指南',
    at:'2026-04-14 10:02',by:'王老师',frozen:true,labels:13,rels:5,snap:'guide-v1.2.pdf'}];
  state.guideVer='v1.2';
  toast('已重置','<p>演示数据恢复到初始状态（v1.2 指南、张三/李四两版、未定稿）。</p>'); render();
}
function openUC(){ $('#ucImg').src='data:image/png;base64,'+UC_B64; $('#ucDlg').showModal(); }

function applyHash(){
  var h=(location.hash||'').replace('#','');
  if(VIEWS[h]) state.mod=h;
  render();
}
window.addEventListener('hashchange',applyHash);
window.addEventListener('resize',function(){ if(state.mod==='work') paintSvg(); });
if(!location.hash) location.hash='#overview';
applyHash();
'''

HTML = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>法律论证结构标注系统 · 原型 v2.0</title>
<style>__CSS__</style>
</head>
<body>
<div id="app"></div>
<dialog id="dlg">
  <div class="dh"><span id="dlgTitle">提示</span><button class="ghost" onclick="closeDlg()">关闭</button></div>
  <div class="db" id="dlgBody"></div>
  <div class="df" id="dlgFoot"><button class="primary" onclick="closeDlg()">知道了</button></div>
</dialog>
<dialog id="ucDlg">  <div class="dh"><span>系统用例图</span><button class="ghost" onclick="document.getElementById('ucDlg').close()">关闭</button></div>
  <div class="db"><img id="ucImg" alt="系统用例图" style="width:100%"></div>
</dialog>
<script>
var UC_B64 = "__UC__";
__JS__
</script>
</body>
</html>
'''

html = HTML.replace('__CSS__', CSS).replace('__JS__', JS).replace('__UC__', UC_B64)
with open(OUT, 'w', encoding='utf-8') as fh:
    fh.write(html)
print('saved', OUT, len(html), 'chars')
