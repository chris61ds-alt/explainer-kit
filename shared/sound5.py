"""Audio v5 (since 01.11.2026 for new episodes): music=dict(audio="v5") in render.py, or NJY_AUDIO=v5
A. dramaturgy  – the bed follows the script: sparse intro (guess) → build with an opening filter → full drop on every
                 reveal → thinned-out outro; fills before every cut, a variation every 4th bar, pumping on the beat
B. sonification – every on-screen counter gets a rising note run that lands on a bell
C. sound kit   – "afterdark" (808 bass with slides, claps, 16th hats with rolls, plucked arp with echo); more kits to follow
Everything is synthesised (no samples)."""
import math
import numpy as np
from scipy.signal import butter, lfilter
from cute import SR, tt_, bp, lp

_R = np.random.default_rng(23)
GAIN = .3                                # bed sits ≈ 10 dB under the voice, drops ≈ 5 dB louder than the build
def _noise(n, seed): return np.random.default_rng(seed).standard_normal(n)
def hp(x, fc): b, a = butter(2, fc / (SR / 2), "high"); return lfilter(b, a, x)

# ---------------------------------------------------------------- instruments
def k808(f0, dur=.55, amp=.42, f1=None, glide=.12, drive=2.2):
    """808: sine with a fast pitch drop at the attack, saturated; f1 = slide target"""
    t = tt_(dur); f = f0 * (1 + 1.6 * np.exp(-t * 60))
    if f1: f = f + (f1 - f0) * np.clip((t - (dur - glide)) / glide, 0, 1)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.2) * np.minimum(1, t / .002)
    click = _noise(len(t), 4) * np.exp(-t * 900) * .3
    return amp * np.tanh((x + click) * drive) / np.tanh(drive)

def clap(amp=.10):
    t = tt_(.22); n = _noise(len(t), 7); env = np.zeros(len(t))
    for d in (0, .009, .018): env += np.exp(-np.clip(t - d, 0, None) * 140) * (t >= d)
    env += .45 * np.exp(-t * 18)
    return amp * bp(n, 950, 3600) * env

def chat(amp=.02, open_=False):
    t = tt_(.32 if open_ else .05); return amp * bp(_noise(len(t), 11), 6500, 15500) * np.exp(-t * (14 if open_ else 95))

def pluck(f, amp=.035, dur=.35):
    t = tt_(dur); x = np.sin(2 * np.pi * f * t) + .45 * np.sin(4 * np.pi * f * t + .3) + .2 * np.sin(6 * np.pi * f * t)
    return amp * lp(x * np.exp(-t * 13), 4200)

def bell(f, amp=.06, dur=1.1):
    t = tt_(dur); x = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * d) for r, a, d in ((1, 1, 3), (2.76, .5, 5), (5.4, .25, 8)))
    return amp * x * np.minimum(1, t / .003)

def pad(ch, dur, cutoff=1300, amp=.016):
    """dark detuned pad: two slightly detuned partials per chord tone + sub octave"""
    t = tt_(dur); env = np.minimum(1, t / .35)
    x = 0
    for j, f in enumerate(ch):
        for dt in (-.0035, .0035): x = x + np.sin(2 * np.pi * f * (1 + dt) * t + j)
    x = x + .8 * np.sin(2 * np.pi * ch[0] / 2 * t)
    return amp * lp(x * env, cutoff)

def delay(x, d, fb=.35, n=3):
    out = x.copy(); s = int(d * SR)
    for i in range(1, n + 1):
        if s * i >= len(x): break
        out[s * i:] += x[:len(x) - s * i] * fb ** i
    return out

# ---------------------------------------------------------------- arrangement
def energy_map(total, intro_end, reveals, cuts, outro):
    """energy per time: 0 intro · 1 groove-in · 2 build/groove · 3 drop (2 bars after a reveal) · 1 outro"""
    def E(t, bar):
        if t < intro_end: return 0
        if outro and t >= outro: return 1
        for r in reveals:
            if r - .01 <= t < r + 2 * bar: return 3
        if t < intro_end + 2 * bar: return 1
        return 2
    return E

def music(TL_, M, n, bpm, prog, kit="afterdark"):
    """returns (stereo music bed, kick times) following the episode's structure in M"""
    beat = 60 / bpm; bar = 4 * beat; s16 = beat / 4
    total = TL_.total; mus = np.zeros((n, 2))
    reveals = sorted(M.get("reveals", ())); cuts = sorted(M.get("cuts", ())); intro_end = M.get("intro_end", 0.0)
    outro = M.get("outro"); E = energy_map(total, intro_end, reveals, cuts, outro)
    if not reveals and cuts: reveals = [cuts[len(cuts) // 2]]                     # no tease: drop on the middle cut
    def put(x, t0, pan=0.):
        s = int(t0 * SR)
        if s < 0 or s >= n: return
        e = min(n, s + len(x)); x = x[:e - s]; mus[s:e, 0] += x * (1 - max(0, pan)); mus[s:e, 1] += x * (1 + min(0, pan))
    kicks = []
    # bars are anchored so a bar starts exactly at the first reveal (the drop lands on "one")
    anchor = reveals[0] if reveals else intro_end
    tb = anchor - math.ceil(anchor / bar) * bar
    i = 0; arp_bus = np.zeros(n)
    while tb < total - .2:
        ch = prog[i % len(prog)]; nxt = prog[(i + 1) % len(prog)]
        e_bar = E(max(tb, 0) + .01, bar)
        root = ch[0]
        while root > 70: root /= 2
        nroot = nxt[0]
        while nroot > 70: nroot /= 2
        # pad (always) – darker in the intro
        p = pad(ch, bar + .3, cutoff=600 if e_bar == 0 else 1400)
        put(p, tb, -.2); put(p, tb + .012, .2)
        last_bar_of_4 = (i % 4) == 3
        for st in range(16):
            t = tb + st * s16
            if t < 0 or t >= total - .15: continue
            e = E(t, bar)
            cut_next = any(0 <= c - t < beat for c in cuts)                       # last beat before a scene cut → fill
            gap = any(a <= t < b for a, b in M.get("gaps", ()))
            if gap: continue
            if e == 0:
                if st % 4 == 0: put(k808(root, .35, .16, drive=1.2), t); kicks.append(t)      # heartbeat pulse
                continue
            # 808 / kick
            pat = {1: (0, 10), 2: (0, 6, 10), 3: (0, 3, 6, 10, 14)}[e]
            if st in pat and not (cut_next and st >= 12):
                slide = nroot if (e == 3 and st == 14) else None
                put(k808(root, .5 if st != 14 else .35, (.42 if st == 0 else .34) * (1 if e == 3 else .55), f1=slide), t); kicks.append(t)
            # clap on 2 and 4
            if e >= 2 and st in (4, 12): put(clap(.11 if e == 3 else .055), t, .05)
            # hats
            if e == 1 and st % 2 == 0: put(chat(.012), t, .25)
            if e >= 2:
                if st % 2 == 0 or e == 3: put(chat(.018 if st % 4 == 2 else .011), t, (.3 if st % 2 else -.15))
                if last_bar_of_4 and st == 14: put(chat(.02, open_=True), t, .3)                 # variation: open hat
            if e == 3 and last_bar_of_4 and st >= 12:                                             # triplet roll
                for k in range(3): put(chat(.012 + .004 * k), t + k * s16 / 3, -.3)
            # fill before a cut: 32nd hat roll, crescendo
            if cut_next and st >= 12 and e >= 1:
                for k in range(2): put(chat(.008 + .006 * (st - 12) + .003 * k), t + k * s16 / 2, .2)
            # arp (drop only), octave up, echo on the dotted 8th
            if e == 3 and st % 2 == 0:
                f = ch[[0, 1, 2, 1, 0, 2, 1, 2][(st // 2) % 8]] * 2
                x = pluck(f); s = int(t * SR); arp_bus[s:s + len(x)] += x[:max(0, min(len(x), n - s))]
        tb += bar; i += 1
    arp = delay(arp_bus, 3 * s16, .38, 4)
    mus[:, 0] += arp * .9; mus[:, 1] += np.roll(arp, int(.011 * SR))
    # filter opening: muffled in the intro, opens through the build, full from the first drop
    w = np.ones(n); tt = np.arange(n) / SR
    first = reveals[0] if reveals else intro_end + 4 * bar
    w[tt < intro_end] = 0.0
    sel = (tt >= intro_end) & (tt < first); w[sel] = .25 + .75 * ((tt[sel] - intro_end) / max(.1, first - intro_end)) ** 1.5
    if outro: w[tt >= outro] = .55
    muff = np.stack([lp(mus[:, 0], 650), lp(mus[:, 1], 650)], 1)
    mus = mus * w[:, None] + muff * (1 - w[:, None])
    # pump: pad & co. duck on every kick
    pump = np.ones(n)
    for k in kicks:
        s = int(k * SR); L = int(.22 * SR); seg = pump[s:s + L]
        pump[s:s + L] = np.minimum(seg, 1 - .35 * np.exp(-np.arange(len(seg)) / SR * 14))
    mus *= pump[:, None] ** .5
    return mus * GAIN

def counter_runs(counters, root_hz):
    """B: rising pentatonic run under each on-screen counter, landing on a bell"""
    out = []; pent = [0, 2, 4, 7, 9]
    for (t0, dur, _to) in counters:
        steps = max(4, int(dur / .055))
        for k in range(steps):
            semi = pent[k % 5] + 12 * (k // 5)
            out.append((t0 + dur * k / steps, pluck(root_hz * 2 * 2 ** (semi / 12), .018 + .014 * k / steps, .18), (k % 2 - .5) * .4))
        out.append((t0 + dur, bell(root_hz * 4, .05), 0))
    return out
