"""MAPS (27.11.2026, Chris: "Google-Maps-Karten wären ein spannendes Medium"): a satellite "Google-Earth" zoom and route
animations, as a cut-away (same interface as board.VideoInsert: .render(tl, k) -> float array H x W x 3).

Imagery: EOX Sentinel-2 cloudless – ONLY the 2016/2017 layers are CC BY 4.0 (2018+ are CC BY-NC-SA = not allowed by
our image rules), so LAYERS below is a hard allowlist. Credit line: CREDIT. Tiles are cached in ~/.cache/njy_tiles.

    from maps import MapInsert, CREDIT
    m = MapInsert(cam=[(0, lon, lat, zoom), (3.5, lon2, lat2, zoom2)],          # zoom = Web-Mercator level (float)
                  routes=[dict(pts=[(lon, lat), ...], t0=1.0, t1=3.0, color=RED)],
                  marks=[dict(lon=..., lat=..., t=2.0, label="NOV 25, 1872")], grade=(.95, .2, .3))
    EP.inserts.append((t0, t1, m, "THE ROUTE", CREDIT))
"""
import math, os, io, threading
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import requests
from PIL import Image, ImageDraw, ImageFilter
from cute import F, BLK, MONO, W, H, clamp, ease, ease_io, lerp

LAYERS = {"s2cloudless_3857": 2016, "s2cloudless-2017_3857": 2017}          # CC BY 4.0 only – never add 2018+
LAYER = "s2cloudless_3857"
URL = "https://tiles.maps.eox.at/wmts/1.0.0/{layer}/default/g/{z}/{y}/{x}.jpg"
CREDIT = "SENTINEL-2 CLOUDLESS 2016 BY EOX · MODIFIED COPERNICUS SENTINEL DATA · CC BY 4.0"
CACHE = os.path.expanduser("~/.cache/njy_tiles")
MAXZ = 15
RED, WHITE, GOLD = (214, 48, 40), (245, 240, 230), (222, 178, 92)
_mem = {}
_lock = threading.Lock()
_sess = requests.Session(); _sess.headers["User-Agent"] = "NotJustYouReels/1.0 (github.com/chris61ds-alt/explainer-kit)"


def merc(lon, lat, z):
    """lon/lat -> global pixel at zoom z (float z allowed)"""
    n = 256 * 2 ** z; lat = max(-85.0, min(85.0, lat))
    x = (lon + 180) / 360 * n
    y = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
    return x, y


def tile(z, x, y, layer=LAYER):
    assert layer in LAYERS, "only CC BY 4.0 layers"
    n = 2 ** z; x %= n
    if y < 0 or y >= n: return None
    key = (layer, z, x, y)
    if key in _mem: return _mem[key]
    p = os.path.join(CACHE, layer, str(z), str(y), f"{x}.jpg")
    if not os.path.exists(p):
        os.makedirs(os.path.dirname(p), exist_ok=True)
        for i in range(4):
            try:
                r = _sess.get(URL.format(layer=layer, z=z, y=y, x=x), timeout=30)
                if r.status_code == 200: open(p, "wb").write(r.content); break
            except requests.RequestException:
                pass
        else:
            return None
    im = Image.open(p).convert("RGB")
    with _lock:
        if len(_mem) > 1500: _mem.clear()
        _mem[key] = im
    return im


def view(lon, lat, z, layer=LAYER):
    """1080x1920 satellite frame centred on lon/lat at float zoom z (tiles of level ceil(z), scaled down)"""
    zi = min(MAXZ, math.ceil(z - 1e-6)); s = 2 ** (z - zi)                 # s <= 1: scale of level-zi pixels
    cx, cy = merc(lon, lat, zi); hw, hh = W / 2 / s, H / 2 / s
    x0, y0, x1, y1 = cx - hw, cy - hh, cx + hw, cy + hh
    tx0, ty0, tx1, ty1 = int(x0 // 256), int(y0 // 256), int(x1 // 256), int(y1 // 256)
    canvas = Image.new("RGB", ((tx1 - tx0 + 1) * 256, (ty1 - ty0 + 1) * 256), (8, 14, 22))
    need = [(tx, ty) for ty in range(ty0, ty1 + 1) for tx in range(tx0, tx1 + 1)]
    with ThreadPoolExecutor(6) as ex: ims = list(ex.map(lambda p: tile(zi, p[0], p[1], layer), need))
    for (tx, ty), im in zip(need, ims):
        if im is not None: canvas.paste(im, ((tx - tx0) * 256, (ty - ty0) * 256))
    ox, oy = x0 - tx0 * 256, y0 - ty0 * 256
    return canvas.transform((W, H), Image.AFFINE, (1 / s, 0, ox, 0, 1 / s, oy), resample=Image.BILINEAR)


def prefetch(cam, fps=10, layer=LAYER):
    """download every tile a camera path needs (call once before rendering)"""
    t_end = cam[-1][0]
    for i in range(int(t_end * fps) + 2):
        lon, lat, z = cam_at(cam, i / fps); view(lon, lat, z, layer)


def cam_at(cam, t):
    """camera keys (t, lon, lat, z): zoom eased, position follows in Mercator space (looks like a real flight)"""
    if t <= cam[0][0]: return cam[0][1:]
    for (t0, a0, b0, z0), (t1, a1, b1, z1) in zip(cam, cam[1:]):
        if t0 <= t < t1:
            e = ease_io((t - t0) / max(.01, t1 - t0)); z = lerp(z0, z1, e)
            # the centre arrives early (62 % of the move), the zoom keeps going: reads like a real flight, no detours
            zr = min(z0, z1); xa, ya = merc(a0, b0, zr); xb, yb = merc(a1, b1, zr)
            k = ease_io(clamp((t - t0) / max(.01, (t1 - t0) * .62))); x, y = lerp(xa, xb, k), lerp(ya, yb, k)
            n = 256 * 2 ** zr; lon = x / n * 360 - 180
            lat = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n))))
            return lon, lat, z
    return cam[-1][1:]


class MapInsert:
    def __init__(self, cam, routes=(), marks=(), grade=(1.0, .1, .15), layer=LAYER, labels=()):
        assert layer in LAYERS, "only CC BY 4.0 layers"
        self.cam, self.routes, self.marks, self.grade, self.layer, self.labels = cam, routes, marks, grade, layer, labels
        prefetch(cam, layer=layer)

    def to_screen(self, lon, lat, clon, clat, z):
        cx, cy = merc(clon, clat, z); x, y = merc(lon, lat, z); return W / 2 + x - cx, H / 2 + y - cy

    def render(self, tl, k):
        lon, lat, z = cam_at(self.cam, tl)
        img = view(lon, lat, z, self.layer)
        b, warm, sep = self.grade
        a = np.asarray(img, np.float32) * b
        if sep:
            g = a @ np.array([.299, .587, .114], np.float32); a = a * (1 - sep) + np.stack([g * 1.03, g * .95, g * .82], -1) * sep
        a[..., 0] *= 1 + .06 * warm; a[..., 2] *= 1 - .06 * warm
        img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        for r in self.routes:                                                 # route drawn progressively
            if tl < r["t0"]: continue
            e = ease_io(clamp((tl - r["t0"]) / max(.01, r["t1"] - r["t0"])))
            pts = [self.to_screen(p[0], p[1], lon, lat, z) for p in r["pts"]]
            seg = [0]
            for p, q in zip(pts, pts[1:]): seg.append(seg[-1] + math.dist(p, q))
            L = seg[-1] * e; out = [pts[0]]
            for i in range(1, len(pts)):
                if seg[i] <= L: out.append(pts[i])
                else:
                    f = (L - seg[i - 1]) / max(1e-6, seg[i] - seg[i - 1]); out.append((lerp(pts[i - 1][0], pts[i][0], f), lerp(pts[i - 1][1], pts[i][1], f))); break
            col = r.get("color", RED)
            if len(out) > 1:
                d.line(out, fill=(0, 0, 0, 120), width=r.get("w", 9) + 6, joint="curve")
                d.line(out, fill=col + (255,), width=r.get("w", 9), joint="curve")
            if r.get("dashed_head", True) and len(out) > 1:
                x, y = out[-1]; d.ellipse([x - 12, y - 12, x + 12, y + 12], fill=col + (255,))
        for m in self.marks:                                                  # markers + typed labels
            if tl < m["t"]: continue
            e = ease(clamp((tl - m["t"]) / .3)); x, y = self.to_screen(m["lon"], m["lat"], lon, lat, z)
            r_ = 16 + 14 * (1 - e); col = m.get("color", RED)
            if m.get("cross"):
                d.line([(x - r_, y - r_), (x + r_, y + r_)], fill=col + (255,), width=8); d.line([(x - r_, y + r_), (x + r_, y - r_)], fill=col + (255,), width=8)
            else:
                d.ellipse([x - r_, y - r_, x + r_, y + r_], outline=col + (255,), width=7)
            if m.get("label"):
                f = F(MONO, 34); tw = d.textlength(m["label"], font=f); lx = min(W - tw - 70, max(50, x + 30)); ly = y - 30
                d.rectangle([lx - 14, ly - 8, lx + tw + 14, ly + 44], fill=(14, 14, 14, int(225 * e)))
                d.text((lx, ly), m["label"], font=f, fill=WHITE + (int(255 * e),))
        for lb in self.labels:                                                # place names (fade with zoom window)
            zmin, zmax = lb.get("z", (0, 30))
            if not (zmin <= z <= zmax) or tl < lb.get("t", 0): continue
            x, y = self.to_screen(lb["lon"], lb["lat"], lon, lat, z); f = F(BLK, lb.get("size", 44))
            d.text((x + 2, y + 3), lb["text"], font=f, fill=(0, 0, 0, 170), anchor="mm"); d.text((x, y), lb["text"], font=f, fill=WHITE + (235,), anchor="mm")
        img.alpha_composite(ov)
        return np.asarray(img.convert("RGB"), np.float32)
