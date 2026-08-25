#!/usr/bin/env python3
"""Build the paid landing pages from template.html + styles.css.

Two pages, one template: the blocked-drain LP lives here, the CCTV LP is
written into ../cctv-drain-quote/. CSS is inlined, fonts and images are
shared from this folder (the CCTV page links back to ../blocked-drain-quote/
for both), so there is one copy of each asset on the origin.

Run after editing template.html or styles.css:  python3 build.py
"""
import html as html_lib
import json
import pathlib

HERE = pathlib.Path(__file__).parent
CCTV = HERE.parent / "cctv-drain-quote"

def work_cards(items, prefix=""):
    """Captioned job photos. Captions describe what is in the frame and nothing
    more - no suburb claims, no invented job stories. Same rule as the main
    site's gallery captions."""
    out = []
    for img, w, h, alt, cap in items:
        out.append(
            '      <li><figure>\n'
            f'        <img src="{prefix}img/{img}" alt="{alt}" width="{w}" height="{h}" loading="lazy">\n'
            f'        <figcaption>{cap}</figcaption>\n'
            '      </figure></li>'
        )
    return "\n".join(out)


def faq_items(items):
    out = []
    for i, (q, a) in enumerate(items):
        open_attr = " open" if i == 0 else ""
        out.append(f'      <details{open_attr}><summary>{q}</summary><p>{a}</p></details>')
    return "\n".join(out)


LICENSED = ("Are you licensed?",
            "Yes. We are licensed under the Victorian Building Authority for sewerage and stormwater drainage, licence 50192. "
            "We notify the VBA on every job and issue a Certificate of Compliance on completion, so it lands in the property file properly.")
WHO = ("Who do you work for?",
       "Homeowners, builders and property managers. We are a family run drainage and civil crew out of Somerville, "
       "members of Master Plumbers Australia and the Civil Contractors Federation Victoria.")
COST = ("What will it cost?",
        "$480 + GST covers the call-out and the first hour on site with the jetter and camera, then $190 + GST per hour after that. "
        "Most blockages are cleared within two to three hours. Anything that needs repair is quoted separately before we do it.")

WORK_BLOCKED = [
    ("vactruck-600.webp", 600, 400, "Hoad vac truck on site with an operator working the suction lance",
     "Vac truck on site. Digging by suction, not by blade, when there are live services in the ground."),
    ("jetting-600.webp", 600, 900, "Hoad crew working at a manhole connection",
     "Working a manhole connection. Access through an existing point beats digging to find the fault."),
    ("repair-600.webp", 600, 795, "Excavated pit showing an old pipe section re-laid and bedded in concrete",
     "What sits under a repeat blockage. Failed section exposed, re-laid and bedded in concrete."),
    ("pipework-600.webp", 600, 800, "Hoad worker fitting a PVC junction in a trench",
     "New junction going in. Levels checked before anything gets covered back over."),
]
WORK_CCTV = [
    ("jetting-600.webp", 600, 900, "Hoad crew working at a manhole connection",
     "Camera goes in through an existing access point. No digging to find the fault."),
    ("repair-600.webp", 600, 795, "Excavated pit showing an old pipe section re-laid and bedded in concrete",
     "The kind of thing the camera finds. A failed section, located before anyone dug for it."),
    ("pipework-600.webp", 600, 800, "Hoad worker fitting a PVC junction in a trench",
     "Once we know where the fault is, the repair is a targeted dig rather than a search."),
    ("vacwork-600.webp", 600, 400, "Hoad vac truck operator working beside the truck",
     "Vac truck for exposing a located line without putting a bucket through it."),
]

PAGES = {
    HERE / "index.html": {
        "asset_prefix": "",
        "TITLE": "Blocked Drain Cleared, Usually Same Day | Hoad Drainage &amp; Excavations",
        "META_DESC": "Blocked drains cleared with high-pressure jetting and a camera check, across the Mornington Peninsula and South East Melbourne. VBA licensed, family run from Somerville. $480 + GST call-out including the first hour on site.",
        "CANONICAL": "https://hoaddrainage.com.au/blocked-drains-jetting.html",
        "H1": "Blocked drain cleared, usually the same day.",
        "LEDE": "High-pressure jetting to clear it, then a camera through the line so you know what caused it and whether it is coming back. Across the Mornington Peninsula and South East Melbourne.",
        "ANCHOR_CTA": "Get a price",
        "URGENT": "Water rising right now? Calling is faster than the form.",
        "SUBJECT": "New blocked drain enquiry - hoaddrainage.com.au",
        "SERVICE": "blockage",
        "REQUEST_TYPE": "Booking",
        "FORM_TITLE": "Get a blocked drain sorted",
        "FORM_SUB": "Tell us what it is doing and we will come back the same business day with a time.",
        "MESSAGE_LABEL": "What is happening?",
        "PLACEHOLDER": "e.g. toilet backing up, gurgling in the shower, water pooling near the tank",
        "SUBMIT": "Send it through",
        "FORM_NOTE": "$480 + GST call-out, including the first hour on site with the jetter and camera. $190 + GST per hour after that.",
        "PROCESS_HEAD": "How a blocked drain job runs",
        "PROCESS_LEDE": "Clearing a blockage is the easy part. Knowing why it blocked is what stops you paying for it again in three months.",
        "S1H": "We get to you", "S1P": "Call early and we will do our best to be there the same business day. You get a time, not a four hour window and a shrug.",
        "S2H": "We jet it clear", "S2P": "High-pressure jetting cuts through roots, fat and debris and scours the pipe wall properly, rather than punching a hole through the middle of the blockage.",
        "S3H": "The camera confirms it", "S3P": "We run the camera through the cleared line so you can see it is actually clear, and see anything underneath the blockage that caused it. Cracks, root intrusion, a collapsed section.",
        "Q1": "Do you clear blocked drains the same day?",
        "A1": "Wherever we can, yes. Call us early and we will do our best to get to a blockage the same day. We clear it with high-pressure jetting, then run a camera through to confirm it is clear and show what caused it.",
        "REVIEW_ORDER": ["Blake McCormack", "aaron", "Chris Cleef"],
        "WORK_HEAD": "On the tools",
        "WORK_LEDE": "Jetting and camera work is most of the week. The gear below is ours, not hired in, which is why we can usually get to a blockage the same day.",
        "WORK_ITEMS": WORK_BLOCKED,
        "FAQ_ITEMS": [
            ("Do you clear blocked drains the same day?",
             "Wherever we can, yes. Call us early and we will do our best to get to a blockage the same day. We clear it with high-pressure jetting, then run a camera through to confirm it is clear and show what caused it."),
            ("What is high-pressure jetting?",
             "Jetting uses a high-pressure water hose to cut through grease, tree roots and debris and flush the line clean. It clears blockages a plunger or a snake will not shift, and it scours the pipe wall rather than just punching a hole through the blockage."),
            ("Will the blockage just come back?",
             "That depends on what caused it. After we clear the line we run a camera through to see whether it was a one-off or a bigger problem like root intrusion or a broken pipe. If it is structural we will show you and talk through a lasting fix, so you are not paying to clear the same drain every few months."),
            ("What drains can you clear?",
             "Sewer, stormwater and sink drains at homes, units and commercial sites. Blocked toilets, gurgling drains, water backing up in the yard, slow-draining sinks and showers, we clear the lot."),
            COST, LICENSED, WHO,
        ],
        "FINAL_HEAD": "Drain backing up? Let's clear it.",
        "FINAL_P": "Call the office and we will do our best to get to you the same business day. If it is not urgent, send the form through and we will come back with a time and a price.",
    },
    CCTV / "index.html": {
        "asset_prefix": "../blocked-drain-quote/",
        "TITLE": "CCTV Drain Inspections, Footage and a Report | Hoad Drainage &amp; Excavations",
        "META_DESC": "CCTV drain inspections across the Mornington Peninsula and South East Melbourne. Camera footage plus a written report for insurance, pre-purchase checks and recurring blockages. VBA licensed, family run from Somerville.",
        "CANONICAL": "https://hoaddrainage.com.au/cctv-drain-inspections.html",
        "H1": "See what is actually in the drain.",
        "LEDE": "A camera through the line, recorded, with a written report you can act on. For recurring blockages, pre-purchase checks and insurance claims across the Peninsula and South East Melbourne.",
        "ANCHOR_CTA": "Book an inspection",
        "URGENT": "Not sure whether you need a camera or a clear? Ring and describe it, we will tell you straight.",
        "SUBJECT": "New CCTV drain inspection enquiry - hoaddrainage.com.au",
        "SERVICE": "cctv",
        "REQUEST_TYPE": "Booking",
        "FORM_TITLE": "Book a drain inspection",
        "FORM_SUB": "Tell us what you need it for and we will come back the same business day with a time.",
        "MESSAGE_LABEL": "What do you need it for?",
        "PLACEHOLDER": "e.g. drain blocks every few months, buying a house, need a report for an insurance claim",
        "SUBMIT": "Send it through",
        "FORM_NOTE": "$480 + GST call-out, including the first hour on site with the camera and jetter. $190 + GST per hour after that.",
        "PROCESS_HEAD": "How a CCTV inspection runs",
        "PROCESS_LEDE": "You are paying to stop guessing. So you get the footage and a written rundown, not a verbal opinion at the gate.",
        "S1H": "Camera through the line", "S1P": "We feed the camera through the drain and record the whole run, so nothing depends on anyone's memory of what they saw.",
        "S2H": "We locate the problem", "S2P": "Blockages, cracks, root intrusion, collapsed sections and misaligned joints, found and located without digging up the yard to look for them.",
        "S3H": "You get it in writing", "S3P": "A clear rundown of what is going on and where, with the footage. Enough to hand to an insurer, a conveyancer or the next trade.",
        "Q1": "What does a camera inspection involve?",
        "A1": "We feed a camera through the drain and record the run, so we can see blockages, cracks, root intrusion or collapsed sections without digging. You get a clear rundown of what is going on and where, plus the footage.",
        "REVIEW_ORDER": ["Ben Rahilly", "aaron", "Tim Scott"],
        "WORK_HEAD": "What the camera is for",
        "WORK_LEDE": "The camera is ours and it goes out most days, usually alongside the jetter. Finding the fault is the job; digging is what happens after you know where it is.",
        "WORK_ITEMS": WORK_CCTV,
        "FAQ_ITEMS": [
            ("What does a CCTV drain inspection involve?",
             "We feed a camera through the drain and record the run, so we can see blockages, cracks, root intrusion or collapsed sections without digging. You get a clear rundown of what is going on, and where needed a written report with photos and footage, plus the location and depth of the problem."),
            ("Do I get a report with the inspection?",
             "Where you need one, yes. We can supply a written report with photos and footage for a sale, a builder or your own records. Just let us know when you book so we bring the right gear and set aside the time."),
            ("Can you find where the drain runs and how deep it is?",
             "Yes. The camera carries a locator so we can mark the line and depth from above ground. That is useful before you dig, landscape or build over a drain."),
            ("Do I need to dig anything up for the camera?",
             "No, that is the point of a CCTV inspection. We access the drain through an existing point such as an inspection opening, gully or pit, so there is no digging to find the fault."),
            COST, LICENSED, WHO,
        ],
        "FINAL_HEAD": "Want to know what is down there?",
        "FINAL_P": "Send the form through and we will come back the same business day with a time and a price for the inspection. If it is urgent, calling is faster.",
    },
}


def review_cards(order):
    """Real Google reviews, rendered statically. No Elfsight, no third-party JS.

    Cached in reviews.json, pulled from their Business Profile (cid
    6920814491620276121) via Serper. Text is verbatim - never edit a review.
    Refresh by re-running the Serper reviews pull when the count moves.
    """
    data = json.loads((HERE / "reviews.json").read_text())
    by_name = {r["name"]: r for r in data["reviews"]}
    cards = []
    for name in order:
        r = by_name[name]
        stars = "&#9733;" * int(float(r["rating"]))
        cards.append(
            '      <li class="rev">\n'
            f'        <div class="rev__stars" aria-label="{r["rating"]} out of 5">{stars}</div>\n'
            f'        <p>{html_lib.escape(r["text"])}</p>\n'
            f'        <p class="rev__by"><b>{html_lib.escape(r["name"])}</b> &middot; {r["date"]} &middot; Google review</p>\n'
            '      </li>'
        )
    return "\n".join(cards)


def main():
    template = (HERE / "template.html").read_text()
    css = (HERE / "styles.css").read_text()
    for path, vals in PAGES.items():
        html = template.replace("/*STYLES*/", css)
        prefix = vals["asset_prefix"]
        if prefix:
            # shared fonts, images and stylesheet live in blocked-drain-quote/,
            # so both the href/src attributes and the url() references inside the
            # inlined CSS have to be rewritten
            for folder in ("img/", "fonts/"):
                html = html.replace('"' + folder, '"' + prefix + folder)
                html = html.replace("url('" + folder, "url('" + prefix + folder)
        html = html.replace("<title>Blocked Drain Cleared, Usually Same Day | Hoad Drainage &amp; Excavations</title>",
                            "<title>" + vals["TITLE"] + "</title>")
        html = html.replace('content="Blocked drains cleared with high-pressure jetting and a camera check, across the Mornington Peninsula and South East Melbourne. VBA licensed, family run from Somerville. $480 + GST call-out including the first hour on site."',
                            'content="' + vals["META_DESC"] + '"')
        html = html.replace('href="https://hoaddrainage.com.au/blocked-drains-jetting.html"',
                            'href="' + vals["CANONICAL"] + '"')
        html = html.replace("{REVIEWS}", review_cards(vals["REVIEW_ORDER"]))
        html = html.replace("{GALLERY}", work_cards(vals["WORK_ITEMS"], prefix))
        html = html.replace("{FAQS}", faq_items(vals["FAQ_ITEMS"]))
        for key, value in vals.items():
            if key in ("asset_prefix", "TITLE", "META_DESC", "CANONICAL", "REVIEW_ORDER",
                       "WORK_ITEMS", "FAQ_ITEMS"):
                continue
            html = html.replace("{" + key + "}", value)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html)
        left = [t for t in ("{H1}", "{LEDE}", "{Q1}") if t in html]
        print(f"built {path.relative_to(HERE.parent)}  {len(html)/1024:.0f} KB  unresolved={left}")


if __name__ == "__main__":
    main()
