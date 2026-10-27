"""NOT JUST YOU – No. 14: the photo-taking impairment effect (Henkel 2014). Area: memory."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .4, "study": .8, "result": .5, "name": .45, "why": .45, "twist": .5, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "name", "why", "twist", "point", "end"]
EP = Episode(TL, 14, "LOOK UP", order=ORDER,
             chapters={"hook": "THE CONCERT", "study": "THE MUSEUM", "result": "THE NEXT DAY", "name": "THE NAME", "why": "WHY",
                       "twist": "THE TWIST", "point": "LOOK UP"},
             sources=("Henkel (2014), Psychological Science 25(2)", "via Live Science"),
             music=dict(bpm=92, root=0, prog="dream", kick="half", gaps=[(E("study") + .05, S("result") + .05)]),
             cover=dict(words=["LOOK", "UP."], kicker="Why photos make you forget."))

FILM = {"arms": ((130, 95), (125, 100))}
def phone_acc(d, h, s):
    if not getattr(phone_acc, "on", True): return
    phone(d, h[0] + 80 * s, h[1] - 20 * s, .55 * s, INK, lit=True)
POSES = [(0, FILM), (cue("point", "look up") - .2, IDLE), (cue("point", "actually"), OPEN)]
ACT = actors_layer(ORDER, S, [dict(col=INK, f=1, tg={"hook": (300, 1.0, 0), "study": (300, 1.0, 700), "result": (300, 1.0, 700),
    "name": (300, 1.0, 700), "why": (230, .9, 0), "twist": (230, .9, 700), "point": (300, 1.0, 0)}, poses=POSES, acc=phone_acc)])
EP.layers.append(ACT)

def stage_lights(d, t, x0=470, x1=880, y=420):
    d.rectangle([x0, y + 200, x1, y + 220], fill=INK)
    for i in range(3):
        cx = x0 + 60 + i * 140; sw = 40 * math.sin(t * 2 + i)
        d.polygon([(cx - 14, y), (cx + 14, y), (cx + 70 + sw, y + 200), (cx - 70 + sw, y + 200)], fill=(242, 241, 236))
        d.rectangle([cx - 18, y - 16, cx + 18, y + 6], fill=INK)
    for i, x in enumerate((560, 680, 800)): picto(d, x, y + 200, .32, SIG if i == 1 else INK, pose=SING(t + i))

def sc_hook(img, d, t):
    d.text((X0 - 8, 300), "REC", font=F(BLK, 200), fill=INK)
    if int(t * 2) % 2 == 0: d.ellipse([440, 340, 500, 400], fill=SIG)
    stage_lights(d, t, y=600)
    phone_acc.on = True
    if t >= cue("hook", "remember"):
        note(d, 380, 730, 470, 520, "watching through a screen", (t - cue("hook", "remember")) / .35, SIG, size=26)
    fig(d, "fig. 1 — the whole concert, on your phone")

def sc_study(img, d, t):
    t0 = S("study"); ph = cue("study", "photographed")
    d.text((X0, 320), "THE MUSEUM", font=F(BLK, 110), fill=INK)
    for i in range(3): frame_art(d, X0 + 20 + i * 290, 520, X0 + 240 + i * 290, 760, kind=i)
    picto(d, X0 + 130, FLOOR, .62, INK, f=1, pose=IDLE); eye(d, X0 + 130, 830, .7, INK, look=(0, -1))
    box_label(d, X0 + 130, 1000, "LOOKED", 26, WHITE, INK, anchor="ma")
    if t >= ph - .2:
        picto(d, X0 + 710, FLOOR, .62, SIG, f=-1, pose=FILM)
        camera(d, X0 + 660, 860, .55, INK, flash=clamp((t - ph) * 3 % 1) if t - ph < 1.2 else 0)
        box_label(d, X0 + 710, 1000, "PHOTOGRAPHED", 26, WHITE, SIG, anchor="ma")
    fig(d, "Henkel — Psychological Science, 2014")

def sc_result(img, d, t):
    t0 = S("result")
    d.text((X0, 320), "THE NEXT DAY", font=F(BLK, 100), fill=INK)
    d.text((X0, 440), "memory for the objects", font=F(COND, 34), fill=INK)
    hbar(d, 560, .8, (t - t0) / .5, INK, "only looked at", h=100)
    hbar(d, 760, .52, (t - cue("result", "worse") + .3) / .5, SIG, "photographed", h=100)
    if t >= cue("result", "worse") + .3: dim_h(d, X0 + 840 * .52, X0 + 840 * .8, 900, (t - cue("result", "worse") - .3) / .4, SIG, "LESS", 24)
    d.text((X1, 1146), "schematic", font=F(MED, 22), fill=MID, anchor="ra")

def sc_name(img, d, t):
    words_in(d, t, [("PHOTO-", cue("name", "photo") - .1, 330, 170, INK), ("TAKING", cue("name", "taking") - .1, 500, 170, INK),
                    ("IMPAIRMENT", cue("name", "impairment") - .1, 680, 140, SIG), ("EFFECT.", cue("name", "effect") - .1, 840, 140, INK)])

def sc_why(img, d, t):
    t0 = S("why"); sv = cue("why", "saved"); phone_acc.on = False
    d.text((X0, 320), "OUTSOURCED", font=F(BLK, 120), fill=INK)
    camera(d, 680, 720, 1.4, INK)
    h = ACT.heads.get(0, (230, 760))
    k = ease((t - cue("why", "hands")) / .6)
    if k > 0:
        x1 = lerp(h[0] + 60, 560, k)
        for xx in range(int(h[0] + 60), int(x1), 28): d.line([xx, h[1], xx + 14, h[1] - 3], fill=SIG, width=6)
    if t >= sv: box_label(d, 680, 830, "SAVED", 30, WHITE, SIG, anchor="ma")
    if t >= sv + .4:
        d.rectangle([X0 + 20, 470, X0 + 300, 540], outline=INK, width=4); d.text((X0 + 40, 505), "memory: —", font=F(COND, 30), fill=MID, anchor="lm")
    fig(d, "one explanation: cognitive offloading")

def sc_twist(img, d, t):
    t0 = S("twist"); zi = cue("twist", "zooming")
    d.text((X0, 320), "ZOOM IN", font=F(BLK, 130), fill=INK)
    frame_art(d, 200, 500, 760, 1060, kind=2)
    if t >= zi - .1:
        k = ease((t - zi + .1) / .4); cx, cy, w = 480, 700, 120 * k
        for (x, y, sx, sy) in ((cx - w, cy - w, 1, 1), (cx + w, cy - w, -1, 1), (cx - w, cy + w, 1, -1), (cx + w, cy + w, -1, -1)):
            d.line([x, y, x + sx * 40, y], fill=SIG, width=6); d.line([x, y, x, y + sy * 40], fill=SIG, width=6)
    if t >= cue("twist", "whole") - .1:
        k = ease((t - cue("twist", "whole") + .1) / .4)
        d.rectangle([200 - 16 * k, 500 - 16 * k, 760 + 16 * k, 1060 + 16 * k], outline=SIG, width=6)
        box_label(d, 480, 1080, "REMEMBERED: ALL OF IT", 26, WHITE, SIG, anchor="ma")
    fig(d, "Henkel, 2014 — experiment 2")

def sc_point(img, d, t):
    t0 = S("point"); lu = cue("point", "look up")
    stage_lights(d, t, y=600)
    phone_acc.on = t < lu
    words_in(d, t, [("TAKE IT.", t0, 300, 150, INK)] if t < lu else [("LOOK UP.", lu, 300, 150, SIG)])
    if t >= cue("point", "actually"): eye(d, 380, 720, .9, SIG, look=(1, -.6))
    fig(d, "fig. 2 — the same concert, in your head")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "name": sc_name, "why": sc_why, "twist": sc_twist, "point": sc_point}
FX = [(0.0, thud(.5), 0), (.2, pop(.15), .2), *EP.cut_fx(),
      (cue("study", "photographed"), pop(.25), .3), (S("result") + .05, thud(.55), 0), (cue("result", "worse"), thud(.35), .2),
      *[(cue("name", w) - .1, thud(.3), 0) for w in ("photo", "taking", "impairment", "effect")],
      (cue("why", "hands"), whoosh(.5, .12), .3), (cue("why", "saved"), pop(.2), .3),
      (cue("twist", "zooming"), pop(.18), 0), (cue("twist", "whole"), riser(.4, .07), 0),
      (cue("point", "look up"), thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
