"""NOT JUST YOU – No. 168 (DOKU, 26.11.2026): the cowpox bet. May 1796 Edward Jenner inoculated 8-year-old James Phipps
with cowpox from milkmaid Sarah Nelmes, two months later exposed him to smallpox – he stayed healthy (WHO). Smallpox
killed ~3 in 10 infected (NIAID); vaccination from Latin vacca; declared eradicated 1980 (WHO, OWID). Gold element
(rule 12, doku): one counter – the boy's age 0 → 8, then 3 IN 10 died, then 0 for the boy, then the year 1796 → 1980.
First 3 s (Chris OK 26.11.): Hillemacher's painting of Jenner vaccinating a boy, camera on the arm from frame 0,
tag ENGLAND · 1796, counter THE BOY · AGE 0 → 8."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from doku import *
from swiss import pop, tick, thud, whoosh, boom
from cute import Timeline
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"cold": .35, "stakes": .85, "back": .4, "but": .6, "so": .4, "turn": .5, "today": .85, "why": .2}, pace="loose")
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["cold", "stakes", "back", "but", "so", "turn", "today", "why", "end"]
EP = DokuEpisode(TL, 168, "THE COWPOX BET", order=ORDER, img_dir=os.path.join(HERE, "img"), credits=os.path.join(HERE, "img", "credits.json"),
                 sources=("WHO, History of smallpox vaccination ·", "Our World in Data"),
                 music=dict(bpm=82, root=0, prog="minor", kick="half", audio="v5"),
                 cover=dict(words=["WHY IS IT", "CALLED", "A VACCINE?"], kicker="It's 1796."))

HILLE = "EDWARD JENNER VACCINATING A BOY · E.-E. HILLEMACHER · WELLCOME COLLECTION · CC BY 4.0"
EP.shots = [
    Shot("cold", "hille", (.56, .44, 2.0), (.56, .42, 2.5), start=0, tag="ENGLAND · 1796", grade=(1.0, .25, 0), flicker=.5, credit=HILLE),
    Shot("cold", "hille", (.40, .40, 1.7), (.40, .38, 2.0), start=cue("cold", "milkmaid") - .2, tag="ENGLAND · 1796", grade=(1.0, .25, 0), flicker=.5, credit=HILLE),
    Shot("stakes", "melingue", (.45, .38, 1.5), (.45, .36, 1.8), tag="ON PURPOSE", grade=(.95, .2, 0),
         credit="JENNER PERFORMING HIS FIRST VACCINATION · GASTON MÉLINGUE · 1879 · PUBLIC DOMAIN"),
    Shot("back", "hille", (.30, .55, 1.1), (.40, .55, 1.2), tag="SMALLPOX", grade=(.7, .25, .3), credit=HILLE),
    Shot("but", "jenner", (.5, .30, 1.15), (.5, .27, 1.35), tag="DR. EDWARD JENNER", grade=(1.0, .2, .2),
         credit="PORTRAIT OF EDWARD JENNER · WELLCOME COLLECTION · CC BY 4.0"),
    Shot("so", "patients", (.35, .55, 1.0), (.55, .55, 1.08), tag="VACCA = COW", grade=(1.0, .2, 0),
         credit="THE COW-POCK · JAMES GILLRAY · 1802 · WELLCOME COLLECTION · CC BY 4.0"),
    Shot("so", "patients", (.62, .45, 1.6), (.66, .42, 1.85), start=cue("so", "vacca") - .2, tag="VACCA = COW", grade=(1.0, .2, 0),
         credit="THE COW-POCK · JAMES GILLRAY · 1802 · WELLCOME COLLECTION · CC BY 4.0"),
    Shot("turn", "needle", (.5, .45, 1.0), (.5, .40, 1.15), tag="THE WORLD VACCINATES", grade=(1.05, .05, 0),
         credit="SMALLPOX VACCINATION NEEDLE · JAMES GATHANY / CDC · PUBLIC DOMAIN"),
    Shot("today", "vaccine", (.62, .5, 1.0), (.62, .45, 1.15), tag="1980 · ERADICATED", grade=(1.1, .05, 0),
         credit="SMALLPOX VACCINE · JAMES GATHANY / CDC · PUBLIC DOMAIN"),
    Shot("why", "hille", (.50, .45, 1.3), (.50, .45, 1.3), tag="ONE BOY", grade=(1.1, .25, 0), flicker=.4, credit=HILLE),
]
EP.accent = {"cold": ["one boy"], "stakes": ["on purpose"], "back": ["three ten"], "but": ["never sick"],
             "so": ["vaccination vacca cow"], "turn": ["vaccinated"], "today": ["nineteen eighty gone"], "why": ["one boy cow"]}
EP.payoff = (S("why") + .1, 1.22)

num = lambda v: f"{v:,.0f}"
year = lambda v: f"{v:.0f}"
T_C0 = 1.4
M = Meter([dict(t=T_C0, to=8, dur=1.4, label="THE BOY · AGE", unit="YEARS OLD", fmt=num),
           dict(t=cue("back", "three") - .2, to=3, dur=.01, tween=False, label="SMALLPOX · OUT OF 10 INFECTED", unit="DIED", fmt=num),
           dict(t=cue("but", "never") - .2, to=0, dur=.01, tween=False, label="THE BOY", unit="TIMES SICK", fmt=num, stamp="PROTECTED"),
           dict(t=S("turn") - .05, from_=1796, to=1796, dur=.01, tween=False, label="YEAR", unit="", fmt=year),
           dict(t=S("turn") + .3, to=1980, dur=cue("today", "eighty") + .2 - S("turn") - .3, label="YEAR", unit="SMALLPOX: GONE", fmt=year, gold=True)],
          t_hide=S("why") - .05)
EP.counter_list = [(T_C0, 1.4, 8)]

def overlay(img, d, t):
    M.draw(img, d, t)
    compare(img, d, t, S("why") - .05, (("1796", "ONE BOY", WHITE), ("1980", "ERADICATED", GOLD)))
EP.overlay = overlay

FX = [(0.0, whoosh(.6, .02), -.2), (T_C0, tick(.012), -.3), (cue("stakes", "purpose"), thud(.25), 0),
      (cue("but", "never") - .2, pop(.1), .2), (cue("today", "eighty") + .25, thud(.3), 0),
      (S("why") - .05, boom(.35), 0)] + EP.cut_fx(.06) + EP.shot_fx(whoosh(.25, .015))
if __name__ == "__main__": EP.run(FX)
