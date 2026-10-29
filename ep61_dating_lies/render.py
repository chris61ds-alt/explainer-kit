"""NOT JUST YOU – No. 61: lies in online dating profiles (Toma, Hancock & Ellison 2008). Look C+D (type + halftone), dark."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from thread import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .8, "result": .5, "how": .5, "small": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "how", "small", "point", "end"]
EP = ThreadEpisode(TL, 61, "PROFILE LIES", order=ORDER, dark=True, label="SMALL STUDY",
                   chapters={"hook": "", "study": "", "result": "", "how": "", "small": "", "point": ""},
                   sources=("Toma, Hancock & Ellison (2008), Personality and", "Social Psychology Bulletin 34(8)"),
                   music=dict(bpm=100, root=-2, prog="tense", kick="four", gaps=[(E("study") + .05, S("result") + .05)]),
                   cover=dict(words=["YOUR DATE", "LIED."], kicker="81 % of profiles do."))

def profile_card(img, d, x, y, t, k=1.0, fields=(("AGE", "29"), ("HEIGHT", "6'0\""), ("WEIGHT", "160 lb")), marks=()):
    w, h = 420, 560
    d.rounded_rectangle([x, y, x + w, y + h], radius=34, outline=INK, width=5)
    silhouette(img, lambda m: front_bust(m, x + w / 2, y + 150, .62, 255), (x + 10, y + 20, x + w - 10, y + 330), INK, cell=9, k=k)
    for i, (a, b) in enumerate(fields):
        yy = y + 360 + i * 60
        d.text((x + 30, yy), a, font=F(MONO, 24), fill=MID); d.text((x + w - 30, yy), b, font=F(BLK, 36), fill=SIG if i in marks else INK, anchor="ra")
        if i in marks: d.line([x + w - 160, yy + 22, x + w - 26, yy + 22], fill=SIG, width=5)

def sc_hook(img, d, t):
    t8 = cue("hook", "eighty-one") - .2
    d.text((X0 - 6, 320), "YOUR DATE", font=F(BLK, 150), fill=INK); d.text((X0 - 6, 470), "LIED.", font=F(BLK, 150), fill=SIG)
    profile_card(img, d, 480, 640 - 0, t, marks=(0, 1, 2) if t >= t8 else ())
    if t >= t8: counter(d, X0, 700, t, t8, .5, 81, "{:.0f} %", 160, SIG); d.text((X0 + 6, 880), "do", font=F(COND, 44), fill=INK)
    fig(d, "fig. 1 — the profile")

def sc_study(img, d, t):
    t0 = S("study")
    counter(d, X0, 320, t, t0 + .1, .7, 80, "{:.0f}", 230, SIG)
    d.text((X0 + 6, 560), "online daters, checked in person", font=F(COND, 40), fill=INK)
    ruler(d, 700, X0, X1, ["5'0\"", "5'6\"", "6'0\"", "6'6\""], minor=35)
    silhouette(img, lambda m: body(m, 300, 1120, 400, 255), (150, 680, 460, 1130), INK, cell=8)
    k = ease((t - cue("study", "checked their id") + .2) / .3) if "checked their id" in TL.T["study"]["text"].lower() else ease((t - t0 - 1.5) / .3)
    if k > 0:
        x0, y0 = 560, 820; d.rounded_rectangle([x0, y0, x0 + 320, y0 + 200], radius=16, outline=INK, width=4)
        d.rectangle([x0 + 24, y0 + 30, x0 + 120, y0 + 150], fill=MID); d.rectangle([x0 + 140, y0 + 40, x0 + 290, y0 + 56], fill=INK)
        d.rectangle([x0 + 140, y0 + 80, x0 + 260, y0 + 94], fill=MID); d.text((x0 + 140, y0 + 120), "DOB ··/··/····", font=F(MONO, 22), fill=SIG)
    fig(d, "height and weight measured, age from ID")

def sc_result(img, d, t):
    t0 = S("result")
    counter(d, X0, 320, t, t0 + .1, .8, 81, "{:.0f} %", 230, SIG)
    d.text((X0 + 6, 560), "fudged at least one number", font=F(COND, 40), fill=INK)
    k = clamp((t - t0 - .2) / 1.4)
    for i in range(100):
        r, c = divmod(i, 10); x = X0 + c * 86; y = 650 + r * 44
        d.rectangle([x, y, x + 74, y + 34], fill=SIG if i < 81 * k else None, outline=INK if i >= 81 * k else SIG, width=2)
    fig(d, "height, weight or age")

def sc_how(img, d, t):
    t0, tm = S("how"), cue("how", "men tended") - .2
    silhouette(img, lambda m: body(m, 280, 1120, 560, 255), (80, 500, 480, 1130), INK, cell=10)
    box_label(d, 280, 470, "− POUNDS", 40, WHITE, INK, font=BLK, anchor="ma")
    if t >= tm:
        k = ease((t - tm) / .5)
        silhouette(img, lambda m: body(m, 680, 1120, 600, 255), (480, 450, 900, 1130), SIG, cell=10)
        top = 1120 - 600; ghost = top - 60 * k
        d.line([600, ghost, 760, ghost], fill=SIG, width=4); dim_v(d, 800, ghost, top, 1, SIG, None)
        box_label(d, 680, 470, "+ INCHES", 40, WHITE, SIG, font=BLK, anchor="ma")
    d.text((X0, 310), "WOMEN · MEN", font=F(BLK, 100), fill=INK)
    fig(d, "typical direction of the fib")

def sc_small(img, d, t):
    t0 = S("small")
    d.text((X0, 320), "BUT SMALL.", font=F(BLK, 160), fill=SIG)
    items = [("≈ 5 LB", "weight", "five pounds"), ("1/3 IN", "height", "third of an inch"), ("MONTHS", "age", "few months")]
    for i, (big, lab, w) in enumerate(items):
        tk = cue("small", w) - .3; k = ease((t - tk) / .3)
        if k <= 0: continue
        y = 540 + i * 190
        d.text((X0 + (1 - k) * 40, y), big, font=F(BLK, 120), fill=INK); d.text((X1, y + 50), lab, font=F(MONO, 28), fill=MID, anchor="ra")
        d.line([X0, y + 160, X1, y + 160], fill=RULE, width=2)
    fig(d, "average size of the lie")

def sc_point(img, d, t):
    t0, td = S("point"), cue("point", "be honest") - .2
    if t < td:
        words_in(d, t, [("SMALL ENOUGH", t0, 320, 120, INK), ("TO GET AWAY.", t0 + .3, 450, 120, INK), ("BIG ENOUGH", cue("point", "big enough") - .2, 600, 120, SIG), ("TO FEEL BETTER.", cue("point", "big enough"), 730, 110, SIG)])
    else:
        words_in(d, t, [("DID", td, 320, 230, INK), ("YOU?", td + .2, 540, 230, SIG)])
        profile_card(img, d, 480, 640, t, marks=(1,))
    fig(d, "fig. 2 — be honest")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "how": sc_how, "small": sc_small, "point": sc_point}
FX = [(0.0, thud(.5), 0), (cue("hook", "eighty-one") - .2, thud(.5), 0), *[(cue("hook", "eighty-one") - .2 + i * .1, pop(.1), (i - 1) / 2) for i in range(3)], *EP.cut_fx(),
      (S("study") + .2, pop(.15), 0), (S("result") + .05, thud(.55), 0), *[(S("result") + .2 + i * .1, tick(.035), (i % 5 - 2) / 3) for i in range(14)],
      (cue("how", "men tended") - .2, pop(.15), .3), *[(cue("small", w) - .3, pop(.15), (i - 1) / 2) for i, w in enumerate(("five pounds", "third of an inch", "few months"))],
      (cue("point", "big enough") - .2, pop(.15), 0), (cue("point", "be honest") - .2, thud(.5), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
