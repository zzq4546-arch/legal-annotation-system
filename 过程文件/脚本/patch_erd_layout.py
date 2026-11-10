# -*- coding: utf-8 -*-
"""重写域 B / C / D 三张 ERD：按属性数自动计算框高，连线端点与框实际边缘对齐。"""
import io

P = r'C:\Users\32354\Documents\deepseek-harness\default-workspace\法律论证标注系统\过程文件\脚本\make_erd.py'
s = io.open(P, encoding='utf-8').read()

NEW_B = '''def draw_domain_b():
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
    d.line([(600, 590), (700, 820)], fill=LINE, width=2)
    card(d, (598, 606), '1', 6, 0); card(d, (676, 796), 'N', -4, 0)
    edge_label(d, (600, 590), (700, 820), '规定', 0.5, 60, -6)

    # 标签自反联系（右侧回环）
    d.line([(1240, 320), (1310, 320)], fill=LINE, width=2)
    d.line([(1310, 320), (1310, 540)], fill=LINE, width=2)
    d.line([(1310, 540), (1240, 540)], fill=LINE, width=2)
    card(d, (1290, 340), 'N', 0, 0); card(d, (1290, 500), '1', 0, 0)
    edge_label(d, (1310, 430), (1310, 430), '父子', 0.5, 52, 0)

    d.text((60, H - 56),
           '说明：Label.parent_id 自反引用实现"一级标签 / 二级子类型"两层结构；'
           'Document 与练习的联系见域 C（练习引用文书）。',
           font=F(19), fill=MUTED)
    p = os.path.join(OUT, 'erd-b.png')
    img.save(p)
    print('saved', p, img.size)


'''

NEW_C = '''def draw_domain_c():
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


'''

NEW_D = '''def draw_domain_d():
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
    card(d, (310, 660), 'N'); card(d, (390, 660), 'N')
    edge_label(d, (300, 680), (380, 700), '学生标注 / 标准标注', 0.5, 0, -6)

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


'''


def replace_func(src, name, new):
    start = src.index('def %s():' % name)
    try:
        nxt = src.index('\n# =====', start + 10)
        tail = src[nxt + 1:]
    except ValueError:
        # 最后一个函数：以调用块为界
        nxt = src.index('\ndraw_domains()', start + 10)
        tail = src[nxt + 1:]
    return src[:start] + new + tail


s = replace_func(s, 'draw_domain_b', NEW_B)
s = replace_func(s, 'draw_domain_c', NEW_C)
s = replace_func(s, 'draw_domain_d', NEW_D)

io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('rewrote domain B/C/D, file chars:', len(s))
