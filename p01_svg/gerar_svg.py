#!/usr/bin/env python3
"""Gera as peças do P01 em SVG vetorial editável (compatível com Inkscape).
Texto real em Montserrat, degradê linear aplicado no preenchimento das palavras
estratégicas, imagens incorporadas e camadas nomeadas."""
import base64, json, subprocess, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
MEDIR = sys.argv[1]  # caminho do medir.js
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

# ====================== C01 · CAPA (estrutura: carrossel "rotina e liberdade", capa fotográfica) ======================
foto = b64(os.path.join(AQUI, 'foto_capa.jpg'), 'image/jpeg')
T, TL, TLS = 106, 116, -2
A, AL, ALS = 60, 80, -0.6
y1 = 650
l1, _ = linha([('Seu cliente do', 400, BR)], 0, y1, T, TLS, 'center', 1080)
l2, _ = linha([('Simples', 700, G), ('vende', 400, BR)], 0, y1 + TL, T, TLS, 'center', 1080)
l3, _ = linha([('para', 400, BR), ('empresas?', 700, G)], 0, y1 + 2 * TL, T, TLS, 'center', 1080)
ya = y1 + 2 * TL + 52 + 64
a1, _ = linha([('A escolha de', 500, '#E4ECF7'), ('2027', 700, G)], 0, ya, A, ALS, 'center', 1080)
a2, _ = linha([('merece atenção.', 500, '#E4ECF7')], 0, ya + AL, A, ALS, 'center', 1080)
capa = svg('P01 · C01 · Capa', '''
<linearGradient id="tratamento" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#061A38" stop-opacity="0.30"/>
  <stop offset="0.30" stop-color="#061A38" stop-opacity="0.05"/>
  <stop offset="0.44" stop-color="#061A38" stop-opacity="0.55"/>
  <stop offset="0.56" stop-color="#061A38" stop-opacity="0.92"/>
  <stop offset="1" stop-color="#061A38" stop-opacity="1"/>
</linearGradient>
<radialGradient id="vinheta" cx="0.5" cy="0.35" r="0.75">
  <stop offset="0.55" stop-color="#061A38" stop-opacity="0"/><stop offset="1" stop-color="#061A38" stop-opacity="0.55"/>
</radialGradient>''', f'''
<g inkscape:groupmode="layer" inkscape:label="Fotografia · expedição para cliente empresarial">
  <image x="0" y="0" width="1080" height="1350" preserveAspectRatio="xMidYMid slice" xlink:href="{foto}" href="{foto}"/>
</g>
<g inkscape:groupmode="layer" inkscape:label="Tratamento de cor">
  <rect width="1080" height="1350" fill="url(#tratamento)"/>
  <rect width="1080" height="1350" fill="url(#vinheta)"/>
</g>
<g inkscape:groupmode="layer" inkscape:label="Título · 106 px">
{l1}
{l2}
{l3}
</g>
<g inkscape:groupmode="layer" inkscape:label="Apoio · 60 px">
{a1}
{a2}
</g>''')
open(os.path.join(AQUI, 'P01_C01_capa.svg'), 'w').write(capa)

# ====================== C02 · BRANCO TIPOGRÁFICO (estrutura: card claro "Sem rotina, você vive apagando incêndio") ======================
I, IL, ILS = 92, 102, -1.6
t1, _ = linha([('Revise a', 400, MAR)], 90, 500, I, ILS)
t2, _ = linha([('opção', 700, GC)], 90, 500 + IL, I, ILS)
ap, n = paragrafo([('Identifique os clientes que escolheram o', 500, '#1C2F52'),
                   ('regime regular de IBS e CBS', 700, '#007B8C'),
                   ('para o primeiro semestre de 2027.', 500, '#1C2F52')],
                  140, 740, A, 82, ALS, 850)
fio_y0, fio_y1 = 740 - 58, 740 + (n - 1) * 82 + 22
c02 = svg('P01 · C02 · Branco tipográfico', '''
<linearGradient id="fundoClaro" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#F3F5F8"/>
</linearGradient>
<linearGradient id="forma1" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#EEF2F7"/><stop offset="1" stop-color="#E3E9F1"/>
</linearGradient>
<linearGradient id="fio" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#20B4F5"/><stop offset="0.5" stop-color="#00D6DC"/><stop offset="1" stop-color="#00E6A0"/>
</linearGradient>''', f'''
<g inkscape:groupmode="layer" inkscape:label="Fundo">
  <rect width="1080" height="1350" fill="url(#fundoClaro)"/>
  <circle cx="1210" cy="560" r="640" fill="url(#forma1)"/>
  <circle cx="1210" cy="560" r="430" fill="#FFFFFF" opacity="0.55"/>
</g>
<g inkscape:groupmode="layer" inkscape:label="Título · 92 px">
{t1}
{t2}
</g>
<g inkscape:groupmode="layer" inkscape:label="Fio vertical">
  <rect x="92" y="{fio_y0}" width="5" height="{fio_y1 - fio_y0}" rx="2.5" fill="url(#fio)"/>
</g>
<g inkscape:groupmode="layer" inkscape:label="Apoio · 60 px">
{ap}
</g>''')
open(os.path.join(AQUI, 'P01_C02_branco.svg'), 'w').write(c02)

# ====================== C03 · AZUL VIBRANTE (estrutura: card escuro "Como montar uma rotina", painéis geométricos + cores do relógio) ======================
tt, _ = linha([('Compare a', 400, BR), ('cadeia', 700, G)], 90, 560, I, ILS)
ap3, n3 = paragrafo([('Considere o', 500, '#E4ECF7'), ('perfil dos compradores,', 700, BR),
                     ('os créditos possíveis e os custos da operação.', 500, '#E4ECF7')],
                    90, 700, A, 82, ALS, 860)
c03 = svg('P01 · C03 · Azul vibrante', '''
<linearGradient id="fundoAzul" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#0865EE"/><stop offset="0.58" stop-color="#1246C9"/><stop offset="0.86" stop-color="#0B2F86"/><stop offset="1" stop-color="#092653"/>
</linearGradient>
<linearGradient id="painel" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#061A38" stop-opacity="0.00"/><stop offset="0.35" stop-color="#061A38" stop-opacity="0.30"/><stop offset="1" stop-color="#061A38" stop-opacity="0.55"/>
</linearGradient>
<linearGradient id="painelLuz" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#20B4F5" stop-opacity="0.00"/><stop offset="0.5" stop-color="#20B4F5" stop-opacity="0.16"/><stop offset="1" stop-color="#00D6DC" stop-opacity="0.04"/>
</linearGradient>
<filter id="desfoque" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="90"/></filter>''', f'''
<g inkscape:groupmode="layer" inkscape:label="Fundo">
  <rect width="1080" height="1350" fill="url(#fundoAzul)"/>
  <ellipse cx="880" cy="260" rx="360" ry="260" fill="#20B4F5" opacity="0.40" filter="url(#desfoque)"/>
  <ellipse cx="200" cy="1120" rx="340" ry="200" fill="#00D6DC" opacity="0.18" filter="url(#desfoque)"/>
</g>
<g inkscape:groupmode="layer" inkscape:label="Painéis geométricos">
  <rect x="620" y="0" width="220" height="1350" fill="url(#painel)"/>
  <rect x="0" y="0" width="1080" height="2" fill="none"/>
  <rect x="800" y="140" width="280" height="1210" fill="url(#painel)"/>
  <rect x="930" y="380" width="150" height="970" fill="url(#painelLuz)"/>
</g>
<g inkscape:groupmode="layer" inkscape:label="Título · 92 px">
{tt}
</g>
<g inkscape:groupmode="layer" inkscape:label="Apoio · 60 px">
{ap3}
</g>''')
open(os.path.join(AQUI, 'P01_C03_azul.svg'), 'w').write(c03)
print('ok', n, n3)
