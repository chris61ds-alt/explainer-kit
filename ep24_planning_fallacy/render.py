"""NOT JUST YOU – No. 24: the planning fallacy (Buehler, Griffin & Ross 1994). Area: time."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .4, "worst": .8, "real": .5, "name": .5, "tip": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "worst", "real", "name", "tip", "end"]
EP = Episode(TL, 24, "TWO DAYS", order=ORDER,
             chapters={"hook": "FAMOUS LAST WORDS", "study": "THE GUESS", "worst": "WORST CASE", "real": "REALITY", "name": "THE NAME", "tip": "THE FIX"},
             sources=("Buehler, Griffin & Ross (1994), Journal of", "Personality and Social Psychology 67(3)"),
             music=dict(bpm=102, root=0, prog="minor", kick="four", gaps=[(E("worst") + .05, S("real") + .05)]),
             cover=dict(words=["TWO", "DAYS."], kicker="Famous last words."))

X_A, X_B, YT = X0 + 20, X1 - 20, 760
def days_x(v): return lerp(X_A, X_B, v / 60)
def timeline(d, t):
    d.line([X_A, YT, X_B, YT], fill=INK, width=5)
    for v in range(0, 61, 5):
        x = days_x(v); h = 18 if v % 10 == 0 else 9
        d.line([x, YT, x, YT + h], fill=INK, width=3)
        if v % 10 == 0: d.text((x, YT + 26), str(v), font=F(MONO, 22), fill=MID, anchor="ma")
    d.text((X_B, YT + 60), "days", font=F(MONO, 20), fill=MID, anchor="ra")
def marker(d, v, k, label, col, up=1, lvl=0):
    if k <= 0: return
    x = days_x(v * ease(k)); y = YT - 20 if up > 0 else YT + 20
    d.polygon([(x, YT - 8), (x - 18, YT - 44), (x + 18, YT - 44)], fill=col)
    if k > .9:
        d.line([x, YT - 44, x, YT - 120 - lvl * 90], fill=col, width=3)
        box_label(d, x, YT - 160 - lvl * 90, label, 28, WHITE, col, anchor="ma" if v < 50 else "ra")

def sc_hook(img, d, t):
    fl = cue("hook", "famous")
    d.text((X0 - 6, 300), "2 DAYS.", font=F(BLK, 230), fill=INK if t < fl else RULE)
    if t >= fl - .1: words_in(d, t, [("FAMOUS", fl - .1, 560, 140, SIG), ("LAST WORDS.", fl + .2, 710, 120, SIG)])
    d.rectangle([600, 880, 860, 1100], fill=SIG_L, outline=INK, width=3); d.text((620, 900), "TO DO", font=F(COND, 28), fill=INK)
    for i in range(4): d.line([620, 960 + i * 34, 840 - (i % 2) * 60, 960 + i * 34], fill=INK, width=4)
    fig(d, "fig. 1 — every plan, ever")

def sc_study(img, d, t):
    d.text((X0, 320), "THE THESIS", font=F(BLK, 120), fill=INK)
    timeline(d, t); marker(d, 33.9, (t - cue("study", "thirty") + .3) / .6, "GUESS: 34", INK, lvl=0)
    fig(d, "37 psychology students · Buehler, Griffin & Ross, 1994")

def sc_worst(img, d, t):
    d.text((X0, 320), "WORST CASE", font=F(BLK, 120), fill=INK)
    timeline(d, t); marker(d, 33.9, 1, "GUESS: 34", INK, lvl=0)
    marker(d, 48.6, (t - cue("worst", "forty") + .3) / .6, "WORST CASE: 49", MID, lvl=1)

def sc_real(img, d, t):
    t0 = S("real")
    d.text((X0, 320), "REALITY", font=F(BLK, 130), fill=SIG)
    timeline(d, t); marker(d, 33.9, 1, "GUESS: 34", INK, lvl=0); marker(d, 48.6, 1, "WORST CASE: 49", MID, lvl=1)
    marker(d, 55.5, (t - t0 - .1) / .7, "ACTUAL: 55.5", SIG, lvl=2)
    if t >= cue("real", "three in ten") - .2:
        for i in range(10):
            on = i < 3; picto(d, X0 + 50 + i * 86, FLOOR, .36, SIG if on else MID, pose=OPEN if on else WORRY)
        d.text((X0, 900), "finished by their guess:", font=F(COND, 30), fill=INK)

def sc_name(img, d, t):
    t0 = S("name"); ip = cue("name", "not the interruptions")
    words_in(d, t, [("PLANNING", cue("name", "planning") - .1, 300, 160, INK), ("FALLACY.", cue("name", "fallacy") - .1, 470, 160, SIG)])
    ya = 820
    d.text((X0, 690), "THE PLAN", font=F(COND, 28), fill=INK); d.line([X0, ya - 60, X1, ya - 60], fill=INK, width=6)
    if t >= ip - .1:
        k = ease((t - ip + .1) / .8)
        pts = [(X0, ya + 80), (X0 + 120, ya + 80), (X0 + 160, ya + 160), (X0 + 300, ya + 160), (X0 + 330, ya + 60), (X0 + 480, ya + 140), (X0 + 560, ya + 220), (X0 + 700, ya + 120), (X1, ya + 180)]
        n = max(2, int(len(pts) * k)); d.line(pts[:n], fill=SIG, width=6)
        d.text((X0, ya + 20), "WHAT HAPPENS", font=F(COND, 28), fill=SIG)
        for i, (lab, pi) in enumerate((("email", 2), ("sick day", 4), ("meeting", 6), ("redo", 7))):
            if n > pi: box_label(d, pts[pi][0], pts[pi][1] + 20, lab, 22, WHITE, INK, anchor="ma")

def sc_tip(img, d, t):
    t0 = S("tip"); lt = cue("tip", "last time")
    d.text((X0, 320), "LAST TIME:", font=F(BLK, 130), fill=INK)
    rows = [("planned", "2 days", INK), ("took", "5 days", SIG)]
    for i, (a, b, col) in enumerate(rows):
        k = ease((t - lt - i * .4) / .35)
        if k > 0:
            y = 560 + i * 150; d.rectangle([X0, y, X1, y + 120], outline=INK, width=4)
            d.text((X0 + 30, y + 60), a, font=F(COND, 40), fill=INK, anchor="lm"); d.text((X1 - 30, y + 60), b, font=F(BLK, 64), fill=col, anchor="rm")
    if t >= cue("tip", "should"): note(d, X1 - 150, 860, 700, 1000, "plan with this number", (t - cue("tip", "should")) / .35, SIG, anchor="ra", size=28)
    fig(d, "fig. 2 — the outside view · example")

EP.scenes = {"hook": sc_hook, "study": sc_study, "worst": sc_worst, "real": sc_real, "name": sc_name, "tip": sc_tip}
FX = [(0.0, thud(.5), 0), (cue("hook", "famous") - .1, rewind_sfx(.12, .4), 0), *EP.cut_fx(),
      (cue("study", "thirty"), pop(.18), -.2), (cue("worst", "forty"), pop(.18), .2), (S("real") + .1, thud(.6), .3),
      (cue("real", "three in ten"), pop(.15), 0), (cue("name", "planning") - .1, thud(.4), 0), (cue("name", "not the interruptions"), whoosh(.8, .1), 0),
      (cue("tip", "last time"), pop(.18), 0), (cue("tip", "last time") + .4, pop(.18), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
