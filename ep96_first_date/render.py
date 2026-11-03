"""NOT JUST YOU – No. 96 (tips format test): 3 first-date tips from research – follow-up questions (Huang et al. 2017),
deep talk (Kardas, Kumar & Epley 2022), be picky (Eastwick et al. 2007). Look C+D, dark · two fixed figures: YOU + DATE."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from thread import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "tip1": .5, "tip2": .5, "tip3": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "tip1", "tip2", "tip3", "point", "end"]          # opener: "BE HONEST" question to the viewer (toolkit)
EP = ThreadEpisode(TL, 96, "FIRST DATE", order=ORDER, dark=True, label="DATING · 3 STUDIES",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Huang et al. (2017) JPSP · Kardas, Kumar &", "Epley (2022) JPSP · Eastwick et al. (2007) Psych. Sci."),
                   music=dict(bpm=104, root=2, prog="major", kick="four", audio="v5"),
                   cover=dict(words=["3 FIRST-DATE", "TIPS FROM", "SCIENCE."], kicker="Save this for your next date."))

YOU, DATE, BS = (290, 950), (670, 950), .34                     # the two fixed figures
COUPLE = (110, 820, 860, 1135)
def bust_box(x, y, s): return (int(x - 160 * s / .32), int(y - 110 * s / .32), int(x + 160 * s / .32), int(y + 160 * s / .32))
def couple(img, d, k=1.0, date_col=MID, labels=False):
    silhouette(img, lambda m: front_bust(m, *YOU, BS, 255), bust_box(*YOU, BS), INK, cell=8, k=k)
    silhouette(img, lambda m: front_bust(m, *DATE, BS, 255), bust_box(*DATE, BS), date_col, cell=8, k=k)
    if k > .6 and labels:
        d.text((YOU[0], 1104), "YOU", font=F(BLK, 26), fill=INK, anchor="ma"); d.text((DATE[0], 1104), "DATE", font=F(BLK, 26), fill=date_col, anchor="ma")

def bubble(d, who, text, k, col=INK, y=700, size=34):
    """speech bubble above YOU or DATE, pops in with k"""
    if k <= 0: return None
    f = F(BLK, size); w = d.textlength(text, font=f) + 44; h = size + 30; sx = (YOU if who == "you" else DATE)[0]
    x0 = min(max(X0, sx - w / 2), X1 - w); s = back(clamp(k)); cx, cy = x0 + w / 2, y + h / 2
    d.rounded_rectangle([cx - w / 2 * s, cy - h / 2 * s, cx + w / 2 * s, cy + h / 2 * s], radius=int(h / 2 * s), fill=col)
    d.polygon([(sx - 14 * s, y + h * s - 2), (sx + 14 * s, y + h * s - 2), (sx, y + h * s + 26 * s)], fill=col)
    if s > .6: d.text((cx, cy), text, font=F(BLK, int(size * min(1, s))), fill=BG, anchor="mm")
    return (x0, y, x0 + w, y + h)

def heart(d, cx, cy, r, col):
    d.ellipse([cx - r, cy - r * .9, cx, cy + r * .1], fill=col); d.ellipse([cx, cy - r * .9, cx + r, cy + r * .1], fill=col)
    d.polygon([(cx - r * .97, cy - r * .25), (cx + r * .97, cy - r * .25), (cx, cy + r * 1.05)], fill=col)

def tip_head(d, t, n, lines, t0):
    box_label(d, X0, 300, f"TIP {n}", 40, WHITE, INK, font=BLK)
    words_in(d, t, [(l, t0 + .1 + i * .15, 370 + i * 100, 100, INK) for i, l in enumerate(lines)])

def sc_hook(img, d, t):
    t0, ts = S("hook"), cue("hook", "Save this") - .1
    words_in(d, t, [("3 TIPS.", t0 + .05, 320, 210, INK)])
    tb = cue("hook", "backed by") - .1
    if t >= tb: d.text((X0 + 4 - (1 - ease((t - tb) / .25)) * 40, 560), "backed by research", font=F(COND, 54), fill=mix(BG, INK, ease((t - tb) / .25)))
    if t >= ts:                                            # bookmark = save
        k = back(clamp((t - ts) / .3)); bx, by = X1 - 40, 420
        d.polygon([(bx - 50 * k, by - 70 * k), (bx + 50 * k, by - 70 * k), (bx + 50 * k, by + 70 * k), (bx, by + 35 * k), (bx - 50 * k, by + 70 * k)], fill=INK)
        if k > .7: d.text((bx, by + 100), "SAVE", font=F(BLK, 30), fill=INK, anchor="ma")
    couple(img, d, clamp((t - t0 - .3) / .5), labels=True)
    fig(d, "fig. 1 — you and your date, schematic")

def sc_tip1(img, d, t):
    t0 = S("tip1"); tip_head(d, t, 1, ["ASK", "FOLLOW-UPS."], t0)
    t1, t2, t3, tr = cue("tip1", "In a speed") - .1, cue("tip1", "speed-dating study") + .3, cue("tip1", "asked more") - .1, cue("tip1", "more second") - .1
    couple(img, d, labels=True)
    if t < t3: bubble(d, "you", "Where are you from?", (t - t1) / .3)
    if t2 <= t < t3 + .9: bubble(d, "date", "Lisbon!", (t - t2) / .3, col=MID, y=620)
    if t >= t3:
        b = bubble(d, "you", "Oh, why did you move?", (t - t3) / .3)
        if b and t >= t3 + .25: box_label(d, b[2], b[1] - 52, "FOLLOW-UP", 30, WHITE, INK, font=BLK, anchor="ra")
    if t >= tr: box_label(d, X1 - (1 - ease((t - tr) / .25)) * 50, 600, "MORE 2ND DATES", 46, WHITE, SIG, font=BLK, anchor="ra")
    fig(d, "110 speed daters · 1,961 dates · a link, not proof")

def sc_tip2(img, d, t):
    t0 = S("tip2"); tip_head(d, t, 2, ["SKIP THE", "SMALL TALK."], t0)
    couple(img, d)
    ts_, tt, te, tn, tc = cue("tip2", "small talk") + .2, cue("tip2", "In twelve") - .1, cue("tip2", "expected deep") - .1, cue("tip2", "They didn't") - .1, cue("tip2", "more connected") - .1
    if t < tt:
        b = bubble(d, "you", "So… nice weather?", (t - t0 - .15) / .3, col=MID)
        if b and t >= ts_: d.line([b[0] - 8, (b[1] + b[3]) / 2, lerp(b[0] - 8, b[2] + 8, ease((t - ts_) / .2)), (b[1] + b[3]) / 2], fill=INK, width=8)
    else: bubble(d, "you", "What matters most to you?", (t - tt) / .3)
    if t >= te:                                            # awkwardness: expected vs. actual (schematic)
        k = ease((t - te) / .4); d.text((X1 - 560, 596), "EXPECTED AWKWARD", font=F(BLK, 26), fill=MID)
        d.rectangle([X1 - 270, 598, X1 - 270 + 270 * k, 626], fill=MID)
    if t >= tn:
        k = ease((t - tn) / .4); d.text((X1 - 560, 640), "ACTUAL", font=F(BLK, 26), fill=SIG)
        d.rectangle([X1 - 270, 642, X1 - 270 + 100 * k, 670], fill=SIG)
    if t >= tc:                                            # connection: a line grows between the two
        k = ease((t - tc) / .5); y = 1000
        d.line([YOU[0] + 110, y, lerp(YOU[0] + 110, DATE[0] - 110, k), y], fill=SIG, width=10)
        if k >= 1: heart(d, (YOU[0] + DATE[0]) / 2, y - 6, 26 + 4 * math.sin(t * 8), SIG)
    fig(d, "12 experiments · 1,800+ people · bars schematic")

DATES = [(440 + i * 105, 960) for i in range(5)]
ME = (200, 950)
def sc_tip3(img, d, t):
    t0 = S("tip3"); box_label(d, X0, 300, "TIP 3", 40, WHITE, INK, font=BLK)
    words_in(d, t, [("BE PICKY.", t0 + .05, 380, 170, INK)])
    ta, tr, to, tb = cue("tip3", "liked everyone") - .1, cue("tip3", "got rejected") - .1, cue("tip3", "if you liked one") - .1, cue("tip3", "They liked you back") - .1
    silhouette(img, lambda m: front_bust(m, *ME, .3, 255), bust_box(*ME, .3), INK, cell=8)
    d.text((ME[0], 1104), "YOU", font=F(BLK, 26), fill=INK, anchor="ma")
    for i, (x, y) in enumerate(DATES):
        silhouette(img, lambda m, x=x, y=y: front_bust(m, x, y, .15, 255), bust_box(x, y, .15), MID, cell=5)
        if ta <= t < to and t >= ta + i * .1: heart(d, x, y - 95, 16, INK)          # hearts for everyone …
        if tr <= t < to: d.line([x - 34, y - 40, x + 34, y + 40], fill=INK, width=7); d.line([x - 34, y + 40, x + 34, y - 40], fill=INK, width=7)
    if tr <= t < to: box_label(d, X1, 620, "REJECTED", 46, WHITE, INK, font=BLK, anchor="ra")
    if t >= to:                                            # … vs. one heart for one person
        x, y = DATES[2]; heart(d, x, y - 95, 20 + 3 * math.sin(t * 8), INK)
    if t >= tb:
        k = ease_io((t - tb) / .6); x, y = DATES[2]
        heart(d, lerp(x, ME[0] + 60, k), lerp(y - 95, ME[1] - 150, k) - 80 * math.sin(math.pi * k), 26, SIG)
        if k >= 1: box_label(d, X1, 620, "LIKED BACK", 46, WHITE, SIG, font=BLK, anchor="ra")
    fig(d, "156 speed daters · Eastwick et al. 2007")

def sc_point(img, d, t):
    t0, tp = S("point"), cue("point", "be picky") - .2
    words_in(d, t, [("ASK MORE.", t0 + .1, 320, 120, INK), ("GO DEEPER.", cue("point", "Go deeper") - .15, 445, 120, INK)] +
             ([("BE PICKY.", tp, 570, 120, SIG)] if t >= tp else []))
    couple(img, d)
    heart(d, (YOU[0] + DATE[0]) / 2, 960, 30 + 4 * math.sin(t * 8), INK)
    fig(d, "fig. 2 — save it for your next date")

# magic move: the couple stays put while the rest of the scene slides · tip 1 → 2 → 3 change on the spot
EP.carry = {"tip1": [(COUPLE, COUPLE)], "point": [((70, 800, 300, 1135), COUPLE)]}
EP.cuts = {"tip2": "stay", "tip3": "stay"}

EP.scenes = {"hook": sc_hook, "tip1": sc_tip1, "tip2": sc_tip2, "tip3": sc_tip3, "point": sc_point}
FX = [*EP.cut_fx(), (S("hook") + .05, thud(.45), 0), (cue("hook", "backed by") - .1, tick(.06), 0), (S("hook") + .3, whoosh(.4, .04), 0),
      (cue("hook", "Save this") - .1, pop(.15), .3),
      (S("tip1") + .1, pop(.12), -.3), (cue("tip1", "In a speed") - .1, pop(.12), -.2), (cue("tip1", "speed-dating study") + .3, pop(.12), .3),
      (cue("tip1", "asked more") - .1, pop(.14), -.2), (cue("tip1", "more second") - .1, thud(.5), .3),
      (S("tip2") + .1, pop(.12), -.3), (cue("tip2", "small talk") + .2, whoosh(.2, .05), 0), (cue("tip2", "In twelve") - .1, pop(.13), -.2),
      (cue("tip2", "expected deep") - .1, tick(.06), .2), (cue("tip2", "They didn't") - .1, thud(.45), .2), (cue("tip2", "more connected") - .1, riser(.5, .04), 0),
      (S("tip3") + .1, thud(.4), 0), *[(cue("tip3", "liked everyone") - .1 + i * .1, tick(.04), (i - 2) / 3) for i in range(5)],
      (cue("tip3", "got rejected") - .1, thud(.45), 0), (cue("tip3", "if you liked one") - .1, pop(.14), .2),
      (cue("tip3", "They liked you back") - .1, whoosh(.5, .05), 0), (cue("tip3", "They liked you back") + .5, pop(.16), -.3),
      (S("point") + .1, pop(.12), 0), (cue("point", "Go deeper") - .15, pop(.12), 0), (cue("point", "be picky") - .2, thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
