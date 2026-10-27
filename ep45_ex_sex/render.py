"""NOT JUST YOU · AFTER DARK – No. 45: sex with an ex doesn't hinder breakup recovery (Spielmann, Joel & Impett 2019)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .8, "result": .5, "who": .5, "mood": .5, "quote": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "who", "mood", "quote", "point", "end"]
EP = Episode(TL, 45, "THE EX", order=ORDER, dark=True, series="NOT JUST YOU · AFTER DARK",
             chapters={"hook": "MISTAKE?", "study": "THE DIARIES", "result": "RECOVERY", "who": "WHO", "mood": "THE MOOD", "quote": "THE QUOTE", "point": "NO SHAME"},
             sources=("Spielmann, Joel & Impett (2019),", "Archives of Sexual Behavior 48 · via ScienceDaily"),
             music=dict(bpm=86, root=-4, prog="tense", kick="half", gaps=[(E("study") + .05, S("result") + .05)]),
             cover=dict(words=["SLEPT WITH", "YOUR EX?"], kicker="It might not set you back."))

def heart(d, cx, cy, r, col=SIG, split=0.0):
    """heart; split > 0 pulls the halves apart along a zig-zag"""
    for side in (-1, 1):
        ox = cx + side * split
        d.ellipse([min(ox, ox + side * r), cy - r * .9, max(ox, ox + side * r), cy + r * .1], fill=col)
        d.polygon([(ox + side * r * .98, cy - r * .3), (ox, cy - r * .3), (ox, cy + r * .95)], fill=col)
    if split > 1:
        zz = [(cx, cy - r * .5), (cx - r * .15, cy - r * .1), (cx + r * .12, cy + r * .3), (cx, cy + r)]
        d.line(zz, fill=BG, width=int(4 + split * .6))

def sc_hook(img, d, t):
    d.text((X0 - 6, 300), "YOUR EX?", font=F(BLK, 190), fill=INK)
    k = ease((t - .5) / .8)
    picto(d, lerp(260, 380, k), FLOOR, .9, INK, f=1, pose=IDLE); picto(d, lerp(700, 580, k), FLOOR, .9, SIG, f=-1, pose=IDLE)
    heart(d, 480, 760, 50, SIG, split=26 * (1 - k))
    if t >= cue("hook", "might not"): box_label(d, 480, 560, "A MISTAKE?", 40, WHITE, INK, anchor="ma")
    fig(d, "fig. 1 — the classic bad idea")

def sc_study(img, d, t):
    t0 = S("study"); k = clamp((t - t0 - .2) / 2.4)
    counter(d, X0, 300, t, t0 + .1, 1.0, 485, "{:.0f}", 220, SIG)
    d.text((X0 + 6, 540), "people after a recent breakup", font=F(COND, 36), fill=INK)
    for i in range(28):
        r, c = divmod(i, 7); x = X0 + 10 + c * 120; y = 630 + r * 110
        on = i < 28 * k
        d.rectangle([x, y, x + 100, y + 90], outline=INK, width=3, fill=SIG if on and i % 5 == 2 else None)
        d.text((x + 8, y + 6), f"{i + 1}", font=F(MONO, 18), fill=MID)
        if on: d.line([x + 25, y + 55, x + 45, y + 72, x + 78, y + 32], fill=INK if i % 5 != 2 else WHITE, width=5)
    fig(d, "daily diaries + follow-up after 2 months")

OX, OY, GW, GH = X0 + 50, 1060, X1 - X0 - 70, 400
def axes(d):
    d.line([OX, OY, OX + GW, OY], fill=INK, width=4); d.line([OX, OY, OX, OY - GH], fill=INK, width=4)
    d.text((OX + 10, OY - GH - 10), "getting over it", font=F(COND, 26), fill=INK, anchor="ld")
    for i, lab in enumerate(("breakup", "day 10", "day 20", "2 months")):
        x = OX + GW * i / 3; d.text((x, OY + 18), lab, font=F(MONO, 18), fill=MID, anchor="ma")

def sc_result(img, d, t):
    t0 = S("result"); k = clamp((t - t0) / 2.4)
    d.text((X0, 300), "NO SETBACK", font=F(BLK, 130), fill=SIG)
    axes(d)
    n = int(2 + 58 * k)
    p1 = [(OX + GW * i / 59, OY - GH * (.15 + .7 * (1 - math.exp(-i / 18)))) for i in range(n)]
    p2 = [(x, y - 8) for x, y in p1]
    if len(p1) > 1:
        d.line(p1, fill=MID, width=6); d.line(p2, fill=SIG, width=6)
    if t >= cue("result", "not day"):
        legend(d, [(SIG, "pursued sex with the ex"), (MID, "didn't")], y=520)
    if t >= cue("result", "two months"): box_label(d, X1, OY - GH - 60, "SAME CURVE", 30, WHITE, INK, anchor="ra")
    d.text((X1, 1146), "schematic", font=F(MED, 22), fill=MID, anchor="ra")

def sc_who(img, d, t):
    t0 = S("who")
    d.text((X0, 300), "WHO?", font=F(BLK, 150), fill=INK)
    h = picto(d, 330, FLOOR, .8, INK, f=1, pose=WORRY)
    box = think_box(d, h, 220, 130, (t - t0 - .2) / .4, "", INK, 1)
    if box: heart(d, (box[0] + box[2]) / 2, (box[1] + box[3]) / 2, 34, SIG)
    if t >= cue("who", "still attached"): box_label(d, X1, 560, "STILL ATTACHED", 34, WHITE, SIG, anchor="ra")
    picto(d, 760, FLOOR, .7, MID, f=-1, pose=IDLE)
    fig(d, "most eager: those who hadn't let go")

def sc_mood(img, d, t):
    t0 = S("mood")
    d.text((X0, 300), "DISTRESS?", font=F(BLK, 150), fill=INK)
    hbar(d, 560, .45, (t - t0 - .1) / .5, MID, "attached, no ex sex", h=90)
    hbar(d, 740, .45, (t - t0 - .5) / .5, SIG, "attached, with ex sex", h=90)
    if t >= cue("mood", "more distress"): box_label(d, X0 + 840 * .45 + 40, 770, "NO EXTRA HARM", 40, WHITE, INK)
    d.text((X1, 1146), "schematic", font=F(MED, 22), fill=MID, anchor="ra")

def sc_quote(img, d, t):
    d.text((X0 - 10, 300), "“", font=F(BLK, 280), fill=SIG)
    lines = [("The hand-wringing", cue("quote", "hand-wringing") - .2), ("may not be", cue("quote", "may not")), ("warranted.", cue("quote", "warranted") - .2)]
    for i, (l, tk) in enumerate(lines):
        k = ease((t - tk) / .3)
        if k > 0: d.text((X0, 580 + i * 100 + (1 - k) * 30), l, font=F(BLK, 80), fill=mix(BG, SIG if i == 2 else INK, k))
    box_label(d, X0, 960, "STEPHANIE SPIELMANN · LEAD AUTHOR", 26, WHITE, INK)

def sc_point(img, d, t):
    t0 = S("point"); tj = cue("point", "just be")
    words_in(d, t, [("NO", t0, 300, 190, INK), ("SHAME.", t0 + .2, 490, 190, SIG)] if t < tj - .2 else [("KNOW", tj - .2, 300, 170, INK), ("YOUR WHY.", tj, 470, 150, SIG)])
    picto(d, 480, FLOOR, 1.0, INK, f=1, pose=OPEN if t < tj else SHRUG)
    fig(d, "fig. 2 — an honest look beats a rule")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "who": sc_who, "mood": sc_mood, "quote": sc_quote, "point": sc_point}
FX = [(0.0, thud(.5), 0), (.5, whoosh(.8, .08), 0), (cue("hook", "might not"), pop(.15), 0), *EP.cut_fx(),
      *[(S("study") + .2 + i * .085, tick(.04), (i % 5 - 2) / 3) for i in range(28)],
      (S("result") + .05, thud(.55), 0), (cue("result", "two months"), pop(.15), .2), (cue("who", "still attached"), thud(.35), 0),
      (cue("mood", "more distress"), pop(.15), 0), (cue("quote", "hand-wringing") - .2, pop(.15), 0), (cue("point", "just be"), thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
