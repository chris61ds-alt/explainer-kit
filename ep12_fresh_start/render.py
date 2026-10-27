"""NOT JUST YOU – No. 12: the fresh start effect (Dai, Milkman & Riis 2014; 2015). Look: Swiss Detail v2."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .4, "search": .4, "gym": .8, "name": .5, "why": .45, "trick": .55, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "search", "gym", "name", "why", "trick", "point", "end"]
EP = Episode(TL, 12, "FRESH START", order=ORDER,
             chapters={"hook": "MONDAY", "search": "THE SEARCHES", "gym": "THE GYM", "name": "THE NAME", "why": "WHY",
                       "trick": "THE TRICK", "point": "ANOTHER FIRST DAY"},
             sources=("Dai, Milkman & Riis (2014), Management Science 60", "(2015), Psychological Science 26"),
             music=dict(bpm=108, root=-2, prog="major", kick="four", gaps=[(E("gym") + .05, S("name") + .05)]),
             cover=dict(words=["MONDAY", "AGAIN?"], kicker="The fresh start effect."))

DAYS = ["MO", "TU", "WE", "TH", "FR", "SA", "SU"]
def calendar(d, box, t, k_col=0.0, marks=(), month="NEXT MONTH"):
    x0, y0, x1, y1 = box; cw = (x1 - x0) / 7; rh = (y1 - y0 - 60) / 5
    d.rectangle([x0, y0, x1, y1], outline=INK, width=5)
    d.rectangle([x0, y0, x1, y0 + 60], fill=INK); d.text((x0 + 20, y0 + 30), month, font=F(COND, 30), fill=WHITE, anchor="lm")
    if k_col > 0:
        d.rectangle([x0, y0 + 60, x0 + cw, y0 + 60 + (y1 - y0 - 60) * ease(k_col)], fill=SIG)
    for i, dn in enumerate(DAYS):
        d.text((x0 + cw * i + cw / 2, y0 + 80), dn, font=F(COND, 24), fill=WHITE if (i == 0 and k_col > .1) else INK, anchor="mm")
    n = 1
    for r in range(5):
        for c in range(7):
            x, y = x0 + cw * c, y0 + 100 + rh * r * .92
            if n <= 30:
                d.text((x + 14, y + 6), str(n), font=F(COND, 26), fill=WHITE if (c == 0 and k_col > .3) else INK)
                if n in marks: d.rectangle([x + 8, y + 2, x + cw - 8, y + rh * .8], outline=SIG, width=5)
            n += 1
    for c in range(1, 7): d.line([x0 + cw * c, y0 + 60, x0 + cw * c, y1], fill=RULE, width=2)

# ---------------------------------------------------------------- actor carried across scenes
TG = {"hook": (760, 1.0, 0), "search": (760, 1.0, 700), "gym": (300, .9, 0), "name": (300, .9, 700), "why": (300, .9, 700),
      "trick": (300, .9, 700), "point": (760, 1.0, 0)}
POSE = [(0, SHRUG), (S("gym"), WALK), (E("gym"), IDLE), (S("point"), IDLE), (cue("point", "find"), WAVE)]
def actor(img, d, t, cur):
    i = ORDER.index(cur); prev = ORDER[max(0, i - 1)]
    k = ease_io((t - S(cur) + .05) / .55) if i else 1
    x, s, dy = (lerp(a, b, k) for a, b in zip(TG[prev], TG[cur]))
    if cur == "gym": x = lerp(240, 470, clamp((t - S("gym")) / (E("gym") - S("gym"))))
    if dy < 650: picto(d, x, FLOOR + dy, s, INK, f=1 if cur == "gym" else -1, pose=pose_seq(t, POSE))
EP.layers.append(actor)

# ---------------------------------------------------------------- scenes
def sc_hook(img, d, t):
    giant(d, "MONDAY?", size=200)
    calendar(d, (X0, 560, 640, 1120), t, k_col=(t - .3) / .6)
    if t >= cue("hook", "start"):
        note(d, X0 + 40, 700, 700, 620, "again", (t - cue("hook", "start")) / .35, SIG, size=30)

def sc_search(img, d, t):
    t0 = S("search")
    d.text((X0, 320), "SEARCHES FOR", font=F(BLK, 64), fill=INK)
    box_label(d, X0, 410, '"DIET"', 56, WHITE, SIG)
    ox, oy, w, h = X0, 1000, X1 - X0, 380
    d.line([ox, oy, ox + w, oy], fill=INK, width=4)
    prog = clamp((t - t0 - .2) / 3.6)
    pts = []
    for i in range(0, 241):
        u = i / 240
        if u > prog: break
        wk = (i % 20 == 0); mo = (i % 80 == 0); yr = (i == 160)
        v = .18 + .05 * math.sin(i * .7) + (.22 if wk else 0) + (.18 if mo else 0) + (.35 if yr else 0)
        pts.append((ox + w * u, oy - h * v))
    if len(pts) > 1: d.line(pts, fill=INK, width=4, joint="curve")
    for u, lab, tk in ((20 / 240, "NEW WEEK", cue("search", "week")), (80 / 240, "NEW MONTH", cue("search", "month")), (160 / 240, "NEW YEAR", cue("search", "year"))):
        if t >= tk - .1 and prog >= u:
            x = ox + w * u; note(d, x, oy - h * .55, x + 20, oy - h * .55 - 60 - (40 if lab == "NEW YEAR" else 0), lab, (t - tk + .1) / .35, SIG, size=26)
    d.text((X1, 1146), "schematic", font=F(MED, 22), fill=MID, anchor="ra")
    fig(d, "Google searches · Dai, Milkman & Riis, 2014")

def cake(d, x, y, s=1.0):
    d.rectangle([x - 50 * s, y - 60 * s, x + 50 * s, y], fill=SIG); d.rectangle([x - 50 * s, y - 70 * s, x + 50 * s, y - 60 * s], fill=INK)
    d.line([x, y - 70 * s, x, y - 100 * s], fill=INK, width=int(6 * s)); d.ellipse([x - 7 * s, y - 116 * s, x + 7 * s, y - 100 * s], fill=SIG)

def dumbbell(d, x, y, s=1.0):
    d.line([x - 60 * s, y, x + 60 * s, y], fill=INK, width=int(12 * s))
    for sx in (-1, 1): d.rectangle([x + sx * 60 * s - 16 * s, y - 40 * s, x + sx * 60 * s + 16 * s, y + 40 * s], fill=INK)

def sc_gym(img, d, t):
    t0 = S("gym")
    d.text((X0, 320), "GYM VISITS", font=F(BLK, 110), fill=INK)
    dumbbell(d, 760, 1060, 1.1)
    items = [("NEW WEEK", cue("gym", "week")), ("NEW SEMESTER", cue("gym", "semester")), ("BIRTHDAY", cue("gym", "birthday"))]
    for i, (lab, tk) in enumerate(items):
        k = ease((t - tk + .1) / .3)
        if k > 0:
            y = 480 + i * 110
            d.text((X0, y), "+", font=F(BLK, 60), fill=SIG)
            box_label(d, X0 + 60, y + 8, lab, 44, WHITE, INK if i < 2 else SIG)
            if lab == "BIRTHDAY": cake(d, X0 + 330, y + 54, .5)
    fig(d, "university gym check-ins · Dai, Milkman & Riis, 2014")

def sc_name(img, d, t):
    t0 = S("name"); k = (t - cue("name", "fresh") + .15) / .4
    if k > 0:
        d.text((X0 - 8 - (1 - ease(k)) * 80, 330), "FRESH", font=F(BLK, 250), fill=mix(BG, INK, ease(k)))
        d.text((X0 - 8 - (1 - ease(k - .2)) * 80, 580), "START.", font=F(BLK, 250), fill=mix(BG, SIG, ease(k - .2)))
    if k > 1: note(d, 820, 700, 860, 960, "effect", (t - cue("name", "start") - .2) / .4, INK, anchor="ra", size=30)

def book(d, t, flip):
    x0, y0, x1, y1 = 120, 470, 840, 1080; cx = (x0 + x1) / 2
    d.rectangle([x0, y0, x1, y1], outline=INK, width=6); d.line([cx, y0, cx, y1], fill=INK, width=6)
    d.text((x0 + 30, y0 + 30), "CHAPTER 1", font=F(COND, 30), fill=MID)
    for i in range(6): d.line([x0 + 30, y0 + 110 + i * 60, cx - 40 - (i % 3) * 30, y0 + 110 + i * 60], fill=RULE, width=6)
    for i, lab in enumerate(("skipped gym", "ate the cake", "gave up")):
        d.text((x0 + 34, y0 + 100 + i * 120), lab, font=F(COND, 28), fill=MID)
        d.line([x0 + 30, y0 + 120 + i * 120, x0 + 30 + 260 * ease(flip), y0 + 120 + i * 120], fill=INK, width=4)
    # right page: new chapter
    d.text((cx + 30, y0 + 30), "CHAPTER 2", font=F(COND, 30), fill=SIG)
    if flip > 0:
        ph = ease(flip)
        poly = [(cx, y0), (cx + (x1 - cx) * (1 - ph), y0 - 40 * math.sin(ph * math.pi)), (cx + (x1 - cx) * (1 - ph), y1 - 40 * math.sin(ph * math.pi)), (cx, y1)]
        if ph < .98: d.polygon(poly, fill=WHITE, outline=INK)
    d.text((cx + 30, y0 + 110), "blank.", font=F(BLK, 48), fill=INK)

def sc_why(img, d, t):
    t0 = S("why")
    d.text((X0, 320), "A NEW CHAPTER", font=F(BLK, 96), fill=INK)
    book(d, t, clamp((t - cue("why", "old")) / .8))
    fig(d, "fig. 1 — past slip-ups feel like they belong to the old you")

def sc_trick(img, d, t):
    t0 = S("trick"); sp = cue("trick", "first day")
    d.text((X0, 320), "MARCH 20", font=F(BLK, 130), fill=INK)
    d.text((X0, 470), "the same day, two names:", font=F(COND, 34), fill=INK)
    d.text((X0, 530), "the third Thursday in March", font=F(BLK, 44), fill=MID)
    if t >= sp - .1:
        k = ease((t - sp + .1) / .35); d.line([X0, 556, X0 + 640 * k, 556], fill=INK, width=6)
        box_label(d, X0, 610, "THE FIRST DAY OF SPRING", 44, WHITE, SIG) if k > .8 else None
    kb = (t - cue("trick", "more likely") + .2) / .6
    if kb > 0:
        hbar(d, 760, .07 / .3, kb, INK, "called \"third Thursday in March\": 7 % signed up", h=80)
        hbar(d, 900, .26 / .3, kb - .3, SIG, "called \"the first day of spring\": 26 %", h=80)
    fig(d, "goal reminder sign-ups · Dai, Milkman & Riis, 2015")

def sc_point(img, d, t):
    t0 = S("point"); fd = cue("point", "find")
    giant(d, "MISSED IT?", size=120, k=(t - t0) / .3)
    marks = (1, 8, 15, 22, 29) if t < fd else (1, 8, 11, 15, 19, 22, 26, 29)
    calendar(d, (X0, 600, 640, 1120), t, k_col=1 - ease((t - fd) / .4) * .7, marks=marks if t >= fd else ())
    if t >= fd:
        for i, (lab, dx, dy) in enumerate((("first day of autumn", 0, 0), ("first day after vacation", 0, 70), ("first day of the month", 0, 140))):
            kk = ease((t - fd - i * .15) / .3)
            if kk > 0: box_label(d, X0 + 10, 440 + dy * .7, lab, 26, WHITE, SIG if i == 0 else INK)
    fig(d, "fig. 2 — every calendar is full of first days")

EP.scenes = {"hook": sc_hook, "search": sc_search, "gym": sc_gym, "name": sc_name, "why": sc_why, "trick": sc_trick, "point": sc_point}

FX = [(0.0, thud(.5), 0), (.3, whoosh(.5, .1), -.2), (cue("hook", "start"), pop(.18), .3),
      *EP.cut_fx(),
      (cue("search", "week"), pop(.15), -.3), (cue("search", "month"), pop(.15), 0), (cue("search", "year"), thud(.35), .3),
      (cue("gym", "week"), pop(.15), -.2), (cue("gym", "semester"), pop(.15), 0), (cue("gym", "birthday"), pop(.2), .2),
      (cue("name", "fresh") - .15, thud(.55), 0), (cue("name", "start"), thud(.4), 0),
      (cue("why", "old"), whoosh(.7, .14), .2),
      (cue("trick", "first day"), pop(.2), 0), (cue("trick", "more likely"), riser(.5, .08), 0),
      (cue("point", "find"), thud(.45), 0), *[(cue("point", "find") + i * .15, pop(.12), .3) for i in range(3)],
      (S("end"), thud(.5), 0)]

if __name__ == "__main__": EP.run(FX)
