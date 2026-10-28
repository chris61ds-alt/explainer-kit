"""NOT JUST YOU – No. 58 (format test: STORY / case study): patient S.M. without fear (Feinstein et al. 2011, 2013).
v3 'Swiss Thread', light. The thread is her heartbeat: flat calm through every threat, chaos only with CO2."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from thread import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .6, "who": .6, "tests": .5, "snakes": .8, "twist": .6, "why": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "who", "tests", "snakes", "twist", "why", "point", "end"]
EP = ThreadEpisode(TL, 58, "NO FEAR", order=ORDER, dark=os.environ.get("V3_DARK") == "1", label="CASE STUDY",
                   chapters={"hook": "KNIFEPOINT", "who": "PATIENT S.M.", "tests": "HAUNTED HOUSE", "snakes": "PET STORE",
                             "twist": "THE TWIST", "why": "TWO FEARS", "point": "AT LEAST TWO"},
                   sources=("Feinstein, Adolphs, Damasio & Tranel (2011), Current", "Biology 21(1) · Feinstein et al. (2013), Nat. Neurosci."),
                   music=dict(bpm=78, root=-5, prog="tense", kick="half", gaps=[(E("snakes") + .05, S("twist") + .05)]),
                   cover=dict(words=["SHE FEELS", "NO FEAR."], kicker="Until one experiment."))

def heart_line(d, t, calm=True, chaos=0.0, y=THREAD_Y, col=SIG):
    pts = ekg(LX, RX, y, t, period=210, amp=48 if calm else 70, speed=200 if calm else 520, chaos=chaos, seed=int(t * 20) if chaos else 0)
    d.line(pts, fill=col, width=6, joint="curve")

def snake(d, x0, y, t, length=420, col=INK):
    pts = [(x0 + i * 6, y + 26 * math.sin(i * .16 - t * 4)) for i in range(int(length / 6))]
    d.line(pts, fill=col, width=26, joint="curve")
    hx, hy = pts[-1]; d.ellipse([hx - 24, hy - 20, hx + 30, hy + 20], fill=col)
    d.line([hx + 30, hy, hx + 52, hy - 6], fill=SIG, width=4); d.line([hx + 30, hy, hx + 52, hy + 6], fill=SIG, width=4)

def sc_hook(img, d, t):
    tn = cue("hook", "and felt")
    if t < tn - .1: d.text((X0 - 6, 320), "KNIFE-", font=F(BLK, 190), fill=INK); d.text((X0 - 6, 500), "POINT.", font=F(BLK, 190), fill=INK)
    else: words_in(d, t, [("NO", tn - .1, 320, 190, SIG), ("FEAR.", tn, 500, 190, SIG)])
    halftone(img, lambda m: bust(m, 300, 760, .55, 255, f=1), (60, 640, 640, 1000), cell=9, col=INK)
    knife(d, 760, 720, .9, INK, ang=math.pi + .05 * math.sin(t * 6))
    bbox(d, (190, 660, 380, 840), "S.M.  ·  HEART RATE: NORMAL", SIG, (t - tn) / .3, coords=False, size=18)
    heart_line(d, t)
    fig(d, "fig. 1 — a real case, reconstructed")

def sc_who(img, d, t):
    t0, ta = S("who"), cue("who", "the amygdala") - .3
    d.text((X0, 320), "S. M.", font=F(BLK, 200), fill=INK)
    cx, cy = 560, 640
    d.ellipse([cx - 260, cy - 190, cx + 260, cy + 170], outline=INK, width=6)                 # brain outline (side view)
    d.arc([cx - 200, cy - 140, cx + 120, cy + 60], 200, 340, fill=RULE, width=4); d.arc([cx - 120, cy - 60, cx + 220, cy + 120], 190, 330, fill=RULE, width=4)
    for i, (ax, ay) in enumerate(((cx - 40, cy + 60), (cx + 40, cy + 70))):
        k = ease((t - ta - i * .15) / .3)
        if k > 0:
            d.ellipse([ax - 22 * k, ay - 14 * k, ax + 22 * k, ay + 14 * k], fill=SIG)
            if t >= ta + .6: cross_out = ease((t - ta - .6) / .25); d.line([ax - 30 * cross_out, ay - 30 * cross_out, ax + 30 * cross_out, ay + 30 * cross_out], fill=INK, width=6)
    if t >= ta: note(d, cx, cy + 70, X1 - 20, 470, "AMYGDALA · BOTH SIDES", 1, SIG, anchor="ra", size=26)
    d.text((X0, 980), "Urbach-Wiethe disease (very rare)", font=F(MONO, 22), fill=MID)
    heart_line(d, t)
    fig(d, "damage to both amygdalae since late childhood")

def sc_tests(img, d, t):
    t0, tp = S("tests"), cue("tests", "poked") - .2
    d.text((X0, 320), "HAUNTED", font=F(BLK, 150), fill=INK); d.text((X0, 470), "HOUSE.", font=F(BLK, 150), fill=SIG)
    hx = 540; d.polygon([(hx, 640), (hx + 190, 560), (hx + 380, 640)], outline=INK, width=6); d.rectangle([hx + 30, 640, hx + 350, 820], outline=INK, width=6)
    mon = picto(d, hx + 250, 820, .55, INK, f=-1, pose={"arms": ((110, 30), (100, 25))})
    picto(d, 250, THREAD_Y - 10, .6, SIG, f=1, pose=LAUGH if t < tp else {"arms": ((95, 0), (-30, -60))})
    if t >= tp: box_label(d, mon[0], mon[1] - 90, "POKE", 26, WHITE, SIG, anchor="ma")
    heart_line(d, t)
    fig(d, "Waverly Hills Sanatorium · she laughed")

def sc_snakes(img, d, t):
    t0 = S("snakes")
    d.text((X0, 320), "CAN I", font=F(BLK, 150), fill=INK); d.text((X0, 470), "TOUCH IT?", font=F(BLK, 150), fill=SIG)
    snake(d, 420, 720, t, 380)
    picto(d, 250, THREAD_Y - 10, .6, SIG, f=1, pose={"arms": ((100, 10), (-10, -5))})
    bbox(d, (400, 650, 900, 790), "VENOMOUS", INK, (t - t0 - .5) / .3, coords=False)
    heart_line(d, t)
    fig(d, "exotic pet store · she kept asking to touch them")

def sc_twist(img, d, t):
    t0, tp = S("twist"), cue("twist", "she panicked") - .2
    if t < tp:
        d.text((X0, 320), "ONE BREATH", font=F(BLK, 130), fill=INK)
        for i in range(7):
            k = (t - t0) * .8 + i / 7; r = 30 + 60 * (k % 1)
            d.ellipse([480 - r * 2.2, 650 - r, 480 + r * 2.2, 650 + r], outline=mix(BG, MID, 1 - (k % 1)), width=4)
        box_label(d, 480, 640, "CO2", 60, WHITE, INK, font=BLK, anchor="ma")
        heart_line(d, t)
    else:
        words_in(d, t, [("PANIC.", tp, 320, 230, SIG)])
        picto(d, 300, THREAD_Y - 10, .75, INK, f=1, pose=FACEPALM)
        if t >= cue("twist", "completely new") - .2: box_label(d, X1, 640, "A NEW FEELING", 40, WHITE, INK, anchor="ra")
        heart_line(d, t, calm=False, chaos=.9)
        if t < tp + .35: glitch(img, (0, 300, W, 1180), 1.6, seed=int(t * 30), pixel=6)
    fig(d, "inhaling air with extra carbon dioxide · 2013")

def sc_why(img, d, t):
    t0, ti = S("why"), cue("why", "fear from inside") - .2
    d.text((X0, 320), "OUTSIDE", font=F(BLK, 110), fill=INK)
    knife(d, X0 + 30, 520, .6, INK, 0); snake(d, X0 + 260, 520, t, 180)
    d.text((X0, 600), "needs the amygdala", font=F(COND, 34), fill=MID)
    if t >= ti:
        d.text((X0 + 440, 640), "INSIDE", font=F(BLK, 110), fill=SIG)
        d.text((X0 + 440, 760), "body alarm, no amygdala", font=F(COND, 34), fill=SIG)
    heart_line(d, t, calm=t < ti, chaos=.5 if t >= ti else 0)
    fig(d, "external threat vs. internal threat")

def sc_point(img, d, t):
    t0, ta = S("point"), cue("point", "at least") - .2
    words_in(d, t, [("FEAR ISN'T", t0, 320, 140, INK), ("ONE THING.", t0 + .4, 470, 140, SIG)])
    k = ease((t - ta) / .6)
    a = ekg(LX, 480, THREAD_Y, t, period=210, amp=48, speed=200)
    d.line(a, fill=SIG, width=6)
    d.line(spline([(480, THREAD_Y), (640, THREAD_Y - 120 * k), (RX, THREAD_Y - 120 * k)]), fill=SIG, width=6)
    d.line(spline([(480, THREAD_Y), (640, THREAD_Y + 120 * k), (RX, THREAD_Y + 120 * k)]), fill=INK, width=6)
    if k > .9:
        d.text((X1, THREAD_Y - 140), "OUTSIDE", font=F(MONO, 22), fill=SIG, anchor="rd"); d.text((X1, THREAD_Y + 140), "INSIDE", font=F(MONO, 22), fill=INK, anchor="ra")
    fig(d, "fig. 2 — at least two alarm systems")

EP.scenes = {"hook": sc_hook, "who": sc_who, "tests": sc_tests, "snakes": sc_snakes, "twist": sc_twist, "why": sc_why, "point": sc_point}
FX = [(0.0, thud(.5), 0), *[(.3 + i * .9, heartbeat(.2) if False else softkick(.12), 0) for i in range(3)], (cue("hook", "and felt") - .1, pop(.15), 0), *EP.cut_fx(),
      (cue("who", "the amygdala") - .3, pop(.15), -.2), (cue("who", "the amygdala") + .3, thud(.3), 0), (cue("tests", "poked") - .2, pop(.18), .3),
      (S("snakes") + .5, pop(.12), 0), (S("twist") + .1, whoosh(1.2, .05), 0), (cue("twist", "she panicked") - .2, thud(.6), 0),
      (cue("twist", "she panicked") - .2, rewind_sfx(.12, .35), 0), *[(cue("twist", "she panicked") + i * .22, softkick(.18), 0) for i in range(8)],
      (cue("why", "fear from inside") - .2, pop(.15), 0), (cue("point", "at least") - .2, riser(.5, .05), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
