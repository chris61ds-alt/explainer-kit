"""NOT JUST YOU · AFTER DARK – No. 42: once a week is enough (Muise, Schimmack & Impett 2016)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .8, "result": .5, "flat": .5, "single": .5, "caveat": .5, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "flat", "single", "caveat", "point", "end"]
EP = Episode(TL, 42, "ONCE A WEEK", order=ORDER, dark=True, series="NOT JUST YOU · AFTER DARK",
             chapters={"hook": "MORE?", "study": "THE DATA", "result": "THE CURVE", "flat": "THE PLATEAU", "single": "SINGLES", "caveat": "THE CAVEAT", "point": "STOP COUNTING"},
             sources=("Muise, Schimmack & Impett (2016), Social", "Psychological and Personality Science 7(4)"),
             music=dict(bpm=92, root=2, prog="warm", kick="half", gaps=[(E("study") + .05, S("result") + .05)]),
             cover=dict(words=["ONCE", "A WEEK."], kicker="Intimacy, by the numbers."))

def heart(d, cx, cy, r, col=SIG):
    d.ellipse([cx - r, cy - r * .9, cx, cy + r * .1], fill=col); d.ellipse([cx, cy - r * .9, cx + r, cy + r * .1], fill=col)
    d.polygon([(cx - r * .98, cy - r * .3), (cx + r * .98, cy - r * .3), (cx, cy + r * .95)], fill=col)

OX, OY, GW, GH = X0 + 50, 1060, X1 - X0 - 70, 440
LABS = ["never", "monthly", "2–3× month", "weekly", "2–3× week", "4+ week"]
def axes(d):
    d.line([OX, OY, OX + GW, OY], fill=INK, width=4); d.line([OX, OY, OX, OY - GH], fill=INK, width=4)
    for i, lab in enumerate(LABS):
        x = OX + GW * (i + .5) / 6; d.line([x, OY, x, OY + 10], fill=INK, width=3); d.text((x, OY + 18), lab, font=F(MONO, 16), fill=MID, anchor="ma")
    d.text((OX + 10, OY - GH - 10), "well-being", font=F(COND, 26), fill=INK, anchor="ld")
def pts_for(vals): return [(OX + GW * (i + .5) / 6, OY - GH * v) for i, v in enumerate(vals)]
COUPLE = [.3, .45, .58, .74, .74, .75]

def sc_hook(img, d, t):
    d.text((X0 - 6, 300), "MORE =", font=F(BLK, 190), fill=INK); d.text((X0 - 6, 490), "HAPPIER?", font=F(BLK, 160), fill=SIG)
    picto(d, 370, FLOOR, .95, INK, f=1, pose=IDLE); picto(d, 590, FLOOR, .95, SIG, f=-1, pose=IDLE)
    heart(d, 480, 760 - 10 * math.sin(t * 4), 40 + 6 * math.sin(t * 6))
    fig(d, "fig. 1 — a couple, wondering")

def sc_study(img, d, t):
    t0 = S("study")
    counter(d, X0, 300, t, t0 + .1, 1.2, 30000, "{:,.0f}+", 190, SIG)
    d.text((X0 + 6, 520), "Americans, three studies", font=F(COND, 36), fill=INK)
    for i in range(40):
        r, c = divmod(i, 10); k = ease((t - t0 - i * .02) / .3)
        if k > 0: picto(d, X0 + 40 + c * 86, 700 + r * 120, .26, MID if i % 4 else SIG, pose=IDLE)
    fig(d, "national surveys incl. 2,400 married couples · Muise et al., 2016")

def sc_result(img, d, t):
    t0 = S("result")
    d.text((X0, 300), "COUPLES", font=F(BLK, 150), fill=INK)
    axes(d); P = pts_for(COUPLE); k = clamp((t - t0) / 2.4); n = max(2, int(1 + 3 * k + .5))
    d.line(P[:min(4, n + 1)], fill=SIG, width=8)
    for x, y in P[:min(4, n + 1)]: heart(d, x, y, 16)
    if t >= cue("result", "once a week"):
        box_label(d, P[3][0], P[3][1] - 70, "≈ ONCE A WEEK", 26, WHITE, SIG, anchor="ma")
    d.text((X1, 1146), "schematic", font=F(MED, 22), fill=MID, anchor="ra")

def sc_flat(img, d, t):
    t0 = S("flat")
    d.text((X0, 300), "THEN: FLAT.", font=F(BLK, 150), fill=SIG)
    axes(d); P = pts_for(COUPLE); k = clamp((t - t0) / 1.2)
    d.line(P[:4], fill=SIG, width=8); d.line([P[3], (lerp(P[3][0], P[5][0], k), lerp(P[3][1], P[5][1], k))], fill=INK, width=8)
    for x, y in P[:4]: heart(d, x, y, 16)
    if k > .9: dim_h(d, P[3][0], P[5][0], P[3][1] - 40, 1, INK, None); box_label(d, (P[3][0] + P[5][0]) / 2, P[3][1] - 110, "NO EXTRA GAIN", 24, WHITE, INK, anchor="ma")
    d.text((X1, 1146), "schematic", font=F(MED, 22), fill=MID, anchor="ra")

def sc_single(img, d, t):
    t0 = S("single")
    d.text((X0, 300), "SINGLES", font=F(BLK, 150), fill=INK)
    axes(d); k = clamp((t - t0) / 1.2)
    d.line([pts_for([.5] * 6)[0], (lerp(pts_for([.5] * 6)[0][0], pts_for([.5] * 6)[5][0], k), OY - GH * .5)], fill=MID, width=8)
    if k > .9: box_label(d, X1 - 20, OY - GH * .5 - 70, "NO LINK", 28, WHITE, INK, anchor="ra")
    d.text((X1, 1146), "schematic", font=F(MED, 22), fill=MID, anchor="ra")

def sc_caveat(img, d, t):
    t0 = S("caveat")
    d.text((X0, 300), "CHICKEN", font=F(BLK, 150), fill=INK); d.text((X0, 460), "OR EGG?", font=F(BLK, 150), fill=SIG)
    for i, (lab, y) in enumerate((("more intimacy", 760), ("happier couple", 960))):
        box_label(d, 480, y, lab, 40, WHITE, INK if i == 0 else SIG, anchor="ma")
    a = t * 2
    d.arc([620, 780, 820, 1000], -80 + math.degrees(a) % 30, 80, fill=INK, width=6); d.arc([140, 780, 340, 1000], 100, 260, fill=SIG, width=6)
    fig(d, "correlation, not proof of cause")

def sc_point(img, d, t):
    t0 = S("point"); cn = cue("point", "connected")
    words_in(d, t, [("STOP", t0, 300, 190, INK), ("COUNTING.", t0 + .2, 490, 150, SIG)])
    picto(d, 400, FLOOR, .95, INK, f=1, pose={"arms": ((70, 20), (-10, -5))}); picto(d, 560, FLOOR, .95, SIG, f=-1, pose={"arms": ((70, 20), (-10, -5))})
    if t >= cn: heart(d, 480, 760, 44 * back((t - cn) / .4))
    fig(d, "fig. 2 — connection over numbers")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "flat": sc_flat, "single": sc_single, "caveat": sc_caveat, "point": sc_point}
FX = [(0.0, thud(.5), 0), *EP.cut_fx(), *[(S("study") + i * .1, tick(.04), (i % 5 - 2) / 3) for i in range(12)],
      (S("result") + .05, thud(.5), 0), *[(S("result") + .6 * i, pop(.12), (i - 1.5) / 2) for i in range(4)], (cue("result", "once a week"), thud(.35), 0),
      (S("flat") + .2, whoosh(.8, .08), 0), (S("single") + .2, whoosh(.8, .06), 0), (cue("point", "connected"), riser(.4, .06), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
