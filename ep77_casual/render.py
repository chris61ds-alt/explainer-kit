"""NOT JUST YOU · AFTER DARK – No. 77: who ticks 'casual sex' (Rudder 2014, Dataclysm). Look C+D, dark."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from dating import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .6, "study": .7, "men": .5, "others": .5, "women": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "men", "others", "women", "point", "end"]
EP = ThreadEpisode(TL, 77, "JUST SEX?", order=ORDER, dark=True, series="NOT JUST YOU · AFTER DARK", label="PLATFORM DATA · SELF-REPORTED",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Rudder (2014), Dataclysm,", "OkCupid data"),
                   music=dict(bpm=96, root=-2, prog="tense", kick="four", gaps=[(E("study") + .05, S("men") + .05)]),
                   cover=dict(words=["JUST FOR", "SEX?"], kicker="Who actually ticks the box."))

def tick_box(d, x, y, on, size=56, col=SIG):
    d.rectangle([x, y, x + size, y + size], outline=INK, width=5, fill=col if on else None)
    if on: d.line([(x + 12, y + size * .52), (x + size * .42, y + size - 14), (x + size - 10, y + 12)], fill=WHITE, width=7)

def grid_people(img, d, n, hi, k, cols, x0, y0, step, s, cell):
    for i in range(int(n * clamp(k))):
        r, c = divmod(i, cols); x = x0 + c * step; y = y0 + r * step * 1.25
        d.ellipse([x - s, y - s, x + s, y + s], fill=SIG if i in hi else MID)

def sc_hook(img, d, t):
    d.text((X0 - 6, 320), "JUST FOR", font=F(BLK, 150), fill=INK); d.text((X0 - 6, 470), "SEX?", font=F(BLK, 230), fill=SIG)
    for i, x in enumerate((230, 480, 730)): phone(d, x, 960, 1.2, INK, lit=i == 1)
    fig(d, "fig. 1 — the honest checkbox")

def sc_study(img, d, t):
    t0, tc = S("study"), cue("study", "casual sex") - .3
    d.text((X0, 320), "LOOKING FOR:", font=F(BLK, 100), fill=INK)
    opts = ["new friends", "long-term dating", "short-term dating", "casual sex"]
    for i, o in enumerate(opts):
        y = 500 + i * 120; last = i == 3
        tick_box(d, X0, y, last and t >= tc)
        d.text((X0 + 90, y + 28), o, font=F(BLK if last else COND, 54), fill=SIG if last and t >= tc else INK, anchor="lm")
    fig(d, "OkCupid profile options")

def sc_men(img, d, t):
    t0 = S("men")
    counter(d, X0, 320, t, t0 + .1, .7, 6.1, "{:.1f} %", 250, SIG)
    d.text((X0 + 6, 590), "of straight men", font=F(COND, 44), fill=INK)
    grid_people(img, d, 16, {5}, (t - t0 - .3) / .8, 8, X0 + 50, 760, 105, 34, 6)
    fig(d, "about 1 in 16")

def sc_others(img, d, t):
    t0 = S("others")
    for j, (lab, v) in enumerate((("GAY MEN", 6.9), ("LESBIANS", 6.9))):
        k = ease((t - t0 - .2 - j * .3) / .5); y = 330 + j * 280
        d.text((X0, y), lab, font=F(BLK, 80), fill=INK)
        d.rectangle([X0, y + 110, X0 + 720 * v / 8 * k, y + 190], fill=SIG if j else INK)
        if k > .9: d.text((X0 + 720 * v / 8 * k + 16, y + 150), f"{v} %", font=F(BLK, 54), fill=SIG if j else INK, anchor="lm")
    fig(d, "explicitly seeking casual sex")

def sc_women(img, d, t):
    t0 = S("women")
    counter(d, X0, 320, t, t0 + .1, .7, .8, "{:.1f} %", 250, SIG)
    d.text((X0 + 6, 590), "of straight women", font=F(COND, 44), fill=INK)
    grid_people(img, d, 125, {62}, (t - t0 - .3) / 1.0, 25, X0 + 14, 700, 34, 11, 4)
    fig(d, "about 1 in 125")

def sc_point(img, d, t):
    t0, tw, tt = S("point"), cue("point", "hundred") - .4, cue("point", "at least") - .2
    words_in(d, t, [("1 IN 16 MEN.", t0 + .1, 320, 130, INK)] + ([("1 IN 125 WOMEN.", tw, 470, 110, SIG)] if t >= tw else []))
    if t >= tt:
        box_label(d, X0, 680, "AT LEAST,", 46, WHITE, INK, font=BLK)
        box_label(d, X0, 760, "THAT'S WHAT THEY TICKED.", 46, WHITE, SIG, font=BLK)
    silhouette(img, lambda m: bust(m, 760, 960, .38, 255, f=-1), (600, 860, 920, 1130), MID, cell=7)
    fig(d, "fig. 2 — saying is not the same as wanting")

EP.scenes = {"hook": sc_hook, "study": sc_study, "men": sc_men, "others": sc_others, "women": sc_women, "point": sc_point}
FX = [(0.0, thud(.5), 0), (.4, pop(.15), 0), *EP.cut_fx(), *[(S("study") + .2 + i * .25, tick(.035), 0) for i in range(3)], (cue("study", "casual sex") - .3, thud(.45), 0),
      (S("men") + .05, thud(.55), 0), (S("others") + .2, pop(.15), -.3), (S("others") + .5, pop(.15), .3), (S("women") + .05, thud(.55), 0),
      (S("women") + .3, riser(1.0, .04), 0), (cue("point", "hundred") - .4, thud(.4), 0), (cue("point", "at least") - .2, pop(.15), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
