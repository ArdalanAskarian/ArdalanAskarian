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


def main():
    OUT.mkdir(exist_ok=True)
    n = 0
    for theme in ("light", "dark"):
        sfx = "" if theme == "light" else "-dark"   # light is canonical
        for stem, body in (("masthead", masthead(theme)),
                           ("masthead-narrow", masthead_narrow(theme)),
                           ("study", study(theme)),
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
