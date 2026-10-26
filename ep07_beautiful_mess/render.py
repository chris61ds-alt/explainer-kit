"""NOT JUST YOU – No. 07: the beautiful mess effect (Bruk, Scholl & Bless 2018; 2022). Look: Swiss Detail."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .35, "flip": .45, "study": .5, "self": .3, "other": .5, "name": .5, "why": .5, "kind": .5, "point": .7, "end": 2.4})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "flip", "study", "self", "other", "name", "why", "kind", "point", "end"]
EP = Episode(TL, 7, "THE BEAUTIFUL MESS", order=ORDER,
             chapters={"hook": "CRINGE", "flip": "THE OTHER VIEW", "study": "THE STUDY", "self": "YOU", "other": "THEM",
                       "name": "THE NAME", "why": "WHY", "kind": "THE FIX", "point": "AGAIN"},
             sources=("Bruk, Scholl & Bless (2018), Journal of", "Personality and Social Psychology · (2022), PSPB"))

def cringe_meter(d, x, y0, y1, v, label="cringe-o-meter"):
    d.rectangle([x, y0, x + 40, y1], outline=INK, width=4)
    h = (y1 - y0) * v; d.rectangle([x + 6, y1 - h, x + 34, y1 - 4], fill=SIG)
    for i in range(11):
        yy = y1 - (y1 - y0) * i / 10; d.line([x - (16 if i % 5 == 0 else 8), yy, x, yy], fill=INK, width=2)
    d.text((x + 20, y1 + 16), label, font=F(MONO, 18), fill=MID, anchor="ma")

def viewfinder(d, box, k=1.0, col=INK):
    if k <= 0: return
    x0, y0, x1, y1 = box; L = 50 * ease(k)
    for (x, y, sx, sy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        d.line([x, y, x + sx * L, y], fill=col, width=6); d.line([x, y, x, y + sy * L], fill=col, width=6)

# ---------------------------------------------------------------- scenes
def sc_hook(img, d, t):
    cr = cue("hook", "cringing")
    giant(d, "CRINGE.", size=200)
    v = .25 + .75 * ease((t - cr + .4) / .6) + .03 * math.sin(t * 20) * (t > cr)
    cringe_meter(d, 820, 560, 1000, clamp(v))
    said = (t - .2) / .3
    hp = picto(d, 400, FLOOR, 1.05, INK, f=1, pose=TALK(t) if t < cue("hook", "and now") else FACEPALM,
               head_dy=3 * math.sin(t * 14) if t >= cr else 0)
    if t < cue("hook", "and now") + .5:
        speech_box(d, 460, 600, 300, said, INK, 1, "I messed up.", 34)
    else:
        note(d, hp[0] + 40, hp[1], 660, 640, "on repeat", (t - cue("hook", "and now") - .5) / .4, SIG)
    fig(d, "fig. 1 — you, right after")

def sc_flip(img, d, t):
    t0 = S("flip")
    giant(d, "THEIR VIEW", size=150, k=(t - t0) / .3)
    viewfinder(d, (300, 560, 660, 1140), (t - t0 - .2) / .3, SIG)
    if int(t * 2) % 2 == 0: d.ellipse([320, 580, 344, 604], fill=SIG); d.text((354, 592), "REC", font=F(COND, 26), fill=SIG, anchor="lm")
    picto(d, 480, FLOOR, .8, INK, f=1, pose=FACEPALM)
    for i, (x, f) in enumerate(((150, 1), (250, 1), (790, -1))):
        picto(d, x, FLOOR, .62, MID, f=f, pose=IDLE)
    fig(d, "fig. 2 — the view from outside")

def scenario(d, x, y, no, label, k, icon):
    if k <= 0: return
    e = ease(k); w, h = 260, 330; yy = y + (1 - e) * 60
    d.rectangle([x, yy, x + w, yy + h], outline=INK, width=4)
    d.text((x + 16, yy + 12), no, font=F(COND, 26), fill=SIG)
    icon(d, x + w / 2, yy + h - 80)
    for li, l in enumerate(label): d.text((x + w / 2, yy + h + 16 + li * 34), l, font=F(COND, 28), fill=INK, anchor="ma")

def sc_study(img, d, t):
    t0 = S("study")
    d.text((X0 - 10, 280), "7", font=F(BLK, 300), fill=SIG)
    d.text((X0 + 190, 330), "STUDIES", font=F(BLK, 110), fill=INK)
    d.text((X0 + 196, 470), "people pictured moments of vulnerability", font=F(COND, 30), fill=INK)
    cards = [(cue("study", "admitting"), "01", ("Admitting", "a mistake"), lambda d_, cx, cy: picto(d_, cx, cy + 50, .55, INK, pose=SHRUG)),
             (cue("study", "confessing"), "02", ("Confessing", "love"), lambda d_, cx, cy: picto(d_, cx, cy + 50, .55, SIG, pose=OPEN)),
             (cue("study", "improvising"), "03", ("Singing", "for a jury"), lambda d_, cx, cy: (picto(d_, cx - 30, cy + 50, .55, INK, pose=SING(t)), mic(d_, cx + 60, cy + 50, 120)))]
    for i, (tk, no, lab, ic) in enumerate(cards):
        scenario(d, X0 + i * 290, 560, no, lab, (t - tk + .1) / .35, ic)
    fig(d, "Bruk, Scholl & Bless — Journal of Personality and Social Psychology, 2018")

def scale_row(d, y, title, col, pose, val, k, kk):
    if k <= 0: return
    e = ease(k)
    d.text((X0, y), title, font=F(BLK, 44), fill=mix(BG, INK, e))
    picto(d, X0 + 70, y + 340, .55, col, pose=pose)
    x0, x1, ya = X0 + 180, X1 - 10, y + 230
    d.line([x0, ya, x1, ya], fill=INK, width=4)
    for i in range(11): xx = x0 + (x1 - x0) * i / 10; d.line([xx, ya - (14 if i % 5 == 0 else 7), xx, ya + (14 if i % 5 == 0 else 7)], fill=INK, width=2)
    d.text((x0, ya + 30), "WEAKNESS", font=F(COND, 26), fill=INK); d.text((x1, ya + 30), "COURAGE", font=F(COND, 26), fill=INK, anchor="ra")
    xm = x0 + (x1 - x0) * lerp(.5, val, ease(kk))
    d.polygon([(xm, ya - 10), (xm - 22, ya - 50), (xm + 22, ya - 50)], fill=col)

def sc_selfother(img, d, t):
    scale_row(d, 330, "WHEN IT'S YOU", INK, SING(t), .25, (t - S("self")) / .3, (t - cue("self", "weakness") + .2) / .6)
    if t >= S("other") - .1:
        scale_row(d, 730, "WHEN IT'S SOMEONE ELSE", SIG, SING(t + 1), .78, (t - S("other") + .1) / .3, (t - cue("other", "courage") + .2) / .6)
    if t >= cue("other", "courage") + .4:
        x0, x1 = X0 + 180, X1 - 10
        a, b = x0 + (x1 - x0) * .25, x0 + (x1 - x0) * .78
        dim_h(d, a, b, 690, (t - cue("other", "courage") - .4) / .4, SIG, "SAME ACT", 24)
    d.text((X1, 1146), "schematic", font=F(MED, 22), fill=MID, anchor="ra")
    fig(d, "fig. 3 — rating the same moment")

def messy_word(img, text, x, y, size, col, t, k, seed=1):
    """letters set individually, each rotated / offset a little – settles but stays messy"""
    f = F(BLK, size); rng = np.random.default_rng(seed); dd = ImageDraw.Draw(img); xx = x
    for i, ch in enumerate(text):
        w = dd.textlength(ch, font=f)
        rot = (rng.uniform(-14, 14)) * (1 + 2 * (1 - ease(k))) + math.sin(t * 2 + i) * 1.5
        dy = rng.uniform(-24, 24) * (1 + (1 - ease(k)) * 3)
        lay = Image.new("RGBA", (int(w + 80), int(size * 1.4)), (0, 0, 0, 0))
        ImageDraw.Draw(lay).text((40, 0), ch, font=f, fill=col + (255,))
        lay = lay.rotate(rot, resample=Image.BICUBIC, expand=False)
        img.paste(lay, (int(xx - 40), int(y + dy)), lay); xx += w + 6

def sc_name(img, d, t):
    t0 = S("name"); kb = (t - cue("name", "beautiful") + .1) / .35
    d.text((X0, 330), "THE", font=F(BLK, 100), fill=INK)
    if kb > 0:
        fb = F(BLK, 150); d.text((X0 - 6 - (1 - ease(kb)) * 80, 450), "BEAUTIFUL", font=fb, fill=mix(BG, INK, ease(kb)))
    km = (t - cue("name", "mess") + .1) / .5
    if km > 0: messy_word(img, "MESS", X0, 640, 260, SIG, t, km)
    if km > .9:
        d.text((X0, 960), "EFFECT", font=F(BLK, 100), fill=INK)
        note(d, 700, 760, 860, 1000, "not a typo", (t - cue("name", "mess") - .8) / .4, INK, anchor="ra", size=26)

def scribbles(d, cx, cy, r, t):
    rng = np.random.default_rng(4)
    for i in range(26):
        a = rng.uniform(0, 2 * math.pi); rr = rng.uniform(0, r * .8)
        x, y = cx + math.cos(a) * rr, cy + math.sin(a) * rr
        pts = [(x + rng.uniform(-30, 30), y + rng.uniform(-30, 30)) for _ in range(4)]
        d.line(pts, fill=INK if i % 4 else SIG, width=4)

def sc_why(img, d, t):
    t0 = S("why"); fo = cue("why", "from the outside")
    # left: up close (lens full of detail)
    k = ease((t - t0) / .4)
    d.text((X0, 320), "UP CLOSE", font=F(BLK, 56), fill=INK)
    cx, cy, r = 260, 680, 190 * k
    if k > 0:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=8)
        if k > .9:
            scribbles(d, cx, cy, r, t)
            for i, (lab, dx, dy) in enumerate((("voice cracked", -60, -150), ("blushed", 120, -60), ("wrong word", -120, 90), ("um…", 90, 130))):
                kk = (t - t0 - .4 - i * .25) / .3
                if kk > 0: box_label(d, cx + dx - 40, cy + dy, lab, 24, WHITE, SIG if i % 2 else INK)
        d.line([cx + r * .7, cy + r * .7, cx + r * 1.15, cy + r * 1.15], fill=INK, width=18)
    # right: from the outside (small figure, whole frame)
    if t >= fo - .1:
        k2 = ease((t - fo + .1) / .4)
        d.text((520, 320), "FROM OUTSIDE", font=F(BLK, 56), fill=mix(BG, INK, k2))
        bx = (560, 470, 880, 1060)
        d.rectangle(bx, outline=mix(BG, INK, k2), width=4)
        picto(d, 720, 1000, .55, SIG, pose=SING(t))
        d.line([620, 1000, 820, 1000], fill=INK, width=4)
        if k2 > .9:
            dim_h(d, 580, 860, 1090, (t - fo - .4) / .4, INK, "THE WHOLE PICTURE", 22)
    fig(d, "fig. 4 — concrete vs. abstract")

def sc_kind(img, d, t):
    t0 = S("kind")
    giant(d, "KINDER", size=170, k=(t - t0) / .3)
    d.text((X0, 520), "to yourself = a smaller gap", font=F(COND, 40), fill=INK)
    x0, x1, ya = X0 + 20, X1 - 20, 720
    d.line([x0, ya, x1, ya], fill=INK, width=4)
    d.text((x0, ya + 30), "WEAKNESS", font=F(COND, 26), fill=INK); d.text((x1, ya + 30), "COURAGE", font=F(COND, 26), fill=INK, anchor="ra")
    shrink = ease_io((t - cue("kind", "smaller") + .2) / .8)
    a = x0 + (x1 - x0) * lerp(.25, .52, shrink); b = x0 + (x1 - x0) * .78
    d.polygon([(a, ya - 10), (a - 22, ya - 50), (a + 22, ya - 50)], fill=INK)
    d.polygon([(b, ya - 10), (b - 22, ya - 50), (b + 22, ya - 50)], fill=SIG)
    dim_h(d, a, b, ya - 90, 1, SIG, None)
    box_label(d, (a + b) / 2, ya - 150, "GAP", 26, WHITE, SIG, anchor="ma")
    picto(d, 480, FLOOR, .7, INK, pose=OPEN)
    fig(d, "Bruk, Scholl & Bless — PSPB, 2022 · schematic")

def sc_point(img, d, t):
    rv = cue("point", "to them")
    giant(d, "CRINGE.", size=200, col=INK if t < rv else RULE)
    if t >= rv:
        k = ease((t - rv) / .3)
        d.line([X0, 420, X0 + 760 * k, 400], fill=SIG, width=14)
        kb = ease((t - cue("point", "brave") + .1) / .35)
        if kb > 0: d.text((X0 - 8 - (1 - kb) * 60, 510), "BRAVE.", font=F(BLK, 200), fill=mix(BG, SIG, kb))
    calm = t >= rv
    hp = picto(d, 400, FLOOR, 1.05, INK, pose=IDLE if calm else FACEPALM)
    for i, (x, f) in enumerate(((150, 1), (760, -1))):
        h = picto(d, x, FLOOR, .62, MID if not calm else SIG, f=f, pose=IDLE if not calm else OPEN)
    if calm:
        note(d, 760, 830, 640, 760, "brave.", (t - cue("point", "brave")) / .4, SIG, anchor="ra", size=32)
    fig(d, "fig. 5 — the same moment, from outside")

EP.scenes = {"hook": sc_hook, "flip": sc_flip, "study": sc_study, "self": sc_selfother, "other": sc_selfother,
             "name": sc_name, "why": sc_why, "kind": sc_kind, "point": sc_point}

FX = [(0.0, thud(.5), 0), (.15, riser(.6, .06), 0), (cue("hook", "and now"), pop(.18), 0), (cue("hook", "cringing"), riser(.5, .1), 0),
      *EP.cut_fx(),
      (cue("study", "admitting"), thud(.3), -.3), (cue("study", "confessing"), thud(.3), 0), (cue("study", "improvising"), thud(.3), .3),
      (cue("self", "weakness"), pop(.15), -.2), (cue("other", "courage"), pop(.15), .2),
      (cue("name", "beautiful"), thud(.45), 0), (cue("name", "mess"), rewind_sfx(.14, .4), 0),
      (cue("why", "from the outside"), whoosh(.4, .15), .3),
      (cue("kind", "smaller"), whoosh(.6, .1), 0),
      (cue("point", "to them"), thud(.5), 0), (cue("point", "brave"), pop(.2), 0),
      (S("end"), thud(.5), 0)]

if __name__ == "__main__": EP.run(FX)
