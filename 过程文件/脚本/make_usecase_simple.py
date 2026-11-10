# -*- coding: utf-8 -*-
"""Compact landscape use-case diagram: block layout, generalized actors, minimal links."""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1180, 600
img = Image.new('RGB', (W, H), 'white')
d = ImageDraw.Draw(img)
FONT = r'C:\Windows\Fonts\msyh.ttc'
FONTB = r'C:\Windows\Fonts\msyhbd.ttc'


def f(s, b=False):
    return ImageFont.truetype(FONTB if b else FONT, s)


def ctext(box, lines, size=10.5, bold=True, fill='#111111', gap=2):
    x0, y0, x1, y1 = box
    fo = f(size, bold)
    hs = [d.textbbox((0, 0), ln, font=fo)[3] - d.textbbox((0, 0), ln, font=fo)[1] for ln in lines]
    total = sum(hs) + gap * (len(lines) - 1)
    y = (y0 + y1) / 2 - total / 2
    for ln, h in zip(lines, hs):
        bb = d.textbbox((0, 0), ln, font=fo)
        d.text(((x0 + x1) / 2 - (bb[2] - bb[0]) / 2 - bb[0], y - bb[1]), ln, font=fo, fill=fill)
        y += h + gap


def uc(box, lines, fill, size=10.5):
    d.rounded_rectangle(box, radius=8, fill=fill, outline='#2f4f6f', width=1)
    ctext(box, lines, size=size, bold=True)


def block(box, title, fill, outline, sub=None):
    d.rounded_rectangle(box, radius=10, fill=fill, outline=outline, width=2)
    d.text((box[0] + 8, box[1] + 5), title, font=f(12, True), fill=outline)
    if sub:
        d.text((box[0] + 14 + d.textbbox((0, 0), title, font=f(12, True))[2], box[1] + 7),
               sub, font=f(9.5), fill='#6b7580')


def actor(cx, cy, name, size=11):
    hh = 18
    d.ellipse([cx - 8, cy - hh, cx + 8, cy - hh + 16], outline='#111111', width=2)
    d.line([cx, cy - hh + 16, cx, cy + 12], fill='#111111', width=2)
    d.line([cx - 15, cy - hh + 28, cx + 15, cy - hh + 28], fill='#111111', width=2)
    d.line([cx, cy + 12, cx - 11, cy + 32], fill='#111111', width=2)
    d.line([cx, cy + 12, cx + 11, cy + 32], fill='#111111', width=2)
    bb = d.textbbox((0, 0), name, font=f(size, True))
    d.text((cx - (bb[2] - bb[0]) / 2, cy + 36), name, font=f(size, True), fill='#111111')


def gen(p1, p2):
    d.line([p1, p2], fill='#333333', width=2)
    ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    L, sp = 9, math.radians(24)
    a = (p2[0] + L * math.cos(ang + math.pi - sp), p2[1] + L * math.sin(ang + math.pi - sp))
    b = (p2[0] + L * math.cos(ang + math.pi + sp), p2[1] + L * math.sin(ang + math.pi + sp))
    d.polygon([p2, a, b], fill='#ffffff', outline='#333333')


GREEN, BLUE, PINK, CYAN = '#dcecd8', '#d8e6f4', '#f8dcdc', '#d9f0f2'

# boundary
BX0, BY0, BX1, BY1 = 216, 14, 1170, 568
d.rectangle((BX0, BY0, BX1, BY1), outline='#1f4e79', width=2)
d.text((BX0 + 8, BY0 + 10), '法律论证结构标注系统', font=f(13, True), fill='#1f4e79')
d.line([(BX0, BY0 + 30), (BX1, BY0 + 30)], fill='#1f4e79', width=1)

GX, GW = 232, 920
# ① 指南管理
b1 = (GX, 42, GX + GW, 108)
block(b1, '① 指南管理', '#f2f8f0', '#4b8b4b', '（标准的唯一来源）')
uc((GX + 16, 64, GX + 16 + 296, 98), ['从文件导入标注指南（解析标签与关系体系）'], GREEN)
uc((GX + 326, 64, GX + 326 + 296, 98), ['指南与标签版本管理（任务期冻结 / 可追溯）'], GREEN)
uc((GX + 636, 64, GX + 904, 98), ['查看指南与标签定义（术语即时查阅）'], GREEN)

# ② 任务管理
b2 = (GX, 116, GX + GW, 182)
block(b2, '② 任务管理', '#eef3fb', '#5a7fb5')
uc((GX + 16, 138, GX + 312, 172), ['创建标注任务（分配标注员与裁定者）'], BLUE)
uc((GX + 326, 138, GX + 622, 172), ['案例信息与标注范围（裁判理由提取核对）'], BLUE)
uc((GX + 636, 138, GX + 904, 172), ['任务分配与进度查看（一份文书多人独立标注）'], BLUE)

# ③ 标注核心
b3 = (GX, 190, GX + GW, 310)
block(b3, '③ 标注核心', '#fdf1f1', '#c06a6a', '（命题标注、关系标注即为原型页面）')
uc((GX + 16, 212, GX + 312, 246), ['颗粒度切割（对齐校验：差异 >10% 退回）'], PINK)
uc((GX + 326, 212, GX + 622, 246), ['命题标注（SF / GF / SM / GM 及子类型）'], PINK)
uc((GX + 636, 212, GX + 904, 246), ['关系标注（S / A / J / M / I，支持嵌套）'], PINK)
uc((GX + 16, 256, GX + 312, 290), ['论证图示生成与导出（多图 / PNG·SVG）'], PINK)
uc((GX + 326, 256, GX + 622, 290), ['标签一致性检查（一致率 / 高分歧标签）'], PINK)
uc((GX + 636, 256, GX + 904, 290), ['参考答案比对与差异分类（教学场景）'], PINK)

# ④ 裁定与输出
b4 = (GX, 318, GX + GW, 384)
block(b4, '④ 裁定与输出', '#eef8f9', '#3f8b93', '（流程终点）')
uc((GX + 16, 340, GX + 312, 374), ['裁定与冲突解决（多版本人工比对）'], CYAN)
uc((GX + 326, 340, GX + 622, 374), ['结果导出与再导入（JSON / Excel / 图示）'], CYAN)
uc((GX + 636, 340, GX + 904, 374), ['裁定结果留痕（理由 / 前后值可追溯）'], CYAN)

# ⑤ 质量与知识沉淀
b5 = (GX, 392, GX + GW, 458)
block(b5, '⑤ 质量与知识沉淀', '#eef3fb', '#5a7fb5')
uc((GX + 16, 414, GX + 312, 448), ['疑难问题台账（分歧登记与反馈）'], BLUE)
uc((GX + 326, 414, GX + 622, 448), ['标注员培训与试标（指南校准）'], BLUE)
uc((GX + 636, 414, GX + 904, 448), ['示例库与标准样例（教师发布的参考答案）'], BLUE)

# ⑥ 学习与掌握支持
b6 = (GX, 466, GX + GW, 556)
d.rounded_rectangle(b6, radius=10, fill='#eef7ee', outline='#2f7d32', width=2)
d.text((b6[0] + 8, b6[1] + 5), '⑥ 论证框架学习与掌握支持', font=f(12, True), fill='#2f7d32')
d.text((b6[0] + 198, b6[1] + 7), '★ 落实“学生更快、更好地掌握论证框架”的业务需求',
       font=f(9.5, True), fill='#2f7d32')
for i, t in enumerate(['论证骨架视图（问题-理由-结论）', '参考答案比对（差异自动分类）', '错题集与反馈（结构错误：组合/匹配）']):
    x = b6[0] + 16 + i * 302
    uc((x, 488, x + 286, 522), [t], '#ffffff', size=10)
d.text((b6[0] + 16, 532), '更快：骨架先给结构、比对即时反馈、差异自动分类、关系拖动即建；'
                          '更好：标准样例统一标准、错题集聚焦结构错误、裁定理由可见',
       font=f(9.5), fill='#3f6b3f')

# actors
AX = 100
A_student = (AX, 78)
A_annot = (AX, 176)
A_teacher = (AX, 274)
A_admin = (AX, 372)
A_adjud = (AX, 470)
actor(*A_student, '学生')
actor(*A_annot, '标注员')
actor(*A_teacher, '教师')
actor(*A_admin, '管理员')
actor(*A_adjud, '裁定者')

gen((AX, A_annot[1] - 16), (AX, A_student[1] + 36))
gen((AX, A_teacher[1] - 16), (AX, A_annot[1] + 36))
gen((AX, A_admin[1] - 16), (AX, A_teacher[1] + 36))
d.text((AX - 14, A_teacher[1] - 6), '«泛化»', font=f(8.5), fill='#666666')

# one association per actor (horizontal)
d.line([(AX + 18, A_student[1] + 22), (GX, 500)], fill='#2f7d32', width=2)
d.line([(AX + 18, A_annot[1] + 8), (GX, 228)], fill='#8a939c', width=1)
d.line([(AX + 18, A_teacher[1] - 4), (GX, 80)], fill='#8a939c', width=1)
d.line([(AX + 18, A_admin[1] + 8), (GX, 156)], fill='#8a939c', width=1)
d.line([(AX + 18, A_adjud[1] + 8), (GX, 356)], fill='#8a939c', width=1)
d.text((AX + 22, A_student[1] + 26), '学习路径', font=f(8.5), fill='#2f7d32')

# 领域专家 → 疑难问题台账（从右侧进入）
A_expert = (1096, 552)
actor(*A_expert, '领域专家')
d.line([(A_expert[0], A_expert[1] - 42), (1108, 430)], fill='#8a939c', width=1)
d.line([(1108, 430), (GX + GW, 430)], fill='#8a939c', width=1)

img.save(r'C:\Users\32354\Documents\deepseek-harness\default-workspace\法律论证标注系统\过程文件\输出\usecase_simple.png')
img.save(r'C:\Users\32354\Documents\deepseek-harness\default-workspace\法律论证标注系统\过程文件\输出\usecase.png')
print('saved', img.size)
