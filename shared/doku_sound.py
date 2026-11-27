"""Doku sound (26.11.2026, after the Dyatlov reference reel): a dark, CONTINUOUS cinematic bed – never silence – and
small foley sounds for things that appear on screen (paper, pin, typewriter, stamp, camera shutter, string).

    music=dict(audio="doku", root=..., bpm=70)       # in the episode's EP = DokuEpisode(...)
    from doku_sound import paper, pin, typewriter, stamp, shutter, string_pull, riser, hit

The bed: a low drone (root, fifth), a slow minor pad that changes every two bars, a soft heartbeat pulse that gets
denser towards reveals, a noise riser into every reveal and a deep hit on it. Ducking under the voice happens in
cute.build_audio as for every episode. Levels: the bed sits ~10 dB under the voice."""
import math
import numpy as np
from scipy.signal import butter, lfilter
from cute import SR
GAIN = .55


def lp(x, fc, order=2):
    b, a = butter(order, min(.99, fc / (SR / 2)), "low"); return lfilter(b, a, x)

def hp(x, fc, order=2):
    b, a = butter(order, min(.99, fc / (SR / 2)), "high"); return lfilter(b, a, x)

def bp(x, lo, hi):
    return lp(hp(x, lo), hi)

def _n(n, seed): return np.random.default_rng(seed).standard_normal(n)

def env(n, a=.005, r=.08):
    t = np.arange(n) / SR; return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / max(r, 1e-4))


# ---- foley --------------------------------------------------------------------------------------------------------
def paper(amp=.09, dur=.35, seed=1):
    """a photo/card sliding onto the board: filtered noise swish"""
    n = int(dur * SR); x = bp(_n(n, seed), 900, 6000) * np.sin(np.linspace(0, math.pi, n)) ** 1.5
    return x / (np.abs(x).max() + 1e-9) * amp

def pin(amp=.12, seed=2):
    """a push pin going into cork: short click + tiny low thump"""
    n = int(.09 * SR); t = np.arange(n) / SR
    click = hp(_n(n, seed), 2500) * np.exp(-t * 180)
    thump = np.sin(2 * np.pi * 140 * t) * np.exp(-t * 40) * .6
    x = click + thump; return x / (np.abs(x).max() + 1e-9) * amp

def typewriter(n_keys=6, amp=.08, seed=3, rate=.07):
    """a burst of typewriter keys (+ a ding is not included – too cute)"""
    g = np.random.default_rng(seed); out = np.zeros(int((n_keys * rate + .15) * SR))
    for k in range(n_keys):
        m = int(.05 * SR); t = np.arange(m) / SR
        key = bp(g.standard_normal(m), 1200, 7000) * np.exp(-t * 90) + np.sin(2 * np.pi * (180 + 40 * g.random()) * t) * np.exp(-t * 60) * .4
        s = int((k * rate + g.random() * .02) * SR); out[s:s + m] += key * (.7 + .3 * g.random())
    return out / (np.abs(out).max() + 1e-9) * amp

def stamp(amp=.22, seed=4):
    """rubber stamp hitting paper: low thud + paper slap"""
    n = int(.25 * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * 70 * t) * np.exp(-t * 18) + bp(_n(n, seed), 400, 3000) * np.exp(-t * 60) * .7
    return x / (np.abs(x).max() + 1e-9) * amp

def shutter(amp=.1, seed=5):
    """old camera shutter: two clicks"""
    n = int(.14 * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for d in (0, .07):
        s = int(d * SR); m = n - s; x[s:] += hp(_n(m, seed + int(d * 100)), 2000) * np.exp(-np.arange(m) / SR * 150)
    return x / (np.abs(x).max() + 1e-9) * amp

def string_pull(amp=.06, dur=.4, seed=6):
    """a red string pulled taut: a short rising zip"""
    n = int(dur * SR); t = np.arange(n) / SR
    f = 300 + 900 * t / dur; x = np.sin(2 * np.pi * np.cumsum(f) / SR) * bp(_n(n, seed), 500, 4000) * .5 + bp(_n(n, seed + 1), 2000, 8000) * .3
    x *= np.sin(np.linspace(0, math.pi, n)); return x / (np.abs(x).max() + 1e-9) * amp

def riser(dur=1.6, amp=.12, seed=7):
    """noise riser into a reveal (filter opens, gets louder)"""
    n = int(dur * SR); x = _n(n, seed); out = np.zeros(n); seg = n // 16
    for i in range(16):
        a, b = i * seg, (i + 1) * seg if i < 15 else n
        out[a:b] = bp(x[a:b], 300 + 250 * i, 1500 + 600 * i)
    out *= np.linspace(0, 1, n) ** 2.2; return out / (np.abs(out).max() + 1e-9) * amp

def hit(amp=.35, seed=8):
    """deep cinematic hit on a reveal"""
    n = int(1.8 * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * (48 + 30 * np.exp(-t * 6)) * t) * np.exp(-t * 2.2) + lp(_n(n, seed), 900) * np.exp(-t * 8) * .5
    return x / (np.abs(x).max() + 1e-9) * amp


# ---- the bed ------------------------------------------------------------------------------------------------------
def _saw(f, n, detune=0.0):
    t = np.arange(n) / SR; ph = (f * (1 + detune)) * t; return 2 * (ph - np.floor(ph + .5))

def bed(TL_, M, n, prog):
    """continuous bed for the whole episode (stereo). M: reveals, root, bpm"""
    total = TL_.total; bpm = M.get("bpm", 70); beat = 60 / bpm; bar = 4 * beat
    root = 55.0 * 2 ** (M.get("root", 0) / 12)
    while root > 70: root /= 2
    t = np.arange(n) / SR; mus = np.zeros((n, 2))
    # drone: root + fifth, slow breathing
    breath = .75 + .25 * np.sin(2 * np.pi * t / (bar * 2))
    drone = (np.sin(2 * np.pi * root * t) * .5 + lp(_saw(root, n, .002) + _saw(root * 1.5, n, -.003) * .6, 260) * .35) * breath
    mus += np.stack([drone, np.roll(drone, int(.013 * SR))], 1) * .5
    # pad: chord every 2 bars, dark, crossfaded
    seg = int(2 * bar * SR); i = 0
    for s in range(0, n, seg):
        ch = prog[i % len(prog)]; m = min(n - s, seg + int(.6 * SR)); x = np.zeros(m)
        for k, f in enumerate(ch):
            while f > 440: f /= 2
            x += _saw(f, m, .004 * (k - 1)) + _saw(f, m, -.004 * (k - 1))
        x = lp(x, 900) * .045; w = np.minimum(1, np.arange(m) / (.6 * SR)) * np.minimum(1, (m - np.arange(m)) / (.6 * SR))
        mus[s:s + m, 0] += x * w; mus[s:s + m, 1] += np.roll(x, 300) * w; i += 1
    # heartbeat pulse (two soft hits per bar), denser in the 4 s before a reveal
    reveals = sorted(M.get("reveals", ()))
    def put(x, t0, pan=0.):
        s = int(t0 * SR)
        if s < 0 or s >= n: return
        e = min(n, s + len(x)); x = x[:e - s]; mus[s:e, 0] += x * (1 - max(0, pan)); mus[s:e, 1] += x * (1 + min(0, pan))
    def thump(a):
        m = int(.3 * SR); tt = np.arange(m) / SR; return np.sin(2 * np.pi * (root * 1.0 + 25 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 14) * a
    tb = 0.0
    while tb < total - .3:
        near = any(0 <= r - tb < 4 for r in reveals)
        put(thump(.20), tb); put(thump(.13), tb + beat * .45)
        if near: put(thump(.16), tb + 2 * beat); put(thump(.11), tb + 2 * beat + beat * .45)
        tb += bar if not near else bar / 1
    # riser + hit into every reveal
    for r in reveals:
        x = riser(1.6, .10); put(x, r - 1.6); put(hit(.30), r)
    # gentle high air (tension) all the time
    air = bp(_n(n, 11), 3000, 9000) * .006 * breath
    mus[:, 0] += air; mus[:, 1] += np.roll(air, 900)
    # fade in/out
    f = np.minimum(1, t / .4) * np.minimum(1, np.maximum(0, total + .2 - t) / 1.0)
    return mus * f[:, None] * GAIN
