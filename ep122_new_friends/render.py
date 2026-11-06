"""NOT JUST YOU – No. 122: no new friends in years – phone contacts peak at ~25, shrink, plateau in the late 40s (Bhattacharya,
Dunbar et al. 2016, 3.2 million users); a close friend takes 200+ hours (Hall 2019). Look C+D · statement opener with "you" ·
isometric contact columns by age · orange reveal: 25."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"study": .5, "peak": .6, "after": .5, "hours": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["study", "peak", "after", "hours", "point", "end"]
EP = ThreadEpisode(TL, 122, "NEW FRIENDS", order=ORDER, dark=True, label="PHONE DATA · 3.2 MILLION USERS",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Bhattacharya, Ghosh, Monsivais, Dunbar & Kaski (2016),", "R. Soc. Open Sci. 3(4) · Hall (2019), JSPR 36(4)"),
                   music=dict(bpm=96, root=-1, prog="dream", kick="four", audio="v5", gaps=[(E("study") + .05, S("peak") + .05)]),
                   cover=dict(words=["YOU HAVEN'T MADE", "A NEW FRIEND", "IN YEARS."], kicker="It's not you. It's your age."))

def sc_study(img, d, t):
    t0, th = S("study"), cue("study", "How many people") - .1
    counter(d, X0, 320, t, t0 + .1, .8, 3.2, "{:.1f} M", 230, INK)
    d.text((X0 + 6, 565), "phone users · their calls", font=F(COND, 46), fill=INK)
    if t >= th: box_label(d, X0 + 4 - (1 - ease((t - th) / .2)) * 40, 640, "HOW MANY CONTACTS?", 44, WHITE, INK, font=BLK)
    dot_field(d, (X0 + 14, 760, X1, 1110), t, cell=26, col=MID, hit=set(range(0, 600, 7)), hitcol=INK)
    fig(d, "one European country, 2007")

I = Iso(470, 1050, .7)
AGES = [(18, .78), (25, 1.0), (35, .74), (45, .58), (55, .57), (65, .45)]
def columns(img, d, t, t0, hi=True, upto=6):
    I.grid(img)
    for i, (age, v) in enumerate(AGES[:upto]):
        k = ease(clamp((t - t0 - i * .12) / .4)); x, y = -330 + i * 130, 330 - i * 130; h = max(6, 420 * v * k)
        I.box(d, x, y, 0, 90, 90, h, top=SIG if (hi and age == 25) else TOP)
        fx, fy = I.P(x + 90, y + 90, 0); d.text((fx, fy + 12), str(age), font=F(BLK, 34), fill=SIG if (hi and age == 25) else INK, anchor="ma")

def sc_peak(img, d, t):
    t0 = S("peak"); words_in(d, t, [("PEAK AT 25.", t0 + .05, 320, 150, SIG)])
    columns(img, d, t, t0 + .1)
    fig(d, "contacts by age · schematic shape")

def sc_after(img, d, t):
    t0, tl = S("after"), cue("after", "levels off") - .1
    words_in(d, t, [("THEN IT", t0 + .05, 320, 150, INK), ("SHRINKS.", t0 + .2, 470, 150, INK)])
    columns(img, d, t, t0 - 3, hi=False)
    if t >= tl: box_label(d, X1, 640, "LEVELS OFF ~45", 44, WHITE, INK, font=BLK, anchor="ra")
    fig(d, "contacts by age · schematic shape")

def sc_hours(img, d, t):
    t0 = S("hours")
    counter(d, X0, 320, t, t0 + .1, .8, 200, "{:.0f}+", 230, INK)
    d.text((X0 + 6, 565), "hours together for a close friend", font=F(COND, 46), fill=INK)
    clock(d, 480, 850, 140, (t - t0 - .2) / 1.4)
    fig(d, "Hall 2019 · see No. 100")

def sc_point(img, d, t):
    t0, tl, tp = S("point"), cue("point", "Life got full") - .15, cue("point", "Pick one person") - .15
    words_in(d, t, [("NOT HARD", t0 + .05, 320, 140, MID), ("TO LIKE.", t0 + .2, 460, 140, MID)])
    if t >= tl: words_in(d, t, [("LIFE GOT FULL.", tl, 610, 110, INK)])
    if t >= tp: words_in(d, t, [("PICK ONE.", tp, 760, 130, SIG), ("KEEP SHOWING UP.", tp + .2, 900, 100, SIG)])
    fig(d, "fig. 2 — one person")

EP.cuts = {"after": "stay"}
EP.bg = {"peak": "light", "after": "light"}
EP.scenes = {"study": sc_study, "peak": sc_peak, "after": sc_after, "hours": sc_hours, "point": sc_point}
FX = [*EP.cut_fx(), (S("study") + .1, riser(.8, .04), 0), (cue("study", "How many people") - .1, pop(.13), .2),
      (S("peak") + .05, thud(.55), 0), *[(S("peak") + .1 + i * .12, tick(.04), (i - 2.5) / 3) for i in range(6)],
      (S("after") + .1, whoosh(.6, .04), .2), (cue("after", "levels off") - .1, pop(.13), .3),
      (S("hours") + .1, riser(.9, .04), 0), (S("hours") + .9, thud(.45), 0),
      (S("point") + .1, pop(.12), 0), (cue("point", "Life got full") - .15, pop(.13), 0), (cue("point", "Pick one person") - .15, thud(.5), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
