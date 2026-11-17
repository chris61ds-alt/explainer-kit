"""NOT JUST YOU – No. 137: guess vs wish vs real – Norton & Ariely (2011): 5,522 Americans guessed the richest fifth owns
59 % of wealth, wished for 32 %, actual 84 % (poorest 40 %: 0.3 %).
Light look (paper + soft shadows, reveal on black) + clarity rules ("Each coin is one percent") + rule 13 opener.
ONE continuous object (same coin language as No. 136): five people, richest left, coin stacks. Cold open: the guess stack (59)
with a dashed GUESS line, then the real tower shoots past it to 84, "WAY OFF" stamp; rewind to empty; one coin each;
guess -> wish -> real (on black) with dashed GUESS / WISH lines left behind; loop: back to the guess (= frame 0)."""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from fx2 import light_look, is_light, stamp
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .5, "setup": .5, "explain": .5, "est": .6, "wish": .6, "reveal": .8, "why": .1})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "setup", "explain", "est", "wish", "reveal", "why", "end"]
EP = ThreadEpisode(TL, 137, "GUESS, WISH, REAL", order=ORDER, dark=True, label="SURVEY · 5,522 AMERICANS",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Norton & Ariely (2011), Perspectives on", "Psychological Science 6(1), 9–12"),
                   music=dict(bpm=94, root=2, prog="tense", kick="four", audio="v5"),
                   cover=dict(words=["WE GUESSED 59%.", "WE WISHED 32%.", "IT'S 84%."], kicker="How much the richest fifth owns."))
light_look(EP, ORDER)

GUESS = [59, 20, 12, 6, 3]                       # only the top fifth is exact (59 / 32 / 84); the rest is schematic
WISH = [32, 22, 21, 14, 11]
REAL = [84, 11, 4, .2, .1]
EMPTY = [0] * 5; ONE = [1] * 5
XS = [150 + i * 195 for i in range(5)]
BASE, STEP, CW, CH = 1005, 6.0, 52, 12
HEAD_Y = 1058

T_O = .7;                     D_O = 1.0          # cold open: the real tower shoots past the guess
T_STAMP = cue("hook", "way off") - .05
T_REW = S("setup") - .05;     D_REW = .8
T_ONE = cue("explain", "Each coin") - .2; D_ONE = .5
T_G = S("est") + .05;       D_G = 1.3
T_W = S("wish") + .05;        D_W = 1.0
T_R = S("reveal") + .05;      D_R = 1.2
T_POOR = cue("reveal", "poorest") - .1
T_BACK = 1e9;      D_BACK = .9
MOVES = [(T_O, D_O, GUESS, REAL), (T_REW, D_REW, REAL, EMPTY), (T_ONE, D_ONE, EMPTY, ONE), (T_G, D_G, ONE, GUESS),
         (T_W, D_W, GUESS, WISH), (T_R, D_R, WISH, REAL), (T_BACK, D_BACK, REAL, GUESS)]

def stacks(t):
    cur = list(GUESS)
    for ts, dur, A, B in MOVES:
        if t < ts: break
        cur = [A[i] + (B[i] - A[i]) * ease_io(clamp((t - ts - i * dur * .06) / (dur * .76))) for i in range(5)]
    return cur

def lines_on(t):
    """which dashed reference lines are visible: guess (59) and wish (32)"""
    g = t < T_REW or t >= T_G + D_G * .8
    w = T_W + D_W * .8 <= t < T_BACK
    return g, w

def person(d, x, col):
    d.ellipse([x - 22, HEAD_Y - 22, x + 22, HEAD_Y + 22], fill=col)
    d.chord([x - 44, HEAD_Y + 28, x + 44, HEAD_Y + 112], 180, 360, fill=col)

def stack(d, x, c):
    if c <= 0: return
    if c < 1:
        w = max(5, CW * c); d.ellipse([x - w, BASE - CH * .6, x + w, BASE + CH * .6], fill=WHITE, outline=INK, width=3); return
    n = int(c + .001); fr = c - n
    for i in range(n):
        y = BASE - i * STEP; d.ellipse([x - CW, y - CH, x + CW, y + CH], fill=WHITE, outline=INK, width=3)
    if fr > .05:
        y = BASE - n * STEP; w = CW * fr; d.ellipse([x - w, y - CH, x + w, y + CH], fill=WHITE, outline=INK, width=3)

def objects(L, d, t):
    cnt = stacks(t); cur = EP.current(t)
    for i, x in enumerate(XS):
        hot = (cur == "explain" and t >= S("explain") + i * .08) or (cur in ("est", "wish") and i == 0) or (cur == "reveal" and (i == 0 or (i >= 3 and t >= T_POOR)))
        person(d, x, INK if hot else MID)
        stack(d, x, cnt[i])
    if T_ONE + .3 <= t < S("est"):                                    # the picture explained once: one coin = 1 %
        k = spring((t - T_ONE - .3) / .45); cx, cy = XS[2], BASE
        bx, by = XS[2] + 40, 720; r = 78 * k
        d.line([(cx, cy), (bx, by + r)], fill=INK, width=4)
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=WHITE, outline=INK, width=6)
        if k > .6: d.text((bx, by), "1%", font=F(BLK, 58), fill=INK, anchor="mm")

def dashed(d, y, label, col):
    x = 50
    while x < 1030: d.line([(x, y), (min(x + 26, 1030), y)], fill=col, width=5); x += 44
    d.text((1030, y - 12), label, font=F(BLK, 36), fill=col, anchor="rb")

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

def labels(d, t):
    cur = EP.current(t); g, w = lines_on(t)
    if g: dashed(d, BASE - 59 * STEP - CH, "GUESS 59", MID if cur == "reveal" else INK)
    if w: dashed(d, BASE - 32 * STEP - CH, "WISH 32", MID if cur == "reveal" else INK)
    if T_STAMP <= t < T_REW + .2: stamp(d, (700, 640), "WAY OFF", t, T_STAMP, size=86)
    if cur == "reveal" and t >= T_R + D_R * .8:
        d.text((XS[0] + 120, BASE - 84 * STEP - 8), "84", font=F(BLK, 80), fill=SIG, anchor="lm")
    if cur == "reveal" and t >= T_POOR:
        d.line([(XS[3] - 60, BASE + 32), (XS[4] + 60, BASE + 32)], fill=SIG, width=6)
        d.text(((XS[3] + XS[4]) / 2, BASE - 70), "< 1", font=F(BLK, 64), fill=SIG, anchor="mm")

def head(d, t, line):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    c = stacks(t)[0]
    d.text((X0, 400), "RICHEST FIFTH", font=F(MONO, 30), fill=MID)
    d.text((X0 + 280, 388), f"{c:.0f}%", font=F(BLK, 64), fill=SIG if EP.current(t) == "reveal" else INK)

def draw(img, d, t, line, note="1 coin = 1% of all wealth · USA"):
    shadowed(img, t); d = ImageDraw.Draw(img); labels(d, t); head(d, t, line); fig(d, note)

def sc_hook(img, d, t): draw(img, d, t, "THE RICHEST FIFTH")
def sc_setup(img, d, t): draw(img, d, t, "GUESS. WISH.", note="survey · 5,522 Americans")
def sc_explain(img, d, t): draw(img, d, t, "RICH TO POOR")
def sc_guess(img, d, t): draw(img, d, t, "THE GUESS.", note="other bars: schematic")
def sc_wish(img, d, t): draw(img, d, t, "THE WISH.", note="other bars: schematic")
def sc_reveal(img, d, t): draw(img, d, t, "THE TRUTH.", note="actual: 84 / 11 / 4 / 0.2 / 0.1 %")
def sc_why(img, d, t): draw(img, d, t, "FAIRER IN OUR HEADS." if t < T_BACK else "THE RICHEST FIFTH")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.scenes = {"hook": sc_hook, "setup": sc_setup, "explain": sc_explain, "est": sc_guess, "wish": sc_wish, "reveal": sc_reveal, "why": sc_why}
FX = [(T_O, whoosh(.7, .05), -.4), *[(T_O + .1 + j * .07, tick(.02), -.5) for j in range(8)], (T_STAMP, thud(.5), .3),
      (T_REW, whoosh(.6, .05), 0), (T_ONE, pop(.12), 0), (T_ONE + .3, pop(.14), .2),
      (T_G, whoosh(.5, .04), -.3), *[(T_G + .1 + j * .09, tick(.02), -.4) for j in range(8)],
      (T_W, whoosh(.5, .04), .3), (S("reveal") + .05, thud(.55), 0), *[(T_R + .1 + j * .08, tick(.025), -.5) for j in range(10)],
      (T_POOR, pop(.16), .5), (T_BACK, whoosh(.6, .05), 0)]
FX = [fx for fx in FX if fx[0] < 1e8]                  # rule 15 (17.11.2026): no loop, the payoff stays to the last frame
if __name__ == "__main__": EP.run(FX)
