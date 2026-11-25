"""NOT JUST YOU – No. 163: the price of light as a STORY (first 'story' episode, 25.11.2026, after Chris' reference
'diver at Boesmansgat': cold open on the climax, a stakes line, one character, But/So, plant & payoff, light tells the story).
Mary (illustrative) in 1800 wants one hour of modern-bulb light (1,000 lumen-hours): ~5.4 hours of work (Nordhaus 1996);
today 0.00012 h = 0.43 s. The wall picture: price of light in the UK 1301–2006 (Fouquet & Pearson, log).
ONE world: Mary's room in cross-section. Candle-lit and DARK while light is expensive (rule 24), then the world turns
LIGHT at 'Then came gas lamps…'. Top of the frame: two bars, LIGHT 1 h vs WORK 5.4 h -> 0.4 s. Payoff (rule 15): bright room,
tiny work bar, 'six hours' (planted in 'stakes') returns in 'why' (rule 23)."""
import os, sys, json, math
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from fx2 import light_look
from stand import payoff_cam, stamp_box
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"cold": .8, "stakes": 1.4, "back": 1.5, "but": 4.4, "so": 1.8, "turn": 4.8, "today": 1.2, "why": .2},
              pace="loose")
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["cold", "stakes", "back", "but", "so", "turn", "today", "why", "end"]
EP = ThreadEpisode(TL, 163, "MARY'S CANDLE", order=ORDER, dark=True, label="STORY · NORDHAUS 1996 · FOUQUET & PEARSON",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Nordhaus (1996), The History of Lighting ·", "Fouquet & Pearson (2006) via Our World in Data"),
                   music=dict(bpm=84, root=2, prog="minor", kick="four", audio="v5"),
                   cover=dict(words=["ONE HOUR OF", "LIGHT = SIX", "HOURS OF WORK."], kicker="It's 1800."))
light_look(EP, ORDER, reveal=())
for k in ("cold", "stakes", "back", "but", "so"): EP.bg[k] = "dark"          # rule 24: candle-lit while light is expensive

def inv(c):
    """dark scenes are lightness-inverted by the pipeline -> pre-invert colours that must look a certain way there"""
    m, n = max(c), min(c); return tuple(int(v + 255 - m - n) for v in c)
def dark(t): return EP.bg_of(EP.current(t)) == "dark"
def C(c, t): return inv(c) if dark(t) else c

FQ = {int(k): v for k, v in json.load(open(os.path.join(HERE, "fouquet.json"))).items()}; FY = sorted(FQ)
WARM, SKY_N, SKY_D, WOOD = (255, 206, 120), (28, 36, 64), (170, 210, 245), (150, 110, 70)
FLOOR = 1150

T_CANDLE = .15; T_WORK0, T_WORK1 = cue("stakes", "cost") - .1, E("stakes") + .9
T_Y0, T_Y1 = S("back"), E("but") + 3.2                          # wall chart 1300 -> 1800 (flat)
T_SUN = S("so") + .1
T_TURN = S("turn"); T_GAS, T_KERO, T_BULB = cue("turn", "gas") - .1, cue("turn", "kerosene") - .1, cue("turn", "bulb") - .1
T_Y2 = E("turn") + 3.6                                          # wall chart 1800 -> 2006 (plunge)
T_SHRINK = cue("today", "less") - .1; T_PAY = S("why")

def year_at(t):
    if t < T_Y0: return 1300
    if t < T_Y1: return 1300 + 500 * ease_io(clamp((t - T_Y0) / (T_Y1 - T_Y0)))
    if t < T_TURN: return 1800
    return 1800 + 206 * ease_io(clamp((t - T_TURN) / (T_Y2 - T_TURN)))

def lamp(t):
    if t < T_GAS: return "candle"
    if t < T_KERO: return "gas"
    if t < T_BULB: return "kerosene"
    return "bulb"

def glow(img, x, y, r, col, a, t):
    """warm light pool (pre-inverted in dark scenes)"""
    if a <= 0: return
    Y, X = np.ogrid[:img.size[1], :img.size[0]]
    m = np.clip(1 - np.sqrt((X - x) ** 2 + (Y - y) ** 2) / r, 0, 1) ** 1.6 * a
    base = np.asarray(img, np.float32); c = np.array(C(col, t), np.float32)
    img.paste(Image.fromarray(np.clip(base * (1 - m[..., None]) + c * m[..., None], 0, 255).astype(np.uint8)))

def room(img, t):
    d = ImageDraw.Draw(img); dk = dark(t)
    # window: night while dark (and the sun sets in 'so'), day once light is cheap
    wx0, wy0, wx1, wy1 = 90, 640, 300, 880
    sky = SKY_N if dk else SKY_D
    if dk and t >= T_SUN - 1.2 and t < T_TURN: sky = SKY_N
    d.rectangle([wx0, wy0, wx1, wy1], fill=C(sky, t), outline=C((90, 80, 70), t), width=8)
    d.line([((wx0 + wx1) / 2, wy0), ((wx0 + wx1) / 2, wy1)], fill=C((90, 80, 70), t), width=6)
    d.line([(wx0, (wy0 + wy1) / 2), (wx1, (wy0 + wy1) / 2)], fill=C((90, 80, 70), t), width=6)
    if dk:                                                                    # moon / setting sun in 'so'
        if EP.current(t) == "so":
            u = ease_io(clamp((t - T_SUN) / 1.6)); sy = wy0 + 60 + 170 * u
            d.ellipse([200 - 26, sy - 26, 200 + 26, sy + 26], fill=C((255, 150, 60), t))
        else: d.ellipse([230, 680, 262, 712], fill=C((240, 240, 220), t))
    d.line([(40, FLOOR), (1040, FLOOR)], fill=C((120, 110, 100), t), width=4)
    d.rectangle([380, 1000, 800, 1020], fill=C(WOOD, t)); d.rectangle([400, 1020, 418, FLOOR], fill=C(WOOD, t)); d.rectangle([762, 1020, 780, FLOOR], fill=C(WOOD, t))
    # Mary, seated, sewing (illustrative)
    mx = 470; col = C((70, 70, 80), t)
    d.ellipse([mx - 32, 840, mx + 32, 904], fill=col)
    d.rounded_rectangle([mx - 44, 904, mx + 44, 1040], radius=20, fill=col)
    d.line([(mx + 30, 940), (mx + 110, 990)], fill=col, width=18)
    d.rectangle([mx - 50, 1040, mx + 40, 1060], fill=C(WOOD, t)); d.rectangle([mx - 46, 1060, mx - 34, FLOOR], fill=C(WOOD, t))
    d.rectangle([mx + 100, 985, mx + 190, 1000], fill=C((220, 210, 190), t))          # the cloth
    d.text((mx, 820), "MARY", font=F(MONO, 22), fill=C((120, 120, 130), t), anchor="mm")
    # the light source on the table
    lx, ly = 680, 1000; L = lamp(t); fl = 1 + .12 * math.sin(t * 21) + .08 * math.sin(t * 33)
    if L == "candle":
        k = spring(clamp((t - T_CANDLE) / .5))
        d.rectangle([lx - 12, ly - 70, lx + 12, ly], fill=C((235, 225, 200), t))
        if k > 0:
            d.ellipse([lx - 10 * fl * k, min(ly - 110 * fl * k, ly - 74), lx + 10 * fl * k, ly - 72], fill=C(WARM, t))
            d.ellipse([lx - 4 * k, min(ly - 96 * k, ly - 78), lx + 4 * k, ly - 76], fill=C((255, 250, 220), t))
    elif L == "gas":
        d.rectangle([lx - 6, ly - 120, lx + 6, ly], fill=C((90, 90, 90), t)); d.ellipse([lx - 22, ly - 160, lx + 22, ly - 116], fill=C((200, 230, 255), t))
    elif L == "kerosene":
        d.polygon([(lx - 30, ly), (lx + 30, ly), (lx + 18, ly - 50), (lx - 18, ly - 50)], fill=C((160, 120, 60), t))
        d.ellipse([lx - 24, ly - 120, lx + 24, ly - 46], outline=C((150, 150, 150), t), width=4); d.ellipse([lx - 8, ly - 98, lx + 8, ly - 64], fill=C(WARM, t))
    else:
        d.line([(lx, 520), (lx, ly - 150)], fill=C((90, 90, 90), t), width=3); d.ellipse([lx - 30, ly - 160, lx + 30, ly - 100], fill=C((255, 245, 200), t))
    # the light pool: small while expensive, the whole room once cheap
    if L == "candle": glow(img, lx, ly - 90, 300 * fl, WARM, .55 * spring(clamp((t - T_CANDLE) / .5)), t)
    elif L == "gas": glow(img, lx, ly - 140, 420, (220, 235, 255), .35, t)
    elif L == "kerosene": glow(img, lx, ly - 80, 520, WARM, .35, t)
    else: glow(img, lx, ly - 130, 900, (255, 248, 225), .45, t)

def wall_chart(img, t):
    """the price of light on the wall (Fouquet & Pearson, UK, log)"""
    d = ImageDraw.Draw(img); x0, y0, x1, y1 = 820, 700, 1030, 900
    yr = year_at(t)
    if t < T_Y0 - .3: return
    k = ease(clamp((t - T_Y0 + .3) / .4))
    d.rectangle([x0 - 10, y0 - 40, x1 + 10, y1 + 34], fill=C((235, 228, 214), t), outline=C((120, 100, 80), t), width=5)
    d.text(((x0 + x1) / 2, y0 - 20), "PRICE OF LIGHT", font=F(MONO, 18), fill=C((90, 80, 70), t), anchor="mm")
    lo, hi = math.log10(2), math.log10(40000)
    def P(y, v): return x0 + (y - 1300) / 706 * (x1 - x0), y1 - (math.log10(v) - lo) / (hi - lo) * (y1 - y0)
    pts = [P(y, FQ[y]) for y in FY if y <= yr]
    if len(pts) > 1: d.line(pts, fill=C((230, 90, 40), t), width=3)
    if pts: d.ellipse([pts[-1][0] - 5, pts[-1][1] - 5, pts[-1][0] + 5, pts[-1][1] + 5], fill=C((230, 90, 40), t))
    d.text(((x0 + x1) / 2, y1 + 18), f"{int(yr)}", font=F(BLK, 22), fill=C((90, 80, 70), t), anchor="mm")

def bars(img, t):
    """LIGHT 1 h vs WORK 5.4 h -> 0.43 s"""
    d = ImageDraw.Draw(img); x0, unit = 260, 108
    if t < T_WORK0 - .4: return
    d.text((x0 - 20, 530), "1 h LIGHT", font=F(MONO, 24), fill=C((120, 120, 120), t), anchor="rm")
    d.rectangle([x0, 514, x0 + unit, 546], fill=C(WARM, t))
    d.text((x0 - 20, 590), "WORK", font=F(MONO, 24), fill=C((120, 120, 120), t), anchor="rm")
    if t < T_SHRINK: w = 5.4 * unit * ease_io(clamp((t - T_WORK0) / (T_WORK1 - T_WORK0))); lab = f"{5.4 * w / (5.4 * unit):.1f} HOURS"
    else:
        u = ease_io(clamp((t - T_SHRINK) / 1.2)); w = max(3, 5.4 * unit * (1 - u)); lab = "0.4 SECONDS" if u > .95 else f"{5.4 * (1 - u):.1f} HOURS"
    d.rectangle([x0, 574, x0 + w, 606], fill=C(SIG, t))
    for i in range(1, 6):                                                         # hour ticks
        if x0 + i * unit < x0 + w: d.line([(x0 + i * unit, 574), (x0 + i * unit, 606)], fill=C((255, 255, 255), t), width=2)
    d.text((x0 + w + 16, 590), lab, font=F(BLK, 30), fill=C(SIG, t), anchor="lm")

def head(d, t, line, label, val, hot=False):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    d.text((X0, 400), label, font=F(MONO, 30), fill=MID)
    d.text((X0 + d.textlength(label, font=F(MONO, 30)) + 24, 388), val, font=F(BLK, 56), fill=SIG if hot else INK)

LINES = {"cold": ("1800. ONE HOUR.", "LIGHT WANTED", "1 HOUR"), "stakes": ("SIX HOURS OF WORK.", "COST", "≈5.4 h"),
         "back": ("CANDLES.", "MADE OF", "ANIMAL FAT"), "but": ("500 YEARS. NO CHANGE.", "PRICE OF LIGHT", "FLAT"),
         "so": ("SUNSET = BEDTIME.", "EVENINGS", "DARK"), "turn": ("THEN: GAS, OIL, BULB.", "PRICE OF LIGHT", "FALLING"),
         "today": ("TODAY: HALF A SECOND.", "COST", "0.4 s"), "why": ("6 HOURS = 0.4 SECONDS.", "MARY VS. YOU", "×45,000")}

def sc_full(img, d, t):
    cur = EP.current(t)
    room(img, t); wall_chart(img, t); bars(img, t); d = ImageDraw.Draw(img)
    if T_WORK1 - .4 <= t < S("back") + .2: stamp_box(d, (760, 760), "6 HOURS", t, T_WORK1 - .4, size=70)
    line, lab, val = LINES.get(cur, LINES["why"]); head(d, t, line, lab, val, cur in ("stakes", "today", "why"))
    fig(d, "Mary is illustrative · 1 h of light = 1,000 lumen-hours (one modern bulb)")

def sc(img, d, t):
    payoff_cam(img, lambda L, dL: sc_full(L, dL, t), t, T_PAY, focus=(560, 760), z1=1.12, ep=EP)

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.scenes = {k: sc for k in ORDER[:-1]}
FX = [(T_CANDLE, pop(.08), .2), (T_WORK0, tick(.012), -.4), (T_WORK1 - .4, thud(.22), 0), (T_Y0, whoosh(.5, .02), .4), (T_SUN, whoosh(.8, .015), -.5),
      (T_TURN, thud(.25), 0), (T_GAS, pop(.08), .2), (T_KERO, pop(.08), .2), (T_BULB, pop(.12), .2), (T_SHRINK, whoosh(.6, .02), -.3)]
if __name__ == "__main__": EP.run(FX)
