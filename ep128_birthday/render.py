"""NOT JUST YOU – No. 128: the birthday problem – 23 people: 50.7 % chance that two share a birthday, 70 people: 99.9 %;
23 people form 253 pairs. Visible SIMULATION of 1,000 rooms.
Level 2 + fx2: a 365-day calendar grid is there from frame 0 (ripple); 23 birthdays drop in with gravity, a shared day GLOWS;
then 1,000 rooms flicker through the same grid with a live counter, orange reveal, all 253 pair lines draw in, loop back."""
import os, sys, math, random
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from fx2 import glow
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .34, "setup": .34, "sim": .2, "reveal": .4, "why": .1})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "setup", "sim", "reveal", "why", "end"]
EP = ThreadEpisode(TL, 128, "BIRTHDAY", order=ORDER, dark=False, label="SIMULATION · MATH MODEL",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Birthday problem (probability theory) ·", "simulation: 1,000 rooms of 23 people"),
                   music=dict(bpm=104, root=1, prog="major", kick="four", audio="v5"),
                   cover=dict(words=["23 PEOPLE.", "2 SHARE A", "BIRTHDAY."], kicker="Probably. Watch 1,000 rooms."))

COLS, ROWS, CW, CH = 19, 20, 44, 30
GX, GY = (W - COLS * CW) // 2, 540
def cell(day): return GX + (day % COLS) * CW, GY + (day // COLS) * CH
R = random.Random(18); ROOMS = []                                        # seed 18: 509 of 1,000 rooms match (math: 50.7 %)
for _ in range(1000):
    b = [R.randrange(365) for _ in range(23)]; ROOMS.append((b, len(set(b)) < 23))
FIRST = next(r for r in ROOMS if r[1] and len(set(r[0])) == 22)[0]       # the example room: exactly one shared day
MATCH = next(x for x in FIRST if FIRST.count(x) == 2)
RATE = sum(r[1] for r in ROOMS) / 1000                                   # ~0.5

T_DROP0 = .25; DROP_DT = (cue("setup", "Sounds unlikely") - .3 - T_DROP0) / 23
T_SIM0, T_SIM1 = S("sim") - .1, S("reveal") - .2
T_PAIRS = cue("why", "two hundred fifty") - .2
T_BACK = cue("why", "That's why") - .35

def nrooms(t): return 0 if t < T_SIM0 else 1000 if t >= T_SIM1 else max(1, int(1000 * ease_io(clamp((t - T_SIM0) / (T_SIM1 - T_SIM0)))))

def grid(d, t):
    wave = (t - .05) / .9
    for day in range(365):
        x, y = cell(day); k = 0
        if 0 <= wave <= 1.4: k = max(0, 1 - abs(day / 364 - wave) * 6)              # cold open ripple across the year
        g = 4 * k; d.rectangle([x + 4 - g, y + 4 - g, x + CW - 4 + g, y + CH - 4 + g], fill=mix(RULE, MID, k))

def birthdays(img, d, t):
    """the example room: dots fall into their day; returns screen centres"""
    back = clamp((t - T_BACK) / .4) if t >= T_BACK else 0
    out = []
    for i, day in enumerate(FIRST):
        x, y = cell(day); cx, cy = x + CW / 2, y + CH / 2
        if day == MATCH and FIRST.index(day) != i: cx += 9                          # the second dot sits next to the first
        if day == MATCH and FIRST.index(day) == i: cx -= 9
        tk = T_DROP0 + i * DROP_DT; dt = t - tk
        if dt < 0: continue
        fall = max(0, 1 - dt / .35); yy = cy - 500 * fall * fall - 1100 * back * back
        out.append((cx, yy)); d.ellipse([cx - 9, yy - 9, cx + 9, yy + 9], fill=INK)
    return out

def room_dots(img, d, t):
    b, m = ROOMS[nrooms(t) - 1]; shared = {x for x in b if b.count(x) > 1}; g = []
    for day in b:
        x, y = cell(day); d.ellipse([x + CW / 2 - 8, y + CH / 2 - 8, x + CW / 2 + 8, y + CH / 2 + 8], fill=INK if day not in shared else SIG)
        if day in shared: g.append(("c", x + CW / 2, y + CH / 2, 16))
    glow(img, g, col=SIG, r=14, k=.8)

def match_glow(img, d, t, k=1.0):
    x, y = cell(MATCH); glow(img, [("c", x + CW / 2, y + CH / 2, 22)], col=SIG, r=18, k=.9 * k)
    callout(d, (x + CW / 2, y), "r", y - 60, 1, "SAME DAY", SIG, k=k)

def pairs(d, t, pts):
    k = clamp((t - T_PAIRS) / 1.0) * (1 - clamp((t - T_BACK) / .25)); n = int(253 * ease(k)); c = 0
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            if c >= n: return
            d.line([pts[i], pts[j]], fill=MID, width=1); c += 1

def head(d, t, line, sub=None):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    n = nrooms(t) if t < T_BACK else 0
    if n == 0:
        k = sum(1 for i in range(23) if t >= T_DROP0 + i * DROP_DT) if t < T_BACK else 0
        d.text((X0, 400), "PEOPLE", font=F(MONO, 30), fill=MID); d.text((X0 + 150, 388), f"{k}", font=F(BLK, 64), fill=INK)
    else:
        r = sum(ROOMS[i][1] for i in range(n)) / n; rev = t >= S("reveal") - .2
        d.text((X0, 400), "ROOMS WITH A MATCH", font=F(MONO, 30), fill=MID)
        d.text((X0 + 380, 388), f"{r * 100:.0f} %", font=F(BLK, 64), fill=SIG if rev else INK)
    if sub: d.text((X1, 470), sub, font=F(MONO, 26), fill=MID, anchor="ra")

def sc_hook(img, d, t): head(d, t, "23 PEOPLE."); grid(d, t); birthdays(img, d, t); fig(d, "every square: one day of the year")
def sc_setup(img, d, t):
    head(d, t, "365 DAYS."); grid(d, t); birthdays(img, d, t)
    if t >= cue("setup", "Sounds unlikely") - .1: match_glow(img, d, t, clamp((t - cue("setup", "Sounds unlikely") + .1) / .4))
    fig(d, "one room · 23 birthdays")
def sc_sim(img, d, t): head(d, t, f"{nrooms(t):,} ROOMS", sub="23 people each"); grid(d, t); room_dots(img, d, t); fig(d, "simulation")
def sc_reveal(img, d, t):
    head(d, t, "HALF HAVE A MATCH.", sub="70 people: 99.9 %"); grid(d, t); birthdays(img, d, t); match_glow(img, d, t); fig(d, "simulation · math: 50.7 %")
def sc_why(img, d, t):
    head(d, t, "253 PAIRS." if t < T_BACK else "23 PEOPLE.", sub="23 × 22 ÷ 2" if t < T_BACK else None); grid(d, t)
    pts = birthdays(img, d, t); pairs(d, t, pts)
    if t < T_BACK: match_glow(img, d, t)
    fig(d, "every line: one pair that could match")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.bg = {"hook": "light", "setup": "light", "sim": "light", "reveal": "orange", "why": "light"}
EP.scenes = {"hook": sc_hook, "setup": sc_setup, "sim": sc_sim, "reveal": sc_reveal, "why": sc_why}
FX = [(.05, whoosh(.8, .04), 0), *[(T_DROP0 + i * DROP_DT + .3, tick(.03), (cell(FIRST[i])[0] - 540) / 450) for i in range(23)],
      (cue("setup", "Sounds unlikely") - .1, pop(.14), .3),
      *[(T_SIM0 + j * .09, tick(.025), (j % 5 - 2) / 3) for j in range(int((T_SIM1 - T_SIM0) / .09))],
      (S("reveal") + .1, thud(.55), 0), (T_PAIRS, riser(.9, .04), 0), (T_BACK, whoosh(.5, .05), 0)]
if __name__ == "__main__": EP.run(FX)
