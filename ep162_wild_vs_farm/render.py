"""NOT JUST YOU – No. 162: all wild land mammals vs. all farm animals ('pour test' riddle, 25.11.2026).
Greenspoon et al. (2023, PNAS): wild land mammals ~20 Mt, domesticated mammals ~630 Mt (x30). 20 Mt / 8.2 bn = 2.4 kg/person.
Riddle structure (rule 17), dark look. ONE scene: two sand heaps on the ground, WILD (green) and FARM (orange); the area of a
heap is proportional to its mass (self-similar pile). Both pour at the same tonnes per second: the wild heap is done almost at
once, the farm heap keeps growing. Payoff (rule 15): tiny green heap next to the huge orange one, x30."""
import os, sys, math
import numpy as np
from PIL import ImageDraw
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from stand import stamp_box, dashed, payoff_cam
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .4, "rules": .4, "lock": .7, "gut": .5, "reveal": .85, "pour": .5, "why": .1}, pace="loose")
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "rules", "lock", "gut", "reveal", "pour", "why", "end"]
EP = ThreadEpisode(TL, 162, "WILD VS. FARM", order=ORDER, dark=True, label="RIDDLE · GREENSPOON ET AL. 2023 · PNAS",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Greenspoon et al. (2023), The global biomass", "of wild mammals, PNAS · wet mass"),
                   music=dict(bpm=96, root=9, prog="major", kick="four", audio="v5"),
                   cover=dict(words=["WILD ANIMALS", "VS. FARM ANIMALS.", "WHICH WEIGHS MORE?"], kicker="Lock in your answer."))

GREEN, FARM = (96, 190, 100), (232, 120, 70)
GY = 1120; W_MT, F_MT = 20, 630
FW, FH, FCX = 640, 400, 660                                  # full farm heap
WCX = 190
def size(mt): k = math.sqrt(mt / F_MT); return FW * k, FH * k

T_W = [cue("rules", w) - .1 for w in ("Elephants", "deer", "wolves", "mice")]; T_F = [cue("rules", w) - .1 for w in ("Cows", "pigs", "sheep")]
T_LOCK = S("lock"); T_321 = [cue("lock", "Three") - .05, cue("lock", "Two") - .05, cue("lock", "One") - .05]
T_GUT = S("gut"); T_X30 = cue("reveal", "thirty") - .15; T_P0 = T_GUT + .5; T_P1 = T_X30 - .05; T_KG = cue("pour", "two and a half") - .15
RATE = F_MT / (T_P1 - T_P0)                                   # tonnes per second, the same for both

def mass(which, t):
    if t < T_P0: return 0
    m = RATE * (t - T_P0); return min(m, W_MT if which == "w" else F_MT)

def heap(d, cx, mt, col, t, seed):
    if mt <= 0: return 0
    w, h = size(mt); xs = np.linspace(cx - w / 2, cx + w / 2, 60)
    pts = [(x, GY - h * (1 - ((x - cx) / (w / 2)) ** 2)) for x in xs]
    d.polygon(pts + [(cx + w / 2, GY), (cx - w / 2, GY)], fill=col)
    R = np.random.RandomState(seed * 1000 + int(t * 8))                  # sandy texture, it glitters (rule 13)
    for _ in range(int(40 + w * h / 400)):
        x = R.uniform(cx - w / 2, cx + w / 2); top = GY - h * (1 - ((x - cx) / (w / 2)) ** 2); y = R.uniform(top + 3, GY - 2)
        d.point((x, y), fill=mix(col, (255, 255, 255), .35))
    return GY - h

def stream(d, cx, top, col, t, on):
    if not on: return
    R = np.random.RandomState(int(t * 30) + int(cx))
    for _ in range(120):
        u = R.uniform(); x = cx + R.normal(0, 4 + 10 * u); y = 470 + (top - 470) * u
        d.rectangle([x - 1.5, y - 1.5, x + 1.5, y + 1.5], fill=col)

def countdown(d, t):
    if not (T_LOCK <= t < S("gut")): return
    d.rounded_rectangle([290, 640, 790, 1040], radius=40, fill=BG)
    d.text((540, 690), "LOCK IN YOUR ANSWER", font=F(BLK, 38), fill=INK, anchor="mm")
    i = sum(1 for x in T_321 if t >= x)
    ring = clamp((t - T_321[0]) / (T_321[2] + .7 - T_321[0])) if t >= T_321[0] else 0
    d.ellipse([420, 750, 660, 990], outline=mix(BG, MID, .6), width=12)
    if ring > 0: d.arc([420, 750, 660, 990], -90, -90 + 360 * (1 - ring), fill=SIG, width=12)
    else: a0 = (t * 300) % 360; d.arc([420, 750, 660, 990], a0, a0 + 50, fill=SIG, width=12)           # rule 13: spinner until "Three"
    d.text((540, 870), ["?", "3", "2", "1"][i], font=F(BLK, 130), fill=INK, anchor="mm")

def head(d, line, label=None, val=None, hot=False):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    if label:
        d.text((X0, 400), label, font=F(MONO, 30), fill=MID)
        d.text((X0 + d.textlength(label, font=F(MONO, 30)) + 24, 388), val, font=F(BLK, 56), fill=SIG if hot else INK)

def lists(d, t):
    if t >= T_LOCK: return
    for i, (w, t0) in enumerate(zip(("ELEPHANTS", "DEER", "WOLVES", "MICE"), T_W)):
        if t >= t0: d.text((WCX, 700 + i * 44), w, font=F(BLK, 34), fill=mix(BG, GREEN, ease(clamp((t - t0) / .25))), anchor="mm")
    for i, (w, t0) in enumerate(zip(("COWS", "PIGS", "SHEEP"), T_F)):
        if t >= t0: d.text((FCX, 700 + i * 44), w, font=F(BLK, 34), fill=mix(BG, FARM, ease(clamp((t - t0) / .25))), anchor="mm")

def sc(img, d, t):
    payoff_cam(img, lambda L, dL: sc_full(L, dL, t), t, S("why"), focus=(540, 900), z1=1.12)

T_OUT = S("rules") - .2                                           # 25.11.2026 (rule 11): elephant vs cow on a seesaw
def seesaw(d, t):
    o = 1 - ease_io(clamp((t - T_OUT) / .4)) if t >= T_OUT else 1
    if o <= 0: return
    k = spring(clamp((t - .1) / .5)); a = math.radians(9 * math.sin(t * 3.2) * min(1, t / .8))
    px, py = 540, 1040; L_ = 420 * k
    def rot(x, y): return px + x * math.cos(a) - y * math.sin(a), py + x * math.sin(a) + y * math.cos(a)
    d.polygon([(px - 40, GY), (px + 40, GY), (px, py)], fill=mix(BG, MID, .6 * o))
    d.line([rot(-L_, 0), rot(L_, 0)], fill=mix(BG, INK, o), width=10)
    ex, ey = rot(-L_ * .62, -70 * k)                                                  # elephant: body, head, trunk, legs
    d.ellipse([ex - 90 * k, ey - 60 * k, ex + 90 * k, ey + 60 * k], fill=mix(BG, GREEN, o)); d.ellipse([ex - 140 * k, ey - 70 * k, ex - 60 * k, ey + 10 * k], fill=mix(BG, GREEN, o))
    d.line([(ex - 130 * k, ey - 10 * k), (ex - 150 * k, ey + 60 * k)], fill=mix(BG, GREEN, o), width=max(2, int(16 * k)))
    cx_, cy_ = rot(L_ * .62, -55 * k)                                                 # cow: body, head, legs
    d.rounded_rectangle([cx_ - 85 * k, cy_ - 40 * k, cx_ + 75 * k, cy_ + 30 * k], radius=int(14 * k), fill=mix(BG, FARM, o))
    d.rounded_rectangle([cx_ + 65 * k, cy_ - 70 * k, cx_ + 115 * k, cy_ - 15 * k], radius=int(10 * k), fill=mix(BG, FARM, o))
    for lx in (-70, -40, 40, 60): d.line([(cx_ + lx * k, cy_ + 28 * k), (cx_ + lx * k, cy_ + 52 * k)], fill=mix(BG, FARM, o), width=max(2, int(10 * k)))
    if 1.2 <= t < T_OUT: stamp_box(d, (540, 700), "WHICH IS HEAVIER?", t, 1.2, size=60)

def sc_full(img, d, t):
    cur = EP.current(t)
    seesaw(d, t)
    d.line([(40, GY), (1040, GY)], fill=mix(BG, MID, .5), width=3)
    d.text((WCX, GY + 34), "WILD", font=F(BLK, 30), fill=GREEN, anchor="mm"); d.text((FCX, GY + 34), "FARM", font=F(BLK, 30), fill=FARM, anchor="mm")
    mw, mf = mass("w", t), mass("f", t)
    if T_OUT <= t < T_P0:
        for cx in (WCX, FCX):
            d.text((cx, 1010 + 14 * math.sin(t * 5 + cx)), "?", font=F(BLK, 110), fill=mix(BG, MID, .55 + .25 * math.sin(t * 4)), anchor="mm")
    tw = heap(d, WCX, mw, GREEN, t, 1); tf = heap(d, FCX, mf, FARM, t, 2)
    stream(d, WCX, tw or GY, GREEN, t, T_P0 <= t and mw < W_MT); stream(d, FCX, tf or GY, FARM, t, T_P0 <= t and mf < F_MT)
    if t >= T_P0:
        d.text((WCX, (tw or GY) - 40), f"{mw:.0f} Mt", font=F(BLK, 30), fill=GREEN, anchor="mm")
        d.text((FCX, (tf or GY) - 40), f"{mf:.0f} Mt", font=F(BLK, 34), fill=FARM, anchor="mm")
    if T_GUT <= t < T_X30:                                                      # the gut answer points at the wild side
        y = 860 + 14 * math.sin((t - T_GUT) * 10)
        d.polygon([(WCX - 22, y - 30), (WCX + 22, y - 30), (WCX, y)], fill=SIG); d.text((WCX, y - 60), "THE WILD?", font=F(BLK, 32), fill=SIG, anchor="mm")
    if t >= T_P1:                                                               # rule 13: sand keeps sliding down the heaps
        for cx, mt, col, n in ((FCX, F_MT, FARM, 70), (WCX, W_MT, GREEN, 10)):
            w, h = size(mt)
            for j in range(n):
                u = ((t - T_P1) * .35 + j / n) % 1; side = 1 if j % 2 else -1
                x = cx + side * (w / 2) * u ** .8 * .98; y = GY - h * (1 - ((x - cx) / (w / 2)) ** 2) - 5
                d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=mix(col, (255, 255, 255), .45))
    if t >= T_KG:                                                               # a 2.5 kg weight drops next to the wild heap
        k = spring(clamp((t - T_KG) / .5)); x, y = WCX, GY - 230 - (1 - k) * 300
        d.polygon([(x - 46, y + 58), (x + 46, y + 58), (x + 30, y), (x - 30, y)], fill=mix(BG, INK, .85)); d.ellipse([x - 18, y - 22, x + 18, y + 6], outline=mix(BG, INK, .85), width=6)
        d.text((x, y + 32), "2.5 kg", font=F(BLK, 26), fill=BG, anchor="mm"); d.text((x, y + 86), "PER PERSON", font=F(MONO, 20), fill=GREEN, anchor="mm")
    lists(d, t); countdown(d, t)
    if t >= T_X30: stamp_box(d, (420, 610), "×30", t, T_X30, size=110)
    if cur == "hook": head(d, "WHICH IS HEAVIER?", "WILD VS. FARM", "?")
    elif cur == "rules": head(d, "WILD VS. FARM.", "LAND MAMMALS", "ALL OF THEM")
    elif cur == "lock": head(d, "LOCK IT IN.", "HEAVIER", "?")
    elif cur == "gut": head(d, "THE WILD?", "HEAVIER", "?")
    elif cur == "reveal": head(d, "FARM. BY FAR.", "FARM ÷ WILD", "×30" if t >= T_X30 else "…", True)
    elif cur == "pour": head(d, "2.5 KG PER PERSON.", "ALL WILD LAND MAMMALS", "2.5 kg" if t >= T_KG else "…", True)
    else: head(d, "MOST LIVE ON FARMS.", "FARM ÷ WILD", "×30", True)
    fig(d, "total body weight · heap area ∝ weight · Mt = million tonnes")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.scenes = {k: sc for k in ORDER[:-1]}
FX = [(.1, pop(.1), 0), (1.2, thud(.2), 0), (T_OUT, whoosh(.4, .02), 0), *[(x, pop(.08), -.5) for x in T_W], *[(x, pop(.08), .4) for x in T_F], *[(x, thud(.16), 0) for x in T_321], (T_GUT, pop(.08), -.5),
      (T_P0, whoosh(2.5, .02), .2), (T_X30, thud(.22), 0), (T_KG, thud(.2), -.4)]
if __name__ == "__main__": EP.run(FX)
