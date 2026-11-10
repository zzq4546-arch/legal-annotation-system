# -*- coding: utf-8 -*-
"""交付前结构校验：段落、表格、图片、章节、关键内容。"""
import os
from docx import Document
from docx.shared import Cm

BASE = r'C:\Users\32354\Documents\deepseek-harness\default-workspace\法律论证标注系统'
P = os.path.join(BASE, '法律论证模型教学辅助模块-自然语言描述与ERD.docx')

doc = Document(P)
text = '\n'.join(p.text for p in doc.paragraphs)
tables = doc.tables


def table_text(t):
    return '\n'.join(c.text for r in t.rows for c in r.cells)


all_table_text = '\n'.join(table_text(t) for t in tables)
rels = doc.part.rels
images = [r for r in rels.values() if 'image' in r.reltype]

print('文件大小: %.1f KB' % (os.path.getsize(P) / 1024))
print('段落数:', len(doc.paragraphs), '| 表格数:', len(tables), '| 内嵌图片数:', len(images))
print('分节数:', len(doc.sections), '| 横向节:', sum(1 for s in doc.sections if s.page_width > s.page_height))
print('正文字符数（段落）:', len(text), '| 表格字符数:', len(all_table_text))

checks = {
    '关键词 业务目标': '业务目标' in text,
    '关键词 ERD 构建流程': 'ERD 构建流程' in text,
    '关键词 实体—联系': '实体—联系' in text,
    '16 个实体全部出现': all(k in all_table_text or k in text for k in
        ['用户 User', '角色 Role', '班级 Class', '教学文书 Document', '标注指南 Guide',
         '标签 Label', '关系类型 RelationType', '练习 Exercise', '练习目标 ExerciseTarget',
         '练习布置 ExerciseAssignment', '标注 Annotation', '命题 Proposition',
         '关系 Relation', '关系参数 RelationArg', '差异项 Difference', '掌握度 Mastery']),
    '五类关系齐备': all(k in all_table_text for k in ['S', 'A', 'J', 'M', 'I']),
    '图 1–图 6 齐备': all(('图 %d' % i) in text for i in range(1, 7)),
    '联系清单 R27': 'R27' in all_table_text,
    '规范化说明': ('第三范式' in text or '3NF' in text),
    '需求覆盖表': 'FR-12' in all_table_text,
}
for k, v in checks.items():
    print(('  ✅ ' if v else '  ❌ ') + k)

print('\n各节页面方向:')
for i, s in enumerate(doc.sections):
    orient = '横向' if s.page_width > s.page_height else '纵向'
    print('  第 %d 节: %s  %.1f × %.1f cm' % (i + 1, orient, s.page_width.cm, s.page_height.cm))
