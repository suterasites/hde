#!/usr/bin/env python3
"""
Hoad Drainage - Blocked Drains & Jetting x suburb landing-page generator.

Same shape as .build/suburb_render.py (the CCTV cluster), but built off the
hand-written reference page `blocked-drains-frankston.html`: chrome (head icons/
fonts, GA + lead events, nav header, footer) is extracted VERBATIM from it, then
localised copy is templated per suburb. Frankston is NOT regenerated (it has its
own suburb-specific related grid pointing at the four other Frankston service
pages); it is the reference only.

Filenames follow the reference: blocked-drains-<suburb>.html. That matters -
WP HQ's coverage matrix lights the "Blocked Drains & Jetting" row by matching the
clients.yaml term "blocked drain" as a substring of the page basename, with the
suburb slug as a contiguous token run.

Run from the site root:  python3 .build/blocked_drains_render.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(ROOT, "blocked-drains-frankston.html")

with open(REF, encoding="utf-8") as fh:
    ref = fh.read()


def grab(pattern):
    m = re.search(pattern, ref)
    if not m:
        raise SystemExit(f"chrome block not found: {pattern}")
    return m.group(1)


# --- verbatim chrome, byte-identical to the reference page ---
HEAD_ICONS = grab(r'(<link rel="icon"[\s\S]*?<link rel="stylesheet" href="styles\.css">)')
GA_EVENTS  = grab(r'(  <!-- Google tag \(gtag\.js\) -->[\s\S]*?</script>)\s*</head>')
NAV        = grab(r'(<header class="site-header"[\s\S]*?</header>)')
FOOTER     = grab(r'(<footer class="site-footer">[\s\S]*?</footer>)')

BASE = "https://hoaddrainage.com.au"

# --- per-suburb data. hub = existing suburb hub LP (breadcrumb parent) or None ---
# angle  = one localising sentence inside the "What we do" paragraph
# cause  = tail of "In <Suburb> it's often ..." in the causes FAQ
SUBURBS = [
    {
        "slug": "somerville", "display": "Somerville", "hub": None, "nearby": None,
        "home_base": True,
        "angle": "It's our home patch, we're based on Arduina Street, so a Somerville blockage is usually a quick run for us.",
        "cause": "tree roots and grease in the older pipes on the bigger blocks around here, plus the usual debris and foreign objects",
    },
    {
        "slug": "mornington", "display": "Mornington", "hub": "drainage-mornington.html", "nearby": "Mount Martha",
        "angle": "Plenty of Mornington's older beachside homes still run ageing clay and earthenware pipe that roots and grease block up.",
        "cause": "tree roots and grease working into the ageing clay and earthenware pipe under a lot of the older beachside homes",
    },
    {
        "slug": "mount-eliza", "display": "Mount Eliza", "hub": "drainage-mount-eliza.html", "nearby": None,
        "angle": "Mount Eliza's leafy, established blocks mean mature trees and long drain runs, and both put roots where they aren't wanted.",
        "cause": "tree roots off the mature gardens getting into long drain runs, along with grease and the usual debris",
    },
    {
        "slug": "hastings", "display": "Hastings", "hub": None, "nearby": "Crib Point",
        "angle": "A lot of Hastings sits on older, low-lying ground where a slow sewer or stormwater line backs up fast once it blocks.",
        "cause": "roots and debris in older pipework on low-lying ground, where a slow line backs up quickly once it silts up",
    },
    {
        "slug": "baxter", "display": "Baxter", "hub": None, "nearby": None,
        "angle": "Baxter's larger, semi-rural blocks often carry long drain runs, so jetting is the quick way to scour the whole line out.",
        "cause": "roots and debris building up in the long drain runs that come with larger, semi-rural blocks",
    },
    {
        "slug": "tyabb", "display": "Tyabb", "hub": None, "nearby": None,
        "angle": "Tyabb properties are frequently on acreage with older or extended drain runs a jetter can clear end to end.",
        "cause": "roots and silt in the older, extended drain runs you get on acreage, plus grease off the house lines",
    },
    {
        "slug": "bittern", "display": "Bittern", "hub": None, "nearby": "Hastings",
        "angle": "Around Bittern, sandy Western Port ground and older coastal pipework mean blockages that keep coming back until the line is properly scoured.",
        "cause": "roots and sand working into older coastal pipework, along with grease and debris from the house",
    },
    {
        "slug": "balnarring", "display": "Balnarring", "hub": None, "nearby": "Merricks",
        "angle": "Balnarring's mix of coastal, holiday and rural homes means drains that sit unused for stretches and then block up once the house fills again.",
        "cause": "roots and debris settling in lines that sit unused between visits at holiday and weekend homes, plus grease in the older pipes",
    },
    {
        "slug": "cranbourne", "display": "Cranbourne", "hub": None, "nearby": "Clyde",
        "region": "the Peninsula and the south-east",
        "angle": "Cranbourne's reactive clay soils shift with the seasons and crack rigid pipe, which is often the real reason a drain keeps blocking.",
        "cause": "reactive clay ground cracking rigid pipe and letting roots in, on top of the usual grease and debris",
    },
    {
        "slug": "dromana", "display": "Dromana", "hub": None, "nearby": "Safety Beach",
        "angle": "Dromana's sloping foreshore blocks put a lot through the stormwater lines, so a blockage tends to show itself quickly after rain.",
        "cause": "roots and debris in older beach-house pipework, and stormwater lines that cop a lot off sloping blocks",
    },
    {
        "slug": "rosebud", "display": "Rosebud", "hub": None, "nearby": "Rye",
        "angle": "Rosebud's older beach houses and flat, sandy blocks are a regular jetting job, especially where tree roots have found the sewer.",
        "cause": "tree roots getting into tired earthenware sewer pipe under a lot of the older beach houses, plus grease and debris",
    },
]

PAGE = """<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>@@TITLE@@</title>
<meta name="description" content="@@DESC@@">
<!-- SUTERA_SOCIAL_META -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="Hoad Drainage & Excavations">
<meta property="og:title" content="@@OGTITLE@@">
<meta property="og:description" content="@@OGDESC@@">
<meta property="og:url" content="@@CANON@@">
<meta property="og:image" content="https://hoaddrainage.com.au/assets/og-hoad.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Hoad Drainage & Excavations">
<meta property="og:locale" content="en_AU">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="@@OGTITLE@@">
<meta name="twitter:description" content="@@OGDESC@@">
<meta name="twitter:image" content="https://hoaddrainage.com.au/assets/og-hoad.jpg">

<meta name="theme-color" content="#0A1F2E">
<link rel="canonical" href="@@CANON@@">

@@HEAD_ICONS@@

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "Blocked Drain Clearing",
  "name": "Blocked Drains & Jetting in @@DISPLAY@@",
  "description": "Clearing of blocked sewer, stormwater and sink drains in @@DISPLAY@@ with high-pressure water jetting, followed by a camera check to confirm the line is clear.",
  "url": "@@CANON@@",
  "areaServed": {"@type": "Place", "name": "@@DISPLAY@@, VIC"},
  "provider": {
    "@type": "Plumber",
    "name": "Hoad Drainage & Excavations",
    "telephone": "+61359780120",
    "url": "https://hoaddrainage.com.au/",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "5 Arduina Street",
      "addressLocality": "Somerville",
      "addressRegion": "VIC",
      "postalCode": "3912",
      "addressCountry": "AU"
    }
  }
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
@@BREADCRUMB_JSON@@
  ]
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
@@FAQ_JSON@@
  ]
}
</script>
@@GA_EVENTS@@
</head>
<body>

<a class="skip-link" href="#main">Skip to content</a>

@@NAV@@

<main id="main">

  <section class="page-hero">
    <div class="container page-hero__inner">
      <p class="eyebrow">Blocked drains &amp; jetting &middot; @@DISPLAY@@</p>
      <h1 class="page-hero__title">Blocked Drains in @@DISPLAY@@</h1>
      <p class="page-hero__lede">
        @@LEDE@@
      </p>
      <div class="page-hero__meta">
        <span>Same day where possible</span>
        <span>Camera check included</span>
        <span>Call <a href="tel:0359780120">(03) 5978 0120</a></span>
      </div>
    </div>
  </section>

  <nav class="crumbs" aria-label="Breadcrumb">
    <div class="container crumbs__inner">
@@CRUMBS@@
    </div>
  </nav>

  <section class="svc-detail">
    <div class="container">
      <article class="svc-row">
        <div class="svc-row__media">
          <img width="1400" height="933" src="assets/crew-drainage-pit-fenceline.jpg" alt="Hoad Drainage crew clearing a drain along a fence line in @@DISPLAY@@." loading="lazy">
        </div>
        <div class="svc-row__body">
          <p class="eyebrow">What we do</p>
          <h2>@@DISPLAY@@ blockages, cleared properly</h2>
          <p>
            High-pressure water jetting cuts through the grease, roots and debris that a plunger or a snake won't shift, and scours the pipe wall clean instead of just punching a hole through the blockage. Then we camera the line to confirm it's clear and show you what caused it. @@ANGLE@@ It's the same <a href="blocked-drains-jetting.html">blocked drain and jetting service</a> we run right across @@REGION@@, here in @@DISPLAY@@.
          </p>
          <ul class="svc-row__list" role="list">
            <li>High-pressure water jetting</li>
            <li>Tree-root cutting and grease removal</li>
            <li>Sewer, stormwater and sink drains</li>
            <li>Camera check after clearing</li>
            <li>Same-day service where possible</li>
          </ul>
          <a class="btn btn--primary" href="contact.html">Book a drain clear</a>
        </div>
      </article>
    </div>
  </section>

  <section class="process">
    <div class="container">
      <header class="section-head">
        <p class="eyebrow">How it works</p>
        <h2 class="section-head__title">From blocked to flowing in @@DISPLAY@@.</h2>
        <p class="section-head__lede">@@PROCESS_LEDE@@</p>
      </header>
      <div class="process__grid">
        <div class="process__step">
          <span class="process__num">1</span>
          <h3>You call it in</h3>
          <p>Tell us what's blocked and the @@DISPLAY@@ address. If it's backing up, call early and we'll try for the same day.</p>
        </div>
        <div class="process__step">
          <span class="process__num">2</span>
          <h3>We find the blockage</h3>
          <p>We locate the affected line and the cause, whether it's roots, grease, debris or something that shouldn't be down there.</p>
        </div>
        <div class="process__step">
          <span class="process__num">3</span>
          <h3>Jet it clear</h3>
          <p>High-pressure water clears the blockage and scours the pipe wall, so the line runs the way it should again.</p>
        </div>
        <div class="process__step">
          <span class="process__num">4</span>
          <h3>Camera confirm</h3>
          <p>We camera the line to prove it's clear and show what caused it, so you know if it's a one-off or a bigger fix.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="faq">
    <div class="container faq__inner">
      <header class="section-head faq__head">
        <p class="eyebrow">Frequently asked</p>
        <h2 class="section-head__title">@@DISPLAY@@ blocked drain questions.</h2>
      </header>
      <div class="faq__list">
@@FAQ_HTML@@
      </div>
      <p class="faq__footnote">
        @@FAQ_FOOTNOTE@@
      </p>
    </div>
  </section>

  <section class="related">
    <div class="container">
      <header class="section-head">
        <p class="eyebrow">More in @@DISPLAY@@</p>
        <h2 class="section-head__title">Other services in @@DISPLAY@@.</h2>
      </header>
      <div class="related__grid">
        <a class="related__card" href="cctv-drain-inspections-@@SLUG@@.html">
          <span class="related__num">01</span>
          <span>
            <h3>CCTV Drain Inspections</h3>
            <p>Camera survey to find exactly what's blocking the line and why.</p>
          </span>
        </a>
        <a class="related__card" href="non-destructive-digging.html">
          <span class="related__num">03</span>
          <span>
            <h3>Non-Destructive Digging</h3>
            <p>Vac truck excavation to safely expose a @@DISPLAY@@ drain for repair.</p>
          </span>
        </a>
        <a class="related__card" href="sewer-stormwater-drainage.html">
          <span class="related__num">04</span>
          <span>
            <h3>Sewer &amp; Stormwater</h3>
            <p>Renewals and repairs when a blockage turns out to be a broken pipe.</p>
          </span>
        </a>
        <a class="related__card" href="civil-commercial-drainage.html">
          <span class="related__num">05</span>
          <span>
            <h3>Civil, Unit &amp; Commercial</h3>
            <p>Full underground drainage for @@DISPLAY@@ builders and developers.</p>
          </span>
        </a>
      </div>
    </div>
  </section>

  <section class="related related--areas">
    <div class="container">
      <header class="section-head">
        <p class="eyebrow">Where else we work</p>
        <h2 class="section-head__title">Blocked drains cleared across the Peninsula.</h2>
        <p class="section-head__lede">We clear and jet drains suburb by suburb, from Somerville out across the Peninsula and into the south-east.</p>
      </header>
      <div class="regions">
@@AREAS@@
      </div>
    </div>
  </section>

  <section class="cta-band">
    <div class="container cta-band__inner">
      <div class="cta-band__copy">
        <h2>Drain backing up in @@DISPLAY@@?</h2>
        <p>Book a drain clear online, or call the office and we'll do our best to get to you the same business day.</p>
      </div>
      <div class="cta-band__ctas">
        <a class="btn btn--pill btn--primary btn--pill-icon" href="contact.html">
          <span>Book a drain clear</span>
          <span class="btn__icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" width="14" height="14" focusable="false">
              <path fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" d="M7 17L17 7M9 7h8v8"/>
            </svg>
          </span>
        </a>
        <a class="btn btn--pill btn--outline-light" href="tel:0359780120">(03) 5978 0120</a>
      </div>
    </div>
  </section>

</main>

@@FOOTER@@

<script src="script.js"></script>
</body>
</html>
"""


# All 12 blocked-drain suburb pages (incl. the hand-built Frankston), split into
# two link columns. Same split as the CCTV cluster so the two clusters read alike.
ALL = [
    ("somerville", "Somerville", "A"),
    ("frankston", "Frankston", "A"),
    ("mornington", "Mornington", "A"),
    ("mount-eliza", "Mount Eliza", "A"),
    ("baxter", "Baxter", "A"),
    ("tyabb", "Tyabb", "A"),
    ("hastings", "Hastings", "B"),
    ("bittern", "Bittern", "B"),
    ("balnarring", "Balnarring", "B"),
    ("dromana", "Dromana", "B"),
    ("rosebud", "Rosebud", "B"),
    ("cranbourne", "Cranbourne", "B"),
]
COL_HEADS = {"A": "Mornington Peninsula", "B": "Western Port &amp; South East"}


def areas_regions(exclude_slug=None):
    cols = {"A": [], "B": []}
    for slug, disp, col in ALL:
        if slug == exclude_slug:
            continue
        cols[col].append(f'            <li><a href="blocked-drains-{slug}.html">{disp}</a></li>')
    blocks = []
    for key in ("A", "B"):
        blocks.append(
            '        <div class="region">\n'
            f'          <h3>{COL_HEADS[key]}</h3>\n'
            '          <ul role="list">\n'
            + "\n".join(cols[key]) + "\n"
            '          </ul>\n'
            '        </div>'
        )
    return "\n".join(blocks)


def faq_blocks(s):
    d = s["display"]
    nearby = s.get("nearby")
    near_and = f" and {nearby}" if nearby else ""
    if s.get("home_base"):
        q1 = ("Wherever we can, yes. We're based right here in Somerville, so call early and we'll do our best to clear "
              "your blockage the same day, then run a camera through to confirm it's clear.")
    else:
        q1 = (f"Wherever we can, yes. We're only a short drive from {d} in Somerville, so call early and we'll do our best "
              "to clear your blockage the same day, then run a camera through to confirm it's clear.")
    q2 = (f"In {d} it's often {s['cause']}. We clear it with high-pressure jetting and camera the line to see whether it was "
          "a one-off or a bigger issue like root intrusion into a cracked pipe.")
    q3 = ("That depends on the cause. After we clear the line we run a camera through to check. If it's structural, like root "
          f"intrusion or a broken pipe, we'll show you and talk through a lasting fix so you're not clearing the same {d} drain "
          "every few months.")
    q4 = (f"Sewer, stormwater and sink drains at homes, units and commercial sites across {d}{near_and}. Blocked toilets, gurgling "
          "drains, water backing up in the yard and slow sinks and showers, we clear the lot.")
    qa = [
        (f"Can you clear a blocked drain in {d} today?", q1),
        (f"What causes blocked drains in {d} homes?", q2),
        ("Will the blockage come back?", q3),
        ("What drains can you clear?", q4),
    ]
    # JSON-LD (answers carry no double quotes, so they are safe to inline)
    json_items = []
    for q, a in qa:
        assert '"' not in a and '"' not in q, f"double quote in FAQ copy for {d}"
        json_items.append(
            '    {\n'
            '      "@type": "Question",\n'
            f'      "name": "{q}",\n'
            '      "acceptedAnswer": {"@type": "Answer", "text": "' + a + '"}\n'
            '    }'
        )
    faq_json = ",\n".join(json_items)
    # visual HTML
    html_items = []
    for q, a in qa:
        html_items.append(
            '        <details class="faq__item">\n'
            '          <summary>\n'
            f'            <span>{q}</span>\n'
            '            <span class="faq__icon" aria-hidden="true"></span>\n'
            '          </summary>\n'
            '          <div class="faq__answer">\n'
            f'            <p>{a}</p>\n'
            '          </div>\n'
            '        </details>'
        )
    return faq_json, "\n".join(html_items)


def breadcrumb(s):
    d = s["display"]
    slug = s["slug"]
    page_url = f"{BASE}/blocked-drains-{slug}.html"
    if s.get("hub"):
        hub_url = f"{BASE}/{s['hub']}"
        bc = (
            f'    {{"@type": "ListItem", "position": 1, "name": "Home", "item": "{BASE}/"}},\n'
            f'    {{"@type": "ListItem", "position": 2, "name": "{d}", "item": "{hub_url}"}},\n'
            f'    {{"@type": "ListItem", "position": 3, "name": "Blocked Drains & Jetting", "item": "{page_url}"}}'
        )
        crumbs = (
            '      <a href="index.html">Home</a>\n'
            '      <span class="crumbs__sep" aria-hidden="true">/</span>\n'
            f'      <a href="{s["hub"]}">{d}</a>\n'
            '      <span class="crumbs__sep" aria-hidden="true">/</span>\n'
            '      <span aria-current="page">Blocked Drains &amp; Jetting</span>'
        )
    else:
        bc = (
            f'    {{"@type": "ListItem", "position": 1, "name": "Home", "item": "{BASE}/"}},\n'
            f'    {{"@type": "ListItem", "position": 2, "name": "Blocked Drains & Jetting", "item": "{BASE}/blocked-drains-jetting.html"}},\n'
            f'    {{"@type": "ListItem", "position": 3, "name": "{d}", "item": "{page_url}"}}'
        )
        crumbs = (
            '      <a href="index.html">Home</a>\n'
            '      <span class="crumbs__sep" aria-hidden="true">/</span>\n'
            '      <a href="blocked-drains-jetting.html">Blocked Drains &amp; Jetting</a>\n'
            '      <span class="crumbs__sep" aria-hidden="true">/</span>\n'
            f'      <span aria-current="page">{d}</span>'
        )
    return bc, crumbs


def build(s):
    d = s["display"]
    slug = s["slug"]
    nearby = s.get("nearby")
    near_and = f" and {nearby}" if nearby else ""
    region = s.get("region", "the Peninsula")
    canon = f"{BASE}/blocked-drains-{slug}.html"

    title = f"Blocked Drains in {d} | Hoad Drainage"
    desc = (f"Blocked drains in {d} cleared fast with high-pressure jetting: sewer, stormwater and sink drains, "
            "tree roots and grease, and a camera check to finish.")
    og_title = f"Blocked Drains in {d} | Same-Day Jetting Where Possible | Hoad Drainage &amp; Excavations"
    og_desc = (f"Blocked drains in {d} cleared fast with high-pressure jetting. Sewer, stormwater and sink drains, tree roots "
               "and grease, with a camera check to confirm it&#x27;s clear. Local, same day where possible.")

    lede = ("Blocked toilet, gurgling drain, or water backing up in the yard? We clear blocked sewer, stormwater and sink drains "
            f"across {d}{near_and} fast with high-pressure jetting, then camera the line to make sure it's properly clear, so it "
            "doesn't come straight back.")

    if s.get("home_base"):
        process_lede = "A straightforward job when it's done right, and we're just around the corner."
    else:
        process_lede = "A straightforward job when it's done right, and we're close by."

    if s.get("hub"):
        footnote = (f'See all our <a href="{s["hub"]}">drainage services in {d}</a>, '
                    'or call <a href="tel:0359780120">(03) 5978 0120</a>.')
    else:
        footnote = ('See our full range of <a href="services.html">drainage services</a> across ' + region + ', '
                    'or call <a href="tel:0359780120">(03) 5978 0120</a>.')

    faq_json, faq_html = faq_blocks(s)
    bc_json, crumbs = breadcrumb(s)

    if len(title) > 60:
        print(f"  WARN title {len(title)} chars: {title}")
    if len(desc) > 160:
        print(f"  WARN description {len(desc)} chars: {slug}")

    out = PAGE
    repl = {
        "@@TITLE@@": title,
        "@@DESC@@": desc,
        "@@OGTITLE@@": og_title,
        "@@OGDESC@@": og_desc,
        "@@CANON@@": canon,
        "@@HEAD_ICONS@@": HEAD_ICONS,
        "@@GA_EVENTS@@": GA_EVENTS,
        "@@NAV@@": NAV,
        "@@FOOTER@@": FOOTER,
        "@@BREADCRUMB_JSON@@": bc_json,
        "@@FAQ_JSON@@": faq_json,
        "@@FAQ_HTML@@": faq_html,
        "@@FAQ_FOOTNOTE@@": footnote,
        "@@LEDE@@": lede,
        "@@ANGLE@@": s["angle"],
        "@@PROCESS_LEDE@@": process_lede,
        "@@CRUMBS@@": crumbs,
        "@@AREAS@@": areas_regions(exclude_slug=slug),
        "@@SLUG@@": slug,
        "@@REGION@@": region,
        "@@DISPLAY@@": d,
    }
    for k, v in repl.items():
        out = out.replace(k, v)
    if "@@" in out:
        raise SystemExit(f"unresolved placeholder in {slug}")
    return out


def main():
    written = []
    for s in SUBURBS:
        path = os.path.join(ROOT, f"blocked-drains-{s['slug']}.html")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(build(s))
        written.append(os.path.basename(path))
    print(f"Wrote {len(written)} pages:")
    for w in written:
        print("  " + w)


if __name__ == "__main__":
    main()
