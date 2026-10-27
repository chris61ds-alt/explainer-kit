"""NOT JUST YOU – No. 20: the first-night effect (Tamaki, Bang, Watanabe & Sasaki 2016). Area: sleep."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .45, "study": .8, "result": .5, "sound": .5, "second": .5, "name": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "sound", "second", "name", "end"]
EP = Episode(TL, 20, "FIRST NIGHT", order=ORDER,
             chapters={"hook": "3 A.M.", "study": "THE SCAN", "result": "ONE HALF", "sound": "THE SOUNDS", "second": "NIGHT TWO", "name": "NIGHT WATCH"},
             sources=("Tamaki, Bang, Watanabe & Sasaki (2016),", "Current Biology 26(9)"),
             music=dict(bpm=80, root=-4, prog="dream", kick="half", gaps=[(E("study") + .05, S("result") + .05)]),
             cover=dict(words=["NEW", "BED?"], kicker="Why the first night is always bad."))

def sleeper(d, x0, y, t, awake=True):
    bed(d, x0, y, 520)
    d.ellipse([x0 + 50, y - 170, x0 + 130, y - 90], fill=INK)                       # head on the pillow
    d.rounded_rectangle([x0 + 120, y - 130, x0 + 500, y - 70], radius=30, fill=MID)   # blanket
    if awake: eye(d, x0 + 90, y - 200, .55, SIG, look=(.6, -.4))
    else:
        for i in range(3): d.text((x0 + 150 + i * 36, y - 220 - i * 30), "z", font=F(BLK, 30 + i * 8), fill=MID)

def sc_hook(img, d, t):
    d.text((X0 - 6, 300), "3 A.M.", font=F(BLK, 220), fill=INK)
    sleeper(d, X0 + 40, 1060, t, awake=True)
    clock(d, 760, 620, 90, minutes=180 + t * 4)
    d.rectangle([X0 + 20, 560, X0 + 240, 640], outline=INK, width=4); d.text((X0 + 130, 600), "ROOM 214", font=F(COND, 34), fill=INK, anchor="mm")
    if t >= cue("hook", "terribly"): note(d, X0 + 130, 860, 520, 760, "wide awake", (t - cue("hook", "terribly")) / .35, SIG, size=28)
    fig(d, "fig. 1 — the first night somewhere new")

def brain(d, cx, cy, kl, kr, t, labels=True):
    """top view: left and right hemispheres; k = alertness 0..1"""
    for side, k in ((-1, kl), (1, kr)):
        x0 = cx - 220 if side < 0 else cx + 10; x1 = cx - 10 if side < 0 else cx + 220
        pulse = 1 + .03 * math.sin(t * 6) * k
        d.ellipse([x0, cy - 260 * pulse, x1, cy + 260 * pulse], fill=mix(RULE, SIG, k), outline=INK, width=6)
        for i in range(4):
            yy = cy - 180 + i * 110; d.arc([x0 + 30, yy, x1 - 30, yy + 80], 200, 340, fill=mix(MID, WHITE, k), width=4)
    if labels:
        d.text((cx - 115, cy + 290), "LEFT", font=F(COND, 32), fill=INK, anchor="ma"); d.text((cx + 115, cy + 290), "RIGHT", font=F(COND, 32), fill=INK, anchor="ma")

def eeg(d, x0, x1, y, t, amp, col):
    pts = [(x0 + (x1 - x0) * i / 80, y + amp * math.sin(i * .9 + t * 8) * (.5 + .5 * math.sin(i * .21))) for i in range(81)]
    d.line(pts, fill=col, width=3)

def sc_study(img, d, t):
    t0 = S("study")
    d.text((X0, 320), "NIGHT 1", font=F(BLK, 130), fill=INK)
    brain(d, 480, 760, 0, 0, t)
    for i in range(3): eeg(d, X0, X1, 1110 - i * 24, t + i, 8, MID)
    fig(d, "Tamaki et al. — Current Biology, 2016 · EEG, MEG, MRI")

def sc_result(img, d, t):
    t0 = S("result"); lk = ease((t - cue("result", "left") + .2) / .6)
    d.text((X0, 320), "ONE HALF AWAKE", font=F(BLK, 96), fill=INK)
    brain(d, 480, 760, lk, 0, t)
    if lk > .9:
        note(d, 330, 700, X0 + 10, 520, "more alert", 1, SIG, anchor="la", size=30)
        note(d, 630, 700, X1 - 10, 520, "deep sleep", 1, INK, anchor="ra", size=30)
    fig(d, "fig. 2 — slow-wave sleep, night 1")

def speaker(d, x, y, s=1.0, k=0.0):
    d.rectangle([x - 30 * s, y - 30 * s, x, y + 30 * s], fill=INK); d.polygon([(x, y - 30 * s), (x + 50 * s, y - 70 * s), (x + 50 * s, y + 70 * s), (x, y + 30 * s)], fill=INK)
    for i in range(3):
        if k > i * .3:
            r = 70 + i * 34; d.arc([x + 20 - r, y - r, x + 20 + r, y + r], -40, 40, fill=SIG, width=6)

def sc_sound(img, d, t):
    t0 = S("sound"); st = cue("sound", "strange"); wk = cue("sound", "woke")
    d.text((X0, 320), "BEEP?", font=F(BLK, 130), fill=SIG)
    brain(d, 560, 790, 1.0, 0, t, labels=False)
    speaker(d, X0 + 40, 600, 1.0, (t - st) / .6 if t >= st else 0)
    if t >= st:
        k = ease((t - st) / .5); d.line([X0 + 140, 600, lerp(X0 + 140, 430, k), lerp(600, 760, k)], fill=SIG, width=5)
    if t >= wk - .1:
        box_label(d, 560, 1080, "WOKE UP FASTER", 32, WHITE, SIG, anchor="ma")
    fig(d, "deviant sounds · faster waking when the left side was stimulated")

def sc_second(img, d, t):
    t0 = S("second"); k = ease((t - t0) / .8)
    d.text((X0, 320), "NIGHT 2", font=F(BLK, 130), fill=INK)
    brain(d, 480, 760, lerp(1.0, 0, k), 0, t)
    if k > .9: dim_h(d, 270, 690, 1110, (t - t0 - .8) / .4, INK, "NO DIFFERENCE", 24)

def sc_name(img, d, t):
    t0 = S("name"); nw = cue("name", "night watch")
    words_in(d, t, [("FIRST-NIGHT", cue("name", "first") - .1, 320, 140, INK), ("EFFECT.", cue("name", "effect") - .1, 480, 140, SIG)])
    sleeper(d, X0 + 40, 1060, t, awake=False)
    if t >= nw - .2:
        eye(d, X0 + 90, 760, .9 * ease((t - nw + .2) / .3), SIG, look=(1, 0))
        note(d, X0 + 140, 760, 700, 700, "the night watch", (t - nw) / .35, SIG, size=30)

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "sound": sc_sound, "second": sc_second, "name": sc_name}
def beep(amp=.08, f=1800, dur=.12):
    t = tt_(dur); return amp * np.sin(2 * np.pi * f * t) * np.exp(-t * 20)
FX = [(0.0, thud(.45), 0), (cue("hook", "terribly"), pop(.15), .2), *EP.cut_fx(), (S("result") + .05, thud(.5), 0),
      (cue("result", "left"), riser(.6, .06), -.4), *[(cue("sound", "strange") + i * .25, beep(.08), .8) for i in range(3)],
      (cue("sound", "woke"), pop(.2), 0), (S("second") + .2, whoosh(.8, .08), 0), (cue("name", "first") - .1, thud(.4), 0),
      (cue("name", "night watch"), pop(.18), -.3), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
