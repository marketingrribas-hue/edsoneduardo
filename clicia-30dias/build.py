"""Gera os HTML das artes (carrossel 5 lâminas + card) dos 30 dias.
Uso: python3 build.py  -> build/dia_XX.html ; depois node render.js
"""
import html, re, os, json
from conteudo_01_15 import DIAS as D1
from conteudo_16_30 import DIAS as D2

ROOT = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(ROOT, "build")
os.makedirs(BUILD, exist_ok=True)
DIAS = D1 + D2

# ---------------------------------------------------------------- rodízio
CORES = ["marinho", "creme", "areia", "branco"]
# sequência de fundo por lâmina (capa, 2, 3, 4, 5) para cada cor do dia
SEQ = {
    "marinho": ["marinho", "marinho", "creme", "marinho", "marinho"],
    "creme":   ["creme", "creme", "marinho", "creme", "creme"],
    "areia":   ["areia", "areia", "creme", "areia", "areia"],
    "branco":  ["branco", "branco", "marinho", "branco", "branco"],
}
# modelo de card (independente da cor do carrossel, para variar o feed)
CARDS = ["moldura", "aspas", "destaque", "split"]

FOTOS_MARINHO = ["1496181133206-80ce9b88a853", "1460925895917-afdab827c52f", "1551288049-bebda4e38f71",
                 "1526628953301-3e589a6a8b74", "1498050108023-c5249f4df085", "1504868584819-f8e8b4b6d7e3",
                 "1497215728101-856f4ea42174", "1593642632559-0c6d3fc62b89"]
FOTOS_BRANCO = ["1453928582365-b6ad33cbcf64", "1497032628192-86f99bcd76bc", "1501504905252-473c47e087f8",
                "1506784983877-45594efa4cbe", "1543286386-713bdd548da4", "1499951360447-b19be8fe80f5",
                "1497366216548-37526070297c"]


def plano(d):
    i = d - 1
    cor = CORES[i % 4]
    card = CARDS[(i + 2) % 4]
    foto = None
    if cor == "marinho":
        foto = FOTOS_MARINHO[(i // 4) % len(FOTOS_MARINHO)]
    elif cor == "branco":
        foto = FOTOS_BRANCO[(i // 4) % len(FOTOS_BRANCO)]
    return cor, card, foto


# ---------------------------------------------------------------- helpers
def md(s):
    s = html.escape(s, quote=False)
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)


def corpo(s):
    """Primeira frase em tom secundário, restante em tom principal (como nas referências)."""
    m = re.match(r"^(.+?[.?!:])\s+(.+)$", s)
    if not m:
        return f'<span class="b2">{md(s)}</span>'
    return f'<span class="b1">{md(m.group(1))}</span> <span class="b2">{md(m.group(2))}</span>'


def logo(kind, part="mono"):
    return f"../assets/logo/{part}_{kind}.png"


def mono_for(t):
    return logo("dourado") if t == "marinho" else logo("marinho")


def horiz_for(t):
    # fundo escuro: monograma dourado + texto creme (composto); fundo claro: institucional
    return "INST_DARK" if t == "marinho" else logo("institucional", "horizontal")


def horizontal(t, w=360):
    if t == "marinho":
        return (f'<div class="hlogo" style="width:{w}px">'
                f'<img src="{logo("dourado")}" style="height:{w*0.25:.0f}px">'
                f'<img src="{logo("creme","nome")}" style="height:{w*0.145:.0f}px">'
                f'</div>')
    return f'<img class="hlogo-img" src="{logo("institucional","horizontal")}" style="width:{w}px">'


ARROW = '<svg width="34" height="12" viewBox="0 0 34 12"><path d="M0 6h31M26 1l5 5-5 5" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'


def header(t, cover=False):
    left = (f'<img class="hmono" src="{mono_for(t)}">' if cover
            else '<span><b>CLÍCIA</b> NASCIMENTO</span>')
    return f'<div class="hd">{left}<span>TRIBUTARISTA</span></div>'


def footer(t, n, last=False):
    right = ('<span class="save">SALVE &amp; COMPARTILHE</span>' if last
             else f'<span class="pill">ARRASTE {ARROW}</span>')
    return f'<div class="ft"><span class="idx">{n:02d}<i></i>05</span>{right}</div>'


# ---------------------------------------------------------------- lâminas
def capa(dia, t, foto):
    titulo, texto = dia["slides"][0]
    kick = f'<div class="kick"><i></i>{html.escape(dia["kicker"].upper())}</div>'
    if t == "marinho" and foto:
        return f'''
<section class="slide t-marinho capa-foto" id="s1">
  <div class="photo" style="background-image:url(../assets/photos/{foto}.jpg)"></div>
  <div class="photo-ov"></div><div class="noise"></div>
  {header(t, True)}
  <div class="fitbox bottom">{kick}<h1 class="tt">{md(titulo)}</h1><p class="sub">{md(texto)}</p></div>
  {footer(t,1)}
</section>'''
    if t == "branco" and foto:
        return f'''
<section class="slide t-branco capa-branco" id="s1">
  <div class="linen"></div><div class="noise"></div>
  {header(t, True)}
  <div class="fitbox top">{kick}<h1 class="tt">{md(titulo)}</h1><p class="sub">{md(texto)}</p></div>
  <div class="bw"><div class="bw-img" style="background-image:url(../assets/photos/{foto}.jpg)"></div></div>
  {footer(t,1)}
</section>'''
    if t == "areia":
        return f'''
<section class="slide t-areia capa-areia" id="s1">
  <div class="linen"></div><div class="noise"></div>
  {header(t)}
  <div class="fitbox center"><img class="cmono" src="{mono_for(t)}">{kick}<h1 class="tt">{md(titulo)}</h1><div class="fil"></div><p class="sub">{md(texto)}</p></div>
  {footer(t,1)}
</section>'''
    if t == "creme":
        return f'''
<section class="slide t-creme capa-creme" id="s1">
  <div class="satin"></div><div class="noise"></div><div class="frame"></div>
  {header(t, True)}
  <div class="fitbox mid">{kick}<h1 class="tt">{md(titulo)}</h1><div class="fil left"></div><p class="sub">{md(texto)}</p></div>
  {footer(t,1)}
</section>'''
    # marinho sem foto
    return f'''
<section class="slide t-marinho capa-marinho" id="s1">
  <div class="glow"></div><div class="rays"></div><img class="wm" src="{logo("dourado")}"><div class="noise"></div>
  {header(t, True)}
  <div class="fitbox mid">{kick}<h1 class="tt">{md(titulo)}</h1><p class="sub">{md(texto)}</p></div>
  {footer(t,1)}
</section>'''


def bg(t):
    return {
        "marinho": '<div class="glow"></div><div class="rays"></div><div class="noise"></div>',
        "creme": '<div class="satin"></div><div class="noise"></div>',
        "areia": '<div class="linen"></div><div class="noise"></div>',
        "branco": '<div class="linen"></div><div class="noise"></div>',
    }[t]


def interna(dia, n, t, estilo):
    titulo, texto = dia["slides"][n - 1]
    num = f'<div class="num"><span>{n:02d}</span><i></i></div>'
    if estilo == "box":
        body = f'<div class="box"><p class="bd">{corpo(texto)}</p></div>'
    elif estilo == "bar":
        body = f'<div class="bar"><p class="bd">{corpo(texto)}</p></div>'
    else:
        body = f'<p class="bd">{corpo(texto)}</p>'
    return f'''
<section class="slide t-{t} interna" id="s{n}">
  {bg(t)}
  {header(t)}
  <div class="fitbox mid">{num}<h2 class="tt">{md(titulo)}</h2>{body}</div>
  {footer(t,n)}
</section>'''


def fechamento(dia, t):
    titulo, texto = dia["slides"][4]
    return f'''
<section class="slide t-{t} fecho" id="s5">
  {bg(t)}
  {header(t)}
  <div class="fitbox mid"><div class="num"><span>05</span><i></i></div><h2 class="tt">{md(titulo)}</h2><p class="bd">{corpo(texto)}</p></div>
  <div class="sign">{horizontal(t, 430)}</div>
  {footer(t,5,True)}
</section>'''


# ---------------------------------------------------------------- cards
def card(dia, modelo):
    cham, apoio = dia["card"]
    if modelo == "moldura":
        return f'''
<section class="slide t-marinho card moldura" id="card">
  <div class="glow"></div><div class="rays"></div><div class="noise"></div>
  <div class="l1"></div><div class="l2"></div>
  {header("marinho")}
  <div class="fitbox mid"><h1 class="tt">{md(cham)}</h1><p class="bd">{md(apoio)}</p></div>
  <div class="sign">{horizontal("marinho", 330)}</div>
</section>'''
    if modelo == "aspas":
        return f'''
<section class="slide t-creme card aspas" id="card">
  <div class="satin"></div><div class="noise"></div>
  {header("creme")}
  <div class="q">“</div>
  <div class="fitbox mid"><h1 class="tt">{md(cham)}</h1><p class="bd">{md(apoio)}</p>
    <div class="assin"><i></i><div><b>Clícia Nascimento</b><span>Tributarista</span></div></div></div>
  <img class="cornermono" src="{logo("marinho")}">
</section>'''
    if modelo == "destaque":
        return f'''
<section class="slide t-areia card destaque" id="card">
  <div class="linen"></div><div class="noise"></div>
  {header("areia")}
  <div class="fitbox center"><div class="fil"></div><h1 class="tt">{md(cham)}</h1><p class="bd"><mark>{md(apoio)}</mark></p></div>
  <div class="sign">{horizontal("areia", 330)}</div>
</section>'''
    # split
    plain = re.sub(r"\*", "", cham)
    m = re.match(r"^(.+?[.?!])\s+(.+)$", cham)
    if m:
        top, bottom, small = m.group(1), m.group(2), apoio
    else:
        top, bottom, small = cham, None, apoio
    top = top.replace("*", "") if bottom else top
    btm = (f'<h1 class="tt2">{md(bottom if bottom.count("*")%2==0 else bottom.replace("*",""))}</h1>'
           f'<p class="bd">{md(small)}</p>') if bottom else f'<p class="bd big">{md(small)}</p>'
    return f'''
<section class="slide t-branco card split" id="card">
  <div class="linen"></div><div class="noise"></div>
  <div class="topband"><div class="glow"></div><div class="noise"></div></div>
  <div class="hd light"><span><b>CLÍCIA</b> NASCIMENTO</span><span>TRIBUTARISTA</span></div>
  <div class="tophalf fitbox"><h1 class="tt">{md(top)}</h1></div>
  <div class="bothalf fitbox">{btm}</div>
  <img class="cornermono" src="{logo("marinho")}">
</section>'''


# ---------------------------------------------------------------- página
def pagina(dia):
    d = dia["dia"]
    cor, cmod, foto = plano(d)
    seq = SEQ[cor]
    estilo = {"marinho": "plain", "creme": "plain", "areia": "bar", "branco": "box"}[cor]
    parts = [capa(dia, cor, foto)]
    for n in (2, 3, 4):
        t = seq[n - 1]
        parts.append(interna(dia, n, t, estilo if t == cor else "plain"))
    parts.append(fechamento(dia, seq[4]))
    parts.append(card(dia, cmod))
    return f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<link rel="stylesheet" href="../assets/fonts/fonts.css"><link rel="stylesheet" href="../style.css">
</head><body>{"".join(parts)}<script src="../fit.js"></script></body></html>'''


if __name__ == "__main__":
    meta = []
    for dia in DIAS:
        with open(os.path.join(BUILD, f"dia_{dia['dia']:02d}.html"), "w") as f:
            f.write(pagina(dia))
        cor, cmod, foto = plano(dia["dia"])
        meta.append(dict(dia=dia["dia"], cor=cor, card=cmod, foto=foto))
    json.dump(meta, open(os.path.join(BUILD, "plano.json"), "w"), indent=1)
    print("ok", len(DIAS))
