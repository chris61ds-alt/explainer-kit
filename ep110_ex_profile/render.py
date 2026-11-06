"""NOT JUST YOU – No. 110: checking your ex's profile – 88 % admit it (Lukacs & Quan-Haase 2015); more checking went with
more longing and distress, less growth, while staying friends did not (Marshall 2012, 464 people, correlational).
Look C+D · statement opener with "you" · isometric phone (the ex's profile, refresh count) that ends face-down · orange reveal."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from tips import phone as _iso_phone
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"study": .6, "longing": .5, "friends": .5, "twist": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["study", "longing", "friends", "twist", "point", "end"]
EP = ThreadEpisode(TL, 110, "EX PROFILE", order=ORDER, dark=True, label="SURVEY · 464 PEOPLE · CORRELATION",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Lukacs & Quan-Haase (2015), Inform., Comm. & Society ·", "Marshall (2012), Cyberpsych., Behav. & Soc. Netw. 15(10)"),
                   music=dict(bpm=92, root=-3, prog="tense", kick="half", audio="v5", gaps=[(E("study") + .05, S("longing") + .05)]),
                   cover=dict(words=["YOU STILL", "CHECK YOUR", "EX'S PROFILE."], kicker="88 % admit it. Here's the price."))

def sc_study(img, d, t):
    t0, tf = S("study"), cue("study", "how often") - .1
    counter(d, X0, 320, t, t0 + .1, .8, 464, "{:.0f}", 230, INK)
    d.text((X0 + 6, 565), "people after a breakup", font=F(COND, 46), fill=INK)
    if t >= tf:                                            # the scale they answered on
        d.text((X0, 680), "HOW OFTEN DID YOU CHECK?", font=F(BLK, 46), fill=INK)
        labs = ["NEVER", "", "", "", "", "", "", "", "SEVERAL A DAY"]
        for i in range(9):
            k = back(clamp((t - tf - i * .06) / .25)); x = X0 + 40 + i * 98; r = 34 * k
            d.ellipse([x - r, 820 - r, x + r, 820 + r], fill=INK if i == 6 else MID)
        d.text((X0, 880), "NEVER", font=F(MONO, 26), fill=MID); d.text((X1, 880), "SEVERAL A DAY", font=F(MONO, 26), fill=MID, anchor="ra")
        if t >= tf + .7: d.text((X0, 960), "on Facebook", font=F(COND, 44), fill=MID)
    fig(d, "self-report, 1–9 scale")

IP = Iso(480, 1000, .95)
def sc_longing(img, d, t):
    t0, td, tg = S("longing"), cue("longing", "More distress") - .1, cue("longing", "Less personal") - .1
    d.text((X0, 320), "MORE CHECKING,", font=F(BLK, 105), fill=INK)
    IP.grid(img); IP.shadow(d, 0, 0, 230)
    n = int(clamp((t - t0 - .2) / 1.4) * 7)                # refresh after refresh
    A = _iso_phone(IP, d, t, msgs=[("l", t0 + .1 + i * .2, MID) for i in range(min(4, n + 1))])
    p = IP.P(*A["screen"])
    if n: d.text((p[0] + 150, p[1] - 150), f"×{n}", font=F(BLK, 90), fill=INK, anchor="mm")
    rows = [("MORE LONGING", t0 + .3), ("MORE DISTRESS", td), ("LESS GROWTH", tg)]
    for j, (lab, tk) in enumerate(rows):
        if t >= tk: box_label(d, X0 + 4 - (1 - ease((t - tk) / .2)) * 40, 450 + j * 75, lab, 44, WHITE, INK, font=BLK)
    fig(d, "a link, not proof")

def friends_card(d, t, t0, unfr_k):
    """the friend button: 'FRIENDS ✓' that a finger hovers over"""
    x, y, w, h = X0 + 40, 760, 480, 130
    d.rounded_rectangle([x, y, x + w, y + h], radius=26, fill=INK)
    d.text((x + w / 2, y + h / 2), "FRIENDS", font=F(BLK, 60), fill=BG, anchor="mm")
    if unfr_k > 0:
        k = ease(unfr_k); cx, cy = x + w + 90, y + h / 2 + 30 * (1 - k)
        d.ellipse([cx - 44, cy - 44, cx + 44, cy + 44], outline=MID, width=10)
        d.text((cx, cy), "?", font=F(BLK, 60), fill=MID, anchor="mm")

def sc_friends(img, d, t):
    t0 = S("friends")
    words_in(d, t, [("SHOULD YOU", t0 + .05, 320, 140, INK), ("UNFRIEND?", t0 + .2, 470, 140, INK)])
    friends_card(d, t, t0, clamp((t - t0 - .4) / .4))
    fig(d, "schematic")

def sc_twist(img, d, t):
    t0, tc = S("twist"), cue("twist", "The checking was") - .15
    words_in(d, t, [("STAYING FRIENDS:", t0 + .05, 320, 110, INK), ("NOT THE PROBLEM.", t0 + .2, 430, 110, INK)])
    friends_card(d, t, t0, 0)
    if t >= tc: words_in(d, t, [("THE CHECKING", tc, 960, 120, SIG), ("WAS.", tc + .12, 1080, 120, SIG)])
    fig(d, "friends: fewer negative feelings · a link, not proof")

def sc_point(img, d, t):
    t0, tp = S("point"), cue("point", "put the phone down") - .25
    IP.grid(img); IP.shadow(d, 0, 0, 230)
    if t < tp: A = _iso_phone(IP, d, t, msgs=[("l", t0 + .1, MID), ("l", t0 + .2, MID)])
    else:                                                  # face-down: back of the phone, screen hidden
        k = ease((t - tp) / .3); dz = 60 * (1 - k)
        IP.box(d, -90, -170, dz, 180, 340, 18)
        iso_quad(IP, d, -30, -120, 30, -60, 18 + dz, MID)  # camera bump
        A = {"phone": (60, 120, 18)}
    words_in(d, t, [("KEEP THE", t0 + .05, 320, 120, MID), ("FRIEND LIST.", t0 + .2, 440, 120, MID)] +
             ([("PUT IT DOWN.", tp, 580, 130, SIG)] if t >= tp else []))
    if t >= tp + .3: p = IP.P(60, 120, 18); callout(d, p, "r", p[1] + 60, 1, "FACE DOWN", SIG, k=(t - tp - .3) / .4)
    fig(d, "fig. 2 — schematic")

EP.cuts = {"twist": "stay"}
EP.bg = {"longing": "light", "point": "light"}
EP.scenes = {"study": sc_study, "longing": sc_longing, "friends": sc_friends, "twist": sc_twist, "point": sc_point}
FX = [*EP.cut_fx(), (S("study") + .1, riser(.8, .04), 0), *[(cue("study", "how often") - .1 + i * .06, tick(.035), (i - 4) / 5) for i in range(9)],
      *[(S("longing") + .2 + i * .2, tick(.05), (i % 3 - 1) / 2) for i in range(7)], (S("longing") + .3, pop(.13), -.3),
      (cue("longing", "More distress") - .1, pop(.13), -.3), (cue("longing", "Less personal") - .1, thud(.45), 0),
      (S("friends") + .1, thud(.4), 0), (S("friends") + .4, pop(.13), .3),
      (S("twist") + .1, thud(.5), 0), (cue("twist", "The checking was") - .15, thud(.55), 0),
      (S("point") + .1, pop(.12), 0), (cue("point", "put the phone down") - .25, thud(.5), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
