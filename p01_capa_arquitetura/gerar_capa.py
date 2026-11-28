#!/usr/bin/env python3
"""Capa P01 — fotografia editorial de arquitetura empresarial integrada ao azul.
SVG vetorial editável (Inkscape): texto real em Montserrat; escrita branca (Regular)
intercalada com palavras em Bold preenchidas com degradê ciano → turquesa → verde-água."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base_svg import larg, espaco, estilo, esc, b64, logo

AQUI = os.path.dirname(os.path.abspath(__file__))
FOTO = b64(os.path.join(AQUI, 'arquitetura.jpg'), 'image/jpeg')

T, TL, TLS = 106, 116, -2
A, AL, ALS = 60, 80, -0.6
X0 = 90
GR = 'url(#degrade)'

def linha(segs, base, sz, ls):
    x, out = X0, []
    for t, w, f in segs:
        out.append(f'<text xml:space="preserve" x="{x:.1f}" y="{base}" style="{estilo(w, sz, ls)};fill:{f}">{esc(t)}</text>')
        x += larg(t, w, sz, ls) + espaco(w, sz, ls)
    return '\n'.join(out)

b0 = 706
titulo = '\n'.join([
    linha([('Seu cliente do', 400, '#FFFFFF')], b0, T, TLS),
    linha([('Simples', 700, GR), ('vende', 400, '#FFFFFF')], b0 + TL, T, TLS),
    linha([('para', 400, '#FFFFFF'), ('empresas?', 700, GR)], b0 + 2 * TL, T, TLS)])
a0 = b0 + 2 * TL + 112
apoio = '\n'.join([
    linha([('A escolha de', 400, '#E8EFF9'), ('2027', 700, GR)], a0, A, ALS),
    linha([('merece atenção.', 400, '#E8EFF9')], a0 + AL, A, ALS)])

svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
     width="1080" height="1350" viewBox="0 0 1080 1350">
<title>P01 · Capa · arquitetura empresarial</title>
<defs>
  <linearGradient id="degrade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#20B4F5"/><stop offset="0.5" stop-color="#00D6DC"/><stop offset="1" stop-color="#00E6A0"/>
  </linearGradient>
  <linearGradient id="integracao" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#0A2E86" stop-opacity="0.10"/>
    <stop offset="0.36" stop-color="#0A2E86" stop-opacity="0"/>
    <stop offset="0.48" stop-color="#0A2E86" stop-opacity="0.55"/>
    <stop offset="0.60" stop-color="#0A2A70" stop-opacity="0.92"/>
    <stop offset="0.82" stop-color="#081F52" stop-opacity="1"/>
    <stop offset="1" stop-color="#061A38" stop-opacity="1"/>
  </linearGradient>
  <radialGradient id="brilho" cx="0.18" cy="0.62" r="0.55">
    <stop offset="0" stop-color="#0865EE" stop-opacity="0.38"/><stop offset="1" stop-color="#0865EE" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="ceu" x1="1" y1="0" x2="0" y2="0.6">
    <stop offset="0" stop-color="#1246C9" stop-opacity="0.30"/><stop offset="1" stop-color="#1246C9" stop-opacity="0"/>
  </linearGradient>
  <filter id="grao" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="3" result="n"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.045 0"/>
  </filter>
</defs>
<g inkscape:groupmode="layer" inkscape:label="Fotografia · arquitetura empresarial">
  <rect width="1080" height="1350" fill="#061A38"/>
  <image x="0" y="0" width="1080" height="1350" preserveAspectRatio="xMidYMid slice" xlink:href="{FOTO}" href="{FOTO}"/>
</g>
<g inkscape:groupmode="layer" inkscape:label="Integração ao azul">
  <rect width="1080" height="1350" fill="url(#ceu)"/>
  <rect width="1080" height="1350" fill="url(#integracao)"/>
  <rect width="1080" height="1350" fill="url(#brilho)"/>
</g>
<g inkscape:groupmode="layer" inkscape:label="Granulação">
  <rect width="1080" height="1350" filter="url(#grao)"/>
</g>
<g inkscape:groupmode="layer" inkscape:label="Título · 106 px">
{titulo}
</g>
<g inkscape:groupmode="layer" inkscape:label="Texto complementar · 60 px">
{apoio}
</g>
{logo()}
</svg>'''
open(os.path.join(AQUI, 'P01_capa.svg'), 'w').write(svg)
print('ok')
