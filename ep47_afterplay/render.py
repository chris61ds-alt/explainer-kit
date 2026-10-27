"""NOT JUST YOU · AFTER DARK – No. 47: post-sex affection and satisfaction (Muise, Giang & Impett 2014)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .8, "result": .5, "link": .5, "later": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "link", "later", "point", "end"]
EP = Episode(TL, 47, "AFTERPLAY", order=ORDER, dark=True, series="NOT JUST YOU · AFTER DARK",
             chapters={"hook": "AFTER", "study": "THE STUDY", "result": "15 MINUTES", "link": "THE LINK", "later": "3 MONTHS", "point": "STAY"},
             sources=("Muise, Giang & Impett (2014),", "Archives of Sexual Behavior 43(7)"),
             music=dict(bpm=80, root=3, prog="warm", kick="half", gaps=[(E("study") + .05, S("result") + .05)]),
             cover=dict(words=["WHAT", "HAPPENS", "AFTER."], kicker="The underrated part."))

HUG = {"arms": ((70, 20), (-10, -5))}
def heart(d, cx, cy, r, col=SIG):
    d.ellipse([cx - r, cy - r * .9, cx, cy + r * .1], fill=col); d.ellipse([cx, cy - r * .9, cx + r, cy + r * .1], fill=col)
    d.polygon([(cx - r * .98, cy - r * .3), (cx + r * .98, cy - r * .3), (cx, cy + r * .95)], fill=col)

def pair(d, t, cx=480, s=.95, close=1.0):
    g = lerp(150, 80, ease(close))
    picto(d, cx - g, FLOOR, s, INK, f=1, pose=blend(IDLE, HUG, ease(close))); picto(d, cx + g, FLOOR, s, SIG, f=-1, pose=blend(IDLE, HUG, ease(close)))

def sc_hook(img, d, t):
    ta = cue("hook", "what happens")
    d.text((X0 - 6, 300), "UNDERRATED:", font=F(BLK, 120), fill=INK)
    words_in(d, t, [("AFTER.", ta - .1, 440, 230, SIG)])
    pair(d, t, close=(t - ta) / .8)
    if t >= ta + .4: heart(d, 480, 760 - 8 * math.sin(t * 4), 36 * back((t - ta - .4) / .4))
    fig(d, "fig. 1 — the part nobody talks about")

def sc_study(img, d, t):
    t0 = S("study"); tc = cue("study", "a hundred")
    counter(d, X0, 300, t, t0 + .1, .9, 335, "{:.0f}", 200, SIG); d.text((X0 + 6, 510), "people surveyed", font=F(COND, 36), fill=INK)
    if t >= tc - .2:
        counter(d, X0, 600, t, tc - .2, .6, 101, "{:.0f} couples", 110, INK)
        k = clamp((t - tc) / 1.6)
        for i in range(21):
            r, c = divmod(i, 7); x = X0 + 10 + c * 120; y = 780 + r * 100
            d.rectangle([x, y, x + 100, y + 80], outline=INK, width=3, fill=SIG if i < 21 * k else None)
    fig(d, "online survey + 21-day couple diaries")

def sc_result(img, d, t):
    t0 = S("result"); k = clamp((t - t0 - .1) / 1.4)
    counter(d, X0, 300, t, t0 + .1, 1.4, 15, "≈ {:.0f} MIN", 170, SIG)
    cx, cy, r = 300, 800, 170
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=8)
    if k > 0: d.pieslice([cx - r + 14, cy - r + 14, cx + r - 14, cy + r - 14], -90, -90 + 90 * k, fill=SIG)
    for i in range(12):
        a = math.radians(i * 30); d.line([cx + math.cos(a) * (r - 24), cy + math.sin(a) * (r - 24), cx + math.cos(a) * (r - 6), cy + math.sin(a) * (r - 6)], fill=INK, width=4)
    for i, (w, lab) in enumerate((("cuddling", "CUDDLING"), ("kissing", "KISSING"), ("talking", "TALKING"))):
        tk = cue("result", w) - .2
        if t >= tk: box_label(d, 560 + (1 - ease((t - tk) / .3)) * 40, 660 + i * 110, lab, 38, WHITE, SIG if i == 0 else INK)
    fig(d, "average affection time after intimacy")

OX, OY, GW, GH = X0 + 50, 1060, X1 - X0 - 70, 420
def sc_link(img, d, t):
    t0 = S("link"); k = clamp((t - t0 - .1) / 2.0)
    d.text((X0, 300), "LONGER =", font=F(BLK, 140), fill=INK); d.text((X0, 450), "HAPPIER", font=F(BLK, 140), fill=SIG)
    d.line([OX, OY, OX + GW, OY], fill=INK, width=4); d.line([OX, OY, OX, OY - GH + 60], fill=INK, width=4)
    d.text((OX + GW, OY + 18), "afterplay →", font=F(MONO, 20), fill=MID, anchor="ra"); d.text((OX + 10, OY - GH + 50), "satisfaction", font=F(COND, 26), fill=INK, anchor="ld")
    for j, (col, off, w) in enumerate(((SIG, 0, "sex life"), (INK, 50, "relationship"))):
        kk = clamp(k - j * .2) if t < cue("link", "relationship") - .3 or j == 0 else clamp((t - cue("link", "relationship") + .3) / .8)
        if j == 1 and t < cue("link", "relationship") - .3: continue
        x2 = OX + 20 + (GW - 60) * kk; y2 = OY - 40 - off - (GH - 180) * kk
        d.line([OX + 20, OY - 40 - off, x2, y2], fill=col, width=7)
        if kk > .95: d.text((x2 - 10, y2 - 14), w, font=F(BLK, 28), fill=col, anchor="rd")
    d.text((X1, 1146), "schematic", font=F(MED, 22), fill=MID, anchor="ra")

def sc_later(img, d, t):
    t0 = S("later"); tp = cue("later", "parents")
    counter(d, X0, 300, t, t0 + .1, .6, 3, "+{:.0f} MONTHS", 150, SIG)
    hbar(d, 560, .45, (t - t0 - .2) / .5, MID, "less afterplay", h=80)
    hbar(d, 700, .72, (t - t0 - .5) / .5, SIG, "more afterplay", h=80)
    if t >= tp - .2:
        k = ease((t - tp + .2) / .4)
        picto(d, 200, FLOOR, .8, INK, f=1, pose=HUG); picto(d, 310, FLOOR, .45, SIG, f=-1, pose=WAVE(t)); picto(d, 430, FLOOR, .8, INK, f=-1, pose=HUG)
        box_label(d, X1, 960 + (1 - k) * 30, "PARENTS: STRONGER", 36, WHITE, SIG, anchor="ra")
    fig(d, "still more satisfied at follow-up · schematic")

def sc_point(img, d, t):
    t0 = S("point"); tc = cue("point", "the cuddle")
    words_in(d, t, [("DON'T", t0, 300, 170, INK), ("RUSH OFF.", t0 + .3, 470, 150, SIG)] if t < tc - .2 else [("THE CUDDLE", tc - .2, 300, 120, INK), ("COUNTS.", tc + .1, 430, 190, SIG)])
    pair(d, t, close=(t - t0 - .2) / .8)
    if t >= tc: heart(d, 480, 760, 44 * back((t - tc) / .4))
    fig(d, "fig. 2 — stay a little longer")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "link": sc_link, "later": sc_later, "point": sc_point}
FX = [(0.0, thud(.5), 0), (cue("hook", "what happens"), thud(.4), 0), (cue("hook", "what happens") + .4, pop(.15), 0), *EP.cut_fx(),
      *[(cue("study", "a hundred") + i * .076, tick(.04), (i % 5 - 2) / 3) for i in range(21)],
      (S("result") + .05, thud(.55), 0), *[(cue("result", w) - .2, pop(.15), (i - 1) / 2) for i, w in enumerate(("cuddling", "kissing", "talking"))],
      (S("link") + .1, riser(2.0, .05), 0), (cue("later", "parents"), thud(.35), 0), (cue("point", "the cuddle"), riser(.4, .06), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
