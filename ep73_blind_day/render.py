"""NOT JUST YOU – No. 73: Love Is Blind Day (OkCupid 2013, via Rudder 2014). Look C+D, dark."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from dating import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .6, "study": .6, "result": .5, "back": .5, "melt": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "result", "back", "melt", "point", "end"]
EP = ThreadEpisode(TL, 73, "BLIND DAY", order=ORDER, dark=True, label="PLATFORM DATA · OKCUPID",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Rudder (2014), We Experiment On Human Beings,", "OkCupid blog · Dataclysm (2014)"),
                   music=dict(bpm=96, root=-2, prog="tense", kick="four", gaps=[(E("study") + .05, S("result") + .05)]),
                   cover=dict(words=["PHOTOS", "OFF."], kicker="For one day."))

def sc_hook(img, d, t):
    toff = cue("hook", "turned off") - .1
    d.text((X0 - 6, 320), "PHOTOS", font=F(BLK, 200), fill=INK); d.text((X0 - 6, 510), "OFF.", font=F(BLK, 200), fill=SIG)
    ph = 1 - clamp((t - toff) / .4) if t > .5 else 1
    for i, x in enumerate((210, 480, 750)):
        profile_card(img, d, x, 950, .72, photo=ph, col=INK if i != 1 else SIG)
    if toff <= t < toff + .3: glitch(img, (X0, 720, X1, 1140), 1.0, seed=int(t * 30))
    fig(d, "fig. 1 — every profile, blank")

def sc_study(img, d, t):
    t0 = S("study")
    counter(d, X0, 320, t, t0 + .1, .8, 7, "{:.0f} HOURS", 170, SIG)
    d.text((X0 + 6, 520), "Love Is Blind Day · Jan 15, 2013", font=F(COND, 40), fill=INK)
    clock(d, 270, 860, 180, minutes=9 * 60 + 420 * clamp((t - t0) / 3.0))
    profile_card(img, d, 680, 880, .62, photo=0, col=INK)
    fig(d, "photos hidden, site otherwise normal")

def sc_result(img, d, t):
    t0, td = S("result"), cue("result", "deeper") - .3
    counter(d, X0, 320, t, t0 + .1, .7, 44, "+{:.0f} %", 230, SIG)
    d.text((X0 + 6, 560), "more replies to first messages", font=F(COND, 40), fill=INK)
    bubbles(d, X0 + 10, X1 - 260, 660, 6, k=(t - t0 - .3) / 1.6)
    if t >= td: box_label(d, X1, 700, "DEEPER", 50, WHITE, SIG, font=BLK, anchor="ra"); box_label(d, X1, 790, "TALKS", 50, WHITE, INK, font=BLK, anchor="ra")
    fig(d, "vs. a normal day on the site")

def sc_back(img, d, t):
    t0 = S("back"); tb = cue("back", "photos came") - .2
    d.text((X0 - 6, 320), "4 PM.", font=F(BLK, 230), fill=INK)
    ph = clamp((t - tb) / .5)
    for i, x in enumerate((210, 480, 750)): profile_card(img, d, x, 950, .72, photo=ph, col=INK if i != 1 else SIG)
    if tb <= t < tb + .3: glitch(img, (X0, 720, X1, 1140), 1.0, seed=int(t * 30))
    fig(d, "fig. 2 — faces are back")

def sc_melt(img, d, t):
    t0, tm = S("melt"), cue("melt", "melted") - .4
    counter(d, X0, 320, t, t0 + .1, .8, 2200, "{:,.0f}", 220, SIG)
    d.text((X0 + 6, 560), "conversations that started blind", font=F(COND, 40), fill=INK)
    m = clamp((t - tm) / 1.2); fade = [clamp(1 - m * 2.2 + (i * .37 % 1) * .9) for i in range(7)]
    bubbles(d, X0 + 10, X1 - 40, 660, 7, k=1, fade=fade, h=48, gap=16)
    fig(d, "after the photos came back")

def sc_point(img, d, t):
    t0, tw = S("point"), cue("point", "with one") - .2
    words_in(d, t, [("NO FACE:", t0, 320, 110, MID), ("KINDER.", t0 + .3, 440, 150, INK)] + ([("FACE:", tw, 640, 110, MID), ("PICKY.", tw + .2, 760, 150, SIG)] if t >= tw else []))
    silhouette(img, lambda m: bust(m, 720, 470, .42, 255, f=-1), (560, 360, 900, 660), MID, cell=8)
    if t >= tw: silhouette(img, lambda m: bust(m, 720, 820, .42, 255, f=-1), (560, 700, 900, 1010), SIG, cell=8)
    fig(d, "fig. 3 — same people, different rules")

EP.scenes = {"hook": sc_hook, "study": sc_study, "result": sc_result, "back": sc_back, "melt": sc_melt, "point": sc_point}
FX = [(0.0, thud(.5), 0), (cue("hook", "turned off") - .1, rewind_sfx(.1, .3), 0), *EP.cut_fx(), *[(S("study") + .1 + i * .1, tick(.03), (i % 5 - 2) / 3) for i in range(8)],
      (S("result") + .05, thud(.55), 0), (cue("result", "deeper") - .3, pop(.15), 0), (cue("back", "photos came") - .2, rewind_sfx(.12, .3), 0),
      (S("melt") + .1, thud(.45), 0), (cue("melt", "melted") - .4, whoosh(1.0, .05), 0), (cue("point", "with one") - .2, thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
