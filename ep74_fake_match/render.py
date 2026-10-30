"""NOT JUST YOU – No. 74: the fake match score (OkCupid 2014). Look C+D, dark."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from dating import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .6, "study": .7, "result": .5, "quote": .6, "backlash": .5, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "quote", "backlash", "point", "end"]
EP = ThreadEpisode(TL, 74, "FAKE MATCH", order=ORDER, dark=True, label="EXPERIMENT · OKCUPID",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Rudder (2014), We Experiment On Human Beings,", "OkCupid blog"),
                   music=dict(bpm=100, root=-1, prog="tense", kick="four", gaps=[(E("study") + .05, S("result") + .05)]),
                   cover=dict(words=["90 %", "MATCH?"], kicker="It was a lie."))

def pair(img, d, y=900, s=.55, c1=INK, c2=SIG):
    silhouette(img, lambda m: bust(m, 250, y, s, 255, f=1), (40, y - 160, 470, y + 250), c1, cell=8)
    silhouette(img, lambda m: bust(m, 710, y, s, 255, f=-1), (490, y - 160, 920, y + 250), c2, cell=8)

def sc_hook(img, d, t):
    tl = cue("hook", "a lie") - .15
    pair(img, d, 880)
    big = "30 %" if tl <= t < tl + .35 else "90 %"
    d.text((X0 - 6, 320), big, font=F(BLK, 260), fill=SIG)
    d.text((X0 + 6, 590), "MATCH", font=F(BLK, 80), fill=INK)
    if t >= tl:
        if t < tl + .35: glitch(img, (X0, 300, X1, 600), 1.0, seed=int(t * 30))
        box_label(d, X1, 600, "OR 30 %?", 44, WHITE, INK, font=BLK, anchor="ra")
    fig(d, "fig. 1 — the number on your screen")

def sc_study(img, d, t):
    t0, tt = S("study"), cue("study", "told them") - .2
    d.text((X0, 320), "ACTUAL", font=F(COND, 44), fill=MID)
    counter(d, X0, 370, t, t0 + .3, .6, 30, "{:.0f} %", 170, INK)
    hbar(d, 580, .3, (t - t0 - .3) / .6, INK, h=60)
    if t >= tt:
        d.text((X0, 700), "SHOWN", font=F(COND, 44), fill=SIG)
        counter(d, X0, 750, t, tt, .6, 90, "{:.0f} %", 170, SIG)
        hbar(d, 960, .9, (t - tt) / .6, SIG, h=60)
    fig(d, "bad matches, told they were great")

def sc_result(img, d, t):
    t0, ta = S("result"), cue("result", "acted like") - .2
    d.text((X0, 320), "MORE", font=F(BLK, 170), fill=INK); d.text((X0, 490), "MESSAGES.", font=F(BLK, 130), fill=SIG)
    bubbles(d, X0 + 10, X1 - 30, 680, 5, k=(t - t0 - .3) / 1.4)
    if t >= ta: box_label(d, X0, 1060, "ACTED LIKE A GOOD MATCH", 40, WHITE, SIG, font=BLK)
    fig(d, "first messages + replies")

def sc_quote(img, d, t):
    t0 = S("quote"); tm = cue("quote", "the myth") - .2
    d.text((X0, 320), "“", font=F(BLK, 220), fill=SIG)
    words_in(d, t, [("THE MYTH OF", tm, 470, 100, INK), ("COMPATIBILITY", tm + .25, 580, 100, INK),
                    ("WORKS JUST AS WELL", cue("quote", "works") - .1, 720, 76, MID), ("AS THE TRUTH.", cue("quote", "truth") - .3, 810, 110, SIG)])
    fig(d, "OkCupid about its own experiment, 2014")

def sc_backlash(img, d, t):
    t0, tf = S("backlash"), cue("backlash", "furious") - .25
    d.text((X0, 320), "2014:", font=F(BLK, 150), fill=INK)
    for i in range(5):
        x = X0 + 80 + i * 170; k = ease((t - tf - i * .07) / .25)
        silhouette(img, lambda m, x=x: front_bust(m, x, 820, .26, 255), (x - 85, 700, x + 85, 960), SIG if k > 0 else MID, cell=6)
    if t >= tf:
        d.text((X0, 500), "USERS WERE FURIOUS.", font=F(BLK, 84), fill=SIG)
        if t < tf + .3: glitch(img, (X0, 480, X1, 980), .8, seed=int(t * 30))
    fig(d, "\"we experiment on human beings\"")

def sc_point(img, d, t):
    t0, te = S("point"), cue("point", "expect") - .3
    words_in(d, t, [("CHEMISTRY", t0 + .2, 320, 150, INK), ("IS PARTLY", t0 + .5, 480, 120, MID), ("EXPECTATION.", te, 620, 118, SIG)])
    pair(img, d, 930, .42, MID, SIG)
    fig(d, "fig. 2 — told to click, they clicked")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "quote": sc_quote, "backlash": sc_backlash, "point": sc_point}
FX = [(0.0, thud(.5), 0), (cue("hook", "a lie") - .15, rewind_sfx(.12, .3), 0), *EP.cut_fx(), (S("study") + .3, pop(.15), -.3), (cue("study", "told them") - .2, thud(.45), .3),
      (S("result") + .05, thud(.5), 0), *[(S("result") + .4 + i * .28, pop(.1), (i % 2 - .5)) for i in range(5)], (cue("result", "acted like") - .2, pop(.15), 0),
      (cue("quote", "truth") - .3, thud(.45), 0), (cue("backlash", "furious") - .25, rewind_sfx(.14, .35), 0), (cue("point", "expect") - .3, thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
