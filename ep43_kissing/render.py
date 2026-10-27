"""NOT JUST YOU · AFTER DARK – No. 43: the romantic kiss is not universal (Jankowiak, Volsche & Garcia 2015)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .6, "study": .8, "result": .5, "regions": .5, "forager": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "regions", "forager", "point", "end"]
EP = Episode(TL, 43, "THE KISS", order=ORDER, dark=True, series="NOT JUST YOU · AFTER DARK",
             chapters={"hook": "HUMAN NATURE?", "study": "168 CULTURES", "result": "THE RESULT", "regions": "BY REGION", "forager": "HUNTER-GATHERERS", "point": "CULTURE"},
             sources=("Jankowiak, Volsche & Garcia (2015),", "American Anthropologist 117(3) · via ScienceAlert"),
             music=dict(bpm=88, root=1, prog="dream", kick="half", gaps=[(E("study") + .05, S("result") + .05)]),
             cover=dict(words=["NOT", "UNIVERSAL."], kicker="Most cultures don't kiss."))

LEAN = {"arms": ((40, 30), (-10, -5)), "tilt": 10}
def couple(d, t, cx=480, s=1.0, kiss=True, col2=SIG):
    gap = 70 * s if kiss else 150 * s
    picto(d, cx - gap, FLOOR, s, INK, f=1, pose=LEAN if kiss else IDLE)
    picto(d, cx + gap, FLOOR, s, col2, f=-1, pose=LEAN if kiss else IDLE)

def sc_hook(img, d, t):
    d.text((X0 - 6, 300), "HUMAN", font=F(BLK, 200), fill=INK); d.text((X0 - 6, 490), "NATURE?", font=F(BLK, 170), fill=SIG)
    couple(d, t, kiss=True)
    fig(d, "fig. 1 — the assumption")

def sc_study(img, d, t):
    t0 = S("study"); k = clamp((t - t0 - .2) / 2.2)
    counter(d, X0, 300, t, t0 + .1, 1.0, 168, "{:.0f}", 220, SIG); d.text((X0 + 6, 540), "cultures, worldwide", font=F(COND, 36), fill=INK)
    for i in range(int(168 * k)):
        r, c = divmod(i, 14); x = X0 + 20 + c * 60; y = 620 + r * 40
        d.rectangle([x, y, x + 48, y + 30], outline=INK, width=2)
    fig(d, "ethnographic records · Jankowiak, Volsche & Garcia, 2015")

def sc_result(img, d, t):
    t0 = S("result"); k = clamp((t - t0 - .2) / 1.0)
    d.text((X0, 300), "≈ 46 %", font=F(BLK, 220), fill=SIG)
    for i in range(168):
        r, c = divmod(i, 14); x = X0 + 20 + c * 60; y = 620 + r * 40
        on = i < 77 * k
        d.rectangle([x, y, x + 48, y + 30], outline=INK, width=2, fill=SIG if on else None)
    if k >= 1: box_label(d, X1, 560, "FEWER THAN HALF", 28, WHITE, INK, anchor="ra")
    fig(d, "share with romantic-sexual kissing")

def sc_regions(img, d, t):
    t0 = S("regions")
    d.text((X0, 300), "BY REGION", font=F(BLK, 140), fill=INK)
    rows = [("Middle East", 10, 10, cue("regions", "middle east") - .3), ("Europe", 7, 10, cue("regions", "middle east") + .3),
            ("North America", 18, 33, cue("regions", "south america") - .6), ("South America", 4, 33, cue("regions", "south america") - .1)]
    for i, (lab, a, b, tk) in enumerate(rows):
        y = 500 + i * 150; k = ease((t - tk) / .5)
        if k <= 0: continue
        d.text((X0, y), lab, font=F(COND, 32), fill=INK); d.text((X1, y), f"{a} of {b}", font=F(BLK, 34), fill=SIG if i in (0, 3) else INK, anchor="ra")
        d.rectangle([X0, y + 50, X1, y + 100], outline=INK, width=3); d.rectangle([X0 + 4, y + 54, X0 + 4 + (X1 - X0 - 8) * a / b * k, y + 96], fill=SIG if i in (0, 3) else INK)
    fig(d, "cultures studied per region")

def sc_forager(img, d, t):
    t0 = S("forager")
    d.text((X0, 300), "FORAGERS", font=F(BLK, 150), fill=INK)
    for i, x in enumerate((220, 420, 620, 800)):
        picto(d, x, FLOOR, .7, MID if i % 2 else INK, f=1 if i < 2 else -1, pose=TALK(t, i) if i % 2 else IDLE)
    if t >= cue("forager", "little sign"): box_label(d, 480, 600, "LITTLE SIGN OF IT", 34, WHITE, SIG, anchor="ma")
    fig(d, "hunter-gatherer societies in the sample")

def sc_point(img, d, t):
    t0 = S("point"); sp = cue("point", "special")
    words_in(d, t, [("NOT NATURE.", t0, 300, 150, INK), ("CULTURE.", cue("point", "culture") - .2, 450, 170, SIG)])
    couple(d, t, kiss=t >= sp - .4)
    if t >= sp - .4:
        r = 30 * back((t - sp + .4) / .4); cx, cy = 480, 720
        d.ellipse([cx - r, cy - r * .9, cx, cy + r * .1], fill=SIG); d.ellipse([cx, cy - r * .9, cx + r, cy + r * .1], fill=SIG)
        d.polygon([(cx - r * .98, cy - r * .3), (cx + r * .98, cy - r * .3), (cx, cy + r * .95)], fill=SIG)
    fig(d, "fig. 2 — a learned tradition, and a nice one")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "regions": sc_regions, "forager": sc_forager, "point": sc_point}
FX = [(0.0, thud(.5), 0), *EP.cut_fx(), *[(S("study") + .2 + i * .12, tick(.04), (i % 5 - 2) / 3) for i in range(16)],
      (S("result") + .05, thud(.55), 0), (cue("regions", "middle east"), pop(.15), -.2), (cue("regions", "south america"), pop(.15), .2),
      (cue("forager", "little sign"), thud(.35), 0), (cue("point", "culture"), thud(.45), 0), (cue("point", "special"), riser(.4, .06), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
