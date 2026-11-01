"""NOT JUST YOU – No. 89: couples post more about their relationship on insecure days (Emery, Muise, Dix & Le 2014). Look C+D, dark."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from dating import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"study": .6, "result": .5, "anxious": .5, "avoid": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["study", "result", "anxious", "avoid", "point", "end"]          # opener: statement ("claim" beat)
EP = ThreadEpisode(TL, 89, "COUPLE POSTS", order=ORDER, dark=True, label="3 STUDIES · FACEBOOK",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Emery, Muise, Dix & Le (2014), Personality", "and Social Psychology Bulletin 40(11)"),
                   music=dict(bpm=92, root=3, prog="warm", kick="half", audio="v5", gaps=[(E("study") + .05, S("result") + .05)]),
                   cover=dict(words=["POST THE MOST:", "NOT HAPPIEST."], kicker="What couple photos can mean."))

def couple_post(img, d, x0, y0, w=360, h=250, col=INK, heart=SIG, k=1.0):
    if k <= 0: return
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=16, outline=col, width=4)
    silhouette(img, lambda m: (front_bust(m, x0 + w * .36, y0 + 92, .2, 255), front_bust(m, x0 + w * .64, y0 + 92, .2, 255)),
               (int(x0 + 10), int(y0 + 10), int(x0 + w - 10), int(y0 + h - 50)), col, cell=6, k=k)
    hx, hy = x0 + 26, y0 + h - 30
    d.ellipse([hx - 12, hy - 12, hx, hy], fill=heart); d.ellipse([hx - 2, hy - 12, hx + 10, hy], fill=heart)
    d.polygon([(hx - 12, hy - 5), (hx + 10, hy - 5), (hx - 1, hy + 9)], fill=heart)
    d.rounded_rectangle([x0 + 50, hy - 8, x0 + w * .7, hy + 4], radius=6, fill=MID)

def sc_claim(img, d, t):                                # toolkit statement opener + the feed it is about
    EP.claim_scene(img, d, t)
    d.rounded_rectangle([560, 840, 860, 1160], radius=34, outline=MID, width=6)
    couple_post(img, d, 580, 870, w=260, h=190, heart=SIG)

DAYS = [(X0 + 10 + i * 120, 760) for i in range(7)]
def sc_study(img, d, t):
    t0, td = S("study"), cue("study", "day by day") - .3
    counter(d, X0, 320, t, t0 + .1, .5, 3, "{:.0f}", 230, INK)
    d.text((X0 + 170, 360), "STUDIES", font=F(BLK, 110), fill=INK)
    tf = cue("study", "on Facebook") - .1
    if t >= tf: d.text((X0 + 6 - (1 - ease((t - tf) / .3)) * 40, 570), "how people show their relationship on Facebook", font=F(COND, 40), fill=mix(BG, INK, ease((t - tf) / .3)))
    for i, (x, y) in enumerate(DAYS):
        on = t >= td + i * .12
        d.rectangle([x, y, x + 100, y + 100], outline=INK if on else MID, width=4)
        d.text((x + 50, y + 125), f"DAY {i + 1}", font=F(MONO, 22), fill=MID, anchor="ma")
        if on: d.line([x + 24, y + 52, x + 44, y + 72, x + 78, y + 30], fill=INK, width=7)
    fig(d, "one study: a daily diary · schematic")

INSEC = [.3, .8, .4, .25, .9, .35, .5]
def sc_result(img, d, t):
    t0, tw = S("result"), cue("result", "they posted more") - .2
    d.text((X0, 320), "INSECURE DAY:", font=F(BLK, 110), fill=INK)
    if t >= tw: d.text((X0 - (1 - ease((t - tw) / .3)) * 60, 440), "MORE POSTS.", font=F(BLK, 120), fill=mix(BG, SIG, ease((t - tw) / .3)))
    for i, (x, y) in enumerate(DAYS):
        v = INSEC[i]; hi = v > .7
        d.rectangle([x, y, x + 100, y + 100], outline=INK, width=4)
        r = 12 + 30 * v; d.ellipse([x + 50 - r, y + 50 - r, x + 50 + r, y + 50 + r], fill=INK if hi else MID)
        k = ease((t - tw - i * .05) / .4) if t >= tw else 0
        for j in range(int(1 + 4 * v)):
            if j / 4 > k: break
            yy = y + 140 + j * 44; d.rounded_rectangle([x + 10, yy, x + 90, yy + 32], radius=8, fill=SIG if hi else MID)
    d.text((X0, 700), "circle = insecurity · bars = relationship posts · schematic", font=F(MONO, 22), fill=MID)

def sc_anxious(img, d, t):
    t0 = S("anxious")
    d.text((X0, 320), "ANXIOUS", font=F(BLK, 180), fill=SIG)
    d.text((X0, 510), "attachment", font=F(BLK, 80), fill=INK)
    d.text((X0 + 4, 620), "worried the partner might leave", font=F(COND, 44), fill=INK)
    silhouette(img, lambda m: front_bust(m, 260, 860, .36, 255), (100, 760, 440, 1110), INK, cell=8)
    bubbles(d, 480, X1, 760, 4, clamp((t - t0 - .3) / 1.0), col=MID, alt=SIG, h=56, gap=22)
    fig(d, "want the relationship to be visible")

def sc_avoid(img, d, t):
    t0, tn = S("avoid"), cue("avoid", "No couple photo") - .2
    d.text((X0, 320), "AVOIDANT:", font=F(BLK, 150), fill=INK)
    d.text((X0, 490), "the opposite", font=F(BLK, 80), fill=INK)
    profile_card(img, d, 260, 870, s=.95, photo=1.0, col=MID, text=1.0)
    for i, lab in enumerate(("COUPLE PHOTO", "RELATIONSHIP STATUS")):
        tk = tn + i * .6; y = 760 + i * 170
        if t < tk: continue
        d.text((470, y), lab, font=F(BLK, 40), fill=INK)
        k = ease((t - tk) / .3); w = d.textlength(lab, font=F(BLK, 40))
        d.line([466, y + 24, 466 + (w + 8) * k, y + 24], fill=INK, width=6)
        d.text((470, y + 56), "none", font=F(COND, 36), fill=MID)
    fig(d, "fewer statuses, fewer couple profile pictures")

def sc_point(img, d, t):
    t0, ts = S("point"), cue("point", "Sometimes") - .2
    words_in(d, t, [("NOT PROOF", t0 + .2, 320, 140, INK), ("OF LOVE.", t0 + .4, 460, 140, INK)] +
             ([("SOMETIMES:", ts, 650, 90, MID), ("A QUIET ASK", ts + .3, 760, 115, SIG), ("FOR REASSURANCE.", ts + .5, 880, 95, SIG)] if t >= ts else []))
    fig(d, "fig. 2 — a link, not a rule")

# magic move: the diary day 5 flies into the result chart, where day 5 is the most insecure one
EP.carry = {"result": [((DAYS[4][0], DAYS[4][1], DAYS[4][0] + 100, DAYS[4][1] + 100), (DAYS[4][0], DAYS[4][1], DAYS[4][0] + 100, DAYS[4][1] + 100))]}

EP.scenes = {"claim": sc_claim, "study": sc_study, "result": sc_result, "anxious": sc_anxious, "avoid": sc_avoid, "point": sc_point}
FX = [(0.0, thud(.5), 0), *EP.cut_fx(), (S("study") + .1, pop(.12), 0),
      *[(cue("study", "day by day") - .3 + i * .12, tick(.04), (i - 3) / 4) for i in range(7)],
      (cue("result", "they posted more") - .2, thud(.5), 0), (S("anxious") + .05, thud(.45), 0), (cue("study", "on Facebook") - .1, pop(.12), 0),
      *[(S("anxious") + .3 + i * .25, pop(.1), (.3 if i % 2 else -.3)) for i in range(4)], (cue("anxious", "worry") - .1, tick(.05), 0),
      (cue("avoid", "No couple photo") - .2, pop(.12), .2), (cue("avoid", "No couple photo") + .4, pop(.12), .2),
      (cue("point", "Sometimes") - .2, thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
