# -*- coding: utf-8 -*-
"""Assemble the three sequence diagrams into one Word document."""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

PROJ = r'C:\Users\32354\Documents\deepseek-harness\default-workspace\法律论证标注系统'
OUTDIR = os.path.join(PROJ, '过程文件', '输出')
DOCX = os.path.join(PROJ, '法律论证标注系统-顺序图集-含激活条.docx')

IMGS = [
    ('图 1　标注主流程的系统顺序图', os.path.join(OUTDIR, 'seq-main.png'),
     '按需求文档的四个阶段（创建任务 → 标注 → 冲突解决 → 结果输出）串起端到端主流程：'
     '创建任务者上传文书并冻结标签版本，两位标注员各自独立完成“颗粒度切割 → 要素标注 → 关系标注 → 图示确认”，'
     '系统计算颗粒度差异率并在超阈值时退回重切；裁定者汇总多版本差异、逐条裁定并留痕；最后由创建者导出数据与图示。',
     [['阶段一 创建标注任务', '上传文书 → 智能提取“裁判理由” → 确认范围与案例信息 → 引用并冻结指南版本 v1.2 → 分配标注员与裁定者 → 写入任务库',
       '需求 2.1–2.3；Q3（任务期标签不变）'],
      ['阶段二 独立标注', '（loop）对每份已分配文书、每位标注员独立执行：① 颗粒度切割 ② 要素标注 ③ 关系标注 ④ 图示确认；'
                          '完成后写入该标注员版本；系统计算两版颗粒度差异率，>10% 退回重切',
       '需求 3.1–3.6；指南 8.2.3、步骤一'],
      ['阶段三 冲突解决', '（opt 存在差异）逐条人工比对：采纳某一方 / 取并集 / 直接重标；填写裁定理由；'
                          '一致项自动通过；核心概念分歧登记疑难问题台账并提交专家确认',
       '需求 4.1–4.2；Q11、Q13'],
      ['阶段四 结果输出', '选择导出内容与文件名 → 读取最终版本生成导出包并写入下载记录 → 返回压缩包，数据置为只读',
       '需求 5.1–5.3；Q18（不加密）']]),
    ('图 2　关系标注的详细顺序图（含关系“图形化展示”）', os.path.join(OUTDIR, 'seq-relation.png'),
     '本图细化“关系标注”这一用例，并把需求 3.5“系统自动生成符号表示”与 3.6“论证图示生成/交互”落成具体消息：'
     '关系在图上通过拖动图元建立，服务端保存关系数据后交由图示渲染器按指南第 6 章的图元规范重绘。'
     '图中用红色（graph）标注的消息都与图形化展示有关。',
     [['① 进入关系标注', '标注界面请求命题清单与坐标系，图示渲染器按论证单元分区渲染：命题＝矩形（框内仅写序号）',
       '需求 3.6.1；指南 6.1（命题节点不显示类型）'],
      ['② 建立关系', '点击起点与终点图元（节点可为命题，也可为已有关系，用于嵌套）→ 选择关系类型 S/A/J/M/I → '
                     '提交（类型＋参数列表）→ 规则校验器校验：组合成员 ≥2、匹配双方个别↔一般、无环、无重复；'
                     '（alt 校验不通过）返回违规项与指南依据并在图上标红',
       '需求 3.5.1–3.5.2；指南 5.3.3'],
      ['③ 图形化展示', '服务端写入关系记录（编号、类型、参数、形式化表达、父关系、论证单元）→ 通知图示渲染器重绘 → '
                       '计算图元与坐标（关系节点置于连线中点；嵌套关系自内而外逐层构造）→ 回写形式化表达 '
                       'S(M(J(P4,P5),P2),P6) →（loop）逐条按类型出图：S 实心圆●+有向边、A 空心圆○+有向边、'
                       'J/M 带“+”圆（J 无向连线、M 有向边）、I 矩形框内“/”',
       '需求 3.5.1、3.6.1；指南第 6 章表 8'],
      ['④ 图示交互与双向联动', '拖动方框调整布局 / 缩放 / 平移 → 提交坐标变化 → 坐标写回关系数据并保存；'
                               '切换论证单元分图查看（一份文书含多个独立论证结构）',
       '需求 3.6.2；Q9（关系在图建立）'],
      ['⑤ 导出与确认', '请求导出图示（PNG/JPG/SVG）→ 返回图示文件（矢量为 SVG）→ 提交关系版本并锁定，进入裁定阶段',
       '需求 5.1.1']]),
    ('图 3　标注任务创建的详细顺序图', os.path.join(OUTDIR, 'seq-create.png'),
     '本图细化“创建标注任务”这一用例，重点体现三类约束：文书的智能提取与人工校正、'
     '指南与标签版本在任务内的冻结、以及“文书 ↔ 标注员”多对多的分配关系。',
     [['① 新建任务与文书导入', '特权用户登录 → 新建任务（任务名、案例类型、标注份数/份）→ 校验角色权限 → '
                               '创建任务草稿 → 上传文书（可批量）→ 文书解析器按“本院认为”“判决如下”定位裁判理由 → '
                               '返回正文与理由区间',
       '需求 2.1（三种格式、批量上传、智能提取）'],
      ['② 标注范围与案例信息确认', '人工校正标注范围（例如排除“综上所述，依照……判决如下：”）→ 服务端校验范围合法且不越界 → '
                                   '锁定范围（后续命题的字符索引基准）→ 填写案例信息 → 必填项校验，缺失则阻止进入下一步',
       '需求 2.1.2、3.2；指南表 1'],
      ['③ 指南与标签版本冻结', '打开指南版本库选择并冻结 v1.2 → 查询该版本的标签体系与关系类型 → '
                               '返回标签 13 个（SF/GF/SM/GM 及子类型、SM-C、IS/Non）与关系 5 种（S/A/J/M/I）→ '
                               '冻结为标签集 LS-v1.2 并与任务绑定（任务期内不可增删改）',
       '需求 2.2.1；Q3、Q5'],
      ['④ 分配标注员与裁定者', '选择 ≥2 名标注员与裁定者 → 提交分配（文书 ↔ 标注员 多对多）→ '
                               '校验权限与重复分配 → 生成每位标注员的独立标注任务 → 返回任务清单（可再次分配给新增标注员）',
       '需求 2.3；Q1（人员可增加）'],
      ['⑤ 任务生效与通知', '确认创建（可设截止时间）→ 任务状态置为“已创建”并写操作日志 → 通知标注员 → '
                           '标注员点“下一条”领取，文书置为“标注中”',
       '需求 2.3；Q2（数据可增加）']]),
]


def set_font(run, ascii_font, ea_font, size=None, bold=None, color=None):
    run.font.name = ascii_font
    if size:
        run.font.size = size
    if bold is not None:
        run.bold = bold
    if color:
        run.font.color.rgb = color
    rPr = run._element.get_or_add_rPr()
    rf = rPr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts'); rPr.insert(0, rf)
    for k in ('w:ascii', 'w:hAnsi', 'w:cs'):
        rf.set(qn(k), ascii_font)
    rf.set(qn('w:eastAsia'), ea_font)


def set_table_width(t, widths):
    tbl = t._tbl
    tblPr = tbl.tblPr
    for tag in ('w:tblW', 'w:tblLayout'):
        for el in tblPr.findall(qn(tag)):
            tblPr.remove(el)
    el = OxmlElement('w:tblW'); el.set(qn('w:type'), 'dxa')
    el.set(qn('w:w'), str(int(round(sum(widths) * 567)))); tblPr.append(el)
    el = OxmlElement('w:tblLayout'); el.set(qn('w:type'), 'fixed'); tblPr.append(el)
    for grid in tbl.findall(qn('w:tblGrid')):
        tbl.remove(grid)
    grid = OxmlElement('w:tblGrid')
    for w in widths:
        gc = OxmlElement('w:gridCol'); gc.set(qn('w:w'), str(int(round(w * 567)))); grid.append(gc)
    tbl.insert(list(tbl).index(tblPr) + 1, grid)
    for row in t.rows:
        for i, c in enumerate(row.cells):
            c.width = Cm(widths[i])


doc = Document()
s = doc.sections[0]
s.page_width = Cm(21.0)
s.page_height = Cm(29.7)
s.left_margin = s.right_margin = Cm(2.0)
s.top_margin = Cm(1.8)
s.bottom_margin = Cm(1.8)
USABLE = 16.4

normal = doc.styles['Normal']
normal.font.name = 'Times New Roman'
normal.font.size = Pt(10.5)
normal.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
normal.paragraph_format.space_after = Pt(4)
normal.paragraph_format.line_spacing = 1.25


def heading(text, level=1):
    p = doc.add_heading('', level=level)
    p.paragraph_format.space_before = Pt(8 if level > 1 else 0)
    p.paragraph_format.space_after = Pt(5)
    r = p.add_run(text)
    sizes = {1: Pt(17), 2: Pt(14), 3: Pt(12)}
    set_font(r, 'Times New Roman', '微软雅黑', size=sizes.get(level, Pt(12)), bold=True,
             color=RGBColor(0x1F, 0x30, 0x50))
    return p


def para(text, size=10.5, bold=False, color=None, italic=False):
    p = doc.add_paragraph()
    r = p.add_run(text)
    set_font(r, 'Times New Roman', '宋体', size=Pt(size), bold=bold, color=color)
    r.italic = italic
    return p


def bullets(items, size=10.5):
    for it in items:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(1.5)
        p.paragraph_format.left_indent = Cm(0.75)
        r = p.add_run(it)
        set_font(r, 'Times New Roman', '宋体', size=Pt(size))


def grid_table(header, rows, widths, sizes=None):
    sizes = sizes or [10] * len(header)
    t = doc.add_table(rows=0, cols=len(header))
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    t.autofit = False
    cells = t.add_row().cells
    for i, h in enumerate(header):
        p = cells[i].paragraphs[0]
        p.paragraph_format.space_after = Pt(1)
        set_font(p.add_run(h), 'Times New Roman', '微软雅黑', size=Pt(sizes[i]), bold=True)
    for row in rows:
        cells = t.add_row().cells
        for i in range(len(header)):
            v = row[i] if i < len(row) else ''
            p = cells[i].paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.12
            set_font(p.add_run(v), 'Times New Roman', '宋体', size=Pt(sizes[i]))
    set_table_width(t, widths)
    return t


# ---------------- 封面与说明 ----------------
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(2)
set_font(p.add_run('法律论证结构标注系统'), 'Times New Roman', '微软雅黑', size=Pt(20), bold=True,
         color=RGBColor(0x1F, 0x30, 0x50))
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(10)
set_font(p.add_run('系统顺序图集（主流程 / 关系标注 / 任务创建）'), 'Times New Roman', '微软雅黑',
         size=Pt(14), bold=True, color=RGBColor(0x1F, 0x30, 0x50))

grid_table(['文档版本', 'v1.0'],
           [['编制日期', '2026-10-14'], ['图数量', '3 张（主流程图 + 2 张详细图）'],
            ['依据材料', '《裁判文书标记需求_按阶段组织》v1.1；《v1.2 …标注与图示指南》']],
           [3.4, 13.6])

heading('一、读图说明（UML 顺序图元件）', 1)
bullets([
    '顶部与底部的方框是参与者（对象）；从参与者垂下的虚线是它的生命线，代表它在整个交互中的存在时间。',
    '生命线上加粗的琥珀色长条是激活条：参与者在这段时间内正在执行操作——每次调用使它向下延伸，'
    '返回消息到达后收束；同一参与者在不同区段的操作分成多条，中间留出空档（因此不会出现"全程激活"的假象）。',
    '实线箭头＝同步消息（调用）；虚线箭头＝返回消息；两条相邻消息之间的竖直距离就是该操作占用的时间段。',
    '左下角带小三角的 tag 是交互片段：loop（循环）、alt（条件分支，可含 else）、opt（可选），括号内写条件。',
    '本图集中，蓝色消息为界面/用户操作，黑色为服务调用，红色（标注 graph）的消息与需求 3.6“图形化展示”直接相关，'
    '紫色消息表示读写数据存储。',
])

# ---------------- 三张图 ----------------
for idx, (title, img, intro, rows) in enumerate(IMGS):
    doc.add_page_break()
    heading('二、%s' % title, 1)
    para(intro, size=10.5)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.add_run().add_picture(img, width=Cm(USABLE))
    cap = doc.add_paragraph(); cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_font(cap.add_run(title), 'Times New Roman', '微软雅黑', size=Pt(10), bold=True)
    heading('要点与需求对照', 2)
    grid_table(['交互片段', '主要消息流', '对应需求 / 指南'], rows, [3.4, 9.4, 3.6], [9.5, 9.5, 9.5])

doc.save(DOCX)
print('saved', DOCX)
print('paragraphs', len(doc.paragraphs), 'tables', len(doc.tables))
