"""NOT JUST YOU – No. 135: arousal concordance – meta-analysis of 132 lab studies (2,505 women, 1,918 men): agreement between
genital response and self-reported arousal r = .66 for men, r = .26 for women (Chivers et al. 2010). Message: a body's
reaction is not a yes.
Light look (paper + soft shadows, reveal on black) + clarity rules + big hook intro. Two lab-monitor cards (MEN / WOMEN) with two
live traces each, BODY and MIND, scrolling from frame 0; men's traces move together, women's drift apart (gap shaded);
CAMERA pushes into the card being talked about; loop."""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from fx2 import camera, cam_path, glow, light_look, is_light, hook_intro
from PIL import Image, ImageDraw, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .5, "setup": .5, "explain": .5, "men": .5, "reveal": .8, "why": .1})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "setup", "explain", "men", "reveal", "why", "end"]
EP = ThreadEpisode(TL, 135, "BODY VS MIND", order=ORDER, dark=True, label="META-ANALYSIS · 132 LAB STUDIES",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Chivers, Seto, Lalumière, Laan & Grimbos (2010),", "Archives of Sexual Behavior 39(1), 5–56"),
                   music=dict(bpm=92, root=-2, prog="tense", kick="half", audio="v5"),
                   cover=dict(words=["YOUR BODY", "REACTS. YOUR", "MIND DOESN'T."], kicker="Body vs. mind, from 132 lab studies."))
light_look(EP, ORDER)

def smooth(seed, n=4000):
    R = np.random.RandomState(seed); x = np.cumsum(R.randn(n)); x = np.convolve(x - np.convolve(x, np.ones(200) / 200, "same"), np.ones(25) / 25, "same")
    return np.clip(x / (x.std() * 2.2 + 1e-6), -1, 1)
SIG_B = smooth(1); N1, N2 = smooth(2), smooth(3)
MEN_MIND = .85 * SIG_B + .45 * N1; WOMEN_MIND = .3 * SIG_B + .95 * N2
MEN_MIND = np.clip(MEN_MIND / (MEN_MIND.std() * 2.2), -1, 1); WOMEN_MIND = np.clip(WOMEN_MIND / (WOMEN_MIND.std() * 2.2), -1, 1)
FPS_S = 100                                                     # samples per second of video time

CARDS = {"MEN": (X0 + 10, 560, X1 - 10, 800), "WOMEN": (X0 + 10, 870, X1 - 10, 1110)}
T_LAB = cue("explain", "what the body did") - .1; T_LAB2 = cue("explain", "what people said") - .1
T_BACK = cue("why", "Because") - .35

def trace(d, box, arr, t, col, w, k=1.0):
    x0, y0, x1, y1 = box; cy = (y0 + y1) / 2 + 18; amp = (y1 - y0) * .36
    i1 = int(t * FPS_S) + 400; n = 400
    seg = arr[max(0, i1 - n):i1]
    pts = [(x0 + 30 + (x1 - x0 - 60) * j / (n - 1), cy - amp * v * k) for j, v in enumerate(seg)]
    if len(pts) > 1: d.line(pts, fill=col, width=w, joint="curve")
    return pts

def card_shadow(L, boxes):
    m = Image.new("L", L.size, 0); dm = ImageDraw.Draw(m)
    for (x0, y0, x1, y1) in boxes: dm.rounded_rectangle([x0 + 14, y0 + 18, x1 + 14, y1 + 18], radius=26, fill=255)
    a = np.asarray(m.filter(ImageFilter.GaussianBlur(16)), np.float32)[..., None] / 255 * .28
    L.paste(Image.fromarray(np.clip(np.asarray(L, np.float32) * (1 - a) + a * np.array(INK, np.float32), 0, 255).astype(np.uint8)))

def focus(t):
    cur = EP.current(t)
    return "MEN" if cur == "men" else "WOMEN" if cur in ("reveal",) else None

def scene(L, d, t):
    if is_light(EP, t): card_shadow(L, CARDS.values())
    f = focus(t)
    for name, box in CARDS.items():
        x0, y0, x1, y1 = box
        d.rounded_rectangle(box, radius=26, fill=WHITE if is_light(EP, t) else mix(BG, INK, .1), outline=INK if f == name else RULE, width=5 if f == name else 2)
        d.text((x0 + 30, y0 + 22), name, font=F(BLK, 40), fill=INK)
        mind = MEN_MIND if name == "MEN" else WOMEN_MIND
        pb = trace(d, box, SIG_B, t, INK, 6)
        pm = trace(d, box, mind, t, SIG if (name == "WOMEN" and EP.current(t) == "reveal") else MID, 6)
        if name == "WOMEN" and S("reveal") <= t < T_BACK:                      # the gap between body and mind, shaded
            for a, b in list(zip(pb, pm))[::6]: d.line([a, b], fill=mix(WHITE if is_light(EP, t) else BG, SIG, .35), width=3)
        if t >= T_LAB:                                                          # legend
            k = spring((t - T_LAB) / .4); d.text((x1 - 30, y0 + 26), "BODY", font=F(BLK, 28), fill=INK, anchor="ra")
            if t >= T_LAB2: d.text((x1 - 140, y0 + 26), "MIND", font=F(BLK, 28), fill=MID, anchor="ra")

def cam(t):
    m = (540, 835); mc = (540, (CARDS["MEN"][1] + CARDS["MEN"][3]) / 2); wc = (540, (CARDS["WOMEN"][1] + CARDS["WOMEN"][3]) / 2)
    keys = [(0, 1.35, wc), (S("setup") - .2, 1.3, wc), (S("setup") + 1.0, 1.0, m), (S("men") - .2, 1.0, m), (S("men") + .7, 1.3, mc),
            (S("reveal") - .3, 1.3, mc), (S("reveal") + .7, 1.3, wc), (S("why") + .2, 1.0, m), (T_BACK, 1.0, m), (T_BACK + .7, 1.35, wc)]
    return cam_path(t, keys)

def head(d, t, line, sub=None):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    cur = EP.current(t)
    if cur in ("men", "reveal") or (cur == "why" and t < T_BACK):
        d.text((X0, 392), "MEN: STRONG", font=F(BLK, 52), fill=INK)                 # how well body and mind agree
        if cur != "men": d.text((X0 + 430, 392), "WOMEN: WEAK", font=F(BLK, 52), fill=SIG if cur == "reveal" else INK)
    else:
        d.text((X0, 400), "LAB STUDIES", font=F(MONO, 30), fill=MID); d.text((X0 + 240, 388), "132", font=F(BLK, 64), fill=INK)
    if sub: d.text((X1, 470), sub, font=F(MONO, 26), fill=MID, anchor="ra")

def draw(img, d, t, line, sub=None, note="traces: schematic"):
    z, f = cam(t); camera(img, lambda L, dL: scene(L, dL, t), z, f); head(d, t, line, sub); fig(d, note)

def sc_hook(img, d, t): draw(img, d, t, "BODY VS. MIND")
def sc_setup(img, d, t): draw(img, d, t, "4,423 PEOPLE", sub="1969 – 2007")
def sc_explain(img, d, t): draw(img, d, t, "2 LINES")
def sc_men(img, d, t): draw(img, d, t, "MEN: TOGETHER", note="body + mind agreement r = .66 · schematic")
def sc_reveal(img, d, t): draw(img, d, t, "WOMEN: APART", note="body + mind agreement r = .26 · schematic")
def sc_why(img, d, t): draw(img, d, t, "A REACTION ≠ A YES." if t < T_BACK else "BODY VS. MIND", note="lab studies · part of the gap is method")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.scenes = {"hook": sc_hook, "setup": sc_setup, "explain": sc_explain, "men": sc_men, "reveal": sc_reveal, "why": sc_why}
FX = [(.05, whoosh(.8, .04), 0), (S("setup") - .1, whoosh(.8, .05), 0), (T_LAB, pop(.12), .3), (T_LAB2, pop(.12), .1),
      (S("men") + .2, whoosh(.5, .04), 0), (S("reveal") + .1, thud(.55), 0), (S("reveal") + .8, whoosh(.5, .04), 0),
      (S("why") + .2, pop(.14), 0), (T_BACK, whoosh(.6, .05), 0)]
hook_intro(EP)
if __name__ == "__main__": EP.run(FX)
