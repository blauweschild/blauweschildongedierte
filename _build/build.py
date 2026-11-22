#!/usr/bin/env python3
"""Maakt alle pagina's van de Blauweschild-website.

Gebruik (vanuit de hoofdmap van de repo):
    python3 _build/build.py

Teksten staan in _build/content.py, iconen in _build/icons.py.
Stijl in css/site.css, scripts in js/.
Let op: handmatige wijzigingen in de gegenereerde index.html-bestanden
worden overschreven als je dit script opnieuw draait.
"""
import os, re, sys
from html import escape as E

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from content import *  # noqa
from icons import ICONS

SHIELD = '<svg viewBox="0 0 22 26" aria-hidden="true"><path d="M1 1h20v10c0 7-5 11-10 14C6 22 1 18 1 11z" fill="#3a74ff"/><path d="M6 12.5l3.5 3.5L16 9" stroke="#d6e3ff" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
MARK = '<svg class="mark" viewBox="0 0 22 26" aria-hidden="true"><path d="M1 1h20v10c0 7-5 11-10 14C6 22 1 18 1 11z" fill="#d6e3ff"/></svg>'
PEST = {p["slug"]: p for p in PESTS}
MONTHS = ["jan", "feb", "mrt", "apr", "mei", "jun", "jul", "aug", "sep", "okt", "nov", "dec"]
MONTHS_1 = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]


# ---------------------------------------------------------------- hulpjes
def ic(name, cls="i"):
    assert name in ICONS, f"onbekend icoon: {name}"
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{name}"/></svg>'


def tile(name, cls=""):
    return f'<span class="ico {cls}">{ic(name)}</span>'


def checklist(items, cls="ticks"):
    return f'<ul class="{cls}">' + "".join(f"<li>{ic('circle-check')}<span>{E(x)}</span></li>" for x in items) + "</ul>"


def u(root, path=""):
    """Relatieve link naar een pagina, werkt ook zonder server (file://)."""
    return root + (path + "/" if path else "") + "index.html"


def pu(root, slug):
    return u(root, "ongedierte/" + slug)


def lu(root, slug):
    return u(root, "locaties/" + slug)


def sprite(html):
    used = sorted(set(re.findall(r'#i-([a-z0-9-]+)"', html)))
    syms = "".join(f'<symbol id="i-{n}" viewBox="0 0 24 24">{ICONS[n]}</symbol>' for n in used)
    return f'<svg width="0" height="0" style="position:absolute" aria-hidden="true">{syms}</svg>'


def initials(name):
    parts = [p for p in name.split() if p[0].isupper()]
    return (parts[0][0] + parts[-1][0]) if len(parts) > 1 else parts[0][0]


# ---------------------------------------------------------------- vaste delen
def nav(root, cur, home):
    def ca(key):
        return ' aria-current="page"' if cur == key else ""
    mega = "".join(f'<a class="mi" href="{pu(root, p["slug"])}"{ca("ongedierte/" + p["slug"])}>{tile(p["icon"], "sm")}<span><b>{E(p["name"])}</b><small>{E(p["lat"])}</small></span></a>' for p in PESTS)
    check = "#check" if home else u(root) + "#check"
    provs = "".join(f'<a href="{lu(root, p["slug"])}"{ca("locaties/" + p["slug"])}>{ic("map-pin")}<span>{E(p["name"])}<small>{E(", ".join(p["cities"][:3]))}</small></span></a>' for p in PROVINCES)
    on_p = " on" if cur.startswith("ongedierte") or cur == "diensten" else ""
    on_l = " on" if cur.startswith("locaties") else ""
    inspect = "#contact" if home else u(root, "contact") + "#formulier"
    m_pests = "".join(f'<a class="mtile" href="{pu(root, p["slug"])}"{ca("ongedierte/" + p["slug"])}>{tile(p["icon"], "sm")}<span><b>{E(p["name"])}</b><small>{E(p["lat"])}</small></span></a>' for p in PESTS)
    m_provs = "".join(f'<a href="{lu(root, p["slug"])}"{ca("locaties/" + p["slug"])}>{ic("map-pin")}{E(p["name"])}</a>' for p in PROVINCES)
    company = [("", "house", "Home", "Plaagcheck en overzicht"), ("diensten", "layers", "Diensten", "Alle bestrijding op een rij"),
               ("spoed", "siren", "Spoedhulp", "Vandaag nog geholpen"), ("over-ons", "users", "Over ons", "Wie we zijn en hoe we werken"),
               ("vacatures", "briefcase", "Vacatures", "Kom ons team versterken"), ("contact", "message-circle", "Contact", "Bel, mail of vraag een inspectie aan")]
    m_comp = "".join(f'<li><a href="{u(root, k)}"{ca(k)}>{tile(icn, "sm")}<span><b>{E(t)}</b><small>{E(s)}</small></span>{ic("chevron-right", "i chev")}</a></li>' for k, icn, t, s in company)
    brand = f'<a class="brand" href="{u(root)}">{SHIELD}<span>Blauweschild<small>Ongediertebestrijding</small></span></a>'
    return f'''<a class="skip" href="#main">Naar de inhoud</a>
<nav class="nav" aria-label="Hoofdmenu">
  <div class="wrap">
    {brand}
    <ul class="menu">
      <li class="dd{on_p}"><button type="button" aria-expanded="false" aria-controls="dd-ong">Ongedierte {ic("chevron-down")}</button>
        <div class="dd-panel mega" id="dd-ong" hidden><div class="mega-items">{mega}</div>
          <a class="promo" href="{check}">{tile("scan-search", "sig")}<h3>Niet zeker wat het is?</h3><p>Doe de plaagcheck: tik aan wat je ziet of hoort en je krijgt direct een inschatting.</p><span class="link">Naar de plaagcheck {ic("arrow-right")}</span></a>
          <div class="dd-foot"><span>Acht soorten, één aanpak: eerst begrijpen, dan bestrijden.</span><a class="link" href="{u(root, "diensten")}"{ca("diensten")}>Alle diensten {ic("arrow-right")}</a></div>
        </div></li>
      <li class="dd{on_l}"><button type="button" aria-expanded="false" aria-controls="dd-loc">Locaties {ic("chevron-down")}</button>
        <div class="dd-panel dd-list" id="dd-loc" hidden>{provs}<div class="dd-foot"><span>Werkgebied</span><a class="link" href="{u(root, "locaties")}"{ca("locaties")}>Heel Nederland {ic("arrow-right")}</a></div></div></li>
      <li><a href="{u(root, "spoed")}"{ca("spoed")}>Spoed</a></li>
      <li><a href="{u(root, "over-ons")}"{ca("over-ons")}>Over ons</a></li>
      <li><a href="{u(root, "vacatures")}"{ca("vacatures")}>Vacatures</a></li>
      <li><a href="{u(root, "contact")}"{ca("contact")}>Contact</a></li>
    </ul>
    <div class="nav-cta">
      <button class="btn btn-spoed" type="button" data-spoed aria-haspopup="dialog"><span class="pulse"></span>Spoed</button>
      <a class="btn btn-primary" href="{inspect}">{ic("calendar-check")}Inspectie aanvragen</a>
      <button class="burger" id="burger" type="button" aria-expanded="false" aria-controls="mnav" aria-label="Menu openen">{ic("menu")}</button>
    </div>
  </div>
</nav>
<div class="mnav" id="mnav" hidden role="dialog" aria-modal="true" aria-label="Menu">
  <div class="mnav-in">
    <div class="mnav-top">{brand}<button type="button" data-close aria-label="Menu sluiten">{ic("x")}</button></div>
    <div class="mquick">
      <a class="q-call" href="{TEL_HREF}">{ic("phone")}Bel direct</a>
      <button class="q-spoed" type="button" data-spoed>{ic("siren")}Spoed</button>
      <a class="q-insp" href="{inspect}">{ic("calendar-check")}Inspectie</a>
    </div>
    <div class="msec"><h2>Ongedierte <a href="{u(root, "diensten")}">Alle diensten {ic("arrow-right")}</a></h2><div class="mtiles">{m_pests}</div></div>
    <div class="msec"><h2>Locaties <a href="{u(root, "locaties")}">Overzicht {ic("arrow-right")}</a></h2><div class="mchips">{m_provs}</div></div>
    <div class="msec"><h2>Blauweschild</h2><ul class="mlist">{m_comp}</ul></div>
    <div class="mcontact">
      <a href="{TEL_HREF}">{ic("phone")}<b>{E(TEL)}</b></a>
      <a href="mailto:{MAIL}">{ic("mail")}{E(MAIL)}</a>
      <span>{ic("clock")}7 dagen per week, 08:00–17:00</span>
    </div>
  </div>
</div>'''


def sheet(root):
    return f'''<button class="btn btn-spoed fab" type="button" data-spoed aria-haspopup="dialog"><span class="pulse"></span>Spoed? Bel ons</button>

<div class="sheet-bg" id="spoed" hidden>
  <div class="sheet" role="dialog" aria-modal="true" aria-labelledby="spoed-h">
    <button class="x" type="button" id="spoed-x" aria-label="Sluiten">{ic("x")}</button>
    <div class="eyebrow">Spoedhulp</div>
    <h2 id="spoed-h">Direct hulp bij ongedierte</h2>
    <ul>
      <li>{ic("triangle-alert")}Muizen of ratten die met de kou naar binnen trekken</li>
      <li>{ic("triangle-alert")}Een wespennest bij de deur, dakrand of speelplek</li>
      <li>{ic("triangle-alert")}Bedwantsen of kakkerlakken</li>
    </ul>
    <div class="bignum"><strong id="spoed-nr">{E(TEL)}</strong><button class="copy" type="button" id="spoed-copy">Kopieer nummer</button></div>
    <a class="btn btn-spoed" href="{TEL_HREF}" style="font-size:1.05rem;padding:15px">{ic("phone-call")}Bel nu met spoed</a>
    <form data-form="Spoed" data-subject="Terugbelverzoek" novalidate>
      <p class="small">Of laat je nummer achter, dan bellen we je zo snel mogelijk terug. <a href="{u(root, "spoed")}">Meer over spoedhulp</a></p>
      {honeypot()}
      <div class="row">{field("s-naam", "naam", "Naam", ac="name")}{field("s-tel", "telefoon", "Telefoonnummer", "tel", True, "tel", "06 12345678")}</div>
      <button class="btn btn-ghost" type="submit">{ic("phone-incoming")}Bel mij terug</button>
      <div class="sent" role="status" hidden></div>
    </form>
  </div>
</div>'''


def footer(root):
    pests = "".join(f'<li><a href="{pu(root, p["slug"])}">{E(p["name"])}</a></li>' for p in PESTS)
    return f'''<footer>
  <div class="wrap cols">
    <div>
      <a class="brand" href="{u(root)}">{SHIELD}<span>Blauweschild<small>Ongediertebestrijding</small></span></a>
      <p>Ongediertebestrijding voor particulier en zakelijk, door heel Nederland. We zoeken uit waar het vandaan komt, lossen het op en sluiten de toegang af.</p>
      <ul class="ticks" style="font-size:.9rem;color:var(--text)"><li>{ic("badge-check")}Gecertificeerde specialisten</li><li>{ic("timer")}Spoedservice, 7 dagen per week</li><li>{ic("shield-check")}Preventie volgens IPM</li></ul>
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
      <div class="fcontact">
        <a href="{TEL_HREF}">{tile("phone", "sm")}<span><small>Bel ons</small><b>{E(TEL)}</b></span></a>
        <a href="mailto:{MAIL}">{tile("mail", "sm")}<span><small>E-mail</small>{E(MAIL)}</span></a>
        <div>{tile("clock", "sm")}<span><small>Bereikbaar</small>7 dagen per week, 08:00–17:00</span></div>
        <div>{tile("map-pin", "sm")}<span><small>Werkgebied</small>Heel Nederland</span></div>
      </div>
    </div>
  </div>
  <div class="wrap bottom">
    <span>© 2026 Blauweschild Ongediertebestrijding</span>
    <span>Gecertificeerd · Discreet · Garantie op resultaat</span>
  </div>
</footer>'''


def page(path, title, desc, main, home=False, scripts=""):
    depth = 0 if path == "" else path.count("/") + 1
    root = "../" * depth
    full_title = title if home else f"{title} – Blauweschild Ongediertebestrijding"
    main_html = main(root)
    body = f'''{nav(root, path, home)}
<main id="main">
{main_html}
</main>
{sheet(root)}
{footer(root)}'''
    html = f'''<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(full_title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="theme-color" content="#071029">
<link rel="icon" href="data:image/svg+xml,{E('<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 22 26%22><path d=%22M1 1h20v10c0 7-5 11-10 14C6 22 1 18 1 11z%22 fill=%22%233a74ff%22/></svg>')}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Instrument+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="{root}css/site.css">
</head><body data-root="{root}">
{sprite(body)}
{body}
<script src="{root}js/site.js"></script>{scripts}
</body></html>
'''
    d = os.path.join(OUT, path)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    text = re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style|svg)[\s\S]*?</\1>", " ", main_html))
    return (path or "/", len(re.findall(r"\w+", text)))


# ---------------------------------------------------------------- bouwstenen
def crumbs(root, items):
    li = [f'<li><a href="{u(root)}">{ic("house")}<span class="sr">Home</span></a></li>']
    for label, path in items:
        li.append(f'<li><a href="{u(root, path)}">{E(label)}</a></li>' if path is not None else f'<li aria-current="page">{E(label)}</li>')
    return f'<ol class="crumbs" aria-label="Kruimelpad">{"".join(li)}</ol>'


def head(eyebrow, h2, p=None, cls="", side=""):
    inner = f'<div class="eyebrow">{E(eyebrow)}</div><h2>{h2}</h2>{f"<p>{p}</p>" if p else ""}'
    if side:
        return f'<div class="head row {cls}"><div class="head">{inner}</div>{side}</div>'
    return f'<div class="head {cls}">{inner}</div>'


def section(inner, cls="", sid=""):
    idattr = f' id="{sid}"' if sid else ""
    return f'<section class="block {cls}"{idattr}><div class="wrap">{inner}</div></section>'


def call_btns(root):
    return f'<div class="actions"><a class="btn btn-spoed" href="{TEL_HREF}">{ic("phone")}Bel {E(TEL)}</a><a class="btn btn-primary" href="{u(root, "contact")}#formulier">{ic("calendar-check")}Plan een inspectie</a></div>'


def trustbar():
    items = "".join(f'<div>{tile(i, "sm")}<span><b>{E(t)}</b><span>{E(s)}</span></span></div>' for i, t, s in TRUST)
    return f'<div class="trustbar"><div class="wrap"><div class="trust">{items}</div></div></div>'


def pest_grid(root, text=None):
    out = []
    for i, p in enumerate(PESTS):
        txt = E(text(i, p)) if text else E(p["kort"])
        tag = f'<span class="tagline hot">{ic("siren")}Spoed</span>' if p["spoed"] else ""
        out.append(f'<a class="card pcard" href="{pu(root, p["slug"])}"><div class="card-top">{tile(p["icon"])}{tag}</div><h3>{E(p["name"])}</h3><span class="lat">{E(p["lat"])}</span><p>{txt}</p><span class="link">Meer over {E(p["name"].lower())} {ic("arrow-right")}</span></a>')
    return f'<div class="pgrid">{"".join(out)}</div>'


def feat_cards(items, cls="cards", tcls="", hz=False):
    if hz:
        return f'<div class="{cls}">' + "".join(f'<div class="card hz">{tile(i, tcls)}<div><h3>{E(t)}</h3><p>{E(x)}</p></div></div>' for i, t, x in items) + "</div>"
    return f'<div class="{cls}">' + "".join(f'<div class="card">{tile(i, tcls)}<h3>{E(t)}</h3><p>{E(x)}</p></div>' for i, t, x in items) + "</div>"


def steps(items=None, cls="steps"):
    items = items or STEPS
    return f'<ol class="{cls}">' + "".join(f"<li>{tile(i)}<h3>{E(a)}</h3><p>{E(b)}</p></li>" for i, a, b in items) + "</ol>"


def ipm():
    return f'<div class="ipm">{tile("leaf", "lg")}<div><strong>Integrated Pest Management</strong><p style="margin-top:6px">We werken volgens IPM: eerst voorkomen en weren, dan pas bestrijden. Middelen zetten we alleen in waar het nodig is. Dat is beter voor je gezondheid, je huisdieren en het milieu, en het resultaat houdt langer stand.</p></div></div>'


def why(items=WHY):
    return feat_cards(items, "cards four")


def stats(items=STATS, cls=""):
    return f'<div class="stats {cls}">' + "".join(f"<div><strong>{E(a)}</strong><span>{E(b)}</span></div>" for a, b in items) + "</div>"


def stars():
    return '<div class="stars" role="img" aria-label="5 van 5 sterren">' + ic("star") * 5 + "</div>"


def reviews(only=None):
    rs = [r for r in REVIEWS if not only or r[3] in only]
    if not rs:
        return ""
    if only and len(rs) < 3:  # vul aan tot een volle rij, de passende review eerst
        rs += [r for r in REVIEWS if r not in rs][:3 - len(rs)]
    cards = "".join(
        f'<figure class="review">{stars()}<blockquote>{E(q)}</blockquote>'
        f'<figcaption><span class="avatar" aria-hidden="true">{E(initials(n))}</span><span><b>{E(n)}</b><small>{E(PEST[s]["name"])} · {E(c)}</small></span></figcaption></figure>'
        for q, n, c, s in rs)
    if not only and len(rs) % 3:
        cards += f'<div class="review" style="background:radial-gradient(90% 90% at 100% 0%,color-mix(in srgb,var(--signal) 14%,transparent),transparent 70%),var(--panel);border-color:color-mix(in srgb,var(--signal) 45%,var(--line))">{tile("thumbs-up", "sig")}<div style="display:grid;gap:8px"><h3 style="font-size:1.4rem">Ook zo geholpen worden?</h3><p style="color:var(--muted)">Gemiddeld een 4,9 uit 5 op Google. Plan een inspectie of bel ons direct.</p></div><a class="link" href="{TEL_HREF}">Bel {E(TEL)} {ic("arrow-right")}</a></div>'
    return f'<div class="reviews">{cards}</div>'


def score():
    return f'<span class="score">{stars()}<b>4,9</b> / 5 op Google</span>'


def faq(items, cols=False):
    return f'<div class="faq{" cols" if cols else ""}">' + "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in items) + "</div>"


def cta(root, h, p):
    return f'''<div class="cta">{MARK}<div><h2>{h}</h2><p>{p}</p></div>
      <div class="actions"><a class="btn btn-spoed" href="{TEL_HREF}">{ic("phone")}Bel {E(TEL)}</a><button class="btn btn-ghost" type="button" data-spoed>{ic("phone-incoming")}Terugbelverzoek</button></div></div>'''


def season_table(root):
    rows = []
    for p in PESTS:
        cells = "".join(f'<td class="l{v}" title="{MONTHS[k]}: {["weinig", "actief", "piek"][v]}"></td>' for k, v in enumerate(SEASONS[p["slug"]]))
        rows.append(f'<tr><th scope="row"><a href="{pu(root, p["slug"])}">{tile(p["icon"])}{E(p["name"])}</a></th>{cells}</tr>')
    headr = "".join(f'<th scope="col">{m}</th>' for m in MONTHS)
    return f'''<div class="season"><table><caption class="sr">Activiteit van ongedierte per maand</caption><thead><tr><th><span class="sr">Plaagdier</span></th>{headr}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>
    <div class="legend"><span><i></i>Weinig activiteit</span><span><i class="l1"></i>Actief</span><span><i class="l2"></i>Piekseizoen</span><span>Indicatie: het weer en je woning maken veel uit.</span></div>'''


def audience():
    out = []
    for icn, t, sub, txt, items in (PARTICULIER, ZAKELIJK):
        out.append(f'<div class="card">{tile(icn, "lg")}<span class="sub">{E(sub)}</span><h3>{E(t)}</h3><p>{E(txt)}</p>{checklist(items)}</div>')
    return f'<div class="aud">{"".join(out)}</div>'


def field(fid, name, label, typ="text", req=False, ac="", ph="", cls=""):
    star = ' <span class="req">*</span>' if req else ""
    attrs = (" required" if req else "") + (f' autocomplete="{ac}"' if ac else "") + (f' placeholder="{E(ph)}"' if ph else "")
    if typ == "tel":
        attrs += ' inputmode="tel"'
    return f'<label class="field {cls}" for="{fid}"><span class="lbl">{E(label)}{star}</span><input id="{fid}" name="{name}" type="{typ}"{attrs}></label>'


def select(fid, name, label, options, cls=""):
    opts = "".join(f"<option>{E(o)}</option>" for o in options)
    return f'<label class="field {cls}" for="{fid}"><span class="lbl">{E(label)}</span><select id="{fid}" name="{name}">{opts}</select></label>'


def textarea(fid, name, label, ph, req=False, maxlen=1000):
    star = ' <span class="req">*</span>' if req else ""
    return f'<label class="field" for="{fid}"><span class="lbl">{E(label)}{star}<span class="counter" aria-hidden="true"></span></span><textarea id="{fid}" name="{name}" maxlength="{maxlen}"{" required" if req else ""} placeholder="{E(ph)}"></textarea></label>'


def seg(name, legend, options, default=None):
    out = []
    for opt in options:
        val, icn = (opt if isinstance(opt, tuple) else (opt, None))
        chk = " checked" if val == default else ""
        out.append(f'<label><input type="radio" name="{name}" value="{E(val)}"{chk}><span>{ic(icn) if icn else ""}{E(val)}</span></label>')
    return f'<fieldset class="group"><legend class="lbl">{E(legend)}</legend><div class="seg">{"".join(out)}</div></fieldset>'


def chipsel(name, legend, options):
    out = "".join(f'<label><input type="checkbox" name="{name}" value="{E(o)}"><span>{ic("check")}{E(o)}</span></label>' for o in options)
    return f'<fieldset class="group"><legend class="lbl">{E(legend)} <small>meerdere mogelijk</small></legend><div class="seg chk">{out}</div></fieldset>'


def consent(fid, text="Ik ga akkoord dat Blauweschild mijn gegevens gebruikt om contact met me op te nemen over deze aanvraag."):
    return f'<label class="field consent" for="{fid}"><input type="checkbox" id="{fid}" name="akkoord" value="Ja" required><span class="box">{ic("check")}</span><span>{E(text)} <span class="req">*</span></span></label>'


def honeypot():
    return '<div class="hp" aria-hidden="true"><label>Laat leeg<input name="_gotcha" tabindex="-1" autocomplete="off"></label></div>'


def form_foot(extra=""):
    return f'<div class="form-foot"><span>{ic("lock")}Je gegevens gebruiken we alleen voor je aanvraag</span><span>{ic("timer")}Reactie binnen één werkdag</span>{extra}</div>'


def contact_form(fid, subject, redirect=True):
    """Compacte versie, voor de homepage."""
    soorten = [p["name"] for p in PESTS] + ["Anders of weet ik niet"]
    return f'''<form class="xform" data-form="Inspectie" data-subject="{E(subject)}"{' data-redirect' if redirect else ''} novalidate>
        <div class="xform-head">{tile("calendar-check")}<div><h3>Inspectie aanvragen</h3><p>We bellen je terug om een afspraak te plannen.</p></div></div>
        {honeypot()}
        <div class="row">{field(fid + "-naam", "naam", "Naam", req=True, ac="name")}{field(fid + "-tel", "telefoon", "Telefoonnummer", "tel", True, "tel", "06 12345678")}</div>
        <div class="row">{field(fid + "-pc", "postcode", "Postcode", ac="postal-code", ph="1234 AB")}{select(fid + "-soort", "plaagdier", "Wat speelt er?", soorten)}</div>
        {textarea(fid + "-msg", "toelichting", "Toelichting", "Waar zie je het, sinds wanneer, hoeveel?", maxlen=600)}
        {consent(fid + "-ok")}
        <button class="btn btn-primary btn-lg" type="submit">{ic("send")}Verstuur aanvraag</button>
        {form_foot()}
        <div class="sent" role="status" hidden></div>
      </form>'''


def detailed_form(fid):
    """Uitgebreide versie, voor de contactpagina."""
    choices = "".join(f'<label class="choice"><input type="radio" name="plaagdier" value="{E(p["name"])}"><span class="choice-box">{tile(p["icon"], "sm")}<b>{E(p["name"])}</b></span></label>' for p in PESTS)
    choices += f'<label class="choice"><input type="radio" name="plaagdier" value="Weet ik niet"><span class="choice-box">{tile("circle-help", "sm")}<b>Weet ik niet</b></span></label>'
    return f'''<form class="xform big" data-form="Inspectie" data-subject="Inspectie-aanvraag" data-redirect novalidate>
        <div class="xform-head">{tile("calendar-check", "lg")}<div><h2>Inspectie aanvragen</h2><p>Duurt ongeveer twee minuten. Velden met <span class="req">*</span> zijn verplicht, de rest helpt ons om je sneller en beter te helpen.</p></div></div>
        {honeypot()}
        <fieldset class="fs">
          <legend><span class="num">1</span>Wat speelt er?</legend>
          <div class="choice-grid" role="radiogroup" aria-label="Plaagdier">{choices}</div>
          <div class="row">{select(fid + "-sinds", "sinds_wanneer", "Sinds wanneer merk je het?", ["Vandaag", "Een paar dagen", "Een paar weken", "Langer dan een maand", "Weet ik niet"])}{select(fid + "-vaak", "hoe_vaak", "Hoe vaak zie of hoor je het?", ["Eén keer", "Af en toe", "Dagelijks", "Weet ik niet"])}</div>
          {seg("urgentie", "Hoe dringend is het?", [("Spoed, zo snel mogelijk", "siren"), ("Deze week", "calendar-days"), ("Geen haast", "clock")], "Deze week")}
        </fieldset>
        <fieldset class="fs">
          <legend><span class="num">2</span>Waar is het?</legend>
          {seg("type_pand", "Soort pand", [("Woning", "house"), ("Bedrijf", "building-2"), ("VvE of verhuur", "users")], "Woning")}
          {chipsel("plek", "Waar zie je het?", ["Keuken", "Woonkamer", "Slaapkamer", "Badkamer", "Zolder", "Kruipruimte of kelder", "Tuin of schuur", "Dak of gevel"])}
          <div class="row">{field(fid + "-pc", "postcode", "Postcode", ac="postal-code", ph="1234 AB")}{field(fid + "-plaats", "plaats", "Plaats", ac="address-level2", ph="Bijv. Utrecht")}</div>
          {field(fid + "-bedrijf", "bedrijfsnaam", "Bedrijfsnaam (alleen bij zakelijk)", ac="organization")}
        </fieldset>
        <fieldset class="fs">
          <legend><span class="num">3</span>Je gegevens</legend>
          <div class="row">{field(fid + "-naam", "naam", "Naam", req=True, ac="name")}{field(fid + "-tel", "telefoon", "Telefoonnummer", "tel", True, "tel", "06 12345678")}</div>
          {field(fid + "-mail", "email", "E-mail", "email", ac="email", ph="naam@voorbeeld.nl")}
          {seg("beste_moment", "Wanneer kunnen we je het best bellen?", [("Ochtend", "sun"), ("Middag", "clock"), ("Maakt niet uit", "check")], "Maakt niet uit")}
          {textarea(fid + "-msg", "toelichting", "Toelichting", "Beschrijf kort wat je ziet of hoort. Bijvoorbeeld: keutels in het keukenkastje, geritsel op zolder 's nachts.")}
          {consent(fid + "-ok")}
        </fieldset>
        <button class="btn btn-primary btn-lg" type="submit">{ic("send")}Verstuur aanvraag</button>
        {form_foot(f'<span>{ic("phone")}Spoed? Bel <a href="{TEL_HREF}">{E(TEL)}</a></span>')}
        <div class="sent" role="status" hidden></div>
      </form>'''


def contact_dl():
    return f'''<dl class="dl">
        <dt>Telefoon</dt><dd><a href="{TEL_HREF}" style="font-variant-numeric:tabular-nums">{E(TEL)}</a></dd>
        <dt>E-mail</dt><dd><a href="mailto:{MAIL}">{E(MAIL)}</a></dd>
        <dt>Open</dt><dd>7 dagen per week, 08:00–17:00</dd>
      </dl>'''


def phero(root, crumb_items, eyebrow, h1, lead, side="", facts=None, buttons=None):
    f = ""
    if facts:
        f = '<ul class="facts">' + "".join(f"<li>{ic('circle-check')}{E(x)}</li>" for x in facts) + "</ul>"
    cls = "phero" if side else "phero narrow"
    return f'''<header class="{cls}">
  <div class="wrap">
    <div>
      {crumbs(root, crumb_items)}
      <div class="eyebrow">{E(eyebrow)}</div>
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
      {buttons if buttons is not None else call_btns(root)}
      {f}
    </div>
    {side}
  </div>
</header>'''


def side_card(tag, title, sub, icon, big, dl_rows, extra=""):
    dl = "".join(f"<dt>{E(k)}</dt><dd>{v}</dd>" for k, v in dl_rows)
    return f'''<aside class="spec" aria-label="{E(tag)}: {E(title)}">
      <div class="spec-top">{tile(icon, "xl")}<div><span class="tag">{E(tag)}</span><h2>{E(title)}</h2><span class="lat">{E(sub)}</span></div></div>
      <div class="big">{E(big[0])}<small>{E(big[1])}</small></div>
      {extra}
      <dl>{dl}</dl>
    </aside>'''


def mini_season(slug):
    cells = "".join(f'<i class="l{v}" title="{MONTHS[k]}"></i>' for k, v in enumerate(SEASONS[slug]))
    lab = "".join(f"<span>{m}</span>" for m in MONTHS_1)
    return f'<div><span class="tag" style="display:block;margin-bottom:8px">Seizoen · <span style="color:var(--signal)">■</span> piek</span><div class="mini-season" aria-hidden="true">{cells}</div><div class="mini-season-l" aria-hidden="true">{lab}</div></div>'


def pest_tiles(root, exclude=None):
    return '<div class="ptiles">' + "".join(f'<a class="ptile" href="{pu(root, o["slug"])}">{tile(o["icon"], "sm")}<span><b>{E(o["name"])}</b><small>{E(o["lat"])}</small></span></a>' for o in PESTS if o is not exclude) + "</div>"


# ---------------------------------------------------------------- pagina's
built = []

# --- homepage
def home_main(root):
    provcards = "".join(f'<a class="card" href="{lu(root, p["slug"])}"><div class="card-top">{tile("map-pin")}{ic("arrow-up-right")}</div><h3>{E(p["name"])}</h3><p>{E(", ".join(p["cities"]))} en omgeving.</p></a>' for p in PROVINCES)
    provcards += f'<a class="card warn" href="{u(root, "locaties")}"><div class="card-top">{tile("map", "sig")}{ic("arrow-up-right")}</div><h3>Heel Nederland</h3><p>Woon je ergens anders? Bel ons om de mogelijkheden te bespreken.</p></a>'
    return f'''<header class="hero" id="top">
  <div class="wrap">
    <div>
      <div class="eyebrow">Ongediertebestrijding · heel Nederland</div>
      <h1>Wij houden <em>ongedierte</em> buiten de deur.</h1>
      <p class="lead">Als het kouder wordt, trekken muizen en ratten naar binnen, op zoek naar warmte en eten. Ook bedwantsen na een vakantie of kakkerlakken in de keuken pakken we aan. Blauweschild zoekt uit waar het vandaan komt, lost het op en sluit de toegang af zodat het niet terugkomt.</p>
      <div class="actions">
        <a class="btn btn-primary" href="#contact">{ic("calendar-check")}Plan een inspectie</a>
        <button class="btn btn-spoed" type="button" data-spoed><span class="pulse"></span>Spoedhulp</button>
        <a class="btn btn-ghost" href="#check">{ic("scan-search")}Wat zit er in huis?</a>
      </div>
      <ul class="facts">
        <li>{ic("circle-check")}Binnen 24 uur ter plaatse</li>
        <li>{ic("circle-check")}Garantie op resultaat</li>
        <li>{ic("circle-check")}Preventie volgens IPM</li>
      </ul>
    </div>
    <div class="stage" data-stage>
      <div class="fallback" aria-hidden="true">{SHIELD}</div>
    </div>
  </div>
</header>
{trustbar()}

<section class="block solid" id="check">
  <div class="wrap">
    {head("Plaagcheck", "Wat zie of hoor je in huis?", "Tik aan wat je herkent. Je ziet meteen welk plaagdier het meest waarschijnlijk is, hoe snel je moet handelen en wat je nu alvast kunt doen.")}
    <div class="check">
      <div class="signs" id="signs" role="group" aria-label="Signalen"></div>
      <div class="result" aria-live="polite">
        <span class="tag" id="r-tag">Meest waarschijnlijk</span>
        <h3 id="r-name">Muizen</h3>
        <span class="urg" id="r-urg">Binnen een week</span>
        <p id="r-advice"></p>
        <div class="meter" id="r-meter"></div>
        <a class="more" id="r-more" href="{pu(root, "muizen")}">Alles over muizen →</a>
        <span class="note" id="r-note">Voorbeeld: twee signalen staan al aan. Pas ze aan naar jouw situatie.</span>
      </div>
    </div>
  </div>
</section>

<section class="block" id="diensten">
  <div class="wrap">
    {head("Diensten", "Van knaagdier tot kruipend insect", "Elke soort vraagt een andere aanpak. We kijken eerst naar gedrag en toegangswegen, en pas daarna naar middelen. Zo los je het probleem op bij de bron, in plaats van alleen de dieren die je ziet.", side=f'<a class="btn btn-ghost" href="{u(root, "diensten")}">Alle diensten {ic("arrow-right")}</a>')}
    {pest_grid(root)}
  </div>
</section>

<section class="block alt">
  <div class="wrap">
    {head("Voor wie", "Thuis of op de zaak", "Of het nu gaat om muizen op zolder of kakkerlakken in een bedrijfskeuken: we passen onze aanpak aan op de plek en de mensen die er wonen of werken.")}
    {audience()}
  </div>
</section>

<section class="block" id="werkwijze">
  <div class="wrap">
    {head("Werkwijze", "Zo pakken we het aan", "Vier stappen, van eerste telefoontje tot blijvend resultaat. Je weet bij elke stap waar je aan toe bent.")}
    {steps()}
    {ipm()}
  </div>
</section>

<section class="block alt">
  <div class="wrap">
    {head("Seizoenskalender", "Wanneer zie je wat?", "Elk plaagdier heeft zijn eigen seizoen. Muizen en ratten trekken in het najaar naar binnen, wespen pieken eind van de zomer en bedwantsen nemen toe na de vakantieperiode. Wie het seizoen kent, kan op tijd voorkomen.")}
    {season_table(root)}
  </div>
</section>

<section class="block">
  <div class="wrap">
    {head("Waarom Blauweschild", "Snel ter plaatse, blijvend resultaat", "We combineren snelheid, vakmanschap en eerlijk advies. Geen standaard spuitbeurt, maar een aanpak die past bij jouw situatie.")}
    {why()}
    {stats()}
  </div>
</section>

<section class="block alt">
  <div class="wrap">
    {head("Reviews", "Wat klanten zeggen", None, side=score())}
    {reviews()}
  </div>
</section>

<section class="block">
  <div class="wrap">
    {head("Werkgebied", "Door heel Nederland", "We zijn actief in zeven provincies, van de grachten van Amsterdam tot de akkers van Flevoland. Kies je regio voor meer informatie.", side=f'<a class="btn btn-ghost" href="{u(root, "locaties")}">Alle locaties {ic("arrow-right")}</a>')}
    <div class="cards four">{provcards}</div>
  </div>
</section>

<section class="block alt">
  <div class="wrap">
    {head("Veelgestelde vragen", "Goed om te weten", "Staat je vraag er niet bij? Bel of mail ons, we helpen je graag.")}
    {faq(FAQ, cols=True)}
  </div>
</section>

<section class="block contact" id="contact" style="background:color-mix(in srgb,var(--ink) 55%,transparent)">
  <div class="wrap">
    <div class="contact-side">
      {head("Contact", "Last van ongedierte? Vraag een inspectie aan.", "Laat je gegevens achter, dan bellen we je terug om een afspraak te plannen. Liever direct contact? Bel of mail ons.")}
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
    side = side_card("Overzicht", "Acht specialismen", "Knaagdieren en insecten", "layers", ("8", "soorten ongedierte, elk met een eigen aanpak"),
                     [("Reactie", "Binnen 24 uur"), ("Spoed", '<span class="urg hot">Dezelfde dag</span>'), ("Voor", "Particulier en zakelijk")])
    return phero(root, [("Diensten", None)], "Diensten", "Bestrijding met <em>een plan</em>",
        "Professionele bestrijding van alle soorten ongedierte, voor particulieren en bedrijven. We beginnen altijd met een inspectie, zodat we de oorzaak aanpakken en niet alleen de gevolgen.", side,
        facts=["Binnen 24 uur hulp", "Garantie op resultaat", "Veilig voor kinderen en huisdieren"]) + trustbar() + \
    section(head("Welk ongedierte?", "Kies het plaagdier", "Klik op een soort voor uitleg over herkennen, risico's, onze aanpak, preventietips en veelgestelde vragen.") + pest_grid(root)) + \
    section(head("Methoden", "Wat we inzetten", "Geen standaard spuitbeurt, maar de juiste methode voor de situatie. Vaak combineren we meerdere methoden voor een blijvend resultaat.") + feat_cards(METHODS), "alt") + \
    section(head("Voor wie", "Particulier en zakelijk", "Thuis wil je vooral snel en discreet geholpen worden. Een bedrijf heeft daarnaast te maken met hygiëne-eisen, openingstijden en rapportage. We stemmen onze aanpak daarop af.") + audience()) + \
    section(head("Werkwijze", "Zo pakken we het aan", "Van eerste contact tot controlebezoek: je weet bij elke stap wat er gebeurt en wat het kost.") + steps() + ipm(), "alt") + \
    section(head("Seizoenskalender", "Wanneer zie je wat?", "Met deze kalender zie je wanneer welk plaagdier het meest actief is. Zo weet je wanneer je extra alert moet zijn.") + season_table(root)) + \
    section(head("Veelgestelde vragen", "Goed om te weten") + faq(FAQ, cols=True), "alt") + \
    section(cta(root, "Direct hulp nodig?", "Onze specialisten staan 7 dagen per week voor je klaar. Bel voor snelle, professionele hulp of laat je terugbellen."))

built.append(page("diensten", "Diensten", "Alle diensten van Blauweschild: bestrijding van muizen, ratten, wespen, bedwantsen, vlooien, mieren, kakkerlakken en zilvervisjes, voor particulier en zakelijk.", diensten_main))


# --- ongedierte
PSTEP_ICONS = ["scan-search", "clipboard-list", "target", "shield-check"]

for p in PESTS:
    def pest_main(root, p=p):
        name_l = p["name"].lower()
        urg_cls = "urg hot" if p["spoed"] else "urg"
        side = side_card("Soortkaart", p["name"], p["lat"], p["icon"], p["big"],
                         [("Urgentie", f'<span class="{urg_cls}">{E(p["urg"])}</span>'), ("Spoed", "Mogelijk, dezelfde dag" if p["spoed"] else "Binnen 24 uur ter plaatse")],
                         extra=mini_season(p["slug"]))
        risk_li = "".join(f"<li>{ic('triangle-alert')}<span>{E(t)}</span></li>" for t in p["gevaren"])
        sign_cls = "cards" if len(p["signs"]) % 3 == 0 else "cards two"
        rv = reviews([p["slug"]])
        alt = ["", "alt"]
        k = 0
        def nxt():
            nonlocal k
            k += 1
            return alt[k % 2]
        out = phero(root, [("Diensten", "diensten"), (p["name"], None)], p["title"], f"Last van <em>{E(name_l)}</em>?", E(p["lead"]), side,
                    facts=["Binnen 24 uur hulp", "Garantie op resultaat", "Veilig en effectief"]) + trustbar()
        out += section(head("Het probleem", f"Wat je moet weten over {E(name_l)}") + f'''<div class="split">
      <div class="prose"><p>{E(p["intro"])}</p><p>{E(p["intro2"])}</p></div>
      <div style="display:grid;gap:18px"><div class="card warn">{tile("timer", "sig")}<h3>Waarom snel handelen?</h3><p>{E(p["snel"])}</p></div>
      <div class="card"><h3>Risico's van {E(name_l)}</h3><ul class="risks">{risk_li}</ul></div></div>
    </div>''' + stats(p["facts"], "three sig"))
        out += section(head("Herkennen", f"Zo herken je {E(name_l)}", "Twijfel je? Let op deze signalen. Zie je er meerdere tegelijk, laat het dan bekijken.") + feat_cards(p["signs"], sign_cls), nxt())
        out += section(head("Onze aanpak", f"Zo bestrijden we {E(name_l)}") + f'''<div class="split">
      <div class="prose"><p>{E(p["aanpak"])}</p><p>Je krijgt vooraf een duidelijk voorstel met aanpak en prijs. Na de behandeling hoor je wat je zelf kunt doen om herhaling te voorkomen, en we komen terug voor controle.</p></div>
      <div class="card"><h3>Dit krijg je van ons</h3>{checklist(p["ticks"])}</div>
    </div>''' + steps([(PSTEP_ICONS[j], a, b) for j, (a, b) in enumerate(p["steps"])]), nxt())
        out += section(head("Zelf voorkomen", f"Tips tegen {E(name_l)}", "Met deze maatregelen verklein je de kans op een (nieuwe) plaag flink.") + f'''<div class="split">
      {checklist(p["tips"], "tips")}
      <div class="card">{tile(ZAKELIJK[0], "lg")}<span class="sub">Zakelijk</span><h3>{E(p["name"])} in je bedrijf</h3><p>{E(p["zakelijk"])}</p><a class="link" href="{u(root, "contact")}#formulier">Vraag een bedrijfsinspectie aan {ic("arrow-right")}</a></div>
    </div>''', nxt())
        if rv:
            out += section(head("Ervaring", "Wat klanten zeggen", None, side=score()) + rv, nxt())
        out += section(head("Veelgestelde vragen", f"Vragen over {E(name_l)}", "De vragen die we het vaakst krijgen. Staat die van jou er niet bij? Bel ons gerust.") + faq(p["faq"], cols=True), nxt())
        out += section(cta(root, f"Hulp nodig bij {E(name_l)}?", "Onze specialisten staan klaar. Bel voor directe hulp of laat je terugbellen, dan plannen we een inspectie.") +
                       head("Ander ongedierte", "Bekijk ook") + pest_tiles(root, p), nxt())
        return out

    built.append(page("ongedierte/" + p["slug"], p["title"],
        f"{p['name']} in huis of bedrijf? {p['lead']} Bel {TEL}.", pest_main))


# --- locaties
LOC_HOW = [
    ("timer", "Binnen 24 uur", "In alle provincies in ons werkgebied zijn we bij een gewone melding binnen 24 uur bij je. Bij spoed proberen we dezelfde dag te komen."),
    ("route", "Kennis van de regio", "Een grachtenpand in Amsterdam vraagt een andere aanpak dan een boerderij in Brabant of een nieuwbouwwoning in Almere. Die verschillen kennen we."),
    ("building-2", "Particulier en zakelijk", "We helpen huiseigenaren en huurders, maar ook horeca, winkels, kantoren, VvE's, verhuurders en agrarische bedrijven."),
]
LOC_FAQ = [
    ("Komen jullie ook in mijn plaats?", "Waarschijnlijk wel. We noemen per provincie de grotere steden, maar we komen in de hele provincie, ook in kleinere plaatsen en het buitengebied. Twijfel je? Bel ons even."),
    ("Werken jullie ook buiten deze provincies?", "Ons werkgebied is heel Nederland. Woon je buiten de genoemde provincies, bel ons dan om de mogelijkheden te bespreken."),
    ("Hoe snel zijn jullie er?", "Bij een gewone melding binnen 24 uur. Bij spoed, zoals ratten in huis of een wespennest bij de voordeur, proberen we dezelfde dag te komen."),
    ("Kunnen jullie ook regelmatig controleren bij mijn bedrijf?", "Ja. Voor bedrijven werken we met preventieve controles op vaste momenten, met een rapport van de bevindingen."),
]


def city_chips(cities, small=False):
    st = ' style="padding:5px 11px;font-size:.8rem"' if small else ""
    return '<ul class="chips" style="gap:6px">' + "".join(f"<li{st}>{E(c)}</li>" for c in cities) + "</ul>"


def locaties_main(root):
    cards = "".join(f'<a class="card" href="{lu(root, p["slug"])}"><div class="card-top">{tile("map-pin")}<span class="tagline">{len(p["cities"])} steden</span></div><h3>{E(p["name"])}</h3><p>{E(p["intro"].split(". ")[0])}.</p>{city_chips(p["cities"], True)}<span class="link">Bekijk {E(p["name"])} {ic("arrow-right")}</span></a>' for p in PROVINCES)
    side = side_card("Werkgebied", "7 provincies", "Heel Nederland", "map", ("24 uur", "en we zijn bij je ter plaatse"),
                     [("Spoed", '<span class="urg hot">Dezelfde dag</span>'), ("Bereikbaar", "7 dagen per week, 08:00–17:00")])
    return phero(root, [("Locaties", None)], "Werkgebied", "Door heel <em>Nederland</em>",
        "Blauweschild is actief in meerdere provincies. Kies je provincie voor meer informatie over onze diensten, het soort ongedierte dat we er vaak tegenkomen en de plaatsen waar we werken.", side,
        facts=["Binnen 24 uur ter plaatse", "Spoed: dezelfde dag", "7 dagen per week bereikbaar"]) + trustbar() + \
        section(head("Regionaal", "Overal dezelfde kwaliteit") + f'''<div class="split">
      <div class="prose"><p>Of je nu in een grachtenpand in Amsterdam woont, een boerderij in Brabant hebt of net in een nieuwbouwwoning in Almere bent getrokken: ongedierte houdt zich niet aan grenzen. Wel verschilt per regio welk ongedierte vaak voorkomt en hoe het binnenkomt.</p>
      <p>In oude binnensteden spelen vaak muizen en ratten, via kruipruimtes, oude riolering en houten vloeren. Op het platteland trekken muizen en ratten in het najaar van het land naar huizen en schuren. In nieuwbouwwijken zien we juist vaker papiervisjes en wespennesten onder dakpannen.</p>
      <p>Onze specialisten kennen die verschillen. Daardoor weten ze waar ze moeten zoeken en welke aanpak in jouw situatie het beste werkt.</p></div>
      {feat_cards(LOC_HOW, "stack", hz=True)}
    </div>''') + \
        section(head("Provincies", "Kies je regio", "Klik op je provincie voor de plaatsen waar we werken, typische situaties in de regio en antwoorden op veelgestelde vragen.") + f'<div class="cards">{cards}</div>', "alt") + \
        section(head("Veelgestelde vragen", "Over ons werkgebied") + faq(LOC_FAQ, cols=True)) + \
        section(cta(root, "Direct hulp nodig?", "Onze specialisten staan 7 dagen per week voor je klaar (08:00–17:00). Bel voor snelle hulp in jouw regio."), "alt")

built.append(page("locaties", "Locaties", "Blauweschild is actief in Noord-Holland, Zuid-Holland, Utrecht, Noord-Brabant, Gelderland, Flevoland en Overijssel. Binnen 24 uur ter plaatse.", locaties_main))

for pr in PROVINCES:
    def prov_main(root, pr=pr):
        c = pr["cities"]
        n = pr["name"]
        cl = ", ".join(c[:-1]) + " en " + c[-1] if len(c) > 1 else c[0]
        chips = "".join(f"<li>{ic('map-pin')}{E(x)}</li>" for x in c)
        side = side_card("Werkgebied", n, "Provincie", "map-pin", ("24 uur", "en we zijn bij je ter plaatse"),
                         [("Steden", E(", ".join(c))), ("Spoed", '<span class="urg hot">Dezelfde dag</span>'), ("Bereikbaar", "7 dagen per week, 08:00–17:00")])

        def local(i, p):
            a, b = c[i % len(c)], c[(i + 1) % len(c)]
            return f"{p['kort']} Ook in {a}, {b} en omgeving."
        why_local = [("timer", "Snel in de regio", f"Snel ter plaatse in heel {n}, ook in {c[0]} en {c[1]}.")] + WHY[1:]
        faq_local = [
            (f"Hoe snel zijn jullie in {n}?", f"Bij een gewone melding zijn we binnen 24 uur bij je, ook in {cl}. Bij spoed proberen we dezelfde dag te komen."),
            ("Mijn plaats staat er niet bij. Komen jullie wel?", f"Ja. We werken in heel {n}, ook in kleinere plaatsen en het buitengebied. Bel ons gerust om het na te vragen."),
            (f"Helpen jullie ook bedrijven in {n}?", "Ja. We werken voor horeca, winkels, kantoren, VvE's, verhuurders en agrarische bedrijven, met losse bestrijding of preventieve controles."),
            ("Wat kost een behandeling?", "Dat hangt af van het soort ongedierte en de omvang van de plaag. Na de inspectie krijg je een vrijblijvende offerte met een vaste prijs."),
        ]
        others = "".join(f'<li><a href="{lu(root, o["slug"])}">{ic("map-pin")}{E(o["name"])}</a></li>' for o in PROVINCES if o is not pr)
        prov_txt = n if pr["slug"] != "utrecht" else "de provincie Utrecht"
        return phero(root, [("Locaties", "locaties"), (n, None)], f"Ongediertebestrijding {n}", f"Ongedierte&shy;bestrijding in <em>{E(n)}</em>",
                     E(f"Actief in {cl} en heel {prov_txt}. Binnen 24 uur hulp bij ongedierte: effectief, discreet en met garantie op resultaat."), side,
                     facts=["Binnen 24 uur ter plaatse", "Garantie op resultaat", "Particulier en zakelijk"]) + trustbar() + \
            section(head("De regio", f"Ongedierte in {E(n)}") + f'''<div class="split">
      <div class="prose"><p>{E(pr["intro"])}</p><p>{E(pr["intro2"])}</p><p>Waar je ook woont in {E(n)}: we beginnen met een inspectie, pakken de oorzaak aan en sluiten de toegang af. Zo heb je niet alleen nu, maar ook later geen last meer.</p></div>
      {feat_cards(pr["situaties"], "stack", hz=True)}
    </div>''') + \
            section(head("Plaatsen", "Hier zijn we actief", f"Een greep uit de plaatsen in {E(n)} waar we werken. Woon je ergens anders in de provincie? Ook dan komen we graag langs.") + f'<ul class="chips">{chips}</ul>', "alt tight") + \
            section(head("Diensten", f"Welk ongedierte in {E(n)}?", f"We bestrijden alle soorten ongedierte in {E(n)}, voor particulieren en bedrijven.") + pest_grid(root, text=local)) + \
            section(head("Werkwijze", "Zo pakken we het aan") + steps(), "alt") + \
            section(head("Waarom Blauweschild", f"Jouw specialist in {E(n)}") + why(why_local)) + \
            section(head("Veelgestelde vragen", f"Vragen uit {E(n)}") + faq(faq_local, cols=True), "alt") + \
            section(cta(root, f"Direct hulp in {E(n)}?", f"Bel ons voor snelle, professionele ongediertebestrijding in {E(cl)} en de rest van {E(n)}.") +
                    head("Andere provincies", "Ook actief in") + f'<ul class="chips">{others}</ul>')

    built.append(page("locaties/" + pr["slug"], f"Ongediertebestrijding {pr['name']}",
        f"Ongediertebestrijding in {pr['name']}: actief in {', '.join(pr['cities'])}. Binnen 24 uur ter plaatse. Bel {TEL}.", prov_main))


# --- spoed
SPOED_WHEN = [
    ("rat", "Ratten in huis", "Ratten in de keuken, kruipruimte of op zolder verspreiden ziektes en knagen aan kabels en leidingen."),
    ("wesp", "Wespennest bij de deur", "Een nest bij de voordeur, een raam, het terras of een speelplek is een direct risico op steken."),
    ("bedwants", "Bedwantsen", "Hoe langer je wacht, hoe meer kamers besmet raken. Snel handelen beperkt de schade en de kosten."),
    ("kakkerlak", "Kakkerlakken in een keuken", "In een bedrijfskeuken of horecazaak kan een plaag tot problemen bij een inspectie leiden."),
    ("zap", "Knaagschade aan kabels", "Aangevreten elektriciteitskabels kunnen kortsluiting en brand veroorzaken. Laat dit direct bekijken."),
    ("activity", "Allergie in het gezin", "Is iemand allergisch voor wespensteken? Dan is een nest in de buurt altijd spoed."),
]
SPOED_ADVICE = {
    "ratten": "Houd deuren naar kruipruimte en kelder dicht en zet voedsel weg. Raak keutels niet met blote handen aan.",
    "bedwantsen": "Was beddengoed op 60 °C en neem geen spullen mee naar andere kamers.",
    "wespen": "Blijf uit de buurt van de opening en sluit hem niet zelf af; de wespen zoeken dan een weg naar binnen.",
    "kakkerlakken": "Ruim voedselresten op en zet etenswaren in afgesloten bakken. Gebruik geen spray: die verjaagt ze naar andere plekken.",
}
SPOED_ASK = ["Om welk dier het gaat, of wat je ziet of hoort", "Sinds wanneer je het merkt en hoe vaak", "Waar in huis of in het pand het zit",
             "Of er kinderen, huisdieren of mensen met een allergie zijn", "Je adres en een telefoonnummer waarop we je kunnen bereiken"]
SPOED_FAQ = [
    ("Hoe snel zijn jullie er bij spoed?", "Bij spoed proberen we dezelfde dag bij je te zijn. Hoe snel precies, hoor je meteen aan de telefoon."),
    ("Wat kost een spoedbehandeling?", "Dat hangt af van het soort ongedierte en de situatie. Je hoort vooraf wat het kost, zodat je niet voor verrassingen komt te staan."),
    ("Kan ik ook in het weekend bellen?", "Ja. We zijn 7 dagen per week bereikbaar van 08:00 tot 17:00. Bij spoed kun je ons ook buiten deze tijden bellen."),
    ("Ik ben gestoken en reageer heftig. Wat nu?", "Bij benauwdheid, duizeligheid of zwelling in gezicht of keel bel je direct 112. Daarna helpen wij je met het nest."),
]


def spoed_main(root):
    cards = "".join(
        f'<a class="card pcard" href="{pu(root, s)}"><div class="card-top">{tile(PEST[s]["icon"], "sig")}<span class="tagline hot">Urgent</span></div><h3>{E(PEST[s]["name"])}</h3><p><strong style="color:var(--text)">Dit kun je alvast doen:</strong> {E(t)}</p><span class="link">Meer over {E(PEST[s]["name"].lower())} {ic("arrow-right")}</span></a>'
        for s, t in SPOED_ADVICE.items())
    spoed_steps = [("phone-call", "Bel ons", "Neem direct telefonisch contact op. We stellen een paar korte vragen en plannen meteen."), ("truck", "Ter plaatse", "Onze specialist komt zo mogelijk dezelfde dag voor een inspectie."),
                   ("target", "Behandeling", "Directe bestrijding met professionele middelen, veilig voor jou en je gezin."), ("shield-check", "Garantie", "Controle en garantie dat het probleem echt is opgelost.")]
    side = side_card("Spoedlijn", TEL, "7 dagen per week", "siren", ("Vandaag", "nog bij je ter plaatse bij spoed"),
                     [("Open", "08:00–17:00, ook in het weekend"), ("Buiten tijden", "Bel bij spoed gerust")],
                     extra=f'<a class="btn btn-spoed" href="{TEL_HREF}" style="width:100%">{ic("phone-call")}Bel nu</a>')
    return phero(root, [("Spoed", None)], "Spoedservice · 7 dagen per week", "Acute <em>ongedierte</em>&shy;overlast?",
        "Wacht niet langer. Bij spoed zijn onze specialisten vandaag nog bij je ter plaatse. Snel, professioneel en met garantie op resultaat.", side,
        facts=["Dezelfde dag ter plaatse", "Ook in het weekend", "Garantie op resultaat"],
        buttons=f'<div class="actions"><a class="btn btn-spoed" href="{TEL_HREF}">{ic("phone-call")}Bel {E(TEL)}</a><button class="btn btn-ghost" type="button" data-spoed>{ic("phone-incoming")}Laat je terugbellen</button></div>') + trustbar() + \
        section(head("Wanneer is het spoed?", "Hier telt elk uur", "Niet elke plaag is spoed. Maar in deze situaties wil je niet wachten: het risico voor je gezondheid, je woning of je bedrijf is te groot.") + feat_cards(SPOED_WHEN, "cards", "sig")) + \
        section(head("Tot we er zijn", "Dit kun je alvast doen", "Een paar eenvoudige stappen beperken de schade en maken de bestrijding makkelijker. Ga vooral niet zelf aan de slag met spuitbussen.") + f'<div class="pgrid">{cards}</div>', "alt") + \
        section(head("Zo werkt het", "Hoe werkt onze spoedservice?", "Van telefoontje tot oplossing in vier stappen. Je weet steeds waar je aan toe bent.") + steps(spoed_steps) +
                stats([("Dezelfde dag", "Ter plaatse bij spoed"), ("08:00–17:00", "Dagelijks bereikbaar"), ("7/7", "Ook in het weekend"), ("Garantie", "Op elk resultaat")])) + \
        section(head("Aan de telefoon", "Wat we je vragen") + f'''<div class="split">
      <div class="prose"><p>Om je zo snel mogelijk te helpen, stellen we aan de telefoon een paar korte vragen. Zo weten we welke specialist en welk materiaal we meenemen, en hoe snel we moeten komen.</p><p>Heb je een foto van het dier, de keutels of het nest? Die helpt ons enorm. Je kunt hem na het gesprek mailen naar <a href="mailto:{MAIL}">{E(MAIL)}</a>.</p></div>
      <div class="card">{tile("list-checks")}<h3>Handig om bij de hand te hebben</h3>{checklist(SPOED_ASK)}</div>
    </div>''', "alt") + \
        section(head("Veelgestelde vragen", "Over spoedhulp") + faq(SPOED_FAQ, cols=True)) + \
        section(cta(root, "Spoed? Bel ons direct.", "Of laat je nummer achter, dan bellen we je zo snel mogelijk terug."), "alt")

built.append(page("spoed", "Spoedhulp bij ongedierte", f"Acute overlast van ratten, wespen, bedwantsen of kakkerlakken? Bel {TEL}. Dezelfde dag hulp, 7 dagen per week bereikbaar.", spoed_main))


# --- over ons
VALUES = [("target", "Resultaatgericht", "We stoppen pas als het probleem echt is opgelost. Met garantie op resultaat."),
          ("heart-handshake", "Klantgericht", "Jouw situatie staat centraal. We luisteren, adviseren en doen wat we beloven."),
          ("handshake", "Betrouwbaar", "Een duidelijke werkwijze, eerlijke prijzen en afspraken die we nakomen."),
          ("sparkles", "Vooruitstrevend", "We werken met de nieuwste technieken en middelen, en alleen waar ze nodig zijn.")]
IPM_STEPS = [("search", "Voorkomen", "We kijken naar de oorzaak: voedsel, vocht, schuilplekken en toegangen. Wat je weghaalt, trekt geen ongedierte meer aan."),
             ("activity", "Monitoren", "Met inspecties en monitoringvallen zien we hoe groot het probleem is en of het afneemt."),
             ("brick-wall", "Weren", "We dichten kieren, plaatsen roosters, gaas of rattenkleppen en houden ongedierte zo buiten."),
             ("target", "Bestrijden", "Pas als het nodig is, zetten we middelen in. Gericht, in de juiste dosis en op de juiste plek.")]
EXPECT = ["Uitleg over wat er aan de hand is en wat we doen", "Vooraf een duidelijke prijs, zonder verborgen kosten", "Middelen alleen waar ze echt nodig zijn",
          "Een controlebezoek en garantie op het resultaat", "Eerlijk advies, ook als je het zelf kunt oplossen", "Discretie: onopvallende voertuigen en kleding"]


def over_main(root):
    side = side_card("Over ons", "Blauweschild", "Ongediertebestrijding", "shield-check", ("10+ jaar", "ervaring in ongediertebestrijding"),
                     [("Werkgebied", "Heel Nederland"), ("Voor", "Particulier en zakelijk"), ("Werkwijze", "Volgens IPM")])
    return phero(root, [("Over ons", None)], "Over ons", "Een schild om <em>je huis</em>",
        "Al meer dan tien jaar je betrouwbare partner in professionele ongediertebestrijding. Gecertificeerd, discreet en altijd gericht op een blijvende oplossing.", side) + trustbar() + \
        section(head("Ons verhaal", "Waarom Blauweschild bestaat") + f'''<div class="split">
      <div class="prose">
        <p>Blauweschild is opgericht met één doel: mensen snel en goed helpen bij overlast van ongedierte. Wat klein begon, is uitgegroeid tot een bestrijdingsbedrijf dat door heel Nederland werkt, voor particulieren en bedrijven.</p>
        <p>Ons team van gecertificeerde specialisten heeft jarenlange ervaring en werkt met de nieuwste technieken en middelen. We vinden dat iedereen recht heeft op een veilige, ongediertevrije leefomgeving, zonder onnodig gif in huis.</p>
        <p>Onze naam zegt het al: we bestrijden niet alleen wat er nu zit, we zorgen ook dat het niet terugkomt. Daarom zoeken we altijd uit hoe het ongedierte binnenkomt en sluiten we die route af. Met meer dan 200 tevreden klanten en een gemiddelde Google-score van 4,9 uit 5 zijn we trots op het vertrouwen dat klanten in ons hebben.</p>
      </div>
      <div class="card">{tile("hand-heart", "lg")}<h3>Wat je van ons mag verwachten</h3>{checklist(EXPECT)}</div>
    </div>''' + stats()) + \
        section(head("Integrated Pest Management", "Eerst begrijpen, dan bestrijden", "We werken volgens IPM, de internationale standaard voor verantwoorde plaagdierbeheersing. Dat betekent vier stappen, in deze volgorde.") + steps(IPM_STEPS), "alt") + \
        section(head("Onze waarden", "Waar we voor staan", "Vier principes die je terugziet in elke inspectie, elke behandeling en elk gesprek.") + why(VALUES)) + \
        section(head("Reviews", "Wat klanten zeggen", None, side=score()) + reviews(), "alt") + \
        section(cta(root, "Kennismaken?", f"Bel ons op {E(TEL)} of vraag een inspectie aan. We denken graag met je mee."))

built.append(page("over-ons", "Over ons", "Maak kennis met Blauweschild: meer dan tien jaar ervaring, gecertificeerde specialisten, werken volgens IPM en actief in heel Nederland.", over_main))


# --- vacatures
PERKS = [("euro", "Goed salaris", "Een marktconform salaris en goede secundaire arbeidsvoorwaarden."), ("graduation-cap", "Opleiding", "Opleiding en begeleiding, ook als je nog geen ervaring hebt."),
         ("users", "Hecht team", "Werken door heel Nederland, met collega's die voor elkaar klaarstaan."), ("award", "Doorgroeien", "Doorgroeimogelijkheden binnen een bedrijf dat hard groeit.")]
ROLES = [
    ("bug-off", "Ongediertebestrijder", "Buitendienst", "Je gaat op pad naar klanten, doet inspecties, bestrijdt ongedierte en geeft advies om herhaling te voorkomen. Je bent het gezicht van Blauweschild bij de klant.",
     ["Inspecties en behandelingen bij particulieren en bedrijven", "Advies over preventie en afdichting", "Rapporteren wat je hebt gedaan en gezien"]),
    ("wrench", "Monteur / technisch medewerker", "Buitendienst", "Je zorgt dat ongedierte buiten blijft: kieren dichten, roosters en gaas plaatsen, rattenkleppen monteren en helpen bij rioolinspecties.",
     ["Afdichten van woningen en bedrijfspanden", "Plaatsen van roosters, gaas en rattenkleppen", "Samenwerken met de bestrijders in het veld"]),
    ("headset", "Klantenservice", "Binnendienst", "Je staat klanten te woord aan de telefoon en per mail, stelt de juiste vragen en plant afspraken in. Bij spoed zorg jij dat er snel iemand komt.",
     ["Telefoon en e-mail van klanten beantwoorden", "Afspraken en spoedmeldingen inplannen", "Klanten op de hoogte houden"]),
]
SEEK = ["Je bent klantvriendelijk en kunt dingen helder uitleggen", "Je werkt zelfstandig, netjes en betrouwbaar", "Je bent niet vies van een kruipruimte of zolder (buitendienst)", "Je bent leergierig: het vak leren we je"]


def vac_main(root):
    funcs = "".join(f"<option>{E(x)}</option>" for x in ["Ongediertebestrijder", "Monteur / technisch medewerker", "Klantenservice", "Open sollicitatie", "Anders"])
    roles = "".join(f'<div class="card">{tile(i, "lg")}<span class="tagline" style="justify-self:start">{E(t)}</span><h3>{E(n)}</h3><p>{E(d)}</p>{checklist(li)}<a class="link" href="#solliciteer">Solliciteer {ic("arrow-right")}</a></div>' for i, n, t, d, li in ROLES)
    proc = [("send", "Sollicitatie", "Je stuurt het formulier hieronder in, met een korte motivatie."), ("phone-call", "Kennismaking", "We bellen je binnen een paar werkdagen voor een eerste kennismaking."),
            ("users", "Gesprek", "Je komt langs voor een gesprek en, bij buitendienst, een dag meelopen."), ("graduation-cap", "Aan de slag", "Je start met een inwerkperiode en opleiding.")]
    side = side_card("Werken bij", "Blauweschild", "We groeien", "briefcase", ("3", "functies, plus open sollicitatie"),
                     [("Ervaring", "Niet vereist"), ("Opleiding", "Wij leiden je op"), ("Werkgebied", "Heel Nederland")])
    return phero(root, [("Vacatures", None)], "Werken bij", "Werken bij <em>Blauweschild</em>",
        "We groeien en zoeken gemotiveerde collega's die samen met ons Nederland ongediertevrij houden. Ervaring is mooi, maar motivatie is belangrijker: het vak leren we je.", side,
        buttons=f'<div class="actions"><a class="btn btn-primary" href="#solliciteer">{ic("send")}Solliciteer direct</a><a class="btn btn-ghost" href="#functies">{ic("briefcase")}Bekijk functies</a></div>') + \
        section(head("Waarom bij ons?", "Een vak met impact") + f'''<div class="split">
      <div class="prose"><p>Blauweschild groeit hard en we zijn steeds op zoek naar enthousiaste vakmensen. Heb je al ervaring in de ongediertebestrijding, of ben je gemotiveerd om het vak te leren? We horen graag van je.</p><p>Het werk is afwisselend: geen dag is hetzelfde. De ene dag help je een gezin dat niet meer rustig slaapt door bedwantsen, de volgende dag zorg je dat een restaurant weer zonder zorgen open kan. Je ziet direct het resultaat van je werk, en klanten zijn je dankbaar.</p></div>
      <div class="card">{tile("user-check", "lg")}<h3>Wie zoeken we?</h3>{checklist(SEEK)}</div>
    </div>''' + feat_cards(PERKS, "cards four")) + \
        section(head("Functies", "Waar kun je ons mee helpen?", "Staat er geen passende functie bij? Solliciteer gerust open. We nemen elke aanmelding serieus.") + f'<div class="cards">{roles}</div>', "alt", "functies") + \
        section(head("Procedure", "Zo verloopt het", "Kort en persoonlijk. Je hoort altijd van ons, ook als het niet past.") + steps(proc)) + \
        section(f'''<div class="split">
      <div class="contact-side">{head("Solliciteer direct", "Kom ons team versterken", "Vul het formulier in. We nemen binnen een paar werkdagen contact met je op.")}
        <div class="card">{tile("circle-help")}<h3>Vragen over werken bij ons?</h3><p>Bel ons op <a href="{TEL_HREF}">{E(TEL)}</a> of mail naar <a href="mailto:{MAIL}">{E(MAIL)}</a>. We vertellen je graag meer over de functies en het team.</p></div>
      </div>
      <form class="xform" data-form="Sollicitatie" data-subject="Sollicitatie" data-redirect novalidate>
        <div class="xform-head">{tile("send")}<div><h3>Sollicitatieformulier</h3><p>Velden met <span class="req">*</span> zijn verplicht.</p></div></div>
        {honeypot()}
        <div class="row">{field("v-naam", "naam", "Naam", req=True, ac="name")}{field("v-mail", "email", "E-mail", "email", True, "email", "naam@voorbeeld.nl")}</div>
        <div class="row">{field("v-tel", "telefoon", "Telefoonnummer", "tel", ac="tel", ph="06 12345678")}{field("v-plaats", "woonplaats", "Woonplaats", ac="address-level2")}</div>
        {seg("functie", "Voor welke functie?", [("Ongediertebestrijder", "bug-off"), ("Monteur", "wrench"), ("Klantenservice", "headset"), ("Open sollicitatie", "send")], "Ongediertebestrijder")}
        {seg("ervaring", "Ervaring in het vak?", ["Ja", "Een beetje", "Nee, maar ik wil het leren"], "Nee, maar ik wil het leren")}
        {textarea("v-mot", "motivatie", "Motivatie", "Vertel kort wie je bent en waarom je bij ons wilt werken.", req=True)}
        {consent("v-ok", "Ik ga akkoord dat Blauweschild mijn gegevens gebruikt voor deze sollicitatie.")}
        <button class="btn btn-primary btn-lg" type="submit">{ic("send")}Verstuur sollicitatie</button>
        {form_foot()}
        <div class="sent" role="status" hidden></div>
      </form>
    </div>''', "alt", "solliciteer")

built.append(page("vacatures", "Vacatures", "Werken bij Blauweschild Ongediertebestrijding: ongediertebestrijder, monteur of klantenservice. Opleiding en begeleiding, ook zonder ervaring.", vac_main))


# --- contact
AFTER = [("message-circle", "We nemen contact op", "Binnen één werkdag bellen we je terug, bij spoed zo snel mogelijk."), ("calendar-check", "Afspraak", "We plannen een inspectie op een moment dat jou uitkomt."),
         ("scan-search", "Inspectie", "Onze specialist bekijkt de situatie en legt uit wat er aan de hand is."), ("clipboard-list", "Voorstel", "Je krijgt een duidelijk voorstel met aanpak en prijs. Pas daarna gaan we aan de slag.")]
MENTION = ["Welk dier je denkt te zien, of wat je ziet of hoort", "Sinds wanneer je het merkt", "Waar in huis of in het pand het zit", "Of het om een woning of een bedrijf gaat", "Een foto, als je die hebt"]
CONTACT_FAQ = [
    ("Hoe snel reageren jullie op een aanvraag?", "Binnen één werkdag nemen we contact met je op. Bij spoed kun je het beste bellen, dan helpen we je meteen."),
    ("Is een inspectie vrijblijvend?", "Na de inspectie krijg je een voorstel met aanpak en prijs. Je beslist zelf of je daarmee verder wilt."),
    ("Kan ik een foto sturen?", f"Graag. Mail je foto naar {MAIL}, met je naam en telefoonnummer. Een foto helpt ons om snel te zien wat het is."),
]


def contact_main(root):
    methods = f'''<div class="cards">
      <a class="card" href="{TEL_HREF}">{tile("phone")}<h3>Bel ons</h3><p>De snelste manier om geholpen te worden. 7 dagen per week, 08:00–17:00.</p><span class="link" style="font-size:1.05rem;color:var(--text)">{E(TEL)} {ic("arrow-right")}</span></a>
      <a class="card" href="mailto:{MAIL}">{tile("mail")}<h3>Mail ons</h3><p>Stuur je vraag of een foto. We reageren binnen één werkdag.</p><span class="link" style="overflow-wrap:anywhere">{E(MAIL)}</span></a>
      <button class="card warn" type="button" data-spoed style="text-align:left;font:inherit;color:inherit;cursor:pointer">{tile("siren", "sig")}<h3>Spoed?</h3><p>Ratten in huis, een wespennest bij de deur of bedwantsen? We komen zo mogelijk dezelfde dag.</p><span class="link" style="color:var(--signal)">Spoedhulp {ic("arrow-right")}</span></button>
    </div>'''
    return phero(root, [("Contact", None)], "Contact", "Neem <em>contact</em> op",
        "Bel ons, mail ons of vul het formulier in. We helpen je direct verder en plannen een inspectie op een moment dat jou uitkomt.",
        buttons=f'<div class="actions"><a class="btn btn-spoed" href="{TEL_HREF}">{ic("phone")}Bel {E(TEL)}</a><a class="btn btn-primary" href="#formulier">{ic("send")}Naar het formulier</a></div>') + \
        trustbar() + section(methods, "tight") + \
        section(f'''<div class="form-layout">
      <div id="formulier">{detailed_form("c")}</div>
      <aside class="form-aside">
        <div class="card warn">{tile("phone-call", "sig")}<h3>Liever direct contact?</h3><p>Bel ons, dan plannen we meteen een afspraak. Bij spoed is bellen altijd het snelst.</p><a class="btn btn-spoed" href="{TEL_HREF}">{ic("phone")}Bel {E(TEL)}</a><a class="link" href="mailto:{MAIL}" style="overflow-wrap:anywhere">{ic("mail")}{E(MAIL)}</a></div>
        <div class="card">{tile("list-checks")}<h3>Handig om te vermelden</h3>{checklist(MENTION)}</div>
        <div class="card">{tile("lock")}<h3>Veilig en vertrouwelijk</h3><p>We gebruiken je gegevens alleen om contact met je op te nemen over je aanvraag. We delen ze niet met anderen.</p></div>
        <div class="card">
          <h3>Bedrijfsgegevens</h3>
          <dl class="dl">
            <dt>Bedrijf</dt><dd>Blauweschild Ongediertebestrijding</dd>
            <dt>Telefoon</dt><dd><a href="{TEL_HREF}">{E(TEL)}</a></dd>
            <dt>E-mail</dt><dd><a href="mailto:{MAIL}">{E(MAIL)}</a></dd>
            <dt>Open</dt><dd>7 dagen per week, 08:00–17:00</dd>
            <dt>Werkgebied</dt><dd><a href="{u(root, "locaties")}">Heel Nederland</a></dd>
          </dl>
        </div>
      </aside>
    </div>''', "alt") + \
        section(head("Na je aanvraag", "Wat gebeurt er nu?", "Zo ziet het traject eruit, van je aanvraag tot de start van de behandeling.") + steps(AFTER)) + \
        section(head("Veelgestelde vragen", "Over contact en afspraken") + faq(CONTACT_FAQ, cols=True), "alt")

built.append(page("contact", "Contact", f"Neem contact op met Blauweschild Ongediertebestrijding. Bel {TEL}, mail {MAIL} of vraag online een inspectie aan.", contact_main))


# --- bedankt
def bedankt_main(root):
    nxt = [("message-circle", "We bellen je", "Binnen één werkdag nemen we contact met je op. Bij spoed zo snel mogelijk."), ("calendar-check", "Afspraak maken", "Samen plannen we een moment voor de inspectie."),
           ("scan-search", "Inspectie", "Onze specialist komt langs en legt uit wat er aan de hand is en wat de aanpak is.")]
    tips = ["Ruim voedsel op en bewaar het in afgesloten bakken", "Ga niet zelf aan de slag met spuitbussen: die verjagen ongedierte naar andere plekken", "Maak, als het kan, een foto van het dier, de keutels of het nest",
            "Houd kinderen en huisdieren uit de buurt van een wespennest", "Neem bij bedwantsen geen spullen mee naar andere kamers", "Houd deuren naar kelder, kruipruimte en zolder dicht"]
    return phero(root, [("Bedankt", None)], "Verstuurd", "Bedankt voor je <em>bericht</em>",
        "We hebben je aanvraag goed ontvangen en nemen zo snel mogelijk contact met je op. Hieronder lees je wat er nu gebeurt en wat je in de tussentijd alvast kunt doen.",
        buttons=f'<div class="actions"><a class="btn btn-primary" href="{u(root)}">{ic("house")}Terug naar de homepage</a><a class="btn btn-ghost" href="{u(root, "diensten")}">Bekijk onze diensten</a></div>').replace("<h1>", "<h1 data-thanks>", 1).replace('<p class="lead">', '<p class="lead" data-thanks-lead>', 1) + \
        section(head("Wat gebeurt er nu?", "De volgende stappen") + steps(nxt, "steps three")) + \
        section(head("In de tussentijd", "Dit kun je alvast doen", "Met deze stappen beperk je de overlast en maak je de bestrijding makkelijker.") + checklist(tips, "tips"), "alt") + \
        section(head("Lees alvast verder", "Meer over je plaagdier", "Op de pagina van elk plaagdier lees je hoe je het herkent, wat de risico's zijn en hoe we het aanpakken.") + pest_tiles(root)) + \
        section(cta(root, "Is het dringend?", "Wacht dan niet op onze terugbelactie, maar bel ons direct. We helpen je meteen verder."), "alt")

built.append(page("bedankt", "Bedankt", "Bedankt voor je bericht. We nemen zo snel mogelijk contact met je op.", bedankt_main))

print(f"{len(built)} pagina's gemaakt (woorden in de hoofdinhoud):")
for b, w in built:
    print(f"  {b:28} {w}")
