"""NOT JUST YOU – No. 88: your followers are more popular than you – the friendship paradox (Hodas, Kooti & Lerman 2013). Look C+D, dark."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from thread import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .6, "result": .5, "active": .5, "why": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "active", "why", "point", "end"]
EP = ThreadEpisode(TL, 88, "FOLLOWER MATH", order=ORDER, dark=True, label="PLATFORM DATA · TWITTER 2009",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Hodas, Kooti & Lerman (2013), Friendship", "Paradox Redux, ICWSM · 5.8 M Twitter users"),
                   music=dict(bpm=100, root=0, prog="dream", kick="four", audio="v5", gaps=[(E("study") + .05, S("result") + .05)]),
                   cover=dict(words=["YOUR FOLLOWERS:", "10 × MORE", "POPULAR."], kicker="It's math, not you."))

def sc_hook(img, d, t):
    tp = cue("hook", "They are more") - .15
    d.text((X0 - 4, 320), "FEELS PERSONAL?", font=F(BLK, 105), fill=MID)
    d.text((X0 - 4, 450), "IT ISN'T.", font=F(BLK, 130), fill=INK)
    for i, (x, y, s) in enumerate(((190, 860, .32), (770, 860, .32), (300, 1010, .26), (660, 1010, .26))):
        silhouette(img, lambda m, x=x, y=y, s=s: front_bust(m, x, y, s, 255), (int(x - 160 * s / .32), int(y - 110 * s / .32), int(x + 160 * s / .32), int(y + 160 * s / .32)), MID, cell=7)
    silhouette(img, lambda m: front_bust(m, 480, 920, .2, 255), (400, 860, 560, 1050), INK, cell=6)
    d.text((480, 1062), "YOU", font=F(BLK, 30), fill=INK, anchor="ma")
    if t >= tp: d.text((X0 - 4 - (1 - ease((t - tp) / .3)) * 60, 600), "THEY ARE.", font=F(BLK, 120), fill=mix(BG, SIG, ease((t - tp) / .3)))
    fig(d, "fig. 1 — your feed, schematic")

def sc_study(img, d, t):
    t0, tw = S("study"), cue("study", "four hundred") - .2
    counter(d, X0, 320, t, t0 + .1, .8, 5.8, "{:.1f} M", 230, INK)
    d.text((X0 + 6, 570), "Twitter users, second half of 2009", font=F(COND, 42), fill=INK)
    if t >= tw:
        counter(d, X0, 660, t, tw, .7, 476, "{:.0f} M", 120, MID)
        d.text((X0 + 6, 800), "tweets", font=F(COND, 42), fill=MID)
    dot_field(d, (X0 + 14, 900, X1, 1110), t, cell=26, col=RULE)
    fig(d, "who follows whom, and how active everyone is")

def sc_result(img, d, t):
    t0, tb = S("result"), S("result") + .4
    d.text((X0, 320), "YOUR FOLLOWERS:", font=F(BLK, 96), fill=INK)
    counter(d, X0, 430, t, tb, .7, 10, "{:.0f} ×", 220, SIG)
    d.text((X0 + 440, 495), "more", font=F(BLK, 56), fill=INK); d.text((X0 + 440, 560), "followers", font=F(BLK, 56), fill=INK); d.text((X0 + 440, 625), "than you", font=F(BLK, 56), fill=INK)
    k = ease((t - tb) / .7); base = 1090
    d.rectangle([X0 + 60, base - 36, X0 + 220, base], fill=MID); d.text((X0 + 140, base - 48), "YOU", font=F(BLK, 34), fill=MID, anchor="md")
    h = 360 * k; d.rectangle([X0 + 380, base - max(36, h), X0 + 540, base], fill=SIG)
    d.text((X0 + 460, base - max(36, h) - 12), "A FOLLOWER", font=F(BLK, 34), fill=SIG, anchor="md")
    fig(d, "typical ratio, by follower count")

def grid(d, n, k, col, y0=640):
    for i in range(100):
        r, c = divmod(i, 10); x = X0 + c * 86; y = y0 + r * 44
        on = i < n * k
        d.rectangle([x, y, x + 74, y + 34], fill=col if on else None, outline=col if on else MID, width=2)

def sc_active(img, d, t):
    t0 = S("active")
    counter(d, X0, 320, t, t0 + .1, .8, 88, "{:.0f} %", 230, SIG)
    d.text((X0 + 6, 570), "post less than the people they follow", font=F(COND, 44), fill=INK)
    grid(d, 88, clamp((t - t0 - .2) / 1.0), SIG)
    fig(d, "share of users · 99 % if inactive accounts are left out")

HUB = (480, 860)
LEAVES = [(HUB[0] + 300 * math.cos(a), HUB[1] + 240 * math.sin(a)) for a in [i * 2 * math.pi / 11 - math.pi / 2 for i in range(11)]]
YOU = LEAVES[7]

def sc_why(img, d, t):
    t0, tm = S("why"), cue("why", "Including yours") - .2
    tm0 = cue("why", "it's math") - .1
    if t >= tm0: d.text((X0 - (1 - ease((t - tm0) / .25)) * 50, 320), "IT'S MATH.", font=F(BLK, 150), fill=mix(BG, INK, ease((t - tm0) / .25)))
    d.text((X0 + 4, 490), "popular accounts are in everyone's network", font=F(COND, 40), fill=INK)
    k = clamp((t - t0 - .4) / 1.0)
    for i, (x, y) in enumerate(LEAVES):
        if i / len(LEAVES) > k: continue
        d.line([HUB, (x, y)], fill=MID, width=3)
        tt_ = cue("why", "tons of people") - .1; lit = t >= tt_ and (x, y) != YOU
        r = 16 + (4 if lit else 0); d.ellipse([x - r, y - r, x + r, y + r], fill=(INK if lit else MID) if (x, y) != YOU else (SIG if t >= tm else INK))
    d.ellipse([HUB[0] - 64, HUB[1] - 64, HUB[0] + 64, HUB[1] + 64], fill=INK)
    ts = cue("why", "So they show up") - .1
    if t >= ts:
        r = 64 + 60 * ease((t - ts) / .5); a = 1 - clamp((t - ts) / .8)
        if a > 0: d.ellipse([HUB[0] - r, HUB[1] - r, HUB[0] + r, HUB[1] + r], outline=mix(BG, INK, a), width=6)
    d.text((HUB[0], HUB[1]), "POPULAR", font=F(BLK, 24), fill=BG, anchor="mm")
    d.text((YOU[0] - 26, YOU[1]), "YOU", font=F(BLK, 30), fill=SIG if t >= tm else INK, anchor="rm")
    fig(d, "friendship paradox (Feld 1991) · schematic")

def sc_point(img, d, t):
    t0, tf = S("point"), cue("point", "Your feed") - .2
    words_in(d, t, [("NOT", t0 + .1, 320, 150, MID), ("BORING.", t0 + .3, 470, 170, INK)] +
             ([("YOUR FEED:", tf, 680, 110, INK), ("THE POPULAR", tf + .2, 800, 110, SIG), ("KIDS.", tf + .35, 915, 110, SIG)] if t >= tf else []))
    fig(d, "fig. 2 — followers typically 10 × more popular")

# magic move: one of the 88 % squares becomes "you" in the network diagram
_gx, _gy = X0 + 7 * 86, 640 + 4 * 44
EP.carry = {"why": [((_gx, _gy, _gx + 74, _gy + 34), (YOU[0] - 16, YOU[1] - 16, YOU[0] + 16, YOU[1] + 16))]}

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "active": sc_active, "why": sc_why, "point": sc_point}
FX = [(0.0, thud(.5), 0), (cue("hook", "They are more") - .15, pop(.15), .3), *EP.cut_fx(), (S("study") + .1, riser(.8, .04), 0),
      (cue("study", "four hundred") - .2, pop(.12), .2), (S("result") + .4, thud(.5), 0), (S("active") + .1, thud(.45), 0),
      *[(S("active") + .25 + i * .09, tick(.03), (i % 5 - 2) / 3) for i in range(11)],
      *[(S("why") + .4 + i / 11, tick(.035), (i % 5 - 2) / 3) for i in range(11)], (cue("why", "So they show up") - .1, pop(.14), 0), (cue("why", "it's math") - .1, thud(.4), 0), (cue("why", "tons of people") - .1, pop(.13), 0),
      (cue("why", "Including yours") - .2, pop(.15), .3), (cue("point", "Your feed") - .2, thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
