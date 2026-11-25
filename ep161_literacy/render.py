"""NOT JUST YOU – No. 161: world literacy, 1820–2016 (time-travel line + 100 people, 25.11.2026).
OWID (OECD 2014, UNESCO): 12.0 % (1820) -> 56 % (1950) -> 86.2 % (2016). Same build as No. 159: 100 dots above the chart,
readers light up orange. Payoff (rule 15): 86 orange dots + the curve stay."""
import os, sys, json
import numpy as np
from PIL import ImageDraw
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from race import Race, year_at
from stand import payoff_cam, stamp_box
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .8, "then": 3.0, "mid": 3.0, "now": 1.2, "why": .1}, pace="loose")
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "then", "mid", "now", "why", "end"]
EP = ThreadEpisode(TL, 161, "WHO COULD READ?", order=ORDER, dark=True, label="OECD · UNESCO · OUR WORLD IN DATA",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Our World in Data, based on OECD (2014)", "and UNESCO · adults 15+, 1820–2016"),
                   music=dict(bpm=92, root=5, prog="major", kick="four", audio="v5"),
                   cover=dict(words=["HOW MANY", "PEOPLE COULD", "READ?"], kicker="The world since 1820."))

D = {int(k): v for k, v in json.load(open(os.path.join(HERE, "data.json"))).items()}
YS = sorted(D); VS = [D[y] for y in YS]
R = Race(YS, VS, box=(150, 770, 740, 1120), scrub_y=482, fmt="{:.0f} of 100", hot_from=20, hot_to=80, zero=True,
         marker=1950, events=[(1950, "HALF")], ticks=[1820, 1870, 1920, 1970, 2016])
KEYS = [(.2, 1820), (E("then") + .1, 1830), (cue("mid", "fifty") + .1, 1950), (S("now") + .4, 2016)]

def people(d, yr, t=99):
    v = float(np.interp(yr, YS, VS)); n = int(round(v))
    if t < 1.6: n = int(12 * ease_io(clamp((t - .3) / 1.1)))                              # rule 11: 12 lights come on
    for i in range(100):
        r, c = divmod(i, 25); x = 140 + c * 33; y = 590 + r * 28
        if i < n: d.ellipse([x - 10, y - 10, x + 10, y + 10], fill=SIG)
        else: d.ellipse([x - 9, y - 9, x + 9, y + 9], outline=mix(BG, MID, .6), width=2)
    d.text((126, 566), "100 PEOPLE", font=F(MONO, 22), fill=MID, anchor="lm")
    d.text((140 + 24 * 33 + 14, 566), f"{n} CAN READ", font=F(MONO, 22), fill=SIG, anchor="rm")

def sc(img, d, t):
    payoff_cam(img, lambda L, dL: sc_full(L, dL, t), t, S("why"), focus=(700, 780), z1=1.1, band=(0, 548, 1080, 1180))

def sc_full(img, d, t):
    yr = year_at(t, KEYS)
    d.text((540, 325), "Adults Who Can Read", font=F(BLK, 56), fill=INK, anchor="mm")
    d.text((540, 380), "world · share of adults 15+ · 1820–2016", font=F(MONO, 24), fill=MID, anchor="mm")
    people(d, yr, t); R.draw(img, yr)
    if 1.7 <= t < 3.6: stamp_box(ImageDraw.Draw(img), (560, 960), "12 OF 100", t, 1.7, size=70)   # rule 11
    fig(ImageDraw.Draw(img), "historical values: estimates · definitions vary")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.scenes = {k: sc for k in ORDER[:-1]}
FX = [(.2, whoosh(.6, .02), -.3), (KEYS[2][0], pop(.1), .2), (KEYS[3][0], pop(.12), 0)]
if __name__ == "__main__": EP.run(FX)
