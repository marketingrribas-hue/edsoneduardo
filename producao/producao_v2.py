#!/usr/bin/env python3
"""Produção v2 — padrão da capa aprovada do P01 (fotografia integrada, tipografia
protagonista, degradê nas letras). Sem ícones ou ilustrações vetoriais.
P01–P08: preservados (aprovados / lote 1). P09–P70 e todos os Stories: refeitos."""
import base64, glob, json, os, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nucleo as N
from nucleo import larg, espaco, estilo, esc, LOGO_H, camada, render_linhas, render_apoio, quebra, ajusta, destaques, qc, salvar, fundo, LOG, MARG, CAPA, INT, A, AL, BR, NAV

AQUI = N.AQUI; RAIZ = N.RAIZ; OUT = N.OUT
if os.path.isdir(OUT): shutil.rmtree(OUT)
os.makedirs(OUT)
PUBS = N.PUBS

def foto(pid_foto):
    f = glob.glob(os.path.join(AQUI, 'fotos_prep', f'*{pid_foto}*.jpg'))
    if not f: raise SystemExit('foto não encontrada: ' + pid_foto)
    return 'data:image/jpeg;base64,' + base64.b64encode(open(f[0], 'rb').read()).decode()

LOGO_TOP = 1350 - 50 - LOGO_H

def nome_arq(data, hora, suf):
    d, m, a = data.split('/')
    hh = hora.replace('h', ''); hh = (hh[:2] + (hh[2:] if len(hh) > 2 else '00')).ljust(4, '0')
    return f'{a}-{m}-{d}_{hh}_{suf}'

# ---------------- tratamentos fotográficos ----------------
def trat(estilo_foto, f, H=1350, tt=600, tb=900):
    a = lambda v: max(0.0, min(1.0, v / H))
    """Devolve (defs, camadas) da fotografia integrada ao azul da marca."""
    img = f'<image x="-60" y="-60" width="1200" height="{H + 120}" preserveAspectRatio="xMidYMid slice" xlink:href="{f}"/>'
    if estilo_foto == 'base':        # padrão P01: foto no alto, leitura na base
        d = f'''<linearGradient id="tf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1246C9" stop-opacity="0.22"/><stop offset="{a(tt - 260):.3f}" stop-color="#1246C9" stop-opacity="0.34"/><stop offset="{a(tt - 40):.3f}" stop-color="#0B3A9E" stop-opacity="0.84"/><stop offset="{a(tt + 120):.3f}" stop-color="#0B3A9E" stop-opacity="0.90"/><stop offset="1" stop-color="#092653" stop-opacity="0.96"/></linearGradient>
<linearGradient id="tl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#092653" stop-opacity="0.5"/><stop offset="0.7" stop-color="#092653" stop-opacity="0"/></linearGradient>'''
        c = f'<rect width="1080" height="{H}" fill="#092653"/>{img}<rect width="1080" height="{H}" fill="url(#tf)"/><rect width="1080" height="{H}" fill="url(#tl)"/>'
    elif estilo_foto == 'topo':      # leitura no alto, foto respira na base
        d = f'''<linearGradient id="tf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#071F48" stop-opacity="0.95"/><stop offset="{a(tb + 30):.3f}" stop-color="#0B3A9E" stop-opacity="0.86"/><stop offset="{a(tb + 250):.3f}" stop-color="#1246C9" stop-opacity="0.38"/><stop offset="{max(a(tb + 251), 0.86):.3f}" stop-color="#0B3A9E" stop-opacity="0.50"/><stop offset="1" stop-color="#092653" stop-opacity="0.94"/></linearGradient>'''
        c = f'<rect width="1080" height="{H}" fill="#092653"/>{img}<rect width="1080" height="{H}" fill="url(#tf)"/>'
    elif estilo_foto == 'centro':    # foto em tela cheia, véu uniforme, texto central
        d = f'''<radialGradient id="tf" cx="0.5" cy="0.5" r="0.75"><stop offset="0" stop-color="#0B3A9E" stop-opacity="0.78"/><stop offset="1" stop-color="#071F48" stop-opacity="0.92"/></radialGradient>'''
        c = f'<rect width="1080" height="{H}" fill="#092653"/>{img}<rect width="1080" height="{H}" fill="url(#tf)"/>'
    elif estilo_foto == 'relogio':   # azul vibrante: foto monocromática azul integrada (ref. relógio)
        d = f'''<linearGradient id="fv" x1="0.2" y1="0" x2="0.6" y2="1"><stop offset="0" stop-color="#0865EE"/><stop offset="0.6" stop-color="#1246C9"/><stop offset="1" stop-color="#0A2E86"/></linearGradient>
<linearGradient id="mf" x1="0" y1="0" x2="0" y2="1"><stop offset="{a(tb + 20):.3f}" stop-color="#000"/><stop offset="{a(tb + 230):.3f}" stop-color="#fff"/><stop offset="{max(a(tb + 231), 0.9):.3f}" stop-color="#fff"/><stop offset="1" stop-color="#444"/></linearGradient><mask id="mfm"><rect width="1080" height="{H}" fill="url(#mf)"/></mask>
<linearGradient id="bb" x1="0" y1="0" x2="0" y2="1"><stop offset="0.8" stop-color="#092653" stop-opacity="0"/><stop offset="1" stop-color="#092653" stop-opacity="0.9"/></linearGradient>'''
        c = f'<rect width="1080" height="{H}" fill="url(#fv)"/><g mask="url(#mfm)" opacity="0.62" style="mix-blend-mode:luminosity">{img}</g><rect width="1080" height="{H}" fill="url(#bb)"/>'
    else:                            # 'branco': branco editorial com foto clara na base
        d = f'''<linearGradient id="fw" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#EEF2F8"/></linearGradient>
<linearGradient id="mw" x1="0" y1="0" x2="0" y2="1"><stop offset="{a(tb + 20):.3f}" stop-color="#000"/><stop offset="{a(tb + 240):.3f}" stop-color="#fff"/></linearGradient><mask id="mwm"><rect width="1080" height="{H}" fill="url(#mw)"/></mask>
<linearGradient id="vw" x1="0" y1="0" x2="0" y2="1"><stop offset="0.6" stop-color="#FFFFFF" stop-opacity="0.15"/><stop offset="0.86" stop-color="#EEF2F8" stop-opacity="0.55"/><stop offset="1" stop-color="#EEF2F8" stop-opacity="0.95"/></linearGradient>'''
        c = f'<rect width="1080" height="{H}" fill="url(#fw)"/><g mask="url(#mwm)">{img}</g><rect width="1080" height="{H}" fill="url(#vw)"/>'
    return d, c

# ---------------- composição de capa / card único ----------------
def capa(nome, doc, f, estilo_foto, titulo, apoio_txt='', kicker=None, tom_sem_foto='marinho', var=0, alinhar=None):
    claro = (estilo_foto == 'branco') or (f is None and tom_sem_foto in ('branco', 'gelo'))
    if f is None:
        d, fc, _ = fundo(tom_sem_foto, var, 1350)
    cor = NAV if claro else BR
    grad = 'url(#degradeClaro)' if claro else 'url(#degrade)'
    cor_a, cor_d = ('#1C2F52', '#0A6FB8') if claro else ('#E8EFF9', BR)
    pal = titulo.split()
    marc = destaques(pal, 2)
    spec, maxw, x0 = ajusta(pal, marc, CAPA, 900, MARG, nome)
    T, TL, ls = spec
    lns = quebra(pal, marc, T, ls, maxw)
    gap = 118
    ap_lns = render_apoio(apoio_txt, x0, 0, maxw, cor_a, cor_d)[1] if apoio_txt else 0
    k_h = 70 if kicker else 0
    def altura(T, TL, gap): return k_h + 0.74 * T + (len(lns) - 1) * TL + (gap + (ap_lns - 1) * AL if ap_lns else 0) + 0.24 * T
    topo, base = 100, LOGO_TOP - 44
    alt = altura(T, TL, gap); passo = 0
    while alt > base - topo and passo < 12:
        passo += 1
        if passo <= 4: TL -= 3; gap -= 8; topo -= 8
        else:
            T = int(T * 0.97); TL = int(TL * 0.97); lns = quebra(pal, marc, T, ls, maxw)
        alt = altura(T, TL, gap)
    if passo > 4: LOG['excecoes'].append(f'{nome}: título ajustado para {T} px (texto aprovado extenso)')
    spec = (T, TL, ls)
    # posição do bloco conforme o tratamento
    if estilo_foto in ('base',): y0 = base - alt
    elif estilo_foto in ('topo', 'branco', 'relogio'): y0 = topo + 20
    else: y0 = topo + (base - topo - alt) / 2
    if f is None: y0 = topo + (base - topo - alt) / 2
    al = alinhar or ('center' if estilo_foto == 'centro' else 'start')
    if f is not None:
        d, fc = trat(estilo_foto, f, 1350, y0, y0 + alt)
    caixas = []
    camadas = [camada('Fotografia integrada' if f else 'Fundo', fc)]
    y = y0 + k_h
    if kicker:
        kx = x0 if al == 'start' else (1080 - larg(kicker, 700, 40, 8)) / 2
        camadas.append(camada('Chamada', f'<text x="{kx:.0f}" y="{y - 24:.0f}" style="{estilo(700, 40, 8)};fill:{grad}">{esc(kicker)}</text>'))
    y1 = y + 0.74 * T
    camadas.append(camada(f'Título · {T} px', render_linhas(pal, lns, marc, x0, y1, spec, cor, grad, al, (x0, maxw), caixas)))
    if apoio_txt:
        s, _ = render_apoio(apoio_txt, x0, y1 + (len(lns) - 1) * TL + gap, maxw, cor_a, cor_d, al, (x0, maxw), caixas)
        camadas.append(camada(f'Texto complementar · {A} px', s))
    qc(nome, caixas, 1350, LOGO_TOP, 45 if x0 == 45 else MARG)
    salvar(nome, doc, 1350, d, '\n'.join(camadas), LOGO_TOP)

# ---------------- card interno (padrão aprovado P01 02/03) ----------------
def interno(nome, doc, tom, f_marca, titulo, apoio_txt, var):
    claro = tom in ('branco', 'gelo')
    d, fc, _ = fundo(tom, var, 1350)
    extra = ''
    if f_marca and not claro:
        d += '<linearGradient id="mfi" x1="0" y1="0" x2="1" y2="1"><stop offset="0.25" stop-color="#000"/><stop offset="0.8" stop-color="#fff"/></linearGradient><mask id="mfim"><rect width="1080" height="1350" fill="url(#mfi)"/></mask>'
        extra = camada('Fotografia · marca-d’água da capa', f'<g mask="url(#mfim)" opacity="0.26"><image x="-200" y="-150" width="1480" height="1650" preserveAspectRatio="xMidYMid slice" style="mix-blend-mode:luminosity" xlink:href="{f_marca}"/></g>')
    cor = NAV if claro else BR
    grad = 'url(#degradeClaro)' if claro else 'url(#degrade)'
    cor_a, cor_d = ('#1C2F52', '#0A6FB8') if claro else ('#E8EFF9', BR)
    pal = titulo.split()
    marc = destaques(pal, 1)
    spec, maxw, x0 = ajusta(pal, marc, INT, 900, MARG, nome)
    T, TL, ls = spec
    lns = quebra(pal, marc, T, ls, maxw)
    if len(pal) in (2, 3, 4) and len(lns) == 1:
        nm = [i for i in range(len(pal)) if i not in marc]
        if nm and marc and max(nm) < min(marc): lns = [nm, sorted(marc)]
    _, ap = render_apoio(apoio_txt, x0, 0, maxw, cor_a, cor_d)
    alt = 0.74 * T + (len(lns) - 1) * TL + 140 + (ap - 1) * AL + 0.24 * A
    y1 = 100 + (LOGO_TOP - 44 - 100 - alt) / 2 + 0.74 * T
    caixas = []
    camadas = [camada('Fundo', fc), extra,
               camada(f'Título interno · {T} px', render_linhas(pal, lns, marc, x0, y1, spec, cor, grad, 'start', (x0, maxw), caixas))]
    s, _ = render_apoio(apoio_txt, x0, y1 + (len(lns) - 1) * TL + 140, maxw, cor_a, cor_d, 'start', (x0, maxw), caixas)
    camadas.append(camada(f'Texto complementar · {A} px', s))
    qc(nome, caixas, 1350, LOGO_TOP, 45 if x0 == 45 else MARG)
    salvar(nome, doc, 1350, d, '\n'.join(camadas), LOGO_TOP)

# ---------------- Stories (1080 × 1920) ----------------
ST = (92, 106, -1.6)
def story(nome, doc, texto, f, tom, var, com_foto):
    H = 1920; logo_y = H - 230 - LOGO_H
    if com_foto and f:
        d = f'''<linearGradient id="ts" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1246C9" stop-opacity="0.25"/><stop offset="0.32" stop-color="#1246C9" stop-opacity="0.40"/><stop offset="0.48" stop-color="#0B3A9E" stop-opacity="0.85"/><stop offset="0.62" stop-color="#092653" stop-opacity="0.97"/><stop offset="1" stop-color="#071F48" stop-opacity="1"/></linearGradient>'''
        fc = f'<rect width="1080" height="{H}" fill="#092653"/><image x="0" y="0" width="1080" height="1100" preserveAspectRatio="xMidYMid slice" xlink:href="{f}"/><rect width="1080" height="{H}" fill="url(#ts)"/>'
        claro = False; y_ini = 880
    else:
        d, fc, claro = fundo(tom, var, H)
        y_ini = None
    cor = NAV if claro else BR
    grad = 'url(#degradeClaro)' if claro else 'url(#degrade)'
    pal = texto.split()
    marc = destaques(pal, 2)
    spec, maxw, x0 = ajusta(pal, marc, ST, 900, MARG, nome)
    T, TL, ls = spec
    lns = quebra(pal, marc, T, ls, maxw)
    alt = 0.74 * T + (len(lns) - 1) * TL + 0.24 * T
    if y_ini is None: y_ini = 560 + max(0, (560 - alt) / 2)   # bloco no terço central; sticker abaixo
    else: y_ini = min(y_ini, 1390 - alt)
    y1 = y_ini + 0.74 * T
    caixas = []
    regua = f'<rect x="{x0}" y="{y_ini - 70:.0f}" width="120" height="8" rx="4" fill="{grad}"/>'
    camadas = [camada('Fundo' if not com_foto else 'Fotografia integrada', fc), camada('Fio de abertura', regua),
               camada(f'Texto · {T} px', render_linhas(pal, lns, marc, x0, y1, spec, cor, grad, 'start', (x0, maxw), caixas))]
    fim = y1 + (len(lns) - 1) * TL + 0.24 * T
    if fim > 1400: LOG['qc_falhas'].append((nome, ['texto avança sobre a área do sticker']))
    qc(nome, caixas, H, logo_y, 45 if x0 == 45 else MARG)
    salvar(nome, doc, H, d, '\n'.join(camadas), logo_y)

# ---------------- direção por publicação ----------------
# (foto, tratamento) ; None = composição tipográfica editorial
F = {
 'P09': ('1564846824194', 'base'), 'P11': ('1617761141732', 'relogio'), 'P13': ('1768270181430', 'topo'),
 'P14': ('1771678040857', 'branco'), 'P15': ('1779043152010', 'branco'), 'P16': ('1762291323534', 'base'),
 'P17': ('1518186285589', 'relogio'), 'P19': ('1644079446600', 'topo'), 'P21': ('1716191299984', 'base'),
 'P22': ('1764025851210', 'branco'), 'P23': ('1576731753569', 'relogio'), 'P25': ('1603294278610', 'base'),
 'P27': ('1571624436279', 'branco'), 'P28': ('1779700210487', 'centro'), 'P29': ('1717386255773', 'relogio'),
 'P30': ('1623177623442', 'branco'), 'P31': ('1774953037913', 'branco'), 'P33': ('1794415287131', 'topo'),
 'P34': ('1759222973482', 'centro'), 'P35': ('1763729805496', 'relogio'), 'P36': ('1450101499163', 'base'),
 'P37': ('1736507748808', 'topo'), 'P38': ('1694885156873', 'branco'), 'P39': ('1556742212', 'branco'),
 'P41': ('1494412519320', 'base'), 'P42': ('1694253988732', 'branco'), 'P43': ('1766785368863', 'branco'),
 'P44': ('1780000291226', 'centro'), 'P45': ('1705147217444', 'base'), 'P47': ('1605732562742', 'relogio'),
 'P49': ('1627878091865', 'topo'), 'P51': ('1762427354566', 'branco'), 'P52': ('1758448656987', 'base'),
 'P53': ('1635174815612', 'relogio'), 'P54': ('1704785119987', 'branco'), 'P55': ('1740933084056', 'branco'),
 'P56': ('1497366754035', 'centro'), 'P57': ('1612925221031', 'centro'), 'P58': ('1607202563351', 'centro'),
 'P59': ('1758448093806', 'relogio'), 'P61': ('1758448500688', 'base'), 'P63': ('1523477593243', 'branco'),
 'P64': ('1741711333479', 'centro'), 'P65': ('1556114846', 'relogio'), 'P67': ('1535320903710', 'branco'),
 'P68': ('1621831337128', 'relogio'), 'P69': ('1691525891769', 'topo'), 'P70': ('1672718945831', 'centro'),
}
TIPO = {'P10': 'branco', 'P18': 'marinho', 'P20': 'vibrante', 'P26': 'gelo', 'P32': 'royal', 'P46': 'branco',
        'P48': 'marinho', 'P50': 'gelo', 'P60': 'royal', 'P66': 'branco'}
FOTO_ST = {'P01': None, 'P02': None, 'P03': '1644079446600', 'P04': None, 'P05': None, 'P06': None, 'P07': None, 'P08': None,
           'P12': '1617761141732', 'P24': '1576731753569', 'P40': '1556742212', 'P62': '1758448500688'}
ESQ_ESCURA = [['branco', 'royal', 'branco', 'marinho'], ['gelo', 'marinho', 'branco', 'royal'], ['branco', 'intermediario', 'gelo', 'marinho']]
ESQ_CLARA = [['marinho', 'branco', 'royal', 'gelo'], ['royal', 'gelo', 'marinho', 'branco']]
TONS_ST = ['vibrante', 'branco', 'marinho', 'gelo', 'royal', 'intermediario']

lote1 = os.path.join(AQUI, 'lote1')
for n, p in enumerate(PUBS):
    pid = p['id']; doc = f"{pid} · {p['tema']}"
    nome = lambda suf, h=None: nome_arq(p['data'], h or p['hora'], suf)
    if pid in ('P01', 'P02', 'P03', 'P04', 'P05', 'P06', 'P07', 'P08'):
        k_tot = len(p['cards']) if p['formato'] == 'CARROSSEL' else 1
        for k in range(k_tot):
            nm = nome(f'C{k + 1:02d}')
            shutil.copy(os.path.join(lote1, nm + '.svg'), os.path.join(OUT, nm + '.svg')); LOG['pecas'].append(nm)
        f_st = foto(FOTO_ST[pid]) if FOTO_ST.get(pid) else None
    elif p['formato'] == 'REELS':
        f_st = foto(FOTO_ST[pid])
    else:
        if pid in F:
            fid, est = F[pid]; f = foto(fid)
        else:
            f, est = None, None
        c0 = p['cards'][0]
        if p['formato'] == 'CARROSSEL':
            capa(nome('C01'), doc + ' · capa', f, est, c0['titulo'], c0.get('apoio', ''), c0.get('kicker'), TIPO.get(pid, 'marinho'), n)
            claro_capa = est == 'branco' or (f is None and TIPO.get(pid) in ('branco', 'gelo'))
            esq = (ESQ_CLARA if claro_capa else ESQ_ESCURA)[n % (2 if claro_capa else 3)]
            for k, c in enumerate(p['cards'][1:]):
                interno(nome(f'C{k + 2:02d}'), doc + f' · card {k + 2:02d}', esq[k], f, c['titulo'], c['apoio'], n + k)
        else:
            capa(nome('C01'), doc + ' · card único', f, est, c0['titulo'], c0['apoio'], c0.get('kicker'), TIPO.get(pid, 'marinho'), n,
                 'center' if (f is None and n % 2 == 0) else None)
        f_st = f
    for s_i, s in enumerate(p['stories']):
        story(nome(f'S{s_i + 1:02d}', s['hora']), doc + f' · story {s_i + 1:02d}', s['texto'], f_st, TONS_ST[(n * 2 + s_i) % 6], n + s_i, s_i == 0 and f_st is not None)

for k, src in enumerate(['P01_capa', 'P01_C02', 'P01_C03']):
    shutil.copy(os.path.join(RAIZ, 'p01_carrossel', src + '.svg'), os.path.join(OUT, f'2026-11-27_0900_C{k + 1:02d}.svg'))

json.dump(LOG, open(os.path.join(AQUI, 'relatorio_qc_v2.json'), 'w'), ensure_ascii=False, indent=1)
print('peças:', len(set(LOG['pecas'])), '| arquivos:', len(os.listdir(OUT)))
print('exceções:', len(LOG['excecoes'])); [print('  ', e) for e in LOG['excecoes']]
print('falhas QC:', len(LOG['qc_falhas'])); [print('  ', e) for e in LOG['qc_falhas']]
