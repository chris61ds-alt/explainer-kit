"""NOT JUST YOU – No. 101: the liking gap – after a first conversation people like us more than we think (Boothby et al. 2018). Look C+D · claim opener."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"study": .6, "result": .5, "roommates": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["study", "result", "roommates", "point", "end"]
EP = ThreadEpisode(TL, 101, "LIKING GAP", order=ORDER, dark=True, label="5 STUDIES",
                   chapters={k: "" for k in ORDER[:-1]}, sources=("Boothby, Cooney, Sandstrom & Clark (2018),", "The Liking Gap in Conversations, Psychological Science"),
                   music=dict(bpm=100, root=2, prog="major", kick="four", audio="v5", gaps=[(E("study") + .05, S("result") + .05)]),
                   cover=dict(words=["THEY LIKE YOU", "MORE THAN", "YOU THINK."], kicker="The liking gap."))

def sc_study(img, d, t):
    t0, tq = S("study"), cue("study", "how much do I like") - .1; tm = cue("study", "do they like me") - .1
    d.text((X0, 320), "5-MINUTE", font=F(BLK, 150), fill=INK); d.text((X0, 470), "CHAT", font=F(BLK, 150), fill=INK)
    clock(d, X1 - 80, 600, 56, (t - t0) / 3)
    couple(img, d, labels=("YOU", "STRANGER"))
    if t >= tq: bubble(d, "you", "I like them…", (t - tq) / .3, y=680)
    if t >= tm: bubble(d, "you", "…but do they like me?", (t - tm) / .3, col=MID, y=760, size=30)
    fig(d, "conversation study · schematic")

def gapbars(d, t, k_all=1.0):
    d.text((X0, 320), "HOW MUCH", font=F(BLK, 120), fill=INK); d.text((X0, 440), "THEY LIKED YOU", font=F(BLK, 90), fill=INK)
    t0 = S("result")
    for j, (lab, v, col, tk) in enumerate((("WHAT YOU THOUGHT", .55, MID, t0 + .2), ("ACTUAL", .85, INK, t0 + .6))):
        if t < tk: continue
        k = ease((t - tk) / .6); y = 620 + j * 220
        d.text((X0, y), lab, font=F(BLK, 48), fill=col); d.rectangle([X0, y + 66, X0 + 760 * v * k, y + 176], fill=col)
    tg = t0 + 1.3
    if t >= tg:
        k = ease((t - tg) / .4); x0, x1 = X0 + 760 * .55, X0 + 760 * .85; y = 1070
        d.line([x0, y, x0 + (x1 - x0) * k, y], fill=SIG, width=8); d.line([x0, y - 16, x0, y + 16], fill=SIG, width=8)
        if k >= 1: d.line([x1, y - 16, x1, y + 16], fill=SIG, width=8); d.text(((x0 + x1) / 2, y + 22), "THE GAP", font=F(BLK, 34), fill=SIG, anchor="ma")

def sc_result(img, d, t): gapbars(d, t); fig(d, "bars schematic")
def sc_roommates(img, d, t):
    gapbars(d, t); t0 = S("roommates")
    box_label(d, X1, 560, "ROOMMATES: MONTHS LATER", 40, WHITE, SIG, font=BLK, anchor="ra") if t >= t0 + .05 else None
    fig(d, "bars schematic")

def sc_point(img, d, t):
    t0, tb = S("point"), cue("point", "It went better") - .2
    words_in(d, t, [("THAT AWKWARD", t0 + .05, 320, 110, MID), ("CHAT?", t0 + .2, 435, 110, MID)] + ([("IT WENT", tb, 600, 140, INK), ("BETTER.", tb + .15, 745, 160, SIG)] if t >= tb else []))
    fig(d, "fig. 2 — the liking gap")

EP.cuts = {"roommates": "stay"}
EP.scenes = {"study": sc_study, "result": sc_result, "roommates": sc_roommates, "point": sc_point}
FX = [(0.0, thud(.5), 0), *EP.cut_fx(), (S("study") + .1, riser(.8, .04), 0), (cue("study", "how much do I like") - .1, pop(.13), -.2), (cue("study", "do they like me") - .1, pop(.13), .2),
      (S("result") + .2, pop(.12), -.2), (S("result") + .6, thud(.45), 0), (S("result") + 1.3, whoosh(.3, .05), .2),
      (S("roommates") + .05, thud(.55), 0), (S("point") + .1, pop(.12), 0), (cue("point", "It went better") - .2, thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
