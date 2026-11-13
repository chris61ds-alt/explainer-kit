"""NOT JUST YOU – No. 131: the spotlight effect – students in an embarrassing T-shirt guessed that ~46 % of the room noticed,
~23 % actually did (Gilovich, Medvec & Savitsky 2000).
Level 2 + fx2 + CLARITY rules: top-down room, the picture is explained once ("Each dot is one person"). A spotlight (GLOW)
swings onto you in the cold open; the CAMERA pulls out; the guess = 11 people turn and look (gaze lines), the reality = only
6 still look; then everyone gets their own little spotlight. Orange reveal, loop."""
import os, sys, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from fx2 import camera, cam_path, glow
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .5, "setup": .5, "explain": .5, "guess": .5, "reveal": .8, "why": .1})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "setup", "explain", "guess", "reveal", "why", "end"]
EP = ThreadEpisode(TL, 131, "SPOTLIGHT", order=ORDER, dark=True, label="EXPERIMENT · STUDENTS",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Gilovich, Medvec & Savitsky (2000), The spotlight effect", "in social judgment, JPSP 78(2)"),
                   music=dict(bpm=98, root=1, prog="major", kick="four", audio="v5"),
                   cover=dict(words=["NOBODY", "NOTICED YOUR", "SHIRT."], kicker="Well, about 1 in 4 did."))

C = (540, 830); SP = 150
SEATS = [(C[0] + (c - 2) * SP, C[1] + (r - 2) * SP) for r in range(5) for c in range(5)]
YOU = 12; OTHERS = [i for i in range(25) if i != YOU]
R = random.Random(5); HEAD = {i: R.uniform(0, 2 * math.pi) for i in OTHERS}
order = OTHERS[:]; R.shuffle(order)
GUESS = set(order[:11]); REAL = set(order[:6])                     # 11 / 24 ≈ 46 %, 6 / 24 = 25 % (study: ~23 %)

T_SPOT = .1
T_YOU = cue("explain", "The bright one") - .1
T_G = cue("guess", "about half") - .2
T_R = cue("reveal", "one in four") - .2
T_ALL = cue("why", "Everyone else") - .1
T_BACK = cue("why", "So next time") - .35

def looking(t, i):
    """0..1: how much person i is turned toward you"""
    if t >= T_BACK: return 0
    if i in REAL and t >= T_G: return spring((t - T_G - order.index(i) * .06) / .4)
    if i in GUESS and T_G <= t: return spring((t - T_G - order.index(i) * .06) / .4) * (1 - ease(clamp((t - T_R) / .5)))
    return 0

def scene(L, d, t):
    I = None
    for i, (x, y) in enumerate(SEATS):                        # chairs / desks
        d.rounded_rectangle([x - 52, y - 40, x + 52, y + 40], radius=12, fill=RULE)
    g = []
    k_spot = ease(clamp((t - T_SPOT) / .8))                   # the spotlight swings in from the left (cold open)
    if t < T_BACK + .2 or True:
        sx = C[0] - 600 * (1 - k_spot); r_sp = 95 if t < T_ALL else 95 - 45 * ease(clamp((t - T_ALL) / .6))
        if t >= T_BACK: sx = C[0] + 0; r_sp = 95
        g.append(("c", sx, C[1], r_sp))
    if T_ALL <= t < T_BACK + .2:                              # everyone has their own spotlight
        k = ease(clamp((t - T_ALL) / .8)) * (1 - clamp((t - T_BACK) / .3))
        g += [("c", x, y, 50 * k) for j, (x, y) in enumerate(SEATS) if j != YOU and k > .05]
    if EP.current(t) != "reveal": glow(L, g, r=30, k=.55)        # on orange the bloom reads as a shadow
    for i in OTHERS:                                          # people + gaze
        x, y = SEATS[i]; lk = looking(t, i)
        to_you = math.atan2(C[1] - y, C[0] - x); a = HEAD[i] + (((to_you - HEAD[i] + math.pi) % (2 * math.pi)) - math.pi) * lk
        a += .25 * math.sin(t * 1.3 + i) * (1 - lk)            # idle: looking around at their own stuff
        d.ellipse([x - 22, y - 22, x + 22, y + 22], fill=MID if lk < .5 else INK)
        d.ellipse([x + 30 * math.cos(a) - 7, y + 30 * math.sin(a) - 7, x + 30 * math.cos(a) + 7, y + 30 * math.sin(a) + 7], fill=MID if lk < .5 else INK)
        if lk > .2:
            ex, ey = x + (C[0] - x) * .78 * min(1, lk), y + (C[1] - y) * .78 * min(1, lk)
            d.line([(x + 38 * math.cos(to_you), y + 38 * math.sin(to_you)), (ex, ey)], fill=SIG if EP.current(t) == "reveal" else INK, width=4)
    d.ellipse([C[0] - 30, C[1] - 30, C[0] + 30, C[1] + 30], fill=INK)   # you, in the shirt
    if T_YOU <= t < T_BACK + .2: callout(d, (C[0], C[1] - 30), "r", C[1] - 120, 1, "YOU", INK, k=(t - T_YOU) / .4)

def cam(t):
    keys = [(0, 1.9, C), (S("setup") - .1, 1.8, C), (S("explain") - .2, 1.0, C), (T_BACK, 1.0, C), (T_BACK + .7, 1.9, C)]
    return cam_path(t, keys)

def head(d, t, line, sub=None):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    if T_G <= t < T_BACK:
        d.text((X0, 400), "GUESSED", font=F(MONO, 30), fill=MID); d.text((X0 + 170, 388), "46 %", font=F(BLK, 64), fill=INK if t < T_R else MID)
        if t >= T_R: d.text((X0 + 420, 400), "REAL", font=F(MONO, 30), fill=MID); d.text((X0 + 520, 388), "23 %", font=F(BLK, 64), fill=SIG if EP.current(t) == "reveal" else INK)
    else:
        d.text((X0, 400), "PEOPLE IN THE ROOM", font=F(MONO, 30), fill=MID); d.text((X0 + 380, 388), "25", font=F(BLK, 64), fill=INK)
    if sub: d.text((X1, 470), sub, font=F(MONO, 26), fill=MID, anchor="ra")

def draw(img, d, t, line, sub=None, note="schematic room"):
    z, f = cam(t); camera(img, lambda L, dL: scene(L, dL, t), z, f); head(d, t, line, sub); fig(d, note)

def sc_hook(img, d, t): draw(img, d, t, "THAT SHIRT.")
def sc_setup(img, d, t): draw(img, d, t, "THE SHIRT TEST", sub="a real experiment")
def sc_explain(img, d, t): draw(img, d, t, "1 DOT = 1 PERSON")
def sc_guess(img, d, t): draw(img, d, t, "YOUR GUESS: HALF", note="what the shirt wearers guessed")
def sc_reveal(img, d, t): draw(img, d, t, "REALITY: 1 IN 4", note="who could actually name the shirt")
def sc_why(img, d, t): draw(img, d, t, "THEIR OWN SPOTLIGHT." if t < T_BACK else "THAT SHIRT.", note="one experiment · repeated in later studies")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.bg = {k: "dark" for k in ORDER[:-1]}; EP.bg["reveal"] = "orange"
EP.scenes = {"hook": sc_hook, "setup": sc_setup, "explain": sc_explain, "guess": sc_guess, "reveal": sc_reveal, "why": sc_why}
FX = [(T_SPOT, whoosh(.8, .05), -.6), (S("explain") - .2, whoosh(.7, .04), 0), (T_YOU, pop(.12), .3),
      *[(T_G + order.index(i) * .06, tick(.04), (SEATS[i][0] - 540) / 400) for i in GUESS],
      (S("reveal") + .1, thud(.55), 0), (T_R + .2, whoosh(.4, .04), 0), (T_ALL, riser(.8, .04), 0), (T_BACK, whoosh(.5, .05), 0)]
if __name__ == "__main__": EP.run(FX)
