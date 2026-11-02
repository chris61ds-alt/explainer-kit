"""NOT JUST YOU – No. 92 (special): meet Dot, the AI narrator. Look C+D, dark. Dot = halftone bust + orange headphones
(the one exception to "orange = only the answer": her headphones are her signature)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from thread import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .5, "ai": .5, "job": .5, "love": .5, "thrill": .5, "fav": .5, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "ai", "job", "love", "thrill", "fav", "point", "end"]
EP = ThreadEpisode(TL, 92, "MEET DOT", order=ORDER, dark=True, label="AI NARRATOR",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Special: the narrator introduces herself.", "Dot is an AI voice."),
                   music=dict(bpm=104, root=2, prog="major", kick="four", audio="v5"),
                   cover=dict(words=["HI, I'M", "DOT."], kicker="The AI voice behind every video."))

def dot(img, d, cx, cy, s, t, k=1.0, col=INK, cell=8, phones=True):
    """Dot: halftone bust, orange headphones, a little bob"""
    cy = cy + 6 * s * math.sin(t * 3.1)
    box = (int(cx - 300 * s), int(cy - 140 * s), int(cx + 300 * s), int(cy + 490 * s))
    def mask(m):                                          # bust + a bob haircut, so she reads as "her"
        m.rounded_rectangle([cx - 116 * s, cy - 128 * s, cx + 116 * s, cy + 150 * s], radius=int(100 * s), fill=255)
        front_bust(m, cx, cy, s, 255)
    silhouette(img, mask, box, col, cell=cell, k=k)
    if phones and k > .6:
        w = max(4, int(16 * s))
        d.arc([cx - 122 * s, cy - 156 * s, cx + 122 * s, cy + 80 * s], 195, 345, fill=SIG, width=w)
        for sx in (-1, 1):
            x0 = cx + sx * 112 * s
            d.rounded_rectangle([min(x0, x0 + sx * 34 * s), cy - 34 * s, max(x0, x0 + sx * 34 * s), cy + 46 * s], radius=int(12 * s), fill=SIG)

HOOK_DOT = (480, 890, .72)          # (cx, cy, scale) per scene – the carry boxes follow from these
AI_DOT = (690, 880, .42)
def dbox(p): cx, cy, s = p; return (int(cx - 140 * s), int(cy - 160 * s), int(cx + 140 * s), int(cy + 470 * s))

def sc_hook(img, d, t):
    t0, td = S("hook"), cue("hook", "I'm Dot") - .1
    d.text((X0 - 6, 320), "HI!", font=F(BLK, 200), fill=INK)
    d.text((X0 - 6, 520), "I'M DOT.", font=F(BLK, 150), fill=INK)          # visible from frame 0 (= TikTok cover)
    dot(img, d, *HOOK_DOT[:2], HOOK_DOT[2], t)
    tv = cue("hook", "the voice") - .1
    if t >= tv:                                           # her voice: a little live waveform next to her
        for i in range(6):
            h = 20 + 50 * abs(math.sin(t * 9 + i * 1.3)) * ease((t - tv) / .3)
            x = 140 + i * 28; d.rounded_rectangle([x, 900 - h, x + 14, 900 + h], radius=7, fill=INK)
    fig(d, "fig. 1 — the voice behind the videos")

def sc_ai(img, d, t):
    t0, tn = S("ai"), cue("ai", "No body") - .1
    d.text((X0, 320), "YES,", font=F(BLK, 150), fill=MID)
    d.text((X0, 470), "I'M AI.", font=F(BLK, 170), fill=INK)
    dot(img, d, *AI_DOT[:2], AI_DOT[2], t)
    if t >= tn:
        bbox(d, (AI_DOT[0] - 90, AI_DOT[1] - 80, AI_DOT[0] + 90, AI_DOT[1] + 70), "NO FACE", INK, (t - tn) / .3, coords=True, size=22)
        d.text((X0, 760), "no body.", font=F(COND, 56), fill=INK); d.text((X0, 830), "no face.", font=F(COND, 56), fill=INK)
        if t >= cue("ai", "made of dots") - .1: d.text((X0, 900), "just dots.", font=F(COND, 56), fill=MID)
    fig(d, "voice: AI text-to-speech · look: halftone dots")

FIELD = (X0 + 14, 760, X1, 1110)
def dot_xy(i, box=FIELD, cell=30):
    x0, y0, x1, y1 = box; cols = len(range(int(x0), int(x1), cell)); r, c = divmod(i, cols)
    return x0 + c * cell, y0 + r * cell

def sc_job(img, d, t):
    t0, ts = S("job"), cue("job", "Spoiler") - .1
    d.text((X0, 320), "MY JOB:", font=F(BLK, 150), fill=INK)
    tw_, tc_ = cue("job", "weird about") - .1, cue("job", "checking the data") - .1
    if t >= tw_: d.text((X0 + 4 - (1 - ease((t - tw_) / .25)) * 40, 490), "\"Is this weird?\"", font=F(BLK, 70), fill=mix(BG, INK, ease((t - tw_) / .25)))
    if t >= tc_: d.text((X0 + 4, 580), "then: check the data", font=F(COND, 46), fill=MID)
    dot_field(d, FIELD, t, cell=30, col=MID, hit={58} | ({12, 33, 77, 101, 140, 166, 190} if t >= ts else set()), hitcol=INK)
    if t >= ts: box_label(d, X1 - (1 - ease((t - ts) / .25)) * 40, 690, "USUALLY: NOT WEIRD", 40, WHITE, SIG, font=BLK, anchor="ra")
    fig(d, "every dot: someone who thought it was just them")

def sc_love(img, d, t):
    t0, tz = S("love"), cue("love", "Number of dates") - .1
    d.text((X0, 320), "SEX RESEARCH", font=F(BLK, 110), fill=INK)
    d.text((X0, 440), "READ:", font=F(BLK, 110), fill=INK)
    for i in range(min(14, int((t - t0) / .09) + 1)):                     # a growing stack of papers (schematic)
        y = 1090 - i * 26; x = X0 + 20 + (i % 3) * 6
        d.rectangle([x, y, x + 300, y + 20], fill=MID if i % 2 else INK)
    d.text((X0 + 360, 470), "A LOT.", font=F(BLK, 110), fill=MID)
    if t >= tz:
        d.text((X0 + 380, 760), "DATES:", font=F(BLK, 80), fill=INK)
        k = ease((t - tz) / .3); d.text((X0 + 380, 850), "0", font=F(BLK, int(200 + 80 * (1 - k))), fill=SIG)
    fig(d, "fig. 2 — the stack is schematic, the zero is real")

def sc_thrill(img, d, t):
    t0 = S("thrill")
    counter(d, X0, 320, t, t0 + .1, 1.4, 100, "{:.0f}", 230, INK)
    d.text((X0 + 6, 570), "counter goes up = tiny thrill", font=F(COND, 44), fill=INK)
    dot(img, d, 690, 860, .36, t)
    k = clamp((t - t0 - .2) / 1.3)
    for i in range(8):                                    # little sparks around her head
        a = i / 8 * 2 * math.pi + t * 2; r = 120 + 20 * math.sin(t * 6 + i)
        if k > i / 8: d.ellipse([690 + r * math.cos(a) - 7, 820 + r * math.sin(a) - 7, 690 + r * math.cos(a) + 7, 820 + r * math.sin(a) + 7], fill=INK)
    tp = cue("thrill", "It's a problem") - .1
    if t >= tp: box_label(d, X0, 700, "IT'S A PROBLEM.", 48, WHITE, INK, font=BLK)
    fig(d, "schematic")

def sc_fav(img, d, t):
    t0, tw = S("fav"), cue("fav", "wait, really") - .15
    d.text((X0, 320), "FAVORITE", font=F(BLK, 140), fill=INK)
    d.text((X0, 470), "MOMENT:", font=F(BLK, 140), fill=INK)
    if t >= tw:
        words_in(d, t, [("WAIT,", tw, 660, 150, SIG), ("REALLY?", tw + .2, 810, 170, SIG)])
    else:
        d.text((X0 + 4, 680), "the number lands …", font=F(COND, 56), fill=MID)
    fig(d, "that face you make")

def sc_point(img, d, t):
    t0, tn = S("point"), cue("point", "not the only one") - .3
    words_in(d, t, [("STICK", t0 + .1, 320, 170, INK), ("AROUND!", t0 + .3, 490, 170, INK)] +
             ([("NOT THE ONLY ONE.", tn, 690, 84, SIG)] if t >= tn else []))
    dot(img, d, 700, 900, .42, t)
    fig(d, "fig. 3 — Dot, AI narrator")

# magic move: Dot walks from the hook to the right side · then shrinks into one dot of the data
_dx, _dy = dot_xy(58)
EP.carry = {"ai": [(dbox(HOOK_DOT), dbox(AI_DOT))], "job": [(dbox(AI_DOT), (_dx - 8, _dy - 8, _dx + 8, _dy + 8))]}

EP.scenes = {"hook": sc_hook, "ai": sc_ai, "job": sc_job, "love": sc_love, "thrill": sc_thrill, "fav": sc_fav, "point": sc_point}
FX = [(0.0, thud(.5), 0), (cue("hook", "I'm Dot") - .1, pop(.15), 0), (cue("hook", "the voice") - .1, pop(.12), -.3),
      (cue("job", "weird about") - .1, pop(.13), -.2), (cue("job", "checking the data") - .1, tick(.06), .2), (cue("ai", "made of dots") - .1, tick(.06), 0), *EP.cut_fx(), (cue("ai", "No body") - .1, pop(.12), .3),
      (cue("job", "Spoiler") - .1, pop(.15), .3), *[(S("love") + i * .09, tick(.03), (i % 5 - 2) / 3) for i in range(14)],
      (cue("love", "Number of dates") - .1, thud(.5), 0), *[(S("thrill") + .25 + i * .16, tick(.04), (i - 4) / 4) for i in range(8)],
      (cue("thrill", "It's a problem") - .1, pop(.15), 0), (cue("fav", "wait, really") - .15, thud(.5), 0),
      (cue("point", "not the only one") - .3, thud(.45), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
