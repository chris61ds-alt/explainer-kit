"""NOT JUST YOU – No. 100: hours to make a friend – ~50 h casual friend, ~90 h friend, 200+ h close friend (Hall 2019).
Look C+D · guess opener · isometric hour cubes (1 cube = 10 hours) on light paper, the close-friend stack as orange reveal."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .6, "casual": .5, "friend": .5, "close": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "casual", "friend", "close", "point", "end"]
EP = ThreadEpisode(TL, 100, "FRIEND HOURS", order=ORDER, dark=True, label="SURVEY · 467 PEOPLE",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Hall (2019), How many hours does it take to make", "a friend?, J. of Social and Personal Relationships"),
                   music=dict(bpm=100, root=2, prog="major", kick="four", audio="v5", gaps=[(E("study") + .05, S("casual") + .05)]),
                   cover=dict(words=["A CLOSE FRIEND", "TAKES 200+", "HOURS."], kicker="Casual friend: 50. Friend: 90."))
I = Iso(530, 900, .9)
COLS = [(-290, 90, 5, "CASUAL", "50 H", "casual"), (-50, -40, 9, "FRIEND", "90 H", "friend"), (190, -190, 20, "CLOSE", "200+ H", "close")]

def sc_hook(img, d, t):
    t0 = S("hook")
    words_in(d, t, [("MORE THAN", t0 + .05, 320, 150, INK), ("YOU THINK.", t0 + .2, 470, 150, SIG)])
    clock(d, 480, 880, 120, (t - t0) / 1.6)
    fig(d, "fig. 1 — schematic")

def sc_study(img, d, t):
    t0, tc = S("study"), cue("study", "followed new") - .1
    counter(d, X0, 320, t, t0 + .1, .8, 355, "{:.0f}", 230, INK)
    d.text((X0 + 6, 570), "adults who had just moved", font=F(COND, 46), fill=INK)
    if t >= tc: counter(d, X0, 660, t, tc, .6, 112, "+ {:.0f}", 120, MID); d.text((X0 + 6, 800), "new college students, followed for weeks", font=F(COND, 40), fill=MID)
    dot_field(d, (X0 + 14, 880, X1, 1110), t, cell=30, col=MID, hit={44} if t < tc else {44, 12, 70, 101, 150}, hitcol=INK)
    fig(d, "online survey + follow-up")

def stacks(img, d, t, upto):
    d.text((X0, 320), "HOURS", font=F(BLK, 150), fill=INK); d.text((X0 + 4, 480), "1 cube = 10 hours", font=F(MONO, 30), fill=MID)
    I.grid(img)
    for i, (x, y, n, lab, hrs, beat) in enumerate(COLS[:upto]):
        t0 = S(beat) + .1; top = SIG if beat == "close" else TOP
        ax, ay, az = cube_stack(I, d, t, x, y, n, t0=t0, step=.05 if n < 20 else .035, top=top, size=66)
        if t >= t0 + .3:                                   # label on the floor in front of the stack
            px, py = I.P(x + 66, y + 140, 0); col = SIG if beat == "close" else INK
            d.text((px, py + 14), hrs, font=F(BLK, 52), fill=col, anchor="ma"); d.text((px, py + 74), lab, font=F(MONO, 28), fill=col, anchor="ma")

def sc_casual(img, d, t): stacks(img, d, t, 1); fig(d, "from stranger · schematic")
def sc_friend(img, d, t): stacks(img, d, t, 2); fig(d, "from stranger · schematic")
def sc_close(img, d, t): stacks(img, d, t, 3); fig(d, "from stranger · schematic")

def sc_point(img, d, t):
    t0, tk = S("point"), cue("point", "keep showing up") - .2
    words_in(d, t, [("NOT CLICKING", t0 + .05, 320, 120, MID), ("YET?", t0 + .2, 440, 120, MID)] + ([("KEEP", tk, 600, 150, SIG), ("SHOWING UP.", tk + .15, 750, 120, SIG)] if t >= tk else []))
    fig(d, "fig. 2 — 200 hours")

EP.cuts = {"friend": "stay", "close": "stay"}
EP.bg = {"casual": "light", "friend": "light"}
EP.scenes = {"hook": sc_hook, "study": sc_study, "casual": sc_casual, "friend": sc_friend, "close": sc_close, "point": sc_point}
FX = [*EP.cut_fx(), (S("hook") + .05, thud(.45), 0), (S("hook") + .2, riser(1.2, .04), 0),
      (S("study") + .1, riser(.8, .04), 0), (cue("study", "followed new") - .1, pop(.13), .2),
      *[(S(b) + .1 + i * (.05 if n < 20 else .035), tick(.035), (i % 5 - 2) / 3) for (x, y, n, lab, hrs, b) in COLS for i in range(n)],
      (S("casual") + .4, pop(.14), -.3), (S("friend") + .4, pop(.14), 0), (S("close") + .1, thud(.55), 0), (S("close") + .8, pop(.16), .3),
      (S("point") + .1, pop(.12), 0), (cue("point", "keep showing up") - .2, thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
