"""NOT JUST YOU – No. 105: after a bad night's sleep couples fight more and read each other worse (Gordon & Chen 2014).
Look C+D · quick-question opener · recap: isometric bed on light paper."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .6, "result": .5, "lab": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "lab", "point", "end"]
EP = ThreadEpisode(TL, 105, "SLEEP FIGHTS", order=ORDER, dark=True, label="DIARY + LAB · 78 PEOPLE, 71 COUPLES",
                   chapters={k: "" for k in ORDER[:-1]}, sources=("Gordon & Chen (2014), The Role of Sleep in Interpersonal", "Conflict, Social Psych. and Personality Science 5(2)"),
                   music=dict(bpm=92, root=-3, prog="dream", kick="half", audio="v5", gaps=[(E("study") + .05, S("result") + .05)]),
                   cover=dict(words=["BAD SLEEP,", "MORE", "FIGHTS."], kicker="You're not imagining it."))
I = Iso(470, 990, .66)

def moon(d, cx, cy, r, col=INK):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col); d.ellipse([cx - r + r * .55, cy - r - r * .15, cx + r + r * .55, cy + r - r * .15], fill=BG)

def bolt(d, cx, cy, s, col=INK):
    d.polygon([(cx + 10 * s, cy - 60 * s), (cx - 30 * s, cy + 6 * s), (cx, cy + 6 * s), (cx - 14 * s, cy + 60 * s), (cx + 30 * s, cy - 10 * s), (cx, cy - 10 * s)], fill=col)

def sc_hook(img, d, t):
    t0 = S("hook"); words_in(d, t, [("NOT", t0 + .05, 320, 170, INK), ("IMAGINING IT.", t0 + .15, 490, 120, SIG)])
    moon(d, 480, 860, 120 * back(clamp((t - t0) / .4)))
    fig(d, "fig. 1 — schematic")

def sc_study(img, d, t):
    t0 = S("study")
    counter(d, X0, 320, t, t0 + .1, .8, 14, "{:.0f} DAYS", 200, INK); d.text((X0 + 6, 545), "sleep + fights, tracked every day", font=F(COND, 46), fill=INK)
    for i in range(14):
        ti = t0 + .5 + i * .2
        if t < ti: continue
        x = X0 + (i % 7) * 122; y = 700 + (i // 7) * 200; d.rounded_rectangle([x, y, x + 100, y + 160], radius=16, outline=INK, width=4)
        h = [120, 60, 110, 40, 120, 90, 50, 115, 70, 120, 35, 100, 110, 80][i]; d.rectangle([x + 30, y + 150 - h, x + 70, y + 150], fill=INK if h > 60 else MID)
    fig(d, "bars: hours slept · schematic")

def sc_result(img, d, t):
    t0, tg = S("result"), cue("result", "Even good") - .1
    d.text((X0, 320), "BAD NIGHT", font=F(BLK, 130), fill=INK); moon(d, X1 - 80, 380, 60)
    if t >= t0 + .5:
        k = ease((t - t0 - .5) / .4); d.text((X0, 470), "= MORE CONFLICT", font=F(BLK, 80), fill=mix(BG, INK, k)); d.text((X0 + 4, 570), "the next day", font=F(COND, 50), fill=MID)
    couple(img, d)
    if t >= t0 + .8: bolt(d, 480, 760, 1.2 * back(clamp((t - t0 - .8) / .3)))
    if t >= tg: box_label(d, X0, 640, "EVEN GOOD SLEEPERS", 40, WHITE, INK, font=BLK)
    fig(d, "diary study · a link, not proof")

def sc_lab(img, d, t):
    t0 = S("lab"); box_label(d, X0, 300, "IN THE LAB", 40, WHITE, INK, font=BLK)
    words_in(d, t, [("TIRED COUPLES", t0 + .05, 370, 110, INK), ("MISREAD", t0 + .2, 490, 150, INK), ("FEELINGS.", t0 + .35, 640, 140, INK)])
    couple(img, d)
    bubble(d, "you", "?", (t - t0 - .6) / .3, y=760, size=44); bubble(d, "partner", "?", (t - t0 - .8) / .3, col=MID, y=760, size=44)
    fig(d, "lab study")

sc_point = iso_recap(TL, "point", I, bed, "SLEEP ON IT.", [("pillow_l", "l", -80, "SLEEP FIRST", INK, "sleep on it"), ("lamp", "r", -40, "TALK AFTER", SIG, "Literally")])

EP.cuts = {"lab": "stay"}
EP.bg = {"point": "light"}
EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "lab": sc_lab, "point": sc_point}
FX = [*EP.cut_fx(), (S("hook") + .05, thud(.45), 0), (S("study") + .1, riser(.8, .04), 0), *[(S("study") + .5 + i * .2, tick(.035), (i % 5 - 2) / 3) for i in range(14)],
      (S("result") + .5, pop(.13), 0), (S("result") + .8, thud(.45), 0), (cue("result", "Even good") - .1, pop(.14), -.2),
      (S("lab") + .05, thud(.55), 0), (S("lab") + .6, pop(.12), -.3), (S("lab") + .8, pop(.12), .3),
      (cue("point", "sleep on it") - .15, pop(.12), -.3), (cue("point", "Literally") - .15, thud(.45), .3), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
