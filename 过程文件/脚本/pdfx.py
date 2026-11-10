# -*- coding: utf-8 -*-
"""Minimal pure-stdlib PDF text extractor for Type0/Identity-H Chinese PDFs."""
import re, sys, zlib

path = sys.argv[1]

data = open(path, 'rb').read()

objs = {}
for m in re.finditer(rb'(\d+)\s+(\d+)\s+obj\b', data):
    num = int(m.group(1))
    e = data.find(b'endobj', m.end())
    objs[num] = data[m.end():e]


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
    if b'FlateDecode' in body[:body.find(b'stream')]:
        try:
            return zlib.decompress(r)
        except Exception:
            try:
                return zlib.decompressobj().decompress(r)
            except Exception:
                return None
    return r


def parse_tounicode(cmap_bytes):
    txt = cmap_bytes.decode('latin-1', 'replace')
    mapping = {}
    for blk in re.findall(r'beginbfchar(.*?)endbfchar', txt, re.S):
        for a, b in re.findall(r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', blk):
            try:
                mapping[int(a, 16)] = bytes.fromhex(b).decode('utf-16-be', 'replace')
            except Exception:
                pass
    for blk in re.findall(r'beginbfrange(.*?)endbfrange', txt, re.S):
        # lo hi <dst>
        for lo, hi, dst in re.findall(r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', blk):
            lo_i, hi_i = int(lo, 16), int(hi, 16)
            base = int(dst, 16)
            for i in range(min(hi_i - lo_i + 1, 65536)):
                try:
                    mapping[lo_i + i] = chr(base + i)
                except Exception:
                    pass
        # lo hi [ <d1> <d2> ... ]
        for lo, hi, arr in re.findall(r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*\[(.*?)\]', blk, re.S):
            lo_i = int(lo, 16)
            items = re.findall(r'<([0-9A-Fa-f]+)>', arr)
            for k, it in enumerate(items):
                try:
                    mapping[lo_i + k] = bytes.fromhex(it).decode('utf-16-be', 'replace')
                except Exception:
                    pass
    return mapping


# build font -> tounicode map
font_maps = {}
for n, body in objs.items():
    if b'/ToUnicode' in body and b'/Type' in body and b'/Font' in body:
        m = re.search(rb'/ToUnicode\s+(\d+)\s+0\s+R', body)
        if not m:
            continue
        cmap_obj = int(m.group(1))
        if cmap_obj in objs:
            s = decoded_stream(objs[cmap_obj])
            if s:
                font_maps[n] = parse_tounicode(s)

print("fonts with tounicode:", {k: len(v) for k, v in font_maps.items()}, file=sys.stderr)

# page order from page tree
pages = []
def walk(num):
    body = objs.get(num, b'')
    if b'/Type' in body and b'/Pages' in body:
        kids = re.search(rb'/Kids\s*\[(.*?)\]', body, re.S)
        if kids:
            for k in re.findall(rb'(\d+)\s+0\s+R', kids.group(1)):
                walk(int(k))
    elif b'/Type' in body and b'/Page' in body:
        pages.append(num)

walk(2)
print("pages:", len(pages), pages, file=sys.stderr)


def decode_string(hexstr, fmap):
    if fmap:
        out = []
        for i in range(0, len(hexstr) - 1, 2):
            code = int(hexstr[i:i+2], 16)
            out.append(fmap.get(code, ''))
        return ''.join(out)
    return ''


def extract_page(pnum):
    body = objs[pnum]
    fonts = {}
    res = re.search(rb'/Font\s*<<(.*?)>>', body, re.S)
    if res:
        for name, fnum in re.findall(rb'/(\w+)\s+(\d+)\s+0\s+R', res.group(1)):
            fonts[name.decode()] = int(fnum)
    cm = re.search(rb'/Contents\s+(\d+)\s+0\s+R', body)
    if not cm:
        arr = re.search(rb'/Contents\s*\[(.*?)\]', body, re.S)
        nums = [int(x) for x in re.findall(rb'(\d+)\s+0\s+R', arr.group(1))] if arr else []
    else:
        nums = [int(cm.group(1))]
    content = b''.join(decoded_stream(objs[n]) or b'' for n in nums if n in objs)
    return content, fonts


def page_text(pnum):
    content, fonts = extract_page(pnum)
    txt = content.decode('latin-1', 'replace')
    out = []
    cur_font = None
    # tokenize simply: iterate over Tf and show operators in order
    pattern = re.compile(
        r'/(\w+)\s+[\d.]+\s+Tf|\[(.*?)\]\s*TJ|\((?:\\.|[^\\()])*\)\s*Tj|<([0-9A-Fa-f\s]+)>\s*Tj|(T\*|Td|TD|ET)',
        re.S)
    for m in pattern.finditer(txt):
        if m.group(1):
            cur_font = fonts.get(m.group(1))
            continue
        fmap = font_maps.get(cur_font) if cur_font else None
        if m.group(2) is not None:
            parts = []
            arr = m.group(2)
            for mm in re.finditer(r'<([0-9A-Fa-f\s]+)>|\((?:\\.|[^\\()])*\)|(-?\d+\.?\d*)', arr):
                if mm.group(1):
                    h = re.sub(r'\s', '', mm.group(1))
                    parts.append(decode_string(h, fmap))
                elif mm.group(3):
                    try:
                        if float(mm.group(3)) < -120:
                            parts.append(' ')
                    except Exception:
                        pass
            out.append(''.join(parts))
        elif m.group(3) is not None:
            h = re.sub(r'\s', '', m.group(3))
            out.append(decode_string(h, fmap))
        elif m.group(4):
            if m.group(4) in ('T*', 'Td', 'TD', 'ET'):
                out.append('\n')
    return ''.join(out)


all_pages = []
for i, p in enumerate(pages, 1):
    t = page_text(p)
    all_pages.append(t)
    print(f"--- page {i} chars {len(t)}")

# outlines
def outlines():
    body = objs.get(5, b'')
    first = re.search(rb'/First\s+(\d+)\s+0\s+R', body)
    res = []
    if not first:
        return res
    def rec(num, depth):
        b = objs.get(num, b'')
        title = re.search(rb'/Title\s*\(((?:\\.|[^\\()])*)\)', b)
        if title:
            raw = title.group(1)
            if raw.startswith(b'\xfe\xff'):
                t = raw[2:].decode('utf-16-be', 'replace')
            else:
                t = raw.decode('latin-1', 'replace')
            res.append('  ' * depth + t)
        f = re.search(rb'/First\s+(\d+)\s+0\s+R', b)
        if f:
            rec(int(f.group(1)), depth + 1)
        nxt = re.search(rb'/Next\s+(\d+)\s+0\s+R', b)
        if nxt:
            rec(int(nxt.group(1)), depth)
    rec(int(first.group(1)), 0)
    return res

print("=== OUTLINES ===")
outlines_txt = outlines()
with open(sys.argv[2], 'w', encoding='utf-8') as f:
    f.write('===== OUTLINES =====\n')
    f.write('\n'.join(outlines_txt))
    f.write('\n\n===== PAGES =====\n')
    f.write('\n'.join(f'[[[PAGE {i+1}]]]\n{t}' for i, t in enumerate(all_pages)))
print("total chars", sum(len(t) for t in all_pages))
print("outlines", len(outlines_txt))
