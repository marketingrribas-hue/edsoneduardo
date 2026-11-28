#!/usr/bin/env python3
"""Produção final EcoFiscal — todas as publicações do planejamento aprovado.
- P01: capa, 02 e 03 aprovados (copiados sem alteração); 04 e 05 do lote 1.
- P02–P08: direção de arte do lote 1 (já revisada).
- P09–P70 e todos os Stories: composição individual por pauta (motivo gráfico
  ligado ao conteúdo, família de cor, posição e estilo de carrossel variáveis).
Toda peça passa por verificação geométrica (margens, logo, colisões) antes de salvar."""
import json, os, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base_svg import larg, espaco, estilo, esc, logo, LOGO_H
import motivos as M

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
OUT = os.path.join(AQUI, 'final_svg')
os.makedirs(OUT, exist_ok=True)
PUBS = json.load(open(os.path.join(AQUI, 'planejamento.json')))
LOG = {'excecoes': [], 'qc_falhas': [], 'pecas': []}

MARG = 90
CAPA = (128, 136, -2.4)
INT = (120, 128, -2.3)
STO = (84, 100, -1.4)
A, AL, ALS = 60, 82, -0.6
BR, NAV = '#FFFFFF', '#092653'

# ---------------- destaques ----------------
CH = set('''simples icms icms-st ibs cbs pis cofins das ncm xml erp pgfn receita irpj csll mt split payment diferimento isenção
transação crédito créditos credor autuação fisco apuração incentivo benefício parametrização reforma presumido real agro soja
estoque substituição devolução contrato margem preço fornecedor caixa parcela parcelas acordo desconto recesso notificações
honorários diagnóstico natal decisões decisão empresas saldo uf trilha escrituração parecer tributarista contador especialidade
olhares nota mercadoria destino documental 2026 2027 imposto risco rescindida clientes compra dados entregas operação operações
prova direito dívida negociação feliz boas lucro exportada ano masterclass custo tributário prazo prazos documentação
equipe responsável cenários premissas cálculo'''.split())
LIGA = {'e', 'de', 'do', 'da', 'dos', 'das', 'no', 'na'}

def base(w): return w.lower().strip('.,:;?!()"“”')

def destaques(pal, maximo=2, forcar=True):
    idx = [i for i, p in enumerate(pal) if base(p) in CH and not (base(p) == 'real' and (i == 0 or base(pal[i - 1]) != 'lucro'))]
    tr, cur = [], []
    for i in idx:
        if cur and (i == cur[-1] + 1 or (i == cur[-1] + 2 and base(pal[i - 1]) in LIGA)):
            cur += list(range(cur[-1] + 1, i + 1))
        else:
            if cur: tr.append(cur)
            cur = [i]
    if cur: tr.append(cur)
    tr = [t[:4] for t in tr]
    tr.sort(key=lambda t: (len(t), t[-1]), reverse=True)
    tr = tr[:maximo]
    if not tr and forcar: tr = [[len(pal) - 1]]
    return {i for t in tr for i in t}

# ---------------- quebra medida ----------------
def quebra(pal, marc, T, ls, maxw):
    lns, cur, wc = [], [], 0
    for i, p in enumerate(pal):
        w = 700 if i in marc else 500
        wp = larg(p, w, T, ls); sp = espaco(w, T, ls) if cur else 0
        if cur and wc + sp + wp > maxw:
            lns.append(cur); cur, wc, sp = [], 0, 0
        cur.append(i); wc += sp + wp
    if cur: lns.append(cur)
    # evita palavra isolada na última linha
    if len(lns) > 1 and len(lns[-1]) == 1 and len(lns[-2]) >= 3:
        cand = [lns[-2][-1]] + lns[-1]
        if largura_linha(pal, cand, marc, T, ls) <= maxw:
            lns[-2] = lns[-2][:-1]; lns[-1] = cand
    return lns

def largura_linha(pal, ln, marc, T, ls):
    return sum(larg(pal[i], 700 if i in marc else 500, T, ls) for i in ln) + sum(espaco(700 if i in marc else 500, T, ls) for i in ln[:-1])

def ajusta(pal, marc, spec, maxw=900, x0=MARG, rotulo=''):
    """Garante que nenhuma palavra ultrapasse a área útil; registra exceções."""
    T, TL, ls = spec
    maior = max(larg(p, 700 if i in marc else 500, T, ls) for i, p in enumerate(pal))
    if maior > maxw:
        if maior <= 990:
            LOG['excecoes'].append(f'{rotulo}: margem lateral reduzida a 45 px para a palavra mais longa (fonte mantida em {T} px)')
            return (T, TL, ls), 990, 45
        f = 990 / maior
        T2 = int(T * f); TL2 = int(TL * f)
        LOG['excecoes'].append(f'{rotulo}: fonte do título reduzida de {T} para {T2} px (palavra mais longa não cabe na largura útil)')
        return (T2, TL2, ls * f), 990, 45
    return spec, maxw, x0

# ---------------- render ----------------
def render_linhas(pal, lns, marc, x0, y0, spec, cor, grad, alinhar='start', area=(MARG, 900), caixas=None):
    T, TL, ls = spec
    out = []
    for n, ln in enumerate(lns):
        y = y0 + n * TL
        tot = largura_linha(pal, ln, marc, T, ls)
        x = x0 if alinhar == 'start' else area[0] + (area[1] - tot) / 2
        if caixas is not None: caixas.append((x, y - 0.74 * T, tot, 0.98 * T))
        grupos = []
        for i in ln:
            m = i in marc
            if grupos and grupos[-1][0] == m: grupos[-1][1].append(pal[i])
            else: grupos.append([m, [pal[i]]])
        for m, ws in grupos:
            t = ' '.join(ws); w = 700 if m else 500
            out.append(f'<text xml:space="preserve" x="{x:.1f}" y="{y:.1f}" style="{estilo(w, T, ls)};fill:{grad if m else cor}">{esc(t)}</text>')
            x += larg(t, w, T, ls) + espaco(w, T, ls)
    return '\n'.join(out)

def render_apoio(texto, x0, y0, largura, cor, cor_d, alinhar='start', area=(MARG, 900), caixas=None, al=AL):
    pal = texto.split()
    marc = destaques(pal, 1, forcar=False)
    lns = quebra(pal, marc, A, ALS, largura)
    out = []
    for n, ln in enumerate(lns):
        y = y0 + n * al
        tot = largura_linha(pal, ln, marc, A, ALS)
        x = x0 if alinhar == 'start' else area[0] + (area[1] - tot) / 2
        if caixas is not None: caixas.append((x, y - 0.74 * A, tot, 0.98 * A))
        spans = ''.join(f'<tspan style="font-weight:{700 if i in marc else 500};-inkscape-font-specification:\'Montserrat {"Bold" if i in marc else "Medium"}\';fill:{cor_d if i in marc else cor}">{esc(pal[i] + (" " if k < len(ln) - 1 else ""))}</tspan>' for k, i in enumerate(ln))
        out.append(f'<text xml:space="preserve" x="{x:.1f}" y="{y:.1f}" style="{estilo(500, A, ALS)}">{spans}</text>')
    return '\n'.join(out), len(lns)

def camada(nome, c): return f'<g inkscape:groupmode="layer" inkscape:label="{nome}">\n{c}\n</g>'

DEFS = '''<linearGradient id="degrade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#20B4F5"/><stop offset="0.5" stop-color="#00D6DC"/><stop offset="1" stop-color="#00E6A0"/></linearGradient>
<linearGradient id="degradeClaro" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#1287D4"/><stop offset="0.5" stop-color="#00A3B4"/><stop offset="1" stop-color="#00A47E"/></linearGradient>
<linearGradient id="degradeV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#20B4F5"/><stop offset="0.5" stop-color="#00D6DC"/><stop offset="1" stop-color="#00E6A0"/></linearGradient>
<linearGradient id="degradeClaroV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1287D4"/><stop offset="0.5" stop-color="#00A3B4"/><stop offset="1" stop-color="#00A47E"/></linearGradient>
<filter id="grao" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="3" result="n"/><feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.04 0"/></filter>'''

TONS = {'marinho': ('#0B3A9E', '#092653', '#071F48', '#0865EE', 0.30),
        'royal': ('#1246C9', '#0B3A9E', '#092653', '#0865EE', 0.34),
        'vibrante': ('#0865EE', '#1246C9', '#0A2E86', '#20B4F5', 0.26),
        'intermediario': ('#1E5BD6', '#14449F', '#0B2D6B', '#20B4F5', 0.22)}
LUZ = [(0.85, 0.12), (0.12, 0.15), (0.88, 0.55), (0.15, 0.85), (0.6, 0.05), (0.5, 0.95)]

def fundo(tom, var, H):
    lx, ly = LUZ[var % len(LUZ)]
    if tom in ('branco', 'gelo'):
        top = '#FFFFFF' if tom == 'branco' else '#F6F8FB'
        d = f'''<linearGradient id="f" x1="0" y1="0" x2="0.4" y2="1"><stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="#EDF1F7"/></linearGradient>
<radialGradient id="l1" cx="{lx}" cy="{ly}" r="0.7"><stop offset="0" stop-color="#1246C9" stop-opacity="0.14"/><stop offset="0.55" stop-color="#20B4F5" stop-opacity="0.05"/><stop offset="1" stop-color="#20B4F5" stop-opacity="0"/></radialGradient>
<radialGradient id="l2" cx="{1 - lx}" cy="{1 - ly}" r="0.55"><stop offset="0" stop-color="#00D6DC" stop-opacity="0.11"/><stop offset="1" stop-color="#00D6DC" stop-opacity="0"/></radialGradient>'''
        return d, f'<rect width="1080" height="{H}" fill="url(#f)"/><rect width="1080" height="{H}" fill="url(#l1)"/><rect width="1080" height="{H}" fill="url(#l2)"/>', True
    c0, c1, c2, cl, op = TONS[tom]
    d = f'''<linearGradient id="f" x1="0.2" y1="0" x2="0.5" y2="1"><stop offset="0" stop-color="{c0}"/><stop offset="0.55" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>
<radialGradient id="l1" cx="{lx}" cy="{ly}" r="0.65"><stop offset="0" stop-color="{cl}" stop-opacity="{op}"/><stop offset="1" stop-color="{cl}" stop-opacity="0"/></radialGradient>
<linearGradient id="b" x1="0" y1="0" x2="0" y2="1"><stop offset="0.74" stop-color="#092653" stop-opacity="0"/><stop offset="1" stop-color="#092653" stop-opacity="0.85"/></linearGradient>'''
    return d, f'<rect width="1080" height="{H}" fill="url(#f)"/><rect width="1080" height="{H}" fill="url(#l1)"/><rect width="1080" height="{H}" fill="url(#b)"/>', False

def motivo(nome, caixa, claro, opac=1.0):
    x, y, w, h = caixa
    g = 'degradeClaro' if claro else 'degrade'
    fill = '#FFFFFF' if claro else 'rgba(255,255,255,0.05)'
    if not claro: fill = '#0E2F70'
    basec = '#C9D5E6' if claro else '#3D62B8'
    return f'<g opacity="{opac}">' + M.MOTIVOS[nome](x, y, w, h, g, fill, basec) + '</g>'

def qc(nome, caixas, H, logo_top, margem_min=MARG, extra_obst=()):
    falhas = []
    for (x, y, w, h) in caixas:
        if x < margem_min - 1 or x + w > 1080 - margem_min + 1: falhas.append(f'margem lateral ({x:.0f}–{x + w:.0f})')
        if y < 40: falhas.append('topo')
        if y + h > logo_top - 18: falhas.append(f'invade área da logo ({y + h:.0f} > {logo_top - 18})')
        for (ox, oy, ow, oh) in extra_obst:
            if x < ox + ow and x + w > ox and y < oy + oh and y + h > oy: falhas.append('colide com elemento gráfico')
    if falhas: LOG['qc_falhas'].append((nome, sorted(set(falhas))))
    return not falhas

def salvar(nome, titulo, H, defs, corpo, logo_y):
    lg = logo().replace(f'y="{1350 - 50 - LOGO_H}"', f'y="{logo_y}"')
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" width="1080" height="{H}" viewBox="0 0 1080 {H}">
<title>{esc(titulo)}</title>
<defs>{DEFS}{defs}</defs>
{corpo}
{camada('Granulação', f'<rect width="1080" height="{H}" filter="url(#grao)"/>')}
{lg}
</svg>'''
    open(os.path.join(OUT, nome + '.svg'), 'w').write(svg)
    LOG['pecas'].append(nome)

# ---------------- peças ----------------
def peca_feed(nome, titulo_doc, tom, var, titulo, apoio_txt='', kicker=None, tipo='capa', mot=None, pos='base', alinhar='start', estilo_int=None, idx=0):
    H = 1350; logo_top = 1350 - 50 - LOGO_H
    spec = CAPA if tipo == 'capa' else INT
    d, fc, claro = fundo(tom, var, H)
    cor = NAV if claro else BR
    grad = 'url(#degradeClaro)' if claro else 'url(#degrade)'
    cor_a, cor_d = ('#1C2F52', '#0A6FB8') if claro else ('#E8EFF9', BR)
    pal = titulo.split()
    marc = destaques(pal, 2 if tipo == 'capa' else 1)
    x0 = MARG + (90 if estilo_int == 'vertical' else 0)
    maxw = 900 - (90 if estilo_int == 'vertical' else 0)
    spec, maxw, x0b = ajusta(pal, marc, spec, maxw, x0, nome)
    if x0b == 45: x0 = 45
    T, TL, ls = spec
    lns = quebra(pal, marc, T, ls, maxw)
    if tipo == 'interno' and len(pal) <= 4 and len(lns) == 1 and len(pal) >= 2:
        # título curto: estrutura frase/destaque em duas linhas (padrão aprovado do P01)
        nm = [i for i in range(len(pal)) if i not in marc]
        if nm and max(nm) < min(marc): lns = [nm, sorted(marc)]
    # altura do bloco
    gap = 120 if tipo == 'capa' else 136
    ap_lns = 0
    if apoio_txt:
        _, ap_lns = render_apoio(apoio_txt, x0, 0, maxw, cor_a, cor_d)
    k_h = 70 if kicker else 0
    topo, base_lim = 100, logo_top - 40
    alt = k_h + 0.74 * T + (len(lns) - 1) * TL + (gap + (ap_lns - 1) * AL if ap_lns else 0) + 0.24 * T
    passo = 0
    while alt > base_lim - topo and passo < 12:
        passo += 1
        if passo <= 4:      # 1º: reorganiza entrelinha, respiro e margem superior
            TL -= 3; gap -= 8; topo -= 8
        else:               # último recurso: menor ajuste de fonte necessário (registrado)
            T = int(T * 0.97); TL = int(TL * 0.97)
            lns = quebra(pal, marc, T, ls, maxw)
        spec = (T, TL, ls)
        alt = k_h + 0.74 * T + (len(lns) - 1) * TL + (gap + (ap_lns - 1) * AL if ap_lns else 0) + 0.24 * T
    if passo > 4:
        LOG['excecoes'].append(f'{nome}: título ajustado para {T} px (texto aprovado extenso; entrelinha e respiros já reduzidos)')
    livre = base_lim - topo - alt
    corpo_extra, obst = '', []
    mbox = None
    if mot and livre >= 300 and pos in ('base', 'topo'):
        mh = min(420, livre - 60)
        mw = min(820, mh * 1.9)
        if pos == 'base':
            y_txt = topo + 20
            mbox = ((1080 - mw) / 2, y_txt + alt + 50, mw, mh)
        else:
            mbox = ((1080 - mw) / 2, topo + 10, mw, mh)
            y_txt = topo + 10 + mh + 50
        corpo_extra = camada(f'Elemento gráfico · {mot}', motivo(mot, mbox, claro))
        obst = [mbox]
    else:
        y_txt = topo + max(0, livre) / 2
        if mot:
            mw, mh = 760, 760
            corpo_extra = camada(f'Elemento gráfico (fundo) · {mot}', motivo(mot, (1080 - mw - 20, 1350 - mh - 260, mw, mh), claro, 0.16))
    caixas = []
    camadas = [camada('Fundo', fc)]
    if estilo_int == 'barra':
        camadas.append(camada('Barra lateral em degradê', f'<rect x="0" y="0" width="14" height="1350" fill="url(#{"degradeClaroV" if claro else "degradeV"})"/>'))
    camadas.append(corpo_extra)
    y = y_txt + k_h
    if kicker:
        camadas.append(camada('Chamada', f'<text x="{x0}" y="{y - 26:.0f}" style="{estilo(700, 40, 8)};fill:{grad}">{esc(kicker)}</text>'))
        caixas.append((x0, y - 56, larg(kicker, 700, 40, 8), 40))
    y1 = y + 0.74 * T
    camadas.append(camada(f'Título · {T} px', render_linhas(pal, lns, marc, x0, y1, spec, cor, grad, alinhar, (x0, maxw), caixas)))
    if apoio_txt:
        ya = y1 + (len(lns) - 1) * TL + gap
        s, _ = render_apoio(apoio_txt, x0, ya, maxw, cor_a, cor_d, alinhar, (x0, maxw), caixas)
        camadas.append(camada(f'Texto complementar · {A} px', s))
    if estilo_int in ('trilha', 'vertical'):
        n_et, at = 4, idx
        base_c = '#C9D5E6' if claro else '#3D62B8'
        if estilo_int == 'trilha':
            s = ''.join(f'<rect x="{90 + i * 232}" y="{max(60, y_txt - 90):.0f}" width="212" height="10" rx="5" fill="{grad if i == at else base_c}"/>' for i in range(n_et))
        else:
            ys0, ys1 = y_txt - 20, y_txt + alt + 20
            s = f'<line x1="104" y1="{ys0:.0f}" x2="104" y2="{ys1:.0f}" stroke="{base_c}" stroke-width="4"/>'
            for i in range(n_et):
                yy = ys0 + i * (ys1 - ys0) / 3
                s += f'<circle cx="104" cy="{yy:.0f}" r="{22 if i == at else 12}" fill="{grad if i == at else base_c}"/>'
        camadas.append(camada('Indicador de etapa', s))
    if estilo_int == 'motivo' and mot and not mbox:
        pass
    qc(nome, caixas, H, logo_top, 45 if x0 == 45 else MARG, obst)
    salvar(nome, titulo_doc, H, d, '\n'.join(camadas), 1350 - 50 - LOGO_H)

def peca_story(nome, titulo_doc, tom, var, texto, mot):
    H = 1920; logo_y = H - 230 - LOGO_H; logo_top = logo_y
    d, fc, claro = fundo(tom, var, H)
    cor = NAV if claro else BR
    grad = 'url(#degradeClaro)' if claro else 'url(#degrade)'
    pal = texto.split()
    marc = destaques(pal, 2)
    spec, maxw, x0 = ajusta(pal, marc, STO, 900, MARG, nome)
    T, TL, ls = spec
    lns = quebra(pal, marc, T, ls, maxw)
    y1 = 520 + 0.74 * T
    caixas = []
    camadas = [camada('Fundo', fc)]
    if mot:
        camadas.append(camada(f'Elemento gráfico · {mot}', motivo(mot, (240, 150, 600, 290), claro, 0.9)))
    camadas.append(camada(f'Texto · {T} px', render_linhas(pal, lns, marc, x0, y1, spec, cor, grad, 'start', (x0, maxw), caixas)))
    fim = y1 + (len(lns) - 1) * TL
    if fim > 1250: LOG['qc_falhas'].append((nome, ['texto invade a área reservada ao sticker']))
    qc(nome, caixas, H, logo_top, 45 if x0 == 45 else MARG, [(240, 150, 600, 290)] if mot else [])
    salvar(nome, titulo_doc, H, d, '\n'.join(camadas), logo_y)

# ---------------- direção por publicação ----------------
# (tom da capa, motivo gráfico, posição do motivo, estilo dos internos)
DIR = {
 'P09': ('marinho', 'lupa', 'base', 'barra'),
 'P10': ('branco', 'colunas', 'base', None), 'P11': ('vibrante', 'transicao', 'base', 'trilha'),
 'P13': ('marinho', 'pastas', 'topo', 'vertical'), 'P14': ('branco', 'parcelas', 'base', None),
 'P15': ('gelo', 'mapa_br', 'base', 'barra'), 'P16': ('marinho', 'mapa_br', 'fundo', None),
 'P17': ('royal', 'lupa', 'base', 'trilha'), 'P18': ('branco', 'notas', 'base', None),
 'P19': ('gelo', 'colunas', 'topo', 'vertical'), 'P20': ('vibrante', 'colunas', 'fundo', None),
 'P21': ('marinho', 'mapa_mt', 'base', 'barra'), 'P22': ('branco', 'pastas', 'base', None),
 'P23': ('royal', 'notas', 'topo', 'trilha'), 'P25': ('marinho', 'colunas', 'base', 'vertical'),
 'P26': ('branco', 'colunas', 'fundo', None), 'P27': ('gelo', 'rede', 'base', 'barra'),
 'P28': ('marinho', 'rede', 'fundo', None), 'P29': ('vibrante', 'pastas', 'base', 'trilha'),
 'P30': ('branco', 'pastas', 'topo', None), 'P31': ('gelo', 'parcelas', 'base', 'vertical'),
 'P32': ('royal', None, None, None), 'P33': ('marinho', 'documentos', 'base', 'barra'),
 'P34': ('intermediario', 'grafico', 'fundo', None), 'P35': ('vibrante', 'contrato', 'base', 'trilha'),
 'P36': ('marinho', 'contrato', 'fundo', None), 'P37': ('marinho', 'blocos', 'base', 'vertical'),
 'P38': ('branco', 'documentos', 'base', None), 'P39': ('gelo', 'split', 'base', 'barra'),
 'P41': ('marinho', 'blocos', 'topo', 'trilha'), 'P42': ('branco', 'rede', 'base', None),
 'P43': ('gelo', 'notas', 'base', 'vertical'), 'P44': ('royal', 'notas', 'fundo', None),
 'P45': ('marinho', 'notas', 'topo', 'barra'), 'P46': ('branco', 'grafico', 'base', None),
 'P47': ('vibrante', 'colunas', 'base', 'trilha'), 'P48': ('marinho', None, None, None),
 'P49': ('marinho', 'envelope', 'base', 'vertical'), 'P50': ('branco', 'envelope', 'base', None),
 'P51': ('gelo', 'documentos', 'base', 'barra'), 'P52': ('marinho', 'documentos', 'fundo', None),
 'P53': ('royal', 'mapa_br', 'base', 'trilha'), 'P54': ('branco', 'mapa_br', 'base', None),
 'P55': ('gelo', 'envelope', 'base', 'vertical'), 'P56': ('vibrante', 'rede', 'fundo', None),
 'P57': ('marinho', 'festivo', 'fundo', 'barra'), 'P58': ('branco', 'festivo', 'fundo', None),
 'P59': ('royal', 'parcelas', 'base', 'trilha'), 'P60': ('marinho', None, None, None),
 'P61': ('gelo', 'rede', 'base', 'vertical'), 'P63': ('branco', 'documentos', 'topo', 'barra'),
 'P64': ('intermediario', 'grafico', 'fundo', None), 'P65': ('royal', 'mapa_mt', 'base', 'trilha'),
 'P66': ('branco', 'mapa_mt', 'fundo', None), 'P67': ('gelo', 'grafico', 'base', 'vertical'),
 'P68': ('vibrante', 'grafico', 'fundo', None), 'P69': ('marinho', 'notas', 'base', 'barra'),
 'P70': ('branco', 'festivo', 'fundo', None),
}
DIR_LOTE1 = {'P01': 'transicao', 'P02': 'colunas', 'P03': 'blocos', 'P04': 'mapa_mt', 'P05': 'notas', 'P06': 'notas',
             'P07': 'grafico', 'P08': 'rede', 'P12': 'transicao', 'P24': 'notas', 'P40': 'split', 'P62': 'rede'}

def nome_arq(data, hora, suf):
    d, m, a = data.split('/')
    hh = hora.replace('h', ''); hh = (hh[:2] + (hh[2:] if len(hh) > 2 else '00')).ljust(4, '0')
    return f'{a}-{m}-{d}_{hh}_{suf}'

ESQUEMAS_CLARO = [['marinho', 'branco', 'royal', 'branco'], ['royal', 'gelo', 'marinho', 'gelo']]
ESQUEMAS_ESCURO = [['branco', 'marinho', 'branco', 'royal'], ['gelo', 'royal', 'gelo', 'marinho'], ['branco', 'intermediario', 'gelo', 'marinho']]

lote1 = os.path.join(AQUI, 'lote1')
for n, p in enumerate(PUBS):
    pid = p['id']; doc = f"{pid} · {p['tema']}"
    if pid in ('P01', 'P02', 'P03', 'P04', 'P05', 'P06', 'P07', 'P08'):
        if p['formato'] != 'REELS':
            k_tot = len(p['cards']) if p['formato'] == 'CARROSSEL' else 1
            for k in range(k_tot):
                nm = nome_arq(p['data'], p['hora'], f'C{k + 1:02d}')
                shutil.copy(os.path.join(lote1, nm + '.svg'), os.path.join(OUT, nm + '.svg'))
                LOG['pecas'].append(nm)
        mot_s = DIR_LOTE1.get(pid)
    elif p['formato'] == 'REELS':
        mot_s = DIR_LOTE1.get(pid)
    else:
        tom, mot, pos, est = DIR[pid]
        mot_s = mot
        if p['formato'] == 'CARROSSEL':
            c0 = p['cards'][0]
            peca_feed(nome_arq(p['data'], p['hora'], 'C01'), doc + ' · capa', tom, n, c0['titulo'], c0.get('apoio', ''), c0.get('kicker'), 'capa', mot, pos, 'start')
            esq = (ESQUEMAS_CLARO if tom in ('branco', 'gelo') else ESQUEMAS_ESCURO)[n % (2 if tom in ('branco', 'gelo') else 3)]
            for k, c in enumerate(p['cards'][1:]):
                peca_feed(nome_arq(p['data'], p['hora'], f'C{k + 2:02d}'), doc + f' · card {k + 2:02d}', esq[k], n + k + 1,
                          c['titulo'], c['apoio'], None, 'interno', mot if est == 'barra' else None, 'base', 'start', est, k)
        else:
            c = p['cards'][0]
            alinhar = 'center' if (pos == 'fundo' and n % 2 == 0) else 'start'
            peca_feed(nome_arq(p['data'], p['hora'], 'C01'), doc + ' · card único', tom, n, c['titulo'], c['apoio'], c.get('kicker'), 'capa', mot, pos, alinhar)
    # Stories
    for s_i, s in enumerate(p['stories']):
        tom_s = ['vibrante', 'branco', 'marinho', 'gelo', 'royal', 'intermediario'][(n * 2 + s_i) % 6]
        peca_story(nome_arq(p['data'], s['hora'], f'S{s_i + 1:02d}'), doc + f' · story {s_i + 1:02d}', tom_s, n + s_i, s['texto'],
                   mot_s if s_i == 0 else None)

# P01: capa, 02 e 03 aprovados
for k, src in enumerate(['P01_capa', 'P01_C02', 'P01_C03']):
    shutil.copy(os.path.join(RAIZ, 'p01_carrossel', src + '.svg'), os.path.join(OUT, f'2026-11-27_0900_C{k + 1:02d}.svg'))

json.dump(LOG, open(os.path.join(AQUI, 'relatorio_qc.json'), 'w'), ensure_ascii=False, indent=1)
print('peças:', len(set(LOG['pecas'])) , 'svg na pasta:', len(os.listdir(OUT)))
print('exceções tipográficas:', len(LOG['excecoes']))
print('falhas de QC:', len(LOG['qc_falhas']))
for f in LOG['qc_falhas'][:40]: print('  ', f)
