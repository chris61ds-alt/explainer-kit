"""NOT JUST YOU – No. 107 (Bodies: all normal 1/2): there's no 'normal' vulva – 657 women measured, inner labia 5–100 mm,
outer 12–180 mm (Kreklau et al. 2018, BJOG). Look C+D · claim opener · no anatomical drawings."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
HERE = os.path.dirname(os.path.abspath(__file__))
from bodies import *
TL = Timeline(HERE, lead=.15, gaps={"study": .6, "range": .5, "normal": .6, "inside": .5, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["study", "range", "normal", "inside", "point", "end"]
EP = ThreadEpisode(TL, 107, "ALL NORMAL", order=ORDER, dark=True, label="MEASURED · 657 WOMEN",
                   chapters={k: "" for k in ORDER[:-1]}, sources=("Kreklau et al. (2018), BJOG 125(13) ·", "Lloyd et al. (2005), BJOG 112(5)"),
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

def sc_inside(img, d, t):
    t0, tv = S("inside"), cue("inside", "The vagina") - .1
    d.text((X0, 320), "BY THE WAY:", font=F(BLK, 110), fill=MID)
    words_in(d, t, [("VULVA", t0 + .3, 470, 170, INK)])
    if t >= t0 + .5: d.text((X0 + 6, 650), "= what you see, outside", font=F(COND, 54), fill=INK)
    if t >= tv:
        words_in(d, t, [("VAGINA", tv, 760, 170, INK)])
        d.text((X0 + 6, 940), "= inside", font=F(COND, 54), fill=INK)
    fig(d, "anatomy, words only")

def sc_point(img, d, t):
    t0, tn = S("point"), cue("point", "that's the normal") - .2
    words_in(d, t, [("LOOKS", t0 + .05, 320, 150, MID), ("DIFFERENT?", t0 + .2, 470, 150, MID)] + ([("THAT'S THE", tn, 650, 120, SIG), ("NORMAL PART.", tn + .15, 770, 120, SIG)] if t >= tn else []))
    fig(d, "fig. — Bodies: all normal")

EP.cuts = {"normal": "stay"}
EP.scenes = {"study": sc_study, "range": sc_range, "normal": sc_normal, "inside": sc_inside, "point": sc_point}
FX = [(0.0, thud(.5), 0), *EP.cut_fx(), (S("study") + .1, riser(.8, .04), 0), (cue("study", "aged fifteen") - .1, pop(.13), .2),
      (cue("range", "From one millimeter") - .1, whoosh(.8, .04), 0), (cue("range", "From one millimeter") + .8, thud(.45), .3), (cue("range", "Their length") - .1, pop(.13), -.2),
      (S("normal") + .05, thud(.55), 0), *[(S("normal") + .1 + i * .045, tick(.025), (i % 5 - 2) / 3) for i in range(0, 45, 3)],
      (S("inside") + .3, pop(.13), -.2), (cue("inside", "The vagina") - .1, pop(.13), .2),
      (S("point") + .1, pop(.12), 0), (cue("point", "that's the normal") - .2, thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
