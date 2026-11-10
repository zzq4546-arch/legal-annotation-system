# -*- coding: utf-8 -*-
"""Convert the analysis markdown (known, controlled subset) into a clean DOCX."""
import re, sys
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SRC, DST = sys.argv[1], sys.argv[2]
lines = open(SRC, encoding='utf-8').read().split('\n')

BODY_EA = '宋体'
HEAD_EA = '微软雅黑'
MONO = 'Consolas'

doc = Document()

sec = doc.sections[0]
sec.page_width = Cm(21.0)
sec.page_height = Cm(29.7)
sec.left_margin = Cm(2.2)
sec.right_margin = Cm(2.2)
sec.top_margin = Cm(2.2)
sec.bottom_margin = Cm(2.0)
USABLE_CM = 21.0 - 4.4          # A4 width minus margins

normal = doc.styles['Normal']
normal.font.name = 'Times New Roman'
normal.font.size = Pt(10.5)
normal.element.rPr.rFonts.set(qn('w:eastAsia'), BODY_EA)
normal.paragraph_format.space_after = Pt(4)
normal.paragraph_format.line_spacing = 1.3


def set_run_font(run, ascii_font, ea_font, size=None, bold=None):
    run.font.name = ascii_font
    if size:
        run.font.size = size
    if bold is not None:
        run.bold = bold
    rPr = run._element.get_or_add_rPr()
    rf = rPr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts')
        rPr.insert(0, rf)
    rf.set(qn('w:ascii'), ascii_font)
    rf.set(qn('w:hAnsi'), ascii_font)
    rf.set(qn('w:eastAsia'), ea_font)
    rf.set(qn('w:cs'), ascii_font)


HEAD_SPEC = {1: Pt(15), 2: Pt(13), 3: Pt(11.5), 4: Pt(10.5)}

INLINE = re.compile(r'(\*\*.+?\*\*|`[^`]+`)')


def add_inline(par, text, ea=BODY_EA):
    for chunk in INLINE.split(text):
        if not chunk:
            continue
        if chunk.startswith('**') and chunk.endswith('**'):
            r = par.add_run(chunk[2:-2])
            set_run_font(r, 'Times New Roman', ea, bold=True)
        elif chunk.startswith('`') and chunk.endswith('`'):
            r = par.add_run(chunk[1:-1])
            set_run_font(r, MONO, MONO, size=Pt(9))
        else:
            r = par.add_run(chunk)
            set_run_font(r, 'Times New Roman', ea)


def add_code(buf):
    for ln in buf:
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.space_after = Pt(0)
        pf.space_before = Pt(0)
        pf.line_spacing = 1.0
        pf.left_indent = Cm(0.3)
        r = p.add_run(ln if ln.strip() else ' ')
        set_run_font(r, MONO, MONO, size=Pt(8.5))


def _twips_cm(cm):
    return int(round(cm * 567))


def set_table_width(t, widths):
    """Force a fixed table layout with explicit total width and grid columns."""
    tbl = t._tbl
    tblPr = tbl.tblPr
    for tag in ('w:tblW', 'w:tblLayout'):
        for el in tblPr.findall(qn(tag)):
            tblPr.remove(el)
    tblW = OxmlElement('w:tblW')
    tblW.set(qn('w:type'), 'dxa')
    tblW.set(qn('w:w'), str(_twips_cm(sum(widths))))
    tblPr.append(tblW)
    layout = OxmlElement('w:tblLayout')
    layout.set(qn('w:type'), 'fixed')
    tblPr.append(layout)
    # rebuild the grid
    for grid in tbl.findall(qn('w:tblGrid')):
        tbl.remove(grid)
    grid = OxmlElement('w:tblGrid')
    for w in widths:
        gc = OxmlElement('w:gridCol')
        gc.set(qn('w:w'), str(_twips_cm(w)))
        grid.append(gc)
    tbl.insert(list(tbl).index(tblPr) + 1, grid)
    for row in t.rows:
        for i, c in enumerate(row.cells):
            c.width = Cm(widths[i])


def add_table(rows):
    ncol = len(rows[0])
    t = doc.add_table(rows=0, cols=ncol)
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    t.autofit = False

    lens = [0.0] * ncol
    for row in rows:
        for i in range(ncol):
            cell = row[i] if i < len(row) else ''
            lens[i] = max(lens[i], min(len(cell), 60))
    total = sum(lens) or 1
    widths = [max(1.6, USABLE_CM * (l / total)) for l in lens]
    scale = USABLE_CM / sum(widths)
    widths = [w * scale for w in widths]

    for ri, row in enumerate(rows):
        cells = t.add_row().cells
        for i in range(ncol):
            txt = row[i] if i < len(row) else ''
            par = cells[i].paragraphs[0]
            par.paragraph_format.space_after = Pt(1)
            par.paragraph_format.space_before = Pt(1)
            par.paragraph_format.line_spacing = 1.05
            add_inline(par, txt)
            if ri == 0:
                for r in par.runs:
                    r.bold = True
    set_table_width(t, widths)


i, n = 0, len(lines)
while i < n:
    ln = lines[i]
    if ln.startswith('```'):
        j = i + 1
        buf = []
        while j < n and not lines[j].startswith('```'):
            buf.append(lines[j]); j += 1
        add_code(buf)
        i = j + 1
        continue
    m = re.match(r'^(#{1,6})\s+(.*)$', ln)
    if m:
        lvl = min(len(m.group(1)), 4)
        p = doc.add_heading('', level=lvl)
        p.paragraph_format.space_before = Pt(10 if lvl <= 2 else 8)
        p.paragraph_format.space_after = Pt(4)
        par = p
        for chunk in INLINE.split(m.group(2)):
            if not chunk:
                continue
            bold = chunk.startswith('**') and chunk.endswith('**')
            txt = chunk[2:-2] if bold else chunk
            if txt.startswith('`') and txt.endswith('`'):
                txt = txt[1:-1]
            r = par.add_run(txt)
            set_run_font(r, 'Times New Roman', HEAD_EA,
                         size=HEAD_SPEC[lvl], bold=True)
        i += 1
        continue
    if re.match(r'^(\*\*\*|---|___)\s*$', ln):
        doc.add_paragraph('─' * 32).alignment = WD_ALIGN_PARAGRAPH.CENTER
        i += 1
        continue
    if ln.startswith('|') and i + 1 < n and re.match(r'^\|[\s:|-]+\|\s*$', lines[i + 1]):
        rows = []
        j = i
        while j < n and lines[j].startswith('|'):
            if not re.match(r'^\|[\s:|-]+\|\s*$', lines[j]):
                rows.append([c.strip() for c in lines[j].strip().strip('|').split('|')])
            j += 1
        add_table(rows)
        i = j
        continue
    mb = re.match(r'^(\s*)([-*])\s+(.*)$', ln)
    if mb:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.left_indent = Cm(0.7)
        add_inline(p, mb.group(3))
        i += 1
        continue
    mo = re.match(r'^(\s*)(\d+)\.\s+(.*)$', ln)
    if mo:
        p = doc.add_paragraph(style='List Number')
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.left_indent = Cm(0.7)
        add_inline(p, mo.group(3))
        i += 1
        continue
    if ln.startswith('>'):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.6)
        add_inline(p, ln.lstrip('> ').rstrip())
        for r in p.runs:
            r.italic = True
        i += 1
        continue
    if not ln.strip():
        i += 1
        continue
    buf = [ln]
    j = i + 1
    while j < n and lines[j].strip() and not re.match(
            r'^(#{1,6}\s|```|\||>|\s*[-*]\s|\s*\d+\.\s|---|\*\*\*)', lines[j]):
        buf.append(lines[j]); j += 1
    p = doc.add_paragraph()
    add_inline(p, ' '.join(x.strip() for x in buf))
    i = j

doc.save(DST)
print('saved', DST, 'paragraphs', len(doc.paragraphs), 'tables', len(doc.tables))
