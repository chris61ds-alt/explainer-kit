"""NOT JUST YOU – No. 156: all the gold in the world as one cube ('pour test' riddle, 25.11.2026).
World Gold Council: about 224,200 t above ground (end-Q3 2026), ~US$30 tn. 224,200 / 19.32 = 11,600 m3 -> edge 22.6 m.
Riddle structure (rule 17), dark look. ONE scene in an oblique 3D view (1 m = 17 px): an empty dashed cube; ring, coin and bar
pop in; countdown; a dashed MOUNTAIN (the gut answer) collapses into the real cube with '22.6 m' labels, a 7-storey building
and a person for scale; gold pours in and fills the cube from the bottom; two tennis courts appear under it; a shine sweeps
over the full cube in the payoff (rule 15)."""
import os, sys, math
import numpy as np
from PIL import ImageDraw
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from fx2 import light_look
from stand import dashed, stamp_box, payoff_cam
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .4, "rules": .4, "lock": .7, "gut": .5, "reveal": .85, "pour": .5, "value": .5, "why": .1}, pace="loose")
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "rules", "lock", "gut", "reveal", "pour", "value", "why", "end"]
EP = ThreadEpisode(TL, 156, "ALL THE GOLD", order=ORDER, dark=True, label="RIDDLE · WORLD GOLD COUNCIL 2026",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("World Gold Council (2026), How much gold", "has been mined? · 224,200 t above ground"),
                   music=dict(bpm=96, root=7, prog="major", kick="four", audio="v5"),
                   cover=dict(words=["ALL THE GOLD", "IN THE WORLD.", "HOW BIG?"], kicker="Lock in your answer."))
light_look(EP, ORDER)                                          # rule 16 (25.11.2026): light paper + shadows, reveal on black

GOLD, GSIDE, GTOP = (226, 176, 60), (186, 140, 44), (246, 210, 120)   # light look (rule 16): top brightest, side darkest
A = 22.6; SC = 17; OX, OY = 170, 1120
def P(x, y, z): return OX + x * SC + z * SC * .5, OY - y * SC - z * SC * .35

T_ICONS = [cue("rules", "ring") - .1, cue("rules", "coin") - .1, cue("rules", "bar") - .1]; T_TON = cue("rules", "Two hundred") - .1
T_LOCK = S("lock"); T_321 = [cue("lock", "Three") - .05, cue("lock", "Two") - .05, cue("lock", "One") - .05]
T_MTN = S("gut") - .1; T_REAL = S("reveal") + .05; T_M = cue("reveal", "twenty-three") - .15; T_BLD = cue("reveal", "seven-story") - .15
T_P0, T_P1 = S("pour") - .3, E("pour") + .3; T_COURT = cue("pour", "two tennis") - .15
T_USD = S("value"); T_SHINE = S("why")
T_OUT = S("rules") - .2                                            # 25.11.2026 (rule 11): ring -> drop -> 'ALL OF IT?', then the cube

def ring_intro(d, t):
    if t >= T_OUT + .5: return
    out = ease_io(clamp((t - T_OUT) / .5)); x = 540; y = 640 + 300 * ease(clamp((t - .1) / .5))
    melt = ease_io(clamp((t - .8) / .6))
    if melt < 1:                                                                 # the ring
        r_ = 70 * (1 - melt); d.ellipse([x - r_, y - r_ * (1 - .5 * melt), x + r_, y + r_], outline=GOLD, width=max(1, int(18 * (1 - melt))))
    if melt > 0:                                                                 # the drop, then it flies into the cube
        tx, ty = P(A / 2, A / 2, 0); X, Y = x + (tx - x) * out, y + (ty - y) * out; s = 75 * melt * (1 - .7 * out)
        d.ellipse([X - s, Y - s * .8, X + s, Y + s], fill=GOLD); d.polygon([(X - s * .6, Y - s * .3), (X + s * .6, Y - s * .3), (X, Y - s * 1.7)], fill=GOLD)
    if 1.4 <= t < T_OUT: stamp_box(d, (720, 1060), "ALL OF IT?", t, 1.4, size=70)

def poly(d, pts, fill): d.polygon([P(*p) for p in pts], fill=fill)

def wire(d, col, solid):
    c = [(0, 0, 0), (A, 0, 0), (A, A, 0), (0, A, 0), (0, 0, A), (A, 0, A), (A, A, A), (0, A, A)]
    E_ = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]
    for i, j in E_:
        a, b = P(*c[i]), P(*c[j])
        if solid: d.line([a, b], fill=col, width=3)
        else: dashed(d, a, b, col, w=3, dash=16, gap=12)

def courts(d, k, lines_only=False):
    if k <= 0: return
    col = mix(BG, (60, 130, 90), k); ln = mix(BG, INK, .8 * k)
    W, L = 10.97, 23.77; x0 = (A - L) / 2; z0 = (A - 2 * W) / 2
    for c in range(2):
        zz = z0 + c * W
        if not lines_only: poly(d, [(x0, 0, zz), (x0 + L, 0, zz), (x0 + L, 0, zz + W), (x0, 0, zz + W)], col)
        for a, b in (((x0, 0, zz), (x0 + L, 0, zz)), ((x0 + L, 0, zz), (x0 + L, 0, zz + W)), ((x0 + L, 0, zz + W), (x0, 0, zz + W)),
                     ((x0, 0, zz + W), (x0, 0, zz)), ((x0 + L / 2, 0, zz), (x0 + L / 2, 0, zz + W))):
            d.line([P(*a), P(*b)], fill=ln, width=2)

def fill(d, h, t):
    if h <= 0: return
    poly(d, [(A, 0, 0), (A, 0, A), (A, h, A), (A, h, 0)], GSIDE)                     # right side
    poly(d, [(0, 0, 0), (A, 0, 0), (A, h, 0), (0, h, 0)], GOLD)                      # front
    poly(d, [(0, h, 0), (A, h, 0), (A, h, A), (0, h, A)], GTOP)                      # top
    R = np.random.RandomState(int(t * 30) % 7)                                       # sandy sparkle on the front
    for _ in range(140):
        x, y = R.uniform(0, A), R.uniform(0, h); px, py = P(x, y, 0)
        d.point((px, py), fill=GTOP)
    if T_SHINE <= t:                                                                  # payoff: a shine sweeps across
        u = ((t - T_SHINE) / 1.6) % 1.6
        if u < 1:
            x = -4 + (A + 8) * u
            pts = [(x, 0, 0), (x + 2.5, 0, 0), (x + 2.5 + 3, h, 0), (x + 3, h, 0)]
            pts = [(min(max(a, 0), A), b, c) for a, b, c in pts]
            poly(d, pts, (255, 238, 180))

def stream(d, t, h):
    if not (T_P0 <= t < T_P1 + .4): return
    R = np.random.RandomState(int(t * 30))
    x0, y0 = P(A / 2, A * 1.9, A / 2); x1, y1 = P(A / 2, h, A / 2)
    for _ in range(160):
        u = R.uniform(); x = x0 + (x1 - x0) * u + R.normal(0, 6 + 10 * u); y = y0 + (y1 - y0) * u
        d.rectangle([x - 1.5, y - 1.5, x + 1.5, y + 1.5], fill=GOLD)

def building(d, k):
    if k <= 0: return
    x0, x1 = 820, 980; top = OY - 22.4 * SC * k
    d.rectangle([x0, top, x1, OY], fill=mix(BG, MID, .35))
    for f in range(7):
        y = OY - (f + 1) * 3.2 * SC * k + 14
        if y < top + 6: continue
        for wx in range(x0 + 16, x1 - 20, 34): d.rectangle([wx, y, wx + 18, y + 26 * k], fill=mix(BG, INK, .25))
    if k > .9: d.text(((x0 + x1) / 2, top - 24), "7 STOREYS", font=F(MONO, 22), fill=MID, anchor="mm")

def person(d):
    x, y = 770, OY; h = 1.8 * SC
    d.ellipse([x - 4, y - h - 4, x + 4, y - h + 4], fill=INK); d.line([(x, y - h + 4), (x, y)], fill=INK, width=4)

def icons(d, t):
    for i, t0 in enumerate(T_ICONS):
        if not (t0 <= t < T_LOCK): continue
        k = spring(clamp((t - t0) / .4)); x = 380 + i * 160; y = 640
        if i == 0: d.ellipse([x - 34 * k, y - 34 * k, x + 34 * k, y + 34 * k], outline=GOLD, width=int(10 * k) + 1)
        elif i == 1: d.ellipse([x - 38 * k, y - 38 * k, x + 38 * k, y + 38 * k], fill=GOLD); d.ellipse([x - 26 * k, y - 26 * k, x + 26 * k, y + 26 * k], outline=GSIDE, width=3)
        else: d.polygon([(x - 50 * k, y + 22 * k), (x + 50 * k, y + 22 * k), (x + 34 * k, y - 22 * k), (x - 34 * k, y - 22 * k)], fill=GOLD)

def mountain(d, t):
    if not (T_MTN <= t < T_REAL + .5): return
    k = ease(clamp((t - T_MTN) / .5)) * (1 - ease_io(clamp((t - T_REAL) / .5)))
    if k <= .02: return
    peak = (540, OY - 640 * k); L, R_ = (540 - 620 * k, OY), (540 + 620 * k, OY)
    for a, b in ((L, peak), (peak, R_)): dashed(d, a, b, mix(BG, SIG, k), w=4)
    if k > .7: d.text((540, OY - 680 * k), "A MOUNTAIN?", font=F(BLK, 40), fill=SIG, anchor="mm")

def countdown(d, t):
    if not (T_LOCK <= t < S("gut")): return
    d.rounded_rectangle([290, 640, 790, 1040], radius=40, fill=BG)
    d.text((540, 690), "LOCK IN YOUR ANSWER", font=F(BLK, 38), fill=INK, anchor="mm")
    i = sum(1 for x in T_321 if t >= x)
    ring = clamp((t - T_321[0]) / (T_321[2] + .7 - T_321[0])) if t >= T_321[0] else 0
    d.ellipse([420, 750, 660, 990], outline=mix(BG, MID, .6), width=12)
    if ring > 0: d.arc([420, 750, 660, 990], -90, -90 + 360 * (1 - ring), fill=SIG, width=12)
    d.text((540, 870), ["?", "3", "2", "1"][i], font=F(BLK, 130), fill=INK, anchor="mm")

def head(d, line, label=None, val=None, hot=False):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    if label:
        d.text((X0, 400), label, font=F(MONO, 30), fill=MID)
        d.text((X0 + d.textlength(label, font=F(MONO, 30)) + 24, 388), val, font=F(BLK, 56), fill=GOLD if hot else INK)

def sc(img, d, t):
    payoff_cam(img, lambda L, dL: sc_full(L, dL, t), t, S("why"), focus=(420, 880), z1=1.12, ep=EP)

def sc_full(img, d, t):
    cur = EP.current(t)
    d.line([(40, OY), (1040, OY)], fill=mix(BG, MID, .5), width=3)
    real = t >= T_REAL
    courts(d, ease(clamp((t - T_COURT) / .5)) if t >= T_COURT else 0)
    h = A * ease_io(clamp((t - T_P0) / (T_P1 - T_P0))) if t >= T_P0 else 0
    if t < T_OUT: ring_intro(d, t); icons(d, t); countdown(d, t); head(d, "ALL THE GOLD.", "CUBE SIZE", "?"); fig(d, "above-ground stocks, end Q3 2026 (rounded) · 1 m = 17 px"); return
    ring_intro(d, t)
    if real: wire(d, mix(BG, INK, .35), False)
    fill(d, h, t); stream(d, t, h)
    if t >= T_COURT: courts(d, ease(clamp((t - T_COURT) / .5)), lines_only=True)   # x-ray: the courts under the gold
    if real: wire(d, mix(BG, INK, .9), True)
    else: wire(d, mix(BG, MID, .7), False)
    if real:
        building(d, ease(clamp((t - T_BLD) / .6)) if t >= T_BLD else 0); person(d)
        if t >= T_M:
            k = ease(clamp((t - T_M) / .4))
            a, b = P(0, -1.6, 0), P(A, -1.6, 0); d.line([a, b], fill=mix(BG, GOLD, k), width=3)
            d.text(((a[0] + b[0]) / 2, a[1] + 26), "22.6 m", font=F(BLK, 30), fill=mix(BG, GOLD, k), anchor="mm")
            a, b = P(-1.4, 0, 0), P(-1.4, A, 0); d.line([a, b], fill=mix(BG, GOLD, k), width=3)
            d.text((a[0] - 12, (a[1] + b[1]) / 2), "22.6 m", font=F(BLK, 30), fill=mix(BG, GOLD, k), anchor="rm")
    else:
        x, y = P(A / 2, A / 2, 0); d.text((x, y), "?", font=F(BLK, 160), fill=mix(BG, MID, .6), anchor="mm")
    icons(d, t); mountain(d, t); countdown(d, t)
    if cur == "hook": head(d, "ALL THE GOLD.", "CUBE SIZE", "?")
    elif cur == "rules": head(d, "EVERY RING, EVER.", "TONNES", f"{int(224200 * ease_io(clamp((t - T_TON) / 1.2))):,}", True)
    elif cur == "lock": head(d, "LOCK IT IN.", "CUBE SIZE", "?")
    elif cur == "gut": head(d, "A MOUNTAIN?", "CUBE SIZE", "?")
    elif cur == "reveal": head(d, "22.6 METERS.", "CUBE SIZE", "22.6 m" if t >= T_M else "?", True)
    elif cur == "pour": head(d, "2 TENNIS COURTS.", "FILLED", f"{int(100 * h / A)}%", True)
    elif cur == "value": head(d, "WORTH ~$30 TRILLION.", "VALUE", f"${30 * ease_io(clamp((t - T_USD) / 1.0)):.0f} TN", True)
    else: head(d, "SO LITTLE.", "ALL GOLD ABOVE GROUND", "224,200 t", True)
    fig(d, "above-ground stocks, end Q3 2026 (rounded) · 1 m = 17 px")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.scenes = {k: sc for k in ORDER[:-1]}
FX = [(.1, whoosh(.4, .02), 0), (.6, thud(.18), 0), (1.4, thud(.2), .2), (T_OUT, whoosh(.5, .02), 0), *[(x, pop(.1), -.4 + i * .4) for i, x in enumerate(T_ICONS)], *[(x, thud(.16), 0) for x in T_321],
      (T_MTN, whoosh(.5, .02), 0), (T_REAL, thud(.22), 0), (T_BLD, pop(.08), .5), (T_P0, whoosh(1.4, .02), 0), (T_COURT, pop(.08), 0),
      (T_USD, pop(.1), 0), (T_SHINE, whoosh(.4, .015), .3)]
if __name__ == "__main__": EP.run(FX)
