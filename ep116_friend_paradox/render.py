"""NOT JUST YOU – No. 116 (level 2 remake, 12.11.2026): the friendship paradox – your friends have more friends than you
(Feld 1991; Marketville high school: 55 % of girls had fewer friends than their friends' average).
Level 2: the friend network is there from frame 0 (ripple), ONE continuous object, the popular one grows and lights up
all their links, then everyone compares (live counter), orange reveal, loop back into the hook. Old version: render_v1.py."""
import os, sys, math, random
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .34, "setup": .34, "count": .34, "reveal": .4, "why": .1})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "setup", "count", "reveal", "why", "end"]
EP = ThreadEpisode(TL, 116, "FRIEND PARADOX", order=ORDER, dark=True, label="SIMULATION · SCHOOL DATA",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Feld (1991), Why your friends have more friends", "than you do, American Journal of Sociology 96(6)"),
                   music=dict(bpm=98, root=-1, prog="dream", kick="four", audio="v5"),
                   cover=dict(words=["YOUR FRIENDS", "HAVE MORE", "FRIENDS THAN YOU."], kicker="It's math, not you."))

# a made-up friend group: one very popular person (0), a second social one (1), the rest with a few friends each
R = random.Random(5); N = 26; EDGES = set()
for j in R.sample(range(2, N), 17): EDGES.add((0, j))
for j in R.sample(range(2, N), 8): EDGES.add((1, j))
EDGES.add((0, 1))
for _ in range(12):
    a, b = R.sample(range(2, N), 2); EDGES.add((min(a, b), max(a, b)))
EDGES = sorted(EDGES); DEG = [0] * N; NB = [[] for _ in range(N)]
for a, b in EDGES: DEG[a] += 1; DEG[b] += 1; NB[a].append(b); NB[b].append(a)
FAVG = [sum(DEG[j] for j in NB[i]) / len(NB[i]) for i in range(N)]
FEWER = [DEG[i] < FAVG[i] for i in range(N)]; NF = sum(FEWER)          # 23 of 26

def layout():
    """deterministic force layout, scaled into the content box"""
    rs = np.random.RandomState(3); P = rs.rand(N, 2) - .5; P[0] = 0
    for it in range(400):
        F_ = np.zeros_like(P)
        for i in range(N):
            dv = P[i] - P; dist = np.sqrt((dv ** 2).sum(1)) + 1e-3
            F_[i] += (dv / dist[:, None] ** 3 * .004).sum(0)
        for a, b in EDGES:
            dv = P[b] - P[a]; F_[a] += dv * .08; F_[b] -= dv * .08
        F_ -= P * .02; P += np.clip(F_, -.05, .05)
    P -= P.mean(0); P /= np.abs(P).max(0)
    return [(500 + x * 360, 850 + y * 260) for x, y in P]
POS = layout()
ORDER_EVAL = sorted(range(N), key=lambda i: (POS[i][1], POS[i][0]))       # nodes compare top to bottom

T_HUB = cue("setup", "One person") - .1
T_C0, T_C1 = cue("count", "compares") - .1, E("count") + .1
T_SCH = cue("reveal", "In a real high school") - .1
T_BACK = cue("why", "That's why") - .35
def t_eval(i): return T_C0 + ORDER_EVAL.index(i) * (T_C1 - T_C0) / N

def radius(i): return 10 + 2.2 * DEG[i]

def net(d, t):
    back = clamp((t - T_BACK) / .4) if t >= T_BACK else 0
    hub = spring((t - T_HUB) / .6) * (1 - back) if t >= T_HUB else 0
    for k_, (a, b) in enumerate(EDGES):                          # links draw in during the hook
        k = spring((t - .1 - k_ * .025) / .4, f=1.2, damp=6)
        if k <= 0: continue
        pa, pb = POS[a], POS[b]; hot = 0 in (a, b) and hub > .2
        d.line([pa, (pa[0] + (pb[0] - pa[0]) * min(1, k), pa[1] + (pb[1] - pa[1]) * min(1, k))], fill=INK if hot else MID, width=5 if hot else 3)
    wave = (t - .05) / .9
    for i in range(N):
        x, y = POS[i]; r = 14.0
        if 0 <= wave <= 1.4: r += 10 * max(0, 1 - abs((x - X0) / (X1 - X0) - wave) * 5)    # cold open ripple
        r += (radius(i) - 14) * (1 - back) * (1 if t >= T_C0 else (hub if i == 0 else 0))
        if i == 0 and hub: r += 2 * hub * (1 + .1 * math.sin(t * 7))
        col = INK
        if T_C0 <= t and not back:
            te = t_eval(i)
            if t >= te:
                k = spring((t - te) / .3)
                col = SIG if (FEWER[i] and S("reveal") <= t < S("why")) else (INK if FEWER[i] else MID)
                if FEWER[i]: r += 6 * (k - 1) * -1 if k > 1 else 0
        d.ellipse([x - r, y - r, x + r, y + r], fill=col)
    if hub > .3 and t < T_C0:
        x, y = POS[0]; callout(d, (x, y - radius(0) * hub), "r", y - 200, 1, f"{DEG[0]} FRIENDS", INK, k=(t - T_HUB - .3) / .4)

def head(d, t, line, sub=None):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    if T_C0 <= t < T_BACK:
        n = sum(1 for i in range(N) if FEWER[i] and t >= t_eval(i))
        d.text((X0, 400), "FEWER THAN THEIR FRIENDS", font=F(MONO, 30), fill=MID); d.text((X0 + 470, 388), f"{n} / {N}", font=F(BLK, 64), fill=SIG if S("reveal") <= t < S("why") else INK)
    else:
        d.text((X0, 400), "PEOPLE", font=F(MONO, 30), fill=MID); d.text((X0 + 140, 388), f"{N}", font=F(BLK, 64), fill=INK)
    if t >= T_SCH and t < T_BACK:
        k = spring((t - T_SCH) / .4); d.text((X1, 470 + 20 * (1 - k)), "REAL SCHOOL: 55 % OF GIRLS", font=F(BLK, 40), fill=INK, anchor="ra")
    if sub: d.text((X1, 470), sub, font=F(MONO, 26), fill=MID, anchor="ra")

def sc_hook(img, d, t): head(d, t, "MORE FRIENDS?"); net(d, t); fig(d, "made-up group · simulation")
def sc_setup(img, d, t): head(d, t, "ONE POPULAR PERSON", sub="everyone else: a few friends"); net(d, t); fig(d, "made-up group · simulation")
def sc_count(img, d, t): head(d, t, "YOU VS. YOUR FRIENDS"); net(d, t); fig(d, "your friend count vs. their average")
def sc_reveal(img, d, t): head(d, t, "MOST HAVE FEWER."); net(d, t); fig(d, "simulation · school data: Feld 1991")
def sc_why(img, d, t):
    head(d, t, "IT'S MATH, NOT YOU." if t < T_BACK else "MORE FRIENDS?"); net(d, t)
    fig(d, "the popular one is in everyone's list")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.bg = {"hook": "dark", "setup": "dark", "count": "dark", "reveal": "orange", "why": "dark"}
EP.scenes = {"hook": sc_hook, "setup": sc_setup, "count": sc_count, "reveal": sc_reveal, "why": sc_why}
FX = [(.05, whoosh(.8, .05), 0), *[(.1 + j * .1, tick(.025), (j % 5 - 2) / 3) for j in range(len(EDGES) // 4)],
      (T_HUB, thud(.4), 0), (T_HUB + .3, pop(.12), .3),
      *[(t_eval(i), pop(.07) if FEWER[i] else tick(.03), (POS[i][0] - 500) / 420) for i in range(N)],
      (S("reveal") + .1, thud(.55), 0), (T_SCH, pop(.14), .3), (T_BACK, whoosh(.45, .05), 0)]
if __name__ == "__main__": EP.run(FX)
