"""NOT JUST YOU – No. 35: the rejection mindset in online dating (Pronk & Denissen 2020). Area: dating."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .5, "result": .6, "mood": .5, "name": .5, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "mood", "name", "point", "end"]
EP = Episode(TL, 35, "SWIPE FATIGUE", order=ORDER,
             chapters={"hook": "NOBODY?", "study": "THE STUDY", "result": "THE RESULT", "mood": "THE MOOD", "name": "THE NAME", "point": "TAKE A BREAK"},
             sources=("Pronk & Denissen (2020), Social Psychological", "and Personality Science 11(3) · via PsyPost"),
             music=dict(bpm=104, root=-1, prog="minor", kick="four", gaps=[(E("study") + .05, S("result") + .05)]),
             cover=dict(words=["NOBODY", "LOOKS", "GOOD?"], kicker="Blame the swiping."))

def heart(d, cx, cy, r, col=SIG):
    d.ellipse([cx - r, cy - r * .9, cx, cy + r * .1], fill=col); d.ellipse([cx, cy - r * .9, cx + r, cy + r * .1], fill=col)
    d.polygon([(cx - r * .98, cy - r * .3), (cx + r * .98, cy - r * .3), (cx, cy + r * .95)], fill=col)

def xmark(d, cx, cy, r, col=INK, w=12):
    d.line([cx - r, cy - r, cx + r, cy + r], fill=col, width=w); d.line([cx - r, cy + r, cx + r, cy - r], fill=col, width=w)

def profile_card(d, cx, cy, s=1.0, dx=0.0, rot_col=None, seed=0):
    w, h = 300 * s, 420 * s; x0, y0 = cx - w / 2 + dx, cy - h / 2
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=WHITE, outline=INK, width=int(5 * s))
    d.rectangle([x0 + 20 * s, y0 + 20 * s, x0 + w - 20 * s, y0 + h * .68], fill=RULE)
    picto(d, x0 + w / 2, y0 + h * .68, .5 * s, [INK, MID, SIG][seed % 3], pose=IDLE)
    d.line([x0 + 24 * s, y0 + h * .78, x0 + w * .6, y0 + h * .78], fill=INK, width=int(8 * s)); d.line([x0 + 24 * s, y0 + h * .87, x0 + w * .8, y0 + h * .87], fill=RULE, width=int(6 * s))
    if rot_col == "no": xmark(d, x0 + w - 50 * s, y0 + 50 * s, 26 * s, INK, int(8 * s))
    if rot_col == "yes": heart(d, x0 + w - 50 * s, y0 + 50 * s, 28 * s)

def swipe_stack(d, t, t0, rate, cx=480, cy=780, sc=.9):
    """cards fly off; rate = fraction of 'yes' (right)"""
    period = .45; n = int(max(0, t - t0) / period); ph = (max(0, t - t0) % period) / period
    profile_card(d, cx, cy + 16, sc, 0, seed=n + 1)
    yes = ((n * 7) % 10) / 10 < rate
    dx = ease(ph) * (600 if yes else -600)
    profile_card(d, cx, cy, sc, dx, "yes" if yes else "no", seed=n)
    return n

def sc_hook(img, d, t):
    d.text((X0 - 6, 300), "NOBODY?", font=F(BLK, 200), fill=INK)
    phone(d, 480, 800, 2.6, INK)
    n = swipe_stack(d, t, 0, .1, 480, 790, .62)
    box_label(d, X1, 1080, f"swipes: {n * 9}", 28, WHITE, SIG, anchor="ra")
    fig(d, "fig. 1 — minute ten")

def sc_study(img, d, t):
    t0 = S("study")
    d.text((X0, 320), "YES OR NO", font=F(BLK, 130), fill=INK)
    swipe_stack(d, t, t0, .5, 480, 780)
    heart(d, X1 - 60, 1060, 40); xmark(d, X0 + 60, 1060, 30)
    fig(d, "3 studies · Pronk & Denissen, 2020")

def sc_result(img, d, t):
    t0 = S("result")
    d.text((X0, 320), "YES-RATE", font=F(BLK, 130), fill=INK)
    ox, oy, w, h = X0 + 20, 1020, X1 - X0 - 40, 440
    d.line([ox, oy, ox + w, oy], fill=INK, width=4); d.line([ox, oy, ox, oy - h], fill=INK, width=4)
    d.text((ox + w, oy + 20), "profiles seen", font=F(COND, 26), fill=INK, anchor="ra")
    k = clamp((t - t0) / 2.2); pts = []
    for i in range(int(60 * k) + 1):
        u = i / 60; pts.append((ox + w * u, oy - h * (.82 - .45 * u - .03 * math.sin(i * 1.3))))
    if len(pts) > 1: d.line(pts, fill=SIG, width=6)
    if k > .95: box_label(d, pts[-1][0], pts[-1][1] - 70, "FEWER YESES", 28, WHITE, SIG, anchor="ra")
    d.text((X1, 1146), "schematic", font=F(MED, 22), fill=MID, anchor="ra")

def sc_mood(img, d, t):
    t0 = S("mood")
    d.text((X0, 320), "AND YOU?", font=F(BLK, 130), fill=INK)
    for i, (lab, v, tk) in enumerate((("satisfied with the options", .25, cue("mood", "satisfied")), ("hope you'll get a match", .2, cue("mood", "pessimistic")))):
        y = 540 + i * 200; k = ease((t - tk + .1) / .6)
        d.text((X0, y), lab, font=F(COND, 32), fill=INK)
        d.rectangle([X0, y + 50, X1, y + 120], outline=INK, width=4)
        d.rectangle([X0 + 6, y + 56, X0 + 6 + (X1 - X0 - 12) * lerp(.8, v, k), y + 114], fill=SIG if i else INK)
    picto(d, 480, FLOOR, .6, INK, pose=WORRY)
    fig(d, "both dropped while swiping · schematic")

def sc_name(img, d, t):
    words_in(d, t, [("REJECTION", cue("name", "rejection") - .1, 320, 160, INK), ("MINDSET.", cue("name", "mindset") - .1, 480, 160, SIG)])
    for i in range(7): xmark(d, X0 + 60 + i * 125, 820 + 20 * math.sin(i), 34, INK if i % 2 else SIG, 10)
    fig(d, "choice overload in online dating")

def sc_point(img, d, t):
    t0 = S("point"); br = cue("point", "take a break")
    words_in(d, t, [("NOT THEM.", t0 + .3, 300, 150, INK)] if t < br - .1 else [("TAKE A", br - .1, 300, 150, INK), ("BREAK.", br + .1, 450, 150, SIG)])
    phone(d, 330, 820, 2.0, INK, lit=False)
    if t >= br: d.text((330, 820), "zZ", font=F(BLK, 70), fill=MID, anchor="mm")
    picto(d, 700, FLOOR, .9, INK, f=-1, pose=IDLE if t < br else OPEN)
    fig(d, "fig. 2 — close the app, reset the mindset")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "mood": sc_mood, "name": sc_name, "point": sc_point}
FX = [(0.0, thud(.5), 0), *[(i * .45, whoosh(.18, .07), (-.5 if i % 3 else .5)) for i in range(7)], *EP.cut_fx(),
      *[(S("study") + i * .45, whoosh(.18, .06), (.5 if i % 2 else -.5)) for i in range(7)], (S("result") + .05, thud(.5), 0),
      (cue("mood", "satisfied"), pop(.15), -.2), (cue("mood", "pessimistic"), pop(.15), .2), (cue("name", "rejection") - .1, thud(.45), 0),
      (cue("point", "take a break"), riser(.4, .06), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
