"""NOT JUST YOU – No. 163 as DOKU (26.11.2026): same story and voice as ep163_light_story (Mary, 1800, one hour of light
= ~5.4 hours of work; today ~0.4 s – Nordhaus 1996), new look after Chris' reference reel (Teotihuacan, @jimswormhole):
real archive pictures from Wikimedia Commons (public domain / CC0 / CC BY, credits in img/credits.json), slow camera,
place/year tag top left, credit line bottom, captions white + gold. Rule 24: dark candle-lit pictures while light is
expensive, brighter pictures from 'turn' on. Rule 12 (doku): the gold PRICE OF LIGHT line (Fouquet & Pearson) runs
over all pictures from 'back' on; it grows big in 'but'. First 3 s (Chris OK 26.11.): Wright's candle painting, camera
pushes in from frame 0, tag ENGLAND · 1800, gold counter 1 HOUR OF LIGHT = 0:00 → 5:24 h WORK.
Chris 26.11.2026: faster (pictures must not stand and wait) – short gaps, extra cut on "bright", stronger camera;
credits small and vertical at the left edge."""
import os, sys, json, math
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from doku import *
from swiss import pop, tick, thud, whoosh, boom, riser
from cute import Timeline
import cute; cute.LOUD = -14                       # new standard 26.11.2026 (Dyatlov reference)
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"cold": .2, "stakes": .85, "back": .15, "detail": .3, "but": .5, "so": .3, "turn": .5, "today": .85, "why": .25},
              pace="loose")
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["cold", "stakes", "back", "detail", "but", "so", "turn", "today", "why", "end"]
EP = DokuEpisode(TL, 163, "MARY'S CANDLE", order=ORDER, img_dir=os.path.join(HERE, "img"), credits=os.path.join(HERE, "img", "credits.json"),
                 sources=("Nordhaus (1996), The History of Lighting ·", "Fouquet & Pearson (2006) via Our World in Data"),
                 music=dict(bpm=70, root=2, prog="minor", audio="doku"),
                 cover=dict(words=["WHAT DID ONE", "HOUR OF LIGHT", "COST?"], kicker="It's 1800."))

T_GAS, T_KERO, T_BULB = cue("turn", "gas") - .15, cue("turn", "kerosene") - .15, cue("turn", "bulb") - .25
EP.shots = [
    Shot("cold", "wright", (.66, .36, 1.55), (.70, .42, 2.05), start=0, tag="ENGLAND · 1800", grade=(.92, .25, 0), flicker=1,
         credit="TWO GIRLS DRESSING A KITTEN BY CANDLELIGHT · J. WRIGHT OF DERBY · PD"),
    Shot("cold", "wright", (.36, .66, 2.3), (.40, .62, 2.7), start=cue("cold", "bright") - .1, tag="ENGLAND · 1800", grade=(.95, .25, 0),
         flicker=1, credit="TWO GIRLS DRESSING A KITTEN BY CANDLELIGHT · J. WRIGHT OF DERBY · PD"),
    Shot("stakes", "sewing", (.44, .42, 1.05), (.36, .36, 1.4), tag="MARY · ILLUSTRATIVE", grade=(1.0, .2, 0), flicker=1,
         credit="WOMAN BY CANDLELIGHT · P. C. VAN SLINGELANDT · PUBLIC DOMAIN"),
    Shot("back", "chandler", (.12, .5, 1.0), (.48, .5, 1.12), tag="TALLOW CANDLES · 1700s", grade=(.86, 0, .75),
         credit="CANDLE MAKERS' WORKSHOP · WELLCOME COLLECTION · CC BY 4.0"),
    Shot("detail", "wright", (.50, .50, 1.1), (.46, .52, 1.45), tag="ABOUT 80 CANDLES · ONE ROOM", grade=(.95, .25, 0), flicker=1.4,
         credit="TWO GIRLS DRESSING A KITTEN BY CANDLELIGHT · J. WRIGHT OF DERBY · PD"),
    Shot("but", "chandler", (.62, .5, 1.12), (.80, .5, 1.2), tag="PRICE OF LIGHT · ENGLAND", grade=(.34, 0, .85),
         credit="PRICE OF LIGHT · FOUQUET & PEARSON (2006) · OUR WORLD IN DATA"),
    Shot("so", "angelus", (.50, .45, 1.0), (.56, .47, 1.1), tag="EVENING · 1859", grade=(.85, .3, 0),
         credit="THE ANGELUS · JEAN-FRANÇOIS MILLET · PUBLIC DOMAIN"),
    Shot("turn", "gas", (.30, .55, 1.0), (.40, .55, 1.08), start=S("turn") - .05, tag="LONDON · 1809 · GAS", grade=(.92, .15, 0),
         credit="A PEEP AT THE GAS LIGHTS IN PALL-MALL · T. ROWLANDSON · CC0"),
    Shot("turn", "backer", (.62, .52, 1.0), (.62, .50, 1.1), start=T_KERO, tag="NORWAY · 1890 · OIL LAMP", grade=(1.0, .15, 0),
         credit="BY LAMPLIGHT · HARRIET BACKER · PUBLIC DOMAIN"),
    Shot("turn", "edison", (.5, .40, 1.0), (.5, .36, 1.18), start=T_BULB, tag="U.S. PATENT · 1880 · BULB", grade=(.95, .45, .3),
         credit="ELECTRIC-LAMP, PATENT 223,898 · T. A. EDISON · PUBLIC DOMAIN"),
    Shot("today", "night", (.5, .5, 1.45), (.47, .44, 1.75), mode="fit", tag="EARTH · TODAY", grade=(1.25, 0, 0),
         credit="EARTH AT NIGHT · NASA EARTH OBSERVATORY · PUBLIC DOMAIN"),
    Shot("why", "sewing", (.40, .38, 1.15), (.40, .38, 1.15), tag="1800 VS. TODAY", grade=(1.12, .2, 0), flicker=.6,
         credit="WOMAN BY CANDLELIGHT · P. C. VAN SLINGELANDT · PUBLIC DOMAIN"),
]
# the 'turn' gas shot starts the beat; the oil-lamp and bulb pictures cut in on their words
EP.accent = {"cold": ["eighteen hundred", "one hour"], "stakes": ["six hours"], "back": ["animal fat"], "detail": ["eighty", "All at once"],
             "but": ["five hundred years"], "so": ["sunset"], "turn": ["gas kerosene light bulb"],
             "today": ["half second"], "why": ["Six hours", "Half second"]}
EP.payoff = (S("why") + .1, 1.22)

# ---- the work counter (first 3 s → 'stakes') and its return in 'today' / 'why' --------------------------------
HOURS = 5.4
T_C0, T_C1 = 1.6, cue("stakes", "work") + .2
T_SHRINK = cue("today", "less") - .1
EP.counter_list = [(T_C0, T_C1 - T_C0, HOURS)]

def hm(h):
    m = int(round(h * 60)); return f"{m // 60}:{m % 60:02d} h"

def work_counter(img, d, t):
    if T_C0 - .2 <= t < S("back") - .1:
        k = clamp((t - T_C0 + .2) / .3); kout = clamp((S("back") - .1 - t) / .25)
        a = min(k, kout)
        if a <= 0: return
        tag(img, d, "1 HOUR OF LIGHT =", a, y=330)
        v = HOURS * ease_io(clamp((t - T_C0) / (T_C1 - T_C0)))
        text_shadow(img, (60, 400), hm(v), F(BLK, 190), GOLD if t >= T_C1 else WHITE, blur=14, strength=220)
        text_shadow(img, (66, 610), "OF WORK", F(MONO, 40), (230, 215, 185))
        if t >= T_C1:                                                    # the plant: ≈ 6 HOURS (returns in 'why')
            ks = ease((t - T_C1) / .18); sz = int(64 * (1 + .5 * (1 - ks)))
            f = F(BLK, sz); w = d.textlength("≈ 6 HOURS", font=f)
            d.rectangle([66, 680, 66 + w + 40, 680 + sz * 1.25], outline=GOLD, width=6)
            d.text((86, 680 + sz * .62), "≈ 6 HOURS", font=f, fill=GOLD, anchor="lm")
    elif S("today") - .1 <= t < S("why") - .05:
        tag(img, d, "THE SAME LIGHT, TODAY =", clamp((t - S("today") + .1) / .3), y=330)
        if t < T_SHRINK: txt, col = hm(HOURS), WHITE
        else:
            u = ease_io(clamp((t - T_SHRINK) / 1.3)); sec = HOURS * 3600 * (1 - u) ** 5 + .43 * u
            if sec >= 60: txt = f"{int(sec // 3600)}:{int(sec % 3600 // 60):02d}:{int(sec % 60):02d}"
            else: txt = f"{sec:.1f} s"
            col = GOLD if u >= 1 else WHITE
        text_shadow(img, (60, 400), txt, F(BLK, 190), col, blur=14, strength=220)
        text_shadow(img, (66, 610), "OF WORK", F(MONO, 40), (230, 215, 185))
    elif t >= S("why") - .05:
        k = ease((t - S("why") + .05) / .35)
        for i, (who, val, col) in enumerate((("MARY · 1800", "≈ 6 HOURS", WHITE), ("YOU · TODAY", "0.4 SEC", GOLD))):
            y = 340 + i * 230; dx = (1 - k) * (-60 if i == 0 else 60)
            text_shadow(img, (60 + dx, y), who, F(MONO, 36), (230, 215, 185))
            text_shadow(img, (60 + dx, y + 44), val, F(BLK, 150), col, blur=14, strength=220)

# ---- the continuous gold element: PRICE OF LIGHT, England 1300–2006 (Fouquet & Pearson, log) -------------------
FQ = {int(k): v for k, v in json.load(open(os.path.join(HERE, "fouquet.json"))).items()}; FY = sorted(FQ)
T_Y0, T_Y1 = S("back"), E("but") + .6
T_TURN = S("turn"); T_Y2 = E("turn") + .8
BAND = (90, 1290, 990, 1388); BIG = (110, 470, 970, 1010)

def year_at(t):
    if t < T_Y0: return 1300
    if t < T_Y1: return 1300 + 500 * ease_io(clamp((t - T_Y0) / (T_Y1 - T_Y0)))
    if t < T_TURN: return 1800
    return 1800 + 206 * ease_io(clamp((t - T_TURN) / (T_Y2 - T_TURN)))

def chart_box(t):
    kb = ease_io(clamp((t - S("but") + .05) / .45)) - ease_io(clamp((t - S("so") + .05) / .5))
    return tuple(lerp(a, b, kb) for a, b in zip(BAND, BIG)), kb

def price_line(img, d, t):
    if t < T_Y0 - .3: return
    a = ease(clamp((t - T_Y0 + .3) / .4))
    (x0, y0, x1, y1), kb = chart_box(t)
    if t >= S("why") - .05: return                                       # the payoff picture stays clean
    ov = Image.new("L", (int(x1 - x0 + 40), int(y1 - y0 + 70)), int((120 + 60 * kb) * a))
    img.paste(Image.new("RGB", ov.size, SHADE), (int(x0 - 20), int(y0 - 50)), ov)
    lo, hi = math.log10(2), math.log10(40000); yr = year_at(t)
    def P(y, v): return x0 + (y - 1300) / 706 * (x1 - x0), y1 - (math.log10(v) - lo) / (hi - lo) * (y1 - y0)
    fl = F(MONO, int(lerp(20, 30, kb)))
    d.text((x0, y0 - 28), "PRICE OF LIGHT · ENGLAND · LOG SCALE", font=fl, fill=mix(SHADE, (205, 190, 160), a), anchor="lm")
    d.line([(x0, y1), (x1, y1)], fill=mix(SHADE, GOLD_D, a), width=2)
    for yy in (1300, 1500, 1700, 1900, 2000):
        px = P(yy, 2)[0]; d.line([(px, y1), (px, y1 + 8)], fill=mix(SHADE, GOLD_D, a), width=2)
        if kb > .5 or yy in (1300, 2000): d.text((px, y1 + 22), str(yy), font=F(MONO, int(lerp(18, 24, kb))), fill=mix(SHADE, (170, 155, 125), a), anchor="mm")
    pts = [P(y, FQ[y]) for y in FY if y <= yr]
    if len(pts) > 1: d.line(pts, fill=mix(SHADE, GOLD, a), width=int(lerp(4, 7, kb)), joint="curve")
    if pts:
        x, y = pts[-1]; r = lerp(7, 12, kb) * (1 + .25 * math.sin(t * 9))
        d.ellipse([x - r * 2, y - r * 2, x + r * 2, y + r * 2], outline=mix(SHADE, GOLD_D, a), width=2)
        d.ellipse([x - r, y - r, x + r, y + r], fill=mix(SHADE, GOLD, a))
        d.text((min(x + 26, x1 - 10), y - 30), f"{int(yr)}", font=F(BLK, int(lerp(34, 64, kb))), fill=mix(SHADE, WHITE, a),
               anchor="rm" if x > x1 - 120 else "lm")

    if kb > .6 and yr >= 1650:                                           # 'but': say what the line shows (rule 15)
        k = ease(clamp((yr - 1650) / 80)) * clamp((kb - .6) / .4)
        text_shadow(img, ((x0 + x1) / 2, y0 + (y1 - y0) * .62), "500 YEARS.", F(BLK, 96), mix(SHADE, WHITE, k), anchor="mm", blur=12)
        text_shadow(img, ((x0 + x1) / 2, y0 + (y1 - y0) * .62 + 100), "NO CHANGE.", F(BLK, 96), mix(SHADE, GOLD, k), anchor="mm", blur=12)

T_SUNSET = cue("so", "sunset") - .05
def dusk(img, t):
    """'so': on 'sunset' the evening picture goes dark (rule 24 – light tells the story)"""
    if T_SUNSET <= t < S("turn") - .05:
        a = int(170 * ease_io(clamp((t - T_SUNSET) / 1.2)))
        img.paste(Image.new("RGB", img.size, (6, 5, 12)), (0, 0), Image.new("L", img.size, a))

def overlay(img, d, t):
    price_line(img, d, t); work_counter(img, d, t)
EP.overlay = overlay
EP.under = dusk

def t_year(y, a, b):
    """first time in [a, b] at which the price line reaches year y"""
    for i in range(400):
        t = a + (b - a) * i / 399
        if year_at(t) >= y: return t
    return b
T_FLAT = t_year(1650, T_Y0, T_Y1)                       # '500 YEARS. NO CHANGE.' appears
T_1900, T_NOW = t_year(1900, T_TURN, T_Y2), t_year(2005, T_TURN, T_Y2)

FX = [(T_SUNSET, whoosh(1.2, .02), -.4), (T_FLAT, thud(.22), 0), (T_Y1, tick(.03), 0), (T_1900, tick(.03), 0), (T_NOW, pop(.1), .2),
      (0.0, whoosh(.6, .02), -.2), (T_C0, tick(.012), -.3), (T_C1, thud(.28), 0), (S("but") - .05, whoosh(.5, .03), 0),
      (T_GAS, pop(.08), .2), (T_KERO, pop(.08), .2), (T_BULB, pop(.12), .2), (T_SHRINK, whoosh(.6, .02), -.3),
      (S("why") - .05, boom(.35), 0)] + EP.cut_fx(.06)
if __name__ == "__main__": EP.run(FX)
