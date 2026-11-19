"""Helpers for the 'Where do you stand?' format (19.11.2026, after No. 138 reached ~5x the usual views on TikTok).
Idea: a question cover, one simple object (steps / a line of dots / bars), a 'YOU?' marker, and a payoff that stays (rule 15)."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from tips import BG, INK, MID, RULE, SIG, WHITE, F, BLK, MONO, clamp, ease, spring
from fx2 import is_light


def shadowed(EP, img, t, objects):
    """draw objects(L, d, t) on a paper layer and put it back with a soft drop shadow (light scenes only)"""
    if not is_light(EP, t):
        objects(img, ImageDraw.Draw(img), t); return
    L = Image.new("RGB", img.size, BG); objects(L, ImageDraw.Draw(L), t)
    a = np.asarray(L, np.int16); m = (np.abs(a - np.array(BG)).max(axis=2) > 10).astype(np.uint8) * 255
    m[:470] = 0; m[1186:] = 0
    M = Image.fromarray(m); sh = Image.new("L", img.size, 0); sh.paste(M, (16, 18))
    k = np.asarray(sh.filter(ImageFilter.GaussianBlur(14)), np.float32)[..., None] / 255 * .3
    out = np.asarray(img, np.float32) * (1 - k) + k * np.array(INK, np.float32)
    img.paste(Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))); img.paste(L, (0, 0), M)


def dashed(d, p0, p1, col, w=4, dash=22, gap=16):
    (x0, y0), (x1, y1) = p0, p1
    n = max(1, int(((x1 - x0) ** 2 + (y1 - y0) ** 2) ** .5 // (dash + gap)))
    for i in range(n + 1):
        u0 = i / (n + 1e-9) if n else 0; u1 = min(1, u0 + dash / max(1, ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** .5))
        d.line([(x0 + (x1 - x0) * u0, y0 + (y1 - y0) * u0), (x0 + (x1 - x0) * u1, y0 + (y1 - y0) * u1)], fill=col, width=w)


def you_marker(d, x, y, t, t0, col=SIG, label="YOU?"):
    """a pin with a 'YOU?' bubble that drops in at t0"""
    if t < t0: return
    k = spring(clamp((t - t0) / .45)); yy = y - 40 * (1 - k)
    d.polygon([(x, yy), (x - 14, yy - 26), (x + 14, yy - 26)], fill=col)
    f = F(BLK, 34); w = d.textlength(label, font=f)
    d.rounded_rectangle([x - w / 2 - 16, yy - 84, x + w / 2 + 16, yy - 26], radius=14, fill=col)
    d.text((x, yy - 55), label, font=f, fill=WHITE, anchor="mm")
