"""NOT JUST YOU – No. 125 (simulation): make the first move – Gale-Shapley deferred acceptance with 10 + 10 people and random
rankings: askers' average partner rank 2.2 vs 4.8; swapped 2.1 vs 4.4 (Gale & Shapley 1962; Nobel 2012 Roth & Shapley).
Look C+D · statement opener with "you" · live matching simulation (proposals as lines, rounds counter) · orange reveal."""
import os, sys, math, random, statistics as st
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"setup": .6, "run": .5, "score": .5, "result": .6, "swap": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["setup", "run", "score", "result", "swap", "point", "end"]
EP = ThreadEpisode(TL, 125, "FIRST MOVE", order=ORDER, dark=True, label="SIMULATION · MATH MODEL",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Gale & Shapley (1962), American Mathematical Monthly 69(1) ·", "Nobel Prize in Economics 2012 (Roth & Shapley)"),
                   music=dict(bpm=104, root=2, prog="major", kick="four", audio="v5", gaps=[(E("setup") + .05, S("run") + .05)]),
                   cover=dict(words=["MAKE THE", "FIRST", "MOVE."], kicker="It's math. Nobel-prize math."))

N = 10; R = random.Random(2)
A = [R.sample(range(N), N) for _ in range(N)]; B = [R.sample(range(N), N) for _ in range(N)]
def gale_shapley(prop, rec):
    free = list(range(N)); nxt = [0] * N; eng = {}; events = []
    rank = [{m: i for i, m in enumerate(rec[w])} for w in range(N)]
    while free:
        m = free.pop(0); w = prop[m][nxt[m]]; nxt[m] += 1
        if w not in eng: eng[w] = m; events.append((m, w, "yes", None))
        elif rank[w][m] < rank[w][eng[w]]: old = eng[w]; free.append(old); eng[w] = m; events.append((m, w, "swap", old))
        else: free.append(m); events.append((m, w, "no", None))
    return {m: w for w, m in eng.items()}, events
MATCH, EVENTS = gale_shapley(A, B)
ASK = st.mean(A[i].index(MATCH[i]) + 1 for i in range(N)); WAIT = st.mean(B[w].index(i) + 1 for i, w in MATCH.items())   # 2.2 / 4.8

LX, RX, Y0, DY = X0 + 90, X1 - 90, 590, 52
def people(d, lab_l="ASK", lab_r="WAIT", col_l=INK, col_r=MID):
    d.text((LX, Y0 - 44), lab_l, font=F(BLK, 40), fill=col_l, anchor="mm"); d.text((RX, Y0 - 44), lab_r, font=F(BLK, 40), fill=col_r, anchor="mm")
    for i in range(N):
        y = Y0 + i * DY
        d.ellipse([LX - 18, y - 18, LX + 18, y + 18], fill=col_l); d.ellipse([RX - 18, y - 18, RX + 18, y + 18], fill=col_r)

def state_at(k):
    """current engagements after the first k proposal events"""
    eng = {}
    for (m, w, res, old) in EVENTS[:k]:
        if res in ("yes", "swap"): eng[w] = m
    return eng

def draw_links(d, eng, col=INK, w=6):
    for wv, m in eng.items(): d.line([LX + 20, Y0 + m * DY, RX - 20, Y0 + wv * DY], fill=col, width=w)

def sc_setup(img, d, t):
    t0, ta = S("setup"), cue("setup", "One side asks") - .1
    d.text((X0, 320), "10 + 10 PEOPLE", font=F(BLK, 100), fill=INK); d.text((X0 + 4, 430), "everyone ranks everyone, secretly", font=F(COND, 46), fill=MID)
    people(d)
    if t >= ta:                                              # one demo proposal
        k = ease(clamp((t - ta) / .5)); m, w = EVENTS[0][0], EVENTS[0][1]
        a, b = (LX + 20, Y0 + m * DY), (RX - 20, Y0 + w * DY); d.line([a, (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k)], fill=INK, width=6)
    fig(d, "random rankings · simulation")

def sc_run(img, d, t):
    t0 = S("run"); dur = max(1.2, E("run") - t0 - .2)
    d.text((X0, 320), "ROUND", font=F(BLK, 100), fill=INK)
    k = int(clamp((t - t0) / dur) * len(EVENTS)); people(d); draw_links(d, state_at(k))
    if 0 < k <= len(EVENTS):
        m, w, res, old = EVENTS[k - 1]
        col = MID if res == "no" else INK; d.line([LX + 20, Y0 + m * DY, RX - 20, Y0 + w * DY], fill=col, width=3)
    d.text((X0 + 430, 320), f"{min(len(EVENTS), k)}", font=F(BLK, 100), fill=INK)
    d.text((X0 + 4, 430), f"proposals · {sum(1 for e in EVENTS[:k] if e[2] == 'no')} turned down", font=F(COND, 46), fill=MID)
    fig(d, "deferred acceptance · simulation")

def sc_score(img, d, t):
    t0 = S("score")
    d.text((X0, 320), "HOW HAPPY?", font=F(BLK, 110), fill=INK); d.text((X0 + 4, 440), "rank of the partner each one got", font=F(COND, 46), fill=MID)
    people(d); draw_links(d, MATCH)
    fig(d, "1 = their first choice")

def bars(d, t, t0, rows, y0=560):
    for j, (lab, v, col) in enumerate(rows):
        k = ease(clamp((t - t0 - j * .35) / .5)); y = y0 + j * 210
        d.text((X0, y), lab, font=F(BLK, 50), fill=col); w = 640 * v / 5 * k
        d.rectangle([X0, y + 66, X0 + max(8, w), y + 156], fill=col)
        d.text((X0 + max(8, w) + 16, y + 111), f"#{v * k:.1f}" if k > .05 else "", font=F(BLK, 64), fill=col, anchor="lm")

def sc_result(img, d, t):
    t0 = S("result")
    d.text((X0, 320), "THE ASKERS:", font=F(BLK, 110), fill=SIG); d.text((X0 + 4, 440), "average rank of their match (lower = better)", font=F(COND, 42), fill=INK)
    bars(d, t, t0 + .1, [("ASKED", ASK, SIG), ("WAITED", WAIT, INK)])
    fig(d, "simulation · 10 + 10 people")

def sc_swap(img, d, t):
    t0, tp = S("swap"), cue("swap", "The math is proven") - .1
    d.text((X0, 320), "SWAPPED:", font=F(BLK, 110), fill=INK)
    M2, _ = gale_shapley(B, A); ask2 = st.mean(B[i].index(M2[i]) + 1 for i in range(N)); wait2 = st.mean(A[w].index(i) + 1 for i, w in M2.items())
    bars(d, t, t0 + .2, [("ASKED", ask2, INK), ("WAITED", wait2, MID)], y0=500)
    if t >= tp: box_label(d, X0 + 4 - (1 - ease((t - tp) / .2)) * 40, 960, "ASKING: NEVER WORSE", 54, WHITE, INK, font=BLK)
    fig(d, "proven theorem, Gale & Shapley 1962")

def sc_point(img, d, t):
    t0, ts = S("point"), cue("point", "send the first") - .2
    words_in(d, t, [("REAL DATING:", t0 + .05, 320, 120, MID), ("MESSIER.", t0 + .2, 440, 120, MID)])
    if t >= ts: words_in(d, t, [("SEND THE", ts, 620, 140, SIG), ("FIRST MESSAGE.", ts + .15, 760, 110, SIG)])
    fig(d, "fig. 2 — a model, not your love life")

EP.cuts = {"run": "stay", "score": "stay"}
EP.bg = {"setup": "light", "run": "light", "score": "light"}
EP.scenes = {"setup": sc_setup, "run": sc_run, "score": sc_score, "result": sc_result, "swap": sc_swap, "point": sc_point}
_rd = max(1.2, E("run") - S("run") - .2)
FX = [*EP.cut_fx(), (cue("setup", "One side asks") - .1, whoosh(.4, .05), .2),
      *[(S("run") + (i + 1) / len(EVENTS) * _rd, tick(.035) if EVENTS[i][2] != "no" else pop(.06), .3 if EVENTS[i][2] != "no" else -.3) for i in range(len(EVENTS))],
      (S("score") + .1, riser(.8, .04), 0), (S("result") + .05, thud(.55), 0), (S("result") + .45, pop(.13), .3),
      (S("swap") + .2, whoosh(.5, .05), 0), (cue("swap", "The math is proven") - .1, thud(.45), 0),
      (S("point") + .1, pop(.12), 0), (cue("point", "send the first") - .2, thud(.5), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
