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
import cute; cute.LOUD = -14
from board import Board, BoardInsert, desk, fit, check_frame, insert_fx, title_card
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"cold": .2, "stakes": .85, "back": .25, "detail": .3, "but": .3, "so": .3, "turn": .3, "today": .85, "why": .25},
              pace="loose")
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["cold", "stakes", "back", "detail", "but", "so", "turn", "today", "why", "end"]
EP = DokuEpisode(TL, 168, "THE COWPOX BET", order=ORDER, img_dir=os.path.join(HERE, "img"), credits=os.path.join(HERE, "img", "credits.json"),
                 sources=("WHO, History of smallpox vaccination ·", "Our World in Data"),
                 music=dict(bpm=66, root=4, prog="minor", audio="doku"),
                 cover=dict(words=["WHY IS IT", "CALLED", "A VACCINE?"], kicker="It's 1796."))

HILLE = "EDWARD JENNER VACCINATING A BOY · E.-E. HILLEMACHER · WELLCOME COLLECTION · CC BY 4.0"
EP.shots = [
    Shot("cold", "hille", (.56, .44, 2.0), (.56, .42, 2.5), start=0, tag="", grade=(1.0, .25, 0), flicker=.5, credit=HILLE),
    Shot("cold", "hille", (.40, .40, 1.7), (.40, .38, 2.0), start=cue("cold", "milkmaid") - .2, tag="ENGLAND · 1796", grade=(1.0, .25, 0), flicker=.5, credit=HILLE),
    Shot("stakes", "melingue", (.45, .38, 1.5), (.45, .36, 1.8), tag="ON PURPOSE", grade=(.95, .2, 0),
         credit="JENNER PERFORMING HIS FIRST VACCINATION · GASTON MÉLINGUE · 1879 · PUBLIC DOMAIN"),
    Shot("back", "hille", (.30, .55, 1.1), (.40, .55, 1.2), tag="SMALLPOX", grade=(.7, .25, .3), credit=HILLE),
    Shot("detail", "jenner", (.5, .30, 1.15), (.5, .27, 1.35), tag="DR. EDWARD JENNER", grade=(1.0, .2, .2),
         credit="PORTRAIT OF EDWARD JENNER · WELLCOME COLLECTION · CC BY 4.0"),
    Shot("but", "hille", (.50, .45, 1.4), (.45, .40, 1.8), tag="JAMES PHIPPS, 8", grade=(1.0, .25, 0), credit=HILLE),
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
EP.accent = {"cold": ["eight-year-old boy"], "stakes": ["On purpose"], "back": ["three in ten"], "detail": ["never got smallpox"],
             "but": ["never got sick"], "so": ["growing cows", "vacca"], "turn": ["vaccinated"], "today": ["gone"], "why": ["one boy", "Blossom"]}

# ---- cut-away: Gillray's 1802 cartoon on a desk, red circle around a cow growing out of a face -----------------------
T_G0, T_G1 = cue("so", "famous") - .15, cue("so", "But the name") - .1
GB = Board(os.path.join(HERE, "img"), bg=desk(3600, 6000), size=(3600, 6000))
GB.photo("cart", "gillray", 1800, 3000, 1700, -1, tilt=-1.2, sepia=.1,
         marks=[("circle", (.565, .15, .655, .30), cue("so", "growing") - T_G0, cue("so", "growing") - T_G0 + .6)])
GB.items["cart"].pin = False
GB.cam = [fit(GB, ["cart"], 0, pad=80), fit(GB, ["cart"], T_G1 - T_G0, pad=10)]
for tt in (0, T_G1 - T_G0): assert not check_frame(GB, tt, ["cart"]), "cartoon not fully visible"
EP.inserts = [(T_G0, T_G1, BoardInsert(GB), "1802 · THE COW-POCK", "THE COW-POCK · JAMES GILLRAY · 1802 · PUBLIC DOMAIN")]
EP.payoff = (S("why") + .1, 1.22)

num = lambda v: f"{v:,.0f}"
year = lambda v: f"{v:.0f}"
T_C0 = cue("cold", "eight") - .3
M = Meter([dict(t=T_C0, to=8, dur=1.4, label="THE BOY · AGE", unit="YEARS OLD", fmt=num),
           dict(t=cue("back", "three") - .2, to=3, dur=.01, tween=False, label="SMALLPOX · OUT OF 10 INFECTED", unit="DIED", fmt=num),
           dict(t=cue("but", "never") - .2, to=0, dur=.01, tween=False, label="THE BOY", unit="TIMES SICK", fmt=num, stamp="PROTECTED"),
           dict(t=S("turn") - .05, from_=1796, to=1796, dur=.01, tween=False, label="YEAR", unit="", fmt=year),
           dict(t=S("turn") + .3, to=1980, dur=cue("today", "eighty") + .2 - S("turn") - .3, label="YEAR", unit="SMALLPOX: GONE", fmt=year, gold=True)],
          t_hide=S("why") - .05)
EP.counter_list = [(T_C0, 1.4, 8)]

def overlay(img, d, t):
    if t < 3.0: title_card(img, t, .25, 2.9, "ONE BOY", "ENGLAND · 1796", 250)
    if not (S("detail") - .1 <= t < S("but") - .1 or T_G0 - .2 <= t < T_G1 + .2): M.draw(img, d, t)   # free for the book card and the cartoon
    paper_card(img, t, S("detail") + .3, E("detail") + .15, "BOOK · EDWARD JENNER · 1798",
               "An Inquiry into the Causes and Effects of the Variolae Vaccinae", "Variolae Vaccinae",
               (cue("detail", "cowpox") - .1, cue("detail", "cowpox") + .5), foot="THE COWPOX STUDY", y=380)
    compare(img, d, t, S("why") - .05, (("1796", "ONE BOY", WHITE), ("1980", "ERADICATED", GOLD)))
EP.overlay = overlay

FX = [(T_C0, tick(.012), -.3), (cue("stakes", "purpose"), thud(.25), 0), (cue("back", "blind") - .05, thud(.2), 0),
      (cue("detail", "milkmaids") - .05, tick(.01), .2), (cue("so", "scared") - .05, tick(.01), -.2), (cue("why", "Blossom") - .05, pop(.08), .2),
      (cue("but", "never") - .2, pop(.1), .2), (cue("today", "eighty") + .25, thud(.3), 0),
      (S("why") - .05, boom(.35), 0)] + EP.cut_fx(.06) + EP.shot_fx(whoosh(.25, .015)) + insert_fx(EP.inserts)
if __name__ == "__main__": EP.run(FX)
