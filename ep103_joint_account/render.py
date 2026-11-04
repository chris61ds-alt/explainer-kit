"""NOT JUST YOU – No. 103: joint bank account – randomized 2-year experiment, 230 couples: separate accounts declined in
relationship quality, joint accounts didn't (Olson, Rick, Small & Finkel 2023). Look C+D · claim opener."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"study": .6, "separate": .5, "joint": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["study", "separate", "joint", "point", "end"]
EP = ThreadEpisode(TL, 103, "JOINT ACCOUNT", order=ORDER, dark=True, label="RANDOMIZED EXPERIMENT · 230 COUPLES",
                   chapters={k: "" for k in ORDER[:-1]}, sources=("Olson, Rick, Small & Finkel (2023), Common Cents,", "Journal of Consumer Research 50(4)"),
                   music=dict(bpm=98, root=0, prog="major", kick="four", audio="v5", gaps=[(E("study") + .05, S("separate") + .05)]),
                   cover=dict(words=["ONE BANK", "ACCOUNT,", "HAPPIER COUPLE."], kicker="A 2-year experiment."))
GROUPS = [("MERGE", "merge"), ("STAY SEPARATE", "stay separate"), ("YOUR CHOICE", "do whatever")]

def sc_study(img, d, t):
    t0 = S("study")
    counter(d, X0, 320, t, t0 + .1, .8, 230, "{:.0f}", 230, INK); d.text((X0 + 6, 565), "engaged or newly married couples", font=F(COND, 44), fill=INK)
    tr = cue("study", "randomly") - .1
    if t >= tr: box_label(d, X0 + 4, 640, "RANDOMLY ASSIGNED", 40, WHITE, INK, font=BLK)
    for i, (lab, c) in enumerate(GROUPS):
        tc = cue("study", c) - .1
        if t < tc: continue
        k = back(clamp((t - tc) / .3)); x = X0 + 20 + i * 290; y = 760
        d.rounded_rectangle([x, y, x + 250 * k, y + 250 * k], radius=24, outline=INK, width=5)
        if k > .8:
            for j in range(4): cx_, cy_ = x + 70 + (j % 2) * 110, y + 80 + (j // 2) * 90; d.ellipse([cx_ - 26, cy_ - 26, cx_ + 26, cy_ + 26], fill=MID if i else INK)
            d.text((x + 125, y + 270), lab, font=F(BLK, 30), fill=INK, anchor="ma")
    fig(d, "each circle: a group of couples · schematic")

def chart(d, t, joint):
    d.text((X0, 320), "RELATIONSHIP", font=F(BLK, 110), fill=INK); d.text((X0, 435), "QUALITY", font=F(BLK, 110), fill=INK)
    x0, x1, y0 = X0 + 20, X1 - 20, 640; d.line([x0, 1060, x1, 1060], fill=MID, width=3)
    d.text((x0, 1072), "START", font=F(MONO, 26), fill=MID); d.text((x1, 1072), "2 YEARS", font=F(MONO, 26), fill=MID, anchor="ra")
    def line(k, drop_, col, lab, w=8):
        pts = [(lerp(x0, x1, u), y0 + 60 + drop_ * u * u) for u in [i / 30 * k for i in range(31)]]
        d.line(pts, fill=col, width=w, joint="curve"); d.text((pts[-1][0] + 8, pts[-1][1]), lab, font=F(BLK, 30), fill=col, anchor="ra" if k >= 1 else "lm")
    ts = S("separate") + .2
    if t >= ts: k = ease_io((t - ts) / 1.2); line(k, 300, MID, "SEPARATE"); line(k, 270, MID, "") if k else None
    if joint:
        tj = S("joint") + .1
        if t >= tj: line(ease_io((t - tj) / .8), 0, SIG, "JOINT", 12)

def sc_separate(img, d, t): chart(d, t, False); fig(d, "lines schematic")
def sc_joint(img, d, t):
    chart(d, t, True); tm = cue("joint", "more in sync") - .1
    if t >= tm: box_label(d, X0, 560, "MORE IN SYNC ABOUT MONEY", 38, WHITE, SIG, font=BLK)
    fig(d, "lines schematic")

def sc_point(img, d, t):
    t0, tm = S("point"), cue("point", "Maybe money") - .2
    words_in(d, t, [("LOVE IS", t0 + .05, 320, 150, MID), ("SHARED.", t0 + .2, 470, 150, MID)] + ([("MONEY", tm, 650, 170, SIG), ("TOO?", tm + .15, 820, 170, SIG)] if t >= tm else []))
    fig(d, "fig. 2 — not for every couple")

EP.cuts = {"joint": "stay"}
EP.scenes = {"study": sc_study, "separate": sc_separate, "joint": sc_joint, "point": sc_point}
FX = [(0.0, thud(.5), 0), *EP.cut_fx(), (S("study") + .1, riser(.8, .04), 0), (cue("study", "randomly") - .1, thud(.4), 0),
      *[(cue("study", c) - .1, pop(.13), (i - 1) / 2) for i, (l, c) in enumerate(GROUPS)],
      (S("separate") + .2, whoosh(.8, .04), 0), (S("separate") + 1.4, tick(.06), 0), (S("joint") + .1, thud(.55), 0), (cue("joint", "more in sync") - .1, pop(.15), .3),
      (S("point") + .1, pop(.12), 0), (cue("point", "Maybe money") - .2, thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
