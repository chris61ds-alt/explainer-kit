"""NOT JUST YOU · AFTER DARK – No. 46: 'kinky' acts are common (Herbenick et al. 2017, US probability sample)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .8, "result": .5, "more": .5, "both": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "more", "both", "point", "end"]
EP = Episode(TL, 46, "KINK", order=ORDER, dark=True, series="NOT JUST YOU · AFTER DARK",
             chapters={"hook": "NICHE?", "study": "THE SAMPLE", "result": "SPANKING", "more": "AND MORE", "both": "WOMEN & MEN", "point": "THE RULE"},
             sources=("Herbenick et al. (2017), PLoS ONE 12(7)", "e0181198 · US probability sample"),
             music=dict(bpm=98, root=-1, prog="tense", kick="four", gaps=[(E("study") + .05, S("result") + .05)]),
             cover=dict(words=["KINK IS", "NICHE?"], kicker="Not even close."))

def crowd(d, t, n, hit, y, s, tk, x0=X0 + 40, x1=X1 - 40):
    gap = (x1 - x0) / max(1, n - 1)
    for i in range(n):
        k = ease((t - tk - i * .04) / .3)
        if k <= 0: continue
        picto(d, x0 + i * gap, y + (1 - k) * 40, s, SIG if i in hit else (INK if i % 2 else MID), f=1 if i % 2 else -1, pose=IDLE)

def sc_hook(img, d, t):
    nc = cue("hook", "not even")
    d.text((X0 - 6, 300), "NICHE?", font=F(BLK, 230), fill=INK if t < nc else RULE)
    if t >= nc - .1:
        k = ease((t - nc + .1) / .3); d.line([X0, 440, X0 + 800 * k, 380], fill=SIG, width=14)
        words_in(d, t, [("NOT EVEN", nc, 560, 120, SIG), ("CLOSE.", nc + .25, 680, 120, SIG)])
    if t < nc:
        spotlight(d, 480, top=760, w=150); picto(d, 480, FLOOR, .7, SIG, pose=WORRY)
    else:
        crowd(d, t, 7, (1, 3, 5), FLOOR, .6, nc)
    fig(d, "fig. 1 — the thing nobody else does?")

def sc_study(img, d, t):
    t0 = S("study"); k = clamp((t - t0 - .3) / 2.2)
    counter(d, X0, 300, t, t0 + .1, 1.0, 2021, "{:,.0f}", 220, SIG)
    d.text((X0 + 6, 540), "US adults, nationally representative", font=F(COND, 36), fill=INK)
    for i in range(int(400 * k)):
        r, c = divmod(i, 25); x = X0 + 20 + c * 34; y = 620 + r * 30
        d.rectangle([x - 8, y - 8, x + 8, y + 8], fill=INK if i % 9 else SIG)
    fig(d, "probability sample, 2015 · Herbenick et al., 2017")

def sc_result(img, d, t):
    t0 = S("result"); tk = cue("result", "thirty")
    d.text((X0, 300), "≥", font=F(BLK, 120), fill=INK)
    counter(d, X0 + 90, 280, t, tk - .2, .6, 30, "{:.0f} %", 220, SIG)
    if t >= cue("result", "spanking"): box_label(d, X0, 560, "TRIED SPANKING", 40, WHITE, INK)
    crowd(d, t, 10, (1, 5, 8), FLOOR, .4, t0 + .2)
    fig(d, "lifetime experience · 3 in 10")

def sc_more(img, d, t):
    t0 = S("more")
    d.text((X0, 300), "AND MORE", font=F(BLK, 140), fill=INK)
    hbar(d, 520, .75, 1, RULE, "spanking  ≥ 30 %", h=80)
    hbar(d, 690, .55, (t - cue("more", "role play") + .3) / .5, SIG, "role play  ≥ 22 %", h=80)
    hbar(d, 860, .50, (t - cue("more", "tied up") + .3) / .5, INK, "tied up / tying  ≥ 20 %", h=80)
    if t >= cue("more", "tied up") + .3: dim_h(d, X0, X0 + 840 * .5, 1010, (t - cue("more", "tied up") - .3) / .4, SIG, "≈ 1 in 5", 28)
    fig(d, "share of US adults, ever · bars to scale of 40 %")

def sc_both(img, d, t):
    t0 = S("both")
    d.text((X0, 300), "WOMEN", font=F(BLK, 130), fill=SIG); d.text((X0, 440), "& MEN", font=F(BLK, 130), fill=INK)
    groups = [("spanking", 34, 30), ("tied up", 21, 22)]
    base = 1060; sc = 9
    for g, (lab, w, m) in enumerate(groups):
        gx = X0 + 80 + g * 420; k = ease((t - t0 - .2 - g * .4) / .5)
        for j, (v, col) in enumerate(((w, SIG), (m, INK))):
            x = gx + j * 130; h = v * sc * k
            d.rectangle([x, base - h, x + 110, base], fill=col)
            if k > .9: d.text((x + 55, base - h - 12), f"{v} %", font=F(BLK, 34), fill=col, anchor="md")
        d.text((gx + 120, base + 16), lab, font=F(COND, 30), fill=INK, anchor="ma")
    if t >= cue("both", "similar"): box_label(d, X1, 640, "SIMILAR", 34, WHITE, INK, anchor="ra")
    legend(d, [(SIG, "women"), (INK, "men")], y=600)
    fig(d, "lifetime experience by gender")

def sc_point(img, d, t):
    t0 = S("point"); tc = cue("point", "the one rule")
    words_in(d, t, [("JUST", t0 + .2, 300, 170, INK), ("TUESDAY.", cue("point", "tuesday") - .2, 470, 170, SIG)] if t < tc - .2 else
             [("THE RULE:", tc - .2, 300, 130, INK), ("CONSENT.", cue("point", "consent") - .2, 440, 160, SIG)])
    if t < tc - .2:
        x0, y0 = 560, 720; d.rectangle([x0, y0, x0 + 300, y0 + 260], outline=INK, width=5); d.rectangle([x0, y0, x0 + 300, y0 + 60], fill=SIG)
        d.text((x0 + 150, y0 + 30), "TUE", font=F(BLK, 36), fill=WHITE, anchor="mm"); [d.rectangle([x0 + 30 + c * 85, y0 + 90 + r * 55, x0 + 70 + c * 85, y0 + 125 + r * 55], fill=SIG if (r, c) == (1, 1) else RULE) for r in range(3) for c in range(3)]
        picto(d, 300, FLOOR, .9, INK, f=1, pose=SHRUG)
    else:
        picto(d, 380, FLOOR, .9, INK, f=1, pose=TALK(t)); picto(d, 580, FLOOR, .9, SIG, f=-1, pose=TALK(t, 2))
        if t >= cue("point", "consent"): speech_box(d, 400, 660, 160, (t - cue("point", "consent")) / .3, INK, 1, "YES", 38)
    fig(d, "fig. 2 — ordinary, as long as everyone says yes")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "more": sc_more, "both": sc_both, "point": sc_point}
FX = [(0.0, thud(.5), 0), (cue("hook", "not even"), rewind_sfx(.1, .3), 0), *[(cue("hook", "not even") + i * .04, pop(.08), (i - 4) / 4) for i in range(0, 9, 2)],
      *EP.cut_fx(), *[(S("study") + .3 + i * .15, tick(.04), (i % 5 - 2) / 3) for i in range(14)],
      (S("result") + .05, thud(.55), 0), (cue("result", "spanking"), snare(.06), 0), (cue("more", "role play"), pop(.15), -.2), (cue("more", "tied up"), pop(.15), .2),
      (cue("both", "similar"), thud(.35), 0), (cue("point", "tuesday"), pop(.15), 0), (cue("point", "consent"), thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
