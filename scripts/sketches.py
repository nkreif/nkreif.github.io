"""Inline SVG "method sketches" used on index.html and research.html.

Run `python scripts/sketches.py` to (re)insert them. Each sketch is inserted
once, immediately before its anchor on index.html (the numbered cards) or
after its anchor on research.html (the strand headings). Existing sketches
are removed first, so the script is safe to run repeatedly.
"""
from __future__ import annotations

import math
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

AC = "var(--accent)"
HI = "var(--highlight)"
MU = "var(--ink-3)"
SOFT = "var(--accent-soft)"
BG = "var(--bg-elev)"
INK = "var(--ink-2)"
LINE = 'fill="none" stroke-linecap="round" stroke-linejoin="round"'


def svg(body: str, defs: str = "", title: str = "") -> str:
    d = f"<defs>{defs}</defs>" if defs else ""
    return (
        f'<svg class="sketch" viewBox="0 0 240 150" role="img" aria-label="{title}" '
        f'xmlns="http://www.w3.org/2000/svg">{d}{body}</svg>'
    )


def txt(x, y, s, anchor="middle", size=9, fill=INK, extra=""):
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" '
        f'font-family="Inter, system-ui, sans-serif" fill="{fill}" {extra}>{s}</text>'
    )


def policy_tree() -> str:
    def box(x, y, w=50, h=20):
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{BG}" stroke="{AC}" stroke-width="1.6"/>'

    b = [box(95, 12), box(45, 60), box(145, 60)]
    b.append(
        f'<path d="M120 32 L70 60 M120 32 L170 60 M70 80 L40 110 M70 80 L100 110 '
        f'M170 80 L140 110 M170 80 L200 110" stroke="{MU}" stroke-width="1.4" {LINE}/>'
    )
    for x, filled in [(40, True), (100, False), (140, True), (200, False)]:
        b.append(f'<circle cx="{x}" cy="112" r="9" fill="{AC if filled else BG}" stroke="{AC}" stroke-width="1.6"/>')
        b.append(txt(x, 136, "treat" if filled else "no", size=8, fill=MU))
    b.append(txt(120, 26, "x&#8321; &lt; c&#8321;", size=8))
    b.append(txt(70, 74, "x&#8322; &lt; c&#8322;", size=8))
    b.append(txt(170, 74, "x&#8323; &lt; c&#8323;", size=8))
    return svg("".join(b), title="Sketch of a policy tree assigning treatment by subgroup")


def dag() -> str:
    defs = (
        f'<marker id="ah-dag" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" '
        f'orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{MU}"/></marker>'
    )
    nodes = {
        "L0": (35, 38, "L&#8320;", MU, BG),
        "A0": (35, 112, "A&#8320;", AC, SOFT),
        "L1": (120, 38, "L&#8321;", MU, BG),
        "A1": (120, 112, "A&#8321;", AC, SOFT),
        "Y": (208, 75, "Y", HI, BG),
    }
    r = 15

    def edge(a, c):
        x1, y1 = nodes[a][:2]
        x2, y2 = nodes[c][:2]
        dx, dy = x2 - x1, y2 - y1
        d = math.hypot(dx, dy)
        ux, uy = dx / d, dy / d
        return (
            f'<line x1="{x1 + ux * (r + 1):.1f}" y1="{y1 + uy * (r + 1):.1f}" '
            f'x2="{x2 - ux * (r + 3):.1f}" y2="{y2 - uy * (r + 3):.1f}" '
            f'stroke="{MU}" stroke-width="1.4" marker-end="url(#ah-dag)"/>'
        )

    b = [edge(a, c) for a, c in [("L0", "A0"), ("L0", "L1"), ("A0", "L1"), ("L1", "A1"), ("A0", "A1"), ("A1", "Y"), ("L1", "Y")]]
    for x, y, lab, col, fill in nodes.values():
        b.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{col}" stroke-width="1.8"/>')
        b.append(txt(x, y + 4, lab, size=10, fill=INK))
    b.append(txt(35, 140, "time &#8594;", anchor="start", size=8, fill=MU))
    return svg("".join(b), defs, title="Sketch of a causal diagram with time-varying treatment and confounders")


def synth() -> str:
    tr = [(30, 80), (55, 75), (80, 78), (105, 70), (130, 72), (155, 85), (180, 95), (205, 100), (225, 104)]
    sy = [(30, 80), (55, 76), (80, 77), (105, 71), (130, 72), (155, 68), (180, 66), (205, 62), (225, 60)]
    P = lambda pts: " ".join(f"{x},{y}" for x, y in pts)
    gap = [p for p in tr if p[0] >= 130] + [p for p in reversed(sy) if p[0] >= 130]
    b = [
        f'<path d="M30 15 L30 125 L225 125" stroke="{MU}" stroke-width="1.2" {LINE}/>',
        f'<polygon points="{P(gap)}" fill="{SOFT}"/>',
        f'<polyline points="{P(sy)}" stroke="{AC}" stroke-width="1.6" stroke-dasharray="4 3" {LINE}/>',
        f'<polyline points="{P(tr)}" stroke="{AC}" stroke-width="2" {LINE}/>',
        f'<line x1="130" y1="18" x2="130" y2="125" stroke="{HI}" stroke-width="1.4" stroke-dasharray="3 3"/>',
        txt(133, 26, "policy", anchor="start", size=8, fill=HI),
        txt(224, 52, "synthetic", anchor="end", size=7, fill=MU),
        txt(224, 117, "treated", anchor="end", size=7, fill=MU),
        txt(225, 138, "time", anchor="end", size=8, fill=MU),
    ]
    return svg("".join(b), title="Sketch of a synthetic control comparison before and after a policy")


def dist_bars() -> str:
    b = [f'<path d="M30 15 L30 125 L225 125" stroke="{MU}" stroke-width="1.2" {LINE}/>']
    hs = [8, 22, 44, 68, 88]
    for i, h in enumerate(hs):
        x = 45 + i * 36
        b.append(f'<rect x="{x}" y="{125 - h}" width="24" height="{h}" rx="3" fill="{SOFT}" stroke="{AC}" stroke-width="1.5"/>')
    avg = 125 - sum(hs) / len(hs)
    b.append(f'<line x1="30" y1="{avg:.0f}" x2="225" y2="{avg:.0f}" stroke="{HI}" stroke-width="1.4" stroke-dasharray="3 3"/>')
    b.append(txt(224, avg - 4, "average", anchor="end", size=8, fill=HI))
    b.append(txt(128, 140, "baseline quality &#8594;", size=8, fill=MU))
    b.append(txt(20, 72, "effect", size=8, fill=MU, extra='transform="rotate(-90 20 72)"'))
    return svg("".join(b), title="Sketch of policy effects that vary with baseline quality")


def event_study() -> str:
    b = [
        f'<line x1="30" y1="85" x2="225" y2="85" stroke="{MU}" stroke-width="1.2" stroke-dasharray="2 3"/>',
        f'<line x1="130" y1="18" x2="130" y2="130" stroke="{HI}" stroke-width="1.4" stroke-dasharray="3 3"/>',
        txt(133, 26, "event", anchor="start", size=8, fill=HI),
    ]
    for x, y, e in [(45, 83, 10), (72, 88, 10), (100, 84, 9), (160, 106, 11), (190, 113, 11), (218, 110, 12)]:
        b.append(f'<line x1="{x}" y1="{y - e}" x2="{x}" y2="{y + e}" stroke="{AC}" stroke-width="1.4"/>')
        b.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{AC}"/>')
    b.append(txt(30, 140, "before", anchor="start", size=8, fill=MU))
    b.append(txt(225, 140, "after", anchor="end", size=8, fill=MU))
    return svg("".join(b), title="Sketch of an event study with effects appearing after exposure")


def ite_dist() -> str:
    curve = "M30 125 C 70 125, 85 40, 115 40 C 145 40, 165 125, 225 125"
    defs = '<clipPath id="clip-ite"><rect x="150" y="0" width="90" height="150"/></clipPath>'
    b = [
        f'<path d="M30 15 L30 125 L225 125" stroke="{MU}" stroke-width="1.2" {LINE}/>',
        f'<path d="{curve} Z" fill="{SOFT}" clip-path="url(#clip-ite)"/>',
        f'<path d="{curve}" stroke="{AC}" stroke-width="2" {LINE}/>',
        f'<line x1="150" y1="18" x2="150" y2="125" stroke="{HI}" stroke-width="1.4" stroke-dasharray="3 3"/>',
        txt(154, 26, "treat &#8594;", anchor="start", size=8, fill=HI),
        txt(128, 140, "individual treatment effect &#8594;", size=8, fill=MU),
    ]
    return svg("".join(b), defs, title="Sketch of a distribution of individual treatment effects with a targeting threshold")


def ce_plane() -> str:
    rnd = random.Random(7)
    b = [
        f'<path d="M20 75 L236 75 M128 10 L128 140" stroke="{MU}" stroke-width="1.2" {LINE}/>',
        f'<line x1="128" y1="75" x2="230" y2="22" stroke="{HI}" stroke-width="1.4" stroke-dasharray="3 3"/>',
    ]
    for _ in range(34):
        x = min(max(128 + rnd.gauss(38, 22), 24), 234)
        y = min(max(75 - rnd.gauss(28, 20), 14), 138)
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="{AC}" fill-opacity="0.75"/>')
    b.append(txt(234, 86, "&#916; effect", anchor="end", size=8, fill=MU))
    b.append(txt(132, 20, "&#916; cost", anchor="start", size=8, fill=MU))
    b.append(txt(222, 18, "threshold", anchor="end", size=7, fill=HI))
    return svg("".join(b), title="Sketch of a cost-effectiveness plane with an uncertainty cloud")


SKETCHES = {
    "tree": policy_tree,
    "dag": dag,
    "synth": synth,
    "bars": dist_bars,
    "event": event_study,
    "ite": ite_dist,
    "ce": ce_plane,
}

SKETCH_RE = re.compile(r'\s*<svg class="sketch".*?</svg>', re.S)

INDEX_PLACEMENTS = [("01", "tree"), ("02", "dag"), ("03", "synth")]
RESEARCH_PLACEMENTS = [
    ("Causal inference for comparative effectiveness and economic evaluation", "ce"),
    ("Causal machine learning and policy learning", "ite"),
    ("Quasi-experimental evaluation of health policies", "synth"),
    ("Health systems in low- and middle-income countries", "bars"),
    ("Conflict, violence, mental health and economic outcomes", "event"),
]


def main() -> None:
    index = ROOT / "index.html"
    s = SKETCH_RE.sub("", index.read_text(encoding="utf-8"))
    for num, key in INDEX_PLACEMENTS:
        anchor = f'<span class="num">{num}</span>'
        assert anchor in s, anchor
        s = s.replace(anchor, SKETCHES[key]() + "\n          " + anchor, 1)
    index.write_text(s, encoding="utf-8")

    research = ROOT / "research.html"
    s = SKETCH_RE.sub("", research.read_text(encoding="utf-8"))
    for heading, key in RESEARCH_PLACEMENTS:
        anchor = f"<h2>{heading}</h2>"
        assert anchor in s, anchor
        s = s.replace(anchor, anchor + "\n        " + SKETCHES[key](), 1)
    research.write_text(s, encoding="utf-8")
    print("Inserted", len(INDEX_PLACEMENTS), "sketches in index.html and", len(RESEARCH_PLACEMENTS), "in research.html")


if __name__ == "__main__":
    main()
