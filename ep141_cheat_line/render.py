"""NOT JUST YOU – No. 141: what counts as cheating? – iFidelity Survey (YouGov 2019, N = 2,000 US adults): secret emotional
relationship 76 % say infidelity, flirting 42 %, following an ex online 32 %, secret porn 30 %.
Light look (paper + soft shadows, reveal on black) + clarity rules ("Bottom means nobody… top means everybody") + rule 13 opener.
ONE continuous object: a vertical 0–100 % scale with behaviour cards hanging on it. Cold open: a "FLIRTING?" card swings between
CHEATING and NOT like a pendulum and settles below half, "42%" stamp; rewind; scale labels + half line; reveal on black: the
emotional-bond card shoots to 76; the others slide in; finally two lines YOU / PARTNER at different heights; loop."""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from fx2 import light_look, is_light, stamp
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .5, "setup": .5, "explain": .5, "reveal": .8, "rest": .6, "why": .1})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "setup", "explain", "reveal", "rest", "why", "end"]
EP = ThreadEpisode(TL, 141, "WHERE'S THE LINE?", order=ORDER, dark=True, label="SURVEY · 2,000 US ADULTS · 2019",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("iFidelity Survey (YouGov 2019), Wheatley Institution", "& National Marriage Project, via IFS"),
                   music=dict(bpm=92, root=-3, prog="tense", kick="half", audio="v5"),
                   cover=dict(words=["IS FLIRTING", "CHEATING?", "ONLY 42% SAY YES."], kicker="Where people draw the line."))
light_look(EP, ORDER)

SX = 190                                                   # the scale's x
def sy(p): return 1140 - p * 5.8                           # % -> y
T_SW = .2
T_STAMP = cue("hook", "Fewer") - .05
T_REW = S("setup") - .05
T_SCALE = S("setup") + .1
T_BOT = cue("explain", "Bottom") - .1; T_TOPL = cue("explain", "Top") - .1
T_EMO = S("reveal") + .1
T_FL, T_EX, T_PO = cue("rest", "Flirting") - .1, cue("rest", "Following") - .1, cue("rest", "Secret") - .1
T_YOU = cue("why", "you and your partner") - .1
T_BACK = E("why") - 1.0
CARDS = [("SECRET EMOTIONAL BOND", 76, -26, T_EMO), ("FLIRTING", 42, -30, T_FL), ("FOLLOWING AN EX ONLINE", 32, 8, T_EX),
         ("SECRET PORN", 30, 86, T_PO)]

def card(d, x, y, text, hot):
    f = F(BLK, 34); w = d.textlength(text, font=f) + 48
    d.rounded_rectangle([x, y - 30, x + w, y + 30], radius=16, fill=WHITE, outline=INK if hot else RULE, width=4 if hot else 2)
    d.text((x + 24, y), text, font=f, fill=INK, anchor="lm")
    return w

def flirt_pct(t):
    """cold open: the FLIRTING? card swings between 100 and 0, then settles at 42"""
    if t < T_SW: return 60
    u = t - T_SW; settle = clamp(u / max(.5, T_STAMP - T_SW))
    return 42 + 50 * math.cos(u * 7.0) * (1 - settle) ** 1.5

def objects(L, d, t):
    cur = EP.current(t)
    d.line([(SX, sy(0)), (SX, sy(100))], fill=INK, width=8)                     # the scale
    for p in (0, 50, 100): d.line([(SX - 22, sy(p)), (SX + 22, sy(p))], fill=INK, width=6)
    if t < T_REW + .3:                                                          # cold open card
        k = 1 - clamp((t - T_REW) / .3) if t >= T_REW else 1
        p = flirt_pct(t); y = sy(p)
        d.ellipse([SX - 14, y - 14, SX + 14, y + 14], fill=INK)
        d.line([(SX, y), (SX + 80, y)], fill=INK, width=4)
        card(d, SX + 80 + (1 - k) * 900, y, "FLIRTING?" if t < T_STAMP else "FLIRTING", True)
    for name, p, dy, t0 in CARDS:
        if t < t0 or t >= T_BACK + .4: continue
        k = spring((t - t0) / .55); out = ease(clamp((t - T_BACK) / .4)) if t >= T_BACK else 0
        y = sy(p); yc = y + dy
        d.ellipse([SX - 14, y - 14, SX + 14, y + 14], fill=INK)
        x = SX + 80 + (1 - k) * 900 + out * 900
        d.line([(SX, y), (x, yc)], fill=INK, width=4)
        hot = (cur == "reveal" and name.startswith("SECRET EMO")) or (cur == "rest" and t0 == max(c[3] for c in CARDS if c[3] <= t))
        card(d, x, yc, f"{name}  {p}%", hot)

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

def dashed(d, y, col, x0, x1):
    x = x0
    while x < x1: d.line([(x, y), (min(x + 22, x1), y)], fill=col, width=4); x += 38

def labels(d, t):
    cur = EP.current(t)
    d.text((SX - 34, sy(100)), "100%", font=F(MONO, 24), fill=MID, anchor="rm")
    d.text((SX - 34, sy(50)), "50%", font=F(MONO, 24), fill=MID, anchor="rm")
    d.text((SX - 34, sy(0)), "0%", font=F(MONO, 24), fill=MID, anchor="rm")
    if t < T_REW:
        d.text((SX + 40, sy(100) - 34), "CHEATING", font=F(BLK, 30), fill=INK, anchor="lm")
        d.text((SX + 40, sy(0) + 30), "NOT CHEATING", font=F(BLK, 30), fill=INK, anchor="lm")
    if T_STAMP <= t < T_REW + .2: stamp(d, (760, 640), "42%", t, T_STAMP, size=110)
    if T_SCALE <= t < T_BACK:
        dashed(d, sy(50), MID, SX + 30, 1030)
        if t >= T_BOT: d.text((SX + 40, sy(0) + 30), "NOBODY SAYS CHEATING", font=F(MONO, 24), fill=INK if cur == "explain" else MID, anchor="lm")
        if t >= T_TOPL: d.text((SX + 40, sy(100) - 30), "EVERYBODY SAYS CHEATING", font=F(MONO, 24), fill=INK if cur == "explain" else MID, anchor="lm")
    if cur == "reveal" and t >= T_EMO + .3: d.text((1030, sy(76) - 80), "76%", font=F(BLK, 80), fill=SIG, anchor="rm")
    if cur == "why" and T_YOU <= t < T_BACK:                                   # you and your partner, different lines
        for p, lab, t0 in ((58, "YOUR LINE", T_YOU), (36, "PARTNER'S LINE", T_YOU + .35)):
            if t < t0: continue
            k = ease(clamp((t - t0) / .4)); y = sy(p)
            d.line([(SX - 60, y), (SX - 60 + (1090 - SX) * k, y)], fill=SIG, width=6)
            if k > .6: d.text((1030, y - 12), lab, font=F(BLK, 30), fill=SIG, anchor="rb")

def head(d, t, line):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    d.text((X0, 400), "SAY IT'S CHEATING", font=F(MONO, 30), fill=MID)
    cur = EP.current(t)
    v = {"reveal": "76%", "rest": "30–42%"}.get(cur, "42%" if t >= T_STAMP and t < T_REW + .3 else "?")
    if cur == "rest" and t < T_FL: v = "76%"
    d.text((X0 + 360, 388), v, font=F(BLK, 64), fill=SIG if cur == "reveal" else INK)

def draw(img, d, t, line, note="share of US adults who call it infidelity"):
    shadowed(img, t); d = ImageDraw.Draw(img); labels(d, t); head(d, t, line); fig(d, note)

def sc_hook(img, d, t): draw(img, d, t, "IS FLIRTING CHEATING?")
def sc_setup(img, d, t): draw(img, d, t, "2,000 PEOPLE RATED", note="married person · YouGov 2019")
def sc_explain(img, d, t): draw(img, d, t, "THE SCALE")
def sc_reveal(img, d, t): draw(img, d, t, "MOST AGREE HERE.")
def sc_rest(img, d, t): draw(img, d, t, "BELOW HALF.", note="secret porn = without the partner knowing")
def sc_why(img, d, t): draw(img, d, t, "DIFFERENT LINES." if t < T_BACK else "IS FLIRTING CHEATING?")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.scenes = {"hook": sc_hook, "setup": sc_setup, "explain": sc_explain, "reveal": sc_reveal, "rest": sc_rest, "why": sc_why}
FX = [*[(T_SW + j * (math.pi / 7.0), whoosh(.25, .03), (-.4 if j % 2 else .4)) for j in range(4)], (T_STAMP, thud(.5), .3),
      (T_REW, whoosh(.5, .05), 0), (T_SCALE, pop(.12), -.5), (T_BOT, tick(.03), -.3), (T_TOPL, tick(.03), .3),
      (S("reveal") + .05, thud(.55), 0), (T_EMO, whoosh(.4, .04), .4), (T_FL, pop(.14), .3), (T_EX, pop(.14), .3), (T_PO, pop(.14), .3),
      (T_YOU, pop(.12), -.3), (T_YOU + .35, pop(.12), .3), (T_BACK, whoosh(.6, .05), 0)]
if __name__ == "__main__": EP.run(FX)
