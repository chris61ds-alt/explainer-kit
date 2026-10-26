"""NOT JUST YOU – No. 01: your recorded voice. Editorial monochrome, Reel 9:16 with safe zones, deterministic per frame.
Usage: python3 render.py out.mp4 | python3 render.py sheet.png --t 1,2,3
"""
import json, math, os, sys, wave, subprocess
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont
from scipy.signal import resample_poly, butter, lfilter

HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(HERE, "..", "fonts") + "/"
W, H, FPS, SR = 1080, 1920, 30, 48000
SAFE_R, SAFE_B = 900, 1480                       # Instagram: buttons right, caption bottom
BLACK = (8, 8, 8); PAPER = (236, 235, 231); GREY = (150, 150, 146); DARK = (44, 44, 42); RED = (228, 38, 28)
_f = {}
def F(n, s):
    if (n, s) not in _f: _f[(n, s)] = ImageFont.truetype(FD + n, s)
    return _f[(n, s)]
COND, MONO, MONOB = "Roboto-Condensed-Bold.woff", "roboto-mono-latin-500.woff", "roboto-mono-latin-700.woff"
def ease(k): k = max(0., min(1., k)); return 1 - (1 - k) ** 3
def ease_io(k): k = max(0., min(1., k)); return k * k * (3 - 2 * k)
def lerp(a, b, k): return a + (b - a) * k
def mix(a, b, k): k = max(0, min(1, k)); return tuple(int(lerp(x, y, k)) for x, y in zip(a, b))

PROOF = json.load(open(os.path.join(HERE, "proof.json")))
META = json.load(open(os.path.join(HERE, "vo", "meta.json")))
VO = {m["id"]: sf.read(os.path.join(HERE, "vo", m["id"] + ".wav"))[0] for m in META}

LEAD = 0.4
GAP = {"hook": .5, "alone": .4, "bone": .3, "low": .5, "demo_in": .6, "demo_rec": .7, "record": .6, "twist": .5, "result": .5, "point": .6, "end": 2.2}
T, t = {}, LEAD
for m in META:
    T[m["id"]] = dict(start=t, dur=m["dur"], text=m["text"]); t += m["dur"] + GAP.get(m["id"], .35)
TOTAL_S = t; TOTAL = int(round(TOTAL_S * FPS))
def S(k): return T[k]["start"]
def E(k): return T[k]["start"] + T[k]["dur"]
def cue(beat, word):
    b = T[beat]; i = b["text"].lower().find(word.lower())
    if i < 0: raise ValueError(f"cue '{word}' missing in '{beat}'")
    return b["start"] + b["dur"] * i / len(b["text"])

# ---------------------------------------------------------------- helpers
def header(d):
    d.text((60, 228), "NOT JUST YOU — NO. 01", font=F(MONO, 24), fill=GREY)
    d.text((SAFE_R, 228), "YOUR RECORDED VOICE", font=F(MONO, 24), fill=GREY, anchor="ra")
    d.line([60, 274, SAFE_R, 274], fill=(110, 110, 106), width=1)

def wrap(text, font, maxw, d):
    out, cur = [], ""
    for w_ in text.split():
        tst = (cur + " " + w_).strip()
        if d.textlength(tst, font=font) <= maxw: cur = tst
        else: out.append(cur); cur = w_
    out.append(cur); return out

def subtitle(d, t, y0=1250):
    cur = None
    for k, b in T.items():
        if t >= b["start"] - .05: cur = k
    if cur in (None, "end"): return
    b = T[cur]
    if t > b["start"] + b["dur"] + .5: return
    f = F(COND, 60); lines = wrap(b["text"], f, SAFE_R - 70, d)
    shown = (t - b["start"]) / b["dur"] * len(b["text"]); c = 0
    for li, line in enumerate(lines):
        x = 70
        for w_ in line.split(" "):
            d.text((x, y0 + li * 72), w_, font=f, fill=PAPER if c <= shown else DARK)
            x += d.textlength(w_ + " ", font=f); c += len(w_) + 1

def mono_tag(d, x, y, text, bg, fg, size=24, anchor="la"):
    f = F(MONOB, size); w_ = d.textlength(text, font=f)
    if anchor == "ma": x -= (w_ + 18) / 2
    if anchor == "ra": x -= w_ + 18
    d.rectangle([x, y, x + w_ + 18, y + size + 14], fill=bg); d.text((x + 9, y + 6), text, font=f, fill=fg)

def waveform(d, audio, t_local, x0, x1, yc, h, col, window=1.2, sr=24000):
    n = int(window * sr); end = int(t_local * sr); seg = audio[max(0, end - n):end]
    if len(seg) < 10: return
    cols = int((x1 - x0) / 6)
    chunks = np.array_split(np.abs(seg), cols)
    off = cols - len(chunks)
    for i, c in enumerate(chunks):
        v = min(1, (c.max() if len(c) else 0) * 1.4) * h
        x = x0 + (i + off) * 6
        d.rectangle([x, yc - v, x + 3, yc + v], fill=col)

# ---------------------------------------------------------------- head diagram
HEAD = [(120, 560), (110, 470), (80, 380), (70, 260), (100, 150), (170, 70), (270, 40), (360, 60), (420, 120), (440, 190), (445, 230),
        (470, 290), (505, 330), (470, 345), (468, 370), (482, 395), (466, 410), (480, 432), (460, 465), (430, 490), (380, 500), (350, 560)]
HX, HY, HS = 160, 330, 1.18
def hp_(p): return (HX + p[0] * HS, HY + p[1] * HS)
MOUTH = hp_((470, 412)); EAR = hp_((235, 300)); COCH = hp_((262, 305)); THROAT = hp_((390, 470))

def bez(p0, p1, p2, n=60): return [((1 - s) ** 2 * p0[0] + 2 * (1 - s) * s * p1[0] + s * s * p2[0], (1 - s) ** 2 * p0[1] + 2 * (1 - s) * s * p1[1] + s * s * p2[1]) for s in np.linspace(0, 1, n)]
AIR_PATH = bez(MOUTH, hp_((520, 120)), hp_((215, 230)), 80)

def head_scene(img, d, t):
    k = ease((t - S("twice")) / .6)
    outline = [hp_(p) for p in HEAD]
    d.line(outline, fill=mix(BLACK, PAPER, k), width=4, joint="curve")
    # ear
    ex, ey = EAR
    d.arc([ex - 26, ey - 40, ex + 26, ey + 40], 100, 280, fill=mix(BLACK, PAPER, k), width=4)
    # sound leaving the mouth
    if t >= S("twice"):
        for j in range(4):
            r = ((t - S("twice")) * 140 + j * 45) % 180
            if r > 10:
                d.arc([MOUTH[0] - r, MOUTH[1] - r, MOUTH[0] + r, MOUTH[1] + r], -50, 50, fill=mix(BLACK, PAPER, (1 - r / 180) * .8), width=3)
    # air path: dotted, flowing toward the ear
    if t >= S("air") - .1:
        ka = ease((t - S("air")) / .9); n = int(len(AIR_PATH) * ka)
        dim = .35 if t >= E("record") + .3 else 1
        for i in range(0, n - 1):
            if (i + int(t * 20)) % 4 < 2:
                d.line([AIR_PATH[i], AIR_PATH[i + 1]], fill=mix(BLACK, PAPER, dim), width=5)
        if ka > .9: mono_tag(d, hp_((470, 60))[0], hp_((470, 60))[1], "AIR", PAPER, BLACK)
    # bone path: thick red low wave through the head
    if t >= S("bone") - .1:
        kb = ease((t - S("bone")) / .8)
        dim_b = .25 if (S("record") <= t) else 1
        x0, y0 = THROAT; x1, y1 = COCH
        pts = []
        for s in np.linspace(0, kb, 60):
            x = lerp(x0, x1, s); y = lerp(y0, y1, s) + math.sin(s * 9 - t * 6) * 16
            pts.append((x, y))
        if len(pts) > 1: d.line(pts, fill=mix(BLACK, RED, dim_b), width=9, joint="curve")
        if kb > .9:
            cx, cy = COCH
            for r in range(4, 26, 5): d.arc([cx - r, cy - r, cx + r, cy + r], r * 20 % 360, r * 20 % 360 + 260, fill=mix(BLACK, RED, dim_b), width=4)
            mono_tag(d, hp_((150, 380))[0], hp_((150, 380))[1], "BONE", mix(BLACK, RED, dim_b), PAPER)
    # recording: microphone only catches the air
    if t >= S("record"):
        km = ease((t - S("record")) / .5)
        mx, my = lerp(SAFE_R + 80, 800, km), 700
        d.rounded_rectangle([mx - 32, my - 80, mx + 32, my + 20], radius=32, outline=PAPER, width=5)
        for yy in range(int(my - 60), int(my + 10), 14): d.line([mx - 20, yy, mx + 20, yy], fill=GREY, width=2)
        d.arc([mx - 52, my - 30, mx + 52, my + 50], 0, 180, fill=PAPER, width=5); d.line([mx, my + 50, mx, my + 110], fill=PAPER, width=5)
        d.line([mx - 40, my + 110, mx + 40, my + 110], fill=PAPER, width=5)
        if km > .9:
            mono_tag(d, mx, my + 130, "AIR ONLY", PAPER, BLACK, anchor="ma")
            pr = (t - S("record")) % 1.2 / 1.2
            d.ellipse([mx - 9, my - 150 - 9, mx + 9, my - 150 + 9], fill=RED if pr < .5 else BLACK)
    # low frequencies note
    if t >= cue("low", "low frequencies"):
        mono_tag(d, 60, 1080, "BONE CONDUCTION BOOSTS THE LOWS", RED, PAPER, size=22)

# ---------------------------------------------------------------- spectrum demo (real band levels of the two demo files)
SPI, SPR = np.array(PROOF["spectrum_inside"]), np.array(PROOF["spectrum_recording"])
TOP = max(SPI.max(), SPR.max()); RNG = 45.0
def spec_scene(img, d, t):
    x0, x1, yb, hmax = 80, 880, 1040, 600
    bw = (x1 - x0) / 24
    playing_in = S("demo_in") - .1 <= t < S("demo_rec") - .1
    playing_rec = t >= S("demo_rec") - .1
    ki = ease((t - S("demo_in")) / .5); kr = ease((t - S("demo_rec")) / .5)
    d.line([x0, yb, x1, yb], fill=GREY, width=2)
    for i in range(24):
        hi = max(0, (SPI[i] - (TOP - RNG)) / RNG) * hmax * ki
        hr = max(0, (SPR[i] - (TOP - RNG)) / RNG) * hmax * kr
        x = x0 + i * bw
        if hi > 0: d.rectangle([x + 3, yb - hi, x + bw - 3, yb], fill=mix(BLACK, RED, .55 if playing_rec else 1))
        if hr > 0: d.rectangle([x + 3, yb - hr, x + bw - 3, yb], outline=PAPER, width=3)
    edges = PROOF["band_edges_hz"]
    for hz, lab in ((60, "60 Hz"), (500, "500 Hz"), (8000, "8 kHz")):
        i = np.searchsorted(edges, hz) - (1 if hz == 8000 else 0)
        x = x0 + min(24, i) * bw
        d.line([x, yb, x, yb + 14], fill=GREY, width=2)
        d.text((x, yb + 22), lab, font=F(MONO, 22), fill=GREY, anchor="ma")
    xl = x0 + (np.searchsorted(edges, 500)) * bw
    d.rectangle([x0, 330, xl, 360], fill=RED); d.text(((x0 + xl) / 2, 333), "LOWS", font=F(MONOB, 22), fill=PAPER, anchor="ma")
    mono_tag(d, x0, 390, "▶ INSIDE YOUR HEAD" if False else "INSIDE YOUR HEAD", RED if playing_in else DARK, PAPER, size=26)
    if t >= S("demo_rec") - .1:
        mono_tag(d, SAFE_R, 390, "ON A RECORDING", PAPER if playing_rec else DARK, BLACK if playing_rec else GREY, size=26, anchor="ra")
    d.text((x0, 1100), f"low-band difference ≈ {PROOF['low_band_db_difference']} dB  ·  simulated bone path", font=F(MONO, 22), fill=GREY)
    # live waveform of the playing demo
    if playing_in: waveform(d, VO["demo_in"], t - S("demo_in"), x0, x1, 480, 40, RED)
    if playing_rec: waveform(d, VO["demo_rec"], t - S("demo_rec"), x0, x1, 480, 40, PAPER)

# ---------------------------------------------------------------- study scene
TILES = 12; YOU = 7
def study_scene(img, d, t):
    k0 = S("study")
    d.text((70, 320), "HUGHES & HARRISON, 2013", font=F(MONOB, 26), fill=PAPER)
    d.text((70, 360), "Perception 42(9) · 80 participants", font=F(MONO, 24), fill=GREY)
    reveal = t >= cue("result", "most didn't")
    for i in range(TILES):
        if t < k0 + .3 + i * .12: continue
        r, c = divmod(i, 3)
        x = 70 + c * 280; y = 430 + r * 150
        you = i == YOU
        col = RED if (you and reveal) else GREY
        d.rectangle([x, y, x + 250, y + 120], outline=col if (you and reveal) else DARK, width=4 if (you and reveal) else 2)
        rr = np.random.default_rng(i)
        for j in range(26):
            v = (0.2 + 0.8 * rr.random()) * 40 * (0.6 + 0.4 * math.sin(j * .5 + i))
            d.rectangle([x + 14 + j * 9, y + 60 - v, x + 18 + j * 9, y + 60 + v], fill=col)
        lab = "YOUR VOICE" if (you and reveal) else f"VOICE {i + 1:02d}"
        d.text((x + 12, y + 92), lab, font=F(MONOB if (you and reveal) else MONO, 18), fill=PAPER if (you and reveal) else GREY)
    if t >= cue("result", "rated it higher"):
        k = ease((t - cue("result", "rated it higher")) / .6)
        y = 1060
        d.text((70, y - 4), "HOW YOU RATED IT", font=F(MONO, 22), fill=PAPER)
        d.rectangle([420, y, 420 + 440 * k, y + 26], fill=RED)
        d.text((70, y + 44), "HOW OTHERS RATED IT", font=F(MONO, 22), fill=GREY)
        d.rectangle([420, y + 48, 420 + 300 * k, y + 74], fill=GREY)
        d.text((70, y + 96), "schematic — direction from the study, not to scale", font=F(MONO, 18), fill=(100, 100, 96))

# ---------------------------------------------------------------- big type scenes
def big(d, lines, t0, t, colors=None, y=760, size=200):
    for i, line in enumerate(lines):
        k = ease((t - t0 - i * .15) / .35)
        if k <= 0: continue
        col = (colors or [PAPER] * len(lines))[i]
        d.text((70, y + i * size * .95 + (1 - k) * 40), line, font=F(COND, size), fill=mix(BLACK, col, k))

def hook_scene(img, d, t):
    waveform(d, VO["hook"], t - S("hook"), 70, SAFE_R, 760, 120, RED, window=1.8)
    if (int(t * 2) % 2 == 0): d.ellipse([70, 330, 96, 356], fill=RED)
    d.text((110, 328), "REC", font=F(MONOB, 26), fill=PAPER)
    d.text((SAFE_R, 328), f"00:0{min(9, int(t))}", font=F(MONO, 26), fill=GREY, anchor="ra")

def alone_scene(img, d, t):
    k = ease((t - S("alone")) / 1.2)
    n = int(48 * k)
    for i in range(n):
        r, c = divmod(i, 8)
        x = 90 + c * 100; y = 420 + r * 100
        rr = np.random.default_rng(100 + i)
        for j in range(6):
            v = (0.3 + 0.7 * rr.random()) * 26 * (0.5 + .5 * math.sin(t * 7 + i + j))
            d.rectangle([x + j * 11, y + 30 - v, x + j * 11 + 5, y + 30 + v], fill=RED if i == 19 else GREY)
    if k >= 1: mono_tag(d, 70, 1060, "MOST PEOPLE KNOW THIS FEELING", PAPER, BLACK, size=22)

def end_scene(img, d, t):
    big(d, ["NOT", "JUST", "YOU."], S("end"), t, [PAPER, PAPER, RED], y=420, size=250)
    if t > S("end") + 1.0:
        d.line([70, 1170, SAFE_R, 1170], fill=(110, 110, 106), width=1)
        d.text((70, 1195), "Sources", font=F(MONOB, 22), fill=PAPER)
        d.text((70, 1230), "Hullar, Washington Univ. (Scientific American)", font=F(MONO, 20), fill=GREY)
        d.text((70, 1260), "Hughes & Harrison (2013), Perception 42(9)", font=F(MONO, 20), fill=GREY)
        mono_tag(d, 70, 1320, "@vascoda.soda", PAPER, BLACK, size=30)

# ---------------------------------------------------------------- frame
_g = np.random.default_rng(3)
GRAIN = [(_g.normal(0, 9, (H // 2, W // 2, 1))).repeat(2, 0).repeat(2, 1).astype(np.int16) for _ in range(6)]
yy_, xx_ = np.mgrid[0:H, 0:W]
VIG = (1 - 0.3 * np.clip(np.hypot((xx_ - W / 2) / (W * .75), (yy_ - H / 2) / (H * .62)) - .35, 0, 1) ** 1.5)[..., None]

def render_frame(fr):
    t = fr / FPS
    img = Image.new("RGB", (W, H), BLACK); d = ImageDraw.Draw(img)
    header(d)
    if t < S("alone"): hook_scene(img, d, t)
    elif t < S("twice"): alone_scene(img, d, t)
    elif t < S("demo_in") - .2: head_scene(img, d, t)
    elif t < S("record") - .1: spec_scene(img, d, t)
    elif t < S("twist") - .1: head_scene(img, d, t)
    elif t < S("study"): big(d, ["HERE'S", "THE TWIST."], S("twist"), t, [PAPER, RED], y=620, size=180)
    elif t < S("point"): study_scene(img, d, t)
    elif t < S("end"): big(d, ["IT'S NOT", "YOUR VOICE.", "IT'S THE", "SURPRISE."], S("point"), t, [PAPER, PAPER, PAPER, RED], y=380, size=160)
    else: end_scene(img, d, t)
    if t < S("end"): subtitle(d, t)
    arr = (np.array(img).astype(np.int16) + GRAIN[fr % 6]) * VIG
    return np.clip(arr, 0, 255).astype(np.uint8)

# ---------------------------------------------------------------- sound
rng = np.random.default_rng(7)
def lp(x, fc): b, a = butter(2, fc / (SR / 2)); return lfilter(b, a, x)
def bp(x, lo, hi): b, a = butter(2, [lo / (SR / 2), hi / (SR / 2)], "band"); return lfilter(b, a, x)
def tt_(dur): return np.arange(int(dur * SR)) / SR
def thud(amp=.7, f0=90, f1=38, dur=.6):
    t = tt_(dur); f = f1 + (f0 - f1) * np.exp(-t * 20); return amp * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)
def swipe(dur=.22, amp=.3):
    t = tt_(dur); return amp * bp(rng.standard_normal(len(t)), 800, 7000) * np.sin(np.pi * t / dur) ** 2
def bell(f, amp=.06, dur=1.6):
    t = tt_(dur); return amp * (np.sin(2 * np.pi * f * t) + .3 * np.sin(4 * np.pi * f * t)) * np.exp(-t * 3)
def pad(freqs, dur, amp=.045, cutoff=900):
    t = tt_(dur); L = np.zeros(len(t)); R = np.zeros(len(t))
    for i, f in enumerate(freqs):
        L += 2 * ((f * .998 * t + i * .13) % 1) - 1; R += 2 * ((f * 1.002 * t + i * .29) % 1) - 1
    e = np.minimum(1, t / .8) * np.minimum(1, (dur - t) / .6); return lp(L, cutoff) * e * amp, lp(R, cutoff) * e * amp

def build_audio(path):
    n = int((TOTAL_S + 1) * SR); vo = np.zeros(n); mL = np.zeros(n); mR = np.zeros(n); fx = np.zeros((n, 2))
    def put(buf, x, t0):
        s = int(t0 * SR); e = min(len(buf), s + len(x)); buf[s:e] += x[:e - s]
    def putfx(x, t0, pan=0.):
        s = int(t0 * SR); e = min(n, s + len(x)); x = x[:e - s]
        fx[s:e, 0] += x * (1 - max(0, pan)); fx[s:e, 1] += x * (1 + min(0, pan))
    for m in META:
        a = resample_poly(VO[m["id"]], SR, m["sr"]); put(vo, a, T[m["id"]]["start"])
    chords = [[110, 130.8, 164.8, 196], [87.3, 110, 130.8, 164.8], [130.8, 164.8, 196, 246.9], [98, 123.5, 146.8, 196]]
    def bed(t0, t1, bright=1.):
        tt = t0; i = 0
        while tt < t1 - .2:
            dur = min(2.6, t1 - tt + .4); l, r = pad(chords[i % 4], dur, .045, 900 * bright); put(mL, l, tt); put(mR, r, tt)
            ts = tt_(dur); sub = .1 * np.sin(2 * np.pi * chords[i % 4][0] / 2 * ts) * np.minimum(1, ts / .05) * np.minimum(1, (dur - ts) / .4)
            put(mL, sub, tt); put(mR, sub, tt); tt += 2.0; i += 1
    bed(S("alone") - .3, S("demo_in") - .3)              # music silent under the hook and the demo
    bed(S("record"), S("twist"))
    bed(S("study") - .2, TOTAL_S - .2, 1.5)
    putfx(thud(.3, 140, 60, .2), .15)                      # rec button
    putfx(swipe(.2, .2), S("twice"))
    putfx(thud(.5, 110, 40, .5), S("bone"))
    putfx(swipe(.22, .3), S("twist") - .05); putfx(thud(.9, 80, 30, 1.0), S("twist"))
    putfx(bell(659.3), cue("result", "most didn't")); putfx(bell(880), cue("result", "rated it higher"))
    putfx(thud(.8, 90, 30, 1.0), S("point"))
    for j, f in enumerate([220, 277.2, 329.6, 440, 554.4]): putfx(bell(f, .05, 2.2), S("end") + j * .06)
    env = np.convolve(np.abs(vo), np.ones(int(.12 * SR)) / int(.12 * SR), "same")
    duck = 1 - .75 * np.clip(env / (env.max() * .15 + 1e-9), 0, 1)
    L = vo + mL * duck + fx[:, 0]; R = vo + mR * duck + fx[:, 1]
    st = np.stack([L, R], 1)[: int(TOTAL_S * SR)]; st /= np.abs(st).max() / .9
    fd = int(.4 * SR); st[-fd:] *= np.linspace(1, 0, fd)[:, None]
    with wave.open(path, "wb") as w_:
        w_.setnchannels(2); w_.setsampwidth(2); w_.setframerate(SR); w_.writeframes((st * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    out = sys.argv[1]
    if "--t" in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index("--t") + 1].split(",")]
        ims = []
        for x in ts:
            im = Image.fromarray(render_frame(int(x * FPS))).convert("RGBA"); ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(ov)
            g.rectangle([0, 0, W, 200], fill=(0, 160, 255, 60)); g.rectangle([0, SAFE_B, W, H], fill=(0, 160, 255, 60)); g.rectangle([960, 900, W, SAFE_B], fill=(0, 160, 255, 60))
            ims.append(Image.alpha_composite(im, ov).convert("RGB").resize((270, 480)))
        sh = Image.new("RGB", (270 * len(ims), 480))
        for i, im in enumerate(ims): sh.paste(im, (270 * i, 0))
        sh.save(out); print("saved", out, "total", round(TOTAL_S, 2), {k: round(v["start"], 2) for k, v in T.items()}); sys.exit()
    wav = out.replace(".mp4", ".wav"); build_audio(wav); print("audio ok", flush=True)
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-i", wav, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "28", "-preset", "slow",
                          "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest",
                          "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for fr in range(TOTAL):
        p.stdin.write(render_frame(fr).tobytes())
        if fr % 150 == 0: print("frame", fr, "/", TOTAL, flush=True)
    p.stdin.close(); p.wait(); print("done", out, round(TOTAL / FPS, 2), "s")
