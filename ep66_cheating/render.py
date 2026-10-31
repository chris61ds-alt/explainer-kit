"""NOT JUST YOU · AFTER DARK – No. 66: who cheats (GSS via Institute for Family Studies, Wang 2018). Look C+D, dark."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from thread import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .8, "result": .5, "young": .5, "old": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "young", "old", "point", "end"]
EP = ThreadEpisode(TL, 66, "WHO CHEATS", order=ORDER, dark=True, series="NOT JUST YOU · AFTER DARK",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("General Social Survey, analysis: Wang (2018),", "Institute for Family Studies"),
                   music=dict(bpm=96, root=-3, prog="tense", kick="four", gaps=[(E("study") + .05, S("result") + .05)]),
                   cover=dict(words=["1 IN 5", "MEN."], kicker="Have cheated. Women? 13 %."))

def ring(d, cx, cy, r, col, w=14):
    d.ellipse([cx - r, cy - r * .55, cx + r, cy + r * .55], outline=col, width=w)
    d.polygon([(cx - 22, cy - r * .55 - 4), (cx + 22, cy - r * .55 - 4), (cx, cy - r * .55 - 40)], fill=SIG)

def bars(d, t, t0, vals, labels, cols, y0=1060, hmax=420, w=200, prev=None, pcols=None):
    """prev: values (and colours) the bars morph from – carry-over from the scene before"""
    for i, (v, lab, col) in enumerate(zip(vals, labels, cols)):
        k = ease((t - t0 - i * .3) / .5); x = X0 + 120 + i * 360
        if prev:
            vv = lerp(prev[i], v, k); c = mix(pcols[i], col, k); h = hmax * vv / 30
            d.rectangle([x, y0 - h, x + w, y0], fill=c)
            d.text((x + w / 2, y0 - h - 14), f"{vv:.0f} %", font=F(BLK, 60), fill=c, anchor="md")
        else:
            h = hmax * v / 30 * k
            d.rectangle([x, y0 - h, x + w, y0], fill=col)
            if k > .9: d.text((x + w / 2, y0 - h - 14), f"{v} %", font=F(BLK, 60), fill=col, anchor="md")
        d.text((x + w / 2, y0 + 16), lab, font=F(COND, 34), fill=INK, anchor="ma")

def sc_hook(img, d, t):
    d.text((X0 - 6, 320), "1 IN 5", font=F(BLK, 250), fill=SIG); d.text((X0, 570), "married men", font=F(BLK, 90), fill=INK)
    silhouette(img, lambda m: front_bust(m, 330, 860, .55, 255), (120, 740, 560, 1130), INK, cell=9)
    silhouette(img, lambda m: front_bust(m, 640, 870, .5, 255), (440, 760, 860, 1130), MID, cell=9)
    ring(d, 480, 1020, 46, SIG, 10)
    tw = cue("hook", "and women") - .1                                  # impulse: the second figure gets asked
    if t >= tw: box_label(d, 640 - (1 - ease((t - tw) / .2)) * 40, 760, "WOMEN?", 40, WHITE, INK, font=BLK, anchor="ma")
    fig(d, "fig. 1 — the question nobody answers honestly. Except here.")

def sc_study(img, d, t):
    t0 = S("study")
    d.text((X0, 320), "ONE QUESTION.", font=F(BLK, 130), fill=INK)
    k = ease((t - cue("study", "have you ever") + .2) / .4)
    if k > 0:
        d.rectangle([X0, 520, X1, 760], outline=INK, width=4)
        d.text((X0 + 30, 550), "Have you ever had sex with someone", font=F(COND, 40), fill=INK)
        d.text((X0 + 30, 600), "other than your spouse while married?", font=F(COND, 40), fill=INK)
        for i, lab in enumerate(("YES", "NO")):
            x = X0 + 30 + i * 220; d.rectangle([x, 680, x + 40, 720], outline=INK, width=4); d.text((x + 56, 700), lab, font=F(BLK, 36), fill=INK, anchor="lm")
        if t >= cue("study", "while married") + .2:                      # impulse: YES gets ticked
            d.line([X0 + 38, 700, X0 + 48, 712, X0 + 66, 686], fill=SIG, width=7)
    dot_field(d, (X0 + 14, 840, X1, 1110), t, cell=30, col=MID, hit={7, 44, 81})
    fig(d, "General Social Survey (USA), ever-married adults")

def sc_result(img, d, t):
    t0 = S("result")
    d.text((X0, 320), "SAID YES", font=F(BLK, 150), fill=INK)
    bars(d, t, t0 + .1, (20, 13), ("men", "women"), (SIG, INK))
    fig(d, "ever had sex outside the marriage")

def sc_young(img, d, t):
    t0 = S("young")
    words_in(d, t, [("UNDER 30:", t0 - .05, 320, 150, INK)])
    bars(d, t, t0 + .5, (10, 11), ("men", "women"), (INK, SIG), prev=(20, 13), pcols=(SIG, INK))
    if t >= cue("young", "eleven") + .3: box_label(d, X1, 520, "WOMEN AHEAD", 40, WHITE, SIG, font=BLK, anchor="ra")
    fig(d, "ages 18–29")

def sc_old(img, d, t):
    t0, t2 = S("old"), cue("old", "twenty-six") - .3
    d.text((X0, 320), "HIGHEST:", font=F(BLK, 130), fill=INK)
    d.text((X0, 470), "MEN IN THEIR 70s", font=F(BLK, 100), fill=SIG)
    if t >= t2: counter(d, X0, 620, t, t2, .5, 26, "{:.0f} %", 220, SIG)
    silhouette(img, lambda m: body(m, 700, 1120, 460, 255), (540, 640, 860, 1130), INK, cell=9)
    fig(d, "the oldest group, not the youngest")

def sc_point(img, d, t):
    t0, tm = S("point"), cue("point", "and most") - .2
    words_in(d, t, [("OLDER THAN", t0, 320, 140, INK), ("THE CLICHÉ.", t0 + .3, 470, 140, SIG)] if t < tm else [("MOST", tm, 320, 200, INK), ("NEVER DO.", tm + .2, 520, 150, SIG)])
    if t >= tm:
        k = clamp((t - tm) / 1.0)
        for i in range(100):
            r, c = divmod(i, 20); x = X0 + 20 + c * 42; y = 760 + r * 42
            d.ellipse([x - 12, y - 12, x + 12, y + 12], fill=(SIG if i < 17 else INK) if i < 100 * k else RULE)
        d.text((X1, 1146), "≈ 1 in 6 overall · schematic", font=F(MED, 22), fill=MID, anchor="ra")
    fig(d, "fig. 2 — the majority stays faithful")

# carry-over: every scene hands one element to the next
EP.carry = {
    "hook":  [((680, 950, 880, 1150), (430, 952, 530, 1050))],      # countdown ring → wedding ring
    "study": [((120, 740, 560, 1130), (277, 833, 291, 847))],       # the man → one dot in the data
    "result": [((144, 686, 212, 714), (434, 338, 708, 447))],       # the ticked YES → the headline's YES
}
EP.cuts = {"young": "stay"}                                         # same bars, new values: no whip

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "young": sc_young, "old": sc_old, "point": sc_point}
FX = [(0.0, thud(.5), 0), (.3, pop(.12), .2), (cue("hook", "and women") - .1, pop(.14), .2), (cue("study", "while married") + .2, tick(.08), 0), *EP.cut_fx(), (cue("study", "have you ever") - .2, pop(.15), 0), (S("result") + .05, thud(.55), 0),
      (S("result") + .1, pop(.15), -.3), (S("result") + .4, pop(.15), .3), (cue("young", "eleven") + .3, thud(.35), 0),
      (cue("old", "twenty-six") - .3, thud(.5), 0), (cue("point", "and most") - .2, riser(.5, .05), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
