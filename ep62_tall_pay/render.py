"""NOT JUST YOU – No. 62: height and income (Judge & Cable 2004). Look C+D, dark."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from thread import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .8, "result": .5, "career": .6, "why": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "career", "why", "point", "end"]
EP = ThreadEpisode(TL, 62, "THE TALL TAX", order=ORDER, dark=True,
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Judge & Cable (2004), Journal of", "Applied Psychology 89(3)"),
                   music=dict(bpm=104, root=0, prog="tense", kick="four", gaps=[(E("study") + .05, S("result") + .05)]),
                   cover=dict(words=["$789", "PER INCH."], kicker="Every year. Height pays."))

def pair(img, d, hs=(520, 600), cols=(INK, SIG), xs=(320, 640), cell=10, y=1120):
    for h, c, x in zip(hs, cols, xs):
        silhouette(img, lambda m, h=h, x=x: body(m, x, y, h, 255), (x - 200, y - h - 20, x + 200, y + 10), c, cell=cell)

def sc_hook(img, d, t):
    d.text((X0 - 6, 320), "$789", font=F(BLK, 230), fill=SIG)
    d.text((X0, 560), "per inch · per year", font=F(COND, 46), fill=INK)
    pair(img, d, (430, 470), xs=(360, 620))
    dim_v(d, 790, 1120 - 470, 1120 - 430, 1, SIG, "+1 IN")
    fig(d, "fig. 1 — above average height")

def sc_study(img, d, t):
    t0 = S("study")
    counter(d, X0, 320, t, t0 + .1, 1.0, 8500, "{:,.0f}", 220, SIG)
    d.text((X0 + 6, 560), "people · from teens to careers · US + UK", font=F(COND, 40), fill=INK)
    for i in range(14):
        k = ease((t - t0 - .3 - i * .06) / .3)
        if k <= 0: continue
        h = 220 + (i * 37) % 120; x = X0 + 30 + i * 60
        silhouette(img, lambda m, h=h, x=x: body(m, x, 1100, h, 255), (x - 40, 1100 - h - 10, x + 40, 1105), SIG if i % 5 == 2 else MID, cell=7, k=k)
    fig(d, "4 long-term datasets + 45 earlier studies")

def sc_result(img, d, t):
    t0 = S("result")
    d.text((X0, 320), "TALLER", font=F(BLK, 170), fill=INK); d.text((X0, 500), "= PAID MORE", font=F(BLK, 120), fill=SIG)
    for i in range(5):
        k = ease((t - t0 - .4 - i * .25) / .3)
        if k <= 0: continue
        h = 280 + i * 45; x = X0 + 70 + i * 180
        silhouette(img, lambda m, h=h, x=x: body(m, x, 1120, h, 255), (x - 70, 1120 - h - 10, x + 70, 1125), SIG if i == 4 else INK, cell=8)
        for j in range(i + 1): d.ellipse([x + 50, 1100 - j * 22 - 14, x + 90, 1100 - j * 22 + 4], fill=SIG, outline=BG, width=2)
    fig(d, "controlling for gender, age and weight · schematic")

def sc_career(img, d, t):
    t0, tc = S("career"), cue("career", "a hundred and sixty") - .3
    d.text((X0, 320), "6'0\" vs 5'5\"", font=F(BLK, 120), fill=INK)
    if t >= tc: counter(d, X0, 470, t, tc, .9, 166000, "${:,.0f}", 170, SIG)
    pair(img, d, (390, 450), cols=(INK, SIG), xs=(280, 520), cell=9)
    k = clamp((t - tc) / 1.4)
    for j in range(int(14 * k)): d.ellipse([760, 1100 - j * 26 - 16, 860, 1100 - j * 26 + 6], fill=SIG if j % 2 else INK, outline=BG, width=3)
    d.text((X1, 1146), "over a 30-year career", font=F(MED, 22), fill=MID, anchor="ra")

def sc_why(img, d, t):
    t0 = S("why")
    d.text((X0, 320), "LOOKS LIKE", font=F(BLK, 130), fill=INK); d.text((X0, 470), "CONFIDENCE", font=F(BLK, 130), fill=SIG)
    silhouette(img, lambda m: body(m, 480, 1120, 470, 255), (280, 630, 680, 1130), INK, cell=10)
    bbox(d, (380, 640, 580, 780), "SEEMS: CONFIDENT", SIG, (t - t0 - .4) / .3, coords=False)
    fig(d, "one explanation: how others treat taller people")

def sc_point(img, d, t):
    t0, tn = S("point"), cue("point", "but now") - .2
    words_in(d, t, [("UNFAIR.", t0, 320, 210, SIG)] + ([("NOW YOU", tn, 540, 140, INK), ("KNOW.", tn + .2, 690, 140, INK)] if t >= tn else []))
    pair(img, d, (300, 340), xs=(640, 820), cell=8)
    fig(d, "fig. 2 — the bias is real")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "career": sc_career, "why": sc_why, "point": sc_point}
def coin_sfx(amp=.04):
    tt = tt_(.3); return amp * (np.sin(2 * np.pi * 2600 * tt) + .6 * np.sin(2 * np.pi * 3900 * tt)) * np.exp(-tt * 18)
FX = [(0.0, thud(.5), 0), *[(.1 + i * .1, coin_sfx(.035), .3) for i in range(8)], *EP.cut_fx(), *[(S("study") + .3 + i * .06, tick(.03), (i % 5 - 2) / 3) for i in range(14)],
      (S("result") + .05, thud(.55), 0), *[(S("result") + .4 + i * .25, coin_sfx(.04), (i - 2) / 3) for i in range(5)],
      (cue("career", "a hundred and sixty") - .3, thud(.45), 0), *[(cue("career", "a hundred and sixty") + i * .1, coin_sfx(.035), .3) for i in range(14)],
      (S("why") + .4, pop(.15), 0), (S("point") + .05, thud(.5), 0), (cue("point", "but now") - .2, pop(.15), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
