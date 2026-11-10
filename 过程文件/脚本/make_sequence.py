# -*- coding: utf-8 -*-
"""Draw three UML sequence diagrams for the legal-argument annotation system.

Outputs (project 过程文件/输出/):
  seq-main.png     标注主流程的系统顺序图
  seq-relation.png 关系标注的详细顺序图（含图形化展示）
  seq-create.png   标注任务创建的详细顺序图
"""
from PIL import Image, ImageDraw, ImageFont
import os

PROJ = r'C:\Users\32354\Documents\deepseek-harness\default-workspace\法律论证标注系统'
OUT = os.path.join(PROJ, '过程文件', '输出')
FONT = r'C:\Windows\Fonts\msyh.ttc'
FONTB = r'C:\Windows\Fonts\msyhbd.ttc'

HEAD_H = 190
FOOT_H = 124
MSG_GAP = 34
TOP_PAD = 96
TITLE_H = 66
LEFT = 62
RIGHT = 62


def font(sz, bold=False):
    return ImageFont.truetype(FONTB if bold else FONT, sz)


def measure(text, sz, bold=False):
    f = font(sz, bold)
    bb = f.getbbox(text)
    return bb[2] - bb[0], bb[3] - bb[1]


class Seq:
    """A sequence diagram builder."""

    def __init__(self, title, actors, width=1760, wrap=26, wrap_alt=30):
        self.title = title
        self.actors = actors               # [(key, label, kind)] kind: 'user'|'sys'|'store'
        self.width = width
        n = len(actors)
        inner = width - LEFT - RIGHT
        step = inner / max(n - 1, 1) if n > 1 else 0
        self.x = {}
        for i, a in enumerate(actors):
            self.x[a[0]] = int(LEFT + i * step) if n > 1 else int(width / 2)
        self.msgs = []
        self.frags = []
        self.wrap = wrap
        self.wrap_alt = wrap_alt

    # ---------- content ----------
    def msg(self, src, dst, text, kind='sync', note=None, self_w=None):
        self.msgs.append({'type': 'msg', 'src': src, 'dst': dst, 'text': text,
                          'kind': kind, 'note': note, 'self_w': self_w})
        return self

    def frag(self, kind, cond, lines):
        """kind: 'loop' | 'alt' | 'opt'; lines: list of (src,dst,text,kind,note)"""
        self.msgs.append({'type': 'frag', 'kind': kind, 'cond': cond, 'lines': lines})
        return self

    def note(self, text, width=210):
        self.msgs.append({'type': 'note', 'text': text, 'width': width})
        return self

    def sep(self, label=''):
        self.msgs.append({'type': 'sep', 'label': label})
        return self

    # ---------- layout ----------
    def _frag_height(self, fr):
        h = 38                                    # header
        for ln in fr['lines']:
            h += self._line_height(ln) + 14
        return h + 16

    def _line_height(self, ln):
        src, dst, text, kind, note = (list(ln) + [None] * 5)[:5]
        nl = len(self._wrap_text(text))
        h = 18 + nl * 19 + 8
        if note:
            h += len(self._wrap_text(note, self.wrap_alt)) * 17 + 6
        return h

    def _wrap_text(self, text, wrap=None):
        wrap = wrap or self.wrap
        if not text:
            return ['']
        out, cur = [], ''
        for ch in text:
            cur += ch
            if len(cur) >= wrap and ch in '，。；、）】》」':
                out.append(cur); cur = ''
            elif len(cur) >= wrap + 6:
                out.append(cur); cur = ''
        if cur:
            out.append(cur)
        return out

    def layout(self):
        y = HEAD_H + TOP_PAD
        for m in self.msgs:
            if m['type'] == 'msg':
                m['y'] = y
                y += self._line_height((m['src'], m['dst'], m['text'], m['kind'], m['note']))
            elif m['type'] == 'frag':
                m['y'] = y
                h = self._frag_height(m)
                yy = y + 38
                for ln in m['lines']:
                    ln = list(ln) + [None] * 5
                    m.setdefault('ys', []).append(yy)
                    yy += self._line_height(ln) + 14
                m['h'] = h
                y += h + 14
            elif m['type'] == 'note':
                m['y'] = y
                y += len(self._wrap_text(m['text'], 34)) * 19 + 22
            elif m['type'] == 'sep':
                m['y'] = y
                y += 30
            else:
                m['y'] = y
                y += 22
        self.height = y + FOOT_H + 20
        return self

    # ---------- 激活条 ----------
    def _activation_bars(self):
        """按参与者计算活跃区间：收到调用激活，返回后结束；相邻区间小间隔自动合并成一条长条。

        返回 [{key, kind, y0, y1}, …]，已按“浅→深”排序，保证嵌套时后画的条向右错开。
        """
        KIND_ORDER = {'store': 0, 'sys': 1, 'user': 2}
        events = []
        for m in self.msgs:
            if m['type'] == 'msg':
                is_call = m['kind'] != 'return'
                events.append((m['y'], m['src'], is_call))
                events.append((m['y'] + 9, m['dst'], is_call))
            elif m['type'] == 'frag':
                for i, ln in enumerate(m['lines']):
                    ln = list(ln) + [None] * 5
                    k = ln[3] or 'sync'
                    y = m['ys'][i]
                    ic = k != 'return'
                    events.append((y + 1, ln[0], ic))
                    events.append((y + 9, ln[1], ic))
        events.sort(key=lambda e: e[0])

        open_seg = {}
        spans = {}

        def close(key, y):
            seg = open_seg.pop(key, None)
            if seg and y - seg[0] > 5:
                spans.setdefault(key, []).append((seg[0], y))

        for y, key, act in events:
            if act and key not in open_seg:
                open_seg[key] = (max(40, y - 9), y)
            elif not act and key in open_seg:
                close(key, y + 8)

        if self.msgs:
            last_y = max([m['y'] for m in self.msgs if m['type'] == 'msg'] or [200])
        else:
            last_y = 200
        for key in list(open_seg.keys()):
            close(key, last_y + 12)

        # 合并同一参与者的活跃区间：只合并"紧挨着"的（约等于同一段连续操作），
        # 留出空档，避免把中间并不活跃的区段也连成一条长条。
        MERGE_GAP = 8
        merged = {}
        for key, lst in spans.items():
            lst.sort()
            out = []
            for s, e in lst:
                if out and s - out[-1][1] <= MERGE_GAP:
                    out[-1][1] = max(out[-1][1], e)
                else:
                    out.append([s, e])
            merged[key] = out

        kind_of = {a[0]: a[2] for a in self.actors}
        bars = []
        for key, lst in merged.items():
            for s, e in lst:
                bars.append({'key': key, 'kind': kind_of.get(key, 'user'), 'y0': s, 'y1': e})
        bars.sort(key=lambda b: (KIND_ORDER.get(b['kind'], 1), b['key'], b['y0']))
        return bars

    # ---------- draw ----------
    def draw(self):
        W, H = self.width, self.height
        img = Image.new('RGB', (W, H), 'white')
        d = ImageDraw.Draw(img)

        # title
        d.text((LEFT, 16), self.title, font=font(25, True), fill='#12304d')
        d.line([(LEFT, TITLE_H - 12), (W - RIGHT, TITLE_H - 12)], fill='#c8d4e0', width=1)

        # actor boxes + lifelines
        for key, label, kind in self.actors:
            cx = self.x[key]
            tw, th = measure(label, 15, True)
            bw, bh = max(tw + 30, 104), 52
            x0, y0 = cx - bw / 2, 42
            fill = {'user': '#e8f0fb', 'sys': '#fdf1f1', 'store': '#eef7ee'}[kind]
            edge = {'user': '#5a7fb5', 'sys': '#c06a6a', 'store': '#3f8b61'}[kind]
            d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=9, fill=fill, outline=edge, width=2)
            d.text((cx - tw / 2, y0 + (bh - th) / 2 - 2), label, font=font(15, True), fill='#16273a')
            d.line([(cx, y0 + bh), (cx, H - FOOT_H + 22)], fill='#b9c6d4', width=1)
            d.line([(cx - 5, y0 + bh), (cx, y0 + bh + 8)], fill='#b9c6d4', width=1)
            d.line([(cx + 5, y0 + bh), (cx, y0 + bh + 8)], fill='#b9c6d4', width=1)
            # footer box
            d.rounded_rectangle([x0, H - FOOT_H + 22, x0 + bw, H - FOOT_H + 74], radius=9,
                                fill=fill, outline=edge, width=2)
            d.text((cx - tw / 2, H - FOOT_H + 22 + (bh - th) / 2 - 2), label, font=font(15, True), fill='#16273a')

        # 激活条：把每个参与者的活跃区间画成醒目的填充长条（生命线画虚线，长条压在上面）
        bar_off = {'user': 0, 'sys': 0, 'store': 0}
        for seg in self._activation_bars():
            cx = self.x[seg['key']]
            off = bar_off.get(seg['kind'], 0)
            hw = 10.5
            x0 = cx - hw + off
            x1 = cx + hw + off
            y0, y1 = seg['y0'], seg['y1']
            d.rounded_rectangle([x0 + 2, y0 + 2, x1 + 2, y1 + 3], radius=4, fill='#dce3ea')
            d.rounded_rectangle([x0, y0, x1, y1], radius=4, fill='#f6c96a', outline='#b07a1e', width=2)
            d.line([(x0 + 1, y0 + 1), (x0 + 1, y1 - 1)], fill='#e0a800', width=1)

        # pass 1: 分隔线（先画，避免盖住消息文字）
        for m in self.msgs:
            if m['type'] == 'sep':
                y = m['y'] - 14
                lab = m.get('label') or ''
                d.line([(LEFT, y), (W - RIGHT, y)], fill='#dfe6ee', width=2)
                if lab:
                    tw, th = measure(lab, 14, True)
                    d.rectangle([LEFT + 6, y - 12, LEFT + 6 + tw + 20, y + 12], fill='#eff4f9', outline='#c8d4e0')
                    d.text((LEFT + 16, y - th / 2 - 2), lab, font=font(14, True), fill='#3d5064')
        # pass 2: 消息、片段、注释
        active = {}
        for m in self.msgs:
            if m['type'] == 'sep':
                continue
            if m['type'] == 'note':
                y = m['y']
                lines = self._wrap_text(m['text'], 34)
                w = m['width']
                h = len(lines) * 19 + 14
                x = W - RIGHT - w - 10
                d.rounded_rectangle([x, y, x + w, y + h], radius=6, fill='#fdf6e3', outline='#d8bf7a', width=1)
                d.polygon([(x + 16, y + h), (x + 28, y + h), (x + 20, y + h + 10)], fill='#fdf6e3', outline='#d8bf7a')
                for i, ln in enumerate(lines):
                    d.text((x + 9, y + 7 + i * 19), ln, font=font(13), fill='#5c4a00')
                continue
            if m['type'] == 'frag':
                self._draw_frag(d, m)
                continue
            self._draw_msg(d, m, active)
        return img

    def _draw_msg(self, d, m, active, dy=0, x0=None, x1=None):
        src, dst, text, kind, note = m['src'], m['dst'], m['text'], m['kind'], m['note']
        y = m['y'] + dy
        xs, xd = self.x[src], self.x[dst]
        W_SAFE = self.width - RIGHT - 8
        color = {'sync': '#2f4f6f', 'return': '#4b8b4b', 'self': '#8a6d00',
                 'async': '#2f6f8f', 'data': '#7a5c9a', 'graph': '#c06a6a'}.get(kind, '#2f4f6f')
        dash = (kind == 'return')

        if kind == 'self' or src == dst:
            w = m.get('self_w') or 44
            d.line([(xs, y), (xs + w, y)], fill=color, width=2)
            d.line([(xs + w, y), (xs + w, y + 22)], fill=color, width=2)
            arrow(d, xs + w, y + 22, xs + 8, y + 22, color, 2, dashed=dash)
            tx = xs + w + 12
            maxw = W_SAFE - tx
        else:
            arrow(d, xs, y, xd, y, color, 2, dashed=dash)
            tx = min(xs, xd) + 12
            maxw = W_SAFE - tx
        # label
        is_self = (kind == 'self' or src == dst)
        lines = self._wrap_text(text, 18) if is_self else self._wrap_text(text)
        for i, ln in enumerate(lines):
            d.text((tx, y - 20 + i * 19), ln, font=font(14.5, True if kind == 'graph' else False),
                   fill='#16273a' if kind != 'graph' else '#8a3b3b')
        if note:
            nl = self._wrap_text(note, self.wrap_alt)
            for i, ln in enumerate(nl):
                d.text((tx, y + 3 + i * 17), '· ' + ln, font=font(12.5), fill='#6b7784')

    def _draw_frag(self, d, m):
        y, h = m['y'], m['h']
        xs = [self.x[a[0]] for a in self.actors]
        x0, x1 = min(xs) - 46, max(xs) + 46
        d.rounded_rectangle([x0, y, x1, y + h], radius=8, outline='#7a8ca0', width=2)
        # tag
        tag = {'loop': 'loop', 'alt': 'alt', 'opt': 'opt'}[m['kind']]
        tw, th = measure(tag, 13.5, True)
        d.polygon([(x0, y), (x0 + tw + 26, y), (x0 + tw + 16, y + 24), (x0, y + 24)],
                  fill='#eef2f7', outline='#7a8ca0')
        d.text((x0 + 11, y + 5), tag, font=font(13.5, True), fill='#33478a')
        cw, ch = measure(m['cond'], 14)
        cond_x = x0 + tw + 34
        d.rectangle([cond_x, y + 3, cond_x + cw + 16, y + 25], fill='#f7fafd', outline='#c8d4e0')
        d.text((cond_x + 8, y + 5), m['cond'], font=font(14), fill='#33478a')
        for i, ln in enumerate(m['lines']):
            ln = list(ln) + [None] * 5
            sub = {'src': ln[0], 'dst': ln[1], 'text': ln[2], 'kind': ln[3] or 'sync',
                   'note': ln[4], 'y': m['ys'][i]}
            self._draw_msg(d, sub, {}, dy=0)


def arrow(d, x1, y1, x2, y2, color, width=2, dashed=False, head=True, double=False):
    if dashed:
        import math
        dist = math.hypot(x2 - x1, y2 - y1)
        n = max(int(dist // 10), 1)
        for i in range(n):
            if i % 2 == 0:
                t0, t1 = i / n, (i + 0.55) / n
                d.line([(x1 + (x2 - x1) * t0, y1 + (y2 - y1) * t0),
                        (x1 + (x2 - x1) * t1, y1 + (y2 - y1) * t1)], fill=color, width=width)
    else:
        d.line([(x1, y1), (x2, y2)], fill=color, width=width)
    if head:
        import math
        ang = math.atan2(y2 - y1, x2 - x1)
        L = 11
        for da in (math.radians(152), math.radians(-152)):
            d.line([(x2, y2), (x2 + L * math.cos(ang + da), y2 + L * math.sin(ang + da))],
                   fill=color, width=width)
    if double:
        import math
        ang = math.atan2(y2 - y1, x2 - x1)
        L = 11
        for da in (math.radians(28), math.radians(-28)):
            d.line([(x1, y1), (x1 + L * math.cos(ang + da), y1 + L * math.sin(ang + da))],
                   fill=color, width=width)


# ============================================================
# 图 1：标注主流程的系统顺序图
# ============================================================
def build_main():
    A = [('TC', '任务创建者', 'user'), ('SYS', '系统', 'sys'), ('AN', '标注员', 'user'),
         ('AD', '裁定者', 'user'), ('DB', '版本库', 'store')]
    s = Seq('图 1　标注主流程的系统顺序图', A)
    s.sep('阶段一　创建标注任务')
    s.msg('TC', 'SYS', '登录并进入“标注任务管理”')
    s.msg('TC', 'SYS', '新建任务：任务名、案例类型（原始判决书 / 指导性案例 / 参考案例）')
    s.msg('TC', 'SYS', '上传裁判文书（PDF / Word / 纯文本），系统智能提取“裁判理由”')
    s.msg('TC', 'SYS', '确认识别出的标注范围与案例信息')
    s.msg('SYS', 'TC', '返回任务摘要：标注范围 char 区间、文书数、待分配人数')
    s.msg('TC', 'SYS', '引用指南版本 v1.2，冻结标签集 LS-v1.2', kind='data')
    s.msg('TC', 'SYS', '分配标注员（≥2 人独立标注）并指定裁定者')
    s.msg('SYS', 'DB', '写入任务、文书、分配关系、指南与标签版本绑定', kind='data')
    s.sep('阶段二　独立标注')
    s.msg('SYS', 'AN', '通知待标注任务（标注员点“下一条”领取）', kind='async')
    s.frag('loop', '对每一份已分配的文书（每个标注员独立执行一遍）', [
        ('AN', 'SYS', '① 颗粒度切割：按句号切分、按逗号/分号考察子句并合并同性质子句'),
        ('AN', 'SYS', '② 要素标注：选段 → 分配序号 → 选择一级/二级标签（SF/GF/SM/GM 及子类型）', 'graph'),
        ('AN', 'SYS', '③ 关系标注：在图上建立 S/A/J/M/I，支持嵌套与多对一', 'graph'),
        ('AN', 'SYS', '④ 图示确认：拖动节点、缩放查看，核对图示与规则一致', 'graph'),
        ('SYS', 'DB', '保存该标注员的版本（命题、标签、关系、坐标）', 'data'),
    ])
    s.msg('SYS', 'SYS', '计算两版颗粒度差异率；>10% 退回重新切割', kind='self')
    s.sep('阶段三　冲突解决')
    s.msg('SYS', 'AD', '汇总同一文书的多个标注版本，列出差异（标签 / 关系 / 边界）', kind='async')
    s.frag('opt', '存在差异项', [
        ('AD', 'SYS', '逐条人工比对：采纳某一方 / 取并集 / 直接重标'),
        ('AD', 'SYS', '填写裁定理由（可引用指南条目）'),
        ('SYS', 'SYS', '一致项自动通过，进入最终库', 'self'),
        ('AD', 'SYS', '涉及核心概念分歧 → 登记疑难问题台账，提交专家线下讨论后线上确认'),
    ])
    s.msg('SYS', 'DB', '写入最终版本与裁定记录（裁定人、理由、时间）', kind='data')
    s.sep('阶段四　结果输出')
    s.msg('TC', 'SYS', '选择导出内容（JSON / Excel / 图示）与文件名')
    s.msg('SYS', 'DB', '读取最终版本，生成导出包并写入下载记录', kind='data')
    s.msg('SYS', 'TC', '返回压缩包下载；导出后数据置为只读', kind='return')
    s.note('阶段顺序不可逆：进入结果输出后如需重标，必须新建任务。', 260)
    return s.layout().draw()


# ============================================================
# 图 2：关系标注的详细顺序图（重点：图形化展示）
# ============================================================
def build_relation():
    A = [('AN', '标注员', 'user'), ('UI', '标注界面', 'user'), ('SYS', '关系服务', 'sys'),
         ('RV', '规则校验器', 'sys'), ('VZ', '图示渲染器', 'sys'), ('DB', '版本库', 'store')]
    s = Seq('图 2　关系标注的详细顺序图（含关系“图形化展示”）', A, width=1860, wrap=22, wrap_alt=24)
    s.sep('① 进入关系标注')
    s.msg('AN', 'UI', '进入“③ 关系标注”步骤（颗粒度与要素标注已完成）')
    s.msg('UI', 'SYS', '请求命题清单与坐标系')
    s.msg('SYS', 'UI', '返回命题列表（含论证单元 A1/A2/A3）', kind='return')
    s.msg('UI', 'VZ', '按论证单元分区渲染：命题＝矩形（框内仅写序号）', kind='graph')
    s.msg('VZ', 'UI', '输出空白关系图与可用关系类型提示', kind='graph')
    s.sep('② 建立关系（在图上拖动图元）')
    s.msg('AN', 'UI', '点击起点图元，再点击终点图元（节点可为命题或已有关系）', kind='graph')
    s.msg('UI', 'VZ', '高亮选中节点、绘制临时连线', kind='graph')
    s.msg('AN', 'UI', '选择关系类型：S 支持 / A 反对 / J 组合 / M 匹配 / I 同一')
    s.msg('UI', 'SYS', '提交关系（类型 + 参数列表，参数支持嵌套）', kind='sync')
    s.msg('SYS', 'RV', '校验：组合成员≥2、匹配双方个别↔一般、无环、无重复', kind='sync')
    s.frag('alt', '校验不通过', [
        ('RV', 'SYS', '返回违规项与指南依据（如 5.3.3 组合关系不得拆为独立支持）', 'return'),
        ('SYS', 'UI', '阻止保存并在图上标红该连线', 'graph'),
    ])
    s.msg('SYS', 'DB', '写入关系记录：编号、类型、参数、形式化表达、父关系、论证单元', kind='data')
    s.sep('③ 图形化展示（关系→图元的映射在本步产生）')
    s.msg('SYS', 'VZ', '提交关系结构，请求重绘', kind='graph')
    s.msg('VZ', 'VZ', '计算图元与坐标：关系节点置于连线中点；嵌套关系自内而外逐层构造', kind='self')
    s.msg('VZ', 'SYS', '生成形式化表达 S(M(J(P4,P5),P2),P6) 并回写界面', kind='return')
    s.msg('VZ', 'UI', '按规范图元绘制并输出 SVG：', kind='graph')
    s.frag('loop', '对每一条关系按类型选择图元', [
        ('VZ', 'UI', '支持 S：实心圆 ● + 有向边（支持者 → 被支持命题）', 'graph'),
        ('VZ', 'UI', '反对 A：空心圆 ○ + 有向边（反对者 → 被反对者）', 'graph'),
        ('VZ', 'UI', '组合 J / 匹配 M：带“+”圆节点；J 用无向连线，M 用有向边（匹配者→被匹配者）', 'graph'),
        ('VZ', 'UI', '同一 I：矩形框内以“/”分隔同类命题', 'graph'),
    ])
    s.msg('VZ', 'UI', '命题节点不显示命题类型（类型只存在于标注表与数据库）', kind='graph')
    s.sep('④ 图示交互与双向联动')
    s.msg('AN', 'UI', '拖动方框调整布局 / 滚轮缩放 / 平移查看大图', kind='graph')
    s.msg('UI', 'VZ', '提交节点坐标变化', kind='graph')
    s.msg('VZ', 'SYS', '坐标写回关系数据（图示区调整 → 标注数据同步）', kind='sync')
    s.msg('SYS', 'DB', '保存布局与节点坐标', kind='data')
    s.msg('AN', 'UI', '切换论证单元分图查看（一份文书含多个独立论证结构）', kind='graph')
    s.sep('⑤ 导出与确认')
    s.msg('UI', 'VZ', '请求导出图示（PNG / JPG / SVG）', kind='graph')
    s.msg('VZ', 'UI', '返回图示文件（矢量为 SVG）', kind='return')
    s.msg('AN', 'UI', '提交关系版本')
    s.msg('UI', 'SYS', '锁定该版本，进入裁定阶段')
    s.note('图形化展示的三条硬规则：① 命题＝矩形只写序号；② 关系＝圆形节点（实心/空心/带“+”）；'
           '③ 嵌套结构自内而外逐层构造，括号层级与逻辑层级一致。', 300)
    return s.layout().draw()


# ============================================================
# 图 3：标注任务创建的详细顺序图
# ============================================================
def build_create():
    A = [('TC', '任务创建者', 'user'), ('UI', '任务管理界面', 'user'), ('SYS', '任务服务', 'sys'),
         ('EX', '文书解析器', 'sys'), ('GL', '指南与标签库', 'store'), ('DB', '任务库', 'store'),
         ('AN', '标注员', 'user')]
    s = Seq('图 3　标注任务创建的详细顺序图', A, width=1900, wrap=22, wrap_alt=26)
    s.sep('① 新建任务与文书导入')
    s.msg('TC', 'UI', '登录（特权用户）→ 点击“新建标注任务”')
    s.msg('UI', 'SYS', '提交任务基本信息：任务名、案例类型、文书数、标注份数/份')
    s.msg('SYS', 'SYS', '校验角色权限（是否具备“创建任务/分配任务”特权）', kind='self')
    s.msg('SYS', 'UI', '创建任务草稿，返回导入入口', kind='return')
    s.msg('TC', 'UI', '上传裁判文书：PDF / Word / 纯文本（可批量上传）')
    s.msg('UI', 'EX', '提交文件与格式信息')
    s.msg('EX', 'EX', '提取正文，按“本院认为”“判决如下”定位裁判理由', kind='self')
    s.msg('EX', 'UI', '返回提取结果：正文、理由区间 char 区间、命中锚点', kind='return')
    s.sep('② 标注范围与案例信息确认（人工校正）')
    s.msg('TC', 'UI', '校正标注范围（例如排除“综上所述，依照……判决如下：”）')
    s.msg('UI', 'SYS', '提交范围 char 起止')
    s.msg('SYS', 'SYS', '校验：范围合法且落在正文内、不越界', kind='self')
    s.msg('SYS', 'UI', '锁定标注范围，用于后续所有命题的字符索引', kind='return')
    s.msg('TC', 'UI', '填写案例信息（案号 / 裁判法院 / 法院层级 / 审级 / 裁判日期 / 案件性质 / 案由 / 裁判结果类型）')
    s.msg('UI', 'SYS', '保存案例信息')
    s.msg('SYS', 'UI', '必填项校验；缺失则阻止进入下一步并逐项提示', kind='return')
    s.sep('③ 指南与标签版本冻结')
    s.msg('TC', 'UI', '打开指南版本库，选择并冻结指南版本 v1.2')
    s.msg('UI', 'GL', '查询该版本的标签体系与关系类型', kind='sync')
    s.msg('GL', 'SYS', '返回标签 13 个（SF/GF/SM/GM 及子类型、SM-C、IS/Non）与关系 5 种（S/A/J/M/I）', kind='return')
    s.msg('SYS', 'DB', '冻结为标签集 LS-v1.2，与任务绑定（任务期内不可增删改）', kind='data')
    s.sep('④ 分配标注员与裁定者')
    s.msg('TC', 'UI', '选择标注员（≥2 人独立标注）与裁定者（可指定多人或后续分配）')
    s.msg('UI', 'SYS', '提交分配：文书 ↔ 标注员 多对多；指定裁定者')
    s.msg('SYS', 'SYS', '校验：标注员权限、是否重复分配、裁定者是否具备裁定角色', kind='self')
    s.msg('SYS', 'DB', '生成每位标注员的独立标注任务，写入任务库与分配关系', kind='data')
    s.msg('SYS', 'UI', '返回任务清单与分配结果（可再次分配给新增标注员）', kind='return')
    s.sep('⑤ 任务生效与通知')
    s.msg('TC', 'UI', '确认创建任务（可设置截止时间）')
    s.msg('UI', 'SYS', '提交创建确认')
    s.msg('SYS', 'DB', '任务状态置为“已创建”，写入操作日志', kind='data')
    s.msg('SYS', 'AN', '通知标注员（点“下一条”领取任务，无需自己上传）', kind='async')
    s.msg('AN', 'SYS', '领取任务，文书置为“标注中”', kind='sync')
    s.note('任务创建完成后：标签体系与关系类型冻结（需求 Q3）；人员可增加、数据可增加（Q1/Q2）；'
           '如需改标签必须新建任务版本。', 300)
    return s.layout().draw()


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for name, fn in (('seq-main.png', build_main), ('seq-relation.png', build_relation),
                     ('seq-create.png', build_create)):
        img = fn()
        p = os.path.join(OUT, name)
        img.save(p)
        print('saved', name, img.size)
