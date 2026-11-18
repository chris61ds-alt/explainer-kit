"""NOT JUST YOU – No. 146: Japan – Pew (2026, fielded 2025): an affair is morally unacceptable for 65 % in Japan vs 83 % in
South Korea and 90 % in the US; JFPA (2023 survey): nearly half of married people in Japan had no sex in the past month.
3D MAP (4th use, spin-off of No. 145): same 25-country blocks (height = % who call an affair wrong); the camera starts close on
Japan, pulls out to the US for the comparison and comes back; the 'home' beat (on black) adds a panel of 10 couples, half of
them drifting apart. Rule 13 opener: Japan's block rises next to Korea's taller one, "65 vs 83" stamp. Rule 15: payoff holds."""
import os, sys, math, json
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from fx2 import light_look, is_light, stamp, camera, cam_path
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .5, "setup": .5, "compare": .8, "home": .8, "why": .1})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "setup", "compare", "home", "why", "end"]
EP = ThreadEpisode(TL, 146, "JAPAN", order=ORDER, dark=True, label="PEW 2026 · JFPA 2023",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Pew Research Center (2026), 25-country survey ·", "Japan Family Planning Association (2023)"),
                   music=dict(bpm=88, root=-1, prog="tense", kick="half", audio="v5"),
                   cover=dict(words=["JAPAN JUDGES", "AN AFFAIR MORE", "MILDLY."], kicker="65% vs 83% next door."))
light_look(EP, ORDER, reveal=("home",))

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
def _h(s): return sum(map(ord, s))

HMAX = 70
def hfull(p): return 4 + HMAX * clamp((p - 40) / 55)
T_JP = .3; T_KR = .75
T_STAMP = cue("hook", "neighbors") - .1
T_ALL = cue("setup", "taller") - .2
T_KR2 = cue("compare", "South Korea") - .1; T_US = cue("compare", "the US") - .15
T_HOME = S("home") + .05
FOCUS = ("Japan", "South Korea", "United States of America")

def height(name, t):
    if name not in PCT: return 3
    if name == "Japan": return 3 + (hfull(65) - 3) * spring(clamp((t - T_JP) / .55))
    if name == "South Korea": return 3 + (hfull(83) - 3) * spring(clamp((t - T_KR) / .55))
    k = spring(clamp((t - T_ALL - (_h(name) % 9) * .04) / .6))
    if name == "United States of America": k = max(k, spring(clamp((t - T_US) / .5)))
    return 3 + (hfull(PCT[name]) - 3) * k

def block(d, ring, h, top, side):
    for i in range(0, int(h), 3): d.polygon([(x, y - i) for x, y in ring], fill=side)
    d.polygon([(x, y - h) for x, y in ring], fill=top, outline=side)

def tag(d, t, t0, lab, lo, la, dx, L_, f=28):
    if t < t0: return
    k = ease(clamp((t - t0) / .3)); x, y = proj(lo, la); y -= 10
    d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=SIG)
    tx = x + dx * k; ty = y - L_ * k
    d.line([(x, y), (tx, ty)], fill=INK, width=3)
    if k > .5:
        fo = F(BLK, f); w = d.textlength(lab, font=fo)
        d.rounded_rectangle([tx - w / 2 - 12, ty - f - 12, tx + w / 2 + 12, ty], radius=10, fill=WHITE, outline=INK, width=3)
        d.text((tx, ty - f / 2 - 6), lab, font=fo, fill=INK, anchor="mm")

def scene(L, d, t):
    cur = EP.current(t)
    for name, ring, _ in POLYS:
        h = height(name, t)
        if name not in PCT: top, side = WHITE, RULE
        elif name in FOCUS: top, side = INK, MID
        else: top, side = mix(WHITE, INK, .15 + .3 * clamp((PCT[name] - 50) / 45)), RULE
        block(d, ring, h, top, side)
    tag(d, t, T_JP + .5, "JAPAN 65%", 138, 36, -30, 150, 22)
    tag(d, t, T_KR + .4, "S. KOREA 83%", 127.8, 36.5, -150, 70, 22)
    if t >= T_US: tag(d, t, T_US + .3, "USA 90%", -98, 39, 0, 90)

def couples(d, t):
    """10 couples; half of them drift apart (nearly half sexless)"""
    if EP.current(t) not in ("home", "why", "end"): return
    x0, y0 = 70, 860; k0 = clamp((t - T_HOME) / .4)
    d.rounded_rectangle([x0, y0, x0 + 520, y0 + 290], radius=24, fill=WHITE, outline=INK, width=3)
    d.text((x0 + 24, y0 + 30), "10 MARRIED PEOPLE IN JAPAN", font=F(MONO, 22), fill=MID, anchor="lm")
    for i in range(10):
        cx = x0 + 68 + (i % 5) * 96; cy = y0 + 115 + (i // 5) * 100
        apart = i % 2 == 1 and i != 9 or i == 8                  # 5 of 10
        k = ease_io(clamp((t - T_HOME - .5 - i * .08) / .6)) if apart else 0
        g = 15 + 16 * k
        col = SIG if apart and k > .5 else INK
        for s in (-1, 1): d.ellipse([cx + s * g - 14, cy - 14, cx + s * g + 14, cy + 14], fill=col if s < 0 or not apart else col)
        if not apart: d.line([(cx - 12, cy), (cx + 12, cy)], fill=INK, width=4)
    if k0 >= 1 and t >= T_HOME + 1.4: d.text((x0 + 24, y0 + 262), "ABOUT HALF: NO SEX IN A MONTH", font=F(BLK, 22), fill=SIG, anchor="lm")

def cam(t):
    def at(lo, la): x, y = proj(lo, la); return (x, y - 40)
    jp = at(132, 37); m = (540, 800)
    keys = [(0, 2.4, jp), (S("setup") + .6, 2.4, jp), (S("setup") + 1.6, 1.0, m), (T_US + 1.2, 1.0, m), (T_HOME + .1, 2.0, at(128, 36)),
            (S("why") - .1, 2.0, at(128, 36)), (S("why") + .7, 1.0, m)]
    return cam_path(t, keys)

def labels(d, t):
    if T_STAMP <= t < S("setup") + .3: stamp(d, (760, 1040), "65 vs 83", t, T_STAMP, size=80)
    if T_ALL <= t < S("compare"):
        x0, y0 = 830, 1130
        for i, hh in enumerate((14, 30, 46)): d.rectangle([x0 + i * 46, y0 - hh, x0 + i * 46 + 30, y0], fill=INK if i == 2 else MID)
        d.text((x0 + 150, y0 - 10), "WRONG", font=F(BLK, 26), fill=INK, anchor="lm")
    couples(d, t)

def head(d, t, line):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    cur = EP.current(t)
    if cur in ("home",):
        d.text((X0, 400), "MARRIED, NO SEX IN A MONTH", font=F(MONO, 30), fill=MID)
        d.text((X0 + 540, 388), "~1/2", font=F(BLK, 56), fill=SIG)
    else:
        d.text((X0, 400), "AFFAIR = WRONG · JAPAN", font=F(MONO, 30), fill=MID)
        d.text((X0 + 470, 388), "65%" if t >= T_JP + .5 else "?", font=F(BLK, 56), fill=INK)

def draw(img, d, t, line, note="Pew 2026 · grey = not surveyed"):
    z, f = cam(t); camera(img, lambda L, dL: scene(L, dL, t), z, f)
    d = ImageDraw.Draw(img); labels(d, t); head(d, t, line); fig(d, note)

def sc_hook(img, d, t): draw(img, d, t, "JAPAN.")
def sc_setup(img, d, t): draw(img, d, t, "65% SAY WRONG.", note="Pew 2026 · surveyed in 2025")
def sc_compare(img, d, t): draw(img, d, t, "NEXT DOOR: 83%.")
def sc_home(img, d, t): draw(img, d, t, "AT HOME.", note="JFPA 2023 · random sample, ages 16–49")
def sc_why(img, d, t): draw(img, d, t, "RULES ≠ REALITY.", note="two different surveys")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.scenes = {"hook": sc_hook, "setup": sc_setup, "compare": sc_compare, "home": sc_home, "why": sc_why}
FX = [(T_JP, whoosh(.3, .025), .3), (T_KR, whoosh(.3, .025), -.2), (T_STAMP, thud(.3), .3),
      (S("setup") + .6, whoosh(.4, .03), 0), *[(T_ALL + .2 + j * .08, tick(.012), -.6 + j * .15) for j in range(8)],
      (T_KR2, pop(.1), -.3), (T_US, pop(.1), -.6), (S("home") + .05, thud(.35), 0),
      *[(T_HOME + .5 + i * .16, tick(.012), -.4 + i * .2) for i in range(5)], (S("why") + .1, whoosh(.3, .025), 0)]
if __name__ == "__main__": EP.run(FX)
