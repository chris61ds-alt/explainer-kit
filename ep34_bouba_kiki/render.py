"""NOT JUST YOU – No. 34: the bouba/kiki effect (Köhler 1929; Ramachandran & Hubbard 2001; Ćwiek et al. 2021). Area: language."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .9, "answer": .5, "study": .5, "why": .5, "point": .8, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "answer", "study", "why", "point", "end"]
EP = Episode(TL, 34, "BOUBA / KIKI", order=ORDER,
             chapters={"hook": "WHICH IS WHICH?", "answer": "THE ANSWER", "study": "25 LANGUAGES", "why": "WHY", "point": "SHAPED SOUNDS"},
             sources=("Ćwiek et al. (2021), Phil. Trans. R. Soc. B 377", "Ramachandran & Hubbard (2001) · Köhler (1929)"),
             music=dict(bpm=98, root=2, prog="warm", kick="half", gaps=[(E("hook") + .05, S("answer") + .05)]),
             cover=dict(words=["BOUBA", "OR KIKI?"], kicker="Some sounds have a shape."))

def blob(d, cx, cy, R, col=INK, t=0.0, spiky=0.0):
    pts = []
    for i in range(120):
        a = i / 120 * 2 * math.pi
        smooth = 1 + .12 * math.sin(5 * a + t) + .06 * math.sin(3 * a - t * .7)
        sharp = 1.0 if i % 12 < 1 else .5
        sharp = lerp(.5, 1.0, max(0, 1 - abs((i % 12) - 0) / 1.0)) if True else 1
        r = lerp(smooth, (1.0 if i % 12 == 0 else .48 + .04 * ((i % 12) % 2)), spiky)
        pts.append((cx + math.cos(a) * R * r, cy + math.sin(a) * R * r))
    d.polygon(pts, fill=col)

def star(d, cx, cy, R, col=INK, t=0.0, n=9):
    pts = []
    for i in range(n * 2):
        a = i / (n * 2) * 2 * math.pi + t * .1; r = R if i % 2 == 0 else R * .42
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    d.polygon(pts, fill=col)

def sc_hook(img, d, t):
    d.text((X0 - 6, 300), "BOUBA?", font=F(BLK, 120), fill=INK); d.text((X1, 300), "KIKI?", font=F(BLK, 120), fill=SIG, anchor="ra")
    blob(d, 260, 790, 165, INK, t)
    star(d, 710, 790, 175, SIG, t)
    if t >= cue("hook", "which is which"):
        box_label(d, 480, 1060, "WHICH IS WHICH?", 40, WHITE, INK, anchor="ma")
    fig(d, "fig. 1 — decide before you read on")

def sc_answer(img, d, t):
    t0 = S("answer"); ae = cue("answer", "almost everyone")
    blob(d, 260, 760, 160, INK, t); star(d, 710, 760, 170, SIG, t)
    k = ease((t - cue("answer", "round one") + .1) / .3)
    if k > 0: box_label(d, 260, 980, "BOUBA", 50, WHITE, INK, anchor="ma"); box_label(d, 710, 980, "KIKI", 50, WHITE, SIG, anchor="ma")
    d.text((X0, 320), "YOU SAID:", font=F(BLK, 110), fill=INK)
    if t >= ae: box_label(d, 480, 1090, "SO DOES ALMOST EVERYONE", 32, WHITE, SIG, anchor="ma")

LANGS = ["EN", "DE", "FR", "ES", "IT", "PL", "RO", "HU", "TR", "ZH", "JA", "KO", "AR", "HE", "EL", "KA", "HY", "TH", "SV", "NO", "PT", "AL", "SW", "ZU", "FA"]
def sc_study(img, d, t):
    t0 = S("study")
    d.text((X0, 320), "25 LANGUAGES", font=F(BLK, 110), fill=INK)
    d.text((X0, 440), "10 writing systems · 9 language families", font=F(COND, 32), fill=INK)
    k = clamp((t - t0 - .3) / 2.0)
    for i, code in enumerate(LANGS):
        r, c = divmod(i, 5); x = X0 + 40 + c * 170; y = 520 + r * 112
        on = i < 25 * k
        opp = code in ("RO", "TR", "ZH")
        d.rectangle([x, y, x + 150, y + 96], fill=(MID if opp else SIG) if on else None, outline=INK, width=3)
        d.text((x + 75, y + 48), code, font=F(BLK, 40), fill=WHITE if on else INK, anchor="mm")
    fig(d, "Ćwiek et al., 2021 · grey: exceptions (e.g. RO, TR, ZH) · other codes illustrative")

def mouth(d, cx, cy, kind, s=1.0):
    if kind == "boo": d.ellipse([cx - 60 * s, cy - 70 * s, cx + 60 * s, cy + 70 * s], outline=INK, width=int(16 * s))
    else: d.arc([cx - 150 * s, cy - 60 * s, cx + 150 * s, cy + 60 * s], 10, 170, fill=SIG, width=int(16 * s)); d.line([cx - 140 * s, cy + 10 * s, cx + 140 * s, cy + 10 * s], fill=SIG, width=int(10 * s))

def sc_why(img, d, t):
    t0 = S("why"); sh = cue("why", "sharp sounds")
    d.text((X0, 320), "MOUTH = SHAPE", font=F(BLK, 104), fill=INK)
    mouth(d, 230, 620, "boo"); blob(d, 230, 900, 110, INK, t)
    d.text((230, 1040), '"boo-ba"', font=F(BLK, 40), fill=INK, anchor="ma")
    # smooth vs jagged sound waves
    for i in range(80):
        x = 360 + i * 2.4; d.point((x, 620 + 40 * math.sin(i * .2 + t * 4)), fill=INK)
    if t >= sh - .2:
        mouth(d, 700, 620, "kee", .9); star(d, 700, 900, 120, SIG, t)
        d.text((700, 1040), '"kee-kee"', font=F(BLK, 40), fill=SIG, anchor="ma")
        pts = [(470 + i * 10, 620 + (36 if i % 2 else -36)) for i in range(10)]; d.line(pts, fill=SIG, width=4)
    fig(d, "round lips, round sounds · sharp sounds, sharp shapes")

def sc_point(img, d, t):
    t0 = S("point"); sp = cue("point", "come with")
    words_in(d, t, [("NOT RANDOM.", t0, 300, 150, INK)] if t < sp - .2 else [("SOUNDS", sp - .2, 300, 150, INK), ("HAVE SHAPES.", sp, 450, 130, SIG)])
    m = .5 + .5 * math.sin(t * 2.2)
    blob(d, 480, 860, 210, mix(INK, SIG, m), t, spiky=m)
    fig(d, "fig. 2 — bouba ↔ kiki")

EP.scenes = {"hook": sc_hook, "answer": sc_answer, "study": sc_study, "why": sc_why, "point": sc_point}
def boo(amp=.07, dur=.35):
    t = tt_(dur); return amp * np.sin(2 * np.pi * 160 * t) * np.sin(np.pi * t / dur)
def kee(amp=.05, dur=.18):
    t = tt_(dur); return amp * np.sign(np.sin(2 * np.pi * 1200 * t)) * np.exp(-t * 18)
FX = [(0.0, thud(.45), 0), (.3, boo(), -.3), (.6, kee(), .3), (cue("hook", "which is which"), pop(.18), 0), *EP.cut_fx(),
      (cue("answer", "round one"), boo(.08), -.3), (cue("answer", "round one") + .2, kee(.06), .3), (cue("answer", "almost everyone"), thud(.4), 0),
      *[(S("study") + .3 + i * .08, tick(.05), (i % 5 - 2) / 3) for i in range(25)], (cue("why", "round sounds"), boo(.07), -.3),
      (cue("why", "sharp sounds"), kee(.06), .3), (cue("point", "come with"), thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
