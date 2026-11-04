"""'Bodies: all normal' helpers (No. 107/108): measuring ruler with a sliding range, a field of 'all different' blobs.
Deliberately no anatomical drawings (taste + platform rules)."""
import math, random
from thread import *

def ruler(d, x0, x1, y, v0, v1, lo, hi, k, unit="mm", col=INK, rng_col=SIG, ticks=10, label_every=None, fmt="{:.0f}"):
    """horizontal ruler v0..v1; the measured range lo..hi grows in with k (0..1)"""
    X = lambda v: x0 + (x1 - x0) * (v - v0) / (v1 - v0)
    d.line([x0, y, x1, y], fill=col, width=4)
    for i in range(ticks + 1):
        v = v0 + (v1 - v0) * i / ticks; x = X(v); big = label_every is None or i % label_every == 0
        d.line([x, y, x, y - (30 if big else 16)], fill=col, width=3)
        if big: d.text((x, y + 12), fmt.format(v), font=F(MONO, 24), fill=MID, anchor="ma")
    d.text((x1, y - 70), unit, font=F(MONO, 24), fill=MID, anchor="ra")
    if k > 0:
        kk = ease(clamp(k)); a, b = X(lo), X(lo + (hi - lo) * kk)
        d.rectangle([a, y - 64, b, y - 40], fill=rng_col)
        for xx in (a, b): d.line([xx, y - 76, xx, y - 28], fill=rng_col, width=5)

def blob(d, cx, cy, r, seed, col, k=1.0):
    """an irregular closed shape – every one different"""
    if k <= 0: return
    g = random.Random(seed); ph = [g.uniform(0, 6.28) for _ in range(3)]; am = [g.uniform(.05, .22) for _ in range(3)]
    sx, sy = g.uniform(.6, 1.0), g.uniform(.8, 1.3)
    pts = []
    for i in range(28):
        a = i / 28 * 2 * math.pi; rr = r * k * (1 + sum(am[j] * math.sin((j + 2) * a + ph[j]) for j in range(3)))
        pts.append((cx + rr * sx * math.cos(a), cy + rr * sy * math.sin(a)))
    d.polygon(pts, fill=col)

def blob_field(d, box, t, t0, n=60, col=INK, hi=(), hicol=SIG, step=.015, cell=96):
    x0, y0, x1, y1 = box; cols = int((x1 - x0) // cell)
    for i in range(n):
        r_, c_ = divmod(i, cols); cx, cy = x0 + cell / 2 + c_ * cell, y0 + cell / 2 + r_ * cell
        if cy > y1: break
        k = back(clamp((t - t0 - i * step) / .25)); g = random.Random(i * 7 + 3)
        blob(d, cx, cy, cell * g.uniform(.22, .42), i, hicol if i in hi else col, k)
