"""NOT JUST YOU – No. 81 (remake 15.11.2026, current standards): split opinions get more messages – OkCupid 2011: among women
with similar average looks scores, the more men disagreed (1s and 5s), the more messages; one example: 3x the messages.
Light look (paper + soft shadows, reveal on black) + clarity rules (the picture explained once: "Each dot is one rating").
Two women, two 1-5 rating histograms that fill up with falling dots (same average 3.0, very different shape); a live average
marker; on the reveal envelopes fly in as PARTICLES, 3x as many to the right; loop: the dots fall away.
Old version: render_v1.py / script_v1.json."""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from fx2 import dots, light_look, is_light, phone_inbox, stamp
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .5, "setup": .5, "explain": .5, "same": .5, "diff": .5, "reveal": .8, "why": .1})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "setup", "explain", "same", "diff", "reveal", "why", "end"]
EP = ThreadEpisode(TL, 81, "SPLIT OPINION", order=ORDER, dark=True, label="PLATFORM DATA · OKCUPID · 2011",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("OkTrends (2011), The Mathematics Of Beauty ·", "OkCupid platform data, not peer-reviewed"),
                   music=dict(bpm=98, root=1, prog="major", kick="four", audio="v5"),
                   cover=dict(words=["NOT EVERYONE", "SHOULD LIKE", "YOUR LOOKS."], kicker="Split opinions get more messages."))
light_look(EP, ORDER)

CX = {"A": 285, "B": 795}
COUNTS = {"A": [0, 2, 26, 2, 0], "B": [12, 2, 2, 2, 12]}          # both average exactly 3.0 (schematic)
MSG = {"A": 6, "B": 18}
BASE, COLW, DOT = 1100, 74, 22
def col_x(k, r): return CX[k] + (r - 3) * COLW                    # r = rating 1..5
VOTES = {}
for k in "AB":
    seq = [r for r in range(1, 6) for _ in range(COUNTS[k][r - 1])]
    rng = np.random.RandomState(1 if k == "A" else 2); rng.shuffle(seq); VOTES[k] = seq
T_V0, T_V1 = cue("explain", "Each dot") - .1, E("explain") + .2
T_AVG = cue("same", "same average") - .1
T_DIFF_A, T_DIFF_B = cue("diff", "on the left") - .1, cue("diff", "On the right") - .1
T_MSG = S("reveal") + .1; T3 = cue("reveal", "three times") - .2
T_BACK = cue("why", "Because") - .35

def vote_t(k, i): return T_V0 + (T_V1 - T_V0) * i / len(VOTES[k]) + (.08 if k == "B" else 0)

def woman(d, cx, y, col):
    d.ellipse([cx - 44, y, cx + 44, y + 88], fill=col)
    d.chord([cx - 95, y + 92, cx + 95, y + 270], 180, 360, fill=col)

def shadow(L, shapes, k=.26):
    m = Image.new("L", L.size, 0); dm = ImageDraw.Draw(m)
    for s in shapes: s(dm)
    a = np.asarray(m.filter(ImageFilter.GaussianBlur(12)), np.float32)[..., None] / 255 * k
    L.paste(Image.fromarray(np.clip(np.asarray(L, np.float32) * (1 - a) + a * np.array(INK, np.float32), 0, 255).astype(np.uint8)))

def envelope(d, x, y, s, col, line):
    d.rectangle([x - 22 * s, y - 15 * s, x + 22 * s, y + 15 * s], fill=col)
    d.line([(x - 22 * s, y - 15 * s), (x, y + 3 * s), (x + 22 * s, y - 15 * s)], fill=line, width=max(1, int(3 * s)))

def scene(img, d, t):
    light = is_light(EP, t); back = clamp((t - T_BACK) / .45) if t >= T_BACK else 0
    body = RULE if light else mix(BG, INK, .2)
    if light: shadow(img, [lambda dm, k=k: woman(dm, CX[k] + 18, 560 + 14, 255) for k in "AB"])
    for k in "AB":
        wave = (t - .05) / .8; up = 14 * max(0, 1 - abs(wave - (0 if k == "A" else .4)) * 3) if 0 <= wave <= 1.3 else 0   # cold open bounce
        woman(d, CX[k], 560 - up, body)
        for r in range(1, 6):                                       # the 1-5 scale under each woman
            x = col_x(k, r); d.line([(x - 28, BASE + 26), (x + 28, BASE + 26)], fill=MID, width=3)
            if t >= T_V0 - .4 and back < 1: d.text((x, BASE + 52), str(r), font=F(BLK, 30), fill=MID, anchor="mm")
        stack = [0] * 6
        for i, r in enumerate(VOTES[k]):                            # ratings fall in with gravity and stack up
            tk = vote_t(k, i)
            if t < tk: continue
            h = stack[r]; stack[r] += 1
            fall = clamp((t - tk) / .35); y = BASE - h * DOT - 650 * (1 - fall) ** 2 + 900 * back * back
            hot = (k == "A" and r == 3 and T_DIFF_A <= t < T_DIFF_B + .4) or (k == "B" and r in (1, 5) and t >= T_DIFF_B and EP.current(t) in ("diff",))
            c = SIG if (not light and k == "B" and r in (1, 5)) else (INK if hot or not light else MID)
            d.ellipse([col_x(k, r) - 9, y - 9, col_x(k, r) + 9, y + 9], fill=c)
        if T_AVG <= t < T_BACK:                                      # the average marker: a triangle under the scale at 3.0
            ka = spring((t - T_AVG - (.15 if k == "B" else 0)) / .5); x = col_x(k, 3)
            d.polygon([(x, BASE + 74), (x - 16 * ka, BASE + 100), (x + 16 * ka, BASE + 100)], fill=INK)
            if ka > .5: d.text((x, BASE + 126), "AVG 3.0", font=F(MONO, 24), fill=INK, anchor="mm")
        if T_MSG <= t < T_BACK + .3:                                 # messages fly in
            n = MSG[k]
            for j in range(n):
                tj = T_MSG + j * (1.6 / MSG["B"]); kk = ease(clamp((t - tj) / .5))
                if kk <= 0: continue
                sx, sy = (-80 if k == "A" else W + 80), 480 + (j * 37) % 140
                tx, ty = CX[k] + 120 + (j % 3) * 44, 610 + (j // 3) * 36          # stacked next to her
                x, y = sx + (tx - sx) * kk, sy + (ty - sy) * kk - 80 * math.sin(math.pi * kk)
                envelope(d, x, y - 400 * back, .9, INK, BG)            # INK = dark on paper, white on black
    for k, lab in (("A", "SHE"), ("B", "HER")):
        if t >= cue("explain", "two women") - .1 and back < 1:
            d.text((CX[k], 525), "LEFT" if k == "A" else "RIGHT", font=F(MONO, 24), fill=MID, anchor="mm")

# ---- the first 3 seconds (15.11.2026): POV phone, messages slam in, a "1/5" stamp lands on her picture, camera pulls out
T_M = list(np.linspace(-.3, cue("hook", "Then not") - .15, 16))          # 2–3 already there at frame 0 (= TikTok cover)
T_STAMP = cue("hook", "not everyone") - .05
T_OUT = S("setup") - .25
BIG = (270, 485, 810, 1150); SMALL = (CX["B"] - 40, 560, CX["B"] + 40, 650)
def opener(img, d, t):
    k = ease_io(clamp((t - T_OUT) / .7))
    if k >= 1: return
    box = tuple(a + (b - a) * k for a, b in zip(BIG, SMALL))
    shake = 10 * math.sin(t * 90) * max(0, 1 - (t - T_STAMP) / .25) if t >= T_STAMP else 0
    box = (box[0] + shake, box[1], box[2] + shake, box[3])
    pc, pr = phone_inbox(d, box, t, T_M, title="INBOX")
    if k < .3: stamp(d, (pc[0] + pr * 1.4, pc[1] + pr * .5), "1/5", t, T_STAMP, size=int(100 * (1 - k)))

def head(d, t, line, sub=None):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    cur = EP.current(t)
    if T_MSG <= t < T_BACK:
        v = 1 + 2 * ease(clamp((t - T3) / .7)) if t >= T3 else 1
        d.text((X0, 400), "MESSAGES · RIGHT VS LEFT", font=F(MONO, 30), fill=MID); d.text((X0 + 470, 388), f"{v:.0f}×", font=F(BLK, 64), fill=SIG)
    elif T_AVG <= t < T_BACK:
        d.text((X0, 400), "AVERAGE", font=F(MONO, 30), fill=MID); d.text((X0 + 170, 388), "3.0 = 3.0", font=F(BLK, 64), fill=INK)
    elif t < T_OUT + .5:
        n = sum(1 for x in T_M if t >= x)
        d.text((X0, 400), "MESSAGES", font=F(MONO, 30), fill=MID); d.text((X0 + 190, 388), f"{n}", font=F(BLK, 64), fill=INK)
    else:
        n = sum(1 for i in range(len(VOTES["A"])) if t >= vote_t("A", i)) * 2 if T_V0 <= t < T_BACK else 0
        d.text((X0, 400), "RATINGS", font=F(MONO, 30), fill=MID); d.text((X0 + 170, 388), f"{n}", font=F(BLK, 64), fill=INK)
    if sub: d.text((X1, 470), sub, font=F(MONO, 26), fill=MID, anchor="ra")

def draw(img, d, t, line, sub=None, note="dots: schematic example"):
    if t >= T_OUT: scene(img, d, t)
    opener(img, d, t); head(d, t, line, sub); fig(d, note)

def sc_hook(img, d, t): draw(img, d, t, "MORE MESSAGES?")
def sc_setup(img, d, t): draw(img, d, t, "LOOKS: 1 TO 5", note="men rating women · OkCupid")
def sc_explain(img, d, t): draw(img, d, t, "1 DOT = 1 RATING")
def sc_same(img, d, t): draw(img, d, t, "SAME AVERAGE.")
def sc_diff(img, d, t): draw(img, d, t, "DIFFERENT SHAPE.")
def sc_reveal(img, d, t): draw(img, d, t, "SPLIT = MORE.", note="one example: 3× the messages")
def sc_why(img, d, t): draw(img, d, t, "LESS COMPETITION." if t < T_BACK else "MORE MESSAGES?", note="platform data 2011 · not peer-reviewed")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.scenes = {"hook": sc_hook, "setup": sc_setup, "explain": sc_explain, "same": sc_same, "diff": sc_diff, "reveal": sc_reveal, "why": sc_why}
FX = [*[(x, pop(.05), .2) for x in T_M if x > 0], (T_STAMP, thud(.5), .3), (T_OUT, whoosh(.7, .05), 0), *[(vote_t("A", i) + .35, tick(.02), -.5) for i in range(0, 30, 2)],
      *[(vote_t("B", i) + .35, tick(.02), .5) for i in range(1, 30, 2)],
      (T_AVG, pop(.12), -.4), (T_AVG + .15, pop(.12), .4), (T_DIFF_A, whoosh(.4, .04), -.5), (T_DIFF_B, whoosh(.4, .04), .5),
      (S("reveal") + .1, thud(.55), 0), *[(T_MSG + j * (1.6 / 18) + .5, tick(.03), .6) for j in range(18)], (T3 + .3, pop(.16), .3),
      (T_BACK, whoosh(.6, .05), 0)]
if __name__ == "__main__": EP.run(FX)
