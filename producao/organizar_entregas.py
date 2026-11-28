#!/usr/bin/env python3
"""Organiza as artes exportadas em pastas por semana/data/publicação, gera legendas,
PDF semanal (uma arte por página), prévia do feed e ZIP por semana."""
import json, os, shutil, zipfile, glob
from datetime import date
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SVG = os.path.join(AQUI, 'svg')
ENT = os.path.join(RAIZ, 'entregas_ecofiscal')
PUBS = json.load(open(os.path.join(AQUI, 'planejamento.json')))

SEMANAS = [('semana_01_27nov-03dez', date(2026, 11, 27), date(2026, 12, 3)),
           ('semana_02_04dez-10dez', date(2026, 12, 4), date(2026, 12, 10)),
           ('semana_03_11dez-17dez', date(2026, 12, 11), date(2026, 12, 17)),
           ('semana_04_18dez-24dez', date(2026, 12, 18), date(2026, 12, 24)),
           ('semana_05_25dez-31dez', date(2026, 12, 25), date(2026, 12, 31))]

# P01: capa e cards 02/03 aprovados, preservados sem alteração
APROVADOS = {
    '2026-11-27_0900_C01': os.path.join(RAIZ, 'p01_carrossel', 'P01_capa'),
    '2026-11-27_0900_C02': os.path.join(RAIZ, 'p01_carrossel', 'P01_C02'),
    '2026-11-27_0900_C03': os.path.join(RAIZ, 'p01_carrossel', 'P01_C03'),
}

def dt(p):
    d, m, a = p['data'].split('/')
    return date(int(a), int(m), int(d))

def nome(data, hora, suf):
    d, m, a = data.split('/')
    hh = hora.replace('h', ''); hh = (hh[:2] + (hh[2:] if len(hh) > 2 else '00')).ljust(4, '0')
    return f'{a}-{m}-{d}_{hh}_{suf}'

if os.path.isdir(ENT): shutil.rmtree(ENT)
pendencias = []
for sem, ini, fim in SEMANAS:
    base_sem = os.path.join(ENT, sem)
    feed, todas, md = [], [], [f'# EcoFiscal MT — legendas e publicação · {sem.replace("_", " ")}\n']
    for p in [x for x in PUBS if ini <= dt(x) <= fim]:
        d, m, a = p['data'].split('/')
        pasta = os.path.join(base_sem, f'{a}-{m}-{d}', f"{p['id']}_{p['hora']}_{p['formato'].replace(' ', '-').lower()}")
        os.makedirs(pasta, exist_ok=True)
        arquivos = []
        if p['formato'] == 'REELS':
            pendencias.append(f"{p['id']} ({p['data']} {p['hora']}) — Reels: o planejamento pede vídeo original do André com legendas sincronizadas e proíbe arte estática; aguardando o vídeo.")
        else:
            n = len(p['cards']) if p['formato'] == 'CARROSSEL' else 1
            for k in range(n):
                nm = nome(p['data'], p['hora'], f'C{k + 1:02d}')
                src = APROVADOS.get(nm, os.path.join(SVG, nm))
                for ext in ('png', 'svg'):
                    shutil.copy(f'{src}.{ext}', os.path.join(pasta, f'{nm}.{ext}'))
                arquivos.append(os.path.join(pasta, nm + '.png'))
            feed.append(arquivos[0])
        stories = []
        for s_i, s in enumerate(p['stories']):
            nm = nome(p['data'], s['hora'], f'S{s_i + 1:02d}')
            for ext in ('png', 'svg'):
                shutil.copy(os.path.join(SVG, f'{nm}.{ext}'), os.path.join(pasta, f'{nm}.{ext}'))
            stories.append(os.path.join(pasta, nm + '.png'))
        todas += arquivos + stories
        # legenda e instruções de publicação
        leg = [f"{p['id']} · {p['data']} · {p['hora']} · {p['formato']}", f"Tema: {p['tema']}", f"Público: {p['publico']}", '',
               'LEGENDA', p['legenda'] or '(sem legenda no planejamento)', '']
        if p['roteiro']:
            leg += ['ROTEIRO FALADO (Reels — vídeo original do André)', p['roteiro'], '']
        leg += ['STORIES']
        for s_i, s in enumerate(p['stories']):
            leg.append(f"S{s_i + 1:02d} · {s['hora']} — {s['texto']}  [sticker nativo a aplicar no Instagram: {s.get('sticker', '-')}]")
        leg += ['', 'VALIDAÇÃO TÉCNICA (interno, não publicar)', p['validacao'] or '-']
        open(os.path.join(pasta, 'legenda.txt'), 'w').write('\n'.join(leg) + '\n')
        md += [f"## {p['id']} · {p['data']} · {p['hora']} · {p['formato']} — {p['tema']}", '', '**Legenda:** ' + (p['legenda'] or '-'), '']
        for s_i, s in enumerate(p['stories']):
            md.append(f"- **Story S{s_i + 1:02d} · {s['hora']}:** {s['texto']} _(sticker: {s.get('sticker', '-')})_")
        md += ['', '**Validação técnica (interno):** ' + (p['validacao'] or '-'), '']
    os.makedirs(base_sem, exist_ok=True)
    open(os.path.join(base_sem, 'LEGENDAS.md'), 'w').write('\n'.join(md))
    # PDF semanal: uma arte por página
    imgs = [Image.open(f).convert('RGB') for f in todas]
    if imgs:
        imgs[0].save(os.path.join(base_sem, f'{sem}_artes.pdf'), save_all=True, append_images=imgs[1:], resolution=96)
    # prévia do feed (ordem do Instagram: mais recente no alto à esquerda)
    capas = list(reversed(feed)); W, H = 360, 450
    lin = (len(capas) + 2) // 3
    grade = Image.new('RGB', (3 * W + 4 * 6, lin * (H + 6) + 6), '#FFFFFF')
    for i, f in enumerate(capas):
        grade.paste(Image.open(f).convert('RGB').resize((W, H)), (6 + (i % 3) * (W + 6), 6 + (i // 3) * (H + 6)))
    grade.save(os.path.join(base_sem, f'{sem}_previa_feed.png'))
    # prévias das sequências de cada carrossel
    for pasta in glob.glob(os.path.join(base_sem, '*', '*carrossel*')):
        cards = sorted(glob.glob(os.path.join(pasta, '*_C*.png')))
        seq = Image.new('RGB', (len(cards) * 366 + 6, 462), '#FFFFFF')
        for i, f in enumerate(cards):
            seq.paste(Image.open(f).convert('RGB').resize((360, 450)), (6 + i * 366, 6))
        seq.save(os.path.join(pasta, 'previa_sequencia.png'))
    # ZIP da semana
    with zipfile.ZipFile(os.path.join(ENT, f'{sem}.zip'), 'w', zipfile.ZIP_DEFLATED) as z:
        for r, _, fs in os.walk(base_sem):
            for f in fs:
                z.write(os.path.join(r, f), os.path.relpath(os.path.join(r, f), ENT))
    print(sem, 'feed', len(feed), 'arquivos', len(todas))

open(os.path.join(ENT, 'PENDENCIAS.md'), 'w').write('# Pendências\n\n' + '\n'.join('- ' + x for x in pendencias) + '\n')
# fontes e instruções
shutil.copytree(os.path.join(AQUI, 'fontes'), os.path.join(ENT, 'fontes_montserrat'))
shutil.copy(os.path.join(AQUI, 'LEIA-ME_entregas.md'), os.path.join(ENT, 'LEIA-ME.md'))
print('pendências:', len(pendencias))
