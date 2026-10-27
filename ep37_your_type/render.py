"""NOT JUST YOU – No. 37: your type isn't your type (Eastwick & Finkel 2008). Area: dating."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .6, "study": .5, "said": .9, "real": .6, "gap": .5, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "said", "real", "gap", "point", "end"]
EP = Episode(TL, 37, "YOUR TYPE", order=ORDER,
             chapters={"hook": "MY TYPE", "study": "THE LIST", "said": "WHAT THEY SAID", "real": "WHAT HAPPENED", "gap": "THE GAP", "point": "GO ANYWAY"},
             sources=("Eastwick & Finkel (2008), Journal of Personality", "and Social Psychology 94(2) · via ScienceDaily"),
             music=dict(bpm=102, root=-2, prog="major", kick="four", gaps=[(E("said") + .05, S("real") + .05)]),
             cover=dict(words=["YOUR", "TYPE?"], kicker="It might just be a theory."))

def heart(d, cx, cy, r, col=SIG):
    d.ellipse([cx - r, cy - r * .9, cx, cy + r * .1], fill=col); d.ellipse([cx, cy - r * .9, cx + r, cy + r * .1], fill=col)
    d.polygon([(cx - r * .98, cy - r * .3), (cx + r * .98, cy - r * .3), (cx, cy + r * .95)], fill=col)

def checklist(d, x, y, items, t, t0, w=520, col=INK):
    d.rectangle([x, y, x + w, y + 90 + len(items) * 76], fill=WHITE, outline=INK, width=4)
    d.text((x + 24, y + 22), "MY TYPE", font=F(COND, 34), fill=SIG)
    for i, it in enumerate(items):
        yy = y + 90 + i * 76; d.rectangle([x + 24, yy, x + 62, yy + 38], outline=INK, width=3)
        if t > t0 + .3 + i * .25: d.line([x + 28, yy + 20, x + 40, yy + 34, x + 64, yy - 4], fill=SIG, width=5)
        d.text((x + 84, yy + 19), it, font=F(COND, 32), fill=col, anchor="lm")

ITEMS = ["tall", "funny", "ambitious", "likes hiking", "no cat people"]
def sc_hook(img, d, t):
    d.text((X0 - 6, 300), "MY TYPE.", font=F(BLK, 200), fill=INK)
    checklist(d, X0, 540, ITEMS, t, 0)
    picto(d, 760, FLOOR, 1.0, INK, f=-1, pose=SHRUG if t >= cue("hook", "right") else IDLE)
    fig(d, "fig. 1 — the list in your head")

def sc_study(img, d, t):
    t0 = S("study")
    d.text((X0, 320), "BEFORE", font=F(BLK, 130), fill=INK)
    d.text((X0, 470), "a speed-dating event", font=F(COND, 36), fill=INK)
    for i in range(3):
        x = X0 + 20 + i * 290; k = ease((t - t0 - .3 - i * .25) / .3)
        if k > 0:
            d.rectangle([x, 560, x + 260, 900], fill=WHITE, outline=INK, width=4)
            for j in range(5): d.line([x + 24, 620 + j * 54, x + 230 - ((i + j) * 30) % 90, 620 + j * 54], fill=INK if j else SIG, width=6)
    fig(d, "questionnaires, about 10 days before · Eastwick & Finkel, 2008")

def pair_bars(d, y, title, a, b, k, la="men", lb="women"):
    d.text((X0, y), title, font=F(BLK, 44), fill=INK)
    d.rectangle([X0, y + 66, X0 + (X1 - X0) * a * ease(k), y + 126], fill=INK); d.text((X0 + 10, y + 96), la, font=F(COND, 26), fill=WHITE if a * k > .15 else INK, anchor="lm")
    d.rectangle([X0, y + 140, X0 + (X1 - X0) * b * ease(k), y + 200], fill=SIG); d.text((X0 + 10, y + 170), lb, font=F(COND, 26), fill=WHITE if b * k > .15 else INK, anchor="lm")

def sc_said(img, d, t):
    t0 = S("said")
    d.text((X0, 320), "THEY SAID", font=F(BLK, 130), fill=INK)
    pair_bars(d, 500, "looks matter", .85, .5, (t - cue("said", "looks") + .2) / .5)
    pair_bars(d, 780, "earning potential matters", .45, .8, (t - cue("said", "earning") + .2) / .5)
    d.text((X1, 1146), "stated preferences · schematic", font=F(MED, 22), fill=MID, anchor="ra")

def sc_real(img, d, t):
    t0 = S("real")
    d.text((X0, 320), "AT THE DATES", font=F(BLK, 120), fill=SIG)
    pair_bars(d, 500, "looks", .8, .8, (t - t0 - .1) / .5)
    pair_bars(d, 780, "earning potential", .4, .4, (t - t0 - .4) / .5)
    if t >= cue("real", "about the same"): box_label(d, X1, 470, "SAME FOR BOTH", 30, WHITE, INK, anchor="ra")
    d.text((X1, 1146), "actual attraction · schematic", font=F(MED, 22), fill=MID, anchor="ra")

def sc_gap(img, d, t):
    t0 = S("gap"); lk = cue("gap", "actually liked")
    d.text((X0, 320), "SAID ≠ FELT", font=F(BLK, 140), fill=INK)
    checklist(d, X0, 520, ITEMS, t + 99, 0, w=420, col=MID)
    if t >= lk - .2:
        k = ease((t - lk + .2) / .4)
        d.line([X0 + 10, 560, X0 + 410 * k, 900], fill=SIG, width=10)
        heart(d, 720, 760, 90 * back(k))
        box_label(d, 720, 880, "WHO THEY LIKED", 28, WHITE, SIG, anchor="ma")
    fig(d, "stated preferences barely predicted real attraction")

def sc_point(img, d, t):
    t0 = S("point"); ga = cue("point", "go on")
    words_in(d, t, [("JUST A", t0, 300, 160, INK), ("THEORY.", t0 + .3, 460, 160, INK)] if t < ga - .2 else [("GO ON", ga - .2, 300, 160, INK), ("THE DATE.", ga, 460, 160, SIG)])
    picto(d, 330, FLOOR, 1.0, INK, f=1, pose=WALK(t) if t >= ga else IDLE)
    picto(d, 690, FLOOR, 1.0, SIG, f=-1, pose=WAVE(t) if t >= ga else IDLE)
    if t >= ga: heart(d, 510, 700 - 10 * math.sin(t * 4), 34)
    fig(d, "fig. 2 — the only way to find out")

EP.scenes = {"hook": sc_hook, "study": sc_study, "said": sc_said, "real": sc_real, "gap": sc_gap, "point": sc_point}
FX = [(0.0, thud(.5), 0), *[(.3 + i * .25, pop(.1), (i - 2) / 3) for i in range(5)], *EP.cut_fx(),
      *[(S("study") + .3 + i * .25, pop(.12), (i - 1) / 2) for i in range(3)], (cue("said", "looks"), pop(.15), -.2), (cue("said", "earning"), pop(.15), .2),
      (S("real") + .05, thud(.55), 0), (cue("real", "about the same"), thud(.35), 0), (cue("gap", "actually liked"), riser(.4, .07), 0),
      (cue("point", "go on"), thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
