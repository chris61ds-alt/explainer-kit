"""NOT JUST YOU – No. 98 (tips): how to fight without breaking up – start soft (Carrère & Gottman 1999), 5:1 (Gottman),
take a 20-minute break (Gottman). Look C+D · quick-question opener · hook + recap: isometric kitchen table with a timer."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "tip1": .5, "tip2": .5, "tip3": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "tip1", "tip2", "tip3", "point", "end"]
EP = ThreadEpisode(TL, 98, "FIGHT FAIR", order=ORDER, dark=True, label=None,
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Carrère & Gottman (1999) Family Process ·", "Gottman & Levenson · Gottman Institute"),
                   music=dict(bpm=92, root=-3, prog="tense", kick="half", audio="v5"),
                   cover=dict(words=["HOW TO FIGHT", "WITHOUT", "BREAKING UP."], kicker="Save this for your next fight."))
I = Iso(480, 1000, .72)

sc_hook = iso_hook(TL, "hook", I, kitchen_table, ["3 TIPS."], "from decades of couples research", sub_cue="decades", save="Save this",
                   figtxt="fig. 1 — the kitchen table, schematic")

def sc_tip1(img, d, t):
    t0 = S("tip1"); tip_head(d, t, 1, ["START SOFT."], t0, size=130)
    couple(img, d)
    th, tf, tdv = t0 + .3, cue("tip1", "first three minutes") - .1, cue("tip1", "divorced years later") - .1
    b = bubble(d, "you", "You NEVER listen!", (t - th) / .3, col=MID, y=600)
    if t >= th + .6: strike(d, b, (t - th - .6) / .2)
    bubble(d, "you", "Hey, can we talk?", (t - th - .9) / .3, y=690)
    if t >= tf: clock(d, PARTNER[0], 690, 62, (t - tf) / 1.2, label="3 MIN")
    if t >= tdv: box_label(d, X1, 560, "PREDICTED DIVORCE", 40, WHITE, INK, font=BLK, anchor="ra")
    fig(d, "a link, not proof")

def sc_tip2(img, d, t):
    t0 = S("tip2"); tip_head(d, t, 2, ["KEEP IT", "5 : 1."], t0, size=130)
    ts = cue("tip2", "Stable couples") - .1; tw = cue("tip2", "Even while") - .1
    if t >= ts:                                            # five positives for one negative
        for i in range(6):
            ti = ts + .2 + i * .18
            if t < ti: continue
            k = back(clamp((t - ti) / .25)); x = X0 + 40 + i * 140; y = 800; r = 50 * k
            pos = i < 5; d.ellipse([x - r, y - r, x + r, y + r], fill=INK if pos else MID)
            if k > .6: d.text((x, y), "+" if pos else "–", font=F(BLK, 70), fill=BG, anchor="mm")
    if t >= tw: box_label(d, X0, 900, "EVEN WHILE FIGHTING", 44, WHITE, INK, font=BLK)
    fig(d, "positive vs. negative moments · schematic")

def sc_tip3(img, d, t):
    t0 = S("tip3"); box_label(d, X0, 300, "TIP 3", 40, WHITE, INK, font=BLK)
    words_in(d, t, [("TAKE A", t0 + .05, 370, 160, INK), ("BREAK.", t0 + .2, 530, 170, INK)])
    tr, tm = cue("tip3", "heart races") - .1, cue("tip3", "twenty minutes") - .15
    if t >= tr and t < tm + .3:                            # heart rate racing (schematic)
        pts = ekg(X0, X1, 860, t, period=110, amp=70, speed=420, chaos=.25)
        d.line(pts, fill=INK, width=6)
    if t >= tm: clock(d, 480, 860, 110, (t - tm) / 1.5, col=SIG, label="20 MIN")
    fig(d, "heart rate · schematic")

sc_point = iso_recap(TL, "point", I, kitchen_table, "SO:", [("you", "l", -60, "START SOFT", INK, "start soft"),
                     ("note", "l", 90, "STAY KIND", INK, "Stay kind"), ("timer", "r", -40, "PAUSE", SIG, "pause")])

EP.cuts = {"tip2": "stay", "tip3": "stay"}
EP.bg = {"hook": "light", "point": "light"}
EP.scenes = {"hook": sc_hook, "tip1": sc_tip1, "tip2": sc_tip2, "tip3": sc_tip3, "point": sc_point}
FX = [*EP.cut_fx(), (S("hook") + .05, thud(.45), 0), *iso_fx(TL, "hook"), (cue("hook", "Save this") - .1, pop(.15), .3),
      (S("tip1") + .3, pop(.13), -.2), (S("tip1") + .9, whoosh(.2, .05), 0), (S("tip1") + 1.2, pop(.13), -.2),
      (cue("tip1", "first three minutes") - .1, tick(.06), .3), (cue("tip1", "divorced years later") - .1, thud(.5), .3),
      (S("tip2") + .1, thud(.4), 0), *[(cue("tip2", "Stable couples") + .1 + i * .18, pop(.1), (i - 2.5) / 3) for i in range(6)],
      (cue("tip2", "Even while") - .1, thud(.45), 0),
      (S("tip3") + .1, thud(.4), 0), (cue("tip3", "heart races") - .1, riser(.8, .05), 0), (cue("tip3", "twenty minutes") - .15, thud(.5), 0),
      (cue("point", "start soft") - .15, pop(.12), -.3), (cue("point", "Stay kind") - .15, pop(.12), -.3), (cue("point", "pause") - .15, thud(.45), .3), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
