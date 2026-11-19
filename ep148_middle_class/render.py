"""NOT JUST YOU – No. 148: are you middle class? ('Where do you stand?' format)
Pew (2024): middle income = 2/3 to 2x the median size-adjusted household income; 3-person household 2022: ~$56,600–$169,800;
US adults 2022: lower 28 %, middle 52 %, upper 19 %.
ONE continuous object: 100 dots (1 dot = 1 % of adults) lined up by income in a 20 x 5 grid, poorest left; a bracket = the
middle band. Cold open: the bracket sweeps over the dots and snaps onto the middle, "MIDDLE?" stamp. Reveal on black: inside vs
outside counted. Payoff (rule 15): band + 'YOU?' marker inside. Light look."""
import os, sys, math
import numpy as np
from PIL import ImageDraw
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from fx2 import light_look, is_light, stamp
from stand import shadowed, you_marker, dashed
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .5, "setup": .5, "explain": .5, "band": .8, "reveal": .8, "why": .1})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "setup", "explain", "band", "reveal", "why", "end"]
EP = ThreadEpisode(TL, 148, "MIDDLE CLASS?", order=ORDER, dark=True, label="PEW RESEARCH · US ADULTS · 2022",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Pew Research Center (2024), The State of", "the American Middle Class · data for 2022"),
                   music=dict(bpm=98, root=0, prog="major", kick="four", audio="v5"),
                   cover=dict(words=["ARE YOU", "MIDDLE CLASS?", "HERE'S THE LINE."], kicker="Where do you stand?"))
light_look(EP, ORDER)

LOW, MIDN, UP = 28, 53, 19                         # 28 / 52 / 19 in the report (rounding) -> 100 dots
COLS, ROWS = 20, 5
GX0, GW, GY0, GH = 70, 47, 820, 62
def dot_xy(i): c, r = divmod(i, ROWS); return GX0 + c * GW + GW / 2, GY0 + r * GH
def col_x(c): return GX0 + c * GW
BX0, BX1 = col_x(LOW / ROWS), col_x((LOW + MIDN) / ROWS)    # the band in pixels

T_SWEEP = .25
T_STAMP = cue("hook", "where the line") - .1
T_LINEUP = cue("explain", "lined up") - .2
T_BAND = S("band") + .05; T_LO_LAB = cue("band", "fifty-seven") - .1; T_HI_LAB = cue("band", "one hundred seventy") - .1
T_IN = S("reveal") + .05; T_BELOW = cue("reveal", "Twenty-eight") - .1; T_ABOVE = cue("reveal", "nineteen") - .1
T_YOU = S("why") + .3
R = np.random.RandomState(4); SCATTER = [(R.uniform(80, 1000), R.uniform(760, 1120)) for _ in range(100)]

def band_x(t):
    """the bracket: sweeps across in the cold open, rests on the middle afterwards"""
    if t < T_SWEEP: return None
    if t < S("setup"):
        k = clamp((t - T_SWEEP) / 1.2); w = BX1 - BX0
        x0 = 40 + (BX0 - 40) * ease_io(k) + 160 * math.sin(k * math.pi * 2) * (1 - k)
        return x0, x0 + w
    if t < T_BAND: return None
    return BX0, BX1

def dot_pos(i, t):
    tx, ty = dot_xy(i); sx, sy = SCATTER[i]
    if t < S("setup"): return tx, ty                                      # frame 0: already lined up (cover)
    if t < T_LINEUP:                                                      # setup: loose crowd
        k = ease_io(clamp((t - S("setup")) / .6)); return tx + (sx - tx) * k, ty + (sy - ty) * k
    k = ease_io(clamp((t - T_LINEUP - (i % 20) * .02) / .8)); return sx + (tx - sx) * k, sy + (ty - sy) * k

def objects(L, d, t):
    cur = EP.current(t); b = band_x(t)
    if b:
        d.rounded_rectangle([b[0] - 6, GY0 - 50, b[1] + 6, GY0 + (ROWS - 1) * GH + 50], radius=22,
                            fill=mix(WHITE, SIG, .12) if is_light(EP, t) else mix(BG, SIG, .25), outline=SIG, width=5)
    for i in range(100):
        x, y = dot_pos(i, t)
        zone = 0 if i < LOW else 1 if i < LOW + MIDN else 2
        col = INK
        if cur in ("reveal",):
            col = INK if zone == 1 else MID
            if zone == 0 and t >= T_BELOW: col = SIG
            if zone == 2 and t >= T_ABOVE: col = SIG
        d.ellipse([x - 15, y - 15, x + 15, y + 15], fill=col)
    if t >= T_LINEUP + .6 or t < S("setup"):                               # the income axis
        y = GY0 + (ROWS - 1) * GH + 80
        d.line([(GX0, y), (GX0 + COLS * GW, y)], fill=INK, width=4)
        d.polygon([(GX0 + COLS * GW + 18, y), (GX0 + COLS * GW, y - 10), (GX0 + COLS * GW, y + 10)], fill=INK)
        d.text((GX0, y + 30), "LOWER INCOME", font=F(MONO, 22), fill=MID, anchor="lm")
        d.text((GX0 + COLS * GW, y + 30), "HIGHER", font=F(MONO, 22), fill=MID, anchor="rm")
        if t >= T_LO_LAB:
            d.line([(BX0, y - 12), (BX0, y + 12)], fill=SIG, width=5); d.text((BX0, y + 62), "$57K", font=F(BLK, 34), fill=SIG, anchor="mm")
        if t >= T_HI_LAB:
            d.line([(BX1, y - 12), (BX1, y + 12)], fill=SIG, width=5); d.text((BX1, y + 62), "$170K", font=F(BLK, 34), fill=SIG, anchor="mm")
    if cur in ("why", "end"): you_marker(d, (BX0 + BX1) / 2, GY0 - 56, t, T_YOU)

def labels(d, t):
    cur = EP.current(t)
    if T_STAMP <= t < S("setup") + .3: stamp(d, (540, 640), "MIDDLE?", t, T_STAMP, size=96)
    if cur == "reveal":
        for x, txt, t0 in (((GX0 + BX0) / 2, "28%", T_BELOW), ((BX0 + BX1) / 2, "52%", T_IN + .3), ((BX1 + GX0 + COLS * GW) / 2, "19%", T_ABOVE)):
            if t >= t0: d.text((x, GY0 - 100), txt, font=F(BLK, 64), fill=SIG if txt != "52%" else INK, anchor="mm")

def head(d, t, line):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    d.text((X0, 400), "MIDDLE BAND · 3 PEOPLE", font=F(MONO, 30), fill=MID)
    d.text((X0 + 460, 388), "$57K–$170K" if t >= T_HI_LAB else "?", font=F(BLK, 56), fill=SIG if EP.current(t) == "band" else INK)

def draw(img, d, t, line, note="1 dot = 1% of US adults · 2022 dollars"):
    shadowed(EP, img, t, objects); d = ImageDraw.Draw(img); labels(d, t); head(d, t, line); fig(d, note)

def sc_hook(img, d, t): draw(img, d, t, "MIDDLE CLASS?")
def sc_setup(img, d, t): draw(img, d, t, "2/3 TO 2X TYPICAL", note="Pew: size-adjusted household income")
def sc_explain(img, d, t): draw(img, d, t, "1 DOT = 1%")
def sc_band(img, d, t): draw(img, d, t, "THE BAND.", note="household of 3 · 2022 · Pew")
def sc_reveal(img, d, t): draw(img, d, t, "HALF ARE INSIDE.", note="Pew: 28% / 52% / 19% (rounded)")
def sc_why(img, d, t): draw(img, d, t, "A WIDE BAND.")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.scenes = {"hook": sc_hook, "setup": sc_setup, "explain": sc_explain, "band": sc_band, "reveal": sc_reveal, "why": sc_why}
FX = [(T_SWEEP, whoosh(.5, .03), -.4), (T_STAMP, thud(.3), 0), (S("setup"), whoosh(.4, .03), 0),
      *[(T_LINEUP + .2 + j * .06, tick(.012), -.6 + j * .1) for j in range(12)], (T_BAND, pop(.12), 0), (T_LO_LAB, tick(.015), -.4),
      (T_HI_LAB, tick(.015), .4), (S("reveal") + .05, thud(.35), 0), (T_BELOW, pop(.1), -.6), (T_ABOVE, pop(.1), .6), (T_YOU, pop(.12), 0)]
if __name__ == "__main__": EP.run(FX)
