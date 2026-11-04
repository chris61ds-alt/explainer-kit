"""NOT JUST YOU – No. 108 (Bodies: all normal 2/2): average erect length 13.1 cm (Veale et al. 2015, up to 15,521 men);
55 % of men happy with their size, 85 % of women with their partner's (Lever et al. 2006). Look C+D · no anatomical drawings."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
HERE = os.path.dirname(os.path.abspath(__file__))
from bodies import *
TL = Timeline(HERE, lead=.15, gaps={"study": .6, "avg": .5, "worry": .5, "partners": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["study", "avg", "worry", "partners", "point", "end"]
EP = ThreadEpisode(TL, 108, "ALL NORMAL 2", order=ORDER, dark=True, label="REVIEW · 15,521 MEN",
                   chapters={k: "" for k in ORDER[:-1]}, sources=("Veale et al. (2015), BJU International 115(6) ·", "Lever, Frederick & Peplau (2006), Psych. of Men & Masc."),
                   music=dict(bpm=100, root=0, prog="major", kick="four", audio="v5", gaps=[(E("study") + .05, S("avg") + .05)]),
                   cover=dict(words=["AVERAGE:", "13.1 CM.", "RELAX."], kicker="Bodies: all normal, part 2."))

def sc_study(img, d, t):
    t0, tm = S("study"), cue("study", "Measured by") - .1
    counter(d, X0, 320, t, t0 + .1, .8, 15521, "{:,.0f}", 210, INK); d.text((X0 + 6, 545), "men · 17 studies pooled", font=F(COND, 46), fill=INK)
    if t >= tm: box_label(d, X0 + 4, 620, "MEASURED", 40, WHITE, INK, font=BLK)
    tn = cue("study", "Not self-reported") - .1
    if t >= tn: box_label(d, X0 + 240, 620, "NOT SELF-REPORTED", 40, WHITE, INK, font=BLK)
    dot_field(d, (X0 + 14, 760, X1, 1110), t, cell=26, col=MID, hit={40})
    fig(d, "systematic review")

def sc_avg(img, d, t):
    t0, ti = S("avg"), cue("avg", "About five") - .1
    d.text((X0, 320), "AVERAGE", font=F(BLK, 150), fill=INK); d.text((X0 + 4, 480), "erect length", font=F(COND, 54), fill=MID)
    ruler(d, X0, X1, 760, 0, 20, 0, 13.12, (t - t0 - .2) / 1.0, unit="cm", ticks=20, label_every=5)
    if t >= t0 + 1.2: counter(d, X0, 820, t, t0 + 1.2, .4, 13.1, "{:.1f} CM", 150, SIG)
    if t >= ti: d.text((X0 + 6, 990), "≈ 5.2 inches", font=F(COND, 54), fill=INK)
    fig(d, "mean across studies")

def bars(d, t, both):
    d.text((X0, 320), "HAPPY WITH", font=F(BLK, 120), fill=INK); d.text((X0, 440), "THE SIZE", font=F(BLK, 120), fill=INK)
    rows = [("MEN, THEIR OWN", 55, MID, cue("worry", "only fifty") - .1)] + ([("WOMEN, THEIR PARTNER'S", 85, SIG, S("partners") + .1)] if both else [])
    for j, (lab, v, col, tk) in enumerate(rows):
        if t < tk: continue
        k = ease((t - tk) / .6); y = 620 + j * 250
        d.text((X0, y), lab, font=F(BLK, 48), fill=col); w = 620 * v / 85 * k
        d.rectangle([X0, y + 66, X0 + max(8, w), y + 190], fill=col)
        d.text((X0 + max(8, w) + 16, y + 128), f"{v * k:.0f} %", font=F(BLK, 72), fill=col, anchor="lm")

def sc_worry(img, d, t):
    bars(d, t, False); tf = cue("worry", "over fifty thousand") - .1
    if t >= tf: d.text((X0 + 4, 560), "survey · 52,031 people", font=F(MONO, 28), fill=MID)
    fig(d, "online survey, self-selected")
def sc_partners(img, d, t):
    bars(d, t, True); d.text((X0 + 4, 560), "survey · 52,031 people", font=F(MONO, 28), fill=MID)
    ts = cue("partners", "satisfied with") - .1
    if t >= ts: box_label(d, X1 - (1 - ease((t - ts) / .25)) * 50, 600, "SATISFIED", 44, WHITE, SIG, font=BLK, anchor="ra")
    fig(d, "online survey, self-selected")

def sc_point(img, d, t):
    t0, tb = S("point"), cue("point", "bigger than") - .2
    words_in(d, t, [("THE WORRY", t0 + .05, 320, 150, MID)] + ([("IS BIGGER", tb, 480, 150, SIG), ("THAN THE", tb + .12, 630, 150, SIG), ("PROBLEM.", tb + .24, 780, 150, SIG)] if t >= tb else []))
    fig(d, "fig. — Bodies: all normal")

EP.cuts = {"partners": "stay"}
EP.scenes = {"study": sc_study, "avg": sc_avg, "worry": sc_worry, "partners": sc_partners, "point": sc_point}
FX = [*EP.cut_fx(), (S("study") + .1, riser(.8, .04), 0), (cue("study", "Measured by") - .1, thud(.4), 0), (cue("study", "Not self-reported") - .1, pop(.13), .3),
      (S("avg") + .2, whoosh(.9, .04), 0), (S("avg") + 1.2, thud(.5), 0), (cue("avg", "About five") - .1, pop(.12), .2),
      (cue("worry", "over fifty thousand") - .1, tick(.06), 0), (cue("worry", "only fifty") - .1, thud(.45), -.2),
      (S("partners") + .1, thud(.55), 0), (cue("partners", "satisfied with") - .1, pop(.15), .3), (S("point") + .1, pop(.12), 0), (cue("point", "bigger than") - .2, thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
