"""'Time-travel line' building block (25.11.2026, after the deardata1 reference 'Earth's Temperature Over 2,000 Years'):
  · a scrubber on top: track first..last year, knob with a clock icon, year bubble above it, a red marker for THE event ahead
  · the x-axis always shows everything from the first year to now (history gets squeezed, the end looks steeper)
  · the y-axis re-fits to the values seen so far (only grows, so it never jitters)
  · line with an area gradient below, colour shifts (cold -> hot) with the current value, dot + live value at the tip
  · events: a thin vertical line + small label appear when the line passes them and stay
Use: r = Race(years, values, ...); r.draw(img, year_now). Keyframes for year_now come from the episode (synced to the voice)."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from tips import BG, INK, MID, RULE, SIG, F, BLK, MONO, clamp, ease, mix

COLD = (120, 180, 255)


def year_at(t, keys):
    """keys = [(t, year), ...] -> year at time t (linear between keys; hold at the ends)"""
    if t <= keys[0][0]: return keys[0][1]
    for (t0, y0), (t1, y1) in zip(keys, keys[1:]):
        if t <= t1: return y0 + (y1 - y0) * clamp((t - t0) / max(.01, t1 - t0))
    return keys[-1][1]


def nice_step(span, n=5):
    for s in (.1, .2, .25, .5, 1, 2, 2.5, 5, 10, 20, 25, 50, 100, 200, 500):
        if span / s <= n: return s
    return 1000


class Race:
    def __init__(self, years, values, box=(150, 900, 640, 1130), scrub_y=520, fmt="{:.1f}", unit="", hot_from=None, hot_to=None,
                 marker=None, events=(), ticks=None, pad=.12):
        self.Y = np.array(years, float); self.V = np.array(values, float)
        self.box, self.sy, self.fmt, self.unit = box, scrub_y, fmt, unit
        self.hot = (hot_from, hot_to); self.marker = marker; self.events = list(events); self.ticks = ticks; self.pad = pad

    def col(self, v):
        a, b = self.hot
        if a is None: return COLD
        return mix(COLD, SIG, clamp((v - a) / (b - a)))

    def ranges(self, yr):
        m = self.Y <= yr; vs = self.V[m] if m.any() else self.V[:1]
        lo, hi = float(vs.min()), float(vs.max())
        if hi - lo < 1e-6: lo, hi = lo - 1, hi + 1
        p = (hi - lo) * self.pad
        return (self.Y[0], max(self.Y[0] + 1, yr)), (lo - p, hi + p)

    def scrubber(self, d, yr):
        X0, X1 = 120, 960; y = self.sy; a, b = self.Y[0], self.Y[-1]
        def px(v): return X0 + (v - a) / (b - a) * (X1 - X0)
        d.line([(X0, y), (X1, y)], fill=mix(BG, MID, .5), width=4)
        d.line([(X0, y), (px(yr), y)], fill=INK, width=4)
        for v in (self.ticks or []):
            d.text((px(v), y + 30), str(v), font=F(MONO, 22), fill=MID, anchor="mm")
        if self.marker and yr < self.marker:                                   # the red marker: what's coming
            x = px(self.marker); d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=SIG); d.ellipse([x - 17, y - 17, x + 17, y + 17], outline=SIG, width=2)
        x = px(yr)
        d.ellipse([x - 20, y - 20, x + 20, y + 20], fill=BG, outline=INK, width=4)                  # knob with a clock icon
        ang = yr * 2.2
        d.line([(x, y), (x + 10 * math.cos(math.radians(ang)), y + 10 * math.sin(math.radians(ang)))], fill=INK, width=3)
        d.line([(x, y), (x, y - 12)], fill=INK, width=3)
        txt = f"{int(yr)}"; f = F(BLK, 34); w = d.textlength(txt, font=f)
        d.rounded_rectangle([x - w / 2 - 14, y - 82, x + w / 2 + 14, y - 34], radius=10, fill=mix(BG, MID, .3))
        d.text((x, y - 58), txt, font=f, fill=INK, anchor="mm")

    def draw(self, img, yr, final=False):
        PX0, PX1, PY0, PY1 = self.box; (x0, x1), (v0, v1) = self.ranges(yr)
        def P(a, v): return PX0 + (a - x0) / (x1 - x0) * (PX1 - PX0), PY1 - (v - v0) / (v1 - v0) * (PY1 - PY0)
        d = ImageDraw.Draw(img); self.scrubber(d, yr)
        st = nice_step(v1 - v0); v = math.ceil(v0 / st) * st                       # y grid
        while v <= v1:
            y = P(x0, v)[1]; d.line([(PX0, y), (PX1, y)], fill=mix(BG, MID, .18), width=2)
            d.text((PX0 - 16, y), f"{v:g}", font=F(MONO, 24), fill=MID, anchor="rm"); v += st
        m = self.Y <= yr; ys, vs = self.Y[m], self.V[m]
        if len(ys) and ys[-1] < yr:                                                  # interpolate the tip between data years
            i = np.searchsorted(self.Y, yr); ys = np.append(ys, yr); vs = np.append(vs, self.V[i - 1] + (self.V[i] - self.V[i - 1]) * (yr - self.Y[i - 1]) / (self.Y[i] - self.Y[i - 1]))
        if len(ys) < 2: return
        pts = [P(a, b) for a, b in zip(ys, vs)]
        for ey, lab in self.events:                                                  # events stay once passed
            if yr >= ey:
                ex = P(ey, v0)[0]; d.line([(ex, PY0 + 40), (ex, PY1)], fill=mix(BG, MID, .45), width=2)
                d.text((ex, PY0 + 22), lab, font=F(MONO, 20), fill=MID, anchor="mm")
        tip = vs[-1]; c = self.col(tip)
        # area gradient under the line
        L = Image.new("L", img.size, 0); ImageDraw.Draw(L).polygon(pts + [(pts[-1][0], PY1), (pts[0][0], PY1)], fill=255)
        grad = np.linspace(.42, 0, PY1 - PY0 + 1)[:, None, None]
        A = np.asarray(L, np.float32)[PY0:PY1 + 1, :, None] / 255 * grad
        base = np.asarray(img, np.float32).copy()
        base[PY0:PY1 + 1] = base[PY0:PY1 + 1] * (1 - A) + np.array(COLD, np.float32) * A
        img.paste(Image.fromarray(base.astype(np.uint8)))
        d = ImageDraw.Draw(img)
        # line: cold part + hot tail coloured by value
        for (p, q), a in zip(zip(pts, pts[1:]), vs[1:]):
            d.line([p, q], fill=self.col(a), width=5)
        d.line([(PX0, PY1), (PX1, PY1)], fill=MID, width=2)
        tx, ty = pts[-1]
        d.ellipse([tx - 12, ty - 12, tx + 12, ty + 12], fill=c)
        lab = self.fmt.format(tip) + self.unit
        d.text((tx + 22, ty), lab, font=F(BLK, 36), fill=c, anchor="lm")
