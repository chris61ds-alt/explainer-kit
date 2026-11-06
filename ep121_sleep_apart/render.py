"""NOT JUST YOU – No. 121: sleeping apart – about a third of US adults sleep in another room at least sometimes because of a
bed partner; men 45 % vs. women 25 %; millennials 43 % (AASM Sleep Prioritization Survey 2023, 2,005 adults).
Look C+D · statement opener with "you" · isometric: one bed → two beds · orange reveal: men."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"survey": .6, "who": .5, "men": .6, "young": .5, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["survey", "who", "men", "young", "point", "end"]
EP = ThreadEpisode(TL, 121, "SLEEP APART", order=ORDER, dark=True, label="SURVEY · 2,005 US ADULTS",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("American Academy of Sleep Medicine (2023),", "Sleep Prioritization Survey"),
                   music=dict(bpm=88, root=-2, prog="dream", kick="half", audio="v5", gaps=[(E("survey") + .05, S("who") + .05)]),
                   cover=dict(words=["YOU SLEEP", "BETTER", "ALONE."], kicker="About 1 in 3 sleep apart, at least sometimes."))

def sc_survey(img, d, t):
    t0, tr = S("survey"), cue("survey", "Fifteen percent") - .1
    d.text((X0, 320), "ANOTHER ROOM", font=F(BLK, 110), fill=INK); d.text((X0 + 4, 445), "because of their partner", font=F(COND, 48), fill=MID)
    rows = [("SOMETIMES", 20, MID, t0 + .4), ("REGULARLY", 15, INK, tr)]
    for j, (lab, v, col, tk) in enumerate(rows):
        if t < tk: continue
        k = ease((t - tk) / .5); y = 580 + j * 210
        d.text((X0, y), lab, font=F(BLK, 50), fill=col); w = 640 * v / 20 * k
        d.rectangle([X0, y + 68, X0 + max(8, w), y + 168], fill=col)
        d.text((X0 + max(8, w) + 16, y + 118), f"{v * k:.0f} %", font=F(BLK, 64), fill=col, anchor="lm")
    fig(d, "US adults, 2023")

def sc_who(img, d, t):
    t0 = S("who"); words_in(d, t, [("WHO MOVES", t0 + .05, 320, 150, INK), ("OUT MOST?", t0 + .2, 470, 150, INK)])
    fig(d, "schematic")

def sc_men(img, d, t):
    t0, tw = S("men"), cue("men", "twenty-five") - .1
    words_in(d, t, [("MEN.", t0 + .05, 320, 200, SIG)])
    rows = [("MEN", 45, SIG, t0 + .3), ("WOMEN", 25, INK, tw)]
    for j, (lab, v, col, tk) in enumerate(rows):
        if t < tk: continue
        k = ease((t - tk) / .5); y = 600 + j * 210
        d.text((X0, y), lab, font=F(BLK, 50), fill=col); w = 640 * v / 45 * k
        d.rectangle([X0, y + 68, X0 + max(8, w), y + 168], fill=col)
        d.text((X0 + max(8, w) + 16, y + 118), f"{v * k:.0f} %", font=F(BLK, 64), fill=col, anchor="lm")
    fig(d, "sleep apart at least sometimes")

def sc_young(img, d, t):
    t0 = S("young")
    d.text((X0, 320), "BY GENERATION", font=F(BLK, 100), fill=INK)
    rows = [("MILLENNIALS", 43), ("GEN X", 33), ("GEN Z", 28), ("BOOMERS", 22)]
    for j, (lab, v) in enumerate(rows):
        k = ease(clamp((t - t0 - .15 - j * .12) / .4)); y = 470 + j * 150; col = INK if j == 0 else MID
        d.text((X0, y), lab, font=F(BLK, 40), fill=col); w = 600 * v / 43 * k
        d.rectangle([X0, y + 52, X0 + max(8, w), y + 116], fill=col)
        d.text((X0 + max(8, w) + 14, y + 84), f"{v * k:.0f} %", font=F(BLK, 48), fill=col, anchor="lm")
    fig(d, "sleep apart at least sometimes")

I = Iso(560, 1020, .5)
def sc_point(img, d, t):
    t0, tk = S("point"), cue("point", "Just keep some") - .15
    words_in(d, t, [("NOT A", t0 + .05, 320, 150, MID), ("BREAKUP.", t0 + .2, 470, 150, MID)] + ([("KEEP SOME", tk, 640, 110, SIG), ("BED TIME.", tk + .15, 750, 110, SIG)] if t >= tk else []))
    I.grid(img); I.shadow(d, 0, 0, 220)
    split = ease(clamp((t - t0 - .4) / .8))                  # one bed slides apart into two
    for sx in (-1, 1):
        dx = sx * 120 * split
        I.box(d, -250 + (0 if sx < 0 else 250) + dx, -260, 0, 250, 560, 80); I.box(d, -240 + (0 if sx < 0 else 250) + dx, -250, 80, 230, 540, 40)
        I.box(d, -220 + (0 if sx < 0 else 250) + dx, -235, 120, 190, 110, 26)
    fig(d, "fig. 2 — schematic")

EP.cuts = {"men": "stay"}
EP.bg = {"point": "light"}
EP.scenes = {"survey": sc_survey, "who": sc_who, "men": sc_men, "young": sc_young, "point": sc_point}
FX = [*EP.cut_fx(), (S("survey") + .4, pop(.13), -.2), (cue("survey", "Fifteen percent") - .1, thud(.45), .2),
      (S("who") + .1, riser(.8, .04), 0), (S("men") + .05, thud(.55), 0), (cue("men", "twenty-five") - .1, pop(.13), .3),
      *[(S("young") + .15 + j * .12, tick(.04), (j - 1.5) / 2) for j in range(4)],
      (S("point") + .4, whoosh(.8, .04), 0), (cue("point", "Just keep some") - .15, thud(.5), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
