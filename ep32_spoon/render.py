"""NOT JUST YOU – No. 32: semantic satiation (Jakobovits 1962). Area: language."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .3, "demo": .4, "weird": .6, "name": .5, "why": .5, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "demo", "weird", "name", "why", "point", "end"]
EP = Episode(TL, 32, "SPOON", order=ORDER,
             chapters={"hook": "SAY IT", "demo": "AGAIN", "weird": "WAIT…", "name": "THE NAME", "why": "WHY", "point": "TIRED"},
             sources=("Jakobovits (1962), McGill dissertation ·", "Severance & Washburn (1907) · via Wikipedia"),
             music=dict(bpm=92, root=0, prog="dream", kick="half", gaps=[(E("demo") + .05, S("weird") + .05)]),
             cover=dict(words=["SPOON.", "SPOON.", "SPOON?"], kicker="Why words stop making sense."))

def spoon(d, cx, cy, s=1.0, col=INK, rot=0.0):
    a = math.radians(rot); ux, uy = math.cos(a), math.sin(a)
    hx, hy = cx + ux * 80 * s, cy + uy * 80 * s
    d.line([hx, hy, cx + ux * 260 * s, cy + uy * 260 * s], fill=col, width=int(18 * s))
    pts = [(cx + ux * 80 * s * math.cos(q) - uy * 46 * s * math.sin(q), cy + uy * 80 * s * math.cos(q) + ux * 46 * s * math.sin(q)) for q in np.linspace(0, 2 * math.pi, 40)]
    d.polygon(pts, fill=col)

def jitter_word(img, text, x, y, size, col, amt, t, seed=0):
    f = F(BLK, size); dd = ImageDraw.Draw(img); rng = np.random.default_rng(seed); xx = x
    for i, ch in enumerate(text):
        w = dd.textlength(ch, font=f); rot = rng.uniform(-1, 1) * 25 * amt + math.sin(t * 3 + i) * 4 * amt
        dy = rng.uniform(-1, 1) * 40 * amt; dx = rng.uniform(0, 1) * 30 * amt
        lay = Image.new("RGBA", (int(w + 80), int(size * 1.4)), (0, 0, 0, 0)); ImageDraw.Draw(lay).text((40, 0), ch, font=f, fill=col + (255,))
        lay = lay.rotate(rot, resample=Image.BICUBIC); img.paste(lay, (int(xx - 40 + dx), int(y + dy)), lay); xx += w + 6 + dx

def sc_hook(img, d, t):
    d.text((X0 - 6, 300), "SPOON.", font=F(BLK, 230), fill=INK)
    spoon(d, 480, 820, 1.4, SIG, rot=-30)
    ag = [m.start() for m in __import__("re").finditer("Again", TL.T["hook"]["text"])]
    n = sum(1 for i in ag if t >= S("hook") + TL.T["hook"]["dur"] * i / len(TL.T["hook"]["text"]))
    box_label(d, X1, 560, f"×{n + 1}", 60, WHITE, INK, anchor="ra")
    fig(d, "fig. 1 — say it out loud")

def sc_demo(img, d, t):
    t0 = S("demo"); n = int(clamp((t - t0) / TL.T["demo"]["dur"]) * 18) + 1
    for i in range(n):
        r, c = divmod(i, 3); x = X0 + c * 290; y = 320 + r * 130
        fade = i / 18
        d.text((x, y), "SPOON", font=F(BLK, 74), fill=mix(INK, RULE, fade) if i < n - 1 else SIG)
    fig(d, "fig. 2 — still a word?")

def sc_weird(img, d, t):
    t0 = S("weird")
    jitter_word(img, "SPOON", X0, 520, 230, INK, ease((t - t0) / 1.6), t, seed=3)
    if t >= cue("weird", "stops"): note(d, 700, 760, 860, 1000, "…is that even a word?", (t - cue("weird", "stops")) / .4, SIG, anchor="ra", size=30)
    fig(d, "fig. 3 — just shapes and sounds")

def sc_name(img, d, t):
    words_in(d, t, [("SEMANTIC", cue("name", "semantic") - .1, 320, 170, INK), ("SATIATION.", cue("name", "satiation") - .1, 500, 156, SIG)])
    if t >= cue("name", "nineteen"):
        box_label(d, X0, 760, "NAMED IN 1962", 40, WHITE, INK); d.text((X0, 840), "Leon Jakobovits James, McGill University", font=F(COND, 30), fill=INK)

def battery(d, x, y, w, h, v):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=6); d.rectangle([x + w, y + h * .3, x + w + 16, y + h * .7], fill=INK)
    d.rectangle([x + 10, y + 10, x + 10 + (w - 20) * v, y + h - 10], fill=SIG if v < .3 else INK)

def sc_why(img, d, t):
    t0 = S("why"); tr = cue("why", "tired")
    d.text((X0, 320), "WORN OUT", font=F(BLK, 130), fill=INK)
    box_label(d, X0 + 10, 560, "spoon", 60, WHITE, INK)
    spoon(d, 700, 600, .7, INK, rot=-20)
    v = 1 - ease((t - t0 - .3) / max(.5, TL.T["why"]["dur"] - .6))
    for i in range(8):
        x = lerp(X0 + 230, 600, i / 8)
        if (i / 8) < v + .1: d.line([x, 600, x + 30, 600], fill=mix(RULE, SIG, v), width=int(4 + 8 * v))
    d.text((X0 + 300, 520), "link to the meaning", font=F(COND, 26), fill=MID)
    battery(d, X0 + 60, 820, 400, 160, max(.05, v))
    if t >= tr: note(d, X0 + 470, 900, 860, 1060, "like a muscle", (t - tr) / .35, SIG, anchor="ra", size=30)

def sc_point(img, d, t):
    t0 = S("point"); tr = cue("point", "tired of")
    words_in(d, t, [("NOT A", t0, 300, 150, INK), ("GLITCH.", t0 + .2, 450, 150, INK)] if t < tr - .1 else [("TIRED OF", tr - .1, 300, 150, INK), ("SPOON.", tr + .2, 450, 190, SIG)])
    spoon(d, 300, 960, 1.1, INK, rot=0)
    for i in range(3): d.text((680 + i * 40, 880 - i * 34), "z", font=F(BLK, 34 + i * 10), fill=MID)
    fig(d, "fig. 4 — give it a minute, it comes back")

EP.scenes = {"hook": sc_hook, "demo": sc_demo, "weird": sc_weird, "name": sc_name, "why": sc_why, "point": sc_point}
FX = [(0.0, thud(.5), 0), *[(S("demo") + i * TL.T["demo"]["dur"] / 6, tick(.05), (i % 3 - 1) * .5) for i in range(6)], *EP.cut_fx(),
      (S("weird") + .05, rewind_sfx(.12, .8), 0), (cue("name", "semantic") - .1, thud(.4), 0), (cue("name", "satiation") - .1, thud(.4), 0),
      (cue("name", "nineteen"), pop(.15), 0), (cue("why", "tired"), whoosh(.5, .08), 0), (cue("point", "tired of"), thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
