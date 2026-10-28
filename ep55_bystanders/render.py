"""NOT JUST YOU – No. 55: bystanders do intervene (Philpot et al. 2020, CCTV). Swiss Dark."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .6, "study": .8, "result": .6, "more": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "more", "point", "end"]
EP = Episode(TL, 55, "NOBODY HELPS?", order=ORDER, dark=True,
             chapters={"hook": "THE MYTH", "study": "THE FOOTAGE", "result": "9 IN 10", "more": "MORE PEOPLE", "point": "BE ONE"},
             sources=("Philpot, Liebst, Levine, Bernasco & Lindegaard", "(2020), American Psychologist 75(1)"),
             music=dict(bpm=92, root=0, prog="tense", kick="four", gaps=[(E("study") + .05, S("result") + .05)]),
             cover=dict(words=["NOBODY", "HELPS?"], kicker="Wrong. 9 out of 10 times."))

def cctv(d, x0, y0, x1, y1, t, label="CAM 03"):
    d.rectangle([x0, y0, x1, y1], outline=INK, width=5)
    for i in range(int(y0) + 10, int(y1), 14): d.line([x0 + 5, i, x1 - 5, i], fill=mix(BG, INK, .05), width=2)
    if int(t * 2) % 2 == 0: d.ellipse([x0 + 20, y0 + 20, x0 + 40, y0 + 40], fill=SIG)
    d.text((x0 + 52, y0 + 18), "REC " + label, font=F(MONO, 22), fill=INK)
    d.text((x1 - 20, y1 - 36), f"00:{int(t * 7) % 60:02d}:{int(t * 30) % 30:02d}", font=F(MONO, 20), fill=MID, anchor="ra")

def sc_hook(img, d, t):
    tm = cue("hook", "that's a myth")
    d.text((X0 - 6, 300), "NOBODY", font=F(BLK, 210), fill=INK if t < tm else RULE); d.text((X0 - 6, 500), "HELPS?", font=F(BLK, 210), fill=SIG if t < tm else RULE)
    if t >= tm - .1:
        k = ease((t - tm + .1) / .3); d.line([X0, 640, X0 + 760 * k, 560], fill=SIG, width=14)
        box_label(d, X1, 760, "MYTH.", 70, WHITE, SIG, font=BLK, anchor="ra")
    picto(d, 300, FLOOR, .8, INK, f=1, pose=WORRY)
    for i, x in enumerate((560, 680, 800)): picto(d, x, FLOOR, .6, MID, f=-1, pose=IDLE)
    fig(d, "fig. 1 — the story everyone knows")

def sc_study(img, d, t):
    t0 = S("study")
    counter(d, X0, 300, t, t0 + .1, 1.0, 219, "{:.0f}", 220, SIG)
    d.text((X0 + 6, 540), "real street fights on camera", font=F(COND, 36), fill=INK)
    for i, (c, lab) in enumerate((("AMS", "Amsterdam"), ("CPT", "Cape Town"), ("LAN", "Lancaster"))):
        k = ease((t - cue("study", "three countries") + .3 - i * .15) / .3)
        if k <= 0: continue
        x0 = X0 + i * 290; cctv(d, x0, 640 + (1 - k) * 30, x0 + 260, 860 + (1 - k) * 30, t + i, c)
        d.text((x0, 880), lab, font=F(COND, 28), fill=INK)
    fig(d, "CCTV footage, 3 countries · Philpot et al., 2020")

def sc_result(img, d, t):
    t0 = S("result"); tn = cue("result", "nine out")
    d.text((X0, 300), "9 IN 10", font=F(BLK, 230), fill=SIG)
    d.text((X0 + 6, 540), "someone stepped in", font=F(COND, 40), fill=INK)
    for i in range(10):
        r, c = divmod(i, 5); x = X0 + 30 + c * 175; y = 640 + r * 210; on = i < 9 and t >= tn + i * .08
        cctv(d, x, y, x + 150, y + 180, t + i * .3, f"{i + 1:02d}")
        if on: picto(d, x + 75, y + 165, .3, SIG, pose=OPEN)
        elif t >= tn + .9: d.text((x + 75, y + 100), "—", font=F(BLK, 40), fill=MID, anchor="mm")
    fig(d, "≈ 91 % · on average 3–4 people helped")

def sc_more(img, d, t):
    t0 = S("more")
    d.text((X0, 300), "MORE PEOPLE", font=F(BLK, 120), fill=INK); d.text((X0, 430), "= MORE HELP", font=F(BLK, 120), fill=SIG)
    k = clamp((t - t0 - .2) / 2.0); n = 1 + int(7 * k)
    for i in range(n):
        x = 180 + i * 90; picto(d, x, FLOOR, .55, SIG if i % 2 == 0 else MID, f=1, pose=OPEN if i % 2 == 0 else IDLE)
    hbar(d, 640, .3 + .6 * k, 1, SIG, "odds that someone helps", h=70)
    fig(d, "each extra bystander raised the odds · schematic")

def sc_point(img, d, t):
    t0 = S("point"); tb = cue("point", "be one")
    words_in(d, t, [("PEOPLE", t0, 300, 190, INK), ("SHOW UP.", t0 + .3, 480, 170, SIG)] if t < tb - .2 else [("BE", tb - .2, 300, 190, INK), ("ONE OF THEM.", tb, 480, 120, SIG)])
    picto(d, 340, FLOOR, .85, INK, f=1, pose=WORRY)
    picto(d, 600, FLOOR, .95, SIG, f=-1, pose=OPEN if t >= tb else IDLE)
    fig(d, "fig. 2 — the rule, not the exception")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "more": sc_more, "point": sc_point}
FX = [(0.0, thud(.5), 0), (cue("hook", "that's a myth"), rewind_sfx(.12, .35), 0), (cue("hook", "that's a myth") + .3, thud(.5), 0), *EP.cut_fx(),
      *[(cue("study", "three countries") - .3 + i * .15, pop(.12), (i - 1) / 2) for i in range(3)], (S("result") + .05, thud(.55), 0),
      *[(cue("result", "nine out") + i * .08, tick(.04), (i % 5 - 2) / 3) for i in range(9)], (S("more") + .2, riser(2.0, .05), 0),
      (cue("point", "be one") - .2, thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
