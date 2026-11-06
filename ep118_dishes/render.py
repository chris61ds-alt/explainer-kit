"""NOT JUST YOU – No. 118: fighting about the dishes – 62 % rate sharing chores 'very important' for marriage (Pew 2007);
couples who share the tasks themselves call it fair (99 %) far more than couples who only split 50/50 (about half)
(Carlson 2022). Look C+D · statement opener with "you" · isometric plate stack · orange reveal: share the tasks."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"survey": .6, "split": .5, "together": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["survey", "split", "together", "point", "end"]
EP = ThreadEpisode(TL, 118, "DISHES", order=ORDER, dark=True, label="SURVEYS · US COUPLES",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Pew Research Center (2007), Modern Marriage ·", "Carlson (2022), Sex Roles"),
                   music=dict(bpm=100, root=0, prog="major", kick="four", audio="v5", gaps=[(E("survey") + .05, S("split") + .05)]),
                   cover=dict(words=["YOU FIGHT", "ABOUT THE", "DISHES."], kicker="It's not a small thing."))

def sc_survey(img, d, t):
    t0 = S("survey")
    d.text((X0, 320), "A GOOD MARRIAGE", font=F(BLK, 96), fill=INK); d.text((X0 + 4, 430), "\"very important\"", font=F(COND, 50), fill=MID)
    rows = [("FAITHFULNESS", 93, cue("survey", "faithfulness") - .1), ("GOOD SEX", 70, cue("survey", "Good sex") - .1), ("SHARING CHORES", 62, cue("survey", "Sharing chores") - .1)]
    for j, (lab, v, tk) in enumerate(rows):
        if t < tk: continue
        k = ease((t - tk) / .5); y = 540 + j * 190; col = INK if j == 2 else MID
        d.text((X0, y), lab, font=F(BLK, 46), fill=col); w = 640 * v / 93 * k
        d.rectangle([X0, y + 60, X0 + max(8, w), y + 140], fill=col)
        d.text((X0 + max(8, w) + 14, y + 100), f"{v * k:.0f} %", font=F(BLK, 56), fill=col, anchor="lm")
    fig(d, "US adults, 2007")

I = Iso(500, 1020, .8)
def plates(I, d, x, y, n, k=1.0, top=TOP):
    for i in range(int(n * clamp(k))): I.cyl(d, x, y, i * 16, 95, 10, top=top)

def sc_split(img, d, t):
    t0 = S("split")
    words_in(d, t, [("50 / 50", t0 + .05, 320, 170, INK), ("ISN'T ENOUGH.", t0 + .2, 500, 110, INK)])
    I.grid(img); I.shadow(d, -170, 170, 120); I.shadow(d, 170, -170, 120)
    plates(I, d, -170, 170, 6, (t - t0 - .3) / .5); plates(I, d, 170, -170, 6, (t - t0 - .5) / .5)
    for (x, y, lab) in ((-170, 170, "YOURS"), (170, -170, "MINE")):
        if t >= t0 + .9: fx, fy = I.P(x + 100, y + 100, 0); d.text((fx, fy + 12), lab, font=F(MONO, 26), fill=MID, anchor="ma")
    fig(d, "split, but separate · schematic")

def sc_together(img, d, t):
    t0, th = S("together"), cue("together", "only half") - .15
    words_in(d, t, [("SHARE THE", t0 + .05, 320, 150, SIG), ("TASKS.", t0 + .2, 470, 150, SIG)])
    rows = [("SHARED EVERY TASK", 99, SIG, t0 + .5), ("50/50, NOT SHARED", 50, MID, th)]
    d.text((X0, 650), "CALLED IT FAIR:", font=F(BLK, 46), fill=INK)
    for j, (lab, v, col, tk) in enumerate(rows):
        if t < tk: continue
        k = ease((t - tk) / .5); y = 730 + j * 170
        d.text((X0, y), lab, font=F(BLK, 40), fill=col); w = 640 * v / 99 * k
        d.rectangle([X0, y + 54, X0 + max(8, w), y + 124], fill=col)
        d.text((X0 + max(8, w) + 14, y + 89), f"{v * k:.0f} %" if v != 50 else ("~ HALF" if k > .9 else ""), font=F(BLK, 52), fill=col, anchor="lm")
    fig(d, "US surveys · a link, not proof")

def sc_point(img, d, t):
    t0, ts = S("point"), cue("point", "Start with the dishes") - .15
    words_in(d, t, [("DON'T JUST DIVIDE.", t0 + .05, 320, 100, MID), ("DO SOME TOGETHER.", t0 + .3, 430, 100, INK)])
    I.grid(img); I.shadow(d, 0, 0, 160)
    plates(I, d, 0, 0, 8, 1 - clamp((t - ts) / 1.2) * .6, top=TOP)
    if t >= ts: words_in(d, t, [("START WITH", ts, 570, 110, SIG), ("THE DISHES.", ts + .12, 680, 110, SIG)])
    fig(d, "fig. 2 — schematic")

EP.cuts = {"together": "stay"}
EP.bg = {"split": "light", "point": "light"}
EP.scenes = {"survey": sc_survey, "split": sc_split, "together": sc_together, "point": sc_point}
FX = [*EP.cut_fx(), (cue("survey", "faithfulness") - .1, pop(.12), -.3), (cue("survey", "Good sex") - .1, pop(.12), 0), (cue("survey", "Sharing chores") - .1, thud(.5), .3),
      *[(S("split") + .3 + i * .08, tick(.035), -.3) for i in range(6)], *[(S("split") + .5 + i * .08, tick(.035), .3) for i in range(6)],
      (S("together") + .05, thud(.55), 0), (S("together") + .5, pop(.14), -.2), (cue("together", "only half") - .15, pop(.13), .2),
      (S("point") + .1, pop(.12), 0), (cue("point", "Start with the dishes") - .15, thud(.5), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
