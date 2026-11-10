# -*- coding: utf-8 -*-
"""抽出刚写入的动效脚本做语法检查，并确认 HTML 里没有破坏既有结构。"""
import io
import re
import sys

P = r'C:\Users\32354\Documents\deepseek-harness\default-workspace\法律论证标注系统\过程文件\输出\legal-annotation-prototype.html'
OUT = r'C:\Users\32354\Documents\deepseek-harness\default-workspace\法律论证标注系统\过程文件\输出\ux-motion.extracted.js'

s = io.open(P, encoding='utf-8').read()
m = re.search(r'<script id="ux-motion-js">(.*?)</script>', s, re.S)
if not m:
    print('未找到动效脚本')
    sys.exit(1)
js = m.group(1)
io.open(OUT, 'w', encoding='utf-8', newline='').write(js)

print('提取 JS %d 字符' % len(js))
print('style 块数量:', s.count('<style'))
print('script 块数量:', s.count('<script'))
print('</body> 数量:', s.count('</body>'))
print('动效样式 id 出现:', s.count('id="ux-motion-v1"'))
print('动效脚本 id 出现:', s.count('id="ux-motion-js"'))
print('模板字符串(${)残留:', js.count('${'))
