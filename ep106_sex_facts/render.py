"""NOT JUST YOU – No. 106 (tips): 3 sex facts worth saving – once a week is enough (Muise et al. 2016), affection after sex
(Muise et al. 2014), the afterglow lasts ~48 h (Meltzer et al. 2017). Look C+D · claim opener · recap: isometric bed, light."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"tip1": .5, "tip2": .5, "tip3": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["tip1", "tip2", "tip3", "point", "end"]
EP = ThreadEpisode(TL, 106, "SEX FACTS", order=ORDER, dark=True, label=None,
                   chapters={k: "" for k in ORDER[:-1]}, sources=("Muise et al. (2016) SPPS · Muise, Giang & Impett (2014)", "Arch. Sex. Behav. · Meltzer et al. (2017) Psych. Sci."),
                   music=dict(bpm=96, root=-2, prog="dream", kick="four", audio="v5"),
                   cover=dict(words=["3 SEX FACTS", "WORTH", "SAVING."], kicker="Backed by research."))
I = Iso(470, 990, .66)

def sc_tip1(img, d, t):
    t0 = S("tip1"); tip_head(d, t, 1, ["ONCE A WEEK", "IS ENOUGH."], t0, size=105)
    td, tm = cue("tip1", "well-being rose") - .1, cue("tip1", "More didn't") - .1
    if t >= td:                                            # well-being vs. frequency: rises, then flat (schematic)
        x0, x1, yb = X0 + 20, X1 - 20, 1040; d.line([x0, yb, x1, yb], fill=MID, width=3)
        for lab, u in (("NEVER", 0), ("1× / WEEK", .5), ("4+", 1)): d.text((lerp(x0, x1, u), yb + 14), lab, font=F(MONO, 26), fill=MID, anchor="ma")
        k = ease_io(clamp((t - td) / 1.2)); pts = [(lerp(x0, x1, u), yb - 40 - 260 * min(u, .5) * 2) for u in [i / 40 * k for i in range(41)]]
        d.line(pts, fill=INK, width=9, joint="curve")
        if t >= tm: px = lerp(x0, x1, .5); box_label(d, px + 20, yb - 380, "MORE: NO GAIN", 36, WHITE, INK, font=BLK)
    d.text((X0, 620), "30,000+ people", font=F(COND, 46), fill=MID) if t >= td else None
    fig(d, "well-being · line schematic")

def sc_tip2(img, d, t):
    t0, tm = S("tip2"), cue("tip2", "felt more satisfied") - .1; tip_head(d, t, 2, ["DON'T SKIP", "THE CUDDLE."], t0, size=105)
    couple(img, d, you=(380, 950), partner=(580, 950))
    if t >= t0 + .8: heart(d, 480, 760, 30 + 4 * math.sin(t * 8), INK)
    if t >= tm: box_label(d, X1, 640, "MORE SATISFIED", 44, WHITE, SIG, font=BLK, anchor="ra")
    fig(d, "a link, not proof")

def sc_tip3(img, d, t):
    t0 = S("tip3"); box_label(d, X0, 300, "FACT 3", 40, WHITE, INK, font=BLK)
    words_in(d, t, [("THE AFTERGLOW", t0 + .05, 370, 100, INK)])
    counter(d, X0, 500, t, t0 + .1, .8, 48, "≈ {:.0f} H", 240, SIG)
    for i in range(2): clock(d, X0 + 120 + i * 300, 960, 90, (t - t0 - .3 - i * .3) / .5, col=SIG, label=f"DAY {i + 1}")
    fig(d, "sexual satisfaction stays higher")

sc_point = iso_recap(TL, "point", I, bed, "SO:", [("pillow_l", "l", -80, "ONCE A WEEK", INK, "once a week"), ("blanket", "l", 60, "CUDDLE AFTER", INK, "Cuddle after"),
                                               ("lamp", "r", -40, "ENJOY THE GLOW", SIG, "Enjoy the glow")])

EP.cuts = {"tip3": "stay"}
EP.bg = {"point": "light"}
EP.scenes = {"tip1": sc_tip1, "tip2": sc_tip2, "tip3": sc_tip3, "point": sc_point}
FX = [(0.0, thud(.5), 0), *EP.cut_fx(), (S("tip1") + .1, pop(.12), -.3), (cue("tip1", "well-being rose") - .1, riser(1.0, .04), 0), (cue("tip1", "More didn't") - .1, thud(.45), .2),
      (S("tip2") + .1, pop(.12), -.3), (S("tip2") + .8, pop(.14), 0), (cue("tip2", "felt more satisfied") - .1, thud(.45), .3),
      (S("tip3") + .1, thud(.55), 0), (S("tip3") + .3, tick(.06), -.3), (S("tip3") + .6, tick(.06), .3),
      (cue("point", "once a week") - .15, pop(.12), -.3), (cue("point", "Cuddle after") - .15, pop(.12), -.3), (cue("point", "Enjoy the glow") - .15, thud(.45), .3), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
