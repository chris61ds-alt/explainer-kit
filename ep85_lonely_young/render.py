"""NOT JUST YOU – No. 85: the young are the loneliest (Gallup & Meta 2023, 142 countries). Look C+D, dark."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from thread import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .6, "study": .6, "world": .6, "young": .5, "old": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "world", "young", "old", "point", "end"]
EP = ThreadEpisode(TL, 85, "LONELIEST", order=ORDER, dark=True, label="SURVEY · 142 COUNTRIES",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Gallup & Meta (2023), Global State of", "Social Connections · news.gallup.com"),
                   music=dict(bpm=88, root=-3, prog="minor", kick="half", gaps=[(E("world") + .05, S("young") + .05)]),
                   cover=dict(words=["LONELIEST?", "THE YOUNG."], kicker="Not your grandparents."))

def sc_hook(img, d, t):
    tn = cue("hook", "not your") - .3
    d.text((X0 - 6, 320), "LONELIEST?", font=F(BLK, 170), fill=INK)
    silhouette(img, lambda m: body(m, 300, 1120, 420, 255), (150, 670, 450, 1125), MID, cell=7)
    silhouette(img, lambda m: body(m, 640, 1120, 450, 255), (480, 640, 800, 1125), INK, cell=7)
    box_label(d, 300, 650, "70", 34, WHITE, MID, font=BLK, anchor="ma"); box_label(d, 640, 620, "22", 34, WHITE, INK, font=BLK, anchor="ma")
    if t >= tn:
        d.text((X0 + 4, 505), "Not your grandparents.", font=F(BLK, 56), fill=SIG)
        bbox(d, (510, 640, 770, 1120), None, SIG, (t - tn) / .3, coords=True)
    fig(d, "fig. 1 — who feels it most?")

def sc_study(img, d, t):
    t0 = S("study")
    counter(d, X0, 320, t, t0 + .1, .9, 142, "{:.0f}", 240, SIG)
    d.text((X0 + 6, 580), "countries · about 1,000 people each", font=F(COND, 40), fill=INK)
    dot_field(d, (X0 + 14, 680, X1, 1110), t, cell=30, col=MID, hit={7, 41, 88, 130, 177, 222, 260})
    fig(d, "2022–23 · China not included")

def sc_world(img, d, t):
    t0, tb = S("world"), cue("world", "billion") - .3
    d.text((X0, 320), "1 IN 4", font=F(BLK, 230), fill=SIG)
    d.text((X0 + 6, 570), "adults: very or fairly lonely", font=F(COND, 42), fill=INK)
    for i in range(4):
        x = X0 + 100 + i * 210
        silhouette(img, lambda m, x=x: front_bust(m, x, 760, .3, 255), (x - 100, 660, x + 100, 920), SIG if i == 2 else MID, cell=6)
    if t >= tb: box_label(d, X0, 990, "1 BILLION+ PEOPLE", 60, WHITE, INK, font=BLK)
    fig(d, "24 % worldwide")

def bars(d, t, show_old):
    for j, (lab, v, col, tk) in enumerate((("AGES 19–29", 27, SIG, S("young") + .3), ("65 AND OLDER", 17, MID, S("old") + .3))):
        if j == 1 and not show_old: continue
        k = ease((t - tk) / .6); y = 600 + j * 220
        d.text((X0, y), lab, font=F(BLK, 50), fill=col)
        d.rectangle([X0, y + 70, X0 + 760 * v / 30 * k, y + 170], fill=col)
        if k > .9: d.text((X0 + 760 * v / 30 * k + 16, y + 120), f"{v} %", font=F(BLK, 64), fill=col, anchor="lm")

def sc_young(img, d, t):
    d.text((X0, 320), "LONELIEST:", font=F(BLK, 150), fill=INK)
    bars(d, t, False)
    fig(d, "very or fairly lonely, by age")

def sc_old(img, d, t):
    d.text((X0, 320), "LEAST:", font=F(BLK, 150), fill=INK)
    bars(d, t, True)
    fig(d, "very or fairly lonely, by age")

def sc_point(img, d, t):
    t0, tb = S("point"), cue("point", "biggest") - .3
    words_in(d, t, [("NOT THE", t0 + .2, 320, 140, MID), ("EXCEPTION.", t0 + .5, 470, 130, INK)] + ([("THE BIGGEST", tb - .2, 650, 120, INK), ("GROUP.", tb + .1, 780, 170, SIG)] if t >= tb - .2 else []))
    fig(d, "fig. 2 — call someone today")

EP.scenes = {"hook": sc_hook, "study": sc_study, "world": sc_world, "young": sc_young, "old": sc_old, "point": sc_point}
FX = [(0.0, thud(.5), 0), (cue("hook", "not your") - .3, pop(.15), 0), *EP.cut_fx(), (S("study") + .1, riser(.9, .04), 0),
      (S("world") + .05, thud(.5), 0), (cue("world", "billion") - .3, pop(.15), 0), (S("young") + .3, thud(.5), 0), (S("old") + .3, pop(.15), 0),
      (cue("point", "biggest") - .3, thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
