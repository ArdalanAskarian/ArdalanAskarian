#!/usr/bin/env python3
"""
Build the two SVG figures used by README.md.

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
    "under Dr. Mark Eramian.")


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
    W, H, CL = 880, 336, 76          # --gutter 24 + --frame-pad 52
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
    o.append("</g>" + edge(p, c, W, H))
    return "".join(o) + "</svg>"


def masthead_narrow(theme):
    c = THEMES[theme]
    W, H, CL = 420, 372, 36          # clamp floors: gutter 14 + frame-pad 22
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


def chain(theme, title, groups, stats, narrow=False, short=None,
          stats_short=None):
    """A labelled sequence on the shared spine. `groups` is a list of
    (group_label | None, [(step, description, hue_or_None), ...])."""
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
    for label, steps in groups:
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
            spine_bot = y - 4
            y += pitch
    o.insert(4, f'<line x1="{SPINE}.5" y1="{spine_top}" x2="{SPINE}.5" y2="{spine_bot}" '
                f'stroke="{c["line"]}" stroke-width="1"/>')
    fy = H - 62
    o.append(f'<line x1="{CL}" y1="{fy}.5" x2="{CR}" y2="{fy}.5" stroke="{c["line"]}" stroke-width="1"/>')
    o.append(text(fits(stats, 10 if narrow else 11, CR - CL, 1.3), CL, fy + 26, MONO,
                  10 if narrow else 11, 500, c["faint"], tracking=1.3))
    return "".join(o) + "</svg>"


# Each chain declares its own narrow copy. The wide grid has 728px of measure
# and the narrow one has 348px, so a string that fits one often will not fit
# the other - and fits() fails the build rather than clipping it.
SIGNAL = dict(
    title="One heartbeat, four hops",
    stats="TEAM OF 4 · MIT REALITY HACK 2026",
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
                 short=spec.get("short"), stats_short=spec.get("stats_short"))


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
                           ("study-narrow", study_narrow(theme))):
            path = OUT / f"{stem}{sfx}.svg"
            low = body.lower()
            bad = [b for b in BANNED if b in low]
            assert not bad, f"{path.name}: {bad} - accent or shadow in a static asset"
            path.write_text(body)
            n += 1
    print(f"wrote {n} svg files to assets/")


if __name__ == "__main__":
    main()
