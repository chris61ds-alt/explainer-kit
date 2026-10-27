"""NOT JUST YOU – No. 36: asking questions gets second dates (Huang et al. 2017). Area: dating."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .8, "result": .5, "best": .5, "math": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "best", "math", "point", "end"]
EP = Episode(TL, 36, "ASK ONE MORE", order=ORDER,
             chapters={"hook": "SECOND DATE?", "study": "THE DATA", "result": "THE RESULT", "best": "THE BEST KIND", "math": "THE MATH", "point": "TELL ME MORE"},
             sources=("Huang, Yeomans, Brooks, Minson & Gino (2017),", "J. Personality & Social Psych. 113(3) · via HBS"),
             music=dict(bpm=100, root=4, prog="warm", kick="half", gaps=[(E("study") + .05, S("result") + .05)]),
             cover=dict(words=["ASK", "ONE MORE."], kicker="The second-date trick."))

def heart(d, cx, cy, r, col=SIG):
    d.ellipse([cx - r, cy - r * .9, cx, cy + r * .1], fill=col); d.ellipse([cx, cy - r * .9, cx + r, cy + r * .1], fill=col)
    d.polygon([(cx - r * .98, cy - r * .3), (cx + r * .98, cy - r * .3), (cx, cy + r * .95)], fill=col)

ACT = actors_layer(ORDER, S, [
    dict(col=INK, f=1, tg={"hook": (230, 1.0, 0), "study": (230, 1.0, 700), "result": (230, 1.0, 700), "best": (230, .9, 0), "math": (230, .9, 700), "point": (230, 1.0, 0)},
         poses=[(0, IDLE), (cue("hook", "ask"), TALK), (S("best"), TALK), (S("point"), TALK)]),
    dict(col=SIG, f=-1, tg={"hook": (730, 1.0, 0), "study": (730, 1.0, 700), "result": (730, 1.0, 700), "best": (730, .9, 0), "math": (730, .9, 700), "point": (730, 1.0, 0)},
         poses=[(0, IDLE), (S("best"), OPEN), (cue("point", "tell me more"), LAUGH)])])
EP.layers.append(ACT)

def sc_hook(img, d, t):
    d.text((X0 - 6, 300), "DATE #2?", font=F(BLK, 200), fill=INK)
    table(d, 480, 900, 300); cup(d, 420, 896, t); cup(d, 540, 896, t + 1)
    if t >= cue("hook", "ask"): speech_box(d, 300, 640, 120, (t - cue("hook", "ask")) / .3, INK, 1, "?", 50)
    fig(d, "fig. 1 — a first date")

def sc_study(img, d, t):
    t0 = S("study")
    counter(d, X0, 300, t, t0 + .1, 1.2, 2000, "{:,.0f}+", 190, SIG)
    d.text((X0 + 6, 520), "speed-dating conversations", font=F(COND, 36), fill=INK)
    for i in range(24):
        r, c = divmod(i, 6); x = X0 + 20 + c * 140; y = 620 + r * 120
        k = ease((t - t0 - .2 - i * .04) / .3)
        if k > 0:
            d.rectangle([x, y, x + 120, y + 70], outline=INK, width=3)
            for j in range(3): d.line([x + 12, y + 16 + j * 18, x + 100 - (j * 20 + i * 7) % 40, y + 16 + j * 18], fill=SIG if (i + j) % 5 == 0 else RULE, width=5)
    fig(d, "110 people, analysed by a language algorithm · Huang et al., 2017")

def sc_result(img, d, t):
    t0 = S("result")
    d.text((X0, 320), "MORE QUESTIONS", font=F(BLK, 100), fill=INK)
    d.text((X0, 440), "= more second dates", font=F(BLK, 70), fill=SIG)
    ox, oy, w, h = X0 + 40, 1060, X1 - X0 - 60, 440
    d.line([ox, oy, ox + w, oy], fill=INK, width=4); d.line([ox, oy, ox, oy - h], fill=INK, width=4)
    d.text((ox + w, oy + 16), "questions asked", font=F(COND, 26), fill=INK, anchor="ra"); d.text((ox + 10, oy - h - 10), "second-date yeses", font=F(COND, 26), fill=INK, anchor="ld")
    rng = np.random.default_rng(3)
    for i in range(30):
        u = rng.uniform(.05, .95); v = clamp(.15 + .7 * u + rng.normal(0, .1)); k = ease((t - t0 - i * .04) / .2)
        if k > 0: heart(d, ox + w * u, oy - h * v, 14 * k, SIG if i % 3 else INK)
    d.text((X1, 1146), "schematic", font=F(MED, 22), fill=MID, anchor="ra")

def sc_best(img, d, t):
    t0 = S("best"); lt = cue("best", "listening")
    d.text((X0, 320), "FOLLOW-UPS", font=F(BLK, 130), fill=SIG)
    speech_box(d, 760, 560, 360, (t - t0 - .1) / .3, SIG, -1, "I just got back from Lisbon.", 24)
    speech_box(d, 300, 700, 340, (t - cue("best", "follow-up") + .1) / .3, INK, 1, "Wait, what was it like?", 26)
    if t >= lt: note(d, 470, 770, 620, 950, "proof you were listening", (t - lt) / .35, INK, size=28)
    fig(d, "follow-ups were the most common question type in the study")

def sc_math(img, d, t):
    t0 = S("math")
    d.text((X0, 320), "THE MATH", font=F(BLK, 130), fill=INK)
    d.text((X0, 480), "+1 question", font=F(BLK, 60), fill=INK); d.text((X0 + 380, 490), "per date", font=F(COND, 40), fill=INK)
    for i in range(20):
        r, c = divmod(i, 10); x = X0 + 30 + c * 86; y = 640 + r * 120
        k = ease((t - cue("math", "twenty") + .3 - i * .04) / .25)
        if k > 0: d.rectangle([x, y, x + 70, y + 90], outline=INK, width=3); d.text((x + 35, y + 45), "?", font=F(BLK, 44), fill=INK, anchor="mm")
    if t >= cue("math", "one more yes") - .1:
        k = back((t - cue("math", "one more yes") + .1) / .4); heart(d, 480, 1000, 60 * k)
        box_label(d, 480, 1070, "+1 YES", 34, WHITE, SIG, anchor="ma")
    fig(d, "researchers' estimate across 20 speed dates")

def sc_point(img, d, t):
    t0 = S("point"); tm = cue("point", "tell me more")
    words_in(d, t, [("LESS PITCH.", t0, 300, 150, INK)] if t < tm - .2 else [("TELL ME", tm - .2, 300, 150, INK), ("MORE.", tm, 450, 150, SIG)])
    if t < tm - .2: speech_box(d, 300, 650, 380, (t - t0 - .2) / .3, MID, 1, "me, me, my job, me…", 26)
    else:
        speech_box(d, 300, 650, 380, (t - tm + .2) / .3, INK, 1, "Wait, tell me more!", 30)
        for i in range(3): heart(d, 760 + i * 30, 640 - ((t * 80 + i * 40) % 140), 16)
    fig(d, "fig. 2 — curiosity is attractive")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "best": sc_best, "math": sc_math, "point": sc_point}
FX = [(0.0, thud(.5), 0), (cue("hook", "ask"), pop(.2), -.2), *EP.cut_fx(),
      *[(S("study") + .2 + i * .1, tick(.05), (i % 5 - 2) / 3) for i in range(12)], (S("result") + .05, thud(.5), 0),
      (cue("best", "follow-up"), pop(.18), -.2), (cue("best", "listening"), pop(.15), .2), (cue("math", "twenty"), whoosh(.6, .08), 0),
      (cue("math", "one more yes"), thud(.45), 0), (cue("point", "tell me more"), riser(.4, .07), .2), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
