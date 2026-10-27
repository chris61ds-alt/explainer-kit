"""NOT JUST YOU – No. 17: why you can't tickle yourself (Blakemore, Frith & Wolpert 1999). Area: body."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "why": .5, "study": .45, "delay": .5, "name": .5, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "why", "study", "delay", "name", "point", "end"]
EP = Episode(TL, 17, "NO TICKLE", order=ORDER,
             chapters={"hook": "TRY IT", "why": "THE PREDICTION", "study": "THE ROBOT", "delay": "THE DELAY", "name": "THE RULE", "point": "SOMEONE ELSE"},
             sources=("Blakemore, Frith & Wolpert (1999),", "Journal of Cognitive Neuroscience 11(5)"),
             music=dict(bpm=104, root=1, prog="major", kick="four", gaps=[(E("study") + .05, S("delay") + .1)]),
             cover=dict(words=["TICKLE", "YOURSELF?"], kicker="Why it never works."))

SELF = {"arms": ((40, -60), (-10, -5))}          # hand to own side
def feather(d, x, y, s=1.0, col=SIG, t=0.0, flip=False):
    a = math.sin(t * 10) * .25 + (-.8 if not flip else -2.34)
    tip = (x + math.cos(a) * 140 * s, y + math.sin(a) * 140 * s)
    d.line([x, y, tip[0], tip[1]], fill=INK, width=int(5 * s))
    for i in range(1, 9):
        u = i / 9; px, py = lerp(x, tip[0], u), lerp(y, tip[1], u); L = 34 * s * math.sin(u * math.pi)
        for sg in (-1, 1): d.line([px, py, px + sg * L * .6, py - L], fill=col, width=int(4 * s))

def sc_hook(img, d, t):
    d.text((X0 - 6, 300), "TICKLE", font=F(BLK, 200), fill=INK)
    d.text((X0, 500), "yourself.", font=F(BLK, 90), fill=SIG)
    h = picto(d, 420, FLOOR, 1.05, INK, f=1, pose=SELF)
    feather(d, 470, 860, .8, SIG, t)
    if t >= cue("hook", "nothing"):
        note(d, 470, 860, 720, 760, "nothing.", (t - cue("hook", "nothing")) / .35, INK, size=34)
    fig(d, "fig. 1 — the experiment you've done")

def sc_why(img, d, t):
    t0 = S("why"); pr = cue("why", "predicts"); wk = cue("why", "weaker")
    d.text((X0, 320), "PREDICTED", font=F(BLK, 130), fill=INK)
    ox, oy, w = X0 + 20, 820, X1 - X0 - 40
    def bump(u, c=.5, wd=.12): return math.exp(-((u - c) / wd) ** 2)
    kp = ease((t - pr) / .6); ka = ease((t - pr - .8) / .6)
    pts_p = [(ox + w * i / 100, oy - 220 * bump(i / 100)) for i in range(int(101 * kp))]
    pts_a = [(ox + w * i / 100, oy - 200 * bump(i / 100, .52)) for i in range(int(101 * ka))]
    for i in range(0, len(pts_p) - 1, 2): d.line([pts_p[i], pts_p[i + 1]], fill=MID, width=5)
    if len(pts_a) > 1: d.line(pts_a, fill=SIG, width=7)
    d.line([ox, oy, ox + w, oy], fill=INK, width=3)
    legend(d, [(MID, "what your brain expects"), (SIG, "what you feel")], y=880)
    if t >= wk - .1:
        k = ease((t - wk + .1) / .4)
        d.rectangle([X0, 960, X0 + 520 * k, 1040], fill=INK)
        if k > .9: d.text((X0 + 20, 1000), "expected − felt ≈ nothing", font=F(COND, 34), fill=WHITE, anchor="lm")
    fig(d, "fig. 2 — the brain subtracts its own prediction")

def sc_study(img, d, t):
    t0 = S("study"); ctl = cue("study", "controlled")
    d.text((X0, 320), "THE ROBOT", font=F(BLK, 130), fill=INK)
    # left hand moves a stick → robot → foam stroking the right palm
    u = math.sin(t * 3)
    d.rounded_rectangle([X0 + 40, 700, X0 + 240, 800], radius=40, fill=INK)                    # left hand
    d.line([X0 + 140, 700, X0 + 140 + 50 * u, 560], fill=INK, width=12); d.ellipse([X0 + 120 + 50 * u, 530, X0 + 160 + 50 * u, 570], fill=SIG)
    d.rectangle([380, 520, 600, 640], outline=INK, width=6); d.text((490, 580), "ROBOT", font=F(COND, 40), fill=INK, anchor="mm")
    d.line([X0 + 160 + 50 * u, 550, 380, 580], fill=MID, width=4)
    d.line([600, 580, 720 + 60 * u, 760], fill=INK, width=10)
    d.rectangle([680 + 60 * u, 760, 760 + 60 * u, 790], fill=SIG)                                 # foam
    d.rounded_rectangle([620, 800, 860, 880], radius=36, fill=MID)                               # right palm
    note(d, X0 + 140, 800, X0 + 140, 960, "your left hand", 1, INK, size=26)
    note(d, 740, 880, 740, 960, "your right palm", 1, INK, size=26)
    if t >= ctl: box_label(d, 490, 660, "NO DELAY", 26, WHITE, INK, anchor="ma")
    fig(d, "Blakemore, Frith & Wolpert, 1999")

def sc_delay(img, d, t):
    t0 = S("delay"); td = cue("delay", "tiny delay"); tk = cue("delay", "tickle")
    d.text((X0, 320), "+ A DELAY", font=F(BLK, 130), fill=SIG)
    yb = 1020; vals = [("0 ms", .2), ("100 ms", .4), ("200 ms", .6), ("300 ms", .8)]
    for i, (lab, v) in enumerate(vals):
        k = ease((t - td - i * .35) / .4)
        x = X0 + 40 + i * 210
        d.text((x + 60, yb + 16), lab, font=F(MONO, 22), fill=INK, anchor="ma")
        if k > 0: d.rectangle([x, yb - 420 * v * k, x + 120, yb], fill=SIG if i else INK)
    d.line([X0, yb, X1, yb], fill=INK, width=3)
    d.text((X0, 500), "how ticklish it felt", font=F(COND, 34), fill=INK)
    if t >= tk: note(d, X0 + 40 + 3 * 210 + 60, yb - 336, 640, 600, "it tickles", (t - tk) / .35, SIG, anchor="ra", size=30)
    d.text((X1, 1146), "schematic", font=F(MED, 22), fill=MID, anchor="ra")

def sc_name(img, d, t):
    words_in(d, t, [("NO SURPRISE,", S("name") + .1, 330, 128, INK), ("NO TICKLE.", cue("name", "surprises") - .2, 520, 150, SIG)])
    d.text((X0, 760), "your brain cancels its own", font=F(COND, 40), fill=INK)
    d.text((X0, 812), "predicted touches", font=F(COND, 40), fill=INK)

def sc_point(img, d, t):
    t0 = S("point"); se = cue("point", "someone else")
    d.text((X0 - 6, 300), "SOMEONE", font=F(BLK, 170), fill=INK)
    d.text((X0, 480), "else.", font=F(BLK, 110), fill=SIG)
    picto(d, 330, FLOOR, 1.0, INK, f=1, pose=LAUGH if t >= se else IDLE, tilt=-8 + 6 * math.sin(t * 14) if t >= se else 0)
    picto(d, 640, FLOOR, 1.0, SIG, f=-1, pose={"arms": ((80, 70), (-10, -5))})
    feather(d, 590, 900, .75, SIG, t, flip=True)
    if t >= se: note(d, 500, 820, 760, 640, "unpredicted", (t - se) / .35, SIG, size=28)
    fig(d, "fig. 3 — the same feather, someone else's hand")

EP.scenes = {"hook": sc_hook, "why": sc_why, "study": sc_study, "delay": sc_delay, "name": sc_name, "point": sc_point}
FX = [(0.0, thud(.5), 0), (.3, whoosh(.4, .08), .2), (cue("hook", "nothing"), rewind_sfx(.1, .3), 0), *EP.cut_fx(),
      (cue("why", "predicts"), whoosh(.6, .08), -.2), (cue("why", "weaker"), thud(.35), 0),
      (cue("study", "controlled"), pop(.15), 0), *[(cue("delay", "tiny delay") + i * .35, pop(.12), (i - 1.5) / 2) for i in range(4)],
      (cue("delay", "tickle"), riser(.4, .07), 0), (cue("name", "surprises") - .2, thud(.5), 0),
      (cue("point", "someone else"), pop(.2), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
