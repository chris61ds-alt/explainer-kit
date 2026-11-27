"""NOT JUST YOU – No. 165 (DOKU, new narration 27.11.2026): wash day. Monday 1900, Anna (illustrative) does the laundry,
the whole day: ~50 gallons of water per load carried by hand; per year ~150 miles walked and 36 tons of water carried
(Strasser 1982 via Digital History, UH); Tuesday ironing with irons heated on the stove. Mixed material: Lumière film of
washerwomen (1897, illustrative), photo, paintings (Millet, Degas), soap ad, the 1920 washer ad on a desk with a red
underline, the 'Never Done' study card, the water meter. Board elements framed with fit() (always fully visible).
First 3 s: Lumière washerwomen film, title WASH DAY · MONDAY, 1900."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from doku import *
from board import Board, BoardInsert, VideoInsert, desk, fit, check_frame, insert_fx, title_card
from swiss import pop, tick, thud, whoosh, boom
from cute import Timeline
import cute; cute.LOUD = -14
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"cold": .2, "stakes": .85, "back": .2, "detail": .3, "but": .3, "so": .2, "turn": .3, "today": .85, "why": .25},
              pace="loose")
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["cold", "stakes", "back", "detail", "but", "so", "turn", "today", "why", "end"]
IMG = os.path.join(HERE, "img"); VID = os.path.join(HERE, "vid")
EP = DokuEpisode(TL, 165, "WASH DAY", order=ORDER, img_dir=IMG, credits=os.path.join(IMG, "credits.json"),
                 sources=("Strasser (1982), Never Done ·", "via Digital History, Univ. of Houston"),
                 music=dict(bpm=68, root=7, prog="minor", audio="doku"),
                 cover=dict(words=["ONE LOAD OF", "LAUNDRY TOOK", "HOW LONG?"], kicker="Monday, 1900."))
FILM = "LAVEUSES SUR LA RIVIÈRE · LUMIÈRE, 1897 · PUBLIC DOMAIN"
EP.shots = [
    Shot("cold", "veranda", (.5, .55, 1.0), (.5, .55, 1.0), start=0, tag=""),                              # under the film
    Shot("cold", "veranda", (.5, .50, 1.05), (.5, .55, 1.2), start=cue("cold", "Today") - .2, tag="MONDAY · 1900", grade=(.95, .2, .3)),
    Shot("stakes", "veranda", (.5, .55, 1.2), (.48, .62, 1.5), tag="QUEENSLAND · c. 1903", grade=(.95, .2, .3)),
    Shot("back", "millet", (.45, .5, 1.0), (.50, .48, 1.15), tag="HAUL", grade=(1.0, .25, 0)),
    Shot("back", "soapad", (.20, .55, 1.0), (.30, .55, 1.08), start=cue("back", "Heats") - .1, tag="HEAT · SCRUB", grade=(.9, .2, 0)),
    Shot("back", "veranda", (.48, .62, 1.6), (.48, .60, 1.9), start=cue("back", "Boils") - .1, tag="BOIL · WRING · HANG", grade=(.95, .2, .3)),
    Shot("detail", "millet", (.50, .48, 1.15), (.45, .52, 1.4), tag="CARRY · CARRY · CARRY", grade=(1.0, .25, 0)),
    Shot("but", "degas", (.45, .62, 1.6), (.43, .58, 2.1), tag="TUESDAY · IRONING DAY", grade=(.95, .25, 0)),
    Shot("so", "degas2", (.35, .55, 1.4), (.35, .50, 1.6), tag="EVERY SINGLE WEEK", grade=(.95, .25, 0)),
    Shot("turn", "washer1920", (.30, .45, 1.0), (.33, .42, 1.15), tag="1920 · ELECTRIC WASHER", grade=(1.05, .1, .3)),
    Shot("today", "modern", (.5, .55, 1.0), (.5, .60, 1.25), tag="TODAY", grade=(1.1, .05, 0)),
    Shot("why", "veranda", (.48, .60, 1.5), (.5, .55, 1.0), tag="1900 VS. TODAY", grade=(1.0, .2, .3)),
]

# ---- cut-aways -------------------------------------------------------------------------------------------------
T_W0, T_W1 = cue("turn", "Electricity") - .1, E("turn") + .15            # the 1920 washer ad on a desk, red underline
AD = Board(IMG, bg=desk(2800, 4400), size=(2800, 4400))
AD.photo("ad", "washer1920", 1400, 2200, 1500, -1, tilt=1.2, sepia=.25, crop=(.49, .03, .99, .63),   # text column only -> readable AND whole
         marks=[("underline", (.506, .528, .956, .572), cue("turn", "washing") - T_W0, cue("turn", "washing") - T_W0 + .5),
                ("underline", (.506, .575, .62, .612), cue("turn", "machine") - T_W0, cue("turn", "machine") - T_W0 + .3)])
AD.items["ad"].pin = False
a_ = AD.items["ad"]; ux, uy = a_.x - a_.w / 2 + .73 * a_.w, a_.y - a_.h / 2 + .56 * a_.h
c0 = fit(AD, ["ad"], 0)
AD.cam = [fit(AD, ["ad"], 0, pad=140), fit(AD, ["ad"], T_W1 - T_W0, pad=40)]                 # slow push, ad always complete
assert not check_frame(AD, 0, ["ad"]), "washer ad not fully visible"
EP.inserts = [
    (0.0, cue("cold", "Today") - .1, VideoInsert(os.path.join(VID, "laveuses.mp4"), 4, 5, os.path.join(VID, "cache", "lav0c"), sepia=.5, crop="476:350:84:5"),
     None, FILM),
    (cue("back", "Scrubs") - .1, cue("back", "Boils") - .1, VideoInsert(os.path.join(VID, "laveuses.mp4"), 20, 3, os.path.join(VID, "cache", "lav20c"),
     sepia=.5, z=(1.0, 1.1), crop="476:350:84:5"), "SCRUB · ILLUSTRATIVE · 1897", FILM),
    (T_W0, T_W1, BoardInsert(AD), "1920 · NEWSPAPER AD", "ELECTRIC WASHER AD · SEATTLE ELECTRIC WASHER CO. · 1920 · PUBLIC DOMAIN"),
]
EP.accent = {"cold": ["wash day", "whole day"], "stakes": ["fifty gallons"], "back": ["Boils"], "detail": ["thirty-six tons"],
             "but": ["ironing day"], "so": ["Monday", "Tuesday"], "turn": ["washing machine"], "today": ["one button"], "why": ["whole day", "one button"]}
EP.payoff = (S("why") + .1, 1.2)

num = lambda v: f"{v:,.0f}"
M = Meter([dict(t=S("stakes") + .1, to=50, dur=cue("stakes", "gallons") + .2 - S("stakes"), label="ONE LOAD OF LAUNDRY", unit="GALLONS OF WATER", fmt=num,
                stamp="ABOUT 190 LITRES"),
           dict(t=cue("detail", "hundred") - .2, to=150, dur=.8, label="IN ONE YEAR", unit="MILES WALKED, CARRYING WATER", fmt=num),
           dict(t=cue("detail", "thirty") - .2, to=36, dur=.01, tween=False, label="IN ONE YEAR", unit="TONS OF WATER, CARRIED", fmt=num),
           dict(t=cue("today", "button") - .2, to=1, dur=.01, tween=False, label="TODAY", unit="BUTTON", fmt=num, gold=True)],
          t_hide=S("why") - .05)
EP.counter_list = M.counters()

def overlay(img, d, t):
    if t < 3.0: title_card(img, t, .25, 2.9, "WASH DAY", "MONDAY · 1900 · (FILM: 1897, ILLUSTRATIVE)", 250)
    if not (S("back") - .1 <= t < S("detail") - .1 or S("but") - .1 <= t < S("today") - .1): M.draw(img, d, t)   # free for pictures, card, ad
    paper_card(img, t, S("so") + .1, E("so") + .15, "BOOK · 1982", "Never Done: A History of American Housework", "Never Done",
               (cue("so", "same") - .1, cue("so", "same") + .4), foot="SUSAN STRASSER · PANTHEON BOOKS", y=380)
    compare(img, d, t, S("why") - .05, (("ANNA · 1900", "1 DAY", WHITE), ("YOU · TODAY", "1 BUTTON", GOLD)))
EP.overlay = overlay

FX = [(cue("stakes", "gallons") + .25, thud(.25), 0), (cue("back", "hauls") - .05, tick(.01), -.2), (cue("back", "Heats") - .05, tick(.01), .2),
      (cue("back", "Wrings") - .05, tick(.01), -.2), (cue("detail", "thirty") - .2, thud(.3), 0), (cue("but", "irons") - .05, thud(.2), 0),
      (cue("so", "Monday") - .05, tick(.012), -.2), (cue("so", "Tuesday") - .05, tick(.012), .2), (cue("today", "button") - .2, pop(.12), .2),
      (S("why") - .05, boom(.35), 0)] + EP.cut_fx(.06) + EP.shot_fx(whoosh(.25, .015)) + insert_fx(EP.inserts)
if __name__ == "__main__": EP.run(FX)
