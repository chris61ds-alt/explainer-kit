"""NOT JUST YOU – No. 78: women rate 80 % of men below average (OkTrends 2009). Look C+D, dark."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from dating import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .6, "study": .5, "women": .6, "men": .6, "twist": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "women", "men", "twist", "point", "end"]
EP = ThreadEpisode(TL, 78, "BELOW AVERAGE", order=ORDER, dark=True, label="PLATFORM DATA · OKCUPID",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("OkTrends (2009), Your Looks and", "Your Inbox · OkCupid"),
                   music=dict(bpm=98, root=-1, prog="tense", kick="four", gaps=[(E("study") + .05, S("women") + .05)]),
                   cover=dict(words=["80 % OF MEN:", "UGLY?"], kicker="According to women."))
LAB = ["1", "2", "3", "4", "5"]

def sc_hook(img, d, t):
    d.text((X0 - 6, 300), "80 %", font=F(BLK, 300), fill=SIG)
    d.text((X0 + 6, 610), "of men: below average?", font=F(BLK, 58), fill=INK)
    for i in range(10):
        x = X0 + 40 + i * 86
        silhouette(img, lambda m, x=x: front_bust(m, x, 830, .15, 255), (x - 44, 780, x + 44, 920), INK if i >= 8 else MID, cell=5)
    bbox(d, (X0 - 10, 770, X0 + 700, 930), "BELOW MEDIUM", SIG, (t - .8) / .3, coords=False)
    fig(d, "fig. 1 — according to women")

def sc_study(img, d, t):
    t0 = S("study")
    d.text((X0, 320), "RATE THEIR", font=F(BLK, 120), fill=INK); d.text((X0, 450), "LOOKS:", font=F(BLK, 120), fill=SIG)
    for i in range(5):
        k = ease((t - t0 - .3 - i * .12) / .3); x = X0 + i * 170
        d.rectangle([x, 650, x + 140, 790], outline=INK, width=5, fill=SIG if (i == 2 and k > .9) else None)
        d.text((x + 70, 720), str(i + 1), font=F(BLK, 70), fill=WHITE if (i == 2 and k > .9) else INK, anchor="mm")
    d.text((X0 + 2 * 170 + 70, 810), "medium", font=F(COND, 30), fill=SIG, anchor="ma")
    fig(d, "OkCupid looks ratings, 1 to 5")

def sc_women(img, d, t):
    t0 = S("women"); te = cue("women", "eighty") - .3
    d.text((X0, 320), "WOMEN RATE MEN", font=F(BLK, 92), fill=INK)
    hist(d, X0 + 20, 1060, [.95, .85, .42, .2, .08], k=(t - t0 - .2) / 1.2, bw=130, gap=34, hmax=420, hi=(0, 1) if t >= te else ())
    if t >= te: box_label(d, X1, 480, "80 % BELOW MEDIUM", 40, WHITE, SIG, font=BLK, anchor="ra")
    fig(d, "schematic shape · ratings 1 to 5")

def sc_men(img, d, t):
    t0 = S("men")
    d.text((X0, 320), "MEN RATE WOMEN", font=F(BLK, 92), fill=INK)
    hist(d, X0 + 20, 1060, [.25, .6, .95, .6, .25], k=(t - t0 - .2) / 1.2, bw=130, gap=34, hmax=420, hi=(2,) if t >= cue("men", "middle") - .3 else ())
    if t >= cue("men", "middle") - .3: box_label(d, X1, 480, "MOSTLY MEDIUM", 40, WHITE, SIG, font=BLK, anchor="ra")
    fig(d, "schematic shape · ratings 1 to 5")

def sc_twist(img, d, t):
    t0, tt = S("twist"), cue("twist", "two thirds") - .3
    d.text((X0, 320), "BUT MESSAGES:", font=F(BLK, 100), fill=INK)
    for c in range(3):
        for r in range(2):
            x = 210 + c * 270; y = 700 + r * 200; top = c == 2
            silhouette(img, lambda m, x=x, y=y: front_bust(m, x, y, .2, 255), (x - 70, y - 40, x + 70, y + 110), SIG if top and t >= tt else MID, cell=5)
    if t >= tt:
        d.text((X0, 450), "2/3", font=F(BLK, 150), fill=SIG)
        k = ease((t - tt) / .5); d.rectangle([X1 - 250, 620, X1 - 250 + 250 * k, 1110], outline=SIG, width=6)
        d.text((X1 - 125, 1120), "best-looking third", font=F(COND, 26), fill=SIG, anchor="ma")
    fig(d, "of men's messages")

def sc_point(img, d, t):
    t0, tc = S("point"), cue("point", "men chase") - .2
    words_in(d, t, [("WOMEN", t0 + .1, 320, 130, INK), ("JUDGE HARDER.", t0 + .35, 450, 116, INK)] + ([("MEN", tc, 630, 130, SIG), ("CHASE HARDER.", tc + .25, 760, 116, SIG)] if t >= tc else []))
    fig(d, "fig. 2 — pick your poison")

EP.scenes = {"hook": sc_hook, "study": sc_study, "women": sc_women, "men": sc_men, "twist": sc_twist, "point": sc_point}
FX = [(0.0, thud(.55), 0), (.8, pop(.15), 0), *EP.cut_fx(), *[(S("study") + .3 + i * .12, tick(.035), (i - 2) / 3) for i in range(5)],
      (S("women") + .2, riser(1.0, .04), 0), (cue("women", "eighty") - .3, thud(.5), 0), (cue("men", "middle") - .3, pop(.15), 0),
      (cue("twist", "two thirds") - .3, thud(.5), 0), (cue("point", "men chase") - .2, thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
