"""NOT JUST YOU – No. 119: deep talks – strangers expected deep conversations to be awkward; they were far less awkward than
predicted, felt closer and more enjoyable (Kardas, Kumar & Epley 2021, JPSP, 12 experiments, 1,800+ people).
Look C+D · statement opener with "you" · isometric two chairs with a small-talk vs. deep bubble · orange reveal: less awkward."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"study": .6, "example": .5, "guess": .5, "result": .6, "interest": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["study", "example", "guess", "result", "interest", "point", "end"]
EP = ThreadEpisode(TL, 119, "DEEP TALK", order=ORDER, dark=True, label="12 EXPERIMENTS · 1,800+ PEOPLE",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Kardas, Kumar & Epley (2021), Overly shallow?", "J. of Personality and Social Psychology"),
                   music=dict(bpm=96, root=1, prog="dream", kick="four", audio="v5", gaps=[(E("study") + .05, S("example") + .05)]),
                   cover=dict(words=["YOU AVOID", "DEEP", "TALKS."], kicker="You think they'll be awkward. They're not."))

I = Iso(500, 1000, .78)
def sc_study(img, d, t):
    t0, ts, tdp = S("study"), cue("study", "small talk") - .1, cue("study", "deep ones") - .1
    d.text((X0, 320), "STRANGERS,", font=F(BLK, 120), fill=INK); d.text((X0, 440), "PAIRED UP", font=F(BLK, 120), fill=INK)
    I.grid(img); I.shadow(d, 0, 0, 280)
    A = chairs(I, d, t, T=[t0 + .05 + i * .1 for i in range(4)])
    if t >= ts: p = I.P(*A["you"]); box_label(d, p[0] - 120, p[1] - 140, "THE WEATHER?", 34, WHITE, MID, font=BLK)
    if t >= tdp: p = I.P(*A["them"]); box_label(d, p[0] - 60, p[1] - 200, "WHEN DID YOU CRY?", 34, WHITE, INK, font=BLK)
    fig(d, "fig. 1 — schematic")

def sc_example(img, d, t):
    t0 = S("example")
    d.text((X0, 320), "A DEEP ONE:", font=F(BLK, 110), fill=MID)
    words_in(d, t, [("\"WHEN DID YOU", t0 + .1, 470, 110, INK), ("LAST CRY IN", t0 + .25, 580, 110, INK), ("FRONT OF", t0 + .4, 690, 110, INK), ("SOMEONE?\"", t0 + .55, 800, 110, INK)])
    fig(d, "one of the study's questions")

def meter(d, y, lab, v, col, k):
    d.text((X0, y), lab, font=F(BLK, 46), fill=col)
    w = 760 * v * ease(clamp(k)); d.rectangle([X0, y + 64, X0 + 760, y + 144], outline=RULE, width=4)
    d.rectangle([X0, y + 64, X0 + max(6, w), y + 144], fill=col)

def sc_guess(img, d, t):
    t0 = S("guess"); d.text((X0, 320), "AWKWARD?", font=F(BLK, 150), fill=INK)
    meter(d, 560, "PREDICTED", .78, MID, (t - t0 - .2) / .6)
    fig(d, "awkwardness · schematic")

def sc_result(img, d, t):
    t0, tc = S("result"), cue("result", "closer and more fun") - .1
    d.text((X0, 320), "AWKWARD?", font=F(BLK, 150), fill=INK)
    meter(d, 560, "PREDICTED", .78, MID, 1)
    meter(d, 760, "ACTUALLY", .32, SIG, (t - t0 - .1) / .6)
    if t >= tc: box_label(d, X0 + 4 - (1 - ease((t - tc) / .2)) * 40, 960, "CLOSER · MORE FUN", 52, WHITE, INK, font=BLK)
    fig(d, "direction only · schematic")

def sc_interest(img, d, t):
    t0 = S("interest")
    words_in(d, t, [("THEY WERE", t0 + .05, 320, 140, INK), ("MORE INTERESTED", t0 + .2, 470, 100, INK), ("IN YOU", t0 + .35, 580, 140, INK), ("THAN YOU THINK.", t0 + .5, 730, 100, MID)])
    fig(d, "underestimated interest")

def sc_point(img, d, t):
    t0, ta = S("point"), cue("point", "Ask the real") - .15
    words_in(d, t, [("SKIP THE", t0 + .05, 320, 150, MID), ("WEATHER.", t0 + .2, 470, 150, MID)] + ([("ASK THE REAL", ta, 640, 120, SIG), ("QUESTION.", ta + .15, 760, 120, SIG)] if t >= ta else []))
    fig(d, "fig. 2 — go deeper")

EP.cuts = {"result": "stay"}
EP.bg = {"study": "light"}
EP.scenes = {"study": sc_study, "example": sc_example, "guess": sc_guess, "result": sc_result, "interest": sc_interest, "point": sc_point}
FX = [*EP.cut_fx(), *[(S("study") + .05 + i * .1, tick(.04), (i - 1.5) / 2) for i in range(4)], (cue("study", "small talk") - .1, pop(.12), -.3), (cue("study", "deep ones") - .1, pop(.14), .3),
      *[(S("example") + .1 + i * .15, tick(.04), 0) for i in range(4)], (S("guess") + .2, riser(.6, .04), 0),
      (S("result") + .05, thud(.55), 0), (cue("result", "closer and more fun") - .1, pop(.14), 0),
      (S("interest") + .1, pop(.12), -.2), (S("interest") + .4, pop(.12), .2), (S("point") + .1, pop(.12), 0), (cue("point", "Ask the real") - .15, thud(.5), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
