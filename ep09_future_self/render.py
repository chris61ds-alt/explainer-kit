"""NOT JUST YOU – No. 09: future you is a stranger (Ersner-Hershfield et al. 2009; Hershfield et al. 2011). Look: Swiss Detail."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .45, "scan": .5, "result": .5, "save": .5, "meet": .5, "double": .6, "point": .7, "end": 2.4})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "scan", "result", "save", "meet", "double", "point", "end"]
EP = Episode(TL, 9, "FUTURE YOU", order=ORDER,
             chapters={"hook": "A STRANGER", "scan": "THE SCAN", "result": "THE RESULT", "save": "THE COST",
                       "meet": "THE MEETING", "double": "THE EFFECT", "point": "NOW VS. LATER"},
             sources=("Ersner-Hershfield, Wimmer & Knutson (2009), SCAN 4", "Hershfield et al. (2011), J. Marketing Research 48"))

OLD = {"arms": ((25, 10), (-10, -5)), "tilt": 12}
def old_you(d, x, y=FLOOR, s=1.0, col=MID, f=-1):
    h = picto(d, x, y, s, col, f=f, pose=OLD)
    cx = x + f * 70 * s; d.line([cx, y, cx + f * 6 * s, y - 150 * s], fill=col, width=int(10 * s)); d.arc([cx - 2 * s + f * 6 * s - 20 * s, y - 170 * s, cx + f * 6 * s + 20 * s, y - 130 * s], 180, 360, fill=col, width=int(10 * s))
    return h

def name_tag(d, x, y, text, k=1.0, col=SIG):
    if k <= 0: return
    e = back(k); w, h = 150 * e, 96 * e
    d.rectangle([x - w / 2, y - h / 2, x + w / 2, y + h / 2], fill=WHITE, outline=col, width=4)
    d.rectangle([x - w / 2, y - h / 2, x + w / 2, y - h / 2 + 30 * e], fill=col)
    if e > .8:
        d.text((x, y - h / 2 + 15), "HELLO, I'M", font=F(COND, 18), fill=WHITE, anchor="mm")
        d.text((x, y + 14), text, font=F(BLK, 36), fill=INK, anchor="mm")

def sc_hook(img, d, t):
    giant(d, "STRANGER?", size=176)
    picto(d, 250, FLOOR, 1.0, INK, f=1, pose=IDLE)
    old_you(d, 700, s=1.0)
    name_tag(d, 250, 900, "YOU", (t - .2) / .3, INK)
    name_tag(d, 690, 930, "???", (t - cue("hook", "future")) / .3, SIG)
    if t >= cue("hook", "stranger"):
        dim_h(d, 330, 600, 640, (t - cue("hook", "stranger")) / .4, SIG, "10 YEARS", 24)
    fig(d, "fig. 1 — you, and future you")

def head_scan(d, cx, cy, r, t):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=6)
    d.polygon([(cx + r * .9, cy + r * .1), (cx + r * 1.12, cy + r * .35), (cx + r * .9, cy + r * .45)], fill=INK)     # nose
    d.rectangle([cx - r * .25, cy + r * .9, cx + r * .25, cy + r * 1.35], fill=INK)                                    # neck
    y = cy - r + (t * 160 % (2 * r))
    d.line([cx - r + 10, y, cx + r - 10, y], fill=SIG, width=4)
    for i in range(5): d.line([cx - r + 30, cy - r + 40 + i * 55, cx + r - 30, cy - r + 40 + i * 55], fill=RULE, width=2)
    d.ellipse([cx - 40, cy - 70, cx + 10, cy - 20], fill=SIG)                                                         # region of interest
    note(d, cx - 15, cy - 45, cx + 250, cy - 150, "self / other region", 1, INK)

def sc_scan(img, d, t):
    t0 = S("scan")
    head_scan(d, 300, 560, 170, t)
    d.text((X1, 640), "fMRI", font=F(BLK, 90), fill=INK, anchor="ra")
    conds = [("YOU · NOW", cue("scan", "themselves now"), INK, IDLE), ("YOU · IN 10 YEARS", cue("scan", "in ten years"), SIG, OLD), ("ANOTHER PERSON", cue("scan", "another person"), MID, IDLE)]
    for i, (lab, tk, col, pose) in enumerate(conds):
        k = ease((t - tk + .1) / .35)
        if k <= 0: continue
        x = X0 + i * 290; y = 830 + (1 - k) * 50
        d.rectangle([x, y, x + 260, y + 260], outline=INK, width=4)
        d.text((x + 14, y + 10), f"0{i + 1}", font=F(COND, 24), fill=SIG)
        picto(d, x + 130, y + 240, .48, col, pose=pose)
        d.text((x + 130, y + 276), lab, font=F(COND, 24), fill=INK, anchor="ma")
    fig(d, "Ersner-Hershfield, Wimmer & Knutson — SCAN, 2009")

def sc_result(img, d, t):
    t0 = S("result"); yb = 1000
    d.text((X0, 320), "ACTIVITY", font=F(BLK, 110), fill=INK)
    d.text((X0, 450), "in the self / other region", font=F(COND, 32), fill=INK)
    bars = [("NOW YOU", .9, INK, .2), ("FUTURE YOU", .45, SIG, .5), ("SOMEONE ELSE", .4, MID, .8)]
    for i, (lab, v, col, dl) in enumerate(bars):
        x = X0 + 40 + i * 270; k = ease((t - t0 - dl) / .5)
        d.rectangle([x, yb - 420 * v * k, x + 180, yb], fill=col)
        d.text((x + 90, yb + 18), lab, font=F(COND, 28), fill=INK, anchor="ma")
    d.line([X0, yb, X1, yb], fill=INK, width=3)
    if t >= cue("result", "someone else"):
        k = (t - cue("result", "someone else")) / .4
        dim_h(d, X0 + 130, X0 + 40 + 540 + 90, yb - 420 * .55, k, SIG, "LOOKS ALIKE", 24)
    d.text((X1, 1146), "schematic", font=F(MED, 22), fill=MID, anchor="ra")
    fig(d, "fig. 2 — on average")

def sc_save(img, d, t):
    t0 = S("save")
    d.text((X0, 320), "THE BIGGER THE GAP", font=F(BLK, 64), fill=INK)
    d.text((X0, 400), "the less people saved", font=F(BLK, 64), fill=SIG)
    ox, oy, w, h = X0 + 60, 1040, 760, 480
    d.line([ox, oy, ox + w, oy], fill=INK, width=4); d.line([ox, oy, ox, oy - h], fill=INK, width=4)
    d.text((ox + w, oy + 20), "gap: now-you vs. future-you →", font=F(COND, 24), fill=INK, anchor="ra")
    d.text((ox - 14, oy - h), "saving", font=F(COND, 24), fill=INK, anchor="ra")
    rng = np.random.default_rng(6)
    for i in range(36):
        u = rng.uniform(.05, .95); v = clamp(.9 - .7 * u + rng.normal(0, .09))
        k = ease((t - t0 - .3 - i * .03) / .2)
        if k > 0:
            x, y = ox + w * u, oy - h * v; r = 9 * k
            d.ellipse([x - r, y - r, x + r, y + r], fill=INK if i % 5 else SIG)
    kl = ease((t - cue("save", "worse")) / .6)
    if kl > 0: d.line([ox + w * .05, oy - h * .87, ox + w * (.05 + .9 * kl), oy - h * (.87 - .63 * kl)], fill=SIG, width=6)
    d.text((X1, 1146), "schematic", font=F(MED, 22), fill=MID, anchor="ra")
    fig(d, "fig. 3 — saving, two weeks later")

def headset(d, h, s, col=INK):
    d.rectangle([h[0] - 10 * s, h[1] - 22 * s, h[0] + 54 * s, h[1] + 14 * s], fill=col)
    d.arc([h[0] - 46 * s, h[1] - 50 * s, h[0] + 46 * s, h[1] + 30 * s], 200, 340, fill=col, width=int(8 * s))

def sc_meet(img, d, t):
    t0 = S("meet")
    giant(d, "MEET", size=200, k=(t - t0) / .3)
    # mirror frame on the right with the aged avatar
    mx0, my0, mx1, my1 = 520, 560, 860, 1140
    km = ease((t - t0 - .3) / .4)
    if km > 0:
        d.rectangle([mx0, my1 - (my1 - my0) * km, mx1, my1], outline=INK, width=8)
        for i in range(0, 300, 40): d.line([mx0 + 20 + i, my0 + 30, mx0 + 60 + i, my0 + 70], fill=RULE, width=3)
        if t >= cue("meet", "aged") - .2:
            kk = ease((t - cue("meet", "aged") + .2) / .5)
            old_you(d, 690, FLOOR, .85, mix(BG, SIG, kk), f=-1)
    h = picto(d, 300, FLOOR, 1.0, INK, f=1, pose=merge(IDLE, {"arms": ((60, 100), (-10, -5))}))
    if t >= cue("meet", "virtual"):
        headset(d, h, 1.0)
        note(d, h[0] + 30, h[1], 400, 640, "VR headset", (t - cue("meet", "virtual")) / .4, INK, anchor="ra")
    fig(d, "Hershfield et al. — Journal of Marketing Research, 2011")

def sc_double(img, d, t):
    t0 = S("double")
    d.text((X0 - 8, 290), "×2", font=F(BLK, 300), fill=SIG)
    for i, (lab, v, col, dl) in enumerate((("saw their current self", .4, INK, .3), ("met their future self", .8, SIG, .7))):
        y = 700 + i * 170
        hbar(d, y, v, (t - t0 - dl) / .6, col, lab, h=88)
    if t >= cue("double", "twice"):
        dim_h(d, X0 + (X1 - X0) * .4, X0 + (X1 - X0) * .8, 660, (t - cue("double", "twice")) / .4, SIG, None)
    d.text((X1, 1146), "hypothetical retirement account", font=F(MED, 22), fill=MID, anchor="ra")
    fig(d, "fig. 4 — VR study")

def sc_point(img, d, t):
    t0 = S("point")
    ns = cue("point", "not a stranger")
    d.text((X0, 320), "NOW", font=F(BLK, 120), fill=INK); d.text((X1, 320), "LATER", font=F(BLK, 120), fill=SIG, anchor="ra")
    # seesaw
    tilt = lerp(-10, 0, ease((t - ns) / .8))
    cx, cy, L = 480, 760, 360; r = math.radians(tilt)
    a = (cx - L * math.cos(r), cy - L * math.sin(r)); b = (cx + L * math.cos(r), cy + L * math.sin(r))
    d.line([a, b], fill=INK, width=12); d.polygon([(cx, cy), (cx - 50, cy + 90), (cx + 50, cy + 90)], fill=INK)
    picto(d, a[0] + 40, a[1] - 6, .62, INK, f=1, pose=IDLE)
    if t < ns: old_you(d, b[0] - 40, b[1] - 6, .62, MID, f=-1)
    else: old_you(d, b[0] - 40, b[1] - 6, .62, INK, f=-1)
    if t >= ns:
        name_tag(d, b[0] - 40, b[1] - 290, "ME", (t - ns - .3) / .3, SIG)
        k = ease((t - ns) / .4)
        d.text((X0 - 6, 920), "NOT A", font=F(BLK, 110), fill=mix(BG, INK, k)); d.text((X0 - 6, 1030), "STRANGER.", font=F(BLK, 110), fill=mix(BG, SIG, k))
    fig(d, "fig. 5 — same person, two dates")

EP.scenes = {"hook": sc_hook, "scan": sc_scan, "result": sc_result, "save": sc_save, "meet": sc_meet, "double": sc_double, "point": sc_point}

FX = [(0.0, thud(.5), 0), (.1, riser(.5, .05), 0), (cue("hook", "future"), pop(.18), .3), (cue("hook", "stranger"), thud(.4), 0),
      *EP.cut_fx(),
      (cue("scan", "themselves now"), pop(.15), -.3), (cue("scan", "in ten years"), pop(.15), 0), (cue("scan", "another person"), pop(.15), .3),
      (cue("result", "someone else"), thud(.4), 0),
      (cue("save", "worse"), whoosh(.5, .12), 0),
      (cue("meet", "aged"), riser(.6, .1), .3), (cue("meet", "virtual"), pop(.18), -.2),
      (cue("double", "twice"), thud(.5), 0),
      (cue("point", "not a stranger"), thud(.5), 0),
      (S("end"), thud(.5), 0)]

if __name__ == "__main__": EP.run(FX)
