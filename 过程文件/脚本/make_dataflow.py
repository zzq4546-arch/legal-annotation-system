# -*- coding: utf-8 -*-
"""法律论证标注系统 · 三条数据流（索引对齐 / SVG 拖拽 / 导图校验）"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, '..', '..'))
os.makedirs(os.path.join(PROJ, '过程文件', '输出', 'dfd'), exist_ok=True)
OUT = os.path.join(PROJ, '数据流图.png')

FR = r'C:\Windows\Fonts\msyh.ttc'
FB = r'C:\Windows\Fonts\msyhbd.ttc'
INK = (33, 45, 38)
MUTED = (110, 120, 110)
LINE = (208, 214, 204)
CREAM = (250, 251, 245)

BLUE, BLUE_L = (45, 84, 106), (233, 240, 244)
AMBER, AMBER_L = (139, 94, 32), (247, 239, 225)
PURP, PURP_L = (110, 58, 79), (245, 235, 239)
GREEN, GREEN_L = (36, 75, 60), (232, 240, 232)


def F(s, bold=False):
    return ImageFont.truetype(FB if bold else FR, s)


def tw(d, s, f):
    b = d.textbbox((0, 0), s, font=f)
    return b[2] - b[0]


def fit(d, s, maxw, size, bold=False, minsize=11):
    while size > minsize and tw(d, s, F(size, bold)) > maxw:
        size -= 1
    return F(size, bold)


def wrap(d, s, maxw, size, bold=False):
    """按像素宽度断行（中文逐字，英文按空格）"""
    f = F(size, bold)
    lines, cur = [], ''
    for ch in s:
        if ch == '\n':
            lines.append(cur)
            cur = ''
            continue
        if tw(d, cur + ch, f) <= maxw:
            cur += ch
        else:
            lines.append(cur)
            cur = ch
    if cur:
        lines.append(cur)
    return lines


def badge(d, x, y, ch, color):
    d.ellipse((x, y, x + 34, y + 34), fill=color)
    d.text((x + 17, y + 17), ch, font=F(19, True), fill='white', anchor='mm')


def step(d, box, num, title, sub, color, fill, store=None):
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, radius=10, fill=fill, outline=color, width=2)
    # 序号
    d.ellipse((x0 + 12, y0 + 12, x0 + 42, y0 + 42), fill=color)
    d.text((x0 + 27, y0 + 27), str(num), font=F(15, True), fill='white', anchor='mm')
    # 标题
    ft = fit(d, title, x1 - x0 - 62, 20, True)
    d.text((x0 + 54, y0 + 16), title, font=ft, fill=INK, anchor='la')
    # 正文
    body = wrap(d, sub, x1 - x0 - 30, 15)
    for i, ln in enumerate(body[:4]):
        d.text((x0 + 16, y0 + 56 + i * 23), ln, font=F(15), fill=(78, 88, 78), anchor='la')
    # 存储标记
    if store:
        ft2 = F(13, True)
        w = tw(d, store, ft2) + 16
        d.rounded_rectangle((x1 - w - 12, y1 - 26, x1 - 12, y1 - 6), radius=8,
                            fill='white', outline=color, width=1)
        d.text((x1 - w / 2 - 12, y1 - 16), store, font=ft2, fill=color, anchor='mm')


def arrow(d, p0, p1, color, w=3):
    d.line([p0, p1], fill=color, width=w)
    x0, y0 = p0
    x1, y1 = p1
    if abs(y1 - y0) >= abs(x1 - x0):
        s = 1 if y1 > y0 else -1
        d.polygon([(x1, y1), (x1 - 9, y1 - 14 * s), (x1 + 9, y1 - 14 * s)], fill=color)
    else:
        s = 1 if x1 > x0 else -1
        d.polygon([(x1, y1), (x1 - 14 * s, y1 - 9), (x1 - 14 * s, y1 + 9)], fill=color)


W, H = 2400, 1806
img = Image.new('RGB', (W, H), 'white')
d = ImageDraw.Draw(img)

d.text((70, 46), '法律论证标注系统 · 三条核心数据流', font=F(42, True), fill=GREEN)
d.text((72, 110), '数据从“裁判理由原文”流到“可校验的论证图”，三条链路各有唯一真源：偏移、坐标、规则。',
       font=F(20), fill=MUTED)
d.text((72, 148), '图中 R/W 表示该步读取 / 写入的数据存储；① 索引对齐　② SVG 拖拽　③ 导图校验',
       font=F(17), fill=(150, 150, 142))

LANES = [
    dict(y=210, h=400, ch='①', title='索引对齐', sub='char 偏移是唯一真源', color=BLUE, fill=BLUE_L, ret=(2,'solid','发现偏差则回退重切'),
         steps=[
             ('文书入库', '原文全文 + 长度；存 docId、text 与 hash（示例 244 字）', 'W D1'),
             ('定位论证区', '“本院认为”之后、“判决如下”之前；得到 span 5–243', 'R D1'),
             ('颗粒度切分', '句号切句；逗号/分号考察子句；同性质合并；得 n 个单元', 'W D1'),
             ('命题落位', '每个命题记 {id, charStart, charEnd, seq}，与切分单元一一对应', 'W D3'),
             ('对齐校验', '区间不重叠、不越界、拼接无空洞；偏移可逆回原文', 'R D1 D3'),
         ]),
    dict(y=650, h=400, ch='②', title='SVG 拖拽', sub='坐标只改布局，不改语义', color=AMBER, fill=AMBER_L, ret=(2,'solid','没摆好就继续调整'),
         steps=[
             ('布局计算', '按“前提在下、结论在上”分层，给每个命题 (x, y)', 'R D3'),
             ('渲染 SVG', '命题=矩形仅序号；关系=圆点 + 有向边 + 标签', 'W D4'),
             ('命中测试', 'pointerdown 取最近节点，记录起点与当前缩放', 'R D4'),
             ('拖拽中', 'pointermove 改位移，rAF 节流；边路径实时重算', '内存'),
             ('提交坐标', 'pointerup 归一化后写回；触发重绘并记版本', 'W D4'),
         ]),
    dict(y=1090, h=400, ch='③', title='导图校验', sub='结构必须能被规则证明', color=PURP, fill=PURP_L, ret=(0,'dash','驳回：退回重标，重新收集'),
         steps=[
             ('收集图结构', '命题集合 + 关系集合（含嵌套参数 RelationArg）', 'R D3'),
             ('规则求值', '成员≥2 / 无环 / 类型匹配 / 同类互斥 / 两端存在', 'R D2'),
             ('违规定位', '每条违规产出 {relId, rule, 提示, 涉及节点}', 'W D5'),
             ('图示标红', '违规边与节点高亮，附提示气泡，可点击定位', 'W D4'),
             ('裁定 / 驳回', '通过则冻结版本；不通过退回标注员并写台账', 'W D3 D5'),
         ]),
]

for lane in LANES:
    y0, h = lane['y'], lane['h']
    d.rounded_rectangle((60, y0, 2340, y0 + h), radius=18, fill='white', outline=LINE, width=2)
    # 左侧标识
    d.rounded_rectangle((78, y0 + 20, 300, y0 + h - 20), radius=12, fill=lane['fill'], outline=lane['color'], width=2)
    d.text((189, y0 + 66), lane['ch'], font=F(40, True), fill=lane['color'], anchor='mm')
    d.text((189, y0 + 120), lane['title'], font=F(26, True), fill=lane['color'], anchor='mm')
    fsub = F(15)
    for i, ln in enumerate(wrap(d, lane['sub'], 190, 15)):
        d.text((189, y0 + 162 + i * 24), ln, font=fsub, fill=(120, 110, 100), anchor='ma')

    # 链路之间的衔接（上一条的输出即下一条的输入）
    if lane is not LANES[-1]:
        d.line([(189, y0 + h + 6), (189, y0 + h + 14)], fill=(170, 175, 166), width=2)
        for k in range(4):
            yy2 = y0 + h + 16 + k * 6
            d.line([(189, yy2), (189, yy2 + 4)], fill=(170, 175, 166), width=2)
        arrow(d, (189, y0 + h + 34), (189, y0 + h + 38), (170, 175, 166), 2)
    # 步骤框
    x = 336
    bw, gap, bh = 330, 58, 158
    by = y0 + (h - bh) / 2
    boxes = []
    for i, (t, s, st) in enumerate(lane['steps']):
        bx0 = x + i * (bw + gap)
        b = (bx0, by, bx0 + bw, by + bh)
        step(d, b, i + 1, t, s, lane['color'], lane['fill'], st)
        boxes.append(b)

    # 箭头
    for i in range(len(boxes) - 1):
        p0 = (boxes[i][2] + 6, by + bh / 2)
        p1 = (boxes[i + 1][0] - 6, by + bh / 2)
        arrow(d, p0, p1, lane['color'])

    # 回流箭头（不同链路回退到不同步骤，语义不同）
    ret_to, ret_style, ret_label = lane['ret']
    src, dst = boxes[4], boxes[ret_to]
    yy = by + bh + 26
    sx = src[0] + bw / 2
    dx = dst[0] + bw / 2
    if ret_style == 'solid':
        d.line([(sx, src[3]), (sx, yy)], fill=lane['color'], width=2)
        d.line([(sx, yy), (dx, yy)], fill=lane['color'], width=2)
        arrow(d, (dx, yy), (dx, dst[3] + 4), lane['color'], 2)
    else:
        # 虚线：驳回后回到起点
        for xx in range(int(dx), int(sx), 18):
            d.line([(xx, yy), (xx + 9, yy)], fill=lane['color'], width=2)
        d.line([(sx, src[3]), (sx, yy)], fill=lane['color'], width=2)
        arrow(d, (dx, yy), (dx, dst[3] + 4), lane['color'], 2)
    mid = (sx + dx) / 2
    fl = F(14)
    lw = tw(d, ret_label, fl) + 16
    d.rectangle((mid - lw / 2, yy - 12, mid + lw / 2, yy + 12), fill='white')
    d.text((mid, yy), ret_label, font=fl, fill=lane['color'], anchor='mm')

# 底部：数据契约
cy = 1520
d.rounded_rectangle((60, cy, 2340, cy + 210), radius=16, fill=CREAM, outline=LINE, width=2)
d.text((90, cy + 22), '三条链路的数据契约（最小字段）', font=F(22, True), fill=GREEN)

contracts = [
    (BLUE, '① 命题与偏移', ['{ "id": "P3", "seq": 3,', '  "charStart": 39, "charEnd": 82,', '  "label": "SF", "unit": "S3" }']),
    (AMBER, '② 节点与坐标', ['{ "propId": "P3", "x": 412, "y": 168,', '  "w": 76, "h": 34,', '  "draggedAt": "2026-11-10T10:02" }']),
    (PURP, '③ 校验与违规', ['{ "relId": "R4", "rule": "NO_CYCLE",', '  "path": ["P5","P4","P5"],', '  "hint": "组合关系不得成环" }']),
]
for i, (col, title, lines) in enumerate(contracts):
    cx = 90 + i * 756
    d.text((cx, cy + 62), title, font=F(17, True), fill=col)
    for k, ln in enumerate(lines):
        d.text((cx, cy + 94 + k * 26), ln, font=F(15), fill=(70, 80, 70))

d.line([(70, 1750), (2330, 1750)], fill=LINE, width=1)
d.text((70, 1762), '读图：三段链路串起来就是一次完整标注——先在原文上钉住偏移，再把命题摆成图，最后用规则证明这张图成立。',
       font=F(16), fill=(140, 140, 132))

img.save(OUT)
img.save(os.path.join(PROJ, '过程文件', '输出', 'dfd', 'dataflow-3chains.png'))
print('saved', OUT, img.size)
