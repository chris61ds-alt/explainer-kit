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
import cute; cute.LOUD = -14
from board import Board, BoardInsert, VideoInsert, desk, fit, check_frame, insert_fx, title_card
from maps import MapInsert, CREDIT as MAPCREDIT
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"cold": .2, "stakes": .85, "back": .3, "detail": .3, "but": .3, "so": .3, "turn": .3, "today": .85, "why": .25},
              pace="loose")
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["cold", "stakes", "back", "detail", "but", "so", "turn", "today", "why", "end"]
EP = DokuEpisode(TL, 171, "THE BRONZE LUMP", order=ORDER, img_dir=os.path.join(HERE, "img"), credits=os.path.join(HERE, "img", "credits.json"),
                 sources=("Freeth et al. (2006), Nature 444 ·", "Linda Hall Library"),
                 music=dict(bpm=64, root=6, prog="minor", audio="doku"),
                 cover=dict(words=["WHAT WAS INSIDE", "THIS LUMP", "OF BRONZE?"], kicker="Found in 1901."))

FRAG = "ANTIKYTHERA FRAGMENT A · LOGG TANDY · CC BY 4.0"
TIL = "THE ANTIKYTHERA MECHANISM · TILEMAHOS EFTHIMIADIS · CC BY 2.0"
EP.shots = [
    Shot("cold", "ephebe", (.62, .16, 2.6), (.62, .15, 3.0), start=0, tag="", grade=(.85, .3, 0),
         credit="ANTIKYTHERA YOUTH, FROM THE SAME WRECK · NAMA ATHENS · JEBULON · CC0"),
    Shot("cold", "ephebe", (.62, .20, 2.2), (.62, .16, 2.7), start=cue("cold", "bodies") - .2, tag="BODIES ON THE SEABED?", grade=(.85, .3, 0), credit=None),
    Shot("stakes", "ephebe", (.55, .35, 1.3), (.55, .30, 1.5), tag="BRONZE STATUES · 2,000 YEARS", grade=(.9, .3, 0), credit=None),
    Shot("stakes", "fragA", (.50, .50, 1.3), (.50, .50, 1.55), start=cue("stakes", "lump") - .2, tag="A LUMP OF BRONZE", grade=(.85, .25, 0), credit=FRAG),
    Shot("back", "fragA", (.45, .45, 1.6), (.45, .45, 2.0), tag="ATHENS · 1902 · A GEAR", grade=(.95, .25, 0), credit=FRAG),
    Shot("back", "til1", (.50, .5, 1.1), (.55, .5, 1.25), start=cue("back", "Nothing") - .2, tag="TOO ADVANCED?", grade=(.85, .2, 0), credit=TIL),
    Shot("back", "til1", (.55, .5, 1.25), (.55, .5, 1.6), start=cue("back", "aliens") - .25, tag="THE ALIEN THEORY", grade=(.55, 0, .6), ghost=1.2, credit=TIL),
    Shot("detail", "fragB", (.50, .50, 1.2), (.50, .48, 1.45), tag="X-RAY · 2005", grade=(.9, .1, .5),
         credit="ANTIKYTHERA FRAGMENT B · LOGG TANDY · CC BY 4.0"),
    Shot("but", "fragD", (.50, .50, 1.1), (.50, .50, 1.3), start=S("but") - .05, tag="30+ GEARS", grade=(.95, .2, 0),
         credit="ANTIKYTHERA FRAGMENT D · LOGG TANDY · CC BY 4.0"),
    Shot("so", "til2", (.50, .5, 1.1), (.55, .48, 1.3), tag="SUN · MOON · ECLIPSES", grade=(1.0, .25, 0), credit=TIL),
    Shot("so", "nama", (.50, .5, 1.3), (.45, .5, 1.6), start=cue("so", "eclipses") - .25, tag="SUN · MOON · ECLIPSES", grade=(1.0, .25, 0),
         credit="ANTIKYTHERA MECHANISM · NAMA ATHENS · CC BY 2.5"),
    Shot("turn", "portrait", (.50, .35, 1.1), (.50, .32, 1.3), tag="GREECE · 150–100 BC", grade=(1.0, .3, 0),
         credit="ANTIKYTHERA YOUTH, PORTRAIT · NIKOS KITSAKIS · CC BY 4.0"),
    Shot("today", "til3", (.50, .5, 1.1), (.50, .5, 1.25), tag="NATURE · 2006", grade=(.6, .2, 0), credit=TIL),
    Shot("why", "fragA", (.50, .50, 1.5), (.50, .50, 1.5), tag="NO ALIENS", grade=(1.05, .25, 0), credit=FRAG),
]
EP.accent = {"cold": ["bodies"], "stakes": ["lump of corroded bronze"], "back": ["aliens"], "detail": ["X-ray"], "but": ["thirty", "user manual"],
             "so": ["machine", "eclipses"], "turn": ["Greeks"], "today": ["analog computer"], "why": ["Greek genius"]}

# ---- cut-aways: storm film, satellite flight to Antikythera, the lump + typed card on a desk ------------------------------
WRECK = (23.317, 35.888)                                              # Point Glyphadia, NE coast (approx.)
T_F1 = cue("cold", "shelter") - .1
T_M1 = cue("cold", "bodies") - .25
M1 = MapInsert(cam=[(0, 18, 39, 5.0), (T_M1 - T_F1, WRECK[0] - .02, WRECK[1] - .045, 12.6)],
               marks=[dict(lon=WRECK[0], lat=WRECK[1], t=T_M1 - T_F1 - 1.4, label="THE WRECK · c. 60 BC", cross=True)],
               labels=[dict(lon=22.5, lat=37.6, text="GREECE", z=(5, 7.6))],
               grade=(1.0, .15, .1))
T_D0, T_D1 = cue("detail", "Then") - .15, E("detail") + .15
DK = Board(os.path.join(HERE, "img"), bg=desk(3600, 6000), size=(3600, 6000))
DK.photo("lump", "fragA", 1800, 2650, 1300, -1, tilt=-1.5, sepia=.1)
DK.card("ct", ["NATIONAL ARCHAEOLOGICAL MUSEUM", "82 FRAGMENTS", "2005: X-RAY CT SCANS", "INSIDE: GEARS + TEXT"], 2050, 3420, 1050, -1, tilt=2,
        marks=[(2, "X-RAY CT", cue("detail", "X-ray") - T_D0, cue("detail", "X-ray") - T_D0 + .5, "underline")], size=54)
for it in DK.items.values(): it.pin = False
DK.cam = [fit(DK, ["lump", "ct"], 0, pad=90), fit(DK, ["lump", "ct"], T_D1 - T_D0, pad=20)]
for tt in (0, T_D1 - T_D0): assert not check_frame(DK, tt, ["lump", "ct"]), "desk items not fully visible"
EP.inserts = [(0.0, T_F1, VideoInsert(os.path.join(HERE, "vid", "storm.webm"), 40, T_F1 + .3, os.path.join(HERE, "vid", "cache", "st")),
               None, "A STORM AT SEA (1900) · EDISON MFG. CO. · PUBLIC DOMAIN"),
              (T_F1, T_M1, M1, "ANTIKYTHERA · GREECE", MAPCREDIT),
              (T_D0, T_D1, BoardInsert(DK), "2005 · LOOKING INSIDE", FRAG)]
EP.payoff = (S("why") + .1, 1.22)

num = lambda v: f"{v:,.0f}"
T_C0 = cue("stakes", "two thousand") - .2
M = Meter([dict(t=T_C0, to=2000, dur=2.0, label="THE SHIPWRECK IS", unit="YEARS OLD", fmt=num),
           dict(t=cue("but", "thirty") - .3, to=0, dur=.01, tween=False, label="INSIDE THE LUMP", unit="BRONZE GEARS", fmt=num),
           dict(t=cue("but", "thirty") - .25, to=30, dur=.9, label="INSIDE THE LUMP", unit="BRONZE GEARS", fmt=lambda v: f"{v:.0f}+" if v >= 29.5 else f"{v:.0f}",
                stamp="HAND-CUT")],
          t_hide=S("today") - .1)
EP.counter_list = [(T_C0, 2.0, 2000), (cue("but", "thirty") - .25, .9, 30)]

T_CARD = S("today") - .05
def overlay(img, d, t):
    if t < 3.0: title_card(img, t, .25, 2.9, "THE LUMP", "GREECE · 1900 · (FILM: ILLUSTRATIVE)", 250)
    if not (T_D0 - .2 <= t < T_D1 + .2): M.draw(img, d, t)
    paper_card(img, t, T_CARD, S("why") - .1, "NATURE · VOL. 444 · 30 NOVEMBER 2006",
               "Decoding the ancient Greek astronomical calculator known as the Antikythera Mechanism",
               "astronomical calculator", (cue("today", "analog") - .3, cue("today", "computer") + .3),
               foot="Freeth, Bitsakis, Moussas et al.", y=470)
    compare(img, d, t, S("why") - .05, (("THE MYTH", "ALIENS", WHITE), ("THE LUMP", "30+ GEARS", GOLD)))
EP.overlay = overlay

FX = [(T_C0, tick(.012), -.3), (T_C0 + 2.0, thud(.25), 0), (cue("back", "gear"), pop(.1), .2), (cue("cold", "terrified") - .05, thud(.2), 0),
      (cue("so", "handle") - .05, tick(.01), .2), (cue("turn", "Greeks") - .05, tick(.01), -.2),
      (cue("back", "aliens") - .25, whoosh(.7, .018), 0), (cue("but", "thirty") + .7, thud(.22), 0),
      (T_CARD, whoosh(.4, .015), .2), (cue("today", "analog") - .3, tick(.02), 0),
      (S("why") - .05, boom(.35), 0)] + EP.cut_fx(.06) + EP.shot_fx(whoosh(.25, .015)) + insert_fx(EP.inserts)
if __name__ == "__main__": EP.run(FX)
