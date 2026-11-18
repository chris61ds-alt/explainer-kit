"""NOT JUST YOU – No. 145: is an affair always wrong? – Pew (5 March 2026), Spring 2025 survey, 25 countries, >30,000 adults:
share saying married people having an affair is morally unacceptable: Indonesia & Turkey 92 %, US 90 % … Germany 55 %, France 53 %.
3D MAP (3rd use): tilted extruded world map; block height = % who call an affair wrong (scaled from 40 %); countries not surveyed
stay flat. Follow-up to No. 141 (Where's the line?).
Light look (paper; the France/Germany beat on black) + clarity rules ("The taller the block…") + rule 13 opener (all 25 blocks
slam up, "53% vs 92%" stamp) + rule 15 (the payoff stays: both extremes tagged to the last frame, no loop)."""
import os, sys, math, json
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from fx2 import light_look, is_light, stamp, camera, cam_path
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .5, "setup": .5, "explain": .5, "top": .6, "bottom": .8, "why": .1})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "setup", "explain", "top", "bottom", "why", "end"]
EP = ThreadEpisode(TL, 145, "AFFAIRS, WORLDWIDE", order=ORDER, dark=True, label="PEW · 25 COUNTRIES · 2025 SURVEY",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Pew Research Center (2026), 25-country", "survey on morality, fielded Jan – May 2025"),
                   music=dict(bpm=92, root=-3, prog="tense", kick="half", audio="v5"),
                   cover=dict(words=["IS AN AFFAIR", "ALWAYS WRONG?", "53% vs 92%."], kicker="It depends on where you ask."))
light_look(EP, ORDER, reveal=("bottom",))

PCT = {"Indonesia": 92, "Turkey": 92, "United States of America": 90, "Israel": 85, "Australia": 84, "Nigeria": 83, "South Korea": 83,
       "United Kingdom": 81, "Poland": 80, "Brazil": 77, "Greece": 77, "India": 77, "Sweden": 77, "Canada": 76, "Mexico": 76,
       "Kenya": 70, "South Africa": 69, "Italy": 67, "Netherlands": 67, "Argentina": 65, "Japan": 65, "Spain": 65, "Hungary": 64,
       "Germany": 55, "France": 53}
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
assert all(n in {p[0] for p in POLYS} for n in PCT), [n for n in PCT if n not in {p[0] for p in POLYS}]
def _h(s): return sum(map(ord, s))

HMAX = 90
def hfull(p): return 4 + HMAX * clamp((p - 40) / 55)
T_UP = .3
T_STAMP = cue("hook", "Depends") - .05
T_REW = S("setup") - .05
T_GROW = cue("explain", "taller") - .2
T_TOP = S("top") + .05; T_BOT = S("bottom") + .05
TAGS = {"top": [("INDONESIA 92%", 118, -2, 40, 80), ("TURKEY 92%", 35, 39, 60, 150), ("USA 90%", -98, 39, 0, 90)],
        "bottom": [("FRANCE 53%", 2.5, 46.5, -110, 90), ("GERMANY 55%", 10, 51, 90, 120)]}
FINAL = [("FRANCE 53%", 2.5, 46.5, -150, 110), ("INDONESIA 92%", 118, -2, -40, 90), ("TURKEY 92%", 35, 39, 110, 150)]

def height(name, t):
    if name not in PCT: return 3
    if t < T_REW:                                            # cold open: everything slams up at once
        k = spring(clamp((t - T_UP - (_h(name) % 7) * .04) / .55))
        return 3 + (hfull(PCT[name]) - 3) * k
    if t < T_GROW:                                           # rewind flat for the explanation
        return 3 + (hfull(PCT[name]) - 3) * (1 - ease_io(clamp((t - T_REW) / .5)))
    k = spring(clamp((t - T_GROW - (100 - PCT[name]) * .01) / .7))
    return 3 + (hfull(PCT[name]) - 3) * k

def block(d, ring, h, top, side):
    for i in range(0, int(h), 3): d.polygon([(x, y - i) for x, y in ring], fill=side)
    d.polygon([(x, y - h) for x, y in ring], fill=top, outline=side)

def hot_names(t):
    cur = EP.current(t)
    if cur == "top": return {"Indonesia", "Turkey", "United States of America"}
    if cur == "bottom": return {"France", "Germany"}
    if cur in ("why", "end"): return {"France", "Indonesia", "Turkey"}
    return set()

def tag(d, t, t0, lab, lo, la, dx, L_):
    if t < t0: return
    k = ease(clamp((t - t0) / .3)); x, y = proj(lo, la); y -= 10
    d.ellipse([x - 8, y - 8, x + 8, y + 8], fill=SIG)
    tx = x + dx * k; ty = y - L_ * k
    d.line([(x, y), (tx, ty)], fill=INK, width=3)
    if k > .5:
        f = F(BLK, 28); w = d.textlength(lab, font=f); tx = min(max(tx, w / 2 + 30), 1050 - w / 2)
        d.rounded_rectangle([tx - w / 2 - 12, ty - 40, tx + w / 2 + 12, ty], radius=10, fill=WHITE, outline=INK, width=3)
        d.text((tx, ty - 20), lab, font=f, fill=INK, anchor="mm")

def scene(L, d, t):
    hot = hot_names(t)
    for name, ring, _ in POLYS:
        h = height(name, t)
        if name not in PCT: top, side = WHITE, RULE
        elif name in hot: top, side = INK, MID
        else: top, side = mix(WHITE, INK, .15 + .45 * clamp((PCT[name] - 50) / 45)), RULE
        block(d, ring, h, top, side)
    cur = EP.current(t)
    if cur in ("top", "bottom"):
        for i, tg in enumerate(TAGS[cur]): tag(d, t, (T_TOP if cur == "top" else T_BOT) + .4 + i * .35, *tg)
    if cur in ("why", "end"):
        for i, tg in enumerate(FINAL): tag(d, t, S("why") + .2 + i * .2, *tg)

def cam(t):
    m = (540, 800)
    def at(lo, la): x, y = proj(lo, la); return (x, y - 50)
    keys = [(0, 1.0, m), (T_BOT - .2, 1.0, m), (T_BOT + .7, 1.55, at(8, 47)), (S("why") - .1, 1.55, at(8, 47)), (S("why") + .6, 1.0, m)]
    return cam_path(t, keys)

def labels(d, t):
    if T_STAMP <= t < T_REW + .2: stamp(d, (760, 600), "53% vs 92%", t, T_STAMP, size=80)
    if T_GROW <= t < T_TOP:
        x0, y0 = 830, 1130
        for i, hh in enumerate((14, 30, 46)): d.rectangle([x0 + i * 46, y0 - hh, x0 + i * 46 + 30, y0], fill=INK if i == 2 else MID)
        d.text((x0 + 150, y0 - 10), "WRONG", font=F(BLK, 26), fill=INK, anchor="lm")

def head(d, t, line):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    cur = EP.current(t)
    d.text((X0, 400), "SAY AN AFFAIR IS WRONG", font=F(MONO, 30), fill=MID)
    v = {"top": "92%", "bottom": "53%"}.get(cur, "53–92%" if cur in ("why", "end") or (T_STAMP <= t < T_REW) else "MEDIAN 77%" if t >= T_GROW else "?")
    d.text((X0 + 470, 388), v, font=F(BLK, 56), fill=SIG if cur == "bottom" else INK)

def draw(img, d, t, line, note="Pew 2026 · 25 countries · grey = not surveyed"):
    z, f = cam(t); camera(img, lambda L, dL: scene(L, dL, t), z, f)
    d = ImageDraw.Draw(img); labels(d, t); head(d, t, line); fig(d, note)

def sc_hook(img, d, t): draw(img, d, t, "ALWAYS WRONG?")
def sc_setup(img, d, t): draw(img, d, t, "25 COUNTRIES", note="30,000+ adults · surveyed in 2025")
def sc_explain(img, d, t): draw(img, d, t, "1 BLOCK = 1 COUNTRY")
def sc_top(img, d, t): draw(img, d, t, "MOST STRICT.")
def sc_bottom(img, d, t): draw(img, d, t, "BARELY HALF.", note="others: acceptable or not a moral issue")
def sc_why(img, d, t): draw(img, d, t, "IT DEPENDS WHERE.")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.scenes = {"hook": sc_hook, "setup": sc_setup, "explain": sc_explain, "top": sc_top, "bottom": sc_bottom, "why": sc_why}
FX = [(T_UP, whoosh(.3, .025), 0), *[(T_UP + .15 + j * .07, tick(.012), -.6 + j * .15) for j in range(8)], (T_STAMP, thud(.3), .3),
      (T_REW, whoosh(.3, .025), 0), *[(T_GROW + .2 + j * .08, tick(.012), -.6 + j * .15) for j in range(8)],
      (T_TOP, whoosh(.3, .025), .3), *[(T_TOP + .4 + i * .35, tick(.015), -.4 + i * .4) for i in range(3)],
      (S("bottom") + .05, thud(.35), 0), *[(T_BOT + .4 + i * .35, tick(.015), -.3 + i * .6) for i in range(2)],
      *[(S("why") + .2 + i * .2, tick(.012), -.4 + i * .4) for i in range(3)]]
if __name__ == "__main__": EP.run(FX)
