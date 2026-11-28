# Gera exemplos.html com todas as artes de exemplo (texto real editável).
CSS = open('estilo.css').read()
ARTS = [
 # id, tipo, titulo, apoio, top
 ("2026-11-27_0900_C01","capa-escura","Seu cliente do <span class=t>Simples</span> vende para <b>empresas?</b>","A escolha de <b>2027</b> merece atenção.",650),
 ("2026-11-27_0900_C02","int-clara","Revise a <span class=t>opção</span>","Identifique os clientes que escolheram o <b>regime regular de IBS e&nbsp;CBS</b> para o&nbsp;primeiro semestre de&nbsp;2027.",470),
 ("2026-11-27_0900_C03","int-escura","Compare a <span class=t>cadeia</span>","Considere o <b>perfil dos compradores</b>, os créditos possíveis e os custos da&nbsp;operação.",540),
 ("2026-11-27_0900_C04","int-clara2","Confirme no <span class=t>portal</span>","Consulte a <b>opção registrada</b> e as condições vigentes antes de orientar qualquer&nbsp;mudança.",420),
 ("2026-11-27_0900_C05","concl-clara","Decisão <span class=t>documentada</span>","Registre os cenários e a orientação ao empresário <b>antes de qualquer alteração.</b>",0),
 ("2026-11-27_1800_C01","unico-claro","O <span class=t>DAS mais baixo</span> não garante a melhor decisão <b>tributária.</b>","O perfil dos <b>clientes e fornecedores</b> também importa.",470),
 ("2026-11-28_0900_C01","capa-clara","Mesmo produto. <span class=t>ICMS diferente.</span> Onde está a <b>diferença?</b>","",0),
 ("2026-11-28_0900_C02","int-clara","A <span class=t>mercadoria</span>","Descrição, <b>NCM</b> e demais características precisam corresponder ao produto&nbsp;real.",470),
 ("2026-11-28_0900_C03","int-escura","A <span class=t>operação</span>","<b>Origem, destino, finalidade</b> e perfil do destinatário podem alterar a&nbsp;regra.",520),
 ("2026-11-28_0900_C04","int-clara2","A <span class=t>legislação</span>","Consulte o tratamento vigente <b>no estado e na data</b> da&nbsp;operação.",430),
 ("2026-11-28_0900_C05","concl-escura","A <span class=t>conferência</span>","Documente o <b>fundamento fiscal</b> antes de parametrizar o&nbsp;sistema.",0),
]
DECOR = {
 "capa-escura": '<svg class="deco" viewBox="0 0 1080 1350"><defs><linearGradient id="g1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#27C9D5" stop-opacity=".55"/><stop offset=".55" stop-color="#1259D8" stop-opacity=".35"/><stop offset="1" stop-color="#103A82" stop-opacity="0"/></linearGradient><filter id="b1" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="5"/></filter></defs><g transform="translate(300 120)" filter="url(#b1)" fill="none" stroke="url(#g1)" stroke-linecap="round"><path stroke-width="46" d="M60 470 C 160 330, 300 400, 400 300 S 560 80, 660 120"/><path stroke-width="18" opacity=".7" d="M150 520 C 260 420, 380 470, 480 360 S 620 190, 690 230"/></g></svg>',
 "int-clara": '<svg class="deco" viewBox="0 0 1080 1350"><path d="M1080 140 C 900 300, 880 640, 960 900 S 1080 1200, 1080 1200 Z" fill="#E7EEF7"/><path d="M1080 320 C 970 440, 960 700, 1020 900 L 1080 1020 Z" fill="#DCE7F3" opacity=".7"/></svg>',
 "int-clara2": '<svg class="deco" viewBox="0 0 1080 1350"><path d="M0 1350 L0 860 C 220 980, 520 1000, 760 1120 S 1000 1300, 1080 1350 Z" fill="#E7EEF7"/><path d="M0 1350 L0 1020 C 260 1110, 520 1140, 720 1350 Z" fill="#DCE7F3" opacity=".6"/></svg>',
 "int-escura": '<svg class="deco" viewBox="0 0 1080 1350"><defs><radialGradient id="r1" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#1259D8" stop-opacity=".45"/><stop offset="1" stop-color="#1259D8" stop-opacity="0"/></radialGradient></defs><ellipse cx="980" cy="180" rx="520" ry="420" fill="url(#r1)"/><path d="M1080 760 C 900 820, 860 1000, 940 1350 L1080 1350 Z" fill="#103A82" opacity=".55"/></svg>',
 "concl-clara": '<svg class="deco" viewBox="0 0 1080 1350"><path d="M1080 0 L1080 360 C 900 300, 760 160, 720 0 Z" fill="#E7EEF7"/></svg>',
 "unico-claro": '<svg class="deco" viewBox="0 0 1080 1350"><path d="M1080 820 C 860 840, 700 980, 680 1350 L1080 1350 Z" fill="#E7EEF7"/><path d="M1080 960 C 940 980, 840 1100, 830 1350 L1080 1350 Z" fill="#DCE7F3" opacity=".7"/></svg>',
 "capa-clara": '<svg class="deco" viewBox="0 0 1080 1350"><defs><linearGradient id="g3" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#27C9D5" stop-opacity="0"/><stop offset="1" stop-color="#27C9D5" stop-opacity=".22"/></linearGradient></defs><path d="M1080 60 C 820 160, 760 460, 900 700 S 1080 980, 1080 980 Z" fill="url(#g3)"/><path d="M1080 0 L1080 220 C 960 160, 900 80, 880 0 Z" fill="#E7EEF7"/></svg>',
 "concl-escura": '<svg class="deco" viewBox="0 0 1080 1350"><defs><radialGradient id="r2" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#27C9D5" stop-opacity=".28"/><stop offset="1" stop-color="#27C9D5" stop-opacity="0"/></radialGradient></defs><ellipse cx="540" cy="600" rx="560" ry="460" fill="url(#r2)"/></svg>',
}
out = ['<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>EcoFiscal exemplos</title><style>', CSS, '</style></head><body>']
for aid, tipo, tit, apoio, top in ARTS:
    tag = 'h1' if tipo.startswith(('capa','unico')) else 'h2'
    style = f' style="top:{top}px"' if top else ''
    p = f'<p>{apoio}</p>' if apoio else ''
    out.append(f'<section class="art {tipo}" id="a{aid}">{DECOR[tipo]}<div class="block"{style}><{tag}>{tit}</{tag}>{p}</div><div class="logo-area"></div></section>')
out.append('</body></html>')
open('exemplos.html','w').write('\n'.join(out))
print(' '.join(f'a{a[0]}={a[0]}.png' for a in ARTS))
