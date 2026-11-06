"""NOT JUST YOU – No. 117: thinking about breaking up and staying – people who believed their partner needed the relationship
were less likely to leave, even when unhappy themselves (Joel, Impett, Spielmann & MacDonald 2018, JPSP; 1,348 + 500 people).
Look C+D · statement opener with "you" · isometric: two 'need' columns, the partner's taller · orange reveal: partner needs them."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"study": .6, "who": .5, "result": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["study", "who", "result", "point", "end"]
EP = ThreadEpisode(TL, 117, "STAY OR LEAVE", order=ORDER, dark=True, label="2 STUDIES · 1,848 PEOPLE",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Joel, Impett, Spielmann & MacDonald (2018), J. of", "Personality and Social Psychology 115(5)"),
                   music=dict(bpm=88, root=-3, prog="tense", kick="half", audio="v5", gaps=[(E("study") + .05, S("who") + .05)]),
                   cover=dict(words=["YOU'VE THOUGHT", "ABOUT", "BREAKING UP."], kicker="And stayed. Here's why."))

def sc_study(img, d, t):
    t0, tf = S("study"), cue("study", "Then five hundred") - .1
    counter(d, X0, 320, t, t0 + .1, .8, 1348, "{:,.0f}", 210, INK)
    d.text((X0 + 6, 545), "people in relationships · 10 weeks", font=F(COND, 46), fill=INK)
    if t >= tf:
        counter(d, X0, 640, t, tf, .5, 500, "+ {:.0f}", 130, MID)
        d.text((X0 + 6, 800), "thinking about leaving · 2 months", font=F(COND, 44), fill=MID)
    dot_field(d, (X0 + 14, 880, X1, 1110), t, cell=30, col=MID, hit={22, 60} if t >= tf else set(), hitcol=INK)
    fig(d, "followed over time")

def sc_who(img, d, t):
    t0 = S("who"); words_in(d, t, [("SO WHO", t0 + .05, 320, 170, INK), ("STAYED?", t0 + .2, 500, 170, INK)])
    for i, x in enumerate((X0 + 160, X0 + 480)):            # two doors: stay / go
        k = ease(clamp((t - t0 - .3 - i * .15) / .3)); y0 = 740
        d.rectangle([x - 100, y0, x + 100, y0 + 240 * k], outline=MID, width=8)
        if k > .9: d.text((x, y0 + 262), ("STAY", "GO")[i], font=F(MONO, 30), fill=MID, anchor="ma")
    fig(d, "schematic")

I = Iso(500, 950, .85)
def sc_result(img, d, t):
    t0, te = S("result"), cue("result", "Even when") - .1
    words_in(d, t, [("THEIR PARTNER", t0 + .05, 320, 110, SIG), ("NEEDED THEM.", t0 + .2, 430, 110, SIG)])
    I.grid(img)
    for i, (x, y, lab, v) in enumerate(((-180, 180, "YOUR HAPPINESS", .35), (180, -180, "PARTNER NEEDS YOU", 1.0))):
        k = ease(clamp((t - t0 - .3 - i * .3) / .5)); h = max(6, 330 * v * k)
        if lab.startswith("YOUR") and t < te: continue
        I.box(d, x, y, 0, 120, 120, h, top=TOP if i == 0 else SIG)
        fx, fy = I.P(x + 120, y + 120, 0); d.text((fx, fy + 14), lab, font=F(MONO, 24), fill=INK, anchor="ma")
    if t >= te: box_label(d, X0 + 4 - (1 - ease((t - te) / .2)) * 40, 560, "EVEN WHEN UNHAPPY", 44, WHITE, INK, font=BLK)
    fig(d, "a link, not proof · schematic")

def sc_point(img, d, t):
    t0, tn = S("point"), cue("point", "don't forget") - .15
    words_in(d, t, [("STAYING", t0 + .05, 320, 150, MID), ("OFTEN = CARING.", t0 + .2, 470, 110, MID)])
    if t >= tn: words_in(d, t, [("YOUR NEEDS", tn, 640, 150, SIG), ("COUNT TOO.", tn + .15, 790, 150, SIG)])
    fig(d, "fig. 2 — both of you")

EP.cuts = {"result": "stay"}
EP.bg = {"result": "light"}
EP.scenes = {"study": sc_study, "who": sc_who, "result": sc_result, "point": sc_point}
FX = [*EP.cut_fx(), (S("study") + .1, riser(.8, .04), 0), (cue("study", "Then five hundred") - .1, pop(.13), .2),
      (S("who") + .3, thud(.4), -.3), (S("who") + .45, thud(.4), .3),
      (S("result") + .05, thud(.55), 0), (S("result") + .6, pop(.14), .3), (cue("result", "Even when") - .1, pop(.14), -.3),
      (S("point") + .1, pop(.12), 0), (cue("point", "don't forget") - .15, thud(.5), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
