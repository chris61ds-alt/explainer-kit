"""NOT JUST YOU – No. 139: split the world's INCOME equally (part 2 of No. 136) – IMF WEO 2025, GDP per capita PPP:
world ≈ $25,600; USA ≈ 86k, Germany ≈ 74k (≈ 3x), India ≈ 11k, Nigeria ≈ 9k; an equal split ≈ the level of Mexico / Thailand.
Light look (paper + soft shadows, reveal on black) + clarity rules ("Each bar is one country") + rule 13 opener.
ONE continuous object: seven country bars, each carrying a little person on top. Cold open: all bars slam to the world line
(rich bars drop, poor bars rise), "1/3" stamp on the US bar; rewind; dashed world line; reveal on black; level again with ghost
outlines of the old heights + "LIKE MEXICO" marker; arrows down / up; loop: back to the real heights (= frame 0)."""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from fx2 import light_look, is_light, stamp
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .5, "setup": .8, "explain": .5, "reveal": .8, "life": .8, "why": .1})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "setup", "explain", "reveal", "life", "why", "end"]
EP = ThreadEpisode(TL, 139, "SPLIT THE INCOME", order=ORDER, dark=True, label="IMF · GDP PER PERSON · 2025",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("IMF World Economic Outlook 2025,", "GDP per capita, PPP (international $)"),
                   music=dict(bpm=96, root=-1, prog="major", kick="four", audio="v5"),
                   cover=dict(words=["SPLIT ALL", "INCOME EQUALLY:", "RICH LIVE ON 1/3."], kicker="The world's income, per person."))
light_look(EP, ORDER)

NAMES = ["USA", "GER", "CHN", "MEX", "THA", "IND", "NGA"]
REAL = [86, 74, 27, 26, 25, 11, 9]               # thousand int. $ per person (IMF 2025, rounded)
WORLD = 25.6
EQ = [WORLD] * 7
XS = [118 + i * 140 for i in range(7)]
BW, BASE, PX = 92, 1120, 6.4                       # bar width, base line, pixels per $1k
def bar_top(v): return BASE - v * PX

T_O = .6;                  D_O = 1.0               # cold open: everything slams to the world average
T_STAMP = cue("hook", "a third") - .05
T_REW = S("setup") - .05;  D_REW = .9
T_LINE = cue("setup", "twenty-six") - .2
T_BARS = S("explain") - .05; T_EXLINE = cue("explain", "The line") - .1
T_RICH = cue("reveal", "America") - .1; T_POOR = cue("reveal", "India") - .1
T_EQ = S("life") + .05;    D_EQ = 1.1
T_LIKE = cue("life", "Mexico") - .15
T_CUT = cue("why", "pay cut") - .2; T_RAISE = cue("why", "raise") - .25
T_BACK = E("why") - 1.1;   D_BACK = .9
MOVES = [(T_O, D_O, REAL, EQ), (T_REW, D_REW, EQ, REAL), (T_EQ, D_EQ, REAL, EQ), (T_BACK, D_BACK, EQ, REAL)]

def heights(t):
    cur = list(REAL)
    for ts, dur, A, B in MOVES:
        if t < ts: break
        cur = [A[i] + (B[i] - A[i]) * spring(clamp((t - ts - i * .05) / (dur * .7)), f=2.0, damp=6.0) for i in range(7)]
    return cur

def leveled(t): return (T_O + .3 <= t < T_REW) or (T_EQ + .3 <= t < T_BACK)

def person(d, x, y, col):
    d.ellipse([x - 14, y - 66, x + 14, y - 38], fill=col)
    d.chord([x - 26, y - 34, x + 26, y + 18], 180, 360, fill=col)

def objects(L, d, t):
    h = heights(t); cur = EP.current(t)
    for i, x in enumerate(XS):
        hot = (cur == "explain" and t >= T_BARS + i * .07 and t < T_EXLINE) or (cur == "reveal" and ((i < 2 and t >= T_RICH) or (i >= 5 and t >= T_POOR))) \
              or (cur == "life" and t >= T_LIKE and i in (3, 4))
        y = bar_top(h[i])
        d.rectangle([x - BW / 2, y, x + BW / 2, BASE], fill=INK if hot else MID)
        person(d, x, y - 2, INK)
    d.line([(60, BASE), (1020, BASE)], fill=INK, width=4)

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

def dashed(d, y, col, x0=60, x1=1020):
    x = x0
    while x < x1: d.line([(x, y), (min(x + 22, x1), y)], fill=col, width=4); x += 38

def ghost(d, i, col):
    x = XS[i]; y = bar_top(REAL[i])
    for (a, b) in (((x - BW / 2, y), (x + BW / 2, y)), ((x - BW / 2, y), (x - BW / 2, BASE)), ((x + BW / 2, y), (x + BW / 2, BASE))):
        n = int(math.dist(a, b) // 30) + 1
        for j in range(n):
            u0, u1 = j / n, min(1, (j + .5) / n)
            d.line([(a[0] + (b[0] - a[0]) * u0, a[1] + (b[1] - a[1]) * u0), (a[0] + (b[0] - a[0]) * u1, a[1] + (b[1] - a[1]) * u1)], fill=col, width=3)

def arrow(d, x, y0, y1, col):
    d.line([(x, y0), (x, y1)], fill=col, width=8); s = 1 if y1 > y0 else -1
    d.polygon([(x - 18, y1 - 22 * s), (x + 18, y1 - 22 * s), (x, y1 + 6 * s)], fill=col)

def labels(d, t):
    cur = EP.current(t)
    for i, x in enumerate(XS): d.text((x, BASE + 28), NAMES[i], font=F(MONO, 26), fill=INK, anchor="mm")
    if T_LINE <= t < T_BACK or t < T_REW:                               # the world average line
        dashed(d, bar_top(WORLD), SIG if cur in ("setup", "explain") and t >= T_LINE else INK)
        if T_LINE <= t < T_BACK and not leveled(t): d.text((1020, bar_top(WORLD) - 12), "WORLD $26K", font=F(BLK, 34), fill=INK, anchor="rb")
    if T_STAMP <= t < T_REW + .2: stamp(d, (XS[1] + 40, 690), "1/3", t, T_STAMP, size=110)
    if cur == "reveal":
        if t >= T_RICH: d.text((XS[0] + 70, bar_top(86) + 40), "×3", font=F(BLK, 76), fill=SIG, anchor="lm")
    if leveled(t) and t >= T_EQ:
        for i in range(7): ghost(d, i, MID)
    if cur == "life" and t >= T_LIKE:
        d.text(((XS[3] + XS[4]) / 2, bar_top(WORLD) - 120), "LIKE MEXICO", font=F(BLK, 44), fill=INK, anchor="mm")
    if cur == "why" and t < T_BACK:
        if t >= T_CUT:
            for i in (0, 1): arrow(d, XS[i], bar_top(REAL[i]) + 30, bar_top(WORLD) - 90, SIG)
        if t >= T_RAISE:
            for i in (5, 6): arrow(d, XS[i], bar_top(REAL[i]), bar_top(WORLD) + 26, WHITE)     # inside the risen bar

def head(d, t, line):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    v = heights(t)[0]
    d.text((X0, 400), "USA, PER PERSON", font=F(MONO, 30), fill=MID)
    d.text((X0 + 320, 388), f"${v:.0f}K", font=F(BLK, 64), fill=SIG if EP.current(t) == "reveal" else INK)

def draw(img, d, t, line, note="GDP per person, PPP · rounded"):
    shadowed(img, t); d = ImageDraw.Draw(img); labels(d, t); head(d, t, line); fig(d, note)

def sc_hook(img, d, t): draw(img, d, t, "SPLIT THE INCOME?")
def sc_setup(img, d, t): draw(img, d, t, "THE WORLD AVERAGE")
def sc_explain(img, d, t): draw(img, d, t, "1 BAR = 1 COUNTRY")
def sc_reveal(img, d, t): draw(img, d, t, "TODAY.")
def sc_life(img, d, t): draw(img, d, t, "EQUAL.", note="same average output · ignores gaps inside countries")
def sc_why(img, d, t): draw(img, d, t, "CUT HERE. RAISE THERE." if t < T_BACK else "SPLIT THE INCOME?")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.scenes = {"hook": sc_hook, "setup": sc_setup, "explain": sc_explain, "reveal": sc_reveal, "life": sc_life, "why": sc_why}
FX = [(T_O, whoosh(.6, .05), 0), *[(T_O + .15 + i * .05, tick(.03), -.6 + i * .2) for i in range(7)], (T_STAMP, thud(.5), -.2),
      (T_REW, whoosh(.6, .05), 0), (T_LINE, pop(.14), 0), *[(T_BARS + i * .07, tick(.02), -.6 + i * .2) for i in range(7)],
      (S("reveal") + .05, thud(.55), 0), (T_RICH, pop(.16), -.5), (T_POOR, pop(.16), .5),
      (T_EQ, whoosh(.6, .05), 0), *[(T_EQ + .15 + i * .05, tick(.03), -.6 + i * .2) for i in range(7)], (T_LIKE, pop(.14), 0),
      (T_CUT, pop(.12), -.5), (T_RAISE, pop(.12), .5), (T_BACK, whoosh(.6, .05), 0)]
if __name__ == "__main__": EP.run(FX)
