"""NOT JUST YOU – No. 40: money and happiness (Killingsworth, Kahneman & Mellers 2023). Series: Swiss Dark (edgy)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "old": .5, "study": .8, "result": .5, "except": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "old", "study", "result", "except", "point", "end"]
EP = Episode(TL, 40, "MONEY & HAPPINESS", order=ORDER, dark=True,
             chapters={"hook": "SORRY", "old": "THE OLD STORY", "study": "THE TEAM-UP", "result": "THE CURVE", "except": "THE EXCEPTION", "point": "THE CATCH"},
             sources=("Killingsworth, Kahneman & Mellers (2023),", "PNAS 120(10) · via ScienceDaily"),
             music=dict(bpm=100, root=0, prog="tense", kick="four", gaps=[(E("study") + .05, S("result") + .05)]),
             cover=dict(words=["MONEY", "BUYS", "HAPPINESS."], kicker="Mostly. Sorry."))

OX, OY, GW, GH = X0 + 50, 1060, X1 - X0 - 70, 460
def axes(d):
    d.line([OX, OY, OX + GW, OY], fill=INK, width=4); d.line([OX, OY, OX, OY - GH], fill=INK, width=4)
    for i, lab in enumerate(("$25k", "$75k", "$125k", "$200k+")):
        x = OX + GW * (i + .5) / 4; d.line([x, OY, x, OY + 12], fill=INK, width=3); d.text((x, OY + 20), lab, font=F(MONO, 20), fill=MID, anchor="ma")
    d.text((OX + 10, OY - GH - 10), "happiness", font=F(COND, 26), fill=INK, anchor="ld")
def xpos(k): return OX + GW * (k / 225)     # k = income in thousands
def curve(d, fn, k, col, width=6, dash=False):
    pts = [(xpos(v), OY - GH * fn(v)) for v in range(10, int(10 + 215 * clamp(k)) + 1, 3)]
    if len(pts) < 2: return pts
    if dash:
        for i in range(0, len(pts) - 1, 2): d.line([pts[i], pts[i + 1]], fill=col, width=width)
    else: d.line(pts, fill=col, width=width)
    return pts
def old_fn(v): return .2 + .5 * min(v, 75) / 75
def most_fn(v): return .25 + .55 * math.log(v / 10) / math.log(22.5)
def unhappy_fn(v): return .08 + .22 * math.log(min(v, 100) / 10) / math.log(10)

def coins_stack(d, x, y, n, t):
    for i in range(n): d.ellipse([x - 50, y - i * 18 - 16, x + 50, y - i * 18 + 16], fill=SIG if i % 2 else INK, outline=BG, width=3)

def sc_hook(img, d, t):
    sr = cue("hook", "sorry")
    d.text((X0 - 6, 300), "CAN'T BUY", font=F(BLK, 150), fill=INK if t < sr else RULE)
    d.text((X0 - 6, 450), "HAPPINESS?", font=F(BLK, 150), fill=INK if t < sr else RULE)
    if t >= sr - .1:
        k = ease((t - sr + .1) / .3); d.line([X0, 530, X0 + 840 * k, 470], fill=SIG, width=14)
        words_in(d, t, [("IT CAN.", cue("hook", "it can") - .1, 640, 190, SIG)])
    coins_stack(d, X1 - 120, 1100, int(4 + 8 * clamp(t / 2.5)), t)
    fig(d, "fig. 1 — the saying")

def sc_old(img, d, t):
    t0 = S("old")
    d.text((X0, 300), "THE OLD STORY", font=F(BLK, 110), fill=INK)
    axes(d); pts = curve(d, old_fn, (t - t0 - .3) / 2.5, MID)
    if t >= cue("old", "seventy-five"):
        x = xpos(75); d.line([x, OY, x, OY - GH], fill=SIG, width=3)
        box_label(d, x, OY - GH - 60, "$75k: FLAT?", 30, WHITE, SIG, anchor="ma")
    fig(d, "Kahneman & Deaton, 2010 · schematic")

def sc_study(img, d, t):
    t0 = S("study"); rv = cue("study", "rival")
    d.text((X0, 300), "THE TEAM-UP", font=F(BLK, 120), fill=INK)
    picto(d, 250, 900, .8, INK, f=1, pose=STOP if False else IDLE)
    picto(d, 710, 900, .8, SIG, f=-1, pose=IDLE)
    if t >= rv + .3:
        k = ease((t - rv - .3) / .5); x = lerp(250, 380, k); x2 = lerp(710, 580, k)
        d.line([x + 60, 760, x2 - 60, 760], fill=INK, width=8)
    if t >= cue("study", "app"):
        phone(d, 480, 1030, .8, INK, lit=True); speech_box(d, 520, 900, 300, (t - cue("study", "app")) / .3, SIG, 1, "How do you feel?", 26)
    fig(d, "adversarial collaboration · Killingsworth, Kahneman & Mellers, 2023")

def sc_result(img, d, t):
    t0 = S("result")
    d.text((X0, 300), "IT KEEPS RISING", font=F(BLK, 104), fill=SIG)
    axes(d); curve(d, old_fn, 1, RULE, 4, dash=True)
    pts = curve(d, most_fn, (t - t0) / 2.6, SIG, 8)
    if t >= cue("result", "way past"):
        x = xpos(75); d.line([x, OY, x, OY - GH], fill=MID, width=3)
        note(d, pts[-1][0], pts[-1][1], X1 - 30, OY - GH - 20, "most people", 1, SIG, anchor="ra", size=28)
    d.text((X1, 1146), "schematic", font=F(MED, 22), fill=MID, anchor="ra")

def sc_except(img, d, t):
    t0 = S("except")
    d.text((X0, 300), "EXCEPT…", font=F(BLK, 130), fill=INK)
    axes(d); curve(d, most_fn, 1, SIG, 6)
    pts = curve(d, unhappy_fn, (t - t0) / 2.2, INK, 8)
    if t >= cue("except", "hundred"):
        x = xpos(100); d.line([x, OY, x, OY - GH * .5], fill=INK, width=3)
        box_label(d, x, OY - GH * .5 - 56, "$100k: FLAT", 28, WHITE, INK, anchor="ma")
        note(d, pts[-1][0], pts[-1][1], X1 - 30, OY - 60, "the unhappiest group", 1, INK, anchor="ra", size=26)
    d.text((X1, 1146), "schematic", font=F(MED, 22), fill=MID, anchor="ra")

def sc_point(img, d, t):
    t0 = S("point"); bt = cue("point", "but if")
    words_in(d, t, [("MONEY", t0, 300, 160, INK), ("HELPS.", t0 + .2, 460, 160, SIG)] if t < bt - .1 else [("NOT A", bt - .1, 300, 160, INK), ("FIX-ALL.", bt + .1, 460, 160, SIG)])
    coins_stack(d, 300, 1100, 10, t)
    picto(d, 640, FLOOR, 1.0, INK, f=-1, pose=SHRUG if t >= bt else OPEN)
    fig(d, "fig. 2 — helps a lot, solves not everything")

EP.scenes = {"hook": sc_hook, "old": sc_old, "study": sc_study, "result": sc_result, "except": sc_except, "point": sc_point}
def coin_sfx(amp=.05):
    t = tt_(.3); return amp * (np.sin(2 * np.pi * 2600 * t) + .6 * np.sin(2 * np.pi * 3900 * t)) * np.exp(-t * 18)
FX = [(0.0, thud(.5), 0), *[(.2 + i * .25, coin_sfx(.04), .4) for i in range(8)], (cue("hook", "sorry"), rewind_sfx(.12, .35), 0),
      (cue("hook", "it can"), thud(.55), 0), *EP.cut_fx(), (cue("old", "seventy-five"), pop(.18), 0),
      (cue("study", "rival") + .3, whoosh(.5, .1), 0), (cue("study", "app"), pop(.18), .2), (S("result") + .05, thud(.55), 0),
      (S("result") + .1, riser(2.4, .06), 0), (cue("except", "hundred"), thud(.4), 0), (cue("point", "but if"), thud(.35), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
