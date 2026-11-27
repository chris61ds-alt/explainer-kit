"""NOT JUST YOU – No. 170 (MYSTERY, 26.11.2026): the diary of Merer. 2013: Pierre Tallet's team finds the oldest inscribed
papyri of Egypt at Wadi al-Jarf on the Red Sea – the logbook of inspector Merer, whose ~40 boatmen shipped white Tura
limestone to Giza, ~200 blocks a month, most likely for the Great Pyramid's casing (Tallet 2017; Tallet & Marouard 2014).
Mystery format (REGELN.md): cold opens ONE loop (whose diary?), back names the alien claim only as a claim, why closes
the loop. Gold element (rule 12): the counter THIS DIARY IS 0 → 4,500 YEARS OLD → 200 BLOCKS A MONTH → 4,500+.
First 3 s: hieratic papyrus (illustrative), camera pushes in from frame 0, tag RED SEA · 2013, counter 0 → 4,500 years."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from doku import *
from swiss import pop, tick, thud, whoosh, boom
from cute import Timeline
import cute; cute.LOUD = -14
from board import Board, BoardInsert, desk, fit, check_frame, insert_fx, title_card
from maps import MapInsert, CREDIT as MAPCREDIT
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"cold": .2, "stakes": .85, "back": .3, "detail": .3, "but": .3, "so": .3, "turn": .3, "today": .85, "why": .25},
              pace="loose")
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["cold", "stakes", "back", "detail", "but", "so", "turn", "today", "why", "end"]
EP = DokuEpisode(TL, 170, "MERER'S DIARY", order=ORDER, img_dir=os.path.join(HERE, "img"), credits=os.path.join(HERE, "img", "credits.json"),
                 sources=("Tallet (2017), Les papyrus de la Mer Rouge I ·", "Tallet & Marouard (2014)"),
                 music=dict(bpm=64, root=3, prog="minor", audio="doku"),
                 cover=dict(words=["WHO REALLY BUILT", "THE GREAT", "PYRAMID?"], kicker="Found in 2013."))

PAP = "ILLUSTRATIVE: LETTER IN HIERATIC SCRIPT · THE MET · CC0"
EP.shots = [
    Shot("cold", "papyrus", (.47, .45, 3.8), (.50, .45, 4.4), start=0, tag="", grade=(.85, .3, 0), credit=PAP),
    Shot("stakes", "haghe", (.62, .45, 1.15), (.62, .42, 1.35), tag="GIZA · c. 2560 BC", grade=(.95, .3, 0),
         credit="PYRAMIDS AT GÎZA · LOUIS HAGHE after DAVID ROBERTS · WELLCOME COLLECTION · CC BY 4.0"),
    Shot("back", "bonfils", (.25, .45, 1.2), (.32, .42, 1.35), tag="HOW?", grade=(.9, .25, .4),
         credit="CAIRE. ALLÉE DE PYRAMIDES · FÉLIX BONFILS · THE MET · CC0"),
    Shot("back", "rijks", (.55, .30, 1.4), (.55, .26, 1.8), start=cue("back", "aliens") - .25, tag="THE ALIEN THEORY", grade=(.6, 0, .6), ghost=1.2,
         credit="PYRAMID OF CHEOPS, GIZEH · RIJKSMUSEUM · CC0"),
    Shot("detail", "scribe", (.5, .45, 1.1), (.5, .42, 1.3), tag="MERER · INSPECTOR · 40 BOATMEN", grade=(1.0, .25, 0),
         credit="ILLUSTRATIVE: STATUE OF A SCRIBE · MUSEO EGIZIO, TURIN · CC0"),
    Shot("so", "boat", (.35, .5, 1.2), (.55, .48, 1.3), tag="30 BLOCKS PER TRIP", grade=(1.0, .25, 0),
         credit="MODEL PADDLING BOAT · TOMB OF MEKETRE · THE MET · CC0"),
    Shot("so", "boat2", (.40, .5, 1.1), (.60, .5, 1.15), start=cue("so", "two") - .2, tag="200 BLOCKS A MONTH", grade=(.95, .2, .3),
         credit="MODEL BOAT · THE MET · CC0"),
    Shot("turn", "casing", (.45, .45, 1.1), (.50, .42, 1.3), tag="TURA LIMESTONE · CASING", grade=(1.0, .25, 0),
         credit="CASING STONE OF THE GREAT PYRAMID · BRITISH MUSEUM · CAPTMONDO · CC BY 2.5"),
    Shot("today", "papyrus", (.50, .45, 3.6), (.52, .45, 4.0), tag="OLDEST PAPYRUS IN EGYPT", grade=(1.05, .3, 0), credit=PAP),
    Shot("why", "rijks", (.55, .35, 1.25), (.55, .35, 1.25), tag="NO ALIENS", grade=(1.05, .2, .3),
         credit="PYRAMID OF CHEOPS, GIZEH · RIJKSMUSEUM · CC0"),
]
EP.accent = {"cold": ["Papyrus"], "stakes": ["diary", "Great Pyramid"], "back": ["aliens"], "detail": ["forty boatmen"],
             "but": ["no mystery"], "so": ["two hundred blocks"], "turn": ["white limestone"], "today": ["oldest"], "why": ["forty men"]}

# ---- cut-aways: satellite flight to the Red Sea caves, the Tura -> Giza route, the papyrus + typed card on a desk ------
JARF, TURA, GIZA = (32.62, 29.0), (31.28, 29.93), (31.134, 29.979)
T_M0, T_M1 = 0.0, cue("cold", "Papyrus") - .1
M1 = MapInsert(cam=[(0, 25, 33, 4.4), (T_M1 - T_M0, JARF[0], JARF[1], 11.0)],
               marks=[dict(lon=JARF[0], lat=JARF[1], t=T_M1 - T_M0 - 1.3, label="WADI AL-JARF · CAVES")],
               labels=[dict(lon=33.8, lat=27.5, text="RED SEA", z=(6, 9.5), size=40)],
               grade=(1.0, .2, .15))
T_R0, T_R1 = S("but") + .2, E("but") + .2
M2 = MapInsert(cam=[(0, 31.2, 29.95, 10.6), (T_R1 - T_R0, 31.2, 29.95, 11.0)],
               routes=[dict(pts=[TURA, (31.25, 29.95), (31.22, 29.965), GIZA], t0=cue("but", "Sail") - T_R0, t1=cue("but", "Unload") - T_R0 + .3)],
               marks=[dict(lon=TURA[0], lat=TURA[1], t=cue("but", "Tura") - T_R0 - .1, label="TURA · QUARRY"),
                      dict(lon=GIZA[0], lat=GIZA[1], t=cue("but", "Giza") - T_R0 - .1, label="GIZA · PYRAMIDS", cross=True)],
               grade=(1.0, .2, .15))
T_D0, T_D1 = cue("detail", "wrote") - .1, E("detail") + .15
DK = Board(os.path.join(HERE, "img"), bg=desk(3600, 6000), size=(3600, 6000))
DK.photo("pap", "papyrus", 1800, 2650, 1500, -1, tilt=-1.2, sepia=.1)
DK.card("log", ["PAPYRUS JARF A · c. 2560 BC", "AUTHOR: MERER, INSPECTOR", "CREW: ~40 BOATMEN", "DAY BY DAY · LIKE A LOGBOOK"], 2000, 3350, 1050, -1, tilt=2,
        marks=[(3, "DAY BY DAY", cue("detail", "one by one") - T_D0, cue("detail", "one by one") - T_D0 + .5, "underline")], size=54)
for it in DK.items.values(): it.pin = False
DK.cam = [fit(DK, ["pap", "log"], 0, pad=90), fit(DK, ["pap", "log"], T_D1 - T_D0, pad=20)]
for tt in (0, T_D1 - T_D0): assert not check_frame(DK, tt, ["pap", "log"]), "desk items not fully visible"
EP.inserts = [(T_M0, T_M1, M1, None, MAPCREDIT), (T_D0, T_D1, BoardInsert(DK), "THE DIARY · ILLUSTRATIVE PAPYRUS", PAP),
              (T_R0, T_R1, M2, "TURA TO GIZA · BY BOAT", MAPCREDIT)]
EP.payoff = (S("why") + .1, 1.22)

num = lambda v: f"{v:,.0f}"
T_C0 = S("stakes") + .05
M = Meter([dict(t=T_C0, to=4500, dur=2.2, label="THIS DIARY IS", unit="YEARS OLD", fmt=num),
           dict(t=cue("so", "two") - .3, to=0, dur=.01, tween=False, label="MERER'S CREW", unit="BLOCKS A MONTH", fmt=num),
           dict(t=cue("so", "two") - .25, to=200, dur=1.0, label="MERER'S CREW", unit="BLOCKS A MONTH", fmt=num),
           dict(t=cue("today", "oldest") - .2, to=4500, dur=.01, tween=False, label="OLDEST PAPYRUS IN EGYPT", unit="YEARS OLD", fmt=lambda v: "4,500+",
                gold=True)],
          t_hide=S("why") - .05)
EP.counter_list = [(T_C0, 2.2, 4500), (cue("so", "two") - .25, 1.0, 200)]

def overlay(img, d, t):
    if t < 3.0: title_card(img, t, .25, 2.9, "THE DIARY", "RED SEA · 2013", 250)
    if not (S("back") - .1 <= t < cue("so", "two") - .35 or S("turn") - .1 <= t < S("today") - .1): M.draw(img, d, t)
    compare(img, d, t, S("why") - .05, (("THE MYTH", "ALIENS", WHITE), ("THE DIARY", "40 MEN, 1 BOAT", GOLD)))
EP.overlay = overlay

FX = [(T_C0, tick(.012), -.3), (T_C0 + 2.2, thud(.25), 0), (cue("cold", "Papyrus") - .05, thud(.2), 0),
      (cue("back", "aliens") - .25, whoosh(.7, .018), 0), (cue("but", "Tura") - .05, tick(.01), -.2), (cue("but", "Giza") - .05, thud(.2), 0),
      (cue("detail", "inspector") - .05, tick(.01), .2), (cue("so", "thirty") - .05, tick(.01), -.2),
      (cue("today", "oldest") - .2, pop(.12), .2), (S("why") - .05, boom(.35), 0)] + EP.cut_fx(.06) + EP.shot_fx(whoosh(.25, .015)) + insert_fx(EP.inserts)
if __name__ == "__main__": EP.run(FX)
