"""NOT JUST YOU – No. 91: teens like what's already liked (Sherman et al. 2016, Psychological Science). Look C+D, dark."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from thread import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .6, "trick": .5, "result": .5, "brain": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "trick", "result", "brain", "point", "end"]
EP = ThreadEpisode(TL, 91, "LIKES", order=ORDER, dark=True, label="SMALL STUDY · 32 TEENS",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Sherman et al. (2016), The Power of the Like", "in Adolescence, Psychological Science"),
                   music=dict(bpm=98, root=-1, prog="dream", kick="half", audio="v5", gaps=[(E("study") + .05, S("trick") + .05)]),
                   cover=dict(words=["YOU LIKE", "WHAT'S LIKED."], kicker="Even your own photos."))

def heart(d, x, y, s=1.0, col=SIG):
    r = 12 * s
    d.ellipse([x - 2 * r, y - r, x, y + r], fill=col); d.ellipse([x, y - r, x + 2 * r, y + r], fill=col)
    d.polygon([(x - 2 * r + 1, y + r * .3), (x + 2 * r - 1, y + r * .3), (x, y + 2.4 * r)], fill=col)

def photo(img, d, x0, y0, w=330, h=420, likes=0, col=INK, hcol=SIG, k=1.0):
    """feed post: frame, halftone portrait, a row of hearts (likes = 0..1, schematic)"""
    if k <= 0: return
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=18, outline=col, width=4)
    silhouette(img, lambda m: front_bust(m, x0 + w / 2, y0 + 130, .3, 255), (int(x0 + 14), int(y0 + 14), int(x0 + w - 14), int(y0 + h - 90)), col, cell=7, k=k)
    n = int(round(likes * 8))
    for i in range(8):
        hx = x0 + 34 + i * 38
        heart(d, hx, y0 + h - 56, .8, hcol if i < n else RULE)

def sc_hook(img, d, t):
    tb = cue("hook", "Your brain") - .2
    d.text((X0 - 4, 320), "YOU LIKE IT", font=F(BLK, 130), fill=INK)
    d.text((X0 - 4, 450), "BECAUSE IT'S GOOD?", font=F(BLK, 80), fill=INK)
    photo(img, d, 315, 640, likes=.6)
    if t >= tb: box_label(d, X1 - (1 - ease((t - tb) / .25)) * 40, 570, "YOUR BRAIN DISAGREES", 38, WHITE, SIG, font=BLK, anchor="ra")
    fig(d, "fig. 1 — a feed post, schematic")

def sc_study(img, d, t):
    t0 = S("study")
    counter(d, X0, 320, t, t0 + .1, .6, 32, "{:.0f}", 230, INK)
    d.text((X0 + 290, 360), "TEENS", font=F(BLK, 120), fill=INK)
    ti = cue("study", "Instagram-style") - .1
    d.text((X0 + 6, 570), "ages 13 to 18 · UCLA" + (" · Instagram-style feed" if t >= ti else ""), font=F(COND, 40), fill=INK)
    silhouette(img, lambda m: bust(m, 470, 840, .9, 255), (200, 650, 760, 1125), MID, cell=9)
    k = clamp((t - cue("study", "inside a brain") + .1) / .6)
    if k > 0:
        d.arc([270, 620, 690, 1000], 200, 200 + 140 * k, fill=INK, width=14); d.arc([270, 620, 690, 1000], -20, -20 + 140 * k, fill=INK, width=14)
    fig(d, "inside a brain scanner (fMRI)")

L_CARD, R_CARD = (X0 + 20, 640), (X0 + 470, 640)
def sc_trick(img, d, t):
    t0, ts = S("trick"), cue("trick", "Same photo") - .2
    d.text((X0, 320), "THE TRICK:", font=F(BLK, 130), fill=INK)
    d.text((X0 + 4, 470), "the likes were set by the researchers", font=F(COND, 44), fill=INK)
    photo(img, d, *L_CARD, likes=ease((t - ts) / .6) if t >= ts else 0)
    photo(img, d, *R_CARD, likes=.25 * ease((t - ts - .3) / .4) if t >= ts else 0, hcol=MID)
    if t >= ts:
        d.text((L_CARD[0] + 165, 1080), "LOTS OF LIKES", font=F(BLK, 34), fill=INK, anchor="ma")
        d.text((R_CARD[0] + 165, 1080), "JUST A FEW", font=F(BLK, 34), fill=MID, anchor="ma")
    fig(d, "same photo · like counts schematic")

def sc_result(img, d, t):
    t0, te = S("result"), cue("result", "Even their own") - .2
    d.text((X0, 320), "LOTS OF LIKES:", font=F(BLK, 100), fill=INK)
    d.text((X0, 430), "THEY LIKED IT TOO.", font=F(BLK, 90), fill=SIG)
    photo(img, d, X0 + 20, 640, likes=1.0)
    k = ease((t - t0 - .4) / .4)
    if k > 0:
        heart(d, 650, 760, 3.2 * (.6 + .4 * k), SIG)
        d.text((650, 900), "+ 1", font=F(BLK, 80), fill=SIG, anchor="ma")
    if t >= te: box_label(d, X1, 1010, "EVEN THEIR OWN PHOTOS", 36, WHITE, INK, font=BLK, anchor="ra")
    fig(d, "more likely to like a photo with many likes")

def sc_brain(img, d, t):
    t0, tr = S("brain"), cue("brain", "reward center") - .2
    d.text((X0, 320), "REWARD", font=F(BLK, 160), fill=INK)
    d.text((X0, 480), "lit up more", font=F(BLK, 80), fill=INK)
    silhouette(img, lambda m: bust(m, 470, 840, .9, 255), (200, 650, 760, 1125), MID, cell=9)
    if t >= tr:
        k = ease((t - tr) / .4); r = 34 + 8 * math.sin(t * 9) * k
        d.ellipse([500 - r, 800 - r, 500 + r, 800 + r], fill=SIG)
        bbox(d, (430, 730, 570, 870), "REWARD CENTER", SIG, k, coords=False, size=24)
    fig(d, "nucleus accumbens · for photos with many likes · schematic")

def sc_point(img, d, t):
    t0, ta = S("point"), cue("point", "You like what's") - .2
    words_in(d, t, [("NOT WHAT'S", t0 + .2, 320, 130, MID), ("GOOD.", t0 + .4, 450, 170, INK)] +
             ([("WHAT'S", ta, 660, 120, SIG), ("ALREADY LIKED.", ta + .2, 780, 110, SIG)] if t >= ta else []))
    for i in range(8): heart(d, X0 + 40 + i * 70, 1040, 1.1, SIG if t >= ta + .3 + i * .06 else RULE)
    fig(d, "fig. 2 — 32 teens, one experiment")

# magic move: the photo with lots of likes moves into the result scene
EP.carry = {"result": [((L_CARD[0], L_CARD[1], L_CARD[0] + 330, L_CARD[1] + 420), (X0 + 20, 640, X0 + 350, 1060))]}

EP.scenes = {"hook": sc_hook, "study": sc_study, "trick": sc_trick, "result": sc_result, "brain": sc_brain, "point": sc_point}
FX = [(0.0, thud(.5), 0), (cue("hook", "Your brain") - .2, pop(.15), .3), *EP.cut_fx(), (S("study") + .1, pop(.12), 0),
      (cue("study", "Instagram-style") - .1, pop(.12), .2), (cue("study", "inside a brain") - .1, riser(.6, .05), 0), (cue("study", "inside a brain") + .5, tick(.06), 0), *[(cue("trick", "Same photo") - .2 + i * .075, tick(.035), -.4) for i in range(8)],
      (cue("trick", "Same photo") + .1, tick(.035), .4), (S("result") + .4, thud(.5), 0), (cue("result", "Even their own") - .2, pop(.15), .3),
      (cue("brain", "reward center") - .2, thud(.45), 0), (cue("point", "You like what's") - .2, thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
