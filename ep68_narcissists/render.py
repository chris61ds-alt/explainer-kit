"""NOT JUST YOU – No. 68: narcissists win first impressions, then lose (Back et al. 2010; Paulhus 1998). Look C+D, dark."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from thread import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .8, "result": .5, "why": .5, "flip": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "why", "flip", "point", "end"]
EP = ThreadEpisode(TL, 68, "THE CHARMER", order=ORDER, dark=True,
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Back, Schmukle & Egloff (2010), JPSP 98(1) ·", "Paulhus (1998), JPSP 74(5)"),
                   music=dict(bpm=98, root=-1, prog="tense", kick="four", gaps=[(E("study") + .05, S("result") + .05)]),
                   cover=dict(words=["CHARMING?", "CAREFUL."], kicker="First impressions lie."))

def spotlight_on(img, d, x, h, col, cell=9, glow=True):
    if glow: d.polygon([(x - 50, 300), (x + 50, 300), (x + 200, 1120), (x - 200, 1120)], fill=mix(BG, INK, .06))
    silhouette(img, lambda m: body(m, x, 1120, h, 255, arm=.25), (x - 220, 1120 - h - 20, x + 220, 1125), col, cell=cell)

def sc_hook(img, d, t):
    spotlight_on(img, d, 640, 470, SIG)
    for x in (180, 330): silhouette(img, lambda m, x=x: body(m, x, 1120, 380, 255), (x - 120, 720, x + 120, 1125), MID, cell=8)
    d.text((X0 - 6, 320), "MOST", font=F(BLK, 200), fill=INK); d.text((X0 - 6, 510), "CHARMING?", font=F(BLK, 150), fill=SIG)
    bbox(d, (560, 650, 720, 790), "NARCISSIST?", SIG, (t - .5) / .3, coords=False)
    fig(d, "fig. 1 — the center of the room")

def sc_study(img, d, t):
    t0 = S("study")
    counter(d, X0, 320, t, t0 + .1, .6, 73, "{:.0f}", 230, SIG)
    d.text((X0 + 6, 560), "strangers · short introductions", font=F(COND, 40), fill=INK)
    for i in range(6):
        k = ease((t - t0 - .3 - i * .12) / .3)
        if k > 0: silhouette(img, lambda m, i=i: front_bust(m, X0 + 80 + i * 150, 860, .3, 255), (X0 + i * 150, 760, X0 + 160 + i * 150, 1010), SIG if i == 3 else INK, cell=7, k=k)
    fig(d, "zero acquaintance · Back et al., 2010")

def sc_result(img, d, t):
    t0 = S("result")
    d.text((X0, 320), "MORE NARCISSISTIC", font=F(BLK, 90), fill=INK); d.text((X0, 430), "= MORE LIKED", font=F(BLK, 120), fill=SIG)
    OX, OY, GW, GH = X0 + 40, 1080, X1 - X0 - 60, 400
    d.line([OX, OY, OX + GW, OY], fill=INK, width=4); d.line([OX, OY, OX, OY - GH], fill=INK, width=4)
    d.text((OX + GW, OY + 18), "narcissism", font=F(MONO, 22), fill=MID, anchor="ra"); d.text((OX + 10, OY - GH - 10), "liked at first sight", font=F(COND, 28), fill=INK, anchor="ld")
    import random; rnd = random.Random(4); k = clamp((t - t0 - .2) / 1.4)
    for i in range(int(60 * k)):
        u = rnd.random(); v = clamp(.2 + .6 * u + rnd.uniform(-.18, .18))
        d.ellipse([OX + GW * u - 8, OY - GH * v - 8, OX + GW * u + 8, OY - GH * v + 8], fill=SIG if u > .75 else MID)
    if k >= 1: d.line([OX, OY - GH * .2, OX + GW, OY - GH * .8], fill=SIG, width=5)
    d.text((X1, 1146), "schematic", font=F(MED, 22), fill=MID, anchor="ra")

def sc_why(img, d, t):
    t0 = S("why")
    d.text((X0, 320), "ALL SURFACE.", font=F(BLK, 150), fill=SIG)
    spotlight_on(img, d, 330, 520, INK, glow=False)
    items = [("STYLISH CLOTHES", "stylish"), ("CONFIDENT BODY", "confident"), ("ENTERTAINING TALK", "entertaining")]
    for i, (lab, w) in enumerate(items):
        tk = cue("why", w) - .2; k = ease((t - tk) / .3)
        if k <= 0: continue
        y = 640 + i * 130; d.line([440, y + 30, 540, y + 30], fill=SIG, width=3)
        box_label(d, 550 + (1 - k) * 30, y, lab, 36, WHITE, SIG if i == 1 else INK, font=BLK)
    fig(d, "cues people picked up in seconds")

def sc_flip(img, d, t):
    t0, tf = S("flip"), cue("flip", "flipped") - .3
    d.text((X0, 320), "7 MEETINGS", font=F(BLK, 150), fill=INK)
    OX, OY, GW, GH = X0 + 40, 1060, X1 - X0 - 60, 420
    mid = OY - GH / 2
    d.line([OX, OY, OX, OY - GH], fill=INK, width=4); d.line([OX, mid, OX + GW, mid], fill=MID, width=2)
    for i in range(7): d.text((OX + GW * i / 6, OY + 18), f"{i + 1}", font=F(MONO, 22), fill=MID, anchor="ma")
    d.text((OX + 10, OY - GH - 10), "liked", font=F(COND, 28), fill=INK, anchor="ld"); d.text((OX + 10, OY + 8), "disliked", font=F(COND, 28), fill=INK, anchor="la")
    k = clamp((t - t0 - .3) / max(.5, (tf - t0) + .8)); n = max(2, int(40 * k))
    pts = [(OX + GW * u, mid - GH * .4 * math.cos(u * math.pi)) for u in np.linspace(0, k, n)]
    d.line(pts, fill=SIG, width=8)
    good = [(OX + GW * u, mid - GH * .32) for u in np.linspace(0, k, n)]; d.line(good, fill=INK, width=5)
    if k > .95: d.text((pts[-1][0] - 8, pts[-1][1] + 14), "narcissists", font=F(BLK, 28), fill=SIG, anchor="ra"); d.text((good[-1][0] - 8, good[-1][1] - 12), "well-adjusted", font=F(BLK, 26), fill=INK, anchor="rd")
    d.text((X1, 1146), "Paulhus, 1998 · schematic", font=F(MED, 22), fill=MID, anchor="ra")

def sc_point(img, d, t):
    t0, tg = S("point"), cue("point", "give it") - .2
    words_in(d, t, [("EASY TO FAKE.", t0, 320, 130, INK)] + ([("GIVE IT", tg, 480, 170, SIG), ("7 MEETINGS.", tg + .2, 650, 130, SIG)] if t >= tg else []))
    spotlight_on(img, d, 760, 330, MID, cell=7, glow=False)
    fig(d, "fig. 2 — time reveals")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "why": sc_why, "flip": sc_flip, "point": sc_point}
FX = [(0.0, thud(.5), 0), (.5, pop(.15), .3), *EP.cut_fx(), *[(S("study") + .3 + i * .12, pop(.08), (i - 2.5) / 3) for i in range(6)],
      (S("result") + .05, thud(.55), 0), (S("result") + .2, riser(1.2, .04), 0), *[(cue("why", w) - .2, pop(.15), (i - 1) / 2) for i, w in enumerate(("stylish", "confident", "entertaining"))],
      (S("flip") + .3, whoosh(1.6, .05), 0), (cue("flip", "flipped") - .3, rewind_sfx(.1, .4), 0), (cue("point", "give it") - .2, thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
