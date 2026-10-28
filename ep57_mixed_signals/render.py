"""NOT JUST YOU · AFTER DARK – No. 57: misperceiving sexual interest (Perilloux, Easton & Buss 2012)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .8, "result": .6, "who": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "who", "point", "end"]
EP = Episode(TL, 57, "MIXED SIGNALS", order=ORDER, dark=True, series="NOT JUST YOU · AFTER DARK",
             chapters={"hook": "A SMILE", "study": "SPEED DATING", "result": "THE MISREAD", "who": "THE WORST", "point": "ASK"},
             sources=("Perilloux, Easton & Buss (2012),", "Psychological Science 23(2)"),
             music=dict(bpm=90, root=1, prog="dream", kick="half", gaps=[(E("study") + .05, S("result") + .05)]),
             cover=dict(words=["INTO", "YOU?"], kicker="Maybe not."))

def meter(d, x, y, w, real, guess, k, col):
    d.rectangle([x, y, x + w, y + 34], outline=INK, width=3)
    d.rectangle([x + 3, y + 3, x + 3 + (w - 6) * real, y + 31], fill=MID)
    gx = x + w * lerp(real, guess, ease(k)); d.polygon([(gx - 14, y - 22), (gx + 14, y - 22), (gx, y - 2)], fill=col)

def sc_hook(img, d, t):
    tm = cue("hook", "maybe not")
    d.text((X0 - 6, 300), "INTO", font=F(BLK, 230), fill=INK); d.text((X0 - 6, 510), "YOU?", font=F(BLK, 230), fill=SIG)
    picto(d, 340, FLOOR, .95, INK, f=1, pose=OPEN)
    h = picto(d, 640, FLOOR, .95, SIG, f=-1, pose=IDLE)
    d.arc([h[0] - 18, h[1] - 4, h[0] + 18, h[1] + 20], 20, 160, fill=BG, width=5)
    if t >= tm: box_label(d, X1, 800, "MAYBE NOT.", 40, WHITE, INK, anchor="ra")
    fig(d, "fig. 1 — one smile, many theories")

def sc_study(img, d, t):
    t0 = S("study")
    counter(d, X0, 300, t, t0 + .1, .9, 199, "{:.0f}", 220, SIG)
    d.text((X0 + 6, 540), "students · 3-minute speed dates", font=F(COND, 36), fill=INK)
    for i in range(5):
        k = ease((t - t0 - .4 - i * .3) / .3)
        if k <= 0: continue
        y = 650 + i * 90
        d.text((X0, y), f"date {i + 1}", font=F(MONO, 22), fill=MID)
        clock(d, X0 + 180, y + 12, 26, t, None, INK, 2.0)
        d.text((X0 + 240, y), "how interested were they?", font=F(COND, 30), fill=INK)
    fig(d, "Perilloux, Easton & Buss, 2012")

def sc_result(img, d, t):
    t0 = S("result"); tw = cue("result", "women tended")
    d.text((X0, 300), "MEN: TOO HIGH", font=F(BLK, 110), fill=SIG)
    meter(d, X0, 520, 840, .35, .65, (t - t0 - .3) / .6, SIG)
    d.text((X0, 570), "grey = her actual interest · marker = his guess", font=F(COND, 26), fill=MID)
    if t >= tw - .3:
        d.text((X0, 680), "WOMEN: TOO LOW", font=F(BLK, 110), fill=INK)
        meter(d, X0, 900, 840, .6, .35, (t - tw) / .6, INK)
    d.text((X1, 1146), "schematic", font=F(MED, 22), fill=MID, anchor="ra")

def sc_who(img, d, t):
    t0 = S("who")
    d.text((X0, 300), "WORST READERS", font=F(BLK, 110), fill=INK)
    for i, (lab, w) in enumerate((("WANTS SOMETHING CASUAL", "casual"), ("MOST ATTRACTED TO HER", "most attracted"))):
        tk = cue("who", w) - .3; k = ease((t - tk) / .35)
        if k <= 0: continue
        y = 500 + i * 150
        d.text((X0, y + 8), f"0{i + 1}", font=F(MONO, 30), fill=MID)
        box_label(d, X0 + 70 + (1 - k) * 40, y, lab, 44, WHITE, SIG if i else INK)
    h = picto(d, 480, FLOOR, .8, INK, f=1, pose=OPEN)
    heart_r = 26 + 6 * math.sin(t * 6); cx, cy = h[0] + 70, h[1] - 90
    d.ellipse([cx - heart_r, cy - heart_r * .9, cx, cy + heart_r * .1], fill=SIG); d.ellipse([cx, cy - heart_r * .9, cx + heart_r, cy + heart_r * .1], fill=SIG)
    d.polygon([(cx - heart_r * .98, cy - heart_r * .3), (cx + heart_r * .98, cy - heart_r * .3), (cx, cy + heart_r * .95)], fill=SIG)
    fig(d, "overperception was strongest here")

def sc_point(img, d, t):
    t0 = S("point"); ta = cue("point", "so ask")
    words_in(d, t, [("WANT MORE,", t0, 300, 150, INK), ("READ WORSE.", t0 + .6, 450, 150, SIG)] if t < ta - .2 else [("ASK.", ta - .2, 300, 230, SIG), ("DON'T GUESS.", ta + .3, 520, 120, INK)])
    picto(d, 340, FLOOR, .85, INK, f=1, pose=TALK(t) if t >= ta else IDLE); picto(d, 620, FLOOR, .85, SIG, f=-1, pose=IDLE)
    if t >= ta: speech_box(d, 370, 760, 150, (t - ta) / .3, INK, 1, "?", 40)
    fig(d, "fig. 2 — a question beats a theory")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "who": sc_who, "point": sc_point}
FX = [(0.0, thud(.5), 0), (.4, pop(.15), .3), (cue("hook", "maybe not"), rewind_sfx(.1, .3), 0), *EP.cut_fx(),
      *[(S("study") + .4 + i * .3, tick(.04), (i - 2) / 3) for i in range(5)], (S("result") + .05, thud(.55), 0),
      (S("result") + .3, riser(.6, .05), -.2), (cue("result", "women tended"), whoosh(.6, .06), .2),
      *[(cue("who", w) - .3, pop(.15), (i - .5)) for i, w in enumerate(("casual", "most attracted"))],
      (cue("point", "so ask") - .2, thud(.5), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
