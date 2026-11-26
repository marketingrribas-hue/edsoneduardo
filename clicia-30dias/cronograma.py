"""Gera cronograma/Cronograma_30_dias_Clicia_Nascimento.html (convertido em PDF por cronograma_pdf.js)."""
import html, os, re
from PIL import Image
from build import DIAS, plano

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "cronograma"); os.makedirs(os.path.join(OUT, "thumbs"), exist_ok=True)

COR = {"marinho": ("Marinho", "#051D40"), "creme": ("Creme", "#F7F3E9"),
       "areia": ("Areia (dourado claro)", "#E9DDC4"), "branco": ("Branco linho + foto P&B", "#FAF8F3")}
CARD = {"moldura": "Moldura · fundo marinho", "aspas": "Aspas · fundo creme",
        "destaque": "Destaque · fundo areia", "split": "Dividido · marinho/branco"}

def e(s): return html.escape(re.sub(r"\*", "", s))

def thumbs(d):
    out = []
    for name in [f"dia{d:02d}_carrossel_{i}" for i in range(1, 6)] + [f"dia{d:02d}_card"]:
        src = os.path.join(ROOT, "out", f"dia_{d:02d}", name + ".png")
        dst = os.path.join(OUT, "thumbs", name + ".jpg")
        im = Image.open(src).convert("RGB"); im.thumbnail((220, 275)); im.save(dst, quality=82)
        out.append(f"thumbs/{name}.jpg")
    return out

def sw(cor):
    n, c = COR[cor]
    return f'<span class="sw" style="background:{c}"></span>{n}'

rows, pages = [], []
for dia in DIAS:
    d = dia["dia"]; cor, cmod, foto = plano(d)
    rows.append(f'<tr><td class="c">{d:02d}</td><td>{sw(cor)}</td><td>{e(dia["slides"][0][0])}</td>'
                f'<td>{e(dia["card"][0])}<div class="mini">{CARD[cmod]}</div></td><td>{e(dia["reels"])}</td></tr>')
    th = "".join(f'<img src="{t}">' for t in thumbs(d))
    head = (f'<div class="dh"><span class="dn">DIA {d:02d}</span><span class="dk">{e(dia["kicker"]).upper()}</span>'
            f'<span class="dc">{sw(cor)}</span></div><h2>{e(dia["tema"])}</h2>')
    if "leg_carrossel" in dia:
        st = "".join(f'<li><b>{i+1:02d} {html.escape(r)}</b> {html.escape(t)}</li>' for i, (r, t) in enumerate(dia["stories"]))
        body = f'''
<p class="sub">{html.escape(dia["sub"])}</p>
<div class="th">{th}</div>
<h4>08h · Carrossel (5 lâminas) · arquivos dia{d:02d}_carrossel_1 a 5</h4>
<p class="lbl">LEGENDA DO CARROSSEL</p><p>{html.escape(dia["leg_carrossel"])}</p>
<h4>12h30 · Reels · título de capa: {html.escape(dia["reels"])}</h4>
<p class="lbl">ROTEIRO DE FALA · GRAVAR COM NATURALIDADE</p><p>{html.escape(dia["roteiro"])}</p>
<p class="lbl">LEGENDA DO REELS</p><p>{html.escape(dia["leg_reels"])}</p>
<h4>18h30 · Card estático · arquivo dia{d:02d}_card</h4>
<p class="lbl">LEGENDA DO CARD</p><p>{html.escape(dia["leg_card"])}</p>
<h4>Stories · quatro telas</h4><ul class="st">{st}</ul>'''
    else:
        body = f'''
<div class="th">{th}</div>
<h4>08h · Carrossel · 12h30 · Reels “{html.escape(dia["reels"])}” · 18h30 · Card</h4>
<p class="note">Legendas, roteiro do Reels e stories deste dia: <b>Roteiro revisado (PDF), páginas {dia["pdf_pag"]}</b>. Os textos das artes foram transcritos de lá sem alteração.</p>'''
    pages.append(f'<section class="pg day">{head}{body}</section>')

doc = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<link rel="stylesheet" href="../assets/fonts/fonts.css">
<style>
@page{{size:A4;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font:400 10.5pt/1.5 'Manrope',sans-serif;color:#051D40}}
.pg{{width:210mm;min-height:297mm;padding:18mm 18mm 16mm;page-break-after:always;position:relative}}
.cover{{background:#051D40;color:#F7F3E9;display:flex;flex-direction:column;justify-content:space-between}}
.cover img.logo{{width:95mm}}
.cover h1{{font:400 34pt/1.1 'Playfair Display',serif;margin:10mm 0 4mm}}
.cover h1 em{{color:#D4AE60}}
.cover .k{{font:600 8pt/1 'Manrope';letter-spacing:.3em;color:#D4AE60}}
.cover p{{color:#d9d2c0;max-width:150mm;margin-top:3mm}}
.cover .grid{{display:grid;grid-template-columns:1fr 1fr;gap:6mm 10mm;margin-top:8mm}}
.cover .grid b{{display:block;font:600 7.5pt/1 'Manrope';letter-spacing:.25em;color:#D4AE60;margin-bottom:2mm}}
.sw{{display:inline-block;width:9pt;height:9pt;border-radius:50%;border:1px solid rgba(127,127,127,.6);margin-right:5pt;vertical-align:-1pt}}
h2{{font:400 20pt/1.15 'Playfair Display',serif;margin:2mm 0 2mm}}
h3{{font:400 22pt/1.15 'Playfair Display',serif;margin-bottom:6mm}}
h4{{font:700 9pt/1.3 'Manrope';margin:5mm 0 1.5mm;color:#051D40;border-top:1px solid #e3dccb;padding-top:3mm}}
.lbl{{font:700 7pt/1 'Manrope';letter-spacing:.2em;color:#A27B33;margin:2.5mm 0 1mm}}
.sub{{color:#5A6880;margin-bottom:4mm}}
.dh{{display:flex;gap:6mm;align-items:center;font:700 8pt/1 'Manrope';letter-spacing:.22em}}
.dn{{color:#A27B33}} .dk{{color:#5A6880}} .dc{{margin-left:auto;font-weight:500;letter-spacing:0}}
.th{{display:flex;gap:2.2mm;margin:3mm 0 1mm}}
.th img{{width:27.5mm;height:34.4mm;object-fit:cover;border-radius:1mm;box-shadow:0 0 0 .3mm #ddd}}
.th img:last-child{{margin-left:2.5mm;box-shadow:0 0 0 .5mm #D4AE60}}
.st{{list-style:none}} .st li{{margin:1.2mm 0}} .st b{{color:#A27B33;font-size:8pt;letter-spacing:.12em;margin-right:2mm}}
.note{{margin-top:5mm;padding:4mm 5mm;background:#F7F3E9;border-left:2px solid #D4AE60}}
table{{width:100%;border-collapse:collapse;font-size:7.8pt;line-height:1.35}}
th{{text-align:left;font:700 7pt/1 'Manrope';letter-spacing:.18em;color:#A27B33;padding:2mm 2mm;border-bottom:1px solid #D4AE60}}
td{{padding:1.1mm 2mm;border-bottom:1px solid #eee7d8;vertical-align:top}}
td.c{{font-weight:700;color:#A27B33}}
.mini{{font-size:7pt;color:#8a93a3}}
ul.rules{{margin:3mm 0 0 4mm}} ul.rules li{{margin:1.5mm 0}}
</style></head><body>
<section class="pg cover">
 <div><img class="logo" src="../assets/logo/horizontal_branco.png" style="filter:none"></div>
 <div>
  <div class="k">CRONOGRAMA EDITORIAL · 30 DIAS</div>
  <h1>Conteúdo que explica,<br><em>conecta e gera confiança.</em></h1>
  <p>30 carrosséis (5 lâminas) e 30 cards estáticos em arte final 1080 × 1350 px, mais 30 roteiros de Reels e 120 telas de stories em texto.</p>
  <div class="grid">
   <div><b>CADÊNCIA</b>08h carrossel · 12h30 Reels · 18h30 card · 4 stories ao longo do dia</div>
   <div><b>RODÍZIO DE CORES DO CARROSSEL</b>{sw("marinho")} → {sw("creme")} → {sw("areia")} → {sw("branco")}</div>
   <div><b>CARDS</b>Quatro modelos em rodízio próprio (moldura, aspas, destaque e dividido), sempre em cor diferente do carrossel do dia.</div>
   <div><b>FOTOS</b>Somente objetos e ambientes (notebook, mesa, café, gráficos), sem pessoas e sem símbolos jurídicos. Fonte: Unsplash (licença gratuita).</div>
  </div>
 </div>
 <p style="font-size:8.5pt;color:#9aa3b3">Dias 01–15: Roteiro revisado (03/11/2026). Dias 16–30: conteúdo novo na mesma linha editorial; requer validação da Clícia antes de publicar.</p>
</section>
<section class="pg">
 <h3>Visão geral</h3>
 <table><tr><th>DIA</th><th>COR</th><th>CARROSSEL · CAPA</th><th>CARD ESTÁTICO</th><th>REELS</th></tr>{"".join(rows)}</table>
 <h4>Cuidados de publicação</h4>
 <ul class="rules">
  <li>Não anunciar valores, percentuais, prazos ou créditos como garantidos.</li>
  <li>Conteúdos sobre restituição, compensação, prazos, parcelamentos e reforma tributária são educativos: conferir as orientações oficiais vigentes antes de publicar.</li>
  <li>Não pedir nem expor documentos, CNPJ ou dados empresariais em comentários e caixinhas.</li>
 </ul>
</section>
{"".join(pages)}
</body></html>'''
open(os.path.join(OUT, "cronograma.html"), "w").write(doc)
print("ok")
