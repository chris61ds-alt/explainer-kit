"""NOT JUST YOU – No. 138: everyone thinks they're in the middle – Hoy & Mager (2021, AEJ: Policy): >30,000 people in
10 countries; among the poorest two fifths 67–94 % overestimate their position; Hvidberg, Kreiner & Stantcheva (2023, REStud,
Denmark): people ranked higher think they rank lower ('center bias').
Light look (paper + soft shadows, reveal on black) + clarity rules ("Each dot is one person") + rule 13 opener.
ONE continuous object: a 5-step staircase (poorest left), 100 dots on their real step. Cold open: the dots jump from every
step onto the middle step, "THE MIDDLE" stamp; rewind; explain; the jump again on black; poor movers / rich movers marked;
loop: the dots jump back to their real steps (= frame 0)."""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from fx2 import light_look, is_light, stamp
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .5, "setup": .5, "explain": .5, "reveal": .6, "poor": .8, "rich": .6, "why": .1})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "setup", "explain", "reveal", "poor", "rich", "why", "end"]
EP = ThreadEpisode(TL, 138, "THE MIDDLE", order=ORDER, dark=True, label="SURVEYS · 10 COUNTRIES · 30,000+",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Hoy & Mager (2021), AEJ: Economic Policy ·", "Hvidberg, Kreiner & Stantcheva (2023), REStud"),
                   music=dict(bpm=100, root=0, prog="major", kick="four", audio="v5"),
                   cover=dict(words=["EVERYONE", "THINKS THEY'RE", "IN THE MIDDLE."], kicker="Where people think they stand."))
light_look(EP, ORDER, reveal=("reveal", "poor", "rich"))

# real step -> [(perceived step, n)]  (schematic; poorer two fifths: 31 of 40 = 77.5 % too high)
MOVE = {0: [(0, 4), (1, 5), (2, 9), (3, 2)], 1: [(1, 5), (2, 12), (3, 3)], 2: [(2, 16), (1, 2), (3, 2)],
        3: [(3, 10), (2, 10)], 4: [(4, 6), (3, 8), (2, 6)]}
DOTS = []                                         # (real step, perceived step)
for s in range(5):
    for p, n in MOVE[s]: DOTS += [(s, p)] * n
SX0, SW = 70, 188                                 # step i spans SX0 + i*SW .. + SW
def step_top(i): return 1080 - i * 92
PER_ROW, DR, GAP = 7, 10, 24

def slots():
    """pixel positions per dot for the real layout and the perceived layout"""
    real, perc = [], []
    nr, np_ = [0] * 5, [0] * 5
    for s, p in DOTS:
        for (lay, cnt, k) in ((real, nr, s), (perc, np_, p)):
            j = cnt[k]; cnt[k] += 1
            x = SX0 + k * SW + 22 + (j % PER_ROW) * GAP + (GAP / 2 if (j // PER_ROW) % 2 else 0)
            y = step_top(k) - DR - 2 - (j // PER_ROW) * (GAP - 3)
            lay.append((x, y))
    return real, perc
REAL_XY, PERC_XY = slots()

T_J0 = .35;                 D_J = 1.1                 # cold open: everyone jumps to the middle
T_STAMP = cue("hook", "the middle") - .05
T_REW = S("setup") - .05;   D_REW = .9
T_STEPS = S("explain") - .05; T_DOT = cue("explain", "Each dot") - .1
T_JUMP = S("reveal") + .05
T_POOR = S("poor") + .05; T_RICH = S("rich") + .05
T_BACK = E("why") - 1.15;   D_BACK = .95
MOVES = [(T_J0, D_J, 1), (T_REW, D_REW, 0), (T_JUMP, D_J, 1), (T_BACK, D_BACK, 0)]   # target: 1 = perceived, 0 = real

def dot_pos(i, t):
    cur_from, cur_to, k = 0, 0, 1.0
    for ts, dur, tgt in MOVES:
        if t < ts: break
        cur_from = cur_to; cur_to = tgt
        delay = (i % 17) * .025
        k = ease_io(clamp((t - ts - delay) / (dur * .75)))
    A = REAL_XY[i] if cur_from == 0 else PERC_XY[i]; B = REAL_XY[i] if cur_to == 0 else PERC_XY[i]
    x = A[0] + (B[0] - A[0]) * k; y = A[1] + (B[1] - A[1]) * k
    if A != B: y -= 150 * math.sin(math.pi * k)                    # a hop
    return x, y

def objects(L, d, t):
    cur = EP.current(t)
    for i in range(5):                                             # the staircase
        x0 = SX0 + i * SW; hot = cur == "explain" and t >= T_STEPS + i * .1
        d.rectangle([x0, step_top(i), x0 + SW - 8, 1150], fill=WHITE, outline=INK if hot else RULE, width=4 if hot else 2)
    for i, (s, p) in enumerate(DOTS):
        x, y = dot_pos(i, t)
        col = INK
        if cur == "explain" and t >= T_DOT: col = INK if s == 2 else MID
        if cur == "poor" and t >= T_POOR and s <= 1 and p > s: col = SIG
        if cur == "rich" and t >= T_RICH and s >= 3 and p < s: col = SIG
        if cur in ("poor", "rich") and col is INK: col = MID
        d.ellipse([x - DR, y - DR, x + DR, y + DR], fill=col)
    if t >= T_STEPS - .3 and t < T_BACK:                            # step labels
        d.text((SX0 + SW - 16, step_top(0) + 30), "POOREST", font=F(MONO, 22), fill=MID, anchor="ra")
        d.text((SX0 + 4 * SW + SW - 16, step_top(4) + 30), "RICHEST", font=F(MONO, 22), fill=MID, anchor="ra")

def shadowed(img, t):
    if not is_light(EP, t):
        objects(img, ImageDraw.Draw(img), t); return
    L = Image.new("RGB", img.size, BG); objects(L, ImageDraw.Draw(L), t)
    a = np.asarray(L, np.int16); m = (np.abs(a - np.array(BG)).max(axis=2) > 10).astype(np.uint8) * 255
    m[:470] = 0; m[1186:] = 0
    M = Image.fromarray(m); sh = Image.new("L", img.size, 0); sh.paste(M, (16, 18))
    k = np.asarray(sh.filter(ImageFilter.GaussianBlur(14)), np.float32)[..., None] / 255 * .3
    out = np.asarray(img, np.float32) * (1 - k) + k * np.array(INK, np.float32)
    img.paste(Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))); img.paste(L, (0, 0), M)

def middle_count(t):
    mx0, mx1 = SX0 + 2 * SW, SX0 + 3 * SW
    return sum(1 for i in range(len(DOTS)) if mx0 <= dot_pos(i, t)[0] < mx1)

def labels(d, t):
    cur = EP.current(t)
    if T_STAMP <= t < T_REW + .2: stamp(d, (SX0 + 2.5 * SW, 600), "THE MIDDLE", t, T_STAMP, size=78)
    if cur == "poor" and t >= T_POOR + .3:
        d.text((SX0 + SW, step_top(1) - 150), "≥ 2 IN 3", font=F(BLK, 56), fill=SIG, anchor="mm")
        d.text((SX0 + SW, step_top(1) - 105), "TOO HIGH", font=F(MONO, 26), fill=SIG, anchor="mm")
    if cur == "rich" and t >= T_RICH + .3:
        d.text((SX0 + 4 * SW + SW / 2 - 6, step_top(4) - 110), "TOO LOW", font=F(BLK, 48), fill=SIG, anchor="mm")

def head(d, t, line):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    d.text((X0, 400), "ON THE MIDDLE STEP", font=F(MONO, 30), fill=MID)
    d.text((X0 + 380, 388), f"{middle_count(t)}", font=F(BLK, 64), fill=SIG if EP.current(t) in ("reveal", "poor") else INK)

def draw(img, d, t, line, note="dots: schematic · 100 people"):
    shadowed(img, t); d = ImageDraw.Draw(img); labels(d, t); head(d, t, line); fig(d, note)

def sc_hook(img, d, t): draw(img, d, t, "WHERE DO YOU STAND?")
def sc_setup(img, d, t): draw(img, d, t, "10 COUNTRIES", note="30,000+ people · income fifths")
def sc_explain(img, d, t): draw(img, d, t, "1 DOT = 1 PERSON")
def sc_reveal(img, d, t): draw(img, d, t, "WHERE THEY THINK.")
def sc_poor(img, d, t): draw(img, d, t, "POORER: TOO HIGH.", note="67–94% of the poorer 40% overestimate")
def sc_rich(img, d, t): draw(img, d, t, "RICHER: TOO LOW.", note="Denmark, tax records · Hvidberg et al. 2023")
def sc_why(img, d, t): draw(img, d, t, "EVERYONE'S \"AVERAGE\"." if t < T_BACK else "WHERE DO YOU STAND?")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.scenes = {"hook": sc_hook, "setup": sc_setup, "explain": sc_explain, "reveal": sc_reveal, "poor": sc_poor, "rich": sc_rich, "why": sc_why}
FX = [(T_J0, whoosh(.6, .05), 0), *[(T_J0 + .2 + j * .06, tick(.02), -.6 + j * .1) for j in range(12)], (T_STAMP, thud(.5), 0),
      (T_REW, whoosh(.6, .05), 0), *[(T_STEPS + i * .1, tick(.025), -.6 + i * .3) for i in range(5)], (T_DOT, pop(.12), 0),
      (T_JUMP - .05, thud(.5), 0), *[(T_JUMP + .2 + j * .06, tick(.02), -.6 + j * .1) for j in range(12)],
      (T_POOR, pop(.16), -.5), (T_RICH, pop(.16), .5), (T_BACK, whoosh(.6, .05), 0)]
if __name__ == "__main__": EP.run(FX)
