import sys, zipfile, re
from docx import Document

path = sys.argv[1]
out = sys.argv[2]
doc = Document(path)

lines = []

def para_text(p):
    return p.text

body = doc.element.body
from docx.table import Table
from docx.text.paragraph import Paragraph

def iter_block_items(parent):
    from docx.oxml.ns import qn
    for child in parent.element.body.iterchildren():
        if child.tag == qn('w:p'):
            yield Paragraph(child, parent)
        elif child.tag == qn('w:tbl'):
            yield Table(child, parent)

for block in iter_block_items(doc):
    if isinstance(block, Paragraph):
        style = block.style.name if block.style is not None else ''
        t = block.text
        if t.strip():
            lines.append(f"[{style}] {t}")
        else:
            lines.append("")
    else:
        lines.append("=== TABLE START ===")
        for row in block.rows:
            cells = [c.text.replace("\n", " / ").strip() for c in row.cells]
            lines.append(" | ".join(cells))
        lines.append("=== TABLE END ===")

text = "\n".join(lines)
with open(out, "w", encoding="utf-8") as f:
    f.write(text)
print("paragraphs:", len(doc.paragraphs), "tables:", len(doc.tables), "chars:", len(text))
