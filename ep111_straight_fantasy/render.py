"""NOT JUST YOU – No. 111: same-sex fantasies – 37 % of women and 21 % of men fantasized about same-sex sex, while only 6 % /
1.5 % identified as gay (Joyal, Cossette & Lapierre 2015, 1,516 adults, 85 % straight). Look C+D · statement opener with "you" ·
isometric columns: fantasy vs. label · orange reveal: men 21 %."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"study": .6, "women": .5, "men": .6, "gap": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["study", "women", "men", "gap", "point", "end"]
EP = ThreadEpisode(TL, 111, "STRAIGHT FANTASY", order=ORDER, dark=True, label="SURVEY · 1,516 ADULTS",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Joyal, Cossette & Lapierre (2015), What exactly is an", "unusual sexual fantasy?, J. of Sexual Medicine 12(2)"),
                   music=dict(bpm=98, root=1, prog="dream", kick="four", audio="v5", gaps=[(E("study") + .05, S("women") + .05)]),
                   cover=dict(words=["YOU'RE STRAIGHT.", "AND YOU'VE HAD", "THAT FANTASY."], kicker="1 in 5 men. 37 % of women."))

def sc_study(img, d, t):
    t0, ts = S("study"), cue("study", "Eighty-five") - .1
    counter(d, X0, 320, t, t0 + .1, .8, 1516, "{:,.0f}", 230, INK)
    d.text((X0 + 6, 565), "adults, asked about their fantasies", font=F(COND, 46), fill=INK)
    n = 100; straight = set(range(85))
    if t >= ts: box_label(d, X0 + 4 - (1 - ease((t - ts) / .2)) * 40, 640, "85 % STRAIGHT", 44, WHITE, INK, font=BLK)
    dot_field(d, (X0 + 14, 760, X1, 1110), t, cell=30, col=MID, hit=set(range(0, 380, 4)) if t >= ts else set(), hitcol=INK)
    fig(d, "Quebec, Canada · schematic")

def bars(d, t, show_m):
    d.text((X0, 320), "HAD A", font=F(BLK, 120), fill=INK); d.text((X0, 440), "SAME-SEX FANTASY", font=F(BLK, 90), fill=INK)
    rows = [("WOMEN", 37, INK, S("women") + .3)] + ([("MEN", 21, SIG, S("men") + .1)] if show_m else [])
    for j, (lab, v, col, tk) in enumerate(rows):
        if t < tk: continue
        k = ease((t - tk) / .6); y = 600 + j * 250
        d.text((X0, y), lab, font=F(BLK, 54), fill=col); w = 600 * v / 37 * k
        d.rectangle([X0, y + 75, X0 + max(8, w), y + 200], fill=col)
        d.text((X0 + max(8, w) + 16, y + 137), f"{v * k:.0f} %", font=F(BLK, 72), fill=col, anchor="lm")

def sc_women(img, d, t): bars(d, t, False); fig(d, "whole sample, mostly straight")
def sc_men(img, d, t): bars(d, t, True); fig(d, "whole sample, mostly straight")

I = Iso(520, 1040, .8)
COLS = [(-330, 60, 37, "FANTASY", "WOMEN", INK), (-190, 60, 6, "SAY GAY", "WOMEN", MID), (90, -60, 21, "FANTASY", "MEN", INK), (230, -60, 1.5, "SAY GAY", "MEN", MID)]
def sc_gap(img, d, t):
    t0, tg = S("gap"), cue("gap", "only six") - .15
    d.text((X0, 320), "FANTASY", font=F(BLK, 120), fill=INK); d.text((X0, 440), "VS. LABEL", font=F(BLK, 120), fill=MID)
    I.grid(img)
    for i, (x, y, v, lab, who, col) in enumerate(COLS):
        tk = t0 + .1 + (i // 2) * .25 if lab == "FANTASY" else tg + (i // 2) * .25
        if t < tk: continue
        k = ease(clamp((t - tk) / .5)); h = max(6, v * 11 * k)
        I.box(d, x, y, 0, 100, 100, h, top=RIGHT if lab == "SAY GAY" else TOP)
        px, py = I.P(x + 50, y + 50, h); d.text((px, py - 40), f"{v:g} %", font=F(BLK, 46), fill=INK, anchor="mm")
        fx, fy = I.P(x + 50, y + 150, 0); d.text((fx, fy + 10), lab, font=F(MONO, 24), fill=col, anchor="ma"); d.text((fx, fy + 42), who, font=F(MONO, 24), fill=MID, anchor="ma")
    fig(d, "share of all 1,516 · schematic")

def sc_point(img, d, t):
    t0, tj = S("point"), cue("point", "just a fantasy") - .2
    words_in(d, t, [("A FANTASY", t0 + .05, 320, 150, MID), ("ISN'T A LABEL.", t0 + .2, 470, 120, MID)] + ([("IT'S JUST", tj, 640, 150, SIG), ("A FANTASY.", tj + .15, 790, 150, SIG)] if t >= tj else []))
    fig(d, "fig. 2 — no label needed")

EP.cuts = {"men": "stay"}
EP.bg = {"gap": "light"}
EP.scenes = {"study": sc_study, "women": sc_women, "men": sc_men, "gap": sc_gap, "point": sc_point}
FX = [*EP.cut_fx(), (S("study") + .1, riser(.8, .04), 0), (cue("study", "Eighty-five") - .1, pop(.13), .2),
      (S("women") + .3, thud(.5), 0), (S("men") + .1, thud(.55), 0), (cue("men", "One in five") - .1, pop(.14), .3),
      (S("gap") + .1, whoosh(.5, .04), -.3), (S("gap") + .35, whoosh(.5, .04), .3), (cue("gap", "only six") - .15, pop(.14), -.3), (cue("gap", "only six") + .1, pop(.14), .3),
      (S("point") + .1, pop(.12), 0), (cue("point", "just a fantasy") - .2, thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
