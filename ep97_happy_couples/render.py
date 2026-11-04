"""NOT JUST YOU – No. 97 (tips): 3 things happy couples do – new things together (Aron et al. 2000), celebrate good news
(Gable et al. 2004), say thank you (Algoe et al. 2010). Look C+D · statement opener · recap: isometric sofa on light paper."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"tip1": .5, "tip2": .5, "tip3": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["tip1", "tip2", "tip3", "point", "end"]                     # opener: statement ("claim", toolkit)
EP = ThreadEpisode(TL, 97, "HAPPY COUPLES", order=ORDER, dark=True, label=None,
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Aron et al. (2000) JPSP · Gable et al. (2004)", "JPSP · Algoe, Gable & Maisel (2010) Pers. Rel."),
                   music=dict(bpm=100, root=2, prog="major", kick="four", audio="v5"),
                   cover=dict(words=["HAPPY COUPLES", "DO THESE", "3 THINGS."], kicker="Send this to your partner."))
I = Iso(470, 990, .7)

def sc_tip1(img, d, t):
    t0 = S("tip1"); tip_head(d, t, 1, ["DO SOMETHING", "NEW TOGETHER."], t0)
    te, tn, tf, tb = cue("tip1", "In an experiment") - .1, cue("tip1", "new, exciting") - .1, cue("tip1", "felt better") - .1, cue("tip1", "something boring") - .1
    couple(img, d, s=.26, you=(230, 1000), partner=(400, 1000), labels=None)
    if t >= te: box_label(d, X0, 620, "EXPERIMENT", 34, WHITE, INK, font=BLK)
    if t >= tn:                                            # the exciting task: a zig-zag mountain path
        k = ease((t - tn) / .6); pts = [(560 + i * 60, 1000 - (60 if i % 2 else 0) - i * 30) for i in range(6)]
        d.line(pts[: max(2, int(1 + k * 5))], fill=INK, width=8, joint="curve"); d.text((560, 1040), "NEW + EXCITING", font=F(BLK, 28), fill=INK)
    if t >= tf:                                            # relationship quality: up for the new task (schematic)
        k = ease((t - tf) / .5); d.text((X1 - 60, 640), "FELT BETTER", font=F(BLK, 44), fill=SIG, anchor="ra")
        d.polygon([(X1 - 25, 690 - 40 * k), (X1 - 50, 726 - 40 * k), (X1, 726 - 40 * k)], fill=SIG)
    if t >= tb: d.text((560, 1080), "vs. a boring task", font=F(COND, 34), fill=MID)
    fig(d, "experiment · schematic")

def sc_tip2(img, d, t):
    t0 = S("tip2"); tip_head(d, t, 2, ["CELEBRATE THEIR", "GOOD NEWS."], t0, size=90)
    couple(img, d)
    tg, tr, tc = t0 + .6, cue("tip2", "react with") - .1, cue("tip2", "feel closer") - .1
    if t < tr: bubble(d, "partner", "I got the job!", (t - tg) / .3, col=MID, y=640)
    else:
        b = bubble(d, "you", "Cool.", 1, col=MID, y=600); strike(d, b, (t - tr) / .2)
        bubble(d, "you", "That's amazing! Tell me everything!", (t - tr - .3) / .3, y=690, size=30)
    if t >= tc:
        k = ease((t - tc) / .5); y = 1000
        d.line([YOU[0] + 110, y, lerp(YOU[0] + 110, PARTNER[0] - 110, k), y], fill=SIG, width=10)
        if k >= 1: heart(d, (YOU[0] + PARTNER[0]) / 2, y - 6, 26 + 4 * math.sin(t * 8), SIG)
    fig(d, "a link, not proof")

def sc_tip3(img, d, t):
    t0 = S("tip3"); box_label(d, X0, 300, "TIP 3", 40, WHITE, INK, font=BLK)
    words_in(d, t, [("SAY", t0 + .05, 370, 170, INK), ("THANK YOU.", t0 + .2, 540, 150, INK)])
    couple(img, d)
    bubble(d, "you", "Thank you!", (t - cue("tip3", "In a diary") + .1) / .3, y=760)
    tn = cue("tip3", "the next day") - .1
    if t >= tn:
        box_label(d, X1 - (1 - ease((t - tn) / .25)) * 50, 760, "NEXT DAY: CLOSER", 40, WHITE, SIG, font=BLK, anchor="ra")
        heart(d, (YOU[0] + PARTNER[0]) / 2, 990, 24 + 3 * math.sin(t * 8), SIG)
    fig(d, "diary study · a link, not proof")

sc_point = iso_recap(TL, "point", I, sofa, "SO:", [("back", "l", -40, "NEW THINGS", INK, "try new"), ("left", "l", 70, "CHEER LOUDER", INK, "Cheer louder"),
                                                 ("mug", "r", -60, "SAY THANKS", SIG, "Say thanks")])

EP.cuts = {"tip3": "stay"}
EP.bg = {"point": "light"}
EP.scenes = {"tip1": sc_tip1, "tip2": sc_tip2, "tip3": sc_tip3, "point": sc_point}
FX = [(0.0, thud(.5), 0), *EP.cut_fx(), (S("tip1") + .1, pop(.12), -.3), (cue("tip1", "In an experiment") - .1, pop(.13), -.2),
      (cue("tip1", "new, exciting") - .1, whoosh(.5, .04), .2), (cue("tip1", "felt better") - .1, thud(.45), .3), (cue("tip1", "something boring") - .1, tick(.06), 0),
      (S("tip2") + .1, pop(.12), -.3), (S("tip2") + .6, pop(.13), .3), (cue("tip2", "react with") - .1, whoosh(.2, .05), 0), (cue("tip2", "react with") + .2, pop(.14), -.2),
      (cue("tip2", "feel closer") - .1, riser(.5, .04), 0),
      (S("tip3") + .1, thud(.4), 0), (cue("tip3", "In a diary") - .1, pop(.14), -.2), (cue("tip3", "the next day") - .1, thud(.45), .3),
      (cue("point", "try new") - .15, pop(.12), -.3), (cue("point", "Cheer louder") - .15, pop(.12), -.3), (cue("point", "Say thanks") - .15, thud(.45), .3), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
