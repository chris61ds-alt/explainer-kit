"""NOT JUST YOU – No. 153: all of humanity on one island ('pour test' riddle, 25.11.2026; Chris picked idea 3 of the sand format).
8.2 billion people x 1 m2 = 8,200 km2 < Crete 8,336 km2 -> everyone fits, just barely. Earth's land ~149 M km2 = ~18,000x.
Riddle structure like No. 152 (solution in the same video, rule 17), dark look. ONE continuous picture: the world map on top
is made of sand (= people); Crete appears big at the bottom; the sand pours from every continent into Crete and fills it
from the bottom up (98 %). Then a tiny orange dot marks Crete on the map. Payoff (rule 15): full Crete + the map stay."""
import os, sys, math, json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from stand import stamp_box
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .4, "rules": .4, "lock": .7, "gut": .5, "reveal": .5, "pour": .6, "scale": .5, "why": .1})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "rules", "lock", "gut", "reveal", "pour", "scale", "why", "end"]
EP = ThreadEpisode(TL, 153, "HUMANITY ON AN ISLAND", order=ORDER, dark=True, label="RIDDLE · 8.2 BN PEOPLE · 1 M² EACH",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("US Census Bureau, International Database 2026 ·", "Crete 8,336 km² · Natural Earth outlines"),
                   music=dict(bpm=96, root=2, prog="major", kick="four", audio="v5"),
                   cover=dict(words=["1 M² FOR EVERY", "HUMAN. HOW MUCH", "LAND IS THAT?"], kicker="Lock in your answer."))

SAND = (226, 186, 120)
FEAT = [f for f in json.load(open(os.path.join(HERE, "countries.geojson")))["features"] if f["properties"]["NAME"] != "Antarctica"]
def rings(name=None):
    for f in FEAT:
        if name and f["properties"]["NAME"] != name: continue
        g = f["geometry"]; parts = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for p in parts: yield f["properties"]["NAME"], p[0]

# world map (top), equirectangular
WX0, WS, WLAT = 115, 2.35, 80
def wproj(lo, la): return WX0 + (lo + 180) * WS, 500 + (WLAT - la) * WS
# Crete (bottom), big, lon scaled by cos(lat)
CLON, CLAT, CS = 24.9, 35.25, 330
def cproj(lo, la): return 540 + (lo - CLON) * CS * math.cos(math.radians(35.3)), 1000 - (la - CLAT) * CS
def chaikin(pts, n=3):
    for _ in range(n):
        q = []
        for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]): q += [(.75 * x0 + .25 * x1, .75 * y0 + .25 * y1), (.25 * x0 + .75 * x1, .25 * y0 + .75 * y1)]
        pts = q
    return pts
CRETE = json.load(open(os.path.join(HERE, "crete.json")))               # Crete from Natural Earth 1:50m (69 points)
CRETE = chaikin([cproj(lo, la) for lo, la in CRETE], 1)
WORLD = [[wproj(lo, la) for lo, la in r] for n, r in rings()]
AUS = [[wproj(lo, la) for lo, la in r] for n, r in rings("Australia")]
CRETE_ON_MAP = wproj(24.9, 35.25)

def sample(polys, n, seed):
    L = Image.new("L", (1080, 1920), 0); g = ImageDraw.Draw(L)
    for p in polys:
        if len(p) > 2: g.polygon(p, fill=255)
    ys, xs = np.nonzero(np.asarray(L)); R = np.random.RandomState(seed); idx = R.choice(len(xs), n, replace=len(xs) < n)
    return np.stack([xs[idx] + R.uniform(-.5, .5, n), ys[idx] + R.uniform(-.5, .5, n)], 1)
N = 2600
SRC = sample(WORLD, N, 1)
DST = sample([CRETE], int(N / .98), 2)                                      # 98 % of Crete gets filled
DST = DST[np.argsort(-DST[:, 1] + np.random.RandomState(3).uniform(0, 30, len(DST)))][:N]   # bottom first, like a pile
ORDER_P = np.random.RandomState(4).permutation(N)                           # which grain leaves the map when

T_MAP = .1
T_LOCK = S("lock"); T_321 = [cue("lock", "Three") - .05, cue("lock", "Two") - .05, cue("lock", "One") - .05]
T_GUT = S("gut") + .05
T_CRETE = cue("reveal", "Crete") - .15; T_KM = cue("reveal", "eight thousand") - .1
T_P0, T_P1 = S("pour") - .2, E("pour") + .5
T_DOT = S("scale") + .1
# 25.11.2026 (Chris: "for a long time nothing happens"): one person on 1 m², the squares multiply, rolling counters
T_ME = .15; T_SHRINK = cue("rules", "Eight point two") - .1
T_BN = cue("rules", "Eight point two") - .1; T_TILE = cue("rules", "One square") - .1; T_TOFF = S("lock") - .1

def person_square(d, x, y, s, k=1.0, labels=False):
    col = mix(BG, INK, k)
    from stand import dashed
    h = s / 2
    for a, b in (((x - h, y - h), (x + h, y - h)), ((x + h, y - h), (x + h, y + h)), ((x + h, y + h), (x - h, y + h)), ((x - h, y + h), (x - h, y - h))):
        if s > 80: dashed(d, a, b, col, w=4, dash=18, gap=12)
        else: d.line([a, b], fill=col, width=2)
    r = s * .09; d.ellipse([x - r, y - s * .32 - r, x + r, y - s * .32 + r], fill=mix(BG, SAND, k))          # head
    d.rounded_rectangle([x - s * .14, y - s * .2, x + s * .14, y + s * .3], radius=max(2, int(s * .06)), fill=mix(BG, SAND, k))
    if labels and s > 150:
        d.text((x, y + h + 30), "1 m", font=F(MONO, 30), fill=col, anchor="mm")
        d.text((x + h + 20, y), "1 m", font=F(MONO, 30), fill=col, anchor="lm")

TILE = 40
TILES = sorted([(540 + (c - 12) * TILE, 1030 + (r - 3) * TILE) for c in range(25) for r in range(7)], key=lambda p: (p[0] - 540) ** 2 + (p[1] - 1030) ** 2)
def me_and_tiles(d, t):
    if t < T_ME or t >= T_TOFF + .4: return
    fade = 1 - clamp((t - T_TOFF) / .4)
    if t < T_TILE:
        k = spring(clamp((t - T_ME) / .5)); sh = ease_io(clamp((t - T_SHRINK) / .6))
        s = 300 * k * (1 - sh) + (TILE - 6) * sh
        if sh > 0: s = s                                                     # (the square shrinks into the first tile)
        person_square(d, 540, 960, max(1, s), fade, labels=sh < .2)
    else:
        n = int(len(TILES) * ease_io(clamp((t - T_TILE) / 1.3)))
        for (x, y) in TILES[:max(1, n)]: person_square(d, x, y - 70, TILE - 6, fade)

def grains(d, t):
    u = clamp((t - T_P0) / (T_P1 - T_P0)) if t >= T_P0 else 0
    show = clamp((t - T_MAP) / .8)
    for k in range(N):
        i = ORDER_P[k]; sx, sy = SRC[i]; tx, ty = DST[k]
        st = T_P0 + (T_P1 - T_P0 - .6) * k / N
        if t < T_MAP + .8 * (sx - WX0) / 850 * show + .01 and t < T_P0: continue           # map appears west -> east
        if t < st:
            x, y = sx, sy
        else:
            v = ease_io(clamp((t - st) / .6)); cx, cy = (sx + tx) / 2, min(sy, ty) - 120
            x = (1 - v) ** 2 * sx + 2 * (1 - v) * v * cx + v * v * tx; y = (1 - v) ** 2 * sy + 2 * (1 - v) * v * cy + v * v * ty
        d.rectangle([x - 1.6, y - 1.6, x + 1.6, y + 1.6], fill=SAND)
    return u

def crete(d, t):
    if t < T_CRETE: return
    k = ease(clamp((t - T_CRETE) / .5))
    d.polygon(CRETE, fill=mix(BG, MID, .25 * k), outline=mix(BG, INK, k))
    d.line(CRETE + CRETE[:1], fill=mix(BG, INK, k), width=4)
    if k > .6:
        d.text((540, 1170), "CRETE · 8,336 km²", font=F(MONO, 28), fill=INK, anchor="mm")

def countdown(d, t):
    if not (T_LOCK <= t < S("gut")): return
    d.rounded_rectangle([290, 640, 790, 1040], radius=40, fill=BG)
    d.text((540, 690), "LOCK IN YOUR ANSWER", font=F(BLK, 38), fill=INK, anchor="mm")
    i = sum(1 for x in T_321 if t >= x)
    ring = clamp((t - T_321[0]) / (T_321[2] + .7 - T_321[0])) if t >= T_321[0] else 0
    d.ellipse([420, 750, 660, 990], outline=mix(BG, MID, .6), width=12)
    if ring > 0: d.arc([420, 750, 660, 990], -90, -90 + 360 * (1 - ring), fill=SIG, width=12)
    d.text((540, 870), ["?", "3", "2", "1"][i], font=F(BLK, 130), fill=INK, anchor="mm")

def head(d, line, label=None, val=None, hot=False):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    if label:
        d.text((X0, 400), label, font=F(MONO, 30), fill=MID)
        d.text((X0 + d.textlength(label, font=F(MONO, 30)) + 24, 388), val, font=F(BLK, 56), fill=SIG if hot else INK)

def sc(img, d, t):
    cur = EP.current(t)
    for p in WORLD:                                                         # the land stays as a faint ground (the map empties)
        if len(p) > 2: d.polygon(p, fill=mix(BG, MID, .18))
    crete(d, t); u = grains(d, t); me_and_tiles(d, t)
    if t >= T_P1:                                                            # payoff: the people on Crete twinkle
        for j in range(0, N, 9):
            if math.sin(t * 7 + j * 1.7) > .85:
                x, y = DST[j]; d.rectangle([x - 2.5, y - 2.5, x + 2.5, y + 2.5], fill=(255, 236, 200))
    if cur == "gut":                                                         # 'a whole continent?' -> Australia lights up, pulsing
        pk = .6 + .4 * math.sin((t - T_GUT) * 9)
        for p in AUS:
            if len(p) > 2: d.polygon(p, fill=mix(BG, SIG, pk))
        ax, ay = wproj(134, -25); d.text((ax, ay + 70), "AUSTRALIA?", font=F(BLK, 34), fill=SIG, anchor="mm")
    if cur in ("scale", "why", "end") and t >= T_DOT:                       # Crete on the world map: one tiny dot
        k = spring(clamp((t - T_DOT) / .5)); x, y = CRETE_ON_MAP
        d.ellipse([x - 7 * k, y - 7 * k, x + 7 * k, y + 7 * k], fill=SIG)
        rr = 26 + 6 * math.sin((t - T_DOT) * 6)
        d.ellipse([x - rr, y - rr, x + rr, y + rr], outline=SIG, width=3)
        d.line([(x + 18, y + 18), (x + 120, y + 120)], fill=SIG, width=3)
        d.text((x + 130, y + 124), "CRETE", font=F(BLK, 30), fill=SIG, anchor="lm")
    countdown(d, t)
    if cur in ("hook",): head(d, "1 M² EACH.", "LAND NEEDED", "?")
    elif cur == "rules": head(d, "8.2 BILLION.", "PEOPLE", f"{8.2 * ease_io(clamp((t - T_BN) / 1.0)):.1f} BN")
    elif cur == "lock": head(d, "LOCK IT IN.", "LAND NEEDED", "?")
    elif cur == "gut": head(d, "A CONTINENT?", "LAND NEEDED", "?")
    elif cur == "reveal": head(d, "THAT'S CRETE." if t >= T_CRETE else "8,200 KM².", "LAND NEEDED", f"{int(8200 * ease_io(clamp((t - T_KM) / .9))):,} km²" if t >= T_KM else "?", True)
    elif cur == "pour": head(d, "EVERYONE FITS.", "PEOPLE ON CRETE", f"{8.2 * u:.1f} BN", True)
    elif cur == "scale": head(d, f"×{int(18000 * ease_io(clamp((t - S('scale')) / 1.6))):,} MORE LAND.", "EARTH'S LAND", "149M km²")
    else: head(d, "SPACE ISN'T IT.", "EVERYONE ON CRETE", "8,200 km²", True)
    if cur == "reveal" and t >= T_CRETE: stamp_box(d, (780, 860), "CRETE", t, T_CRETE, size=80)
    fig(d, "1 m² per person, standing · Crete: Natural Earth 1:50m")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.scenes = {k: sc for k in ORDER[:-1]}
FX = [(T_MAP, whoosh(.6, .02), -.3), (T_ME, pop(.1), 0), (T_SHRINK, whoosh(.4, .02), 0), (T_TILE, whoosh(.8, .015), .2), *[(x, thud(.16), 0) for x in T_321], (T_GUT, pop(.08), 0), (T_KM, pop(.1), 0),
      (T_CRETE, thud(.22), 0), (T_P0, whoosh(1.2, .02), 0), (T_DOT, pop(.1), .3)]
if __name__ == "__main__": EP.run(FX)
