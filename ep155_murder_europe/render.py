"""NOT JUST YOU – No. 155: murder rates in Europe, 1300–2016 (time-travel line, shared/race.py, 25.11.2026).
Eisner (2003) period estimates (plotted at midpoints) + IHME from 1990, via Our World in Data (data.json).
Main line Italy (56 -> peak 73 in 1450 -> 0.9), thin lines Germany & Switzerland and England. Orange = high, blue = low.
Mostly music; voice at the start, the high point, the fall, today, the punchline. Payoff (rule 15): all lines at 2016 stay."""
import os, sys, json
from PIL import ImageDraw
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from race import Race, year_at
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": 1.2, "then": 3.0, "fall": 3.0, "now": 1.2, "why": .1}, pace="loose")
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "then", "fall", "now", "why", "end"]
EP = ThreadEpisode(TL, 155, "MURDER RATES", order=ORDER, dark=True, label="EISNER 2003 · IHME · OWID",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Eisner (2003), Long-Term Historical Trends in", "Violent Crime · IHME · via Our World in Data"),
                   music=dict(bpm=90, root=9, prog="minor", kick="four", audio="v5"),
                   cover=dict(words=["HOW VIOLENT", "WAS MEDIEVAL", "EUROPE?"], kicker="700 years of murder rates."))

D = {k: {int(y): v for y, v in d.items()} for k, d in json.load(open(os.path.join(HERE, "data.json"))).items()}
def ser(k): ys = sorted(D[k]); return ys, [D[k][y] for y in ys]
IY, IV = ser("Italy")
R = Race(IY, IV, box=(150, 760, 660, 1120), scrub_y=530, fmt="{:.1f}", hot_from=3, hot_to=30, marker=1450, log=True, name="ITALY",
         others=[("GER/CH", *ser("Germany and Switzerland")), ("ENGLAND", *ser("England"))],
         events=[(1450, "PEAK"), (1990, "TODAY'S DATA")], ticks=[1300, 1500, 1700, 1900, 2016])
KEYS = [(.2, 1300), (E("then") + .4, 1460), (E("fall") + 2.6, 1900), (E("now") + .6, 2016)]

def sc(img, d, t):
    yr = year_at(t, KEYS)
    d.text((540, 330), "Murders per 100,000 People", font=F(BLK, 54), fill=INK, anchor="mm")
    d.text((540, 395), "per year · Europe · 1300–2016", font=F(MONO, 28), fill=MID, anchor="mm")
    R.draw(img, yr)
    fig(ImageDraw.Draw(img), "log scale · historic values: estimates from court & coroner records")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.scenes = {k: sc for k in ORDER[:-1]}
FX = [(.2, whoosh(.6, .02), -.3), (KEYS[1][0], thud(.18), 0), (KEYS[2][0], whoosh(.5, .02), .2), (KEYS[3][0], pop(.1), .3)]
if __name__ == "__main__": EP.run(FX)
