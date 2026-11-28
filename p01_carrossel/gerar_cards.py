#!/usr/bin/env python3
"""P01 — cards internos 02 (branco) e 03 (azul), no padrão da capa aprovada.
SVG vetorial editável (Inkscape): Montserrat Medium/Bold, degradê nas letras."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base_svg import larg, espaco, estilo, esc, b64, logo, paragrafo

AQUI = os.path.dirname(os.path.abspath(__file__))
T, TL, TLS = 120, 128, -2.3      # título interno (mesmo tamanho nas duas linhas)
A, AL, ALS = 60, 82, -0.6        # texto complementar (igual à capa)
X0 = 90

def linha(segs, base):
    x, out = X0, []
    for t, w, f in segs:
        out.append(f'<text xml:space="preserve" x="{x:.1f}" y="{base}" style="{estilo(w, T, TLS)};fill:{f}">{esc(t)}</text>')
        x += larg(t, w, T, TLS) + espaco(w, T, TLS)
    return '\n'.join(out)

GRAD = '''<linearGradient id="degrade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#20B4F5"/><stop offset="0.5" stop-color="#00D6DC"/><stop offset="1" stop-color="#00E6A0"/>
  </linearGradient>
  <linearGradient id="degradeClaro" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#1287D4"/><stop offset="0.5" stop-color="#00A3B4"/><stop offset="1" stop-color="#00A47E"/>
  </linearGradient>
  <filter id="grao" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="3" result="n"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.045 0"/>
  </filter>'''

def doc(titulo, defs, corpo):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
     width="1080" height="1350" viewBox="0 0 1080 1350">
<title>{titulo}</title>
<defs>
  {GRAD}
  {defs}
</defs>
{corpo}
{logo()}
</svg>'''

# ================= CARD 02 · branco tipográfico =================
b0 = 480
t2 = '\n'.join([linha([('Revise a', 500, '#092653')], b0),
                linha([('opção', 700, 'url(#degradeClaro)')], b0 + TL)])
ap2, n2 = paragrafo([('Identifique os clientes que escolheram o', 500, '#1C2F52'),
                     ('regime regular de IBS e CBS', 700, '#0A6FB8'),
                     ('para o primeiro semestre de 2027.', 500, '#1C2F52')],
                    X0, b0 + TL + 140, A, AL, ALS, 900)
c02 = doc('P01 · C02 · Branco', '''
  <linearGradient id="fundoClaro" x1="0" y1="0" x2="0.4" y2="1">
    <stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#EEF2F8"/>
  </linearGradient>
  <radialGradient id="luzAzul" cx="0.92" cy="0.06" r="0.7">
    <stop offset="0" stop-color="#1246C9" stop-opacity="0.16"/><stop offset="0.55" stop-color="#20B4F5" stop-opacity="0.06"/><stop offset="1" stop-color="#20B4F5" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="luzTurq" cx="0.05" cy="0.98" r="0.55">
    <stop offset="0" stop-color="#00D6DC" stop-opacity="0.12"/><stop offset="1" stop-color="#00D6DC" stop-opacity="0"/>
  </radialGradient>''', f'''
<g inkscape:groupmode="layer" inkscape:label="Fundo branco">
  <rect width="1080" height="1350" fill="url(#fundoClaro)"/>
  <rect width="1080" height="1350" fill="url(#luzAzul)"/>
  <rect width="1080" height="1350" fill="url(#luzTurq)"/>
</g>
<g inkscape:groupmode="layer" inkscape:label="Título interno · 120 px">
{t2}
</g>
<g inkscape:groupmode="layer" inkscape:label="Texto complementar · 60 px">
{ap2}
</g>''')
open(os.path.join(AQUI, 'P01_C02.svg'), 'w').write(c02)

# ================= CARD 03 · azul royal → marinho, fachada como textura =================
FOTO = b64(os.path.join(AQUI, 'arquitetura.jpg'), 'image/jpeg')
b3 = 480
t3 = '\n'.join([linha([('Compare a', 500, '#FFFFFF')], b3),
                linha([('cadeia', 700, 'url(#degrade)')], b3 + TL)])
ap3, n3 = paragrafo([('Considere o', 500, '#E8EFF9'), ('perfil dos compradores,', 700, '#FFFFFF'),
                     ('os créditos possíveis e os custos da operação.', 500, '#E8EFF9')],
                    X0, b3 + TL + 140, A, AL, ALS, 900)
c03 = doc('P01 · C03 · Azul', '''
  <linearGradient id="fundoAzul" x1="0.2" y1="0" x2="0.5" y2="1">
    <stop offset="0" stop-color="#1246C9"/><stop offset="0.5" stop-color="#0B3A9E"/><stop offset="1" stop-color="#092653"/>
  </linearGradient>
  <linearGradient id="fadeFoto" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0.25" stop-color="#000"/><stop offset="0.75" stop-color="#fff"/>
  </linearGradient>
  <mask id="mFoto"><rect width="1080" height="1350" fill="url(#fadeFoto)"/></mask>
  <radialGradient id="brilho" cx="0.85" cy="0.2" r="0.6">
    <stop offset="0" stop-color="#0865EE" stop-opacity="0.35"/><stop offset="1" stop-color="#0865EE" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="base" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0.7" stop-color="#092653" stop-opacity="0"/><stop offset="1" stop-color="#092653" stop-opacity="0.9"/>
  </linearGradient>''', f'''
<g inkscape:groupmode="layer" inkscape:label="Fundo azul">
  <rect width="1080" height="1350" fill="url(#fundoAzul)"/>
</g>
<g inkscape:groupmode="layer" inkscape:label="Fachada · continuidade com a capa">
  <g mask="url(#mFoto)" opacity="0.30">
    <image x="-520" y="-260" width="2160" height="2700" preserveAspectRatio="xMidYMid slice" style="mix-blend-mode:luminosity" xlink:href="{FOTO}" href="{FOTO}"/>
  </g>
  <rect width="1080" height="1350" fill="url(#brilho)"/>
  <rect width="1080" height="1350" fill="url(#base)"/>
</g>
<g inkscape:groupmode="layer" inkscape:label="Granulação">
  <rect width="1080" height="1350" filter="url(#grao)"/>
</g>
<g inkscape:groupmode="layer" inkscape:label="Título interno · 120 px">
{t3}
</g>
<g inkscape:groupmode="layer" inkscape:label="Texto complementar · 60 px">
{ap3}
</g>''')
open(os.path.join(AQUI, 'P01_C03.svg'), 'w').write(c03)
print('ok', n2, n3)
