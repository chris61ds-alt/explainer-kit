"""NOT JUST YOU – PILOT "level 2" of No. 124 (Berkson's paradox), 12.11.2026. New storytelling rules under test:
cold open in the picture (the cloud is there from frame 0), ONE continuous object (the scatter plot, no whip cuts),
no pure text scenes, springy/physical motion (rejected dots fall, the trend line swings in), loop ending
(the last line runs into the first, the dots come back). Same simulation and numbers as No. 124."""
import os, sys, math, random, statistics as st
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .34, "setup": .34, "filter": .34, "reveal": .4, "why": .1})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "setup", "filter", "reveal", "why", "end"]
EP = ThreadEpisode(TL, 124, "BERKSON", order=ORDER, dark=True, label="SIMULATION · MATH MODEL",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Berkson (1946), Biometrics Bulletin 2(3) ·", "Ellenberg (2014), How Not to Be Wrong"),
                   music=dict(bpm=100, root=1, prog="tense", kick="four", audio="v5"),
                   cover=dict(words=["YOU THINK", "HOT PEOPLE", "ARE MEAN."], kicker="It's a statistics trick."))

R = random.Random(4); PEOPLE = [(R.random(), R.random()) for _ in range(400)]
KEEP = [p[0] + p[1] > 1.0 for p in PEOPLE]; KS = [p for p, k in zip(PEOPLE, KEEP) if k]
R_ALL = st.correlation([p[0] for p in PEOPLE], [p[1] for p in PEOPLE]); R_KEPT = st.correlation([p[0] for p in KS], [p[1] for p in KS])
MX, MY = st.mean(p[0] for p in KS), st.mean(p[1] for p in KS)
SLOPE = sum((p[0] - MX) * (p[1] - MY) for p in KS) / sum((p[0] - MX) ** 2 for p in KS)
PX0, PX1, PY0, PY1 = X0 + 70, X1 - 10, 520, 1080
def pxy(p): return PX0 + p[0] * (PX1 - PX0), PY1 - p[1] * (PY1 - PY0)
def spring(k, f=2.2, damp=5.0):                             # 0 → 1 with a little overshoot
    k = clamp(k); return 1 - math.exp(-damp * k) * math.cos(f * math.pi * k) if k < 1 else 1.0

T_F = cue("filter", "drop everyone") - .1                    # the filter line sweeps in
T_DROP = cue("filter", "Not hot enough") - .15               # … and the rejected dots fall
T_BACK = cue("why", "And it's why") - .5                     # loop: they come back

def fall(i, t):
    """vertical offset + alpha of a rejected dot (gravity, staggered by distance from the bar); returns on the loop"""
    if t < T_DROP: return 0.0, 1.0
    p = PEOPLE[i]; delay = (1 - (p[0] + p[1])) * .5 + (i % 7) * .02
    if t >= T_BACK:
        k = spring((t - T_BACK - (i % 9) * .012) / .45, f=1.2, damp=6); return (1 - k) * 60, clamp(k * 1.4)
    dt = t - T_DROP - delay
    if dt <= 0: return 0.0, 1.0
    return 900 * dt * dt, clamp(1 - dt / .7)

def plot(d, t):
    cur = EP.current(t)
    d.line([PX0, PY1, PX1, PY1], fill=INK, width=4); d.line([PX0, PY0, PX0, PY1], fill=INK, width=4)
    d.text((PX1, PY1 + 14), "LOOKS →", font=F(MONO, 26), fill=MID, anchor="ra"); d.text((PX0 - 14, PY0), "KIND", font=F(MONO, 26), fill=MID, anchor="ra")
    wave = (t - .05) / .9                                     # cold open: a ripple runs through the cloud
    for i, p in enumerate(PEOPLE):
        x, y = pxy(p); r = 7.0
        if 0 <= wave <= 1.3: r += 5 * max(0, 1 - abs(p[0] - wave) * 6)
        if t >= S("setup") and t < T_F: r += 1.2 * math.sin(t * 5 + i)       # idle shimmer: nothing stands still
        if not KEEP[i]:
            dy, a = fall(i, t)
            if a <= 0.02: continue
            col = mix(BG, MID if T_DROP <= t < T_BACK else INK, a); d.ellipse([x - r, y + dy - r, x + r, y + dy + r], fill=col)
        else: d.ellipse([x - r, y - r, x + r, y + r], fill=INK)
    if T_F <= t < T_BACK + .3:                               # the bar: looks + kindness
        k = spring((t - T_F) / .6, f=1.0, damp=5.5) if t < T_BACK else 1 - clamp((t - T_BACK) / .3)
        a, b = pxy((0, 1)), pxy((1, 0)); d.line([a, (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k)], fill=MID, width=6)
    if S("reveal") <= t < T_BACK:                            # the trend line swings from flat into its slope
        k = spring((t - S("reveal") - .15) / .8)
        b = SLOPE * k; a0 = MY - b * MX; d.line([pxy((.05, a0 + b * .05)), pxy((1.0, a0 + b * 1.0))], fill=SIG if cur == "reveal" else INK, width=10)

def link_value(t):
    if t < T_DROP + .4: return R_ALL
    if t >= T_BACK: return R_ALL + (R_KEPT - R_ALL) * (1 - clamp((t - T_BACK) / .4))
    return R_ALL + (R_KEPT - R_ALL) * ease_io(clamp((t - T_DROP - .4) / 1.1))

def head(d, t, line, col=INK, sub=None):
    d.text((X0, 300), line, font=F(BLK, 84), fill=col)
    v = link_value(t); d.text((X0, 400), "LINK", font=F(MONO, 30), fill=MID); d.text((X0 + 110, 388), f"{v:+.2f}", font=F(BLK, 64), fill=SIG if abs(v) > .3 else INK)
    if sub: d.text((X1, 408), sub, font=F(MONO, 26), fill=MID, anchor="ra")

def sc_hook(img, d, t): head(d, t, "HOT = MEAN?"); plot(d, t); fig(d, "simulation")
def sc_setup(img, d, t): head(d, t, "400 PEOPLE, RANDOM", sub="no link"); plot(d, t); fig(d, "looks and kindness independent")
def sc_filter(img, d, t):
    n = 400 if t < T_DROP else max(209, 400 - int(clamp((t - T_DROP) / 1.0) * 191))
    head(d, t, "YOUR FILTER", sub=f"{n} left"); plot(d, t); fig(d, "attractive enough, kind enough, or both")
def sc_reveal(img, d, t): head(d, t, "HOTTER = MEANER", sub="209 left"); plot(d, t); fig(d, "among the ones you date · simulation")
def sc_why(img, d, t):
    head(d, t, "NOBODY CHANGED." if t < cue("why", "Berkson") - .1 else ("BERKSON'S PARADOX" if t < T_BACK else "HOT = MEAN?"), sub=None if t >= T_BACK else "your filter did"); plot(d, t)
    fig(d, "a filter, not a law")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.bg = {"hook": "dark", "setup": "dark", "filter": "dark", "reveal": "orange", "why": "dark"}
EP.scenes = {"hook": sc_hook, "setup": sc_setup, "filter": sc_filter, "reveal": sc_reveal, "why": sc_why}
FX = [(.05, whoosh(.8, .05), 0), (S("setup") + .1, pop(.1), 0),
      (T_F, whoosh(.5, .05), -.2), *[(T_DROP + i * .06, tick(.03), (i % 5 - 2) / 3) for i in range(14)],
      (S("reveal") + .1, thud(.55), 0), (S("reveal") + .5, pop(.14), .2),
      (cue("why", "Berkson") - .1, pop(.13), 0), (T_BACK, whoosh(.45, .05), 0)]
if __name__ == "__main__": EP.run(FX)
