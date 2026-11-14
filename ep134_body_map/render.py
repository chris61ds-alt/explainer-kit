"""NOT JUST YOU – No. 134: erogenous body maps – 704 Finnish volunteers colored body outlines; men's and women's maps were very
similar (partner-sex maps r ≈ 0.9), women's slightly larger: 26 % vs 22 % of the body (Nummenmaa et al. 2016).
Light look (paper + soft shadows, reveal on black) + clarity rules + big hook intro. Two body outlines (women / men) from frame 0;
answers rain in as PARTICLES and pile up into heat maps; CAMERA starts on one figure and pulls out; reveal: the two maps slide
on top of each other (white + orange, GLOW on black) and match; loop: the dots fall away."""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from fx2 import camera, cam_path, glow, dots, light_look, is_light, hook_intro
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .5, "setup": .5, "explain": .5, "reveal": .8, "detail": .6, "why": .1})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "setup", "explain", "reveal", "detail", "why", "end"]
EP = ThreadEpisode(TL, 134, "BODY MAP", order=ORDER, dark=True, label="SURVEY · 704 PEOPLE · BODY MAPS",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Nummenmaa et al. (2016), Topography of Human", "Erogenous Zones, Archives of Sexual Behavior 45(5)"),
                   music=dict(bpm=96, root=-1, prog="dream", kick="four", audio="v5"),
                   cover=dict(words=["SAME BODY", "MAP. MEN", "AND WOMEN."], kicker="704 people colored where touch turns them on."))
light_look(EP, ORDER)

FW, FM = (330, 520), (750, 520)                 # top of each figure (women left, men right)
H_ = 600
ZONES = [((0, 335), 1.0, 13), ((-40, 170), .55, 11), ((40, 170), .55, 11), ((-30, 400), .45, 11), ((30, 400), .45, 11),
         ((0, 62), .40, 7), ((0, 104), .28, 8), ((0, 270), .1, 22)]          # genitals, chest, inner thighs, lips, neck, belly
def sample(n, spread, seed):
    R = np.random.RandomState(seed); w = np.array([z[1] for z in ZONES]); w = w / w.sum()
    idx = R.choice(len(ZONES), n, p=w); c = np.array([ZONES[i][0] for i in idx], float); s = np.array([ZONES[i][2] for i in idx]) * spread
    return c + R.randn(n, 2) * s[:, None]
NDOT = 1400
PW, PM = sample(NDOT, 1.12, 1), sample(NDOT, 1.0, 2)                            # women's zones a little larger
DROP = np.random.RandomState(3).rand(NDOT)                                       # when each answer arrives (0..1 of the fill time)

T_FILL0, T_FILL1 = S("setup") + .3, E("explain")
T_REV = S("reveal") - .1
T_BACK = cue("why", "And still") - .35

def figure(d, top, col):
    x, y = top
    d.ellipse([x - 42, y, x + 42, y + 92], fill=col)                                         # head
    d.rounded_rectangle([x - 16, y + 86, x + 16, y + 120], radius=6, fill=col)               # neck
    d.rounded_rectangle([x - 78, y + 115, x + 78, y + 330], radius=46, fill=col)             # torso
    d.line([(x - 70, y + 135), (x - 118, y + 290), (x - 126, y + 370)], fill=col, width=34, joint="curve")   # arms
    d.line([(x + 70, y + 135), (x + 118, y + 290), (x + 126, y + 370)], fill=col, width=34, joint="curve")
    d.line([(x - 38, y + 300), (x - 46, y + 450), (x - 50, y + 590)], fill=col, width=46, joint="curve")    # legs
    d.line([(x + 38, y + 300), (x + 46, y + 450), (x + 50, y + 590)], fill=col, width=46, joint="curve")

def shadow(L, tops, k=.3):
    m = Image.new("L", L.size, 0); dm = ImageDraw.Draw(m)
    for (x, y) in tops: figure(dm, (x + 26, y + 18), 255)
    a = np.asarray(m.filter(ImageFilter.GaussianBlur(14)), np.float32)[..., None] / 255 * k
    L.paste(Image.fromarray(np.clip(np.asarray(L, np.float32) * (1 - a) + a * np.array(INK, np.float32), 0, 255).astype(np.uint8)))

def fill_k(t):
    if t >= T_BACK: return 1 - clamp((t - T_BACK) / .4)
    return clamp((t - T_FILL0) / (T_FILL1 - T_FILL0))

def slide(t):
    """0 = side by side, 1 = both maps on one body (reveal)"""
    if t < T_REV: return 0
    k = spring((t - T_REV) / .7, f=1.1, damp=6)
    if t >= cue("detail", "Women's maps") - .2: k *= 1 - ease(clamp((t - cue("detail", "Women's maps") + .2) / .6))
    return k

def scene(L, d, t):
    s = slide(t); mid = (FW[0] + FM[0]) / 2
    tw = (FW[0] + (mid - FW[0]) * s, FW[1]); tm = (FM[0] + (mid - FM[0]) * s, FM[1])
    if is_light(EP, t): shadow(L, [tw, tm] if s < .95 else [tw])
    body = RULE if is_light(EP, t) else mix(BG, INK, .18)
    figure(d, tw, body); figure(d, tm, body)
    k = fill_k(t); wave = (t - .05) / .9
    if 0 <= wave <= 1.2:                                                          # cold open: a scan line runs down both bodies
        yy = FW[1] + H_ * wave; d.line([(FW[0] - 160, yy), (FM[0] + 160, yy)], fill=MID, width=3)
    for P_, top, col in ((PW, tw, INK), (PM, tm, SIG if not is_light(EP, t) else INK)):
        n = (DROP < k)
        if not n.any(): continue
        p = P_[n] + np.array([top[0], top[1]])
        fall = np.clip((k - DROP[n]) / .08, 0, 1)                               # each answer drops in from above
        p[:, 1] -= (1 - fall) ** 2 * 260
        dots(L, p, col, size=3)
    if not is_light(EP, t) and k > .5:
        glow(L, [("c", tw[0], tw[1] + 335, 40), ("c", tw[0], tw[1] + 168, 50)], col=SIG, r=26, k=.35)
    for top, lab in ((tw, "WOMEN"), (tm, "MEN")):
        if s < .5: d.text((top[0], top[1] - 30), lab, font=F(BLK, 36), fill=INK, anchor="mm")
    if s >= .5: d.text((mid, FW[1] - 30), "WOMEN + MEN", font=F(BLK, 36), fill=INK, anchor="mm")

def cam(t):
    w = (FW[0], FW[1] + 300); m = (540, 820)
    keys = [(0, 1.6, w), (S("setup") - .2, 1.5, w), (S("setup") + 1.0, 1.0, m), (T_BACK, 1.0, m), (T_BACK + .7, 1.6, w)]
    return cam_path(t, keys)

def head(d, t, line, sub=None):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    cur = EP.current(t)
    if cur == "detail" or (cur == "why" and t < T_BACK):
        d.text((X0, 400), "BODY AREA", font=F(MONO, 30), fill=MID)
        d.text((X0 + 200, 388), "26 %", font=F(BLK, 64), fill=INK); d.text((X0 + 380, 400), "WOMEN", font=F(MONO, 26), fill=MID)
        d.text((X0 + 520, 388), "22 %", font=F(BLK, 64), fill=INK); d.text((X0 + 700, 400), "MEN", font=F(MONO, 26), fill=MID)
    else:
        n = int(704 * fill_k(t)) if t >= T_FILL0 else 0
        d.text((X0, 400), "PEOPLE", font=F(MONO, 30), fill=MID); d.text((X0 + 150, 388), f"{n}", font=F(BLK, 64), fill=SIG if cur == "reveal" else INK)
    if sub: d.text((X1, 470), sub, font=F(MONO, 26), fill=MID, anchor="ra")

def draw(img, d, t, line, sub=None, note="dots: schematic, after the published maps"):
    z, f = cam(t); camera(img, lambda L, dL: scene(L, dL, t), z, f); head(d, t, line, sub); fig(d, note)

def sc_hook(img, d, t): draw(img, d, t, "WHERE?")
def sc_setup(img, d, t): draw(img, d, t, "704 PEOPLE")
def sc_explain(img, d, t): draw(img, d, t, "1 DOT = 1 ANSWER")
def sc_reveal(img, d, t): draw(img, d, t, "ALMOST THE SAME.", note="maps rated alike: r ≈ 0.9")
def sc_detail(img, d, t): draw(img, d, t, "WOMEN: A BIT BIGGER", note="share of the body that felt arousing")
def sc_why(img, d, t): draw(img, d, t, "MORE ALIKE." if t < T_BACK else "WHERE?", note="one online study · Finland · self-reported")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.scenes = {"hook": sc_hook, "setup": sc_setup, "explain": sc_explain, "reveal": sc_reveal, "detail": sc_detail, "why": sc_why}
FX = [(.05, whoosh(.8, .04), 0), (S("setup") - .1, whoosh(.8, .05), 0),
      *[(T_FILL0 + j * .12, tick(.02), (j % 5 - 2) / 3) for j in range(int((T_FILL1 - T_FILL0) / .12))],
      (S("reveal") + .1, thud(.55), 0), (T_REV + .5, pop(.16), 0), (cue("detail", "Women's maps") - .2, whoosh(.4, .04), 0),
      (T_BACK, whoosh(.6, .05), 0)]
hook_intro(EP)
if __name__ == "__main__": EP.run(FX)
