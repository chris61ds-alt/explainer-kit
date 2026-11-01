"""NOT JUST YOU – No. 87: men with no close friends, 3 % → 15 % (Survey Center on American Life 2021). Look C+D, dark."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from thread import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"study": .6, "zero": .5, "six": .5, "support": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["study", "zero", "six", "support", "point", "end"]          # opener: statement ("claim" beat, drawn by the toolkit)
EP = ThreadEpisode(TL, 87, "NO FRIENDS", order=ORDER, dark=True, label="SURVEY · 2,019 PEOPLE",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Survey Center on American Life (2021),", "The State of American Friendship"),
                   music=dict(bpm=88, root=-5, prog="tense", kick="half", audio="v5", gaps=[(E("study") + .05, S("zero") + .05)]),
                   cover=dict(words=["15 % OF MEN:", "ZERO FRIENDS."], kicker="In 1990: 3 %."))

FIELD = (X0 + 14, 760, X1, 1110)
def dot_xy(i, box=FIELD, cell=30):
    x0, y0, x1, y1 = box; cols = len(range(int(x0), int(x1), cell)); r, c = divmod(i, cols)
    return x0 + c * cell, y0 + r * cell

def sc_study(img, d, t):
    t0 = S("study")
    counter(d, X0, 320, t, t0 + .1, .8, 2019, "{:,.0f}", 230, INK)
    d.text((X0 + 6, 570), "US adults · Survey Center on American Life", font=F(COND, 40), fill=INK)
    d.text((X0 + 6, 625), "May 2021 · how many close friends do you have?", font=F(COND, 30), fill=MID)
    dot_field(d, FIELD, t, cell=30, col=MID, hit={45} if t < cue("study", "close friends") - .1 else {45, 12, 73, 101, 160, 199})
    fig(d, "compared with a 1990 survey")

def hbars(d, t, rows, vmax):
    for j, (lab, v, col, tk) in enumerate(rows):
        if t < tk - .01: continue
        k = ease((t - tk) / .6); y = 600 + j * 270
        d.text((X0, y), lab, font=F(BLK, 54), fill=col)
        w = 660 * v / vmax * k
        d.rectangle([X0, y + 75, X0 + max(6, w), y + 215], fill=col)
        d.text((X0 + max(6, w) + 16, y + 145), f"{v * k:.0f} %", font=F(BLK, 72), fill=col, anchor="lm")

def sc_zero(img, d, t):
    d.text((X0, 320), "ZERO", font=F(BLK, 170), fill=INK); d.text((X0, 490), "close friends", font=F(BLK, 70), fill=INK)
    hbars(d, t, [("MEN, 1990", 3, MID, S("zero") + .2), ("MEN, 2021", 15, SIG, S("zero") + .6)], 15)
    tf = cue("zero", "five times") - .1
    if t >= tf: box_label(d, X1, 1095, "5 × AS MANY", 44, WHITE, SIG, font=BLK, anchor="ra")
    fig(d, "men with no close friends at all")

def sc_six(img, d, t):
    d.text((X0, 320), "6 OR MORE", font=F(BLK, 150), fill=INK); d.text((X0, 490), "close friends", font=F(BLK, 70), fill=INK)
    hbars(d, t, [("MEN, 1990", 55, MID, S("six") + .2), ("MEN, 2021", 27, SIG, cue("six", "twenty-seven") - .2)], 55)
    fig(d, "men with six or more close friends")

def sc_support(img, d, t):
    t0, tm = S("support"), cue("support", "Men?") - .1
    d.text((X0, 320), "SUPPORT", font=F(BLK, 160), fill=INK)
    d.text((X0, 485), "from a friend, last week", font=F(BLK, 56), fill=INK)
    te = cue("support", "emotional support") - .1
    if t >= te: d.line([X0, 556, X0 + 640 * ease((t - te) / .4), 556], fill=INK, width=6)
    silhouette(img, lambda m: front_bust(m, 270, 800, .4, 255), (100, 690, 440, 1010), INK, cell=8)
    counter(d, 270, 1020, t, t0 + .7, .6, 41, "{:.0f} %", 90, INK, anchor="ma")
    d.text((270, 1120), "WOMEN", font=F(BLK, 34), fill=INK, anchor="ma")
    if t >= tm:
        k = ease((t - tm) / .3)
        silhouette(img, lambda m: front_bust(m, 690, 800, .4, 255), (520, 690, 860, 1010), SIG, cell=8, k=k)
        counter(d, 690, 1020, t, tm + .1, .5, 21, "{:.0f} %", 90, SIG, anchor="ma")
        d.text((690, 1120), "MEN", font=F(BLK, 34), fill=SIG, anchor="ma")

def sc_point(img, d, t):
    t0, tr = S("point"), cue("point", "You're the trend") - .2
    words_in(d, t, [("NOT THE", t0 + .2, 320, 140, MID), ("EXCEPTION.", t0 + .4, 460, 140, INK)] +
             ([("THE TREND.", tr, 640, 150, SIG)] if t >= tr else []))
    k = clamp((t - t0 - .3) / 1.2)                      # 3 % → 15 %, endpoints only (schematic line)
    x0, y0, x1, y1 = X0 + 20, 1020, X1 - 40, 900
    if k > 0:
        d.line([x0, y0, lerp(x0, x1, k), lerp(y0, y1, k)], fill=SIG, width=8)
        d.ellipse([x0 - 10, y0 - 10, x0 + 10, y0 + 10], fill=MID); d.text((x0, y0 + 20), "1990 · 3 %", font=F(BLK, 30), fill=MID)
        if k >= 1: d.ellipse([x1 - 12, y1 - 12, x1 + 12, y1 + 12], fill=SIG); d.text((x1, y1 - 20), "2021 · 15 %", font=F(BLK, 30), fill=SIG, anchor="rd")
    fig(d, "men with no close friends · line schematic")

# magic move: one man in the survey (an orange dot) grows into the 1990 bar
_dx, _dy = dot_xy(45)
EP.carry = {"zero": [((_dx - 8, _dy - 8, _dx + 8, _dy + 8), (X0, 675, X0 + 132, 815))]}

EP.scenes = {"study": sc_study, "zero": sc_zero, "six": sc_six, "support": sc_support, "point": sc_point}
FX = [(0.0, thud(.5), 0), *EP.cut_fx(), (S("study") + .1, riser(.8, .04), 0),
      (S("zero") + .2, pop(.12), 0), (S("zero") + .6, thud(.5), 0), (cue("zero", "five times") - .1, pop(.15), .3),
      (S("six") + .2, pop(.12), -.2), (cue("six", "twenty-seven") - .2, thud(.45), 0),
      (S("support") + .7, pop(.12), -.3), (cue("support", "emotional support") - .1, whoosh(.3, .05), 0), (cue("study", "close friends") - .1, pop(.12), 0), (cue("support", "Men?") - .1, thud(.45), .3),
      (cue("point", "You're the trend") - .2, thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
