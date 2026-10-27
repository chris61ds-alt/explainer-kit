"""NOT JUST YOU · AFTER DARK – No. 49: the orgasm gap (Frederick, St. John, Garcia & Lloyd 2018)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .8, "result": .5, "twist": .6, "why": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "twist", "why", "point", "end"]
EP = Episode(TL, 49, "THE GAP", order=ORDER, dark=True, series="NOT JUST YOU · AFTER DARK",
             chapters={"hook": "THE GAP", "study": "52,588 PEOPLE", "result": "THE GAP", "twist": "THE TWIST", "why": "WHAT HELPS", "point": "CLOSE IT"},
             sources=("Frederick, St. John, Garcia & Lloyd (2018),", "Archives of Sexual Behavior 47(1)"),
             music=dict(bpm=94, root=0, prog="tense", kick="four", gaps=[(E("study") + .05, S("result") + .05)]),
             cover=dict(words=["MIND", "THE GAP."], kicker="The one nobody talks about."))

BASE, TOP = 1090, 640                       # bar chart frame: 100 % = BASE - TOP px
def vbar(d, x, v, k, col, lab, w=170, show=True):
    h = (BASE - TOP) * v / 100 * ease(k)
    d.rectangle([x, BASE - h, x + w, BASE], fill=col)
    if show and k > .9: d.text((x + w / 2, BASE - h - 12), f"{v} %", font=F(BLK, 44), fill=col, anchor="md")
    d.text((x + w / 2, BASE + 16), lab, font=F(COND, 28), fill=INK, anchor="ma")
    return BASE - h

def sc_hook(img, d, t):
    d.text((X0 - 6, 300), "THE GAP", font=F(BLK, 210), fill=INK)
    d.text((X0, 510), "nobody talks about", font=F(COND, 44), fill=MID)
    g = 40 + 200 * ease((t - .4) / 1.0)
    d.rectangle([X0, 760, 480 - g / 2, 900], fill=INK); d.rectangle([480 + g / 2, 760, X1, 900], fill=SIG)
    if g > 60: dim_h(d, 480 - g / 2, 480 + g / 2, 940, 1, SIG, None)
    d.text((480, 960), "?", font=F(BLK, 90), fill=SIG, anchor="ma")
    fig(d, "fig. 1 — mind the gap")

def sc_study(img, d, t):
    t0 = S("study"); k = clamp((t - t0 - .2) / 2.2)
    counter(d, X0, 300, t, t0 + .1, 1.2, 52588, "{:,.0f}", 190, SIG)
    d.text((X0 + 6, 520), "US adults · how often do you usually orgasm?", font=F(COND, 34), fill=INK)
    for i in range(int(500 * k)):
        r, c = divmod(i, 25); x = X0 + 20 + c * 34; y = 620 + r * 24
        d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=INK if i % 11 else SIG)
    fig(d, "online national sample · Frederick et al., 2018")

def sc_result(img, d, t):
    t0 = S("result"); tm = cue("result", "straight men"); tw = cue("result", "straight women")
    d.text((X0, 300), "USUALLY / ALWAYS", font=F(BLK, 90), fill=INK)
    y1 = vbar(d, X0 + 40, 95, (t - tm) / .5, INK, "straight men")
    y2 = vbar(d, X0 + 300, 65, (t - tw) / .5, SIG, "straight women")
    if t >= tw + .6:
        x = X0 + 520; dim_v(d, x, y1, y2, (t - tw - .6) / .4, SIG, "30 pts")
        d.line([X0 + 210, y1, x + 10, y1], fill=MID, width=2)
    fig(d, "share who usually or always orgasm during sex")

def sc_twist(img, d, t):
    t0 = S("twist"); tl = cue("twist", "eighty-six")
    d.text((X0, 300), "BUT…", font=F(BLK, 150), fill=INK)
    vbar(d, X0 + 0, 95, 1, MID, "straight men", w=150)
    vbar(d, X0 + 210, 65, 1, MID, "straight women", w=150)
    vbar(d, X0 + 440, 86, (t - tl + .2) / .5, SIG, "lesbian women", w=170)
    if t >= tl + .4: box_label(d, X1, 470, "SAME BODIES.", 40, WHITE, SIG, anchor="ra"); box_label(d, X1, 540, "DIFFERENT SEX.", 40, WHITE, INK, anchor="ra")
    fig(d, "women with women: 86 %")

def sc_why(img, d, t):
    t0 = S("why")
    tb = cue("why", "not just biology")
    words_in(d, t, [("NOT JUST", tb - .1, 300, 120, INK), ("BIOLOGY.", tb + .2, 420, 120, SIG)])
    items = [("MORE ORAL", "oral"), ("LONGER", "longer"), ("ASKED FOR IT", "asked for")]
    for i, (lab, w) in enumerate(items):
        tk = cue("why", w) - .2; k = ease((t - tk) / .35)
        if k <= 0: continue
        y = 620 + i * 150
        d.text((X0, y + 10), "+", font=F(BLK, 70), fill=SIG)
        box_label(d, X0 + 70 + (1 - k) * 40, y, lab, 60, WHITE, SIG if i == 2 else INK)
    fig(d, "what women who orgasmed more often reported")

def sc_point(img, d, t):
    t0 = S("point"); tc = cue("point", "can be closed"); ts = cue("point", "start by")
    words_in(d, t, [("REAL.", t0, 300, 170, INK), ("CLOSABLE.", tc - .1, 470, 150, SIG)])
    g = 240 * (1 - ease((t - tc) / 1.4))
    d.rectangle([X0, 760, 480 - g / 2 - 2, 880], fill=INK); d.rectangle([480 + g / 2 + 2, 760, X1, 880], fill=SIG)
    if t >= ts:
        picto(d, 330, FLOOR, .6, INK, f=1, pose=TALK(t)); picto(d, 630, FLOOR, .6, SIG, f=-1, pose=TALK(t, 2))
        speech_box(d, 360, 920, 200, (t - ts) / .3, INK, 1, "talk", 32)
    fig(d, "fig. 2 — start with a conversation")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "twist": sc_twist, "why": sc_why, "point": sc_point}
FX = [(0.0, thud(.5), 0), (.4, whoosh(1.0, .08), 0), *EP.cut_fx(), *[(S("study") + .2 + i * .12, tick(.035), (i % 5 - 2) / 3) for i in range(16)],
      (cue("result", "straight men"), thud(.45), -.2), (cue("result", "straight women"), thud(.45), .2), (cue("result", "straight women") + .6, pop(.15), 0),
      (cue("twist", "eighty-six") - .2, riser(.4, .06), 0), (cue("twist", "eighty-six") + .4, thud(.5), 0),
      *[(cue("why", w) - .2, pop(.15), (i - 1) / 2) for i, w in enumerate(("oral", "longer", "asked for"))],
      (cue("point", "can be closed"), riser(1.2, .05), 0), (cue("point", "start by"), pop(.15), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
