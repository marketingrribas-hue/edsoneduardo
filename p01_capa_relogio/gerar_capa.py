#!/usr/bin/env python3
"""Capa P01 — estrutura da referência do relógio azul.
SVG vetorial editável (Inkscape): texto real em Montserrat, degradê contínuo
aplicado no preenchimento de todo o título, objeto fotográfico à direita."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base_svg import larg, espaco, estilo, esc, b64, logo, AQUI

AQUI = os.path.dirname(os.path.abspath(__file__))
OBJ = b64(os.path.join(AQUI, 'calendario_2027.jpg'), 'image/jpeg')

T, TL, TLS = 106, 116, -2      # título da capa
A, AL, ALS = 60, 80, -0.6      # texto complementar
X0 = 90

def linha_titulo(segs, base):
    """Cada trecho é um <text>; todos usam o MESMO degradê em coordenadas da página,
    de modo que a transição atravessa o bloco inteiro, como na referência."""
    x, out = X0, []
    for k, (t, w) in enumerate(segs):
        out.append(f'<text xml:space="preserve" x="{x:.1f}" y="{base}" style="{estilo(w, T, TLS)};fill:url(#degradeTitulo)">{esc(t)}</text>')
        x += larg(t, w, T, TLS) + espaco(w, T, TLS)
    return '\n'.join(out), x - X0

linhas = [[('Seu cliente do', 500)],
          [('Simples', 700), ('vende', 500)],
          [('para', 500), ('empresas?', 700)]]
b0 = 236
tit, largs = [], []
for i, segs in enumerate(linhas):
    s, w = linha_titulo(segs, b0 + i * TL)
    tit.append(s); largs.append(w)
x_fim = X0 + max(largs)

def linha_apoio(segs, base):
    x, out = X0, []
    for t, w in segs:
        out.append(f'<text xml:space="preserve" x="{x:.1f}" y="{base}" style="{estilo(w, A, ALS)};fill:#FFFFFF">{esc(t)}</text>')
        x += larg(t, w, A, ALS) + espaco(w, A, ALS)
    return '\n'.join(out)

a0 = b0 + 2 * TL + 128
apoio = '\n'.join([linha_apoio([('A escolha de', 400)], a0),
                   linha_apoio([('2027', 700), ('merece', 400)], a0 + AL),
                   linha_apoio([('atenção.', 400)], a0 + 2 * AL)])

# objeto: calendário em escala 0.92, deslocado para a direita
S, OX, OY = 0.92, 223, 158
W, H = 1080 * S, 1350 * S

svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
     width="1080" height="1350" viewBox="0 0 1080 1350">
<title>P01 · Capa · estrutura relógio azul</title>
<defs>
  <linearGradient id="degradeTitulo" gradientUnits="userSpaceOnUse" x1="{X0}" y1="0" x2="{x_fim:.0f}" y2="0">
    <stop offset="0" stop-color="#20B4F5"/><stop offset="0.5" stop-color="#00D6DC"/><stop offset="1" stop-color="#00E6A0"/>
  </linearGradient>
  <linearGradient id="fundo" x1="0" y1="0" x2="0.35" y2="1">
    <stop offset="0" stop-color="#0150D8"/><stop offset="0.45" stop-color="#0142B6"/>
    <stop offset="0.78" stop-color="#0B2B70"/><stop offset="1" stop-color="#091D45"/>
  </linearGradient>
  <radialGradient id="luz" cx="0.12" cy="0.08" r="0.7">
    <stop offset="0" stop-color="#0865EE" stop-opacity="0.55"/><stop offset="1" stop-color="#0865EE" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="fadeX" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#000"/><stop offset="0.22" stop-color="#fff"/>
  </linearGradient>
  <linearGradient id="fadeY" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#000"/><stop offset="0.12" stop-color="#fff"/><stop offset="0.74" stop-color="#fff"/><stop offset="0.86" stop-color="#000"/>
  </linearGradient>
  <mask id="mx"><rect x="{OX}" y="{OY}" width="{W:.0f}" height="{H:.0f}" fill="url(#fadeX)"/></mask>
  <mask id="my"><rect x="{OX}" y="{OY}" width="{W:.0f}" height="{H:.0f}" fill="url(#fadeY)"/></mask>
  <linearGradient id="base" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#091D45" stop-opacity="0"/><stop offset="1" stop-color="#091D45" stop-opacity="0.95"/>
  </linearGradient>
  <pattern id="hex" width="240" height="416" patternUnits="userSpaceOnUse">
    <path d="M120 0 L240 69 L240 208 L120 277 L0 208 L0 69 Z M120 277 L120 416" fill="none" stroke="#FFFFFF" stroke-width="2"/>
  </pattern>
  <radialGradient id="mHex" cx="0.25" cy="0.2" r="0.7"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/></radialGradient>
  <mask id="mh"><rect width="1080" height="1350" fill="url(#mHex)"/></mask>
  <filter id="grao" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="7" result="n"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.06 0"/>
  </filter>
</defs>
<g inkscape:groupmode="layer" inkscape:label="Fundo azul vibrante">
  <rect width="1080" height="1350" fill="url(#fundo)"/>
  <rect width="1080" height="1350" fill="url(#luz)"/>
</g>
<g inkscape:groupmode="layer" inkscape:label="Textura · hexágonos discretos">
  <rect width="1080" height="1350" fill="url(#hex)" opacity="0.05" mask="url(#mh)"/>
</g>
<g inkscape:groupmode="layer" inkscape:label="Objeto · calendário 2027 (Canva)">
  <g mask="url(#my)"><g mask="url(#mx)">
    <image x="{OX}" y="{OY}" width="{W:.0f}" height="{H:.0f}" preserveAspectRatio="none" xlink:href="{OBJ}" href="{OBJ}"/>
  </g></g>
  <rect x="0" y="1070" width="1080" height="280" fill="url(#base)"/>
</g>
<g inkscape:groupmode="layer" inkscape:label="Granulação">
  <rect width="1080" height="1350" filter="url(#grao)"/>
</g>
<g inkscape:groupmode="layer" inkscape:label="Título · 106 px · degradê contínuo">
{chr(10).join(tit)}
</g>
<g inkscape:groupmode="layer" inkscape:label="Texto complementar · 60 px">
{apoio}
</g>
{logo()}
</svg>'''
open(os.path.join(AQUI, 'P01_capa.svg'), 'w').write(svg)
print('ok', round(x_fim))
