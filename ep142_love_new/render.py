"""NOT JUST YOU – No. 142: marrying for love is new – Kephart (1967): asked whether they'd marry someone with all desired
qualities without being in love, only 24 % of US college women (65 % of men) said no; Levine et al. (1995): only 3.5 % of
Americans said yes; India and Pakistan were the exceptions.
Light look (paper + soft shadows, reveal on black) + clarity rules ("Each dot is one in a hundred women") + rule 13 opener.
ONE continuous object: 100 dots forming a heart. Cold open: a ring drops into the heart, the heart breaks apart into a loose
cloud (love optional), "LOVE? OPTIONAL." stamp; rewind into the heart; 24 dots fill as "NO"; then the 1990s: 96.5 fill,
3.5 stay as "YES"; loop: the heart is whole again (= frame 0)."""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from fx2 import light_look, is_light, stamp
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .5, "setup": .5, "explain": .5, "reveal": .8, "later": .8, "why": .1})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "setup", "explain", "reveal", "later", "why", "end"]
EP = ThreadEpisode(TL, 142, "LOVE IS NEW", order=ORDER, dark=True, label="SURVEYS · 1967 & 1995",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Kephart (1967), J. of Marriage and the Family ·", "Levine et al. (1995), J. of Cross-Cultural Psych."),
                   music=dict(bpm=90, root=3, prog="major", kick="half", audio="v5"),
                   cover=dict(words=["1967: MOST", "WOULDN'T RULE OUT", "A LOVELESS MARRIAGE."], kicker="Marrying for love is newer than you think."))
light_look(EP, ORDER)

def heart_points(n=100):
    """n points evenly filling a heart (deterministic)"""
    pts = []
    xs = np.linspace(-1.2, 1.2, 15); ys = np.linspace(-1.1, 1.3, 15)
    for y in ys[::-1]:
        for x in xs:
            if (x * x + (y - abs(x) ** (2 / 3) * .9) ** 2) <= 1.0: pts.append((x, y))
    pts = sorted(pts, key=lambda p: (-p[1], p[0]))
    idx = np.linspace(0, len(pts) - 1, n).round().astype(int)
    return [pts[i] for i in idx]
HP = heart_points()
CX, CY, SC = 540, 800, 230
HEART = [(CX + x * SC, CY - y * SC) for x, y in HP]
R = np.random.RandomState(7)
CLOUD = [(CX + R.uniform(-430, 430), CY + R.uniform(-300, 330)) for _ in HEART]
NO67 = set(np.random.RandomState(3).choice(100, 24, replace=False))            # 24 "no" dots (women, 1967)
YES95 = set(np.random.RandomState(5).choice(100, 4, replace=False))            # ≈ 3.5 "yes" dots (Americans, 1995)
DR = 15

T_RING = .3;  T_BREAK = cue("hook", "rule out") - .3
T_STAMP = cue("hook", "without love") - .05
T_REW = S("setup") - .05
T_EXP = cue("explain", "Each dot") - .1
T_NO = cue("reveal", "twenty-four") - .15
T_95 = S("later") + .05; T_YES = cue("later", "three point five") - .15
T_BACK = E("why") - .9

def pos(i, t):
    """heart at frame 0, breaks into a loose cloud in the hook, rewinds to the heart"""
    hx, hy = HEART[i]; cx, cy = CLOUD[i]
    if T_BREAK <= t < T_REW + .8:
        k = ease_io(clamp((t - T_BREAK - (i % 10) * .02) / .7)) if t < T_REW else 1 - ease_io(clamp((t - T_REW) / .8))
        return hx + (cx - hx) * k, hy + (cy - hy) * k
    return hx, hy

def dot_col(i, t):
    cur = EP.current(t)
    if T_NO <= t < T_95 and i in NO67 and t >= T_NO + (sorted(NO67).index(i)) * .02: return INK, "fill"
    if T_95 <= t < T_BACK:
        k = sorted(range(100)).index(i) * .012
        if i in YES95: return SIG, "fill"
        if t >= T_95 + .2 + k: return INK, "fill"
    return MID, "ring"

def objects(L, d, t):
    for i in range(100):
        x, y = pos(i, t); col, kind = dot_col(i, t)
        if kind == "fill": d.ellipse([x - DR, y - DR, x + DR, y + DR], fill=col)
        else: d.ellipse([x - DR, y - DR, x + DR, y + DR], outline=col, width=4)
    if T_RING <= t < T_REW:                                                    # cold open: the ring drops in
        k = clamp((t - T_RING) / .55); y = 400 + (CY - 80 - 400) * k * k
        if k >= 1: y = CY - 80 + 10 * math.sin((t - T_RING - .55) * 18) * max(0, 1 - (t - T_RING - .55) / .4)
        d.ellipse([CX - 60, y - 60, CX + 60, y + 60], outline=INK, width=16)
        d.polygon([(CX - 22, y - 62), (CX + 22, y - 62), (CX, y - 92)], fill=INK)

def shadowed(img, t):
    if not is_light(EP, t):
        objects(img, ImageDraw.Draw(img), t); return
    L = Image.new("RGB", img.size, BG); objects(L, ImageDraw.Draw(L), t)
    a = np.asarray(L, np.int16); m = (np.abs(a - np.array(BG)).max(axis=2) > 10).astype(np.uint8) * 255
    m[:470] = 0; m[1186:] = 0
    M = Image.fromarray(m); sh = Image.new("L", img.size, 0); sh.paste(M, (16, 18))
    k = np.asarray(sh.filter(ImageFilter.GaussianBlur(14)), np.float32)[..., None] / 255 * .3
    out = np.asarray(img, np.float32) * (1 - k) + k * np.array(INK, np.float32)
    img.paste(Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))); img.paste(L, (0, 0), M)

def labels(d, t):
    cur = EP.current(t)
    if T_STAMP <= t < T_REW + .2: stamp(d, (CX, 1080), "LOVE? OPTIONAL.", t, T_STAMP, size=70)
    if cur == "explain" and t >= T_EXP:
        x, y = HEART[0]; d.ellipse([x - DR - 12, y - DR - 12, x + DR + 12, y + DR + 12], outline=SIG, width=5)
        d.text((x + 60, y - 30), "1 IN 100", font=F(BLK, 36), fill=INK, anchor="lm")
    if cur == "reveal" and t >= T_NO + .5:
        d.text((CX, 1140), "● SAID NO   ○ YES OR UNSURE", font=F(MONO, 26), fill=INK, anchor="mm")
    if cur in ("later", "why") and t >= T_YES and t < T_BACK:
        d.text((CX, 1140), "● NOT YES   ● YES", font=F(MONO, 26), fill=INK, anchor="mm")

def head(d, t, line):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    cur = EP.current(t)
    if t >= T_95 and t < T_BACK:
        d.text((X0, 400), "1990s · AMERICANS SAID YES", font=F(MONO, 30), fill=MID)
        d.text((X0 + 520, 388), "3.5%" if t >= T_YES else "…", font=F(BLK, 64), fill=SIG if cur == "later" else INK)
    else:
        n = sum(1 for i in NO67 if T_NO <= t and t >= T_NO + sorted(NO67).index(i) * .02)
        d.text((X0, 400), "1967 · WOMEN SAID NO", font=F(MONO, 30), fill=MID)
        d.text((X0 + 410, 388), f"{n}%" if T_NO <= t < T_95 else "?", font=F(BLK, 64), fill=SIG if cur == "reveal" else INK)

def draw(img, d, t, line, note="US college students · dots schematic"):
    shadowed(img, t); d = ImageDraw.Draw(img); labels(d, t); head(d, t, line); fig(d, note)

def sc_hook(img, d, t): draw(img, d, t, "MARRY WITHOUT LOVE?")
def sc_setup(img, d, t): draw(img, d, t, "THE PERFECT PARTNER.", note="all qualities you want · but no love")
def sc_explain(img, d, t): draw(img, d, t, "1 DOT = 1%")
def sc_reveal(img, d, t): draw(img, d, t, "1967: ONLY 24 NO.", note="women · men: 65% said no")
def sc_later(img, d, t): draw(img, d, t, "1990s: 3.5% YES.", note="India & Pakistan: many still yes")
def sc_why(img, d, t): draw(img, d, t, "LOVE FIRST IS NEW." if t < T_BACK else "MARRY WITHOUT LOVE?")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.scenes = {"hook": sc_hook, "setup": sc_setup, "explain": sc_explain, "reveal": sc_reveal, "later": sc_later, "why": sc_why}
FX = [(T_RING, whoosh(.4, .04), 0), (T_RING + .55, thud(.45), 0), (T_BREAK, whoosh(.7, .05), 0), (T_STAMP, thud(.5), .2),
      (T_REW, whoosh(.6, .05), 0), (T_EXP, pop(.12), -.3), (S("reveal") + .05, thud(.55), 0),
      *[(T_NO + j * .08, tick(.02), -.5 + j * .1) for j in range(10)], (T_95, whoosh(.5, .04), 0),
      *[(T_95 + .2 + j * .12, tick(.02), -.5 + j * .1) for j in range(10)], (T_YES, pop(.16), .3), (T_BACK, whoosh(.6, .05), 0)]
if __name__ == "__main__": EP.run(FX)
