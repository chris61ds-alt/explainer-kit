"""NOT JUST YOU – No. 112: mismatched sex drive – about 80 % recalled a recent mismatch; communal motivation (caring about the
partner's needs, freely) went with more satisfaction for both (Day, Muise, Joel & Impett 2015, PSPB, 3 studies incl. a
21-day couples diary). Look C+D · statement opener with "you" · isometric bed with two desire gauges · orange: caring."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"common": .6, "diary": .5, "care": .6, "pressure": .5, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["common", "diary", "care", "pressure", "point", "end"]
EP = ThreadEpisode(TL, 112, "DESIRE GAP", order=ORDER, dark=True, label="3 STUDIES · ONE LAB",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Day, Muise, Joel & Impett (2015), To do it or not to do it?", "Personality and Social Psychology Bulletin 41(6)"),
                   music=dict(bpm=96, root=-1, prog="dream", kick="four", audio="v5", gaps=[(E("common") + .05, S("diary") + .05)]),
                   cover=dict(words=["YOU WANT IT", "MORE THAN", "YOUR PARTNER."], kicker="Or less. Here's what helps."))

def sc_common(img, d, t):
    t0 = S("common")
    counter(d, X0, 320, t, t0 + .1, .8, 80, "{:.0f} %", 230, INK)
    d.text((X0 + 6, 565), "remembered a recent mismatch", font=F(COND, 46), fill=INK)
    dot_field(d, (X0 + 14, 680, X1, 1110), t, cell=42, col=MID, hit=set(range(0, 200, 5)) | set(range(1, 200, 5)) | set(range(2, 200, 5)) | set(range(3, 200, 5)), hitcol=INK)
    fig(d, "4 of 5 · schematic")

I = Iso(560, 1040, .52)
def gauges(I, d, t, a, b, col_a=INK, col_b=MID):
    """two desire gauges above the pillows: cylinders of different height"""
    A = {"l": (-125, -180, 160), "r": (105, -180, 160)}
    for (side, v, col) in (("l", a, col_a), ("r", b, col_b)):
        x, y, z = A[side]; h = max(8, 260 * v)
        I.cyl(d, x, y - 120, z + 40, 30, h, top=TOP, side=LEFT)
        px, py = I.P(x, y - 120, z + 40 + h); d.ellipse([px - 14, py - 14, px + 14, py + 14], fill=col)

def sc_diary(img, d, t):
    t0, tr = S("diary"), cue("diary", "Every day") - .1
    counter(d, X0, 320, t, t0 + .1, .6, 21, "{:.0f} DAYS", 170, INK)
    d.text((X0 + 6, 520), "couples, every day: how much desire?", font=F(COND, 44), fill=INK)
    I.grid(img); I.shadow(d, 0, 0, 240)
    A = bed(I, d, t, T=[t0 + .05 + i * .06 for i in range(7)])
    if t >= tr:
        day = (t - tr) * 2.2                                 # the two gauges wander, rarely in sync
        a = .55 + .35 * math.sin(day * 1.7); b = .45 + .35 * math.sin(day * 1.1 + 2.2)
        gauges(I, d, t, clamp(a), clamp(b))
        p = I.P(-125, -300, 200); d.text((p[0] - 95, p[1] - 40), "YOU", font=F(MONO, 26), fill=INK, anchor="rm")
        p = I.P(105, -300, 200); d.text((p[0] + 60, p[1] - 40), "PARTNER", font=F(MONO, 26), fill=MID, anchor="lm")
    fig(d, "21-day diary · schematic")

def sc_care(img, d, t):
    t0, to, th = S("care"), cue("care", "were more open") - .1, cue("care", "both partners") - .1
    words_in(d, t, [("CARING", t0 + .05, 320, 170, SIG), ("ABOUT EACH", t0 + .2, 500, 110, INK), ("OTHER'S NEEDS.", t0 + .3, 610, 110, INK)])
    if t >= to: box_label(d, X0 + 4 - (1 - ease((t - to) / .2)) * 40, 780, "MORE OPEN, EVEN WITHOUT THE MOOD", 38, WHITE, INK, font=BLK)
    if t >= th:
        k = back(clamp((t - th) / .35))
        heart(d, X0 + 110, 1000, 70 * k, SIG); heart(d, X0 + 290, 1000, 70 * k, SIG)
        d.text((X0 + 420, 1000), "BOTH HAPPIER", font=F(BLK, 60), fill=INK, anchor="lm")
    fig(d, "a link, not proof")

def sc_pressure(img, d, t):
    t0, tp, tn = S("pressure"), cue("pressure", "Out of guilt") - .1, cue("pressure", "a no gets") - .1
    words_in(d, t, [("ONLY WHEN", t0 + .05, 320, 140, INK), ("IT'S FREE.", t0 + .2, 470, 140, INK)])
    if t >= tp:
        box_label(d, X0 + 4, 680, "GUILT", 64, WHITE, MID, font=BLK); box_label(d, X0 + 280, 680, "PRESSURE", 64, WHITE, MID, font=BLK)
        k = ease((t - tp - .25) / .25)
        if k > 0: d.line([X0 - 10, 712, X0 - 10 + 700 * k, 712], fill=INK, width=12)
    if t >= tn: words_in(d, t, [("A NO IS OK.", tn, 860, 130, INK)])
    fig(d, "consent first, always")

def sc_point(img, d, t):
    t0, tc = S("point"), cue("point", "It's about caring") - .2
    words_in(d, t, [("NOT ABOUT", t0 + .05, 320, 140, MID), ("WHO'S RIGHT.", t0 + .2, 470, 140, MID)] + ([("CARING.", tc, 640, 170, SIG), ("BOTH WAYS.", tc + .5, 820, 130, SIG)] if t >= tc else []))
    fig(d, "fig. 2 — both ways")

EP.cuts = {"pressure": "stay"}
EP.bg = {"diary": "light"}
EP.scenes = {"common": sc_common, "diary": sc_diary, "care": sc_care, "pressure": sc_pressure, "point": sc_point}
FX = [*EP.cut_fx(), (S("common") + .1, riser(.8, .04), 0), (S("common") + .9, thud(.45), 0),
      (S("diary") + .1, tick(.05), 0), *[(S("diary") + .05 + i * .06, tick(.03), (i - 3) / 4) for i in range(7)], (cue("diary", "Every day") - .1, pop(.13), -.2), (cue("diary", "Every day") + .1, pop(.13), .2),
      (S("care") + .1, thud(.55), 0), (cue("care", "were more open") - .1, pop(.13), -.2), (cue("care", "both partners") - .1, pop(.15), 0),
      (S("pressure") + .1, thud(.4), 0), (cue("pressure", "Out of guilt") - .1, pop(.12), -.2), (cue("pressure", "Out of guilt") + .25, whoosh(.25, .05), 0), (cue("pressure", "a no gets") - .1, thud(.45), 0),
      (S("point") + .1, pop(.12), 0), (cue("point", "It's about caring") - .2, thud(.5), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
