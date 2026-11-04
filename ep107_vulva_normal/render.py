"""NOT JUST YOU – No. 107 (Bodies: all normal 1/2): there's no 'normal' vulva – 657 women measured, inner labia 5–100 mm,
outer 12–180 mm (Kreklau et al. 2018, BJOG). Look C+D · claim opener · no anatomical drawings."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
HERE = os.path.dirname(os.path.abspath(__file__))
from bodies import *
TL = Timeline(HERE, lead=.15, gaps={"study": .6, "range": .5, "normal": .6, "inside": .5, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["study", "range", "normal", "inside", "point", "end"]
EP = ThreadEpisode(TL, 107, "ALL NORMAL", order=ORDER, dark=True, label="MEASURED · 657 WOMEN",
                   chapters={k: "" for k in ORDER[:-1]}, sources=("Kreklau et al. (2018), BJOG 125(13) ·", "Lloyd et al. (2005), BJOG 112(5)"),
                   music=dict(bpm=100, root=2, prog="major", kick="four", audio="v5", gaps=[(E("study") + .05, S("range") + .05)]),
                   cover=dict(words=["THERE'S NO", "\"NORMAL\"", "VULVA."], kicker="Bodies: all normal, part 1."))

def sc_study(img, d, t):
    t0, ta = S("study"), cue("study", "aged fifteen") - .1
    counter(d, X0, 320, t, t0 + .1, .8, 657, "{:.0f}", 230, INK); d.text((X0 + 6, 565), "women, measured by gynecologists", font=F(COND, 46), fill=INK)
    if t >= ta: box_label(d, X0 + 4, 640, "AGED 15 TO 84", 44, WHITE, INK, font=BLK)
    dot_field(d, (X0 + 14, 760, X1, 1110), t, cell=30, col=MID, hit={45})
    fig(d, "Lucerne, Switzerland")

def sc_range(img, d, t):
    t0, tf, to = S("range"), cue("range", "five millimeters") - .1, cue("range", "The outer ones") - .1
    d.text((X0, 320), "INNER LABIA", font=F(BLK, 100), fill=INK)
    ruler(d, X0, X1, 560, 0, 100, 5, 100, (t - tf) / .9, ticks=10, label_every=2)
    if t >= tf + .9: box_label(d, X1, 600, "20 ×", 60, WHITE, SIG, font=BLK, anchor="ra")
    if t >= to:
        d.text((X0, 720), "OUTER LABIA", font=F(BLK, 100), fill=INK)
        ruler(d, X0, X1, 960, 0, 180, 12, 180, (t - to) / .9, ticks=9, label_every=1)
    fig(d, "range across 657 women")

def sc_normal(img, d, t):
    t0 = S("normal"); words_in(d, t, [("ALL OF IT.", t0 + .05, 320, 170, INK)])
    blob_field(d, (X0, 560, X1, 1110), t, t0 + .1, n=45, col=INK, hi=set(range(45)), hicol=SIG)
    fig(d, "every shape different · schematic")

def sc_inside(img, d, t):
    t0, tv = S("inside"), cue("inside", "The vagina") - .1
    d.text((X0, 320), "BY THE WAY:", font=F(BLK, 110), fill=MID)
    words_in(d, t, [("VULVA", t0 + .3, 470, 170, INK)])
    if t >= t0 + .5: d.text((X0 + 6, 650), "= what you see, outside", font=F(COND, 54), fill=INK)
    if t >= tv:
        words_in(d, t, [("VAGINA", tv, 760, 170, INK)])
        d.text((X0 + 6, 940), "= inside", font=F(COND, 54), fill=INK)
    fig(d, "anatomy, words only")

def sc_point(img, d, t):
    t0, tn = S("point"), cue("point", "that's the normal") - .2
    words_in(d, t, [("LOOKS", t0 + .05, 320, 150, MID), ("DIFFERENT?", t0 + .2, 470, 150, MID)] + ([("THAT'S THE", tn, 650, 120, SIG), ("NORMAL PART.", tn + .15, 770, 120, SIG)] if t >= tn else []))
    fig(d, "fig. — Bodies: all normal")

EP.cuts = {"normal": "stay"}
EP.scenes = {"study": sc_study, "range": sc_range, "normal": sc_normal, "inside": sc_inside, "point": sc_point}
FX = [(0.0, thud(.5), 0), *EP.cut_fx(), (S("study") + .1, riser(.8, .04), 0), (cue("study", "aged fifteen") - .1, pop(.13), .2),
      (cue("range", "five millimeters") - .1, whoosh(.8, .04), 0), (cue("range", "five millimeters") + .8, thud(.45), .3), (cue("range", "The outer ones") - .1, whoosh(.8, .04), 0),
      (S("normal") + .05, thud(.55), 0), *[(S("normal") + .1 + i * .045, tick(.025), (i % 5 - 2) / 3) for i in range(0, 45, 3)],
      (S("inside") + .3, pop(.13), -.2), (cue("inside", "The vagina") - .1, pop(.13), .2),
      (S("point") + .1, pop(.12), 0), (cue("point", "that's the normal") - .2, thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
