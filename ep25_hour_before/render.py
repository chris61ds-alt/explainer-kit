"""NOT JUST YOU – No. 25: the hour before a meeting (Tonietto, Malkoc & Nowlis 2019). Area: time."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .8, "felt": .5, "done": .5, "name": .5, "tip": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "felt", "done", "name", "tip", "end"]
EP = Episode(TL, 25, "THE HOUR BEFORE", order=ORDER,
             chapters={"hook": "MEETING AT 11", "study": "THE STUDY", "felt": "FELT TIME", "done": "GOT DONE", "name": "THE RULE", "tip": "THE FIX"},
             sources=("Tonietto, Malkoc & Nowlis (2019), Journal of", "Consumer Research 45(5) · via Ohio State News"),
             music=dict(bpm=96, root=1, prog="warm", kick="half", gaps=[(E("study") + .05, S("felt") + .05)]),
             cover=dict(words=["MEETING", "IN 1 HOUR?"], kicker="Why that hour feels useless."))

def day_view(d, x0, y0, x1, y1, blocks, hours=("9", "10", "11", "12", "13", "14", "15", "16", "17")):
    n = len(hours) - 1; hh = (y1 - y0) / n
    for i, h in enumerate(hours):
        y = y0 + i * hh; d.line([x0 + 60, y, x1, y], fill=RULE, width=2); d.text((x0, y), h, font=F(MONO, 22), fill=MID, anchor="lm")
    for (a, b, lab, col) in blocks:
        d.rectangle([x0 + 70, y0 + a * hh, x1 - 10, y0 + b * hh - 6], fill=col)
        if lab: d.text((x0 + 90, y0 + a * hh + 10), lab, font=F(COND, 26), fill=WHITE)

def sc_hook(img, d, t):
    d.text((X0 - 6, 300), "MEETING", font=F(BLK, 170), fill=INK)
    d.text((X0, 470), "at 11.", font=F(BLK, 100), fill=SIG)
    clock(d, 270, 820, 150, minutes=600 + t * 3)
    day_view(d, 500, 620, X1, 1100, [(2, 3, "MEETING", SIG)], hours=("9", "10", "11", "12", "13"))
    if t >= cue("hook", "can't"):
        k = ease((t - cue("hook", "can't")) / .4)
        d.rectangle([570, 740, 570 + (X1 - 580) * k, 850], fill=RULE); d.text((590, 795), "…can't really start anything", font=F(COND, 26), fill=INK, anchor="lm") if k > .9 else None
    fig(d, "fig. 1 — 10:00, and the hour feels gone")

def strip(d, y, label, k, appt):
    d.text((X0, y - 44), label, font=F(COND, 30), fill=INK)
    d.rectangle([X0, y, X0 + (X1 - X0) * ease(k), y + 80], outline=INK, width=4)
    if appt and k > .9:
        d.rectangle([X1 - 120, y, X1, y + 80], fill=SIG); d.text((X1 - 60, y + 40), "FRIEND", font=F(COND, 22), fill=WHITE, anchor="mm")

def sc_study(img, d, t):
    t0 = S("study"); ap = cue("study", "appointment")
    d.text((X0, 320), "SAME FREE TIME", font=F(BLK, 100), fill=INK)
    strip(d, 560, "group A: nothing planned after", (t - t0 - .2) / .5, False)
    strip(d, 760, "group B: an appointment coming up", (t - ap + .3) / .5, True)
    fig(d, "online study, n = 198 · Tonietto, Malkoc & Nowlis, 2019")

def sc_felt(img, d, t):
    t0 = S("felt"); tm = cue("felt", "ten minutes")
    d.text((X0, 320), "FELT LIKE", font=F(BLK, 130), fill=INK)
    counter(d, X0, 480, t, t0 + .1, .6, 50, "≈ {:.0f} min", 110, INK); d.text((X0 + 6, 600), "no appointment", font=F(COND, 30), fill=INK)
    counter(d, X0, 700, t, tm - .3, .7, 40, "≈ {:.0f} min", 110, SIG); d.text((X0 + 6, 820), "appointment coming", font=F(COND, 30), fill=SIG) if t >= tm - .3 else None
    if t >= tm + .3: box_label(d, X1, 980, "−10 MINUTES", 40, WHITE, SIG, anchor="ra")
    fig(d, "objectively: about 50 minutes free in both cases")

def sc_done(img, d, t):
    t0 = S("done"); ld = cue("done", "less done")
    d.text((X0, 320), "IN 5 MINUTES", font=F(BLK, 110), fill=INK)
    for i, (lab, v, col, tk) in enumerate((("no reminder", 2.38, INK, t0 + .2), ("reminded of a task", 1.86, SIG, ld - .3))):
        y = 560 + i * 220; k = ease((t - tk) / .6)
        d.text((X0, y), lab, font=F(COND, 30), fill=INK)
        d.rectangle([X0, y + 50, X0 + 300 * v * k, y + 140], fill=col)
        if k > .9: d.text((X0 + 300 * v + 20, y + 95), f"{v:.2f}", font=F(BLK, 60), fill=col, anchor="lm")
    d.text((X0, 1040), "activities completed, on average", font=F(COND, 28), fill=MID)
    fig(d, "lab study, n = 158")

def sc_name(img, d, t):
    t0 = S("name")
    words_in(d, t, [("DEADLINES", t0 + .1, 300, 150, INK), ("SHRINK", cue("name", "shorter") - .3, 460, 150, SIG), ("TIME.", cue("name", "shorter"), 620, 150, INK)])
    clock(d, 700, 960, 110 * (1 - .3 * ease((t - cue("name", "shorter")) / .6)), t=t, speed=4)

def sc_tip(img, d, t):
    t0 = S("tip"); bt = cue("tip", "batch")
    d.text((X0, 320), "BATCH THEM", font=F(BLK, 120), fill=INK)
    k = ease_io((t - bt) / 1.0)
    blocks = [(lerp(1, 6, k), lerp(1.6, 6.6, k), "MEET", SIG), (lerp(3.2, 6.6, k), lerp(3.8, 7.2, k), "CALL", SIG), (lerp(5, 7.2, k), lerp(5.6, 7.8, k), "SYNC", SIG)]
    if k > .9: blocks = [(0, 5.8, "DEEP WORK", INK)] + blocks
    day_view(d, X0, 480, X1, 1100, blocks)
    if t >= cue("tip", "count"): note(d, X0 + 300, 700, 860, 560, "count the real minutes", (t - cue("tip", "count")) / .35, WHITE, anchor="ra", size=30)

EP.scenes = {"hook": sc_hook, "study": sc_study, "felt": sc_felt, "done": sc_done, "name": sc_name, "tip": sc_tip}
FX = [(0.0, thud(.5), 0), *[(.3 + i * .5, tick(.06), 0) for i in range(4)], (cue("hook", "can't"), rewind_sfx(.1, .3), 0), *EP.cut_fx(),
      (cue("study", "appointment"), pop(.18), .3), (S("felt") + .05, thud(.5), 0), (cue("felt", "ten minutes"), thud(.35), .2),
      (cue("done", "less done"), pop(.18), .2), (cue("name", "shorter") - .3, thud(.45), 0), (cue("tip", "batch"), whoosh(1.0, .1), 0),
      (cue("tip", "batch") + 1.0, pop(.2), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
