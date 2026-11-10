# -*- coding: utf-8 -*-
"""生成《法律论证模型教学辅助模块：自然语言描述与 ERD》Word 文档。"""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.section import WD_ORIENT, WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BASE = r'C:\Users\32354\Documents\deepseek-harness\default-workspace\法律论证标注系统'
ERD = os.path.join(BASE, '过程文件', '输出', 'erd')
OUT = os.path.join(BASE, '法律论证模型教学辅助模块-自然语言描述与ERD.docx')

INK = RGBColor(0x1F, 0x2D, 0x24)
HEAD = RGBColor(0x2E, 0x50, 0x41)
MUTED = RGBColor(0x62, 0x6D, 0x60)
ACCENT = RGBColor(0x8A, 0x5A, 0x12)

doc = Document()


# ---------------- 基础工具 ----------------
def set_run(run, size=10.5, bold=False, color=INK, font_cn='宋体', font_en='Times New Roman'):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = font_en
    run._element.rPr.rFonts.set(qn('w:eastAsia'), font_cn)


def para(text='', size=10.5, bold=False, color=INK, font_cn='宋体', indent=True,
         space_before=0, space_after=6, align=WD_ALIGN_PARAGRAPH.JUSTIFY, line=1.5):
    p = doc.add_paragraph()
    p.alignment = align
    pf = p.paragraph_format
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing = line
    if indent:
        pf.first_line_indent = Pt(size * 2)
    if text:
        r = p.add_run(text)
        set_run(r, size, bold, color, font_cn)
    return p


def h1(text, num=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(10)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    set_run(r, 16, True, HEAD, '黑体')
    # 下划一条细线
    pPr = p._p.get_or_add_pPr()
    pbdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:color'), 'C9D6C0')
    bottom.set(qn('w:space'), '4')
    pbdr.append(bottom)
    pPr.append(pbdr)
    return p


def h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    set_run(r, 13, True, HEAD, '微软雅黑')
    return p


def h3(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    set_run(r, 11.5, True, RGBColor(0x35, 0x50, 0x40), '微软雅黑')
    return p


def bullet(text, size=10.5):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.9)
    p.paragraph_format.first_line_indent = Cm(-0.45)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.45
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run('· ' + text)
    set_run(r, size)
    return p


def caption(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(10)
    r = p.add_run(text)
    set_run(r, 9, False, MUTED, '宋体')
    return p


def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hexcolor)
    tcPr.append(shd)


def set_table_borders(table):
    tbl = table._tbl
    tblPr = tbl.tblPr
    borders = OxmlElement('w:tblBorders')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        el = OxmlElement('w:' + edge)
        el.set(qn('w:val'), 'single')
        el.set(qn('w:sz'), '4')
        el.set(qn('w:space'), '0')
        el.set(qn('w:color'), 'C9D3C4')
        borders.append(el)
    tblPr.append(borders)


def table(headers, rows, widths, size=8.5, header_fill='E7EFE2', align_center=None):
    t = doc.add_table(rows=1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    set_table_borders(t)
    hdr = t.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = ''
        p = hdr[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(h)
        set_run(r, size, True, HEAD, '微软雅黑')
        shade(hdr[i], header_fill)
    # 表头行跨页重复 + 行内不拆分
    trPr = t.rows[0]._tr.get_or_add_trPr()
    th = OxmlElement('w:tblHeader'); th.set(qn('w:val'), 'true'); trPr.append(th)
    cs = OxmlElement('w:cantSplit'); cs.set(qn('w:val'), 'true'); trPr.append(cs)
    for row in rows:
        r_ = t.add_row()
        trPr2 = r_._tr.get_or_add_trPr()
        cs2 = OxmlElement('w:cantSplit'); cs2.set(qn('w:val'), 'true'); trPr2.append(cs2)
        cells = r_.cells
        for i, v in enumerate(row):
            cells[i].text = ''
            p = cells[i].paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.15
            if align_center and i in align_center:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(str(v))
            set_run(r, size)
    for i, w in enumerate(widths):
        for row in t.rows:
            row.cells[i].width = Cm(w)
    return t


def add_page_field(p):
    run = p.add_run()
    fld1 = OxmlElement('w:fldChar'); fld1.set(qn('w:fldCharType'), 'begin')
    instr = OxmlElement('w:instrText'); instr.set(qn('xml:space'), 'preserve'); instr.text = 'PAGE'
    fld2 = OxmlElement('w:fldChar'); fld2.set(qn('w:fldCharType'), 'end')
    run._r.append(fld1); run._r.append(instr); run._r.append(fld2)
    set_run(run, 9, False, MUTED)


def footer_for(section):
    p = section.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run('法律论证模型教学辅助模块 · 自然语言描述与 ERD　　')
    set_run(r, 9, False, MUTED)
    add_page_field(p)


def page(section, landscape=False):
    if landscape:
        section.orientation = WD_ORIENT.LANDSCAPE
        section.page_width, section.page_height = Cm(29.7), Cm(21.0)
        section.left_margin = section.right_margin = Cm(2.0)
        section.top_margin = section.bottom_margin = Cm(1.8)
    else:
        section.orientation = WD_ORIENT.PORTRAIT
        section.page_width, section.page_height = Cm(21.0), Cm(29.7)
        section.left_margin = section.right_margin = Cm(2.4)
        section.top_margin = section.bottom_margin = Cm(2.3)


page(doc.sections[0], False)
footer_for(doc.sections[0])

# =====================================================================
# 封面
# =====================================================================
for _ in range(4):
    doc.add_paragraph()

p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('法律论证模型教学辅助模块')
set_run(r, 26, True, HEAD, '微软雅黑')

p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(6)
r = p.add_run('自然语言描述与实体—联系模型（ERD）')
set_run(r, 18, True, RGBColor(0x3F, 0x6A, 0x52), '微软雅黑')

p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(10)
r = p.add_run('—— 面向法学课程的论证结构标注教学子系统')
set_run(r, 12, False, MUTED, '宋体')

for _ in range(5):
    doc.add_paragraph()

info = doc.add_table(rows=5, cols=2)
info.alignment = WD_TABLE_ALIGNMENT.CENTER
info.style = 'Table Grid'
tblPr = info._tbl.tblPr
_b = OxmlElement('w:tblBorders')
for _e in ('top','left','bottom','right','insideH','insideV'):
    _x = OxmlElement('w:'+_e); _x.set(qn('w:val'),'none'); _x.set(qn('w:sz'),'0')
    _b.append(_x)
tblPr.append(_b)
info.autofit = False
rows_info = [
    ('课程名称', '信息系统分析与设计'),
    ('作业主题', 'ERD 建模：法律论证模型教学辅助模块'),
    ('作　　　者', 'zzq'),
    ('院系 / 专业', '南京大学　法学'),
    ('完成日期', '2026 年 10 月 25 日'),
]
for i, (k, v) in enumerate(rows_info):
    c0, c1 = info.rows[i].cells
    c0.width, c1.width = Cm(4.0), Cm(8.0)
    p0 = c0.paragraphs[0]; p0.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r0 = p0.add_run(k + '：'); set_run(r0, 10.5, False, MUTED)
    p1 = c1.paragraphs[0]
    r1 = p1.add_run(v); set_run(r1, 10.5, False, INK)

doc.add_page_break()

# =====================================================================
# 目录
# =====================================================================
h1('目　录')
toc = [
    ('第一部分　自然语言描述', ''),
    ('　1.1　模块定位与系统边界', ''),
    ('　1.2　业务目标与度量指标', ''),
    ('　1.3　用户角色与职责', ''),
    ('　1.4　功能需求', ''),
    ('　1.5　关键业务规则', ''),
    ('　1.6　数据需求概述', ''),
    ('　1.7　非功能需求', ''),
    ('　1.8　典型业务场景', ''),
    ('第二部分　ERD 构建流程', ''),
    ('　2.1　构建流程总览', ''),
    ('　2.2　步骤一：需求抽取与候选实体', ''),
    ('　2.3　步骤二：实体确定与主键', ''),
    ('　2.4　步骤三：联系识别与基数判定', ''),
    ('　2.5　步骤四：属性设计与规范化', ''),
    ('　2.6　步骤五：多对多联系的拆解', ''),
    ('　2.7　步骤六：完整性校验', ''),
    ('第三部分　结果 ERD', ''),
    ('　3.1　数据域总览', ''),
    ('　3.2　核心概念模型（Chen 记法）', ''),
    ('　3.3　逻辑 ERD（四个数据域）', ''),
    ('第四部分　数据字典与联系清单', ''),
    ('　4.1　实体属性字典', ''),
    ('　4.2　联系清单', ''),
    ('　4.3　主键与外键汇总', ''),
    ('第五部分　需求覆盖对照与建模说明', ''),
    ('　5.1　功能需求覆盖对照', ''),
    ('　5.2　关键建模决策', ''),
    ('　5.3　局限与后续工作', ''),
]
for item, _ in toc:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.3
    r = p.add_run(item)
    set_run(r, 10, item.startswith('第'), HEAD if item.startswith('第') else INK,
            '微软雅黑' if item.startswith('第') else '宋体')

doc.add_page_break()

# =====================================================================
# 第一部分
# =====================================================================
h1('第一部分　自然语言描述')

h2('1.1　模块定位与系统边界')
para('法律论证模型教学辅助模块是面向法学课程的教学子系统。它把"法律论证模型"这一抽象的分析框架，'
     '落到真实的裁判文书之上：学生阅读法院裁判理由，按规范把说理切分为命题要素，为每个要素选择'
     '事实判断或规范判断的标签，再在要素之间建立支持、反对、组合、匹配、同一等论证关系，最后由系统'
     '生成论证结构图。学生"在文本上做结构"，而不是"背结构名称"，从而真正理解要件事实、规范基础与'
     '裁判结论之间如何被理由连接起来。')
para('模块的边界是"教学与练习"，不承担司法实务中的正式标注生产。它向下依赖三份基础数据：'
     '教学文书（裁判理由原文）、标注指南（标签体系与颗粒度规则）、标准样例（教师给出的参考答案）；'
     '向上输出四类教学产物：学生的作答与反馈、按标签聚合的学情、面向薄弱点的练习、以及可供教学研究的'
     '结构化数据（JSON / CSV / 图示）。')

h2('1.2　业务目标与度量指标')
para('本模块有两条核心业务目标，二者互为支撑：学生学得又快又好，教师才拿得到可靠的学情；'
     '教师看得清学情，才能把练习发到学生的薄弱处。')
h3('目标一：提升学生学习法律论证模型的效率与效果')
bullet('效率：系统以"切分 → 标签 → 关系 → 读图"的固定步骤引导，配合即时校验（区间重叠、关系参数约束、'
       '循环引用），把学生原本在纸面上的反复试错收敛为可控的几步。度量：单次练习平均完成时长、'
       '首次提交时的规则错误数、重做次数。')
bullet('效果：以教师发布的标准样例为参照，自动给出三项量化指标——标签一致率、关系一致率、颗粒度差异率；'
       '并把这些差异归入"边界 / 标签 / 关系"三类错题。度量：三项指标的提升曲线、同类错题的复现率。')
h3('目标二：帮助教师掌握学情并针对性发布练习')
bullet('学情可见：按"班级—学生—标签"三个维度呈现掌握率、错误类型分布、练习完成度与耗时，'
       '使教师能回答"哪个班、哪个学生、哪个标签最弱"。')
bullet('针对性发布：系统按掌握率低于阈值的标签生成推荐练习池，教师可指定目标标签、难度、题量与截止时间，'
       '一键发布到班级；发布后学生端即时可见。')
para('两条目标在数据上通过"差异项（Difference）"与"掌握度（Mastery）"两个实体闭环：'
     '差异项记录一次作答与标准样例在具体对象上的分歧，掌握度把差异累计为按标签的稳定估计，'
     '教师据此决策，学生据此复练。', indent=True)

h2('1.3　用户角色与职责')
table(['角色', '职责', '可见范围'],
      [['学生', '领取练习、独立完成标注、查看反馈与错题、重做提升', '本班练习、自己的作答与反馈'],
       ['教师', '维护班级与账号、上传文书、配置指南与标准样例、发布练习、批阅、查看学情', '其所任教班级的全部数据'],
       ['裁定者', '对存在争议的标注（如标签分歧、关系结构分歧）进行复核与裁定', '被指派任务的差异与版本'],
       ['系统', '自动比对作答与标准样例、生成差异项、更新掌握度、生成推荐', '全部（内部计算）']],
      [2.2, 8.4, 4.6], align_center=[0])

h2('1.4　功能需求')
table(['编号', '功能', '说明'],
      [['FR-01', '账号与角色', '教师创建账号并分配角色；学生用账号登录，角色决定可见模块与操作权限。'],
       ['FR-02', '班级管理', '教师创建班级、添加或移除成员；班级是练习发布与学情统计的单位。'],
       ['FR-03', '教学文书管理', '上传 TXT/Word/PDF 文书，系统定位"本院认为"至"判决如下"之间的裁判理由区间，'
                                '支持人工校正起止位置。'],
       ['FR-04', '指南与标签体系', '导入或维护标注指南（标签定义、颗粒度规则、关系类型），以版本号冻结；'
                                 '任务绑定版本，运行中不可修改。'],
       ['FR-05', '练习创建与定向组卷', '选择文书与指南，设定题型、难度、目标标签与题量；系统按薄弱标签推荐。'],
       ['FR-06', '练习发布', '将练习发布到一个或多个班级，设定开始与截止时间；发布后学生端可见。'],
       ['FR-07', '学生作答工作台', '三栏式界面：原文与切分、命题与标签、论证关系图；支持拖拽节点、缩放图示。'],
       ['FR-08', '自动比对', '提交后与标准样例比对，输出差异清单（边界/标签/关系）与三项一致率。'],
       ['FR-09', '反馈与批阅', '教师查看作答、填写评语、标记典型错误；学生端看到反馈与差异依据。'],
       ['FR-10', '学情看板', '按班级/学生/标签查看掌握率、错误分布、完成度与耗时趋势。'],
       ['FR-11', '错题本与重练', '自动收集差异项形成个人错题本，支持按标签重练并记录改进。'],
       ['FR-12', '导出与归档', '导出 JSON（字符索引 + 标签 + 关系）、CSV、结构图 SVG 与教学报告。']],
      [1.6, 3.6, 10.2], align_center=[0])

h2('1.5　关键业务规则')
table(['编号', '规则'],
      [['BR-01', '一个练习绑定一份教学文书与一个指南版本；练习发布后，文书与指南版本冻结，不得修改。'],
       ['BR-02', '练习必须已有标准样例，才允许开放自动比对；否则学生只能查看自己的作答。'],
       ['BR-03', '学生作答与标准样例物理隔离，互不覆盖；学生临时编辑不写入标准样例。'],
       ['BR-04', '每个命题必须落在裁判理由区间内，且命题之间不得重叠；切分以句号为主，句内再考察逗号与分号，'
                 '双引号内保持整体。'],
       ['BR-05', '关系类型与参数约束：支持（S）与反对（A）各两个有序参数；组合（J）与同一（I）至少两个成员，'
                 '且同一（I）的成员只能是命题；匹配（M）的来源须为个别判断（SF/SM）、目标须为一般判断（GF/GM）；'
                 '反对（A）的目标只能是命题或支持关系。'],
       ['BR-06', '同一份标注中不得重复建立类型与参数序列完全相同的关系。'],
       ['BR-07', '提交后作答锁定；允许"重做"生成新版本，历史版本保留以支持学习轨迹。'],
       ['BR-08', '差异分为三类：边界（切分不一致）、标签（同一区间标签不同）、关系（关系结构不同）。'],
       ['BR-09', '一致率口径：颗粒度差异率 = |A命题数 − B命题数| ÷ 较大者；标签一致率 = 同位标签相同的命题数 ÷ 较大者；'
                 '关系一致率 = 两侧关系表达式集合的交集大小 ÷ 较大者。'],
       ['BR-10', '掌握度按（学生, 标签）累计，默认取最近 10 次判定；掌握率 = 正确判定数 ÷ 判定总数。'],
       ['BR-11', '定向推荐阈值默认 0.6：掌握率低于阈值的标签进入推荐池，按错误频次排序。'],
       ['BR-12', '教师只能访问自己所任教班级的数据；学生只能访问自己的作答与教师已发布的反馈。']],
      [1.6, 13.8], align_center=[0])

h2('1.6　数据需求概述')
para('从数据形态看，本模块处理五类数据：')
table(['类别', '内容', '规模估计（单班一学期）'],
      [['基础数据', '账号、角色、班级、班级成员', '学生 40–120 人；班级 1–4 个'],
       ['内容数据', '教学文书、指南版本、标签、关系类型', '文书 10–40 份（每份 200–3000 字理由）；标签约 12 个；关系类型 5 种'],
       ['教学数据', '练习、练习目标、练习布置', '练习 20–60 个；每个练习 1 份文书'],
       ['过程数据', '标注（标准/学生）、命题、关系、关系参数、学习记录', '每次作答 5–30 个命题、3–20 条关系'],
       ['结果数据', '差异项、反馈、掌握度', '每个学生每练习 0–10 条差异；掌握度按标签累计']],
      [2.4, 7.6, 5.4], align_center=[0])

h2('1.7　非功能需求')
table(['类别', '要求'],
      [['性能', '打开练习到可交互 < 1 s；标注操作响应 < 100 ms；3000 字文书的切分与关系校验 < 200 ms。'],
       ['并发', '支持一个班级 40 人同时作答；同一版本采用乐观锁，冲突时提示刷新。'],
       ['安全', '密码使用不可逆散列存储；接口按角色与班级校验权限；导出文件含操作者与时间。'],
       ['可靠性', '作答自动保存草稿；提交为事务操作，失败不产生半成品版本。'],
       ['可追溯', '标准样例、作答、差异、反馈、裁定均保留时间与操作者，支持按版本回溯。'],
       ['可移植', '导出 JSON 带 schema_version 与字符索引口径，可被外部工具复现。']],
      [2.4, 13.0], align_center=[0])

h2('1.8　典型业务场景')
h3('场景一：学生完成一次练习并得到反馈')
para('学生李明登录后进入学习与反馈，看到教师布置的《劳务合同纠纷（第一批）》练习。系统按三步引导：'
     '先对照颗粒度规则切分裁判理由，得到 13 个命题；再为每个命题选择标签，遇到"本院认为，依法成立的合同"'
     '时，系统提示"该句包含规范依据"；最后在命题之间建立关系，尝试建立 M 关系时因目标不是一般判断被拒绝，'
     '系统给出规则说明。提交后，系统与标准样例比对：标签一致率 12/13，关系一致率 8/10，颗粒度差异率 0；'
     '差异清单列出 P10 的标签分歧与两处关系结构差异，并附指南原文依据。学生据此修改，并加入错题本。')
h3('场景二：教师依据学情发布针对性练习')
para('王老师打开学情看板，班级视图显示：本周练习完成率 92%，但"一般规范判断的子类型（GM-L / GM-I）"'
     '的平均掌握率为 0.54，"组合与匹配关系的区分"为 0.61，均低于 0.6 阈值。系统据此推荐两组练习：'
     '一组以 GM 子类型辨析为目标标签、难度中等、5 道题；另一组以 M 关系匹配为目标、难度较高、3 道题。'
     '王老师确认题量、设定截止时间后一键发布到班级，学生端随即出现新的练习卡片。')

# =====================================================================
# 第二部分
# =====================================================================
doc.add_page_break()
h1('第二部分　ERD 构建流程')

h2('2.1　构建流程总览')
para('本次建模按六个步骤推进，每一步的输出都是下一步的输入：')
table(['步骤', '任务', '输出'],
      [['① 需求抽取', '从自然语言描述中抽取名词与动词，形成候选实体与候选联系', '候选实体清单、候选联系清单'],
       ['② 实体确定', '判定名词是否为独立实体（合并同义、剔除派生与属性），为主键选型', '实体清单 + 主键'],
       ['③ 联系识别', '判定实体之间的语义联系，确定基数（1:1 / 1:N / M:N）', '联系清单 + 基数'],
       ['④ 属性与规范化', '为实体补齐属性，做 1NF/2NF/3NF 检查', '属性字典'],
       ['⑤ 拆解与细化', 'M:N 联系拆为关联实体；带属性的联系提升为实体；递归与多态处理', '逻辑 ERD'],
       ['⑥ 完整性校验', '对照业务目标与功能需求检查覆盖与冗余', '校验记录、需求覆盖表']],
      [2.6, 8.8, 4.0])

h2('2.2　步骤一：需求抽取与候选实体')
para('对第一部分的功能需求与场景做名词扫描，并对每个候选词做"是否独立实体"的判定。'
     '判定标准有三条：是否具有独立标识；是否被多处引用；是否只是其他实体的属性或视图。')
table(['候选名词', '判定', '理由'],
      [['学生 / 教师', '合并为「用户」', '两类人共享账号、姓名等属性，差异由角色表达；且同一用户可兼多角色'],
       ['角色', '独立实体', '角色可授予多人，且需独立维护代码与说明；与用户为 M:N'],
       ['班级', '独立实体', '有独立标识，是练习发布与统计的单位'],
       ['教学文书', '独立实体', '有独立标识与案号，被多个练习引用'],
       ['指南 / 标签 / 关系类型', '三个独立实体', '指南有版本；标签有父子层级；关系类型有参数约束，均被多处引用'],
       ['练习', '独立实体', '教学活动的核心对象，被布置、作答、统计多处引用'],
       ['目标标签（练习针对哪些标签）', 'M:N 联系', '本质是练习与标签之间的多对多关系，拆为关联实体'],
       ['布置（练习发到班级）', 'M:N 联系', '练习与班级多对多，拆为关联实体'],
       ['作答 / 标注', '独立实体', '是学生与练习之间的多对多联系，且带时间、状态、版本等属性——按规则提升为实体'],
       ['命题 / 关系 / 关系参数', '三个独立实体', '命题是标注的组成部分；关系可嵌套，参数需有序，故单独成实体'],
       ['标准样例', '不单独建实体', '与学生作答结构相同，用「标注.kind」区分，避免结构重复'],
       ['差异项', '独立实体', '记录两个标注在具体对象上的分歧，带类别与是否掌握'],
       ['反馈', '独立实体', '教师/系统对某次标注的评语，需保留作者与时间'],
       ['掌握度', '独立实体（统计）', '按（学生, 标签）聚合的派生数据，物化存储以支撑看板与推荐'],
       ['学习记录', '独立实体', '行为日志，用于过程性评价'],
       ['成绩 / 得分', '剔除', '可由差异项与掌握度计算得出，属派生数据，存储会引入不一致'],
       ['题库 / 知识点', '剔除', '题库是练习的视图；知识粒度以标签为准，另建知识点会与标签重复']],
      [4.6, 3.2, 7.6], align_center=[1])

h2('2.3　步骤二：实体确定与主键')
para('经上一步筛选，得到 16 个实体。主键一律采用与业务无关的代理键（自增或雪花 ID），'
     '业务唯一性用唯一约束表达（如账号、案号、指南版本号、标签代码），避免业务字段变化影响引用关系。'
     '关联实体使用复合主键（两到三个外键列组合），天然表达"同一组合只能出现一次"。')
table(['序号', '实体', '主键', '主要唯一约束'],
      [['1', '用户 User', 'user_id', 'account'],
       ['2', '角色 Role', 'role_id', 'role_code'],
       ['3', '用户角色 UserRole', '(user_id, role_id)', '—'],
       ['4', '班级 Class', 'class_id', '—'],
       ['5', '班级成员 ClassMember', '(class_id, user_id)', '—'],
       ['6', '教学文书 Document', 'doc_id', 'case_no'],
       ['7', '标注指南 Guide', 'guide_id', 'version_no'],
       ['8', '标签 Label', 'label_id', 'code（同一指南内）'],
       ['9', '关系类型 RelationType', 'type_id', 'code'],
       ['10', '练习 Exercise', 'exercise_id', '—'],
       ['11', '练习目标 ExerciseTarget', '(exercise_id, label_id)', '—'],
       ['12', '练习布置 ExerciseAssignment', 'assign_id', '(exercise_id, class_id)'],
       ['13', '标注 Annotation', 'annotation_id', '(exercise_id, student_id, version_no)'],
       ['14', '命题 Proposition', 'prop_id', '(annotation_id, seq_no)'],
       ['15', '关系 Relation', 'rel_id', '—'],
       ['16', '关系参数 RelationArg', '(rel_id, seq_no)', '—'],
       ['17', '差异项 Difference', 'diff_id', '—'],
       ['18', '反馈 Feedback', 'feedback_id', '—'],
       ['19', '掌握度 Mastery', '(student_id, label_id)', '—'],
       ['20', '学习记录 LearningLog', 'log_id', '—']],
      [1.4, 5.2, 4.6, 4.2], align_center=[0, 2])

h2('2.4　步骤三：联系识别与基数判定')
para('基数判定依据业务语义而不是直觉。例如"一个班级可以有多个学生，一个学生也可以属于多个班级"，'
     '所以班级与用户是 M:N；而"一个练习只使用一份文书，一份文书可被多个练习复用"，'
     '所以文书与练习是 1:N。下表列出主要联系（完整清单见 4.2）。')
table(['联系', '参与实体', '基数', '业务依据'],
      [['拥有', '用户—角色', 'M:N', '一人可兼多角色，一角色可授予多人'],
       ['创建班级', '用户（教师）—班级', '1:N', '一位教师可带多个班；一个班有唯一班主任'],
       ['加入', '班级—用户', 'M:N', '学生可跨班选修'],
       ['上传', '用户（教师）—文书', '1:N', '一位教师上传多份文书'],
       ['制定', '用户（教师）—指南', '1:N', '一位教师可发布多个指南版本'],
       ['定义', '指南—标签', '1:N', '一个版本内定义若干标签'],
       ['隶属', '标签—标签', '1:N（递归）', '一级标签下可有二级子类型'],
       ['规定', '指南—关系类型', '1:N', '一个版本内规定若干关系类型'],
       ['引用', '练习—文书', 'N:1', '一个练习锁定一份文书'],
       ['遵循', '练习—指南', 'N:1', '一个练习绑定一个指南版本'],
       ['针对', '练习—标签', 'M:N', '一个练习可针对多个薄弱标签'],
       ['布置', '练习—班级', 'M:N', '同一练习可布置到多个班级'],
       ['产生', '练习—标注', '1:N', '一个练习对应多份作答（含标准样例）'],
       ['作答者', '用户（学生）—标注', '1:N', '一名学生可有多次作答'],
       ['包含', '标注—命题', '1:N', '一份标注包含多个命题'],
       ['包含', '标注—关系', '1:N', '一份标注包含多条关系'],
       ['标记', '命题—标签', 'N:1', '一个命题选择一个标签'],
       ['采用', '关系—关系类型', 'N:1', '一条关系采用一种关系类型'],
       ['组成', '关系—关系参数', '1:N', '一条关系由有序参数构成'],
       ['指向', '关系参数—命题', 'N:1', '参数可引用命题'],
       ['指向', '关系参数—关系', 'N:1', '参数也可引用另一关系（嵌套）'],
       ['比对', '差异项—标注', 'N:1 ×2', '每条差异同时引用学生标注与标准标注'],
       ['评价', '反馈—标注', 'N:1', '一条反馈针对一份标注'],
       ['给出', '反馈—用户', 'N:1', '反馈由某位教师或系统给出'],
       ['统计', '掌握度—用户 / 标签', 'N:1 ×2', '按（学生, 标签）聚合'],
       ['记录', '学习记录—用户 / 练习', 'N:1 ×2', '行为归属于某学生与某练习']],
      [1.8, 5.2, 2.2, 6.0], align_center=[0, 2])

h2('2.5　步骤四：属性设计与规范化')
para('属性设计遵循"只存原始事实、不存可推导结果"的原则，唯一例外是掌握度——它是为了看板与推荐性能而物化的统计结果，'
     '并明确标注为派生数据。规范化检查如下：')
bullet('第一范式（1NF）：所有属性均为原子值。练习的"目标标签"不写成逗号分隔字符串，而是拆为 ExerciseTarget 关联实体；'
       '关系的参数不写成 "P4,P5" 字符串，而是拆为 RelationArg 有序行。')
bullet('第二范式（2NF）：关联实体的非主属性完全依赖整个复合主键。例如 ExerciseTarget 的 weight 依赖'
       '（exercise_id, label_id）整体，不能只依赖其中一列；ClassMember 的 member_role 亦然。')
bullet('第三范式（3NF）：消除传递依赖。标注中不冗余存"练习名称""学生姓名"，只存外键；'
       '命题中不存标签名称，只存 label_id；差异项中不存标注副本，只存两个标注外键。')
para('一个需要说明的取舍：差异项同时引用"学生标注"与"标准标注"，两条外键都指向 Annotation。'
     '这在 3NF 上是干净的，但需要在应用层校验二者类型不同（一条 kind=学生，一条 kind=标准）。'
     '另一种做法是建"标注对"实体，但对本场景而言多余，故采用双外键加约束。', indent=True)

h2('2.6　步骤五：多对多联系的拆解')
para('四个 M:N 联系按规则拆为关联实体，其中两个带业务属性，因此成为独立实体而非纯连接表：')
table(['原 M:N 联系', '拆解结果', '附加属性', '说明'],
      [['用户 ↔ 角色', 'UserRole', '授予时间', '记录授权时点，便于审计'],
       ['班级 ↔ 用户', 'ClassMember', '成员角色、加入时间', '区分学生与助教'],
       ['练习 ↔ 标签', 'ExerciseTarget', '权重', '表达该练习对某标签的侧重'],
       ['练习 ↔ 班级', 'ExerciseAssignment', '布置时间、截止时间', '同一练习对不同班级可有不同截止时间']],
      [3.4, 3.6, 3.6, 5.4])
para('另有一个"带属性的 M:N 联系提升为实体"的典型处理：学生与练习之间的"作答"联系带有开始时间、提交时间、'
     '状态、版本号等属性，且被差异项、反馈、学习记录多处引用，因此提升为独立实体「标注 Annotation」。'
     '标准样例与学生作答结构相同，用 kind 字段区分，避免为两者各建一套命题与关系表。', indent=True)

h2('2.7　步骤六：完整性校验')
para('校验从三个方向进行：')
bullet('覆盖性：每一条功能需求都能在模型中找到承载对象（见 5.1 覆盖对照表），无悬空需求。')
bullet('冗余性：不存在两个实体表达同一事实；派生数据（成绩、题库）已剔除或明确标注为统计表。')
bullet('一致性：每个 1:N 联系的主键侧唯一、外键侧可重复；每个 M:N 都已拆解；递归联系（标签父子）已限定层级。')

# =====================================================================
# 第三部分：横向
# =====================================================================
sec = doc.add_section(WD_SECTION.NEW_PAGE)
page(sec, True)

h1('第三部分　结果 ERD')
para('本部分给出建模结果。先以"数据域总览"说明四块数据的分工与跨域引用，再用 Chen 记法给出核心联系的概念模型，'
     '最后按四个数据域给出带属性、主键与外键的逻辑 ERD。图片为矢量风格绘制，可放大查看。', indent=True)

h2('3.1　数据域总览')
doc.add_picture(os.path.join(ERD, 'erd-domains.png'), width=Cm(21.8))
doc.paragraphs[-1].paragraph_format.keep_with_next = True
caption('图 1　法律论证模型教学辅助模块 · 数据域总览')
para('四个域分别回答四个问题：谁在用（用户与教学组织域）、学什么（学习内容域）、怎么练（练习域）、练得怎样'
     '（学情与反馈域）。跨域引用只有六条主链路，域内高内聚、域间低耦合，便于分工实现与后续扩展。', indent=True)

h2('3.2　核心概念模型（Chen 记法）')
doc.add_picture(os.path.join(ERD, 'erd-chen.png'), width=Cm(21.6))
doc.paragraphs[-1].paragraph_format.keep_with_next = True
caption('图 2　核心联系的概念模型（Chen 记法）')
para('图中矩形为实体、菱形为联系，连线两端的 1 / N / M 为基数。需要特别注意两处：其一，"用户—班级"存在两条联系'
     '（创建与加入），分别表达教师任教与学生选课，不能合并；其二，"学生—练习"之间不是简单连线，'
     '而是提升后的实体「标注」，这正是 ERD 构建流程中"带属性联系提升为实体"的规则体现。', indent=True)

h2('3.3　逻辑 ERD（四个数据域）')
doc.add_picture(os.path.join(ERD, 'erd-a.png'), width=Cm(23.8))
doc.paragraphs[-1].paragraph_format.keep_with_next = True
caption('图 3　ERD（一）用户与教学组织域')
para('用户与角色为 M:N，通过 UserRole 关联；班级为教师 1:N 创建，班级与用户为 M:N，通过 ClassMember 关联。'
     '该域的建模关键在于"同一个用户可兼多角色"，因此角色不能作为用户的枚举属性。', indent=True)

doc.add_picture(os.path.join(ERD, 'erd-b.png'), width=Cm(22.4))
doc.paragraphs[-1].paragraph_format.keep_with_next = True
caption('图 4　ERD（二）学习内容域')
para('指南以版本号冻结，一个版本内定义标签与关系类型；标签通过 parent_id 自反引用形成"一级—二级"两层结构。'
     '教学文书独立成实体，被练习引用，使同一份文书可支撑多轮练习。', indent=True)

doc.add_picture(os.path.join(ERD, 'erd-c.png'), width=Cm(24.4))
doc.paragraphs[-1].paragraph_format.keep_with_next = True
caption('图 5　ERD（三）练习与标注域')
para('这是全系统的核心域。练习通过 ExerciseTarget 定向到标签（支撑"针对性发布"），通过 ExerciseAssignment '
     '布置到班级；学生作答与标准样例统一建模为 Annotation，其下挂命题与关系；关系通过 RelationArg 支持嵌套——'
     '参数既可以是命题，也可以是另一条关系，故用 ref_type 加两个互斥可空外键表达。', indent=True)

doc.add_picture(os.path.join(ERD, 'erd-d.png'), width=Cm(24.4))
doc.paragraphs[-1].paragraph_format.keep_with_next = True
caption('图 6　ERD（四）学情与反馈域')
para('差异项同时引用学生标注与标准标注，记录类别、对象、两侧取值与是否已掌握；掌握度按（学生, 标签）累计；'
     '学习记录保存行为轨迹。该域是"教师掌握学情、系统推荐练习"的数据基础。', indent=True)

# =====================================================================
# 第四部分：纵向
# =====================================================================
sec = doc.add_section(WD_SECTION.NEW_PAGE)
page(sec, False)

h1('第四部分　数据字典与联系清单')

h2('4.1　实体属性字典')
para('下表按数据域列出全部实体的属性、类型与约束。PK 为主键，FK 为外键，UK 为唯一约束；'
     '复合主键以括号形式标注。', indent=True)

DOMAINS = [
    ('域一：用户与教学组织', [
        ('用户 User', [('user_id', 'BIGINT', 'PK', '用户标识'),
                       ('name', 'VARCHAR(40)', '', '姓名'),
                       ('account', 'VARCHAR(40)', 'UK', '登录账号'),
                       ('password_hash', 'VARCHAR(120)', '', '密码散列值'),
                       ('status', 'VARCHAR(12)', '', '状态：在用 / 停用'),
                       ('created_at', 'DATETIME', '', '创建时间')]),
        ('角色 Role', [('role_id', 'INT', 'PK', '角色标识'),
                      ('role_code', 'VARCHAR(20)', 'UK', '角色代码：教师 / 学生 / 裁定者'),
                      ('role_name', 'VARCHAR(30)', '', '角色名称'),
                      ('description', 'VARCHAR(200)', '', '职责说明')]),
        ('用户角色 UserRole', [('user_id', 'BIGINT', 'PK,FK', '引用用户'),
                              ('role_id', 'BIGINT', 'PK,FK', '引用角色'),
                              ('granted_at', 'DATETIME', '', '授予时间')]),
        ('班级 Class', [('class_id', 'BIGINT', 'PK', '班级标识'),
                       ('class_name', 'VARCHAR(60)', '', '班级名称'),
                       ('term', 'VARCHAR(20)', '', '学期'),
                       ('teacher_id', 'BIGINT', 'FK', '班主任 / 任课教师'),
                       ('created_at', 'DATETIME', '', '创建时间')]),
        ('班级成员 ClassMember', [('class_id', 'BIGINT', 'PK,FK', '引用班级'),
                                 ('user_id', 'BIGINT', 'PK,FK', '引用用户'),
                                 ('member_role', 'VARCHAR(12)', '', '成员角色：学生 / 助教'),
                                 ('joined_at', 'DATETIME', '', '加入时间')]),
    ]),
    ('域二：学习内容', [
        ('标注指南 Guide', [('guide_id', 'BIGINT', 'PK', '指南标识'),
                           ('version_no', 'VARCHAR(20)', 'UK', '版本号，如 v1.2'),
                           ('name', 'VARCHAR(60)', '', '指南名称'),
                           ('granularity_rule', 'TEXT', '', '颗粒度规则原文'),
                           ('publisher_id', 'BIGINT', 'FK', '发布教师'),
                           ('published_at', 'DATETIME', '', '发布时间'),
                           ('status', 'VARCHAR(12)', '', '状态：草稿 / 已发布 / 停用')]),
        ('标签 Label', [('label_id', 'BIGINT', 'PK', '标签标识'),
                       ('code', 'VARCHAR(12)', 'UK', '标签代码：SF / GF / SM / GM 及子类型'),
                       ('name', 'VARCHAR(40)', '', '标签名称'),
                       ('definition', 'VARCHAR(300)', '', '定义与标志性表述'),
                       ('level', 'TINYINT', '', '层级：1 一级、2 二级'),
                       ('parent_id', 'BIGINT', 'FK', '父标签（自反）'),
                       ('guide_id', 'BIGINT', 'FK', '所属指南版本')]),
        ('关系类型 RelationType', [('type_id', 'INT', 'PK', '类型标识'),
                                  ('code', 'CHAR(1)', 'UK', 'S / A / J / M / I'),
                                  ('name', 'VARCHAR(20)', '', '关系名称'),
                                  ('expr_template', 'VARCHAR(60)', '', '表达式模板'),
                                  ('arg_rule', 'VARCHAR(120)', '', '参数约束说明')]),
        ('教学文书 Document', [('doc_id', 'BIGINT', 'PK', '文书标识'),
                              ('case_no', 'VARCHAR(40)', 'UK', '案号'),
                              ('court', 'VARCHAR(80)', '', '裁判法院'),
                              ('court_level', 'VARCHAR(20)', '', '法院层级'),
                              ('instance', 'VARCHAR(20)', '', '审级'),
                              ('judgment_date', 'DATE', '', '裁判日期'),
                              ('cause', 'VARCHAR(40)', '', '案由'),
                              ('case_nature', 'VARCHAR(20)', '', '案件性质'),
                              ('reasoning_text', 'TEXT', '', '裁判理由全文'),
                              ('span_start / span_end', 'INT', '', '理由区间字符偏移'),
                              ('uploader_id', 'BIGINT', 'FK', '上传教师')]),
    ]),
    ('域三：练习与标注', [
        ('练习 Exercise', [('exercise_id', 'BIGINT', 'PK', '练习标识'),
                          ('title', 'VARCHAR(80)', '', '练习标题'),
                          ('type', 'VARCHAR(20)', '', '题型：基础 / 专项 / 综合'),
                          ('difficulty', 'TINYINT', '', '难度 1–5'),
                          ('objective', 'VARCHAR(300)', '', '练习目标说明'),
                          ('doc_id', 'BIGINT', 'FK', '引用的教学文书'),
                          ('guide_id', 'BIGINT', 'FK', '绑定的指南版本'),
                          ('teacher_id', 'BIGINT', 'FK', '创建教师'),
                          ('publish_at / due_at', 'DATETIME', '', '发布与截止时间')]),
        ('练习目标 ExerciseTarget', [('exercise_id', 'BIGINT', 'PK,FK', '引用练习'),
                                    ('label_id', 'BIGINT', 'PK,FK', '引用标签'),
                                    ('weight', 'DECIMAL(3,2)', '', '该标签的考察权重')]),
        ('练习布置 ExerciseAssignment', [('assign_id', 'BIGINT', 'PK', '布置标识'),
                                        ('exercise_id', 'BIGINT', 'FK', '引用练习'),
                                        ('class_id', 'BIGINT', 'FK', '引用班级'),
                                        ('assigned_at', 'DATETIME', '', '布置时间'),
                                        ('due_at', 'DATETIME', '', '该班截止时间')]),
        ('标注 Annotation', [('annotation_id', 'BIGINT', 'PK', '标注标识'),
                            ('exercise_id', 'BIGINT', 'FK', '引用练习'),
                            ('student_id', 'BIGINT', 'FK', '学生；标准样例为空'),
                            ('kind', 'CHAR(6)', '', '类型：标准 / 学生'),
                            ('version_no', 'INT', '', '版本号（重做递增）'),
                            ('status', 'VARCHAR(12)', '', '状态：草稿 / 已提交'),
                            ('started_at / submitted_at', 'DATETIME', '', '开始与提交时间'),
                            ('duration_sec', 'INT', '', '作答用时（秒）')]),
        ('命题 Proposition', [('prop_id', 'BIGINT', 'PK', '命题标识'),
                             ('annotation_id', 'BIGINT', 'FK', '所属标注'),
                             ('seq_no', 'INT', '', '序号 P1、P2…'),
                             ('label_id', 'BIGINT', 'FK', '所选标签'),
                             ('char_start / char_end', 'INT', '', '原文区间'),
                             ('argument_unit', 'VARCHAR(8)', '', '论证单元编号')]),
        ('关系 Relation', [('rel_id', 'BIGINT', 'PK', '关系标识'),
                          ('annotation_id', 'BIGINT', 'FK', '所属标注'),
                          ('type_id', 'INT', 'FK', '关系类型'),
                          ('expr_text', 'VARCHAR(200)', '', '展开后的表达式，如 S(J(P4,P5),P6)')]),
        ('关系参数 RelationArg', [('rel_id', 'BIGINT', 'PK,FK', '引用关系'),
                                 ('seq_no', 'TINYINT', 'PK', '参数序号（有序）'),
                                 ('ref_type', 'CHAR(4)', '', '参数类型：命题 / 关系'),
                                 ('ref_prop_id', 'BIGINT', 'FK', '引用命题（与下者互斥）'),
                                 ('ref_rel_id', 'BIGINT', 'FK', '引用关系（嵌套）')]),
    ]),
    ('域四：学情与反馈', [
        ('差异项 Difference', [('diff_id', 'BIGINT', 'PK', '差异标识'),
                              ('student_ann_id', 'BIGINT', 'FK', '学生标注'),
                              ('standard_ann_id', 'BIGINT', 'FK', '标准标注'),
                              ('category', 'VARCHAR(12)', '', '类别：边界 / 标签 / 关系'),
                              ('object_ref', 'VARCHAR(60)', '', '差异对象（命题号或关系表达式）'),
                              ('student_value / standard_value', 'VARCHAR(40)', '', '两侧取值'),
                              ('is_mastered', 'BOOLEAN', '', '改正后是否已掌握')]),
        ('反馈 Feedback', [('feedback_id', 'BIGINT', 'PK', '反馈标识'),
                          ('annotation_id', 'BIGINT', 'FK', '被评价的标注'),
                          ('author_id', 'BIGINT', 'FK', '反馈人'),
                          ('type', 'VARCHAR(12)', '', '类型：评语 / 典型错误'),
                          ('content', 'TEXT', '', '反馈内容'),
                          ('created_at', 'DATETIME', '', '创建时间')]),
        ('掌握度 Mastery', [('student_id', 'BIGINT', 'PK,FK', '学生'),
                           ('label_id', 'BIGINT', 'PK,FK', '标签'),
                           ('correct_cnt', 'INT', '', '正确判定次数'),
                           ('total_cnt', 'INT', '', '判定总次数'),
                           ('mastery_rate', 'DECIMAL(4,3)', '', '掌握率（派生）'),
                           ('updated_at', 'DATETIME', '', '更新时间')]),
        ('学习记录 LearningLog', [('log_id', 'BIGINT', 'PK', '记录标识'),
                                 ('student_id', 'BIGINT', 'FK', '学生'),
                                 ('exercise_id', 'BIGINT', 'FK', '关联练习'),
                                 ('action', 'VARCHAR(20)', '', '行为：开始 / 提交 / 查看反馈 / 重做'),
                                 ('detail', 'VARCHAR(200)', '', '补充说明'),
                                 ('created_at', 'DATETIME', '', '发生时间')]),
    ]),
]

for dname, ents in DOMAINS:
    h3(dname)
    rows = []
    for ename, attrs in ents:
        for i, (a, t, cons, note) in enumerate(attrs):
            rows.append([ename if i == 0 else '', a, t, cons, note])
    table(['实体', '属性', '类型', '约束', '说明'], rows, [3.4, 4.4, 3.0, 1.6, 3.8], size=8,
          align_center=[2, 3])

h2('4.2　联系清单')
para('下表汇总全部联系，包含基数与实现方式。1:N 通过外键实现；M:N 通过关联实体实现；'
     '递归与多态联系单独说明。', indent=True)
table(['编号', '联系', '实体 A', '实体 B', '基数', '实现方式'],
      [['R01', '拥有', '用户', '角色', 'M:N', 'UserRole'],
       ['R02', '创建班级', '用户（教师）', '班级', '1:N', 'Class.teacher_id'],
       ['R03', '加入班级', '班级', '用户', 'M:N', 'ClassMember'],
       ['R04', '上传文书', '用户（教师）', '教学文书', '1:N', 'Document.uploader_id'],
       ['R05', '制定指南', '用户（教师）', '标注指南', '1:N', 'Guide.publisher_id'],
       ['R06', '定义标签', '标注指南', '标签', '1:N', 'Label.guide_id'],
       ['R07', '标签隶属', '标签', '标签', '1:N', 'Label.parent_id（自反）'],
       ['R08', '规定关系类型', '标注指南', '关系类型', '1:N', 'RelationType.guide_id'],
       ['R09', '引用文书', '练习', '教学文书', 'N:1', 'Exercise.doc_id'],
       ['R10', '绑定指南', '练习', '标注指南', 'N:1', 'Exercise.guide_id'],
       ['R11', '针对标签', '练习', '标签', 'M:N', 'ExerciseTarget'],
       ['R12', '创建练习', '用户（教师）', '练习', '1:N', 'Exercise.teacher_id'],
       ['R13', '布置练习', '练习', '班级', 'M:N', 'ExerciseAssignment'],
       ['R14', '产生标注', '练习', '标注', '1:N', 'Annotation.exercise_id'],
       ['R15', '作答者', '用户（学生）', '标注', '1:N', 'Annotation.student_id（可空）'],
       ['R16', '包含命题', '标注', '命题', '1:N', 'Proposition.annotation_id'],
       ['R17', '包含关系', '标注', '关系', '1:N', 'Relation.annotation_id'],
       ['R18', '标记', '命题', '标签', 'N:1', 'Proposition.label_id'],
       ['R19', '采用类型', '关系', '关系类型', 'N:1', 'Relation.type_id'],
       ['R20', '组成', '关系', '关系参数', '1:N', 'RelationArg.rel_id'],
       ['R21', '指向命题', '关系参数', '命题', 'N:1', 'RelationArg.ref_prop_id'],
       ['R22', '指向关系', '关系参数', '关系', 'N:1', 'RelationArg.ref_rel_id（嵌套）'],
       ['R23', '比对', '差异项', '标注', 'N:1×2', 'Difference 的双外键'],
       ['R24', '评价', '反馈', '标注', 'N:1', 'Feedback.annotation_id'],
       ['R25', '给出反馈', '反馈', '用户', 'N:1', 'Feedback.author_id'],
       ['R26', '统计掌握', '掌握度', '用户 / 标签', 'N:1×2', 'Mastery 复合主键'],
       ['R27', '记录行为', '学习记录', '用户 / 练习', 'N:1×2', 'LearningLog 外键']],
      [1.4, 2.8, 3.4, 3.4, 1.8, 5.0], size=8, align_center=[0, 4])

h2('4.3　主键与外键汇总')
para('主键共 20 组（含复合主键 5 组）。外键共 25 个约束方向，其中两个需要应用层语义约束：'
     'Annotation.student_id 仅在 kind=学生 时非空；RelationArg 的两个引用列必须且只能有一个非空。')
table(['约束类型', '数量', '说明'],
      [['单列主键', '15', '代理键，全局唯一'],
       ['复合主键', '5', 'UserRole、ClassMember、ExerciseTarget、Mastery、RelationArg'],
       ['唯一约束', '6', 'account、case_no、version_no、label.code、relation_type.code、练习布置组合'],
       ['外键', '25', '含两条指向同一实体的双外键（差异项）'],
       ['应用层约束', '3', '标注类型互斥、关系参数引用互斥、差异项两侧类型不同']],
      [3.4, 2.0, 9.4], align_center=[1])

# =====================================================================
# 第五部分
# =====================================================================
doc.add_page_break()
h1('第五部分　需求覆盖对照与建模说明')

h2('5.1　功能需求覆盖对照')
table(['功能需求', '承载实体 / 联系', '说明'],
      [['FR-01 账号与角色', 'User、Role、UserRole', '多对多角色，支持一人多职'],
       ['FR-02 班级管理', 'Class、ClassMember', '成员与角色分离，支持跨班'],
       ['FR-03 教学文书', 'Document', '理由区间以字符偏移保存，便于回指原文'],
       ['FR-04 指南与标签', 'Guide、Label、RelationType', '版本冻结 + 标签自反层级'],
       ['FR-05 定向组卷', 'Exercise、ExerciseTarget', '标签级定向，带权重'],
       ['FR-06 练习发布', 'ExerciseAssignment', '按班级布置，独立截止时间'],
       ['FR-07 作答工作台', 'Annotation、Proposition、Relation、RelationArg', '统一标注模型，支持嵌套关系'],
       ['FR-08 自动比对', 'Difference', '三类差异，双外键指向两个标注'],
       ['FR-09 反馈与批阅', 'Feedback', '作者与时间可追溯'],
       ['FR-10 学情看板', 'Mastery、Difference、LearningLog', '按标签聚合 + 行为轨迹'],
       ['FR-11 错题本与重练', 'Difference.is_mastered、Annotation.version_no', '差异标记掌握，重做递增版本'],
       ['FR-12 导出归档', '由上述实体投影生成', 'JSON / CSV / SVG / 报告']],
      [3.4, 6.4, 5.2])

h2('5.2　关键建模决策')
bullet('统一标注模型：标准样例与学生作答结构完全相同，仅以 kind 区分。好处是比对算法只需面对一种结构，'
       '差异比较即两个 Annotation 的比较；代价是需要在应用层保证学生作答有 student_id、标准样例为空。')
bullet('关系参数单独成实体：法律论证关系允许嵌套（如"组合关系作为支持关系的理由"），若把参数存成数组，'
       '既无法建外键约束，也无法表达顺序。拆为 RelationArg 后，顺序由 seq_no 表达，引用由互斥外键表达。')
bullet('掌握度物化：掌握度可由差异项实时计算，但看板与推荐会频繁读取，故物化为统计表，并在写入差异时同步更新；'
       '文档中明确其为派生数据，允许重建。')
bullet('指南版本而非标签快照：练习绑定指南版本，标签属于版本。这样旧任务的标注不会因新标签体系而失真，'
       '也避免了在每个命题上冗余存标签定义。')
bullet('字符偏移而非文本切片：命题只存 char_start / char_end，原文存一份。这样原文修订后可用偏移校验，'
       '导出数据也能被外部工具精确复现。')

h2('5.3　局限与后续工作')
bullet('关系参数的互斥外键在部分数据库上难以用纯 DDL 表达，需要触发器或应用层校验；'
       '若目标数据库支持检查约束（CHECK），可直接写成"两列恰有一列非空"。')
bullet('当前模型未包含"领域专家"角色与线下讨论记录，教学场景可以先并入裁定者与反馈实体。')
bullet('掌握度的滑动窗口大小、定向推荐阈值都应可配置，建议后续引入"教学策略"配置表。')
bullet('若需支持小组协作标注，需在 Annotation 之外增加"协作会话"与"分工"实体，本版未建模。')

para('')
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(6)
r = p.add_run('（全文完）')
set_run(r, 9, False, MUTED)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.save(OUT)
print('saved', OUT, os.path.getsize(OUT))
