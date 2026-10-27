"""NOT JUST YOU – No. 27: the denomination effect (Raghubir & Srivastava 2009). Area: money."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .8, "result": .6, "name": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "name", "point", "end"]
EP = Episode(TL, 27, "BREAK THE FIFTY", order=ORDER,
             chapters={"hook": "GONE BY FRIDAY", "study": "THE STUDY", "result": "THE RESULT", "name": "THE NAME", "point": "ONE PIECE"},
             sources=("Raghubir & Srivastava (2009), Journal of", "Consumer Research 36(4) · via NPR"),
             music=dict(bpm=100, root=3, prog="warm", kick="half", gaps=[(E("study") + .05, S("result") + .05)]),
             cover=dict(words=["BREAK", "THE 50?"], kicker="Why small change disappears."))

DAYS = ["MON", "TUE", "WED", "THU", "FRI"]
def sc_hook(img, d, t):
    bk = cue("hook", "break"); gf = cue("hook", "gone")
    d.text((X0 - 6, 300), "GONE." if t >= gf - .1 else "BREAK IT.", font=F(BLK, 190), fill=SIG if t >= gf - .1 else INK)
    for i, dname in enumerate(DAYS):
        x = X0 + i * 170; d.rectangle([x, 980, x + 150, 1080], outline=INK, width=4); d.text((x + 75, 1030), dname, font=F(COND, 30), fill=INK, anchor="mm")
    if t < bk: banknote(d, 480, 720, 1.6, "50")
    else:
        k = clamp((t - bk) / 1.8)
        for i in range(10):
            u = clamp(k * 1.4 - i * .07); x = lerp(480, X0 + 75 + (i % 5) * 170, u); y = lerp(720, 960 - (i // 5) * 40, u)
            if u < 1: (banknote(d, x, y, .5, "5") if i % 2 == 0 else coin(d, x, y, 26, INK, "1"))
            else: d.rectangle([X0 + 30 + (i % 5) * 170 + (i // 5) * 40, 1050, X0 + 60 + (i % 5) * 170 + (i // 5) * 40, 1066], fill=SIG)
    fig(d, "fig. 1 — a week of small change")

def pump(d, x, y, s=1.0):
    d.rectangle([x - 70 * s, y - 260 * s, x + 70 * s, y], fill=INK); d.rectangle([x - 50 * s, y - 230 * s, x + 50 * s, y - 160 * s], fill=WHITE)
    d.line([x + 70 * s, y - 200 * s, x + 120 * s, y - 200 * s, x + 120 * s, y - 60 * s], fill=INK, width=int(8 * s))

def sc_study(img, d, t):
    t0 = S("study"); ob = cue("study", "one bill"); fo = cue("study", "five ones")
    d.text((X0, 320), "$5, THREE WAYS", font=F(BLK, 104), fill=INK)
    pump(d, X1 - 90, 1100, .7)
    k1 = ease((t - ob + .1) / .3); k2 = ease((t - fo + .1) / .3)
    if k1 > 0: banknote(d, X0 + 150, 700, .9, "5"); box_label(d, X0 + 150, 790, "ONE BILL", 26, WHITE, INK, anchor="ma")
    if k2 > 0:
        for i in range(5): banknote(d, X0 + 360 + i * 14, 680 + i * 10, .55, "1")
        box_label(d, X0 + 420, 790, "FIVE ONES", 26, WHITE, INK, anchor="ma")
        for i in range(5): coin(d, X0 + 620 + (i % 3) * 56, 680 + (i // 3) * 56, 26, INK, "1")
        box_label(d, X0 + 680, 790, "FIVE COINS", 26, WHITE, INK, anchor="ma")
    fig(d, "gas-station survey thank-you · Raghubir & Srivastava, 2009")

def sc_result(img, d, t):
    t0 = S("result"); sb = cue("result", "single bill")
    d.text((X0, 320), "SPENT IT", font=F(BLK, 130), fill=INK)
    yb = 980
    for i, (lab, v, col) in enumerate((("five coins", .8, SIG), ("five ones", .68, SIG), ("one bill", .25, INK))):
        k = ease((t - t0 - .1 - i * .25) / .5); x = X0 + 60 + i * 280
        d.rectangle([x, yb - 420 * v * k, x + 180, yb], fill=col); d.text((x + 90, yb + 16), lab, font=F(COND, 30), fill=INK, anchor="ma")
    d.line([X0, yb, X1, yb], fill=INK, width=3)
    if t >= sb: note(d, X0 + 60 + 560 + 90, yb - 120, 860, 520, "mostly stayed in the pocket", (t - sb) / .35, INK, anchor="ra", size=28)
    d.text((X1, 1146), "schematic", font=F(MED, 22), fill=MID, anchor="ra")

def sc_name(img, d, t):
    t0 = S("name"); tw = cue("name", "too whole")
    words_in(d, t, [("DENOMINATION", cue("name", "denomination") - .1, 320, 118, INK), ("EFFECT.", cue("name", "effect") - .1, 460, 150, SIG)])
    banknote(d, 480, 820, 1.6, "50")
    if t >= tw:
        k = ease((t - tw) / .4)
        d.line([330, 820, 330 + 300 * k, 820], fill=SIG, width=6)
        note(d, 600, 760, 860, 1040, "feels too whole to break", (t - tw) / .35, SIG, anchor="ra", size=28)

def wallet(d, x, y, s=1.0):
    d.rounded_rectangle([x - 200 * s, y - 120 * s, x + 200 * s, y + 120 * s], radius=24 * s, fill=INK)
    d.rounded_rectangle([x + 90 * s, y - 30 * s, x + 220 * s, y + 30 * s], radius=14 * s, fill=INK); d.ellipse([x + 160 * s, y - 12 * s, x + 184 * s, y + 12 * s], fill=SIG)

def sc_point(img, d, t):
    t0 = S("point")
    words_in(d, t, [("KEEP IT IN", cue("point", "keep") - .1, 300, 130, INK), ("ONE PIECE.", cue("point", "one piece") - .1, 440, 150, SIG)])
    banknote(d, 480, 760 + 40 * (1 - ease((t - t0 - .3) / .5)), 1.3, "50")
    wallet(d, 480, 920, 1.1)
    fig(d, "fig. 2 — a small trick for saving")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "name": sc_name, "point": sc_point}
FX = [(0.0, thud(.5), 0), (cue("hook", "break"), rewind_sfx(.12, .4), 0), *[(cue("hook", "break") + i * .18, tick(.06), (i % 5 - 2) / 3) for i in range(10)],
      (cue("hook", "gone"), thud(.45), 0), *EP.cut_fx(), (cue("study", "one bill"), pop(.18), -.3), (cue("study", "five ones"), pop(.18), .3),
      (S("result") + .05, thud(.5), 0), (cue("result", "single bill"), pop(.15), .3), (cue("name", "denomination") - .1, thud(.4), 0),
      (cue("name", "too whole"), whoosh(.4, .1), 0), (cue("point", "one piece"), thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
