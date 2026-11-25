"""NOT JUST YOU – No. 151: is Black Friday really the cheapest day? (cliché check, single cliché, posted on Black Friday 27.11.2026)
Which? (2023): 208 products on sale on Black Friday 2022 at eight UK retailers, prices tracked daily six months before and after:
5 of 208 (2 %) cheapest on Black Friday, 98 % the same or cheaper on another day (86 % even for 18 Nov – 2 Dec).
ONE continuous object: 208 price tags (16 x 13 grid, 1 tag = 1 product) above a year strip with Black Friday in the middle.
Cold open: the tags pop in as orange 'deals', "CHEAPEST?" stamp. Setup: tags go neutral, a playhead runs through the year.
Reveal on black: only 5 tags light up. 'other': the 203 others fill in, FALSE stamp. Payoff (rule 15): 5 orange tags + FALSE stay."""
import os, sys, math
import numpy as np
from PIL import ImageDraw
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from fx2 import light_look, is_light, stamp
from stand import shadowed
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .5, "setup": .5, "reveal": .8, "other": .7, "why": .1})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "setup", "reveal", "other", "why", "end"]
EP = ThreadEpisode(TL, 151, "BLACK FRIDAY", order=ORDER, dark=True, label="WHICH? · 208 DEALS · UK 2022",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Which? (2023), Only 2% of discounted products", "are cheapest on Black Friday · UK, 2022"),
                   music=dict(bpm=100, root=3, prog="major", kick="four", audio="v5"),
                   cover=dict(words=["IS BLACK FRIDAY", "REALLY THE", "CHEAPEST DAY?"], kicker="Cliché check."))
light_look(EP, ORDER)

N, COLS = 208, 16
GX0, GDX, GY0, GDY = 92, 56.6, 520, 41
TW, TH = 40, 28                                              # one price tag
def tag_xy(i): r, c = divmod(i, COLS); return GX0 + c * GDX, GY0 + r * GDY
WIN = [21, 70, 107, 148, 190]                                # the 5 products that were cheapest on Black Friday (positions schematic)
SY, SX0, SX1 = 1112, 90, 990                                 # year strip
SXM = (SX0 + SX1) / 2

T_POP = .15
T_STAMP = cue("hook", "cheapest") - .1
T_NEUTRAL = S("setup") + .05
T_SWEEP0, T_SWEEP1 = cue("setup", "every day") - .1, E("setup") + .2
T_FIVE = cue("reveal", "Only five") - .1; T_PCT = cue("reveal", "two percent") - .15
T_REST = cue("other", "ninety-eight") - .2; T_FALSE = cue("other", "false") - .15

def tag(d, x, y, col, s=1.0):
    w, h = TW * s / 2, TH * s / 2
    d.rounded_rectangle([x - w, y - h, x + w, y + h], radius=int(6 * s), fill=col)
    d.ellipse([x - w + 5 * s, y - 3 * s, x - w + 11 * s, y + 3 * s], fill=BG if s > .3 else col)

def objects(L, d, t):
    cur = EP.current(t)
    for i in range(N):
        x, y = tag_xy(i); win = i in WIN
        s = spring(clamp((t - T_POP - (i % COLS) * .03 - (i // COLS) * .02) / .4))
        if t < T_NEUTRAL: col = SIG
        elif t < T_FIVE: col = INK
        elif t < T_REST:
            col = SIG if win and t >= T_FIVE + (WIN.index(i) * .08) else MID
            if win: s *= 1 + .3 * clamp((t - T_FIVE - WIN.index(i) * .08) / .35) + .35 * math.sin(math.pi * clamp((t - T_FIVE - WIN.index(i) * .08) / .35))
        else:
            if win: col = SIG; s *= 1.3
            else: col = INK if t >= T_REST + (i % COLS) * .02 + (i // COLS) * .015 else MID
        if s > .02: tag(d, x, y, col, s)
    # the year strip: six months before | Black Friday | six months after
    if t >= T_NEUTRAL:
        k = ease(clamp((t - T_NEUTRAL) / .5))
        d.line([(SXM - (SXM - SX0) * k, SY), (SXM + (SX1 - SXM) * k, SY)], fill=INK, width=4)
        d.line([(SXM, SY - 16), (SXM, SY + 16)], fill=SIG, width=6)
        if k > .8:
            d.text((SX0, SY + 34), "6 MONTHS BEFORE", font=F(MONO, 22), fill=MID, anchor="lm")
            d.text((SX1, SY + 34), "6 MONTHS AFTER", font=F(MONO, 22), fill=MID, anchor="rm")
            d.text((SXM, SY - 34), "BLACK FRIDAY", font=F(MONO, 22), fill=SIG, anchor="mm")
        if T_SWEEP0 <= t:                                    # the playhead: every day, the whole year
            u = ease_io(clamp((t - T_SWEEP0) / (T_SWEEP1 - T_SWEEP0))); px = SX0 + (SX1 - SX0) * u
            if u < 1:
                d.ellipse([px - 11, SY - 11, px + 11, SY + 11], fill=INK)
                d.text((px, SY + 62), f"DAY {int(1 + 364 * u)}", font=F(BLK, 24), fill=INK, anchor="mm")

def stamp_box(d, c, text, t, t0, size=90, col=None, ang=-12):
    """like fx2.stamp, but on a solid paper card: the stamp sits on top of the busy tag grid and must stay readable"""
    from PIL import Image as _I, ImageDraw as _D
    if t < t0: return
    k = clamp((t - t0) / .22); s = 2.2 - 1.2 * ease(k) + (.12 * math.sin(math.pi * clamp((t - t0 - .22) / .18)) if t > t0 + .22 else 0)
    col = col or SIG; f = F(BLK, int(size * s)); tw = d.textlength(text, font=f); pad = size * s * .22
    im = _I.new("RGBA", (int(tw + 4 * pad), int(size * s * 1.6)), (0, 0, 0, 0)); g = _D.Draw(im)
    g.rounded_rectangle([pad * .5, pad * .5, im.width - pad * .5, im.height - pad * .5], radius=int(pad * .6), fill=BG + (255,),
                        outline=col + (255,), width=max(3, int(8 * s)))
    g.text((im.width / 2, im.height / 2), text, font=f, fill=col + (255,), anchor="mm")
    im = im.rotate(ang, expand=True, resample=_I.BICUBIC)
    d._image.paste(im, (int(c[0] - im.width / 2), int(c[1] - im.height / 2)), im)

def labels(d, t):
    if T_STAMP <= t < S("setup") + .3: stamp_box(d, (540, 790), "CHEAPEST?", t, T_STAMP, size=90)
    if t >= T_FALSE: stamp_box(d, (600, 965), "FALSE", t, T_FALSE, size=110)

def head(d, t, line):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    if t >= T_REST:
        d.text((X0, 400), "AS CHEAP OR CHEAPER ANOTHER DAY", font=F(MONO, 30), fill=MID)
        d.text((X0 + 640, 388), "98%", font=F(BLK, 56), fill=INK)
    elif t >= T_FIVE:
        d.text((X0, 400), "CHEAPEST ON BLACK FRIDAY", font=F(MONO, 30), fill=MID)
        d.text((X0 + 480, 388), "2%" if t >= T_PCT else "5 OF 208", font=F(BLK, 56), fill=SIG)
    else:
        d.text((X0, 400), "CHEAPEST ON BLACK FRIDAY", font=F(MONO, 30), fill=MID)
        d.text((X0 + 480, 388), "?", font=F(BLK, 56), fill=INK)

def draw(img, d, t, line, note="1 tag = 1 product · 8 UK retailers · Black Friday 2022"):
    shadowed(EP, img, t, objects); d = ImageDraw.Draw(img); labels(d, t); head(d, t, line); fig(d, note)

def sc_hook(img, d, t): draw(img, d, t, "CHEAPEST DAY?")
def sc_setup(img, d, t): draw(img, d, t, "208 DEALS. 1 YEAR.", note="Which?: prices tracked daily, 6 months before and after")
def sc_reveal(img, d, t): draw(img, d, t, "ONLY 5.")
def sc_other(img, d, t): draw(img, d, t, "98% ELSEWHERE.", note="even for the 2 weeks around Black Friday: 86%")
def sc_why(img, d, t): draw(img, d, t, "CHECK THE HISTORY.")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.scenes = {"hook": sc_hook, "setup": sc_setup, "reveal": sc_reveal, "other": sc_other, "why": sc_why}
FX = [*[(T_POP + .1 + j * .05, tick(.012), -.6 + j * .08) for j in range(16)], (T_STAMP, thud(.3), 0),
      (T_NEUTRAL, whoosh(.4, .03), 0), (T_SWEEP0, whoosh(.6, .02), -.5),
      (S("reveal") + .05, thud(.35), 0), *[(T_FIVE + j * .08, pop(.1), -.6 + j * .3) for j in range(5)],
      (T_REST, whoosh(.5, .03), .3), (T_FALSE, thud(.35), 0)]
if __name__ == "__main__": EP.run(FX)
