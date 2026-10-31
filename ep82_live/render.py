"""NOT JUST YOU – No. 82: this video, live – the video narrates its own (typical) retention in real time.
A live timer + a schematic retention curve that draws with playback; 'YOU' rides along at 100 %. Look C+D, dark, hard cuts."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from thread import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, end="card", lead=.15, gaps={"hook": .4, "drop": .5, "glance": .5, "value": .5, "half": .5, "algo": .6, "end": 2.6})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "drop", "glance", "value", "half", "algo", "end"]
EP = ThreadEpisode(TL, 82, "THIS VIDEO, LIVE", order=ORDER, dark=True, label="LIVE · THIS VIDEO", slide=0.0,
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Fors Marsh for Facebook (2016) · Facebook/Nielsen ·", "quso.ai Shorts data · Mosseri, Instagram (2025)"),
                   music=dict(bpm=104, root=0, prog="tense", kick="four"),
                   cover=dict(words=["THIS VIDEO,", "LIVE."], kicker="Watch yourself get counted."))
T_END = E("algo") + .6                       # chart spans the talking part of the video
CX0, CX1, CY0, CY1 = X0 + 40, X1, 600, 860     # chart box (top = 100 %, bottom = 0 %)

def ret(s):
    """schematic retention of a typical short at second s (1.0 = everyone)"""
    if s < .4: return 1.0
    r = .52 + .48 * math.exp(-(s - .4) / 1.1)          # steep hook drop
    r -= .12 * clamp((s - 3) / 4)                       # second drop, seconds 4-7
    return r - .006 * max(0, s - 7)                     # slow bleed afterwards

def X(s): return CX0 + (CX1 - CX0) * clamp(s / T_END)
def Y(r): return CY1 - (CY1 - CY0) * r

def timer(d, t):
    s = min(t, T_END)
    d.text((X0 - 6, 300), f"{s:04.1f}", font=F(MONO, 200), fill=INK)
    d.text((X0 + 520, 400), "SEC", font=F(BLK, 60), fill=SIG)

def chart(d, t, zone=None, mark=None):
    if zone:
        a, b, lab = zone
        d.rectangle([X(a), CY0 - 10, X(b), CY1], fill=mix(BG, SIG, .16))
        d.text((X(a) + 8, CY1 - 36), lab, font=F(BLK, 26), fill=SIG)
    d.line([CX0, CY1, CX1, CY1], fill=INK, width=3); d.line([CX0, CY0, CX0, CY1], fill=INK, width=3)
    for p, lab in ((1, "100 %"), (.5, "50 %"), (0, "0")):
        d.text((CX0 - 12, Y(p)), lab, font=F(MONO, 20), fill=MID, anchor="rm")
    for s in range(0, int(T_END) + 1, 5): d.text((X(s), CY1 + 12), f"{s}s", font=F(MONO, 20), fill=MID, anchor="ma")
    now = min(t, T_END); n = max(2, int(now * 12))
    pts = [(X(s), Y(ret(s))) for s in np.linspace(0, now, n)]
    d.line(pts, fill=MID, width=6)
    d.line([CX0, Y(1), X(now), Y(1)], fill=SIG, width=6)                       # you: still at 100 %
    if mark is not None:
        d.line([X(mark), CY0 - 10, X(mark), CY1], fill=INK, width=3)
        d.text((X(mark) + 8, CY1 - 34), "median", font=F(BLK, 24), fill=INK)
    d.ellipse([X(now) - 14, Y(1) - 14, X(now) + 14, Y(1) + 14], fill=SIG)
    box_label(d, min(X(now) + 22, CX1 - 70), Y(1) - 52, "YOU", 26, WHITE, SIG, font=BLK)
    d.ellipse([X(now) - 9, Y(ret(now)) - 9, X(now) + 9, Y(ret(now)) + 9], fill=MID)
    if now > 2: d.text((X(now) + 16, Y(ret(now)) + 6), "typical", font=F(COND, 24), fill=MID, anchor="la")
    d.text((X1, 1146), "typical curve: schematic", font=F(MED, 22), fill=MID, anchor="ra")

def base(d, t, zone=None, mark=None): timer(d, t); chart(d, t, zone, mark)

def sc_hook(img, d, t):
    base(d, t, (0, 3, "DECIDE"))
    ts = cue("hook", "swipe") - .15; tt = cue("hook", "stay") - .15
    if t >= ts: box_label(d, X0, 970, "SWIPE", 70, WHITE, MID, font=BLK)
    if t >= tt: box_label(d, X0 + 330, 970, "OR STAY?", 70, WHITE, SIG, font=BLK)

def sc_drop(img, d, t):
    base(d, t, (3, 7, "PAY OFF"))
    words_in(d, t, [("THE HOOK", S("drop") + .9, 950, 90, INK), ("IS OVER.", S("drop") + 1.1, 1050, 90, SIG)])

def sc_glance(img, d, t):
    base(d, t)
    if t >= S("glance") + .3: d.text((X0, 945), "0.25 s", font=F(BLK, 150), fill=SIG)
    d.text((X0 + 470, 985), "to register", font=F(COND, 36), fill=INK); d.text((X0 + 470, 1030), "a feed post", font=F(COND, 36), fill=INK)
    fig(d, "Fors Marsh for Facebook, 2016")

def sc_value(img, d, t):
    base(d, t, (0, 3, "FIRST 3 S"))
    counter(d, X0, 945, t, S("value") + .3, .7, 47, "{:.0f} %", 150, SIG)
    d.text((X0 + 330, 985), "of an ad's impact", font=F(COND, 36), fill=INK); d.text((X0 + 330, 1030), "in the first 3 seconds (up to)", font=F(COND, 36), fill=INK)
    fig(d, "Facebook / Nielsen")

def sc_half(img, d, t):
    m = .45 * T_END
    base(d, t, mark=m)
    counter(d, X0, 945, t, S("half") + .3, .6, 45, "{:.0f} %", 150, SIG)
    d.text((X0 + 330, 985), "median view-through", font=F(COND, 36), fill=INK); d.text((X0 + 330, 1030), "YouTube Shorts", font=F(COND, 36), fill=INK)
    if t >= cue("half", "behind you") - .2: box_label(d, X0 + 330, 1082, f"THIS VIDEO: SECOND {m:.0f}. PASSED.", 28, WHITE, INK, font=BLK)
    fig(d, "quso.ai, 508k Shorts")

def sc_algo(img, d, t):
    base(d, t)
    for i, lab in enumerate(("1 WATCH TIME", "2 LIKES", "3 SENDS")):
        k = ease((t - S("algo") - .4 - i * .2) / .3)
        if k > 0: box_label(d, X0 + i * 0, 945 + i * 62, lab, 44, WHITE, SIG if i == 0 else MID, font=BLK)
    if t >= cue("algo", "voted") - .2: box_label(d, X0 + 470, 945, "DONE.", 50, WHITE, INK, font=BLK)
    fig(d, "Adam Mosseri, Instagram, 2025")

def end_card(d, t):
    k0 = S("end")
    for i, (w_, col) in enumerate((("YOU", INK), ("STAYED.", SIG))):
        k = ease((t - k0 - i * .15) / .35)
        if k > 0: d.text((X0 - 8, 300 + i * 220), w_, font=F(BLK, 220), fill=mix(BG, col, k))
    lk, sk = cue("end", "likes") - .1, cue("end", "sends") - .1
    if t >= lk: box_label(d, X0, 800, "2 LIKE", 70, WHITE, INK, font=BLK)
    if t >= sk: box_label(d, X0 + 330, 800, "3 SEND", 70, WHITE, SIG, font=BLK)
    if t > k0 + 1.4:
        d.text((X0, 980), "SOURCES", font=F(COND, 26), fill=SIG)
        for i, l in enumerate(EP.sources): d.text((X0, 1016 + i * 32), l, font=F(MED, 24), fill=INK)
        box_label(d, X1, 1110, EP.handle, 32, WHITE, INK, anchor="ra")
EP.end_card = end_card

EP.scenes = {"hook": sc_hook, "drop": sc_drop, "glance": sc_glance, "value": sc_value, "half": sc_half, "algo": sc_algo}
FX = [(0.0, thud(.5), 0), *[(float(s), tick(.05), 0) for s in range(1, int(T_END) + 1)], *EP.cut_fx(.06),
      (cue("hook", "swipe") - .15, pop(.14), -.3), (cue("hook", "stay") - .15, thud(.4), .3), (S("drop") + .9, thud(.4), 0),
      (S("glance") + .3, pop(.15), 0), (S("value") + .3, riser(.7, .04), 0), (S("half") + .3, riser(.6, .04), 0), (cue("half", "behind you") - .2, thud(.4), 0),
      *[(S("algo") + .4 + i * .2, pop(.12), (i - 1) / 2) for i in range(3)], (cue("algo", "voted") - .2, thud(.45), 0),
      (S("end"), thud(.5), 0), (cue("end", "likes") - .1, pop(.15), -.3), (cue("end", "sends") - .1, pop(.15), .3)]
if __name__ == "__main__": EP.run(FX)
