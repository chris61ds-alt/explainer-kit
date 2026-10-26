"""NOT JUST YOU – No. 10: the spotlight effect (Gilovich, Medvec & Savitsky 2000). Look: Swiss Detail."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .45, "study": .5, "guess": .4, "real": .6, "name": .5, "why": .6, "point": .7, "end": 2.4})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "guess", "real", "name", "why", "point", "end"]
EP = Episode(TL, 10, "THE SPOTLIGHT", order=ORDER,
             chapters={"hook": "THE STAIN", "study": "THE SHIRT", "guess": "THE GUESS", "real": "THE TRUTH",
                       "name": "THE NAME", "why": "WHY", "point": "THE STAIN, AGAIN"},
             sources=("Gilovich, Medvec & Savitsky (2000),", "Journal of Personality and Social Psychology 78(2)"))

def eye(d, x, y, s=1.0, col=INK, open_k=1.0, look=(0, 0)):
    h = 26 * s * open_k
    d.chord([x - 44 * s, y - h, x + 44 * s, y + h], 0, 360, fill=WHITE, outline=col, width=int(5 * s))
    if open_k > .3:
        px, py = x + look[0] * 14 * s, y + look[1] * 8 * s
        d.ellipse([px - 14 * s, py - 14 * s, px + 14 * s, py + 14 * s], fill=col)
    else: d.line([x - 44 * s, y, x + 44 * s, y], fill=col, width=int(5 * s))

def stain(d, x, y, s=1.0, k=1.0):
    if k <= 0: return
    rng = np.random.default_rng(8); e = ease(k)
    d.ellipse([x - 22 * s * e, y - 18 * s * e, x + 22 * s * e, y + 18 * s * e], fill=SIG)
    for i in range(7):
        a = rng.uniform(0, 2 * math.pi); r = rng.uniform(24, 40) * s * e; rr = rng.uniform(4, 9) * s * e
        d.ellipse([x + math.cos(a) * r - rr, y + math.sin(a) * r - rr, x + math.cos(a) * r + rr, y + math.sin(a) * r + rr], fill=SIG)

def spill_cup(d, x, y, t, k):
    """cup tipping over with falling drops"""
    ang = 70 * ease(k)
    r = math.radians(ang)
    pts = [(-22, -44), (22, -44), (22, 0), (-22, 0)]
    rot = [(x + px * math.cos(r) - py * math.sin(r), y + px * math.sin(r) + py * math.cos(r)) for px, py in pts]
    d.polygon(rot, outline=INK, width=6)
    if k > .5:
        for i in range(4):
            u = ((t * 2 + i * .25) % 1)
            d.ellipse([x + 30 - 5 + i * 4, y - 20 + u * 120 - 6, x + 30 + 5 + i * 4, y - 20 + u * 120 + 6], fill=SIG)

def sc_hook(img, d, t):
    sp = cue("hook", "spill"); ev = cue("hook", "everyone")
    giant(d, "STAIN.", size=220)
    h = picto(d, 420, FLOOR, 1.05, INK, f=1, pose={"arms": ((95, 60), (-10, -5))} if t < sp + .6 else WORRY)
    spill_cup(d, 560, 790, t, (t - sp) / .4)
    stain(d, 430, 880, 1.2, (t - sp - .4) / .3)
    if t >= ev - .1:
        spots = [(140, 600), (760, 600), (130, 860), (790, 860), (260, 640), (680, 640)]
        for i, (x, y) in enumerate(spots):
            k = back((t - ev + .1 - i * .08) / .3)
            if k > .05:
                eye(d, x, y, .8 * k, INK, look=((430 - x) / 300, (880 - y) / 300))
                if k > .9:
                    for xx in range(0, 10):
                        u = xx / 10; d.point((lerp(x, 430, u), lerp(y, 880, u)), fill=SIG)
    fig(d, "fig. 1 — how it feels")

def tshirt(d, cx, cy, s=1.0, k=1.0):
    if k <= 0: return
    s *= back(k)
    w, h = 240 * s, 280 * s
    pts = [(cx - w * .5, cy - h * .5), (cx - w * .18, cy - h * .5), (cx, cy - h * .42), (cx + w * .18, cy - h * .5), (cx + w * .5, cy - h * .5),
           (cx + w * .85, cy - h * .25), (cx + w * .66, cy - h * .08), (cx + w * .5, cy - h * .18), (cx + w * .5, cy + h * .5),
           (cx - w * .5, cy + h * .5), (cx - w * .5, cy - h * .18), (cx - w * .66, cy - h * .08), (cx - w * .85, cy - h * .25)]
    d.polygon(pts, fill=WHITE, outline=INK, width=int(6 * s))
    # big portrait print (generic) + name banner
    d.ellipse([cx - 62 * s, cy - 100 * s, cx + 62 * s, cy + 24 * s], fill=SIG)
    d.ellipse([cx - 36 * s, cy - 78 * s, cx + 36 * s, cy - 6 * s], fill=WHITE)
    d.rectangle([cx - 100 * s, cy + 44 * s, cx + 100 * s, cy + 90 * s], fill=INK)
    d.text((cx, cy + 67 * s), "BARRY!", font=F(BLK, int(36 * s)), fill=WHITE, anchor="mm")

def room(d, t, hl=0, hl_k=1.0, walker_x=None):
    """8 people in a room; hl = how many noticed (orange)"""
    d.rectangle([X0 + 280, 560, X1, FLOOR], outline=INK, width=5)
    for i in range(8):
        r, c = divmod(i, 4)
        x = X0 + 350 + c * 130; y = 820 + r * 290; s = .42 + .08 * r
        col = SIG if i < hl * hl_k else MID
        picto(d, x, y, s, col, f=-1, pose=IDLE)
    if walker_x is not None:
        h = picto(d, walker_x, FLOOR, .75, INK, f=1, pose=WALK(t))
        tshirt(d, walker_x, h[1] + 100, .3)

def sc_study(img, d, t):
    t0 = S("study")
    giant(d, "THE SHIRT", size=170, k=(t - t0) / .3)
    if t < cue("study", "into a room") - .2:
        tshirt(d, 480, 790, 1.2, (t - t0 - .3) / .4)
        if t >= cue("study", "barry"):
            note(d, 540, 720, 760, 600, "a giant picture of", (t - cue("study", "barry")) / .4, INK, anchor="la", size=26)
            note(d, 560, 860, 760, 940, "70s pop singer", (t - cue("study", "barry") - .2) / .4, SIG, anchor="la", size=26)
    else:
        wk = clamp((t - cue("study", "into a room") + .2) / 1.6)
        room(d, t, walker_x=lerp(X0 + 60, X0 + 220, wk))
    fig(d, "Cornell students · Gilovich, Medvec & Savitsky, 2000")

def counter(d, x, y, val, col, label):
    d.text((x, y), f"≈ {int(val)} %", font=F(BLK, 120), fill=col)
    d.text((x + 6, y + 140), label, font=F(COND, 32), fill=INK)

def sc_guess(img, d, t):
    t0 = S("guess")
    room(d, t, hl=4, hl_k=clamp((t - cue("guess", "half") + .3) / .6))
    h = picto(d, X0 + 140, FLOOR, .75, INK, f=1, pose=WORRY)
    tshirt(d, X0 + 140, h[1] + 100, .3)
    counter(d, X0, 300, 46 * ease((t - t0 - .2) / .8), INK, "THEIR GUESS: NOTICED")

def sc_real(img, d, t):
    t0 = S("real"); rq = cue("real", "quarter")
    k = ease((t - rq + .3) / .6)
    room(d, t, hl=4 - 2 * k)
    h = picto(d, X0 + 140, FLOOR, .75, INK, f=1, pose=IDLE if k > .5 else WORRY)
    tshirt(d, X0 + 140, h[1] + 100, .3)
    counter(d, X0, 300, lerp(46, 23, k), SIG, "REALITY: NOTICED")
    if k > .9: dim_v(d, X1 - 30, 330, 440, (t - rq - .3) / .4, SIG, "HALF")
    fig(d, "fig. 2 — 8 people, schematic")

def sc_name(img, d, t):
    t0 = S("name"); ks = (t - cue("name", "spotlight") + .1) / .4
    spotlight(d, 480, FLOOR, Y_TOP + 260, 320) if ks > 0 else None
    if ks > 0:
        d.text((X0 - 8 - (1 - ease(ks)) * 80, 300), "SPOTLIGHT", font=F(BLK, 148), fill=mix(BG, INK, ease(ks)))
        d.text((X0 - 8, 460), "EFFECT", font=F(BLK, 148), fill=mix(BG, SIG, ease(ks - .3)))
    picto(d, 480, FLOOR, .9, INK, pose=WORRY)
    d.ellipse([280, FLOOR - 26, 680, FLOOR + 26], outline=SIG, width=5)

def sc_why(img, d, t):
    t0 = S("why"); ot = cue("why", "but everyone")
    # you, in your own spotlight
    spotlight(d, 300 if t >= ot else 480, FLOOR, Y_TOP + 220, 150 if t >= ot else 260)
    picto(d, 300 if t >= ot else 480, FLOOR, .8, INK, pose=WORRY)
    note(d, 330 if t >= ot else 510, 700, 600, 560, "you: center of your world", (t - t0 - .3) / .4, INK, anchor="la", size=26) if t < ot else None
    if t >= ot:
        for i, x in enumerate((560, 700, 840)):
            k = ease((t - ot - i * .2) / .35)
            if k <= 0: continue
            d.polygon([(x - 18, Y_TOP + 380), (x + 18, Y_TOP + 380), (x + 90, FLOOR), (x - 90, FLOOR)], fill=mix(BG, (242, 241, 236), k))
            picto(d, x, FLOOR, .55, SIG, f=-1, pose=[TALK(t, i), SHRUG, WORRY][i])
        box_label(d, 700, 560, "BUSY WITH THEMSELVES", 26, WHITE, SIG, anchor="ma") if t > ot + .8 else None
    fig(d, "fig. 3 — everyone has their own spotlight")

def sc_point(img, d, t):
    t0 = S("point"); nv = cue("point", "never")
    giant(d, "STAIN.", size=220, col=RULE if t >= nv else INK)
    picto(d, 420, FLOOR, 1.05, INK, pose=IDLE if t >= nv else WORRY)
    stain(d, 430, 880, 1.2)
    spots = [(140, 600), (760, 600), (130, 860), (790, 860), (260, 640), (680, 640)]
    for i, (x, y) in enumerate(spots):
        closed = clamp((t - nv - i * .1) / .25) if i != 0 else 0
        eye(d, x, y, .8, MID if closed > .5 else INK, open_k=1 - closed * .9, look=((430 - x) / 300, (880 - y) / 300) if i == 0 else ((x - 430) / 300, -.5))
    if t >= nv:
        note(d, 160, 620, 200, 470, "this one did", (t - nv - .7) / .4, SIG, anchor="la", size=26)
        k = ease((t - nv) / .4)
        d.text((X1, 940), "MOST", font=F(BLK, 90), fill=mix(BG, SIG, k), anchor="ra")
        d.text((X1, 1040), "DIDN'T SEE IT.", font=F(BLK, 52), fill=mix(BG, SIG, k), anchor="ra")
    fig(d, "fig. 4 — how it actually is")

EP.scenes = {"hook": sc_hook, "study": sc_study, "guess": sc_guess, "real": sc_real, "name": sc_name, "why": sc_why, "point": sc_point}

FX = [(0.0, thud(.5), 0), (cue("hook", "spill"), whoosh(.3, .15), .2), (cue("hook", "spill") + .45, pop(.25), .2),
      *[(cue("hook", "everyone") + i * .08, tick(.06), (i % 3 - 1) * .6) for i in range(6)],
      *EP.cut_fx(),
      (cue("study", "barry"), pop(.2), 0), (cue("study", "into a room"), riser(.5, .06), 0),
      (cue("guess", "half"), thud(.35), 0),
      (cue("real", "quarter"), thud(.5), 0), (cue("real", "quarter") + .3, rewind_sfx(.12, .35), 0),
      (cue("name", "spotlight"), thud(.5), 0),
      (cue("why", "but everyone"), whoosh(.4, .12), .3),
      (cue("point", "even"), pop(.12), 0),
      (S("end"), thud(.5), 0)]

if __name__ == "__main__": EP.run(FX)
