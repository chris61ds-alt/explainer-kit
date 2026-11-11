"""NOT JUST YOU – No. 124 (simulation): 'hot people are mean' – Berkson's paradox. 400 simulated people, looks and kindness
independent (r ≈ 0); keep only looks + kindness above a bar → r ≈ −0.54 among the rest (Berkson 1946, Ellenberg 2014).
Look C+D · statement opener with "you" · live scatter simulation with a running correlation counter · orange reveal."""
import os, sys, math, random, statistics as st
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"setup": .6, "filter": .5, "reveal": .6, "why": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["setup", "filter", "reveal", "why", "point", "end"]
EP = ThreadEpisode(TL, 124, "BERKSON", order=ORDER, dark=True, label="SIMULATION · MATH MODEL",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Berkson (1946), Biometrics Bulletin 2(3) ·", "Ellenberg (2014), How Not to Be Wrong"),
                   music=dict(bpm=100, root=1, prog="tense", kick="four", audio="v5", gaps=[(E("setup") + .05, S("filter") + .05)]),
                   cover=dict(words=["YOU THINK", "HOT PEOPLE", "ARE MEAN."], kicker="It's a statistics trick."))

R = random.Random(4); PEOPLE = [(R.random(), R.random()) for _ in range(400)]
KEEP = [p[0] + p[1] > 1.0 for p in PEOPLE]
PX0, PX1, PY0, PY1 = X0 + 70, X1 - 10, 560, 1060           # plot box: x = looks, y = kindness (up = kinder)
def pxy(p): return PX0 + p[0] * (PX1 - PX0), PY1 - p[1] * (PY1 - PY0)
def corr(ps):
    if len(ps) < 3: return 0.0
    return st.correlation([p[0] for p in ps], [p[1] for p in ps])

def axes(d):
    d.line([PX0, PY1, PX1, PY1], fill=INK, width=4); d.line([PX0, PY0, PX0, PY1], fill=INK, width=4)
    d.text((PX1, PY1 + 14), "LOOKS →", font=F(MONO, 26), fill=MID, anchor="ra")
    d.text((PX0 - 16, PY0), "KIND", font=F(MONO, 26), fill=MID, anchor="ra")

def scatter(d, t, n_vis, fade=0.0, line=False, rcol=INK):
    vis = PEOPLE[:n_vis]
    for i, p in enumerate(vis):
        x, y = pxy(p); out = not KEEP[i]
        if out and fade >= 1: continue
        col = MID if out and fade > 0 else INK
        r = 7 if not (out and fade > 0) else 7 * (1 - fade) + 2
        d.ellipse([x - r, y - r, x + r, y + r], fill=col)
    if line:                                                # least-squares trend line through the kept people
        ks = [p for p, k in zip(PEOPLE, KEEP) if k]; mx = st.mean(p[0] for p in ks); my = st.mean(p[1] for p in ks)
        b = sum((p[0] - mx) * (p[1] - my) for p in ks) / sum((p[0] - mx) ** 2 for p in ks); a = my - b * mx
        x0, x1 = .05, 1.0; d.line([pxy((x0, a + b * x0)), pxy((x1, a + b * x1))], fill=rcol, width=10)
    shown = [p for i, p in enumerate(vis) if fade < 1 or KEEP[i]]
    return corr(shown)

def link_box(d, r, col=INK, y=440):
    d.text((X0, y), "LINK:", font=F(BLK, 64), fill=col); d.text((X0 + 220, y), f"{r:+.2f}", font=F(BLK, 64), fill=col)

def sc_setup(img, d, t):
    t0, tn = S("setup"), cue("setup", "Four hundred") - .1
    d.text((X0, 320), "400 PEOPLE", font=F(BLK, 110), fill=INK)
    axes(d); n = int(clamp((t - tn) / 2.2) * 400) if t >= tn else 0
    r = scatter(d, t, n)
    if n > 20: link_box(d, r)
    fig(d, "random: looks and kindness independent")

def sc_filter(img, d, t):
    t0, tw = S("filter"), cue("filter", "Watch what") - .2
    d.text((X0, 320), "YOUR LIST", font=F(BLK, 110), fill=INK)
    axes(d); k = ease(clamp((t - t0 - .3) / .8))
    a, b = pxy((0, 1)), pxy((1, 0))                          # the bar: looks + kindness = 1
    d.line([a, (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k)], fill=MID, width=6)
    fade = clamp((t - t0 - 1.2) / 1.0)
    scatter(d, t, 400, fade=fade)
    if fade > .5: box_label(d, PX0 + 10, PY1 - 70, "NOT DATED", 34, WHITE, MID, font=BLK)
    fig(d, "attractive enough, kind enough, or both")

def sc_reveal(img, d, t):
    t0 = S("reveal")
    d.text((X0, 320), "HOTTER = MEANER?", font=F(BLK, 96), fill=SIG)
    axes(d); k = clamp((t - t0 - .2) / .8)
    r = scatter(d, t, 400, fade=1, line=k > 0, rcol=SIG)
    link_box(d, r * ease(k) + 0 * (1 - k), SIG)
    fig(d, "among the 209 you date · simulation")

def sc_why(img, d, t):
    t0, th = S("why"), cue("why", "So the hot ones") - .1
    axes(d); scatter(d, t, 400, fade=1)
    k = ease(clamp((t - t0 - .3) / .5)); a, b, c = pxy((0, 0)), pxy((0, 1)), pxy((1, 0))
    if k > 0: d.polygon([a, (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k), (a[0] + (c[0] - a[0]) * k, a[1] + (c[1] - a[1]) * k)], outline=INK, width=6)
    d.text((X0, 320), "MEAN + PLAIN:", font=F(BLK, 90), fill=INK); d.text((X0, 420), "NEVER ON YOUR LIST", font=F(BLK, 70), fill=MID)
    if t >= th: p = pxy((.92, .2)); box_label(d, p[0] - 260, p[1] - 140, "HOT, NOT NICE", 34, WHITE, INK, font=BLK)
    fig(d, "simulation")

def sc_point(img, d, t):
    t0, tn = S("point"), cue("point", "It's not that") - .15
    words_in(d, t, [("BERKSON'S", t0 + .05, 320, 140, MID), ("PARADOX.", t0 + .2, 470, 140, MID)])
    if t >= tn: words_in(d, t, [("IT'S WHO YOU", tn, 650, 110, SIG), ("FILTERED OUT.", tn + .4, 770, 110, SIG)])
    fig(d, "fig. 2 — a filter, not a law")

EP.cuts = {"filter": "stay", "reveal": "stay", "why": "stay"}
EP.bg = {"setup": "light", "filter": "light"}
EP.scenes = {"setup": sc_setup, "filter": sc_filter, "reveal": sc_reveal, "why": sc_why, "point": sc_point}
FX = [*EP.cut_fx(), *[(cue("setup", "Four hundred") - .1 + i * .11, tick(.03), (i % 5 - 2) / 3) for i in range(20)],
      (S("filter") + .3, whoosh(.8, .04), 0), (S("filter") + 1.2, riser(1.0, .04), 0),
      (S("reveal") + .05, thud(.55), 0), (S("reveal") + .3, whoosh(.6, .05), .2),
      (S("why") + .3, pop(.13), -.3), (cue("why", "So the hot ones") - .1, pop(.13), .3),
      (S("point") + .1, pop(.12), 0), (cue("point", "It's not that") - .15, thud(.5), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
