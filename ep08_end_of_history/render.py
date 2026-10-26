"""NOT JUST YOU – No. 08: the end of history illusion (Quoidbach, Gilbert & Wilson 2013). Look: Swiss Detail."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .35, "ahead": .5, "study": .45, "result": .5, "name": .5, "band": .5, "quote": .6, "point": .7, "end": 2.4})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "ahead", "study", "result", "name", "band", "quote", "point", "end"]
EP = Episode(TL, 8, "THE END OF HISTORY", order=ORDER,
             chapters={"hook": "10 YEARS AGO", "ahead": "10 YEARS AHEAD", "study": "THE STUDY", "result": "THE RESULT",
                       "name": "THE NAME", "band": "THE BAND TEST", "quote": "THE QUOTE", "point": "NOT FINAL"},
             sources=("Quoidbach, Gilbert & Wilson (2013),", "Science 339 · via New York Times, 2013"))

# accessories that make each 'version' of you different
def cap(d, h, s, col=SIG): d.pieslice([h[0] - 44 * s, h[1] - 46 * s, h[0] + 44 * s, h[1] + 30 * s], 180, 360, fill=col); d.rectangle([h[0], h[1] - 14 * s, h[0] + 70 * s, h[1] - 4 * s], fill=col)
def phones(d, h, s, col=SIG):
    d.arc([h[0] - 56 * s, h[1] - 60 * s, h[0] + 56 * s, h[1] + 40 * s], 190, 350, fill=col, width=int(10 * s))
    for sx in (-1, 1): d.rectangle([h[0] + sx * 56 * s - 12 * s, h[1] - 14 * s, h[0] + sx * 56 * s + 12 * s, h[1] + 22 * s], fill=col)
def specs(d, h, s, col=WHITE):
    for sx in (-1, 1): d.rectangle([h[0] + sx * 18 * s - 13 * s, h[1] - 8 * s, h[0] + sx * 18 * s + 13 * s, h[1] + 8 * s], outline=col, width=int(4 * s))

def timeline(d, y, t, ahead_k=0.0):
    x0, xn, x1 = X0 + 20, 560, X1 - 20
    d.line([x0, y, xn, y], fill=INK, width=5)
    for i, lab in enumerate(("−10", "−5", "NOW")):
        x = lerp(x0 + 60, xn, i / 2); d.line([x, y - 14, x, y + 14], fill=INK, width=4)
        d.text((x, y + 26), lab, font=F(COND, 28), fill=INK if lab != "NOW" else SIG, anchor="ma")
    if ahead_k > 0:
        e = ease(ahead_k); xe = lerp(xn, x1, e)
        for xx in range(int(xn), int(xe), 26): d.line([xx, y, xx + 14, y], fill=SIG, width=5)
        if e > .95:
            d.line([x1 - 60, y - 14, x1 - 60, y + 14], fill=SIG, width=4); d.text((x1 - 60, y + 26), "+10", font=F(COND, 28), fill=SIG, anchor="ma")

def versions(d, t, y=FLOOR - 120, k=1.0):
    x0, xn = X0 + 80, 560
    looks = [(INK, cap, TALK(t)), (MID, phones, SHRUG), (SIG, specs, IDLE)]
    heads = []
    for i, (col, acc, pose) in enumerate(looks):
        kk = ease((k - i * .25) / .3)
        if kk <= 0: continue
        x = lerp(x0, xn, i / 2)
        h = picto(d, x, y, .6 * kk, col, pose=pose); acc(d, h, .6 * kk); heads.append(h)
    return heads

def sc_hook(img, d, t):
    giant(d, "−10 YEARS", size=170)
    timeline(d, 1040, t)
    versions(d, t, k=(t - .1) / .9)
    if t >= cue("hook", "different"):
        dim_h(d, X0 + 80, 560, 600, (t - cue("hook", "different")) / .4, SIG, "A LOT OF CHANGE", 24)
    fig(d, "fig. 1 — three versions of you")

def sc_ahead(img, d, t):
    t0 = S("ahead")
    giant(d, "+10 YEARS", size=170, k=(t - t0) / .3)
    timeline(d, 1040, t, (t - t0 - .2) / .6)
    versions(d, t)
    if t >= cue("ahead", "same") - .2:
        k = ease((t - cue("ahead", "same") + .2) / .4)
        x = X1 - 80
        h = picto(d, x, FLOOR - 120, .6, mix(BG, RULE, k), pose=IDLE); specs(d, h, .6, BG)
        note(d, x - 40, FLOOR - 300, 690, 560, "same as now?", (t - cue("ahead", "same")) / .4, SIG, anchor="ra")
    fig(d, "fig. 2 — the version you predict")

def sc_study(img, d, t):
    t0 = S("study"); n = int(clamp((t - t0 - .1) / 1.6) * 19000)
    d.text((X0 - 8, 290), f"{n:,}+", font=F(BLK, 200), fill=SIG)
    d.text((X0, 520), "people · six studies", font=F(COND, 40), fill=INK)
    rng = np.random.default_rng(2)
    kk = clamp((t - cue("study", "aged")) / 1.2)
    for i in range(int(420 * kk)):
        x = X0 + 20 + rng.uniform(0, X1 - X0 - 40); y = 640 + rng.uniform(0, 300)
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=INK if i % 9 else SIG)
    ruler(d, 980, X0 + 20, X1 - 20, ["18", "28", "38", "48", "58", "68"], minor=50)
    d.text((X1 - 20, 1050), "age", font=F(MONO, 20), fill=MID, anchor="ra")
    fig(d, "Quoidbach, Gilbert & Wilson — Science, 2013")

def sc_result(img, d, t):
    t0 = S("result"); yb = 1020
    d.text((X0, 320), "CHANGE", font=F(BLK, 110), fill=INK)
    groups = [("18", .92, .38), ("28", .78, .33), ("38", .66, .28), ("48", .58, .24), ("58", .5, .21), ("68", .44, .18)]
    pk = cue("result", "predicted")
    for i, (age, rep, pre) in enumerate(groups):
        x = X0 + 30 + i * 140
        k1 = ease((t - t0 - .2 - i * .08) / .4); k2 = ease((t - pk - i * .08) / .4)
        d.rectangle([x, yb - 480 * rep * k1, x + 46, yb], fill=INK)
        if k2 > 0: d.rectangle([x + 54, yb - 480 * pre * k2, x + 100, yb], fill=SIG)
        d.text((x + 50, yb + 16), age, font=F(COND, 28), fill=INK, anchor="ma")
    d.line([X0, yb, X1, yb], fill=INK, width=3)
    legend(d, [(INK, "changed (last 10 years)"), (SIG, "will change (next 10)")], y=1086)
    d.text((X1, 1146), "schematic", font=F(MED, 22), fill=MID, anchor="ra")
    fig(d, "fig. 3 — by age")

def sc_name(img, d, t):
    t0 = S("name"); ke = (t - cue("name", "end") + .1) / .35
    if ke > 0:
        for i, (w_, col) in enumerate((("THE END", INK), ("OF HISTORY", INK))):
            k = ease(ke - i * .3)
            if k > 0: d.text((X0 - 8 - (1 - k) * 80, 320 + i * 150), w_, font=F(BLK, 138), fill=mix(BG, col, k))
    ki = ease((t - cue("name", "illusion") + .1) / .4)
    if ki > 0: d.text((X0 - 8, 680), "ILLUSION.", font=F(BLK, 170), fill=mix(BG, SIG, ki))
    if ki > .9:
        note(d, 600, 430, 860, 960, "spoiler: it never ends", (t - cue("name", "illusion") - .4) / .4, INK, anchor="ra")

def ticket(d, x, y, w, h, top, sub, sub2, price_to, k, col):
    if k <= 0: return
    e = ease(k); yy = y + (1 - e) * 80
    d.rectangle([x, yy, x + w, yy + h], fill=col)
    for i in range(int(h / 26)): d.ellipse([x + w - 190 - 7, yy + 12 + i * 26, x + w - 190 + 7, yy + 26 + i * 26], fill=BG)   # perforation
    d.text((x + 30, yy + 26), top, font=F(COND, 30), fill=WHITE)
    d.text((x + 30, yy + 66), sub, font=F(BLK, 46), fill=WHITE)
    d.text((x + 30, yy + 122), sub2, font=F(COND, 34), fill=WHITE)
    for i in range(22): d.line([x + 30 + i * 9, yy + h - 60, x + 30 + i * 9, yy + h - 24], fill=WHITE, width=2 + (i * 7) % 3)
    p = int(price_to * clamp((k - .3) / .7))
    d.text((x + w - 95, yy + h / 2), f"${p}", font=F(BLK, 76), fill=WHITE, anchor="mm")

def sc_band(img, d, t):
    t0 = S("band")
    d.text((X0, 320), "WHAT WOULD YOU PAY?", font=F(BLK, 64), fill=INK)
    ticket(d, X0, 430, X1 - X0, 260, "ADMIT ONE · TODAY", "Your favorite band", "from 10 years ago", 80, (t - cue("band", "eighty") + .3) / .8, INK)
    ticket(d, X0, 740, X1 - X0, 260, "ADMIT ONE · IN 10 YEARS", "Your favorite band", "of today", 129, (t - cue("band", "hundred") + .3) / .8, SIG)
    d.text((X1, 1146), "typical answers", font=F(MED, 22), fill=MID, anchor="ra")
    fig(d, "via New York Times, 2013")

def sc_quote(img, d, t):
    t0 = S("quote")
    d.text((X0 - 10, 300), "“", font=F(BLK, 280), fill=SIG)
    lines = [("At every age,", cue("quote", "at every age")), ("we think we're having", cue("quote", "we think")), ("the last laugh.", cue("quote", "last laugh")),
             ("And at every age,", cue("quote", "and at every")), ("we're wrong.", cue("quote", "wrong") - .2)]
    for i, (l, tk) in enumerate(lines):
        k = ease((t - tk) / .3)
        if k > 0: d.text((X0, 560 + i * 92 + (1 - k) * 30), l, font=F(BLK, 72), fill=mix(BG, SIG if i == 4 else INK, k))
    box_label(d, X0, 1080, "DANIEL GILBERT · HARVARD", 26, WHITE, INK)
    fig(d, "quoted in the New York Times, 2013")

def sc_point(img, d, t):
    t0 = S("point")
    nf = cue("point", "not the final")
    h = picto(d, 300, FLOOR, 1.0, INK, pose=WAVE(t) if t > nf else IDLE); specs(d, h, 1.0)
    box_label(d, 300, 620, "YOU · CURRENT VERSION", 26, WHITE, INK, anchor="ma")
    if t >= nf - .2:
        k = ease((t - nf + .2) / .4)
        d.text((X0 - 8, 300), "NOT FINAL.", font=F(BLK, 160), fill=mix(BG, SIG, k))
        x0, x1, y = 520, X1, 900
        d.text((x0, y - 60), "next version loading", font=F(COND, 30), fill=INK)
        d.rectangle([x0, y, x1, y + 40], outline=INK, width=4)
        p = .1 + .5 * clamp((t - nf) / 2.5)
        d.rectangle([x0 + 6, y + 6, x0 + 6 + (x1 - x0 - 12) * p, y + 34], fill=SIG)
        d.text((x1, y + 56), f"{int(p * 100)} %", font=F(MONO, 24), fill=MID, anchor="ra")
    fig(d, "fig. 4 — work in progress")

EP.scenes = {"hook": sc_hook, "ahead": sc_ahead, "study": sc_study, "result": sc_result, "name": sc_name,
             "band": sc_band, "quote": sc_quote, "point": sc_point}

FX = [(0.0, rewind_sfx(.2, .6), 0), (0.0, thud(.5), 0), (cue("hook", "different"), pop(.18), 0),
      *EP.cut_fx(),
      (cue("ahead", "same"), pop(.18), .3),
      *[(S("study") + .1 + i * .1, tick(.04), (i % 5 - 2) / 4) for i in range(14)],
      (cue("result", "predicted"), thud(.35), 0),
      (cue("name", "end"), thud(.45), 0), (cue("name", "illusion"), thud(.5), 0),
      (cue("band", "eighty"), pop(.2), -.2), (cue("band", "hundred"), pop(.2), .2),
      (cue("quote", "wrong") - .2, thud(.45), 0),
      (cue("point", "not the final") - .2, riser(.6, .1), 0), (cue("point", "not the final"), thud(.5), 0),
      (S("end"), thud(.5), 0)]

if __name__ == "__main__": EP.run(FX)
