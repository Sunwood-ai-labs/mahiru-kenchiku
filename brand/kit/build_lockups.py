#!/usr/bin/env python3
"""Build MAHIRU KENCHIKU lockups with fully outlined wordmarks (no live text).

Fonts (SIL OFL 1.1): Noto Sans Bold / Regular, Noto Sans CJK JP Bold.
Symbol: Stepped Joint (concept D), baked in as transformed path data.
"""
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

NOTO_B = TTFont('/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf')
NOTO_R = TTFont('/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf')
CJK_B = TTFont('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', fontNumber=0)

SYMBOL_D = ("M48,48 H208 V208 H48 Z "
            "M48,112 H116 V136 H172 V160 H208 V176 H156 V152 H84 V128 H48 Z")


def text_paths(font, text, size, tracking_em, x0, baseline):
    """Return (svg_path_d_fragments, total_advance_width). Coordinates baked."""
    upem = font['head'].unitsPerEm
    s = size / upem
    gs = font.getGlyphSet()
    hmtx = font['hmtx']
    cmap = font.getBestCmap()
    frags, cursor = [], x0
    for ch in text:
        gname = cmap[ord(ch)]
        pen = SVGPathPen(gs)
        tpen = TransformPen(pen, (s, 0, 0, -s, cursor, baseline))
        gs[gname].draw(tpen)
        d = pen.getCommands()
        if d:
            frags.append(d)
        cursor += hmtx[gname][0] * s + tracking_em * size
    width = cursor - x0 - tracking_em * size  # drop trailing tracking
    return frags, width


def text_width(font, text, size, tracking_em):
    upem = font['head'].unitsPerEm
    s = size / upem
    hmtx = font['hmtx']
    cmap = font.getBestCmap()
    w = sum(hmtx[cmap[ord(c)]][0] * s for c in text)
    return w + tracking_em * size * (len(text) - 1)


def transform_symbol(scale, tx, ty):
    """Bake a scale/translate into the symbol path (absolute M/H/V/Z only)."""
    import re
    out, cx, cy = [], None, None
    tokens = re.findall(r'([MHVZ])|(-?\d+(?:\.\d+)?)', SYMBOL_D)
    # simpler: manual parse
    parts = SYMBOL_D.replace(',', ' ').replace('Z', ' Z ').replace('M', ' M ').replace('H', ' H ').replace('V', ' V ').split()
    res, i = [], 0
    def fmt(v):
        return f"{v:.1f}".rstrip('0').rstrip('.')
    while i < len(parts):
        t = parts[i]
        if t == 'M':
            x, y = float(parts[i+1]), float(parts[i+2])
            res.append(f"M{fmt(x*scale+tx)},{fmt(y*scale+ty)}")
            i += 3
        elif t == 'H':
            res.append(f"H{fmt(float(parts[i+1])*scale+tx)}")
            i += 2
        elif t == 'V':
            res.append(f"V{fmt(float(parts[i+1])*scale+ty)}")
            i += 2
        elif t == 'Z':
            res.append('Z')
            i += 1
        else:
            i += 1
    return ' '.join(res)


def write_svg(path, w, h, body, title):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}">\n'
           f'  <title>{title}</title>\n  {body}\n</svg>\n')
    open(path, 'w', encoding='utf-8').write(svg)
    print('wrote', path, f'{w:.0f}x{h:.0f}')


def path_el(d, fill='#000'):
    return f'<path fill-rule="evenodd" fill="{fill}" d="{d}"/>'


OUT = '/home/hatch/workspace/logo-brand/kit/lockups/'

# ---------- horizontal EN ----------
sym = path_el(transform_symbol(1.0, 0, 0))
wx = 256 + 38
m_frags, m_w = text_paths(NOTO_B, 'MAHIRU', 118, 0.055, wx, 138)
k_frags, k_w = text_paths(NOTO_R, 'KENCHIKU', 40, 0.335, wx + 2, 196)
body = sym + '\n  ' + path_el(' '.join(m_frags)) + '\n  ' + path_el(' '.join(k_frags))
write_svg(OUT + 'mahiru-horizontal-en.svg', wx + max(m_w, k_w) + 10, 256, body,
          'MAHIRU KENCHIKU — horizontal lockup (EN)')

# ---------- horizontal JP ----------
m2_frags, m2_w = text_paths(CJK_B, 'マヒル建築', 112, 0.04, wx, 140)
k2_frags, k2_w = text_paths(NOTO_R, 'MAHIRU KENCHIKU', 29, 0.30, wx + 2, 194)
body = sym + '\n  ' + path_el(' '.join(m2_frags)) + '\n  ' + path_el(' '.join(k2_frags))
write_svg(OUT + 'mahiru-horizontal-jp.svg', wx + max(m2_w, k2_w) + 10, 256, body,
          'MAHIRU KENCHIKU — horizontal lockup (JP)')

# ---------- stacked EN ----------
S = 0.78
sym_w = 256 * S
m3_w = text_width(NOTO_B, 'MAHIRU', 92, 0.055)
k3_w = text_width(NOTO_R, 'KENCHIKU', 31, 0.335)
W = max(sym_w, m3_w, k3_w) + 40
sym_x = (W - sym_w) / 2
body = path_el(transform_symbol(S, sym_x, 6))
m3_frags, _ = text_paths(NOTO_B, 'MAHIRU', 92, 0.055, (W - m3_w) / 2, 256 * S + 96)
k3_frags, _ = text_paths(NOTO_R, 'KENCHIKU', 31, 0.335, (W - k3_w) / 2, 256 * S + 146)
body += '\n  ' + path_el(' '.join(m3_frags)) + '\n  ' + path_el(' '.join(k3_frags))
write_svg(OUT + 'mahiru-stacked-en.svg', W, 256 * S + 168, body,
          'MAHIRU KENCHIKU — stacked lockup (EN)')

# ---------- wordmark EN ----------
wm_frags, wm_w = text_paths(NOTO_B, 'MAHIRU', 118, 0.055, 6, 128)
wk_frags, wk_w = text_paths(NOTO_R, 'KENCHIKU', 40, 0.335, 8, 186)
body = path_el(' '.join(wm_frags)) + '\n  ' + path_el(' '.join(wk_frags))
write_svg(OUT + 'mahiru-wordmark-en.svg', max(wm_w, wk_w) + 16, 214, body,
          'MAHIRU KENCHIKU — wordmark (EN)')

# ---------- wordmark JP ----------
wj_frags, wj_w = text_paths(CJK_B, 'マヒル建築', 112, 0.04, 6, 130)
body = path_el(' '.join(wj_frags))
write_svg(OUT + 'mahiru-wordmark-jp.svg', wj_w + 16, 158, body,
          'MAHIRU KENCHIKU — wordmark (JP)')
