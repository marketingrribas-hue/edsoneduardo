#!/usr/bin/env python3
"""Três propostas de capa para o P01, em SVG vetorial editável (Inkscape).
Mesmo texto aprovado; composições distintas. Sem novas gerações de imagem."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base_svg import linha, svg, b64, G, BR, AQUI as _A

AQUI = os.path.dirname(os.path.abspath(__file__))
TXT = '#FFFFFF'
APOIO = '#E6EEF9'

# Mapa de degradê (duotone) editável: escuro #061A38 → médio #0865EE → claro #BFE9FF
DUOTONE = '''
<filter id="duotone" color-interpolation-filters="sRGB">
  <feColorMatrix type="saturate" values="0"/>
  <feComponentTransfer>
    <feFuncR type="table" tableValues="0.024 0.031 0.749"/>
    <feFuncG type="table" tableValues="0.102 0.396 0.914"/>
    <feFuncB type="table" tableValues="0.220 0.933 1"/>
  </feComponentTransfer>
</filter>'''

def titulo(linhas, x0, base, sz, lh, ls, alinhar, area):
    out = []
    for i, segs in enumerate(linhas):
        s, _ = linha(segs, x0, base + i * lh, sz, ls, alinhar, area)
        out.append(s)
    return '\n'.join(out)

TIT_3 = [[('Seu cliente do', 400, TXT)],
         [('Simples', 700, G), ('vende', 400, TXT)],
         [('para', 400, TXT), ('empresas?', 700, G)]]
TIT_4 = [[('Seu cliente do', 400, TXT)],
         [('Simples', 700, G)],
         [('vende para', 400, TXT)],
         [('empresas?', 700, G)]]
AP = [[('A escolha de', 500, APOIO), ('2027', 700, G)],
      [('merece atenção.', 500, APOIO)]]

# ============ PROPOSTA A — estrutura da referência do relógio: azul vibrante, tipografia à esquerda, objeto fotográfico monocromático integrado ============
foto_dec = b64(os.path.join(AQUI, 'foto_decisao.jpg'), 'image/jpeg')
A = svg('P01 · Capa · Proposta A', DUOTONE + '''
<linearGradient id="fundoA" x1="0.1" y1="0" x2="0.6" y2="1">
  <stop offset="0" stop-color="#0A5EE0"/><stop offset="0.45" stop-color="#0865EE"/>
  <stop offset="0.78" stop-color="#1246C9"/><stop offset="1" stop-color="#0A2F86"/>
</linearGradient>
<radialGradient id="luzA" cx="0.18" cy="0.12" r="0.6">
  <stop offset="0" stop-color="#4FC3FF" stop-opacity="0.18"/><stop offset="1" stop-color="#4FC3FF" stop-opacity="0"/>
</radialGradient>
<radialGradient id="mascaraFotoA" cx="0.55" cy="0.58" r="0.5">
  <stop offset="0.35" stop-color="#fff"/><stop offset="1" stop-color="#000"/>
</radialGradient>
<mask id="mA"><rect x="120" y="560" width="1080" height="720" fill="url(#mascaraFotoA)"/></mask>
<linearGradient id="baseA" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#092653" stop-opacity="0"/><stop offset="1" stop-color="#092653" stop-opacity="0.9"/>
</linearGradient>''', f'''
<g inkscape:groupmode="layer" inkscape:label="Fundo azul vibrante">
  <rect width="1080" height="1350" fill="url(#fundoA)"/>
  <rect width="1080" height="1350" fill="url(#luzA)"/>
</g>
<g inkscape:groupmode="layer" inkscape:label="Fotografia · decisão (monocromática)">
  <g mask="url(#mA)" opacity="0.92">
    <image x="120" y="560" width="1080" height="720" preserveAspectRatio="xMidYMid slice" filter="url(#duotone)" xlink:href="{foto_dec}" href="{foto_dec}" style="mix-blend-mode:screen"/>
  </g>
  <rect x="0" y="1060" width="1080" height="290" fill="url(#baseA)"/>
</g>
<g inkscape:groupmode="layer" inkscape:label="Título · 106 px">
{titulo(TIT_3, 90, 230, 106, 116, -2, 'start', None)}
</g>
<g inkscape:groupmode="layer" inkscape:label="Apoio · 60 px">
{titulo(AP, 90, 230 + 2*116 + 116, 60, 80, -0.6, 'start', None)}
</g>''')
open(os.path.join(AQUI, 'P01_capa_proposta_A.svg'), 'w').write(A)

# ============ PROPOSTA B — tipografia protagonista, sofisticação de contraste (estrutura editorial escura → vibrante) ============
grade = '\n'.join(f'<line x1="{x}" y1="0" x2="{x}" y2="1350"/>' for x in range(90, 1080, 150)) + '\n' + \
        '\n'.join(f'<line x1="0" y1="{y}" x2="1080" y2="{y}"/>' for y in range(75, 1350, 150))
B = svg('P01 · Capa · Proposta B', '''
<linearGradient id="fundoB" x1="1" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#0865EE"/><stop offset="0.45" stop-color="#1246C9"/>
  <stop offset="0.80" stop-color="#092653"/><stop offset="1" stop-color="#061A38"/>
</linearGradient>
<linearGradient id="feixe" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#20B4F5" stop-opacity="0"/><stop offset="0.5" stop-color="#20B4F5" stop-opacity="0.35"/><stop offset="1" stop-color="#00E6A0" stop-opacity="0"/>
</linearGradient>
<radialGradient id="mascaraGrade" cx="0.75" cy="0.2" r="0.75">
  <stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/>
</radialGradient>
<mask id="mB"><rect width="1080" height="1350" fill="url(#mascaraGrade)"/></mask>
<filter id="desfoqueB" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="40"/></filter>''', f'''
<g inkscape:groupmode="layer" inkscape:label="Fundo">
  <rect width="1080" height="1350" fill="url(#fundoB)"/>
</g>
<g inkscape:groupmode="layer" inkscape:label="Textura · grade discreta">
  <g mask="url(#mB)" stroke="#FFFFFF" stroke-opacity="0.07" stroke-width="1.5">
{grade}
  </g>
</g>
<g inkscape:groupmode="layer" inkscape:label="Feixes de luz">
  <rect x="-200" y="250" width="1500" height="70" fill="url(#feixe)" transform="rotate(-28 540 675)" filter="url(#desfoqueB)"/>
  <rect x="-200" y="430" width="1500" height="24" fill="url(#feixe)" transform="rotate(-28 540 675)" opacity="0.8"/>
</g>
<g inkscape:groupmode="layer" inkscape:label="Fio em degradê">
  <rect x="90" y="290" width="160" height="8" rx="4" fill="url(#degrade)"/>
</g>
<g inkscape:groupmode="layer" inkscape:label="Título · 124 px">
{titulo(TIT_4, 90, 440, 124, 132, -2.4, 'start', None)}
</g>
<g inkscape:groupmode="layer" inkscape:label="Apoio · 60 px">
{titulo(AP, 90, 440 + 3*132 + 120, 60, 80, -0.6, 'start', None)}
</g>''')
open(os.path.join(AQUI, 'P01_capa_proposta_B.svg'), 'w').write(B)

# ============ PROPOSTA C — fotografia integrada em tela cheia (estrutura da capa do Renato), tratada em azul vibrante, texto centralizado ============
foto_op = b64(os.path.join(AQUI, 'foto_operacao.jpg'), 'image/jpeg')
C = svg('P01 · Capa · Proposta C', DUOTONE + '''
<linearGradient id="vibC" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#0865EE" stop-opacity="0.35"/><stop offset="0.38" stop-color="#0865EE" stop-opacity="0.10"/>
  <stop offset="0.55" stop-color="#1246C9" stop-opacity="0.70"/><stop offset="0.72" stop-color="#0B2F86" stop-opacity="0.95"/>
  <stop offset="1" stop-color="#092653" stop-opacity="1"/>
</linearGradient>
<radialGradient id="brilhoC" cx="0.5" cy="0.32" r="0.45">
  <stop offset="0" stop-color="#20B4F5" stop-opacity="0.35"/><stop offset="1" stop-color="#20B4F5" stop-opacity="0"/>
</radialGradient>''', f'''
<g inkscape:groupmode="layer" inkscape:label="Fotografia · operação empresarial (tratada em azul)">
  <rect width="1080" height="1350" fill="#0865EE"/>
  <image x="-470" y="0" width="2025" height="1350" preserveAspectRatio="xMidYMid slice" filter="url(#duotone)" xlink:href="{foto_op}" href="{foto_op}"/>
</g>
<g inkscape:groupmode="layer" inkscape:label="Tratamento de cor">
  <rect width="1080" height="1350" fill="url(#brilhoC)"/>
  <rect width="1080" height="1350" fill="url(#vibC)"/>
</g>
<g inkscape:groupmode="layer" inkscape:label="Título · 106 px">
{titulo(TIT_3, 0, 720, 106, 116, -2, 'center', 1080)}
</g>
<g inkscape:groupmode="layer" inkscape:label="Apoio · 60 px">
{titulo(AP, 0, 720 + 2*116 + 112, 60, 80, -0.6, 'center', 1080)}
</g>''')
open(os.path.join(AQUI, 'P01_capa_proposta_C.svg'), 'w').write(C)
print('ok')
