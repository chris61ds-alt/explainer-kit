"""NOT JUST YOU – No. 56: revenge makes you feel worse (Carlsmith, Wilson & Gilbert 2008). Swiss Dark."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .8, "result": .5, "predict": .5, "why": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "predict", "why", "point", "end"]
EP = Episode(TL, 56, "REVENGE", order=ORDER, dark=True,
             chapters={"hook": "SWEET?", "study": "THE CHEATER", "result": "THE PUNISHERS", "predict": "THE FORECAST", "why": "WHY", "point": "THE WOUND"},
             sources=("Carlsmith, Wilson & Gilbert (2008), Journal of", "Personality and Social Psychology 95(6)"),
             music=dict(bpm=88, root=-4, prog="minor", kick="half", gaps=[(E("study") + .05, S("result") + .05)]),
             cover=dict(words=["REVENGE", "IS SWEET?"], kicker="It makes you feel worse."))

def coins(d, x, y, n, col=SIG):
    for i in range(n): d.ellipse([x - 34, y - i * 14 - 12, x + 34, y - i * 14 + 12], fill=col if i % 2 else INK, outline=BG, width=3)

def sc_hook(img, d, t):
    tu = cue("hook", "until")
    d.text((X0 - 6, 300), "REVENGE", font=F(BLK, 200), fill=INK)
    d.text((X0 - 6, 490), "= SWEET?" if t < tu else "= SOUR.", font=F(BLK, 170), fill=SIG)
    picto(d, 360, FLOOR, 1.0, INK, f=1, pose=LAUGH if t < tu else WORRY)
    cx, cy = 650, 860
    d.ellipse([cx - 70, cy - 70, cx + 70, cy + 70], fill=SIG if t < tu else MID)
    d.line([cx, cy - 70, cx + 20, cy - 110], fill=INK, width=8)
    fig(d, "fig. 1 — the fantasy")

def sc_study(img, d, t):
    t0 = S("study"); tc = cue("study", "secretly cheated"); tp = cue("study", "punish")
    d.text((X0, 300), "THE MONEY GAME", font=F(BLK, 110), fill=INK)
    xs = (200, 380, 560, 760)
    for i, x in enumerate(xs):
        cheat = i == 3
        picto(d, x, FLOOR, .75, SIG if cheat and t >= tc else INK, f=-1 if cheat else 1, pose=LAUGH if cheat and t >= tc else IDLE)
        coins(d, x, 760, 9 if cheat and t >= tc else 4)
    if t >= tc: box_label(d, xs[3], 560, "FREE RIDER", 30, WHITE, SIG, anchor="ma")
    if t >= tp: box_label(d, X0, 470, "PUNISH HIM? (COSTS YOU)", 34, WHITE, INK)
    fig(d, "public-goods game with a planted cheater · 2008")

def sc_result(img, d, t):
    t0 = S("result"); tw = cue("result", "feeling worse")
    d.text((X0, 300), "100 %", font=F(BLK, 200), fill=SIG); d.text((X0 + 6, 510), "of those who could, punished", font=F(COND, 36), fill=INK)
    hbar(d, 640, .62, (t - tw + .4) / .5, MID, "mood: couldn't punish", h=90)
    hbar(d, 820, .42, (t - tw) / .5, SIG, "mood: punished", h=90)
    if t >= tw + .4: box_label(d, X0 + 840 * .42 + 30, 830, "WORSE", 44, WHITE, SIG)
    d.text((X1, 1146), "schematic", font=F(MED, 22), fill=MID, anchor="ra")

def sc_predict(img, d, t):
    t0 = S("predict"); tn = cue("predict", "it didn't")
    d.text((X0, 300), "EXPECTED:", font=F(BLK, 120), fill=INK)
    hbar(d, 470, .85, (t - t0 - .2) / .5, MID, "how good revenge would feel", h=90)
    d.text((X0, 680), "ACTUAL:", font=F(BLK, 120), fill=SIG)
    hbar(d, 850, .4, (t - tn) / .5, SIG, "how it felt", h=90)
    fig(d, "both groups overestimated it · schematic")

def sc_why(img, d, t):
    t0 = S("why"); tm = cue("why", "moved on")
    d.text((X0, 300), "REPLAY", font=F(BLK, 170), fill=SIG)
    h = picto(d, 300, FLOOR, .85, INK, f=1, pose=WORRY)
    box = think_box(d, h, 220, 120, (t - t0 - .2) / .4, "", INK, 1)
    if box:
        cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2; a = t * 6
        d.arc([cx - 34, cy - 34, cx + 34, cy + 34], math.degrees(a) % 360, math.degrees(a) % 360 + 270, fill=SIG, width=8)
    if t >= tm - .3:
        picto(d, 720, FLOOR, .85, MID, f=-1, pose=WALK(t)); box_label(d, 720, 680, "MOVED ON", 30, WHITE, MID, anchor="ma")
    fig(d, "punishers kept thinking about it")

def sc_point(img, d, t):
    t0 = S("point"); to = cue("point", "keeps it open")
    words_in(d, t, [("NO CLOSURE.", t0 + .2, 300, 140, INK), ("IT STAYS OPEN.", to - .1, 450, 110, SIG)])
    picto(d, 480, FLOOR, 1.0, INK, f=1, pose=SHRUG if t >= to else IDLE)
    fig(d, "fig. 2 — let it go, literally")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "predict": sc_predict, "why": sc_why, "point": sc_point}
FX = [(0.0, thud(.5), 0), (cue("hook", "until"), rewind_sfx(.12, .4), 0), *EP.cut_fx(), (cue("study", "secretly cheated"), pop(.18), .3),
      (cue("study", "punish"), thud(.35), 0), (S("result") + .05, thud(.55), 0), (cue("result", "feeling worse") + .4, thud(.4), 0),
      (cue("predict", "it didn't"), pop(.15), 0), (S("why") + .2, whoosh(.8, .06), 0), (cue("point", "keeps it open") - .1, thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
