"""NOT JUST YOU – No. 02: the doorway effect. Soft & cute style, Reel 9:16 with safe zones, deterministic per frame.
Usage: python3 render.py out.mp4 | python3 render.py sheet.png --t 1,2,3
"""
import json, math, os, sys, wave, subprocess
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont
from scipy.signal import resample_poly, butter, lfilter

HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(HERE, "..", "fonts") + "/"
W, H, FPS, SR = 1080, 1920, 30, 48000
SAFE_R = 900
# ---- soft & cute palette (Material-You-like tonal set)
BG = (246, 242, 255); CARD = (236, 228, 255); WALL_A = (232, 222, 255); WALL_B = (220, 244, 234); FLOOR = (214, 200, 245)
INK = (44, 32, 72); PRIMARY = (103, 80, 164); BEAN = (176, 150, 240); BEAN_D = (120, 94, 196)
PINK = (239, 128, 160); BLUSH = (255, 176, 196); MINT = (125, 211, 176); MINT_D = (60, 150, 115); SUN = (255, 214, 120); WHITE = (255, 255, 255)
SKY = (150, 200, 255)
_f = {}
def F(n, s):
    if (n, s) not in _f: _f[(n, s)] = ImageFont.truetype(FD + n, s)
    return _f[(n, s)]
BLK, BOLD, MONO = "Roboto-Black.woff", "Roboto-Bold.woff", "roboto-mono-latin-500.woff"
def clamp(k): return max(0., min(1., k))
def ease(k): k = clamp(k); return 1 - (1 - k) ** 3
def ease_io(k): k = clamp(k); return k * k * (3 - 2 * k)
def back(k, s=2.2): k = clamp(k) - 1; return k * k * ((s + 1) * k + s) + 1
def elastic(k):
    k = clamp(k)
    return 1 if k >= 1 else 1 - math.exp(-6 * k) * math.cos(k * 12)
def lerp(a, b, k): return a + (b - a) * k
def mix(a, b, k): k = clamp(k); return tuple(int(lerp(x, y, k)) for x, y in zip(a, b))

META = json.load(open(os.path.join(HERE, "vo", "meta.json")))
LEAD = .5
GAP = {"hook": .7, "name": .3, "title": .6, "event": .4, "tidy": .3, "reason": .7, "study": .3, "forgot": .5, "back": .7, "busy": .4, "carry": .6, "end": 2.4}
T, t = {}, LEAD
for m in META:
    T[m["id"]] = dict(start=t, dur=m["dur"], text=m["text"]); t += m["dur"] + GAP.get(m["id"], .35)
TOTAL_S = t; TOTAL = int(round(TOTAL_S * FPS))
def S(k): return T[k]["start"]
def E(k): return T[k]["start"] + T[k]["dur"]
def cue(beat, word):
    b = T[beat]; i = b["text"].lower().find(word.lower())
    if i < 0: raise ValueError(f"cue '{word}' missing in '{beat}'")
    return b["start"] + b["dur"] * i / len(b["text"])

# ---------------------------------------------------------------- building blocks
def pill(d, x, y, text, bg, fg, size=30, anchor="la", k=1.0):
    if k <= 0: return
    f = F(BLK, size); w = d.textlength(text, font=f) + size * 1.4; h = size * 1.75
    if anchor == "ma": x -= w / 2
    if anchor == "ra": x -= w
    s = back(k); cx, cy = x + w / 2, y + h / 2
    d.rounded_rectangle([cx - w / 2 * s, cy - h / 2 * s, cx + w / 2 * s, cy + h / 2 * s], radius=h / 2 * s, fill=bg)
    if s > .6: d.text((cx, cy), text, font=F(BLK, max(8, int(size * min(1, s)))), fill=fg, anchor="mm")

def card(d, box, fill=CARD, r=56): d.rounded_rectangle(box, radius=r, fill=fill)

def sparkle(d, x, y, r, col):
    d.polygon([(x, y - r), (x + r * .28, y - r * .28), (x + r, y), (x + r * .28, y + r * .28), (x, y + r), (x - r * .28, y + r * .28), (x - r, y), (x - r * .28, y - r * .28)], fill=col)

def bean(d, x, y, t, s=1.0, walk=0.0, squash=0.0, look=0.0, mood="happy", key=0, color=BEAN, wave=0.0):
    """cute bean character; (x, y) = feet on the floor"""
    bw, bh = 120 * s * (1 + squash), 170 * s * (1 - squash)
    bob = abs(math.sin(walk * math.pi)) * 10 * s
    top = y - 18 * s - bh - bob
    # legs
    for i, side in enumerate((-1, 1)):
        sw = math.sin(walk * math.pi + i * math.pi) * 14 * s if walk else 0
        lx = x + side * 26 * s + sw
        d.rounded_rectangle([lx - 11 * s, y - 34 * s - bob * .3, lx + 11 * s, y], radius=11 * s, fill=mix(color, INK, .45))
    # body
    d.rounded_rectangle([x - bw / 2, top, x + bw / 2, top + bh], radius=bw / 2, fill=color)
    d.rounded_rectangle([x - bw / 2 + 12 * s, top + 14 * s, x - bw / 2 + 30 * s, top + 60 * s], radius=9 * s, fill=mix(color, WHITE, .45))
    # arm wave
    if wave:
        ax, ay = x + bw / 2 - 6 * s, top + bh * .55
        ang = -math.pi / 3 + math.sin(wave * 12) * .5
        d.line([ax, ay, ax + math.cos(ang) * 50 * s, ay + math.sin(ang) * 50 * s], fill=mix(color, INK, .25), width=int(16 * s))
    # face
    ey = top + bh * .36
    blink = (int((t + key * .7) * FPS) % 110) < 4
    for side in (-1, 1):
        ex = x + side * 24 * s + look * 10 * s
        if blink: d.line([ex - 10 * s, ey, ex + 10 * s, ey], fill=INK, width=int(5 * s))
        else:
            d.ellipse([ex - 13 * s, ey - 15 * s, ex + 13 * s, ey + 15 * s], fill=INK)
            d.ellipse([ex - 6 * s + look * 3 * s, ey - 10 * s, ex + 1 * s + look * 3 * s, ey - 3 * s], fill=WHITE)
        d.ellipse([x + side * 40 * s - 13 * s, ey + 18 * s, x + side * 40 * s + 13 * s, ey + 30 * s], fill=BLUSH)
    my = ey + 30 * s
    if mood == "happy": d.arc([x - 14 * s, my - 10 * s, x + 14 * s, my + 10 * s], 20, 160, fill=INK, width=int(5 * s))
    elif mood == "o": d.ellipse([x - 8 * s, my - 6 * s, x + 8 * s, my + 10 * s], fill=INK)
    else: d.line([x - 10 * s, my + 2 * s, x + 10 * s, my - 2 * s], fill=INK, width=int(5 * s))
    return (x, top)

def bubble(d, head, t, content, k=1.0, poof=0.0, s=1.0, dx=60):
    """thought bubble above/right of the head; content: 'glass' | '?' | text"""
    if k <= 0 and poof <= 0: return
    hx, hy = head
    cx, cy = hx + dx * s, hy - 110 * s
    if poof > 0:   # burst
        for i in range(9):
            a = i / 9 * 2 * math.pi; r = 30 + poof * 110
            rr = (1 - poof) * 18 * s
            if rr > 1: d.ellipse([cx + math.cos(a) * r * s - rr, cy + math.sin(a) * r * s - rr, cx + math.cos(a) * r * s + rr, cy + math.sin(a) * r * s + rr], fill=WHITE)
        if poof < .6: sparkle(d, cx, cy, 40 * s * (1 - poof), SUN)
        return
    sc = back(k)
    for (ox, oy, r) in ((-12, 70, 9), (-2, 46, 14)):
        d.ellipse([hx + (ox + 6) * s - r * s * sc, hy + (oy - 110 + 40) * s - r * s * sc, hx + (ox + 6) * s + r * s * sc, hy + (oy - 110 + 40) * s + r * s * sc], fill=WHITE)
    for (ox, oy, r) in ((-46, 6, 46), (0, -18, 58), (48, 4, 46), (0, 26, 48)):
        R = r * s * sc
        d.ellipse([cx + ox * s * sc - R, cy + oy * s * sc - R, cx + ox * s * sc + R, cy + oy * s * sc + R], fill=WHITE)
    if sc < .5: return
    if content == "glass":
        gx, gy = cx, cy + 2 * s
        d.polygon([(gx - 26 * s, gy - 38 * s), (gx + 26 * s, gy - 38 * s), (gx + 20 * s, gy + 38 * s), (gx - 20 * s, gy + 38 * s)], fill=(235, 245, 255), outline=INK, width=int(4 * s))
        wl = gy - 4 * s + math.sin(t * 5) * 3 * s
        d.polygon([(gx - 22 * s, wl), (gx + 22 * s, wl), (gx + 19 * s, gy + 34 * s), (gx - 19 * s, gy + 34 * s)], fill=SKY)
    elif content == "?":
        d.text((cx, cy + 4 * s), "?", font=F(BLK, int(74 * s)), fill=PINK, anchor="mm")
    else:
        d.text((cx, cy + 4 * s), content, font=F(BLK, int(50 * s)), fill=PRIMARY, anchor="mm")

def room(d, box, door_x, t, left=WALL_A, right=WALL_B, floor_y=None):
    x0, y0, x1, y1 = box
    fy = floor_y or (y1 - 110)
    d.rounded_rectangle(box, radius=56, fill=left)
    d.rectangle([door_x, y0 + 0, x1 - 56, y1], fill=right); d.rounded_rectangle([door_x, y0, x1, y1], radius=56, fill=right)
    d.rectangle([door_x, y0, door_x + 60, y1], fill=right)
    d.rounded_rectangle([x0, fy, x1, y1], radius=56, fill=FLOOR); d.rectangle([x0, fy, x1, fy + 50], fill=FLOOR)
    # door frame (arch)
    dw, dh = 150, 330
    d.rounded_rectangle([door_x - dw / 2 - 18, fy - dh - 18, door_x + dw / 2 + 18, fy + 6], radius=dw / 2 + 18, fill=PRIMARY)
    d.rounded_rectangle([door_x - dw / 2, fy - dh, door_x + dw / 2, fy + 6], radius=dw / 2, fill=mix(right, WHITE, .4))
    # left room: plant + sofa ; right room: fridge
    px, py = x0 + 90, fy
    d.rounded_rectangle([px - 32, py - 70, px + 32, py], radius=14, fill=PINK)
    for i, a in enumerate((-.6, 0, .6)):
        lx, ly = px + math.sin(a + math.sin(t * 2 + i) * .08) * 70, py - 70 - math.cos(a) * 80
        d.ellipse([lx - 26, ly - 40, lx + 26, ly + 40], fill=MINT)
    fx = x1 - 120
    d.rounded_rectangle([fx - 70, fy - 290, fx + 70, fy], radius=34, fill=WHITE)
    d.line([fx - 70, fy - 190, fx + 70, fy - 190], fill=mix(WHITE, INK, .2), width=5)
    d.rounded_rectangle([fx + 38, fy - 270, fx + 48, fy - 215], radius=5, fill=mix(WHITE, INK, .35))
    d.rounded_rectangle([fx + 38, fy - 165, fx + 48, fy - 90], radius=5, fill=mix(WHITE, INK, .35))
    return fy

def subtitle(d, t, y0=1210):
    cur = None
    for k, b in T.items():
        if t >= b["start"] - .05: cur = k
    if cur in (None, "end"): return
    b = T[cur]
    if t > b["start"] + b["dur"] + .5: return
    f = F(BLK, 58); words = b["text"].split(); lines, curl = [], ""
    for w_ in words:
        tst = (curl + " " + w_).strip()
        if d.textlength(tst, font=f) <= SAFE_R - 80: curl = tst
        else: lines.append(curl); curl = w_
    lines.append(curl)
    shown = (t - b["start"]) / b["dur"] * len(b["text"]); c = 0
    for li, line in enumerate(lines):
        x = 70
        for w_ in line.split(" "):
            on = c <= shown
            col = INK if on else mix(BG, INK, .18)
            yy = y0 + li * 70 - (6 if on and c > shown - 6 else 0)
            d.text((x, yy), w_, font=f, fill=col)
            x += d.textlength(w_ + " ", font=f); c += len(w_) + 1

def header(d, t):
    pill(d, 60, 222, "NOT JUST YOU · 02", PRIMARY, WHITE, size=26)
    d.text((SAFE_R, 238), "the doorway effect", font=F(BOLD, 28), fill=PRIMARY, anchor="ra")

# ---------------------------------------------------------------- scenes
BOX = (60, 320, 900, 1140)
DOOR_X = 470
def walk_x(t, t0, x0, x1, dur):
    k = clamp((t - t0) / dur); return lerp(x0, x1, ease_io(k)), (k > 0 and k < 1)

def sc_hook(img, d, t):
    fy = room(d, BOX, DOOR_X, t)
    t0 = S("hook") + .1
    x, walking = walk_x(t, t0, 200, 700, 2.0)
    cross = t0 + 2.0 * .54
    look = math.sin((t - t0 - 2.1) * 4) if t > t0 + 2.2 else 0
    mood = "o" if t > cross + .3 else "happy"
    head = bean(d, x, fy, t, 1.0, walk=(t - t0) * 2.2 if walking else 0, look=look, mood=mood)
    if t < cross: bubble(d, head, t, "glass", k=(t - S("hook") + .3) / .4)
    elif t < cross + .45: bubble(d, head, t, "glass", poof=(t - cross) / .45)
    else: bubble(d, head, t, "?", k=(t - cross - .45) / .35)
    if t > cross + .8: pill(d, BOX[0] + 40, BOX[1] + 40, "KITCHEN", WHITE, MINT_D, size=24, k=(t - cross - .8) / .3)

def sc_name(img, d, t):
    fy = room(d, BOX, DOOR_X, t)
    head = bean(d, 700, fy, t, 1.0, look=math.sin(t * 3) * .6, mood="o")
    bubble(d, head, t, "?")
    if t >= S("title") - .1:
        k = (t - S("title")) / .45
        card(d, (110, 470, 850, 900), fill=WHITE)
        d.text((480, 560), "the", font=F(BOLD, 60), fill=PRIMARY, anchor="mm")
        s = back(k)
        d.text((480, 690), "DOORWAY", font=F(BLK, max(10, int(150 * s))), fill=PINK, anchor="mm")
        d.text((480, 820), "EFFECT", font=F(BLK, max(10, int(150 * s))), fill=PRIMARY, anchor="mm")
        for i, (sx, sy) in enumerate(((150, 500), (800, 520), (820, 860), (140, 870))):
            sparkle(d, sx, sy, 18 + 8 * math.sin(t * 6 + i), SUN)

def scene_card(d, x, y, w, h, t, content="glass", label="SCENE", col=WALL_A, s=1.0):
    d.rounded_rectangle([x, y, x + w, y + h], radius=28, fill=col, outline=PRIMARY, width=5)
    head = bean(d, x + w * .4, y + h - 18, t, .42 * s, mood="happy", key=3)
    bubble(d, head, t, content, s=.42 * s, dx=50)
    pill(d, x + 14, y + 14, label, PRIMARY, WHITE, size=18)

def sc_event(img, d, t):
    card(d, BOX, fill=CARD)
    # big head with a scene card inside
    k = ease((t - S("event")) / .5)
    bean(d, 300, 1090, t, 2.2, mood="happy", key=1)
    if t >= cue("event", "like a little scene") - .2:
        kk = back((t - cue("event", "like a little scene") + .2) / .45)
        if kk > .05:
            w, h = 320 * kk, 230 * kk
            scene_card(d, 560 - w / 2 + 40, 480 - h / 2, w, h, t, s=kk)
    pill(d, 560, 380, "EVENT", PINK, WHITE, size=26, k=(t - cue("event", "event") + .1) / .3)

def sc_tidy(img, d, t):
    card(d, BOX, fill=CARD)
    tt_ = (t - S("tidy"))
    # box at the bottom
    bx, by = 480, 1000
    d.rounded_rectangle([bx - 170, by - 120, bx + 170, by + 60], radius=26, fill=SUN)
    lid = 0
    if t >= S("reason") + .6: lid = ease((t - S("reason") - .6) / .35)
    ly = lerp(by - 330, by - 150, back(lid, 1.4)) if lid > 0 else by - 330
    d.rounded_rectangle([bx - 186, ly, bx + 186, ly + 34], radius=17, fill=mix(SUN, INK, .18))
    d.text((bx, by - 30), "OLD SCENES", font=F(BLK, 34), fill=INK, anchor="mm")
    # old scene card flies into the box at "tidies up"
    tf = cue("tidy", "tidies")
    k = ease_io((t - tf) / .7)
    sx, sy = lerp(330, bx - 110, k), lerp(460, by - 150, k)
    sc_ = lerp(1, .55, k)
    if k < .98 and t < S("reason"):
        scene_card(d, sx - 160 * sc_, sy - 115 * sc_, 320 * sc_, 230 * sc_, t, s=sc_, label="OLD")
    # new scene appears at "new scene"
    tn = cue("tidy", "new scene")
    if t >= tn:
        kk = back((t - tn) / .45)
        scene_card(d, 560, 380, 300 * kk, 220 * kk, t, content="?", label="NEW", col=WALL_B, s=kk)
    # the reason (glass) gets packed too
    if t >= S("reason"):
        kg = ease_io((t - S("reason")) / .7)
        gx, gy = lerp(300, bx, kg), lerp(520, by - 110, kg)
        if kg < 1:
            d.polygon([(gx - 26, gy - 38), (gx + 26, gy - 38), (gx + 20, gy + 38), (gx - 20, gy + 38)], fill=(235, 245, 255), outline=INK, width=4)
            d.polygon([(gx - 22, gy), (gx + 22, gy), (gx + 19, gy + 34), (gx - 19, gy + 34)], fill=SKY)
        pill(d, 120, 420, "the reason you came", WHITE, PINK, size=26, k=(t - S("reason")) / .3)
        if lid >= 1: sparkle(d, bx + 150, by - 150, 22, PINK)

def lane(d, t, y, label, door, t0, back_at=None, busy=False, forget=True):
    x0, x1 = 90, 870
    d.rounded_rectangle([x0, y, x1, y + 330], radius=40, fill=WALL_A)
    fy = y + 290
    d.rounded_rectangle([x0, fy, x1, y + 330], radius=40, fill=FLOOR); d.rectangle([x0, fy, x1, fy + 20], fill=FLOOR)
    if door:
        d.rounded_rectangle([DOOR_X - 60, fy - 210, DOOR_X + 60, fy + 4], radius=60, fill=PRIMARY)
        d.rounded_rectangle([DOOR_X - 46, fy - 196, DOOR_X + 46, fy + 4], radius=46, fill=WALL_B)
    pill(d, x0 + 18, y + 18, label, WHITE, PRIMARY, size=20)
    x, walking = walk_x(t, t0, 190, 750, 2.2)
    cross = t0 + 2.2 * .5
    if back_at and t >= back_at:
        x, walking = walk_x(t, back_at, 750, 210, 1.8)
    head = bean(d, x, fy, t, .62, walk=(t - t0) * 2.4 if walking else 0, mood="happy" if not (door and forget and t > cross) else "o",
                look=-1 if (back_at and t >= back_at) else (1 if walking else 0), key=int(y))
    if busy:
        n_b = 4
        for i in range(n_b):
            hx, hy = head
            ang = i / n_b * math.pi - math.pi
            if door and t > cross:
                fall = clamp((t - cross) / .8)
                bx_ = hx + math.cos(ang) * 70 + i * 20 * fall; by_ = hy - 60 + math.sin(ang) * 50 + fall * 260 + fall * fall * 80
                if fall < 1: d.ellipse([bx_ - 26, by_ - 26, bx_ + 26, by_ + 26], fill=WHITE); d.text((bx_, by_), "7394"[i], font=F(BLK, 30), fill=PRIMARY, anchor="mm")
            else:
                bx_ = hx + math.cos(ang + math.sin(t * 3) * .1) * 80; by_ = hy - 70 + math.sin(ang) * 50
                d.ellipse([bx_ - 26, by_ - 26, bx_ + 26, by_ + 26], fill=WHITE); d.text((bx_, by_), "7394"[i], font=F(BLK, 30), fill=PRIMARY, anchor="mm")
        return cross
    if door and forget and t > cross:
        if t < cross + .4: bubble(d, head, t, "glass", poof=(t - cross) / .4, s=.62)
        else: bubble(d, head, t, "?", k=(t - cross - .4) / .3, s=.62)
    else:
        bubble(d, head, t, "glass", k=(t - t0 + .2) / .3, s=.62)
    return cross

def sc_study(img, d, t):
    pill(d, 60, 300, "RADVANSKY ET AL., 2011", PINK, WHITE, size=24)
    t0 = S("study") + .6
    lane(d, t, 380, "SAME ROOM", False, t0)
    lane(d, t, 760, "THROUGH A DOOR", True, t0, back_at=S("back") + .2)
    d.text((480, 727), "same distance", font=F(BOLD, 26), fill=PRIMARY, anchor="mm")
    if t >= cue("forgot", "they forgot"):
        pill(d, 860, 400, "remembered", MINT, WHITE, size=22, anchor="ra", k=(t - cue("forgot", "they forgot")) / .3)
        pill(d, 860, 780, "forgot more", PINK, WHITE, size=22, anchor="ra", k=(t - cue("forgot", "they forgot") - .2) / .3)
    if t >= S("back") + 1.6:
        pill(d, 480, 1100, "walking back: still ?", INK, WHITE, size=24, anchor="ma", k=(t - S("back") - 1.6) / .3)

def sc_busy(img, d, t):
    pill(d, 60, 300, "McFADYEN ET AL., 2021", PINK, WHITE, size=24)
    t0 = S("busy") + 1.4
    lane(d, t, 380, "CALM HEAD", True, t0, forget=False)
    lane(d, t, 760, "BUSY HEAD (counting task)", True, t0, busy=True)
    if t >= cue("busy", "mostly hurt"):
        pill(d, 860, 400, "mostly fine", MINT, WHITE, size=22, anchor="ra", k=(t - cue("busy", "mostly hurt")) / .3)
        pill(d, 860, 780, "forgot more", PINK, WHITE, size=22, anchor="ra", k=(t - cue("busy", "mostly hurt") - .2) / .3)

def sc_carry(img, d, t):
    card(d, BOX, fill=CARD)
    k = (t - S("carry"))
    head = bean(d, 480, 1060, t, 1.6, mood="happy", key=5)
    hx, hy = head
    for i in range(5):
        a = -math.pi * .9 + i * .45
        rise = ease_io((t - cue("carry", "you're just") - i * .12) / 1.6)
        bx_, by_ = hx + math.cos(a) * 170, hy - 40 + math.sin(a) * 120 - rise * 400
        r = 40 * (1 - rise * .4)
        if rise < 1:
            d.ellipse([bx_ - r, by_ - r, bx_ + r, by_ + r], fill=WHITE)
            d.text((bx_, by_), ["7", "?", "!", "9", "…"][i], font=F(BLK, int(r)), fill=PRIMARY, anchor="mm")
    if t >= cue("carry", "you're just") + 1.2:
        sparkle(d, hx + 150, hy - 60, 26 + 6 * math.sin(t * 7), SUN); sparkle(d, hx - 160, hy - 20, 18, PINK)

def sc_end(img, d, t):
    k0 = S("end")
    card(d, (60, 320, 900, 1140), fill=CARD)
    for i, (word, col) in enumerate((("NOT", PRIMARY), ("JUST", PRIMARY), ("YOU.", PINK))):
        k = back((t - k0 - i * .15) / .45)
        if k > .05: d.text((110, 380 + i * 175), word, font=F(BLK, max(8, int(190 * k))), fill=col)
    bean(d, 720, 1000, t, 1.15, mood="happy", key=7, wave=t if t > k0 + .4 else 0)
    if t > k0 + 1.0:
        d.text((70, 1190), "Sources", font=F(BLK, 26), fill=INK)
        d.text((70, 1228), "Radvansky, Krawietz & Tamplin (2011), QJEP", font=F(MONO, 22), fill=PRIMARY)
        d.text((70, 1260), "McFadyen et al. (2021), BMC Psychology", font=F(MONO, 22), fill=PRIMARY)
        pill(d, 70, 1310, "@vascoda.soda", PRIMARY, WHITE, size=28, k=(t - k0 - 1.0) / .3)

_g = np.random.default_rng(3)
PAPER = (_g.normal(0, 4, (H // 2, W // 2, 1))).repeat(2, 0).repeat(2, 1).astype(np.int16)   # soft static paper grain

def render_frame(fr):
    t = fr / FPS
    img = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(img)
    header(d, t)
    if t < S("name"): sc_hook(img, d, t)
    elif t < S("event") - .1: sc_name(img, d, t)
    elif t < S("tidy"): sc_event(img, d, t)
    elif t < S("study") - .1: sc_tidy(img, d, t)
    elif t < S("busy") - .1: sc_study(img, d, t)
    elif t < S("carry") - .1: sc_busy(img, d, t)
    elif t < S("end") - .1: sc_carry(img, d, t)
    else: sc_end(img, d, t)
    if t < S("end") - .1: subtitle(d, t)
    return np.clip(np.array(img).astype(np.int16) + PAPER, 0, 255).astype(np.uint8)

# ---------------------------------------------------------------- sound (major key, plucks, pops)
rng = np.random.default_rng(11)
def lp(x, fc): b, a = butter(2, fc / (SR / 2)); return lfilter(b, a, x)
def bp(x, lo, hi): b, a = butter(2, [lo / (SR / 2), hi / (SR / 2)], "band"); return lfilter(b, a, x)
def tt_(dur): return np.arange(int(dur * SR)) / SR
def pluck(f, amp=.08, dur=.6):
    t = tt_(dur); return amp * (np.sin(2 * np.pi * f * t) + .4 * np.sin(4 * np.pi * f * t) + .15 * np.sin(6 * np.pi * f * t)) * np.exp(-t * 9)
def pop(amp=.25):
    t = tt_(.12); f = 400 + 900 * (1 - np.exp(-t * 50)); return amp * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 30)
def boing(amp=.18):
    t = tt_(.35); f = 260 + 120 * np.sin(t * 40) * np.exp(-t * 6); return amp * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)
def poof(amp=.25):
    t = tt_(.3); return amp * bp(rng.standard_normal(len(t)), 600, 5000) * np.exp(-t * 14)
def chime(fs, amp=.05):
    out = np.zeros(int(1.6 * SR))
    for i, f in enumerate(fs):
        p_ = pluck(f, amp, 1.4); s = int(i * .07 * SR); out[s:s + len(p_)] += p_[:len(out) - s]
    return out
def softkick(amp=.35):
    t = tt_(.25); f = 45 + 70 * np.exp(-t * 30); return amp * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 14)
def step(amp=.06):
    t = tt_(.05); return amp * lp(rng.standard_normal(len(t)), 900) * np.exp(-t * 60)

def build_audio(path):
    n = int((TOTAL_S + 1) * SR); vo = np.zeros(n); mus = np.zeros((n, 2)); fx = np.zeros((n, 2))
    def put(buf, x, t0, pan=0.):
        s = int(t0 * SR); e = min(n, s + len(x)); x = x[:e - s]
        if buf.ndim == 1: buf[s:e] += x
        else: buf[s:e, 0] += x * (1 - max(0, pan)); buf[s:e, 1] += x * (1 + min(0, pan))
    for m in META:
        a, sr = sf.read(os.path.join(HERE, "vo", m["id"] + ".wav")); put(vo, resample_poly(a, SR, sr), T[m["id"]]["start"])
    # music: C – Am – F – G, marimba-ish plucks in 8ths at 112 bpm, soft kick on 1 & 3
    beat = 60 / 112; chords = [[261.6, 329.6, 392], [220, 261.6, 329.6], [174.6, 220, 261.6], [196, 246.9, 293.7]]
    pattern = [0, 2, 1, 2, 0, 2, 1, 2]
    tt = 0.0; i = 0
    while tt < TOTAL_S - .5:
        ch = chords[(i // 8) % 4]
        put(mus, pluck(ch[pattern[i % 8]] * (2 if i % 8 in (3, 7) else 1), .05), tt, pan=(.25 if i % 2 else -.25))
        if i % 8 == 0: put(mus, pluck(ch[0] / 2, .09, 1.2), tt)
        if i % 4 == 0: put(mus, softkick(), tt)
        tt += beat / 2; i += 1
    # effects bound to the picture
    t0 = S("hook") + .1
    for k_ in range(9): put(fx, step(), t0 + k_ * .23, pan=-.3 + k_ * .07)
    cross = t0 + 2.0 * .54; put(fx, poof(), cross); put(fx, pop(.2), cross + .45)
    put(fx, chime([523.3, 659.3, 784, 1046.5]), S("title"))
    put(fx, pop(), cue("event", "like a little scene"))
    put(fx, boing(), cue("tidy", "tidies")); put(fx, pop(), cue("tidy", "new scene"))
    put(fx, pop(.2), S("reason")); put(fx, softkick(.5), S("reason") + .6 + .35)
    st0 = S("study") + .6
    for k_ in range(10): put(fx, step(.04), st0 + k_ * .22)
    put(fx, poof(.2), st0 + 1.1); put(fx, pop(.15), cue("forgot", "they forgot")); put(fx, pop(.15), cue("forgot", "they forgot") + .2)
    put(fx, boing(.12), S("back") + .2)
    bt0 = S("busy") + 1.4; put(fx, poof(.3), bt0 + 1.1)
    for k_ in range(4): put(fx, pop(.12), bt0 + 1.15 + k_ * .1)
    for k_ in range(5): put(fx, pop(.1), cue("carry", "you're just") + k_ * .12)
    put(fx, chime([392, 523.3, 659.3, 784]), cue("carry", "you're just") + 1.2)
    put(fx, chime([523.3, 659.3, 784, 1046.5, 1318.5], .06), S("end"))
    env = np.convolve(np.abs(vo), np.ones(int(.12 * SR)) / int(.12 * SR), "same")
    duck = (1 - .6 * np.clip(env / (env.max() * .15 + 1e-9), 0, 1))[:, None]
    st = (vo[:, None] + mus * duck + fx)[: int(TOTAL_S * SR)]
    st /= np.abs(st).max() / .9
    fd = int(.5 * SR); st[-fd:] *= np.linspace(1, 0, fd)[:, None]
    with wave.open(path, "wb") as w_:
        w_.setnchannels(2); w_.setsampwidth(2); w_.setframerate(SR); w_.writeframes((st * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    out = sys.argv[1]
    if "--t" in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index("--t") + 1].split(",")]
        ims = []
        for x in ts:
            im = Image.fromarray(render_frame(int(x * FPS))).convert("RGBA"); ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(ov)
            g.rectangle([0, 0, W, 200], fill=(0, 160, 255, 50)); g.rectangle([0, 1480, W, H], fill=(0, 160, 255, 50)); g.rectangle([960, 900, W, 1480], fill=(0, 160, 255, 50))
            ims.append(Image.alpha_composite(im, ov).convert("RGB").resize((270, 480)))
        sh = Image.new("RGB", (270 * len(ims), 480))
        for i, im in enumerate(ims): sh.paste(im, (270 * i, 0))
        sh.save(out); print("saved", out, "total", round(TOTAL_S, 2), {k: round(v["start"], 2) for k, v in T.items()}); sys.exit()
    wav = out.replace(".mp4", ".wav"); build_audio(wav); print("audio ok", flush=True)
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-i", wav, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "24", "-preset", "slow",
                          "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest",
                          "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for fr in range(TOTAL):
        p.stdin.write(render_frame(fr).tobytes())
        if fr % 150 == 0: print("frame", fr, "/", TOTAL, flush=True)
    p.stdin.close(); p.wait(); print("done", out, round(TOTAL / FPS, 2), "s")
