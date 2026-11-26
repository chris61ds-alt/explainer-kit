"""NOT JUST YOU – No. 164 (DOKU, 26.11.2026): why nobody smiled in old photos. 1840: hold still for a full minute
(early daguerreotypes 60–90 s; after ~1845 a few seconds – Mental Floss; Getty 2023). People stayed serious anyway:
a photo was rare, expensive, forever. Today < 1/100 s. Gold element (rule 12, doku): the HOLD STILL counter in
seconds, 0 → 60 → 90 → 3 → 1/100. First 3 s (Chris OK 26.11.): daguerreotype portrait, camera on the eyes from frame 0,
tag 1840, counter HOLD STILL 0 → 60 s."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from doku import *
from swiss import pop, tick, thud, whoosh, boom
from cute import Timeline
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"cold": .35, "stakes": .85, "back": .4, "but": .6, "so": .4, "turn": .5, "today": .85, "why": .2}, pace="loose")
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["cold", "stakes", "back", "but", "so", "turn", "today", "why", "end"]
EP = DokuEpisode(TL, 164, "HOLD STILL", order=ORDER, img_dir=os.path.join(HERE, "img"), credits=os.path.join(HERE, "img", "credits.json"),
                 sources=("Getty Museum (2023), Say Prunes! ·", "Mental Floss, Daguerreotype Q&A"),
                 music=dict(bpm=84, root=5, prog="minor", kick="half", audio="v5"),
                 cover=dict(words=["WHY DID NOBODY", "SMILE IN", "OLD PHOTOS?"], kicker="It's 1840."))

EP.shots = [
    Shot("cold", "man", (.47, .36, 1.7), (.47, .33, 2.3), start=0, tag="1840 · YOUR FIRST PHOTO", grade=(.95, .15, 0),
         credit="PORTRAIT OF A MAN · DAGUERREOTYPE · FINNISH MUSEUM OF PHOTOGRAPHY · NO RESTRICTIONS"),
    Shot("stakes", "man", (.47, .33, 2.3), (.47, .31, 2.6), tag="DON'T BLINK", grade=(.95, .15, 0), ghost=1.6,
         credit="PORTRAIT OF A MAN · DAGUERREOTYPE · FINNISH MUSEUM OF PHOTOGRAPHY · NO RESTRICTIONS"),
    Shot("back", "boulevard", (.20, .5, 1.0), (.55, .5, 1.1), tag="PARIS · 1838", grade=(.9, .1, .4),
         credit="BOULEVARD DU TEMPLE · LOUIS DAGUERRE · PUBLIC DOMAIN"),
    Shot("but", "woman", (.50, .30, 1.45), (.50, .27, 1.75), tag="c. 1850 · A FEW SECONDS", grade=(1.0, .15, 0),
         credit="UNIDENTIFIED WOMAN · SOUTHWORTH & HAWES · c. 1850 · PUBLIC DOMAIN"),
    Shot("so", "family", (.72, .45, 1.6), (.72, .42, 2.0), tag="RARE · EXPENSIVE · FOREVER", grade=(.95, .2, 0),
         credit="PORTRAIT OF A FAMILY · DAGUERREOTYPE · FINNISH MUSEUM OF PHOTOGRAPHY · NO RESTRICTIONS"),
    Shot("so", "family", (.62, .62, 2.2), (.62, .60, 2.6), start=cue("so", "rare") - .15, tag="RARE · EXPENSIVE · FOREVER", grade=(.95, .2, 0),
         credit="PORTRAIT OF A FAMILY · DAGUERREOTYPE · FINNISH MUSEUM OF PHOTOGRAPHY · NO RESTRICTIONS"),
    Shot("turn", "brownie", (.5, .30, 1.0), (.5, .26, 1.15), tag="1905 · THE BROWNIE", grade=(1.0, .1, 0),
         credit="BROWNIE CAMERA ADVERT (1905) · KODAK · PUBLIC DOMAIN"),
    Shot("turn", "phone", (.42, .55, 1.0), (.45, .52, 1.12), start=cue("turn", "phones") - .2, tag="TODAY", grade=(1.05, .1, 0),
         credit="WOMAN HOLDING CELL PHONE · LUISELLA PLANETA · CC0"),
    Shot("today", "phone", (.45, .52, 1.12), (.47, .50, 1.3), tag="TODAY", grade=(1.1, .1, 0),
         credit="WOMAN HOLDING CELL PHONE · LUISELLA PLANETA · CC0"),
    Shot("why", "woman", (.50, .30, 1.3), (.50, .30, 1.3), tag="1840 VS. TODAY", grade=(1.05, .15, 0),
         credit="UNIDENTIFIED WOMAN · SOUTHWORTH & HAWES · c. 1850 · PUBLIC DOMAIN"),
]
EP.accent = {"cold": ["eighteen forty full minute"], "stakes": ["blur"], "back": ["ninety seconds"], "but": ["few seconds"],
             "so": ["rare expensive forever"], "turn": ["phones"], "today": ["hundredth second"], "why": ["full minute blink"]}
EP.payoff = (S("why") + .1, 1.22)

def secs(v):
    if v >= .95: return f"{v:.0f} s"
    return "1/100 s" if v <= .0105 else f"{v:.2f} s"
T_C0 = 1.4
M = Meter([dict(t=T_C0, to=60, dur=cue("cold", "minute") - T_C0, label="HOLD STILL FOR", unit="SECONDS", fmt=secs, stamp="DON'T MOVE"),
           dict(t=cue("back", "ninety") - .2, to=90, dur=.8, label="EARLY CAMERAS · UP TO", unit="SECONDS", fmt=secs),
           dict(t=cue("but", "few") - .2, to=3, dur=.8, label="BY THE 1850s", unit="SECONDS", fmt=secs),
           dict(t=cue("today", "hundredth") - .2, to=.01, dur=1.0, label="TODAY", unit="OF A SECOND", fmt=secs, gold=True)],
          t_hide=S("why") - .05)
EP.counter_list = M.counters()

def overlay(img, d, t):
    M.draw(img, d, t)
    compare(img, d, t, S("why") - .05, (("1840 · HOLD STILL", "60 SEC", WHITE), ("YOU · TODAY", "1/100 SEC", GOLD)))
EP.overlay = overlay

FX = [(0.0, whoosh(.6, .02), -.2), (T_C0, tick(.012), -.3), (cue("cold", "minute") + .1, thud(.25), 0),
      (cue("stakes", "blur") - .1, whoosh(.5, .02), 0), (cue("today", "hundredth") + .8, pop(.1), .2),
      (S("why") - .05, boom(.35), 0)] + EP.cut_fx(.06) + EP.shot_fx(whoosh(.25, .015))
if __name__ == "__main__": EP.run(FX)
