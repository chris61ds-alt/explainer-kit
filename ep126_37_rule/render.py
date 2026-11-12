"""NOT JUST YOU – No. 126 (level 2 remake, 12.11.2026): the 37 % rule – secretary problem with 10 dates; skipping the first 3,
then taking the first better one finds the best ~40 % of the time vs. ~10 % for a random pick (Ferguson 1989; Christian & Griffiths 2016).
Level 2: the isometric row of 10 dates is there from frame 0 (ripple), ONE continuous object, dates you pass drop away,
the rule plays out on the row, then 1,000 lives flicker through it with a live counter, orange reveal, loop back into the hook.
Old version: render_v1.py / script_v1.json."""
import os, sys, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .34, "setup": .34, "rule": .34, "sim": .2, "reveal": .4, "why": .1})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "setup", "rule", "sim", "reveal", "why", "end"]
EP = ThreadEpisode(TL, 126, "37 RULE", order=ORDER, dark=True, label="SIMULATION · MATH MODEL",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Ferguson (1989), Who solved the secretary problem?, Stat. Science ·", "Christian & Griffiths (2016), Algorithms to Live By"),
                   music=dict(bpm=100, root=0, prog="dream", kick="four", audio="v5"),
                   cover=dict(words=["YOU SETTLED", "TOO EARLY.", "OR TOO LATE."], kicker="The 37 % rule. Simulated."))

QUAL = [.42, .71, .55, .38, .66, .97, .5, .9, .6, .45]       # one example life: the rule picks date 6, which is also the best
SKIP, PICK = 3, 5
R = random.Random(1); LIVES = []
for _ in range(1000):
    v = [R.random() for _ in range(10)]; best = max(v); th = max(v[:SKIP])
    pick = next((x for x in v[SKIP:] if x > th), v[-1]); LIVES.append((v, pick == best, R.choice(v) == best))
WIN_RULE = sum(l[1] for l in LIVES); WIN_RAND = sum(l[2] for l in LIVES)     # 401 / 107

I = Iso(500, 1010, .62)
def hq(q): return 60 + 520 * q
T_GONE0, T_GONE1 = cue("setup", "Pass on") - .1, E("setup")
T_LOOK, T_TAKE = cue("rule", "just look") - .1, cue("rule", "Then take") - .1
T_SIM0, T_SIM1 = S("sim") - .1, S("reveal") - .2
T_BACK = cue("why", "Otherwise") - .3

def nlives(t): return 0 if t < T_SIM0 else 1000 if t >= T_SIM1 else int(1000 * ease_io(clamp((t - T_SIM0) / (T_SIM1 - T_SIM0))))

def card_state(t, i):
    """(height, top colour, sink offset) of date i at time t"""
    flat, top, sink = 40.0, TOP, 0.0
    wave = (t - .05) / .9
    if 0 <= wave <= 1.4: flat += 70 * max(0, 1 - abs(i / 9 - wave) * 4)          # cold open: a ripple runs down the row
    if t < S("rule"):
        if t >= T_GONE0:                                                          # you pass on them: they sink away
            dt = t - T_GONE0 - i * (T_GONE1 - T_GONE0) / 10
            if dt > 0: sink = -min(1, dt / .35) ** 2 * 60; top = RIGHT
        return flat, top, sink
    if T_SIM0 <= t < T_SIM1:                                                      # 1,000 lives flicker through the row
        v = LIVES[max(0, nlives(t) - 1)][0]; th = max(v[:SKIP]); p = next((j for j in range(SKIP, 10) if v[j] > th), 9)
        return hq(v[i]), RIGHT if i < SKIP else (INK if i == p else TOP), 0
    back = clamp((t - T_BACK) / .45) if t >= T_BACK else 0
    h = flat
    if i < SKIP and t >= T_LOOK: h = flat + (hq(QUAL[i]) - flat) * spring((t - T_LOOK - i * .15) / .5); top = RIGHT
    if SKIP <= i <= PICK and t >= T_TAKE:
        h = flat + (hq(QUAL[i]) - flat) * spring((t - T_TAKE - (i - SKIP) * .3) / .5)
        if i == PICK and t >= T_TAKE + .7: top = SIG if t >= S("reveal") else INK
    if t >= S("reveal") and i > PICK: h = flat + (hq(QUAL[i]) - flat) * spring((t - S("reveal") - .5 - (i - PICK) * .08) / .5); top = TOP
    if back: h = h + (40 - h) * ease(back); top = TOP if back > .5 else top
    return h, top, 0

def row(img, d, t):
    I.grid(img)
    for i in range(10):
        h, top, sink = card_state(t, i); x, y = -470 + i * 100, 260 - i * 60
        I.box(d, x, y, sink, 70, 70, max(4, h), top=top)
        fx, fy = I.P(x + 70, y + 70, sink); d.text((fx, fy + 10), str(i + 1), font=F(BLK, 30), fill=MID if top == RIGHT else INK, anchor="ma")
    if T_LOOK + .6 <= t < T_SIM0 or S("reveal") <= t < T_BACK:                   # the bar set by the first three
        th = hq(max(QUAL[:SKIP])); k = spring((t - (T_LOOK + .6 if t < T_SIM0 else S("reveal"))) / .5, f=1, damp=6)
        a, b = I.P(-470, 260, th), I.P(-470 + 9 * 100 + 70, 260 - 9 * 60, th); d.line([a, (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k)], fill=MID, width=4)
    if T_TAKE + .7 <= t < T_SIM0 or S("reveal") + .2 <= t < T_BACK:
        p = I.P(-470 + PICK * 100 + 35, 260 - PICK * 60 + 35, hq(QUAL[PICK])); tk = T_TAKE + .7 if t < T_SIM0 else S("reveal") + .2
        callout(d, p, "r", p[1] - 70, 1, "PICK", SIG if t >= S("reveal") else INK, k=(t - tk) / .4)

def head(d, t, line, sub=None):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    n = nlives(t) if t < T_BACK else 0
    if n == 0:
        d.text((X0, 400), "DATES", font=F(MONO, 30), fill=MID); d.text((X0 + 130, 388), "10", font=F(BLK, 64), fill=INK)
    else:
        wr = sum(l[1] for l in LIVES[:n]) / n; wd = sum(l[2] for l in LIVES[:n]) / n
        d.text((X0, 400), "BEST FOUND", font=F(MONO, 30), fill=MID); d.text((X0 + 240, 388), f"{wr * 100:.0f} %", font=F(BLK, 64), fill=SIG)
        d.text((X0 + 470, 400), "RANDOM", font=F(MONO, 30), fill=MID); d.text((X0 + 620, 388), f"{wd * 100:.0f} %", font=F(BLK, 64), fill=INK)
    if sub: d.text((X1, 470), sub, font=F(MONO, 26), fill=MID, anchor="ra")

def sc_hook(img, d, t): head(d, t, "WHEN DO YOU COMMIT?"); row(img, d, t); fig(d, "simulation")
def sc_setup(img, d, t): head(d, t, "PASS = GONE.", sub="one after another"); row(img, d, t); fig(d, "schematic")
def sc_rule(img, d, t): head(d, t, "SKIP 37 %. THEN PICK.", sub="for 10 dates: skip 3"); row(img, d, t); fig(d, "then take the first who beats them all")
def sc_sim(img, d, t): head(d, t, f"{nlives(t):,} LOVE LIVES", sub="10 dates each"); row(img, d, t); fig(d, "simulation")
def sc_reveal(img, d, t): head(d, t, "THE RULE: 40 %.", sub="found the very best one"); row(img, d, t); fig(d, "simulation · 1,000 lives")
def sc_why(img, d, t):
    head(d, t, "EXPLORE. THEN COMMIT." if t < T_BACK else "WHEN DO YOU COMMIT?"); row(img, d, t)
    fig(d, "a model · real people can say no")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.bg = {"hook": "light", "setup": "light", "rule": "light", "sim": "light", "reveal": "orange", "why": "light"}
EP.scenes = {"hook": sc_hook, "setup": sc_setup, "rule": sc_rule, "sim": sc_sim, "reveal": sc_reveal, "why": sc_why}
FX = [(.05, whoosh(.8, .05), 0), *[(T_GONE0 + i * (T_GONE1 - T_GONE0) / 10, tick(.03), (i - 5) / 6) for i in range(10)],
      *[(T_LOOK + i * .15, pop(.08), -.3) for i in range(SKIP)], (T_LOOK + .6, whoosh(.4, .04), 0),
      *[(T_TAKE + j * .3, pop(.08), .1 * j) for j in range(3)], (T_TAKE + .7, pop(.14), .3),
      *[(T_SIM0 + j * .09, tick(.025), (j % 5 - 2) / 3) for j in range(int((T_SIM1 - T_SIM0) / .09))],
      (S("reveal") + .1, thud(.55), 0), (T_BACK, whoosh(.45, .05), 0)]
if __name__ == "__main__": EP.run(FX)
