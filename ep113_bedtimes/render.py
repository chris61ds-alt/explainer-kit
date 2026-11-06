"""NOT JUST YOU – No. 113: different bedtimes – mismatched couples reported more conflict, less serious talk, less shared time
and less sex (Larson, Crane & Smith 1991, 150 couples); happier wives went with more in-sync sleep (Gunn et al. 2015, Sleep).
Look C+D · statement opener with "you" · isometric bed: one lamp on, one off → both in bed · orange reveal: less sex."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"study": .6, "cost": .5, "sex": .6, "sync": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["study", "cost", "sex", "sync", "point", "end"]
EP = ThreadEpisode(TL, 113, "BEDTIMES", order=ORDER, dark=True, label="SURVEY · 150 COUPLES · CORRELATION",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Larson, Crane & Smith (1991), J. of Marital and Family", "Therapy 17(1) · Gunn et al. (2015), Sleep 38(6)"),
                   music=dict(bpm=88, root=-2, prog="dream", kick="half", audio="v5", gaps=[(E("study") + .05, S("cost") + .05)]),
                   cover=dict(words=["DIFFERENT", "BEDTIMES?", "IT COSTS."], kicker="More conflict. Less sex."))

I = Iso(520, 1050, .62)
def head(I, d, side, k, col=MID):
    """a sleeper's head on the pillow (simple disc), appears with k"""
    if k <= 0: return
    x, y, z = {"l": (-125, -190, 175), "r": (105, -190, 175)}[side]; px, py = I.P(x, y, z); r = 34 * back(clamp(k))
    d.ellipse([px - r, py - r, px + r, py + r], fill=col)

def sc_study(img, d, t):
    t0, tm = S("study"), cue("study", "mixed pairs") - .1
    counter(d, X0, 320, t, t0 + .1, .8, 150, "{:.0f}", 230, INK)
    d.text((X0 + 6, 565), "couples, compared", font=F(COND, 46), fill=INK)
    I.grid(img); I.shadow(d, 0, 0, 240)
    A = bed(I, d, t, T=[t0 + .05 + i * .06 for i in range(7)], lamp_col=SIG if False else TOP)
    head(I, d, "l", (t - t0 - .6) / .3, INK)                # the morning person is already asleep
    if t >= tm:                                             # the night owl's side stays empty, lamp on
        p = I.P(*A["lamp"]); r = 70 + 6 * math.sin(t * 6)
        d.ellipse([p[0] - r, p[1] - r - 20, p[0] + r, p[1] + r - 20], outline=MID, width=4)
        box_label(d, X1, 650, "MIXED PAIR", 40, WHITE, INK, font=BLK, anchor="ra")
        p2 = I.P(105, -190, 175); d.text((p2[0] + 70, p2[1] - 90), "01:00?", font=F(MONO, 30), fill=MID, anchor="mm")
    fig(d, "self-report · schematic")

def items(d, t, upto_sex):
    d.text((X0, 320), "MISMATCHED", font=F(BLK, 120), fill=INK); d.text((X0 + 4, 450), "couples reported", font=F(COND, 50), fill=MID)
    rows = [("MORE CONFLICT", S("cost") + .1), ("LESS SERIOUS TALK", cue("cost", "Less serious") - .1), ("LESS TIME TOGETHER", cue("cost", "Less time") - .1)]
    for j, (lab, tk) in enumerate(rows):
        if t >= tk: box_label(d, X0 + 4 - (1 - ease((t - tk) / .2)) * 40, 560 + j * 95, lab, 54, WHITE, INK, font=BLK)
    if upto_sex: words_in(d, t, [("LESS SEX.", S("sex") + .05, 880, 170, SIG)])

def sc_cost(img, d, t): items(d, t, False); fig(d, "a link, not proof")
def sc_sex(img, d, t): items(d, t, True); fig(d, "a link, not proof")

def sc_sync(img, d, t):
    t0, tw = S("sync"), cue("sync", "When wives") - .1
    d.text((X0, 320), "IN SYNC", font=F(BLK, 150), fill=INK); d.text((X0 + 4, 480), "asleep or awake at the same minute", font=F(COND, 44), fill=MID)
    y = 660; w = X1 - X0
    for row, (lab, ph) in enumerate((("YOU", 0.0), ("PARTNER", .5))):     # two hypnogram strips that line up more and more
        yy = y + row * 120; d.text((X0, yy), lab, font=F(MONO, 26), fill=MID)
        k = clamp((t - t0 - .2) / 1.2); sh = (1 - clamp((t - tw) / 1.0)) * ph if t >= tw else ph
        for i in range(int(40 * k)):
            on = math.sin(i * .5 + sh * 6) > -.2
            if on: d.rectangle([X0 + i * w / 40, yy + 36, X0 + (i + 1) * w / 40 - 4, yy + 86], fill=INK if row == 0 else MID)
    if t >= tw: box_label(d, X0 + 4 - (1 - ease((t - tw) / .2)) * 40, 950, "HAPPIER WIVES: MORE IN SYNC", 48, WHITE, INK, font=BLK)
    fig(d, "sleep sensors, 10 nights · a link, not proof")

def sc_point(img, d, t):
    t0, ti, to = S("point"), cue("point", "go to bed together") - .2, cue("point", "night owl") - .1
    words_in(d, t, [("SAME TYPE?", t0 + .05, 320, 130, MID), ("NOT NEEDED.", t0 + .2, 450, 130, MID)])
    I2 = Iso(540, 1080, .6); I2.grid(img); I2.shadow(d, 0, 0, 240)
    A = bed(I2, d, t, T=[t0 - 1] * 7)
    head(I2, d, "l", 1, INK); head(I2, d, "r", (t - ti) / .3, INK)
    if t >= ti: words_in(d, t, [("GO TO BED", ti, 590, 110, SIG), ("TOGETHER.", ti + .12, 700, 110, SIG)])
    if t >= to: p = I2.P(105, -190, 175); callout(d, p, "r", p[1] - 60, 1, "GET UP AGAIN", INK, k=(t - to) / .4)
    fig(d, "an idea, not a study result")

EP.cuts = {"sex": "stay"}
EP.bg = {"study": "light", "point": "light"}
EP.scenes = {"study": sc_study, "cost": sc_cost, "sex": sc_sex, "sync": sc_sync, "point": sc_point}
FX = [*EP.cut_fx(), (S("study") + .1, riser(.8, .04), 0), *[(S("study") + .05 + i * .06, tick(.03), (i - 3) / 4) for i in range(7)], (cue("study", "mixed pairs") - .1, pop(.13), .3),
      (S("cost") + .1, thud(.45), 0), (cue("cost", "Less serious") - .1, pop(.13), -.2), (cue("cost", "Less time") - .1, pop(.13), .2),
      (S("sex") + .05, thud(.55), 0),
      (S("sync") + .2, riser(1.2, .03), 0), (cue("sync", "When wives") - .1, pop(.14), 0),
      (S("point") + .1, pop(.12), 0), (cue("point", "go to bed together") - .2, thud(.45), 0), (cue("point", "night owl") - .1, pop(.13), .3), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
