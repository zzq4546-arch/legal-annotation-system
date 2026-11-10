# -*- coding: utf-8 -*-
"""裁出差异区域放大对比，确认改动是『激活指示条』这类预期效果，而非布局位移。"""
import os
from PIL import Image, ImageDraw

BASE = r'C:\Users\32354\Documents\deepseek-harness\default-workspace\法律论证标注系统\过程文件\输出\ux-check'
OUT = os.path.join(BASE, 'crop')
os.makedirs(OUT, exist_ok=True)

REGION = (0, 160, 90, 235)   # 左栏激活位置附近
SCALE = 4

for name in ('overview', 'work'):
    a = Image.open(os.path.join(BASE, 'A-%s.png' % name)).convert('RGB')
    b = Image.open(os.path.join(BASE, 'B-%s.png' % name)).convert('RGB')
    ra, rb = a.crop(REGION), b.crop(REGION)
    w, h = ra.size
    canvas = Image.new('RGB', (w * SCALE * 2 + 20, h * SCALE + 30), 'white')
    canvas.paste(ra.resize((w * SCALE, h * SCALE), Image.NEAREST), (0, 30))
    canvas.paste(rb.resize((w * SCALE, h * SCALE), Image.NEAREST), (w * SCALE + 20, 30))
    d = ImageDraw.Draw(canvas)
    d.text((4, 8), 'BEFORE (no motion)', fill='#333')
    d.text((w * SCALE + 24, 8), 'AFTER (with motion)', fill='#333')
    p = os.path.join(OUT, '%s-rail.png' % name)
    canvas.save(p)
    print('saved', p, canvas.size)
