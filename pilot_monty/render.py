"""Monty Hall – editorial monochrome explainer. 1080x1920 @30fps. Deterministic: every frame = f(time, proof.json, script timings).
Usage: python3 render.py out.mp4 | python3 render.py sheet.png --t 1.0,5.0,...
"""
import json, math, os, sys, wave, subprocess
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont
from scipy.signal import resample_poly, butter, lfilter

HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(HERE, "..", "fonts") + "/"
W, H, FPS, SR = 1080, 1920, 30, 48000
BLACK = (8, 8, 8); PAPER = (236, 235, 231); GREY = (150, 150, 146); DIM = (60, 60, 58); RED = (228, 38, 28); PANEL = (24, 24, 24)
_f = {}
def F(n, s):
    if (n, s) not in _f: _f[(n, s)] = ImageFont.truetype(FD + n, s)
    return _f[(n, s)]
COND, MONO, MONOB = "Roboto-Condensed-Bold.woff", "roboto-mono-latin-500.woff", "roboto-mono-latin-700.woff"
def ease(k): k = max(0., min(1., k)); return 1 - (1 - k) ** 3
def ease_io(k): k = max(0., min(1., k)); return k * k * (3 - 2 * k)
def lerp(a, b, k): return a + (b - a) * k
def mix(a, b, k): return tuple(int(lerp(x, y, max(0, min(1, k)))) for x, y in zip(a, b))

PROOF = json.load(open(os.path.join(HERE, "proof.json")))
SIM = PROOF["simulation"]; ORDER = np.array(PROOF["order"])
META = json.load(open(os.path.join(HERE, "vo", "meta.json")))

# ---------------------------------------------------------------- timeline (bound to the synthesized narration)
LEAD = 0.5
GAP = {"fifty": 0.7, "nope": 0.9, "sim": 2.6, "result": 0.5, "end": 2.0}
T, t = {}, LEAD
for m in META:
    T[m["id"]] = dict(start=t, dur=m["dur"], text=m["text"])
    t += m["dur"] + GAP.get(m["id"], 0.35)
TOTAL_S = t
TOTAL = int(round(TOTAL_S * FPS))

def word_time(beat, word):
    """time the given word starts within its beat (char-proportional). Missing word → fail loudly."""
    b = T[beat]; txt = b["text"].lower()
    i = txt.find(word.lower())
    if i < 0: raise ValueError(f"cue word '{word}' not in beat '{beat}'")
    return b["start"] + b["dur"] * i / len(txt)
CUE = dict(
    pick=word_time("pick", "door one"),
    open=word_time("open", "opens"),
    goat=word_time("open", "a goat"),
    offer=word_time("offer", "switch"),
    fifty=word_time("fifty", "fifty"),
    nope=T["nope"]["start"],
    third=word_time("third", "one in three"),
    move=word_time("move", "packed"),
    sim=T["sim"]["start"],
    result=T["result"]["start"],
    end=T["end"]["start"],
)

def beat_at(t):
    cur = None
    for k, b in T.items():
        if t >= b["start"] - 0.05: cur = k
    return cur

# ---------------------------------------------------------------- drawing helpers
def captions(d):
    d.text((60, 228), "NO. 01 — PROBABILITY", font=F(MONO, 24), fill=GREY)
    d.text((900, 228), "THE MONTY HALL PROBLEM", font=F(MONO, 24), fill=GREY, anchor="ra")
    d.line([60, 274, 900, 274], fill=(110, 110, 106), width=1)

def wrap(text, font, maxw, d):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        test = (cur + " " + w_).strip()
        if d.textlength(test, font=font) <= maxw: cur = test
        else: lines.append(cur); cur = w_
    lines.append(cur); return lines

def subtitle(d, t, y0=1330):
    k = beat_at(t)
    if k is None: return
    b = T[k]
    if t > b["start"] + b["dur"] + 0.6: return
    f = F(COND, 62)
    lines = wrap(b["text"], f, 830, d)
    total = len(b["text"]); shown = (t - b["start"]) / b["dur"] * total
    c = 0
    for li, line in enumerate(lines):
        x = 70
        for w_ in line.split(" "):
            col = PAPER if c <= shown else (44, 44, 42)
            d.text((x, y0 + li * 74), w_, font=f, fill=col)
            x += d.textlength(w_ + " ", font=f); c += len(w_) + 1

DX = [190, 480, 770]; DW, DH, DY = 250, 520, 430
def door(img, d, i, open_k=0.0, behind="GOAT", outline=PAPER, width=3, alpha=1.0):
    x0 = DX[i] - DW / 2; x1 = x0 + DW; y0 = DY; y1 = DY + DH
    def c(col): return mix(BLACK, col, alpha)
    d.rectangle([x0, y0, x1, y1], fill=c((14, 14, 14)))
    if open_k > 0:
        col = RED if behind == "CAR" else PAPER
        f = F(COND, 92)
        d.text((DX[i] + DW * .06, y0 + DH * .55), behind, font=f, fill=c(col), anchor="mm")
    pw = DW * (1 - 0.88 * ease(open_k))
    d.rectangle([x0, y0, x0 + pw, y1], fill=c(PANEL if open_k < 1 else (30, 30, 30)))
    if pw > 60:
        d.text((x0 + pw / 2, y0 + 120), str(i + 1), font=F(COND, 190 if open_k == 0 else int(190 * pw / DW) + 1), fill=c(PAPER), anchor="mm")
        d.ellipse([x0 + pw - 34, y0 + DH / 2 - 8, x0 + pw - 18, y0 + DH / 2 + 8], fill=c(GREY))
    d.rectangle([x0, y0, x1, y1], outline=c(outline), width=width)

def mono_tag(d, x, y, text, bg, fg, size=24, anchor="la"):
    f = F(MONOB, size); w_ = d.textlength(text, font=f)
    if anchor == "ma": x -= (w_ + 18) / 2
    d.rectangle([x, y, x + w_ + 18, y + size + 14], fill=bg); d.text((x + 9, y + 6), text, font=f, fill=fg)

def bracket(d, xa, xb, y, label, col, k=1.0, size=64):
    if k <= 0: return
    xb_ = lerp(xa, xb, ease(k))
    d.line([xa, y, xa, y + 24], fill=col, width=4); d.line([xa, y + 24, xb_, y + 24], fill=col, width=4)
    if k >= 1: d.line([xb, y, xb, y + 24], fill=col, width=4)
    if k > .5: d.text(((xa + xb_) / 2, y + 40), label, font=F(COND, size), fill=col, anchor="ma")

# ---------------------------------------------------------------- scenes
def doors_scene(img, d, t):
    # appear
    for i in range(3):
        a = ease((t - LEAD - .1 - i * .25) / .5)
        if a <= 0: continue
        picked = t >= CUE["pick"]
        dim = 1.0
        if CUE["fifty"] <= t < CUE["third"] - .3: dim = .35
        open3 = ease((t - CUE["open"]) / .6) if i == 2 else 0
        outline, width = PAPER, 3
        if i == 0 and picked: outline, width = RED, 7
        if i == 1 and CUE["offer"] <= t < CUE["fifty"]:
            outline, width = mix(PAPER, RED, .5 + .5 * math.sin((t - CUE["offer"]) * 9)), 5
        if i == 1 and t >= CUE["move"] + .9: outline, width = RED, 9
        door(img, d, i, open3, "GOAT", outline, width, alpha=a * dim)
    if t >= CUE["pick"] and t < CUE["fifty"]:
        mono_tag(d, DX[0], DY + DH + 24, "YOUR PICK", RED, PAPER, anchor="ma")
    if CUE["offer"] <= t < CUE["fifty"]:
        k = ease((t - CUE["offer"]) / .5)
        y = DY - 60
        x_end = lerp(DX[0], DX[1], k)
        for x in np.arange(DX[0], x_end, 22): d.line([x, y, min(x + 12, x_end), y], fill=PAPER, width=4)
        if k > .9:
            d.polygon([(DX[1], y), (DX[1] - 18, y - 11), (DX[1] - 18, y + 11)], fill=PAPER)
            mono_tag(d, (DX[0] + DX[1]) / 2, y - 62, "SWITCH?", PAPER, BLACK, anchor="ma")
    # 50/50 + strike
    if CUE["fifty"] <= t < CUE["third"] - .3:
        k = ease((t - CUE["fifty"]) / .25)
        f = F(COND, int(lerp(360, 280, k)))
        d.text((480, DY + DH / 2), "50/50", font=f, fill=PAPER, anchor="mm")
        if t >= CUE["nope"]:
            s = ease((t - CUE["nope"]) / .18)
            d.line([90, DY + DH / 2 + 60, lerp(90, 870, s), DY + DH / 2 - 50], fill=RED, width=22)
    # 1/3 vs 2/3
    if t >= CUE["third"]:
        k1 = (t - CUE["third"]) / .5
        y = DY + DH + 26
        bracket(d, DX[0] - DW / 2, DX[0] + DW / 2, y, "1/3", PAPER, k1)
        k2 = (t - CUE["third"] - .5) / .5
        mv = ease((t - CUE["move"]) / .9)
        xb_right = lerp(DX[2] + DW / 2, DX[1] + DW / 2, mv)
        bracket(d, DX[1] - DW / 2, xb_right, y, "2/3", RED, k2)
        if 0 < mv < 1:   # probability mass flowing from door 3 into door 2
            for j in range(26):
                p = (mv * 1.4 - j / 40)
                if 0 < p < 1:
                    x = lerp(DX[2], DX[1], ease_io(p)); yy = DY + DH * .5 - math.sin(p * math.pi) * 180 + (j % 5) * 16
                    d.rectangle([x - 5, yy - 5, x + 5, yy + 5], fill=RED)

GX0, GY0, CELL = 120, 430, 7
def sim_scene(img, d, t):
    k = ease_io((t - CUE["sim"] - .25) / 3.2)
    n = int(k * SIM["n"])
    a = np.array(img)
    if n > 0:
        idx = np.arange(n); r, c = idx // 100, idx % 100
        col = np.where(ORDER[:n, None] == 1, np.array(RED), np.array((150, 150, 146)))
        for dy in range(CELL - 1):
            for dx in range(CELL - 1):
                a[GY0 + r * CELL + dy, GX0 + c * CELL + dx] = col
    img.paste(Image.fromarray(a))
    d = ImageDraw.Draw(img)
    sw = int(ORDER[:n].sum()); st = n - sw
    d.text((GX0, GY0 - 120), "SWITCH", font=F(MONO, 26), fill=RED)
    d.text((GX0, GY0 - 88), f"{sw:,}", font=F(COND, 64), fill=RED)
    d.text((GX0 + 700, GY0 - 120), "STAY", font=F(MONO, 26), fill=GREY, anchor="ra")
    d.text((GX0 + 700, GY0 - 88), f"{st:,}", font=F(COND, 64), fill=PAPER, anchor="ra")
    if n == SIM["n"]:
        d.text((GX0, GY0 + 712), f"{sw / n:.1%}", font=F(COND, 64), fill=RED)
        d.text((GX0 + 700, GY0 + 712), f"{st / n:.1%}", font=F(COND, 64), fill=PAPER, anchor="ra")
    d.text((GX0 + 350, GY0 - 150), f"games played: {n:,} / {SIM['n']:,}  ·  seed {SIM['seed']}", font=F(MONO, 22), fill=GREY, anchor="ma")

def end_scene(img, d, t):
    k = ease((t - CUE["end"]) / .3)
    d.text((480, 760), "SWITCH.", font=F(COND, int(lerp(330, 250, k))), fill=RED, anchor="mm")
    if t > CUE["end"] + .7:
        d.text((480, 930), "every time.", font=F(COND, 96), fill=PAPER, anchor="mm")
    if t > CUE["end"] + 1.2:
        d.line([100, 1030, 860, 1030], fill=(110, 110, 106), width=1)
        d.text((480, 1060), f"exact: stay {PROOF['exact']['stay']} · switch {PROOF['exact']['switch']}", font=F(MONO, 26), fill=GREY, anchor="ma")
        d.text((480, 1100), f"simulated: {SIM['switch_wins']:,} / {SIM['n']:,} wins by switching", font=F(MONO, 26), fill=GREY, anchor="ma")
        mono_tag(d, 480, 1170, "@vascoda.soda", PAPER, BLACK, size=30, anchor="ma")

_g = np.random.default_rng(3)
GRAIN = [(_g.normal(0, 9, (H // 2, W // 2, 1))).repeat(2, 0).repeat(2, 1).astype(np.int16) for _ in range(6)]
yy_, xx_ = np.mgrid[0:H, 0:W]
VIG = (1 - 0.3 * np.clip(np.hypot((xx_ - W / 2) / (W * .75), (yy_ - H / 2) / (H * .62)) - .35, 0, 1) ** 1.5)[..., None]

def render_frame(fr):
    t = fr / FPS
    img = Image.new("RGB", (W, H), BLACK); d = ImageDraw.Draw(img)
    captions(d)
    if t < CUE["sim"]: doors_scene(img, d, t)
    elif t < CUE["end"]: sim_scene(img, d, t)
    else: end_scene(img, d, t)
    d = ImageDraw.Draw(img)
    if t < CUE["end"]: subtitle(d, t, 1200 if t < CUE["sim"] else 1290)
    arr = (np.array(img).astype(np.int16) + GRAIN[fr % 6]) * VIG
    return np.clip(arr, 0, 255).astype(np.uint8)

# ---------------------------------------------------------------- sound
rng = np.random.default_rng(7)
def lp(x, fc): b, a = butter(2, fc / (SR / 2)); return lfilter(b, a, x)
def hp(x, fc): b, a = butter(2, fc / (SR / 2), "high"); return lfilter(b, a, x)
def bp(x, lo, hi): b, a = butter(2, [lo / (SR / 2), hi / (SR / 2)], "band"); return lfilter(b, a, x)
def env_t(n): return np.arange(n) / SR
def thud(amp=.7, f0=90, f1=38, dur=.6):
    t = env_t(int(dur * SR)); f = f1 + (f0 - f1) * np.exp(-t * 20)
    return amp * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)
def creak(dur=.7, amp=.18):
    t = env_t(int(dur * SR)); f = 140 + 60 * np.sin(t * 9) + 80 * t
    saw = 2 * ((np.cumsum(f) / SR) % 1) - 1
    return amp * bp(saw * (1 + .5 * rng.standard_normal(len(t))), 300, 2500) * np.sin(np.pi * t / dur)
def swipe(dur=.2, amp=.3):
    t = env_t(int(dur * SR)); return amp * bp(rng.standard_normal(len(t)), 800, 7000) * np.sin(np.pi * t / dur) ** 2
def tick(amp=.08):
    n = int(.004 * SR); return amp * hp(rng.standard_normal(n), 3000) * np.linspace(1, 0, n)
def bell(f, amp=.08, dur=1.4):
    t = env_t(int(dur * SR)); return amp * (np.sin(2 * np.pi * f * t) + .3 * np.sin(4 * np.pi * f * t)) * np.exp(-t * 3)
def pad(freqs, dur, amp=.05, cutoff=1000, att=.8):
    t = env_t(int(dur * SR)); L = np.zeros(len(t)); R = np.zeros(len(t))
    for i, f in enumerate(freqs):
        L += 2 * ((f * 0.998 * t + i * .13) % 1) - 1; R += 2 * ((f * 1.002 * t + i * .29) % 1) - 1
    e = np.minimum(1, t / att) * np.minimum(1, (dur - t) / .6)
    return lp(L, cutoff) * e * amp, lp(R, cutoff) * e * amp

def build_audio(path):
    n = int((TOTAL_S + 1) * SR)
    vo = np.zeros(n); mL = np.zeros(n); mR = np.zeros(n); fx = np.zeros((n, 2))
    def put(buf, x, t0):
        s = int(t0 * SR); e = min(len(buf), s + len(x)); buf[s:e] += x[:e - s]
    def putfx(x, t0, pan=0.):
        s = int(t0 * SR); e = min(n, s + len(x)); x = x[:e - s]
        fx[s:e, 0] += x * (1 - max(0, pan)); fx[s:e, 1] += x * (1 + min(0, pan))
    for m in META:
        a, sr = sf.read(os.path.join(HERE, "vo", m["id"] + ".wav"), dtype="float64")
        a = resample_poly(a, SR, sr); put(vo, a, T[m["id"]]["start"])
    # music: A minor pad, cut out at "It's not.", back at the 1/3 explanation, brighter for the result
    chords = [[110, 130.8, 164.8, 196], [87.3, 110, 130.8, 164.8], [130.8, 164.8, 196, 246.9], [98, 123.5, 146.8, 196]]
    def bed(t0, t1, bright=1.0):
        bar = 2.0; tt = t0; i = 0
        while tt < t1 - .2:
            dur = min(bar + .6, t1 - tt + .4)
            l, r = pad(chords[i % 4], dur, .05, 900 * bright)
            put(mL, l, tt); put(mR, r, tt)
            tsub = env_t(int(dur * SR)); sub = .12 * np.sin(2 * np.pi * chords[i % 4][0] / 2 * tsub) * np.minimum(1, tsub / .05) * np.minimum(1, (dur - tsub) / .4)
            put(mL, sub, tt); put(mR, sub, tt)
            tt += bar; i += 1
    bed(0, CUE["nope"])
    bed(CUE["third"] - .2, CUE["sim"])
    bed(CUE["sim"], TOTAL_S - .2, bright=1.6)
    # effects
    for i in range(3): putfx(thud(.35, 120, 50, .3), LEAD + .1 + i * .25)
    putfx(thud(.45, 140, 60, .25), CUE["pick"])
    putfx(creak(), CUE["open"]); putfx(thud(.3, 80, 40), CUE["goat"])
    putfx(swipe(.25, .2), CUE["offer"], .3)
    putfx(thud(.8, 100, 32, .9), CUE["fifty"])
    putfx(swipe(.18, .5), CUE["nope"]); putfx(thud(.9, 70, 28, 1.2), CUE["nope"])
    for j in range(20): putfx(tick(.03), CUE["move"] + j * .045, -.3 + j * .03)
    putfx(thud(.5, 110, 45, .4), CUE["move"] + .9)
    k_prev = 0
    for fr in range(int(CUE["sim"] * FPS), int((CUE["sim"] + 3.6) * FPS)):
        k = ease_io((fr / FPS - CUE["sim"] - .25) / 3.2)
        if k > k_prev + .008: putfx(tick(.025 + .025 * k), fr / FPS, ((fr % 7) - 3) / 6)
        k_prev = k
    for j, f in enumerate([440, 554.4, 659.3, 880]): putfx(bell(f, .06), CUE["result"] + j * .12)
    putfx(thud(.9, 100, 30, 1.0), CUE["end"])
    for j, f in enumerate([220, 277.2, 329.6, 440, 554.4]): putfx(bell(f, .05, 2.2), CUE["end"] + .05 + j * .05)
    # ducking: music −12 dB under the voice (smoothed envelope)
    ev = np.abs(vo); ev = lp(np.maximum.accumulate(ev[::-1])[::-1] * 0 + ev, 6)
    ev = np.convolve(np.abs(vo), np.ones(int(.12 * SR)) / int(.12 * SR), "same")
    duck = 1 - .75 * np.clip(ev / (ev.max() * .15 + 1e-9), 0, 1)
    L = vo * 1.0 + mL * duck + fx[:, 0]; R = vo * 1.0 + mR * duck + fx[:, 1]
    st = np.stack([L, R], 1)[: int(TOTAL_S * SR)]
    st /= np.abs(st).max() / .9
    fade = int(.4 * SR); st[-fade:] *= np.linspace(1, 0, fade)[:, None]
    with wave.open(path, "wb") as w_:
        w_.setnchannels(2); w_.setsampwidth(2); w_.setframerate(SR); w_.writeframes((st * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    out = sys.argv[1]
    if "--t" in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index("--t") + 1].split(",")]
        ims = [Image.fromarray(render_frame(int(x * FPS))).resize((270, 480)) for x in ts]
        sh = Image.new("RGB", (270 * len(ims), 480))
        for i, im in enumerate(ims): sh.paste(im, (270 * i, 0))
        sh.save(out); print("saved", out, "total", round(TOTAL_S, 2), {k: round(v, 2) for k, v in CUE.items()}); sys.exit()
    wav = out.replace(".mp4", ".wav"); build_audio(wav); print("audio ok", flush=True)
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-i", wav, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "24", "-preset", "medium",
                          "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest",
                          "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for fr in range(TOTAL):
        p.stdin.write(render_frame(fr).tobytes())
        if fr % 150 == 0: print("frame", fr, "/", TOTAL, flush=True)
    p.stdin.close(); p.wait(); print("done", out, round(TOTAL / FPS, 2), "s")
