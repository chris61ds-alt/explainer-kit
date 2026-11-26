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
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"cold": .35, "stakes": .85, "back": .4, "but": .6, "so": .4, "turn": .5, "today": .85, "why": .2}, pace="loose")
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["cold", "stakes", "back", "but", "so", "turn", "today", "why", "end"]
EP = DokuEpisode(TL, 169, "WHO PICKS?", order=ORDER, img_dir=os.path.join(HERE, "img"), credits=os.path.join(HERE, "img", "credits.json"),
                 sources=("Stephanie Coontz (2005),", "Marriage, a History"),
                 music=dict(bpm=80, root=4, prog="minor", kick="half", audio="v5"),
                 cover=dict(words=["WHO PICKED", "YOUR PARTNER", "IN 1743?"], kicker="Marriage A-la-Mode."))

HOG = "MARRIAGE A-LA-MODE 1, THE MARRIAGE SETTLEMENT · WILLIAM HOGARTH · c. 1743 · PUBLIC DOMAIN"
EP.shots = [
    Shot("cold", "hogarth", (.22, .50, 2.4), (.24, .48, 2.9), start=0, tag="LONDON · 1743", grade=(1.0, .25, 0), credit=HOG),
    Shot("cold", "hogarth", (.66, .48, 2.2), (.68, .46, 2.6), start=cue("cold", "parents") - .2, tag="LONDON · 1743", grade=(1.0, .25, 0), credit=HOG),
    Shot("stakes", "plate", (.45, .60, 2.0), (.48, .58, 2.4), tag="LAND · MONEY · FAMILY", grade=(.95, .2, .6),
         credit="MARRIAGE A-LA-MODE, PLATE I · SCOTIN after HOGARTH · 1745 · THE MET · CC0"),
    Shot("back", "hogarth", (.25, .5, 1.05), (.65, .5, 1.1), tag="A DEAL BETWEEN FAMILIES", grade=(.95, .25, 0), credit=HOG),
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
EP.accent = {"cold": ["your parents"], "stakes": ["land money family"], "back": ["deal"], "but": ["marry love"],
             "so": ["normal"], "turn": ["apps"], "today": ["eight ten soulmate"], "why": ["your parents yourself"]}
EP.payoff = (S("why") + .1, 1.22)

T_C0 = 1.2
M = Meter([dict(t=T_C0, to=0, dur=.8, label="WHO PICKS YOUR PARTNER?", fmt=lambda v: "PARENTS", stamp="ARRANGED"),
           dict(t=cue("but", "love") - .2, to=0, dur=.5, tween=False, label="c. 1800 · A NEW IDEA", fmt=lambda v: "LOVE"),
           dict(t=cue("today", "eight") - .2, to=80, dur=1.2, label="TODAY", unit="LOOKING FOR A SOULMATE", fmt=lambda v: f"{v:.0f}%", gold=True)],
          t_hide=S("why") - .05)
EP.counter_list = [(cue("today", "eight") - .2, 1.2, 80)]

def overlay(img, d, t):
    M.draw(img, d, t)
    compare(img, d, t, S("why") - .05, (("1743", "PARENTS PICK", WHITE), ("YOU · TODAY", "YOU PICK", GOLD)))
EP.overlay = overlay

FX = [(0.0, whoosh(.6, .02), -.2), (T_C0 + .8, thud(.25), 0), (cue("stakes", "money"), tick(.02), 0),
      (cue("but", "love") - .2, pop(.12), .2), (S("why") - .05, boom(.35), 0)] + EP.cut_fx(.06) + EP.shot_fx(whoosh(.25, .015))
if __name__ == "__main__": EP.run(FX)
