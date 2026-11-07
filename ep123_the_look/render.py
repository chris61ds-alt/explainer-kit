"""NOT JUST YOU – No. 123: the look – men's first fixation on a woman's photo hit chest or waist within 200 ms (Dixson et al.
2011); rating appearance, men AND women looked longer at chest/waist than face (Gervais et al. 2013); being gazed at lowered
women's math scores (Gervais, Vescio & Allen 2011). Look C+D · statement opener with "you" · isometric eye-tracking monitor
with an abstract figure and numbered gaze points · orange reveal: women too."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"fast": .6, "tease": .5, "women": .6, "cost": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["fast", "tease", "women", "cost", "point", "end"]
EP = ThreadEpisode(TL, 123, "THE LOOK", order=ORDER, dark=True, label="EYE-TRACKING · SMALL STUDIES",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Dixson et al. (2011), Arch. Sex. Behav. 40 · Gervais et al. (2013),", "Sex Roles 69 · Gervais, Vescio & Allen (2011), PWQ 35"),
                   music=dict(bpm=92, root=-2, prog="tense", kick="half", audio="v5", gaps=[(E("fast") + .05, S("tease") + .05)]),
                   cover=dict(words=["YOU CATCH", "YOURSELF", "LOOKING."], kicker="Your eyes got there in 0.2 seconds."))

I = Iso(500, 1060, .75)
def monitor(img, d, t, t0, pts, col=INK):
    """isometric screen; on it an abstract figure (head, torso with waist) and numbered gaze points"""
    I.grid(img); I.shadow(d, 0, 0, 260)
    I.box(d, -40, -40, 0, 80, 80, 120)                       # stand
    I.box(d, -260, -30, 120, 520, 60, 380, top=TOP)          # screen block (front face at y = 30)
    Y = 30                                                  # the visible front face of the screen (plane y = 30)
    P = lambda x, z: I.P(x, Y, z)
    d.polygon([P(-240, 140), P(240, 140), P(240, 480), P(-240, 480)], fill=WHITE)      # the display
    d.polygon([P(36 * math.cos(a), 420 + 36 * math.sin(a)) for a in [i * math.pi / 12 for i in range(24)]], fill=MID)   # head
    d.polygon([P(-70, 370), P(70, 370), P(38, 290), P(76, 180), P(-76, 180), P(-38, 290)], fill=MID)                    # torso
    spots = {"face": P(0, 420), "chest": P(0, 345), "waist": P(0, 270)}
    for i, (key, tk) in enumerate(pts):
        if t < tk: continue
        k = back(clamp((t - tk) / .25)); x, y = spots[key]; r = 22 * k
        d.ellipse([x - r, y - r, x + r, y + r], outline=col, width=8)
        if k > .7: d.text((x + 40, y), str(i + 1), font=F(BLK, 40), fill=col, anchor="lm")

def sc_fast(img, d, t):
    t0, tf, tb = S("fast"), cue("fast", "chest or waist") - .1, cue("fast", "Before her face") - .1
    d.text((X0, 320), "EYE-TRACKING", font=F(BLK, 110), fill=INK); d.text((X0 + 4, 440), "where the first look lands", font=F(COND, 48), fill=MID)
    monitor(img, d, t, t0, [("chest", tf), ("waist", tf + .35), ("face", tb)])
    if t >= cue("fast", "Faster than") - .1: box_label(d, X1, 520, "< 0.2 S", 54, WHITE, INK, font=BLK, anchor="ra")
    fig(d, "fig. 1 — schematic, abstract figure")

def sc_tease(img, d, t):
    t0 = S("tease"); words_in(d, t, [("NOT JUST", t0 + .05, 320, 170, INK), ("MEN.", t0 + .2, 500, 200, INK)])
    fig(d, "schematic")

def sc_women(img, d, t):
    t0, tr = S("women"), cue("women", "Asked to rate") - .1
    words_in(d, t, [("WOMEN", t0 + .05, 320, 170, SIG), ("TOO.", t0 + .2, 500, 170, SIG)])
    if t >= tr:
        rows = [("CHEST + WAIST", .8, INK), ("FACE", .4, MID)]
        for j, (lab, v, col) in enumerate(rows):
            k = ease(clamp((t - tr - j * .25) / .5)); y = 720 + j * 170
            d.text((X0, y), lab, font=F(BLK, 46), fill=col); d.rectangle([X0, y + 60, X0 + max(8, 700 * v * k), y + 130], fill=col)
        d.text((X0, 1060), "when rating her looks · men and women", font=F(COND, 40), fill=INK)
    fig(d, "65 people · schematic, direction only")

def sc_cost(img, d, t):
    t0, tm = S("cost"), cue("cost", "solved fewer") - .1
    d.text((X0, 320), "THE COST", font=F(BLK, 140), fill=INK); d.text((X0 + 4, 470), "math problems solved, out of 12", font=F(COND, 46), fill=MID)
    rows = [("NOT STARED AT", 6.0, MID, t0 + .4), ("STARED AT", 4.8, INK, tm)]
    for j, (lab, v, col, tk) in enumerate(rows):
        if t < tk: continue
        k = ease((t - tk) / .5); y = 580 + j * 210
        d.text((X0, y), lab, font=F(BLK, 48), fill=col); w = 640 * v / 6 * k
        d.rectangle([X0, y + 66, X0 + max(8, w), y + 156], fill=col)
        d.text((X0 + max(8, w) + 16, y + 111), "~6" if j == 0 else "<5", font=F(BLK, 64), fill=col, anchor="lm")
    if t >= cue("cost", "Men didn't") - .1: box_label(d, X0 + 4, 1020, "MEN: NO DROP", 44, WHITE, INK, font=BLK)
    fig(d, "small study · women's scores")

def sc_point(img, d, t):
    t0, ts, tl = S("point"), cue("point", "The stare") - .15, cue("point", "Look at her face") - .15
    words_in(d, t, [("THE GLANCE:", t0 + .05, 320, 120, MID), ("FAST.", t0 + .2, 440, 120, MID)])
    if t >= ts: words_in(d, t, [("THE STARE:", ts, 590, 120, INK), ("A CHOICE.", ts + .15, 710, 120, INK)])
    if t >= tl: words_in(d, t, [("LOOK AT HER FACE.", tl, 880, 92, SIG)])
    fig(d, "fig. 2 — eyes up")

EP.cuts = {"women": "stay"}
EP.bg = {"fast": "light"}
EP.scenes = {"fast": sc_fast, "tease": sc_tease, "women": sc_women, "cost": sc_cost, "point": sc_point}
FX = [*EP.cut_fx(), (S("fast") + .1, riser(.8, .04), 0), (cue("fast", "chest or waist") - .1, pop(.12), .2), (cue("fast", "chest or waist") + .25, pop(.12), .2),
      (cue("fast", "Faster than") - .1, tick(.06), .3), (cue("fast", "Before her face") - .1, pop(.13), -.2),
      (S("tease") + .1, thud(.45), 0), (S("women") + .05, thud(.55), 0), (cue("women", "Asked to rate") - .1, pop(.13), -.2),
      (S("cost") + .4, pop(.12), -.2), (cue("cost", "solved fewer") - .1, thud(.5), .2), (cue("cost", "Men didn't") - .1, pop(.12), .3),
      (S("point") + .1, pop(.12), 0), (cue("point", "The stare") - .15, thud(.45), 0), (cue("point", "Look at her face") - .15, thud(.5), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
