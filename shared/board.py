"""EVIDENCE BOARD look (26.11.2026, after Chris' reference 'The Dyatlov Pass Incident', @misterjp7): ONE continuous board
instead of many pictures – a dark teal topographic map, photos pinned like prints, typed index cards, black label
tags, red strings between pins, red marker underlines/circles, a stamp. The camera travels across the board (no cuts),
the payoff zooms out to the whole board and shows the title. Format `board` in REGELN.md.

    from board import *
    B = Board(img_dir)                                    # 2400 x 4200 px virtual board
    B.photo("ship", "ship", x=600, y=700, w=900, t=cue("cold","ship"), tilt=-3, label="DEC 4, 1872 · ATLANTIC")
    B.card("log", ["CAPTAIN'S LOG", "NOV 25, 1872", "6 MI NE OF SANTA MARIA"], x=1500, y=1300, w=700, t=..., tilt=2,
           marks=[(2, "6 MI NE OF SANTA MARIA", t0, t1, "underline")])
    B.label("BRIGGS", x, y, t)         B.string("ship", "log", t)       B.stamp("UNSOLVED", x, y, t, rot=-12)
    B.cam = [(0, cx, cy, view_w), (t, cx, cy, view_w), ...]   # view_w = how many board px fill the 1080 px width
    EP = BoardEpisode(TL, 175, "...", order=ORDER, board=B, ...)
"""
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from doku import *
import doku
from cute import F, BLK, MONO, W, H, FPS, clamp, ease, ease_io, lerp

TYPE = "SpecialElite-Regular.woff"
BW, BH = 2400, 4200
TEAL = (24, 52, 56)
RED = (196, 36, 36)
CARD_C = (236, 228, 208)


def topo(w=BW, h=BH, seed=5):
    """procedural topographic-map texture: dark teal, faint contour lines, grain, vignette"""
    g = np.random.default_rng(seed)
    small = g.standard_normal((h // 60 + 3, w // 60 + 3))
    f = np.asarray(Image.fromarray(((small - small.min()) / (np.ptp(small)) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32) / 255
    f2 = np.asarray(Image.fromarray((g.random((h // 18, w // 18)) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32) / 255
    field = f * .8 + f2 * .2
    lines = (np.abs(((field * 22) % 1) - .5) < .035).astype(np.float32)
    major = (np.abs(((field * 22 / 5) % 1) - .5) < .012).astype(np.float32)
    base = np.array(TEAL, np.float32)[None, None, :] * (.82 + .3 * field[..., None])
    base += lines[..., None] * np.array([28, 48, 48], np.float32) * .55 + major[..., None] * np.array([40, 70, 70], np.float32) * .6
    base += g.normal(0, 5, (h, w, 1)).astype(np.float32)
    Y, X = np.ogrid[:h, :w]; r = np.sqrt(((X - w / 2) / (w * .7)) ** 2 + ((Y - h / 2) / (h * .7)) ** 2)
    base *= np.clip(1.15 - .6 * r ** 2, .35, 1.1)[..., None]
    return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))


def _shadowed(rgba, blur=14, off=(10, 16), alpha=150):
    """item with a soft drop shadow (returns a bigger RGBA + the offset of the item inside it)"""
    pad = blur * 3; w, h = rgba.size
    out = Image.new("RGBA", (w + 2 * pad + off[0], h + 2 * pad + off[1]), (0, 0, 0, 0))
    sh = Image.new("L", out.size, 0); sh.paste(rgba.split()[3].point(lambda v: v * alpha // 255), (pad + off[0], pad + off[1]))
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    out.paste(Image.new("RGBA", out.size, (0, 0, 0, 255)), (0, 0), sh)
    out.alpha_composite(rgba, (pad, pad)); return out, pad


class Item:
    def __init__(self, kind, im, x, y, t, tilt=0.0, pin=True):
        self.kind, self.x, self.y, self.t, self.tilt, self.pin = kind, x, y, t, tilt, pin
        self.raw = im; self.mk = []          # marks: (style, (x0, y0, x1, y1) raw px, t0, t1)
        rot = im.rotate(tilt, expand=True, resample=Image.BICUBIC) if tilt else im
        self.im, self.pad = _shadowed(rot)
        self.w, self.h = im.size; self.rw, self.rh = rot.size

    def anchor(self):                      # pin position (board px)
        return self.x, self.y - self.h / 2 + 26


class Board:
    def __init__(self, img_dir, bg=None, size=(BW, BH)):
        self.dir = img_dir; self.items = {}; self.strings = []; self.cam = []; self.order = []
        self.size = size; self.bg = bg or topo(*size)

    def _pic(self, name):
        return Image.open(os.path.join(self.dir, name + ".jpg")).convert("RGB")

    def photo(self, key, img, x, y, w, t, tilt=0.0, label=None, label_t=None, crop=None, sepia=.85, marks=(), credit=None):
        """a photo print / clipping with a white border; x, y = centre on the board.
        marks: ('underline'|'circle', (x0, y0, x1, y1) as fractions of the ORIGINAL picture, t0, t1)"""
        im = self._pic(img); iw0, ih0 = im.size; c = crop or (0, 0, 1, 1)
        if crop: iw, ih = im.size; im = im.crop((int(crop[0] * iw), int(crop[1] * ih), int(crop[2] * iw), int(crop[3] * ih)))
        a = np.asarray(im, np.float32)
        if sepia:
            gr = a @ np.array([.299, .587, .114], np.float32); a = a * (1 - sepia) + np.stack([gr * 1.02, gr * .93, gr * .8], -1) * sepia
        im = Image.fromarray(np.clip(a * .95 + 6, 0, 255).astype(np.uint8))
        h = int(w * im.height / im.width); im = im.resize((w, h), Image.LANCZOS)
        b = max(14, w // 40); card = Image.new("RGBA", (w + 2 * b, h + 2 * b), (238, 234, 224, 255)); card.paste(im, (b, b))
        it = Item("photo", card, x, y, t, tilt); it.credit = credit; self.items[key] = it; self.order.append(key)
        fx_ = lambda u: b + (u - c[0]) / (c[2] - c[0]) * w; fy_ = lambda v: b + (v - c[1]) / (c[3] - c[1]) * h
        it.mk = [(st, (fx_(x0), fy_(y0), fx_(x1), fy_(y1)), t0, t1) for st, (x0, y0, x1, y1), t0, t1 in marks]
        if label: self.label(label, x - w / 2 + 10, y + h / 2 + 10, label_t if label_t is not None else t + .5, key=key + "_lab")
        return it

    def card(self, key, lines, x, y, w, t, tilt=0.0, marks=(), size=44, head=True):
        """a typed index card. marks: (line index, substring, t0, t1, 'underline'|'circle')"""
        f = F(TYPE, size); lh = int(size * 1.45); pad = 46
        h = pad * 2 + lh * len(lines) + (14 if head else 0)
        im = Image.new("RGBA", (w, h), CARD_C + (255,)); d = ImageDraw.Draw(im)
        noise = np.random.default_rng(len(lines) + w).normal(0, 5, (h, w, 1)).astype(np.int16)
        arr = np.asarray(im, np.int16); arr[..., :3] = np.clip(arr[..., :3] + noise, 0, 255); im = Image.fromarray(arr.astype(np.uint8), "RGBA")
        d = ImageDraw.Draw(im); y0 = pad; spans = []
        for i, ln in enumerate(lines):
            d.text((pad, y0), ln, font=f, fill=(30, 28, 26)); spans.append((pad, y0, d.textlength(ln, font=f), lh))
            if head and i == 0: d.line([(pad, y0 + lh - 4), (w - pad, y0 + lh - 4)], fill=(120, 110, 95), width=2); y0 += 14
            y0 += lh
        it = Item("card", im, x, y, t, tilt)
        for li, sub, t0, t1, style in marks:
            px, py, _, lh_ = spans[li]; ln = lines[li]; i = ln.find(sub); assert i >= 0, (ln, sub)
            xa = px + d.textlength(ln[:i], font=f); xb = px + d.textlength(ln[:i + len(sub)], font=f)
            it.mk.append((style, (xa, py, xb, py + lh_), t0, t1))
        self.items[key] = it; self.order.append(key); return it

    def label(self, text, x, y, t, key=None, size=30):
        f = F(TYPE, size); tmp = ImageDraw.Draw(Image.new("RGB", (4, 4))); w = int(tmp.textlength(text, font=f)) + 30
        im = Image.new("RGBA", (w, size + 22), (16, 16, 16, 255)); ImageDraw.Draw(im).text((15, 11), text, font=f, fill=(235, 232, 225))
        it = Item("label", im, x + w / 2, y + (size + 22) / 2, t, 0, pin=False); key = key or f"lab{len(self.items)}"
        self.items[key] = it; self.order.append(key); return it

    def stamp(self, text, x, y, t, rot=-12, size=110, key=None):
        f = F(BLK, size); tmp = ImageDraw.Draw(Image.new("RGB", (4, 4))); w = int(tmp.textlength(text, font=f)) + 60
        im = Image.new("RGBA", (w, size + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rectangle([6, 6, w - 6, size + 54], outline=RED + (230,), width=10); d.text((30, 18), text, font=f, fill=RED + (230,))
        a = np.asarray(im).copy(); holes = np.random.default_rng(9).random(a.shape[:2]) < .12; a[holes, 3] = (a[holes, 3] * .3).astype(np.uint8)
        im = Image.fromarray(a, "RGBA")
        it = Item("stamp", im, x, y, t, rot, pin=False); key = key or f"stamp{len(self.items)}"
        self.items[key] = it; self.order.append(key); return it

    def string(self, a, b, t, dur=.5):
        self.strings.append((a, b, t, dur))

    # ---- camera -----------------------------------------------------------------------------------------------
    def view(self, t):
        ks = self.cam
        if t <= ks[0][0]: return ks[0][1:]
        for (t0, *p0), (t1, *p1) in zip(ks, ks[1:]):
            if t0 <= t < t1:
                e = ease_io((t - t0) / max(.01, t1 - t0)); return tuple(lerp(a, b, e) for a, b in zip(p0, p1))
        return ks[-1][1:]

    def render(self, t):
        cx, cy, vw = self.view(t); s = W / vw; vh = H / s
        bw, bh = self.size                                    # keep the view on the board (no empty edges)
        cx = min(max(cx, vw / 2), bw - vw / 2) if vw < bw else bw / 2
        cy = min(max(cy, vh / 2), bh - vh / 2) if vh < bh else bh / 2
        x0, y0 = cx - vw / 2, cy - vh / 2
        frame = self.bg.transform((W, H), Image.AFFINE, (1 / s, 0, x0, 0, 1 / s, y0), resample=Image.BILINEAR, fillcolor=(10, 22, 24)).convert("RGBA")
        def to_v(bx, by): return (bx - x0) * s, (by - y0) * s
        # strings under the items' pins but over the board
        dr = ImageDraw.Draw(frame)
        for a, b, ts, dur in self.strings:
            if t < ts or a not in self.items or b not in self.items: continue
            if t < self.items[a].t or t < self.items[b].t: continue
            k = ease_io((t - ts) / dur); (ax, ay), (bx, by) = to_v(*self.items[a].anchor()), to_v(*self.items[b].anchor())
            ex, ey = lerp(ax, bx, k), lerp(ay, by, k)
            dr.line([(ax, ay), (ex, ey)], fill=RED + (235,), width=max(2, int(5 * s)))
        for key in self.order:
            it = self.items[key]
            if t < it.t - .02: continue
            k = ease((t - it.t) / .28); z = 1 + .12 * (1 - k)
            im = it.im
            if it.mk and t >= it.mk[0][2]: im = self._marked(it, t)
            sw, sh = int(im.width * s * z), int(im.height * s * z)
            if sw < 2 or sh < 2: continue
            vx, vy = to_v(it.x, it.y)
            if vx + sw < -50 or vx - sw > W + 50 or vy + sh < -50 or vy - sh > H + 50: continue
            sm = im.resize((sw, sh), Image.BILINEAR)
            if k < 1: sm.putalpha(sm.split()[3].point(lambda v: int(v * k)))
            frame.alpha_composite(sm, (int(vx - sw / 2), int(vy - sh / 2 + (1 - k) * -30 * s))) if True else None
        # pins on top
        for key in self.order:
            it = self.items[key]
            if not it.pin or t < it.t + .15: continue
            px, py = to_v(*it.anchor()); r = max(4, 11 * s)
            dr = ImageDraw.Draw(frame)
            dr.ellipse([px - r + 2, py - r + 4, px + r + 2, py + r + 4], fill=(0, 0, 0, 120))
            dr.ellipse([px - r, py - r, px + r, py + r], fill=RED + (255,)); dr.ellipse([px - r * .45, py - r * .6, px, py - r * .15], fill=(255, 150, 150, 255))
        return frame.convert("RGB")

    def _marked(self, it, t):
        """item with red marker strokes drawn in progressively"""
        base = it.raw.copy(); d = ImageDraw.Draw(base)
        for style, (xa, ya, xb, yb), t0, t1 in it.mk:
            if t < t0: continue
            k = ease_io(clamp((t - t0) / max(.01, t1 - t0))); lh = yb - ya
            if style == "underline":
                yy = ya + lh * .82; d.line([(xa, yy), (xa + (xb - xa) * k, yy)], fill=RED + (255,), width=6)
            else:
                cx, cy, rx, ry = (xa + xb) / 2, ya + lh * .42, (xb - xa) / 2 + 12, lh * .6
                pts = [(cx + rx * math.cos(q), cy + ry * math.sin(q)) for q in np.linspace(-math.pi * .9, -math.pi * .9 + 2.15 * math.pi * k, 60)]
                if len(pts) > 1: d.line(pts, fill=RED + (255,), width=6, joint="curve")
        rot = base.rotate(it.tilt, expand=True, resample=Image.BICUBIC) if it.tilt else base
        return _shadowed(rot)[0]

    def fx(self):
        """foley for everything that appears: paper swish, pin, typewriter, string, stamp, marker"""
        import doku_sound as ds
        out = []
        for i, key in enumerate(self.order):
            it = self.items[key]; pan = max(-.6, min(.6, (it.x - self.size[0] / 2) / self.size[0]))
            if it.kind in ("photo", "card"): out.append((it.t - .05, ds.paper(.07, seed=i), pan))
            if it.kind == "card": out.append((it.t + .25, ds.typewriter(5, .05, seed=i), pan))
            if it.kind == "label": out.append((it.t, ds.typewriter(3, .04, seed=i), pan))
            if it.pin: out.append((it.t + .15, ds.pin(.09, seed=i), pan))
            if it.kind == "stamp": out.append((it.t, ds.stamp(.25), 0))
            for _, _, t0, t1 in it.mk: out.append((t0, ds.paper(.05, dur=max(.2, t1 - t0), seed=i + 50), pan))
        for a, b, ts, dur in self.strings: out.append((ts, ds.string_pull(.05, dur), 0))
        return out


def title_card(img, t, t0, t1, title, sub="", y=300):
    """opening headline in a serif, white on a dark band (Dyatlov opener)"""
    if not (t0 <= t < t1): return
    k = ease(clamp((t - t0) / .3)) * clamp((t1 - t) / .3)
    d = ImageDraw.Draw(img); ft, fs = F(doku.SERIF, 64), F(doku.SERIF, 40)
    lines = wrap(d, title, ft, 920); hh = len(lines) * 78 + (sub and 70 or 0) + 50
    ov = Image.new("L", (W, hh), int(170 * k)); img.paste(Image.new("RGB", (W, hh), (8, 10, 12)), (0, y - 25), ov)
    yy = y
    for ln in lines:
        d.text((W / 2, yy), ln, font=ft, fill=mix((8, 10, 12), (245, 240, 230), k), anchor="ma"); yy += 78
    if sub: d.text((W / 2, yy + 10), sub, font=fs, fill=mix((8, 10, 12), (200, 190, 170), k), anchor="ma")


class BoardEpisode(DokuEpisode):
    """a DokuEpisode whose picture is the evidence board (no shots). Captions, overlay, payoff camera as in doku."""
    def __init__(self, TL, no, title, order, board, **kw):
        super().__init__(TL, no, title, order, img_dir=board.dir, **kw)
        self.board = board; self.title_spec = None; self.end_title = None
        import cute; cute.LOUD = -14

    def reveals(self):
        return [self.TL.S(k) for k in self.order if k in self.TL.T and self.TL.T[k].get("key")]

    def draw(self, img, d, t):
        fr = int(round(t * FPS))
        frame = self.board.render(t)
        a = np.asarray(frame, np.float32) * doku.vignette() + doku.grain(fr)
        img.paste(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)))
        if self.under: self.under(img, t)
        d = ImageDraw.Draw(img)
        if self.title_spec: title_card(img, t, *self.title_spec)
        cx, cy, vw = self.board.view(t); best = None                     # credit of the photo closest to the view centre
        for it in self.board.items.values():
            if getattr(it, "credit", None) and t >= it.t:
                dist = math.hypot(it.x - cx, it.y - cy)
                if dist < vw * .9 and (best is None or dist < best[0]): best = (dist, it.credit)
        if best: credit(img, d, best[1])
        if self.overlay: self.overlay(img, d, t)
        self.caption(img, t)

    def make_cover(self, path, words=None, kicker=None):
        spec = dict(self.cover_spec or {}); words = words or spec.get("words", [self.title]); kicker = kicker or spec.get("kicker", "")
        t_all = self.TL.total - .5
        hide = {k: self.board.items[k].t for k in spec.get("hide", ()) if k in self.board.items}
        for k in hide: self.board.items[k].t = 1e9
        img = self.board.render(t_all)
        for k, v in hide.items(): self.board.items[k].t = v
        a = np.asarray(img, np.float32) * doku.vignette() * .7; img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)); d = ImageDraw.Draw(img)
        size = min(140, int(min(900 / max(1, d.textlength(w_, font=F(BLK, 100))) * 100 for w_ in words)))
        y = 1000 - len(words) * size * 1.05
        if kicker: tag(img, d, kicker.upper(), 1, x=(W - d.textlength(kicker.upper(), font=F(MONO, 30)) - 30) / 2, y=int(y - 90))
        for i, w_ in enumerate(words):
            text_shadow(img, (W / 2, y), w_, F(BLK, size), RED if i == len(words) - 1 else WHITE, anchor="ma", blur=14, strength=230); y += size * 1.05
        text_shadow(img, (W / 2, 1390), "NOT JUST YOU · " + self.handle, F(MONO, 30), (225, 210, 180), anchor="mm", blur=10, strength=240)
        img.save(path); return path


# ---- cut-aways (Chris 26.11.2026: "nicht nur Karten" – mix in film, pictures, drawings, newspapers) ----------------
class VideoInsert:
    """an archive film clip as a card on its own blurred, darkened copy (low-res footage stays crisp enough).
    src: video file, ss: start second in the source, sepia/bright: grade, z: (z0, z1) slow zoom of the card"""
    def __init__(self, src, ss, dur, cache, sepia=.8, bright=1.0, z=(1.0, 1.08), fx=.5, crop=None):
        self.ss, self.dur, self.sep, self.b, self.z = ss, dur, sepia, bright, z
        os.makedirs(cache, exist_ok=True)
        if not os.path.exists(os.path.join(cache, "f0001.jpg")):
            vf = f"fps={FPS}" + (f",crop={crop}" if crop else "") + ",scale=960:-2"
            import subprocess
            subprocess.run(["ffmpeg", "-v", "error", "-ss", str(ss), "-t", str(dur + .2), "-i", src, "-vf", vf, "-q:v", "3",
                            os.path.join(cache, "f%04d.jpg")], check=True)
        self.files = sorted(os.path.join(cache, f) for f in os.listdir(cache) if f.endswith(".jpg"))

    def render(self, tl, k):
        im = Image.open(self.files[min(len(self.files) - 1, int(tl * FPS))]).convert("RGB")
        iw, ih = im.size
        sc = max(W / 4 / iw, H / 4 / ih) * 1.2; bg = im.resize((int(iw * sc), int(ih * sc)), Image.BILINEAR)
        bg = bg.crop(((bg.width - W // 4) // 2, (bg.height - H // 4) // 2, (bg.width - W // 4) // 2 + W // 4, (bg.height - H // 4) // 2 + H // 4))
        a = np.asarray(bg.filter(ImageFilter.GaussianBlur(6)).resize((W, H), Image.BILINEAR), np.float32) * .42
        z = lerp(self.z[0], self.z[1], ease_io(k)); s = min(doku.CARD_W / iw, doku.CARD_H / ih) * z * 1.06
        cw, ch = int(iw * s), int(ih * s); card = np.asarray(im.resize((cw, ch), Image.BICUBIC), np.float32)
        x0, y0 = (W - cw) // 2, int(doku.CARD_Y - 60 - ch / 2)
        sh = Image.new("L", (W, H), 0); ImageDraw.Draw(sh).rectangle([x0 + 8, y0 + 18, x0 + cw + 8, y0 + ch + 18], fill=170)
        a *= 1 - np.asarray(sh.filter(ImageFilter.GaussianBlur(22)), np.float32)[..., None] / 255
        ys, ye, xs, xe = max(0, y0), min(H, y0 + ch), max(0, x0), min(W, x0 + cw)
        a[ys:ye, xs:xe] = card[ys - y0:ye - y0, xs - x0:xe - x0]
        if self.sep:
            g = a @ np.array([.299, .587, .114], np.float32); a = a * (1 - self.sep) + np.stack([g, g * .88, g * .7], -1) * self.sep
        fl = 1 + .05 * math.sin(tl * 23) + .03 * math.sin(tl * 37 + 2)          # projector flicker
        return a * self.b * fl


class ShotInsert:
    """a full-screen picture / drawing with Ken Burns (doku.Shot) – a, b = (focus x, focus y, zoom)"""
    def __init__(self, ep_ref, img, a, b, mode="cover", grade=(1.0, .2, .4), flicker=0.0):
        self.ep, self.shot = ep_ref, Shot("x", img, a, b, mode=mode, grade=grade, flicker=flicker)
    def render(self, tl, k): return self.ep.render_shot(self.shot, k, tl)


class BoardInsert:
    """a second, simpler board (e.g. ONE newspaper page filling the screen on a dark desk) with its own camera"""
    def __init__(self, board): self.board = board
    def render(self, tl, k): return np.asarray(self.board.render(tl), np.float32)


def desk(w=1600, h=2800, seed=3):
    """dark wooden desk texture for full-screen papers"""
    g = np.random.default_rng(seed)
    grain = np.asarray(Image.fromarray((g.random((h // 4, w // 40)) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32) / 255
    base = np.array([46, 32, 22], np.float32)[None, None, :] * (.75 + .5 * grain[..., None]) + g.normal(0, 4, (h, w, 1))
    Y, X = np.ogrid[:h, :w]; r = np.sqrt(((X - w / 2) / (w * .6)) ** 2 + ((Y - h / 2) / (h * .6)) ** 2)
    base *= np.clip(1.1 - .7 * r ** 2, .3, 1)[..., None]
    return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))


def _draw_with_inserts(self, img, d, t):
    """BoardEpisode.draw with cut-aways: self.inserts = [(t0, t1, insert, tag, credit)]; 0.18 s dissolves"""
    fr = int(round(t * FPS)); X = .18
    a = None; ins = None
    for t0, t1, obj, tg, cr in self.inserts:
        if t0 - X <= t < t1 + X: ins = (t0, t1, obj, tg, cr); break
    base = np.asarray(self.board.render(t), np.float32) if (ins is None or t < ins[0] or t >= ins[1]) else None
    if ins:
        t0, t1, obj, tg, cr = ins; tl = min(max(t - t0, 0), t1 - t0 - .001)
        f = obj.render(tl, (tl) / max(.01, t1 - t0))
        w_in = clamp((t - t0 + X) / X) * clamp((t1 + X - t) / X) if base is not None else 1.0
        a = f if base is None else base * (1 - w_in) + f * w_in
    else:
        a = base
    a = a * doku.vignette() + doku.grain(fr)
    img.paste(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)))
    if self.under: self.under(img, t)
    d = ImageDraw.Draw(img)
    if self.title_spec: title_card(img, t, *self.title_spec)
    if ins and ins[0] <= t < ins[1]:
        if ins[3]: tag(img, d, ins[3], clamp((t - ins[0]) / .25))
        if ins[4]: credit(img, d, ins[4])
    else:
        cx, cy, vw = self.board.view(t); best = None
        for it in self.board.items.values():
            if getattr(it, "credit", None) and t >= it.t:
                dist = math.hypot(it.x - cx, it.y - cy)
                if dist < vw * .9 and (best is None or dist < best[0]): best = (dist, it.credit)
        if best: credit(img, d, best[1])
    if self.overlay: self.overlay(img, d, t)
    self.caption(img, t)

BoardEpisode.inserts = ()
BoardEpisode.draw = _draw_with_inserts

def insert_fx(inserts):
    """a soft whoosh into every cut-away and back out (so the cut is heard, rule 13)"""
    from swiss import whoosh
    return [(t0 - .2, whoosh(.35, .012), 0) for t0, *_ in inserts] + [(t1 - .2, whoosh(.3, .009), 0) for _, t1, *_ in inserts]


# ---- keep everything inside the frame (Chris 27.11.2026: "alle Elemente komplett im sichtbaren Bereich") -----------
SAFE = (60, 300, 60, 1060)          # left, top, right margin, bottom edge in screen px: above the subtitles (CAP_Y 1100)

def _box(it):
    hw, hh = it.rw / 2, it.rh / 2
    return it.x - hw, it.y - hh, it.x + hw, it.y + hh

def fit(board, keys, t, pad=30, max_vw=None):
    """camera key (t, cx, cy, vw) that shows the items `keys` COMPLETELY in the safe area (between the tag and the
    subtitles); use it instead of hand-made camera keys"""
    xs0, ys0, xs1, ys1 = zip(*[_box(board.items[k]) for k in keys])
    x0, y0, x1, y1 = min(xs0) - pad, min(ys0) - pad, max(xs1) + pad, max(ys1) + pad
    aw, ah = W - SAFE[0] - SAFE[2], SAFE[3] - SAFE[1]
    s = min(aw / (x1 - x0), ah / (y1 - y0)); vw = W / s
    if max_vw: vw = max(vw, W / max_vw)
    s = W / vw
    cx = (x0 + x1) / 2; cy = (y0 + y1) / 2 + (H / 2 - (SAFE[1] + SAFE[3]) / 2) / s
    return (t, cx, cy, vw)

def check_frame(board, t, keys):
    """list of items (keys) that are not completely visible at time t (for tests)"""
    cx, cy, vw = board.view(t); s = W / vw; vh = H / s; bad = []
    for k in keys:
        x0, y0, x1, y1 = _box(board.items[k])
        if (x0 - cx) * s + W / 2 < 0 or (x1 - cx) * s + W / 2 > W or (y0 - cy) * s + H / 2 < 0 or (y1 - cy) * s + H / 2 > H: bad.append(k)
    return bad
