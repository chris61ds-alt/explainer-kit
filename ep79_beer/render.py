"""NOT JUST YOU · AFTER DARK – No. 79: the beer question (OkTrends 2011). Look C+D, dark."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from dating import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .6, "question": .8, "result": .6, "long": .5, "three": .6, "match": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "question", "result", "long", "three", "match", "end"]
EP = ThreadEpisode(TL, 79, "THE BEER QUESTION", order=ORDER, dark=True, series="NOT JUST YOU · AFTER DARK", label="PLATFORM DATA · OKCUPID",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("OkTrends (2011), The Best Questions", "For A First Date · OkCupid"),
                   music=dict(bpm=100, root=0, prog="tense", kick="four", gaps=[(E("question") + .05, S("result") + .05)]),
                   cover=dict(words=["THE BEER", "QUESTION."], kicker="Ask it on date one."))

def sc_hook(img, d, t):
    d.text((X0 - 6, 320), "ONE", font=F(BLK, 220), fill=INK); d.text((X0 - 6, 530), "QUESTION.", font=F(BLK, 150), fill=SIG)
    silhouette(img, lambda m: bust(m, 270, 900, .5, 255, f=1), (60, 760, 500, 1130), INK, cell=8)
    silhouette(img, lambda m: bust(m, 700, 900, .5, 255, f=-1), (470, 760, 910, 1130), MID, cell=8)
    fig(d, "fig. 1 — first date, first night?")

def sc_question(img, d, t):
    t0 = S("question")
    words_in(d, t, [("“DO YOU LIKE", t0, 320, 96, INK), ("THE TASTE OF", t0 + .35, 430, 96, INK), ("BEER?”", cue("question", "beer") - .2, 540, 190, SIG)])
    beer(d, 700, 1120, 1.0, k=(t - t0 - .3) / 1.4, t=t)
    fig(d, "that's it")

def sc_result(img, d, t):
    t0, tm = S("result"), cue("result", "men and women") - .3
    counter(d, X0, 320, t, t0 + .1, .7, 60, "+{:.0f} %", 240, SIG)
    d.text((X0 + 6, 580), "more likely to be okay with", font=F(COND, 40), fill=INK)
    d.text((X0 + 6, 630), "sex with someone they just met", font=F(COND, 40), fill=INK)
    beer(d, 760, 1120, .7, k=1, t=t)
    if t >= tm: box_label(d, X0, 760, "MEN", 50, WHITE, INK, font=BLK); box_label(d, X0 + 150, 760, "& WOMEN", 50, WHITE, SIG, font=BLK)
    fig(d, "beer fans vs. everyone else")

def sc_long(img, d, t):
    t0 = S("long"); ta = cue("long", "ask three") - .2
    d.text((X0, 320), "LONG-TERM?", font=F(BLK, 150), fill=INK)
    if t >= ta: d.text((X0, 500), "ASK 3 THINGS.", font=F(BLK, 130), fill=SIG)
    for i in range(3):
        k = ease((t - ta - i * .15) / .3)
        if k > 0: d.text((X0 + 120 + i * 260, 900), str(i + 1), font=F(BLK, 220), fill=mix(BG, SIG if i == 1 else INK, k), anchor="mm")
    fig(d, "the questions couples agree on")

def sc_three(img, d, t):
    t0 = S("three")
    items = [("HORROR MOVIES?", "horror"), ("TRAVELED ALONE ABROAD?", "traveled"), ("QUIT IT ALL,", "quit"), ("LIVE ON A SAILBOAT?", "sailboat")]
    for i, (lab, w) in enumerate(items):
        tk = cue("three", w) - .25; k = ease((t - tk) / .3)
        if k <= 0: continue
        y = (330, 480, 660, 750)[i]
        box_label(d, X0 + (1 - k) * 40, y, lab, 62 if i != 1 else 54, WHITE, SIG if i in (0, 3) else INK, font=BLK)
    fig(d, "1 · 2 · 3")

def sc_match(img, d, t):
    t0, tn = S("match"), cue("match", "nearly four") - .3
    counter(d, X0, 320, t, t0 + .1, .7, 32, "{:.0f} %", 260, SIG)
    d.text((X0 + 6, 600), "of long-term couples agreed on all 3", font=F(COND, 40), fill=INK)
    silhouette(img, lambda m: bust(m, 270, 920, .42, 255, f=1), (80, 820, 470, 1130), INK, cell=7)
    silhouette(img, lambda m: bust(m, 560, 920, .42, 255, f=-1), (370, 820, 760, 1130), SIG, cell=7)
    if t >= tn: box_label(d, X1, 720, "~4× CHANCE", 48, WHITE, INK, font=BLK, anchor="ra")
    fig(d, "3.7 times the rate of coincidence")

EP.scenes = {"hook": sc_hook, "question": sc_question, "result": sc_result, "long": sc_long, "three": sc_three, "match": sc_match}
FX = [(0.0, thud(.5), 0), *EP.cut_fx(), (S("question") + .3, riser(1.2, .04), 0), (cue("question", "beer") - .2, thud(.55), 0),
      (S("result") + .05, thud(.5), 0), (cue("result", "men and women") - .3, pop(.15), 0), (cue("long", "ask three") - .2, thud(.45), 0),
      *[(cue("three", w) - .25, pop(.15), (i - 1.5) / 2) for i, w in enumerate(("horror", "traveled", "quit", "sailboat"))],
      (S("match") + .05, thud(.5), 0), (cue("match", "nearly four") - .3, pop(.15), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
