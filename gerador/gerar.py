#!/usr/bin/env python3
"""Gera as páginas do site a partir do conteúdo em paginas.py e dados.py.

Uso: python3 gerador/gerar.py   (a partir da raiz do repositório)
As páginas geradas (index.html e as pastas de cada área) são as que o GitHub Pages publica.
"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from dados import *  # noqa: E402,F403
from paginas import AREAS, FAQ_HOME, SEDACAO, TECNOLOGIA  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAS = {a["slug"]: a for a in AREAS + [TECNOLOGIA, SEDACAO]}
DESTAQUES = ["cirurgia-ortognatica", "dtm-atm-dor-orofacial", "trauma-facial-fraturas"]
OUTRAS = ["sisos-cirurgia-oral", "implantes-enxertos", "patologias-dos-maxilares", "mentoplastia"]

ENDERECO_TXT = f"{ENDERECO['local']} · {ENDERECO['rua']} · {ENDERECO['bairro']}, {ENDERECO['cidade']} – {ENDERECO['uf']}, {ENDERECO['cep']}"
WA_LINK = f"https://wa.me/{WHATSAPP}"

CONSULTORIO = {
    "@type": "Dentist",
    "@id": f"{SITE}/#consultorio",
    "name": f"{NOME_CURTO} · {AREA}",
    "url": f"{SITE}/",
    "logo": f"{SITE}/logo.png",
    "image": [f"{SITE}/img/consultorio-sala.webp", f"{SITE}/img/consultorio-recepcao.webp"],
    "telephone": TELEFONE_E164,
    "email": EMAIL,
    "address": {
        "@type": "PostalAddress",
        "streetAddress": ENDERECO["rua"],
        "addressLocality": ENDERECO["cidade"],
        "addressRegion": ENDERECO["uf"],
        "postalCode": ENDERECO["cep"],
        "addressCountry": ENDERECO["pais"],
    },
    "openingHoursSpecification": HORARIO_LD,
    "areaServed": [{"@type": "City", "name": "Curitiba"}, {"@type": "AdministrativeArea", "name": "Região Metropolitana de Curitiba"}],
    "contactPoint": {"@type": "ContactPoint", "contactType": "Agendamento", "telephone": "+" + WHATSAPP, "availableLanguage": "pt-BR"},
    "containedInPlace": {"@type": "Hospital", "name": HOSPITAL, "address": {"@type": "PostalAddress", "streetAddress": ENDERECO["rua"], "addressLocality": ENDERECO["cidade"], "addressRegion": ENDERECO["uf"], "addressCountry": ENDERECO["pais"]}},
    "medicalSpecialty": "Cirurgia e Traumatologia Bucomaxilofacial",
    "employee": {"@id": f"{SITE}/#daniel"},
    "hasMap": MAPA,
    "sameAs": [MAPA],
}
PROFISSIONAL = {
    "@type": "Person",
    "@id": f"{SITE}/#daniel",
    "name": NOME,
    "alternateName": NOME_CURTO,
    "image": f"{SITE}/img/dr-daniel-negrelle.webp",
    "jobTitle": f"Cirurgião-dentista · {ESPECIALISTA}",
    "url": f"{SITE}/sobre/",
    "worksFor": {"@id": f"{SITE}/#consultorio"},
    "workLocation": {"@id": f"{SITE}/#consultorio"},
    "identifier": {"@type": "PropertyValue", "propertyID": "CRO-PR", "value": "16620"},
    "sameAs": ["https://br.linkedin.com/in/daniel-negrelle-3a6968131", "https://hslcuritiba.com.br/member/daniel-bonato-negrelle-2/", "https://www.doctoralia.com.br/perfil/daniel-bonato-negrelle-2"],
    "alumniOf": [
        {"@type": "CollegeOrUniversity", "name": "Universidade Federal do Paraná"},
        {"@type": "Hospital", "name": "Hospital das Clínicas da Faculdade de Medicina da Universidade de São Paulo"},
    ],
    "hasCredential": [
        {"@type": "EducationalOccupationalCredential", "credentialCategory": "degree", "name": "Graduação em Odontologia", "recognizedBy": {"@type": "CollegeOrUniversity", "name": "Universidade Federal do Paraná"}, "dateCreated": "2004"},
        {"@type": "EducationalOccupationalCredential", "credentialCategory": "Especialização", "name": "Especialização em Cirurgia e Traumatologia Bucomaxilofacial", "recognizedBy": {"@type": "Hospital", "name": "Hospital das Clínicas da FMUSP"}, "dateCreated": "2007"},
        {"@type": "EducationalOccupationalCredential", "credentialCategory": "degree", "name": "Mestrado", "recognizedBy": {"@type": "CollegeOrUniversity", "name": "Universidade Federal do Paraná"}, "dateCreated": "2018"},
    ],
    "knowsAbout": [
        "Cirurgia ortognática", "Disfunção temporomandibular", "Articulação temporomandibular",
        "Dor orofacial", "Trauma facial", "Fraturas de mandíbula", "Terceiros molares",
        "Implantes dentários", "Próteses sobre implantes", "Fluxo digital em prótese sobre implantes", "Enxertos ósseos", "Sedação endovenosa em cirurgia oral", "Cirurgia guiada", "Escaneamento intraoral", "Próteses em zircônia", "Patologia dos maxilares", "Mentoplastia",
        "Planejamento virtual tridimensional",
    ],
}


def esc(s):
    return html.escape(s, quote=True)


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", **obj}, ensure_ascii=False) + "</script>"


def cabecalho():
    areas = "".join(f'<li><a href="/{s}/">{esc(TODAS[s]["menu"])}</a></li>' for s in DESTAQUES + OUTRAS)
    return f"""<header>
  <div class="wrap">
    <a href="/" class="marca"><img src="/logo.png" alt="Dr. Daniel Negrelle – Cirurgia Bucomaxilofacial" width="158" height="40"></a>
    <nav aria-label="Principal" class="nav-desk">
      <details class="drop"><summary>Áreas de atuação</summary><ul>{areas}</ul></details>
      <a href="/tecnologia-e-planejamento/">Tecnologia</a>
      <a href="/sobre/">Sobre</a>
      <a href="/contato/">Contato</a>
    </nav>
    <details class="nav-mob"><summary aria-label="Abrir menu">Menu</summary>
      <ul>{areas}<li><a href="/sedacao-e-ambiente-hospitalar/">Sedação e ambiente hospitalar</a></li><li><a href="/tecnologia-e-planejamento/">Tecnologia e planejamento</a></li><li><a href="/sobre/">Sobre o Dr. Daniel</a></li><li><a href="/contato/">Contato</a></li></ul>
    </details>
  </div>
</header>"""


def rodape():
    return f"""<footer>
  <div class="wrap rodape">
    <div>
      <strong>{esc(NOME)}</strong><br>
      {esc(ESPECIALISTA)} · {esc(CRO)}<br>
      {esc(ENDERECO_TXT)}<br>
      <a href="tel:{TELEFONE_E164}">{esc(TELEFONE)}</a> · <a href="{WA_LINK}">WhatsApp</a>
    </div>
    <div class="rodape-links">
      <a href="/sedacao-e-ambiente-hospitalar/">Sedação e ambiente hospitalar</a>
      <a href="/tecnologia-e-planejamento/">Tecnologia e planejamento</a>
      <a href="/sobre/">Sobre</a>
      <a href="/contato/">Contato</a>
      <a href="/privacidade.html">Política de privacidade</a>
    </div>
  </div>
</footer>"""


def pagina(caminho, titulo, descricao, corpo, dados=None):
    url = f"{SITE}/{caminho}"
    blocos = "\n".join(ld(d) for d in (dados or []))
    doc = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titulo)}</title>
<meta name="description" content="{esc(descricao)}">
{'<meta name="robots" content="noindex">' if caminho == "404.html" else f'<link rel="canonical" href="{url}">'}
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="{esc(NOME_CURTO)}">
<meta property="og:title" content="{esc(titulo)}">
<meta property="og:description" content="{esc(descricao)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/logo.png">
<link rel="icon" href="/favicon.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css">
{blocos}
</head>
<body>
{cabecalho()}
<main>
{corpo}
</main>
{rodape()}
</body>
</html>
"""
    destino = os.path.join(RAIZ, caminho, "index.html") if caminho.endswith("/") or caminho == "" else os.path.join(RAIZ, caminho)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "w", encoding="utf-8") as f:
        f.write(doc)


def cta(texto="Entender se este tratamento é indicado para o seu caso"):
    return f"""<section class="cta">
  <div class="wrap">
    <h2>{esc(texto)}</h2>
    <p>A avaliação reúne exame clínico, exames de imagem e a conversa sobre as alternativas de tratamento.</p>
    <a class="btn btn-light" href="{WA_LINK}">Agendar uma avaliação</a>
    <a class="btn btn-outline" href="tel:{TELEFONE_E164}">Falar com a equipe</a>
  </div>
</section>"""


def migalhas(nome, caminho):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Início", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": nome, "item": f"{SITE}/{caminho}"},
        ],
    }


def faq_html(faq):
    itens = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faq)
    return f'<section class="faq"><h2>Perguntas frequentes</h2>{itens}</section>'


def faq_ld(faq):
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq
        ],
    }


def relacionadas_html(slugs):
    cards = "".join(
        f'<a class="card link" href="/{s}/"><h3>{esc(TODAS[s]["menu"])}</h3><p>{esc(TODAS[s].get("resumo", TODAS[s]["descricao"]))}</p></a>'
        for s in slugs
    )
    return f'<section class="relacionadas"><h2>Assuntos relacionados</h2><div class="grid">{cards}</div></section>'


def gerar_area(a):
    caminho = f"{a['slug']}/"
    secoes = "".join(f"<section><h2>{esc(t)}</h2>{c}</section>" for t, c in a["secoes"])
    corpo = f"""<div class="hero hero-int">
  <div class="wrap">
    <nav class="migalhas" aria-label="Você está em"><a href="/">Início</a> › {esc(a['menu'])}</nav>
    <h1>{esc(a['titulo'])}</h1>
    <p>{esc(a['intro'])}</p>
  </div>
</div>
<div class="wrap texto">
{secoes}
{faq_html(a['faq'])}
{relacionadas_html(a['relacionadas'])}
</div>
{cta(a.get('cta', 'Entender se este tratamento é indicado para o seu caso'))}"""
    dados = [
        {
            "@type": "MedicalWebPage",
            "@id": f"{SITE}/{caminho}#pagina",
            "url": f"{SITE}/{caminho}",
            "name": a["titulo"],
            "description": a["descricao"],
            "inLanguage": "pt-BR",
            "about": {"@type": "MedicalProcedure", "name": a.get("procedimento", a["menu"])} if a is not TECNOLOGIA else {"@type": "Thing", "name": "Planejamento virtual em cirurgia bucomaxilofacial"},
            "author": {"@id": f"{SITE}/#daniel"},
            "publisher": {"@id": f"{SITE}/#consultorio"},
        },
        faq_ld(a["faq"]),
        migalhas(a["menu"], caminho),
        CONSULTORIO,
        PROFISSIONAL,
    ]
    pagina(caminho, a["seo_titulo"], a["descricao"], corpo, dados)


def gerar_home():
    destaques = "".join(
        f'<a class="card destaque link" href="/{s}/"><h3>{esc(TODAS[s]["menu"])}</h3><p>{esc(TODAS[s]["resumo"])}</p><span class="mais">Saiba mais sobre {esc(TODAS[s]["menu"].lower() if s != "dtm-atm-dor-orofacial" else "DTM, ATM e dor orofacial")}</span></a>'
        for s in DESTAQUES
    )
    outras = "".join(
        f'<a class="card link" href="/{s}/"><h3>{esc(TODAS[s]["menu"])}</h3><p>{esc(TODAS[s]["resumo"])}</p></a>' for s in OUTRAS
    )
    corpo = f"""<div class="hero">
  <div class="wrap">
    <p class="sobretitulo">{esc(NOME)} · {esc(ESPECIALISTA)} · {esc(CRO)}</p>
    <h1>Cirurgião bucomaxilofacial em Curitiba</h1>
    <p>Diagnóstico, planejamento e tratamento de casos complexos da face, dos maxilares e da articulação temporomandibular. Consultório dentro do {esc(HOSPITAL)}, com estrutura hospitalar para as cirurgias que precisam dela.</p>
    <a class="btn btn-light" href="{WA_LINK}">Agendar uma avaliação</a>
    <a class="btn btn-outline" href="tel:{TELEFONE_E164}">Ligar {esc(TELEFONE)}</a>
  </div>
</div>

<section id="areas">
  <div class="wrap">
    <h2>Áreas de atuação</h2>
    <p class="lead">A Cirurgia e Traumatologia Bucomaxilofacial trata as alterações dos ossos da face, dos maxilares, da articulação temporomandibular e das estruturas da boca.</p>
    <div class="grid grid-3">{destaques}</div>
    <h3 class="sub">Outras áreas</h3>
    <div class="grid">{outras}</div>
  </div>
</section>

<section class="faixa">
  <div class="wrap">
    <h2>Cada caso começa pelo diagnóstico</h2>
    <div class="grid etapas">
      <div><h3>Diagnóstico</h3><p>Exame clínico, história do paciente e exames de imagem definem o problema a ser tratado.</p></div>
      <div><h3>Planejamento</h3><p>Exames e modelos dentários são integrados para definir a indicação, as alternativas e a estratégia de tratamento.</p></div>
      <div><h3>Tratamento</h3><p>Em consultório ou em ambiente hospitalar, conforme a complexidade do procedimento.</p></div>
      <div><h3>Acompanhamento</h3><p>Consultas de revisão e orientações até a recuperação e a estabilização do resultado.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>Cirurgia com conforto e segurança</h2>
    <p class="lead">O consultório fica dentro do {esc(HOSPITAL)}. Quando indicado, a cirurgia é feita com sedação endovenosa, conduzida por médico anestesiologista em ambiente hospitalar, de acordo com a complexidade do procedimento e as necessidades de cada paciente.</p>
    <a class="btn btn-escuro" href="/sedacao-e-ambiente-hospitalar/">Conhecer as opções de sedação</a>
  </div>
</section>

<section class="faixa">
  <div class="wrap duas">
    <div>
      <h2>Tecnologia a serviço do planejamento</h2>
      <p>Tomografia, modelos digitais, planejamento virtual tridimensional, guias impressos em 3D e fluxo digital na prótese sobre implantes são usados quando melhoram uma decisão clínica: mais precisão, previsibilidade ou compreensão do tratamento.</p>
      <p><a href="/tecnologia-e-planejamento/">Como a tecnologia é usada no planejamento</a></p>
    </div>
    <div>
      <h2>Sobre o Dr. Daniel Negrelle</h2>
      <img class="foto-mini" src="/img/dr-daniel-negrelle.webp" alt="Dr. Daniel Negrelle, cirurgião bucomaxilofacial" width="120" height="120" loading="lazy">
      <p>{esc(NOME)} é especialista em Cirurgia e Traumatologia Bucomaxilofacial, com consultório no {esc(HOSPITAL)}, em Curitiba, e participação no desenvolvimento de ferramentas digitais para o planejamento cirúrgico.</p>
      <p><a href="/sobre/">Conheça o profissional</a></p>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>Avaliações de pacientes</h2>
    <p class="lead">As avaliações de quem já foi atendido estão publicadas no perfil do consultório no Google.</p>
    <a class="btn btn-escuro" href="{MAPA}">Ver avaliações no Google</a>
  </div>
</section>

<section id="app" class="faixa">
  <div class="wrap">
    <h2>App do paciente</h2>
    <p class="lead">Em desenvolvimento: um aplicativo exclusivo para os pacientes do consultório acompanharem o tratamento entre as consultas.</p>
    <div class="card">
      <ul>
        <li>Alertas para manter os dentes separados ao longo do dia, no tratamento do apertamento</li>
        <li>Diário da dor, com registro das crises, e diário do sono</li>
        <li>Orientações de cuidados após as cirurgias</li>
        <li>Aviso e confirmação de consultas</li>
      </ul>
      <p><a href="/privacidade.html">Política de privacidade do app</a></p>
    </div>
  </div>
</section>

<section>
  <div class="wrap texto">{faq_html(FAQ_HOME)}</div>
</section>
{cta("Agende uma avaliação")}"""
    dados = [
        {**CONSULTORIO},
        faq_ld(FAQ_HOME),
        PROFISSIONAL,
        {"@type": "WebSite", "@id": f"{SITE}/#site", "url": f"{SITE}/", "name": NOME_CURTO, "inLanguage": "pt-BR", "publisher": {"@id": f"{SITE}/#consultorio"}},
    ]
    pagina(
        "",
        "Cirurgião Bucomaxilofacial em Curitiba | Dr. Daniel Negrelle",
        "Especialista em Cirurgia Bucomaxilofacial em Curitiba: ortognática, DTM e ATM, trauma facial, sisos e implantes. Consultório no Hospital São Lucas. CRO-PR 16620.",
        corpo,
        dados,
    )


def gerar_sobre():
    corpo = f"""<div class="hero hero-int">
  <div class="wrap">
    <nav class="migalhas" aria-label="Você está em"><a href="/">Início</a> › Sobre</nav>
    <h1>{esc(NOME)}</h1>
    <p>Cirurgião-dentista especialista em {esc(AREA)}, com consultório no {esc(HOSPITAL)}, em Curitiba, Paraná. {esc(CRO)}.</p>
  </div>
</div>
<div class="wrap texto">
<section>
  <img class="foto-perfil" src="/img/dr-daniel-negrelle.webp" alt="Dr. Daniel Bonato Negrelle, especialista em Cirurgia e Traumatologia Bucomaxilofacial em Curitiba" width="390" height="390">
  <h2>Atuação</h2>
  <p>O Dr. Daniel Negrelle dedica-se ao diagnóstico, ao planejamento e ao tratamento de casos da face, dos maxilares e da articulação temporomandibular, com atenção especial à <a href="/cirurgia-ortognatica/">cirurgia ortognática</a>, à <a href="/dtm-atm-dor-orofacial/">DTM e às alterações da ATM</a> e ao <a href="/trauma-facial-fraturas/">trauma facial</a>. Também realiza <a href="/sisos-cirurgia-oral/">cirurgias de sisos</a> e cirurgia oral, <a href="/implantes-enxertos/">implantes, enxertos ósseos e próteses sobre implantes</a>, da cirurgia guiada à prótese feita por escaneamento intraoral, o tratamento de <a href="/patologias-dos-maxilares/">patologias dos maxilares</a> e a <a href="/mentoplastia/">mentoplastia</a>.</p>
  <p>O consultório fica dentro do {esc(HOSPITAL)}, o que integra o atendimento ambulatorial à estrutura hospitalar onde são realizadas as cirurgias de maior porte e o tratamento das fraturas da face. Quando indicado, procedimentos são feitos com <a href="/sedacao-e-ambiente-hospitalar/">sedação endovenosa conduzida por médico anestesiologista</a>.</p>
</section>
<section>
  <h2>Formação</h2>
  <ul>
    <li>Graduação em Odontologia pela Universidade Federal do Paraná (UFPR), 2004.</li>
    <li>Especialização em Cirurgia e Traumatologia Bucomaxilofacial pelo Hospital das Clínicas da Faculdade de Medicina da USP (HC-FMUSP), 2007.</li>
    <li>Mestrado pela Universidade Federal do Paraná (UFPR), 2018.</li>
  </ul>
  <p>Especialista inscrito no {esc(CRO)}. <a href="https://br.linkedin.com/in/daniel-negrelle-3a6968131">Perfil no LinkedIn</a>.</p>
</section>
<section>
  <h2>Filosofia de trabalho</h2>
  <p>Cada caso começa pelo diagnóstico. Exames clínicos e de imagem são integrados ao planejamento para definir a indicação, as alternativas e a estratégia de tratamento mais adequada. O paciente acompanha esse raciocínio e participa das decisões, com informações claras sobre o que esperar em cada etapa.</p>
</section>
<section>
  <h2>Tecnologia e desenvolvimento</h2>
  <p>O planejamento virtual tridimensional, a análise digital da oclusão e os guias cirúrgicos impressos em 3D fazem parte da rotina de planejamento dos casos em que trazem mais precisão. Além de usar a tecnologia existente, o Dr. Daniel participa do desenvolvimento de novas ferramentas a partir de problemas clínicos reais, como o OcclusaLab, que trabalha com modelos digitais para a análise e a simulação da oclusão no planejamento ortodôntico-cirúrgico. <a href="/tecnologia-e-planejamento/">Saiba mais</a>.</p>
</section>
</div>
{cta("Agende uma avaliação")}"""
    dados = [
        {"@type": "ProfilePage", "url": f"{SITE}/sobre/", "name": f"Sobre o {NOME_CURTO}", "mainEntity": {"@id": f"{SITE}/#daniel"}},
        PROFISSIONAL,
        CONSULTORIO,
        migalhas("Sobre", "sobre/"),
    ]
    pagina("sobre/", f"Sobre o {NOME_CURTO} | Cirurgião Bucomaxilofacial em Curitiba",
           f"Conheça o {NOME}, cirurgião-dentista especialista em Cirurgia e Traumatologia Bucomaxilofacial, com consultório no {HOSPITAL}, em Curitiba. {CRO}.", corpo, dados)


def gerar_contato():
    corpo = f"""<div class="hero hero-int">
  <div class="wrap">
    <nav class="migalhas" aria-label="Você está em"><a href="/">Início</a> › Contato</nav>
    <h1>Contato e agendamento</h1>
    <p>Fale com a equipe do consultório para agendar uma avaliação ou tirar dúvidas sobre o atendimento.</p>
  </div>
</div>
<div class="wrap texto">
<section class="contato">
  <div class="card">
    <dl>
      <div><dt>Endereço</dt><dd><a href="{MAPA}">{esc(ENDERECO_TXT)}</a></dd></div>
      <div><dt>Celular e WhatsApp</dt><dd><a href="{WA_LINK}">{esc(TELEFONE)}</a></dd></div>
      <div><dt>Telefone fixo</dt><dd><a href="tel:{FIXO_E164}">{esc(FIXO)}</a></dd></div>
      <div><dt>Horário</dt><dd>{esc(HORARIO_TXT)}</dd></div>
      <div><dt>E-mail</dt><dd><a href="mailto:{EMAIL}">{esc(EMAIL)}</a></dd></div>
    </dl>
  </div>
  <h2>O consultório</h2>
  <p>O consultório fica dentro do Hospital São Lucas, em Curitiba.</p>
  <div class="fotos">
    <img src="/img/consultorio-recepcao.webp" alt="Recepção do consultório do Dr. Daniel Negrelle no Hospital São Lucas" width="680" height="453" loading="lazy">
    <img src="/img/consultorio-sala.webp" alt="Sala de atendimento do consultório do Dr. Daniel Negrelle" width="680" height="453" loading="lazy">
  </div>
  <p class="nota">Em caso de trauma recente no rosto com sangramento intenso, dificuldade para respirar ou perda de consciência, procure imediatamente um pronto-socorro.</p>
</section>
</div>"""
    dados = [{"@type": "ContactPage", "url": f"{SITE}/contato/", "name": "Contato"}, CONSULTORIO, migalhas("Contato", "contato/")]
    pagina("contato/", f"Contato | {NOME_CURTO} · Cirurgião Bucomaxilofacial em Curitiba",
           f"Agende uma avaliação com o {NOME_CURTO} em Curitiba: {ENDERECO_TXT}. Celular e WhatsApp {TELEFONE}.", corpo, dados)


# Endereços do site antigo (WordPress, 2021) que apontam para as páginas novas.
REDIRECIONA = {
    "2021/11/09/implantes-dentais-6/": "implantes-enxertos/",
}


def gerar_redirecionamentos():
    # O GitHub Pages não faz redirecionamento no servidor; o meta refresh imediato
    # com canonical é tratado pelo Google como redirecionamento permanente.
    for antigo, novo in REDIRECIONA.items():
        destino = f"{SITE}/{novo}"
        pasta = os.path.join(RAIZ, antigo)
        os.makedirs(pasta, exist_ok=True)
        with open(os.path.join(pasta, "index.html"), "w", encoding="utf-8") as f:
            f.write(f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><title>Redirecionando…</title>
<link rel="canonical" href="{destino}">
<meta http-equiv="refresh" content="0; url={destino}"></head>
<body><p>Esta página mudou para <a href="{destino}">{destino}</a>.</p></body></html>
''')


def gerar_404():
    # Página mostrada pelo GitHub Pages para endereços que não existem (inclui links antigos do domínio).
    corpo = f"""<div class="hero hero-int">
  <div class="wrap">
    <h1>Página não encontrada</h1>
    <p>O endereço que você abriu não existe mais ou foi digitado errado.</p>
  </div>
</div>
<div class="wrap texto">
<section>
  <p>Veja as <a href="/#areas">áreas de atuação</a>, conheça o <a href="/sobre/">Dr. Daniel Negrelle</a> ou fale com o consultório pela página de <a href="/contato/">contato</a>.</p>
</section>
</div>"""
    pagina("404.html", f"Página não encontrada | {NOME_CURTO}", "Página não encontrada.", corpo)


def gerar_privacidade():
    # Mantém o texto da política (link da App Store) e só troca o cabeçalho e o rodapé.
    origem = os.path.join(os.path.dirname(__file__), "privacidade-texto.html")
    with open(origem, encoding="utf-8") as f:
        artigo = f.read()
    pagina("privacidade.html", "Política de Privacidade · App do Paciente · Dr. Daniel Negrelle",
           "Como o app do paciente do consultório Dr. Daniel Negrelle trata os seus dados, conforme a LGPD.",
           f'<div class="wrap">{artigo}</div>')


def gerar_mapa_do_site():
    urls = [""] + [f"{s}/" for s in DESTAQUES + OUTRAS] + ["sedacao-e-ambiente-hospitalar/", "tecnologia-e-planejamento/", "sobre/", "contato/", "privacidade.html"]
    itens = "".join(f"<url><loc>{SITE}/{u}</loc></url>" for u in urls)
    with open(os.path.join(RAIZ, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{itens}</urlset>\n')
    with open(os.path.join(RAIZ, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nDisallow: /gerador/\n\nSitemap: {SITE}/sitemap.xml\n")


if __name__ == "__main__":
    gerar_home()
    for a in AREAS:
        gerar_area(a)
    gerar_area(TECNOLOGIA)
    gerar_area(SEDACAO)
    gerar_sobre()
    gerar_contato()
    gerar_privacidade()
    gerar_404()
    gerar_redirecionamentos()
    gerar_mapa_do_site()
    print("Páginas geradas.")
