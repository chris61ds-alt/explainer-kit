"""NOT JUST YOU – No. 93 (Wedding Math 1/3): pricier weddings, higher divorce risk (Francis-Tan & Mialon 2015). Look C+D, dark."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from thread import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"study": .6, "women": .5, "men": .5, "why": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["study", "women", "men", "why", "point", "end"]               # opener: statement ("claim" beat, toolkit)
EP = ThreadEpisode(TL, 93, "WEDDING COST", order=ORDER, dark=True, label="WEDDING MATH 1/3 · SURVEY",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Francis-Tan & Mialon (2015), Economic Inquiry", "survey of 3,000+ ever-married US adults · correlation"),
                   music=dict(bpm=96, root=-3, prog="tense", kick="four", audio="v5", gaps=[(E("study") + .05, S("women") + .05)]),
                   cover=dict(words=["BIG WEDDING,", "BIGGER", "DIVORCE RISK."], kicker="Wedding Math, part 1 of 3."))

FIELD = (X0 + 14, 760, X1, 1110)
def dot_xy(i, box=FIELD, cell=30):
    x0, y0, x1, y1 = box; cols = len(range(int(x0), int(x1), cell)); r, c = divmod(i, cols)
    return x0 + c * cell, y0 + r * cell

def sc_claim(img, d, t):                                # toolkit statement opener + "Seriously!" underlines BIGGER
    EP.claim_scene(img, d, t)
    ts = cue("claim", "Seriously") - .1
    if t >= ts:
        lines = TL.screen["claim"]
        size = int(min(170, 600 / (len(lines) * 1.05), *(840 / max(1, d.textlength(l, font=F(BLK, 100))) * 100 for l in lines)))
        y = 330 + int(size * 1.05) + int(size * .98); w = d.textlength("BIGGER", font=F(BLK, size))
        if LOOK == "v6": scribble_under(d, X0 - 12, X0 + w + 14, y + 4, (t - ts) / .35, col=INK, w=11)
        else: d.line([X0 - 8, y, X0 - 8 + (w + 10) * ease((t - ts) / .25), y], fill=INK, width=12)

def sc_study(img, d, t):
    t0, th, tl = S("study"), cue("study", "How much") - .1, cue("study", "did it last") - .1
    counter(d, X0, 320, t, t0 + .1, .8, 3000, "{:,.0f}+", 230, INK)
    d.text((X0 + 6, 570), "Americans who'd been married · two economists", font=F(COND, 40), fill=INK)
    if t >= th: d.text((X0 + 6 - (1 - ease((t - th) / .25)) * 40, 630), "1. what did the wedding cost?", font=F(COND, 40), fill=mix(BG, INK, ease((t - th) / .25)))
    if t >= tl: d.text((X0 + 6 - (1 - ease((t - tl) / .25)) * 40, 685), "2. are you still married?", font=F(COND, 40), fill=mix(BG, INK, ease((t - tl) / .25)))
    dot_field(d, FIELD, t, cell=30, col=MID, hit={47} | ({12, 33, 77, 101, 140, 166, 190, 212} if t >= tl else set()), hitcol=INK)
    if LOOK == "v6" and t >= tl:                          # circle one person: "you"
        _x, _y = dot_xy(47); scribble_circle(d, (_x - 14, _y - 14, _x + 14, _y + 14), (t - tl) / .45, col=INK, w=6, seed=4, pad=10)
    fig(d, "online survey · Francis-Tan & Mialon, Emory University")

def xbars(d, t, rows, vmax, y0=600, step=270):
    for j, (lab, v, col, tk) in enumerate(rows):
        if tk is None or t < tk - .01: continue
        k = ease((t - tk) / .6); y = y0 + j * step
        d.text((X0, y), lab, font=F(BLK, 54), fill=col)
        w = 640 * v / vmax * k
        d.rectangle([X0, y + 75, X0 + max(6, w), y + 215], fill=col)
        d.text((X0 + max(6, w) + 16, y + 145), f"{v * k:.1f} ×", font=F(BLK, 72), fill=col, anchor="lm")

def head(d, who):
    d.text((X0, 320), who, font=F(BLK, 150), fill=INK)
    d.text((X0 + 4, 485), "divorce risk, by wedding cost", font=F(COND, 46), fill=MID)

def sc_women(img, d, t):
    head(d, "WOMEN")
    xbars(d, t, [("$5–10K", 1.0, MID, cue("women", "Compared") - .1), ("OVER $20K", 1.6, SIG, cue("women", "twenty thousand") - .1)], 1.6)
    tr = cue("women", "One point six") - .1
    if t >= tr: box_label(d, X1, 600, "1.6 × RISK", 52, WHITE, SIG, font=BLK, anchor="ra")
    if LOOK == "v6" and t >= tr: scribble_circle(d, (X0 + 652, 972, X0 + 808, 1058), (t - tr) / .45, seed=5)
    fig(d, "relative divorce risk · women · vs. $5,000–10,000")

def sc_men(img, d, t):
    head(d, "MEN")
    xbars(d, t, [("$5–10K", 1.0, MID, S("men") - 1), ("UNDER $1K", .5, SIG, cue("men", "under a thousand") - .1)], 1.6)
    th = cue("men", "about half") - .1
    if t >= th: box_label(d, X1, 600, "ABOUT HALF", 52, WHITE, SIG, font=BLK, anchor="ra")
    if LOOK == "v6" and t >= th: scribble_circle(d, (X0 + 212, 972, X0 + 368, 1058), (t - th) / .45, seed=6)
    fig(d, "relative divorce risk · men · hazard 0.49")

def sc_why(img, d, t):
    t0, tn, td, tm = S("why"), cue("why", "Nobody knows") - .1, cue("why", "debt") - .1, cue("why", "money stress") - .1
    d.text((X0, 320), "WHY?", font=F(BLK, 170), fill=INK)
    if t >= tn: d.text((X0 + 4, 510), "nobody knows for sure.", font=F(COND, 50), fill=MID)
    if t >= td:
        k = ease((t - td) / .25); d.text((X0 - (1 - k) * 50, 590), "DEBT?", font=F(BLK, 140), fill=mix(BG, INK, k))
        n = min(9, int((t - td) / .12) + 1)
        for i in range(n):                                # a growing stack of bills (schematic)
            y = 1090 - i * 34; x = X1 - 340 + (i % 3) * 8
            d.rectangle([x, y, x + 300, y + 26], fill=MID if i % 2 else INK)
            d.text((x + 150, y + 13), "$", font=F(BLK, 22), fill=BG, anchor="mm")
    if t >= tm:
        k = ease((t - tm) / .25)
        d.text((X0 + 4, 800), "money stress", font=F(COND, 50), fill=mix(BG, INK, k))
        d.text((X0 + 4, 860), "= relationship", font=F(COND, 50), fill=mix(BG, INK, k))
        d.text((X0 + 4, 920), "   stress", font=F(COND, 50), fill=mix(BG, INK, k))
    if LOOK == "v6" and t >= td + .35: scribble_arrow(d, (X0 + 420, 700), (X1 - 360, 1000), (t - td - .35) / .5, bend=-.3)
    fig(d, "the study shows a link, not the cause")

def sc_point(img, d, t):
    t0, tb = S("point"), cue("point", "But the bill") - .2
    words_in(d, t, [("THE PARTY", t0 + .1, 320, 130, MID), ("ENDS.", t0 + .25, 445, 130, MID)] +
             ([("THE BILL", tb, 600, 130, SIG), ("DOESN'T.", tb + .15, 725, 130, SIG)] if t >= tb else []))
    k = clamp((t - t0 - .2) / 1.4); x0, x1, y0 = X1 - 330, X1 - 40, 880
    if k > 0:                                             # a receipt printing out
        y1 = y0 + 230 * k; d.rectangle([x0, y0, x1, y1], fill=INK)
        for i in range(int(5 * k)): d.rectangle([x0 + 24, y0 + 24 + i * 34, x1 - 24 - (i % 2) * 80, y0 + 36 + i * 34], fill=BG)
        if t >= tb: d.rectangle([x0 + 24, y1 - 34, x1 - 24, y1 - 16], fill=SIG)
    if LOOK == "v6" and t >= tb + .35:
        scribble_under(d, X0 - 8, X0 + d.textlength("DOESN'T.", font=F(BLK, 130)), 868, (t - tb - .35) / .35, seed=7)
    fig(d, "fig. — Wedding Math, part 1 of 3")

# magic move: one married person in the survey grows into the "over $20K" bar
_dx, _dy = dot_xy(47)
EP.carry = {"women": [((_dx - 8, _dy - 8, _dx + 8, _dy + 8), (X0, 945, X0 + 132, 1085))]}
EP.cuts = {"men": "stay"}
EP.focus = {"claim": (480, 520), "study": (X0 + 250, 420), "women": (X0 + 720, 1015), "why": (X0 + 200, 650), "point": (480, 700)}

EP.scenes = {"claim": sc_claim, "study": sc_study, "women": sc_women, "men": sc_men, "why": sc_why, "point": sc_point}
FX = [(0.0, thud(.5), 0), (cue("claim", "Seriously") - .1, pop(.15), 0), *EP.cut_fx(), (S("study") + .1, riser(.8, .04), 0),
      (cue("study", "How much") - .1, pop(.12), -.2), (cue("study", "did it last") - .1, pop(.12), .2),
      (cue("women", "twenty thousand") - .1, thud(.5), 0), (cue("women", "One point six") - .1, pop(.15), .3), (cue("women", "Compared") - .1, pop(.12), -.3),
      (cue("men", "under a thousand") - .1, thud(.5), 0), (cue("men", "about half") - .1, pop(.15), .3),
      (S("why") + .05, thud(.4), 0), (cue("why", "Nobody knows") - .1, tick(.06), 0), (cue("why", "debt") - .1, thud(.45), 0),
      *[(cue("why", "debt") - .1 + i * .12, tick(.03), (i % 5 - 2) / 3) for i in range(9)], (cue("why", "money stress") - .1, pop(.13), 0),
      (S("point") + .1, pop(.12), 0), (cue("point", "But the bill") - .2, thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
