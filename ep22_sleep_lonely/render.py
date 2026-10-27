"""NOT JUST YOU – No. 22: sleep loss and social withdrawal (Ben Simon & Walker 2018). Area: sleep."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .45, "num": .6, "others": .5, "viral": .5, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "num", "others", "viral", "point", "end"]
EP = Episode(TL, 22, "BAD NIGHT", order=ORDER,
             chapters={"hook": "STAY BACK", "study": "THE TEST", "num": "THE DISTANCE", "others": "THE VIEWERS", "viral": "CONTAGIOUS", "point": "JUST SLEEP"},
             sources=("Ben Simon & Walker (2018),", "Nature Communications 9 · via UC Berkeley"),
             music=dict(bpm=86, root=-5, prog="tense", kick="half", gaps=[(E("study") + .05, S("num") + .05)]),
             cover=dict(words=["STAY", "BACK."], kicker="What one bad night does to you."))

STOP = {"arms": ((90, 0), (80, 0))}
def tired(d, h, s=1.0):
    for i in range(3): d.line([h[0] - 30 * s + i * 30 * s, h[1] - 50 * s, h[0] - 22 * s + i * 30 * s, h[1] - 64 * s], fill=SIG, width=int(5 * s))

def sc_hook(img, d, t):
    d.text((X0 - 6, 300), "STAY BACK.", font=F(BLK, 160), fill=INK)
    lit = cue("hook", "literally")
    h = picto(d, 260, FLOOR, 1.0, INK, f=1, pose=STOP if t > .4 else IDLE); tired(d, h)
    x = move(t, [(0, 820), (.3, 700), (lit, 760)])
    picto(d, x, FLOOR, 1.0, MID, f=-1, pose=WALK(t) if t < 1.2 else IDLE)
    if t >= lit: dim_h(d, 380, x - 70, 640, (t - lit) / .4, SIG, "PERSONAL SPACE: +", 24)
    fig(d, "fig. 1 — after a sleepless night")

def screen(d, x0, y0, x1, y1, t, prog, stop_at):
    d.rectangle([x0, y0, x1, y1], outline=INK, width=6)
    s = lerp(.3, .9, min(prog, stop_at))
    picto(d, (x0 + x1) / 2, y1 - 20, s, MID, pose=WALK(t) if prog < stop_at else IDLE)

def sc_study(img, d, t):
    t0 = S("study"); sp = cue("study", "stopped")
    d.text((X0, 320), "COME CLOSER", font=F(BLK, 110), fill=INK)
    prog = clamp((t - t0) / 3.0)
    screen(d, X0 + 300, 500, X1, 1100, t, prog, .55 if t >= sp else 1)
    h = picto(d, X0 + 140, FLOOR, .9, INK, f=1, pose=STOP if t >= sp else IDLE); tired(d, h, .9)
    if t >= sp: box_label(d, X0 + 140, 520, "STOP", 34, WHITE, SIG, anchor="ma")
    fig(d, "Ben Simon & Walker — Nature Communications, 2018 · 18 adults")

def sc_num(img, d, t):
    t0 = S("num")
    d.text((X0, 320), "+18–60 %", font=F(BLK, 170), fill=SIG)
    d.text((X0, 520), "more distance kept", font=F(COND, 38), fill=INK)
    k1 = ease((t - t0 - .2) / .5); k2 = ease((t - cue("num", "farther") + .2) / .6)
    d.text((X0, 620), "rested", font=F(COND, 30), fill=INK)
    picto(d, X0 + 40, 860, .42, INK, pose=IDLE); picto(d, X0 + 40 + 360 * k1 + 20, 860, .42, MID, f=-1, pose=IDLE)
    dim_h(d, X0 + 70, X0 + 40 + 360 * k1, 890, 1, INK, None)
    d.text((X0, 920), "after no sleep", font=F(COND, 30), fill=INK)
    picto(d, X0 + 40, 1120, .42, INK, pose=STOP); xo = X0 + 40 + 360 * (1 + .6 * k2) + 20
    picto(d, xo, 1120, .42, MID, f=-1, pose=IDLE)
    d.rectangle([X0 + 40 + 360 * 1.18, 1128, X0 + 40 + 360 * 1.6, 1140], fill=SIG_L)
    dim_h(d, X0 + 70, xo - 20, 1160, k2, SIG, None)

def sc_others(img, d, t):
    t0 = S("others"); rl = cue("others", "lonelier")
    d.text((X0, 320), "1,000+ VIEWERS", font=F(BLK, 104), fill=INK)
    d.text((X0, 440), "didn't know who had slept", font=F(COND, 34), fill=INK)
    for i in range(30):
        r, c = divmod(i, 10); k = ease((t - t0 - i * .02) / .3)
        if k > 0: picto(d, X0 + 40 + c * 86, 680 + r * 120, .26, MID, pose=IDLE)
    if t >= rl - .2:
        k = ease((t - rl + .2) / .5)
        d.text((X0, 1010), "rated them:", font=F(COND, 30), fill=INK)
        d.rectangle([X0 + 200, 1000, X1, 1044], outline=INK, width=4); d.rectangle([X0 + 206, 1006, X0 + 206 + (X1 - X0 - 212) * .72 * k, 1038], fill=SIG)
        d.text((X1, 1060), "lonelier", font=F(MONO, 20), fill=SIG, anchor="ra")

def sc_viral(img, d, t):
    t0 = S("viral"); fl = cue("viral", "lonelier")
    d.text((X0, 320), "CONTAGIOUS", font=F(BLK, 120), fill=SIG)
    picto(d, 240, FLOOR, .9, INK, pose=WORRY)
    for i in range(5):
        x = 480 + i * 90; col = mix(MID, SIG, ease((t - fl + .3 - i * .08) / .4) * .7)
        picto(d, x, FLOOR, .5, col, f=-1, pose=IDLE)
    for i in range(3):
        k = ease((t - t0 - .3 - i * .2) / .4)
        if k > 0:
            x = lerp(300, 480 + i * 160, k)
            for xx in range(300, int(x), 26): d.line([xx, 760 + i * 20, xx + 12, 760 + i * 20], fill=MID, width=4)
    if t >= fl: note(d, 660, 880, 860, 560, "a little lonelier", (t - fl) / .35, SIG, anchor="ra", size=28)
    fig(d, "fig. 2 — after watching a 60-second clip")

def sc_point(img, d, t):
    t0 = S("point")
    words_in(d, t, [("NOBODY", t0, 300, 150, INK), ("LIKES ME?", t0 + .3, 450, 150, INK)] if t < cue("point", "maybe") - .1
             else [("MAYBE", cue("point", "maybe") - .1, 300, 150, INK), ("JUST SLEEP.", cue("point", "sleep") - .2, 450, 150, SIG)])
    bed(d, X0 + 120, 1080, 600)
    d.ellipse([X0 + 180, 870, X0 + 260, 950], fill=INK); d.rounded_rectangle([X0 + 250, 910, X0 + 690, 970], radius=30, fill=MID)
    if t >= cue("point", "sleep"):
        for i in range(3): d.text((X0 + 300 + i * 40, 840 - i * 34), "z", font=F(BLK, 34 + i * 10), fill=MID)
    fig(d, "fig. 3 — the cheapest social skill")

EP.scenes = {"hook": sc_hook, "study": sc_study, "num": sc_num, "others": sc_others, "viral": sc_viral, "point": sc_point}
FX = [(0.0, thud(.5), 0), (.4, pop(.15), -.2), (cue("hook", "literally"), thud(.35), 0), *EP.cut_fx(),
      (cue("study", "stopped"), pop(.2), -.2), (S("num") + .05, thud(.5), 0), (cue("num", "farther"), whoosh(.6, .1), .3),
      *[(S("others") + i * .08, tick(.04), (i % 5 - 2) / 3) for i in range(10)], (cue("others", "lonelier"), thud(.35), 0),
      (cue("viral", "lonelier"), riser(.4, .06), .3), (cue("point", "maybe"), thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
