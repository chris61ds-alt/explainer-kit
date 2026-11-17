"""NOT JUST YOU – No. 140: how rich are you globally? – Our World in Data (2025, World Bank PIP): a post-tax income of
$20,000 (one-person household, int. $ 2021) puts you in the world's richest tenth; global median ≈ $3,400 a year;
more than half of people in Germany / the US are above that line.
Light look (paper + soft shadows, reveal on black) + clarity rules ("Each bar is one tenth of humanity") + rule 13 opener.
ONE continuous object: ten bars (deciles, poorest left) each with a little person; a "$20K" payslip card drops onto the
top bar, the 20K line snaps across, "TOP 10%" stamp; rewind; median marked; reveal on black; loop back to frame 0."""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from fx2 import light_look, is_light, stamp
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .5, "setup": .5, "explain": .5, "median": .8, "reveal": .8, "why": .1})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "setup", "explain", "median", "reveal", "why", "end"]
EP = ThreadEpisode(TL, 140, "RICH ON EARTH", order=ORDER, dark=True, label="OUR WORLD IN DATA · WORLD BANK",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Our World in Data (2025), based on the World Bank", "Poverty and Inequality Platform"),
                   music=dict(bpm=98, root=1, prog="major", kick="four", audio="v5"),
                   cover=dict(words=["$20K A YEAR?", "YOU'RE IN THE", "TOP 10% ON EARTH."], kicker="Where your income ranks globally."))
light_look(EP, ORDER)

TOPS = [.9, 1.3, 1.8, 2.5, 3.4, 4.7, 6.8, 10.5, 20, 20]     # $k per year, decile upper edges (schematic except 3.4 and 20)
XS = [95 + i * 99 for i in range(10)]
BW, BASE, PX = 66, 1120, 26.0
def top(v): return BASE - v * PX

T_CARD = .45;  D_CARD = .7
T_STAMP = cue("hook", "nine in ten") - .05
T_REW = S("setup") - .05
T_GROW = S("setup") + .2;  D_GROW = 1.4
T_EXP = S("explain") - .05
T_MED = cue("median", "middle") - .15
T_TOP = S("reveal") + .05; T_HALF = cue("reveal", "Germany") - .15
T_BACK = E("why") - 1.0

def grow(t):
    """bar heights: full at the start (frame 0 = cover), shrink to 0 at the rewind, grow back in setup"""
    if t < T_REW: return TOPS
    k = [ease_io(clamp((t - T_GROW - i * .07) / (D_GROW * .6))) for i in range(10)]
    if t < T_GROW: k = [max(0, 1 - (t - T_REW) / .25)] * 10
    return [v * kk for v, kk in zip(TOPS, k)]

def person(d, x, y, col):
    d.ellipse([x - 13, y - 62, x + 13, y - 36], fill=col)
    d.chord([x - 24, y - 32, x + 24, y + 16], 180, 360, fill=col)

def card(d, cx, cy, s=1.0):
    w, h = 190 * s, 104 * s
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=int(16 * s), fill=WHITE, outline=INK, width=5)
    d.text((cx, cy - 18 * s), "TAKE-HOME", font=F(MONO, int(20 * s)), fill=MID, anchor="mm")
    d.text((cx, cy + 16 * s), "$20K", font=F(BLK, int(46 * s)), fill=INK, anchor="mm")

def objects(L, d, t):
    h = grow(t); cur = EP.current(t)
    for i, x in enumerate(XS):
        hot = (cur == "explain" and t >= T_EXP + i * .07) or (cur == "median" and i == 4 and t >= T_MED) or \
              (i == 9 and (T_STAMP <= t < T_REW or (cur == "reveal" and t >= T_TOP) or (cur == "why" and t < T_BACK)))
        y = top(h[i])
        d.rectangle([x - BW / 2, y, x + BW / 2, BASE], fill=INK if hot else MID)
        if i == 9 and h[i] > 1:                                       # the top tenth goes far beyond: arrow out of the frame
            d.polygon([(x - 20, y - 4), (x + 20, y - 4), (x, y - 30)], fill=INK if hot else MID)
        person(d, x, (y - 34) if i == 9 else (y - 2), INK)
    d.line([(55, BASE), (1030, BASE)], fill=INK, width=4)
    if t < T_REW:                                                     # cold open: the payslip card drops onto the top bar
        k = spring(clamp((t - T_CARD) / D_CARD)); cy = -200 + (530 + 200) * k if t >= T_CARD else -400
        if t >= T_CARD: card(d, XS[9] - 190, cy)
    if cur == "reveal" and t >= T_HALF or (cur == "why" and t < T_BACK):
        card(d, XS[9] - 190, 530, .85)

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

def dashed(d, y, col):
    x = 55
    while x < 1030: d.line([(x, y), (min(x + 22, 1030), y)], fill=col, width=4); x += 38

def labels(d, t):
    cur = EP.current(t)
    show20 = (T_CARD + .5 <= t < T_REW) or (t >= T_TOP and t < T_BACK)
    if show20:
        dashed(d, top(20), SIG if cur == "reveal" else INK)
        d.text((55, top(20) - 14), "$20K", font=F(BLK, 34), fill=SIG if cur == "reveal" else INK, anchor="lb")
    if T_STAMP <= t < T_REW + .2: stamp(d, (330, 700), "TOP 10%", t, T_STAMP, size=82)
    if T_GROW + .8 <= t < T_BACK:
        d.text((XS[0] - 30, BASE + 28), "POOREST", font=F(MONO, 22), fill=MID, anchor="lm")
        d.text((XS[9] + 30, BASE + 28), "RICHEST", font=F(MONO, 22), fill=MID, anchor="rm")
    if cur in ("median", "reveal", "why") and t >= T_MED and t < T_BACK:
        d.text((XS[4], top(3.4) - 84), "$3.4K", font=F(BLK, 40), fill=INK, anchor="mm")
        d.text((XS[4], top(3.4) - 120), "MIDDLE", font=F(MONO, 22), fill=MID, anchor="mm")
    if cur == "reveal" and t >= T_HALF or (cur == "why" and t < T_BACK):
        d.text((540, top(20) + 70), "GERMANY / US: OVER HALF ARE HERE", font=F(BLK, 34), fill=SIG if cur == "reveal" else INK, anchor="mm")

def head(d, t, line):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    d.text((X0, 400), "WORLD MIDDLE", font=F(MONO, 30), fill=MID)
    d.text((X0 + 250, 388), "$3.4K / YEAR" if t >= T_MED else "?", font=F(BLK, 64), fill=INK)

def draw(img, d, t, line, note="after tax · one person · intl. $ · bars schematic"):
    shadowed(img, t); d = ImageDraw.Draw(img); labels(d, t); head(d, t, line); fig(d, note)

def sc_hook(img, d, t): draw(img, d, t, "RICH ON EARTH?")
def sc_setup(img, d, t): draw(img, d, t, "EVERYONE, LINED UP")
def sc_explain(img, d, t): draw(img, d, t, "1 BAR = 1/10 OF US")
def sc_median(img, d, t): draw(img, d, t, "THE MIDDLE.")
def sc_reveal(img, d, t): draw(img, d, t, "THE TOP TENTH.")
def sc_why(img, d, t): draw(img, d, t, "RICH ON EARTH." if t < T_BACK else "RICH ON EARTH?")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.scenes = {"hook": sc_hook, "setup": sc_setup, "explain": sc_explain, "median": sc_median, "reveal": sc_reveal, "why": sc_why}
FX = [(T_CARD, whoosh(.5, .04), .5), (T_CARD + D_CARD * .5, thud(.45), .5), (T_STAMP, thud(.5), -.3),
      (T_REW, whoosh(.5, .05), 0), *[(T_GROW + .3 + i * .07, tick(.02), -.6 + i * .13) for i in range(10)],
      *[(T_EXP + i * .07, tick(.02), -.6 + i * .13) for i in range(0, 10, 2)], (T_MED, pop(.14), -.1),
      (S("reveal") + .05, thud(.55), 0), (T_HALF, pop(.16), .3), (T_BACK, whoosh(.6, .05), 0)]
if __name__ == "__main__": EP.run(FX)
