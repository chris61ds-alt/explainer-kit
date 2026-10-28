"""NOT JUST YOU – No. 54 (v3 'Swiss Thread' test): people detect lies at 54 % (Bond & DePaulo 2006).
The thread is a polygraph trace that runs through the whole video. Default light; set V3_DARK=1 for the dark variant."""
import os, sys, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from thread import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .8, "result": .5, "lies": .5, "why": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "lies", "why", "point", "end"]
DARK = os.environ.get("V3_DARK") == "1"         # default: light (closest to the reference look)
EP = ThreadEpisode(TL, 54, "LIE DETECTOR", order=ORDER, dark=DARK,
                   chapters={"hook": "SUBJECT 01", "study": "24,483 JUDGES", "result": "THE SCORE", "lies": "THE LIES", "why": "TRUTH BIAS", "point": "THE COIN"},
                   sources=("Bond & DePaulo (2006), Personality and", "Social Psychology Review 10(3)"),
                   music=dict(bpm=96, root=-3, prog="minor", kick="four", gaps=[(E("study") + .05, S("result") + .05)]),
                   cover=dict(words=["YOU CAN'T", "SPOT A LIE."], kicker="54 %. A coin gets 50."))

LIES = ["LIE", "LÜGE", "MENTIRA", "ЛОЖЬ", "LIAR?", "ψέμα", "MENSONGE", "BUGIA", "LEUGEN"]

def bust(d, cx, cy, s=1.0, col=255, nose=0):
    """profile bust facing right (for halftone masks): egg-shaped head, jaw, small nose, neck, shoulders"""
    d.ellipse([cx - 105 * s, cy - 150 * s, cx + 95 * s, cy + 85 * s], fill=col)
    d.polygon([(cx + 85 * s, cy), (cx + 98 * s, cy + 55 * s), (cx + 62 * s, cy + 112 * s), (cx - 10 * s, cy + 122 * s), (cx - 50 * s, cy + 60 * s)], fill=col)
    d.polygon([(cx + 88 * s, cy - 42 * s), (cx + 122 * s + nose * s, cy + 4 * s), (cx + 88 * s, cy + 14 * s)], fill=col)
    d.rectangle([cx - 48 * s, cy + 80 * s, cx + 30 * s, cy + 200 * s], fill=col)
    d.rounded_rectangle([cx - 250 * s, cy + 175 * s, cx + 200 * s, cy + 440 * s], radius=int(140 * s), fill=col)

def coin(d, cx, cy, r, t, spin=True, face="50 %", col=SIG):
    w = max(.06, abs(math.cos(t * 9))) if spin else 1.0
    d.ellipse([cx - r * w, cy - r, cx + r * w, cy + r], outline=col, width=8)
    if w > .55: d.text((cx, cy), face, font=F(BLK, int(r * .5)), fill=col, anchor="mm")

def edge_thread(d, mid_pts, k=1.0, col=SIG):
    return draw_thread(d, path((LX, THREAD_Y), *mid_pts, (RX, THREAD_Y)), k, col)

# ---------------------------------------------------------------- HOOK: grid of 'lie' → subject → YOU CAN'T
def sc_hook(img, d, t):
    tb, tc = cue("hook", "when someone") - .1, cue("hook", "you can't") - .15
    if t < tb:                                                     # A: multilingual grid, glitching
        cw, ch = (X1 - X0) / 3, 190
        for i, w_ in enumerate(LIES):
            r, c = divmod(i, 3); x, y = X0 + c * cw, 320 + r * ch
            d.rectangle([x, y, x + cw, y + ch], outline=RULE, width=2)
            centre = i == 4
            d.text((x + cw / 2, y + ch / 2), w_, font=F(BLK, 74 if centre else 44), fill=SIG if centre else INK, anchor="mm")
        g = int(t * 12)
        cell = [0, 2, 6, 8, 1, 3, 5, 7][g % 8]; r, c = divmod(cell, 3)
        glitch(img, (X0 + c * cw, 320 + r * ch, X0 + (c + 1) * cw, 320 + (r + 1) * ch), 1.0, seed=g, pixel=6 if g % 2 else 0)
        pts = trace(LX, RX, THREAD_Y + 120, t, amp=16, seed=3, spikes=[(.5, 3 + 2 * math.sin(t * 5), .05)])
        d.line(pts, fill=SIG, width=6)
    elif t < tc:                                                   # B: subject under observation
        k = ease((t - tb) / .4)
        halftone(img, lambda m: bust(m, 400, 560, 1.0, 255, nose=8 + 14 * (.5 + .5 * math.sin(t * 4))), (100, 330, 900, 1100), cell=13, col=INK, k=k)
        bbox(d, (250, 380, 580, 720), "SUBJECT 01", SIG, (t - tb - .2) / .35)
        for j, (lab, amp, sp) in enumerate((("PULSE", 26, (.62, 2.5, .04)), ("VOICE", 14, (.4, 1.5, .08)), ("EYES", 10, (.8, 3, .03)))):
            y = 1010 + j * 48
            track(d, 200, X1, y, lab, trace(200, X1, y, t, amp=amp * .4, seed=j + 5, spikes=[sp], step=5), INK if j else SIG)
        d.line(trace(LX, RX, THREAD_Y + 60, t, amp=10, seed=3), fill=SIG, width=6)
    else:                                                           # C: the verdict
        words_in(d, t, [("YOU", tc, 320, 230, INK), ("CAN'T", tc + .12, 540, 230, SIG), ("TELL.", tc + .24, 760, 120, INK)])
        if t < tc + .25: glitch(img, (X0, 320, X1, 780), 1.4, seed=int(t * 30), pixel=8)
        edge_thread(d, [(300, THREAD_Y + 40), (520, THREAD_Y + 40), (560, THREAD_Y - 120), (600, THREAD_Y + 120), (640, THREAD_Y + 40), (900, THREAD_Y + 40)])
    fig(d, "fig. 1 — you, staring very hard")

# ---------------------------------------------------------------- STUDY: 206 studies → 24,483 judges
def sc_study(img, d, t):
    t0, tj = S("study"), cue("study", "almost twenty-five") - .2
    if t < tj:
        counter(d, X0, 320, t, t0 + .1, .9, 206, "{:.0f}", 230, SIG)
        d.text((X0 + 6, 560), "studies, pooled", font=F(COND, 40), fill=INK)
        n = int(24 * clamp((t - t0 - .2) / 1.2))
        for i in range(n):
            x = 520 + (i % 6) * 8; y = 700 - i * 14
            d.rectangle([x, y, x + 300, y + 190], fill=BG, outline=INK, width=3)
        if n: d.rectangle([520 + ((n - 1) % 6) * 8 + 24, 700 - (n - 1) * 14 + 30, 520 + ((n - 1) % 6) * 8 + 200, 700 - (n - 1) * 14 + 44], fill=SIG)
        edge_thread(d, [(200, THREAD_Y), (480, THREAD_Y + 20), (860, THREAD_Y + 20), (960, THREAD_Y)])
    else:
        counter(d, X0, 320, t, tj, 1.1, 24483, "{:,.0f}", 190, SIG)
        d.text((X0 + 6, 530), "people judging lie or truth", font=F(COND, 40), fill=INK)
        dot_field(d, (X0 + 14, 620, X1, 840), t, cell=28, col=MID, hit={17, 64, 101})
        bbox(d, (X0 + 14 + 17 % 30 * 28 - 22, 620 + 17 // 30 * 28 - 22, X0 + 14 + 17 % 30 * 28 + 22, 620 + 17 // 30 * 28 + 22), "JUDGE #18,204", SIG,
             (t - tj - .6) / .3, coords=False)
        edge_thread(d, [(260, THREAD_Y + 10), (700, THREAD_Y + 10)])
    fig(d, "meta-analysis · Bond & DePaulo, 2006")

# ---------------------------------------------------------------- RESULT: 54 % gauge → coin 50 %
def sc_result(img, d, t):
    t0, tc = S("result"), cue("result", "a coin") - .15
    counter(d, X0, 320, t, t0 + .1, .9, 54, "{:.0f} %", 230, SIG)
    d.text((X0 + 6, 560), "correct, overall", font=F(COND, 40), fill=INK)
    gx0, gx1, gy = X0 + 20, X1 - 20, THREAD_Y
    for v in (0, 50, 100):
        x = lerp(gx0, gx1, v / 100); d.line([x, gy - 40, x, gy + 40], fill=INK if v != 50 else MID, width=3)
        d.text((x, gy + 52), f"{v}", font=F(MONO, 22), fill=MID, anchor="ma")
    d.text((lerp(gx0, gx1, .5), gy - 50), "CHANCE", font=F(MONO, 20), fill=MID, anchor="md")
    k = clamp((t - t0 - .1) / .9); xe = lerp(gx0, gx1, .54 * k)
    if t < tc:
        draw_thread(d, [(LX, gy), (gx0, gy), (xe, gy)], 1, SIG, smooth=False)
        d.ellipse([xe - 14, gy - 14, xe + 14, gy + 14], fill=SIG)
        if k >= 1: box_label(d, xe + 24, gy - 110, "+4 POINTS", 30, WHITE, INK)
    else:                                                           # the thread loops into a coin
        cx, cy, r = 700, gy - 200, 120; kk = ease((t - tc) / .5)
        loop = [(cx + r * math.sin(a), cy + r * math.cos(a)) for a in np.linspace(0, 2 * math.pi * kk, 40)]
        d.line([(LX, gy), (lerp(gx0, gx1, .54), gy), (cx, cy + r)] + loop, fill=SIG, width=7, joint="curve")
        if kk >= 1: coin(d, cx, cy, r, t, True, "50 %")
        d.line([(cx, cy + r), (cx + 120, gy), (RX, gy)], fill=SIG, width=7)
        box_label(d, X0, 640, "A COIN FLIP: 50 %", 36, WHITE, INK)
    fig(d, "accuracy of lie–truth judgments")

# ---------------------------------------------------------------- LIES: scanner over ten subjects
def sc_lies(img, d, t):
    t0, tf = S("lies"), cue("lies", "forty-seven") - .3
    d.text((X0, 320), "LIES CAUGHT", font=F(BLK, 120), fill=INK)
    counter(d, X0, 460, t, tf, .6, 47, "{:.0f} %", 190, SIG)
    xs = [X0 + 50 + i * 88 for i in range(10)]
    sx = lerp(X0, X1, clamp((t - t0 - .2) / 2.4))                     # scanner position
    def figs(m):
        for i, x in enumerate(xs): picto(m, x, 1110, .42, 255, f=1, pose=IDLE)
    halftone(img, figs, (X0, 760, X1 + 30, 1120), cell=8, col=MID)
    for i, x in enumerate(xs):
        caught = i < 4 or (i == 4 and t > tf + .6)
        if caught and sx > x:
            picto(d, x, 1110, .42, SIG, f=1, pose=IDLE)
            bbox(d, (x - 40, 840, x + 40, 1120), "CAUGHT" if i == 0 else None, SIG, (t - t0 - .2 - (x - X0) / 840 * 2.4) / .3, coords=False, size=16)
    d.line([sx, 740, sx, 1130], fill=SIG, width=3)
    draw_thread(d, [(LX, THREAD_Y), (sx, THREAD_Y)], 1, SIG, smooth=False)
    d.line(trace(sx, RX, THREAD_Y, t, amp=6, seed=9, step=8), fill=MID, width=3)
    d.text((X1, 1146), "less than half · truths: 61 %", font=F(MED, 22), fill=MID, anchor="ra")

# ---------------------------------------------------------------- WHY: conveyor of messages through 'your gut'
def sc_why(img, d, t):
    t0, ts = S("why"), cue("why", "slip right")
    d.text((X0, 320), "TRUTH BIAS", font=F(BLK, 150), fill=INK)
    d.text((X0, 480), "we assume honesty", font=F(COND, 46), fill=SIG)
    gx = 480
    d.rectangle([gx - 70, THREAD_Y - 150, gx + 70, THREAD_Y + 150], outline=INK, width=4)
    d.text((gx, THREAD_Y + 170), "YOUR GUT", font=F(MONO, 22), fill=INK, anchor="ma")
    draw_thread(d, [(LX, THREAD_Y), (RX, THREAD_Y)], 1, SIG, smooth=False)
    msgs = [("truth", 0), ("truth", 1), ("lie", 2), ("truth", 3), ("lie", 4), ("truth", 5), ("lie", 6)]
    for lab, i in msgs:
        x = (t - t0) * 260 - i * 170 + 60
        if -120 < x < W + 40:
            lie = lab == "lie"
            box_label(d, x, THREAD_Y - 84, lab, 44, WHITE, SIG if lie else INK, anchor="ma")
            if lie and x > gx + 80 and t >= ts - .4: d.text((x, THREAD_Y + 20), "slipped through", font=F(MONO, 18), fill=SIG, anchor="ma")
    if t >= ts - .2: box_label(d, X1, 600, "MOST LIES PASS", 36, WHITE, SIG, anchor="ra")
    fig(d, "most messages are judged as true")

# ---------------------------------------------------------------- POINT: your gut = a coin, with confidence
def sc_point(img, d, t):
    t0, tc, tw = S("point"), cue("point", "coin flip") - .2, cue("point", "with confidence")
    words_in(d, t, [("YOUR GUT", t0, 320, 160, INK), ("= A COIN.", tc, 480, 160, SIG)])
    cx, cy, r = 480, THREAD_Y + 40, 130
    if t >= tc:
        kk = ease((t - tc) / .5)
        loop = [(cx + r * math.sin(a), cy + r * math.cos(a)) for a in np.linspace(0, 2 * math.pi * kk, 40)]
        d.line([(LX, THREAD_Y), (cx - 200, THREAD_Y), (cx, cy + r)] + loop, fill=SIG, width=7, joint="curve")
        d.line([(cx, cy + r), (cx + 200, THREAD_Y), (RX, THREAD_Y)], fill=SIG, width=7)
        if kk >= 1: coin(d, cx, cy, r, t, spin=t < tw, face="?")
    else:
        draw_thread(d, [(LX, THREAD_Y), (RX, THREAD_Y)], 1, SIG, smooth=False)
    if t >= tw: box_label(d, 480, 1060, "WITH CONFIDENCE", 40, WHITE, INK, anchor="ma"); bbox(d, (cx - r - 30, cy - r - 30, cx + r + 30, cy + r + 30), "YOUR GUT", SIG, (t - tw) / .3)
    fig(d, "fig. 2 — heads or tails")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "lies": sc_lies, "why": sc_why, "point": sc_point}
def scribble(amp=.035, dur=.5):
    t = tt_(dur); return amp * np.sin(2 * np.pi * (900 + 400 * np.sin(2 * np.pi * 23 * t)) * t) * np.exp(-t * 3)
FX = [(0.0, thud(.5), 0), *[(i * .085, tick(.03), (i % 3 - 1) / 2) for i in range(10)], (cue("hook", "when someone") - .1, scribble(), 0),
      (cue("hook", "you can't") - .15, thud(.55), 0), (cue("hook", "you can't") - .15, rewind_sfx(.08, .25), 0), *EP.cut_fx(),
      *[(S("study") + .2 + i * .05, tick(.025), (i % 5 - 2) / 3) for i in range(24)], (cue("study", "almost twenty-five") - .2, pop(.15), 0),
      (S("result") + .05, thud(.55), 0), (cue("result", "a coin") - .15, riser(.5, .05), 0), *[(cue("result", "a coin") + .4 + i * .08, tick(.05), .4) for i in range(8)],
      (S("lies") + .2, scribble(.03, 2.4), 0), (cue("lies", "forty-seven") - .3, pop(.15), 0),
      (cue("why", "slip right") - .2, pop(.15), .3), (cue("point", "coin flip") - .2, thud(.45), 0),
      *[(cue("point", "coin flip") + .3 + i * .08, tick(.05), 0) for i in range(8)], (cue("point", "with confidence"), thud(.4), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
