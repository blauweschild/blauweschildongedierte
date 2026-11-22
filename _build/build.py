#!/usr/bin/env python3
"""Maakt alle pagina's van de Blauweschild-website.

Gebruik (vanuit de hoofdmap van de repo):
    python3 _build/build.py

Teksten staan in _build/content.py. Stijl in css/site.css, scripts in js/.
Let op: handmatige wijzigingen in de gegenereerde index.html-bestanden
worden overschreven als je dit script opnieuw draait.
"""
import os, sys
from html import escape as E

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from content import *  # noqa

SHIELD = '<svg viewBox="0 0 22 26" aria-hidden="true"><path d="M1 1h20v10c0 7-5 11-10 14C6 22 1 18 1 11z" fill="#3a74ff"/><path d="M6 12.5l3.5 3.5L16 9" stroke="#d6e3ff" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
PEST = {p["slug"]: p for p in PESTS}


def u(root, path=""):
    """Relatieve link naar een pagina, werkt ook zonder server (file://)."""
    return root + (path + "/" if path else "") + "index.html"


def tel_link(text=None, cls=""):
    return f'<a class="{cls}" href="{TEL_HREF}">{E(text or TEL)}</a>' if cls else f'<a href="{TEL_HREF}">{E(text or TEL)}</a>'


# ---------------------------------------------------------------- vaste delen
def nav(root, cur, home):
    def cur_attr(key):
        return ' aria-current="page"' if cur == key else ""
    pests = "".join(f'<a href="{u(root, "ongedierte/" + p["slug"])}"{cur_attr("ongedierte/" + p["slug"])}>{E(p["name"])}<small>{E(p["lat"])}</small></a>' for p in PESTS)
    provs = "".join(f'<a href="{u(root, "locaties/" + p["slug"])}"{cur_attr("locaties/" + p["slug"])}>{E(p["name"])}</a>' for p in PROVINCES)
    on_p = " on" if cur.startswith("ongedierte") or cur == "diensten" else ""
    on_l = " on" if cur.startswith("locaties") else ""
    inspect = "#contact" if home else u(root, "contact")
    m_pests = "".join(f'<li><a href="{u(root, "ongedierte/" + p["slug"])}"{cur_attr("ongedierte/" + p["slug"])}>{E(p["name"])}</a></li>' for p in PESTS)
    m_provs = "".join(f'<li><a href="{u(root, "locaties/" + p["slug"])}"{cur_attr("locaties/" + p["slug"])}>{E(p["name"])}</a></li>' for p in PROVINCES)
    return f'''<a class="skip" href="#main">Naar de inhoud</a>
<nav class="nav" aria-label="Hoofdmenu">
  <div class="wrap">
    <a class="brand" href="{u(root)}">{SHIELD}Blauweschild</a>
    <ul class="menu">
      <li class="dd{on_p}"><button type="button" aria-expanded="false" aria-controls="dd-ong">Ongedierte</button>
        <div class="dd-panel" id="dd-ong" hidden>{pests}<a class="all" href="{u(root, "diensten")}"{cur_attr("diensten")}>Alle diensten</a></div></li>
      <li class="dd{on_l}"><button type="button" aria-expanded="false" aria-controls="dd-loc">Locaties</button>
        <div class="dd-panel" id="dd-loc" hidden>{provs}<a class="all" href="{u(root, "locaties")}"{cur_attr("locaties")}>Heel Nederland</a></div></li>
      <li><a href="{u(root, "spoed")}"{cur_attr("spoed")}>Spoed</a></li>
      <li><a href="{u(root, "over-ons")}"{cur_attr("over-ons")}>Over ons</a></li>
      <li><a href="{u(root, "vacatures")}"{cur_attr("vacatures")}>Vacatures</a></li>
      <li><a href="{u(root, "contact")}"{cur_attr("contact")}>Contact</a></li>
    </ul>
    <div class="nav-cta">
      <button class="btn btn-spoed" type="button" data-spoed aria-haspopup="dialog"><span class="pulse"></span>Spoed</button>
      <a class="btn btn-primary" href="{inspect}">Inspectie aanvragen</a>
      <button class="burger" id="burger" type="button" aria-expanded="false" aria-controls="mnav" aria-label="Menu openen"><span></span></button>
    </div>
  </div>
</nav>
<div class="mnav" id="mnav" hidden role="dialog" aria-modal="true" aria-label="Menu">
  <div class="mnav-top"><a class="brand" href="{u(root)}">{SHIELD}Blauweschild</a><button type="button" data-close aria-label="Menu sluiten">×</button></div>
  <h2>Ongedierte</h2><ul>{m_pests}</ul>
  <h2>Locaties</h2><ul>{m_provs}</ul>
  <h2>Bedrijf</h2>
  <ul class="one">
    <li><a href="{u(root)}"{cur_attr("")}>Home</a></li>
    <li><a href="{u(root, "diensten")}"{cur_attr("diensten")}>Diensten</a></li>
    <li><a href="{u(root, "spoed")}"{cur_attr("spoed")}>Spoedhulp</a></li>
    <li><a href="{u(root, "over-ons")}"{cur_attr("over-ons")}>Over ons</a></li>
    <li><a href="{u(root, "vacatures")}"{cur_attr("vacatures")}>Vacatures</a></li>
    <li><a href="{u(root, "contact")}"{cur_attr("contact")}>Contact</a></li>
  </ul>
  <a class="btn btn-primary" href="{TEL_HREF}">Bel {E(TEL)}</a>
</div>'''


def sheet(root):
    return f'''<button class="btn btn-spoed fab" type="button" data-spoed aria-haspopup="dialog"><span class="pulse"></span>Spoed? Bel ons</button>

<div class="sheet-bg" id="spoed" hidden>
  <div class="sheet" role="dialog" aria-modal="true" aria-labelledby="spoed-h">
    <button class="x" type="button" id="spoed-x" aria-label="Sluiten">×</button>
    <div class="eyebrow">Spoedhulp</div>
    <h2 id="spoed-h">Direct hulp bij ongedierte</h2>
    <ul>
      <li>Muizen of ratten die met de kou naar binnen trekken</li>
      <li>Een wespennest bij de deur, dakrand of speelplek</li>
      <li>Bedwantsen of kakkerlakken</li>
    </ul>
    <div class="bignum"><strong id="spoed-nr">{E(TEL)}</strong><button class="copy" type="button" id="spoed-copy">Kopieer nummer</button></div>
    <a class="btn btn-spoed" href="{TEL_HREF}" style="justify-content:center;font-size:1.05rem;padding:15px"><span class="pulse"></span>Bel nu met spoed</a>
    <form data-form="Spoed" data-subject="SPOED terugbelverzoek" novalidate>
      <p class="small">Of laat je nummer achter, dan bellen we je zo snel mogelijk terug. <a href="{u(root, "spoed")}">Meer over spoedhulp</a></p>
      <div class="row">
        <label for="s-naam">Naam<input id="s-naam" name="naam" autocomplete="name"></label>
        <label for="s-tel"><span>Telefoonnummer <span class="req">*</span></span><input id="s-tel" name="telefoon" type="tel" autocomplete="tel" required></label>
      </div>
      <button class="btn btn-ghost" type="submit">Bel mij terug</button>
      <div class="sent" hidden></div>
    </form>
  </div>
</div>'''


def footer(root):
    kvk = E(KVK) if KVK else '<span class="ph">[nummer]</span>'
    pests = "".join(f'<li><a href="{u(root, "ongedierte/" + p["slug"])}">{E(p["name"])}</a></li>' for p in PESTS)
    return f'''<footer>
  <div class="wrap cols">
    <div>
      <a class="brand" href="{u(root)}">{SHIELD}Blauweschild</a>
      <p style="margin:0">Ongediertebestrijding voor particulier en zakelijk, door heel Nederland. Snel, effectief en met garantie op resultaat.</p>
      <ul class="ticks" style="font-size:.9rem"><li>Gecertificeerde specialisten</li><li>Spoedservice, 7 dagen per week</li><li>Preventie volgens IPM</li></ul>
    </div>
    <div><h2>Ongedierte</h2><ul>{pests}</ul></div>
    <div><h2>Bedrijf</h2><ul>
      <li><a href="{u(root)}">Home</a></li>
      <li><a href="{u(root, "diensten")}">Diensten</a></li>
      <li><a href="{u(root, "locaties")}">Locaties</a></li>
      <li><a href="{u(root, "spoed")}">Spoedservice</a></li>
      <li><a href="{u(root, "over-ons")}">Over ons</a></li>
      <li><a href="{u(root, "vacatures")}">Vacatures</a></li>
      <li><a href="{u(root, "contact")}">Contact</a></li>
    </ul></div>
    <div><h2>Contact</h2>
      <dl class="spec-dl" style="display:grid;gap:10px;margin:0">
        <div><dt class="small">Bel ons</dt><dd style="margin:0"><a href="{TEL_HREF}" style="font-weight:600;color:var(--text);font-variant-numeric:tabular-nums">{E(TEL)}</a></dd></div>
        <div><dt class="small">E-mail</dt><dd style="margin:0"><a href="mailto:{MAIL}" style="font-weight:600;color:var(--text);overflow-wrap:anywhere">{E(MAIL)}</a></dd></div>
        <div><dt class="small">Bereikbaar</dt><dd style="margin:0;color:var(--text)">7 dagen per week, 08:00–17:00</dd></div>
        <div><dt class="small">Werkgebied</dt><dd style="margin:0;color:var(--text)">Heel Nederland</dd></div>
      </dl>
    </div>
  </div>
  <div class="wrap bottom">
    <span>© 2026 Blauweschild Ongediertebestrijding</span>
    <span>KvK {kvk}</span>
  </div>
</footer>'''


def page(path, title, desc, main, home=False, extra_head="", scripts=""):
    depth = 0 if path == "" else path.count("/") + 1
    root = "../" * depth
    full_title = title if home else f"{title} – Blauweschild Ongediertebestrijding"
    html = f'''<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(full_title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="theme-color" content="#071029">
<link rel="icon" href="data:image/svg+xml,{E('<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 22 26%22><path d=%22M1 1h20v10c0 7-5 11-10 14C6 22 1 18 1 11z%22 fill=%22%233a74ff%22/></svg>')}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Instrument+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="{root}css/site.css">{extra_head}
</head><body data-root="{root}">
{nav(root, path, home)}
<main id="main">
{main(root)}
</main>
{sheet(root)}
{footer(root)}
<script src="{root}js/site.js"></script>{scripts}
</body></html>
'''
    d = os.path.join(OUT, path)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    return path or "/"


# ---------------------------------------------------------------- bouwstenen
def crumbs(root, items):
    li = [f'<li><a href="{u(root)}">Home</a></li>']
    for label, path in items:
        li.append(f'<li><a href="{u(root, path)}">{E(label)}</a></li>' if path is not None else f'<li aria-current="page">{E(label)}</li>')
    return f'<ol class="crumbs" aria-label="Kruimelpad">{"".join(li)}</ol>'


def head(eyebrow, h2, p=None, hid=None):
    idattr = f' id="{hid}"' if hid else ""
    return f'<div class="head"><div class="eyebrow">{E(eyebrow)}</div><h2{idattr}>{h2}</h2>{f"<p>{p}</p>" if p else ""}</div>'


def section(sid, inner, solid=False, label=None):
    cls = "block solid" if solid else "block"
    lab = f' aria-labelledby="{label}"' if label else ""
    idattr = f' id="{sid}"' if sid else ""
    return f'<section class="{cls}"{idattr}{lab} style="background:var(--ink)"><div class="wrap">{inner}</div></section>'


def actions(root, primary=True, inspect_href=None):
    return f'''<div class="actions">
        <a class="btn btn-spoed" href="{TEL_HREF}"><span class="pulse"></span>Bel {E(TEL)}</a>
        <a class="btn btn-primary" href="{inspect_href or u(root, "contact")}">Plan een inspectie</a>
      </div>'''


def pest_grid(root, cls="grid", local=None):
    out = []
    for i, p in enumerate(PESTS):
        txt = E(p["kort"]) if not local else E(local(i, p))
        sp = '<span class="spoed">Spoed mogelijk</span>' if p["spoed"] else ""
        out.append(f'<a class="svc" href="{u(root, "ongedierte/" + p["slug"])}"><span class="lat">{E(p["lat"])}</span><h3>{E(p["name"])}</h3><p>{txt}</p>{sp}<span class="more">Meer info</span></a>')
    return f'<div class="{cls}">{"".join(out)}</div>'


def steps():
    return '<ol class="steps">' + "".join(f"<li><h3>{E(a)}</h3><p>{E(b)}</p></li>" for a, b in STEPS) + "</ol>"


def ipm():
    return '<div class="ipm"><strong>IPM</strong><p>We werken volgens Integrated Pest Management: eerst voorkomen en weren, dan pas bestrijden. Middelen zetten we alleen in waar het nodig is.</p></div>'


def why(items=WHY):
    return '<div class="why">' + "".join(f"<div><b>{E(a)}</b><h3>{E(b)}</h3><p>{E(c)}</p></div>" for a, b, c in items) + "</div>"


def stats(items=STATS):
    return '<div class="stats">' + "".join(f"<div><strong>{E(a)}</strong><span>{E(b)}</span></div>" for a, b in items) + "</div>"


def reviews(only=None):
    rs = [r for r in REVIEWS if not only or r[3] in only]
    if not rs:
        return ""
    cards = "".join(
        f'<figure class="review"><div class="stars" aria-label="5 van 5 sterren">★★★★★</div><blockquote>“{E(q)}”</blockquote>'
        f'<figcaption><b>{E(n)}</b><span>{E(PEST[s]["name"])} · {E(c)}</span></figcaption></figure>'
        for q, n, c, s in rs)
    return f'<div class="reviews">{cards}</div>'


def faq(items):
    return '<div class="faq">' + "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in items) + "</div>"


def cta(h, p):
    return f'''<div class="cta"><div><h2>{h}</h2><p>{p}</p></div>
      <div class="actions"><a class="btn btn-spoed" href="{TEL_HREF}"><span class="pulse"></span>Bel {E(TEL)}</a><button class="btn btn-ghost" type="button" data-spoed>Terugbelverzoek</button></div></div>'''


def contact_form(fid, subject, redirect=True, extra=""):
    soorten = "".join(f"<option>{E(p['name'])}</option>" for p in PESTS) + "<option>Anders of weet ik niet</option>"
    return f'''<form data-form="Inspectie" data-subject="{E(subject)}"{' data-redirect' if redirect else ''} novalidate>
        <div class="hp" aria-hidden="true"><label>Laat leeg<input name="_gotcha" tabindex="-1" autocomplete="off"></label></div>
        <div class="row">
          <label for="{fid}-naam"><span>Naam <span class="req">*</span></span><input id="{fid}-naam" name="naam" autocomplete="name" required></label>
          <label for="{fid}-tel"><span>Telefoonnummer <span class="req">*</span></span><input id="{fid}-tel" name="telefoon" type="tel" autocomplete="tel" required></label>
        </div>
        {extra}
        <div class="row">
          <label for="{fid}-pc">Postcode of plaats<input id="{fid}-pc" name="plaats" autocomplete="postal-code" placeholder="1234 AB"></label>
          <label for="{fid}-soort">Wat speelt er?
            <select id="{fid}-soort" name="plaagdier">{soorten}</select>
          </label>
        </div>
        <label for="{fid}-msg">Toelichting<textarea id="{fid}-msg" name="toelichting" placeholder="Waar zie je het, sinds wanneer?"></textarea></label>
        <button class="btn btn-primary" type="submit">Verstuur aanvraag</button>
        <p class="small">Door te versturen ga je akkoord met het verwerken van je gegevens om contact met je op te nemen over je aanvraag.</p>
        <div class="sent" hidden></div>
      </form>'''


def contact_dl():
    return f'''<dl>
        <dt>Telefoon</dt><dd><a href="{TEL_HREF}" style="font-weight:600;text-decoration:none;font-variant-numeric:tabular-nums">{E(TEL)}</a></dd>
        <dt>E-mail</dt><dd><a href="mailto:{MAIL}" style="font-weight:600;text-decoration:none;overflow-wrap:anywhere">{E(MAIL)}</a></dd>
        <dt>Open</dt><dd>7 dagen per week, 08:00–17:00</dd>
      </dl>'''


def phero(root, crumb_items, eyebrow, h1, lead, side="", facts=None, narrow=False, inspect_href=None):
    f = ""
    if facts:
        f = '<ul class="facts">' + "".join(f"<li>{E(x)}</li>" for x in facts) + "</ul>"
    cls = "phero narrow" if narrow or not side else "phero"
    return f'''<header class="{cls}">
  <div class="wrap">
    <div>
      {crumbs(root, crumb_items)}
      <div class="eyebrow">{E(eyebrow)}</div>
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
      {actions(root, inspect_href=inspect_href)}
      {f}
    </div>
    {side}
  </div>
</header>'''


# ---------------------------------------------------------------- pagina's
built = []

# --- homepage
def home_main(root):
    chips = "".join(f'<li><a href="{u(root, "locaties/" + p["slug"])}">{E(p["name"])}</a></li>' for p in PROVINCES)
    return f'''<header class="hero" id="top">
  <div class="wrap">
    <div>
      <div class="eyebrow">Ongediertebestrijding</div>
      <h1>Wij houden <em>ongedierte</em> buiten de deur.</h1>
      <p class="lead">Als het kouder wordt, trekken muizen en ratten naar binnen, op zoek naar warmte en eten. Ook bedwantsen na een vakantie of kakkerlakken in de keuken pakken we aan. Blauweschild zoekt uit waar het vandaan komt, lost het op en sluit de toegang af zodat het niet terugkomt.</p>
      <div class="actions">
        <a class="btn btn-primary" href="#contact">Plan een inspectie</a>
        <button class="btn btn-spoed" type="button" data-spoed><span class="pulse"></span>Spoedhulp</button>
        <a class="btn btn-ghost" href="#check">Wat zit er in huis?</a>
      </div>
      <ul class="facts">
        <li>Binnen 24 uur ter plaatse</li>
        <li>Garantie op resultaat</li>
        <li>Preventie volgens IPM</li>
      </ul>
    </div>
    <div class="stage" data-stage>
      <div class="fallback" aria-hidden="true">{SHIELD}</div>
    </div>
  </div>
</header>

<section class="block solid" id="check" aria-labelledby="check-h">
  <div class="wrap">
    {head("Plaagcheck", "Wat zie of hoor je in huis?", "Tik aan wat je herkent. Je ziet meteen welk plaagdier het meest waarschijnlijk is en wat je nu kunt doen.", "check-h")}
    <div class="check">
      <div class="signs" id="signs" role="group" aria-label="Signalen"></div>
      <div class="result" aria-live="polite">
        <span class="tag" id="r-tag">Meest waarschijnlijk</span>
        <h3 id="r-name">Muizen</h3>
        <span class="urg" id="r-urg">Binnen een week</span>
        <p id="r-advice"></p>
        <div class="meter" id="r-meter"></div>
        <a class="more" id="r-more" href="{u(root, "ongedierte/muizen")}">Alles over muizen →</a>
        <span class="note" id="r-note">Voorbeeld: twee signalen staan al aan. Pas ze aan naar jouw situatie.</span>
      </div>
    </div>
  </div>
</section>

<section class="block" id="diensten" aria-labelledby="diensten-h" style="background:var(--ink)">
  <div class="wrap">
    {head("Diensten", "Van knaagdier tot kruipend insect", "Elke soort vraagt een andere aanpak. We kijken eerst naar gedrag en toegangswegen, en pas daarna naar middelen.", "diensten-h")}
    {pest_grid(root)}
  </div>
</section>

<section class="block solid" id="werkwijze" aria-labelledby="werk-h">
  <div class="wrap">
    {head("Werkwijze", "Zo pakken we het aan", None, "werk-h")}
    {steps()}
    {ipm()}
  </div>
</section>

<section class="block" aria-labelledby="why-h" style="background:var(--ink)">
  <div class="wrap">
    {head("Waarom Blauweschild", "Snel ter plaatse, blijvend resultaat", "We combineren snelheid, vakmanschap en eerlijk advies.", "why-h")}
    {why()}
    {stats()}
  </div>
</section>

<section class="block solid" aria-labelledby="rev-h">
  <div class="wrap">
    {head("Reviews", "Wat klanten zeggen", '<span class="score"><b>4,9</b> / 5 op Google</span>', "rev-h")}
    {reviews()}
  </div>
</section>

<section class="block" aria-labelledby="loc-h" style="background:var(--ink)">
  <div class="wrap">
    {head("Werkgebied", "Door heel Nederland", "We zijn actief in deze provincies. Kies je regio voor meer informatie.", "loc-h")}
    <ul class="chips">{chips}</ul>
  </div>
</section>

<section class="block solid" aria-labelledby="faq-h">
  <div class="wrap">
    {head("Veelgestelde vragen", "Goed om te weten", None, "faq-h")}
    {faq(FAQ)}
  </div>
</section>

<section class="block contact" id="contact" aria-labelledby="contact-h" style="background:color-mix(in srgb,var(--ink) 55%,transparent)">
  <div class="wrap">
    <div class="contact-side">
      {head("Contact", "Last van ongedierte? Vraag een inspectie aan.", "Laat je gegevens achter, dan bellen we je terug om een afspraak te plannen.", "contact-h")}
      {contact_dl()}
      {contact_form("f", "Inspectie-aanvraag")}
    </div>
    <div class="stage" data-stage></div>
  </div>
</section>'''

built.append(page("", "Blauweschild Ongediertebestrijding",
    f"Ongediertebestrijding door heel Nederland. Binnen 24 uur ter plaatse, preventie volgens IPM en garantie op resultaat. Bel {TEL}.",
    lambda r: '<canvas id="scene" aria-hidden="true"></canvas>\n<div id="tags3d" aria-hidden="true"></div>\n' + home_main(r), home=True,
    scripts='\n<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>\n<script src="js/scene.js"></script>'))


# --- diensten
def diensten_main(root):
    return phero(root, [("Diensten", None)], "Diensten", "Onze <em>diensten</em>",
        "Professionele bestrijding van alle soorten ongedierte. Snel, effectief en met garantie op resultaat, voor particulieren en bedrijven.",
        facts=["Binnen 24 uur hulp", "Garantie op resultaat", "Veilig voor kinderen en huisdieren"]) + \
    section("", head("Welk ongedierte?", "Kies het plaagdier", "Klik op een soort voor uitleg, onze aanpak en veelgestelde vragen.") + pest_grid(root)) + \
    section("", head("Werkwijze", "Zo pakken we het aan") + steps() + ipm(), solid=True) + \
    section("", head("Waarom Blauweschild", "Snel ter plaatse, blijvend resultaat") + why() + stats()) + \
    section("", head("Veelgestelde vragen", "Goed om te weten") + faq(FAQ), solid=True) + \
    section("", cta("Direct hulp nodig?", "Onze specialisten staan voor je klaar. Bel voor snelle, professionele hulp."))

built.append(page("diensten", "Diensten", "Alle diensten van Blauweschild: bestrijding van muizen, ratten, wespen, bedwantsen, vlooien, mieren, kakkerlakken en zilvervisjes.", diensten_main))


# --- ongedierte
for p in PESTS:
    def pest_main(root, p=p):
        signs = "".join(f"<li>{E(s)}</li>" for s in p["signs"])
        urg_cls = "urg hot" if p["spoed"] else "urg"
        side = f'''<aside class="spec" aria-label="Soortkaart {E(p["name"])}">
      <span class="tag">Soortkaart</span>
      <div><h2 style="font-size:1.8rem">{E(p["name"])}</h2><span class="lat">{E(p["lat"])}</span></div>
      <div class="big">{E(p["big"][0])}<small>{E(p["big"][1])}</small></div>
      <dl>
        <dt>Urgentie</dt><dd><span class="{urg_cls}">{E(p["urg"])}</span></dd>
        <dt>Herken je</dt><dd><ul class="ticks" style="gap:6px;font-size:.9rem">{signs}</ul></dd>
      </dl>
    </aside>'''
        others = "".join(f'<li><a href="{u(root, "ongedierte/" + o["slug"])}">{E(o["name"])}</a></li>' for o in PESTS if o is not p)
        rv = reviews([p["slug"]])
        rv_sec = section("", head("Review", "Wat klanten zeggen") + rv, solid=True) if rv else ""
        tick_li = "".join(f"<li>{E(t)}</li>" for t in p["ticks"])
        risk_li = "".join(f"<li>{E(t)}</li>" for t in p["gevaren"])
        name_l = p["name"].lower()
        return phero(root, [("Diensten", "diensten"), (p["name"], None)], p["title"], f"Last van <em>{E(name_l)}</em>?", E(p["lead"]), side,
                     facts=["Binnen 24 uur hulp", "Garantie op resultaat", "Veilig en effectief"]) + \
            section("", head("Het probleem", f"Wat je moet weten over {E(name_l)}") + f'''<div class="split">
      <div class="prose"><p>{E(p["intro"])}</p><div class="box warn"><h3>Waarom snel handelen?</h3><p>{E(p["snel"])}</p></div></div>
      <div class="box"><h3>Risico's van {E(name_l)}</h3><ul class="risks">{risk_li}</ul></div>
    </div>''') + \
            section("", head("Onze aanpak", f"Zo bestrijden we {E(name_l)}") + f'''<div class="split">
      <div class="prose"><p>{E(p["aanpak"])}</p></div>
      <div class="box"><ul class="ticks">{tick_li}</ul></div>
    </div>''' + steps(), solid=True) + rv_sec + \
            section("", head("Veelgestelde vragen", f"Vragen over {E(name_l)}") + faq(p["faq"])) + \
            section("", cta(f"Hulp nodig bij {E(name_l)}?", "Onze specialisten staan klaar. Bel voor directe hulp of laat je terugbellen.") +
                    f'<div class="head" style="gap:10px"><div class="eyebrow">Ander ongedierte</div></div><ul class="chips">{others}</ul>', solid=True)

    built.append(page("ongedierte/" + p["slug"], p["title"],
        f"{p['name']} in huis of bedrijf? {p['lead']} Bel {TEL}.", pest_main))


# --- locaties
def locaties_main(root):
    cards = "".join(f'<a href="{u(root, "locaties/" + p["slug"])}"><b>Provincie</b><h3>{E(p["name"])}</h3><p>{E(", ".join(p["cities"]))} en omgeving.</p></a>' for p in PROVINCES)
    return phero(root, [("Locaties", None)], "Werkgebied", "Ongediertebestrijding <em>door heel Nederland</em>",
        "Blauweschild is actief in meerdere provincies. Kies je provincie voor meer informatie over onze diensten in jouw regio.",
        facts=["Binnen 24 uur ter plaatse", "Spoed: dezelfde dag", "7 dagen per week bereikbaar"]) + \
        section("", head("Provincies", "Kies je regio") + f'<div class="prov">{cards}</div>') + \
        section("", cta("Direct hulp nodig?", "Onze specialisten staan 7 dagen per week voor je klaar (08:00–17:00). Bel voor snelle hulp in jouw regio."), solid=True)

built.append(page("locaties", "Locaties", "Blauweschild is actief in Noord-Holland, Zuid-Holland, Utrecht, Noord-Brabant, Gelderland, Flevoland en Overijssel.", locaties_main))

for pr in PROVINCES:
    def prov_main(root, pr=pr):
        c = pr["cities"]
        cl = ", ".join(c[:-1]) + " en " + c[-1] if len(c) > 1 else c[0]
        chips = "".join(f"<li>{E(x)}</li>" for x in c)
        side = f'''<aside class="spec" aria-label="Werkgebied {E(pr["name"])}">
      <span class="tag">Werkgebied</span>
      <div><h2 style="font-size:1.8rem">{E(pr["name"])}</h2><span class="lat">Provincie</span></div>
      <div class="big">24 uur<small>en we zijn bij je ter plaatse</small></div>
      <dl>
        <dt>Steden</dt><dd>{E(", ".join(c))}</dd>
        <dt>Spoed</dt><dd><span class="urg hot">Dezelfde dag</span></dd>
        <dt>Bereikbaar</dt><dd>7 dagen per week, 08:00–17:00</dd>
      </dl>
    </aside>'''

        def local(i, p):
            a, b = c[i % len(c)], c[(i + 1) % len(c)]
            return f"{p['kort']} Ook in {a}, {b} en omgeving."
        why_local = [("24 uur", "Snel in de regio", f"Snel ter plaatse in heel {pr['name']}, ook in {c[0]} en {c[1]}.")] + WHY[1:]
        others = "".join(f'<li><a href="{u(root, "locaties/" + o["slug"])}">{E(o["name"])}</a></li>' for o in PROVINCES if o is not pr)
        return phero(root, [("Locaties", "locaties"), (pr["name"], None)], "Werkgebied", f"Ongediertebestrijding in <em>{E(pr['name'])}</em>",
                     E(f"Actief in {cl} en heel {pr['name'] if pr['slug'] != 'utrecht' else 'de provincie Utrecht'}. Binnen 24 uur hulp bij ongedierte: effectief, discreet en met garantie op resultaat."), side) + \
            section("", head("Plaatsen", f"Hier zijn we actief") + f'<ul class="chips">{chips}</ul><p class="small" style="font-size:.95rem">Woon je ergens anders in {E(pr["name"])}? Ook dan komen we graag langs.</p>') + \
            section("", head("Diensten", f"Welk ongedierte in {E(pr['name'])}?", f"We bestrijden alle soorten ongedierte in {E(pr['name'])}, voor particulieren en bedrijven.") + pest_grid(root, local=local), solid=True) + \
            section("", head("Waarom Blauweschild", f"Jouw specialist in {E(pr['name'])}") + why(why_local)) + \
            section("", cta(f"Direct hulp in {E(pr['name'])}?", f"Bel ons voor snelle, professionele ongediertebestrijding in {E(cl)} en de rest van {E(pr['name'])}.") +
                    f'<div class="head" style="gap:10px"><div class="eyebrow">Andere provincies</div></div><ul class="chips">{others}</ul>', solid=True)

    built.append(page("locaties/" + pr["slug"], f"Ongediertebestrijding {pr['name']}",
        f"Ongediertebestrijding in {pr['name']}: actief in {', '.join(pr['cities'])}. Binnen 24 uur ter plaatse. Bel {TEL}.", prov_main))


# --- spoed
SPOED_ADVICE = {
    "ratten": "Houd deuren naar kruipruimte en kelder dicht en zet voedsel weg. Raak keutels niet met blote handen aan.",
    "bedwantsen": "Was beddengoed op 60 °C en neem geen spullen mee naar andere kamers.",
    "wespen": "Blijf uit de buurt van de opening en sluit hem niet zelf af; de wespen zoeken dan een weg naar binnen.",
    "kakkerlakken": "Ruim voedselresten op en zet etenswaren in afgesloten bakken. Gebruik geen spray: die verjaagt ze naar andere plekken.",
}

def spoed_main(root):
    cards = "".join(
        f'<a class="svc" href="{u(root, "ongedierte/" + s)}"><span class="spoed" style="margin:0">Urgent</span><h3>{E(PEST[s]["name"])}</h3><p>{E(t)}</p><span class="more">Meer info</span></a>'
        for s, t in SPOED_ADVICE.items())
    spoed_steps = [("Bel ons", "Neem direct telefonisch contact op. We staan klaar."), ("Inspectie", "Onze specialist komt dezelfde dag voor een inspectie."),
                   ("Behandeling", "Directe bestrijding met professionele middelen."), ("Garantie", "Controle en garantie dat het probleem is opgelost.")]
    st = '<ol class="steps">' + "".join(f"<li><h3>{E(a)}</h3><p>{E(b)}</p></li>" for a, b in spoed_steps) + "</ol>"
    return phero(root, [("Spoed", None)], "Spoedservice · 7 dagen per week", "Acute <em>ongedierte</em>overlast?",
        "Wacht niet langer. Onze specialisten zijn vandaag nog bij je ter plaatse. Snel, professioneel en met garantie.",
        facts=["Dezelfde dag ter plaatse", "Ook in het weekend", "Garantie op resultaat"]) + \
        section("", head("Urgente situaties", "Hier telt elk uur", "Bij deze plaagdieren is snel handelen belangrijk om schade en gezondheidsrisico's te beperken. Dit kun je alvast doen tot we er zijn.") +
                f'<div class="grid">{cards}</div>') + \
        section("", head("Zo werkt het", "Hoe werkt onze spoedservice?") + st +
                stats([("Dezelfde dag", "Ter plaatse bij spoed"), ("08:00–17:00", "Dagelijks bereikbaar"), ("7/7", "Ook in het weekend"), ("Garantie", "Op elk resultaat")]), solid=True) + \
        section("", cta("Spoed? Bel ons direct.", "Of laat je nummer achter, dan bellen we je zo snel mogelijk terug."))

built.append(page("spoed", "Spoedhulp bij ongedierte", f"Acute overlast van ratten, wespen, bedwantsen of kakkerlakken? Bel {TEL}. Dezelfde dag hulp, 7 dagen per week bereikbaar.", spoed_main))


# --- over ons
def over_main(root):
    values = [("01", "Resultaatgericht", "We stoppen pas als het probleem echt is opgelost. Met garantie op resultaat."),
              ("02", "Klantgericht", "Jouw situatie staat centraal. We luisteren, adviseren en doen wat we beloven."),
              ("03", "Betrouwbaar", "Een duidelijke werkwijze, eerlijke prijzen en afspraken die we nakomen."),
              ("04", "Vooruitstrevend", "We werken met de nieuwste technieken en middelen, en alleen waar ze nodig zijn.")]
    return phero(root, [("Over ons", None)], "Over ons", "Vakmanschap tegen <em>ongedierte</em>",
        "Al meer dan tien jaar je betrouwbare partner in professionele ongediertebestrijding.") + \
        section("", head("Ons verhaal", "Waarom Blauweschild bestaat") + f'''<div class="split">
      <div class="prose">
        <p>Blauweschild is opgericht met één doel: mensen snel en goed helpen bij overlast van ongedierte. Wat klein begon, is uitgegroeid tot een bestrijdingsbedrijf dat door heel Nederland werkt.</p>
        <p>Ons team van gecertificeerde specialisten heeft jarenlange ervaring en werkt met de nieuwste technieken en middelen. We vinden dat iedereen recht heeft op een veilige, ongediertevrije leefomgeving.</p>
        <p>Met meer dan 200 tevreden klanten en een gemiddelde Google-score van 4,9 uit 5 zijn we trots op het vertrouwen dat klanten in ons hebben.</p>
      </div>
      <div class="box"><h3>Schild om je huis</h3><p>Onze naam zegt het al: we bestrijden niet alleen wat er nu zit, we zorgen ook dat het niet terugkomt. Daarom zoeken we altijd uit hoe het ongedierte binnenkomt en sluiten we die route af.</p>{ipm()}</div>
    </div>''' + stats()) + \
        section("", head("Onze waarden", "Waar we voor staan") + why(values), solid=True) + \
        section("", cta("Kennismaken?", f"Bel ons op {E(TEL)} of vraag een inspectie aan. We denken graag met je mee."))

built.append(page("over-ons", "Over ons", "Maak kennis met Blauweschild: meer dan tien jaar ervaring, gecertificeerde specialisten en werkgebied in heel Nederland.", over_main))


# --- vacatures
def vac_main(root):
    perks = "".join(f"<li>{E(x)}</li>" for x in ["Marktconform salaris en goede secundaire arbeidsvoorwaarden", "Opleiding en begeleiding, ook zonder ervaring", "Werken door heel Nederland in een hecht team", "Doorgroeimogelijkheden binnen een groeiend bedrijf"])
    funcs = "".join(f"<option>{E(x)}</option>" for x in ["Ongediertebestrijder", "Monteur / technisch medewerker", "Klantenservice", "Open sollicitatie", "Anders"])
    return phero(root, [("Vacatures", None)], "Werken bij", "Werken bij <em>Blauweschild</em>",
        "We groeien en zoeken gemotiveerde collega's die samen met ons Nederland ongediertevrij houden.") + \
        section("", head("Waarom bij ons?", "Een vak met impact") + f'''<div class="split">
      <div class="prose">
        <p>Blauweschild groeit hard en we zijn steeds op zoek naar enthousiaste vakmensen. Heb je al ervaring in de ongediertebestrijding, of ben je gemotiveerd om het vak te leren? We horen graag van je.</p>
        <ul class="ticks">{perks}</ul>
        <div class="box"><h3>Open sollicitatie</h3><p>Staat er geen passende vacature bij? Solliciteer gerust open. We nemen elke aanmelding serieus.</p></div>
      </div>
      <form data-form="Sollicitatie" data-subject="Sollicitatie" data-redirect novalidate>
        <h2 style="font-size:1.6rem">Solliciteer direct</h2>
        <p class="small">Vul het formulier in. We nemen zo snel mogelijk contact met je op.</p>
        <div class="hp" aria-hidden="true"><label>Laat leeg<input name="_gotcha" tabindex="-1" autocomplete="off"></label></div>
        <div class="row">
          <label for="v-naam"><span>Naam <span class="req">*</span></span><input id="v-naam" name="naam" autocomplete="name" required></label>
          <label for="v-mail"><span>E-mail <span class="req">*</span></span><input id="v-mail" name="email" type="email" autocomplete="email" required></label>
        </div>
        <div class="row">
          <label for="v-tel">Telefoonnummer<input id="v-tel" name="telefoon" type="tel" autocomplete="tel"></label>
          <label for="v-func">Functie<select id="v-func" name="functie">{funcs}</select></label>
        </div>
        <label for="v-mot"><span>Motivatie <span class="req">*</span></span><textarea id="v-mot" name="motivatie" required placeholder="Vertel kort wie je bent en waarom je bij ons wilt werken."></textarea></label>
        <button class="btn btn-primary" type="submit">Verstuur sollicitatie</button>
        <p class="small">Door te versturen ga je akkoord met het verwerken van je gegevens voor deze sollicitatie.</p>
        <div class="sent" hidden></div>
      </form>
    </div>''')

built.append(page("vacatures", "Vacatures", "Werken bij Blauweschild Ongediertebestrijding. Bekijk wat we bieden en solliciteer direct via het formulier.", vac_main))


# --- contact
def contact_main(root):
    kvk = E(KVK) if KVK else '<span class="ph">[nummer]</span>'
    email_row = '<label for="c-mail">E-mail<input id="c-mail" name="email" type="email" autocomplete="email"></label>'
    return phero(root, [("Contact", None)], "Contact", "Neem <em>contact</em> op",
        "Bel ons of vul het formulier in, dan helpen we je direct verder.", inspect_href="#formulier") + \
        section("", f'''<div class="split">
      <div class="contact-side">
        {head("Direct contact", "Bel of mail ons", "Kies wat je het handigst vindt. We zijn 7 dagen per week bereikbaar.")}
        <div class="actions"><a class="btn btn-spoed" href="{TEL_HREF}"><span class="pulse"></span>Bel {E(TEL)}</a><a class="btn btn-ghost" href="mailto:{MAIL}">Stuur een e-mail</a></div>
        <p class="small" style="font-size:.95rem">Spoed? Bel direct, we zijn zo snel mogelijk bij je.</p>
        <div class="box">
          <h3>Bedrijfsgegevens</h3>
          <div class="contact-side"><dl>
            <dt>Bedrijf</dt><dd>Blauweschild Ongediertebestrijding</dd>
            <dt>Telefoon</dt><dd><a href="{TEL_HREF}" style="font-weight:600;text-decoration:none">{E(TEL)}</a></dd>
            <dt>E-mail</dt><dd><a href="mailto:{MAIL}" style="font-weight:600;text-decoration:none;overflow-wrap:anywhere">{E(MAIL)}</a></dd>
            <dt>Open</dt><dd>7 dagen per week, 08:00–17:00</dd>
            <dt>Werkgebied</dt><dd><a href="{u(root, "locaties")}">Heel Nederland</a></dd>
            <dt>KvK</dt><dd>{kvk}</dd>
          </dl></div>
        </div>
      </div>
      <div id="formulier">
        {contact_form("c", "Vraag via website", extra='<div class="row">' + email_row + '<span></span></div>')}
      </div>
    </div>''')

built.append(page("contact", "Contact", f"Neem contact op met Blauweschild Ongediertebestrijding. Bel {TEL} of mail {MAIL}.", contact_main))


# --- bedankt
def bedankt_main(root):
    return f'''<header class="phero narrow"><div class="wrap"><div>
      <div class="eyebrow">Verstuurd</div>
      <h1>Bedankt voor je <em>bericht</em></h1>
      <p class="lead">We hebben je aanvraag ontvangen en nemen zo snel mogelijk contact met je op.</p>
      <div class="actions"><a class="btn btn-primary" href="{u(root)}">Terug naar de homepage</a><a class="btn btn-ghost" href="{u(root, "diensten")}">Bekijk onze diensten</a></div>
    </div></div></header>''' + section("", cta("Is het dringend?", "Bel ons direct, dan helpen we je meteen verder."))

built.append(page("bedankt", "Bedankt", "Bedankt voor je bericht. We nemen zo snel mogelijk contact met je op.", bedankt_main))

print(f"{len(built)} pagina's gemaakt:")
for b in built:
    print("  " + b)
