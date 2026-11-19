"""NOT JUST YOU – No. 149: how much money is normal in the bank? ('Where do you stand?' format)
Federal Reserve SCF 2022, transaction accounts, families with a head under 35: mean $20,540, median $5,400.
ONE continuous object: ten bars (each = one tenth of under-35 households, smallest balance left, schematic deciles chosen so
mean = 20.5k and median ≈ 5.4k). Cold open: the last bar shoots up out of frame and drags a dashed AVERAGE line up with it,
"AVERAGE?" stamp. Reveal on black: the MEDIAN marker drops onto the middle bars. Payoff (rule 15): average line + median
marker + 'YOU?' next to the median. Light look."""
import os, sys, math
import numpy as np
from PIL import ImageDraw
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from fx2 import light_look, is_light, stamp
from stand import shadowed, you_marker, dashed
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .5, "setup": .5, "explain": .5, "average": .8, "reveal": .8, "why": .1})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "setup", "explain", "average", "reveal", "why", "end"]
EP = ThreadEpisode(TL, 149, "MONEY IN THE BANK", order=ORDER, dark=True, label="FEDERAL RESERVE · SCF 2022 · UNDER 35",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Federal Reserve, Survey of Consumer", "Finances 2022 · transaction accounts"),
                   music=dict(bpm=96, root=1, prog="major", kick="four", audio="v5"),
                   cover=dict(words=["HOW MUCH IN", "THE BANK IS", "NORMAL?"], kicker="Under 35, US. Where do you stand?"))
light_look(EP, ORDER)

DEC = [.3, 1, 2, 3.5, 5.4, 7, 11, 18, 35, 122]                # $k, schematic deciles (mean 20.5, median ~5.4)
MEAN, MEDIAN = 20.5, 5.4
XS = [100 + i * 98 for i in range(10)]; BW = 70
BASE, PX = 1130, 15.0                                       # 15 px per $1k -> the 35k bar = 525 px, the last one leaves the frame
def top(v): return BASE - v * PX

T_UP = .3
T_STAMP = cue("hook", "normal") - .1
T_REW = S("setup") - .05
T_GROW = cue("explain", "Each bar") - .1
T_AVG = S("average") + .1
T_MED = cue("reveal", "five thousand") - .2; T_PULL = cue("reveal", "pull") - .2
T_YOU = S("why") + .3

def heights(t):
    if t < T_REW:                                            # cold open: everything up, the last bar shoots out of the frame
        return [v * spring(clamp((t - T_UP - i * .04) / .5)) for i, v in enumerate(DEC)]
    if t < T_GROW: return [v * (1 - ease_io(clamp((t - T_REW) / .4))) for v in DEC]
    return [v * spring(clamp((t - T_GROW - i * .08) / .55)) for i, v in enumerate(DEC)]

def objects(L, d, t):
    h = heights(t); cur = EP.current(t)
    for i, x in enumerate(XS):
        hot = (cur == "reveal" and i in (4, 5) and t >= T_MED) or (cur == "reveal" and i == 9 and t >= T_PULL)
        y = max(top(h[i]), 470)
        d.rectangle([x - BW / 2, y, x + BW / 2, BASE], fill=SIG if (hot and i == 9) else INK if hot else MID)
        if top(h[i]) < 470: d.polygon([(x - 18, 482), (x + 18, 482), (x, 462)], fill=WHITE)        # 'goes on' arrow
    d.line([(55, BASE), (1030, BASE)], fill=INK, width=4)
    d.text((XS[0] - 30, BASE + 28), "SMALLEST", font=F(MONO, 22), fill=MID, anchor="lm")
    d.text((XS[9] + 30, BASE + 28), "BIGGEST", font=F(MONO, 22), fill=MID, anchor="rm")
    avg_on = (T_UP + .5 <= t < T_REW) or t >= T_AVG
    if avg_on:
        k = 1 if t < T_REW else ease(clamp((t - T_AVG) / .5)); y = BASE - (BASE - top(MEAN)) * k
        dashed(d, (55, y), (1030, y), INK if cur != "reveal" else MID, w=5)
        d.text((60, y - 14), f"AVERAGE ${MEAN:.1f}K", font=F(BLK, 34), fill=INK if cur != "reveal" else MID, anchor="lb")
    if t >= T_MED and cur in ("reveal", "why", "end"):
        k = spring(clamp((t - T_MED) / .5)); x = (XS[4] + XS[5]) / 2; y = top(MEDIAN) - 30 - 60 * (1 - k)
        d.line([(x, y), (x, top(MEDIAN) - 4)], fill=SIG, width=6)
        f = F(BLK, 36); w = d.textlength("MIDDLE $5.4K", font=f)
        d.rounded_rectangle([x - w / 2 - 14, y - 58, x + w / 2 + 14, y], radius=12, fill=SIG)
        d.text((x, y - 29), "MIDDLE $5.4K", font=f, fill=WHITE, anchor="mm")
    if cur in ("why", "end"): you_marker(d, XS[3], top(DEC[3]) - 8, t, T_YOU)

def labels(d, t):
    if T_STAMP <= t < T_REW + .2: stamp(d, (700, 760), "AVERAGE?", t, T_STAMP, size=90)

def head(d, t, line):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    cur = EP.current(t)
    if t >= T_MED:
        d.text((X0, 400), "TYPICAL (MEDIAN)", font=F(MONO, 30), fill=MID); d.text((X0 + 340, 388), "$5,400", font=F(BLK, 56), fill=SIG)
    else:
        d.text((X0, 400), "AVERAGE", font=F(MONO, 30), fill=MID)
        d.text((X0 + 170, 388), "$20,540" if (t >= T_AVG or T_STAMP <= t < T_REW) else "?", font=F(BLK, 56), fill=INK)

def draw(img, d, t, line, note="US households, head under 35 · bars schematic"):
    shadowed(EP, img, t, objects); d = ImageDraw.Draw(img); labels(d, t); head(d, t, line); fig(d, note)

def sc_hook(img, d, t): draw(img, d, t, "WHAT'S NORMAL?")
def sc_setup(img, d, t): draw(img, d, t, "THE FED CHECKED.", note="checking, savings, money market · 2022")
def sc_explain(img, d, t): draw(img, d, t, "1 BAR = 1/10")
def sc_average(img, d, t): draw(img, d, t, "THE AVERAGE.")
def sc_reveal(img, d, t): draw(img, d, t, "THE MIDDLE.")
def sc_why(img, d, t): draw(img, d, t, "COMPARE TO THE MIDDLE.")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.scenes = {"hook": sc_hook, "setup": sc_setup, "explain": sc_explain, "average": sc_average, "reveal": sc_reveal, "why": sc_why}
FX = [(T_UP, whoosh(.4, .03), .4), *[(T_UP + .1 + i * .04, tick(.012), -.6 + i * .13) for i in range(10)], (T_STAMP, thud(.3), 0),
      (T_REW, whoosh(.4, .03), 0), *[(T_GROW + .2 + i * .08, tick(.012), -.6 + i * .13) for i in range(10)], (T_AVG, pop(.12), 0),
      (S("reveal") + .05, thud(.35), 0), (T_MED, pop(.14), 0), (T_PULL, whoosh(.3, .025), .6), (T_YOU, pop(.12), -.2)]
if __name__ == "__main__": EP.run(FX)
