# -*- coding: utf-8 -*-
"""生成原型架构图（单文件前端原型 · 分层视图）v2"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, '..', '输出', 'arch'))
os.makedirs(OUT, exist_ok=True)
TOP = os.path.abspath(os.path.join(HERE, '..', '..', '原型架构图.png'))

FONT_R = r'C:\Windows\Fonts\msyh.ttc'
FONT_B = r'C:\Windows\Fonts\msyhbd.ttc'

INK = (34, 48, 40)
MUTED = (108, 120, 110)
LINE = (206, 214, 202)
GREEN_D = (36, 75, 60)
GREEN_M = (74, 107, 85)
GREEN_L = (232, 240, 232)
CREAM = (250, 251, 245)
BROWN = (140, 100, 61)
BROWN_L = (247, 241, 231)
BLUE = (45, 84, 106)
BLUE_L = (233, 240, 244)
PLUM = (110, 58, 79)
PLUM_L = (247, 238, 242)


def F(size, bold=False):
    return ImageFont.truetype(FONT_B if bold else FONT_R, size)


def text_w(d, s, f):
    b = d.textbbox((0, 0), s, font=f)
    return b[2] - b[0]


def fit(d, s, maxw, size, bold=False, minsize=11):
    while size > minsize:
        f = F(size, bold)
        if text_w(d, s, f) <= maxw:
            return f
        size -= 1
    return F(minsize, bold)


def card(d, box, title, sub=None, fill=CREAM, outline=LINE, ink=INK,
         tsize=25, ssize=17, pad=14, accent=None):
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, radius=10, fill=fill, outline=outline, width=2)
    cx = (x0 + x1) / 2
    avail = x1 - x0 - 2 * pad
    if sub:
        ft = fit(d, title, avail, tsize, True)
        fs = fit(d, sub, avail, ssize, False)
        th = d.textbbox((0, 0), title, font=ft)[3] - d.textbbox((0, 0), title, font=ft)[1]
        sh = d.textbbox((0, 0), sub, font=fs)[3] - d.textbbox((0, 0), sub, font=fs)[1]
        total = th + 10 + sh
        ty = (y0 + y1) / 2 - total / 2
        d.text((cx, ty), title, font=ft, fill=ink, anchor='ma')
        d.text((cx, ty + th + 10), sub, font=fs, fill=MUTED, anchor='ma')
    else:
        ft = fit(d, title, avail, tsize, True)
        d.text((cx, (y0 + y1) / 2), title, font=ft, fill=ink, anchor='mm')


def band(d, y0, y1, label, color=GREEN_M, x0=52, x1=1580):
    d.rounded_rectangle((x0, y0, x1, y1), radius=14, fill='white', outline=LINE, width=2)
    d.rectangle((x0, y0 + 14, x0 + 6, y1 - 14), fill=color)
    d.text((x0 + 20, y0 - 30), label, font=F(18, True), fill=color)


def arrow(d, p0, p1, color=GREEN_M, w=3):
    d.line([p0, p1], fill=color, width=w)
    x0, y0 = p0
    x1, y1 = p1
    if abs(y1 - y0) >= abs(x1 - x0):
        s = 1 if y1 > y0 else -1
        d.polygon([(x1, y1), (x1 - 8, y1 - 13 * s), (x1 + 8, y1 - 13 * s)], fill=color)
    else:
        s = 1 if x1 > x0 else -1
        d.polygon([(x1, y1), (x1 - 13 * s, y1 - 8), (x1 - 13 * s, y1 + 8)], fill=color)


W, H = 2100, 1500
img = Image.new('RGB', (W, H), 'white')
d = ImageDraw.Draw(img)

d.text((70, 44), '原型架构（单文件 · 零依赖 · 纯前端）', font=F(40, True), fill=GREEN_D)
d.text((72, 104), '法律论证标注系统 · 交互版 v3.0　—　一个 HTML 文件，双击即用；无构建、无服务端，数据只留在本机浏览器',
       font=F(19), fill=MUTED)

# ① 入口层
band(d, 200, 344, '① 入口层', GREEN_D)
card(d, (90, 224, 700, 320), '登录界面 #loginLayer', '账号 + 密码；错误原地提示；演示账号一键填入', fill=GREEN_L, accent=GREEN_D)
card(d, (724, 224, 1540, 320), '账号与会话', '初始账号组 teacher / stu01 / stu02 / judge（密码 123456）· 教师可新建账号', fill=CREAM)

# ② 外壳
band(d, 384, 574, '② 应用外壳（shell）', GREEN_M)
card(d, (90, 408, 610, 550), '顶栏', '面包屑 · 保存状态 · 当前账号 · 退出', fill=CREAM)
card(d, (634, 408, 960, 550), '侧栏 NAV', '按角色过滤：\n教师 10 / 学生 5 / 裁定者 5', fill=CREAM)
card(d, (984, 408, 1540, 550), '内容区 #view', '整块重绘；工作台另绑定 canvas 与拖拽', fill=CREAM)

# ③ 视图层
band(d, 614, 844, '③ 视图层（VIEWS：每个模块一个 view 函数）', BLUE)
views = [
    ('项目概览', 'overview', 0), ('指南管理', 'guide', 0), ('任务管理', 'task', 0),
    ('标注工作台', 'work', 0), ('冲突裁定', 'adj', 0),
    ('质量看板', 'quality', 0), ('教学比对', 'teach', 0), ('导出与归档', 'exp', 0),
    ('台账与记录', 'ledger', 0), ('账号管理', 'accounts', 1),
]
bw, step = 278, 290
for i, (t, k, is_new) in enumerate(views):
    row = i // 5
    col = i % 5
    bx = 90 + col * step
    by = 644 + row * 92
    box = (bx, by, bx + bw, by + 76)
    fill = BROWN_L if is_new else GREEN_L
    out = (216, 192, 162) if is_new else (198, 214, 202)
    d.rounded_rectangle(box, radius=8, fill=fill, outline=out, width=2)
    d.text((bx + bw / 2, by + 26), t, font=fit(d, t, bw - 20, 21, True), fill=INK, anchor='mm')
    d.text((bx + bw / 2, by + 55), k, font=F(15), fill=MUTED, anchor='mm')

# ④ 运行时
band(d, 884, 1094, '④ 运行时（状态 · 路由 · 权限 · 事件）', BROWN)
card(d, (90, 908, 556, 1070), 'state', '模块、角色、文档、两版标注、选区、缩放', fill=BROWN_L, ssize=16)
card(d, (580, 908, 960, 1070), '路由与渲染', 'setMod → hash → render() 整块重绘', fill=BROWN_L, ssize=16)
card(d, (984, 908, 1266, 1070), '权限', 'ROLE_NAV / canSee\nGATED / writable()', fill=BROWN_L, ssize=16)
card(d, (1290, 908, 1540, 1070), '事件绑定', '委托 + 逐元素\npointer 拖拽', fill=BROWN_L, ssize=16)

# ⑤ 持久层
band(d, 1134, 1224, '⑤ 持久层（localStorage，仅本机）', GREEN_D)
keys = [('legal-annotation-warm-v3', '标注数据 + 版本'),
        ('legal-annotation-accounts-v1', '账号表'),
        ('legal-annotation-session-v1', '登录会话')]
for i, (k, s) in enumerate(keys):
    kx = 90 + i * 484
    box = (kx, 1152, kx + 462, 1204)
    d.rounded_rectangle(box, radius=8, fill=CREAM, outline=LINE, width=2)
    d.text((kx + 14, 1158), k, font=F(15, True), fill=INK, anchor='la')
    d.text((kx + 14, 1179), s, font=F(14), fill=MUTED, anchor='la')

# ⑥ 产出
band(d, 1264, 1364, '⑥ 产出（浏览器下载，无后端）', BLUE)
card(d, (90, 1284, 556, 1344), 'JSON 标注版本导出', '', fill=BLUE_L, tsize=23)
card(d, (580, 1284, 1046, 1344), 'CSV / 台账记录', '', fill=BLUE_L, tsize=23)
card(d, (1070, 1284, 1540, 1344), 'SVG / PNG 论证图示', '', fill=BLUE_L, tsize=23)

# 纵向箭头
for y0, y1 in [(344, 384), (574, 614), (844, 884), (1094, 1134), (1224, 1264)]:
    arrow(d, (816, y0 + 2), (816, y1 - 2))

# 右侧跨切面
px0, px1 = 1608, 2036
d.rounded_rectangle((px0, 190, px1, 1148), radius=16, fill=PLUM_L, outline=(212, 182, 196), width=2)
d.text((px0 + 24, 212), '跨切面能力', font=F(24, True), fill=PLUM)
d.text((px0 + 24, 248), '贯穿各层，只追加样式与脚本，不改结构', font=F(15), fill=(120, 92, 106))
cap = [
    ('交互动效 ux-motion', '按钮悬停 / 按下 / 涟漪、侧栏激活条、\n页面淡入错峰、toast 胶囊'),
    ('滚动与渲染性能', 'contain:paint 隔离重绘、\n去整页 transform、去强制回流'),
    ('登录与账号 auth', '登录锁屏、初始化账号组、\n教师建号、会话与退出'),
]
yy = 296
for t, s in cap:
    d.rounded_rectangle((px0 + 18, yy, px1 - 18, yy + 244), radius=10,
                        fill='white', outline=(212, 182, 196), width=2)
    d.text(((px0 + px1) / 2, yy + 30), t, font=fit(d, t, px1 - px0 - 60, 21, True), fill=PLUM, anchor='ma')
    for k, ln in enumerate(s.split('\n')):
        d.text(((px0 + px1) / 2, yy + 78 + k * 32), ln,
               font=fit(d, ln, px1 - px0 - 56, 16), fill=(96, 76, 86), anchor='ma')
    yy += 276

d.text((72, 146), '注：右侧三项能力作用于 ②③④，均以追加 <style> / <script> 块的方式实现，不改变视图函数与 DOM 结构。',
       font=F(16), fill=(160, 150, 140))

# 页脚
d.line([(70, 1404), (2036, 1404)], fill=LINE, width=1)
d.text((70, 1420), '读图：箭头为自上而下的调用方向；⑤ 中的键名即 DevTools → Application → Local Storage 里的条目。',
       font=F(17), fill=MUTED)
d.text((70, 1452), '重置：清空这三个键，或点侧栏「恢复演示数据」，即回到初始演示状态。',
       font=F(17), fill=MUTED)

img.save(TOP)
img.save(os.path.join(OUT, 'arch-prototype.png'))
print('saved', TOP, img.size)
