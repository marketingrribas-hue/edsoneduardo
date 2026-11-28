#!/usr/bin/env python3
"""Produção integral EcoFiscal — gera os SVGs editáveis (Inkscape) de todas as
publicações do planejamento aprovado, no padrão da capa P01 aprovada.

Regras fixas: Montserrat Medium/Bold; capa e card único 128 px; título interno
120 px; complementar 60 px; degradê #20B4F5→#00D6DC→#00E6A0 nas letras
(versão escura no branco); logo oficial 400 px centralizada no rodapé."""
import json, os, re, sys, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base_svg import larg, espaco, estilo, esc, logo, LOGO_H

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, 'svg')
os.makedirs(SAIDA, exist_ok=True)
PUBS = json.load(open(os.path.join(AQUI, 'planejamento.json')))

X0, LARG = 90, 900
CAPA = dict(T=128, TL=136, TLS=-2.4)
INT = dict(T=120, TL=128, TLS=-2.3)
STO = dict(T=84, TL=96, TLS=-1.4)
A, AL, ALS = 60, 82, -0.6

# ---------------- destaques estratégicos ----------------
CHAVES = ['simples', 'icms', 'icms-st', 'ibs', 'cbs', 'pis', 'cofins', 'das', 'ncm', 'xml', 'erp', 'pgfn', 'receita',
          'irpj', 'csll', 'mt', 'split', 'payment', 'diferimento', 'isenção', 'transação', 'crédito', 'créditos', 'credor',
          'autuação', 'fisco', 'apuração', 'incentivo', 'benefício', 'parametrização', 'reforma', 'lucro', 'presumido',
          'real', 'agro', 'soja', 'estoque', 'substituição', 'devolução', 'contrato', 'margem', 'preço', 'fornecedor',
          'caixa', 'parcela', 'parcelas', 'acordo', 'desconto', 'recesso', 'notificações', 'honorários', 'diagnóstico',
          'natal', 'decisões', 'decisão', 'empresas', 'saldo', 'uf', 'trilha', 'escrituração', 'parecer', 'tributarista',
          'contador', 'especialidade', 'real', 'olhares', 'nota', 'mercadoria', 'destino', 'documental', '2026', '2027', 'imposto',
          'risco', 'rescindida', 'clientes', 'compra', 'dados', 'entregas', 'operação', 'operações', 'prova',
          'direito', 'dívida', 'negociação', 'feliz', 'boas']
LIGA = {'e', 'de', 'do', 'da', '-'}

def base(w):
    w = w.lower().strip('.,:;?!()"“”')
    return w

def destaques(palavras, maximo=2, ultimo_se_vazio=True):
    """Índices das palavras em destaque: trechos contíguos de termos-chave (até `maximo` trechos)."""
    idx = [i for i, p in enumerate(palavras)
           if (base(p) in CHAVES and base(p) != 'real') or (base(p) == 'real' and i and base(palavras[i - 1]) == 'lucro')]
    trechos, cur = [], []
    for i in idx:
        if cur and (i == cur[-1] + 1 or (i == cur[-1] + 2 and base(palavras[i - 1]) in LIGA)):
            cur += list(range(cur[-1] + 1, i + 1))
        else:
            if cur: trechos.append(cur)
            cur = [i]
    if cur: trechos.append(cur)
    # prioriza os trechos mais longos e, em empate, os mais ao fim da frase
    trechos.sort(key=lambda t: (len(t), t[-1]), reverse=True)
    trechos = trechos[:maximo]
    if not trechos and ultimo_se_vazio:
        trechos = [[len(palavras) - 1]]
    return {i for t in trechos for i in t}

# ---------------- composição tipográfica ----------------
def quebrar(palavras, marcados, T, TLS, forcar_quebra=False):
    linhas, atual, w = [], [], 0
    for i, p in enumerate(palavras):
        peso = 700 if i in marcados else 500
        wp = larg(p, peso, T, TLS)
        sp = espaco(peso, T, TLS) if atual else 0
        quebra = atual and (w + sp + wp > LARG)
        if forcar_quebra and atual and (i in marcados) != (atual[-1][0] in marcados):
            quebra = True
        if quebra:
            linhas.append(atual); atual, w, sp = [], 0, 0
        atual.append((i, p, peso, wp)); w += sp + wp
    if atual: linhas.append(atual)
    return linhas

def render_titulo(linhas, marcados, x0, y0, T, TL, TLS, cor, grad, alinhar='start'):
    out = []
    for n, ln in enumerate(linhas):
        y = y0 + n * TL
        # agrupa palavras vizinhas do mesmo estilo num único <text> editável
        grupos = []
        for i, p, peso, wp in ln:
            m = i in marcados
            if grupos and grupos[-1][0] == m: grupos[-1][1].append((p, peso, wp))
            else: grupos.append([m, [(p, peso, wp)]])
        tot = sum(wp for _, _, _, wp in ln) + sum(espaco(pe, T, TLS) for _, _, pe, _ in ln[:-1])
        x = x0 if alinhar == 'start' else x0 + (LARG - tot) / 2
        for m, ws in grupos:
            txt = ' '.join(p for p, _, _ in ws)
            peso = ws[0][1]
            out.append(f'<text xml:space="preserve" x="{x:.1f}" y="{y:.1f}" style="{estilo(peso, T, TLS)};fill:{grad if m else cor}">{esc(txt)}</text>')
            x += larg(txt, peso, T, TLS) + espaco(peso, T, TLS)
    return '\n'.join(out)

def quebrar_apoio(texto, marcados_apoio):
    palavras = texto.split()
    return palavras, quebrar(palavras, marcados_apoio, A, ALS)

def render_apoio(palavras, linhas, marcados, x0, y0, cor, cor_dest, alinhar='start'):
    out = []
    for n, ln in enumerate(linhas):
        y = y0 + n * AL
        tot = sum(wp for _, _, _, wp in ln) + sum(espaco(pe, A, ALS) for _, _, pe, _ in ln[:-1])
        x = x0 if alinhar == 'start' else x0 + (LARG - tot) / 2
        spans = []
        for k, (i, p, peso, wp) in enumerate(ln):
            fim = ' ' if k < len(ln) - 1 else ''
            c = cor_dest if i in marcados else cor
            spans.append(f'<tspan style="font-weight:{peso};-inkscape-font-specification:\'Montserrat {"Bold" if peso == 700 else "Medium"}\';fill:{c}">{esc(p + fim)}</tspan>')
        out.append(f'<text xml:space="preserve" x="{x:.1f}" y="{y:.1f}" style="{estilo(500, A, ALS)}">{"".join(spans)}</text>')
    return '\n'.join(out)

# ---------------- famílias de fundo ----------------
DEFS_COMUNS = '''<linearGradient id="degrade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#20B4F5"/><stop offset="0.5" stop-color="#00D6DC"/><stop offset="1" stop-color="#00E6A0"/></linearGradient>
  <linearGradient id="degradeClaro" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#1287D4"/><stop offset="0.5" stop-color="#00A3B4"/><stop offset="1" stop-color="#00A47E"/></linearGradient>'''

LUZES = [(0.85, 0.12), (0.12, 0.15), (0.88, 0.55), (0.15, 0.85), (0.6, 0.05)]

def fundo(familia, var, H):
    lx, ly = LUZES[var % len(LUZES)]
    if familia == 'branco':
        defs = f'''<linearGradient id="f" x1="0" y1="0" x2="0.4" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#EEF2F8"/></linearGradient>
  <radialGradient id="l1" cx="{lx}" cy="{ly}" r="0.7"><stop offset="0" stop-color="#1246C9" stop-opacity="0.15"/><stop offset="0.55" stop-color="#20B4F5" stop-opacity="0.06"/><stop offset="1" stop-color="#20B4F5" stop-opacity="0"/></radialGradient>
  <radialGradient id="l2" cx="{1-lx}" cy="{1-ly}" r="0.55"><stop offset="0" stop-color="#00D6DC" stop-opacity="0.12"/><stop offset="1" stop-color="#00D6DC" stop-opacity="0"/></radialGradient>'''
        corpo = f'<rect width="1080" height="{H}" fill="url(#f)"/><rect width="1080" height="{H}" fill="url(#l1)"/><rect width="1080" height="{H}" fill="url(#l2)"/>'
        return defs, corpo, 'claro'
    paleta = {
        'marinho': ('#0B3A9E', '#092653', '#071F48', '#0865EE', 0.30),
        'royal': ('#1246C9', '#0B3A9E', '#092653', '#0865EE', 0.32),
        'vibrante': ('#0865EE', '#1246C9', '#0A2E86', '#20B4F5', 0.26),
    }[familia]
    c0, c1, c2, cl, op = paleta
    defs = f'''<linearGradient id="f" x1="0.2" y1="0" x2="0.5" y2="1"><stop offset="0" stop-color="{c0}"/><stop offset="0.55" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>
  <radialGradient id="l1" cx="{lx}" cy="{ly}" r="0.65"><stop offset="0" stop-color="{cl}" stop-opacity="{op}"/><stop offset="1" stop-color="{cl}" stop-opacity="0"/></radialGradient>
  <linearGradient id="b" x1="0" y1="0" x2="0" y2="1"><stop offset="0.72" stop-color="#092653" stop-opacity="0"/><stop offset="1" stop-color="#092653" stop-opacity="0.85"/></linearGradient>'''
    corpo = f'<rect width="1080" height="{H}" fill="url(#f)"/><rect width="1080" height="{H}" fill="url(#l1)"/><rect width="1080" height="{H}" fill="url(#b)"/>'
    return defs, corpo, 'escuro'

def documento(titulo_doc, H, defs, fundo_svg, camadas, logo_y):
    lg = logo().replace(f'y="{1350 - 50 - LOGO_H}"', f'y="{logo_y}"')
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
     width="1080" height="{H}" viewBox="0 0 1080 {H}">
<title>{esc(titulo_doc)}</title>
<defs>
  {DEFS_COMUNS}
  {defs}
</defs>
<g inkscape:groupmode="layer" inkscape:label="Fundo">{fundo_svg}</g>
{camadas}
{lg}
</svg>'''

# ---------------- montagem de uma peça ----------------
def peca(nome, titulo_doc, tipo, familia, var, titulo, apoio='', kicker=None, layout='centro'):
    for aperto in range(6):
        e = _peca(nome, titulo_doc, tipo, familia, var, titulo, apoio, kicker, layout, aperto)
        if e <= 0:
            return e
    return e

def _peca(nome, titulo_doc, tipo, familia, var, titulo, apoio, kicker, layout, aperto):
    H = 1920 if tipo == 'story' else 1350
    spec = {'capa': CAPA, 'unico': CAPA, 'interno': INT, 'story': STO}[tipo]
    T, TL, TLS = spec['T'], spec['TL'], spec['TLS']
    global AL
    AL = 82
    # reorganização progressiva (sem reduzir a fonte): entrelinhas, espaçamentos e margens
    TL -= 3 * aperto
    AL = 82 - 2 * aperto
    defs, fsvg, tom = fundo(familia, var, H)
    claro = tom == 'claro'
    cor_t = '#092653' if claro else '#FFFFFF'
    grad = 'url(#degradeClaro)' if claro else 'url(#degrade)'
    cor_a = '#1C2F52' if claro else '#E8EFF9'
    cor_ad = '#0A6FB8' if claro else '#FFFFFF'

    pal = titulo.split()
    if tipo == 'interno':
        marc = destaques(pal, maximo=1)
        prefixo = [w for i, w in enumerate(pal) if i not in marc]
        forcar = len(pal) <= 4 and len(prefixo) >= 2 and all(i not in marc for i in range(len(prefixo)))
    else:
        marc = destaques(pal, maximo=2)
        forcar = False
    lt = quebrar(pal, marc, T, TLS, forcar_quebra=forcar)

    pa, la, marc_a = [], [], set()
    if apoio:
        pa = apoio.split()
        marc_a = destaques(pa, maximo=1, ultimo_se_vazio=False)
        la = quebrar(pa, marc_a, A, ALS)

    gap = (140 if tipo == 'interno' else 122) - 10 * aperto
    if tipo == 'story':
        gap = 120
    altura = 0.74 * T + (len(lt) - 1) * TL + ((gap + (len(la) - 1) * AL + 0.22 * A) if la else 0.22 * T)
    k_h = 90 if kicker else 0
    if tipo == 'story':
        topo_min, base_max = 470, 1150          # área livre para sticker abaixo do texto
        logo_y = H - 230 - LOGO_H
    else:
        topo_min, base_max = 110 - 15 * aperto, 1350 - 50 - LOGO_H - 48 + 8 * aperto
        logo_y = 1350 - 50 - LOGO_H
    livre = base_max - topo_min
    if layout == 'topo' or tipo == 'story':
        inicio = topo_min + 40
    elif layout == 'base':
        inicio = base_max - altura - k_h
    else:
        inicio = topo_min + (livre - altura - k_h) / 2
    inicio = max(topo_min, inicio)
    estouro = inicio + k_h + altura - base_max
    y1 = inicio + k_h + 0.74 * T

    camadas = []
    if kicker:
        camadas.append(f'<g inkscape:groupmode="layer" inkscape:label="Chamada"><text x="{X0}" y="{y1 - T * 0.74 - 34:.1f}" style="{estilo(700, 40, 8)};fill:{grad}">{esc(kicker)}</text></g>')
    camadas.append(f'<g inkscape:groupmode="layer" inkscape:label="Título · {T} px">\n{render_titulo(lt, marc, X0, y1, T, TL, TLS, cor_t, grad)}\n</g>')
    if la:
        ya = y1 + (len(lt) - 1) * TL + gap
        camadas.append(f'<g inkscape:groupmode="layer" inkscape:label="Texto complementar · {A} px">\n{render_apoio(pa, la, marc_a, X0, ya, cor_a, cor_ad)}\n</g>')
    svg = documento(titulo_doc, H, defs, fsvg, '\n'.join(camadas), logo_y)
    open(os.path.join(SAIDA, nome + '.svg'), 'w').write(svg)
    return estouro

# ---------------- plano de famílias (alternância do feed) ----------------
CICLO_CAPA = ['royal', 'branco', 'marinho', 'vibrante', 'branco', 'royal', 'marinho', 'branco', 'vibrante']
LAYOUTS = ['topo', 'centro', 'base']

def nome_arquivo(data, hora, sufixo):
    d, m, a = data.split('/')
    hh = hora.replace('h', '')
    hh = (hh[:2] + (hh[2:] if len(hh) > 2 else '00')).ljust(4, '0')
    return f'{a}-{m}-{d}_{hh}_{sufixo}'

relatorio = {'estouros': [], 'reels': [], 'pecas': 0}
for n, p in enumerate(PUBS):
    fam = CICLO_CAPA[n % len(CICLO_CAPA)]
    lay = LAYOUTS[n % len(LAYOUTS)]
    doc_base = f"{p['id']} · {p['tema']}"
    if p['formato'] == 'REELS':
        relatorio['reels'].append(p['id'])
    elif p['formato'] == 'CARROSSEL':
        if p['id'] == 'P01':
            fams_int = ['branco', 'royal', 'branco', 'marinho']   # 02 e 03 já aprovados
        else:
            claro_capa = fam == 'branco'
            fams_int = ['marinho' if claro_capa else 'branco', 'branco' if claro_capa else 'royal',
                        'royal' if claro_capa else 'branco', 'branco' if claro_capa else 'marinho']
        for k, c in enumerate(p['cards']):
            nome = nome_arquivo(p['data'], p['hora'], f'C{k + 1:02d}')
            if p['id'] == 'P01' and k < 3:
                continue   # capa, 02 e 03 aprovados: copiados sem alteração
            if k == 0:
                e = peca(nome, doc_base + ' · capa', 'capa', fam, n, c['titulo'], c.get('apoio', ''), c.get('kicker'), lay)
            else:
                e = peca(nome, doc_base + f' · card {k + 1:02d}', 'interno', fams_int[k - 1], n + k, c['titulo'], c['apoio'])
            relatorio['pecas'] += 1
            if e > 0: relatorio['estouros'].append((nome, round(e)))
    else:
        c = p['cards'][0]
        nome = nome_arquivo(p['data'], p['hora'], 'C01')
        e = peca(nome, doc_base + ' · card único', 'unico', fam, n, c['titulo'], c['apoio'], c.get('kicker'), 'centro')
        relatorio['pecas'] += 1
        if e > 0: relatorio['estouros'].append((nome, round(e)))
    # stories (somente o texto; o sticker nativo é aplicado depois no Instagram)
    for s_i, s in enumerate(p['stories']):
        nome = nome_arquivo(p['data'], s['hora'], f'S{s_i + 1:02d}')
        fam_s = ['vibrante', 'branco', 'marinho', 'royal'][(n * 2 + s_i) % 4]
        e = peca(nome, doc_base + f' · story {s_i + 1:02d}', 'story', fam_s, n + s_i, s['texto'])
        relatorio['pecas'] += 1
        if e > 0: relatorio['estouros'].append((nome, round(e)))

json.dump(relatorio, open(os.path.join(AQUI, 'relatorio_geracao.json'), 'w'), ensure_ascii=False, indent=1)
print('peças:', relatorio['pecas'], '| estouros:', relatorio['estouros'], '| reels:', relatorio['reels'])
