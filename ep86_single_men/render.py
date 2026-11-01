"""NOT JUST YOU – No. 86: most young men are single, most young women are not (Pew Research 2023). Look C+D, dark."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from thread import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .6, "men": .5, "women": .5, "looking": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "men", "women", "looking", "point", "end"]
EP = ThreadEpisode(TL, 86, "SINGLE MEN", order=ORDER, dark=True, label="SURVEY · 6,034 PEOPLE",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Pew Research Center (2023), survey of", "6,034 US adults, July 2022"),
                   music=dict(bpm=96, root=-2, prog="minor", kick="half", audio="v5", gaps=[(E("study") + .05, S("men") + .05)]),
                   cover=dict(words=["UNDER 30:", "63 % SINGLE."], kicker="Young men. Women: 34 %."))

FIELD = (X0 + 14, 760, X1, 1110)                       # dot field in the study scene; dot 40 = "him"
def dot_xy(i, box=FIELD, cell=30):
    x0, y0, x1, y1 = box; cols = len(range(int(x0), int(x1), cell)); r, c = divmod(i, cols)
    return x0 + c * cell, y0 + r * cell

def sc_hook(img, d, t):
    tw = cue("hook", "Most young women") - .1
    d.text((X0 - 4, 320), "YOUNG MEN:", font=F(BLK, 130), fill=INK)
    d.text((X0 - 6, 450), "SINGLE.", font=F(BLK, 170), fill=SIG)
    silhouette(img, lambda m: front_bust(m, 300, 860, .5, 255), (110, 740, 490, 1125), INK, cell=9)
    if t >= tw:
        k = ease((t - tw) / .3)
        silhouette(img, lambda m: front_bust(m, 680, 860, .5, 255), (490, 740, 870, 1125), MID, cell=9, k=k)
        box_label(d, 680, 700 + (1 - k) * 30, "YOUNG WOMEN: NOT", 34, WHITE, INK, font=BLK, anchor="ma")
    fig(d, "fig. 1 — under 30, United States")

def sc_study(img, d, t):
    t0 = S("study")
    counter(d, X0, 320, t, t0 + .1, .8, 6034, "{:,.0f}", 230, INK)
    d.text((X0 + 6, 570), "US adults · Pew Research · July 2022", font=F(COND, 40), fill=INK)
    d.text((X0 + 6, 625), "single = no spouse, no live-in partner, no relationship", font=F(COND, 30), fill=MID)
    dot_field(d, FIELD, t, cell=30, col=MID, hit={40})
    fig(d, "one question: are you in a relationship?")

def hbars(d, t, show_women):
    for j, (lab, v, col, tk) in enumerate((("MEN UNDER 30", 63, SIG, S("men") + .3), ("WOMEN UNDER 30", 34, INK, S("women") + .1))):
        if j == 1 and not show_women: continue
        k = ease((t - tk) / .6); y = 580 + j * 270
        d.text((X0, y), lab, font=F(BLK, 54), fill=col)
        w = 660 * v / 63 * k
        d.rectangle([X0, y + 75, X0 + w, y + 215], fill=col)
        if k > .05: d.text((X0 + w + 16, y + 145), f"{v * k:.0f} %", font=F(BLK, 72), fill=col, anchor="lm")

def sc_men(img, d, t):
    d.text((X0, 320), "SINGLE:", font=F(BLK, 170), fill=INK)
    hbars(d, t, False)
    fig(d, "not married, not living with a partner, not in a relationship")

def sc_women(img, d, t):
    d.text((X0, 320), "SINGLE:", font=F(BLK, 170), fill=INK)
    hbars(d, t, True)
    if t >= S("women") + .8: box_label(d, X1, 1080, "ABOUT HALF", 40, WHITE, SIG, font=BLK, anchor="ra")
    fig(d, "not married, not living with a partner, not in a relationship")

def row(d, y, n, filled, col, t, tk):
    for i in range(n):
        x = X0 + 20 + i * 42; on = i < filled * ease((t - tk) / .8)
        d.ellipse([x - 15, y - 15, x + 15, y + 15], fill=col if on else None, outline=col if on else MID, width=3)

def sc_looking(img, d, t):
    t0, tw = S("looking"), cue("looking", "Only thirty-five") - .2
    d.text((X0, 320), "LOOKING", font=F(BLK, 160), fill=INK)
    d.text((X0, 480), "for someone", font=F(BLK, 80), fill=INK)
    d.text((X0, 640), "SINGLE MEN", font=F(BLK, 44), fill=INK); counter(d, X1, 630, t, t0 + .6, .6, 50, "{:.0f} %", 60, SIG, anchor="ra")
    row(d, 740, 20, 10, SIG, t, t0 + .6)
    if t >= tw:
        d.text((X0, 840), "SINGLE WOMEN", font=F(BLK, 44), fill=INK); counter(d, X1, 830, t, tw, .6, 35, "{:.0f} %", 60, INK, anchor="ra")
        row(d, 940, 20, 7, INK, t, tw)
    fig(d, "singles of all ages · 1 dot = 5 %")

def sc_point(img, d, t):
    t0, tm = S("point"), cue("point", "You're the majority") - .2
    words_in(d, t, [("NOT", t0 + .2, 320, 150, MID), ("BEHIND.", t0 + .4, 470, 170, INK)] +
             ([("THE", tm, 680, 120, INK), ("MAJORITY.", tm + .15, 800, 150, SIG)] if t >= tm else []))
    for i in range(10):                                  # 6 of 10 young men (63 %), schematic
        x = X0 + 45 + i * 84; k = ease((t - t0 - .3 - i * .05) / .3)
        if k > 0: silhouette(img, lambda m, x=x: front_bust(m, x, 1000, .14, 255), (x - 42, 960, x + 42, 1080), SIG if i < 6 else MID, cell=5, k=k)
    fig(d, "fig. 2 — about 6 in 10 men under 30 · schematic")

# magic move: the man from the hook becomes one dot in the survey · the bars stay and grow
_dx, _dy = dot_xy(40)
EP.carry = {"study": [((110, 740, 490, 1125), (_dx - 7, _dy - 7, _dx + 7, _dy + 7))]}
EP.cuts = {"women": "stay"}

EP.scenes = {"hook": sc_hook, "study": sc_study, "men": sc_men, "women": sc_women, "looking": sc_looking, "point": sc_point}
FX = [(0.0, thud(.5), 0), (cue("hook", "Most young women") - .1, pop(.15), .3), *EP.cut_fx(), (S("study") + .1, riser(.8, .04), 0),
      (S("men") + .3, thud(.5), 0), (S("women") + .1, thud(.45), 0), (S("women") + .8, pop(.15), .3),
      (S("looking") + .6, pop(.12), -.2), (cue("looking", "Only thirty-five") - .2, pop(.12), .2),
      (cue("point", "You're the majority") - .2, thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
