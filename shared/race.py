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
    for s in (.1, .2, .25, .5, 1, 2, 2.5, 5, 10, 20, 25, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000):
        if span / s <= n: return s
    return 1000


class Race:
    def __init__(self, years, values, box=(150, 900, 640, 1130), scrub_y=520, fmt="{:.1f}", unit="", hot_from=None, hot_to=None,
                 marker=None, events=(), ticks=None, pad=.12, others=(), name=None, zero=False, log=False):
        """others = [(label, years, values), ...] thin comparison lines (25.11.2026); name = label of the main line; zero = y from 0"""
        self.others = [(l, np.array(y, float), np.array(v, float)) for l, y, v in others]; self.name = name; self.zero = zero; self.log = log
        self.Y = np.array(years, float); self.V = np.array(values, float)
        self.box, self.sy, self.fmt, self.unit = box, scrub_y, fmt, unit
        self.hot = (hot_from, hot_to); self.marker = marker; self.events = list(events); self.ticks = ticks; self.pad = pad

    def col(self, v):
        a, b = self.hot
        if a is None: return COLD
        return mix(COLD, SIG, clamp((v - a) / (b - a)))

    def _f(self, v): return self.fmt(v) if callable(self.fmt) else self.fmt.format(v)

    def f(self, v): return np.log10(np.maximum(v, 1e-6)) if self.log else v

    def ranges(self, yr):
        m = self.Y <= yr; vs = self.V[m] if m.any() else self.V[:1]
        vs = np.append(vs, np.interp(yr, self.Y, self.V))                            # include the interpolated tips
        for _, oy, ov in self.others:
            if (oy <= yr).any(): vs = np.concatenate([vs, ov[oy <= yr], [np.interp(yr, oy, ov)]])
        vs = self.f(vs); lo, hi = float(vs.min()), float(vs.max())
        if self.zero and not self.log: lo = 0
        if hi - lo < 1e-6: lo, hi = lo - 1, hi + 1
        p = (hi - lo) * self.pad
        if self.zero and not self.log: return (self.Y[0], max(self.Y[0] + 1, yr)), (0, hi + p)
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
        def P(a, v): return PX0 + (a - x0) / (x1 - x0) * (PX1 - PX0), PY1 - (float(self.f(v)) - v0) / (v1 - v0) * (PY1 - PY0)
        d = ImageDraw.Draw(img); self.scrubber(d, yr); self._labs = []
        if self.log:                                                                 # log grid: 0.5 1 2 5 10 20 50 ...
            ms = (1,) if v1 - v0 > 2.2 else (1, 2, 5)
            grid = [m * 10 ** e for e in range(-2, 7) for m in ms if v0 <= math.log10(m * 10 ** e) <= v1]
            if len(grid) < 2:                                                       # narrow range: plain steps
                a, b = 10 ** v0, 10 ** v1; st = nice_step(b - a, 4); grid = list(np.arange(math.ceil(a / st) * st, b, st))
        else:
            st = nice_step(v1 - v0); grid = list(np.arange(math.ceil(v0 / st) * st, v1 + 1e-9, st))
        for v in grid:
            y = P(x0, v)[1]; d.line([(PX0, y), (PX1, y)], fill=mix(BG, MID, .18), width=2)
            d.text((PX0 - 16, y), f"{v:g}", font=F(MONO, 24), fill=MID, anchor="rm")
        m = self.Y <= yr; ys, vs = self.Y[m], self.V[m]
        if len(ys) and ys[-1] < yr:                                                  # interpolate the tip between data years
            i = np.searchsorted(self.Y, yr); ys = np.append(ys, yr); vs = np.append(vs, self.V[i - 1] + (self.V[i] - self.V[i - 1]) * (yr - self.Y[i - 1]) / (self.Y[i] - self.Y[i - 1]))
        if len(ys) < 2: return
        pts = [P(a, b) for a, b in zip(ys, vs)]
        lastx, row = -999, 0
        for ey, lab in self.events:                                                  # events stay once passed
            if yr >= ey:
                ex = P(ey, v0)[0]; row = row + 1 if ex - lastx < 110 else 0; lastx = ex
                d.line([(ex, PY0 + 40 + row * 26), (ex, PY1)], fill=mix(BG, MID, .45), width=2)
                d.text((ex, PY0 + 22 + row * 26), lab, font=F(MONO, 20), fill=MID, anchor="mm")
        tip = vs[-1]; c = self.col(tip)
        # area gradient under the line
        L = Image.new("L", img.size, 0); ImageDraw.Draw(L).polygon(pts + [(pts[-1][0], PY1), (pts[0][0], PY1)], fill=255)
        grad = np.linspace(.42, 0, PY1 - PY0 + 1)[:, None, None]
        A = np.asarray(L, np.float32)[PY0:PY1 + 1, :, None] / 255 * grad
        base = np.asarray(img, np.float32).copy()
        base[PY0:PY1 + 1] = base[PY0:PY1 + 1] * (1 - A) + np.array(COLD, np.float32) * A
        img.paste(Image.fromarray(base.astype(np.uint8)))
        d = ImageDraw.Draw(img)
        for lab, oy, ov in self.others:                                              # thin comparison lines
            k = oy <= yr
            if k.sum() < 1: continue
            xs_, vs_ = oy[k], ov[k]
            if xs_[-1] < yr and (oy > yr).any():
                i = np.searchsorted(oy, yr); xs_ = np.append(xs_, yr); vs_ = np.append(vs_, ov[i - 1] + (ov[i] - ov[i - 1]) * (yr - oy[i - 1]) / (oy[i] - oy[i - 1]))
            op = [P(a, b) for a, b in zip(xs_, vs_)]
            if len(op) > 1: d.line(op, fill=mix(BG, INK, .45), width=3, joint="curve")
            ox, oyy = op[-1]; d.ellipse([ox - 6, oyy - 6, ox + 6, oyy + 6], fill=mix(BG, INK, .6))
            self._labs.append([oyy, ox + 14, f"{lab} {self._f(vs_[-1])}", F(MONO, 22), mix(BG, INK, .7)])
        # line: cold part + hot tail coloured by value
        for (p, q), a in zip(zip(pts, pts[1:]), vs[1:]):
            d.line([p, q], fill=self.col(a), width=5)
        d.line([(PX0, PY1), (PX1, PY1)], fill=MID, width=2)
        tx, ty = pts[-1]
        d.ellipse([tx - 12, ty - 12, tx + 12, ty + 12], fill=c)
        lab = (self.name + " " if self.name else "") + self._f(tip) + self.unit
        self._labs.append([ty, tx + 22, lab, F(BLK, 36), c])
        L = sorted(self._labs, key=lambda r: r[0])                                    # labels never overlap: push apart
        for a, b in zip(L, L[1:]):
            if b[0] - a[0] < 36: b[0] = a[0] + 36
        for y, x, txt, f, col in L: d.text((x, y), txt, font=f, fill=col, anchor="lm")
