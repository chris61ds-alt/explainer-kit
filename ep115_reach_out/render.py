"""NOT JUST YOU – No. 115: reaching out – people underestimate how much a 'just because' note is appreciated, more so when it's
a surprise (Liu, Rim, Min & Min 2022, JPSP, 5,900+ participants). Look C+D · statement opener with "you" ·
isometric phone: a message goes out · orange reveal: loved it more than expected."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from tips import phone as _iso_phone
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"study": .6, "guess": .5, "result": .6, "surprise": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["study", "guess", "result", "surprise", "point", "end"]
EP = ThreadEpisode(TL, 115, "REACH OUT", order=ORDER, dark=True, label="EXPERIMENTS · 5,900+ PEOPLE",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Liu, Rim, Min & Min (2022), The surprise of reaching out,", "J. of Personality and Social Psychology"),
                   music=dict(bpm=100, root=2, prog="major", kick="four", audio="v5", gaps=[(E("study") + .05, S("guess") + .05)]),
                   cover=dict(words=["YOU LOST TOUCH", "WITH A", "FRIEND."], kicker="Text them. It means more than you think."))

IP = Iso(480, 1000, .95)
def sc_study(img, d, t):
    t0, tn = S("study"), cue("study", "a short note") - .1
    d.text((X0, 320), "A SHORT NOTE", font=F(BLK, 120), fill=INK); d.text((X0 + 4, 450), "to someone from the past", font=F(COND, 50), fill=MID)
    IP.grid(img); IP.shadow(d, 0, 0, 230)
    _iso_phone(IP, d, t, msgs=[("r", tn, INK)] if t >= tn else [])
    if t >= tn + .5: p = IP.P(40, -130, 20); callout(d, p, "r", p[1] - 80, 1, "\"HEY, THOUGHT OF YOU\"", INK, k=(t - tn - .5) / .4)
    fig(d, "fig. 1 — schematic")

def meter(d, y, lab, v, col, k):
    d.text((X0, y), lab, font=F(BLK, 48), fill=col)
    w = 760 * v * ease(clamp(k)); d.rectangle([X0, y + 66, X0 + 760, y + 150], outline=RULE, width=4)
    d.rectangle([X0, y + 66, X0 + max(6, w), y + 150], fill=col)

def sc_guess(img, d, t):
    t0 = S("guess")
    d.text((X0, 320), "HOW MUCH", font=F(BLK, 120), fill=INK); d.text((X0, 440), "WILL THEY LIKE IT?", font=F(BLK, 80), fill=INK)
    meter(d, 600, "SENDERS GUESSED", .52, MID, (t - t0 - .2) / .6)
    fig(d, "appreciation · schematic")

def sc_result(img, d, t):
    t0 = S("result")
    d.text((X0, 320), "HOW MUCH", font=F(BLK, 120), fill=INK); d.text((X0, 440), "WILL THEY LIKE IT?", font=F(BLK, 80), fill=INK)
    meter(d, 600, "SENDERS GUESSED", .52, MID, 1)
    meter(d, 820, "FRIENDS FELT", .82, SIG, (t - t0 - .1) / .6)
    fig(d, "appreciation · schematic, direction only")

def sc_surprise(img, d, t):
    t0, tb = S("surprise"), cue("surprise", "the bigger the gap") - .15
    words_in(d, t, [("MORE OUT", t0 + .05, 320, 150, INK), ("OF THE BLUE", t0 + .2, 470, 150, INK)])
    if t >= tb: words_in(d, t, [("= BIGGER GAP.", tb, 650, 130, INK)])
    for i in range(5):                                       # a surprise burst
        if t >= t0 + .4 + i * .08:
            a = i * 1.26; r = 60 + 30 * ease(clamp((t - t0 - .4 - i * .08) / .3))
            cx, cy = X1 - 160, 900; d.line([cx + 30 * math.cos(a), cy + 30 * math.sin(a), cx + r * math.cos(a), cy + r * math.sin(a)], fill=MID, width=10)
    fig(d, "weaker ties too")

def sc_point(img, d, t):
    t0, tn = S("point"), cue("point", "Right now") - .15
    IP.grid(img); IP.shadow(d, 0, 0, 230)
    A = _iso_phone(IP, d, t, msgs=[("l", t0 - 1, MID), ("r", tn, SIG)] if t >= tn else [("l", t0 - 1, MID)])
    words_in(d, t, [("SEND THE", t0 + .05, 320, 150, MID), ("TEXT.", t0 + .2, 470, 150, MID)] + ([("RIGHT NOW.", tn, 620, 130, SIG)] if t >= tn else []))
    if t >= tn + .3: p = IP.P(40, -70, 20); callout(d, p, "r", p[1] - 40, 1, "SENT", SIG, k=(t - tn - .3) / .4)
    fig(d, "fig. 2 — schematic")

EP.cuts = {"result": "stay"}
EP.bg = {"study": "light", "point": "light"}
EP.scenes = {"study": sc_study, "guess": sc_guess, "result": sc_result, "surprise": sc_surprise, "point": sc_point}
FX = [*EP.cut_fx(), (S("study") + .1, riser(.8, .04), 0), (cue("study", "a short note") - .1, pop(.14), .2), (cue("study", "a short note") + .4, tick(.05), .3),
      (S("guess") + .2, whoosh(.6, .04), -.2), (S("result") + .1, thud(.55), 0), (S("result") + .7, pop(.15), .3),
      *[(S("surprise") + .4 + i * .08, pop(.08), .4) for i in range(5)], (cue("surprise", "the bigger the gap") - .15, thud(.45), 0),
      (S("point") + .1, pop(.12), 0), (cue("point", "Right now") - .15, whoosh(.25, .05), .3), (cue("point", "Right now"), thud(.5), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
