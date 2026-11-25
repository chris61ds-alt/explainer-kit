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


def stamp_box(d, c, text, t, t0, size=90, col=None, ang=-12):
    """like fx2.stamp, but on a solid card (25.11.2026, No. 151): stays readable on top of a busy grid of objects"""
    import math
    if t < t0: return
    k = clamp((t - t0) / .22); s = 2.2 - 1.2 * ease(k) + (.12 * math.sin(math.pi * clamp((t - t0 - .22) / .18)) if t > t0 + .22 else 0)
    col = col or SIG; f = F(BLK, int(size * s)); tw = d.textlength(text, font=f); pad = size * s * .22
    im = Image.new("RGBA", (int(tw + 4 * pad), int(size * s * 1.6)), (0, 0, 0, 0)); g = ImageDraw.Draw(im)
    g.rounded_rectangle([pad * .5, pad * .5, im.width - pad * .5, im.height - pad * .5], radius=int(pad * .6), fill=BG + (255,),
                        outline=col + (255,), width=max(3, int(8 * s)))
    g.text((im.width / 2, im.height / 2), text, font=f, fill=col + (255,), anchor="mm")
    im = im.rotate(ang, expand=True, resample=Image.BICUBIC)
    d._image.paste(im, (int(c[0] - im.width / 2), int(c[1] - im.height / 2)), im)


def payoff_cam(img, draw, t, t0, focus=None, z1=1.1, dur=2.8):
    """rule 14 (25.11.2026): from t0 (start of the payoff) the camera slowly pushes in on the answer (z1 > 1) or pulls back
    to the whole picture (start with z1 < 1 is not possible -> use fx2.cam_path for pull-backs). draw(L, dL) paints the scene."""
    from fx2 import camera
    z = 1 + (z1 - 1) * ease(clamp((t - t0) / dur)) if t >= t0 else 1.0
    camera(img, draw, z, focus)
