"""NOT JUST YOU · AFTER DARK – No. 83: the OnlyFans math (OnlyFans Aug 2026; Ball estimate). Look C+D, dark."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from dating import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .6, "big": .6, "split": .6, "avg": .6, "skew": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "big", "split", "avg", "skew", "point", "end"]
EP = ThreadEpisode(TL, 83, "THE ONLYFANS MATH", order=ORDER, dark=True, series="NOT JUST YOU · AFTER DARK", label="PLATFORM DATA · ONLYFANS",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("OnlyFans figures via Tubefilter (Aug 2026) ·", "Matthew Ball, OnlyFans economics (estimate)"),
                   music=dict(bpm=98, root=-1, prog="tense", kick="four", gaps=[(E("split") + .05, S("avg") + .05)]),
                   cover=dict(words=["EVERYONE", "RICH?"], kicker="The OnlyFans math."))

def sc_hook(img, d, t):
    t0, tr = S("hook"), cue("hook", "rich") - .3
    d.text((X0 - 6, 300), "$6.3 B", font=F(BLK, 250), fill=SIG)
    d.text((X0 + 6, 560), "paid to creators in one year", font=F(COND, 42), fill=INK)
    for i, x in enumerate((230, 480, 730)): phone(d, x, 900, 1.3, INK, lit=i == 1)
    if t >= tr:
        box_label(d, X0, 1040, "EVERYONE RICH?", 60, WHITE, SIG, font=BLK)
        if t < tr + .3: glitch(img, (X0, 280, X1, 620), 1.0, seed=int(t * 30))
    fig(d, "fiscal 2025")

def sc_big(img, d, t):
    t0, tm = S("big"), cue("big", "five thousand") - .3
    counter(d, X0, 320, t, t0 + .1, .8, 30, "${:.0f} B", 200, INK)
    d.text((X0 + 6, 540), "paid out since 2016", font=F(COND, 42), fill=INK)
    if t >= tm:
        counter(d, X0, 640, t, tm, .8, 5076, "{:,.0f}", 170, SIG)
        d.text((X0 + 6, 830), "creators made $1 million+", font=F(COND, 42), fill=INK)
        for i in range(3):
            x = 560 + i * 120
            silhouette(img, lambda m, x=x: front_bust(m, x, 960, .2, 255), (x - 60, 910, x + 60, 1060), SIG, cell=5)
    fig(d, "OnlyFans, August 2026")

def sc_split(img, d, t):
    t0 = S("split")
    counter(d, X0, 320, t, t0 + .3, .9, 2.5, "{:.1f} M", 230, INK)
    d.text((X0 + 6, 570), "active creators", font=F(COND, 42), fill=INK)
    dot_field(d, (X0 + 14, 660, X1, 1110), t, cell=26, col=MID, hit={44, 190, 333})
    fig(d, "per regulatory filings")

def sc_avg(img, d, t):
    t0, tm = S("avg"), cue("avg", "two hundred") - .3
    d.text((X0, 320), "EVEN SPLIT:", font=F(BLK, 110), fill=INK)
    counter(d, X0, 450, t, t0 + .5, .8, 2520, "${:,.0f}", 180, SIG)
    d.text((X0 + 6, 650), "per creator, per year", font=F(COND, 42), fill=INK)
    if t >= tm:
        box_label(d, X0, 760, "ABOUT $210 A MONTH", 60, WHITE, INK, font=BLK)
        banknote(d, 560, 960, 1.0, "100", SIG); banknote(d, 760, 960, 1.0, "100")
    fig(d, "our calculation: $6.3 B / 2.5 M")

def sc_skew(img, d, t):
    t0, te = S("skew"), cue("skew", "top ten") - .3
    d.text((X0, 320), "NOT EVEN.", font=F(BLK, 160), fill=INK)
    if t >= te:
        k = ease((t - te) / .8)
        d.rectangle([X0, 560, X0 + 840 * .73 * k, 680], fill=SIG); d.rectangle([X0 + 840 * .73 * k, 560, X0 + 840 * k, 680], fill=MID)
        if k > .95:
            d.text((X0 + 14, 620), "TOP 10 %", font=F(BLK, 44), fill=WHITE, anchor="lm")
            d.text((X0, 700), "about 3/4 of the money", font=F(BLK, 40), fill=SIG)
            d.text((X1, 700), "the other 90 %", font=F(COND, 32), fill=MID, anchor="ra")
        for i in range(10):
            x = X0 + 42 + i * 84
            silhouette(img, lambda m, x=x: front_bust(m, x, 880, .15, 255), (x - 42, 830, x + 42, 970), SIG if i == 0 else MID, cell=5)
    fig(d, "analyst estimate · Matthew Ball")

def sc_point(img, d, t):
    t0, tc = S("point"), cue("point", "concentrated") - .4
    words_in(d, t, [("THE MONEY", t0 + .1, 320, 140, INK), ("IS REAL.", t0 + .4, 470, 140, INK)] + ([("IT'S JUST", tc - .3, 650, 120, MID), ("CONCENTRATED.", tc, 780, 108, SIG)] if t >= tc - .3 else []))
    fig(d, "fig. 2 — a few win big")

EP.scenes = {"hook": sc_hook, "big": sc_big, "split": sc_split, "avg": sc_avg, "skew": sc_skew, "point": sc_point}
FX = [(0.0, thud(.55), 0), (cue("hook", "rich") - .3, rewind_sfx(.12, .3), 0), *EP.cut_fx(), (S("big") + .1, riser(.8, .04), 0), (cue("big", "five thousand") - .3, thud(.45), 0),
      *[(S("split") + .3 + i * .1, tick(.03), (i % 5 - 2) / 3) for i in range(9)], (S("avg") + .5, thud(.5), 0), (cue("avg", "two hundred") - .3, pop(.15), 0),
      (cue("skew", "top ten") - .3, thud(.5), 0), (cue("point", "concentrated") - .4, thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
