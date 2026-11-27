"""NOT JUST YOU – No. 169 (DOKU, 26.11.2026): marrying for love is new. For most of history marriage was an economic and
political deal between families; the love-match ideal spread from the late 18th century, about 200 years ago
(Stephanie Coontz 2005, Marriage, a History). Today ~80% (US) say they look for a soulmate (Coontz interview).
1743 = Hogarth's Marriage A-la-Mode (illustrative). Gold element (rule 12, doku): WHO PICKS? PARENTS → LOVE → 80%.
First 3 s (Chris OK 26.11.): Hogarth's Marriage Settlement, camera on the bored couple from frame 0, tag LONDON · 1743,
stamp ARRANGED."""
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
EP = DokuEpisode(TL, 169, "WHO PICKS?", order=ORDER, img_dir=os.path.join(HERE, "img"), credits=os.path.join(HERE, "img", "credits.json"),
                 sources=("Stephanie Coontz (2005),", "Marriage, a History"),
                 music=dict(bpm=66, root=9, prog="minor", audio="doku"),
                 cover=dict(words=["WHO PICKED", "YOUR PARTNER", "IN 1743?"], kicker="Marriage A-la-Mode."))

HOG = "MARRIAGE A-LA-MODE 1, THE MARRIAGE SETTLEMENT · WILLIAM HOGARTH · c. 1743 · PUBLIC DOMAIN"
EP.shots = [
    Shot("cold", "hogarth", (.22, .50, 2.4), (.24, .48, 2.9), start=0, tag="", grade=(1.0, .25, 0), credit=HOG),
    Shot("cold", "hogarth", (.66, .48, 2.2), (.68, .46, 2.6), start=cue("cold", "bride") - .2, tag="LONDON · 1743", grade=(1.0, .25, 0), credit=HOG),
    Shot("stakes", "plate", (.45, .60, 2.0), (.48, .58, 2.4), tag="LAND · MONEY · FAMILY", grade=(.95, .2, .6),
         credit="MARRIAGE A-LA-MODE, PLATE I · SCOTIN after HOGARTH · 1745 · THE MET · CC0"),
    Shot("back", "hogarth", (.25, .5, 1.05), (.65, .5, 1.1), tag="A DEAL BETWEEN FAMILIES", grade=(.95, .25, 0), credit=HOG),
    Shot("detail", "plate", (.40, .55, 1.6), (.55, .55, 1.8), tag="LAND · MONEY · ALLIANCES", grade=(.95, .2, .6)),
    Shot("but", "boecklin", (.45, .25, 1.4), (.45, .22, 1.7), tag="THE LOVE MATCH", grade=(1.05, .2, 0),
         credit="HONEYMOON · ARNOLD BÖCKLIN · c. 1890 · PUBLIC DOMAIN"),
    Shot("so", "sandberg", (.5, .40, 1.0), (.5, .36, 1.15), tag="c. 1916", grade=(1.05, .15, .3),
         credit="THEA & RAGNAR SANDBERG · c. 1916 · PUBLIC DOMAIN"),
    Shot("turn", "japanese", (.5, .40, 1.0), (.5, .38, 1.12), tag="1920s · DATING", grade=(1.05, .15, .3),
         credit="JAPANESE COUPLE TAKING A PHOTO TOGETHER · 1920s · PUBLIC DOMAIN"),
    Shot("turn", "phone", (.45, .45, 1.0), (.48, .45, 1.12), start=cue("turn", "apps") - .2, tag="THE APPS", grade=(1.0, .05, 0),
         credit="SMARTPHONE · UNKNOWN AUTHOR · CC0"),
    Shot("today", "phone", (.48, .45, 1.12), (.50, .45, 1.3), tag="TODAY", grade=(1.0, .05, 0), credit="SMARTPHONE · UNKNOWN AUTHOR · CC0"),
    Shot("why", "hogarth", (.23, .49, 2.0), (.23, .49, 2.0), tag="1743 VS. TODAY", grade=(1.05, .25, 0), credit=HOG),
]
EP.accent = {"cold": ["barely look"], "stakes": ["parents"], "back": ["family tree", "money"], "detail": ["too fragile"],
             "but": ["marry for love"], "so": ["Courtship"], "turn": ["apps"], "today": ["soulmate"], "why": ["Your choice"]}

# ---- cut-aways: the Hogarth as a print on a desk (red circles: family tree, merchant), the 1897 ball film -------------
T_H0, T_H1 = cue("back", "earl") - .2, E("back") + .15
HB = Board(os.path.join(HERE, "img"), bg=desk(3600, 6000), size=(3600, 6000))
HB.photo("hog", "hogarth", 1800, 3000, 1700, -1, tilt=1.0, sepia=.1,
         marks=[("circle", (.70, .78, .88, .96), cue("back", "family") - T_H0, cue("back", "family") - T_H0 + .6),
                ("circle", (.38, .50, .56, .72), cue("back", "merchant") - T_H0, cue("back", "merchant") - T_H0 + .6)])
HB.items["hog"].pin = False
HB.cam = [fit(HB, ["hog"], 0, pad=80), fit(HB, ["hog"], T_H1 - T_H0, pad=10)]
for tt in (0, T_H1 - T_H0): assert not check_frame(HB, tt, ["hog"]), "painting not fully visible"
EP.inserts = [(T_H0, T_H1, BoardInsert(HB), "THE MARRIAGE SETTLEMENT · 1743", HOG),
              (cue("so", "Balls") - .15, E("so") + .15, VideoInsert(os.path.join(HERE, "vid", "ball.mp4"), 6, 4, os.path.join(HERE, "vid", "cache", "ball"),
               sepia=.35, crop="304:240:8:0"), "BALLS · COURTSHIP", "CHARITY BALL · EDISON, 1897 · PUBLIC DOMAIN")]
EP.payoff = (S("why") + .1, 1.22)

T_C0 = S("stakes") + .05
M = Meter([dict(t=T_C0, to=0, dur=.8, label="WHO PICKS YOUR PARTNER?", fmt=lambda v: "PARENTS", stamp="ARRANGED"),
           dict(t=cue("but", "love") - .2, to=0, dur=.5, tween=False, label="c. 1800 · A NEW IDEA", fmt=lambda v: "LOVE"),
           dict(t=cue("today", "eight") - .2, to=80, dur=1.2, label="TODAY", unit="LOOKING FOR A SOULMATE", fmt=lambda v: f"{v:.0f}%", gold=True)],
          t_hide=S("why") - .05)
EP.counter_list = [(cue("today", "eight") - .2, 1.2, 80)]

def overlay(img, d, t):
    if t < 3.0: title_card(img, t, .25, 2.9, "WHO PICKS?", "LONDON · 1743", 250)
    if not (T_H0 - .2 <= t < T_H1 + .2 or S("detail") - .1 <= t < E("detail") + .2 or S("so") - .1 <= t < S("today") - .1): M.draw(img, d, t)
    paper_card(img, t, S("detail") + .1, E("detail") + .2, "BOOK · STEPHANIE COONTZ · 2005",
               "Marriage, a History: From Obedience to Intimacy, or How Love Conquered Marriage", "How Love Conquered Marriage",
               (cue("detail", "Love") - .1, cue("detail", "Love") + .5), foot="VIKING PRESS, NEW YORK", y=380)
    compare(img, d, t, S("why") - .05, (("1743", "PARENTS PICK", WHITE), ("YOU · TODAY", "YOU PICK", GOLD)))
EP.overlay = overlay

FX = [(T_C0 + .8, thud(.25), 0), (cue("cold", "barely") - .05, tick(.01), .2), (cue("detail", "Love") - .05, tick(.012), -.2),
      (cue("turn", "Divorce") - .05, tick(.01), .2),
      (cue("but", "love") - .2, pop(.12), .2), (S("why") - .05, boom(.35), 0)] + EP.cut_fx(.06) + EP.shot_fx(whoosh(.25, .015)) + insert_fx(EP.inserts)
if __name__ == "__main__": EP.run(FX)
