"""NOT JUST YOU – No. 132: three and a half degrees – on Facebook (2016, ~1.59 billion users) any two people are connected by
3.57 people in between on average (Bhagat et al. 2016); the old "six degrees" idea comes from Milgram's letter chains.
Level 2 + fx2 + CLARITY rules: a friend network is there from frame 0, the picture is explained once ("Each dot is a person").
OLD: the route through only local friends needs 6 people in between (made-up network, seed 55); NEW: a few long-distance
friendships (they GLOW) cut it to 3. A PARTICLE pulse runs along the route; the CAMERA starts on you, pulls out; orange reveal; loop."""
import os, sys, math, random
from collections import deque
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from fx2 import camera, cam_path, glow, dots, Stream
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .5, "setup": .5, "explain": .5, "old": .5, "reveal": .8, "why": .1})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "setup", "explain", "old", "reveal", "why", "end"]
EP = ThreadEpisode(TL, 132, "3.5 DEGREES", order=ORDER, dark=True, label="PLATFORM DATA · 1.6 BILLION USERS",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Bhagat et al. (2016), Three and a half degrees of", "separation, Facebook Research · Travers & Milgram (1969)"),
                   music=dict(bpm=100, root=2, prog="dream", kick="four", audio="v5"),
                   cover=dict(words=["YOU'RE 3.5", "PEOPLE AWAY", "FROM ANYONE."], kicker="Not six. Here's the network."))

N = 40; R = random.Random(55)
P = [(R.uniform(140, 940), R.uniform(570, 1100)) for _ in range(N)]
YOU = min(range(N), key=lambda i: P[i][0]); STR = max(range(N), key=lambda i: P[i][0])
D = lambda a, b: math.dist(P[a], P[b])
LOCAL = set()
for i in range(N):
    for j in sorted(range(N), key=lambda j: D(i, j))[1:4]: LOCAL.add((min(i, j), max(i, j)))
LONG = set()
while len(LONG) < 5:
    a, b = R.sample(range(N), 2)
    if D(a, b) > 420: LONG.add((min(a, b), max(a, b)))
def route(E):
    adj = {i: [] for i in range(N)}
    for a, b in E: adj[a].append(b); adj[b].append(a)
    prev = {YOU: None}; q = deque([YOU])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in prev: prev[v] = u; q.append(v)
    p = [STR]
    while prev[p[-1]] is not None: p.append(prev[p[-1]])
    return p[::-1]
OLD, NEW = route(LOCAL), route(LOCAL | LONG)          # 6 / 3 people in between
S_OLD, S_NEW = Stream([P[i] for i in OLD], n=260, width=10, seed=1), Stream([P[i] for i in NEW], n=260, width=10, seed=2)

T_YOU = S("explain") - .1
T_OLD = cue("old", "six steps") - .3
T_LONG = S("reveal") - .2; T_NEW = cue("reveal", "three and a half") - .2
T_BACK = cue("why", "That's why") - .35

def hops(t, path, t0, dt=.32):
    """how many links of the route are lit at t"""
    return min(len(path) - 1, max(0, int((t - t0) / dt) + 1)) if t >= t0 else 0

def scene(L, d, t):
    back = t >= T_BACK
    for k_, (a, b) in enumerate(sorted(LOCAL)):            # local friendships, drawn in during the cold open
        k = clamp((t - .05 - k_ * .012) / .3)
        if k > 0:
            pa, pb = P[a], P[b]; d.line([pa, (pa[0] + (pb[0] - pa[0]) * k, pa[1] + (pb[1] - pa[1]) * k)], fill=RULE, width=3)
    g = []
    if T_LONG <= t and not back:                            # long-distance friendships light up
        for (a, b) in LONG:
            k = spring((t - T_LONG) / .6, f=1.2, damp=6); pa, pb = P[a], P[b]
            q = (pa[0] + (pb[0] - pa[0]) * min(1, k), pa[1] + (pb[1] - pa[1]) * min(1, k)); d.line([pa, q], fill=MID, width=4)
            g.append([(pa[0] - 3, pa[1] - 3), (q[0] - 3, q[1] - 3), (q[0] + 3, q[1] + 3), (pa[0] + 3, pa[1] + 3)])
    if g and EP.current(t) != "reveal": glow(L, g, r=10, k=.6)
    path, t0, st = (OLD, T_OLD, S_OLD) if t < T_NEW else (NEW, T_NEW, S_NEW)
    if T_OLD <= t and not back:                             # the route, link by link, then a particle pulse along it
        n = hops(t, path, t0)
        for j in range(n): d.line([P[path[j]], P[path[j + 1]]], fill=SIG if EP.current(t) == "reveal" else INK, width=7)
        if n == len(path) - 1: dots(L, st.pos(t, flow=.5, active=1), INK, size=5)
    for i in range(N):
        x, y = P[i]; wave = (t - .05) / .9; r = 11 + 7 * max(0, 1 - abs((x - 140) / 800 - wave) * 5) if 0 <= wave <= 1.4 else 11
        on = (T_OLD <= t < T_NEW and i in OLD[:hops(t, OLD, T_OLD) + 1]) or (T_NEW <= t and not back and i in NEW[:hops(t, NEW, T_NEW) + 1])
        d.ellipse([x - r, y - r, x + r, y + r], fill=INK if (on or i in (YOU, STR)) else MID)
    if T_YOU <= t and not back:
        x, y = P[YOU]; callout(d, (x, y - 12), "l", y - 90, 1, "YOU", INK, k=(t - T_YOU) / .4)
        x, y = P[STR]; callout(d, (x, y - 12), "r", y - 90, 1, "ANYONE", INK, k=(t - T_YOU - .3) / .4)

def between(t):
    if T_OLD <= t < T_NEW: return max(0, min(len(OLD) - 2, hops(t, OLD, T_OLD) - 1)), False
    if T_NEW <= t < T_BACK: return 3.57 if t >= T_NEW + .9 else max(0, min(3, hops(t, NEW, T_NEW) - 1)), True
    return None, False

def cam(t):
    you = P[YOU]; mid = (540, 835)
    keys = [(0, 2.0, (you[0] + 120, you[1])), (S("setup") - .1, 1.9, (you[0] + 120, you[1])), (S("explain") - .1, 1.0, mid),
            (T_BACK, 1.0, mid), (T_BACK + .7, 2.0, (you[0] + 120, you[1]))]
    return cam_path(t, keys)

def head(d, t, line, sub=None):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    v, new = between(t)
    d.text((X0, 400), "PEOPLE IN BETWEEN" if v is not None else "PEOPLE", font=F(MONO, 30), fill=MID)
    txt = (f"{v:.2f}" if isinstance(v, float) else f"{v}") if v is not None else f"{N}"
    d.text((X0 + (370 if v is not None else 150), 388), txt, font=F(BLK, 64), fill=SIG if EP.current(t) == "reveal" else INK)
    if sub: d.text((X1, 470), sub, font=F(MONO, 26), fill=MID, anchor="ra")

def draw(img, d, t, line, sub=None, note="made-up network · schematic"):
    z, f = cam(t); camera(img, lambda L, dL: scene(L, dL, t), z, f); head(d, t, line, sub); fig(d, note)

def sc_hook(img, d, t): draw(img, d, t, "YOU TO ANYONE")
def sc_setup(img, d, t): draw(img, d, t, "1.6 BILLION USERS", sub="Facebook, 2016")
def sc_explain(img, d, t): draw(img, d, t, "DOT = PERSON")
def sc_old(img, d, t): draw(img, d, t, "THE OLD IDEA: 6", note="only through nearby friends")
def sc_reveal(img, d, t): draw(img, d, t, "REAL AVERAGE: 3.57", note="far-away friends make the shortcut")
def sc_why(img, d, t): draw(img, d, t, "A FRIEND OF A FRIEND." if t < T_BACK else "YOU TO ANYONE", note="Facebook users only · USA: 3.46")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.bg = {k: "dark" for k in ORDER[:-1]}; EP.bg["reveal"] = "orange"
EP.scenes = {"hook": sc_hook, "setup": sc_setup, "explain": sc_explain, "old": sc_old, "reveal": sc_reveal, "why": sc_why}
FX = [(.05, whoosh(.8, .04), 0), (S("explain") - .1, whoosh(.7, .04), 0), (T_YOU, pop(.12), -.5),
      *[(T_OLD + j * .32, tick(.04), -.6 + j * .2) for j in range(len(OLD) - 1)],
      (T_LONG, riser(.6, .04), 0), (S("reveal") + .1, thud(.55), 0), *[(T_NEW + j * .32, pop(.1), -.5 + j * .3) for j in range(len(NEW) - 1)],
      (T_BACK, whoosh(.5, .05), 0)]
if __name__ == "__main__": EP.run(FX)
