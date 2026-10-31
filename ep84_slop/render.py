"""NOT JUST YOU – No. 84: can you spot AI slop? (Astral Codex Ten AI Art Turing Test, 2024). Look C+D, dark."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from thread import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .6, "study": .6, "result": .6, "fav": .6, "haters": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "fav", "haters", "point", "end"]
EP = ThreadEpisode(TL, 84, "SLOP", order=ORDER, dark=True, label="ONLINE SURVEY · 11,000 READERS",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Scott Alexander (2024), How Did You Do On", "The AI Art Turing Test? · Astral Codex Ten"),
                   music=dict(bpm=96, root=-2, prog="tense", kick="four", gaps=[(E("study") + .05, S("result") + .05)]),
                   cover=dict(words=["SPOT THE", "SLOP?"], kicker="Most people can't."))

def scene_mask(m, x0, y0, w, h, kind=0):
    """a little 'painting' motif for halftone: hills + sun (kind 0) or sea + cliff (kind 1)"""
    if kind == 0:
        m.ellipse([x0 + w * .62, y0 + h * .12, x0 + w * .86, y0 + h * .36], fill=255)
        pts = [(x0 + w * u, y0 + h * (.62 + .12 * math.sin(u * 7 + 1))) for u in np.linspace(0, 1, 30)]
    else:
        m.polygon([(x0, y0 + h * .3), (x0 + w * .35, y0 + h * .45), (x0 + w * .35, y0 + h), (x0, y0 + h)], fill=255)
        pts = [(x0 + w * u, y0 + h * (.72 + .03 * math.sin(u * 20))) for u in np.linspace(0, 1, 30)]
    m.polygon(pts + [(x0 + w, y0 + h), (x0, y0 + h)], fill=255)

def painting(img, d, x0, y0, w, h, kind=0, col=INK, frame=INK, cell=7):
    d.rectangle([x0 - 10, y0 - 10, x0 + w + 10, y0 + h + 10], outline=frame, width=6)
    silhouette(img, lambda m: scene_mask(m, x0, y0, w, h, kind), (int(x0), int(y0), int(x0 + w), int(y0 + h)), col, cell=cell)

def sc_hook(img, d, t):
    tm = cue("hook", "most people") - .3
    d.text((X0 - 6, 300), "SPOT THE", font=F(BLK, 150), fill=INK); d.text((X0 - 6, 450), "SLOP?", font=F(BLK, 210), fill=SIG)
    painting(img, d, X0 + 10, 730, 360, 300, 0, INK); painting(img, d, X0 + 460, 730, 360, 300, 1, MID)
    if t >= tm:
        box_label(d, X0 + 190, 1060, "AI?", 44, WHITE, SIG, font=BLK, anchor="ma"); box_label(d, X0 + 640, 1060, "HUMAN?", 44, WHITE, INK, font=BLK, anchor="ma")
    fig(d, "Merriam-Webster word of the year 2025: slop")

def sc_study(img, d, t):
    t0 = S("study")
    counter(d, X0, 320, t, t0 + .1, .8, 11000, "{:,.0f}", 200, SIG)
    d.text((X0 + 6, 540), "people · 50 pictures · human or AI?", font=F(COND, 40), fill=INK)
    k = clamp((t - t0 - .4) / 1.6)
    for i in range(int(50 * k)):
        r, c = divmod(i, 10); x = X0 + 6 + c * 84; y = 640 + r * 92
        d.rectangle([x, y, x + 68, y + 76], outline=INK if i % 3 else MID, width=4)
        d.line([x + 8, y + 58, x + 30, y + 40, x + 46, y + 52, x + 60, y + 34], fill=SIG if i % 7 == 0 else MID, width=3)
    fig(d, "online test, 2024")

def sc_result(img, d, t):
    t0, tg = S("result"), cue("result", "guessing") - .3
    counter(d, X0, 320, t, t0 + .1, .7, 60, "{:.0f} %", 240, SIG)
    d.text((X0 + 6, 580), "median score", font=F(COND, 42), fill=INK)
    k = ease((t - t0 - .3) / .7)
    d.rectangle([X0, 700, X0 + 840 * .6 * k, 790], fill=SIG); d.text((X0 + 840 * .6 * k + 14, 745), "the crowd", font=F(BLK, 34), fill=SIG, anchor="lm")
    if t >= tg:
        k2 = ease((t - tg) / .5)
        d.rectangle([X0, 840, X0 + 840 * .5 * k2, 930], fill=MID); d.text((X0 + 840 * .5 * k2 + 14, 885), "coin flip: 50 %", font=F(BLK, 34), fill=MID, anchor="lm")
    fig(d, "barely better than chance")

def sc_fav(img, d, t):
    t0, ta = S("fav"), cue("fav", "made by ai") - .3
    d.text((X0, 320), "MOST LIKED", font=F(BLK, 130), fill=INK); d.text((X0, 460), "PICTURE:", font=F(BLK, 130), fill=INK)
    painting(img, d, X0 + 10, 650, 560, 420, 0, SIG if t >= ta else INK, cell=8)
    if t >= ta:
        bbox(d, (X0 + 10, 650, X0 + 570, 1070), "AI", SIG, (t - ta) / .3, coords=False)
        box_label(d, X0 + 610, 820, "MADE", 50, WHITE, INK, font=BLK); box_label(d, X0 + 610, 900, "BY AI.", 50, WHITE, SIG, font=BLK)
        if t < ta + .3: glitch(img, (X0, 640, X0 + 580, 1080), 1.0, seed=int(t * 30))
    fig(d, "\"Riverside Cafe\"")

def sc_haters(img, d, t):
    t0, th = S("haters"), cue("haters", "half") - .3
    d.text((X0, 320), "AI HATERS'", font=F(BLK, 130), fill=INK); d.text((X0, 460), "TOP 10:", font=F(BLK, 130), fill=SIG)
    for i in range(10):
        r, c = divmod(i, 5); x = X0 + c * 168; y = 680 + r * 200; ai = i in (0, 2, 3, 6, 8)
        k = ease((t - t0 - .4 - i * .08) / .3)
        if k <= 0: continue
        d.rectangle([x, y, x + 140, y + 160], outline=INK, width=5, fill=SIG if (ai and t >= th) else None)
        d.text((x + 70, y + 80), "AI" if (ai and t >= th) else str(i + 1), font=F(BLK, 50), fill=WHITE if (ai and t >= th) else INK, anchor="mm")
    fig(d, "1,278 people who rated AI art 1 of 5")

def sc_point(img, d, t):
    t0, tk = S("point"), cue("point", "knowing") - .3
    words_in(d, t, [("WE DON'T", t0 + .1, 320, 140, MID), ("HATE SLOP.", t0 + .4, 470, 140, INK)] + ([("WE HATE", tk - .2, 650, 140, INK), ("KNOWING.", tk + .1, 800, 170, SIG)] if t >= tk - .2 else []))
    fig(d, "fig. 2 — taste, until the label")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "fav": sc_fav, "haters": sc_haters, "point": sc_point}
FX = [(0.0, thud(.5), 0), (cue("hook", "most people") - .3, pop(.15), 0), *EP.cut_fx(), (S("study") + .1, riser(.8, .04), 0),
      *[(S("study") + .4 + i * .2, tick(.03), (i % 5 - 2) / 3) for i in range(8)], (S("result") + .05, thud(.55), 0), (cue("result", "guessing") - .3, pop(.15), 0),
      (cue("fav", "made by ai") - .3, rewind_sfx(.12, .3), 0), *[(S("haters") + .4 + i * .08, tick(.035), 0) for i in range(10)], (cue("haters", "half") - .3, thud(.45), 0),
      (cue("point", "knowing") - .3, thud(.5), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
