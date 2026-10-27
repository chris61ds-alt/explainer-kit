"""NOT JUST YOU – No. 15: the next-in-line effect (Brenner 1973; Bond 1985). Area: memory."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .35, "blank": .5, "study": .5, "name": .45, "why": .45, "fix": .5, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "blank", "study", "name", "why", "fix", "point", "end"]
EP = Episode(TL, 15, "NEXT IN LINE", order=ORDER,
             chapters={"hook": "THE ROUND", "blank": "BLANK", "study": "THE STUDY", "name": "THE NAME", "why": "WHY", "fix": "THE FIX", "point": "LISTEN FIRST"},
             sources=("Brenner (1973), J. Verbal Learning & Verbal Behavior 12", "Bond (1985) · via Wikipedia"),
             music=dict(bpm=98, root=-1, prog="minor", kick="half", gaps=[(E("hook") + .05, S("blank") + .05)]),
             cover=dict(words=["WHAT", "DID THEY", "SAY?"], kicker="The next-in-line effect."))

XS = [130, 285, 440, 595, 760]       # seats in the round; index 3 = the one before you, 4 = you
SHOW = {"hook": 0, "blank": 0, "study": 700, "name": 700, "why": 0, "fix": 0, "point": 0}
specs = []
for i, x in enumerate(XS):
    col = INK if i == 4 else (SIG if i == 3 else MID)
    poses = [(0, IDLE)]
    if i == 3: poses = [(0, TALK), (S("blank"), IDLE), (S("why"), TALK), (S("point"), IDLE)]
    if i == 4: poses = [(0, IDLE), (S("blank"), SHRUG), (S("why"), WORRY), (S("fix"), IDLE), (S("point"), TALK)]
    specs.append(dict(col=col, f=-1 if i == 4 else 1, tg={k: (x, .62, dy) for k, dy in SHOW.items()}, poses=poses))
ACT = actors_layer(ORDER, S, specs); EP.layers.append(ACT)

def sc_hook(img, d, t):
    d.text((X0 - 6, 300), "YOUR TURN", font=F(BLK, 150), fill=INK)
    d.text((X0, 470), "is next.", font=F(BLK, 80), fill=SIG)
    # turn marker moving along the row
    k = clamp(t / 2.0); xm = lerp(XS[0], XS[3], k)
    d.polygon([(xm - 18, 640), (xm + 18, 640), (xm, 668)], fill=SIG)
    speech_box(d, XS[3] - 20, 540, 200, (t - .4) / .3, SIG, -1, "· · ·")
    think_box(d, (XS[4], 880), 150, 70, (t - .8) / .3, "my line", INK, -1, WHITE, 26)
    if t >= cue("hook", "what did"):
        box_label(d, XS[3] - 120, 480, "WHAT DID THEY SAY?", 26, WHITE, INK, anchor="ma")
    fig(d, "fig. 1 — a round of introductions")

def sc_blank(img, d, t):
    words_in(d, t, [("NO IDEA.", S("blank"), 320, 190, SIG)])
    speech_box(d, XS[3] - 20, 540, 200, 1, SIG, -1, "?")
    fig(d, "fig. 2 — gone")

WORDS = ["LAMP", "RIVER", "CHAIR", "CLOUD", "TRAIN", "SALT", "ROPE", "YOU"]
def sc_study(img, d, t):
    t0 = S("study"); ba = cue("study", "barely")
    d.text((X0, 320), "WORD BY WORD", font=F(BLK, 100), fill=INK)
    for i, w in enumerate(WORDS):
        k = ease((t - t0 - .2 - i * .35) / .25)
        if k <= 0: continue
        x = X0 + i * 106; y = 470
        you = w == "YOU"
        d.rectangle([x, y, x + 94, y + 130], fill=SIG if you else WHITE, outline=INK, width=4)
        d.text((x + 47, y + 65), w if not you else "YOUR\nTURN", font=F(COND, 22 if not you else 20), fill=WHITE if you else INK, anchor="mm", align="center")
    if t >= ba - .3:
        # recall per position: dip right before your turn
        yb = 1050; vals = [.7, .72, .68, .7, .66, .3, .22, .0]
        for i, v in enumerate(vals[:-1]):
            k = ease((t - ba + .3 - i * .05) / .4)
            x = X0 + i * 106 + 20
            d.rectangle([x, yb - 300 * v * k, x + 54, yb], fill=SIG if i >= 5 else INK)
        d.line([X0, yb, X1, yb], fill=INK, width=3)
        dim_h(d, X0 + 5 * 106 + 10, X0 + 7 * 106, yb - 330, (t - ba) / .4, SIG, "≈ 9 S BEFORE YOUR TURN", 22)
        d.text((X0, yb + 14), "recalled later", font=F(COND, 24), fill=INK)
        d.text((X1, 1146), "schematic", font=F(MED, 22), fill=MID, anchor="ra")
    fig(d, "Brenner, 1973")

def sc_name(img, d, t):
    words_in(d, t, [("NEXT-", cue("name", "next") - .1, 330, 220, INK), ("IN-LINE", cue("name", "line") - .2, 560, 220, SIG), ("EFFECT.", cue("name", "effect") - .1, 800, 160, INK)])

def sc_why(img, d, t):
    t0 = S("why"); sr = cue("why", "stops")
    d.text((X0, 320), "REHEARSING", font=F(BLK, 120), fill=INK)
    think_box(d, (XS[4], 880), 220, 80, (t - t0) / .3, "my line…", INK, -1, WHITE, 28)
    speech_box(d, XS[3] - 20, 540, 200, 1, SIG, -1, "· · ·")
    if t >= sr - .1:
        k = ease((t - sr + .1) / .3)
        box_label(d, X0, 500, "■ RECORDING PAUSED", 34, WHITE, SIG)
    fig(d, "fig. 3 — attention goes to your own line")

def sc_fix(img, d, t):
    t0 = S("fix"); ft = cue("fix", "focus")
    d.text((X0, 320), "THE FIX", font=F(BLK, 130), fill=INK)
    speech_box(d, XS[3] - 20, 540, 200, 1, SIG, -1, "· · ·")
    if t >= ft: eye(d, XS[4], 600, .8, INK, look=(-1, 0))
    if t >= cue("fix", "avoided"): box_label(d, XS[4] + 40, 640, "GOT IT", 30, WHITE, INK, anchor="ra")
    fig(d, "Bond, 1985 — told to focus on the speaker first")

def sc_point(img, d, t):
    t0 = S("point"); tk = cue("point", "then talk")
    words_in(d, t, [("LISTEN", t0, 300, 170, INK), ("FIRST.", t0 + .3, 470, 170, SIG)])
    if t >= tk: speech_box(d, XS[4] + 20, 690, 180, (t - tk) / .3, INK, -1, "Hi!")
    fig(d, "fig. 4 — the same round, done right")

EP.scenes = {"hook": sc_hook, "blank": sc_blank, "study": sc_study, "name": sc_name, "why": sc_why, "fix": sc_fix, "point": sc_point}
FX = [(0.0, thud(.5), 0), (.4, pop(.15), .1), (.8, pop(.12), .3), (cue("hook", "what did"), riser(.5, .07), 0), *EP.cut_fx(),
      (S("blank") + .05, thud(.55), 0), *[(S("study") + .2 + i * .35, tick(.05), (i - 4) / 5) for i in range(8)],
      (cue("study", "barely"), thud(.35), 0), *[(cue("name", w) - .1, thud(.3), 0) for w in ("next", "line", "effect")],
      (cue("why", "stops"), rewind_sfx(.12, .35), .3), (cue("fix", "focus"), pop(.18), .3), (cue("fix", "avoided"), pop(.2), .3),
      (cue("point", "then talk"), pop(.2), .3), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
