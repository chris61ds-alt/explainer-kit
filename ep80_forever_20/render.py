"""NOT JUST YOU – No. 80: men's ideal age stays 20 (Rudder 2014, Dataclysm). Look C+D, dark."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from dating import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .6, "data": .6, "women": .6, "but": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "data", "women", "but", "point", "end"]
EP = ThreadEpisode(TL, 80, "FOREVER 20", order=ORDER, dark=True, label="PLATFORM DATA · OKCUPID",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Rudder (2014), Dataclysm,", "OkCupid data"),
                   music=dict(bpm=96, root=-2, prog="minor", kick="half", gaps=[(E("data") + .05, S("women") + .05)]),
                   cover=dict(words=["HE'S 50.", "HIS TYPE: 20."], kicker="What dating data shows."))
OX, OY, GW, GH = X0 + 70, 1060, X1 - X0 - 100, 440

def chart(d, t, k_m, k_w=0.0):
    d.line([OX, OY, OX + GW, OY], fill=INK, width=4); d.line([OX, OY, OX, OY - GH], fill=INK, width=4)
    for i, a in enumerate((20, 30, 40, 50)):
        x = OX + GW * i / 3; d.text((x, OY + 14), str(a), font=F(MONO, 22), fill=MID, anchor="ma")
        y = OY - GH * i / 3; d.text((OX - 14, y), str(a), font=F(MONO, 22), fill=MID, anchor="rm")
    d.text((OX + GW, OY + 44), "rater's own age", font=F(COND, 26), fill=INK, anchor="ra")
    d.text((OX + 10, OY - GH - 12), "most attractive age", font=F(COND, 26), fill=INK, anchor="ld")
    if k_m > 0:
        n = max(2, int(40 * clamp(k_m))); pts = [(OX + GW * u, OY - GH * (.05 + .06 * u) / 1) for u in np.linspace(0, clamp(k_m), n)]
        d.line(pts, fill=SIG, width=9)
        if k_m >= 1: d.text((pts[-1][0], pts[-1][1] - 16), "men", font=F(BLK, 34), fill=SIG, anchor="rd")
    if k_w > 0:
        n = max(2, int(40 * clamp(k_w))); pts = [(OX + GW * u, OY - GH * (.03 + .85 * u)) for u in np.linspace(0, clamp(k_w), n)]
        d.line(pts, fill=INK, width=9)
        if k_w >= 1: d.text((pts[-1][0] - 14, pts[-1][1]), "women", font=F(BLK, 34), fill=INK, anchor="rm")

def sc_hook(img, d, t):
    tf = cue("hook", "fifty") - .3
    silhouette(img, lambda m: body(m, 240, 1120, 460, 255), (100, 640, 380, 1125), INK, cell=7)
    box_label(d, 240, 600, "20", 40, WHITE, INK, font=BLK, anchor="ma")
    if t >= tf:
        silhouette(img, lambda m: body(m, 520, 1120, 470, 255), (380, 630, 660, 1125), MID, cell=7)
        box_label(d, 520, 590, "50", 40, WHITE, MID, font=BLK, anchor="ma")
    d.text((X0 - 6, 320), "HIS TYPE:", font=F(BLK, 120), fill=INK)
    d.text((X0 - 6, 440), "20.", font=F(BLK, 120), fill=SIG)
    if t >= tf + .4: box_label(d, X1, 760, "STILL 20.", 56, WHITE, SIG, font=BLK, anchor="ra")
    fig(d, "fig. 1 — two men, one answer")

def sc_data(img, d, t):
    t0 = S("data")
    d.text((X0, 320), "EVERY AGE:", font=F(BLK, 110), fill=INK); d.text((X0, 440), "EARLY 20s.", font=F(BLK, 110), fill=SIG)
    chart(d, t, (t - t0 - .3) / 1.6)
    d.text((X1, 1146), "schematic", font=F(MED, 22), fill=MID, anchor="ra")

def sc_women(img, d, t):
    t0 = S("women")
    d.text((X0, 320), "WOMEN'S TASTE", font=F(BLK, 100), fill=INK); d.text((X0, 430), "GREW UP.", font=F(BLK, 110), fill=MID)
    chart(d, t, 1, (t - t0 - .3) / 1.6)
    d.text((X1, 1146), "schematic", font=F(MED, 22), fill=MID, anchor="ra")

def sc_but(img, d, t):
    t0, tm = S("but"), cue("but", "messaged") - .3
    d.text((X0, 320), "BUT THEY", font=F(BLK, 120), fill=INK); d.text((X0, 450), "MESSAGE:", font=F(BLK, 120), fill=INK)
    if t >= tm:
        d.text((X0, 600), "THEIR OWN AGE.", font=F(BLK, 104), fill=SIG)
        silhouette(img, lambda m: bust(m, 270, 920, .42, 255, f=1), (80, 820, 470, 1130), INK, cell=7)
        silhouette(img, lambda m: bust(m, 640, 920, .42, 255, f=-1), (450, 820, 840, 1130), SIG, cell=7)
        bubbles(d, 380, 560, 780, 2, k=(t - tm) / .6, h=40, gap=12)
    fig(d, "hardly any men in their 30s message 20-year-olds")

def sc_point(img, d, t):
    t0, tm = S("point"), cue("point", "their messages") - .2
    words_in(d, t, [("RATINGS:", t0 + .1, 320, 120, MID), ("FANTASY.", t0 + .35, 440, 150, INK)] + ([("MESSAGES:", tm, 640, 120, MID), ("REALITY.", tm + .25, 760, 150, SIG)] if t >= tm else []))
    fig(d, "fig. 2 — what they click vs. who they write")

EP.scenes = {"hook": sc_hook, "data": sc_data, "women": sc_women, "but": sc_but, "point": sc_point}
FX = [(0.0, thud(.5), 0), (cue("hook", "fifty") - .3, pop(.15), .3), (cue("hook", "fifty") + .1, thud(.4), 0), *EP.cut_fx(),
      (S("data") + .3, whoosh(1.6, .05), 0), (S("women") + .3, whoosh(1.6, .05), 0), (cue("but", "messaged") - .3, thud(.5), 0),
      (cue("point", "their messages") - .2, thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
