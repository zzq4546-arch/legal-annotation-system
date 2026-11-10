# -*- coding: utf-8 -*-
"""重写图 1（数据域总览）：纵向流式布局，箭头只连接相邻数据块。"""
import io

P = r'C:\Users\32354\Documents\deepseek-harness\default-workspace\法律论证标注系统\过程文件\脚本\make_erd.py'
s = io.open(P, encoding='utf-8').read()

NEW = '''def draw_domains():
    W, H = 2040, 1470
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
    domain(1420, 1100, 560, 320, '学情与反馈域', 'LEARNING', [
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
        d.line([(700, 790), (700 - 16 * math.cos(math.pi + s), 790 - 16 * math.sin(math.pi + s))],
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
    arrow((1300, 1260), (1420, 1260), '比对生成差异与掌握度', 0, -26)

    d.text((70, H - 60), '说明：箭头表示跨域的外键引用方向；实体完整属性与主外键见图 3–图 6 及第四部分数据字典。',
           font=F(19), fill=MUTED)
    p = os.path.join(OUT, 'erd-domains.png')
    img.save(p)
    print('saved', p, img.size)


'''

start = s.index('def draw_domains():')
nxt = s.index('\n# =====', start + 10)
s = s[:start] + NEW + s[nxt + 1:]
io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('rewrote draw_domains')
