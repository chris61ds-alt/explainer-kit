"""NOT JUST YOU – No. 107 (Bodies: all normal 1/2): there's no 'normal' vulva – 657 women measured, inner labia 5–100 mm,
outer 12–180 mm (Kreklau et al. 2018, BJOG). Since 06.11.2026 a 'what helps' ending: looking at real vulvas improved
genital self-image, still 2 weeks later (Laan et al. 2017, small study). Look C+D · claim opener · no anatomical drawings."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
HERE = os.path.dirname(os.path.abspath(__file__))
from bodies import *
TL = Timeline(HERE, lead=.15, gaps={"study": .6, "range": .5, "normal": .6, "feel": .5, "helps": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["study", "range", "normal", "feel", "helps", "point", "end"]
EP = ThreadEpisode(TL, 107, "ALL NORMAL", order=ORDER, dark=True, label="MEASURED · 657 WOMEN",
                   chapters={k: "" for k in ORDER[:-1]}, sources=("Kreklau et al. (2018), BJOG 125(13) · Lloyd et al. (2005) ·", "Laan et al. (2017), J. Psychosom. Obstet. Gynecol. 38(4)"),
                   music=dict(bpm=100, root=2, prog="major", kick="four", audio="v5", gaps=[(E("study") + .05, S("range") + .05)]),
                   cover=dict(words=["THERE'S NO", "\"NORMAL\"", "VULVA."], kicker="Bodies: all normal, part 1."))

def sc_study(img, d, t):
    t0, ta = S("study"), cue("study", "aged fifteen") - .1
    counter(d, X0, 320, t, t0 + .1, .8, 657, "{:.0f}", 230, INK); d.text((X0 + 6, 565), "women, measured by gynecologists", font=F(COND, 46), fill=INK)
    if t >= ta: box_label(d, X0 + 4, 640, "AGED 15 TO 84", 44, WHITE, INK, font=BLK)
    dot_field(d, (X0 + 14, 760, X1, 1110), t, cell=30, col=MID, hit={45})
    fig(d, "Lucerne, Switzerland")

def lens(d, cx, cy, w, h, col, width=6, k=1.0):
    """almond / lens outline (two arcs) – purely geometric schematic"""
    if k <= 0: return
    hh = h * ease(clamp(k)); r = (w * w / 4 + hh * hh / 4) / w          # circle through the tips and the widest point
    for sx in (-1, 1):
        ccx = cx - sx * (r - w / 2); a = math.degrees(math.asin(min(1, hh / 2 / r)))
        d.arc([ccx - r, cy - r, ccx + r, cy + r], (180 if sx < 0 else 0) - a if sx > 0 else 180 - a, (a if sx > 0 else 180 + a), fill=col, width=width)

def varrow(d, x, y0, y1, col, k=1.0, label=None):
    if k <= 0: return
    y1 = y0 + (y1 - y0) * ease(clamp(k)); d.line([x, y0, x, y1], fill=col, width=5)
    for yy, sg in ((y0, 1), (y1, -1)): d.polygon([(x - 12, yy + sg * 18), (x + 12, yy + sg * 18), (x, yy)], fill=col)
    if label and k >= 1: d.text((x + 22, (y0 + y1) / 2), label, font=F(MONO, 26), fill=col, anchor="lm")

DIA = (300, 540)                                                      # schematic centre
def harrow(d, x0, x1, y, col, k=1.0):
    if k <= 0: return
    x1 = x0 + (x1 - x0) * ease(clamp(k)); d.line([x0, y, x1, y], fill=col, width=5)
    d.polygon([(x1, y), (x1 - 18, y - 12), (x1 - 18, y + 12)], fill=col)

def schematic(d, t, t_w, t_l):
    cx, cy = DIA
    lens(d, cx, cy, 300, 380, MID, 6, 1)                               # outer lips (context)
    lens(d, cx, cy, 120, 300, INK, 7, (t - S("range")) / .5)           # inner lips
    if t >= t_w: harrow(d, cx + 60, cx + 230, cy, SIG, (t - t_w) / .4)                  # how far they stick out
    if t >= t_l: varrow(d, cx - 190, cy - 150, cy + 150, INK, (t - t_l) / .5)          # length, front to back
    d.text((cx - 175, cy - 230), "SCHEMATIC", font=F(MONO, 22), fill=MID)

def sc_range(img, d, t):
    t0, tw, tl = S("range"), cue("range", "From one millimeter") - .1, cue("range", "Their length") - .1
    schematic(d, t, tw, tl)
    d.text((X1, 330), "INNER LIPS", font=F(BLK, 74), fill=INK, anchor="ra"); d.text((X1, 415), "labia minora", font=F(MONO, 28), fill=MID, anchor="ra")
    d.text((X0, 820), "HOW FAR THEY STICK OUT", font=F(BLK, 46), fill=SIG)
    ruler(d, X0, X1, 940, 0, 70, 1, 61, (t - tw) / .9, ticks=7, label_every=1)
    if t >= tw + .9: box_label(d, X1, 560, "1 TO 61 MM", 48, WHITE, SIG, font=BLK, anchor="ra")
    if t >= tl:
        d.text((X0, 1010), "LENGTH (FRONT TO BACK)", font=F(BLK, 40), fill=INK); d.text((X1, 1016), "5 to 100 mm", font=F(MONO, 30), fill=INK, anchor="ra")
    fig(d, "schematic · ranges across 657 women")

def sc_normal(img, d, t):
    t0 = S("normal"); words_in(d, t, [("ALL OF IT.", t0 + .05, 320, 170, INK)])
    blob_field(d, (X0, 560, X1, 1110), t, t0 + .1, n=45, col=INK, hi=set(range(45)), hicol=SIG)
    fig(d, "every shape different · schematic")

def sc_feel(img, d, t):
    t0, tl = S("feel"), cue("feel", "love it") - .15
    words_in(d, t, [("NORMAL", t0 + .05, 320, 170, MID), ("DOESN'T MEAN", t0 + .2, 500, 120, INK)] + ([("YOU LOVE IT.", tl, 630, 120, INK)] if t >= tl else []))
    if t >= tl: heart(d, 480, 930, 110 * back(clamp((t - tl) / .35)), MID)
    fig(d, "fair enough")

def curve(d, x0, y0, w, h, pts, col, k, width=10):
    """before → after → 2 weeks, direction only (no scale in the source summary)"""
    xs = [x0, x0 + w / 2, x0 + w]; P = [(xs[i], y0 - pts[i] * h) for i in range(3)]
    n = k * 2
    for i in range(2):
        if n <= i: break
        f = min(1, n - i); a, b = P[i], P[i + 1]; e = (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)
        d.line([a, e], fill=col, width=width)
    for i in range(3):
        if n >= i: d.ellipse([P[i][0] - 16, P[i][1] - 16, P[i][0] + 16, P[i][1] + 16], fill=col)
    return P

def sc_helps(img, d, t):
    t0, ta, t2, tn = S("helps"), cue("helps", "Afterwards") - .1, cue("helps", "Two weeks") - .1, cue("helps", "Neutral photos") - .1
    d.text((X0, 320), "HOW THEY FELT", font=F(BLK, 100), fill=INK); d.text((X0 + 4, 430), "about their own", font=F(COND, 50), fill=MID)
    x0, y0, w, h = X0 + 40, 900, 760, 260
    d.line([x0 - 20, y0 + 30, x0 + w + 20, y0 + 30], fill=RULE, width=4)
    for i, lab in enumerate(("BEFORE", "AFTER", "2 WEEKS")): d.text((x0 + i * w / 2, y0 + 50), lab, font=F(MONO, 26), fill=MID, anchor="ma")
    kv = 0 if t < ta else (.5 * clamp((t - ta) / .5) + (.5 * clamp((t - t2) / .5) if t >= t2 else 0))
    P = curve(d, x0, y0, w, h, (.2, .8, .8), SIG, kv)
    if t >= ta: d.text((P[1][0], P[1][1] - 70), "REAL VULVA PHOTOS", font=F(BLK, 40), fill=SIG, anchor="ma")
    if t >= tn:
        curve(d, x0, y0, w, h, (.2, .2, .2), MID, clamp((t - tn) / .6), width=8)
        d.text((x0 + w, y0 - .2 * h + 40), "NEUTRAL PHOTOS", font=F(BLK, 34), fill=MID, anchor="ra")
    fig(d, "small study · 43 women · direction only, schematic")

def sc_point(img, d, t):
    t0, td = S("point"), cue("point", "talk to a doctor") - .2
    words_in(d, t, [("LOOK AT", t0 + .05, 320, 140, SIG), ("REAL ONES.", t0 + .2, 460, 140, SIG)])
    blob_field(d, (X0, 640, X1, 960), t, t0 + .1, n=24, col=INK, hi=set(), hicol=SIG)
    if t >= td: words_in(d, t, [("STILL HEAVY? TALK TO A DOCTOR.", td, 990, 58, INK)])
    fig(d, "fig. — Bodies: all normal")

EP.cuts = {"normal": "stay"}
EP.scenes = {"study": sc_study, "range": sc_range, "normal": sc_normal, "feel": sc_feel, "helps": sc_helps, "point": sc_point}
EP.bg = {"helps": "light"}
FX = [(0.0, thud(.5), 0), *EP.cut_fx(), (S("study") + .1, riser(.8, .04), 0), (cue("study", "aged fifteen") - .1, pop(.13), .2),
      (cue("range", "From one millimeter") - .1, whoosh(.8, .04), 0), (cue("range", "From one millimeter") + .8, thud(.45), .3), (cue("range", "Their length") - .1, pop(.13), -.2),
      (S("normal") + .05, thud(.55), 0), *[(S("normal") + .1 + i * .045, tick(.025), (i % 5 - 2) / 3) for i in range(0, 45, 3)],
      (S("feel") + .1, thud(.4), 0), (cue("feel", "love it") - .15, pop(.13), 0),
      (S("helps") + .1, riser(.8, .04), 0), (cue("helps", "Afterwards") - .1, pop(.14), -.2), (cue("helps", "Two weeks") - .1, pop(.14), .2), (cue("helps", "Neutral photos") - .1, tick(.06), .3),
      (S("point") + .1, thud(.45), 0), *[(S("point") + .1 + i * .06, tick(.025), (i % 5 - 2) / 3) for i in range(0, 24, 3)], (cue("point", "talk to a doctor") - .2, pop(.14), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
