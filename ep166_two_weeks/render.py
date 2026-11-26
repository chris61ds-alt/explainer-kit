"""NOT JUST YOU – No. 166 (DOKU, 26.11.2026): two weeks to Edinburgh. 1763: one stage coach a month London ↔ Edinburgh,
12–14 days; ~1830: several a day, about 48 h (All the Year Round, vol. VI); 1829 North Mail ≈ 43.5 h (Spectator).
Today: a message in seconds. The lovers are illustrative. Gold element (rule 12, doku): the travel-time counter
0 → 14 days → 2 days → 2 seconds. First 3 s (Chris OK 26.11.): a painting of a girl writing a letter, camera pushes in
from frame 0, tag LONDON · 1763, counter LONDON → EDINBURGH 0 → 14 days."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from doku import *
from swiss import pop, tick, thud, whoosh, boom
from cute import Timeline
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"cold": .35, "stakes": .85, "back": .4, "but": .6, "so": .4, "turn": .5, "today": .85, "why": .2}, pace="loose")
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["cold", "stakes", "back", "but", "so", "turn", "today", "why", "end"]
EP = DokuEpisode(TL, 166, "TWO WEEKS", order=ORDER, img_dir=os.path.join(HERE, "img"), credits=os.path.join(HERE, "img", "credits.json"),
                 sources=("All the Year Round, vol. VI ·", "The Spectator, 11 July 1829"),
                 music=dict(bpm=76, root=9, prog="minor", kick="half", audio="v5"),
                 cover=dict(words=["HOW LONG", "TO REACH", "YOUR LOVE?"], kicker="It's 1763."))

PAULSEN = "GIRL WRITING A LETTER · JULIUS PAULSEN · PUBLIC DOMAIN"
REEVE = "MAIL COACH IN A THUNDERSTORM · R. G. REEVE after J. POLLARD · 1827 · PUBLIC DOMAIN"
EP.shots = [
    Shot("cold", "letter", (.55, .32, 1.05), (.55, .28, 1.3), start=0, tag="LONDON · 1763", grade=(.95, .25, 0), credit=PAULSEN),
    Shot("cold", "edinburgh", (.30, .78, 1.0), (.45, .78, 1.05), start=cue("cold", "Edinburgh") - .25, tag="EDINBURGH", grade=(.95, .2, 0),
         credit="A VIEW OF EDINBURGH FROM THE SOUTH · SAMUEL SCOTT · PUBLIC DOMAIN"),
    Shot("stakes", "reeve", (.25, .62, 1.3), (.30, .62, 1.45), tag="ONE COACH A MONTH", grade=(.9, .2, 0), credit=REEVE),
    Shot("back", "pollard", (.40, .55, 1.0), (.50, .55, 1.12), tag="MUD · INNS · 12–14 DAYS", grade=(.95, .2, 0),
         credit="THE MAIL COACH IN A THUNDERSTORM · JAMES POLLARD · PUBLIC DOMAIN"),
    Shot("but", "reeve", (.55, .62, 1.2), (.68, .62, 1.35), tag="1830 · DAY AND NIGHT", grade=(1.0, .2, 0), credit=REEVE),
    Shot("so", "edinburgh", (.55, .78, 1.05), (.75, .78, 1.1), tag="2 WEEKS, THEN 2 DAYS", grade=(1.0, .2, 0),
         credit="A VIEW OF EDINBURGH FROM THE SOUTH · SAMUEL SCOTT · PUBLIC DOMAIN"),
    Shot("turn", "rocket", (.45, .5, 1.0), (.50, .5, 1.1), tag="1829 · THE RAILWAY", grade=(1.0, .15, .25),
         credit="STEPHENSON'S ROCKET (REPLICA) · GARY LEE TODD · CC0"),
    Shot("turn", "telegraph", (.55, .5, 1.0), (.62, .5, 1.1), start=cue("turn", "telegraph") - .2, tag="THE TELEGRAPH", grade=(1.0, .15, .3),
         credit="POST AND TELEGRAPH OFFICE, THAMES NZ · NATIONAL LIBRARY NZ · NO RESTRICTIONS"),
    Shot("turn", "phone", (.42, .55, 1.0), (.45, .52, 1.12), start=cue("turn", "phone") - .2, tag="THE PHONE", grade=(1.05, .1, 0),
         credit="WOMAN HOLDING CELL PHONE · LUISELLA PLANETA · CC0"),
    Shot("today", "phone", (.45, .52, 1.12), (.47, .45, 1.35), tag="TODAY", grade=(1.1, .1, 0),
         credit="WOMAN HOLDING CELL PHONE · LUISELLA PLANETA · CC0"),
    Shot("why", "letter", (.55, .30, 1.1), (.55, .30, 1.1), tag="1763 VS. TODAY", grade=(1.05, .25, 0), credit=PAULSEN),
]
EP.accent = {"cold": ["two weeks"], "stakes": ["once month"], "back": ["muddy"], "but": ["two days"],
             "so": ["two weeks two days"], "turn": ["phone"], "today": ["before"], "why": ["two weeks two seconds"]}
EP.payoff = (S("why") + .1, 1.22)

num = lambda v: f"{v:,.0f}"
T_C0 = 1.4
M = Meter([dict(t=T_C0, to=14, dur=cue("cold", "weeks") + .2 - T_C0, label="LONDON TO EDINBURGH", unit="DAYS BY COACH", fmt=num,
                stamp="ONCE A MONTH"),
           dict(t=cue("but", "two") - .2, to=2, dur=.9, label="1830 · MAIL COACH", unit="DAYS, DAY AND NIGHT", fmt=num),
           dict(t=cue("today", "arrives") - .2, to=2, dur=.01, tween=False, label="TODAY", unit="SECONDS", fmt=num, gold=True)],
          t_hide=S("why") - .05)
EP.counter_list = M.counters()

def overlay(img, d, t):
    M.draw(img, d, t)
    compare(img, d, t, S("why") - .05, (("1763 · BY COACH", "14 DAYS", WHITE), ("YOU · TODAY", "2 SEC", GOLD)))
EP.overlay = overlay

FX = [(0.0, whoosh(.6, .02), -.2), (T_C0, tick(.012), -.3), (cue("cold", "weeks") + .25, thud(.25), 0),
      (cue("but", "two") + .7, thud(.22), 0), (cue("today", "arrives") - .2, pop(.12), .2),
      (S("why") - .05, boom(.35), 0)] + EP.cut_fx(.06) + EP.shot_fx(whoosh(.25, .015))
if __name__ == "__main__": EP.run(FX)
