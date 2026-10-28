"""NOT JUST YOU – No. 53: why every fight escalates (Shergill, Bays, Frith & Wolpert 2003). Swiss Dark."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .8, "result": .5, "why": .5, "both": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "why", "both", "point", "end"]
EP = Episode(TL, 53, "THEY STARTED IT", order=ORDER, dark=True,
             chapters={"hook": "WHO STARTED IT", "study": "THE EXPERIMENT", "result": "+38 %", "why": "THE BRAIN", "both": "BOTH SIDES", "point": "TONE IT DOWN"},
             sources=("Shergill, Bays, Frith & Wolpert (2003),", "Science 301(5630)"),
             music=dict(bpm=104, root=-1, prog="tense", kick="four", gaps=[(E("study") + .05, S("result") + .05)]),
             cover=dict(words=["THEY", "STARTED IT."], kicker="Everyone thinks so."))

PUSH = {"arms": ((80, 85), (-10, -5))}
def duo(d, t, gap=190, s=1.0, pushA=0.0, pushB=0.0):
    picto(d, 480 - gap, FLOOR, s, INK, f=1, pose=blend(IDLE, PUSH, pushA), tilt=6 * pushA)
    picto(d, 480 + gap, FLOOR, s, SIG, f=-1, pose=blend(IDLE, PUSH, pushB), tilt=6 * pushB)

def sc_hook(img, d, t):
    ts = cue("hook", "so do")
    d.text((X0 - 6, 300), "THEY", font=F(BLK, 230), fill=INK); d.text((X0 - 6, 510), "STARTED IT.", font=F(BLK, 150), fill=SIG)
    a = .5 + .5 * math.sin(t * 5)
    duo(d, t, 170, 1.0, a if t < ts else .4, (1 - a) if t >= ts else .2)
    if t >= ts:
        speech_box(d, 300, 610, 150, (t - ts) / .25, INK, 1, "YOU!", 34); speech_box(d, 660, 610, 150, (t - ts - .3) / .25, SIG, -1, "YOU!", 34)
    fig(d, "fig. 1 — every argument, ever")

def sc_study(img, d, t):
    t0 = S("study")
    d.text((X0, 300), "PRESS BACK.", font=F(BLK, 150), fill=INK); d.text((X0, 470), "SAME FORCE.", font=F(BLK, 150), fill=SIG)
    k = .5 + .5 * math.sin((t - t0) * 3)
    for side, col in ((-1, INK), (1, SIG)):
        x = 480 + side * 140
        d.rectangle([x - 70, 900, x + 70, 960], fill=col)
        d.rounded_rectangle([x - 18, 760 + (20 * k if side < 0 else 20 * (1 - k)), x + 18, 900], radius=16, fill=col)
    d.rectangle([380, 850, 580, 870], fill=MID)
    fig(d, "6 pairs, finger presses, 8 turns · Shergill et al., 2003")

def sc_result(img, d, t):
    t0 = S("result"); tr = cue("result", "thirty-eight")
    counter(d, X0, 300, t, tr - .3, .6, 38, "+{:.0f} %", 220, SIG)
    d.text((X0 + 6, 540), "per turn, on average", font=F(COND, 36), fill=INK)
    k = clamp((t - t0) / 2.4); n = int(1 + 7 * k)
    v = 1.0
    for i in range(n):
        h = min(420, 40 * v); x = X0 + 30 + i * 105
        d.rectangle([x, 1060 - h, x + 80, 1060], fill=SIG if i % 2 else INK)
        d.text((x + 40, 1076), f"{i + 1}", font=F(MONO, 20), fill=MID, anchor="ma")
        v *= 1.38
    d.line([X0, 1060, X1, 1060], fill=INK, width=4)
    d.text((X1, 1146), "turns · schematic", font=F(MED, 22), fill=MID, anchor="ra")

def sc_why(img, d, t):
    t0 = S("why"); ts = cue("why", "so your")
    d.text((X0, 300), "YOURS:", font=F(BLK, 120), fill=INK); d.text((X0 + 470, 300), "THEIRS:", font=F(BLK, 120), fill=SIG)
    hbar(d, 560, .45, (t - ts + .3) / .5, MID, "how hard it feels when you push", h=90)
    hbar(d, 760, .9, (t - ts) / .5, SIG, "how hard it feels when they push", h=90)
    if t >= cue("why", "even when") - .1: box_label(d, X0, 960, "SAME ACTUAL FORCE", 40, WHITE, INK)
    fig(d, "your brain dampens self-made touch · schematic")

def sc_both(img, d, t):
    t0 = S("both"); tt = cue("both", "they pushed")
    d.text((X0, 300), "BOTH SIDES:", font=F(BLK, 130), fill=INK)
    duo(d, t, 200, .9, .3, .3)
    speech_box(d, 330, 640, 300, (t - cue("both", "i matched") + .1) / .3, INK, 1, "I matched it.", 30)
    speech_box(d, 630, 760, 300, (t - tt) / .3, SIG, -1, "They pushed harder!", 26)
    fig(d, "each person was sure the other escalated")

def sc_point(img, d, t):
    t0 = S("point"); th = cue("point", "harder")
    words_in(d, t, [("YOU HIT", t0 + .1, 300, 170, INK), ("HARDER.", th - .2, 470, 170, SIG)])
    k = ease((t - th) / .8)
    picto(d, 300, FLOOR, .95, INK, f=1, pose=blend(PUSH, IDLE, k)); picto(d, 660, FLOOR, .95, SIG, f=-1, pose=IDLE)
    if k > .5: box_label(d, 480, 700, "TONE IT DOWN 38 %", 36, WHITE, INK, anchor="ma")
    fig(d, "fig. 2 — than you think")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "why": sc_why, "both": sc_both, "point": sc_point}
FX = [(0.0, thud(.5), 0), (cue("hook", "so do"), snare(.06), -.3), (cue("hook", "so do") + .3, snare(.06), .3), *EP.cut_fx(),
      *[(S("study") + .3 + i * .5, thud(.2), (i % 2 - .5)) for i in range(6)], (S("result") + .05, thud(.55), 0),
      *[(S("result") + i * .3, tick(.03 + i * .006), (i % 2 - .5) / 2) for i in range(8)], (cue("result", "thirty-eight"), riser(.4, .05), 0),
      (cue("why", "even when"), pop(.15), 0), (cue("both", "i matched"), pop(.15), -.3), (cue("both", "they pushed"), pop(.15), .3),
      (cue("point", "harder") - .2, thud(.5), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
