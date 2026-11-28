#!/usr/bin/env python3
"""Lê o PDF do planejamento aprovado e extrai, sem reescrever, o conteúdo de cada publicação."""
import json, re, sys, pymupdf

PDF = sys.argv[1]; OUT = sys.argv[2]
doc = pymupdf.open(PDF)
linhas = []  # (pagina, bloco, tamanho, negrito, texto)
for pno, p in enumerate(doc):
    for bi, b in enumerate(p.get_text('dict')['blocks']):
        for l in b.get('lines', []):
            txt = ''.join(s['text'] for s in l['spans']).strip()
            if not txt: continue
            s0 = l['spans'][0]
            linhas.append((pno, bi, round(s0['size']), 'Bold' in s0['font'], txt))

pubs, atual, secao, card = [], None, None, None
HDR = re.compile(r'^P(\d{2}) / (\d{2}/\d{2}/2026) / (\d{2}h\d*)(?: / (.+))?$')
def add_par(lst, bloco, txt):
    if lst and lst[-1][0] == bloco: lst[-1][1].append(txt)
    else: lst.append([bloco, [txt]])
for pno, bi, sz, bold, txt in linhas:
    if txt.startswith('ECOFISCAL MT  /') or re.fullmatch(r'\d{1,3}', txt): continue
    m = HDR.match(txt)
    if m and sz == 10:
        if not m.group(4):
            secao = 'producao'
        if m.group(4):
            atual = dict(id='P'+m.group(1), data=m.group(2), hora=m.group(3), formato=m.group(4).strip(),
                         tema=None, publico=None, cards=[], direcao=[], legenda=[], stories=[], validacao=[], roteiro=[])
            pubs.append(atual); secao = 'topo'
        continue
    if atual is None: continue
    if sz == 10 and bold:
        u = txt.upper()
        if 'RÓTULO INTERNO' in u:
            card = dict(rotulo=txt.split(' / ')[0], tit=[], apoio=[]); atual['cards'].append(card); secao = 'card'
        elif u.startswith('DIREÇÃO VISUAL'): secao = 'direcao'
        elif u.startswith('LEGENDA'): secao = 'legenda'
        elif u.startswith('STORIES'): secao = 'stories'
        elif u.startswith('VALIDAÇÃO'): secao = 'validacao'
        elif u.startswith('ROTEIRO'): secao = 'roteiro'
        elif u.startswith('TEXTO FINAL'): secao = 'texto'
        continue
    if secao == 'producao': continue
    if secao == 'topo':
        if sz == 24: atual['tema'] = (atual['tema'] + ' ' + txt) if atual['tema'] else txt
        elif sz == 12: atual['publico'] = txt
        continue
    if secao == 'card':
        if sz >= 17: add_par(card['tit'], (pno, bi), txt)
        else: add_par(card['apoio'], (pno, bi), txt)
    elif secao == 'stories':
        if txt.startswith('Sticker/recurso:'): atual['stories'][-1]['sticker'] = txt.split(':', 1)[1].strip()
        elif re.match(r'^\d{2}h(\d{2})? — ', txt): h, t = txt.split(' — ', 1); atual['stories'].append(dict(hora=h, texto=t))
        elif atual['stories']: atual['stories'][-1]['texto'] += ' ' + txt
    elif secao in ('direcao', 'legenda', 'validacao', 'roteiro'):
        atual[secao].append(txt)
    elif secao == 'roteiro_falado':
        atual['roteiro'].append(txt)

def junta(ls): return ' '.join(ls).replace('  ', ' ').strip()
for p in pubs:
    for c in p['cards']:
        pars = [junta(x[1]) for x in c['tit']]
        # capas/arte única: 1º parágrafo grande = título; os demais grandes viram apoio
        c['titulo'] = pars[0] if pars else ''
        extra = pars[1:]
        c['apoio'] = ' '.join(extra + [junta(x[1]) for x in c['apoio']]).strip()
        del c['tit']
        # caso aprovado do P01: 2ª frase da capa é o texto complementar
    if p['id'] == 'P01':
        c0 = p['cards'][0]; c0['titulo'], c0['apoio'] = 'Seu cliente do Simples vende para empresas?', 'A escolha de 2027 merece atenção.'
    for c in p['cards']:
        if c['titulo'].startswith('MASTERCLASS '):
            c['kicker'] = 'MASTERCLASS'; c['titulo'] = c['titulo'][len('MASTERCLASS '):]
    for k in ('direcao', 'legenda', 'validacao', 'roteiro'): p[k] = junta(p[k])
json.dump(pubs, open(OUT, 'w'), ensure_ascii=False, indent=1)
print(len(pubs), sum(len(p['cards']) for p in pubs), sum(len(p['stories']) for p in pubs))
