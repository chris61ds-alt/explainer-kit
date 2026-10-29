"""NOT JUST YOU – No. 64: swearing raises pain tolerance (Stephens, Atkins & Kingston 2009). Look C+D, dark."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from thread import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .8, "result": .5, "pain": .5, "why": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "pain", "why", "point", "end"]
EP = ThreadEpisode(TL, 64, "#@!%", order=ORDER, dark=True,
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Stephens, Atkins & Kingston (2009),", "NeuroReport 20(12)"),
                   music=dict(bpm=110, root=1, prog="tense", kick="four", gaps=[(E("study") + .05, S("result") + .05)]),
                   cover=dict(words=["SWEAR.", "IT HELPS."], kicker="Science says so."))

def bucket(d, x, y, t, col=INK):
    d.polygon([(x - 160, y - 220), (x + 160, y - 220), (x + 130, y), (x - 130, y)], outline=col, width=6)
    for i in range(5):
        yy = y - 170 + i * 36 + 4 * math.sin(t * 3 + i); d.line([x - 140 + i * 4, yy, x + 140 - i * 4, yy], fill=mix(BG, MID, .6), width=3)
    for (cx, cy) in ((x - 70, y - 190), (x + 40, y - 175), (x + 100, y - 200)): d.rectangle([cx - 22, cy - 18, cx + 22, cy + 18], outline=col, width=3)

def sc_hook(img, d, t):
    k = .5 + .5 * math.sin(t * 10)
    d.text((X0 - 6, 320), "#@!%", font=F(BLK, 300), fill=SIG)
    if t > .5 and int(t * 10) % 4 == 0: glitch(img, (X0, 320, X1, 620), .9, seed=int(t * 30))
    silhouette(img, lambda m: front_bust(m, 480, 820, .8, 255), (100, 680, 860, 1130), INK, cell=10)
    d.text((X0, 650), "it actually helps", font=F(COND, 46), fill=INK)
    fig(d, "fig. 1 — the reflex")

def sc_study(img, d, t):
    t0, tn = S("study"), cue("study", "once repeating a neutral") - .2
    d.text((X0, 320), "ICE WATER.", font=F(BLK, 150), fill=INK)
    bucket(d, 480, 1060, t)
    def arm(m):
        m.polygon([(180, 560), (260, 540), (470, 930), (410, 960)], fill=255)
        m.ellipse([380, 900, 500, 1010], fill=255)
    silhouette(img, arm, (150, 520, 560, 1020), INK, cell=8)
    clock(d, 760, 640, 70, t, None, SIG, 1.0)
    if t >= cue("study", "once repeating a swear") - .2: speech_box(d, 560, 470, 200, (t - cue("study", "once repeating a swear") + .2) / .3, SIG, 1, "#@!%", 40)
    if t >= tn: speech_box(d, 470, 560, 200, (t - tn) / .3, INK, -1, "table", 34)
    fig(d, "67 students · cold-pressor test · 2009")

def sc_result(img, d, t):
    t0 = S("result")
    counter(d, X0, 320, t, t0 + .1, .7, 40, "+{:.0f} SEC", 200, SIG)
    d.text((X0 + 6, 540), "hand in ice water, while swearing", font=F(COND, 40), fill=INK)
    hbar(d, 660, 119 / 200, (t - t0 - .3) / .5, MID, "neutral word ≈ 119 s", h=90)
    hbar(d, 840, 160 / 200, (t - t0 - .7) / .5, SIG, "swear word ≈ 160 s", h=90)
    fig(d, "men 147 to 191 s · women 83 to 120 s")

def sc_pain(img, d, t):
    t0 = S("pain"); th = cue("pain", "heart rate") - .2
    d.text((X0, 320), "HURT LESS.", font=F(BLK, 160), fill=SIG)
    if t >= th:
        d.text((X0, 500), "PULSE UP.", font=F(BLK, 160), fill=INK)
        d.line(ekg(LX, RX, THREAD_Y + 60, t, period=150, amp=70, speed=420), fill=SIG, width=6)
    else:
        d.line(ekg(LX, RX, THREAD_Y + 60, t, period=230, amp=45, speed=220), fill=SIG, width=6)
    fig(d, "lower pain ratings · higher heart rate")

def sc_why(img, d, t):
    t0 = S("why")
    d.text((X0, 320), "FIGHT", font=F(BLK, 170), fill=INK); d.text((X0, 500), "OR FLIGHT.", font=F(BLK, 150), fill=SIG)
    silhouette(img, lambda m: body(m, 480, 1120, 380, 255, arm=.55, step=.4), (260, 720, 700, 1125), SIG, cell=8)
    fig(d, "one explanation, not fully settled")

def sc_point(img, d, t):
    t0, tl = S("point"), cue("point", "let it out") - .2
    words_in(d, t, [("NEXT TIME", t0, 320, 150, INK), ("LET IT OUT.", tl, 480, 150, SIG)])
    if t >= tl:
        d.text((X0, 700), "#@!%", font=F(BLK, 240), fill=INK)
        if t < tl + .4: glitch(img, (X0, 700, X1, 960), 1.2, seed=int(t * 30))
    fig(d, "fig. 2 — within reason")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "pain": sc_pain, "why": sc_why, "point": sc_point}
def bleep(amp=.05, dur=.45):
    tt = tt_(dur); return amp * np.sin(2 * np.pi * 1000 * tt) * np.minimum(1, np.minimum(tt, dur - tt) * 60)
FX = [(0.0, bleep(.05, .35), 0), (.05, thud(.5), 0), *EP.cut_fx(), (cue("study", "once repeating a swear") - .2, bleep(.04, .25), .3),
      (cue("study", "once repeating a neutral") - .2, pop(.12), -.3), (S("result") + .05, thud(.55), 0), (S("result") + .7, riser(.5, .05), 0),
      (cue("pain", "heart rate") - .2, softkick(.2), 0), (S("why") + .1, thud(.4), 0), (cue("point", "let it out") - .2, bleep(.05, .4), 0),
      (cue("point", "let it out") - .1, thud(.5), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
