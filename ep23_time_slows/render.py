"""NOT JUST YOU – No. 23: does time slow down in fear? (Stetson, Fiesta & Eagleman 2007). Area: time."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .45, "guess": .5, "test": .9, "result": .6, "why": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "guess", "test", "result", "why", "end"]
EP = Episode(TL, 23, "SLOW MOTION", order=ORDER,
             chapters={"hook": "SLOW MO?", "study": "THE FALL", "guess": "THE GUESS", "test": "THE TEST", "result": "THE ANSWER", "why": "WHY"},
             sources=("Stetson, Fiesta & Eagleman (2007),", "PLoS ONE 2(12) · via ScienceDaily"),
             music=dict(bpm=90, root=-1, prog="tense", kick="half", gaps=[(E("test") + .05, S("result") + .1)]),
             cover=dict(words=["SLOW", "MOTION?"], kicker="Why fear stretches time."))

FALL = {"arms": ((160, 10), (-160, -10)), "legs": ((20, 10), (-20, -10))}
def sc_hook(img, d, t):
    d.text((X0 - 6, 300), "SLOW MO?", font=F(BLK, 190), fill=INK)
    clock(d, 700, 760, 140, t=t, speed=.3)
    x, y = 300, 700 + 20 * math.sin(t * 1.2)
    for i in range(4): d.line([x + (-110 if i < 2 else 90) + (i % 2) * 22, y - 40 + (i % 2) * 40, x + (-110 if i < 2 else 90) + (i % 2) * 22, y + 80 + (i % 2) * 40], fill=RULE, width=6)
    picto(d, x, y + 200, .9, INK, pose=FALL, head_dy=0)
    if t >= cue("hook", "right"): box_label(d, 700, 940, "RIGHT?", 34, WHITE, SIG, anchor="ma")
    fig(d, "fig. 1 — how a scary moment feels")

def sc_study(img, d, t):
    t0 = S("study"); ff = cue("study", "free fall")
    d.text((X0, 320), "THE DROP", font=F(BLK, 130), fill=INK)
    tx = 260; top, net = 500, 1080
    d.rectangle([tx - 80, top - 20, tx + 80, top], fill=INK); d.line([tx + 80, top - 10, tx + 80, net], fill=RULE, width=4)
    for i in range(7): d.line([tx - 120 + i * 40, net, tx - 100 + i * 40, net + 30], fill=INK, width=4)
    d.line([tx - 140, net, tx + 140, net], fill=INK, width=6)
    u = clamp((t - ff + .4) / 1.1) ** 2
    y = lerp(top, net - 20, u)
    picto(d, tx, y, .45, SIG, pose=FALL if u > 0 else IDLE)
    dim_v(d, tx + 180, top, net, (t - t0 - .3) / .5, SIG, "≈ 31 M")
    note(d, tx + 140, net, 620, 980, "into a net", (t - t0 - .6) / .4, INK, size=28)
    fig(d, "Stetson, Fiesta & Eagleman — PLoS ONE, 2007")

def sc_guess(img, d, t):
    t0 = S("guess"); tl = cue("guess", "third")
    d.text((X0, 320), "HOW LONG?", font=F(BLK, 130), fill=INK)
    hbar(d, 560, .55, (t - t0 - .3) / .5, MID, "someone else's fall", h=100)
    hbar(d, 760, .55 * 1.36, (t - cue("guess", "own fall") + .2) / .5, SIG, "my own fall", h=100)
    if t >= tl: dim_h(d, X0 + 840 * .55, X0 + 840 * .748, 900, (t - tl) / .4, SIG, "+36 %", 26)
    fig(d, "estimated duration · schematic bars, study value")

def wrist(d, cx, cy, t, fast=True):
    d.rectangle([cx - 200, cy - 40, cx + 200, cy + 40], fill=INK)
    d.rounded_rectangle([cx - 110, cy - 110, cx + 110, cy + 110], radius=18, fill=INK)
    d.rectangle([cx - 90, cy - 90, cx + 90, cy + 90], fill=WHITE)
    if fast:
        ph = int(t * 30) % 2; n = (int(t * 7) * 37) % 90 + 10
        if ph == 0: d.text((cx, cy), f"{n}", font=F(BLK, 110), fill=INK, anchor="mm")
        else:
            d.rectangle([cx - 90, cy - 90, cx + 90, cy + 90], fill=INK); d.text((cx, cy), f"{n}", font=F(BLK, 110), fill=WHITE, anchor="mm")

def sc_test(img, d, t):
    t0 = S("test"); rd = cue("test", "if time")
    d.text((X0, 320), "THE DISPLAY", font=F(BLK, 120), fill=INK)
    wrist(d, 480, 720, t)
    note(d, 590, 640, 860, 520, "numbers flashing too fast", (t - t0 - .6) / .4, SIG, anchor="ra", size=28)
    if t >= rd: box_label(d, 480, 900, "SLOWER TIME = READABLE", 30, WHITE, INK, anchor="ma")
    fig(d, "the 'perceptual chronometer' on the wrist")

def sc_result(img, d, t):
    t0 = S("result")
    words_in(d, t, [("THEY", t0, 300, 200, INK), ("COULDN'T.", t0 + .15, 500, 176, SIG)])
    wrist(d, 480, 920, t)
    k = ease((t - t0 - .3) / .3)
    d.line([360, 800, 360 + 240 * k, 800 + 240 * k], fill=SIG, width=12); d.line([600, 800, 600 - 240 * k, 800 + 240 * k], fill=SIG, width=12)

def film(d, x0, x1, y, n, k, col):
    d.rectangle([x0, y, x0 + (x1 - x0) * ease(k), y + 120], fill=INK)
    for i in range(int(n * ease(k))):
        x = x0 + 20 + i * (x1 - x0 - 40) / n
        d.rectangle([x, y + 26, x + (x1 - x0 - 40) / n - 10, y + 94], fill=col)
    for i in range(int((x1 - x0) / 30 * ease(k))):
        d.rectangle([x0 + 8 + i * 30, y + 6, x0 + 20 + i * 30, y + 16], fill=WHITE); d.rectangle([x0 + 8 + i * 30, y + 104, x0 + 20 + i * 30, y + 114], fill=WHITE)

def sc_why(img, d, t):
    t0 = S("why"); mm = cue("why", "more memory")
    d.text((X0, 320), "MORE FRAMES", font=F(BLK, 120), fill=INK)
    d.text((X0, 470), "a normal moment", font=F(COND, 32), fill=INK); film(d, X0, X0 + 480, 520, 4, (t - t0 - .2) / .5, RULE)
    d.text((X0, 700), "a frightening moment", font=F(COND, 32), fill=SIG); film(d, X0, X1, 750, 14, (t - cue("why", "detail") + .2) / .6, SIG_L)
    if t >= mm - .1: dim_h(d, X0, X1, 930, (t - mm + .1) / .4, SIG, "FEELS LONGER", 26)
    fig(d, "fig. 2 — denser memories, not slower time")

EP.scenes = {"hook": sc_hook, "study": sc_study, "guess": sc_guess, "test": sc_test, "result": sc_result, "why": sc_why}
FX = [(0.0, thud(.5), 0), (0.0, whoosh(1.2, .1), 0), (cue("hook", "right"), pop(.18), .2), *EP.cut_fx(),
      (E("study") - .05, whoosh(.6, .1), 0), (cue("study", "free fall") + .7, thud(.4), 0),
      (cue("guess", "own fall"), pop(.15), .2), (cue("guess", "third"), thud(.35), 0),
      *[(S("test") + .3 + i * .12, tick(.05), (i % 3 - 1) * .4) for i in range(20)], (S("result") + .1, thud(.6), 0),
      (cue("why", "detail"), whoosh(.5, .1), 0), (cue("why", "more memory"), riser(.4, .07), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
