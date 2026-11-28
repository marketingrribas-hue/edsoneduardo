#!/usr/bin/env python3
"""Direção de arte individual — publicações P01 a P09 (SVG editável, Inkscape).
Cada peça tem composição própria; a automação apenas posiciona texto medido e exporta."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base_svg import larg, espaco, estilo, esc, b64, logo, LOGO_H

AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(AQUI, 'lote1')
os.makedirs(OUT, exist_ok=True)
FOTO = lambda n: b64(os.path.join(AQUI, 'fotos', n), 'image/jpeg')

CT, CL, CLS = 128, 136, -2.4     # título de capa / card único
IT, IL, ILS = 120, 128, -2.3     # título interno
A, AL, ALS = 60, 82, -0.6        # texto complementar
BR, NAV, TXT_E, TXT_C = '#FFFFFF', '#092653', '#E8EFF9', '#1C2F52'
G, GC = 'url(#degrade)', 'url(#degradeClaro)'

DEFS = '''<linearGradient id="degrade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#20B4F5"/><stop offset="0.5" stop-color="#00D6DC"/><stop offset="1" stop-color="#00E6A0"/></linearGradient>
<linearGradient id="degradeClaro" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#1287D4"/><stop offset="0.5" stop-color="#00A3B4"/><stop offset="1" stop-color="#00A47E"/></linearGradient>
<linearGradient id="degradeV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#20B4F5"/><stop offset="0.5" stop-color="#00D6DC"/><stop offset="1" stop-color="#00E6A0"/></linearGradient>
<filter id="grao" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="3" result="n"/><feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.04 0"/></filter>'''

def W(t, w, sz, ls): return larg(t, w, sz, ls)

def linhas(spec, x0, y0, sz, lh, ls, alinhar='start', area=(90, 900)):
    """spec: lista de linhas; cada linha = [(texto, peso, preenchimento)]. Retorna SVG editável."""
    out = []
    for n, segs in enumerate(spec):
        y = y0 + n * lh
        tot = sum(W(t, w, sz, ls) for t, w, f in segs) + sum(espaco(w, sz, ls) for t, w, f in segs[:-1])
        x = x0 if alinhar == 'start' else area[0] + (area[1] - tot) / 2
        for t, w, f in segs:
            out.append(f'<text xml:space="preserve" x="{x:.1f}" y="{y:.1f}" style="{estilo(w, sz, ls)};fill:{f}">{esc(t)}</text>')
            x += W(t, w, sz, ls) + espaco(w, sz, ls)
    return '\n'.join(out)

def auto(palavras, x0, y0, sz, lh, ls, maxw=900, alinhar='start', area=(90, 900)):
    """Quebra medida (sem reduzir fonte). palavras: [(palavra, peso, preenchimento)]."""
    spec, cur, wc = [], [], 0
    for t, w, f in palavras:
        wt = W(t, w, sz, ls); sp = espaco(w, sz, ls) if cur else 0
        if cur and wc + sp + wt > maxw: spec.append(cur); cur, wc, sp = [], 0, 0
        cur.append((t, w, f)); wc += sp + wt
    if cur: spec.append(cur)
    # agrupa vizinhos do mesmo estilo
    sp2 = []
    for ln in spec:
        g = []
        for t, w, f in ln:
            if g and g[-1][1] == w and g[-1][2] == f: g[-1] = (g[-1][0] + ' ' + t, w, f)
            else: g.append((t, w, f))
        sp2.append(g)
    return linhas(sp2, x0, y0, sz, lh, ls, alinhar, area), len(sp2)

def P(txt, w, f): return [(x, w, f) for x in txt.split()]

def apoio(texto, destaque, x0, y0, largura, cor, cor_d, alinhar='start', area=(90, 900)):
    """Texto complementar com quebra medida; `destaque` (trecho exato) em Bold."""
    tokens = []
    if destaque and destaque in texto:
        a, b = texto.split(destaque, 1)
        for p in a.split(): tokens.append((p, 500, cor))
        for p in destaque.split(): tokens.append((p, 700, cor_d))
        for p in b.split():
            if tokens and p[0] in ',.;:' : tokens[-1] = (tokens[-1][0] + p, tokens[-1][1], tokens[-1][2])
            else: tokens.append((p, 500, cor))
    else:
        tokens = [(p, 500, cor) for p in texto.split()]
    lns, cur, wc = [], [], 0
    for t, w, c in tokens:
        wt = W(t, w, A, ALS); sp = espaco(w, A, ALS) if cur else 0
        if cur and wc + sp + wt > largura: lns.append(cur); cur, wc, sp = [], 0, 0
        cur.append((t, w, c)); wc += sp + wt
    if cur: lns.append(cur)
    out = []
    for n, ln in enumerate(lns):
        tot = sum(W(t, w, A, ALS) for t, w, c in ln) + sum(espaco(w, A, ALS) for t, w, c in ln[:-1])
        x = x0 if alinhar == 'start' else area[0] + (area[1] - tot) / 2
        spans = ''.join(f'<tspan style="font-weight:{w};-inkscape-font-specification:\'Montserrat {"Bold" if w == 700 else "Medium"}\';fill:{c}">{esc(t + (" " if k < len(ln) - 1 else ""))}</tspan>' for k, (t, w, c) in enumerate(ln))
        out.append(f'<text xml:space="preserve" x="{x:.1f}" y="{y0 + n * AL:.1f}" style="{estilo(500, A, ALS)}">{spans}</text>')
    return '\n'.join(out), len(lns)

def camada(nome, conteudo): return f'<g inkscape:groupmode="layer" inkscape:label="{nome}">\n{conteudo}\n</g>'

def salvar(nome, titulo, defs, corpo, grao=True):
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" width="1080" height="1350" viewBox="0 0 1080 1350">
<title>{esc(titulo)}</title>
<defs>{DEFS}{defs}</defs>
{corpo}
{camada("Granulação", '<rect width="1080" height="1350" filter="url(#grao)"/>') if grao else ''}
{logo()}
</svg>'''
    open(os.path.join(OUT, nome + '.svg'), 'w').write(svg)

# ---------- fundos reutilizáveis da identidade ----------
def f_branco(lx=0.9, ly=0.08):
    d = f'''<linearGradient id="fb" x1="0" y1="0" x2="0.4" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#EEF2F8"/></linearGradient>
<radialGradient id="lb1" cx="{lx}" cy="{ly}" r="0.7"><stop offset="0" stop-color="#1246C9" stop-opacity="0.15"/><stop offset="0.55" stop-color="#20B4F5" stop-opacity="0.06"/><stop offset="1" stop-color="#20B4F5" stop-opacity="0"/></radialGradient>
<radialGradient id="lb2" cx="{1-lx}" cy="{1-ly}" r="0.55"><stop offset="0" stop-color="#00D6DC" stop-opacity="0.12"/><stop offset="1" stop-color="#00D6DC" stop-opacity="0"/></radialGradient>'''
    c = camada('Fundo branco', '<rect width="1080" height="1350" fill="url(#fb)"/><rect width="1080" height="1350" fill="url(#lb1)"/><rect width="1080" height="1350" fill="url(#lb2)"/>')
    return d, c

def f_azul(c0, c1, c2, lx=0.85, ly=0.15, luz='#0865EE', op=0.32):
    d = f'''<linearGradient id="fa" x1="0.2" y1="0" x2="0.5" y2="1"><stop offset="0" stop-color="{c0}"/><stop offset="0.55" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>
<radialGradient id="la" cx="{lx}" cy="{ly}" r="0.65"><stop offset="0" stop-color="{luz}" stop-opacity="{op}"/><stop offset="1" stop-color="{luz}" stop-opacity="0"/></radialGradient>
<linearGradient id="ba" x1="0" y1="0" x2="0" y2="1"><stop offset="0.74" stop-color="#092653" stop-opacity="0"/><stop offset="1" stop-color="#092653" stop-opacity="0.85"/></linearGradient>'''
    c = camada('Fundo azul', '<rect width="1080" height="1350" fill="url(#fa)"/><rect width="1080" height="1350" fill="url(#la)"/><rect width="1080" height="1350" fill="url(#ba)"/>')
    return d, c

ROYAL = ('#1246C9', '#0B3A9E', '#092653')
MARINHO = ('#0B3A9E', '#092653', '#071F48')
VIBRANTE = ('#0865EE', '#1246C9', '#0A2E86')

def fachada(op=0.30, x=-520, y=-260, w=2160, h=2700, ang=0):
    foto = FOTO('p09_arquitetura.jpg')
    d = '<linearGradient id="ff" x1="0" y1="0" x2="1" y2="1"><stop offset="0.2" stop-color="#000"/><stop offset="0.8" stop-color="#fff"/></linearGradient><mask id="mf"><rect width="1080" height="1350" fill="url(#ff)"/></mask>'
    c = camada('Fachada · textura', f'<g mask="url(#mf)" opacity="{op}"><image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice" transform="rotate({ang} 540 675)" style="mix-blend-mode:luminosity" xlink:href="{foto}"/></g>')
    return d, c

def interno(nome, titulo_doc, fundo, tit_spec, texto, destaque, claro, extra_defs='', extra='', y_tit=470, x0=90, larg_ap=900):
    """Card interno: título 120 px em até 2 linhas + texto complementar 60 px."""
    fd, fc = fundo
    cor_a, cor_d = (TXT_C, '#0A6FB8') if claro else (TXT_E, BR)
    t = linhas(tit_spec, x0, y_tit, IT, IL, ILS)
    ap, n = apoio(texto, destaque, x0, y_tit + (len(tit_spec) - 1) * IL + 140, larg_ap, cor_a, cor_d)
    salvar(nome, titulo_doc, fd + extra_defs, fc + extra + camada('Título interno · 120 px', t) + camada('Texto complementar · 60 px', ap))
    return n

# ======================================================================
# P01 — cards 04 e 05 (02 e 03 já aprovados)
interno('2026-11-27_0900_C04', 'P01 · card 04', f_branco(0.92, 0.06),
        [[('Confirme no', 500, NAV)], [('portal', 700, GC)]],
        'Consulte a opção registrada e as condições vigentes antes de orientar qualquer mudança.', 'opção registrada', True, y_tit=480)
fd, fc = f_azul(*MARINHO, lx=0.2, ly=0.1)
fd2, fc2 = fachada(0.32, -300, -200, 1800, 2250)
interno('2026-11-27_0900_C05', 'P01 · card 05', (fd + fd2, fc + fc2),
        [[('Decisão', 500, BR)], [('documentada', 700, G)]],
        'Registre os cenários e a orientação ao empresário antes de qualquer alteração.', 'os cenários e a orientação', False, y_tit=480)

# ======================================================================
# P02 — card único · C branco editorial (ref. Anderson/Whost): tipografia dominante, formas discretas
fd, fc = f_branco(0.95, 0.95)
orb = camada('Formas discretas', '''<circle cx="1010" cy="70" r="300" fill="none" stroke="url(#degradeClaro)" stroke-width="2" opacity="0.35"/>
<circle cx="1010" cy="70" r="220" fill="none" stroke="url(#degradeClaro)" stroke-width="2" opacity="0.22"/>''')
t = linhas([[('O', 500, NAV), ('DAS', 700, GC), ('mais', 500, NAV)], [('baixo não', 500, NAV)], [('garante a', 500, NAV)],
            [('melhor', 700, GC)], [('decisão', 700, GC)], [('tributária.', 700, GC)]], 90, 230, CT, CL, CLS)
ap, _ = apoio('O perfil dos clientes e fornecedores também importa.', 'clientes e fornecedores', 90, 230 + 5 * CL + 118, 760, TXT_C, '#0A6FB8')
salvar('2026-11-27_1800_C01', 'P02 · card único', fd, fc + orb + camada('Título · 128 px', t) + camada('Texto complementar · 60 px', ap))

# ======================================================================
# P03 — carrossel ICMS · A fotografia (estoque com duas embalagens idênticas), texto central no alto
foto = FOTO('p03_estoque.jpg')
d = '''<linearGradient id="t3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#071F48" stop-opacity="0.92"/><stop offset="0.36" stop-color="#0B3A9E" stop-opacity="0.55"/><stop offset="0.55" stop-color="#0B3A9E" stop-opacity="0.12"/><stop offset="0.80" stop-color="#092653" stop-opacity="0.35"/><stop offset="1" stop-color="#092653" stop-opacity="0.92"/></linearGradient>
<linearGradient id="cor3" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1246C9"/><stop offset="1" stop-color="#092653"/></linearGradient>'''
c = camada('Fotografia · estoque', f'<rect width="1080" height="1350" fill="url(#cor3)"/><image x="0" y="60" width="1080" height="1350" preserveAspectRatio="xMidYMid slice" style="mix-blend-mode:luminosity" opacity="0.88" xlink:href="{foto}"/>') + \
    camada('Tratamento', '<rect width="1080" height="1350" fill="url(#t3)"/>')
t = linhas([[('Mesmo', 500, BR)], [('produto.', 500, BR)], [('ICMS', 700, G)], [('diferente.', 700, G)]], 0, 200, CT, CL, CLS, 'center')
t2 = linhas([[('Onde está a', 500, BR), ('diferença?', 700, G)]], 0, 200 + 3 * CL + 108, 64, 80, -0.8, 'center')
salvar('2026-11-28_0900_C01', 'P03 · capa', d, c + camada('Título · 128 px', t + '\n' + t2))
# P03 · internos (E educativo: trilha de 4 etapas no topo)
def trilha(atual, claro):
    base = '#C9D5E6' if claro else '#2C4E8F'
    s = ''
    for i in range(4):
        x = 90 + i * 232
        s += f'<rect x="{x}" y="170" width="212" height="10" rx="5" fill="{"url(#degradeClaro)" if (claro and i == atual) else ("url(#degrade)" if i == atual else base)}"/>'
    return camada('Trilha das etapas', s)
etapas = [('A', 'mercadoria', 'Descrição, NCM e demais características precisam corresponder ao produto real.', 'NCM'),
          ('A', 'operação', 'Origem, destino, finalidade e perfil do destinatário podem alterar a regra.', 'Origem, destino, finalidade'),
          ('A', 'legislação', 'Consulte o tratamento vigente no estado e na data da operação.', 'no estado e na data'),
          ('A', 'conferência', 'Documente o fundamento fiscal antes de parametrizar o sistema.', 'fundamento fiscal')]
for i, (a, b, tx, dz) in enumerate(etapas):
    claro = i < 3
    fundo = f_branco(0.9, 0.9 if i % 2 else 0.1) if claro else f_azul(*MARINHO, lx=0.85, ly=0.85)
    cor = NAV if claro else BR
    interno(f'2026-11-28_0900_C{i + 2:02d}', f'P03 · card {i + 2:02d}', fundo,
            [[(a, 500, cor), (b, 700, GC if claro else G)]], tx, dz, claro, extra=trilha(i, claro), y_tit=420)

# ======================================================================
# P04 — card único · D marinho com mapa estilizado de Mato Grosso (objeto em segundo plano)
mt = re.search(r'"id":"mt","path":"([^"]+)"', open(os.path.join(AQUI, 'fotos', 'mapa', 'package', 'index.js')).read()).group(1)
fd, fc = f_azul(*MARINHO, lx=0.7, ly=0.45, luz='#0865EE', op=0.38)
d = '''<pattern id="pontos" width="4" height="4" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="0.7" fill="#20B4F5"/></pattern>
<linearGradient id="mtg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#20B4F5"/><stop offset="0.5" stop-color="#00D6DC"/><stop offset="1" stop-color="#00E6A0"/></linearGradient>'''
mapa = camada('Mapa estilizado · Mato Grosso', f'''<g transform="translate(410 300) scale(3.6) translate(-193.6 -196.2)" opacity="0.42">
<path d="{mt}" fill="url(#pontos)"/>
<path d="{mt}" fill="none" stroke="url(#mtg)" stroke-width="0.6"/></g>''')
t, n = auto(P('Copiar a regra de', 500, BR) + P('ICMS', 700, G) + P('de outro estado pode sair caro em', 500, BR) + P('MT.', 700, G), 90, 250, CT, CL, CLS)
ap, _ = apoio('Acompanhar a legislação estadual faz parte do trabalho do especialista.', 'legislação estadual', 90, 250 + (n - 1) * CL + 118, 900, TXT_E, BR)
salvar('2026-11-28_1800_C01', 'P04 · card único', fd + d, fc + mapa + camada('Título · 128 px', t) + camada('Texto complementar · 60 px', ap))

# ======================================================================
# P05 — carrossel · B azul vibrante com o computador (tela desfocada) como elemento protagonista
foto = FOTO('p05_computador.jpg')
d = '''<linearGradient id="t5" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0865EE" stop-opacity="1"/><stop offset="0.42" stop-color="#0865EE" stop-opacity="0.97"/><stop offset="0.58" stop-color="#1246C9" stop-opacity="0.40"/><stop offset="0.78" stop-color="#0A2E86" stop-opacity="0.25"/><stop offset="1" stop-color="#092653" stop-opacity="0.92"/></linearGradient>
<filter id="desf2"><feGaussianBlur stdDeviation="4.5"/></filter>
<clipPath id="tela"><rect x="140" y="360" width="800" height="560" rx="6"/></clipPath>'''
c = camada('Fotografia · sistema (tela desfocada)', f'''<rect width="1080" height="1350" fill="#0A2E86"/>
<image x="0" y="230" width="1080" height="1350" preserveAspectRatio="xMidYMid slice" filter="url(#desf2)" xlink:href="{foto}"/>
''') + \
    camada('Integração ao azul vibrante', '<rect width="1080" height="1350" fill="url(#t5)"/>')
t, n = auto(P('PIS e Cofins', 700, G) + P('dão lugar à', 500, BR) + P('CBS.', 700, G), 90, 200, CT, CL, CLS)
t2 = linhas([[('Seu sistema está pronto?', 500, BR)]], 90, 200 + (n - 1) * CL + 108, 64, 80, -0.8)
salvar('2026-11-29_0900_C01', 'P05 · capa', d, c + camada('Título · 128 px', t + '\n' + t2))
p05 = [('O', 'calendário', 'A transição prevê a substituição de PIS e Cofins pela CBS em 2027.', 'pela CBS em 2027'),
       ('O', 'sistema', 'Revise os campos fiscais e as integrações exigidas na emissão de documentos.', 'campos fiscais e as integrações'),
       ('A', 'operação', 'Teste vendas, devoluções e compras representativas antes da virada.', 'vendas, devoluções e compras'),
       ('O', 'responsável', 'Defina quem valida cada cenário: fiscal, TI e financeiro.', 'fiscal, TI e financeiro.')]
for i, (a, b, tx, dz) in enumerate(p05):
    claro = i % 2 == 1
    if claro:
        fundo = f_branco(0.1, 0.9)
        extra = camada('Barra lateral em degradê', '<rect x="0" y="0" width="14" height="1350" fill="url(#degradeV)"/>')
        ed = ''
    else:
        fd, fc = f_azul(*VIBRANTE, lx=0.9, ly=0.9, luz='#20B4F5', op=0.22)
        fundo = (fd, fc)
        ed = '<linearGradient id="mf5" x1="0" y1="0" x2="0" y2="1"><stop offset="0.45" stop-color="#000"/><stop offset="1" stop-color="#fff"/></linearGradient><mask id="m5"><rect width="1080" height="1350" fill="url(#mf5)"/></mask>'
        extra = camada('Sistema · continuidade', f'<g mask="url(#m5)" opacity="0.22"><image x="-200" y="250" width="1480" height="1850" preserveAspectRatio="xMidYMid slice" filter="url(#desf)" style="mix-blend-mode:luminosity" xlink:href="{foto}"/></g>')
        ed += '<filter id="desf"><feGaussianBlur stdDeviation="14"/></filter>'
    interno(f'2026-11-29_0900_C{i + 2:02d}', f'P05 · card {i + 2:02d}', fundo,
            [[(a, 500, NAV if claro else BR)], [(b, 700, GC if claro else G)]], tx, dz, claro, extra_defs=ed, extra=extra, y_tit=380)

# ======================================================================
# P06 — card único · E branco com sequência gráfica de notas repetidas (margem ampliada para a palavra longa)
fd, fc = f_branco(0.1, 0.05)
notas = ''
for row in range(12):
    for col in range(10):
        x, y = 8 + col * 108, 8 + row * 112
        erro = (row * 10 + col) % 7 == 3
        notas += f'<g opacity="{0.55 if erro else 0.38}"><rect x="{x}" y="{y}" width="92" height="100" rx="10" fill="#FFFFFF" stroke="{"#00A3B4" if erro else "#C9D5E6"}" stroke-width="2"/>'
        notas += f'<rect x="{x + 14}" y="{y + 20}" width="64" height="8" rx="4" fill="{"url(#degradeClaro)" if erro else "#D6E0EE"}"/><rect x="{x + 14}" y="{y + 40}" width="48" height="8" rx="4" fill="#E3EAF4"/><rect x="{x + 14}" y="{y + 60}" width="56" height="8" rx="4" fill="#E3EAF4"/></g>'
notas += '<rect width="1080" height="1350" fill="url(#vel6)"/>'
seq = camada('Sequência gráfica · notas repetidas', notas)
t, n = auto(P('Uma', 500, NAV) + P('parametrização', 500, GC) + P('errada pode se repetir em', 500, NAV) + P('milhares de notas.', 700, GC), 45, 200, CT, CL, CLS, maxw=990)
ap, _ = apoio('Uma configuração de sistema também é uma decisão tributária.', '', 45, 200 + (n - 1) * CL + 100, 990, TXT_C, '#0A6FB8')
salvar('2026-11-29_1800_C01', 'P06 · card único', fd + '<radialGradient id="vel6" cx="0.35" cy="0.45" r="0.75"><stop offset="0.3" stop-color="#F6F8FC" stop-opacity="0.92"/><stop offset="1" stop-color="#F6F8FC" stop-opacity="0.35"/></radialGradient>', fc + seq + camada('Título · 128 px', t) + camada('Texto complementar · 60 px', ap))

# ======================================================================
# P07 — carrossel · E royal com linha do tempo (venda realizada → recebimento pendente)
fd, fc = f_azul(*ROYAL, lx=0.15, ly=0.1, luz='#20B4F5', op=0.22)
tl = camada('Linha do tempo · venda e recebimento', '''<line x1="160" y1="1030" x2="920" y2="1030" stroke="#5C7FD1" stroke-width="4" stroke-dasharray="14 14"/>
<circle cx="160" cy="1030" r="34" fill="url(#degrade)"/>
<circle cx="920" cy="1030" r="34" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-dasharray="10 9"/>''')
t, n = auto(P('Simples', 700, G) + P('no', 500, BR) + P('regime de caixa:', 700, G) + P('vendeu em', 500, BR) + P('2026', 700, G) + P('e ainda não recebeu?', 500, BR), 90, 210, CT, CL, CLS)
salvar('2026-11-30_0900_C01', 'P07 · capa', fd, fc + tl + camada('Título · 128 px', t))
p07 = [('O que', 'mudou', 'O CGSN publicou regra de transição para valores de operações de 2026 ainda não recebidos.', 'regra de transição'),
       ('O', 'levantamento', 'Identifique os recebíveis referentes a operações realizadas até 31 de dezembro de 2026.', 'recebíveis'),
       ('A', 'apuração', 'A orientação oficial prevê inclusão desses valores na apuração de dezembro de 2026.', 'apuração de dezembro de 2026.'),
       ('A', 'conferência', 'Concilie recebíveis e documentos para evitar nova tributação indevida no recebimento posterior.', 'nova tributação indevida')]
def vertical(atual, claro):
    base = '#C9D5E6' if claro else '#3D62B8'
    s = f'<line x1="104" y1="300" x2="104" y2="1100" stroke="{base}" stroke-width="4"/>'
    for i in range(4):
        y = 300 + i * 266
        if i == atual: s += f'<circle cx="104" cy="{y}" r="22" fill="{"url(#degradeClaro)" if claro else "url(#degrade)"}"/>'
        else: s += f'<circle cx="104" cy="{y}" r="12" fill="{base}"/>'
    return camada('Linha do tempo vertical', s)
for i, (a, b, tx, dz) in enumerate(p07):
    claro = i < 3
    fundo = f_branco(0.92, 0.1 if i % 2 == 0 else 0.9) if claro else f_azul(*MARINHO, lx=0.85, ly=0.2)
    interno(f'2026-11-30_0900_C{i + 2:02d}', f'P07 · card {i + 2:02d}', fundo,
            [[(a, 500, NAV if claro else BR)], [(b, 700, GC if claro else G)]], tx, dz, claro, extra=vertical(i, claro), y_tit=420, x0=180, larg_ap=810)

# ======================================================================
# P08 — card único · F tipográfico central em royal (composição centralizada)
fd, fc = f_azul(*ROYAL, lx=0.5, ly=0.42, luz='#0865EE', op=0.45)
t = linhas([[('Quem atende', 500, BR)], [('empresas', 500, BR)], [('precisa discutir', 500, BR)], [('a', 500, BR), ('reforma', 700, G)],
            [('além do', 500, BR), ('DAS.', 700, G)]], 0, 300, CT, CL, CLS, 'center')
ap, _ = apoio('Contadores e tributaristas: comparem os efeitos sobre as operações reais.', 'Contadores e tributaristas:', 0, 300 + 4 * CL + 118, 860, TXT_E, BR, 'center', (110, 860))
salvar('2026-11-30_1800_C01', 'P08 · card único', fd, fc + camada('Título · 128 px', t) + camada('Texto complementar · 60 px', ap))

# ======================================================================
# P09 — carrossel · D institucional premium: detalhe da fachada, texto na base
foto = FOTO('p09_arquitetura.jpg')
d = '''<linearGradient id="t9" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0B3A9E" stop-opacity="0.30"/><stop offset="0.38" stop-color="#0B3A9E" stop-opacity="0.35"/><stop offset="0.55" stop-color="#092653" stop-opacity="0.80"/><stop offset="1" stop-color="#071F48" stop-opacity="0.96"/></linearGradient>'''
c = camada('Fotografia · fachada (detalhe)', f'<rect width="1080" height="1350" fill="#092653"/><image x="-760" y="-180" width="2300" height="2875" preserveAspectRatio="xMidYMid slice" transform="scale(-1 1) translate(-1080 0)" xlink:href="{foto}"/>') + \
    camada('Tratamento', '<rect width="1080" height="1350" fill="url(#t9)"/>')
_pal = P('Achou', 500, BR) + P('crédito tributário?', 700, G) + P('Antes de calcular o valor, prove', 500, BR) + P('o direito.', 700, G)
_, n = auto(_pal, 90, 0, CT, CL, CLS)
t, n = auto(_pal, 90, 1100 - (n - 1) * CL, CT, CL, CLS)
salvar('2026-12-01_0900_C01', 'P09 · capa', d, c + camada('Título · 128 px', t))
p09 = [('Origem', 'do crédito', 'Identifique qual tributo foi recolhido ou escriturado e por que existe diferença.', 'recolhido ou escriturado'),
       ('', 'Documentos', 'Reúna XML, escrituração, comprovantes e memória de cálculo.', 'XML, escrituração, comprovantes'),
       ('', 'Fundamento', 'Verifique a hipótese legal, os limites e o procedimento de utilização.', 'hipótese legal'),
       ('', 'Risco', 'Registre o que está comprovado, o que falta validar e o que deve ser descartado.', 'o que falta validar')]
for i, (a, b, tx, dz) in enumerate(p09):
    claro = i % 2 == 0
    if claro:
        fundo, extra, ed = f_branco(0.95, 0.05), '', ''
    else:
        fd, fc = f_azul(*MARINHO, lx=0.85, ly=0.1)
        fd2, fc2 = fachada(0.28, -700, -300, 2300, 2875)
        fundo, extra, ed = (fd + fd2, fc + fc2), '', ''
    spec = [[(a, 500, NAV if claro else BR)], [(b, 700, GC if claro else G)]] if a else [[(b, 700, GC if claro else G)]]
    interno(f'2026-12-01_0900_C{i + 2:02d}', f'P09 · card {i + 2:02d}', fundo, spec, tx, dz, claro, extra_defs=ed, extra=extra, y_tit=480 if a else 540)
print('ok')
