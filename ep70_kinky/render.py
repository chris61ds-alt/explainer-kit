"""NOT JUST YOU · AFTER DARK – No. 70: who's kinkier, men or women (Joyal & Carpentier 2017). Look C+D, dark."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from thread import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .6, "study": .8, "result": .5, "women": .6, "men": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "women", "men", "point", "end"]
EP = ThreadEpisode(TL, 70, "WHO'S KINKIER", order=ORDER, dark=True, series="NOT JUST YOU · AFTER DARK", label="SURVEY · 1,040 PEOPLE",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Joyal & Carpentier (2017),", "Journal of Sex Research 54(2)"),
                   music=dict(bpm=96, root=-2, prog="tense", kick="four", gaps=[(E("study") + .05, S("result") + .05)]),
                   cover=dict(words=["WHO'S", "KINKIER?"], kicker="Not who you think."))

def duo_bars(d, t, t0, label, w, m, y, sig_w=True):
    d.text((X0, y), label, font=F(BLK, 56), fill=INK)
    for j, (v, lab, col) in enumerate(((w, "women", SIG), (m, "men", MID))):
        k = ease((t - t0 - j * .25) / .5); yy = y + 80 + j * 80
        d.rectangle([X0, yy, X0 + 840 * v / 60 * k, yy + 60], fill=col)
        if k > .9: d.text((X0 + 840 * v / 60 * k + 14, yy + 30), f"{v:.0f} %  {lab}", font=F(BLK, 32), fill=col, anchor="lm")

def sc_hook(img, d, t):
    tb = cue("hook", "get ready")
    d.text((X0 - 6, 320), "WHO'S", font=F(BLK, 220), fill=INK); d.text((X0 - 6, 520), "KINKIER?", font=F(BLK, 180), fill=SIG)
    silhouette(img, lambda m: bust(m, 300, 880, .6, 255, f=1), (60, 760, 560, 1130), INK, cell=9)
    silhouette(img, lambda m: bust(m, 660, 880, .6, 255, f=-1), (420, 760, 900, 1130), SIG, cell=9)
    if t >= tb and t < tb + .3: glitch(img, (X0, 300, X1, 760), 1.0, seed=int(t * 30))
    fig(d, "fig. 1 — the stereotype says: him")

def sc_study(img, d, t):
    t0 = S("study")
    counter(d, X0, 320, t, t0 + .1, .9, 1040, "{:,.0f}", 230, SIG)
    d.text((X0 + 6, 560), "adults · anonymous questionnaire", font=F(COND, 40), fill=INK)
    dot_field(d, (X0 + 14, 660, X1, 1100), t, cell=32, col=MID, hit={9, 40, 77, 101, 150})
    fig(d, "Quebec, Canada · Joyal & Carpentier, 2017")

def sc_result(img, d, t):
    t0, tt = S("result"), cue("result", "a third") - .2
    counter(d, X0, 320, t, t0 + .1, .7, 46, "{:.0f} %", 230, SIG)
    d.text((X0 + 6, 560), "want at least one unusual thing", font=F(COND, 40), fill=INK)
    if t >= tt:
        counter(d, X0, 660, t, tt, .6, 34, "{:.0f} %", 180, INK)
        d.text((X0 + 6, 860), "have actually tried one", font=F(COND, 40), fill=INK)
    fig(d, "sample not fully random, rates may run high")

def sc_women(img, d, t):
    t0, tp = S("women"), cue("women", "pain") - .3
    d.text((X0, 320), "WOMEN:", font=F(BLK, 150), fill=SIG)
    duo_bars(d, t, t0 + .2, "FETISHES", 48, 40, 500)
    if t >= tp: duo_bars(d, t, tp, "PAIN & SUBMISSION", 28, 19, 790)
    fig(d, "desire, women vs men")

def sc_men(img, d, t):
    t0 = S("men")
    d.text((X0, 320), "MEN LED", font=F(BLK, 150), fill=INK); d.text((X0, 480), "ELSEWHERE.", font=F(BLK, 150), fill=MID)
    if t >= cue("men", "far smaller") - .3:
        box_label(d, X0, 700, "STEREOTYPE: 20 TO 1", 44, WHITE, MID, font=BLK)
        box_label(d, X0, 800, "REALITY: CLOSE", 56, WHITE, SIG, font=BLK)
    fig(d, "gaps far smaller than commonly assumed")

def sc_point(img, d, t):
    t0, tn = S("point"), cue("point", "might not") - .2
    words_in(d, t, [("THE KINKY ONE", t0, 320, 120, INK), ("MIGHT NOT BE", tn, 460, 120, INK), ("WHO YOU THINK.", tn + .3, 600, 120, SIG)])
    silhouette(img, lambda m: bust(m, 300, 900, .5, 255, f=1), (80, 800, 540, 1130), MID, cell=8)
    silhouette(img, lambda m: bust(m, 640, 900, .5, 255, f=-1), (420, 800, 880, 1130), SIG, cell=8)
    bbox(d, (560, 800, 760, 980), None, SIG, (t - tn - .5) / .3, coords=True)
    fig(d, "fig. 2 — ask, don't assume")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "women": sc_women, "men": sc_men, "point": sc_point}
FX = [(0.0, thud(.5), 0), (cue("hook", "get ready"), rewind_sfx(.1, .3), 0), *EP.cut_fx(), *[(S("study") + .2 + i * .1, tick(.03), (i % 5 - 2) / 3) for i in range(10)],
      (S("result") + .05, thud(.55), 0), (cue("result", "a third") - .2, pop(.15), 0), (S("women") + .2, pop(.15), -.2), (cue("women", "pain") - .3, thud(.4), 0),
      (cue("men", "far smaller") - .3, pop(.15), 0), (cue("point", "might not") - .2, riser(.5, .05), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
