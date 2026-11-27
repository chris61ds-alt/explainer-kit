"""NOT JUST YOU – No. 175 (BOARD, first evidence-board episode, 26.11.2026): the Mary Celeste. Found adrift 4 Dec 1872
near the Azores, seaworthy, six months of food, lifeboat gone, 10 people missing, never found. Boston Post 1873 clipping
('seized by pirates', public domain), Conan Doyle's 1884 fiction, Gibraltar inquiry: no foul play. Ending stays open.
Voice: Kyutai Pocket TTS alba. Look after Chris' Dyatlov reference: one board, one continuous camera, red strings.
First 3 s: the ship painting is already on the board at frame 0, camera pushes in and drifts right, serif title
THE GHOST SHIP · ATLANTIC 1872, the FOUND ADRIFT card slaps on with paper + pin sound at 'drifts'."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from board import *
from cute import Timeline
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"cold": .15, "stakes": .85, "back": .1, "clues": .1, "but": .2, "log": .1, "cargo": .2,
                                    "myth": .1, "doyle": .2, "so": .15, "turn": .15, "today": .85, "why": .3}, pace="loose")
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["cold", "stakes", "back", "clues", "but", "log", "cargo", "myth", "doyle", "so", "turn", "today", "why", "end"]
IMG = os.path.join(HERE, "img")
B = Board(IMG, size=(2400, 5700))
PD = "PUBLIC DOMAIN"

# ---- the board (x, y = centre in board px) ------------------------------------------------------------------------
B.photo("ship", "ship", 900, 700, 1100, -.4, tilt=-2, label="MARY CELESTE · PAINTED 1861", label_t=.6,
        credit="MARY CELESTE AS 'AMAZON', 1861 · UNKNOWN PAINTER · " + PD)
B.card("found", ["FOUND ADRIFT", "DEC 4, 1872", "ATLANTIC OCEAN", "PEOPLE ON BOARD: NONE"], 1780, 560, 700, cue("cold", "drifts"), tilt=3,
       marks=[(3, "NONE", cue("cold", "nobody"), cue("cold", "nobody") + .6, "circle")], size=40)
B.string("ship", "found", cue("cold", "drifts") + .4)
B.card("aboard", ["SAILED WITH", "10 PEOPLE", "SEEN AGAIN: 0"], 1350, 1280, 640, S("stakes"), tilt=-2,
       marks=[(1, "10 PEOPLE", S("stakes") + .1, S("stakes") + .6, "underline"), (2, "0", cue("stakes", "nobody"), cue("stakes", "nobody") + .5, "circle")], size=48)
B.string("found", "aboard", S("stakes") + .3)
B.photo("briggs", "briggs", 560, 1950, 400, cue("back", "Captain"), tilt=-3, label="CAPT. BENJAMIN BRIGGS",
        credit="BENJAMIN S. BRIGGS · UNKNOWN PHOTOGRAPHER · " + PD)
B.photo("sarah", "sarah", 1120, 1990, 270, cue("back", "Sarah"), tilt=2, label="SARAH BRIGGS",
        credit="SARAH E. BRIGGS · UNKNOWN PHOTOGRAPHER · " + PD)
B.photo("sophia", "sophia", 1640, 1940, 380, cue("back", "Sophia"), tilt=-1, label="SOPHIA, 2",
        credit="SOPHIA M. BRIGGS · UNKNOWN PHOTOGRAPHER · " + PD)
B.string("aboard", "briggs", cue("back", "Captain") + .3); B.string("briggs", "sarah", cue("back", "Sarah") + .3)
B.string("sarah", "sophia", cue("back", "Sophia") + .3)
B.card("clues", ["FOUND ON BOARD", "SHIP: COULD STILL SAIL", "FOOD: 6 MONTHS", "CREW'S THINGS: LEFT"], 760, 2700, 820, S("clues"), tilt=2,
       marks=[(1, "COULD STILL SAIL", cue("clues", "could"), cue("clues", "could") + .6, "underline"),
              (2, "6 MONTHS", cue("clues", "Six"), cue("clues", "Six") + .5, "underline"),
              (3, "LEFT", cue("clues", "still there"), cue("clues", "still there") + .5, "circle")], size=40)
B.photo("engr", "engraving", 1760, 2560, 720, cue("clues", "sailors"), tilt=-4, label="THE MARY CELESTE",
        credit="MARY CELESTE, ENGRAVING · UNKNOWN ARTIST · " + PD)
B.string("sophia", "clues", S("clues") + .2)
B.card("but", ["BUT:", "LIFEBOAT: GONE", "1 PUMP: TAKEN APART", "WATER IN THE HOLD"], 1600, 3250, 760, S("but"), tilt=-2,
       marks=[(1, "GONE", cue("but", "gone"), cue("but", "gone") + .5, "circle"),
              (2, "TAKEN APART", cue("but", "taken"), cue("but", "taken") + .5, "underline"),
              (3, "WATER", cue("but", "water"), cue("but", "water") + .5, "underline")], size=42)
B.string("clues", "but", S("but") + .2)
B.card("log", ["LAST LOG ENTRY", "NOV 25, 1872", "NEAR SANTA MARIA, AZORES", "THEN: 9 DAYS OF SILENCE"], 760, 3600, 820, S("log"), tilt=1,
       marks=[(2, "SANTA MARIA", cue("log", "Santa"), cue("log", "Santa") + .6, "underline"),
              (3, "9 DAYS", cue("log", "nine"), cue("log", "nine") + .5, "circle")], size=40)
B.string("but", "log", S("log") + .2)
B.card("cargo", ["CARGO", "1,701 BARRELS OF ALCOHOL", "EMPTY: 9"], 900, 4180, 760, S("cargo"), tilt=-3,
       marks=[(1, "1,701", cue("cargo", "one thousand"), cue("cargo", "one thousand") + .5, "underline"),
              (2, "EMPTY: 9", cue("cargo", "Nine"), cue("cargo", "Nine") + .6, "circle")], size=42)
B.string("log", "cargo", S("cargo") + .2)
T_NP0, T_NP1 = cue("myth", "pirates") - .3, cue("myth", "Others") - .15            # full-screen newspaper cut-away
B.photo("paper", "paper", 1700, 4120, 680, T_NP1 - .1, tilt=3, crop=(0, 0, 1, .41), sepia=.35,
        marks=[("underline", (.875, .152, .985, .172), cue("myth", "pirates") + .1, cue("myth", "pirates") + .4),
               ("underline", (.012, .177, .225, .198), cue("myth", "pirates") + .4, cue("myth", "pirates") + .8)],
        label="BOSTON POST · FEB 24, 1873", credit="BOSTON POST, 24 FEB 1873 (NYT REPRINT) · " + PD)
B.string("cargo", "paper", cue("myth", "pirates"))
B.label("MUTINY?", 1180, 4560, cue("myth", "mutiny"), size=36)
B.label("SEA MONSTER?", 1560, 4640, cue("myth", "monster"), size=36)
B.label("FROM THE SKY?", 1300, 4740, cue("myth", "sky"), size=36)
B.card("doyle", ["1884", "A. CONAN DOYLE", "SHORT STORY", "MADE UP · FICTION"], 640, 4720, 640, S("doyle"), tilt=2,
       marks=[(3, "FICTION", cue("doyle", "made-up"), cue("doyle", "made-up") + .5, "circle")], size=40)
B.card("court", ["GIBRALTAR INQUIRY · 1873", "SIGNS OF A FIGHT: NONE", "CRIME: NO PROOF"], 1620, 5000, 820, S("so"), tilt=-1,
       marks=[(1, "NONE", cue("so", "fight"), cue("so", "fight") + .5, "circle"), (2, "NO PROOF", cue("so", "No crime"), cue("so", "No crime") + .5, "underline")], size=40)
B.string("doyle", "court", S("so") + .2)
B.card("theory", ["MOST LIKELY?", "FEARED: SINKING / EXPLOSION", "ALL INTO THE LIFEBOAT"], 760, 5180, 860, S("turn"), tilt=-2,
       marks=[(1, "SINKING", cue("turn", "sinking"), cue("turn", "sinking") + .4, "underline"), (1, "EXPLOSION", cue("turn", "explode"), cue("turn", "explode") + .5, "underline"),
              (2, "LIFEBOAT", cue("turn", "little boat"), cue("turn", "little boat") + .5, "circle")], size=38)
B.string("court", "theory", S("turn") + .2)
B.stamp("NEVER FOUND", 1650, 5240, E("today") + .5, rot=-8, size=90)
B.stamp("UNSOLVED", 1200, 2700, S("why") + 1.2, rot=-12, size=300, key="unsolved")

V = 1500                                           # view width (board px on screen) while reading
B.cam = [(0, 900, 760, 1380), (cue("cold", "drifts") - .2, 1150, 720, 1500), (S("stakes") - .2, 1450, 950, 1700), (S("stakes") + 1.2, 1350, 1250, 1450),
         (S("back") + .3, 1150, 1700, 1800), (E("back") - .3, 1150, 1900, 1700),
         (S("clues") + .2, 1150, 2550, 1750), (E("clues") - .3, 1000, 2700, 1500),
         (S("but") + .2, 1500, 3180, 1450), (S("log") + .2, 900, 3550, 1450), (S("cargo") + .2, 1000, 4100, 1500),
         (S("myth") + .2, 1550, 4150, 1450), (cue("myth", "mutiny"), 1350, 4500, 1600),
         (S("doyle") + .2, 850, 4700, 1500), (S("so") + .2, 1500, 4950, 1500), (S("turn") + .2, 900, 5150, 1500),
         (S("today") + .1, 1500, 5200, 1400), (E("today") + .3, 1450, 5150, 1250),
         (S("why") + .1, 1300, 4500, 2200), (S("why") + 1.6, 1200, 2700, 3040), (TL.total, 1200, 2700, 3100)]
B.cam = [(t, x, y - 100, w * .74) if w < 2000 else (t, x, y, w) for t, x, y, w in B.cam]   # closer: cards readable, items above the subtitles

EP = BoardEpisode(TL, 175, "THE GHOST SHIP", order=ORDER, board=B,
                  sources=("Britannica · Smithsonian Magazine · Boston Post 1873", ""),
                  music=dict(bpm=66, root=2, prog="minor", audio="doku"),
                  cover=dict(words=["10 PEOPLE.", "NO TRACE."], kicker="Mary Celeste, 1872", hide=["unsolved"]))
EP.title_spec = (.15, 2.9, "THE GHOST SHIP", "ATLANTIC OCEAN · 1872", 250)
EP.accent = {"cold": ["nobody"], "stakes": ["Ten people"], "back": ["Mary Celeste"], "clues": ["could still sail"], "but": ["lifeboat gone"],
             "log": ["nine days"], "cargo": ["Nine empty"], "myth": ["pirates"], "doyle": ["made-up"], "so": ["No crime"],
             "turn": ["sinking explode"], "today": ["never found"], "why": ["ten people"]}
# ---- cut-aways: archive film, a drawing, the newspaper on a desk, a portrait (Chris 26.11.: "abwechslungsreicher") ----
VID = os.path.join(HERE, "vid"); CACHE = os.path.join(HERE, "vid", "cache")
FILM = "ARCHIVE FILM · ILLUSTRATIVE"
NP = Board(IMG, bg=desk(), size=(1600, 2800))
NP.photo("np", "paper", 800, 1200, 1500, -1, tilt=-1.5, crop=(0, 0, 1, .55), sepia=.3,
         marks=[("underline", (.875, .152, .985, .172), T_NP0 + .5, T_NP0 + .8), ("underline", (.012, .177, .225, .198), T_NP0 + .8, T_NP0 + 1.2)])
NP.items["np"].pin = False
NP.cam = [(0, 800, 700, 1500), (T_NP1 - T_NP0, 790, 900, 1450)]
NP_T = lambda tl: tl                                         # the desk board runs on insert-local time
class NewsInsert(BoardInsert):
    def render(self, tl, k):                                 # dark band behind the subtitles (white text on white paper)
        a = np.asarray(self.board.render(tl), np.float32).copy()
        y = np.arange(H)[:, None, None]; band = np.clip(1 - np.abs(y - 1130) / 190, 0, 1) ** .8
        return a * (1 - .62 * band)
for it in NP.items.values(): it.t -= T_NP0                  # item/mark times are absolute above -> make them insert-local
NP.items["np"].mk = [(st, box, a_ - T_NP0, b_ - T_NP0) for st, box, a_, b_ in NP.items["np"].mk]
NP.items["np"].t = -1
def have(f): return os.path.exists(os.path.join(VID, f)) and os.path.getsize(os.path.join(VID, f)) > 100000
sea = "sea.webm" if have("sea.webm") else "storm.webm"
EP_INS = [
    (0.0, cue("cold", "Sails") - .1, VideoInsert(os.path.join(VID, "storm.webm"), 8, 4, os.path.join(CACHE, "storm8")),
     None, "A STORM AT SEA (1900) · EDISON MFG. CO. · PUBLIC DOMAIN"),
    (S("clues") - .05, cue("clues", "The ship") - .1, VideoInsert(os.path.join(VID, "storm.webm"), 40, 4, os.path.join(CACHE, "storm40")),
     "THE SAILORS WHO FOUND HER · " + "ILLUSTRATIVE", "A STORM AT SEA (1900) · EDISON MFG. CO. · PUBLIC DOMAIN"),
    (cue("log", "Then") - .1, E("log") + .15, VideoInsert(os.path.join(VID, "bluenose.webm" if have("bluenose.webm") else "storm.webm"),
     30 if have("bluenose.webm") else 75.5, 3.9, os.path.join(CACHE, "drift" + ("b" if have("bluenose.webm") else "s"))), "9 DAYS · NO ONE AT THE WHEEL",
     "BLUENOSE VS. GERTRUDE L. THEBAUD (1938) · W. R. MACASKILL · PUBLIC DOMAIN" if have("bluenose.webm") else "A STORM AT SEA (1900) · EDISON MFG. CO. · PUBLIC DOMAIN"),
    (T_NP0, T_NP1, NewsInsert(NP), "BOSTON POST · FEB 24, 1873", "BOSTON POST, 24 FEB 1873 (NYT REPRINT) · PUBLIC DOMAIN"),
    (S("turn") - .05, cue("turn", "And he") - .1, None, "THE MOST LIKELY THEORY", "MARY CELESTE, ENGRAVING · UNKNOWN ARTIST · PUBLIC DOMAIN"),
    (S("today") - .05, E("today") + .45, VideoInsert(os.path.join(VID, sea), 20 if sea == "sea.webm" else 74.8, 4.6, os.path.join(CACHE, sea[:-5]), sepia=.6, bright=.85),
     "NEVER FOUND", "MARELLA EXPLORER CRUISE 2024 · DEBS HOME & GARDEN · CC BY 3.0" if sea == "sea.webm" else "A STORM AT SEA (1900) · EDISON MFG. CO. · PUBLIC DOMAIN"),
]
if os.path.exists(os.path.join(IMG, "doyle.jpg")):
    EP_INS.append((S("doyle") - .05, E("doyle") + .1, None, "ARTHUR CONAN DOYLE", "A. CONAN DOYLE, 1914 · WALTER BENINGTON · PUBLIC DOMAIN"))
FX = B.fx()
EP_INS = [(a_, b_, o if o else ShotInsert(EP, "engraving", (.5, .5, 1.0), (.5, .5, 1.12), mode="card", grade=(.95, .15, .5)) if "THEORY" in tg
           else ShotInsert(EP, "doyle", (.5, .45, 1.0), (.5, .42, 1.1), mode="card", grade=(1.0, .1, .6)), tg, cr) for a_, b_, o, tg, cr in EP_INS]
EP.inserts = sorted(EP_INS, key=lambda x: x[0])
FX = [f for f in FX if not any(a_ <= f[0] < b_ for a_, b_, *_ in EP.inserts)] + insert_fx(EP.inserts)   # no board foley under cut-aways
if __name__ == "__main__": EP.run(FX)
