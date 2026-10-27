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

Every internal href, canonical, og:url and JSON-LD url is the extension-less
form (/blocked-drains-cranbourne, not .html). Cloudflare Pages 308s the .html
form, and pointing at a redirect split every page into two indexed URLs until the
2026-08-28 clean-URL sweep. Regenerating must not bring the .html form back.

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
        "home_base": True, "civil": "civil-commercial-somerville",
        "angle": "It's our home patch, we're based on Arduina Street, so a Somerville blockage is usually a quick run for us.",
        "cause": "tree roots and grease in the older pipes on the bigger blocks around here, plus the usual debris and foreign objects",
    },
    {
        "slug": "mornington", "display": "Mornington", "hub": "drainage-mornington", "nearby": "Mount Martha",
        "angle": "Plenty of Mornington's older beachside homes still run ageing clay and earthenware pipe that roots and grease block up.",
        "cause": "tree roots and grease working into the ageing clay and earthenware pipe under a lot of the older beachside homes",
    },
    {
        "slug": "mount-eliza", "display": "Mount Eliza", "hub": "drainage-mount-eliza", "nearby": None,
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

# --- suburbs rewritten with their own copy (2026-10-27) ---
# The 12 templated pages were 94% the same words with the suburb swapped. Seven of them
# (Cranbourne, Mornington, Mount Eliza, Rosebud, Dromana, Tyabb, Somerville) fell from
# ~40 impressions a day to zero between 2026-09-22 and 09-24, still indexed, as Google's
# September 2026 spam update rolled out, while the hand-built suburb hubs held. A page
# listed here keeps the shared chrome, process, related and areas blocks, and gets its
# own lede, its own "What we do" row, a second local row with a verbatim Google review,
# its own photos and its own FAQ. The rest stay templated, as the control.
# Copy rules: no claim about a suburb's soil or pipe stock that cannot be checked, no
# invented jobs, reviews quoted verbatim (reviews.json), photo alts never name a place.
LOCAL = {
    "cranbourne": {
        "lede": ("Blocked toilet, a gurgling floor waste, or stormwater pooling across a new estate yard? We clear "
                 "blocked sewer, stormwater and sink drains across Cranbourne and Clyde with high-pressure jetting, "
                 "then camera the line so you can see what caused it."),
        "img": ("pvc-pipe-ends-closeup.jpg", 1400, 933, "Close-up of PVC drainage pipe ends on a job."),
        "what_h2": "Newer pipe, different blockages",
        "what_paras": [
            "Much of Cranbourne is newer estate housing, and newer houses run PVC drains. PVC doesn't crack and root "
            "up the way old clay pipe does, so when a Cranbourne drain blocks, the cause is usually something that "
            "went down it: wet wipes, cooking fat, sanitary products, or building debris left in the line when the "
            "house went up.",
            "We jet the line with high-pressure water, which scours the pipe wall instead of punching a hole through "
            "the blockage, then run a camera through it. On a newer house the camera answers the question that "
            "matters: was it something flushed, or a fault in how the drain was laid?",
        ],
        "what_list": [
            "High-pressure jetting for sewer, stormwater and sink lines",
            "Camera check after every clear",
            "CCTV reports for a builder or owners corporation",
            "Unit and townhouse sites with shared drains",
            "Same day where possible",
        ],
        "local_img": ("estate-drainage-trench.jpg", 1050, 1400, "Long drainage trench running across an estate block."),
        "local_eyebrow": "Cranbourne drains",
        "local_h2": "When a new drain keeps blocking",
        "local_paras": [
            "A drain that blocks again a few weeks after it was cleared usually isn't a flushing problem. On newer "
            "homes the usual suspects are a length of pipe that sagged as the ground settled, leaving a dip where "
            "waste sits, or concrete slurry and render that washed into the line during the build and set hard.",
            "Jetting moves the blockage. The camera shows whether there's a sag, a joint that has pulled apart or "
            "debris set in the pipe, and exactly where. If the house is new, that footage is what your builder "
            "will want to see.",
            "Unit and townhouse sites are the other common job. Several dwellings often share one sewer line, so "
            "one blockage backs up more than one home. We clear the shared line and camera it, so whoever manages "
            "the site knows which section needs work.",
            "We lay new-build drainage for builders across the south-east, and were named Best Supplier East at the "
            "2026 Carlisle Homes Supplier of the Year Awards, so we know how these lines are meant to go in.",
        ],
        "quote": {"name": "Chris Cleef",
                  "text": "Jarryd and his team were fantastic to deal with across the whole process of creating and "
                          "implementing a storm water drainage plan, even with project delays out of their control. "
                          "Work was completed swiftly to the highest standard."},
        "faqs": [
            ("Can you clear a blocked drain in Cranbourne today?",
             "Wherever we can, yes. We come up to Cranbourne from our Somerville base, so call early and we'll do our "
             "best to get to you the same day. Every clear finishes with a camera check."),
            ("My house is only a few years old. Why is the drain blocking?",
             "Usually one of three things: something flushed that shouldn't have been, building debris left in the "
             "line from construction, or a section of pipe that has sagged as the ground settled. Jetting clears it, "
             "and the camera shows which one it was."),
            ("Is a blocked sewer my problem or South East Water's?",
             "South East Water looks after the sewer main. The drain on your side of the connection is the property "
             "owner's. If your neighbours are backing up too, ring South East Water first, because a blocked main is "
             "theirs to clear. If it's only your place, it's usually your line, and that's where we come in."),
            ("Do you clear shared drains on unit sites?",
             "Yes. We clear and camera shared sewer and stormwater lines on unit and townhouse sites, and the footage "
             "shows which section the problem is in, which matters when more than one owner is involved."),
            ("Can I get a CCTV report to show my builder?",
             'Yes. We can record the camera run and put it in a report, so your builder or owners corporation sees '
             'the same footage we did. See our <a href="cctv-drain-inspections-cranbourne">CCTV drain inspections '
             'in Cranbourne</a>.'),
        ],
    },
    "mornington": {
        "lede": ("Blocked toilet, a gurgling drain, or water coming up through the yard after rain? We clear blocked "
                 "sewer, stormwater and sink drains across Mornington with high-pressure jetting, then camera the "
                 "line to show you what caused it."),
        "img": ("hoad-service-truck-equipment.jpg", 1400, 933,
                "Hoad Drainage CCTV and jetting truck with its high-pressure hose reel."),
        "what_h2": "Roots, grease and older pipe",
        "what_paras": [
            "Mornington has a lot of established homes, and the older the house, the more likely its sewer is clay "
            "pipe rather than PVC. Clay is laid in short lengths, and every joint is a gap a tree root can find. "
            "Once a root is in, it grows, catches paper and grease, and the line slows until it stops.",
            "Our jetter cuts the roots out and scours the pipe wall, then the camera goes through to show the state "
            "of the line. One root at one joint is a maintenance job. Roots at every joint, or a cracked section, is "
            "a different conversation, and we'll show you the footage rather than ask you to take our word for it.",
        ],
        "what_list": [
            "Root cutting and high-pressure jetting",
            "Sewer, stormwater and sink drains",
            "Camera check after every clear",
            "Commercial and kitchen lines",
            "Same day where possible",
        ],
        "local_img": ("crew-working-manhole-connection.jpg", 933, 1400,
                      "Crew member making a connection at a drainage access point."),
        "local_eyebrow": "Mornington drains",
        "local_h2": "Renovating? Camera the old line first",
        "local_paras": [
            "There's a lot of renovating going on around Mornington, and the old sewer line usually stays put while "
            "the house above it gets a new kitchen and bathroom. If that line is already rooted or cracked, the "
            "easiest time to renew it is while the yard is open and the builder is on site, not after the new "
            "paving goes down.",
            'A camera inspection before the work starts tells you which you have. See our '
            '<a href="cctv-drain-inspections-mornington">CCTV drain inspections in Mornington</a>, or everything '
            'we do in town, from blocked drains to the underground stage of a renovation, on our '
            '<a href="drainage-mornington">Mornington drainage page</a>.',
            "We jet commercial lines too. In a busy kitchen, grease sets on the pipe wall a little every service "
            "until the line closes up. Jetting strips it back to the pipe, and the camera confirms it's gone, not "
            "just holed through.",
        ],
        "quote": {"name": "Ben Rahilly",
                  "text": "Highly recommend Hoad Drainage & Excavations. They arrived on time an assessed our drainage "
                          "issue using their CCTV camera at a facility in Baxter and got the drains flowing again in "
                          "no time with their jetting truck."},
        "faqs": [
            ("Can you clear a blocked drain in Mornington today?",
             "Wherever we can, yes. Mornington is close to our Somerville base, so call early and we'll do our best "
             "to get there the same day. Every clear finishes with a camera check."),
            ("Why does my drain keep blocking with roots?",
             "Because cutting the roots out doesn't seal the joint they came through, so they grow back. The camera "
             "shows how many joints are affected, so you can weigh up regular jetting against renewing the worst "
             "section of pipe."),
            ("Should I get the drain checked before I renovate?",
             "If the house is older, yes. A camera inspection before work starts shows whether the sewer line is "
             "sound or due for renewal, and renewing it while the yard is already open is far simpler than digging "
             "up new paving later."),
            ("Do you clear commercial drains in Mornington?",
             "Yes. We jet commercial and kitchen lines as well as homes, and the camera check afterwards confirms the "
             "grease is off the pipe wall, not just holed through."),
        ],
    },
    "rosebud": {
        "lede": ("Blocked toilet, a slow shower, or the drains backing up the first weekend the house is full? We "
                 "clear blocked sewer, stormwater and sink drains in Rosebud with high-pressure jetting, then camera "
                 "the line to make sure it's properly clear."),
        "img": ("sewer-junction-trench-worker.jpg", 1201, 1600,
                "Worker beside a deep sewer trench on a Hoad Drainage site."),
        "what_h2": "Sand, roots and a busy summer",
        "what_paras": [
            "A lot of Rosebud is built on sand, and sand is hard on a drain. Where a joint in the line has cracked or "
            "shifted, sand washes in, settles, and catches everything that comes down after it. Add roots from the "
            "garden and grease from the kitchen, and a line can run slower for months before one busy weekend tips "
            "it over.",
            "We jet out the roots and the sand, scour the pipe wall, then camera the line end to end. That tells you "
            "whether it was a build-up worth clearing once, or a cracked joint that will keep letting sand in until "
            "it's fixed.",
        ],
        "what_list": [
            "High-pressure jetting for roots, sand and grease",
            "Sewer, stormwater and sink drains",
            "Camera check after every clear",
            "Footage you can send to an owner or agent",
            "Same day where possible",
        ],
        "local_img": ("hoad-vac-truck-street.jpg", 1600, 1066,
                      "Hoad Drainage branded truck parked on a suburban street."),
        "local_eyebrow": "Rosebud drains",
        "local_h2": "Holiday houses block when they fill up",
        "local_paras": [
            "Rosebud fills up over summer, and plenty of its houses sit empty for weeks between visits. A drain that "
            "was slowly closing up goes unnoticed in an empty house, then backs up the first time a full house is "
            "running showers, the dishwasher and the washing machine at once.",
            "If you own the place, or manage it for someone who does, we can send the camera footage after the "
            "clear, so whoever is paying for the work sees what was in the line without making the trip down.",
            "Rosebud is a longer run down the Peninsula from our Somerville base than Mornington or Frankston, so "
            "for a same-day job, call early in the day.",
        ],
        "quote": {"name": "Blake McCormack",
                  "text": "Jarryd and the team at Hoad Drainage cleared a blocked stormwater drain at our property in "
                          "Frankston using their jetting truck. Great communication, arrived on time and fixed the "
                          "issue quickly. Highly recommend."},
        "faqs": [
            ("Can you clear a blocked drain in Rosebud today?",
             "Wherever we can, yes. Rosebud is a longer run from our Somerville base than the towns closer in, so ring "
             "early in the day and we'll do our best to get there the same day."),
            ("Why does sand keep ending up in my drain?",
             "Sand gets in where a joint in the pipe has cracked or pulled apart. Jetting clears it out, but it will "
             "keep coming back until that joint is repaired. The camera shows exactly where it's getting in."),
            ("Can you check the drains at a holiday house before summer?",
             "Yes. A jet and camera check before the busy season finds a line that's closing up while the house is "
             "still empty, rather than on the first full weekend."),
            ("Is a blocked sewer my problem or South East Water's?",
             "It depends where the blockage is. South East Water is responsible for the sewer main, and the property "
             "owner for the drain on their side of the connection. If several houses in the street are backing up, "
             "call South East Water first. If it's only your house, it's almost always your line."),
        ],
    },
}

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
          <img width="@@IMG_W@@" height="@@IMG_H@@" src="assets/@@IMG@@" alt="@@IMG_ALT@@" loading="lazy">
        </div>
        <div class="svc-row__body">
          <p class="eyebrow">What we do</p>
          <h2>@@WHAT_H2@@</h2>
@@WHAT_BODY@@
          <ul class="svc-row__list" role="list">
@@WHAT_LIST@@
          </ul>
          <a class="btn btn--primary" href="contact">Book a drain clear</a>
        </div>
      </article>@@LOCAL_ROW@@
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
        <a class="related__card" href="cctv-drain-inspections-@@SLUG@@">
          <span class="related__num">01</span>
          <span>
            <h3>CCTV Drain Inspections</h3>
            <p>Camera survey to find exactly what's blocking the line and why.</p>
          </span>
        </a>
        <a class="related__card" href="non-destructive-digging">
          <span class="related__num">03</span>
          <span>
            <h3>Non-Destructive Digging</h3>
            <p>Vac truck excavation to safely expose a @@DISPLAY@@ drain for repair.</p>
          </span>
        </a>
        <a class="related__card" href="sewer-stormwater-drainage">
          <span class="related__num">04</span>
          <span>
            <h3>Sewer &amp; Stormwater</h3>
            <p>Renewals and repairs when a blockage turns out to be a broken pipe.</p>
          </span>
        </a>
        <a class="related__card" href="@@CIVIL@@">
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
        <a class="btn btn--pill btn--primary btn--pill-icon" href="contact">
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
        cols[col].append(f'            <li><a href="blocked-drains-{slug}">{disp}</a></li>')
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
    if s["slug"] in LOCAL:
        qa = LOCAL[s["slug"]]["faqs"]
    # JSON-LD (answers carry no double quotes once links are stripped, so they are safe to inline)
    json_items = []
    for q, a in qa:
        a_text = re.sub(r"<[^>]+>", "", a)
        assert '"' not in a_text and '"' not in q, f"double quote in FAQ copy for {d}"
        json_items.append(
            '    {\n'
            '      "@type": "Question",\n'
            f'      "name": "{q}",\n'
            '      "acceptedAnswer": {"@type": "Answer", "text": "' + a_text + '"}\n'
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
    page_url = f"{BASE}/blocked-drains-{slug}"
    if s.get("hub"):
        hub_url = f"{BASE}/{s['hub']}"
        bc = (
            f'    {{"@type": "ListItem", "position": 1, "name": "Home", "item": "{BASE}/"}},\n'
            f'    {{"@type": "ListItem", "position": 2, "name": "{d}", "item": "{hub_url}"}},\n'
            f'    {{"@type": "ListItem", "position": 3, "name": "Blocked Drains & Jetting", "item": "{page_url}"}}'
        )
        crumbs = (
            '      <a href="/">Home</a>\n'
            '      <span class="crumbs__sep" aria-hidden="true">/</span>\n'
            f'      <a href="{s["hub"]}">{d}</a>\n'
            '      <span class="crumbs__sep" aria-hidden="true">/</span>\n'
            '      <span aria-current="page">Blocked Drains &amp; Jetting</span>'
        )
    else:
        bc = (
            f'    {{"@type": "ListItem", "position": 1, "name": "Home", "item": "{BASE}/"}},\n'
            f'    {{"@type": "ListItem", "position": 2, "name": "Blocked Drains & Jetting", "item": "{BASE}/blocked-drains-jetting"}},\n'
            f'    {{"@type": "ListItem", "position": 3, "name": "{d}", "item": "{page_url}"}}'
        )
        crumbs = (
            '      <a href="/">Home</a>\n'
            '      <span class="crumbs__sep" aria-hidden="true">/</span>\n'
            '      <a href="blocked-drains-jetting">Blocked Drains &amp; Jetting</a>\n'
            '      <span class="crumbs__sep" aria-hidden="true">/</span>\n'
            f'      <span aria-current="page">{d}</span>'
        )
    return bc, crumbs


DEFAULT_WHAT_BODY = """          <p>
            High-pressure water jetting cuts through the grease, roots and debris that a plunger or a snake won't shift, and scours the pipe wall clean instead of just punching a hole through the blockage. Then we camera the line to confirm it's clear and show you what caused it. @@ANGLE@@ It's the same <a href="blocked-drains-jetting">blocked drain and jetting service</a> we run right across @@REGION@@, here in @@DISPLAY@@.
          </p>"""
DEFAULT_WHAT_LIST = [
    "High-pressure water jetting",
    "Tree-root cutting and grease removal",
    "Sewer, stormwater and sink drains",
    "Camera check after clearing",
    "Same-day service where possible",
]
# One photo serves every templated page, so its alt must not name a suburb: the old
# "...along a fence line in <Suburb>." claimed the same shot was taken in 12 places.
DEFAULT_IMG = ("crew-drainage-pit-fenceline.jpg", 1400, 933,
               "Hoad Drainage crew working on a drain along a fence line.")


def paras(ps, indent="          "):
    return "\n".join(f"{indent}<p>\n{indent}  {p}\n{indent}</p>" for p in ps)


def local_row(loc):
    """The second, suburb-specific svc-row on a rewritten page (see LOCAL below)."""
    img, w, h, alt = loc["local_img"]
    q = loc["quote"]
    quote_text = " ".join(q["text"].split())
    return (
        "\n\n"
        '      <article class="svc-row svc-row--reverse">\n'
        '        <div class="svc-row__media">\n'
        f'          <img width="{w}" height="{h}" src="assets/{img}" alt="{alt}" loading="lazy">\n'
        '        </div>\n'
        '        <div class="svc-row__body">\n'
        f'          <p class="eyebrow">{loc["local_eyebrow"]}</p>\n'
        f'          <h2>{loc["local_h2"]}</h2>\n'
        f'{paras(loc["local_paras"])}\n'
        '          <blockquote class="svc-quote">\n'
        f'            <p>&ldquo;{quote_text}&rdquo;</p>\n'
        f'            <cite>{q["name"]}, Google review</cite>\n'
        '          </blockquote>\n'
        '        </div>\n'
        '      </article>'
    )


def build(s):
    d = s["display"]
    slug = s["slug"]
    loc = LOCAL.get(slug)
    nearby = s.get("nearby")
    near_and = f" and {nearby}" if nearby else ""
    region = s.get("region", "the Peninsula")
    canon = f"{BASE}/blocked-drains-{slug}"

    # SERP copy. The first version ("Blocked Drains in X | Hoad Drainage") ranked on
    # page 1 for 12 suburbs and drew 0 clicks from 1,451 impressions in 28 days: it
    # matched the query and gave no reason to pick it over the map pack and the ads.
    # The rewrite (2026-09-15) mirrors the searcher's problem as a question, then
    # sells the two things a franchise call centre can't: a local crew and camera
    # proof the line is clear. The brand is dropped from the title because Google
    # already prints the site name above it. Frankston is hand-built, so patch its
    # <title> and description to the same pattern when this changes.
    title = f"Blocked Drain in {d}? Jetted Clear, Camera Checked"
    if s.get("home_base"):
        crew = "a crew based right here in town"
    else:
        crew = "a local Somerville crew"
    desc = (f"Blocked drains in {d} jetted clear by {crew}, same day where possible, "
            "then camera checked to prove it. Call (03) 5978 0120.")
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
        footnote = ('See our full range of <a href="services">drainage services</a> across ' + region + ', '
                    'or call <a href="tel:0359780120">(03) 5978 0120</a>.')

    img, img_w, img_h, img_alt = DEFAULT_IMG
    what_h2 = f"{d} blockages, cleared properly"
    what_body = DEFAULT_WHAT_BODY
    what_list = DEFAULT_WHAT_LIST
    local_html = ""
    if loc:
        lede = loc["lede"]
        img, img_w, img_h, img_alt = loc["img"]
        what_h2 = loc["what_h2"]
        what_body = paras(loc["what_paras"])
        what_list = loc["what_list"]
        local_html = local_row(loc)
    what_list_html = "\n".join(f"            <li>{li}</li>" for li in what_list)

    faq_json, faq_html = faq_blocks(s)
    bc_json, crumbs = breadcrumb(s)

    if len(title) > 60:
        print(f"  WARN title {len(title)} chars: {title}")
    if len(desc) > 160:
        print(f"  WARN description {len(desc)} chars: {slug}")

    out = PAGE
    repl = {
        # body blocks first: the default body carries @@ANGLE@@/@@REGION@@/@@DISPLAY@@,
        # which the later keys resolve
        "@@WHAT_BODY@@": what_body,
        "@@WHAT_LIST@@": what_list_html,
        "@@WHAT_H2@@": what_h2,
        "@@LOCAL_ROW@@": local_html,
        "@@IMG@@": img,
        "@@IMG_W@@": str(img_w),
        "@@IMG_H@@": str(img_h),
        "@@IMG_ALT@@": img_alt,
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
        "@@CIVIL@@": s.get("civil", "civil-commercial-drainage"),
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
