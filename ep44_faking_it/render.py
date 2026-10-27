"""NOT JUST YOU · AFTER DARK – No. 44: pretending orgasm is common, for women and men (Muehlenhard & Shippee 2010)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .8, "result": .5, "men": .5, "why": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "men", "why", "point", "end"]
EP = Episode(TL, 44, "FAKED IT", order=ORDER, dark=True, series="NOT JUST YOU · AFTER DARK",
             chapters={"hook": "THE PERFORMANCE", "study": "THE SURVEY", "result": "WOMEN", "men": "MEN", "why": "WHY", "point": "TALK"},
             sources=("Muehlenhard & Shippee (2010),", "Journal of Sex Research 47(6)"),
             music=dict(bpm=90, root=-2, prog="minor", kick="half", gaps=[(E("study") + .05, S("result") + .05)]),
             cover=dict(words=["FAKED", "IT?"], kicker="You're far from alone."))

def star(d, cx, cy, r, col=SIG):
    pts = [(cx + math.cos(math.radians(-90 + i * 36)) * (r if i % 2 == 0 else r * .45),
            cy + math.sin(math.radians(-90 + i * 36)) * (r if i % 2 == 0 else r * .45)) for i in range(10)]
    d.polygon(pts, fill=col)

def row(d, t, n, hit, y, s, tk, x0=X0 + 60, gap=None):
    gap = gap or (X1 - X0 - 120) / max(1, n - 1)
    for i in range(n):
        on = i < hit and t >= tk + i * .15
        picto(d, x0 + i * gap, y, s, SIG if on else MID, f=1 if i % 2 else -1, pose=LAUGH if on else IDLE)

def sc_hook(img, d, t):
    d.text((X0 - 6, 300), "FAKED", font=F(BLK, 220), fill=INK); d.text((X0 - 6, 500), "IT?", font=F(BLK, 220), fill=SIG)
    spotlight(d, 620, top=720, w=200); stage(d)
    picto(d, 620, FLOOR, .8, INK, f=-1, pose=SING(t))
    speech_box(d, 520, 760, 230, (t - .4) / .3, SIG, -1, "WOW!", 40)
    for i, (x, y) in enumerate(((760, 820), (820, 900), (720, 940))):
        star(d, x, y, 18 + 6 * math.sin(t * 6 + i), SIG if i % 2 else INK)
    fig(d, "fig. 1 — a convincing performance")

def sc_study(img, d, t):
    t0 = S("study"); k = clamp((t - t0 - .3) / 2.0)
    counter(d, X0, 300, t, t0 + .1, 1.0, 281, "{:.0f}", 220, SIG)
    d.text((X0 + 6, 540), "college students, anonymous survey", font=F(COND, 36), fill=INK)
    for i in range(int(281 * k)):
        r, c = divmod(i, 20); x = X0 + 20 + c * 42; y = 630 + r * 32
        d.ellipse([x - 10, y - 10, x + 10, y + 10], fill=SIG if i < 101 else INK)
    legend(d, [(SIG, "101 women"), (INK, "180 men")]) if k >= 1 else None
    fig(d, "Muehlenhard & Shippee, 2010")

def sc_result(img, d, t):
    t0 = S("result"); tk = cue("result", "two out")
    d.text((X0, 300), "WOMEN", font=F(BLK, 150), fill=INK)
    counter(d, X0, 470, t, tk - .2, .6, 67, "{:.0f} %", 190, SIG)
    row(d, t, 3, 2, FLOOR, 1.0, tk, x0=230, gap=250)
    if t >= cue("result", "said yes"): box_label(d, X1, 560, "2 IN 3", 40, WHITE, SIG, anchor="ra")
    fig(d, "women with intercourse experience")

def sc_men(img, d, t):
    t0 = S("men"); tk = cue("men", "more than")
    d.text((X0, 300), "MEN?", font=F(BLK, 150), fill=INK)
    counter(d, X0, 470, t, tk - .2, .6, 28, "{:.0f} %", 190, SIG)
    row(d, t, 4, 1, FLOOR, .9, tk, x0=200, gap=190)
    if t >= cue("men", "yes, men"): box_label(d, X1, 560 + (1 - ease((t - cue("men", "yes, men")) / .3)) * 30, "MEN TOO.", 44, WHITE, SIG, anchor="ra")
    fig(d, "men with intercourse experience")

def sc_why(img, d, t):
    t0 = S("why")
    d.text((X0, 300), "WHY?", font=F(BLK, 150), fill=INK)
    items = [("“IT WASN'T GOING TO HAPPEN”", "just wasn't"), ("“I WANTED IT TO END”", "wanted it to end"), ("“DON'T HURT THEIR FEELINGS”", "hurt their")]
    for i, (lab, w) in enumerate(items):
        tk = cue("why", w) - .3; k = ease((t - tk) / .35)
        if k <= 0: continue
        y = 520 + i * 170
        d.text((X0 + (1 - k) * 40, y), f"0{i + 1}", font=F(MONO, 30), fill=MID)
        box_label(d, X0 + 70 + (1 - k) * 40, y - 14, lab, 50, WHITE, SIG if i == 2 else INK)
    fig(d, "most common reasons given")

def sc_point(img, d, t):
    t0 = S("point"); tb = cue("point", "but talking")
    words_in(d, t, [("KINDNESS,", t0, 300, 150, INK), ("NOT DECEPTION.", t0 + .3, 450, 110, SIG)] if t < tb - .2 else
             [("TALK", tb - .2, 300, 190, SIG), ("> PERFORM.", tb, 490, 130, INK)])
    picto(d, 340, FLOOR, .9, INK, f=1, pose=TALK(t) if t >= tb else IDLE); picto(d, 620, FLOOR, .9, SIG, f=-1, pose=TALK(t, 2) if t >= tb + .6 else IDLE)
    if t >= tb: speech_box(d, 380, 660, 150, (t - tb) / .3, INK, 1, "· · ·", 34)
    if t >= tb + .6: speech_box(d, 580, 660, 150, (t - tb - .6) / .3, SIG, -1, "· · ·", 34)
    fig(d, "fig. 2 — the real thing beats the show")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "men": sc_men, "why": sc_why, "point": sc_point}
FX = [(0.0, thud(.5), 0), (.4, pop(.18), .3), *EP.cut_fx(), *[(S("study") + .3 + i * .15, tick(.04), (i % 5 - 2) / 3) for i in range(12)],
      (S("result") + .05, thud(.55), 0), (cue("result", "said yes"), pop(.15), .2), (cue("men", "more than"), thud(.4), 0),
      (cue("men", "yes, men"), riser(.3, .05), 0), *[(cue("why", w) - .3, pop(.15), (i - 1) / 2) for i, w in enumerate(("just wasn't", "wanted it to end", "hurt their"))],
      (cue("point", "but talking"), thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
