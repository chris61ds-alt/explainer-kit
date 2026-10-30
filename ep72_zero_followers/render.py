"""NOT JUST YOU – No. 72 (special): 'basically no followers' – comment-to-content call. Look C+D, dark.
The arrow points to the comment icon of the Instagram Reels UI (right rail, around y≈1390 on 1080x1920)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from thread import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .6, "what": .6, "deal": .5, "next": .6, "point": 1.2, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "what", "deal", "next", "point", "end"]
EP = ThreadEpisode(TL, 72, "YOU DECIDE", order=ORDER, dark=True,
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("No study this time.", "Your comment might be the next one."),
                   music=dict(bpm=104, root=0, prog="tense", kick="four"),
                   cover=dict(words=["YOU", "DECIDE."], kicker="Top comment = next video."))
COMMENT_XY = (1000, 1390)

def arrow_to(d, x0, y0, x1, y1, k=1.0, col=SIG, w=14):
    if k <= 0: return
    pts = spline([(x0, y0), ((x0 + x1) / 2, y0 + 30), (x1 - 60, y1 - 60)])
    n = max(2, int(len(pts) * ease(k))); d.line(pts[:n], fill=col, width=w, joint="curve")
    if k > .95:
        ax, ay = pts[-1]; a = math.atan2(y1 - ay, x1 - ax); L = 48
        d.polygon([(x1, y1), (x1 - L * math.cos(a - .5), y1 - L * math.sin(a - .5)), (x1 - L * math.cos(a + .5), y1 - L * math.sin(a + .5))], fill=col)

def sc_hook(img, d, t):
    counter(d, X0 - 6, 320, t, .3, .8, 0, "{:.0f}", 330, SIG) if False else d.text((X0 - 6, 300), "0", font=F(BLK, 360), fill=SIG)
    d.text((X0 + 230, 380), "followers.", font=F(BLK, 110), fill=INK); d.text((X0 + 236, 510), "(basically)", font=F(COND, 46), fill=MID)
    silhouette(img, lambda m: front_bust(m, 480, 880, .62, 255), (160, 760, 800, 1130), INK, cell=10)
    if t >= cue("hook", "let's fix") - .2: box_label(d, X0, 680, "LET'S FIX THAT.", 44, WHITE, SIG, font=BLK)
    fig(d, "fig. 1 — a brand new account")

def sc_what(img, d, t):
    t0, tn = S("what"), cue("what", "you're not alone") - .3
    d.text((X0, 320), "\"ONLY ME?\"", font=F(BLK, 150), fill=INK)
    k = clamp((t - tn) / 1.0)
    for i in range(36):
        r, c = divmod(i, 9); x = X0 + 50 + c * 96; y = 640 + r * 120
        on = i == 13 or i < 36 * k
        silhouette(img, lambda m, x=x, y=y: front_bust(m, x, y, .17, 255), (x - 50, y - 30, x + 50, y + 90), SIG if i == 13 else (INK if on else RULE), cell=5)
    if t >= tn: box_label(d, X1, 500, "NOT ALONE", 44, WHITE, SIG, font=BLK, anchor="ra")
    fig(d, "every video so far")

def sc_deal(img, d, t):
    t0 = S("deal")
    d.text((X0, 320), "THE DEAL:", font=F(BLK, 150), fill=INK)
    words_in(d, t, [("COMMENT", cue("deal", "comment") - .2, 500, 150, SIG), ("YOUR SECRET", cue("deal", "secretly") - .2, 660, 110, INK), ("\"NOT NORMAL\".", cue("deal", "isn't normal") - .2, 780, 110, INK)])
    fig(d, "anything you think only you do")

def sc_next(img, d, t):
    t0 = S("next")
    d.text((X0, 320), "TOP COMMENT", font=F(BLK, 130), fill=INK); d.text((X0, 470), "= NEXT VIDEO", font=F(BLK, 130), fill=SIG)
    for i, lab in enumerate(("REAL RESEARCH", "NO JUDGMENT")):
        k = ease((t - cue("next", "real research" if i == 0 else "no judgment") + .2) / .3)
        if k > 0: box_label(d, X0 + (1 - k) * 40, 680 + i * 110, lab, 50, WHITE, INK if i == 0 else SIG, font=BLK)
    fig(d, "we read every comment")

def sc_point(img, d, t):
    t0 = S("point")
    words_in(d, t, [("GO.", t0, 320, 260, SIG), ("COMMENTS.", cue("point", "comments") - .1, 600, 150, INK), ("NOW.", cue("point", "now") - .1, 760, 150, SIG)])
    fig(d, "fig. 2 — right there")

_compose = EP.compose
def compose_with_arrow(img, d, t):
    """the arrow leaves the content band, so it is drawn on top of the finished frame"""
    _compose(img, d, t)
    cur = EP.current(t)
    if cur in ("deal", "next", "point"):
        k = 1 if cur != "deal" else (t - cue("deal", "comment")) / .5
        w = int(12 + 6 * (.5 + .5 * math.sin(t * 10))) if cur == "point" else 14
        arrow_to(d, 880, 980, *COMMENT_XY, k=k, w=w)
EP.compose = compose_with_arrow

EP.scenes = {"hook": sc_hook, "what": sc_what, "deal": sc_deal, "next": sc_next, "point": sc_point}
FX = [(0.0, thud(.55), 0), (cue("hook", "let's fix") - .2, pop(.15), 0), *EP.cut_fx(), (cue("what", "you're not alone") - .3, riser(.6, .05), 0),
      (cue("deal", "comment") - .2, thud(.45), .3), (cue("deal", "comment"), whoosh(.5, .08), .5), (cue("next", "real research") - .2, pop(.15), 0),
      (cue("next", "no judgment") - .2, pop(.15), 0), (S("point"), thud(.55), 0), (cue("point", "comments") - .1, thud(.4), .4), (cue("point", "now") - .1, thud(.5), .5), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
