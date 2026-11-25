"""NOT JUST YOU – No. 154: life expectancy in England, 475 years (first episode with shared/race.py, the 'time-travel line',
after Chris' deardata1 reference, 25.11.2026). Dark look, mostly music: voice only at the start (question), in the middle
and the punchline; the line runs through the years with a scrubber, events (1558 flu, 1665 plague, 1918 flu) stay as
thin marks, the line turns orange above ~60. Data: Gapminder/UN/IHME via Our World in Data (data.json, UK; early = England).
Payoff (rule 15): the full curve to 2016 with 80.9 stays."""
import os, sys, json
from PIL import ImageDraw
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from race import Race, year_at
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": 7.5, "flat": 2.6, "rise": 1.6, "why": .1}, pace="loose")   # music-only stretches
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "flat", "rise", "why", "end"]
EP = ThreadEpisode(TL, 154, "LIFE EXPECTANCY", order=ORDER, dark=True, label="GAPMINDER · UN · IHME · OWID",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Gapminder, UN, IHME via Our World in Data ·", "life expectancy at birth, UK (early: England)"),
                   music=dict(bpm=92, root=5, prog="major", kick="four", audio="v5"),
                   cover=dict(words=["HOW LONG DID", "PEOPLE LIVE?", "475 YEARS."], kicker="Life expectancy in England."))

D = {int(k): v for k, v in json.load(open(os.path.join(HERE, "data.json"))).items()}
YS = sorted(D); VS = [D[y] for y in YS]
R = Race(YS, VS, box=(150, 790, 660, 1120), scrub_y=530, fmt="{:.1f}", unit=" yrs", hot_from=50, hot_to=75, marker=1870,
         events=[(1558, "FLU"), (1665, "PLAGUE"), (1918, "1918 FLU")], ticks=[1541, 1700, 1850, 2016])
KEYS = [(.2, 1541), (S("flat") + .2, 1800), (E("flat") + 1.4, 1870), (E("rise") + 1.2, 2016)]

def sc(img, d, t):
    yr = year_at(t, KEYS)
    d.text((540, 330), "Life Expectancy in England", font=F(BLK, 56), fill=INK, anchor="mm")
    d.text((540, 395), "at birth · 1541–2016", font=F(MONO, 28), fill=MID, anchor="mm")
    R.draw(img, yr)
    fig(ImageDraw.Draw(img), "low values: mostly child deaths · early years: England")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.scenes = {k: sc for k in ORDER[:-1]}
T1558 = KEYS[0][0] + (1558 - 1541) / (1800 - 1541) * (KEYS[1][0] - KEYS[0][0])
T1665 = KEYS[0][0] + (1665 - 1541) / (1800 - 1541) * (KEYS[1][0] - KEYS[0][0])
T1918 = KEYS[2][0] + (1918 - 1870) / (2016 - 1870) * (KEYS[3][0] - KEYS[2][0])
FX = [(.2, whoosh(.6, .02), -.3), (T1558, thud(.18), -.4), (T1665, thud(.18), 0), (KEYS[2][0], whoosh(.5, .02), .2), (T1918, thud(.18), .3)]
if __name__ == "__main__": EP.run(FX)
