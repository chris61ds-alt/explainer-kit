"""NOT JUST YOU – No. 04: the focusing illusion (Schkade & Kahneman, 1998)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from cute import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, gaps={"hook": .7, "study": .5, "same": .6, "predict": .7, "zoom": .5, "day": .7, "name": .6, "quote": .8, "worry": .8, "end": 2.4})
S, E, cue = TL.S, TL.E, TL.cue
BOX = (60, 320, 900, 1140)

def rain(d, box, t, dens=14, col=RAIN):
    x0, y0, x1, y1 = box
    for i in range(dens):
        x = x0 + 20 + (i * 97) % (x1 - x0 - 40)
        y = y0 + ((t * 420 + i * 131) % (y1 - y0))
        d.line([x, y, x - 6, y + 22], fill=col, width=5)

def sky_card(d, box, sunny, t, k=1.0, label=None):
    x0, y0, x1, y1 = box
    if k <= 0: return
    sc = back(k); cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    w, h = (x1 - x0) * sc / 2, (y1 - y0) * sc / 2
    b = (cx - w, cy - h, cx + w, cy + h)
    d.rounded_rectangle(b, radius=44, fill=(255, 240, 205) if sunny else (222, 226, 240))
    if sc < .8: return
    if sunny:
        icon_sun(d, b[2] - 90, b[1] + 80, 1.3 + .08 * math.sin(t * 4))
    else:
        rain(d, (b[0] + 20, b[1] + 110, b[2] - 20, b[3] - 20), t, 10)
        icon_cloud(d, b[2] - 110, b[1] + 70, 1.6)
    if label: pill(d, b[0] + 30, b[1] + 30, label, PRIMARY if not sunny else (226, 140, 40), WHITE, size=24)

def sc_hook(img, d, t):
    card(d, BOX, fill=(222, 226, 240))
    rain(d, (BOX[0] + 30, BOX[1] + 30, BOX[2] - 30, BOX[3] - 140), t, 16)
    d.rectangle([BOX[0], 1030, BOX[2], 1060], fill=FLOOR); d.rounded_rectangle([BOX[0], 1030, BOX[2], BOX[3]], radius=56, fill=FLOOR)
    # little umbrella over the bean
    d.pieslice([290, 600, 590, 780], 180, 360, fill=PINK); d.line([440, 690, 440, 830], fill=INK, width=6)
    right = t >= cue("hook", "right")
    h = bean(d, 440, 1030, t, 1.05, mood="flat" if not right else "o", key=1, look=.6)
    k = (t - S("hook") - .5) / .4
    def dream(d_, cx, cy, s):
        icon_sun(d_, cx - 20 * s, cy, s * .9); heart(d_, cx + 40 * s, cy + 14 * s, 18 * s, PINK)
    thought(d, h, k, s=.95, dx=180, draw=dream)
    if right: pill(d, 660, 420, "right?", PRIMARY, WHITE, size=40, anchor="ma", k=(t - cue("hook", "right")) / .3)

def sc_study(img, d, t):
    t0 = S("study")
    pill(d, 480, 330, "SCHKADE & KAHNEMAN, 1998", PINK, WHITE, size=24, anchor="ma", k=(t - t0) / .3)
    sky_card(d, (60, 400, 900, 740), False, t, (t - cue("study", "midwest") + .3) / .4, "MIDWEST")
    sky_card(d, (60, 770, 900, 1110), True, t, (t - cue("study", "california") + .2) / .4, "CALIFORNIA")
    n = int(clamp((t - t0 - .4) / 3.0) * 1993)
    for row, (y, col) in enumerate(((680, BEAN), (1050, BEAN2))):
        for i in range(12):
            kk = back((t - t0 - .6 - row * .5 - i * .06) / .3)
            if kk > .1: bean(d, 120 + i * 62, y, t, .32 * kk, key=i + row * 5, color=col, mood="happy")
    if n: d.text((100, 560), f"{n:,} students", font=F(BLK, 60), fill=INK, anchor="lm")

def bars(d, t, t0, vals, labels, cols, y_base=1000, top=520, caption=""):
    for i, (v, lab, col) in enumerate(zip(vals, labels, cols)):
        x = 260 + i * 440
        k = ease((t - t0 - i * .15) / .6)
        hgt = (y_base - top) * v * k
        d.rounded_rectangle([x - 95, y_base - hgt, x + 95, y_base], radius=34, fill=col)
        if i == 0: icon_cloud(d, x, y_base + 60, 1.0)
        else: icon_sun(d, x, y_base + 60, .9)
        d.text((x, y_base + 115), lab, font=F(BLK, 28), fill=INK, anchor="mm")
    if caption: d.text((480, 400), caption, font=F(BLK, 44), fill=INK, anchor="mm")

def sc_same(img, d, t):
    card(d, BOX, fill=CARD)
    bars(d, t, S("same") + .1, (.78, .78), ("MIDWEST", "CALIFORNIA"), (BEAN, BEAN2), caption="how satisfied they WERE")
    if t > S("same") + .9:
        big_number(d, 480, 760, "=", 160, PINK, k=(t - S("same") - .9) / .4)
    d.text((480, 455), "average score 2.79 in both", font=F(MONO, 24), fill=mix(CARD, INK, .55), anchor="mm")

def sc_predict(img, d, t):
    card(d, BOX, fill=CARD)
    bars(d, t, S("predict") + .1, (.55, .95), ("MIDWEST", "CALIFORNIA"), (mix(BEAN, CARD, .3), SUN), caption="what they PREDICTED")
    d.text((480, 455), "both groups guessed the same way", font=F(MONO, 24), fill=mix(CARD, INK, .55), anchor="mm")
    if t > cue("predict", "happier") - .2:
        for i in range(4): sparkle(d, 700 + 60 * math.cos(t * 2 + i * 1.6), 520 + 40 * math.sin(t * 2 + i * 1.6), 14, SUN)

def magnifier(d, cx, cy, r, k=1.0):
    d.line([cx + r * .7, cy + r * .7, cx + r * 1.5, cy + r * 1.5], fill=PRIMARY, width=int(r * .28))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=PRIMARY, width=int(r * .16))

def life_icons(d, t, k_alpha=1.0, sc=1.0, cx=480, cy=730):
    """everything else in a life — drawn around the centre"""
    items = [(-280, -250, "work"), (0, -310, "friends"), (280, -250, "sleep"), (-300, 60, "food"), (300, 60, "family"), (-150, 300, "money"), (150, 300, "health")]
    for i, (ox, oy, lab) in enumerate(items):
        k = back((k_alpha - i * .06) / .5)
        if k > .05: pill(d, cx + ox * sc, cy + oy * sc, lab, WHITE, PRIMARY, size=int(30 * k), anchor="mm" if False else "ma")

def sc_zoom(img, d, t):
    card(d, BOX, fill=CARD)
    t0 = S("zoom"); kz = ease_io((t - cue("zoom", "one thing")) / .9)
    life_icons(d, t, 1 - kz * 1.6)
    s_ = 1.0 + kz * 2.8; cx_ = 480 - kz * 60; cy_ = 730 - kz * 30
    icon_sun(d, cx_, cy_, s_ + .05 * math.sin(t * 4))
    magnifier(d, cx_, cy_, 120 + kz * 150)
    if t >= cue("zoom", "the weather"):
        pill(d, 480, 360, "THE WEATHER", (226, 140, 40), WHITE, size=40, anchor="ma", k=(t - cue("zoom", "the weather")) / .3)

def sc_day(img, d, t):
    card(d, BOX, fill=CARD)
    t0 = S("day")
    # schematic day: 24 blocks, weather is a sliver
    segs = [("sleep", 8, mix(BEAN, CARD, .4)), ("work", 8, BEAN), ("people", 3, PINK), ("weather", .5, SUN), ("food", 2, MINT), ("chores", 2.6, SKY)]
    x0, x1, y = 110, 850, 640
    tot = sum(s[1] for s in segs); x = x0; sx = x0
    kk = ease((t - t0 - .1) / 1.2)
    for i, (lab, v, col) in enumerate(segs):
        w = (x1 - x0) * v / tot
        xe = min(x + w, x0 + (x1 - x0) * kk)
        if lab == "weather": sx = x + w / 2
        if xe > x: d.rectangle([x, y, xe, y + 140], fill=col)
        if kk >= (x + w / 2 - x0) / (x1 - x0) and lab != "weather":
            d.text((x + w / 2, y + 70), lab, font=F(BLK, 26 if w > 90 else 20), fill=WHITE if lab in ("work",) else INK, anchor="mm")
        x += w
    d.rounded_rectangle([x0 - 12, y - 12, x1 + 12, y + 152], radius=40, outline=CARD, width=24)
    d.text((480, 520), "ONE ORDINARY DAY", font=F(BLK, 44), fill=INK, anchor="mm")
    if t >= cue("day", "tiny") - .1:
        k = back((t - cue("day", "tiny") + .1) / .4)
        d.line([sx, y + 150, sx, y + 250], fill=INK, width=5)
        icon_sun(d, sx, y + 300, .9 * k)
        pill(d, sx, y + 360, "the weather", (226, 140, 40), WHITE, size=30, anchor="ma", k=k)
    d.text((480, 1090), "schematic", font=F(MONO, 20), fill=mix(CARD, INK, .5), anchor="mm")

def sc_name(img, d, t):
    card(d, BOX, fill=WHITE)
    t0 = S("name")
    for i, (w_, col) in enumerate((("THE", PRIMARY), ("FOCUSING", PRIMARY), ("ILLUSION.", PINK))):
        k = back((t - cue("name", "focusing") + .4 - i * .15) / .45)
        if k > .05: d.text((110, 420 + i * 150), w_, font=F(BLK, 130 * k), fill=col)
    magnifier(d, 720, 960, 80 + 6 * math.sin(t * 3))
    icon_sun(d, 720, 960, 1.2)

def sc_quote(img, d, t):
    card(d, BOX, fill=CARD)
    t0 = cue("quote", "nothing")
    d.text((120, 300), "“", font=F(BLK, 300), fill=PINK)
    lines = ["Nothing that you", "focus on will make", "as much difference", "as you think."]
    for i, ln in enumerate(lines):
        k = ease((t - t0 - i * .35) / .4)
        if k > 0: d.text((120, 560 + i * 92 + (1 - k) * 30), ln, font=F(BLK, 64), fill=mix(CARD, INK, k))
    k = (t - t0 - 1.8) / .4
    pill(d, 120, 960, "Schkade & Kahneman, 1998", PRIMARY, WHITE, size=26, k=k)

def sc_worry(img, d, t):
    card(d, BOX, fill=WALL_B)
    d.rectangle([BOX[0], 1030, BOX[2], 1060], fill=FLOOR); d.rounded_rectangle([BOX[0], 1030, BOX[2], BOX[3]], radius=56, fill=FLOOR)
    t0 = S("worry"); shrink = ease_io((t - cue("worry", "smaller")) / 1.0)
    calm = shrink > .6
    h = bean(d, 300, 1030, t, 1.05, mood="relieved" if calm else "worried", key=3, look=.8, sweat=0 if calm else .7)
    k = (t - t0 - .1) / .5
    big = 1.9 - shrink * 1.2
    def worry(d_, cx, cy, s):
        icon_cloud(d_, cx, cy - 4 * s, s * 1.3, col=RAIN)
        for i in range(3): d_.line([cx - 20 * s + i * 20 * s, cy + 30 * s, cx - 26 * s + i * 20 * s, cy + 50 * s], fill=RAIN, width=max(2, int(5 * s)))
    thought(d, h, k, s=big, dx=150 - shrink * 60, draw=worry)
    if calm:
        for i in range(3): sparkle(d, 470 + i * 110, 560 + 30 * math.sin(t * 3 + i), 14, SUN)

def draw(img, d, t):
    header(d, 4, "the focusing illusion")
    if t < S("study") - .05: sc_hook(img, d, t)
    elif t < S("same") - .05: sc_study(img, d, t)
    elif t < S("predict") - .05: sc_same(img, d, t)
    elif t < S("zoom") - .05: sc_predict(img, d, t)
    elif t < S("day") - .05: sc_zoom(img, d, t)
    elif t < S("name") - .05: sc_day(img, d, t)
    elif t < S("quote") - .05: sc_name(img, d, t)
    elif t < S("worry") - .05: sc_quote(img, d, t)
    elif t < S("end") - .05: sc_worry(img, d, t)
    else: end_card(d, TL, t, sources=("Schkade & Kahneman (1998), Does living in", "California make people happy? Psych. Science 9(5)"))
    subtitle(d, TL, t, stop_at=S("end") - .05)

FX = [(S("hook") + .5, pop(.2), .2), (cue("hook", "right"), boing(.14), 0),
      (S("study"), pop(.2), 0), (cue("study", "midwest"), whoosh(.3, .12), -.3), (cue("study", "california"), whoosh(.3, .12), .3),
      *[(S("study") + .6 + i * .07, tick(.035), (i % 5 - 2) / 4) for i in range(24)],
      (S("same") + .1, pop(.2), -.2), (S("same") + .25, pop(.2), .2), (S("same") + .9, chime([523.3, 659.3, 784]), 0),
      (S("predict") + .1, pop(.2), -.2), (S("predict") + .25, boing(.12), .2),
      (cue("zoom", "one thing"), whoosh(.6, .18), 0), (cue("zoom", "the weather"), pop(.25), 0),
      (S("day") + .1, whoosh(.9, .1), 0), (cue("day", "tiny"), pop(.2), .3),
      (cue("name", "focusing") - .4, softkick(.45), 0), (cue("name", "focusing") - .1, softkick(.35), 0),
      (cue("quote", "nothing"), chime([392, 523.3, 659.3]), 0),
      (cue("worry", "smaller"), poof(.18), 0), (cue("worry", "smaller") + .7, chime([523.3, 659.3, 784, 1046.5]), 0),
      (S("end"), chime([523.3, 659.3, 784, 1046.5, 1318.5], .06), 0)]

if __name__ == "__main__": run(TL, draw, FX)
