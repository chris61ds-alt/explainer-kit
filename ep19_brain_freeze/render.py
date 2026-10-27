"""NOT JUST YOU – No. 19: brain freeze (Kaczorowski & Kaczorowski 2002, BMJ). Area: body."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .45, "study": .8, "result": .5, "why": .5, "tip": .5, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "why", "tip", "point", "end"]
EP = Episode(TL, 19, "BRAIN FREEZE", order=ORDER,
             chapters={"hook": "OUCH", "study": "THE STUDY", "result": "THE RESULT", "why": "WHY", "tip": "THE FIX", "point": "WRONG ADDRESS"},
             sources=("Kaczorowski & Kaczorowski (2002), BMJ 325", "via Wikipedia: cold-stimulus headache"),
             music=dict(bpm=110, root=2, prog="major", kick="four", gaps=[(E("study") + .05, S("result") + .05)]),
             cover=dict(words=["BRAIN", "FREEZE."], kicker="It's not your brain."))

def cone(d, x, y, s=1.0, bite=0.0):
    d.polygon([(x - 50 * s, y - 120 * s), (x + 50 * s, y - 120 * s), (x, y + 40 * s)], fill=INK)
    for i in range(4): d.line([x - 40 * s + i * 24 * s, y - 116 * s, x - 10 * s + i * 14 * s, y - 40 * s], fill=MID, width=int(3 * s))
    r = 60 * s * (1 - .4 * bite); d.ellipse([x - r, y - 120 * s - r * 1.4, x + r, y - 120 * s + r * .4], fill=SIG)

def bolt(d, x, y, s=1.0, col=SIG):
    d.polygon([(x, y - 60 * s), (x - 30 * s, y + 6 * s), (x - 4 * s, y + 6 * s), (x - 14 * s, y + 60 * s), (x + 30 * s, y - 10 * s), (x + 4 * s, y - 10 * s), (x + 14 * s, y - 60 * s)], fill=col)

def profile(d, cx, cy, r):
    """side view of a head facing right"""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=8)
    d.polygon([(cx + r * .96, cy - r * .05), (cx + r * 1.22, cy + r * .2), (cx + r * .92, cy + r * .28)], fill=INK)    # nose
    d.line([cx + r * .55, cy + r * .5, cx + r * .9, cy + r * .5], fill=INK, width=6)                                     # mouth
    d.arc([cx + r * .05, cy + r * .2, cx + r * .9, cy + r * .7], 180, 360, fill=INK, width=4)                          # palate
    d.rectangle([cx - r * .3, cy + r * .95, cx + r * .2, cy + r * 1.35], fill=INK)

def sc_hook(img, d, t):
    d.text((X0 - 6, 300), "OUCH.", font=F(BLK, 220), fill=INK)
    ex = cue("hook", "explodes")
    h = picto(d, 360, FLOOR, 1.05, INK, f=1, pose=TALK(t) if t < ex - .2 else FACEPALM)
    cone(d, 640, 940, .9, bite=clamp((t - .8) / 1.0))
    if t >= ex - .1:
        k = back((t - ex + .1) / .3); bolt(d, h[0] + 10, h[1] - 90, 1.1 * k)
        note(d, h[0] + 30, h[1] - 60, 760, 600, "forehead", (t - ex) / .35, SIG, anchor="ra", size=30)
    fig(d, "fig. 1 — one spoon too many")

def stopwatch(d, cx, cy, r, t, sec, col=INK):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=8); d.rectangle([cx - 14, cy - r - 30, cx + 14, cy - r], fill=col)
    a = math.radians(-90 + 360 * ((t * (60 / sec) / 60) % 1)); d.line([cx, cy, cx + math.cos(a) * r * .8, cy + math.sin(a) * r * .8], fill=SIG, width=6)

def sc_study(img, d, t):
    t0 = S("study"); fs = cue("study", "fast")
    d.text((X0, 320), "FAST VS. SLOW", font=F(BLK, 110), fill=INK)
    for i, (lab, sec, col, tk) in enumerate((("under 5 s", 5, SIG, fs), ("over 30 s", 30, INK, cue("study", "slowly")))):
        k = ease((t - tk + .2) / .35)
        if k <= 0: continue
        x = X0 + 200 + i * 440
        stopwatch(d, x, 620, 90 * k, t, sec, col)
        picto(d, x, FLOOR, .6, col, pose={"arms": ((120 + 40 * math.sin(t * (14 if i == 0 else 3)), 120), (-10, -5))})
        cone(d, x + 90, 1010, .45)
        box_label(d, x, 740, lab, 30, WHITE, col, anchor="ma")
    fig(d, "Kaczorowski & Kaczorowski — BMJ, 2002 · middle-school students")

def sc_result(img, d, t):
    t0 = S("result")
    d.text((X0, 320), "BRAIN FREEZE", font=F(BLK, 110), fill=INK)
    counter(d, X0, 470, t, cue("result", "fast") - .2, .8, 27, "{:.0f} %", 190, SIG)
    d.text((X0 + 6, 680), "ate fast", font=F(COND, 34), fill=INK)
    counter(d, X0 + 450, 470, t, cue("result", "slowly") - .1, .8, 12, "{:.0f} %", 190, INK)
    if t >= cue("result", "slowly") - .1: d.text((X0 + 456, 680), "ate slowly", font=F(COND, 34), fill=INK)
    for i in range(20):
        r, c = divmod(i, 10); x = X0 + 40 + c * 84; y = 860 + r * 110
        picto(d, x, y, .28, SIG if (i < 5 and t >= cue("result", "fast")) else MID, pose=IDLE)
    d.text((X1, 1146), "≈ 1 in 4 vs. ≈ 1 in 8", font=F(MED, 22), fill=MID, anchor="ra")

def sc_why(img, d, t):
    t0 = S("why"); fh = cue("why", "forehead")
    d.text((X0, 320), "REFERRED PAIN", font=F(BLK, 104), fill=INK)
    cx, cy, r = 420, 760, 230
    profile(d, cx, cy, r)
    k1 = ease((t - cue("why", "roof")) / .4)
    if k1 > 0:
        for i in range(6): d.line([cx + r * (.2 + i * .1), cy + r * .32, cx + r * (.2 + i * .1), cy + r * .42], fill=SIG, width=5)
        note(d, cx + r * .5, cy + r * .4, 820, 1060, "cold here", k1 * 1.2, INK, anchor="ra", size=28)
    if t >= fh - .3:
        k = ease((t - fh + .3) / .6)
        pts = [(cx + r * .5, cy + r * .35), (cx + r * .1, cy), (cx + r * .2, cy - r * .4), (cx + r * .65, cy - r * .62)]
        n = int(30 * k)
        for i in range(n):
            u = i / 30; seg_ = min(2, int(u * 3)); uu = u * 3 - seg_
            a, b = pts[seg_], pts[seg_ + 1]
            if i % 2 == 0: d.ellipse([lerp(a[0], b[0], uu) - 5, lerp(a[1], b[1], uu) - 5, lerp(a[0], b[0], uu) + 5, lerp(a[1], b[1], uu) + 5], fill=SIG)
        if k > .95:
            bolt(d, cx + r * .65, cy - r * .62, .8)
            note(d, cx + r * .7, cy - r * .62, 860, 470, "felt here", 1, SIG, anchor="ra", size=28)
    fig(d, "fig. 2 — the trigeminal nerve sends the signal on")

def sc_tip(img, d, t):
    t0 = S("tip"); pr = cue("tip", "press")
    d.text((X0, 320), "TONGUE UP", font=F(BLK, 130), fill=SIG)
    cx, cy, r = 420, 760, 230
    profile(d, cx, cy, r)
    up = ease((t - pr) / .5)
    d.pieslice([cx + r * .15, cy + r * (.38 - .1 * up), cx + r * .85, cy + r * (.75 - .1 * up)], 180, 360, fill=SIG)
    if t >= cue("tip", "warm"): note(d, cx + r * .5, cy + r * .3, 860, 1060, "warms the palate", (t - cue("tip", "warm")) / .35, INK, anchor="ra", size=28)
    fig(d, "fig. 3 — or a sip of warm water")

def parcel(d, x, y, k, stamp=0.0):
    if k <= 0: return
    e = ease(k); xx = lerp(x + 300, x, e)
    d.rectangle([xx, y, xx + 420, y + 260], fill=WHITE, outline=INK, width=6)
    d.line([xx, y + 60, xx + 420, y + 60], fill=INK, width=4)
    d.text((xx + 24, y + 90), "TO:", font=F(COND, 28), fill=MID)
    d.text((xx + 24, y + 126), "roof of the mouth", font=F(BLK, 40), fill=INK)
    d.text((xx + 24, y + 190), "delivered: forehead", font=F(COND, 30), fill=SIG)
    if stamp > 0:
        s = back(stamp); d.rectangle([xx + 230 - 140 * s, y - 40 - 40 * s, xx + 230 + 140 * s, y - 40 + 40 * s], outline=SIG, width=8)
        if s > .7: d.text((xx + 230, y - 40), "WRONG ADDRESS", font=F(BLK, 34), fill=SIG, anchor="mm")

def sc_point(img, d, t):
    t0 = S("point"); wa = cue("point", "wrong address")
    words_in(d, t, [("NOT FROZEN.", t0, 300, 150, INK)])
    parcel(d, X0 + 120, 640, (t - t0 - .3) / .5, (t - wa + .1) / .3)
    fig(d, "fig. 4 — a delivery error, not a frozen brain")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "why": sc_why, "tip": sc_tip, "point": sc_point}
FX = [(0.0, thud(.5), 0), (.8, pop(.12), .2), (cue("hook", "explodes") - .1, thud(.55), 0), (cue("hook", "explodes"), riser(.4, .08), 0), *EP.cut_fx(),
      (cue("study", "fast"), pop(.2), -.3), (cue("study", "slowly"), pop(.2), .3), (S("result") + .05, thud(.5), 0),
      (cue("result", "slowly"), thud(.35), 0), (cue("why", "roof"), pop(.15), .2), (cue("why", "forehead"), whoosh(.5, .12), -.2),
      (cue("tip", "press"), pop(.2), 0), (cue("point", "wrong address"), thud(.55), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
