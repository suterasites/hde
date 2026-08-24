#!/usr/bin/env python3
"""
Hoad Drainage - CCTV Drain Inspections x suburb landing-page generator.

Extracts chrome (head icons/fonts, GA + lead events, nav header, footer) VERBATIM
from the hand-built reference page `cctv-drain-inspections-frankston.html`, then
templates localised copy per suburb. Frankston is NOT regenerated (it has its own
suburb-specific service cluster and a richer related grid); it is the reference only.

Run from the site root:  python3 .build/suburb_render.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(ROOT, "cctv-drain-inspections-frankston.html")

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

# --- per-suburb data. hub = existing suburb hub page (breadcrumb parent) or None ---
SUBURBS = [
    {
        "slug": "somerville", "display": "Somerville", "hub": None, "nearby": None,
        "angle": "It's our home patch, we're based on Arduina Street, so a Somerville job is usually a quick run for us.",
        "prepurchase": "older homes on larger blocks often carry tree roots and the odd cracked section",
        "home_base": True,
    },
    {
        "slug": "mornington", "display": "Mornington", "hub": "drainage-mornington.html", "nearby": "Mount Martha",
        "angle": "Plenty of Mornington's older beachside homes still run ageing clay and earthenware pipe that tree roots love.",
        "prepurchase": "older coastal homes can have tree-root intrusion and ageing pipes",
    },
    {
        "slug": "mount-eliza", "display": "Mount Eliza", "hub": "drainage-mount-eliza.html", "nearby": None,
        "angle": "Mount Eliza's leafy, established blocks mean mature trees and long garden runs, and both put roots into drains.",
        "prepurchase": "established gardens and mature trees make tree-root intrusion one of the most common finds",
    },
    {
        "slug": "hastings", "display": "Hastings", "hub": None, "nearby": "Crib Point",
        "angle": "A lot of Hastings sits on older, low-lying ground where stormwater and sewer lines are worth checking before they back up.",
        "prepurchase": "older housing and low-lying ground mean clay pipe and tree roots are the usual culprits",
    },
    {
        "slug": "baxter", "display": "Baxter", "hub": None, "nearby": None,
        "angle": "Baxter's larger, semi-rural blocks often carry long drain runs, so a camera is the quick way to find where a fault sits.",
        "prepurchase": "larger semi-rural blocks often have long, older drain runs worth checking end to end",
    },
    {
        "slug": "tyabb", "display": "Tyabb", "hub": None, "nearby": None,
        "angle": "Tyabb properties are frequently on acreage with older or extended drain runs a camera can check end to end.",
        "prepurchase": "acreage blocks frequently have older or extended drain runs that are easy to miss",
    },
    {
        "slug": "bittern", "display": "Bittern", "hub": None, "nearby": "Hastings",
        "angle": "Around Bittern, sandy Western Port ground and older coastal pipework make a camera the fastest way to pin down a fault.",
        "prepurchase": "older coastal homes can hide root intrusion and tired pipework",
    },
    {
        "slug": "balnarring", "display": "Balnarring", "hub": None, "nearby": "Merricks",
        "angle": "Balnarring's mix of coastal, holiday and rural homes means drains that don't get used year-round and are worth a look before they cause trouble.",
        "prepurchase": "established and holiday homes often have ageing pipes and tree roots",
    },
    {
        "slug": "cranbourne", "display": "Cranbourne", "hub": None, "nearby": "Clyde",
        "region": "the Peninsula and the south-east",
        "angle": "Cranbourne's reactive clay soils shift with the seasons and crack rigid pipe, which is often the real cause of a drain that keeps blocking.",
        "prepurchase": "reactive clay ground is hard on rigid pipe, so cracked and misaligned joints are common, especially on older estates",
    },
    {
        "slug": "dromana", "display": "Dromana", "hub": None, "nearby": "Safety Beach",
        "angle": "Dromana's sloping foreshore blocks put a lot through the stormwater lines, and a camera shows exactly where a run is failing.",
        "prepurchase": "older beach homes and sloping blocks make stormwater faults and root intrusion common",
    },
    {
        "slug": "rosebud", "display": "Rosebud", "hub": None, "nearby": "Rye",
        "angle": "Rosebud's older beach houses and flat, sandy blocks are a regular camera job, especially where tree roots have found the sewer.",
        "prepurchase": "older beachside homes often have tree roots and tired earthenware pipe",
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
  "serviceType": "CCTV Drain Inspection",
  "name": "CCTV Drain Inspections in @@DISPLAY@@",
  "description": "In-pipe CCTV camera inspections of sewer, stormwater and sink drains in @@DISPLAY@@ to find blockages, tree roots, cracks and collapses without digging, with a written report on request.",
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
      <p class="eyebrow">CCTV drain inspections &middot; @@DISPLAY@@</p>
      <h1 class="page-hero__title">CCTV Drain Inspections in @@DISPLAY@@</h1>
      <p class="page-hero__lede">
        @@LEDE@@
      </p>
      <div class="page-hero__meta">
        <span>VBA licensed</span>
        <span>Written report on request</span>
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
          <img width="933" height="1400" src="assets/crew-working-manhole-connection.jpg" alt="Hoad Drainage crew member working at a drainage access point in @@DISPLAY@@." loading="lazy">
        </div>
        <div class="svc-row__body">
          <p class="eyebrow">What we do</p>
          <h2>See inside your @@DISPLAY@@ drain before you dig</h2>
          <p>
            We put a camera down the line and find out exactly why a @@DISPLAY@@ drain is slow, blocked or backing up, without tearing up the yard to guess. @@ANGLE@@ You get a straight rundown of what we found and what it takes to fix it, and where you need it, a written report with photos and footage for your records, a sale or a builder. It's the same <a href="cctv-drain-inspections.html">CCTV drain inspection service</a> we run right across @@REGION@@, here in @@DISPLAY@@.
          </p>
          <ul class="svc-row__list" role="list">
            <li>In-pipe camera survey of sewer, stormwater and sink drains</li>
            <li>Blockage, tree-root, crack and collapse detection</li>
            <li>Pipe locating and depth marking above ground</li>
            <li>Written report with photos and footage on request</li>
            <li>Pre-purchase and pre-handover inspections</li>
          </ul>
          <a class="btn btn--primary" href="contact.html">Book a CCTV inspection</a>
        </div>
      </article>
    </div>
  </section>

  <section class="process">
    <div class="container">
      <header class="section-head">
        <p class="eyebrow">How it works</p>
        <h2 class="section-head__title">A CCTV inspection in @@DISPLAY@@.</h2>
        <p class="section-head__lede">No mess, no guesswork, and we're only a short drive away.</p>
      </header>
      <div class="process__grid">
        <div class="process__step">
          <span class="process__num">1</span>
          <h3>You get in touch</h3>
          <p>Tell us what the drain's doing and the @@DISPLAY@@ address. We book a time and confirm if you need a written report.</p>
        </div>
        <div class="process__step">
          <span class="process__num">2</span>
          <h3>We access the line</h3>
          <p>We reach the drain through an existing point, an inspection opening, gully or pit, so there's nothing to dig up.</p>
        </div>
        <div class="process__step">
          <span class="process__num">3</span>
          <h3>Camera survey</h3>
          <p>We feed the camera through and record the run, locating any blockage, root, crack or collapse, plus its position and depth.</p>
        </div>
        <div class="process__step">
          <span class="process__num">4</span>
          <h3>Findings &amp; report</h3>
          <p>We talk you through what we found on the spot, and send a report with photos and footage where you've asked for one.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="faq">
    <div class="container faq__inner">
      <header class="section-head faq__head">
        <p class="eyebrow">Frequently asked</p>
        <h2 class="section-head__title">@@DISPLAY@@ CCTV inspection questions.</h2>
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
        <a class="related__card" href="blocked-drains-@@SLUG@@.html">
          <span class="related__num">02</span>
          <span>
            <h3>Blocked Drains &amp; Jetting</h3>
            <p>Found a blockage on camera? We clear it fast with high-pressure jetting.</p>
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
            <p>Renewals and repairs when the camera finds a collapse or broken line.</p>
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
        <h2 class="section-head__title">CCTV inspections across the Peninsula.</h2>
        <p class="section-head__lede">We run camera inspections suburb by suburb, from Somerville out across the Peninsula and into the south-east.</p>
      </header>
      <div class="regions">
@@AREAS@@
      </div>
    </div>
  </section>

  <section class="cta-band">
    <div class="container cta-band__inner">
      <div class="cta-band__copy">
        <h2>Want eyes on your @@DISPLAY@@ drain?</h2>
        <p>Book a CCTV inspection online, or call the office and we'll come back the same business day.</p>
      </div>
      <div class="cta-band__ctas">
        <a class="btn btn--pill btn--primary btn--pill-icon" href="contact.html">
          <span>Book an inspection</span>
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


# All 12 CCTV suburb pages (incl. the hand-built Frankston), split into two link columns.
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
        cols[col].append(f'            <li><a href="cctv-drain-inspections-{slug}.html">{disp}</a></li>')
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
        q1 = ("Yes. We're based right here in Somerville, so a CCTV inspection is often a same-day run for us. "
              "We feed a camera through the line and show you exactly what's going on, without digging.")
    else:
        q1 = (f"Yes. We're based just up the road in Somerville and CCTV inspections in {d}{near_and} are a regular job for us. "
              "We feed a camera through the line and show you exactly what's going on, without digging.")
    q2 = (f"Yes. Pre-purchase CCTV inspections are common in {d}, where {s['prepurchase']}. "
          "We give you a clear picture of the drain's condition and, where you need it, a written report with photos and footage for the sale.")
    q3 = ("Where you need one, yes. We can supply a written report with photos and footage for a sale, a builder or your own records. "
          "Just let us know when you book.")
    q4 = ("No. We access the drain through an existing point such as an inspection opening, gully or pit, so there's no digging to find the fault.")
    qa = [
        (f"Do you do CCTV drain inspections in {d}?", q1),
        (f"Can you inspect the drains before I buy a {d} property?", q2),
        ("Do I get a report with the inspection?", q3),
        ("Do you need to dig anything up for the camera?", q4),
    ]
    # JSON-LD (answers have no double quotes, safe to inline)
    json_items = []
    for q, a in qa:
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
    faq_html = "\n".join(html_items)
    return faq_json, faq_html


def breadcrumb(s):
    d = s["display"]
    slug = s["slug"]
    page_url = f"{BASE}/cctv-drain-inspections-{slug}.html"
    if s.get("hub"):
        hub_url = f"{BASE}/{s['hub']}"
        bc = (
            f'    {{"@type": "ListItem", "position": 1, "name": "Home", "item": "{BASE}/"}},\n'
            f'    {{"@type": "ListItem", "position": 2, "name": "{d}", "item": "{hub_url}"}},\n'
            f'    {{"@type": "ListItem", "position": 3, "name": "CCTV Drain Inspections", "item": "{page_url}"}}'
        )
        crumbs = (
            '      <a href="index.html">Home</a>\n'
            '      <span class="crumbs__sep" aria-hidden="true">/</span>\n'
            f'      <a href="{s["hub"]}">{d}</a>\n'
            '      <span class="crumbs__sep" aria-hidden="true">/</span>\n'
            '      <span aria-current="page">CCTV Drain Inspections</span>'
        )
    else:
        bc = (
            f'    {{"@type": "ListItem", "position": 1, "name": "Home", "item": "{BASE}/"}},\n'
            f'    {{"@type": "ListItem", "position": 2, "name": "CCTV Drain Inspections", "item": "{BASE}/cctv-drain-inspections.html"}},\n'
            f'    {{"@type": "ListItem", "position": 3, "name": "{d}", "item": "{page_url}"}}'
        )
        crumbs = (
            '      <a href="index.html">Home</a>\n'
            '      <span class="crumbs__sep" aria-hidden="true">/</span>\n'
            '      <a href="cctv-drain-inspections.html">CCTV Drain Inspections</a>\n'
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
    canon = f"{BASE}/cctv-drain-inspections-{slug}.html"

    title = f"CCTV Drain Inspections in {d} | Hoad Drainage"
    desc = (f"CCTV drain camera inspections in {d}{near_and}. "
            "Find blockages, tree roots, cracks and collapses without digging, with a written report on request.")
    og_title = f"CCTV Drain Inspections in {d} | Camera Surveys &amp; Reports | Hoad Drainage &amp; Excavations"
    og_desc = desc + " Local, VBA licensed."

    lede = (f"When a {d} drain keeps blocking, or you're about to buy, a camera tells you exactly what's going on before anyone digs. "
            f"We survey sewer, stormwater and sink drains across {d}{near_and}, and give you a clear picture with a written report on request.")

    if s.get("hub"):
        footnote = (f'See all our <a href="{s["hub"]}">drainage services in {d}</a>, '
                    'or call <a href="tel:0359780120">(03) 5978 0120</a>.')
    else:
        footnote = ('See our full range of <a href="services.html">drainage services</a> across ' + region + ', '
                    'or call <a href="tel:0359780120">(03) 5978 0120</a>.')

    faq_json, faq_html = faq_blocks(s)
    bc_json, crumbs = breadcrumb(s)

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
        "@@CRUMBS@@": crumbs,
        "@@AREAS@@": areas_regions(exclude_slug=slug),
        "@@SLUG@@": slug,
        "@@REGION@@": region,
        "@@DISPLAY@@": d,
    }
    for k, v in repl.items():
        out = out.replace(k, v)
    return out


def main():
    written = []
    for s in SUBURBS:
        path = os.path.join(ROOT, f"cctv-drain-inspections-{s['slug']}.html")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(build(s))
        written.append(os.path.basename(path))
    print(f"Wrote {len(written)} pages:")
    for w in written:
        print("  " + w)


if __name__ == "__main__":
    main()
