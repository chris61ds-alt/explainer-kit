"""NOT JUST YOU – No. 81: polarising looks get more messages (OkTrends 2011). Look C+D, dark."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from dating import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .6, "study": .5, "result": .5, "example": .6, "why": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "example", "why", "point", "end"]
EP = ThreadEpisode(TL, 81, "SPLIT OPINION", order=ORDER, dark=True, label="PLATFORM DATA · OKCUPID",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("OkTrends (2011), The Mathematics", "Of Beauty · OkCupid"),
                   music=dict(bpm=98, root=-1, prog="tense", kick="four", gaps=[(E("study") + .05, S("result") + .05)]),
                   cover=dict(words=["SOME SHOULD", "HATE IT."], kicker="More messages, says the data."))

def votes(d, x0, y, vals, k, size=56, gap=12):
    for i, v in enumerate(vals):
        kk = ease((k * len(vals) - i) / 1.5)
        if kk <= 0: continue
        x = x0 + i * (size + gap); hot = v in (1, 5)
        d.rectangle([x, y, x + size, y + size], fill=(SIG if v == 5 else INK) if hot else None, outline=INK, width=4)
        d.text((x + size / 2, y + size / 2), str(v), font=F(BLK, 30), fill=WHITE if hot else INK, anchor="mm")

def sc_hook(img, d, t):
    tu = cue("hook", "ugly") - .3
    d.text((X0 - 6, 320), "MORE", font=F(BLK, 150), fill=INK); d.text((X0 - 6, 470), "MESSAGES?", font=F(BLK, 130), fill=SIG)
    silhouette(img, lambda m: front_bust(m, 640, 830, .5, 255), (380, 700, 900, 1130), INK, cell=9)
    if t >= tu:
        box_label(d, X0, 760, "SOME SHOULD", 46, WHITE, INK, font=BLK); box_label(d, X0, 840, "THINK: UGLY.", 46, WHITE, SIG, font=BLK)
        if t < tu + .3: glitch(img, (380, 700, 900, 1130), 1.0, seed=int(t * 30))
    fig(d, "fig. 1 — the counterintuitive one")

def sc_study(img, d, t):
    t0 = S("study")
    d.text((X0, 320), "SAME AVERAGE", font=F(BLK, 110), fill=INK); d.text((X0, 440), "LOOKS SCORE.", font=F(BLK, 110), fill=MID)
    for i, (x, c) in enumerate(((260, INK), (660, SIG))):
        silhouette(img, lambda m, x=x: front_bust(m, x, 760, .3, 255), (x - 170, 660, x + 170, 920), c, cell=7)
        box_label(d, x, 950, "AVG 3", 40, WHITE, c, font=BLK, anchor="ma")
    fig(d, "~43,000 women · men's ratings")

def sc_result(img, d, t):
    t0, td = S("result"), cue("result", "disagreed") - .3
    d.text((X0, 320), "AGREE", font=F(BLK, 90), fill=MID); votes(d, X0, 430, [3, 3, 3, 3, 3, 3, 3, 3], (t - t0) / .8)
    d.text((X0, 560), "DISAGREE", font=F(BLK, 90), fill=SIG); votes(d, X0, 670, [1, 5, 1, 5, 5, 1, 5, 1], (t - td) / .8 if t >= td else 0)
    if t >= cue("result", "more messages") - .3:
        k = ease((t - cue("result", "more messages") + .3) / .6)
        d.rectangle([X0, 840, X0 + 200 * k, 900], fill=MID); d.rectangle([X0, 930, X0 + 680 * k, 990], fill=SIG)
        if k > .95: d.text((X0 + 680 + 16, 960), "msgs", font=F(BLK, 30), fill=SIG, anchor="lm")
    fig(d, "schematic")

def sc_example(img, d, t):
    t0, t3 = S("example"), cue("example", "three times") - .3
    d.text((X0, 320), "MORE 1s.", font=F(BLK, 150), fill=INK)
    if t >= t3:
        d.text((X0, 500), "3× THE", font=F(BLK, 150), fill=SIG); d.text((X0, 660), "MESSAGES.", font=F(BLK, 130), fill=SIG)
    silhouette(img, lambda m: front_bust(m, 760, 980, .26, 255), (600, 880, 920, 1130), SIG, cell=6)
    fig(d, "rated lowest 142 % more often")

def sc_why(img, d, t):
    t0, tc = S("why"), cue("why", "curse") - .4
    d.text((X0, 320), "LESS", font=F(BLK, 150), fill=INK); d.text((X0, 470), "COMPETITION?", font=F(BLK, 112), fill=MID)
    for i in range(6):
        x = X0 + 60 + i * 140
        silhouette(img, lambda m, x=x: body(m, x, 1120, 280, 255), (x - 80, 820, x + 80, 1125), INK if i == 0 else RULE, cell=6)
    if t >= tc: box_label(d, X0, 660, "“THE CURSE OF BEING CUTE.”", 44, WHITE, SIG, font=BLK)
    fig(d, "OkCupid's own guess")

def sc_point(img, d, t):
    t0, tl = S("point"), cue("point", "lean") - .2
    words_in(d, t, [("DON'T HIDE", t0 + .1, 320, 150, INK), ("YOUR WEIRD.", t0 + .4, 480, 140, MID)] + ([("LEAN IN.", tl, 680, 200, SIG)] if t >= tl else []))
    fig(d, "fig. 2 — polarising beats pleasant")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "example": sc_example, "why": sc_why, "point": sc_point}
FX = [(0.0, thud(.5), 0), (cue("hook", "ugly") - .3, rewind_sfx(.12, .3), 0), *EP.cut_fx(), (S("study") + .2, pop(.15), -.3), (S("study") + .5, pop(.15), .3),
      *[(S("result") + i * .1, tick(.03), 0) for i in range(8)], *[(cue("result", "disagreed") - .3 + i * .1, tick(.04), (i % 2 - .5)) for i in range(8)],
      (cue("result", "more messages") - .3, thud(.45), 0), (cue("example", "three times") - .3, thud(.5), 0), (cue("why", "curse") - .4, pop(.15), 0),
      (cue("point", "lean") - .2, thud(.5), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
