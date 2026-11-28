#!/usr/bin/env python3
"""Gera as peças do P01 em SVG vetorial editável (compatível com Inkscape).
Texto real em Montserrat, degradê linear aplicado no preenchimento das palavras
estratégicas, imagens incorporadas e camadas nomeadas."""
import base64, json, subprocess, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
MEDIR = None
FONTES = os.path.join(AQUI, 'fontes')

PESO_NOME = {400: 'Regular', 500: 'Medium', 600: 'SemiBold', 700: 'Bold'}

# ---------- medição ----------
_cache = {}
import uharfbuzz as hb
_fontes = {}
def _fonte(w):
    if w not in _fontes:
        blob = hb.Blob.from_file_path(os.path.join(FONTES, f'Montserrat-{PESO_NOME[w]}.ttf'))
        face = hb.Face(blob); f = hb.Font(face); _fontes[w] = (f, face.upem)
    return _fontes[w]

def medir(itens):
    """Largura real com shaping (kerning) da Montserrat oficial + espaçamento entre letras."""
    res = []
    for s, w, sz, ls in itens:
        k = (s, w, sz, ls)
        if k not in _cache:
            f, upem = _fonte(w)
            buf = hb.Buffer(); buf.add_str(s); buf.guess_segment_properties()
            hb.shape(f, buf, {'kern': True, 'liga': True})
            adv = sum(p.x_advance for p in buf.glyph_positions) * sz / upem
            _cache[k] = adv + ls * len(s)
        res.append(_cache[k])
    return res

def larg(s, w, sz, ls):
    return medir([[s, w, sz, ls]])[0]

def espaco(w, sz, ls):
    a, b = medir([['n n', w, sz, ls], ['nn', w, sz, ls]])
    return a - b

def estilo(w, sz, ls):
    return (f"font-family:Montserrat;font-weight:{w};font-size:{sz}px;letter-spacing:{ls}px;"
            f"-inkscape-font-specification:'Montserrat {PESO_NOME[w]}'")

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

# ---------- linha de título com segmentos (cada palavra em degradê vira um <text> próprio) ----------
def linha(segs, x0, base, sz, ls, alinhar='start', largura_area=None):
    """segs: [(texto, peso, preenchimento)]. Retorna SVG."""
    ws = [larg(t, w, sz, ls) for t, w, f in segs]
    sp = [espaco(w, sz, ls) for t, w, f in segs]
    total = sum(ws) + sum(sp[:-1])
    x = x0 if alinhar == 'start' else x0 + (largura_area - total) / 2
    out = []
    for (t, w, f), wd, s in zip(segs, ws, sp):
        out.append(f'<text xml:space="preserve" x="{x:.1f}" y="{base:.1f}" style="{estilo(w, sz, ls)};fill:{f}">{esc(t)}</text>')
        x += wd + s
    return '\n'.join(out), total

# ---------- parágrafo com quebra automática e trechos em outro peso/cor ----------
def paragrafo(runs, x0, base, sz, lh, ls, largura, alinhar='start', nome='Apoio'):
    """runs: [(texto, peso, cor)]. Quebra por palavras sem reduzir a fonte."""
    tokens = []
    for t, w, c in runs:
        for i, palavra in enumerate(t.split(' ')):
            if palavra == '':
                continue
            tokens.append([palavra, w, c])
    # juntar sinais que ficaram separados (ex.: vírgula logo após trecho)
    linhas, atual, w_atual = [], [], 0
    for tok in tokens:
        wt = larg(tok[0], tok[1], sz, ls)
        sp = espaco(tok[1], sz, ls) if atual else 0
        if atual and w_atual + sp + wt > largura:
            linhas.append(atual); atual, w_atual = [], 0; sp = 0
        atual.append(tok + [wt]); w_atual += sp + wt
    if atual:
        linhas.append(atual)
    out = []
    for n, ln in enumerate(linhas):
        y = base + n * lh
        tot = sum(t[3] for t in ln) + sum(espaco(t[1], sz, ls) for t in ln[:-1])
        x = x0 if alinhar == 'start' else x0 + (largura - tot) / 2
        spans = []
        for k, (p, w, c, wt) in enumerate(ln):
            txt = p + (' ' if k < len(ln) - 1 else '')
            spans.append(f'<tspan style="font-weight:{w};-inkscape-font-specification:\'Montserrat {PESO_NOME[w]}\';fill:{c}">{esc(txt)}</tspan>')
        out.append(f'<text xml:space="preserve" x="{x:.1f}" y="{y:.1f}" style="{estilo(500, sz, ls)}">{"".join(spans)}</text>')
    return '\n'.join(out), len(linhas)

def b64(caminho, mime):
    return f'data:{mime};base64,' + base64.b64encode(open(caminho, 'rb').read()).decode()

LOGO = b64(os.path.join(AQUI, 'logo_ecofiscal.png'), 'image/png')
LOGO_W = 400
LOGO_H = round(LOGO_W * 597 / 1894)
LOGO_Y = 1350 - 50 - LOGO_H

def logo():
    return (f'<g inkscape:groupmode="layer" inkscape:label="Logomarca oficial" id="logo">'
            f'<image x="{540 - LOGO_W/2:.0f}" y="{LOGO_Y}" width="{LOGO_W}" height="{LOGO_H}" '
            f'preserveAspectRatio="xMidYMid meet" xlink:href="{LOGO}" href="{LOGO}"/></g>')

DEGRADES = '''
<linearGradient id="degrade" x1="0" y1="0" x2="1" y2="0" gradientUnits="objectBoundingBox">
  <stop offset="0" stop-color="#20B4F5"/><stop offset="0.5" stop-color="#00D6DC"/><stop offset="1" stop-color="#00E6A0"/>
</linearGradient>
<linearGradient id="degradeClaro" x1="0" y1="0" x2="1" y2="0" gradientUnits="objectBoundingBox">
  <stop offset="0" stop-color="#1246C9"/><stop offset="0.5" stop-color="#0A6FB8"/><stop offset="1" stop-color="#007B8C"/>
</linearGradient>'''

def svg(titulo, defs, corpo):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
     width="1080" height="1350" viewBox="0 0 1080 1350">
<title>{titulo}</title>
<defs>{DEGRADES}{defs}</defs>
{corpo}
{logo()}
</svg>'''

G = 'url(#degrade)'
GC = 'url(#degradeClaro)'
BR = '#FFFFFF'
MAR = '#092653'

