"""NOT JUST YOU · AFTER DARK – No. 69: vibrator use, women vs men (Herbenick et al. 2009; Reece et al. 2009). Look C+D, dark.
Visuals stay abstract (no product depictions): type, percentages, silhouettes."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from thread import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "study": .8, "women": .5, "men": .6, "health": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "women", "men", "health", "point", "end"]
EP = ThreadEpisode(TL, 69, "THE DRAWER", order=ORDER, dark=True, series="NOT JUST YOU · AFTER DARK",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Herbenick et al. (2009) & Reece et al. (2009),", "Journal of Sexual Medicine 6(7)"),
                   music=dict(bpm=94, root=2, prog="dream", kick="half", gaps=[(E("study") + .05, S("women") + .05)]),
                   cover=dict(words=["MEN", "OR WOMEN?"], kicker="Who owns more toys."))

def drawer(d, x, y, w, h, open_k, col=INK):
    d.rectangle([x, y, x + w, y + h], outline=col, width=5)
    dy = 70 * ease(open_k); d.rectangle([x + 20, y + 30 + dy, x + w - 20, y + h - 30 + dy], outline=col, width=4, fill=BG)
    d.rectangle([x + w / 2 - 40, y + h / 2 - 8 + dy, x + w / 2 + 40, y + h / 2 + 8 + dy], fill=SIG)

def grid(d, n, k, col, y0=660):
    for i in range(100):
        r, c = divmod(i, 10); x = X0 + c * 86; y = y0 + r * 44
        d.rectangle([x, y, x + 74, y + 34], fill=col if i < n * k else None, outline=col if i < n * k else INK, width=2)

def sc_hook(img, d, t):
    d.text((X0 - 6, 320), "MEN", font=F(BLK, 220), fill=INK); d.text((X0 - 6, 520), "OR WOMEN?", font=F(BLK, 150), fill=SIG)
    silhouette(img, lambda m: front_bust(m, 260, 860, .5, 255), (80, 760, 470, 1130), INK, cell=9)
    silhouette(img, lambda m: front_bust(m, 700, 860, .5, 255), (500, 760, 900, 1130), SIG, cell=9)
    d.text((480, 900), "?", font=F(BLK, 160), fill=INK, anchor="mm")
    fig(d, "fig. 1 — who's got the toy drawer")

def sc_study(img, d, t):
    t0 = S("study")
    counter(d, X0, 320, t, t0 + .1, .9, 3103, "{:,.0f}", 230, SIG)
    d.text((X0 + 6, 560), "US adults · 18 to 60 · two surveys", font=F(COND, 40), fill=INK)
    drawer(d, 260, 700, 440, 280, (t - t0 - .6) / .6)
    fig(d, "Indiana University, 2009")

def sc_women(img, d, t):
    t0 = S("women")
    counter(d, X0, 320, t, t0 + .1, .8, 53, "{:.0f} %", 230, SIG)
    d.text((X0 + 6, 560), "of women have used a vibrator", font=F(COND, 40), fill=INK)
    grid(d, 53, clamp((t - t0 - .2) / 1.2), SIG)
    fig(d, "2,056 women · Herbenick et al.")

def sc_men(img, d, t):
    t0, tp = S("men"), cue("men", "most of them") - .2
    counter(d, X0, 320, t, t0 + .4, .8, 45, "{:.0f} %", 230, INK)
    d.text((X0 + 6, 560), "of men, too", font=F(COND, 40), fill=INK)
    grid(d, 45, clamp((t - t0 - .4) / 1.2), INK)
    if t >= tp: box_label(d, X1, 500, "MOSTLY WITH A PARTNER", 32, WHITE, SIG, anchor="ra")
    fig(d, "1,047 men · Reece et al.")

def sc_health(img, d, t):
    t0 = S("health")
    d.text((X0, 320), "BONUS:", font=F(BLK, 150), fill=INK)
    d.text((X0, 480), "more self-checks", font=F(BLK, 90), fill=SIG)
    silhouette(img, lambda m: body(m, 480, 1120, 470, 255), (280, 630, 680, 1130), INK, cell=9)
    bbox(d, (400, 720, 560, 860), "CHECK-UP ✓".replace("✓", "OK"), SIG, (t - t0 - .4) / .3, coords=False)
    fig(d, "users did more sexual-health self-exams (a link, not proof)")

def sc_point(img, d, t):
    t0, tb = S("point"), cue("point", "both halves") - .2
    words_in(d, t, [("HALF THE", t0 + .5, 320, 170, INK), ("COUNTRY.", t0 + .7, 490, 170, SIG)] + ([("BOTH HALVES.", tb, 680, 110, INK)] if t >= tb else []))
    drawer(d, 300, 860, 360, 220, 1)
    fig(d, "fig. 2 — not a secret drawer thing")

EP.scenes = {"hook": sc_hook, "study": sc_study, "women": sc_women, "men": sc_men, "health": sc_health, "point": sc_point}
FX = [(0.0, thud(.5), 0), (.4, pop(.15), 0), *EP.cut_fx(), (S("study") + .6, whoosh(.5, .06), 0), (S("women") + .05, thud(.55), 0),
      *[(S("women") + .2 + i * .1, tick(.03), (i % 5 - 2) / 3) for i in range(12)], (S("men") + .4, thud(.45), 0),
      (cue("men", "most of them") - .2, pop(.15), .3), (S("health") + .4, pop(.15), 0), (cue("point", "both halves") - .2, thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
