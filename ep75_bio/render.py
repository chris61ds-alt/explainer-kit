"""NOT JUST YOU – No. 75: nobody reads your dating bio (OkCupid 2014). Look C+D, dark."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from dating import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .6, "study": .7, "result": .5, "twist": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "twist", "point", "end"]
EP = ThreadEpisode(TL, 75, "NOBODY READS IT", order=ORDER, dark=True, label="EXPERIMENT · OKCUPID",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Rudder (2014), We Experiment On Human Beings,", "OkCupid blog"),
                   music=dict(bpm=94, root=-3, prog="minor", kick="half", gaps=[(E("study") + .05, S("result") + .05)]),
                   cover=dict(words=["YOUR BIO?", "UNREAD."], kicker="Under 10 % of the verdict."))

def sc_hook(img, d, t):
    tn = cue("hook", "nobody") - .2
    d.text((X0 - 6, 320), "YOUR BIO?", font=F(BLK, 170), fill=INK)
    profile_card(img, d, 330, 880, .78, photo=1, cross_text=t >= tn)
    if t >= tn:
        box_label(d, 560, 820, "UNREAD", 60, WHITE, SIG, font=BLK)
        bbox(d, (150, 1000, 520, 1110), None, SIG, (t - tn) / .3, coords=True)
    fig(d, "fig. 1 — one hour of writing")

def sc_study(img, d, t):
    t0, ts = S("study"), cue("study", "some saw only") - .2
    d.text((X0, 320), "RATE:", font=F(BLK, 120), fill=INK)
    box_label(d, X0, 470, "LOOKS", 40, WHITE, INK, font=BLK); box_label(d, X0 + 200, 470, "PERSONALITY", 40, WHITE, SIG, font=BLK)
    profile_card(img, d, 270, 850, .68, photo=1, text=1)
    d.text((270, 1110), "photo + text", font=F(COND, 34), fill=INK, anchor="ma")
    if t >= ts:
        profile_card(img, d, 690, 850, .68, photo=1, text=0, col=SIG)
        d.text((690, 1110), "photo only", font=F(COND, 34), fill=SIG, anchor="ma")
    fig(d, "text hidden for some raters")

def sc_result(img, d, t):
    t0, tl = S("result"), cue("result", "less than") - .3
    d.text((X0, 320), "BARELY MOVED.", font=F(BLK, 112), fill=INK)
    if t >= tl:
        d.text((X0, 470), "< 10 %", font=F(BLK, 220), fill=SIG)
        d.text((X0 + 6, 710), "of the verdict came from your text", font=F(COND, 40), fill=INK)
        k = ease((t - tl - .3) / .7)
        d.rectangle([X0, 820, X0 + (X1 - X0) * .91 * k, 900], fill=INK); d.rectangle([X0 + (X1 - X0) * .91 * k, 820, X0 + (X1 - X0) * (.91 * k + .09 * k), 900], fill=SIG)
        if k > .95: d.text((X0, 920), "photo", font=F(BLK, 30), fill=INK); d.text((X1, 920), "text", font=F(BLK, 30), fill=SIG, anchor="ra")
    fig(d, "schematic split")

def sc_twist(img, d, t):
    t0, tn = S("twist"), cue("twist", "ninety-two") - .3
    d.text((X0, 320), "LOOKS", font=F(BLK, 130), fill=INK); d.text((X0, 460), "= PERSONALITY?", font=F(BLK, 104), fill=SIG)
    k = ease((t - t0 - .4) / .8)
    d.rectangle([X0, 660, X0 + 700 * k, 730], fill=INK); d.text((X0, 740), "looks", font=F(COND, 30), fill=INK)
    d.rectangle([X0, 800, X0 + 690 * k, 870], fill=SIG); d.text((X0, 880), "personality", font=F(COND, 30), fill=SIG)
    if t >= tn:
        counter(d, X1, 950, t, tn, .6, 92, "{:.0f} %", 150, SIG, anchor="ra")
        d.text((X1, 1110), "almost the same score", font=F(COND, 34), fill=INK, anchor="ra")
    fig(d, "within half a point")

def sc_point(img, d, t):
    t0, tp = S("point"), cue("point", "your photo") - .2
    words_in(d, t, [("YOUR WORDS", t0 + .1, 320, 130, MID), ("MATTER.", t0 + .4, 460, 130, MID)] + ([("YOUR PHOTO", tp, 640, 130, INK), ("TALKS LOUDER.", tp + .25, 780, 112, SIG)] if t >= tp else []))
    fig(d, "fig. 2 — choose the photo first")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "twist": sc_twist, "point": sc_point}
FX = [(0.0, thud(.5), 0), (cue("hook", "nobody") - .2, rewind_sfx(.12, .3), 0), *EP.cut_fx(), (S("study") + .2, pop(.15), -.3), (cue("study", "some saw only") - .2, pop(.15), .3),
      (S("result") + .05, thud(.5), 0), (cue("result", "less than") - .3, thud(.45), 0), (S("twist") + .4, riser(.8, .04), 0), (cue("twist", "ninety-two") - .3, thud(.5), 0),
      (cue("point", "your photo") - .2, thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
