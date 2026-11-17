"""NOT JUST YOU – No. 143: what countries sell – UNCTAD (2023): 101 of 191 countries are commodity-dependent; map: each country's
top export (CEPII 2018 via Visual Capitalist) grouped into OIL & COAL / METALS / CROPS / MADE.
FIRST 3D MAP (17.11.2026): an extruded world map (Natural Earth 110m) seen at a tilt; countries rise as blocks when their
category is named; the named category is tall + black, earlier ones stay up in grey, so the map fills up category by category.
Light look (paper; the oil beat on black) + clarity rules ("Each country rises when…") + rule 13 opener (all raw-material
countries shoot up at once, "OVER HALF" stamp). Camera pushes into the region being talked about. Loop: everything sinks flat."""
import os, sys, math, json
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from fx2 import light_look, is_light, stamp, camera, cam_path
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from exports import TOP, cat
TL = Timeline(HERE, lead=.05, gaps={"hook": .5, "setup": .5, "explain": .5, "oil": .6, "metals": .5, "food": .5, "made": .6, "why": .1})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "setup", "explain", "oil", "metals", "food", "made", "why", "end"]
EP = ThreadEpisode(TL, 143, "WHAT COUNTRIES SELL", order=ORDER, dark=True, label="UNCTAD 2023 · TRADE DATA 2018",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("UNCTAD, State of Commodity Dependence 2023 ·", "CEPII BACI 2018 via Visual Capitalist"),
                   music=dict(bpm=96, root=-2, prog="tense", kick="four", audio="v5"),
                   cover=dict(words=["HALF THE WORLD", "LIVES FROM OIL,", "METALS & CROPS."], kicker="What every country sells most."))
light_look(EP, ORDER, reveal=("oil",))

# ---- geometry: tilted equirectangular map
LON0, LON1, LAT_TOP = -130, 155, 75
SCL = 1040 / (LON1 - LON0); TILT = .62; MAP_Y0 = 640
def proj(lon, lat): return 20 + (lon - LON0) * SCL, MAP_Y0 + (LAT_TOP - lat) * SCL * TILT
POLYS = []                                                      # (name, category, ring in screen coords, depth)
for f in json.load(open(os.path.join(HERE, "countries.geojson")))["features"]:
    name = f["properties"]["NAME"]
    if name == "Antarctica": continue
    g = f["geometry"]; parts = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    for p in parts:
        ring = [proj(lo, la) for lo, la in p[0]]
        if len(ring) > 2: POLYS.append((name, cat(name), ring, max(y for _, y in ring)))
POLYS.sort(key=lambda r: r[3])                                  # far (north) first, near (south) last
COUNT = {k: sum(1 for n in set(p[0] for p in POLYS) if cat(n) == k) for k in ("OIL", "METALS", "FOOD", "MADE")}
LABEL = {"OIL": "OIL & COAL", "METALS": "METALS", "FOOD": "CROPS & FOOD", "MADE": "MADE GOODS"}
RAW = ("OIL", "METALS", "FOOD")

T_RISE = .35
T_STAMP = cue("hook", "half") - .05
T_REW = S("setup") - .05
T_DEMO = cue("explain", "rises") - .2
T_CAT = {"OIL": S("oil") + .05, "METALS": S("metals") + .05, "FOOD": S("food") + .05, "MADE": S("made") + .05}
T_BACK = 1e9
TAGS = {"OIL": [("NORWAY", 10, 62), ("NIGERIA", 8, 9), ("SAUDI ARABIA", 45, 24)],
        "METALS": [("GHANA · GOLD", -1, 7), ("CONGO · COPPER", 23, -3), ("CHILE · COPPER", -71, -28)],
        "FOOD": [("ETHIOPIA · COFFEE", 39, 9), ("IVORY COAST · COCOA", -5, 7), ("BRAZIL · SOY", -52, -10)],
        "MADE": [("GERMANY · CARS", 10, 51), ("CHINA · PHONES", 104, 34), ("JAPAN · CARS", 138, 37)]}

def _h(s): return sum(map(ord, s))

def current_cat(t):
    cur = EP.current(t); return cur.upper() if cur in ("oil", "metals", "food", "made") else None

def height(name, c, t):
    """block height (px) and role: 'hot' (named now), 'up' (named before), 'flat'"""
    if t < T_REW:                                               # cold open: every raw-material country shoots up
        if c in RAW: k = spring(clamp((t - T_RISE - (_h(name) % 7) * .03) / .5)); return 3 + 34 * k, "hot" if k > .05 else "flat"
        return 3, "flat"
    if t < T_REW + .5 and t >= T_REW:
        if c in RAW: return 3 + 34 * (1 - ease_io((t - T_REW) / .5)), "up"
        return 3, "flat"
    if name == "Germany" and T_DEMO <= t < T_CAT["OIL"] - .2:   # the picture explained once
        return 3 + 34 * spring((t - T_DEMO) / .5), "hot"
    back = ease_io(clamp((t - T_BACK) / .8)) if t >= T_BACK else 0
    if c and t >= T_CAT[c]:
        k = spring((t - T_CAT[c] - (_h(name) % 9) * .025) / .55)
        hot = current_cat(t) == c or (EP.current(t) in ("why", "end") and c in RAW)   # payoff: drill, dig, grow
        h = (3 + 38 * k) if hot else 3 + 12 * (1 if k >= 1 else k)
        return h * (1 - back) + 3 * back, ("hot" if hot else "up") if back < .5 else "flat"
    return 3, "flat"

def block(d, ring, h, top, side):
    for i in range(0, int(h), 3): d.polygon([(x, y - i) for x, y in ring], fill=side)
    d.polygon([(x, y - h) for x, y in ring], fill=top, outline=side)

def scene(L, d, t):
    for name, c, ring, _ in POLYS:
        h, role = height(name, c, t)
        if role == "hot": top, side = INK, MID
        elif role == "up": top, side = MID, RULE
        else: top, side = WHITE, RULE
        block(d, ring, h, top, side)
    c = current_cat(t)
    if c:                                                       # region tags
        for i, (lab, lo, la) in enumerate(TAGS[c]):
            t0 = T_CAT[c] + .5 + i * .35
            if t < t0: continue
            x, y = proj(lo, la); y -= 44; L = 60 + 70 * (i % 2)
            k = ease(clamp((t - t0) / .3))
            d.line([(x, y), (x, y - L * k)], fill=INK, width=3)
            if k > .5:
                f = F(BLK, 26); w = d.textlength(lab, font=f); x = min(max(x, w / 2 + 30), 1050 - w / 2)
                d.rounded_rectangle([x - w / 2 - 12, y - L - 40, x + w / 2 + 12, y - L], radius=10, fill=WHITE, outline=INK, width=3)
                d.text((x, y - L - 20), lab, font=f, fill=INK, anchor="mm")
    if T_DEMO <= t < T_CAT["OIL"] - .2:
        x, y = proj(10, 51); d.text((x + 40, y - 120), "GERMANY: CARS", font=F(BLK, 32), fill=INK, anchor="lm")

def cam(t):
    m = (540, 800)
    def at(lo, la): x, y = proj(lo, la); return (x, y - 30)
    keys = [(0, 1.0, m), (T_CAT["OIL"] - .2, 1.0, m), (T_CAT["OIL"] + .8, 1.25, at(30, 30)), (T_CAT["METALS"] - .2, 1.25, at(30, 30)),
            (T_CAT["METALS"] + .7, 1.0, m), (T_CAT["MADE"] - .2, 1.0, m), (T_CAT["MADE"] + .8, 1.2, at(55, 42)), (S("why") - .1, 1.2, at(55, 42)),
            (S("why") + .6, 1.0, m)]
    return cam_path(t, keys)

def labels(d, t):
    if T_STAMP <= t < T_REW + .2: stamp(d, (760, 600), "OVER HALF", t, T_STAMP, size=80)

def head(d, t, line):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    c = current_cat(t)
    if c:
        d.text((X0, 400), LABEL[c], font=F(MONO, 30), fill=MID)
        d.text((X0 + d.textlength(LABEL[c], font=F(MONO, 30)) + 24, 388), f"{COUNT[c]} COUNTRIES", font=F(BLK, 56), fill=SIG if c == "OIL" else INK)
    else:
        d.text((X0, 400), "COMMODITY-DEPENDENT", font=F(MONO, 30), fill=MID)
        d.text((X0 + 400, 388), "101 / 191" if t >= T_STAMP and t < T_DEMO else "?" if t < T_STAMP else "53%", font=F(BLK, 56), fill=INK)

def draw(img, d, t, line, note="map: each country's no. 1 export, 2018 · grouped"):
    z, f = cam(t); camera(img, lambda L, dL: scene(L, dL, t), z, f)
    d = ImageDraw.Draw(img); labels(d, t); head(d, t, line); fig(d, note)

def sc_hook(img, d, t): draw(img, d, t, "WHO SELLS WHAT?")
def sc_setup(img, d, t): draw(img, d, t, "RAW MATERIALS", note="UNCTAD 2023 · over 60% of exports = commodities")
def sc_explain(img, d, t): draw(img, d, t, "1 BLOCK = 1 COUNTRY")
def sc_oil(img, d, t): draw(img, d, t, "OIL & COAL.")
def sc_metals(img, d, t): draw(img, d, t, "METALS.")
def sc_food(img, d, t): draw(img, d, t, "CROPS.")
def sc_made(img, d, t): draw(img, d, t, "MADE GOODS.")
def sc_why(img, d, t): draw(img, d, t, "DRILL. DIG. GROW." if t < T_BACK else "WHO SELLS WHAT?")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.scenes = {"hook": sc_hook, "setup": sc_setup, "explain": sc_explain, "oil": sc_oil, "metals": sc_metals, "food": sc_food,
             "made": sc_made, "why": sc_why}
FX = [(T_RISE, whoosh(.5, .04), 0), *[(T_RISE + .1 + j * .05, tick(.015), -.6 + j * .15) for j in range(8)], (T_STAMP, thud(.4), .3),
      (T_REW, whoosh(.5, .05), 0), (T_DEMO, pop(.12), -.2), (S("oil") + .05, thud(.4), 0),
      *[(T_CAT[c] + .1, whoosh(.4, .04), 0) for c in ("METALS", "FOOD", "MADE")],
      *[(T_CAT[c] + .5 + i * .35, tick(.02), -.4 + i * .4) for c in T_CAT for i in range(3)], (T_BACK, whoosh(.6, .05), 0)]
FX = [fx for fx in FX if fx[0] < 1e8]                  # rule 15 (17.11.2026): no loop, the payoff stays to the last frame
if __name__ == "__main__": EP.run(FX)
