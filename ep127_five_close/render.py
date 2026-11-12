"""NOT JUST YOU – No. 127: Dunbar's circles – call records of ~35 million people show layers of about 4 / 11 / 30 / 129
(MacCarron, Kaski & Dunbar 2016; classic 5 / 15 / 50 / 150: Zhou et al. 2005).
Level 2 + fx2: top-down circles around YOU, there from frame 0; calls fly out as PARTICLES (inner people get called most),
the CAMERA pulls out ring by ring as the counter grows, then pushes back in on the inner four, who GLOW; orange reveal, loop."""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from fx2 import camera, cam_path, glow, dots
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .34, "setup": .34, "layers": .34, "reveal": .4, "why": .1})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "setup", "layers", "reveal", "why", "end"]
EP = ThreadEpisode(TL, 127, "FIVE CLOSE", order=ORDER, dark=True, label="CALL RECORDS · 35 MILLION PEOPLE",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("MacCarron, Kaski & Dunbar (2016), Calling Dunbar's", "numbers, Social Networks 47 · Zhou et al. (2005)"),
                   music=dict(bpm=96, root=-2, prog="dream", kick="four", audio="v5"),
                   cover=dict(words=["YOU ONLY HAVE", "ROOM FOR", "ABOUT 4."], kicker="Close people. The circles, from 6 billion calls."))

C = (540, 830)
RAD = [95, 175, 255, 335]; SIZES = [4, 11, 30, 129]
R = np.random.RandomState(7); PEOPLE = []                    # (x, y, ring)
for k, n in enumerate(SIZES):
    r0 = 40 if k == 0 else RAD[k - 1] + 14; m = n - (SIZES[k - 1] if k else 0)
    for j in range(m):
        a = (j + R.rand() * .6) / m * 2 * math.pi + k * .7; rr = r0 + (RAD[k] - 14 - r0) * (.5 if k == 0 else R.rand())
        PEOPLE.append((C[0] + rr * math.cos(a), C[1] + rr * math.sin(a), k))
PH = R.rand(len(PEOPLE)) * 10
PERIOD = [.9, 1.8, 3.6, 7.0]

T_L = [cue("layers", w) - .1 for w in ("About four", "Then eleven", "Then thirty", "Then about")]
T_BACK = cue("why", "That's why") - .35

def shown(t):
    """how many rings are visible"""
    if t >= T_BACK + .3: return 1
    if t < T_L[1]: return 1
    return 1 + sum(1 for x in T_L[1:] if t >= x)

def count(t):
    if t < T_L[0] or t >= T_BACK: return None
    k = shown(t) - 1; tk = T_L[k] if k else T_L[0]; prev = SIZES[k - 1] if k else 0
    return prev + (SIZES[k] - prev) * ease(clamp((t - tk) / .5))

def scene(L, d, t):
    rings = shown(t); back = clamp((t - T_BACK) / .3) if t >= T_BACK else 0
    for k in range(4):                                        # the circles
        if k < rings or (k < 4 and back < 1 and t >= T_BACK and k < shown(T_BACK - .01)):
            tk = 0 if k == 0 else T_L[k]; s = spring((t - tk) / .6) if k else 1
            if k and t >= T_BACK: s *= 1 - back
            if s <= 0: continue
            r = RAD[k] * s; d.ellipse([C[0] - r, C[1] - r, C[0] + r, C[1] + r], outline=MID, width=3)
            if s > .8: d.text((C[0], C[1] - r - 26), f"{SIZES[k]}", font=F(BLK, 34), fill=MID, anchor="mm")
    pts, inner = [], []
    for j, (x, y, k) in enumerate(PEOPLE):
        vis = k < rings or (t >= T_BACK and k < shown(T_BACK - .01) and back < 1)
        if not vis: continue
        tk = 0 if k == 0 else T_L[k]; s = spring((t - tk - (j % 17) * .015) / .4) if k else 1
        if k and t >= T_BACK: s *= 1 - back
        px, py = C[0] + (x - C[0]) * s, C[1] + (y - C[1]) * s
        wave = (t - .05) / .8; rad = 9 if k == 0 else 6
        if k == 0 and 0 <= wave <= 1.4: rad += 6 * max(0, 1 - abs(j / 3 - wave) * 3)          # cold open ripple
        if k == 0 and S("reveal") <= t: rad += 6 * spring((t - S("reveal") - .2) / .5) * (1 - back)       # the inner four grow
        d.ellipse([px - rad, py - rad, px + rad, py + rad], fill=INK if k == 0 else MID)
        if k == 0: inner.append(("c", px, py, rad + 4))
        if S("setup") - .1 <= t < T_BACK:                     # calls: a pulse flies from you to them
            u = ((t + PH[j]) % PERIOD[k]) / .45
            for q in range(8):                                # a short streak: head + tail
                uq = u - q * .035
                if 0 <= uq < 1: pts.append((C[0] + (px - C[0]) * uq, C[1] + (py - C[1]) * uq))
    if pts:
        P = np.array(pts); jit = np.random.RandomState(int(t * 30)).randn(len(P) * 6, 2) * 3
        dots(L, np.repeat(P, 6, 0) + jit, INK, size=4)
    d.ellipse([C[0] - 20, C[1] - 20, C[0] + 20, C[1] + 20], fill=INK)
    d.text((C[0], C[1] + 40), "YOU", font=F(BLK, 26), fill=INK, anchor="mm")
    if S("why") <= t < T_BACK + .3: glow(L, inner, r=16, k=.9 * (1 - back))          # not on orange: there it reads as a smudge

def cam(t):
    keys = [(0, 2.3, C), (T_L[0], 2.2, C), (T_L[1] + .2, 1.75, C), (T_L[2] + .2, 1.35, C), (T_L[3] + .3, 1.0, C),
            (S("reveal") + .1, 1.0, C), (S("reveal") + 1.0, 2.0, C), (T_BACK, 2.0, C), (T_BACK + .6, 2.3, C)]
    return cam_path(t, keys)

def head(d, t, line, sub=None):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    n = count(t); rev = EP.current(t) == "reveal"
    d.text((X0, 400), "CLOSE PEOPLE" if (rev or n is None) else "PEOPLE", font=F(MONO, 30), fill=MID)
    v = "4" if (rev or n is None) else f"{n:.0f}"
    d.text((X0 + (270 if (rev or n is None) else 150), 388), v, font=F(BLK, 64), fill=SIG if rev else INK)
    if sub: d.text((X1, 408), sub, font=F(MONO, 26), fill=MID, anchor="ra")

def draw(img, d, t, line, sub=None, note="call records · 2007 · one European country"):
    z, f = cam(t); camera(img, lambda L, dL: scene(L, dL, t), z, f); head(d, t, line, sub); fig(d, note)

def sc_hook(img, d, t): draw(img, d, t, "YOUR CIRCLES.", note="schematic")
def sc_setup(img, d, t): draw(img, d, t, "6 BILLION CALLS", sub="35 million people")
def sc_layers(img, d, t): draw(img, d, t, "WHO YOU CALL MOST", sub="averages")
def sc_reveal(img, d, t): draw(img, d, t, "INNER CIRCLE: 4.", sub="about 4.1 on average")
def sc_why(img, d, t): draw(img, d, t, "A LIMIT, NOT A FLAW." if t < T_BACK else "YOUR CIRCLES.", note="classic estimate: 5 / 15 / 50 / 150")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.bg = {k: "dark" for k in ORDER[:-1]}; EP.bg["reveal"] = "orange"
EP.scenes = {"hook": sc_hook, "setup": sc_setup, "layers": sc_layers, "reveal": sc_reveal, "why": sc_why}
FX = [(.05, whoosh(.8, .04), 0), (S("setup"), riser(.8, .04), 0), *[(x, pop(.12), (i - 1.5) / 2) for i, x in enumerate(T_L)],
      *[(T_L[i] + .1, whoosh(.5, .04), 0) for i in (1, 2, 3)],
      (S("reveal") + .1, thud(.55), 0), (S("reveal") + .9, pop(.14), 0), (T_BACK, whoosh(.5, .05), 0)]
if __name__ == "__main__": EP.run(FX)
