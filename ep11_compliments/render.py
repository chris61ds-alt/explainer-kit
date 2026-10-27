"""NOT JUST YOU – No. 11: compliments land better than you think (Zhao & Epley 2021). Look: Swiss Detail v2."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .35, "why": .4, "study": .9, "result": .5, "words": .5, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "why", "study", "result", "words", "point", "end"]
EP = Episode(TL, 11, "SAY IT", order=ORDER,
             chapters={"hook": "UNSAID", "why": "WHY NOT", "study": "THE STUDY", "result": "THE RESULT", "words": "WHAT COUNTS", "point": "SAY IT"},
             sources=("Zhao & Epley (2021), Journal of Personality", "and Social Psychology 121(2)"),
             music=dict(bpm=100, root=2, prog="warm", kick="half", gaps=[(E("study") + .05, S("result") + .05)]),
             cover=dict(words=["SAY", "IT."], kicker="Compliments land better than you think."))

# ---------------------------------------------------------------- actors carried across scenes
#                x_you  x_friend  scale  y-offset
TG = {"hook": (260, 720, 1.0, 0), "why": (260, 720, 1.0, 0), "study": (130, 830, .55, 0), "result": (130, 830, .55, 700),
      "words": (130, 830, .55, 700), "point": (260, 720, 1.0, 0)}
YOU_POSE = [(0, IDLE), (cue("hook", "didn't"), SHRUG), (S("why"), WORRY), (S("study"), IDLE), (S("point"), TALK)]
FR_POSE = [(0, TALK), (cue("hook", "didn't"), IDLE), (cue("point", "lands") - .3, OPEN), (cue("point", "think"), LAUGH)]
HEADS = {}

def actors(img, d, t, cur):
    i = ORDER.index(cur); prev = ORDER[max(0, i - 1)]
    k = ease_io((t - S(cur) + .05) / .6) if i else 1
    xy, xf, s, dy = (lerp(a, b, k) for a, b in zip(TG[prev], TG[cur]))
    if dy > 650: return
    HEADS["you"] = picto(d, xy, FLOOR + dy, s, INK, f=1, pose=pose_seq(t, YOU_POSE))
    HEADS["fr"] = picto(d, xf, FLOOR + dy, s, SIG, f=-1, pose=pose_seq(t, FR_POSE))
EP.layers.append(actors)

# ---------------------------------------------------------------- scenes
def sc_hook(img, d, t):
    giant(d, "UNSAID.", size=200)
    # the thought you never say
    hx, hy = 260, 760
    kb = (t - .15) / .35; dn = cue("hook", "didn't")
    box = think_box(d, (hx, hy), 400, 90, kb, "you're great at this", INK, 1, WHITE, 32)
    if t >= dn and box:
        k = ease((t - dn) / .35)
        d.line([box[0] + 10, (box[1] + box[3]) / 2, box[0] + 10 + (box[2] - box[0] - 20) * k, (box[1] + box[3]) / 2], fill=SIG, width=8)
    fig(d, "fig. 1 — a thought that stays a thought")

def sc_why(img, d, t):
    t0 = S("why")
    giant(d, "WHY NOT?", size=190, k=(t - t0) / .3)
    for i, (lab, tk) in enumerate((("too awkward?", cue("why", "awkward")), ("not good enough?", cue("why", "not good")))):
        k = ease((t - tk + .1) / .3)
        if k > 0: box_label(d, 420 + i * 30, 640 + i * 110, lab, 40, WHITE, INK if i == 0 else SIG)
    fig(d, "fig. 2 — the usual excuses")

def sc_study(img, d, t):
    t0 = S("study")
    d.text((X0, 320), "COMPLIMENTS", font=F(BLK, 110), fill=INK)
    d.text((X0, 450), "written to someone close", font=F(COND, 36), fill=INK)
    # note card being written
    cx0, cy0, cx1, cy1 = 230, 530, 730, 900
    kc = ease((t - t0 - .2) / .4)
    if kc > 0:
        d.rectangle([cx0, cy0 + (1 - kc) * 60, cx1, cy1 + (1 - kc) * 60], fill=WHITE, outline=INK, width=4)
        for i in range(3):
            kl = clamp((t - t0 - .6 - i * .5) / .5)
            y = cy0 + 70 + i * 100
            d.text((cx0 + 30, y - 22), f"{i + 1}.", font=F(COND, 34), fill=SIG)
            if kl > 0: d.line([cx0 + 80, y, cx0 + 80 + (cx1 - cx0 - 120) * kl * (1 - .2 * i), y], fill=INK, width=6)
    if t >= cue("study", "predict"):
        k = ease((t - cue("study", "predict")) / .4)
        note(d, cx1 - 20, cy0 + 40, 860, 620, "how will they feel?", k * 1.2, SIG, anchor="ra", size=28)
    fig(d, "Zhao & Epley — Journal of Personality and Social Psychology, 2021")

def pair_rows(d, y, title, pred, real, k1, k2, tag):
    d.text((X0, y), title, font=F(BLK, 48), fill=INK)
    hbar(d, y + 80, pred, k1, INK, "they predicted", h=70)
    hbar(d, y + 200, real, k2, SIG, "what it really was", h=70)
    if k2 > .95: box_label(d, X0 + (X1 - X0) * max(pred, real) - 10, y + 6, tag, 26, WHITE, SIG, anchor="ra")

def sc_result(img, d, t):
    t0 = S("result"); ov = cue("result", "overestimated")
    pair_rows(d, 330, "HOW GOOD IT FELT", .45, .85, (t - t0) / .4, (t - t0 - .5) / .6, "UNDERESTIMATED")
    if t >= ov - .2:
        pair_rows(d, 720, "HOW AWKWARD IT WAS", .7, .3, (t - ov + .2) / .4, (t - ov - .2) / .6, "OVERESTIMATED")
    d.text((X1, 1146), "schematic", font=F(MED, 22), fill=MID, anchor="ra")

def sc_words(img, d, t):
    t0 = S("words"); wm = cue("words", "warmth")
    kw = ease((t - t0) / .3)
    d.text((X0, 360), "WORDING", font=F(BLK, 120), fill=mix(BG, MID, kw))
    if t >= cue("words", "barely"):
        k = ease((t - cue("words", "barely")) / .35)
        d.line([X0, 430, X0 + 560 * k, 430], fill=INK, width=10)
    kk = ease((t - wm + .1) / .4)
    if kk > 0: d.text((X0 - 8 - (1 - kk) * 80, 560), "WARMTH.", font=F(BLK, 210), fill=mix(BG, SIG, kk))
    if kk > .9: note(d, 300, 820, 420, 960, "what people actually feel", (t - wm - .3) / .4, INK, size=28)
    fig(d, "fig. 3 — what counts")

def sc_point(img, d, t):
    t0 = S("point")
    giant(d, "SAY IT.", size=210, k=(t - t0) / .3)
    hy = HEADS.get("you", (260, 760))
    speech_box(d, 290, 630, 380, (t - t0 - .2) / .35, INK, 1, "You're great at this.", 30)
    if t >= cue("point", "lands"):
        rng = np.random.default_rng(3)
        for i in range(14):
            a = rng.uniform(-math.pi, 0); sp = rng.uniform(80, 220); u = clamp((t - cue("point", "lands") - i * .03) / .8)
            x = 720 + math.cos(a) * sp * u; y = 700 + math.sin(a) * sp * u + 120 * u * u
            r = 10 * (1 - u * .6)
            if u < 1: d.rectangle([x - r, y - r, x + r, y + r], fill=SIG if i % 3 else INK)
    fig(d, "fig. 4 — the same thought, said")

EP.scenes = {"hook": sc_hook, "why": sc_why, "study": sc_study, "result": sc_result, "words": sc_words, "point": sc_point}

FX = [(0.0, thud(.5), 0), (.15, pop(.15), -.2), (cue("hook", "didn't"), rewind_sfx(.12, .35), 0),
      *EP.cut_fx(),
      (cue("why", "awkward"), pop(.15), .2), (cue("why", "not good"), pop(.15), .3),
      *[(S("study") + .6 + i * .5, whoosh(.3, .05), 0) for i in range(3)],
      (S("result") + .05, thud(.55), 0), (cue("result", "overestimated"), thud(.35), 0),
      (cue("words", "barely"), whoosh(.3, .1), 0), (cue("words", "warmth"), thud(.5), 0),
      (S("point") + .2, pop(.2), -.2), (cue("point", "lands"), riser(.4, .08), .3),
      (S("end"), thud(.5), 0)]

if __name__ == "__main__": EP.run(FX)
