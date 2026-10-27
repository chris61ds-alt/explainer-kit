"""NOT JUST YOU – No. 21: sleep inspires insight (Wagner, Gais, Haider, Verleger & Born 2004). Area: sleep."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .6, "study": .9, "result": .6, "detail": .6, "point": .8, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "detail", "point", "end"]
EP = Episode(TL, 21, "SLEEP ON IT", order=ORDER,
             chapters={"hook": "STUCK", "study": "THE PUZZLE", "result": "THE RESULT", "detail": "THE CATCH", "point": "PART OF THE WORK"},
             sources=("Wagner, Gais, Haider, Verleger & Born (2004),", "Nature 427"),
             music=dict(bpm=84, root=-3, prog="dream", kick="half", gaps=[(E("study") + .05, S("result") + .05)]),
             cover=dict(words=["SLEEP", "ON IT."], kicker="Your brain keeps working."))

def bulb(d, cx, cy, s=1.0, on=0.0):
    d.ellipse([cx - 60 * s, cy - 80 * s, cx + 60 * s, cy + 40 * s], fill=mix(WHITE, SIG, on), outline=INK, width=int(6 * s))
    d.rectangle([cx - 30 * s, cy + 36 * s, cx + 30 * s, cy + 80 * s], fill=INK)
    if on > .5:
        for i in range(7):
            a = math.radians(-180 + i * 30); d.line([cx + math.cos(a) * 90 * s, cy - 20 * s + math.sin(a) * 90 * s, cx + math.cos(a) * 130 * s, cy - 20 * s + math.sin(a) * 130 * s], fill=SIG, width=int(6 * s))

def tangle(d, cx, cy, r, t, col=INK):
    rng = np.random.default_rng(2); pts = [(cx + rng.uniform(-r, r), cy + rng.uniform(-r, r) * .6) for _ in range(18)]
    d.line(pts, fill=col, width=4, joint="curve")

def sc_hook(img, d, t):
    gb = cue("hook", "go to bed")
    if t < gb - .1:
        d.text((X0 - 6, 300), "STUCK?", font=F(BLK, 220), fill=INK)
        picto(d, 300, FLOOR, 1.0, INK, f=1, pose=WORRY)
        d.rectangle([480, 640, 860, 900], outline=INK, width=5); tangle(d, 670, 770, 150, t)
    else:
        words_in(d, t, [("GO TO BED.", gb - .1, 300, 160, SIG)])
        bed(d, X0 + 120, 1080, 600)
        d.ellipse([X0 + 180, 870, X0 + 260, 950], fill=INK); d.rounded_rectangle([X0 + 250, 910, X0 + 690, 970], radius=30, fill=MID)
        for i in range(3): d.text((X0 + 300 + i * 40, 840 - i * 34), "z", font=F(BLK, 34 + i * 10), fill=MID)
    fig(d, "fig. 1 — the problem stays on the desk")

DIG = [1, 1, 4, 4, 9, 4, 9, 1]
def sc_study(img, d, t):
    t0 = S("study"); sc = cue("study", "shortcut")
    d.text((X0, 320), "THE PUZZLE", font=F(BLK, 130), fill=INK)
    for r in range(3):
        k = ease((t - t0 - .3 - r * .5) / .4)
        if k <= 0: continue
        y = 520 + r * 120
        for i, v in enumerate(DIG):
            x = X0 + i * 92
            d.rectangle([x, y, x + 78, y + 90], outline=INK, width=4, fill=SIG if (r == 1 and i == 1 and t >= sc) else None)
            d.text((x + 39, y + 45), str((v + r * 3) % 9 + 1 if r else v), font=F(BLK, 48), fill=WHITE if (r == 1 and i == 1 and t >= sc) else INK, anchor="mm")
    if t >= sc:
        note(d, X0 + 92 + 39, 700, 560, 960, "hidden shortcut: the answer shows up early", (t - sc) / .4, SIG, anchor="la", size=26)
    fig(d, "number reduction task · Wagner et al. — Nature, 2004")

def sc_result(img, d, t):
    t0 = S("result")
    d.text((X0, 320), "FOUND IT", font=F(BLK, 130), fill=INK)
    for i, (lab, v, col, dl) in enumerate((("stayed awake", .35, MID, .2), ("slept 8 hours", .75, SIG, cue("result", "twice") - t0))):
        x = X0 + 120 + i * 380; yb = 1040; k = ease((t - t0 - dl) / .6)
        d.rectangle([x, yb - 480 * v * k, x + 220, yb], fill=col)
        d.text((x + 110, yb + 18), lab, font=F(COND, 30), fill=INK, anchor="ma")
        if i == 1 and k > 0:
            picto(d, x + 110, yb - 480 * v * k - 10, .4, INK, pose=OPEN); bulb(d, x + 220, yb - 480 * v * k - 160, .45, 1)
    d.line([X0, 1040, X1, 1040], fill=INK, width=3)
    if t >= cue("result", "twice") + .5: dim_v(d, X1 - 30, 1040 - 480 * .75, 1040 - 480 * .35, (t - cue("result", "twice") - .5) / .4, SIG, "×2+")
    d.text((X1, 1146), "schematic · more than twice as many", font=F(MED, 22), fill=MID, anchor="ra")

def sc_detail(img, d, t):
    t0 = S("detail")
    d.text((X0, 320), "THE CATCH", font=F(BLK, 130), fill=INK)
    rows = [("practised + slept", True, True), ("no practice + slept", False, True)]
    for i, (lab, pr, sl) in enumerate(rows):
        k = ease((t - t0 - .2 - i * .6) / .4)
        if k <= 0: continue
        y = 540 + i * 220
        d.rectangle([X0, y, X1, y + 170], outline=INK, width=4)
        d.text((X0 + 30, y + 85), lab, font=F(BLK, 48), fill=INK, anchor="lm")
        bulb(d, X1 - 110, y + 85, .6, 1.0 if pr else 0.0)
        if not pr: d.line([X1 - 180, y + 20, X1 - 40, y + 150], fill=INK, width=8)
    fig(d, "sleep didn't help without initial training")

def sc_point(img, d, t):
    t0 = S("point")
    words_in(d, t, [("NOT", t0, 300, 150, INK), ("GIVING UP.", t0 + .2, 450, 150, INK)] if t < cue("point", "part") - .1
             else [("PART OF", cue("point", "part") - .1, 300, 150, INK), ("THE WORK.", cue("point", "part"), 450, 150, SIG)])
    bed(d, X0 + 120, 1080, 600)
    d.ellipse([X0 + 180, 870, X0 + 260, 950], fill=INK); d.rounded_rectangle([X0 + 250, 910, X0 + 690, 970], radius=30, fill=MID)
    bulb(d, X0 + 220, 740, .6, ease((t - cue("point", "part")) / .4))
    fig(d, "fig. 2 — overnight processing")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "detail": sc_detail, "point": sc_point}
FX = [(0.0, thud(.5), 0), (cue("hook", "go to bed") - .1, thud(.45), 0), (cue("hook", "go to bed"), rewind_sfx(.08, .5), 0), *EP.cut_fx(),
      *[(S("study") + .3 + r * .5, pop(.12), (r - 1) / 2) for r in range(3)], (cue("study", "shortcut"), pop(.2), -.2),
      (S("result") + .05, thud(.45), 0), (cue("result", "twice"), riser(.5, .07), .3), (cue("result", "twice") + .5, thud(.4), 0),
      (S("detail") + .2, pop(.15), 0), (S("detail") + .8, pop(.15), 0), (cue("point", "part"), thud(.5), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
