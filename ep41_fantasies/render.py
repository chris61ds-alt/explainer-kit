"""NOT JUST YOU · AFTER DARK – No. 41: sexual fantasies are mostly common (Joyal et al. 2015)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .8, "result": .5, "power": .5, "quote": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "power", "quote", "point", "end"]
EP = Episode(TL, 41, "FANTASIES", order=ORDER, dark=True, series="NOT JUST YOU · AFTER DARK",
             chapters={"hook": "WEIRD?", "study": "THE SURVEY", "result": "RARE?", "power": "POWER", "quote": "THE QUOTE", "point": "JUST A THOUGHT"},
             sources=("Joyal, Cossette & Lapierre (2015),", "Journal of Sexual Medicine 12(2)"),
             music=dict(bpm=84, root=-3, prog="dream", kick="half", gaps=[(E("study") + .05, S("result") + .05)]),
             cover=dict(words=["WEIRD", "FANTASY?"], kicker="Probably not."))

def padlock(d, cx, cy, s=1.0, open_k=0.0, col=SIG):
    d.rectangle([cx - 50 * s, cy - 10 * s, cx + 50 * s, cy + 70 * s], fill=col)
    lift = 30 * s * ease(open_k)
    d.arc([cx - 34 * s, cy - 70 * s - lift, cx + 34 * s, cy + 10 * s - lift], 180, 360, fill=col, width=int(12 * s))
    d.line([cx - 34 * s, cy - 30 * s - lift, cx - 34 * s, cy - 6 * s - (lift if open_k < .5 else lift)], fill=col, width=int(12 * s))
    d.line([cx + 34 * s, cy - 30 * s - lift, cx + 34 * s, cy - 6 * s], fill=col, width=int(12 * s))
    d.ellipse([cx - 9 * s, cy + 18 * s, cx + 9 * s, cy + 36 * s], fill=BG)

def sc_hook(img, d, t):
    d.text((X0 - 6, 300), "WEIRD?", font=F(BLK, 220), fill=INK)
    h = picto(d, 330, FLOOR, .75, INK, f=1, pose=WORRY)
    box = think_box(d, h, 240, 120, (t - .3) / .4, "", INK, 1)
    if box: padlock(d, (box[0] + box[2]) / 2, (box[1] + box[3]) / 2 - 10, .7)
    fig(d, "fig. 1 — the thought you keep to yourself")

def sc_study(img, d, t):
    t0 = S("study")
    counter(d, X0, 300, t, t0 + .1, 1.0, 1517, "{:,.0f}", 190, SIG)
    d.text((X0 + 6, 520), "adults rated dozens of fantasies", font=F(COND, 36), fill=INK)
    k = clamp((t - t0 - .3) / 2.0)
    for i in range(int(300 * k)):
        r, c = divmod(i, 25); x = X0 + 20 + c * 34; y = 610 + r * 40
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=INK if i % 7 else SIG)
    fig(d, "Quebec, anonymous survey · Joyal, Cossette & Lapierre, 2015")

def sc_result(img, d, t):
    t0 = S("result")
    d.text((X0, 300), "RARE?", font=F(BLK, 160), fill=INK)
    d.text((X0, 500), "how many fantasies were…", font=F(COND, 34), fill=INK)
    hbar(d, 580, .08, (t - cue("result", "rare") + .2) / .5, MID, "statistically rare", h=90)
    hbar(d, 760, .8, (t - cue("result", "shared") + .2) / .5, SIG, "shared by many people", h=90)
    d.text((X1, 1146), "schematic", font=F(MED, 22), fill=MID, anchor="ra")

def dial(d, cx, cy, r, v, col):
    d.arc([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=INK, width=10)
    a = math.radians(180 + 180 * v); d.line([cx, cy, cx + math.cos(a) * r * .9, cy + math.sin(a) * r * .9], fill=col, width=10)
    d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=col)

def sc_power(img, d, t):
    t0 = S("power")
    d.text((X0, 300), "CONTROL", font=F(BLK, 170), fill=SIG)
    v = .5 + .45 * math.sin(t * 1.6)
    dial(d, 480, 780, 200, v, SIG)
    d.text((280, 820), "give it up", font=F(COND, 30), fill=INK, anchor="ma"); d.text((680, 820), "take it", font=F(COND, 30), fill=INK, anchor="ma")
    if t >= cue("power", "especially"): box_label(d, 480, 920, "ESPECIALLY COMMON", 32, WHITE, SIG, anchor="ma")
    fig(d, "themes of power and control")

def sc_quote(img, d, t):
    t0 = S("quote")
    d.text((X0 - 10, 300), "“", font=F(BLK, 280), fill=SIG)
    lines = [("There are a lot more", cue("quote", "there are")), ("common fantasies", cue("quote", "common")), ("than unusual ones.", cue("quote", "unusual") - .3)]
    for i, (l, tk) in enumerate(lines):
        k = ease((t - tk) / .3)
        if k > 0: d.text((X0, 580 + i * 100 + (1 - k) * 30), l, font=F(BLK, 74), fill=mix(BG, SIG if i == 1 else INK, k))
    box_label(d, X0, 960, "CHRISTIAN JOYAL · LEAD AUTHOR", 26, WHITE, INK)

def sc_point(img, d, t):
    t0 = S("point"); tp = cue("point", "a fantasy")
    words_in(d, t, [("GOOD", t0, 300, 170, INK), ("COMPANY.", t0 + .2, 470, 170, SIG)] if t < tp - .2 else [("A THOUGHT,", tp - .2, 300, 140, INK), ("NOT A PLAN.", tp, 450, 140, SIG)])
    h = picto(d, 330, FLOOR, .75, INK, f=1, pose=OPEN)
    box = think_box(d, h, 240, 120, 1, "", INK, 1)
    if box: padlock(d, (box[0] + box[2]) / 2, (box[1] + box[3]) / 2 - 10, .7, open_k=(t - t0 - .4) / .6)
    for i, x in enumerate((640, 760, 860)): picto(d, x, FLOOR, .55, MID, f=-1, pose=IDLE)
    fig(d, "fig. 2 — you're not the only one")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "power": sc_power, "quote": sc_quote, "point": sc_point}
FX = [(0.0, thud(.5), 0), (.3, pop(.15), .2), *EP.cut_fx(), *[(S("study") + .3 + i * .15, tick(.04), (i % 5 - 2) / 3) for i in range(12)],
      (S("result") + .05, thud(.5), 0), (cue("result", "shared"), riser(.4, .06), .2), (cue("power", "especially"), thud(.4), 0),
      (cue("quote", "there are"), pop(.15), 0), (S("point") + .4, rewind_sfx(.08, .3), 0), (cue("point", "a fantasy"), thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
