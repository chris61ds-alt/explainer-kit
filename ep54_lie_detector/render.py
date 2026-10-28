"""NOT JUST YOU – No. 54: people detect lies at 54 % (Bond & DePaulo 2006). Swiss Dark."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .8, "result": .5, "lies": .5, "why": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "lies", "why", "point", "end"]
EP = Episode(TL, 54, "LIE DETECTOR", order=ORDER, dark=True,
             chapters={"hook": "YOUR GUT", "study": "24,483 JUDGES", "result": "THE SCORE", "lies": "THE LIES", "why": "WHY", "point": "THE COIN"},
             sources=("Bond & DePaulo (2006), Personality and", "Social Psychology Review 10(3)"),
             music=dict(bpm=96, root=-3, prog="minor", kick="four", gaps=[(E("study") + .05, S("result") + .05)]),
             cover=dict(words=["YOU CAN'T", "SPOT A LIE."], kicker="54 %. A coin gets 50."))

def nose(d, h, s, L, col=SIG):
    d.polygon([(h[0] + 38 * s, h[1] - 6 * s), (h[0] + 38 * s + L, h[1] + 2 * s), (h[0] + 38 * s, h[1] + 10 * s)], fill=col)

def coin(d, cx, cy, r, t, spin=True, face="50"):
    w = abs(math.cos(t * 9)) if spin else 1.0
    d.ellipse([cx - r * max(.08, w), cy - r, cx + r * max(.08, w), cy + r], fill=SIG, outline=INK, width=6)
    if w > .5: d.text((cx, cy), face, font=F(BLK, int(r * .7)), fill=WHITE, anchor="mm")

def sc_hook(img, d, t):
    tc = cue("hook", "you can't")
    d.text((X0 - 6, 300), "LIAR?", font=F(BLK, 230), fill=INK)
    h = picto(d, 330, FLOOR, 1.0, INK, f=1, pose=TALK(t)); nose(d, h, 1.0, 30 + 20 * math.sin(t * 3))
    eye(d, 700, 760, 1.4, SIG, 1, (-.6, 0))
    if t >= tc: words_in(d, t, [("YOU CAN'T TELL.", tc, 520, 90, SIG)])
    fig(d, "fig. 1 — you, staring very hard")

def sc_study(img, d, t):
    t0 = S("study"); k = clamp((t - t0 - .3) / 2.0)
    counter(d, X0, 300, t, t0 + .1, 1.2, 24483, "{:,.0f}", 200, SIG)
    d.text((X0 + 6, 520), "people judging lie or truth · 206 studies", font=F(COND, 34), fill=INK)
    for i in range(int(480 * k)):
        r, c = divmod(i, 24); x = X0 + 20 + c * 35; y = 610 + r * 24
        d.text((x, y), "?" if i % 13 else "!", font=F(BLK, 22), fill=MID if i % 13 else SIG, anchor="mm")
    fig(d, "meta-analysis · Bond & DePaulo, 2006")

def sc_result(img, d, t):
    t0 = S("result"); tc = cue("result", "a coin")
    counter(d, X0, 300, t, t0 + .1, .9, 54, "{:.0f} %", 230, SIG)
    d.text((X0 + 6, 540), "correct, overall", font=F(COND, 36), fill=INK)
    hbar(d, 660, .54, (t - t0 - .2) / .6, SIG, "humans", h=100)
    hbar(d, 860, .50, (t - tc) / .5, MID, "coin flip", h=100)
    if t >= tc: coin(d, X1 - 90, 900, 70, t)
    if t >= tc + .8: box_label(d, X0 + 840 * .54 + 20, 640, "+4 POINTS", 30, WHITE, INK)
    fig(d, "accuracy of lie–truth judgments")

def sc_lies(img, d, t):
    t0 = S("lies"); tf = cue("lies", "forty-seven")
    d.text((X0, 300), "LIES CAUGHT:", font=F(BLK, 120), fill=INK)
    counter(d, X0, 440, t, tf - .3, .6, 47, "{:.0f} %", 200, SIG)
    for i in range(10):
        x = X0 + 40 + i * 88; on = i < 5 and t >= tf - .3 + i * .1
        h = picto(d, x, FLOOR, .45, SIG if on else MID, f=1, pose=IDLE); nose(d, h, .45, 30, SIG if on else MID)
    d.text((X1, 1146), "less than half · truths: 61 %", font=F(MED, 22), fill=MID, anchor="ra")

def sc_why(img, d, t):
    t0 = S("why")
    d.text((X0, 300), "TRUTH BIAS", font=F(BLK, 140), fill=INK)
    d.text((X0, 460), "we assume honesty", font=F(COND, 44), fill=SIG)
    for i in range(7):
        k = ease((t - t0 - .3 - i * .2) / .4)
        if k <= 0: continue
        y = 580 + i * 70; lie = i in (2, 5)
        box_label(d, X0 + (1 - k) * 60 + i * 40, y, "lie" if lie else "truth", 36, WHITE, SIG if lie else INK)
        if lie and k > .9: d.text((X1, y + 4), "slips through", font=F(COND, 32), fill=SIG, anchor="ra")
    fig(d, "most messages are judged as true")

def sc_point(img, d, t):
    t0 = S("point"); tc = cue("point", "coin flip"); tw = cue("point", "with confidence")
    words_in(d, t, [("YOUR GUT", t0, 300, 170, INK), ("= A COIN.", tc - .2, 470, 170, SIG)])
    coin(d, 480, 860, 140, t, spin=t < tw, face="?")
    if t >= tw: box_label(d, 480, 1040, "WITH CONFIDENCE", 38, WHITE, INK, anchor="ma")
    fig(d, "fig. 2 — heads or tails")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "lies": sc_lies, "why": sc_why, "point": sc_point}
FX = [(0.0, thud(.5), 0), (cue("hook", "you can't"), thud(.45), 0), *EP.cut_fx(), *[(S("study") + .3 + i * .12, tick(.035), (i % 5 - 2) / 3) for i in range(16)],
      (S("result") + .05, thud(.55), 0), *[(cue("result", "a coin") + i * .08, tick(.05), .4) for i in range(8)],
      (cue("lies", "forty-seven") - .3, pop(.15), 0), *[(S("why") + .3 + i * .2, pop(.1), (i % 3 - 1) / 2) for i in range(7)],
      (cue("point", "coin flip") - .2, thud(.45), 0), (cue("point", "with confidence"), riser(.3, .05), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
