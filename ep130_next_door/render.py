"""NOT JUST YOU – No. 130: proximity – in Westgate West (MIT student housing, Festinger, Schachter & Back 1950) 41 % of
next-door neighbors became friends, 22 % two doors apart, 10 % at opposite ends of the hall.
Level 2 + fx2 + CLARITY rules (13.11.2026): slower voice, the picture is explained once ("Each box is one apartment"),
one number at a time. Isometric hallway of 8 apartments from frame 0 with people walking by (PARTICLES); CAMERA starts on your
door, pulls out, arcs of friendship grow from your door with a spring, the neighbors' doors GLOW; orange reveal; loop."""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from fx2 import camera, cam_path, glow, dots, Stream
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .5, "setup": .5, "explain": .5, "reveal": .8, "far": .6, "why": .1})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "setup", "explain", "reveal", "far", "why", "end"]
EP = ThreadEpisode(TL, 130, "NEXT DOOR", order=ORDER, dark=True, label="FIELD STUDY · STUDENT HOUSING · 1950",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Festinger, Schachter & Back (1950), Social Pressures", "in Informal Groups (Westgate West, MIT)"),
                   music=dict(bpm=92, root=0, prog="dream", kick="half", audio="v5"),
                   cover=dict(words=["YOUR FRIENDS", "LIVE CLOSER", "THAN YOU THINK."], kicker="41 % of next-door neighbors became friends."))

I = Iso(150, 610, .9)
N, STEP, A_, B_, HH = 8, 130, 110, 110, 80
YOU = 2
PCT = {1: 41, 3: 41, 0: 22, 4: 22, 7: 10}
def door(i, z=25): return I.P(i * STEP + 55, B_, z)

T_YOU = cue("explain", "You live here") - .1
T41 = cue("reveal", "forty-one") - .2
T22, T10 = cue("far", "twenty-two") - .15, cue("far", "only ten") - .15
T_BACK = cue("why", "That's why") - .35
WALK = Stream([I.P(-20, 165, 0), I.P(N * STEP, 165, 0)], n=26, width=40, seed=2)

def arc(d, a, b, k, w, col, lift):
    """friendship arc from a to b, grown to fraction k"""
    if k <= 0: return
    c = ((a[0] + b[0]) / 2, min(a[1], b[1]) - lift); pts = []
    for j in range(int(30 * min(1, k)) + 1):
        u = j / 30
        pts.append(((1 - u) ** 2 * a[0] + 2 * (1 - u) * u * c[0] + u * u * b[0], (1 - u) ** 2 * a[1] + 2 * (1 - u) * u * c[1] + u * u * b[1]))
    if len(pts) > 1: d.line(pts, fill=col, width=w, joint="curve")

def arc_k(t, i):
    back = clamp((t - T_BACK) / .35) if t >= T_BACK else 0
    tk = T41 if PCT[i] == 41 else T22 if PCT[i] == 22 else T10
    return spring((t - tk) / .6, f=1.2, damp=6) * (1 - back)

def scene(L, d, t):
    I.grid(L)
    I.poly(d, [I.P(-20, 120, 0), I.P(N * STEP, 120, 0), I.P(N * STEP, 210, 0), I.P(-20, 210, 0)], RULE)     # the hallway floor
    for i in range(N):
        wave = (t - .05) / .9; up = 14 * max(0, 1 - abs(i / (N - 1) - wave) * 4) if 0 <= wave <= 1.4 else 0  # cold open ripple
        I.box(d, i * STEP, 0, up, A_, B_, HH, top=INK if (i == YOU and t >= T_YOU and t < T_BACK + .3) else TOP)
        dq = [I.P(i * STEP + 40, B_, up), I.P(i * STEP + 70, B_, up), I.P(i * STEP + 70, B_, up + 55), I.P(i * STEP + 40, B_, up + 55)]
        d.polygon(dq, fill=INK if i == YOU else MID)
    xy = WALK.pos(t, flow=.06, active=1.0)                      # neighbors walking up and down the hall
    dots(L, xy, MID, size=10)
    if T_YOU <= t < T_BACK + .3:
        p = I.P(YOU * STEP + 55, 55, HH); callout(d, p, "l", p[1] - 110, 1, "YOU", INK, k=(t - T_YOU) / .4)
    g = []
    for i, pct in PCT.items():                                  # friendship arcs from your door
        k = arc_k(t, i)
        if k <= 0: continue
        a, b = door(YOU, 60), door(i, 60); lift = 70 + 28 * abs(i - YOU)
        arc(d, a, b, k, max(3, int(pct / 3)), SIG if (EP.current(t) == "reveal" and pct == 41) else INK, lift)
        if k > .8:
            q = I.P(i * STEP + 55, 55, HH); d.text((q[0], q[1] - 30), f"{pct} %", font=F(BLK, 40), fill=INK, anchor="mm")   # on the roof
            if pct == 41 and EP.current(t) != "reveal": g.append([I.P(i * STEP + 40, B_, 0), I.P(i * STEP + 70, B_, 0), I.P(i * STEP + 70, B_, 55), I.P(i * STEP + 40, B_, 55)])
    if g: glow(L, g, r=16, k=.7)

def cam(t):
    you = I.P(YOU * STEP + 55, 80, 40); mid = I.P(N * STEP / 2, 80, 40); near = I.P(YOU * STEP + 120, 80, 40)
    keys = [(0, 2.1, you), (S("setup") - .2, 2.0, you), (S("setup") + 1.2, 1.0, mid), (T41 - .3, 1.0, mid), (T41 + .8, 1.3, near),
            (T22 - .4, 1.3, near), (T22 + .6, 1.0, mid), (T_BACK, 1.0, mid), (T_BACK + .8, 2.1, you)]
    return cam_path(t, keys)

def head(d, t, line, sub=None):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    cur = EP.current(t)
    if cur in ("reveal", "far") or (cur == "why" and t < T_BACK):
        v = 41 if t < T22 else 22 if t < T10 else 10
        d.text((X0, 400), "BECAME FRIENDS", font=F(MONO, 30), fill=MID); d.text((X0 + 300, 388), f"{v} %", font=F(BLK, 64), fill=SIG if cur == "reveal" else INK)
    else:
        d.text((X0, 400), "APARTMENTS", font=F(MONO, 30), fill=MID); d.text((X0 + 230, 388), f"{N}", font=F(BLK, 64), fill=INK)
    if sub: d.text((X1, 408), sub, font=F(MONO, 26), fill=MID, anchor="ra")

def draw(img, d, t, line, sub=None, note="one hallway of the housing block · schematic"):
    z, f = cam(t); camera(img, lambda L, dL: scene(L, dL, t), z, f); head(d, t, line, sub); fig(d, note)

def sc_hook(img, d, t): draw(img, d, t, "YOUR NEIGHBORS.")
def sc_setup(img, d, t): draw(img, d, t, "STUDENT HOUSING", sub="1950")
def sc_explain(img, d, t): draw(img, d, t, "1 BOX = 1 APARTMENT")
def sc_reveal(img, d, t): draw(img, d, t, "NEXT DOOR: 41 %", note="share of neighbors named as friends")
def sc_far(img, d, t): draw(img, d, t, "FURTHER = FEWER", note="share of neighbors named as friends")
def sc_why(img, d, t): draw(img, d, t, "WHO YOU RUN INTO." if t < T_BACK else "YOUR NEIGHBORS.", note="one housing study · a classic, not the last word")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.bg = {k: "dark" for k in ORDER[:-1]}; EP.bg["reveal"] = "orange"
EP.scenes = {"hook": sc_hook, "setup": sc_setup, "explain": sc_explain, "reveal": sc_reveal, "far": sc_far, "why": sc_why}
FX = [(.05, whoosh(.8, .04), 0), (S("setup") - .1, whoosh(.9, .05), 0), (T_YOU, pop(.12), -.3),
      (S("reveal") + .1, thud(.55), 0), (T41 + .2, pop(.14), .2), (T22 + .2, pop(.12), .3), (T10 + .2, tick(.05), .5),
      (T_BACK, whoosh(.6, .05), 0)]
from fx2 import hook_intro
hook_intro(EP)                                                  # big hook in the first 1.7 s (13.11.2026)
if __name__ == "__main__": EP.run(FX)
