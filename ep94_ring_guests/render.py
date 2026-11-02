"""NOT JUST YOU – No. 94 (Wedding Math 2/3): more guests, cheaper ring, a honeymoon (Francis-Tan & Mialon 2015). Look C+D, dark."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from thread import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "guests": .5, "ring": .5, "honey": .5, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "guests", "ring", "honey", "point", "end"]           # opener: guess (toolkit)
EP = ThreadEpisode(TL, 94, "RING & GUESTS", order=ORDER, dark=True, label="WEDDING MATH 2/3 · SURVEY",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Francis-Tan & Mialon (2015), Economic Inquiry", "survey of 3,000+ ever-married US adults · correlation"),
                   music=dict(bpm=104, root=2, prog="major", kick="four", audio="v5", gaps=[(E("hook") + .05, S("guests") + .05)]),
                   cover=dict(words=["BIG WEDDING", "OR SMALL:", "WHICH LASTS?"], kicker="Wedding Math, part 2 of 3."))

CROWD = [(x, 1062, .15) for x in (480, 380, 580, 280, 680, 180, 780, 90, 870)]
def sc_hook(img, d, t):
    t0, tb, tr = S("hook"), cue("hook", "big wins") - .1, cue("hook", "right way") - .1
    d.text((X0 - 4, 320), "PLOT TWIST:", font=F(BLK, 120), fill=MID)
    if t >= tb:
        k = ease((t - tb) / .25); d.text((X0 - 4 - (1 - k) * 60, 450), "BIG WINS!", font=F(BLK, 170), fill=mix(BG, SIG, k))
    if t >= tr: d.text((X0 + 4, 650), "… if it's big in the right way.", font=F(COND, 50), fill=INK)
    silhouette(img, lambda m: (front_bust(m, 400, 850, .3, 255), front_bust(m, 560, 850, .3, 255)), (230, 740, 730, 1010), INK, cell=8)
    if t >= tb:                                           # the guests arrive around the couple
        n = min(len(CROWD), int((t - tb) / .1) + 1)
        for x, y, s in CROWD[:n]:
            silhouette(img, lambda m, x=x, y=y, s=s: front_bust(m, x, y, s, 255), (int(x - 110 * s / .22), int(y - 76 * s / .22), int(x + 110 * s / .22), int(y + 110 * s / .22)), MID, cell=6)
    fig(d, "fig. 1 — the couple and their guests, schematic")

FIELD = (X0 + 14, 640, X1, 940)
def sc_guests(img, d, t):
    t0, tm, tu = S("guests"), cue("guests", "the more guests") - .1, cue("guests", "Up to") - .1
    d.text((X0, 320), "GUESTS", font=F(BLK, 150), fill=INK)
    n = 0 if t < tm else int(200 * ease_io(clamp((t - tm) / 2.4)))
    counter(d, X0 + 620, 345, t, tm, 2.4, 200, "{:.0f}", 120, INK) if t >= tm else None
    x0, y0, x1, y1 = FIELD; cols = len(range(int(x0), int(x1), 30))
    dot_field(d, FIELD, t, cell=30, col=RULE, hit=set(range(n)), hitcol=INK)
    k = clamp((t - tm) / 2.4) if t >= tm else 0          # divorce risk meter shrinks as the room fills (schematic)
    d.text((X0, 975), "DIVORCE RISK", font=F(BLK, 44), fill=SIG)
    d.rectangle([X0, 1040, X0 + 840 * (1 - .55 * ease_io(k)), 1100], fill=SIG)
    if t >= tu: box_label(d, X1, 490, "UP TO ~200", 52, WHITE, SIG, font=BLK, anchor="ra")
    fig(d, "risk falls as attendance rises · meter schematic")

def ring_icon(d, cx, cy, r, col):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=max(6, r // 5))
    d.polygon([(cx - r * .45, cy - r * 1.05), (cx + r * .45, cy - r * 1.05), (cx + r * .7, cy - r * 1.35), (cx, cy - r * 1.75), (cx - r * .7, cy - r * 1.35)], fill=col)

def xbars(d, t, rows, vmax, y0=600, step=270):
    for j, (lab, v, col, tk) in enumerate(rows):
        if t < tk - .01: continue
        k = ease((t - tk) / .6); y = y0 + j * step
        d.text((X0, y), lab, font=F(BLK, 54), fill=col)
        w = 640 * v / vmax * k
        d.rectangle([X0, y + 75, X0 + max(6, w), y + 215], fill=col)
        d.text((X0 + max(6, w) + 16, y + 145), f"{v * k:.1f} ×", font=F(BLK, 72), fill=col, anchor="lm")

def sc_ring(img, d, t):
    t0, tm = S("ring"), cue("ring", "Men who spent") - .1
    d.text((X0, 320), "THE RING", font=F(BLK, 150), fill=INK)
    ring_icon(d, X1 - 90, 440, 56, INK)
    if t >= tm: d.text((X0 + 4, 485), "what men spent on it", font=F(COND, 46), fill=MID)
    xbars(d, t, [("$500–2K", 1.0, MID, cue("ring", "Compared") - .1), ("$2–4K", 1.3, SIG, cue("ring", "two to four") - .1)], 1.6)
    tr = cue("ring", "one point three") - .1
    if t >= tr: box_label(d, X1, 600, "1.3 × RISK", 52, WHITE, SIG, font=BLK, anchor="ra")
    fig(d, "relative divorce risk · men · engagement ring")

def sc_honey(img, d, t):
    t0, tl = S("honey"), cue("honey", "less likely") - .1
    d.text((X0, 320), "HONEYMOON?", font=F(BLK, 130), fill=INK)
    k = ease(clamp((t - t0 - .1) / .6)); cx, cy = 480, 920       # sun rising over the sea
    r = 120; y = cy + 120 * (1 - k)
    d.pieslice([cx - r, y - r, cx + r, y + r], 180, 360, fill=INK)
    for i in range(7):
        a = math.pi * (i + .5) / 7; d.line([cx - (r + 30) * math.cos(a), y - (r + 30) * math.sin(a), cx - (r + 70 * k) * math.cos(a), y - (r + 70 * k) * math.sin(a)], fill=INK, width=8) if k > .2 else None
    d.rectangle([X0 - 40, cy, X1 + 40, 1125], fill=BG)
    for j in range(3):
        yy = cy + 30 + j * 50; ph = t * 3 + j
        d.line([(x, yy + 10 * math.sin(x / 40 + ph)) for x in range(X0, X1, 8)], fill=MID, width=6)
    if t >= tl: box_label(d, X0 + 4 - (1 - ease((t - tl) / .2)) * 60, 500, "LOWER RISK", 60, WHITE, SIG, font=BLK)
    fig(d, "couples who took a honeymoon · schematic")

def sc_point(img, d, t):
    t0, ti = S("point"), cue("point", "invite more") - .2
    words_in(d, t, [("LESS RING.", t0 + .1, 320, 150, INK)] + ([("MORE PEOPLE.", ti, 490, 130, SIG)] if t >= ti else []))
    k = clamp((t - t0) / .8); ring_icon(d, X1 - 110, 840, int(70 - 34 * ease(k)), MID)
    if t >= ti:
        n = min(24, int((t - ti) / .05) + 1)
        for i in range(n):
            r_, c_ = divmod(i, 8); x = X0 + 20 + c_ * 70; y = 760 + r_ * 110
            silhouette(img, lambda m, x=x, y=y: front_bust(m, x, y, .12, 255), (x - 60, y - 42, x + 60, y + 60), INK, cell=5)
    fig(d, "fig. 2 — Wedding Math, part 2 of 3")

EP.carry = {"guests": [((20, 1000, 940, 1140), (X0 + 14, 640, X1, 700))]}

EP.scenes = {"hook": sc_hook, "guests": sc_guests, "ring": sc_ring, "honey": sc_honey, "point": sc_point}
FX = [*EP.cut_fx(), (cue("hook", "big wins") - .1, thud(.5), 0), *[(cue("hook", "big wins") - .1 + i * .1, tick(.03), (i % 5 - 2) / 3) for i in range(len(CROWD))],
      (cue("hook", "right way") - .1, pop(.12), .2), (S("guests") + .1, pop(.12), 0), (cue("guests", "the more guests") - .1, riser(2.2, .04), 0),
      *[(cue("guests", "the more guests") + i * .2, tick(.03), (i % 5 - 2) / 3) for i in range(12)], (cue("guests", "Up to") - .1, thud(.45), .3),
      (S("ring") + .1, pop(.12), 0), (cue("ring", "Men who spent") - .1, tick(.06), 0), (cue("ring", "two to four") - .1, thud(.5), 0),
      (cue("ring", "one point three") - .1, pop(.15), .3), (cue("ring", "Compared") - .1, pop(.12), -.3),
      (S("honey") + .9, tick(.06), 0), (cue("honey", "less likely") - .1, thud(.45), 0),
      (S("point") + .1, pop(.12), 0), (cue("point", "invite more") - .2, thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
