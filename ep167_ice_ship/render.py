"""NOT JUST YOU – No. 167 (DOKU, 26.11.2026): ice for India. 12 May 1833 the Tuscany left Boston with ~180 tons of lake ice
packed in sawdust; early September 1833 it reached Calcutta after ~4 months with ~100 tons still frozen (Frederic Tudor,
'the Ice King' – American Heritage 'Cold Mine'; Atlas Obscura; Scroll.in). Gold element (rule 12, doku): the ice
counter 0 → 180 t → 100 t (melting) → A FEW HOURS. First 3 s (Chris OK 26.11.): an 1830s East Indiaman under sail,
camera on the ship from frame 0, tag BOSTON · 1833, counter ICE ON BOARD 0 → 180 t."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from doku import *
from swiss import pop, tick, thud, whoosh, boom
from cute import Timeline
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"cold": .35, "stakes": .85, "back": .4, "but": .6, "so": .4, "turn": .5, "today": .85, "why": .2}, pace="loose")
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["cold", "stakes", "back", "but", "so", "turn", "today", "why", "end"]
EP = DokuEpisode(TL, 167, "ICE FOR INDIA", order=ORDER, img_dir=os.path.join(HERE, "img"), credits=os.path.join(HERE, "img", "credits.json"),
                 sources=("American Heritage, Cold Mine ·", "Atlas Obscura"),
                 music=dict(bpm=78, root=2, prog="minor", kick="half", audio="v5"),
                 cover=dict(words=["WHY DID A SHIP", "CARRY ICE", "TO INDIA?"], kicker="It's 1833."))

SHIP = "EAST INDIAMAN ASIA · WILLIAM JOHN HUGGINS · PUBLIC DOMAIN"
HARV = "MINNESOTA ICE HARVEST · WHITNEY & ZIMMERMAN · PUBLIC DOMAIN"
EP.shots = [
    Shot("cold", "ship", (.50, .45, 1.5), (.53, .42, 1.85), start=0, tag="BOSTON · 1833", grade=(.82, .3, 0), credit=SHIP),
    Shot("stakes", "ship", (.30, .55, 1.3), (.70, .55, 1.4), tag="4 MONTHS AT SEA", grade=(.8, .3, 0), credit=SHIP),
    Shot("back", "harvest", (.18, .45, 1.35), (.28, .45, 1.4), tag="FROZEN LAKES · SAWDUST", grade=(1.0, .05, .3), credit=HARV),
    Shot("but", "fort", (.40, .55, 1.0), (.55, .55, 1.08), tag="CALCUTTA · 1833", grade=(1.0, .3, 0),
         credit="FORT WILLIAM, CALCUTTA · WILLIAM WOOD · 1828 · PUBLIC DOMAIN"),
    Shot("so", "chowringhee", (.30, .5, 1.0), (.60, .5, 1.05), tag="ICE-COLD DRINKS", grade=(1.0, .3, 0),
         credit="VIEW OF PART OF CHOWRINGHEE, CALCUTTA · CHARLES D'OYLY · YALE CENTER FOR BRITISH ART · CC0"),
    Shot("turn", "harvest3", (.72, .45, 1.35), (.80, .45, 1.4), tag="ICE HOUSES · ICE SHIPS", grade=(1.0, .05, .3),
         credit="MINNESOTA ICE HARVEST · WHITNEY & ZIMMERMAN · PUBLIC DOMAIN"),
    Shot("turn", "freezer", (.5, .5, 1.0), (.5, .55, 1.12), start=cue("turn", "fridge") - .25, tag="THE FRIDGE", grade=(1.05, 0, 0),
         credit="TRAY OF ICE CUBES IN A FREEZER · PHILSACOR · CC0"),
    Shot("today", "freezer", (.5, .55, 1.12), (.5, .60, 1.35), tag="TODAY", grade=(1.1, 0, 0), credit="TRAY OF ICE CUBES IN A FREEZER · PHILSACOR · CC0"),
    Shot("why", "ship", (.52, .43, 1.6), (.52, .43, 1.6), tag="1833 VS. TODAY", grade=(1.05, .25, 0), credit=SHIP),
]
EP.accent = {"cold": ["one hundred eighty tons"], "stakes": ["four months"], "back": ["sawdust"], "but": ["hundred tons frozen"],
             "so": ["ice-cold"], "turn": ["fridge"], "today": ["few hours"], "why": ["one hundred eighty tons cold drink"]}
EP.payoff = (S("why") + .1, 1.22)

tons = lambda v: f"{v:,.0f} t"
T_C0 = 1.4
M = Meter([dict(t=T_C0, to=180, dur=cue("cold", "tons") + .2 - T_C0, label="ICE ON BOARD", unit="TONS", fmt=tons, stamp="4 MONTHS AT SEA"),
           dict(t=cue("but", "hundred") - .9, to=100, dur=1.1, label="CALCUTTA · STILL FROZEN", unit="TONS", fmt=tons),
           dict(t=cue("today", "few") - .2, to=0, dur=.01, tween=False, label="TODAY · YOUR FREEZER", unit="HOURS", fmt=lambda v: "A FEW",
                gold=True)],
          t_hide=S("why") - .05)
EP.counter_list = [(T_C0, cue("cold", "tons") + .2 - T_C0, 180), (cue("but", "hundred") - .9, 1.1, 100)]

def overlay(img, d, t):
    M.draw(img, d, t)
    compare(img, d, t, S("why") - .05, (("1833 · BY SHIP", "4 MONTHS", WHITE), ("YOU · TODAY", "A FEW HOURS", GOLD)))
EP.overlay = overlay

FX = [(0.0, whoosh(.6, .02), -.2), (T_C0, tick(.012), -.3), (cue("cold", "tons") + .25, thud(.25), 0),
      (cue("but", "frozen"), thud(.22), 0), (cue("today", "few") - .2, pop(.12), .2),
      (S("why") - .05, boom(.35), 0)] + EP.cut_fx(.06) + EP.shot_fx(whoosh(.25, .015))
if __name__ == "__main__": EP.run(FX)
