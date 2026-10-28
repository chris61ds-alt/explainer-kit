"""NOT JUST YOU – No. 59 (format test: SELF-TEST): the Stroop effect (Stroop 1935). v3 'Swiss Thread', light only
(the test needs real colours). The thread is a fuse/timer during both rounds."""
import os, sys, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from thread import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "r1": 4.2, "r2": 5.0, "result": .6, "why": .6, "name": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "r1", "r2", "result", "why", "name", "point", "end"]
EP = ThreadEpisode(TL, 59, "SAY THE COLOR", order=ORDER, dark=False, label="SELF-TEST",
                   chapters={"hook": "THE RULES", "r1": "ROUND 1", "r2": "ROUND 2", "result": "THE RESULT", "why": "WHY", "name": "1935", "point": "TRY IT"},
                   sources=("Stroop (1935), Journal of Experimental", "Psychology 18(6)"),
                   music=dict(bpm=110, root=0, prog="tense", kick="four", gaps=[(S("r1") - .2, E("r2") + 5.0)]),
                   cover=dict(words=["SAY THE", "COLOR."], kicker="Not the word. Out loud."))

C = {"RED": (226, 32, 44), "BLUE": (28, 84, 232), "GREEN": (22, 150, 70), "YELLOW": (236, 182, 0), "PURPLE": (138, 58, 200), "BLACK": (12, 12, 12)}
R1 = [("RED", "RED"), ("BLUE", "BLUE"), ("GREEN", "GREEN"), ("YELLOW", "YELLOW"), ("PURPLE", "PURPLE"), ("BLACK", "BLACK")]
R2 = [("BLUE", "RED"), ("GREEN", "PURPLE"), ("RED", "BLUE"), ("YELLOW", "GREEN"), ("BLACK", "YELLOW"), ("PURPLE", "RED")]

def word_grid(d, items, t, t0, step=.45):
    cw, chh = (X1 - X0) / 2, 150
    for i, (word, ink) in enumerate(items):
        r, c = divmod(i, 2); x, y = X0 + c * cw, 340 + r * chh
        k = ease((t - t0 - i * step) / .2)
        d.rectangle([x, y, x + cw, y + chh], outline=RULE, width=2)
        if k > 0: d.text((x + cw / 2, y + chh / 2 + (1 - k) * 20), word, font=F(BLK, 104), fill=C[ink], anchor="mm")

def fuse(d, t, a, b, label):
    k = clamp((t - a) / (b - a)); x = lerp(LX, RX, k)
    d.line([(LX, THREAD_Y), (x, THREAD_Y)], fill=SIG, width=7)
    d.line([(x, THREAD_Y), (RX, THREAD_Y)], fill=RULE, width=3)
    if 0 < k < 1:
        for i in range(5):
            a_ = t * 13 + i * 1.3; d.line([x, THREAD_Y, x + 18 * math.cos(a_), THREAD_Y + 18 * math.sin(a_)], fill=SIG, width=3)
    d.text((X0, THREAD_Y + 40), label, font=F(MONO, 22), fill=MID)

def sc_hook(img, d, t):
    d.text((X0 - 6, 320), "SAY THE", font=F(BLK, 170), fill=INK); d.text((X0 - 6, 500), "COLOR.", font=F(BLK, 170), fill=SIG)
    d.text((X0, 690), "not the word · out loud", font=F(COND, 44), fill=INK)
    k = ease((t - cue("hook", "not the word")) / .3)
    if k > 0:
        d.text((X0, 800), "GREEN", font=F(BLK, 90), fill=C["RED"])
        d.text((X0 + 380, 830), "→ say: “red”", font=F(MONO, 34), fill=INK)
    fig(d, "fig. 1 — the rules")

def sc_r1(img, d, t):
    t0 = E("r1") + .05
    word_grid(d, R1, t, t0)
    fuse(d, t, t0, S("r2") - .1, "ROUND 1 · EASY")

def sc_r2(img, d, t):
    t0 = E("r2") + .05
    word_grid(d, R2, t, t0)
    fuse(d, t, t0, S("result") - .1, "ROUND 2 · SAY THE INK COLOUR")

def sc_result(img, d, t):
    t0 = S("result")
    d.text((X0, 320), "SLOWER?", font=F(BLK, 190), fill=SIG)
    hbar(d, 580, .45, (t - t0 - .2) / .4, MID, "round 1", h=90)
    hbar(d, 760, .85, (t - t0 - .6) / .6, SIG, "round 2", h=90)
    if t >= cue("result", "almost everyone"): box_label(d, X0, 950, "ALMOST EVERYONE", 40, WHITE, INK)
    d.line([(LX, THREAD_Y + 140), (RX, THREAD_Y + 140)], fill=SIG, width=6)
    fig(d, "your time · schematic")

def sc_why(img, d, t):
    t0, tf = S("why"), cue("why", "fight itself") - .2
    d.text((X0, 320), "AUTOPILOT", font=F(BLK, 150), fill=INK)
    d.text((480, 600), "RED", font=F(BLK, 150), fill=C["BLUE"], anchor="mm")
    bbox(d, (300, 520, 660, 690), "INPUT", INK, (t - t0 - .2) / .3)
    k = ease((t - t0 - .5) / .6)
    d.line(spline([(LX, 600), (200, 600), (300, 605)]), fill=SIG, width=6)
    d.line([(480, 720), (lerp(480, 240, k), 900)], fill=C["RED"], width=8); d.text((240, 915), "READ: red", font=F(MONO, 30), fill=C["RED"], anchor="ma")
    d.line([(480, 720), (lerp(480, 720, k), 900)], fill=C["BLUE"], width=8); d.text((720, 915), "SEE: blue", font=F(MONO, 30), fill=C["BLUE"], anchor="ma")
    if t >= tf:
        box_label(d, 480, 990, "CONFLICT", 44, WHITE, SIG, font=BLK, anchor="ma")
        if t < tf + .3: glitch(img, (X0, 500, X1, 1000), 1.0, seed=int(t * 30))
    fig(d, "reading wins the race, naming has to override it")

def sc_name(img, d, t):
    t0 = S("name")
    d.text((X0, 320), "STROOP", font=F(BLK, 200), fill=INK)
    counter(d, X0, 540, t, t0 + .4, .8, 1935, "{:.0f}", 200, SIG)
    for i, (w_, ink) in enumerate(R2[:4]):
        d.text((X0 + i * 215, 820), w_[:3], font=F(BLK, 70), fill=C[ink])
    d.line([(LX, THREAD_Y + 120), (RX, THREAD_Y + 120)], fill=SIG, width=6)
    fig(d, "J. R. Stroop, 1935 · still works today")

def sc_point(img, d, t):
    t0, tf = S("point"), cue("point", "try it")
    words_in(d, t, [("YOU CAN'T", t0, 320, 150, INK), ("NOT READ.", t0 + .3, 480, 150, SIG)])
    if t >= tf - .2:
        picto(d, 330, THREAD_Y + 260, .7, INK, f=1, pose=TALK(t)); picto(d, 620, THREAD_Y + 260, .7, SIG, f=-1, pose=FACEPALM)
        speech_box(d, 360, 760, 220, (t - tf + .2) / .3, INK, 1, "say it!", 30)
    fig(d, "fig. 2 — send it to a friend")

EP.scenes = {"hook": sc_hook, "r1": sc_r1, "r2": sc_r2, "result": sc_result, "why": sc_why, "name": sc_name, "point": sc_point}
FX = [(0.0, thud(.5), 0), (cue("hook", "not the word"), pop(.15), 0), *EP.cut_fx(),
      *[(E("r1") + .05 + i * .45, tick(.06), (i % 2 - .5)) for i in range(6)], *[(E("r1") + .05 + i * .5, softkick(.08), 0) for i in range(8)],
      *[(E("r2") + .05 + i * .45, tick(.06), (i % 2 - .5)) for i in range(6)], *[(E("r2") + .05 + i * .45, softkick(.09), 0) for i in range(11)],
      (S("result") - .1, thud(.5), 0), (cue("result", "almost everyone"), pop(.15), 0), (cue("why", "fight itself") - .2, thud(.45), 0),
      (cue("name", "nineteen") - .3, riser(.6, .05), 0), (cue("point", "try it") - .2, pop(.15), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
