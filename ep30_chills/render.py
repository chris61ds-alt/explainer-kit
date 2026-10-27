"""NOT JUST YOU – No. 30: music chills and dopamine (Salimpoor et al. 2011). Area: music."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .5, "peak": .5, "before": .6, "point": 1.0, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "peak", "before", "point", "end"]
DROP = cue("point", "wait")
EP = Episode(TL, 30, "CHILLS", order=ORDER,
             chapters={"hook": "GOOSEBUMPS", "study": "THE SCAN", "peak": "THE PEAK", "before": "THE BUILD-UP", "point": "THE DROP"},
             sources=("Salimpoor, Benovoy, Larcher, Dagher & Zatorre", "(2011), Nature Neuroscience 14"),
             music=dict(bpm=120, root=-3, prog="dream", kick="four", gaps=[(S("point") - .2, DROP + .1)]),
             cover=dict(words=["CHILLS."], kicker="What a song does to your brain."))

def bumps(d, h, t, k):
    rng = np.random.default_rng(1)
    for i in range(int(30 * k)):
        x = h[0] + 60 + rng.uniform(0, 90); y = h[1] + 120 + rng.uniform(0, 110)
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=SIG)

def intensity(u):        # song intensity: build-up to a peak at u = .62, then release
    return .2 + .7 * (u / .62) ** 2 if u < .62 else .9 - .5 * (u - .62) / .38

def song_curve(d, x0, y0, w, h, k, hl_before=0.0, hl_peak=0.0):
    pts = [(x0 + w * i / 100, y0 + h * (1 - intensity(i / 100))) for i in range(101)]
    n = max(2, int(101 * k))
    if hl_before > 0: d.polygon([(x0 + w * .3, y0 + h)] + pts[30:62] + [(x0 + w * .62, y0 + h)], fill=mix(BG, SIG_L, hl_before))
    d.line(pts[:n], fill=INK, width=6)
    if hl_peak > 0 and n > 62:
        px, py = pts[62]; r = 20 + 30 * hl_peak
        d.ellipse([px - r, py - r, px + r, py + r], outline=SIG, width=6); d.ellipse([px - 12, py - 12, px + 12, py + 12], fill=SIG)
    d.line([x0, y0 + h, x0 + w, y0 + h], fill=INK, width=3)
    return pts

def sc_hook(img, d, t):
    d.text((X0 - 6, 300), "CHILLS.", font=F(BLK, 220), fill=INK)
    h = picto(d, 380, FLOOR, 1.05, INK, pose=merge(OPEN, {"tilt": -6}))
    headphones(d, h, 1.05)
    bumps(d, h, t, clamp((t - .5) / 1.5))
    for i in range(3): note_icon(d, 640 + i * 80, 700 - 40 * math.sin(t * 3 + i), .7, SIG if i == 1 else INK)
    if t >= cue("hook", "wild"): note(d, h[0] + 110, h[1] + 170, 860, 1000, "goosebumps", (t - cue("hook", "wild")) / .35, SIG, anchor="ra", size=28)
    fig(d, "fig. 1 — the moment a song gets you")

def sc_study(img, d, t):
    t0 = S("study")
    d.text((X0, 320), "THE SCAN", font=F(BLK, 130), fill=INK)
    cx, cy = 480, 760
    d.ellipse([cx - 260, cy - 260, cx + 260, cy + 260], outline=INK, width=30); d.ellipse([cx - 180, cy - 180, cx + 180, cy + 180], outline=RULE, width=4)
    h = picto(d, cx, cy + 150, .7, INK, pose=IDLE); headphones(d, h, .7)
    a = t * 2; d.arc([cx - 260, cy - 260, cx + 260, cy + 260], math.degrees(a), math.degrees(a) + 40, fill=SIG, width=30)
    fig(d, "PET + fMRI · 8 listeners, their own chill-inducing music")

def sc_peak(img, d, t):
    t0 = S("peak"); dp = cue("peak", "dopamine")
    d.text((X0, 320), "AT THE PEAK", font=F(BLK, 120), fill=INK)
    pts = song_curve(d, X0, 520, X1 - X0, 420, clamp((t - t0) / 1.4), hl_peak=ease((t - dp) / .4) if t >= dp else 0)
    if t >= dp:
        box_label(d, X0 + (X1 - X0) * .62, 470, "DOPAMINE", 34, WHITE, SIG, anchor="ma")
        note(d, pts[62][0], pts[62][1], 860, 1010, "nucleus accumbens", (t - dp - .3) / .4, INK, anchor="ra", size=26)
    d.text((X0, 980), "song intensity", font=F(COND, 26), fill=MID)
    fig(d, "fig. 2 — the reward chemical, also released for food")

def sc_before(img, d, t):
    t0 = S("before"); bp_ = cue("before", "before the peak")
    d.text((X0, 320), "BEFORE IT", font=F(BLK, 130), fill=SIG)
    pts = song_curve(d, X0, 520, X1 - X0, 420, 1, hl_before=ease((t - bp_ + .2) / .5), hl_peak=1)
    if t >= bp_ - .2:
        rng = np.random.default_rng(5)
        for i in range(14):
            u = (t * .4 + i / 14) % 1; x = lerp(X0 + (X1 - X0) * .3, X0 + (X1 - X0) * .6, u); y = 940 - 60 * math.sin(u * math.pi) - rng.uniform(0, 80)
            d.ellipse([x - 8, y - 8, x + 8, y + 8], fill=SIG)
        note(d, X0 + (X1 - X0) * .45, 850, X0 + 20, 1060, "caudate · anticipation", (t - bp_) / .4, SIG, size=26)
    d.text((X0, 980), "song intensity", font=F(COND, 26), fill=MID)

def synth(d, x0, y0, w, t, knob):
    d.rectangle([x0, y0, x0 + w, y0 + 260], fill=INK)
    for i in range(3):
        cx = x0 + 70 + i * 110; d.ellipse([cx - 34, y0 + 30, cx + 34, y0 + 98], fill=MID)
        a = math.radians(-220 + 260 * (knob if i == 0 else .4)); d.line([cx, y0 + 64, cx + math.cos(a) * 30, y0 + 64 + math.sin(a) * 30], fill=SIG if i == 0 else WHITE, width=6)
    d.text((x0 + 70, y0 + 118), "CUTOFF", font=F(COND, 20), fill=WHITE, anchor="ma")
    for i in range(14):
        kx = x0 + 10 + i * (w - 20) / 14; d.rectangle([kx, y0 + 150, kx + (w - 20) / 14 - 4, y0 + 250], fill=WHITE)
    for i in (0, 1, 3, 4, 5, 7, 8, 10, 11, 12):
        kx = x0 + 10 + (i + .7) * (w - 20) / 14; d.rectangle([kx, y0 + 150, kx + (w - 20) / 14 * .6, y0 + 210], fill=INK)

def sc_point(img, d, t):
    t0 = S("point")
    if t < DROP: words_in(d, t, [("THE", t0, 300, 150, INK), ("BUILD-UP…", t0 + .2, 450, 150, INK)])
    else: words_in(d, t, [("WAIT", DROP, 300, 190, SIG), ("FOR IT.", DROP + .2, 500, 150, INK)])
    knob = clamp((t - t0) / max(.5, DROP - t0))
    synth(d, X0, 760, X1 - X0, t, knob if t < DROP else 1)
    if t >= DROP:
        for i in range(10):
            a = i / 10 * 2 * math.pi; r = 60 + 300 * ease((t - DROP) / .5)
            d.line([480 + math.cos(a) * (r - 40), 650 + math.sin(a) * (r - 40) * .4, 480 + math.cos(a) * r, 650 + math.sin(a) * r * .4], fill=SIG, width=6)
    fig(d, "fig. 3 — your brain pays you to wait")

EP.scenes = {"hook": sc_hook, "study": sc_study, "peak": sc_peak, "before": sc_before, "point": sc_point}
def sweep(dur, amp=.14):
    t = tt_(dur); f = 300 * (12 ** (t / dur)); return amp * np.sin(2 * np.pi * np.cumsum(f) / SR) * (t / dur) ** 1.5
FX = [(0.0, thud(.5), 0), (cue("hook", "wild"), riser(.5, .06), .3), *EP.cut_fx(),
      (S("study"), whoosh(1.2, .06), 0), (cue("peak", "dopamine"), thud(.55), 0), (cue("peak", "dopamine"), riser(.3, .08), .2),
      (cue("before", "before the peak") - .2, riser(1.0, .08), -.2), (S("point"), sweep(DROP - S("point") + .05, .12), 0),
      (S("point"), riser(DROP - S("point"), .1), 0), (DROP, thud(.8), 0), (DROP + .02, softkick(.5), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
