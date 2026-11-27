"""NOT JUST YOU – No. 166 (DOKU, new narration 27.11.2026): two weeks to Edinburgh. 1763: one stage coach a month,
12–14 days over ~400 miles of mud, nights at inns; 1784 John Palmer's mail coaches (fresh horses, armed guard); ~1830
day and night in under two days (All the Year Round vol. VI; Spectator 1829 'The North Mail'); then railway, telegraph,
phone. Mixed material: paintings, the mail-coach print on a desk with a typed card (always fully visible via fit()),
the Spectator study card, Edison's 'Fast Mail' train film (1897, illustrative), travel-time meter.
First 3 s: Paulsen's girl writing a letter, push-in, title TWO WEEKS · LONDON, 1763, meter LONDON TO EDINBURGH."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from doku import *
from board import Board, BoardInsert, VideoInsert, desk, fit, check_frame, insert_fx, title_card
from swiss import pop, tick, thud, whoosh, boom
from cute import Timeline
import cute; cute.LOUD = -14
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"cold": .2, "stakes": .85, "back": .25, "detail": .3, "but": .3, "so": .3, "turn": .3, "today": .85, "why": .25},
              pace="loose")
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["cold", "stakes", "back", "detail", "but", "so", "turn", "today", "why", "end"]
IMG = os.path.join(HERE, "img"); VID = os.path.join(HERE, "vid")
EP = DokuEpisode(TL, 166, "TWO WEEKS", order=ORDER, img_dir=IMG, credits=os.path.join(IMG, "credits.json"),
                 sources=("All the Year Round, vol. VI ·", "The Spectator, 11 July 1829"),
                 music=dict(bpm=66, root=9, prog="minor", audio="doku"),
                 cover=dict(words=["HOW LONG", "TO REACH", "YOUR LOVE?"], kicker="It's 1763."))

PAULSEN = "GIRL WRITING A LETTER · JULIUS PAULSEN · PUBLIC DOMAIN"
REEVE = "MAIL COACH IN A THUNDERSTORM · R. G. REEVE after J. POLLARD · 1827 · PUBLIC DOMAIN"
EP.shots = [
    Shot("cold", "letter", (.55, .32, 1.05), (.55, .28, 1.3), start=0, tag="", grade=(.95, .25, 0), credit=PAULSEN),
    Shot("cold", "edinburgh", (.30, .78, 1.0), (.45, .78, 1.05), start=cue("cold", "Edinburgh") - .25, tag="EDINBURGH", grade=(.95, .2, 0)),
    Shot("stakes", "reeve", (.25, .62, 1.3), (.30, .62, 1.45), tag="ONE COACH A MONTH", grade=(.9, .2, 0), credit=REEVE),
    Shot("back", "pollard", (.40, .55, 1.0), (.50, .55, 1.12), tag="400 MILES · MUD · INNS", grade=(.95, .2, 0)),
    Shot("detail", "reeve", (.55, .62, 1.2), (.68, .62, 1.35), tag="1784 · THE MAIL COACH", grade=(1.0, .2, 0), credit=REEVE),
    Shot("but", "edinburgh", (.55, .78, 1.05), (.75, .78, 1.1), tag="1830 · DAY AND NIGHT", grade=(1.0, .2, 0)),
    Shot("so", "pollard", (.55, .5, 1.1), (.60, .5, 1.25), tag="2 WEEKS, THEN 2 DAYS", grade=(1.0, .2, 0)),
    Shot("turn", "rocket", (.45, .5, 1.0), (.50, .5, 1.1), tag="1829 · THE RAILWAY", grade=(1.0, .15, .25)),
    Shot("turn", "telegraph", (.55, .5, 1.0), (.62, .5, 1.1), start=cue("turn", "telegraph") - .2, tag="THE TELEGRAPH", grade=(1.0, .15, .25)),
    Shot("turn", "phone", (.42, .55, 1.0), (.45, .52, 1.12), start=cue("turn", "phone") - .2, tag="THE PHONE", grade=(1.05, .1, 0)),
    Shot("today", "phone", (.45, .52, 1.12), (.47, .45, 1.35), tag="TODAY", grade=(1.1, .1, 0)),
    Shot("why", "letter", (.55, .30, 1.1), (.55, .30, 1.1), tag="1763 VS. TODAY", grade=(1.05, .25, 0), credit=PAULSEN),
]

# ---- cut-aways -------------------------------------------------------------------------------------------------
T_D0, T_D1 = cue("detail", "Put") - .1, E("detail") + .15                 # the mail-coach print + typed card on a desk
DK = Board(IMG, bg=desk(3600, 6000), size=(3600, 6000))
DK.photo("print", "reeve", 1800, 2700, 1500, -1, tilt=-1.5, sepia=.3)
DK.card("palmer", ["1784 · JOHN PALMER", "FAST MAIL COACHES", "FRESH HORSES · EVERY STAGE", "ARMED GUARD ON BOARD"], 2050, 3330, 1000,
        cue("detail", "Fresh") - T_D0 - .1, tilt=2,
        marks=[(2, "FRESH HORSES", cue("detail", "Fresh") - T_D0, cue("detail", "Fresh") - T_D0 + .5, "underline"),
               (3, "ARMED GUARD", cue("detail", "guard") - T_D0, cue("detail", "guard") - T_D0 + .5, "circle")], size=56)
for it in DK.items.values(): it.pin = False
DK.cam = [fit(DK, ["print"], 0, pad=60), fit(DK, ["print", "palmer"], cue("detail", "Fresh") - T_D0 + .3, pad=40), fit(DK, ["print", "palmer"], T_D1 - T_D0, pad=20)]
for tt in (0, T_D1 - T_D0): assert not check_frame(DK, tt, ["print"] + (["palmer"] if tt else [])), "desk items not fully visible"
EP.inserts = [
    (T_D0, T_D1, BoardInsert(DK), "1784 · MAIL COACH", REEVE),
    (cue("turn", "railway") - .15, cue("turn", "telegraph") - .25, VideoInsert(os.path.join(VID, "fastmail.mp4"), 22.5, 2.5, os.path.join(VID, "cache", "fm"),
     sepia=.4, crop="464:352:8:4"), "THE RAILWAY · FILM 1897", "FAST MAIL, NORTHERN PACIFIC R.R. · EDISON, 1897 · PUBLIC DOMAIN"),
]
EP.accent = {"cold": ["Edinburgh"], "stakes": ["two weeks", "once a month"], "back": ["muddy"], "detail": ["guard with a gun"],
             "but": ["two days"], "so": ["two weeks", "two days"], "turn": ["phone"], "today": ["before"], "why": ["Two weeks", "Two seconds"]}
EP.payoff = (S("why") + .1, 1.22)

num = lambda v: f"{v:,.0f}"
M = Meter([dict(t=S("stakes") + .05, to=14, dur=cue("stakes", "weeks") + .2 - S("stakes"), label="LONDON TO EDINBURGH", unit="DAYS BY COACH", fmt=num,
                stamp="ONCE A MONTH"),
           dict(t=cue("but", "two") - .2, to=2, dur=.9, label="1830 · MAIL COACH", unit="DAYS, DAY AND NIGHT", fmt=num),
           dict(t=cue("today", "arrives") - .2, to=2, dur=.01, tween=False, label="TODAY", unit="SECONDS", fmt=num, gold=True)],
          t_hide=S("why") - .05)
EP.counter_list = M.counters()

def overlay(img, d, t):
    if t < 3.0: title_card(img, t, .25, 2.9, "TWO WEEKS", "LONDON · 1763", 250)
    if not (S("back") - .1 <= t < S("but") - .1 or S("so") - .1 <= t < S("today") - .1): M.draw(img, d, t)   # free for desk, card, film
    paper_card(img, t, S("so") + .05, E("so") + .2, "THE SPECTATOR · 11 JULY 1829", "The North Mail", "North Mail",
               (cue("so", "shrank") - .2, cue("so", "shrank") + .3), foot="LONDON TO EDINBURGH IN ABOUT 43 HOURS", y=380)
    compare(img, d, t, S("why") - .05, (("1763 · BY COACH", "14 DAYS", WHITE), ("YOU · TODAY", "2 SEC", GOLD)))
EP.overlay = overlay

FX = [(cue("stakes", "weeks") + .25, thud(.25), 0), (cue("back", "horses") - .05, tick(.01), -.2), (cue("back", "inn") - .05, tick(.01), .2),
      (cue("but", "two") + .7, thud(.22), 0), (cue("so", "shrank") - .1, whoosh(.3, .012), 0), (cue("cold", "love") - .05, tick(.01), .2),
      (cue("detail", "idea") - .05, tick(.01), -.2), (cue("but", "day and night") - .05, tick(.01), .2), (cue("why", "Two seconds") - .05, pop(.08), .2), (cue("today", "arrives") - .2, pop(.12), .2),
      (S("why") - .05, boom(.35), 0)] + EP.cut_fx(.06) + EP.shot_fx(whoosh(.25, .015)) + insert_fx(EP.inserts)
if __name__ == "__main__": EP.run(FX)
