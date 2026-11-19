"""NOT JUST YOU – No. 147: how many close friends is normal? ('Where do you stand?' format, after No. 138)
Survey Center on American Life 2021: none 12 %, one to four 48 %, ten or more 13 % (five to nine = rest 27 %);
Gallup 1990: none 3 %, one to four 32 %, ten or more 33 % (rest 32 %).
ONE continuous object: four steps (0 · 1–4 · 5–9 · 10+), 100 dots (1 dot = 1 % of people). Cold open: dots rain onto the
steps and pile up on '1–4', '1–4' stamp. 'then': the dots hop to the 1990 distribution, 'now' hop back. Payoff (rule 15):
the 2021 piles with a 'YOU?' marker on the biggest step. Light look, reveal on black."""
import os, sys, math
import numpy as np
from PIL import ImageDraw
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from fx2 import light_look, is_light, stamp
from stand import shadowed, you_marker
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .5, "setup": .5, "explain": .5, "reveal": .8, "then": .8, "why": .1})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "setup", "explain", "reveal", "then", "why", "end"]
EP = ThreadEpisode(TL, 147, "HOW MANY FRIENDS?", order=ORDER, dark=True, label="SURVEY · US ADULTS · 2021 vs 1990",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Survey Center on American Life (2021) ·", "Gallup (1990)"),
                   music=dict(bpm=98, root=2, prog="major", kick="four", audio="v5"),
                   cover=dict(words=["HOW MANY", "CLOSE FRIENDS", "IS NORMAL?"], kicker="Where do you stand?"))
light_look(EP, ORDER)

STEPS = ["0", "1–4", "5–9", "10+"]
N21 = [12, 48, 27, 13]; N90 = [3, 32, 32, 33]
SX0, SW = 60, 240
def step_top(i): return 1100 - i * 70
PER_ROW, DR, GAP = 9, 10, 25

def layout(counts):
    pos = []
    for s, n in enumerate(counts):
        for j in range(n):
            x = SX0 + s * SW + 22 + (j % PER_ROW) * GAP + (GAP / 2 if (j // PER_ROW) % 2 else 0)
            y = step_top(s) - DR - 2 - (j // PER_ROW) * (GAP - 3)
            pos.append((x, y, s))
    return pos
P21, P90 = layout(N21), layout(N90)
# pair dots 2021 <-> 1990 so each dot hops to the nearest-step slot
order21 = sorted(range(100), key=lambda i: (P21[i][2], P21[i][0])); order90 = sorted(range(100), key=lambda i: (P90[i][2], P90[i][0]))
PAIR = {a: b for a, b in zip(order21, order90)}

T_RAIN = .2
T_STAMP = cue("hook", "Fewer") - .05
T_EXP = cue("explain", "Each step") - .1
T_HALF = cue("reveal", "Almost half") - .1; T_NONE = cue("reveal", "none") - .3
T_90 = S("then") + .05; T_NOW = cue("then", "Now") - .1
T_YOU = S("why") + .3

def dot_pos(i, t):
    x, y, s = P21[i]
    rain = clamp((t - T_RAIN - (i % 25) * .03) / .45)
    y0 = y - 700 * (1 - rain) ** 2
    if t >= T_90:
        a = (x, y); b = P90[PAIR[i]][:2]
        k = ease_io(clamp((t - T_90 - (i % 13) * .02) / .7))
        if t >= T_NOW: k = 1 - ease_io(clamp((t - T_NOW - (i % 13) * .02) / .7))
        hop = 120 * math.sin(math.pi * k) if 0 < k < 1 else 0
        return a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k - hop
    return x, y0

def objects(L, d, t):
    cur = EP.current(t)
    for s in range(4):
        x0 = SX0 + s * SW; hot = (cur == "explain" and t >= T_EXP + s * .1) or (cur == "reveal" and ((s == 1 and t >= T_HALF) or (s == 0 and t >= T_NONE)))
        d.rectangle([x0, step_top(s), x0 + SW - 10, 1160], fill=WHITE, outline=INK if hot else RULE, width=4 if hot else 2)
        d.text((x0 + (SW - 10) / 2, step_top(s) + 36), STEPS[s], font=F(BLK, 40), fill=INK if hot else MID, anchor="mm")
    for i in range(100):
        x, y = dot_pos(i, t); s = P21[i][2]
        col = INK
        if cur == "reveal": col = SIG if ((s == 1 and t >= T_HALF) or (s == 0 and t >= T_NONE)) else MID
        if cur == "then" and t >= T_90 + .7 and t < T_NOW: col = SIG if P90[PAIR[i]][2] == 3 else MID
        d.ellipse([x - DR, y - DR, x + DR, y + DR], fill=col)
    if cur in ("why", "end"): you_marker(d, SX0 + SW + 115, step_top(1) - 6 * (GAP - 3) - 30, t, T_YOU)

def labels(d, t):
    cur = EP.current(t)
    if T_STAMP <= t < S("setup") + .3: stamp(d, (SX0 + SW + 115, 640), "1–4", t, T_STAMP, size=100)
    if cur == "then" and t >= T_90 + .5 and t < T_NOW:
        d.text((1020, 560), "1990", font=F(BLK, 90), fill=SIG, anchor="ra")
    if cur == "then" and t >= T_NOW + .4: d.text((1020, 560), "2021", font=F(BLK, 90), fill=INK, anchor="ra")

def head(d, t, line):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    cur = EP.current(t)
    if cur == "then" and T_90 + .5 <= t < T_NOW:
        d.text((X0, 400), "10+ CLOSE FRIENDS", font=F(MONO, 30), fill=MID); d.text((X0 + 360, 388), "33%", font=F(BLK, 56), fill=SIG)
    elif cur == "then" and t >= T_NOW:
        d.text((X0, 400), "10+ CLOSE FRIENDS", font=F(MONO, 30), fill=MID); d.text((X0 + 360, 388), "13%", font=F(BLK, 56), fill=INK)
    else:
        d.text((X0, 400), "1 TO 4 CLOSE FRIENDS", font=F(MONO, 30), fill=MID)
        d.text((X0 + 410, 388), "48%" if t >= T_STAMP else "?", font=F(BLK, 56), fill=SIG if cur == "reveal" else INK)

def draw(img, d, t, line, note="1 dot = 1% of US adults · 2021"):
    shadowed(EP, img, t, objects); d = ImageDraw.Draw(img); labels(d, t); head(d, t, line); fig(d, note)

def sc_hook(img, d, t): draw(img, d, t, "HOW MANY IS NORMAL?")
def sc_setup(img, d, t): draw(img, d, t, "COUNT YOUR FRIENDS.", note="Survey Center on American Life · May 2021")
def sc_explain(img, d, t): draw(img, d, t, "1 DOT = 1%")
def sc_reveal(img, d, t): draw(img, d, t, "MOST: 1 TO 4.")
def sc_then(img, d, t): draw(img, d, t, "THEN VS. NOW.", note="1990: Gallup · 5–9 = the rest")
def sc_why(img, d, t): draw(img, d, t, "SMALL IS NORMAL.")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.scenes = {"hook": sc_hook, "setup": sc_setup, "explain": sc_explain, "reveal": sc_reveal, "then": sc_then, "why": sc_why}
FX = [*[(T_RAIN + .3 + j * .06, tick(.012), -.6 + j * .1) for j in range(12)], (T_STAMP, thud(.3), 0),
      *[(T_EXP + s * .1, tick(.015), -.6 + s * .4) for s in range(4)], (S("reveal") + .05, thud(.35), 0), (T_HALF, pop(.1), -.2), (T_NONE, pop(.1), -.6),
      (T_90, whoosh(.4, .03), .3), *[(T_90 + .2 + j * .06, tick(.012), -.4 + j * .1) for j in range(8)], (T_NOW, whoosh(.4, .03), -.3),
      (T_YOU, pop(.12), 0)]
FX = [fx for fx in FX if fx[0] < 1e8]
if __name__ == "__main__": EP.run(FX)
