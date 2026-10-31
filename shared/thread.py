"""'Swiss Thread' (v3) – extension of the Swiss toolkit, inspired by editorial motion design:
one continuous signal-coloured thread that runs through every scene (it enters and leaves each scene at THREAD_Y, so the
horizontal slide between scenes looks like one unbroken line) · halftone / dot-matrix rendering of pictograms ·
lab annotations (bounding boxes with normalised coordinates, data-track labels) · pixel / band glitch · micro-cuts.

Usage:
    from thread import *
    EP = ThreadEpisode(TL, 54, "LIE DETECTOR", order=ORDER, chapters=..., dark=True, ...)
    def sc_hook(img, d, t): ... draw_thread(d, pts) ...
"""
import os, sys, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from swiss import *
from swiss import Episode
import numpy as np
from PIL import Image, ImageDraw

THREAD_Y = 860                     # every scene's thread enters (x < 0) and leaves (x > W) at this height
LX, RX = -20, W + 20

# ---------------------------------------------------------------- geometry
def spline(pts, n=12):
    """Catmull-Rom through pts (list of (x, y)); returns dense point list"""
    if len(pts) < 3: return list(pts)
    P = [pts[0]] + list(pts) + [pts[-1]]; out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for j in range(n):
            s = j / n; s2, s3 = s * s, s * s * s
            out.append(tuple(.5 * ((2 * p1[c]) + (-p0[c] + p2[c]) * s + (2 * p0[c] - 5 * p1[c] + 4 * p2[c] - p3[c]) * s2 +
                                   (-p0[c] + 3 * p1[c] - 3 * p2[c] + p3[c]) * s3) for c in (0, 1)))
    out.append(pts[-1]); return out

def curl(x, y, r=34, d=1, n=26):
    """a small loop (like a knot in a thread) centred above (x, y); d = direction"""
    return [(x + d * r * math.sin(a), y - r + r * math.cos(a)) for a in np.linspace(0, 2 * math.pi, n)]

def path(*parts):
    """concatenate parts: tuples are waypoints, lists are pre-sampled point runs (e.g. curl())"""
    out = []
    for p in parts:
        if isinstance(p, list): out.extend(p)
        else: out.append(p)
    return out

def length(pts): return sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))

def draw_thread(d, pts, k=1.0, col=SIG, width=7, smooth=True):
    """draw the thread up to fraction k of its length (draw-on animation)"""
    pts = spline(pts) if smooth else pts
    if k <= 0 or len(pts) < 2: return []
    L = length(pts) * clamp(k); acc, out = 0.0, [pts[0]]
    for i in range(len(pts) - 1):
        seg_ = math.dist(pts[i], pts[i + 1])
        if acc + seg_ >= L:
            f = (L - acc) / max(seg_, 1e-6); out.append((lerp(pts[i][0], pts[i + 1][0], f), lerp(pts[i][1], pts[i + 1][1], f))); break
        acc += seg_; out.append(pts[i + 1])
    d.line(out, fill=col, width=width, joint="curve")
    return out

def trace(x0, x1, y, t, amp=40, speed=1.0, seed=0, spikes=(), step=6):
    """polygraph-like scribble from x0 to x1 around y; spikes: [(x_frac, height, width_frac)]"""
    rnd = random.Random(seed); ph = [rnd.random() * 6 for _ in range(4)]; out = []
    for x in range(int(x0), int(x1) + 1, step):
        u = (x - x0) / max(1, x1 - x0)
        v = (math.sin(u * 31 + t * 7 * speed + ph[0]) * .5 + math.sin(u * 67 - t * 11 * speed + ph[1]) * .3 +
             math.sin(u * 140 + t * 17 * speed + ph[2]) * .2)
        env = 1.0
        for (sx, sh_, sw) in spikes: env += sh_ * math.exp(-((u - sx) / max(sw, 1e-3)) ** 2)
        out.append((x, y + v * amp * env))
    return out

# ---------------------------------------------------------------- texture
def halftone(img, draw_fn, box, cell=12, col=INK, k=1.0, gain=1.0, shade=.65, light=(-.6, -.8)):
    """render draw_fn(mask_draw) into a mask and show it as a dot matrix inside box (x0, y0, x1, y1).
    shade: 0 = flat dots, 1 = strong directional shading (light from `light` direction) + edge falloff"""
    if k <= 0: return
    x0, y0, x1, y1 = [int(v) for v in box]
    mask = Image.new("L", (W, H), 0); draw_fn(ImageDraw.Draw(mask))
    a = np.asarray(mask, dtype=np.float32)[y0:y1, x0:x1]
    h, w = (a.shape[0] // cell) * cell, (a.shape[1] // cell) * cell
    if h <= 0 or w <= 0: return
    m = a[:h, :w].reshape(h // cell, cell, w // cell, cell).mean((1, 3)) / 255.0
    if shade > 0:
        gy, gx = np.mgrid[0:m.shape[0], 0:m.shape[1]]
        u = (gx / max(1, m.shape[1] - 1) - .5) * light[0] + (gy / max(1, m.shape[0] - 1) - .5) * light[1]
        sm = m.copy()                                   # cheap blur → darker towards the shape's edges
        for _ in range(3): sm = (sm + np.roll(sm, 1, 0) + np.roll(sm, -1, 0) + np.roll(sm, 1, 1) + np.roll(sm, -1, 1)) / 5
        m = m * np.clip((1 - shade) + shade * (.55 + .9 * u) * (.4 + .6 * sm), .08, 1.0)
    d = ImageDraw.Draw(img); rmax = cell * .5 * k
    ys, xs = np.nonzero(m > .04)
    for yy, xx in zip(ys, xs):
        r = rmax * min(1.0, math.sqrt(m[yy, xx] * gain))
        cx, cy = x0 + xx * cell + cell / 2, y0 + yy * cell + cell / 2
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)

def dot_field(d, box, t, cell=26, col=MID, hit=(), hitcol=SIG, seed=1):
    """field of small dots (a crowd / data set); hit = set of indices drawn larger in hitcol"""
    x0, y0, x1, y1 = box; i = 0
    for y in range(int(y0), int(y1), cell):
        for x in range(int(x0), int(x1), cell):
            r = 7 if i in hit else 4
            d.ellipse([x - r, y - r, x + r, y + r], fill=hitcol if i in hit else col); i += 1
    return i

def glitch(img, box, amt=1.0, seed=0, bands=9, pixel=0):
    """horizontal band displacement (+ optional pixelation) inside box"""
    if amt <= 0: return
    x0, y0, x1, y1 = [int(v) for v in box]; rnd = random.Random(seed)
    region = img.crop((x0, y0, x1, y1))
    if pixel > 1:
        region = region.resize((max(1, (x1 - x0) // pixel), max(1, (y1 - y0) // pixel)), Image.NEAREST).resize((x1 - x0, y1 - y0), Image.NEAREST)
    out = region.copy(); y = 0
    while y < y1 - y0:
        hgt = rnd.randint(6, max(8, (y1 - y0) // bands)); dx = int(rnd.uniform(-60, 60) * amt)
        out.paste(region.crop((0, y, x1 - x0, min(y1 - y0, y + hgt))), (dx, y)); y += hgt
    img.paste(out, (x0, y0))

# ---------------------------------------------------------------- lab annotations
def bbox(d, box, label=None, col=INK, k=1.0, coords=True, size=20):
    """thin bounding box with corner ticks + normalised centre coordinates (machine-vision look)"""
    if k <= 0: return
    x0, y0, x1, y1 = box; e = ease(k)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    x0, x1 = lerp(cx, x0, e), lerp(cx, x1, e); y0, y1 = lerp(cy, y0, e), lerp(cy, y1, e)
    d.rectangle([x0, y0, x1, y1], outline=col, width=2)
    L = 18
    for (px, py, sx, sy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        d.line([px, py, px + sx * L, py], fill=col, width=5); d.line([px, py, px, py + sy * L], fill=col, width=5)
    if e > .9:
        tag = (label + "  " if label else "") + (f"{cx / W:.2f}, {cy / H:.2f}" if coords else "")
        if tag.strip(): d.text((x0, y0 - 6), tag, font=F(MONO, size), fill=col, anchor="ld")

def track(d, x0, x1, y, label, pts=None, col=INK, size=18):
    """data-track row: small mono label left + a line/curve (like VOICES / GUNFIRE / MUSIC)"""
    d.text((x0 - 12, y), label, font=F(MONO, size), fill=MID, anchor="rm")
    if pts: d.line(pts, fill=col, width=3)
    else: d.line([x0, y, x1, y], fill=col, width=3)

# ---------------------------------------------------------------- episode with slide transitions
class ThreadEpisode(Episode):
    """Episode whose scenes slide horizontally into each other (the thread looks continuous) and without zoom drift."""
    def __init__(self, *a, slide=.38, **kw):
        kw.setdefault("drift", 0.0); self.label = kw.pop("label", None)     # e.g. "CASE STUDY", "SELF-TEST", "UNSOLVED"
        super().__init__(*a, **kw); self.slide = slide

    def _scene(self, img, d, key, t):
        self.grid(d)
        if key == "end": self.end_card(d, t)
        else:
            self.scenes[key](img, d, t)
            for lay in self.layers: lay(img, d, t, key)

    def compose(self, img, d, t):
        cur = self.current(t); a, b = self.scene_span(cur); i = self.order.index(cur)
        Y0c, Y1c = 280, 1186                             # moving band (chrome + subtitles stay put)
        if i > 0 and t < a + self.slide:
            prev = self.order[i - 1]
            A = Image.new("RGB", (W, H), BG); self._scene(A, ImageDraw.Draw(A), prev, a - 1 / 30)
            B = Image.new("RGB", (W, H), BG); self._scene(B, ImageDraw.Draw(B), cur, t)
            off = int(W * ease_io((t - a) / self.slide))
            img.paste(A.crop((off, Y0c, W, Y1c)), (0, Y0c))
            img.paste(B.crop((0, Y0c, off, Y1c)), (W - off, Y0c)) if off > 0 else None
        else:
            self._scene(img, d, cur, t)
        if cur == self.order[0] and t < .3: zoom_band(img, d, 1 + SLAM * (1 - ease(t / .3)), y0=Y0c, y1=Y1c)
        if cur != "end": self.overlays(img, d, t, cur)
        d.rectangle([0, 0, W, Y0c - 1], fill=BG); d.rectangle([0, Y1c, W, H], fill=BG)
        self.chrome(d, t, cur)
        if self.label and cur != "end": box_label(d, X1, 270, self.label, 22, WHITE, SIG, font=MONO, anchor="ra")
        self.subtitle(d, t)

    def cut_fx(self, amp=.10):
        return [(self.TL.S(k) - .3, whoosh(.45, amp), 0) for k in self.order[1:]]

def ekg(x0, x1, y, t, period=180, amp=60, speed=240, step=4, chaos=0.0, seed=0):
    """scrolling ECG line: flat with periodic P-QRS-T complexes; chaos 0..1 adds irregular spikes (panic)"""
    rnd = random.Random(seed); out = []
    for x in range(int(x0), int(x1) + 1, step):
        p = ((x + t * speed) % period) / period
        v = 0.0
        if .10 < p < .16: v = -.12 * math.sin((p - .10) / .06 * math.pi)            # P
        elif .20 < p < .22: v = .15                                                   # Q
        elif .22 < p < .25: v = -1.0 + (p - .22) / .03 * .0                           # R up
        elif .25 < p < .28: v = .35                                                   # S
        elif .38 < p < .48: v = -.22 * math.sin((p - .38) / .10 * math.pi)           # T
        if chaos > 0:
            v += chaos * (math.sin(x * .21 + t * 23) * .6 + math.sin(x * .053 - t * 41) * .5) * (1 if rnd.random() > .3 else .2)
        out.append((x, y + v * amp))
    return out

def bust(d, cx, cy, s=1.0, col=255, nose=0, f=1):
    """profile bust (f=1 faces right) for halftone masks: head, jaw, nose, neck, shoulders"""
    X = lambda dx: cx + f * dx * s
    d.ellipse([min(X(-105), X(95)), cy - 150 * s, max(X(-105), X(95)), cy + 85 * s], fill=col)
    d.polygon([(X(85), cy), (X(98), cy + 55 * s), (X(62), cy + 112 * s), (X(-10), cy + 122 * s), (X(-50), cy + 60 * s)], fill=col)
    d.polygon([(X(88), cy - 42 * s), (X(122 + nose), cy + 4 * s), (X(88), cy + 14 * s)], fill=col)
    d.rectangle([min(X(-48), X(30)), cy + 80 * s, max(X(-48), X(30)), cy + 200 * s], fill=col)
    d.rounded_rectangle([min(X(-250), X(200)), cy + 175 * s, max(X(-250), X(200)), cy + 440 * s], radius=int(140 * s), fill=col)

def knife(d, x, y, s=1.0, col=INK, ang=0.0):
    """kitchen knife pointing right (rotated by ang radians around (x, y))"""
    pts = [(0, -16), (210, -4), (240, 6), (0, 22)]; hnd = [(-110, -18), (0, -18), (0, 24), (-110, 24)]
    rot = lambda p: (x + (p[0] * math.cos(ang) - p[1] * math.sin(ang)) * s, y + (p[0] * math.sin(ang) + p[1] * math.cos(ang)) * s)
    d.polygon([rot(p) for p in pts], fill=col); d.polygon([rot(p) for p in hnd], fill=col)

# ---------------------------------------------------------------- silhouettes for halftone (look C) – draw into a mask
def front_bust(d, cx, cy, s=1.0, col=255, tilt=0.0):
    """front-facing head + shoulders; (cx, cy) = head centre"""
    d.ellipse([cx - 92 * s, cy - 118 * s, cx + 92 * s, cy + 110 * s], fill=col)
    d.polygon([(cx - 60 * s, cy + 70 * s), (cx + 60 * s, cy + 70 * s), (cx + 26 * s, cy + 128 * s), (cx - 26 * s, cy + 128 * s)], fill=col)
    d.rectangle([cx - 42 * s, cy + 90 * s, cx + 42 * s, cy + 190 * s], fill=col)
    d.rounded_rectangle([cx - 270 * s, cy + 170 * s, cx + 270 * s, cy + 480 * s], radius=int(150 * s), fill=col)

def body(d, cx, feet, h=700, col=255, f=0, arm=0.0, step=0.0):
    """standing figure silhouette (front, f=0) seen as a smooth shape; h = total height in px.
    arm: 0 = arms down, 1 = arms raised; step: leg spread"""
    s = h / 700
    head_c = (cx, feet - 640 * s)
    d.ellipse([cx - 50 * s, head_c[1] - 62 * s, cx + 50 * s, head_c[1] + 58 * s], fill=col)
    d.rectangle([cx - 22 * s, head_c[1] + 40 * s, cx + 22 * s, head_c[1] + 80 * s], fill=col)
    sh_y = feet - 540 * s; hip_y = feet - 330 * s
    d.polygon([(cx - 105 * s, sh_y), (cx + 105 * s, sh_y), (cx + 80 * s, hip_y), (cx - 80 * s, hip_y)], fill=col)
    d.ellipse([cx - 115 * s, sh_y - 22 * s, cx - 60 * s, sh_y + 40 * s], fill=col); d.ellipse([cx + 60 * s, sh_y - 22 * s, cx + 115 * s, sh_y + 40 * s], fill=col)
    d.rounded_rectangle([cx - 82 * s, hip_y - 20 * s, cx + 82 * s, hip_y + 60 * s], radius=int(30 * s), fill=col)
    for side in (-1, 1):
        a = math.radians(8 + 150 * arm) * side
        x0, y0 = cx + side * 95 * s, sh_y + 10 * s
        x1, y1 = x0 + math.sin(a) * 270 * s, y0 + math.cos(a) * 270 * s
        nx, ny = math.cos(a) * 1, -math.sin(a) * 1
        w0, w1 = 30 * s, 20 * s
        d.polygon([(x0 + nx * w0, y0 + ny * w0), (x1 + nx * w1, y1 + ny * w1), (x1 - nx * w1, y1 - ny * w1), (x0 - nx * w0, y0 - ny * w0)], fill=col)
        d.ellipse([x1 - 24 * s, y1 - 24 * s, x1 + 24 * s, y1 + 24 * s], fill=col)
        lx0 = cx + side * 42 * s; lx1 = cx + side * (52 + 40 * step) * s
        d.polygon([(lx0 - 40 * s, hip_y + 40 * s), (lx0 + 40 * s, hip_y + 40 * s), (lx1 + 24 * s, feet - 10 * s), (lx1 - 24 * s, feet - 10 * s)], fill=col)
        d.ellipse([lx1 - 30 * s + side * 10 * s, feet - 26 * s, lx1 + 30 * s + side * 10 * s, feet + 4 * s], fill=col)

def silhouette(img, fn, box, col=INK, cell=11, k=1.0, shade=.65):
    """shortcut: halftone of a mask-drawing function"""
    halftone(img, fn, box, cell=cell, col=col, k=k, shade=shade)
