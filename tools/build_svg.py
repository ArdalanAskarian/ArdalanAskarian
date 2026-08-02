#!/usr/bin/env python3
"""
Build the SVG figures used by README.md.

This profile is themed to match the portfolio at ardalanaskarian.github.io.
That site states its design language at the top of its stylesheet:

    Design language: one accent, held under a strict rule.
    The accent (ultramarine) is only ever allowed on things you can interact
    with: links, the active nav item, the primary button, the focus ring, the
    "now" marker on the timeline. It is never decoration, never a gradient,
    never a category colour. Everything else is neutral, and the project cover
    images carry the rest of the colour on the page.
    Two radii only: --r for surfaces, --r-pill for controls.
    Micro-labels use the system monospace stack, still zero font requests.

Everything below follows from that. Nothing here is a drawn control, and no
font is downloaded: SVG in an <img> cannot fetch web fonts, but font-family
still resolves against the fonts already on the reader's machine - which is
exactly what a system stack is. So the site's three stacks paste in verbatim
and "zero font requests" becomes literally true.

The masthead does carry two colours, and they are the rule's own exception
rather than a hole in it: "the project cover images carry the rest of the
colour on the page." The masthead is a cover. Its two hues are sampled from
the site's actual cover art - teal #1ba69c from the SIFT cover, blue #325eae
from the LLM cover - and each marks the subject it belongs to, so the colour
is carrying meaning rather than filling space. The accent ultramarine is still
absent from every file here, because the accent belongs to links.

    python3 tools/build_svg.py

No dependencies. Standard library only.
"""

from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"


# --------------------------------------------------------------------------
# Tokens
#
# Not a palette - these are the site's own custom properties, copied from
# ardalanaskarian.github.io/styles.css (:root and [data-theme="dark"]). Names
# match the CSS exactly so drift between the two is greppable.
#
# --accent, --accent-ink and --accent-wash are deliberately absent. Nothing in
# a committed SVG is interactive, so nothing in a committed SVG may wear the
# accent. Every accent occurrence in this profile is a real markdown link that
# GitHub colours, focuses and gives a hit area itself.
# --------------------------------------------------------------------------

# Both sets are still built, but README.md serves only the light one, to every
# reader, in every theme. One page, whatever the reader's setting.
#
# That has a cost and it is worth naming, because GitHub owns the colour of the
# prose between the figures and a README cannot reach it: on GitHub's dark theme
# each figure lands as a pale block on a near-black page. Light --bg is #fbfbfc
# against GitHub's #ffffff, so on light the seam disappears entirely; on dark the
# block is meant to read as a block.
#
# Restoring the swap is one flag in the markup, not a change here - both sets
# exist either way. Light is canonical regardless: it is the rendering the
# portfolio's :root describes, it is what these tokens mean, and treating the
# dark values as the source of truth would invert a system that defines itself
# the other way round.
THEMES = {
    "light": {  # :root IS the light theme; light is canonical here too
        "bg": "#fbfbfc",
        "surface": "#ffffff",
        "ink": "#14161c",
        "ink-2": "#3b3f49",
        "muted": "#666b75",
        "faint": "#9498a1",
        "line": "#e6e7ea",
        "line-strong": "#d3d5da",
        # Cover hues, darkened for paper. 4.7:1 and 7.7:1 on --bg.
        "teal": "#0f7f77",   # vision, from covers/sift-cover.png
        "blue": "#2b4f92",   # machine learning, from covers/llm-cover.png
    },
    "dark": {
        "bg": "#0e0f13",
        "surface": "#16181d",
        "ink": "#eceff0",
        "ink-2": "#c2c6cd",
        "muted": "#8a8f99",
        "faint": "#656a74",
        "line": "#24272e",
        "line-strong": "#343841",
        # Lightened for ink. 9.9:1 and 7.1:1 on --bg.
        "teal": "#3ecec2",
        "blue": "#7d9ce6",
    },
}

# The site's stacks, verbatim from styles.css:17-19. The display face is
# unused here: this masthead is set in the monospace.
SANS = ("-apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Helvetica Neue', "
        "'Segoe UI', Roboto, Arial, sans-serif")
MONO = ("ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, "
        "'Liberation Mono', monospace")

R = 14  # --r, the surface radius. The only radius drawn here.

# Anything matching these must never reach a committed asset.
BANNED = ("1b2fd6", "8093ff", "rgba(27, 47, 214", "rgba(128, 147, 255", "shadow")


# --------------------------------------------------------------------------
# Emit helpers
#
# There is no font on this machine to measure against, and the reader's
# machine may resolve a wider one. So the build never measures - it asserts
# against a deliberate over-estimate and fails loudly rather than shipping a
# figure with clipped text.
# --------------------------------------------------------------------------

def fits(s, size, budget, tracking=0.0):
    """Assert a string fits its column at a pessimistic width ceiling.

    0.62 em/char is above every mono in the stack (0.549-0.603) and well above
    every proportional sans in it (~0.50-0.58), so passing here means passing
    on any machine.
    """
    w = len(s) * 0.62 * size + max(len(s) - 1, 0) * tracking
    assert w <= budget, f"{s!r} needs {w:.0f}px but the budget is {budget}px"
    return s


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(s, x, y, family, size, weight=400, fill="#000", tracking=None,
         anchor=None):
    a = [f'x="{x}"', f'y="{y}"', f'font-family="{family}"',
         f'font-size="{size}"', f'font-weight="{weight}"', f'fill="{fill}"']
    if tracking is not None:
        a.append(f'letter-spacing="{tracking}"')
    if anchor:
        a.append(f'text-anchor="{anchor}"')
    return f'<text {" ".join(a)}>{esc(s)}</text>'


def sp(s, fill):
    """Colour one phrase inside a line. <tspan> flows inline, so this needs no
    width - which is the only reason per-phrase colour is safe here at all."""
    return f'<tspan fill="{fill}">{esc(s)}</tspan>'


def text_raw(body, x, y, family, size, weight=400, fill="#000", tracking=None):
    """Like text(), but `body` is already-escaped markup that may hold tspans."""
    a = [f'x="{x}"', f'y="{y}"', f'font-family="{family}"',
         f'font-size="{size}"', f'font-weight="{weight}"', f'fill="{fill}"']
    if tracking is not None:
        a.append(f'letter-spacing="{tracking}"')
    return f'<text {" ".join(a)}>{body}</text>'


def head(w, h, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" role="img" aria-labelledby="t">'
            f'<title id="t">{esc(title)}</title>')


# --------------------------------------------------------------------------
# Masthead
#
# Unframed. The site's .hero is the one major section that is NOT a framed
# panel - it is type on the page ground and nothing else. No border, no rule,
# no marks. Every SVG still carries a full-bleed --bg rect, because GitHub's
# theme and the OS theme can disagree and without a ground the ink can land on
# a background it has no contrast against.
# --------------------------------------------------------------------------

RECEIPTS = [("1,552", "LABELLED REPORTS"), ("36,407", "LOGGED EVENTS"),
            ("6", "PARTICIPANTS"), ("4", "MODELS"), ("1", "NULL RESULT")]

RECEIPTS_ALT = ("1,552 hand-labelled reports. 36,407 logged events. "
                "6 participants. 4 models. 1 null result.")

EYEBROW = "OPEN TO FULL-TIME SOFTWARE & ML ROLES"
TAGLINE = ("Software engineer working on machine learning systems,",
           "and the ordinary software that has to hold them up.")
DESCRIPTOR = ("M.Sc. Computer Science · University of Saskatchewan · Applied ML stream",
              "Computer vision and image processing, under Dr. Mark Eramian.")

MASTHEAD_ALT = (
    "Ardalan Askarian. Open to full-time software and ML roles. Software "
    "engineer working on machine learning systems, and the ordinary software "
    "that has to hold them up. M.Sc. Computer Science, University of "
    "Saskatchewan, Applied ML stream. Computer vision and image processing, "
    "under Dr. Mark Eramian. " + RECEIPTS_ALT)


# --------------------------------------------------------------------------
# Receipts
#
# Five numbers that were already further down the page, pulled up under the
# name so the claims arrive with their evidence attached. Set as a ledger row
# rather than a run of small caps: a number wants to be read as a number, and a
# letter-spaced sentence turns all five into texture.
#
# Part of the masthead rather than a figure of its own. As a separate image it
# was a second block of ground with GitHub's 16px paragraph gutter between the
# two - invisible on a dark page, a white seam on a light one, now that the
# README serves the dark set to everybody. Inside the masthead it sits under
# one hairline, inside the same clip, so the reveal that crosses the name
# crosses the numbers too.
#
# The fifth column is the point. Every other number on a profile went the way
# its owner wanted; this one did not, and it is set at the same size as the
# rest.
# --------------------------------------------------------------------------


def receipts_row(o, c, CL, CR, rule_y, cols, size, label_size, track, pitch=0):
    """The ledger. `cols` is how many columns per row; the rest wrap beneath."""
    o.append(f'<line x1="{CL}" y1="{rule_y}.5" x2="{CR}" y2="{rule_y}.5" '
             f'stroke="{c["line"]}" stroke-width="1"/>')
    col = (CR - CL) / cols
    for i, (n, label) in enumerate(RECEIPTS):
        x = CL + (i % cols) * col
        y = rule_y + 44 + (i // cols) * pitch
        o.append(text(fits(n, size, col - 10, -0.5), x, y, MONO, size, 600,
                      c["ink"], tracking=-0.5))
        o.append(text(fits(label, label_size, col - 10, track), x, y + 22, MONO,
                      label_size, 500, c["faint"], tracking=track))


# The masthead is the one thing here that moves, and it moves once.
#
# A single hairline crosses the block left to right and the type is revealed in
# its wake, firming up from --faint to its final ink just behind the edge - an
# image resolving as it is read. Four staggered bands would have been a generic
# content reveal; one travelling edge is a pass over a surface.
#
# It degrades to the finished masthead, by construction. The clip rect's base
# position covers everything and the edge's base opacity is 0, so anything that
# never runs CSS - a crawler, a social-card renderer, a sanitising proxy - gets
# the complete figure with no edge in it. No animation uses `forwards`.
EASE = "cubic-bezier(.32,.72,.24,1)"


def motion(p, w, dur=1.3):
    return (
        f"<style>"
        f".{p}v{{animation:{p}rv {dur}s {EASE}}}"
        f"@keyframes {p}rv{{from{{transform:translateX(-{w}px)}}}}"
        f".{p}e{{animation:{p}ed {dur}s {EASE}}}"
        f"@keyframes {p}ed{{0%{{transform:translateX(-{w}px);opacity:0}}"
        f"6%{{opacity:1}}88%{{opacity:1}}100%{{transform:translateX(0);opacity:0}}}}"
        f".{p}g{{animation:{p}rs {dur + .25}s {EASE}}}"
        f"@keyframes {p}rs{{from{{opacity:.28}}}}"
        f"@media(prefers-reduced-motion:reduce){{.{p}v,.{p}e,.{p}g{{animation:none}}}}"
        f"</style>")


def edge(p, c, w, h):
    return (f'<rect class="{p}e" x="{w - 1}" y="0" width="1" height="{h}" '
            f'fill="{c["line-strong"]}" opacity="0"/>')


def masthead(theme):
    c = THEMES[theme]
    W, H, CL = 880, 420, 76          # --gutter 24 + --frame-pad 52
    budget = 804 - CL                # to the shared right edge
    p = "m"
    o = [head(W, H, MASTHEAD_ALT), motion(p, W),
         f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>',
         f'<clipPath id="{p}c"><rect class="{p}v" width="{W}" height="{H}"/></clipPath>',
         f'<g clip-path="url(#{p}c)" class="{p}g">']

    # .label geometry, verbatim: mono 11 / w500 / .13em. Teal because the line
    # is about availability, the one thing on the page with a state.
    o.append(text(fits(EYEBROW, 11, budget, 1.43), CL, 75, MONO, 11, 500,
                  c["teal"], tracking=1.43))
    o.append(text(fits("Ardalan Askarian", 58, budget, -1.2), CL, 150, MONO,
                  58, 600, c["ink"], tracking=-1.2))
    o.append(text_raw("Software engineer working on "
                      + sp("machine learning systems,", c["blue"]),
                      CL, 200, MONO, 17, 400, c["ink-2"]))
    o.append(text(fits(TAGLINE[1], 17, budget), CL, 226, MONO, 17, 400, c["ink-2"]))
    o.append(text(fits(DESCRIPTOR[0], 13, budget), CL, 258, MONO, 13, 400, c["muted"]))
    o.append(text_raw(sp("Computer vision and image processing", c["teal"])
                      + esc(", under Dr. Mark Eramian."),
                      CL, 280, MONO, 13, 400, c["muted"]))
    receipts_row(o, c, CL, 804, 316, cols=5, size=26, label_size=10, track=1.3)
    o.append("</g>" + edge(p, c, W, H))
    return "".join(o) + "</svg>"


def masthead_narrow(theme):
    c = THEMES[theme]
    W, H, CL = 420, 616, 36          # clamp floors: gutter 14 + frame-pad 22
    budget = 384 - CL
    p = "n"
    o = [head(W, H, MASTHEAD_ALT), motion(p, W),
         f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>',
         f'<clipPath id="{p}c"><rect class="{p}v" width="{W}" height="{H}"/></clipPath>',
         f'<g clip-path="url(#{p}c)" class="{p}g">']
    o.append(text(fits(EYEBROW, 10, budget, 1.30), CL, 48, MONO, 10, 500,
                  c["teal"], tracking=1.30))
    for i, part in enumerate(("Ardalan", "Askarian")):
        o.append(text(fits(part, 44, budget, -0.9), CL, 100 + i * 46, MONO, 44,
                      600, c["ink"], tracking=-0.9))
    # Hand-broken lines. A coloured phrase never straddles a break, so each
    # line is either plain or holds exactly one tspan.
    tag = ("Software engineer working on", None, "ordinary software that has to hold",
           "them up.")
    for i, line in enumerate(tag):
        y = 210 + i * 23
        if line is None:
            o.append(text_raw(sp("machine learning systems,", c["blue"]) + esc(" and the"),
                              CL, y, MONO, 14, 400, c["ink-2"]))
        else:
            o.append(text(fits(line, 14, budget), CL, y, MONO, 14, 400, c["ink-2"]))
    desc = ("M.Sc. Computer Science · University of", "Saskatchewan · Applied ML stream",
            None, "under Dr. Mark Eramian.")
    for i, line in enumerate(desc):
        y = 306 + i * 20
        if line is None:
            o.append(text_raw(sp("Computer vision and image processing", c["teal"])
                              + esc(","), CL, y, MONO, 11.5, 400, c["muted"]))
        else:
            o.append(text(fits(line, 11.5, budget), CL, y, MONO, 11.5, 400, c["muted"]))
    # Two columns, three rows, five items: the null result lands alone on the
    # last row rather than being padded out to fill the grid.
    receipts_row(o, c, CL, 384, 400, cols=2, size=21, label_size=9.5, track=1.2,
                 pitch=60)
    o.append("</g>" + edge(p, c, W, H))
    return "".join(o) + "</svg>"


# --------------------------------------------------------------------------
# The study
#
# A delta chart, not a pair of absolute bars. The study measured three things
# and found one large effect and two nulls. In absolute-bar form a null cannot
# be drawn at all, so it gets demoted to a sentence; in delta form a null is a
# bar of length zero, which is exactly what it looks like, and all three sit on
# one scale. It also removes the two-segment bar, and with it the last excuse
# for a second colour.
# --------------------------------------------------------------------------

STUDY_ALT = (
    "Change from the manual baseline. Annotation time: plus 71.6 percent. "
    "IoU: no measurable change. Ground-truth coverage: no measurable change. "
    "SIFT-assisted annotation took 1.72 times as long as the manual baseline. "
    "6 participants, 36,407 logged interaction events.")

TITLE = "Change from the manual baseline"
CAPTION = "SIFT-assisted annotation took 1.72× as long as the manual baseline."
STATS = "6 PARTICIPANTS · 36,407 LOGGED INTERACTION EVENTS"
NULLS = ("IoU", "ground-truth coverage")


def study(theme):
    c = THEMES[theme]
    W, H, CL, CR = 880, 380, 76, 804
    ZERO, S = 320, 5.0               # 5px per percentage point
    o = [head(W, H, STUDY_ALT), f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>']
    o.append(f'<rect x="24.5" y="24.5" width="831" height="331" rx="{R}" ry="{R}" '
             f'fill="{c["surface"]}" stroke="{c["line"]}" stroke-width="1"/>')
    o.append(text(fits(TITLE, 17, CR - CL, -0.2), CL, 91, MONO, 17, 600,
                  c["ink"], tracking=-0.2))
    # Without a zero rule a zero-length bar is nothing at all; with it, a dot
    # sitting on the line reads as measured, and it was zero.
    o.append(f'<line x1="{ZERO}.5" y1="112" x2="{ZERO}.5" y2="232" '
             f'stroke="{c["line"]}" stroke-width="1"/>')

    # A new role for --muted, and the only one this README adds: an ink token
    # used as a fill. The site's ramp is a text ramp -- every use is `color:`
    # -- so a bar had no token. --muted is the site's "recessive but must be
    # read" step (nav links, card blurbs), and 5.5:1 clears WCAG for a graphic
    # you have to measure by eye. --line-strong is 1.44:1 and would vanish.
    # Neutral area is not what this system rations. Chromatic area is.
    fits("annotation time", 14, ZERO - CL - 20)
    o.append(f'<rect x="{ZERO}" y="118" width="{71.6 * S:.0f}" height="22" '
             f'fill="{c["muted"]}"/>')          # rx=0: a bar is a measurement,
    o.append(text("annotation time", CL, 134, SANS, 14, 400, c["ink-2"]))
    o.append(text("+71.6%", 692, 134, SANS, 15.5, 600, c["ink"], tracking=-0.155))

    # .timeline-dot ported verbatim: a small neutral mark beside a row, and the
    # one place --line-strong belongs.
    for i, label in enumerate(NULLS):
        y = 175 + i * 46
        fits(label, 14, ZERO - CL - 20)
        o.append(f'<circle cx="{ZERO}" cy="{y}" r="3" fill="{c["line-strong"]}"/>')
        o.append(text(label, CL, y + 5, SANS, 14, 400, c["ink-2"]))
        o.append(text("no measurable change", 340, y + 5, SANS, 14, 400, c["muted"]))

    o.append(f'<line x1="{CL}" y1="272.5" x2="{CR}" y2="272.5" '
             f'stroke="{c["line"]}" stroke-width="1"/>')
    o.append(text(fits(CAPTION, 14, CR - CL), CL, 302, SANS, 14, 400, c["ink-2"]))
    o.append(text(fits(STATS, 11, CR - CL, 1.43), CL, 326, MONO, 11, 500,
                  c["faint"], tracking=1.43))
    return "".join(o) + "</svg>"


def study_narrow(theme):
    c = THEMES[theme]
    W, H, CL, CR = 420, 394, 36, 384
    ZERO, S = 36, 4.0
    o = [head(W, H, STUDY_ALT), f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>']
    o.append(f'<rect x="14.5" y="14.5" width="391" height="364" rx="{R}" ry="{R}" '
             f'fill="{c["surface"]}" stroke="{c["line"]}" stroke-width="1"/>')
    o.append(text(fits(TITLE, 14, CR - CL, -0.15), CL, 68, MONO, 14, 600,
                  c["ink"], tracking=-0.15))
    o.append(f'<line x1="{ZERO - 0.5}" y1="92" x2="{ZERO - 0.5}" y2="250" '
             f'stroke="{c["line"]}" stroke-width="1"/>')

    # Rows stack rather than sit in two columns - the same flip the site makes
    # to its hero at narrow widths. Label start-anchored, value end-anchored,
    # so neither needs a measured width.
    o.append(text("annotation time", CL, 124, SANS, 13, 400, c["ink-2"]))
    o.append(text("+71.6%", CR, 124, SANS, 15.5, 600, c["ink"], anchor="end"))
    o.append(f'<rect x="{ZERO}" y="133" width="{71.6 * S:.0f}" height="16" '
             f'fill="{c["muted"]}"/>')
    for i, label in enumerate(NULLS):
        b = 176 + i * 52
        o.append(text(label, CL, b, SANS, 13, 400, c["ink-2"]))
        o.append(text("no measurable change", CR, b, SANS, 13, 400, c["muted"],
                      anchor="end"))
        o.append(f'<circle cx="{ZERO}" cy="{b + 17}" r="3" fill="{c["line-strong"]}"/>')

    o.append(f'<line x1="{CL}" y1="272.5" x2="{CR}" y2="272.5" '
             f'stroke="{c["line"]}" stroke-width="1"/>')
    for i, line in enumerate(("SIFT-assisted annotation took 1.72× as",
                              "long as the manual baseline.")):
        o.append(text(fits(line, 12.5, CR - CL), CL, 298 + i * 19, SANS, 12.5,
                      400, c["ink-2"]))
    for i, line in enumerate(("6 PARTICIPANTS · 36,407 LOGGED", "INTERACTION EVENTS")):
        o.append(text(fits(line, 10, CR - CL, 1.30), CL, 340 + i * 17, MONO, 10,
                      500, c["faint"], tracking=1.30))
    return "".join(o) + "</svg>"


# --------------------------------------------------------------------------
# Bug classification benchmark
#
# The site leads with this project and the README had no figure for it. The
# story is not that GraphCodeBERT won by half a point over CodeBERT - those
# three are a cluster - it is the twenty-point gap between the transformers
# and the classical baseline. So the bars start at zero, where that gap is
# true, and colour marks the family rather than the winner: blue is the
# transformers, --muted is the baseline they are being measured against.
# --------------------------------------------------------------------------

MODELS = [("GraphCodeBERT", 94.54, True), ("CodeBERT", 93.99, True),
          ("DistilBERT", 92.90, True), ("Naïve Bayes", 74.59, False)]

BENCH_ALT = (
    "Bug classification accuracy. GraphCodeBERT 94.54 percent, CodeBERT 93.99 "
    "percent, DistilBERT 92.90 percent, all fine-tuned transformers. Naïve Bayes, "
    "the classical baseline, 74.59 percent. 1,552 hand-labelled reports across "
    "seven categories, agreement checked with Fleiss' Kappa.")

BENCH_TITLE = "Bug classification accuracy"
BENCH_STATS = "1,552 HAND-LABELLED REPORTS · 7 CATEGORIES · FLEISS' KAPPA CHECKED"


def bench(theme):
    c = THEMES[theme]
    W, H, CL, CR = 880, 380, 76, 804
    X0, SCALE = 300, 4.34            # x=300 is zero; 4.34px per accuracy point
    o = [head(W, H, BENCH_ALT),
         f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>',
         f'<rect x="24.5" y="24.5" width="831" height="331" rx="{R}" ry="{R}" '
         f'fill="{c["surface"]}" stroke="{c["line"]}" stroke-width="1"/>',
         text(fits(BENCH_TITLE, 17, CR - CL, -0.2), CL, 91, MONO, 17, 600,
              c["ink"], tracking=-0.2),
         f'<line x1="{X0}.5" y1="112" x2="{X0}.5" y2="288" stroke="{c["line"]}" stroke-width="1"/>']
    for i, (name, acc, is_tf) in enumerate(MODELS):
        y = 122 + i * 44
        fits(name, 14, X0 - CL - 20)
        o.append(text(name, CL, y + 15, SANS, 14, 400, c["ink-2"]))
        o.append(f'<rect x="{X0}" y="{y}" width="{acc * SCALE:.0f}" height="20" '
                 f'fill="{c["blue"] if is_tf else c["muted"]}"/>')
        o.append(text(f"{acc:.2f}%", X0 + acc * SCALE + 14, y + 15, MONO, 13,
                      600 if is_tf else 400, c["ink"] if is_tf else c["muted"]))
    o.append(f'<line x1="{CL}" y1="308.5" x2="{CR}" y2="308.5" stroke="{c["line"]}" stroke-width="1"/>')
    o.append(text(fits(BENCH_STATS, 11, CR - CL, 1.43), CL, 334, MONO, 11, 500,
                  c["faint"], tracking=1.43))
    return "".join(o) + "</svg>"


def bench_narrow(theme):
    c = THEMES[theme]
    W, H, CL, CR = 420, 372, 36, 384
    X0, SCALE = 36, 3.4
    o = [head(W, H, BENCH_ALT),
         f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>',
         f'<rect x="14.5" y="14.5" width="391" height="343" rx="{R}" ry="{R}" '
         f'fill="{c["surface"]}" stroke="{c["line"]}" stroke-width="1"/>',
         text(fits(BENCH_TITLE, 14, CR - CL, -0.15), CL, 62, MONO, 14, 600,
              c["ink"], tracking=-0.15)]
    for i, (name, acc, is_tf) in enumerate(MODELS):
        b = 100 + i * 52
        o.append(text(name, CL, b, SANS, 13, 400, c["ink-2"]))
        o.append(text(f"{acc:.2f}%", CR, b, MONO, 13, 600 if is_tf else 400,
                      c["ink"] if is_tf else c["muted"], anchor="end"))
        o.append(f'<rect x="{X0}" y="{b + 8}" width="{acc * SCALE:.0f}" height="14" '
                 f'fill="{c["blue"] if is_tf else c["muted"]}"/>')
    o.append(f'<line x1="{CL}" y1="316.5" x2="{CR}" y2="316.5" stroke="{c["line"]}" stroke-width="1"/>')
    for i, line in enumerate(("1,552 HAND-LABELLED REPORTS · 7", "CATEGORIES · FLEISS' KAPPA CHECKED")):
        o.append(text(fits(line, 10, CR - CL, 1.30), CL, 336 + i * 16, MONO, 10, 500,
                      c["faint"], tracking=1.30))
    return "".join(o) + "</svg>"


# --------------------------------------------------------------------------
# Chain figures
#
# Two of the four projects have no measurement to plot, and inventing one
# would be worse than having none. What they do have is a path: a signal
# moving through hardware, and data moving through a pipeline. So the spine
# that carries a scale in the bar figures carries a sequence here - same
# hairline, same grid, same dots as the site's .timeline-dot - and the reader
# gets one drawing grammar across every panel instead of two.
# --------------------------------------------------------------------------


def pulse_mark(c, x, ys, dur=2.4):
    """One mark, hopping the dots it is drawn on, then a ring where it lands.

    The second and last moving thing in this profile, and it earns the same way
    the masthead does: the masthead is an image resolving as it is read, and
    this is a signal arriving. It steps rather than glides, because four hops
    through hardware are discrete events and a smooth slide would draw a
    continuum that is not there.

    No rate is claimed. The figure's caption already says no rate, latency or
    frame time was recorded, and that stays true: the loop period is a legible
    interval, not a measurement, and the caption says so.

    Degrades to nothing, by construction. Both marks carry opacity="0" as an
    attribute, so a crawler, a social-card renderer or a sanitising proxy gets
    the finished diagram with no stray dot in it, and reduced motion gets the
    same by switching the animations off rather than parking them.
    """
    n = len(ys)
    d = ys[-1] - ys[0]
    r = 4
    # steps(n, jump-none) holds each of the n dots for 1/n of the cycle, so the
    # mark reaches the last one at (n-1)/n. Every time below is derived from
    # that rather than typed, because a fade that starts before the arrival
    # means the signal never visibly gets where the figure says it goes.
    arrive = 100 * (n - 1) // n
    return (
        "<style>"
        f".sgh{{animation:sgt {dur}s steps({n},jump-none) infinite}}"
        f"@keyframes sgt{{from{{transform:translateY(0)}}"
        f"to{{transform:translateY({d}px)}}}}"
        f".sgm{{animation:sgo {dur}s linear infinite}}"
        "@keyframes sgo{0%{opacity:0}6%{opacity:1}"
        f"{arrive + 13}%{{opacity:1}}{arrive + 21}%{{opacity:0}}100%{{opacity:0}}}}"
        # The ring peaks nine points after the arrival, not at it. Peaking on
        # arrival puts full opacity on a radius still hidden behind the mark,
        # so the only part you could see was the part that had already faded.
        # scale(), not the `r` geometry property. Animating `r` from CSS is not
        # supported in Firefox at all, and the ring is the payoff for the line
        # that says "breathing and pulsing effects, in real time" - it cannot be
        # the one thing a whole browser does not get. The circle sits at its own
        # origin so scale() grows it about its centre with no transform-origin,
        # and a non-scaling stroke keeps the hairline a hairline.
        f".sgr{{animation:sgb {dur}s linear infinite}}"
        f"@keyframes sgb{{0%,{arrive}%{{transform:scale(1);opacity:0}}"
        f"{arrive + 9}%{{opacity:.85}}"
        f"{arrive + 21}%{{transform:scale(4);opacity:0}}100%{{opacity:0}}}}"
        "@media(prefers-reduced-motion:reduce){.sgh,.sgm,.sgr{animation:none}}"
        "</style>"
        # --muted, not --line-strong. The note under study() is right that
        # line-strong at 1.44:1 vanishes, and a bloom nobody can see is weight
        # without a reading. This one is momentary and fades to nothing, so it
        # never competes with the type it passes.
        f'<g transform="translate({x},{ys[-1]})"><circle class="sgr" r="{r}" '
        f'fill="none" stroke="{c["muted"]}" stroke-width="1.5" '
        f'vector-effect="non-scaling-stroke" opacity="0"/></g>'
        f'<g class="sgh"><circle class="sgm" cx="{x}" cy="{ys[0]}" r="{r}" '
        f'fill="{c["ink"]}" opacity="0"/></g>'
    )


def chain(theme, title, groups, stats, narrow=False, short=None,
          stats_short=None, pulse=False):
    """A labelled sequence on the shared spine. `groups` is a list of
    (group_label | None, [(step, description, hue_or_None), ...]).

    `pulse` animates one mark down the first group's dots. Only the biometric
    chain gets it: there, the thing being drawn really is a signal moving, so
    the motion is the subject. The pipeline is a sequence of stages rather than
    a signal, and animating it would be decoration.
    """
    c = THEMES[theme]
    if narrow:
        W, CL, CR, SPINE = 420, 36, 384, 36
    else:
        W, CL, CR, SPINE = 880, 76, 804, 320
    rows = sum(len(g[1]) for g in groups)
    heads = sum(1 for g in groups if g[0])
    pitch = 54 if narrow else 40
    H = (140 if narrow else 128) + rows * pitch + heads * (30 if narrow else 26) + 56
    if narrow:
        title = short or title
        stats = stats_short or stats
    o = [head(W, H, f"{title}. " + " ".join(
            f"{st}: {d}." for _, steps in groups for st, d, _, _ in steps) + f" {stats}."),
         f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>',
         f'<rect x="{14.5 if narrow else 24.5}" y="14.5" width="{W - (29 if narrow else 49)}" '
         f'height="{H - 45}" rx="{R}" ry="{R}" fill="{c["surface"]}" '
         f'stroke="{c["line"]}" stroke-width="1"/>',
         text(fits(title, 14 if narrow else 17, CR - CL, -0.15),
              CL, 62 if narrow else 78, MONO, 14 if narrow else 17, 600, c["ink"],
              tracking=-0.15)]
    y = 108 if narrow else 118
    spine_top, spine_bot = y - 14, y - 14
    lanes = []
    for label, steps in groups:
        lane = []
        if label:
            o.append(text(fits(label, 10 if narrow else 11, CR - CL, 1.3),
                          CL, y, MONO, 10 if narrow else 11, 500, c["faint"],
                          tracking=1.3))
            y += 30 if narrow else 26
        for st, desc, hue, short_desc in steps:
            if narrow and short_desc:
                desc = short_desc
            if narrow:
                o.append(f'<circle cx="{SPINE}" cy="{y - 4}" r="3" fill="{c["line-strong"]}"/>')
                o.append(text(fits(st, 10, CR - CL - 20, 1.3), CL + 16, y, MONO, 10,
                              500, c[hue] if hue else c["muted"], tracking=1.3))
                o.append(text(fits(desc, 12, CR - CL - 16), CL + 16, y + 20, SANS,
                              12, 400, c["ink-2"]))
            else:
                o.append(text(fits(st, 11, SPINE - CL - 24, 1.3), SPINE - 20, y, MONO,
                              11, 500, c[hue] if hue else c["muted"], tracking=1.3,
                              anchor="end"))
                o.append(f'<circle cx="{SPINE}" cy="{y - 4}" r="3" fill="{c["line-strong"]}"/>')
                o.append(text(fits(desc, 14, CR - SPINE - 36), SPINE + 34, y, SANS, 14,
                              400, c["ink-2"]))
            lane.append(y - 4)
            spine_bot = y - 4
            y += pitch
        lanes.append(lane)
    o.insert(4, f'<line x1="{SPINE}.5" y1="{spine_top}" x2="{SPINE}.5" y2="{spine_bot}" '
                f'stroke="{c["line"]}" stroke-width="1"/>')
    fy = H - 62
    o.append(f'<line x1="{CL}" y1="{fy}.5" x2="{CR}" y2="{fy}.5" stroke="{c["line"]}" stroke-width="1"/>')
    o.append(text(fits(stats, 10 if narrow else 11, CR - CL, 1.3), CL, fy + 26, MONO,
                  10 if narrow else 11, 500, c["faint"], tracking=1.3))
    if pulse and len(lanes[0]) > 1:
        o.append(pulse_mark(c, SPINE, lanes[0]))
    return "".join(o) + "</svg>"


# Each chain declares its own narrow copy. The wide grid has 728px of measure
# and the narrow one has 348px, so a string that fits one often will not fit
# the other - and fits() fails the build rather than clipping it.
SIGNAL = dict(
    title="One heartbeat, four hops",
    stats="TEAM OF 4 · MIT REALITY HACK 2026",
    pulse=True,
    groups=[("BIOMETRIC CHAIN", [
                ("PULSE SENSOR", "reads the pulse as an analog signal", None, None),
                ("ARDUINO", "turns it into BPM and IBI", None, None),
                ("WI-FI", "carries both values into Unity", None, None),
                ("UNITY SHADER", "breathing and pulsing effects, in real time", None,
                 "breathing and pulsing shaders, live")]),
            ("COMPANION APP", [
                ("PHONE", "a swiped card spawns an object in VR", None, None)])])

PIPELINE = dict(
    title="From vendor export to something plottable",
    short="Vendor export to something plottable",
    stats="SOFTWARE DEVELOPER INTERN · OCT 2024 – SEP 2025",
    stats_short="SOFTWARE DEV INTERN · 2024 – 2025",
    groups=[(None, [
                ("INGESTION", "wearable exports arrive, one format per vendor", None,
                 "exports arrive, one shape per vendor"),
                ("PROCESSING", "machine learning normalises the formats", "blue", None),
                ("ANALYTICS", "an interface researchers actually use", None, None)])])


def chain_svg(theme, spec, narrow=False):
    return chain(theme, spec["title"], spec["groups"], spec["stats"], narrow=narrow,
                 short=spec.get("short"), stats_short=spec.get("stats_short"),
                 pulse=spec.get("pulse", False))


# --------------------------------------------------------------------------
# Tenure
#
# The one figure here that shows something the tables cannot. A table of roles
# is a list of ranges, read one at a time; the finding is that three of them
# ran at once through one summer, and only a shared axis can show that.
#
# Drawn to a month scale, from the same dates the table below it carries, on
# the grid the bar figures already use: labels from --gutter, measurement
# starting at x=320. --muted for the roles, because they are the measurement;
# the two cover hues on the projects, marking the same two subjects they mark
# everywhere else. The hackathon is a dot, because a weekend has no length at
# this scale and a three-day bar would be a lie about its width.
# --------------------------------------------------------------------------

START, NOW = (2023, 1), (2026, 8)


def mo(ym):
    """Months since START. Whole months only: nothing here is finer than that."""
    return (ym[0] - START[0]) * 12 + (ym[1] - START[1])


MONTHS = mo(NOW) + 1                     # Jan 2023 through Aug 2026, inclusive

ROLES = [("Teaching Assistant", (2023, 1), NOW),
         ("Software Developer Intern", (2024, 10), (2025, 9)),
         ("Research Assistant", (2025, 5), (2025, 8))]

WORKS = [("bug classification", (2025, 1), (2025, 4), "blue"),
         ("annotation study", (2025, 5), (2025, 8), "teal"),
         ("BEAP Engine", (2024, 10), (2025, 9), None),
         ("Dreaming Machines", (2026, 1), None, None)]

TENURE_TITLE = "Three roles, one overlapping summer"
TENURE_STATS = "THREE ROLES · FOUR PROJECTS · JAN 2023 – AUG 2026"
TENURE_STATS_SHORT = "THREE ROLES · FOUR PROJECTS"

TENURE_ALT = (
    "Three roles, one overlapping summer. Teaching Assistant, January 2023 to "
    "now. Software Developer Intern, October 2024 to September 2025. Research "
    "Assistant, May to August 2025. All three overlap through the summer of "
    "2025. Projects: bug classification January to April 2025, annotation study "
    "May to August 2025, BEAP Engine October 2024 to September 2025, Dreaming "
    "Machines January 2026.")


def _years(o, c, x0, ppm, y0, y1, size, tracking, label_y):
    """Year gridlines and their labels. The scale is the same in both widths,
    so it is written once."""
    for yr in range(START[0], NOW[0] + 1):
        x = x0 + mo((yr, 1)) * ppm
        o.append(f'<line x1="{x:.1f}" y1="{y0}" x2="{x:.1f}" y2="{y1}" '
                 f'stroke="{c["line"]}" stroke-width="1"/>')
        o.append(text(str(yr), x, label_y, MONO, size, 500, c["faint"],
                      tracking=tracking))


def tenure(theme):
    c = THEMES[theme]
    W, H, CL, CR, X0 = 880, 468, 76, 804, 320
    ppm = (CR - X0) / MONTHS             # 11.0 px per month
    o = [head(W, H, TENURE_ALT),
         f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>',
         f'<rect x="24.5" y="24.5" width="831" height="423" rx="{R}" ry="{R}" '
         f'fill="{c["surface"]}" stroke="{c["line"]}" stroke-width="1"/>',
         text(fits(TENURE_TITLE, 17, CR - CL, -0.15), CL, 82, MONO, 17, 600,
              c["ink"], tracking=-0.15)]
    _years(o, c, X0, ppm, 120, 386, 11, 1.43, 112)

    o.append(text(fits("ROLES", 11, CR - CL, 1.3), CL, 142, MONO, 11, 500,
                  c["faint"], tracking=1.3))
    for i, (name, a, b) in enumerate(ROLES):
        top = 156 + i * 34
        fits(name, 14, X0 - CL - 20)
        o.append(text(name, CL, top + 15, SANS, 14, 400, c["ink-2"]))
        o.append(f'<rect x="{X0 + mo(a) * ppm:.1f}" y="{top}" '
                 f'width="{(mo(b) - mo(a) + 1) * ppm:.1f}" height="20" '
                 f'fill="{c["muted"]}"/>')

    # Same 29px from group label to first row as ROLES gets above.
    o.append(text(fits("PROJECTS", 11, CR - CL, 1.3), CL, 272, MONO, 11, 500,
                  c["faint"], tracking=1.3))
    for i, (name, a, b, hue) in enumerate(WORKS):
        top = 292 + i * 28
        fits(name, 14, X0 - CL - 20)
        o.append(text(name, CL, top + 9, SANS, 14, 400, c["ink-2"]))
        fill = c[hue] if hue else c["muted"]
        if b is None:
            o.append(f'<circle cx="{X0 + (mo(a) + 0.5) * ppm:.1f}" cy="{top + 5}" '
                     f'r="5" fill="{fill}"/>')
        else:
            o.append(f'<rect x="{X0 + mo(a) * ppm:.1f}" y="{top}" '
                     f'width="{(mo(b) - mo(a) + 1) * ppm:.1f}" height="10" '
                     f'fill="{fill}"/>')

    # The one thing on this figure with a state, so it gets the hue the
    # masthead's availability line gets. The measured axis stops here.
    o.append(f'<line x1="{CR}.5" y1="120" x2="{CR}.5" y2="386" '
             f'stroke="{c["teal"]}" stroke-width="1"/>')
    o.append(text(fits("NOW", 10, 44, 1.3), CR + 8, 112, MONO, 10, 500,
                  c["teal"], tracking=1.3))

    o.append(f'<line x1="{CL}" y1="406.5" x2="{CR}" y2="406.5" '
             f'stroke="{c["line"]}" stroke-width="1"/>')
    o.append(text(fits(TENURE_STATS, 11, CR - CL, 1.43), CL, 432, MONO, 11, 500,
                  c["faint"], tracking=1.43))
    return "".join(o) + "</svg>"


def tenure_narrow(theme):
    c = THEMES[theme]
    W, H, CL, CR, X0 = 420, 484, 36, 384, 36
    ppm = (CR - X0) / MONTHS
    o = [head(W, H, TENURE_ALT),
         f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>',
         f'<rect x="14.5" y="14.5" width="391" height="439" rx="{R}" ry="{R}" '
         f'fill="{c["surface"]}" stroke="{c["line"]}" stroke-width="1"/>',
         text(fits(TENURE_TITLE, 14, CR - CL, -0.15), CL, 62, MONO, 14, 600,
              c["ink"], tracking=-0.15)]
    _years(o, c, X0, ppm, 96, 402, 9, 1.0, 88)

    # Labels sit above their bars rather than beside them: the same flip the
    # site makes to its hero, and the only way a 25-character role name and a
    # 44-month axis both get the full measure.
    o.append(text(fits("ROLES", 10, CR - CL, 1.3), CL, 116, MONO, 10, 500,
                  c["faint"], tracking=1.3))
    for i, (name, a, b) in enumerate(ROLES):
        base = 140 + i * 40
        o.append(text(fits(name, 12, CR - CL), CL, base, SANS, 12, 400, c["ink-2"]))
        o.append(f'<rect x="{X0 + mo(a) * ppm:.1f}" y="{base + 6}" '
                 f'width="{(mo(b) - mo(a) + 1) * ppm:.1f}" height="12" '
                 f'fill="{c["muted"]}"/>')

    o.append(text(fits("PROJECTS", 10, CR - CL, 1.3), CL, 268, MONO, 10, 500,
                  c["faint"], tracking=1.3))
    for i, (name, a, b, hue) in enumerate(WORKS):
        base = 292 + i * 32
        o.append(text(fits(name, 12, CR - CL), CL, base, SANS, 12, 400, c["ink-2"]))
        fill = c[hue] if hue else c["muted"]
        if b is None:
            o.append(f'<circle cx="{X0 + (mo(a) + 0.5) * ppm:.1f}" cy="{base + 10}" '
                     f'r="4" fill="{fill}"/>')
        else:
            o.append(f'<rect x="{X0 + mo(a) * ppm:.1f}" y="{base + 6}" '
                     f'width="{(mo(b) - mo(a) + 1) * ppm:.1f}" height="8" '
                     f'fill="{fill}"/>')

    o.append(f'<line x1="{CR}.5" y1="96" x2="{CR}.5" y2="402" '
             f'stroke="{c["teal"]}" stroke-width="1"/>')
    # End-anchored, so it cannot drift into the 2026 tick the way a fixed
    # offset from the line did.
    o.append(text("NOW", CR, 88, MONO, 9, 500, c["teal"], tracking=1.0,
                  anchor="end"))

    o.append(f'<line x1="{CL}" y1="422.5" x2="{CR}" y2="422.5" '
             f'stroke="{c["line"]}" stroke-width="1"/>')
    o.append(text(fits(TENURE_STATS_SHORT, 10, CR - CL, 1.3), CL, 448, MONO, 10,
                  500, c["faint"], tracking=1.3))
    return "".join(o) + "</svg>"


# --------------------------------------------------------------------------
# Stack
#
# The skills table answers "which ones". It cannot answer "how much of this is
# current", because thirty-two names in fifteen cells all read at the same
# weight. So the figure counts them instead: one dot per entry, in the column
# for how current it is, and the shape of the answer is visible before any of
# it is read.
#
# No hue at all. The three levels are three weights of the same neutral mark,
# which is what the site's ramp is for, and a fluency level is not a subject.
# The table stays underneath: the names are the part a reader searches for.
# --------------------------------------------------------------------------

STACK = [("Languages", 3, 3, 3), ("Vision & ML", 3, 3, 1), ("Web", 2, 4, 1),
         ("Data", 1, 2, 1), ("Tools", 2, 2, 1)]

LEVELS = ("DAILY", "REGULAR", "FAMILIAR")

STACK_TITLE = "Thirty-two things, and where the daily weight sits"
STACK_TITLE_SHORT = "Thirty-two things, by how current"
STACK_STATS = "32 ENTRIES · 5 CATEGORIES · DAILY, REGULAR OR FAMILIAR"
STACK_STATS_SHORT = "32 ENTRIES · 5 CATEGORIES"

STACK_ALT = (
    "Thirty-two things, and where the daily weight sits. Counts are daily, "
    "regular, familiar. Languages 3, 3, 3. Vision and ML 3, 3, 1. Web 2, 4, 1. "
    "Data 1, 2, 1. Tools 2, 2, 1. Thirty-two entries in five categories.")


def _dot(c, x, y, level, r):
    """One entry. Filled, half-weight or hollow, for daily, regular, familiar."""
    if level == 0:
        return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c["ink-2"]}"/>'
    if level == 1:
        return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c["faint"]}"/>'
    return (f'<circle cx="{x}" cy="{y}" r="{r - 0.5}" fill="none" '
            f'stroke="{c["line-strong"]}" stroke-width="1.5"/>')


def stack(theme):
    c = THEMES[theme]
    W, H, CL, CR = 880, 372, 76, 804
    cols, pitch, r = (320, 480, 640), 20, 5
    o = [head(W, H, STACK_ALT),
         f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>',
         f'<rect x="24.5" y="24.5" width="831" height="323" rx="{R}" ry="{R}" '
         f'fill="{c["surface"]}" stroke="{c["line"]}" stroke-width="1"/>',
         text(fits(STACK_TITLE, 17, CR - CL, -0.15), CL, 82, MONO, 17, 600,
              c["ink"], tracking=-0.15)]
    for x, name in zip(cols, LEVELS):
        o.append(text(fits(name, 10, 150, 1.3), x - r, 118, MONO, 10, 500,
                      c["faint"], tracking=1.3))
    o.append(text("TOTAL", CR, 118, MONO, 10, 500, c["faint"], tracking=1.3,
                  anchor="end"))
    for i, row in enumerate(STACK):
        name, counts = row[0], row[1:]
        cy = 148 + i * 34
        fits(name, 14, cols[0] - CL - 20)
        o.append(text(name, CL, cy + 5, SANS, 14, 400, c["ink-2"]))
        for level, (x, n) in enumerate(zip(cols, counts)):
            for k in range(n):
                o.append(_dot(c, x + k * pitch, cy, level, r))
        o.append(text(str(sum(counts)), CR, cy + 5, MONO, 13, 600, c["ink"],
                      anchor="end"))
    o.append(f'<line x1="{CL}" y1="310.5" x2="{CR}" y2="310.5" '
             f'stroke="{c["line"]}" stroke-width="1"/>')
    o.append(text(fits(STACK_STATS, 11, CR - CL, 1.43), CL, 336, MONO, 11, 500,
                  c["faint"], tracking=1.43))
    return "".join(o) + "</svg>"


def stack_narrow(theme):
    c = THEMES[theme]
    W, H, CL, CR = 420, 412, 36, 384
    pitch, gap, r = 14, 10, 4.5
    o = [head(W, H, STACK_ALT),
         f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>',
         f'<rect x="14.5" y="14.5" width="391" height="367" rx="{R}" ry="{R}" '
         f'fill="{c["surface"]}" stroke="{c["line"]}" stroke-width="1"/>',
         text(fits(STACK_TITLE_SHORT, 14, CR - CL, -0.15), CL, 62, MONO, 14, 600,
              c["ink"], tracking=-0.15)]
    # One legend line, because the three columns collapse into one row here and
    # the mark is the only thing left distinguishing the levels.
    x = CL
    for level, name in enumerate(LEVELS):
        o.append(_dot(c, x + r, 88 - 4, level, r))
        o.append(text(fits(name, 9, 70, 1.1), x + 2 * r + 6, 88, MONO, 9, 500,
                      c["faint"], tracking=1.1))
        x += 2 * r + 6 + len(name) * 0.62 * 9 + (len(name) - 1) * 1.1 + 16
    for i, row in enumerate(STACK):
        name, counts = row[0], row[1:]
        base = 128 + i * 44
        o.append(text(fits(name, 12, CR - CL - 40), CL, base, SANS, 12, 400,
                      c["ink-2"]))
        o.append(text(str(sum(counts)), CR, base, MONO, 12, 600, c["ink"],
                      anchor="end"))
        x = CL + r
        for level, n in enumerate(counts):
            for k in range(n):
                o.append(_dot(c, x, base + 16, level, r))
                x += pitch
            x += gap
        assert x <= CR, f"{name}: dots run {x - CR:.0f}px past the measure"
    o.append(f'<line x1="{CL}" y1="352.5" x2="{CR}" y2="352.5" '
             f'stroke="{c["line"]}" stroke-width="1"/>')
    o.append(text(fits(STACK_STATS_SHORT, 10, CR - CL, 1.3), CL, 376, MONO, 10,
                  500, c["faint"], tracking=1.3))
    return "".join(o) + "</svg>"


def main():
    OUT.mkdir(exist_ok=True)
    n = 0
    for theme in ("light", "dark"):
        sfx = "" if theme == "light" else "-dark"   # light is canonical
        for stem, body in (("masthead", masthead(theme)),
                           ("masthead-narrow", masthead_narrow(theme)),
                           ("study", study(theme)),
                           ("bench", bench(theme)),
                           ("bench-narrow", bench_narrow(theme)),
                           ("signal", chain_svg(theme, SIGNAL)),
                           ("signal-narrow", chain_svg(theme, SIGNAL, narrow=True)),
                           ("pipeline", chain_svg(theme, PIPELINE)),
                           ("pipeline-narrow", chain_svg(theme, PIPELINE, narrow=True)),
                           ("study-narrow", study_narrow(theme)),
                           ("tenure", tenure(theme)),
                           ("tenure-narrow", tenure_narrow(theme)),
                           ("stack", stack(theme)),
                           ("stack-narrow", stack_narrow(theme))):
            path = OUT / f"{stem}{sfx}.svg"
            low = body.lower()
            bad = [b for b in BANNED if b in low]
            assert not bad, f"{path.name}: {bad} - accent or shadow in a static asset"
            path.write_text(body)
            n += 1
    print(f"wrote {n} svg files to assets/")


if __name__ == "__main__":
    main()
