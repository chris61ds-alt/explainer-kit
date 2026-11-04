"""NOT JUST YOU – No. 99: bids for attention – still-married couples turned toward each other 86 % of the time,
divorced couples 33 % (Gottman, newlywed study, 6-year follow-up). Look C+D · guess opener · orange reveal."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .6, "married": .5, "divorced": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "married", "divorced", "point", "end"]
EP = ThreadEpisode(TL, 99, "BIDS", order=ORDER, dark=True, label="OBSERVATION · NEWLYWEDS",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Gottman – newlywed study, 6-year follow-up", "Gottman Institute · The Relationship Cure (2001)"),
                   music=dict(bpm=100, root=0, prog="dream", kick="four", audio="v5", gaps=[(E("study") + .05, S("married") + .05)]),
                   cover=dict(words=["HAPPY COUPLES", "RESPOND", "86 % OF THE TIME."], kicker="Divorced couples: 33 %."))

def bird(d, x, y, s=1.0, col=INK):
    d.arc([x - 40 * s, y - 20 * s, x, y + 20 * s], 200, 340, fill=col, width=int(7 * s)); d.arc([x, y - 20 * s, x + 40 * s, y + 20 * s], 200, 340, fill=col, width=int(7 * s))

def sc_hook(img, d, t):
    t0, tl = S("hook"), cue("hook", "look at this bird") - .1
    words_in(d, t, [("TINY", t0 + .05, 320, 170, INK), ("MOMENTS.", t0 + .2, 490, 150, INK)])
    couple(img, d, labels=("YOU", "PARTNER"))
    if t >= tl:
        bubble(d, "partner", "Look, a bird!", (t - tl) / .3, col=MID, y=700)
        bx = 820 + 30 * math.sin(t * 2); by = 640 - 20 * math.sin(t * 3); bird(d, bx, by, 1.2)
    fig(d, "fig. 1 — a bid for attention, schematic")

FIELD = (X0 + 14, 760, X1, 1110)
def sc_study(img, d, t):
    t0, tb = S("study"), cue("study", "little bids") - .1
    counter(d, X0, 320, t, t0 + .1, .8, 6, "{:.0f} YEARS", 200, INK)
    d.text((X0 + 6, 545), "newlyweds, watched and followed up", font=F(COND, 42), fill=INK)
    if t >= tb: box_label(d, X0 + 4 - (1 - ease((t - tb) / .2)) * 40, 610, "HOW THEY ANSWER LITTLE BIDS", 38, WHITE, INK, font=BLK)
    dot_field(d, FIELD, t, cell=30, col=MID, hit={40, 41} | ({70, 71, 130, 131, 190, 191} if t >= tb else set()), hitcol=INK)
    fig(d, "every pair of dots: one couple · schematic")

def bars(d, t, show_div):
    d.text((X0, 320), "TURNED TOWARD", font=F(BLK, 110), fill=INK); d.text((X0 + 4, 440), "their partner's bids", font=F(COND, 50), fill=MID)
    rows = [("STILL MARRIED", 86, INK, S("married") + .3)] + ([("DIVORCED", 33, SIG, S("divorced") + .1)] if show_div else [])
    for j, (lab, v, col, tk) in enumerate(rows):
        if t < tk: continue
        k = ease((t - tk) / .6); y = 600 + j * 260
        d.text((X0, y), lab, font=F(BLK, 54), fill=col); w = 600 * v / 86 * k
        d.rectangle([X0, y + 75, X0 + max(8, w), y + 205], fill=col)
        d.text((X0 + max(8, w) + 16, y + 140), f"{v * k:.0f} %", font=F(BLK, 72), fill=col, anchor="lm")

def sc_married(img, d, t): bars(d, t, False); fig(d, "share of bids answered by turning toward")
def sc_divorced(img, d, t): bars(d, t, True); fig(d, "share of bids answered by turning toward")

IP = Iso(480, 1010, .9)
def sc_point(img, d, t):
    t0, tl = S("point"), cue("point", "Look!") - .15
    IP.grid(img); IP.shadow(d, 0, 0, 210)
    A = phone(IP, d, t, msgs=[("l", t0 + .1, MID), ("r", tl, SIG)])
    words_in(d, t, [("WHEN THEY", t0 + .05, 320, 110, MID), ("SAY: LOOK!", t0 + .2, 430, 110, INK)] + ([("LOOK.", tl, 545, 150, SIG)] if t >= tl else []))
    if t >= tl: p = IP.P(*A["bubble"]); callout(d, p, "r", p[1] - 60, 1, "TURN TOWARD", SIG, k=(t - tl) / .4)
    fig(d, "fig. 2 — turn toward")

EP.carry = {"study": [((100, 820, 860, 1135), (X0 + 14 + 10 * 30 - 8, 760 + 30 - 8, X0 + 14 + 11 * 30 + 8, 760 + 30 + 8))]}
EP.cuts = {"divorced": "stay"}
EP.bg = {"point": "light"}
EP.scenes = {"hook": sc_hook, "study": sc_study, "married": sc_married, "divorced": sc_divorced, "point": sc_point}
FX = [*EP.cut_fx(), (S("hook") + .05, thud(.45), 0), (S("hook") + .2, pop(.12), .2), (cue("hook", "look at this bird") - .1, pop(.15), .3),
      (S("study") + .1, riser(.8, .04), 0), (cue("study", "little bids") - .1, pop(.13), 0),
      (S("married") + .3, thud(.5), 0), (S("divorced") + .1, thud(.55), 0),
      (S("point") + .1, pop(.12), 0), (cue("point", "Look!") - .15, thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
