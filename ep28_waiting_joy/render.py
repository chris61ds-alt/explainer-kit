"""NOT JUST YOU – No. 28: waiting for experiences vs things (Kumar, Killingsworth & Gilovich 2014). Area: money."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .8, "result": .5, "queue": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "queue", "point", "end"]
EP = Episode(TL, 28, "THE WAITING", order=ORDER,
             chapters={"hook": "THE WAIT", "study": "THE PINGS", "result": "THE RESULT", "queue": "THE LINES", "point": "BOOK EARLY"},
             sources=("Kumar, Killingsworth & Gilovich (2014),", "Psychological Science 25(10) · via APS"),
             music=dict(bpm=104, root=2, prog="dream", kick="four", gaps=[(E("study") + .05, S("result") + .05)]),
             cover=dict(words=["BOOK", "IT EARLY."], kicker="The waiting is part of the gift."))

def ticket(d, x, y, s=1.0, col=SIG):
    d.rectangle([x - 140 * s, y - 70 * s, x + 140 * s, y + 70 * s], fill=col)
    for i in range(6): d.ellipse([x + 70 * s - 6 * s, y - 64 * s + i * 24 * s, x + 70 * s + 6 * s, y - 52 * s + i * 24 * s], fill=BG)
    d.polygon([(x - 90 * s, y - 10 * s), (x - 20 * s, y - 10 * s), (x - 10 * s, y - 34 * s), (x + 4 * s, y - 34 * s), (x - 4 * s, y - 10 * s), (x + 30 * s, y - 10 * s), (x + 30 * s, y + 4 * s), (x - 90 * s, y + 4 * s)], fill=WHITE)

def box(d, x, y, s=1.0):
    d.rectangle([x - 110 * s, y - 80 * s, x + 110 * s, y + 80 * s], fill=INK); d.line([x - 110 * s, y - 30 * s, x + 110 * s, y - 30 * s], fill=MID, width=int(4 * s))

def sc_hook(img, d, t):
    tr = cue("hook", "trip")
    d.text((X0 - 6, 300), "WAITING…", font=F(BLK, 180), fill=INK)
    box(d, 260, 620, .8); d.text((260, 720), "new phone", font=F(COND, 28), fill=INK, anchor="ma")
    d.rectangle([150, 760, 370, 790], outline=INK, width=3); d.rectangle([154, 764, 154 + 212 * (.3 + .05 * math.sin(t)), 786], fill=MID)
    picto(d, 260, FLOOR, .62, MID, pose=WORRY, head_dy=3 * math.sin(t * 12))
    if t >= tr - .3:
        k = ease((t - tr + .3) / .4)
        ticket(d, 700, 620, .8 * k); d.text((700, 720), "a trip", font=F(COND, 28), fill=SIG, anchor="ma")
        picto(d, 700, FLOOR, .62, SIG, f=-1, pose=OPEN)
        note(d, 760, 840, 860, 960, "joy", (t - cue("hook", "joy")) / .35, SIG, anchor="ra", size=32)
    fig(d, "fig. 1 — two kinds of waiting")

def sc_study(img, d, t):
    t0 = S("study")
    counter(d, X0, 300, t, t0 + .1, 1.2, 2266, "{:,.0f}", 170, SIG); d.text((X0 + 6, 500), "people, pinged at random moments", font=F(COND, 34), fill=INK)
    for i in range(30):
        r, c = divmod(i, 10); x = X0 + 40 + c * 86; y = 760 + r * 140
        picto(d, x, y, .28, MID, pose=IDLE)
        if (int(t * 5) + i * 7) % 11 == 0: d.ellipse([x + 20, y - 150, x + 36, y - 134], fill=SIG)
    speech_box(d, X0 + 240, 560, 520, (t - cue("study", "asked") + .1) / .4, INK, 1, "What are you thinking about?", 30)
    fig(d, "experience sampling · Kumar, Killingsworth & Gilovich, 2014")

def sc_result(img, d, t):
    t0 = S("result")
    d.text((X0, 320), "HAPPIER", font=F(BLK, 130), fill=INK)
    d.text((X0, 470), "while looking forward to…", font=F(COND, 34), fill=INK)
    hbar(d, 580, .82, (t - cue("result", "experience") + .2) / .5, SIG, "an experience", h=100)
    hbar(d, 780, .5, (t - cue("result", "a thing") + .2) / .5, INK, "a thing", h=100)
    ticket(d, X1 - 100, 630, .4, WHITE) if t > cue("result", "experience") else None
    d.text((X1, 1146), "schematic", font=F(MED, 22), fill=MID, anchor="ra")

def queue(d, y, label, t, happy, k):
    d.text((X0, y - 290), label, font=F(BLK, 40), fill=SIG if happy else INK)
    for i in range(6):
        kk = ease(k - i * .08)
        if kk <= 0: continue
        x = X0 + 40 + i * 120
        pose = (TALK(t, i) if i % 2 else LAUGH) if happy else (WORRY if i % 2 else IDLE)
        picto(d, x, y, .4, SIG if happy else MID, f=-1, pose=pose)

def sc_queue(img, d, t):
    t0 = S("queue")
    d.text((X0, 300), "IN LINE FOR…", font=F(BLK, 110), fill=INK)
    queue(d, 770, "a concert", t, True, (t - cue("queue", "experiences") + .3) / .5)
    queue(d, 1110, "the newest gadget", t, False, (t - cue("queue", "stuff") + .3) / .5)
    fig(d, "news reports of queues · better moods for experiences")

def sc_point(img, d, t):
    t0 = S("point"); gf = cue("point", "gift")
    words_in(d, t, [("BOOK IT", t0, 300, 160, INK), ("EARLY.", t0 + .3, 460, 160, SIG)])
    ticket(d, 480, 800, 1.2)
    for i in range(7):
        x = X0 + i * 120; k = ease((t - t0 - .4 - i * .1) / .3)
        if k > 0: d.rectangle([x, 980, x + 100, 1060], outline=INK, width=3, fill=SIG_L if i < 6 else SIG); d.text((x + 50, 1020), f"−{6 - i}" if i < 6 else "GO", font=F(COND, 28), fill=INK if i < 6 else WHITE, anchor="mm")
    if t >= gf: note(d, X0 + 300, 980, 860, 1110, "all of this counts", (t - gf) / .35, SIG, anchor="ra", size=26)

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "queue": sc_queue, "point": sc_point}
FX = [(0.0, thud(.5), 0), (cue("hook", "trip"), pop(.2), .3), (cue("hook", "joy"), riser(.4, .06), .3), *EP.cut_fx(),
      *[(S("study") + .1 + i * .1, tick(.05), (i % 5 - 2) / 3) for i in range(12)], (cue("study", "asked"), pop(.18), 0),
      (S("result") + .05, thud(.5), 0), (cue("result", "a thing"), pop(.15), -.2), (cue("queue", "experiences"), pop(.15), -.2), (cue("queue", "stuff"), pop(.15), .2),
      (cue("point", "early"), thud(.45), 0), (cue("point", "gift"), riser(.4, .07), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
