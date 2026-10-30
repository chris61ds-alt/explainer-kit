"""Dating-app props for the Dataclysm / OkTrends episodes (look C+D): profile cards, chat bubbles, histograms, beer glass."""
import math
from thread import *

def profile_card(img, d, cx, cy, s=1.0, photo=1.0, col=INK, text=1.0, badge=None, badge_col=SIG, cell=7, ph_col=None, cross_text=False):
    """dating profile: rounded frame, halftone photo (photo = 0..1 visibility; 0 shows a '?' slot), bio lines, optional badge"""
    w, h = 270 * s, 450 * s; x0, y0 = cx - w / 2, cy - h / 2
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=int(22 * s), outline=col, width=max(3, int(5 * s)))
    px0, py0, px1, py1 = x0 + 16 * s, y0 + 16 * s, x0 + w - 16 * s, y0 + 16 * s + 250 * s
    d.rounded_rectangle([px0, py0, px1, py1], radius=int(12 * s), fill=mix(BG, col, .06))
    if photo > 0:
        silhouette(img, lambda m: front_bust(m, cx, py0 + 115 * s, .36 * s, 255), (int(px0), int(py0), int(px1), int(py1)), ph_col or col, cell=cell, k=photo)
    if photo < 1:
        d.text((cx, (py0 + py1) / 2), "?", font=F(BLK, int(120 * s)), fill=mix(BG, MID, 1 - photo), anchor="mm")
    if text > 0:
        for i, f in enumerate((.82, .64, .74)):
            y = py1 + (26 + i * 34) * s; xe = px0 + (px1 - px0) * f * clamp(text)
            d.rounded_rectangle([px0, y, xe, y + 14 * s], radius=int(7 * s), fill=mix(BG, MID, .8))
            if cross_text: d.line([px0 - 6, y + 7 * s, px0 + (px1 - px0) * f + 6, y + 7 * s], fill=SIG, width=max(3, int(4 * s)))
    if badge: box_label(d, cx, y0 + h - 44 * s, badge, int(30 * s), WHITE, badge_col, font=BLK, anchor="ma")

def bubbles(d, x0, x1, y0, n, k=1.0, col=INK, alt=SIG, h=54, gap=18, fade=None):
    """chat thread: n bubbles alternating left/right, revealed with k (0..1); fade: optional per-bubble alpha list"""
    shown = n * clamp(k)
    for i in range(n):
        a = clamp(shown - i)
        if fade is not None: a *= fade[i]
        if a <= 0: continue
        left = i % 2 == 0; w = (x1 - x0) * (.55 if i % 3 else .42)
        bx0 = x0 if left else x1 - w; y = y0 + i * (h + gap)
        d.rounded_rectangle([bx0, y, bx0 + w, y + h], radius=h // 2, fill=mix(BG, col if left else alt, a))

def hist(d, x0, y_base, vals, k=1.0, bw=120, gap=24, hmax=380, col=INK, hi=(), hicol=SIG, labels=None):
    """vertical bars (schematic distributions); hi = indices drawn in hicol"""
    for i, v in enumerate(vals):
        kk = ease((k * (len(vals) + 2) - i) / 2); x = x0 + i * (bw + gap)
        d.rectangle([x, y_base - hmax * v * kk, x + bw, y_base], fill=hicol if i in hi else col)
        if labels: d.text((x + bw / 2, y_base + 14), labels[i], font=F(MONO, 22), fill=MID, anchor="ma")
    d.line([x0 - 10, y_base, x0 + len(vals) * (bw + gap) - gap + 10, y_base], fill=INK, width=4)

def beer(d, cx, base, s=1.0, k=1.0, t=0.0, col=INK):
    """pint glass, filled with k (0..1), rising bubbles"""
    w0, w1, h = 120 * s, 160 * s, 360 * s
    top = base - h; lvl = base - (h - 40 * s) * clamp(k)
    def xw(y): u = (base - y) / h; return (w0 + (w1 - w0) * u) / 2
    d.polygon([(cx - xw(lvl), lvl), (cx + xw(lvl), lvl), (cx + w0 / 2, base), (cx - w0 / 2, base)], fill=SIG)
    if k > .9:
        for i in range(5): r = 26 * s; d.ellipse([cx - xw(lvl) + i * 34 * s - 6, lvl - r - 6, cx - xw(lvl) + i * 34 * s + 2 * r - 6, lvl + r - 6], fill=WHITE)
        for i in range(7):
            y = base - ((t * 140 + i * 53) % (base - lvl - 20)) - 10; x = cx + math.sin(i * 2.1) * 34 * s
            d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=WHITE)
    d.line([(cx - w1 / 2, top), (cx - w0 / 2, base), (cx + w0 / 2, base), (cx + w1 / 2, top)], fill=col, width=int(8 * s), joint="curve")
