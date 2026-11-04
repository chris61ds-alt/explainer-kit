"""Signature transition sound (04.11.2026, Chris' pick 'H'): reverse swell + deep body → snap with a low punch,
panned right → left with the slide, own reverb tail. Stereo array; place it so the snap lands as the new scene settles."""
import numpy as np
from cute import SR, bp

_CACHE = {}
SNAP_AT = .38                      # seconds into the sample where the snap hits

def swoosh_h(rms=.04, verb=True, seed=4):
    key = (rms, verb, seed)
    if key in _CACHE: return _CACHE[key]
    g = np.random.default_rng(seed); t_ = lambda d: np.arange(int(d * SR)) / SR
    n = int(SNAP_AT * SR); u = np.linspace(0, 1, n)
    sw = bp(g.standard_normal(n), 900, 6000) * u ** 3
    body = np.sin(2 * np.pi * np.cumsum(60 + 90 * u) / SR) * u ** 2 * .7
    snap = np.zeros(int(.12 * SR)); snap[:60] = 1; snap = bp(snap, 1200, 8000) * 5 * np.exp(-np.arange(len(snap)) / 400)
    snap = snap + 1.0 * np.sin(2 * np.pi * 60 * t_(.12)) * np.exp(-t_(.12) * 28)
    m = np.concatenate([sw + body, snap])
    p = np.concatenate([.7 - 1.4 * u, np.full(len(snap), -.7)]); a = (p + 1) * np.pi / 4
    st = np.stack([m * np.cos(a), m * np.sin(a)], 1)
    st *= rms / (np.sqrt(np.mean(st ** 2)) + 1e-9)
    if verb:                                           # its own plate tail (on top of the mix's general fx reverb)
        from swiss import fx_reverb
        st = np.vstack([st, np.zeros((int(1.4 * SR), 2))]); st = st + fx_reverb(st, 1.3, .5, pre=.025, seed=9)
    _CACHE[key] = st
    return st
