"""'Swiss Detail' toolkit for 'Not just you' (house style since No. 06).
Swiss editorial grid · giant Roboto type · one signal colour (orange) · Aicher-style pictograms with poses ·
line-art props · annotations / dimension lines · numbered chapters · progress rule · orange current-word subtitles ·
dark minimal music bed. Builds on cute.py for Timeline, fonts, easing, sound primitives and the render harness.

Episode usage:
    from swiss import *
    TL = Timeline(HERE, lead=.15, gaps={...})
    EP = Episode(TL, no=7, title="THE BEAUTIFUL MESS", chapters={"hook": "CRINGE", ...}, order=[...])
    def sc_hook(img, d, t): ...
    EP.scenes = {"hook": sc_hook, ...}
    EP.sources = ("Author (Year).", "Journal.")
    EP.run(FX)
"""
import os, sys, math, wave, re
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw
from scipy.signal import resample_poly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cute
from cute import (F, BLK, BOLD, MONO, clamp, ease, ease_io, back, lerp, mix, Timeline, W, H, SR, FPS, SAFE_R, SAFE_B,
                  tt_, bp, lp, softkick, whoosh, pop, tick, heartbeat, poof)

V4 = os.environ.get("NJY_FX") == "v4"          # test 31.10.2026: impulse beat (number pulses) – carry-over lives in ThreadEpisode
V3 = os.environ.get("NJY_STYLE", "v3") == "v3"   # default since 31.10.2026 (NJY_STYLE=v2 = old look): orange only for the answer, whip transitions, new sound

# ---------------------------------------------------------------- palette + type
COND, MED = "Roboto-Condensed-Bold.woff", "Roboto-Medium.woff"
BG = (250, 250, 248); INK = (12, 12, 12); SIG = (255, 64, 0); RULE = (226, 226, 222); MID = (140, 140, 136)
SIG_L = (255, 222, 208); WHITE = (255, 255, 255)
X0, X1, Y_TOP, Y1 = 60, 900, 300, 1170          # content frame (inside Instagram safe zones)
FLOOR = 1128                                    # default feet line for pictograms
cute.BG, cute.INK = BG, INK

# ---------------------------------------------------------------- Aicher-style pictogram
def seg(d, a, b, w, col):
    d.line([a, b], fill=col, width=int(w)); r = w / 2
    for p in (a, b): d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=col)

def picto(d, x, y=FLOOR, s=1.0, col=INK, f=1, tilt=0.0, arms=None, legs=None, head_dy=0.0, pose=None):
    """Pictogram figure. (x, y) = feet line. Angles in degrees from straight down, positive = towards facing f (±1).
    arms: ((upper, fore) front, (upper, fore) back) · legs likewise · tilt leans the torso · pose: dict with any of these.
    Returns the head centre."""
    if pose: arms, legs, tilt = pose.get("arms", arms), pose.get("legs", legs), pose.get("tilt", tilt)
    arms = arms or IDLE["arms"]; legs = legs or ((4, 0), (-4, 0))
    L_leg, L_t, L_u, L_f = 70 * s, 130 * s, 62 * s, 58 * s
    def v(a, L): r = math.radians(a); return (math.sin(r) * f * L, math.cos(r) * L)
    hip = (x, y - 2 * L_leg)
    for (a1, a2) in legs:
        k = (hip[0] + v(a1, L_leg)[0], hip[1] + v(a1, L_leg)[1]); ft = (k[0] + v(a2, L_leg)[0], k[1] + v(a2, L_leg)[1])
        seg(d, hip, k, 42 * s, col); seg(d, k, ft, 42 * s, col)
    tr = math.radians(tilt); neck = (hip[0] + math.sin(tr) * f * L_t, hip[1] - math.cos(tr) * L_t)
    seg(d, hip, neck, 66 * s, col)
    sh = (neck[0], neck[1] + 14 * s)
    for (a1, a2) in arms:
        e = (sh[0] + v(a1, L_u)[0], sh[1] + v(a1, L_u)[1]); h = (e[0] + v(a2, L_f)[0], e[1] + v(a2, L_f)[1])
        seg(d, sh, e, 36 * s, col); seg(d, e, h, 36 * s, col)
    hc = (neck[0] + math.sin(tr) * f * 82 * s, neck[1] - 82 * s + head_dy * s)
    d.ellipse([hc[0] - 42 * s, hc[1] - 42 * s, hc[0] + 42 * s, hc[1] + 42 * s], fill=col)
    return hc

# poses (dicts) – animated ones are functions of t
IDLE = {"arms": ((15, 40), (-10, -5))}
WORRY = {"arms": ((165, 250), (-15, -5))}                         # one hand to the head
FACEPALM = {"arms": ((150, 250), (140, 245)), "tilt": 10}          # both hands to the face
LAUGH = {"arms": ((40, 120), (-30, -60)), "tilt": -8}
SHRUG = {"arms": ((60, 160), (-60, -160))}
OPEN = {"arms": ((70, 110), (-70, -110))}                         # arms open, welcoming
SIT = {"legs": ((90, 0), (86, 2))}                                 # combine with chair(); feet line = seat + 140
def TALK(t, ph=0.0): a = math.sin(t * 5 + ph); return {"arms": ((60 + 22 * a, 110 + 25 * a), (-12, -6))}
def WAVE(t): return {"arms": ((125, 165 + 30 * math.sin(t * 9)), (-10, -5))}
def SING(t): a = math.sin(t * 3); return {"arms": ((95 + 10 * a, 120), (-70 - 10 * a, -100)), "tilt": -6}
def WALK(t, speed=6): a = math.sin(t * speed); return {"arms": ((25 * a, 20), (-25 * a, -10)), "legs": ((22 * a, 0), (-22 * a, 0))}
def merge(*ps):
    out = {}
    for p in ps: out.update(p)
    return out

def _pz(p, t): return p(t) if callable(p) else p
def blend(a, b, k):
    """interpolate two poses (arms, legs, tilt)"""
    out = {}
    for key, default in (("arms", IDLE["arms"]), ("legs", ((4, 0), (-4, 0)))):
        A, B = a.get(key, default), b.get(key, default)
        out[key] = tuple(tuple(lerp(x, y, k) for x, y in zip(pa, pb)) for pa, pb in zip(A, B))
    out["tilt"] = lerp(a.get("tilt", 0), b.get("tilt", 0), k)
    return out
def pose_seq(t, keys, dur=.35):
    """keys: [(t0, pose_or_fn), ...] ascending – poses morph smoothly (dur) instead of snapping"""
    cur = _pz(keys[0][1], t)
    for tk, p in keys[1:]:
        if t >= tk: cur = blend(cur, _pz(p, t), ease_io((t - tk) / dur))
    return cur
def move(t, keys, dur=.6):
    """keys: [(t0, x), ...] – position that glides between key values"""
    x = keys[0][1]
    for tk, v in keys[1:]:
        if t >= tk: x = lerp(x, v, ease_io((t - tk) / dur))
    return x

# ---------------------------------------------------------------- props (line art)
def cup(d, x, y, t, s=1.0, steam=True):
    d.rectangle([x - 22 * s, y - 44 * s, x + 22 * s, y], outline=INK, width=int(6 * s))
    d.arc([x + 12 * s, y - 36 * s, x + 40 * s, y - 12 * s], 270, 90, fill=INK, width=int(6 * s))
    if steam:
        for i in (-1, 1):
            pts = [(x + i * 8 * s + 6 * s * math.sin(t * 4 + j * .7 + i), y - 56 * s - j * 10 * s) for j in range(6)]
            d.line(pts, fill=MID, width=int(4 * s))

def table(d, cx, y, w=380):
    d.line([cx - w / 2, y, cx + w / 2, y], fill=INK, width=10); d.line([cx, y, cx, y + 160], fill=INK, width=10)
    d.line([cx - 70, y + 160, cx + 70, y + 160], fill=INK, width=10)

def chair(d, x, y, f=1):
    """seat at height y, backrest behind (opposite of facing f)"""
    d.line([x - 60, y, x + 60, y], fill=INK, width=10)
    bx = x - f * 60; d.line([bx, y, bx, y - 150], fill=INK, width=10)
    d.line([x - 50, y, x - 50, y + 140], fill=INK, width=8); d.line([x + 50, y, x + 50, y + 140], fill=INK, width=8)

def mic(d, x, y, h=230):
    d.line([x, y, x, y - h], fill=INK, width=7); d.line([x - 40, y, x + 40, y], fill=INK, width=8)
    d.rounded_rectangle([x - 16, y - h - 50, x + 16, y - h + 2], radius=16, fill=INK)

def phone(d, cx, cy, s=1.0, col=INK, lit=False):
    d.rounded_rectangle([cx - 46 * s, cy - 84 * s, cx + 46 * s, cy + 84 * s], radius=14 * s, outline=col, width=int(7 * s), fill=SIG_L if lit else None)
    d.line([cx - 14 * s, cy + 66 * s, cx + 14 * s, cy + 66 * s], fill=col, width=int(5 * s))

def door(d, x, y, h=300, open_k=0.0):
    d.rectangle([x, y - h, x + 150, y], outline=INK, width=8)
    w = 150 * (1 - .7 * ease(open_k)); d.polygon([(x, y - h), (x + w, y - h + 20 * open_k), (x + w, y - 20 * open_k), (x, y)], fill=INK)

def stage(d, y=FLOOR):
    d.rectangle([X0, y, X1, y + 14], fill=INK)
    for i in range(6): d.line([X0 + 20 + i * 150, y + 14, X0 + 20 + i * 150, Y1], fill=RULE, width=2)

def spotlight(d, cx, y=FLOOR, top=Y_TOP + 40, w=260):
    d.polygon([(cx - 40, top), (cx + 40, top), (cx + w, y), (cx - w, y)], fill=(242, 241, 236))

def speech_box(d, x, y, w, k, col=INK, side=1, txt="· · ·", size=36):
    if k <= 0: return
    e = ease(k); ww = w * e; x0 = x if side > 0 else x - ww
    d.rectangle([x0, y, x0 + ww, y + 70], fill=col)
    tx = x + 24 * side; d.polygon([(tx, y + 70), (tx + 24 * side, y + 70), (tx, y + 96)], fill=col)
    if e > .9: d.text((x0 + ww / 2, y + 35), txt, font=F(BLK, size), fill=WHITE, anchor="mm")

def think_box(d, head, w, h, k, txt="", col=INK, side=1, fg=WHITE, size=34):
    """square thought box with three stepping squares towards the head"""
    if k <= 0: return None
    e = ease(k); hx, hy = head
    for i, r in enumerate((8, 12, 16)):
        cx, cy = hx + side * (30 + i * 28), hy - 60 - i * 30
        if e > .2 + i * .2: d.rectangle([cx - r, cy - r, cx + r, cy + r], fill=col)
    x0 = hx + side * 60 - (0 if side > 0 else w * e); y0 = hy - 160 - h * e
    d.rectangle([x0, y0, x0 + w * e, y0 + h * e], fill=col)
    if e > .9 and txt: d.text((x0 + w / 2, y0 + h / 2), txt, font=F(BLK, size), fill=fg, anchor="mm")
    return (x0, y0, x0 + w * e, y0 + h * e)

# ---------------------------------------------------------------- annotation / data
def cross(d, x, y, r=12): d.line([x - r, y, x + r, y], fill=INK, width=2); d.line([x, y - r, x, y + r], fill=INK, width=2)

def note(d, x, y, tx, ty, text, k=1.0, col=INK, anchor="la", size=28):
    """annotation: dot at (x, y), leader line to (tx, ty), text there"""
    if k <= 0: return
    e = ease(k); ex, ey = lerp(x, tx, e), lerp(y, ty, e)
    d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=col); d.line([x, y, ex, ey], fill=col, width=3)
    if k > .9: d.text((tx + (10 if anchor == "la" else -10), ty), text, font=F(COND, size), fill=col, anchor="lm" if anchor == "la" else "rm")

def box_label(d, x, y, text, size, fg=WHITE, bg=INK, font=COND, anchor="la"):
    f = F(font, size); w = d.textlength(text, font=f)
    if anchor == "ma": x -= w / 2
    if anchor == "ra": x -= w
    d.rectangle([x - 10, y - 4, x + w + 10, y + size + 8], fill=bg); d.text((x, y), text, font=f, fill=fg)

def dim_h(d, a, b, y, k=1.0, col=SIG, label=None, size=26, arrows=False):
    """horizontal dimension line from a to b at y (grows with k), end ticks, optional label box below"""
    if k <= 0: return
    e = ease(k); bb = a + (b - a) * e
    d.line([a, y, bb, y], fill=col, width=4); d.line([a, y - 16, a, y + 16], fill=col, width=4)
    if e > .95:
        d.line([b, y - 16, b, y + 16], fill=col, width=4)
        if arrows:
            d.polygon([(a, y), (a + 16, y - 10), (a + 16, y + 10)], fill=col); d.polygon([(b, y), (b - 16, y - 10), (b - 16, y + 10)], fill=col)
        if label: box_label(d, (a + b) / 2, y + 22, label, size, WHITE, col, anchor="ma")

def dim_v(d, x, a, b, k=1.0, col=SIG, label=None, size=26):
    if k <= 0: return
    e = ease(k); bb = a + (b - a) * e
    d.line([x, a, x, bb], fill=col, width=4); d.line([x - 16, a, x + 16, a], fill=col, width=4)
    if e > .95:
        d.line([x - 16, b, x + 16, b], fill=col, width=4)
        if label: box_label(d, x + 24, (a + b) / 2 - size / 2, label, size, WHITE, col)

def ruler(d, y, x0, x1, labels, minor=60):
    d.line([x0, y, x1, y], fill=INK, width=3); major = minor // (len(labels) - 1)
    for i in range(0, minor + 1):
        x = x0 + (x1 - x0) * i / minor; h = 18 if i % major == 0 else 8
        d.line([x, y, x, y + h], fill=INK, width=2)
        if i % major == 0: d.text((x, y + 26), labels[i // major], font=F(MONO, 20), fill=MID, anchor="ma")

def scale7(d, x, y, sel, k, col, size=92, gap=20):
    for i in range(7):
        bx = x + i * (size + gap); fill = col if (i + 1) <= sel * k else None
        d.rectangle([bx, y, bx + size, y + size], outline=INK, width=4, fill=fill)
        d.text((bx + size / 2, y + size / 2), str(i + 1), font=F(COND, 34), fill=WHITE if fill else INK, anchor="mm")

def hbar(d, y, v, k, col, label=None, h=90, x0=X0, x1=X1):
    d.rectangle([x0, y, x0 + (x1 - x0) * v * ease(k), y + h], fill=col)
    if label: d.text((x0, y + h + 12), label, font=F(COND, 28), fill=INK)

def axis_ticks(d, y, n=8, x0=X0, x1=X1):
    d.line([x0, y, x1, y], fill=INK, width=2)
    for i in range(n): x = x0 + (x1 - x0) * i / (n - 1); d.line([x, y, x, y + 14], fill=INK, width=2)

def giant(d, text, y=Y_TOP, size=230, col=INK, k=1.0, x=X0 - 8, slide=100):
    """big headline word; k animates a slide-in"""
    if k <= 0: return
    e = ease(k); d.text((x - (1 - e) * slide, y), text, font=F(BLK, size), fill=mix(BG, col, e))

def fig(d, text): d.text((X0, 1146), text, font=F(MED, 22), fill=MID)

def legend(d, items, y=1100):
    x = X0
    for col, lab in items:
        d.rectangle([x, y, x + 22, y + 22], fill=col); d.text((x + 32, y + 11), lab, font=F(COND, 24), fill=INK, anchor="lm")
        x += 60 + d.textlength(lab, font=F(COND, 24))

# ---------------------------------------------------------------- more props (line art, Swiss)
def camera(d, cx, cy, s=1.0, col=INK, flash=0.0):
    d.rectangle([cx - 70 * s, cy - 44 * s, cx + 70 * s, cy + 50 * s], fill=col)
    d.rectangle([cx - 30 * s, cy - 62 * s, cx + 10 * s, cy - 44 * s], fill=col)
    d.ellipse([cx - 32 * s, cy - 26 * s, cx + 32 * s, cy + 38 * s], fill=WHITE); d.ellipse([cx - 20 * s, cy - 14 * s, cx + 20 * s, cy + 26 * s], fill=col)
    if flash > 0:
        for i in range(8):
            a = i / 8 * 2 * math.pi; r0, r1 = 90 * s, (90 + 60 * flash) * s
            d.line([cx + math.cos(a) * r0, cy + math.sin(a) * r0, cx + math.cos(a) * r1, cy + math.sin(a) * r1], fill=SIG, width=int(6 * s))

def frame_art(d, x0, y0, x1, y1, kind=0, col=INK):
    """framed artwork on a wall: 0 circle, 1 triangle, 2 bars"""
    d.rectangle([x0, y0, x1, y1], outline=col, width=8); d.rectangle([x0 + 18, y0 + 18, x1 - 18, y1 - 18], outline=RULE, width=3)
    cx, cy, w = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) * .28
    if kind == 0: d.ellipse([cx - w, cy - w, cx + w, cy + w], fill=SIG)
    elif kind == 1: d.polygon([(cx, cy - w), (cx + w, cy + w), (cx - w, cy + w)], fill=INK)
    else:
        for i in range(3): d.rectangle([cx - w + i * w * .75, cy - w + i * 14, cx - w + i * w * .75 + w * .5, cy + w], fill=SIG if i == 1 else INK)

def clock(d, cx, cy, r, t=0.0, minutes=None, col=INK, speed=1.0):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=int(max(4, r * .08)))
    for i in range(12):
        a = i / 12 * 2 * math.pi; d.line([cx + math.cos(a) * r * .82, cy + math.sin(a) * r * .82, cx + math.cos(a) * r * .92, cy + math.sin(a) * r * .92], fill=col, width=int(max(2, r * .04)))
    m = minutes if minutes is not None else t * 60 * speed
    am = math.radians(m / 60 * 360 - 90); ah = math.radians(m / 720 * 360 - 90)
    d.line([cx, cy, cx + math.cos(ah) * r * .5, cy + math.sin(ah) * r * .5], fill=col, width=int(max(4, r * .09)))
    d.line([cx, cy, cx + math.cos(am) * r * .78, cy + math.sin(am) * r * .78], fill=SIG, width=int(max(3, r * .05)))
    d.ellipse([cx - r * .07, cy - r * .07, cx + r * .07, cy + r * .07], fill=col)

def bed(d, x0, y, w=420, col=INK):
    d.rectangle([x0, y - 90, x0 + w, y - 40], fill=col); d.rectangle([x0, y - 170, x0 + 20, y], fill=col)
    d.rectangle([x0 + w - 20, y - 120, x0 + w, y], fill=col); d.rounded_rectangle([x0 + 30, y - 130, x0 + 130, y - 90], radius=18, fill=RULE)

def credit_card(d, cx, cy, s=1.0, col=INK, rot=0):
    w, h = 220 * s, 140 * s
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=14 * s, fill=col)
    d.rectangle([cx - w / 2 + 20 * s, cy - h / 2 + 30 * s, cx - w / 2 + 60 * s, cy - h / 2 + 60 * s], fill=SIG)
    for i in range(4): d.rectangle([cx - w / 2 + 20 * s + i * 46 * s, cy + 20 * s, cx - w / 2 + 56 * s + i * 46 * s, cy + 30 * s], fill=WHITE)

def banknote(d, cx, cy, s=1.0, value="50", col=INK):
    w, h = 240 * s, 120 * s
    d.rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], fill=WHITE, outline=col, width=int(5 * s))
    d.ellipse([cx - 34 * s, cy - 34 * s, cx + 34 * s, cy + 34 * s], outline=col, width=int(4 * s))
    d.text((cx - w / 2 + 14 * s, cy - h / 2 + 8 * s), value, font=F(BLK, int(34 * s)), fill=col)
    d.text((cx + w / 2 - 14 * s, cy + h / 2 - 8 * s), value, font=F(BLK, int(34 * s)), fill=col, anchor="rd")

def coin(d, cx, cy, r=30, col=INK, label="1"):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE, outline=col, width=5)
    d.text((cx, cy), label, font=F(BLK, int(r)), fill=col, anchor="mm")

def note_icon(d, x, y, s=1.0, col=INK):
    d.ellipse([x - 22 * s, y - 14 * s, x + 14 * s, y + 14 * s], fill=col); d.line([x + 12 * s, y, x + 12 * s, y - 80 * s], fill=col, width=int(7 * s))
    d.polygon([(x + 12 * s, y - 80 * s), (x + 46 * s, y - 60 * s), (x + 46 * s, y - 44 * s), (x + 12 * s, y - 62 * s)], fill=col)

def headphones(d, h, s=1.0, col=INK):
    d.arc([h[0] - 56 * s, h[1] - 64 * s, h[0] + 56 * s, h[1] + 40 * s], 190, 350, fill=col, width=int(10 * s))
    for sx in (-1, 1): d.rectangle([h[0] + sx * 54 * s - 13 * s, h[1] - 14 * s, h[0] + sx * 54 * s + 13 * s, h[1] + 24 * s], fill=col)

def waveform(d, x0, x1, y, t, amp=60, col=INK, prog=1.0, seed=1, n=90):
    for i in range(n):
        u = i / (n - 1); x = x0 + (x1 - x0) * u
        a = amp * (.25 + .75 * abs(math.sin(i * 1.7 + seed) * math.sin(i * .43 + seed * .3)))
        d.rectangle([x - 2.5, y - a, x + 2.5, y + a], fill=col if u <= prog else RULE)

def eye(d, x, y, s=1.0, col=INK, open_k=1.0, look=(0, 0)):
    h = 26 * s * open_k
    d.chord([x - 44 * s, y - h, x + 44 * s, y + h], 0, 360, fill=WHITE, outline=col, width=int(5 * s))
    if open_k > .3:
        px, py = x + look[0] * 14 * s, y + look[1] * 8 * s
        d.ellipse([px - 14 * s, py - 14 * s, px + 14 * s, py + 14 * s], fill=col)
    else: d.line([x - 44 * s, y, x + 44 * s, y], fill=col, width=int(5 * s))

# ---------------------------------------------------------------- generic scene helpers
def words_in(d, t, items, x=X0 - 8, slide=80):
    """items: [(text, t_in, y, size, col)] – headline words that slide + fade in"""
    for text, tk, y, size, col in items:
        k = ease((t - tk) / .35)
        if k > 0: d.text((x - (1 - k) * slide, y), text, font=F(BLK, size), fill=mix(BG, col, k))

def counter(d, x, y, t, t0, dur, to, fmt="{:,.0f}", size=200, col=SIG, anchor="la"):
    v = to * ease_io((t - t0) / dur)
    if t >= t0: d.text((x, y), fmt.format(v), font=F(BLK, size), fill=col, anchor=anchor)

def actors_layer(order, S, specs, slide=.55):
    """specs: [dict(col, f, tg={scene: (x, s, dy)}, poses=[(t, pose)], acc=fn(d, head, s) or None)] → layer fn.
    Actors glide between scene targets; dy >= 650 hides them below the frame."""
    heads = {}
    def layer(img, d, t, cur):
        i = order.index(cur); prev = order[max(0, i - 1)]
        k = ease_io((t - S(cur) + .05) / slide) if i else 1
        for j, sp in enumerate(specs):
            tg = sp["tg"]; a, b = tg.get(prev, tg.get(cur)), tg.get(cur)
            if b is None: continue
            x, sc, dy = (lerp(p, q, k) for p, q in zip(a, b))
            if dy >= 650 or sc <= .05: continue
            h = picto(d, x, FLOOR + dy, sc, sp.get("col", INK), f=sp.get("f", 1), pose=pose_seq(t, sp["poses"]))
            if sp.get("acc"): sp["acc"](d, h, sc)
            heads[j] = h
    layer.heads = heads
    return layer

# ---------------------------------------------------------------- sound: dark minimal bed + sfx
def rewind_sfx(amp=.22, dur=.55):
    t = tt_(dur); f = 2400 * np.exp(-t * 4.5) + 200
    return amp * (np.sin(2 * np.pi * np.cumsum(f) / SR) * .5 + bp(np.random.default_rng(5).standard_normal(len(t)), 800, 5000)) * np.sin(np.pi * t / dur) ** .5
def thud(amp=.45): return softkick(amp)
def snare(amp=.05):
    t = tt_(.18); return amp * bp(np.random.default_rng(9).standard_normal(len(t)), 900, 3500) * np.exp(-t * 22)
def riser(dur=.8, amp=.12):
    t = tt_(dur); return amp * bp(np.random.default_rng(3).standard_normal(len(t)), 1200, 6000) * (t / dur) ** 2
def boom(amp=.55, dur=.9):
    """sub drop for a reveal: pitch falls from ~100 Hz to 38 Hz"""
    t = tt_(dur); f = 38 + 62 * np.exp(-t * 18)
    return amp * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.5) * np.minimum(1, t / .005)
def hat(amp=.012):
    t = tt_(.05); return amp * bp(np.random.default_rng(11).standard_normal(len(t)), 7000, 15000) * np.exp(-t * 90)
def voice_polish(vo):
    """v3: high-pass, gentle compression, a little presence and warmth"""
    from scipy.signal import butter as _b, lfilter as _l
    b, a = _b(2, 90 / (SR / 2), "high"); x = _l(b, a, vo)
    env = np.sqrt(np.convolve(x * x, np.ones(int(.03 * SR)) / int(.03 * SR), "same")) + 1e-6
    ref = np.percentile(env[env > env.max() * .05], 90) if (env > env.max() * .05).any() else env.max()
    g = np.where(env > ref * .5, (env / (ref * .5)) ** (1 / 3 - 1), 1.0)       # 3:1 above the knee
    x = x * g
    x = x + .25 * bp(x, 2500, 6000) + .12 * lp(x, 300)
    return np.tanh(x / (np.abs(x).max() + 1e-9) * 1.2) * np.abs(vo).max()

PROGS = {   # (root offset in semitones, quality)
    "minor": [(0, "m"), (-4, "M"), (3, "M"), (-2, "M")],      # i  VI  III VII
    "major": [(0, "M"), (7, "M"), (9, "m"), (5, "M")],        # I  V   vi  IV
    "warm":  [(0, "M"), (9, "m"), (5, "M"), (7, "M")],        # I  vi  IV  V
    "dream": [(0, "M"), (5, "M"), (9, "m"), (4, "m")],        # I  IV  vi  iii
    "tense": [(0, "m"), (-2, "M"), (-4, "M"), (-5, "M")],     # i  VII VI  V
}
MUSIC = dict(bpm=96, root=0, prog="minor", kick="half", gaps=())

def _chord(root_hz, q):
    third = 3 if q == "m" else 4
    return [root_hz, root_hz * 2 ** (third / 12), root_hz * 2 ** (7 / 12)]

def build_audio(TL_, fx_cues, path, bpm=None, music_gaps=()):
    """dark minimal bed (pad + sub + soft kick/snare) in the episode's key/tempo; music_gaps = hard silences (e.g. before a reveal)"""
    M = dict(MUSIC); bpm = bpm or M["bpm"]; gaps = list(M.get("gaps", ())) + list(music_gaps)
    n = int((TL_.total + 1) * SR); vo = np.zeros(n); mus = np.zeros((n, 2)); fx = np.zeros((n, 2))
    def put(buf, x, t0, pan=0.):
        s = int(t0 * SR)
        if s < 0 or s >= n: return
        e = min(n, s + len(x)); x = x[:e - s]
        if buf.ndim == 1: buf[s:e] += x
        else: buf[s:e, 0] += x * (1 - max(0, pan)); buf[s:e, 1] += x * (1 + min(0, pan))
    for m in TL_.meta:
        a, sr = sf.read(os.path.join(TL_.dir, "vo", m["id"] + ".wav")); put(vo, resample_poly(a, SR, sr), TL_.T[m["id"]]["start"])
    beat = 60 / bpm; bar = beat * 4; base = 220.0 * 2 ** (M["root"] / 12)
    prog = [_chord(base * 2 ** (o / 12) if o >= -5 else base * 2 ** ((o + 12) / 12), q) for o, q in PROGS[M["prog"]]]
    tb, i = 0.0, 0
    while tb < TL_.total - .3:
        ch = prog[i % 4]
        t_ = tt_(bar); env = np.minimum(1, t_ / .4) * np.exp(-t_ * .35)
        pad = sum(np.sin(2 * np.pi * f * t_ + j) for j, f in enumerate(ch)) * env * .018
        put(mus, lp(pad, 1800), tb, -.15); put(mus, lp(pad, 1800), tb + .01, .15)
        put(mus, .07 * np.sin(2 * np.pi * ch[0] / 2 * t_) * np.exp(-t_ * 1.2), tb)
        for b_ in range(4):
            if M["kick"] == "four" or b_ in (0, 2): put(mus, softkick(.3), tb + b_ * beat)
            if M["kick"] != "four" and b_ in (1, 3): put(mus, snare(.035), tb + b_ * beat)
            if M["kick"] == "four" and b_ in (1, 3): put(mus, snare(.03), tb + b_ * beat + beat / 2)
        if V3:                                       # momentum: soft hats on 8ths + a quiet arp from the chord
            for e in range(8):
                put(mus, hat(.014 if e % 2 else .008), tb + e * beat / 2, (.3 if e % 2 else -.3))
                put(mus, lp(.022 * np.sin(2 * np.pi * ch[e % 3] * 2 * tt_(.22)) * np.exp(-tt_(.22) * 14), 3000), tb + e * beat / 2, (-.2 if e % 2 else .2))
        tb += bar; i += 1
    if V3: vo = voice_polish(vo)
    gate = np.ones(n); fdur = int(.06 * SR)
    for a_, b_ in gaps:
        s0, s1 = int(a_ * SR), int(b_ * SR); gate[s0:s1] = 0
        gate[max(0, s0 - fdur):s0] = np.linspace(1, 0, s0 - max(0, s0 - fdur)); gate[s1:s1 + fdur] = np.linspace(0, 1, len(gate[s1:s1 + fdur]))
    mus *= gate[:, None]
    for (t0, sig, pan) in fx_cues: put(fx, sig, t0, pan)
    env = np.convolve(np.abs(vo), np.ones(int(.12 * SR)) / int(.12 * SR), "same")
    duck = (1 - .55 * np.clip(env / (env.max() * .15 + 1e-9), 0, 1))[:, None]
    st = (vo[:, None] + mus * duck + fx)[: int(TL_.total * SR)]
    st /= np.abs(st).max() / .9
    fd = int(.35 * SR); st[-fd:] *= np.linspace(1, 0, fd)[:, None]
    with wave.open(path, "wb") as w_:
        w_.setnchannels(2); w_.setsampwidth(2); w_.setframerate(SR); w_.writeframes((st * 32767).astype(np.int16).tobytes())
cute.build_audio = build_audio

# ---------------------------------------------------------------- episode chrome + harness
def darken(img):
    """'Swiss Dark': invert lightness, keep hue + chroma (p' = p + 255 - max - min).
    White paper → near-black, ink → near-white, signal orange stays orange, anti-aliased edges stay clean."""
    a = np.asarray(img).astype(np.int16)
    sh_ = 255 - a.max(axis=2, keepdims=True) - a.min(axis=2, keepdims=True)
    out = np.clip(a + sh_, 0, 255)
    out = np.clip(out + (out < 40) * 8, 0, 255)          # lift pure black a touch (less harsh on OLED)
    img.paste(Image.fromarray(out.astype(np.uint8)))

SLAM = .10              # frame-0 slam-in: the first scene starts zoomed 10 % and snaps to place within 0.3 s

def zoom_band(img, d, z, cx=480, cy=730, y0=300, y1=1180):
    l, tp = cx - cx / z, cy - cy / z
    img.paste(img.crop((int(l), int(tp), int(l + W / z), int(tp + H / z))).resize((W, H), Image.BILINEAR))
    d.rectangle([0, 0, W, y0], fill=BG); d.rectangle([0, y1, W, H], fill=BG)

def hblur(img, box, w):
    """horizontal motion blur (box filter of width w px) inside box"""
    w = int(w)
    if w < 2: return
    a = np.asarray(img.crop(box)).astype(np.float32)
    c = np.cumsum(np.pad(a, ((0, 0), (w, 0), (0, 0)), mode="edge"), axis=1)
    img.paste(Image.fromarray(((c[:, w:] - c[:, :-w]) / w).astype(np.uint8)), box[:2])

def whip_in(img, k, box=(0, 300, W, 1180)):
    """v3 cut for Episode (no slide): the new scene arrives from the right with motion blur"""
    off = int(140 * (1 - ease(k)))
    if off > 0:
        band = img.crop(box); img.paste(BG, (box[0], box[1], box[2], box[3])); img.paste(band, (box[0] + off, box[1]))
    hblur(img, box, 70 * (1 - k) ** 2)

class Episode:
    """chrome + harness. Options: layers (drawn every frame on top of the scene, for actors that carry over between scenes),
    drift (slow camera push per scene), loop (last frames wipe back to frame 0 for a seamless Instagram loop),
    music (dict for MUSIC), cover (dict for make_cover)."""
    def __init__(self, TL, no, title, chapters, order, sources=(), handle="@vascoda.soda", series="NOT JUST YOU",
                 drift=.03, loop=False, music=None, cover=None, dark=False, ui=None):
        self.TL, self.no, self.title, self.order = TL, no, title, list(order)
        if "guess" in TL.T and self.order[0] != "guess": self.order.insert(0, "guess")    # format v2: guess-first opener
        # ui: "minimal" (default since 28.10.2026) = no header, episode title, chapter or progress bar; "full" = old chrome
        self.ui = ui or os.environ.get("NJY_UI", "minimal")
        self.chapters = {k: (f"{i + 1:02d}", v) for i, (k, v) in enumerate(chapters.items())}
        self.sources, self.handle, self.series = sources, handle, series
        self.scenes, self.layers = {}, []
        self.drift, self.loop, self.music, self.cover_spec = drift, loop, music or {}, cover
        self.dark = dark

    def current(self, t):
        cur = self.order[0]
        for k in self.order[1:]:
            if t >= self.TL.S(k) - .05: cur = k
        if cur == "end" and getattr(self.TL, "end_mode", "card") == "hard":    # hard ending: hold the last content scene
            cur = self.order[self.order.index("end") - 1]
        return cur

    def scene_span(self, cur):
        i = self.order.index(cur); a = 0.0 if i == 0 else self.TL.S(cur) - .05
        b = self.TL.S(self.order[i + 1]) - .05 if i + 1 < len(self.order) else self.TL.total
        return a, b

    def grid(self, d):
        for x in range(X0, X1 + 1, 140): d.line([x, 280, x, Y1], fill=RULE, width=2)
        for (x, y) in ((X0, Y1), (X1, Y1)): cross(d, x, y)

    def chrome(self, d, t, cur, progress=True):
        if self.ui == "minimal": return
        d.text((X0, 212), self.series, font=F(COND, 34), fill=INK)
        d.text((X1, 212), f"{self.no:02d} / {self.title}", font=F(COND, 34), fill=INK, anchor="ra")
        d.line([X0, 262, X1, 262], fill=INK, width=4)
        if progress: d.line([X0, 262, X0 + (X1 - X0) * clamp(t / self.TL.S("end")), 262], fill=SIG, width=8)
        if cur in self.chapters:
            no, title = self.chapters[cur]
            d.text((X0, 274), no, font=F(COND, 26), fill=SIG); d.text((X0 + 44, 274), title, font=F(COND, 26), fill=INK)
        d.line([X0, 1188, X1, 1188], fill=INK, width=4)

    def subtitle(self, d, t, y0=1206):
        TL = self.TL; cur = TL.current(t) or self.order[0]
        if cur == "end": return
        b = TL.T[cur]
        if t > b["start"] + b["dur"] + .4: return
        f = F(BLK, 62); lines, curl = [], ""
        for w_ in b["text"].split():
            tst = (curl + " " + w_).strip()
            if d.textlength(tst, font=f) <= X1 - X0: curl = tst
            else: lines.append(curl); curl = w_
        lines.append(curl)
        shown = (t - b["start"]) / b["dur"] * len(b["text"])
        starts, c = [], 0                      # pages of max 3 lines; the page follows the spoken word
        for line in lines: starts.append(c); c += len(line) + 1
        cur_line = max([i for i, s0 in enumerate(starts) if s0 <= max(0, shown)] or [0])
        page = cur_line // 3; c = starts[page * 3]
        for li, line in enumerate(lines[page * 3: page * 3 + 3]):
            x = X0
            for w_ in line.split(" "):
                now = c <= shown < c + len(w_) + 1
                d.text((x, y0 + li * 72), w_, font=f, fill=SIG if now else (INK if c <= shown else RULE))
                x += d.textlength(w_ + " ", font=f); c += len(w_) + 1

    def end_card(self, d, t):
        k0 = self.TL.S("end")
        for i, (w_, col) in enumerate((("NOT", INK), ("JUST", INK), ("YOU.", SIG))):
            k = ease((t - k0 - i * .12) / .35)
            if k > 0: d.text((X0 - 8, 290 + i * 210), w_, font=F(BLK, 230), fill=mix(BG, col, k))
        if t > k0 + .9:
            d.text((X0, 980), "SOURCES", font=F(COND, 26), fill=SIG)
            for i, l in enumerate(self.sources): d.text((X0, 1016 + i * 32), l, font=F(MED, 24), fill=INK)
            box_label(d, X1, 1110, self.handle, 32, WHITE, INK, anchor="ra")

    def compose(self, img, d, t):
        cur = self.current(t)
        self.grid(d)
        if cur == "end": self.end_card(d, t)
        else:
            self.scenes[cur](img, d, t)
            for lay in self.layers: lay(img, d, t, cur)
            a, b = self.scene_span(cur)
            z = 1 + self.drift * ease_io((t - a) / max(.5, b - a))           # slow push through the scene
            if V3 and cur != self.order[0] and t - a < .2: whip_in(img, (t - a) / .2)
            z *= self.pulse_zoom(t)
            if cur != self.order[0]: z += .035 * math.exp(-(t - a) * 8)      # punch-in on every cut
            else: z += SLAM * (1 - ease(t / .3))                             # slam-in from frame 0 (no static first second)
            if z > 1.002: zoom_band(img, d, z)
            self.overlays(img, d, t, cur)
        self.chrome(d, t, cur)
        self.subtitle(d, t)

    # ---- format v2 (31.10.2026): guess-first opener, re-hook banners, comment question ----------------------------
    def last_scene(self):
        return self.order[self.order.index("end") - 1] if "end" in self.order else self.order[-1]

    def guess_scene(self, img, d, t):
        """opener: the question in big type from frame 0, a 3-2-1 countdown until the hook starts"""
        TL = self.TL; t0, t1 = TL.S("guess"), TL.S(self.order[1])
        box_label(d, X0, 300, "GUESS FIRST", 40, WHITE, INK if V3 else SIG, font=BLK)
        lines = TL.screen.get("guess") or [TL.T["guess"]["text"].upper()]
        size = int(min(170, 540 / (len(lines) * 1.05), *(840 / max(1, d.textlength(l, font=F(BLK, 100))) * 100 for l in lines)))
        words_in(d, t, [(l, -1 if i == 0 or V3 else t0 + .1 + i * .2, 390 + i * int(size * 1.05), size,
                         SIG if i == len(lines) - 1 and not V3 else INK) for i, l in enumerate(lines)])
        k = clamp((t - t0) / max(.5, t1 - t0)); n = 3 - min(2, int(k * 3))
        cx, cy, r = X1 - 120, 1050, 92
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=RULE, width=10)
        if k > 0: d.arc([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360 * k, fill=SIG, width=14)
        d.text((cx, cy), str(n), font=F(BLK, 120), fill=INK, anchor="mm")
        d.text((X0, 1010), "Your number?", font=F(COND, 54), fill=INK)
        d.text((X0, 1080), "Answer coming.", font=F(COND, 40), fill=MID)

    def overlays(self, img, d, t, cur):
        """re-hook banner (open loop) and the comment question, bottom of the content band"""
        TL = self.TL
        if cur in TL.tease:
            say, show = TL.tease[cur]; ts = TL.cue(cur, say[:16]) - .1
            if t >= ts:
                k = ease((t - ts) / .2); size = min(46, int(840 / max(1, d.textlength(show, font=F(BLK, 100))) * 100))
                box_label(d, X0 - (1 - k) * 70, 1122, show, size, WHITE, INK if V3 else SIG, font=BLK)
        if TL.ask and cur == self.last_scene():
            ta = TL.S(cur) + TL.T[cur]["dur"] * .55
            if t >= ta:
                k = ease((t - ta) / .25); size = min(46, int(840 / max(1, d.textlength(TL.ask, font=F(BLK, 100))) * 100))
                box_label(d, X0 - (1 - k) * 70, 1122, TL.ask, size, WHITE, INK if V3 else SIG, font=BLK)

    def v2_fx(self):
        TL = self.TL; out = []
        if "guess" in TL.T:
            t0, t1 = TL.S("guess"), TL.S(self.order[1])
            out += [(t0 + (t1 - t0) * i / 3, tick(.09), 0) for i in range(3)] + [(t1 - .02, thud(.5), 0)]
        for k, (say, _) in TL.tease.items(): out.append((TL.cue(k, say[:16]) - .1, pop(.18), 0))
        if TL.ask:
            c = self.last_scene(); out.append((TL.S(c) + TL.T[c]["dur"] * .55, pop(.15), 0))
        out += [(tc, tick(.07), 0) for tc in self.pulses()]
        if V3:                                        # reveal after every re-hook: riser → 0.35 s silence → sub drop
            for r in self.reveals(): out += [(r - .85, riser(.7, .07), 0), (r - .02, boom(.5), 0)]
        return out

    NUM = re.compile(r"\b(\d[\d,.]*|zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|"
                     r"sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|billion|half)\b", re.I)

    def pulses(self):
        """impulse beat: a short zoom pulse + tick on every spoken number (min. 0.6 s apart)"""
        if not V4: return []
        if getattr(self, "_pulses", None) is None:
            out = []
            for k in self.order:
                b = self.TL.T.get(k)
                if not b or not b["text"] or k == "guess": continue
                for m in self.NUM.finditer(b["text"]):
                    tc = b["start"] + b["dur"] * m.start() / len(b["text"])
                    if not out or tc - out[-1] >= .6: out.append(tc)
            self._pulses = out
        return self._pulses

    def pulse_zoom(self, t):
        z = 1.0
        for tc in self.pulses():
            if 0 <= t - tc < .45: z += .028 * math.exp(-(t - tc) * 9)
        return z

    def calm(self, fx=()):
        """longest stretch (s) without a visual/sound event – the build report flags > 3 s"""
        TL = self.TL; ev = [TL.S(k) for k in self.order if k in TL.T] + [t for t, *_ in fx] + self.pulses() + self.reveals()
        ev += [TL.cue(k, say[:16]) for k, (say, _) in TL.tease.items()]
        ev = sorted(e for e in ev if 0 <= e <= TL.total) + [TL.total]
        return round(max(b - a for a, b in zip([0.0] + ev, ev)), 2)

    def reveals(self):
        TL = self.TL; o = self.order
        return [TL.S(o[o.index(k) + 1]) for k in TL.tease if k in o and o.index(k) + 1 < len(o) and o[o.index(k) + 1] != "end"]

    def draw(self, img, d, t):
        self.scenes.setdefault("guess", self.guess_scene)
        self._draw(img, d, t)
        if self.dark: darken(img)

    def _draw(self, img, d, t):
        T = self.TL.total; L = .5
        if not self.loop or t < T - L: return self.compose(img, d, t)
        k = (t - (T - L)) / L                   # wipe: end card → frame 0 (seamless loop on Instagram)
        if k < .5:
            self.compose(img, d, t); d.rectangle([0, 0, W * ease(k * 2), H], fill=SIG)
        else:
            d.rectangle([0, 0, W, H], fill=BG); self.compose(img, d, 0.0)
            d.rectangle([W * ease((k - .5) * 2), 0, W, H], fill=SIG)

    def make_cover(self, path, words=None, kicker=None):
        """1080x1920 cover; key content sits inside the 1080x1440 centre crop of the profile grid"""
        spec = dict(self.cover_spec or {}); words = words or spec.get("words", [self.title]); kicker = kicker or spec.get("kicker", "")
        img = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(img)
        for x in range(X0, X1 + 1, 140): d.line([x, 240, x, 1680], fill=RULE, width=2)
        d.text((X0, 300), self.series, font=F(COND, 40), fill=INK); d.line([X0, 356, X1 + 60, 356], fill=INK, width=5)
        d.text((X0 - 10, 380), f"{self.no:02d}", font=F(BLK, 260), fill=SIG)
        size = spec.get("size") or min(320, int(min(860 / max(1, d.textlength(w_, font=F(BLK, 100))) * 100 for w_ in words)),
                                       int(820 / (len(words) * 1.02)))
        y = 700
        for i, w_ in enumerate(words):
            d.text((X0 - 8, y), w_, font=F(BLK, size), fill=SIG if i == len(words) - 1 and spec.get("accent_last", True) else INK); y += int(size * 1.02)
        if kicker: d.text((X0, y + 30), kicker, font=F(COND, 46), fill=INK)
        d.line([X0, 1600, X1 + 60, 1600], fill=INK, width=5)
        d.text((X0, 1616), self.handle, font=F(COND, 34), fill=INK)
        if self.dark: darken(img)
        img = Image.fromarray(np.clip(np.array(img).astype(np.int16) + cute.PAPER, 0, 255).astype(np.uint8))
        img.save(path); return path

    def cut_fx(self, amp=.12):
        """whoosh on every scene cut (ends before the voice starts)"""
        return [(self.TL.S(k) - .3, whoosh(.25, amp), 0) for k in self.order[1:]]

    def run(self, fx):
        global MUSIC
        MUSIC = dict(MUSIC, **self.music)
        if V3: MUSIC["gaps"] = list(MUSIC.get("gaps", ())) + [(r - .35, r) for r in self.reveals()]
        if "--cover" in sys.argv: print("cover", self.make_cover(sys.argv[1])); return
        cute.run(self.TL, self.draw, list(fx) + self.v2_fx())
