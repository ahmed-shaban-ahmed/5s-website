# -*- coding: utf-8 -*-
"""Static site generator for 5S (فايف إس). Run: python3 _build/build.py
Writes folder-based pages (about/index.html, ...) with relative links so the
site works under the GitHub Pages sub-path /5s-website/."""
import json, os, html
from urllib.parse import quote
from data import *

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = html.escape

# ------------------------------------------------------------------ icons (1.5px line)
IC = {
 "dune": '<path d="M2 18c3-4 6-6 10-6s7 2 10 6"/><path d="M5 13c2-3 4-4 7-4"/><path d="M14 7c2 0 4 1 6 3"/>',
 "road": '<path d="M8 3 4 21"/><path d="M16 3l4 18"/><path d="M12 5v2M12 11v2M12 17v2"/>',
 "slope": '<path d="M3 20h18L3 6z"/><path d="M7 15l3 2M5 11l2 1"/>',
 "dust": '<circle cx="6" cy="8" r="1.5"/><circle cx="12" cy="6" r="1"/><circle cx="17" cy="9" r="1.5"/><circle cx="9" cy="13" r="1"/><circle cx="15" cy="14" r="1"/><path d="M3 19h18"/>',
 "walk": '<circle cx="13" cy="4" r="2"/><path d="M11 21l2-6 3 3v3M9 12l2-4 4 2 2 3M13 15l-2-3"/>',
 "pipe": '<path d="M2 9h12a4 4 0 0 1 4 4v8"/><path d="M2 15h9a1 1 0 0 1 1 1v5"/>',
 "building": '<rect x="4" y="3" width="10" height="18" rx="1"/><path d="M14 9h6v12h-6M8 7h2M8 11h2M8 15h2"/>',
 "layers": '<path d="M12 3 2 8l10 5 10-5z"/><path d="M2 13l10 5 10-5"/>',
 "truck": '<rect x="2" y="7" width="12" height="9" rx="1"/><path d="M14 10h4l3 3v3h-7"/><circle cx="6" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>',
 "bridge": '<path d="M2 16h20M4 16V10M20 16V10M2 10c4-4 16-4 20 0M8 16v-4M16 16v-4"/>',
 "drop": '<path d="M12 3s6 7 6 11a6 6 0 0 1-12 0c0-4 6-11 6-11z"/>',
 "plane": '<path d="M2 16l8-2 4 6 2-1-2-6 6-2a2 2 0 0 0-1-4l-6 2-6-5-2 1 3 6-4 1-2-1-1 1z"/>',
 "factory": '<path d="M3 21V10l6 4V10l6 4V5h6v16z"/><path d="M7 18h2M12 18h2M17 18h2"/>',
 "flag": '<path d="M5 21V4M5 4h11l-2 4 2 4H5"/>',
 "heritage": '<path d="M3 21h18M5 21V9l7-5 7 5v12M9 21v-6h6v6"/>',
 "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
 "leaf": '<path d="M5 19c0-9 6-14 15-14 0 9-5 15-14 15"/><path d="M5 19l7-7"/>',
 "flagsa": '<path d="M4 21V4"/><rect x="4" y="4" width="16" height="10" rx="1"/><path d="M8 9h8"/>',
 "flask": '<path d="M9 3h6M10 3v6L4 19a1.5 1.5 0 0 0 1.3 2h13.4a1.5 1.5 0 0 0 1.3-2L14 9V3"/><path d="M7 15h10"/>',
 "coin": '<circle cx="12" cy="12" r="8"/><path d="M14.5 9.5c-.5-1-1.5-1.5-2.5-1.5-1.5 0-2.5.8-2.5 2s1 1.6 2.5 2 2.5.8 2.5 2-1 2-2.5 2c-1 0-2-.5-2.5-1.5M12 6.5v1.5M12 16v1.5"/>',
 "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4 12H2M22 12h-2M5 5l1.5 1.5M17.5 17.5 19 19M5 19l1.5-1.5M17.5 6.5 19 5"/>',
 "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
 "phone": '<path d="M5 3h4l2 5-3 2a11 11 0 0 0 6 6l2-3 5 2v4a2 2 0 0 1-2 2A17 17 0 0 1 3 5a2 2 0 0 1 2-2z"/>',
 "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
 "pin": '<path d="M12 21s7-6 7-12a7 7 0 0 0-14 0c0 6 7 12 7 12z"/><circle cx="12" cy="9" r="2.5"/>',
 "download": '<path d="M12 3v12M7 10l5 5 5-5M4 21h16"/>',
 "doc": '<path d="M6 3h8l5 5v13H6z"/><path d="M14 3v5h5M9 13h7M9 17h5"/>',
 "package": '<path d="M3 7l9-4 9 4v10l-9 4-9-4z"/><path d="M3 7l9 4 9-4M12 11v10"/>',
 "users": '<circle cx="9" cy="8" r="3"/><path d="M3 20c0-3 3-5 6-5s6 2 6 5"/><circle cx="17" cy="9" r="2.5"/><path d="M16 15c3 0 5 2 5 5"/>',
 "award": '<circle cx="12" cy="9" r="5"/><path d="M9 13l-2 8 5-3 5 3-2-8"/>',
 "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>',
}
def icon(name, cls="icon"):
    return f'<span class="{cls}" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{IC.get(name, IC["spark"])}</svg></span>'

WA_SVG = '<svg viewBox="0 0 32 32" aria-hidden="true"><path fill="currentColor" d="M16.01 3C9.39 3 4 8.39 4 15.01c0 2.11.55 4.16 1.6 5.98L4 29l8.2-1.55A11.96 11.96 0 0 0 16.01 27C22.63 27 28 21.61 28 14.99 28 8.39 22.63 3 16.01 3zm6.9 16.98c-.29.82-1.7 1.51-2.36 1.61-.61.09-1.38.13-2.23-.14-.51-.16-1.17-.38-2.02-.74-3.55-1.54-5.86-5.13-6.04-5.37-.17-.24-1.43-1.9-1.43-3.63s.9-2.57 1.22-2.92c.32-.35.7-.44.93-.44h.67c.22 0 .5-.08.78.6.29.71.98 2.4 1.07 2.57.09.17.14.38.03.61-.12.24-.18.38-.35.59-.17.2-.36.45-.51.61-.17.17-.35.36-.15.7.2.35.88 1.45 1.89 2.35 1.3 1.15 2.4 1.51 2.74 1.68.35.17.55.14.75-.09.2-.22.87-.99 1.1-1.33.23-.35.46-.29.78-.17.32.12 2.04.96 2.39 1.13.35.18.58.26.67.41.08.15.08.86-.21 1.68z"/></svg>'
SOC = {
 "x": '<svg viewBox="0 0 24 24"><path d="M17.8 3h3.1l-6.8 7.7L22 21h-6.2l-4.9-6.4L5.3 21H2.2l7.3-8.3L2 3h6.4l4.4 5.8zm-1.1 16.2h1.7L7.4 4.7H5.5z"/></svg>',
 "yt": '<svg viewBox="0 0 24 24"><path d="M23 7.2a3 3 0 0 0-2.1-2.1C19 4.6 12 4.6 12 4.6s-7 0-8.9.5A3 3 0 0 0 1 7.2 31 31 0 0 0 .5 12 31 31 0 0 0 1 16.8a3 3 0 0 0 2.1 2.1c1.9.5 8.9.5 8.9.5s7 0 8.9-.5a3 3 0 0 0 2.1-2.1 31 31 0 0 0 .5-4.8 31 31 0 0 0-.5-4.8zM9.7 15V9l5.9 3z"/></svg>',
 "in": '<svg viewBox="0 0 24 24"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9.5h4V21H3zM9.5 9.5h3.8v1.6h.1c.5-1 1.8-2 3.8-2 4 0 4.8 2.6 4.8 6V21h-4v-5.2c0-1.3 0-2.9-1.8-2.9s-2 1.4-2 2.8V21h-4z"/></svg>',
 "ig": '<svg viewBox="0 0 24 24"><path d="M12 7a5 5 0 1 0 0 10 5 5 0 0 0 0-10zm0 8.2a3.2 3.2 0 1 1 0-6.4 3.2 3.2 0 0 1 0 6.4zM17.3 5.5a1.2 1.2 0 1 0 0 2.4 1.2 1.2 0 0 0 0-2.4zM12 2.2c-2.7 0-3 0-4 .1-3.6.2-5.5 2-5.7 5.7-.1 1-.1 1.4-.1 4s0 3 .1 4c.2 3.6 2 5.5 5.7 5.7 1 .1 1.4.1 4 .1s3 0 4-.1c3.6-.2 5.5-2 5.7-5.7.1-1 .1-1.4.1-4s0-3-.1-4c-.2-3.6-2-5.5-5.7-5.7-1-.1-1.3-.1-4-.1z"/></svg>',
}

def L(href, depth):
    """Make a site-root path relative for a page at the given folder depth."""
    if href.startswith(("http", "mailto:", "tel:", "#")):
        return href
    if depth:
        return ("../" * depth) + href
    return href or "./"

def head(title, desc, path, depth, extra_ld=None, cls=""):
    assert len(title) < 60, (title, len(title))
    assert len(desc) < 156, (path, len(desc))
    canon = SITE + path
    lds = "".join(f'\n  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>' for ld in (extra_ld or []))
    return f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{E(title)}</title>
  <meta name="description" content="{E(desc)}"/>
  <link rel="canonical" href="{canon}"/>
  <meta property="og:type" content="website"/>
  <meta property="og:locale" content="ar_SA"/>
  <meta property="og:site_name" content="فايف إس 5S"/>
  <meta property="og:title" content="{E(title)}"/>
  <meta property="og:description" content="{E(desc)}"/>
  <meta property="og:url" content="{canon}"/>
  <meta property="og:image" content="{SITE}assets/hero-poster.jpg"/>
  <meta name="twitter:card" content="summary_large_image"/>
  <meta name="theme-color" content="#397E3D"/>
  <link rel="icon" href="{L('assets/favicon.svg', depth)}" type="image/svg+xml"/>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link href="https://fonts.googleapis.com/css2?family=Readex+Pro:wght@300;400;500;600;700&amp;display=swap" rel="stylesheet"/>
  <link rel="stylesheet" href="{L('css/style.css', depth)}"/>{lds}
</head>
<body class="{cls}">
  <a class="skip-link" href="#main">تخطَّ إلى المحتوى</a>
'''

NAV = [
  ("home", "الرئيسية", ""),
  ("about", "من نحن", "about/"),
  ("solutions", "الحلول", [("solutions/", "تقنية 5S — نظرة عامة")] + [(f"solutions/{p['slug']}/", p["name"]) for p in PRODUCTS]),
  ("sectors", "القطاعات", [("sectors/", "كل القطاعات")] + [(f"sectors/{s['slug']}/", s["name"]) for s in SECTORS]),
  ("projects", "المشاريع", "projects/"),
  ("knowledge", "المعرفة", [("technical-data/", "البيانات الفنية"), (None, "الأخبار والإعلام — قريبًا"), ("calculator/", "حاسبة المواد"), ("partners/", "الشركاء والوكلاء")]),
  ("contact", "تواصل معنا", "contact/"),
]

def header(active, depth):
    d, m = [], []
    for key, label, target in NAV:
        is_act = key == active
        if isinstance(target, list):
            items = "".join(
                (f'<li><a href="{L(h, depth)}">{E(t)}</a></li>' if h else f'<li><span class="is-disabled" aria-disabled="true">{E(t)}</span></li>')
                for h, t in target)
            wide = " dropdown--wide" if key == "sectors" else ""
            d.append(f'<li class="has-dd{" is-active" if is_act else ""}"><button class="dd-btn" type="button" aria-expanded="false" aria-haspopup="true">{label}</button><ul class="dropdown{wide}">{items}</ul></li>')
            mitems = "".join(
                (f'<li><a href="{L(h, depth)}">{E(t)}</a></li>' if h else f'<li><span class="is-disabled" aria-disabled="true">{E(t)}</span></li>')
                for h, t in target)
            m.append(f'<li><button class="acc-btn" type="button" aria-expanded="false" aria-controls="acc-{key}">{label}</button><ul class="acc-panel" id="acc-{key}">{mitems}</ul></li>')
        else:
            cur = ' aria-current="page"' if is_act else ""
            d.append(f'<li><a href="{L(target, depth)}"{cur}>{label}</a></li>')
            m.append(f'<li><a href="{L(target, depth)}"{cur}>{label}</a></li>')
    return f'''  <header class="site-header" id="top">
    <div class="wrap header-inner">
      <a class="logo" href="{L('', depth)}" aria-label="فايف إس — الصفحة الرئيسية">
        <img class="logo-mark" src="{L('assets/logo-mark.png', depth)}" alt="5S" width="52" height="48"/>
        <img class="logo-full" src="{L('assets/logo.png', depth)}" alt="فايف إس لحلول تثبيت الرمال والتربة" width="88" height="64"/>
        <img class="logo-white" src="{L('assets/logo-white.png', depth)}" alt="فايف إس لحلول تثبيت الرمال والتربة" width="88" height="64"/>
      </a>
      <nav class="main-nav" aria-label="القائمة الرئيسية"><ul>{"".join(d)}</ul></nav>
      <div class="header-actions">
        <button class="lang-switch" type="button" disabled title="النسخة الإنجليزية قيد الإعداد">EN قريبًا</button>
        <a class="btn btn-gold header-cta" href="{L('contact/', depth)}#quote">اطلب عرض سعر</a>
        <button class="menu-toggle" id="menu-toggle" type="button" aria-expanded="false" aria-controls="mobile-menu" aria-label="فتح القائمة"><span></span><span></span><span></span></button>
      </div>
    </div>
    <nav class="mobile-menu" id="mobile-menu" aria-label="قائمة الجوال">
      <ul>{"".join(m)}</ul>
      <a class="btn btn-gold" href="{L('contact/', depth)}#quote">اطلب عرض سعر</a>
    </nav>
  </header>
'''

def banner(title, crumbs, depth, sub=None, tag=None):
    items = [f'<li><a href="{L("", depth)}">الرئيسية</a></li>']
    for i, (lab, href) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            items.append(f'<li aria-current="page">{E(lab)}</li>')
        else:
            items.append(f'<li><a href="{L(href, depth)}">{E(lab)}</a></li>')
    s = f'<p class="banner-sub">{sub}</p>' if sub else ""
    t = f'<span class="banner-tag">{E(tag)}</span>' if tag else ""
    return f'''    <section class="page-banner" aria-labelledby="page-title">
      <div class="wrap">
        <nav class="breadcrumb" aria-label="مسار التنقل"><ol>{"".join(items)}</ol></nav>
        <h1 id="page-title">{title}</h1>{s}{t}
      </div>
    </section>
'''

def crumbs_ld(crumbs):
    els = [{"@type": "ListItem", "position": 1, "name": "الرئيسية", "item": SITE}]
    for i, (lab, href) in enumerate(crumbs, start=2):
        els.append({"@type": "ListItem", "position": i, "name": lab, "item": SITE + href})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": els}

def faq_ld(pairs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]}

def sector_select(name="sector", required=True, label="القطاع"):
    opts = "".join(f'<option value="{E(n)}">{E(n)}</option>' for _, n in SECTOR_OPTIONS)
    return f'<label class="field">{label}<select name="{name}"{" required" if required else ""}><option value="">— اختر القطاع —</option>{opts}</select></label>'

def phone_field(required=True, name="phone"):
    return f'<label class="field">رقم الجوال<span class="phone-group"><span class="cc">+966</span><input type="tel" name="{name}" inputmode="tel" autocomplete="tel-national" placeholder="5XXXXXXXX" data-phone{" required" if required else ""}/></span></label>'

def hidden(subject, source):
    return (f'<input type="hidden" name="_subject" value="{E(subject)}"/>'
            '<input type="hidden" name="_captcha" value="false"/><input type="hidden" name="_template" value="table"/>'
            f'<input type="hidden" name="source_page" value="{E(source)}"/>'
            '<span class="hp" aria-hidden="true"><input type="text" name="_honey" tabindex="-1" autocomplete="off"/></span>')

def cta_final(depth, source):
    return f'''    <section class="cta-final dunes" aria-labelledby="cta-final-title">
      <div class="wrap cta-final-grid">
        <div class="reveal">
          <p class="kicker">تقنية عالمية. صناعة سعودية. نتائج تدوم.</p>
          <h2 id="cta-final-title">لديك مشروع في بيئة رملية؟ تحدث إلى مهندسينا</h2>
          <p>اترك بياناتك وسيتواصل معك مهندس من فريقنا لاختيار الحل المناسب لتربتك.</p>
          <form class="short-form" action="{FORM_ACTION}" method="POST" data-validate>
            {hidden("طلب تواصل سريع — فايف إس", source)}
            <label class="field">الاسم<input type="text" name="name" autocomplete="name" required/></label>
            {phone_field()}
            {sector_select()}
            <div class="form-actions">
              <button class="btn btn-gold" type="submit">اطلب عرض سعر</button>
              <a class="wa-link" href="{WA}" target="_blank" rel="noopener">{WA_SVG} أو تحدث معنا عبر واتساب</a>
            </div>
          </form>
          <div class="form-success" role="status">شكرًا لك! وصلنا طلبك، وسيتواصل معك فريقنا خلال يوم عمل. <span class="ph-badge">مدة الرد بانتظار اعتماد الإدارة</span></div>
        </div>
        <div class="visual reveal">
          <img src="{L('assets/img/product-can.webp', depth)}" alt="عبوة منتج فايف إس لتثبيت الرمال والتربة" width="600" height="664" loading="lazy"/>
        </div>
      </div>
    </section>
'''

def footer(depth):
    sol = "".join(f'<li><a href="{L("solutions/" + p["slug"] + "/", depth)}">{p["name"]}</a></li>' for p in PRODUCTS)
    sec = "".join(f'<li><a href="{L("sectors/" + s["slug"] + "/", depth)}">{E(s["name"])}</a></li>' for s in SECTORS[:6])
    return f'''  <footer class="site-footer">
    <div class="wrap">
      <div class="footer-grid">
        <div class="footer-brand">
          <img src="{L('assets/logo-white.png', depth)}" alt="فايف إس" width="99" height="72" loading="lazy"/>
          <p>فايف إس شركة سعودية متخصصة في حلول ومواد تثبيت الرمال والتربة. تقنية عالمية، صناعة سعودية.</p>
          <div class="social">
            <a href="https://x.com/5sSolution" target="_blank" rel="noopener" aria-label="X — 5sSolution">{SOC["x"]}</a>
            <a href="{VIDEO}" target="_blank" rel="noopener" aria-label="YouTube">{SOC["yt"]}</a>
            <span title="رابط LinkedIn بانتظار العميل" role="img" aria-label="LinkedIn — الرابط بانتظار العميل">{SOC["in"]}</span>
            <a href="https://www.instagram.com/5s_techo/" target="_blank" rel="noopener" aria-label="Instagram">{SOC["ig"]}</a>
          </div>
        </div>
        <div><h3>الحلول</h3><ul><li><a href="{L('solutions/', depth)}">تقنية 5S</a></li>{sol}</ul></div>
        <div><h3>القطاعات</h3><ul>{sec}<li><a href="{L('sectors/', depth)}">كل القطاعات ←</a></li></ul></div>
        <div><h3>الشركة</h3><ul>
          <li><a href="{L('about/', depth)}">من نحن</a></li>
          <li><a href="{L('projects/', depth)}">المشاريع</a></li>
          <li><a href="{L('partners/', depth)}">الشركاء والوكلاء</a></li>
          <li><a href="{L('technical-data/', depth)}">البيانات الفنية</a></li>
          <li><a href="{L('calculator/', depth)}">حاسبة المواد</a></li>
          <li><a href="{B2C}" target="_blank" rel="noopener">المتجر الإلكتروني (B2C)</a></li>
        </ul></div>
        <div>
          <h3>تواصل معنا</h3>
          <ul>
            <li><a href="tel:{PHONE1_TEL}" dir="ltr">{PHONE1}</a></li>
            <li><a href="tel:{PHONE2_TEL}" dir="ltr">{PHONE2}</a></li>
            <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
            <li>برج بوابة الخبر، الطابق 21، الخبر</li>
          </ul>
          <form class="newsletter" action="{FORM_ACTION}" method="POST" data-validate aria-label="الاشتراك في النشرة">
            {hidden("اشتراك في النشرة — فايف إس", "footer")}
            <label class="field" style="flex:1"><span class="sr-only">بريدك الإلكتروني</span><input type="email" name="email" placeholder="بريدك للنشرة" required/></label>
            <button class="btn btn-gold btn-sm" type="submit">اشترك</button>
          </form>
          <div class="form-success" role="status">تم الاشتراك، شكرًا لك.</div>
        </div>
      </div>
      <div class="footer-bottom">
        <span>© <span data-year>2026</span> فايف إس — جميع الحقوق محفوظة</span>
        <nav aria-label="روابط قانونية"><a href="{L('privacy/', depth)}">سياسة الخصوصية</a><a href="{L('terms/', depth)}">الشروط والأحكام</a></nav>
      </div>
    </div>
  </footer>
  <nav class="mobile-bar" aria-label="تواصل سريع">
    <a href="tel:{PHONE1_TEL}">{icon("phone", "")} اتصل</a>
    <a href="{WA}" target="_blank" rel="noopener">{WA_SVG} واتساب</a>
    <a class="quote" href="{L('contact/', depth)}#quote">{icon("doc", "")} عرض سعر</a>
  </nav>
  <a class="wa-float" href="{WA}" target="_blank" rel="noopener">{WA_SVG} تحدث إلى مهندس</a>
  <script src="{L('js/main.js', depth)}" defer></script>
</body>
</html>
'''

PAGES = []
def page(path, title, desc, active, body, crumbs=None, extra_ld=None, cls="", source=None, cta=True):
    depth = path.count("/")
    lds = list(extra_ld or [])
    if crumbs:
        lds.append(crumbs_ld(crumbs))
    out = head(title, desc, path, depth, lds, cls) + header(active, depth) + '  <main id="main">\n' + body(depth)
    if cta:
        out += cta_final(depth, source or path or "home")
    out += "  </main>\n" + footer(depth)
    fn = os.path.join(ROOT, path, "index.html")
    os.makedirs(os.path.dirname(fn), exist_ok=True)
    open(fn, "w", encoding="utf-8").write(out)
    PAGES.append(path)

def img(name, depth, alt, cls="", lazy=True, w=1280, h=720):
    c = f' class="{cls}"' if cls else ""
    lz = ' loading="lazy"' if lazy else ""
    return f'<img{c} src="{L("assets/img/" + name + ".webp", depth)}" alt="{E(alt)}" width="{w}" height="{h}"{lz} decoding="async"/>'

def prod_card(p, depth, cls="card challenge-card reveal"):
    return f'''<a class="{cls}" href="{L("solutions/" + p["slug"] + "/", depth)}" style="--accent:{p["accent"]}">
            {icon(p["icon"])}
            <span class="prod">{p["name"]}</span>
            <h3>{E(p["challenge"])}</h3>
            <p>{E(p["short"])}</p>
            <span class="link-arrow">اكتشف الحل</span>
          </a>'''

def sector_tile(s, depth):
    return f'''<a class="sector-tile reveal" href="{L("sectors/" + s["slug"] + "/", depth)}">
            {img(s["img"], depth, "تطبيق ميداني لتقنية 5S — " + s["name"])}
            <span class="ph-badge">صورة مؤقتة</span>
            <span class="label"><strong>{E(s["name"])}</strong><span>{E(s["challenge"])}</span></span>
          </a>'''

def project_card(pr, depth):
    sname = next(s["name"] for s in SECTORS if s["slug"] == pr["sector"])
    ph = '<span class="ph-badge">بيانات مؤقتة</span>' if pr.get("ph") else ""
    return f'''<article class="card media-card card--hover reveal" data-project data-sector="{pr["sector"]}" data-tech="{pr["tech"]}" data-country="{E(pr["country"])}">
            <div class="media">{img(pr["img"], depth, pr["name"])}{ph}</div>
            <div class="body">
              <span class="tag">{E(sname)} · {PBY[pr["tech"]]["name"]}</span>
              <h3>{E(pr["name"])}</h3>
              <p>{E(pr["desc"])}</p>
              <div class="mt-1"><span class="result-num">{E(pr["result"])}</span> <small>{E(pr["result_label"])}</small></div>
            </div>
          </article>'''

def particles_svg():
    import random
    random.seed(5)
    circles, bonds, pts = [], [], []
    for row in range(5):
        for col in range(9):
            pts.append((40 + col * 40 + (20 if row % 2 else 0), 40 + row * 34))
    for x, y in pts:
        dx = random.randint(-70, 70); dy = random.randint(-40, 40)
        circles.append(f'<circle cx="{x}" cy="{y}" r="11" style="--dx:{dx}px;--dy:{dy}px"/>')
    for i, (x, y) in enumerate(pts):
        if (i + 1) % 9 and i + 1 < len(pts):
            x2, y2 = pts[i + 1]
            bonds.append(f'<line class="bond" x1="{x}" y1="{y}" x2="{x2}" y2="{y2}"/>')
    return ('<svg class="particles" viewBox="0 0 420 210" role="img" aria-label="رسم توضيحي: جزيئات رمل متفرقة تتقارب وتتماسك بعد المعالجة">'
            + "".join(bonds) + "".join(circles) + "</svg>")

HOW_STEPS = [
  ("فحص التربة في مختبرنا", "نحلل عينة من تربة الموقع لتحديد المنتج ونسبة الخلط المناسبة."),
  ("خلط المادة بالماء", "تُخفف المادة بالماء في الموقع حسب النسبة المحددة."),
  ("الرش أو الدمج", "تُرش على السطح أو تُدمج مع التربة حسب التطبيق."),
  ("المعالجة والتسليم", "تجف الطبقة وتتماسك الجزيئات لتعطي سطحًا ثابتًا جاهزًا للاستخدام."),
]
def how_block(depth):
    steps = "".join(f'<li class="reveal"><strong>{E(a)}</strong><span>{E(b)}</span></li>' for a, b in HOW_STEPS)
    return f'''<div class="split">
          <ol class="steps stagger">{steps}</ol>
          <div class="particles-box reveal">{particles_svg()}<div class="particles-caption"><span>قبل: جزيئات متفرقة</span><span>بعد: جزيئات متماسكة</span></div></div>
        </div>'''

PROPS = ["آمنة 100% وغير سامة", "مقاومة للأشعة فوق البنفسجية", "غير قابلة للاشتعال (أساس مائي)", "لا تتفاعل مع المواد الأخرى",
         "عديمة اللون والرائحة", "صديقة للبيئة", "تكوين طبقة مقاومة للرياح", "مستقرة في الرطوبة والحرارة العالية والمنخفضة",
         "لا تتحلل ولا تتفكك عند تعرضها لأشعة الشمس", "إنتاج سعودي محلي", "سهولة النقل والتخزين", "توفير في التكاليف مقارنة بالحلول التقليدية"]

WHY = [
  ("flagsa", "إنتاج سعودي 100%", "تصنيع محلي يعني قربًا في التوريد وسرعة في الاستجابة وتكلفة أقل."),
  ("globe", "تقنية عالمية", "تقنية بوليمرات أكريليك مكيّفة لبيئتنا. (مصدر الترخيص أو الشراكة بانتظار التوضيح)"),
  ("sun", "خبرة في البيئة الصحراوية", "حرارة عالية، كثبان متحركة، وعواصف رملية — هذه بيئتنا اليومية."),
  ("flask", "مختبر لتحليل التربة", "نفحص تربة موقعك قبل التنفيذ لنختار المنتج والنسبة الصحيحة."),
  ("users", "شبكة وكلاء إقليمية", "وكلاء في دول الخليج والمنطقة العربية لخدمة مشاريعك أينما كانت."),
  ("leaf", "صديقة للبيئة", "أساس مائي، غير سامة، وتُرشّد استهلاك المياه مقارنة بالرش المستمر."),
]

# =================================================================== HOME
def home(depth):
    cards = "\n          ".join(prod_card(p, depth) for p in PRODUCTS)
    tiles = "\n          ".join(sector_tile(s, depth) for s in SECTORS)
    feats = "".join(f'<div class="feature reveal">{icon(i)}<div><h3>{E(t)}</h3><p>{E(d)}</p></div></div>' for i, t, d in WHY)
    logos = "".join(f'<div class="logo-ph ph-box">شعار جهة {n}<br/><small>بانتظار الشعار</small></div>' for n in range(1, 9))
    logos2 = logos.replace('class="logo-ph', 'aria-hidden="true" class="logo-ph')
    calc_opts = "".join(f'<option value="{p["key"]}">{E(p["challenge"])} ({p["name"]})</option>' for p in PRODUCTS)
    testi = "".join(f'''<div class="tslide" role="group" aria-roledescription="شريحة" aria-label="{n} من 3">
            <span class="ph-badge">شهادة تجريبية</span>
            <blockquote class="mt-1">«نص شهادة العميل يُضاف هنا بعد موافقة الجهة على النشر — جملتان عن التحدي والنتيجة.»</blockquote>
            <cite>اسم العميل · المنصب · الجهة</cite>
          </div>''' for n in range(1, 4))
    featured = "\n          ".join(project_card(p, depth) for p in PROJECTS)
    return f'''    <section class="hero" aria-labelledby="hero-title">
      <div class="hero-media" aria-hidden="true">
        <video class="hero-video is-active" id="heroVideo1" autoplay muted loop playsinline poster="assets/hero-poster.jpg" preload="auto">
          <source src="assets/hero-720.mp4" type="video/mp4" media="(max-width: 767px)"/>
          <source src="assets/hero.mp4" type="video/mp4"/>
        </video>
        <video class="hero-video" id="heroVideo2" muted loop playsinline preload="none">
          <source src="assets/hero-2-720.mp4" type="video/mp4" media="(max-width: 767px)"/>
          <source src="assets/hero-2.mp4" type="video/mp4"/>
        </video>
        <div class="hero-overlay"></div>
      </div>
      <div class="wrap hero-content">
        <div class="hero-copy reveal">
          <span class="kicker">تقنية عالمية. صناعة سعودية. نتائج تدوم.</span>
          <h1 id="hero-title">نُثبّت الرمال... لتنطلق التنمية</h1>
          <p class="sub">فايف إس شركة سعودية متخصصة في حلول ومواد تثبيت الرمال والتربة — من فحص التربة في مختبرنا إلى سطح ثابت يدوم لسنوات.</p>
          <div class="btn-row">
            <a class="btn btn-gold" href="solutions/">اكتشف حلولنا</a>
            <a class="btn btn-ghost-light" href="calculator/">احسب احتياجك</a>
          </div>
          <ul class="hero-points">
            <li>تثبيت الكثبان والرمال الزاحفة</li>
            <li>طرق ترابية بديلة للأسفلت</li>
            <li>مكافحة الغبار وترشيد المياه</li>
          </ul>
        </div>
      </div>
    </section>

    <section class="trust" aria-labelledby="trust-title">
      <div class="wrap">
        <p class="trust-title" id="trust-title">جهات تثق بأرضنا الصلبة <span class="ph-badge">شعارات تجريبية — بانتظار الشعارات وإذن العرض</span></p>
        <div class="marquee" tabindex="0" aria-label="شعارات الجهات"><div class="marquee-track">{logos}{logos2}</div></div>
      </div>
    </section>

    <section class="section">
      <div class="wrap split">
        <div class="reveal">
          <span class="eyebrow">من نحن</span>
          <h2>الرمال ليست قدرًا... بل مورد ننتظر استثماره</h2>
          <p class="lead">فايف إس شركة سعودية متخصصة في حلول ومواد تثبيت الرمال والتربة. نجمع تقنية عالمية مع تصنيع محلي، ونقدم منظومة متكاملة تبدأ بفحص التربة في مختبرنا وتنتهي بسطح ثابت يدوم لسنوات.</p>
          <p>نعمل لنكون شريكًا في تحقيق رؤية المملكة 2030. معًا نطوّر ونبني.</p>
          <a class="link-arrow" href="about/">قصتنا</a>
        </div>
        <div class="reveal rounded-media">{img("field-4", depth, "فريق فايف إس يرش مادة التثبيت على ممشى رملي")}</div>
      </div>
    </section>

    <section class="section section--sand dunes dunes--dark" aria-labelledby="challenge-title">
      <div class="wrap">
        <div class="section-head section-head--center reveal">
          <span class="eyebrow">اختر تحديك</span>
          <h2 id="challenge-title">ما المشكلة التي تواجهها في موقعك؟</h2>
          <p>اختر التحدي، ونقودك إلى التقنية المصممة له.</p>
        </div>
        <div class="grid grid-5 stagger">
          {cards}
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="how-title">
      <div class="wrap">
        <div class="section-head reveal">
          <span class="eyebrow">كيف تعمل التقنية</span>
          <h2 id="how-title">أربع خطوات من الرمال المتحركة إلى أساسٍ صلب</h2>
          <p>أكريليك بوليمر بأساس مائي يتغلغل بين جزيئات التربة ويربطها ببعضها.</p>
        </div>
        {how_block(depth)}
      </div>
    </section>

    <section class="section section--green dunes" aria-labelledby="stats-title">
      <div class="wrap">
        <div class="section-head section-head--center reveal">
          <span class="eyebrow">بالأرقام</span>
          <h2 id="stats-title">نتائج قابلة للقياس</h2>
        </div>
        <!-- TODO(client): «حتى 40%» و«حتى 340%» منشورة على الموقع الحالي لكنها تحتاج توثيقًا (دراسة حالة / تقرير مختبر CBR) قبل الإطلاق. -->
        <div class="stats stagger">
          <div class="stat reveal"><span class="pre">حتى</span><span class="num" data-count="40" data-suffix="%">40%</span><span class="label">توفير في التكلفة</span><span class="ph-badge">بانتظار التوثيق</span></div>
          <div class="stat reveal"><span class="pre">حتى</span><span class="num" data-count="340" data-suffix="%">340%</span><span class="label">زيادة في قيمة CBR</span><span class="ph-badge">بانتظار تقرير المختبر</span></div>
          <div class="stat reveal"><span class="pre">&nbsp;</span><span class="num" data-count="100" data-suffix="%">100%</span><span class="label">إنتاج سعودي</span></div>
          <div class="stat reveal"><span class="pre">&nbsp;</span><span class="num">—</span><span class="label">مشروع منفّذ في — دول</span><span class="ph-badge">يُستكمل من الشركة</span></div>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="sectors-title">
      <div class="wrap">
        <div class="section-head reveal">
          <span class="eyebrow">القطاعات</span>
          <h2 id="sectors-title">حلول لتسعة قطاعات حيوية</h2>
          <p>ابحث عن قطاعك لترى التحديات التي نحلها والتقنيات المناسبة.</p>
        </div>
        <div class="sectors-scroll stagger">
          {tiles}
        </div>
      </div>
    </section>

    <section class="section section--sand" aria-labelledby="ba-title">
      <div class="wrap">
        <div class="section-head section-head--center reveal">
          <span class="eyebrow">قبل / بعد</span>
          <h2 id="ba-title">اسحب لترى الفرق</h2>
        </div>
        <div class="ba reveal">
          {img("before-demo", depth, "قبل المعالجة: سطح رملي غير معالج")}
          {img("after-demo", depth, "بعد المعالجة: سطح رملي معالج بتقنية 5S", cls="ba-after")}
          <span class="ba-label ba-label--before">قبل</span><span class="ba-label ba-label--after">بعد</span>
          <span class="ba-line"></span><span class="ba-handle" aria-hidden="true">S</span>
          <input type="range" min="0" max="100" value="50" dir="ltr" aria-label="اسحب للمقارنة بين قبل وبعد المعالجة"/>
          <span class="ph-badge">صور توضيحية مؤقتة — بانتظار صور قبل/بعد حقيقية</span>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="projects-title">
      <div class="wrap">
        <div class="section-head reveal">
          <span class="eyebrow">المشاريع المميزة</span>
          <h2 id="projects-title">مشاريع نُفّذت بتقنيات 5S</h2>
        </div>
        <div class="grid grid-3 stagger">
          {featured}
        </div>
        <p class="mt-2"><a class="btn btn-outline" href="projects/">كل المشاريع</a></p>
      </div>
    </section>

    <section class="section section--sand" aria-labelledby="why-title">
      <div class="wrap">
        <div class="section-head reveal">
          <span class="eyebrow">لماذا 5S</span>
          <h2 id="why-title">ما يميزنا</h2>
        </div>
        <div class="grid grid-3 stagger">{feats}</div>
      </div>
    </section>

    <section class="section" aria-labelledby="calc-title">
      <div class="wrap split">
        <div class="reveal">
          <span class="eyebrow">حاسبة المواد</span>
          <h2 id="calc-title">احسب احتياجك من المواد</h2>
          <p class="lead">أدخل نوع التطبيق والمساحة لتحصل على كمية تقديرية بحاويات IBC، ثم اطلب عرضًا دقيقًا.</p>
        </div>
        <div class="calc reveal">
          <form data-calc class="calc-grid">
            <label class="field">نوع التطبيق<select name="type">{calc_opts}</select></label>
            <label class="field">المساحة (م²)<input type="number" name="area" min="1" step="1" value="1000" inputmode="numeric"/></label>
          </form>
          <div class="calc-result" aria-live="polite">
            <div class="big">—</div>
            <p class="small"><span class="ph-badge">تقديري — معاملات مؤقتة بانتظار الفريق الفني</span></p>
            <a class="btn btn-gold btn-sm" href="calculator/" data-full-link data-base="calculator/">افتح الحاسبة الكاملة</a>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--sand" aria-labelledby="t-title">
      <div class="wrap">
        <div class="section-head section-head--center reveal">
          <span class="eyebrow">آراء العملاء</span>
          <h2 id="t-title">ماذا يقول عملاؤنا</h2>
        </div>
        <div class="tslider reveal" aria-roledescription="عارض شرائح" aria-label="شهادات العملاء">
          {testi}
          <div class="tslider-nav">
            <button class="arrow prev" type="button" aria-label="الشهادة السابقة">→</button>
            <div class="dots"></div>
            <button class="arrow next" type="button" aria-label="الشهادة التالية">←</button>
          </div>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="ceo-title">
      <div class="wrap ceo">
        <div class="ceo-photo ph-box reveal">صورة الرئيس التنفيذي<br/><small>بانتظار الصورة</small></div>
        <div class="reveal">
          <span class="eyebrow">كلمة الرئيس التنفيذي</span>
          <h2 id="ceo-title">الرمال أساس للتنمية لا عائق أمامها</h2>
          <blockquote>منذ تأسيس فايف إس آمنّا بأن الرمال التي تملأ أرضنا يمكن أن تكون أساسًا للتنمية لا عائقًا أمامها. ومع الرؤية 2030 التزمنا بتقديم بدائل محلية تجمع الكفاءة والاستدامة وانخفاض التكلفة.</blockquote>
          <p class="sig">الرئيس التنفيذي — فايف إس <span class="ph-badge">الاسم بانتظار الاعتماد</span></p>
          <a class="link-arrow" href="about/#ceo">اقرأ الكلمة كاملة</a>
        </div>
      </div>
    </section>
'''

# =================================================================== ABOUT
def about(depth):
    goals = ["أن نحقق الريادة في تثبيت الرمال والتربة في الخليج العربي والشرق الأوسط.",
             "أن نطوّر تقنيات تثبيت التربة والكثبان الرملية باستمرار للوصول إلى أفضل نتيجة.",
             "أن نساهم مباشرة في تحقيق رؤية المملكة 2030 بحلول مبتكرة."]
    g = "".join(f'<div class="card reveal"><div class="goal-num">0{i}</div><p>{E(t)}</p></div>' for i, t in enumerate(goals, 1))
    vals = [("leaf", "بيئة نظيفة"), ("spark", "تنمية مسؤولة"), ("award", "جودة بلا تنازل"), ("coin", "ابتكار يوفّر")]
    v = "".join(f'<div class="card value reveal">{icon(i)}<h3>{t}</h3></div>' for i, t in vals)
    tl = [("2019", "تأسيس فايف إس كإحدى شركات سبأ للتجارة والمقاولات"), ("—", "محطة مهمة — بانتظار البيانات"),
          ("—", "محطة مهمة — بانتظار البيانات"), ("اليوم", "مشاريع في قطاعات متعددة ووكلاء في الخليج والمنطقة العربية")]
    t = "".join(f'<li class="reveal"><strong>{a}</strong><span>{E(b)}</span></li>' for a, b in tl)
    leaders = "".join('<div class="card reveal center"><div class="ceo-photo ph-box" style="width:120px;padding:8px">صورة</div><h3 class="mt-1">اسم القيادي</h3><p>المنصب <span class="ph-badge">بانتظار البيانات</span></p></div>' for _ in range(3))
    certs = "".join(f'<div class="dl reveal"><div><strong>شهادة / اعتماد {n}</strong><span>بانتظار اسم الجهة والشهادة</span></div><span class="ph-badge">مؤقت</span></div>' for n in range(1, 4))
    return banner("من الرمال نصنع الأساس", [("من نحن", "about/")], depth,
                  sub="شركة سعودية متخصصة في حلول ومواد تثبيت الرمال والتربة.") + f'''
    <section class="section">
      <div class="wrap split">
        <div class="reveal">
          <span class="eyebrow">قصتنا</span>
          <h2>كيف نحوّل الرمال من مشكلة إلى قيمة؟</h2>
          <p class="lead">بدأت فايف إس بسؤال بسيط: كيف نحوّل الرمال من مشكلة إلى قيمة؟ الرمال تغطي مساحات واسعة من المملكة، وتسبب أضرارًا للطرق والمنشآت وتكاليف صيانة متواصلة.</p>
          <p>فطوّرنا تقنية متخصصة في تثبيت الرمال، ووفّرناها بتصنيع محلي وتكلفة منافسة. واليوم ننفّذ مشاريع في قطاعات متعددة، ولنا وكلاء في دول الخليج والمنطقة العربية.</p>
        </div>
        <div class="reveal"><div class="rounded-media">{img("field-5", depth, "فريق فايف إس الميداني أثناء تطبيق المادة")}</div><p class="small mt-1"><span class="ph-badge">بانتظار صورة الفريق الميداني</span></p></div>
      </div>
    </section>

    <section class="section section--sand">
      <div class="wrap narrow reveal">
        <span class="eyebrow">نبذة عن الشركة</span>
        <h2>تثبيت التربة بطريقة أذكى وأقل تكلفة</h2>
        <p>فايف إس لحلول تثبيت الرمال والتربة شركة سعودية تأسست عام 2019، وهي إحدى شركات سبأ للتجارة والمقاولات، ومن أوائل الشركات في الخليج والشرق الأوسط في هذا المجال.</p>
        <p>نقدم تقنيات متطورة لتثبيت الرمال والتربة تساعد الشركات والجهات الحكومية والخاصة على إنجاز أعمالها الإنشائية ببدائل اقتصادية عالية الجودة وصديقة للبيئة، بإنتاج سعودي.</p>
      </div>
    </section>

    <section class="section" id="ceo">
      <div class="wrap ceo">
        <div class="ceo-photo ph-box reveal">صورة الرئيس التنفيذي<br/><small>بانتظار الصورة</small></div>
        <div class="reveal">
          <span class="eyebrow">كلمة الرئيس التنفيذي</span>
          <h2>رسالة القيادة</h2>
          <blockquote>منذ تأسيس فايف إس آمنّا بأن الرمال التي تملأ أرضنا يمكن أن تكون أساسًا للتنمية لا عائقًا أمامها. خلال مسيرتنا أثبتنا كفاءة منتجاتنا، ونلنا ثقة جهات حكومية وخاصة في قطاعات حيوية: الدفاع، والزراعة، والعمران، والطيران، وغيرها. ومع الرؤية 2030 التزمنا بتقديم بدائل محلية تجمع الكفاءة والاستدامة وانخفاض التكلفة. وما زلنا نعمل لنبقى الوجهة الأولى في تثبيت التربة في المملكة والمنطقة.</blockquote>
          <p class="sig">التوقيع — الرئيس التنفيذي <span class="ph-badge">الاسم والتوقيع بانتظار الاعتماد</span></p>
        </div>
      </div>
    </section>

    <section class="section section--sand">
      <div class="wrap">
        <div class="grid grid-2 stagger">
          <div class="card reveal">{icon("spark")}<h3>رؤيتنا</h3><p>الريادة في تثبيت الكثبان الرملية والتربة، وأن نكون رافدًا لتحقيق رؤية المملكة 2030.</p></div>
          <div class="card reveal">{icon("flag")}<h3>رسالتنا</h3><p>نبتكر حلولًا فعالة ومستدامة لتثبيت الرمال والتربة، تحقق أهداف عملائنا بتكلفة أقل وأثر بيئي أقل.</p></div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="section-head reveal"><span class="eyebrow">أهدافنا</span><h2>ثلاثة أهداف واضحة</h2></div>
        <div class="grid grid-3 stagger">{g}</div>
        <div class="section-head reveal mt-3"><span class="eyebrow">قيمنا</span><h2>أساس طريقة عملنا</h2></div>
        <div class="grid grid-4 stagger">{v}</div>
      </div>
    </section>

    <section class="section section--sand">
      <div class="wrap">
        <div class="section-head reveal"><span class="eyebrow">مسيرتنا</span><h2>أهم المحطات</h2><p><span class="ph-badge">المسيرة الزمنية تُستكمل من الشركة</span></p></div>
        <ol class="timeline timeline--h stagger" style="--n:4">{t}</ol>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="section-head reveal"><span class="eyebrow">فريقنا</span><h2>خبرة عملية وعلمية</h2><p>نجمع بين الخبرة العملية والعلمية، ونعمل بروح الفريق لتنفيذ المشاريع على الوجه الأكمل. <span class="ph-badge">نص الفريق وبطاقات القيادات بانتظار البيانات</span></p></div>
        <div class="grid grid-3 stagger">{leaders}</div>
      </div>
    </section>

    <section class="section section--sand">
      <div class="wrap">
        <div class="section-head reveal"><span class="eyebrow">الشهادات والاعتمادات</span><h2>اعتمادات وشهادات</h2></div>
        <div class="grid grid-3 stagger">{certs}</div>
        <p class="mt-2"><span class="btn btn-outline is-disabled" aria-disabled="true">{icon("download", "")} تنزيل ملف الشركة PDF — قريبًا</span></p>
      </div>
    </section>
'''

# =================================================================== SOLUTIONS (general)
def solutions(depth):
    cards = "\n          ".join(prod_card(p, depth) for p in PRODUCTS)
    props = "".join(f"<li>{E(x)}</li>" for x in PROPS)
    head_cells = "".join(f'<th scope="col">{p["name"]}</th>' for p in PRODUCTS)
    rows = ""
    for r in RESULT_ROWS:
        cells = ""
        for p in PRODUCTS:
            c = CONFIRMED.get((p["key"], r))
            cells += '<td class="no">✗ لا</td>' if c is False else ('<td class="yes">✓</td>' if c else '<td class="pending">بانتظار التأكيد</td>')
        rows += f'<tr><th scope="row">{E(r)}</th>{cells}</tr>'
    rows += '<tr><th scope="row">فترة الصيانة / إعادة التطبيق</th>' + "".join(f'<td class="pending">{E(p["maint"])}</td>' for p in PRODUCTS) + "</tr>"
    return banner("تقنية 5S", [("الحلول", "solutions/")], depth,
                  sub="مواد تثبيت الرمال والتربة: أكريليك بوليمر بأساس مائي يربط جزيئات التربة ويحوّلها إلى سطح ثابت.") + f'''
    <section class="section">
      <div class="wrap">
        <div class="section-head reveal"><span class="eyebrow">كيف تعمل</span><h2>من الرمال المتحركة إلى أساسٍ صلب</h2>
          <p>تتغلغل المادة بين جزيئات التربة والرمال فتربطها ببعضها، وتعطي سطحًا ثابتًا عديم اللون والرائحة.</p></div>
        {how_block(depth)}
      </div>
    </section>

    <section class="section section--sand dunes dunes--dark">
      <div class="wrap">
        <div class="section-head reveal"><span class="eyebrow">خط المنتجات</span><h2>خمس تقنيات لخمسة تحديات</h2></div>
        <div class="grid grid-5 stagger">
          {cards}
        </div>
        <p class="mt-2 reveal">تحتاج تركيبة خاصة لموقعك؟ <a href="{L('contact/', depth)}?product=custom#quote">اطلب حلًا مخصصًا</a> بالتعاون مع فريقنا الفني.</p>
      </div>
    </section>

    <section class="section">
      <div class="wrap split">
        <div class="reveal">
          <span class="eyebrow">الخصائص العامة</span>
          <h2>خصائص مشتركة في كل منتجات 5S</h2>
          <ul class="check-list cols mt-1">{props}</ul>
        </div>
        <div class="reveal video-embed">
          <iframe src="https://www.youtube-nocookie.com/embed/QL_NMDvD_zw" title="فايف إس — تطبيق ميداني لمثبت الرمال والتربة" loading="lazy" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </div>
      </div>
    </section>

    <section class="section section--sand">
      <div class="wrap">
        <div class="grid grid-2 stagger">
          <div class="card reveal">{icon("shield")}<h3>السلامة</h3>
            <ul class="check-list"><li>آمنة وغير سامة للإنسان والحيوان</li><li>مقاومة للأشعة فوق البنفسجية</li><li>غير قابلة للاشتعال — أساس مائي</li></ul>
            <p class="mt-1"><a href="{L('technical-data/', depth)}">ملفات السلامة (SDS)</a></p></div>
          <div class="card reveal">{icon("package")}<h3>الشحن والتخزين</h3>
            <ul class="check-list"><li>التوريد في حاويات IBC</li><li>الشحن بالكميات الكبيرة في حاويات ISO</li><li>سهولة النقل والتخزين</li></ul>
            <p class="ph-note">السعات وشروط التخزين ومدة الصلاحية بانتظار البيانات الفنية من فايف إس.</p></div>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="matrix-title">
      <div class="wrap">
        <div class="section-head reveal"><span class="eyebrow">مصفوفة المقارنة</span><h2 id="matrix-title">أي منتج يناسب مشروعك؟</h2>
          <p>مقارنة بين المنتجات الخمسة حسب النتيجة المتوقعة.</p></div>
        <p class="ph-note reveal">الثابت حاليًا: 5S BERM لا يتحمل مرور المركبات. بقية الجدول وفترات الصيانة بانتظار تأكيد الفريق الفني لفايف إس.</p>
        <div class="table-wrap reveal"><table class="tbl"><caption class="sr-only">مصفوفة مقارنة منتجات 5S</caption>
          <thead><tr><th scope="col">النتيجة</th>{head_cells}</tr></thead><tbody>{rows}</tbody></table></div>
      </div>
    </section>
'''

# =================================================================== PRODUCT
PROD_FAQ_EXTRA = {
  "berm": [("هل يتحمل 5S BERM مرور المركبات؟", "لا. 5S BERM مخصص لتثبيت الرمال والكثبان والتحكم في زحفها، ولا يتحمل مرور المركبات. للطرق استخدم 5S ROAD.")],
  "road": [("هل يتحمل 5S ROAD الشاحنات الثقيلة؟", "يُستخدم في مواقف السيارات التي تتحمل مرور المركبات والشاحنات الثقيلة، ويُحدد العمق حسب اشتراطات المشروع وفحص التربة.")],
  "slope": [("هل يناسب 5S SLOPE جوانب السدود؟", "نعم، من استخداماته إنشاء السدود وتخزين المياه وتنظيم تدفقها وحماية جوانبها من التآكل.")],
  "dust": [("هل يغني 5S DUST عن الرش اليومي بالمياه؟", "صُمم بديلًا عن الرش المستمر بالمياه؛ تطبيق واحد يعطي فعالية طويلة الأمد، مع فحص دوري وإعادة تطبيق عند الحاجة.")],
  "walk": [("هل يغيّر 5S WALK مظهر الموقع؟", "المادة عديمة اللون، فتبقى الممرات بمظهر التربة الطبيعي — ولهذا استُخدمت في البلدة القديمة بالعلا.")],
}
def product(p):
    faqs = PROD_FAQ_EXTRA[p["key"]] + GENERAL_FAQ[2:4]
    def body(depth):
        uses = "".join(f'<div class="card reveal">{icon(i)}<p>{E(t)}</p></div>' for i, t in p["uses"])
        feats = "".join(f"<li>{E(f)}</li>" for f in p["features"])
        res = ""
        for r in RESULT_ROWS:
            c = CONFIRMED.get((p["key"], r))
            res += f'<tr><th scope="row">{E(r)}</th>' + ('<td class="no">✗ لا</td>' if c is False else '<td class="pending">بانتظار التأكيد</td>') + "</tr>"
        trad_head = " / ".join(p["traditional"])
        cmp_rows = "".join(f'<tr><th scope="row">{E(a)}</th><td class="hl">{E(b)}</td><td>{E(c)}</td></tr>' for a, b, c in p["compare"])
        projects = [pr for pr in PROJECTS if pr["tech"] == p["key"] and not pr.get("ph")]
        prj = ("\n".join(project_card(pr, depth) for pr in projects) if projects else
               '<div class="card ph-box reveal"><h3>مشاريع هذا المنتج</h3><p>بانتظار قائمة المشاريع المعتمدة للنشر من فايف إس.</p></div>')
        fq = "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in faqs)
        strength = ""
        if p["strength"]:
            strength = f'''
        <div class="card mt-3 reveal">
          <span class="eyebrow">القوة وتقليل النفاذية</span>
          <h3>سطح أقوى ونفاذية أقل للمياه</h3>
          <p>يزيد {p["name"]} قوة الترابط بين جزيئات التربة ويقلل نفاذية السطح للمياه، فيقاوم التآكل ويحافظ على تماسكه.</p>
          <p class="ph-note">قيم المقاومة (CBR / مقاومة الضغط) ونسبة تقليل النفاذية بانتظار تقارير الاختبار المعتمدة.</p>
        </div>'''
        berm_note = " — الثابت: لا يتحمل مرور المركبات" if p["key"] == "berm" else ""
        return banner(f'<span class="prod-name">{p["name"]}</span>', [("الحلول", "solutions/"), (p["name"], f"solutions/{p['slug']}/")], depth,
                      sub=E(p["value"]), tag=p["replaces"]) + f'''
    <section class="section">
      <div class="wrap prod-hero">
        <div class="reveal">
          <span class="eyebrow">نبذة</span>
          <h2>{E(p["value"])}</h2>
          <p class="lead">{E(p["intro"])}</p>
          <div class="btn-row mt-1"><a class="btn btn-gold" href="{L('contact/', depth)}?product={p["key"]}#quote">اطلب عرض سعر</a><a class="btn btn-outline" href="{L('calculator/', depth)}?type={p["key"]}">احسب الكمية</a></div>
        </div>
        <div class="media reveal">{img(p["img"], depth, "تطبيق ميداني لمنتج " + p["name"], lazy=False)}<span class="ph-badge">صورة مؤقتة من مشروع العلا</span></div>
      </div>
    </section>

    <section class="section section--sand">
      <div class="wrap">
        <div class="section-head reveal"><span class="eyebrow">الاستخدامات</span><h2>أين يُستخدم {p["name"]}؟</h2></div>
        <div class="grid grid-3 stagger">{uses}</div>
        <h3 class="mt-3 reveal">مزايا خاصة بالمنتج</h3>
        <ul class="check-list cols reveal">{feats}</ul>
        <p class="mt-1 reveal">الخصائص العامة المشتركة في <a href="{L('solutions/', depth)}">صفحة تقنية 5S</a>.</p>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="section-head reveal"><span class="eyebrow">كيف يعمل</span><h2>أربع خطوات للتطبيق</h2></div>
        {how_block(depth)}
      </div>
    </section>

    <section class="section section--sand">
      <div class="wrap split split--top">
        <div class="reveal">
          <span class="eyebrow">النتائج المتوقعة</span>
          <h2>ماذا تتوقع من {p["name"]}؟</h2>
          <div class="table-wrap"><table class="tbl tbl--fit"><thead><tr><th scope="col">النتيجة</th><th scope="col">{p["name"]}</th></tr></thead><tbody>{res}</tbody></table></div>
          <p class="ph-note">جدول ✓/✗ بانتظار تأكيد الفريق الفني{berm_note}.</p>
        </div>
        <div class="reveal">
          <span class="eyebrow">الصيانة</span>
          <h2>خط زمني للفحص</h2>
          <ol class="timeline mt-1">
            <li><strong>اليوم 0</strong><span>التطبيق الأول بعد فحص التربة</span></li>
            <li><strong>فحص دوري</strong><span>زيارة فحص للسطح — الفترة بانتظار التأكيد</span></li>
            <li><strong>{E(p["maint"])}</strong><span>إعادة التطبيق المتوقعة</span></li>
          </ol>
          <p class="ph-note">فترات الصيانة متضاربة في المحتوى الحالي وتحتاج تأكيدًا فنيًا.</p>
        </div>
      </div>
      <div class="wrap">{strength}</div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="section-head reveal"><span class="eyebrow">المقارنة</span><h2>{p["name"]} مقابل الحلول التقليدية</h2></div>
        <div class="table-wrap reveal"><table class="tbl"><thead><tr><th scope="col">المعيار</th><th scope="col">{p["name"]}</th><th scope="col">{E(trad_head)}</th></tr></thead><tbody>{cmp_rows}</tbody></table></div>
        <p class="ph-note reveal">قيم المقارنة مبدئية ووصفية، وتحتاج أرقامًا معتمدة من الفريق الفني قبل الإطلاق.</p>
      </div>
    </section>

    <section class="section section--sand">
      <div class="wrap">
        <div class="section-head reveal"><span class="eyebrow">المشاريع</span><h2>مشاريع استخدمت {p["name"]}</h2></div>
        <div class="grid grid-3 stagger">{prj}</div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="grid grid-2 split--top">
          <div class="reveal">
            <span class="eyebrow">البيانات الفنية</span><h2>تنزيل الملفات</h2>
            <div class="grid">
              <div class="dl"><div><strong>{p["name"]} — TDS</strong><span>البيانات الفنية</span></div><span class="btn btn-sm btn-outline is-disabled" aria-disabled="true">قريبًا</span></div>
              <div class="dl"><div><strong>{p["name"]} — SDS</strong><span>صحيفة بيانات السلامة</span></div><span class="btn btn-sm btn-outline is-disabled" aria-disabled="true">قريبًا</span></div>
            </div>
            <p class="ph-note">ملفات PDF بانتظار فايف إس. <a href="{L('technical-data/', depth)}">مكتبة البيانات الفنية</a></p>
          </div>
          <div class="reveal">
            <span class="eyebrow">الأسئلة الشائعة</span><h2>أسئلة عن {p["name"]}</h2>
            <div class="faq">{fq}</div>
          </div>
        </div>
      </div>
    </section>
'''
    ld = [faq_ld(faqs),
          {"@context": "https://schema.org", "@type": "Product", "name": p["name"], "description": p["intro"],
           "brand": {"@type": "Brand", "name": "5S"}, "manufacturer": {"@type": "Organization", "name": "فايف إس"}}]
    page(f"solutions/{p['slug']}/", p["seo_title"], p["seo_desc"], "solutions", body,
         crumbs=[("الحلول", "solutions/"), (p["name"], f"solutions/{p['slug']}/")], extra_ld=ld, source=p["name"])

# =================================================================== SECTORS
def sectors_index(depth):
    tiles = "\n          ".join(sector_tile(s, depth) for s in SECTORS)
    return banner("القطاعات", [("القطاعات", "sectors/")], depth,
                  sub="ادخل من حاجتك: اختر قطاعك لترى التحديات التي نحلها والتقنيات المناسبة.") + f'''
    <section class="section">
      <div class="wrap">
        <div class="sectors-scroll stagger">
          {tiles}
        </div>
      </div>
    </section>
'''

def sector(s):
    def body(depth):
        sol = "".join(f"<li>{E(x)}</li>" for x in s["solutions"])
        ben = "".join(f"<li>{E(x)}</li>" for x in s["benefits"])
        prods = "\n".join(prod_card(PBY[k], depth) for k in s["products"])
        if s["project"]:
            pr = PRJ[s["project"]]
            case = f'''<div class="split">
          <div class="reveal rounded-media">{img(pr["img"], depth, pr["name"])}</div>
          <div class="reveal">
            <span class="tag">{PBY[pr["tech"]]["name"]}</span>
            <h3>{E(pr["name"])}</h3>
            <p><strong>التحدي:</strong> <span class="ph-badge">نص التحدي بانتظار الشركة</span></p>
            <p><strong>الحل:</strong> {E(pr["desc"])}</p>
            <p><strong>النتيجة:</strong> <span class="result-num">{E(pr["result"])}</span> {E(pr["result_label"])} — {E("، ".join(pr["outcomes"]))}</p>
            <p class="small">الموقع: {E(pr["place"])} · العميل: {E(pr["client"])}</p>
          </div></div>'''
        else:
            case = '<div class="card ph-box reveal"><h3>دراسة حالة من القطاع</h3><p>بانتظار مشروع معتمد للنشر: التحدي ← الحل ← النتيجة بالأرقام ← شهادة العميل.</p></div>'
        review = ('<p class="ph-note">صياغة عامة دون تفاصيل حساسة — تُعتمد من الإدارة قبل النشر.</p>'
                  '<!-- TODO(client): defense page wording requires management approval before launch. -->') if s.get("review") else ""
        return banner(E(s["name"]), [("القطاعات", "sectors/"), (s["name"], f"sectors/{s['slug']}/")], depth, sub=E(s["challenge"])) + f'''
    <section class="section">
      <div class="wrap prod-hero">
        <div class="reveal">
          <span class="eyebrow">التحدي في هذا القطاع</span>
          <h2>{E(s["challenge"])}</h2>
          <p class="lead">{E(s["intro"])}</p>{review}
        </div>
        <div class="media reveal">{img(s["img"], depth, "تطبيق ميداني لتقنية 5S — " + s["name"], lazy=False)}<span class="ph-badge">صورة مؤقتة — بانتظار صورة من القطاع</span></div>
      </div>
    </section>

    <section class="section section--sand">
      <div class="wrap">
        <div class="grid grid-2 split--top">
          <div class="reveal"><span class="eyebrow">حلولنا</span><h2>ماذا نقدم للقطاع؟</h2><ul class="check-list">{sol}</ul></div>
          <div class="reveal"><span class="eyebrow">المزايا والنتائج المتوقعة</span><h2>النتيجة</h2><ul class="check-list">{ben}</ul></div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="section-head reveal"><span class="eyebrow">التقنيات المناسبة</span><h2>منتجات 5S لهذا القطاع</h2></div>
        <div class="grid grid-3 stagger">{prods}</div>
      </div>
    </section>

    <section class="section section--sand">
      <div class="wrap">
        <div class="section-head reveal"><span class="eyebrow">دراسة حالة</span><h2>من الميدان</h2></div>
        {case}
      </div>
    </section>
'''
    title = f"تثبيت التربة لقطاع {s['name']} | فايف إس"
    desc = f"حلول فايف إس لتثبيت الرمال والتربة في قطاع {s['name']}. {s['challenge']}"
    if len(desc) > 155:
        desc = desc[:150] + "…"
    page(f"sectors/{s['slug']}/", title, desc, "sectors", body,
         crumbs=[("القطاعات", "sectors/"), (s["name"], f"sectors/{s['slug']}/")], source="sector:" + s["slug"])

# =================================================================== PROJECTS
def projects(depth):
    cards = "\n          ".join(project_card(p, depth) for p in PROJECTS)
    so = "".join(f'<option value="{s["slug"]}">{E(s["name"])}</option>' for s in SECTORS)
    to = "".join(f'<option value="{p["key"]}">{p["name"]}</option>' for p in PRODUCTS)
    return banner("المشاريع", [("المشاريع", "projects/")], depth,
                  sub="كل مشروع: التحدي ← الحل ← النتيجة بالأرقام.") + f'''
    <section class="section">
      <div class="wrap">
        <form class="filters reveal" id="project-filters" aria-label="فلترة المشاريع">
          <label class="field">القطاع<select name="sector"><option value="">كل القطاعات</option>{so}</select></label>
          <label class="field">التقنية<select name="tech"><option value="">كل التقنيات</option>{to}</select></label>
          <label class="field">الدولة<select name="country"><option value="">كل الدول</option><option value="السعودية">السعودية</option></select></label>
          <button class="btn btn-outline" type="reset">إعادة الضبط</button>
        </form>
        <div class="grid grid-3 stagger" id="projects-grid">
          {cards}
        </div>
        <p class="empty-state" id="projects-empty">لا توجد مشاريع مطابقة لهذه الفلاتر حاليًا.</p>
        <p class="ph-note mt-2">المشروعان الأولان منشوران على الموقع الحالي 5s-tech.org. نحتاج من فايف إس قائمة المشاريع لكل منها: التحدي، الحل، النتيجة، الصور، وإذن النشر — لبناء صفحة لكل مشروع.</p>
      </div>
    </section>
'''

# =================================================================== TECHNICAL DATA
def technical(depth):
    docs = []
    for p in PRODUCTS:
        docs += [(p["name"], "TDS", "البيانات الفنية", "عربي / English"), (p["name"], "SDS", "صحيفة بيانات السلامة", "عربي / English")]
    docs += [("5S ROAD", "test", "تقرير اختبار CBR", "English"), ("تقنية 5S", "cert", "شهادة / اعتماد", "—"), ("فايف إس", "profile", "ملف الشركة", "عربي")]
    tlabel = {"TDS": "TDS", "SDS": "SDS", "test": "تقرير اختبار", "cert": "شهادة", "profile": "ملف الشركة"}
    rows = ""
    for name, t, title, lang in docs:
        gated = ' <span class="small">(يُطلب البريد قبل التنزيل)</span>' if t == "test" else ""
        rows += f'<tr data-type="{t}"><td><span class="prod-name">{E(name)}</span></td><td>{E(title)}{gated}</td><td>{tlabel[t]}</td><td>{E(lang)}</td><td><span class="btn btn-sm btn-outline is-disabled" aria-disabled="true">{icon("download", "")} قريبًا</span></td></tr>'
    topts = "".join(f'<option value="{k}">{v}</option>' for k, v in tlabel.items())
    return banner("البيانات الفنية", [("البيانات الفنية", "technical-data/")], depth,
                  sub="ملفات البيانات الفنية (TDS) وصحائف السلامة (SDS) وتقارير الاختبار والشهادات.") + f'''
    <section class="section">
      <div class="wrap">
        <div class="filters filters--2 reveal">
          <label class="field">ابحث في المستندات<input type="search" id="td-search" placeholder="مثال: ROAD أو SDS"/></label>
          <label class="field">نوع المستند<select id="td-type"><option value="">كل الأنواع</option>{topts}</select></label>
        </div>
        <div class="table-wrap reveal"><table class="tbl" id="td-table"><caption class="sr-only">مكتبة البيانات الفنية</caption>
          <thead><tr><th scope="col">المنتج</th><th scope="col">المستند</th><th scope="col">النوع</th><th scope="col">اللغة</th><th scope="col">تنزيل</th></tr></thead><tbody>{rows}</tbody></table></div>
        <p class="empty-state" id="td-empty">لا توجد مستندات مطابقة.</p>
        <p class="ph-note">كل الملفات بانتظار فايف إس (TDS / SDS / تقارير الاختبار / الشهادات / ملف الشركة). ملفات السلامة تبقى مفتوحة، والتقارير التفصيلية يُقترح طلب البريد قبل تنزيلها.</p>
      </div>
    </section>
'''

# =================================================================== PARTNERS
def partners(depth):
    cards = ""
    for country, name, desc in AGENTS:
        wa = WA + "?text=" + quote(f"مرحبًا، أرغب في التواصل مع وكيل فايف إس في {country}")
        d = f"<p>{E(desc)}</p>" if desc else ""
        cards += f'''<article class="card agent reveal">
            <span class="country">{E(country)}</span>
            <h3>{E(name)}</h3>{d}
            <dl><dt>المدينة</dt><dd>— <span class="ph-badge">بانتظار البيانات</span></dd><dt>الهاتف</dt><dd>—</dd><dt>البريد</dt><dd>—</dd></dl>
            <a class="btn btn-sm wa-btn" href="{wa}" target="_blank" rel="noopener">{WA_SVG} تواصل عبر واتساب</a>
          </article>'''
    return banner("الشركاء والوكلاء", [("الشركاء والوكلاء", "partners/")], depth,
                  sub="شبكة وكلاء في دول الخليج والمنطقة العربية.") + f'''
    <section class="section">
      <div class="wrap">
        <p class="ph-note reveal">الخريطة التفاعلية وبيانات كل وكيل (المدينة، الهاتف، البريد) بانتظار فايف إس. أزرار واتساب حاليًا تصل إلى الرقم الموحد لفايف إس مع ذكر الدولة.</p>
        <div class="grid grid-3 stagger">{cards}</div>
      </div>
    </section>

    <section class="section section--sand" id="join">
      <div class="wrap narrow">
        <div class="reveal"><span class="eyebrow">انضم كشريك</span><h2>هل ترغب بتمثيل فايف إس في بلدك؟</h2><p>أرسل بياناتك وسيتواصل معك فريق الشراكات.</p></div>
        <form class="form form-2 reveal" action="{FORM_ACTION}" method="POST" data-validate>
          {hidden("طلب انضمام كشريك — فايف إس", "partners")}
          <label class="field">الاسم الكامل<input type="text" name="name" autocomplete="name" required/></label>
          <label class="field">الشركة<input type="text" name="company" required/></label>
          <label class="field">الدولة<input type="text" name="country" required/></label>
          <label class="field">البريد الإلكتروني<input type="email" name="email" autocomplete="email" required/></label>
          <label class="field full">رسالة قصيرة<textarea name="message" rows="4" placeholder="عرّفنا بنشاطك والقطاعات التي تغطيها"></textarea></label>
          <div class="full"><button class="btn btn-gold" type="submit">إرسال الطلب</button></div>
        </form>
        <div class="form-success" role="status">شكرًا لك! وصلنا طلبك وسيتواصل معك فريق الشراكات.</div>
      </div>
    </section>
'''

# =================================================================== CALCULATOR
def calculator(depth):
    opts = "".join(f'<option value="{p["key"]}">{E(p["challenge"])} ({p["name"]})</option>' for p in PRODUCTS)
    return banner("حاسبة المواد", [("حاسبة المواد", "calculator/")], depth,
                  sub="احسب الكمية التقديرية بحاويات IBC، ثم اطلب عرضًا دقيقًا من فريقنا.") + f'''
    <section class="section">
      <div class="wrap narrow">
        <div class="calc reveal">
          <form data-calc class="calc-grid">
            <label class="field">نوع التطبيق<select name="type">{opts}</select></label>
            <label class="field">المساحة (م²)<input type="number" name="area" min="1" step="1" value="1000" inputmode="numeric" required/></label>
            <label class="field">عمق المعالجة (سم) — للطرق<input type="number" name="depth" min="1" max="50" step="1" value="10" inputmode="numeric"/></label>
            <label class="field">الموقع (المدينة / المنطقة)<input type="text" name="location" placeholder="مثال: الدمام"/></label>
          </form>
          <div class="calc-result" aria-live="polite">
            <p class="small mt-0">الكمية التقديرية</p>
            <div class="big">—</div>
            <p class="ph-note">تنبيه: النتيجة تقديرية فقط. معاملات الحساب (معدل الاستهلاك لكل م²) مؤقتة ويجب أن يزودها الفريق الفني لفايف إس قبل الإطلاق. الكمية والسعر النهائيان يُحددان بعد فحص التربة.</p>
            <a class="btn btn-gold" href="{L('contact/', depth)}#quote" data-quote-link data-base="{L('contact/', depth)}">أرسل لي عرضًا دقيقًا</a>
          </div>
        </div>
      </div>
    </section>
'''

# =================================================================== CONTACT
def contact(depth):
    popts = "".join(f'<option value="{p["key"]}">{p["name"]}</option>' for p in PRODUCTS) + '<option value="custom">حل مخصص / غير متأكد</option>'
    fq = "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in GENERAL_FAQ)
    return banner("لنبدأ مشروعك", [("تواصل معنا", "contact/")], depth,
                  sub="شكرًا لاهتمامك بفايف إس. أخبرنا عن مشروعك وسيتواصل معك مهندس من فريقنا.") + f'''
    <section class="section" id="quote">
      <div class="wrap split split--top">
        <div class="reveal">
          <h2>طلب عرض سعر</h2>
          <form class="form form-2" id="quote-form" action="{FORM_ACTION}" method="POST" enctype="multipart/form-data" data-validate>
            {hidden("طلب عرض سعر — فايف إس", "contact")}
            <label class="field">الاسم<input type="text" name="name" autocomplete="name" required/></label>
            <label class="field">الجهة / الشركة<input type="text" name="company" autocomplete="organization"/></label>
            {phone_field()}
            <label class="field">البريد الإلكتروني<input type="email" name="email" autocomplete="email" required/></label>
            {sector_select()}
            <label class="field">التقنية المطلوبة<select name="product"><option value="">— اختر —</option>{popts}</select></label>
            <label class="field">المساحة التقريبية (م²)<input type="number" name="area" min="1" inputmode="numeric"/></label>
            <label class="field">الموقع<input type="text" name="location" placeholder="المدينة / المنطقة"/></label>
            <label class="field full">الرسالة<textarea name="message" rows="5" placeholder="صف مشروعك باختصار: نوع التربة، الاستخدام، المدة المتوقعة"></textarea></label>
            <label class="field full">إرفاق ملف (اختياري، حتى 5 ميجابايت)<input type="file" name="attachment" accept=".pdf,.jpg,.jpeg,.png,.dwg,.doc,.docx"/></label>
            <div class="full"><button class="btn btn-gold" type="submit">إرسال الطلب</button></div>
          </form>
          <div class="form-success" role="status">شكرًا لك! وصلنا طلبك، وسيتواصل معك فريقنا خلال يوم عمل. <span class="ph-badge">مدة الرد بانتظار اعتماد الإدارة</span></div>
        </div>
        <div class="reveal">
          <h2>بيانات التواصل</h2>
          <ul class="contact-list">
            <li>{icon("phone")}<div><strong>الهاتف</strong><br/><a href="tel:{PHONE1_TEL}">{PHONE1}</a><br/><a href="tel:{PHONE2_TEL}">{PHONE2}</a></div></li>
            <li>{icon("mail")}<div><strong>البريد</strong><br/><a href="mailto:{EMAIL}">{EMAIL}</a></div></li>
            <li>{icon("pin")}<div><strong>العنوان</strong><br/>برج بوابة الخبر، الطابق 21، شارع الملك فهد، الخبر، المنطقة الشرقية، المملكة العربية السعودية</div></li>
          </ul>
          <a class="btn wa-btn mt-1" href="{WA}" target="_blank" rel="noopener">{WA_SVG} تحدث إلى مهندس عبر واتساب</a>
          <iframe class="map mt-2" title="موقع فايف إس على خريطة Google" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q={quote('برج بوابة الخبر، الخبر')}&amp;output=embed"></iframe>
        </div>
      </div>
    </section>

    <section class="section section--sand">
      <div class="wrap narrow">
        <div class="section-head reveal"><span class="eyebrow">الأسئلة الشائعة</span><h2>إجابات مختصرة</h2></div>
        <div class="faq reveal">{fq}</div>
      </div>
    </section>
'''

def legal(kind):
    t = "سياسة الخصوصية" if kind == "privacy" else "الشروط والأحكام"
    extra = " ويتوافق مع نظام حماية البيانات الشخصية السعودي (PDPL)" if kind == "privacy" else ""
    def body(depth):
        return banner(t, [(t, f"{kind}/")], depth) + f'''
    <section class="section"><div class="wrap narrow prose">
      <p class="ph-note">هذه الصفحة قيد الإعداد. النص النهائي يجب أن يُعتمد من فايف إس{extra}.</p>
      <p>للاستفسار: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </div></section>
'''
    page(f"{kind}/", f"{t} | فايف إس", f"{t} لموقع فايف إس لحلول تثبيت الرمال والتربة.", "", body, crumbs=[(t, f"{kind}/")], cta=False)

# =================================================================== REDIRECTS for old URLs
REDIRECTS = {"about.html": "about/", "solutions.html": "solutions/", "sectors.html": "sectors/",
             "projects.html": "projects/", "partners.html": "partners/", "contact.html": "contact/"}
HASHMAP = {"berm": "solutions/5s-berm/", "road": "solutions/5s-road/", "dust": "solutions/5s-dust/",
           "walk": "solutions/5s-walk/", "slope": "solutions/5s-slope/", "custom": "contact/?product=custom#quote",
           "quote": "contact/#quote", "join": "partners/#join"}
def redirects():
    js = json.dumps(HASHMAP)
    for old, new in REDIRECTS.items():
        open(os.path.join(ROOT, old), "w", encoding="utf-8").write(f'''<!DOCTYPE html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8"/><title>تم نقل الصفحة | فايف إس</title>
<meta name="robots" content="noindex"/><link rel="canonical" href="{SITE}{new}"/>
<script>(function(){{var m={js},h=location.hash.slice(1);location.replace(m[h]||"{new}"+(h?"#"+h:""));}})();</script>
<meta http-equiv="refresh" content="0; url={new}"/>
</head><body><p style="font-family:sans-serif;text-align:center;padding:40px">تم نقل هذه الصفحة إلى <a href="{new}">الرابط الجديد</a>.</p></body></html>
''')

def sitemap():
    urls = "".join(f"<url><loc>{SITE}{p}</loc></url>" for p in PAGES)
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n")

ORG_LD = {"@context": "https://schema.org", "@type": "Organization", "name": "فايف إس — 5S", "alternateName": "5S Sand & Soil Stabilization Smart Solutions",
          "url": SITE, "logo": SITE + "assets/logo.png", "email": EMAIL, "telephone": PHONE1_TEL,
          "address": {"@type": "PostalAddress", "streetAddress": "برج بوابة الخبر، الطابق 21، شارع الملك فهد", "addressLocality": "الخبر", "addressCountry": "SA"},
          "sameAs": ["https://x.com/5sSolution", "https://www.instagram.com/5s_techo/"]}

if __name__ == "__main__":
    page("", "فايف إس | تثبيت الرمال والتربة بإنتاج سعودي", "فايف إس شركة سعودية متخصصة في مواد وحلول تثبيت الرمال والتربة: تثبيت الكثبان، طرق ترابية، مكافحة الغبار، ممرات ومنحدرات.",
         "home", home, extra_ld=[ORG_LD], cls="page-home", source="home")
    page("about/", "من نحن | فايف إس لتثبيت الرمال والتربة", "قصة فايف إس: شركة سعودية تحوّل الرمال من عائق إلى أساس. الرؤية والرسالة والقيم وكلمة الرئيس التنفيذي.",
         "about", about, crumbs=[("من نحن", "about/")])
    page("solutions/", "تقنية 5S | مواد تثبيت الرمال — فايف إس", "تقنية 5S لمواد تثبيت الرمال والتربة: كيف تعمل، الخصائص العامة، السلامة، الشحن، ومقارنة المنتجات الخمسة.",
         "solutions", solutions, crumbs=[("الحلول", "solutions/")])
    for p in PRODUCTS:
        product(p)
    page("sectors/", "القطاعات | حلول فايف إس لتثبيت التربة", "حلول فايف إس لتسعة قطاعات: النقل، النفط والغاز، السياحة والتراث، الدفاع، الإنشاءات، الطيران، التعدين، الزراعة، الطاقة المتجددة.",
         "sectors", sectors_index, crumbs=[("القطاعات", "sectors/")])
    for s in SECTORS:
        sector(s)
    page("projects/", "المشاريع | فايف إس", "مشاريع فايف إس لتثبيت الرمال والتربة ومكافحة الغبار، مع فلترة حسب القطاع والتقنية والدولة.",
         "projects", projects, crumbs=[("المشاريع", "projects/")])
    page("technical-data/", "البيانات الفنية TDS و SDS | فايف إس", "مكتبة البيانات الفنية لمنتجات 5S: ملفات TDS وصحائف السلامة SDS وتقارير الاختبار والشهادات.",
         "knowledge", technical, crumbs=[("البيانات الفنية", "technical-data/")])
    page("partners/", "الشركاء والوكلاء | فايف إس", "وكلاء فايف إس في عمان والإمارات وليبيا ومصر وموريتانيا والسودان واليمن، وطلب الانضمام كشريك.",
         "knowledge", partners, crumbs=[("الشركاء والوكلاء", "partners/")])
    page("calculator/", "حاسبة المواد | فايف إس", "احسب الكمية التقديرية من مواد تثبيت الرمال والتربة بحاويات IBC حسب نوع التطبيق والمساحة، واطلب عرضًا دقيقًا.",
         "knowledge", calculator, crumbs=[("حاسبة المواد", "calculator/")])
    page("contact/", "تواصل معنا | اطلب عرض سعر — فايف إس", "تواصل مع فايف إس واطلب عرض سعر لمشروعك: +966 54 649 2775 · sales@5s-tech.org",
         "contact", contact, crumbs=[("تواصل معنا", "contact/")], extra_ld=[faq_ld(GENERAL_FAQ)])
    legal("privacy")
    legal("terms")
    redirects()
    sitemap()
    print(len(PAGES), "pages:", PAGES)
