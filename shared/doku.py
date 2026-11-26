"""Doku look (26.11.2026, after Chris' reference reel 'Teotihuacan' by @jimswormhole): real archive pictures instead of
drawn objects. Full-bleed pictures with a slow camera (Ken Burns), earthy grade + vignette + moving film grain,
a place/year tag top left (mono, gold box), a small credit line vertical at the left edge (TITLE · ARTIST · LICENCE),
word-by-word captions in white with gold accent words, quote/number cards, and ONE continuous gold element over all
pictures (rule 12 for kind 'doku': e.g. a price line) – pictures may cut, the gold element stays.

    from doku import *
    EP = DokuEpisode(TL, 163, "MARY'S CANDLE", order=ORDER, img_dir=..., credits=...)
    EP.shots = [Shot("cold", "wright", (.62, .40, 1.25), (.55, .48, 1.45), tag="ENGLAND · 1800", credit="..."), ...]
    EP.overlay = fn(img, d, t)          # counters, the continuous gold element
    EP.accent = {"cold": ["1800"], ...} # caption words in gold
    EP.run(FX)

Pictures: Wikimedia Commons (public domain / CC0 / CC BY) via tools/wikimedia.py, credits kept in img/credits.json.
Only standard thumbnail widths (500/960/1280/1920 px) – other sizes get HTTP 429 from Wikimedia."""
import os, sys, json, math, re
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import swiss
from swiss import Episode
from cute import F, BLK, BOLD, MONO, W, H, FPS, clamp, ease, ease_io, lerp, mix

GOLD = (222, 178, 92)
GOLD_D = (150, 118, 60)
WHITE = (250, 246, 238)
SHADE = (14, 11, 8)
import cute
cute.PAPER = np.zeros_like(cute.PAPER)                 # doku has its own moving film grain; the static paper grain cost ~45 MiB
TAG_Y, CAP_Y, CAP_W = 236, 1100, 860          # top UI ends ~200, bottom UI starts ~1480 (SAFE_B)


class Shot:
    """one picture: from/to = (focus x 0..1, focus y 0..1, zoom ≥ 1 relative to 'cover'); mode 'cover' (full bleed) or
    'fit' (whole picture on black, e.g. the Earth at night); grade = (brightness, warmth 0..1, sepia 0..1)"""
    def __init__(self, beat, img, a, b, tag="", credit="", start=None, mode="cover", grade=(.82, .35, 0.0), flicker=0.0, ghost=0.0):
        self.beat, self.img, self.a, self.b, self.tag, self.credit = beat, img, a, b, tag, credit
        self.start, self.mode, self.grade, self.flicker = start, mode, grade, flicker
        self.ghost = ghost                                  # > 0: the picture smears sideways (long exposure, "blink and you blur")


_VIG = None
def vignette():
    global _VIG
    if _VIG is None:
        Y, X = np.ogrid[:H, :W]
        r = np.sqrt(((X - W / 2) / (W * .62)) ** 2 + ((Y - H * .46) / (H * .62)) ** 2)
        _VIG = np.clip(1.08 - .55 * r ** 2.2, .25, 1)[..., None].astype(np.float32)
    return _VIG

_GRAIN = None
GRAIN_SIGMA, GRAIN_STEP = 3.0, 3            # film grain: strength and frames per grain pattern (10 fps)
def grain(fr):
    """moving film grain: 4 pre-made, slightly soft half-res noise patterns, a new one every GRAIN_STEP frames.
    Grain is expensive for H.264 (156 MiB at sigma 7 / every frame) – keep it subtle the real size driver was the static paper grain of cute.py (doku: off, ~65 → ~22 MiB)."""
    global _GRAIN
    if _GRAIN is None:
        g = np.random.default_rng(7)
        _GRAIN = []
        for _ in range(4):
            n = Image.fromarray(np.clip(g.normal(128, 40, (H // 2, W // 2)), 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.6))
            n = (np.asarray(n, np.float32) - 128) / 40 * GRAIN_SIGMA
            _GRAIN.append(n.repeat(2, 0).repeat(2, 1)[..., None])
    return _GRAIN[(fr // GRAIN_STEP) % 4]


def text_shadow(img, xy, text, font, fill, anchor="la", blur=10, strength=200):
    """text with a soft dark shadow (readable on any picture)"""
    d = ImageDraw.Draw(img); x0, y0, x1, y1 = d.textbbox(xy, text, font=font, anchor=anchor)
    pad = blur * 3; box = (int(x0 - pad), int(y0 - pad), int(x1 + pad), int(y1 + pad))
    m = Image.new("L", (box[2] - box[0], box[3] - box[1]), 0)
    ImageDraw.Draw(m).text((xy[0] - box[0], xy[1] - box[1] + 4), text, font=font, fill=strength, anchor=anchor)
    m = m.filter(ImageFilter.GaussianBlur(blur))
    img.paste(Image.new("RGB", m.size, SHADE), box[:2], m)
    ImageDraw.Draw(img).text(xy, text, font=font, fill=fill, anchor=anchor)


def tag(img, d, text, k=1.0, x=60, y=TAG_Y):
    """place / year tag, top left: mono caps in a gold box"""
    if k <= 0 or not text: return
    f = F(MONO, 30); w = d.textlength(text, font=f)
    dx = -(1 - ease(k)) * 40
    d.rectangle([x + dx, y, x + dx + w + 30, y + 50], fill=GOLD)
    d.text((x + dx + 15, y + 25), text, font=f, fill=SHADE, anchor="lm")


def credit(img, d, text, k=1.0, x=22, y1=1440):
    """credit line, unobtrusive (Chris 26.11.2026): small mono text, vertical along the left edge (reads bottom → top),
    half transparent, no frame. Format: TITLE · ARTIST · LICENCE"""
    if k <= 0 or not text: return
    f = F(MONO, 17); w = int(d.textlength(text, font=f)) + 8
    while w > 1180 and f.size > 12: f = F(MONO, f.size - 1); w = int(d.textlength(text, font=f)) + 8
    lay = Image.new("RGBA", (w, 28), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.text((4, 14), text, font=f, fill=(225, 212, 185, int(150 * k)), anchor="lm", stroke_width=1, stroke_fill=(10, 8, 6, int(90 * k)))
    lay = lay.rotate(90, expand=True)
    img.paste(lay, (x, y1 - lay.size[1]), lay)


class DokuEpisode(Episode):
    def __init__(self, TL, no, title, order, img_dir, credits=None, **kw):
        super().__init__(TL, no, title, chapters={k: "" for k in order[:-1]}, order=order, dark=False, **kw)
        self.dir = img_dir; self._img = {}; self.shots = []; self.overlay = None; self.accent = {}
        self.under = None                                   # fn(img, t): drawn on the picture, under tag/credit/overlay
        self.payoff = None                                  # (t0, z1): camera pulls back from z1 to 1 from t0 (rule 14)
        self.counter_list = []
        self.credits = json.load(open(credits)) if credits and os.path.exists(credits) else {}

    # ---- pictures ------------------------------------------------------------------------------------
    def pic(self, name):
        if name not in self._img: self._img[name] = Image.open(os.path.join(self.dir, name + ".jpg")).convert("RGB")
        return self._img[name]

    def shot_times(self):
        out = []
        for s in self.shots:
            t0 = s.start if s.start is not None else self.TL.S(s.beat) - .05
            out.append(max(0.0, t0))
        return out

    def shot_at(self, t):
        ts = self.shot_times(); i = 0
        for j, t0 in enumerate(ts):
            if t >= t0: i = j
        t1 = ts[i + 1] if i + 1 < len(ts) else self.TL.total
        return i, ts[i], t1

    def render_shot(self, s, k, t):
        """Ken Burns: focus/zoom eased from s.a to s.b over the shot (k = 0..1)"""
        im = self.pic(s.img); iw, ih = im.size; e = ease_io(k)
        fx, fy, z = (lerp(p, q, e) for p, q in zip(s.a, s.b))
        if s.mode == "fit":
            sc = W / iw * z; bg = Image.new("RGB", (W, H), (0, 0, 0))
        else:
            sc = max(W / iw, H / ih) * z; bg = None
        cw, ch = W / sc, H / sc
        cx = fx * iw if s.mode == "fit" else min(max(fx * iw, cw / 2), iw - cw / 2)
        cy = fy * ih if s.mode == "fit" else min(max(fy * ih, ch / 2), ih - ch / 2)
        x0, y0 = cx - cw / 2, cy - ch / 2
        out = im.transform((W, H), Image.AFFINE, (1 / sc, 0, x0, 0, 1 / sc, y0), resample=Image.BILINEAR, fillcolor=(0, 0, 0))
        b, warm, sep = s.grade
        a = np.asarray(out, np.float32)
        if sep:
            g = a @ np.array([.299, .587, .114], np.float32); sepia = np.stack([g * 1.0, g * .86, g * .66], -1)
            a = a * (1 - sep) + sepia * sep
        if warm: a = a * np.array([1 + .08 * warm, 1 + .01 * warm, 1 - .12 * warm], np.float32)
        fl = 1 + s.flicker * (.05 * math.sin(t * 19) + .035 * math.sin(t * 31 + 1) + .02 * math.sin(t * 47))
        a = a * b * fl
        if s.ghost:                                         # double exposure drifting apart over the shot
            dx = int(s.ghost * 60 * ease_io(k)) + 1
            a = a * .55 + np.roll(a, dx, axis=1) * .25 + np.roll(a, -dx // 2, axis=1) * .2
        return a

    def camera(self, img, t):
        """payoff camera (rule 14): slow pull back on the final picture"""
        if not self.payoff: return
        t0, z1 = self.payoff
        if t < t0: return
        z = lerp(z1, 1.0, ease_io((t - t0) / 2.2))
        if z <= 1.001: return
        cw, ch = W / z, H / z
        img.paste(img.crop((int((W - cw) / 2), int((H - ch) * .45), int((W + cw) / 2), int((H - ch) * .45 + ch))).resize((W, H), Image.BILINEAR))

    # ---- captions: word by word, 1-3 words per page, gold accents ----------------------------------------
    def pages(self, key):
        b = self.TL.T[key]; words = b["text"].split(); out, cur = [], []
        for w_ in words:
            cur.append(w_)
            if len(cur) == 3 or w_[-1] in ".,?!" or (len(cur) == 2 and len(" ".join(cur)) > 13):
                out.append(cur); cur = []
        if cur: out.append(cur)
        return out

    def caption(self, img, t):
        TL = self.TL; key = TL.current(t)
        if not key or key == "end" or TL.T[key].get("mute"): return
        b = TL.T[key]
        if t > b["start"] + b["dur"] + .35: return
        txt = b["text"]; pos = (t - b["start"]) / max(.01, b["dur"]) * len(txt)
        c = 0; page = None
        for pg in self.pages(key):
            s = " ".join(pg); i = txt.find(s, c)
            if i <= pos + 1: page = (pg, i)
            c = i + len(s)
        if not page: return
        pg, i0 = page; f = F(BLK, 74)
        acc = [a.lower() for a in self.accent.get(key, [])]
        d = ImageDraw.Draw(img)
        # Chris 26.11.2026: subtitles BREAK into lines instead of running over the edge. Max width CAP_W (keeps clear of
        # the frame and of Instagram's buttons on the right); a single word that is still too wide gets a smaller size.
        while max(d.textlength(w_, font=f) for w_ in pg) > CAP_W and f.size > 40: f = F(BLK, f.size - 4)
        lines, cur = [], []
        for w_ in pg:
            if cur and d.textlength(" ".join(cur + [w_]), font=f) > CAP_W: lines.append(cur); cur = []
            cur.append(w_)
        lines.append(cur)
        lh = f.size * 1.12; y = CAP_Y - (len(lines) - 1) * lh / 2
        c = i0
        for ln in lines:
            x = W / 2 - d.textlength(" ".join(ln), font=f) / 2
            for w_ in ln:
                clean = re.sub(r"[^\w']", "", w_).lower()
                gold = any(clean and clean in a.split() for a in acc)
                if c <= pos: text_shadow(img, (x, y), w_, f, GOLD if gold else WHITE)
                x += d.textlength(w_ + " ", font=f); c += len(w_) + 1
            y += lh

    # ---- frame -------------------------------------------------------------------------------------------
    def draw(self, img, d, t):
        fr = int(round(t * FPS))
        i, t0, t1 = self.shot_at(t); s = self.shots[i]
        a = self.render_shot(s, (t - t0) / max(.5, t1 - t0), t)
        if i > 0 and t - t0 < .22:                                   # short dissolve between pictures
            p = self.shots[i - 1]; tp = self.shot_times()[i - 1]
            pa = self.render_shot(p, (t - tp) / max(.5, t0 - tp), t); k = ease((t - t0) / .22)
            a = pa * (1 - k) + a * k
        z = self.pulse_zoom(t)
        a = a * vignette() + grain(fr)
        img.paste(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)))
        if z > 1.002:
            cw, ch = W / z, H / z
            img.paste(img.crop((int((W - cw) / 2), int((H - ch) / 2), int((W + cw) / 2), int((H - ch) / 2 + ch))).resize((W, H), Image.BILINEAR))
        if self.under: self.under(img, t)
        self.camera(img, t)
        d = ImageDraw.Draw(img)
        tag(img, d, s.tag, (t - t0) / .3 if i else 1)
        credit(img, d, s.credit or self.credit_of(s.img), clamp((t - t0) / .3) if i else 1)
        if self.overlay: self.overlay(img, d, t)
        self.caption(img, t)

    def credit_of(self, name):
        c = self.credits.get(name)
        if not c: return ""
        title = re.sub(r"^File:|\.(jpg|png|jpeg)$", "", c["title"], flags=re.I)
        return f"{title[:46].upper()} · {c.get('artist', '')[:28].upper()} · {c['license'].upper()}"

    def counters(self): return list(self.counter_list)

    def shot_fx(self, snd):
        """a soft sound on every picture change inside a beat (beat starts already get EP.cut_fx)"""
        starts = {round(self.TL.S(k) - .05, 2) for k in self.order if k in self.TL.T}
        return [(t, snd, 0) for t in self.shot_times()[1:] if round(t, 2) not in starts and t > .1]

    def make_cover(self, path, words=None, kicker=None):
        """cover = the first picture, darkened, with the question (rule 3) – key content inside the 1080x1440 centre"""
        spec = dict(self.cover_spec or {}); words = words or spec.get("words", [self.title]); kicker = kicker or spec.get("kicker", "")
        s = self.shots[0]; a = self.render_shot(Shot(s.beat, s.img, s.b, s.b, grade=(s.grade[0] * .8,) + tuple(s.grade[1:])), 1, 0)
        img = Image.fromarray(np.clip(a * vignette() + grain(0), 0, 255).astype(np.uint8)); d = ImageDraw.Draw(img)
        size = min(150, int(min(900 / max(1, d.textlength(w_, font=F(BLK, 100))) * 100 for w_ in words)))
        y = 1060 - len(words) * size * 1.05
        if kicker: tag(img, d, kicker.upper(), 1, x=(W - d.textlength(kicker.upper(), font=F(MONO, 30)) - 30) / 2, y=int(y - 90))
        for i, w_ in enumerate(words):
            text_shadow(img, (W / 2, y), w_, F(BLK, size), GOLD if i == len(words) - 1 else WHITE, anchor="ma", blur=14, strength=230)
            y += size * 1.05
        text_shadow(img, (W / 2, 1390), "NOT JUST YOU · " + self.handle, F(MONO, 30), (225, 210, 180), anchor="mm", blur=10, strength=240)
        img.save(path); return path


# ---- generic gold elements (26.11.2026): the Meter runs over all pictures (rule 12 for doku), Compare = payoff -------
class Meter:
    """the continuous gold element: one big number that changes over the story.
    segs: list of dict(t=start, to=value, dur=count time, label='TAG TEXT', unit='UNDER THE NUMBER', fmt=fn(v)->str,
          stamp='BOX TEXT after the count', gold=True when the value is the punchline). From the first seg until t_hide."""
    def __init__(self, segs, t_hide, y=330):
        self.segs, self.t_hide, self.y = segs, t_hide, y

    def value(self, t):
        prev = self.segs[0].get("from", 0); cur = None
        for s in self.segs:
            if t >= s["t"]: cur = s; v0 = prev
            prev = s["to"]
        if cur is None: return None, None
        k = ease_io(clamp((t - cur["t"]) / max(.01, cur.get("dur", .6))))
        return cur, v0 + (cur["to"] - v0) * k if cur.get("tween", True) else cur["to"]

    def counters(self):
        out, prev = [], self.segs[0].get("from", 0)
        for s in self.segs:
            if s.get("dur", .6) >= .5 and s["to"] != prev: out.append((s["t"], s["dur"], abs(s["to"])))
            prev = s["to"]
        return out

    def draw(self, img, d, t):
        s0 = self.segs[0]
        if t < s0["t"] - .2 or t >= self.t_hide: return
        a = min(clamp((t - s0["t"] + .2) / .3), clamp((self.t_hide - t) / .25))
        cur, v = self.value(max(t, s0["t"]))
        done = t >= cur["t"] + cur.get("dur", .6)
        tag(img, d, cur["label"], a, y=self.y)
        txt = cur.get("fmt", lambda v: f"{v:,.0f}")(v)
        size = 190 if len(txt) <= 7 else int(190 * 7 / len(txt))
        text_shadow(img, (60, self.y + 70), txt, F(BLK, size), GOLD if (done and cur.get("gold")) else WHITE, blur=14, strength=220)
        if cur.get("unit"): text_shadow(img, (66, self.y + 280), cur["unit"], F(MONO, 40), (230, 215, 185))
        if cur.get("stamp") and done:
            ks = ease((t - cur["t"] - cur.get("dur", .6)) / .18); sz = int(60 * (1 + .5 * (1 - ks)))
            f = F(BLK, sz); w = d.textlength(cur["stamp"], font=f); y0 = self.y + 345
            d.rectangle([66, y0, 66 + w + 40, y0 + sz * 1.25], outline=GOLD, width=6)
            d.text((86, y0 + sz * .62), cur["stamp"], font=f, fill=GOLD, anchor="lm")


def compare(img, d, t, t0, rows, y=340):
    """payoff: two rows (who, value, colour) sliding in – then vs. now"""
    if t < t0: return
    k = ease((t - t0) / .35)
    for i, (who, val, col) in enumerate(rows):
        yy = y + i * 230; dx = (1 - k) * (-60 if i == 0 else 60)
        text_shadow(img, (60 + dx, yy), who, F(MONO, 36), (230, 215, 185))
        f = F(BLK, 150 if len(val) <= 9 else int(150 * 9 / len(val)))
        text_shadow(img, (60 + dx, yy + 44), val, f, col, blur=14, strength=220)


# ---- paper card with a marker (Chris 26.11.2026: "einen Zeitungsartikel unterstreichen") ---------------------------
# Only for public-domain newspapers (before 1930) or a neutral card for a study (journal · date · REAL title).
# Never a screenshot of a current newspaper, never a real masthead on invented text.
SERIF, SERIF_I = "Roboto-Serif-SemiBold.woff", "Roboto-Serif-Italic.woff"
PAPER_C, INK, MARK = (238, 230, 212), (34, 30, 26), (255, 214, 64)

def wrap(d, text, font, width):
    out, cur = [], ""
    for w_ in text.split():
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= width: cur = t
        else: out.append(cur); cur = w_
    return out + [cur]

def paper_card(img, t, t0, t1, head, title, mark, mark_t, foot="", y=430, w=900, tilt=-2.0):
    """a cream paper card slides in at t0 (until t1): small mono header, serif title, and a yellow marker that is drawn
    across the words `mark` (substring of title) between mark_t[0] and mark_t[1]; slow push-in while it is shown."""
    if not (t0 - .05 <= t < t1): return
    k = ease((t - t0) / .35) * clamp((t1 - t) / .25)
    if k <= 0: return
    pad = 46; fh, ft, ff = F(MONO, 26), F(SERIF, 58), F(SERIF_I, 30)
    tmp = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    lines = wrap(tmp, title, ft, w - 2 * pad)
    h = pad + 40 + len(lines) * 74 + (60 if foot else 10) + pad
    card = Image.new("RGBA", (w, h), PAPER_C + (255,)); cd = ImageDraw.Draw(card)
    noise = (np.random.default_rng(3).normal(0, 6, (h, w, 1))).astype(np.int16)
    card = Image.fromarray(np.clip(np.asarray(card, np.int16) + np.concatenate([noise.repeat(3, 2), np.zeros((h, w, 1), np.int16)], 2), 0, 255).astype(np.uint8), "RGBA")
    cd = ImageDraw.Draw(card)
    cd.text((pad, pad), head, font=fh, fill=(110, 98, 80)); cd.line([(pad, pad + 38), (w - pad, pad + 38)], fill=(150, 138, 118), width=2)
    # marker: find the words of `mark` line by line and draw a growing highlight under them
    m = clamp((t - mark_t[0]) / max(.01, mark_t[1] - mark_t[0]))
    spans, yy = [], pad + 56
    full = " ".join(lines); i0 = full.find(mark); i1 = i0 + len(mark); c = 0
    for ln in lines:
        a, b = max(i0, c), min(i1, c + len(ln))
        if i0 >= 0 and a < b:
            x0 = pad + cd.textlength(ln[:a - c], font=ft); x1 = pad + cd.textlength(ln[:b - c], font=ft)
            spans.append((x0, x1, yy))
        c += len(ln) + 1; yy += 74
    total = sum(x1 - x0 for x0, x1, _ in spans); done = total * ease_io(m)
    for x0, x1, yy_ in spans:
        seg = min(x1 - x0, max(0, done)); done -= x1 - x0
        if seg > 0: cd.rectangle([x0 - 6, yy_ + 8, x0 + seg + 6, yy_ + 66], fill=MARK + (200,))
    yy = pad + 56
    for ln in lines: cd.text((pad, yy), ln, font=ft, fill=INK); yy += 74
    if foot: cd.text((pad, yy + 14), foot, font=ff, fill=(110, 98, 80))
    z = .92 + .08 * k + .03 * clamp((t - t0) / max(.5, t1 - t0))
    card = card.resize((int(w * z), int(h * z)), Image.BILINEAR).rotate(tilt, expand=True, resample=Image.BICUBIC)
    sh = Image.new("L", card.size, 0); sh.paste(card.split()[3].point(lambda v: int(v * .55 * k)), (0, 0))
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    x, yc = int((W - card.size[0]) / 2), int(y + (1 - k) * 80)
    img.paste(Image.new("RGB", card.size, (0, 0, 0)), (x + 10, yc + 22), sh)
    alpha = card.split()[3].point(lambda v: int(v * k))
    img.paste(card.convert("RGB"), (x, yc), alpha)
