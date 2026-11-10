# -*- coding: utf-8 -*-
"""微调动效层：让涟漪更明显、主按钮加扫光、卡片按下有反馈。"""
import io
import sys

P = r'C:\Users\32354\Documents\deepseek-harness\default-workspace\法律论证标注系统\过程文件\输出\legal-annotation-prototype.html'
s = io.open(P, encoding='utf-8').read()

edits = [
    # 1) 涟漪更明显
    ('@keyframes uxRipple{0%{opacity:.30;transform:scale(.12)}60%{opacity:.14}100%{opacity:0;transform:scale(1)}}',
     '@keyframes uxRipple{0%{opacity:.42;transform:scale(.1)}55%{opacity:.20}100%{opacity:0;transform:scale(1)}}'),
    # 2) 主按钮扫光
    ('button.ghost:hover{background:#eef2e9}',
     'button.ghost:hover{background:#eef2e9}\n'
     'button.primary{z-index:0}\n'
     'button.primary::before{content:"";position:absolute;inset:0;pointer-events:none;z-index:-1;\n'
     '  background:linear-gradient(115deg,transparent 28%,rgba(255,255,255,.26) 46%,transparent 64%);\n'
     '  transform:translateX(-130%);transition:transform .6s cubic-bezier(.22,.8,.26,1)}\n'
     'button.primary:hover::before{transform:translateX(130%)}'),
    # 3) 卡片按下反馈
    ('.pitem:hover{transform:translateX(2px)}',
     '.pitem:hover{transform:translateX(2px)}\n.pitem:active{transform:translateX(1px) scale(.996)}'),
]

ok = 0
for old, new in edits:
    if old not in s:
        print('未找到片段，跳过：', old[:52])
        continue
    s = s.replace(old, new, 1)
    ok += 1

io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('已应用 %d/%d 处微调' % (ok, len(edits)))
