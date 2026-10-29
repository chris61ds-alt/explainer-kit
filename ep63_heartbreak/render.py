"""NOT JUST YOU – No. 63: heartbreak looks like withdrawal (Fisher et al. 2010). Look C+D, dark."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from thread import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .8, "result": .5, "pain": .5, "hope": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "pain", "hope", "point", "end"]
EP = ThreadEpisode(TL, 63, "YOUR EX IS A DRUG", order=ORDER, dark=True, label="SMALL STUDY",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Fisher, Brown, Aron, Strong & Mashek (2010),", "Journal of Neurophysiology 104(1)"),
                   music=dict(bpm=82, root=-4, prog="minor", kick="half", gaps=[(E("study") + .05, S("result") + .05)]),
                   cover=dict(words=["YOUR EX", "IS A DRUG."], kicker="To your brain, at least."))

def brain(d, cx, cy, s=1.0, col=INK):
    d.ellipse([cx - 260 * s, cy - 180 * s, cx + 260 * s, cy + 170 * s], outline=col, width=6)
    for (a, b, c, e) in ((-200, -130, 120, 60), (-120, -60, 220, 120), (-230, 0, 0, 160)):
        d.arc([cx + a * s, cy + b * s, cx + c * s, cy + e * s], 200, 340, fill=RULE, width=4)
    d.arc([cx + 120 * s, cy + 40 * s, cx + 300 * s, cy + 240 * s], 180, 270, fill=col, width=6)

def glow(d, x, y, r, k, col=SIG):
    for i in range(4, 0, -1):
        rr = r * (1 + i * .35) * k; d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=mix(BG, col, .12 * (5 - i)))
    d.ellipse([x - r * k, y - r * k, x + r * k, y + r * k], fill=col)

def sc_hook(img, d, t):
    d.text((X0 - 6, 320), "YOUR EX", font=F(BLK, 190), fill=INK); d.text((X0 - 6, 510), "= A DRUG.", font=F(BLK, 160), fill=SIG)
    silhouette(img, lambda m: bust(m, 300, 840, .75, 255, f=1), (60, 700, 620, 1130), INK, cell=10)
    x0, y0 = 600, 760; d.rounded_rectangle([x0, y0, x0 + 230, y0 + 340], radius=24, outline=INK, width=4)
    silhouette(img, lambda m: front_bust(m, x0 + 115, y0 + 120, .38, 255), (x0 + 10, y0 + 20, x0 + 220, y0 + 330), SIG, cell=7)
    fig(d, "fig. 1 — still scrolling their photos")

def sc_study(img, d, t):
    t0 = S("study")
    counter(d, X0, 320, t, t0 + .1, .6, 15, "{:.0f}", 230, SIG)
    d.text((X0 + 6, 560), "just dumped · still madly in love", font=F(COND, 40), fill=INK)
    for i in range(6):
        k = ((t - t0) * .6 + i / 6) % 1; r = 140 + 90 * k
        d.ellipse([420 - r, 860 - r, 420 + r, 860 + r], outline=mix(BG, MID, 1 - k), width=3)
    silhouette(img, lambda m: bust(m, 400, 830, .55, 255, f=1), (200, 700, 640, 1130), INK, cell=8)
    bbox(d, (680, 720, 880, 980), "PHOTO: EX", SIG, (t - t0 - .8) / .3, coords=False)
    fig(d, "brain scans while viewing the ex · 2010")

def sc_result(img, d, t):
    t0, tc = S("result"), cue("result", "cocaine") - .3
    d.text((X0, 320), "REWARD +", font=F(BLK, 130), fill=INK); d.text((X0, 460), "CRAVING", font=F(BLK, 130), fill=SIG)
    brain(d, 480, 850, .9)
    glow(d, 450, 900, 28, ease((t - t0 - .3) / .4)); glow(d, 540, 860, 22, ease((t - t0 - .7) / .4))
    if t >= tc: box_label(d, X1, 640, "LIKE COCAINE", 44, WHITE, SIG, font=BLK, anchor="ra")
    fig(d, "VTA, nucleus accumbens, orbitofrontal cortex")

def sc_pain(img, d, t):
    t0 = S("pain")
    d.text((X0, 320), "+ PAIN", font=F(BLK, 200), fill=SIG)
    brain(d, 480, 850, .9)
    glow(d, 450, 900, 28, 1); glow(d, 540, 860, 22, 1); glow(d, 380, 800, 24, ease((t - t0 - .2) / .4), INK)
    d.text((X0, 1060), "insula · anterior cingulate", font=F(MONO, 24), fill=MID)
    fig(d, "regions tied to physical pain")

def sc_hope(img, d, t):
    t0 = S("hope"); k = clamp((t - t0 - .2) / 2.4)
    d.text((X0, 320), "IT FADES.", font=F(BLK, 180), fill=SIG)
    OX, OY, GW, GH = X0 + 40, 1060, X1 - X0 - 60, 380
    d.line([OX, OY, OX + GW, OY], fill=INK, width=4); d.line([OX, OY, OX, OY - GH], fill=INK, width=4)
    d.text((OX + 10, OY - GH - 10), "attachment signal", font=F(COND, 28), fill=INK, anchor="ld"); d.text((OX + GW, OY + 18), "time since breakup", font=F(MONO, 22), fill=MID, anchor="ra")
    pts = [(OX + GW * u, OY - GH * (.9 * math.exp(-2.2 * u) + .08)) for u in np.linspace(0, k, max(2, int(60 * k)))]
    if len(pts) > 1: d.line(pts, fill=SIG, width=7)
    d.text((X1, 1146), "schematic", font=F(MED, 22), fill=MID, anchor="ra")

def sc_point(img, d, t):
    t0, tw, te = S("point"), cue("point", "it's withdrawal") - .2, cue("point", "withdrawal ends") - .2
    words_in(d, t, [("NOT WEAKNESS.", t0, 320, 120, INK), ("WITHDRAWAL.", tw, 460, 140, SIG)] + ([("IT ENDS.", te, 640, 140, INK)] if t >= te else []))
    calm = clamp((t - te) / 1.0)
    d.line(ekg(LX, RX, THREAD_Y + 140, t, period=220, amp=60 * (1 - .6 * calm), speed=300 - 150 * calm, chaos=.6 * (1 - calm), seed=int(t * 10)), fill=SIG, width=6)
    fig(d, "fig. 2 — give it time")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "pain": sc_pain, "hope": sc_hope, "point": sc_point}
FX = [(0.0, thud(.5), 0), (.5, pop(.12), .3), *EP.cut_fx(), *[(S("study") + i * .8, softkick(.12), 0) for i in range(6)],
      (S("result") + .05, thud(.55), 0), (S("result") + .3, riser(.6, .05), 0), (cue("result", "cocaine") - .3, thud(.45), 0),
      (S("pain") + .2, pop(.15), -.3), (S("hope") + .2, whoosh(1.4, .05), 0), (cue("point", "it's withdrawal") - .2, thud(.45), 0),
      (cue("point", "withdrawal ends") - .2, riser(.4, .05), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
