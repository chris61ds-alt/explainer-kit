"""NOT JUST YOU – No. 06: the liking gap (Boothby, Cooney, Sandstrom & Clark, 2018).
Style test 'Clean Pop': less cute — flat faceless figures, off-white + ink + coral, kinetic type,
yellow marker subtitles, punch-in cuts, darker beat. Hook visible from frame 0."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
import cute
from cute import F, BLK, BOLD, MONO, clamp, ease, ease_io, back, lerp, mix, Timeline, W, H, SR, SAFE_R, FPS
from cute import softkick, whoosh, pop, tt_, bp, lp
import numpy as np, soundfile as sf, wave
from PIL import Image
from scipy.signal import resample_poly

# ---------------------------------------------------------------- 'Clean Pop' palette
BG = (246, 244, 239); INK = (18, 18, 24); CORAL = (255, 90, 70); LAV = (124, 104, 238); YEL = (255, 216, 77)
GREY = (214, 211, 204); GREY_D = (140, 137, 130); TEAL = (24, 170, 136); WHITE = (255, 255, 255); PANEL = (28, 28, 36)
cute.BG, cute.INK = BG, INK   # harness background + paper grain use these

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .35, "replay": .4, "study": .3, "q": .45, "gap": .5, "name": .5, "why": .45, "months": .5, "point": .7, "end": 2.4})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "replay", "study", "q", "gap", "name", "why", "months", "point", "end"]

# ---------------------------------------------------------------- primitives
def person(d, x, y, s, col, nod=0.0):
    """flat, faceless figure; (x, y) = bottom of shoulders"""
    d.rounded_rectangle([x - 86 * s, y - 100 * s, x + 86 * s, y + 40 * s], radius=80 * s, fill=col)
    hy = y - 170 * s + nod * 8 * s
    d.ellipse([x - 54 * s, hy - 54 * s, x + 54 * s, hy + 54 * s], fill=col)
    return (x, hy - 54 * s)

def marker(d, box, col=YEL, k=1.0):
    if k <= 0: return
    x0, y0, x1, y1 = box; d.rectangle([x0, y0, x0 + (x1 - x0) * ease(k), y1], fill=col)

def label(d, x, y, text, size=30, fg=INK, bg=None, anchor="la", font=BLK):
    f = F(font, size); w = d.textlength(text, font=f)
    if anchor == "ma": x -= w / 2
    if anchor == "ra": x -= w
    if bg: d.rectangle([x - 14, y - 8, x + w + 14, y + size + 10], fill=bg)
    d.text((x, y), text, font=f, fill=fg)
    return w

def bubble(d, x, y, w, h, col, k=1.0, tail=1):
    if k <= 0: return
    s = ease(k); cx, cy = x + w / 2, y + h / 2
    d.rounded_rectangle([cx - w / 2 * s, cy - h / 2 * s, cx + w / 2 * s, cy + h / 2 * s], radius=22 * s, fill=col)
    if s > .9:
        tx = x + (40 if tail > 0 else w - 40)
        d.polygon([(tx, y + h - 2), (tx + 30 * tail, y + h - 2), (tx - 10 * tail, y + h + 28)], fill=col)
        for i in range(2): d.rounded_rectangle([x + 26, y + 24 + i * 30, x + w - 26 - i * 70, y + 38 + i * 30], radius=7, fill=mix(col, WHITE, .55))

def rewind_icon(d, cx, cy, s, col):
    for o in (0, 1):
        x = cx + (o - .5) * 52 * s
        d.polygon([(x + 26 * s, cy - 30 * s), (x + 26 * s, cy + 30 * s), (x - 26 * s, cy)], fill=col)

def player(d, t, t0, focus=0.0, reveal=0.0):
    """the 'replay' panel used in hook + point"""
    x0, y0, x1, y1 = 60, 320, 900, 1000
    d.rounded_rectangle([x0, y0, x1, y1], radius=36, fill=PANEL)
    for yy in range(y0 + 10, y1, 8): d.line([x0 + 20, yy, x1 - 20, yy], fill=(34, 34, 44), width=2)
    # REC + timecode running backwards
    if int(t * 2) % 2 == 0 or reveal > 0: d.ellipse([x0 + 40, y0 + 40, x0 + 68, y0 + 68], fill=CORAL)
    secs = max(0, 312 - (t - t0) * 37) if reveal <= 0 else 0
    d.text((x0 + 84, y0 + 34), "REPLAY  00:%02d:%02d" % (secs // 60, secs % 60), font=F(MONO, 30), fill=WHITE)
    if reveal <= 0: rewind_icon(d, x1 - 90, y0 + 54, .7 + .08 * math.sin(t * 12), YEL)
    # two people talking
    pa = person(d, 300 - focus * 60, 930, 1.25, LAV)
    pb = person(d, 660 + focus * 20, 930, 1.25, CORAL, nod=math.sin(t * 7) if reveal > 0 else 0)
    if reveal <= 0:
        j = math.sin(t * 40) * 4  # scrub jitter
        bubble(d, 130 + j, 430, 300, 110, WHITE, k=(t - t0) / .25, tail=1)
        if focus <= 0: bubble(d, 520 - j, 540, 300, 110, GREY, k=(t - t0 - .3) / .25, tail=-1)
    return pa, pb

# ---------------------------------------------------------------- scenes
def sc_hook(img, d, t):
    t0 = 0.0
    pa, pb = player(d, t, t0, focus=ease((t - cue("hook", "here's")) / .6))
    if t >= cue("hook", "here's") - .1:
        k = back((t - cue("hook", "here's") + .1) / .35)
        if k > .05:
            s = k; cx, cy = pb[0] + 20, pb[1] - 120
            d.rectangle([cx - 110 * s, cy - 80 * s, cx + 110 * s, cy + 80 * s], fill=YEL)
            d.text((cx, cy), "?", font=F(BLK, int(130 * s)), fill=INK, anchor="mm")

def sc_replay(img, d, t):
    t0 = S("replay")
    x0, x1, y = 90, 870, 640
    # waveform with a flat 'awkward pause'
    pause = (0.34, 0.46); weird = 0.72
    for i in range(140):
        u = i / 139; x = x0 + (x1 - x0) * u
        a = 0 if pause[0] < u < pause[1] else (30 + 70 * abs(math.sin(i * 1.7) * math.sin(i * .43)))
        col = INK if u < clamp((t - t0) / 3.2) else GREY
        d.rounded_rectangle([x - 2, y - a - 3, x + 2, y + a + 3], radius=2, fill=col)
    head = x0 + (x1 - x0) * clamp((t - t0) / 3.2)
    d.line([head, y - 160, head, y + 160], fill=CORAL, width=6); d.ellipse([head - 12, y - 172, head + 12, y - 148], fill=CORAL)
    def flag(u, text, tk, yy, side):
        k = back((t - tk) / .3)
        if k <= .05: return
        x = x0 + (x1 - x0) * u; tw = (d.textlength(text, font=F(BLK, 34)) + 30) * k
        d.line([x, y + 110, x, yy], fill=INK, width=5)
        xa, xb = (x, x + tw) if side > 0 else (x - tw, x)
        d.rectangle([xa, yy - 56 * k, xb, yy], fill=CORAL)
        if k > .8: d.text(((xa + xb) / 2, yy - 28), text, font=F(BLK, 34), fill=WHITE, anchor="mm")
    flag(sum(pause) / 2, "awkward pause", cue("replay", "awkward"), y + 230, -1)
    flag(weird, "why did I say that?", cue("replay", "weird"), y + 330, -1)
    label(d, 90, 380, "YOUR BRAIN, 2 A.M.", 44, INK)
    d.text((90, 440), "re-watching every second", font=F(BOLD, 30), fill=GREY_D)

def sc_study(img, d, t):
    t0 = S("study")
    pa = person(d, 260, 960, 1.35, LAV); pb = person(d, 700, 960, 1.35, CORAL)
    # countdown ring 5:00 → 0:00
    cx, cy, r = 480, 560, 120
    k = clamp((t - cue("study", "five") ) / 2.0)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE)
    d.pieslice([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360 * (1 - k), fill=YEL)
    d.ellipse([cx - r + 26, cy - r + 26, cx + r - 26, cy + r - 26], fill=WHITE)
    rem = int(300 * (1 - k)); d.text((cx, cy), "%d:%02d" % (rem // 60, rem % 60), font=F(BLK, 64), fill=INK, anchor="mm")
    label(d, 90, 340, "STRANGERS", 40, WHITE, bg=INK)
    label(d, 90, 400, "Boothby et al., 2018 · Psych. Science", 24, GREY_D, font=BOLD)
    if t >= cue("study", "two questions"):
        kk = back((t - cue("study", "two questions")) / .3)
        d.ellipse([700 - 50 * kk, 400 - 50 * kk, 700 + 50 * kk, 400 + 50 * kk], fill=CORAL)
        if kk > .6: d.text((700, 400), "2", font=F(BLK, 60), fill=WHITE, anchor="mm")
        if kk > .6: d.text((770, 400), "questions", font=F(BLK, 30), fill=INK, anchor="lm")

def slider_card(d, y, q, k, col, val=None, tag=None, kv=0.0):
    if k <= 0: return
    dx = (1 - ease(k)) * 600
    x0 = 60 + dx
    d.rounded_rectangle([x0, y, x0 + 840, y + 250], radius=28, fill=WHITE)
    d.text((x0 + 40, y + 34), q, font=F(BLK, 38), fill=INK)
    d.rounded_rectangle([x0 + 40, y + 160, x0 + 800, y + 184], radius=12, fill=GREY)
    if val is not None:
        v = val * ease(kv)
        d.rounded_rectangle([x0 + 40, y + 160, x0 + 40 + 760 * v, y + 184], radius=12, fill=col)
        d.ellipse([x0 + 40 + 760 * v - 24, y + 148, x0 + 40 + 760 * v + 24, y + 196], fill=col)
    if tag: d.text((x0 + 40, y + 100), tag, font=F(BOLD, 26), fill=GREY_D)

def sc_q(img, d, t):
    slider_card(d, 360, "How much did you like them?", (t - S("q")) / .35, LAV, .82, "rate 1–7", kv=(t - S("q") - .6) / .6)
    slider_card(d, 660, "How much did they like you?", (t - cue("q", "and how much")) / .35, CORAL, .55, "your guess", kv=(t - cue("q", "liked you")) / .6)

def sc_gap(img, d, t):
    t0 = S("gap"); yb = 1060
    bars = (("THEY LIKED YOU", .86, LAV, t0 + .2), ("YOU THOUGHT", .58, CORAL, t0 + .5))
    for i, (lab, v, col, tk) in enumerate(bars):
        x = 250 + i * 400; k = ease((t - tk) / .55); h = 560 * v * k
        d.rectangle([x - 120, yb - h, x + 120, yb], fill=col)
        d.text((x, yb + 40), lab, font=F(BLK, 32), fill=INK, anchor="mm")
    if t >= cue("gap", "more than"):
        k = ease((t - cue("gap", "more than")) / .4)
        ya, yt = yb - 560 * .86, yb - 560 * .58
        d.line([400, ya, 400 + 420 * k, ya], fill=INK, width=4)
        if k > .95:
            d.rectangle([800, ya, 860, yt], fill=YEL)
            d.text((830, (ya + yt) / 2), "GAP", font=F(BLK, 30), fill=INK, anchor="mm")
    label(d, 90, 350, "ON AVERAGE", 40, WHITE, bg=INK)
    d.text((SAFE_R - 30, 370), "schematic", font=F(MONO, 20), fill=GREY_D, anchor="ra")

def sc_name(img, d, t):
    t0 = S("name") + .25
    k1 = back((t - S("name")) / .35)
    if k1 > .05: d.text((90, 420), "THE", font=F(BLK, int(110 * k1)), fill=INK)
    f = F(BLK, 200); split = ease_io((t - cue("name", "gap") + .1) / .6) * 150
    if t >= t0:
        wl = d.textlength("LIK", font=f)
        d.text((480 - split / 2 - wl, 650), "LIK", font=f, fill=INK, anchor="la")
        d.text((480 + split / 2, 650), "ING", font=f, fill=INK, anchor="la")
        if split > 24:
            d.rectangle([480 - split / 2 + 10, 690, 480 + split / 2 - 10, 840], fill=YEL)
    if t >= cue("name", "gap"):
        k = back((t - cue("name", "gap") - .3) / .35)
        if k > .05: d.text((480, 960), "GAP", font=F(BLK, int(200 * k)), fill=CORAL, anchor="mt")

def sc_why(img, d, t):
    t0 = S("why")
    pa = person(d, 250, 1020, 1.2, LAV); pb = person(d, 720, 1020, 1.2, CORAL, nod=math.sin(t * 6))
    # self-judgment fragments piling up around 'you'
    frags = [("too much?", 90, 430), ("weird.", 310, 510), ("ugh", 110, 580), ("boring?", 280, 360), ("why did I…", 60, 650)]
    for i, (w_, x, y) in enumerate(frags):
        k = back((t - t0 - .1 - i * .22) / .3)
        if k > .05:
            d.text((x, y), w_, font=F(BLK, int(40 * k)), fill=INK)
    # their signals travel left and fade before reaching you
    miss = cue("why", "miss")
    sig = [("smile", 0), ("nod", .7), ("laughs", 1.4)]
    for lab, off in sig:
        tt = (t - t0 - off) % 2.1
        u = tt / 2.1; x = 640 - u * 260; y = 600 + off * 80
        a = clamp(1 - u * 1.4) if t >= miss else clamp(1 - u * .4)
        if a > .05:
            col = mix(BG, TEAL, a)
            d.rounded_rectangle([x - 90, y - 32, x + 90, y + 32], radius=32, outline=col, width=6)
            d.text((x, y), lab, font=F(BLK, 34), fill=col, anchor="mm")
    if t >= miss:
        label(d, 520, 360, "MISSED", 40, WHITE, bg=CORAL)

def sc_months(img, d, t):
    t0 = S("months"); yb = 1000
    label(d, 90, 340, "NEW ROOMMATES", 40, WHITE, bg=INK)
    d.text((90, 400), "Yale first-years, 2016–17", font=F(BOLD, 26), fill=GREY_D)
    cols = [("SEP", .82, .56), ("OCT", .84, .6), ("DEC", .86, .63), ("FEB", .86, .66), ("MAY", .86, .84)]
    for i, (m, a, g) in enumerate(cols):
        x = 150 + i * 165; k = ease((t - t0 - .2 - i * .45) / .4)
        if k <= 0: continue
        d.rectangle([x - 52, yb - 420 * a * k, x - 4, yb], fill=LAV)
        d.rectangle([x + 4, yb - 420 * g * k, x + 52, yb], fill=CORAL)
        d.text((x, yb + 34), m, font=F(BLK, 30), fill=INK, anchor="mm")
        if i == 4 and k > .9:
            label(d, x, yb - 420 * a - 70, "closed", 26, INK, bg=YEL, anchor="ma")
    d.rectangle([90, 1080, 112, 1102], fill=LAV); d.text((122, 1091), "they liked you", font=F(BOLD, 22), fill=INK, anchor="lm")
    d.rectangle([360, 1080, 382, 1102], fill=CORAL); d.text((392, 1091), "you thought", font=F(BOLD, 22), fill=INK, anchor="lm")
    d.text((870, 1091), "schematic", font=F(MONO, 20), fill=GREY_D, anchor="rm")

def sc_point(img, d, t):
    t0 = S("point"); rv = cue("point", "they probably")
    pa, pb = player(d, t, t0, focus=0, reveal=1 if t >= rv else 0)
    if t >= rv:
        k = back((t - rv) / .35)
        if k > .05:
            cx, cy = 480, 500
            d.rectangle([cx - 330 * k, cy - 70 * k, cx + 330 * k, cy + 70 * k], fill=YEL)
            if k > .7: d.text((cx, cy), "THEY LIKED YOU.", font=F(BLK, 64), fill=INK, anchor="mm")

def end_card(d, t):
    k0 = S("end")
    for i, (w_, col) in enumerate((("NOT", INK), ("JUST", INK), ("YOU.", CORAL))):
        k = ease((t - k0 - i * .12) / .35)
        if k > 0: d.text((90 - (1 - k) * 80, 360 + i * 180), w_, font=F(BLK, 200), fill=mix(BG, col, k))
    if t > k0 + .9:
        d.text((90, 1000), "Sources", font=F(BLK, 26), fill=INK)
        for i, l in enumerate(("Boothby, Cooney, Sandstrom & Clark (2018),", "Psychological Science 29(11)")):
            d.text((90, 1038 + i * 32), l, font=F(MONO, 22), fill=GREY_D)
        label(d, 90, 1130, "@vascoda.soda", 30, WHITE, bg=INK)

# ---------------------------------------------------------------- chrome: header + marker subtitles
def header(d):
    label(d, 74, 224, "NOT JUST YOU · 06", 24, WHITE, bg=INK)
    d.text((SAFE_R, 236), "the liking gap", font=F(BOLD, 28), fill=INK, anchor="ra")

def subtitle(d, t, y0=1230):
    cur = TL.current(t) or "hook"   # hook text visible from frame 0
    if cur == "end": return
    b = TL.T[cur]
    if t > b["start"] + b["dur"] + .4: return
    f = F(BLK, 58); lines, curl = [], ""
    for w_ in b["text"].split():
        tst = (curl + " " + w_).strip()
        if d.textlength(tst, font=f) <= SAFE_R - 90: curl = tst
        else: lines.append(curl); curl = w_
    lines.append(curl)
    shown = (t - b["start"]) / b["dur"] * len(b["text"]); c = 0
    for li, line in enumerate(lines[:4]):
        x = 74
        for w_ in line.split(" "):
            wl = d.textlength(w_, font=f)
            now = c <= shown < c + len(w_) + 1
            if now: d.rectangle([x - 8, y0 + li * 72 + 6, x + wl + 8, y0 + li * 72 + 66], fill=YEL)
            d.text((x, y0 + li * 72), w_, font=f, fill=INK if c <= shown else GREY)
            x += d.textlength(w_ + " ", font=f); c += len(w_) + 1

SCENES = {"hook": sc_hook, "replay": sc_replay, "study": sc_study, "q": sc_q, "gap": sc_gap, "name": sc_name,
          "why": sc_why, "months": sc_months, "point": sc_point}

def draw(img, d, t):
    cur = "hook"
    for k in ORDER:
        if t >= S(k) - .05 and k != "hook": cur = k
    if cur == "end": end_card(d, t)
    else:
        SCENES[cur](img, d, t)
        # punch-in on every cut (and a harder one on frame 0 for the hook)
        st = 0.0 if cur == "hook" else S(cur) - .05
        z = 1 + (.06 if cur == "hook" else .045) * math.exp(-(t - st) * 7)
        if z > 1.002:
            cx, cy = 480, 680; l, tp = cx - cx / z, cy - cy / z
            img.paste(img.crop((int(l), int(tp), int(l + W / z), int(tp + H / z))).resize((W, H), Image.BILINEAR))
            d.rectangle([0, 0, W, 200], fill=BG)
    header(d)
    subtitle(d, t)

# ---------------------------------------------------------------- darker, minimal music bed (no hats, no plucks)
def rewind_sfx(amp=.22, dur=.55):
    t = tt_(dur); f = 2400 * np.exp(-t * 4.5) + 200
    return amp * (np.sin(2 * np.pi * np.cumsum(f) / SR) * .5 + bp(np.random.default_rng(5).standard_normal(len(t)), 800, 5000)) * np.sin(np.pi * t / dur) ** .5

def thud(amp=.45): return softkick(amp)

def snare(amp=.05):
    t = tt_(.18); return amp * bp(np.random.default_rng(9).standard_normal(len(t)), 900, 3500) * np.exp(-t * 22)

def build_audio(TL_, fx_cues, path, bpm=96, music_gaps=()):
    n = int((TL_.total + 1) * SR); vo = np.zeros(n); mus = np.zeros((n, 2)); fx = np.zeros((n, 2))
    def put(buf, x, t0, pan=0.):
        s = int(t0 * SR)
        if s < 0 or s >= n: return
        e = min(n, s + len(x)); x = x[:e - s]
        if buf.ndim == 1: buf[s:e] += x
        else: buf[s:e, 0] += x * (1 - max(0, pan)); buf[s:e, 1] += x * (1 + min(0, pan))
    for m in TL_.meta:
        a, sr = sf.read(os.path.join(TL_.dir, "vo", m["id"] + ".wav")); put(vo, resample_poly(a, SR, sr), TL_.T[m["id"]]["start"])
    beat = 60 / bpm; bar = beat * 4
    prog = [[220.0, 261.6, 329.6], [174.6, 220.0, 261.6], [261.6, 329.6, 392.0], [196.0, 246.9, 293.7]]  # Am F C G
    tb, i = 0.0, 0
    while tb < TL_.total - .3:
        ch = prog[i % 4]
        t_ = tt_(bar); env = np.minimum(1, t_ / .4) * np.exp(-t_ * .35)
        pad = sum(np.sin(2 * np.pi * f * t_ + j) for j, f in enumerate(ch)) * env * .018
        put(mus, lp(pad, 1800), tb, -.15); put(mus, lp(pad, 1800), tb + .01, .15)
        sub = .07 * np.sin(2 * np.pi * ch[0] / 2 * t_) * np.exp(-t_ * 1.2); put(mus, sub, tb)
        for b_ in range(4):
            if b_ in (0, 2): put(mus, softkick(.3), tb + b_ * beat)
            else: put(mus, snare(.035), tb + b_ * beat)
        tb += bar; i += 1
    for (t0, sig, pan) in fx_cues: put(fx, sig, t0, pan)
    env = np.convolve(np.abs(vo), np.ones(int(.12 * SR)) / int(.12 * SR), "same")
    duck = (1 - .55 * np.clip(env / (env.max() * .15 + 1e-9), 0, 1))[:, None]
    st = (vo[:, None] + mus * duck + fx)[: int(TL_.total * SR)]
    st /= np.abs(st).max() / .9
    fd = int(.5 * SR); st[-fd:] *= np.linspace(1, 0, fd)[:, None]
    with wave.open(path, "wb") as w_:
        w_.setnchannels(2); w_.setsampwidth(2); w_.setframerate(SR); w_.writeframes((st * 32767).astype(np.int16).tobytes())
cute.build_audio = build_audio

FX = [(0.0, rewind_sfx(), 0), (0.0, thud(.5), 0),
      (cue("hook", "here's") - .1, pop(.18), .3),
      *[(S(k) - .1, whoosh(.25, .12), 0) for k in ORDER[1:]],
      (cue("replay", "awkward"), thud(.3), -.2), (cue("replay", "weird"), thud(.3), .2),
      (cue("study", "two questions"), pop(.18), .2),
      (cue("gap", "more than"), thud(.4), 0),
      (S("name") + .25, thud(.5), 0), (cue("name", "gap"), whoosh(.5, .2), 0), (cue("name", "gap") + .3, thud(.55), 0),
      (cue("why", "miss"), pop(.15), .3),
      (cue("point", "they probably"), thud(.5), 0),
      (S("end"), thud(.5), 0)]

if __name__ == "__main__": cute.run(TL, draw, FX)
