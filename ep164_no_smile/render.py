"""NOT JUST YOU – No. 164 (DOKU, new narration 27.11.2026): why nobody smiled in old photos. Paris 1838: Daguerre's
Boulevard du Temple – minutes of exposure, the busy street looks EMPTY, only a man having his boots shined stood
still long enough. Then iron head stands, a few seconds by the 1850s, 'say prunes', the $1 Brownie (1900), today
< 1/100 s. Mixed material: Lumière street film 1897 (illustrative), the daguerreotype on a desk with a red circle,
portraits, the Getty 'Say Prunes!' study card, the HOLD STILL meter. Every board element is framed with fit() so
nothing sits outside the picture. First 3 s: Lumière film of a busy Paris bridge, tag PARIS · 1838, title HOLD STILL."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from doku import *
from board import Board, BoardInsert, VideoInsert, desk, fit, check_frame, insert_fx, title_card
from swiss import pop, tick, thud, whoosh, boom
from cute import Timeline
import cute; cute.LOUD = -14
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"cold": .2, "stakes": .85, "back": .2, "detail": .2, "but": .4, "so": .2, "turn": .3, "today": .85, "why": .25},
              pace="loose")
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["cold", "stakes", "back", "detail", "but", "so", "turn", "today", "why", "end"]
IMG = os.path.join(HERE, "img"); VID = os.path.join(HERE, "vid")
EP = DokuEpisode(TL, 164, "HOLD STILL", order=ORDER, img_dir=IMG, credits=os.path.join(IMG, "credits.json"),
                 sources=("Getty Museum (2023), Say Prunes! ·", "Daguerre, Boulevard du Temple (1838)"),
                 music=dict(bpm=68, root=5, prog="minor", audio="doku"),
                 cover=dict(words=["WHY DID NOBODY", "SMILE IN", "OLD PHOTOS?"], kicker="Paris, 1838."))
DAG = "BOULEVARD DU TEMPLE · L. DAGUERRE, 1838 · PUBLIC DOMAIN"
EP.shots = [
    Shot("cold", "boulevard", (.5, .5, 1.0), (.5, .5, 1.0), start=0, tag="", grade=(.95, .1, .4)),          # under the film
    Shot("stakes", "boulevard", (.30, .45, 1.0), (.40, .45, 1.25), tag="THE FIRST PHOTO · 1838", grade=(.95, .1, .4), credit=DAG),
    Shot("detail", "man", (.47, .36, 1.7), (.47, .31, 2.4), tag="c. 1840 · DON'T MOVE", grade=(.95, .15, 0), ghost=1.6,
         credit=None),
    Shot("but", "woman", (.50, .30, 1.45), (.50, .27, 1.75), tag="1850s · A FEW SECONDS", grade=(1.0, .15, 0),
         credit="UNIDENTIFIED WOMAN · SOUTHWORTH & HAWES · c. 1850 · PUBLIC DOMAIN"),
    Shot("so", "family", (.72, .45, 1.6), (.62, .55, 2.1), tag="RARE · EXPENSIVE · FOREVER", grade=(.95, .2, 0)),
    Shot("turn", "brownie", (.5, .30, 1.0), (.5, .26, 1.15), tag="1900 · THE BROWNIE · $1", grade=(1.0, .1, 0)),
    Shot("turn", "phone", (.42, .55, 1.0), (.45, .52, 1.12), start=cue("turn", "smile") - .2, tag="SNAPSHOTS", grade=(1.05, .1, 0)),
    Shot("today", "phone", (.45, .52, 1.12), (.47, .50, 1.3), tag="TODAY", grade=(1.1, .1, 0)),
    Shot("why", "boulevard", (.40, .55, 1.15), (.20, .77, 3.0), tag="1838 VS. TODAY", grade=(1.0, .1, .4), credit=DAG),
]

# ---- cut-aways -------------------------------------------------------------------------------------------------
# the daguerreotype as a print on a desk; red circle around the man with the boots (left, lower third of the picture)
T_B0, T_B1 = S("back") - .05, E("back") + .1
DB = Board(IMG, bg=desk(2600, 4200), size=(2600, 4200))
DB.photo("blv", "boulevard", 1300, 2000, 1560, -1, tilt=-1.2, sepia=.2,
         marks=[("circle", (.17, .735, .23, .80), cue("back", "one man") - T_B0, cue("back", "one man") - T_B0 + .7)])
DB.items["blv"].pin = False
c_full = fit(DB, ["blv"], 0); bx = DB.items["blv"]
man_x, man_y = bx.x - bx.w / 2 + .20 * bx.w, bx.y - bx.h / 2 + .77 * bx.h          # board px of the man (approx.)
DB.cam = [c_full, (cue("back", "vanished") - T_B0, *c_full[1:]), (cue("back", "one man") - T_B0 + .2, man_x + 60, man_y + 170, 700),
          (T_B1 - T_B0, man_x + 50, man_y + 190, 620)]          # man sits at ~y 700, above the subtitles
assert not check_frame(DB, 0, ["blv"]), "daguerreotype not fully visible"
EP.inserts = [
    (0.0, E("cold") + .1, VideoInsert(os.path.join(VID, "parislepontneuf.mp4"), 6, E("cold") + .4, os.path.join(VID, "cache", "pont"),
                                      sepia=.5), None, "PARIS, LE PONT-NEUF · LUMIÈRE, 1897 · PUBLIC DOMAIN"),
    (T_B0, T_B1, BoardInsert(DB), "ONE MAN STOOD STILL", DAG),
]
EP.accent = {"cold": ["people everywhere"], "stakes": ["empty"], "back": ["one man", "stood still"], "detail": ["froze", "blur"],
             "but": ["few seconds"], "so": ["prunes"], "turn": ["one dollar", "smile"], "today": ["hundredth second"], "why": ["empty", "blink"]}
EP.payoff = (S("why") + .1, 1.18)

def secs(v):
    if v >= 299: return "MINUTES"
    if v >= .95: return f"{v:.0f} s"
    return "1/100 s" if v <= .0105 else f"{v:.2f} s"
M = Meter([dict(t=cue("back", "minutes") - .2, to=300, dur=.9, label="HOLD STILL FOR", unit="DAGUERRE · 1838", fmt=secs, stamp="DON'T MOVE"),
           dict(t=cue("but", "few") - .2, to=3, dur=.8, label="BY THE 1850s", unit="SECONDS", fmt=secs),
           dict(t=cue("today", "hundredth") - .2, to=.01, dur=1.0, label="TODAY", unit="OF A SECOND", fmt=secs, gold=True)],
          t_hide=S("why") - .05)
EP.counter_list = M.counters()

def overlay(img, d, t):
    if (t < T_B0 or t >= T_B1) and not (E("but") + .3 <= t < S("today") - .1): M.draw(img, d, t)   # never over the desk print, the card or the Brownie ad                         # the meter never covers the desk print
    if t < 3.0: title_card(img, t, .25, 2.9, "HOLD STILL", "PARIS · 1838 · (FILM: 1897, ILLUSTRATIVE)", 250)
    paper_card(img, t, cue("so", "Some"), E("so") + .1, "GETTY MUSEUM · 2023", "Say Prunes! The surprising history of the smile in early photographs",
               "Say Prunes!", (cue("so", "prunes") - .1, cue("so", "prunes") + .4), foot="J. PAUL GETTY MUSEUM, LOS ANGELES", y=380)
    compare(img, d, t, S("why") - .05, (("1838 · HOLD STILL", "MINUTES", WHITE), ("YOU · TODAY", "1/100 SEC", GOLD)))
EP.overlay = overlay

FX = [(cue("back", "vanished") - .1, whoosh(.35, .012), 0), (cue("back", "boots") - .05, tick(.01), .2),
      (cue("detail", "froze") - .05, thud(.2), 0), (cue("detail", "iron") - .05, tick(.012), -.2), (cue("turn", "snapshots") - .1, pop(.08), .2),
      (cue("back", "minutes") - .1, tick(.012), -.3), (cue("back", "one man") + .1, thud(.25), 0),
      (cue("detail", "blur") - .1, whoosh(.5, .02), 0), (cue("so", "Some") - .05, whoosh(.3, .012), .2),
      (cue("today", "hundredth") + .8, pop(.1), .2), (S("why") - .05, boom(.35), 0)] \
     + EP.cut_fx(.06) + EP.shot_fx(whoosh(.25, .015)) + insert_fx(EP.inserts)
if __name__ == "__main__": EP.run(FX)
