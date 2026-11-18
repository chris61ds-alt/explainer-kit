"""NOT JUST YOU – No. 146 2.0: CLICHÉ CHECK · JAPAN (first episode of the 'cliché check' format, 18.11.2026).
Three clichés, each: quote card ("CLICHÉ?") -> evidence in the picture -> verdict stamp (TRUE / HALF TRUE / FALSE / NO DATA).
1 "Cheating is no big deal there." – Pew 2026 (fielded 2025): Japan 65 % call an affair wrong, South Korea 83 % -> HALF TRUE
2 "Japanese couples don't have sex." – JFPA 2023 survey: nearly half of married people no sex in the past month -> HALF TRUE
3 "Paid sex doesn't count as cheating." – no representative survey found -> NO DATA (on black)
Base: the 3D map (blocks = % who call an affair wrong, Pew 25 countries), camera on East Asia. Rule 15: the scorecard of
all three verdicts stays to the last frame. Old version: render_v1.py / script_v1.json."""
import os, sys, math, json
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from fx2 import light_look, is_light, stamp, camera, cam_path
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .5, "c1": .8, "c2": .8, "c3": .8, "why": .1})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "c1", "c2", "c3", "why", "end"]
EP = ThreadEpisode(TL, 146, "CLICHÉ CHECK: JAPAN", order=ORDER, dark=True, label="PEW 2026 · JFPA 2023",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Pew Research Center (2026), 25-country survey ·", "Japan Family Planning Association (2023)"),
                   music=dict(bpm=96, root=0, prog="major", kick="four", audio="v5"),
                   cover=dict(words=["3 CLICHÉS", "ABOUT LOVE", "IN JAPAN."], kicker="Checked against the data."))
light_look(EP, ORDER, reveal=("c3",))

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
HMAX = 70
def hfull(p): return 4 + HMAX * clamp((p - 40) / 55)

CLICHES = {"c1": "\"CHEATING IS NO BIG DEAL THERE.\"", "c2": "\"COUPLES DON'T HAVE SEX.\"", "c3": "\"PAID SEX ISN'T CHEATING.\""}
VERDICT = {"c1": "HALF TRUE", "c2": "HALF TRUE", "c3": "NO DATA"}
T_Q = {c: S(c) + .05 for c in CLICHES}                               # quote card lands
T_V = {"c1": cue("c1", "Half true") - .1, "c2": cue("c2", "Half true") - .1, "c3": cue("c3", "No data") - .1}
T_JP = cue("c1", "Sixty-five") - .15; T_KR = cue("c1", "South Korea") - .15
T_HALF = cue("c2", "Nearly half") - .15
T_NOSURVEY = cue("c3", "no solid") - .15
T_HOOK_CARDS = [.25, .55, .85]                                        # cold open: three quote cards slam onto Japan

def height(name, t):
    if name not in PCT: return 3
    if name == "Japan": return 3 + (hfull(65) - 3) * spring(clamp((t - T_JP) / .55))
    if name == "South Korea": return 3 + (hfull(83) - 3) * spring(clamp((t - T_KR) / .55))
    return 3

def block(d, ring, h, top, side):
    for i in range(0, int(h), 3): d.polygon([(x, y - i) for x, y in ring], fill=side)
    d.polygon([(x, y - h) for x, y in ring], fill=top, outline=side)

def tag(d, t, t0, lab, lo, la, dx, L_, f=24):
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
    for name, ring, _ in POLYS:
        h = height(name, t)
        if name == "Japan": top, side = INK, MID
        elif name == "South Korea" and t >= T_KR: top, side = MID, RULE
        else: top, side = WHITE, RULE
        block(d, ring, h, top, side)
    if EP.current(t) == "c1":                                       # tags only while cliché 1 is checked
        if t >= T_JP: tag(d, t, T_JP + .3, "JAPAN 65%", 138, 36, -60, -110)
        if t >= T_KR: tag(d, t, T_KR + .3, "S. KOREA 83%", 127.8, 36.5, -170, 50)

def cam(t):
    def at(lo, la): x, y = proj(lo, la); return (x, y - 40)
    ea = at(126, 36)
    return cam_path(t, [(0, 2.6, at(134, 37)), (S("c1") - .1, 2.6, at(134, 37)), (S("c1") + .7, 2.0, ea), (S("why") - .1, 2.0, ea),
                        (S("why") + .6, 1.6, ea)])

def quote_card(d, t, c):
    """the cliché in quotes, sliding in from the top, with a small CLICHÉ? label"""
    k = spring(clamp((t - T_Q[c]) / .5)); y = 470 + 40 * (1 - k)
    txt = CLICHES[c]; f = F(BLK, 40); w = d.textlength(txt, font=f)
    x0 = 540 - w / 2 - 28
    d.rounded_rectangle([x0, y, x0 + w + 56, y + 96], radius=18, fill=WHITE, outline=INK, width=4)
    d.text((540, y + 60), txt, font=f, fill=INK, anchor="mm")
    d.text((x0 + 18, y + 20), f"CLICHÉ {list(CLICHES).index(c) + 1}?", font=F(MONO, 22), fill=MID, anchor="lm")

def couples(d, t):
    x0, y0 = 70, 860
    d.rounded_rectangle([x0, y0, x0 + 520, y0 + 290], radius=24, fill=WHITE, outline=INK, width=3)
    d.text((x0 + 24, y0 + 30), "10 MARRIED PEOPLE IN JAPAN", font=F(MONO, 22), fill=MID, anchor="lm")
    for i in range(10):
        cx = x0 + 68 + (i % 5) * 96; cy = y0 + 115 + (i // 5) * 100
        apart = i in (1, 3, 5, 7, 8)
        k = ease_io(clamp((t - T_HALF - .2 - i * .08) / .6)) if apart else 0
        g = 15 + 16 * k; col = SIG if apart and k > .5 else INK
        for s in (-1, 1): d.ellipse([cx + s * g - 14, cy - 14, cx + s * g + 14, cy + 14], fill=col)
        if not apart: d.line([(cx - 12, cy), (cx + 12, cy)], fill=INK, width=4)
    if t >= T_HALF + 1.2: d.text((x0 + 24, y0 + 262), "ABOUT HALF: NO SEX IN A MONTH", font=F(BLK, 22), fill=SIG, anchor="lm")

def no_survey(d, t):
    """an empty survey sheet: no representative data"""
    k = spring(clamp((t - T_NOSURVEY) / .5)); x0, y0 = 300, 760 + 40 * (1 - k)
    d.rounded_rectangle([x0, y0, x0 + 480, y0 + 360], radius=18, fill=WHITE, outline=INK, width=4)
    d.text((x0 + 30, y0 + 40), "SURVEY", font=F(BLK, 34), fill=INK, anchor="lm")
    for i in range(4):
        y = y0 + 110 + i * 56
        d.rectangle([x0 + 30, y - 14, x0 + 58, y + 14], outline=MID, width=3)
        d.line([(x0 + 80, y), (x0 + 440, y)], fill=RULE, width=4)
    d.text((x0 + 240, y0 + 330), "NONE FOUND", font=F(MONO, 24), fill=MID, anchor="mm")

def scorecard(d, t):
    """payoff (rule 15): all three verdicts stay to the end"""
    x0, y0 = 120, 860
    d.rounded_rectangle([x0, y0, x0 + 840, y0 + 280], radius=24, fill=WHITE, outline=INK, width=4)
    for i, c in enumerate(CLICHES):
        if t < S("why") + .15 + i * .25: continue
        y = y0 + 55 + i * 85
        d.text((x0 + 30, y), CLICHES[c], font=F(BLK, 30), fill=INK, anchor="lm")
        v = VERDICT[c]; fv = F(BLK, 30); w = d.textlength(v, font=fv)
        d.rounded_rectangle([x0 + 810 - w - 24, y - 26, x0 + 810, y + 26], radius=8, outline=SIG, width=4)
        d.text((x0 + 810 - w / 2 - 12, y), v, font=fv, fill=SIG, anchor="mm")

def labels(d, t):
    cur = EP.current(t)
    if cur == "hook":                                                  # cold open: three quote cards slam in, stamp
        for i, t0 in enumerate(T_HOOK_CARDS):
            if t < t0: continue
            k = spring(clamp((t - t0) / .4)); c = list(CLICHES)[i]; txt = CLICHES[c]
            f = F(BLK, 34); w = d.textlength(txt, font=f); y = 500 + i * 110 - 60 * (1 - k)
            d.rounded_rectangle([540 - w / 2 - 24, y, 540 + w / 2 + 24, y + 80], radius=16, fill=WHITE, outline=INK, width=4)
            d.text((540, y + 42), txt, font=f, fill=INK, anchor="mm")
        if t >= cue("hook", "check") - .1: stamp(d, (760, 1000), "CHECK", t, cue("hook", "check") - .1, size=90)
    if cur in CLICHES:
        quote_card(d, t, cur)
        if cur == "c2" and t >= T_HALF: couples(d, t)
        if cur == "c3" and t >= T_NOSURVEY: no_survey(d, t)
        if t >= T_V[cur]: stamp(d, {"c1": (780, 720), "c2": (800, 760), "c3": (820, 700)}[cur], VERDICT[cur], t, T_V[cur], size=72)
    if cur in ("why", "end"): scorecard(d, t)

def head(d, t, line):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    cur = EP.current(t)
    n = sum(1 for c in CLICHES if t >= T_V[c])
    d.text((X0, 400), "CLICHÉS CHECKED", font=F(MONO, 30), fill=MID)
    d.text((X0 + 330, 388), f"{n} / 3", font=F(BLK, 56), fill=SIG if cur == "c3" else INK)

def draw(img, d, t, line, note="Pew 2026 · JFPA 2023"):
    z, f = cam(t); camera(img, lambda L, dL: scene(L, dL, t), z, f)
    d = ImageDraw.Draw(img); labels(d, t); head(d, t, line); fig(d, note)

def sc_hook(img, d, t): draw(img, d, t, "CLICHÉ CHECK: JAPAN")
def sc_c1(img, d, t): draw(img, d, t, "CLICHÉ 1", note="Pew 2026 · % who call an affair wrong")
def sc_c2(img, d, t): draw(img, d, t, "CLICHÉ 2", note="JFPA 2023 · random sample, ages 16–49")
def sc_c3(img, d, t): draw(img, d, t, "CLICHÉ 3", note="only repeated in articles, never measured")
def sc_why(img, d, t): draw(img, d, t, "GRAIN OF TRUTH.")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.scenes = {"hook": sc_hook, "c1": sc_c1, "c2": sc_c2, "c3": sc_c3, "why": sc_why}
FX = [*[(t0, pop(.1), -.3 + i * .3) for i, t0 in enumerate(T_HOOK_CARDS)], (cue("hook", "check") - .1, thud(.3), .3),
      *[(T_Q[c], whoosh(.3, .025), 0) for c in CLICHES], (T_JP, pop(.1), .3), (T_KR, pop(.1), -.3),
      *[(T_HALF + .2 + i * .16, tick(.012), -.4 + i * .2) for i in range(5)], (S("c3") + .05, thud(.3), 0), (T_NOSURVEY, pop(.1), 0),
      *[(T_V[c], thud(.3), .3) for c in CLICHES], *[(S("why") + .15 + i * .25, tick(.015), -.3 + i * .3) for i in range(3)]]
if __name__ == "__main__": EP.run(FX)
