#!/usr/bin/env python3
"""
Build every SVG asset used by README.md.

The README's design lives here. GitHub strips CSS from markdown, so the only way
to control type and colour is to commit SVG and reference it as <img>. An SVG in
<img> context cannot fetch web fonts, so all display type is converted to vector
outlines at build time.

Fonts are fetched into tools/fonts/ by tools/fetch_fonts.sh and are never
committed. Both are OFL, which permits outlining and redistributing the paths.

    python3 tools/build_svg.py

Requires: fontTools (build-time only; ships in nothing).
"""

from pathlib import Path

from fontTools.misc.transform import Transform
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "tools" / "fonts"
OUT = ROOT / "assets"


# --------------------------------------------------------------------------
# Tokens
#
# Palette is derived from matplotlib's `magma` colormap - the ramp that appears
# in every feature-map figure in computer vision. Not a generic dev palette.
# The ramp encodes something wherever it is used (recency, depth of use); it is
# never applied as decoration.
# --------------------------------------------------------------------------

THEMES = {
    "dark": {
        "ground": "#0B0716",  # warm near-black plum, not neutral black
        "plate": "#140C2B",
        "rule": "#4F0C6B",
        "muted": "#9E82BA",  # 6.0:1 on ground; #8A6BA8 sat on the 4.5:1 line
        "body": "#CFC4E0",
        "display": "#F4EFFA",
        "mid": "#B5367A",
        "signal": "#E55C30",  # detection overlay only
        "peak": "#FBA40A",  # the single most important number only
    },
    "light": {
        "ground": "#F7F5FB",  # lilac-tinted, deliberately not cream
        "plate": "#EFEAF7",
        "rule": "#C9B8DC",
        "muted": "#6E5C86",
        "body": "#3B3050",
        "display": "#2A2140",
        "mid": "#A32E6D",
        "signal": "#C9421D",  # darkened for contrast on paper
        "peak": "#A85B06",  # burnt amber, not olive; 4.7:1 on paper for the label
    },
}

RAMP = ["rule", "mid", "signal", "peak"]


# --------------------------------------------------------------------------
# Font plumbing
# --------------------------------------------------------------------------

_cache = {}


def load(name):
    """Return a TTFont, instantiating Archivo's variable axes on first use."""
    if name in _cache:
        return _cache[name]
    if name.startswith("archivo"):
        # wdth=125 is Archivo's Expanded end. Reads as an instrument panel /
        # figure plate rather than a startup landing page, and it is not the
        # README default (JetBrains Mono / Fira Code).
        weight = {"archivo-bold": 700, "archivo-med": 500}[name]
        f = instantiateVariableFont(
            TTFont(FONTS / "Archivo.ttf"), {"wdth": 125, "wght": weight}
        )
    else:
        f = TTFont(FONTS / {"plex": "PlexMono-Reg.ttf", "plex-sb": "PlexMono-SBd.ttf"}[name])
    _cache[name] = f
    return f


def measure(font_name, text, size, tracking=0.0):
    f = load(font_name)
    gs, cmap = f.getGlyphSet(), f.getBestCmap()
    upem = f["head"].unitsPerEm
    w = 0.0
    for ch in text:
        g = cmap.get(ord(ch))
        if g is None:
            continue
        w += gs[g].width * size / upem + tracking
    return w - tracking if text else 0.0


def outline(font_name, text, size, x, y, tracking=0.0, anchor="start"):
    """Convert `text` to an SVG path `d` string with baseline at (x, y)."""
    f = load(font_name)
    gs, cmap = f.getGlyphSet(), f.getBestCmap()
    upem = f["head"].unitsPerEm
    scale = size / upem

    if anchor == "middle":
        x -= measure(font_name, text, size, tracking) / 2
    elif anchor == "end":
        x -= measure(font_name, text, size, tracking)

    parts, cx = [], x
    for ch in text:
        g = cmap.get(ord(ch))
        if g is None:
            continue
        pen = SVGPathPen(gs, ntos=lambda v: f"{v:.1f}")
        # Glyph space is y-up from the baseline; SVG is y-down. Flip and place.
        gs[g].draw(TransformPen(pen, Transform(scale, 0, 0, -scale, cx, y)))
        d = pen.getCommands()
        if d:
            parts.append(d)
        cx += gs[g].width * scale + tracking
    return " ".join(parts)


def text_path(font_name, text, size, x, y, fill, tracking=0.0, anchor="start",
              opacity=None, cls=None):
    d = outline(font_name, text, size, x, y, tracking, anchor)
    if not d:
        return ""
    attrs = [f'd="{d}"', f'fill="{fill}"']
    if opacity is not None:
        attrs.append(f'opacity="{opacity}"')
    if cls:
        attrs.append(f'class="{cls}"')
    return f"<path {' '.join(attrs)}/>"


# --------------------------------------------------------------------------
# Figure 1 - the hero plate
#
# The page opens as a journal figure, not a banner: the name rendered as the
# subject of a detection pass, in the visual language of his own SIFT research.
# --------------------------------------------------------------------------

# Keypoints cluster along the cap-height and baseline bands of the wordmark -
# where a corner detector actually fires - rather than scattering evenly over
# the glyph bodies. Radii vary by an order of magnitude, as real SIFT scales do,
# and the field stays under the type so the name is never obscured.
# (cx, cy, radius, orientation deg)
KEYPOINTS = [
    # line 1, cap-height band
    (90, 148, 7, 40), (155, 156, 12, 190), (225, 146, 5, 110), (300, 152, 26, 300),
    (370, 148, 6, 25), (440, 158, 9, 215), (512, 150, 14, 160), (572, 145, 6, 80),
    # line 1, baseline band
    (112, 212, 10, 255), (190, 204, 6, 15), (266, 214, 17, 130), (340, 206, 7, 290),
    (416, 212, 11, 60), (492, 204, 5, 340), (556, 210, 8, 175),
    # line 2, cap-height band
    (80, 238, 6, 95), (152, 246, 13, 205), (222, 240, 8, 300), (296, 248, 5, 140),
    (366, 238, 31, 45), (436, 246, 7, 265), (506, 240, 10, 120), (578, 244, 6, 200),
    # line 2, baseline band
    (102, 300, 9, 180), (176, 294, 6, 60), (252, 302, 15, 250), (326, 296, 8, 320),
    (402, 300, 12, 100), (472, 294, 5, 20), (542, 302, 22, 230), (604, 296, 11, 150),
]

# The figure's data legend. Real numbers from the study, and the reason the
# `peak` token exists: it marks the one finding the whole page is built around.
LEGEND = [
    ("participants", "6", "body"),
    ("interaction events", "36,407", "body"),
    ("annotation time", "+71.6%", "peak"),
    ("IoU / GTC gain", "none", "mid"),
]


def hero(theme):
    c = THEMES[theme]
    W, H = 1000, 440
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'width="{W}" height="{H}" role="img" aria-labelledby="t">',
         '<title id="t">Ardalan Askarian - M.Sc. Computer Science, University of '
         'Saskatchewan. Computer vision and applied machine learning.</title>']

    # Deliberately static.
    #
    # An earlier build had a 2.3s reveal sequence here. Two things killed it:
    # `prefers-reduced-motion` does not reliably reach an SVG loaded through
    # <img>, and any delayed reveal means the plate renders INCOMPLETE - no
    # brackets, no chip, no caption - for anything that snapshots early or
    # never runs CSS at all (crawlers, social cards, GitHub's own previews).
    # The figure reads the same at rest, so the motion was pure fragility.
    o.append(f'<rect width="{W}" height="{H}" fill="{c["ground"]}"/>')
    o.append(f'<rect x="20.5" y="20.5" width="{W-41}" height="{H-41}" fill="none" '
             f'stroke="{c["rule"]}" stroke-width="1"/>')

    # Figure header
    o.append(text_path("plex-sb", "FIG. 1", 12, 48, 62, c["mid"], tracking=1.6))
    o.append(text_path("plex", "SIFT DETECTION PASS", 12, W - 48, 62, c["muted"],
                       tracking=1.6, anchor="end"))

    # Keypoint field - circle sized by scale with an orientation spoke, the
    # actual SIFT visualisation idiom. Drawn BEFORE the wordmark so the type
    # stays crisp and the detections read as a layer the subject sits in.
    # Nested groups so the CSS scale animation cannot clobber the translate.
    from math import cos, sin, radians
    for i, (cx, cy, r, ang) in enumerate(KEYPOINTS):
        ex, ey = r * cos(radians(ang)), -r * sin(radians(ang))
        o.append(
            f'<g transform="translate({cx},{cy})" opacity=".65">'
            f'<g>'
            f'<circle r="{r}" fill="none" stroke="{c["signal"]}" stroke-width="1.2"/>'
            f'<line x1="0" y1="0" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{c["signal"]}" stroke-width="1.2"/>'
            f'</g></g>')

    # Subject: the wordmark, stacked for monumentality
    o.append(text_path("archivo-bold", "ARDALAN", 78, 62, 210, c["display"], tracking=1.5))
    o.append(text_path("archivo-bold", "ASKARIAN", 78, 62, 296, c["display"], tracking=1.5))

    # Corner brackets rather than a full box - detection UI that does not cage
    # the type. Sized to the measured wordmark, not guessed.
    mark_w = max(measure("archivo-bold", s, 78, 1.5) for s in ("ARDALAN", "ASKARIAN"))
    bx, by, leg = 44, 128, 30
    bw, bh = mark_w + 56, 198
    for px, py, sx, sy in ((bx, by, 1, 1), (bx+bw, by, -1, 1),
                           (bx, by+bh, 1, -1), (bx+bw, by+bh, -1, -1)):
        o.append(f'<path d="M {px:.1f} {py+sy*leg} L {px:.1f} {py} L {px+sx*leg:.1f} {py}" '
                 f'fill="none" stroke="{c["signal"]}" stroke-width="2"/>')

    # Confidence chip - the detector's readout on the subject
    chip = "subject · 0.98"
    cw = measure("plex-sb", chip, 12, 0.6) + 24
    o.append(f'<g><rect x="{bx}" y="{by-30}" width="{cw:.1f}" height="22" '
             f'fill="{c["signal"]}"/>')
    o.append(text_path("plex-sb", chip, 12, bx + 12, by - 14, c["ground"], tracking=0.6) + "</g>")

    # Data legend, right column - what a figure plate actually carries.
    # Vertically set against the wordmark block rather than floating high.
    lx, rx, ly = 700, W - 48, 180
    o.append(f'<line x1="{lx}" y1="{ly-34}" x2="{rx}" y2="{ly-34}" stroke="{c["rule"]}" stroke-width="1"/>')
    for n, (label, value, tone) in enumerate(LEGEND):
        y = ly + n * 39
        o.append(text_path("plex", label, 11.5, lx, y, c["muted"], tracking=0.3))
        o.append(text_path("plex-sb", value, 15, rx, y + 1, c[tone], tracking=0.3, anchor="end"))

    # Identity and caption - the figure's own words
    o.append('<g>')
    o.append(f'<line x1="62" y1="352" x2="{W-62}" y2="352" stroke="{c["rule"]}" stroke-width="1"/>')
    o.append(text_path("plex", "M.Sc. Computer Science  ·  University of Saskatchewan  ·  Computer Vision & Applied ML",
                       13, 62, 382, c["body"], tracking=0.2))
    o.append(text_path("plex", "SIFT-assisted annotation measured against a manual baseline. Negative results are results.",
                       11.5, 62, 406, c["muted"], tracking=0.2))
    o.append("</g></svg>")
    return "\n".join(o)


# --------------------------------------------------------------------------
# Figure 2 - the study
#
# The finding itself, drawn to scale. Bar length encodes the measured result;
# the `peak` segment is the 71.6% overhead. This is the one place `peak` is
# allowed to appear, which is what makes it mean something in Fig. 1 too.
# --------------------------------------------------------------------------

def study(theme):
    c = THEMES[theme]
    W, H = 1000, 330
    BASE_W, X0 = 300.0, 240  # 300px == the manual baseline == 1.00x
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'width="{W}" height="{H}" role="img" aria-labelledby="t2">',
         '<title id="t2">Annotation time, SIFT-assisted versus manual baseline. '
         'Assisted annotation took 1.72 times as long, a 71.6% increase, with no '
         'measurable gain in IoU or ground-truth-coverage quality.</title>']

    o.append(f'<rect width="{W}" height="{H}" fill="{c["ground"]}"/>')
    o.append(f'<rect x="20.5" y="20.5" width="{W-41}" height="{H-41}" fill="none" '
             f'stroke="{c["rule"]}" stroke-width="1"/>')

    o.append(text_path("plex-sb", "FIG. 2", 12, 48, 62, c["mid"], tracking=1.6))
    o.append(text_path("plex", "MEAN ANNOTATION TIME PER IMAGE", 12, W - 48, 62,
                       c["muted"], tracking=1.6, anchor="end"))
    o.append(f'<line x1="48" y1="84" x2="{W-48}" y2="84" stroke="{c["rule"]}" stroke-width="1"/>')

    bars = [("manual baseline", 1.00, False), ("SIFT-assisted", 1.716, True)]
    for n, (label, factor, overhead) in enumerate(bars):
        y = 128 + n * 62
        o.append(text_path("plex", label, 13, 48, y + 18, c["body"], tracking=0.2))
        full = BASE_W * factor
        # The shared baseline portion, then the overhead in `peak`
        o.append(f'<rect x="{X0}" y="{y}" width="{BASE_W:.1f}" height="26" fill="{c["mid"]}"/>')
        if overhead:
            o.append(f'<rect x="{X0+BASE_W:.1f}" y="{y}" width="{full-BASE_W:.1f}" '
                     f'height="26" fill="{c["peak"]}"/>')
        o.append(text_path("plex-sb", f"{factor:.2f}×", 14, X0 + full + 16, y + 19,
                           c["peak"] if overhead else c["body"], tracking=0.3))

    # The overhead callout, tied to the bar segment it describes
    ox = X0 + BASE_W
    ow = BASE_W * 1.716 - BASE_W
    o.append(f'<line x1="{ox:.1f}" y1="{190+26+10}" x2="{ox+ow:.1f}" y2="{190+26+10}" '
             f'stroke="{c["peak"]}" stroke-width="1"/>')
    o.append(text_path("plex-sb", "+71.6%", 12, ox + ow / 2, 190 + 26 + 28, c["peak"],
                       tracking=0.4, anchor="middle"))

    o.append(f'<line x1="48" y1="272" x2="{W-48}" y2="272" stroke="{c["rule"]}" stroke-width="1"/>')
    o.append(text_path("plex", "IoU and ground-truth coverage: no measurable gain over the manual baseline.",
                       12.5, 48, 296, c["body"], tracking=0.2))
    return "\n".join(o) + "</svg>"


# --------------------------------------------------------------------------
# Stack - grouped by domain, each item marked by how deeply it is actually
# used. The mark is an honest encoding, not a proficiency bar with no source.
# `peak` is deliberately absent here so it stays unique to the Fig. 1 finding.
# --------------------------------------------------------------------------

DEPTH = ["signal", "mid", "muted"]  # daily / regular / familiar

STACK = [
    ("LANGUAGES", [("Python", 0), ("TypeScript", 0), ("JavaScript", 0), ("C", 1),
                   ("Java", 1), ("SQL", 1), ("C#", 2), ("PHP", 2), ("R", 2)]),
    ("VISION & ML", [("PyTorch", 0), ("OpenCV", 0), ("scikit-learn", 1), ("TensorFlow", 2)]),
    ("WEB", [("React", 0), ("Django", 0), ("Node.js", 1), ("Next.js", 1),
             ("React Native", 1), ("Flask", 2), ("Express", 2)]),
    ("DATA", [("PostgreSQL", 0), ("MongoDB", 1), ("MySQL", 1), ("SQLite", 2)]),
    ("TOOLS", [("Git", 0), ("Linux", 0), ("Docker", 1), ("Playwright", 1), ("Unity", 2)]),
]


def stack(theme):
    c = THEMES[theme]
    W = 1000
    LX, IX, ROW = 48, 200, 46
    o = []
    y = 46
    for group, items in STACK:
        o.append(text_path("plex-sb", group, 11.5, LX, y + 4, c["muted"], tracking=1.8))
        x = IX
        for name, depth in items:
            w = measure("plex", name, 13, 0.2)
            if x + w + 22 > W - 48:  # wrap
                x, y = IX, y + 26
                o.append("")
            o.append(f'<rect x="{x}" y="{y-8}" width="7" height="7" fill="{c[DEPTH[depth]]}"/>')
            o.append(text_path("plex", name, 13, x + 15, y, c["body"], tracking=0.2))
            x += w + 34
        y += ROW
    body = "\n".join(p for p in o if p)
    H = y + 34

    head = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
            f'width="{W}" height="{H}" role="img" aria-labelledby="t3">',
            '<title id="t3">Technical stack grouped by domain, each item marked '
            'daily, regular, or familiar.</title>',
            f'<rect width="{W}" height="{H}" fill="{c["ground"]}"/>']

    # Legend - the mark has to explain itself or it is decoration
    lx = LX
    foot = [f'<line x1="{LX}" y1="{H-46}" x2="{W-48}" y2="{H-46}" stroke="{c["rule"]}" stroke-width="1"/>']
    for label, tone in (("daily", DEPTH[0]), ("regular", DEPTH[1]), ("familiar", DEPTH[2])):
        foot.append(f'<rect x="{lx}" y="{H-26}" width="7" height="7" fill="{c[tone]}"/>')
        foot.append(text_path("plex", label, 11.5, lx + 15, H - 19, c["muted"], tracking=0.2))
        lx += measure("plex", label, 11.5, 0.2) + 46
    return "\n".join(head + [body] + foot) + "</svg>"


# --------------------------------------------------------------------------
# Link chips - replacing shields.io, in the page's own palette
# --------------------------------------------------------------------------

LINKS = [("linkedin", "LINKEDIN"), ("email", "EMAIL"),
         ("portfolio", "PORTFOLIO"), ("github", "GITHUB")]


def link_chip(label, theme):
    c = THEMES[theme]
    H = 34
    tw = measure("plex-sb", label, 12, 2.0)
    W = int(tw + 40)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'width="{W}" height="{H}" role="img">']
    o.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" fill="{c["plate"]}" '
             f'stroke="{c["rule"]}" stroke-width="1"/>')
    o.append(f'<rect x="0.5" y="0.5" width="3" height="{H-1}" fill="{c["signal"]}"/>')
    o.append(text_path("plex-sb", label, 12, 18, H/2 + 4.5, c["body"], tracking=2.0))
    o.append("</svg>")
    return "\n".join(o)


def main():
    OUT.mkdir(exist_ok=True)
    written = []
    for theme in ("dark", "light"):
        sfx = "" if theme == "dark" else "-light"
        files = {f"hero{sfx}.svg": hero(theme),
                 f"study{sfx}.svg": study(theme),
                 f"stack{sfx}.svg": stack(theme)}
        for key, label in LINKS:
            files[f"link-{key}{sfx}.svg"] = link_chip(label, theme)
        for name, body in files.items():
            (OUT / name).write_text(body)
            written.append(name)
    print(f"wrote {len(written)} svg files to assets/")


if __name__ == "__main__":
    main()
