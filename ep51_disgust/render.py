"""NOT JUST YOU · AFTER DARK – No. 51: arousal turns disgust down (Borg & de Jong 2012)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .6, "tasks": .8, "result": .5, "why": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "tasks", "result", "why", "point", "end"]
EP = Episode(TL, 51, "THE DISGUST DIAL", order=ORDER, dark=True, series="NOT JUST YOU · AFTER DARK",
             chapters={"hook": "GROSS?", "study": "THREE FILMS", "tasks": "THE GROSS PART", "result": "THE RESULT", "why": "THE DIAL", "point": "AFTERWARDS"},
             sources=("Borg & de Jong (2012),", "PLoS ONE 7(9): e44111"),
             music=dict(bpm=92, root=-2, prog="tense", kick="half", gaps=[(E("tasks") + .05, S("result") + .05)]),
             cover=dict(words=["WHY ISN'T", "IT GROSS?"], kicker="Your brain has a dial."))

def dial(d, cx, cy, r, v, col=SIG, labels=("low", "high")):
    """semicircle gauge, v in 0..1 (disgust)"""
    for i in range(20):
        a0 = 180 + i * 9; c = mix(MID, SIG, i / 19)
        d.arc([cx - r, cy - r, cx + r, cy + r], a0, a0 + 7, fill=c, width=26)
    a = math.radians(180 + 180 * clamp(v)); d.line([cx, cy, cx + math.cos(a) * r * .82, cy + math.sin(a) * r * .82], fill=INK, width=10)
    d.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=INK)
    d.text((cx - r, cy + 20), labels[0], font=F(COND, 28), fill=INK, anchor="ma"); d.text((cx + r, cy + 20), labels[1], font=F(COND, 28), fill=INK, anchor="ma")
    d.text((cx, cy + 40), "DISGUST", font=F(BLK, 34), fill=INK, anchor="ma")

def bug_cup(d, cx, y, s=1.0, t=0.0):
    d.polygon([(cx - 80 * s, y - 200 * s), (cx + 80 * s, y - 200 * s), (cx + 60 * s, y), (cx - 60 * s, y)], fill=INK)
    d.rectangle([cx - 76 * s, y - 190 * s, cx + 76 * s, y - 170 * s], fill=SIG)
    bx, by = cx + 10 * s, y - 205 * s + 3 * math.sin(t * 8)
    d.ellipse([bx - 22 * s, by - 12 * s, bx + 22 * s, by + 12 * s], fill=SIG)
    for j in range(3):
        for side in (-1, 1):
            d.line([bx - 12 * s + j * 12 * s, by, bx - 18 * s + j * 14 * s, by + side * 26 * s], fill=SIG, width=int(4 * s))

def screen(d, x, y, w, h, kind, on=1.0, t=0.0):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=5, fill=mix(BG, INK, .06))
    cx, cy = x + w / 2, y + h / 2
    if kind == 0:
        r = 34 * on; d.ellipse([cx - r, cy - r * .9, cx, cy + r * .1], fill=SIG); d.ellipse([cx, cy - r * .9, cx + r, cy + r * .1], fill=SIG)
        d.polygon([(cx - r * .98, cy - r * .3), (cx + r * .98, cy - r * .3), (cx, cy + r * .95)], fill=SIG)
    elif kind == 1:
        d.polygon([(cx - 70, cy + 40), (cx - 10, cy - 50), (cx + 20, cy), (cx + 40, cy - 30), (cx + 80, cy + 40)], fill=INK)
        d.line([cx - 10, cy - 50, cx - 10, cy - 80], fill=SIG, width=4); d.polygon([(cx - 10, cy - 80), (cx + 20, cy - 72), (cx - 10, cy - 64)], fill=SIG)
    else:
        ox = (t * 40) % 40
        d.rectangle([cx - 80, cy - 30, cx + 80, cy + 20], fill=INK)
        for i in range(3): d.rectangle([cx - 66 + i * 50, cy - 22, cx - 36 + i * 50, cy], fill=BG)
        for i in range(-1, 4):
            a = max(x + 20, cx - 100 + i * 40 + ox); b = min(x + w - 20, cx - 80 + i * 40 + ox)
            if b > a: d.line([a, cy + 40, b, cy + 40], fill=MID, width=4)

def sc_hook(img, d, t):
    d.text((X0 - 6, 300), "WHY ISN'T", font=F(BLK, 150), fill=INK); d.text((X0 - 6, 450), "SEX GROSS?", font=F(BLK, 150), fill=SIG)
    dial(d, 480, 900, 230, .5 + .4 * math.sin(t * 2.2))
    fig(d, "fig. 1 — think about it for a second")

def sc_study(img, d, t):
    t0 = S("study")
    counter(d, X0, 300, t, t0 + .1, .8, 90, "{:.0f} women", 140, SIG)
    for i, (w, lab) in enumerate((("erotica", "erotica"), ("extreme", "extreme sports"), ("train", "train ride"))):
        tk = cue("study", w) - .2; k = ease((t - tk) / .3)
        if k <= 0: continue
        y = 520 + i * 200
        screen(d, X0, y + (1 - k) * 30, 300, 170, i, k, t)
        d.text((X0 + 340, y + 60), lab, font=F(BLK, 50), fill=SIG if i == 0 else INK)
    fig(d, "randomly assigned · 35-minute films")

def sc_tasks(img, d, t):
    t0 = S("tasks"); tb = cue("tasks", "bug"); tc = cue("tasks", "condom")
    d.text((X0, 300), "NOW DO THIS:", font=F(BLK, 120), fill=INK)
    if t >= tb - .3:
        bug_cup(d, 280, 1000, 1.2 * back((t - tb + .3) / .4), t)
        d.text((280, 1030), "drink", font=F(COND, 30), fill=INK, anchor="ma")
    if t >= tc - .3:
        k = back((t - tc + .3) / .4); cx, cy = 680, 860
        d.rounded_rectangle([cx - 70 * k, cy - 70 * k, cx + 70 * k, cy + 70 * k], radius=20, fill=INK)
        d.ellipse([cx - 40 * k, cy - 40 * k, cx + 40 * k, cy + 40 * k], outline=SIG, width=8)
        d.text((cx, 1030), "handle", font=F(COND, 30), fill=INK, anchor="ma")
    if t >= tc + .6: box_label(d, X1, 470, "ALL FAKE, ALL CLEAN", 30, WHITE, INK, anchor="ra")
    fig(d, "16 tasks · plastic bug, unused condom")

def sc_result(img, d, t):
    t0 = S("result")
    d.text((X0, 300), "TURNED ON =", font=F(BLK, 120), fill=INK); d.text((X0, 430), "LESS GROSSED OUT", font=F(BLK, 90), fill=SIG)
    for i, (lab, v, col) in enumerate((("train ride", .78, MID), ("extreme sports", .72, MID), ("erotica", .48, SIG))):
        hbar(d, 600 + i * 150, v, (t - t0 - .2 - i * .3) / .5, col, lab, h=80)
    if t >= cue("result", "more willing"): box_label(d, X1, 1050, "+ MORE WILLING", 32, WHITE, SIG, anchor="ra")
    fig(d, "disgust ratings, sexual tasks · schematic")

def sc_why(img, d, t):
    t0 = S("why"); td = cue("why", "dial down"); to = cue("why", "otherwise")
    d.text((X0, 300), "THE DIAL", font=F(BLK, 150), fill=INK)
    v = lerp(.85, .2, ease((t - td + .3) / .8))
    dial(d, 480, 860, 230, v)
    if t >= to: box_label(d, 480, 560, "OR NOBODY WOULD.", 40, WHITE, SIG, anchor="ma")
    fig(d, "arousal turns disgust down")

def sc_point(img, d, t):
    t0 = S("point"); tu = cue("point", "turning back")
    words_in(d, t, [("WEIRD", t0, 300, 170, INK), ("AFTERWARDS?", t0 + .3, 470, 130, SIG)])
    v = lerp(.2, .75, ease((t - tu + .2) / 1.0))
    dial(d, 360, 980, 170, v)
    picto(d, 760, FLOOR, .8, INK, f=-1, pose=SHRUG if t >= tu else IDLE)
    if t >= tu + .6: box_label(d, X0, 660, "JUST THE DIAL. NORMAL.", 34, WHITE, INK)
    fig(d, "fig. 2 — the dial turns back up")

EP.scenes = {"hook": sc_hook, "study": sc_study, "tasks": sc_tasks, "result": sc_result, "why": sc_why, "point": sc_point}
FX = [(0.0, thud(.5), 0), (.3, whoosh(.6, .06), 0), *EP.cut_fx(),
      *[(cue("study", w) - .2, pop(.15), (i - 1) / 2) for i, w in enumerate(("erotica", "extreme", "train"))],
      (cue("tasks", "bug") - .3, pop(.2), -.3), (cue("tasks", "condom") - .3, pop(.2), .3), (S("result") + .05, thud(.55), 0),
      (cue("result", "more willing"), pop(.15), 0), (cue("why", "dial down") - .3, rewind_sfx(.1, .6), 0), (cue("why", "otherwise"), thud(.35), 0),
      (cue("point", "turning back") - .2, riser(1.0, .05), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
