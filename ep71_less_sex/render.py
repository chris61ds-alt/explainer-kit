"""NOT JUST YOU · AFTER DARK – No. 71: less sex than the 90s (Twenge, Sherman & Wells 2017). Look C+D, dark."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from thread import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .8, "result": .5, "couples": .6, "why": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "couples", "why", "point", "end"]
EP = ThreadEpisode(TL, 71, "THE SEX RECESSION", order=ORDER, dark=True, series="NOT JUST YOU · AFTER DARK",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Twenge, Sherman & Wells (2017),", "Archives of Sexual Behavior 46(8)"),
                   music=dict(bpm=90, root=-1, prog="minor", kick="half", gaps=[(E("study") + .05, S("result") + .05)]),
                   cover=dict(words=["WILDER THAN", "THE 90s?"], kicker="We're having less sex."))

def calendar(d, x, y, n_on, k, cols=13, cell=58, total=52, col=SIG):
    for i in range(total):
        r, c = divmod(i, cols); xx = x + c * (cell + 8); yy = y + r * (cell + 8)
        on = i < n_on * k
        d.rectangle([xx, yy, xx + cell, yy + cell], fill=col if on else None, outline=col if on else MID, width=2)

def sc_hook(img, d, t):
    d.text((X0 - 6, 320), "WILDER THAN", font=F(BLK, 130), fill=INK); d.text((X0 - 6, 460), "THE 90s?", font=F(BLK, 200), fill=SIG)
    silhouette(img, lambda m: body(m, 330, 1120, 340, 255), (160, 760, 500, 1125), MID, cell=8)
    silhouette(img, lambda m: body(m, 640, 1120, 350, 255), (460, 750, 820, 1125), INK, cell=8)
    box_label(d, 330, 715, "1995", 30, WHITE, MID, font=BLK, anchor="ma"); box_label(d, 640, 705, "2014", 30, WHITE, SIG, font=BLK, anchor="ma")
    fig(d, "fig. 1 — then vs now")

def sc_study(img, d, t):
    t0 = S("study")
    counter(d, X0, 320, t, t0 + .1, 1.0, 26000, "{:,.0f}+", 200, SIG)
    d.text((X0 + 6, 540), "Americans · asked since 1989", font=F(COND, 40), fill=INK)
    ruler(d, 760, X0, X1, ["1989", "1999", "2009", "2014"], minor=40)
    k = clamp((t - t0 - .5) / 2.0); d.line([X0, 700, X0 + (X1 - X0) * k, 700], fill=SIG, width=6)
    fig(d, "General Social Survey")

def sc_result(img, d, t):
    t0 = S("result")
    counter(d, X0, 320, t, t0 + .1, .7, 9, "− {:.0f}", 260, SIG)
    d.text((X0 + 6, 600), "times a year · early 2010s vs late 90s", font=F(COND, 40), fill=INK)
    calendar(d, X0, 700, 9, clamp((t - t0 - .3) / 1.0), total=9 * 2, cols=9, cell=74)
    fig(d, "average US adult · schematic squares = times")

def sc_couples(img, d, t):
    t0 = S("couples")
    d.text((X0, 320), "MARRIED:", font=F(BLK, 150), fill=INK)
    counter(d, X0, 470, t, t0 + .3, .7, 16, "− {:.0f}", 220, SIG)
    silhouette(img, lambda m: bust(m, 360, 900, .5, 255, f=1), (140, 800, 600, 1130), INK, cell=8)
    silhouette(img, lambda m: bust(m, 720, 910, .5, 255, f=-1), (500, 800, 940, 1130), MID, cell=8)
    fig(d, "per year, 2010–14 vs early 2000s")

def sc_why(img, d, t):
    t0 = S("why")
    d.text((X0, 320), "WHY?", font=F(BLK, 200), fill=INK)
    d.text((X0, 560), "fewer steady partners", font=F(BLK, 80), fill=SIG)
    for i in range(6):
        x = X0 + 60 + i * 140; paired = i < 2
        silhouette(img, lambda m, x=x: body(m, x, 1120, 300, 255), (x - 80, 800, x + 80, 1125), SIG if paired else MID, cell=7)
    d.text((X1, 1146), "among younger adults · one explanation", font=F(MED, 22), fill=MID, anchor="ra")

def sc_point(img, d, t):
    t0, tb = S("point"), cue("point", "but we're") - .2
    words_in(d, t, [("TALK MORE.", t0 + .3, 320, 180, INK)] + ([("DO LESS.", tb, 520, 200, SIG)] if t >= tb else []))
    fig(d, "fig. 2 — the sex recession")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "couples": sc_couples, "why": sc_why, "point": sc_point}
FX = [(0.0, thud(.5), 0), (.3, whoosh(.6, .06), 0), *EP.cut_fx(), (S("study") + .5, riser(2.0, .04), 0), (S("result") + .05, thud(.55), 0),
      *[(S("result") + .3 + i * .1, tick(.035), (i % 5 - 2) / 3) for i in range(9)], (S("couples") + .3, thud(.45), 0),
      (S("why") + .2, pop(.15), 0), (cue("point", "but we're") - .2, thud(.5), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
