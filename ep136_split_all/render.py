"""NOT JUST YOU – No. 136: split all the world's wealth equally – World Inequality Report 2026 (2025, PPP): top 10 % own 75 %,
bottom 50 % own 2 %; an equal split is well over $100,000 per adult (≈ $133k derived), ~20x what the poorer half owns.
Light look (paper + soft shadows, reveal on black) + clarity rules ("Each coin is one percent") + rule 13 opener.
ONE continuous object: ten people with coin stacks (100 coins = all wealth). Cold open: the 75-coin tower tips and rains
coins onto the others until all stacks are level, "9 OF 10 GAIN" stamp; rewind; explain; reveal on black; split again;
"YOU?" over the middle; loop: the coins fly back to the tower (= frame 0)."""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from fx2 import light_look, is_light, stamp, coin
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .5, "setup": .5, "explain": .5, "reveal": .8, "split": .8, "why": .1})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "setup", "explain", "reveal", "split", "why", "end"]
EP = ThreadEpisode(TL, 136, "SPLIT IT ALL", order=ORDER, dark=True, label="WORLD INEQUALITY REPORT 2026",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("World Inequality Report 2026, World Inequality Lab ·", "cross-check: UBS Global Wealth Report 2026"),
                   music=dict(bpm=96, root=0, prog="major", kick="four", audio="v5"),
                   cover=dict(words=["SPLIT ALL", "WEALTH EQUALLY:", "9 IN 10 WIN."], kicker="The world's wealth, in 100 coins."))
light_look(EP, ORDER)

UNEQ = [.4, .4, .4, .4, .4, 6, 6, 6, 5, 75]          # schematic deciles (WIR 2026: bottom 50 % = 2, middle 40 % = 23, top 10 % = 75)
EQ = [10] * 10
XS = [108 + i * 96 for i in range(10)]
BASE, STEP, CW, CH = 1005, 6.4, 36, 10                 # stack base, coin pitch, coin half-width / half-height
HEAD_Y = 1058

T_L0 = .55;                         D_L0 = 1.7            # cold open: the tower rains onto everyone
T_STAMP = cue("hook", "nine") - .05
T_REW = S("setup") - .1;            D_REW = 1.0           # rewind to today
T_PEOPLE = S("explain") - .05; T_COIN = cue("explain", "Each coin") - .1
T_RICH = cue("reveal", "richest") - .1; T_POOR = cue("reveal", "poorest") - .1
T_SPLIT = S("split") + .05;         D_SPLIT = 1.5
T_MONEY = cue("split", "hundred") - .25
T_YOU = cue("why", "If") - .05
T_BACK = 1e9;           D_BACK = .95          # loop: back to frame 0
MOVES = [(T_L0, D_L0, UNEQ, EQ), (T_REW, D_REW, EQ, UNEQ), (T_SPLIT, D_SPLIT, UNEQ, EQ), (T_BACK, D_BACK, EQ, UNEQ)]

def stacks(t):
    """coin count per person + flying coins [(x, y, phase)] for time t"""
    cur, fly = list(UNEQ), []
    for ts, dur, A, B in MOVES:
        if t < ts: break
        cnt = [0.0] * 10
        for j in range(9):
            delay = (j if B is EQ else 8 - j) * dur * .045
            k = ease_io(clamp((t - ts - delay) / (dur * .62)))
            cnt[j] = A[j] + (B[j] - A[j]) * k
            if 0 < k < 1:                                             # two coins in the air per receiving stack
                for u0 in (0, .5):
                    u = (k * 2 + u0) % 1
                    if B is not EQ: u = 1 - u
                    x9, y9 = XS[9], BASE - (A[9] + (B[9] - A[9]) * ease_io(clamp((t - ts) / dur))) * STEP
                    xj, yj = XS[j], BASE - (A[j] + 2) * STEP
                    x = x9 + (xj - x9) * u; y = y9 + (yj - y9) * u - 190 * math.sin(math.pi * u)
                    fly.append((x, y, t * 13 + j + u0 * 3))
        cnt[9] = 100 - sum(cnt[:9]); cur = cnt
    return cur, fly

def cur_top(c): return c * STEP

def person(d, x, col):
    d.ellipse([x - 19, HEAD_Y - 19, x + 19, HEAD_Y + 19], fill=col)
    d.chord([x - 38, HEAD_Y + 24, x + 38, HEAD_Y + 100], 180, 360, fill=col)

def stack(d, x, c, edge=INK, face=WHITE):
    if c < 1:                                                          # a sliver of a coin
        w = max(5, CW * c); d.ellipse([x - w, BASE - CH * .6, x + w, BASE + CH * .6], fill=face, outline=edge, width=3); return
    n = int(c + .001); fr = c - n
    for i in range(n):
        y = BASE - i * STEP; d.ellipse([x - CW, y - CH, x + CW, y + CH], fill=face, outline=edge, width=3)
    if fr > .05:
        y = BASE - n * STEP; w = CW * fr; d.ellipse([x - w, y - CH, x + w, y + CH], fill=face, outline=edge, width=3)

def objects(L, d, t):
    cnt, fly = stacks(t); cur = EP.current(t)
    for i, x in enumerate(XS):
        hot = (cur == "explain" and t >= T_PEOPLE + i * .06) or (cur == "reveal" and ((i == 9 and t >= T_RICH) or (i < 5 and t >= T_POOR))) \
              or (cur == "why" and T_YOU <= t < T_BACK and i < 9)
        person(d, x, INK if hot else MID)
        stack(d, x, cnt[i])
    for x, y, ph in fly: coin(d, x, y, CH + 8, ph, col=WHITE, edge=INK)
    if T_COIN <= t < S("reveal"):                                       # the picture explained once: one coin = 1 %
        k = spring((t - T_COIN) / .45); cx, cy = XS[6], BASE - 6 * STEP
        bx, by = 330, 690; r = 78 * k
        d.line([(cx, cy), (bx + r * .7, by + r * .7)], fill=INK, width=4)
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=WHITE, outline=INK, width=6)
        if k > .6: d.text((bx, by), "1%", font=F(BLK, 58), fill=INK, anchor="mm")

def shadowed(img, t):
    """draw the objects on a paper layer, then put them back with a soft drop shadow (light look)"""
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
    cnt, _ = stacks(t); cur = EP.current(t)
    if t >= T_STAMP and t < T_REW + .2:
        stamp(d, (720, 640), "9 OF 10 GAIN", t, T_STAMP, size=74)
    if cur == "reveal":
        if t >= T_RICH: d.text((XS[9] - 60, BASE - 75 * STEP - 70), "75", font=F(BLK, 72), fill=SIG, anchor="mm")
        if t >= T_POOR:
            d.line([(XS[0] - 30, BASE + 30), (XS[4] + 30, BASE + 30)], fill=SIG, width=6)
            d.text(((XS[0] + XS[4]) / 2, BASE - 60), "2", font=F(BLK, 72), fill=SIG, anchor="mm")
    if T_MONEY <= t < T_YOU: stamp(d, (540, 760), ">$100K EACH", t, T_MONEY, size=70)
    if T_YOU <= t < T_BACK:
        k = spring((t - T_YOU) / .4); d.text((XS[4], BASE - 10 * STEP - 70 - 20 * (1 - k)), "YOU?", font=F(BLK, 46), fill=INK, anchor="mm")

def head(d, t, line):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    cnt, _ = stacks(t)
    d.text((X0, 400), "RICHEST TENTH", font=F(MONO, 30), fill=MID)
    d.text((X0 + 290, 388), f"{cnt[9]:.0f}%", font=F(BLK, 64), fill=SIG if EP.current(t) == "reveal" else INK)

def draw(img, d, t, line, note="coins: schematic · 1 coin = 1% of world wealth"):
    shadowed(img, t); d = ImageDraw.Draw(img); labels(d, t); head(d, t, line); fig(d, note)

def sc_hook(img, d, t): draw(img, d, t, "SPLIT IT ALL?")
def sc_setup(img, d, t): draw(img, d, t, "ALL WEALTH", note="homes, savings, firms – minus debts")
def sc_explain(img, d, t): draw(img, d, t, "10 PEOPLE")
def sc_reveal(img, d, t): draw(img, d, t, "TODAY.", note="World Inequality Report 2026 · 2025, PPP")
def sc_split(img, d, t): draw(img, d, t, "EQUAL.", note="≈ $133K per adult (derived) · thought experiment")
def sc_why(img, d, t): draw(img, d, t, "MOST START SMALL." if t < T_BACK else "SPLIT IT ALL?")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.scenes = {"hook": sc_hook, "setup": sc_setup, "explain": sc_explain, "reveal": sc_reveal, "split": sc_split, "why": sc_why}
FX = [(T_L0, whoosh(.6, .05), .4), *[(T_L0 + .25 + j * .14, tick(.03), -.6 + j * .12) for j in range(9)], (T_STAMP, thud(.5), .3),
      (T_REW, whoosh(.7, .05), 0), *[(T_PEOPLE + i * .06, tick(.02), -.6 + i * .13) for i in range(0, 10, 2)], (T_COIN, pop(.14), -.3),
      (S("reveal") + .1, thud(.55), 0), (T_RICH, pop(.16), .5), (T_POOR, pop(.16), -.5),
      (T_SPLIT, whoosh(.6, .05), .4), *[(T_SPLIT + .25 + j * .14, tick(.03), -.6 + j * .12) for j in range(9)], (T_MONEY, thud(.5), 0),
      (T_YOU, pop(.12), 0), (T_BACK, whoosh(.6, .05), 0)]
FX = [fx for fx in FX if fx[0] < 1e8]                  # rule 15 (17.11.2026): no loop, the payoff stays to the last frame
if __name__ == "__main__": EP.run(FX)
