# -*- coding: utf-8 -*-
"""绘制法律论证模型教学辅助模块的 ERD 系列图。

输出：
  erd-domains.png  四个数据域及其跨域联系（总览）
  erd-chen.png     Chen 记法核心联系图（演示构建流程与基数）
  erd-a.png        域 A：用户与教学组织
  erd-b.png        域 B：学习内容
  erd-c.png        域 C：练习与标注
  erd-d.png        域 D：学情与反馈
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = r'C:\Users\32354\Documents\deepseek-harness\default-workspace\法律论证标注系统\过程文件\输出\erd'
os.makedirs(OUT, exist_ok=True)

REG = r'C:\Windows\Fonts\msyh.ttc'
BOLD = r'C:\Windows\Fonts\msyhbd.ttc'


def F(size, bold=False):
    return ImageFont.truetype(BOLD if bold else REG, size)


INK = '#1f2d24'
MUTED = '#6b7669'
LINE = '#8d9a89'
HEAD = '#2e5041'
HEAD2 = '#3f6a52'
FILL = '#ffffff'
FILL_HEAD = '#e7efe2'
FILL_BRIDGE = '#f4f0e4'
FILL_CTX = '#f7f7f2'
EDGE = '#5f7362'
ACCENT = '#b07a1e'


def tw(d, s, f):
    b = d.textbbox((0, 0), s, font=f)
    return b[2] - b[0], b[3] - b[1]


def center_text(d, cx, cy, s, f, fill=INK):
    w, h = tw(d, s, f)
    d.text((cx - w / 2, cy - h / 2 - 2), s, font=f, fill=fill)


def entity(d, x, y, w, h, title, attrs=None, bridge=False, ctx=False):
    """Crow's Foot 实体框：标题条 + 属性行。"""
    fill = FILL_BRIDGE if bridge else (FILL_CTX if ctx else FILL)
    edge = EDGE if not ctx else '#b9c2b3'
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=fill, outline=edge, width=2)
    head_h = 54
    d.rounded_rectangle([x, y, x + w, y + head_h], radius=10, fill=FILL_HEAD, outline=edge, width=2)
    d.rectangle([x, y + head_h - 12, x + w, y + head_h], fill=FILL_HEAD)
    d.line([x, y + head_h, x + w, y + head_h], fill=edge, width=2)
    center_text(d, x + w / 2, y + head_h / 2, title, F(26, True), HEAD)
    if attrs:
        ay = y + head_h + 12
        for i, (tag, name, typ) in enumerate(attrs):
            font = F(21)
            if tag:
                tagw = 34
                tagfill = '#cfe0c6' if tag == 'PK' else ('#e8dcc0' if tag == 'FK' else '#e3e3e3')
                d.rounded_rectangle([x + 12, ay + 4, x + 12 + tagw * 1.4, ay + 30], radius=5,
                                    fill=tagfill, outline='#c3ceb9')
                center_text(d, x + 12 + tagw * 0.7, ay + 17, tag, F(15, True), '#3c4a37')
                nx = x + 12 + tagw * 1.4 + 10
            else:
                nx = x + 16
            d.text((nx, ay + 4), name, font=font, fill=INK)
            if typ:
                d.text((x + w - 16 - tw(d, typ, F(18))[0], ay + 6), typ, font=F(18), fill=MUTED)
            ay += 42
            if i < len(attrs) - 1:
                d.line([x + 12, ay - 6, x + w - 12, ay - 6], fill='#eef1ea', width=1)


def diamond(d, cx, cy, w, h, text, font=None):
    d.polygon([(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)],
              fill='#fbf6ea', outline=ACCENT, width=2)
    center_text(d, cx, cy, text, font or F(20, True), '#7a5512')


def rect_entity(d, cx, cy, w, h, text, font=None):
    d.rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2],
                fill=FILL_HEAD, outline=HEAD2, width=2)
    center_text(d, cx, cy, text, font or F(21, True), HEAD)


def ell(cx, cy, rx, ry):
    return [(cx, cy - ry), (cx + rx, cy), (cx, cy + ry), (cx - rx, cy)]


def line(d, p1, p2, width=2, fill=LINE, dash=None):
    if dash:
        # 简易虚线
        import math
        x1, y1 = p1; x2, y2 = p2
        dist = math.hypot(x2 - x1, y2 - y1)
        if dist == 0:
            return
        n = int(dist // (dash * 2))
        for i in range(n + 1):
            a = i * dash * 2 / dist
            b = min(1, (i * dash * 2 + dash) / dist)
            d.line([(x1 + (x2 - x1) * a, y1 + (y2 - y1) * a),
                    (x1 + (x2 - x1) * b, y1 + (y2 - y1) * b)], fill=fill, width=width)
    else:
        d.line([p1, p2], fill=fill, width=width)


def card(d, pt, text, dx=0, dy=0, fill=ACCENT):
    f = F(20, True)
    d.text((pt[0] + dx, pt[1] + dy), text, font=f, fill=fill)


def edge_label(d, p1, p2, text, t=0.5, dx=0, dy=-14):
    mx = p1[0] + (p2[0] - p1[0]) * t + dx
    my = p1[1] + (p2[1] - p1[1]) * t + dy
    f = F(18)
    w, h = tw(d, text, f)
    d.rounded_rectangle([mx - w / 2 - 6, my - h / 2 - 3, mx + w / 2 + 6, my + h / 2 + 3],
                        radius=6, fill='white', outline='#dbe2d5')
    center_text(d, mx, my, text, f, '#5b6b58')


def crow_foot(d, pt, direction, many=True, zero=False):
    """在 pt 处画鸦爪（many）或竖线（one）。direction: 'l'/'r'/'u'/'d' 表示线从该方向进入实体。"""
    x, y = pt
    L = 18
    if direction in ('l', 'r'):
        sx = x + (L if direction == 'r' else -L)
        if many:
            for dy in (-9, 0, 9):
                d.line([(sx, y + dy), (x, y)], fill=EDGE, width=2)
        else:
            d.line([(sx, y - 9), (sx, y + 9)], fill=EDGE, width=2)
        if zero:
            d.ellipse([sx - 12, y - 6, sx - 2, y + 6], outline=EDGE, width=2)
    else:
        sy = y + (L if direction == 'd' else -L)
        if many:
            for dx in (-9, 0, 9):
                d.line([(x + dx, sy), (x, y)], fill=EDGE, width=2)
        else:
            d.line([(x - 9, sy), (x + 9, sy)], fill=EDGE, width=2)


def title_block(d, w, title, subtitle=None):
    d.text((70, 46), title, font=F(40, True), fill=HEAD)
    if subtitle:
        d.text((70, 100), subtitle, font=F(22), fill=MUTED)
    d.line([(70, 138), (w - 70, 138)], fill='#d8e0d2', width=2)


# =====================================================================
# 图 1：四个数据域与跨域联系
# =====================================================================
def draw_domains():
    W, H = 2120, 1470
    img = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(img)
    title_block(d, W, '图 1  法律论证模型教学辅助模块 · 数据域总览',
                '四个数据域及其主要跨域联系（各域内部实体的完整属性见图 3–图 6）')

    A, B, C, D = '#3f6a52', '#7a5c34', '#2f5d7a', '#7a3f52'

    def domain(x, y, w, h, name, en, items, color):
        d.rounded_rectangle([x, y, x + w, y + h], radius=16, fill='#fcfcf8', outline=color, width=3)
        d.rounded_rectangle([x, y, x + w, y + 62], radius=16, fill=color, outline=color, width=3)
        d.rectangle([x, y + 40, x + w, y + 62], fill=color)
        center_text(d, x + w / 2, y + 22, name, F(27, True), 'white')
        ty = y + 80
        for it in items:
            d.ellipse([x + 20, ty + 9, x + 30, ty + 19], fill=color)
            d.text((x + 42, ty), it, font=F(22), fill=INK)
            ty += 42
        d.text((x + 20, y + h - 34), en, font=F(16), fill=MUTED)

    domain(70, 180, 520, 380, '用户与教学组织域', 'USER & CLASS', [
        '用户 User', '角色 Role', '用户角色 UserRole', '班级 Class', '班级成员 ClassMember'], A)
    domain(700, 180, 600, 380, '学习内容域', 'CONTENT', [
        '教学文书 Document', '标注指南 Guide', '标签 Label', '关系类型 RelationType'], B)
    domain(700, 700, 600, 300, '练习域', 'EXERCISE', [
        '练习 Exercise', '练习目标 ExerciseTarget', '练习布置 ExerciseAssignment'], C)
    domain(700, 1100, 600, 320, '标注域', 'ANNOTATION', [
        '标注 Annotation（标准样例 / 学生作答）', '命题 Proposition', '关系 Relation',
        '关系参数 RelationArg'], C)
    domain(1540, 1100, 520, 320, '学情与反馈域', 'LEARNING', [
        '差异项 Difference', '反馈 Feedback', '掌握度 Mastery', '学习记录 LearningLog'], D)

    def arrow(p1, p2, text, tx=0, ty=0):
        import math
        d.line([p1, p2], fill='#9aa694', width=3)
        ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
        for s in (-0.42, 0, 0.42):
            d.line([p2, (p2[0] - 16 * math.cos(ang + s), p2[1] - 16 * math.sin(ang + s))],
                   fill='#9aa694', width=3)
        mx, my = (p1[0] + p2[0]) / 2 + tx, (p1[1] + p2[1]) / 2 + ty
        f = F(19)
        w, h = tw(d, text, f)
        d.rounded_rectangle([mx - w / 2 - 9, my - h / 2 - 7, mx + w / 2 + 9, my + h / 2 + 7],
                            radius=8, fill='white', outline='#dbe2d5')
        center_text(d, mx, my, text, f, '#4d5c4a')

    # 用户域 → 练习域（正交折线）
    d.line([(330, 560), (330, 790)], fill='#9aa694', width=3)
    d.line([(330, 790), (700, 790)], fill='#9aa694', width=3)
    import math
    for s in (-0.42, 0, 0.42):
        d.line([(700, 790), (700 - 16 * math.cos(s), 790 - 16 * math.sin(s))],
               fill='#9aa694', width=3)
    f = F(19)
    txt = '教师创建练习'
    w, h = tw(d, txt, f)
    d.rounded_rectangle([340 - 9, 790 - h / 2 - 7, 340 + w + 9, 790 + h / 2 + 7],
                        radius=8, fill='white', outline='#dbe2d5')
    d.text((340, 790 - h / 2 - 4), txt, font=f, fill='#4d5c4a')

    # 内容域 ↓ 练习域
    arrow((1000, 560), (1000, 700), '文书与指南被练习引用', 0, -18)
    # 练习域 ↓ 标注域
    arrow((1000, 1000), (1000, 1100), '练习产生标注', 0, -18)
    # 标注域 → 学情域
    arrow((1300, 1260), (1540, 1260), '生成差异与掌握度', 0, -26)

    d.text((70, H - 60), '说明：箭头表示跨域的外键引用方向；实体完整属性与主外键见图 3–图 6 及第四部分数据字典。',
           font=F(19), fill=MUTED)
    p = os.path.join(OUT, 'erd-domains.png')
    img.save(p)
    print('saved', p, img.size)


# =====================================================================
# 图 2：Chen 记法核心联系图
# =====================================================================
def draw_chen():
    W, H = 2500, 1420
    img = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(img)
    title_block(d, W, '图 2  核心联系的概念模型（Chen 记法）',
                '矩形＝实体　菱形＝联系　连线两端标注基数（1 / N / M）；属性在第四部分以表格给出')

    EW, EH = 200, 76
    P = {
        'ROLE': (170, 180), 'USER': (170, 560),
        'CLASS': (820, 180), 'EXERCISE': (820, 560),
        'ANNOTATION': (1500, 560), 'PROPOSITION': (2100, 560),
        'GUIDE': (820, 1050), 'LABEL': (1350, 1080),
    }

    def put(key, label):
        x, y = P[key]
        rect_entity(d, x, y, EW, EH, label)

    put('ROLE', '角色 Role'); put('USER', '用户 User')
    put('CLASS', '班级 Class'); put('EXERCISE', '练习 Exercise')
    put('ANNOTATION', '标注 Annotation'); put('PROPOSITION', '命题 Proposition')
    put('GUIDE', '指南 Guide'); put('LABEL', '标签 Label')

    def c(x, y, t, dx=0, dy=0):
        card(d, (x, y), t, dx=dx, dy=dy)

    # 1) 角色 M—N 扮演 用户
    d.line([(170, 218), (170, 330)], fill=LINE, width=2)
    diamond(d, 170, 372, 150, 76, '扮演')
    d.line([(170, 410), (170, 522)], fill=LINE, width=2)
    c(178, 240, 'M'); c(178, 505, 'N')

    # 2) 用户 1—N 创建 教师 1—N 班级
    d.line([(270, 560), (470, 400)], fill=LINE, width=2)
    diamond(d, 548, 372, 150, 74, '创建')
    d.line([(625, 350), (720, 195)], fill=LINE, width=2)
    c(300, 510, '1'); c(700, 205, 'N')

    # 3) 班级 1—N 布置 M—N 练习
    d.line([(820, 218), (820, 330)], fill=LINE, width=2)
    diamond(d, 820, 372, 160, 76, '布置')
    d.line([(820, 410), (820, 522)], fill=LINE, width=2)
    c(828, 240, '1'); c(828, 505, 'M')

    # 4) 练习 1—N 作答 N—1 标注
    d.line([(920, 560), (1075, 560)], fill=LINE, width=2)
    diamond(d, 1160, 560, 160, 76, '作答')
    d.line([(1240, 560), (1400, 560)], fill=LINE, width=2)
    c(940, 528, '1'); c(1390, 528, 'N')

    # 5) 标注 1—N 包含 N—1 命题
    d.line([(1600, 560), (1715, 560)], fill=LINE, width=2)
    diamond(d, 1800, 560, 160, 76, '包含')
    d.line([(1880, 560), (2000, 560)], fill=LINE, width=2)
    c(1620, 528, '1'); c(1990, 528, 'N')

    # 6) 练习 M—N 针对 N—1 标签
    d.line([(880, 598), (1090, 780)], fill=LINE, width=2)
    diamond(d, 1150, 812, 160, 76, '针对')
    d.line([(1230, 848), (1312, 1042)], fill=LINE, width=2)
    c(960, 690, 'M'); c(1322, 1030, 'N', 18, -34)

    # 7) 指南 1—N 定义 N—1 标签
    d.line([(920, 1050), (1005, 1066)], fill=LINE, width=2)
    diamond(d, 1085, 1070, 160, 72, '定义')
    d.line([(1165, 1074), (1250, 1080)], fill=LINE, width=2)
    c(940, 1018, '1'); c(1248, 1044, 'N')

    # 8) 命题 N—1 标记 N—1 标签
    d.line([(2100, 598), (1905, 862)], fill=LINE, width=2)
    diamond(d, 1840, 900, 160, 76, '标记')
    d.line([(1762, 918), (1452, 1068)], fill=LINE, width=2)
    c(2050, 660, 'N'); c(1468, 1052, '1')

    # 9) 用户 1—N 作答者 N—1 标注（底部回环）
    d.line([(1500, 598), (1500, 1200)], fill=LINE, width=2)
    d.line([(1500, 1200), (120, 1200)], fill=LINE, width=2)
    d.line([(120, 1200), (120, 598)], fill=LINE, width=2)
    diamond(d, 820, 1200, 180, 70, '作答者')
    c(1510, 640, 'N'); c(128, 620, '1')

    d.text((70, H - 52),
           '建模要点：①学生与练习之间是带属性的 M:N 联系（作答时间、状态、版本），按规则提升为实体「标注」；'
           '②标准样例与学生作答共用同一结构，仅以类型区分。',
           font=F(19), fill=MUTED)
    p = os.path.join(OUT, 'erd-chen.png')
    img.save(p)
    print('saved', p, img.size)


# =====================================================================
# 域 A：用户与教学组织
# =====================================================================
def draw_domain_a():
    W, H = 2160, 1030
    img = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(img)
    title_block(d, W, '图 3  ERD（一）用户与教学组织域',
                '矩形＝实体，标题条下为属性；PK＝主键，FK＝外键，UK＝唯一约束')

    entity(d, 70, 170, 540, 340, '用户 User', [
        ('PK', 'user_id', 'BIGINT'), ('', 'name', 'VARCHAR(40)'),
        ('UK', 'account', 'VARCHAR(40)'), ('', 'password_hash', 'VARCHAR(120)'),
        ('', 'status', 'VARCHAR(12)'), ('', 'created_at', 'DATETIME')])

    entity(d, 760, 170, 520, 250, '用户角色 UserRole', [
        ('PK,FK', 'user_id', 'BIGINT'), ('PK,FK', 'role_id', 'BIGINT'),
        ('', 'granted_at', 'DATETIME')], bridge=True)

    entity(d, 1440, 170, 520, 290, '角色 Role', [
        ('PK', 'role_id', 'INT'), ('UK', 'role_code', 'VARCHAR(20)'),
        ('', 'role_name', 'VARCHAR(30)'), ('', 'description', 'VARCHAR(200)')])

    entity(d, 70, 640, 540, 290, '班级 Class', [
        ('PK', 'class_id', 'BIGINT'), ('', 'class_name', 'VARCHAR(60)'),
        ('', 'term', 'VARCHAR(20)'), ('FK', 'teacher_id', 'BIGINT'),
        ('', 'created_at', 'DATETIME')])

    entity(d, 760, 640, 540, 280, '班级成员 ClassMember', [
        ('PK,FK', 'class_id', 'BIGINT'), ('PK,FK', 'user_id', 'BIGINT'),
        ('', 'member_role', 'VARCHAR(12)'), ('', 'joined_at', 'DATETIME')], bridge=True)

    def pair(p1, c1, p2, c2, text, ty=None):
        """在两点之间画线，基数放在线段两端外侧。"""
        d.line([p1, p2], fill=LINE, width=2)
        card(d, p1, c1, dx=8, dy=-30)
        card(d, p2, c2, dx=-26, dy=-30)
        edge_label(d, p1, p2, text, 0.5, 0, -16 if ty is None else ty)

    # 用户 1—N 用户角色 N—1 角色
    pair((610, 260), '1', (760, 260), 'N', '拥有')
    pair((1280, 260), 'N', (1440, 260), '1', '属于')

    # 用户 1—N 创建（教师）N—1 班级：竖直
    d.line([(340, 510), (340, 640)], fill=LINE, width=2)
    card(d, (340, 516), '1', dx=8, dy=0)
    card(d, (348, 606), 'N', dx=0, dy=0)
    edge_label(d, (340, 510), (340, 640), '教师创建班级', 0.5, 96, 0)

    # 班级 1—N 班级成员
    pair((610, 780), '1', (760, 780), 'N', '班级含成员')

    # 班级成员 N—1 用户（沿左边界回环）
    d.line([(880, 920), (880, 980)], fill=LINE, width=2)
    d.line([(880, 980), (40, 980)], fill=LINE, width=2)
    d.line([(40, 980), (40, 400)], fill=LINE, width=2)
    d.line([(40, 400), (70, 400)], fill=LINE, width=2)
    card(d, (890, 938), 'N', dx=0, dy=0)
    card(d, (48, 420), '1', dx=0, dy=0)

    p = os.path.join(OUT, 'erd-a.png')
    img.save(p)
    print('saved', p, img.size)


# =====================================================================
# 域 B：学习内容
# =====================================================================
def draw_domain_b():
    W, H = 2020, 1250
    img = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(img)
    title_block(d, W, '图 4  ERD（二）学习内容域',
                '指南冻结版本；标签支持父子层级（自反联系）；关系类型由指南规定')

    entity(d, 60, 240, 540, 68 + 7 * 42 + 8, '标注指南 Guide', [
        ('PK', 'guide_id', 'BIGINT'), ('UK', 'version_no', 'VARCHAR(20)'),
        ('', 'name', 'VARCHAR(60)'), ('', 'granularity_rule', 'TEXT'),
        ('FK', 'publisher_id', 'BIGINT'), ('', 'published_at', 'DATETIME'),
        ('', 'status', 'VARCHAR(12)')])

    entity(d, 700, 240, 540, 68 + 7 * 42 + 8, '标签 Label', [
        ('PK', 'label_id', 'BIGINT'), ('UK', 'code', 'VARCHAR(12)'),
        ('', 'name', 'VARCHAR(40)'), ('', 'definition', 'VARCHAR(300)'),
        ('', 'level', 'TINYINT'), ('FK', 'parent_id', 'BIGINT'),
        ('FK', 'guide_id', 'BIGINT')])

    entity(d, 700, 760, 540, 68 + 5 * 42 + 8, '关系类型 RelationType', [
        ('PK', 'type_id', 'INT'), ('UK', 'code', 'CHAR(1)'),
        ('', 'name', 'VARCHAR(20)'), ('', 'expr_template', 'VARCHAR(60)'),
        ('', 'arg_rule', 'VARCHAR(120)')])

    entity(d, 1340, 240, 620, 68 + 11 * 42 + 8, '教学文书 Document', [
        ('PK', 'doc_id', 'BIGINT'), ('UK', 'case_no', 'VARCHAR(40)'),
        ('', 'court', 'VARCHAR(80)'), ('', 'court_level', 'VARCHAR(20)'),
        ('', 'instance', 'VARCHAR(20)'), ('', 'judgment_date', 'DATE'),
        ('', 'cause', 'VARCHAR(40)'), ('', 'case_nature', 'VARCHAR(20)'),
        ('', 'reasoning_text', 'TEXT'), ('', 'span_start / span_end', 'INT'),
        ('FK', 'uploader_id', 'BIGINT')])

    # 指南 1—N 定义 N—1 标签
    d.line([(600, 330), (700, 330)], fill=LINE, width=2)
    card(d, (606, 300), '1'); card(d, (676, 300), 'N')
    edge_label(d, (600, 330), (700, 330), '定义', 0.5, 0, 34)

    # 指南 1—N 规定 N—1 关系类型（斜线）
    d.line([(560, 612), (676, 812)], fill=LINE, width=2)
    card(d, (566, 628), '1', 0, 0); card(d, (648, 790), 'N', 0, 0)
    edge_label(d, (600, 650), (676, 812), '规定', 0.5, 58, -6)

    # 标签自反联系（上方回环）
    d.line([(920, 240), (920, 196)], fill=LINE, width=2)
    d.line([(920, 196), (1150, 196)], fill=LINE, width=2)
    d.line([(1150, 196), (1150, 240)], fill=LINE, width=2)
    card(d, (900, 214), '1', -8, 0); card(d, (1158, 214), 'N', 0, 0)
    edge_label(d, (1035, 196), (1035, 196), '父子', 0.5, 0, -4)

    d.text((60, H - 56),
           '说明：Label.parent_id 自反引用实现"一级标签 / 二级子类型"两层结构；'
           'Document 与练习的联系见域 C（练习引用文书）。',
           font=F(19), fill=MUTED)
    p = os.path.join(OUT, 'erd-b.png')
    img.save(p)
    print('saved', p, img.size)


# =====================================================================
# 域 C：练习与标注
# =====================================================================
def draw_domain_c():
    W, H = 2720, 1110
    img = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(img)
    title_block(d, W, '图 5  ERD（三）练习与标注域',
                '标注区分为"标准样例"与"学生作答"；关系可嵌套，故关系参数以（关系, 序号）为主键并互斥引用命题或关系')

    entity(d, 60, 240, 520, 68 + 9 * 42 + 8, '练习 Exercise', [
        ('PK', 'exercise_id', 'BIGINT'), ('', 'title', 'VARCHAR(80)'),
        ('', 'type', 'VARCHAR(20)'), ('', 'difficulty', 'TINYINT'),
        ('', 'objective', 'VARCHAR(300)'), ('FK', 'doc_id', 'BIGINT'),
        ('FK', 'guide_id', 'BIGINT'), ('FK', 'teacher_id', 'BIGINT'),
        ('', 'publish_at / due_at', 'DATETIME')])

    entity(d, 700, 240, 520, 68 + 3 * 42 + 8, '练习目标 ExerciseTarget', [
        ('PK,FK', 'exercise_id', 'BIGINT'), ('PK,FK', 'label_id', 'BIGINT'),
        ('', 'weight', 'DECIMAL(3,2)')], bridge=True)

    entity(d, 700, 560, 520, 68 + 5 * 42 + 8, '练习布置 ExerciseAssignment', [
        ('PK', 'assign_id', 'BIGINT'), ('FK', 'exercise_id', 'BIGINT'),
        ('FK', 'class_id', 'BIGINT'), ('', 'assigned_at', 'DATETIME'),
        ('', 'due_at', 'DATETIME')], bridge=True)

    entity(d, 1360, 240, 540, 68 + 8 * 42 + 8, '标注 Annotation', [
        ('PK', 'annotation_id', 'BIGINT'), ('FK', 'exercise_id', 'BIGINT'),
        ('FK', 'student_id', 'BIGINT'), ('', 'kind', 'CHAR(6) 标准/学生'),
        ('', 'version_no', 'INT'), ('', 'status', 'VARCHAR(12)'),
        ('', 'started_at / submitted_at', 'DATETIME'),
        ('', 'duration_sec', 'INT')])

    entity(d, 2020, 240, 540, 68 + 6 * 42 + 8, '命题 Proposition', [
        ('PK', 'prop_id', 'BIGINT'), ('FK', 'annotation_id', 'BIGINT'),
        ('', 'seq_no', 'INT'), ('FK', 'label_id', 'BIGINT'),
        ('', 'char_start / char_end', 'INT'),
        ('', 'argument_unit', 'VARCHAR(8)')])

    entity(d, 1360, 740, 540, 68 + 4 * 42 + 8, '关系 Relation', [
        ('PK', 'rel_id', 'BIGINT'), ('FK', 'annotation_id', 'BIGINT'),
        ('FK', 'type_id', 'INT'), ('', 'expr_text', 'VARCHAR(200)')])

    entity(d, 2020, 740, 540, 68 + 5 * 42 + 8, '关系参数 RelationArg', [
        ('PK,FK', 'rel_id', 'BIGINT'), ('PK', 'seq_no', 'TINYINT'),
        ('', 'ref_type', 'CHAR(4) 命题/关系'),
        ('FK', 'ref_prop_id', 'BIGINT'), ('FK', 'ref_rel_id', 'BIGINT')], bridge=True)

    # 1) 练习 1—N 针对 N—1 练习目标
    d.line([(580, 320), (700, 320)], fill=LINE, width=2)
    card(d, (588, 292), '1'); card(d, (672, 292), 'N')
    edge_label(d, (580, 320), (700, 320), '针对', 0.5, 0, 34)

    # 2) 练习 1—N 布置 N—1 练习布置
    d.line([(580, 640), (700, 640)], fill=LINE, width=2)
    card(d, (588, 612), '1'); card(d, (672, 612), 'N')
    edge_label(d, (580, 640), (700, 640), '布置', 0.5, 0, 34)

    # 3) 练习 1—N 产生 N—1 标注（顶部总线）
    d.line([(300, 240), (300, 190)], fill=LINE, width=2)
    d.line([(300, 190), (1420, 190)], fill=LINE, width=2)
    d.line([(1420, 190), (1420, 240)], fill=LINE, width=2)
    card(d, (308, 214), '1'); card(d, (1400, 214), 'N')
    edge_label(d, (860, 190), (860, 190), '产生', 0.5, 0, -4)

    # 4) 标注 1—N 包含 N—1 命题
    d.line([(1900, 320), (2020, 320)], fill=LINE, width=2)
    card(d, (1906, 292), '1'); card(d, (1994, 292), 'N')
    edge_label(d, (1900, 320), (2020, 320), '包含', 0.5, 0, 34)

    # 5) 标注 1—N 包含 N—1 关系
    d.line([(1630, 682), (1630, 740)], fill=LINE, width=2)
    card(d, (1640, 700), '1'); card(d, (1640, 744), 'N')
    edge_label(d, (1630, 682), (1630, 740), '包含', 0.5, 86, 0)

    # 6) 关系 1—N 组成 N—1 关系参数
    d.line([(1900, 840), (2020, 840)], fill=LINE, width=2)
    card(d, (1906, 812), '1'); card(d, (1994, 812), 'N')
    edge_label(d, (1900, 840), (2020, 840), '组成', 0.5, 0, 34)

    # 7) 命题 1—N 被引用 N—1 关系参数（竖直）
    d.line([(2200, 568), (2200, 740)], fill=LINE, width=2)
    card(d, (2210, 590), '1'); card(d, (2210, 716), 'N')
    edge_label(d, (2200, 568), (2200, 740), '被引用', 0.5, 92, 0)

    d.text((60, H - 56),
           '要点：RelationArg 用 ref_type + 两个互斥可空外键表达"参数可以是命题，也可以是另一个关系"；'
           '既保留嵌套能力，又避免多态外键无法建约束。',
           font=F(19), fill=MUTED)
    p = os.path.join(OUT, 'erd-c.png')
    img.save(p)
    print('saved', p, img.size)


# =====================================================================
# 域 D：学情与反馈
# =====================================================================
def draw_domain_d():
    W, H = 2600, 970
    img = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(img)
    title_block(d, W, '图 6  ERD（四）学情与反馈域',
                '虚线框为其他域的实体，仅用于说明外键指向')

    entity(d, 60, 240, 560, 68 + 7 * 42 + 8, '差异项 Difference', [
        ('PK', 'diff_id', 'BIGINT'), ('FK', 'student_ann_id', 'BIGINT'),
        ('FK', 'standard_ann_id', 'BIGINT'), ('', 'category', 'VARCHAR(12)'),
        ('', 'object_ref', 'VARCHAR(60)'),
        ('', 'student_value / standard_value', 'VARCHAR(40)'),
        ('', 'is_mastered', 'BOOLEAN')])

    entity(d, 700, 240, 540, 68 + 6 * 42 + 8, '反馈 Feedback', [
        ('PK', 'feedback_id', 'BIGINT'), ('FK', 'annotation_id', 'BIGINT'),
        ('FK', 'author_id', 'BIGINT'), ('', 'type', 'VARCHAR(12)'),
        ('', 'content', 'TEXT'), ('', 'created_at', 'DATETIME')])

    entity(d, 1320, 240, 540, 68 + 6 * 42 + 8, '掌握度 Mastery', [
        ('PK,FK', 'student_id', 'BIGINT'), ('PK,FK', 'label_id', 'BIGINT'),
        ('', 'correct_cnt', 'INT'), ('', 'total_cnt', 'INT'),
        ('', 'mastery_rate', 'DECIMAL(4,3)'), ('', 'updated_at', 'DATETIME')])

    entity(d, 1940, 240, 560, 68 + 6 * 42 + 8, '学习记录 LearningLog', [
        ('PK', 'log_id', 'BIGINT'), ('FK', 'student_id', 'BIGINT'),
        ('FK', 'exercise_id', 'BIGINT'), ('', 'action', 'VARCHAR(20)'),
        ('', 'detail', 'VARCHAR(200)'), ('', 'created_at', 'DATETIME')])

    def ctx(cx, cy, w, text):
        d.rounded_rectangle([cx - w / 2, cy - 35, cx + w / 2, cy + 35],
                            radius=9, fill=FILL_CTX, outline='#b9c2b3', width=2)
        center_text(d, cx, cy, text, F(21), '#6b7669')

    ctx(340, 760, 470, '标注 Annotation（域 C）')
    ctx(970, 760, 460, '用户 User（域 A）')
    ctx(1590, 760, 460, '标签 Label（域 B）')
    ctx(2220, 760, 500, '练习 Exercise（域 C）')

    # 差异项的双外键（学生标注 / 标准标注）
    d.line([(300, 610), (300, 725)], fill=LINE, width=2)
    d.line([(380, 610), (380, 725)], fill=LINE, width=2)
    card(d, (292, 622), 'N', -8, 0); card(d, (392, 622), 'N', 2, 0)
    edge_label(d, (300, 690), (380, 710), '学生标注 / 标准标注', 0.5, 0, 0)

    # 反馈 → 用户（反馈人）
    d.line([(900, 568), (940, 725)], fill=LINE, width=2)
    card(d, (856, 590), 'N'); card(d, (948, 700), '1')

    # 掌握度 → 标签
    d.line([(1520, 568), (1570, 725)], fill=LINE, width=2)
    card(d, (1478, 590), 'N'); card(d, (1578, 700), '1')

    # 学习记录 → 练习
    d.line([(2160, 568), (2200, 725)], fill=LINE, width=2)
    card(d, (2120, 590), 'N'); card(d, (2208, 700), '1')

    d.text((60, H - 52),
           '说明：差异项同时引用"学生标注"与"标准标注"两个 Annotation 实体，属两条独立外键；'
           '掌握度按（学生, 标签）累计判定结果，支撑按薄弱标签定向组卷。',
           font=F(19), fill=MUTED)
    p = os.path.join(OUT, 'erd-d.png')
    img.save(p)
    print('saved', p, img.size)


draw_domains()
draw_chen()
draw_domain_a()
draw_domain_b()
draw_domain_c()
draw_domain_d()
