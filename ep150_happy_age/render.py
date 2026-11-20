"""NOT JUST YOU – No. 150 2.0: happiness by age, in the style of the viral 'ViralCharts' line charts (Chris, 20.11.2026:
"keep to the kind of animation that works online"). One continuous self-drawing line, NO cuts/stamps/boxes:
dark background, glowing line, the x-axis grows with the age, the y-axis continuously re-fits to the values seen so far
(so the line always fills the frame), the current value rides on the tip, an age counter. The line is synced to the voice.
Scottish Health Survey 2016, table 8.7 (life satisfaction 0–10): 16–24 8.1 · 25–34 7.9 · 35–44 7.7 · 45–54 7.5 · 55–64 7.6 ·
65–74 7.9 · 75+ 7.8. Blanchflower (2021): minimum ~47–48 in 132 countries -> a quiet dashed marker in the 'world' beat.
Payoff (rule 15): the full curve with the low point marked stays to the last frame. Old version: render_v1.py / script_v1.json."""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from stand import dashed
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .4, "setup": .4, "dip": .5, "rise": .5, "world": .6, "why": .1})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "setup", "dip", "rise", "world", "why", "end"]
EP = ThreadEpisode(TL, 150, "HAPPINESS BY AGE", order=ORDER, dark=True, label="SURVEY · SCOTLAND 2016 · 4,309 ADULTS",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Scottish Health Survey 2016, table 8.7 ·", "Blanchflower (2021), J. of Population Economics"),
                   music=dict(bpm=94, root=2, prog="major", kick="four", audio="v5"),
                   cover=dict(words=["LIFE", "SATISFACTION", "BY AGE"], kicker="When are we least happy?"))

AGES = [20, 30, 40, 50, 60, 70, 80]; VALS = [8.1, 7.9, 7.7, 7.5, 7.6, 7.9, 7.8]
def val(a):
    a = min(max(a, AGES[0]), AGES[-1]); xs, ys = np.array(AGES, float), np.array(VALS, float)
    i = min(int(np.searchsorted(xs, a, side="right")) - 1, len(xs) - 2); h = xs[i + 1] - xs[i]; u = (a - xs[i]) / h
    dl = np.diff(ys) / np.diff(xs); m = np.zeros_like(ys)                        # monotone (Fritsch–Carlson): no fake bumps
    m[0], m[-1] = dl[0], dl[-1]
    for j in range(1, len(ys) - 1): m[j] = 0 if dl[j - 1] * dl[j] <= 0 else 2 / (1 / dl[j - 1] + 1 / dl[j])
    m0, m1 = m[i] * h, m[i + 1] * h
    return (2 * u ** 3 - 3 * u ** 2 + 1) * ys[i] + (u ** 3 - 2 * u ** 2 + u) * m0 + (-2 * u ** 3 + 3 * u ** 2) * ys[i + 1] + (u ** 3 - u ** 2) * m1
A_START = 20.0
PX0, PX1, PY0, PY1 = 170, 840, 640, 1090                        # plot area (leaves room right for the tip label)

# the line is synced to the voice: (time, age)
KEYS = [(.25, 20.6), (E("setup"), 23), (cue("dip", "around fifty") + .6, 50), (E("rise"), 69), (E("world") - .2, 80)]
def age_at(t):
    if t <= KEYS[0][0]: return A_START + .6 * clamp(t / KEYS[0][0])
    for (t0, a0), (t1, a1) in zip(KEYS, KEYS[1:]):
        if t <= t1: return a0 + (a1 - a0) * clamp((t - t0) / max(.01, t1 - t0))
    return KEYS[-1][1]

def nice(span):
    for s in (.05, .1, .2, .25, .5, 1, 2, 5, 10):
        if span / s <= 6: return s
    return 10

def ranges(t):
    """x grows with the age; y fits min..max of the values drawn so far (with padding), eased so it never jumps"""
    a = age_at(t); xs = np.linspace(A_START, max(A_START + .01, a), 80); vs = [val(x) for x in xs]
    x1 = max(A_START + 2, a + 1.0)
    lo, hi = min(vs), max(vs)
    if hi - lo < .15: c = (hi + lo) / 2; lo, hi = c - .075, c + .075
    pad = (hi - lo) * .18
    return (A_START, x1), (lo - pad, hi + pad)

def P(a, v, xr, yr): return PX0 + (a - xr[0]) / (xr[1] - xr[0]) * (PX1 - PX0), PY1 - (v - yr[0]) / (yr[1] - yr[0]) * (PY1 - PY0)

def glow_line(img, pts, col, w):
    """a soft glow under the line (the look of the reference)"""
    if len(pts) < 2: return
    L = Image.new("L", img.size, 0); ImageDraw.Draw(L).line(pts, fill=255, width=w * 4, joint="curve")
    m = np.asarray(L.filter(ImageFilter.GaussianBlur(14)), np.float32)[..., None] / 255 * .55
    base = np.asarray(img, np.float32)
    img.paste(Image.fromarray(np.clip(base * (1 - m) + np.array(col, np.float32) * m, 0, 255).astype(np.uint8)))

def scene(img, t):
    d = ImageDraw.Draw(img); a = age_at(t); xr, yr = ranges(t); cur = EP.current(t)
    d.text((540, 520), "Life Satisfaction by Age", font=F(BLK, 52), fill=INK, anchor="mm")
    d.text((PX0 - 10, PY0 - 40), "Score (0–10)", font=F(MONO, 26), fill=MID, anchor="lm")
    d.line([(PX0, PY0 - 10), (PX0, PY1)], fill=MID, width=3); d.line([(PX0, PY1), (PX1 + 40, PY1)], fill=MID, width=3)
    st = nice(yr[1] - yr[0]); v = math.ceil(yr[0] / st) * st
    while v <= yr[1]:
        y = P(xr[0], v, xr, yr)[1]; d.line([(PX0 - 12, y), (PX0, y)], fill=MID, width=3)
        d.text((PX0 - 22, y), f"{v:.2f}", font=F(MONO, 26), fill=MID, anchor="rm"); v += st
    sx = 2 if xr[1] - xr[0] < 12 else 5 if xr[1] - xr[0] < 30 else 10
    x = math.ceil(xr[0] / sx) * sx
    while x <= xr[1] + 1e-6:
        px = P(x, yr[0], xr, yr)[0]; d.line([(px, PY1), (px, PY1 + 12)], fill=MID, width=3)
        d.text((px, PY1 + 40), f"{x:.0f}", font=F(MONO, 26), fill=MID, anchor="mm"); x += sx
    d.text((PX1 + 40, PY1 + 80), "Age", font=F(MONO, 28), fill=MID, anchor="rm")
    if cur in ("world", "why", "end") and t >= cue("world", "low point") - .2:          # quiet marker: 132-country low point
        k = ease(clamp((t - cue("world", "low point") + .2) / .5)); px = P(48, yr[0], xr, yr)[0]
        dashed(d, (px, PY1), (px, PY1 - (PY1 - PY0) * k), MID, w=3)
        if k > .6: d.text((px, PY0 - 4), "low point ~48 (132 countries)", font=F(MONO, 24), fill=MID, anchor="mm")
    pts = [P(x, val(x), xr, yr) for x in np.linspace(A_START, max(A_START + .01, a), 160)]
    glow_line(img, pts, SIG, 6); d = ImageDraw.Draw(img)
    if len(pts) > 1: d.line(pts, fill=SIG, width=7, joint="curve")
    tx, ty = pts[-1]; d.ellipse([tx - 13, ty - 13, tx + 13, ty + 13], fill=SIG)
    d.text((tx + 24, ty), "Score", font=F(MONO, 26), fill=SIG, anchor="lm")
    d.text((tx + 124, ty), f"{val(a):.2f}", font=F(BLK, 34), fill=INK, anchor="lm")
    d.text((1010, 600), "Age", font=F(MONO, 26), fill=MID, anchor="rm")                    # age counter
    d.text((1010, 650), f"{a:.0f}", font=F(BLK, 72), fill=INK, anchor="rm")

def sc_all(img, d, t): scene(img, t); fig(ImageDraw.Draw(img), "averages by age group · not the same people over time")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.scenes = {k: sc_all for k in ORDER[:-1]}
FX = [(.25, whoosh(.5, .02), -.3), *[(cue("world", "low point") - .2, pop(.08), 0)]]
if __name__ == "__main__": EP.run(FX)
