"""NOT JUST YOU – No. 67: everyone messages out of their league (Bruch & Newman 2018). Look C+D, dark."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from thread import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .8, "result": .5, "reply": .5, "age": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "reply", "age", "point", "end"]
EP = ThreadEpisode(TL, 67, "OUT OF YOUR LEAGUE", order=ORDER, dark=True,
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Bruch & Newman (2018),", "Science Advances 4(8)"),
                   music=dict(bpm=100, root=1, prog="tense", kick="four", gaps=[(E("study") + .05, S("result") + .05)]),
                   cover=dict(words=["OUT OF", "YOUR LEAGUE."], kicker="Everyone does it."))

def ladder(d, x, y0, y1, n=10, col=INK):
    d.line([x, y0, x, y1], fill=col, width=4)
    for i in range(n + 1):
        y = lerp(y1, y0, i / n); d.line([x - 16, y, x + 16, y], fill=col, width=3)
        if i % 5 == 0: d.text((x - 28, y), f"{i * 10}", font=F(MONO, 20), fill=MID, anchor="rm")

def phone_msg(d, x, y, w, txt, col, k=1.0):
    if k <= 0: return
    d.rounded_rectangle([x, y, x + w * ease(k), y + 70], radius=30, fill=col)
    if k > .9: d.text((x + 28, y + 35), txt, font=F(COND, 32), fill=WHITE, anchor="lm")

def sc_hook(img, d, t):
    d.text((X0 - 6, 320), "OUT OF", font=F(BLK, 190), fill=INK); d.text((X0 - 6, 510), "YOUR LEAGUE.", font=F(BLK, 120), fill=SIG)
    ladder(d, 880, 700, 1120)
    silhouette(img, lambda m: front_bust(m, 300, 900, .45, 255), (120, 790, 480, 1130), INK, cell=8)
    silhouette(img, lambda m: front_bust(m, 640, 760, .38, 255), (500, 660, 790, 960), SIG, cell=7)
    d.line(spline([(380, 920), (500, 880), (560, 800)]), fill=SIG, width=5)
    fig(d, "fig. 1 — shooting your shot")

def sc_study(img, d, t):
    t0 = S("study")
    d.text((X0, 320), "4 CITIES", font=F(BLK, 170), fill=SIG)
    for i, c in enumerate(("NEW YORK", "BOSTON", "CHICAGO", "SEATTLE")):
        k = ease((t - t0 - .3 - i * .2) / .3)
        if k > 0: box_label(d, X0 + (i % 2) * 430, 540 + (i // 2) * 90, c, 40, WHITE, INK if i % 2 else MID, font=BLK)
    if t >= cue("study", "ranked") - .2:
        ladder(d, 840, 760, 1110)
        for i in range(18):
            v = (i * 37 % 100) / 100; y = lerp(1110, 760, v); x = X0 + 40 + (i * 47) % 600
            d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=SIG if i == 7 else MID)
    fig(d, "desirability ranked by who messages whom")

def sc_result(img, d, t):
    t0 = S("result")
    counter(d, X0, 320, t, t0 + .1, .7, 25, "+{:.0f} %", 240, SIG)
    d.text((X0 + 6, 570), "more desirable than themselves", font=F(COND, 40), fill=INK)
    k = ease((t - t0 - .3) / .8)
    ladder(d, 840, 680, 1110)
    y_me, y_them = lerp(1110, 680, .45), lerp(1110, 680, .45 + .25 * k)
    d.ellipse([820 - 18, y_me - 18, 820 + 18, y_me + 18], fill=INK); d.text((790, y_me), "you", font=F(MONO, 22), fill=INK, anchor="rm")
    d.ellipse([860 - 18, y_them - 18, 860 + 18, y_them + 18], fill=SIG); d.text((890, y_them), "them", font=F(MONO, 22), fill=SIG, anchor="lm")
    fig(d, "typical first message")

def sc_reply(img, d, t):
    t0, to = S("reply"), cue("reply", "but about") - .2
    d.text((X0, 320), "SEEN.", font=F(BLK, 200), fill=INK)
    for i in range(4):
        phone_msg(d, X0 + 40, 560 + i * 100, 520, "hey :)", SIG if i else MID, (t - t0 - .1 - i * .2) / .3)
    if t >= to:
        phone_msg(d, X1 - 420, 980, 400, "hi! :)", INK, (t - to) / .3)
        box_label(d, X1, 1090, "≈ 1 IN 5 GOT A REPLY", 30, WHITE, SIG, anchor="ra")
    fig(d, "most messages up the ladder go unanswered")

def sc_age(img, d, t):
    t0 = S("age"); k = clamp((t - t0 - .2) / 2.2)
    d.text((X0, 320), "AGE", font=F(BLK, 170), fill=INK)
    OX, OY, GW, GH = X0 + 40, 1060, X1 - X0 - 60, 360
    d.line([OX, OY, OX + GW, OY], fill=INK, width=4); d.line([OX, OY, OX, OY - GH], fill=INK, width=4)
    for i, a in enumerate((18, 30, 40, 50, 60)):
        x = OX + GW * (a - 18) / 42; d.text((x, OY + 18), str(a), font=F(MONO, 20), fill=MID, anchor="ma")
    n = max(2, int(50 * k)); us = np.linspace(0, k, n)
    men = [(OX + GW * u, OY - GH * (.35 + .5 * min(1, u / .76) - .1 * max(0, u - .76) / .24)) for u in us]
    wom = [(OX + GW * u, OY - GH * (.85 - .6 * u)) for u in us]
    d.line(men, fill=INK, width=7); d.line(wom, fill=SIG, width=7)
    if k > .95: d.text((men[-1][0] - 10, men[-1][1] - 14), "men", font=F(BLK, 30), fill=INK, anchor="rd"); d.text((wom[-1][0] - 10, wom[-1][1] + 12), "women", font=F(BLK, 30), fill=SIG, anchor="ra")
    d.text((X1, 1146), "desirability on this site · schematic", font=F(MED, 22), fill=MID, anchor="ra")

def sc_point(img, d, t):
    t0, tj = S("point"), cue("point", "just don't") - .2
    words_in(d, t, [("AIM HIGH.", t0, 320, 200, SIG)] + ([("SILENCE ISN'T", tj, 540, 110, INK), ("PERSONAL.", tj + .2, 660, 110, INK)] if t >= tj else []))
    ladder(d, 880, 760, 1120)
    fig(d, "fig. 2 — it's a numbers game")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "reply": sc_reply, "age": sc_age, "point": sc_point}
FX = [(0.0, thud(.5), 0), (.3, whoosh(.6, .06), 0), *EP.cut_fx(), *[(S("study") + .3 + i * .2, pop(.12), (i - 1.5) / 2) for i in range(4)],
      (S("result") + .05, thud(.55), 0), (S("result") + .3, riser(.8, .05), 0), *[(S("reply") + .1 + i * .2, tick(.04), .3) for i in range(4)],
      (cue("reply", "but about") - .2, pop(.18), 0), (S("age") + .2, whoosh(1.4, .05), 0), (S("point") + .05, thud(.5), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
