"""NOT JUST YOU – No. 129: Gottman's 5 : 1 – in stable couples about five positive moments per negative one during
conflict; 1 : 1 or less went with later separation (Gottman & Levenson 1992; Gottman 1994; exact ratio debated).
Level 2 + fx2: a balance scale is there from frame 0, the bad moment drops in with weight (cold open), good moments form out of
PARTICLES that swarm into the other pan and GLOW, the beam tips with a spring; 5 : 1 reveal in orange, then they float off
to 1 : 1 and the scale sinks; loop: the bad moment lifts out again."""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from fx2 import glow, dots
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .34, "setup": .34, "reveal": .4, "split": .34, "why": .1})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "setup", "reveal", "split", "why", "end"]
EP = ThreadEpisode(TL, 129, "FIVE TO ONE", order=ORDER, dark=False, label="OBSERVATION · COUPLES IN CONFLICT",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Gottman & Levenson (1992), J. of Personality and", "Social Psychology 63(2) · Gottman (1994)"),
                   music=dict(bpm=92, root=-1, prog="tense", kick="half", audio="v5"),
                   cover=dict(words=["ONE FIGHT", "NEEDS FIVE", "GOOD MOMENTS."], kicker="What lasting couples do. Even mid-argument."))

PIV = (540, 640); ARM = 300; HANG = 250
LABELS = ["JOKE", "TOUCH", "NOD", "SMILE", "SORRY"]
T_BAD = .15                                                    # the bad moment drops in right away
T_G = [cue("hook", "five good") - .1 + i * .18 for i in range(5)]
T_GONE = [cue("split", "one to one") - .2 + i * .12 for i in range(4)]       # four of five float away
T_LAB = [cue("why", w) - .1 for w in ("A joke", "A touch", "A nod")]
T_BACK = cue("why", "That's why") - .35
T_RE = [S("why") + .3 + i * .15 for i in range(4)]              # after the split they come back for "they add up"

def good_k(t, i):
    """0..1 presence of good moment i (swarm in, float away, come back, gone at the loop)"""
    k = clamp((t - T_G[i]) / .5)
    if i >= 1 and t >= T_GONE[i - 1]: k *= 1 - clamp((t - T_GONE[i - 1]) / .4)
    if i >= 1 and t >= T_RE[i - 1]: k = clamp((t - T_RE[i - 1]) / .5)
    if t >= T_BACK: k *= 1 - clamp((t - T_BACK - i * .05) / .3)
    return k

def bad_k(t):
    if t >= T_BACK + .1: return 1 - clamp((t - T_BACK - .1) / .35)
    return clamp((t - T_BAD) / .35)

def tilt_target(t):
    g = sum(1 for i in range(5) if good_k(t, i) > .6); b = bad_k(t) > .6
    return max(-.35, min(.35, (5 * b - g) * .07))                # + = bad side (left) down

def tilt(t):
    """spring toward the target, re-evaluated at each change: simple critically-damped follow over the last 0.8 s"""
    a = tilt_target(t - .8)
    for j in range(17):
        tt = t - .8 + j * .05; a += (tilt_target(tt) - a) * .35
    return a + .03 * math.sin(t * 9) * math.exp(-max(0, t - T_BAD - .35) * 3)

def pans(t):
    a = tilt(t); ca, sa = math.cos(a), math.sin(a)
    L = (PIV[0] - ARM * ca, PIV[1] + ARM * sa); Rr = (PIV[0] + ARM * ca, PIV[1] - ARM * sa)
    return a, L, Rr

def scale(d, t):
    a, L, Rr = pans(t)
    d.polygon([(PIV[0], PIV[1] + 10), (PIV[0] - 70, 1130), (PIV[0] + 70, 1130)], fill=RULE)   # stand
    d.line([(PIV[0] - 120, 1130), (PIV[0] + 120, 1130)], fill=INK, width=8)
    d.line([L, Rr], fill=INK, width=12); d.ellipse([PIV[0] - 16, PIV[1] - 16, PIV[0] + 16, PIV[1] + 16], fill=INK)
    for (x, y) in (L, Rr):
        py = y + HANG; d.line([(x, y), (x - 110, py)], fill=MID, width=3); d.line([(x, y), (x + 110, py)], fill=MID, width=3)
        d.chord([x - 130, py - 40, x + 130, py + 40], 0, 180, fill=INK)
    return L, Rr

def slot(Rr, i):
    """resting place of good moment i in the right pan"""
    x, y = Rr; py = y + HANG
    return (x - 88 + (i % 3) * 88 + (44 if i >= 3 else 0), py - 26 - (i // 3) * 50)

def draw(img, d, t, line, sub=None, note="observation · a link, not proof"):
    L, Rr = scale(d, t)
    kb = bad_k(t)                                              # the bad moment: one heavy ball
    if kb > 0:
        x, y = L[0], L[1] + HANG - 62; fall = 1 - kb; y -= 700 * fall * fall
        d.ellipse([x - 60, y - 60, x + 60, y + 60], fill=INK); d.text((x, y), "FIGHT", font=F(BLK, 30), fill=BG, anchor="mm")
    g, swarm = [], []
    for i in range(5):                                         # good moments: particles swarm in and become a ball
        k = good_k(t, i)
        if k <= 0: continue
        sx, sy = slot(Rr, i); R_ = np.random.RandomState(i)
        start = np.stack([sx + R_.randn(70) * 160, sy - 420 + R_.randn(70) * 90], 1)
        end = np.stack([sx + R_.randn(70) * 9, sy + R_.randn(70) * 9], 1)
        e = ease(k); p = start + (end - start) * e
        if k < 1: swarm.append(p)
        else:
            d.ellipse([sx - 24, sy - 24, sx + 24, sy + 24], fill=SIG if EP.current(t) == "reveal" else INK)
            g.append(("c", sx, sy, 26))
    for p in swarm: dots(img, p, INK, size=4)
    if g and EP.current(t) != "reveal": glow(img, g, r=16, k=.5)
    for j, tk in enumerate(T_LAB):                             # "A joke. A touch. A nod."
        if tk <= t < T_BACK and good_k(t, j) > .9:
            sx, sy = slot(Rr, j); k = spring((t - tk) / .35)              # the label pops up above its ball
            if k > .05: d.text((sx, sy - 60 - 40 * j - 20 * (1 - k)), LABELS[j], font=F(BLK, max(8, int(32 * min(1.2, k)))), fill=INK, anchor="mm")
    # headline + live ratio
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    ng = sum(1 for i in range(5) if good_k(t, i) > .6); nb = 1 if kb > .6 else 0
    d.text((X0, 400), "GOOD : BAD", font=F(MONO, 30), fill=MID)
    d.text((X0 + 210, 388), f"{ng} : {nb}", font=F(BLK, 64), fill=SIG if EP.current(t) == "reveal" else INK)
    if sub: d.text((X1, 408), sub, font=F(MONO, 26), fill=MID, anchor="ra")
    fig(d, note)

def sc_hook(img, d, t): draw(img, d, t, "ONE FIGHT.", note="schematic")
def sc_setup(img, d, t): draw(img, d, t, "FILMED. FOLLOWED.", sub="years later")
def sc_reveal(img, d, t): draw(img, d, t, "LASTING: 5 : 1", sub="even mid-fight")
def sc_split(img, d, t): draw(img, d, t, "NEAR A SPLIT: 1 : 1", sub="or less")
def sc_why(img, d, t): draw(img, d, t, "THEY ADD UP." if t < T_BACK else "ONE FIGHT.", note="exact ratio debated · Gottman 1994")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.bg = {"hook": "light", "setup": "light", "reveal": "orange", "split": "light", "why": "light"}
EP.scenes = {"hook": sc_hook, "setup": sc_setup, "reveal": sc_reveal, "split": sc_split, "why": sc_why}
FX = [(T_BAD, whoosh(.4, .05), 0), (T_BAD + .35, thud(.6), -.4), *[(x + .45, pop(.1), .4) for x in T_G],
      (S("reveal") + .1, thud(.5), 0), *[(x, whoosh(.3, .03), .4) for x in T_GONE], (T_GONE[-1] + .5, thud(.4), -.4),
      *[(x + .3, pop(.12), .3) for x in T_LAB], (T_BACK, whoosh(.5, .05), 0)]
if __name__ == "__main__": EP.run(FX)
