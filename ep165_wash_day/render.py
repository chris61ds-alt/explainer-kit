"""NOT JUST YOU – No. 165 (DOKU, 26.11.2026): wash day. Monday 1900, Anna (illustrative) does the laundry, the whole day.
One load ≈ 50 gallons of water carried by hand; in a year a housewife carried 36 tons of water (Strasser 1982 via Digital
History, UH). Disputed total-housework hours (Lebergott vs. Ramey) deliberately not used. Gold element (rule 12, doku):
the water counter 0 → 50 gallons → 36 tons a year → 1 button. First 3 s (Chris OK 26.11.): Degas' laundress, camera on
the hands from frame 0, tag MONDAY · 1900, counter ONE LOAD OF LAUNDRY 0 → 50 gallons."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from doku import *
from swiss import pop, tick, thud, whoosh, boom
from cute import Timeline
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"cold": .35, "stakes": .85, "back": .4, "but": .6, "so": .4, "turn": .5, "today": .85, "why": .2}, pace="loose")
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["cold", "stakes", "back", "but", "so", "turn", "today", "why", "end"]
EP = DokuEpisode(TL, 165, "WASH DAY", order=ORDER, img_dir=os.path.join(HERE, "img"), credits=os.path.join(HERE, "img", "credits.json"),
                 sources=("Strasser (1982), Never Done ·", "via Digital History, Univ. of Houston"),
                 music=dict(bpm=80, root=7, prog="minor", kick="half", audio="v5"),
                 cover=dict(words=["ONE LOAD OF", "LAUNDRY TOOK", "HOW LONG?"], kicker="Monday, 1900."))

EP.shots = [
    Shot("cold", "degas", (.45, .62, 1.7), (.43, .58, 2.2), start=0, tag="MONDAY · 1900", grade=(.95, .25, 0),
         credit="THE LAUNDRESS · EDGAR DEGAS · 1873 · PUBLIC DOMAIN"),
    Shot("cold", "degas", (.42, .26, 1.9), (.42, .24, 2.3), start=cue("cold", "whole") - .2, tag="MONDAY · 1900", grade=(.95, .25, 0),
         credit="THE LAUNDRESS · EDGAR DEGAS · 1873 · PUBLIC DOMAIN"),
    Shot("stakes", "veranda", (.5, .55, 1.0), (.5, .58, 1.12), tag="QUEENSLAND · c. 1903", grade=(.95, .2, .3),
         credit="WOMAN HANDWASHING CLOTHES · STATE LIBRARY OF QUEENSLAND · PUBLIC DOMAIN"),
    Shot("back", "soapad", (.20, .55, 1.0), (.30, .55, 1.08), tag="SCRUB · BOIL · WRING", grade=(.9, .2, 0),
         credit="QUEEN OF THE LAUNDRY · SOAP ADVERT · c. 1880 · PUBLIC DOMAIN"),
    Shot("but", "millet", (.45, .5, 1.0), (.50, .48, 1.15), tag="CARRY · CARRY · CARRY", grade=(1.0, .25, 0),
         credit="WASHERWOMEN · JEAN-FRANÇOIS MILLET · 1855 · PUBLIC DOMAIN"),
    Shot("so", "degas2", (.35, .55, 1.4), (.35, .50, 1.6), tag="EVERY MONDAY", grade=(.95, .25, 0),
         credit="LAUNDRESS · EDGAR DEGAS · 1873 · NORTON SIMON MUSEUM · PUBLIC DOMAIN"),
    Shot("turn", "washer1920", (.30, .45, 1.0), (.33, .42, 1.15), tag="1920 · ELECTRIC WASHER", grade=(1.05, .1, .3),
         credit="1920 ELECTRIC WASHER AD · SEATTLE ELECTRIC WASHER CO. · PUBLIC DOMAIN"),
    Shot("today", "modern", (.5, .55, 1.0), (.5, .60, 1.25), tag="TODAY", grade=(1.1, .05, 0),
         credit="COIN-OP WASHING MACHINE · BARON MADDOCK · CC BY 4.0"),
    Shot("why", "degas", (.43, .45, 1.3), (.43, .45, 1.3), tag="1900 VS. TODAY", grade=(1.05, .25, 0),
         credit="THE LAUNDRESS · EDGAR DEGAS · 1873 · PUBLIC DOMAIN"),
]
EP.accent = {"cold": ["whole day"], "stakes": ["fifty gallons"], "back": ["boiled"], "but": ["thirty-six tons"],
             "so": ["every week"], "turn": ["washing machine"], "today": ["one button"], "why": ["whole day one button"]}
EP.payoff = (S("why") + .1, 1.22)

num = lambda v: f"{v:,.0f}"
T_C0 = 1.4
M = Meter([dict(t=T_C0, to=50, dur=cue("stakes", "gallons") + .2 - T_C0, label="ONE LOAD OF LAUNDRY", unit="GALLONS OF WATER", fmt=num,
                stamp="≈ 190 LITRES"),
           dict(t=cue("but", "thirty") - .2, to=36, dur=.01, tween=False, label="IN ONE YEAR", unit="TONS OF WATER, CARRIED", fmt=num),
           dict(t=cue("today", "button") - .2, to=1, dur=.01, tween=False, label="TODAY", unit="BUTTON", fmt=num, gold=True)],
          t_hide=S("why") - .05)
EP.counter_list = M.counters()

def overlay(img, d, t):
    M.draw(img, d, t)
    compare(img, d, t, S("why") - .05, (("ANNA · 1900", "1 DAY", WHITE), ("YOU · TODAY", "1 BUTTON", GOLD)))
EP.overlay = overlay

FX = [(0.0, whoosh(.6, .02), -.2), (T_C0, tick(.012), -.3), (cue("stakes", "gallons") + .25, thud(.25), 0),
      (cue("but", "thirty") - .2, thud(.3), 0), (cue("today", "button") - .2, pop(.12), .2),
      (S("why") - .05, boom(.35), 0)] + EP.cut_fx(.06) + EP.shot_fx(whoosh(.25, .015))
if __name__ == "__main__": EP.run(FX)
