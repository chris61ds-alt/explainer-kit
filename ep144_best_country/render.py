"""NOT JUST YOU – No. 144: the best country to live in depends on what you count – Numbeo 2026 Mid-Year (crowd-sourced),
89 countries; five criteria, five different winners: weather Uruguay, safety UAE, food Pakistan, buying power Kuwait, rent Bangladesh.
3D MAP (2nd use): tilted extruded world map; block height = percentile rank of the country in the current criterion; the top 3
are black with tags (small ones like Malta get a pin); countries without data stay flat. Criteria morph into each other.
Light look (paper; the safety beat on black) + clarity rules ("The taller the block, the better") + rule 13 opener (blocks
jump between criteria like a shuffling ranking, "IT DEPENDS" stamp). Loop: everything sinks flat."""
import os, sys, math, json
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from fx2 import light_look, is_light, stamp, camera, cam_path
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .5, "setup": .5, "weather": .5, "safety": .5, "food": .5, "pay": .5, "rent": .6, "why": .1})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "setup", "weather", "safety", "food", "pay", "rent", "why", "end"]
EP = ThreadEpisode(TL, 144, "BEST COUNTRY?", order=ORDER, dark=True, label="NUMBEO · 2026 MID-YEAR · 89 COUNTRIES",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Numbeo, Quality of Life & Cost of Living", "Index by Country, 2026 Mid-Year (crowd-sourced)"),
                   music=dict(bpm=100, root=2, prog="major", kick="four", audio="v5"),
                   cover=dict(words=["THE BEST COUNTRY", "TO LIVE IN?", "IT DEPENDS."], kicker="5 criteria, 5 different winners."))
light_look(EP, ORDER, reveal=("safety",))

RAW = json.load(open(os.path.join(HERE, "numbeo2026.json")))["data"]
ALIAS = {"United States": "United States of America", "Czech Republic": "Czechia", "Bosnia And Herzegovina": "Bosnia and Herz."}
DATA = {ALIAS.get(k, k): v for k, v in RAW.items()}
CRIT = {"weather": ("climate", False), "safety": ("safety", False), "food": ("groceries", True), "pay": ("power", False), "rent": ("rent", True)}
NAMES = list(DATA)
SCORE = {}
for c, (key, inv) in CRIT.items():
    v = np.array([DATA[n][key] for n in NAMES]); r = v.argsort().argsort() / (len(v) - 1)
    SCORE[c] = {n: float(1 - x if inv else x) for n, x in zip(NAMES, r)}
TOP3 = {c: sorted(NAMES, key=lambda n: -SCORE[c][n])[:3] for c in CRIT}
LABEL = {"weather": "WEATHER", "safety": "SAFETY", "food": "FOOD PRICES", "pay": "BUYING POWER", "rent": "RENT"}
TAGS = {"weather": [("URUGUAY", -56, -33, 0, 70), ("MALTA", 14.4, 35.9, 40, 140), ("PORTUGAL", -8, 39.5, -120, 80)],
        "safety": [("UAE", 54, 24, 50, 70), ("QATAR", 51.2, 25.3, -130, 140), ("TAIWAN", 121, 23.7, 0, 70)],
        "food": [("PAKISTAN", 70, 30, -10, 160), ("INDIA", 79, 22, 160, 70), ("IRAN", 53, 32, -190, 70)],
        "pay": [("KUWAIT", 47.7, 29.3, -40, 160), ("QATAR", 51.2, 25.3, 110, 80), ("SWITZERLAND", 8.2, 46.8, -80, 80)],
        "rent": [("BANGLADESH", 90, 24, 180, 70), ("PAKISTAN", 70, 30, -180, 70), ("INDIA", 79, 22, 0, 170)]}
# check the tags against the data (the top 3 must match)
_alias_tag = {"URUGUAY": "Uruguay", "MALTA": "Malta", "PORTUGAL": "Portugal", "UAE": "United Arab Emirates", "QATAR": "Qatar",
              "TAIWAN": "Taiwan", "PAKISTAN": "Pakistan", "INDIA": "India", "IRAN": "Iran", "KUWAIT": "Kuwait",
              "SWITZERLAND": "Switzerland", "BANGLADESH": "Bangladesh"}
for c in CRIT: assert [_alias_tag[t[0]] for t in TAGS[c]] == TOP3[c], (c, TOP3[c])

LON0, LON1, LAT_TOP = -130, 155, 75
SCL = 1040 / (LON1 - LON0); TILT = .62; MAP_Y0 = 640
def proj(lon, lat): return 20 + (lon - LON0) * SCL, MAP_Y0 + (LAT_TOP - lat) * SCL * TILT
POLYS = []
for f in json.load(open(os.path.join(HERE, "countries.geojson")))["features"]:
    name = f["properties"]["NAME"]
    if name == "Antarctica": continue
    g = f["geometry"]; parts = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    for p in parts:
        ring = [proj(lo, la) for lo, la in p[0]]
        if len(ring) > 2: POLYS.append((name, ring, max(y for _, y in ring)))
POLYS.sort(key=lambda r: r[2])
def _h(s): return sum(map(ord, s))

CRITS = ["weather", "safety", "food", "pay", "rent"]
T_C = {c: S(c) + .05 for c in CRITS}
T_STAMP = cue("hook", "changes") - .05
T_REW = S("setup") - .05
T_SET = cue("setup", "taller") - .2
T_BACK = E("why") - 1.1
HMAX = 72

def crit_at(t):
    """which criterion drives the heights at time t (+ blend progress from the previous one)"""
    if t < T_REW:                                               # cold open: the ranking shuffles through all five, fast
        if t < .3: return None, None, 0
        j = int((t - .3) / .55); i = j % 5; k = clamp(((t - .3) % .55) / .3)
        return (CRITS[i - 1] if j > 0 else None), CRITS[i], k
    if t < T_SET: return None, None, 0
    if t < T_C["weather"]: return None, "avg", clamp((t - T_SET) / .6)
    prev = "avg"
    for c in CRITS:
        if t >= T_C[c]: prev, cur = (CRITS[CRITS.index(c) - 1] if c != "weather" else "avg"), c
    return prev, cur, clamp((t - T_C[cur]) / .7)

def h_of(name, c):
    if name not in DATA: return 0.0
    if c is None: return 0.0
    if c == "avg": return .5
    return SCORE[c][name]

def height(name, t):
    a, b, k = crit_at(t)
    back = ease_io(clamp((t - T_BACK) / .8)) if t >= T_BACK else 0
    if b is None: return 3
    if t < T_REW and t >= T_REW - .4: back = ease_io((t - T_REW + .4) / .4)
    v = h_of(name, a) + (h_of(name, b) - h_of(name, a)) * spring(k)
    return 3 + HMAX * max(0, v) * (1 - back)

def block(d, ring, h, top, side):
    for i in range(0, int(h), 3): d.polygon([(x, y - i) for x, y in ring], fill=side)
    d.polygon([(x, y - h) for x, y in ring], fill=top, outline=side)

def cur_crit(t):
    c = EP.current(t); return c if c in CRITS else None

def scene(L, d, t):
    c = cur_crit(t)
    for name, ring, _ in POLYS:
        h = height(name, t)
        if name not in DATA: top, side = WHITE, RULE
        elif c and name in [_alias_tag.get(x[0]) for x in TAGS[c]]: top, side = INK, MID
        else: v = h_of(name, c) if c else .4; top, side = mix(WHITE, INK, .12 + .5 * v), RULE
        block(d, ring, h, top, side)
    if c:
        for i, (lab, lo, la, dx, L_) in enumerate(TAGS[c]):
            t0 = T_C[c] + .45 + i * .3
            if t < t0: continue
            x, y = proj(lo, la); y -= HMAX + 6
            k = ease(clamp((t - t0) / .3))
            d.ellipse([x - 7, y - 7 + HMAX - 4, x + 7, y + 7 + HMAX - 4], fill=SIG)              # pin (small countries too)
            tx = x + dx * k
            d.line([(x, y + HMAX - 4), (tx, y - L_ * k)], fill=INK, width=3)
            if k > .5:
                f = F(BLK, 28); w = d.textlength(f"{i + 1}. {lab}", font=f); tx = min(max(tx, w / 2 + 30), 1050 - w / 2)
                d.rounded_rectangle([tx - w / 2 - 12, y - L_ - 40, tx + w / 2 + 12, y - L_], radius=10, fill=WHITE, outline=INK, width=3)
                d.text((tx, y - L_ - 20), f"{i + 1}. {lab}", font=f, fill=INK, anchor="mm")

def cam(t):
    m = (540, 800)
    def at(lo, la): x, y = proj(lo, la); return (x, y - 40)
    keys = [(0, 1.0, m), (T_C["food"] - .2, 1.0, m), (T_C["food"] + .7, 1.3, at(65, 28)), (T_C["pay"] - .2, 1.3, at(65, 28)),
            (T_C["pay"] + .7, 1.0, m), (T_C["rent"] - .2, 1.0, m), (T_C["rent"] + .7, 1.3, at(75, 27)), (T_BACK - .3, 1.3, at(75, 27)),
            (T_BACK + .6, 1.0, m)]
    return cam_path(t, keys)

def labels(d, t):
    if T_STAMP <= t < T_REW + .2: stamp(d, (760, 600), "IT DEPENDS", t, T_STAMP, size=80)
    if T_SET <= t < T_C["weather"]:
        x0, y0 = 830, 1130
        for i, hh in enumerate((14, 30, 46)): d.rectangle([x0 + i * 46, y0 - hh, x0 + i * 46 + 30, y0], fill=INK if i == 2 else MID)
        d.text((x0 + 150, y0 - 10), "BETTER", font=F(BLK, 26), fill=INK, anchor="lm")

def head(d, t, line):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    c = cur_crit(t)
    if c:
        d.text((X0, 400), LABEL[c] + " · NO. 1", font=F(MONO, 30), fill=MID)
        d.text((X0 + d.textlength(LABEL[c] + " · NO. 1", font=F(MONO, 30)) + 24, 388), TAGS[c][0][0], font=F(BLK, 56), fill=SIG if c == "safety" else INK)
    else:
        d.text((X0, 400), "CRITERIA", font=F(MONO, 30), fill=MID)
        d.text((X0 + 170, 388), "5", font=F(BLK, 56), fill=INK)

def draw(img, d, t, line, note="Numbeo 2026 · crowd-sourced · height = rank among 89"):
    z, f = cam(t); camera(img, lambda L, dL: scene(L, dL, t), z, f)
    d = ImageDraw.Draw(img); labels(d, t); head(d, t, line); fig(d, note)

def sc_hook(img, d, t): draw(img, d, t, "BEST COUNTRY?")
def sc_setup(img, d, t): draw(img, d, t, "5 THINGS. 89 COUNTRIES.")
def sc_weather(img, d, t): draw(img, d, t, "WEATHER.")
def sc_safety(img, d, t): draw(img, d, t, "SAFETY.")
def sc_food(img, d, t): draw(img, d, t, "FOOD PRICES.", note="Numbeo groceries index · cheaper = taller")
def sc_pay(img, d, t): draw(img, d, t, "BUYING POWER.", note="what a local salary buys locally")
def sc_rent(img, d, t): draw(img, d, t, "RENT.", note="Numbeo rent index · cheaper = taller")
def sc_why(img, d, t): draw(img, d, t, "5 DIFFERENT WINNERS." if t < T_BACK else "BEST COUNTRY?")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.scenes = {"hook": sc_hook, "setup": sc_setup, "weather": sc_weather, "safety": sc_safety, "food": sc_food, "pay": sc_pay,
             "rent": sc_rent, "why": sc_why}
FX = [*[(.3 + j * .55, tick(.012), (-.4 if j % 2 else .4)) for j in range(int((T_REW - .3) / .55))], (T_STAMP, thud(.3), .3),
      (T_REW - .4, whoosh(.3, .03), 0), (T_SET, pop(.08), 0), (S("safety") + .05, thud(.4), 0),
      *[(T_C[c] + .05, whoosh(.3, .025), 0) for c in CRITS if c != "safety"],
      *[(T_C[c] + .45 + i * .3, tick(.012), -.4 + i * .4) for c in CRITS for i in range(3)], (T_BACK, whoosh(.6, .05), 0)]
if __name__ == "__main__": EP.run(FX)
