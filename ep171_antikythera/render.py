"""NOT JUST YOU – No. 171 (MYSTERY, 26.11.2026): the Antikythera mechanism. 1901 sponge divers raise finds from a Roman-era
wreck; May 1902 a gear is noticed in a corroded lump (Stais, Athens); X-ray tomography 2005–06 reveals 30+ hand-cut
bronze gears and inscriptions; dated 150–100 BC; tracked sun and moon, predicted eclipses; nothing comparable for
another thousand years (Freeth et al. 2006, Nature 444; Live Science; Linda Hall Library). Mystery format; first use of
the paper card with marker (Chris 26.11.: "Zeitungsartikel unterstreichen") – a neutral study card with the REAL title.
Gold element (rule 12): AGE 0 → 2,000 YEARS → GEARS 0 → 30+ → the study card. First 3 s: the bronze youth raised from
the same wreck, camera on the face from frame 0, tag ANTIKYTHERA · 1901, counter THE SHIPWRECK IS 0 → 2,000 years old."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from doku import *
from swiss import pop, tick, thud, whoosh, boom
from cute import Timeline
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"cold": .35, "stakes": .85, "back": .5, "but": .6, "so": .4, "turn": .5, "today": .85, "why": .2}, pace="loose")
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["cold", "stakes", "back", "but", "so", "turn", "today", "why", "end"]
EP = DokuEpisode(TL, 171, "THE BRONZE LUMP", order=ORDER, img_dir=os.path.join(HERE, "img"), credits=os.path.join(HERE, "img", "credits.json"),
                 sources=("Freeth et al. (2006), Nature 444 ·", "Linda Hall Library"),
                 music=dict(bpm=76, root=3, prog="minor", kick="half", audio="v5"),
                 cover=dict(words=["WHAT WAS INSIDE", "THIS LUMP", "OF BRONZE?"], kicker="Found in 1901."))

FRAG = "ANTIKYTHERA FRAGMENT A · LOGG TANDY · CC BY 4.0"
TIL = "THE ANTIKYTHERA MECHANISM · TILEMAHOS EFTHIMIADIS · CC BY 2.0"
EP.shots = [
    Shot("cold", "ephebe", (.62, .16, 2.6), (.62, .15, 3.0), start=0, tag="ANTIKYTHERA · 1901", grade=(.85, .3, 0),
         credit="ANTIKYTHERA YOUTH, FROM THE SAME WRECK · NAMA ATHENS · JEBULON · CC0"),
    Shot("cold", "fragA", (.50, .50, 1.3), (.50, .50, 1.55), start=cue("cold", "lump") - .2, tag="A LUMP OF BRONZE", grade=(.85, .25, 0), credit=FRAG),
    Shot("stakes", "fragA", (.45, .45, 1.6), (.45, .45, 2.0), tag="ATHENS · 1902", grade=(.95, .25, 0), credit=FRAG),
    Shot("back", "til1", (.50, .5, 1.1), (.55, .5, 1.25), tag="TOO ADVANCED?", grade=(.85, .2, 0), credit=TIL),
    Shot("back", "til1", (.55, .5, 1.25), (.55, .5, 1.6), start=cue("back", "aliens") - .25, tag="THE ALIEN THEORY", grade=(.55, 0, .6), ghost=1.2, credit=TIL),
    Shot("but", "fragB", (.50, .50, 1.2), (.50, .48, 1.45), tag="X-RAY · 2005", grade=(.9, .1, .5),
         credit="ANTIKYTHERA FRAGMENT B · LOGG TANDY · CC BY 4.0"),
    Shot("but", "fragD", (.50, .50, 1.1), (.50, .50, 1.3), start=cue("but", "thirty") - .2, tag="30+ GEARS", grade=(.95, .2, 0),
         credit="ANTIKYTHERA FRAGMENT D · LOGG TANDY · CC BY 4.0"),
    Shot("so", "til2", (.50, .5, 1.1), (.55, .48, 1.3), tag="SUN · MOON · ECLIPSES", grade=(1.0, .25, 0), credit=TIL),
    Shot("so", "nama", (.50, .5, 1.3), (.45, .5, 1.6), start=cue("so", "eclipses") - .25, tag="SUN · MOON · ECLIPSES", grade=(1.0, .25, 0),
         credit="ANTIKYTHERA MECHANISM · NAMA ATHENS · CC BY 2.5"),
    Shot("turn", "portrait", (.50, .35, 1.1), (.50, .32, 1.3), tag="GREECE · 150–100 BC", grade=(1.0, .3, 0),
         credit="ANTIKYTHERA YOUTH, PORTRAIT · NIKOS KITSAKIS · CC BY 4.0"),
    Shot("today", "til3", (.50, .5, 1.1), (.50, .5, 1.25), tag="NATURE · 2006", grade=(.6, .2, 0), credit=TIL),
    Shot("why", "fragA", (.50, .50, 1.5), (.50, .50, 1.5), tag="NO ALIENS", grade=(1.05, .25, 0), credit=FRAG),
]
EP.accent = {"cold": ["lump bronze"], "stakes": ["gear"], "back": ["aliens"], "but": ["thirty"], "so": ["machine eclipses"],
             "turn": ["greeks"], "today": ["oldest analog computer"], "why": ["lump bronze greek genius"]}
EP.payoff = (S("why") + .1, 1.22)

num = lambda v: f"{v:,.0f}"
T_C0 = 1.0
M = Meter([dict(t=T_C0, to=2000, dur=2.0, label="THE SHIPWRECK IS", unit="YEARS OLD", fmt=num),
           dict(t=cue("but", "thirty") - .3, to=0, dur=.01, tween=False, label="INSIDE THE LUMP", unit="BRONZE GEARS", fmt=num),
           dict(t=cue("but", "thirty") - .25, to=30, dur=.9, label="INSIDE THE LUMP", unit="BRONZE GEARS", fmt=lambda v: f"{v:.0f}+" if v >= 29.5 else f"{v:.0f}",
                stamp="HAND-CUT")],
          t_hide=S("today") - .1)
EP.counter_list = [(T_C0, 2.0, 2000), (cue("but", "thirty") - .25, .9, 30)]

T_CARD = S("today") - .05
def overlay(img, d, t):
    M.draw(img, d, t)
    paper_card(img, t, T_CARD, S("why") - .1, "NATURE · VOL. 444 · 30 NOVEMBER 2006",
               "Decoding the ancient Greek astronomical calculator known as the Antikythera Mechanism",
               "astronomical calculator", (cue("today", "analog") - .3, cue("today", "computer") + .3),
               foot="Freeth, Bitsakis, Moussas et al.", y=470)
    compare(img, d, t, S("why") - .05, (("THE MYTH", "ALIENS", WHITE), ("THE LUMP", "30+ GEARS", GOLD)))
EP.overlay = overlay

FX = [(0.0, whoosh(.6, .02), -.2), (T_C0, tick(.012), -.3), (T_C0 + 2.0, thud(.25), 0), (cue("stakes", "gear"), pop(.1), .2),
      (cue("back", "aliens") - .25, whoosh(.7, .018), 0), (cue("but", "thirty") + .7, thud(.22), 0),
      (T_CARD, whoosh(.4, .015), .2), (cue("today", "analog") - .3, tick(.02), 0),
      (S("why") - .05, boom(.35), 0)] + EP.cut_fx(.06) + EP.shot_fx(whoosh(.25, .015))
if __name__ == "__main__": EP.run(FX)
