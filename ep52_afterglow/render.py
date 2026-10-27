"""NOT JUST YOU · AFTER DARK – No. 52: the 48-hour sexual afterglow (Meltzer et al. 2017)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .8, "result": .5, "who": .5, "months": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "who", "months", "point", "end"]
EP = Episode(TL, 52, "THE AFTERGLOW", order=ORDER, dark=True, series="NOT JUST YOU · AFTER DARK",
             chapters={"hook": "48 HOURS", "study": "THE DIARIES", "result": "THE GLOW", "who": "EVERYONE", "months": "MONTHS LATER", "point": "KEEP IT WARM"},
             sources=("Meltzer et al. (2017),", "Psychological Science 28(5)"),
             music=dict(bpm=84, root=4, prog="warm", kick="half", gaps=[(E("study") + .05, S("result") + .05)]),
             cover=dict(words=["THE 48-HOUR", "GLOW."], kicker="One night, two days."))

def glow(d, cx, cy, r, k, t=0.0):
    for i in range(6, 0, -1):
        rr = r * (1 + i * .28) * (1 + .03 * math.sin(t * 3 + i))
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=mix(BG, SIG, k * (.08 + .1 * (6 - i) / 6)))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=mix(BG, SIG, k))

def pair(d, cx=480, s=.9, col2=SIG):
    p = {"arms": ((70, 20), (-10, -5))}
    picto(d, cx - 80 * s, FLOOR, s, INK, f=1, pose=p); picto(d, cx + 80 * s, FLOOR, s, col2, f=-1, pose=p)

def sc_hook(img, d, t):
    k = ease((t - .2) / .6)
    glow(d, 480, 900, 90, k, t)
    d.text((X0 - 6, 300), "48 H", font=F(BLK, 230), fill=SIG)
    d.text((X0, 540), "of afterglow", font=F(COND, 44), fill=INK)
    pair(d)
    fig(d, "fig. 1 — the night is only the start")

def sc_study(img, d, t):
    t0 = S("study")
    counter(d, X0, 300, t, t0 + .1, .9, 214, "{:.0f} couples", 140, SIG)
    d.text((X0 + 6, 470), "newlyweds · two separate studies", font=F(COND, 36), fill=INK)
    tk = cue("study", "every single")
    for i in range(14):
        r, c = divmod(i, 7); x = X0 + 60 + c * 120; y = 680 + r * 190; on = t >= tk - .8 + i * .1
        d.ellipse([x - 40, y - 40, x + 40, y + 40], fill=INK if on else None, outline=INK, width=3)
        if on: d.ellipse([x - 40 + 22, y - 40 - 6, x + 40 + 22, y + 40 - 6], fill=BG)
        d.text((x, y + 56), f"{i + 1}", font=F(MONO, 20), fill=MID, anchor="ma")
    fig(d, "14 nightly diaries · Meltzer et al., 2017")

OX, OY, GW, GH = X0 + 40, 1060, X1 - X0 - 60, 380
def sc_result(img, d, t):
    t0 = S("result"); k = clamp((t - t0 - .1) / 2.2)
    d.text((X0, 300), "≈ 48 HOURS", font=F(BLK, 150), fill=SIG)
    d.line([OX, OY, OX + GW, OY], fill=INK, width=4); d.line([OX, OY, OX, OY - GH], fill=INK, width=4)
    for i, lab in enumerate(("sex", "24 h", "48 h", "72 h")):
        x = OX + GW * i / 3; d.line([x, OY, x, OY + 12], fill=INK, width=3); d.text((x, OY + 20), lab, font=F(MONO, 20), fill=MID, anchor="ma")
    d.text((OX + 10, OY - GH - 10), "sexual satisfaction", font=F(COND, 26), fill=INK, anchor="ld")
    base = OY - GH * .3
    d.line([OX, base, OX + GW, base], fill=MID, width=2)
    n = int(2 + 118 * k); pts = []
    for i in range(n):
        h = i / 119 * 72; v = .3 + .55 * math.exp(-h / 22) * (1 if h <= 60 else max(0, 1 - (h - 60) / 12))
        pts.append((OX + GW * h / 72, OY - GH * v))
    for x, y in pts[::3]: d.line([x, y, x, base], fill=mix(BG, SIG, .35), width=6)
    if len(pts) > 1: d.line(pts, fill=SIG, width=7)
    if k > .7: dim_h(d, OX, OX + GW * 2 / 3, OY - GH * .15, 1, SIG, "still elevated", 24)
    d.text((X1, 1146), "schematic", font=F(MED, 22), fill=MID, anchor="ra")

def sc_who(img, d, t):
    t0 = S("who")
    d.text((X0, 300), "FOR", font=F(BLK, 150), fill=INK); d.text((X0, 450), "EVERYONE.", font=F(BLK, 150), fill=SIG)
    specs = [(200, .95, INK, "men and"), (380, .95, SIG, "women"), (600, .75, INK, "younger"), (780, .85, SIG, "older")]
    for i, (x, s, col, w) in enumerate(specs):
        k = ease((t - cue("who", w) + .2) / .3)
        if k > 0: picto(d, x, FLOOR + (1 - k) * 40, s, col, f=1 if i % 2 == 0 else -1, pose=WAVE(t) if i == 3 else IDLE)
    fig(d, "independent of gender and age")

def sc_months(img, d, t):
    t0 = S("months"); k = clamp((t - t0 - .2) / 2.4)
    d.text((X0, 300), "MONTHS LATER", font=F(BLK, 120), fill=INK)
    d.line([OX, OY, OX + GW, OY], fill=INK, width=4); d.line([OX, OY, OX, OY - GH - 40], fill=INK, width=4)
    d.text((OX, OY + 20), "wedding", font=F(MONO, 20), fill=MID); d.text((OX + GW, OY + 20), "4–6 months", font=F(MONO, 20), fill=MID, anchor="ra")
    d.text((OX + 10, OY - GH - 50), "marital satisfaction", font=F(COND, 26), fill=INK, anchor="ld")
    x2 = OX + GW * k
    d.line([OX, OY - GH * .85, x2, OY - GH * (.85 - .12 * k)], fill=SIG, width=8)
    d.line([OX, OY - GH * .7, x2, OY - GH * (.7 - .38 * k)], fill=MID, width=8)
    if k > .95:
        d.text((x2 - 8, OY - GH * .73 - 14), "strong afterglow", font=F(BLK, 26), fill=SIG, anchor="rd")
        d.text((x2 - 8, OY - GH * .32 + 14), "weak afterglow", font=F(BLK, 26), fill=MID, anchor="ra")
    d.text((X1, 1146), "schematic", font=F(MED, 22), fill=MID, anchor="ra")

def sc_point(img, d, t):
    t0 = S("point"); tt = cue("point", "two-day"); tw = cue("point", "worth")
    words_in(d, t, [("ONE NIGHT.", t0 + .1, 300, 150, INK), ("TWO DAYS.", tt - .1, 450, 150, SIG)])
    glow(d, 480, 900, 70, ease((t - tt) / .6) * (1 + .1 * math.sin(t * 4)), t)
    pair(d)
    if t >= tw: box_label(d, 480, 640, "KEEP IT WARM", 40, WHITE, SIG, anchor="ma")
    fig(d, "fig. 2 — the glow is part of it")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "who": sc_who, "months": sc_months, "point": sc_point}
FX = [(0.0, thud(.5), 0), (.2, riser(.8, .05), 0), *EP.cut_fx(), *[(cue("study", "every single") - .8 + i * .1, tick(.035), (i % 5 - 2) / 3) for i in range(14)],
      (S("result") + .05, thud(.55), 0), (S("result") + .1, riser(2.0, .04), 0), *[(cue("who", w) - .2, pop(.14), (i - 1.5) / 2) for i, w in enumerate(("men and", "women", "younger", "older"))],
      (S("months") + .2, whoosh(.9, .06), 0), (cue("point", "two-day") - .1, thud(.45), 0), (cue("point", "worth"), pop(.15), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
