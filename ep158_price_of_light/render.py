"""NOT JUST YOU – No. 158: the price of light in England, 1301–2006 (time-travel line, shared/race.py, log scale, 25.11.2026).
Fouquet & Pearson (2006/2012) via Our World in Data: constant 2000 £ per million lumen-hours, 33,043 -> 2.89 (~11,400x).
Annual data, jagged; orange = expensive, blue = cheap; events: gas lamps ~1815, kerosene ~1860, light bulb ~1880.
Mostly music, voice at start / 1300 / flat centuries / the drop / punchline. Payoff (rule 15): full curve to 2006 stays."""
import os, sys, json
from PIL import ImageDraw
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from race import Race, year_at
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": 1.0, "then": 2.2, "flat": 2.4, "drop": 2.6, "why": .1}, pace="loose")
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "then", "flat", "drop", "why", "end"]
EP = ThreadEpisode(TL, 158, "THE PRICE OF LIGHT", order=ORDER, dark=True, label="FOUQUET & PEARSON · OWID",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Fouquet & Pearson (2006), Seven Centuries of", "Energy Services · via Our World in Data"),
                   music=dict(bpm=90, root=4, prog="major", kick="four", audio="v5"),
                   cover=dict(words=["HOW EXPENSIVE", "WAS LIGHT?", "700 YEARS."], kicker="Prices in England."))

D = {int(k): v for k, v in json.load(open(os.path.join(HERE, "data.json"))).items()}
YS = sorted(D)
def money(v): return f"£{v:,.0f}" if v >= 100 else f"£{v:.2f}"
R = Race(YS, [D[y] for y in YS], box=(170, 760, 660, 1120), scrub_y=530, fmt=money, hot_from=100, hot_to=12000, marker=1815, log=True,
         events=[(1815, "GAS"), (1860, "KEROSENE"), (1882, "BULB")], ticks=[1301, 1500, 1700, 1900, 2006])
KEYS = [(.2, 1301), (E("then") + .3, 1450), (E("flat") + 1.6, 1800), (E("drop") + 2.2, 2006)]

def sc(img, d, t):
    yr = year_at(t, KEYS)
    d.text((540, 330), "The Price of Light in England", font=F(BLK, 54), fill=INK, anchor="mm")
    d.text((540, 395), "£ per million lumen-hours · 2000 prices", font=F(MONO, 28), fill=MID, anchor="mm")
    R.draw(img, yr)
    fig(ImageDraw.Draw(img), "log scale · 1 million lumen-hours ≈ one bright bulb for 1,250 h")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.scenes = {k: sc for k in ORDER[:-1]}
TG = lambda y: KEYS[2][0] + (y - 1800) / (2006 - 1800) * (KEYS[3][0] - KEYS[2][0])
FX = [(.2, whoosh(.6, .02), -.3), (KEYS[2][0], whoosh(.5, .02), .2), (TG(1815), pop(.08), -.2), (TG(1860), pop(.08), 0), (TG(1882), thud(.18), .3)]
if __name__ == "__main__": EP.run(FX)
