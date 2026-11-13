"""Level-2 building blocks (12.11.2026, after the "Funfacts" reels): camera moves, glow, particles.
   camera(img, draw, zoom, focus)   – draw the scene on a layer, then crop/zoom it into the object band (headline stays put)
   glow(img, shapes, col, r, k)     – soft light bloom around polygons/circles (lit windows, "active" things)
   stream(...) / dots(...)          – thousands of particles flowing along a path, drawn fast with numpy
All are deterministic in t, so any frame can be rendered on its own (stills, parallel renders)."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from swiss import BG, INK, W, H, clamp, ease

BAND = (0, 470, W, 1180)                 # where the object lives; headline above, subtitles below

def lerp(a, b, k): return a + (b - a) * k

def camera(img, draw, zoom=1.0, focus=None, band=BAND):
    """draw(L, dL) paints the scene in normal coordinates on a full-size layer; the band of img then shows that
    layer zoomed by `zoom` around `focus` (x, y in layer coordinates; default: band centre)."""
    L = Image.new("RGB", img.size, BG); draw(L, ImageDraw.Draw(L))
    x0, y0, x1, y1 = band; bw, bh = x1 - x0, y1 - y0
    fx, fy = focus or ((x0 + x1) / 2, (y0 + y1) / 2)
    cw, ch = bw / zoom, bh / zoom
    cx0 = min(max(fx - cw / 2, 0), img.size[0] - cw); cy0 = min(max(fy - ch / 2, 0), img.size[1] - ch)
    crop = L.resize((bw, bh), Image.LANCZOS, box=(cx0, cy0, cx0 + cw, cy0 + ch))
    img.paste(crop, (x0, y0))

def cam_path(t, keys):
    """keys: [(t, zoom, (fx, fy)), ...] – eased moves between keyframes (holds before the first / after the last)"""
    if t <= keys[0][0]: return keys[0][1], keys[0][2]
    for (ta, za, fa), (tb, zb, fb) in zip(keys, keys[1:]):
        if t < tb:
            k = ease((t - ta) / max(1e-6, tb - ta)); return lerp(za, zb, k), (lerp(fa[0], fb[0], k), lerp(fa[1], fb[1], k))
    return keys[-1][1], keys[-1][2]

def glow(img, shapes, col=INK, r=28, k=.8):
    """soft bloom: shapes = list of polygons (list of points) or circles ('c', x, y, rad). Frames are drawn in the light
    domain and inverted for dark episodes (thread.darken), so the default col=INK becomes a white glow on dark."""
    if k <= 0 or not shapes: return
    m = Image.new("L", img.size, 0); dm = ImageDraw.Draw(m)
    for s in shapes:
        if s and s[0] == "c": _, x, y, rad = s; dm.ellipse([x - rad, y - rad, x + rad, y + rad], fill=255)
        else: dm.polygon(s, fill=255)
    a = np.asarray(m.filter(ImageFilter.GaussianBlur(r)), np.float32)[..., None] / 255 * k
    out = np.asarray(img, np.float32) * (1 - a) + a * np.array(col, np.float32)
    img.paste(Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)))

def dots(img, xy, col, size=3):
    """draw many square dots fast (xy: N×2 array of pixel positions)"""
    if len(xy) == 0: return
    a = np.array(img); h, w = a.shape[:2]; s = size // 2
    xi = np.round(xy[:, 0]).astype(int); yi = np.round(xy[:, 1]).astype(int)
    for dx in range(-s, size - s):
        for dy in range(-s, size - s):
            x, y = xi + dx, yi + dy; ok = (x >= 0) & (x < w) & (y >= 0) & (y < h)
            a[y[ok], x[ok]] = col
    img.paste(Image.fromarray(a))

class Stream:
    """n particles flowing along a polyline path (pixel coords). Each particle has its own phase, lane offset and wobble.
    pos(t, flow, active): flow = how far they travel per second (fraction of the path), active = share of particles shown."""
    def __init__(self, path, n=1500, width=26, seed=1):
        P = np.asarray(path, np.float32); seg = np.sqrt(((P[1:] - P[:-1]) ** 2).sum(1))
        self.P, self.cum = P, np.concatenate([[0], np.cumsum(seg)]); self.L = self.cum[-1]
        R = np.random.RandomState(seed); self.n = n
        self.ph, self.lane, self.wob, self.spd = R.rand(n), R.randn(n) * width / 2, R.rand(n) * 6.28, .75 + R.rand(n) * .5
    def at(self, s):
        d = s * self.L; i = np.clip(np.searchsorted(self.cum, d) - 1, 0, len(self.P) - 2)
        k = ((d - self.cum[i]) / np.maximum(1e-6, self.cum[i + 1] - self.cum[i]))[:, None]
        p = self.P[i] + (self.P[i + 1] - self.P[i]) * k; t_ = self.P[i + 1] - self.P[i]
        nrm = np.stack([-t_[:, 1], t_[:, 0]], 1) / np.maximum(1e-6, np.sqrt((t_ ** 2).sum(1)))[:, None]
        return p, nrm
    def pos(self, t, flow=.25, active=1.0):
        on = np.arange(self.n) < int(self.n * clamp(active))
        s = (self.ph + t * flow * self.spd) % 1.0
        p, nrm = self.at(s)
        off = self.lane + 6 * np.sin(t * 3 + self.wob)
        taper = np.sin(np.pi * s) ** .5                      # thin at both ends: comes out of the door, goes into the door
        return (p + nrm * (off * taper)[:, None])[on]

def _hull(pts):
    pts = sorted(set(pts))
    if len(pts) < 3: return pts
    def cr(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]

def soft_shadow(img, iso, boxes, light=(.55, .3), r=16, k=.32, col=INK):
    """soft drop shadows on the floor (light look, 13.11.2026): boxes = [(x, y, a, b, h), ...] in iso coordinates.
    The shadow is the footprint smeared away from the light by the object's height, blurred, and blended toward col."""
    m = Image.new("L", img.size, 0); dm = ImageDraw.Draw(m)
    for x, y, a, b, h in boxes:
        c = [(x, y), (x + a, y), (x + a, y + b), (x, y + b)]
        pts = [iso.P(px, py, 0) for px, py in c] + [iso.P(px + light[0] * h, py + light[1] * h, 0) for px, py in c]
        dm.polygon(_hull([(round(p[0], 1), round(p[1], 1)) for p in pts]), fill=255)
    a_ = np.asarray(m.filter(ImageFilter.GaussianBlur(r)), np.float32)[..., None] / 255 * k
    out = np.asarray(img, np.float32) * (1 - a_) + a_ * np.array(col, np.float32)
    img.paste(Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)))
