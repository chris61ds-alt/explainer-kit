"""NOT JUST YOU – No. 05: the illusion of transparency (Gilovich, Savitsky & Medvec 1998; Savitsky & Gilovich 2003)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from cute import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, gaps={"hook": .6, "no": .7, "name": .6, "study": .7, "best": .4, "told": .7, "you": .8, "end": 2.4})
S, E, cue = TL.S, TL.E, TL.cue
BOX = (60, 320, 900, 1140)
STAGE_Y = 1000

def beat_k(t, bpm=150):
    ph = (t * bpm / 60) % 1
    return math.exp(-ph * 9) + .6 * math.exp(-max(0, ph - .22) * 9) * (ph > .22)

def stage(d, t, spot=1.0):
    card(d, BOX, fill=(60, 48, 96))
    # spotlight cone
    if spot > 0:
        d.polygon([(440, BOX[1]), (520, BOX[1]), (720, STAGE_Y), (240, STAGE_Y)], fill=mix((60, 48, 96), (255, 246, 214), .22 * spot))
        d.ellipse([230, STAGE_Y - 30, 730, STAGE_Y + 30], fill=mix((60, 48, 96), (255, 246, 214), .45 * spot))
    d.rounded_rectangle([BOX[0], STAGE_Y, BOX[2], BOX[3]], radius=56, fill=(150, 112, 190)); d.rectangle([BOX[0], STAGE_Y, BOX[2], STAGE_Y + 40], fill=(150, 112, 190))
    # curtains + valance
    for side in (-1, 1):
        x = BOX[0] if side < 0 else BOX[2]
        d.polygon([(x, BOX[1] + 40), (x - side * 120, BOX[1] + 40), (x - side * 60, STAGE_Y), (x, STAGE_Y)], fill=PINK)
    for i in range(7):
        cx = BOX[0] + 60 + i * 120
        d.pieslice([cx - 60, BOX[1] - 10, cx + 60, BOX[1] + 90], 0, 180, fill=mix(PINK, INK, .15))
    d.rounded_rectangle([BOX[0], BOX[1], BOX[2], BOX[1] + 40], radius=20, fill=mix(PINK, INK, .15))

def mic(d, x, y):
    d.line([x, y, x, y - 230], fill=INK, width=7); d.line([x - 40, y, x + 40, y], fill=INK, width=8)
    d.rounded_rectangle([x - 16, y - 280, x + 16, y - 228], radius=16, fill=INK)

def audience(d, t, cheer=0.0, n=8):
    for i in range(n):
        x = 130 + i * 100
        col = (BEAN, BEAN2, SUN, SKY, PINK, MINT)[i % 6]
        hop = abs(math.sin(t * 9 + i)) * 18 * cheer
        top = BOX[3] - 70 - hop
        d.rounded_rectangle([x - 44, top, x + 44, BOX[3] - 6], radius=44, fill=mix(col, INK, .1)); d.rectangle([x - 44, top + 44, x + 44, BOX[3] - 6], fill=mix(col, INK, .1))
        if cheer > .3 and i % 3 == 0: heart(d, x, top - 40 - (t * 70 + i * 30) % 90, 14, PINK)

def speaker(d, t, nerv=1.0, mood="worried", x=420, s=1.0, wave=0.0):
    jit = math.sin(t * 61) * 6 * nerv
    h = bean(d, x + jit, STAGE_Y, t, s, mood=mood, key=1, look=.3, sweat=nerv, wave=wave)
    return h

def sc_hook(img, d, t):
    stage(d, t)
    racing = t >= cue("hook", "racing") - .2
    h = speaker(d, t, nerv=.9 if t >= cue("hook", "shaking") else .3)
    mic(d, 560, STAGE_Y)
    if racing:
        r = 46 + 26 * beat_k(t) * clamp((t - cue("hook", "racing") + .2) / .3)
        heart(d, 700, 520, r, PINK)
    if t >= cue("hook", "everyone"):
        audience(d, t)
        for i in range(3):
            k = back((t - cue("hook", "everyone") - i * .12) / .3)
            if k > .1: d.text((250 + i * 50, 460 - i * 20), "?", font=F(BLK, 80 * k), fill=SUN, anchor="mm")

def sc_no(img, d, t):
    stage(d, t)
    speaker(d, t, nerv=.2, mood="o"); mic(d, 560, STAGE_Y); audience(d, t)
    k = (t - S("no") + .1) / .35
    sc = back(k)
    if sc > .05:
        d.rounded_rectangle([240 - 40 * sc, 470 - 40 * sc, 720 + 40 * sc, 640 + 40 * sc], radius=60, fill=WHITE)
        d.text((480, 555), "ACTUALLY, NO.", font=F(BLK, int(76 * sc)), fill=PINK, anchor="mm")

def glass_bean(d, x, y, t, s=1.0, fill_k=1.0):
    """see-through bean: outline only, heart visible inside"""
    bw, bh = 120 * s, 170 * s
    top = y - 18 * s - bh
    for side in (-1, 1):
        lx = x + side * 26 * s
        d.rounded_rectangle([lx - 11 * s, y - 34 * s, lx + 11 * s, y], radius=11 * s, fill=mix(SKY, INK, .3))
    d.rounded_rectangle([x - bw / 2, top, x + bw / 2, top + bh], radius=bw / 2, fill=mix(WHITE, SKY, .35), outline=SKY, width=int(7 * s))
    heart(d, x, top + bh * .62, (26 + 10 * beat_k(t)) * s * fill_k, PINK)
    for side in (-1, 1):
        ex = x + side * 24 * s
        d.ellipse([ex - 12 * s, top + bh * .3 - 14 * s, ex + 12 * s, top + bh * .3 + 14 * s], fill=INK)
    return (x, top)

def sc_name(img, d, t):
    card(d, BOX, fill=CARD)
    t0 = S("name")
    k = (t - S("name") - .2) / .4
    for i, (w_, col) in enumerate((("ILLUSION OF", PRIMARY), ("TRANSPARENCY", PINK))):
        kk = back(k - i * .25)
        if kk > .05: d.text((480, 420 + i * 100), w_, font=F(BLK, int(84 * kk)), fill=col, anchor="mm")
    gk = back((t - S("name") - .8) / .4)
    if gk > .05:
        h = glass_bean(d, 480, 1060, t, 1.5 * gk)
        if t >= cue("name", "written"):
            kw = (t - cue("name", "written")) / .3
            for i, lab in enumerate(("nervous!", "shaky!", "panic!")):
                pill(d, (230, 730, 250)[i], (720, 760, 920)[i], lab, WHITE, PINK, size=30, anchor="ma", k=kw - i * .15)

def split_bars(d, t, t0, v_self, v_aud, title, l1, l2, c1=PINK, c2=MINT, y_base=1010, top=560):
    d.text((480, 400), title, font=F(BLK, 44), fill=INK, anchor="mm")
    for i, (v, lab, col) in enumerate(((v_self, l1, c1), (v_aud, l2, c2))):
        x = 270 + i * 420
        k = ease((t - t0 - i * .35) / .6)
        d.rounded_rectangle([x - 100, y_base - (y_base - top) * v * k, x + 100, y_base], radius=34, fill=col)
        d.text((x, y_base + 50), lab, font=F(BLK, 30), fill=INK, anchor="mm")
    d.text((480, 1110), "schematic", font=F(MONO, 20), fill=mix(CARD, INK, .5), anchor="mm")

def sc_study(img, d, t):
    card(d, BOX, fill=CARD)
    t0 = S("study")
    pill(d, 480, 330, "GILOVICH, SAVITSKY & MEDVEC, 1998", PRIMARY, WHITE, size=22, anchor="ma", k=(t - t0) / .3)
    split_bars(d, t, cue("study", "speakers thought") - .1, .95, .4, "how nervous they looked", "SPEAKER'S GUESS", "AUDIENCE SAW")
    if t >= cue("study", "audience"):
        k = (t - cue("study", "audience")) / .3
        pill(d, 690, 700, "far less", WHITE, MINT_D, size=30, anchor="ma", k=k)

def sc_best(img, d, t):
    card(d, BOX, fill=WHITE)
    k = (t - S("best")) / .35
    for i in range(9):
        a = i / 9 * 2 * math.pi + t * .8; r = 260 + 20 * math.sin(t * 4 + i)
        sparkle(d, 480 + math.cos(a) * r, 730 + math.sin(a) * r, 18 * clamp(k), (SUN, PINK, MINT)[i % 3])
    big_number(d, 480, 680, "the best", 110, PRIMARY, k=k)
    big_number(d, 480, 800, "part.", 110, PINK, k=k - .2)

def sc_told(img, d, t):
    stage(d, t)
    t0 = S("told")
    learned = t >= cue("told", "learned") + .2
    calm_k = clamp((t - cue("told", "calmer") + .3) / .6)
    nerv = .9 * (1 - calm_k)
    h = speaker(d, t, nerv=nerv, mood="relieved" if calm_k > .5 else ("o" if learned else "worried"))
    mic(d, 560, STAGE_Y)
    if learned and calm_k < 1:
        kk = back((t - cue("told", "learned") - .2) / .3) * (1 - calm_k)
        if kk > .05:
            d.rounded_rectangle([200, 470 - 70 * kk, 640, 470 + 70 * kk], radius=26, fill=WHITE)
            d.text((420, 450), "the illusion of", font=F(BOLD, int(30 * kk)), fill=PRIMARY, anchor="mm")
            d.text((420, 495), "TRANSPARENCY", font=F(BLK, int(40 * kk)), fill=PINK, anchor="mm")
    if calm_k > .5:
        thought(d, h, (t - cue("told", "calmer")) / .4, s=.7, dx=-90, draw=lambda d_, cx, cy, s: heart(d_, cx, cy + 6 * s, 26 * s, MINT))
    rated = t >= cue("told", "rated")
    audience(d, t, cheer=clamp((t - cue("told", "rated")) / .4) if rated else 0)
    if rated:
        for i in range(5):
            k = back((t - cue("told", "better") + .3 - i * .1) / .3)
            if k > .05: sparkle(d, 600 + i * 56, 460, 22 * k, SUN)
        pill(d, 740, 520, "rated better", SUN, INK, size=28, anchor="ma", k=(t - cue("told", "better")) / .3)

def sc_you(img, d, t):
    card(d, BOX, fill=WALL_B)
    d.rectangle([BOX[0], 1030, BOX[2], 1060], fill=FLOOR); d.rounded_rectangle([BOX[0], 1030, BOX[2], BOX[3]], radius=56, fill=FLOOR)
    h = bean(d, 480, 1030, t, 1.2, mood="happy", key=2, wave=t)
    k = (t - S("you")) / .35
    speech(d, h, "now you know!", k=k, s=1.0, side=1, size=40)
    for i in range(4): sparkle(d, 200 + i * 180, 480 + 40 * math.sin(t * 3 + i), 16, (SUN, PINK)[i % 2])

def draw(img, d, t):
    header(d, 5, "invisible nerves")
    if t < S("no") - .05: sc_hook(img, d, t)
    elif t < S("name") - .05: sc_no(img, d, t)
    elif t < S("study") - .05: sc_name(img, d, t)
    elif t < S("best") - .05: sc_study(img, d, t)
    elif t < S("told") - .05: sc_best(img, d, t)
    elif t < S("you") - .05: sc_told(img, d, t)
    elif t < S("end") - .05: sc_you(img, d, t)
    else: end_card(d, TL, t, sources=("Gilovich, Savitsky & Medvec (1998), JPSP 75(2)", "Savitsky & Gilovich (2003), JESP 39"))
    subtitle(d, TL, t, stop_at=S("end") - .05)

hb_times = []
_t = cue("hook", "racing") - .2
while _t < S("no") - .1: hb_times.append(_t); _t += 60 / 150
FX = [*[(x, heartbeat(.45), 0) for x in hb_times],
      (cue("hook", "everyone"), pop(.15), -.3), (cue("hook", "everyone") + .12, pop(.15), 0), (cue("hook", "everyone") + .24, pop(.15), .3),
      (S("no") - .1, boing(.2), 0),
      (cue("name", "illusion") - .2, softkick(.45), 0), (cue("name", "we think"), pop(.2), 0), (cue("name", "written"), pop(.15), -.3), (cue("name", "written") + .15, pop(.15), .3),
      (cue("study", "speakers thought") - .1, whoosh(.5, .12), -.2), (cue("study", "speakers thought") + .25, whoosh(.4, .1), .2), (cue("study", "audience"), pop(.18), .2),
      (S("best"), chime([523.3, 659.3, 784, 1046.5]), 0),
      (cue("told", "learned") + .2, pop(.2), 0), (cue("told", "calmer") - .3, poof(.15), 0),
      (cue("told", "rated"), chime([392, 523.3, 659.3]), 0), *[(cue("told", "rated") + .1 + i * .11, tick(.05), (i % 5 - 2) / 3) for i in range(14)],
      (S("you"), pop(.2), 0),
      (S("end"), chime([523.3, 659.3, 784, 1046.5, 1318.5], .06), 0)]

if __name__ == "__main__": run(TL, draw, FX)
