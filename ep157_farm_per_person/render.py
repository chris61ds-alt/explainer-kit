"""NOT JUST YOU – No. 157: how much farmland feeds one person? ('pour test' riddle, 25.11.2026, bridge to the
self-sufficiency topic). OWID 2024 (FAO, Poore & Nemecek): 48 M km2 farmland, 80 % livestock (17 % of calories),
16 % food crops, 4 % non-food. 48 M km2 / 8.2 bn = ~5,850 m2 = 82 % of a football pitch (105 x 68 m).
Riddle structure (rule 17), dark look. Left: a football pitch seen from above with one person in the centre circle;
right: the world's farmland as one block that splits into 8.2 bn pieces; soil pours into the pitch (82 %), the fill splits
into animals / food crops / other; two stacked bars LAND vs CALORIES. Payoff (rule 15): pitch + bars, the green corner glows."""
import os, sys, math
import numpy as np
from PIL import ImageDraw
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from stand import dashed, payoff_cam, stamp_box
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .4, "rules": .4, "lock": .7, "gut": .5, "reveal": .85, "split": .5, "cal": .6, "why": .1}, pace="loose")
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "rules", "lock", "gut", "reveal", "split", "cal", "why", "end"]
EP = ThreadEpisode(TL, 157, "YOUR FIELD", order=ORDER, dark=True, label="RIDDLE · FAO · OUR WORLD IN DATA",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Our World in Data (2024), based on UN FAO", "and Poore & Nemecek (2018) · global averages"),
                   music=dict(bpm=96, root=0, prog="major", kick="four", audio="v5"),
                   cover=dict(words=["HOW MUCH LAND", "FEEDS ONE", "PERSON?"], kicker="Lock in your answer."))

SOIL, GRASS, GREEN, OTHER = (196, 150, 96), (54, 96, 60), (96, 190, 100), (150, 150, 150)
S_ = 5.4; PX0, PY1 = 110, 1127; PW, PH = 68 * S_, 105 * S_; PY0 = PY1 - PH; PX1 = PX0 + PW
FILL = 5850 / 7140
SH = {"animals": .80, "food": .16, "other": .04}

T_OUT = S("rules") - .2; T_P = T_OUT                          # 25.11.2026 (rule 11): plate first
T_RULE = cue("rules", "split") - .1
T_LOCK = S("lock"); T_321 = [cue("lock", "Three") - .05, cue("lock", "Two") - .05, cue("lock", "One") - .05]
T_GARDEN = S("gut"); T_REV = S("reveal"); T_M2 = cue("reveal", "fifty-nine") - .15; T_PITCH = cue("reveal", "football") - .15
T_SPLIT = S("split") + .1; T_BARS = S("cal") + .05; T_CAL = cue("cal", "seventeen") - .15; T_GLOW = S("why")

def pitch_lines(d, k):
    col = mix(BG, INK, .75 * k)
    d.rectangle([PX0, PY0, PX1, PY1], outline=col, width=3)
    cy = (PY0 + PY1) / 2; d.line([(PX0, cy), (PX1, cy)], fill=col, width=2)
    r = 9.15 * S_; d.ellipse([(PX0 + PX1) / 2 - r, cy - r, (PX0 + PX1) / 2 + r, cy + r], outline=col, width=2)
    for y0, sgn in ((PY0, 1), (PY1, -1)):
        w, h = 40.3 * S_, 16.5 * S_; x = (PX0 + PX1) / 2
        d.rectangle([x - w / 2, min(y0, y0 + sgn * h), x + w / 2, max(y0, y0 + sgn * h)], outline=col, width=2)

def person(d, x, y, s=1.0, col=INK):
    d.ellipse([x - 9 * s, y - 40 * s, x + 9 * s, y - 22 * s], fill=col)
    d.rounded_rectangle([x - 11 * s, y - 20 * s, x + 11 * s, y + 18 * s], radius=int(5 * s), fill=col)

def field(d, t):
    if t < T_REV: return
    u = ease_io(clamp((t - T_REV - .2) / 1.6)); h = PH * FILL * u
    d.rectangle([PX0, PY1 - PH * FILL, PX1, PY1], outline=mix(BG, MID, .5), width=1)
    if h <= 0: return
    if t < T_SPLIT:
        d.rectangle([PX0, PY1 - h, PX1, PY1], fill=SOIL)
    else:
        k = ease_io(clamp((t - T_SPLIT) / .9)); y = PY1
        for key, col in (("animals", SIG), ("food", GREEN), ("other", OTHER)):
            hh = PH * FILL * SH[key]; c = mix(SOIL, col, k)
            if key == "food" and t >= T_GLOW: c = mix(GREEN, (190, 255, 190), .5 + .5 * math.sin((t - T_GLOW) * 6))
            d.rectangle([PX0, y - hh, PX1, y], fill=c); y -= hh
        if k > .6 and t < T_BARS:
            y = PY1
            for key, lab in (("animals", "ANIMALS 80%"), ("food", "FOOD CROPS 16%"), ("other", "OTHER 4%")):
                hh = PH * FILL * SH[key]; yy = y - hh / 2
                d.text((PX1 + 18, yy if key != "other" else yy - 10), lab, font=F(MONO, 24), fill={"animals": SIG, "food": GREEN, "other": OTHER}[key], anchor="lm")
                y -= hh
    R = np.random.RandomState(int(t * 30))                                          # soil stream while filling
    if u < 1:
        for _ in range(140):
            v = R.uniform(); x = (PX0 + PX1) / 2 + R.normal(0, 8 + 30 * v); yy = 470 + (PY1 - h - 470) * v
            d.rectangle([x - 1.5, yy - 1.5, x + 1.5, yy + 1.5], fill=SOIL)

def splitter(d, t):
    """rules: the world's farmland as one block that subdivides (2 -> 4 -> 16 -> ... pieces)"""
    if not (T_RULE - .6 <= t < T_LOCK + .3): return
    x0, y0, w, h = 600, 600, 380, 300
    k = clamp((t - T_RULE) / 1.6); n = int(2 ** (1 + 7 * ease_io(k))) if t >= T_RULE else 1
    cols = int(math.sqrt(n * w / h)) or 1; rows = max(1, n // cols)
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=SOIL)
    for c in range(1, cols): d.line([(x0 + w * c / cols, y0), (x0 + w * c / cols, y0 + h)], fill=BG, width=2)
    for r in range(1, rows): d.line([(x0, y0 + h * r / rows), (x0 + w, y0 + h * r / rows)], fill=BG, width=2)
    d.text((x0 + w / 2, y0 - 30), "ALL FARMLAND · 48M km²", font=F(MONO, 24), fill=MID, anchor="mm")
    d.text((x0 + w / 2, y0 + h + 34), "÷ 8.2 BILLION PEOPLE", font=F(MONO, 24), fill=MID, anchor="mm")

def bars(d, t):
    if t < T_BARS: return
    k = ease_io(clamp((t - T_BARS) / .8)); bx = [690, 880]; H = 520; yb = 1127; w = 120
    for i, (lab, parts) in enumerate((("LAND", (("a", .80, SIG), ("f", .16, GREEN), ("o", .04, OTHER))),
                                      ("CALORIES", (("a", .17, SIG), ("f", .83, GREEN))))):
        y = yb
        if i == 1 and t < T_CAL: continue
        kk = k if i == 0 else ease_io(clamp((t - T_CAL) / .8))
        for key, v, col in parts:
            hh = H * v * kk; d.rectangle([bx[i] - w / 2, y - hh, bx[i] + w / 2, y], fill=col)
            if kk > .9 and v > .1: d.text((bx[i], y - hh / 2), f"{int(v * 100)}%", font=F(BLK, 34), fill=BG if key != "x" else INK, anchor="mm")
            y -= hh
        d.text((bx[i], yb + 30), lab, font=F(MONO, 24), fill=MID, anchor="mm")

def countdown(d, t):
    if not (T_LOCK <= t < S("gut")): return
    d.rounded_rectangle([290, 640, 790, 1040], radius=40, fill=BG)
    d.text((540, 690), "LOCK IN YOUR ANSWER", font=F(BLK, 38), fill=INK, anchor="mm")
    i = sum(1 for x in T_321 if t >= x)
    ring = clamp((t - T_321[0]) / (T_321[2] + .7 - T_321[0])) if t >= T_321[0] else 0
    d.ellipse([420, 750, 660, 990], outline=mix(BG, MID, .6), width=12)
    if ring > 0: d.arc([420, 750, 660, 990], -90, -90 + 360 * (1 - ring), fill=SIG, width=12)
    d.text((540, 870), ["?", "3", "2", "1"][i], font=F(BLK, 130), fill=INK, anchor="mm")

def head(d, line, label=None, val=None, hot=False):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    if label:
        d.text((X0, 400), label, font=F(MONO, 30), fill=MID)
        d.text((X0 + d.textlength(label, font=F(MONO, 30)) + 24, 388), val, font=F(BLK, 56), fill=SIG if hot else INK)

def sc(img, d, t):
    payoff_cam(img, lambda L, dL: sc_full(L, dL, t), t, S("why"), focus=(450, 860), z1=1.12)

def sc_full(img, d, t):
    cur = EP.current(t)
    pk = ease(clamp((t - T_PITCH) / .6)) if t >= T_PITCH else 0
    if pk > 0: d.rectangle([PX0, PY0, PX1, PY1], fill=mix(BG, GRASS, .5 * pk))
    field(d, t)
    if pk > 0: pitch_lines(d, pk)
    cx, cy = (PX0 + PX1) / 2, (PY0 + PY1) / 2 + 20
    if t < T_OUT + .4:                                                               # the plate and its growing field
        o = 1 - ease_io(clamp((t - T_OUT) / .4)); k = spring(clamp((t - .15) / .45)) * o; px, py = 540, 860
        g = 260 * ease_io(clamp((t - .7) / .9)) * o
        if g > 4:
            for a, b in (((px - g, py - g), (px + g, py - g)), ((px + g, py - g), (px + g, py + g)), ((px + g, py + g), (px - g, py + g)), ((px - g, py + g), (px - g, py - g))):
                dashed(d, a, b, mix(BG, SOIL, o), w=4)
        d.ellipse([px - 110 * k, py - 110 * k, px + 110 * k, py + 110 * k], fill=mix(BG, INK, .9 * o)); d.ellipse([px - 80 * k, py - 80 * k, px + 80 * k, py + 80 * k], outline=mix(BG, MID, .6 * o), width=3)
        for i, (dx, dy, c) in enumerate(((-30, -20, GREEN), (25, -25, SIG), (0, 30, SOIL))):
            d.ellipse([px + dx * k - 24 * k, py + dy * k - 18 * k, px + dx * k + 24 * k, py + dy * k + 18 * k], fill=mix(BG, c, o))
        if 1.3 <= t < T_OUT: stamp_box(d, (760, 1140), "YOUR FIELD?", t, 1.3, size=60)
    if t < T_P: pass
    elif t < T_REV: person(d, cx, cy, spring(clamp((t - T_P) / .5)) * 1.6)
    else: person(d, cx, cy, 1.0)
    if t < T_REV and t >= T_P:                                                      # the unknown field around the person
        r = 90 + 12 * math.sin(t * 5); dashed(d, (cx - r, cy - r), (cx + r, cy - r), MID); dashed(d, (cx + r, cy - r), (cx + r, cy + r), MID)
        dashed(d, (cx + r, cy + r), (cx - r, cy + r), MID); dashed(d, (cx - r, cy + r), (cx - r, cy - r), MID)
        d.text((cx, cy - r - 30), "?", font=F(BLK, 50), fill=MID, anchor="mm")
    if T_GARDEN <= t < T_REV + .4:                                                   # gut: a garden (10 x 10 m)
        g = 10 * S_ * ease(clamp((t - T_GARDEN) / .3)); d.rectangle([cx + 40, cy - g, cx + 40 + g, cy], outline=SIG, width=3)
        d.text((cx + 40 + g / 2, cy - g - 26), "A GARDEN?", font=F(BLK, 30), fill=SIG, anchor="mm")
    splitter(d, t); bars(d, t); countdown(d, t)
    if cur == "hook": head(d, "YOUR FIELD?", "LAND PER PERSON", "?")
    elif cur == "rules": head(d, "SPLIT IT FAIRLY.", "PEOPLE", "8.2 BN")
    elif cur == "lock": head(d, "LOCK IT IN.", "LAND PER PERSON", "?")
    elif cur == "gut": head(d, "A GARDEN?", "LAND PER PERSON", "?")
    elif cur == "reveal": head(d, "ALMOST A PITCH.", "LAND PER PERSON", f"{int(5900 * ease_io(clamp((t - T_M2) / .9))):,} m²" if t >= T_M2 else "?", True)
    elif cur == "split": head(d, "80% FOR ANIMALS.", "LAND PER PERSON", "5,900 m²")
    elif cur == "cal": head(d, "= 17% OF CALORIES.", "ANIMAL LAND", "80%", True)
    else: head(d, "THE SMALL CORNER.", "16% OF LAND", "83% OF CALORIES", True)
    fig(d, "global averages · pitch 105 × 68 m · OWID (FAO, Poore & Nemecek)")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.scenes = {k: sc for k in ORDER[:-1]}
FX = [(.15, pop(.12), 0), (.7, whoosh(.8, .015), 0), (1.3, thud(.2), .2), (T_P, pop(.1), 0), (T_RULE, whoosh(1.2, .015), .4), *[(x, thud(.16), 0) for x in T_321], (T_GARDEN, pop(.08), .2),
      (T_REV, whoosh(1.4, .02), -.3), (T_PITCH, pop(.1), -.3), (T_SPLIT, whoosh(.5, .02), 0), (T_BARS, pop(.1), .4), (T_CAL, pop(.1), .5)]
if __name__ == "__main__": EP.run(FX)
