"""Dot the cat in the house style (look C+D): a halftone dot-matrix silhouette, orange headphones as the only colour,
features cut out of the dots (eyes, ω mouth, three forehead dots). Drawn in the light domain like every scene
(darken() turns dots light and holes dark afterwards).
dot_cat(img, d, cx, cy, s, t, expr="talk"|"happy"|"wow", mouth=0..1, blink=0..1, tail=-1..1, k=0..1 build-up)"""
import math
from thread import *

def _mask(m, cx, cy, s, tail):
    S = lambda v: v * s
    m.ellipse([cx - S(170), cy - S(150), cx + S(170), cy + S(140)], fill=255)                       # head
    for sx in (-1, 1):
        m.polygon([(cx + sx * S(166), cy - S(30)), (cx + sx * S(132), cy - S(238)), (cx + sx * S(24), cy - S(128))], fill=255)   # ears
        m.polygon([(cx + sx * S(150), cy + S(20)), (cx + sx * S(198), cy + S(46)), (cx + sx * S(162), cy + S(66)),
                   (cx + sx * S(192), cy + S(94)), (cx + sx * S(138), cy + S(106))], fill=255)       # cheek fluff
    m.ellipse([cx - S(140), cy + S(90), cx + S(140), cy + S(420)], fill=255)                         # body
    for sx in (-1, 1): m.ellipse([cx + sx * S(58) - S(44), cy + S(368), cx + sx * S(58) + S(44), cy + S(430)], fill=255)  # paws
    sw = 40 * tail
    pts = [(cx + S(110 + 150 * math.sin(v * 1.6) + sw * v * v), cy + S(380 - 250 * v)) for v in [i / 24 for i in range(25)]]
    m.line(pts, fill=255, width=int(S(38)), joint="curve"); x, y = pts[-1]; m.ellipse([x - S(19), y - S(19), x + S(19), y + S(19)], fill=255)

def dot_cat(img, d, cx, cy, s, t, expr="talk", mouth=0.0, blink=0.0, tail=0.0, k=1.0, cell=None, col=INK):
    cy = cy + 5 * s * math.sin(t * 3.1)                       # idle bob
    S = lambda v: v * s
    box = (int(cx - S(260)), int(cy - S(250)), int(cx + S(330)), int(cy + S(440)))
    silhouette(img, lambda m: _mask(m, cx, cy, s, tail), box, col, cell=cell or max(5, int(11 * s)), k=k, shade=.45)
    if k < .7: return
    # inner ears (cut out) + three forehead dots
    for sx in (-1, 1):
        d.polygon([(cx + sx * S(134), cy - S(74)), (cx + sx * S(126), cy - S(182)), (cx + sx * S(66), cy - S(122))], fill=MID)
    for j in (-1, 0, 1): d.ellipse([cx + S(j * 26 - 9), cy - S(112), cx + S(j * 26 + 9), cy - S(94)], fill=BG)
    # eyes: holes in the dots, orange iris, slit (or round, when amazed) pupil, a light glint
    for sx in (-1, 1):
        ex, ey = cx + sx * S(66), cy - S(14)
        if expr == "happy" or blink > .85:
            d.arc([ex - S(38), ey - S(18), ex + S(38), ey + S(38)], 200, 340, fill=BG, width=max(3, int(S(13)))); continue
        big = 1.15 if expr == "wow" else 1.0; hh = S(50) * big * (1 - blink)
        d.ellipse([ex - S(46) * big, ey - hh, ex + S(46) * big, ey + hh], fill=BG)
        if hh > S(12):
            r = min(hh, S(40) * big)
            d.ellipse([ex - S(34) * big, ey - r + S(3), ex + S(34) * big, ey + r + S(3)], fill=SIG)
            pw = S(19) * big if expr == "wow" else S(10)
            d.ellipse([ex - pw, ey - r * .78 + S(3), ex + pw, ey + r * .78 + S(3)], fill=BG)
            d.ellipse([ex - S(24) * big, ey - S(28) * big, ex - S(8) * big, ey - S(12) * big], fill=INK)
    # nose + ω mouth cut into the dots; open mouth when talking
    d.polygon([(cx - S(13), cy + S(42)), (cx + S(13), cy + S(42)), (cx, cy + S(56))], fill=BG)
    mo = 1.0 if expr == "wow" else mouth
    if mo > .15:
        h = S(10 + 28 * mo); d.rounded_rectangle([cx - S(18 + 6 * mo), cy + S(64), cx + S(18 + 6 * mo), cy + S(64) + h], radius=int(S(13)), fill=BG)
    for sx in (-1, 1): d.arc([cx + sx * S(22) - S(22), cy + S(48), cx + sx * S(22) + S(22), cy + S(80)], 20, 160, fill=BG, width=max(3, int(S(7))))
    # whiskers (outside the head they show on the background)
    for sx in (-1, 1):
        for dy in (-10, 6, 22):
            d.line([cx + sx * S(150), cy + S(44 + dy * .5), cx + sx * S(225), cy + S(32 + dy)], fill=MID, width=max(2, int(S(4))))
    # orange headphones: band between the ears, cups on the sides
    d.arc([cx - S(160), cy - S(196), cx + S(160), cy + S(110)], 205, 335, fill=SIG, width=max(4, int(S(26))))
    for sx in (-1, 1):
        d.rounded_rectangle([cx + sx * S(172) - S(32), cy - S(40), cx + sx * S(172) + S(32), cy + S(64)], radius=int(S(28)), fill=SIG)
