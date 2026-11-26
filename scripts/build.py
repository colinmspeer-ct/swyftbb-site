#!/usr/bin/env python3
"""Generate the static HTML pages for the Swyft Business Broker site.

Usage (from the repo root):  python3 scripts/build.py

Writes index.html, sellers/, buyers/, about/, contact/, privacy/, 404.html,
sitemap.xml and robots.txt at the repo root. The output is committed, so
GitHub Pages serves it as-is. No dependencies beyond the Python 3 stdlib.

All internal links and asset paths are relative so the site works on the
GitHub Pages project preview (https://colinmspeer-ct.github.io/swyftbb-site/).
Canonical, og:url and sitemap URLs use SITE_URL below.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_URL = "https://swyftbb.com/"  # production intent host; change here and rebuild if needed
YEAR = "2026"
LASTMOD = "2026-11-25"
EMAIL = "colin@swyft-hq.com"
PHONE_DISPLAY = "267-606-8667"
PHONE_TEL = "+12676068667"
PHONE_LD = "+1-267-606-8667"
HQ = "https://swyft-hq.com/"
HQ_HOW = "https://swyft-hq.com/how-it-works/"
HQ_IND = "https://swyft-hq.com/industries/"
HQ_INTL = "https://swyft-hq.com/international/"
HQ_ABOUT = "https://swyft-hq.com/about/"
INTL_SITE = "https://swyftinternational.com/"
OG_IMAGE = SITE_URL + "assets/og-image.png"

INDUSTRIES = [
    ("Exteriors and roofing", "exteriors"),
    ("Window cleaning", "window-cleaning"),
    ("Pest control", "pest-control"),
    ("Lawn care", "lawn-care"),
    ("Fiber internet and wireless", "fiber-internet"),
    ("Interior home improvement", "interior-home-improvement"),
    ("Home security", "home-security"),
    ("Water treatment", "water-treatment"),
    ("HVAC", "hvac"),
]

ORG_ID = SITE_URL + "#org"
WEBSITE_ID = SITE_URL + "#website"

ARROW = '<span class="ico" aria-hidden="true">&#8599;</span>'


def ind_url(slug):
    return f"{HQ_IND}{slug}/"


def industry_chips():
    items = "\n".join(
        f'          <li><a href="{ind_url(s)}">{n}</a></li>' for n, s in INDUSTRIES
    )
    return f'        <ul class="chips">\n{items}\n          <li><a href="{HQ_IND}">All Swyft HQ industries</a></li>\n        </ul>'


NAV = [
    ("Sellers", "sellers/"),
    ("Buyers", "buyers/"),
    ("About", "about/"),
    ("Contact", "contact/"),
]


def header(r, current):
    def cur(href):
        return ' aria-current="page"' if href == current else ""

    desk = "\n".join(
        f'            <li><a href="{r}{h}"{cur(h)}>{n}</a></li>' for n, h in NAV
    )
    mob = "\n".join(
        f'                <li><a href="{r}{h}"{cur(h)}>{n}</a></li>' for n, h in NAV
    )
    return f"""  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="wrap header-inner">
      <a class="logo" href="{r or './'}" aria-label="Swyft Business Broker home">
        <img src="{r}assets/logo-white.svg" alt="Swyft" width="139" height="22">
        <span class="logo-sub">Business Broker</span>
      </a>
      <nav class="nav-desktop" aria-label="Main">
        <ul>
{desk}
        </ul>
      </nav>
      <div class="header-actions">
        <a class="header-phone" href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>
        <a class="btn btn-sm" href="{r}contact/">Talk to Colin</a>
        <details class="nav-mobile">
          <summary aria-label="Open menu"><span></span><span></span><span></span></summary>
          <nav aria-label="Mobile">
            <ul>
              <li><a href="{r or './'}">Home</a></li>
{mob}
              <li><a href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a></li>
              <li><a class="nav-cta" href="{HQ}">Swyft HQ</a></li>
            </ul>
          </nav>
        </details>
      </div>
    </div>
  </header>"""


def footer(r):
    return f"""  <footer class="site-footer">
    <div class="wrap foot-grid">
      <div class="foot-brand">
        <a class="logo" href="{r or './'}" aria-label="Swyft Business Broker home">
          <img src="{r}assets/logo-white.svg" alt="Swyft" width="164" height="26">
          <span class="logo-sub">Business Broker</span>
        </a>
        <p>A value-added business broker. We help owners raise value before a sale and help buyers grow after the purchase, with the growth work done by Swyft HQ.</p>
      </div>
      <div>
        <p class="foot-title">Site</p>
        <ul>
          <li><a href="{r}sellers/">Sellers</a></li>
          <li><a href="{r}buyers/">Buyers</a></li>
          <li><a href="{r}about/">About</a></li>
          <li><a href="{r}contact/">Contact</a></li>
        </ul>
      </div>
      <div>
        <p class="foot-title">Swyft</p>
        <ul>
          <li><a href="{HQ}">Swyft HQ</a></li>
          <li><a href="{HQ_HOW}">How Swyft HQ works</a></li>
          <li><a href="{HQ_IND}">Industries</a></li>
          <li><a href="{HQ_INTL}">Swyft International</a></li>
          <li><a href="{INTL_SITE}">swyftinternational.com</a></li>
        </ul>
      </div>
      <div>
        <p class="foot-title">Contact</p>
        <ul>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
          <li><a href="{r}privacy/">Privacy</a></li>
        </ul>
      </div>
    </div>
    <div class="wrap foot-legal">
      <p>&copy; {YEAR} Swyft Solutions LLC. Swyft Business Broker is an offer of Swyft Solutions LLC.</p>
    </div>
  </footer>"""


def head(r, title, desc, url, noindex=False, extra_head="", ld=None):
    robots = '\n  <meta name="robots" content="noindex">' if noindex else ""
    canonical = "" if noindex else f'\n  <link rel="canonical" href="{url}">'
    ld_block = ""
    if ld:
        ld_json = json.dumps(ld, indent=2, ensure_ascii=False).replace("</", "<\\/")
        ld_json = "\n".join("  " + line for line in ld_json.splitlines())
        ld_block = f'\n  <script type="application/ld+json">\n{ld_json}\n  </script>'
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">{robots}{canonical}
  <meta name="theme-color" content="#0b0d0b">{extra_head}
  <link rel="icon" href="{r}assets/favicon.ico" sizes="any">
  <link rel="icon" href="{r}assets/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="{r}assets/favicon-32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="{r}assets/apple-touch-icon.png">
  <link rel="stylesheet" href="{r}assets/site.css">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Swyft Business Broker">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{OG_IMAGE}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Swyft Business Broker wordmark on a dark background">
  <meta property="og:locale" content="en_US">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{OG_IMAGE}">{ld_block}
</head>"""


ORG = {
    "@type": "Organization",
    "@id": ORG_ID,
    "name": "Swyft Business Broker",
    "url": SITE_URL,
    "logo": SITE_URL + "assets/apple-touch-icon.png",
    "image": OG_IMAGE,
    "description": "A value-added business broker. Swyft Business Broker helps owners raise the value of a business before a sale and helps buyers grow the business after a purchase, using Swyft HQ door-to-door sales teams and Swyft International placements.",
    "email": EMAIL,
    "telephone": PHONE_LD,
    "brand": {"@type": "Brand", "name": "Swyft"},
    "parentOrganization": {
        "@type": "Organization",
        "name": "Swyft Solutions LLC",
        "alternateName": "Swyft",
        "url": HQ,
    },
    "sameAs": [HQ],
    "contactPoint": {
        "@type": "ContactPoint",
        "contactType": "sales",
        "email": EMAIL,
        "telephone": PHONE_LD,
        "areaServed": "US",
        "availableLanguage": "English",
    },
}


def breadcrumb(name, url):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL},
            {"@type": "ListItem", "position": 2, "name": name, "item": url},
        ],
    }


def page_ld(kind, name, url, desc):
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": kind,
                "@id": url + "#webpage",
                "url": url,
                "name": name,
                "description": desc,
                "inLanguage": "en-US",
                "isPartOf": {"@id": WEBSITE_ID},
                "publisher": {"@id": ORG_ID},
            },
            breadcrumb(name.split(" | ")[0], url),
            {
                "@type": "WebSite",
                "@id": WEBSITE_ID,
                "url": SITE_URL,
                "name": "Swyft Business Broker",
            },
            ORG,
        ],
    }


def crumbs(r, name):
    return f"""        <nav class="crumbs" aria-label="Breadcrumb">
          <ol>
            <li><a href="{r}">Home</a></li>
            <li aria-current="page">{name}</li>
          </ol>
        </nav>"""


def hero_bg():
    return '    <div class="hero-grid" aria-hidden="true"></div>\n    <div class="hero-glow" aria-hidden="true"></div>'


def answer(text):
    return f"""        <div class="answer">
          <p class="answer-label">Quick answer</p>
          <p>{text}</p>
        </div>"""


def cta_band(r, heading, text, ghost_href=HQ, ghost_label="See how Swyft HQ runs the work"):
    return f"""    <section class="section" aria-labelledby="cta-h">
      <div class="wrap">
        <div class="lead">
          <div class="lead-copy">
            <span class="eyebrow"><span class="dot"></span>Start with a call</span>
            <h2 id="cta-h">{heading}</h2>
            <p>{text}</p>
            <div class="cta-row">
              <a class="btn" href="{r}contact/">Talk to Colin</a>
              <a class="btn btn-ghost" href="{ghost_href}">{ghost_label} {ARROW}</a>
            </div>
          </div>
          <ul class="lead-facts">
            <li>Email: <a href="mailto:{EMAIL}">{EMAIL}</a></li>
            <li>Phone: <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
            <li>No listings, no promised price, no promised timeline.</li>
            <li>A sale of a business involves your own counsel and the usual due diligence.</li>
          </ul>
        </div>
      </div>
    </section>"""


def write_page(rel_dir, title, desc, main, current="", ld=None, noindex=False, extra_head="", scripts=""):
    depth = 0 if rel_dir == "" else 1
    r = "" if depth == 0 else "../"
    url = SITE_URL + (rel_dir + "/" if rel_dir else "")
    html = "\n".join(
        [
            head(r, title, desc, url, noindex=noindex, extra_head=extra_head, ld=ld),
            "<body>",
            header(r, current),
            '  <main id="main">',
            main.replace("{R}", r).rstrip(),
            "  </main>",
            footer(r),
            scripts.replace("{R}", r) if scripts else "",
            "</body>",
            "</html>",
            "",
        ]
    )
    html = html.replace("\n\n</body>", "\n</body>")
    out = ROOT / rel_dir / "index.html" if rel_dir else ROOT / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return out


# ---------------------------------------------------------------- Home
LEVERS = [
    (
        "More sold accounts, no sales force to build",
        "Swyft HQ recruits, trains, houses, and manages door-to-door reps who sell your service on your paperwork. You keep the brand, the customer, and the install, service, and warranty work.",
        HQ_HOW,
        "How the D2D teams work",
    ),
    (
        "Recurring agreements and denser routes",
        "Swyft already runs teams in trades sold as ongoing service, like pest control, lawn care, and window cleaning. Reps work a neighborhood at a time, so new accounts land near routes you already drive.",
        HQ_IND,
        "Industries Swyft HQ runs",
    ),
    (
        "Sold only up to the capacity you set",
        "You tell Swyft how much work your crews can take. The team sells up to that line, so the book a buyer reviews is work you can deliver, not a pile of jobs you cannot get to.",
        HQ_HOW,
        "See the deploy steps",
    ),
    (
        "A sales motion that is written down",
        "Reps use a trained pitch on your paperwork, and you get a weekly report: doors, conversations, and sold accounts by rep. The process is documented and measured instead of living in your head.",
        HQ_HOW,
        "What the weekly report covers",
    ),
    (
        "Less dependence on the owner",
        "Swyft International places offshore staff in seats that do not need a truck: appointment setting, customer support, bookkeeping, and admin. Fewer tasks that only you can do.",
        HQ_INTL,
        "Swyft International placements",
    ),
]


def lever_cards():
    out = []
    for i, (h, p, href, label) in enumerate(LEVERS, 1):
        out.append(
            f"""          <a class="card" href="{href}">
            <span class="card-num">{i:02d}</span>
            <span class="card-go" aria-hidden="true">&#8599;</span>
            <h3>{h}</h3>
            <p>{p}</p>
            <span class="card-link">{label} on Swyft HQ</span>
          </a>"""
        )
    return "\n".join(out)


HOME_DESC = "Swyft Business Broker is a value-added business broker. We help owners raise the value of a business before they sell and help buyers grow it after they buy."
HOME_TITLE = "Swyft Business Broker | Value-added business broker"

HOME_MAIN = f"""    <section class="hero hero-home">
{hero_bg()}
      <div class="wrap">
        <span class="eyebrow"><span class="dot"></span>Value-added business broker</span>
        <h1>Sell a business worth more, or <span class="grad">grow the one you buy.</span></h1>
        <p class="lede">We help owners raise the value of a business before they sell, and help buyers grow the business after they buy. The growth work is done by Swyft HQ.</p>
        <div class="cta-row">
          <a class="btn" href="{{R}}contact/">Talk to Colin</a>
          <a class="btn btn-ghost" href="{HQ}">See how Swyft HQ runs the work {ARROW}</a>
        </div>
{answer("Swyft Business Broker is a business broker that adds value on both sides of a sale. Before you sell, Swyft HQ can put a trained door-to-door team on your service to add sold accounts, and Swyft International can place support or admin staff so the business leans on you less. After a purchase, the same services help the new owner grow. There are no listings here and no promised price or timeline. It starts with a call with Colin Speer.")}
      </div>
    </section>

    <section class="section" aria-labelledby="sellers-h">
      <div class="wrap split">
        <div class="split-copy">
          <span class="eyebrow"><span class="dot"></span>For sellers</span>
          <h2 id="sellers-h">Raise the value first. Sell when you are ready.</h2>
          <p>Buyers pay for accounts, documented process, and a business that runs without the owner on every call. We work on those before the sale.</p>
          <div class="cta-row">
            <a class="btn btn-ghost" href="{{R}}sellers/">How it works for sellers</a>
          </div>
        </div>
        <ol class="steps">
          <li><span class="step-n">01</span><div><h3>Understand the business</h3><p>What you sell, where you sell it, how many accounts you carry, what you still do yourself each week, and how much more work your crews can take.</p></div></li>
          <li><span class="step-n">02</span><div><h3>Work the levers through Swyft HQ</h3><p>A door-to-door team sells your service on your paperwork, up to the capacity you set. Where it fits, Swyft International fills calling, support, bookkeeping, or admin seats.</p></div></li>
          <li><span class="step-n">03</span><div><h3>Run the sale conversation</h3><p>When you decide it is time, we talk through the sale. Your counsel and the usual due diligence are part of it.</p></div></li>
        </ol>
      </div>
    </section>

    <section class="band" aria-labelledby="buyers-h">
      <div class="wrap split">
        <div class="split-copy">
          <span class="eyebrow"><span class="dot"></span>For buyers</span>
          <h2 id="buyers-h">Bought the business. Now grow it.</h2>
          <p>A new owner has to learn the operation and grow it at the same time. Swyft HQ can carry the selling and some of the back-office work.</p>
          <div class="cta-row">
            <a class="btn btn-ghost" href="{{R}}buyers/">How it works for buyers</a>
          </div>
        </div>
        <ol class="steps">
          <li><span class="step-n">01</span><div><h3>Tell us what you are looking for</h3><p>The trade, the area, and the size of business you want. We will be straight with you about what we know of and what we do not.</p></div></li>
          <li><span class="step-n">02</span><div><h3>Close with your own advisors</h3><p>Counsel and due diligence stay with you and your advisors. We do not hand out legal or tax advice.</p></div></li>
          <li><span class="step-n">03</span><div><h3>Grow it after the purchase</h3><p>Swyft HQ can deploy a door-to-door team to add sold accounts and place offshore staff through Swyft International to take operational work off your plate.</p></div></li>
        </ol>
      </div>
    </section>

    <section class="section" aria-labelledby="levers-h">
      <div class="wrap">
        <div class="section-head">
          <h2 id="levers-h">Where the value comes from</h2>
          <p>Each lever is a service Swyft HQ runs today. No made-up multiples. Follow the links to see exactly how each one works.</p>
        </div>
        <div class="grid3">
{lever_cards()}
        </div>
      </div>
    </section>

    <section class="band" aria-labelledby="ind-h">
      <div class="wrap">
        <div class="section-head">
          <h2 id="ind-h">Trades Swyft HQ already runs</h2>
          <p>Each industry has its own page on Swyft HQ.</p>
        </div>
{industry_chips()}
      </div>
    </section>

{cta_band("{R}", "Talk to Colin about your business.", "Selling in a year or two, or just bought? Tell us where things stand. The first step is a conversation, not a valuation.")}
"""

HOME_LD = {
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "WebSite",
            "@id": WEBSITE_ID,
            "url": SITE_URL,
            "name": "Swyft Business Broker",
            "description": HOME_DESC,
            "inLanguage": "en-US",
            "publisher": {"@id": ORG_ID},
        },
        ORG,
    ],
}

# ---------------------------------------------------------------- Sellers
SELLERS_TITLE = "For sellers | Swyft Business Broker"
SELLERS_DESC = "Selling a home-service business? Raise its value first: more sold accounts from Swyft HQ door-to-door teams and less owner dependence through Swyft International."

SELLERS_MAIN = f"""    <section class="hero hero-sub">
{hero_bg()}
      <div class="wrap">
{crumbs("{R}", "Sellers")}
        <span class="eyebrow"><span class="dot"></span>For owners who want to sell</span>
        <h1>Make the business worth more <span class="grad">before you sell it.</span></h1>
        <p class="lede">Buyers look at the accounts on the books, how the work gets sold, and how much of it depends on you. Those can change before a sale. Swyft HQ does that work.</p>
{answer("We learn how your business runs, use Swyft HQ door-to-door teams and Swyft International placements to work on the parts a buyer looks at, and run the sale conversation when you say you are ready. We will not show you invented listings, and we will not promise a timeline or a price.")}
      </div>
    </section>

    <section class="section" aria-labelledby="seq-h">
      <div class="wrap split">
        <div class="split-copy">
          <span class="eyebrow"><span class="dot"></span>The sequence</span>
          <h2 id="seq-h">Three steps, in order</h2>
          <p>The sale comes last. The value work comes first, and it is run by the same teams Swyft HQ deploys for its clients.</p>
        </div>
        <ol class="steps">
          <li><span class="step-n">01</span><div>
            <h3>Understand the business</h3>
            <p>We start with a call. What you sell, the area you cover, how many accounts you carry, which ones renew, what your crews can handle, and which jobs still need you personally.</p>
          </div></li>
          <li><span class="step-n">02</span><div>
            <h3>Work the levers through Swyft HQ</h3>
            <p>If your trade fits, Swyft HQ recruits, trains, houses, and manages a door-to-door team that sells your service on your paperwork. You keep the brand, the customer, and the install, service, and warranty work, and you set the capacity the team sells up to.</p>
            <p>If calls, support, bookkeeping, or admin keep you tied to the business, Swyft International can place offshore staff in those seats.</p>
          </div></li>
          <li><span class="step-n">03</span><div>
            <h3>Run the sale conversation when you are ready</h3>
            <p>You decide when. A sale involves your own counsel and the usual due diligence. We do not give legal or tax advice.</p>
          </div></li>
        </ol>
      </div>
    </section>

    <section class="band" aria-labelledby="deal-h">
      <div class="wrap">
        <div class="section-head">
          <h2 id="deal-h">How the door-to-door deal works</h2>
          <p>The same terms Swyft HQ uses with every client.</p>
        </div>
        <div class="grid3">
          <div class="tile">
            <h3>You keep the business</h3>
            <p>Reps sell on your paperwork under your brand. The customer is yours. Install, service, and warranty stay with your crews.</p>
          </div>
          <div class="tile">
            <h3>Revenue share per account</h3>
            <p>You pay a revenue share on each sold account. The rate is written in the agreement and is not published on this site or on Swyft HQ.</p>
          </div>
          <div class="tile">
            <h3>Deploy and reporting</h3>
            <p>Housing for the team and a check on the city's solicitation permit are part of deploy. You get a weekly report of doors, conversations, and sold accounts by rep.</p>
          </div>
        </div>
        <div class="cta-row">
          <a class="btn btn-ghost" href="{HQ_HOW}">How it works on Swyft HQ {ARROW}</a>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="fit-h">
      <div class="wrap">
        <div class="section-head">
          <h2 id="fit-h">Trades that fit</h2>
          <p>Door-to-door teams run in these industries today. If yours is not here, ask anyway. The Swyft International seats are not tied to a trade.</p>
        </div>
{industry_chips()}
      </div>
    </section>

    <section class="band" aria-labelledby="not-h">
      <div class="wrap split">
        <div class="split-copy">
          <span class="eyebrow"><span class="dot"></span>Straight answers</span>
          <h2 id="not-h">What we will not do</h2>
        </div>
        <div class="why">
          <div>
            <h3>No invented listings</h3>
            <p>There is no marketplace of businesses for sale on this site, and we will not show you sample listings or sample buyers.</p>
          </div>
          <div>
            <h3>No promised price or timeline</h3>
            <p>Results depend on your market, your crews, and the buyer. Anyone who quotes a number before seeing the business is guessing.</p>
          </div>
          <div>
            <h3>No borrowed proof</h3>
            <p>No client names, case studies, or result numbers we cannot back up. Ask on the call and we will tell you what we know.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section faq" aria-labelledby="faq-h">
      <div class="wrap">
        <h2 id="faq-h">Seller questions</h2>
        <div class="faq-list">
          <details>
            <summary><h3>Do I have to sell to use the Swyft HQ services?</h3></summary>
            <div class="faq-a"><p>No. Swyft HQ works with owners who have no plan to sell. The broker side only matters when you decide you want to.</p></div>
          </details>
          <details>
            <summary><h3>Will you list my business somewhere?</h3></summary>
            <div class="faq-a"><p>Not without talking to you first. Nothing about your business goes public from a contact form or a first call.</p></div>
          </details>
          <details>
            <summary><h3>What does it cost?</h3></summary>
            <div class="faq-a"><p>The door-to-door rate is a revenue share per sold account, written in the agreement. Swyft International charges a success fee on placements, published on its page. Broker terms are discussed directly on a call.</p></div>
          </details>
          <details>
            <summary><h3>Do I need a lawyer?</h3></summary>
            <div class="faq-a"><p>A sale of a business normally involves counsel and due diligence on both sides. We are not your lawyer and do not give legal advice.</p></div>
          </details>
        </div>
      </div>
    </section>

{cta_band("{R}", "Thinking about selling?", "Tell us what the business does and when you might sell. We will tell you plainly whether Swyft HQ can help first.", HQ_HOW, "How Swyft HQ works")}
"""

# ---------------------------------------------------------------- Buyers
BUYERS_TITLE = "For buyers | Swyft Business Broker"
BUYERS_DESC = "Buying a home-service or related business? After the purchase, Swyft HQ door-to-door teams can add accounts and Swyft International can take operational work off the new owner."

BUYERS_MAIN = f"""    <section class="hero hero-sub">
{hero_bg()}
      <div class="wrap">
{crumbs("{R}", "Buyers")}
        <span class="eyebrow"><span class="dot"></span>For buyers</span>
        <h1>Buy the business. <span class="grad">Then grow it.</span></h1>
        <p class="lede">A new owner has to learn the operation and grow it at once. Swyft HQ can take on the selling and some of the operational work so you can focus on running it.</p>
{answer("After you buy a home-service or related business, Swyft HQ can deploy a door-to-door team to sell the service on your paperwork, and Swyft International can place offshore staff for appointment setting, support, bookkeeping, or admin. Tell us what you are looking for. We do not run a marketplace or a list of deals.")}
      </div>
    </section>

    <section class="section" aria-labelledby="after-h">
      <div class="wrap">
        <div class="section-head">
          <h2 id="after-h">What Swyft HQ can do after the purchase</h2>
          <p>Two services, both live on Swyft HQ today.</p>
        </div>
        <div class="grid3">
          <a class="card" href="{HQ_HOW}">
            <span class="card-num">01</span>
            <span class="card-go" aria-hidden="true">&#8599;</span>
            <h3>Door-to-door sales teams</h3>
            <p>Swyft recruits, trains, houses, and manages reps who sell your service on your paperwork. You keep the brand, the customer, and fulfillment. You pay a revenue share per sold account, at a rate written in the agreement. Weekly report of doors, conversations, and sold accounts by rep.</p>
            <span class="card-link">How it works on Swyft HQ</span>
          </a>
          <a class="card" href="{HQ_INTL}">
            <span class="card-num">02</span>
            <span class="card-go" aria-hidden="true">&#8599;</span>
            <h3>Swyft International placements</h3>
            <p>Offshore staff for work that does not need a truck: appointment setting, customer support, bookkeeping, and admin. The success fee is 33% of first-year salary, and you pay the salary. A $500 deposit applies only to start a new search when the existing database has no fit. 90-day free replacement.</p>
            <span class="card-link">Swyft International on Swyft HQ</span>
          </a>
          <div class="card">
            <span class="card-num">03</span>
            <h3>Sold to your capacity</h3>
            <p>A new owner often does not know yet how much the crews can absorb. You set the line, and the team sells up to it. Door-to-door work stays with the D2D teams; International covers the office seats.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="band" aria-labelledby="steps-h">
      <div class="wrap split">
        <div class="split-copy">
          <span class="eyebrow"><span class="dot"></span>How it works</span>
          <h2 id="steps-h">Simple on purpose</h2>
          <p>No buyer scorecard, no gated deal room. A conversation, then work.</p>
        </div>
        <ol class="steps">
          <li><span class="step-n">01</span><div><h3>Tell us what you are looking for</h3><p>Trade, area, size, and whether you have already bought. We will be straight about what we know of and what we do not.</p></div></li>
          <li><span class="step-n">02</span><div><h3>Close with your own advisors</h3><p>Your counsel and due diligence run the purchase. We do not give legal or tax advice.</p></div></li>
          <li><span class="step-n">03</span><div><h3>Put Swyft HQ to work</h3><p>If the trade fits, a door-to-door team deploys after a permit check and housing setup. If office work is the bottleneck, Swyft International starts a placement.</p></div></li>
        </ol>
      </div>
    </section>

    <section class="section" aria-labelledby="fit-h">
      <div class="wrap">
        <div class="section-head">
          <h2 id="fit-h">Trades Swyft HQ runs</h2>
          <p>If you are buying in one of these, a door-to-door team may fit from day one.</p>
        </div>
{industry_chips()}
      </div>
    </section>

{cta_band("{R}", "Tell us what you are looking for.", "The trade, the area, the size, and where you are in the process. Colin will reply directly.", HQ_INTL, "See Swyft International")}
"""

# ---------------------------------------------------------------- About
ABOUT_TITLE = "About | Swyft Business Broker"
ABOUT_DESC = "Swyft Business Broker is the business-broker offer of Swyft (Swyft Solutions LLC), led by Colin Speer. The growth work is done by Swyft HQ."

ABOUT_MAIN = f"""    <section class="hero hero-sub">
{hero_bg()}
      <div class="wrap">
{crumbs("{R}", "About")}
        <span class="eyebrow"><span class="dot"></span>About</span>
        <h1>A broker backed by <span class="grad">a team that sells.</span></h1>
        <p class="lede">Swyft Business Broker is the business-broker offer of Swyft (Swyft Solutions LLC). Colin Speer leads the company.</p>
{answer("Swyft Business Broker is run by Swyft, the same company behind Swyft HQ. The value work before a sale and the growth work after a purchase are done by Swyft HQ's door-to-door teams and, where it fits, Swyft International placements. Contact is by email or phone.")}
      </div>
    </section>

    <section class="section" aria-labelledby="who-h">
      <div class="wrap split">
        <div class="split-copy">
          <span class="eyebrow"><span class="dot"></span>Who does the work</span>
          <h2 id="who-h">One company, two offers</h2>
        </div>
        <div class="prose">
          <p><strong>Swyft HQ</strong> recruits, trains, houses, and manages door-to-door reps who sell a client's service on the client's paperwork. The client keeps the brand, the customer, and the install, service, and warranty work. It runs in exteriors and roofing, window cleaning, pest control, lawn care, fiber internet and wireless, interior home improvement, home security, water treatment, and HVAC.</p>
          <p><strong>Swyft International</strong> places offshore staff in seats that do not need a truck: appointment setting, customer support, bookkeeping, and admin.</p>
          <p><strong>Swyft Business Broker</strong> puts those services to work around a sale: raising value before an owner sells, and growing the business after a buyer buys.</p>
          <div class="cta-row">
            <a class="btn btn-ghost" href="{HQ_ABOUT}">About Swyft HQ {ARROW}</a>
            <a class="btn btn-ghost" href="{HQ}">Swyft HQ home {ARROW}</a>
          </div>
        </div>
      </div>
    </section>

    <section class="band" aria-labelledby="not-h">
      <div class="wrap split">
        <div class="split-copy">
          <span class="eyebrow"><span class="dot"></span>Same rule as Swyft HQ</span>
          <h2 id="not-h">What we will not put on this site</h2>
          <p>If we cannot back it up, it does not go up.</p>
        </div>
        <div class="why">
          <div>
            <h3>No borrowed client names</h3>
            <p>No logos, testimonials, or case studies that are not ours to show.</p>
          </div>
          <div>
            <h3>No result numbers</h3>
            <p>No deal counts, revenue multiples, or growth figures. Ask on a call and you will get a straight answer.</p>
          </div>
          <div>
            <h3>No rate card for the door-to-door deal</h3>
            <p>The revenue share is written in the agreement, the same as on Swyft HQ.</p>
          </div>
          <div>
            <h3>No fake listings</h3>
            <p>There is no public marketplace of businesses for sale here.</p>
          </div>
          <div>
            <h3>No license claims</h3>
            <p>We do not claim a broker license on this site. A sale involves your own counsel and the usual due diligence.</p>
          </div>
        </div>
      </div>
    </section>

{cta_band("{R}", "Talk to Colin.", "Selling, buying, or not sure yet. Send a note or call.", HQ_ABOUT, "About Swyft HQ")}
"""

# ---------------------------------------------------------------- Contact
CONTACT_TITLE = "Contact | Swyft Business Broker"
CONTACT_DESC = "Contact Colin Speer at Swyft Business Broker by email at colin@swyft-hq.com or by phone at 267-606-8667."

CONTACT_MAIN = f"""    <section class="hero hero-sub">
{hero_bg()}
      <div class="wrap">
{crumbs("{R}", "Contact")}
        <span class="eyebrow"><span class="dot"></span>Contact</span>
        <h1>Talk to <span class="grad">Colin.</span></h1>
        <p class="lede">Tell us whether you are selling, buying, or not sure yet. Colin Speer reads every message.</p>
{answer(f'Email <a href="mailto:{EMAIL}">{EMAIL}</a> or call <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>. The form below opens your email app with your message filled in. It starts a conversation. It does not produce a quote or a valuation.')}
      </div>
    </section>

    <section class="section" aria-labelledby="form-h">
      <div class="wrap">
        <div class="lead">
          <div class="lead-copy">
            <span class="eyebrow"><span class="dot"></span>Send a note</span>
            <h2 id="form-h">What is going on with the business?</h2>
            <p>A few lines is enough. What it does, where it operates, and what you want to happen next.</p>
            <ul class="lead-facts">
              <li>Email: <a href="mailto:{EMAIL}">{EMAIL}</a></li>
              <li>Phone: <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
              <li>This site has no backend. Nothing you type is stored here.</li>
              <li>See the <a href="{{R}}privacy/">privacy policy</a> for how we handle what you send.</li>
            </ul>
          </div>
          <form class="lead-form" id="contact-form" action="mailto:{EMAIL}?subject=Swyft%20Business%20Broker%20inquiry" method="post" enctype="text/plain">
            <div class="row2">
              <label>Name
                <input type="text" name="name" autocomplete="name" required>
              </label>
              <label><span>Business name <span class="opt">(optional)</span></span>
                <input type="text" name="business" autocomplete="organization">
              </label>
            </div>
            <div class="row2">
              <label>Email
                <input type="email" name="email" autocomplete="email" required>
              </label>
              <label><span>Phone <span class="opt">(optional)</span></span>
                <input type="tel" name="phone" autocomplete="tel">
              </label>
            </div>
            <fieldset>
              <legend>I am a</legend>
              <div class="choice">
                <label><input type="radio" name="role" value="Seller" required> Seller</label>
                <label><input type="radio" name="role" value="Buyer"> Buyer</label>
                <label><input type="radio" name="role" value="Not sure"> Not sure</label>
              </div>
            </fieldset>
            <label>Message
              <textarea name="message" rows="5" required></textarea>
            </label>
            <button class="btn" type="submit">Open email to Colin</button>
            <p class="form-note">Sending opens your email app addressed to {EMAIL}. If it does not open, email or call using the details on this page.</p>
            <p class="form-status" id="form-status" role="status" aria-live="polite"></p>
          </form>
        </div>
      </div>
    </section>
"""

CONTACT_SCRIPTS = '  <script src="{R}assets/contact.js" defer></script>'

# ---------------------------------------------------------------- Privacy
PRIVACY_TITLE = "Privacy policy | Swyft Business Broker"
PRIVACY_DESC = "How Swyft Solutions LLC handles information sent through the Swyft Business Broker website."

PRIVACY_MAIN = f"""    <section class="hero hero-sub">
{hero_bg()}
      <div class="wrap">
{crumbs("{R}", "Privacy")}
        <span class="eyebrow"><span class="dot"></span>Privacy</span>
        <h1>Privacy policy</h1>
        <p class="lede">Last updated November 25, {YEAR}.</p>
{answer("We only get what you send us by email or phone. We use it to reply to you. We do not sell personal information. Email us to see, correct, or delete what we have.")}
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="prose">
          <p>This policy covers swyftbb.com and its preview copy, operated by Swyft Solutions LLC ("Swyft", "we"). Swyft Business Broker is an offer of Swyft Solutions LLC.</p>
          <h2>What we collect</h2>
          <p>This is a static website with no accounts and no database. The contact form does not send anything to a server. It opens your own email app with a message addressed to us. When you email or call us, we receive what you choose to share, such as your name, business name, email, phone number, whether you are a buyer or seller, and your message.</p>
          <h2>How we use it</h2>
          <ul>
            <li>To reply to your inquiry and continue the conversation you started.</li>
            <li>To keep a record of that conversation in our email and business files.</li>
          </ul>
          <p>We do not sell or rent personal information, and we do not use it for third-party advertising.</p>
          <h2>Hosting and technical data</h2>
          <p>The site is hosted on GitHub Pages. GitHub may log technical data such as IP addresses and browser details when pages are requested, under its own privacy terms. This site does not add analytics, ad trackers, or cookies of its own.</p>
          <h2>Your choices</h2>
          <p>To ask for access to, correction of, or deletion of information you have sent us, email <a href="mailto:{EMAIL}">{EMAIL}</a>. We will respond within a reasonable time.</p>
          <h2>Children</h2>
          <p>This site is not directed at children under 13, and we do not knowingly collect information from them.</p>
          <h2>Changes</h2>
          <p>If this policy changes, we will update this page and the date at the top.</p>
          <h2>Contact</h2>
          <p>Swyft Solutions LLC. Email <a href="mailto:{EMAIL}">{EMAIL}</a> or call <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>.</p>
        </div>
      </div>
    </section>
"""

# ---------------------------------------------------------------- 404
# GitHub Pages serves 404.html at whatever path was requested, so relative
# links would resolve against that path. The inline script writes a <base>
# for the project-site preview (/swyftbb-site/) or the domain root.
BASE_SCRIPT = """
  <script>
    (function () {
      var p = location.hostname.slice(-10) === ".github.io" ? "/" + (location.pathname.split("/")[1] || "") + "/" : "/";
      document.write('<base href="' + p.replace(/\\/\\/+$/, "/") + '">');
    })();
  </script>"""

NOTFOUND_MAIN = f"""    <section class="hero hero-sub">
{hero_bg()}
      <div class="wrap">
        <span class="eyebrow"><span class="dot"></span>404</span>
        <h1>That page is not here.</h1>
        <p class="lede">The link may be old or mistyped. Try one of these.</p>
        <div class="cta-row">
          <a class="btn" href="./">Home</a>
          <a class="btn btn-ghost" href="sellers/">Sellers</a>
          <a class="btn btn-ghost" href="buyers/">Buyers</a>
          <a class="btn btn-ghost" href="contact/">Contact</a>
        </div>
      </div>
    </section>
"""


def build():
    pages = []
    write_page("", HOME_TITLE, HOME_DESC, HOME_MAIN, ld=HOME_LD)
    pages.append("")
    for rel, kind, title, desc, main, scripts in [
        ("sellers", "WebPage", SELLERS_TITLE, SELLERS_DESC, SELLERS_MAIN, ""),
        ("buyers", "WebPage", BUYERS_TITLE, BUYERS_DESC, BUYERS_MAIN, ""),
        ("about", "AboutPage", ABOUT_TITLE, ABOUT_DESC, ABOUT_MAIN, ""),
        ("contact", "ContactPage", CONTACT_TITLE, CONTACT_DESC, CONTACT_MAIN, CONTACT_SCRIPTS),
        ("privacy", "WebPage", PRIVACY_TITLE, PRIVACY_DESC, PRIVACY_MAIN, ""),
    ]:
        url = SITE_URL + rel + "/"
        write_page(rel, title, desc, main, current=rel + "/", ld=page_ld(kind, title, url, desc), scripts=scripts)
        pages.append(rel + "/")

    # 404: same chrome, links resolved from the site root via <base>.
    nf = write_page("__404tmp", "Page not found | Swyft Business Broker",
                    "The page you asked for is not on the Swyft Business Broker site.",
                    NOTFOUND_MAIN, noindex=True, extra_head=BASE_SCRIPT)
    html = nf.read_text(encoding="utf-8").replace('href="../"', 'href="./"').replace('href="../', 'href="').replace('src="../', 'src="')
    (ROOT / "404.html").write_text(html, encoding="utf-8")
    nf.unlink()
    nf.parent.rmdir()

    urls = "\n".join(
        f"  <url>\n    <loc>{SITE_URL}{p}</loc>\n    <lastmod>{LASTMOD}</lastmod>\n  </url>" for p in pages
    )
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n',
        encoding="utf-8",
    )
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n", encoding="utf-8"
    )
    print("Built:", ", ".join(["index.html"] + [p + "index.html" for p in pages[1:]] + ["404.html", "sitemap.xml", "robots.txt"]))


if __name__ == "__main__":
    build()
