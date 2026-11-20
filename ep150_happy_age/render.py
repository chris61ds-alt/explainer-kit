"""NOT JUST YOU – No. 150: the happiness U-curve ('Where do you stand?' + line-race format, ref: ViralCharts, 20.11.2026).
Scottish Health Survey 2016, table 8.7 (life satisfaction 0–10, all adults): 16–24 8.1 · 25–34 7.9 · 35–44 7.7 · 45–54 7.5 ·
55–64 7.6 · 65–74 7.9 · 75+ 7.8 (n = 4,309). Blanchflower (2021): U minimum at ~47–48 across 132 countries.
ONE continuous object: a line that draws itself as AGE runs up (big age counter, live score at the tip), y-axis zoomed to
7.3–8.3. Cold open: the whole U draws in one second, "U" stamp. Dip/rise beats draw it slowly. 'world': dashed marker at 48.
'zoom' (on black): the y-axis zooms out to 0–10 and the U flattens – the honest twist. Payoff (rule 15): flat-ish U on the
full scale + 'YOU?' at 35 + "SMALL DIP. IT LIFTS." Light look."""
import os, sys, math
import numpy as np
from PIL import ImageDraw
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from fx2 import light_look, is_light, stamp
from stand import shadowed, you_marker, dashed
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .5, "setup": .5, "dip": .6, "rise": .6, "world": .6, "zoom": .8, "why": .1})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "setup", "dip", "rise", "world", "zoom", "why", "end"]
EP = ThreadEpisode(TL, 150, "HAPPINESS BY AGE", order=ORDER, dark=True, label="SURVEY · SCOTLAND 2016 · 4,309 ADULTS",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Scottish Health Survey 2016, table 8.7 ·", "Blanchflower (2021), J. of Population Economics"),
                   music=dict(bpm=94, root=2, prog="major", kick="four", audio="v5"),
                   cover=dict(words=["WHEN ARE", "WE LEAST", "HAPPY?"], kicker="Life satisfaction by age."))
light_look(EP, ORDER, reveal=("zoom",))

AGES = [20, 30, 40, 50, 60, 70, 80]; VALS = [8.1, 7.9, 7.7, 7.5, 7.6, 7.9, 7.8]
def val(a):
    """smooth (monotone cubic) interpolation through the band midpoints"""
    a = min(max(a, AGES[0]), AGES[-1]); xs, ys = np.array(AGES, float), np.array(VALS, float)
    i = min(int(np.searchsorted(xs, a, side="right")) - 1, len(xs) - 2); h = xs[i + 1] - xs[i]; u = (a - xs[i]) / h
    m = np.gradient(ys, xs); m0, m1 = m[i] * h, m[i + 1] * h
    return (2 * u ** 3 - 3 * u ** 2 + 1) * ys[i] + (u ** 3 - 2 * u ** 2 + u) * m0 + (-2 * u ** 3 + 3 * u ** 2) * ys[i + 1] + (u ** 3 - u ** 2) * m1
PX0, PX1, PY0, PY1 = 150, 990, 600, 1080                       # plot area
A0, A1 = 18, 82

T_FAST0 = .15; T_FAST1 = cue("hook", "climbs") + .3
T_STAMP = cue("hook", "climbs") - .05
T_LINE0 = cue("setup", "The line") - .1
T_DIP0, T_DIP1 = S("dip") + .05, E("dip")
T_RISE0, T_RISE1 = S("rise") + .05, E("rise") + .3
T_LOW = cue("world", "low point") - .2
T_ZOOM0 = S("zoom") + .1; T_ZOOM1 = T_ZOOM0 + 1.4
T_YOU = S("why") + .3

def yrange(t):
    k = ease_io(clamp((t - T_ZOOM0) / (T_ZOOM1 - T_ZOOM0))) if t >= T_ZOOM0 else 0
    return 7.3 * (1 - k) + 0 * k, 8.3 * (1 - k) + 10 * k

def age_now(t):
    """how far the line is drawn"""
    if t < S("setup"): return A0 + 2 + (AGES[-1] - AGES[0]) * ease_io(clamp((t - T_FAST0) / (T_FAST1 - T_FAST0)))
    if t < T_LINE0: return 20
    if t < T_DIP0: return 20 + 8 * ease_io(clamp((t - T_LINE0) / 1.2))
    if t < T_RISE0: return 28 + 22 * ease_io(clamp((t - T_DIP0) / (T_DIP1 - T_DIP0)))
    return 50 + 30 * ease_io(clamp((t - T_RISE0) / (T_RISE1 - T_RISE0)))

def xy(a, v, t):
    lo, hi = yrange(t)
    return PX0 + (a - A0) / (A1 - A0) * (PX1 - PX0), PY1 - (v - lo) / (hi - lo) * (PY1 - PY0)

def objects(L, d, t):
    cur = EP.current(t); lo, hi = yrange(t)
    d.line([(PX0, PY0 - 20), (PX0, PY1)], fill=INK, width=4); d.line([(PX0, PY1), (PX1 + 20, PY1)], fill=INK, width=4)
    for a in (20, 30, 40, 50, 60, 70, 80):
        x = xy(a, lo, t)[0]; d.line([(x, PY1), (x, PY1 + 12)], fill=INK, width=3)
        d.text((x, PY1 + 36), str(a), font=F(MONO, 24), fill=MID, anchor="mm")
    step = .2 if hi - lo < 2 else 2
    v = math.ceil(lo / step) * step
    while v <= hi + 1e-6:
        y = xy(A0, v, t)[1]; d.line([(PX0 - 12, y), (PX0, y)], fill=INK, width=3)
        d.text((PX0 - 20, y), f"{v:.1f}" if step < 1 else f"{v:.0f}", font=F(MONO, 22), fill=MID, anchor="rm"); v += step
    if t >= T_LOW:                                                    # the 132-country low point
        x = xy(48, lo, t)[0]; dashed(d, (x, PY0 - 10), (x, PY1), SIG, w=4)
        d.text((x, PY0 - 30), "LOW POINT ~48", font=F(BLK, 30), fill=SIG, anchor="mm")
    an = age_now(t)
    if t < S("setup"):                                              # cover / cold open: a faint ghost of the whole U
        d.line([xy(a, val(a), t) for a in np.linspace(20, 80, 120)], fill=RULE, width=7, joint="curve")
    pts = [xy(a, val(a), t) for a in np.linspace(20, max(20.01, an), 120)]
    if len(pts) > 1: d.line(pts, fill=INK, width=9, joint="curve")
    if an > 20.2 and (t < S("setup") or t >= T_LINE0):
        x, y = pts[-1]; d.ellipse([x - 13, y - 13, x + 13, y + 13], fill=SIG)
        d.text((x + 22, y - 4), f"{val(an):.1f}", font=F(BLK, 40), fill=SIG, anchor="lm")
    if cur in ("why", "end"): you_marker(d, *xy(35, val(35), t), t, T_YOU)

def labels(d, t):
    cur = EP.current(t)
    if T_STAMP <= t < S("setup") + .2: stamp(d, (560, 720), "U", t, T_STAMP, size=150)
    if cur in ("why", "end") and t >= T_YOU + .4:
        d.text((PX1, PY1 - 140), "SMALL DIP. IT LIFTS.", font=F(BLK, 44), fill=SIG, anchor="ra")

def head(d, t, line):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    a = age_now(t); cur = EP.current(t)
    d.text((X0, 400), "AGE", font=F(MONO, 30), fill=MID)
    d.text((X0 + 90, 384), f"{a:.0f}" if (t < S("setup") or t >= T_LINE0) else "–", font=F(BLK, 64), fill=INK)
    d.text((X0 + 260, 400), "LIFE SATISFACTION", font=F(MONO, 30), fill=MID)
    d.text((X0 + 600, 384), f"{val(a):.1f}" if (t < S("setup") or t >= T_LINE0) else "–", font=F(BLK, 64), fill=SIG if cur == "dip" else INK)

def draw(img, d, t, line, note="0–10 scale · averages by age group"):
    shadowed(EP, img, t, objects); d = ImageDraw.Draw(img); labels(d, t); head(d, t, line); fig(d, note)

def sc_hook(img, d, t): draw(img, d, t, "HAPPY BY AGE?")
def sc_setup(img, d, t): draw(img, d, t, "RATE YOUR LIFE, 0–10.", note="Scottish Health Survey 2016 · 4,309 adults")
def sc_dip(img, d, t): draw(img, d, t, "DOWN…")
def sc_rise(img, d, t): draw(img, d, t, "…AND BACK UP.")
def sc_world(img, d, t): draw(img, d, t, "132 COUNTRIES.", note="Blanchflower 2021 · minimum at 47–48")
def sc_zoom(img, d, t): draw(img, d, t, "FULL SCALE.", note="same data, axis from 0 to 10")
def sc_why(img, d, t): draw(img, d, t, "RIGHT ON SCHEDULE.", note="averages by age group, not the same people over time")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.scenes = {"hook": sc_hook, "setup": sc_setup, "dip": sc_dip, "rise": sc_rise, "world": sc_world, "zoom": sc_zoom, "why": sc_why}
FX = [(T_FAST0, whoosh(.6, .03), -.4), (T_STAMP, thud(.3), 0), (S("setup"), whoosh(.3, .025), 0), (T_LINE0, pop(.1), -.5),
      *[(T_DIP0 + j * (T_DIP1 - T_DIP0) / 6, tick(.012), -.4 + j * .08) for j in range(6)],
      *[(T_RISE0 + j * (T_RISE1 - T_RISE0) / 6, tick(.012), 0 + j * .08) for j in range(6)],
      (T_LOW, pop(.12), 0), (S("zoom") + .05, thud(.35), 0), (T_ZOOM0, whoosh(.8, .03), 0), (T_YOU, pop(.12), -.3)]
if __name__ == "__main__": EP.run(FX)
