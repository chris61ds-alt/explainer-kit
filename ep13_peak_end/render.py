"""NOT JUST YOU – No. 13: the peak-end rule (Kahneman, Fredrickson, Schreiber & Redelmeier 1993). Look: Swiss Detail v2."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .4, "short": .4, "long": .5, "ask": .9, "choice": .5, "name": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "short", "long", "ask", "choice", "name", "point", "end"]
EP = Episode(TL, 13, "THE GOOD ENDING", order=ORDER,
             chapters={"hook": "MORE PAIN?", "short": "TRIAL A", "long": "TRIAL B", "ask": "THE CHOICE", "choice": "THE ANSWER",
                       "name": "THE RULE", "point": "THE ENDING"},
             sources=("Kahneman, Fredrickson, Schreiber & Redelmeier", "(1993), Psychological Science 4(6)"),
             music=dict(bpm=84, root=-3, prog="tense", kick="half", gaps=[(S("ask") - .1, S("choice") + .05)]),
             cover=dict(words=["MORE", "PAIN?"], kicker="Why endings rule your memory."))

def pain_a(sec): return .86 + .012 * math.sin(sec * .6) if sec <= 60 else None
def pain_b(sec):
    if sec <= 60: return .86 + .012 * math.sin(sec * .6 + 1)
    if sec <= 90: return lerp(.86, .58, (sec - 60) / 30)
    return None

def graph(d, box, fn, k, col, label, total=90, fill=False, marks=False, t=0.0):
    x0, y0, x1, y1 = box
    d.line([x0, y1, x1, y1], fill=INK, width=3); d.line([x0, y0, x0, y1], fill=INK, width=3)
    for sec in (0, 30, 60, 90):
        x = x0 + (x1 - x0) * sec / total; d.line([x, y1, x, y1 + 10], fill=INK, width=2)
        d.text((x, y1 + 16), f"{sec}s", font=F(MONO, 18), fill=MID, anchor="ma")
    d.text((x0 + 10, y0 - 34), label, font=F(COND, 28), fill=col)
    pts = []
    for i in range(0, 181):
        sec = i / 2
        if sec > total * k: break
        v = fn(sec)
        if v is None: break
        pts.append((x0 + (x1 - x0) * sec / total, y1 - (y1 - y0) * v))
    if len(pts) > 1:
        if fill: d.polygon([(pts[0][0], y1)] + pts + [(pts[-1][0], y1)], fill=SIG_L if col == SIG else RULE)
        d.line(pts, fill=col, width=6)
    return pts

def tank(d, x, y, w, h, t, temp, k=1.0):
    if k <= 0: return
    d.rectangle([x, y, x + w, y + h], outline=INK, width=6)
    wy = y + 40
    d.rectangle([x + 6, wy, x + w - 6, y + h - 6], fill=RULE)
    pts = [(x + 6 + i * 8, wy + 4 * math.sin(t * 4 + i * .6)) for i in range(int((w - 12) / 8) + 1)]
    d.line(pts, fill=INK, width=3)
    for i, (ix, iy) in enumerate(((x + 30, wy + 20), (x + w - 80, wy + 50))):
        d.rectangle([ix, iy + 3 * math.sin(t * 2 + i), ix + 40, iy + 40 + 3 * math.sin(t * 2 + i)], outline=INK, width=3)
    # thermometer
    tx = x + w + 50
    d.rounded_rectangle([tx - 14, y - 40, tx + 14, y + h - 40], radius=14, outline=INK, width=4)
    d.ellipse([tx - 26, y + h - 60, tx + 26, y + h - 8], fill=SIG)
    lvl = (temp - 10) / 8
    d.rectangle([tx - 7, y + h - 50 - (h - 30) * lvl, tx + 7, y + h - 40], fill=SIG)
    d.text((tx + 30, y + h - 60 - (h - 30) * lvl), f"{temp:.1f} °C".replace(".0 ", " "), font=F(MONO, 24), fill=INK, anchor="lm")

# ---------------------------------------------------------------- actor
TG = {"hook": (480, 1.0, 0), "short": (210, .8, 700), "long": (210, .8, 700), "ask": (480, 1.0, 0), "choice": (480, 1.0, 0),
      "name": (480, 1.0, 700), "point": (760, .9, 0)}
DIP = {"arms": ((60, 30), (-10, -5)), "tilt": 6}
POSE = [(0, SHRUG), (S("short"), DIP), (S("ask"), WORRY), (cue("choice", "longer") - .2, {"arms": ((100, 95), (-10, -5))}),
        (S("point"), IDLE), (cue("point", "good ending"), WAVE)]
def actor(img, d, t, cur):
    i = ORDER.index(cur); prev = ORDER[max(0, i - 1)]
    k = ease_io((t - S(cur) + .05) / .55) if i else 1
    x, s, dy = (lerp(a, b, k) for a, b in zip(TG[prev], TG[cur]))
    if dy < 650: picto(d, x, FLOOR + dy, s, INK, f=1, pose=pose_seq(t, POSE))
EP.layers.append(actor)

# ---------------------------------------------------------------- scenes
def choice_cards(d, t, hi=None, k=1.0):
    for i, (lab, sub) in enumerate((("A", "60 s"), ("B", "90 s"))):
        x = X0 + 40 + i * 500; y = 560
        on = hi == i
        d.rectangle([x, y, x + 300, y + 230], fill=SIG if on else None, outline=INK, width=6)
        d.text((x + 150, y + 95), lab, font=F(BLK, 140), fill=WHITE if on else INK, anchor="mm")
        d.text((x + 150, y + 195), sub, font=F(COND, 34), fill=WHITE if on else INK, anchor="mm")

def sc_hook(img, d, t):
    giant(d, "MORE PAIN.", size=166)
    choice_cards(d, t, hi=1 if t >= cue("hook", "voluntarily") else None)
    if t >= cue("hook", "voluntarily"):
        note(d, X0 + 690, 600, 860, 470, "on purpose", (t - cue("hook", "voluntarily")) / .35, SIG, anchor="ra", size=28)

def sc_short(img, d, t):
    t0 = S("short"); ks = clamp((t - cue("short", "sixty") + .5) / 2.0)
    d.text((X0, 320), "TRIAL A", font=F(BLK, 110), fill=INK)
    tank(d, 330, 460, 330, 260, t, 14.0)
    graph(d, (X0 + 20, 860, X1 - 20, 1080), pain_a, ks * 60 / 90 * 1.5 if ks < 1 else 1, INK, "discomfort", fill=True)
    d.text((X1, 330), f"0:{int(60 * ks):02d}", font=F(MONO, 60), fill=SIG, anchor="ra")
    fig(d, "Kahneman et al. — Psychological Science, 1993")

def sc_long(img, d, t):
    t0 = S("long"); kp = clamp((t - cue("long", "plus") + .2) / 2.2)
    d.text((X0, 320), "TRIAL B", font=F(BLK, 110), fill=SIG)
    temp = 14.0 + 1.0 * kp
    tank(d, 330, 460, 330, 260, t, temp)
    graph(d, (X0 + 20, 860, X1 - 20, 1080), pain_a, 1, MID, "", fill=False)
    pts = graph(d, (X0 + 20, 860, X1 - 20, 1080), pain_b, (60 + 30 * kp) / 90 if t >= cue("long", "plus") - .2 else 60 / 90, SIG, "discomfort", fill=True)
    sec = 60 + int(30 * kp) if t >= cue("long", "plus") - .2 else 60
    d.text((X1, 330), f"{sec // 60}:{sec % 60:02d}", font=F(MONO, 60), fill=SIG, anchor="ra")
    if kp > .95: note(d, X1 - 80, 990, X1 - 60, 800, "a bit less cold", (t - cue("long", "warmer")) / .4, SIG, anchor="ra", size=26)

def sc_ask(img, d, t):
    t0 = S("ask")
    giant(d, "REPEAT?", size=200, k=(t - t0) / .3)
    choice_cards(d, t)
    fig(d, "one of them, once more")

def sc_choice(img, d, t):
    t0 = S("choice"); lg = cue("choice", "longer")
    choice_cards(d, t, hi=1 if t >= lg - .1 else None)
    k = clamp((t - lg) / .9)
    for i in range(32):
        r, c = divmod(i, 16); x = X0 + 30 + c * 52; y = 360 + r * 52
        col = SIG if i < 22 and i < 32 * k * 1.2 else (RULE if i >= 22 else INK)
        d.ellipse([x - 16, y - 16, x + 16, y + 16], fill=col if k > 0 else RULE)
    if k > .6: box_label(d, X0 + 690, 820, "22 OF 32", 40, WHITE, SIG, anchor="ma")
    fig(d, "participants who chose to repeat B · 69 %")

def sc_name(img, d, t):
    t0 = S("name"); pk = cue("name", "worst"); en = cue("name", "ending")
    box = (X0 + 20, 560, X1 - 20, 1030)
    pts = graph(d, box, pain_b, 1, SIG, "", fill=True)
    d.text((box[2], box[1] - 40), "trial B · discomfort", font=F(COND, 26), fill=SIG, anchor="ra")
    # 'minutes' fade out, peak + end stay
    if t >= cue("name", "minutes"):
        k = ease((t - cue("name", "minutes")) / .4)
        dim_h(d, box[0], box[2], 1110, 1, mix(BG, INK, 1 - k * .7), None)
        d.text((480, 1124), "duration: ignored", font=F(COND, 26), fill=mix(BG, MID, k), anchor="ma")
    if t >= pk - .1:
        px, py = pts[40]; d.ellipse([px - 16, py - 16, px + 16, py + 16], fill=INK)
        box_label(d, px, py - 70, "PEAK", 30, WHITE, INK, anchor="ma")
    if t >= en - .1:
        ex, ey = pts[-1]; d.ellipse([ex - 16, ey - 16, ex + 16, ey + 16], fill=INK)
        box_label(d, ex, ey - 70, "END", 30, WHITE, INK, anchor="ra")
    kr = (t - cue("name", "peak end") + .1) / .35
    if kr > 0: d.text((X0 - 8 - (1 - ease(kr)) * 80, 300), "PEAK + END", font=F(BLK, 150), fill=mix(BG, SIG, ease(kr)))
    else: d.text((X0, 320), "MEMORY", font=F(BLK, 110), fill=INK)

def sc_point(img, d, t):
    t0 = S("point"); ge = cue("point", "good ending")
    giant(d, "GOOD ENDING.", size=120, k=(t - ge + .1) / .35) if t >= ge - .1 else giant(d, "WANT A GOOD", size=120, k=(t - t0) / .3)
    # a holiday as a strip of days, the last one highlighted
    n = 7
    for i in range(n):
        x = X0 + i * 90; kk = ease((t - t0 - .1 - i * .05) / .3)
        if kk <= 0: continue
        last = i == n - 1
        d.rectangle([x, 520, x + 76, 640], fill=SIG if (last and t >= ge) else None, outline=INK, width=4)
        d.text((x + 38, 580), f"D{i + 1}", font=F(COND, 28), fill=WHITE if (last and t >= ge) else INK, anchor="mm")
    if t >= ge: note(d, X0 + 6 * 90 + 38, 650, X0 + 250, 780, "the part you'll remember", (t - ge - .2) / .4, SIG, anchor="la", size=28)
    fig(d, "fig. 1 — a holiday, a date, a meeting, a day")

EP.scenes = {"hook": sc_hook, "short": sc_short, "long": sc_long, "ask": sc_ask, "choice": sc_choice, "name": sc_name, "point": sc_point}

FX = [(0.0, thud(.55), 0), (cue("hook", "voluntarily"), pop(.2), .3),
      *EP.cut_fx(),
      (cue("short", "cold"), whoosh(.5, .1), 0), *[(cue("short", "sixty") + i * .5, tick(.05), 0) for i in range(4)],
      (cue("long", "plus"), riser(1.6, .07), 0),
      (S("ask"), thud(.4), 0),
      (cue("choice", "longer"), thud(.6), 0), *[(cue("choice", "longer") + .05 + i * .035, tick(.04), (i % 5 - 2) / 3) for i in range(22)],
      (cue("name", "worst"), pop(.18), -.2), (cue("name", "ending"), pop(.18), .2), (cue("name", "peak end"), thud(.5), 0),
      (cue("point", "good ending"), thud(.45), 0), (cue("point", "good ending") + .1, riser(.4, .06), 0),
      (S("end"), thud(.5), 0)]

if __name__ == "__main__": EP.run(FX)
