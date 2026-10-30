"""NOT JUST YOU – No. 76: hot photos are old photos (OkTrends 2010). Look C+D, dark."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from dating import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .6, "study": .5, "height": .6, "photos": .5, "old": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "height", "photos", "old", "point", "end"]
EP = ThreadEpisode(TL, 76, "THE OLD PHOTO", order=ORDER, dark=True, label="PLATFORM DATA · OKCUPID",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("OkTrends (2010), The Big Lies People", "Tell In Online Dating · OkCupid"),
                   music=dict(bpm=98, root=-1, prog="tense", kick="four", gaps=[(E("study") + .05, S("height") + .05)]),
                   cover=dict(words=["HOT PHOTO?", "OLD PHOTO."], kicker="The data says so."))

def sc_hook(img, d, t):
    to = cue("hook", "probably old") - .2
    d.text((X0 - 6, 320), "HOT PHOTO?", font=F(BLK, 150), fill=INK)
    profile_card(img, d, 330, 880, .8, photo=1, col=SIG)
    if t >= to:
        bbox(d, (180, 650, 480, 860), "AGE: ?", SIG, (t - to) / .3, coords=False)
        box_label(d, 580, 760, "PROBABLY", 44, WHITE, INK, font=BLK); box_label(d, 580, 830, "OLD.", 70, WHITE, SIG, font=BLK)
    fig(d, "fig. 1 — your best angle, from when?")

def sc_study(img, d, t):
    t0 = S("study")
    d.text((X0, 320), "CLAIMED", font=F(BLK, 130), fill=MID); d.text((X0, 460), "VS. DATA", font=F(BLK, 130), fill=SIG)
    dot_field(d, (X0 + 14, 660, X1, 1100), t, cell=32, col=MID, hit={12, 33, 58, 90, 131})
    fig(d, "OkCupid profiles vs. site data")

def sc_height(img, d, t):
    t0, tp = S("height"), cue("height", "poorer") - .3
    counter(d, X0, 320, t, t0 + .1, .6, 2, "− {:.0f} IN", 170, SIG)
    silhouette(img, lambda m: body(m, 220, 1120, 470, 255), (90, 620, 350, 1125), MID, cell=7)
    silhouette(img, lambda m: body(m, 400, 1120, 430, 255), (270, 660, 530, 1125), INK, cell=7)
    dim_v(d, 520, 650, 690, ease((t - t0 - .5) / .4), SIG, "said vs. real", 24)
    if t >= tp:
        counter(d, 600, 640, t, tp, .5, 20, "− {:.0f} %", 120, SIG)
        banknote(d, 730, 880, .9, "100"); banknote(d, 760, 960, .9, "80", SIG)
        d.text((600, 1050), "income", font=F(COND, 34), fill=INK)
    fig(d, "taller and richer on paper")

def sc_photos(img, d, t):
    t0, th = S("photos"), cue("photos", "hottest") - .3
    d.text((X0, 320), "1 IN 3+", font=F(BLK, 200), fill=SIG)
    d.text((X0 + 6, 540), "of the hottest photos: a year old or more", font=F(COND, 38), fill=INK)
    for i in range(3):
        x = 210 + i * 270; old = i == 0 and t >= th
        profile_card(img, d, x, 870, .66, photo=1, col=SIG if old else INK, badge="1 YR+" if old else None)
    fig(d, "photo age at upload, from metadata")

def sc_old(img, d, t):
    t0 = S("old"); tv = cue("old", "twelve") - .3
    d.text((X0, 320), "3 YEARS+", font=F(BLK, 160), fill=INK)
    for j, (v, lab, col) in enumerate(((12, "hot photos", SIG), (5, "average photos", MID))):
        k = ease((t - tv - j * .3) / .5) if t >= tv else 0; y = 600 + j * 170
        d.rectangle([X0, y, X0 + 820 * v / 14 * k, y + 100], fill=col)
        if k > .9: d.text((X0 + 820 * v / 14 * k + 16, y + 50), f"{v} %", font=F(BLK, 60), fill=col, anchor="lm")
        d.text((X0, y + 112), lab, font=F(COND, 32), fill=INK)
    fig(d, "share of photos older than three years")

def sc_point(img, d, t):
    t0, to = S("point"), cue("point", "the older") - .2
    words_in(d, t, [("THE BETTER", t0 + .1, 320, 140, INK), ("THE PHOTO,", t0 + .4, 470, 140, INK)] + ([("THE OLDER", to, 650, 140, SIG), ("IT PROBABLY IS.", to + .3, 800, 104, SIG)] if t >= to else []))
    fig(d, "fig. 2 — check the haircut")

EP.scenes = {"hook": sc_hook, "study": sc_study, "height": sc_height, "photos": sc_photos, "old": sc_old, "point": sc_point}
FX = [(0.0, thud(.5), 0), (cue("hook", "probably old") - .2, pop(.15), 0), *EP.cut_fx(), *[(S("study") + .3 + i * .12, tick(.03), (i % 5 - 2) / 3) for i in range(6)],
      (S("height") + .1, thud(.5), 0), (cue("height", "poorer") - .3, thud(.4), .3), (S("photos") + .05, thud(.5), 0), (cue("photos", "hottest") - .3, pop(.15), -.3),
      (cue("old", "twelve") - .3, pop(.15), 0), (cue("point", "the older") - .2, thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
