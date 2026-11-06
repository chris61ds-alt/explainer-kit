"""NOT JUST YOU – No. 120: everyone has more sex than you? – people guessed young adults have sex ~20× a month, self-reports say
5–6 (Ipsos Perils of Perception 2018, 19 countries); in couples, well-being rose with sex only up to ~once a week (Muise et al. 2016).
Look C+D · statement opener with "you" · isometric month calendar (guess vs. real) · orange reveal: 5–6 times."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"guess": .5, "real": .6, "week": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["guess", "real", "week", "point", "end"]
EP = ThreadEpisode(TL, 120, "MORE SEX", order=ORDER, dark=True, label="SURVEYS · 19 COUNTRIES",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Ipsos (2018), Perils of Perception ·", "Muise, Schimmack & Impett (2016), SPPS 7(4)"),
                   music=dict(bpm=100, root=0, prog="major", kick="four", audio="v5", gaps=[(E("guess") + .05, S("real") + .05)]),
                   cover=dict(words=["YOU THINK", "EVERYONE HAS", "MORE SEX."], kicker="They don't. Here's the real number."))

I = Iso(500, 990, .62)
def calendar(img, d, t, t0, marked, col, grid=True):
    """4 weeks × 7 days of isometric tiles; the first `marked` days pop up as small blocks"""
    if grid: I.grid(img)
    days = [(r, c) for r in range(4) for c in range(7)]
    order = list(range(28)); import random; random.Random(7).shuffle(order); hit = set(order[:marked])
    for i, (r, c) in enumerate(days):
        x, y = -350 + c * 100, -200 + r * 100
        up = i in hit; k = clamp((t - t0 - (sorted(hit).index(i) if up else 0) * .05) / .2) if up else 0
        I.box(d, x, y, 0, 86, 86, 6 + (34 * ease(k) if up else 0), top=(col if up and k > .5 else TOP))

def sc_guess(img, d, t):
    t0, tg = S("guess"), cue("guess", "About twenty") - .1
    d.text((X0, 320), "THE GUESS:", font=F(BLK, 120), fill=INK); d.text((X0 + 4, 450), "sex per month, adults 18–29", font=F(COND, 48), fill=MID)
    calendar(img, d, t, tg, 20 if t >= tg else 0, INK)
    if t >= tg: counter(d, X0, 520, t, tg, .8, 20, "~{:.0f}×", 110, INK)
    fig(d, "19 countries · schematic")

def sc_real(img, d, t):
    t0 = S("real")
    d.text((X0, 320), "THE REAL", font=F(BLK, 120), fill=INK); d.text((X0, 440), "NUMBER:", font=F(BLK, 120), fill=INK)
    counter(d, X0, 600, t, t0 + .1, .5, 5, "{:.0f}–6×", 230, SIG)
    d.text((X0 + 6, 850), "a month · self-reported", font=F(COND, 50), fill=INK)
    fig(d, "national surveys")

def sc_week(img, d, t):
    t0, tm = S("week"), cue("week", "More didn't") - .1
    d.text((X0, 320), "HAPPINESS", font=F(BLK, 120), fill=INK); d.text((X0 + 4, 450), "in couples, by how often", font=F(COND, 48), fill=MID)
    xs = [X0 + 40 + i * 190 for i in range(5)]; ys = [0.15, 0.45, 0.75, 0.78, 0.77]; labs = ["< MONTHLY", "MONTHLY", "WEEKLY", "2–3× WK", "4+× WK"]
    base, h = 1000, 380; n = clamp((t - t0 - .2) / 1.2) * 4
    pts = [(xs[i], base - ys[i] * h) for i in range(5)]
    for i in range(4):
        if n <= i: break
        f = min(1, n - i); a, b = pts[i], pts[i + 1]; d.line([a, (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)], fill=INK, width=10)
    for i in range(5):
        if n >= i: d.ellipse([pts[i][0] - 16, pts[i][1] - 16, pts[i][0] + 16, pts[i][1] + 16], fill=INK if i != 2 else SIG)
        d.text((xs[i], base + 30), labs[i], font=F(MONO, 22), fill=MID, anchor="ma")
    if t >= tm: box_label(d, X1, 560, "MORE: NO EXTRA GAIN", 44, WHITE, INK, font=BLK, anchor="ra")
    fig(d, "a link, not proof · schematic shape")

def sc_point(img, d, t):
    t0, tc = S("point"), cue("point", "closer to normal") - .2
    words_in(d, t, [("STOP", t0 + .05, 320, 170, MID), ("COMPARING.", t0 + .2, 500, 150, MID)] + ([("YOU'RE PROBABLY", tc, 680, 100, SIG), ("PRETTY NORMAL.", tc + .15, 790, 100, SIG)] if t >= tc else []))
    fig(d, "fig. 2 — not a contest")

EP.cuts = {}
EP.bg = {"guess": "light"}
EP.scenes = {"guess": sc_guess, "real": sc_real, "week": sc_week, "point": sc_point}
FX = [*EP.cut_fx(), *[(cue("guess", "About twenty") - .1 + i * .05, tick(.03), (i % 7 - 3) / 4) for i in range(20)],
      (S("real") + .05, thud(.55), 0), (S("real") + .6, pop(.15), .3),
      (S("week") + .2, riser(1.2, .03), 0), (cue("week", "More didn't") - .1, pop(.14), .3),
      (S("point") + .1, pop(.12), 0), (cue("point", "closer to normal") - .2, thud(.5), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
