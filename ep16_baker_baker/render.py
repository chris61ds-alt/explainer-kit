"""NOT JUST YOU – No. 16: the Baker/baker paradox (McWeeny et al. 1987; Cohen 1990). Area: memory."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .45, "study": .8, "result": .5, "name": .5, "why": .5, "tip": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "name", "why", "tip", "end"]
EP = Episode(TL, 16, "BAKER / BAKER", order=ORDER,
             chapters={"hook": "THE NAME", "study": "THE STUDY", "result": "THE RESULT", "name": "THE PARADOX", "why": "WHY", "tip": "THE HOOK"},
             sources=("McWeeny, Young, Hay & Ellis (1987), Brit. J. Psych. 78", "Cohen (1990), Brit. J. Psych. 81"),
             music=dict(bpm=96, root=3, prog="warm", kick="half", gaps=[(E("study") + .05, S("result") + .05)]),
             cover=dict(words=["WHAT", "WAS HIS", "NAME?"], kicker="The Baker/baker paradox."))

def dog(d, x, y, s=1.0, col=INK, t=0.0):
    d.rounded_rectangle([x - 60 * s, y - 70 * s, x + 50 * s, y - 30 * s], radius=18 * s, fill=col)
    d.ellipse([x + 30 * s, y - 110 * s, x + 80 * s, y - 60 * s], fill=col)
    d.polygon([(x + 34 * s, y - 104 * s), (x + 46 * s, y - 128 * s), (x + 56 * s, y - 102 * s)], fill=col)
    for lx in (-48, -24, 20, 40): d.line([x + lx * s, y - 34 * s, x + lx * s, y], fill=col, width=int(10 * s))
    a = math.sin(t * 12) * .5; d.line([x - 60 * s, y - 60 * s, x - 60 * s - 40 * s * math.cos(a), y - 90 * s + 20 * math.sin(a) * s], fill=col, width=int(8 * s))

def loaf(d, x, y, s=1.0):
    d.pieslice([x - 80 * s, y - 60 * s, x + 80 * s, y + 40 * s], 180, 360, fill=SIG); d.rectangle([x - 80 * s, y - 10 * s, x + 80 * s, y + 10 * s], fill=SIG)
    for i in range(3): d.line([x - 40 * s + i * 40 * s, y - 40 * s, x - 20 * s + i * 40 * s, y - 20 * s], fill=WHITE, width=int(6 * s))

def chef_hat(d, h, s=1.0):
    for dx in (-30, 0, 30): d.ellipse([h[0] + dx * s - 28 * s, h[1] - 100 * s, h[0] + dx * s + 28 * s, h[1] - 44 * s], fill=WHITE, outline=INK, width=int(4 * s))
    d.rectangle([h[0] - 40 * s, h[1] - 64 * s, h[0] + 40 * s, h[1] - 36 * s], fill=WHITE, outline=INK, width=int(4 * s))

def sc_hook(img, d, t):
    d.text((X0 - 6, 300), "HIS NAME?", font=F(BLK, 170), fill=INK)
    picto(d, 680, FLOOR, 1.0, SIG, f=-1, pose=TALK(t))
    dog(d, 820, FLOOR, .9, INK, t)
    items = [("FACE", cue("hook", "face")), ("JOB", cue("hook", "job")), ("DOG", cue("hook", "dog"))]
    for i, (lab, tk) in enumerate(items):
        k = ease((t - tk + .1) / .3)
        if k > 0: box_label(d, X0 + 10, 540 + i * 90, lab, 44, WHITE, INK); d.text((X0 + 200, 568 + i * 90), "remembered", font=F(COND, 28), fill=INK, anchor="lm") if k > .9 else None
    if t >= cue("hook", "not their name"):
        box_label(d, X0 + 10, 810, "NAME", 44, WHITE, SIG); d.text((X0 + 200, 838), "???", font=F(BLK, 44), fill=SIG, anchor="lm")
    fig(d, "fig. 1 — what sticks")

def id_card(d, x, y, line1, line2, k, col):
    if k <= 0: return
    e = ease(k); yy = y + (1 - e) * 60
    d.rectangle([x, yy, x + 400, yy + 470], fill=WHITE, outline=INK, width=5)
    d.rectangle([x + 30, yy + 30, x + 370, yy + 280], fill=RULE)
    picto(d, x + 200, yy + 280, .55, col, pose=IDLE)
    d.text((x + 30, yy + 310), line1, font=F(COND, 34), fill=INK)
    d.text((x + 30, yy + 360), line2, font=F(BLK, 56), fill=col)

def sc_study(img, d, t):
    t0 = S("study")
    d.text((X0, 320), "SAME FACE", font=F(BLK, 110), fill=INK)
    id_card(d, X0, 480, "this man is a", "baker.", (t - cue("study", "this man") + .1) / .4, INK)
    id_card(d, X0 + 440, 480, "his name is", "Baker.", (t - cue("study", "his name") + .1) / .4, SIG)
    fig(d, "McWeeny, Young, Hay & Ellis, 1987")

def sc_result(img, d, t):
    t0 = S("result")
    d.text((X0, 320), "REMEMBERED", font=F(BLK, 110), fill=INK)
    d.text((X0, 440), "same word, two meanings", font=F(COND, 34), fill=INK)
    hbar(d, 560, .85, (t - cue("result", "job") + .2) / .5, INK, "baker — the job", h=100)
    hbar(d, 760, .35, (t - cue("result", "name") + .2) / .5, SIG, "Baker — the name", h=100)
    d.text((X1, 1146), "schematic", font=F(MED, 22), fill=MID, anchor="ra")

def sc_name(img, d, t):
    words_in(d, t, [("BAKER", cue("name", "baker") - .1, 320, 200, SIG), ("baker", cue("name", "baker baker") + .2, 520, 200, INK),
                    ("PARADOX.", cue("name", "paradox") - .1, 760, 150, INK)])

def sc_why(img, d, t):
    t0 = S("why"); nb = cue("why", "a name like")
    cx, cy = 330, 760
    d.text((X0, 320), "HOOKS", font=F(BLK, 130), fill=INK)
    for i, (lab, a, tk) in enumerate((("bread", -150, cue("why", "bread")), ("flour", -90, cue("why", "flour")), ("ovens", -30, cue("why", "ovens")),
                                      ("aprons", 150, cue("why", "ovens") + .2), ("early mornings", 100, cue("why", "ovens") + .4))):
        k = ease((t - tk + .1) / .3)
        if k <= 0: continue
        r = 250 * k; x, y = cx + math.cos(math.radians(a)) * r, cy + math.sin(math.radians(a)) * r * .85
        d.line([cx, cy + 10, x, y], fill=INK, width=4); box_label(d, x, y - 18, lab, 30, INK, WHITE, anchor="ma")
    box_label(d, cx, cy - 20, "baker", 48, WHITE, INK, anchor="ma")
    if t >= nb - .1:
        k = ease((t - nb + .1) / .3)
        box_label(d, 720, 880, "Baker", 44, WHITE, SIG, anchor="ma")
        if t >= cue("why", "nothing"): note(d, 720, 950, 760, 1060, "no links", 1, SIG, size=26)
    fig(d, "fig. 2 — meaning gives memory something to hold")

def sc_tip(img, d, t):
    t0 = S("tip"); pc = cue("tip", "picture")
    d.text((X0, 320), "GIVE IT A HOOK", font=F(BLK, 96), fill=INK)
    h = picto(d, 600, FLOOR, 1.0, SIG, f=-1, pose={"arms": ((80, 60), (-10, -5))})
    if t >= pc - .1: chef_hat(d, h, 1.0)
    if t >= cue("tip", "loaf") - .2: loaf(d, 470, 900, .9 * ease((t - cue("tip", "loaf") + .2) / .3))
    box_label(d, 600, 1000, "MR. BAKER", 34, WHITE, INK, anchor="ma")
    if t >= cue("tip", "loaf"): note(d, 470, 860, 260, 640, "now it sticks", (t - cue("tip", "loaf") - .2) / .4, SIG, anchor="ra", size=28)
    fig(d, "fig. 3 — a mnemonic for names")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "name": sc_name, "why": sc_why, "tip": sc_tip}
FX = [(0.0, thud(.5), 0), *[(cue("hook", w) - .1, pop(.15), -.2) for w in ("face", "job", "dog")], (cue("hook", "not their name"), thud(.4), 0),
      *EP.cut_fx(), (cue("study", "this man"), pop(.18), -.2), (cue("study", "his name"), pop(.18), .2),
      (S("result") + .05, thud(.55), 0), (cue("name", "baker") - .1, thud(.4), 0), (cue("name", "paradox"), thud(.4), 0),
      *[(cue("why", w), pop(.13), (i - 1) / 2) for i, w in enumerate(("bread", "flour", "ovens"))], (cue("why", "nothing"), rewind_sfx(.1, .3), .3),
      (cue("tip", "picture"), pop(.2), .2), (cue("tip", "loaf"), riser(.4, .07), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
