"""NOT JUST YOU – No. 90: most couples now meet online (Rosenfeld, Thomas & Hausen 2019, PNAS). Look C+D, dark."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from dating import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .6, "friends": .5, "online": .5, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "friends", "online", "point", "end"]
EP = ThreadEpisode(TL, 90, "MET ONLINE", order=ORDER, dark=True, label="SURVEY · STRAIGHT US COUPLES",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Rosenfeld, Thomas & Hausen (2019), PNAS", "116(36) · HCMST 2009 + 2017"),
                   music=dict(bpm=104, root=2, prog="major", kick="four", audio="v5", gaps=[(E("study") + .05, S("friends") + .05)]),
                   cover=dict(words=["HOW COUPLES", "MEET: ONLINE."], kicker="39 %. Friends: 20 %."))

FIELD = (X0 + 14, 760, X1, 1110)
def dot_xy(i, box=FIELD, cell=30):
    x0, y0, x1, y1 = box; cols = len(range(int(x0), int(x1), cell)); r, c = divmod(i, cols)
    return x0 + c * cell, y0 + r * cell

def sc_hook(img, d, t):
    tn = cue("hook", "not how") - .2
    d.text((X0 - 4, 320), "MET THROUGH", font=F(BLK, 120), fill=INK)
    d.text((X0 - 4, 440), "FRIENDS?", font=F(BLK, 170), fill=INK)
    if t >= tn:
        k = ease((t - tn) / .3); w = d.textlength("FRIENDS?", font=F(BLK, 170))
        d.line([X0 - 10, 540, X0 - 10 + (w + 20) * k, 540], fill=SIG, width=16)
    silhouette(img, lambda m: (front_bust(m, 380, 880, .4, 255), front_bust(m, 600, 880, .4, 255)), (170, 770, 810, 1125), INK, cell=9)
    fig(d, "fig. 1 — how did you two meet?")

def sc_study(img, d, t):
    t0 = S("study")
    counter(d, X0, 320, t, t0 + .1, .8, 5421, "{:,.0f}", 230, INK)
    d.text((X0 + 6, 570), "straight couples · Stanford · US surveys 2009 + 2017", font=F(COND, 38), fill=INK)
    d.text((X0 + 6, 622), "one question: how did you meet?", font=F(COND, 32), fill=MID)
    dot_field(d, FIELD, t, cell=30, col=MID, hit={40, 41})
    fig(d, "How Couples Meet and Stay Together survey")

def morph_bar(d, t, y, lab, v0, v1, t0, dur, col0, col1, vmax=40):
    k = ease_io((t - t0) / dur) if t >= t0 else 0; v = lerp(v0, v1, k); col = mix(col0, col1, k)
    d.text((X0, y), lab, font=F(BLK, 54), fill=col)
    w = 640 * v / vmax; d.rectangle([X0, y + 75, X0 + max(8, w), y + 215], fill=col)
    d.text((X0 + max(8, w) + 16, y + 145), f"{v:.0f} %", font=F(BLK, 72), fill=col, anchor="lm")

def head(d, t):
    d.text((X0, 320), "HOW THEY MET", font=F(BLK, 120), fill=INK)
    yr = "2017" if t >= cue("friends", "By twenty") - .1 else "1995"
    d.text((X0 + 4, 455), yr, font=F(BLK, 80), fill=MID)

def sc_friends(img, d, t):
    head(d, t)
    morph_bar(d, t, 600, "THROUGH FRIENDS", 33, 20, cue("friends", "By twenty") - .1, .7, INK, MID)
    fig(d, "share of straight couples")

def sc_online(img, d, t):
    head(d, t)
    morph_bar(d, t, 600, "THROUGH FRIENDS", 20, 20, 0, 1, MID, MID)
    t2 = S("online") + .1
    if t >= t2: morph_bar(d, t, 870, "ONLINE", 2, 39, t2 + .3, .9, SIG, SIG)
    tn = cue("online", "Now the most") - .1
    if t >= tn: box_label(d, X1, 460, "NO. 1", 60, WHITE, SIG, font=BLK, anchor="ra")
    fig(d, "share of straight couples · online: 2 % in 1995")

def sc_point(img, d, t):
    t0, tn = S("point"), cue("point", "You're the normal") - .2
    words_in(d, t, [("NOT THE", t0 + .3, 320, 140, MID), ("WEIRD STORY.", t0 + .5, 460, 120, INK)] +
             ([("THE NORMAL", tn, 640, 120, SIG), ("ONE.", tn + .15, 760, 150, SIG)] if t >= tn else []))
    d.rounded_rectangle([X0, 930, X0 + 420, 1105], radius=26, outline=MID, width=5)
    bubbles(d, X0 + 22, X0 + 398, 950, 3, clamp((t - t0 - .4) / 1.2), col=MID, alt=INK, h=38, gap=14)
    fig(d, "fig. 2 — 39 % of straight couples, 2017")

# magic move: the couple from the hook becomes two dots in the survey · the friends bar stays, online grows below it
_dx, _dy = dot_xy(40)
EP.carry = {"study": [((170, 770, 810, 1125), (_dx - 7, _dy - 7, _dx + 37, _dy + 7))]}
EP.cuts = {"online": "stay"}

EP.scenes = {"hook": sc_hook, "study": sc_study, "friends": sc_friends, "online": sc_online, "point": sc_point}
FX = [(0.0, thud(.5), 0), (cue("hook", "not how") - .2, pop(.15), .3), *EP.cut_fx(), (S("study") + .1, riser(.8, .04), 0),
      (S("friends") + .1, pop(.12), 0), (cue("friends", "By twenty") - .1, thud(.45), 0), (S("online") + .4, thud(.5), 0),
      (cue("online", "Now the most") - .1, pop(.15), .3), (cue("point", "You're the normal") - .2, thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
