"""NOT JUST YOU – No. 03: conversations end at the wrong time (Mastroianni et al., 2021)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from cute import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, gaps={"hook": .5, "other": .6, "study": .4, "two": .7, "split": .7, "catch": .3, "off": .6, "point": .6, "tip": .8, "end": 2.4})
S, E, cue = TL.S, TL.E, TL.cue
BOX = (60, 320, 900, 1140)
LX, RX, FLOOR_Y = 320, 640, 1030

def room(d):
    card(d, BOX, fill=WALL_A)
    d.rounded_rectangle([BOX[0], FLOOR_Y, BOX[2], BOX[3]], radius=56, fill=FLOOR); d.rectangle([BOX[0], FLOOR_Y, BOX[2], FLOOR_Y + 40], fill=FLOOR)
    # window + lamp for a cosy café feel
    d.rounded_rectangle([140, 420, 340, 640], radius=30, fill=(214, 232, 255)); d.line([240, 420, 240, 640], fill=WHITE, width=8)
    d.line([760, 320, 760, 430], fill=PRIMARY, width=4); d.pieslice([700, 410, 820, 490], 180, 360, fill=SUN)
    d.rounded_rectangle([420, 900, 540, FLOOR_Y], radius=14, fill=mix(FLOOR, INK, .25)); d.ellipse([400, 880, 560, 920], fill=WHITE)
    d.rounded_rectangle([458, 860, 482, 890], radius=6, fill=PINK); d.rounded_rectangle([492, 862, 516, 890], radius=6, fill=MINT)

def two_beans(d, t, mood_l="happy", mood_r="happy", talk_turn=True, sweat=0.0, wave=False):
    turn = int(t * 1.3) % 2 if talk_turn else -1
    hl = bean(d, LX, FLOOR_Y, t, 1.0, look=1, mood=mood_l, key=1, talk=(turn == 0), sweat=sweat, wave=t if wave else 0)
    hr = bean(d, RX, FLOOR_Y, t, 1.0, look=-1, mood=mood_r, key=2, color=BEAN2, talk=(turn == 1), sweat=sweat, flip=True, wave=t if wave else 0)
    return hl, hr

def sc_hook(img, d, t):
    room(d)
    leave = t >= cue("hook", "you both want")
    nobody = t >= cue("hook", "nobody")
    hl, hr = two_beans(d, t, "flat" if nobody else "happy", "flat" if nobody else "happy", talk_turn=not nobody, sweat=.8 if nobody else 0)
    if not leave:
        speech(d, hl, "…and then…", k=(t - S("hook")) / .3, s=.9, side=1, size=30)
    else:
        k = (t - cue("hook", "you both want")) / .4
        thought(d, hl, k, s=.8, dx=-40, draw=icon_door); thought(d, hr, k - .15, s=.8, dx=40, draw=icon_door)

def sc_other(img, d, t):
    room(d)
    hl, hr = two_beans(d, t, "happy", "happy")
    k = (t - S("other")) / .4
    hd = lambda d_, cx, cy, s: heart(d_, cx, cy + 6 * s, 30 * s, PINK)
    thought(d, hl, k, s=.8, dx=-40, draw=hd); thought(d, hr, k - .15, s=.8, dx=40, draw=hd)
    for i, (sx, sy) in enumerate(((200, 700), (780, 640), (480, 560))):
        sparkle(d, sx, sy, 14 + 6 * math.sin(t * 7 + i), SUN)

def pair(d, x, y, s, col_l, col_r):
    d.rounded_rectangle([x - 22 * s, y - 34 * s, x - 2 * s, y], radius=10 * s, fill=col_l)
    d.rounded_rectangle([x + 2 * s, y - 34 * s, x + 22 * s, y], radius=10 * s, fill=col_r)

def sc_study(img, d, t):
    card(d, BOX, fill=CARD)
    pill(d, 100, 360, "MASTROIANNI ET AL., 2021 · PNAS", PINK, WHITE, size=24, k=(t - S("study")) / .3)
    n = int(clamp((t - S("study") - .3) / 2.2) * 1058)
    cols = 46
    for i in range(n):
        r, c = divmod(i, cols)
        x, y = 110 + c * 16.4, 470 + r * 16.4
        d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=PRIMARY if i < 806 else MINT)
    if n > 0: big_number(d, 480, 960, f"{n:,}", 140, PRIMARY, k=1)
    d.text((480, 1080), "people asked about their conversations", font=F(BOLD, 30), fill=PRIMARY, anchor="mm")

def sc_two(img, d, t):
    card(d, BOX, fill=CARD)
    k = (t - S("two")) / .5
    for i in range(100):
        r, c = divmod(i, 10)
        x, y = 150 + c * 74, 470 + r * 46
        hit = i in (44, 57) and t >= cue("two", "two percent")
        pair(d, x, y, .9 if not hit else 1.15, MINT if hit else mix(CARD, PRIMARY, .35), MINT if hit else mix(CARD, PRIMARY, .25))
    if t >= cue("two", "two percent"):
        kk = (t - cue("two", "two percent")) / .4
        d.rounded_rectangle([250, 960, 710, 1100], radius=60, fill=WHITE)
        big_number(d, 480, 1030, "≈ 2 %", 110, MINT_D, k=kk)
    pill(d, 480, 360, "ended when BOTH wanted", PRIMARY, WHITE, size=26, anchor="ma", k=k)

def sc_split(img, d, t):
    card(d, BOX, fill=CARD)
    rows = [("both wanted to talk LESS", cue("split", "about half"), 5, PINK, "≈ 1 in 2"),
            ("both wanted MORE", cue("split", "one in ten"), 1, MINT, "≈ 1 in 10")]
    for ri, (label, t0, hits, col, frac) in enumerate(rows):
        y = 480 + ri * 320
        if t < t0 - .1: continue
        d.text((100, y), label, font=F(BLK, 40), fill=INK)
        for i in range(10):
            k = back((t - t0 - i * .05) / .35)
            if k <= .05: continue
            x = 130 + i * 76
            pair(d, x, y + 160, 1.1 * k, col if i < hits else mix(CARD, PRIMARY, .3), col if i < hits else mix(CARD, PRIMARY, .2))
        pill(d, 860, y + 190, frac, col, WHITE, size=28, anchor="ra", k=(t - t0 - .5) / .3)

def sc_catch(img, d, t):
    room(d)
    hl, hr = two_beans(d, t, "o" if t >= cue("catch", "no idea") else "happy", "happy", talk_turn=False)
    if t >= cue("catch", "no idea"):
        k = (t - cue("catch", "no idea")) / .4
        def guess(d_, cx, cy, s):  # left bean imagines the right bean wants to leave
            d_.rounded_rectangle([cx - 46 * s, cy - 40 * s, cx + 46 * s, cy + 40 * s], radius=18 * s, fill=CARD)
            icon_door(d_, cx, cy, s * .8)
        thought(d, hl, k, s=.85, dx=-40, draw=guess)
        thought(d, hr, k - .2, s=.85, dx=40, draw=lambda d_, cx, cy, s: heart(d_, cx, cy + 6 * s, 30 * s, PINK))
        if k > .8:
            pill(d, 250, 590, "THE GUESS", PRIMARY, WHITE, size=26, anchor="ma", k=k - .8)
            pill(d, 700, 590, "THE TRUTH", PINK, WHITE, size=26, anchor="ma", k=k - .9)

def sc_off(img, d, t):
    card(d, BOX, fill=CARD)
    t0 = S("off")
    x0, x1, y = 120, 840, 700
    d.rounded_rectangle([x0, y - 20, x1, y + 20], radius=20, fill=WHITE)
    d.text((x0, y - 70), "0 min", font=F(BOLD, 26), fill=PRIMARY); d.text((x1, y - 70), "end", font=F(BOLD, 26), fill=PRIMARY, anchor="ra")
    gx, wx = x0 + (x1 - x0) * .18, x0 + (x1 - x0) * .82   # schematic positions 64% apart
    kg, kw = ease((t - t0 - .2) / .5), ease((t - t0 - .7) / .5)
    if kg > 0:
        d.polygon([(gx, y - 26), (gx - 18, y - 60), (gx + 18, y - 60)], fill=PRIMARY); pill(d, gx, y + 40, "guess", PRIMARY, WHITE, size=24, anchor="ma", k=kg)
    if kw > 0:
        d.polygon([(wx, y - 26), (wx - 18, y - 60), (wx + 18, y - 60)], fill=PINK); pill(d, wx, y + 40, "what they wanted", PINK, WHITE, size=24, anchor="ma", k=kw)
    if t >= cue("off", "more than half"):
        k = ease((t - cue("off", "more than half")) / .6)
        d.line([gx, y + 140, gx + (wx - gx) * k, y + 140], fill=INK, width=8)
        if k > .95: d.text(((gx + wx) / 2, y + 200), "off by ≈ 64 % of the talk", font=F(BLK, 44), fill=INK, anchor="mm")
    d.text((480, 1080), "schematic — size of the error from the study", font=F(MONO, 20), fill=mix(CARD, INK, .5), anchor="mm")

def sc_point(img, d, t):
    card(d, BOX, fill=WHITE)
    k0 = S("point")
    for i, (w_, col) in enumerate((("NOBODY", PRIMARY), ("CAN SEE", PRIMARY), ("THE EXIT.", PINK))):
        k = back((t - k0 - .2 - i * .15) / .45)
        if k > .05: d.text((110, 400 + i * 160), w_, font=F(BLK, 150 * k), fill=col)
    wob = math.sin(t * 6) * .15
    icon_door(d, 770, 1010, 2.4 + wob)
    sparkle(d, 660, 960, 16, SUN)

def sc_tip(img, d, t):
    room(d)
    said = t >= cue("tip", "just say it")
    relieved = t >= cue("tip", "relieved") - .2
    hl, hr = two_beans(d, t, "happy", "relieved" if relieved else "happy", talk_turn=False, wave=relieved)
    if said: speech(d, hl, "This was lovely! I'll head off.", k=(t - cue("tip", "just say it")) / .35, s=.9, side=1, size=28)
    if relieved:
        for i in range(3): heart(d, RX + 60 + i * 30, 700 - ((t * 80 + i * 40) % 160), 14, PINK)

def draw(img, d, t):
    header(d, 3, "when talks end")
    if t < S("other") - .05: sc_hook(img, d, t)
    elif t < S("study") - .05: sc_other(img, d, t)
    elif t < S("two") - .05: sc_study(img, d, t)
    elif t < S("split") - .05: sc_two(img, d, t)
    elif t < S("catch") - .05: sc_split(img, d, t)
    elif t < S("off") - .05: sc_catch(img, d, t)
    elif t < S("point") - .05: sc_off(img, d, t)
    elif t < S("tip") - .05: sc_point(img, d, t)
    elif t < S("end") - .05: sc_tip(img, d, t)
    else: end_card(d, TL, t, sources=("Mastroianni, Gilbert, Cooney & Wilson (2021),", "PNAS · via Scientific American"))
    subtitle(d, TL, t, stop_at=S("end") - .05)

FX = [(cue("hook", "you both want"), pop(.2), -.2), (cue("hook", "you both want") + .15, pop(.2), .2), (cue("hook", "nobody"), boing(.12), 0),
      (S("other"), chime([523.3, 659.3, 784]), 0),
      (S("study"), pop(.2), 0), *[(S("study") + .3 + i * .08, tick(.04), (i % 7 - 3) / 6) for i in range(28)],
      (cue("two", "two percent"), chime([659.3, 784, 1046.5]), 0),
      (cue("split", "about half"), pop(.2), 0), (cue("split", "one in ten"), pop(.2), 0),
      (cue("catch", "no idea"), boing(.15), 0), (S("off") + .2, pop(.15), -.3), (S("off") + .7, pop(.15), .3),
      (cue("off", "more than half"), whoosh(.5, .15), 0),
      (S("point") + .2, softkick(.5), 0), (S("point") + .5, softkick(.4), 0),
      (cue("tip", "relieved"), chime([392, 523.3, 659.3, 784]), 0),
      (S("end"), chime([523.3, 659.3, 784, 1046.5, 1318.5], .06), 0)]

if __name__ == "__main__": run(TL, draw, FX)
