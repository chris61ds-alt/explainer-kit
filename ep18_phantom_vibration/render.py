"""NOT JUST YOU – No. 18: phantom vibrations (Drouin, Kaiser & Miller 2012; Rothberg et al. 2010). Area: body."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "stats": .5, "freq": .45, "why": .5, "name": .5, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "stats", "freq", "why", "name", "point", "end"]
EP = Episode(TL, 18, "PHANTOM BUZZ", order=ORDER,
             chapters={"hook": "BZZZ", "stats": "HOW MANY", "freq": "HOW OFTEN", "why": "WHY", "name": "THE NAME", "point": "LISTENING"},
             sources=("Drouin, Kaiser & Miller (2012), Computers in", "Human Behavior 28 · Rothberg et al. (2010), BMJ"),
             music=dict(bpm=100, root=-2, prog="minor", kick="half", gaps=[(E("hook") - .2, S("stats") + .05)]),
             cover=dict(words=["BZZZ?"], kicker="Your phone didn't buzz."))

def buzz(d, x, y, k, col=SIG):
    for i in range(3):
        r = 40 + i * 26 + 6 * math.sin(k * 40)
        d.arc([x - r, y - r, x + r, y + r], -40, 40, fill=col, width=6); d.arc([x - r, y - r, x + r, y + r], 140, 220, fill=col, width=6)

def sc_hook(img, d, t):
    nd = cue("hook", "didn't")
    d.text((X0 - 6, 300), "BZZZ" if t < nd else "…NOPE.", font=F(BLK, 200), fill=SIG if t < nd else INK)
    h = picto(d, 330, FLOOR, 1.05, INK, f=1, pose=IDLE if t < nd else SHRUG)
    phone(d, 370, 960, .5, INK, lit=t < nd)
    if t < nd: buzz(d, 370, 960, t)
    else:
        phone(d, 680, 760, 1.4, INK)
        d.text((680, 760), "0", font=F(BLK, 90), fill=INK, anchor="mm"); d.text((680, 830), "notifications", font=F(COND, 22), fill=MID, anchor="mm")
    fig(d, "fig. 1 — the phone in your pocket")

def sc_stats(img, d, t):
    t0 = S("stats"); k = clamp((t - cue("stats", "nine")) / 1.0)
    d.text((X0 - 8, 290), "9 / 10", font=F(BLK, 230), fill=SIG)
    d.text((X0, 540), "students had felt one", font=F(COND, 40), fill=INK)
    for i in range(10):
        x = X0 + 50 + i * 86; on = i < 9 and i < 10 * k
        picto(d, x, FLOOR, .42, SIG if on else MID, pose=IDLE)
        if on: buzz(d, x + 10, FLOOR - 120, t + i)
    fig(d, "Drouin, Kaiser & Miller, 2012 · ≈ 89 %")

def sc_freq(img, d, t):
    t0 = S("freq"); nb = cue("freq", "bothersome")
    d.text((X0, 320), "NOW AND THEN", font=F(BLK, 110), fill=INK)
    for i in range(14):
        x = X0 + (i % 7) * 120; y = 470 + (i // 7) * 130
        d.rectangle([x, y, x + 100, y + 110], outline=INK, width=3)
        d.text((x + 10, y + 6), str(i + 1), font=F(COND, 22), fill=MID)
        if i == 9 and t > t0 + .5: buzz(d, x + 50, y + 60, t); d.rectangle([x + 40, y + 40, x + 60, y + 80], fill=SIG)
    if t >= nb - .2:
        k = ease((t - nb + .2) / .5)
        d.text((X0, 790), "bothered?", font=F(COND, 34), fill=INK)
        d.rectangle([X0, 840, X1, 880], outline=INK, width=4); d.rectangle([X0 + 6, 846, X0 + 6 + (X1 - X0 - 12) * .15 * k, 874], fill=SIG)
        d.text((X0, 892), "not at all", font=F(MONO, 20), fill=MID); d.text((X1, 892), "very", font=F(MONO, 20), fill=MID, anchor="ra")
        box_label(d, X0, 960, "MOSTLY: NO", 32, WHITE, INK)
    fig(d, "fig. 2 — a typical two weeks · schematic")

def sc_why(img, d, t):
    t0 = S("why"); al = cue("why", "alert")
    d.text((X0, 320), "ON ALERT", font=F(BLK, 130), fill=INK)
    ox, oy, w = X0, 860, X1 - X0
    rng = np.random.default_rng(4); pts = []
    spikes = {28: "twitch", 60: "shirt", 88: "music"}
    for i in range(120):
        v = rng.uniform(.05, .25) + (0.62 if i in spikes else 0)
        pts.append((ox + w * i / 119, oy - 260 * v))
    prog = clamp((t - t0) / 3.2)
    shown = pts[:max(2, int(len(pts) * prog))]
    d.line(shown, fill=INK, width=3)
    thr = lerp(.85, .55, ease((t - al) / .8))
    d.line([ox, oy - 260 * thr, ox + w, oy - 260 * thr], fill=SIG, width=4)
    d.text((X1, oy - 260 * thr - 30), "your 'it buzzed' line", font=F(COND, 24), fill=SIG, anchor="ra")
    for i, lab in spikes.items():
        if len(shown) > i and t >= cue("why", "twitch") - .2:
            x, y = pts[i]
            if 260 * .87 > 260 * thr: box_label(d, x, y - 60, lab, 24, WHITE, SIG if (oy - y) / 260 > thr else INK, anchor="ma")
    d.line([ox, oy, ox + w, oy], fill=INK, width=2)
    fig(d, "fig. 3 — signal detection: the bar drops, false alarms rise · schematic")

def sc_name(img, d, t):
    words_in(d, t, [("TACTILE", cue("name", "tactile") - .1, 330, 190, INK), ("HALLUCINATION.", cue("name", "hallucination") - .1, 540, 104, SIG)])
    if t >= cue("name", "common"): note(d, 520, 680, 700, 860, "and very common", (t - cue("name", "common")) / .35, INK, anchor="ra", size=30)

def sc_point(img, d, t):
    t0 = S("point")
    words_in(d, t, [("LISTENING", t0, 300, 160, INK), ("TOO HARD.", cue("point", "too hard") - .2, 470, 160, SIG)])
    h = picto(d, 480, FLOOR, .95, INK, pose=IDLE)
    for i in range(4):
        r = 60 + ((t * 90 + i * 40) % 150)
        d.arc([h[0] - r, h[1] - r, h[0] + r, h[1] + r], 200, 340, fill=mix(SIG, BG, r / 220), width=5)
    phone(d, 520, 960, .5, INK)
    fig(d, "fig. 4 — a brain tuned to one signal")

EP.scenes = {"hook": sc_hook, "stats": sc_stats, "freq": sc_freq, "why": sc_why, "name": sc_name, "point": sc_point}
def bzz(amp=.12, dur=.45):
    t = tt_(dur); return amp * np.sign(np.sin(2 * np.pi * 150 * t)) * (np.sin(2 * np.pi * 9 * t) > 0) * np.exp(-t * 2)
FX = [(0.0, bzz(.12), 0), (.15, thud(.4), 0), (cue("hook", "didn't"), rewind_sfx(.12, .35), 0), *EP.cut_fx(),
      (cue("stats", "nine"), thud(.45), 0), (S("freq") + .5, bzz(.07, .3), .2), (cue("freq", "bothersome"), pop(.15), 0),
      (cue("why", "alert"), whoosh(.6, .1), 0), *[(cue("why", w), bzz(.06, .25), (i - 1) / 2) for i, w in enumerate(("twitch", "shirt"))],
      (cue("name", "tactile") - .1, thud(.4), 0), (cue("name", "hallucination") - .1, thud(.35), 0),
      (cue("point", "too hard") - .2, riser(.4, .06), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
