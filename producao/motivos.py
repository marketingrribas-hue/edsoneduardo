"""Motivos gráficos vetoriais da identidade EcoFiscal (traço em degradê, sem dados inventados).
Cada função desenha dentro de uma caixa (x, y, w, h) e devolve SVG. `g` = id do degradê."""
import json, os, re

AQUI = os.path.dirname(os.path.abspath(__file__))
_BR = json.load(open(os.path.join(AQUI, 'fotos', 'brasil.json')))

def _doc(x, y, w, h, g, sw, fill, linhas=5, rx=18):
    s = f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{rx}" fill="{fill}" stroke="url(#{g})" stroke-width="{sw}"/>'
    for i in range(linhas):
        lw = w * (0.68 if i % 3 == 2 else 0.78)
        s += f'<rect x="{x + w * 0.11:.0f}" y="{y + h * 0.16 + i * h * 0.13:.0f}" width="{lw * (0.6 if i == 0 else 1):.0f}" height="{max(6, h * 0.035):.0f}" rx="4" fill="url(#{g})" opacity="{0.9 if i == 0 else 0.35}"/>'
    return s

def documentos(x, y, w, h, g, fill, base=None):
    dw, dh = w * 0.56, h * 0.86
    s = ''
    for k in range(3):
        s += f'<g opacity="{[0.35, 0.6, 1][k]}">' + _doc(x + k * w * 0.2, y + (2 - k) * h * 0.06, dw, dh, g, 4, fill) + '</g>'
    return s

def lupa(x, y, w, h, g, fill, base=None):
    dw, dh = w * 0.62, h * 0.92
    s = _doc(x, y, dw, dh, g, 4, fill, 6)
    r = min(w, h) * 0.24
    cx, cy = x + dw * 0.86, y + dh * 0.6
    s += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="{fill}" stroke="url(#{g})" stroke-width="10"/>'
    s += f'<line x1="{cx + r * 0.72:.0f}" y1="{cy + r * 0.72:.0f}" x2="{cx + r * 1.45:.0f}" y2="{cy + r * 1.45:.0f}" stroke="url(#{g})" stroke-width="16" stroke-linecap="round"/>'
    return s

def pastas(x, y, w, h, g, fill, base=None):
    s = ''
    for k in range(4):
        yy = y + k * h * 0.2
        s += f'<g opacity="{0.35 + 0.2 * k}"><path d="M{x + k * 14:.0f} {yy + 30:.0f} h{w * 0.3:.0f} l24 -30 h{w * 0.25:.0f} v30 h{w * 0.35 - k * 28:.0f} v{h * 0.34:.0f} h-{w - k * 28:.0f} z" fill="{fill}" stroke="url(#{g})" stroke-width="4" stroke-linejoin="round"/></g>'
    return s

def colunas(x, y, w, h, g, fill, base):
    bw = w * 0.28
    s = f'<line x1="{x:.0f}" y1="{y + h:.0f}" x2="{x + w:.0f}" y2="{y + h:.0f}" stroke="{base}" stroke-width="3"/>'
    for k, alt in enumerate((0.62, 0.92)):
        bx = x + w * 0.12 + k * w * 0.46
        s += f'<rect x="{bx:.0f}" y="{y + h * (1 - alt):.0f}" width="{bw:.0f}" height="{h * alt:.0f}" rx="14" fill="{"url(#" + g + ")" if k else fill}" stroke="url(#{g})" stroke-width="4" opacity="{1 if k else 0.8}"/>'
    return s

def transicao(x, y, w, h, g, fill, base):
    n = 8; bw = w / n * 0.62
    s = ''
    for i in range(n):
        bx = x + i * w / n
        a = h * (0.9 - i * 0.1); b = h * (0.12 + i * 0.1)
        s += f'<rect x="{bx:.0f}" y="{y + h - a:.0f}" width="{bw:.0f}" height="{a:.0f}" rx="8" fill="{base}" opacity="0.55"/>'
        s += f'<rect x="{bx + bw * 0.18:.0f}" y="{y + h - b:.0f}" width="{bw * 0.64:.0f}" height="{b:.0f}" rx="6" fill="url(#{g})"/>'
    return s

def parcelas(x, y, w, h, g, fill, base):
    n = 6; bw = w / n * 0.7
    s = ''
    for i in range(n):
        bx = x + i * w / n
        s += f'<rect x="{bx:.0f}" y="{y + h * 0.3:.0f}" width="{bw:.0f}" height="{h * 0.7:.0f}" rx="12" fill="{"url(#" + g + ")" if i == 0 else fill}" stroke="{"none" if i == 0 else base}" stroke-width="3"/>'
    return s

def split(x, y, w, h, g, fill, base):
    yc = y + h / 2
    s = f'<path d="M{x:.0f} {yc:.0f} H{x + w * 0.38:.0f} C{x + w * 0.58:.0f} {yc:.0f} {x + w * 0.58:.0f} {y + h * 0.12:.0f} {x + w:.0f} {y + h * 0.12:.0f}" fill="none" stroke="url(#{g})" stroke-width="22" stroke-linecap="round"/>'
    s += f'<path d="M{x + w * 0.38:.0f} {yc:.0f} C{x + w * 0.58:.0f} {yc:.0f} {x + w * 0.58:.0f} {y + h * 0.88:.0f} {x + w:.0f} {y + h * 0.88:.0f}" fill="none" stroke="{base}" stroke-width="22" stroke-linecap="round"/>'
    return s

def notas(x, y, w, h, g, fill, base):
    s = ''; cols = max(3, int(w // 112)); rows = max(1, int(h // 120))
    for r in range(rows):
        for c in range(cols):
            xx, yy = x + c * 112, y + r * 120
            erro = (r * cols + c) % 5 == 2
            s += f'<g opacity="{1 if erro else 0.6}"><rect x="{xx:.0f}" y="{yy:.0f}" width="92" height="104" rx="10" fill="{fill}" stroke="{"url(#" + g + ")" if erro else base}" stroke-width="2.5"/>'
            s += f'<rect x="{xx + 14:.0f}" y="{yy + 22:.0f}" width="64" height="8" rx="4" fill="{"url(#" + g + ")" if erro else base}"/><rect x="{xx + 14:.0f}" y="{yy + 44:.0f}" width="46" height="8" rx="4" fill="{base}" opacity="0.6"/><rect x="{xx + 14:.0f}" y="{yy + 66:.0f}" width="56" height="8" rx="4" fill="{base}" opacity="0.6"/></g>'
    return s

def rede(x, y, w, h, g, fill, base):
    pts = [(0.18, 0.55), (0.5, 0.2), (0.82, 0.55), (0.5, 0.88)]
    P = [(x + a * w, y + b * h) for a, b in pts]
    s = ''
    for i in range(4):
        for j in range(i + 1, 4):
            s += f'<line x1="{P[i][0]:.0f}" y1="{P[i][1]:.0f}" x2="{P[j][0]:.0f}" y2="{P[j][1]:.0f}" stroke="{base}" stroke-width="3"/>'
    for k, (px, py) in enumerate(P):
        r = 46 if k in (0, 2) else 30
        s += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{r}" fill="{"url(#" + g + ")" if k in (0, 2) else fill}" stroke="url(#{g})" stroke-width="4"/>'
    return s

def contrato(x, y, w, h, g, fill, base):
    dw, dh = w * 0.62, h * 0.95
    s = _doc(x + w * 0.1, y, dw, dh, g, 4, fill, 5)
    sy = y + dh * 0.84
    s += f'<path d="M{x + w * 0.2:.0f} {sy:.0f} c30 -40 60 30 90 -10 s50 -20 80 5" fill="none" stroke="url(#{g})" stroke-width="5" stroke-linecap="round"/>'
    s += f'<line x1="{x + w * 0.62:.0f}" y1="{y + dh * 0.95:.0f}" x2="{x + w * 0.98:.0f}" y2="{y + dh * 0.45:.0f}" stroke="url(#{g})" stroke-width="14" stroke-linecap="round"/>'
    return s

def envelope(x, y, w, h, g, fill, base):
    ew, eh = w * 0.8, h * 0.62
    ex, ey = x + w * 0.1, y + h * 0.2
    s = f'<rect x="{ex:.0f}" y="{ey:.0f}" width="{ew:.0f}" height="{eh:.0f}" rx="16" fill="{fill}" stroke="url(#{g})" stroke-width="5"/>'
    s += f'<path d="M{ex:.0f} {ey + 10:.0f} L{ex + ew / 2:.0f} {ey + eh * 0.58:.0f} L{ex + ew:.0f} {ey + 10:.0f}" fill="none" stroke="url(#{g})" stroke-width="5" stroke-linejoin="round"/>'
    s += f'<circle cx="{ex + ew:.0f}" cy="{ey:.0f}" r="{min(w, h) * 0.1:.0f}" fill="url(#{g})"/>'
    return s

def grafico(x, y, w, h, g, fill, base):
    pts = [(0, 0.7), (0.15, 0.62), (0.3, 0.68), (0.45, 0.45), (0.6, 0.52), (0.75, 0.3), (0.9, 0.36), (1, 0.18)]
    d = ' '.join(f'{"M" if i == 0 else "L"}{x + a * w:.0f} {y + b * h:.0f}' for i, (a, b) in enumerate(pts))
    s = ''.join(f'<line x1="{x:.0f}" y1="{y + h * k / 4:.0f}" x2="{x + w:.0f}" y2="{y + h * k / 4:.0f}" stroke="{base}" stroke-width="2" opacity="0.6"/>' for k in range(5))
    s += f'<path d="{d}" fill="none" stroke="url(#{g})" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'
    a, b = pts[-1]
    s += f'<circle cx="{x + a * w:.0f}" cy="{y + b * h:.0f}" r="16" fill="url(#{g})"/>'
    return s

def blocos(x, y, w, h, g, fill, base):
    """Classificação: grade de blocos de código (sem dígitos)."""
    s = ''; n = 8; bw = w / n - 12
    for i in range(n):
        dest = i in (2, 3)
        s += f'<rect x="{x + i * (bw + 12):.0f}" y="{y + h * 0.25:.0f}" width="{bw:.0f}" height="{h * 0.5:.0f}" rx="12" fill="{"url(#" + g + ")" if dest else fill}" stroke="{"none" if dest else base}" stroke-width="3"/>'
    return s

def festivo(x, y, w, h, g, fill, base):
    import random
    rnd = random.Random(7); s = ''
    for _ in range(60):
        cx, cy = x + rnd.random() * w, y + rnd.random() * h
        r = rnd.choice([3, 4, 5, 7, 10])
        s += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r}" fill="url(#{g})" opacity="{rnd.choice([0.25, 0.45, 0.7])}"/>'
    return s

def _mapa_tf(x, y, w, h, bbox):
    bx0, bx1, by0, by1 = bbox
    sc = min(w / (bx1 - bx0), h / (by1 - by0))
    ox = x + (w - (bx1 - bx0) * sc) / 2 - bx0 * sc
    oy = y + (h - (by1 - by0) * sc) / 2 - by0 * sc
    return sc, ox, oy

def mapa_mt(x, y, w, h, g, fill, base):
    sc, ox, oy = _mapa_tf(x, y, w, h, (193.64, 371.29, 196.22, 366.53))
    return (f'<pattern id="pt{g}" width="4" height="4" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="0.75" fill="url(#{g})"/></pattern>'
            f'<g transform="translate({ox:.1f} {oy:.1f}) scale({sc:.3f})"><path d="{_BR["mt"]}" fill="url(#pt{g})"/><path d="{_BR["mt"]}" fill="none" stroke="url(#{g})" stroke-width="{2.4 / sc:.2f}"/></g>')

def mapa_br(x, y, w, h, g, fill, base):
    sc, ox, oy = _mapa_tf(x, y, w, h, (0.26, 612.26, 0.26, 638.79))
    s = f'<g transform="translate({ox:.1f} {oy:.1f}) scale({sc:.3f})">'
    for uf, p in _BR.items():
        s += f'<path d="{p}" fill="{"url(#" + g + ")" if uf == "mt" else fill}" stroke="{base}" stroke-width="{1.4 / sc:.2f}" opacity="{1 if uf == "mt" else 0.9}"/>'
    # fluxos a partir de MT: mercado interno, outro estado e porto (exportação) — sem números
    for (ax, ay) in ((420, 470), (470, 520), (300, 120)):
        s += f'<path d="M270 300 Q{(270 + ax) / 2 + 40:.0f} {(300 + ay) / 2 - 80:.0f} {ax} {ay}" fill="none" stroke="url(#{g})" stroke-width="{4 / sc:.2f}" stroke-dasharray="{10 / sc:.1f} {8 / sc:.1f}"/>'
        s += f'<circle cx="{ax}" cy="{ay}" r="{8 / sc:.1f}" fill="url(#{g})"/>'
    return s + '</g>'

MOTIVOS = {k: v for k, v in globals().items() if callable(v) and not k.startswith('_')}
