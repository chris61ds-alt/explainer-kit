"""Isometric object scenes (03.11.2026) – technical line drawings in the look C+D: white/grey faces, ink outlines,
numbered call-outs (mono labels; the answer in orange), floor grid that fades out, parts that drop in one by one.
Drawn in the light domain like every scene; meant for light scenes (EP.bg = {"scene": "light"}), works dark too.

Usage:
    from iso import *
    I = Iso(480, 1000, .78)                      # screen origin of the floor point (0, 0, 0) + scale
    I.grid(img); I.shadow(d, 0, 0, 230)
    v, dz = drop(t, t0)                          # part visible? + its height offset while it drops in
    if v: I.cyl(d, 0, 0, 0 + dz, 120, 14)
    callout(d, I.P(0, 0, 220), "r", 700, 1, "LABEL", k=(t - t1) / .4)
"""
import math
import numpy as np
from PIL import Image, ImageDraw
from swiss import BG, INK, MID, SIG, RULE, WHITE, F, MONO, X0, X1, clamp, ease, back

TOP, LEFT, RIGHT, SHADOW = WHITE, (234, 234, 230), (212, 212, 208), (222, 222, 217)
C30, S30 = math.cos(math.pi / 6), .5

class Iso:
    def __init__(self, ox=480, oy=1000, sc=.78, lw=4):
        self.ox, self.oy, self.sc, self.lw = ox, oy, sc, lw

    def P(self, x, y, z=0):
        return (self.ox + (x - y) * C30 * self.sc, self.oy + ((x + y) * S30 - z) * self.sc)

    def poly(self, d, pts, fill):
        d.polygon(pts, fill=fill); d.line(pts + [pts[0]], fill=INK, width=self.lw, joint="curve")

    def box(self, d, x, y, z, a, b, h, top=TOP, left=LEFT, right=RIGHT):
        P = self.P
        self.poly(d, [P(x, y + b, z), P(x + a, y + b, z), P(x + a, y + b, z + h), P(x, y + b, z + h)], left)
        self.poly(d, [P(x + a, y, z), P(x + a, y + b, z), P(x + a, y + b, z + h), P(x + a, y, z + h)], right)
        self.poly(d, [P(x, y, z + h), P(x + a, y, z + h), P(x + a, y + b, z + h), P(x, y + b, z + h)], top)

    def ell(self, x, y, z, r, n=72):
        return [self.P(x + r * math.cos(a), y + r * math.sin(a), z) for a in np.linspace(0, 2 * math.pi, n, endpoint=False)]

    def cyl(self, d, x, y, z, r, h, top=TOP, side=LEFT):
        lo, hi = self.ell(x, y, z, r), self.ell(x, y, z + h, r); n = len(lo)
        xs = [p[0] for p in lo]; il, ir = int(np.argmin(xs)), int(np.argmax(xs))
        front = [lo[(il - i) % n] for i in range((il - ir) % n + 1)]       # visible lower half of the bottom ellipse
        if h > 0:
            d.polygon([hi[il]] + front + [hi[ir]], fill=side)
            d.line([hi[il], lo[il]], fill=INK, width=self.lw); d.line([hi[ir], lo[ir]], fill=INK, width=self.lw)
            d.line(front, fill=INK, width=self.lw)
        self.poly(d, hi, top)

    def shadow(self, d, x, y, r, k=1.0):
        if k > 0: d.polygon(self.ell(x + 40, y + 40, 0, r * clamp(k)), fill=SHADOW)

    def grid(self, img, n=6, step=110, fade_h=300, cy=None):
        """dashed floor grid, faded out above/below the floor so it never runs into the type"""
        g = Image.new("RGB", img.size, BG); d = ImageDraw.Draw(g); cy = self.oy if cy is None else cy
        for i in range(-n, n + 1):
            for a, b in (((i * step, -n * step), (i * step, n * step)), ((-n * step, i * step), (n * step, i * step))):
                p, q = self.P(*a), self.P(*b); k = int(math.dist(p, q) // 22)
                for j in range(0, k, 2):
                    u0, u1 = j / k, (j + 1) / k
                    d.line([(p[0] + (q[0] - p[0]) * u0, p[1] + (q[1] - p[1]) * u0), (p[0] + (q[0] - p[0]) * u1, p[1] + (q[1] - p[1]) * u1)], fill=RULE, width=2)
        yy = np.arange(img.size[1])[:, None]; fade = np.clip(1 - np.abs(yy - cy) / fade_h, 0, 1)
        m = Image.fromarray((np.broadcast_to(fade, (img.size[1], img.size[0])) * 255).astype(np.uint8))
        bg = Image.new("RGB", img.size, BG)                                   # only where the frame is still empty paper
        empty = (np.abs(np.asarray(img).astype(np.int16) - np.array(BG)).max(axis=2) < 6)
        m = Image.fromarray((np.asarray(m) * empty).astype(np.uint8)); img.paste(g, (0, 0), m)

def drop(t, t0, h=140, dur=.28):
    """a part that falls into place: (visible, z offset)"""
    if t < t0: return False, 0.0
    return True, h * (1 - ease(clamp((t - t0) / dur)))

def callout(d, anchor, side, y, n, label, col=INK, k=1.0, size=30):
    """numbered call-out: dot on the part → leader line to the margin → circled number + mono label (animated with k)"""
    if k <= 0: return
    ax, ay = anchor; ex = X0 + 26 if side == "l" else X1 - 26
    k1, k2 = ease(clamp(k / .5)), clamp((k - .4) / .6)
    d.ellipse([ax - 7, ay - 7, ax + 7, ay + 7], fill=col)
    d.line([(ax, ay), (ax + (ex - ax) * k1, ay + (y - ay) * k1)], fill=col, width=3)
    if k2 > 0:
        r = 26 * back(k2); d.ellipse([ex - r, y - r, ex + r, y + r], fill=BG, outline=col, width=4)
        if k2 > .5: d.text((ex, y), str(n), font=F(MONO, size), fill=col, anchor="mm")
        if k2 > .3: d.text((ex - 26 if side == "l" else ex + 26, y - 40), label, font=F(MONO, size), fill=col, anchor="ld" if side == "l" else "rd")

def parts_counter(d, x, y, n, total, label="PARTS"):
    """'PARTS 6 / 8' read-out (right-aligned at x)"""
    d.text((x, y), label, font=F(MONO, 26), fill=MID, anchor="ra")
    w = d.textlength(f" / {total}", font=F(MONO, 34))
    d.text((x, y + 34), f" / {total}", font=F(MONO, 34), fill=MID, anchor="ra")
    d.text((x - w, y + 30), f"{n}", font=F(MONO, 64), fill=INK, anchor="ra")
    d.line([x - 220, y + 112, x, y + 112], fill=MID, width=2)
