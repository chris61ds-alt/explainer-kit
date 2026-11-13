"""NOT JUST YOU – No. 133: happiness spreads – Framingham Heart Study, 4,739 people over 20 years: a friend within a mile who
becomes happy raises your chance of being happy by ~25 %; clusters reach up to 3 degrees (Fowler & Christakis 2008, BMJ).
FIRST EPISODE IN THE NEW LIGHT LOOK (13.11.2026): paper + soft shadows (fx2.soft_shadow), reveal on black (fx2.light_look),
clarity rules (slow voice, the picture explained once). Isometric neighbourhood of 16 houses from frame 0 (ripple); a happy
house = dark roof + a ring wave on the ground; PARTICLES flow from the friend to you on the reveal; then it spreads 1-2-3 steps
(houses 4 steps away stay as they are); CAMERA starts on the friend, pulls out; loop: all roofs back to normal."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from fx2 import camera, cam_path, glow, dots, Stream, soft_shadow, light_look, is_light
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .5, "setup": .5, "explain": .5, "reveal": .8, "spread": .6, "why": .1})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "setup", "explain", "reveal", "spread", "why", "end"]
EP = ThreadEpisode(TL, 133, "HAPPY SPREAD", order=ORDER, dark=True, label="LONG-TERM STUDY · 4,739 PEOPLE",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Fowler & Christakis (2008), Dynamic spread of happiness", "in a large social network, BMJ 337:a2338"),
                   music=dict(bpm=100, root=2, prog="major", kick="four", audio="v5"),
                   cover=dict(words=["YOUR FRIEND", "GETS HAPPIER.", "SO DO YOU."], kicker="+25 %. And it spreads 3 steps."))
light_look(EP, ORDER)

I = Iso(540, 600, .8)
G, STEP, A_, B_, HW, RF = 4, 170, 110, 110, 80, 50
HOUSES = [(c, r) for r in range(G) for c in range(G)]
FRIEND, YOU = (1, 1), (2, 1)
def xy(h): return h[0] * STEP, h[1] * STEP
def dist(h): return abs(h[0] - FRIEND[0]) + abs(h[1] - FRIEND[1])

T_FR = cue("hook", "gets happier") - .1
T_YOU0 = cue("hook", "you probably") - .1
T_LAB = cue("explain", "This is you") - .1; T_LAB2 = cue("explain", "This is a friend") - .1
T25 = cue("reveal", "twenty-five") - .2
T_SP = [cue("spread", "three steps") - .1 + j * .7 for j in range(3)]
T_BACK = cue("why", "That's why") - .35
px, py = xy(FRIEND); yx, yy = xy(YOU)
FLOW = Stream([I.P(px + A_, py + 55, 20), I.P((px + A_ + yx) / 2, py + 55, 60), I.P(yx, yy + 55, 20)], n=500, width=16, seed=3)

def happy(t, h):
    """0..1: how happy (dark roof) house h is at time t"""
    if t >= T_BACK: return 0
    if h == FRIEND: return spring((t - T_FR) / .5) if t >= T_FR else 0
    if h == YOU and T_YOU0 <= t < S("setup") - .2: return spring((t - T_YOU0) / .5) * .9      # the hook's promise, briefly
    if h == YOU and t >= T25: return spring((t - T25) / .5)
    dd = dist(h)
    if 1 <= dd <= 3 and t >= T_SP[dd - 1]: return spring((t - T_SP[dd - 1] - (h[0] + h[1]) * .04) / .5)
    return 0

def house(d, x, y, k, up):
    I.box(d, x, y, up, A_, B_, HW)
    P = I.P; apex = P(x + A_ / 2, y + B_ / 2, HW + RF + up)
    I.poly(d, [P(x, y + B_, HW + up), P(x + A_, y + B_, HW + up), apex], mix(LEFT, INK, .85 * clamp(k)))
    I.poly(d, [P(x + A_, y, HW + up), P(x + A_, y + B_, HW + up), apex], mix(RIGHT, INK, .7 * clamp(k)))
    d.polygon([P(x + A_, y + 40, up), P(x + A_, y + 70, up), P(x + A_, y + 70, 46 + up), P(x + A_, y + 40, 46 + up)], fill=MID)

def ring(d, h, t0, t):
    """a ring wave on the ground when a house turns happy"""
    dt = t - t0
    if not 0 <= dt < .9: return
    x, y = xy(h); cx, cy = x + A_ / 2, y + B_ / 2; r = 60 + 160 * ease(dt / .9); n = 36
    pts = [I.P(cx + r * math.cos(a * 2 * math.pi / n), cy + r * math.sin(a * 2 * math.pi / n), 0) for a in range(n + 1)]
    d.line(pts, fill=mix(MID, BG, ease(dt / .9)), width=4)

def scene(L, d, t):
    I.grid(L)
    if is_light(EP, t): soft_shadow(L, I, [(*xy(h), A_, B_, HW + RF * .6) for h in HOUSES], r=14, k=.38)
    for h, tk in ((FRIEND, T_FR), (YOU, T25)) + tuple((hh, T_SP[dist(hh) - 1]) for hh in HOUSES if 1 <= dist(hh) <= 3):
        ring(d, h, tk, t)
    for h in sorted(HOUSES, key=lambda h: h[0] + h[1]):
        x, y = xy(h); wave = (t - .05) / .9
        up = 12 * max(0, 1 - abs((h[0] + h[1]) / 6 - wave) * 4) if 0 <= wave <= 1.4 else 0     # cold open ripple
        house(d, x, y, happy(t, h), up)
    if T25 - .3 <= t < T_BACK:                                  # the good mood flows from the friend to you
        dots(L, FLOW.pos(t, flow=.5, active=min(1, (t - T25 + .3) / .6)), INK, size=5)
    for h, lab, tk in ((YOU, "YOU", T_LAB), (FRIEND, "FRIEND", T_LAB2)):
        if tk <= t < T_BACK + .2:
            x, y = xy(h); p = I.P(x + A_ / 2, y + B_ / 2, HW + RF)
            callout(d, p, "r" if h == YOU else "l", p[1] - 90, 1, lab, INK, k=(t - tk) / .4)
    if S("spread") <= t < T_BACK:                               # step numbers on the ground
        for j, tk in enumerate(T_SP):
            if t >= tk:
                hh = [h for h in HOUSES if dist(h) == j + 1][-1]; x, y = xy(hh); p = I.P(x + A_ + 20, y + B_ + 20, 0)
                k = spring((t - tk) / .4); d.text((p[0], p[1] + 10 * (1 - k)), f"{j + 1}", font=F(BLK, int(max(8, 40 * min(1.2, k)))), fill=INK, anchor="mm")

def cam(t):
    fr = I.P(px + A_ / 2, py + B_ / 2, 60); both = I.P((px + yx) / 2 + A_ / 2, py + B_ / 2, 60); mid = I.P(255 + 55, 255 + 55, 40)
    keys = [(0, 1.5, fr), (S("setup") - .2, 1.45, both), (S("setup") + 1.0, 1.0, mid), (T_LAB - .3, 1.0, mid), (T_LAB + .6, 1.45, both),
            (T25 + 1.0, 1.45, both), (S("spread") + .2, 1.0, mid), (T_BACK, 1.0, mid), (T_BACK + .7, 1.5, fr)]
    return cam_path(t, keys)

def head(d, t, line, sub=None):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    cur = EP.current(t)
    if T25 <= t < S("spread"):
        v = 25 * ease(clamp((t - T25) / .8))
        d.text((X0, 400), "CHANCE OF BEING HAPPY", font=F(MONO, 30), fill=MID); d.text((X0 + 430, 388), f"+{v:.0f} %", font=F(BLK, 64), fill=SIG)
    elif S("spread") <= t < T_BACK:
        n = sum(1 for x in T_SP if t >= x)
        d.text((X0, 400), "STEPS", font=F(MONO, 30), fill=MID); d.text((X0 + 130, 388), f"{n}", font=F(BLK, 64), fill=INK)
    else:
        d.text((X0, 400), "PEOPLE FOLLOWED", font=F(MONO, 30), fill=MID); d.text((X0 + 320, 388), "4,739", font=F(BLK, 64), fill=INK)
    if sub: d.text((X1, 470), sub, font=F(MONO, 26), fill=MID, anchor="ra")

def draw(img, d, t, line, sub=None, note="schematic neighbourhood"):
    z, f = cam(t); camera(img, lambda L, dL: scene(L, dL, t), z, f); head(d, t, line, sub); fig(d, note)

def sc_hook(img, d, t): draw(img, d, t, "GOOD MOOD.")
def sc_setup(img, d, t): draw(img, d, t, "20 YEARS", sub="1983 – 2003")
def sc_explain(img, d, t): draw(img, d, t, "1 HOUSE = 1 PERSON", note="dark roof = happy")
def sc_reveal(img, d, t): draw(img, d, t, "FRIEND NEARBY: +25 %", note="friend within a mile · wide margin of error")
def sc_spread(img, d, t): draw(img, d, t, "UP TO 3 STEPS", note="4 steps away: no effect found")
def sc_why(img, d, t): draw(img, d, t, "YOUR MOOD TRAVELS." if t < T_BACK else "GOOD MOOD.", note="observational · a link, not proof")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.scenes = {"hook": sc_hook, "setup": sc_setup, "explain": sc_explain, "reveal": sc_reveal, "spread": sc_spread, "why": sc_why}
FX = [(.05, whoosh(.8, .04), 0), (T_FR, pop(.14), -.2), (T_YOU0, pop(.1), .2), (S("setup") - .1, whoosh(.8, .05), 0),
      (T_LAB, pop(.12), .3), (T_LAB2, pop(.12), -.3), (S("reveal") + .1, thud(.55), 0), (T25, riser(.7, .04), 0), (T25 + .5, pop(.16), .2),
      *[(x, pop(.12), -.4 + j * .4) for j, x in enumerate(T_SP)], (T_BACK, whoosh(.6, .05), 0)]
if __name__ == "__main__": EP.run(FX)
