"""NOT JUST YOU · AFTER DARK – No. 48: post-sex blues are common (Schweitzer et al. 2015; Maczkowiack & Schweitzer 2019)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .8, "result": .5, "men": .5, "good": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "men", "good", "point", "end"]
EP = Episode(TL, 48, "THE BLUES", order=ORDER, dark=True, series="NOT JUST YOU · AFTER DARK",
             chapters={"hook": "AFTERWARDS", "study": "THE SURVEYS", "result": "WOMEN", "men": "MEN", "good": "EVEN WHEN", "point": "IT HAS A NAME"},
             sources=("Schweitzer et al. (2015), Sexual Medicine 3(4);", "Maczkowiack & Schweitzer (2019), JSMT 45(2)"),
             music=dict(bpm=76, root=-5, prog="minor", kick="half", gaps=[(E("study") + .05, S("result") + .05)]),
             cover=dict(words=["SAD", "AFTER?"], kicker="Even when it was good."))

def cloud(d, cx, cy, s=1.0, col=MID, t=0.0, rain=True):
    for dx, dy, r in ((-50, 10, 38), (0, -14, 52), (52, 8, 40), (0, 20, 40)):
        d.ellipse([cx + (dx - r) * s, cy + (dy - r) * s, cx + (dx + r) * s, cy + (dy + r) * s], fill=col)
    if rain:
        for i in range(5):
            x = cx + (-60 + i * 30) * s; ph = (t * 1.6 + i * .37) % 1
            y = cy + (60 + ph * 120) * s
            d.line([x, y, x - 6 * s, y + 22 * s], fill=SIG, width=int(5 * s))

def grid100(d, x0, y0, n, k, col, cell=56, gap=10):
    for i in range(100):
        r, c = divmod(i, 10); x = x0 + c * (cell + gap); y = y0 + r * (cell * .62 + gap)
        on = i < n * k
        d.rectangle([x, y, x + cell, y + cell * .62], fill=col if on else None, outline=INK if not on else col, width=2)

def sad_sitter(d, t, x=380, s=1.0, col=INK):
    bed(d, x - 240 * s, FLOOR, 480 * s, INK)
    picto(d, x + 80 * s, FLOOR - 50 * s, .8 * s, col, f=-1, pose=merge(SIT, {"tilt": 8, "arms": ((10, 30), (-10, -5))}), head_dy=8)

def sc_hook(img, d, t):
    d.text((X0 - 6, 300), "SAD", font=F(BLK, 230), fill=INK); d.text((X0 - 6, 510), "AFTER?", font=F(BLK, 170), fill=SIG)
    bed(d, 240, FLOOR, 480, INK)
    picto(d, 600, FLOOR - 90, .8, INK, f=-1, pose=merge(SIT, {"tilt": 10}), head_dy=10)
    cloud(d, 640, 760, .7 * ease((t - .5) / .4), MID, t)
    fig(d, "fig. 1 — right after, out of nowhere")

def sc_study(img, d, t):
    t0 = S("study"); tm = cue("study", "twelve hundred")
    d.text((X0, 300), "TWO SURVEYS", font=F(BLK, 120), fill=INK)
    box_label(d, X0, 470, "WOMEN · AUSTRALIA · 2015", 34, WHITE, SIG)
    for i in range(30):
        k = ease((t - t0 - .3 - i * .02) / .3)
        if k > 0: picto(d, X0 + 40 + (i % 15) * 58, 640 + (i // 15) * 110, .22, SIG, pose=IDLE)
    if t >= tm - .3:
        counter(d, X0, 860, t, tm - .3, .8, 1208, "{:,.0f} men", 110, INK)
    fig(d, "anonymous online questionnaires · Schweitzer et al.")

def sc_result(img, d, t):
    t0 = S("result")
    counter(d, X0, 300, t, t0 + .05, .8, 46, "{:.0f} %", 220, SIG)
    d.text((X0 + 6, 540), "of women · at least once", font=F(COND, 36), fill=INK)
    grid100(d, X0, 640, 46, clamp((t - t0 - .1) / 1.2), SIG)
    for i, (w, lab) in enumerate((("sad", "SAD"), ("tearful", "TEARFUL"), ("irritable", "IRRITABLE"))):
        tk = cue("result", w) - .2
        if t >= tk: box_label(d, X1, 340 + i * 66, lab, 30, WHITE, INK, anchor="ra")
    fig(d, "postcoital dysphoria, lifetime")

def sc_men(img, d, t):
    t0 = S("men"); tf = cue("men", "one in five")
    counter(d, X0, 300, t, t0 + .3, .8, 41, "{:.0f} %", 220, INK)
    d.text((X0 + 6, 540), "of men · at least once", font=F(COND, 36), fill=INK)
    grid100(d, X0, 640, 41, clamp((t - t0 - .3) / 1.2), INK)
    if t >= tf - .2:
        k = ease((t - tf + .2) / .4)
        grid100(d, X0, 640, 20, k, SIG)
        box_label(d, X1, 470, "20 % · LAST 4 WEEKS", 32, WHITE, SIG, anchor="ra")
    fig(d, "Maczkowiack & Schweitzer, 2019")

def sc_good(img, d, t):
    t0 = S("good"); tl = cue("good", "loving")
    d.text((X0, 300), "EVEN WHEN", font=F(BLK, 140), fill=INK); d.text((X0, 450), "IT'S GOOD.", font=F(BLK, 140), fill=SIG)
    bed(d, 160, FLOOR, 640, INK)
    picto(d, 380, FLOOR - 90, .75, INK, f=1, pose=merge(SIT, {"arms": ((60, 20), (-10, -5))})); picto(d, 560, FLOOR - 90, .75, SIG, f=-1, pose=merge(SIT, {"arms": ((60, 20), (-10, -5)), "tilt": 8}), head_dy=8)
    if t >= tl:
        r = 30 * back((t - tl) / .4); cx, cy = 470, 760
        d.ellipse([cx - r, cy - r * .9, cx, cy + r * .1], fill=SIG); d.ellipse([cx, cy - r * .9, cx + r, cy + r * .1], fill=SIG)
        d.polygon([(cx - r * .98, cy - r * .3), (cx + r * .98, cy - r * .3), (cx, cy + r * .95)], fill=SIG)
    cloud(d, 640, 700, .5 * ease((t - tl - .6) / .4), MID, t)
    fig(d, "a heart and a cloud at the same time")

def sc_point(img, d, t):
    t0 = S("point"); ts = cue("point", "say it")
    words_in(d, t, [("IT HAS A NAME:", t0, 300, 100, INK), ("POST-SEX", t0 + .5, 420, 150, SIG), ("BLUES.", t0 + .8, 570, 150, SIG)])
    picto(d, 300, FLOOR, .85, INK, f=1, pose=TALK(t) if t >= ts else IDLE); picto(d, 660, FLOOR, .85, SIG, f=-1, pose=OPEN if t >= cue("point", "not about") else IDLE)
    if t >= ts: speech_box(d, 330, 760, 330, (t - ts) / .3, INK, 1, "It's not you.", 32)
    fig(d, "fig. 2 — name it, don't hide it")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "men": sc_men, "good": sc_good, "point": sc_point}
FX = [(0.0, thud(.5), 0), (.5, whoosh(.8, .06), .3), *EP.cut_fx(), *[(S("study") + .3 + i * .1, tick(.035), (i % 5 - 2) / 3) for i in range(10)],
      (cue("study", "twelve hundred") - .3, pop(.15), 0), (S("result") + .05, thud(.55), 0),
      *[(cue("result", w) - .2, pop(.14), (i - 1) / 2) for i, w in enumerate(("sad", "tearful", "irritable"))],
      (S("men") + .3, thud(.4), 0), (cue("men", "one in five") - .2, riser(.4, .05), 0), (cue("good", "loving"), pop(.18), 0),
      (S("point") + .5, thud(.45), 0), (cue("point", "say it"), pop(.15), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
