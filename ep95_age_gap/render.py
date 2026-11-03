"""NOT JUST YOU – No. 95 (Wedding Math 3/3): bigger age gap, higher divorce risk (Francis-Tan & Mialon 2014/15). Look C+D, dark."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from thread import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .6, "one": .5, "five": .5, "ten": .5, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "one", "five", "ten", "point", "end"]      # opener: direct question to the viewer ("QUICK QUESTION", toolkit)
EP = ThreadEpisode(TL, 95, "AGE GAP", order=ORDER, dark=True, label="WEDDING MATH 3/3 · SURVEY",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Francis-Tan & Mialon (2015), Economic Inquiry", "survey of 3,000+ ever-married US adults · correlation"),
                   music=dict(bpm=92, root=-5, prog="dream", kick="half", audio="v5", gaps=[(E("study") + .05, S("one") + .05)]),
                   cover=dict(words=["10 YEARS APART:", "+39 %", "DIVORCE RISK."], kicker="Wedding Math, part 3 of 3."))

def pair(img, cy, sep, s=.22, col=INK, k=1.0):
    for x in (480 - sep / 2, 480 + sep / 2):
        silhouette(img, lambda m, x=x: front_bust(m, x, cy, s, 255), (int(x - 110 * s / .22), int(cy - 76 * s / .22), int(x + 110 * s / .22), int(cy + 110 * s / .22)), col, cell=6, k=k)

def sc_hook(img, d, t):
    t0, tr = S("hook"), cue("hook", "bigger the divorce") - .1
    d.text((X0 - 4, 320), "BIGGER GAP,", font=F(BLK, 150), fill=INK)
    if t >= tr: k = ease((t - tr) / .25); d.text((X0 - 4 - (1 - k) * 60, 480), "BIGGER RISK.", font=F(BLK, 140), fill=mix(BG, SIG, k))
    sep = 240 + 360 * ease_io(clamp((t - t0) / 1.8))
    pair(img, 900, sep, .3)
    d.line([480 - sep / 2 + 90, 1100, 480 + sep / 2 - 90, 1100], fill=MID, width=6)
    fig(d, "fig. 1 — the gap between you, schematic")

def sc_study(img, d, t):
    t0, tc = S("study"), cue("study", "Compared to couples") - .1
    counter(d, X0, 320, t, t0 + .1, .8, 3000, "{:,.0f}+", 230, INK)
    d.text((X0 + 6, 570), "married Americans · same survey as parts 1 + 2", font=F(COND, 40), fill=INK)
    if t >= tc:
        box_label(d, X0 + 4 - (1 - ease((t - tc) / .2)) * 50, 640, "BASELINE: SAME AGE", 44, WHITE, INK, font=BLK)
        pair(img, 900, 240, .3)
    else: dot_field(d, (X0 + 14, 760, X1, 1110), t, cell=30, col=MID, hit={44, 45}, hitcol=INK)
    fig(d, "risk compared with same-aged couples")

ROWS = [("1 YEAR", 3, "one", "Three percent"), ("5 YEARS", 18, "five", "Eighteen"), ("10 YEARS", 39, "ten", None)]
def gap_at(t):
    yrs = 0.0
    for lab, v, b, _ in ROWS:
        if t >= S(b): yrs = lerp(yrs, float(lab.split()[0]), ease_io((t - S(b)) / .5))
    return yrs

def sc_chart(img, d, t):
    d.text((X0, 320), "AGE GAP", font=F(BLK, 150), fill=INK)
    yrs = gap_at(t); sep = 220 + yrs * 40
    pair(img, 590, sep)
    d.text((480, 600), f"{yrs:.0f} Y", font=F(BLK, 52), fill=INK, anchor="mm")
    for j, (lab, v, b, say) in enumerate(ROWS):
        tk = (cue(b, say) - .1) if say else S(b) + .15
        if t < tk - .01: continue
        k = ease((t - tk) / .5); y = 740 + j * 140; col = SIG if b == "ten" else (INK if TL.current(t) == b else MID)
        d.text((X0, y), lab, font=F(BLK, 42), fill=col)
        w = 600 * v / 39 * k; d.rectangle([X0, y + 50, X0 + max(6, w), y + 120], fill=col)
        d.text((X0 + max(6, w) + 16, y + 85), f"+{v * k:.0f} %", font=F(BLK, 56), fill=col, anchor="lm")
    fig(d, "more likely to divorce than same-aged couples")

def heart(m, cx, cy, r):
    m.ellipse([cx - r, cy - r * .9, cx, cy + r * .1], fill=255); m.ellipse([cx, cy - r * .9, cx + r, cy + r * .1], fill=255)
    m.polygon([(cx - r * .97, cy - r * .25), (cx + r * .97, cy - r * .25), (cx, cy + r * 1.05)], fill=255)

def sc_point(img, d, t):
    t0, ts = S("point"), cue("point", "But statistics") - .2
    words_in(d, t, [("LOVE:", t0 + .1, 320, 130, MID), ("NO AGE.", t0 + .25, 445, 130, INK)] +
             ([("STATISTICS:", ts, 600, 120, SIG), ("YES.", ts + .15, 715, 120, SIG)] if t >= ts else []))
    silhouette(img, lambda m: heart(m, X1 - 160, 930, 120), (X1 - 290, 790, X1 - 30, 1070), INK, cell=10, k=clamp((t - t0) / .6))
    fig(d, "fig. 2 — Wedding Math, part 3 of 3")

# magic move: the same-age couple from the study walks up into the chart
EP.carry = {"one": [((150, 820, 810, 1110), (150, 510, 810, 700))]}
EP.cuts = {"five": "stay", "ten": "stay"}

EP.scenes = {"hook": sc_hook, "study": sc_study, "one": sc_chart, "five": sc_chart, "ten": sc_chart, "point": sc_point}
FX = [*EP.cut_fx(), (S("hook") + .1, whoosh(.5, .04), 0), (cue("hook", "bigger the divorce") - .1, thud(.5), 0),
      (S("study") + .1, riser(.8, .04), 0), (cue("study", "Compared to couples") - .1, pop(.13), 0),
      (S("one") + .1, whoosh(.3, .04), 0), (cue("one", "Three percent") - .1, pop(.14), -.2),
      (S("five") + .1, whoosh(.3, .04), 0), (cue("five", "Eighteen") - .1, thud(.45), 0),
      (S("ten") + .05, whoosh(.3, .05), 0), (S("ten") + .15, thud(.55), 0),
      (S("point") + .1, pop(.12), 0), (cue("point", "But statistics") - .2, thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
