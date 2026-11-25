"""NOT JUST YOU – No. 159: child mortality, world, 1800–2017 (time-travel line + 100 children, 25.11.2026).
Gapminder + World Bank (2019) via OWID: 43.3 % (1800) -> 36.2 % (1900) -> 3.9 % (2017). Callback to No. 154.
Above the chart: 100 children as dots; the share that dies before 5 is shown as dark hollow dots, the rest light up orange
as the line falls. Payoff (rule 15): 96 orange dots + the full curve stay."""
import os, sys, json
from PIL import ImageDraw
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from race import Race, year_at
from stand import payoff_cam, stamp_box
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .8, "then": 1.6, "flat": 1.0, "drop": 2.4, "now": .85, "why": .1}, pace="loose")
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "then", "flat", "drop", "now", "why", "end"]
EP = ThreadEpisode(TL, 159, "CHILD MORTALITY", order=ORDER, dark=True, label="GAPMINDER · WORLD BANK · OWID",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Gapminder and World Bank (2019),", "via Our World in Data · world, 1800–2017"),
                   music=dict(bpm=88, root=2, prog="major", kick="four", audio="v5"),
                   cover=dict(words=["HOW MANY", "CHILDREN DIED", "BEFORE AGE 5?"], kicker="The world since 1800."))

D = {int(k): v for k, v in json.load(open(os.path.join(HERE, "data.json"))).items()}
YS = sorted(D)
R = Race(YS, [D[y] for y in YS], box=(150, 770, 740, 1120), scrub_y=482, fmt="{:.0f} of 100", hot_from=30, hot_to=5, zero=True,
         marker=1940, events=[(1928, "PENICILLIN"), (1974, "VACCINE PROGRAMME")], ticks=[1800, 1850, 1900, 1950, 2017])
KEYS = [(.2, 1800), (E("then") + .2, 1850), (E("flat") + .4, 1910), (E("drop") + 1.6, 1990), (E("now") + .4, 2017)]

def kids(d, yr, t=99):
    v = float(__import__("numpy").interp(yr, YS, [D[y] for y in YS])); dead = int(round(v))
    if t < 1.9: dead = int(43 * ease_io(clamp((t - .5) / 1.3)))                          # rule 11: 43 lights go out
    for i in range(100):
        r, c = divmod(i, 25); x = 140 + c * 33; y = 590 + r * 28
        if i < dead: d.ellipse([x - 9, y - 9, x + 9, y + 9], outline=mix(BG, MID, .6), width=2)
        else: d.ellipse([x - 10, y - 10, x + 10, y + 10], fill=SIG)
    d.text((140 - 14, 566), "100 CHILDREN", font=F(MONO, 22), fill=MID, anchor="lm")
    d.text((140 + 24 * 33 + 14, 566), f"{dead} DIE BEFORE 5", font=F(MONO, 22), fill=MID, anchor="rm")

def sc(img, d, t):
    payoff_cam(img, lambda L, dL: sc_full(L, dL, t), t, S("why"), focus=(700, 1000), z1=1.1, band=(0, 548, 1080, 1180))

def sc_full(img, d, t):
    yr = year_at(t, KEYS)
    d.text((540, 325), "Children Dying Before Age 5", font=F(BLK, 54), fill=INK, anchor="mm")
    d.text((540, 380), "world · share of all children · 1800–2017", font=F(MONO, 24), fill=MID, anchor="mm")
    kids(d, yr, t); R.draw(img, yr)
    if 1.9 <= t < 3.6: stamp_box(ImageDraw.Draw(img), (560, 960), "43 OF 100", t, 1.9, size=70)   # rule 11
    fig(ImageDraw.Draw(img), "before 1950: estimates · today ≈ 4 of 100")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.scenes = {k: sc for k in ORDER[:-1]}
FX = [(.2, whoosh(.6, .02), -.3), (KEYS[2][0], whoosh(.5, .02), .2), (KEYS[3][0], pop(.1), .3), (KEYS[4][0], pop(.1), 0)]
if __name__ == "__main__": EP.run(FX)
