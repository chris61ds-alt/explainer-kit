"""Single video (outside the series): why Algeria gets so few tourists vs. Morocco, Egypt, Tunisia. Look C+D, dark."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from thread import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, end="card", lead=.15, gaps={"hook": .6, "numbers": .7, "oil": .6, "war": .6, "visa": .6, "twist": .7, "point": .8, "end": 2.6})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "numbers", "oil", "war", "visa", "twist", "point", "end"]
EP = ThreadEpisode(TL, 0, "EMPTY GIANT", order=ORDER, dark=True, series="TRAVEL DATA", handle="", label="TRAVEL DATA · 2024",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Tourism data 2024: Morocco, Egypt, Tunisia, ONAT Algeria", "Carnegie / IBTimes · Destination Tunisie · TravelMole"),
                   music=dict(bpm=92, root=-2, prog="minor", kick="half", gaps=[(E("numbers") + .05, S("oil") + .05)]))

def dunes(m, y0, bottom=None):
    pts = [(x, y0 + 60 * math.sin(x / 170 + 1.3) + 30 * math.sin(x / 61)) for x in range(-20, 1101, 20)]
    b = bottom or y0 + 400
    m.polygon(pts + [(1100, b), (-20, b)], fill=255)

def arch(m, x, base, h=340, w=300):
    """Roman triumphal arch (Timgad-like): block with a round-headed passage"""
    m.rectangle([x - w / 2, base - h, x + w / 2, base], fill=255)
    m.rectangle([x - w / 2 - 16, base - h - 34, x + w / 2 + 16, base - h], fill=255)
    pw = w * .42; m.rectangle([x - pw / 2, base - h * .55, x + pw / 2, base], fill=0)
    m.ellipse([x - pw / 2, base - h * .55 - pw / 2, x + pw / 2, base - h * .55 + pw / 2], fill=0)
    for dx in (-w * .36, w * .36): m.rectangle([x + dx - 10, base - h + 30, x + dx + 10, base - 20], fill=0)

def sc_hook(img, d, t):
    tw = cue("hook", "so why") - .2
    d.text((X0 - 6, 320), "ALGERIA.", font=F(BLK, 200), fill=INK)
    d.text((X0 + 4, 530), "Africa's largest country", font=F(COND, 44), fill=MID)
    silhouette(img, lambda m: dunes(m, 1020), (0, 900, W, 1150), SIG, cell=9)
    silhouette(img, lambda m: arch(m, 680, 1010), (500, 600, 860, 1015), INK, cell=8)
    if t >= tw:
        box_label(d, X0, 640, "SO WHY", 54, WHITE, INK, font=BLK); box_label(d, X0, 730, "NOBODY GOES?", 54, WHITE, SIG, font=BLK)
    fig(d, "Roman ruins · Sahara · Mediterranean coast")

BARS = [("MOROCCO", 17.4, "morocco"), ("EGYPT", 15.7, "egypt"), ("TUNISIA", 10.2, "tunisia"), ("ALGERIA", 3.5, "algeria")]

def sc_numbers(img, d, t):
    td = cue("numbers", "almost a third") - .3
    d.text((X0, 320), "VISITORS 2024", font=F(BLK, 96), fill=INK)
    for i, (lab, v, w) in enumerate(BARS):
        tk = cue("numbers", w) - .25; k = ease((t - tk) / .5); y = 470 + i * 160; alg = lab == "ALGERIA"
        d.text((X0, y), lab, font=F(COND, 34), fill=SIG if alg else INK)
        if k <= 0: continue
        L = 640 * v / 17.4 * k
        d.rectangle([X0, y + 44, X0 + L, y + 114], fill=SIG if alg else mix(BG, INK, .85))
        if alg and t >= td:
            dk = ease((t - td) / .5); dl = 640 * 1.09 / 17.4
            d.rectangle([X0 + L - dl * dk, y + 44, X0 + L, y + 114], fill=MID)
            if dk > .9: d.text((X0 + L + 16, y + 128), "~1/3 diaspora", font=F(COND, 28), fill=MID, anchor="la")
        if k > .9: d.text((X0 + L + 16, y + 79), f"{v:.1f} M", font=F(BLK, 48), fill=SIG if alg else INK, anchor="lm")
    fig(d, "international arrivals, national statistics")

def sc_oil(img, d, t):
    t0 = S("oil")
    d.text((X0, 320), "1 · OIL & GAS", font=F(BLK, 104), fill=INK)
    counter(d, X0, 460, t, t0 + .6, .8, 85, "{:.0f} %", 230, SIG)
    d.text((X0 + 6, 700), "of exports (2018)", font=F(COND, 40), fill=INK)
    k = ease((t - t0 - .6) / .8)
    d.rectangle([X0, 790, X0 + 840 * .85 * k, 880], fill=SIG); d.rectangle([X0 + 840 * .85 * k, 790, X0 + 840 * k, 880], fill=MID)
    if k > .95: d.text((X0, 900), "hydrocarbons", font=F(BLK, 30), fill=SIG); d.text((X1, 900), "rest", font=F(BLK, 30), fill=MID, anchor="ra")
    if t >= cue("oil", "never needed") - .2: box_label(d, X0, 1000, "NO NEED FOR TOURISTS", 44, WHITE, INK, font=BLK)
    fig(d, "\"tourism was never developed\" – Carnegie")

def sc_war(img, d, t):
    t0, t13 = S("war"), cue("war", "twenty thirteen") - .3
    d.text((X0, 320), "2 · THE 90s", font=F(BLK, 120), fill=INK)
    counter(d, X0, 480, t, t0 + .8, .9, 200000, "{:,.0f}", 170, SIG)
    d.text((X0 + 6, 670), "dead in the civil war (up to)", font=F(COND, 40), fill=INK)
    if t >= t13:
        box_label(d, X0, 780, "2013: IN AMENAS GAS PLANT", 46, WHITE, SIG, font=BLK)
        d.text((X0 + 6, 860), "dozens of foreign hostages killed", font=F(COND, 38), fill=INK)
        if t < t13 + .3: glitch(img, (X0, 460, X1, 900), 1.0, seed=int(t * 30))
    fig(d, "\"the image stuck\"")

def sc_visa(img, d, t):
    d.text((X0, 320), "3 · THE VISA", font=F(BLK, 120), fill=INK)
    rows = [("MOROCCO", "VISA-FREE", "morocco", INK), ("TUNISIA", "VISA-FREE", "tunisia", INK), ("EGYPT", "AT THE AIRPORT", "egypt", INK),
            ("ALGERIA", "CONSULATE, IN ADVANCE", "algeria", SIG)]
    for i, (c, v, w, col) in enumerate(rows):
        tk = cue("visa", w) - .25; k = ease((t - tk) / .3)
        if k <= 0: continue
        y = 500 + i * 140
        d.text((X0 + (1 - k) * 30, y), c, font=F(COND, 34), fill=MID)
        box_label(d, X0 + (1 - k) * 30, y + 44, v, 44, WHITE, col, font=BLK)
    fig(d, "rules for EU citizens")

def sc_twist(img, d, t):
    t0, ta = S("twist"), cue("twist", "about as many") - .3
    d.text((X0, 320), "THE IRONY:", font=F(BLK, 120), fill=INK)
    counter(d, X0, 470, t, t0 + .5, .8, 3.51, "{:.2f} M", 200, SIG)
    d.text((X0 + 6, 690), "Algerians on holiday in Tunisia", font=F(COND, 40), fill=INK)
    if t >= ta:
        k = ease((t - ta) / .6)
        d.rectangle([X0, 790, X0 + 760 * k, 860], fill=SIG); d.text((X0, 870), "Algerians in Tunisia  3.51 M", font=F(BLK, 30), fill=SIG)
        d.rectangle([X0, 940, X0 + 768 * k, 1010], fill=INK); d.text((X0, 1020), "all visitors to Algeria  3.55 M", font=F(BLK, 30), fill=INK)
    fig(d, "2024 · Destination Tunisie · ONAT")

def sc_point(img, d, t):
    t0 = S("point")
    d.text((X0, 320), "NOW:", font=F(BLK, 150), fill=INK)
    items = [("SAHARA: VISA ON ARRIVAL", "visa on arrival", SIG), ("NEW HOTELS", "new hotels", INK), ("GOAL 2030: 12 M VISITORS", "twelve million", SIG)]
    for i, (lab, w, col) in enumerate(items):
        tk = cue("point", w) - .25; k = ease((t - tk) / .3)
        if k > 0: box_label(d, X0 + (1 - k) * 40, 520 + i * 110, lab, 48, WHITE, col, font=BLK)
    silhouette(img, lambda m: dunes(m, 1060), (0, 960, W, 1150), MID, cell=8)
    fig(d, "Sahara visa on arrival via approved tour operators")

def end_card(d, t):
    k0 = S("end")
    for i, (w_, col) in enumerate((("SLEEPING", INK), ("BEAUTY,", INK), ("WAKING UP?", SIG))):
        k = ease((t - k0 - i * .15) / .35)
        if k > 0: d.text((X0 - 8, 300 + i * 190), w_, font=F(BLK, 170 if i < 2 else 140), fill=mix(BG, col, k))
    if t > k0 + .9:
        d.text((X0, 960), "SOURCES", font=F(COND, 26), fill=SIG)
        for i, l in enumerate(EP.sources): d.text((X0, 996 + i * 32), l, font=F(MED, 22), fill=INK)
EP.end_card = end_card

def make_cover(path, **kw):
    img = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(img)
    for x in range(X0, X1 + 1, 140): d.line([x, 240, x, 1680], fill=RULE, width=2)
    d.text((X0, 300), "TRAVEL DATA · 2024", font=F(COND, 40), fill=INK); d.line([X0, 356, X1 + 60, 356], fill=INK, width=5)
    d.text((X0 - 8, 420), "WHY NOBODY", font=F(BLK, 150), fill=INK); d.text((X0 - 8, 580), "VISITS", font=F(BLK, 150), fill=INK)
    d.text((X0 - 8, 740), "ALGERIA.", font=F(BLK, 190), fill=SIG)
    d.text((X0, 980), "17.4 M vs. 3.5 M visitors", font=F(COND, 50), fill=INK)
    halftone(img, lambda m: dunes(m, 1420), (0, 1250, W, 1580), cell=10, col=SIG)
    d.line([X0, 1600, X1 + 60, 1600], fill=INK, width=5)
    darken(img); img.save(path); return path
EP.make_cover = make_cover

EP.scenes = {"hook": sc_hook, "numbers": sc_numbers, "oil": sc_oil, "war": sc_war, "visa": sc_visa, "twist": sc_twist, "point": sc_point}
FX = [(0.0, thud(.5), 0), (.3, whoosh(.8, .05), 0), (cue("hook", "so why") - .2, thud(.45), 0), *EP.cut_fx(),
      *[(cue("numbers", w) - .25, pop(.13), (i - 1.5) / 2) for i, (_, _, w) in enumerate(BARS)], (cue("numbers", "almost a third") - .3, pop(.15), .4),
      (S("oil") + .6, riser(.8, .04), 0), (cue("oil", "never needed") - .2, thud(.4), 0), (S("war") + .8, riser(.9, .04), 0),
      (cue("war", "twenty thirteen") - .3, rewind_sfx(.12, .35), 0), *[(cue("visa", w) - .25, pop(.13), (i - 1.5) / 2) for i, w in enumerate(("morocco", "tunisia", "egypt", "algeria"))],
      (cue("visa", "algeria") - .2, thud(.4), 0), (S("twist") + .5, riser(.8, .04), 0), (cue("twist", "about as many") - .3, thud(.5), 0),
      *[(cue("point", w) - .25, pop(.14), (i - 1) / 2) for i, w in enumerate(("visa on arrival", "new hotels", "twelve million"))], (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
