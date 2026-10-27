"""NOT JUST YOU – No. 39: lying in everyday life (DePaulo et al. 1996). Series: Swiss Dark (edgy)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .8, "result": .5, "often": .5, "what": .5, "self": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "often", "what", "self", "point", "end"]
EP = Episode(TL, 39, "YOU LIED TODAY", order=ORDER, dark=True,
             chapters={"hook": "GUILTY", "study": "THE DIARY", "result": "PER DAY", "often": "PER CONVERSATION", "what": "THE CLASSICS", "self": "FOR WHOM", "point": "I'M FINE"},
             sources=("DePaulo, Kashy, Kirkendol, Wyer & Epstein (1996),", "J. Personality & Social Psychology 70(5)"),
             music=dict(bpm=96, root=-1, prog="minor", kick="four", gaps=[(E("study") + .05, S("result") + .05)]),
             cover=dict(words=["YOU LIED", "TODAY."], kicker="Probably more than once."))

def nose(d, h, s, L):
    d.polygon([(h[0] + 38 * s, h[1] - 6 * s), (h[0] + 38 * s + L, h[1] + 2 * s), (h[0] + 38 * s, h[1] + 10 * s)], fill=SIG)

def sc_hook(img, d, t):
    d.text((X0 - 6, 300), "YOU LIED", font=F(BLK, 180), fill=INK)
    d.text((X0, 480), "today.", font=F(BLK, 110), fill=SIG)
    h = picto(d, 380, FLOOR, 1.05, INK, f=1, pose=SHRUG)
    nose(d, h, 1.05, 20 + 120 * ease((t - cue("hook", "probably")) / .8))
    fig(d, "fig. 1 — be honest")

def diary(d, x, y, w, h, t, t0):
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=INK, width=5); d.line([x + w / 2, y, x + w / 2, y + h], fill=INK, width=4)
    days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    for i, dn in enumerate(days):
        col_x = x + 30 + (0 if i < 4 else w / 2); yy = y + 30 + (i % 4) * (h - 40) / 4
        d.text((col_x, yy), dn, font=F(COND, 26), fill=MID)
        n = (i * 3 + 1) % 3 + 1
        for j in range(n):
            if t > t0 + .4 + i * .3 + j * .1: d.line([col_x + 80 + j * 30, yy + 4, col_x + 80 + j * 30, yy + 34], fill=SIG, width=6)

def sc_study(img, d, t):
    t0 = S("study")
    d.text((X0, 300), "THE DIARY", font=F(BLK, 130), fill=INK)
    diary(d, X0, 480, X1 - X0, 520, t, t0)
    fig(d, "one week, every lie written down · DePaulo et al., 1996")

def sc_result(img, d, t):
    t0 = S("result")
    d.text((X0, 300), "PER DAY", font=F(BLK, 130), fill=INK)
    for i, (lab, n, tk) in enumerate((("college students", 2, cue("result", "twice")), ("other adults", 1, cue("result", "about once")))):
        k = ease((t - tk + .2) / .4); y = 520 + i * 270
        if k <= 0: continue
        d.text((X0, y), lab, font=F(COND, 34), fill=INK)
        counter(d, X0, y + 50, t, tk - .2, .5, n, "≈ {:.0f}", 140, SIG if i == 0 else INK)
        for j in range(n):
            h = picto(d, X0 + 430 + j * 170, y + 240, .5, SIG if i == 0 else INK, pose=TALK(t, j)); nose(d, h, .5, 50)
    fig(d, "1.96 vs. 0.97 lies a day, on average")

def sc_often(img, d, t):
    t0 = S("often"); fv = cue("often", "one in five")
    d.text((X0, 300), "CONVERSATIONS", font=F(BLK, 110), fill=INK)
    for row, (n, lab, tk) in enumerate(((3, "students: 1 in 3", t0 + .2), (5, "everyone else: 1 in 5", fv - .2))):
        k = ease((t - tk) / .4)
        if k <= 0: continue
        y = 500 + row * 290
        d.text((X0, y), lab, font=F(COND, 34), fill=INK)
        for i in range(n):
            x = X0 + i * (840 / n); w = 840 / n - 20
            d.rectangle([x, y + 60, x + w, y + 200], outline=INK, width=4, fill=SIG if i == 0 else None)
            d.text((x + w / 2, y + 130), "💬".replace("💬", "· · ·"), font=F(BLK, 34), fill=WHITE if i == 0 else MID, anchor="mm")
    fig(d, "share of social interactions with at least one lie")

def sc_what(img, d, t):
    t0 = S("what")
    d.text((X0, 300), "THE CLASSICS", font=F(BLK, 120), fill=INK)
    for i, (txt, tk) in enumerate((("“I love it.”", cue("what", "love it")), ("“I'm fine.”", cue("what", "fine")), ("“Great idea.”", cue("what", "great idea")))):
        k = ease((t - tk + .1) / .3)
        if k > 0: speech_box(d, X0 + 20 + (i % 2) * 300, 500 + i * 170, 420, k, SIG if i == 1 else INK, 1, txt.strip("“”"), 36)
    fig(d, "most common: lies about feelings")

def sc_self(img, d, t):
    t0 = S("self")
    d.text((X0, 300), "FOR WHOM?", font=F(BLK, 130), fill=INK)
    hbar(d, 540, .66, (t - cue("self", "protected the liar") + .2) / .5, SIG, "to protect yourself", h=100)
    hbar(d, 740, .33, (t - cue("self", "someone else") + .2) / .5, INK, "to protect someone else", h=100)
    if t >= cue("self", "someone else") + .3: dim_h(d, X0 + 840 * .33, X0 + 840 * .66, 900, (t - cue("self", "someone else") - .3) / .4, SIG, "×2", 30)
    fig(d, "self-centered vs. kind lies · about 2 to 1")

def sc_point(img, d, t):
    t0 = S("point")
    words_in(d, t, [("“I'M FINE.”", t0 + .1, 300, 160, SIG)])
    for i, x in enumerate((180, 400, 620, 820)):
        h = picto(d, x, FLOOR, .7, INK if i != 1 else SIG, f=1 if i % 2 else -1, pose=SHRUG if i % 2 else IDLE); nose(d, h, .7, 40 + 10 * math.sin(t * 3 + i))
    if t >= cue("point", "good company"): box_label(d, 480, 600, "GOOD COMPANY", 36, WHITE, INK, anchor="ma")
    fig(d, "fig. 2 — everyone, basically")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "often": sc_often, "what": sc_what, "self": sc_self, "point": sc_point}
FX = [(0.0, thud(.5), 0), (cue("hook", "probably"), riser(.6, .06), .2), *EP.cut_fx(),
      *[(S("study") + .4 + i * .3, tick(.06), (i % 3 - 1) * .4) for i in range(7)], (S("result") + .05, thud(.5), 0),
      (cue("result", "about once"), pop(.15), 0), (cue("often", "one in five"), pop(.15), 0),
      *[(cue("what", w), pop(.18), (i - 1) / 2) for i, w in enumerate(("love it", "fine", "great idea"))],
      (cue("self", "someone else") + .3, thud(.4), 0), (cue("point", "good company"), riser(.4, .06), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
