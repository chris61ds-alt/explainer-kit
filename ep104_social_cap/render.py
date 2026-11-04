"""NOT JUST YOU – No. 104: limiting social media to 30 min/day (10 per app) reduced loneliness + depression over 3 weeks
(Hunt, Marx, Lipson & Young 2018). Look C+D · guess opener."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from tips import phone as _iso_phone
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .6, "limit": .5, "result": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "limit", "result", "point", "end"]
EP = ThreadEpisode(TL, 104, "SOCIAL CAP", order=ORDER, dark=True, label="EXPERIMENT · 143 STUDENTS",
                   chapters={k: "" for k in ORDER[:-1]}, sources=("Hunt, Marx, Lipson & Young (2018), No More FOMO,", "J. of Social and Clinical Psychology 37(10)"),
                   music=dict(bpm=100, root=-2, prog="dream", kick="four", audio="v5", gaps=[(E("study") + .05, S("limit") + .05)]),
                   cover=dict(words=["30 MINUTES", "A DAY.", "LESS LONELY."], kicker="Social media, capped."))
APPS = ["FACEBOOK", "INSTAGRAM", "SNAPCHAT"]

def phone(d, cx, cy, s=1.0, col=INK):
    d.rounded_rectangle([cx - 110 * s, cy - 200 * s, cx + 110 * s, cy + 200 * s], radius=int(30 * s), outline=col, width=int(8 * s))
    d.rounded_rectangle([cx - 30 * s, cy - 186 * s, cx + 30 * s, cy - 176 * s], radius=4, fill=col)

def sc_hook(img, d, t):
    t0 = S("hook"); words_in(d, t, [("NOT", t0 + .05, 320, 170, INK), ("ZERO.", t0 + .2, 490, 170, SIG)])
    phone(d, 480, 880, .9); d.text((480, 880), "0 MIN?", font=F(BLK, 40), fill=MID, anchor="mm")
    if t >= t0 + .3: d.line([380, 960, 580, 800], fill=INK, width=8)
    fig(d, "fig. 1 — schematic")

def sc_study(img, d, t):
    t0, th = S("study"), cue("study", "half of them") - .1
    counter(d, X0, 320, t, t0 + .1, .8, 143, "{:.0f}", 230, INK); d.text((X0 + 6, 565), "students · 3 weeks", font=F(COND, 46), fill=INK)
    if t >= th:
        for i, a in enumerate(APPS):
            k = back(clamp((t - th - i * .15) / .3)); x = X0 + 30 + i * 280; y = 720
            d.rounded_rectangle([x, y, x + 220 * k, y + 220 * k], radius=40, fill=MID)
            if k > .8: d.text((x + 110, y + 250), a, font=F(MONO, 28), fill=INK, anchor="ma")
        if t >= cue("study", "as usual") - .1: box_label(d, X0, 1040, "HALF: AS USUAL", 38, WHITE, MID, font=BLK)
    fig(d, "randomized")

def apps(d, t, t0):
    for i, a in enumerate(APPS):
        x = X0 + 30 + i * 280; y = 640
        d.rounded_rectangle([x, y, x + 220, y + 220], radius=40, fill=INK)
        clock(d, x + 110, y + 110, 70, clamp((t - t0 - i * .3) / .5), col=BG)
        d.text((x + 110, y + 250), "10 MIN", font=F(BLK, 40), fill=INK, anchor="ma"); d.text((x + 110, y + 300), a, font=F(MONO, 24), fill=MID, anchor="ma")

def sc_limit(img, d, t):
    t0 = S("limit"); d.text((X0, 320), "THE OTHER", font=F(BLK, 130), fill=INK); d.text((X0, 455), "HALF:", font=F(BLK, 130), fill=INK)
    apps(d, t, t0 + .1); tt = cue("limit", "Thirty minutes") - .1
    if t >= tt: box_label(d, X1, 1010, "= 30 MIN A DAY", 50, WHITE, INK, font=BLK, anchor="ra")
    fig(d, "limited group")

def sc_result(img, d, t):
    t0 = S("result"); d.text((X0, 320), "AFTER", font=F(BLK, 130), fill=INK); d.text((X0, 455), "3 WEEKS:", font=F(BLK, 130), fill=INK)
    for j, (lab, tk) in enumerate((("LONELINESS", t0 + .1), ("DEPRESSION", cue("result", "Depression") - .1))):
        if t < tk: continue
        k = ease((t - tk) / .4); y = 680 + j * 200
        d.text((X0, y), lab, font=F(BLK, 80), fill=SIG)
        ax = X1 - 60; d.polygon([(ax - 40, y + 10 + 40 * k), (ax + 40, y + 10 + 40 * k), (ax, y + 90 + 40 * k)], fill=SIG)
    fig(d, "vs. the usual-use group")

IP = Iso(470, 960, .95)
def sc_point(img, d, t):
    t0, tc = S("point"), cue("point", "Just cap it") - .2
    IP.grid(img); IP.shadow(d, 0, 0, 230)
    A = _iso_phone(IP, d, t, msgs=[("l", t0 + .1, MID), ("r", t0 + .3, MID)], timer=(tc, "30"), timer_col=SIG if t >= tc else TOP)
    words_in(d, t, [("DON'T QUIT.", t0 + .05, 320, 140, MID)] + ([("CAP IT.", tc, 480, 200, SIG)] if t >= tc else []))
    if t >= tc: p = IP.P(*A["timer"]); callout(d, p, "r", p[1] - 70, 1, "30 MIN A DAY", SIG, k=(t - tc) / .4)
    fig(d, "fig. 2 — schematic")

EP.cuts = {"result": "stay"}
EP.bg = {"point": "light"}
EP.scenes = {"hook": sc_hook, "study": sc_study, "limit": sc_limit, "result": sc_result, "point": sc_point}
FX = [*EP.cut_fx(), (S("hook") + .05, thud(.45), 0), (S("hook") + .3, whoosh(.2, .05), 0), (S("study") + .1, riser(.8, .04), 0), (cue("study", "as usual") - .1, thud(.4), 0), (cue("study", "three weeks") - .1, tick(.06), .2),
      *[(cue("study", "half of them") - .1 + i * .15, pop(.12), (i - 1) / 2) for i in range(3)],
      *[(S("limit") + .1 + i * .3, tick(.05), (i - 1) / 2) for i in range(3)], (cue("limit", "Thirty minutes") - .1, thud(.45), .3),
      (S("result") + .1, thud(.55), 0), (cue("result", "Depression") - .1, pop(.15), 0),
      (S("point") + .05, pop(.12), 0), (cue("point", "Just cap it") - .2, thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
