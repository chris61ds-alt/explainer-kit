"""Dot – the AI narrator as an original anime-style character (flat colours, thin outlines).
draw_dot(img, cx, cy, s, expr, mouth, blink, variant, pre_dark)
  expr: "talk" | "happy" (^ ^ eyes) | "wow" (big eyes, open mouth)
  mouth: 0..1 open (lip-sync), blink: 0..1 closed
  variant: "silver" (light silver bob) | "dots" (bob rendered as a halftone dot pattern)
  pre_dark: True when the frame is inverted afterwards by darken() (dark episodes) – colours are pre-inverted
  (darken is an involution: p -> p + 255 - max - min), so the final frame shows the real colours."""
import math
from PIL import Image, ImageDraw

def _inv(c):
    m, n = max(c[:3]), min(c[:3]); a = c[3] if len(c) > 3 else 255
    return tuple(max(0, min(255, v + 255 - m - n)) for v in c[:3]) + (a,)

PAL = dict(skin=(250, 226, 210), skin_sh=(236, 196, 178), hair=(232, 232, 236), hair_sh=(188, 190, 202), line=(38, 34, 40),
           iris=(255, 92, 28), iris_d=(170, 40, 10), white=(255, 255, 255), cheek=(255, 176, 160), hood=(74, 74, 80),
           hood_d=(52, 52, 58), phones=(255, 84, 20), phones_d=(190, 52, 10), mouth=(120, 30, 40), tongue=(255, 120, 110))

def draw_dot(img, cx, cy, s=1.0, expr="talk", mouth=0.0, blink=0.0, variant="silver", pre_dark=False, look=(0, 0)):
    SS = 2                                                     # supersampling for clean anti-aliased edges
    W, H = int(700 * s * SS), int(820 * s * SS)
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    P = {k: (_inv(v) if pre_dark else (v if len(v) == 4 else v + (255,))) for k, v in PAL.items()}
    u = s * SS; ox, oy = W / 2, 330 * u                      # local head centre
    X = lambda x: ox + x * u; Y = lambda y: oy + y * u
    def E(x0, y0, x1, y1, **k): d.ellipse([X(x0), Y(y0), X(x1), Y(y1)], **k)
    def R(x0, y0, x1, y1, r, **k): d.rounded_rectangle([X(x0), Y(y0), X(x1), Y(y1)], radius=int(r * u), **k)
    def Pg(pts, **k): d.polygon([(X(a), Y(b)) for a, b in pts], **k)
    lw = max(2, int(5 * u))
    # body: hoodie with orange drawstrings
    R(-205, 205, 205, 520, 140, fill=P["hood"], outline=P["line"], width=lw)
    Pg([(-62, 200), (62, 200), (36, 270), (-36, 270)], fill=P["hood_d"])
    for sx in (-1, 1): d.line([X(sx * 30), Y(262), X(sx * 36), Y(360)], fill=P["phones"], width=int(8 * u)); E(sx * 36 - 9, 356, sx * 36 + 9, 374, fill=P["phones"])
    R(-34, 130, 34, 215, 18, fill=P["skin_sh"])               # neck
    # hair, back part (bob)
    if variant == "dots":
        for yy in range(-190, 170, 16):
            for xx in range(-190, 191, 16):
                if (xx / 185) ** 2 + ((yy + 10) / 185) ** 2 <= 1 or (abs(xx) < 178 and -10 < yy < 165):
                    r = 6.5 if yy < 120 else 6.5 * (1 - (yy - 120) / 60)
                    if r > 1: E(xx - r, yy - r, xx + r, yy + r, fill=P["hair"])
    else:
        E(-185, -200, 185, 160, fill=P["hair"], outline=P["line"], width=lw)
        R(-182, -40, 182, 168, 70, fill=P["hair"], outline=P["line"], width=lw)
        R(-178, 0, 178, 160, 60, fill=P["hair"])
    # face
    E(-134, -150, 134, 132, fill=P["skin"], outline=P["line"], width=lw)          # round, soft chin (chibi)
    E(-112, 30, 112, 146, fill=P["skin"])
    d.arc([X(-112), Y(30), X(112), Y(146)], 25, 155, fill=P["line"], width=lw)
    # cheeks
    for sx in (-1, 1): E(sx * 78 - 26, 62, sx * 78 + 26, 84, fill=P["cheek"])
    # eyes
    lx, ly = look
    for sx in (-1, 1):
        ex, ey = sx * 56, 8
        if expr == "happy" or blink > .85:
            d.arc([X(ex - 34), Y(ey - 20), X(ex + 34), Y(ey + 34)], 200, 340, fill=P["line"], width=int(9 * u))
            continue
        big = 1.18 if expr == "wow" else 1.0; hh = 46 * big * (1 - blink)
        E(ex - 36 * big, ey - hh, ex + 36 * big, ey + hh, fill=P["white"], outline=P["line"], width=lw)
        ix, iy = ex + lx * 6, ey + ly * 6 + 4
        if hh > 10:
            E(ix - 27 * big, iy - min(hh, 38 * big), ix + 27 * big, iy + min(hh, 38 * big), fill=P["iris"])
            E(ix - 27 * big, iy + min(hh, 38 * big) * .1, ix + 27 * big, iy + min(hh, 38 * big), fill=P["iris_d"])
            E(ix - 13 * big, iy - min(hh, 20 * big), ix + 13 * big, iy + min(hh, 20 * big), fill=P["line"])
            E(ix - 20 * big, iy - 26 * big, ix - 4 * big, iy - 10 * big, fill=P["white"])          # big highlight
            E(ix + 8 * big, iy + 10 * big, ix + 16 * big, iy + 18 * big, fill=P["white"])           # small highlight
        d.arc([X(ex - 40 * big), Y(ey - hh - 4), X(ex + 40 * big), Y(ey + hh)], 200, 340, fill=P["line"], width=int(10 * u))   # lash line
        d.line([X(ex + sx * 34 * big), Y(ey - hh * .55), X(ex + sx * 48 * big), Y(ey - hh * .8)], fill=P["line"], width=int(6 * u))
        # brows
        by = ey - 64 - (12 if expr == "wow" else 0)
        d.arc([X(ex - 30), Y(by - 10), X(ex + 30), Y(by + 14)], 210, 330, fill=P["line"], width=int(6 * u))
    # nose + mouth
    d.line([X(0), Y(58), X(-4), Y(64)], fill=P["skin_sh"], width=int(5 * u))
    mo = 1.0 if expr == "wow" else mouth
    if mo < .12:
        d.arc([X(-22), Y(78), X(22), Y(104)], 20, 160, fill=P["line"], width=int(6 * u))
    else:
        h = 8 + 26 * mo
        R(-18 - 6 * mo, 88, 18 + 6 * mo, 88 + h, 14, fill=P["mouth"], outline=P["line"], width=int(5 * u))
        if h > 16: R(-12, 88 + h * .55, 12, 88 + h - 3, 8, fill=P["tongue"])
    # bangs (over the forehead)
    if variant == "dots":
        for yy in range(-180, -50, 16):
            for xx in range(-150, 151, 16):
                if (xx / 150) ** 2 + ((yy + 130) / 120) ** 2 <= 1 and yy < -60 - 25 * abs(math.sin(xx / 30)):
                    E(xx - 6.5, yy - 6.5, xx + 6.5, yy + 6.5, fill=P["hair"])
    else:
        E(-152, -212, 152, -66, fill=P["hair"], outline=P["line"], width=lw)        # soft rounded bangs
        for x0 in (-112, -56, 0, 56, 112):
            E(x0 - 42, -126, x0 + 42, -44, fill=P["hair"])
            d.arc([X(x0 - 42), Y(-126), X(x0 + 42), Y(-44)], 20, 160, fill=P["line"], width=lw)
        for sx in (-1, 1): E(sx * 140 - 26, -110, sx * 140 + 26, 40, fill=P["hair"])  # side locks
        d.arc([X(-110), Y(-178), X(80), Y(-120)], 200, 330, fill=P["white"], width=int(8 * u))          # hair shine
    # headphones
    d.arc([X(-176), Y(-236), X(176), Y(80)], 200, 340, fill=P["phones"], width=int(26 * u))
    for sx in (-1, 1):
        R(sx * 168 - 34, -40, sx * 168 + 34, 70, 30, fill=P["phones"], outline=P["phones_d"], width=lw)
        E(sx * 168 - 12, 4, sx * 168 + 12, 28, fill=P["phones_d"])
    L = L.resize((W // SS, H // SS), Image.LANCZOS)
    img.paste(L, (int(cx - W / SS / 2), int(cy - 330 * s)), L)


# ---------------------------------------------------------------- Dot as a cat (chosen 02.11.2026: "less human, more cat-like")
CAT = dict(fur=(238, 238, 242), fur_sh=(204, 206, 218), chest=(255, 255, 255), line=(40, 36, 44), ear_in=(255, 176, 160),
           iris=(255, 92, 28), iris_d=(176, 44, 10), white=(255, 255, 255), nose=(255, 140, 130), mouth=(120, 30, 40),
           tongue=(255, 128, 118), whisker=(150, 150, 160), phones=(255, 84, 20), phones_d=(190, 52, 10), mark=(72, 72, 82))

def draw_cat(img, cx, cy, s=1.0, expr="talk", mouth=0.0, blink=0.0, pre_dark=False, look=(0, 0), tail=0.0, ears=0.0):
    """Dot the cat: round head, big eyes, ω mouth, whiskers, three dots on the forehead, orange headphones, small body + tail.
    (cx, cy) = head centre on the target image. tail: -1..1 sway, ears: 0..1 perk (twitch)."""
    SS = 2
    W, H = int(760 * s * SS), int(860 * s * SS)
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    P = {k: (_inv(v) if pre_dark else v + (255,)) for k, v in CAT.items()}
    u = s * SS; ox, oy = W / 2, 330 * u
    X = lambda x: ox + x * u; Y = lambda y: oy + y * u
    def E(x0, y0, x1, y1, **k): d.ellipse([X(x0), Y(y0), X(x1), Y(y1)], **k)
    def Pg(pts, **k): d.polygon([(X(a), Y(b)) for a, b in pts], **k)
    lw = max(2, int(5 * u))
    # tail (behind the body)
    sw = 40 * tail                                             # smooth S-curve tail, swaying at the tip
    pts = [(110 + 150 * math.sin(v * 1.6) + sw * v * v, 380 - 250 * v) for v in [i / 24 for i in range(25)]]
    d.line([(X(a), Y(b)) for a, b in pts], fill=P["line"], width=int(46 * u), joint="curve")
    d.line([(X(a), Y(b)) for a, b in pts], fill=P["fur"], width=int(36 * u), joint="curve")
    tx, ty = pts[-1]; E(tx - 19, ty - 19, tx + 19, ty + 19, fill=P["fur"]); E(tx - 18, ty - 26, tx + 18, ty + 6, fill=P["fur_sh"])
    # body (sitting) + paws
    E(-140, 90, 140, 420, fill=P["fur"], outline=P["line"], width=lw)           # small chibi body tucked under the head
    E(-74, 140, 74, 380, fill=P["chest"])
    for sx in (-1, 1):
        E(sx * 58 - 44, 368, sx * 58 + 44, 430, fill=P["fur"], outline=P["line"], width=lw)
        for k in (-1, 0, 1): d.line([X(sx * 58 + k * 15), Y(404), X(sx * 58 + k * 15), Y(426)], fill=P["fur_sh"], width=int(4 * u))
    # ears (perk = slight lift)
    ey_ = -8 * ears
    for sx in (-1, 1):
        Pg([(sx * 166, -30), (sx * 132, -238 + ey_), (sx * 24, -128)], fill=P["fur"], outline=P["line"], width=lw)
        Pg([(sx * 142, -62), (sx * 128, -196 + ey_), (sx * 54, -120)], fill=P["ear_in"])
    # head with cheek fluff
    E(-170, -150, 170, 140, fill=P["fur"], outline=P["line"], width=lw)
    for sx in (-1, 1):
        Pg([(sx * 150, 20), (sx * 196, 44), (sx * 160, 64), (sx * 190, 92), (sx * 140, 104)], fill=P["fur"], outline=P["line"], width=lw)
        Pg([(sx * 146, 18), (sx * 170, 50), (sx * 150, 72), (sx * 168, 92), (sx * 136, 102)], fill=P["fur"])
    E(-150, -132, 150, 130, fill=P["fur"])
    # forehead mark: three dots ("Dot")
    for k in (-1, 0, 1): E(k * 26 - 9, -112, k * 26 + 9, -94, fill=P["mark"])
    # eyes
    lx, ly = look
    for sx in (-1, 1):
        ex, ey = sx * 66, -14
        if expr == "happy" or blink > .85:
            d.arc([X(ex - 36), Y(ey - 18), X(ex + 36), Y(ey + 36)], 200, 340, fill=P["line"], width=int(10 * u)); continue
        big = 1.15 if expr == "wow" else 1.0; hh = 50 * big * (1 - blink)
        E(ex - 44 * big, ey - hh, ex + 44 * big, ey + hh, fill=P["white"], outline=P["line"], width=lw)
        ix, iy = ex + lx * 6, ey + ly * 6 + 3
        if hh > 12:
            r = min(hh, 42 * big)
            E(ix - 36 * big, iy - r, ix + 36 * big, iy + r, fill=P["iris"])
            E(ix - 36 * big, iy + r * .15, ix + 36 * big, iy + r, fill=P["iris_d"])
            pw = 20 * big if expr == "wow" else 12                                   # round pupils when amazed, slits otherwise
            E(ix - pw, iy - r * .78, ix + pw, iy + r * .78, fill=P["line"])
            E(ix - 26 * big, iy - 30 * big, ix - 6 * big, iy - 10 * big, fill=P["white"])
            E(ix + 10 * big, iy + 12 * big, ix + 20 * big, iy + 22 * big, fill=P["white"])
        d.arc([X(ex - 46 * big), Y(ey - hh - 4), X(ex + 46 * big), Y(ey + hh)], 205, 335, fill=P["line"], width=int(9 * u))
    # nose, ω mouth, whiskers
    Pg([(-13, 44), (13, 44), (0, 58)], fill=P["nose"], outline=P["line"], width=int(3 * u))
    mo = 1.0 if expr == "wow" else mouth
    if mo > .15:
        h = 10 + 30 * mo
        d.rounded_rectangle([X(-20 - 6 * mo), Y(64), X(20 + 6 * mo), Y(64 + h)], radius=int(14 * u), fill=P["mouth"], outline=P["line"], width=int(5 * u))
        if h > 18: d.rounded_rectangle([X(-13), Y(64 + h * .5), X(13), Y(64 + h - 3)], radius=int(8 * u), fill=P["tongue"])
    for sx in (-1, 1): d.arc([X(sx * 22 - 22), Y(50), X(sx * 22 + 22), Y(80)], 20, 160, fill=P["line"], width=int(5 * u))
    for sx in (-1, 1):
        for k, dy in enumerate((-10, 6, 22)):
            d.line([X(sx * 92), Y(44 + dy * .5), X(sx * 200), Y(30 + dy)], fill=P["whisker"], width=int(4 * u))
    # headphones: band between the ears, cups on the sides of the head
    d.arc([X(-160), Y(-196), X(160), Y(110)], 205, 335, fill=P["phones"], width=int(26 * u))
    for sx in (-1, 1):
        d.rounded_rectangle([X(sx * 172 - 32), Y(-40), X(sx * 172 + 32), Y(64)], radius=int(28 * u), fill=P["phones"], outline=P["phones_d"], width=lw)
        E(sx * 172 - 11, 0, sx * 172 + 11, 24, fill=P["phones_d"])
    L = L.resize((W // SS, H // SS), Image.LANCZOS)
    img.paste(L, (int(cx - W / SS / 2), int(cy - 330 * s)), L)
