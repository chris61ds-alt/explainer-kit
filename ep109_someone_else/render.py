"""NOT JUST YOU – No. 109: fantasizing about someone else – 98 % of men, 80 % of women in relationships (past 2 months,
Hicks & Leitenberg 2001); ~38 % during partnered sex, target not tied to relationship satisfaction (Gormezano et al. 2026).
Look C+D · statement opener with "you" · isometric bed with a thought cloud (during sex) · orange reveal: women 80 %."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"study": .6, "men": .5, "women": .6, "during": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["study", "men", "women", "during", "point", "end"]
EP = ThreadEpisode(TL, 109, "SOMEONE ELSE", order=ORDER, dark=True, label="SURVEY · 349 IN RELATIONSHIPS",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Hicks & Leitenberg (2001), J. of Sex Research 38(1) ·", "Gormezano et al. (2026), Archives of Sexual Behavior"),
                   music=dict(bpm=96, root=-2, prog="dream", kick="four", audio="v5", gaps=[(E("study") + .05, S("men") + .05)]),
                   cover=dict(words=["YOU FANTASIZE", "ABOUT", "SOMEONE ELSE."], kicker="So do most people in a relationship."))

FIELD = (X0 + 14, 720, X1, 1110)
def sc_study(img, d, t):
    t0, tp = S("study"), cue("study", "past two months") - .1
    counter(d, X0, 320, t, t0 + .1, .8, 349, "{:.0f}", 230, INK)
    d.text((X0 + 6, 565), "people, all in relationships", font=F(COND, 46), fill=INK)
    if t >= tp: box_label(d, X0 + 4 - (1 - ease((t - tp) / .2)) * 40, 640, "PAST 2 MONTHS", 40, WHITE, INK, font=BLK)
    dot_field(d, FIELD, t, cell=30, col=MID, hit={40, 41, 100, 101, 160, 161}, hitcol=INK)
    fig(d, "every pair of dots: one couple · schematic")

def bars(d, t, show_w):
    d.text((X0, 320), "FANTASIZED", font=F(BLK, 120), fill=INK); d.text((X0 + 4, 450), "about someone else", font=F(COND, 50), fill=MID)
    rows = [("MEN", 98, INK, S("men") + .3)] + ([("WOMEN", 80, SIG, S("women") + .1)] if show_w else [])
    for j, (lab, v, col, tk) in enumerate(rows):
        if t < tk: continue
        k = ease((t - tk) / .6); y = 590 + j * 250
        d.text((X0, y), lab, font=F(BLK, 54), fill=col); w = 620 * v / 98 * k
        d.rectangle([X0, y + 75, X0 + max(8, w), y + 200], fill=col)
        d.text((X0 + max(8, w) + 16, y + 137), f"{v * k:.0f} %", font=F(BLK, 72), fill=col, anchor="lm")

def sc_men(img, d, t): bars(d, t, False); fig(d, "at least occasionally, past 2 months")
def sc_women(img, d, t): bars(d, t, True); fig(d, "at least occasionally, past 2 months")

IB = Iso(640, 1060, .55)
def cloud(d, x, y, k):
    """thought cloud: three rising dots, then the cloud with a stranger's silhouette inside"""
    for i, (dx, dy, r) in enumerate(((-120, 120, 12), (-80, 70, 18), (-30, 20, 26))):
        if k > i * .15: d.ellipse([x + dx - r, y + dy - r, x + dx + r, y + dy + r], fill=MID)
    kc = clamp((k - .45) / .4)
    if kc <= 0: return
    R = 120 * back(kc)
    for ox, oy, rr in ((-70, -10, .62), (0, -40, .75), (80, -10, .62), (0, 30, .6), (-40, 25, .5), (45, 25, .5)):
        d.ellipse([x + 90 + ox * R / 120 - rr * R, y - 120 + oy * R / 120 - rr * R, x + 90 + ox * R / 120 + rr * R, y - 120 + oy * R / 120 + rr * R], fill=WHITE)
    if kc > .7:
        hx, hy = x + 90, y - 150; d.ellipse([hx - 26, hy - 26, hx + 26, hy + 26], fill=MID)
        d.chord([hx - 52, hy + 26, hx + 52, hy + 120], 180, 360, fill=MID)
        d.text((hx, hy + 70), "?", font=F(BLK, 44), fill=WHITE, anchor="mm")

def sc_during(img, d, t):
    t0, tn = S("during"), cue("during", "thirty-eight") - .1
    d.text((X0, 320), "EVEN", font=F(BLK, 130), fill=INK); d.text((X0, 455), "DURING SEX:", font=F(BLK, 130), fill=INK)
    IB.grid(img); IB.shadow(d, 0, 0, 200)
    A = bed(IB, d, t, T=[t0 + .05 + i * .07 for i in range(7)])
    if t >= t0 + .6:
        p = IB.P(*A["pillow_r"]); cloud(d, p[0] - 40, p[1] - 30, clamp((t - t0 - .6) / .9))
    if t >= tn:                                            # the number, left of the bed
        k = ease((t - tn) / .3)
        d.text((X0 - (1 - k) * 40, 640), "~38 %", font=F(BLK, 130), fill=INK)
        d.text((X0 + 4, 790), "think of", font=F(COND, 46), fill=INK); d.text((X0 + 4, 845), "someone else", font=F(COND, 46), fill=INK)
    fig(d, "newer study · 546 adults · schematic")

def sc_point(img, d, t):
    t0, tr, tn = S("point"), cue("point", "not a red flag") - .15, cue("point", "It's normal") - .15
    words_in(d, t, [("NOT TIED TO", t0 + .05, 320, 100, MID), ("HOW HAPPY", t0 + .2, 420, 100, MID), ("THEY WERE.", t0 + .35, 520, 100, MID)])
    if t >= tr:                                            # the red flag, crossed out
        k = ease((t - tr) / .3); fx, fy = X0 + 40, 680
        d.line([fx, fy, fx, fy + 230 * k], fill=INK, width=12)
        d.polygon([(fx, fy), (fx + 170 * k, fy + 45), (fx, fy + 90)], fill=MID)
        if t >= tr + .3: d.line([fx - 30, fy - 20, fx + 200, fy + 220], fill=INK, width=12)
        d.text((X0 + 270, fy + 40), "NOT A", font=F(BLK, 80), fill=INK); d.text((X0 + 270, fy + 130), "RED FLAG.", font=F(BLK, 80), fill=INK)
    if t >= tn: words_in(d, t, [("IT'S NORMAL.", tn, 950, 120, SIG)])
    fig(d, "one snapshot study · a link, not proof")

EP.cuts = {"women": "stay"}
EP.bg = {"during": "light"}
EP.scenes = {"study": sc_study, "men": sc_men, "women": sc_women, "during": sc_during, "point": sc_point}
FX = [*EP.cut_fx(), (S("study") + .1, riser(.8, .04), 0), (cue("study", "past two months") - .1, pop(.13), .2),
      (S("men") + .3, thud(.5), 0), (S("women") + .1, thud(.55), 0),
      *[(S("during") + .05 + i * .07, tick(.04), (i - 3) / 4) for i in range(7)], (S("during") + .6, pop(.1), .2), (S("during") + 1.1, pop(.15), .3),
      (cue("during", "thirty-eight") - .1, pop(.14), -.3),
      (S("point") + .05, pop(.12), 0), (cue("point", "not a red flag") - .15, thud(.45), 0), (cue("point", "It's normal") - .15, thud(.5), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
