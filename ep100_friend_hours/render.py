"""NOT JUST YOU – No. 100 (level 2 remake, 12.11.2026, first test of shared/fx2.py): hours to make a friend –
~50 h casual friend, ~90 h friend, 200+ h close friend (Hall 2019, 355 adults who had moved + 112 students).
Level 2 + fx2: an isometric street at night is there from frame 0; the CAMERA starts on your house, pulls out to the street,
pushes in on the friend's house for the reveal and snaps back for the loop. Hours flow as PARTICLES from your door to theirs,
their windows light up with GLOW stage by stage (50 / 90 / 200+), live hour counter, orange reveal.
Old version: render_v1.py / script_v1.json."""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
from fx2 import camera, cam_path, glow, dots, Stream
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .34, "setup": .34, "casual": .3, "friend": .3, "reveal": .4, "why": .1})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "setup", "casual", "friend", "reveal", "why", "end"]
EP = ThreadEpisode(TL, 100, "FRIEND HOURS", order=ORDER, dark=True, label="SURVEY · 467 PEOPLE",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Hall (2019), How many hours does it take to make", "a friend?, J. of Social and Personal Relationships 36(4)"),
                   music=dict(bpm=96, root=2, prog="dream", kick="four", audio="v5"),
                   cover=dict(words=["A CLOSE FRIEND", "TAKES 200+", "HOURS."], kicker="You just moved? Here's the math."))

I = Iso(470, 655, 1.0)
HOUSES = [(x, y) for y in (0, 300) for x in (0, 160, 320, 480)]     # two rows, the street runs between them
YOU, FRIEND = HOUSES.index((0, 300)), HOUSES.index((480, 0))
A_, B_, HW, RF = 110, 110, 95, 55                                     # footprint, wall height, roof height

T_PULL = S("setup") - .1
T50, T90 = cue("casual", "about fifty") - .1, cue("friend", "about ninety") - .1
T200 = cue("reveal", "over two hundred") - .1
T_BACK = cue("why", "Because") - .35

def hours(t):
    """the live hour counter: 0 → 50 → 90 → 200"""
    if t < S("casual") - .1 or t >= T_BACK: return 0
    if t < T90: return 50 * ease(clamp((t - S("casual") + .1) / max(.3, T50 + .6 - S("casual"))))
    if t < T200: return 50 + 40 * ease(clamp((t - T90) / .8))
    return 90 + 110 * ease(clamp((t - T200) / 1.0))

def lit(h):
    """how many of the friend's 3 windows are lit (fractional = fading in)"""
    return clamp(h / 50) * 1 + clamp((h - 50) / 40) * 1 + clamp((h - 90) / 110) * 1

def windows(x, y):
    """3 window quads: two on the front-left face, one on the front-right face (screen polygons)"""
    P = I.P; z0, z1 = 30, 62; out = []
    for xa in (18, 62):
        out.append([P(x + xa, y + B_, z0), P(x + xa + 30, y + B_, z0), P(x + xa + 30, y + B_, z1), P(x + xa, y + B_, z1)])
    out.append([P(x + A_, y + 40, z0), P(x + A_, y + 70, z0), P(x + A_, y + 70, z1), P(x + A_, y + 40, z1)])
    return out

def door(x, y):
    P = I.P; return [P(x + A_, y + 78, 0), P(x + A_, y + 100, 0), P(x + A_, y + 100, 46), P(x + A_, y + 78, 46)]

def house(d, x, y, wl, you=False):
    """wl = list of 3 window light levels 0..1"""
    I.box(d, x, y, 0, A_, B_, HW)
    P = I.P; apex = P(x + A_ / 2, y + B_ / 2, HW + RF)
    I.poly(d, [P(x, y + B_, HW), P(x + A_, y + B_, HW), apex], LEFT)                # roof, front-left
    I.poly(d, [P(x + A_, y, HW), P(x + A_, y + B_, HW), apex], RIGHT)              # roof, front-right
    for q, k in zip(windows(x, y), wl): d.polygon(q, fill=mix(TOP, INK, k))
    d.polygon(door(x, y), fill=INK if you else MID)

PATH = None
def street_path():
    P = I.P; xd, yd = HOUSES[YOU]; xf, yf = HOUSES[FRIEND]
    return [P(xd + A_ + 10, yd + 89), P(xd + A_ + 30, 210), P(xf - 40, 210), P(xf + A_ + 20, 210), P(xf + A_ + 20, yf + 89 + 30), P(xf + A_ + 4, yf + 89)]
STREAM = Stream(street_path(), n=1400, width=22, seed=4)

def scene(L, d, t):
    I.grid(L)
    h = hours(t); fl = lit(h)
    back = clamp((t - T_BACK) / .4) if t >= T_BACK else 0
    order = sorted(range(len(HOUSES)), key=lambda i: HOUSES[i][0] + HOUSES[i][1])
    for i in order:
        x, y = HOUSES[i]
        if i == YOU: wl = [1, 0, .15 + .1 * math.sin(t * 2)]                       # you: one light on, at home
        elif i == FRIEND: wl = [clamp(fl - j) * (1 - back) for j in range(3)]
        else: wl = [.25 * (((i * 7 + j * 3) % 5) == 0) for j in range(3)]           # the rest of the street, mostly dark
        house(d, x, y, wl, you=i == YOU)
        if i == YOU and S("setup") <= t < T_BACK + .3:
            p = I.P(x + A_ / 2, y + B_ / 2, HW + RF); callout(d, p, "l", p[1] - 70, 1, "YOU", INK, k=(t - S("setup") - .2) / .4)
        if i == FRIEND and S("casual") - .1 <= t < T_BACK + .3:
            p = I.P(x + A_ / 2, y + B_ / 2, HW + RF); callout(d, p, "r", p[1] - 70, 1, "THEM", INK, k=(t - S("casual")) / .4)
    if fl > 0:                                                                        # the friend's lit windows glow
        g = windows(*HOUSES[FRIEND]); glow(L, g[:int(math.ceil(fl))], r=18 + 14 * clamp((h - 90) / 110), k=min(1, fl / 3 + .3) * (1 - back))
    if S("casual") - .2 <= t < T_BACK + .2:                                          # the hours, flowing from your door to theirs
        act = clamp(.15 + h / 200) * (1 - clamp((t - T_BACK) / .3))
        dots(L, STREAM.pos(t, flow=.18 + .25 * clamp(h / 200), active=act), INK, size=4)

def cam(t):
    xy = I.P(*HOUSES[YOU]); fy = I.P(*HOUSES[FRIEND])
    you_f = (xy[0] + 40, xy[1] + 10); fr_f = (fy[0] + 60, fy[1] + 30); mid = (540, 830)
    keys = [(0, 2.1, you_f), (T_PULL - .4, 1.85, you_f), (T_PULL + .9, 1.0, mid), (T200 - .3, 1.0, mid),
            (T200 + .9, 1.75, fr_f), (T_BACK, 1.8, fr_f), (T_BACK + .7, 2.1, you_f)]
    return cam_path(t, keys)

def head(d, t, line, sub=None):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    h = hours(t)
    d.text((X0, 400), "HOURS TOGETHER", font=F(MONO, 30), fill=MID)
    d.text((X0 + 300, 388), f"{h:.0f}" + ("+" if h >= 199.5 else ""), font=F(BLK, 64), fill=SIG if EP.current(t) == "reveal" else INK)
    if sub: d.text((X1, 408), sub, font=F(MONO, 26), fill=MID, anchor="ra")

def draw(img, d, t, line, sub=None, note="survey · self-reported hours"):
    z, f = cam(t); camera(img, lambda L, dL: scene(L, dL, t), z, f)
    head(d, t, line, sub); fig(d, note)

def sc_hook(img, d, t): draw(img, d, t, "NEW CITY.", note="schematic")
def sc_setup(img, d, t): draw(img, d, t, "HOW MANY HOURS?", sub="467 people")
def sc_casual(img, d, t): draw(img, d, t, "CASUAL FRIEND", sub="stranger → casual")
def sc_friend(img, d, t): draw(img, d, t, "FRIEND", sub="casual → friend")
def sc_reveal(img, d, t): draw(img, d, t, "CLOSE FRIEND", sub="over 200 hours")
def sc_why(img, d, t): draw(img, d, t, "MONTHS. NOT YOU." if t < T_BACK else "NEW CITY.", note="hours spent together · a rough guide")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.bg = {k: "dark" for k in ORDER[:-1]}; EP.bg["reveal"] = "orange"
EP.scenes = {"hook": sc_hook, "setup": sc_setup, "casual": sc_casual, "friend": sc_friend, "reveal": sc_reveal, "why": sc_why}
FX = [(.05, whoosh(.9, .04), 0), (T_PULL, whoosh(.8, .05), 0), (S("setup") + .2, pop(.1), -.4),
      (S("casual"), pop(.1), .4), (T50 + .5, pop(.14), .3), (T90 + .6, pop(.14), .3),
      (S("reveal") + .1, thud(.55), 0), (T200 + .8, pop(.16), .3), (T_BACK, whoosh(.6, .05), 0)]
from fx2 import hook_intro
hook_intro(EP)                                                  # big hook in the first 1.7 s (13.11.2026)
if __name__ == "__main__": EP.run(FX)
