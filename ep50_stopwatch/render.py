"""NOT JUST YOU · AFTER DARK – No. 50: the stopwatch study (Waldinger et al. 2005; Corty & Guardiani 2008)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .8, "result": .5, "range": .5, "experts": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "range", "experts", "point", "end"]
EP = Episode(TL, 50, "THE STOPWATCH", order=ORDER, dark=True, series="NOT JUST YOU · AFTER DARK",
             chapters={"hook": "HOW LONG?", "study": "THE EXPERIMENT", "result": "THE MEDIAN", "range": "THE SPREAD", "experts": "THE EXPERTS", "point": "NOT THE POINT"},
             sources=("Waldinger et al. (2005), J Sex Med 2(4);", "Corty & Guardiani (2008), J Sex Med 5(5)"),
             music=dict(bpm=120, root=2, prog="tense", kick="four", gaps=[(E("study") + .05, S("result") + .05)]),
             cover=dict(words=["HOW", "LONG?"], kicker="Scientists used a stopwatch."))

def stopwatch(d, cx, cy, r, minutes, col=SIG, scale=10.0, ink=INK):
    """analog stopwatch; one full turn = `scale` minutes"""
    d.rectangle([cx - 22, cy - r - 46, cx + 22, cy - r - 10], fill=ink); d.rectangle([cx - 50, cy - r - 64, cx + 50, cy - r - 40], fill=ink)
    d.line([cx + r * .72, cy - r * .72, cx + r * .9, cy - r * .9], fill=ink, width=14)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=ink, width=12)
    f = (minutes / scale) % 1
    if minutes > 0: d.pieslice([cx - r + 22, cy - r + 22, cx + r - 22, cy + r - 22], -90, -90 + 360 * f if minutes < scale else 270, fill=mix(BG, col, .35))
    for i in range(60):
        a = math.radians(i * 6 - 90); L = 26 if i % 5 == 0 else 12
        d.line([cx + math.cos(a) * (r - 18), cy + math.sin(a) * (r - 18), cx + math.cos(a) * (r - 18 - L), cy + math.sin(a) * (r - 18 - L)], fill=ink, width=4 if i % 5 == 0 else 2)
    a = math.radians(-90 + 360 * f); d.line([cx, cy, cx + math.cos(a) * (r - 40), cy + math.sin(a) * (r - 40)], fill=col, width=8)
    d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=col)

def readout(m): mm = int(m); ss = int(round((m - mm) * 60)) % 60; return f"{mm}:{ss:02d}"

def sc_hook(img, d, t):
    d.text((X0 - 6, 300), "HOW", font=F(BLK, 220), fill=INK); d.text((X0 - 6, 500), "LONG?", font=F(BLK, 220), fill=SIG)
    stopwatch(d, 660, 960, 165, t * 2.4)
    if t >= cue("hook", "stopwatch"): box_label(d, X0, 960, "FOR SCIENCE", 40, WHITE, INK)
    fig(d, "fig. 1 — the least romantic lab tool")

def sc_study(img, d, t):
    t0 = S("study")
    counter(d, X0, 300, t, t0 + .1, .9, 500, "{:.0f} couples", 140, SIG)
    for i, c in enumerate(("NL", "ES", "TR", "UK", "US")):
        k = ease((t - cue("study", "five countries") - i * .1) / .3)
        if k > 0: box_label(d, X0 + i * 170, 520 + (1 - k) * 20, c, 50, WHITE, INK if i % 2 else SIG, font=BLK)
    tk = cue("study", "four weeks") - .2
    for i in range(28):
        r, c = divmod(i, 7); x = X0 + 10 + c * 120; y = 690 + r * 100; on = t >= tk + i * .04
        d.rectangle([x, y, x + 100, y + 80], outline=INK, width=3, fill=SIG if on and i % 3 == 0 else None)
        if on: d.line([x + 50, y + 40, x + 50, y + 18], fill=INK, width=4); d.line([x + 50, y + 40, x + 70, y + 40], fill=INK, width=4)
    fig(d, "4 weeks, timed at home · Waldinger et al., 2005")

def sc_result(img, d, t):
    t0 = S("result"); tf = cue("result", "five point"); m = 5.4 * ease((t - t0 - .1) / (tf - t0 + .3))
    d.text((X0, 300), readout(m), font=F(BLK, 230), fill=SIG)
    d.text((X0 + 6, 540), "median · minutes:seconds", font=F(COND, 34), fill=INK)
    stopwatch(d, 480, 880, 200, m)
    if t >= tf + .3: box_label(d, X1, 640, "≈ 5.4 MIN", 40, WHITE, INK, anchor="ra")
    fig(d, "from start of intercourse to finish")

def sc_range(img, d, t):
    t0 = S("range")
    d.text((X0, 300), "THE SPREAD", font=F(BLK, 130), fill=INK)
    ax0, ax1, ay = X0 + 20, X1 - 20, 900
    def xm(m): return ax0 + (ax1 - ax0) * m / 15
    d.line([ax0, ay, ax1, ay], fill=INK, width=4)
    for m in (0, 5, 10, 15):
        d.line([xm(m), ay, xm(m), ay + 14], fill=INK, width=3); d.text((xm(m), ay + 22), f"{m} min", font=F(MONO, 20), fill=MID, anchor="ma")
    k = clamp((t - t0 - .1) / 1.4)
    import random; rnd = random.Random(7)
    for i in range(int(120 * k)):
        m = min(14.6, max(.4, rnd.lognormvariate(math.log(5.4), .65))); y = ay - 30 - rnd.random() * 220
        d.ellipse([xm(m) - 7, y - 7, xm(m) + 7, y + 7], fill=SIG if m < 3.33 or m > 10 else MID)
    if t >= cue("range", "three and a half"): box_label(d, X0, 560, "14 % < 3:20", 34, WHITE, SIG)
    if t >= cue("range", "over ten"): box_label(d, X1, 560, "26 % > 10:00", 34, WHITE, SIG, anchor="ra")
    d.line([xm(5.4), ay - 270, xm(5.4), ay], fill=INK, width=3); d.text((xm(5.4) + 8, ay - 270), "median", font=F(MONO, 20), fill=INK)
    d.text((X1, 1146), "schematic", font=F(MED, 22), fill=MID, anchor="ra")

def sc_experts(img, d, t):
    t0 = S("experts"); ta = cue("experts", "three to seven")
    d.text((X0, 300), "THERAPISTS", font=F(BLK, 130), fill=INK)
    zones = [(1, 2, "too short", MID), (3, 7, "adequate", SIG), (7, 13, "desirable", INK), (13, 30, "too long", MID)]
    ay, bw = 620, (X1 - X0) / 4
    for i, (a, b, lab, col) in enumerate(zones):
        k = ease((t - t0 - .2 - i * .2) / .4)
        if k <= 0: continue
        on = i == 1 and t >= ta; x = X0 + i * bw
        d.rectangle([x, ay + (0 if on else 40), x + (bw - 8) * k, ay + 260], fill=col if (on or i != 1) else mix(BG, SIG, .4))
        if k > .9:
            d.text((x + 12, ay + 210 - (0 if on else 0)), f"{a}–{b}", font=F(BLK, 36), fill=WHITE if col != MID else INK, anchor="ls")
            d.text((x, ay + 290), lab, font=F(COND, 30), fill=SIG if i == 1 else INK)
    if t >= ta: box_label(d, X0 + bw, 1000, "ADEQUATE: 3–7 MIN", 44, WHITE, SIG)
    fig(d, "survey of sex therapists (minutes) · Corty & Guardiani, 2008")

def sc_point(img, d, t):
    t0 = S("point"); tn = cue("point", "totally normal"); tc = cue("point", "the clock")
    if t < tc - .2:
        words_in(d, t, [("SHORTER", t0, 300, 170, INK), ("THAN THE MOVIES.", t0 + .3, 470, 96, SIG)])
        x0, y0 = X0 + 120, 700
        d.rectangle([x0, y0, x0 + 600, y0 + 300], fill=INK)
        for i in range(8):
            d.rectangle([x0 + 20 + i * 74, y0 + 14, x0 + 56 + i * 74, y0 + 40], fill=BG); d.rectangle([x0 + 20 + i * 74, y0 + 260, x0 + 56 + i * 74, y0 + 286], fill=BG)
        d.text((x0 + 300, y0 + 150), "THE END?", font=F(BLK, 70), fill=SIG, anchor="mm")
        if t >= tn: box_label(d, X1, 1040, "TOTALLY NORMAL", 36, WHITE, SIG, anchor="ra")
    else:
        words_in(d, t, [("THE CLOCK", tc - .2, 300, 150, INK), ("WAS NEVER", tc + .1, 450, 150, INK), ("THE POINT.", tc + .4, 600, 150, SIG)])
        stopwatch(d, 480, 960, 130, 5.4, MID, ink=MID)
        k = ease((t - tc - .6) / .3); d.line([480 - 170 * k, 960 - 170 * k, 480 + 170 * k, 960 + 170 * k], fill=SIG, width=16)
    fig(d, "fig. 2 — connection over duration")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "range": sc_range, "experts": sc_experts, "point": sc_point}
def clk(amp=.05):
    t = tt_(.05); return amp * np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 120)
FX = [(0.0, thud(.5), 0), *[(.15 + i * .5, clk(.05), .3) for i in range(5)], (cue("hook", "stopwatch"), pop(.18), 0), *EP.cut_fx(),
      *[(cue("study", "five countries") + i * .1, pop(.1), (i - 2) / 3) for i in range(5)], *[(cue("study", "four weeks") - .2 + i * .04, tick(.03), (i % 5 - 2) / 3) for i in range(0, 28, 2)],
      (S("result") + .05, thud(.55), 0), *[(S("result") + .1 + i * .25, clk(.05), 0) for i in range(8)], (cue("result", "five point") + .3, thud(.4), 0),
      (cue("range", "three and a half"), pop(.15), -.3), (cue("range", "over ten"), pop(.15), .3), (cue("experts", "three to seven"), thud(.4), 0),
      (cue("point", "the clock") + .6, rewind_sfx(.1, .3), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
