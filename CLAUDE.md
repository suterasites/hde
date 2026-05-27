# CLAUDE.md - Hoad Drainage & Excavations Mockup

Prospect mockup. Somerville VIC (Mornington Peninsula) sewer + stormwater drainage and excavation contractor. Cold IG/FB outreach by Christian Bitsikas 2026-05-27 - bad website pitch landed, prospect accepted free mockup. Christian's read on current site: "pretty average." Rebuild is the wedge.

## Canonical references (read first)

- **Prospect profile**: [../../../CRM/prospects/Hoad Drainage & Excavations/profile.md](../../../CRM/prospects/Hoad%20Drainage%20%26%20Excavations/profile.md)
- **Status + pipeline**: [../../../CRM/prospects/Hoad Drainage & Excavations/status.md](../../../CRM/prospects/Hoad%20Drainage%20%26%20Excavations/status.md)
- **Notes (background, gotchas, leverage)**: [../../../CRM/prospects/Hoad Drainage & Excavations/notes.md](../../../CRM/prospects/Hoad%20Drainage%20%26%20Excavations/notes.md)
- **Comms log**: [../../../CRM/prospects/Hoad Drainage & Excavations/communications/interaction-log.md](../../../CRM/prospects/Hoad%20Drainage%20%26%20Excavations/communications/interaction-log.md)
- **Sales rep**: Christian Bitsikas <chbitsi@gmail.com>
- **GitHub repo**: git@github.com:suterasites/hde.git (deployed branch: `main`, initial push 2026-05-27)

## Source material (pull before designing)

- **Live site**: https://hoaddrainage.com.au/ (current build, target to beat)
- **Instagram**: https://www.instagram.com/hoaddrainage_excavations/ (289 posts, 1,614 followers, verified - rich source for job photos, brand voice, services list)
- **Google Business Profile**: "Hoad Drainage and Excavations" - Drainage service category, 5 Arduina St Somerville VIC 3912, phone (03) 5978 0120, hours Mon-Fri 6:30am opening
- **CCFV member listing**: Civil Contractors Federation Victoria - signals B2B/civil credibility, secondary mobile 0402 066 506
- **Bio email**: jarryd@hoaddrainage.com.au (owner contact likely Jarryd - confirm before personalising any direct copy)

## Services to surface (from IG bio + GBP)

- Sewer and Stormwater Drains (positioned first - the headline specialty)
- Site Cuts
- Unit Developments
- Civil Works
- KDR (Knock Down Rebuild) - Cap & Seals

Audience leans B2B: builders, developers, civil contractors needing drainage subcontractor on KDR + new builds. Not a residential plumber. Copy should respect that.

## Brand rules (to verify when pulling assets)

- **Name**: "Hoad Drainage & Excavations" (ampersand, plural Excavations). NOT "Hoad Drainage and Excavations" in display copy (GBP uses "and" but IG and the logo use "&"). Confirm logo lockup before designing.
- **Logo**: Word mark with stylised "O" in HOAD - confirm vector source from Jarryd before launch (IG profile pic is a JPG, not production-grade).
- **Colours**: Logo uses dark blue/teal + light cyan on white. Extract exact hex from logo SVG/PSD when sourced. Do not approximate without confirmation.
- **Phone display**: Use mobile 0402 066 506 OR landline (03) 5978 0120 - confirm with Jarryd which is the preferred lead-capture number.
- **No fake testimonials or fabricated review counts**. Pull real reviews from GBP if any exist.
- **No personal/family claims**. Christian's outreach relationship is the only context - keep copy neutral.

## Tech stack

- Vanilla HTML / CSS / JS, no framework
- Single-page mockup (`index.html`), scroll-anchored sections
- Google Fonts: Archivo (display, 500-800) + Inter (body, 400-600)
- Schema.org JSON-LD: `Plumber` type with full NAP + opening hours
- Form: mock contact form with JS no-op submit (replace with Formspree on launch)

## Design system (CSS custom properties in styles.css)

- `--ink: #0A1F2E` - deep navy near-black for dark sections, body text
- `--ink-soft: #1A3445` - secondary dark
- `--ink-mute: #4F6675` - body copy on light bg
- `--cyan: #38B6C5` - primary accent (CTAs, eyebrow on dark, hover lines, trust stamps). Pulled from logo "O" sphere.
- `--cyan-dark: #1A6F7D` - hover state, links on light bg, eyebrow on light
- `--cyan-soft: #C7E8ED` - input focus ring, card hover borders
- `--bone: #F6F4F0` - warm off-white for alternating section backgrounds (services, area)
- `--paper: #FFFFFF` - card backgrounds, default
- Container: 1200px max, 1.5rem mobile / 2.5rem tablet+ gutter

## Coding conventions (Sutera Sites global)

- **No em dashes** anywhere - hyphens, commas, periods only
- Date format: YYYY-MM-DD
- Folder name = exact business name with spaces ("Hoad Drainage & Excavations"), match across CRM + Websites
- Comments only where the WHY is non-obvious
- All images: lazy-load below the fold, eager only on hero
- Respect `prefers-reduced-motion`

## Page structure (in render order)

1. **Header** - sticky white bar. Brand lockup (logo circle + HOAD wordmark + tag), primary nav, phone CTA button. Mobile collapses to hamburger.
2. **Hero** - full-bleed aerial site-cut photo with navy gradient veil. Eyebrow ("Mornington Peninsula and Greater Melbourne"), big two-line headline, lede, dual CTAs ("Request a quote" + tel link), trust bar (VBA / Master Plumbers / CCFV / Somerville Based).
3. **Services (`#services`)** - bone-toned section. Featured card (Sewer & Stormwater Drains, dark + compliance bullets) spans 4 cols at md+. Four secondary cards (Site Cuts / Unit Developments / Civil Works / KDR Cap & Seals).
4. **Recent Work (`#work`)** - photo grid. Mobile single column, desktop 3-col with one --tall (col 1 spans 2 rows) and one --wide (spans 2 cols). Captions overlay bottom with gradient.
5. **About (`#about`)** - dark navy section. Two-col on desktop: copy + 3 trust metrics on left (VBA / CCFV / MPA), crew portrait photo on right.
6. **Service Area (`#area`)** - bone section. Copy + suburb pill list on left, vertical excavator photo panel on right.
7. **Contact (`#contact`)** - dark navy section. Left: copy + labelled detail list (phone / mobile / email / office / hours). Right: white "Request a quote" form card.
8. **Footer** - very dark navy. Brand lockup + services/contact columns, base bar with copyright + Sutera Sites credit.

## Mockup build status: BUILT - ready for internal review

- `index.html` (~410 lines): all sections complete with copy, semantic markup, ARIA, schema.org JSON-LD
- `styles.css` (~880 lines): full design system, all components, mobile-first responsive
- `script.js` (~90 lines): mobile nav toggle, footer year, hero video reduced-motion handling, recent-work carousel (prev/next/dots/swipe/arrow keys), mock form submit
- All 13 assets wired in (12 photos + logo + reel).
  - Hero uses `reel-jobsite-overview.mp4` as autoplay/muted/loop background, with `aerial-site-cut-suburban-block.jpg` as poster for instant first paint and reduced-motion fallback.
  - Recent Work section is a single-image carousel (dark navy backdrop) cycling through the 6 install/site-cut photos. CTA below links to Instagram.

## Recent design changes (2026-05-27)

- Recent Work converted from 6-tile grid to a single-image carousel on a dark navy backdrop, matching the reference James shared. Side-arrow controls, dot pagination (active dot stretches to a pill), keyboard arrows + touch swipe. CTA `[See more recent work] -> Instagram`.
- Hero backdrop swapped from a static aerial photo to the looped jobsite reel video. Poster image preserved for first paint + `prefers-reduced-motion` fallback.
- Reel cropped from 31.4s -> 20s using AVFoundation (Swift script in `/tmp/crop-video.swift`, no ffmpeg required). File size: 9.7MB -> 6.5MB. Still heavier than ideal for production (see launch checklist).

## Copy assumptions to verify with Christian before sending

- **Owner name spelling**: copy uses "Jarryd" (matches bio email) but team polo reads "Jarrod M". Schema uses no first name. Confirm canonical before sending.
- **Phone numbers**: Hero + header use landline (03) 5978 0120, contact section also lists mobile 0402 066 506. Confirm Jarryd's preferred lead-capture number.
- **VBA / Master Plumbers / CCFV memberships**: claimed in hero trust bar + about section. Sourced from current site copy and CCFV member directory. Verify all three are current.
- **Service area suburbs**: list is a reasonable Mornington-Peninsula-plus-SE-Melbourne assumption. Confirm Jarryd's actual catchment.
- **"Family-run"** wording in about heading: confirm not a stretch (multiple Hoad relatives implied by surname-as-brand, but not verified).
- **"Same business day" reply commitment** in contact section: confirm Jarryd can actually meet this SLA.

## Production-ready checklist (before launch)

- [ ] Replace mock form submit with Formspree (Sutera Sites default endpoint)
- [ ] Request hi-res SVG logo from Jarryd (current PNG is good to ~50px)
- [ ] Precompile + inline critical CSS, self-host Inter + Archivo woff2 (per `[[feedback_landing_page_tailwind_cdn]]` for production sites)
- [ ] Compress JPGs, generate WebP + responsive srcset
- [ ] Transcode hero reel for web: target H.264 baseline ~1.5-2.5MB at 720p + WebM alternate source. Currently 6.5MB H.264 (cropped from raw IG download). Add `<source>` fallbacks rather than single `src=`.
- [ ] Consider a dedicated wide hero shot (still) as a secondary asset for hero `poster` once a real photographer pass happens
- [ ] Add Google Analytics 4 measurement ID
- [ ] sitemap.xml + robots.txt
- [ ] Schema.org review counts once real GBP reviews exist
- [ ] Confirm exact lat/lng for Somerville office, currently approximate (-38.2363, 145.1722)
- [ ] Lighthouse pass: 90+ on all four scores (hero video will pull LCP down - measure with poster + lazy-promote video after first paint if needed)
- [ ] DNS cutover plan from current Cloudways WooCommerce host
