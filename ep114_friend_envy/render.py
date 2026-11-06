"""NOT JUST YOU – No. 114: envy among friends – when a word game 'measured intelligence', men gave their friend harder clues
than a stranger in 10 of 13 sessions (Tesser & Smith 1980); responding to good news with enthusiasm went with closer
relationships (Gable et al. 2004). Look C+D · statement opener with "you" · isometric clue cards · orange reveal: harder clues."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from tips import *
HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"game": .6, "matters": .5, "harder": .6, "why": .6, "fix": .6, "point": .7, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["game", "matters", "harder", "why", "fix", "point", "end"]
EP = ThreadEpisode(TL, 114, "FRIEND ENVY", order=ORDER, dark=True, label="EXPERIMENT · SMALL STUDY",
                   chapters={k: "" for k in ORDER[:-1]},
                   sources=("Tesser & Smith (1980), J. of Exp. Social Psych. 16(6) ·", "Gable, Reis, Impett & Asher (2004), JPSP 87(2)"),
                   music=dict(bpm=96, root=0, prog="tense", kick="half", audio="v5", gaps=[(E("game") + .05, S("matters") + .05)]),
                   cover=dict(words=["YOUR FRIEND'S", "SUCCESS", "STINGS."], kicker="That doesn't make you a bad friend."))

I = Iso(500, 1010, .82)
def card(I, d, x, y, z, lab, col=TOP, txt=INK):
    I.box(d, x, y, z, 170, 240, 8, top=col)
    px, py = I.P(x + 85, y + 120, z + 8); d.text((px, py), lab, font=F(BLK, 34), fill=txt, anchor="mm")

def sc_game(img, d, t):
    t0, te = S("game"), cue("game", "easy clues") - .1
    d.text((X0, 320), "WORD GAME", font=F(BLK, 130), fill=INK); d.text((X0 + 4, 460), "you, your friend, a stranger", font=F(COND, 48), fill=MID)
    I.grid(img); I.shadow(d, 0, 0, 260)
    if t >= te:
        for i in range(4):                                  # two stacks of clue cards drop in
            v, dz = drop(t, te + i * .08)
            if v: card(I, d, -260, -120, i * 10 + dz, "EASY" if i == 3 else "")
            v, dz = drop(t, te + .35 + i * .08)
            if v: card(I, d, 80, -120, i * 10 + dz, "HARD" if i == 3 else "", col=RIGHT)
    fig(d, "Password-style game · schematic")

def sc_matters(img, d, t):
    t0, ti = S("matters"), cue("matters", "measured intelligence") - .15
    words_in(d, t, [("THEN:", t0 + .05, 320, 130, MID)])
    if t >= ti: words_in(d, t, [("\"THIS MEASURES", ti, 470, 110, INK), ("INTELLIGENCE.\"", ti + .12, 580, 110, INK)])
    fig(d, "the cover story")

def sc_harder(img, d, t):
    t0, ts = S("harder"), cue("harder", "In ten of") - .1
    words_in(d, t, [("HARDER CLUES", t0 + .05, 320, 120, SIG), ("FOR THE FRIEND.", t0 + .2, 440, 110, INK)])
    if t >= ts:                                             # 10 of 13 sessions
        for i in range(13):
            k = back(clamp((t - ts - i * .05) / .25)); x = X0 + 30 + (i % 7) * 120; y = 640 + (i // 7) * 130; r = 44 * k
            d.rounded_rectangle([x - r, y - r, x + r, y + r], radius=12, fill=SIG if i < 10 else MID)
        d.text((X0, 930), "10 OF 13 SESSIONS", font=F(BLK, 64), fill=INK)
    fig(d, "small study · men only · 1980")

def sc_why(img, d, t):
    t0, ti = S("why"), cue("why", "When it is your") - .1
    d.text((X0, 320), "NOT YOUR THING:", font=F(BLK, 80), fill=MID)
    if t >= t0 + .3: heart(d, X0 + 70, 490, 50 * back(clamp((t - t0 - .3) / .3)), MID); d.text((X0 + 150, 490), "you cheer", font=F(COND, 60), fill=MID, anchor="lm")
    if t >= ti:
        d.text((X0, 620), "YOUR THING:", font=F(BLK, 80), fill=INK)
        k = ease((t - ti) / .3)
        d.text((X0 - (1 - k) * 40, 720), "their win", font=F(COND, 60), fill=INK); d.text((X0 - (1 - k) * 40, 800), "feels like your loss", font=F(COND, 60), fill=INK)
    fig(d, "Tesser's self-evaluation model")

def sc_fix(img, d, t):
    t0, tg = S("fix"), cue("fix", "In studies") - .1
    words_in(d, t, [("CELEBRATE", t0 + .05, 320, 150, INK), ("ANYWAY.", t0 + .2, 470, 150, INK)])
    if t >= tg:
        for j, lab in enumerate(("EXCITED", "CURIOUS")):
            box_label(d, X0 + 4 + j * 330 - (1 - ease((t - tg - j * .2) / .2)) * 40, 680, lab, 60, WHITE, INK, font=BLK) if t >= tg + j * .2 else None
        if t >= tg + .8: d.text((X0, 820), "= closer relationships", font=F(COND, 60), fill=INK)
    fig(d, "a link, not proof")

def sc_point(img, d, t):
    t0, tt = S("point"), cue("point", "tell me everything") - .2
    words_in(d, t, [("FEEL THE STING.", t0 + .05, 320, 110, MID), ("THEN SAY:", t0 + .3, 450, 110, MID)])
    if t >= tt:
        k = back(clamp((t - tt) / .35)); x0, y0 = X0, 610
        d.rounded_rectangle([x0, y0, x0 + 820 * k, y0 + 230 * k], radius=40, fill=SIG)
        d.polygon([(x0 + 80, y0 + 230 * k), (x0 + 60, y0 + 230 * k + 70 * k), (x0 + 170, y0 + 230 * k)], fill=SIG)
        if k > .8: d.text((x0 + 410, y0 + 115), "TELL ME EVERYTHING!", font=F(BLK, 68), fill=WHITE, anchor="mm")
    fig(d, "fig. 2 — say it out loud")

EP.cuts = {"harder": "stay"}
EP.bg = {"game": "light"}
EP.scenes = {"game": sc_game, "matters": sc_matters, "harder": sc_harder, "why": sc_why, "fix": sc_fix, "point": sc_point}
FX = [*EP.cut_fx(), (S("game") + .1, riser(.8, .04), 0), *[(cue("game", "easy clues") - .1 + i * .08, tick(.03), -.3) for i in range(4)], *[(cue("game", "easy clues") + .25 + i * .08, tick(.03), .3) for i in range(4)],
      (S("matters") + .1, thud(.4), 0), (cue("matters", "measured intelligence") - .15, pop(.14), 0),
      (S("harder") + .05, thud(.55), 0), *[(cue("harder", "In ten of") - .1 + i * .05, pop(.07), (i % 7 - 3) / 4) for i in range(13)],
      (S("why") + .3, pop(.12), -.3), (cue("why", "When it is your") - .1, thud(.45), .2),
      (S("fix") + .1, thud(.4), 0), (cue("fix", "In studies") - .1, pop(.13), -.2), (cue("fix", "In studies") + .1, pop(.13), .2),
      (S("point") + .1, pop(.12), 0), (cue("point", "tell me everything") - .2, thud(.5), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
