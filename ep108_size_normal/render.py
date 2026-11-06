"""NOT JUST YOU – No. 108 (Bodies: all normal 2/2): average erect length 13.1 cm (Veale et al. 2015, up to 15,521 men);
55 % of men happy with their size, 85 % of women with their partner's (Lever et al. 2006). Since 06.11.2026 a 'what helps'
ending: measuring + real numbers relieved most of 92 worried men (Shamloul 2005, Urology). Look C+D · no anatomical drawings."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
HERE = os.path.dirname(os.path.abspath(__file__))
from bodies import *
TL = Timeline(HERE, lead=.15, gaps={"study": .6, "avg": .5, "worry": .5, "partners": .6, "feel": .5, "helps": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["study", "avg", "worry", "partners", "feel", "helps", "point", "end"]
EP = ThreadEpisode(TL, 108, "ALL NORMAL 2", order=ORDER, dark=True, label="REVIEW · 15,521 MEN",
                   chapters={k: "" for k in ORDER[:-1]}, sources=("Veale et al. (2015), BJU International 115(6) ·", "Lever et al. (2006) · Shamloul (2005), Urology 65(6)"),
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

def sc_feel(img, d, t):
    t0, tw = S("feel"), cue("feel", "the worry go away") - .15
    words_in(d, t, [("KNOWING THE", t0 + .05, 320, 120, MID), ("AVERAGE", t0 + .2, 440, 120, MID)] + ([("DOESN'T FIX", tw, 600, 130, INK), ("THE WORRY.", tw + .15, 740, 130, INK)] if t >= tw else []))
    fig(d, "fair enough")

def sc_helps(img, d, t):
    t0, tm, tr, tl = S("helps"), cue("helps", "worried about") - .1, cue("helps", "Getting measured") - .1, cue("helps", "relieved most") - .15
    counter(d, X0, 320, t, t0 + .1, .7, 92, "{:.0f}", 230, INK)
    d.text((X0 + 6, 565), "men at one clinic", font=F(COND, 46), fill=INK)
    if t >= tm: box_label(d, X0 + 4, 640, "WORRIED ABOUT THEIR SIZE", 40, WHITE, INK, font=BLK)
    if t >= tr:
        d.text((X0, 760), "1  MEASURED", font=F(BLK, 54), fill=INK)
        if t >= tr + .5: d.text((X0, 840), "2  THE REAL NUMBERS", font=F(BLK, 54), fill=INK)
    if t >= tl: box_label(d, X0 + 4 - (1 - ease((t - tl) / .2)) * 40, 950, "MOST: RELIEVED", 64, WHITE, SIG, font=BLK)
    fig(d, "one clinic · small study, no control group")

def sc_point(img, d, t):
    t0, td = S("point"), cue("point", "talk to a doctor") - .2
    words_in(d, t, [("STILL", t0 + .05, 320, 150, MID), ("BOTHERS YOU?", t0 + .2, 470, 130, MID)] + ([("TALK TO", td, 640, 150, SIG), ("A DOCTOR.", td + .15, 790, 150, SIG)] if t >= td else []))
    fig(d, "fig. — Bodies: all normal")

EP.cuts = {"partners": "stay"}
EP.scenes = {"study": sc_study, "avg": sc_avg, "worry": sc_worry, "partners": sc_partners, "feel": sc_feel, "helps": sc_helps, "point": sc_point}
EP.bg = {"helps": "light"}
FX = [*EP.cut_fx(), (S("study") + .1, riser(.8, .04), 0), (cue("study", "Measured by") - .1, thud(.4), 0), (cue("study", "Not self-reported") - .1, pop(.13), .3),
      (S("avg") + .2, whoosh(.9, .04), 0), (S("avg") + 1.2, thud(.5), 0), (cue("avg", "About five") - .1, pop(.12), .2),
      (cue("worry", "over fifty thousand") - .1, tick(.06), 0), (cue("worry", "only fifty") - .1, thud(.45), -.2),
      (S("partners") + .1, thud(.55), 0), (cue("partners", "satisfied with") - .1, pop(.15), .3), (S("feel") + .1, thud(.4), 0), (cue("feel", "the worry go away") - .15, pop(.13), 0),
      (S("helps") + .1, riser(.7, .04), 0), (cue("helps", "worried about") - .1, pop(.13), -.2), (cue("helps", "Getting measured") - .1, tick(.06), 0), (cue("helps", "Getting measured") + .4, tick(.06), 0), (cue("helps", "relieved most") - .15, thud(.5), 0),
      (S("point") + .1, pop(.12), 0), (cue("point", "talk to a doctor") - .2, thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
