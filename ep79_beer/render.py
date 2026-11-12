"""NOT JUST YOU – No. 79 (level 2 remake, 12.11.2026): the beer question (OkTrends 2011) – beer fans 60 % more likely to be okay
with a hookup with someone they just met; long-term couples agreed on horror movies / solo travel / sailboat 3.7× more than chance.
Level 2: two pint glasses (= the two of you) are on the table from frame 0, ONE continuous object, the fill level is the data,
the three questions pop up above them, the glasses clink at the end and the loop pours them empty again.
Old version: render_v1.py / script_v1.json."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.05, gaps={"hook": .34, "setup": .34, "reveal": .4, "long": .34, "match": .1})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "setup", "reveal", "long", "match", "end"]
EP = ThreadEpisode(TL, 79, "THE BEER QUESTION", order=ORDER, dark=True, label="PLATFORM DATA · OKCUPID",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("OkTrends (2011), The Best Questions", "For A First Date · OkCupid"),
                   music=dict(bpm=100, root=0, prog="tense", kick="four", audio="v5"),
                   cover=dict(words=["ONE QUESTION", "ON DATE ONE."], kicker="Tells you how the night ends."))

GL, GR, BASE = 300, 660, 1070
T_Q = cue("setup", "do you like") - .1
T_60 = S("reveal") + .1; T_MW = cue("reveal", "Men and women") - .1
T_3 = [cue("long", w) - .15 for w in ("horror", "solo", "sailboat")]
T_ALL = S("match") + .1
T_BACK = cue("match", "Because") - .3

def glass(d, cx, base, k, body, t, s=1.0, lift=0.0):
    """pint glass filled to k (0..1.05), foam + rising bubbles when filled"""
    w0, w1, h = 120 * s, 165 * s, 380 * s; base -= lift
    top = base - h; lvl = base - (h - 30 * s) * clamp(k)
    def xw(y): u = (base - y) / h; return (w0 + (w1 - w0) * u) / 2
    if k > .02:
        d.polygon([(cx - xw(lvl), lvl), (cx + xw(lvl), lvl), (cx + w0 / 2, base), (cx - w0 / 2, base)], fill=body)
        for i in range(6):                                       # foam
            r = 18 * s * min(1, k * 3); fx = cx - xw(lvl) + 14 + i * (2 * xw(lvl) - 28) / 5
            d.ellipse([fx - r, lvl - r * .9, fx + r, lvl + r * .9], fill=WHITE)
        for i in range(6):
            y = base - ((t * 160 + i * 61) % max(20, base - lvl - 30)) - 12; x = cx + math.sin(i * 2.3) * 30 * s
            if y > lvl + 10: d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=BG)
    d.line([(cx - w1 / 2, top), (cx - w0 / 2, base), (cx + w0 / 2, base), (cx + w1 / 2, top)], fill=INK, width=int(8 * s), joint="curve")
    return top, lvl

def fills(t):
    """fill of the left (not a fan) and right (beer fan) glass"""
    back = clamp((t - T_BACK) / .5) if t >= T_BACK else 0
    if t < T_Q: return 0, 0
    base_k = .55 * spring((t - T_Q) / .7, f=1.2, damp=5)
    fan = base_k if t < T_60 else .55 + (.88 - .55) * spring((t - T_60) / .8)
    return base_k * (1 - back), fan * (1 - back)

def scene(d, t):
    wave = (t - .05) / .8; drop = lambda i: -40 * max(0, 1 - abs(wave - i * .3) * 3) if 0 <= wave <= 1.3 else 0     # cold open bounce
    lean = 0.0                                                   # the clink: glasses lean together
    if T_ALL <= t < T_BACK + .4: lean = 60 * spring((t - T_ALL) / .6) * (1 - clamp((t - T_BACK) / .4))
    kl, kr = fills(t); cur = EP.current(t)
    body_l = MID; body_r = SIG if cur == "reveal" else INK
    gl, gr = GL + lean, GR - lean
    glass(d, gl, BASE, kl, body_l, t, lift=-drop(0)); glass(d, gr, BASE, kr, body_r, t, lift=-drop(1))
    d.line([X0, BASE + 4, X1, BASE + 4], fill=MID, width=4)
    if t >= T_Q and t < S("long"):
        k = spring((t - T_Q) / .4)
        d.text((gl, BASE + 22 + 20 * (1 - k)), "NOT A FAN", font=F(MONO, 30), fill=MID, anchor="ma")
        d.text((gr, BASE + 22 + 20 * (1 - k)), "BEER FAN", font=F(MONO, 30), fill=INK, anchor="ma")
    if t < T_Q or t >= T_BACK + .3:                              # the question hangs between the two of you (and again at the loop)
        k = spring((t - (.4 if t < T_Q else T_BACK + .3)) / .6); r = 70 * k
        if r > 2: d.ellipse([(GL + GR) / 2 - r, 580 - r, (GL + GR) / 2 + r, 580 + r], outline=INK, width=8); d.text(((GL + GR) / 2, 580), "?", font=F(BLK, int(max(10, 100 * k))), fill=INK, anchor="mm")
    if S("long") - .2 <= t < T_BACK + .3:                       # the three questions pop up above the glasses
        out = clamp((t - T_BACK) / .3)
        for j, (lab, tk) in enumerate(zip(("HORROR MOVIES?", "SOLO TRIP ABROAD?", "LIFE ON A SAILBOAT?"), T_3)):
            if t < tk: continue
            k = spring((t - tk) / .4) * (1 - out); y = 470 + j * 74
            if k > .05: box_label(d, X0 + 40 + (1 - k) * -60, y, lab, int(40 * min(1, max(.3, k))), WHITE, INK, font=BLK)
            if t >= T_ALL + j * .12 and k > .5:                  # both of you: yes
                kc = spring((t - T_ALL - j * .12) / .3); cx, cy = X1 - 50, y + 26
                d.line([(cx - 22 * kc, cy), (cx - 6, cy + 18 * kc), (cx + 26 * kc, cy - 22 * kc)], fill=INK, width=9, joint="curve")

def head(d, t, line):
    d.text((X0, 300), line, font=F(BLK, 84), fill=INK)
    if T_60 <= t < S("long"):
        v = 1 + .6 * ease(clamp((t - T_60 - .1) / .8))
        d.text((X0, 400), "BEER FANS, NIGHT ONE", font=F(MONO, 30), fill=MID); d.text((X0 + 390, 388), f"×{v:.1f}", font=F(BLK, 64), fill=SIG)
        if t >= T_MW: d.text((X1, 408), "men and women", font=F(MONO, 26), fill=MID, anchor="ra")
    elif T_ALL <= t < T_BACK:
        v = 1 + 2.7 * ease(clamp((t - T_ALL - .1) / .9))
        d.text((X0, 400), "ALL 3 VS. CHANCE", font=F(MONO, 30), fill=MID); d.text((X0 + 330, 388), f"×{v:.1f}", font=F(BLK, 64), fill=INK)
    else:
        d.text((X0, 400), "QUESTIONS", font=F(MONO, 30), fill=MID)
        n = 0 if t < T_Q or t >= T_BACK else 1 if t < T_3[0] else sum(1 for x in T_3 if t >= x)
        d.text((X0 + 210, 388), f"{n}", font=F(BLK, 64), fill=INK)

def sc_hook(img, d, t): head(d, t, "ONE QUESTION."); scene(d, t); fig(d, "first date")
def sc_setup(img, d, t): head(d, t, "“LIKE BEER?”"); scene(d, t); fig(d, "fill = how often they're okay with it")
def sc_reveal(img, d, t): head(d, t, "BEER FANS: +60 %"); scene(d, t); fig(d, "okay with a hookup with someone just met")
def sc_long(img, d, t): head(d, t, "LONG-TERM? ASK 3."); scene(d, t); fig(d, "the questions couples agree on")
def sc_match(img, d, t): head(d, t, "ALMOST 4× CHANCE." if t < T_BACK else "ONE QUESTION."); scene(d, t); fig(d, "32 % of long-term couples agreed on all 3")

EP.cuts = {k: "stay" for k in ORDER[1:]}
EP.bg = {"hook": "dark", "setup": "dark", "reveal": "orange", "long": "dark", "match": "dark"}
EP.scenes = {"hook": sc_hook, "setup": sc_setup, "reveal": sc_reveal, "long": sc_long, "match": sc_match}
FX = [(.05, whoosh(.8, .05), 0), (.4, pop(.12), 0), (T_Q, whoosh(.6, .04), 0),
      (T_60, thud(.55), 0), (T_60 + .4, pop(.14), .3), (T_MW, pop(.1), -.2),
      *[(x, pop(.12), (j - 1) / 2) for j, x in enumerate(T_3)],
      (T_ALL, pop(.1), -.3), (T_ALL + .5, pop(.16), 0), (T_BACK, whoosh(.45, .05), 0)]
if __name__ == "__main__": EP.run(FX)
