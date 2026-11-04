"""NOT JUST YOU – No. 102: the most important part of an apology – own it, offer repair; asking forgiveness matters least (Lewicki et al. 2016). Look C+D."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "own": .5, "fix": .5, "least": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "own", "fix", "least", "point", "end"]
EP = ThreadEpisode(TL, 102, "APOLOGY", order=ORDER, dark=True, label="SURVEY EXPERIMENTS · 755 PEOPLE",
                   chapters={k: "" for k in ORDER[:-1]}, sources=("Lewicki, Polin & Lount (2016), An Exploration of the", "Structure of Effective Apologies, NCMR 9(2)"),
                   music=dict(bpm=96, root=-2, prog="dream", kick="four", audio="v5"),
                   cover=dict(words=["THE MOST", "IMPORTANT PART", "OF A SORRY."], kicker="And the least useful one."))
PARTS = ["REGRET", "EXPLANATION", "RESPONSIBILITY", "REPENTANCE", "REPAIR", "FORGIVENESS?"]
RANK = {"RESPONSIBILITY": ("#1", "own", INK), "REPAIR": ("#2", "fix", INK), "FORGIVENESS?": ("LAST", "least", SIG)}

def sc_list(img, d, t):
    t0 = S("hook"); cur = EP.current(t)
    d.text((X0, 320), "6 PARTS", font=F(BLK, 150), fill=INK); d.text((X0 + 4, 480), "of an apology, tested", font=F(COND, 50), fill=MID)
    counter(d, X1, 330, t, t0 + .3, .8, 755, "{:.0f}", 70, INK, anchor="ra"); d.text((X1, 410), "PEOPLE", font=F(MONO, 26), fill=MID, anchor="ra")
    for i, p in enumerate(PARTS):
        ti = t0 + .4 + i * .18
        if t < ti: continue
        y = 580 + i * 86; k = ease((t - ti) / .25); r = RANK.get(p); lit = r and t >= S(r[1]) + .05
        col = (r[2] if lit else (MID if cur in ("own", "fix", "least") else INK))
        d.text((X0 + 90 - (1 - k) * 40, y), p, font=F(MONO, 44), fill=col); d.text((X0, y), f"{i + 1:02d}", font=F(MONO, 44), fill=MID)
        if lit: box_label(d, X1, y - 4, r[0], 40, WHITE, r[2], font=BLK, anchor="ra")
        if lit and p == "FORGIVENESS?": d.line([X0 + 86, y + 26, X0 + 90 + d.textlength(p, font=F(MONO, 44)) + 6, y + 26], fill=SIG, width=6)
    say = {"own": "This was my fault.", "fix": "How can I fix it?", "least": "Please forgive me?"}.get(cur)
    if say: bubble(d, "you", say, (t - S(cur) - .2) / .3, col=MID if cur == "least" else INK, y=500, x=700, size=34)
    fig(d, "ranked by how much each part helped")

def sc_point(img, d, t):
    t0 = S("point")
    words_in(d, t, [("OWN IT.", t0 + .05, 320, 170, INK), ("FIX IT.", cue("point", "Fix it") - .15, 500, 170, INK), ("DON'T BEG.", cue("point", "Don't beg") - .15, 680, 150, SIG)])
    fig(d, "fig. 2 — the apology")

EP.cuts = {"own": "stay", "fix": "stay", "least": "stay"}
EP.scenes = {"hook": sc_list, "own": sc_list, "fix": sc_list, "least": sc_list, "point": sc_point}
FX = [*EP.cut_fx(), (S("hook") + .05, thud(.45), 0), *[(S("hook") + .4 + i * .18, tick(.04), (i % 5 - 2) / 3) for i in range(6)],
      (S("own") + .05, thud(.45), 0), (S("own") + .2, pop(.13), -.2), (S("fix") + .05, thud(.45), 0), (S("fix") + .2, pop(.13), -.2),
      (S("least") + .05, thud(.55), 0), (S("least") + .2, pop(.13), -.2),
      (S("point") + .05, pop(.12), 0), (cue("point", "Fix it") - .15, pop(.12), 0), (cue("point", "Don't beg") - .15, thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
