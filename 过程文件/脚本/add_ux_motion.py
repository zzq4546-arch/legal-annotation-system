# -*- coding: utf-8 -*-
"""给 v3.0「明理」原型加一层交互动效（只追加 <style> 与 <script>，不改动既有结构）。

覆盖：
1) 所有按钮：悬停上浮+投影、按下回弹、点击涟漪
2) 侧栏导航：激活竖条滑入、图标微缩放、标签轻移；支持 ↑↓ 键盘切换
3) 模块切换：整体淡入 + 卡片错峰浮入
4) 对话框：打开时缩放淡入、遮罩淡入
5) 提示条 #snackbar：补上原本缺失的样式（固定底部胶囊 + 进出场动效）
6) 表格行 / 命题卡片 / 图形节点 / 输入框 / 拖拽分隔条：悬停与聚焦反馈
7) 保存状态圆点脉冲
8) 全部走 transform/opacity，不触发重排；沿用文件已有的 prefers-reduced-motion 全局降级
"""
import io
import sys

P = r'C:\Users\32354\Documents\deepseek-harness\default-workspace\法律论证标注系统\过程文件\输出\legal-annotation-prototype.html'
MARK = 'ux-motion-v1'

CSS = r"""
<style id="ux-motion-v1">
/* ===== 交互动效层 v1（只做动效与反馈，不改布局尺寸） ===== */

/* 1. 按钮：悬停上浮、按下回弹、涟漪 */
button{position:relative;overflow:hidden;-webkit-tap-highlight-color:transparent;
  transition:background .18s ease,border-color .18s ease,color .18s ease,box-shadow .24s ease,
             transform .2s cubic-bezier(.34,1.4,.64,1)}
button:hover{transform:translateY(-2px);box-shadow:0 8px 18px -10px rgba(38,64,44,.55)}
button:active{transform:translateY(0) scale(.972);transition-duration:.06s}
button.primary:hover{box-shadow:0 10px 24px -10px rgba(46,80,65,.72)}
button.ghost:hover{background:#eef2e9}
button:disabled,button[disabled]{transform:none!important;box-shadow:none!important}

.ux-ripple{position:absolute;border-radius:50%;background:currentColor;opacity:0;
  pointer-events:none;transform:scale(0);animation:uxRipple .62s cubic-bezier(.2,.7,.3,1) forwards}
@keyframes uxRipple{0%{opacity:.30;transform:scale(.12)}60%{opacity:.14}100%{opacity:0;transform:scale(1)}}

button.ux-press{animation:uxPop .34s cubic-bezier(.34,1.56,.64,1)}
@keyframes uxPop{0%{transform:translateY(0) scale(.945)}55%{transform:translateY(-2px) scale(1.02)}
  100%{transform:translateY(-2px) scale(1)}}

/* 2. 侧栏导航 */
.rail button{position:relative;overflow:hidden}
.rail button::after{content:"";position:absolute;left:0;top:50%;width:3px;height:0;
  border-radius:0 3px 3px 0;background:var(--primary);transform:translateY(-50%);opacity:0;
  transition:height .3s cubic-bezier(.34,1.4,.64,1),opacity .2s ease}
.rail button.on::after{height:58%;opacity:1}
.rail button:hover{transform:none;box-shadow:none}
.rail .nav-label{transition:transform .2s ease}
.rail button:hover .nav-label{transform:translateX(2px)}
.rail .nav-icon{transition:transform .24s cubic-bezier(.34,1.4,.64,1),opacity .2s ease}
.rail button:hover .nav-icon{transform:scale(1.08);opacity:.92}
.rail button.on .nav-icon{opacity:1}

/* 3. 模块切换 */
.ux-view-in{animation:uxView .36s cubic-bezier(.22,.8,.26,1) both}
@keyframes uxView{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.ux-rise{animation:uxRise .46s cubic-bezier(.22,.8,.26,1) both}
@keyframes uxRise{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}

/* 4. 对话框 */
dialog[open]{animation:uxDialog .26s cubic-bezier(.22,.9,.3,1.02) both}
@keyframes uxDialog{from{opacity:0;transform:translateY(14px) scale(.97)}to{opacity:1;transform:none}}
dialog::backdrop{animation:uxFade .26s ease both}
@keyframes uxFade{from{opacity:0}to{opacity:1}}

/* 5. 提示条（原本没有任何样式，这里是补全） */
#snackbar{position:fixed;left:50%;bottom:30px;z-index:9999;max-width:min(560px,86vw);
  padding:12px 20px;border-radius:12px;background:#26382c;color:#f2f5ec;font-size:13px;
  line-height:1.6;letter-spacing:.2px;box-shadow:0 18px 44px rgba(18,32,24,.34);
  pointer-events:none;opacity:0;transform:translate(-50%,14px);
  transition:opacity .22s ease,transform .34s cubic-bezier(.22,.9,.3,1.04)}
#snackbar.show{opacity:1;transform:translate(-50%,0)}

/* 6. 保存圆点脉冲 */
.saved-pill.ux-pulse:before{animation:uxDot .9s ease}
@keyframes uxDot{0%{box-shadow:0 0 0 0 rgba(127,154,117,.7)}100%{box-shadow:0 0 0 7px rgba(127,154,117,0)}}

/* 7. 表格 / 命题卡片 / 图形节点 / 输入框 / 分隔条 */
table tr{transition:background .16s ease}
table tr:hover td{background:#f7f9f1}
.pitem{transition:background .18s ease,border-color .18s ease,transform .2s cubic-bezier(.34,1.4,.64,1)}
.pitem:hover{transform:translateX(2px)}
.pitem.cur{animation:uxFlash .55s ease}
@keyframes uxFlash{0%{box-shadow:0 0 0 0 rgba(128,155,91,.5)}100%{box-shadow:0 0 0 10px rgba(128,155,91,0)}}

input,select,textarea{transition:border-color .18s ease,box-shadow .22s ease,background .18s ease}
input:focus,select:focus,textarea:focus{box-shadow:0 0 0 4px rgba(126,155,116,.16);border-color:#9fb590}
button:focus-visible,a:focus-visible,input:focus-visible,select:focus-visible,textarea:focus-visible{
  outline:2.5px solid #7f9b6e;outline-offset:2px}

.node{cursor:pointer}
.node rect{transition:stroke .18s ease,stroke-width .18s ease,fill .18s ease}
.node text{transition:fill .18s ease}
.node:hover rect{stroke:#526f37;stroke-width:2.2}
.node:hover text{fill:#2e5041}
.node.rel:hover rect{fill:#f4f7ea}
.edge{transition:stroke .18s ease,stroke-width .18s ease}

.drop{transition:border-color .2s ease,background .2s ease}
.drop:hover{border-color:#8fab7c;background:#f7fbf4}

.gutter{transition:background .18s ease}
</style>
"""

JS = r"""
<script id="ux-motion-js">
(function(){
  "use strict";
  var doc = document, body = doc.body;
  var mq = window.matchMedia ? window.matchMedia("(prefers-reduced-motion: reduce)") : null;
  function calm(){ return !!(mq && mq.matches); }

  /* 1) 按钮涟漪：指针按下处扩散 */
  doc.addEventListener("pointerdown", function(e){
    if (e.button !== 0 || calm()) return;
    var b = e.target && e.target.closest ? e.target.closest("button") : null;
    if (!b || b.disabled) return;
    var r = b.getBoundingClientRect();
    var size = Math.max(r.width, r.height) * 2;
    var s = doc.createElement("span");
    s.className = "ux-ripple";
    s.style.width = size + "px";
    s.style.height = size + "px";
    s.style.left = (e.clientX - r.left - size / 2) + "px";
    s.style.top  = (e.clientY - r.top  - size / 2) + "px";
    b.appendChild(s);
    window.setTimeout(function(){ if (s.parentNode) s.parentNode.removeChild(s); }, 700);
  }, { passive: true });

  /* 2) 点击回弹 */
  doc.addEventListener("click", function(e){
    var b = e.target && e.target.closest ? e.target.closest("button") : null;
    if (!b || b.disabled || calm()) return;
    b.classList.remove("ux-press");
    void b.offsetWidth;
    b.classList.add("ux-press");
    window.setTimeout(function(){ b.classList.remove("ux-press"); }, 340);
  }, true);

  /* 3) 模块切换：整体淡入 + 卡片错峰浮入（只在切换模块时触发，避免每次重绘都闪） */
  var lastHash = location.hash;
  function items(root){
    return root.querySelectorAll(".page-heading, .hero, .stats, .card");
  }
  function playIn(){
    var view = doc.getElementById("view");
    if (!view || calm()) return;
    view.classList.remove("ux-view-in");
    void view.offsetWidth;
    view.classList.add("ux-view-in");
    if (!view.classList.contains("work-view")) {
      var list = items(view), n = Math.min(list.length, 10), i;
      for (i = 0; i < n; i++) {
        list[i].style.animationDelay = (i * 40) + "ms";
        list[i].classList.add("ux-rise");
      }
      window.setTimeout(function(){
        for (var j = 0; j < n; j++) {
          list[j].classList.remove("ux-rise");
          list[j].style.animationDelay = "";
        }
      }, 1100);
    }
    window.setTimeout(function(){ view.classList.remove("ux-view-in"); }, 520);
  }
  if (typeof window.render === "function") {
    var baseRender = window.render;
    window.render = function(){
      var out = baseRender.apply(this, arguments);
      if (location.hash !== lastHash) { lastHash = location.hash; playIn(); }
      return out;
    };
  }

  /* 4) 点击命题/节点后，让当前项滚入视野 */
  doc.addEventListener("click", function(e){
    var t = e.target && e.target.closest ? e.target.closest(".pitem, .node") : null;
    if (!t) return;
    window.setTimeout(function(){
      var cur = doc.querySelector("#view .pitem.cur");
      if (cur && cur.scrollIntoView) {
        try { cur.scrollIntoView({ block: "nearest", behavior: calm() ? "auto" : "smooth" }); }
        catch (err) { cur.scrollIntoView(false); }
      }
    }, 60);
  }, true);

  /* 5) 保存状态圆点脉冲（文本变化时触发） */
  function pulse(el){
    el.classList.remove("ux-pulse");
    void el.offsetWidth;
    el.classList.add("ux-pulse");
    window.setTimeout(function(){ el.classList.remove("ux-pulse"); }, 900);
  }
  if (window.MutationObserver) {
    new MutationObserver(function(muts){
      for (var i = 0; i < muts.length; i++) {
        var n = muts[i].target;
        var el = n && n.nodeType === 3 ? n.parentElement : n;
        if (el && el.id === "savedLabel") { pulse(el); return; }
      }
    }).observe(body, { childList: true, subtree: true, characterData: true });
  }

  /* 6) 侧栏支持 ↑↓ 键盘移动 */
  doc.addEventListener("keydown", function(e){
    if (e.key !== "ArrowDown" && e.key !== "ArrowUp") return;
    var t = e.target;
    if (!t || !t.closest || !t.closest(".rail")) return;
    var list = Array.prototype.slice.call(doc.querySelectorAll(".rail button"));
    var i = list.indexOf(t);
    if (i < 0) return;
    var j = e.key === "ArrowDown" ? i + 1 : i - 1;
    if (j < 0 || j >= list.length) return;
    e.preventDefault();
    list[j].focus();
  });
})();
</script>
"""

with io.open(P, encoding='utf-8', newline='') as f:
    s = f.read()

if MARK in s:
    print('已存在动效层，未重复写入')
    sys.exit(0)

if '</body>' not in s:
    print('找不到 </body>，未改动')
    sys.exit(1)

s = s.replace('</body>', CSS + JS + '</body>', 1)
with io.open(P, 'w', encoding='utf-8', newline='') as f:
    f.write(s)
print('已写入动效层：CSS %d 字节，JS %d 字节' % (len(CSS.encode('utf-8')), len(JS.encode('utf-8'))))
