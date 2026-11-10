# -*- coding: utf-8 -*-
"""Draw the system use-case diagram for the legal-argument annotation system (v2)."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1700, 1210
img = Image.new('RGB', (W, H), 'white')
d = ImageDraw.Draw(img)

FONT = r'C:\Windows\Fonts\msyh.ttc'
FONTB = r'C:\Windows\Fonts\msyhbd.ttc'
if not os.path.exists(FONTB):
    FONTB = FONT


def f(size, bold=False):
    return ImageFont.truetype(FONTB if bold else FONT, size)


def center_text(box, lines, size=19, bold=False, fill='#111111'):
    x0, y0, x1, y1 = box
    font = f(size, bold)
    hs = [d.textbbox((0, 0), ln, font=font)[3] - d.textbbox((0, 0), ln, font=font)[1] for ln in lines]
    total = sum(hs) + 6 * (len(lines) - 1)
    y = (y0 + y1) / 2 - total / 2
    for ln, h in zip(lines, hs):
        bb = d.textbbox((0, 0), ln, font=font)
        d.text(((x0 + x1) / 2 - (bb[2] - bb[0]) / 2 - bb[0], y - bb[1]), ln, font=font, fill=fill)
        y += h + 6


def arrow(p1, p2, color='#8a6d00', width=2, dashed=False):
    if dashed:
        import math
        x1, y1 = p1
        x2, y2 = p2
        dist = math.hypot(x2 - x1, y2 - y1)
        n = max(int(dist // 10), 1)
        for i in range(n):
            if i % 2 == 0:
                t0, t1 = i / n, (i + 0.55) / n
                d.line([(x1 + (x2 - x1) * t0, y1 + (y2 - y1) * t0),
                        (x1 + (x2 - x1) * t1, y1 + (y2 - y1) * t1)], fill=color, width=width)
    else:
        d.line([p1, p2], fill=color, width=width)
    # barbed head
    import math
    ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    L = 12
    for da in (math.radians(155), math.radians(-155)):
        d.line([p2, (p2[0] + L * math.cos(ang + da), p2[1] + L * math.sin(ang + da))],
               fill=color, width=width)


def cylinder(cx, cy, w, h, label, size=15, bold=True):
    rx, ry = w / 2, 9
    d.ellipse([cx - rx, cy - h / 2, cx + rx, cy - h / 2 + 2 * ry], outline='#333333', width=2)
    d.line([cx - rx, cy - h / 2 + ry, cx - rx, cy + h / 2 - ry], fill='#333333', width=2)
    d.line([cx + rx, cy - h / 2 + ry, cx + rx, cy + h / 2 - ry], fill='#333333', width=2)
    d.arc([cx - rx, cy + h / 2 - 2 * ry, cx + rx, cy + h / 2], 0, 180, fill='#333333', width=2)
    center_text((cx - rx, cy - h / 2 + 2 * ry, cx + rx, cy + h / 2 - ry), label.split('\n'),
                size=size, bold=bold)


def usecase(box, lines, fill, size=19, bold=True, outline='#2f4f6f'):
    d.rounded_rectangle(box, radius=14, fill=fill, outline=outline, width=2)
    center_text(box, lines, size=size, bold=bold)


def actor(cx, cy, name, size=19):
    hh = 30
    d.ellipse([cx - 13, cy - hh, cx + 13, cy - hh + 26], outline='#111111', width=3)
    d.line([cx, cy - hh + 26, cx, cy + 22], fill='#111111', width=3)
    d.line([cx - 24, cy - hh + 44, cx + 24, cy - hh + 44], fill='#111111', width=3)
    d.line([cx, cy + 22, cx - 18, cy + 56], fill='#111111', width=3)
    d.line([cx, cy + 22, cx + 18, cy + 56], fill='#111111', width=3)
    lines = name.split('\n')
    font = f(size, True)
    y = cy + 62
    for ln in lines:
        bb = d.textbbox((0, 0), ln, font=font)
        d.text((cx - (bb[2] - bb[0]) / 2, y), ln, font=font, fill='#111111')
        y += 24


def line(p1, p2, width=2, color='#7a7a7a'):
    d.line([p1, p2], fill=color, width=width)


# ---------- system boundary ----------
BX0, BY0, BX1, BY1 = 330, 80, 1080, 1040
d.rectangle((BX0, BY0, BX1, BY1), outline='#1f4e79', width=3)
d.text((348, 94), '法律论证结构标注系统', font=f(22, True), fill='#1f4e79')
d.line([(BX0, 130), (BX1, 130)], fill='#1f4e79', width=2)

GREEN = '#dcecd8'
PINK = '#f8dcdc'
BLUE = '#d8e6f4'

# ---------- actors ----------
student = (160, 330)
annot = (160, 620)
teacher = (160, 900)
actor(*student, '学生')
actor(*annot, '标注员')
actor(*teacher, '教师')

adjud = (1560, 170)
creator = (1560, 450)
admin = (1560, 730)
expert = (1560, 960)
actor(*adjud, '裁定者')
actor(*creator, '任务创建者\n（教师/管理员）')
actor(*admin, '管理员')
actor(*expert, '领域专家')

# ---------- use cases ----------
C = [440, 602, 765, 928]
UW, UH = 170, 66
U1Y, U2Y = 158, 244
uc1 = (C[0] - UW / 2, U1Y, C[0] + UW / 2, U1Y + UH)          # 从文件导入标注指南
uc2 = (C[1] - UW / 2, U1Y, C[1] + UW / 2, U1Y + UH)          # 创建标注任务
uc3 = (C[2] - UW / 2, U1Y, C[2] + UW / 2, U1Y + UH)          # 查看指南与标签定义
uc4 = (C[3] - UW / 2, U1Y, C[3] + UW / 2, U1Y + UH)          # 颗粒度切割
uc5 = (C[0] - UW / 2, U2Y, C[0] + UW / 2, U2Y + UH)          # 命题标注
uc6 = (C[1] - UW / 2, U2Y, C[1] + UW / 2, U2Y + UH)          # 关系标注与裁定
uc7 = (C[2] - UW / 2, U2Y, C[2] + UW / 2, U2Y + UH)          # 论证图示生成与导出
uc8 = (C[3] - UW / 2, U2Y, C[3] + UW / 2, U2Y + UH)          # 裁定与冲突解决

usecase(uc1, ['从文件导入', '标注指南'], GREEN)
usecase(uc2, ['创建标注任务', '（指南/标签版本冻结）'], GREEN, size=15)
usecase(uc3, ['查看指南', '与标签定义'], GREEN, size=16)
usecase(uc4, ['颗粒度切割', '（对齐校验）'], GREEN)
usecase(uc5, ['命题标注'], PINK, size=20)
usecase(uc6, ['关系标注与裁定'], PINK, size=19)
usecase(uc7, ['论证图示', '生成与导出'], PINK)
usecase(uc8, ['裁定与冲突解决', '（含人工比对）'], PINK, size=15)

# ---------- learning block ----------
MID = (352, 388, 1058, 596)
d.rounded_rectangle(MID, radius=16, fill='#eef4fb', outline='#1f4e79', width=2)
d.text((368, 398), '论证框架学习与掌握支持 ★', font=f(20, True), fill='#1f4e79')
MW, MH = 206, 62
MX = [478, 704, 930]
mid = [(MX[i] - MW / 2, 466, MX[i] + MW / 2, 466 + MH) for i in range(3)]
usecase(mid[0], ['论证骨架视图', '（问题-理由-结论）'], '#ffffff', size=15)
usecase(mid[1], ['参考答案比对', '与差异分类'], '#ffffff', size=16)
usecase(mid[2], ['错题集与反馈', '（结构错误）'], '#ffffff', size=16)

# ---------- support row ----------
SY, SW, SH = 650, 160, 60
SX = [440, 602, 765, 928]
sup = [
    (SX[0] - SW / 2, SY, SX[0] + SW / 2, SY + SH),   # 标签一致性检查
    (SX[1] - SW / 2, SY, SX[1] + SW / 2, SY + SH),   # 疑难问题台账
    (SX[2] - SW / 2, SY, SX[2] + SW / 2, SY + SH),   # 裁定结果留痕
    (SX[3] - SW / 2, SY, SX[3] + SW / 2, SY + SH),   # 结果导出与再导入
]
usecase(sup[0], ['标签一致性', '检查'], BLUE, size=16)
usecase(sup[1], ['疑难问题台账', '（分歧记录）'], BLUE, size=15)
usecase(sup[2], ['裁定结果留痕', '（可追溯）'], BLUE, size=15)
usecase(sup[3], ['结果导出', '与再导入'], BLUE, size=16)

# ---------- data stores ----------
DSY = 860
DSX = [470, 704, 938]
DW, DH = 196, 68
cylinder(DSX[0], DSY, DW, DH, '指南版本库\n（v1.2 及快照）')
cylinder(DSX[1], DSY, DW, DH, '标签体系库\n（冻结版本）')
cylinder(DSX[2], DSY, DW, DH, '标注与裁定\n版本库')

# ---------- student associations ----------
RX = 344                      # right edge of the actor column
line((186, 316), (RX, 452), 3, '#2f7d32')      # 学生 -> 学习支持块
line((186, 300), (352, 500), 2, '#2f7d32')     # 学生 -> 参考答案比对
line((186, 336), (352, 540), 2, '#2f7d32')     # 学生 -> 错题集与反馈
line((186, 284), (uc5[0], uc5[1] + 20))        # 学生 -> 命题标注
line((186, 352), (uc6[0], uc6[1] + 56))        # 学生 -> 关系标注与裁定
line((186, 366), (uc3[0], uc3[3]))             # 学生 -> 查看指南

# ---------- annotator associations ----------
line((186, 604), (344, 686))                   # 标注员 -> 标签一致性检查
line((186, 586), (uc4[0], uc4[3]))             # 标注员 -> 颗粒度切割
line((186, 622), (sup[1][0], sup[1][1] + 20))  # 标注员 -> 疑难问题台账
line((186, 640), (sup[3][0], sup[3][1]))       # 标注员 -> 结果导出与再导入

# ---------- teacher associations ----------
line((186, 880), (uc1[0], uc1[3]))             # 教师 -> 从文件导入标注指南
line((186, 898), (uc2[0], uc2[3]))             # 教师 -> 创建标注任务
line((186, 916), (uc3[0], uc3[3] - 10))        # 教师 -> 查看指南与标签定义
line((186, 934), (uc4[0], uc4[3]))             # 教师 -> 颗粒度切割
line((186, 952), (sup[2][0], sup[2][3]))       # 教师 -> 裁定结果留痕

# ---------- right actors ----------
line((uc2[2] - 6, uc2[1] + 26), (1536, 172))                       # 创建任务 -> 裁定者
line((uc8[2], uc8[1] + 20), (1536, 188))                           # 裁定 -> 裁定者
line((uc1[2], uc1[1] + 34), (1536, 448))                           # 导入指南 -> 创建者
line((uc2[2], uc2[1] + 48), (1536, 432))                           # 创建任务 -> 创建者
line((uc6[2], uc6[1] + 12), (1536, 466))                           # 关系标注与裁定 -> 创建者
line((uc7[2], uc7[3]), (1536, 480))                                # 图示导出 -> 创建者
line((uc1[2], uc1[3] - 6), (1536, 716))                            # 导入指南 -> 管理员
line((uc2[2], uc2[3] - 6), (1536, 730))                            # 创建任务 -> 管理员
line((uc4[2], uc4[3]), (1536, 744))                                # 颗粒度切割 -> 管理员
line((sup[0][2], sup[0][3]), (1536, 758))                          # 标签一致性 -> 管理员
line((sup[3][2], sup[3][3]), (1536, 772))                          # 导出 -> 管理员
line((uc8[2], uc8[3]), (1536, 946))                                # 裁定 -> 领域专家

# ---------- include / extend ----------
arrow((uc3[0] - 30, uc3[1]), (uc3[0] - 30, uc1[3] + 4), width=2)
d.text((uc3[0] + 12, 226), '«include»', font=f(14), fill='#8a6d00')
arrow((uc6[0] - 46, uc6[1]), (uc6[0] - 46, uc2[3] + 4), width=2)
d.text((uc6[0] - 144, 226), '«include»', font=f(14), fill='#8a6d00')
arrow((sup[1][0] + 12, sup[1][1]), (uc6[0] + 40, uc6[3] + 4), width=2, dashed=True)
d.text((sup[1][0] - 116, 612), '«extend»', font=f(14), fill='#8a6d00')

# ---------- data store links ----------
line((uc1[0] + 30, uc1[3]), (DSX[0], DSY - DH / 2), 2, '#2f4f6f')
line((uc3[0] - 20, uc3[3]), (DSX[0] + 40, DSY - DH / 2), 2, '#2f4f6f')
line((uc2[0], uc2[3]), (DSX[1], DSY - DH / 2), 2, '#2f4f6f')
line((uc5[0] + 40, uc5[3]), (DSX[2] - 60, DSY - DH / 2), 2, '#2f4f6f')
line((uc6[0], uc6[3]), (DSX[2] - 10, DSY - DH / 2), 2, '#2f4f6f')
line((uc8[0] + 30, uc8[3]), (DSX[2] + 60, DSY - DH / 2), 2, '#2f4f6f')
line((sup[3][0] + 10, sup[3][3]), (DSX[2] + 90, DSY - DH / 2), 2, '#2f4f6f')

# ---------- teaching-value panels ----------
d.rounded_rectangle((1115, 120, 1470, 320), radius=14, fill='#e8f3e8', outline='#2f7d32', width=2)
d.text((1130, 130), '更快（学习效率）', font=f(18, True), fill='#2f7d32')
for i, t in enumerate(['骨架视图先给结构，降低认知负荷',
                       '参考答案即时比对，缩短反馈周期',
                       '差异自动分类，减少无效返工',
                       '表单化标注，命题一次成型',
                       '关系在图上拖动即建，无需记符号']):
    d.text((1130, 162 + i * 31), '· ' + t, font=f(13), fill='#1f3d20')

d.rounded_rectangle((1115, 336, 1470, 560), radius=14, fill='#e8f0fb', outline='#1f4e79', width=2)
d.text((1130, 346), '更好（掌握程度）', font=f(18, True), fill='#1f4e79')
for i, t in enumerate(['对照标准样例，统一判断标准',
                       '错题集聚焦结构错误：组合/匹配',
                       '嵌套关系逐层构造，理解"缺一不可"',
                       '术语即时查阅标签定义',
                       '教师裁定理由可见，知其所以然',
                       '骨架视图把理由与结论显性化']):
    d.text((1130, 378 + i * 30), '· ' + t, font=f(13), fill='#12304d')

d.rounded_rectangle((1115, 576, 1470, 700), radius=14, fill='#fdf6e3', outline='#8a6d00', width=2)
d.text((1130, 586), '一致性控制（质量保障）', font=f(18, True), fill='#8a6d00')
for i, t in enumerate(['颗粒度差异 >10% 退回重切', '标签/关系一致率留痕可追溯',
                       '裁定理由入疑难问题台账']):
    d.text((1130, 618 + i * 28), '· ' + t, font=f(13), fill='#5c4a00')

# ---------- legend (below the boundary) ----------
d.rounded_rectangle((60, 1064, 1080, 1196), radius=12, fill='#fafafa', outline='#999999', width=1)
d.text((80, 1076), '图例：', font=f(16, True), fill='#333333')
d.rounded_rectangle((140, 1078, 190, 1110), radius=8, fill=GREEN, outline='#2f4f6f', width=1)
d.text((198, 1080), '任务准备与指南管理', font=f(15), fill='#333333')
d.rounded_rectangle((380, 1078, 430, 1110), radius=8, fill=PINK, outline='#2f4f6f', width=1)
d.text((438, 1080), '核心标注与裁定', font=f(15), fill='#333333')
d.rounded_rectangle((600, 1078, 650, 1110), radius=8, fill=BLUE, outline='#2f4f6f', width=1)
d.text((658, 1080), '质量与输出', font=f(15), fill='#333333')
d.rounded_rectangle((790, 1078, 840, 1110), radius=8, fill='#eef4fb', outline='#1f4e79', width=1)
d.text((848, 1080), '学习与掌握支持', font=f(15), fill='#333333')
d.text((140, 1122), '实线＝关联（参与者与用例）　　虚线箭头＝«include» / «extend»　　圆柱＝数据存储',
       font=f(14), fill='#555555')
d.text((140, 1152), '绿色粗线＝学生学习路径（学生 → 论证框架学习与掌握支持）',
       font=f(14), fill='#2f7d32')

img.save(r'C:\Users\32354\Documents\deepseek-harness\default-workspace\法律论证标注系统\过程文件\输出\usecase.png')
print('saved', img.size)
