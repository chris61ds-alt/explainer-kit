"""NOT JUST YOU – No. 31: why sad music feels good (Taruffi & Koelsch 2014). Area: music."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .8, "result": .6, "when": .6, "point": .8, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "when", "point", "end"]
EP = Episode(TL, 31, "SAD SONGS", order=ORDER,
             chapters={"hook": "THE PARADOX", "study": "THE SURVEY", "result": "THE FEELINGS", "when": "WHEN", "point": "COMPANY"},
             sources=("Taruffi & Koelsch (2014), PLOS ONE 9(10)", "via Pacific Standard"),
             music=dict(bpm=72, root=-5, prog="minor", kick="half", gaps=[(E("study") + .05, S("result") + .05)]),
             cover=dict(words=["SAD", "SONGS."], kicker="Why they feel so good."))

SIT = {"arms": ((40, 60), (-20, 40)), "legs": ((90, 0), (86, 0))}
def seated(d, x, y, s, col, t, head_dy=0):
    d.line([x - 80 * s, y - 130 * s, x + 90 * s, y - 130 * s], fill=INK, width=int(10 * s))           # bench
    d.line([x - 70 * s, y - 130 * s, x - 70 * s, y], fill=INK, width=int(8 * s)); d.line([x + 80 * s, y - 130 * s, x + 80 * s, y], fill=INK, width=int(8 * s))
    return picto(d, x - 20 * s, y - 130 * s + 140 * s, s, col, f=1, pose=SIT, head_dy=head_dy)

def rain(d, t, x0=X0, x1=X1, y0=520, y1=1100, n=22, col=RULE):
    for i in range(n):
        x = x0 + (i * 97) % (x1 - x0); y = y0 + ((t * 300 + i * 131) % (y1 - y0))
        d.line([x, y, x - 6, y + 26], fill=col, width=4)

def sc_hook(img, d, t):
    d.text((X0 - 6, 300), "SAD SONG?", font=F(BLK, 180), fill=INK)
    rain(d, t)
    h = seated(d, 420, FLOOR, 1.0, INK, t, head_dy=6)
    headphones(d, h, 1.0)
    if t >= cue("hook", "good"):
        k = ease((t - cue("hook", "good")) / .4)
        box_label(d, 720, 640, "FEELS GOOD", 34, WHITE, SIG, anchor="ma")
    fig(d, "fig. 1 — a rainy evening playlist")

def sc_study(img, d, t):
    t0 = S("study")
    counter(d, X0, 300, t, t0 + .1, 1.0, 772, "{:,.0f}", 200, SIG); d.text((X0 + 6, 530), "people surveyed online", font=F(COND, 36), fill=INK)
    d.rectangle([X0 + 120, 620, X1 - 120, 1080], fill=WHITE, outline=INK, width=4)
    d.text((X0 + 150, 650), "How does sad music make you feel?", font=F(COND, 28), fill=INK)
    for i in range(5):
        y = 720 + i * 70; d.rectangle([X0 + 150, y, X0 + 186, y + 36], outline=INK, width=3)
        d.line([X0 + 210, y + 18, X1 - 160 - (i % 3) * 60, y + 18], fill=RULE, width=6)
        if t > t0 + .8 + i * .3 and i in (0, 1, 2): d.line([X0 + 154, y + 18, X0 + 168, y + 32, X0 + 190, y - 4], fill=SIG, width=5)
    fig(d, "Taruffi & Koelsch — PLOS ONE, 2014")

def sc_result(img, d, t):
    t0 = S("result"); ns = cue("result", "nostalgia")
    d.text((X0, 320), "NOT SADNESS.", font=F(BLK, 120), fill=INK)
    rows = [("nostalgia", .9, SIG, ns), ("peacefulness", .7, INK, cue("result", "peacefulness")), ("tenderness", .66, INK, cue("result", "tenderness")), ("sadness", .5, MID, ns + 1.2)]
    for i, (lab, v, col, tk) in enumerate(rows):
        y = 500 + i * 150; k = ease((t - tk + .1) / .5)
        d.text((X0, y), lab, font=F(COND, 32), fill=col if col != MID else MID)
        d.rectangle([X0, y + 46, X0 + (X1 - X0) * v * k, y + 116], fill=col)
    d.text((X1, 1146), "schematic ranking", font=F(MED, 22), fill=MID, anchor="ra")

def sc_when(img, d, t):
    t0 = S("when")
    d.text((X0, 320), "WHEN?", font=F(BLK, 130), fill=INK)
    rain(d, t, y0=480, n=14)
    h = seated(d, 360, FLOOR, 1.0, INK, t, head_dy=8); headphones(d, h, 1.0)
    for i, (lab, tk) in enumerate((("lonely", cue("when", "lonely")), ("down", cue("when", "down")))):
        k = ease((t - tk + .1) / .3)
        if k > 0: box_label(d, 700, 560 + i * 90, lab, 40, WHITE, SIG if i == 0 else INK, anchor="ma")
    fig(d, "listeners reach for it to feel consoled")

def sc_point(img, d, t):
    t0 = S("point"); kc = cue("point", "company")
    words_in(d, t, [("NOT WORSE.", t0, 300, 150, INK)] if t < kc - .3 else [("COMPANY.", kc - .3, 300, 180, SIG)])
    h = seated(d, 330, FLOOR, 1.0, INK, t); headphones(d, h, 1.0)
    # the song, sitting next to you
    k = ease((t - t0 - .5) / .6)
    if k > 0: note_icon(d, 600, 970 - 10 * math.sin(t * 3), 2.2 * k, SIG)
    if t >= kc: note(d, 640, 900, 860, 640, "the song", (t - kc) / .35, SIG, anchor="ra", size=30)
    fig(d, "fig. 2 — sitting with it, not stuck in it")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "when": sc_when, "point": sc_point}
def bell(f, amp=.05, dur=1.2):
    t = tt_(dur); return amp * (np.sin(2 * np.pi * f * t) + .3 * np.sin(4 * np.pi * f * t)) * np.exp(-t * 3)
FX = [(0.0, thud(.4), 0), (.2, bell(440), -.2), (.6, bell(523.3), .2), (cue("hook", "good"), bell(659.3, .06), 0), *EP.cut_fx(),
      *[(S("study") + .8 + i * .3, pop(.1), 0) for i in range(3)], (S("result") + .05, thud(.45), 0), (cue("result", "nostalgia"), bell(587.3, .07), 0),
      (cue("when", "lonely"), pop(.15), .2), (cue("when", "down"), pop(.15), .3), (cue("point", "company"), bell(784, .07, 1.6), 0), (S("end"), thud(.45), 0)]
if __name__ == "__main__": EP.run(FX)
