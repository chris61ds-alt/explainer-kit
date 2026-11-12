"""NOT JUST YOU – No. 125 (level 2 remake, 12.11.2026): make the first move – Gale-Shapley deferred acceptance with 10 + 10
people and random rankings: askers' average partner rank 2.2 vs 4.8 (Gale & Shapley 1962; Nobel 2012 Roth & Shapley).
Level 2: the two columns are there from frame 0 (ripple), ONE continuous object (no whip cuts), proposals fly in with a spring,
turned-down ones snap back, live counter, orange reveal with each person's rank popping up, loop back into the hook.
Old version: render_v1.py / script_v1.json."""
import os, sys, math, random, statistics as st
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .34, "setup": .34, "run": .3, "reveal": .4, "why": .1})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "setup", "run", "reveal", "why", "end"]
EP = ThreadEpisode(TL, 125, "FIRST MOVE", order=ORDER, dark=True, label="SIMULATION · MATH MODEL",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Gale & Shapley (1962), American Mathematical Monthly 69(1) ·", "Nobel Prize in Economics 2012 (Roth & Shapley)"),
                   music=dict(bpm=104, root=2, prog="major", kick="four", audio="v5"),
                   cover=dict(words=["YOU WAIT", "FOR THEM", "TO TEXT FIRST."], kicker="Here's what it costs you. Simulated."))

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
RANK_A = [A[i].index(MATCH[i]) + 1 for i in range(N)]
RANK_B = {w: B[w].index(i) + 1 for i, w in MATCH.items()}
ASK, WAIT = st.mean(RANK_A), st.mean(RANK_B.values())     # 2.2 / 4.8

LX, RX, Y0, DY = X0 + 150, X1 - 150, 590, 58
T_ASK, T_WAIT = cue("setup", "One side asks") - .1, cue("setup", "The other side") - .1
T_RUN0 = S("run") - .1; T_RUN1 = E("run") + .15                # all proposals happen in here
SLOT = (T_RUN1 - T_RUN0) / len(EVENTS)
T_N2 = cue("reveal", "The ones who waited") - .15
T_BACK = cue("why", "Because right now") - .35                  # loop: links let go, back to the start

def ev_t(i): return T_RUN0 + i * SLOT
def pos(side, i): return (LX, Y0 + i * DY) if side == 0 else (RX, Y0 + i * DY)

def links(t):
    """(m, w, k) for every link standing at time t, k = drawn fraction (spring in, falls away when replaced / at the loop)"""
    out = {}; dead = []
    for i, (m, w, res, old) in enumerate(EVENTS):
        te = ev_t(i)
        if t < te: break
        if res in ("yes", "swap"):
            if w in out: dead.append((out[w][0], w, te))
            out[w] = (m, te)
    cur = [(m, w, spring((t - te) / .35, f=1.4, damp=6)) for w, (m, te) in out.items()]
    return cur, dead

def people(d, t):
    wave = (t - .05) / .9
    for side in (0, 1):
        for i in range(N):
            x, y = pos(side, i); r = 20.0
            if 0 <= wave <= 1.4: r += 9 * max(0, 1 - abs(i / (N - 1) - wave) * 5)       # cold open: ripple down the columns
            if t < T_RUN0 and side == 1 and t >= T_WAIT: r += 2.5 * math.sin(t * 6 + i)    # the waiters, waiting
            col = INK if side == 0 or T_WAIT <= t < T_BACK + .2 else MID
            d.ellipse([x - r, y - r, x + r, y + r], fill=col)
    for side, lab, tk in ((0, "ASK", T_ASK), (1, "WAIT", T_WAIT)):
        if tk <= t < T_BACK + .3:
            k = spring((t - tk) / .4) * (1 - clamp((t - T_BACK) / .3)); x = pos(side, 0)[0]
            d.text((x, Y0 - 60 - 30 * (1 - k)), lab, font=F(BLK, int(46 * max(.2, k))), fill=INK, anchor="mm")

def line(d, a, b, k, col, w):
    d.line([a, (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k)], fill=col, width=w)

def plot(d, t):
    people(d, t)
    back = clamp((t - T_BACK) / .4) if t >= T_BACK else 0
    cur, dead = links(t)
    for m, w, te in dead:                                       # a replaced partner: the old link drops away
        dt = t - te
        if dt < .5:
            a, b = pos(0, m), pos(1, w); dy = 600 * dt * dt
            d.line([(a[0] + 22, a[1] + dy), (b[0] - 22, b[1] + dy)], fill=mix(BG, MID, clamp(1 - dt / .5)), width=5)
    for m, w, k in cur:
        if back >= 1: continue
        a, b = (pos(0, m)[0] + 22, pos(0, m)[1]), (pos(1, w)[0] - 22, pos(1, w)[1])
        line(d, a, b, k * (1 - ease(back)), INK, 7)
    for i, (m, w, res, old) in enumerate(EVENTS):              # turned down: the line shoots out and snaps back
        if res != "no": continue
        dt = t - ev_t(i)
        if 0 <= dt < .4:
            k = math.sin(math.pi * dt / .4) * .9; a, b = (pos(0, m)[0] + 22, pos(0, m)[1]), (pos(1, w)[0] - 22, pos(1, w)[1])
            line(d, a, b, k, MID, 4)
    if S("reveal") <= t < T_BACK + .4:                         # each person's rank of the partner they got
        fade = 1 - clamp((t - T_BACK) / .3) if t >= T_BACK else 1
        for i in range(N):
            for side, rk, tk in ((0, RANK_A[i], S("reveal") + .15 + i * .04), (1, RANK_B.get(i, 0), T_N2 + i * .04)):
                if t < tk: continue
                k = spring((t - tk) / .35) * fade; x, y = pos(side, i); x += -70 if side == 0 else 70
                if k > .05: d.text((x, y), f"#{rk}", font=F(BLK, max(8, int(44 * k))), fill=INK if side == 0 else MID, anchor="mm")

def head(d, t, line_, sub=None):
    d.text((X0, 300), line_, font=F(BLK, 84), fill=INK)
    if t < S("reveal") or t >= T_BACK:
        n = sum(1 for i in range(len(EVENTS)) if t >= ev_t(i)) if t < T_BACK else 0
        d.text((X0, 400), "PROPOSALS", font=F(MONO, 30), fill=MID); d.text((X0 + 230, 388), f"{n}", font=F(BLK, 64), fill=INK)
    else:                                                       # the result, counted up
        ka = ease(clamp((t - S("reveal") - .15) / .7)); kb = ease(clamp((t - T_N2) / .7))
        d.text((X0, 400), "ASKED", font=F(MONO, 30), fill=MID); d.text((X0 + 140, 388), f"#{1 + (ASK - 1) * ka:.1f}", font=F(BLK, 64), fill=SIG)
        if t >= T_N2: d.text((X0 + 420, 400), "WAITED", font=F(MONO, 30), fill=MID); d.text((X0 + 580, 388), f"#{1 + (WAIT - 1) * kb:.1f}", font=F(BLK, 64), fill=INK)
    if sub: d.text((X1, 408), sub, font=F(MONO, 26), fill=MID, anchor="ra")

def sc_hook(img, d, t): head(d, t, "WHO TEXTS FIRST?"); plot(d, t); fig(d, "simulation")
def sc_setup(img, d, t): head(d, t, "10 + 10 PEOPLE", sub="random rankings"); plot(d, t); fig(d, "everyone ranks everyone, secretly")
def sc_run(img, d, t):
    nd = sum(1 for i, e in enumerate(EVENTS) if e[2] == "no" and t >= ev_t(i))
    head(d, t, "ROUND AFTER ROUND", sub=f"{nd} turned down"); plot(d, t); fig(d, "deferred acceptance · simulation")
def sc_reveal(img, d, t): head(d, t, "ASKING WINS."); plot(d, t); fig(d, "#1 = their first choice · simulation")
def sc_why(img, d, t):
    head(d, t, "NEVER WORSE OFF." if t < T_BACK else "WHO TEXTS FIRST?"); plot(d, t)
    fig(d, "proven for this model · real dating is messier")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.bg = {"hook": "dark", "setup": "dark", "run": "dark", "reveal": "orange", "why": "dark"}
EP.scenes = {"hook": sc_hook, "setup": sc_setup, "run": sc_run, "reveal": sc_reveal, "why": sc_why}
FX = [(.05, whoosh(.8, .05), 0), (T_ASK, pop(.1), -.4), (T_WAIT, pop(.1), .4),
      *[(ev_t(i), tick(.03) if e[2] == "no" else pop(.06), -.3 if e[2] == "no" else .2) for i, e in enumerate(EVENTS)],
      (S("reveal") + .1, thud(.55), 0), (T_N2, pop(.14), .3), (T_BACK, whoosh(.45, .05), 0)]
if __name__ == "__main__": EP.run(FX)
