"""NOT JUST YOU – No. 26: the pain of paying (Prelec & Simester 2001). Area: money."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .8, "result": .6, "name": .6, "tip": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "name", "tip", "end"]
EP = Episode(TL, 26, "TAP TO PAY", order=ORDER,
             chapters={"hook": "TAP", "study": "THE AUCTION", "result": "THE RESULT", "name": "THE PAIN", "tip": "THE FIX"},
             sources=("Prelec & Simester (2001), Marketing Letters 12(1)", "via Psychology Today"),
             music=dict(bpm=104, root=-2, prog="minor", kick="four", gaps=[(E("study") + .05, S("result") + .05)]),
             cover=dict(words=["TAP", "TO PAY."], kicker="Why cards make you spend more."))

def terminal(d, x, y, s=1.0, ok=0.0):
    d.rounded_rectangle([x - 90 * s, y - 150 * s, x + 90 * s, y + 150 * s], radius=20 * s, fill=INK)
    d.rectangle([x - 66 * s, y - 120 * s, x + 66 * s, y - 20 * s], fill=SIG if ok > .5 else MID)
    if ok > .5: d.text((x, y - 70 * s), "OK", font=F(BLK, int(50 * s)), fill=WHITE, anchor="mm")
    for r in range(3):
        for c in range(3): d.rectangle([x - 60 * s + c * 44 * s, y + 10 * s + r * 40 * s, x - 30 * s + c * 44 * s, y + 36 * s + r * 40 * s], fill=MID)

def ball(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SIG); d.line([cx - r, cy, cx + r, cy], fill=INK, width=4); d.line([cx, cy - r, cx, cy + r], fill=INK, width=4)
    d.arc([cx - r * 1.4, cy - r, cx - r * .2, cy + r], -60, 60, fill=INK, width=4); d.arc([cx + r * .2, cy - r, cx + r * 1.4, cy + r], 120, 240, fill=INK, width=4)

def sc_hook(img, d, t):
    nt = cue("hook", "nothing")
    d.text((X0 - 6, 300), "TAP." if t < nt else "…NOTHING?", font=F(BLK, 200 if t < nt else 150), fill=INK)
    x = move(t, [(0, 330), (.4, 540)], .5)
    terminal(d, 640, 820, 1.1, 1.0 if t > 1.0 else 0)
    credit_card(d, x, 900, .9, INK)
    picto(d, 200, FLOOR, .8, INK, pose=IDLE)
    if t >= nt: note(d, 640, 700, 860, 540, "didn't even feel it", (t - nt) / .35, SIG, anchor="ra", size=28)
    fig(d, "fig. 1 — a payment you don't notice")

def sc_study(img, d, t):
    t0 = S("study"); ca = cue("study", "cash"); cd = cue("study", "by card")
    d.text((X0, 320), "SOLD OUT", font=F(BLK, 130), fill=INK)
    ball(d, 760, 380, 60)
    d.rectangle([X0, 500, X1, 620], outline=INK, width=4); d.text((X0 + 30, 560), "TICKETS · BIDDING", font=F(COND, 40), fill=INK, anchor="lm")
    for i, (lab, tk, draw) in enumerate((("CASH", ca, lambda: banknote(d, X0 + 210, 820, 1.1, "$")), ("CARD", cd, lambda: credit_card(d, X0 + 630, 820, 1.2, SIG)))):
        k = ease((t - tk + .1) / .3)
        if k > 0: draw(); box_label(d, X0 + 210 + i * 420, 940, lab, 34, WHITE, INK if i == 0 else SIG, anchor="ma")
    fig(d, "Prelec & Simester — Marketing Letters, 2001")

def sc_result(img, d, t):
    t0 = S("result"); tw = cue("result", "twice")
    d.text((X0, 320), "WILLING TO PAY", font=F(BLK, 104), fill=INK)
    hbar(d, 560, .38, (t - t0) / .5, INK, "paying cash", h=110)
    hbar(d, 780, .88, (t - tw + .3) / .6, SIG, "paying by card", h=110)
    if t >= tw + .3: dim_h(d, X0 + 840 * .38, X0 + 840 * .88, 940, (t - tw - .3) / .4, SIG, "MORE THAN ×2", 26)
    d.text((X1, 1146), "schematic", font=F(MED, 22), fill=MID, anchor="ra")

def gauge(d, cx, cy, r, v, label):
    d.arc([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=INK, width=10)
    for i in range(11):
        a = math.radians(180 + i * 18); d.line([cx + math.cos(a) * r * .86, cy + math.sin(a) * r * .86, cx + math.cos(a) * r, cy + math.sin(a) * r], fill=INK, width=3)
    a = math.radians(180 + 180 * v); d.line([cx, cy, cx + math.cos(a) * r * .9, cy + math.sin(a) * r * .9], fill=SIG, width=8)
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=INK); d.text((cx, cy + 30), label, font=F(COND, 30), fill=INK, anchor="ma")

def sc_name(img, d, t):
    t0 = S("name"); ch = cue("name", "cash hurts"); cn = cue("name", "cards numb")
    words_in(d, t, [("PAIN OF", cue("name", "pain") - .1, 300, 150, INK), ("PAYING.", cue("name", "paying") - .1, 450, 150, SIG)])
    if t >= ch - .2:
        gauge(d, 260, 900, 160, .15 + .7 * ease((t - ch + .2) / .5) + .03 * math.sin(t * 20), "cash"); banknote(d, 260, 1060, .6, "$")
    if t >= cn - .2:
        gauge(d, 700, 900, 160, .15 + .05 * ease((t - cn + .2) / .5), "card"); credit_card(d, 700, 1060, .5, SIG)
    fig(d, "pain meter · schematic")

def sc_tip(img, d, t):
    t0 = S("tip"); pc = cue("tip", "pay cash"); cb = cue("tip", "balance")
    words_in(d, t, [("MAKE IT", t0, 300, 150, INK), ("HURT.", t0 + .3, 450, 150, SIG)])
    if t >= pc - .2:
        for i in range(3): banknote(d, 260 + i * 16, 820 - i * 16, .9, "$")
        box_label(d, 280, 940, "PAY CASH", 30, WHITE, INK, anchor="ma")
    if t >= cb - .2:
        phone(d, 700, 820, 1.2, INK, lit=True); d.text((700, 790), "BALANCE", font=F(COND, 22), fill=INK, anchor="mm"); d.text((700, 830), "check", font=F(BLK, 30), fill=SIG, anchor="mm")
        box_label(d, 700, 940, "CHECK FIRST", 30, WHITE, SIG, anchor="ma")
    fig(d, "fig. 2 — bring a little pain back")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "name": sc_name, "tip": sc_tip}
def beep(amp=.08, f=1600, dur=.15):
    t = tt_(dur); return amp * np.sin(2 * np.pi * f * t) * np.exp(-t * 12)
FX = [(0.0, thud(.5), 0), (.9, beep(), .2), (cue("hook", "nothing"), rewind_sfx(.1, .3), 0), *EP.cut_fx(),
      (cue("study", "cash"), pop(.18), -.3), (cue("study", "by card"), pop(.18), .3), (S("result") + .05, thud(.5), 0),
      (cue("result", "twice"), riser(.5, .08), .3), (cue("name", "pain") - .1, thud(.4), 0), (cue("name", "cash hurts"), whoosh(.4, .12), -.3),
      (cue("tip", "pay cash"), pop(.18), -.2), (cue("tip", "balance"), beep(.06, 1200), .3), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
