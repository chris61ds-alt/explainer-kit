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
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"cold": .35, "stakes": .85, "back": .5, "but": .6, "so": .4, "turn": .5, "today": .85, "why": .2}, pace="loose")
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["cold", "stakes", "back", "but", "so", "turn", "today", "why", "end"]
EP = DokuEpisode(TL, 170, "MERER'S DIARY", order=ORDER, img_dir=os.path.join(HERE, "img"), credits=os.path.join(HERE, "img", "credits.json"),
                 sources=("Tallet (2017), Les papyrus de la Mer Rouge I ·", "Tallet & Marouard (2014)"),
                 music=dict(bpm=74, root=1, prog="minor", kick="half", audio="v5"),
                 cover=dict(words=["WHO REALLY BUILT", "THE GREAT", "PYRAMID?"], kicker="Found in 2013."))

PAP = "ILLUSTRATIVE: LETTER IN HIERATIC SCRIPT · THE MET · CC0"
EP.shots = [
    Shot("cold", "papyrus", (.47, .45, 3.8), (.50, .45, 4.4), start=0, tag="RED SEA · 2013", grade=(.85, .3, 0), credit=PAP),
    Shot("stakes", "haghe", (.62, .45, 1.15), (.62, .42, 1.35), tag="GIZA · c. 2560 BC", grade=(.95, .3, 0),
         credit="PYRAMIDS AT GÎZA · LOUIS HAGHE after DAVID ROBERTS · WELLCOME COLLECTION · CC BY 4.0"),
    Shot("back", "bonfils", (.25, .45, 1.2), (.32, .42, 1.35), tag="HOW?", grade=(.9, .25, .4),
         credit="CAIRE. ALLÉE DE PYRAMIDES · FÉLIX BONFILS · THE MET · CC0"),
    Shot("back", "rijks", (.55, .30, 1.4), (.55, .26, 1.8), start=cue("back", "aliens") - .25, tag="THE ALIEN THEORY", grade=(.6, 0, .6), ghost=1.2,
         credit="PYRAMID OF CHEOPS, GIZEH · RIJKSMUSEUM · CC0"),
    Shot("but", "scribe", (.5, .45, 1.1), (.5, .42, 1.3), tag="MERER · INSPECTOR", grade=(1.0, .25, 0),
         credit="ILLUSTRATIVE: STATUE OF A SCRIBE · MUSEO EGIZIO, TURIN · CC0"),
    Shot("so", "boat", (.35, .5, 1.2), (.55, .48, 1.3), tag="THE NILE · 40 BOATMEN", grade=(1.0, .25, 0),
         credit="MODEL PADDLING BOAT · TOMB OF MEKETRE · THE MET · CC0"),
    Shot("so", "boat2", (.40, .5, 1.1), (.60, .5, 1.15), start=cue("so", "two") - .2, tag="200 BLOCKS A MONTH", grade=(.95, .2, .3),
         credit="MODEL BOAT · THE MET · CC0"),
    Shot("turn", "casing", (.45, .45, 1.1), (.50, .42, 1.3), tag="TURA LIMESTONE · CASING", grade=(1.0, .25, 0),
         credit="CASING STONE OF THE GREAT PYRAMID · BRITISH MUSEUM · CAPTMONDO · CC BY 2.5"),
    Shot("today", "papyrus", (.50, .45, 3.6), (.52, .45, 4.0), tag="OLDEST PAPYRUS IN EGYPT", grade=(1.05, .3, 0), credit=PAP),
    Shot("why", "rijks", (.55, .35, 1.25), (.55, .35, 1.25), tag="NO ALIENS", grade=(1.05, .2, .3),
         credit="PYRAMID OF CHEOPS, GIZEH · RIJKSMUSEUM · CC0"),
]
EP.accent = {"cold": ["diary"], "stakes": ["great pyramid"], "back": ["aliens"], "but": ["merer forty"],
             "so": ["two hundred blocks"], "turn": ["tura"], "today": ["oldest"], "why": ["diary forty boat"]}
EP.payoff = (S("why") + .1, 1.22)

num = lambda v: f"{v:,.0f}"
T_C0 = 1.0
M = Meter([dict(t=T_C0, to=4500, dur=2.2, label="THIS DIARY IS", unit="YEARS OLD", fmt=num),
           dict(t=cue("so", "two") - .3, to=0, dur=.01, tween=False, label="MERER'S CREW", unit="BLOCKS A MONTH", fmt=num),
           dict(t=cue("so", "two") - .25, to=200, dur=1.0, label="MERER'S CREW", unit="BLOCKS A MONTH", fmt=num),
           dict(t=cue("today", "oldest") - .2, to=4500, dur=.01, tween=False, label="OLDEST PAPYRUS IN EGYPT", unit="YEARS OLD", fmt=lambda v: "4,500+",
                gold=True)],
          t_hide=S("why") - .05)
EP.counter_list = [(T_C0, 2.2, 4500), (cue("so", "two") - .25, 1.0, 200)]

def overlay(img, d, t):
    M.draw(img, d, t)
    compare(img, d, t, S("why") - .05, (("THE MYTH", "ALIENS", WHITE), ("THE DIARY", "40 MEN, 1 BOAT", GOLD)))
EP.overlay = overlay

FX = [(0.0, whoosh(.6, .02), -.2), (T_C0, tick(.012), -.3), (T_C0 + 2.2, thud(.25), 0),
      (cue("back", "aliens") - .25, whoosh(.7, .018), 0), (cue("but", "logbook"), thud(.25), 0),
      (cue("today", "oldest") - .2, pop(.12), .2), (S("why") - .05, boom(.35), 0)] + EP.cut_fx(.06) + EP.shot_fx(whoosh(.25, .015))
if __name__ == "__main__": EP.run(FX)
