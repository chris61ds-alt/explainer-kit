"""NOT JUST YOU – No. 116: the friendship paradox – popular people show up in many friend lists, so most people's friends have
more friends than they do (Feld 1991; 55 % of girls in a high-school network). Look C+D · statement opener with "you" ·
isometric friend network with one hub · orange reveal: most had fewer friends than their friends."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hub": .5, "why": .6, "school": .5, "result": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hub", "why", "school", "result", "point", "end"]
EP = ThreadEpisode(TL, 116, "FRIEND PARADOX", order=ORDER, dark=True, label="MATH · NETWORK DATA",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Feld (1991), Why your friends have more friends than", "you do, American Journal of Sociology 96(6)"),
                   music=dict(bpm=104, root=1, prog="major", kick="four", audio="v5", gaps=[(E("hub") + .05, S("why") + .05)]),
                   cover=dict(words=["YOUR FRIENDS", "HAVE MORE", "FRIENDS THAN YOU."], kicker="It's math, not you."))

I = Iso(500, 960, .8)
HUB = (0, 0)
RING = [(260 * math.cos(a), 260 * math.sin(a)) for a in [i * 2 * math.pi / 7 + .3 for i in range(7)]]
PAIRS = [(0, 1), (3, 4)]                                     # a few friendships among the others
def person(I, d, x, y, h, top, k=1.0):
    if k <= 0: return
    I.cyl(d, x, y, 0, 34, h * ease(clamp(k)), top=top)

def network(img, d, t, t0, hl=-1, pulse=False):
    I.grid(img)
    for i, (x, y) in enumerate(RING):                        # links to the hub
        k = clamp((t - t0 - .3 - i * .06) / .25)
        if k > 0:
            a, b = I.P(HUB[0], HUB[1], 0), I.P(x, y, 0); e = (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k)
            d.line([a, e], fill=SIG if (pulse and i == hl) else MID, width=6)
    for i, j in PAIRS:
        if t >= t0 + .9: d.line([I.P(*RING[i], 0), I.P(*RING[j], 0)], fill=MID, width=6)
    order = sorted(range(7), key=lambda i: RING[i][0] + RING[i][1])
    for i in order:
        if RING[i][0] + RING[i][1] < 0: person(I, d, *RING[i], 70, TOP, (t - t0 - i * .05) / .25)
    person(I, d, *HUB, 170, TOP, (t - t0) / .3)
    for i in order:
        if RING[i][0] + RING[i][1] >= 0: person(I, d, *RING[i], 70, TOP, (t - t0 - i * .05) / .25)
    px, py = I.P(*HUB, 170); d.text((px, py - 50), "7 FRIENDS", font=F(BLK, 40), fill=INK, anchor="mm")

def sc_hub(img, d, t):
    t0 = S("hub")
    d.text((X0, 320), "ONE POPULAR", font=F(BLK, 120), fill=INK); d.text((X0, 440), "PERSON", font=F(BLK, 120), fill=INK)
    network(img, d, t, t0 + .1)
    fig(d, "fig. 1 — schematic")

def sc_why(img, d, t):
    t0, ta = S("why"), cue("why", "the average goes up") - .15
    d.text((X0, 320), "SHOWS UP", font=F(BLK, 120), fill=INK); d.text((X0, 440), "AGAIN & AGAIN", font=F(BLK, 110), fill=INK)
    hl = int((t - t0) * 4) % 7
    network(img, d, t, t0 - 2, hl=hl, pulse=True)
    if t >= ta: box_label(d, X1, 600, "AVERAGE: UP", 48, WHITE, INK, font=BLK, anchor="ra")
    fig(d, "friends of friends · schematic")

def sc_school(img, d, t):
    t0 = S("school")
    words_in(d, t, [("ONE HIGH", t0 + .05, 320, 170, INK), ("SCHOOL.", t0 + .2, 500, 170, INK)])
    dot_field(d, (X0 + 14, 720, X1, 1100), t, cell=34, col=MID, hit=set(), hitcol=INK)
    fig(d, "Coleman's school network data")

def sc_result(img, d, t):
    t0, tn = S("result"), cue("result", "Fifty-five") - .1
    words_in(d, t, [("MOST HAD FEWER", t0 + .05, 320, 100, SIG), ("FRIENDS THAN", t0 + .15, 420, 100, INK), ("THEIR FRIENDS.", t0 + .25, 520, 100, INK)])
    if t >= tn:
        counter(d, X0, 680, t, tn, .5, 55, "{:.0f} %", 200, SIG)
        d.text((X0 + 6, 900), "of the girls · 80 of 146", font=F(COND, 50), fill=INK)
    fig(d, "1991 · one school")

def sc_point(img, d, t):
    t0, ti = S("point"), cue("point", "that's an illusion") - .15
    words_in(d, t, [("EVERYONE", t0 + .05, 320, 140, MID), ("MORE SOCIAL?", t0 + .2, 470, 130, MID)] + ([("AN ILLUSION.", ti, 640, 140, SIG), ("NOT YOU.", ti + .5, 790, 140, SIG)] if t >= ti else []))
    fig(d, "fig. 2 — the friendship paradox")

EP.cuts = {"why": "stay", "result": "stay"}
EP.bg = {"hub": "light", "why": "light"}
EP.scenes = {"hub": sc_hub, "why": sc_why, "school": sc_school, "result": sc_result, "point": sc_point}
FX = [*EP.cut_fx(), (S("hub") + .1, thud(.45), 0), *[(S("hub") + .4 + i * .06, tick(.035), (i - 3) / 4) for i in range(7)],
      *[(S("why") + i * .25, tick(.03), ((i % 7) - 3) / 4) for i in range(12)], (cue("why", "the average goes up") - .15, pop(.14), .3),
      (S("school") + .1, riser(.8, .04), 0), (S("result") + .05, thud(.55), 0), (cue("result", "Fifty-five") - .1, pop(.15), 0),
      (S("point") + .1, pop(.12), 0), (cue("point", "that's an illusion") - .15, thud(.5), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
