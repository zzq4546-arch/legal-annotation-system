# -*- coding: utf-8 -*-
"""Pure-stdlib PDF text extractor tuned for Type0/Identity-H Chinese PDFs.

Improvements over pdfx.py:
  * full-ish content-stream tokenizer (names, numbers, strings, hex strings, arrays, dicts)
  * text rendering mode tracking -> skip invisible text (3 Tr, watermark)
  * Td/TD/T*/Tm driven line grouping, sorted by y then x
"""
import re, sys, zlib

SRC = sys.argv[1]
DST = sys.argv[2]

data = open(SRC, 'rb').read()
objs = {}
for m in re.finditer(rb'(\d+)\s+(\d+)\s+obj\b', data):
    e = data.find(b'endobj', m.end())
    objs[int(m.group(1))] = data[m.end():e]


def raw_stream(body):
    m = re.search(rb'stream\r\n|stream\n|stream\r', body)
    if not m:
        return None
    s = m.end()
    e = body.find(b'endstream', s)
    return body[s:e]


def decoded_stream(body):
    r = raw_stream(body)
    if r is None:
        return None
    head = body[:body.find(b'stream')]
    for _ in range(3):
        if b'FlateDecode' in head:
            try:
                r = zlib.decompress(r)
            except Exception:
                try:
                    r = zlib.decompressobj().decompress(r)
                except Exception:
                    return None
            head = head.replace(b'FlateDecode', b'', 1)
        else:
            break
    return r


def parse_tounicode(b):
    txt = b.decode('latin-1', 'replace')
    mp = {}
    for blk in re.findall(r'beginbfchar(.*?)endbfchar', txt, re.S):
        for a, d in re.findall(r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', blk):
            try:
                mp[int(a, 16)] = bytes.fromhex(d).decode('utf-16-be', 'replace')
            except Exception:
                pass
    for blk in re.findall(r'beginbfrange(.*?)endbfrange', txt, re.S):
        for lo, hi, dst in re.findall(r'<([0-9A-Fa-f]{2,})>\s*<([0-9A-Fa-f]{2,})>\s*<([0-9A-Fa-f]{2,})>', blk):
            a, z, base = int(lo, 16), int(hi, 16), int(dst, 16)
            if z - a > 65535:
                continue
            for i in range(z - a + 1):
                mp[a + i] = chr(base + i)
        for lo, hi, arr in re.findall(r'<([0-9A-Fa-f]{2,})>\s*<([0-9A-Fa-f]{2,})>\s*\[(.*?)\]', blk, re.S):
            a = int(lo, 16)
            for k, it in enumerate(re.findall(r'<([0-9A-Fa-f]+)>', arr)):
                try:
                    mp[a + k] = bytes.fromhex(it).decode('utf-16-be', 'replace')
                except Exception:
                    pass
    return mp


font_map = {}       # font obj num -> cid->str
for n, body in objs.items():
    if b'/Font' in body and b'/ToUnicode' in body:
        m = re.search(rb'/ToUnicode\s+(\d+)\s+0\s+R', body)
        if m and int(m.group(1)) in objs:
            s = decoded_stream(objs[int(m.group(1))])
            if s:
                font_map[n] = parse_tounicode(s)

if __import__('os').environ.get('PDFX_DEBUG'):
    import json
    print('font_map sizes:', {k: len(v) for k, v in font_map.items()}, file=sys.stderr)
    fm = font_map.get(14) or {}
    print('fm14 sample:', [(hex(k), v) for k, v in list(fm.items())[:6]], file=sys.stderr)
    print('lookup 0x07A3 ->', repr(fm.get(0x07A3)), '0x4B5E ->', repr(fm.get(0x4B5E)), file=sys.stderr)

pages = []
def walk(num, seen=set()):
    if num in seen:
        return
    seen.add(num)
    body = objs.get(num, b'')
    if re.search(rb'/Type\s*/Pages', body):
        kids = re.search(rb'/Kids\s*\[(.*?)\]', body, re.S)
        if kids:
            for k in re.findall(rb'(\d+)\s+0\s+R', kids.group(1)):
                walk(int(k), seen)
    elif re.search(rb'/Type\s*/Page\b', body):
        pages.append(num)

root = None
for n, body in objs.items():
    if re.search(rb'/Type\s*/Catalog', body):
        m = re.search(rb'/Pages\s+(\d+)\s+0\s+R', body)
        if m:
            root = int(m.group(1))
walk(root)

# ---------- content stream tokenizer ----------
TOKEN = re.compile(rb'''
    (?P<ws>\s+)
  | (?P<comment>%[^\r\n]*)
  | (?P<name>/[^\s/\[\]<>(){}%]*)
  | (?P<hexstr><[0-9A-Fa-f\s]*>)
  | (?P<litstr>\((?:\\.|[^\\()])*\))
  | (?P<arrayopen>\[)
  | (?P<arrayclose>\])
  | (?P<dictopen><<)
  | (?P<dictclose>>>)
  | (?P<num>[-+]?(?:\d+\.\d*|\.\d+|\d+))
  | (?P<op>[A-Za-z'"*][A-Za-z0-9'"*]*)
''', re.X | re.S)


def tokenize(buf):
    pos = 0
    n = len(buf)
    while pos < n:
        m = TOKEN.match(buf, pos)
        if not m:
            pos += 1
            continue
        pos = m.end()
        kind = m.lastgroup
        if kind in ('ws', 'comment'):
            continue
        yield kind, m.group(0)


def unescape_lit(raw):
    body = raw[1:-1]
    out = bytearray()
    i = 0
    while i < len(body):
        c = body[i]
        if c == 0x5C:  # backslash
            i += 1
            if i >= len(body):
                break
            d = body[i]
            mp = {0x6E: 10, 0x72: 13, 0x74: 9, 0x62: 8, 0x66: 12,
                  0x28: 0x28, 0x29: 0x29, 0x5C: 0x5C}
            if d in mp:
                out.append(mp[d]); i += 1
            elif 0x30 <= d <= 0x37:
                oct_digits = ''
                while i < len(body) and len(oct_digits) < 3 and 0x30 <= body[i] <= 0x37:
                    oct_digits += chr(body[i]); i += 1
                out.append(int(oct_digits, 8) & 0xFF)
            else:
                out.append(d); i += 1
        else:
            out.append(c); i += 1
    return bytes(out)


def decode_show(bytes_or_hex, fmap, is_hex, nbytes=2):
    if fmap is None:
        return ''
    if is_hex:
        h = re.sub(rb'\s', b'', bytes_or_hex)
        step = nbytes * 2
        codes = [int(h[i:i+step], 16) for i in range(0, len(h) - step + 1, step)]
    else:
        b = bytes_or_hex
        codes = [int.from_bytes(b[i:i+nbytes], 'big') for i in range(0, len(b) - nbytes + 1, nbytes)]
    return ''.join(fmap.get(c, '') for c in codes)


def page_lines(pnum):
    body = objs[pnum]
    fonts = {}
    m = re.search(rb'/Font\s*<<(.*?)>>', body, re.S)
    if m:
        for nm, fn in re.findall(rb'/([^\s/]+)\s+(\d+)\s+0\s+R', m.group(1)):
            fonts[nm.decode('latin-1')] = int(fn)
    cnums = []
    m = re.search(rb'/Contents\s+(\d+)\s+0\s+R', body)
    if m:
        cnums = [int(m.group(1))]
    else:
        m = re.search(rb'/Contents\s*\[(.*?)\]', body, re.S)
        if m:
            cnums = [int(x) for x in re.findall(rb'(\d+)\s+0\s+R', m.group(1))]
    content = b''
    for cn in cnums:
        s = decoded_stream(objs.get(cn, b''))
        if s:
            content += s + b'\n'

    items = []          # (y, x, text)
    buf = []            # pending operands
    fmap = None
    leading = 0.0
    tm = [1, 0, 0, 1, 0, 0]
    tlm = list(tm)
    trise = 3
    render_mode = 0
    cur_y = cur_x = 0.0

    def show(txt):
        if txt and render_mode != 3 and render_mode != 7:
            items.append((round(cur_y, 1), round(cur_x, 1), txt))

    for kind, tok in tokenize(content):
        if kind == 'op':
            op = tok.decode('latin-1')
            try:
                if op == 'BT':
                    tm = [1, 0, 0, 1, 0, 0]; tlm = list(tm)
                elif op == 'Tf':
                    if len(buf) >= 2 and buf[-2][0] == 'name':
                        fname = buf[-2][1][1:].decode('latin-1')
                        fmap = font_map.get(fonts.get(fname, -1))
                elif op == 'TL':
                    leading = float(buf[-1][1])
                elif op == 'Tm':
                    v = [float(x[1]) for x in buf[-6:]]
                    tm = v; tlm = list(v)
                elif op in ('Td', 'TD'):
                    tx, ty = float(buf[-2][1]), float(buf[-1][1])
                    if op == 'TD':
                        leading = -ty
                    tlm = [tlm[0], tlm[1], tlm[2], tlm[3], tlm[4] + tx * tlm[0] + ty * tlm[2],
                           tlm[5] + tx * tlm[1] + ty * tlm[3]]
                    tm = list(tlm)
                elif op == 'T*':
                    tlm = [tlm[0], tlm[1], tlm[2], tlm[3], tlm[4] - leading * tlm[2],
                           tlm[5] - leading * tlm[3]]
                    tm = list(tlm)
                elif op == 'Tr':
                    render_mode = int(float(buf[-1][1]))
                elif op == 'Ts':
                    trise = float(buf[-1][1])
                elif op == 'Tj':
                    if buf and buf[-1][0] == 'litstr':
                        show(decode_show(unescape_lit(buf[-1][1]), fmap, False))
                    elif buf and buf[-1][0] == 'hexstr':
                        show(decode_show(buf[-1][1][1:-1], fmap, True))
                elif op == "'":
                    tlm = [tlm[0], tlm[1], tlm[2], tlm[3], tlm[4] - leading * tlm[2],
                           tlm[5] - leading * tlm[3]]
                    tm = list(tlm)
                    if buf and buf[-1][0] in ('litstr', 'hexstr'):
                        ish = buf[-1][0] == 'hexstr'
                        raw = buf[-1][1][1:-1] if ish else unescape_lit(buf[-1][1])
                        show(decode_show(raw, fmap, ish))
                elif op == 'TJ':
                    arr = next((x for x in reversed(buf) if x[0] == 'array'), None)
                    if arr:
                        parts = []
                        for k, t in arr[1]:
                            if t[0] == 'hexstr':
                                parts.append(decode_show(t[1][1:-1], fmap, True))
                            elif t[0] == 'litstr':
                                parts.append(decode_show(unescape_lit(t[1]), fmap, False))
                        show(''.join(parts))
                cur_x = tm[4] + (tm[2] * trise)
                cur_y = tm[5] + (tm[3] * trise)
            except Exception:
                pass
            buf = []
        elif kind == 'arrayopen':
            buf.append(('array', []))
        elif kind == 'arrayclose':
            pass
        else:
            if buf and buf[-1][0] == 'array' and kind in ('hexstr', 'litstr', 'num'):
                buf[-1][1].append((kind, tok))
            else:
                buf.append((kind, tok))
            if len(buf) > 24:
                buf = buf[-24:]

    # page uses a flipped CTM (1 0 0 -1 0 H cm), so larger y = higher on the page
    items.sort(key=lambda t: (-t[0], t[1]))
    lines = []
    for y, x, txt in items:
        if lines and abs(lines[-1][0] - y) <= 1.5:
            lines[-1][2].append((x, txt))
        else:
            lines.append([y, y, [(x, txt)]])
    lines.reverse()
    out = []
    for _, _, cells in lines:
        cells.sort(key=lambda c: c[0])
        s = ''
        prev_x = None
        for x, txt in cells:
            if prev_x is not None and x - prev_x > 12 and not s.endswith(' '):
                s += ' '
            s += txt
            prev_x = x + len(txt) * 3
        out.append(s)
    return out


all_out = []
for i, p in enumerate(pages, 1):
    ls = page_lines(p)
    all_out.append(f'[[[PAGE {i}]]]\n' + '\n'.join(ls))
    print(f"page {i}: {len(ls)} lines, {sum(len(l) for l in ls)} chars")

with open(DST, 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(all_out))
print('pages:', len(pages), 'chars:', sum(len(t) for t in all_out))
