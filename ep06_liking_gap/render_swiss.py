"""NOT JUST YOU – No. 06: the liking gap — look E 'Swiss Detail'.
Swiss editorial grid, giant type, one signal colour (orange), Aicher-style pictograms with poses,
line-art props, numbered chapters, annotations, progress rule. Same narration as render.py."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cute
from cute import F, BLK, BOLD, MONO, clamp, ease, ease_io, back, lerp, mix, Timeline, W, H, SAFE_R
from cute import whoosh, pop
import render as clean                      # reuse narration timeline, music bed + sfx of the Clean Pop cut
from PIL import Image

COND = "Roboto-Condensed-Bold.woff"; MED = "Roboto-Medium.woff"
BG = (250, 250, 248); INK = (12, 12, 12); SIG = (255, 64, 0); RULE = (226, 226, 222); MID = (140, 140, 136)
SIG_L = (255, 222, 208); WHITE = (255, 255, 255)
cute.BG, cute.INK = BG, INK
cute.build_audio = clean.build_audio

TL = clean.TL; S, E, cue = TL.S, TL.E, TL.cue
ORDER = clean.ORDER
CH = {"hook": ("01", "THE REPLAY"), "replay": ("02", "EVERY SECOND"), "study": ("03", "THE STUDY"), "q": ("04", "TWO QUESTIONS"),
      "gap": ("05", "THE RESULT"), "name": ("06", "THE NAME"), "why": ("07", "WHY"), "months": ("08", "IT LASTS"), "point": ("09", "PLAY IT AGAIN")}
X0, X1, Y0, Y1 = 60, 900, 300, 1170

# ---------------------------------------------------------------- Aicher-style pictogram
def seg(d, a, b, w, col):
    d.line([a, b], fill=col, width=int(w)); r = w / 2
    for p in (a, b): d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=col)

def picto(d, x, y, s=1.0, col=INK, f=1, tilt=0.0, arms=((10, 5), (-10, -5)), legs=((4, 0), (-4, 0)), head_dy=0.0):
    """(x, y) = feet line. angles in degrees from straight down, positive = towards facing direction f.
    arms: ((upper, fore) front arm, (upper, fore) back arm). legs likewise."""
    L_leg, L_t, L_u, L_f = 70 * s, 130 * s, 62 * s, 58 * s
    def v(a, L): r = math.radians(a); return (math.sin(r) * f * L, math.cos(r) * L)
    hip = (x, y - 2 * L_leg)
    for (a1, a2) in legs:
        k = (hip[0] + v(a1, L_leg)[0], hip[1] + v(a1, L_leg)[1]); ft = (k[0] + v(a2, L_leg)[0], k[1] + v(a2, L_leg)[1])
        seg(d, hip, k, 42 * s, col); seg(d, k, ft, 42 * s, col)
    tr = math.radians(tilt); neck = (hip[0] + math.sin(tr) * f * L_t, hip[1] - math.cos(tr) * L_t)
    seg(d, hip, neck, 66 * s, col)
    sh = (neck[0], neck[1] + 14 * s)
    for (a1, a2) in arms:
        e = (sh[0] + v(a1, L_u)[0], sh[1] + v(a1, L_u)[1]); h = (e[0] + v(a2, L_f)[0], e[1] + v(a2, L_f)[1])
        seg(d, sh, e, 36 * s, col); seg(d, e, h, 36 * s, col)
    hc = (neck[0] + math.sin(tr) * f * 82 * s, neck[1] - 82 * s + head_dy * s)
    d.ellipse([hc[0] - 42 * s, hc[1] - 42 * s, hc[0] + 42 * s, hc[1] + 42 * s], fill=col)
    return hc

def talk(t, ph=0.0): a = math.sin(t * 5 + ph); return ((60 + 22 * a, 110 + 25 * a), (-12, -6))
WORRY = ((165, 250), (-15, -5))          # hand to the head
def wave(t): return ((125, 165 + 30 * math.sin(t * 9)), (-10, -5))
LAUGH = ((40, 120), (-30, -60))

# ---------------------------------------------------------------- line-art props + chrome
def cup(d, x, y, t, s=1.0, steam=True):
    d.rectangle([x - 22 * s, y - 44 * s, x + 22 * s, y], outline=INK, width=int(6 * s))
    d.arc([x + 12 * s, y - 36 * s, x + 40 * s, y - 12 * s], 270, 90, fill=INK, width=int(6 * s))
    if steam:
        for i in (-1, 1):
            pts = [(x + i * 8 * s + 6 * s * math.sin(t * 4 + j * .7 + i), y - 56 * s - j * 10 * s) for j in range(6)]
            d.line(pts, fill=MID, width=int(4 * s))

def table(d, cx, y, w=380):
    d.line([cx - w / 2, y, cx + w / 2, y], fill=INK, width=10); d.line([cx, y, cx, y + 160], fill=INK, width=10)
    d.line([cx - 70, y + 160, cx + 70, y + 160], fill=INK, width=10)

def cross(d, x, y, r=12): d.line([x - r, y, x + r, y], fill=INK, width=2); d.line([x, y - r, x, y + r], fill=INK, width=2)

def note(d, x, y, tx, ty, text, k=1.0, col=INK, anchor="la"):
    """annotation with leader line from (x, y) to the text at (tx, ty)"""
    if k <= 0: return
    e = ease(k); ex, ey = lerp(x, tx, e), lerp(y, ty, e)
    d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=col); d.line([x, y, ex, ey], fill=col, width=3)
    if k > .9: d.text((tx + (10 if anchor == "la" else -10), ty), text, font=F(COND, 28), fill=col, anchor="lm" if anchor == "la" else "rm")

def box_label(d, x, y, text, size, fg=WHITE, bg=INK, font=COND, anchor="la"):
    f = F(font, size); w = d.textlength(text, font=f)
    if anchor == "ma": x -= w / 2
    if anchor == "ra": x -= w
    d.rectangle([x - 10, y - 4, x + w + 10, y + size + 8], fill=bg); d.text((x, y), text, font=f, fill=fg)

def grid(d):
    for x in range(X0, X1 + 1, 140): d.line([x, 280, x, Y1], fill=RULE, width=2)
    for (x, y) in ((X0, Y1), (X1, Y1)): cross(d, x, y)

def chrome(d, t, cur):
    d.text((X0, 212), "NOT JUST YOU", font=F(COND, 34), fill=INK)
    d.text((X1, 212), "06 / THE LIKING GAP", font=F(COND, 34), fill=INK, anchor="ra")
    d.line([X0, 262, X1, 262], fill=INK, width=4)
    d.line([X0, 262, X0 + (X1 - X0) * clamp(t / S("end")), 262], fill=SIG, width=8)   # progress rule
    if cur in CH:
        no, title = CH[cur]
        d.text((X0, 274), no, font=F(COND, 26), fill=SIG); d.text((X0 + 44, 274), title, font=F(COND, 26), fill=INK)
    d.line([X0, 1188, X1, 1188], fill=INK, width=4)

def subtitle(d, t, y0=1206):
    cur = TL.current(t) or "hook"
    if cur == "end": return
    b = TL.T[cur]
    if t > b["start"] + b["dur"] + .4: return
    f = F(BLK, 62); lines, curl = [], ""
    for w_ in b["text"].split():
        tst = (curl + " " + w_).strip()
        if d.textlength(tst, font=f) <= X1 - X0: curl = tst
        else: lines.append(curl); curl = w_
    lines.append(curl)
    shown = (t - b["start"]) / b["dur"] * len(b["text"]); c = 0
    for li, line in enumerate(lines[:4]):
        x = X0
        for w_ in line.split(" "):
            now = c <= shown < c + len(w_) + 1
            d.text((x, y0 + li * 72), w_, font=f, fill=SIG if now else (INK if c <= shown else RULE))
            x += d.textlength(w_ + " ", font=f); c += len(w_) + 1

# ---------------------------------------------------------------- scenes
def cafe(d, t, talking=True, partner_pose=None, you_pose=None):
    table(d, 480, 880, 360)
    cup(d, 400, 876, t); cup(d, 560, 876, t + 1.3)
    ya = you_pose or (talk(t) if talking and int(t * 1.2) % 2 == 0 else ((15, 40), (-10, -5)))
    pa = partner_pose or (talk(t, 1.0) if talking and int(t * 1.2) % 2 == 1 else ((15, 40), (-10, -5)))
    hy = picto(d, 230, 1128, 1.0, INK, f=1, arms=ya)
    hp = picto(d, 730, 1128, 1.0, SIG, f=-1, arms=pa)
    return hy, hp

def speech_box(d, x, y, w, k, col=INK, side=1, txt="· · ·"):
    if k <= 0: return
    e = ease(k); ww = w * e
    x0 = x if side > 0 else x - ww
    d.rectangle([x0, y, x0 + ww, y + 70], fill=col)
    tx = x + 24 * side; d.polygon([(tx, y + 70), (tx + 24 * side, y + 70), (tx, y + 96)], fill=col)
    if e > .9: d.text((x0 + ww / 2, y + 35), txt, font=F(BLK, 36), fill=WHITE, anchor="mm")

def sc_hook(img, d, t):
    k = ease(t / .25)
    d.text((X0 - 8, 300), "REPLAY", font=F(BLK, 230), fill=INK)
    # rewind glyph + reversed timecode (mono)
    if int(t * 3) % 2 == 0:
        for o in (0, 1): x = 805 + o * 46; d.polygon([(x + 23, 590), (x + 23, 640), (x - 23, 615)], fill=SIG)
    secs = max(0, 300 - t * 31)
    d.text((X0, 600), "00:%02d:%02d" % (secs // 60, secs % 60), font=F(MONO, 34), fill=INK)
    hy, hp = cafe(d, t)
    speech_box(d, 120, 690, 200, (t - .2) / .25, INK, 1)
    q = cue("hook", "here's")
    if t < q: speech_box(d, 840, 720, 200, (t - .5) / .25, SIG, -1)
    else:
        kk = back((t - q) / .35)
        if kk > .05:
            d.rectangle([hp[0] - 80 * kk, 660 - 80 * kk, hp[0] + 80 * kk, 660 + 80 * kk], fill=SIG)
            d.text((hp[0], 660), "?", font=F(BLK, int(130 * kk)), fill=WHITE, anchor="mm")
        note(d, hp[0] - 90, 690, 520, 680, "what did they think?", (t - q - .4) / .4, anchor="ra")
    d.text((X0, 1146), "fig. 1 — a normal conversation", font=F(MED, 22), fill=MID)

def ruler(d, y, x0, x1, labels):
    d.line([x0, y, x1, y], fill=INK, width=3)
    for i in range(0, 61):
        x = x0 + (x1 - x0) * i / 60; h = 18 if i % 12 == 0 else 8
        d.line([x, y, x, y + h], fill=INK, width=2)
        if i % 12 == 0: d.text((x, y + 26), labels[i // 12], font=F(MONO, 20), fill=MID, anchor="ma")

def sc_replay(img, d, t):
    t0 = S("replay"); x0, x1, y = X0, X1, 760
    d.text((X0 - 6, 300), "AGAIN.", font=F(BLK, 220), fill=INK)
    loops = 1 + int(max(0, t - t0) / 1.1)
    d.text((X1, 560), f"replay no. {loops}", font=F(MONO, 26), fill=SIG, anchor="ra")
    pause = (.36, .48); weird = .74; prog = clamp((t - t0) / 3.2)
    for i in range(120):
        u = i / 119; x = x0 + (x1 - x0) * u
        a = 0 if pause[0] < u < pause[1] else (20 + 80 * abs(math.sin(i * 1.7) * math.sin(i * .43)))
        d.rectangle([x - 2.5, y - a - 2, x + 2.5, y + a + 2], fill=INK if u < prog else RULE)
    ruler(d, y + 130, x0, x1, ["0:00", "1:00", "2:00", "3:00", "4:00", "5:00"])
    hx = x0 + (x1 - x0) * prog
    d.line([hx, y - 140, hx, y + 120], fill=SIG, width=5); d.polygon([(hx - 14, y - 160), (hx + 14, y - 160), (hx, y - 138)], fill=SIG)
    # dimension line over the pause
    if t >= cue("replay", "awkward"):
        k = ease((t - cue("replay", "awkward")) / .4)
        a, b = x0 + (x1 - x0) * pause[0], x0 + (x1 - x0) * pause[1]
        d.line([a, y - 70, a + (b - a) * k, y - 70], fill=SIG, width=4); d.line([a, y - 86, a, y - 54], fill=SIG, width=4)
        if k > .95: d.line([b, y - 86, b, y - 54], fill=SIG, width=4); box_label(d, (a + b) / 2, y - 140, "AWKWARD PAUSE", 28, WHITE, SIG, anchor="ma")
    if t >= cue("replay", "weird"):
        wx = x0 + (x1 - x0) * weird
        note(d, wx, y + 20, wx - 40, y + 260, "why did I say that?", (t - cue("replay", "weird")) / .4, SIG, anchor="ra")
    d.text((X0, 1146), "fig. 2 — your memory of it", font=F(MED, 22), fill=MID)

def sc_study(img, d, t):
    t0 = S("study"); k = clamp((t - cue("study", "five")) / 2.2); rem = int(300 * (1 - k))
    d.text((X0 - 6, 290), "%d:%02d" % (rem // 60, rem % 60), font=F(BLK, 250), fill=SIG)
    d.text((X0, 560), "minutes, strangers, icebreakers", font=F(COND, 34), fill=INK)
    for i, q in enumerate(("Where are you from?", "What are your hobbies?")):
        kk = ease((t - t0 - .4 - i * .4) / .35)
        if kk > 0:
            x = X1 - (300 + i * 40) * kk
            d.rectangle([x, 640 + i * 84, x + 300, 700 + i * 84], outline=INK, width=3)
            d.text((x + 150, 670 + i * 84), q, font=F(COND, 26), fill=INK, anchor="mm")
    table(d, 480, 900, 300)
    picto(d, 250, 1128, .9, INK, f=1, arms=talk(t)); picto(d, 710, 1128, .9, SIG, f=-1, arms=talk(t, 2))
    if t >= cue("study", "two questions"):
        kk = back((t - cue("study", "two questions")) / .3)
        d.rectangle([380, 640, 380 + 70 * kk, 640 + 70 * kk], fill=INK)
        if kk > .7: d.text((415, 675), "2", font=F(BLK, 52), fill=WHITE, anchor="mm")
    d.text((X0, 1146), "Boothby, Cooney, Sandstrom & Clark — Psychological Science, 2018", font=F(MED, 22), fill=MID)

def scale7(d, x, y, sel, k, col):
    for i in range(7):
        bx = x + i * 112
        fill = col if (i + 1) <= sel * k else None
        d.rectangle([bx, y, bx + 92, y + 92], outline=INK, width=4, fill=fill)
        d.text((bx + 46, y + 46), str(i + 1), font=F(COND, 34), fill=WHITE if fill else INK, anchor="mm")

def sc_q(img, d, t):
    t0 = S("q"); q2 = cue("q", "and how much")
    for i, (no, txt, t_in, sel, col) in enumerate((("Q1", "How much did you like them?", t0, 6, INK), ("Q2", "How much do you think they liked you?", q2, 4, SIG))):
        k = ease((t - t_in) / .35)
        if k <= 0: continue
        y = 330 + i * 400
        d.text((X0, y), no, font=F(BLK, 120), fill=col)
        for li, l in enumerate(("How much did you" if i == 0 else "How much do you think", "like them?" if i == 0 else "they liked you?")):
            d.text((X0 + 180, y + 10 + li * 54), l, font=F(BLK, 48), fill=INK)
        scale7(d, X0, y + 170, sel, ease((t - t_in - .7) / .6), col)
        d.text((X0, y + 280), "not at all", font=F(MONO, 20), fill=MID); d.text((X1 - 40, y + 280), "very much", font=F(MONO, 20), fill=MID, anchor="ra")

def sc_gap(img, d, t):
    t0 = S("gap")
    d.text((X0 - 10, 290), "MORE", font=F(BLK, 300), fill=SIG)
    d.text((X0, 620), "than they thought.", font=F(BLK, 62), fill=INK)
    for i, (v, c, lab, dl) in enumerate(((.86, INK, "They liked you", .2), (.58, SIG, "You thought they liked you", .5))):
        y = 760 + i * 170; k = ease((t - t0 - dl) / .6)
        d.rectangle([X0, y, X0 + (X1 - X0) * v * k, y + 90], fill=c)
        d.text((X0, y + 102), lab, font=F(COND, 28), fill=INK)
    for i in range(8):
        x = X0 + (X1 - X0) * i / 7; d.line([x, 1080, x, 1094], fill=INK, width=2)
    d.line([X0, 1080, X1, 1080], fill=INK, width=2)
    if t >= cue("gap", "more than"):
        k = ease((t - cue("gap", "more than")) / .4)
        a, b = X0 + (X1 - X0) * .58, X0 + (X1 - X0) * .86
        d.line([a, 1010, a + (b - a) * k, 1010], fill=SIG, width=4)
        if k > .95:
            for xx in (a, b): d.line([xx, 994, xx, 1026], fill=SIG, width=4)
            box_label(d, (a + b) / 2, 1030, "GAP", 26, WHITE, SIG, anchor="ma")
    d.text((X0, 1146), "schematic — average across participants", font=F(MED, 22), fill=MID)

def sc_name(img, d, t):
    d.text((X0, 320), "THE", font=F(BLK, 130), fill=INK)
    f = F(BLK, 230); split = ease_io((t - cue("name", "gap") + .1) / .6) * 170
    wl = d.textlength("LIK", font=f)
    if t >= S("name") + .25:
        d.text((480 - split / 2 - wl, 480), "LIK", font=f, fill=INK)
        d.text((480 + split / 2, 480), "ING", font=f, fill=INK)
    if split > 30:   # architect's dimension line inside the split
        a, b = 480 - split / 2 + 12, 480 + split / 2 - 12
        d.line([a, 640, b, 640], fill=SIG, width=4)
        d.polygon([(a, 640), (a + 16, 630), (a + 16, 650)], fill=SIG); d.polygon([(b, 640), (b - 16, 630), (b - 16, 650)], fill=SIG)
    if t >= cue("name", "gap"):
        k = ease((t - cue("name", "gap") - .3) / .35)
        if k > 0: d.text((X0 - 8 - (1 - k) * 100, 770), "GAP", font=F(BLK, 300), fill=SIG)
    d.text((X0, 1146), "Boothby et al., 2018", font=F(MED, 22), fill=MID)

def sc_why(img, d, t):
    t0 = S("why"); miss = cue("why", "miss")
    hy = picto(d, 230, 1128, 1.0, INK, f=1, arms=WORRY, head_dy=4 * math.sin(t * 3))
    hp = picto(d, 760, 1128, 1.0, SIG, f=-1, arms=LAUGH, tilt=-8 + 4 * math.sin(t * 8))
    # wall of self-criticism
    wall_x = 410
    for i, w_ in enumerate(("too much?", "boring?", "weird.", "ugh.", "why did I…")):
        k = ease((t - t0 - .15 - i * .2) / .3)
        if k > 0: box_label(d, X0 + 10, 330 + i * 76, w_, 34, WHITE, INK)
    k = ease((t - t0 - .9) / .4)
    if k > 0: d.line([wall_x, 330, wall_x, 330 + 560 * k], fill=INK, width=10)
    # their signals: dashed arrows that stop at the wall
    for i, lab in enumerate(("smile", "nod", "laugh")):
        y = 420 + i * 150; u = ((t - t0) * .8 + i * .33) % 1
        tip = lerp(hp[0] - 80, wall_x + 20, u)
        for xx in range(int(tip), int(hp[0] - 80), 30): d.line([xx, y, xx + 16, y], fill=SIG, width=6)
        d.polygon([(tip, y), (tip + 22, y - 14), (tip + 22, y + 14)], fill=SIG)
        d.text((hp[0] - 70, y - 44), lab, font=F(COND, 30), fill=SIG, anchor="ra")
    if t >= miss: box_label(d, wall_x + 20, 920, "BLOCKED", 30, WHITE, SIG)
    d.text((X0, 1146), "fig. 3 — attention on yourself", font=F(MED, 22), fill=MID)

def sc_months(img, d, t):
    t0 = S("months")
    d.text((X0 - 6, 290), "MONTHS.", font=F(BLK, 190), fill=INK)
    d.text((X0, 500), "First-year suite mates, Yale, n = 102", font=F(COND, 30), fill=INK)
    cols = [("SEP", .82, .56), ("OCT", .84, .6), ("DEC", .86, .63), ("FEB", .86, .66), ("MAY", .86, .84)]
    yb = 1040
    for i, (m, a, g) in enumerate(cols):
        x = X0 + 30 + i * 168; k = ease((t - t0 - .2 - i * .4) / .4)
        d.text((x + 44, yb + 20), m, font=F(COND, 30), fill=INK, anchor="ma")
        if k <= 0: continue
        d.rectangle([x, yb - 400 * a * k, x + 40, yb], fill=INK); d.rectangle([x + 48, yb - 400 * g * k, x + 88, yb], fill=SIG)
        if i < 4 and k > .95:
            ya, yg = yb - 400 * a, yb - 400 * g
            d.line([x + 100, ya, x + 100, yg], fill=SIG, width=3)
        if i == 4 and k > .95: box_label(d, x + 44, yb - 400 * a - 60, "CLOSED", 24, WHITE, SIG, anchor="ma")
    d.line([X0, yb, X1, yb], fill=INK, width=3)
    d.rectangle([X0, 1100, X0 + 22, 1122], fill=INK); d.text((X0 + 32, 1111), "they liked you", font=F(COND, 24), fill=INK, anchor="lm")
    d.rectangle([X0 + 250, 1100, X0 + 272, 1122], fill=SIG); d.text((X0 + 282, 1111), "you thought", font=F(COND, 24), fill=INK, anchor="lm")
    d.text((X1, 1111), "schematic", font=F(MED, 22), fill=MID, anchor="rm")

def sc_point(img, d, t):
    rv = cue("point", "they probably")
    d.text((X0 - 8, 300), "REPLAY", font=F(BLK, 230), fill=INK if t < rv else RULE)
    revealed = t >= rv
    hy, hp = cafe(d, t, talking=not revealed, partner_pose=wave(t) if revealed else None)
    if revealed:
        k = back((t - rv) / .35)
        if k > .05:
            d.rectangle([X0, 560, X0 + (X1 - X0) * min(1, k), 690], fill=SIG)
            if k > .8: d.text((480, 625), "THEY LIKED YOU.", font=F(BLK, 80), fill=WHITE, anchor="mm")
        note(d, hp[0] - 30, hp[1] - 20, 600, 728, "probably more than you think", (t - rv - .5) / .4, INK, anchor="ra")
    d.text((X0, 1146), "fig. 4 — the same conversation", font=F(MED, 22), fill=MID)

def end_card(d, t):
    k0 = S("end")
    for i, (w_, col) in enumerate((("NOT", INK), ("JUST", INK), ("YOU.", SIG))):
        k = ease((t - k0 - i * .12) / .35)
        if k > 0: d.text((X0 - 8, 290 + i * 210), w_, font=F(BLK, 230), fill=mix(BG, col, k))
    if t > k0 + .9:
        d.text((X0, 980), "SOURCES", font=F(COND, 26), fill=SIG)
        for i, l in enumerate(("Boothby, Cooney, Sandstrom & Clark (2018).", "The liking gap in conversations.", "Psychological Science 29(11).")):
            d.text((X0, 1016 + i * 32), l, font=F(MED, 24), fill=INK)
        box_label(d, X1, 1110, "@vascoda.soda", 32, WHITE, INK, anchor="ra")

SCENES = {"hook": sc_hook, "replay": sc_replay, "study": sc_study, "q": sc_q, "gap": sc_gap, "name": sc_name,
          "why": sc_why, "months": sc_months, "point": sc_point}

def draw(img, d, t):
    cur = "hook"
    for k in ORDER:
        if t >= S(k) - .05 and k != "hook": cur = k
    grid(d)
    if cur == "end": end_card(d, t)
    else:
        SCENES[cur](img, d, t)
        st = 0.0 if cur == "hook" else S(cur) - .05
        z = 1 + (0 if cur == "hook" else .035) * math.exp(-(t - st) * 8)
        if z > 1.002:
            cx, cy = 480, 730; l, tp = cx - cx / z, cy - cy / z
            img.paste(img.crop((int(l), int(tp), int(l + W / z), int(tp + H / z))).resize((W, H), Image.BILINEAR))
            d.rectangle([0, 0, W, 300], fill=BG); d.rectangle([0, 1180, W, H], fill=BG)
    chrome(d, t, cur)
    subtitle(d, t)

if __name__ == "__main__": cute.run(TL, draw, clean.FX)
