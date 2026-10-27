"""Shared 'Soft & Cute' toolkit for 'Not just you' episodes.
Bean character, bubbles, pills, subtitles, timeline bound to narration, sound kit, render harness.
Episode files define SCENES (time ranges -> draw fns) and FX (sound cues) and call run().
"""
import json, math, os, sys, wave, subprocess
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont
from scipy.signal import resample_poly, butter, lfilter

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD = os.path.join(KIT, "fonts") + "/"
W, H, FPS, SR = 1080, 1920, 30, 48000
SAFE_R, SAFE_B = 900, 1480

# ---------------------------------------------------------------- palette (Material-You-like tonal set)
BG = (246, 242, 255); CARD = (236, 228, 255); WALL_A = (232, 222, 255); WALL_B = (220, 244, 234); FLOOR = (214, 200, 245)
INK = (44, 32, 72); PRIMARY = (103, 80, 164); BEAN = (176, 150, 240); BEAN2 = (125, 211, 176)
PINK = (239, 128, 160); BLUSH = (255, 176, 196); MINT = (125, 211, 176); MINT_D = (60, 150, 115)
SUN = (255, 214, 120); WHITE = (255, 255, 255); SKY = (150, 200, 255); RAIN = (170, 180, 205); RED = (235, 90, 110)

_f = {}
def F(n, s):
    if (n, s) not in _f: _f[(n, s)] = ImageFont.truetype(FD + n, max(6, int(s)))
    return _f[(n, s)]
BLK, BOLD, MONO = "Roboto-Black.woff", "Roboto-Bold.woff", "roboto-mono-latin-500.woff"

def clamp(k): return max(0., min(1., k))
def ease(k): k = clamp(k); return 1 - (1 - k) ** 3
def ease_io(k): k = clamp(k); return k * k * (3 - 2 * k)
def back(k, s=2.2): k = clamp(k) - 1; return k * k * ((s + 1) * k + s) + 1
def lerp(a, b, k): return a + (b - a) * k
def mix(a, b, k): k = clamp(k); return tuple(int(lerp(x, y, k)) for x, y in zip(a, b))

# ---------------------------------------------------------------- timeline bound to the narration
class Timeline:
    def __init__(self, ep_dir, lead=.5, gaps=None, default_gap=.35):
        self.dir = ep_dir
        self.meta = json.load(open(os.path.join(ep_dir, "vo", "meta.json")))
        self.T, t = {}, lead
        for m in self.meta:
            self.T[m["id"]] = dict(start=t, dur=m["dur"], text=m["text"])
            t += m["dur"] + (gaps or {}).get(m["id"], default_gap)
        self.total = t
    def S(self, k): return self.T[k]["start"]
    def E(self, k): return self.T[k]["start"] + self.T[k]["dur"]
    def cue(self, beat, word):
        b = self.T[beat]; i = b["text"].lower().find(word.lower())
        if i < 0: raise ValueError(f"cue '{word}' missing in beat '{beat}'")
        return b["start"] + b["dur"] * i / len(b["text"])
    def current(self, t):
        cur = None
        for k, b in self.T.items():
            if t >= b["start"] - .05: cur = k
        return cur

# ---------------------------------------------------------------- widgets
def pill(d, x, y, text, bg, fg, size=30, anchor="la", k=1.0):
    if k <= 0: return
    f = F(BLK, size); w = d.textlength(text, font=f) + size * 1.4; h = size * 1.75
    if anchor == "ma": x -= w / 2
    if anchor == "ra": x -= w
    s = back(k); cx, cy = x + w / 2, y + h / 2
    d.rounded_rectangle([cx - w / 2 * s, cy - h / 2 * s, cx + w / 2 * s, cy + h / 2 * s], radius=h / 2 * s, fill=bg)
    if s > .6: d.text((cx, cy), text, font=F(BLK, size * min(1, s)), fill=fg, anchor="mm")

def card(d, box, fill=CARD, r=56): d.rounded_rectangle(box, radius=r, fill=fill)

def sparkle(d, x, y, r, col):
    d.polygon([(x, y - r), (x + r * .28, y - r * .28), (x + r, y), (x + r * .28, y + r * .28), (x, y + r), (x - r * .28, y + r * .28), (x - r, y), (x - r * .28, y - r * .28)], fill=col)

def heart(d, x, y, r, col):
    d.ellipse([x - r, y - r * .9, x, y + r * .1], fill=col); d.ellipse([x, y - r * .9, x + r, y + r * .1], fill=col)
    d.polygon([(x - r * .98, y - r * .3), (x + r * .98, y - r * .3), (x, y + r * .95)], fill=col)

def big_number(d, x, y, text, size, col, k=1.0, anchor="mm"):
    s = back(k)
    if s > .05: d.text((x, y), text, font=F(BLK, size * s), fill=col, anchor=anchor)

def bean(d, x, y, t, s=1.0, walk=0.0, squash=0.0, look=0.0, mood="happy", key=0, color=BEAN, wave=0.0,
         talk=False, sweat=0.0, flip=False):
    """cute bean character; (x, y) = feet on the floor. mood: happy | o | flat | worried | relieved. returns head anchor."""
    bw, bh = 120 * s * (1 + squash), 170 * s * (1 - squash)
    bob = abs(math.sin(walk * math.pi)) * 10 * s
    top = y - 18 * s - bh - bob
    for i, side in enumerate((-1, 1)):
        sw = math.sin(walk * math.pi + i * math.pi) * 14 * s if walk else 0
        lx = x + side * 26 * s + sw
        d.rounded_rectangle([lx - 11 * s, y - 34 * s - bob * .3, lx + 11 * s, y], radius=11 * s, fill=mix(color, INK, .45))
    d.rounded_rectangle([x - bw / 2, top, x + bw / 2, top + bh], radius=bw / 2, fill=color)
    hx = x - bw / 2 + 12 * s if not flip else x + bw / 2 - 30 * s
    d.rounded_rectangle([hx, top + 14 * s, hx + 18 * s, top + 60 * s], radius=9 * s, fill=mix(color, WHITE, .45))
    if wave:
        ax, ay = (x + bw / 2 - 6 * s) if not flip else (x - bw / 2 + 6 * s), top + bh * .55
        ang = (-math.pi / 3 + math.sin(wave * 12) * .5) if not flip else (-2 * math.pi / 3 - math.sin(wave * 12) * .5)
        d.line([ax, ay, ax + math.cos(ang) * 50 * s, ay + math.sin(ang) * 50 * s], fill=mix(color, INK, .25), width=int(16 * s))
    ey = top + bh * .36
    blink = (int((t + key * .7) * FPS) % 110) < 4
    for side in (-1, 1):
        ex = x + side * 24 * s + look * 10 * s
        if blink: d.line([ex - 10 * s, ey, ex + 10 * s, ey], fill=INK, width=max(2, int(5 * s)))
        elif mood == "relieved":
            d.arc([ex - 12 * s, ey - 8 * s, ex + 12 * s, ey + 12 * s], 200, 340, fill=INK, width=max(2, int(5 * s)))
        else:
            d.ellipse([ex - 13 * s, ey - 15 * s, ex + 13 * s, ey + 15 * s], fill=INK)
            d.ellipse([ex - 6 * s + look * 3 * s, ey - 10 * s, ex + 1 * s + look * 3 * s, ey - 3 * s], fill=WHITE)
        if mood == "worried":
            d.line([ex - 14 * s, ey - 26 * s - side * 4 * s, ex + 12 * s, ey - 26 * s + side * 4 * s], fill=INK, width=max(2, int(4 * s)))
        d.ellipse([x + side * 40 * s - 13 * s, ey + 18 * s, x + side * 40 * s + 13 * s, ey + 30 * s], fill=BLUSH)
    my = ey + 30 * s
    if talk and (int(t * 8 + key) % 2 == 0): d.ellipse([x - 10 * s, my - 6 * s, x + 10 * s, my + 12 * s], fill=INK)
    elif mood in ("happy", "relieved"): d.arc([x - 14 * s, my - 10 * s, x + 14 * s, my + 10 * s], 20, 160, fill=INK, width=max(2, int(5 * s)))
    elif mood == "o": d.ellipse([x - 8 * s, my - 6 * s, x + 8 * s, my + 10 * s], fill=INK)
    elif mood == "worried": d.arc([x - 12 * s, my, x + 12 * s, my + 16 * s], 200, 340, fill=INK, width=max(2, int(5 * s)))
    else: d.line([x - 10 * s, my + 2 * s, x + 10 * s, my - 2 * s], fill=INK, width=max(2, int(5 * s)))
    if sweat > 0:
        sx, sy = x + bw / 2 - 4 * s, top + 24 * s + (t * 60 % 30) * s
        r = 9 * s * sweat
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=SKY); d.polygon([(sx - r * .8, sy - r * .3), (sx + r * .8, sy - r * .3), (sx, sy - r * 2.2)], fill=SKY)
    return (x, top)

def thought(d, head, k=1.0, poof=0.0, s=1.0, dx=60, draw=None, t=0.0):
    """thought cloud; draw(d, cx, cy, s) renders the content"""
    hx, hy = head; cx, cy = hx + dx * s, hy - 110 * s
    if poof > 0:
        for i in range(9):
            a = i / 9 * 2 * math.pi; r = 30 + poof * 110; rr = (1 - poof) * 18 * s
            if rr > 1: d.ellipse([cx + math.cos(a) * r * s - rr, cy + math.sin(a) * r * s - rr, cx + math.cos(a) * r * s + rr, cy + math.sin(a) * r * s + rr], fill=WHITE)
        if poof < .6: sparkle(d, cx, cy, 40 * s * (1 - poof), SUN)
        return
    if k <= 0: return
    sc = back(k)
    for (ox, oy, r) in ((-12, 70, 9), (-2, 46, 14)):
        d.ellipse([hx + (ox + 6) * s - r * s * sc, hy + (oy - 70) * s - r * s * sc, hx + (ox + 6) * s + r * s * sc, hy + (oy - 70) * s + r * s * sc], fill=WHITE)
    for (ox, oy, r) in ((-46, 6, 46), (0, -18, 58), (48, 4, 46), (0, 26, 48)):
        R = r * s * sc
        d.ellipse([cx + ox * s * sc - R, cy + oy * s * sc - R, cx + ox * s * sc + R, cy + oy * s * sc + R], fill=WHITE)
    if sc > .5 and draw: draw(d, cx, cy, s * min(1, sc))

def speech(d, head, text, k=1.0, s=1.0, side=1, size=34, col=WHITE, fg=INK):
    """speech bubble with a tail; side=1 → to the right of the head"""
    if k <= 0: return
    hx, hy = head; sc = back(k)
    f = F(BLK, size * s * sc); w = d.textlength(text, font=f) + 44 * s * sc; h = (size + 30) * s * sc
    x0 = hx + side * 40 * s - (0 if side > 0 else w); y0 = hy - h - 30 * s
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=h / 2, fill=col)
    tx = hx + side * 50 * s
    d.polygon([(tx, y0 + h - 2), (tx + side * 30 * s, y0 + h - 2), (hx + side * 20 * s, hy - 6 * s)], fill=col)
    if sc > .6: d.text((x0 + w / 2, y0 + h / 2), text, font=f, fill=fg, anchor="mm")

def icon_door(d, cx, cy, s):
    """Exit door, slightly ajar: frame, bright gap, swung leaf with knob."""
    d.rounded_rectangle([cx - 26 * s, cy - 40 * s, cx + 26 * s, cy + 40 * s], radius=10 * s, fill=PRIMARY)
    d.rectangle([cx - 19 * s, cy - 33 * s, cx + 19 * s, cy + 40 * s], fill=SUN)
    d.polygon([(cx - 19 * s, cy - 33 * s), (cx + 8 * s, cy - 27 * s), (cx + 8 * s, cy + 34 * s), (cx - 19 * s, cy + 40 * s)], fill=PINK)
    d.ellipse([cx + 1 * s, cy + 2 * s, cx + 6 * s, cy + 7 * s], fill=WHITE)
    d.rectangle([cx - 30 * s, cy + 38 * s, cx + 30 * s, cy + 43 * s], fill=PRIMARY)
def icon_sun(d, cx, cy, s):
    for i in range(8):
        a = i / 8 * 2 * math.pi; d.line([cx + math.cos(a) * 30 * s, cy + math.sin(a) * 30 * s, cx + math.cos(a) * 44 * s, cy + math.sin(a) * 44 * s], fill=SUN, width=max(2, int(7 * s)))
    d.ellipse([cx - 24 * s, cy - 24 * s, cx + 24 * s, cy + 24 * s], fill=SUN)
def icon_cloud(d, cx, cy, s, col=RAIN):
    for (ox, oy, r) in ((-22, 6, 20), (0, -8, 26), (24, 6, 20)): d.ellipse([cx + (ox - r) * s, cy + (oy - r) * s, cx + (ox + r) * s, cy + (oy + r) * s], fill=col)
    d.rounded_rectangle([cx - 42 * s, cy + 2 * s, cx + 42 * s, cy + 26 * s], radius=12 * s, fill=col)

def header(d, no, title):
    pill(d, 60, 222, f"NOT JUST YOU · {no:02d}", PRIMARY, WHITE, size=26)
    d.text((SAFE_R, 238), title, font=F(BOLD, 28), fill=PRIMARY, anchor="ra")

def subtitle(d, TL, t, y0=1210, stop_at=None):
    cur = TL.current(t)
    if cur is None or (stop_at and t >= stop_at): return
    b = TL.T[cur]
    if t > b["start"] + b["dur"] + .5: return
    f = F(BLK, 58); lines, curl = [], ""
    for w_ in b["text"].split():
        tst = (curl + " " + w_).strip()
        if d.textlength(tst, font=f) <= SAFE_R - 80: curl = tst
        else: lines.append(curl); curl = w_
    lines.append(curl)
    shown = (t - b["start"]) / b["dur"] * len(b["text"]); c = 0
    for li, line in enumerate(lines[:4]):
        x = 70
        for w_ in line.split(" "):
            on = c <= shown
            d.text((x, y0 + li * 70 - (6 if on and c > shown - 6 else 0)), w_, font=f, fill=INK if on else mix(BG, INK, .18))
            x += d.textlength(w_ + " ", font=f); c += len(w_) + 1

def sources_block(d, lines, y=1190):
    d.text((70, y), "Sources", font=F(BLK, 26), fill=INK)
    for i, l in enumerate(lines): d.text((70, y + 38 + i * 32), l, font=F(MONO, 22), fill=PRIMARY)

def end_card(d, TL, t, beat="end", sources=(), handle="@vascoda.soda"):
    k0 = TL.S(beat)
    card(d, (60, 320, 900, 1140), fill=CARD)
    for i, (word, col) in enumerate((("NOT", PRIMARY), ("JUST", PRIMARY), ("YOU.", PINK))):
        k = back((t - k0 - i * .15) / .45)
        if k > .05: d.text((110, 380 + i * 175), word, font=F(BLK, 190 * k), fill=col)
    bean(d, 720, 1000, t, 1.15, mood="happy", key=7, wave=t if t > k0 + .4 else 0)
    if t > k0 + 1.0:
        sources_block(d, sources)
        pill(d, 70, 1190 + 38 + len(sources) * 32 + 20, handle, PRIMARY, WHITE, size=28, k=(t - k0 - 1.0) / .3)

_g = np.random.default_rng(3)
PAPER = (_g.normal(0, 4, (H // 2, W // 2, 1))).repeat(2, 0).repeat(2, 1).astype(np.int16)

# ---------------------------------------------------------------- sound kit (major key, plucks, pops)
_rng = np.random.default_rng(11)
def lp(x, fc): b, a = butter(2, fc / (SR / 2)); return lfilter(b, a, x)
def bp(x, lo, hi): b, a = butter(2, [lo / (SR / 2), hi / (SR / 2)], "band"); return lfilter(b, a, x)
def tt_(dur): return np.arange(int(dur * SR)) / SR
def pluck(f, amp=.08, dur=.6):
    t = tt_(dur); return amp * (np.sin(2 * np.pi * f * t) + .4 * np.sin(4 * np.pi * f * t) + .15 * np.sin(6 * np.pi * f * t)) * np.exp(-t * 9)
def pop(amp=.25):
    t = tt_(.12); f = 400 + 900 * (1 - np.exp(-t * 50)); return amp * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 30)
def boing(amp=.18):
    t = tt_(.35); f = 260 + 120 * np.sin(t * 40) * np.exp(-t * 6); return amp * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)
def poof(amp=.25):
    t = tt_(.3); return amp * bp(_rng.standard_normal(len(t)), 600, 5000) * np.exp(-t * 14)
def chime(fs, amp=.05):
    out = np.zeros(int(1.6 * SR))
    for i, f in enumerate(fs):
        p_ = pluck(f, amp, 1.4); s = int(i * .07 * SR); out[s:s + len(p_)] += p_[:len(out) - s]
    return out
def softkick(amp=.35):
    t = tt_(.25); f = 45 + 70 * np.exp(-t * 30); return amp * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 14)
def step(amp=.06):
    t = tt_(.05); return amp * lp(_rng.standard_normal(len(t)), 900) * np.exp(-t * 60)
def heartbeat(amp=.5):
    out = np.zeros(int(.6 * SR)); a = softkick(amp); b = softkick(amp * .7)
    out[:len(a)] += a; s = int(.18 * SR); out[s:s + len(b)] += b[:len(out) - s]; return out
def whoosh(dur=.35, amp=.2):
    t = tt_(dur); return amp * bp(_rng.standard_normal(len(t)), 500, 4000) * np.sin(np.pi * t / dur) ** 2
def tick(amp=.05):
    n = int(.004 * SR); return amp * lp(_rng.standard_normal(n), 6000) * np.linspace(1, 0, n)

def build_audio(TL, fx_cues, path, bpm=112, music_gaps=()):
    """fx_cues: list of (time_s, signal, pan). music_gaps: list of (t0, t1) where the music pauses."""
    n = int((TL.total + 1) * SR); vo = np.zeros(n); mus = np.zeros((n, 2)); fx = np.zeros((n, 2))
    def put(buf, x, t0, pan=0.):
        s = int(t0 * SR)
        if s < 0 or s >= n: return
        e = min(n, s + len(x)); x = x[:e - s]
        if buf.ndim == 1: buf[s:e] += x
        else: buf[s:e, 0] += x * (1 - max(0, pan)); buf[s:e, 1] += x * (1 + min(0, pan))
    for m in TL.meta:
        a, sr = sf.read(os.path.join(TL.dir, "vo", m["id"] + ".wav")); put(vo, resample_poly(a, SR, sr), TL.T[m["id"]]["start"])
    beat = 60 / bpm; chords = [[261.6, 329.6, 392], [220, 261.6, 329.6], [174.6, 220, 261.6], [196, 246.9, 293.7]]
    pattern = [0, 2, 1, 2, 0, 2, 1, 2]; tt = 0.0; i = 0
    while tt < TL.total - .5:
        if not any(a <= tt < b for a, b in music_gaps):
            ch = chords[(i // 8) % 4]
            put(mus, pluck(ch[pattern[i % 8]] * (2 if i % 8 in (3, 7) else 1), .05), tt, pan=(.25 if i % 2 else -.25))
            if i % 8 == 0: put(mus, pluck(ch[0] / 2, .09, 1.2), tt)
            if i % 4 == 0: put(mus, softkick(), tt)
        tt += beat / 2; i += 1
    for (t0, sig, pan) in fx_cues: put(fx, sig, t0, pan)
    env = np.convolve(np.abs(vo), np.ones(int(.12 * SR)) / int(.12 * SR), "same")
    duck = (1 - .6 * np.clip(env / (env.max() * .15 + 1e-9), 0, 1))[:, None]
    st = (vo[:, None] + mus * duck + fx)[: int(TL.total * SR)]
    st /= np.abs(st).max() / .9
    fd = int(.5 * SR); st[-fd:] *= np.linspace(1, 0, fd)[:, None]
    with wave.open(path, "wb") as w_:
        w_.setnchannels(2); w_.setsampwidth(2); w_.setframerate(SR); w_.writeframes((st * 32767).astype(np.int16).tobytes())

# ---------------------------------------------------------------- harness
def run(TL, draw_frame, fx_cues, music_gaps=()):
    """CLI: out.mp4  |  sheet.png --t 1,2,3"""
    def frame(fr):
        img = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(img)
        draw_frame(img, d, fr / FPS)
        return np.clip(np.array(img).astype(np.int16) + PAPER, 0, 255).astype(np.uint8)
    out = sys.argv[1]
    if "--t" in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index("--t") + 1].split(",")]
        ims = []
        for x in ts:
            im = Image.fromarray(frame(int(x * FPS))).convert("RGBA"); ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(ov)
            g.rectangle([0, 0, W, 200], fill=(0, 160, 255, 50)); g.rectangle([0, SAFE_B, W, H], fill=(0, 160, 255, 50)); g.rectangle([960, 900, W, SAFE_B], fill=(0, 160, 255, 50))
            ims.append(Image.alpha_composite(im, ov).convert("RGB").resize((270, 480)))
        sh = Image.new("RGB", (270 * len(ims), 480))
        for i, im in enumerate(ims): sh.paste(im, (270 * i, 0))
        sh.save(out); print("saved", out, "total", round(TL.total, 2), {k: round(v["start"], 2) for k, v in TL.T.items()}); return
    wav = out.replace(".mp4", ".wav"); build_audio(TL, fx_cues, wav, music_gaps=music_gaps); print("audio ok", flush=True)
    total = int(round(TL.total * FPS))
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-i", wav, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "24", "-preset", "slow",
                          "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,alimiter=limit=0.75:level=false", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest",
                          "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for fr in range(total):
        p.stdin.write(frame(fr).tobytes())
        if fr % 300 == 0: print("frame", fr, "/", total, flush=True)
    p.stdin.close(); p.wait(); print("done", out, round(total / FPS, 2), "s")
