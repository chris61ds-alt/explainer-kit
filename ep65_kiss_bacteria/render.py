"""NOT JUST YOU · AFTER DARK – No. 65: 80 million bacteria per kiss (Kort et al. 2014). Look C+D, dark."""
import os, sys, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from thread import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .8, "result": .5, "often": .5, "twist": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "often", "twist", "point", "end"]
EP = ThreadEpisode(TL, 65, "80 MILLION", order=ORDER, dark=True, series="NOT JUST YOU · AFTER DARK", label="SMALL STUDY",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Kort, Caspers, van de Graaf, van Egmond, Keijser &", "Roeselers (2014), Microbiome 2:41"),
                   music=dict(bpm=88, root=2, prog="dream", kick="half", gaps=[(E("study") + .05, S("result") + .05)]),
                   cover=dict(words=["ONE KISS.", "80 MILLION."], kicker="Bacteria. Swapped."))

def couple(img, d, gap=0, cell=10, y=760, s=.95):
    silhouette(img, lambda m: bust(m, 330 - gap, y, s, 255, f=1), (40, 450, 640, 1140), INK, cell=cell)
    silhouette(img, lambda m: bust(m, 630 + gap, y + 10, s * .96, 255, f=-1), (330, 450, 1040, 1140), SIG, cell=cell)

def swarm(d, t, n=70, x0=440, x1=520, y=750, seed=3):
    rnd = random.Random(seed)
    for i in range(n):
        u = (t * .7 + rnd.random()) % 1; x = lerp(x0, x1, u) + 30 * math.sin(t * 3 + i); yy = y + rnd.uniform(-60, 60) + 10 * math.sin(t * 5 + i * 1.7)
        r = rnd.choice((3, 4, 5)); d.ellipse([x - r, yy - r, x + r, yy + r], fill=SIG if i % 3 else INK)

def sc_hook(img, d, t):
    d.text((X0 - 6, 320), "80,000,000", font=F(BLK, 130), fill=SIG)
    d.text((X0, 470), "bacteria · one 10-second kiss", font=F(COND, 42), fill=INK)
    couple(img, d, 0, y=800, s=.85)
    swarm(d, t, y=780)
    fig(d, "fig. 1 — romance, microscopically")

def sc_study(img, d, t):
    t0, tk = S("study"), cue("study", "then they kissed") - .2
    counter(d, X0, 320, t, t0 + .1, .6, 21, "{:.0f} COUPLES", 160, SIG)
    if t < tk:
        x, y = 480, 900; d.rounded_rectangle([x - 70, y - 220, x + 70, y + 60], radius=30, outline=INK, width=6); d.rectangle([x - 40, y - 270, x + 40, y - 220], fill=INK)
        lvl = clamp(1 - (t - t0 - .8) / 2.0); d.rectangle([x - 62, y + 52 - 260 * lvl, x + 62, y + 52], fill=SIG)
        d.text((x, y + 100), "probiotic drink · traceable bacteria", font=F(MONO, 22), fill=MID, anchor="ma")
    else:
        couple(img, d, 0, cell=9, y=820, s=.8)
        clock(d, 830, 560, 60, t, None, SIG, 3.0); d.text((830, 640), "10 s", font=F(MONO, 26), fill=SIG, anchor="ma")
    fig(d, "Kort et al., 2014")

def sc_result(img, d, t):
    t0 = S("result")
    d.text((X0 - 6, 320), "× 3", font=F(BLK, 240), fill=SIG)
    d.text((X0, 560), "in the partner's saliva", font=F(COND, 42), fill=INK)
    if t >= cue("result", "about eighty") - .3: box_label(d, X0, 640, "≈ 80 MILLION SWAPPED", 44, WHITE, SIG, font=BLK)
    k = clamp((t - t0) / 1.6)
    for i in range(int(240 * k)):
        r, c = divmod(i, 24); x = X0 + 20 + c * 36; y = 760 + r * 34
        d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=SIG if i % 3 == 0 else MID)
    fig(d, "probiotic tracer bacteria · schematic")

def sc_often(img, d, t):
    t0 = S("often")
    d.text((X0, 320), "9+ KISSES", font=F(BLK, 160), fill=INK); d.text((X0, 490), "A DAY", font=F(BLK, 160), fill=SIG)
    for i in range(9):
        k = ease((t - t0 - .3 - i * .15) / .25)
        if k <= 0: continue
        x = X0 + 30 + i * 92; r = 26 * k; cy = 760
        d.ellipse([x - r, cy - r * .9, x, cy + r * .1], fill=SIG); d.ellipse([x, cy - r * .9, x + r, cy + r * .1], fill=SIG)
        d.polygon([(x - r * .98, cy - r * .3), (x + r * .98, cy - r * .3), (x, cy + r * .95)], fill=SIG)
    if t >= cue("often", "noticeably") - .2: box_label(d, X0, 880, "MORE SIMILAR SALIVA MICROBES", 38, WHITE, INK)
    fig(d, "couples who kiss often share more bacteria")

def sc_twist(img, d, t):
    t0, tw = S("twist"), cue("twist", "the women") - .2
    d.text((X0, 320), "MEN SAID:", font=F(BLK, 110), fill=INK)
    hbar(d, 470, .8, (t - t0 - .2) / .4, INK, "10 kisses a day", h=90)
    if t >= tw:
        d.text((X0, 650), "WOMEN SAID:", font=F(BLK, 110), fill=SIG)
        hbar(d, 800, .4, (t - tw) / .4, SIG, "5 kisses a day", h=90)
        if t >= tw + .8: d.text((X1, 960), "?", font=F(BLK, 160), fill=INK, anchor="ra")
    fig(d, "self-reported kissing frequency")

def sc_point(img, d, t):
    t0, ta = S("point"), cue("point", "at least") - .2
    words_in(d, t, [("YOU BECOME", t0, 320, 130, INK), ("ALIKE.", t0 + .3, 460, 170, SIG)])
    couple(img, d, 0, cell=9, y=860, s=.75)
    if t >= ta: box_label(d, X1, 680, "(IN YOUR MOUTH)", 34, WHITE, INK, anchor="ra")
    fig(d, "fig. 2 — literally")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "often": sc_often, "twist": sc_twist, "point": sc_point}
FX = [(0.0, thud(.5), 0), *[(i * .09, tick(.025), (i % 5 - 2) / 3) for i in range(13)], *EP.cut_fx(), (cue("study", "then they kissed") - .2, pop(.15), 0),
      (S("result") + .05, thud(.55), 0), (cue("result", "about eighty") - .3, riser(.4, .05), 0), *[(S("often") + .3 + i * .15, pop(.08), (i - 4) / 5) for i in range(9)],
      (cue("twist", "the women") - .2, rewind_sfx(.08, .3), 0), (cue("twist", "the women") + .6, pop(.15), 0), (cue("point", "at least") - .2, pop(.15), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
