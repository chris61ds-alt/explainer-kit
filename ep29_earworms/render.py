"""NOT JUST YOU – No. 29: earworms (Jakubowski et al. 2017; Beaman et al. 2015). Area: music."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .5, "traits": .8, "top": .6, "tip": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "traits", "top", "tip", "end"]
EP = Episode(TL, 29, "EARWORMS", order=ORDER,
             chapters={"hook": "STUCK", "study": "THE STUDY", "traits": "THE RECIPE", "top": "THE TOP 3", "tip": "THE FIX"},
             sources=("Jakubowski et al. (2017), Psych. of Aesthetics,", "Creativity & the Arts 11(2) · Beaman et al. (2015)"),
             music=dict(bpm=116, root=0, prog="major", kick="four", gaps=[(E("traits") + .05, S("top") + .05)]),
             cover=dict(words=["STUCK IN", "YOUR HEAD?"], kicker="Why some songs never leave."))

def orbit_notes(d, h, t, n=4, r=120):
    for i in range(n):
        a = t * 2 + i * 2 * math.pi / n; x = h[0] + math.cos(a) * r; y = h[1] - 20 + math.sin(a) * r * .45
        note_icon(d, x, y, .6, SIG if i % 2 else INK)

def contour(d, x0, y0, w, h, pts, col=INK, k=1.0):
    P = [(x0 + w * u, y0 + h * (1 - v)) for u, v in pts]
    n = max(2, int(len(P) * k)); d.line(P[:n], fill=col, width=5)
    for x, y in P[:n]: d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=col)

def sc_hook(img, d, t):
    d.text((X0 - 6, 300), "STUCK.", font=F(BLK, 220), fill=INK)
    h = picto(d, 420, FLOOR, 1.05, INK, pose=WORRY)
    orbit_notes(d, h, t)
    if t >= cue("hook", "not random"): box_label(d, 760, 640, "NOT RANDOM", 34, WHITE, SIG, anchor="ra")
    fig(d, "fig. 1 — on repeat, in your head")

def sc_study(img, d, t):
    t0 = S("study"); cp = cue("study", "compared")
    counter(d, X0, 300, t, t0 + .1, 1.0, 3000, "{:,.0f}", 170, SIG); d.text((X0 + 6, 500), "people named their earworms", font=F(COND, 34), fill=INK)
    d.text((X0, 600), "EARWORM", font=F(COND, 30), fill=SIG); waveform(d, X0 + 200, X1, 620, t, 40, SIG, clamp((t - t0) / 2), seed=2)
    if t >= cp - .2:
        d.text((X0, 760), "EQUALLY POPULAR SONG", font=F(COND, 30), fill=INK)
        waveform(d, X0 + 40, X1, 840, t, 40, INK, clamp((t - cp + .2) / 1.5), seed=7)
        note(d, 480, 700, 700, 980, "what's different?", (t - cp - .3) / .4, SIG, size=28)
    fig(d, "Jakubowski, Finkel, Stewart & Müllensiefen, 2017")

def sc_traits(img, d, t):
    t0 = S("traits")
    d.text((X0, 320), "THE RECIPE", font=F(BLK, 130), fill=INK)
    cards = [("01", "FASTER", cue("traits", "faster")), ("02", "FAMILIAR SHAPE", cue("traits", "familiar")), ("03", "ONE SURPRISE", cue("traits", "surprising"))]
    for i, (no, lab, tk) in enumerate(cards):
        k = ease((t - tk + .1) / .35)
        if k <= 0: continue
        y = 480 + i * 210; d.rectangle([X0, y, X1, y + 180], outline=INK, width=4)
        d.text((X0 + 20, y + 14), no, font=F(COND, 26), fill=SIG); d.text((X0 + 20, y + 120), lab, font=F(BLK, 44), fill=INK, anchor="lm")
        if i == 0:
            a = math.sin(t * 9) * .5; d.polygon([(X1 - 140, y + 160), (X1 - 60, y + 160), (X1 - 100, y + 30)], outline=INK, width=4)
            d.line([X1 - 100, y + 150, X1 - 100 + math.sin(a) * 90, y + 150 - math.cos(a) * 110], fill=SIG, width=5)
        if i == 1: contour(d, X1 - 340, y + 30, 300, 120, [(0, .2), (.2, .5), (.4, .8), (.6, .9), (.8, .5), (1, .2)], INK, k)
        if i == 2: contour(d, X1 - 340, y + 30, 300, 120, [(0, .4), (.2, .4), (.4, .45), (.55, .95), (.7, .4), (1, .4)], SIG, k)
    fig(d, "faster tempo · common melodic contour · unusual intervals or repeats")

def sc_top(img, d, t):
    t0 = S("top")
    d.text((X0, 320), "MOST NAMED", font=F(BLK, 120), fill=INK)
    rows = [("1", "Bad Romance", "Lady Gaga"), ("2", "Can't Get You Out of My Head", "Kylie Minogue"), ("3", "Don't Stop Believin'", "Journey")]
    for i, (n, song, art) in enumerate(rows):
        k = ease((t - t0 - (0 if i == 0 else .9 + i * .3)) / .35)
        if k <= 0: continue
        y = 500 + i * 170; first = i == 0
        d.rectangle([X0, y, X1, y + 140], fill=SIG if first else None, outline=INK, width=4)
        d.text((X0 + 30, y + 70), n, font=F(BLK, 90), fill=WHITE if first else INK, anchor="lm")
        d.text((X0 + 140, y + 46), song, font=F(BLK, 40 if len(song) < 22 else 32), fill=WHITE if first else INK, anchor="lm")
        d.text((X0 + 140, y + 100), art, font=F(COND, 28), fill=WHITE if first else MID, anchor="lm")
    fig(d, "Jakubowski et al., 2017 · song titles only")

def gum(d, x, y, s=1.0):
    d.rounded_rectangle([x - 90 * s, y - 40 * s, x + 90 * s, y + 40 * s], radius=14 * s, fill=SIG); d.rectangle([x - 90 * s, y - 8 * s, x + 90 * s, y + 8 * s], fill=WHITE)

def sc_tip(img, d, t):
    t0 = S("tip"); cg = cue("tip", "chew gum")
    d.text((X0, 320), "THE FIX", font=F(BLK, 130), fill=INK)
    k1 = ease((t - cue("tip", "all the way") + .2) / .4)
    if k1 > 0:
        d.text((X0, 500), "01  play it to the end", font=F(BLK, 44), fill=INK)
        d.rectangle([X0, 580, X1, 610], outline=INK, width=3); d.rectangle([X0 + 4, 584, X0 + 4 + (X1 - X0 - 8) * clamp((t - cue("tip", "all the way")) / 1.2), 606], fill=INK)
    if t >= cg - .2:
        d.text((X0, 700), "02  chew gum", font=F(BLK, 44), fill=SIG)
        gum(d, 480, 860, 1.2 * ease((t - cg + .2) / .3))
        if t >= cue("tip", "helped"): note(d, 560, 830, 860, 1000, "it helped in one study", (t - cue("tip", "helped")) / .35, INK, anchor="ra", size=28)
    fig(d, "Beaman et al. — Quarterly Journal of Experimental Psychology, 2015")

EP.scenes = {"hook": sc_hook, "study": sc_study, "traits": sc_traits, "top": sc_top, "tip": sc_tip}
def blip(f=880, amp=.06, dur=.18):
    t = tt_(dur); return amp * np.sin(2 * np.pi * f * t) * np.exp(-t * 14)
LOOP = [(i * .25, blip([659, 784, 880, 784][i % 4]), (i % 2 - .5)) for i in range(8)]
FX = [(0.0, thud(.5), 0), *LOOP, (cue("hook", "not random"), pop(.2), .3), *EP.cut_fx(),
      *[(S("study") + .1 + i * .1, tick(.05), (i % 5 - 2) / 3) for i in range(10)], (cue("study", "compared"), pop(.15), 0),
      (cue("traits", "faster"), pop(.18), -.3), (cue("traits", "familiar"), pop(.18), 0), (cue("traits", "surprising"), blip(1320, .08, .3), .3),
      (S("top") + .05, thud(.55), 0), (cue("tip", "chew gum"), pop(.2), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
