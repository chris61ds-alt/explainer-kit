"""NOT JUST YOU – No. 126 (simulation): the 37 % rule – secretary problem with 10 dates; skipping the first 3 then taking the
first better one finds the best ~40 % of the time vs. ~10 % for 'first date' or random (Ferguson 1989; Christian & Griffiths 2016).
Look C+D · statement opener with "you" · isometric row of date cards + live 1,000-run counter · orange reveal: 40 %."""
import os, sys, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"setup": .6, "rule": .6, "sim": .5, "result": .6, "caveat": .5, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["setup", "rule", "sim", "result", "caveat", "point", "end"]
EP = ThreadEpisode(TL, 126, "37 RULE", order=ORDER, dark=True, label="SIMULATION · MATH MODEL",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Ferguson (1989), Who solved the secretary problem?, Stat. Science ·", "Christian & Griffiths (2016), Algorithms to Live By"),
                   music=dict(bpm=100, root=0, prog="dream", kick="four", audio="v5", gaps=[(E("setup") + .05, S("rule") + .05)]),
                   cover=dict(words=["YOU SETTLED", "TOO EARLY.", "OR TOO LATE."], kicker="The 37 % rule. Simulated."))

# one example life: ten dates with hidden quality (fixed seed so the rule visibly works)
QUAL = [.42, .71, .55, .38, .66, .97, .5, .9, .6, .45]       # the rule picks date 6, which is also the best
SKIP = 3
# the 1,000-life simulation (counted live)
R = random.Random(1); RUNS = []
for _ in range(1000):
    v = [R.random() for _ in range(10)]; best = max(v); th = max(v[:SKIP])
    pick = next((x for x in v[SKIP:] if x > th), v[-1]); RUNS.append((pick == best, v[0] == best, R.choice(v) == best))
WIN = [sum(r[i] for r in RUNS) for i in range(3)]

I = Iso(500, 1010, .62)
def cards(img, d, t, t0, show_skip=False, pick_t=None, reveal=False):
    I.grid(img)
    for i, q in enumerate(QUAL):
        tk = t0 + i * .12
        if t < tk: continue
        x, y = -470 + i * 100, 260 - i * 60; k = ease(clamp((t - tk) / .25)); h = (60 + 300 * q) * k if (reveal or (show_skip and i < SKIP) or (pick_t and t >= pick_t + (i - SKIP) * .25)) else 40 * k
        top = TOP
        if show_skip and i < SKIP: top = RIGHT
        if pick_t and i == 5 and t >= pick_t + 1.0: top = SIG
        I.box(d, x, y, 0, 70, 70, h, top=top)
        fx, fy = I.P(x + 70, y + 70, 0); d.text((fx, fy + 10), str(i + 1), font=F(BLK, 30), fill=MID if (show_skip and i < SKIP) else INK, anchor="ma")
    if show_skip:
        a, b = I.P(-470, 260, 60 + 300 * .55), I.P(-470 + 9 * 100 + 70, 260 - 9 * 60, 60 + 300 * .55)
        d.line([a, b], fill=MID, width=4)

def sc_setup(img, d, t):
    t0, tg = S("setup"), cue("setup", "they're gone") - .1
    d.text((X0, 320), "10 DATES", font=F(BLK, 130), fill=INK); d.text((X0 + 4, 470), "one after another · no going back", font=F(COND, 46), fill=MID)
    cards(img, d, t, t0 + .2)
    if t >= tg: box_label(d, X1, 560, "PASS = GONE", 44, WHITE, INK, font=BLK, anchor="ra")
    fig(d, "fig. 1 — schematic")

def sc_rule(img, d, t):
    t0, tl, tp = S("rule"), cue("rule", "Just look") - .1, cue("rule", "Then pick") - .1
    d.text((X0, 320), "SKIP 37 %.", font=F(BLK, 130), fill=INK); d.text((X0 + 4, 470), "then take the first who beats them all", font=F(COND, 46), fill=MID)
    cards(img, d, t, t0 - 3, show_skip=t >= tl, pick_t=tp if t >= tp else None)
    if t >= tl: box_label(d, X0 + 4, 560, "JUST LOOK: 1–3", 40, WHITE, MID, font=BLK)
    if t >= tp + 1.0: box_label(d, X1, 640, "PICK: NO. 6", 40, WHITE, INK, font=BLK, anchor="ra")
    fig(d, "for 10 dates: skip 3")

def counters(d, t, t0, dur, y0=560, hl=False):
    n = int(clamp((t - t0) / dur) * 1000)
    wins = [sum(r[i] for r in RUNS[:n]) for i in range(3)]
    d.text((X0, y0), f"{n:,} LOVE LIVES", font=F(MONO, 34), fill=MID)
    for j, (lab, col) in enumerate((("37 % RULE", SIG if hl else INK), ("FIRST DATE", MID), ("RANDOM", MID))):
        y = y0 + 80 + j * 170; v = wins[j] / max(1, n)
        d.text((X0, y), lab, font=F(BLK, 46), fill=col); w = 600 * v / .45
        d.rectangle([X0, y + 60, X0 + max(6, w), y + 130], fill=col)
        d.text((X0 + max(6, w) + 14, y + 95), f"{v * 100:.0f} %", font=F(BLK, 56), fill=col, anchor="lm")

def sc_sim(img, d, t):
    t0 = S("sim"); d.text((X0, 320), "1,000 LIVES", font=F(BLK, 120), fill=INK); d.text((X0 + 4, 450), "found the very best one", font=F(COND, 46), fill=MID)
    counters(d, t, t0 + .3, max(1.5, E("sim") - t0 - .6))
    fig(d, "simulation · 10 dates each")

def sc_result(img, d, t):
    t0 = S("result"); d.text((X0, 320), "THE RULE: 40 %.", font=F(BLK, 110), fill=SIG); d.text((X0 + 4, 450), "found the very best one", font=F(COND, 46), fill=INK)
    counters(d, t, t0 - 10, 1, hl=True)
    fig(d, "simulation · 10 dates each")

def sc_caveat(img, d, t):
    t0, tn = S("caveat"), cue("caveat", "People can say no") - .1
    words_in(d, t, [("REAL LIFE:", t0 + .05, 320, 140, INK), ("MESSIER.", t0 + .2, 470, 140, INK)])
    if t >= tn: box_label(d, X0 + 4, 660, "PEOPLE SAY NO", 50, WHITE, MID, font=BLK)
    if t >= cue("caveat", "you never know") - .1: box_label(d, X0 + 4, 760, "HOW MANY? UNKNOWN", 50, WHITE, MID, font=BLK)
    fig(d, "a model, not a guarantee")

def sc_point(img, d, t):
    t0, tc = S("point"), cue("point", "Then commit") - .15
    words_in(d, t, [("EXPLORE", t0 + .05, 320, 170, MID), ("FIRST.", t0 + .2, 500, 170, MID)] + ([("THEN COMMIT.", tc, 690, 130, SIG)] if t >= tc else []))
    fig(d, "fig. 2 — optimal stopping")

EP.cuts = {"rule": "stay", "result": "stay"}
EP.bg = {"setup": "light", "rule": "light"}
EP.scenes = {"setup": sc_setup, "rule": sc_rule, "sim": sc_sim, "result": sc_result, "caveat": sc_caveat, "point": sc_point}
FX = [*EP.cut_fx(), *[(S("setup") + .2 + i * .12, tick(.035), (i - 4.5) / 5) for i in range(10)], (cue("setup", "they're gone") - .1, thud(.4), 0),
      (cue("rule", "Just look") - .1, pop(.13), -.3), *[(cue("rule", "Then pick") - .1 + i * .25, tick(.04), (i - 3) / 4) for i in range(7)], (cue("rule", "Then pick") + .9, thud(.5), .2),
      *[(S("sim") + .3 + i * max(1.5, E("sim") - S("sim") - .6) / 24, tick(.025), (i % 5 - 2) / 3) for i in range(24)],
      (S("result") + .05, thud(.55), 0), (S("caveat") + .1, pop(.12), 0), (cue("caveat", "People can say no") - .1, pop(.12), -.2),
      (S("point") + .1, pop(.12), 0), (cue("point", "Then commit") - .15, thud(.5), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
