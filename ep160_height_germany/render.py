"""NOT JUST YOU – No. 160: height of German men by birth decade, 1810–1980 (time-travel line + silhouette, 25.11.2026).
Tübingen / Baten & Blum (2015) via OWID: 163.8 cm (1850) -> 180.5 cm (1980). Left: a silhouette at true scale (2.4 px/cm)
next to a ruler grows with the line; the 1850 man stays as a dashed ghost. Right: the race line.
Payoff (rule 15): ghost 1850 vs. solid 1980 with '+17 cm' stays."""
import os, sys, json
import numpy as np
from PIL import ImageDraw
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from race import Race, year_at
from stand import dashed, payoff_cam, stamp_box
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .8, "then": 1.2, "rise": 2.6, "now": .85, "why": .1}, pace="loose")
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "then", "rise", "now", "why", "end"]
EP = ThreadEpisode(TL, 160, "HOW TALL?", order=ORDER, dark=True, label="UNI TÜBINGEN · BATEN & BLUM · OWID",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("University of Tübingen, Baten & Blum (2015),", "Human Height · via Our World in Data"),
                   music=dict(bpm=94, root=7, prog="major", kick="four", audio="v5"),
                   cover=dict(words=["HOW TALL WERE", "GERMAN MEN", "200 YEARS AGO?"], kicker="Every generation since 1810."))

D = {int(k): v for k, v in json.load(open(os.path.join(HERE, "data.json"))).items()}
YS = sorted(D); VS = [D[y] for y in YS]
R = Race(YS, VS, box=(520, 820, 600, 1120), scrub_y=470, fmt="{:.1f} cm", hot_from=168, hot_to=180, marker=1850,
         events=[(1850, "LOWEST")], ticks=[1810, 1850, 1900, 1950, 1980])
KEYS = [(.2, 1810), (E("then") - .4, 1850), (E("rise") + 2.2, 1960), (E("now") + .2, 1980)]
FOOT, PXCM = 1120, 2.9

def man(d, x, h, fill=None, outline=None):
    """a simple silhouette, h = height in px, feet on FOOT"""
    y = lambda f: FOOT - h * f
    parts = [("e", x - .065 * h, y(1.0), x + .065 * h, y(.87)),
             ("r", x - .13 * h, y(.84), x + .13 * h, y(.47)),
             ("r", x - .11 * h, y(.48), x - .015 * h, y(0)), ("r", x + .015 * h, y(.48), x + .11 * h, y(0)),
             ("r", x - .18 * h, y(.83), x - .135 * h, y(.5)), ("r", x + .135 * h, y(.83), x + .18 * h, y(.5))]
    for kind, a, b, c, e in parts:
        if kind == "e": d.ellipse([a, b, c, e], fill=fill, outline=outline, width=3)
        else: d.rounded_rectangle([a, b, c, e], radius=int(.03 * h), fill=fill, outline=outline, width=3)

def ruler(d):
    x = 90
    d.line([(x, FOOT), (x, FOOT - 185 * PXCM)], fill=MID, width=2)
    for cm in range(0, 186, 5):
        y = FOOT - cm * PXCM; w = 16 if cm % 50 == 0 else 8
        d.line([(x, y), (x + w, y)], fill=MID, width=2)
        if cm in (50, 100, 150, 160, 170, 180): d.text((x - 8, y), f"{cm}", font=F(MONO, 20), fill=MID, anchor="rm")

def sc(img, d, t):
    payoff_cam(img, lambda L, dL: sc_full(L, dL, t), t, S("why"), focus=(330, 800), z1=1.1, band=(0, 520, 1080, 1180))

T_OUT = E("hook") + .2
def sc_full(img, d, t):
    yr = year_at(t, KEYS); h = float(np.interp(yr, YS, VS))
    if t < T_OUT + .5: h = 180.5 + (h - 180.5) * ease_io(clamp((t - T_OUT) / .5))          # rule 11: the 1980 man first
    d.text((540, 325), "Height of German Men", font=F(BLK, 56), fill=INK, anchor="mm")
    d.text((540, 385), "average by year of birth · 1810–1980", font=F(MONO, 24), fill=MID, anchor="mm")
    ruler(d)
    if yr >= 1850 or t < T_OUT:                                                            # the 1850 man stays (left)
        man(d, 190, 163.8 * PXCM, fill=mix(BG, MID, .45)); y0 = FOOT - 163.8 * PXCM
        dashed(d, (100, y0), (470, y0), MID, w=2); d.text((190, FOOT + 26), "1850", font=F(MONO, 22), fill=MID, anchor="mm")
    j = spring(clamp((t - .15) / .45)) if t < 1 else 1
    man(d, 360, h * PXCM * j, fill=mix(BG, R.col(h), .9))
    y = FOOT - h * PXCM; d.line([(100, y), (470, y)], fill=R.col(h), width=2)
    d.text((360, FOOT + 26), "1980" if t < T_OUT else f"{int(yr)}", font=F(MONO, 22), fill=INK, anchor="mm")
    if yr >= 1979:
        k = ease(clamp((t - KEYS[3][0] + .2) / .5)); y0 = FOOT - 163.8 * PXCM
        d.line([(290, y0), (290, y)], fill=SIG, width=4)
        d.text((200, (y0 + y) / 2), "+17 cm", font=F(BLK, 30), fill=mix(BG, SIG, k), anchor="mm")
    R.draw(img, yr)
    if 1.0 <= t < T_OUT: stamp_box(ImageDraw.Draw(img), (330, 640), "+17 CM?", t, 1.0, size=70)   # rule 11
    fig(ImageDraw.Draw(img), "men only · soldiers & conscripts · by birth decade")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.scenes = {k: sc for k in ORDER[:-1]}
FX = [(.2, whoosh(.6, .02), -.3), (KEYS[1][0], thud(.18), -.2), (KEYS[2][0] - 2.5, whoosh(.5, .02), .2), (KEYS[3][0], pop(.12), 0)]
if __name__ == "__main__": EP.run(FX)
