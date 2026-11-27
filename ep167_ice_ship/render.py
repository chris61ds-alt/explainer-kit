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
import cute; cute.LOUD = -14
from board import Board, BoardInsert, VideoInsert, desk, fit, check_frame, insert_fx, title_card
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"cold": .2, "stakes": .85, "back": .25, "detail": .3, "but": .3, "so": .3, "turn": .3, "today": .85, "why": .25},
              pace="loose")
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["cold", "stakes", "back", "detail", "but", "so", "turn", "today", "why", "end"]
EP = DokuEpisode(TL, 167, "ICE FOR INDIA", order=ORDER, img_dir=os.path.join(HERE, "img"), credits=os.path.join(HERE, "img", "credits.json"),
                 sources=("American Heritage, Cold Mine ·", "Atlas Obscura"),
                 music=dict(bpm=66, root=2, prog="minor", audio="doku"),
                 cover=dict(words=["WHY DID A SHIP", "CARRY ICE", "TO INDIA?"], kicker="It's 1833."))

SHIP = "EAST INDIAMAN ASIA · WILLIAM JOHN HUGGINS · PUBLIC DOMAIN"
HARV = "MINNESOTA ICE HARVEST · WHITNEY & ZIMMERMAN · PUBLIC DOMAIN"
EP.shots = [
    Shot("cold", "ship", (.50, .45, 1.5), (.53, .42, 1.85), start=0, tag="", grade=(.82, .3, 0), credit=SHIP),
    Shot("cold", "ship", (.50, .45, 1.3), (.53, .42, 1.6), start=cue("cold", "cargo") - .2, tag="BOSTON · 1833", grade=(.82, .3, 0), credit=SHIP),
    Shot("stakes", "ship", (.30, .55, 1.3), (.70, .55, 1.4), tag="4 MONTHS AT SEA", grade=(.8, .3, 0), credit=SHIP),
    Shot("back", "harvest3", (.72, .45, 1.35), (.80, .45, 1.4), tag="FREDERIC TUDOR · BOSTON", grade=(1.0, .05, .3)),
    Shot("detail", "harvest", (.18, .45, 1.35), (.28, .45, 1.4), tag="FROZEN LAKES · SAWDUST", grade=(1.0, .05, .3), credit=HARV),
    Shot("but", "fort", (.40, .55, 1.0), (.55, .55, 1.08), tag="CALCUTTA · 1833", grade=(1.0, .3, 0)),
    Shot("so", "chowringhee", (.30, .5, 1.0), (.60, .5, 1.05), tag="ICE-COLD DRINKS", grade=(1.0, .3, 0)),
    Shot("so", "esplanade", (.40, .5, 1.0), (.55, .5, 1.08), start=cue("so", "Tudor") - .2, tag="THE ICE KING", grade=(1.0, .3, 0)),
    Shot("turn", "harvest3", (.30, .55, 1.6), (.36, .55, 1.75), tag="ICE HOUSES · ICE FACTORIES", grade=(1.0, .05, .3)),
    Shot("turn", "freezer", (.5, .5, 1.0), (.5, .55, 1.12), start=cue("turn", "fridge") - .25, tag="THE FRIDGE", grade=(1.05, 0, 0)),
    Shot("today", "freezer", (.5, .55, 1.12), (.5, .60, 1.35), tag="TODAY", grade=(1.1, 0, 0)),
    Shot("why", "ship", (.52, .43, 1.6), (.52, .43, 1.6), tag="1833 VS. TODAY", grade=(1.05, .25, 0), credit=SHIP),
]
for s_ in EP.shots:                                            # keep the old per-shot credits where they were set
    if s_.img == "freezer" and s_.beat == "today": s_.credit = None

# ---- cut-aways -------------------------------------------------------------------------------------------------
T_D0, T_D1 = cue("detail", "Packed") - .1, E("detail") + .15           # ice-harvest photo + typed card on a desk
DK = Board(os.path.join(HERE, "img"), bg=desk(3600, 6000), size=(3600, 6000))
DK.photo("harv", "harvest", 1800, 2700, 1500, -1, tilt=1.5, sepia=.3)
DK.card("pack", ["THE ICE TRICK", "CUT FROM FROZEN LAKES", "PACKED IN SAWDUST", "STACKED TIGHT · MELTS SLOWLY"], 1550, 3330, 1050,
        -1, tilt=-2, marks=[(2, "SAWDUST", .05, .5, "underline"), (3, "MELTS SLOWLY", cue("detail", "melt") - T_D0, cue("detail", "melt") - T_D0 + .5, "circle")], size=56)
for it in DK.items.values(): it.pin = False
DK.cam = [fit(DK, ["harv", "pack"], 0, pad=90), fit(DK, ["harv", "pack"], T_D1 - T_D0, pad=20)]
for tt in (0, T_D1 - T_D0): assert not check_frame(DK, tt, ["harv", "pack"]), "desk items not fully visible"
EP.inserts = [
    (0.0, cue("cold", "cargo") - .25, VideoInsert(os.path.join(HERE, "vid", "coptic.mp4"), 9, 5, os.path.join(HERE, "vid", "cache", "cop"), sepia=.4,
     crop="464:352:8:4"), None, "S.S. COPTIC SAILING AWAY · EDISON, 1897 · PUBLIC DOMAIN"),
    (T_D0, T_D1, BoardInsert(DK), "HOW TO SHIP ICE", HARV),
]
EP.accent = {"cold": ["one hundred eighty tons"], "stakes": ["Four months"], "back": ["slippery speculation"], "detail": ["sawdust"],
             "but": ["still frozen"], "so": ["Ice King"], "turn": ["fridge"], "today": ["few hours"], "why": ["open the door"]}
EP.payoff = (S("why") + .1, 1.22)

tons = lambda v: f"{v:,.0f} t"
T_C0 = cue("cold", "Its") - .1
M = Meter([dict(t=T_C0, to=180, dur=cue("cold", "tons") + .2 - T_C0, label="ICE ON BOARD", unit="TONS", fmt=tons, stamp="4 MONTHS AT SEA"),
           dict(t=cue("but", "hundred") - .9, to=100, dur=1.1, label="CALCUTTA · STILL FROZEN", unit="TONS", fmt=tons),
           dict(t=cue("today", "few") - .2, to=0, dur=.01, tween=False, label="TODAY · YOUR FREEZER", unit="HOURS", fmt=lambda v: "A FEW",
                gold=True)],
          t_hide=S("why") - .05)
EP.counter_list = [(T_C0, cue("cold", "tons") + .2 - T_C0, 180), (cue("but", "hundred") - .9, 1.1, 100)]

def overlay(img, d, t):
    if t < 3.0: title_card(img, t, .25, 2.9, "ICE FOR INDIA", "BOSTON · 1833 · (FILM: 1897, ILLUSTRATIVE)", 250)
    if not (S("back") - .1 <= t < S("but") - .1 or S("so") - .1 <= t < S("today") - .1): M.draw(img, d, t)   # free for card and desk
    paper_card(img, t, cue("back", "Boston") - .2, E("back") + .2, "BOSTON GAZETTE · 1806",
               "No joke. A vessel with a cargo of ice has cleared out for Martinique. We hope this will not prove to be a slippery speculation.",
               "slippery speculation", (cue("back", "slippery") - .1, cue("back", "slippery") + .5), foot="ON TUDOR'S FIRST ICE SHIPMENT", y=360)
    compare(img, d, t, S("why") - .05, (("1833 · BY SHIP", "4 MONTHS", WHITE), ("YOU · TODAY", "A FEW HOURS", GOLD)))
EP.overlay = overlay

FX = [(cue("back", "laughed") - .05, tick(.01), .2), (cue("detail", "frozen") - .05, tick(.01), -.2), (cue("so", "Ice King") - .1, thud(.2), 0),
      (cue("why", "open") - .05, pop(.08), .2), (T_C0, tick(.012), -.3), (cue("cold", "tons") + .25, thud(.25), 0),
      (cue("but", "frozen"), thud(.22), 0), (cue("today", "few") - .2, pop(.12), .2),
      (S("why") - .05, boom(.35), 0)] + EP.cut_fx(.06) + EP.shot_fx(whoosh(.25, .015))
if __name__ == "__main__": EP.run(FX)
