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
    crete(d, t); u = grains(d, t)
    if cur == "gut":                                                         # 'a whole continent?' -> Australia lights up
        for p in AUS:
            if len(p) > 2: d.polygon(p, fill=SIG)
    if cur in ("scale", "why", "end") and t >= T_DOT:                       # Crete on the world map: one tiny dot
        k = spring(clamp((t - T_DOT) / .5)); x, y = CRETE_ON_MAP
        d.ellipse([x - 7 * k, y - 7 * k, x + 7 * k, y + 7 * k], fill=SIG)
        d.ellipse([x - 26, y - 26, x + 26, y + 26], outline=SIG, width=3)
        d.line([(x + 18, y + 18), (x + 120, y + 120)], fill=SIG, width=3)
        d.text((x + 130, y + 124), "CRETE", font=F(BLK, 30), fill=SIG, anchor="lm")
    countdown(d, t)
    if cur in ("hook",): head(d, "1 M² EACH.", "LAND NEEDED", "?")
    elif cur == "rules": head(d, "8.2 BILLION.", "1 GRAIN = ~3 MILLION PEOPLE", "")
    elif cur == "lock": head(d, "LOCK IT IN.", "LAND NEEDED", "?")
    elif cur == "gut": head(d, "A CONTINENT?", "LAND NEEDED", "?")
    elif cur == "reveal": head(d, "THAT'S CRETE." if t >= T_CRETE else "8,200 KM².", "LAND NEEDED", "8,200 km²" if t >= T_KM else "?", True)
    elif cur == "pour": head(d, "EVERYONE FITS.", "PEOPLE ON CRETE", f"{8.2 * u:.1f} BN", True)
    elif cur == "scale": head(d, "×18,000 MORE LAND.", "EARTH'S LAND", "149M km²")
    else: head(d, "SPACE ISN'T IT.", "EVERYONE ON CRETE", "8,200 km²", True)
    if cur == "reveal" and t >= T_CRETE: stamp_box(d, (780, 860), "CRETE", t, T_CRETE, size=80)
    fig(d, "1 m² per person, standing · Crete: Natural Earth 1:50m")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.scenes = {k: sc for k in ORDER[:-1]}
FX = [(T_MAP, whoosh(.6, .02), -.3), *[(x, thud(.16), 0) for x in T_321], (T_GUT, pop(.08), 0), (T_KM, pop(.1), 0),
      (T_CRETE, thud(.22), 0), (T_P0, whoosh(1.2, .02), 0), (T_DOT, pop(.1), .3)]
if __name__ == "__main__": EP.run(FX)
