"""NOT JUST YOU – No. 152: the birthday riddle (first 'riddle' episode, 25.11.2026, after a reference Chris sent:
question -> rules -> 3-2-1 'lock in your answer' -> the gut answer -> the solution IN THE SAME VIDEO (Chris: solution included)).
Math: P(match among n) = 1 - prod((365-i)/365); n=23: 50.7 %, n=70: 99.9 %; 23 people = 253 pairs.
ONE continuous story on dark (riddle look like the reference): a 365-day calendar grid; people drop onto their birthdays one
by one with a live chance counter; the 23rd lands on a taken day -> '23'. The 23 dots morph into a circle and every pair gets a
chord (0 -> 253). Then the curve 1..70 people draws itself. Payoff (rule 15): curve with the 23 / 50 % mark stays."""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from fx2 import light_look
from stand import dashed, stamp_box, payoff_cam
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .4, "rules": .4, "lock": .7, "gut": .5, "reveal": .85, "pairs": .5, "curve": .5, "why": .1}, pace="loose")
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "rules", "lock", "gut", "reveal", "pairs", "curve", "why", "end"]
EP = ThreadEpisode(TL, 152, "THE BIRTHDAY RIDDLE", order=ORDER, dark=True, label="RIDDLE · 365 DAYS · 1 ROOM",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("The birthday problem · standard probability", "365 equal days, no leap day, no twins"),
                   music=dict(bpm=96, root=4, prog="major", kick="four", audio="v5"),
                   cover=dict(words=["HOW MANY PEOPLE", "FOR A SHARED", "BIRTHDAY?"], kicker="Lock in your answer."))
light_look(EP, ORDER)                                          # rule 16 (25.11.2026): light paper + shadows, reveal on black

def P(n): return 1 - float(np.prod([(365 - i) / 365 for i in range(int(n))]))

# calendar: 365 days, 21 x 18
COLS, CX0, CDX, CY0, CDY, CW, CH = 21, 102, 41.8, 520, 36, 30, 26
def cell(d): r, c = divmod(d, COLS); return CX0 + c * CDX + CW / 2, CY0 + r * CDY + CH / 2
R = np.random.RandomState(11); DAYS = list(R.choice(365, 22, replace=False)) + [None]
DAYS[22] = DAYS[8]                                           # the 23rd person shares a birthday with person 9
MATCH = (8, 22)

T_OUT = S("rules") - .2; T_FILL = T_OUT + .05                # 25.11.2026 (rule 11): two people + cakes first, then the calendar
T_LOCK = S("lock"); T_321 = [cue("lock", "Three") - .05, cue("lock", "Two") - .05, cue("lock", "One") - .05]
T_GUT = cue("gut", "half") - .1; T_180 = cue("gut", "one hundred") - .1
T_DROP0, T_DROP1 = S("reveal") - .25, cue("reveal", "twenty-three") - .05
T_23 = T_DROP1 + .05
T_MORPH = S("pairs") + .05; T_CH0, T_CH1 = S("pairs") + .7, E("pairs") + .2
T_CURVE0, T_CURVE1 = S("curve") - .1, E("curve") + .3

def n_dropped(t): return 0 if t < T_DROP0 else min(23, 1 + int(22 * ease_io(clamp((t - T_DROP0) / (T_DROP1 - T_DROP0)))))

CIRC = [(540 + 300 * math.cos(-math.pi / 2 + 2 * math.pi * i / 23), 830 + 300 * math.sin(-math.pi / 2 + 2 * math.pi * i / 23)) for i in range(23)]
PAIRS = [(i, j) for i in range(23) for j in range(i + 1, 23)]

def calendar(d, t, dim=0.0):
    for k in range(365):
        x, y = cell(k); s = clamp((t - T_FILL - (k // COLS) * .025 - (k % COLS) * .01) / .25)
        if s <= 0: continue
        col = mix(RULE, MID, .3)
        if S("gut") <= t < S("reveal") and t >= T_180 and k < 182: col = mix(RULE, MID, .7)     # 'half the year'
        col = mix(col, BG, dim)
        w, h = CW / 2 * s, CH / 2 * s
        d.rounded_rectangle([x - w, y - h, x + w, y + h], radius=5, fill=col)

def people(d, t):
    n = n_dropped(t); m = 1 - ease_io(clamp((t - T_MORPH) / .6)) if t >= T_MORPH else 1
    for i in range(n):
        x0, y0 = cell(DAYS[i]); k = spring(clamp((t - T_DROP0 - (T_DROP1 - T_DROP0) * i / 22) / .3))
        if i == 22: x0 += 7; y0 += 0                                                        # visibly ON the taken day
        x1, y1 = CIRC[i]; x, y = x0 + (x1 - x0) * (1 - m), y0 + (y1 - y0) * (1 - m) - 30 * (1 - k) * m
        hot = i in MATCH and t >= T_23
        r = 11 + 9 * (1 - m)
        d.ellipse([x - r, y - r, x + r, y + r], fill=SIG if hot else INK)

def chords(d, t):
    if t < T_CH0: return 0
    u = clamp((t - T_CH0) / (T_CH1 - T_CH0)); k = int(round(253 * ease_io(u)))
    for (i, j) in PAIRS[:k]:
        d.line([CIRC[i], CIRC[j]], fill=mix(BG, SIG if (i, j) == MATCH else MID, .8 if (i, j) == MATCH else .55), width=4 if (i, j) == MATCH else 2)
    return k

PX0, PX1, PY0, PY1 = 170, 900, 620, 1090
def Pxy(n, p): return PX0 + n / 70 * (PX1 - PX0), PY1 - p * (PY1 - PY0)
def glow_line(img, pts, col, w):
    if len(pts) < 2: return
    L = Image.new("L", img.size, 0); ImageDraw.Draw(L).line(pts, fill=255, width=w * 4, joint="curve")
    m = np.asarray(L.filter(ImageFilter.GaussianBlur(14)), np.float32)[..., None] / 255 * .55
    base = np.asarray(img, np.float32)
    img.paste(Image.fromarray(np.clip(base * (1 - m) + np.array(col, np.float32) * m, 0, 255).astype(np.uint8)))

def curve(img, t):
    d = ImageDraw.Draw(img); k = ease(clamp((t - T_CURVE0) / .4))
    d.line([(PX0, PY0 - 10), (PX0, PY1)], fill=MID, width=3); d.line([(PX0, PY1), (PX1 + 30, PY1)], fill=MID, width=3)
    for p in (0, .5, 1):
        y = Pxy(0, p)[1]; d.line([(PX0 - 12, y), (PX0, y)], fill=MID, width=3); d.text((PX0 - 22, y), f"{int(p * 100)}%", font=F(MONO, 26), fill=MID, anchor="rm")
    for n in (0, 23, 50, 70):
        x = Pxy(n, 0)[0]; d.line([(x, PY1), (x, PY1 + 12)], fill=MID, width=3); d.text((x, PY1 + 40), str(n), font=F(MONO, 26), fill=SIG if n == 23 else MID, anchor="mm")
    d.text((PX1 + 30, PY1 + 80), "People", font=F(MONO, 28), fill=MID, anchor="rm")
    d.text((PX0 - 10, PY0 - 40), "Chance of a match", font=F(MONO, 26), fill=MID, anchor="lm")
    nn = 1 + 69 * ease_io(clamp((t - T_CURVE0) / (T_CURVE1 - T_CURVE0)))
    xs = np.linspace(1, nn, 140); pts = [Pxy(x, P_smooth(x)) for x in xs]
    if nn >= 23:                                                                            # the 23 / 50 % mark
        x, y = Pxy(23, P(23)); dashed(d, (x, PY1), (x, y), SIG, w=3); dashed(d, (PX0, y), (x, y), SIG, w=3)
    glow_line(img, pts, SIG, 6); d = ImageDraw.Draw(img); d.line(pts, fill=SIG, width=7, joint="curve")
    tx, ty = pts[-1]; d.ellipse([tx - 13, ty - 13, tx + 13, ty + 13], fill=SIG)
    d.text((tx - 20 if nn > 55 else tx + 24, ty - (40 if nn > 55 else 0)), f"{P_smooth(nn) * 100:.1f}%", font=F(BLK, 36), fill=INK, anchor="rm" if nn > 55 else "lm")

def P_smooth(x):                                              # P between integers, for a smooth tip
    a = int(x); return P(a) + (P(a + 1) - P(a)) * (x - a)

def countdown(d, t):
    if not (T_LOCK <= t < S("gut")): return
    d.rounded_rectangle([290, 640, 790, 1040], radius=40, fill=BG)
    d.text((540, 690), "LOCK IN YOUR ANSWER", font=F(BLK, 38), fill=INK, anchor="mm")
    i = sum(1 for x in T_321 if t >= x)
    ring = clamp((t - T_321[0]) / (T_321[2] + .7 - T_321[0])) if t >= T_321[0] else 0
    d.ellipse([420, 750, 660, 990], outline=mix(BG, MID, .6), width=12)
    if ring > 0: d.arc([420, 750, 660, 990], -90, -90 + 360 * (1 - ring), fill=SIG, width=12)
    d.text((540, 870), ["?", "3", "2", "1"][i], font=F(BLK, 130), fill=INK, anchor="mm")

def head(d, t, line, label=None, val=None, hot=False):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    if label:
        d.text((X0, 400), label, font=F(MONO, 30), fill=MID)
        d.text((X0 + d.textlength(label, font=F(MONO, 30)) + 24, 388), val, font=F(BLK, 56), fill=SIG if hot else INK)

def cake(d, x, y, s):
    d.rounded_rectangle([x - 44 * s, y - 30 * s, x + 44 * s, y + 20 * s], radius=int(8 * s), fill=mix(BG, INK, .85))
    d.rectangle([x - 44 * s, y - 12 * s, x + 44 * s, y - 4 * s], fill=SIG)
    d.line([(x, y - 30 * s), (x, y - 56 * s)], fill=INK, width=max(1, int(5 * s)))
    d.ellipse([x - 7 * s, y - 72 * s, x + 7 * s, y - 56 * s], fill=SIG)

def intro(d, t):
    """the mini-film: two strangers pop in, the same cake appears over both, 'SAME DAY?'"""
    out = ease_io(clamp((t - T_OUT) / .4)) if t >= T_OUT else 0
    if out >= 1: return
    for i, (x, t0) in enumerate(((380, .1), (700, .35))):
        k = spring(clamp((t - t0) / .4)) * (1 - out)
        if k <= 0: continue
        y = 960
        d.ellipse([x - 40 * k, y - 210 * k, x + 40 * k, y - 130 * k], fill=INK)
        d.rounded_rectangle([x - 62 * k, y - 120 * k, x + 62 * k, y + 60 * k], radius=int(30 * k), fill=INK)
        c = spring(clamp((t - .8 - i * .25) / .35)) * (1 - out)
        if c > 0: cake(d, x, y - 290, c * 1.4)
    if .8 <= t < T_OUT + .2: d.line([(470, 640), (610, 640)], fill=SIG, width=5)
    if t >= 1.4 and out < .5: stamp_box(d, (540, 1080), "SAME DAY?", t, 1.4, size=70)

def sc(img, d, t):
    payoff_cam(img, lambda L, dL: sc_full(L, dL, t), t, S("why"), focus=Pxy(23, .5), z1=1.12, ep=EP)

def sc_full(img, d, t):
    cur = EP.current(t)
    if cur in ("curve", "why", "end"):
        curve(img, t); d = ImageDraw.Draw(img)
        head(d, t, "PAIRS, NOT PEOPLE." if cur != "curve" else "70 PEOPLE: 99.9%", "23 PEOPLE", "50.7%", True)
        fig(d, "365 equal days · no leap day · no twins"); return
    if cur == "pairs":
        k = chords(d, t); people(d, t)
        head(d, t, "253 PAIRS.", "PAIRS COMPARED", f"{k}", True); fig(d, "every line = one pair of people"); return
    intro(d, t)
    calendar(d, t, dim=.6 if cur == "lock" else 0); people(d, t); countdown(d, t)
    n = n_dropped(t)
    if cur == "reveal":
        head(d, t, "JUST 23." if t >= T_23 else "LET'S FILL THE ROOM.", f"{n} PEOPLE · MATCH", f"{P(n) * 100:.1f}%", t >= T_23)
        if t >= T_23: stamp_box(d, (720, 1000), "23", t, T_23, size=120)
    elif cur == "gut": head(d, t, "HALF THE YEAR?", "PEOPLE FOR 50/50", "~180?" if t >= T_180 else "?")
    elif cur == "lock": head(d, t, "LOCK IT IN.", "PEOPLE FOR 50/50", "?")
    elif cur == "rules": head(d, t, "365 DAYS.", "NO TWINS · NO LEAP YEARS", "")
    else: head(d, t, "SHARED BIRTHDAY?", "PEOPLE FOR 50/50", "?")
    fig(d, "1 square = 1 day of the year")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.scenes = {k: sc for k in ORDER[:-1]}
FX = [(.1, pop(.1), -.4), (.35, pop(.1), .4), (.8, pop(.08), -.3), (1.05, pop(.08), .3), (1.4, thud(.2), 0), (T_FILL, whoosh(.5, .02), -.3), *[(x, thud(.16), 0) for x in T_321], (T_180, pop(.1), 0),
      *[(T_DROP0 + (T_DROP1 - T_DROP0) * i / 22, tick(.008), -.6 + i * .055) for i in range(23)], (T_23, thud(.22), 0),
      (T_MORPH, whoosh(.5, .03), .3), (T_CURVE0, whoosh(.5, .02), -.3)]
if __name__ == "__main__": EP.run(FX)
