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
        for key, value in vals.items():
            if key in ("asset_prefix", "TITLE", "META_DESC", "CANONICAL", "REVIEW_ORDER"):
                continue
            html = html.replace("{" + key + "}", value)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html)
        left = [t for t in ("{H1}", "{LEDE}", "{Q1}") if t in html]
        print(f"built {path.relative_to(HERE.parent)}  {len(html)/1024:.0f} KB  unresolved={left}")


if __name__ == "__main__":
    main()
