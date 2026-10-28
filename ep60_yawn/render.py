"""NOT JUST YOU – No. 60 (format test: UNSOLVED + interactive): contagious yawning (Provine 1986), function still unknown.
v3 'Swiss Thread', light. The thread carries the yawn from head to head."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from thread import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .7, "read": .6, "watch": .8, "unsolved": .6, "theories": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "read", "watch", "unsolved", "theories", "point", "end"]
EP = ThreadEpisode(TL, 60, "THE YAWN", order=ORDER, dark=os.environ.get("V3_DARK") == "1", label="UNSOLVED",
                   chapters={"hook": "WARNING", "read": "READING", "watch": "WATCHING", "unsolved": "WHY?", "theories": "THEORIES", "point": "DID YOU?"},
                   sources=("Provine (1986), Ethology 72 · function of yawning", "still debated (brain cooling, empathy)"),
                   music=dict(bpm=70, root=3, prog="dream", kick="half", gaps=[(E("watch") + .05, S("unsolved") + .05)]),
                   cover=dict(words=["YOU'LL", "YAWN."], kicker="Science can't explain why."))

STRETCH = {"arms": ((165, 175), (-160, -170)), "tilt": -4}
def yawn_amt(t, t0, dur=2.4):
    u = (t - t0) / dur
    return 0.0 if u <= 0 or u >= 1 else math.sin(u * math.pi) ** 1.5

def yawner(d, x, y, s, col, open_k):
    h = picto(d, x, y, s, col, f=1, pose=blend(IDLE, STRETCH, open_k * .9), head_dy=-6 * open_k)
    rx, ry = 14 * s + 6 * s * open_k, 4 * s + 26 * s * open_k
    d.ellipse([h[0] - rx, h[1] + 4 * s - ry * .4, h[0] + rx, h[1] + 4 * s + ry], fill=BG)
    return h

def big_mouth(d, cx, cy, k, col=INK):
    rx, ry = 150 + 40 * k, 24 + 190 * k
    d.ellipse([cx - rx - 30, cy - ry - 30, cx + rx + 30, cy + ry + 30], fill=col)
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=BG)
    if k > .4: d.ellipse([cx - 60 * k, cy + ry * .35, cx + 60 * k, cy + ry * .85], fill=SIG)    # tongue

def sc_hook(img, d, t):
    k = yawn_amt(t, .3, 2.6)
    d.text((X0 - 6, 320), "YOU'LL", font=F(BLK, 200), fill=INK); d.text((X0 - 6, 520), "YAWN.", font=F(BLK, 200), fill=SIG)
    big_mouth(d, 620, 860, k)
    bbox(d, (430, 650, 810, 1070), "MOUTH", SIG, (t - .4) / .3, size=18)
    d.line(trace(LX, 380, THREAD_Y, t, amp=6, seed=2), fill=SIG, width=6)
    fig(d, "fig. 1 — this is a trap")

def sc_read(img, d, t):
    t0, tq = S("read"), cue("read", "over a quarter") - .2
    counter(d, X0, 320, t, tq, .6, 25, "> {:.0f} %", 200, SIG)
    d.text((X0 + 6, 540), "yawned just from reading about it", font=F(COND, 38), fill=INK)
    for i in range(7):
        y = 640 + i * 44; w_ = 760 - (i * 97) % 260
        d.rectangle([X0, y, X0 + w_, y + 18], fill=RULE)
        if i in (1, 4):
            xx = X0 + 120 + i * 60; d.rectangle([xx, y - 8, xx + 150, y + 26], fill=SIG); d.text((xx + 75, y + 9), "yawn", font=F(MONO, 22), fill=WHITE, anchor="mm")
    d.line(trace(LX, RX, THREAD_Y + 120, t, amp=5, seed=4), fill=SIG, width=6)
    fig(d, "reading a passage about yawning · Provine, 1986")

def sc_watch(img, d, t):
    t0 = S("watch")
    d.text((X0, 320), "WATCHING", font=F(BLK, 150), fill=INK); d.text((X0, 470), "IT SPREADS", font=F(BLK, 120), fill=SIG)
    xs = [150, 330, 510, 690, 860]
    heads = []
    for i, x in enumerate(xs):
        k = yawn_amt(t, t0 + .2 + i * .55, 2.0)
        heads.append(yawner(d, x, 1100, .55, SIG if k > .1 else INK, k))
    kk = clamp((t - t0 - .2) / (len(xs) * .55 + .4))
    draw_thread(d, path((LX, THREAD_Y), *[(h[0], h[1] - 70) for h in heads], (RX, THREAD_Y)), kk, SIG, width=5)
    if t >= cue("watch", "five minutes") - .2: box_label(d, X1, 600, "MOST · WITHIN 5 MIN", 30, WHITE, INK, anchor="ra")
    fig(d, "watching videotaped yawns · Provine, 1986")

def sc_unsolved(img, d, t):
    t0, tn = S("unsolved"), cue("unsolved", "science still")
    d.text((X0 - 10, 300), "WHY?", font=F(BLK, 300), fill=INK)
    if t >= tn - .1:
        k = back((t - tn + .1) / .4)
        st = Image.new("RGBA", (560, 160), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
        sd.rectangle([6, 6, 554, 154], outline=SIG + (255,), width=10); sd.text((280, 80), "UNSOLVED", font=F(BLK, 96), fill=SIG + (255,), anchor="mm")
        st = st.resize((max(1, int(560 * k)), max(1, int(160 * k)))).rotate(-8, expand=True)
        img.paste(st, (int(480 - st.width / 2), int(720 - st.height / 2)), st)
        if t < tn + .25: glitch(img, (X0, 300, X1, 900), .8, seed=int(t * 30))
    d.line([(LX, THREAD_Y + 140), (RX, THREAD_Y + 140)], fill=SIG, width=6)
    fig(d, "the function of yawning is still debated")

def sc_theories(img, d, t):
    t0, te = S("theories"), cue("theories", "another") - .2
    tn = cue("theories", "neither")
    d.text((X0, 320), "TWO IDEAS", font=F(BLK, 130), fill=INK)
    # 1 brain cooling: thermometer
    x0 = X0; d.rectangle([x0, 500, x0 + 400, 900], outline=INK, width=4); d.text((x0 + 20, 520), "01  BRAIN COOLING", font=F(MONO, 24), fill=INK)
    lvl = .7 - .3 * clamp((t - t0 - .4) / 1.2)
    d.rounded_rectangle([x0 + 180, 600, x0 + 220, 820], radius=20, outline=INK, width=4); d.ellipse([x0 + 165, 800, x0 + 235, 870], fill=SIG)
    d.rectangle([x0 + 188, 820 - 210 * lvl, x0 + 212, 830], fill=SIG)
    # 2 empathy: two heads connected
    if t >= te:
        x1 = X0 + 440; d.rectangle([x1, 500, x1 + 400, 900], outline=INK, width=4); d.text((x1 + 20, 520), "02  EMPATHY", font=F(MONO, 24), fill=INK)
        for j, hx in enumerate((x1 + 110, x1 + 290)): d.ellipse([hx - 50, 640, hx + 50, 740], fill=INK if j == 0 else SIG)
        d.line(spline([(x1 + 160, 690), (x1 + 200, 640), (x1 + 240, 690)]), fill=SIG, width=5)
    if t >= tn - .1:
        st = Image.new("RGBA", (640, 120), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
        sd.rectangle([5, 5, 635, 115], outline=INK + (255,), width=8); sd.text((320, 60), "NOT SETTLED", font=F(BLK, 80), fill=INK + (255,), anchor="mm")
        st = st.rotate(6, expand=True); img.paste(st, (int(480 - st.width / 2), 640), st)
    d.line([(LX, THREAD_Y + 140), (RX, THREAD_Y + 140)], fill=SIG, width=6)
    fig(d, "hypotheses, not answers")

def sc_point(img, d, t):
    t0, tc = S("point"), cue("point", "comment") - .2
    words_in(d, t, [("DID YOU", t0, 320, 170, INK), ("YAWN?", t0 + .3, 500, 170, SIG)])
    yawner(d, 300, 1100, .7, INK, yawn_amt(t, t0 + .4, 2.2))
    if t >= tc: box_label(d, 560, 760, "COMMENT: Y", 50, WHITE, SIG, font=BLK)
    fig(d, "fig. 2 — be honest")

EP.scenes = {"hook": sc_hook, "read": sc_read, "watch": sc_watch, "unsolved": sc_unsolved, "theories": sc_theories, "point": sc_point}
def yawn_sfx(amp=.05, dur=1.6):
    t = tt_(dur); env = np.sin(np.pi * t / dur) ** 2
    return amp * env * lp(np.random.default_rng(3).standard_normal(len(t)), 900) * 3
FX = [(0.0, thud(.4), 0), (.4, yawn_sfx(.05, 2.2), 0), (cue("hook", "before"), pop(.12), 0), *EP.cut_fx(),
      (cue("read", "over a quarter") - .2, pop(.15), 0), *[(S("watch") + .2 + i * .55, pop(.1), (i - 2) / 3) for i in range(5)],
      (cue("unsolved", "science still") - .1, thud(.6), 0), (cue("unsolved", "science still") - .1, rewind_sfx(.1, .3), 0),
      (cue("theories", "another") - .2, pop(.15), .3), (cue("theories", "neither") - .1, thud(.45), 0),
      (cue("point", "comment") - .2, pop(.18), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
