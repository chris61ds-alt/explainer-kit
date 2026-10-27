"""NOT JUST YOU – No. 38: shock over thinking (Wilson et al. 2014). Series: Swiss Dark (edgy)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .4, "hate": .5, "button": .9, "result": .5, "record": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "hate", "button", "result", "record", "point", "end"]
EP = Episode(TL, 38, "JUST THINK", order=ORDER, dark=True,
             chapters={"hook": "SHOCK", "study": "THE ROOM", "hate": "15 MINUTES", "button": "THE BUTTON", "result": "WHO PRESSED", "record": "THE RECORD", "point": "THINKING IS HARD"},
             sources=("Wilson et al. (2014), Science 345(6192)", "via BPS Research Digest"),
             music=dict(bpm=88, root=-5, prog="tense", kick="half", gaps=[(E("button") + .05, S("result") + .05)]),
             cover=dict(words=["SHOCK", "OR", "THINK?"], kicker="People chose the shock."))

def bolt(d, x, y, s=1.0, col=SIG):
    d.polygon([(x, y - 60 * s), (x - 30 * s, y + 6 * s), (x - 4 * s, y + 6 * s), (x - 14 * s, y + 60 * s), (x + 30 * s, y - 10 * s), (x + 4 * s, y - 10 * s), (x + 14 * s, y - 60 * s)], fill=col)

def room(d):
    d.rectangle([X0 + 20, 520, X1 - 20, FLOOR], outline=INK, width=6)
    d.line([X0 + 20, FLOOR, X1 - 20, FLOOR], fill=INK, width=8)

def button(d, cx, cy, pressed=0.0, s=1.0):
    d.rectangle([cx - 90 * s, cy - 10 * s, cx + 90 * s, cy + 60 * s], fill=INK)
    h = 46 * s * (1 - .6 * pressed)
    d.ellipse([cx - 60 * s, cy - h, cx + 60 * s, cy - h + 50 * s], fill=SIG); d.rectangle([cx - 60 * s, cy - h + 25 * s, cx + 60 * s, cy + 10 * s], fill=SIG)

SIT = {"arms": ((40, 60), (-20, 40)), "legs": ((90, 0), (86, 0))}
def chair_person(d, x, t, pose=None, col=INK):
    chair(d, x, 970, f=1)
    return picto(d, x - 10, 970 + 140, 1.0, col, f=1, pose=pose or SIT, head_dy=2 * math.sin(t * 2))

def sc_hook(img, d, t):
    d.text((X0 - 6, 300), "SHOCK", font=F(BLK, 200), fill=SIG)
    d.text((X0, 500), "or think?", font=F(BLK, 90), fill=INK)
    chair_person(d, 300, t)
    button(d, 680, 1020, pressed=1 if int(t * 2) % 2 else 0)
    if int(t * 2) % 2: bolt(d, 680, 860, 1.2)
    fig(d, "fig. 1 — the choice")

def sc_study(img, d, t):
    t0 = S("study")
    d.text((X0, 300), "15:00", font=F(BLK, 200), fill=INK)
    room(d); chair_person(d, 480, t)
    k = clamp((t - t0) / 5)
    clock(d, X1 - 120, 640, 70, minutes=15 * k)
    if t >= cue("study", "no phone"):
        phone(d, X0 + 120, 700, .8, MID); d.line([X0 + 70, 620, X0 + 170, 780], fill=SIG, width=8)
    fig(d, "students alone in a bare room · Wilson et al., 2014")

def sc_hate(img, d, t):
    t0 = S("hate")
    d.text((X0, 300), "BORING.", font=F(BLK, 200), fill=INK)
    room(d); chair_person(d, 480, t, pose=WORRY)
    d.text((X0 + 60, 560), "enjoyment", font=F(COND, 28), fill=INK)
    d.rectangle([X0 + 60, 600, X1 - 60, 640], outline=INK, width=4)
    d.rectangle([X0 + 66, 606, X0 + 66 + (X1 - X0 - 132) * lerp(.7, .35, ease((t - t0) / .8)), 634], fill=SIG)
    fig(d, "half rated it at or below the midpoint")

def sc_button(img, d, t):
    t0 = S("button"); pay = cue("button", "pay")
    d.text((X0, 300), "THE BUTTON", font=F(BLK, 130), fill=INK)
    room(d); chair_person(d, 300, t)
    button(d, 680, 1040, s=1.1 * ease((t - cue("button", "button") + .2) / .3))
    if t >= cue("button", "mild"): box_label(d, 680, 860, "MILD SHOCK", 30, WHITE, SIG, anchor="ma")
    if t >= pay: note(d, 560, 1000, 520, 640, "they'd pay to avoid it", (t - pay) / .35, INK, anchor="ra", size=28)

def sc_result(img, d, t):
    t0 = S("result"); wm = cue("result", "women")
    d.text((X0, 300), "PRESSED IT", font=F(BLK, 130), fill=SIG)
    for row, (lab, n_on, n, tk, y) in enumerate((("men", 2, 3, t0 + .1, 560), ("women", 1, 4, wm - .2, 860))):
        k = ease((t - tk) / .4)
        if k <= 0: continue
        d.text((X0, y - 40), lab, font=F(COND, 34), fill=INK)
        for i in range(n):
            x = X0 + 80 + i * 190; on = i < n_on
            picto(d, x, y + 240, .55, SIG if on else MID, pose=IDLE)
            if on: bolt(d, x + 60, y + 30, .5)
        box_label(d, X1, y - 40, ("2 OF 3" if row == 0 else "1 OF 4"), 36, WHITE, SIG if row == 0 else INK, anchor="ra")
    fig(d, "67 % of men · 25 % of women · at least once")

def sc_record(img, d, t):
    t0 = S("record")
    counter(d, X0, 300, t, t0 + .1, 1.6, 190, "{:.0f}×", 260, SIG)
    room(d); h = chair_person(d, 300, t, pose={"arms": ((80, 90), (-20, 40)), "legs": ((90, 0), (86, 0))})
    pr = int(t * 8) % 2
    button(d, 520, 1040, pressed=pr, s=.8)
    if pr: bolt(d, 600, 900, .7)
    fig(d, "one participant · excluded from the analysis")

def sc_point(img, d, t):
    t0 = S("point"); hw = cue("point", "hard work")
    words_in(d, t, [("NOT WEIRD.", t0 + .2, 300, 150, INK)] if t < hw - .2 else [("THINKING IS", hw - .2, 300, 130, INK), ("HARD WORK.", hw, 450, 140, SIG)])
    h = picto(d, 420, FLOOR, 1.05, INK, pose={"arms": ((100, 110), (-10, -5))})
    phone(d, 560, 820, .8, INK, lit=True)
    fig(d, "fig. 2 — reaching for the phone, again")

EP.scenes = {"hook": sc_hook, "study": sc_study, "hate": sc_hate, "button": sc_button, "result": sc_result, "record": sc_record, "point": sc_point}
def zap(amp=.1, dur=.25):
    t = tt_(dur); return amp * np.sign(np.sin(2 * np.pi * 90 * t)) * bp(np.random.default_rng(1).standard_normal(len(t)), 400, 6000) * np.exp(-t * 10)
FX = [(0.0, thud(.5), 0), (.5, zap(.09), .3), (1.5, zap(.09), .3), *EP.cut_fx(),
      *[(S("study") + i * .4, tick(.05), 0) for i in range(10)], (cue("button", "button"), pop(.2), .3), (cue("button", "pay"), thud(.35), 0),
      (S("result") + .05, thud(.55), 0), (S("result") + .3, zap(.1), -.3), (cue("result", "women"), zap(.08), .3),
      *[(S("record") + .2 + i * .125, zap(.05, .1), (i % 3 - 1) * .4) for i in range(14)], (cue("point", "hard work"), thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
